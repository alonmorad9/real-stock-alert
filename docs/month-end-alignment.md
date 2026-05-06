# Month-End Alignment

Last updated: 2026-05-06

## Current Repo Meanings

| Repo | Meaning | Money Mode | Source of Truth |
| --- | --- | --- | --- |
| `tqqq-alert` | Real TQQQ early-warning cash/re-entry strategy | Real | `position_state.json` |
| `swing-stock-alert` | Weekly stock swing demo/paper tracker | Paper/demo | `pilot_state.json` and `reports/` |
| `real-stock-alert` | Real stock-buying turbo swing pilot | Real | `position_state.json` |

## Current Known Status

### `tqqq-alert`

- Real TQQQ repo.
- Current state inspected locally on 2026-05-06:
  - `position_open`: `false`
  - `shares`: `0.0`
  - `cash`: `$2,726.11`
  - `last_action`: `strategy_switched_to_early_warning_cash`
  - `manual_exit_mode`: `false`
  - `early_exit_price`: `$67.37`
  - `early_exit_date`: `2026-05-05`
  - `waiting_for_early_reentry`: `true`
- Meaning: the bot assumes no open TQQQ position and waits under early-warning re-entry rules.

### `swing-stock-alert`

- Demo/paper repo.
- Current state inspected locally on 2026-05-06:
  - paper positions: `INTC`, `MRVL`
  - paper start date: `2026-05-04`
  - latest paper value: `1.046144`
  - latest paper return: `4.6144%`
- Meaning: this is a paper/demo comparison only. It should not be treated as real holdings.

### `real-stock-alert`

- Real stock pilot repo.
- Current state inspected locally on 2026-05-06:
  - strategy: `turbo_top_2_real_stock_momentum`
  - active profile: `turbo`
  - max positions: `2`
  - allocated cash: `$1,000`
  - cash: `$1,000`
  - positions: `[]`
  - latest candidates: `INTC`, `AMD`
  - latest market risk: `NORMAL`, score `1`
  - risk overlay: `risk_balanced`, half-size new buys only when market risk is elevated/defensive
- latest research decision:
  - Turbo remains the live stock strategy.
  - Buy-the-dip was tested as a separate entry system and did not beat Turbo.
  - Best dip variant: `14.46x`, `37.8%` CAGR, `-34.9%` max drawdown.
  - Turbo baseline in the same dip test: `43.59x`, `57.2%` CAGR, `-35.8%` max drawdown.
- Meaning: no real stock position exists until `manual_bought` is run with actual broker fill details.

## Month-End Review Plan

At month end, compare the three systems separately:

1. `tqqq-alert`
   - Inspect `position_state.json`.
   - Confirm real TQQQ cash/shares match the brokerage account.
   - Check whether early-warning cash mode caused a re-buy, continued cash, or a new state.
   - Review action history and Telegram/GitHub Actions behavior.

2. `swing-stock-alert`
   - Inspect `pilot_state.json`.
   - Inspect `reports/latest_report.md` and dated reports.
   - Treat all positions as paper/demo assumptions.
   - Do not compare this as real-money performance.

3. `real-stock-alert`
   - Inspect `position_state.json`.
   - Confirm real stock cash/shares match the brokerage account.
   - Confirm any real buys/sells were manually confirmed with actual fills.
   - Review turbo profile performance separately from the swing demo.
   - Keep buy-the-dip as research/watchlist only unless a future test beats Turbo.

## Known Alignment Notes

- `tqqq-alert` is no longer in an open TQQQ trade as of the inspected state.
- `tqqq-alert` is currently early-warning cash/re-entry, not manual safety mode.
- Some older `swing-stock-alert` text still refers to the "current open TQQQ trade." Read that as historical/stale wording; the live TQQQ state is the source of truth.
- Strategy choices are currently aligned as:
  - TQQQ repo: keep the optimized early-warning cash/re-entry TQQQ strategy.
  - Swing repo: keep as paper/demo weekly stock comparison only.
  - Real-stock repo: keep Turbo top-2 momentum as the live stock pilot.
- `swing-stock-alert` and `real-stock-alert` can show overlapping tickers, such as `INTC`, but they mean different things:
  - swing repo: paper/demo assumed positions,
  - real-stock repo: real candidates only until manually confirmed.
- The TQQQ market reference inside the swing repo is not the real TQQQ strategy result.
