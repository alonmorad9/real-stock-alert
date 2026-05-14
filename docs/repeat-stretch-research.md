# Repeat Stretch Research

Last updated: 2026-05-09

## Purpose

Test the idea before live implementation:

> If the same top candidates keep appearing while they are very stretched, should the bot wait for cool-off or confirmation instead of repeating the buy recommendation?

This started as research only. After the 2026-05-09 test, `skip_repeat_stretched` was selected for live buy scans.

## Tested Variants

- `baseline_full_two`: current Turbo top-2 behavior.
- `skip_repeat_stretched`: if a ticker was already a prior recommended target and is still stretched, skip it for new ranking.
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

## 2026-05-09 Result

| Strategy | Final | CAGR | Max Drawdown |
| --- | ---: | ---: | ---: |
| `skip_repeat_stretched` | `49.27x` | `59.5%` | `-33.4%` |
| baseline full Turbo | `46.83x` | `58.6%` | `-35.8%` |
| `skip_repeat_extreme` | `46.83x` | `58.6%` | `-35.8%` |
| `skip_all_extreme` | `33.60x` | `52.4%` | `-34.9%` |
| `half_stretched_baseline` | `29.64x` | `50.1%` | `-34.1%` |
| `skip_stretched_baseline` | `11.74x` | `34.3%` | `-29.3%` |

Decision: implement `skip_repeat_stretched` in live buy scans. Do not skip all stretched names.

Live clarification: opening, daily, and weekly messages all use the same rule. For message-to-message consistency, the live bot treats both prior recommended candidates and prior skipped repeat-stretched candidates as recent targets. This prevents a name from disappearing from repeat memory only because it was skipped in the last message.
