📊 Real Stock Daily Report — 03/06/2026
──────────────────────────────
Action: 🟢 REVIEW BUYS — Candidates available
Read first: TQQQ is the master system. Use these stock candidates only when the TQQQ bucket is available for stocks.
──────────────────────────────
Mode:          daily
Capital Mode:  TQQQ-out swing mode
Profile:       turbo — aggressive momentum leaders, not dip buys
Max Positions: 2
Data Source:   daily Yahoo bars
──────────────────────────────
🧭 Market Filter
Meaning: controls whether new stock buys are allowed.
What to do: if this is OFF, do not start new stock positions.
QQQ:           $744.21
SMA200:        $619.33
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
Allocated:     $3,028.38
Tracked Cash:  $3,028.38
Planning Cash: $3,028.38 — used only to size suggestions in this message
Open:          0 confirmed positions
Value Est.:    $3,028.38
Realized P&L:  $0.00
──────────────────────────────
🧪 Bot-Only Benchmark
Meaning: paper path showing what this stock bot would do if its own buy/sell instructions were followed automatically.
What to do: use this to compare your confirmed real-stock bucket against the bot path; it is not a trade instruction.
Start Cash:    $3,028.38
Bot Value:     $3,020.61 (-0.3%)
Real Bucket:   $3,028.38
Vs Bot-Only:   $7.77 (0.3%)
Bot Cash:      $0.00
Bot Holding:   DDOG, INTC
Bot Actions:   held
──────────────────────────────
🤖 Bot-Only Trade Log
Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.
- BOT HOLD: no bot-only buy or sell this run.
──────────────────────────────
📌 Bot-Only Holdings
DDOG
Shares:        6.1216
Entry:         $247.35
Current:       $250.33
Stop:          $237.92
Value:         $1,532.43
Return:        1.2%
Status:        HOLD

INTC
Shares:        13.2036
Entry:         $114.68
Current:       $112.71
Stop:          $103.84
Value:         $1,488.18
Return:        -1.7%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: MU, AMD, MRVL, ARM
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
MRVL: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 86, 91% above SMA50).
ARM: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 84, 92% above SMA50).

🥇 DDOG
Price:         $250.33
Score:         154.15 — higher means stronger momentum rank
Suggested Buy: $1,514.19 (6.0488 shares)
Normal Slot:   $1,514.19
Initial Stop:  $220.29
63d RS:        89.5%
20d Return:    71.8%
Stretch:       HOT BUT STRETCHED: 55% above SMA50

🥈 INTC
Price:         $112.71
Score:         129.07 — higher means stronger momentum rank
Suggested Buy: $1,514.19 (13.4344 shares)
Normal Slot:   $1,514.19
Initial Stop:  $99.18
63d RS:        125.3%
20d Return:    4.2%
Stretch:       HOT BUT STRETCHED: 30% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
DDOG: HOT BUT STRETCHED: 55% above SMA50
INTC: HOT BUT STRETCHED: 30% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
