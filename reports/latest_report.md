# REAL STOCK SYSTEM Report - 2026-05-13

Mode: `daily`
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $714.71
- QQQ SMA200: $608.35
- Market filter: ON

## Market Risk Overlay

- Risk level: `NORMAL`
- Risk score: `1`
- Suggested new-buy size: `100.0%` of normal
- Action: Use normal suggested allocation.
- Reasons: QQQ hot RSI

## Quick Meaning

- `turbo`: aggressive momentum mode. It buys leaders, not cheap/dip names.
- Score formula: 63d relative strength plus 20d momentum. Extra distance above SMA50 is no longer rewarded.
- Risk `NORMAL` / score `1` controls size only. This run uses 100.0% of normal new-buy size.
- Reasons explain market-wide QQQ warnings; they do not pick the stocks.
- Overextension warnings are stock-specific. They warn about chasing hot names, but they do not add points to the score.
- `skip_repeat_stretched` means a recent top pick is skipped if it is still stretched, so the bot stops repeating the same overextended names.
- A hard down day may not remove a ticker if its 20d/63d momentum is still strongest.

## Real Account State

- Allocated cash: $1,000.00
- Tracked cash: $1,000.00
- Portfolio value estimate: $1,000.00
- Realized P&L: $0.00

## Open Positions

No confirmed real positions are currently tracked.

## Buy Candidates

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | INTC | $120.29 | $500.00 | $500.00 | $105.86 | 132.4% | 85.2% |
| 2 | AMD | $445.50 | $500.00 | $500.00 | $392.04 | 91.9% | 72.6% |

## Explicit Buy Instructions

- `INTC`: suggested buy amount $500.00 (about 4.1566 shares at $120.29). Initial stop reference: $105.86.
- `AMD`: suggested buy amount $500.00 (about 1.1223 shares at $445.50). Initial stop reference: $392.04.

## Overextension Warnings

- `INTC`: HOT BUT STRETCHED: RSI14 80, 80% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `AMD`: HOT BUT STRETCHED: 65% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
