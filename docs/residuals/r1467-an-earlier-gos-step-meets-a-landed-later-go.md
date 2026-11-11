---
title: The go a refusal names for an earlier download is refused beside a later go's download that already landed
found: at the review of #655, R-1467, 2026-11-11.
issue: no
---

**The mechanism.** U239's `_beside` refuses a run's own tail beside any go
job queued after it that is open or holds a downloaded track, whether or not
that later download has since landed. R-1467's refusal of a fresh go names
`crate --run RUN label sync --go` for an earlier go it can put files down to;
when a later go's download exists, that command refuses saying the folder
holds the later download, which may have landed long ago. Downloads from
before R-1467 that share the folder name each other this way, and only moving
files out lands them (landing two batches from one folder separately was out
of R-1467's scope).

**Measured cost.** Driven at the review's round two (`test_f2.py`): go A
finished by hand, its tracks moved out, go B landed with its proof, one stray
file. The fresh go named A's command; that command exited 42 with the false
sentence and no tail. The refusal's other step, land or move the stray file
out, works.

**Closes when:** `_beside` counts a later go's job only while it is open or
holds a track in the folder, or the step for a go named with no tracks of its
own present says it may refuse. Ledger only.
