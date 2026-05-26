📊 Real Stock Daily Report — 26/05/2026
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
QQQ:           $730.28
SMA200:        $614.41
Status:        ON
──────────────────────────────
🛡️ Market Risk Overlay
Meaning: controls suggested buy size only; it does not choose tickers and does not auto-sell.
What to do: NORMAL means use the full suggested buy amount; ELEVATED/DEFENSIVE means size down.
Risk Level:    NORMAL
Risk Score:    0
Buy Size:      100.0% of normal
Reasons:       none
Action:        Use normal suggested allocation.
──────────────────────────────
⚙️ Strategy Settings
Meaning: these rules decide which stocks appear in the candidate list.
What to do: use the score and warnings together; the highest score is not a guarantee.
Turbo:         ranks strong momentum leaders
Score:         63d relative strength vs QQQ + 20d return
Rank Policy:   skip_repeat_stretched
ATR Cap:       10.0% max ATR14/price for fresh buys
Repeat Rule:   recent stretched names are skipped so the list does not chase the same hot ticker forever
──────────────────────────────
💼 Real Stock Bucket
Allocated:     $0.00
Tracked Cash:  $0.00
Planning Cash: $2,699.99 — used only to size suggestions in this message
Open:          0 confirmed positions
Value Est.:    $0.00
Realized P&L:  $0.00
──────────────────────────────
🧪 Bot-Only Benchmark
Meaning: paper path showing what this stock bot would do if its own buy/sell instructions were followed automatically.
What to do: use this to compare your confirmed real-stock bucket against the bot path; it is not a trade instruction.
Start Cash:    $2,699.99
Bot Value:     $2,863.23 (6.0%)
Real Bucket:   $0.00
Vs Bot-Only:   $-2,863.23 (-100.0%)
Bot Cash:      $0.00
Bot Holding:   AMD, MU
Bot Actions:   held
──────────────────────────────
🤖 Bot-Only Trade Log
Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.
- BOT HOLD: no bot-only buy or sell this run.
──────────────────────────────
📌 Bot-Only Holdings
AMD
Shares:        2.8221
Entry:         $490.23
Current:       $503.89
Stop:          $431.40
Value:         $1,422.03
Return:        2.8%
Status:        HOLD

MU
Shares:        1.6087
Entry:         $860.00
Current:       $895.88
Stop:          $756.80
Value:         $1,441.20
Return:        4.2%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: ARM, DDOG, INTC, MRVL
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
INTC: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 58% above SMA50).
ARM: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 73% above SMA50).

🥇 AMD
Price:         $503.89
Score:         160.87 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (2.6791 shares)
Normal Slot:   $1,349.99
Initial Stop:  $443.42
63d RS:        115.3%
20d Return:    50.6%
Stretch:       HOT BUT STRETCHED: 63% above SMA50

🥈 MU
Price:         $895.88
Score:         157.83 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (1.5069 shares)
Normal Slot:   $1,349.99
Initial Stop:  $788.37
63d RS:        94.1%
20d Return:    70.8%
Stretch:       HOT BUT STRETCHED: 70% above SMA50, 19% above prior close

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
AMD: HOT BUT STRETCHED: 63% above SMA50
MU: HOT BUT STRETCHED: 70% above SMA50, 19% above prior close
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
