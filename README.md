# Real Stock Alert

Real-money stock alert system for a small, manually executed pilot.

This repo is intentionally separate from:

- `tqqq-alert`, the real TQQQ/manual safety strategy repo.
- `swing-stock-alert`, the demo/paper weekly stock swing repo.

The bot sends candidate and exit instructions, but it never assumes a trade happened until the real fill is confirmed with a manual command.

## Strategy

Active live profile: `turbo` max 2.

Current capital mode: **TQQQ-out swing mode**.

This means the TQQQ repo is the master controller:

- When `tqqq-alert` says TQQQ is out/waiting, this repo can manage the freed cash in top-2 real swing stocks.
- When `tqqq-alert` sends a TQQQ buy/re-buy signal, TQQQ takes priority. Sell all real-stock positions, confirm the sales here with `manual_sold`, then use the cash to buy TQQQ and confirm that buy in `tqqq-alert`.
- The stock bot's normal sell rules still apply while TQQQ is waiting. If a stock sell fires and TQQQ still says wait, sell that stock and follow the next real-stock candidate/cash instruction.

- Trade liquid large-cap and growth stocks.
- Hold at most 2 stocks.
- Allow new buys only when `QQQ` is above SMA200.
- Rank Turbo candidates by 63-day relative strength plus 20-day momentum; extra distance above SMA50 is not rewarded.
- Skip repeat stretched names as fresh buy candidates, using the tested `skip_repeat_stretched` rank policy.
- If `QQQ` closes below SMA200, flag all open positions for sale.
- Run an opening turbo candidate scan 15 minutes after US market open on market weekdays.
- Run a daily close exit check for confirmed positions and include Turbo buy candidates.
- Run a weekly full buy scan after Friday close.
- Sell when price closes below SMA50, the trailing stop is hit, or a holding drops out of the weekly top list.

The old initial state used a small pilot allocation of `$1,000`. In TQQQ-out swing mode, reset the cash bucket to the actual freed TQQQ cash after TQQQ exits. The TQQQ repo itself now waits in cash while out of TQQQ; this repo is the optional real-stock swing bucket during that waiting period.

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

Set the real-stock cash bucket after TQQQ exits:

```bash
python3 script.py set_cash AMOUNT
```

Example:

```bash
python3 script.py set_cash 2726.11
```

Confirm a real buy after you manually buy:

```bash
python3 script.py manual_bought TICKER SHARES FILL_PRICE --date YYYY-MM-DD
```

Confirm a real sell after you manually sell:

```bash
python3 script.py manual_sold TICKER SHARES FILL_PRICE --date YYYY-MM-DD
```

If `tqqq-alert` sends a TQQQ re-buy signal, sell every open real-stock position and confirm each sale with `manual_sold` before buying TQQQ.

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
Repeat-stretch tests are documented in [docs/repeat-stretch-research.md](docs/repeat-stretch-research.md).
Separate buy-the-dip entry tests can be run before deciding whether to add a dip scanner to live alerts.
Expanded-universe tests compare the current fixed universe against broader growth and ETF baskets.
Strategy-idea tests are documented in [docs/strategy-idea-research.md](docs/strategy-idea-research.md).

Run locally:

```bash
python3 research/real_stock_strategy.py --research --start 2018-01-01
python3 research/real_stock_strategy.py --risk-research --start 2018-01-01
python3 research/real_stock_strategy.py --entry-research --start 2018-01-01
python3 research/real_stock_strategy.py --repeat-stretch-research --start 2018-01-01
python3 research/real_stock_strategy.py --dip-research --start 2018-01-01
python3 research/real_stock_strategy.py --universe-research --start 2018-01-01
python3 research/real_stock_strategy.py --idea-research --start 2018-01-01
```

Or run the `Real Stock Research` workflow in GitHub Actions.

## Caveats

This is research and tooling, not financial advice. The human makes every final trade decision and executes trades manually.
