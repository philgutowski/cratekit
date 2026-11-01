---
title: Six guards of the custom playlist twins kill no test, most of them behind the gate's own digest
found: at the review of #330, U149, 2026-11-01.
issue: no
---

**The mechanism.** The review reverted each guard of `sync/twins.py`, `sync/pair_cli.py` and the landing's twin path and ran the unit's two test files. These killed nothing: `recheck`'s gone rows check, `assert_read_back`, `recheck_landing`'s held name check, the `written_for` filter in `native.plan_rows`, the unpaired term of `pair_cli.Plan.writes` (which nothing in `src` reads), and `write_landing`'s filter of a twin whose INBOX playlist holds nothing. The fix round pinned three more that had killed nothing: the SQL confinement wired through `assert_confined`, the live filter on the mirror's links, and the folding of two account tracks of one ISRC onto one row.

**Measured cost.** None driven. Both rechecks were reached by drives and refused, but the gate's digest on the replan refused first, so they are race guards between the replan and the write. The rest are dead or defensive paths whose producer was not found. The second review measured that `recheck`'s gone rows check and `assert_read_back` each kill a test once the guard in front of them is removed, so they are second layers rather than guards nothing covers.

**Closes when:** a test reaches each one, or it is removed as redundant. Ledger only: a guard that kills zero is maintainer facing, and the writes it sits on are each covered by another guard that does kill.
