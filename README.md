# Solana Ecosystem X (Twitter) Leaderboard & Directory

An interactive, responsive leaderboard and directory showcasing the most influential X (Twitter) accounts in the Solana ecosystem. Consolidates founders, OGs, core developers, researchers, marketers, and regional hubs to help new builders navigate the ecosystem.

## Live Demo
Deployed and hosted on Vercel.

## Features
- **Trending Metrics**: Top 4 fastest-growing accounts based on 90-day follower growth rates.
- **Dynamic Charting**: Category distribution and follower reach visualization using Chart.js.
- **Advanced Filters**: Real-time fuzzy search, category quick-pills, and sliders for weekly tweet activity and engagement rates.
- **Sortable Directory Table**: Responsive list displaying handles, project associations, exact followers, weekly tweet volumes, and engagement percentages.
- **Profile Modals**: Detailed profiles containing account notes, project contexts, and follow shortcuts.
- **No-Framework Portability**: Structured in semantic HTML, styled with custom Vanilla CSS variables, and powered by raw JavaScript. The database is embedded, enabling it to run cleanly under the `file://` protocol without CORS blocks.

## Development & Build Setup

The database is unified and compiled using a simple local Node build system:
1. `data.json`: The database compiled from the raw directory.
2. `merge_data.js`: A script that parses CSV lists and Markdown files to output `data.json`.
3. `build_dashboard.js`: The compilation builder that injects `data.json` into the `dashboard_template.html` template to generate `index.html`.

### Run Locally
Simply clone the repository and open `index.html` directly in your browser:
```bash
# Clone the repository
git clone https://github.com/<username>/solana-twitter-leaderboard.git

# Open index.html
open index.html
```

Or run a local server:
```bash
npx http-server .
```
