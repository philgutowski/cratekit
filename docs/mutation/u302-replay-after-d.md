# Mutation table: u302-replay-after-d

Measured by `scripts/mutate.py` on 2026-11-22 21:31 UTC, branch `cloud/859-write-layer-fifth-smaller` at `e702f6cd`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22930 collected. pytest invocations for this batch: 128.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `1cc4b9a30481`, and this tree is at `e702f6cd3662`).

Subset baselines: 18, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/d930efe3-5590-58b9-aa05-4d28a488c563/scratchpad/known-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22930 against 22930. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u119-b.G12r_removed_namesake_written_into` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119-b.G5r_favorites_counted_as_members` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119-c.C2_torn_bucket_bound_anyway` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119-c.C5_interruption_unreported` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 4 | killed |
| `u119.G10_placements_no_gap` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.G11_stale_digest` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.G13_removals_when_not_asked` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.G1_class_undeclared` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.G4_removed_membership_live` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119.G6_wanted_is_members` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 14 | killed |
| `u119.G7_twin_folders_first_taken` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119.G9_digest_over_adds` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u132.G1_undeclared_cause` | `src/cratekit/write/genre_favorites.py` | user | 5 file(s) | 319 | 2 | killed |
| `u185.R4_genre_source` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u76-a.D1_duplicate_sibling` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.D2_type_collision` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.D3_tree_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.D4_folder_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.D5_playlist_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-a.M1_merge_not_append` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 16 | killed |
| `u76-a.P2_dedupe_ids` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.W1_copy_on_write` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.W2_commit_on_success` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.X1_dedupe_against_held` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 6 | killed |
| `u76-b.C1_count_bump` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-b.L1_folder_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L2_anchor_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L3_folder_close_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L4_playlist_close_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.O1_anchor_order` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 4 | killed |
| `u76-b.O2_anchor_none` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 4 | killed |
| `u76-b.S1_self_closed_folder` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.X2_entries_count` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-b.X3_self_closed_playlist` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-b.X4_track_indent` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-zeros.P1_join_pairs` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-zeros.X5_entries_absent` | `src/cratekit/write/rbxml.py` | maintainer | 4 file(s) | 224 | 3 | killed |
| `u91.R1_crlf_guard` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 343 | 2 | killed |
| `a32.J3_bookkeeping_counted_as_moved` | `src/cratekit/write/row_defaults.py` | user | 2 file(s) | 113 | 6 | killed |
| `r923.N11_digest_drops_items` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N13_judge_compares_raw` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 4 | killed |
| `r923.N2_plan_lists_tombstones` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 14 | killed |
| `r923.N3_plan_sees_no_null` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 9 | killed |
| `r923.N4_stale_fill_accepted` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N5_stale_tombstone_accepted` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N6_judge_blind_to_wrong` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N7_judge_blind_to_moved` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N8_read_back_never_refuses` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `u115.F11_stale_file_id_not_checked` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F12_read_back_ignores_file_id` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F13_planned_renumber_read_as_moved` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F14_renumber_never_written` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F17_bound_is_zero` | `src/cratekit/write/row_defaults.py` | maintainer | 1 file(s) | 53 | 1 | killed |
| `u115.F21_other_volume_compared` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F22_off_apfs_decides` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F23_loose_digits` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `u115.F5_bound_boundary` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F6_every_id_above` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 12 | killed |
| `u115.F7_zero_is_not_zero` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 4 | killed |
| `u115.F9_unreadable_file_dropped_silently` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 5 | killed |
| `u298.H24_record_commit_nothing_written` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 100 | 1 | killed |
| `a32.A2_stale_deleted` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.A3_stale_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.A5_policy_widened` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.D1_digest_drops_replaced` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 2 | killed |
| `a32.D2_digest_unordered` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.J1_wrong_unjudged` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.J2_planned_across_rows` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.J4_moved_not_refused` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 2 | killed |
| `a32.P1_tombstone_plans` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.P2_unknown_row` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 4 | killed |
| `a32.P3_unheld_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 3 | killed |
| `a32.P4_count_tombstones` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 5 | killed |
| `a32.P6_writes_always` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 6 | killed |
| `a32.P7_minority_boundary` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.P8_null_fellows` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.V1_any_column` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 4 | killed |
| `a32.V2_link_not_converted` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 4 | killed |
| `u126.M1_half_is_a_majority` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 119 | 2 | killed |
| `u126.M2_plurality` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 119 | 3 | killed |
| `u126.M3_dead_rows_count` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 119 | 2 | killed |
| `u126.M4_least_common_first` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 119 | 3 | killed |
| `u126.M5_null_is_a_value` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 119 | 3 | killed |
| `u126.M6_any_text` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 119 | 2 | killed |
| `r375-b.T3_a_noop_claims_a_commit` | `src/cratekit/write/trees.py` | user | 3 file(s) | 197 | 1 | killed |
| `r375-b.T4_noop_bound_off_by_one` | `src/cratekit/write/trees.py` | user | 3 file(s) | 197 | 5 | killed |
| `r375-b.T8_counts_filed_as_updates` | `src/cratekit/write/trees.py` | user | 3 file(s) | 197 | 4 | killed |
| `r500-c.G14_located_skips_the_decode` | `src/cratekit/write/trees.py` | user | 10 file(s) | 1029 | 16 | killed |
| `r758-a.T5_dead_track_moved` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T6_removed_playlist_is_a_destination` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 2 | killed |
| `u298.H13_capture_verified` | `src/cratekit/write/trees.py` | user | 3 file(s) | 308 | 3 | killed |
| `u298.H14_capture_attached_before_judged` | `src/cratekit/write/trees.py` | user | 3 file(s) | 308 | 2 | killed |
| `u298.H15_rollback_swallows` | `src/cratekit/write/trees.py` | user | 2 file(s) | 160 | 1 | killed |
| `u40-author-full.F4_tombstone_indexed` | `src/cratekit/write/trees.py` | user | 7 file(s) | 751 | 3 | killed |
| `u77-b.B6_trial_id` | `src/cratekit/write/trees.py` | user | 6 file(s) | 284 | 2 | killed |
| `u77-b.B7_check_empty_catalog` | `src/cratekit/write/trees.py` | user | 6 file(s) | 284 | 2 | killed |
| `u77-b.B8_label_write_order` | `src/cratekit/write/trees.py` | user | 6 file(s) | 284 | 3 | killed |
| `u88-b.W1_replace_not_append` | `src/cratekit/write/trees.py` | user | 1 file(s) | 197 | 2 | killed |
| `u88-b.W3_dedupe` | `src/cratekit/write/trees.py` | user | 1 file(s) | 197 | 1 | killed |
| `u119.G15_removal_commit_admits_nothing` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 6 | killed |
| `u76-a.F1_nfc_fold` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.F2_case_fold` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `r375-b.T7_commit_recorded_after_the_fingerprint` | `src/cratekit/write/trees.py` | user | 3 file(s) | 197 | 1 | killed |
| `r758-a.T2_first_commit_admits_a_removal` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T3_target_not_proven` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T4_target_can_be_removed_from` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-b.T7_refusal_read_as_an_interruption` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `u111-b.B1_move_names_every_table` | `src/cratekit/write/trees.py` | user | 2 file(s) | 153 | 1 | killed |

## Row definitions

### `u119-b.G12r_removed_namesake_written_into`

_playlist_row: a removed Favorites of the name under the folder is written into

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-b.json`, row `G12r_removed_namesake_written_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removed_favorites_under_the_folder_is_not_written_into`

