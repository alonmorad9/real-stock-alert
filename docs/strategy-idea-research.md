# Strategy Idea Research

Last updated: 2026-05-12

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
