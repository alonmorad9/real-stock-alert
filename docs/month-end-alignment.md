# Month-End Alignment

Last updated: 2026-05-21

Latest decision: `tqqq-alert` is the master controller and currently has an open TQQQ position. `real-stock-alert` is the optional temporary real-stock swing engine only while `tqqq-alert` says TQQQ is out/waiting. Because TQQQ is currently open, the real-stock bucket should be inactive with no deployable cash. If `tqqq-alert` later exits TQQQ and waits in cash, reset this repo with `set_cash <actual freed cash amount>` before following stock candidates.

## Current Repo Meanings

| Repo | Meaning | Money Mode | Source of Truth |
| --- | --- | --- | --- |
| `tqqq-alert` | Real TQQQ strategy, currently open TQQQ position | Real | `position_state.json` |
| `swing-stock-alert` | Weekly stock swing demo/paper tracker | Paper/demo | `pilot_state.json` and `reports/` |
| `real-stock-alert` | Real stock-buying turbo swing pilot | Real | `position_state.json` |

## Current Known Status

### `tqqq-alert`

- Real TQQQ repo.
- Current state inspected locally on 2026-05-21:
  - `position_open`: `true`
  - `shares`: `35.6658`
  - `avg_cost`: `$75.20`
  - `entry_date`: `2026-05-21`
  - `cash`: `$0.00`
  - `last_action`: `manual_broker_buy_sync`
  - `manual_exit_mode`: `false`
  - `manual_exit_price`: `null`
  - `manual_exit_date`: `null`
  - `manual_exit_saw_below_sma`: `false`
  - `early_exit_price`: `null`
  - `early_exit_date`: `null`
  - `waiting_for_early_reentry`: `false`
- Meaning: the bot assumes a real TQQQ position is open. TQQQ is using the active position sell/risk rules, not manual-safety re-entry mode.
- Meaning of cash state: the TQQQ bucket is currently deployed into TQQQ. No XLK parking asset is part of the selected TQQQ strategy.
- If TQQQ exits later, manual safety re-buy rules require the correct pullback/reset/timeout trigger plus `RSI14 <= 70`.
- Current selected TQQQ strategy uses a 25% TQQQ ratcheting trailing stop, +20% profit target, -5% re-buy pullback, 15-trading-day profit re-buy timeout, 5-day >= 25% profitable parabolic auto-exit, advisory early-warning signals, and cash as the waiting state.
- Current early-warning inputs are advisory only, with no automatic sell: VIX >= 25, VIX 5-day spike >= 25%, QQQ below EMA21, TQQQ below SMA20, and TQQQ RSI falling from 70+.
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
- Current state inspected locally on 2026-05-21:
  - strategy: `turbo_top_2_real_stock_momentum`
  - active profile: `turbo`
  - max positions: `2`
  - allocated cash: `$0.00`
  - cash: `$0.00`
  - positions: `[]`
  - latest candidates: `ARM`, `MRVL`
  - latest skipped repeat-stretched candidates: `INTC`, `DDOG`
  - latest market risk: `NORMAL`, score `0`
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
  - The 2026-05-21 volatility test improved this with `atr_cap_10pct`: `47.12x`, `58.4%` CAGR, `-31.2%` max drawdown.
  - Live Turbo scoring now uses 63-day relative strength plus 20-day momentum only; extra distance above SMA50 is not rewarded. Fresh buy candidates with ATR14 above 10% of price are skipped.
  - Opening, daily, and weekly messages now use consistent repeat-stretch memory: prior recommended candidates plus prior skipped repeat-stretched candidates.
- Meaning: no real stock position exists, and no real-stock cash should be deployed while TQQQ is open.

## Month-End Review Plan

At month end, compare the three systems separately:

1. `tqqq-alert`
   - Inspect `position_state.json`.
   - Confirm real TQQQ cash/shares match the brokerage account.
   - Check current TQQQ shares, average cost, stop/risk state, cash, and action history.
   - Treat the selected TQQQ waiting state as cash only if `position_state.json` later says TQQQ is out.
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

- `tqqq-alert` is currently in an open TQQQ trade as of the inspected state.
- `tqqq-alert` is not currently in manual safety cash/re-entry mode.
- Some older `tqqq-alert` history may describe previous XLK/early-warning states. Read current `script.py`, current docs, and `position_state.json` as the source of truth.
- Some older `swing-stock-alert` text still refers to the "current open TQQQ trade." Read that as historical/stale wording; the live TQQQ state is the source of truth.
- Strategy choices are currently aligned as:
  - TQQQ repo: current selected strategy is 25% TQQQ ratchet, RSI14 <= 70 re-entry cap, -5% re-buy pullback, 15-trading-day profit re-buy timeout, +20% profit target, 5-day >= 25% profitable parabolic auto-exit, advisory early-warning signals, and cash/no-XLK as the waiting state.
  - TQQQ warning layer: early-warning signals are advisory only and no longer auto-sell. Current warning inputs are VIX >= 25, VIX 5-day spike >= 25%, QQQ below EMA21, TQQQ below SMA20, RSI falling from 70+.
  - Swing repo: keep as paper/demo weekly stock comparison only.
  - Real-stock repo: keep Turbo top-2 momentum as the live stock engine during TQQQ-out periods, using `skip_repeat_stretched`, consistent repeat-stretch memory across report modes, `score_no_extension`, and the tested `atr_cap_10pct` fresh-buy volatility filter.
- Before using real-stock as the TQQQ-out engine again, reset its cash bucket with `set_cash <actual freed cash amount>` after a future TQQQ exit. As of the current TQQQ source state, deployable real-stock cash should be `$0.00` because the bucket is in TQQQ.
- `swing-stock-alert` and `real-stock-alert` can show overlapping tickers, such as `INTC`, but they mean different things:
  - swing repo: paper/demo assumed positions,
  - real-stock repo: real candidates only until manually confirmed.
- The TQQQ market reference inside the swing repo is not the real TQQQ strategy result.
