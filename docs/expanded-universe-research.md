# Expanded Universe Research

Last updated: 2026-05-09

## Purpose

Test whether Turbo keeps recommending the same two stocks because the live universe is too narrow.

This does not change live alerts yet. It only compares historical results.

## Tested Universes

- `current_top2`: current fixed live universe, max 2 positions.
- `current_top3`: current fixed live universe, max 3 positions.
- `expanded_growth_top2`: current universe plus additional liquid/high-beta growth names, max 2 positions.
- `expanded_growth_top3`: same expanded growth basket, max 3 positions.
- `expanded_with_etfs_top2`: expanded growth basket plus liquid sector/leveraged ETFs, max 2 positions.
- `expanded_with_etfs_top3`: expanded growth/ETF basket, max 3 positions.

The expanded growth basket includes names such as `RDDT`, `COIN`, `HOOD`, `SOFI`, `VRT`, `ANET`, `NET`, `RBLX`, `UPST`, `AFRM`, and other high-beta liquid stocks. The ETF basket adds names such as `TQQQ`, `SOXL`, `SMH`, `XLE`, `XBI`, `ARKK`, and `XLK`.

## Run

```bash
python3 research/real_stock_strategy.py --universe-research --start 2018-01-01
```

Or run the `Real Stock Research` GitHub Action with:

- `kind`: `universe`
- `start`: `2018-01-01`

## Output

- `research/out/universe_comparison_summary.csv`
- `research/out/universe_*_equity_curve.csv`
- `research/out/universe_*_trades.csv`
- `research/out/universe_load_errors.csv`, if any tickers fail to load

## Decision Rule

Do not expand the live universe only because it produces different tickers. Expand it only if the broader universe improves the historical return/drawdown tradeoff and the trades look realistic enough to follow manually.
