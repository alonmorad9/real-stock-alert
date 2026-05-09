# Repeat Stretch Research

Last updated: 2026-05-09

## Purpose

Test the idea before live implementation:

> If the same top candidates keep appearing while they are very stretched, should the bot wait for cool-off or confirmation instead of repeating the buy recommendation?

This is research only. It does not change live alerts.

## Tested Variants

- `baseline_full_two`: current Turbo top-2 behavior.
- `skip_repeat_stretched`: if a ticker was already a prior target and is still stretched, skip it for new ranking.
- `skip_repeat_extreme`: same idea, but only when the repeat ticker is extremely stretched.
- `skip_all_extreme`: skip any extremely stretched new candidate.
- `half_stretched_baseline`: keep the current ranking but half-size stretched entries.
- `skip_stretched_baseline`: skip stretched entries entirely.

## Run

```bash
python3 research/real_stock_strategy.py --repeat-stretch-research --start 2018-01-01
```

Or run the `Real Stock Research` GitHub Action with:

- `kind`: `repeat`
- `start`: `2018-01-01`

## Output

- `research/out/repeat_stretch_summary.csv`
- `research/out/repeat_*_equity_curve.csv`
- `research/out/repeat_*_trades.csv`

## Decision Rule

Only add a live repeat-stretch rule if it improves the return/drawdown tradeoff. If it reduces return heavily, keep overextension as a warning only.
