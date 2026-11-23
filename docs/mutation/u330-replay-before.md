# Mutation table: u330-replay-before

Measured by `scripts/mutate.py` on 2026-11-23 16:51 UTC, branch `cloud/979-scripts-back-under-7374-lines` at `2bff472c`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22622 collected. pytest invocations for this batch: 120.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 16:51 UTC for commit `2bff472cbf7d`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 12, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22622 against 22622. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u122.H1_no_hold` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 10 | killed |
| `u122.H2_review_not_held` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 6 | killed |
| `u122.H3_progress_not_held` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 6 | killed |
| `u122.H4_hold_flattened` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 5 | killed |
| `u122.H5_units_only` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 4 | killed |
| `u122.H6_hold_beats_closure` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 4 | killed |
| `u122.H7_attended_beats_hold` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 2 | killed |
| `u122.N1_next_busy_progress_only` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 1 | killed |
| `u122.N2_next_offers_busy` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 2 | killed |
| `u122.N3_next_no_status` | `scripts/board.py` | maintainer | 2 file(s) | 125 | 2 | killed |
| `u124-b19.B19_audit_reads_folder` | `scripts/board.py` | maintainer | 2 file(s) | 149 | 1 | killed |
| `u124.B10_validate_first` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B11_relanded_title` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 2 | killed |
| `u124.B12_highest_not_count` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 6 | killed |
| `u124.B13_separator` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B14_files_deleted` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 4 | killed |
| `u124.B15_closing_reads_folder` | `scripts/board.py` | maintainer | 2 file(s) | 149 | 3 | killed |
| `u124.B17_land_on_main_only` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B18_behind_origin` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B1_untracked_filter` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B2_readme_excluded` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 2 | killed |
| `u124.B3_name_order` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 3 | killed |
| `u124.B4_fence_open` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 2 | killed |
| `u124.B5_unknown_key` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B6_required_keys` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 6 | killed |
| `u124.B7_issue_values` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B8_numbered_title` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B9_empty_body` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u148.C1_one_short_allowed` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 2 | killed |
| `u148.C2_count_off` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 2 | killed |
| `u148.C3_no_count_skips` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 2 | killed |
| `u148.C4_only_none_refused` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 1 | killed |
| `u148.C5_issue_count_dropped` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 2 | killed |
| `u148.L1_old_limit` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 4 | killed |
| `u148.L2_issue_literal` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 6 | killed |
| `u148.N1_truncation_blamed_on_token` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 1 | killed |
| `u148.S1_branch_before_read` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 1 | killed |
| `u148.S2_claims_in_progress` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 1 | killed |
| `u148.W1_full_page_taken` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 3 | killed |
| `u148.W2_whole_off` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 3 | killed |
| `u148.W3_issue_whole_dropped` | `scripts/board.py` | maintainer | 4 file(s) | 185 | 3 | killed |
| `u151.A1_archived_read` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.C1_no_cursor_trusted` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.C2_page_bound_short` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.F1_cursor_typed` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.M1_membership_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.M2_issue_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 2 | killed |
| `u151.N1_number_filter_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.O1_owner_filter_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.O2_owner_case_sensitive` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.U1_unblocks_always_written` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 4 | killed |
| `u151.U2_added_card_zero` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.X1_next_skips_context` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.X2_no_org_fallback` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.X3_status_refusal_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.X4_unseen_project_trusted` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 2 | killed |
| `u151.X5_field_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u158.M1_card_not_judged` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 2 | killed |
| `u158.M2_any_branch_names_a_card` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 1 | killed |
| `u158.M3_implied_close_not_a_reference` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 2 | killed |
| `u187.A1_relayed_answer_never_matches` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 5 | killed |
| `u187.A2_answer_counted_as_a_hold` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 5 | killed |
| `u187.A3_answer_not_read_as_reply` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 3 | killed |
| `u187.A4_heading_drifts` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 5 | killed |
| `u196.S3_empty_search` | `scripts/board.py` | maintainer | 1 file(s) | 7 | 1 | killed |
| `u196.S4_missing_ledger_no_match` | `scripts/board.py` | maintainer | 1 file(s) | 7 | 1 | killed |
| `u203.M1_no_opening_span` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 6 | killed |
| `u203.M2_span_closer_any_follower` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u203.M3_no_sentence_cut` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 4 | killed |
| `u203.M4_sentence_cut_anywhere` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 1 | killed |
| `u203.M5_no_trailing_strip` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 27 | killed |
| `u203.M6_one_pass` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u203.M7_rule_line_is_a_heading` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 1 | killed |
| `u203.M8_ellipsis_not_trailing` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 1 | killed |
| `u203.M9_no_comma_cut` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u291.L1_lanes_back_to_five` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 3 | killed |
| `u291.L2_lanes_one_short` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 3 | killed |
| `u291.L3_lanes_one_over` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 3 | killed |
| `u291.L4_help_names_a_literal` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 1 | killed |
| `u291.L5_default_ignores_the_constant` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u313.B2_landed_twice` | `scripts/board.py` | maintainer | 2 file(s) | 55 | 2 | killed |
| `u313.B3_stale_window_doubled` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 10 | killed |
| `u313.B4_withdrawn_held` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u313.B5_owed_unit_closes` | `scripts/board.py` | maintainer | 2 file(s) | 149 | 41 | killed |
| `u313.B6_refusal_exit_code` | `scripts/board.py` | maintainer | 2 file(s) | 55 | 4 | killed |
| `u314.L10_search_names_no_file` | `scripts/board.py` | maintainer | 1 file(s) | 7 | 2 | killed |
| `u314.L1_archives_unread` | `scripts/board.py` | maintainer | 3 file(s) | 156 | 7 | killed |
| `u314.L2_landing_never_archives` | `scripts/board.py` | maintainer | 2 file(s) | 55 | 1 | killed |
| `u314.L3_archive_header_undercounted` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 4 | killed |
| `u314.L5_duplicate_heading_passes` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u314.L6_misnamed_archive_passes` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u314.L7_removed_heading_reversed` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u314.L8_unchanged_ignored` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u314.L9_archives_at_rev_unread` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u59.B1_per_message_split` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u59.B2_raw_true_on_range` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u59.B3_unit_mapping_ignored` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u59.B4_guess_caveat_dropped` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 1 | killed |
| `u59.B6_duplicate_unit_kept` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 2 | killed |
| `u59.B8_missing_file_raises` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 1 | killed |
| `u81-round-2.B5_owed_argument_ignored` | `scripts/board.py` | user | 1 file(s) | 101 | 2 | killed |
| `u81-round-3.B5_audit_drops_the_detector` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u81-round-3.B5_audit_exit_code` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u81-round-3.B5_owed_default_dropped` | `scripts/board.py` | user | 1 file(s) | 101 | 2 | killed |
| `u81.B5_composite` | `scripts/board.py` | maintainer | 7 file(s) | 2374 | 1 | killed |
| `u81.B5_contradictions_by_number` | `scripts/board.py` | user | 1 file(s) | 101 | 3 | killed |
| `u81.B5_residual_repoint_dropped` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |

