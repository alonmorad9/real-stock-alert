# Real Stock Alert

Real-money stock alert system for a small, manually executed pilot.

This repo is intentionally separate from:

- `tqqq-alert`, the real TQQQ/manual safety strategy repo.
- `swing-stock-alert`, the demo/paper weekly stock swing repo.

The bot sends candidate and exit instructions, but it never assumes a trade happened until the real fill is confirmed with a manual command.

## Strategy

Active live profile: `turbo` max 2.

- Trade liquid large-cap and growth stocks.
- Hold at most 2 stocks.
- Allow new buys only when `QQQ` is above SMA200.
- If `QQQ` closes below SMA200, flag all open positions for sale.
- Run an opening turbo candidate scan 15 minutes after US market open on market weekdays.
- Run a daily close exit check for confirmed positions and include Turbo buy candidates.
- Run a weekly full buy scan after Friday close.
- Sell when price closes below SMA50, the trailing stop is hit, or a holding drops out of the weekly top list.

The initial state uses a small pilot allocation of `$1,000`. Edit `position_state.json` before going live if the real allocation is different.

## Manual Trade Flow

Weekly scan:

```bash
python3 script.py weekly
```

Opening scan:

```bash
python3 script.py opening
```

Daily exit check:

```bash
python3 script.py daily
```

Confirm a real buy after you manually buy:

```bash
python3 script.py manual_bought TICKER SHARES FILL_PRICE --date YYYY-MM-DD
```

Confirm a real sell after you manually sell:

```bash
python3 script.py manual_sold TICKER SHARES FILL_PRICE --date YYYY-MM-DD
```

Generated reports:

- `reports/latest_report.md`
- dated reports in `reports/`

## State

`position_state.json` is the source of truth for this repo.

It tracks:

- allocated cash
- tracked cash
- confirmed real positions
- actual shares
- actual fill prices
- stop levels
- realized P&L
- last scan and action

## Automation

See [docs/automation.md](docs/automation.md).

## Aggressive Research

Higher-risk swing variants are documented in [docs/aggressive-research.md](docs/aggressive-research.md).
Predictive risk-overlay tests are documented in [docs/risk-overlay-research.md](docs/risk-overlay-research.md).
Entry-decision tests are documented in [docs/entry-decision-research.md](docs/entry-decision-research.md).
Separate buy-the-dip entry tests can be run before deciding whether to add a dip scanner to live alerts.
Expanded-universe tests compare the current fixed universe against broader growth and ETF baskets.

Run locally:

```bash
python3 research/real_stock_strategy.py --research --start 2018-01-01
python3 research/real_stock_strategy.py --risk-research --start 2018-01-01
python3 research/real_stock_strategy.py --entry-research --start 2018-01-01
python3 research/real_stock_strategy.py --dip-research --start 2018-01-01
python3 research/real_stock_strategy.py --universe-research --start 2018-01-01
```

Or run the `Real Stock Research` workflow in GitHub Actions.

## Caveats

This is research and tooling, not financial advice. The human makes every final trade decision and executes trades manually.
