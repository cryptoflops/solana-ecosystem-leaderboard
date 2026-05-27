#!/usr/bin/env python3
"""
X-Link Auditor
==============
Reads a CSV of X/Twitter account URLs, checks each account for:
  - Existence (live / suspended / not found)
  - Follower count
  - Recent post timestamp (days since last post)
  - Suspicion flags

Outputs a detailed report CSV + a summary.

Usage
-----
  # Mode 1: X API v2 (recommended, free Basic tier is sufficient)
  python auditor.py --input accounts.csv --mode api --bearer-token YOUR_BEARER_TOKEN

  # Mode 2: Scraper fallback (no API key, requires X login cookies)
  python auditor.py --input accounts.csv --mode scraper --cookies cookies.json

  # Mode 3: HTTP probe only (no auth — detects dead links, no metrics)
  python auditor.py --input accounts.csv --mode probe
"""

import argparse
import asyncio
import csv
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("auditor")

# ── Thresholds (tune as needed) ───────────────────────────────────────────────
INACTIVE_DAYS_THRESHOLD  = 90   # flag if last post > N days ago
LOW_FOLLOWER_THRESHOLD   = 100  # flag if followers < N
SUSPICIOUS_FOLLOWER_MAX  = 50   # flag if followers < N AND account > 1 year old
RATE_LIMIT_SLEEP         = 1.0  # seconds between API calls


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def extract_handle(url: str) -> str | None:
    """Extract @handle from a twitter.com or x.com URL."""
    url = url.strip().rstrip("/")
    for prefix in ("https://twitter.com/", "https://x.com/",
                   "http://twitter.com/", "http://x.com/",
                   "twitter.com/", "x.com/"):
        if url.lower().startswith(prefix):
            handle = url[len(prefix):].split("/")[0].split("?")[0]
            return handle if handle else None
    # bare @handle
    if url.startswith("@"):
        return url[1:]
    return None


def days_since(iso_str: str | None) -> int | None:
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return None


def build_flags(row: dict) -> list[str]:
    flags = []
    status = row.get("status", "")

    if status == "NOT_FOUND":
        flags.append("DEAD_LINK")
    elif status == "SUSPENDED":
        flags.append("SUSPENDED")
    elif status == "ERROR":
        flags.append("CHECK_MANUALLY")

    if status == "LIVE":
        followers = row.get("followers")
        last_post_days = row.get("last_post_days")

        if followers is not None and followers < LOW_FOLLOWER_THRESHOLD:
            flags.append("LOW_FOLLOWERS")

        if last_post_days is not None and last_post_days > INACTIVE_DAYS_THRESHOLD:
            flags.append(f"INACTIVE_{last_post_days}d")
        elif last_post_days is None:
            flags.append("NO_RECENT_POSTS")

        # Suspicious: very low followers on an old account
        if followers is not None and followers < SUSPICIOUS_FOLLOWER_MAX:
            created = row.get("account_created_at")
            if created:
                age_days = days_since(created)
                if age_days and age_days > 365:
                    flags.append("SUSPICIOUS_LOW_ENGAGEMENT")

    return flags


# ─────────────────────────────────────────────────────────────────────────────
# MODE 1 — X API v2 via Tweepy
# ─────────────────────────────────────────────────────────────────────────────

def audit_api(handles: list[str], bearer_token: str) -> list[dict]:
    try:
        import tweepy
    except ImportError:
        log.error("tweepy not installed. Run: pip install tweepy")
        sys.exit(1)

    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
    results = []

    # Batch up to 100 handles per request (API v2 limit)
    BATCH = 100
    for i in range(0, len(handles), BATCH):
        batch = handles[i : i + BATCH]
        log.info(f"API batch {i//BATCH + 1}: querying {len(batch)} handles…")

        try:
            resp = client.get_users(
                usernames=batch,
                user_fields=[
                    "public_metrics", "created_at", "description",
                    "verified", "most_recent_tweet_id", "pinned_tweet_id"
                ],
                expansions=["most_recent_tweet_id"],
                tweet_fields=["created_at"],
            )
        except tweepy.errors.TweepyException as e:
            log.error(f"API error: {e}")
            for h in batch:
                results.append({"handle": h, "status": "ERROR", "error": str(e), "flags": ["CHECK_MANUALLY"]})
            continue

        found_map = {}
        if resp.data:
            for user in resp.data:
                found_map[user.username.lower()] = user

        tweet_map = {}
        if resp.includes and "tweets" in resp.includes:
            for tw in resp.includes["tweets"]:
                tweet_map[tw.id] = tw

        for h in batch:
            user = found_map.get(h.lower())
            if not user:
                # Check errors list for suspension
                suspended = False
                if resp.errors:
                    for err in resp.errors:
                        if err.get("value", "").lower() == h.lower():
                            if "suspended" in err.get("detail", "").lower():
                                suspended = True
                status = "SUSPENDED" if suspended else "NOT_FOUND"
                row = {"handle": h, "status": status}
                row["flags"] = build_flags(row)
                results.append(row)
                continue

            pm = user.public_metrics or {}
            last_tweet = tweet_map.get(user.most_recent_tweet_id) if user.most_recent_tweet_id else None
            last_post_iso = last_tweet.created_at.isoformat() if last_tweet and last_tweet.created_at else None
            created_iso   = user.created_at.isoformat() if user.created_at else None

            row = {
                "handle":            user.username,
                "display_name":      user.name,
                "status":            "LIVE",
                "followers":         pm.get("followers_count"),
                "following":         pm.get("following_count"),
                "tweet_count":       pm.get("tweet_count"),
                "listed_count":      pm.get("listed_count"),
                "verified":          user.verified,
                "account_created_at": created_iso,
                "last_post_iso":     last_post_iso,
                "last_post_days":    days_since(last_post_iso),
                "bio":               (user.description or "")[:120],
            }
            row["flags"] = build_flags(row)
            results.append(row)

        time.sleep(RATE_LIMIT_SLEEP)

    return results


