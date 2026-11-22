# Mutation table: u310-replay-after-c

Measured by `scripts/mutate.py` on 2026-11-22 23:21 UTC, branch `HEAD` at `3ab6abf3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22849 collected. pytest invocations for this batch: 73.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 9, each measured by this driver.

Known failures: 254 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/sp/known-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22849 against 22849. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u243.D10_prefix_order_fewest_first` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 1 | killed |
| `u243.D11_refusal_names_no_prefix` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 3 | killed |
| `u243.D12_refusal_offers_no_rule` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 2 | killed |
| `u243.D1_id_class_takes_a_dot` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 2 | killed |
| `u243.D2_end_anchor_is_dollar` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 1 | killed |
| `u243.D3_no_end_anchor` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 4 | killed |
| `u243.D4_search_not_match` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 1 | killed |
| `u243.D5_spelling_not_asked` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 17 | killed |
| `u243.D6_disk_not_asked` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 5 | killed |
| `u243.D7_an_error_reads_as_absent` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 3 | killed |
| `u243.D8_something_there_reads_as_absent` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 1 | killed |
| `u243.D9_streaming_still_counted_unmapped` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 3 | killed |
| `r1844.N17_screen_silent` | `src/cratekit/deletion/cli.py` | user | 2 file(s) | 373 | 6 | killed |
| `r239-b.S6_delete_key_off` | `src/cratekit/deletion/cli.py` | user | 7 file(s) | 723 | 1 | killed |
| `u243.D14_screen_never_says_ignored` | `src/cratekit/deletion/cli.py` | user | 2 file(s) | 353 | 2 | killed |
| `r1037.M7_earlier_landing_kept` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1037.M8_playlist_ids_live_only` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 9 | killed |
| `r1844.N10_numbered_ignored` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1844.N11_marked_uuid_unread` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1844.N12_record_uuid_unread` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 5 | killed |
| `r1844.N1_uuid_proof_dropped` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 5 | killed |
| `r1844.N2_id_alone_proves` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 3 | killed |
| `r1844.N3_empty_uuid_proves` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1844.N4_playlist_proof_dropped` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 11 | killed |
| `r1844.N5_any_playlist_proves` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1844.N6_no_playlist_proves` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 5 | killed |
| `r1844.N8_nothing_absent_listed` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1844.N9_rolled_back_unlisted` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 7 | killed |
| `u288.M23_recorded_identity` | `src/cratekit/deletion/library.py` | user | 2 file(s) | 405 | 1 | killed |
| `r1037.M9_recorded_not_excluded` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1844.N14_uuids_not_passed` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 4 | killed |
| `r1844.N15_baseline_count_lost` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1844.N16_review_count_lost` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 5 | killed |
| `r44-b.R1_rules_drop_identity` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-b.R5_both_looks_gone` | `src/cratekit/deletion/run.py` | maintainer | 1 file(s) | 331 | 4 | killed |
| `r44-b.X2_suspect_anchor` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `r431-a.A10_the_shared_companion_goes_with_the_first_lift` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1141 | 4 | killed |
| `r431-a.A11_a_lifted_tombstone_still_accounts` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1141 | 3 | killed |
| `r431-a.A12_the_named_tombstone_accounts_for_itself` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1141 | 6 | killed |
| `r431-a.A13_accounting_by_stripping_alone` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1141 | 1 | killed |
| `r431-a.A14_accounting_by_pointer_alone` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1141 | 1 | killed |
| `r431-a.A3_stripped_from_the_title_column` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1141 | 2 | killed |
| `r431-a.A4_the_tombstone_names_no_companion` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1141 | 2 | killed |
| `r1037.M13_sight_renumbers` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 3 | killed |
| `r1037.M14_sight_at_the_watermark` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 15 | killed |
| `r1037.M15_sight_keeps_held` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1037.M16_advance_drops_sightings` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1037.M17_sightings_unchecked` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1037.M18_sighting_value_unchecked` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1037.M19_version_two_refused` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 114 | killed |
| `r1037.M1_identity_unchecked` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1844.N7_held_rows_read_absent` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 35 | killed |
| `r1037.M10_landed_not_joined` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 14 | killed |
| `r1037.M11_sightings_never_forgotten` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1037.M12_playlists_always_held` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 8 | killed |
| `r431-a.A15_the_verb_lifts_through_the_store` | `src/cratekit/deletion/run.py` | user | 2 file(s) | 366 | 6 | killed |
| `r44-b.R2_no_gate_at_the_plan` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 4 | killed |
| `r44-b.R3_no_look_at_the_loop_top` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `r44-b.R4_no_look_after_the_recheck` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-b.X1_library_root_gate` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r431-a.A5_the_companion_names_no_tombstone` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1141 | 7 | killed |
| `u27-reports-round-3-fixes.F4_absent_flag_never_set` | `src/cratekit/deletion/trash.py` | user | 2 file(s) | 748 | 1 | killed |

## Row definitions

### `u243.D10_prefix_order_fewest_first`

reference_set: unmapped prefixes sorted fewest first, so the refusal names the smallest groups

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D10_prefix_order_fewest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule`

