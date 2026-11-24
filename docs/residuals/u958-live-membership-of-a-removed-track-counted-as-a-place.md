---
title: The closing up counts a live membership of a track marked removed from the collection as a place, and whether rekordbox shows that row is unmeasured
found: at the review of #1058, U958, round one, 2026-11-24.
issue: no
---

**The mechanism.** `rb_positions.contiguous_positions` and `numbering` read a
membership row as live from its own `rb_local_deleted` alone. A live membership
whose content row is marked removed (a cloud sync tombstone, R-675's shape) is
numbered as a place. `playlist_pair.members` leaves such a row out of what it
says rekordbox shows. If rekordbox does not show it, the shown positions skip
it, and the closing up leaves the numbers one off from the positions after it,
the defect U958 closes.

**Measured cost.** Driven by the round one review on a disposable library with
member 2's content row marked removed: the numbering read the playlist 1 to 4
as contiguous and the doctor row read OK, while `playlist_pair.members` showed
three rows. What rekordbox shows for such a row was not measured; no product
code marks a content row removed while keeping its memberships.

**Closes when:** an attended sitting reads whether rekordbox shows a live
membership of a track marked removed from the collection, and the rule counts
or skips it to match. Ledger only.
