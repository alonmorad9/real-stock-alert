📊 Real Stock Weekly Report — 29/05/2026
──────────────────────────────
Action: 🟢 REVIEW BUYS — Candidates available
Read first: TQQQ is the master system. Use these stock candidates only when the TQQQ bucket is available for stocks.
──────────────────────────────
Mode:          weekly
Capital Mode:  TQQQ-out swing mode
Profile:       turbo — aggressive momentum leaders, not dip buys
Max Positions: 2
Data Source:   daily Yahoo bars
──────────────────────────────
🧭 Market Filter
Meaning: controls whether new stock buys are allowed.
What to do: if this is OFF, do not start new stock positions.
QQQ:           $738.31
SMA200:        $616.82
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
Bot Value:     $3,028.38 (-0.0%)
Real Bucket:   $3,028.38
Vs Bot-Only:   $0.00 (0.0%)
Bot Cash:      $0.00
Bot Holding:   DDOG, INTC
Bot Actions:   bought DDOG, bought INTC
──────────────────────────────
🤖 Bot-Only Trade Log
Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.
- BOT BUY DDOG: $1,514.19 at $247.35 = 6.1216 shares. Initial stop $221.95.
- BOT BUY INTC: $1,514.19 at $114.68 = 13.2036 shares. Initial stop $100.92.
──────────────────────────────
📌 Bot-Only Holdings
DDOG
Shares:        6.1216
Entry:         $247.35
Current:       $247.35
Stop:          $221.95
Value:         $1,514.19
Return:        0.0%
Status:        HOLD

INTC
Shares:        13.2036
Entry:         $114.68
Current:       $114.68
Stop:          $100.92
Value:         $1,514.19
Return:        0.0%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: MU, MRVL, ARM, AMD
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
ARM: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 81, 78% above SMA50).
MU: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 74% above SMA50).

🥇 DDOG
Price:         $247.35
Score:         177.60 — higher means stronger momentum rank
Suggested Buy: $1,514.19 (6.1216 shares)
Normal Slot:   $1,514.19
Initial Stop:  $221.95
63d RS:        99.2%
20d Return:    87.1%
Stretch:       HOT BUT STRETCHED: RSI14 86, 62% above SMA50, 10% above prior close

🥈 INTC
Price:         $114.68
Score:         148.95 — higher means stronger momentum rank
Suggested Buy: $1,514.19 (13.2036 shares)
Normal Slot:   $1,514.19
Initial Stop:  $100.92
63d RS:        129.7%
20d Return:    21.4%
Stretch:       HOT BUT STRETCHED: 39% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
DDOG: HOT BUT STRETCHED: RSI14 86, 62% above SMA50, 10% above prior close
INTC: HOT BUT STRETCHED: 39% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
