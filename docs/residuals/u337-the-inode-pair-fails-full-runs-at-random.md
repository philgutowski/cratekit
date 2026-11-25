---
title: The two inode tests of tests/test_repair_rows.py fail a full run at random on a cloud container, and read as kills
found: at the replay of U290's survey kill set, U337, 2026-11-25.
issue: no
---

**The mechanism.** `test_an_id_above_the_bound_that_is_the_files_inode_is_not_random` and `test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind` fail when run alone on these containers (both of them in three runs of three with the suite's options cleared here, one of them under the suite's own options) and fail inside a full parallel run some of the time, whatever the tree; #702 (U273) is where the battery learned they need a real disk. `cloud_battery.py baseline` records them as passing when its own full run passes them, so the driver does not subtract them, and a full run that fails one reads as a death of whatever row it measured.

**Measured cost.** On this card alone: three null controls killed by one of them (u337-librosa-1-0-0-b's first run, u337-survey-b2 and u337-survey-b2b's first run), each batch invalid and run again; seven rows read killed only by one of them in a promoted full run (u264 M7 under librosa 1.0.1; at ff8e5ec u130-a A1, r923 N12 and u28 L9 in survey a, u165 F5 in survey b1, r259 O1 and u112-b A6 in survey b2a), which `survey.py` now refuses or reads as no kill; and one subset baseline refused red (u115 F17 and F8, u272 S13, u193 M25, whose only killers they are, so those four rows are unmeasured on Linux). Helpers that added the two ids to a scratch copy of their known failures, as U334 recorded, avoided the first two costs; a hand added id is what the cloud unit skill forbids. Maintainer facing.

**Closes when:** the two tests are made deterministic on a container (or skipped where the filesystem cannot give the inode they need, named by the battery), so a full run reads them the same every time.
