---
title: A replay row names a test a later unit renamed away, and its batch then measures nothing
found: at the kill set replay of #984, U335, 2026-11-24.
issue: no
---

**The mechanism.** `killset.py`'s `tests_of` keeps a subset entry whose file exists, without asking whether its test does. Rows u135 A8 and A12 name `test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set` and `test_inspiration_join_stays_pinned_beside_the_inbox_join` in `tests/test_u135_set_inbox_join.py`, which no longer define them, so the subset collects nothing and `mutate.py` refuses the whole batch with NOTHING MEASURED. The load calls (`load_spec`, `load_mapped`, `refuse_unrecorded_sources`) and a collect of the union of a batch's subsets both pass over it.

**Measured cost.** One helper container's run of before batch five, about twenty minutes, before the two rows were pointed at their file and the batch restarted.

**Closes when:** `killset.py rows` drops or widens to its file a subset entry whose node id does not collect, or the driver's load check collects each row's subset. Ledger only: maintainer facing.
