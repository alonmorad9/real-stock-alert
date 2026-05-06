# Dip Entry Research

Last updated: 2026-05-06

## Purpose

Test a separate buy-the-dip entry system before adding it to live alerts.

This is not a replacement for Turbo. Turbo buys the strongest names. The dip system tries to buy strong names only after a red day.

## Tested Idea

A dip candidate must:

- trade above `$50M/day` average dollar volume,
- be in a market where `QQQ` is above SMA200,
- close above its own SMA50 and SMA200,
- have positive 20-day and 63-day momentum,
- have 63-day relative strength above QQQ,
- drop at least 3% or 5% on the signal day,
- drop more than QQQ on that day.

Signals are generated after the close and the backtest buys at the next open.

## Variants

- `dip_3pct_quick_bounce`: buy two 3% dips, exit at 8% profit target or after 15 days.
- `dip_5pct_quick_bounce`: buy two 5% dips, exit at 10% profit target or after 20 days.
- `dip_3pct_ride_trend`: buy two 3% dips, then use normal Turbo stop/SMA50 exits.
- `dip_5pct_ride_trend`: buy two 5% dips, then use normal Turbo stop/SMA50 exits.
- `dip_3pct_top_one_quick`: same as 3% quick bounce, but only one new entry per day.
- `dip_5pct_top_one_quick`: same as 5% quick bounce, but only one new entry per day.

The output includes the current Turbo full-two baseline for comparison.

## Run

```bash
python3 research/real_stock_strategy.py --dip-research --start 2018-01-01
```

Or run the `Real Stock Research` GitHub Action with:

- `kind`: `dip`
- `start`: `2018-01-01`

## Output

- `research/out/dip_entry_summary.csv`
- `research/out/dip_*_equity_curve.csv`
- `research/out/dip_*_trades.csv`

## 2026-05-06 Result

The first historical test did not support replacing Turbo with dip buying.

| Strategy | Final | CAGR | Max Drawdown |
| --- | ---: | ---: | ---: |
| Turbo baseline | `43.59x` | `57.2%` | `-35.8%` |
| Best dip variant, 3% dip and ride trend | `14.46x` | `37.8%` | `-34.9%` |
| 5% dip and ride trend | `9.65x` | `31.2%` | `-29.8%` |
| Best quick-bounce dip variant | `5.14x` | `21.7%` | `-24.2%` |

Decision: keep buy-the-dip as research/watchlist only. The live stock pilot remains Turbo top-2 momentum.
