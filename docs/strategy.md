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

## Buy Rules

Candidates must satisfy:

- close above SMA50,
- SMA50 above SMA200,
- 63-day relative strength better than QQQ,
- average dollar volume above `$50M/day`.

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
- the stock closes below EMA21,
- the stock closes below SMA50,
- the trailing stop is hit,
- the stock drops out of the weekly top list on a weekly rebalance.

## Stops

Initial stop:

- higher of 12% below entry, or entry minus 2.5x ATR14.

Trailing stop:

- ratchets to the higher of 15% below highest high since entry, or highest high minus 3x ATR14.

## Manual Confirmation

The bot does not mark a candidate as owned. It only tracks a real position after `manual_bought` records the actual ticker, shares, fill price, and fill date.

The same applies to sells: cash and realized P&L only update after `manual_sold`.

