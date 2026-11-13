---
title: Seven guards of U273's places and on disk rerun kill no test
found: at the review of #702, U273, 2026-11-13.
issue: no
---

**The mechanism.** Reverted one at a time by the review, each left
`tests/test_cloud_battery.py` and `tests/test_mutation_driver.py` green:
in `scripts/cloud_battery.py`, the `stray` half of the on disk run's
acceptance (no input the review drove reaches it without `unread` firing
too), the collection error exemption in `unread`, the `os.access` write
check on the memory root, and the floor's value (halved to 3 GiB); in
`scripts/mutate.py`, the `again.collected` check after the rerun (a listed
id that is gone exits pytest 4 first), the `collect_errors` merge from the
rerun, and the `place == MEMORY` condition on the rerun widened to any
place (a disk run's rerun is a second disk run and agrees). Round one named
nine; two are pinned since, the errored replacement by
`test_a_listed_test_erroring_in_memory_and_passing_on_disk_is_read_passing`
and `run_pytest`'s own refusal of a place it cannot have by
`test_a_child_whose_place_is_gone_is_refused_rather_than_run_elsewhere`, and
so is the driver's `and known.on_disk` condition, which round two found
unpinned.

**Measured cost.** None driven: each is a defence behind another guard or a
measure no run on this container reaches. Maintainer facing.

**Closes when:** each has a test that fails without it, or is removed as
unreachable with the reason in the code.
