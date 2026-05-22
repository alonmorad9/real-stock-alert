# REAL STOCK SYSTEM Report - 2026-05-22

Mode: `daily`
Capital mode: `inactive while TQQQ position is open`
Master rule: TQQQ has priority: if tqqq-alert sends a TQQQ re-buy signal, sell real-stock positions and move the bucket back to TQQQ.
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
ATR cap: `10.0%`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $720.19
- QQQ SMA200: $613.61
- Market filter: ON
- Meaning: new stock buys are allowed only when QQQ is above its SMA200. If this is OFF, do not start new stock positions.

## Market Risk Overlay

- Risk level: `NORMAL`
- Risk score: `0`
- Suggested new-buy size: `100.0%` of normal
- Action: Use normal suggested allocation.
- Reasons: none

## Strategy Notes

- Turbo profile: aggressive momentum mode. It looks for current leaders, not cheap/dip names.
- Candidate score: higher is better. It combines 63-day relative strength versus QQQ and 20-day return. Extra distance above SMA50 is not rewarded.
- Rank policy `skip_repeat_stretched`: if a recent recommendation is still overextended, skip it and show the next qualified stock instead.
- ATR cap `10.0%`: skip fresh buys when ATR14 is too large versus price. Current live cap is 10%.
- Market risk `NORMAL` / score `0`: this controls position size only. NORMAL means use 100% of the normal suggested buy amount.
- Overextension warnings: stock-specific caution flags. They do not block the recommendation unless the ticker is also a repeat-stretched candidate.
- TQQQ priority: if the TQQQ repo gives a buy/re-buy signal, TQQQ remains the master system.

## Real Account State

- Allocated cash: $0.00
- Tracked cash: $0.00
- Planning cash used for suggested buys: $2,699.99
- Portfolio value estimate: $0.00
- Realized P&L: $0.00

## Open Positions

No confirmed real positions are currently tracked.

## Buy Candidates

Repeat-stretch memory from previous scan: `DDOG, AMD, INTC`.

## Skipped Candidates

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 59% above SMA50).
- `DDOG` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 89, 52% above SMA50).

| Rank | Ticker | Close | Score | Normal Allocation | Suggested Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | ARM | $314.08 | 164.22 | $1,349.99 | $1,349.99 | $276.39 | 133.8% | 33.8% |
| 2 | MRVL | $197.30 | 151.93 | $1,349.99 | $1,349.99 | $173.62 | 133.9% | 20.1% |

## Explicit Buy Instructions

- `ARM`: suggested buy amount $1,349.99 (about 4.2983 shares at $314.08). Initial stop reference: $276.39.
- `MRVL`: suggested buy amount $1,349.99 (about 6.8423 shares at $197.30). Initial stop reference: $173.62.

## Overextension Warnings

- `ARM`: HOT BUT STRETCHED: 72% above SMA50. This means the stock is already hot. The recommendation can still be valid, but avoid chasing if the live open is far above the shown price.
- `MRVL`: HOT BUT STRETCHED: 43% above SMA50. This means the stock is already hot. The recommendation can still be valid, but avoid chasing if the live open is far above the shown price.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