Old text:

```
key=lambda pair: (-pair[1], pair[0])
```

New text:

```
key=lambda pair: (pair[1], pair[0])
```

### `u243.D11_refusal_names_no_prefix`

assert_complete: the prefixes are left out of the refusal's sentence

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D11_refusal_names_no_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_refusal_names_at_most_five_prefixes_and_counts_the_rest`
  - `tests/test_deletion_streaming.py::test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule`
  - `tests/test_deletion_streaming.py::test_delete_review_still_refuses_an_unmapped_local_row_beside_streaming_rows`

Old text:

```
        f"cannot resolve{f' ({under})' if under else ''}, "
```

New text:

```
        f"cannot resolve, "
```

### `u243.D12_refusal_offers_no_rule`

assert_complete: the location_prefix_map step is not offered

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D12_refusal_offers_no_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_refusal_with_no_dead_anchor_offers_no_directory_to_mount`
  - `tests/test_deletion_streaming.py::test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule`

Old text:

```
                for prefix, count in named
            ),
```

New text:

```
                for prefix, count in ()
            ),
```

### `u243.D1_id_class_takes_a_dot`

_STREAMING_LOCATION: the id class takes any character but a slash, so /v4/catalog/tracks/123.flac/ is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D1_id_class_takes_a_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123.flac/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/12_3/]`

Old text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?\Z")
```

New text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[^/]+/?\Z")
```

### `u243.D2_end_anchor_is_dollar`

_STREAMING_LOCATION: \Z becomes $, which also accepts a trailing newline

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D2_end_anchor_is_dollar`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/\n]`

Old text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?\Z")
```

New text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?$")
```

### `u243.D3_no_end_anchor`

_STREAMING_LOCATION: no end anchor, so /v4/catalog/tracks/123/track.flac is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D3_no_end_anchor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123.flac/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/\n]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/track.flac]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/12_3/]`

Old text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?\Z")
```

New text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+")
```

### `u243.D4_search_not_match`

_streaming: search rather than match, so a spelling under another directory is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D4_search_not_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/Elsewhere/v4/catalog/tracks/123/]`

Old text:

```
    if not _STREAMING_LOCATION.match(text):
```

New text:

```
    if not _STREAMING_LOCATION.search(text):
```

### `u243.D5_spelling_not_asked`

_streaming: the spelling test is dropped, so every unmapped row with nothing at it is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D5_spelling_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 17 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_prefix_rule_whose_target_is_not_there_refuses_rather_than_proving_nothing`
  - `tests/test_deletion.py::test_a_refusal_with_no_dead_anchor_offers_no_directory_to_mount`
  - `tests/test_deletion.py::test_an_unresolvable_active_row_makes_the_whole_run_refuse`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/Elsewhere/v4/catalog/tracks/123/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/V4/catalog/tracks/123/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4//catalog/tracks/123/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/albums/123/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks//]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123.flac/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/\n]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/track.flac]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/12_3/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v5/catalog/tracks/123/]`
  - `tests/test_deletion_streaming.py::test_a_refusal_names_at_most_five_prefixes_and_counts_the_rest`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if not _STREAMING_LOCATION.match(text):
        return False
```

New text:

```
    if False:
        return False
```

### `u243.D6_disk_not_asked`

_streaming: the stat is not asked, so a streaming spelling with a file at it is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D6_disk_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 5 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_is_asked_about_on_the_disk`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[None]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer1]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer2]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer3]`

Old text:

```
    try:
        stat(text)
    except FileNotFoundError:
        return True
    except (OSError, ValueError):
        return False
    return False
```

New text:

```
    return True
