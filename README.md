# Real Stock Alert

Real-money stock alert system for a small, manually executed pilot.

This repo is intentionally separate from:

- `tqqq-alert`, the real TQQQ/manual safety strategy repo.
- `swing-stock-alert`, the demo/paper weekly stock swing repo.

The bot sends candidate and exit instructions, but it never assumes a trade happened until the real fill is confirmed with a manual command.

## Strategy

Default first version:

- Trade liquid large-cap and growth stocks.
- Hold at most 2 stocks.
- Allow new buys only when `QQQ` is above SMA200.
- If `QQQ` closes below SMA200, flag all open positions for sale.
- Run a daily close exit check for confirmed positions.
- Run a weekly full buy scan after Friday close.
- Sell when trend breaks, stop is hit, or a holding drops out of the weekly top list.

The initial state uses a small pilot allocation of `$1,000`. Edit `position_state.json` before going live if the real allocation is different.

## Manual Trade Flow

Weekly scan:

```bash
python3 script.py weekly
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

## Caveats

This is research and tooling, not financial advice. The human makes every final trade decision and executes trades manually.

