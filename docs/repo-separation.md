# Repo Separation

Keep the three systems separate.

| Repo | Purpose | Money |
| --- | --- | --- |
| `tqqq-alert` | Real TQQQ/manual safety strategy | Real |
| `swing-stock-alert` | Weekly top-2 stock strategy demo | Paper/demo |
| `real-stock-alert` | Real stock-buying strategy | Real |

Do not copy real stock positions into the swing demo repo.

Do not add the real stock strategy to the TQQQ repo.

Month-end review should inspect each repo's own state file:

- `tqqq-alert/position_state.json`
- `swing-stock-alert/pilot_state.json`
- `real-stock-alert/position_state.json`

