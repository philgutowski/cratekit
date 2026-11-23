# Mutation table: u325-after-l-23

Measured by `scripts/mutate.py` on 2026-11-22 23:48 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 124.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:23 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 20, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u149.T20_short_snapshot` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T7_ambiguous_takes_first` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 2 | killed |
| `u149.T8_mirror_link_skipped` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T9_removed_row_linked` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `r1694.S1_tolerance_reraises` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 7 | killed |
| `r1694.S2_tolerance_always` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 3 | killed |
| `r1694.S3_catch_everything` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 1 | killed |
| `r1694.S4_failures_no_credential` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 8 | killed |
| `r1694.S5_failures_no_cratekit` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 2 | killed |
| `r1694.S6_failures_no_oserror` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 1 | killed |
| `u55-collection-reader.R10_apply_zero_item_refusal` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 1 | killed |
| `u55-collection-reader.R12_apply_item_ids` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 25 | killed |
| `u55-collection-reader.R19_collector_groups_locations` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 1 | killed |
| `u55-collection-reader.R20_membership_locations_key` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 16 | killed |
| `u55-collection-reader.R24_worker_digest_check` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 3 | killed |
| `u55-collection-reader.R27_apply_no_tag_value` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 4 | killed |
| `u55-round-2.R23_worker_raises_on_failure` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 1 | killed |
| `u55-round-2.R8_census_prefix_map` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 1 | killed |
| `r227.V1_validator_not_called` | `src/cratekit/core/config.py` | user | 2 file(s) | 599 | 6 | killed |
| `r227.V2_no_ceiling` | `src/cratekit/core/config.py` | user | 2 file(s) | 599 | 1 | killed |
| `r227.V3_bool_is_a_day_count` | `src/cratekit/core/config.py` | user | 2 file(s) | 599 | 1 | killed |
| `u164.H1_watch_recorded` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 36 | 1 | killed |
| `u164.H2_scratch_folder` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 36 | 20 | killed |
| `u188.M10_detail_mapped_dropped` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 36 | 1 | killed |
| `u188.M11_fields_last_part` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u188.M12_fields_keep_indices` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u188.M13_fields_repeated` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u188.M7_signs_swapped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u188.M8_fields_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 1 | killed |
| `u188.M9_pairs_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 1 | killed |
| `u201-composites.C5_leave_nothing` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 195 | 6 | killed |
| `u201.O1_latch` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 195 | 1 | killed |
| `u201.O2_stale` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 195 | 1 | killed |
| `u201.O3_target_bucket` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 195 | 6 | killed |
| `u201-composites.C4_settle_none` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 195 | 3 | killed |
| `u201.L1_agreed_own_playlist` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 195 | 1 | killed |
| `u70.S2_sentinel_casefold` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 282 | 2 | killed |
| `u70.S3_sentinel_strip` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 282 | 1 | killed |
| `u70.S4_canonical_source` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 282 | 2 | killed |
| `u70.S5_source_id_recorded` | `src/cratekit/intake/cli.py` | maintainer | 2 file(s) | 282 | 1 | killed |
| `u70.S6_source_id_only_for_hearts` | `src/cratekit/intake/cli.py` | maintainer | 2 file(s) | 282 | 1 | killed |
| `u100-a.R1_slug_only_presence` | `src/cratekit/label/registry.py` | user | 4 file(s) | 22933 | 0 (promoted) | zero |
| `u100-a.R2_no_presence_check` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 6 | killed |
| `u100-a.R3_presence_before_the_batch` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 1 | killed |
| `u100-a.R4_slug_refusal_aborts` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 1 | killed |
| `u241.M13_vocal_model_not_kept_back` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M19_failed_run_does_not_say_its_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 4 | killed |
| `u241.M20_held_job_records_a_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M21_no_check_line_on_the_answer` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 12 | killed |
| `u241.M25_an_idle_resume_overwrites_the_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `r1032.A11_empty_album_narrows` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 1 | killed |
| `r1032.A1_adapter_ignores_any_agreeing` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 13 | killed |
| `r1032.A3_unreadable_tie_broken` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 3 | killed |
| `r1032.A6_first_listed_not_lowest` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 7 | killed |
| `r1032.A7_lowest_by_characters` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 1 | killed |
| `r1032.A8_album_narrow_drops_all` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 11 | killed |
| `r1032.A9_album_narrow_unfolded` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 1 | killed |
| `u216.M21_reserve_adopt_empty` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 9 | killed |
| `u216.M22_write_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 12 | killed |
| `u216.M23_read_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 12 | killed |
| `u216.M24_read_unvalidated` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 4 | killed |
| `r259.L1_job_cache_read` | `src/cratekit/label/cli.py` | maintainer | 4 file(s) | 551 | 1 | killed |
| `r504-a.A11_boundary_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 551 | 5 | killed |
| `r504-a.A12_boundary_drops_short` | `src/cratekit/label/cli.py` | user | 4 file(s) | 551 | 5 | killed |
| `u169.A1_retryable_policy_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 1 | killed |
| `u169.A2_any_permanent_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 7 | killed |
| `u169.A3_worker_never_declines` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 9 | killed |
| `u169.A4_no_declined_warning` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 4 | killed |
| `u169.A5_warning_names_failed_items` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 1 | killed |
| `u207.S1_any_client_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.S2_lone_code_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.S3_unfolded_spelling_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.S4_rate_limit_keeps_screening` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 2 | killed |
| `u207.S5_refused_form_keeps_screening` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 3 | killed |
| `u207.S6_failed_batch_read_as_empty` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 8 | killed |
| `u207.S7_failed_batch_sent_again` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 2 | killed |
| `u242.M11_strip_skips_the_held_check` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M12_composite` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 11 | killed |
| `u242.M12_strip_skips_the_migration` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 14 | killed |
| `u242.M13_strip_no_collision_with_others` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u242.M14_strip_no_collision_between_strips` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M15_strip_collision_case_exact` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M17_strip_no_recheck` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M18_strip_records_no_old_title` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 4 | killed |
| `u197.M1_config_fold` | `src/cratekit/core/config.py` | user | 3 file(s) | 815 | 2 | killed |
| `u197.M2_retired_mapping_empty` | `src/cratekit/core/config.py` | user | 3 file(s) | 815 | 4 | killed |
| `u213.M11_unreadable_said_isrc` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 3 | killed |
| `u213.M12_absent_rule` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `u213.M13_unidentified_any` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 3 | killed |
| `u213.M6_readable_refuses_nameless` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 2 | killed |
| `u213.M8_readable_unread_excludes_read` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `u213.M9_readable_order_holds_unread` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 3 | killed |
| `u132.W1_every_apply` | `src/cratekit/adopt/apply_cli.py` | user | 10 file(s) | 515 | 1 | killed |
| `u132.W2_coded_note` | `src/cratekit/adopt/apply_cli.py` | user | 10 file(s) | 515 | 3 | killed |
| `u132.W3_version_from_report` | `src/cratekit/adopt/apply_cli.py` | user | 10 file(s) | 515 | 1 | killed |
| `u79-c.C3_accepted_held_listed_again` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 1 | killed |
| `u79-c.C4_nothing_found_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 2 | killed |
| `u79-c.C5_foreign_ref_names_a_row` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 2 | killed |
| `u79-c.C6_isrc_named_keeps_origin` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 1 | killed |
| `u79-c.C7_fixed_name` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 10 | killed |
| `u79-c.C8_asked_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 1 | killed |
| `sitting3.G8_queue_skips_readiness` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 2 | killed |

## Zero rows and what they owe

- `u100-a.R1_slug_only_presence` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u149.T20_short_snapshot`

