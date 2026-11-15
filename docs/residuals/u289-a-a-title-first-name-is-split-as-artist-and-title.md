---
title: An untagged name written title first is split with its title as the artist
found: at the review of #843, U289, 2026-11-15.
issue: no
---

**The mechanism.** `titles.by_name` reads a headed name of exactly two body
parts as `Artist - Title`, the order `naming.compose_body` writes. A name
written the other way round, `08A - 124 - Sunrise Mood - Bernard Badie` (the
reader's own corpus holds a `{title} - {credit}` body,
`tests/test_title_matcher.py`), is asked with artist `Sunrise Mood` and
track `Bernard Badie`, recorded `by-name`. Nothing in the name tells the two
orders apart without an artist tag.

**Measured cost.** Driven at round one through `tag_one` with a recorded
release credited `Sunrise Mood` carrying a track `Bernard Badie`: that
release's style is written, where main gave `no-hit`. The real recording's
row misses on both. Reachability is unmeasured: no catalogue holding a
release credited to the title's words with a track named after the artist
was driven, and both gates of the unchanged matcher (artist and title) must
pass for a write.

**Closes when:** the split is refused, or both orders are asked and the
catalogue's row decides, or a live sweep over untagged library names counts
how many are written title first. Ledger only.
