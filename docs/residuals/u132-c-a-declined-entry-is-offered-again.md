---
title: A class or bucket a person left out on purpose is offered by every upgrade
found: at the build of #300, U132, 2026-10-10.
issue: no
---

**The mechanism.** The upgrade matches entries by id and has no way to decline
one and take the rest, and no record of an entry the person removed. A copy
that deleted Candy, or a bucket the person does not want, gets it back on the
next approved upgrade, and doctor's `taxonomy.schema` names it as missing on
every run.

**Measured cost.** The gate lists every addition by id, so nothing is added
unseen, and the INFO line is not a refusal. What a person pays is aborting an
upgrade they otherwise want, or deleting the entry again by hand afterwards.
Not driven with a person's copy.

**Closes when:** the copy can record entries it declines, read by the planner
and by doctor, or the verb takes the entries to add by id. Ledger only.