pair_backfilled: record the account snapshot when the listing was short

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T20_short_snapshot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_short_listing_pairs_the_twin_with_no_snapshot`

Old text:

```
            account=list(one.account) if one.whole else None,
```

New text:

```
            account=list(one.account),
```

### `u149.T7_ambiguous_takes_first`

matched: take the first of several library rows, so an ambiguous track is guessed

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T7_ambiguous_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_account_track_two_library_rows_carry_is_named_and_neither_is_guessed`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        if len(found) == 1:
```

New text:

```
        if found:
```

### `u149.T8_mirror_link_skipped`

Library.find: skip the mirror's link to the very track, so the database ISRC decides

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T8_mirror_link_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_mirrors_link_to_a_track_wins_and_a_link_to_a_removed_row_falls_through`

Old text:

```
            self.by_remote.get(remote_id, ()),
```

New text:

```
            (),
```

### `u149.T9_removed_row_linked`

_grouped: drop the live filter, so a mirror link to a removed row is an answer

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T9_removed_row_linked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_mirrors_link_to_a_track_wins_and_a_link_to_a_removed_row_falls_through`

Old text:

```
        if key and content_id in alive and content_id not in found.setdefault(key, []):
```

New text:

```
        if key and content_id not in found.setdefault(key, []):
```

### `r1694.S1_tolerance_reraises`

materialised_session: re-raise a store failure handed to the tolerance, so a refreshed login on the opt in fails the verb again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S1_tolerance_reraises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
            except STORE_FAILURES as exc:
                unstored(exc)

```

New text:

```
            except STORE_FAILURES as exc:
                raise

```

### `r1694.S2_tolerance_always`

materialised_session: tolerate a store failure even when no callback was given, so the drive's own catch and streamrip's scope lose their failure

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S2_tolerance_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_scope_that_asked_for_no_tolerance_still_raises_its_write_back_failure`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        if unstored is None:
            write_back(name, path, codec=codec, stored=payload)
        else:

```

New text:

```
        if False:
            write_back(name, path, codec=codec, stored=payload)
        else:
            unstored = unstored or (lambda exc: None)

```

### `r1694.S3_catch_everything`

materialised_session: catch every exception at the write back, so a defect in the write is a warning rather than a raise

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S3_catch_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_defect_in_the_write_back_still_raises`

Old text:

```
            except STORE_FAILURES as exc:
                unstored(exc)

```

New text:

```
            except Exception as exc:
                unstored(exc)

```

### `r1694.S4_failures_no_credential`

STORE_FAILURES: drop the credential errors, so the keychain's own refusal on the opt in fails the login and the drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S4_failures_no_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 8 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_leaves_a_park_its_own_cause`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    CratekitError,
    OSError,
)
```

### `r1694.S5_failures_no_cratekit`

STORE_FAILURES: drop CratekitError, so an index the write could not read fails the login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S5_failures_no_cratekit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    secrets.CredentialError,
    OSError,
)
```

### `r1694.S6_failures_no_oserror`

STORE_FAILURES: drop OSError, so an index file the write could not make fails the login and the drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S6_failures_no_oserror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    secrets.CredentialError,
    CratekitError,
)
```

### `u55-collection-reader.R10_apply_zero_item_refusal`

The apply queues a job with one item over a plan that can place nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R10_apply_zero_item_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 81 against a baseline of 81
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`

Old text:

```
    if not applicable:
```

New text:

```
    if False:
```

### `u55-collection-reader.R12_apply_item_ids`

The apply enqueues with no items at all

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R12_apply_item_ids`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 81 against a baseline of 81
- Kills: 25 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_the_resume_the_job_driver_spawns_can_actually_proceed`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_drive_that_adds_nothing_still_names_an_undeclared_favorites_class`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_registry_naming_a_root_the_library_does_not_have_is_its_own_refusal`
  - `tests/test_adopt_workers.py::test_a_renamed_vocal_playlist_gains_no_second_one_beside_it`
  - `tests/test_adopt_workers.py::test_a_second_approved_apply_adds_nothing_and_withholds_the_same`
  - `tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`
  - `tests/test_adopt_workers.py::test_a_track_in_the_planned_sub_under_another_name_is_withheld_not_doubled`
  - `tests/test_adopt_workers.py::test_a_track_moved_after_the_approval_is_a_stale_decision`
  - `tests/test_adopt_workers.py::test_a_track_tagged_after_the_approval_is_a_stale_decision`
  - `tests/test_adopt_workers.py::test_a_track_the_tree_write_could_not_place_is_never_marked_applied`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - ... and 10 more, see the JSON sidecar

