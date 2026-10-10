**Last sitting 2026-09-17, afternoon, attended, six workflows on
`sitting/tidal-runs`.** Not a unit. The three adapters U62, U63 and U64 landed
in September have now each run against the live Tidal account, which is what
`docs/cutover.md` said they owed, and its Sitting 4 table is the record. **R-355
was fixed inside the sitting**: the rows both outbound verbs build carried no
ISRC, so a live export or sweep matched nothing and reported a clean job.
`modules/outbound/source.isrc_for` now resolves each row's `Location` through the
configured prefix map and reads the file's own tag, `isrc` is a field in
`core/tags.py` (`TSRC` in ID3), a value that is not ISRC shaped reads as none,
and an absent library root refuses rather than reading as a library of untagged
files, which the review of the fix found. Live: 103 of 109 favourites and 8246 of
9937 collection rows carry an ISRC where none did before.

With that, `crate export playlist` ran twice on a real four track playlist, one
remote playlist created, 2 added, 2 unmatched, the second run adding nothing, and
`crate sync favorites` ran twice over 109 rows, 18 hearted and verified present on
the account, the second pass hearting nothing and reading all 59 matched rows as
already. **R-144 is CLOSED on the ledger.** Also live: one harvest, one intake
playlist, one 47 label sweep of which 32 labels refused, and one `crate sync all`
that listed 599 playlists and queued 19 jobs, **none of them resumed**, 11 being
source system label debris.

Six findings filed, R-378 to R-383. **R-383 is the one that matters beyond the
sitting**: `listing.paginate` stops at the first short page, and this provider's
favourites listing serves short pages because the client drops unplayable tracks,
so the account's 197 favourites read as 93. Playlists and playlist membership were
measured clean, so it is the filtered listings rather than the helper being wrong
everywhere. Phillip decided it is a unit, not a sitting fix. Mutation table
`docs/mutation/sitting4.md`, 10 rows, 8 killing; `sitting4-notes.md` records that
G9's remeasure was killed by memory pressure and is asserted rather than
measured, and that both driver runs were moved to the background by the harness.
Battery on the committed tree is in the merge commit. Do not take #29.
