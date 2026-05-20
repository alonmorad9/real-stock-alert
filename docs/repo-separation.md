# Repo Separation

Keep the three systems separate.

| Repo | Purpose | Money |
| --- | --- | --- |
| `tqqq-alert` | Real TQQQ/manual safety strategy | Real |
| `swing-stock-alert` | Weekly top-2 stock strategy demo | Paper/demo |
| `real-stock-alert` | Real stock-buying strategy | Real |

Do not copy real stock positions into the swing demo repo.

Do not add the real stock strategy to the TQQQ repo.

Current combined behavior:

- `tqqq-alert` is the master controller.
- When TQQQ is in-position, capital belongs in TQQQ.
- When TQQQ is out/waiting, this repo can manage the freed TQQQ cash as real top-2 swing stock positions.
- When `tqqq-alert` sends a TQQQ re-buy signal, sell all real-stock positions first and move the cash back to TQQQ.

Month-end review should inspect each repo's own state file:

- `tqqq-alert/position_state.json`
- `swing-stock-alert/pilot_state.json`
- `real-stock-alert/position_state.json`

The detailed month-end checklist is in [month-end-alignment.md](month-end-alignment.md).