```

### `u243.D7_an_error_reads_as_absent`

_streaming: a stat error other than not found reads as nothing there, failing open

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D7_an_error_reads_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer1]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer2]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer3]`

Old text:

```
    except (OSError, ValueError):
        return False
    return False
```

New text:

```
    except (OSError, ValueError):
        return True
    return False
```

### `u243.D8_something_there_reads_as_absent`

_streaming: a stat that answers, a file or directory at the spelling, reads as nothing there

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D8_something_there_reads_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[None]`

Old text:

```
    except (OSError, ValueError):
        return False
    return False
```

New text:

```
    except (OSError, ValueError):
        return False
    return True
```

### `u243.D9_streaming_still_counted_unmapped`

reference_set: a streaming row is counted but also left unmapped, so the run still refuses

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D9_streaming_still_counted_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_library_with_streaming_rows_offers_the_removed_file`
  - `tests/test_deletion_streaming.py::test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule`
  - `tests/test_deletion_streaming.py::test_delete_review_trashes_a_removed_file_beside_streaming_rows`

Old text:

```
                streaming.append(row.content_id)
                continue
```

New text:

```
                streaming.append(row.content_id)
```

### `r1844.N17_screen_silent`

the gate's screen never shows the landings read as rolled back

- File: `src/cratekit/deletion/cli.py`
- Source: `r1844.json`, row `N17_screen_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`
- Collected: 373 against a baseline of 373
- Kills: 6 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted`
  - `tests/test_delete_landed_removed.py::test_the_first_review_counts_a_landing_already_rolled_back`

Old text:

```
    if found.rolled_back:
```

New text:

```
    if False:
```

### `r239-b.S6_delete_key_off`

delete review's open passes unlock=False

- File: `src/cratekit/deletion/cli.py`
- Source: `r239-b.json`, row `S6_delete_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
    return rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
```

New text:

```
    return rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg, unlock=False)
```

### `u243.D14_screen_never_says_ignored`

deletion.cli._shown: the count of rows excused as no local file is never put on the gate screen

- File: `src/cratekit/deletion/cli.py`
- Source: `u243.json`, row `D14_screen_never_says_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 353 against a baseline of 353
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_deletion_streaming.py::test_delete_review_trashes_a_removed_file_beside_streaming_rows`

Old text:

```
    if ignored:
        shown["ignored, not local files"] = ignored
```

New text:

```
    if False:
        shown["ignored, not local files"] = ignored
```

### `r1037.M7_earlier_landing_kept`

landed_absences: keep the earlier of two landings naming one row

- File: `src/cratekit/deletion/library.py`
- Source: `r1037.json`, row `M7_earlier_landing_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_one_row_two_landings_name_keeps_the_later_landings_count`

Old text:

```
            if seen is None or seen.landed < sequence:
```

New text:

```
            if seen is None or seen.landed > sequence:
```

### `r1037.M8_playlist_ids_live_only`

playlist_ids: count no playlist at all, so every landing reads as rolled back

- File: `src/cratekit/deletion/library.py`
- Source: `r1037.json`, row `M8_playlist_ids_live_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 9 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`

Old text:

```
    return frozenset(str(getattr(row, "ID", "")) for row in playlists if getattr(row, "ID", None))
```

New text:

```
    return frozenset()
```

### `r1844.N10_numbered_ignored`

LandedRead.unasked: count every rolled back landing, a batch already offered and tidied included

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N10_numbered_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
        return sum(1 for rows in self.rolled_back if rows - asked)
```

New text:

```
        return sum(1 for rows in self.rolled_back if rows)
```

### `r1844.N11_marked_uuid_unread`

read_collection: keep the UUID of live rows only, so a marked landed row no longer proves its landing

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N11_marked_uuid_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_read_collection_keeps_each_rows_uuid_read_only`

Old text:

```
        uuids[_identifier(row, "ID")] = _text(row, "UUID")
        if not trees.soft_delete_marker(row):
```

New text:

```
        if not trees.soft_delete_marker(row):
            uuids[_identifier(row, "ID")] = _text(row, "UUID")
```

### `r1844.N12_record_uuid_unread`

landed_absences: the record's UUID is not read, so no row proves its landing

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N12_record_uuid_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
            uuid = entry.get(LANDED_UUID_KEY)
```

New text:

```
            uuid = entry.get("UUID")
```

### `r1844.N1_uuid_proof_dropped`

