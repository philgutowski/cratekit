# R-318 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/169`. Subsets were derived by the driver: the
four test files importing `write/routing_pass.py`, and the two importing
`write/routing_cli.py`.

**`r318.md`**, 20 rows at `b867b53`, null control 0 of 9727, no collect drift,
every restore verified against `git show HEAD`. 17 killed, three zeros.

**`r318-b.md`**, the three zeros' rows measured again at `52882ac`, after
`f5e43ce` added or fixed the tests. All three killed.

23 rows in all, 20 distinct mutations and three re-measures, under the cap of
25. Nothing was dropped.

## The zeros

- **W2, the cap halved from 10 to 5.** Round one shows one kill, and it was
  the wrong one: the reserved code suite's at-risk pin, because 5 is below the
  range that pin counts. The cap test read `SKIPPED_NAMED` back from the module,
  so it followed the constant wherever it went, which is the X equals X shape
  METHOD names. The test now uses literal numbers, and `r318-b` measures the
  same mutation killed on the subset.
- **C7, the tree list not deduplicated.** No driven fixture declares one file
  into two playlists of one tree, which an additive sub-class does on a
  calibrated library. It bought a unit test on `_skipped_files`, and `r318-b`
  measures it killed.
- **N1, the no native tree answer without `skipped_files`.** Maintainer facing,
  the payload shape differing by branch. It bought one assertion, and `r318-b`
  measures it killed.
- **P5, a withdrawn placement's ids taken from the live match.** STILL ZERO,
  and a guard on existing code rather than on this unit's. Maintainer facing
  today, because nothing in `src` reads the ids on a withdrawn `Placed`:
  `route_pending` throws away the whole report `routing_pass.route` returns.
  That is the same shape one file over and is filed as R-641.
