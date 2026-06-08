# Month-End Alignment

Last updated: 2026-06-08

Latest decision: `tqqq-alert` is the master controller and is currently back in an open TQQQ position. `real-stock-alert` remains the active stock-swing engine and bot-only stock benchmark, but it should deploy real stock cash only while `tqqq-alert` says TQQQ is out/waiting. Because TQQQ is currently open, the real-stock bucket should be inactive with no deployable cash, and stock candidates should be treated as watchlist-only.

## Current Repo Meanings

| Repo | Meaning | Money Mode | Source of Truth |
| --- | --- | --- | --- |
| `tqqq-alert` | Real TQQQ strategy, currently open TQQQ position | Real | `position_state.json` |
| `real-stock-alert` | Real stock-buying turbo swing pilot plus bot-only stock benchmark | Real + benchmark | `position_state.json` |
| `swing-stock-alert` | Paused old demo stock swing archive | Historical paper/demo only | `pilot_state.json` and `reports/` |

## Current Known Status

### `tqqq-alert`

- Real TQQQ repo.
- Current state inspected locally on 2026-06-08:
  - `position_open`: `true`
  - `shares`: `35.3032`
  - `avg_cost`: `$83.84`
  - `entry_date`: `2026-06-04`
  - `highest_high_since_entry`: `$86.25`
  - `cash`: `$4.80`
  - `last_action`: `manual_broker_buy_sync`
  - `last_report_key`: `2026-06-08:open`
  - `manual_exit_mode`: `false`
  - `manual_exit_price`: `null`
  - `manual_exit_date`: `null`
  - `manual_exit_saw_below_sma`: `false`
  - `early_exit_price`: `null`
  - `early_exit_date`: `null`
  - `waiting_for_early_reentry`: `false`
- Meaning: the bot assumes a real TQQQ position is open. TQQQ is using the active position sell/risk rules, not manual-safety re-entry mode.
- Meaning of cash state: the TQQQ bucket is currently deployed into TQQQ, with only residual cash tracked. No XLK parking asset is part of the selected TQQQ strategy.
- If TQQQ exits later, manual safety re-buy rules use the Best Calmar re-entry setup: 7.5% pullback from the actual sell price, 10-trading-day profit timeout, and no RSI re-entry gate.
- Current selected TQQQ strategy uses a 25% TQQQ ratcheting trailing stop, a 10% fresh-entry guard for the first 2 trading days after a buy, +20% profit target, -7.5% re-buy pullback, 10-trading-day profit re-buy timeout, parabolic profit exit on 5-day >= 25% or 10-day >= 30%, advisory early-warning signals, and cash as the waiting state.
- Current TQQQ execution guardrails also delay bot-generated buys during the first 30 market minutes and use a same-day cooldown after fresh-entry guard exits.
- Current early-warning inputs are advisory only, with no automatic sell: VIX >= 25, VIX 5-day spike >= 25%, QQQ below EMA21, TQQQ below SMA20, and TQQQ RSI falling from 70+.
- Bot-only benchmark state is separate and still tracks what would have happened if the original TQQQ bot path had stayed in the position.

### `swing-stock-alert`

- Paused research archive.
- Current state inspected locally on 2026-05-27:
  - paper positions: `INTC`, `MRVL`
  - paper start date: `2026-05-04`
  - latest paper value: `1.184576`
  - latest paper return: `18.4576%`
  - repo status: `paused_research_archive`
  - active decision source: `false`
- Meaning: this is optional historical context only. It should not send active alerts and should not be treated as real holdings.

### `real-stock-alert`

- Real stock pilot repo.
- Current state inspected locally on 2026-06-08:
  - strategy: `turbo_top_2_real_stock_momentum`
  - active profile: `turbo`
  - max positions: `2`
  - allocated cash: `$0.00`
  - cash: `$0.00`
  - positions: `[]`
  - latest candidates: `DDOG`, `PANW`
  - latest skipped candidates: `ARM` from ATR cap, `MRVL` from repeat-stretched rule
  - latest market risk: `DEFENSIVE`, score `5`
  - latest market risk reasons: `QQQ below SMA20`, `QQQ below SMA10`, `QQQ 5d drop`, `20d drawdown`
  - risk overlay: `risk_balanced`, half-size new buys only when market risk is elevated/defensive
  - rank policy: `skip_repeat_stretched`
  - bot-only stock benchmark: included in Telegram/report state as the comparison path for this repo
  - bot-only benchmark holdings: `MU`, `DDOG`
  - bot-only benchmark value: `$2,668.13`
  - bot-only benchmark action: sold `INTC`, bought `DDOG`
