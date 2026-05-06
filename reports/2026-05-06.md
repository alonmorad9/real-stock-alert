# REAL STOCK SYSTEM Report - 2026-05-06

Mode: `opening`
Profile: `turbo`
Max positions: `2`
Data source: `daily Yahoo bars with intraday 1-minute opening snapshot`

## Market Filter

- QQQ close: $691.65
- QQQ SMA200: $604.69
- Market filter: ON

## Market Risk Overlay

- Risk level: `NORMAL`
- Risk score: `1`
- Suggested new-buy size: `100.0%` of normal
- Action: Use normal suggested allocation.
- Reasons: QQQ hot RSI

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
| 1 | INTC | $111.26 | $500.00 | $500.00 | $97.91 | 114.6% | 88.7% |
| 2 | AMD | $407.80 | $500.00 | $500.00 | $358.87 | 89.4% | 75.9% |

## Explicit Buy Instructions

- `INTC`: suggested buy amount $500.00 (about 4.4940 shares at $111.26). Initial stop reference: $97.91.
- `AMD`: suggested buy amount $500.00 (about 1.2261 shares at $407.80). Initial stop reference: $358.87.

## Overextension Warnings

- `INTC`: HOT BUT STRETCHED: RSI14 86, 88% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `AMD`: HOT BUT STRETCHED: 66% above SMA50, 15% above prior close. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
