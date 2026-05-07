# REAL STOCK SYSTEM Report - 2026-05-07

Mode: `daily`
Profile: `turbo`
Max positions: `2`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $694.94
- QQQ SMA200: $605.39
- Market filter: ON

## Market Risk Overlay

- Risk level: `NORMAL`
- Risk score: `0`
- Suggested new-buy size: `100.0%` of normal
- Action: Use normal suggested allocation.

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
| 1 | INTC | $109.62 | $500.00 | $500.00 | $96.47 | 110.7% | 77.6% |
| 2 | AMD | $408.46 | $500.00 | $500.00 | $359.44 | 95.6% | 72.6% |

## Explicit Buy Instructions

- `INTC`: suggested buy amount $500.00 (about 4.5612 shares at $109.62). Initial stop reference: $96.47.
- `AMD`: suggested buy amount $500.00 (about 1.2241 shares at $408.46). Initial stop reference: $359.44.

## Overextension Warnings

- `INTC`: HOT BUT STRETCHED: RSI14 82, 81% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `AMD`: HOT BUT STRETCHED: 64% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