## Row definitions

### `u122.H1_no_hold`

Remove the hold: derive_status ignores a held status and derives from the graph

- File: `scripts/board.py`
- Source: `u122.json`, row `H1_no_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 10 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if False:
```

### `u122.H2_review_not_held`

UNDERWAY loses In review, the runner's status, so it reads as drift again

- File: `scripts/board.py`
- Source: `u122.json`, row `H2_review_not_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 6 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In review]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
UNDERWAY = ("In Progress", "In review")
```

New text:

```
UNDERWAY = ("In Progress",)
```

### `u122.H3_progress_not_held`

UNDERWAY loses In Progress, a session's and a lane's status

- File: `scripts/board.py`
- Source: `u122.json`, row `H3_progress_not_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 6 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In Progress]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In Progress]`

Old text:

```
UNDERWAY = ("In Progress", "In review")
```

New text:

```
UNDERWAY = ("In review",)
```

### `u122.H4_hold_flattened`

A held card derives In Progress whatever it held, so In review becomes drift

- File: `scripts/board.py`
- Source: `u122.json`, row `H4_hold_flattened`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In review]`

Old text:

```
        return current

```

New text:

```
        return "In Progress"

```

### `u122.H5_units_only`

The hold applies to units only, the behaviour before the 2026-10-09 amendment

- File: `scripts/board.py`
- Source: `u122.json`, row `H5_units_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if current in UNDERWAY and node["unit"]:
```

### `u122.H6_hold_beats_closure`

The hold is checked before closure, so a closed held card is not Done

- File: `scripts/board.py`
- Source: `u122.json`, row `H6_hold_beats_closure`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[3-In Progress]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[3-In review]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[6-In Progress]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[6-In review]`

Old text:

```
    if node["closed"]:
        return "Done"
    if current in UNDERWAY:
```

New text:

```
    if current in UNDERWAY:
        return current
    if node["closed"]:
        return "Done"
    if False:
```

### `u122.H7_attended_beats_hold`

Attended is checked before the hold, the order the review moved

- File: `scripts/board.py`
- Source: `u122.json`, row `H7_attended_beats_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if node["attended"]:
        return "Attended"
    if current in UNDERWAY:
```

### `u122.N1_next_busy_progress_only`

next counts only In Progress as busy, so an In review card is offered again

- File: `scripts/board.py`
- Source: `u122.json`, row `N1_next_busy_progress_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
.get("status") in UNDERWAY
```

New text:

```
.get("status") == "In Progress"
```

### `u122.N2_next_offers_busy`

next lists a busy card under underway but leaves it in the ready list

- File: `scripts/board.py`
- Source: `u122.json`, row `N2_next_offers_busy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In Progress]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
    ready = [n for n in ready if n["number"] not in busy]
```

New text:

```
    ready = list(ready)
```

### `u122.N3_next_no_status`

next drops the status column, so a reader cannot tell the runner's hold from a session's

- File: `scripts/board.py`
- Source: `u122.json`, row `N3_next_no_status`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 125 against a baseline of 125
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In Progress]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
            print(f"  #{node['number']:<3} {status:<11} {node['title']}")
```

New text:

```
            print(f"  #{node['number']:<3} {node['title']}")
```

### `u124-b19.B19_audit_reads_folder`

audit stops counting a malformed residual file as a contradiction, rerun after the audit test landed

- File: `scripts/board.py`
- Source: `u124-b19.json`, row `B19_audit_reads_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_audit_counts_a_residual_file_that_cannot_land_as_a_contradiction`

Old text:

```
        clashes = clashes + malformed
```

New text:

```
        clashes = clashes
```

### `u124.B10_validate_first`

a malformed file is skipped instead of stopping the landing, so the good ones land

- File: `scripts/board.py`
- Source: `u124.json`, row `B10_validate_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_that_cannot_number_every_file_writes_nothing[files1-u1-b.md]`

Old text:

```
    if problems:
        raise ValueError("; ".join(problems))
    if not parsed:
```

New text:

```
    if not parsed:
```

### `u124.B11_relanded_title`

a title the ledger already holds is numbered again

- File: `scripts/board.py`
- Source: `u124.json`, row `B11_relanded_title`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_a_landing_that_cannot_number_every_file_writes_nothing[files0-R-12 already]`

Old text:

```
    if again:
        raise ValueError("; ".join(again))
```

New text:

```
(empty)
```

### `u124.B12_highest_not_count`

the next number is the ledger's count plus one rather than its highest plus one

- File: `scripts/board.py`
- Source: `u124.json`, row `B12_highest_not_count`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 6 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_an_untracked_draft_is_neither_judged_nor_landed`
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    number = max(titles, default=0)
```

New text:

```
    number = len(titles)
```

### `u124.B13_separator`

landed entries lose the separator line

- File: `scripts/board.py`
- Source: `u124.json`, row `B13_separator`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`

Old text:

```
        text = text.rstrip("\n") + "\n\n---\n\n"
```

New text:

```
        text = text.rstrip("\n") + "\n\n"
```

### `u124.B14_files_deleted`

a landed file is left in the folder

- File: `scripts/board.py`
- Source: `u124.json`, row `B14_files_deleted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    for path, _, _ in parsed:
        path.unlink()
```

New text:

```
    for path, _, _ in parsed:
        pass
```

### `u124.B15_closing_reads_folder`

closing stops reading the residual folder

- File: `scripts/board.py`
- Source: `u124.json`, row `B15_closing_reads_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 149 against a baseline of 149
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[hook]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[range]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[unreadable range]`

Old text:

```
    malformed = residual_file_problems()
    if not problems and not malformed:
```

New text:

```
    malformed = []
    if not problems and not malformed:
