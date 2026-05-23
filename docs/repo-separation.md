# Repo Separation

Keep the three systems separate.

| Repo | Purpose | Money |
| --- | --- | --- |
| `tqqq-alert` | Real TQQQ/manual safety strategy | Real |
| `real-stock-alert` | Real stock-buying strategy plus bot-only stock benchmark | Real + benchmark |
| `swing-stock-alert` | Paused old weekly top-2 stock demo archive | Historical paper/demo |

Do not copy real stock positions into the paused swing demo repo.

Do not add the real stock strategy to the TQQQ repo.

Current combined behavior:

- `tqqq-alert` is the master controller.
- When TQQQ is in-position, capital belongs in TQQQ.
- When TQQQ is out/waiting, this repo can manage the freed TQQQ cash as real top-2 swing stock positions.
- When `tqqq-alert` sends a TQQQ re-buy signal, sell all real-stock positions first and move the cash back to TQQQ.
- `real-stock-alert` reports include the active stock bot-only benchmark.
- `swing-stock-alert` is paused and kept only for historical May paper-pilot context.

Month-end review should inspect active state first:

- `tqqq-alert/position_state.json`
- `real-stock-alert/position_state.json`

Optional historical context:

- `swing-stock-alert/pilot_state.json`

The detailed month-end checklist is in [month-end-alignment.md](month-end-alignment.md).
