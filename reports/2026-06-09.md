📊 Real Stock Daily Report — 09/06/2026
──────────────────────────────
Action: 👀 WATCHLIST — Planning only while TQQQ is open
Read first: TQQQ is the master system. Use these stock candidates only when the TQQQ bucket is available for stocks.
──────────────────────────────
Mode:          daily
Capital Mode:  inactive while TQQQ position is open
Profile:       turbo — aggressive momentum leaders, not dip buys
Max Positions: 2
Data Source:   daily Yahoo bars
──────────────────────────────
🧭 Market Filter
Meaning: controls whether new stock buys are allowed.
What to do: if this is OFF, do not start new stock positions.
QQQ:           $707.83
SMA200:        $622.35
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
Bot Value:     $2,598.19 (-3.7%)
Real Bucket:   $0.00
Vs Bot-Only:   $-2,598.19 (-100.0%)
Bot Cash:      $644.22
Bot Holding:   AMD, DDOG
Bot Actions:   sold MU, bought DDOG
──────────────────────────────
🤖 Bot-Only Trade Log
Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.
- BOT SELL MU: 1.3767 shares at $935.89; proceeds $1,288.44; P&L $-60.25 (-4.5%). Reason: trailing stop hit.
- BOT BUY DDOG: $644.22 at $227.34 = 2.8337 shares. Initial stop $200.06.
──────────────────────────────
📌 Bot-Only Holdings
AMD
Shares:        2.7545
Entry:         $489.64
Current:       $475.50
Stop:          $430.88
Value:         $1,309.76
Return:        -2.9%
Status:        HOLD

DDOG
Shares:        2.8337
Entry:         $227.34
Current:       $227.34
Stop:          $200.06
Value:         $644.22
Return:        -0.0%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Watchlist only. No real stock cash is allocated while TQQQ is open.
Do not use these as real buy instructions unless the TQQQ bucket is later moved back here with set_cash.

Repeat Memory: MU, AMD, MRVL, ARM
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
MRVL: skipped because ATR14 is 11.6%, above the 8.0% fresh-buy cap.
ARM: skipped because ATR14 is 12.4%, above the 8.0% fresh-buy cap.

Watchlist Candidates
🥇 AMD
Price:         $475.51
Score:         154.58 — higher means stronger momentum rank
Real Buy:      $0.00 while TQQQ is open
Initial Stop:  $418.44
63d RS:        117.4%
20d Return:    3.6%
Stretch:       OK

🥈 DDOG
Price:         $227.34
Score:         95.33 — higher means stronger momentum rank
Real Buy:      $0.00 while TQQQ is open
Initial Stop:  $200.06
63d RS:        68.1%
20d Return:    12.4%
Stretch:       HOT BUT STRETCHED: 33% above SMA50
