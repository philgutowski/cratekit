---
title: A Bandcamp heading crediting the artist by initials no longer meets a name written with the same initials and a version part
found: at the review of #788, R-1646, round two, 2026-11-13.
issue: no
---

**The mechanism.** R-1646 reads the whole name of a file whose first part is
the artist's own credit unshed (`_readings`, `_credits_before_featuring`), so
a feature credit cut from it never leaves the artist's name. Bandcamp drops a
heading's head only when `_artist_matches` reads it as the artist, which an
initial does not satisfy, so a heading "B. Badie - Sunrise Mood" is read
whole, while the file "B. Badie - Sunrise Mood - Extended Mix", tagged
"Bernard Badie", now credits the artist by `_names_the_artist`'s initials and
is read unshed. The two met on `main` through the shed whole name and no
longer do.

**Measured cost.** A miss, driven at round two through the Bandcamp parser:
True on `main` and on round one's head, False on the branch. Bandcamp is no
longer asked by `tag folder` (it answers every search with a bot check), so
no shipped verb reaches it. No producer of the heading was driven.

**Closes when:** Bandcamp's heading test and `_names_the_artist` read an
artist's credit the same way. Ledger only.
