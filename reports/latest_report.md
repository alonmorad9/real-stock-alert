# REAL STOCK SYSTEM Report - 2026-05-14

Mode: `daily`
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $719.79
- QQQ SMA200: $609.12
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

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 70% above SMA50).
- `AMD` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 64% above SMA50).

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | ARM | $228.50 | $500.00 | $500.00 | $201.08 | 67.0% | 40.8% |
| 2 | DDOG | $202.84 | $500.00 | $500.00 | $178.50 | 40.8% | 64.3% |

## Explicit Buy Instructions

- `ARM`: suggested buy amount $500.00 (about 2.1882 shares at $228.50). Initial stop reference: $201.08.
- `DDOG`: suggested buy amount $500.00 (about 2.4650 shares at $202.84). Initial stop reference: $178.50.

## Overextension Warnings

- `ARM`: HOT BUT STRETCHED: 38% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `DDOG`: HOT BUT STRETCHED: RSI14 89, 51% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
