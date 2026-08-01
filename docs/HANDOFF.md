# Handoff: where Cratekit stands

Written 2026-08-01 so a session with no memory of the build can pick it up.

## State

`main` carries U1, U2, U3, U4, U5, U6, U13, U14, U31, U35. Pushed to the private
remote. CI green on Python 3.12 and 3.13 plus a cold-install job.

Three more units are committed on branches and **not yet merged**:

| branch | unit |
|---|---|
| `wt/u7` | the guarded rekordbox writer |
| `wt/u10` | the job engine |
| `wt/u15` | concurrent downloads with pacing |

Each is green on its own branch. **None has been verified on the combined tree.**
That matters: every previous wave produced at least one collision that existed
only after merging, including a duplicate dictionary key that the whole suite
passed with, and a unit whose verbs were named differently from the registry.

### Finish the merge like this

Merge one branch at a time, and after each one run the full battery on the
COMBINED tree before touching the next:

    .venv/bin/ruff check src tests scripts
    .venv/bin/python -m pytest
    .venv/bin/python scripts/scan_repo.py

A clean auto-merge is not evidence of compatibility. Then remove the worktrees
(`git worktree remove .worktrees/<name>`) and delete the branches.

## Where the reasoning lives

Everything that shaped these decisions is in the source repository, because it
quotes that system's paths and this repository's portability guard rejects those
by design:

- `DJ_tools/docs/plans/2026-08-01-001-feat-dj-product-reengineering-plan.md`, the plan
- `DJ_tools/docs/migration/00-SEAM-DECISIONS.md`, **authoritative** over any brief
- `DJ_tools/docs/migration/`, the six unit briefs and the wave prompts
- `DJ_tools/docs/runbooks/`, the U9 attended gate

Read the seam decisions before implementing anything. Part 5 in particular is
seven failure shapes learned the expensive way, and they apply to every unit.

## What is blocked, and on what

**U9, the attended spike, is the hard stop.** It gates U18, U20 and U21. A2 is
already answered and recorded as KTD3. A1 and A4 need the author at the machine
with rekordbox, about 1 hour 20 minutes, runbook ready. A3's question was settled
at the desk and its toggle is deliberately recommended against.

Unblocked by the three unmerged branches once they land: U8 and U32 from the
writer, U11 and U12 from the job engine.

## Open items that are not code

1. **The source system's writers refuse right now.** Its pinned rekordbox
   version is older than the installed application, so the pin raises before
   writing. That is the guard working, and re-validating it on a snapshot is a
   deliberate act rather than a number to edit.
2. **The vendored downloader has never been smoke-tested end to end.** Clone,
   install, authorize, download one track, confirm the file carries no tempo tag.
   That last check is the only end-to-end proof of the beatgrid patch, and the
   upstream wrote a tempo tag in three containers before it was patched.
3. `docs/residual-findings.md` carries nine recorded items with what closes each.

## Two hazards worth carrying forward

**Autoflush in the guard path.** Giving the cloud canary a real predicate turned
it from reading nothing into running a query, and an ORM query autoflushes: a
caller's pending write was flushed into the session and the additive whitelist
approved a commit it could no longer see. The guard would have passed a
forbidden write *because* the canary started working. Any unit adding a database
read to the guard path inherits this. A test pins it.

**Closing a database does not release it.** The binding closes the session and
leaves the engine's pooled connection open, so the process still holds the file
and both sidecars. Restoring over them then produces a disk I/O error against a
database that is perfectly intact, which is a terrifying message at exactly the
wrong moment. Fixed here by disposing the engine; still live in the source.