```

### `u124.B17_land_on_main_only`

residuals --land runs on any branch

- File: `scripts/board.py`
- Source: `u124.json`, row `B17_land_on_main_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`

Old text:

```
    if branch != "main":
        print(
            f"board: residuals are numbered on main
```

New text:

```
    if branch == "never":
        print(
            f"board: residuals are numbered on main
```

### `u124.B18_behind_origin`

residuals --land numbers on a main behind origin/main

- File: `scripts/board.py`
- Source: `u124.json`, row `B18_behind_origin`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`

Old text:

```
    if behind.returncode == 0 and behind.stdout.strip() not in ("", "0"):
```

New text:

```
    if behind.returncode == 0 and behind.stdout.strip() not in ("", "0") and False:
```

### `u124.B1_untracked_filter`

residual_files returns every file, git's index ignored, so an untracked draft is judged and landed

- File: `scripts/board.py`
- Source: `u124.json`, row `B1_untracked_filter`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_an_untracked_draft_is_neither_judged_nor_landed`

Old text:

```
    if listed.returncode != 0:
        return paths

```

New text:

```
    if listed.returncode == 0 or listed.returncode != 0:
        return paths

```

### `u124.B2_readme_excluded`

the README is read as a residual file

- File: `scripts/board.py`
- Source: `u124.json`, row `B2_readme_excluded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_the_shipped_residual_folder_holds_only_files_that_can_land`

Old text:

```
    paths = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
```

New text:

```
    paths = sorted(p for p in folder.glob("*.md"))
```

### `u124.B3_name_order`

files land in folder listing order rather than name order

- File: `scripts/board.py`
- Source: `u124.json`, row `B3_name_order`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    paths = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
```

New text:

```
    paths = sorted((p for p in folder.glob("*.md") if p.name != "README.md"), reverse=True)
```

### `u124.B4_fence_open`

a file with no opening fence is not refused

- File: `scripts/board.py`
- Source: `u124.json`, row `B4_fence_open`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[**The mechanism.** No frontmatter at all.\n-does not open]`
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[title: T\nfound: today.\n---\n\nBody.\n-does not open]`

Old text:

```
    if not lines or lines[0] != "---":
        raise ValueError("does not open with a frontmatter fence")
```

New text:

```
    if not lines:
        raise ValueError("does not open with a frontmatter fence")
```

### `u124.B5_unknown_key`

an unknown frontmatter key is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B5_unknown_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\nfond: typo\n---\n\nBody.\n-fond]`

Old text:

```
        if key not in RESIDUAL_REQUIRED and key not in RESIDUAL_OPTIONAL:
```

New text:

```
        if key not in RESIDUAL_REQUIRED and key not in RESIDUAL_OPTIONAL and False:
```

### `u124.B6_required_keys`

a missing title or found line is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B6_required_keys`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 6 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\nfound: today.\n---\n\nBody.\n-no title]`
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: No found line\n---\n\nBody.\n-no found]`
  - `tests/test_restart_and_residual_files.py::test_audit_counts_a_residual_file_that_cannot_land_as_a_contradiction`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[hook]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[range]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[unreadable range]`

Old text:

```
        if not meta.get(key):
            raise ValueError(f"frontmatter has no {key}")
```

New text:

```
        if key not in meta and False:
            raise ValueError(f"frontmatter has no {key}")
```

### `u124.B7_issue_values`

issue takes any value

- File: `scripts/board.py`
- Source: `u124.json`, row `B7_issue_values`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\nissue: maybe\n---\n\nBody.\n-issue]`

Old text:

```
        if key in meta and meta[key] not in allowed:
```

New text:

```
        if key in meta and meta[key] not in allowed and False:
```

### `u124.B8_numbered_title`

the number shape widened back to any leading R number

- File: `scripts/board.py`
- Source: `u124.json`, row `B8_numbered_title`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[text9-None]`

Old text:

```
    if re.match(r"R-\d+\.", meta["title"]):
```

New text:

```
    if re.match(r"R-\d+", meta["title"]):
```

### `u124.B9_empty_body`

a file with frontmatter and no body is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B9_empty_body`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\n---\n\n\n-no body]`

Old text:

```
    if not body.strip():
        raise ValueError("has frontmatter and no body")
```

New text:

```
    if body is None:
        raise ValueError("has frontmatter and no body")
```

### `u148.C1_one_short_allowed`

short_of_count lets a read one row short of the count through

- File: `scripts/board.py`
- Source: `u148.json`, row `C1_one_short_allowed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options0-project_items-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`

Old text:

```
    if len(rows) < total:
```

New text:

```
    if len(rows) < total - 1:
```

### `u148.C2_count_off`

short_of_count never compares rows to the count

- File: `scripts/board.py`
- Source: `u148.json`, row `C2_count_off`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options0-project_items-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`

Old text:

```
    if len(rows) < total:
```

New text:

```
    if False:
```

### `u148.C3_no_count_skips`

a read with no count skips the check, the shape before the review

- File: `scripts/board.py`
- Source: `u148.json`, row `C3_no_count_skips`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options1-project_items-no count to check it against]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options3-load_issues-no count to check it against]`

Old text:

```
    if not isinstance(total, int):
        # No count means no check, and a read nobody could check is not whole.
        raise Truncated(
```

New text:

```
    if not isinstance(total, int):
        return
        raise Truncated(
```

### `u148.C4_only_none_refused`

only a missing count is refused, a count that is not a number falls through

- File: `scripts/board.py`
- Source: `u148.json`, row `C4_only_none_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options3-load_issues-no count to check it against]`

Old text:

```
    if not isinstance(total, int):
```

New text:

```
    if total is None:
```

### `u148.C5_issue_count_dropped`

load_issues never checks its read against the repository's count

- File: `scripts/board.py`
- Source: `u148.json`, row `C5_issue_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options3-load_issues-no count to check it against]`

Old text:

```
    short_of_count(issues, int(total) if total.isdigit() else total, "issue")
```

New text:

```
    pass
```

### `u148.L1_old_limit`

READ_LIMIT back to 300, the ceiling the board passed

- File: `scripts/board.py`
- Source: `u148.json`, row `L1_old_limit`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options3-load_issues-no count to check it against]`
  - `tests/test_board_reads.py::test_every_issue_and_project_item_is_read_past_three_hundred`
  - `tests/test_board_reads.py::test_issues_filed_after_the_count_are_read_and_not_refused`

Old text:

```
READ_LIMIT = 5000
```

New text:

```
READ_LIMIT = 300
```

### `u148.L2_issue_literal`

load_issues asks gh for a literal 300 instead of READ_LIMIT

