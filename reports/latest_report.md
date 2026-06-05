📊 Real Stock Weekly Report — 05/06/2026
──────────────────────────────
Action: 👀 WATCHLIST — Planning only while TQQQ is open
Read first: TQQQ is the master system. Use these stock candidates only when the TQQQ bucket is available for stocks.
──────────────────────────────
Mode:          weekly
Capital Mode:  inactive while TQQQ position is open
Profile:       turbo — aggressive momentum leaders, not dip buys
Max Positions: 2
Data Source:   daily Yahoo bars
──────────────────────────────
🧭 Market Filter
Meaning: controls whether new stock buys are allowed.
What to do: if this is OFF, do not start new stock positions.
QQQ:           $705.06
SMA200:        $620.85
Status:        ON
──────────────────────────────
🛡️ Market Risk Overlay
Meaning: controls suggested buy size only; it does not choose tickers and does not auto-sell.
What to do: NORMAL means use the full suggested buy amount; ELEVATED/DEFENSIVE means size down.
Risk Level:    DEFENSIVE
Risk Score:    5
Buy Size:      50.0% of normal
Reasons:       QQQ below SMA20, QQQ below SMA10, QQQ 5d drop, 20d drawdown
Action:        Use half-size only for new buys. Do not auto-sell from this overlay.
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
Start Cash:    $3,028.38
Bot Value:     $2,668.13 (-11.9%)
Real Bucket:   $0.00
Vs Bot-Only:   $-2,668.13 (-100.0%)
Bot Cash:      $654.70
Bot Holding:   MU, DDOG
Bot Actions:   sold INTC, bought DDOG
──────────────────────────────
🤖 Bot-Only Trade Log
Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.
- BOT SELL INTC: 13.2036 shares at $99.17; proceeds $1,309.40; P&L $-204.79 (-13.5%). Reason: trailing stop hit.
- BOT BUY DDOG: $654.70 at $234.11 = 2.7966 shares. Initial stop $206.02.
──────────────────────────────
📌 Bot-Only Holdings
MU
Shares:        1.5726
Entry:         $933.44
Current:       $864.01
Stop:          $821.43
Value:         $1,358.73
Return:        -7.4%
Status:        HOLD

DDOG
Shares:        2.7966
Entry:         $234.11
Current:       $234.11
Stop:          $206.02
Value:         $654.70
Return:        0.0%
Status:        HOLD

──────────────────────────────
📦 Open Positions
No confirmed real stock positions are currently tracked.
──────────────────────────────
🧾 Buy Candidates
Repeat Memory: MU, AMD, MRVL, ARM
Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.

Skipped Candidates
ARM: skipped because ATR14 is 10.5%, above the 10.0% fresh-buy cap.
MRVL: skipped because it was already a recent target and is still stretched (HOT BUT STRETCHED: 59% above SMA50).

🥇 DDOG
Price:         $234.11
Score:         90.10 — higher means stronger momentum rank
Suggested Buy: $675.00 (2.8832 shares)
Normal Slot:   $1,349.99
Initial Stop:  $206.02
63d RS:        68.5%
20d Return:    24.0%
Stretch:       HOT BUT STRETCHED: 41% above SMA50

🥈 PANW
Price:         $272.05
Score:         81.71 — higher means stronger momentum rank
Suggested Buy: $675.00 (2.4812 shares)
Normal Slot:   $1,349.99
Initial Stop:  $239.40
63d RS:        47.1%
20d Return:    38.4%
Stretch:       HOT BUT STRETCHED: 33% above SMA50

⚠️ Overextension Warnings
Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.
DDOG: HOT BUT STRETCHED: 41% above SMA50
PANW: HOT BUT STRETCHED: 33% above SMA50
──────────────────────────────
These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.
