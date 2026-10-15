# U146 mutation tables, read

The author's table, not independent, measured by `scripts/mutate.py` on
`relay/325`, twenty five distinct guards in five batches. Four batches because
one batch of twenty five rows passes the ten minute ceiling on a foreground
command once a zero is promoted to the full suite; the fifth measures two rows
again. Row subsets were the unit's own suites: `tests/test_favorites_backfill.py`
for the backfill, its gather and the filing rule, and
`tests/test_intake_land_owned_hearts_native.py` for the landing's owned hearts.
Every batch: baseline green at 14,032 collected, null control 0 of 14,032, no
collect drift, every restore verified against `git show HEAD`.

| Batch | Head | Rows | Killed | Zero | Refused |
|---|---|---|---|---|---|
| `u146-a` | `fe9f199a` | 8 | 8 | 0 | 0 |
| `u146-b` | `a1543378` | 8 | 7 | 0 | 1 (B17) |
| `u146-c` | `a1543378` | 8 | 7 | 1 (N3) | 0 |
| `u146-d` | `a1543378` | 1 | 0 | 1 (B7) | 0 |
| `u146-e` | `2dd1d9b8` | 2 | 2 | 0 | 0 |

27 measured mutations over 25 distinct guards: **24 killed, 1 open, a
maintainer zero**.

- **B17, the month label read wrongly.** Refused in batch b, not measured:
  the row's old text was written in a TOML literal string with a doubled
  backslash, which a literal string keeps, so it matched nothing in the
  source. Written with one backslash in batch e and killed, 4 deaths.
- **N3, the owned hearts left out of the landing's digest.** Zero on the full
  suite in batch c. The test meant to hold it,
  `test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`,
  let the whole favourites plan fall away in its second act, so the digest
  moved whether or not the owned hearts were in it. A downloaded heart now
  lands beside the owned one, so only the owned hearts differ between the
  acts; killed in batch e, 1 death.
- **B7, a listed track with no identifier kept under the empty key.** Zero on
  the full suite, maintainer facing, one line: the gather's own
  `not heart.ref` check is the second layer over the same input, and a hearts
  job row with neither a ref nor an item id was not driven, since the queue
  refuses a provider row with no identifier.

Rows the author killed with one test each are the rule here rather than a
gap: B4, B5, B10, B12 to B16, A1, L4 and N3 are each held by the test written
for that guard. Every zero above is the author's to have missed or not, by
METHOD's measured gap between author and independent tables.

Considered and dropped below the cap: `native.single_rows_for`'s MATCHED test
(B13 reverts the whole lookup to the guessing one and is killed), the `known`
field carried on `OwnedHeart` (B10 measures the rule that reads it), the
backfill's empty ref check in the gather (B7's second layer), the landing's
`files to land` and the two keys `landing_facts` drops (a screen wording,
pinned by the AE4 test), and `Placed.said` (wording read by three verbs whose
tests assert its clauses).
