---
title: name apply now reads the title tag's head before the file name's for every file, not only a file the collection references
found: at the review of #944, U327, 2026-11-23.
issue: no
---

**The mechanism.** The brief asked that a reader which would give the old
head for a corrected track read the title tag's head first "for a row that is
in the collection". `write/naming_cli._spec_for` cannot know that when it
builds a spec (the collection is read after the walk, and only when a
candidate exists), and for a referenced file the rename is held back either
way, so the order matters only once a corrected track has left the
collection, when no flag can say it was ever in it. The session made the title
tag lead for every file; `acquire/match_library._read_fresh` the same.

**Measured cost.** None driven: 0 producers were driven of a file outside the
collection whose title tag and file name carry different heads. Every file
`analyze run` stamps and every file the live system wrote carries the same
head on both surfaces, so the order changes nothing for them. A file renamed
by hand to another head while its tag kept the old one would now be renamed
back to the tag's head where it used to have its tag rewritten.

**Closes when:** Phillip confirms the title tag leads for every file, or a
card scopes it to files the collection references. Ledger only.
