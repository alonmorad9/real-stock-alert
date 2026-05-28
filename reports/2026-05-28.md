📊 Real Stock Daily Report — 28/05/2026
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
QQQ:           $735.60
SMA200:        $616.02
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
Bot Value:     $2,754.31 (2.0%)
Real Bucket:   $0.00
Vs Bot-Only:   $-2,754.31 (-100.0%)
Bot Cash:      $0.00
Bot Holding:   MU, AMD
Bot Actions:   held
──────────────────────────────
🤖 Bot-Only Trade Log
Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.
- BOT HOLD: no bot-only buy or sell this run.
──────────────────────────────
📌 Bot-Only Holdings
MU
Shares:        1.4541
Entry:         $928.41
Current:       $923.52
Stop:          $817.00
Value:         $1,342.88
Return:        -0.5%
Status:        HOLD

AMD
Shares:        2.7243
Entry:         $495.54
Current:       $518.09
Stop:          $436.08
Value:         $1,411.43
Return:        4.6%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: ARM, MRVL, MU, AMD
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
ARM: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 73% above SMA50, 11% above prior close).
AMD: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 61% above SMA50).

🥇 INTC
Price:         $120.89
Score:         169.86 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (11.1671 shares)
Normal Slot:   $1,349.99
Initial Stop:  $106.38
63d RS:        145.0%
20d Return:    27.6%
Stretch:       HOT BUT STRETCHED: 49% above SMA50

🥈 DDOG
Price:         $225.24
Score:         133.82 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (5.9936 shares)
Normal Slot:   $1,349.99
Initial Stop:  $201.49
63d RS:        72.5%
20d Return:    68.1%
Stretch:       HOT BUT STRETCHED: RSI14 83, 49% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
INTC: HOT BUT STRETCHED: 49% above SMA50
DDOG: HOT BUT STRETCHED: RSI14 83, 49% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
