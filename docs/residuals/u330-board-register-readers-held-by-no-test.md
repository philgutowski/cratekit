---
title: board.py's register readers and near miss notes are held by almost no test, so a broken reader lets a closing trailer through on a green suite
found: at the reviews of #979, U330, 2026-11-23.
issue: no
---

**The mechanism.** `pending_units`, `planned_units`, `_unit` and `_near_misses` in `scripts/board.py` decide which unit a register still owes a module, which is what `board.py closing` refuses a trailer on. `tests/_pending.py` holds no entry today (`EXPECTED_PENDING` is empty) and every closing test replaces `owed_by_unit` with a lambda, so the parse never sees a register entry from a test. Review round one drove 21 mutations of the lines U330 rewrote through the eight board test files: 5 killed on the head, and the 17 base equivalents show the same survivors, so this predates U330. Round two emptied `pending_units`' loop on the head and the full suite gave 0 deaths beyond the clean head. U330's own table measures the same, its row `A1_annotated_register_unread` among the zeros.

**Measured cost.** None today, since no register entry exists for a broken reader to drop. The day a unit next registers a pending module, a reader that misses it lets `closing` pass a trailer that closes a unit still owed work, and the suite stays green. Maintainer facing.

**Closes when:** a test drives `pending_units` and `planned_units` on a synthetic register in each shape (annotated and plain `PENDING`, a constant through a name, a key with a suffix, a `path:` key, a present package), and `closing` end to end on it without the lambda, killing the rows above. Ledger only; the test slice cards #981 to #984 own these files now.
