---
title: The finished job filter of sync removed's recorded contents kills no test
found: at the review of #373, U287, round two, 2026-11-15.
issue: no
---

**The mechanism.** `recorded_contents` reads only the jobs of a gone playlist that SUCCEEDED. No test puts a job of a gone playlist in any other state in the store, so dropping the filter leaves every test green (round two's N6).

**Measured cost.** None to a person: an unfinished job's reports are a subset of its tracks, and a refusal reading one is caught and reads the playlist as not whole. Maintainer facing.

**Closes when:** a test holds a gone playlist whose only job was cancelled to not read whole, and one with a cancelled and a finished job to the finished one's contents. Ledger only.
