---
title: Doctor's backup age checks read an ejected library volume as never recorded
found: at review round two of #1079, U960, 2026-11-25.
issue: yes
---

**The mechanism.** The backup facts file is library scoped (`state_files`
`_library("backup_facts")`), and `backup_facts._read` takes a missing file
for no fact. `doctor_backup._check_backup_portion` calls `backup_facts.ages`
with no mount gate, while `_check_backup_acknowledgment` beside it asks
`_library_state_unreadable` first. So with the library root absent, as
`/Volumes/<name>` is after an eject, `backup.age.files` and
`backup.age.database` read INFO "no completion has been recorded for this
portion here, which is the state of every library before a backup has run
once". U960's glance asks `core.preflight`'s rule first and reads the same
state unreadable, so doctor and the glance now disagree on that input.

**Measured cost.** Driven on the branch at `f10a9afb`: the root renamed
away, `crate --output json doctor` read both portions as never recorded. A
person is told no backup exists when the record is on the unplugged drive;
doctor reports the volume in its own rows, but these two rows say something
false (board bar b). On main before U960, unchanged by it.

**Closes when:** `_check_backup_portion` asks `_library_state_unreadable`
before reading and answers its note, as the acknowledgment check does, with
a test that renames the root and reads both rows. It earns an issue under
the board bar's (b), a clean report over state it could not read.