# ─────────────────────────────────────────────────────────────────────────────
# MODE 2 — twscrape (no API key, uses X login session)
# ─────────────────────────────────────────────────────────────────────────────

async def _scrape_users(handles: list[str], cookies_path: str) -> list[dict]:
    try:
        from twscrape import API as TwAPI, gather
    except ImportError:
        log.error("twscrape not installed. Run: pip install twscrape")
        sys.exit(1)

    api = TwAPI()

    # Load saved cookies/session
    with open(cookies_path) as f:
        cookies = json.load(f)

    await api.pool.add_account(
        username=cookies["username"],
        password=cookies["password"],
        email=cookies.get("email", ""),
        email_password=cookies.get("email_password", ""),
        cookies=cookies.get("cookies", ""),
    )
    await api.pool.login_all()

    results = []
    for h in handles:
        log.info(f"Scraping @{h}…")
        try:
            user = await api.user_by_login(h)
            if user is None:
                row = {"handle": h, "status": "NOT_FOUND"}
                row["flags"] = build_flags(row)
                results.append(row)
                continue

            # Get most recent tweet
            tweets = await gather(api.user_tweets(user.id, limit=1))
            last_post_iso = tweets[0].date.isoformat() if tweets else None

            row = {
                "handle":             user.username,
                "display_name":       user.displayname,
                "status":             "LIVE",
                "followers":          user.followersCount,
                "following":          user.friendsCount,
                "tweet_count":        user.statusesCount,
                "listed_count":       user.listedCount,
                "verified":           user.verified or user.blue,
                "account_created_at": user.created.isoformat() if user.created else None,
                "last_post_iso":      last_post_iso,
                "last_post_days":     days_since(last_post_iso),
                "bio":                (user.rawDescription or "")[:120],
            }
            row["flags"] = build_flags(row)
            results.append(row)

        except Exception as e:
            msg = str(e).lower()
            if "suspend" in msg:
                row = {"handle": h, "status": "SUSPENDED"}
            elif "not found" in msg or "does not exist" in msg:
                row = {"handle": h, "status": "NOT_FOUND"}
            else:
                row = {"handle": h, "status": "ERROR", "error": str(e)}
            row["flags"] = build_flags(row)
            results.append(row)

        await asyncio.sleep(RATE_LIMIT_SLEEP)

    return results


def audit_scraper(handles: list[str], cookies_path: str) -> list[dict]:
    return asyncio.run(_scrape_users(handles, cookies_path))


# ─────────────────────────────────────────────────────────────────────────────
# MODE 3 — HTTP probe only (no auth)
# ─────────────────────────────────────────────────────────────────────────────

def audit_probe(handles: list[str]) -> list[dict]:
    """
    HEAD-request each x.com/<handle> URL.
    Detects 404 (not found) and some suspensions.
    Cannot retrieve follower counts — marks metrics as None.
    """
    results = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    with httpx.Client(follow_redirects=True, timeout=10, headers=headers) as client:
        for h in handles:
            url = f"https://x.com/{h}"
            log.info(f"Probing {url}…")
            try:
                resp = client.get(url)
                if resp.status_code == 404:
                    status = "NOT_FOUND"
                elif resp.status_code == 200:
                    body = resp.text
                    if "This account doesn" in body or "account doesn" in body:
                        status = "NOT_FOUND"
                    elif "Account suspended" in body or "suspended" in body.lower()[:500]:
                        status = "SUSPENDED"
                    else:
                        status = "LIVE_UNVERIFIED"  # metrics not available in probe mode
                else:
                    status = f"HTTP_{resp.status_code}"
            except Exception as e:
                status = "ERROR"
                log.warning(f"  Error probing @{h}: {e}")

            row = {"handle": h, "status": status,
                   "followers": None, "last_post_days": None}
            row["flags"] = build_flags(row)
            results.append(row)
            time.sleep(RATE_LIMIT_SLEEP)

    return results


