---
title: The rotation dating a batch by its first landing rather than its latest kills no test
found: at the mutation table of #356, U175, 2026-11-01.
issue: no
---

**The mechanism.** `rotate.landings` keeps, for each playlist a native record
names by identifier, the EARLIEST committed landing, so a batch is as old as
its first tracks. Taking the latest instead (row R2 of
`docs/mutation/u175.md`) kills nothing on the full suite: no test lands into
one playlist twice and then plans a rotation.

**Measured cost.** Not driven to a user. The input exists: a set landing
adds to the INBOX playlist an earlier landing of the same set made (U135), so
a later landing would make the batch read younger and rotate later than it
should. Sampled by U175 as an existing guard; it predates the unit.

**Closes when:** a rotation test lands one set twice on two days and asserts
the batch is aged from the first.
