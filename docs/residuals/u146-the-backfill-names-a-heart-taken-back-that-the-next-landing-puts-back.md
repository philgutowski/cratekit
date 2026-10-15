---
title: The backfill names a heart taken out of All Favorites as taken back, and the next landing of a pass that still hearts it puts it back
found: at the review of #325, U146, 2026-10-15.
issue: no
---

**The mechanism.** The brief keeps the backfill's rule that a heart whose All
Favorites membership rekordbox marked removed is skipped and named, and adds
R6, that a track removed from All Favorites by hand and still hearted rejoins
at the next favourites sync. Both are built as written: `backfill.gather`
reads `members_marked_removed`, and the landing's owned path
(`native._favorites_plan`, `backfill.plan_owned`) reads only live membership.
So the backfill's screen says "removed from the playlist in rekordbox" for a
track the very next landing will put back while the account still hearts it.

**Measured cost.** Driven in both suites: the backfill names it
(`test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`) and
the landing restores it
(`test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`).
Nothing is lost; the screen tells the author something the next pass undoes,
which is the author's own two step rule for dropping a favourite.

**Closes when:** the backfill's taken back line says the heart rejoins at the
next landing while the account still hearts it, or the author drops one of
the two rules. Ledger only.
