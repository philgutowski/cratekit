# U78 mutation tables, read

Four tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/123`. Every zero row in this record means the
author could not kill it, not that nobody could.

**`u78-a.md`**, 7 rows over `intake/missing_cli.py`'s ISRC resolution at
`4ee1a9d`, subset `tests/test_intake_missing_isrc.py` and
`tests/test_intake_missing.py` named explicitly, null control 0 of 8380, no
collect drift, every restore verified against `git show HEAD`. 6 killed, 1 zero
promoted to the full suite.

**`u78-b.md`**, 6 rows over the same file's listing step, five new guards and
one existing sample (reports compared by identifier), same subset, null control
0 of 8380. 4 killed, 2 zeros promoted to the full suite.

**`u78-c.md`**, 9 rows over `acquire/listdoc.py`'s text list writer and
`label/tidal_catalogue.py`'s `tracks_for_isrc`, plus one existing listdoc
sample (the emitter reading each listed row back), null control 0 of 8380. All
9 killed.

**`u78-d.md`**, the three zero rows measured again at `c821dfc` after a test
was added for each, null control 0 of 8383. All 3 killed.

25 rows in all, 22 distinct mutations and 3 re-measures, at the cap. Two more
were considered and logged as dropped in `u78-c-rows.toml`: the adapter's
`or ()` over a `None` answer, which the installed client never returns, and the
`--out` check moving after the provider reads, which costs lookups on a refused
run and never a wrong file.

## The three zeros, and what each bought

- **A4, a product refusal from the catalogue relabelled.** Without the
  `except CratekitError: raise`, a refusal the catalogue raised in the product's
  own words would be reported as `unavailable-transient`, and a person whose
  session expired would be told to wait. No shipped adapter raises a
  `CratekitError` from `tracks_for_isrc` today (one candidate driven, the
  Tidal adapter, and it raises the client's own classes), so the test uses a
  fake that does. Killed on re-measure.
- **B2, missing tracks with nothing written.** Every missing row handed on and
  none writable as a line left no file at all, and the verb answered NO_OP, a
  set the library already held to a person and to a script. Driven with one
  recognised track whose artist carries the line separator. Killed on
  re-measure.
- **B4, a skip-failed run whose finished jobs only handed tracks on.** The
  run was refused as "nothing is missing" although a text list was written.
  Driven through a real run with one failed job. Killed on re-measure.
