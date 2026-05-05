# Automation

Last updated: 2026-05-05

## Schedule

Recommended first version:

- Daily exit check: after US market close, only meant to manage confirmed open positions.
- Weekly buy scan: Friday after US market close.

The Cloudflare Worker dispatches the GitHub Action with either `daily` or `weekly` mode. GitHub Actions can also be run manually.

## GitHub Action

Workflow:

- `.github/workflows/main.yml`

Manual run:

```bash
gh workflow run main.yml -f mode=weekly
gh workflow run main.yml -f mode=daily
```

The workflow:

- installs dependencies,
- runs `script.py`,
- sends Telegram if secrets exist,
- commits `position_state.json`,
- commits `reports/latest_report.md`,
- commits dated reports in `reports/`.

Required repository secrets:

- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`

## Cloudflare Worker

Worker files:

- `scheduler/cloudflare/worker.js`
- `scheduler/cloudflare/wrangler.toml`

Required Cloudflare secret:

- `GITHUB_TOKEN`

The token needs permission to dispatch workflows in `alonmorad9/real-stock-alert`.

## Safety Notes

- The bot never places trades.
- The bot never assumes a buy or sell happened.
- Manual trade confirmations should be committed after each real fill.
- Telegram messages are labeled `REAL STOCK SYSTEM`.

