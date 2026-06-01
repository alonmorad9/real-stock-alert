📊 Real Stock Daily Report — 01/06/2026
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
QQQ:           $742.74
SMA200:        $617.65
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
Bot Value:     $3,142.25 (3.8%)
Real Bucket:   $3,028.38
Vs Bot-Only:   $-113.87 (-3.6%)
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
Current:       $277.49
Stop:          $237.92
Value:         $1,698.70
Return:        12.2%
Status:        HOLD

INTC
Shares:        13.2036
Entry:         $114.68
Current:       $109.33
Stop:          $103.84
Value:         $1,443.55
Return:        -4.7%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: AMD, MRVL, ARM, MU
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
ARM: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 85, 100% above SMA50, 16% above prior close).
MU: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 82% above SMA50).

🥇 DDOG
Price:         $277.49
Score:         215.16 — higher means stronger momentum rank
Suggested Buy: $1,514.19 (5.4567 shares)
Normal Slot:   $1,514.19
Initial Stop:  $248.35
63d RS:        127.4%
20d Return:    97.5%
Stretch:       HOT BUT STRETCHED: RSI14 90, 78% above SMA50, 12% above prior close

🥈 CRWD
Price:         $782.17
Score:         145.44 — higher means stronger momentum rank
Suggested Buy: $1,514.19 (1.9359 shares)
Normal Slot:   $1,514.19
Initial Stop:  $698.15
63d RS:        80.9%
20d Return:    71.7%
Stretch:       HOT BUT STRETCHED: RSI14 90, 60% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
DDOG: HOT BUT STRETCHED: RSI14 90, 78% above SMA50, 12% above prior close
CRWD: HOT BUT STRETCHED: RSI14 90, 60% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
