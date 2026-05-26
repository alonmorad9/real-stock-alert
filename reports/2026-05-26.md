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
QQQ:           $730.08
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
Bot Value:     $2,804.38 (3.9%)
Real Bucket:   $0.00
Vs Bot-Only:   $-2,804.38 (-100.0%)
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
Current:       $493.44
Stop:          $431.40
Value:         $1,392.54
Return:        0.7%
Status:        HOLD

MU
Shares:        1.6087
Entry:         $860.00
Current:       $877.63
Stop:          $756.80
Value:         $1,411.84
Return:        2.0%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: AMD, MU, INTC, MRVL
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
INTC: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 57% above SMA50).
MRVL: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 49% above SMA50).

🥇 ARM
Price:         $312.32
Score:         163.68 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (4.3225 shares)
Normal Slot:   $1,349.99
Initial Stop:  $274.84
63d RS:        123.5%
20d Return:    44.7%
Stretch:       HOT BUT STRETCHED: 68% above SMA50

🥈 DDOG
Price:         $221.44
Score:         152.02 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (6.0964 shares)
Normal Slot:   $1,349.99
Initial Stop:  $194.87
63d RS:        91.8%
20d Return:    66.9%
Stretch:       HOT BUT STRETCHED: RSI14 89, 51% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
ARM: HOT BUT STRETCHED: 68% above SMA50
DDOG: HOT BUT STRETCHED: RSI14 89, 51% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
