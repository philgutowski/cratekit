---
title: Rows adopt move took out of a genre folder before R-1965 landed keep that folder's with vox and Favorites, unlisted
found: at the review of #1007, R-1965, round one, 2026-11-23.
issue: no
---

**The mechanism.** A row `tag set` moved and `adopt move` moved on main between U339 and R-1965 had its genre move entry spent (`adopt/genre_moves.py` `discharge`) once its band read back moved, leaving its old folder's `with vox` and Favorites. With the entry spent, the fixed move never asks that folder again, and nothing else lists the leftover.

**Measured cost.** Driven in review round one on a state built by hand to main's documented end state: the leftovers stay and nothing lists them. Whether Phillip's library holds such rows is unmeasured; the run's answer on main told the person to remove them in rekordbox, so nothing false was said.

**Closes when:** a sitting reads whether any row sits in a genre folder's `with vox` or Favorites with no band of that folder (or `converge`'s unexpected list names them), and either they are removed in rekordbox or a one time verb plans them out.
