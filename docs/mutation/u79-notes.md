# U79 mutation tables, read

**Verdict: 25 rows at the cap, 25 killed on the first pass, no zero.** The
author's table and not an independent one, so every row reads as "the author
killed it", and an independent table would be expected to find rows this one
did not think of. Driver `scripts/mutate.py`, rows as data in `u79-a-rows.toml`,
`u79-b-rows.toml` and `u79-c-rows.toml`, run one at a time in the foreground,
each under the tool ceiling, with `PYTHONDONTWRITEBYTECODE=1`. Every row's
`head_verified` is true and `git status` showed no source change after each run.

| Table | Rows | Killed | Subject |
|---|---|---|---|
| `u79-a.md` | 8 | 8 | `candidates.sole_exact`, the five conditions and the page bound both ways, and the version inside the exact test |
| `u79-b.md` | 8 | 8 | the floor halved, exact before score, an option with no identifier, the three answers `settled` reads, the identity, an open item searched again |
| `u79-c.md` | 9 | 9 | the verb: the absent music folder, an owned row, an accepted candidate the library holds, nothing found read as nothing to do, a foreign ref, the origin of a row named by ISRC, the fixed name, the asked outcome, and the adapter's shape check |

Deaths were confirmed on the subset of test files that import the mutated
module: `tests/test_intake_missing_search.py` for `intake/candidates.py`, that
file plus `tests/test_intake_missing.py` and `tests/test_intake_missing_isrc.py`
for `intake/missing_cli.py`, and `tests/test_label_tidal_catalogue.py` for the
adapter. The collected count was 50, 103 and 132 on every row of its group.
No row needed a full suite run, since none was a zero.

Three guards were given a test BEFORE the table, because the author could see
they would be zeros: the identifier condition of `sole_exact` alone (two exact
hits that both lack an id are one distinct value), an accepted option whose
detail names another track, and the outcome of a run that only asked a
question. A4, B6 and C8 are those rows.

## Dropped at the cap, and why each ranked below it

1. The floor removed outright. B1 halves it over the same line and is the
   stricter row.
2. The blank query guard in the adapter. Maintainer facing: the verb never
   sends a blank artist and title, since the list reader refuses such a row.
3. The offer limit's truncation removed. Pinned by
   `test_more_candidates_than_the_screen_holds_are_truncated_and_counted`, and
   a longer screen downloads nothing.
4. The null version kept in the query. Pinned by the original mix test, and a
   worse query is R-488's subject, not a wrong pick.
5. The same line twice searched twice. Pinned by its own test, and the cost is
   one spare search.
6. `review.find` re-raising anything but an unknown item. Pinned by
   `test_a_store_that_cannot_be_read_is_not_read_as_nobody_was_asked`.
7. The write helper's `OSError` arm. Added after the tables ran, pinned by two
   tests, and it changes what a refusal says and not what is written.
