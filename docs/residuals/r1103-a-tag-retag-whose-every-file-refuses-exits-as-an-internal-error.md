---
title: A tag retag whose every file refuses the write exits as an internal error
found: at the review of #411, R-1103, 2026-11-01.
issue: no
---

**The mechanism.** When every item of a job fails, the job engine leaves
through its own `no-evidence` cause, exit 1, and carries the last item's
cause inside it. A `crate tag retag` whose every selected file would not take
its genre therefore reports `failed (INTERNAL)`, the class a script reads as a
defect, over a refusal whose own class is PRECONDITION and whose cure is the
file's. This is the engine's rule for every job verb, present on `main`
before R-1103; R-266 records a related exit of the label jobs.

**Measured cost.** Driven at the review: two files, both refusing, through the
human answer: `tag.retag: failed (INTERNAL)` and then `caused by
tag-retag-unwritten:` naming the file and the genre it would not take. The
words are honest and the file is named; only the exit class is wrong for a
caller that branches on it.

**Closes when:** a job whose every item failed under one reason exits with
that reason's class, or the record says why the engine's class is right.
Ledger only: nothing is lost and the message is true.
