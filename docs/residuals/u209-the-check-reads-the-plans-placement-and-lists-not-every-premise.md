---
title: The check before a held sync pair plan writes reads the lists, places and queued jobs, and not every premise the plan read
found: at the build and round two of #499, U209, 2026-11-05.
issue: no
---

**The mechanism.** A plan held across its gates is not made again, so what
it read can move before the write. The check reads the premises a write is
made from: each pair's two lists, the rows it adds, a self paired playlist's
place as discovery and `home_of` read it now, a made side's account folder,
a brought playlist's folder and title on the account, and the jobs queued
for its acquisitions. It does not read again whether an account playlist is
still one a pair may hold (a label, set or mirrored playlist since), the
pairs document's released sets, or whether two account playlists now take
one rekordbox name, each of which the plan reads and a plan made now could
decide differently.

**Measured cost.** Not driven: each needs another verb or a hand edit to move
between the gate and the write, and none was found that does.

**Closes when:** a producer is found for one, then the check reads it. Ledger
only.
