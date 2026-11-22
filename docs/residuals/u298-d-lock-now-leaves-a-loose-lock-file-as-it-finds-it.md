---
title: config.lock_now takes a lock file left at another mode as it finds it, so the driver and staging locks never harden one
found: at the review of #855, U298, 2026-11-21. On main as well.
issue: no
---

**The mechanism.** `core.config.lock_now`, which the job driver's lock (`core/jobs.py`) and the staging lock (`core/staging_lock.py`) take, opens its file with `os.open` at the private mode. `O_CREAT` applies a mode only when it creates the file, so a lock file already there at 0666 stays at 0666. The docstring warns about exactly that exposure: a lock any local account could hold refuses every later run. `flock_exclusive` takes a `harden` from its caller for this case; `lock_now` takes none. The review drove the driver lock with a file left at 0666, and it stayed at 0666 on the base and on the branch alike.

**Measured cost.** Not driven past the mode: nothing the review found produces a lock file at another mode, so reachability is unmeasured. U298 moved the function and changed none of it.

**Closes when:** `lock_now` hardens a file it did not create, or a test shows nothing can leave one. Ledger only.
