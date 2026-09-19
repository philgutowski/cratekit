# U91 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/136`.

**`u91.md`**, 22 rows at `8d8c6b1`, null control 0 of 8035, no collect drift,
every restore verified against `git show HEAD`. 19 killed on the first run.

**`u91-b.md`**, 2 rows at `608396e`, null control 0 of 8037, no collect drift.
Both killed.

24 rows in all, under the cap of 25. One more was considered and logged as
dropped in `u91-rows.toml`: U2, reading keys off folders as well as playlists,
is equivalent, because a folder's byte range holds only its descendants' keys
and the playlists already put them in a set.

## The three zeros of the first table

- **U6, the writer left unscoped.** User facing. With `tree=None` the creating
  writer searches the whole playlist section for the genre folder, and no
  fixture held a folder of that name outside the routing tree, so every
  placement still landed. A namesake Tech House in the intake folder, ahead
  of the tree, now takes the created High under the mutation.
  `test_a_namesake_genre_folder_outside_the_routing_tree_takes_nothing` was
  written for it, and `u91-b` measures 1 kill.
- **R3, the negative offset check in `_break_before`.** Maintainer facing and
  equivalent: a slice that starts before the buffer is shorter than a CRLF and
  already answers None. The check was removed rather than tested.
- **P1, the existing guard sample in `plan_export`.** User facing. Handing an
  intake key with no collection row to `_decide` anyway leaves it unrouted
  either way, and only adds a second, false `track-file-unreadable` warning.
  The existing test asserted the right code was present, not that it was the
  only one. `test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent`
  pins the list, and `u91-b` measures 1 kill.

Every zero was read as "the author could not kill it" until the second table,
and then it was killed.
