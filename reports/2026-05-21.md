# REAL STOCK SYSTEM Report - 2026-05-21

Mode: `daily`
Capital mode: `inactive while TQQQ position is open`
Master rule: TQQQ has priority: if tqqq-alert sends a TQQQ re-buy signal, sell real-stock positions and move the bucket back to TQQQ.
Profile: `turbo`
Max positions: `2`
Rank policy: `skip_repeat_stretched`
ATR cap: `10.0%`
Data source: `daily Yahoo bars`

## Market Filter

- QQQ close: $714.51
- QQQ SMA200: $612.84
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

- Allocated cash: $0.00
- Tracked cash: $0.00
- Portfolio value estimate: $0.00
- Realized P&L: $0.00

## Open Positions

No confirmed real positions are currently tracked.

## Buy Candidates

Repeat-stretch memory from previous scan: `ARM, DDOG, INTC, AMD`.

## Skipped Candidates

- `INTC` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 58% above SMA50).
- `ARM` skipped: it was already a recent target and is still stretched (HOT BUT STRETCHED: 67% above SMA50, 16% above prior close).

| Rank | Ticker | Close | Normal Allocation | Risk-Adjusted Buy | Initial Stop | 63d RS | 20d Return |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | MRVL | $190.69 | $0.00 | $0.00 | $167.81 | 122.5% | 15.2% |
| 2 | MU | $762.10 | $0.00 | $0.00 | $670.65 | 60.6% | 58.2% |

## Explicit Buy Instructions

- `MRVL`: suggested buy amount $0.00 (about 0.0000 shares at $190.69). Initial stop reference: $167.81.
- `MU`: suggested buy amount $0.00 (about 0.0000 shares at $762.10). Initial stop reference: $670.65.

## הוראות קנייה בעברית

- `MRVL`: סכום קנייה מוצע $0.00 (בערך 0.0000 מניות במחיר $190.69). סטופ התחלתי למעקב: $167.81.
- `MU`: סכום קנייה מוצע $0.00 (בערך 0.0000 מניות במחיר $762.10). סטופ התחלתי למעקב: $670.65.

## Overextension Warnings

- `MRVL`: HOT BUT STRETCHED: 41% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.
- `MU`: HOT BUT STRETCHED: 49% above SMA50. Momentum rank stays valid, but consider hold/not-add discipline if the open is too stretched.

These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.
