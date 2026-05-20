# REAL STOCK SYSTEM Report - 2026-05-20

Mode: `daily`
Capital mode: `TQQQ-out swing mode`
Master rule: TQQQ has priority: if tqqq-alert sends a TQQQ re-buy signal, sell real-stock positions and move the bucket back to TQQQ.
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $713.15
- QQQ SMA200: $612.05
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
- This real-stock bucket is temporary while TQQQ is out. If `tqqq-alert` sends a TQQQ re-entry signal, TQQQ takes priority.

## Real Account State

- Allocated cash: $2,699.66
- Tracked cash: $2,699.66
- Portfolio value estimate: $2,699.66
- Realized P&L: $0.00

## Open Positions

No confirmed real positions are currently tracked.

## Buy Candidates

Repeat-stretch memory from previous scan: `MRVL, MU, INTC, AMD`.

## Skipped Repeat Stretched Candidates

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 62% above SMA50).
- `AMD` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 53% above SMA50, 8% above prior close).

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | DDOG | $212.24 | $1,349.83 | $1,349.83 | $186.77 | 57.7% | 60.6% |
| 2 | ARM | $256.73 | $1,349.83 | $1,349.83 | $225.92 | 83.9% | 30.6% |

## Explicit Buy Instructions

- `DDOG`: suggested buy amount $1,349.83 (about 6.3599 shares at $212.24). Initial stop reference: $186.77.
- `ARM`: suggested buy amount $1,349.83 (about 5.2578 shares at $256.73). Initial stop reference: $225.92.

## Overextension Warnings

- `DDOG`: HOT BUT STRETCHED: RSI14 89, 50% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `ARM`: HOT BUT STRETCHED: 47% above SMA50, 15% above prior close. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
