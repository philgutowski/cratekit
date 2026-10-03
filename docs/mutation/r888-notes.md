# R-888 mutation notes

The author's table, not an independent one: every zero reads as "the author
could not kill it" (METHOD, Verification is the author's). A read path, not a
write, so the table is scoped to the unit's own guards, nine rows of the 25
cap, nothing dropped.

One batch, `r888`, over the subset of the listing, label adapter, label
module, label worker and label playlists suites, 412 tests collected on every
row. A zero is promoted to the full suite. Every restore was verified against
`git show HEAD:`.

- H1 the held branch in `artist_releases`, 11 killed. H2 the deduplication on
  the held path, 1. H3 an unheld listing recorded as skipped, 1. H4 the real
  provider listing's budget halved, 1. H5 `held` abstract, 1.
- C1 `can_list` asking a held roster, 7. C2 `can_list` refusing a held object
  that holds nothing, 1.
- R1 the roster serving each listing by its own name, 3.
- **R2 zero**, promoted to the full suite, 12,593 collected, confirmed: the
  roster's member listings wait through the module's `_pause` rather than the
  real clock. Maintainer facing, since `_pause` is `time.sleep` in production,
  so one line and no composite. No test drives a retry at roster construction.

H4's first run was refused by the driver because its text matched both the
`PAGE_SIZES` and the `PAGE_CAPS` row; the row was anchored to the cap's comment
and resumed.
