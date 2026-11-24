---
title: Slice two's label suites now borrow five helpers from two test files another slice owns
found: at the build of #982, U333, 2026-11-24.
issue: no
---

**The mechanism.** To stop copying them, the trim of slice two (#982) made
three label suites import helpers from test files outside the slice:
`tests/test_label_genre.py` takes the `folder` and `silence` fixtures and
`warning_codes` from `tests/test_tag_workers.py`, `tests/test_label_judge.py`
takes `warning_codes` from it and `item_states` from
`tests/test_label_workers.py`, and `tests/test_label_offer_window.py` takes
`item_causes` from `tests/test_label_workers.py`. Each name was identical in
behaviour to the copy it replaced. Those two files belong to the later slices
building beside this one, whose brief keeps every name another file imports
as it stood on their base, which did not hold these imports yet.

**Measured cost.** None to a user. If a sibling slice renames or reshapes one
of the five names before merging this one, the three label suites fail to
import, and the sibling's own battery on the merged `main` shows it at once.
Not driven, since the siblings had not landed when this was filed.

**Closes when:** the four slices have all landed on `main` and its battery
collects the three label suites. Ledger only, maintainer facing.
