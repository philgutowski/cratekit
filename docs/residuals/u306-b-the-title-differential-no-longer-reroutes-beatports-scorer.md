---
title: scripts/title_differential.py in titles base mode compares the tree's Beatport scorer with itself after the searchers split
found: at the review of #863, U306, 2026-11-22.
issue: no
---

**The mechanism.** In titles base mode the script loads a base revision's
`searchers` and sets `base.titles = base_titles` so the base's Beatport scorer,
`_beatport_best`, reads the base's titles. U306 moved `_beatport_best` to
`tagging/shops.py` and re-exports it from `searchers`, so the function the
script reaches resolves `titles` in `shops`' globals and the reroute no longer
bites: the round one reviewer set a tripwire module as `base.titles`, which
`c9192091` reaches and `511cb4be` never touches. The comment at
`scripts/title_differential.py:393` ("so Beatport's scorer is held to it as
well") and the line in
`docs/solutions/integration-issues/a-strip-that-can-empty-a-title-turns-a-substring-match-into-a-match-anything.md`
that says the script loads main's `searchers.py` for this are now untrue.

**Measured cost.** A developer tool, not a verb: a session holding a future
`titles` change against its base is told there are no Beatport differences
when there may be some. Driven to the mechanism, not through a whole script
run over a real change.

**Closes when:** the script also sets the base's `shops.titles` (and
`catalogues.titles`) when it loads a base, or loads the base package whole,
and the solutions line says so. `scripts/` is #870 (U313)'s. Ledger only.
