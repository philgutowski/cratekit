---
title: Two different titles that fold to nothing by one artist are one recording, so a wanted emoji title is called owned
found: while building #830, U286, 2026-11-13.
issue: yes
---

**The mechanism.** `fold` in `acquire/match.py` keeps letters, digits and
word breaks and drops everything else, so a title of emoji or marks alone
folds to the empty string and `recording_token` gives every such title by
one artist the same token. `resolve_one`'s exact branch then calls any of
them owned by any other.

**Measured cost.** Driven on a disposable directory: a library holding
`Aurora Bloom - 🔥` and a text list asking for `Aurora Bloom - 💧` resolve
`matched`, `exact`, with the held file as the match's path, so the wanted
track is never downloaded and nothing says so. Not caused by U286, whose
title test keeps today's offer for a title that folds to nothing; met while
building its allowance. How many live titles fold to nothing is unmeasured.

**Closes when:** a title that folds to nothing is compared by its unfolded
text, or never read as exact, with a test that two different emoji titles by
one artist do not match. Earns an issue: the product calls a track owned
that the library does not hold, and skips it.
