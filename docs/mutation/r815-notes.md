# R-815 mutation tables, read

Three tables, the author's and not independent, measured by
`scripts/mutate.py` on `relay/240` after both of the review's fix rounds, each
in the foreground and waited on. Every null control killed 0 of the full
suite, 11,679 collected against 11,679, every row's collected count equalled
its subset's baseline, every row's `head_verified` is true, and after each
table `git status` showed the table's own two files and nothing else.

| Table | Rows | Killed | Zero | Wall clock |
|---|---|---|---|---|
| `r815-a.md`, the store's guards and the two bounds | 8 | 8 | 0 | 384 s |
| `r815-b.md`, the sweep, `label held`, and when the run stops | 8 | 8 | 0 | 348 s |
| `r815-c.md`, the worker's branches and both exits | 9 | 9 | 0 | 369 s |

25 rows, the cap, one pass. No zero, so no composite was owed.

Three tables and not one, on R-821's arithmetic: a Relay session runs the
driver in the foreground under a 600 second ceiling, and one table of 25 with
a single zero promoted passes it and leaves a mutation in the source. Three
of eight or nine left room for two zeros each. The split cost two extra
baselines, about nine minutes.

Subsets, named on every row and not derived. Rows that mutate
`core/review.py`, `label/gate.py`, `label/catalogue.py`, `label/sweep.py` and
`label/held_cli.py` ran `tests/test_label_judge.py` and
`tests/test_label_genre_gate.py`, 213 collected, and the ordinal row added
`tests/test_review_queue.py`, 375. Rows that mutate `label/judge_cli.py` ran
`tests/test_label_judge.py`, 75.

## What the cap dropped, and why each ranked below it

Eleven candidate rows were written down and not measured. Each is in
`r815-c`'s `dropped` list with its reason.

- The delete's own verdict guard in `withhold`. The transaction read the
  verdict two statements earlier and holds the write lock, so no input
  reaches it. A maintainer facing guard covered by another guard, and said
  so here and not measured.
- The sibling of a measured row, three times: the filing run carried across
  a refresh, the word `withhold` writes, and the hold written under the
  label's current identifier.
- Five guards each pinned by a test that names it: a stale hold dropped
  beside a passed release, the verb driving only its own job, an item judged
  only on the release it addresses, nothing pending queueing nothing, and
  the taxonomy read before queueing.
- `judged` as held plus passed, which every count in the file asserts.
- The human readable lines, a display over the payload the other rows
  measure.

## What no row measures

The registry entry and the handler table. They are declarations, and
`tests/test_handlers.py` and `tests/test_cli_contract.py` derive their
populations from the registry.

`label approved`. Its two changed lines read a release's record through the
gate module's shared functions and change no verdict, and its own suite,
`tests/test_label_approved.py` and section 6 of
`tests/test_label_genre_gate.py`, passed unchanged.

The live queue. Every kill here is against a fake provider and a fake
catalogue, R-827.
