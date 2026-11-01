---
title: An empty lossy marker under the permissive policy is declined as a refusal for good, though the cure is one configuration value
found: at the review of #350, U169, 2026-11-01.
issue: no
---

**The mechanism.** Under `allow_lossy_marked` with `naming.lossy_marker` empty, `acquire.cli.marked_name` refuses a lossy landing as `lossy-refused`, not retryable. Since U169 `acquire.cli.handle` declines every non retryable cause in the `REFUSED_BY_POLICY` class, so the item is skipped, the job succeeds, and the `acquire-refused` warning calls the track refused for good. The warning's message does name the missing marker text.

**Measured cost.** Driven by the review with the fake adapter: exit 0, the item skipped, the warning naming the marker. On the base the item failed non retryable and `job resume` refused the job just the same, so no route back was lost; the cost is the words "for good" over a configuration omission.

**Closes when:** the marker refusal says the configuration lacks the marker text in its own reason, outside the policy class, or the warning words a configuration cure apart from a refusal. Ledger only, a wording.
