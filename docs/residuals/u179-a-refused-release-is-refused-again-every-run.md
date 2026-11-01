---
title: A Bandcamp release the fetch refused for good is planned and refused again by every later sync bandcamp
found: at the second Fable review of #360, U179, 2026-11-01.
issue: no
---

**The mechanism.** `acquire bandcamp-fetch` records a purchase only once it is fetched (U176), so a release refused for good, a lossy only offer under the strict policy, stays `new` on every plan. Each `crate sync bandcamp` therefore queues a fetch that fails the same way, and names the release as refused again.

**Measured cost.** Driven by the second review with an open fetch parked and the account then offering only MP3: two fetches in one run, one refusal named once since 75205b9, and the same refusal on every later run. A queue row and two account requests per run, and a warning a person learns to read past.

**Closes when:** a refusal for good is recorded beside the fetched record and the plan shows it as refused rather than new, until the policy or the offer changes. U176's rule rather than this unit's; ledger only.