- File: `scripts/board.py`
- Source: `u148.json`, row `L2_issue_literal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 6 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315-316-the whole limit of 315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316-316-the whole limit of 316]`
  - `tests/test_board_reads.py::test_every_issue_and_project_item_is_read_past_three_hundred`
  - `tests/test_board_reads.py::test_issues_filed_after_the_count_are_read_and_not_refused`
  - `tests/test_board_reads.py::test_one_row_under_the_limit_is_taken_as_whole`

Old text:

```
        "all",
        "--limit",
        str(READ_LIMIT),
```

New text:

```
        "all",
        "--limit",
        "300",
```

### `u148.N1_truncation_blamed_on_token`

next catches a truncation as a token that cannot read the board

- File: `scripts/board.py`
- Source: `u148.json`, row `N1_truncation_blamed_on_token`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_next_refuses_a_truncated_item_read_and_names_a_blind_token`

Old text:

```
    except Truncated:
        # A cut short read is not a token that cannot see the board, and the
        # queue below would offer a held card the read missed.
        raise

```

New text:

```
(empty)
```

### `u148.S1_branch_before_read`

start creates the branch before it reads the board, the shape before the review

- File: `scripts/board.py`
- Source: `u148.json`, row `S1_branch_before_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_start_reads_the_board_before_it_branches`

Old text:

```
    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])

    subprocess.run(["git", "checkout", "-b", branch], check=True)

```

New text:

```
    subprocess.run(["git", "checkout", "-b", branch], check=True)
    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])

```

### `u148.S2_claims_in_progress`

start says a card not on the board is In Progress

- File: `scripts/board.py`
- Source: `u148.json`, row `S2_claims_in_progress`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_start_reads_the_board_before_it_branches`

Old text:

```
        print(f"Branch {branch} is checked out, but #{node['number']} is NOT on the")
```

New text:

```
        print(f"Branch {branch} is checked out and #{node['number']} is In Progress.")
```

### `u148.W1_full_page_taken`

whole accepts a read of exactly the limit, a full page read as complete

- File: `scripts/board.py`
- Source: `u148.json`, row `W1_full_page_taken`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[300-330-issue read returned 300 rows]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315-316-the whole limit of 315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316-316-the whole limit of 316]`

Old text:

```
    if len(rows) >= READ_LIMIT:
```

New text:

```
    if len(rows) > READ_LIMIT:
```

### `u148.W2_whole_off`

whole checks nothing

- File: `scripts/board.py`
- Source: `u148.json`, row `W2_whole_off`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[300-330-issue read returned 300 rows]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315-316-the whole limit of 315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316-316-the whole limit of 316]`

Old text:

```
    if len(rows) >= READ_LIMIT:
```

New text:

```
    if False:
```

### `u148.W3_issue_whole_dropped`

load_issues no longer passes its read through whole

- File: `scripts/board.py`
- Source: `u148.json`, row `W3_issue_whole_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 185 against a baseline of 185
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[300-330-issue read returned 300 rows]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315-316-the whole limit of 315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316-316-the whole limit of 316]`

Old text:

```
    whole(issues, "issue")

```

New text:

```
    pass

```

### `u151.A1_archived_read`

archived cards are read as on the board

- File: `scripts/board.py`
- Source: `u151.json`, row `A1_archived_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_card_read_is_a_page_per_hundred_issues_not_a_call_per_card`

Old text:

```
includeArchived: false
```

New text:

```
includeArchived: true
```

### `u151.C1_no_cursor_trusted`

a page that says more and gives no cursor is followed from the start again

- File: `scripts/board.py`
- Source: `u151.json`, row `C1_no_cursor_trusted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_card_read_that_is_short_or_never_ends_is_refused[150-<lambda>-gave no cursor]`

Old text:

```
        if not after:
            raise Truncated("the project membership read said there was more and gave no cursor")

```

New text:

```
(empty)
```

### `u151.C2_page_bound_short`

the page bound drops its last page, a read of 317 issues refused

