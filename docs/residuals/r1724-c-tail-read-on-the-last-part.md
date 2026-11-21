---
title: The tail is read off when the last dash part keeps a title, though the title past the head and marker may be the tail alone
found: at the review of #883, R-1724, round two, 2026-11-21.
issue: no
---

**The mechanism.** `titles.name_title` keeps a name unchanged only when its
last dash part is the tail alone. In `8A - 124 - [MP3] _PN`, `8A - 124 -
[MP3]_PN`, `8A - 124_PN` and `8A_PN` the last part keeps a letter or digit
once the tail is off (`[MP3]`, `124`, `8A`), so the name is read past the
tail, and the question is a head alone, `8A - 124 - [MP3]` (`head-alone`),
where main asked `_PN`. The guard reads the last dash part; the question
reads past the head and the marker.

**Measured cost.** Driven at round two through `tag_one`, the `tag folder`
verb and `tag retag`: every such file took the same genre by ISRC on both
sides, and only the record's `asked` text differs. A main match was lost
only against a contrived row titled `PN`. No producer writes such a name in
this container.

**Closes when:** the tail alone test reads the title past the head and the
marker, or the shape is measured absent from the library. Ledger only.
