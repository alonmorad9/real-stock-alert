# Entry Decision Research

Last updated: 2026-05-06

## Goal

Compare practical choices when Turbo candidates are available:

- buy both candidates,
- buy only the top candidate,
- half-size candidates that are hot/stretched,
- skip hot/stretched candidates.

All variants keep the selected `risk_balanced` market overlay with half-size buys during elevated market risk.

## Run

```bash
python3 research/real_stock_strategy.py --entry-research --start 2018-01-01
```

Or run the `Real Stock Research` GitHub Action with:

- `kind`: `entry`
- `start`: `2018-01-01`

Outputs:

- `research/out/entry_decision_summary.csv`
- `research/out/entry_*_equity_curve.csv`
- `research/out/entry_*_trades.csv`

