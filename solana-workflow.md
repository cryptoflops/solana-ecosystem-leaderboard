# Workflow: Solana Ecosystem Directory & Live Dashboard

This workflow documents the step-by-step process to maintain, verify, compile, and deploy the Solana Ecosystem X.com directory and live dashboard.

## Overview of Components

1. **Source Directory**: [solana_influential_accounts.csv](file:///Users/psyhodivka/.gemini/antigravity-ide/scratch/solana-twitter-research/solana_influential_accounts.csv) (the source of truth for accounts, names, categories, and founder notes).
2. **Dashboard Template**: [dashboard_template.html](file:///Users/psyhodivka/.gemini/antigravity-ide/scratch/solana-twitter-research/dashboard_template.html) (HTML structure, CSS variables, glassmorphic layout, and Chart.js settings).
3. **Data Database**: [data.json](file:///Users/psyhodivka/.gemini/antigravity-ide/scratch/solana-twitter-research/data.json) (compiled intermediate JSON data).
4. **Interactive Dashboard**: [index.html](file:///Users/psyhodivka/.gemini/antigravity-ide/scratch/solana-twitter-research/index.html) (the compiled, portable web app).

---

## The Workflow Steps

### Step 1: Directory Update & Verification
Whenever you add or modify accounts in [solana_influential_accounts.csv](file:///Users/psyhodivka/.gemini/antigravity-ide/scratch/solana-twitter-research/solana_influential_accounts.csv), verify that the links contain no formatting errors, spaces, non-ASCII homoglyphs, or duplicates:

```bash
node check_csv_links.js
```

### Step 2: Merge Data & Compile Database
Run the merge script to parse the CSV file, normalize handles, synthesize active metrics, and generate the unified database `data.json`:

```bash
node merge_data.js
```
*(This script reads the metadata of the top accounts from the original spec and matches them with your curated CSV to construct high-fidelity profiles).*

### Step 3: Build the Dashboard
Compile the portable single-page app `index.html` from the HTML template and the newly generated database:

```bash
node build_dashboard.js
```

### Step 4: Validate Script Syntax
Before publishing, ensure the embedded JavaScript code compiles with zero syntax errors:

```bash
node verify_js.js
```

### Step 5: Local Testing
You can open `index.html` directly in any web browser (`file://` protocol) or start a lightweight local web server to verify features:

```bash
npx http-server .
```

### Step 6: Deploy Changes
Push the updated files to GitHub and Vercel will automatically rebuild and deploy the new dashboard (configured in `package.json`):

```bash
git add .
git commit -m "Update Solana directory and rebuild dashboard"
git push origin main
```