- File: `scripts/board.py`
- Source: `u151.json`, row `C2_page_bound_short`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_one_row_under_the_limit_is_taken_as_whole`

Old text:

```
    for _ in range(READ_LIMIT // 100 + 1):
```

New text:

```
    for _ in range(READ_LIMIT // 100):
```

### `u151.F1_cursor_typed`

the cursor goes as -F, which gh would type

- File: `scripts/board.py`
- Source: `u151.json`, row `F1_cursor_typed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_card_read_is_a_page_per_hundred_issues_not_a_call_per_card`

Old text:

```
            args += ["-f", f"after={after}"]
```

New text:

```
            args += ["-F", f"after={after}"]
```

### `u151.M1_membership_count_dropped`

an issue whose memberships come back short is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `M1_membership_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_card_read_that_is_short_or_never_ends_is_refused[5-<lambda>-#1 project membership read returned 1 of the 21]`

Old text:

```
            short_of_count(
                memberships["nodes"], memberships.get("totalCount"),
                f"#{issue['number']} project membership",
            )

```

New text:

```
(empty)
```

### `u151.M2_issue_count_dropped`

an issue read shorter than the repository count is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `M2_issue_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options0-project_items-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options1-project_items-no count to check it against]`

Old text:

```
    short_of_count(seen, total, "project membership")

```

New text:

```
(empty)
```

### `u151.N1_number_filter_dropped`

a card on another project of the same owner counts as this board's

- File: `scripts/board.py`
- Source: `u151.json`, row `N1_number_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_only_this_owners_project_is_the_board_whatever_the_case`

Old text:

```
                if str(project.get("number")) != PROJECT_NUMBER:
                    continue

```

New text:

```
                pass

```

### `u151.O1_owner_filter_dropped`

a card on this project number under another owner counts as this board's

- File: `scripts/board.py`
- Source: `u151.json`, row `O1_owner_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_only_this_owners_project_is_the_board_whatever_the_case`

Old text:

```
                if login.lower() != owner.lower():
                    continue

```

New text:

```
                pass

```

### `u151.O2_owner_case_sensitive`

the owner match becomes case sensitive

- File: `scripts/board.py`
- Source: `u151.json`, row `O2_owner_case_sensitive`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_only_this_owners_project_is_the_board_whatever_the_case`

Old text:

```
                if login.lower() != owner.lower():
```

New text:

```
                if login != owner:
```

### `u151.U1_unblocks_always_written`

Unblocks is rewritten on every card again, the U151 cost

- File: `scripts/board.py`
- Source: `u151.json`, row `U1_unblocks_always_written`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_changed_or_missing_unblocks_number_is_written_once[0-7-written0]`
  - `tests/test_board_cost.py::test_a_changed_or_missing_unblocks_number_is_written_once[2-None-written1]`
  - `tests/test_board_cost.py::test_a_sync_with_no_drift_lists_nothing_and_writes_nothing`
  - `tests/test_board_cost.py::test_an_issue_off_the_board_is_added_then_given_its_status_and_number`

Old text:

```
 and apply and item.get("unblocks") != unblocks:
```

New text:

```
 and apply:
```

### `u151.U2_added_card_zero`

a card sync just added reads as holding 0, so a derived 0 is never written

- File: `scripts/board.py`
- Source: `u151.json`, row `U2_added_card_zero`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_an_issue_off_the_board_is_added_then_given_its_status_and_number`

Old text:

```
"status": None, "unblocks": None}
```

New text:

```
"status": None, "unblocks": 0}
```

### `u151.X1_next_skips_context`

next trusts the card read without asking for the project first

- File: `scripts/board.py`
- Source: `u151.json`, row `X1_next_skips_context`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_next_asks_for_the_project_before_trusting_an_empty_card_read`

Old text:

```
        project_context(owner)
        items = project_items(owner)
```

New text:

```
        items = project_items(owner)
```

### `u151.X2_no_org_fallback`

the context never asks for an organization project

- File: `scripts/board.py`
- Source: `u151.json`, row `X2_no_org_fallback`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_context_is_one_query_for_the_project_its_status_and_unblocks`

Old text:

```
    for kind in ("user", "organization"):
```

New text:

```
    for kind in ("user",):
```

### `u151.X3_status_refusal_dropped`

a project with no Status field is not refused

- File: `scripts/board.py`
- Source: `u151.json`, row `X3_status_refusal_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_the_token_cannot_read_whole_is_refused_by_name[<lambda>-Fail-no single select Status field]`

Old text:

```
    if not status or "options" not in status:
        raise Fail(
```

New text:

```
    if False:
        raise Fail(
```

### `u151.X4_unseen_project_trusted`

a project the token cannot see is not refused

- File: `scripts/board.py`
- Source: `u151.json`, row `X4_unseen_project_trusted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_the_token_cannot_read_whole_is_refused_by_name[gh-Fail-cannot be read with this token]`
  - `tests/test_board_cost.py::test_next_asks_for_the_project_before_trusting_an_empty_card_read`

Old text:

```
    if not project:
        raise Fail(
```

New text:

```
    if False:
        raise Fail(
```

### `u151.X5_field_count_dropped`

a project whose fields come back short is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `X5_field_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_the_token_cannot_read_whole_is_refused_by_name[<lambda>-Truncated-project field read returned 1 of the 101]`

Old text:

```
    short_of_count(fields["nodes"], fields.get("totalCount"), "project field")

```

New text:

```
(empty)
```

### `u158.M1_card_not_judged`

cmd_closing: never judge the card a pull request's head names, so an owed unit merges

- File: `scripts/board.py`
- Source: `u158.json`, row `M1_card_not_judged`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_pull_request_range_closing_a_unit_still_owed_is_refused`
  - `tests/test_pending_units.py::test_the_card_a_head_names_is_judged_even_when_the_range_is_unreadable`

Old text:

```
        if card is not None:
```

New text:

```
        if False:
```

### `u158.M2_any_branch_names_a_card`

pull_request_card: read a card off any owner/N-slug branch, not only a cloud one

- File: `scripts/board.py`
- Source: `u158.json`, row `M2_any_branch_names_a_card`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_only_a_cloud_branch_names_the_card_its_merge_closes[feature/36-x-None]`

Old text:

```
CLOUD_BRANCH_RE = re.compile(r"^cloud/(\d+)-")
```

New text:

```
CLOUD_BRANCH_RE = re.compile(r"^\w+/(\d+)-")
```

### `u158.M3_implied_close_not_a_reference`

cmd_closing: write the implied trailer without its hash, so it closes nothing

- File: `scripts/board.py`
- Source: `u158.json`, row `M3_implied_close_not_a_reference`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_pull_request_range_closing_a_unit_still_owed_is_refused`
  - `tests/test_pending_units.py::test_the_card_a_head_names_is_judged_even_when_the_range_is_unreadable`

Old text:

```
            problems += unresolved_closes(f"Closes #{card}", raw=False)
```

New text:

```
            problems += unresolved_closes(f"Closes {card}", raw=False)
```

### `u187.A1_relayed_answer_never_matches`

_relayed_answer: never match, so the relay thread's Answer from Phillip is read as a session hold and never as his reply

- File: `scripts/board.py`
- Source: `u187.json`, row `A1_relayed_answer_never_matches`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Question for Phillip@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; **Answer from Phillip.**@s+5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-**Answer from Phillip.**@s+6]`

Old text:

```
    return comment_heading(comment.get("body") or "") == HEAD_ANSWER
```

New text:

```
    return False
```

### `u187.A2_answer_counted_as_a_hold`

cloud_state: count a relayed answer among the session's own comments, so an answer alone holds the card

- File: `scripts/board.py`
- Source: `u187.json`, row `A2_answer_counted_as_a_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Question for Phillip@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; **Answer from Phillip.**@s+5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-**Answer from Phillip.**@s+6]`

Old text:

```
    mine = [c for c in ordered if SESSION_MARK in (c.get("body") or "") and not _relayed_answer(c)]
```

New text:

```
    mine = [c for c in ordered if SESSION_MARK in (c.get("body") or "")]
```

### `u187.A3_answer_not_read_as_reply`

cloud_state: drop the relayed answer from the replies after a question, so the card is never offered as answered

- File: `scripts/board.py`
- Source: `u187.json`, row `A3_answer_not_read_as_reply`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Question for Phillip@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; **Answer from Phillip.**@s+5]`

Old text:

```
        if _when(c) > since and (SESSION_MARK not in (c.get("body") or "") or _relayed_answer(c))
```

New text:

```
        if _when(c) > since and (SESSION_MARK not in (c.get("body") or ""))
```

### `u187.A4_heading_drifts`

HEAD_ANSWER: a nearby heading, answer from phil, so the documented heading no longer matches

- File: `scripts/board.py`
- Source: `u187.json`, row `A4_heading_drifts`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Question for Phillip@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; **Answer from Phillip.**@s+5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-**Answer from Phillip.**@s+6]`

Old text:

```
HEAD_ANSWER = "answer from phillip"
```

New text:

```
HEAD_ANSWER = "answer from phil"
```

### `u196.S3_empty_search`

cmd_residuals: drop the refusal of an empty search, which matches every heading

- File: `scripts/board.py`
- Source: `u196.json`, row `S3_empty_search`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 7 against a baseline of 7
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_the_command_prints_hits_and_refuses_an_empty_search`

Old text:

```
        if args.land or not words:
```

New text:

```
        if args.land:
```

### `u196.S4_missing_ledger_no_match`

search_residuals: drop the refusal of a missing ledger, so a search over a file never read says no match

- File: `scripts/board.py`
- Source: `u196.json`, row `S4_missing_ledger_no_match`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 7 against a baseline of 7
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_missing_ledger_is_refused_never_read_as_no_match`

Old text:

```
    if not source.is_file():
        # A missing
```

New text:

```
    if False:
        # A missing
```

### `u203.M1_no_opening_span`

comment_heading: never take an opening emphasised span, so **Brainstorm.** One question waits reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M1_no_opening_span`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 6 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[set-aside-## Started@s+4; **Needs the machine.** It reads the live library.@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[waiting-on-phillip-comments21]`
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[**Brainstorm**.One question waits-brainstorm]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[**Question for Phillip**?Which-question for phillip]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[text5-brainstorm]`

Old text:

```
        span = _OPENING_EMPHASIS.match(text)
```

New text:

```
        span = None
```

### `u203.M2_span_closer_any_follower`

_OPENING_EMPHASIS: accept a closer followed by a letter, so **Brainstorm**s reads as a brainstorm

- File: `scripts/board.py`
- Source: `u203.json`, row `M2_span_closer_any_follower`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorm**s@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[underway-**Brainstorm**s@1]`

Old text:

```
_OPENING_EMPHASIS = re.compile(r"([*_]+)(.+?)\1(?=$|[\s.,:;?!\u2026])")
```

New text:

```
_OPENING_EMPHASIS = re.compile(r"([*_]+)(.+?)\1")
```

### `u203.M3_no_sentence_cut`

_HEADING_END: cut only at a colon or comma, so Needs the machine. The card needs rekordbox is a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M3_no_sentence_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Landed; merge 5c8b26a-landed]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Needs the machine. The card needs rekordbox-needs the machine]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Question for Phillip? Which one-question for phillip]`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:,]")
```

