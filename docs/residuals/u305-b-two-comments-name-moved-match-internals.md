---
title: Two comments in other cards' files name match internals that moved in U305
found: at the build of #862, U305, 2026-11-22.
issue: no
---

**The mechanism.** The comment above `_RESOLVED` in `src/cratekit/intake/cli.py`
points a reader at "the note above `match._REMEMBERED`". U305 split
`acquire/match.py`, and the remembered reads with that note now live in
`acquire/match_library.py`. `match._REMEMBERED` no longer exists as an
attribute of `match`. The file is #864's (U307), so U305 left it. The same
holds for `src/cratekit/modules/outbound/tidal_account.py`, whose comment
names ``match._first_named``, now in `acquire/match_list.py`; that file is
#866's (U309).

**Measured cost.** A reader following either comment finds nothing on
`match`; no code reads either name.

**Closes when:** the comments name `match_library._REMEMBERED` and
`match_list._first_named`, in #864 and #866 or any later edit of those
files. Ledger only.