Old text:

```
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
```

New text:

```
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row):
            continue
```

### `u119-b.G5r_favorites_counted_as_members`

plan_refresh: the folder's own Favorites counts among the folder's members

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-b.json`, row `G5r_favorites_counted_as_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`

Old text:

```
            if favorites_node is not None and node.playlist_id == favorites_node.playlist_id:
                continue
            members.update(node.content_ids)
```

New text:

```
            members.update(node.content_ids)
```

### `u119-c.C2_torn_bucket_bound_anyway`

plan_refresh: a bucket whose record names two live folders is bound to the first

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-c.json`, row `C2_torn_bucket_bound_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_bucket_is_bound_by_its_band_entries_before_its_favorites_entry`

Old text:

```
        if bucket.id in recorded_folder and bucket.id not in torn
    }
```

New text:

```
        if bucket.id in recorded_folder
    }
```

### `u119-c.C5_interruption_unreported`

apply_refresh: a failure after the additions landed is raised bare, the additions unreported

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-c.json`, row `C5_interruption_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removal_commit_that_lands_and_then_raises_is_recorded_with_its_count`
  - `tests/test_genre_favorites.py::test_a_removal_that_fails_after_the_additions_landed_says_what_landed`
  - `tests/test_genre_favorites.py::test_the_additive_half_carries_the_additions_when_interrupted_past_them`
  - `tests/test_genre_favorites.py::test_the_verb_reports_an_interrupted_refresh_with_the_additions_that_committed`

Old text:

```
        except Exception as exc:
            raise RefreshInterrupted(landed) from exc
```

New text:

```
        except Exception:
            raise
```

### `u119.G10_placements_no_gap`

placements: a source that cannot be read names no dimension as not compared

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G10_placements_no_gap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`
  - `tests/test_genre_favorites.py::test_the_favourites_become_declared_placements_and_a_missing_source_a_gap`

Old text:

```
        return (), (FAVORITES_DIMENSION,)
```

New text:

```
        return (), ()
```

### `u119.G11_stale_digest`

apply_refresh: a plan whose digest moved since the approval is written anyway

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G11_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_plan_that_moved_between_the_approval_and_the_write_is_refused`
  - `tests/test_genre_favorites.py::test_the_digest_moves_when_a_track_is_dragged_into_favorites_between_the_acts`

Old text:

```
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them
```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them
```

### `u119.G13_removals_when_not_asked`

apply_refresh: the removals are made whether or not the caller was approved for them

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G13_removals_when_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_additive_half_adds_and_counts_what_it_leaves_owed`
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`

Old text:

```
        if remove and owed:
```

New text:

```
        if owed:
```

### `u119.G1_class_undeclared`

