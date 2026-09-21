# U105 mutation notes

The author's own tables, as METHOD requires since 2026-09-07. No independent
verifier ran, so every row below reads as what the author could or could not
kill, not as a measurement anybody else checked.

**25 rows, two batches, all killed.** `u105-a.md` holds fifteen engine rows over
`modules/tools/mastering.py`, `u105-b.md` ten shell rows over
`master/cli.py`. Split in two so each batch runs inside one foreground command,
since a relay session cannot background the driver. Every row's restore was
verified against `git show HEAD:` by the driver, and `git status` was clean of
source edits after each batch.

**Two rows were dropped for the cap**, logged at the foot of `u105-a-rows.toml`:
the drift intermediate's `-rf64 auto`, the same family as E12 and pinned by the
same test, and the `parts` field of the replaced report, maintainer facing and
measured through E15's emission of the same key.

**One guard had no test when the rows were drafted and got one first:** the
engine's own refusal of an existing joined master, E6. Without it the
handler's pre-check was the only thing covering the queued path, and a direct
engine caller would have archived every part and joined the set before
`master` refused the same destination.

**Rows killing exactly one test**, E4 to E12, E15, S3, S4 and S6 to S8, each
rest on a single test. That is a thin pin, not a zero, and it is recorded here
so a later reader does not mistake a green count for depth.
