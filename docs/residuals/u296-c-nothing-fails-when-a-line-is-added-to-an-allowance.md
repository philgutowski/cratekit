---
title: An allowance only shrinks by rule, and nothing fails when a line is added to one
found: while building #853, U296, 2026-11-21.
issue: no
---

**The mechanism.** The files under `tests/ratchets/duplication/` and
`tests/ratchets/imports/` hold what each package may still keep, and the two
checks fail on anything beyond them. Whether a line may be added is a rule in
the files' own headers, in `docs/DEVELOPING.md` and in each failure's
message. A branch that copies a block and adds its windows to the allowance
in the same commit passes the suite. `refactor_measure.py prune` can add
none, but a hand edit can. The same holds for `CORE_INTERFACE`, whose length
is capped at 25 but whose members can be swapped, and for `CORE_NAMES_CEILING`.

**Measured cost.** Driven by the review: a six line copy planted in
`skills/cli.py` and `vocals/cli.py` with its digest appended to one allowance
and a new file made for the other passed both suites, and `table` exited 0
over 438 lines. A maintainer facing guard that depends on the
review reading the diff of `tests/ratchets/`: a line added there is plain in
a pull request, one `+` line per window or crossing. A check that compares
the allowance with the base commit needs the base's history, which a test
cannot assume, so it belongs in `board.py closing` or in CI's scan job, and
both are outside this card.

**Closes when:** the pull request check refuses a diff that adds a line under
`tests/ratchets/duplication/` or `tests/ratchets/imports/`, or the final
audit of U290 reads the history of those files and finds no line added.
Ledger only.
