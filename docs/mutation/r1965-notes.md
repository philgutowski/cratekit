# Mutation table r1965: notes

**The baseline.** `scripts/cloud_battery.py compare` on `ac589d53` and again on
`9c576cc0` read `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`
as newly failing, so the driver refused both batches on the battery's red
verdict. The branch does not touch that file. Run alone it failed on the base
`6001888` (once, in a worktree) and on `ac589d53` (three of three), a fresh
file under `/tmp` and `/var/tmp` getting inode 680,159 and 658,878, under the
2,000,000 bound the test asserts, the trap
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`
records. The baseline was measured again on `origin/main` at `99e0cbc0`, where
it passed in the full run. A scratch copy of the baseline file with the id
added by hand was not used. The table was then measured with
`--measure-baseline`: the driver's own full baseline was green, 22,945
collected, and the null control killed 0.

**The two zeros**, both user facing, are killed by tests added after the
measurement, each kill checked by hand on the same tree (one run of
`tests/test_tag_set_move.py`, 27 collected, the mutation applied by hand and
restored):

- `R08_alongside_no_folder` (a place beside the band names no folder): killed
  by `test_a_folder_holding_the_track_only_beside_the_band_still_reads_its_other_playlists`,
  a folder holding the track only through Favorites and Candy, where the
  folder is known from the Favorites node alone.
- `R11_stays_any_folder` (a band in another folder counts as keeping this
  folder's Favorites): killed by
  `test_a_band_of_another_folder_does_not_keep_this_folders_favorites`, a Soul
  row in R&B High, Soul's split place, which is R&B's playlist.

So 25 of 25 rows are killed, 23 in the table and 2 by hand.
