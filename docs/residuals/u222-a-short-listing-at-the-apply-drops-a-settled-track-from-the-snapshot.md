---
title: A short account listing at the mirror's apply drops a track the rekordbox area settled between the acts from the snapshot, and the next gate plans to add it
found: at the review of #552, U222, 2026-11-05.
issue: no
---

**The mechanism.** U222 hands the snapshot the gate's plan read to the
decided run's whole mirror plan, so `PlaylistPlan.agreed` is the gate's word
there too, and `mirror.settled()` and `PlaylistPlan.unlisted()` take the
tracks a short listing did not list from it. When the rekordbox area's
`mirror-edits` step settled a track into the snapshot between the acts and
the apply's listing comes back short without that track, the decided run's
plan time `record_mirror_agreed` writes the snapshot without it, where main's
live reading kept it. The next run reads the track as rekordbox's own and its
gate shows "add 1" for a track the playlist already holds unlisted.

**Measured cost.** Unmeasured, and contested. Round one of U222's review
reported it driven on U204's world with the fake hiding the track from the
listing (the snapshot after the decided run `['r1']` against `['r1', 'r2']`
with the live reading, and the next gate planning "add 1"). Round two drove
four candidates of that input (the listing short with its count whole, both
short, and the track hidden from the catalogue and from the account fake) and
none produced it: the settle record makes the decided run hold the track, so
`agreed_after` keeps its word. Four candidates were driven and none produces
it; the exact input of round one was not recovered. If it is reachable, the
cost is one wasted request and a false "add 1" on one gate, since the Tidal
adapter reads membership before adding, after which the snapshot repairs
itself.

**Closes when:** the decided run takes the gate's snapshot for the edit rule
alone and the live one for `unlisted()` and the plan time record, or a test
shows the short case keeps the settled word. Ledger only.
