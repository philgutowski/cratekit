---
title: The mirror's apply plans the whole account again, so a first build pays its matching twice and a library write between the passes makes the decision stale
found: at sitting 42, 2026-10-15, the first live `crate organize --only mirror` (U147, #326).
issue: yes
---

**The mechanism.** `organize` plans the mirror from the library and the account,
matching every tree row `mirror_links` has not yet linked against the provider,
one or more calls per row, and shows the gate. The apply under `--run` plans
everything again, from the account and the provider, and applies only if the
second plan's digest equals the decided one. Nothing links a row until an apply
lands, so the first build's matching is paid twice by design, and any library
write between the two passes, a landing, a refresh, a split, turns the approved
plan stale (`decision-stale`) and starts the pair over.

**Measured cost.** The first attempt planned 23 folders in 7,548 s and 12,305
account requests at 0.25 s, the apply's pass cost the same again at 0.15 s,
then refused `decision-stale` because `favorites split` and `favorites backfill`
had run between the reads. The second attempt paid both passes again, 3,166 s
and 12,307 requests for the plan at 0.1 s and about the same for the apply's
pass, before the first folder was written. A refresh after the first build
plans in 2,001 s and 7,215 requests, so this is a first build cost, but it is
the one a person is waiting on, about two hours of it.

**Closes when:** the apply under `--run` rebuilds its plan from the matches the
gate's plan found, frozen on the run or recorded in `mirror_links` at plan time
(a link is a fact about a row and a provider track, not a write to the
account), asking the provider only about rows the frozen plan does not carry,
so the digest the gate showed is the digest the apply applies and the second
pass costs the listing alone. Earns an issue: it is a change to how an
organize run carries its plan from the gate to the apply, which every account
step shares.