Old text:

```
            item_ids=(plan.digest(),),
```

New text:

```
            item_ids=(),
```

### `u55-collection-reader.R19_collector_groups_locations`

The collector groups content identifiers again, which is the seam defect U55 found

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R19_collector_groups_locations`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 81 against a baseline of 81
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_memberships_are_collected_and_match_what_the_loop_reached`

Old text:

```
            into.setdefault((folder, sub), []).append(entry.path)
```

New text:

```
            into.setdefault((folder, sub), []).append(entry.content_id)
```

### `u55-collection-reader.R20_membership_locations_key`

The written mapping groups content identifiers, so the write matches nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R20_membership_locations_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 81 against a baseline of 81
- Kills: 16 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_memberships_are_collected_and_match_what_the_loop_reached`
  - `tests/test_adopt_workers.py::test_a_drive_that_adds_nothing_still_names_an_undeclared_favorites_class`
  - `tests/test_adopt_workers.py::test_a_renamed_vocal_playlist_gains_no_second_one_beside_it`
  - `tests/test_adopt_workers.py::test_a_second_approved_apply_adds_nothing_and_withholds_the_same`
  - `tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`
  - `tests/test_adopt_workers.py::test_a_track_in_the_planned_sub_under_another_name_is_withheld_not_doubled`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`
  - `tests/test_adopt_workers.py::test_the_apply_writes_no_tag_and_leaves_every_file_byte_identical`
  - `tests/test_adopt_workers.py::test_the_approving_actor_travels_in_the_payload`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        grouped.setdefault((folder, sub), []).append(entry.path)
```

New text:

```
        grouped.setdefault((folder, sub), []).append(entry.content_id)
```

### `u55-collection-reader.R24_worker_digest_check`

The worker applies a plan nobody approved, because the frozen digest is not compared

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R24_worker_digest_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 81 against a baseline of 81
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_track_moved_after_the_approval_is_a_stale_decision`
  - `tests/test_adopt_workers.py::test_a_track_tagged_after_the_approval_is_a_stale_decision`

Old text:

```
    if plan.digest() != frozen_digest:
```

New text:

```
    if False:
```

### `u55-collection-reader.R27_apply_no_tag_value`

A tag_value supplier is installed, so the apply writes a genre onto the person's files

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R27_apply_no_tag_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 81 against a baseline of 81
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_drive_that_adds_nothing_still_names_an_undeclared_favorites_class`
  - `tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_the_apply_writes_no_tag_and_leaves_every_file_byte_identical`

Old text:

```
    report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)
```

New text:

```
    report, gathered = apply_outstanding(
        cfg, plan, declared, actor=actor, tag_value=lambda entry, _d: entry.bucket or None
    )
```

### `u55-round-2.R23_worker_raises_on_failure`

A failed apply returns rather than raising, so the job reaches SUCCEEDED over nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-round-2.json`, row `R23_worker_raises_on_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 81 against a baseline of 81
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`

Old text:

```
    if report.failed:
        _commit(produced)
        raise refuse(
```

New text:

```
    if False:
        _commit(produced)
        raise refuse(
```

### `u55-round-2.R8_census_prefix_map`

The census drops the configured volume rewrites, so an older volume name resolves nowhere

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-round-2.json`, row `R8_census_prefix_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 81 against a baseline of 81
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`

Old text:

```
            prefix_map=collection.prefix_rules(cfg),
        )
    )
```

New text:

```
            prefix_map=(),
        )
    )
```

### `r227.V1_validator_not_called`

validate never asks about outbound.export_stale_days

- File: `src/cratekit/core/config.py`
- Source: `r227.json`, row `V1_validator_not_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/modules/test_reports.py`
- Collected: 599 against a baseline of 599
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_an_export_staleness_nobody_could_mean_is_refused_with_its_ceiling`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[-3]`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[0]`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[2.5]`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[True]`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[seven]`

Old text:

```
    problems += _validate_export_staleness(data)

```

New text:

```
(empty)
```

### `r227.V2_no_ceiling`

The key has no ceiling, so ten billion days validates and overflows later

- File: `src/cratekit/core/config.py`
- Source: `r227.json`, row `V2_no_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/modules/test_reports.py`
- Collected: 599 against a baseline of 599
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_an_export_staleness_nobody_could_mean_is_refused_with_its_ceiling`

Old text:

```
        maximum=MAX_EXPORT_STALE_DAYS,
```

New text:

```
        maximum=None,
```

### `r227.V3_bool_is_a_day_count`

The shared day count rule accepts a boolean, for the intake ages as well

