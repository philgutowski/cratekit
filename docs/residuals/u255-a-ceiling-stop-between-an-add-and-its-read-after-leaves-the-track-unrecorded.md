---
title: A ceiling stop between an add and the client's read after it leaves a landed track the outbound ledger never records
found: at the review of #684, U255, 2026-11-12.
issue: no
---

**The mechanism.** The client's add is a POST and then its own GET of the
playlist for the next tag. When the provider gate's per command ceiling
refuses that GET, the add has landed and `export.apply` raises before
`ledger.record_playlist_track`. The resumed item finds the track on the
playlist and reports it as already there, and the ledger's `added` never
names it, so `export prune` reads it as a track a person put there.

**Measured cost.** Driven by round one's review with a real gate over the
counting transport, a ceiling of 6 on main and 4 on the branch: the resume
reports `already` for the track and the ledger records `added: []`, on main
and on the branch alike. No track is lost or added twice. U255 makes the cut
position one in two requests of an add where it was one in four, the same
share per request.

**Closes when:** a track a resumed export finds on the playlist and the
ledger does not name is recorded when the plan matched it to that row, or the
ceiling refusal is raised only between whole adds. Ledger only: the cost is a
prune that leaves a track, not a loss.
