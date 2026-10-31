---
title: Whether a clone keeps a staged file's modification time to the nanosecond on the library volume is unmeasured, and a rehearsal depends on it
found: at the review of #343, U162, 2026-10-31.
issue: no
---

**The mechanism.** A landing's gate digests the staged folder as each file's name, size and `st_mtime_ns`, and a rehearsal refuses unless the plan at its area, over clones of those files, reads line for line as the live plan. The clone is `cp -c -p` on macOS and `shutil.copy2` elsewhere or where the volume does not clone. On Linux ext4 `copy2` round trips the nanoseconds and every rehearsal passes. On APFS through `cp -c -p`, or on exFAT through `copy2`, it was not measured.

**Measured cost.** Unmeasured; not drivable on the cloud container. If the time does not round trip, every rehearsal on that volume refuses `decision-stale` on the one `gate.files` line, which the refusal prints, and the feature is unusable there until fixed. Nothing is written or moved either way.

**Closes when:** the attended landing approved on `--rehearse` alone, which the record owes, reads a rehearsal that passed on the real volume, or a refusal on `gate.files` is driven and the clone is made to keep the time (an explicit `os.utime` with `ns=`). Ledger only.
