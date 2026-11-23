---
title: An audio file removed since an adopt makes every restore reaching past that adopt end refused
found: at the review of #970, R-1924, 2026-11-23.
issue: no
---

**The mechanism.** A restore puts back the title tag and key tag of every
file a later session kept, and names a file that is gone as not written,
which ends the verb refused under `restore-tags-unwritten`. A file removed on
purpose, or one an adopt stopped before writing, is named on every run, the
dry run included, and the step "check each named file is there" cannot be met.

**Measured cost.** Driven at review round two with an adopt stopped before
its first file and one file unlinked: four of four runs, dry and real, exit
30 naming a file no session changed. The database half and every other file
land on each real run and the message is true. The stop needed an injected
fault and the removal was by hand.

**Closes when:** a file whose tags already read as kept, or that no session
wrote, is not named, or the refusal says the file is gone and how to restore
past it. Ledger only: the work lands and nothing false is said.
