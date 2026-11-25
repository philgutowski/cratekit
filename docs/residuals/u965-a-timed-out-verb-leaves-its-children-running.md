---
title: The app's runner ends a timed out verb's own process and not its children, with a three second grace that cuts a job's clean stop short
found: at the review of #1084, U965, 2026-11-25.
issue: no
---

**The mechanism.** `CrateRunner.runBlocking` in `app/Sources/CrateEngine/CrateRunner.swift` sends SIGTERM to crate's own pid at the timeout, then SIGKILL after `terminationGrace`, three seconds. Foundation's `Process` starts crate in the app's process group and offers no way to start a new one, so a child crate started (rclone, ffmpeg, a pool worker) is not signalled and keeps running after the app reports `timedOut`. A job driver that stops cleanly on SIGTERM at an item boundary may need longer than three seconds, and every call defaults to a 60 second timeout whatever the verb.

**Measured cost.** Not driven: no container runs Swift, and no shipped caller runs a long verb, since the app in U965 only shows the crate setup state. The timeout tests use a fake that `exec`s one process, so they cannot see a grandchild. The cost lands when a later card runs `sync` or a job through the runner: the app would say timed out while a child keeps writing.

**Closes when:** the card that first runs a long verb through the runner (the Sync card) ends the whole tree, by a process group made through `posix_spawn` or a `setsid` wrapper, sets a timeout per verb, and gives a job driver the grace it needs to stop at an item boundary, each with a test over a fake that leaves a child. Ledger only: no shipped caller pays it.
