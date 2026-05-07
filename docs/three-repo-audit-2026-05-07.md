# Three Repo Audit - 2026-05-07

## Source Of Truth

| Repo | Current Meaning | Source Of Truth | Status |
| --- | --- | --- | --- |
| `tqqq-alert` | Real TQQQ strategy | `position_state.json` | Cash, manual safety mode after `manual_sold` |
| `swing-stock-alert` | Weekly stock swing paper/demo tracker | `pilot_state.json` and reports | Paper positions `INTC`, `MRVL` |
| `real-stock-alert` | Real stock Turbo pilot | `position_state.json` | No real positions; latest candidates `INTC`, `AMD` |

## TQQQ Repo

Inspected path:

`/Users/alonmorad/Documents/Codex/2026-04-30/github-plugin-github-openai-curated-can/tqqq-alert`

Current real state:

- `position_open`: `false`
- `shares`: `0.0`
- `cash`: `$2,726.11`
- `last_action`: `manual_sold`
- `manual_exit_mode`: `true`
- `manual_exit_price`: `$67.37`
- `manual_exit_date`: `2026-05-05`
- `manual_exit_saw_below_sma`: `false`
- `waiting_for_early_reentry`: `false`
- `waiting_for_pullback`: `false`

Meaning:

- The repo should be treated as cash/no real TQQQ position.
- The current re-buy logic is manual safety mode, not early-warning recovery.
- The bot should wait for either:
  - a 7.5% pullback from `$67.37` while still above SMA200, or
  - a full SMA200 reset: price goes below SMA200 first, then later crosses back above SMA200.

Doc drift found:

- `docs/monthly-context.md` still shows the prior early-warning cash state.
- `docs/research-handoff.md` still shows the prior early-warning cash state.

The TQQQ repo is outside this writable workspace, so these files could not be patched from this audit run.

## Swing Repo

Inspected path:

`/Users/alonmorad/Documents/Codex/2026-05-04/files-mentioned-by-the-user-research/swing-stock-alert`

Current paper state:

- paper positions: `INTC`, `MRVL`
- latest paper value: `1.046144`
- latest paper return: `4.6144%`
- TQQQ line is only a market reference.

Meaning:

- This repo remains paper/demo only.
- It must not be used as the real TQQQ state.
- It must not be used as real stock ownership.

Doc drift found:

- `README.md` still says "current open TQQQ trade."
- `docs/tqqq-strategy-context.md` still contains older copied TQQQ state.
- Generated reports from 2026-05-04 and 2026-05-05 use historical wording about the TQQQ trade; treat those as historical reports, not current state.

The swing repo is outside this writable workspace, so these files could not be patched from this audit run.

## Real Stock Repo

Inspected path:

`/Users/alonmorad/Documents/Codex/2026-05-05/files-mentioned-by-the-user-new/real-stock-alert`

Current real-stock state:

- active profile: `turbo`
- allocated cash: `$1,000`
- cash: `$1,000`
- positions: none
- latest candidates: `INTC`, `AMD`
- market risk: `NORMAL`, score `1`
- risk overlay: `risk_balanced`, half-size new buys only when risk is elevated/defensive

Strategy decision:

- Keep Turbo top-2 momentum as the live real-stock strategy.
- Keep buy-the-dip as research/watchlist only because the dip backtest did not beat Turbo.

## Aligned Operating Plan

- TQQQ repo: real TQQQ source of truth; currently manual safety cash/re-entry.
- Swing repo: paper/demo stock swing comparison only.
- Real-stock repo: real stock Turbo pilot; no position exists until `manual_bought` records a real broker fill.

## Still Needed Outside This Workspace

Patch stale docs in the older repo folders:

- `tqqq-alert/docs/monthly-context.md`
- `tqqq-alert/docs/research-handoff.md`
- `swing-stock-alert/README.md`
- `swing-stock-alert/docs/tqqq-strategy-context.md`
