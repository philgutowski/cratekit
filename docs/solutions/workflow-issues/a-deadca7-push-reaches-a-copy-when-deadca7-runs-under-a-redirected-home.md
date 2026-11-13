---
title: "A DEADCA7 push reaches a disposable copy when DEADCA7 runs under a redirected home whose agent settings name the copy"
date: 2026-11-13
category: workflow-issues
module: "core/foreign_tree.py, cli/doctor.py, docs/cutover.md"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: workflow_improvement
tags: [deadca7, copy, rehearsal, rekordbox-agent, options-json, A57]
applies_when:
  - "a card asks for a DEADCA7 push into a copy of the library rather than the live database"
  - "any other app that finds rekordbox's database from the agent's settings has to be aimed at a copy"
---

# A DEADCA7 push reaches a copy under a redirected home

## The trap

DEADCA7 0.2.3 has no library chooser. It finds rekordbox's database itself, from
the rekordbox agent's settings file
(`~/Library/Application Support/Pioneer/rekordboxAgent/storage/options.json`,
its `db-path` and `analysis-data-root-path`), so a push from its window writes
the live database. Sitting 82 held A57 for that reason, and the only aim it saw
was editing the agent's real settings, which points rekordbox itself at the copy
too and leaves the live library one slip away.

## What works, measured at sitting 98

Launch DEADCA7's binary directly with `HOME` set to a folder on the copy. It
resolves its home from `HOME`, so it reads a settings file there, logs there and
backs up there, and the real settings are never touched.

1. Build the copy as the rehearsal rule does (database cloned, library state
   redirected), then beside it:
   - clone `PIONEER/Master/share` into the copy (`cp -Rc`, instant on the APFS
     volume), since a push writes analysis files;
   - copy `masterPlaylists6.xml` and `automixPlaylist6.xml` from
     `PIONEER/Master` beside the copied `master.db`. **Without
     `masterPlaylists6.xml` the push writes the database and then fails** with
     "masterPlaylists6.xml: no such file or directory", leaving a half push;
   - make `home/Library/Application Support/Pioneer/rekordboxAgent/storage/options.json`
     from the real one with `db-path`, `analysis-data-root-path` and
     `settings-root-path` pointed into the copy, and clone the `rekordbox6`
     settings folder and DEADCA7's `deadcatalog` folder into that home.
2. `HOME=<copy>/home /Applications/DEADCA7.app/Contents/MacOS/DEADCA7 &`
3. **Before touching anything**, read the newest log under
   `<copy>/home/Library/Logs/deadca7/`: its `rekordbox found` line must name the
   copy's `master.db`. If it names the live one, quit; a launch alone writes
   nothing.
4. The library's rows record the volume's old name, which is not mounted, so
   DEADCA7 reads them as not on disk. Import real files from the library volume
   with Choose, linked in place; DEADCA7 matches them to the existing rows.
5. Export, rekordbox, Sync writes a `DEADCA7` folder at the top with the
   catalog's playlists, hot cues, grids and waveforms, and backs the database up
   first under `<copy>/home/Library/Application Support/deadca7/rekordbox-backups/`.

`crate doctor` run with the same `HOME` reads that backup folder, so its
`deadca7.push` line compares the push with the product's last backup. Run with
the normal home it reads the real, empty one.

## What the first real push showed

DEADCA7 writes `created_at` and `updated_at` as `0001-01-01T00:00:00Z` on its
folder, playlist and membership rows, which the test fixtures never did (their
stamp is an ordinary 2026 date). That value broke pyrekordbox's date reading in
a time zone west of UTC. U285 (#800, filed as U283) reads it as a bound at the
open seam, `core/rb_dates.py`, and the fixture now writes `ZERO_STAMP` exactly.
A fixture written beside a fix is not the producer's value: drive the real push.