require_class: a taxonomy with no playlist class is not refused

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G1_class_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_taxonomy_declaring_no_playlist_class_refuses_by_name`
  - `tests/test_genre_favorites.py::test_the_verb_refuses_an_undeclared_class_by_name`

Old text:

```
    found = favorites_class(declared)
    if found is None:
        raise refuse(
            CLASS_UNDECLARED,
```

New text:

```
    found = favorites_class(declared)
    if False:
        raise refuse(
            CLASS_UNDECLARED,
```

### `u119.G4_removed_membership_live`

_live_members: a membership rekordbox removed still counts as held

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G4_removed_membership_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`

Old text:

```
        if not rb_writer.membership_removed(song)
    )
```

New text:

```
    )
```

### `u119.G6_wanted_is_members`

plan_refresh: every member of the folder is wanted, favourite or not

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G6_wanted_is_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 14 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh`
  - `tests/test_genre_favorites.py::test_a_plan_that_moved_between_the_approval_and_the_write_is_refused`
  - `tests/test_genre_favorites.py::test_a_removal_commit_that_lands_and_then_raises_is_recorded_with_its_count`
  - `tests/test_genre_favorites.py::test_a_removal_that_fails_after_the_additions_landed_says_what_landed`
  - `tests/test_genre_favorites.py::test_a_source_that_went_between_the_two_acts_is_refused_by_the_gate`
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`
  - `tests/test_genre_favorites.py::test_a_vocal_favourite_is_in_its_band_with_vox_and_favorites_under_one_genre`
  - `tests/test_genre_favorites.py::test_the_additive_half_adds_and_counts_what_it_leaves_owed`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`
  - `tests/test_genre_favorites.py::test_the_digest_moves_when_a_track_is_dragged_into_favorites_between_the_acts`
  - `tests/test_genre_favorites.py::test_the_favourites_become_declared_placements_and_a_missing_source_a_gap`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`
  - `tests/test_genre_favorites.py::test_the_verb_reports_an_interrupted_refresh_with_the_additions_that_committed`

Old text:

```
                wanted=tuple(sorted(members & favourites)),
```

New text:

```
                wanted=tuple(sorted(members)),
```

### `u119.G7_twin_folders_first_taken`

plan_refresh: two folders of one bucket's name, the first is taken

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G7_twin_folders_first_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_folder_nobody_declares_and_a_name_two_folders_carry_are_left_alone`

Old text:

```
        if len(named) > 1:
            unclaimed.extend(
```

New text:

```
        if len(named) > 9:
            unclaimed.extend(
```

### `u119.G9_digest_over_adds`

identity: the digest covers the adds rather than the target

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G9_digest_over_adds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`

Old text:

```
            "wanted": list(self.wanted),
            "removes": list(self.removes),
```

New text:

```
            "wanted": list(self.adds),
            "removes": list(self.removes),
```

### `u132.G1_undeclared_cause`

The additive half's skip over an undeclared class carries no cause

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u132.json`, row `G1_undeclared_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_routing_workers.py`
- Collected: 319 against a baseline of 319
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_drive_that_adds_nothing_still_names_an_undeclared_favorites_class`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
            cause=CLASS_UNDECLARED,

```

New text:

```
            cause="",

```

### `u185.R4_genre_source`

source_playlist: count a playlist of the source's name inside the folder

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u185.json`, row `R4_genre_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_source_namesake_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
    live = foreign_tree.outside(live, list(db.get_playlist()))
```

New text:

```
    live = list(live)
```

### `u76-a.D1_duplicate_sibling`

_sole_child: answer the first of two same named siblings instead of refusing the duplicate (R-129's refusal removed)

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `D1_duplicate_sibling`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`

Old text:

```
    if len(matches) > 1:
        return (
            f"{len(matches)} {_type_name(node_type)}s named
```

New text:

```
    if len(matches) > 99:
        return (
            f"{len(matches)} {_type_name(node_type)}s named
```

### `u76-a.D2_type_collision`

_sole_child: check the type of every match but the first, so a same named node of the other type standing first is merged into

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `D2_type_collision`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`

Old text:

```
    for child in matches:
        if child.node_type != node_type:
```

New text:

```
    for child in matches[1:]:
        if child.node_type != node_type:
```

### `u76-a.D3_tree_level_lookup`

_write_catalog: locate the catalog tree under ROOT with direct_child, so two trees of one name are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D3_tree_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`

Old text:

```
        found = _sole_child(content, root, tree.display, FOLDER_TYPE)
```

New text:

```
        found = direct_child(content, root, tree.display, FOLDER_TYPE)
```

### `u76-a.D4_folder_level_lookup`

_write_catalog: locate the label folder with direct_child, so two folders of the label's name are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D4_folder_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`

Old text:

```
    existing = _sole_child(content, parent, folder_name, FOLDER_TYPE)
```

New text:

```
    existing = direct_child(content, parent, folder_name, FOLDER_TYPE)
```

### `u76-a.D5_playlist_level_lookup`

_merge_catalog: locate a held year playlist with direct_child, so two playlists of one year are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D5_playlist_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`

Old text:

```
        playlist = _sole_child(content, here, name, PLAYLIST_TYPE)
```

New text:

```
        playlist = direct_child(content, here, name, PLAYLIST_TYPE)
```

### `u76-a.M1_merge_not_append`

_write_catalog: never take the merge path, so a held folder gets a second folder of its name beside it (the R-129 doubling)

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `M1_merge_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 16 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_catalog_written_twice_is_byte_identical_to_written_once`
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_playlist_that_gains_nothing_is_left_byte_identical`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_a_catalog_rerun_refreshes_the_folder_rather_than_duplicating_it`
  - `tests/test_tree_writer.py::test_one_source_the_writer_refuses_writes_none_of_them`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    if existing is not None:
        return _merge_catalog(content, existing, pairs)
```

New text:

```
    if existing is not None and not existing:
        return _merge_catalog(content, existing, pairs)
```

### `u76-a.P2_dedupe_ids`

_merged_pairs: keep a batch's repeated ids, so a playlist lists one track twice

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `P2_dedupe_ids`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`

Old text:

```
    return [(joined[key][0], dedupe_track_ids(joined[key][1])) for key in order]
```

New text:

```
    return [(joined[key][0], list(joined[key][1])) for key in order]
```

### `u76-a.W1_copy_on_write`

insert_catalog_folder: edit the caller's document directly, so a refusal after an earlier merge leaves that merge behind

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `W1_copy_on_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    work = bytearray(content)
    warning = _write_catalog(
```

New text:

```
    work = content
    warning = _write_catalog(
```

### `u76-a.W2_commit_on_success`

insert_catalog_folder: copy the working bytes back even on a refusal

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `W2_commit_on_success`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    if warning is None:
        content[:] = work
    return warning
```

New text:

```
    if warning is None or warning:
        content[:] = work
    return warning
```

### `u76-a.X1_dedupe_against_held`

_extend_playlist: dedupe the new ids against nothing, so a member the playlist holds is added again

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `X1_dedupe_against_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 6 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_catalog_written_twice_is_byte_identical_to_written_once`
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_a_playlist_that_gains_nothing_is_left_byte_identical`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`
  - `tests/test_xml_splice_golden.py::test_label_subtree_written_twice_matches_the_single_write_golden`

Old text:

```
    fresh = dedupe_track_ids(track_ids, track_keys(content, playlist))
```

New text:

```
    fresh = dedupe_track_ids(track_ids, ())
```

### `u76-b.C1_count_bump`

_merge_catalog: move the folder's Count by one less than the playlists created

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `C1_count_bump`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
        _bump_count(content, here, created)
```

New text:

```
        _bump_count(content, here, created - 1)
```

### `u76-b.L1_folder_own_line`

_merge_catalog: drop the check that the held folder starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L1_folder_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    if not _starts_its_line(content, folder.line_start, folder.tag_start):
        return f"the folder {folder.name!r} does not start its own line"
```

New text:

```
    if False:
        return f"the folder {folder.name!r} does not start its own line"
```

### `u76-b.L2_anchor_own_line`

_merge_catalog: drop the check that the playlist a new year goes before starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L2_anchor_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
            if not _starts_its_line(content, at, anchor.tag_start):
```

New text:

```
            if False:
```

### `u76-b.L3_folder_close_own_line`

_merge_catalog: drop the check that the folder's close tag starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L3_folder_close_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
            if not _starts_its_line(content, at, here.close_start):
```

New text:

```
            if False:
```

### `u76-b.L4_playlist_close_own_line`

_extend_playlist: drop the check that a held playlist's close tag starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L4_playlist_close_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
        if not _starts_its_line(content, at, playlist.close_start):
```

New text:

```
        if False:
```

### `u76-b.O1_anchor_order`

_merge_catalog: place a new year before the first held playlist sorting ABOVE it, reversing newest first

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `O1_anchor_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`

Old text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted
```

New text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) > wanted
```

### `u76-b.O2_anchor_none`

_merge_catalog: always append a new year last

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `O2_anchor_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`

Old text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted
```

New text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted and False
```

### `u76-b.S1_self_closed_folder`

_merge_catalog: do not open a self closed held folder before merging into it

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `S1_self_closed_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    if folder.self_closing:
        # An empty folder exported self closed
```

New text:

```
    if folder.self_closing and not folder.self_closing:
        # An empty folder exported self closed
```

### `u76-b.X2_entries_count`

_extend_playlist: move Entries by the ids offered rather than the ids added

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X2_entries_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`

Old text:

```
    total = _read_int(content, entries) + len(fresh)
```

New text:

```
    total = _read_int(content, entries) + len(track_ids)
```

### `u76-b.X3_self_closed_playlist`

_extend_playlist: treat a self closed playlist as open, writing at the line of a close tag it does not have

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X3_self_closed_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    if playlist.self_closing:
        content[playlist.tag_end - 1 : playlist.tag_end + 1] = bytearray(
            b">" + CRLF + lines + b" " * playlist.indent + _NODE_CLOSE
```

New text:

```
    if playlist.self_closing and not playlist.self_closing:
        content[playlist.tag_end - 1 : playlist.tag_end + 1] = bytearray(
            b">" + CRLF + lines + b" " * playlist.indent + _NODE_CLOSE
```

### `u76-b.X4_track_indent`

_extend_playlist: write the added track keys at the playlist's own indent rather than one step in

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X4_track_indent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    lines = track_key_lines(fresh, playlist.indent + INDENT_STEP).encode("utf-8")
```

New text:

```
    lines = track_key_lines(fresh, playlist.indent).encode("utf-8")
```

### `u76-zeros.P1_join_pairs`

_merged_pairs: keep every pair as given, so a caller naming one playlist twice emits two siblings of that name

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-zeros.json`, row `P1_join_pairs`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`

Old text:

```
    return [(joined[key][0], dedupe_track_ids(joined[key][1])) for key in order]
```

New text:

```
    return [(name, dedupe_track_ids(ids)) for name, ids in playlists]
```

### `u76-zeros.X5_entries_absent`

_extend_playlist: write the ids into a held playlist with no Entries attribute rather than refusing

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-zeros.json`, row `X5_entries_absent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`
  - `tests/test_tree_writer.py::test_one_source_the_writer_refuses_writes_none_of_them`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`

Old text:

```
    if entries is None:
        return f"Entries attr not found for playlist {playlist.name!r}"
    total = _read_int(content, entries) + len(fresh)
```

New text:

```
    if entries is None:
        entries = (playlist.tag_end, playlist.tag_end)
    total = _read_int(content, entries) + len(fresh) if entries[0] != entries[1] else len(fresh)
```

### `u91.R1_crlf_guard`

splice_into_subplaylist create branch: restore the old arithmetic, the close line minus two bytes, with no CRLF check

- File: `src/cratekit/write/rbxml.py`
- Source: `u91.json`, row `R1_crlf_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`
- Collected: 343 against a baseline of 343
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_the_creating_writer_refuses_a_document_whose_lines_end_in_lf`

Old text:

```
        at = _break_before(content, line_start(content, folder.close_start))
        if at is None:
```

New text:

```
        at = line_start(content, folder.close_start) - len(CRLF)
        if at is None:
```

### `a32.J3_bookkeeping_counted_as_moved`

The shared moved column rule counts the binding's bookkeeping columns as moved

- File: `src/cratekit/write/row_defaults.py`
- Source: `a32.json`, row `J3_bookkeeping_counted_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_repair_rows.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_judge_accepts_values_read_back_as_the_live_tables_types`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    skip = set(planned) | rb_writer.BOOKKEEPING_COLUMNS
```

New text:

```
    skip = set(planned)
```

### `r923.N11_digest_drops_items`

The digest no longer covers the rows and columns the plan fills

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N11_digest_drops_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_random_id_is_replaced_elsewhere`

Old text:

```
                "items": [item.to_json() for item in self.items],
```

New text:

```
                "items": [],
```

### `r923.N13_judge_compares_raw`

The read back compares a default by raw value, so the live table's integer reads as wrong against the binding's string

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N13_judge_compares_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            or str(now[column]) != str(rb_writer.CONTENT_ROW_DEFAULTS[column])
```

New text:

```
            or now[column] != rb_writer.CONTENT_ROW_DEFAULTS[column]
```

### `r923.N2_plan_lists_tombstones`

The repair plans soft deleted rows beside live ones

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N2_plan_lists_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 14 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_plan_that_renumbers_nothing_registers_no_file_id_policy`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_a_tombstone_is_never_listed_though_every_default_is_null`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_nothing_is_judged_random`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0"
```

New text:

```
            ""
```

### `r923.N3_plan_sees_no_null`

The repair never finds a NULL default, so it plans nothing

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N3_plan_sees_no_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 9 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-planned-column-set]`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_nothing_is_judged_random`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        missing = tuple(column for column in COLUMNS if row[column] is None)
```

New text:

```
        missing = tuple(column for column in COLUMNS if False)
```

### `r923.N4_stale_fill_accepted`

A planned column set since the plan is written over anyway

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N4_stale_fill_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-planned-column-set]`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
        if filled:
```

New text:

```
        if False:
```

### `r923.N5_stale_tombstone_accepted`

A row soft deleted since the plan is still written

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N5_stale_tombstone_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-row-deleted]`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
```

New text:

```
        if row is None:
```

### `r923.N6_judge_blind_to_wrong`

The read back no longer names a planned column that did not take its default

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N6_judge_blind_to_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`

Old text:

```
        if off:
```

New text:

```
        if False:
```

### `r923.N7_judge_blind_to_moved`

The read back no longer names a column outside the plan that moved

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N7_judge_blind_to_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved`

Old text:

```
        if changed:
```

New text:

```
        if False:
```

### `r923.N8_read_back_never_refuses`

assert_read_back returns whatever the read back found

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N8_read_back_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_assert_read_back_refuses_and_names_the_undo[a-moved-column]`
  - `tests/test_repair_rows.py::test_assert_read_back_refuses_and_names_the_undo[a-wrong-value]`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
    if not written.wrong and not written.moved:
        return
```

New text:

```
    if True:
        return
```

### `u115.F11_stale_file_id_not_checked`

A file id changed since the plan is written over without a staleness refusal

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F11_stale_file_id_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-file-id-renumbered]`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
        if item.renumbers and str(row.get(FILE_ID) or "").strip() != item.file_id_was:
            moved.append(f"{item.content_id}: {FILE_ID} changed since the plan")
```

New text:

```
        if False:
            moved.append(f"{item.content_id}: {FILE_ID} changed since the plan")
```

### `u115.F12_read_back_ignores_file_id`

The read back never checks that the inode took, so a renumber that did not land reads as written

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F12_read_back_ignores_file_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_renumber_that_did_not_take`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
        if item.renumbers and str(now.get(FILE_ID) or "").strip() != str(item.file_id):
            wrong.append(f"{item.content_id}: {FILE_ID} not the file's inode")
```

New text:

```
        if False:
            wrong.append(f"{item.content_id}: {FILE_ID} not the file's inode")
```

### `u115.F13_planned_renumber_read_as_moved`

The read back forgets the file id was planned, so every renumber is reported as a column the guard let move

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F13_planned_renumber_read_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        if item.renumbers:
            planned.add(FILE_ID)
```

New text:

```
        if False:
            planned.add(FILE_ID)
```

### `u115.F14_renumber_never_written`

The apply fills the defaults and never writes the planned file id

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F14_renumber_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        if item.renumbers:
            writes.append((file_owner, FILE_ID, item.file_id))
```

New text:

```
        if False:
            writes.append((file_owner, FILE_ID, item.file_id))
```

### `u115.F17_bound_is_zero`

The volume's inode bound is reported as zero rather than measured from a fresh file

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F17_bound_is_zero`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
        inode=measured.st_ino, device=measured.st_dev, filesystem=filesystem_of(directory)
```

New text:

```
        inode=0, device=measured.st_dev, filesystem=filesystem_of(directory)
```

### `u115.F21_other_volume_compared`

A file on another volume than the bound is stat'ed and its inode compared, so rekordbox's rows there can be renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F21_other_volume_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
    if found.st_dev != device:
        return None, ON_ANOTHER_VOLUME
```

New text:

```
    if False:
        return None, ON_ANOTHER_VOLUME
```

### `u115.F22_off_apfs_decides`

The bound is trusted on any filesystem, so an exFAT or HFS+ library has rekordbox's rows renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F22_off_apfs_decides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
        if self.filesystem != APFS:
            named = self.filesystem or "unknown"
```

New text:

```
        if False:
            named = self.filesystem or "unknown"
```

### `u115.F23_loose_digits`

A signed or underscored text, or a digit from another script, is parsed as a number and judged above the bound

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F23_loose_digits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[+200000000-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[300_000_000-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[\u0663\u0663\u0663\u0663\u0663\u0663\u0663\u0663\u0663-within]`

Old text:

```
    if not (text.isascii() and text.isdigit()):
        return WITHIN
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    try:
        number = int(text)
    except ValueError:
        return WITHIN
    return ABOVE if number > bound else WITHIN
```

### `u115.F5_bound_boundary`

An id equal to the bound is judged above it

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F5_bound_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within1]`

Old text:

```
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    return ABOVE if int(text) >= bound else WITHIN
```

### `u115.F6_every_id_above`

Every nonzero id is judged above the bound, so stale rows rekordbox tolerates are renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F6_every_id_above`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 12 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[1-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within1]`
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_a_tombstone_is_never_listed_though_every_default_is_null`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    return ABOVE
```

### `u115.F7_zero_is_not_zero`

A stored 0 is no longer read as the zero form rekordbox tolerates

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F7_zero_is_not_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[0-zero0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[0-zero1]`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`

Old text:

```
    if text in ("", "0"):
        return ZERO
```

New text:

```
    if text == "":
        return ZERO
```

### `u115.F9_unreadable_file_dropped_silently`

A row above the bound whose file cannot be read is neither listed nor written, and the gate says nothing

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F9_unreadable_file_dropped_silently`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            if inode is None:
                unrenumbered.append(
```

New text:

```
            if False:
                unrenumbered.append(
```

### `u298.H24_record_commit_nothing_written`

record_commit: a run that wrote nothing claims a commit a restore would discard

- File: `src/cratekit/write/row_defaults.py`
- Source: `u298.json`, row `H24_record_commit_nothing_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_row_write_that_wrote_nothing_claims_no_commit`

Old text:

```
    if written <= 0:
        return
    session.record_commit(
```

New text:

```
    session.record_commit(
```

### `a32.A2_stale_deleted`

A row deleted since the plan is still written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A2_stale_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_row_deleted_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
```

New text:

```
        if row is None:
```

### `a32.A3_stale_value`

A row whose column moved since the plan is still written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A3_stale_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_changed_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        elif _text(row.get(probe.column)) != probe.was:
```

New text:

```
        elif False:
```

### `a32.A5_policy_widened`

The commit's policy admits both probe columns whatever the plan writes

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A5_policy_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_writing_one_column_admits_only_that_one_to_the_guard`

Old text:

```
    policy = rb_writer.row_probe_policy(p.column for p in plan.writing)
```

New text:

```
    policy = rb_writer.row_probe_policy(rb_writer.ROW_PROBE_COLUMNS)
```

### `a32.D1_digest_drops_replaced`

Drop the replaced value from the item, so the digest does not move when it changes

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `D1_digest_drops_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_digest_moves_with_the_rows_the_columns_and_both_values`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
            "from": self.was,
```

New text:

```
            "from": "",
```

### `a32.D2_digest_unordered`

Keep the triples in the order given, so the same plan digests two ways

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `D2_digest_unordered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_digest_is_equal_whatever_order_the_triples_are_given_in`

Old text:

```
    probes.sort(key=lambda p: (len(p.content_id), p.content_id, p.column))
```

New text:

```
(empty)
```

### `a32.J1_wrong_unjudged`

The judge never reports a value that did not take

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J1_wrong_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_judge_names_a_value_that_did_not_take_and_a_column_that_moved`

Old text:

```
            if now.get(probe.column) is None or _text(now[probe.column]) != str(probe.value):
```

New text:

```
            if False:
```

### `a32.J2_planned_across_rows`

The judge excuses every column the plan writes on any row, not the row's own

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J2_planned_across_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_judge_counts_a_column_written_on_another_row_as_moved_here`

Old text:

```
        changed = row_defaults.moved_columns(was, now, planned=plan.columns_on(content_id))
```

New text:

```
        changed = row_defaults.moved_columns(was, now, planned=[p.column for p in plan.writing])
```

### `a32.J4_moved_not_refused`

A moved column is reported as a wrong value rather than the guard's defect

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J4_moved_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`
  - `tests/test_repair_link.py::test_assert_read_back_refuses_and_names_the_undo[a-moved-column]`

Old text:

```
    if written.moved:
        raise refuse(
            "whitelist-violation",
```

New text:

```
    if False:
        raise refuse(
            "whitelist-violation",
```

### `a32.P1_tombstone_plans`

Drop the live row filter from the plan's row query, so a tombstone plans

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P1_tombstone_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-tombstone]`

Old text:

```
                    f"WHERE ID = :id AND {rb_writer.SOFT_DELETE_COLUMN} = 0"
```

New text:

```
                    f"WHERE ID = :id"
```

### `a32.P2_unknown_row`

Drop the unknown row refusal, so an absent identifier falls through

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P2_unknown_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_refusal_reaches_no_gate`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-tombstone]`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[an-unknown-row]`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[one-bad-triple-refuses-the-whole-plan]`

Old text:

```
        if row is None:
            raise refuse(
                ROW_UNKNOWN,
```

New text:

```
        if row is None and False:
            raise refuse(
                ROW_UNKNOWN,
```

### `a32.P3_unheld_value`

Drop the unheld value refusal, so a value nobody carries is written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P3_unheld_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-link-nobody-carries]`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-value-only-a-tombstone-carries]`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[an-isrc-nobody-carries]`

Old text:

```
        if probe.writes and carriers == 0:
```

New text:

```
        if probe.writes and carriers < 0:
```

### `a32.P4_count_tombstones`

Count tombstones as carriers and fellows of a value

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P4_count_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_null_counts_its_fellows_as_null_so_writing_one_back_is_the_minority`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-value-only-a-tombstone-carries]`
  - `tests/test_repair_link.py::test_the_bindings_value_onto_a_row_rekordbox_made_refuses_as_the_minority`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`

Old text:

```
            f"AND {rb_writer.SOFT_DELETE_COLUMN} = 0 AND ID != :id"
```

New text:

```
            f"AND ID != :id"
```

### `a32.P6_writes_always`

Every triple writes, a row already at the value included

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P6_writes_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 6 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`
  - `tests/test_repair_link.py::test_a_row_already_at_a_value_nobody_else_carries_still_plans_nothing`
  - `tests/test_repair_link.py::test_a_row_already_at_the_value_plans_nothing_for_that_triple`
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_apply_refuses_a_plan_that_writes_nothing_as_a_defect`
  - `tests/test_repair_link.py::test_judge_skips_a_triple_that_writes_nothing`

Old text:

```
        return self.was != str(self.value)
```

New text:

```
        return True
```

### `a32.P7_minority_boundary`

Move the majority rule's boundary, so a value carried by as many rows as the row's own is written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P7_minority_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-value-as-many-rows-carry-as-the-rows-own]`

Old text:

```
        if probe.writes and carriers <= fellows:
```

New text:

```
        if probe.writes and carriers < fellows:
```

### `a32.P8_null_fellows`

Count a NULL's fellows with an equality, which matches nothing, so a NULL has no fellows

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P8_null_fellows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
    test = f"{column} IS NULL" if value is None else f"{column} = :value"
```

New text:

```
    test = f"{column} = :value"
```

### `a32.V1_any_column`

A triple naming a column outside the probe set is parsed, AnalysisUpdated included

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `V1_any_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:AnalysisUpdated=2]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:BPM=12800]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:Title=x]`
  - `tests/test_repair_link.py::test_a_malformed_triple_refuses_through_the_verb_before_any_gate`

Old text:

```
    if kind is None:
        raise _invalid(
```

New text:

```
    if False:
        raise _invalid(
```

### `a32.V2_link_not_converted`

A ContentLink value is kept as text rather than converted to a whole number

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `V2_link_not_converted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:ContentLink=]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:ContentLink=lots]`
  - `tests/test_repair_link.py::test_a_triple_reads_row_column_and_a_value_of_the_columns_type`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
    if kind is int:
```

New text:

```
    if False:
```

### `u126.M1_half_is_a_majority`

Accept a value carried by exactly half the live rows

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M1_half_is_a_majority`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_library_with_no_majority_content_link_refuses_before_the_gate`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows0]`

Old text:

```
and carriers * 2 > rows:
```

New text:

```
and carriers * 2 >= rows:
```

### `u126.M2_plurality`

Accept the most common value whatever share of the live rows carries it

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M2_plurality`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_library_with_no_majority_content_link_refuses_before_the_gate`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows0]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows1]`

Old text:

```
and carriers * 2 > rows:
```

New text:

```
:
```

### `u126.M3_dead_rows_count`

Count removed rows in the majority, so a library's tombstones vote

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M3_dead_rows_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows6]`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows1-2]`

Old text:

```
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0 GROUP BY {LINK} "
```

New text:

```
            f"GROUP BY {LINK} "
```

### `u126.M4_least_common_first`

Order the values least common first, so the first read is not the majority

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M4_least_common_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows0-3]`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows2-2]`

Old text:

```
            f"ORDER BY COUNT(*) DESC"
```

New text:

```
            f"ORDER BY COUNT(*) ASC"
```

### `u126.M5_null_is_a_value`

Drop the NULL test, so a NULL majority is taken as the value

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M5_null_is_a_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows2]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows6]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows7]`

Old text:

```
    if whole is not None and _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

New text:

```
    if whole is None or _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

### `u126.M6_any_text`

Loosen the whole number test to the sign stripped isdigit the review found, so --5 and a superscript digit reach int()

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M6_any_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows4]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows5]`

Old text:

```
    if whole is not None and _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

New text:

```
    if whole is not None and whole.lstrip("-").isdigit() and carriers * 2 > rows:
```

### `r375-b.T3_a_noop_claims_a_commit`

_record_membership_commit: record a commit for a pass that added nothing, so a restore refuses over sessions that created nothing

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T3_a_noop_claims_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_pass_that_added_nothing_claims_no_commit`

Old text:

```
    if added <= 0:
        return
    session.record_commit(
```

New text:

```
    session.record_commit(
```

### `r375-b.T4_noop_bound_off_by_one`

_record_membership_commit: move the no-op bound by one, so a pass that added exactly one membership claims no commit

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T4_noop_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_moves_removal_commit_that_lands_and_then_raises_is_still_recorded`
  - `tests/test_tree_writer.py::test_a_pass_that_added_nothing_claims_no_commit`

Old text:

```
    if added <= 0:
        return
    session.record_commit(
```

New text:

```
    if added <= 1:
        return
    session.record_commit(
```

### `r375-b.T8_counts_filed_as_updates`

_record_membership_commit: file the added memberships as updated rather than created

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T8_counts_filed_as_updates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - `tests/test_tree_writer.py::test_a_moves_removal_commit_that_lands_and_then_raises_is_still_recorded`

Old text:

```
session.TreeChange(tree=tree_id, created=added)
```

New text:

```
session.TreeChange(tree=tree_id, updated=added)
```

### `r500-c.G14_located_skips_the_decode`

trees.located resolves the raw recorded value without decoding it, the shared locate step both writers and this verb now call

- File: `src/cratekit/write/trees.py`
- Source: `r500-c.json`, row `G14_located_skips_the_decode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 1029 against a baseline of 1029
- Kills: 16 (killed)
- Killed:
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
  - `tests/test_adopt_workers.py::test_the_membership_write_needs_locations_and_not_content_identifiers`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    decoded = locations.location_to_path(str(recorded))
    return decoded,
```

New text:

```
    decoded = str(recorded)
    return decoded,
```

### `r758-a.T5_dead_track_moved`

a track with no live collection row is moved like any other

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T5_dead_track_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_no_live_collection_row_is_skipped_whole`

Old text:

```
        live = [move for move in moves if _live_content(db, move.content_id)]
```

New text:

```
        live = list(moves)
```

### `r758-a.T6_removed_playlist_is_a_destination`

a playlist rekordbox removed answers for a destination, so an addition lands where nobody can see it

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T6_removed_playlist_is_a_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_sub_held_only_through_a_removed_playlist_is_not_planned_for_removal`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`

Old text:

```
        and str(getattr(playlist, "ParentID", "")) in parents
        and not rb_writer.node_removed(playlist)
```

New text:

```
        and str(getattr(playlist, "ParentID", "")) in parents
```

### `u298.H13_capture_verified`

attached_capture: a capture that fails its check is written past

- File: `src/cratekit/write/trees.py`
- Source: `u298.json`, row `H13_capture_verified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 308 against a baseline of 308
- Kills: 3 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_write_commits_behind_a_verified_capture`
  - `tests/test_write_session.py::test_the_shared_capture_attaches_before_it_judges`
  - `tests/test_write_session.py::test_the_tree_writers_reach_for_the_session_spine`

Old text:

```
    session.attach_capture(record, capture.root, cfg)
    snapshot.assert_verified(capture)
    return record, capture
```

New text:

```
    session.attach_capture(record, capture.root, cfg)
    return record, capture
```

### `u298.H14_capture_attached_before_judged`

attached_capture: a capture that fails its check is never attached to the session record

- File: `src/cratekit/write/trees.py`
- Source: `u298.json`, row `H14_capture_attached_before_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 308 against a baseline of 308
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_write_commits_behind_a_verified_capture`
  - `tests/test_write_session.py::test_the_shared_capture_attaches_before_it_judges`

Old text:

```
    session.attach_capture(record, capture.root, cfg)
    snapshot.assert_verified(capture)
    return record, capture
```

New text:

```
    snapshot.assert_verified(capture)
    session.attach_capture(record, capture.root, cfg)
    return record, capture
```

### `u298.H15_rollback_swallows`

rollback_quietly: a rollback that raises replaces the real cause with its own

- File: `src/cratekit/write/trees.py`
- Source: `u298.json`, row `H15_rollback_swallows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_tree_writer.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_rollback_that_fails_is_said_once_and_never_replaces_the_failure_it_follows`

Old text:

```
    try:
        db.session.rollback()
    except Exception:  # noqa: BLE001 - a failed cleanup must not hide its cause
        logger.warning("could not roll back the pending session after a failed write")
```

New text:

```
    db.session.rollback()
```

### `u40-author-full.F4_tombstone_indexed`

First caller sample: stop dropping tombstones from the active row index, so a removed track claims its location

- File: `src/cratekit/write/trees.py`
- Source: `u40-author-full.json`, row `F4_tombstone_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 751 against a baseline of 751
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_tree_writer.py::test_normalization_resolves_each_spelling_to_the_right_row[a-tombstone-beside-an-active-row]`

Old text:

```
    for row in rows:
        if row.deleted:
            continue
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

New text:

```
    for row in rows:
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

### `u77-b.B6_trial_id`

check_record_labels_tree: trial every year with no id, so the writer returns from a held playlist before its three layout refusals and the check passes what the write refuses

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B6_trial_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 284 against a baseline of 284
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`

Old text:

```
trial, label, [(f"{label} {year}", [_TRIAL_ID]) for year in years], target
```

New text:

```
trial, label, [(f"{label} {year}", []) for year in years], target
```

### `u77-b.B7_check_empty_catalog`

check_record_labels_tree: resolve the catalog tree even when nothing would be written, so an undeclared tree refuses a landing that has no label row

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B7_check_empty_catalog`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 284 against a baseline of 284
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing`
  - `tests/test_tree_writer.py::test_the_catalog_check_asks_nothing_when_there_is_nothing_to_write`

Old text:

```
    if not catalog:
        return
    target = _catalog_tree(declared, registry, tree)
    trial
```

New text:

```
    if catalog is None:
        return
    target = _catalog_tree(declared, registry, tree)
    trial
```

### `u77-b.B8_label_write_order`

insert_record_labels_trees: write the sources first name first, so a new tree reads Z to A

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B8_label_write_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 284 against a baseline of 284
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_the_labelled_intake_file_golden`
  - `tests/test_landing_labels.py::test_two_labels_across_two_years_are_four_playlists_in_the_intake_file`
  - `tests/test_tree_writer.py::test_several_sources_are_one_write_and_a_new_tree_reads_a_to_z`

Old text:

```
    for label in sorted(catalog, reverse=True):
        _insert_catalog(content,
```

New text:

```
    for label in sorted(catalog):
        _insert_catalog(content,
```

### `u88-b.W1_replace_not_append`

add_to_root_playlist: write the new tracks alone, so the playlist's members are replaced

- File: `src/cratekit/write/trees.py`
- Source: `u88-b.json`, row `W1_replace_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_track_is_never_removed_from_the_playlist`
  - `tests/test_routing_workers.py::test_the_add_only_writer_counts_each_new_track_once`

Old text:

```
    warning = rbxml.insert_root_playlist(name, [*existing, *new], content)
```

New text:

```
    warning = rbxml.insert_root_playlist(name, new, content)
```

### `u88-b.W3_dedupe`

add_to_root_playlist: drop the dedupe, so a repeated id or an existing member is added again

- File: `src/cratekit/write/trees.py`
- Source: `u88-b.json`, row `W3_dedupe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_add_only_writer_counts_each_new_track_once`

Old text:

```
        if key not in held:
```

New text:

```
        if True:
```

### `u119.G15_removal_commit_admits_nothing`

apply_refresh: the second commit does not admit the membership table

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G15_removal_commit_admits_nothing`
- Moved: the removal commit now sits in _remove_favorites, one level less indented, the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 6 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`
  - `tests/test_genre_favorites.py::test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh`
  - `tests/test_genre_favorites.py::test_a_removal_commit_that_lands_and_then_raises_is_recorded_with_its_count`
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`
  - `tests/test_genre_favorites.py::test_no_content_row_tempo_or_rating_is_written`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`

Old text:

```
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

New text:

```
            rb_writer.commit_guarded(db)
```

### `u76-a.F1_nfc_fold`

_folded: compare names as given, so a composed and a decomposed spelling of one label are two folders

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `F1_nfc_fold`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py; the text also occurs in an intake module, so the tool could not pick the file
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`

Old text:

```
    return unicodedata.normalize("NFC", name)
```

New text:

```
    return name
```

### `u76-a.F2_case_fold`

_folded: fold case as well, so a label differing only by case is poured into another label's folder

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `F2_case_fold`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py; the text also occurs in an intake module, so the tool could not pick the file
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_similarly_named_sibling_folder_is_untouched`

Old text:

```
    return unicodedata.normalize("NFC", name)
```

New text:

```
    return unicodedata.normalize("NFC", name).casefold()
```

### `r375-b.T7_commit_recorded_after_the_fingerprint`

write_tree_membership: record the commit AFTER the fingerprint write, so a failure there closes a committed write as empty

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T7_commit_recorded_after_the_fingerprint`
- Moved: write_tree_membership's commit record and fingerprint now read from the _Run record and their comment is shortened; the same two calls swapped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`

Old text:

```
        _record_membership_commit(record, tree_id, run.added, cfg)

        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT, or the next run
        # would read this session's own write as an out of band restore. Outside
        # the try, since the commit has landed and nothing is pending.
        convergence.record_fingerprint(cfg, db)

```

New text:

```
        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT, or the next run
        # would read this session's own write as an out of band restore. Outside
        # the try, since the commit has landed and nothing is pending.
        convergence.record_fingerprint(cfg, db)
        _record_membership_commit(record, tree_id, run.added, cfg)

```

### `r758-a.T2_first_commit_admits_a_removal`

the move's first commit admits a removal, so one slipped into the additions lands

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T2_first_commit_admits_a_removal`
- Moved: the move's additions and their commit are now the step _add_targets, writing through the _Run record
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_moves_own_first_commit_refuses_a_removal`

Old text:

```
                run.add(places.for_adding(destination), destination, content_ids)
            rb_writer.commit_guarded(run.db)
```

New text:

```
                run.add(places.for_adding(destination), destination, content_ids)
            rb_writer.commit_guarded(run.db, removals=rb_writer.REMOVABLE_TABLES)
```

### `r758-a.T3_target_not_proven`

a removal is made whether or not the track sits in its target, so a track can end in neither

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T3_target_not_proven`
- Moved: the proof of the target is now the step _proven_leavers, one level less indented, the same test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_not_in_its_target_has_nothing_removed`

Old text:

```
        if not places.holds(move.target, move.content_id):
            held_back.append(move.content_id)
            continue
```

New text:

```
(empty)
```

### `r758-a.T4_target_can_be_removed_from`

a move that names its own target among its removals takes the track out of the target

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T4_target_can_be_removed_from`
- Moved: the leavers are now gathered in the step _proven_leavers, one level less indented, the same test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_target_is_never_removed_from_even_when_a_move_names_it`

Old text:

```
            if destination != move.target:
                leaving.setdefault(destination, []).append(move.content_id)
```

New text:

```
            leaving.setdefault(destination, []).append(move.content_id)
```

### `r758-b.T7_refusal_read_as_an_interruption`

a refusal in the removals is raised as an interrupted move and loses its own cause and remedy

- File: `src/cratekit/write/trees.py`
- Source: `r758-b.json`, row `T7_refusal_read_as_an_interruption`
- Moved: the removals are now the step _remove_leavers, one level less indented, the same clause
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`

Old text:

```
            if isinstance(exc, cause.CratekitError):
                raise

```

New text:

```
(empty)
```

### `u111-b.B1_move_names_every_table`

The membership move's commit admits the whole removable set again, the playlist table included

- File: `src/cratekit/write/trees.py`
- Source: `u111-b.json`, row `B1_move_names_every_table`
- Moved: the removal commit is now in the step _remove_leavers, one level less indented, the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_adopt_move.py`
- Collected: 153 against a baseline of 153
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_only_the_rotation_asks_its_commit_to_admit_a_removed_playlist`

Old text:

```
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

New text:

```
            rb_writer.commit_guarded(db, removals=rb_writer.REMOVABLE_TABLES)
```

