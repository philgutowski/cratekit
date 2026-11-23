# Mutation table: u311-replay-before-d3

Measured by `scripts/mutate.py` on 2026-11-23 03:56 UTC, branch `HEAD` at `d8135e39`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 33.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-23 03:56 UTC for commit `d8135e39d6eb`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 3, each measured by this driver.

Known failures: 149 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r757-a.E5_mode_read_backwards` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 758 | 4 | killed |
| `r757-a.E6_unread_total_is_zero` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-a.E7_first_totals_win` | `src/cratekit/modules/tools/backup.py` | maintainer | 4 file(s) | 758 | 1 | killed |
| `r757-a.E8_failed_mirror_reports_nothing` | `src/cratekit/modules/tools/backup.py` | maintainer | 4 file(s) | 758 | 1 | killed |
| `r757-a.E9_stats_interval_zero` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 22933 | 0 (promoted) | zero |
| `r757-b1.E10_fast_run_records_a_full_comparison` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-b1.E11_full_run_records_nothing` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-b1.E12_plain_line_dropped` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-b1.E13_runner_times_nothing` | `src/cratekit/modules/tools/backup.py` | maintainer | 4 file(s) | 22933 | 0 (promoted) | zero |
| `u27-reports-round-1.C1_tree_absent_refusal` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-1.C2_tree_anchored_at_zero` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-1.C4_placement_count` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-2.C3_uncovered_order` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 25 | 2 | killed |
| `u27-reports-round-2.C3b_tie_break` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-3-fixes.F6_folder_count_overwrite` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 25 | 2 | killed |
| `u27-reports-round-1.L1_distinct_tracks` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-1.L3_empty_tempo_is_zero` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-1.L4_median_even` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-1.L5_unused_buckets` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-1.L6_entries_in_no_playlist` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 1 | killed |
| `u27-reports-round-1.L7_shape_governed_filter` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 2 | killed |
| `u27-reports-round-2.L2_genre_parent` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 2 | killed |
| `u27-reports-round-3-fixes.F2_depth_origin` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 1 | killed |
| `r154-b.B11_marker_name_safety` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 5 | killed |
| `r154-b.B9_marker_failure_fails_the_portion` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 1 | killed |
| `r222-a.A1_nothing_held` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 5 | killed |
| `r222-a.A2_boundary_not_strict` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 3 | killed |

## Zero rows and what they owe

- `r757-a.E9_stats_interval_zero` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-b1.E13_runner_times_nothing` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `r757-a.E5_mode_read_backwards`

comparison_mode: report fast for a command without the option and full for one with it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E5_mode_read_backwards`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_only_a_full_mirror_moves_the_date_of_the_last_full_comparison`
  - `tests/test_backup_comparison.py::test_the_frozen_mode_is_the_one_the_plan_is_built_in`
  - `tests/test_backup_comparison.py::test_the_two_modes_differ_by_the_listing_option_and_by_nothing_else`
  - `tests/test_backup_comparison.py::test_totals_that_could_not_be_read_are_none_and_never_zero`

Old text:

```
    return COMPARISON_FAST if FAST_LIST in command.argv else COMPARISON_FULL
```

New text:

```
    return COMPARISON_FAST if FAST_LIST not in command.argv else COMPARISON_FULL
```

### `r757-a.E6_unread_total_is_zero`

_count: answer zero for a total rclone did not give, so an unread run says it sent nothing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E6_unread_total_is_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_totals_that_could_not_be_read_are_none_and_never_zero`

Old text:

```
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value
```

New text:

```
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0
    return value
```

### `r757-a.E7_first_totals_win`

comparison_report: keep the first totals logged and not the last

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E7_first_totals_win`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_the_last_totals_logged_are_the_ones_reported`

Old text:

```
        if isinstance(found, dict):
            stats = found
```

New text:

```
        if isinstance(found, dict) and not stats:
            stats = found
```

### `r757-a.E8_failed_mirror_reports_nothing`

run_backup: read the comparison only when the mirror returned zero

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E8_failed_mirror_reports_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_failed_mirror_says_why_in_words_and_how_far_it_got`

Old text:

```
            if command.label == MIRROR:
```

New text:

```
            if command.label == MIRROR and result.returncode == 0:
```

### `r757-a.E9_stats_interval_zero`

MIRROR_STATS_ARGS: a stats interval of zero, at which rclone logs no totals at all

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E9_stats_interval_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    "--stats", "1h",
```

New text:

```
    "--stats", "0",
