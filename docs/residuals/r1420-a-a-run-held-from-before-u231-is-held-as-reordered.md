---
title: A continue of a run held from before U231, whose order was refused after moves landed, is held as reordered by a person nobody was
found: at the review of #619, R-1420, 2026-11-07.
issue: no
---

**The mechanism.** R-1420 reads a part written pair's account order at the
check before a continue whenever its steps carry `ordering` and no `moving`
(`_ordered_by_this_run` in `sync/pair_cli.py`), since U231's adapter records
its moves before the first is sent. A run planned and refused under a build
from before U231 moved tracks with no `moving` step, so its continue finds
the playlist where those moves left it and refuses `decision-stale`, "was
reordered since the plan".

**Measured cost.** Driven on the fake account only, by the rewritten
`test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`:
the continue refuses as moved with nothing written, and a fresh `crate sync
pair` finishes the stopped write from the side that led (U225). No loss; the
person is told of a reorder nobody made and runs one more command.
Reachability unmeasured: it needs a run held on the machine from the U220 to
U231 window, refused after moves and not yet continued.

**Closes when:** a held run from before U231 has aged out, or the check
tells a pre U231 record from a refusal that sent nothing. Ledger only.
