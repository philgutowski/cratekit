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
`c9192091` reaches and `511cb4be` never touches, and round two found
`_title_matches` the same. The comment at `scripts/title_differential.py:393`
("so Beatport's scorer is held to it as well") is now untrue. The default base
mode, which the solutions entry on a strip that can empty a title describes,
still builds its base side as it did, driven at its default base.

**Measured cost.** A developer tool, not a verb: a session holding a future
`titles` change against its base is told there are no Beatport differences
when there may be some. Driven to the mechanism, not through a whole script
run over a real change.

**Closes when:** the script also sets the base's `shops.titles` (and
`catalogues.titles`) when it loads a base, or loads the base package whole. `scripts/` is #870 (U313)'s. Ledger only.
