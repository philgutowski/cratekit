---
title: With the database outside the library root, a backup's database item publishes the fact file into whatever is at the root, an unmounted volume's mount point included
found: at the round two review of #893, R-1761, 2026-11-21.
issue: no
---

**The mechanism.** The fact file is library state under the root, and the
database portion publishes its age there whether or not the files portion
proved the root, creating the state folder at a mount point, and the root
itself where an unmount removed it. Before round two's fix that file was the
emptied flag's proof, and the reviewer drove a second flagged ask through it
to an emptied mirror; the flag now asks for a files fact, which the database
item does not write.

**Measured cost.** Driven at round two: the database snapshot and its age
are real, and the fact file sits on the boot disk at the mount point, where
a remount hides it and the library's own file no longer carries that age.

**Closes when:** the database portion publishes its age only into a root the
files proof passed, or the files portion's refusal stops the job's database
item from writing there. Ledger only.
