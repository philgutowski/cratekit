---
title: "Folder-level XML import appends the folder's children rather than replacing them, and rekordbox re-parses masterPlaylists6.xml on every play, so duplicated playlists become a hang"
date: 2026-08-15
category: integration-issues
module: src/cratekit/write/trees.py, src/cratekit/write/rbxml.py, src/cratekit/core/tree_registry.py, src/cratekit/core/rb_writer.py
problem_type: integration_issue
component: rekordbox_xml_bridge
severity: high
resolution_type: documentation_update
rekordbox_version: 7.2.17.0303
refines: "the U9 A2 verdict quoted in write/trees.py (XML playlist import replaces unconditionally)"
applies_when:
  - "An XML payload names a FOLDER node that already exists in the library and the operator imports at the folder"
  - "A re-export shows a playlist count that jumped by more than the run added"
  - "rekordbox spins on every track load and the spin report's main thread is in PlaylistSyncManager / SyncSetting::read"
  - "masterPlaylists6.xml is more than a few hundred kilobytes for a library of ten thousand tracks"
  - "A guard is being designed that reasons from 'import replaces' alone"
---

# Two facts about the bridge that the A2 verdict does not carry

Observed on the source library on 2026-08-15, while diagnosing a rekordbox
spinning wheel that had been getting worse for weeks. Attended, on the live
database after a scratch-copy rehearsal.

## Fact 1: importing a FOLDER appends its children

The A2 verdict recorded in `write/trees.py` is that XML **playlist** import
replaces the same-named playlist unconditionally. That holds. What it does not
say is what happens at the folder level:

**Right-click > Import Playlist on a folder node whose name already exists
merges the folder by name and appends every child playlist as a NEW row. It
does not match the children by name.** Import a folder holding N copies of a
year playlist into a library folder that already holds N, and you have 2N.
Nothing errors and the tree looks fine until you scroll.

Evidence: nine label year playlists existed 3,072 times each under ONE label
folder each; the folders were never duplicated. The archived exports move
geometrically across imports (2 -> 4 -> ... -> 256 -> 768 -> 1536 -> 3072)
between 2026-07-04 and 2026-07-15, born from a payload that carried the label
subtree twice and then multiplied by every whole-tree import that named the
folder.

For the guard model this matters in one direction: `refuse_bridge_write` and
the one-way door in `write/trees.py` reason from "import replaces, so a
database-written membership absent from the payload is destroyed". Add the
second failure: **an import that names an existing folder duplicates every
child that is present in the payload.** Both are silent, both scale with the
payload, and both are reasons the payload has to be minimal and the import has
to be at the playlist node.

## Fact 2: masterPlaylists6.xml is parsed on the UI thread on every play

macOS wrote two `cpu_resource.diag` spin reports for rekordbox 7.2.17 with an
identical main-thread stack:

```
PlayHistoryManager::timerCallback
  DatabaseMediator::addTrackToPlayHistory
    DatabaseMediator::update_playlist_timestamp
      PlaylistSyncManager::updateMasterSyncSettingIfExists
        MasterSyncSetting(juce::File) -> SyncSetting::read(file)
          juce::XmlElement::addChildElement
```

Every play-history write re-reads and re-parses `masterPlaylists6.xml`
(beside `master.db`) on the main thread. At 28,249 `<NODE>` entries and 3.2 MB
that is the hang; at 574 nodes and 65 KB it is invisible. So the playlist
count is not cosmetic. It is a latency budget rekordbox spends on every
track load, and a writer that adds playlists is spending it.

`rb_writer` already copies `masterPlaylists6.xml` beside the database in its
snapshot and restore paths (`MASTER_PLAYLIST_XML`). Any Cratekit path that
creates or deletes `djmdPlaylist` rows owes the XML the matching `<NODE>` edit
(the `Id` attribute is the uppercase hex of the decimal playlist ID); a row
without a node or a node without a row is the inconsistency rekordbox is
least equipped to explain.

## What was done about it

An attended one-off, outside this repo, removed 27,675 duplicate playlists and
231,169 membership rows in under eight seconds: bulk delete of
`djmdSongPlaylist` then `djmdPlaylist`, `Seq` renumbered per touched parent,
`wal_checkpoint(TRUNCATE)`, matching hex-Id nodes stripped from the XML,
`integrity_check ok`, DB and XML agree node for node. Kept the oldest copy of
each maximal membership set per (ParentID, Name), so a superset beat its
subset and two disjoint sets each kept one. Backup of db, wal, shm and xml
taken first. Hard delete was acceptable because Cloud Library Sync was off;
with sync on, rekordbox's own soft delete (`rb_local_deleted = 1`) is the
model to copy.

## What is not built, and closes this

- An emitter invariant in `write/rbxml.py`: refuse to emit a payload with two
  `<NODE>`s of the same Name under the same parent.
- A snapshot-time reading in `rb_writer` or the convergence check: duplicate
  sibling playlists in `djmdPlaylist`, or a `masterPlaylists6.xml` node count
  out of proportion to the library, is a red flag before any write.
- The operator instruction wherever the bridge is described: import playlist
  nodes, never a folder that already exists in the library.

Recorded as R-129 in `docs/residual-findings.md`.
