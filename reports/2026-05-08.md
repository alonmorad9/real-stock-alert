# REAL STOCK SYSTEM Report - 2026-05-08

Mode: `daily`
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
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

## Skipped Repeat Stretched Candidates

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 88, 101% above SMA50, 14% above prior close).
- `AMD` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 81, 79% above SMA50, 11% above prior close).

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | MU | $746.81 | $500.00 | $500.00 | $657.19 | 72.5% | 77.6% |
| 2 | DDOG | $200.16 | $500.00 | $500.00 | $176.14 | 62.4% | 90.0% |

## Explicit Buy Instructions

- `MU`: suggested buy amount $500.00 (about 0.6695 shares at $746.81). Initial stop reference: $657.19.
- `DDOG`: suggested buy amount $500.00 (about 2.4980 shares at $200.16). Initial stop reference: $176.14.

## Overextension Warnings

- `MU`: HOT BUT STRETCHED: RSI14 88, 66% above SMA50, 15% above prior close. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `DDOG`: HOT BUT STRETCHED: RSI14 88, 57% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
