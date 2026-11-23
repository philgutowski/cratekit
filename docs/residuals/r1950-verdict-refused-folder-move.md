---
title: A verdict that keeps a two genre track out of its R&B folder is what takes it out of R&B's band
found: at the review of #1000, R-1950, 2026-11-23.
issue: no
---

**The mechanism.** A Soul track whose second genre is R&B (or the reverse)
has two adoption entries, Soul's and R&B's. With no verdict, `adopt move`
plans nothing for it in R&B's band, since R&B's entry claims that folder and
Soul's split place over R&B's band is the track's own other folder
(`adopt/plan.py` `kept_beside`). A collision verdict that withholds the R&B
entry makes it claim nothing (`adopt/move.py` `claims`), so the track is no
longer counted as R&B's, and `build_move_plan` plans removing it from R&B's
band under Soul's split place, the move a one genre Soul track gets. The
same happens with R&B first and Soul second. A one genre R&B track under that
verdict is left alone. So the verdict a person gave to keep adoption out of
R&B is what takes the track out of R&B.

**Measured cost.** Driven at the engine only, with the real `find_collisions`
and `with_collision_verdicts` folding the verdict and a census row built by
hand, no database: the move plan carries one removal from R&B Med. Whether a
person can reach that state through `adopt apply` and `adopt move` on a
library, and whether the removal is what a DJ who gave the verdict wants, is
unmeasured. R-1950's tests do not pin it either way.

**Closes when:** the state is driven through the verbs on a disposable
library and either the move is shown to be what the verdict means, recorded,
or `adopt move` leaves a track in the folder its withheld entry names as it
does for a one genre track. Ledger only until it is driven.
