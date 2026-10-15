# U145 mutation tables, read

Two tables, the author's and not independent, measured by `scripts/mutate.py`
on `relay/324`. The row subsets were the unit's own suites:
`tests/test_favorites_split.py` for the split, its verb and its confinement
rule, `tests/test_favorites_placement.py` and `tests/test_favorites_backfill.py`
for the month rule and the placement, `tests/test_intake_land_hearts_native.py`
for the landing given a pass.

**`u145.md`**, 25 rows at `b0dc93e5`, null control 0 of 14,013, no collect
drift, every restore verified against `git show HEAD`. 24 killed, 1 zero,
promoted to the full suite and still zero. The first launch was stopped by the
harness at its time limit partway through S9 and left that row's mutation in
`src/cratekit/favorites/split.py`; the file was restored from `git show HEAD`
and checked equal to it, and the driver was launched again with `--resume`,
which reused the twelve rows already measured and measured the rest.

**`u145-s2.md`**, 1 row at `a222a600`: the zero, S2, measured again against
the test it bought. Null control 0 of 14,014. Killed, 1 death.

26 measured mutations over 25 distinct guards: **25 killed, 0 open**.

- **S2, the quarter reader counting a membership rekordbox marked removed as a
  member.** Zero on the full suite in the first table: no test held a quarter
  with a removed row. A track taken out of a quarter by hand would have joined
  a month. Pinned by
  `test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month` and killed in
  the second table.

Rows the author killed with one test each are the rule here rather than a
weakness: the split's guards are each driven by one scenario of the brief,
and a row that dies on one named test is a guard that test names.

Dropped below the cap, and why, is in the header of `u145-rows.toml`.
