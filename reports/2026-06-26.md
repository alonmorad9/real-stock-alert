📊 Real Stock Weekly Report — 26/06/2026
──────────────────────────────
Action: 👀 WATCHLIST — Planning only while TQQQ is open
Read first: TQQQ is the master system. Use these stock candidates only when the TQQQ bucket is available for stocks.
──────────────────────────────
Mode:          weekly
Capital Mode:  inactive while TQQQ position is open
Profile:       turbo — aggressive momentum leaders, not dip buys
Max Positions: 2
Data Source:   daily Yahoo bars
Telegram:      weekly routine message; opening/daily stay silent unless a real sell alert fires
──────────────────────────────
🧭 Market Filter
Meaning: controls whether new stock buys are allowed.
What to do: if this is OFF, do not start new stock positions.
QQQ:           $706.52
SMA200:        $630.66
Status:        ON
──────────────────────────────
🛡️ Market Risk Overlay
Meaning: controls suggested buy size only; it does not choose tickers and does not auto-sell.
What to do: NORMAL means use the full suggested buy amount; ELEVATED/DEFENSIVE means size down.
Risk Level:    DEFENSIVE
Risk Score:    6
Buy Size:      50.0% of normal
Reasons:       QQQ below SMA20, QQQ below SMA10, QQQ 5d drop, distribution days, 20d drawdown
Action:        Use half-size only for new buys. Do not auto-sell from this overlay.
──────────────────────────────
⚙️ Strategy Settings
Meaning: these rules decide which stocks appear in the candidate list.
What to do: use the score and warnings together; the highest score is not a guarantee.
Turbo:         ranks strong momentum leaders
Score:         RS63-heavy: 63d relative strength vs QQQ + 20d return
Rank Policy:   skip_repeat_stretched
Rotation:      two_week_confirm (2 weekly checks)
ATR Cap:       8.0% max ATR14/price for fresh buys
Repeat Rule:   recent stretched names are skipped so the list does not chase the same hot ticker forever
──────────────────────────────
💼 Real Stock Bucket
Allocated:     $0.00
Tracked Cash:  $0.00
Planning Cash: $2,697.38 — used only to size suggestions in this message
Open:          0 confirmed positions
Value Est.:    $0.00
Realized P&L:  $0.00
──────────────────────────────
🧪 Bot-Only Benchmark
Meaning: paper path showing what this stock bot would do if its own buy/sell instructions were followed automatically.
What to do: use this to compare your confirmed real-stock bucket against the bot path; it is not a trade instruction.
Start Cash:    $2,697.38
Bot Value:     $2,760.33 (2.3%)
Real Bucket:   $0.00
Vs Bot-Only:   $-2,760.33 (-100.0%)
Bot Cash:      $1,035.12
Bot Holding:   AMD, PANW
Bot Actions:   sold AMD, sold DDOG, bought AMD, bought PANW
──────────────────────────────
🤖 Bot-Only Trade Log
Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.
- BOT SELL AMD: 2.7545 shares at $521.58; proceeds $1,436.67; P&L $87.98 (6.5%). Reason: out of confirmed top ranks for 2 weekly checks.
- BOT SELL DDOG: 2.8337 shares at $239.77; proceeds $679.44; P&L $35.22 (5.5%). Reason: out of confirmed top ranks for 2 weekly checks.
- BOT BUY AMD: $690.08 at $521.58 = 1.3231 shares. Initial stop $458.99.
- BOT BUY PANW: $1,035.12 at $304.20 = 3.4028 shares. Initial stop $275.06.
──────────────────────────────
📌 Bot-Only Holdings
AMD
Shares:        1.3231
Entry:         $521.58
Current:       $521.58
Stop:          $458.99
Value:         $690.08
Return:        0.0%
Status:        HOLD

PANW
Shares:        3.4028
Entry:         $304.20
Current:       $304.20
Stop:          $275.06
Value:         $1,035.12
Return:        0.0%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Watchlist only. No real stock cash is allocated while TQQQ is open.
Do not use these as real buy instructions unless the TQQQ bucket is later moved back here with set_cash.

Repeat Memory: PANW, LRCX, MU, INTC
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
MU: skipped because ATR14 is 9.5%, above the 8.0% fresh-buy cap.
INTC: skipped because ATR14 is 8.5%, above the 8.0% fresh-buy cap.

Watchlist Candidates
🥇 AMD
Price:         $521.58
Score:         172.88 — higher means stronger momentum rank
Real Buy:      $0.00 while TQQQ is open
Initial Stop:  $458.99
63d RS:        132.7%
20d Return:    0.7%
Stretch:       OK

🥈 PANW
Price:         $304.20
Score:         102.58 — higher means stronger momentum rank
Real Buy:      $0.00 while TQQQ is open
Initial Stop:  $275.06
63d RS:        71.3%
20d Return:    18.0%
Stretch:       OK
