---
title: A first line that opens with a known heading word and then contradicts it moves a held card to that heading's state
found: at the Fable review of #493, U203, 2026-11-05.
issue: no
---

**The mechanism.** `comment_heading` in `scripts/board.py` reads the opening
emphasised span, or the text up to the first colon, comma or sentence end, as
the heading. So a session comment whose first line is
`**Withdrawn**? No, I still hold this card` reads `withdrawn` and releases the
card as ready, `Needs the machine? No, it does not.` sets it aside, and
`Landed? No, CI is red.` reads landed-open. Before U203 these three read as a
hold, though the same class already existed for a colon or a comma
(`**Withdrawn**, no` read ready on `main`): U203 widens its surface.

**Measured cost.** Driven through `cloud_state` by the review: a held card
offered to a second session, or a card retired until a hand edit. The producer
was not driven: of the 1,126 comments on the repository on 2026-11-05 and every
template in the cloud skill, none opens this way. Reachability unmeasured.

**Closes when:** the heading is read only when the first line is the heading
alone or the heading followed by a colon, or the skill's comment forms put the
heading on a line of its own and the reader refuses a first line that carries
more. Ledger only: maintainer facing.
