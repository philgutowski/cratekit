---
title: "A list manifest is not the record of what a sync pass still owes; the intake reports are"
date: 2026-09-19
category: integration-issues
module: src/cratekit/sync/mark_cli.py
problem_type: integration_issue
component: sync
severity: high
resolution_type: code_fix
applies_when:
  - "A verb has to decide whether a playlist, a set or a whole sync pass is finished"
  - "A unit's brief names the .manifest.json beside a list as the input to a completeness check"
  - "A check counts manifest rows per source_ref and reads no rows as nothing owed"
tags: [manifest, listdoc, intake-reports, offered, handed-on, sync-mark, u82, r-358]
---

# A list manifest is not the record of what a sync pass still owes

## What happened

U82's brief said to mark an account playlist as DOWNLOADED when every manifest
row naming it had landed or was owned. Built that way, the suite was green and
`/code-review` drove a playlist marked over a track that was not in the library.

## Why

`crate intake missing` writes `<name>.list.json` and `<name>.manifest.json` for
`acquire download` to read. They are a DOWNLOAD list. Two kinds of track a pass
did not find never reach them:

- a track the pass OFFERED for review, because the library holds something
  close. It is not missing, so it is not listed, and it is not in the library.
- a missing track the provider gave no id, which is handed on to
  `<name>.unlisted.json`, a text list with no playlist attribution at all.

So "no manifest row names this playlist" means "nothing of it is downloadable",
which is not "nothing of it is owed". Three more holes follow from the file
being derived and separate: a manifest passed by flag can be another pass's and
yields no rows for this one, a pass whose every missing track was handed on has
no manifest, and the manifest only says which playlists asked for a shared
track through `source_refs`, written only when more than one did.

## What to read instead

The intake job's committed reports, through `missing_cli.job_reports(store,
job)`. One report per track, per playlist, written once, carrying `state`
(`owned`, `suppressed`, `offered`, `missing`) and a frozen `track` that
`intake_cli.thawed` turns back into the `match.Wanted` the engine reads. The
manifest is made from these. A completeness check resolves every `offered` and
`missing` report against `match_cli.library_view(cfg)` as the library is now.

## Two traps met on the way

`match.resolve_one` asks the tombstones LAST, immediately before it calls a
track missing. A wanted title close to one the library holds resolves
`needs_review` and the tombstone is never consulted. The shared test tracks
`Artist 101 - Title 101` and `Artist 102 - Title 102` are close enough to do
this, so a test about a suppressed track needs a track that resembles nothing
else in the fixture.

`match_cli.adjudicate` is what reads an accepted review verdict, and it files
review items as it goes. A verb that stops at a gate cannot call it on the way
there without moving state for an answer of abort. R-482 is that gap.
