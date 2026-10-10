---
title: A genre folder no record binds that carries another bucket's name, or a name two folders carry, gets no Favorites
found: at the review of #276, U119, 2026-10-09, reading the folder binding.
issue: no
---

**The mechanism.** The refresh binds a bucket to its folder through the node a
previous write recorded first and by the bucket's display name only among the
folders no record claims. A folder renamed in rekordbox before any write
recorded it is bound by nothing and is listed as left alone, and so are two
live folders carrying one bucket's name, since whichever the query yielded
first is not an answer. No Favorites is written there and no track is
removed; the gate screen and the verb's note list each by name and row.

**Measured cost.** Driven by `test_a_folder_nobody_declares_and_a_name_two_folders_carry_are_left_alone`
and `test_a_folder_the_record_binds_to_one_bucket_is_not_bound_to_another_by_its_new_name`.
The author's library has every genre folder under its declared name and one
of each, so the cost is nobody's today; a rename before the first refresh
costs that folder its Favorites until a rebuild records its node.

**Closes when:** the tree rebuild, which records every node it writes, has
run once after the rename, or a person renames the folder back. Ledger
only.
