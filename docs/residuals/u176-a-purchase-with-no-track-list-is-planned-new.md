---
title: The Bandcamp plan calls a purchase with no track list new, and a compilation crediting Various Artists per track is not read as Artist - Title
found: at the first review of #357, U176, 2026-10-28.
issue: no
---

**The mechanism.** `bandcamp_cli.plan` resolves a purchase per track from its
track list. A purchase whose list is absent has nothing to resolve and is
planned `new`, which the plan's own wording reads as nothing of it in the
library. A compilation whose tracks carry the release artist, `Various
Artists`, with `Artist - Title` titles, is resolved under `Various Artists`
and planned `new`; the split into artist and title applies only when the
track names no artist.

**Measured cost.** Driven: the plan misreports, and the worker's check of each
downloaded file by its own tags holds the owned tracks back, so nothing owned
is staged. The cost is a plan line that overstates what will arrive, and a
download of a release whose files are then all held.

**Closes when:** an absent track list is its own disposition or a note on the
row, and a track artist equal to the release artist is read the way an empty
one is. Ledger only.
