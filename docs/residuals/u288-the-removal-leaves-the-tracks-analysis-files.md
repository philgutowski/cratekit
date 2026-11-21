---
title: crate sync removed leaves a removed track's analysis folder and files, which rekordbox's own removal deletes
found: at the build of #839, U288, 2026-11-21.
issue: no
---

**The mechanism.** A185 measured rekordbox's Remove from Collection deleting
the track's folder in the analysis store and its DAT, EXT, 2EX and 3EX files.
`rb_writer.collection_removal` deletes the `contentFile` rows that name them
and leaves the files, since the verb touches no file and a delete outside the
database needs a guard of its own. So every track `sync removed` takes out
leaves its analysis folder behind, named by no row.

**Measured cost.** Not driven on a live library. A few files and some hundreds
of kilobytes per track; no row reads them, and a track landed again later is
analysed into a new folder. Nothing a person sees in rekordbox.

**Closes when:** the analysis folder is deleted under a guard proving it is the
removed row's own and named by no other row, or Phillip judges the files
harmless. Ledger only.
