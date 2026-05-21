# Strategy Idea Research

Last updated: 2026-05-21

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
