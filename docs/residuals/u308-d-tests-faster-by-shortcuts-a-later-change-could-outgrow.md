---
title: The label and favourites suites run faster on three shortcuts a later change could outgrow
found: at the review of #865, U308, 2026-11-22.
issue: no
---

**The mechanism.** U308 took about half the summed test time out of its 34
files with three shortcuts. An autouse `one_parser` fixture in
`tests/test_label_workers.py`, imported by most of the label and favourites
suites, keeps one verb parser per module membership in a module global and
reuses it across drives and tests in a worker, where a real run builds one per
process; it holds while no label builder reads state beyond membership and no
test patches a handler after the build (the reviewer ran all fifteen files with a
fresh parser per drive, 1,037 passed either way). The favourites suites'
`_landed_hearts` seeds the rows a landing writes instead of driving the two act
landing, except one test; the seeded rows differ from a landing's in folder,
playlist membership, device and empty columns, and forcing a real landing in
every call passed 93 of 93. And `no_disk_flush` in `tests/test_label_sync.py`
turns SQLite durability and `os.fsync` off for the sync and go suites, none of
whose tests asserts durability and no recorded kill names fsync.

**Measured cost.** None today, each measured as above. A later builder that
reads state at build time, a backfill rule that reads what only a landing
writes, or a durability guard in the sync record would pass these suites
unseen.

**Closes when:** the suite card (#869, U312) moves the parser cache into the
shared test support with its rule beside it, or a change that breaks one of the
three conditions takes its shortcut out. Ledger only.
