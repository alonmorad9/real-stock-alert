# REAL STOCK SYSTEM Report - 2026-05-20

Mode: `daily`
Capital mode: `TQQQ-out swing mode`
Master rule: TQQQ has priority: if tqqq-alert sends a TQQQ re-buy signal, sell real-stock positions and move the bucket back to TQQQ.
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $711.49
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

Repeat-stretch memory from previous scan: `ARM, DDOG, INTC, AMD`.

## Skipped Repeat Stretched Candidates

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 60% above SMA50).
- `AMD` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 53% above SMA50).

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | MRVL | $189.89 | $1,349.83 | $1,349.83 | $167.10 | 120.6% | 20.7% |
| 2 | MU | $721.96 | $1,349.83 | $1,349.83 | $635.32 | 55.0% | 48.1% |

## Explicit Buy Instructions

- `MRVL`: suggested buy amount $1,349.83 (about 7.1085 shares at $189.89). Initial stop reference: $167.10.
- `MU`: suggested buy amount $1,349.83 (about 1.8697 shares at $721.96). Initial stop reference: $635.32.

## Overextension Warnings

- `MRVL`: HOT BUT STRETCHED: 42% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `MU`: HOT BUT STRETCHED: 43% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
