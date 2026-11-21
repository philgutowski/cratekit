---
title: A file named with a title that truly ends in _PN loses it, and a doubled or numbered tail is read only once or not at all
found: at the review of #883, R-1724, 2026-11-21.
issue: no
---

**The mechanism.** `titles.name_title` drops a trailing `_PN` from any name
with no title tag, as the brief asks. A title that is truly spelled with it,
`8A - 124 - Artist - Vitamin_PN`, is asked and matched as `Vitamin`, so a
release titled `Vitamin PN` or `Vitamin_PN` is no longer read as the file's
own. `Track_PN_PN` is read as `Track_PN`, and `Track_PN (1)`, a copy's
numbered name, keeps its tail.

**Measured cost.** Driven at round one: the `Vitamin PN` rows matched on
main and miss on the branch, 4 runs, through Discogs and Beatport. No real
title of this kind is known; the doubled and numbered names are main's
reading, unchanged.

**Closes when:** the library is counted for names whose tail is doubled or
followed by a copy number, and for titles a catalogue spells with `PN`.
Ledger only.
