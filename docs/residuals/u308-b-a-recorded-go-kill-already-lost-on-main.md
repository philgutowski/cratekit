---
title: The recorded kill u108-a G05, the go's digest covering the jobs it would resume, survives on main
found: at the review of #865, U308, 2026-11-22.
issue: no
---

**The mechanism.** `docs/mutation/u108-a.json` records `G05_digest_covers_resume`
(in `label/go.py`, `Summary.plan`: the digest leaves out the jobs a go would
resume) as killed by
`test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again`.
Applied verbatim to `go.py` on `main` at `c919209`, all 110 tests of
`tests/test_label_sync_go.py` pass, the named test included, run alone and in
its file. So the kill was lost before U308, which keeps the row's state as it
found it; U308's replay before measures it on the base.

The replay before first measured it killed on `main`, by one death on the
full suite: `tests/test_repair_rows.py`'s inode bound test, which fails on this
container's disk whatever the code (#702). That batch subtracted the measured
baseline alone; measured again subtracting the two inode bound tests as well,
as the other batches did, the row is a zero on `main`, so no kill of it is owed.

**Measured cost.** Not driven to a user: a go whose resumed jobs changed between
its gate and its write would be approved on the old digest.

**Closes when:** a test drives a second go whose open jobs change after the
gate and asserts `decision-stale`, killing G05 again. Ledger only.
