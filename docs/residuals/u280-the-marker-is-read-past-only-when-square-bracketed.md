---
title: The naming verb's marker is read past only when it is written in square brackets
found: at the build of #791, U280, 2026-11-13.
issue: no
---

**The mechanism.** `tagging/titles.py` reads past the marker the naming verb
writes after the head (`_MARKER`, a square bracketed group), so "[MP3] (Not
Just) Knee Deep" finds its own row. The marker is configurable,
`config.naming.lossy_marker`, and the matcher is not handed the
configuration, so a marker written otherwise, "(MP3)" or "MP3", is read as
part of the title: a leading round group is shed as any title's is, with the
title's own leading group, and a bare word stays in the title.

**Measured cost.** A miss on such a file's row; the default "[MP3]" is read.
Not measured: whether any configuration writes another marker.

**Closes when:** the searcher is handed the configured marker. Ledger only.
