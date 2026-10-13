---
title: An attended rename of a set playlist leaves the account ledger and the frozen job name behind
found: at the review of #310, U136, 2026-10-12.
issue: no
---

**The mechanism.** After the attended rename of the two Public Service
playlists, `export set` with no name plans a twin account playlist.
`recorded_playlist` reads the live row's Name so INSPIRATION follows the
rename, but the account ledger still holds the old `10_10_26 ...` name and
`frozen_name(job)` is immutable on the job payload, so the renamed playlist
reads as inspiration without an account playlist. The brief's "record
follow" would update the ledger (and a hand step for the frozen name) when
the attended tail renames; U136 does not add that write.

**Measured cost.** Not driven here. A person who renamed the INSPIRATION
playlist by hand and then runs `export set` without a name gets a second
account playlist under the frozen or ledger name beside the renamed one,
or a plan that cannot match the renamed inspiration row to an account
playlist. The hand step on the attended tail is to rename the account
playlist to match and update the ledger entry, or to pass `--name` on
`export set`.

**Closes when:** the attended rename writes the new name into the account
ledger and either refreshes the frozen `PLAYLIST_NAME` on the job or stops
preferring the frozen name once a live INSPIRATION row for the job is
recorded under another name. Ledger only until that write is designed.
