---
title: A frozen mirror plan answered after a bare sync pair paired the same WIP set copies it a second time
found: at the review of #1062, U959, 2026-11-24.
issue: no
---

**The mechanism.** `account_mirror._wip` reads the pair record at the plan
(`_paired`), and the run that answers the mirror's gate rebuilds from the
frozen library (R-1031, U222), reading no pair again. A bare `sync pair`
applied between the mirror's gate and its answer pairs a WIP set into `WIP `,
and the answer still creates the mirror's copy in `WIP`; the two titles
differ, so the plan's check for a person's playlist of the title does not
stop it.

**Measured cost.** Not driven end to end: the reviewer read the frozen
rebuild ignoring later rekordbox changes, which
`test_the_answering_run_applies_the_wip_plan_its_gate_showed` shows, and did
not run the interleave in one world. It needs a person to run a bare
`sync pair` between the two halves of a mirror run, which the sync pass never
does. Its reachability is unmeasured.

**Closes when:** the mirror's apply reads the pair record again and leaves a
WIP set a pair took since the gate, or the reverse rule makes the mirror's
copy the only one. Ledger only.
