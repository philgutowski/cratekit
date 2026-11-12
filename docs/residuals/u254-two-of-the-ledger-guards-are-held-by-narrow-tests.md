---
title: The applied ledger's no whole read test watches only Path.read_bytes, and the device in a mark's identity kills no test
found: at the review of #683, U254, round two, 2026-11-12.
issue: no
---

**The mechanism.** `test_a_mark_does_not_parse_the_ledger_it_appends_to` in
`tests/test_adopt_apply_journal_u254.py` counts reads of the ledger through
`Path.read_bytes`, which is how `apply._load` reads it today. A `_load` that
read through `open(...).read()` with the cache off would bring back the whole
read per mark, the square in the CPU, with the suite green. Separately, the
device field of `apply._as_left`'s identity can be dropped with no test dying,
since a file on another device at the same path almost always has another
inode too.

**Measured cost.** None today; the shipped code is correct. Driven by the
round two review on a scratch copy: both mutants pass every test in eleven
files. The size, inode and time fields each kill a test of their own.

**Closes when:** the no whole read test counts records parsed (or bytes read
at the ledger's path by any route), and a test moves the ledger to another
device, or the device field is accepted as belt and braces. Ledger only.
