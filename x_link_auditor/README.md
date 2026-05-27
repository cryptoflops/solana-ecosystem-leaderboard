# X-Link Auditor

Reads a CSV of X/Twitter account URLs and produces a clean audit report
flagging dead, suspended, inactive, or suspicious accounts.

## Quick Start

```bash
pip install -r requirements.txt
```

### Mode 1 — X API v2 (most accurate, free Basic tier works)

1. Get a Bearer Token from [developer.x.com](https://developer.x.com).
2. Run:

```bash
python auditor.py \
  --input solana_twitter_verified.csv \
  --mode api \
  --bearer-token YOUR_BEARER_TOKEN \
  --output-dir audit_output
```

### Mode 2 — Scraper / No API key

1. Fill in `cookies_template.json` → save as `cookies.json`.
2. Run:

```bash
python auditor.py \
  --input solana_twitter_verified.csv \
  --mode scraper \
  --cookies cookies.json \
  --output-dir audit_output
```

### Mode 3 — HTTP Probe only (no auth, no metrics)

Detects dead links (404 / "This account doesn't exist") without
any credentials. No follower counts or post timestamps.

```bash
python auditor.py \
  --input solana_twitter_verified.csv \
  --mode probe \
  --output-dir audit_output
```

## Input CSV Format

The CSV must have a column named one of:
`Twitter URL`, `twitter_url`, `url`, `X URL`, `link`, or `twitter`.

Example (matches the verified Solana CSV from this project):

| Group Name | Twitter URL | Name | Note | ... |
|---|---|---|---|---|
| Core Founders | https://twitter.com/toly | Anatoly Yakovenko | Co-founder... | ... |

## Output Files

| File | Contents |
|---|---|
| `audit_report_<ts>.csv` | All accounts with full metrics + flags |
| `flagged_<ts>.csv` | Only accounts with at least one flag |
| `summary_<ts>.txt` | Human-readable summary of the run |

## Flags

| Flag | Meaning |
|---|---|
| `OK` | No issues detected |
| `DEAD_LINK` | URL returns 404 / "account doesn't exist" |
| `SUSPENDED` | Account is suspended by X |
| `LOW_FOLLOWERS` | Followers < 100 |
| `INACTIVE_<N>d` | No posts in N days (threshold: 90 days) |
| `NO_RECENT_POSTS` | No tweet data available to check recency |
| `SUSPICIOUS_LOW_ENGAGEMENT` | Followers < 50 on account older than 1 year |
| `CHECK_MANUALLY` | API/scraper error — could not determine status |

## Tuning Thresholds

Edit the constants at the top of `auditor.py`:

```python
INACTIVE_DAYS_THRESHOLD  = 90   # flag if last post > N days ago
LOW_FOLLOWER_THRESHOLD   = 100  # flag if followers < N
SUSPICIOUS_FOLLOWER_MAX  = 50   # suspicious if followers < N AND account > 1yr
```

## Security Notes

- Never commit `cookies.json` or your Bearer Token to git.
- Add both to `.gitignore` immediately.
- The scraper mode uses your personal X session — use a dedicated burner account.
