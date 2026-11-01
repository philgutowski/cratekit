---
title: A taken release whose every track the provider will not play still makes its year playlist, empty, on a label playlists build
found: at the review of #402, U191, 2026-10-31.
issue: no
---

**The mechanism.** `_grouped` in `src/cratekit/label/playlists_cli.py` opens a
year before it filters out the tracks the provider will not play, so a release
whose every track is unavailable yields a year with no track. `folders.plan`
then plans that year as a create with nothing to add, and the folder with it.
The full build has had the same shape since R-835; `--releases` makes it the
whole plan when the one taken release is that release.

**Measured cost.** Driven at the review on the fake catalogue: the plan showed
"Kompakt 2025: create it private, put it in the folder, add 0 of 0 track(s)",
and the apply made the folder and an empty playlist. It is shown before the
gate, so nothing is written unseen. Not driven against the provider: how often
every track of a release a go just took stops playing is unmeasured.

**Closes when:** a year opens only once a playable track is found, and a
release with none is counted on the screen with the undated. Ledger only.
