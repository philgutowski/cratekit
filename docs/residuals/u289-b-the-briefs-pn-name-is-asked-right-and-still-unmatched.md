---
title: The brief's untagged Obiman name is asked right and still matched by no release, for its _PN tail
found: at the review of #843, U289, 2026-11-15.
issue: no
---

**The mechanism.** `9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN`
is now asked as artist `Obiman` and track `On The Rocks (Cafe Del Mar
Mix)_PN`, as the card asks. The `_PN` tail after the bracket keeps
`searchers._last_group_stripped` from setting the mix aside, and the shared
matcher reads `mix)_pn` as part of the title's words, so the release
`On The Rocks (Cafe Del Mar Mix)` is not read as the file's own.

**Measured cost.** Driven at round one with that release recorded: `no-hit`
on main and on the branch, and a match (Chill / Ambient) with the tail
removed. A file of this shape stays untagged, as before; not a regression.
How many library names carry a suffix after their mix is unmeasured.

**Closes when:** the name reader or the matcher reads a trailing
underscore suffix after a bracket group as no part of the title, decided on
a count of such names on the live library. Ledger only.
