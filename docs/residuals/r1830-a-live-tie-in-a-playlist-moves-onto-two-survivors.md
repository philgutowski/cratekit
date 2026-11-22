---
title: Where a playlist already holds two live rows on one TrackNo, the removal's renumbering can leave two survivors tied that were apart
found: at the review of #925, R-1830, round two, 2026-11-22.
issue: no
---

**The mechanism.** `rb_writer.renumbered_positions` lowers each surviving
live row by the removed live rows strictly below it. That keeps distinct live
numbers distinct, but an input that already ties two live rows is not
distinct: with r1 at 1, the removed x and a survivor r2b both at 2, and r3 at
3, removing x leaves r2b and r3 both at 2; and two removed rows tied at 3
between survivors at 2 and 4 leave both survivors at 2. `sync pair` then
reads the tied survivors in row id order, which is random.

**Measured cost.** Not driven as a verb. Round two read two candidate
producers and neither leaves a live tie: `add_memberships` appends past the
highest number, and `playlist_pair` numbers the live rows one through N. What
rekordbox does with a tie was not measured.

**Closes when:** a producer of a live tie is found and the rule leaves such a
playlist unrenumbered, or rekordbox is measured on one. Ledger only.
