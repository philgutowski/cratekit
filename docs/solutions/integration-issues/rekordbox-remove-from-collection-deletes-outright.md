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
  - "soft-delete"
  - "usn"
  - "djmdcontent"
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
- **Off the database:** the audio file and the analysis store are untouched.

## How to apply

A writer imitating the removal deletes the content row and every
djmdSongPlaylist row naming it, leaves the playlist rows alone, and advances
`localUpdateCount`. It need not reproduce the orphan artist sweep, since
rekordbox runs it itself at its next removal.

**Not measured:** a track with cues, analysis files or history, and live orphan
albums, genres or labels (none existed). How rekordbox clears those is still
open, so a writer either refuses a track holding any of them or waits for a
second check of that shape.