_landing_stands: never read a landed row held under its UUID as proof, so a landing whose playlist was deleted by hand is read as rolled back (the defect)

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N1_uuid_proof_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
    if any(uuid and uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
```

New text:

```
    if False:
```

### `r1844.N2_id_alone_proves`

_landing_stands: a row held under the landed id proves the landing whatever its UUID, so a later import's id reads a rolled back landing as standing

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N2_id_alone_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 3 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
    if any(uuid and uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
```

New text:

```
    if any(content_id in uuids for content_id, _columns, uuid in rows):
```

### `r1844.N3_empty_uuid_proves`

_landing_stands: a row recorded with no UUID matches a held row holding none

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N3_empty_uuid_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
    if any(uuid and uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
```

New text:

```
    if any(uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
```

### `r1844.N4_playlist_proof_dropped`

_landing_stands: every playlist held no longer proves the landing, so a lone landed track removed while its playlist stays is never offered

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N4_playlist_proof_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 11 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_one_row_two_landings_name_keeps_the_later_landings_count`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`

Old text:

```
    return all(playlist_held(str(one)) for one in playlists)
```

New text:

```
    return False
```

### `r1844.N5_any_playlist_proves`

_landing_stands: one playlist of the landing held is enough, not all of them

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N5_any_playlist_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_one_of_whose_playlists_is_gone_offers_nothing`

Old text:

```
    return all(playlist_held(str(one)) for one in playlists)
```

New text:

```
    return any(playlist_held(str(one)) for one in playlists)
```

### `r1844.N6_no_playlist_proves`

_landing_stands: a landing that made no playlist reads as standing, so a rolled back landing into a playlist already there is offered

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N6_no_playlist_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_restored_landing_into_a_playlist_already_there_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
    if not isinstance(playlists, (list, tuple)) or not playlists:
```

New text:

```
    if not isinstance(playlists, (list, tuple)):
```

### `r1844.N8_nothing_absent_listed`

landed_absences: a landing with every row held is still weighed and listed as rolled back

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N8_nothing_absent_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
        if not absent:
            continue

```

New text:

```
(empty)
```

### `r1844.N9_rolled_back_unlisted`

landed_absences: a landing read as rolled back is not listed, so the gate never counts it

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N9_rolled_back_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 7 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`
  - `tests/test_delete_landed_removed.py::test_the_first_review_counts_a_landing_already_rolled_back`

Old text:

```
            rolled_back.append(frozenset(content_id for content_id, _columns in absent))
```

New text:

```
            pass
```

### `u288.M23_recorded_identity`

recorded_removals: read a record of another database as this one's

- File: `src/cratekit/deletion/library.py`
- Source: `u288.json`, row `M23_recorded_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_deletion.py`
- Collected: 405 against a baseline of 405
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_recorded_removal_is_read_only_for_its_own_database_and_a_row_still_absent`

Old text:

```
        if str(recorded.get("database_identity") or "") != str(database_identity):
```

New text:

```
        if False:
```

### `r1037.M9_recorded_not_excluded`

plan: a row sync removed recorded is read again as a landed absence, so one row is two candidates

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M9_recorded_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`

Old text:

```
        present=held | {row.content_id for row in recorded},
```

New text:

```
        present=held,
```

### `r1844.N14_uuids_not_passed`

run.plan: the held rows' UUIDs are not handed to the landed row reader

- File: `src/cratekit/deletion/run.py`
- Source: `r1844.json`, row `N14_uuids_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 4 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`

Old text:

```
        uuids=seen.uuids,
```

New text:

```
        uuids={},
```

### `r1844.N15_baseline_count_lost`

run.plan: the run that baselines carries no rolled back count

- File: `src/cratekit/deletion/run.py`
- Source: `r1844.json`, row `N15_baseline_count_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_first_review_counts_a_landing_already_rolled_back`

Old text:

```
            baselined_over=len(seen.removed),
            rolled_back=landings.unasked(mark.absent),
```

New text:

```
            baselined_over=len(seen.removed),
```

### `r1844.N16_review_count_lost`

run.plan: an ordinary review carries no rolled back count

- File: `src/cratekit/deletion/run.py`
- Source: `r1844.json`, row `N16_review_count_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted`

Old text:

```
        ambiguous=ambiguous,
        rolled_back=landings.unasked(mark.absent),
```

New text:

```
        ambiguous=ambiguous,
```

### `r44-b.R1_rules_drop_identity`

Build the pass's rules from configuration without each rule's recorded identity

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R1_rules_drop_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_the_rules_the_pass_builds_from_configuration_carry_each_recorded_identity`

Old text:

```
        locations.PrefixRule(source, target, volume_id)
```

New text:

```
        locations.PrefixRule(source, target)
```

### `r44-b.R5_both_looks_gone`

Composite for R3 and R4: make the per file look a no-op, so only the plan's gate stands

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R5_both_looks_gone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_stops_a_confirmed_move`
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`

Old text:

```
    if answered.resolved is None:
        return
    resolved = locations.resolve_recorded_path(
```

New text:

```
    return
    resolved = locations.resolve_recorded_path(
```

### `r44-b.X2_suspect_anchor`

Existing guard, sampled: never hold a row because its anchor proved nothing

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `X2_suspect_anchor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_stale_empty_mount_point_writes_no_tombstone_and_retires_no_row`
  - `tests/test_deletion.py::test_an_unanswered_removal_under_a_stale_mount_point_is_not_retired_either`

Old text:

```
    return answered.anchor is not None and answered.anchor in references.suspect_anchors
```

New text:

```
    return False
```

### `r431-a.A10_the_shared_companion_goes_with_the_first_lift`

Lifting takes every companion the tombstone accounts for, whoever else still does

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A10_the_shared_companion_goes_with_the_first_lift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1141 against a baseline of 1141
- Kills: 4 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_shared_companion_survives_a_lift_even_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
    return tuple(sorted(mine - still_accounted_for))
```

New text:

```
    return tuple(sorted(mine))
```

### `r431-a.A11_a_lifted_tombstone_still_accounts`

A tombstone that was itself lifted still holds the shared companion, so the second lift strands it

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A11_a_lifted_tombstone_still_accounts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1141 against a baseline of 1141
- Kills: 3 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
            and other.suppressing
            and other.suppression_id != named.suppression_id
```

New text:

```
            and other.suppression_id != named.suppression_id
```

### `r431-a.A12_the_named_tombstone_accounts_for_itself`

The tombstone being lifted counts as still accounting, so no companion is ever lifted

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A12_the_named_tombstone_accounts_for_itself`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1141 against a baseline of 1141
- Kills: 6 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_one_write_and_so_is_lifting_it`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
            and other.suppressing
            and other.suppression_id != named.suppression_id
```

New text:

```
            and other.suppressing
```

### `r431-a.A13_accounting_by_stripping_alone`

_accounts_for drops the pointer, so a moved stripping rule strands a companion and takes a shared one

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A13_accounting_by_stripping_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1141 against a baseline of 1141
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`

Old text:

```
    found = {str(credited.payload.get(UNCREDITED_ID_FIELD) or "")}
```

New text:

```
    found = {""}
```

### `r431-a.A14_accounting_by_pointer_alone`

_accounts_for drops the stripping, so a tombstone with no pointer accounts for nothing

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A14_accounting_by_pointer_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1141 against a baseline of 1141
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`

Old text:

```
    if stripped:
        found.add(
```

New text:

```
    if stripped and not stripped:
        found.add(
```

### `r431-a.A3_stripped_from_the_title_column`

The companion is stripped from the Title column and not from the composed identity, so a mix name in the version column is lost

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A3_stripped_from_the_title_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1141 against a baseline of 1141
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_uncredited_tombstone.py::test_the_companion_is_built_from_the_composed_title_not_the_title_column`

Old text:

```
    stripped = tombstone.uncredited_title(verbatim["title"])
```

New text:

```
    stripped = tombstone.uncredited_title(tombstone.fold(row.title))
```

### `r431-a.A4_the_tombstone_names_no_companion`

The tombstone's pointer to its companion is written empty

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A4_the_tombstone_names_no_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1141 against a baseline of 1141
- Kills: 2 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_the_listing_links_the_two_halves_of_one_deletion_in_both_directions`

Old text:

```
            UNCREDITED_ID_FIELD: uncredited_id,
```

New text:

```
            UNCREDITED_ID_FIELD: "",
```

### `r1037.M13_sight_renumbers`

sight: number a row again at every run, so it moves past every advance and is offered again

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M13_sight_renumbers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 3 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says`

Old text:

```
                if content_id in kept or content_id in held:
                    continue
                kept[str(content_id)] = int(counter)
```

New text:

```
                if content_id in held:
                    continue
                kept[str(content_id)] = int(counter)
```

### `r1037.M14_sight_at_the_watermark`

sight: number a new sighting at the watermark, so every outright removal is hidden

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M14_sight_at_the_watermark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 15 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`

Old text:

```
                kept[str(content_id)] = int(counter)
```

New text:

```
                kept[str(content_id)] = existing.sequence
```

### `r1037.M15_sight_keeps_held`

sight: drop no sighting of a row held again

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M15_sight_keeps_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says`

Old text:

```
            kept = {key: value for key, value in existing.absent.items() if key not in held}
```

New text:

```
            kept = dict(existing.absent)
```

### `r1037.M16_advance_drops_sightings`

advance: write the position without the sightings, so the next run renumbers and re-offers

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M16_advance_drops_sightings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says`

Old text:

```
                absent=dict(existing.absent) if existing is not None else {},
```

New text:

```
                absent={},
```

### `r1037.M17_sightings_unchecked`

_recognize: accept sightings of any shape

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M17_sightings_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_watermark_reads_version_one_as_no_sightings_and_refuses_a_bad_one`

Old text:

```
        if not isinstance(absent, Mapping):
            raise self._unusable(f"its sightings are a {type(absent).__name__}, not a mapping")
```

New text:

```
        if not isinstance(absent, Mapping):
            absent = {}
```

### `r1037.M18_sighting_value_unchecked`

_recognize: accept a sighting that is not a whole number

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M18_sighting_value_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_watermark_reads_version_one_as_no_sightings_and_refuses_a_bad_one`

Old text:

```
            if isinstance(sighted, bool) or not isinstance(sighted, int):
```

New text:

```
            if False:
```

### `r1037.M19_version_two_refused`

_recognize: read only version 1, so this build refuses its own document

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M19_version_two_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 114 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_is_one_candidate`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_a_restore_rolled_back_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - ... and 99 more, see the JSON sidecar

Old text:

```
READABLE_VERSIONS = frozenset({1, WATERMARK_VERSION})
```

New text:

```
READABLE_VERSIONS = frozenset({1})
```

### `r1037.M1_identity_unchecked`

landed_absences: read a landing record of any database, so another library's landed rows are offered here

- File: `src/cratekit/deletion/library.py`
- Source: `r1037.json`, row `M1_identity_unchecked`
- Moved: the record preamble of landed_absences and recorded_removals is now one generator, _records, whose record is named recorded; the identity check is dropped from it, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - `tests/test_sync_removed.py::test_a_recorded_removal_is_read_only_for_its_own_database_and_a_row_still_absent`

Old text:

```
        if str(recorded.get("database_identity") or "") != str(database_identity):
            continue
        sequence = recorded.get("sequence")
```

New text:

```
        sequence = recorded.get("sequence")
```

### `r1844.N7_held_rows_read_absent`

landed_absences: a landed row the database holds is read as absent, so a live track's file is offered

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N7_held_rows_read_absent`
- Moved: the formatter split the over long comprehension; the held filter is dropped, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 35 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_is_one_candidate`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_a_restore_rolled_back_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - ... and 20 more, see the JSON sidecar

Old text:

```
            (content_id, columns) for content_id, columns, _uuid in rows if content_id not in held
```

New text:

```
            (content_id, columns) for content_id, columns, _uuid in rows
```

### `r1037.M10_landed_not_joined`

plan: leave the absent landed rows out of the removals, which is the defect R-1037 names

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M10_landed_not_joined`
- Moved: the replace call collapsed onto one argument line; the landed absences are not joined, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 14 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`

Old text:

```
        seen, removed=seen.removed + tuple(one.row(mark.absent[key]) for key, one in absent.items())
```

New text:

```
        seen, removed=seen.removed
```

### `r1037.M11_sightings_never_forgotten`

plan: tell the sightings no row is held, so a row a restore put back keeps its old number

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M11_sightings_never_forgotten`
- Moved: the sight call collapsed onto one line; nothing is held present, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`

Old text:

```
    mark = marks.sight(database_identity=identity, absent=absent, present=held, counter=counter)
```

New text:

```
    mark = marks.sight(database_identity=identity, absent=absent, present=(), counter=counter)
```

### `r1037.M12_playlists_always_held`

_playlists_held: answer every playlist held, so a rolled back landing is offered

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M12_playlists_always_held`
- Moved: the once only playlist read is now functools.cache over the ids; every playlist reads as held, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 8 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_one_of_whose_playlists_is_gone_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_rolled_back_landing_is_kept_by_its_playlist_whatever_the_count`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted`
  - `tests/test_delete_landed_removed.py::test_the_first_review_counts_a_landing_already_rolled_back`

Old text:

```
    return lambda playlist_id: playlist_id in ids()
```

New text:

```
    return lambda playlist_id: True
```

### `r431-a.A15_the_verb_lifts_through_the_store`

run.revoke lifts a tombstone through the store and not through stores.revoke_tombstone, so no companion goes

- File: `src/cratekit/deletion/run.py`
- Source: `r431-a.json`, row `A15_the_verb_lifts_through_the_store`
- Moved: only the comment above the guarded line changed; the verb lifts through the opened store, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_uncredited_tombstone.py`
- Collected: 366 against a baseline of 366
- Kills: 6 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_one_write_and_so_is_lifting_it`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
                # (R-431); tombstones are read first, never needing the declines.
                return stores.revoke_tombstone(cfg, suppression_id, actor=actor)
```

New text:

```
                # (R-431); tombstones are read first, never needing the declines.
                return held.revoke(suppression_id, actor=actor)
```

### `r44-b.R2_no_gate_at_the_plan`

Drop the assertion of every mapped target before the plan resolves a path

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R2_no_gate_at_the_plan`
- Moved: the seams now travel as one mapping and the call is one line; it is deleted, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_under_the_library_root_asks_nothing_of_any_rule_before_it_moves`
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_deletion.py::test_a_volume_holding_only_removed_rows_does_not_settle_off_an_empty_mount_point`

Old text:

```
    session.assert_mapped_volume_identities(cfg, rules, **seams)

```

New text:

```
(empty)
```

### `r44-b.R3_no_look_at_the_loop_top`

Drop the look at the top of the apply loop, before a retirement or a settlement of the plan's answer

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R3_no_look_at_the_loop_top`
- Moved: the seven line volume call became a functools.partial named look, bound to the configuration, the rules and the seams; the loop top's call is deleted, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`

Old text:

```
            look(item)

```

New text:

```
(empty)
```

### `r44-b.R4_no_look_after_the_recheck`

Drop the look after the re-check, before its answer is settled or moved on

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R4_no_look_after_the_recheck`
- Moved: the same partial; the call after the re-check is deleted, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`

Old text:

```
            look(fresh)

```

New text:

```
(empty)
```

### `r44-b.X1_library_root_gate`

Existing guard, sampled: drop the library root's own volume assertion from the pass

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `X1_library_root_gate`
- Moved: the seams now travel as one mapping; the library root's identity check is deleted, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_decoy_volume_at_the_configured_path_refuses_before_anything_resolves`

Old text:

```
    session.assert_volume_identity(cfg, **seams)
    session.assert_mapped_volume_identities(cfg, rules, **seams)
```

New text:

```
    session.assert_mapped_volume_identities(cfg, rules, **seams)
```

### `r431-a.A5_the_companion_names_no_tombstone`

The companion's pointer back is dropped from its payload, so the listing cannot link the pair

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A5_the_companion_names_no_tombstone`
- Moved: the companion's payload is now built into a local before the write, so its indentation changed; the credited id is emptied, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1141 against a baseline of 1141
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - `tests/test_uncredited_tombstone.py::test_a_second_deletion_leaves_the_shared_companion_exactly_as_it_stood`
  - `tests/test_uncredited_tombstone.py::test_the_listing_links_the_two_halves_of_one_deletion_in_both_directions`

Old text:

```
        CREDITED_ID_FIELD: review.suppression_id_for(
            tombstone.STORE_KEY, tombstone.KIND_VERSION, identity
        ),
```

New text:

```
        CREDITED_ID_FIELD: "",
```

### `u27-reports-round-3-fixes.F4_absent_flag_never_set`

Never mark an absent Trash as absent, so doctor cannot tell it from an unwritable one

- File: `src/cratekit/deletion/trash.py`
- Source: `u27-reports-round-3-fixes.json`, row `F4_absent_flag_never_set`
- Moved: the call collapsed onto one argument line; the absent flag is never set, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_doctor.py`
- Collected: 748 against a baseline of 748
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_two_probe_answers_that_made_the_false_red_are_really_different`

Old text:

```
            layout, False, f"{target} is not a directory", absent=not target.exists()
```

New text:

```
            layout, False, f"{target} is not a directory", absent=False
```

