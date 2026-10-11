# U130 mutation notes

Three batches, all by `scripts/mutate.py`, the author's own, 24 rows against
the cap of 25. Every row is user facing: the pair writes memberships into the
live library and tracks onto the account.

**`u130-a.md`, batch A, 6 rows: 6 killed.** The merge in `sync/pair_merge.py`:
an addition beating a removal (A1), a re-add on a new rekordbox row (A2), who
leads the order (A3, A4), a new track placed after its predecessor (A5), and
how a changed order is read (A6).

**`u130-b.md`, batch B, 9 rows: 9 killed.** The plan in `sync/pair_cli.py`: the
short listing's base and its account writes (B1, B2), the account playlist's
own ISRC before the provider (B3), no provider call without an ISRC (B4), the
re-add rule for a track held twice (B5), no second acquisition (B6), the scope
of a pair (B7, B8), and a gone pair left out of a sync of every pair (B9).

**`u130-c.md`, batch C, 9 rows: 7 killed, 2 zeros, both since killed by hand.**
C2 (a snapshot recorded from a short listing) was a zero because the test faked
a withheld track by deleting it, which the sync rightly added back, so the two
arms ended alike; the drive also showed a short listing offering a withheld
track back to the account, which was fixed. C4 (the writer's own stale
membership check) was a zero because the gate's digest refuses the same change
first. Each got a test in the commit after the table, and each mutation was
then applied by hand, run against `tests/test_sync_pair.py`, and restored from
`git show HEAD:`: C2 one death, C4 one death. Those two counts were measured
outside the driver and are the author's.

Two baselines were refused before batch A ran, each over a different single
test that passed alone and in a full run straight after. See the residual
titled "Two tests failed once each in a loaded full suite and never again".

Dropped below the cap, both logged in their row files: B10, the guard that
keeps an add of a row already held live off the gate, since
`add_memberships` already skips a live member; and C10, the read back after
the rekordbox commit, a verification guard no driven input can make differ.
