---
title: A label playlists build from a sync's releases does not ask the tombstone a full build asks, so a release deleted on purpose can reach its year playlist
found: at the review of #402, U191, 2026-10-31.
issue: no
---

**The mechanism.** A full `crate label playlists LABEL` confirms the listing
through `sweep.confirm_listed`, which asks the version tombstone first and
counts a suppressed release as "deleted on purpose". `--releases` reads the
releases a go took straight from the label sync record in
`src/cratekit/label/playlists_cli.py` (`read_taken`) and never asks the
tombstone, and its screen counts no suppressed release.

**Measured cost.** Driven at the review with a tombstone written to the store
for a taken release's artist and title: the full build left that release out
and said so, and `--releases` added its tracks to the year playlist with a
screen saying nothing was left out. Reach is narrow and was not driven
through `crate deletion`: the tombstone is keyed by a deleted track version's
artist and title, so it matches a release only when the two coincide, as on a
single, and the go itself would already have downloaded the release.

**Closes when:** `read_taken` asks the same suppression reader over each taken
release's recorded artist and title before reading it, and the screen counts
what it suppressed. Ledger only: the reach is a single deleted on purpose and
then taken again by a sync.
