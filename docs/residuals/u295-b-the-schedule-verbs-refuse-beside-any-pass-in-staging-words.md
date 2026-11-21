---
title: crate schedule install and remove refuse beside any pass, a first install included, in words about staging
found: at the review of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** The schedule verbs take the staging lock with no `what=`, so beside a `crate label sync --go` or a pass by hand the refusal reads "another pass is staging downloads (...), so crate schedule install stages nothing until it has finished", and a first install with nothing to boot out waits as well. The other way round, a night refused beside the schedule verb is told another pass is staging downloads.

**Measured cost.** Driven at round two: exit 20, launchctl never asked, the refusal's words untrue for the schedule verb. The block ends with the pass and is retryable.

**Closes when:** the schedule verbs take the lock only when there is an agent to boot out, and both refusals name a schedule change rather than a download.
