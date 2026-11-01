---
title: label sync --next with some labels listed and some skipped still ends no_op
found: at the review of #417, R-1114, 2026-11-01.
issue: no
---

**The mechanism.** `label/sync_cli._next` refuses as `label-sync-unlisted`
only when every label it asked about was skipped. A run in which at least one
label was listed with nothing new and another could not be listed ends
`no_op` with exit 0, as the brief and the plan decided: the closing line names
only the listed labels and each skipped label keeps its `fail` line, so the
words are true, but the outcome is the one a run with nothing to ask carries.

**Measured cost.** Driven at the review: three labels, the second unlisted,
`crate label sync --next` exits 0, outcome `no_op`, the closing line "no label
listed has anything new to ask about: Alpha Works, Gamma Works" and Beta
Works's `fail` line. A script that reads only the outcome reads the run as
nothing to do while one label went unread; one that reads the checks does
not.

**Closes when:** a mixed run carries an outcome or a warning a script can read
as partial, without turning a routine provider hiccup on one label into a
failed run for every label that answered. Ledger only: the report names the
failure, so it is not a clean report, and nothing is lost or written.
