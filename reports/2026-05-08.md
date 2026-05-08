# REAL STOCK SYSTEM Report - 2026-05-08

Mode: `weekly`
Profile: `turbo`
Max positions: `2`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $711.23
- QQQ SMA200: $606.14
- Market filter: ON

## Market Risk Overlay

- Risk level: `NORMAL`
- Risk score: `2`
- Suggested new-buy size: `100.0%` of normal
- Action: Use normal suggested allocation.
- Reasons: QQQ hot RSI, QQQ extended above SMA20

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
| 1 | INTC | $124.92 | $500.00 | $500.00 | $109.93 | 130.1% | 100.3% |
| 2 | AMD | $455.19 | $500.00 | $500.00 | $400.57 | 101.6% | 85.8% |

## Explicit Buy Instructions

- `INTC`: suggested buy amount $500.00 (about 4.0026 shares at $124.92). Initial stop reference: $109.93.
- `AMD`: suggested buy amount $500.00 (about 1.0984 shares at $455.19). Initial stop reference: $400.57.

## Overextension Warnings

- `INTC`: HOT BUT STRETCHED: RSI14 88, 101% above SMA50, 14% above prior close. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `AMD`: HOT BUT STRETCHED: RSI14 81, 79% above SMA50, 11% above prior close. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
