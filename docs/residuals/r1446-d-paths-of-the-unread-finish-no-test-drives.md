---
title: Paths of R-1446's finish no test drives, and a fallback branch that kills nothing
found: at the review of #639, R-1446, rounds one and two, 2026-11-08.
issue: no
---

**The mechanism.** In `src/cratekit/sync/pair_cli.py`:

- `plan_pair` passes no target at all when only unread tracks moved and
  `_unread_moved` names none of them, the `else ()` branch. On a settled
  reading that cannot happen, since an order of the shared ids that changed
  with the readable ones held drops an unread id from the shared run; on a
  stop that sent nothing it can, when a readable track moved along the
  write's path. The review's round two mutated it to pass the whole target
  and killed nothing in `tests/test_sync_pair_settle.py`.
- `_readable_moved`'s branch for no settled reading is reached by its unit
  tests only, since `plan_pair` asks it only after `_moved_since_stop` read a
  reorder from a settled reading or the write sent nothing.
- Not driven, named by the review's round one: an unread release of a row
  whose other release is readable (an alias), a track readable when the
  reading settled and unread now, and on a stop that sent nothing any step
  of the write's path accepted as its partial state.
- A move of an unread track to the very front is not pinned by a dispatcher
  test.

**Measured cost.** None driven. In each the readable tracks are finished in
rekordbox's order and rekordbox keeps its own; what is at stake is where an
unread track is put on the account.

**Closes when:** each is driven by a dispatcher test or shown unreachable,
and the fallback branch is pinned or removed. Ledger only: an unread
track's place on the account, nothing in rekordbox.
