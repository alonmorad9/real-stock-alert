# Automation

Last updated: 2026-05-05

## Schedule

Recommended first version:

- Opening turbo candidate scan: 15 minutes after US market open on market weekdays.
- Daily exit check: after US market close, only meant to manage confirmed open positions.
- Weekly buy scan: Friday after US market close.

The Cloudflare Worker dispatches the GitHub Action with either `daily` or `weekly` mode. GitHub Actions can also be run manually.

Cloudflare schedule:

```toml
"30,45 13,21 * * MON-FRI"
```

This is one Cloudflare cron trigger to stay under the free-plan trigger limit. It wakes at `13:30`, `13:45`, `21:30`, and `21:45` UTC, but the Worker only dispatches GitHub at:

- `13:45 UTC`: `opening`
- `21:30 UTC`: after-close run

During Israel daylight time, `13:45 UTC` is `16:45` Israel time.

The Worker maps the `21:30 UTC` after-close run to:

- Monday through Thursday: `daily`
- Friday: `weekly`

## GitHub Action

Workflow:

- `.github/workflows/main.yml`

Manual run:

```bash
gh workflow run main.yml -f mode=opening
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
