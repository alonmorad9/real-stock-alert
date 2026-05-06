# Real Stock Strategy

Last updated: 2026-05-05

## Purpose

This repo manages alerts and durable state for a real-money stock pilot. It is not a paper portfolio and it is not the TQQQ strategy.

## Universe

The first universe is the explicit liquid growth list from the swing demo research:

- Nasdaq-100 style names
- mega-cap technology
- liquid semiconductors, software, internet, healthcare, and consumer growth names

The list is fixed in `research/real_stock_strategy.py` so signals do not change because a website constituent table changes.

## Market Filter

New buys are allowed only when:

- `QQQ` close is above `QQQ` SMA200.

If `QQQ` closes below SMA200:

- open positions are flagged for sale,
- new buys are blocked.

## Active Profile

The live profile is now `turbo` with max 2 positions.

The historical variant pack favored `turbo` max 2 for the user's requested high-risk, high-reward swing mode:

- final: `21.8x`
- CAGR: `44.8%`
- max drawdown: `-37.5%`
- trades: `282`

This is still research, not a guarantee.

## Buy Rules

Candidates must satisfy:

- close above SMA50,
- close above EMA21,
- positive 20-day and 63-day momentum,
- 63-day relative strength better than QQQ,
- average dollar volume above `$50M/day`.

The report may show an advisory `HOT BUT STRETCHED` warning. This does not remove a candidate or change its rank. It flags cases where the stock may be extended by RSI14, distance above SMA50, or a large opening move above the prior close.

## Market Risk Overlay

The live bot uses the `risk_balanced` overlay as allocation guidance for new buys:

- `NORMAL`: use normal suggested allocation.
- `ELEVATED`: use half-size new buys.
- `DEFENSIVE`: use half-size new buys and manually review risk. The overlay does not auto-sell.

The overlay scores QQQ using short-term trend, recent drops, distribution days, 20-day drawdown, RSI14, and distance above SMA20. This was selected from the historical risk-overlay research because half-sizing during elevated risk improved the turbo backtest without replacing the momentum engine.

Ranking favors:

- 63-day relative strength,
- 20-day momentum,
- strength above SMA50.

## Position Sizing

Default pilot sizing:

- allocated cash: `$1,000`,
- max positions: `2`,
- about 50% of available stock-pilot cash per position,
- no margin.

## Sell Rules

Positions are flagged for sale if:

- QQQ closes below SMA200,
- the stock closes below SMA50,
- the trailing stop is hit,
- the stock drops out of the weekly top list on a weekly rebalance.

## Stops

Initial stop:

- higher of 12% below entry, or entry minus 2.5x ATR14.

Trailing stop:

- ratchets to the higher of 18% below highest high since entry, or highest high minus 3.5x ATR14.

## Manual Confirmation

The bot does not mark a candidate as owned. It only tracks a real position after `manual_bought` records the actual ticker, shares, fill price, and fill date.

The same applies to sells: cash and realized P&L only update after `manual_sold`.
