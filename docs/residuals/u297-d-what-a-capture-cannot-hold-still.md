---
title: A behaviour capture cannot hold still a file's own times read back in the command that wrote it, or its change time, and no shipped scenario records one
found: at the build of #854, U297, 2026-11-21.
issue: no
---

**The mechanism.** The stage pins what Python reads: the clock, the two
duration clocks, the id sources and the rekordbox binding's row stamps. It
sets every file's access and modification time to the pinned instant between
commands (`Stage.settle`). It cannot set a change time at all, and a file
written and then read back for its times inside one command carries the real
time. A process id, a process start and a file's inode are read past by
`compare` where each capture holds its own. Product code that persists a
file's `st_mtime_ns` or `st_ctime_ns` taken in the same command (the library
index's cache key in `acquire/match.py`, the ISRC cache in
`acquire/isrc_cache.py`, the adoption fingerprint in `adopt/apply.py`) would
make two captures of one commit differ.

**Measured cost.** None today: the six shipped scenarios compare with no
difference, run after run. The first area card whose scenario reaches such a
write will see the equality test fail with the differing value shown, which
is loud, and will have to pair that value as a capture's own word or pin it.

**Closes when:** a scenario records such a value and the stage or `compare`
is taught it. Ledger only.