# ─────────────────────────────────────────────────────────────────────────────
# REPORT WRITER
# ─────────────────────────────────────────────────────────────────────────────

REPORT_FIELDS = [
    "handle", "display_name", "status", "followers", "following",
    "tweet_count", "listed_count", "verified", "account_created_at",
    "last_post_iso", "last_post_days", "bio", "flags", "error",
]

def write_report(results: list[dict], output_dir: Path, input_csv: Path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path  = output_dir / f"audit_report_{ts}.csv"
    flagged_path = output_dir / f"flagged_{ts}.csv"
    summary_path = output_dir / f"summary_{ts}.txt"

    # Normalise flags to string
    for r in results:
        r["flags"] = "|".join(r.get("flags") or []) or "OK"

    # Full report
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REPORT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    # Flagged-only report
    flagged = [r for r in results if r["flags"] != "OK"]
    with open(flagged_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REPORT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(flagged)

    # Summary
    total      = len(results)
    live       = sum(1 for r in results if r["status"] in ("LIVE", "LIVE_UNVERIFIED"))
    not_found  = sum(1 for r in results if r["status"] == "NOT_FOUND")
    suspended  = sum(1 for r in results if r["status"] == "SUSPENDED")
    errors     = sum(1 for r in results if r["status"] == "ERROR")
    n_flagged  = len(flagged)

    summary = f"""
X-Link Audit Summary
====================
Run at   : {datetime.now().isoformat()}
Input    : {input_csv}

Accounts audited : {total}
  LIVE           : {live}
  NOT FOUND      : {not_found}
  SUSPENDED      : {suspended}
  ERROR          : {errors}

Flagged for review : {n_flagged} ({n_flagged/total*100:.1f}%)

Flag breakdown:
"""
    flag_counts: dict[str, int] = {}
    for r in results:
        for flag in r["flags"].split("|"):
            if flag and flag != "OK":
                flag_counts[flag] = flag_counts.get(flag, 0) + 1
    for flag, count in sorted(flag_counts.items(), key=lambda x: -x[1]):
        summary += f"  {flag:<35} {count}\n"

    summary += f"""
Output files:
  Full report  : {report_path}
  Flagged only : {flagged_path}
"""
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    log.info(summary)
    return report_path, flagged_path, summary_path


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def load_handles_from_csv(path: str) -> list[tuple[str, str]]:
    """Returns list of (original_url, handle) from the CSV."""
    pairs = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        url_col = None
        for col in reader.fieldnames or []:
            if col.lower() in ("twitter url", "twitter_url", "url", "x url", "link", "twitter"):
                url_col = col
                break
        if not url_col:
            log.error(f"Could not find a URL column in {path}. "
                      f"Columns found: {reader.fieldnames}")
            sys.exit(1)
        for row in reader:
            url = row[url_col].strip()
            handle = extract_handle(url)
            if handle:
                pairs.append((url, handle))
            else:
                log.warning(f"Could not parse handle from: {url!r}")
    return pairs


def main():
    parser = argparse.ArgumentParser(description="X-Link Auditor")
    parser.add_argument("--input",        required=True, help="Input CSV path")
    parser.add_argument("--output-dir",   default="audit_output", help="Output directory")
    parser.add_argument("--mode",         choices=["api", "scraper", "probe"], default="probe")
    parser.add_argument("--bearer-token", default="", help="X API v2 Bearer Token (mode=api)")
    parser.add_argument("--cookies",      default="cookies.json",
                        help="Path to cookies JSON for twscrape (mode=scraper)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pairs = load_handles_from_csv(args.input)
    log.info(f"Loaded {len(pairs)} handles from {args.input}")
    handles = [h for _, h in pairs]

    if args.mode == "api":
        if not args.bearer_token:
            log.error("--bearer-token is required for mode=api")
            sys.exit(1)
        results = audit_api(handles, args.bearer_token)

    elif args.mode == "scraper":
        results = audit_scraper(handles, args.cookies)

    else:  # probe
        results = audit_probe(handles)

    write_report(results, output_dir, Path(args.input))


if __name__ == "__main__":
    main()
