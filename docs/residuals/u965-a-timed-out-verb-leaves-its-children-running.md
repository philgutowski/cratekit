---
title: The app's runner signals a timed out verb's own process and not its children, reports a verb a SIGKILL has not yet ended as ended, and gives a job three seconds to stop cleanly
found: at the reviews of #1084, U965, 2026-11-25.
issue: no
---

**The mechanism.** `CrateRunner.runBlocking` in `app/Sources/CrateEngine/CrateRunner.swift` sends SIGTERM to crate's own pid at the timeout, then SIGKILL after `terminationGrace`, three seconds, and signals no other process. A child crate started (rclone, ffmpeg, a pool worker) is not signalled and keeps running after the app reports `timedOut`. swift-corelibs-foundation starts the child in a process group of its own (`POSIX_SPAWN_SETPGROUP`, its commit faef552, which says this matches Darwin), so signalling the group, `kill(-pid, ...)`, may be enough; whether Apple's Foundation does the same was not driven. After the SIGKILL the wait is bounded by the same grace, so a verb a SIGKILL has not ended within it (one held in uninterruptible I/O on a hung volume) is reported as `timedOut`, whose comment says ended. A job driver that stops cleanly on SIGTERM at an item boundary may need longer than three seconds, and every call defaults to a 60 second timeout whatever the verb.

**Measured cost.** On Linux the review killed only a fake shell's pid and its `sleep` child stayed in the group, holding the pipe 0.71 seconds; on the App workflow `testAVerbThatIgnoresTerminateIsKilled` takes about 4.2 seconds, 0.9 past its timeout and grace, the orphaned `sleep 1` holding the pipe. The unkillable case was not driven: no test environment holds a process SIGKILL cannot end. No shipped caller runs a long verb, since the app in U965 only shows the crate setup state, so nobody pays today; the cost lands when a later card runs `sync` or a job through the runner.

**Closes when:** the card that first runs a long verb through the runner (the Sync card) ends the whole group, reports a verb still running after the kill as still running, sets a timeout per verb, and gives a job driver the grace it needs to stop at an item boundary, each with a test over a fake that leaves a child. Ledger only: no shipped caller pays it.
