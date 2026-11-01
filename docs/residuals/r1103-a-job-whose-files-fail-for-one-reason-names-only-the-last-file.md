---
title: A job whose files fail for one reason names only the last of them
found: at the review of #411, R-1103, 2026-11-01.
issue: no
---

**The mechanism.** When several items of a job fail permanently under the same
reason, the job's own cause takes that reason and carries only the last failed
item's cause as its inner one, so the refusal a person reads names one file.
The others are on their item rows. R-391 records the mixed reasons case of the
same choice; this is the one reason case, which R-1103 made reachable from
`crate tag retag` with `tag-retag-unwritten`, and U178's `tag-folder-unwritten`
has the same shape (not driven there).

**Measured cost.** Driven at the review: `tag retag` over three files with the
first and the last refusing the write exits 30 under `tag-retag-unwritten`,
the detail says two failed, and the message and the human answer name only
the last file. Nothing said is false, the counts are right, and every item's
cause is readable with `crate job show`; a person fixing the one file named
and running again meets the second one then.

**Closes when:** a job's cause lists every failed item's file when they share
a reason, or names how to see them. Ledger only: nothing is lost or false, the
counts are honest and the remedy already says to inspect each item's cause.
