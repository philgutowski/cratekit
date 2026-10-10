# R-515 mutation notes

Fourteen rows are prepared in `docs/mutation/r515-rows.toml`, pass_kind light, each reverting one guard of this card's diff with the test file named that should kill it: `ListingShortfall.of` and its count guard (bool, non integer, zero or negative), `of` answering None at or over the count, the caching release reader keeping the triple, the adapter's `num_tracks` read, `_short_of` dropping a block that withheld nothing, the label sync question's shortfall line, the intake playlist all withheld case and its warning, the `sync all` sweep's `withheld` block and warning, and the harvest warning.

The watcher runs the table on macOS. `scripts/mutate.py` refuses a red full suite baseline, and the build lane's Linux box has the macOS dependent failures it had before, so the driver was not run or hand rolled around that refusal.

As a preview only, the build lane applied each row by hand on Linux and ran its named test file. Eleven killed. Three survived, and the watcher's run is the measure:

* `S3_of_takes_non_positive`: likely EQUIVALENT. With a zero or negative count, `listed >= declared` holds for any listing, so `of` answers None by the next guard.
* `S5_of_short_over_count`: a real gap. No release or playlist test lists more rows than its declared count, so a negative "withheld" from a long listing goes unseen. The hearts path has its own such test; the listing path does not.
* `S8_short_of_keeps_zero`: a real gap. No test reads back a saved question whose shortfall block withheld zero.

Neither gap is closed here; the brief was the table. They are named for the watcher to decide.
