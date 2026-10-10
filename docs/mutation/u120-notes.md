# U120 mutation tables, read

Two tables, the author's and not independent, measured by `scripts/mutate.py`
on `fable/277-heart-favourites-sync-lands`. The row subsets were the unit's
own suites: `tests/test_favorites_placement.py` for the engine and the quarter
rule, `tests/test_intake_land_hearts_native.py` for the landing, the claims
and the plan, `tests/test_favorites_backfill.py` for the backfill, and
`tests/intake/test_workers.py` for the frozen date.

**A first launch was invalid and is not a table.** Its null control killed
one test, `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`,
which this unit never touches and which passes three times alone. The #278
battery was running on the same machine at the time, load average over nine,
and the driver was launched again once it had finished. The invalid output is
not kept in the repository.

**`u120.md`**, 25 rows at `9d8a948`, null control 0 of 13,183, no collect
drift, every restore verified against `git show HEAD`. 21 killed, 4 zero,
each promoted to the full suite and still zero.

**`u120-b.md`**, 3 rows at `952830a`: three of the four zeros measured again
against the tests they bought. Null control 0 of 13,186. All 3 killed.

25 distinct mutations in all, under the cap of 25: **24 killed, 1 equivalent on
this binding** (P3, below).

## The first table's zeros

- **P3, `_under` compares the playlist root as an identifier.** Equivalent
  on this binding: pyrekordbox writes the root sentinel `root` into
  `ParentID`, and the mutant compares `held == parent_id` where both read
  `root`, so a source at the root still sees its neighbours. The sentinel set
  exists for the other spellings a database may carry (`""`, `"0"`, `None`),
  which no fixture of this suite writes. Left as an equivalent mutant on this
  binding rather than a test that forges a sentinel the binding never writes.
- **A1, an owned heart counts as carried.** Shadowed by the path rule: the
  suite's owned heart sat under the source system's deep folder, so the path
  rule excluded it whether or not the state rule did. The second pass test
  lands an owned heart's file in a batch folder first, where only the state
  rule stands between it and All Favorites.
- **B1, a heart's file anywhere counts as landed.** Shadowed by the row
  lookup: the suite's deep file had no content row, so `content_ids_for`
  dropped it before the path rule was asked. The second pass test gives the
  deep file a row through the binding.
- **B4, a plan whose digest moved is written anyway.** Shadowed by the gate,
  U119's lesson in a new place: the verb plans again on the acting drive and
  the gate refuses the moved digest before the write's own check runs. The
  second pass test calls the write with the approved plan and no gate in
  front of it.
