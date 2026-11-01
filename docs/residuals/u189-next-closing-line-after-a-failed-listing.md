---
title: label sync --next ends with "no label has anything new" when a label's listing failed
found: at the review of #400, U189, 2026-11-01.
issue: yes
---

**The mechanism.** `label/sync_cli._next` walks the followed labels and, when
none yields a question, appends an `ok` check, "no label has anything new to
ask about", and returns outcome `no_op` with exit 0. A label whose catalogue
could not be listed is skipped with its own `fail` check, and the closing line
is appended all the same, so a run in which every listing failed ends by saying
every label has nothing new. U189's single label form, `--next --label NAME`,
leaves the closing line out and reports the failure as its one check, but keeps
the `no_op` outcome the walk uses, and the guide now says to read the line, not
only the exit status.

**Measured cost.** Driven at the review of U189: two labels followed, the
provider bound for neither, `crate label sync --next` exits 0, outcome
`no_op`, two `fail` lines and the `ok` closing line. An agent or a script that
reads the exit status or the outcome reads a failed listing as nothing new,
and the closing line says so in words. The `fail` lines are in the report, so
it is not a clean report, but its last line is false.

**Closes when:** the closing line names only the labels that were listed and
found nothing, or is left out when any label was skipped, and a run whose every
label was skipped is not `no_op`. Earns an issue: the product says something
false on a shipped verb.
