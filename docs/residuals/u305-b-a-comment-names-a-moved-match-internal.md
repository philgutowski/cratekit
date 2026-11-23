---
title: A comment in another card's file names a match internal that moved in U305
found: at the build of #862, U305, 2026-11-22.
issue: no
---

**The mechanism.** The comment above `_RESOLVED` in `src/cratekit/intake/cli.py`
points a reader at "the note above `match._REMEMBERED`". U305 split
`acquire/match.py`, and the remembered reads with that note now live in
`acquire/match_library.py`. `match._REMEMBERED` no longer exists as an
attribute of `match`. The file is #864's (U307), so U305 left it. A second comment, in
`src/cratekit/modules/outbound/tidal_account.py`, named ``match._first_named``
at the build; #866 (U309) rewrote that file and landed before this unit
merged, and no comment there names it now.

**Measured cost.** A reader following the comment finds nothing on
`match`; no code reads the name.

**Closes when:** the comment names `match_library._REMEMBERED`, in #864 or
any later edit of that file. Ledger only.
