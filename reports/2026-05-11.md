# REAL STOCK SYSTEM Report - 2026-05-11

Mode: `daily`
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $713.29
- QQQ SMA200: $606.89
- Market filter: ON

## Market Risk Overlay

- Risk level: `NORMAL`
- Risk score: `2`
- Suggested new-buy size: `100.0%` of normal
- Action: Use normal suggested allocation.
- Reasons: QQQ hot RSI, QQQ extended above SMA20

## Quick Meaning

- `turbo`: aggressive momentum mode. It buys leaders, not cheap/dip names.
- Risk `NORMAL` / score `2` controls size only. This run uses 100.0% of normal new-buy size.
- Reasons explain market-wide QQQ warnings; they do not pick the stocks.
- Overextension warnings are stock-specific. They warn about chasing hot names.
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
| 1 | INTC | $129.44 | $500.00 | $500.00 | $113.91 | 141.4% | 98.6% |
| 2 | AMD | $458.79 | $500.00 | $500.00 | $403.74 | 96.1% | 85.9% |

## Explicit Buy Instructions

- `INTC`: suggested buy amount $500.00 (about 3.8628 shares at $129.44). Initial stop reference: $113.91.
- `AMD`: suggested buy amount $500.00 (about 1.0898 shares at $458.79). Initial stop reference: $403.74.

## Overextension Warnings

- `INTC`: HOT BUT STRETCHED: RSI14 89, 103% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `AMD`: HOT BUT STRETCHED: RSI14 80, 77% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
