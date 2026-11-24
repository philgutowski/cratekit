---
title: A sync pair answer stopped because the mirror copied a WIP set since the plan says the playlist was moved
found: at the review of #1062, U959, 2026-11-24.
issue: no
---

**The mechanism.** `sync/pair_check.py` discovers again before it writes,
now leaving out a WIP playlist the account mirror copies (U959). A set the
mirror copied between a bare `sync pair`'s plan and its answer is then no
longer found, and the check refuses `decision-stale` with "the rekordbox
playlist ... was moved since the plan, and is no longer one a sync of every
pair would make". Nothing moved: the mirror took it.

**Measured cost.** The stop and the replan are right and nothing is written,
driven by `test_a_wip_set_the_mirror_copies_after_the_plan_is_never_paired_at_the_answer`
with the ledger patched to the mirror's record; only the reason's words are
false. A real mirror apply between the two runs was not driven.

**Closes when:** the check names the mirror when the account mirror's ledger
holds the playlist's WIP title. Ledger only, a wording fix.