### `u203.M4_sentence_cut_anywhere`

_HEADING_END: cut at any stop, whitespace after it or not, so Landed v0.6.0 today is cut inside the version

- File: `scripts/board.py`
- Source: `u203.json`, row `M4_sentence_cut_anywhere`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Landed v0.6.0 today-landed v0.6.0 today]`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026]")
```

### `u203.M5_no_trailing_strip`

comment_heading: strip emphasis but no trailing punctuation, so ## Brainstorm. reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M5_no_trailing_strip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 27 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm?@1; !B@0.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm?@s+6; !B@s+5.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@1; !B@0.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; !B@s+5.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; **Answer from Phillip.**@s+5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Question for Phillip.**@1; !B@0.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Question for Phillip.**@s+6; !B@s+5.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-Brainstorm!@1; !B@0.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-Brainstorm!@s+6; !B@s+5.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[landed-open-## Started@s+4; **Landed.**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Started@s+4; Withdrawn.@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-**Answer from Phillip.**@s+6]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[set-aside-## Started@s+4; **Needs the machine.** It reads the live library.@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[waiting-on-phillip-## Brainstorm?@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[waiting-on-phillip-## Brainstorm?@s+6]`
  - ... and 12 more, see the JSON sidecar

Old text:

```
            text = text.strip().strip("*_").rstrip(_TRAILING)
```

New text:

```
            text = text.strip().strip("*_")
```

### `u203.M6_one_pass`

comment_heading: strip once instead of to a fixed point, so emphasis left behind a full stop survives

- File: `scripts/board.py`
- Source: `u203.json`, row `M6_one_pass`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Brainstorm**.-brainstorm]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Landed_!-landed]`

Old text:

```
        while text != settled:
```

New text:

```
        for _ in (1,):
```

### `u203.M7_rule_line_is_a_heading`

comment_heading: read a line of emphasis markers alone as the heading, so a rule above Started reads as empty

- File: `scripts/board.py`
- Source: `u203.json`, row `M7_rule_line_is_a_heading`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[\n***\n\nStarted\n-started]`

Old text:

```
        if not text.strip("*_").strip():
            continue
```

New text:

```
        if not text:
            continue
```

### `u203.M8_ellipsis_not_trailing`

_TRAILING: leave the ellipsis character out, so Brainstorm followed by one reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M8_ellipsis_not_trailing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`

Old text:

```
_TRAILING = ".?!;\u2026# \t"
```

New text:

```
_TRAILING = ".?!;# \t"
```

### `u203.M9_no_comma_cut`

_HEADING_END: drop the comma cut, so Started, 2026-10-13. reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M9_no_comma_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[**Brainstorm, round 2.**-brainstorm]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Started, 2026-10-13.-started]`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:]|[.?!;\u2026](?=\s)")
```

### `u291.L1_lanes_back_to_five`

CLOUD_LANES: put the cap back at five, the count before 2026-11-21

- File: `scripts/board.py`
- Source: `u291.json`, row `L1_lanes_back_to_five`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes_and_its_help_says_so`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments2-0-said2-unsaid2]`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments3-0-said3-unsaid3]`

Old text:

```
CLOUD_LANES = 10
```

New text:

```
CLOUD_LANES = 5
```

### `u291.L2_lanes_one_short`

CLOUD_LANES: nine lanes, one short of the cap

- File: `scripts/board.py`
- Source: `u291.json`, row `L2_lanes_one_short`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes_and_its_help_says_so`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments2-0-said2-unsaid2]`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments3-0-said3-unsaid3]`

Old text:

```
CLOUD_LANES = 10
```

New text:

```
CLOUD_LANES = 9
```

### `u291.L3_lanes_one_over`

CLOUD_LANES: eleven lanes, one over the cap

- File: `scripts/board.py`
- Source: `u291.json`, row `L3_lanes_one_over`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes_and_its_help_says_so`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments2-0-said2-unsaid2]`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments3-0-said3-unsaid3]`

Old text:

```
CLOUD_LANES = 10
```

