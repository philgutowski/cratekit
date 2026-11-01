---
title: A label sync go with one track refused for good ends failed and runs no tail, where sync land skips the track and lands the rest
found: at the build of #401, U190, 2026-11-01.
issue: yes
---

**The mechanism.** `label/go.py` drives its download through
`acquire_cli.drive_queued`, which ends on `jobs.raise_for_state` and raises
for a job that ended FAILED, however its items failed. A go whose release
holds one track the provider offers only lossy therefore ends `lossy-refused`
with every other track downloaded into staging, and no tail runs: U190 sets
the go's tail only when its download SUCCEEDED. `crate sync land` reads the
same state differently (`_download` in `cli/sync_land.py`): a job FAILED only
by items refused for good is a download that landed, the refused tracks are
named and skipped, and the tail runs on the rest.

**Measured cost.** Driven on the branch with the fake adapter, one release of
two tracks, the second landing lossy: the go exited 42 `lossy-refused`, the
tail stand in recorded no call, and the refusal's only step was "the failed
items cannot succeed on resume; inspect each item's cause". The downloaded
track sits in staging with no command named to land it, and since the answer
is settled a second go does not take it again. The live frequency of a lossy
only track in a followed label's release was not measured.

**Closes when:** the go reads a download FAILED only by items refused for
good the way `sync land` does, names and skips them, and runs the tail on the
tracks that landed, with a test driving one lossy track in a two track
release. It earns an issue because a label landing a DJ needs cannot finish
in the one command the product now offers, and the way on is not named.
