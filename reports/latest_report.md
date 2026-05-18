# REAL STOCK SYSTEM Report - 2026-05-18

Mode: `daily`
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $705.88
- QQQ SMA200: $610.55
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

Repeat-stretch memory from previous scan: `MU, MRVL, INTC, AMD`.

## Skipped Repeat Stretched Candidates

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 53% above SMA50).
- `AMD` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 48% above SMA50).

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | DDOG | $208.82 | $500.00 | $500.00 | $183.76 | 52.8% | 61.0% |
| 2 | PANW | $247.55 | $500.00 | $500.00 | $222.39 | 33.9% | 46.0% |

## Explicit Buy Instructions

- `DDOG`: suggested buy amount $500.00 (about 2.3944 shares at $208.82). Initial stop reference: $183.76.
- `PANW`: suggested buy amount $500.00 (about 2.0198 shares at $247.55). Initial stop reference: $222.39.

## Overextension Warnings

- `DDOG`: HOT BUT STRETCHED: RSI14 90, 52% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `PANW`: HOT BUT STRETCHED: RSI14 96, 40% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
