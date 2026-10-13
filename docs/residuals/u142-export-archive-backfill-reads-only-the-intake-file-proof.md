---
title: The no name export archive still reads only the intake file proof, while organize also reads an INSPIRATION playlist
found: at the review of #319, U142, 2026-10-13.
issue: no
---

**The mechanism.** U142 gave `crate organize`'s set step a second proof of a
set's download, a playlist of the set's name under the declared INSPIRATION
folder. `crate export archive` with no name, the backfill in
`export/set_cli.py`, still proves a set only by `_proof_for_set`, an intake
file named for it, and lists any other set as waiting with "no intake file
proves its download". The brief scoped the second proof to organize, so the
backfill was left as it was.

**Measured cost.** Read from the code and not driven: a set with no intake
file and an INSPIRATION playlist of its name is planned and archived by
`crate organize` (driven, `tests/test_organize.py`) and would be listed as
waiting by `crate export archive`. Nothing is lost and nothing false is
written; the backfill's waiting line is true of its own rule, and organize
finishes the workflow.

**Closes when:** both verbs read one shared proof rule, the intake file or
the INSPIRATION playlist, or the backfill's waiting line names organize as
the verb that reads the second proof. Ledger only.
