---
title: With no census, record or files fact on record, one stray file at an unmounted volume's mount point is mirrored as the library and the whole mirror is archived
found: at the round one review of #893, R-1761, 2026-11-21.
issue: no
---

**The mechanism.** The content proof in `modules/tools/backup.py`'s
`_unproven` measures the root against the census, then the record, then the
library's own files fact. When none of the three is there, a fresh
installation or installation state wiped while the volume is away, a root
holding one file outside the state folder is no new library (it holds a
file) and has no history to fall short of, so the full sync runs over it and
moves every mirror file into the dated archive. The identity proof refuses
this wherever a recorded identity is read, so the hole is a platform that
reads none, today every Linux volume.

**Measured cost.** Driven by the round one and round two reviews with the
installation state removed and the stray file written by hand: 12 of 12
mirror files archived, recoverable from the archive until the rotation
purges it at the second completed run after. No producer of a stray file at
a mount point was found: three candidates (a refused plan, a run time
failure, a flagged run) were driven and none leaves one.

**Closes when:** a run with no history at all lists the remote's top level,
or is held to `--max-delete 0` like a root holding none of the library's
files, at the cost of a first backup failing where the mirror holds files
the library lost since another installation's last run. Ledger only.
