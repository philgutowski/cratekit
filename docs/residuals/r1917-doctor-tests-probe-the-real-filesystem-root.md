---
title: Three doctor tests probe the real filesystem root with a directory, and one widens the test root guard to it, so a mutant there can leave an entry at the root
found: at the review of #966, R-1917, 2026-11-23.
issue: no
---

**The mechanism.** `tests/test_doctor.py` proves its read only volume answers
by making a directory directly under the real filesystem root
(`cratekit-u27-read-only-probe`, `cratekit-u27-finding-probe`,
`cratekit-u27-seed-probe`) and expecting EROFS, which macOS's system volume
gives. On a Linux container run as root the directory is made, removed at
once, and the test fails as machine bound. The seed test also sets
`config._TEST_WRITE_ROOT` to the filesystem root, so a mutation row that
drops its probe's early failure would let `_seed_taxonomy` write
`/.cratekit` on such a machine, R-1917's shape one file over.

**Measured cost.** None to a user, and no leak driven: on the base each
probe is removed before its test fails. R-1917 made the mutation driver stop
a batch at the child that adds an entry under the root, so a leak there is
caught where it happens rather than read by every later row; the entry would
still need a person to remove. The driver's own tests list a stand in root,
since a parallel worker's probe could otherwise read as a leak.

**Closes when:** the three tests probe a read only volume a fixture can
make, or read the volume they stand on before probing it, so no
test writes at the real filesystem root. Ledger only.
