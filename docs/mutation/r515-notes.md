# R-515 mutation notes

Fourteen rows are prepared in `docs/mutation/r515-rows.toml`, pass_kind light, each reverting one guard of this card's diff with the test file named that should kill it: `ListingShortfall.of` and its count guard (bool, non integer, zero or negative), `of` answering None at or over the count, the caching release reader keeping the triple, the adapter's `num_tracks` read, `_short_of` dropping a block that withheld nothing, the label sync question's shortfall line, the intake playlist all withheld case and its warning, the `sync all` sweep's `withheld` block and warning, and the harvest warning.

The watcher runs the table on macOS. `scripts/mutate.py` refuses a red full suite baseline, and the build lane's Linux box has the macOS dependent failures it had before, so the driver was not run or hand rolled around that refusal.

As a preview only, the build lane applied each row by hand on Linux and ran its named test file. Eleven killed. Three survived on that first pass; the two real gaps are closed on this branch, and the third is inert:

* `S3_of_takes_non_positive` is inert (equivalent), confirmed by the watcher's macOS run on the full suite: with a zero or negative count `listed >= declared` holds for any listing and the next guard answers None.
* `S5_of_short_over_count`: closed by `test_a_listing_that_serves_more_than_its_declared_count_carries_no_shortfall` in `tests/test_label_tidal_catalogue.py`.
* `S8_short_of_keeps_zero`: closed by `test_a_saved_shortfall_that_withheld_nothing_reads_back_as_no_shortfall` in `tests/test_label_sync.py`.
