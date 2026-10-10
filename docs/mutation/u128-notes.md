# U128 mutation notes

Two batches, both by `scripts/mutate.py`, the author's own, 24 rows against
the cap of 25, every row user facing since the landing writes playlists into
the live library and an intake file.

**`u128.md`, batch A, 12 rows: 9 killed, 3 zeros.** The claim and the rerun
rule in `account_playlists.py`, and the two warnings in `land_cli.py`. The
zeros were A6 (an abandoned landing read as mirrored), A8 (the first of two
active rows taken as an owned track's row) and A9 (the left rows of a claim
left holding nothing dropped). Each got a test in `bf2c67b7`.

**`u128-b.md`, batch B, 12 rows: 12 killed.** A6b, A8b and A9b are the three
zeros rerun after their tests, each now killed by one test. The rest are the
two media's writers: the bridge engine's stale read before its first move
(B1), the foreign host entry dropped before the index (B2), the owned tracks
resolved at the gate (B3), the owned TrackIDs in the intake playlist (B4), the
account and pass on both records (B5, N2), the owned rows the native commit
joins (N1), the candidate rows the native verb asks (N3), and the left rows
of a native playlist with nothing writable (N4).

The first run of batch B was refused by the driver because one subset
baseline test, `test_set_inspiration_playlist.py::test_no_beat_grid_tempo_or_rating_is_written_for_the_set_playlist`,
failed once with the machine at a load average near 17. It passed three
times alone and the whole subset passed in parallel straight after, so it was
read as starvation and the batch was rerun unchanged.

Dropped below the cap: the bridge's NOT_LANDED rows for a move refused
mid landing, the `split_facts` wording, and the digest key for an emptied
claim on the bridge, each a report surface whose input needs a refused move or
an export with no entry for any owned track and none of whose writes changes
what a playlist holds. Every zero this table reports would read as "the author
could not kill it"; there are none left.
