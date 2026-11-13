---
title: A name whose first part credits the artist otherwise than the tag names them is still read one way, as on main
found: at the build and review of #791, U280, 2026-11-13.
issue: no
---

**The mechanism.** U280 reads R-1651's first two shapes as ambiguous
(`_only_a_list_reads` in `tagging/titles.py`), but its third needs the parse
to know the first part is the artist's credit, which only the tag can say:
"Bernard Badie feat. Tide - Sunrise Mood" tagged "DJ Bernard Badie" or
"Tide" reads its first part as a title, so the self titled row "Bernard
Badie" matches. With no head before it the first part naming the tag's
artist only as featured is read as a title by design (`_featured_first_part`,
R-1646 round two's test); after a head it is not, since round one of U280's
review drove "08A - 124 - Bernard Badie feat. Tide - Sunrise Mood" tagged
"Tide" to a wrong genre once the rule reached past the head (F3).

**Measured cost.** A wrong genre where the tag disagrees with the name, as
on main and no wider: driven through `_title_matches`; no producer of such a
tag was driven, since the naming verb writes "Artist - Title" from the tags.

**Closes when:** a name's credit can be told without the tag, or a tag that
disagrees with the name is shown common. Ledger only.
