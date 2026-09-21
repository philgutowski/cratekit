# R-382 mutation notes

Sixteen rows, the author's own, one pass. Fifteen killed. The brief's named row,
M1, restoring the `source_id == "playlists"` filter, kills 7.

The one zero, M10, lets `open_playlists` keep an empty identity. It is
maintainer facing and equivalent: an empty string in the in flight set matches
no listed playlist, because the adapter drops a listed playlist with no
identifier. The author could not kill it and no test was written for it.

Dropped: D1, widening `source_jobs` for the mark verb, because this unit leaves
that function's behaviour unchanged and its guards were U82's.
