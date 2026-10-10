---
title: An edit to the taxonomy copy in the instant before the upgrade writes it is overwritten
found: at the watcher's review of #300, U132, 2026-10-10.
issue: no
---

**The mechanism.** `crate taxonomy upgrade` plans again after the answer and
refuses a plan whose digest moved, then reads the copy once more as bytes and
refuses those as stale too when they no longer read as the planned text. Those
bytes are the backup and the restore. What is left is the span between that
last read and the atomic replace of the copy, which writes the backup in
between: an edit saved by hand inside it is replaced by the upgraded text, and
the backup holds the copy from before the edit. Read from the code, not driven.

**Measured cost.** The span is one backup write of a 35 KB file, milliseconds.
An edit made any time before it, including between the answer and the second
plan, is refused and kept, which
`test_an_edit_after_the_second_plan_is_refused_as_stale` drives. No other
process writes the copy.

**Closes when:** the write takes a lock that hand edits honour, which none do,
or a decision records the span as accepted. Ledger only.
