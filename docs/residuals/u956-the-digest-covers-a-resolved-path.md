---
title: The adoption digest now covers each outside row's resolved path, and moved for every plan when U956 landed
found: at the review of #1020, U956, 2026-11-23.
issue: no
---

**The mechanism.** `AdoptionPlan.digest` covers `outside_root`, each row's
content id, recorded location and resolved path, so the gate's named rows and
its digest cannot differ. The resolved path depends on a prefix rule's target,
so two machines whose rules map the same rows to different folders digest
differently though the library and the plan's routing are the same. And the
digest's new key moved every plan's digest, outside rows or none.

**Measured cost.** Driven by the round one reviewer: the same rows with a rule
target of `Sampler` and `SamplerCopy` digest `98c16f23e2379acf` and
`b0bb8f1b9af6ea9c`; one fixture with no outside row digests `f85ac2c07ba6d4c0`
on the base and `f71f627d2beadd60` on the branch. Not driven: a job approved on
the previous build and resumed on this one, which refuses `decision-stale` and
asks for the run again, and a rehearsal whose copy resolves the rule
elsewhere; the standing recipe keeps the root and the rules, so a rehearsal's
digest and the live one stay equal.

**Closes when:** the digest covers the outside rows by content id and recorded
location only, if a sitting shows a rehearsal digest differing for this
reason. Ledger only.
