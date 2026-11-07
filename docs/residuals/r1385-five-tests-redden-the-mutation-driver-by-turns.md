---
title: Five tests far from one another each reddened one mutation driver run's null control or baseline on one cloud container, and each passed alone
found: at the mutation table of #600, R-1385, 2026-11-07.
issue: no
---

**The mechanism.** Not traced. `scripts/mutate.py` runs the full suite under `-n auto` for its baseline and its null control, and on the container that built R-1385 one test failed in most runs, a different one each time, none in the card's area, each green when run alone straight after. The driver rightly refuses such a batch, so a table needs as many runs as it takes for one to come up clean.

**Measured cost.** Seven driver runs on 2026-11-07, three valid. The deaths, each once:
`tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job` (passed alone twice),
`tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot` (alone three times and with its file),
`tests/test_sync_bandcamp_native.py::test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label` (alone twice),
`tests/test_export_set.py::test_the_archive_prefixes_records_and_files_it_in_a_year_folder_made_once` (alone once),
`tests/test_outbound_workers.py::test_new_playlist_does_not_hide_a_record_the_crate_already_has`, in the baseline (alone once).
The last three came after `main` was merged in at c2e3d056, on runs that measured one row; R-1385's M7 was left at its pre-merge number after three of them. `cloud_battery.py compare` at the merged head saw none of the five fail. R-591 and R-1164 are earlier tests of the same kind.

**Closes when:** the five are run under `-n auto` with the full suite until each fails again and its cause is named, or the container's load is shown to be the cause and the driver says so. Ledger only until a sixth turns up or one fails twice.
