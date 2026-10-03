# R-837 mutation notes

The author's table, not an independent one: every zero reads as "the author
could not kill it" (METHOD, Verification is the author's).

Two batches, 25 rows, the unit's light cap.

- `r837-a`: 17 rows over the engine (`modules/outbound/sets.py`), the
  ledger's set records and the sweep hand off. Valid, null control zero,
  every row's restore verified against `git show HEAD:`. 15 killed. Two
  user facing zeros, both promoted to the full suite:
  - A3, a track already on the set playlist that this library never wrote
    was planned as an add again. No test put a track on the playlist by
    hand.
  - A9, a recorded year folder the account no longer lists was reused. No
    test deleted a year folder.
  Each was given a test in the next commit rather than a composite.
- `r837-b`: 8 rows over the set verbs' four match routes, the R-850 warning,
  the archive's name spelling, and A3 and A9 measured again as A3r and A9r.
  Valid, null control zero. 8 of 8 killed, A3r and A9r included.

Dropped below the cap, logged in `r837-b-rows.toml`: B7, the archive's proof
check, which `label mark` shares and a test drives, and B8, the mark record's
lock asked before the move, maintainer facing.

Two of the four match routes, the ISRC and an answer accepted in review, had
no test when the rows were written. Both were given one before batch a ran,
so B2 and B3 measure tests rather than read as zeros.
