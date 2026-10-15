---
title: A playlist the product makes on the account is swept as intake unless the sweep is told
date: 2026-10-03
category: integration-issues
module: src/cratekit/sync/playlists.py
problem_type: integration_issue
component: tooling
severity: high
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - "A verb creates playlists on the streaming account"
  - "A new account playlist convention is added beside the swept prefix, the label debris suffix and the favourites placeholder"
---

# A playlist the product makes on the account is swept as intake unless the sweep is told

## Problem

R-835 made `crate label playlists`, which creates one private `<Label> <year>`
playlist per release year of a followed label. Nothing in the brief mentioned
`sync all`. But the playlists source of `sync all` queues EVERY account
playlist it lists that no rule excludes, and a fresh year playlist meets none
of them: no swept prefix, no ` LIBRARY` suffix, not a favourites placeholder,
not in the cursor. The next pass would have queued every year playlist as an
intake job, and `intake missing` would then have listed the label's whole
catalogue as missing from the library.

## Cause

The sweep decides what is intake by exclusion, in `sync.playlists.exclusion`,
and the exclusions are naming conventions plus the cursor. A playlist the
product itself creates carries none of them until something marks it. The
source system has the same trap and closes it by marking each label playlist
`DOWNLOADED ` at once; this product marks only after a batch lands, so in
between the year playlists were plain intake.

## Fix

`Excluded.LABEL_FOLDER`. The outbound ledger records every year playlist a
build made, `ledger.label_playlist_ids` reads them, and `sync.cli` hands the
set to `playlists.plan` as `label_built`. It is HANDED IN rather than read in
`sync/playlists.py`, because that source is core and the ledger is the outbound
feature module's, which a core module does not import. A test drives the hand
off as well as the exclusion, since the mutation table found the exclusion
tested and the hand off not (`docs/mutation/r835-notes.md`, S2).

## The rule

Any verb that creates a playlist on the account must answer, in the same
unit, what the playlists sweep does with it next pass. Exclude it by a record
the product keeps, by identifier, never by a title a person can also type.
R-837's set playlists are the next verb this applies to.

U147's account mirrors were the third such verb, and nothing in their brief
named the sweep either: about 130 mirrored playlists, each holding tracks the
library already owns, would have been swept and then marked with the swept
prefix under the mirror. `Excluded.MIRROR`, handed in from
`ledger.mirror_playlist_ids`. The same unit found the rule has a second half,
`sync pair`: a playlist another writer keeps must also be refused as a pair,
or two writers each remove what the other adds (`pair_cli._scope_account`).
