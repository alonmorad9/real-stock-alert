# REAL STOCK SYSTEM Report - 2026-05-15

Mode: `weekly`
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $708.93
- QQQ SMA200: $609.83
- Market filter: ON

## Market Risk Overlay

- Risk level: `NORMAL`
- Risk score: `0`
- Suggested new-buy size: `100.0%` of normal
- Action: Use normal suggested allocation.

## Quick Meaning

- `turbo`: aggressive momentum mode. It buys leaders, not cheap/dip names.
- Score formula: 63d relative strength plus 20d momentum. Extra distance above SMA50 is no longer rewarded.
- Risk `NORMAL` / score `0` controls size only. This run uses 100.0% of normal new-buy size.
- Reasons explain market-wide QQQ warnings; they do not pick the stocks.
- Overextension warnings are stock-specific. They warn about chasing hot names, but they do not add points to the score.
- `skip_repeat_stretched` means a recent recommended or skipped target is skipped again if it is still stretched.
- A hard down day may not remove a ticker if its 20d/63d momentum is still strongest.

## Real Account State

- Allocated cash: $1,000.00
- Tracked cash: $1,000.00
- Portfolio value estimate: $1,000.00
- Realized P&L: $0.00

## Open Positions

No confirmed real positions are currently tracked.

## Buy Candidates

Repeat-stretch memory from previous scan: `MRVL, MU, INTC, AMD`.

## Skipped Repeat Stretched Candidates

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 57% above SMA50).
- `AMD` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 52% above SMA50).

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | DDOG | $207.98 | $500.00 | $500.00 | $183.02 | 48.2% | 64.3% |
| 2 | ARM | $209.16 | $500.00 | $500.00 | $184.06 | 49.0% | 25.4% |

## Explicit Buy Instructions

- `DDOG`: suggested buy amount $500.00 (about 2.4041 shares at $207.98). Initial stop reference: $183.02.
- `ARM`: suggested buy amount $500.00 (about 2.3905 shares at $209.16). Initial stop reference: $184.06.

## Overextension Warnings

- `DDOG`: HOT BUT STRETCHED: RSI14 89, 53% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
