# Real Stock Strategy

Last updated: 2026-05-27

## Purpose

This repo manages alerts and durable state for a real-money stock pilot. It is not a paper portfolio and it is not the TQQQ strategy.

Current role: **inactive while TQQQ position is open**.

The TQQQ repo is the master controller. This repo manages real swing stocks only while `tqqq-alert` says the TQQQ strategy is out/waiting. If `tqqq-alert` sends a TQQQ buy or re-buy signal, sell all real-stock positions, confirm the sales here, then move the bucket back to TQQQ.

As of the current 2026-05-27 alignment, TQQQ is open, so this repo should have no deployable stock cash. Use this strategy again only after a future TQQQ exit and a fresh `set_cash <actual freed cash amount>`.

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

The live rank policy is `skip_repeat_stretched`. If a ticker was already a recent recommended target or recently skipped repeat-stretched target and is still marked `HOT BUT STRETCHED`, the bot skips it as a fresh buy recommendation and looks for the next qualified momentum name. This is meant to avoid repeatedly chasing the same overextended leaders when no real position was confirmed.

If a stretched ticker is not a repeat target, the report may still show an advisory `HOT BUT STRETCHED` warning. That warning flags cases where the stock may be extended by RSI14, distance above SMA50, or a large opening move above the prior close.

## Market Risk Overlay

The live bot uses the `risk_balanced` overlay as allocation guidance for new buys:

- `NORMAL`: use normal suggested allocation.
- `ELEVATED`: use half-size new buys.
- `DEFENSIVE`: use half-size new buys and manually review risk. The overlay does not auto-sell.

The overlay scores QQQ using short-term trend, recent drops, distribution days, 20-day drawdown, RSI14, and distance above SMA20. This was selected from the historical risk-overlay research because half-sizing during elevated risk improved the turbo backtest without replacing the momentum engine.

Ranking favors:

- 63-day relative strength,
- 20-day momentum.

The current Turbo score does not give extra points for being far above SMA50. SMA50 extension is still used for filters and overextension warnings, but the 2026-05-12 research found that removing it from the score improved the historical result and reduced drawdown.

Fresh buy candidates also use the tested `atr_cap_10pct` filter. If ATR14 is above 10% of price, the candidate is skipped as too volatile for a fresh buy. The 2026-05-21 research found this beat `score_no_extension` while keeping max drawdown about the same.

Opening, daily, and weekly scheduled reports skip US market holidays so this repo stays quiet on non-trading weekdays, matching the TQQQ repo behavior.

## Position Sizing

Sizing in TQQQ-out swing mode:

- allocated cash: the current freed TQQQ cash bucket after TQQQ exits,
- max positions: `2`,
- about 50% of available cash per position,
- no margin.

Use `python3 script.py set_cash AMOUNT` after a TQQQ exit to reset this repo's tracked cash bucket before following buy candidates. The TQQQ repo is TQQQ-only and waits in cash while out; it no longer treats XLK as the selected waiting asset.

## Sell Rules

Positions are flagged for sale if:

- `tqqq-alert` sends a TQQQ re-entry signal,
- QQQ closes below SMA200,
- the stock closes below SMA50,
- the trailing stop is hit,
- the stock drops out of the weekly top list on a weekly rebalance.

Opening and daily reports can still show fresh buy candidates, but they do not force a rotation sale just because a different stock ranks higher during that scan. This keeps the real-trade behavior cleaner: intraday/daily scans manage risk and information, while weekly scans handle rank-based rotation.

## Stops

Initial stop:

- higher of 12% below entry, or entry minus 2.5x ATR14.

Trailing stop:

- ratchets to the higher of 18% below highest high since entry, or highest high minus 3.5x ATR14.

## Manual Confirmation

The bot does not mark a candidate as owned. It only tracks a real position after `manual_bought` records the actual ticker, shares, fill price, and fill date.

The same applies to sells: cash and realized P&L only update after `manual_sold`.

## Bot-Only Benchmark

Every report includes a paper benchmark for the real-stock bot. This benchmark assumes the bot followed its own stock buy/sell instructions automatically, using the same Turbo candidates, market filter, risk sizing, stops, and sell rules.

The benchmark does not change the confirmed real account state. It exists only to compare:

- confirmed real-stock bucket value,
- versus the stock bot-only path.

The Telegram report shows the benchmark like a small paper account: current bot-only holdings, shares, entry price, current price, stop, value, return, and the latest simulated `BOT BUY`, `BOT SELL`, or `BOT HOLD` message. Those messages are only benchmark events, not real broker confirmations.

While TQQQ is open and this repo has `$0` deployable stock cash, the benchmark can still show the planning path using the reference cash amount. That keeps the daily message useful without pretending real stock trades happened.

If the benchmark needs a clean restart after a strategy-behavior fix, run `python3 script.py reset_bot_benchmark`. This clears only the paper benchmark; it does not touch real positions, real cash, or manual trade confirmations.
