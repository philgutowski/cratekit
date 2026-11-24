---
title: The suite is 10 percent faster than at ff8e5ec on one container, not 30, since the rest of its time is product work and the mutation tables every whole tree read pays for
found: at the build of #985, U336, 2026-11-24.
issue: no
---

**The mechanism.** Point 5 of #847 (U290) asks the suite to run at least 30 percent faster than at `ff8e5ec`. Timed three times each, interleaved, on one four core container with nothing else running, `ff8e5ec` read 455.57, 444.50 and 447.93 seconds (median 447.93) and U336's branch at `6cfc857e` 410.04, 390.10 and 402.02 (median 402.02), a ratio of 0.898: 10.3 percent faster, where the bar is 313.55 seconds. A profile of the base `50022274` places the rest: the mutation tables under `docs/mutation` grew from 30 MB at `ff8e5ec` to 223 MB and every test reading every tracked file pays for them (the secret scan's reference proof, about 89 seconds, the repository scan in `tests/test_portability.py`, about 25); the crate parser is built 12,624 times a run, once per verb a test drives (about 86 core seconds after U336, 162 before); the collector takes 22 to 50 seconds a worker; and the workers wait on `fsync`, sqlite and subprocesses for about 15 percent of the cores' time. The suite also runs 2,000 more tests than at `ff8e5ec`. The test side levers that keep every guard are taken: U326's collector thresholds and walks, U312's parse sharing and walks, U336's argparse lookups and pin sweeps.

**Measured cost.** Maintainer facing: the epic's time bar is not met. No verb is affected.

**Closes when:** Phillip chooses one of the remaining levers, each a decision rather than a tuning, asked on #985: make a verb's subparser only when it is chosen (a change to `src/cratekit/cli`, about 25 seconds here), keep the battery's temporary files in memory or skip `fsync` (#702), keep the replay tables out of the tracked text the scans read, or rescope the bar. Ledger only.
