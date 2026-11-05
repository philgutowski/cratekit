---
title: crate sync pair refuses every pair when one paired account playlist lists a track with no title or no artist
found: at the build of #507, U213, 2026-11-05.
issue: yes
---

**The mechanism.** `sync/pair_cli.py` plans each pair's account side through
`intake_cli.list_playlist_dated`, whose reader refuses the whole playlist with
`intake-list-unusable` when one row names no title or no artist. A sync of
every pair passes over a pair only for the two refusals in
`PER_PAIR_REASONS` (`sync-pair-unknown`, `sync-pair-out-of-scope`), so that
refusal stops the run at that pair and no other pair syncs. The account
playlists a synced folder brings take it per playlist (`BROUGHT_REASONS`);
the pairs already made do not.

**Measured cost.** Driven on the twins suite's disposable database: a
backfilled twin whose account playlist lists one track with an empty title,
then `crate sync pair` with no argument, refuses `intake-list-unusable`
("track 3 names no title") and syncs nothing; named alone, the pair refuses
the same way. U213 made this more reachable: before it, `crate sync twins`
refused on such a playlist and paired nothing, and now it makes the twin and
names the track, so the next pair sync stops. A pair made by hand over such a
playlist met it before U213 too. The live case that opened U213, a title
written wholly in brackets, now reads, so on the live account the producer
left is a row with an empty title or no artist, whose reachability is
unmeasured.

**Closes when:** a sync of every pair names a pair whose account listing the
reader refuses and syncs the others, or the pair's account side is read row by
row as the twins backfill reads it (`intake_cli.list_playlist_readable`), a
track the reader refuses kept by its id. Earns an issue under the board bar's
(c): `crate sync pair` is the workflow that keeps every twin one list, and one
track stops it for every pair.
