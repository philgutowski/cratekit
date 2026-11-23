---
title: A cleared second genre leaves the track in that folder, and converge reads it as matching when it is the playlist's only track
found: at the review of #989, U340, 2026-11-23.
issue: yes
---

**The mechanism.** `crate tag second --clear` writes the file tag only. No
filing path removes a membership that no genre files any more, but for a Soul
track's cleared R&B, whose R&B band is Soul's split place again: `adopt move`
moves a track between the bands of a bucket it claims, and with the second
genre gone the track's entry no longer claims that bucket, so the track stays
in the second folder. `crate converge` names the membership as unexpected
only while that playlist holds another track filed into it; with the track
alone there it says `matching`, the declared placements all present.

**Measured cost.** Driven at round one: after the clear, with the track alone
in Tech House / High, converge said `matching` and no warning; with another
Tech House track in that playlist it said `differing`,
`unexpected:tech_house/high`, remedy rebuild-tree. A DJ who clears a second
genre takes the track out of that folder by hand, and converge's clean report
over that state says nothing.

**Closes when:** a cleared second genre is recorded where `adopt move` reads
it (U339's `adopt/genre_moves.py`, once landed, records genre changes for this
purpose) and the move takes the track out of that folder, or converge names a
membership no genre files whatever else the playlist holds. An issue: a clean
report over state it did not read as differing (the bar's b).
