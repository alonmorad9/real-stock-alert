📊 Real Stock Daily Report — 04/06/2026
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
QQQ:           $740.61
SMA200:        $620.16
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
Bot Value:     $2,967.13 (-2.0%)
Real Bucket:   $3,028.38
Vs Bot-Only:   $61.25 (2.1%)
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
Current:       $243.60
Stop:          $237.92
Value:         $1,491.23
Return:        -1.5%
Status:        HOLD

INTC
Shares:        13.2036
Entry:         $114.68
Current:       $111.78
Stop:          $103.84
Value:         $1,475.90
Return:        -2.5%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: MU, AMD, MRVL, ARM
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
MRVL: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 87, 95% above SMA50).
ARM: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 79% above SMA50).

🥇 DDOG
Price:         $243.60
Score:         139.86 — higher means stronger momentum rank
Suggested Buy: $1,514.19 (6.2159 shares)
Normal Slot:   $1,514.19
Initial Stop:  $214.37
63d RS:        77.3%
20d Return:    69.5%
Stretch:       HOT BUT STRETCHED: 49% above SMA50

🥈 PANW
Price:         $279.25
Score:         96.20 — higher means stronger momentum rank
Suggested Buy: $1,514.19 (5.4223 shares)
Normal Slot:   $1,514.19
Initial Stop:  $245.74
63d RS:        49.4%
20d Return:    52.0%
Stretch:       HOT BUT STRETCHED: 39% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
DDOG: HOT BUT STRETCHED: 49% above SMA50
PANW: HOT BUT STRETCHED: 39% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