```

### `r757-b1.E10_fast_run_records_a_full_comparison`

run_backup: record a full comparison for either mode, so doctor says one ran after every fast backup

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-b1.json`, row `E10_fast_run_records_a_full_comparison`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_only_a_full_mirror_moves_the_date_of_the_last_full_comparison`

Old text:

```
                    and comparison["mode"] == COMPARISON_FULL
```

New text:

```
                    and comparison["mode"] in (COMPARISON_FULL, COMPARISON_FAST)
```

### `r757-b1.E11_full_run_records_nothing`

run_backup: never record a full comparison, so doctor asks for one for ever

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-b1.json`, row `E11_full_run_records_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_only_a_full_mirror_moves_the_date_of_the_last_full_comparison`

Old text:

```
                    and comparison["mode"] == COMPARISON_FULL
```

New text:

```
                    and False
```

### `r757-b1.E12_plain_line_dropped`

_said: drop a line that is not a logged object, the review's fix

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-b1.json`, row `E12_plain_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_failed_mirror_says_why_in_words_and_how_far_it_got`

Old text:

```
        if not isinstance(entry, dict):
            lines.append(line)
```

New text:

```
        if not isinstance(entry, dict):
            pass
```

### `r757-b1.E13_runner_times_nothing`

subprocess_runner: report no elapsed time

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-b1.json`, row `E13_runner_times_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        elapsed=time.monotonic() - started,
```

New text:

```
        elapsed=None,
```

### `u27-reports-round-1.C1_tree_absent_refusal`

Drop the refusal for a governed tree the export does not hold, so every entry reports uncovered

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C1_tree_absent_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything`

Old text:

```
    if not view.has_folder(tree.display):
        raise _refuse_absent(tree)

```

New text:

```
(empty)
```

### `u27-reports-round-1.C2_tree_anchored_at_zero`

Anchor the governed-path filter at position zero, the shape that reported nothing for a nested tree

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C2_tree_anchored_at_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_inside_another_folder_is_still_the_governed_tree`

Old text:

```
        playlist.path for playlist in view.playlists if wanted in playlist.path[:-1]
```

New text:

```
        playlist.path for playlist in view.playlists if playlist.path[:1] == (wanted,)
```

### `u27-reports-round-1.C4_placement_count`

Keep only the first placement per track, so a track filed twice reports one

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C4_placement_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_covered_track_names_every_path_under_the_tree_that_holds_it`

Old text:

```
            held.setdefault(track_id, []).append(playlist.path)
```

New text:

```
            held.setdefault(track_id, [playlist.path])
```

### `u27-reports-round-2.C3_uncovered_order`

Round 1 zero, re-run against the replacement guard: drop the deterministic order

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-2.json`, row `C3_uncovered_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_the_uncovered_list_is_ordered_BY_ARTIST_AND_NOT_BY_THE_WALK`
  - `tests/modules/test_reports_engines.py::test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order`

Old text:

```
        uncovered=tuple(sorted(uncovered, key=_by_name)),
```

New text:

```
        uncovered=tuple(uncovered),
```

### `u27-reports-round-2.C3b_tie_break`

Sort on artist and name alone, leaving the tie to the walk

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-2.json`, row `C3b_tie_break`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order`

Old text:

```
    return (placement.entry.artist, placement.entry.name, placement.entry.track_id)
```

New text:

```
    return (placement.entry.artist, placement.entry.name, "")
```

### `u27-reports-round-3-fixes.F6_folder_count_overwrite`

Count a playlist's raw length again, so folder rows stop reconciling with placements

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-3-fixes.json`, row `F6_folder_count_overwrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_folder_count_never_exceeds_what_the_collection_can_account_for`
  - `tests/modules/test_reports_engines.py::test_two_playlists_sharing_a_display_path_add_up_rather_than_overwrite`

Old text:

```
        counts.setdefault(playlist.path, 0)
        for track_id in playlist.track_ids:
            if track_id not in known:
                continue
            counts[playlist.path] += 1
            held.setdefault(track_id, []).append(playlist.path)
```

New text:

```
        counts[playlist.path] = len(playlist.track_ids)
        for track_id in playlist.track_ids:
            held.setdefault(track_id, []).append(playlist.path)
```

### `u27-reports-round-1.L1_distinct_tracks`

Sum the sub-playlists instead of counting distinct tracks, the double count the docstring names

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L1_distinct_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_genre_counts_distinct_tracks_rather_than_summing_its_playlists`

