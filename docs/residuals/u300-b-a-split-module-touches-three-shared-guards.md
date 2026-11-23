---
title: Splitting a module needs one entry in three guards no area card owns, the scenario list, the layer ladder and the reports allowlist
found: at the build of #857, U300, 2026-11-22.
issue: no
---

**The mechanism.** U300 split `core/rb_writer.py`, `core/session.py` and
`core/restore.py`. Three guards outside the card's own files pin what the split
moves: `tests/test_behaviour_compare.py` names every shipped scenario, so the
card's ten new scenarios joined its list; `tests/test_layering.py` places a part
of a write-ranked core module only by a line of its own, so restore's three
parts were placed beside it; and `tests/modules/test_reports.py` asks every
writer its allowlist's closure reaches to be named, so the moved writers were
named under their parts. Each edit is the mechanism the guard's own message
gives, one entry per name, but each file belongs to another card's list
(the suite card #869 for the first two, #868 for the reports guard), and every
area card that adds a scenario or splits a module edits the same lists.

**Measured cost.** None to a person; a merge conflict between two area cards
in a list, which git resolves line by line.

**Closes when:** the suite card (#869) decides whether these three lists stay
hand-kept or are derived. Ledger only.
