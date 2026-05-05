# Aggressive Swing Research

Last updated: 2026-05-05

## Goal

Compare higher-risk, higher-reward versions before changing live real-money rules.

## Variants

`base`

- current conservative weekly top-2 profile,
- max 2 positions,
- QQQ SMA200 market filter,
- EMA21 exit,
- 12%/2.5 ATR initial stop,
- 15%/3 ATR trailing stop.

`aggressive`

- heavier weight on relative strength and 20-day momentum,
- tests max 1, 2, and 3 positions,
- QQQ SMA200 market filter,
- EMA21 exit,
- tighter 10%/2 ATR initial stop,
- tighter 12%/2.5 ATR trailing stop.

`turbo`

- fastest swing profile,
- allows close above EMA21/SMA50 instead of requiring SMA50 above SMA200,
- requires positive 20-day and 63-day momentum,
- uses SMA50 exit instead of EMA21 exit,
- looser 12%/2.5 ATR initial stop,
- looser 18%/3.5 ATR trailing stop.

## Run

```bash
python3 research/real_stock_strategy.py --research --start 2018-01-01
```

Outputs:

- `research/out/aggressive_variant_summary.csv`
- `research/out/*_equity_curve.csv`
- `research/out/*_trades.csv`

## Important

This research compares historical behavior only. It does not prove the best future strategy. Before switching live rules, check CAGR, max drawdown, trade count, and whether the behavior is realistic enough to follow manually.

