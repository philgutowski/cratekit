---
title: The twins backfill keeps a left playlist's provider words out of its digest on a producer nobody drove
found: at the review of #507, U213, 2026-11-05.
issue: no
---

**The mechanism.** `crate sync twins` leaves a playlist whose listing is
refused, with the provider's message as its reason. U213's round one drove a
fixture whose message varied per call and found the approved run refusing
`decision-stale`, since the reason rode in `Backfill.digest`; the fix puts
the refusal's reason code in the digest (`Twin.refused`) and keeps the words
for the gate.

**Measured cost.** None on a real producer: a real `requests` connection
failure run twice gave identical words, and the provider client carries no
request id in its errors. Round two read five other plans that carry a
refusal's message (prune, pair, the mirror's downloads, account playlists,
inspiration) and none compares a message that can move between the ask and
the write; inspiration holds one in its digest but never lists the account
again before the write.

**Closes when:** a provider error whose text varies between calls is seen
live, at which point every plan carrying a refusal's message in its digest
takes the reason code instead. Ledger only.