- latest research decision:
  - Turbo remains the live stock strategy.
  - Repeat-stretched candidates are skipped after the 2026-05-09 test improved both return and max drawdown versus baseline.
  - Expanded-universe tests did not beat the current universe, so the live universe should stay narrow.
  - Buy-the-dip was tested as a separate entry system and did not beat Turbo.
  - Best dip variant: `14.46x`, `37.8%` CAGR, `-34.9%` max drawdown.
  - Turbo baseline in the same dip test: `43.59x`, `57.2%` CAGR, `-35.8%` max drawdown.
  - The 2026-05-12 strategy-idea test selected `score_no_extension`: `45.21x`, `57.8%` CAGR, `-31.2%` max drawdown versus `baseline_live` `32.84x`, `51.9%` CAGR, `-32.7%` max drawdown.
  - The latest 2026-05-27 strategy-idea test keeps `atr_cap_10pct` / `hold_unless_broken` as best: `50.67x`, `59.6%` CAGR, `-31.2%` max drawdown.
  - Live Turbo scoring now uses 63-day relative strength plus 20-day momentum only; extra distance above SMA50 is not rewarded. Fresh buy candidates with ATR14 above 10% of price are skipped.
  - Opening, daily, and weekly messages now use consistent repeat-stretch memory: prior recommended candidates plus prior skipped repeat-stretched candidates.
  - Rank-based sell rotation is disabled after the 2026-05-27 rotation-buffer research. Rankings choose fresh buys for empty slots, but holdings are kept until SMA50, stop, QQQ SMA200, or TQQQ-priority rules break.
  - Scheduled opening/daily/weekly reports now skip US market holidays, matching the TQQQ repo behavior.
- Meaning: no real stock position exists, and no real-stock cash should be deployed while TQQQ is open.

## Month-End Review Plan

At month end, compare the two active systems first, and use the old swing demo only as optional historical context:

1. `tqqq-alert`
   - Inspect `position_state.json`.
   - Confirm real TQQQ cash/shares match the brokerage account.
   - Check current TQQQ shares, average cost, stop/risk state, cash, and action history.
   - Treat the selected TQQQ waiting state as cash only if `position_state.json` later says TQQQ is out.
   - Compare real path against `bot_strategy_state.json`, which is only a paper benchmark.
   - Review action history and Telegram/GitHub Actions behavior.

2. `real-stock-alert`
   - Inspect `position_state.json`.
   - Confirm real stock cash/shares match the brokerage account.
   - Confirm any real buys/sells were manually confirmed with actual fills.
   - Review turbo profile performance and the bot-only benchmark separately from confirmed real fills.
   - Keep buy-the-dip as research/watchlist only unless a future test beats Turbo.

3. `swing-stock-alert`
   - Optional only.
   - Inspect `pilot_state.json` and `reports/latest_report.md` only if we want the old May paper-pilot history.
   - Treat all positions as paper/demo assumptions.
   - Do not compare this as real-money performance and do not use it as an active decision source.

## Known Alignment Notes

- `tqqq-alert` is currently in an open TQQQ trade as of the inspected state.
- `tqqq-alert` is not currently in manual safety cash/re-entry mode.
- Some older `tqqq-alert` history may describe previous XLK/early-warning states. Read current `script.py`, current docs, and `position_state.json` as the source of truth.
- `swing-stock-alert` is paused as of 2026-05-23. Its Cloudflare cron is disabled and the Worker has a pause guard.
- Strategy choices are currently aligned as:
  - TQQQ repo: current selected strategy is Best Calmar high-return: 25% TQQQ ratchet, 10% fresh-entry guard for the first 2 trading days, same-day cooldown after fresh-entry guard exits, no bot-generated buys during the first 30 market minutes, no RSI re-entry gate, -7.5% re-buy pullback, 10-trading-day profit re-buy timeout, +20% profit target, 5-day >= 25% or 10-day >= 30% profitable parabolic auto-exit, advisory early-warning signals, and cash/no-XLK as the waiting state.
  - TQQQ warning layer: early-warning signals are advisory only and no longer auto-sell. Current warning inputs are VIX >= 25, VIX 5-day spike >= 25%, QQQ below EMA21, TQQQ below SMA20, RSI falling from 70+.
  - Real-stock repo: keep Turbo top-2 momentum as the active stock engine during TQQQ-out periods, using `skip_repeat_stretched`, consistent repeat-stretch memory across report modes, `score_no_extension`, the tested `atr_cap_10pct` fresh-buy volatility filter, `hold_unless_broken` position management, watchlist-only real buy wording while TQQQ is open, and the stock bot-only benchmark in reports.
  - Swing repo: keep paused as old paper/demo archive only.
- Real-stock has been handed back to TQQQ-open mode with `$0.00` deployable real-stock cash. Before using real-stock as the TQQQ-out engine again, reset its cash bucket with `set_cash <actual freed cash amount>` after a future TQQQ exit.
- `swing-stock-alert` and `real-stock-alert` can show overlapping tickers, such as `INTC`, but they mean different things:
  - swing repo: paper/demo assumed positions,
  - real-stock repo: real candidates only until manually confirmed.
- The TQQQ market reference inside the swing repo is not the real TQQQ strategy result.
