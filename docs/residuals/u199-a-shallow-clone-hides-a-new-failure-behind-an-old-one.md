---
title: A cloud session's clone is shallow, and the Linux battery subtracts a failure by test id, so a test the missing history already reddens hides any new failure of its own
found: at the build of #484, U199, 2026-11-03.
issue: no
---

**The mechanism.** A cloud container's checkout is a shallow clone
(`git rev-parse --is-shallow-repository` prints `true`), so a test that reads
an old commit fails on the base for want of it. `scripts/cloud_battery.py
baseline` records that failure as the machine's by its node id, and `compare`
and `scripts/mutate.py --known-failures` subtract the same id from every later
run. A test held red by the missing history is therefore never read again in
the cloud, whatever else breaks it. `test_every_moved_paragraph_is_in_a_fragment_byte_for_byte`
failed on the base with "the split base a984968 is not in this clone"; when
U195 then reworded a moved record, the same test also failed for that reason,
and the cloud read it as the machine's.

**Measured cost.** U195's defect reached `main` unseen, and the macOS battery
refused the v0.5.0 cut on it, holding the release and the attended cards
waiting on it. On d8633c17 the shallow baseline held 167 ids; after `git
fetch --unshallow` on the same container and commit, 163, and the difference
is history alone: five tests of `tests/modules/test_reports.py` pass, and the
byte for byte test fails with the Mac's own error, the lost R-301 paragraph.
So six tests were unread in every cloud battery, one of them over a real
defect. The mutation driver showed the same masking on this unit: with the
shallow baseline as its known failures, the row that empties the rewording
table read as a zero, because the one test it kills was subtracted; measured
against a baseline of the branch head with full history, it is killed. A
person using the shipped verbs pays nothing, so it is maintainer facing and
earns no issue by the board bar.

**Closes when:** `cloud_battery.py baseline` refuses a shallow clone, or
unshallows it first, so that a test is subtracted only for a cause the
machine owns, and the cloud unit skill says the same of the mutation
driver's known failures. A one line `git fetch --unshallow origin main`
before the baseline would have shown this defect on U195's own branch.
