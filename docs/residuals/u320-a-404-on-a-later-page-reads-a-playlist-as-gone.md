---
title: A 404 on a later page of a playlist whose id opened is read as a sighting, and sync removed calls it a playlist whose id does not open
found: at the review of #889, U320, round two, 2026-11-21.
issue: no
---

**The mechanism.** `sync.removed.read_one` reads any per playlist failure of
`intake_cli.list_playlist_readable` on a playlist the account's list omits as
"its id does not open", and `unavailable.answered_unavailable` reads its chain.
A playlist whose id opens and whose first page is served, and whose later page
answers 404 through the whole retry ladder, is recorded as a sighting and
retired a day later, its why saying the id does not open.

**Measured cost.** Driven by review round two on fixtures: recorded, then
retired, the why untrue; the track it served was kept by its rekordbox twin,
so no wrong offer was produced in the shape driven. Without a twin, a track
on that playlist removed from another would be offered. A real 404 on a later
page of a playlist that exists is unmeasured.

**Closes when:** a sighting is read only off a failure of `playlist_for`
itself, with the listing's later pages read as any other failure. Ledger only.
