---
title: The approximate offer's reference test restates the title rule it checks, so it catches drift and not a wrong rule
found: at the review of #830, U286, 2026-11-13.
issue: no
---

**The mechanism.** `test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped`
in `tests/test_match_states.py` builds its expected offer from the shipped
scorer and a `passes` predicate written in the test, which states the same
rule `_title_resembles` states and reads the module's own floor.

**Measured cost.** None to a person. It proves the filter, its order and the
cap against the shipped scorer, and that a row losing no hit is offered the
shipped five exactly, but a wrong rule written the same way in both places
passes it. The rule itself is held by the named pairs and the floor's
neighbours, which are computed, and the mutation table.

**Closes when:** ledger only. A maintainer reading the test is told so here.
