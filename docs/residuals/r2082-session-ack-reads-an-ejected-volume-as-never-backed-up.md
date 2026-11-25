---
title: The backup acknowledgment reads an ejected library volume's backup ages as never recorded, and the terminal rule mints over them
found: at review round one of #1093, R-2082, 2026-11-25.
issue: yes
---

**The mechanism.** `session_ack._shown_ages` calls `backup_facts.ages` with
no mount gate, and the backup record is library scoped, so off an ejected
volume the missing file reads as no fact. The session rule then refuses with
`backup-acknowledgment-backup-too-old`, saying the files portion's age is not
known (never-recorded) and to run a backup first. The terminal rule mints
over the same never recorded ages and writes the acknowledgment under the
configured root, recreating the root's state folder where the volume should
mount. Doctor's backup rows ask `core.preflight`'s rule first since R-2082;
this reader does not.

**Measured cost.** Driven at `46830cb7`: both portions recorded a day ago,
the library root renamed away. `crate --output json session ack --as
session` exits 32 with the false advice; nothing is lost, since it refuses.
`session_ack.record_acknowledgment(cfg, terminal=lambda: True)` minted over
never recorded ages and recreated the root's state folder, driven through the
terminal seam, not through the gate a person answers. On a Mac that folder
would sit at the volume's mount point on the boot disk (board bar b, and d
for the write).

**Closes when:** `_shown_ages`, or `record_acknowledgment` before it, asks
`core.preflight.library_state_is_readable` for the mount and refuses with a
cause naming the absent volume, never reading the ages or writing; tests
rename the root and drive both rules through the CLI. Earns an issue under
the board bar's (b), the product saying something false, and (d), a write
with no guard against an absent volume.
