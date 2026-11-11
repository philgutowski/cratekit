---
title: The review list grouped by label shows a label's own releases past the window and the unchecked ones as one beyond figure
found: at the review of #646, U238, 2026-11-10.
issue: no
---

**The mechanism.** `review.record_round` stores one `beyond` per label and
run, which since U238 is the label's own releases past the window plus
those with no copyright line. `crate review list --queue label-release
--group-by label` and `--group-by run` print it whole, so the part that is
only a bound is not told from the part that is a count, while `label
sync` says "7 more of the label's release(s) past this run's window, and
up to 2 more not yet checked" for the same listing. A round recorded by an
earlier build also stays as it was until the label next has a question,
since `_question_for` records a round only when it builds one.

**Measured cost.** Driven by round one's review: after a question of
(9, 2) the grouped row read `beyond: 9`; a hand recorded round of 17 stayed
17 beside a nothing new line saying 7 and up to 2. The figure is defined
as the sum in `CONCEPTS.md` and is not called the label's releases, so
nothing false is said.

**Closes when:** the `offer_rounds` table gains an unchecked column
(additive, as the table itself was) and the grouped list says the two
parts as `label sync` does, and a nothing new listing records its round
too. Ledger only.
