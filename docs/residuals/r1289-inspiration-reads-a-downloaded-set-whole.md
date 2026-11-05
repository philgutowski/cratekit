---
title: crate organize leaves a downloaded set out of INSPIRATION when one of its tracks names no title or no artist
found: at the review of #547, R-1289, 2026-11-05.
issue: yes
---

**The mechanism.** `organize/inspiration.py` `_read` lists a downloaded set's
account playlist through `label_cli.playlist_listing_or_refuse` and reads the
rows whole with `match.read_tidal_tracks`, which raises `UnreadableList` when
one row names no title or no artist. `plan` catches it and files the whole set
as unread with the reader's message, so none of its tracks is matched and no
INSPIRATION playlist is written for it. `crate sync twins` (U213), `crate sync
pair` (R-1264), `crate sync all`'s sweep and the mirror's downloads (R-1289)
now read row by row through `intake_cli.list_playlist_readable`; this is the
class one file over.

**Measured cost.** Driven by the review's round one on a fake catalogue:
`inspiration._read` over a set listing tracks 101, 102 and an untitled 103
raised "track 3 names no title". The set is named unread with that message,
so the report is not silent, but its readable tracks never reach INSPIRATION
while the provider lists the one row that way. Live reachability is the
ledger's unmeasured one for R-1264.

**Closes when:** `_read` reads the set row by row, matches the readable tracks
and names each unread one beside the set's misses. Earns an issue under the
board bar's (c): a workflow a DJ needs, bringing a downloaded set into
INSPIRATION, cannot finish for that set.
