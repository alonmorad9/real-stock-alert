# REAL STOCK SYSTEM Report - 2026-05-20

Mode: `daily`
Capital mode: `TQQQ-out swing mode`
Master rule: TQQQ has priority: if tqqq-alert sends a TQQQ re-buy signal, sell real-stock positions and move the bucket back to TQQQ.
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
ATR cap: `10.0%`
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
- ATR cap: fresh buy candidates with ATR14 above 10% of price are skipped; this tested better than the prior live score.
- Risk `NORMAL` / score `0` controls size only. This run uses 100.0% of normal new-buy size.
- Reasons explain market-wide QQQ warnings; they do not pick the stocks.
- Overextension warnings are stock-specific. They warn about chasing hot names, but they do not add points to the score.
- `skip_repeat_stretched` means a recent recommended or skipped target is skipped again if it is still stretched.
- A hard down day may not remove a ticker if its 20d/63d momentum is still strongest.
- This real-stock bucket is temporary while TQQQ is out. The TQQQ repo itself waits in cash; if `tqqq-alert` sends a TQQQ re-entry signal, TQQQ takes priority.

## הסבר קצר בעברית

- `turbo`: מצב מומנטום אגרסיבי. הוא מחפש מניות מובילות, לא מניות זולות אחרי ירידה.
- הניקוד מבוסס על חוזק יחסי ל-63 יום ומומנטום ל-20 יום.
- מסנן ATR: מניה עם ATR14 מעל 10% מהמחיר תידחה לקנייה חדשה כי היא תנודתית מדי.
- רמת סיכון `NORMAL` / ניקוד `0` משפיעים רק על גודל הקנייה. בריצה הזו משתמשים ב-100.0% מגודל רגיל.
- אם יש כבר 2 פוזיציות מאושרות, לא קונים מניות חדשות רק בגלל המלצה חדשה.
- אם `tqqq-alert` נותן איתות כניסה ל-TQQQ, ה-TQQQ קודם למניות האלה.

## Real Account State

- Allocated cash: $2,699.66
- Tracked cash: $2,699.66
- Portfolio value estimate: $2,699.66
- Realized P&L: $0.00

## Open Positions

No confirmed real positions are currently tracked.

## Buy Candidates

Repeat-stretch memory from previous scan: `DDOG, ARM, INTC, AMD`.

## Skipped Candidates

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 62% above SMA50).
- `AMD` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 53% above SMA50, 8% above prior close).

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | MRVL | $186.80 | $1,349.83 | $1,349.83 | $164.38 | 116.4% | 18.7% |
| 2 | MU | $731.99 | $1,349.83 | $1,349.83 | $644.15 | 57.1% | 50.2% |

## Explicit Buy Instructions

- `MRVL`: suggested buy amount $1,349.83 (about 7.2261 shares at $186.80). Initial stop reference: $164.38.
- `MU`: suggested buy amount $1,349.83 (about 1.8441 shares at $731.99). Initial stop reference: $644.15.

## הוראות קנייה בעברית

- `MRVL`: סכום קנייה מוצע $1,349.83 (בערך 7.2261 מניות במחיר $186.80). סטופ התחלתי למעקב: $164.38.
- `MU`: סכום קנייה מוצע $1,349.83 (בערך 1.8441 מניות במחיר $731.99). סטופ התחלתי למעקב: $644.15.

## Overextension Warnings

- `MRVL`: HOT BUT STRETCHED: 40% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `MU`: HOT BUT STRETCHED: 45% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
