---
title: A genre playlist whose listing fails while the edit rule reads it, and reads at the mirror's own plan, lets the mirror add a moved track back for one run
found: at the review of #489, U201, round one, 2026-11-05.
issue: no
---

**The mechanism.** `account_mirror._read_edits` reads a genre playlist whose
listing fails as its snapshot and short, so it carries no edit of its own, and
caches no listing; `mirror.plan` then reads the listing again. A transient
failure that succeeds on the second read gives the mirror a listing the edit
rule never decided over, so a track a person moved off that playlist is not
held there and the mirror adds it back for one run, converging on the next.

**Measured cost.** Reasoned from the two functions by the round one reviewer,
not driven: reachability unmeasured.

**Closes when:** the mirror plans a playlist the edit rule could not read from
that same failure, refused or held, rather than reading it again.
