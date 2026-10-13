---
title: An archived set's account playlist is refused by the rename rather than renamed under its mark
found: at the build of #317, U140, 2026-10-13.
issue: no
---

**The mechanism.** A set playlist the archive marked carries the
`DOWNLOADED ` prefix, and `sync mark`'s record holds the title before the
mark so `sync unmark` can restore it. `export set --rename` refuses such a
playlist by name (`export-set-rename-unresolved`) rather than retitle it to
the prefixed new name and rewrite the mark record, which was the
conservative call for an unattended build.

**Measured cost.** Driven on the disposable database: a set landed with its
account playlist recorded is archived and marked, and the rename refuses
with nothing written. A person runs `crate sync unmark --pass PASS`, the
rename, then the archive again. Neither live set is marked today.

**Closes when:** the rename writes the prefixed title and moves the mark
record's name with it, or the author keeps the three step path. Ledger only.
