---
title: A second stale cancel cancels the copy of a track set the first one kept, once no other copy is open
found: at the review of #379, U182, 2026-11-01.
issue: no
---

**The mechanism.** The stale cancel keeps the newest of several open intake jobs holding exactly the same tracks. Once the older copies are cancelled the kept job has no open copy, so the next `crate job cancel --stale-days N` reads it as a lone stale job and cancels it. Fable drove it: copies 50 and 45 days old, the command run twice, both cancelled.

**Measured cost.** Nothing false: the second run's `--dry-run` names the job as one it would cancel, and the kept line of the first run does not promise to keep it. A person who wanted the copy kept and runs the command again loses it from the queue, and `crate job resume` reopens it.

**Closes when:** the kept line says "until its copies are gone", or a kept job is remembered. Ledger only, a wording.