- File: `src/cratekit/core/config.py`
- Source: `r227.json`, row `V3_bool_is_a_day_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/modules/test_reports.py`
- Collected: 599 against a baseline of 599
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[True]`

Old text:

```
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        return (
```

New text:

```
    if not isinstance(value, int) or value < 1:
        return (
```

### `u164.H1_watch_recorded`

_filed_watch: watch today's year folder alone, never the recorded folder

- File: `src/cratekit/intake/land_cli.py`
- Source: `u164.json`, row `H1_watch_recorded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`

Old text:

```
        watched.extend((Path(again).parent, Path(again)))
```

New text:

```
        pass
```

### `u164.H2_scratch_folder`

_rehearse_in: map the scratch plan back from the live folder instead of its own

- File: `src/cratekit/intake/land_cli.py`
- Source: `u164.json`, row `H2_scratch_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 20 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_copy_that_fails_its_integrity_check_is_refused_naming_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`
  - `tests/test_intake_land_rehearse.py::test_a_refusal_inside_the_rehearsal_keeps_its_reason_and_names_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_beside_another_runs_area_lands_and_leaves_that_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_fails_otherwise_is_still_a_failed_check`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_finds_no_room_is_refused_under_the_room_slug`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_the_music_folder_and_the_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_of_another_batch_is_not_the_one_compared`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        scratch_target = _folder(scratch_rows)
```

New text:

```
        scratch_target = landing.target_dir(area.cfg, planned.batch)
```

### `u188.M10_detail_mapped_dropped`

_rehearse_in: carry no mapped pairs in the refusal's detail

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M10_detail_mapped_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
                detail={"differs": differ, "mapped": [list(pair) for pair in pairs]},
```

New text:

```
                detail={"differs": differ},
```

### `u188.M11_fields_last_part`

_fields_of: name a field by its last part alone, so a vox row's path reads as rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M11_fields_last_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`
  - `tests/test_intake_land_rehearse.py::test_the_refusal_names_each_field_once_and_strips_every_index`

Old text:

```
        names.append(path.split(".", 1)[-1])
```

New text:

```
        names.append(path.rsplit(".", 1)[-1])
```

### `u188.M12_fields_keep_indices`

_fields_of: keep the indices, so one field is named once per row

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M12_fields_keep_indices`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`
  - `tests/test_intake_land_rehearse.py::test_the_refusal_names_each_field_once_and_strips_every_index`

Old text:

```
        path = re.sub(r"\[\d+\]", "", line[2:].split(" = ", 1)[0])
```

New text:

```
        path = line[2:].split(" = ", 1)[0]
```

### `u188.M13_fields_repeated`

_fields_of: keep every repeat, so a field ten rows differ in is named ten times

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M13_fields_repeated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`
  - `tests/test_intake_land_rehearse.py::test_the_refusal_names_each_field_once_and_strips_every_index`

Old text:

```
    return list(dict.fromkeys(names))


def _place_owned(
```

New text:

```
    return names


def _place_owned(
```

### `u188.M7_signs_swapped`

_rehearse_in: compare live first, so a minus line is the live plan's and the refusal's legend is false

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M7_signs_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_that_is_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
        differ = rehearsal.differing(back, lines)
```

New text:

```
        differ = rehearsal.differing(lines, back)
```

### `u188.M8_fields_left_out`

_rehearse_in: name no field in the refusal

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M8_fields_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
f"{len(differ)} line(s), in {', '.join(_fields_of(differ))}, so nothing "
```

New text:

```
f"{len(differ)} line(s), in the plan, so nothing "
```

### `u188.M9_pairs_left_out`

_rehearse_in: state no pair in the refusal, so the spellings compared are not named

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M9_pairs_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
                + ", ".join(f"{scratch} to {live}" for scratch, live in pairs)
```

New text:

```
                + "the area's paths"
```

### `u201-composites.C5_leave_nothing`

plan: a move leaves no tree playlist, the thing O4 narrows

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201-composites.json`, row `C5_leave_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_mirror_made_before_u201_is_agreed_by_its_first_run_and_an_edit_after_it_is_taken`
  - `tests/test_organize_mirror_edits.py::test_a_move_to_unsorted_clears_the_energy`
  - `tests/test_organize_mirror_edits.py::test_a_move_within_a_genre_keeps_the_genre_and_moves_the_energy_to_the_nearest`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
            leave_ids = [pid for pid in held if pid not in wanted and routed(tree.names[pid])]
```

New text:

```
            leave_ids = []
```

### `u201.O1_latch`

write: the tree's convergence latch is not asked

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O1_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_tree_the_product_latched_refuses_the_write_before_any_file_is_tagged`

Old text:

```
        convergence.assert_tree_writable(cfg, db, tree_id, registry)
```

New text:

```
        pass
```

### `u201.O2_stale`

_stale: a library moved since the plan is written

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O2_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`

Old text:

```
    if approved.identity() != now.identity():
```

New text:

```
    if False:
```

### `u201.O3_target_bucket`

target_tags: a genre word filing into another bucket is taken

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O3_target_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_mirror_made_before_u201_is_agreed_by_its_first_run_and_an_edit_after_it_is_taken`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Minimal / Deep Tech-Low Energy-Deep House-9-expected6]`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Tech House-Med-Deep House-2-expected0]`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Tech House-None-Deep House-5-expected4]`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
        if routing.resolve_bucket(declared, word).bucket_id != bucket_id:
```

New text:

```
        if False:
```

### `u201-composites.C4_settle_none`

settle_mirror_tracks: the library step settles nothing, the thing L2 narrows

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u201-composites.json`, row `C4_settle_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
    wanted = list(settled)
```

New text:

```
    wanted = []
```

### `u201.L1_agreed_own_playlist`

record_mirror_agreed: a snapshot lands on a playlist recorded under the title with another identifier

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u201.json`, row `L1_agreed_own_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
            if not entry or str(entry.get("remote_id") or "") != str(remote_id):
                continue
            base =
```

New text:

```
            if not entry:
                continue
            base =
```

### `u70.S2_sentinel_casefold`

The sentinel is compared case sensitively, so Favorites is read as a playlist reference

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S2_sentinel_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 282 against a baseline of 282
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[ FAVORITES ]`
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[Favorites]`

Old text:

```
    return str(reference or "").strip().casefold() == FAVORITES
```

New text:

```
    return str(reference or "").strip() == FAVORITES
```

### `u70.S3_sentinel_strip`

The sentinel is compared unstripped, so a padded favorites is read as a playlist reference

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S3_sentinel_strip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[ FAVORITES ]`

Old text:

```
    return str(reference or "").strip().casefold() == FAVORITES
```

New text:

```
    return str(reference or "").casefold() == FAVORITES
```

### `u70.S4_canonical_source`

The job records the reference as typed rather than the canonical favorites, so the resume argv carries the typed spelling

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S4_canonical_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 282 against a baseline of 282
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[ FAVORITES ]`
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[Favorites]`

Old text:

```
        if hearts:
            reference = FAVORITES
        found = catalogue.resolve(cfg)
```

New text:

```
        found = catalogue.resolve(cfg)
```

### `u70.S5_source_id_recorded`

A hearts job is queued with no source_id, so nothing can tell it from a playlist job

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S5_source_id_recorded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_and_never_asks_for_a_playlist`

Old text:

```
            source_id=FAVORITES_SOURCE_ID if hearts else None,
```

New text:

```
            source_id=None,
```

### `u70.S6_source_id_only_for_hearts`

Every playlist job is stamped source_id favorites, so a playlist reads as the hearts listing

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S6_source_id_only_for_hearts`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_playlist_reference_still_reaches_the_playlist_and_not_the_hearts`

Old text:

```
            source_id=FAVORITES_SOURCE_ID if hearts else None,
```

New text:

```
            source_id=FAVORITES_SOURCE_ID,
```

### `u100-a.R1_slug_only_presence`

RegistryStore.adopt checks presence by slug alone, the R-381 hazard: a label held under sueno is filed again as sue-o

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R1_slug_only_presence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = Registry(labels=current).by_id(label_id)
```

### `u100-a.R2_no_presence_check`

RegistryStore.adopt never finds a label present, so every accepted name is written over the held entry

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R2_no_presence_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[case]`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[padding]`
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
                if held is not None:
                    results.append(
```

New text:

```
                if False:
                    results.append(
```

### `u100-a.R3_presence_before_the_batch`

RegistryStore.adopt resolves against the file as loaded, not the entries this run already added, so two spellings in one run both add

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R3_presence_before_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = self.load().resolve(name)
```

### `u100-a.R4_slug_refusal_aborts`

a name that yields no identifier is no longer caught per name, so it aborts the whole adopt

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R4_slug_refusal_aborts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
                except CratekitError as exc:
                    results.append(
```

New text:

```
                except KeyError as exc:
                    results.append(
```

### `u241.M13_vocal_model_not_kept_back`

_open_ahead: the driver's vocal model is not kept back from the light pool's budget

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M13_vocal_model_not_kept_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_memory_overrules_a_wide_core_count`

Old text:

```
        reserve += vocals.VOCAL_WORKER_BYTES
    return ahead.open_session(
```

New text:

```
        pass
    return ahead.open_session(
```

### `u241.M19_failed_run_does_not_say_its_pool`

_resume: a run that failed or was stopped leaves without its pool line

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M19_failed_run_does_not_say_its_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_run_that_fails_part_way_says_its_pool_on_the_refusal_and_matches_the_serial_run`
  - `tests/test_analysis_ahead.py::test_an_interrupt_during_a_run_ahead_ends_the_workers_and_the_resume_finishes`
  - `tests/test_analysis_ahead.py::test_an_unreadable_calibration_is_each_items_refusal_and_opens_no_pool`

Old text:

```
                if pooled is None:
                    raise
                raise _with_pool(failed, pooled) from failed

```

New text:

```
                raise

```

### `u241.M20_held_job_records_a_pool`

_heads_ahead: a call that drove nothing, because another driver holds the job, records a pool anyway

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M20_held_job_records_a_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_job_another_driver_holds_records_no_pool_and_adds_none_to_the_refusal`

Old text:

```
        drove = False
        raise

```

New text:

```
        raise

```

### `u241.M21_no_check_line_on_the_answer`

_resume: the answer no longer carries the analyze.pool check

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M21_no_check_line_on_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 12 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_closure_bound_by_a_test_is_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_healthy_machine_says_how_many_workers_and_that_the_ceiling_held_it`
  - `tests/test_analysis_ahead.py::test_a_job_whose_record_is_gone_says_it_does_not_know`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_a_pool_record_that_cannot_be_written_is_a_missing_line_and_never_a_failed_job`
  - `tests/test_analysis_ahead.py::test_a_resume_of_a_finished_job_still_says_what_pool_it_ran_with`
  - `tests/test_analysis_ahead.py::test_a_worker_that_dies_costs_the_run_nothing_but_its_pool`
  - `tests/test_analysis_ahead.py::test_memory_overrules_a_wide_core_count`
  - `tests/test_analysis_ahead.py::test_the_person_reads_the_check_line_without_asking_for_json`
  - `tests/test_analysis_ahead.py::test_two_cores_leave_no_ceiling_for_a_pool`

Old text:

```
            summary["checks"] = [_pool_check(artifacts.pool_record(cfg, job.job_id))]

```

New text:

```
(empty)
```

### `u241.M25_an_idle_resume_overwrites_the_pool`

_worth_recording: a drive that measured nothing overwrites the record of the drive that did

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M25_an_idle_resume_overwrites_the_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_resume_with_nothing_left_to_measure_keeps_the_pool_that_measured_the_job`

Old text:

```
        return True
    return artifacts.pool_record(cfg, job_id) is None

```

New text:

```
        return True
    return True

```

### `r1032.A11_empty_album_narrows`

_on_album: drop the empty tag guard, so a file with no album narrows a tie to the releases the provider left unnamed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A11_empty_album_narrows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`

Old text:

```
        remote for remote in remotes if wanted and match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
        remote for remote in remotes if match.fold(_album_name(tracks[remote])) == wanted
```

### `r1032.A1_adapter_ignores_any_agreeing`

match_track: drop any_agreeing on its way to _among, so the adapter refuses the tie for the mirror too

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A1_adapter_ignores_any_agreeing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
- Kills: 13 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_organize_mirror_tie.py::test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
  - `tests/test_organize_mirror_tie.py::test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_none_of_the_tied_releases_still_takes_one`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_take_the_lower_hearted_one_never_an_unhearted_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
                        any_agreeing=any_agreeing,
```

New text:

```
                        any_agreeing=False,
```

### `r1032.A3_unreadable_tie_broken`

_among: break a tie beside a candidate that could not be read

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A3_unreadable_tie_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`
  - `tests/test_outbound_tidal_account.py::test_a_refused_tie_is_never_said_to_be_broken`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_release_beside_the_tie_still_refuses_with_any_agreeing`

Old text:

```
        if any_agreeing and not unreadable:
```

New text:

```
        if any_agreeing:
```

### `r1032.A6_first_listed_not_lowest`

_lowest: take the first the provider lists, so the choice moves with the listing order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A6_first_listed_not_lowest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
- Kills: 7 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
    return min(remotes, key=lambda remote: (len(remote), remote))
```

New text:

```
    return remotes[0]
```

### `r1032.A7_lowest_by_characters`

_lowest: order the identifiers as text, so 100 sorts before 99

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A7_lowest_by_characters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`

Old text:

```
    return min(remotes, key=lambda remote: (len(remote), remote))
```

New text:

```
    return min(remotes)
```

### `r1032.A8_album_narrow_drops_all`

_on_album: when the album names none, answer the named list alone, empty

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A8_album_narrow_drops_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
- Kills: 11 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_organize_mirror_tie.py::test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
  - `tests/test_organize_mirror_tie.py::test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_none_of_the_tied_releases_still_takes_one`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_take_the_lower_hearted_one_never_an_unhearted_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
    return named or remotes
```

New text:

```
    return named
```

### `r1032.A9_album_narrow_unfolded`

_on_album: compare the album unfolded, so case and spacing defeat the narrowing

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A9_album_narrow_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_files_album_narrows_a_tie_under_the_products_own_fold`

Old text:

```
        remote for remote in remotes if wanted and match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
        remote for remote in remotes if wanted and _album_name(tracks[remote]) == album
```

### `u216.M21_reserve_adopt_empty`

reserve_folder: an adoption records an empty set whatever the plan listed

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M21_reserve_adopt_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_an_adoption_whose_plan_did_not_say_what_it_held_is_recorded_as_unknown`
  - `tests/test_sync_pair_adopted.py::test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                before = (
                    None if held is None else frozenset(str(one) for one in held if str(one))
                )
```

New text:

```
                before = frozenset()
```

### `u216.M22_write_drops_held`

_write: the folder record is written without what it held

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M22_write_drops_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_folder_record_keeps_what_it_held_through_another_write`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_a_created_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                    **({"held": sorted(one.held)} if one.held is not None else {}),
```

New text:

```
                    **({}),
```

### `u216.M23_read_drops_held`

_folders: what a folder held is never read back

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M23_read_drops_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_folder_record_keeps_what_it_held_through_another_write`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_a_created_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                None if held is None else frozenset(held),
            )
```

New text:

```
                None,
            )
```

### `u216.M24_read_unvalidated`

_folders: what a folder held is read without checking it is playlist ids

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M24_read_unvalidated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[a]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held1]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held2]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held3]`

Old text:

```
            if held is not None and (
                not isinstance(held, list) or not all(isinstance(one, str) and one for one in held)
            ):
```

New text:

```
            if False:
```

### `r259.L1_job_cache_read`

The worker never reuses the job's library view, one walk per label

- File: `src/cratekit/label/cli.py`
- Source: `r259.json`, row `L1_job_cache_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_of_two_labels_walks_the_library_once`

Old text:

```
        held = _JOB_LIBRARY.get(key)
```

New text:

```
        held = None
```

### `r504-a.A11_boundary_refuses`

The verb boundary no longer catches the shortfall, so it is refused as an unreadable listing

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A11_boundary_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    except catalogue.HeartsShortfall as short:
        return list(short.rows), short

```

New text:

```
(empty)
```

### `r504-a.A12_boundary_drops_short`

The verb boundary keeps the rows and drops the shortfall, passing the short listing off as the account

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A12_boundary_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        return list(short.rows), short
```

New text:

```
        return list(short.rows), None
```

### `u169.A1_retryable_policy_declined`

refused_for_good: drop the retryable clause, so a retryable policy refusal is skipped

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A1_retryable_policy_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_only_a_permanent_cause_in_the_policy_class_is_refused_for_good`

Old text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY and not cause.retryable
```

New text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY
```

### `u169.A2_any_permanent_declined`

refused_for_good: drop the policy class, so any permanent failure (output-exists) is skipped

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A2_any_permanent_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 7 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it`
  - `tests/test_acquire_workers.py::test_only_a_permanent_cause_in_the_policy_class_is_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY and not cause.retryable
```

New text:

```
    return not cause.retryable
```

### `u169.A3_worker_never_declines`

handle: re-raise a policy refusal instead of declining it, the base's behaviour

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A3_worker_never_declines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 9 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_label_sync_go.py::test_a_go_job_whose_track_was_refused_for_good_is_not_resumed`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
            raise jobs.Declined(exc.cause) from exc
```

New text:

```
            raise
```

### `u169.A4_no_declined_warning`

drive_queued: add no warning for the skipped tracks

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A4_no_declined_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`

Old text:

```
    warnings = (*warnings, *declined_warnings(store, job))
```

New text:

```
    warnings = tuple(warnings)
```

### `u169.A5_warning_names_failed_items`

declined_warnings: name every item with a cause, failed ones included (unreachable through the verb, which refuses a failed job before its warnings; killed at the function)

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A5_warning_names_failed_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`

Old text:

```
        if item.state is not jobs.ItemState.SKIPPED or item.cause is None:
```

New text:

```
        if item.cause is None:
```

### `u207.S1_any_client_screened`

screen: ask any client with an isrcs_held member, not only the app catalogue, so a stand in that answers an empty set marks every code absent

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S1_any_client_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_stand_in_for_the_client_is_never_screened_whatever_it_answers`

Old text:

```
        if self._stopped or not isinstance(client, catalogue_api.AppCatalogue):
            return 0
```

New text:

```
        if self._stopped or not callable(getattr(client, "isrcs_held", None)):
            return 0
```

### `u207.S2_lone_code_screened`

screen: a batch of one code is screened, paying a request its own lookup would have answered

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S2_lone_code_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_lone_code_is_never_screened_since_its_own_lookup_costs_the_same`

Old text:

```
MIN_BATCH = 2
```

New text:

```
MIN_BATCH = 1
```

### `u207.S3_unfolded_spelling_screened`

screen: a spelling that is not its own fold enters a batch, so a lowercase code is screened under its fold

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S3_unfolded_spelling_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_malformed_code_or_a_spelling_not_its_own_fold_never_enters_a_batch`

Old text:

```
            if code and code == match.isrc_token(code) and code not in self._asked
```

New text:

```
            if code and match.isrc_token(code) and code not in self._asked
```

### `u207.S4_rate_limit_keeps_screening`

screen: a rate limit or a rejected app credential on a batch leaves the screening running, so every later batch is sent into it

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S4_rate_limit_keeps_screening`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_rate_limit_on_a_batch_is_counted_marks_nothing_and_stops_the_screening`
  - `tests/test_isrc_screen.py::test_a_rejected_app_credential_on_a_batch_marks_nothing_and_stops_the_screening`

Old text:

```
            except (catalogue_api.CatalogueRateLimited, catalogue_api.AppCredentialsRejected):
                self._stopped = True
                break
```

New text:

```
            except (catalogue_api.CatalogueRateLimited, catalogue_api.AppCredentialsRejected):
                continue
```

### `u207.S5_refused_form_keeps_screening`

screen: a 4xx refusal of the request form does not stop the screening

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S5_refused_form_keeps_screening`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[400]`
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[404]`
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[422]`

Old text:

```
                if exc.status is not None and 400 <= exc.status < 500:
```

New text:

```
                if exc.status is not None and 400 <= exc.status < 400:
```

### `u207.S6_failed_batch_read_as_empty`

screen: a batch the API could not answer is read as an empty answer, so every code in it is answered not found

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S6_failed_batch_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 8 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_failed_batch_does_not_stop_the_next_one`
  - `tests/test_isrc_screen.py::test_a_server_error_on_a_batch_falls_back_to_singles_and_finds_the_one_bad_answer`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[a-code-not-asked]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[no-isrc]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[no-list]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[not-a-resource]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[paged]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[unreadable-isrc]`

Old text:

```
                continue
            self._absent.update(code for code in batch if code not in held)
```

New text:

```
                held = frozenset()
            self._absent.update(code for code in batch if code not in held)
```

### `u207.S7_failed_batch_sent_again`

screen: a batch's codes are marked asked only once it answered, so a failed batch is sent again by the next plan

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S7_failed_batch_sent_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_batch_that_failed_is_not_sent_again_by_the_next_plan`
  - `tests/test_isrc_screen.py::test_a_code_already_screened_is_not_sent_again`

Old text:

```
            self._asked.update(batch)
            made += 1
```

New text:

```
            made += 1
```

### `u242.M11_strip_skips_the_held_check`

strip: rename without confirming the record holds each planned playlist

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M11_strip_skips_the_held_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_no_rename_is_made_for_a_playlist_the_record_does_not_hold`

Old text:

```
    unheld = [identity for identity in planned if identity not in held]
```

New text:

```
    unheld = []
```

### `u242.M12_composite`

strip: neither record first nor confirm the hold, so a stripped playlist is in no record

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M12_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 11 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes`
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_no_rename_is_made_for_a_playlist_the_record_does_not_hold`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
    unheld = [identity for identity in planned if identity not in held]
```

New text:

```
    held = record.taken_ids()
    unheld = []
```

### `u242.M12_strip_skips_the_migration`

strip: rename without recording the prefixed playlists as taken first

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M12_strip_skips_the_migration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 14 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes`
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_a_title_changed_since_the_plan_is_not_renamed`
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_playlist_narrows_and_refuses_a_playlist_with_no_prefix`
  - `tests/test_u242_taken.py::test_the_strip_records_each_old_title_before_its_rename`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_is_put_back_renames_back`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
```

New text:

```
    held = record.taken_ids()
```

### `u242.M13_strip_no_collision_with_others`

strip plan: never refuse a stripped title another playlist already carries

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M13_strip_no_collision_with_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_the_gate_screen_lists_every_rename_and_every_refusal`

Old text:

```
        clash = others.get(to.casefold())
```

New text:

```
        clash = None
```

### `u242.M14_strip_no_collision_between_strips`

strip plan: never refuse two prefixed playlists stripped to one title

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M14_strip_no_collision_between_strips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`

Old text:

```
        twins = sorted(prefixed[one] for one in writes[to.casefold()] if one != identity)
```

New text:

```
        twins = []
```

### `u242.M15_strip_collision_case_exact`

strip plan: compare titles case exactly, so Techno beside techno is renamed

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M15_strip_collision_case_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_the_gate_screen_lists_every_rename_and_every_refusal`

Old text:

```
            others.setdefault(name.strip().casefold(), name)
```

New text:

```
            others.setdefault(name.strip(), name)
```

### `u242.M17_strip_no_recheck`

strip apply: rename a playlist retitled since the plan was shown

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M17_strip_no_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_title_changed_since_the_plan_is_not_renamed`

Old text:

```
            if now.get(identity) != item["name"]:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME
```

New text:

```
            if False:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME
```

### `u242.M18_strip_records_no_old_title`

strip apply: rename without recording the old title, so unmark cannot put it back

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M18_strip_records_no_old_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_the_strip_records_each_old_title_before_its_rename`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_is_put_back_renames_back`

Old text:

```
            record.record_marked(PASS, {identity: (item["name"], item["to"])})
            remote.rename_playlist(identity, item["to"])
```

New text:

```
            remote.rename_playlist(identity, item["to"])
```

### `u197.M1_config_fold`

_acquisition: return the section as written, so a file naming the retired key reaches doctor and every report under it

- File: `src/cratekit/core/config.py`
- Source: `u197.json`, row `M1_config_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_adapter_contract.py`
- Collected: 815 against a baseline of 815
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_file_naming_the_retired_adapter_key_reads_back_as_the_current_one`
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`

Old text:

```
    current = current_adapter_name(built.adapter)
    if current == built.adapter:
        return built
```

New text:

```
    current = current_adapter_name(built.adapter)
    if True:
        return built
```

### `u197.M2_retired_mapping_empty`

RETIRED_ADAPTER_NAMES: forget the vendored downloader's old key, so an older configuration names an unknown adapter

- File: `src/cratekit/core/config.py`
- Source: `u197.json`, row `M2_retired_mapping_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_adapter_contract.py`
- Collected: 815 against a baseline of 815
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_retired_vendored_key_resolves_to_the_same_adapter`
  - `tests/test_config.py::test_a_file_naming_the_retired_adapter_key_reads_back_as_the_current_one`
  - `tests/test_config.py::test_only_a_retired_adapter_key_is_folded`
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`

Old text:

```
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({"tidal_dl_ng": "vendored"})
```

New text:

```
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({})
```

### `u213.M11_unreadable_said_isrc`

Unreadable.said: name the track with no ISRC, so the backfill cannot find it by its code

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M11_unreadable_said_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 154 against a baseline of 154
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        return {"artist": self.artist, "title": self.title, "isrc": self.isrc}
```

New text:

```
        return {"artist": self.artist, "title": self.title, "isrc": ""}
```

### `u213.M12_absent_rule`

_absent: name the missing half by the artist alone, the rule the review replaced, so a row with neither says no artist

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M12_absent_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_aside_track_names_the_half_the_reader_names`

Old text:

```
    return "artist" if match.split_title(title)[0] else "title"
```

New text:

```
    return "artist" if title else "title"
```

### `u213.M13_unidentified_any`

_refuse_unidentified: refuse only when more than one row carries no id

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M13_unidentified_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 154 against a baseline of 154
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_heart_without_an_identifier_is_refused_by_position`
  - `tests/intake/test_workers.py::test_a_provider_row_without_an_identifier_is_refused_by_position`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`

Old text:

```
    if missing:
        raise _unusable(
```

New text:

```
    if len(missing) > 1:
        raise _unusable(
```

### `u213.M6_readable_refuses_nameless`

list_playlist_readable: drop the refusal of a row carrying no provider id, so it is silently dropped from the listing

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M6_readable_refuses_nameless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 154 against a baseline of 154
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_still_refuses_a_row_carrying_no_id_by_position`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`

Old text:

```
    _refuse_unidentified(nameless)
    tracks = frozen_rows(tuple(read))
```

New text:

```
    tracks = frozen_rows(tuple(read))
```

### `u213.M8_readable_unread_excludes_read`

list_playlist_readable: keep a track as unread even when another row of it read

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M8_readable_unread_excludes_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_track_one_row_of_which_reads_is_read_and_not_set_aside`

Old text:

```
    unread = {ref: one for ref, one in refused.items() if ref not in tracks}
```

New text:

```
    unread = dict(refused)
```

### `u213.M9_readable_order_holds_unread`

list_playlist_readable: order only the tracks that read, so a twin's snapshot drops the unread track

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M9_readable_order_holds_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 154 against a baseline of 154
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        order.setdefault(ref, None)
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
```

New text:

```
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
            order.setdefault(ref, None)
```

### `u132.W1_every_apply`

The adoption runs the Favorites step only when it filed a track

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W1_every_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_organize.py`
- Collected: 515 against a baseline of 515
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_drive_that_adds_nothing_still_names_an_undeclared_favorites_class`

Old text:

```
 or genre_favorites.favorites_class(declared) is None
```

New text:

```
(empty)
```

### `u132.W2_coded_note`

A skip over an undeclared class carries favorites-skipped, not its cause code

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W2_coded_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_organize.py`
- Collected: 515 against a baseline of 515
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_drive_that_adds_nothing_still_names_an_undeclared_favorites_class`
  - `tests/test_genre_favorites.py::test_the_undeclared_note_states_the_version_the_skip_saw`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
    if skipped and cause == genre_favorites.CLASS_UNDECLARED:

```

New text:

```
    if False:

```

### `u132.W3_version_from_report`

The job's report does not carry the version the skip saw

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W3_version_from_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_organize.py`
- Collected: 515 against a baseline of 515
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
            "schema_version": declared.schema_version,

```

New text:

```
            "schema_version": None,

```

### `u79-c.C3_accepted_held_listed_again`

An accepted candidate the library now holds is listed for download again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C3_accepted_held_listed_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_candidate_the_library_now_holds_is_not_listed_again`

Old text:

```
            if now.state in (match.MatchState.MATCHED, match.MatchState.SUPPRESSED):
                proposals[n]
```

New text:

```
            if False:
                proposals[n]
```

### `u79-c.C4_nothing_found_is_a_no_op`

Missing rows with no route to any of them end as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C4_nothing_found_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_acceptance_naming_none_of_several_candidates_lists_nothing`
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`

Old text:

```
    if unfound and not listed and not asked:
```

New text:

```
    if False:
```

### `u79-c.C5_foreign_ref_names_a_row`

Another service's identifier is read as the provider's, and the row is in no file

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C5_foreign_ref_names_a_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_missing_row_of_another_services_list_is_searched_for_and_not_dropped`
  - `tests/test_intake_missing_search.py::test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue`

Old text:

```
    return str(wanted.ref or "").strip() if wanted.origin == match.TIDAL else ""
```

New text:

```
    return str(wanted.ref or "").strip()
```

### `u79-c.C6_isrc_named_keeps_origin`

A foreign row named by ISRC keeps its origin, so the emitter takes the ref off again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C6_isrc_named_keeps_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue`

Old text:

```
                named.append(replace(one, ref=answer, origin=match.TIDAL))
```

New text:

```
                named.append(replace(one, ref=answer))
```

### `u79-c.C7_fixed_name`

The found list takes one fixed name, so the run after an answer is refused

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C7_fixed_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_one_exact_candidate_is_listed_without_review`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[.txt-txt-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[\xa7\xa7\xa7.txt-tracklist-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[friday set (2026).txt-friday-set-2026-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[intake-j1.unlisted.json-intake-j1-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[notes-notes-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[warmup.list.json-warmup-found]`
  - `tests/test_intake_missing_search.py::test_the_run_after_an_answer_lists_more_than_the_first_and_is_not_refused`
  - `tests/test_intake_missing_search.py::test_the_unlisted_list_is_read_and_its_found_list_sits_beside_the_jobs`
  - `tests/test_intake_missing_search.py::test_two_tracklists_of_one_file_name_in_two_folders_do_not_collide`

Old text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}-{digest}"
```

New text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}"
```

### `u79-c.C8_asked_is_a_no_op`

A run that only put a question to a person ends as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C8_asked_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
        outcome=Outcome.OK if listed or asked else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if listed else Outcome.NO_OP,
```

### `sitting3.G8_queue_skips_readiness`

File the job whatever is missing, so a restamp scores nothing and reports ok

- File: `src/cratekit/vocals/cli.py`
- Source: `sitting3.json`, row `G8_queue_skips_readiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_missing_checkpoint_is_refused_at_the_queue_and_named`
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`

Old text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if missing is None:
        return

```

New text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if True:
        return

```