New text:

```
CLOUD_LANES = 11
```

### `u291.L4_help_names_a_literal`

--lanes help: name a literal five rather than read the constant

- File: `scripts/board.py`
- Source: `u291.json`, row `L4_help_names_a_literal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes_and_its_help_says_so`

Old text:

```
        help=f"how many cards the cloud builds at once (default {CLOUD_LANES})",
```

New text:

```
        help="how many cards the cloud builds at once (default 5)",
```

### `u291.L5_default_ignores_the_constant`

cmd_cloud: with no --lanes, count four lanes rather than CLOUD_LANES

- File: `scripts/board.py`
- Source: `u291.json`, row `L5_default_ignores_the_constant`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments2-0-said2-unsaid2]`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments3-0-said3-unsaid3]`

Old text:

```
    lanes = max(1, getattr(args, "lanes", None) or CLOUD_LANES)
```

New text:

```
    lanes = max(1, getattr(args, "lanes", None) or 4)
```

### `u313.B2_landed_twice`

land_residuals: number a file whose title the ledger already holds, so a file that came back through a conflict lands twice

- File: `scripts/board.py`
- Source: `u313.json`, row `B2_landed_twice`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_board_residual_search.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_a_landing_that_cannot_number_every_file_writes_nothing[files0-R-12 already]`

Old text:

```
        if meta["title"] in held
```

New text:

```
        if meta["title"] in held and False
```

### `u313.B3_stale_window_doubled`

cloud_state: read a hold as dead only after twice the stale window, so a dead session's card is not offered to resume

- File: `scripts/board.py`
- Source: `u313.json`, row `B3_stale_window_doubled`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 10 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-## Started@s+1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorm notes**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorm**s@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorms**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorms.**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Pre brainstorm.**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-Brainstorm notes.@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-Not **Withdrawn**, held@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-Question.@s+2]`
  - `tests/test_board_cloud.py::test_cloud_offers_answered_before_resumable_before_fresh`

Old text:

```
    if age is not None and age > STALE_HOURS:
```

New text:

```
    if age is not None and age > STALE_HOURS * 2:
```

### `u313.B4_withdrawn_held`

cloud_state: read a Withdrawn card as held, so a released card is never offered

- File: `scripts/board.py`
- Source: `u313.json`, row `B4_withdrawn_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Started@2; ## Withdrawn@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Started@s+4; Withdrawn.@s+2]`

Old text:

```
    if heading == HEAD_WITHDRAWN:
```

New text:

```
    if heading == HEAD_WITHDRAWN and False:
```

### `u313.B5_owed_unit_closes`

unresolved_closes: pass a unit a register still owes a module, so a closing trailer closes it early

- File: `scripts/board.py`
- Source: `u313.json`, row `B5_owed_unit_closes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 149 against a baseline of 149
- Kills: 41 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closing_trailer_is_refused_while_a_register_still_owes_that_unit`
  - `tests/test_pending_units.py::test_a_hash_leading_body_line_survives_the_range_check`
  - `tests/test_pending_units.py::test_a_pull_request_range_closing_a_unit_still_owed_is_refused`
  - `tests/test_pending_units.py::test_a_refusal_names_what_the_package_actually_contains`
  - `tests/test_pending_units.py::test_an_issue_number_is_resolved_to_its_unit_when_the_board_says_they_differ`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Close #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closed #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes #36, #33]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes #36.]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes GH-36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes: #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Fix #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Fixed #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Fixes #36]`
  - ... and 26 more, see the JSON sidecar

Old text:

```
        if not modules:
```

New text:

```
        if modules or not modules:
```

### `u313.B6_refusal_exit_code`

_refuse: print the refusal and return 0, so a refused residuals command reads as done

- File: `scripts/board.py`
- Source: `u313.json`, row `B6_refusal_exit_code`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_board_residual_search.py`
- Collected: 55 against a baseline of 55
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_missing_ledger_is_refused_never_read_as_no_match`
  - `tests/test_board_residual_search.py::test_the_command_prints_hits_and_refuses_an_empty_search`
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`

Old text:

```
    print(f"board: {message}", file=sys.stderr)
    return code
```

New text:

```
    print(f"board: {message}", file=sys.stderr)
    return 0
```

### `u314.L10_search_names_no_file`

cmd_residuals: print a search hit without the file it is in

- File: `scripts/board.py`
- Source: `u314.json`, row `L10_search_names_no_file`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 7 against a baseline of 7
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_search_reads_every_archive_and_says_where_each_hit_is`
  - `tests/test_board_residual_search.py::test_the_command_prints_hits_and_refuses_an_empty_search`

Old text:

```
            print(f"R-{number}. {title}  ({path.relative_to(LEDGER.parent.parent)})")
```

New text:

```
            print(f"R-{number}. {title}")
```

### `u314.L1_archives_unread`

ledger_files: read the working file alone, so search, the highest number and the title check never see an archive

- File: `scripts/board.py`
- Source: `u314.json`, row `L1_archives_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`, `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 156 against a baseline of 156
- Kills: 7 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_search_reads_every_archive_and_says_where_each_hit_is`
  - `tests/test_pending_units.py::test_the_residual_heading_reader_reads_the_document_as_it_is_written`
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_file_over_the_limit_and_archives_that_overlap`
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`
  - `tests/test_restart_and_residual_files.py::test_the_archive_moves_every_entry_byte_for_byte_and_a_rerun_changes_nothing`

Old text:

```
    return sorted((ledger.parent / "ledger").glob("*.md"), key=first) + [ledger]
```

New text:

```
    return [ledger]
```

### `u314.L2_landing_never_archives`

land_residuals: append without archiving, so the working file grows past the limit

- File: `scripts/board.py`
- Source: `u314.json`, row `L2_landing_never_archives`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_board_residual_search.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`

Old text:

```
    ledger.write_text(text)
    archive_ledger(ledger)
```

New text:

```
    ledger.write_text(text)
```

### `u314.L3_archive_header_undercounted`

archive_ledger: count a two line header where four are written, so an archive can pass the limit

- File: `scripts/board.py`
- Source: `u314.json`, row `L3_archive_header_undercounted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`
  - `tests/test_restart_and_residual_files.py::test_the_archive_moves_every_entry_byte_for_byte_and_a_rerun_changes_nothing`
  - `tests/test_restart_and_residual_files.py::test_the_working_file_archives_at_one_line_over_the_limit_and_not_at_it`

Old text:

```
        while last < count - 1 and 4 + len(body(first, last + 1)) <= LEDGER_LIMIT:
