📊 Real Stock Daily Report — 22/05/2026
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
QQQ:           $717.54
SMA200:        $613.60
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
Bot Holding:   ARM, MRVL
Bot Actions:   bought ARM, bought MRVL
──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: AMD, CRWD, INTC, DDOG
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
INTC: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 57% above SMA50).
DDOG: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: RSI14 89, 53% above SMA50).

🥇 ARM
Price:         $306.51
Score:         155.65 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (4.4044 shares)
Normal Slot:   $1,349.99
Initial Stop:  $269.73
63d RS:        128.2%
20d Return:    30.5%
Stretch:       HOT BUT STRETCHED: 68% above SMA50

🥈 MRVL
Price:         $196.33
Score:         150.59 — higher means stronger momentum rank
Suggested Buy: $1,349.99 (6.8762 shares)
Normal Slot:   $1,349.99
Initial Stop:  $172.77
63d RS:        133.1%
20d Return:    19.5%
Stretch:       HOT BUT STRETCHED: 43% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
ARM: HOT BUT STRETCHED: 68% above SMA50
MRVL: HOT BUT STRETCHED: 43% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
