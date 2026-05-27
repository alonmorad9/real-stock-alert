# Strategy Idea Research

Last updated: 2026-05-27

## Purpose

Test ideas that might beat the current live strategy before changing live behavior.

Current live baseline:

- `turbo`
- current narrow universe
- max 2 positions
- `risk_balanced` with half-size new buys during elevated risk
- `skip_repeat_stretched`

## Tested Ideas

- Score weights:
  - heavier 20-day momentum
  - heavier 63-day relative strength
  - no distance-above-SMA50 score
  - volatility-adjusted score variants that penalize high ATR as a percent of price
- Exit rules:
  - EMA21 exit
  - SMA20 exit
  - current SMA50 exit baseline
- Stops:
  - tighter trailing stop
  - looser trailing stop
- Profit protection:
  - after +25%, use 10% trailing lock
  - after +40%, use 15% trailing lock
  - fixed +50% profit target
- Entry filter:
  - skip next-open buys if opening gap is above 8%
  - skip next-open buys if opening gap is above 12%
  - skip next-open buys if ATR14 is above 8% or 10% of price
- Concentration:
  - avoid opening two positions from the same broad sector group.

## Run

```bash
python3 research/real_stock_strategy.py --idea-research --start 2018-01-01
```

Or run the `Real Stock Research` GitHub Action with:

- `kind`: `ideas`
- `start`: `2018-01-01`

## Output

- `research/out/strategy_idea_summary.csv`
- `research/out/idea_*_equity_curve.csv`
- `research/out/idea_*_trades.csv`

## Decision Rule

Only change live behavior if an idea beats the live baseline on return while keeping drawdown reasonable and the trades realistic enough to follow manually.

## 2026-05-12 Result

The best tested idea was `score_no_extension`.

| Idea | Final multiple | CAGR | Max drawdown | Decision |
| --- | ---: | ---: | ---: | --- |
| `score_no_extension` | 45.21x | 57.8% | -31.2% | Implement live |
| `score_20d_heavy` | 39.24x | 55.1% | -37.6% | Reject |
| `score_rs63_heavy` | 37.00x | 54.1% | -31.4% | Reject |
| `baseline_live` | 32.84x | 51.9% | -32.7% | Replaced |

Decision: keep Turbo, `risk_balanced`, half-size elevated-risk buys, and `skip_repeat_stretched`, but change the live Turbo score to use 63-day relative strength plus 20-day momentum only. Do not reward extra distance above SMA50 in the score; keep SMA50 extension for warnings and stretched-repeat discipline.

## 2026-05-21 Added Test

Added research-only volatility variants:

| Idea | Meaning |
| --- | --- |
| `score_vol_penalty_50` | Keep current score, subtract a light ATR14/price penalty. |
| `score_vol_penalty_100` | Keep current score, subtract a medium ATR14/price penalty. |
| `score_vol_penalty_150` | Keep current score, subtract a stronger ATR14/price penalty. |
| `atr_cap_8pct` | Keep current score, but skip fresh buys where ATR14 is above 8% of price. |
| `atr_cap_10pct` | Keep current score, but skip fresh buys where ATR14 is above 10% of price. |

Decision rule: these should replace live scoring only if they beat `score_no_extension` on return or materially improve drawdown without giving up too much return.

## 2026-05-21 Result

The best volatility idea was `atr_cap_10pct`.

| Idea | Final multiple | CAGR | Max drawdown | Decision |
| --- | ---: | ---: | ---: | --- |
| `atr_cap_10pct` | 47.12x | 58.4% | -31.2% | Implement live |
| `atr_cap_8pct` | 47.02x | 58.3% | -31.2% | Reject, slightly lower return |
| `score_no_extension` | 45.10x | 57.6% | -31.2% | Replaced |
| `score_vol_penalty_100` | 44.02x | 57.1% | -32.4% | Reject |
| `score_vol_penalty_50` | 41.90x | 56.2% | -32.4% | Reject |
| `score_vol_penalty_150` | 37.08x | 53.9% | -32.4% | Reject |

Decision: keep the current `score_no_extension` formula, but add a fresh-buy ATR cap. Live buy scans should skip candidates where ATR14 is above 10% of price.

## 2026-05-21 Stop Management Result

Tested proposed open-trade management changes against the current best `atr_cap_10pct` setup:

- tighter initial stop: higher of 8% below entry or 2.0x ATR14 below entry,
- tighter trailing stop: higher of 12% below highest high or 3.0x ATR14 below highest high,
- breakeven floor after the trade moves 1.5x entry ATR14 in profit,
- adaptive trailing ladder that tightens after +10% and +20% profit,
- combinations of those rules.

| Idea | Final multiple | CAGR | Max drawdown | Decision |
| --- | ---: | ---: | ---: | --- |
| `atr_cap_10pct` | 47.12x | 58.4% | -31.2% | Keep live |
| `atr_cap_10pct_tight_recommended_stops` | 20.54x | 43.4% | -22.9% | Reject for high-risk/high-reward mode |
| `atr_cap_10pct_breakeven_1_5atr` | 34.89x | 52.8% | -31.6% | Reject |
| `atr_cap_10pct_adaptive_trail` | 5.66x | 23.0% | -30.3% | Reject |
| `atr_cap_10pct_breakeven_adaptive` | 4.41x | 19.4% | -37.6% | Reject |
| `atr_cap_10pct_all_tight_changes` | 4.34x | 19.2% | -22.8% | Reject |

Decision: do not change live stop rules. Tighter stops reduce drawdown in some variants, but they cut the historical compounding too much. For the stated high-risk/high-reward goal, the current `atr_cap_10pct` setup remains the best tested live stock strategy.

## 2026-05-27 Rank Rotation Result

Tested whether rank-based sell rotation improves the current best `atr_cap_10pct` setup.

| Idea | Final multiple | CAGR | Max drawdown | Trades | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| `atr_cap_10pct` / `hold_unless_broken` | 50.67x | 59.6% | -31.2% | 277 | Keep live |
| `strict_weekly_top2_rotation` | 38.10x | 54.3% | -42.2% | 660 | Reject |
| `two_week_rank_confirm` | 35.99x | 53.2% | -41.3% | 505 | Reject |
| `weekly_top5_buffer` | 31.90x | 51.0% | -28.0% | 478 | Reject for high-risk/high-reward mode |
| `weekly_top4_buffer` | 31.88x | 51.0% | -26.7% | 506 | Reject for high-risk/high-reward mode |

Decision: do not force-sell a holding just because a different stock ranks higher. Rankings should choose fresh buys for empty slots. Existing holdings should be kept until a real risk/trend rule breaks: QQQ below SMA200, stock below SMA50, trailing stop, or TQQQ-priority exit.