```

New text:

```
        while last < count - 1 and 2 + len(body(first, last + 1)) <= LEDGER_LIMIT:
```

### `u314.L5_duplicate_heading_passes`

ledger_problems: never report a heading held by two files

- File: `scripts/board.py`
- Source: `u314.json`, row `L5_duplicate_heading_passes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`

Old text:

```
            if number in where:
```

New text:

```
            if False:
```

### `u314.L6_misnamed_archive_passes`

ledger_problems: never compare an archive's name with the range it holds

- File: `scripts/board.py`
- Source: `u314.json`, row `L6_misnamed_archive_passes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`

Old text:

```
        if path != ledger and (not numbers or path.name != _archive_name(numbers[0], numbers[-1])):
```

New text:

```
        if path != ledger and not numbers:
```

### `u314.L7_removed_heading_reversed`

ledger_problems: look for headings added since the revision rather than removed, so a removed heading passes

- File: `scripts/board.py`
- Source: `u314.json`, row `L7_removed_heading_reversed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`

Old text:

```
    missing = [f"R-{n}" for n in sorted(set(before) - set(now))]
```

New text:

```
    missing = [f"R-{n}" for n in sorted(set(now) - set(before))]
```

### `u314.L8_unchanged_ignored`

ledger_problems: never report an entry that differs from the revision, so the move's byte comparison passes anything

- File: `scripts/board.py`
- Source: `u314.json`, row `L8_unchanged_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`

Old text:

```
    if unchanged and changed:
```

New text:

```
    if False:
```

### `u314.L9_archives_at_rev_unread`

_ledger_at: read only the working file at the revision, so a heading removed from an archive passes the check against it

- File: `scripts/board.py`
- Source: `u314.json`, row `L9_archives_at_rev_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`

Old text:

```
    for name in [*(n for n in listed.stdout.split() if n.endswith(".md")), ledger.name]:
```

New text:

```
    for name in [ledger.name]:
```

### `u59.B1_per_message_split`

Concatenate the range again, manufacturing a trailer across two commits

- File: `scripts/board.py`
- Source: `u59.json`, row `B1_per_message_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closing_reference_is_never_manufactured_across_two_commit_messages`

Old text:

```
            ["git", "log", "--format=%B%x00", f"{args.since}..HEAD"],
```

New text:

```
            ["git", "log", "--format=%B", f"{args.since}..HEAD"],
```

### `u59.B2_raw_true_on_range`

Strip comments on the CI path, which can only delete a real trailer

- File: `scripts/board.py`
- Source: `u59.json`, row `B2_raw_true_on_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_hash_leading_body_line_survives_the_range_check`

Old text:

```
                problems += unresolved_closes(message, raw=False)
```

New text:

```
                problems += unresolved_closes(message, raw=True)
```

### `u59.B3_unit_mapping_ignored`

Ignore the supplied issue-to-unit map, restoring the number conflation

- File: `scripts/board.py`
- Source: `u59.json`, row `B3_unit_mapping_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_an_issue_number_is_resolved_to_its_unit_when_the_board_says_they_differ`

Old text:

```
        uid = reference if units is None else units.get(reference)
```

New text:

```
        uid = reference
```

### `u59.B4_guess_caveat_dropped`

Stop saying the unit number was guessed, so the reader trusts it

- File: `scripts/board.py`
- Source: `u59.json`, row `B4_guess_caveat_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_network_free_path_says_that_it_guessed_the_unit_number`

Old text:

```
        if units is None and reference == uid:
```

New text:

```
        if False:
```

### `u59.B6_duplicate_unit_kept`

Let a duplicated unit number resolve to whichever issue was seen last

- File: `scripts/board.py`
- Source: `u59.json`, row `B6_duplicate_unit_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_register_owing_a_unit_with_no_issue_at_all_is_silence_not_a_crash`
  - `tests/test_pending_units.py::test_the_unit_to_issue_map_is_read_off_the_titles_and_drops_a_duplicate`

Old text:

```
    return {unit: number for unit, number in seen.items() if unit not in duplicated}
```

New text:

```
    return seen
```

### `u59.B8_missing_file_raises`

Let a missing message file raise instead of refusing with a sentence

- File: `scripts/board.py`
- Source: `u59.json`, row `B8_missing_file_raises`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_missing_message_file_refuses_with_a_sentence_not_a_traceback`

Old text:

```
        if not path.is_file():
```

New text:

```
        if False:
```

### `u81-round-2.B5_owed_argument_ignored`

Ignore a supplied register and always read the live one

- File: `scripts/board.py`
- Source: `u81-round-2.json`, row `B5_owed_argument_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
```

New text:

```
    owed = owed_by_unit()
    issues_by_unit = units_by_issue_number(graph)
```

### `u81-round-3.B5_audit_drops_the_detector`

Have the audit find no contradictions at all, keeping its drift report

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_audit_drops_the_detector`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`

Old text:

```
    clashes = contradictions(graph)
```

New text:

```
    clashes = []
```

### `u81-round-3.B5_audit_exit_code`

Report a contradiction as exit 1, the code that sends a session to sync

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_audit_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`

Old text:

```
    return 2 if clashes else 1
```

New text:

```
    return 1
```

### `u81-round-3.B5_owed_default_dropped`

Collapse the no-register default into a falsy test, so an empty register reads as none

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_owed_default_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
```

New text:

```
    owed = owed or {}
    issues_by_unit = units_by_issue_number(graph)
```

### `u81.B5_composite`

What B5 does hold: report a contradiction over an OPEN issue as well

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_composite`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_mutation_driver.py`, `tests/test_pool_sizing.py`, `tests/test_restore.py`
- Collected: 2374 against a baseline of 2374
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`

Old text:

```
        if node and node["unit"] and node["closed"]:
```

New text:

```
        if node and node["unit"]:
```

### `u81.B5_contradictions_by_number`

Index the graph by unit number again in contradictions()

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_contradictions_by_number`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 3 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
        number = issues_by_unit.get(uid)
        node = graph.get(number) if number is not None else None
```

New text:

```
        node = graph.get(uid)
```

### `u81.B5_residual_repoint_dropped`

Return only the register contradictions, dropping the repointed residuals

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_residual_repoint_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_repointed_residual_issue_is_reported_through_the_same_call`

Old text:

```
    return found + repointed_residuals(graph)
```

New text:

```
    return found
```