Old text:

```
                tracks=len(tracks),
```

New text:

```
                tracks=playlists and sum(len(p.track_ids) for p in view.playlists if p.path[: len(folder)] == folder and len(p.path) > len(folder)),
```

### `u27-reports-round-1.L3_empty_tempo_is_zero`

Report an unreadable library as a tempo range of zero rather than as unknown

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L3_empty_tempo_is_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_library_with_no_readable_head_reports_none_rather_than_zero`

Old text:

```
    if not found:
        return TempoSpread(readable=0, unreadable=unreadable)

```

New text:

```
    if not found:
        return TempoSpread(
            readable=0, unreadable=unreadable, lowest=0.0, highest=0.0, median=0.0
        )

```

### `u27-reports-round-1.L4_median_even`

Take the upper middle instead of averaging the pair on an even population

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L4_median_even`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tempo_median_over_an_even_population_averages_the_middle_pair`

Old text:

```
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2

```

New text:

```
    return ordered[middle]

```

### `u27-reports-round-1.L5_unused_buckets`

Report no unused buckets at all

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L5_unused_buckets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_declared_bucket_with_no_folder_is_a_gap`

Old text:

```
            unused_buckets=tuple(sorted(declared_ids - present_ids)),
```

New text:

```
            unused_buckets=(),
```

### `u27-reports-round-1.L6_entries_in_no_playlist`

Count every entry as in no playlist

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L6_entries_in_no_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_the_gaps_count_entries_with_no_head_and_entries_in_no_playlist`

Old text:

```
            entries_in_no_playlist=sum(1 for entry in view.entries if not entry.playlists),
```

New text:

```
            entries_in_no_playlist=len(view.entries),
```

### `u27-reports-round-1.L7_shape_governed_filter`

Measure the tree shape over every folder in the export rather than the governed tree

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L7_shape_governed_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_taxonomy_whose_tree_this_library_does_not_use_reports_no_genres`
  - `tests/modules/test_reports_engines.py::test_the_shape_measures_the_governed_tree_from_its_own_node`

Old text:

```
    governed_folders = [
        path for path in view.folders if tree_display == path[-1] or tree_display in path[:-1]
    ]

```

New text:

```
    governed_folders = list(view.folders)

```

### `u27-reports-round-2.L2_genre_parent`

Round 1 zero, re-run against the replacement guards: loosen the genre filter

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-2.json`, row `L2_genre_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_folder_below_a_genre_is_not_itself_a_genre`
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder`

Old text:

```
        if len(folder) < 2 or folder[-2] != tree_display:
```

New text:

```
        if len(folder) < 2 or tree_display not in folder:
```

### `u27-reports-round-3-fixes.F2_depth_origin`

Measure the tree depth from the export root again rather than from the tree's own node

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-3-fixes.json`, row `F2_depth_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder`

Old text:

```
    try:
        return len(path) - path.index(tree_display)
    except ValueError:  # pragma: no cover - callers filter to governed paths
        return 0
```

New text:

```
    return len(path)
```

### `r154-b.B11_marker_name_safety`

Write a marker for any identity at all, so one carrying a separator or a dot segment is interpolated into a remote path

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B11_marker_name_safety`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[..]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[.hidden]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[has space]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[has/slash]`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`

Old text:

```
    if not _MARKER_IDENTITY.fullmatch(folded):
        return None
```

New text:

```
    if False:
        return None
```

### `r154-b.B9_marker_failure_fails_the_portion`

Let a marker that cannot be written fail the database portion, which skips the settings and publishes no age over a good copy

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B9_marker_failure_fails_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_marker_that_cannot_be_written_warns_and_does_not_fail_the_backup`

Old text:

```
            if result.returncode != 0 and command.label == SNAPSHOT_IDENTITY:
```

New text:

```
            if False and command.label == SNAPSHOT_IDENTITY:
```

### `r222-a.A1_nothing_held`

Hold nothing, which is the finding itself: the rotation counts attempts again and a retry that succeeds purges the failed attempt's archive

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A1_nothing_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
```

New text:

```
    held = []
```

### `r222-a.A2_boundary_not_strict`

Hold a folder named exactly at the floor, so the last completed run's own folder is never settled and survives every later run

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A2_boundary_not_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`

Old text:

```
(floor is None or name > floor)]
```

New text:

```
(floor is None or name >= floor)]
```

