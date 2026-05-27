📊 Real Stock Daily Report — 27/05/2026
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
QQQ:           $729.45
SMA200:        $615.20
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
Bot Value:     $2,699.99 (0.0%)
Real Bucket:   $0.00
Vs Bot-Only:   $-2,699.99 (-100.0%)
Bot Cash:      $0.00
Bot Holding:   MU, AMD
Bot Actions:   bought MU, bought AMD
──────────────────────────────
🤖 Bot-Only Trade Log
Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.
- BOT BUY MU: $1,349.99 at $928.41 = 1.4541 shares. Initial stop $817.00.
- BOT BUY AMD: $1,349.99 at $495.54 = 2.7243 shares. Initial stop $436.08.
──────────────────────────────
📌 Bot-Only Holdings
MU
Shares:        1.4541
Entry:         $928.41
Current:       $928.41
Stop:          $817.00
Value:         $1,350.00
Return:        -0.0%
Status:        HOLD

AMD
Shares:        2.7243
Entry:         $495.54
Current:       $495.54
Stop:          $436.08
Value:         $1,350.00
Return:        0.0%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: MRVL, DDOG, ARM, INTC
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
INTC: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 53% above SMA50).

🥇 MU
Price:         $928.41
Score:         173.76 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (1.4541 shares)
Normal Slot:   $1,349.99
Initial Stop:  $817.00
63d RS:        98.1%
20d Return:    84.1%
Stretch:       HOT BUT STRETCHED: 73% above SMA50

🥈 AMD
Price:         $495.54
Score:         164.56 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (2.7243 shares)
Normal Slot:   $1,349.99
Initial Stop:  $436.08
63d RS:        116.6%
20d Return:    53.3%
Stretch:       HOT BUT STRETCHED: 57% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
MU: HOT BUT STRETCHED: 73% above SMA50
AMD: HOT BUT STRETCHED: 57% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
