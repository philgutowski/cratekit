---
title: A name crediting the artist before a version with no version word in it is still read as a title
found: at the build of #788, R-1646, 2026-11-12.
issue: no
---

**The mechanism.** R-1646 reads "Artist - X" by its splits only when X ends
in a word of `core.tombstone.VERSION_WORDS` (`_title_starts`, through
`_a_tail_to_shed`). A version written with no such word, "Bernard Badie -
Vocal" or "Bernard Badie - Beats", is read as a title X by the artist, as
every "Artist - Title" name is, so a row "Vocal" by the artist matches it.
This is the list failing open in the one direction R-1646 leaves to it: the
alternative, reading every "Artist - Title" name by its splits, would refuse
nearly every untagged file asked by its name.

**Measured cost.** Driven through `tagging.searchers._title_matches`: "Bernard
Badie - Vocal" matches a row "Vocal", on `main` and on the branch alike. A
wrong genre only for a self titled track whose name writes its version as
bare words with no version word among them. Not measured: how many files are
named so.

**Closes when:** a version is told from a title without a list, or Phillip
decides that an untagged "Artist - W" name is asked by its splits. Ledger
only: no rule closes it without refusing the common case.
