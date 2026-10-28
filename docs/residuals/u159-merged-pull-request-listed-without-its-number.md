---
title: A pull request whose branch merged main before landing is listed in the notes without its number
found: at the review of #340, U159, 2026-10-28.
issue: no
---

**The mechanism.** `landings_since` in `scripts/release.py` matches a pull
request by its merge commit or by its head being the second parent of a first
parent merge. Pull requests 306, 312 and 313 merged `main` into their branch
after their last head, so neither matches, and each lands under "Merged
without a pull request" with its merge subject.

**Measured cost.** Driven on a full clone; cosmetic, the landing is listed.

**Closes when:** a head that is an ancestor of a merge's second parent also
matches. Ledger only.
