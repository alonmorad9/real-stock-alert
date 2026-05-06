# Predictive Risk Overlay Research

Last updated: 2026-05-06

## Goal

Test whether early-warning market risk signals improve the live `turbo` stock strategy before changing real-money behavior.

This is research only. The live bot should not auto-block, reduce, or sell based on these rules until the results are reviewed.

## Inputs

The overlay scores QQQ market risk using:

- QQQ below SMA10/SMA20,
- QQQ 5-day drop,
- recent high-volume distribution days,
- QQQ 20-day drawdown,
- QQQ RSI14 overextension,
- QQQ distance above SMA20.

## Policies Tested

- `none`: baseline turbo max 2.
- `block_elevated`: skip new buys when market risk is elevated.
- `half_elevated`: use half-size new buys when market risk is elevated.
- `exit_defensive`: exit positions when risk reaches a defensive threshold.

## Selected Live Use

The live bot uses `risk_balanced` as guidance only:

- normal risk: normal new-buy allocation,
- elevated or defensive risk: half-size new buys,
- no automatic selling from this overlay.

Telegram reports should show explicit dollar instructions for the risk-adjusted buy amount.

## Run

```bash
python3 research/real_stock_strategy.py --risk-research --start 2018-01-01
```

Or run the `Real Stock Research` GitHub Action with:

- `kind`: `risk`
- `start`: `2018-01-01`

Outputs:

- `research/out/risk_overlay_summary.csv`
- `research/out/risk_*_equity_curve.csv`
- `research/out/risk_*_trades.csv`
- `research/out/risk_*_risk_events.csv`
