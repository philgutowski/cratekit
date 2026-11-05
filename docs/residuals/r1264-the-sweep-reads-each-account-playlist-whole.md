---
title: crate sync all leaves out a whole account playlist when one of its tracks names no title or no artist
found: at the review of #532, R-1264, 2026-11-05.
issue: yes
---

**The mechanism.** `sync/playlists.py` lists each account playlist it sweeps
through `intake_cli.list_playlist_declared`, whose reader refuses the whole
listing with `intake-list-unusable` when one row names no title or no artist.
The sweep takes that refusal per playlist, so the run goes on, but the playlist
is excluded as unreadable and none of its readable tracks is queued.
`organize/mirror_downloads.py` lists the same way (not driven). `crate sync
twins` (U213) and `crate sync pair` (R-1264) now read row by row through
`intake_cli.list_playlist_readable`; the sweep is the class one file over.

**Measured cost.** Driven by the review's round one on a disposable world: a
swept playlist holding two readable tracks and a third with no title was
excluded with "track 3 names no title", and only the other playlist queued.
The playlist is named in the summary and a warning, so the report is not
clean, but its readable tracks never reach intake while the provider lists the
one row that way, which may be for good. Live reachability is the ledger's
unmeasured one for R-1264.

**Closes when:** the sweep (and the mirror's downloads) read each playlist row
by row through `list_playlist_readable`, queue the readable tracks and name
each unread one. Earns an issue under the board bar's (c): a workflow a DJ
needs, bringing an account playlist into intake, cannot finish for that
playlist.
