# Month-End Alignment

Last updated: 2026-05-14

## Current Repo Meanings

| Repo | Meaning | Money Mode | Source of Truth |
| --- | --- | --- | --- |
| `tqqq-alert` | Real TQQQ strategy, currently manual safety cash/re-entry mode | Real | `position_state.json` |
| `swing-stock-alert` | Weekly stock swing demo/paper tracker | Paper/demo | `pilot_state.json` and `reports/` |
| `real-stock-alert` | Real stock-buying turbo swing pilot | Real | `position_state.json` |

## Current Known Status

### `tqqq-alert`

- Real TQQQ repo.
- Current state inspected locally on 2026-05-14:
  - `position_open`: `false`
  - `shares`: `0.0`
  - `cash`: `$2,726.11`
  - `last_action`: `manual_sold`
  - `manual_exit_mode`: `true`
  - `manual_exit_price`: `$67.37`
  - `manual_exit_date`: `2026-05-05`
  - `manual_exit_saw_below_sma`: `false`
  - `early_exit_price`: `null`
  - `early_exit_date`: `null`
  - `waiting_for_early_reentry`: `false`
  - `parking_ticker`: `XLK`
  - `parking_shares`: `0.0`
- Meaning: the bot assumes no open TQQQ position and is in manual safety mode. It should not immediately re-buy just because TQQQ is above SMA200.
- Meaning of parking fields: XLK is tracked only as an optional waiting/parking asset. Because `parking_shares` is `0.0`, there is no real XLK parking position in the inspected state.
- Manual safety re-buy rule: re-buy after a 7.5% pullback from `$67.37` while still above SMA200, or after price first goes below SMA200 and later crosses back above SMA200.
- Manual safety timeout rule: after 20 trading days in manual safety cash mode, allow re-entry above SMA200 if `RSI14 <= 60`.
- Fresh buys and re-buys also require `RSI14 <= 60`, based on the 2026-05-12 RSI guard research.
- Parabolic-stretch checks were added as Telegram advisory warnings only. They are not automatic sell rules for the month-end test.
- Bot-only benchmark state is separate and still tracks what would have happened if the original TQQQ bot path had stayed in the position.

### `swing-stock-alert`

- Demo/paper repo.
- Current state inspected locally on 2026-05-07:
  - paper positions: `INTC`, `MRVL`
  - paper start date: `2026-05-04`
  - latest paper value: `1.046144`
  - latest paper return: `4.6144%`
- Meaning: this is a paper/demo comparison only. It should not be treated as real holdings.

### `real-stock-alert`

- Real stock pilot repo.
- Current state inspected locally on 2026-05-14:
  - strategy: `turbo_top_2_real_stock_momentum`
  - active profile: `turbo`
  - max positions: `2`
  - allocated cash: `$1,000`
  - cash: `$1,000`
  - positions: `[]`
  - latest candidates: `INTC`, `AMD`
  - latest skipped repeat-stretched candidates: `[]`
  - latest market risk: `NORMAL`, score `1`
  - risk overlay: `risk_balanced`, half-size new buys only when market risk is elevated/defensive
  - rank policy: `skip_repeat_stretched`
- latest research decision:
  - Turbo remains the live stock strategy.
  - Repeat-stretched candidates are skipped after the 2026-05-09 test improved both return and max drawdown versus baseline.
  - Expanded-universe tests did not beat the current universe, so the live universe should stay narrow.
  - Buy-the-dip was tested as a separate entry system and did not beat Turbo.
  - Best dip variant: `14.46x`, `37.8%` CAGR, `-34.9%` max drawdown.
  - Turbo baseline in the same dip test: `43.59x`, `57.2%` CAGR, `-35.8%` max drawdown.
  - The 2026-05-12 strategy-idea test selected `score_no_extension`: `45.21x`, `57.8%` CAGR, `-31.2%` max drawdown versus `baseline_live` `32.84x`, `51.9%` CAGR, `-32.7%` max drawdown.
  - Live Turbo scoring now uses 63-day relative strength plus 20-day momentum only; extra distance above SMA50 is not rewarded.
  - Opening, daily, and weekly messages now use consistent repeat-stretch memory: prior recommended candidates plus prior skipped repeat-stretched candidates.
- Meaning: no real stock position exists until `manual_bought` is run with actual broker fill details.

## Month-End Review Plan

At month end, compare the three systems separately:

1. `tqqq-alert`
   - Inspect `position_state.json`.
   - Confirm real TQQQ cash/shares match the brokerage account.
   - Check whether manual safety mode caused a re-buy, continued cash, or a new state.
   - Compare real path against `bot_strategy_state.json`, which is only a paper benchmark.
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
- `tqqq-alert` is currently manual safety cash/re-entry mode, not early-warning cash/re-entry mode.
- Some older `tqqq-alert` docs still describe the previous early-warning cash state. Read `position_state.json` as the source of truth.
- Some older `swing-stock-alert` text still refers to the "current open TQQQ trade." Read that as historical/stale wording; the live TQQQ state is the source of truth.
- Strategy choices are currently aligned as:
  - TQQQ repo: keep the optimized TQQQ strategy with the RSI14 re-entry guard and manual safety timeout; parabolic-stretch warnings are advisory only. XLK parking tracking exists but currently has zero shares. Current real state is manual safety cash/re-entry after `manual_sold`.
  - Swing repo: keep as paper/demo weekly stock comparison only.
  - Real-stock repo: keep Turbo top-2 momentum as the live stock pilot, using `skip_repeat_stretched`, consistent repeat-stretch memory across report modes, and `score_no_extension`.
- `swing-stock-alert` and `real-stock-alert` can show overlapping tickers, such as `INTC`, but they mean different things:
  - swing repo: paper/demo assumed positions,
  - real-stock repo: real candidates only until manually confirmed.
- The TQQQ market reference inside the swing repo is not the real TQQQ strategy result.
