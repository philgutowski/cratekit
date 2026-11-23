---
title: Ten writers still spell the empty analysis roots refusal inline beside watched_roots
found: at the build of #978, U329, 2026-11-23.
issue: no
---

**The mechanism.** `write.row_defaults.watched_roots` is the one home of
"the roots a write's analysis-file watch covers, refused when empty" since
U329, which `intake.rotate`, `intake.analyzed`, `intake.refill`,
`intake.shelve`, `write.row_link` and `analysis.head_adopt` call. Ten other
writers raise the same `ValueError` with the same three sentences inline,
inside a longer function: `write/trees.py`, `write/genre_favorites.py`,
`write/playlist_pair.py`, `tagging/rows.py`, `sync/twins.py`,
`sync/pair_reverse.py`, `sync/removed.py`, `favorites/spine.py`,
`intake/native.py` and `intake/set_playlist.py`. Neither reading
U290 measures sees them: each copy is under six logical lines and is not a
function body of its own.

**Measured cost.** None to a user: every copy refuses the same empty list
with the same words, measured by grep, and no test reads the words. A change
to the refusal made in the home alone would leave ten writers saying the old
thing.

**Closes when:** each of the ten calls `row_defaults.watched_roots`, or the
measure grows a reading of copied statement runs shorter than six lines.
Ledger only.
