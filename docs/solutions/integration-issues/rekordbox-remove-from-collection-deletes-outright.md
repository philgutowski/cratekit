---
title: rekordbox's Remove from Collection deletes the content row and its memberships outright, and sweeps a live orphan artist
date: 2026-11-21
category: integration-issues
module: "src/cratekit/core/rb_writer.py"
problem_type: integration_issue
component: database
root_cause: incorrect_assumption
resolution_type: documentation_update
severity: high
symptoms:
  - "A removal written as a soft delete leaves a row rekordbox itself never leaves"
  - "An artist row nobody touched is gone after a removal in rekordbox"
applies_when:
  - "A verb is to take a track out of the rekordbox collection the way rekordbox does (U288)"
  - "Code assumes a removed track is marked rb_local_deleted 1 rather than gone"
  - "A writer advances localUpdateCount once per row it writes"
tags:
  - "remove-from-collection"
  - "u288"
  - "a178"
  - "a185"
  - "analysis-files"
  - "soft-delete"
  - "usn"
  - "djmdcontent"
  - "trackno"
  - "r1830"
---

# rekordbox's Remove from Collection deletes outright

## What was measured

At sitting 101 (2026-11-21) one ten second silent AIFF, never analysed and with
no artist, was imported, put alone in a hand made top level playlist, and taken
out with Remove from Collection in rekordbox 7.2.19. Dated copies of the
database were taken with `crate backup run` before and after, with rekordbox
and its agent gone each time, and compared table by table on disposable copies
through `read_only_copy`, every table keyed by its primary key.

## The shape

- **djmdContent:** the row is deleted outright. It is not marked
  `rb_local_deleted` 1. The 7,404 rows already soft deleted stayed as they were.
- **djmdSongPlaylist:** the track's membership is deleted outright.
- **djmdPlaylist:** the playlist row is untouched in every column, its
  `updated_at` and `rb_local_usn` included, and is left empty.
- **djmdArtist:** the one artist row that was live and named by no content row
  and no album was deleted outright, though the removed track never named it.
  Every orphan artist already soft deleted stayed. A launch alone did not sweep
  it: it survived the session that imported the track.
- **agentRegistry:** `localUpdateCount` advanced by 12 for three deleted rows,
  and no surviving row carries any of the twelve values. Do not assume one step
  per row.
- **Unchanged:** every other table, history, cues, `contentFile`, the cloud and
  sync tables (despite the dialog's "removed from the Collections of all synced
  devices"), `djmdProperty` and `uuidIDMap`. No tombstone row is written
  anywhere.
- **Off the database:** the audio file and the analysis store are untouched,
  for a track with no analysis files. A185 below found an analysed track's
  analysis files deleted.

## How to apply

A writer imitating the removal deletes the content row and every
djmdSongPlaylist row naming it, leaves the playlist rows alone, and advances
`localUpdateCount`. It need not reproduce the orphan artist sweep, since
rekordbox runs it itself at its next removal.

**Not measured by A178:** a track with cues, analysis files or history, and
live orphan albums, genres or labels (none existed). A185 below measured the
first three and the album.

## An analysed track with cues and history, from A185

At sitting 102 (2026-11-21) a 60 second 120 BPM click AIFF with an artist and an
album only it carried was imported, analysed on Phillip's standard settings,
given a hot cue and a memory cue, played to its end on a deck so it entered a
history list, and put alone in a hand made playlist; then taken out with Remove
from Collection in rekordbox 7.2.19. Dated copies before and after, compared
table by table through `read_only_copy`.

- **Every row of the track is deleted outright, in nine tables**: djmdContent,
  djmdSongPlaylist, both djmdCue rows, contentCue, all four contentFile rows,
  djmdSongHistory, djmdMixerParam, and the artist and album rows only it named.
  None is marked `rb_local_deleted` 1, the soft deleted rows stayed at 7,404,
  and no row is added or changed anywhere but agentRegistry.
- **The analysis files are deleted too.** The track's folder in the analysis
  store and its DAT, EXT, 2EX and 3EX files are gone (44,457 files to 44,453),
  removed during the removal session. A178's untouched store held nothing of
  its track's. The audio file itself is unchanged, the same sha256 after.
- **Lists are left empty, untouched.** The history list that held the play and
  the hand made playlist both keep their rows unchanged in every column,
  `rb_local_usn` and `updated_at` included, with no members left.
- **Shared rows stay.** The key row the track used stays, one user fewer.
- **The counter:** `localUpdateCount` advanced by 14 for 13 deleted rows (12 for
  3 at A178), and no surviving row carries any of the new values.

So a writer imitating the removal deletes the content row and every row naming
it in djmdSongPlaylist, djmdCue, contentCue, contentFile, djmdSongHistory and
djmdMixerParam, deletes the artist and album rows the removal leaves named by
nothing, deletes the track's analysis folder and files (a write outside the
database, which needs its own guard), leaves playlist and history list rows
alone, and advances `localUpdateCount`. U288 makes the database deletes
through `rb_writer.CollectionRemoval` and refuses a track any other table
names (its plan keeps such a track rather than offering it); it does not
delete the analysis files or the orphan artist and album rows, which it
leaves. Since the row leaves no soft delete marker, its session record names
every row it removed, and `crate delete review` reads that record to offer
the file (R-1037), from a position the removal gives the pass when it has
none, so a first review does not accept the removal as history.
**Measured at sitting 102 (A197, A200), 2026-11-22:** a throwaway between two
real tracks in a playlist made by hand, taken out with Remove from Collection,
leaves **the member after it renumbered**, `TrackNo` 3 to 2 (R-1830); a playlist
deleted by hand in the sidebar is **deleted outright** from `djmdPlaylist`, no
`rb_local_deleted` marker (R-1844; since #926 the deletion pass tells such a
landing from a rollback by a row it made, held under its recorded UUID). On its next launch rekordbox also deleted an
album row and a genre row that no track carried any more (the album a `sync
removed` removal left, a genre a retag had emptied), so orphan album and genre
rows are pruned by rekordbox itself at launch.
**Imitated since #925 (R-1830):** `rb_writer.CollectionRemoval` lowers the
`TrackNo` of each live membership after a removed live one, in every playlist
the removal deletes a row from, by one per removed live row below it, writing
that one column from SQL so no `updated_at` or `rb_local_usn` moves, and the
SQL confinement admits exactly those rows. A row marked `rb_local_deleted` is
neither counted nor moved: this product's own membership writers leave a
marked row at a number a live row also holds, and counting it put two live
rows on one place (review round one). The binding's `remove_from_playlist`
has the same numbering rule but is not reused: it commits by itself and
stamps `updated_at` and `rb_local_usn` on every row it moves, and an ORM
write of `TrackNo` adds `updated_at` through the binding's `onupdate`.
**Still unmeasured:** a history list holding other tracks (left numbered as it
was), a playlist already holding a gap or a row marked removed below the
renumbered one (the rule is applied there unmeasured), how far
`localUpdateCount` moves for a renumbering, label rows, and My Tag and
sampler rows.
