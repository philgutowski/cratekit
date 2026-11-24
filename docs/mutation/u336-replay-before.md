# Mutation table: u336-replay-before

Measured by `scripts/mutate.py` on 2026-11-24 15:51 UTC, branch `cloud/985-replay-before` at `9a5c2d1f`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23237 collected. pytest invocations for this batch: 44.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 11, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23237 against 23237. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B10_a_changed_mode_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u297.B11_a_changed_schema_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 5 | killed |
| `u297.B1_a_root_outside_the_temporary_directory` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 3 | killed |
| `u297.B2_the_temporary_directory_itself` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u297.B3_somebodys_directory_emptied` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 3 | killed |
| `u297.B4_a_failed_run_closed_as_a_capture` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u297.B5_a_scenario_with_no_record_closed_over` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 4 | killed |
| `u297.B6_any_two_texts_the_same` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 21 | killed |
| `u297.B7_a_word_read_inside_a_longer_one` | `scripts/behaviour_compare.py` | maintainer | 1 file(s) | 137 | 3 | killed |
| `u297.B8_a_changed_exit_code_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 2 | killed |
| `u297.B9_a_file_in_one_capture_only_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 2 | killed |
| `u339-composites.C6_census_tombstone` | `src/cratekit/adopt/scan.py` | user | 7 file(s) | 1016 | 49 | killed |
| `u248.L10_built_before_the_builder` | `src/cratekit/cli/__init__.py` | maintainer | 1 file(s) | 161 | 1 | killed |
| `u248.L1_lazy_off` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1182 | 12 | killed |
| `u248.L2_chosen_never_built` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1182 | 315 | killed |
| `u248.L3_listing_asks_everyone` | `src/cratekit/cli/__init__.py` | maintainer | 1 file(s) | 161 | 4 | killed |
| `u248.L4_listing_drops_the_stub_line` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1236 | 4 | killed |
| `u248.L5_listing_asked_twice` | `src/cratekit/cli/__init__.py` | maintainer | 1 file(s) | 161 | 2 | killed |
| `u248.L6_built_twice` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 161 | 1 | killed |
| `u248.L7_defect_as_stub` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1182 | 2 | killed |
| `u248.L8_listing_raises_a_defect` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 161 | 1 | killed |
| `u331.S13_doctor_state_loads_the_taxonomy_loader_at_top` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 161 | 1 | killed |
| `u328.S1_a_part_left_out_of_the_table` | `src/cratekit/cli/registry.py` | user | 92 file(s) | 8498 | collection error | collect-error |
| `u43-author-light.R1_marker_restored` | `src/cratekit/cli/registry_modules.py` | maintainer | 2 file(s) | 1025 | collection error | collect-error |
| `u42-author.R1_planned_marker_returns` | `src/cratekit/cli/registry_pipeline.py` | user | 1 file(s) | 1018 | collection error | collect-error |
| `r395.M11_render_literal` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1034 | 2 | killed |
| `r679-a.E1_cli_offers_every_verdict` | `src/cratekit/cli/review.py` | user | 3 file(s) | 834 | 1 | killed |
| `r679-a.A7_person_verdicts_are_all_verdicts` | `src/cratekit/core/review.py` | user | 3 file(s) | 834 | 2 | killed |
| `u331.S14_upgrade_loads_the_taxonomy_loader_at_top` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 161 | 1 | killed |
| `u184.A2_any_actor_accepted` | `src/cratekit/session/cli.py` | user | 3 file(s) | 86 | 3 | killed |
| `u297.S1_a_root_outside_the_scenarios_own_directory` | `tests/behaviour/conftest.py` | user | 1 file(s) | 137 | 1 | killed |

## Row definitions

### `u297.B10_a_changed_mode_unseen`

compare_files: stop comparing permission bits, so a private file written world readable compares clean

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B10_a_changed_mode_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_private_file_written_world_readable_is_reported`

Old text:

```
        if one.get("mode") != other.get("mode"):
```

New text:

```
        if False:
```

### `u297.B11_a_changed_schema_unseen`

compare_databases: compare no declarations, so a table that lost its key, a constraint or an index compares clean

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B11_a_changed_schema_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 5 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base0-changed0-said0]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base1-changed1-said1]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base2-changed2-said2]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base3-changed3-said3]`
  - `tests/test_behaviour_compare.py::test_a_table_in_one_dump_only_is_reported`

Old text:

```
            one.get("schema", []), other.get("schema", []), words, limit,
```

New text:

```
            [], [], words, limit,
```

### `u297.B1_a_root_outside_the_temporary_directory`

refuse_outside_temporary: accept any root, so a capture can be pointed at a directory somebody keeps

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B1_a_root_outside_the_temporary_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_link_inside_the_temporary_directory_that_leads_out_of_it_is_refused`
  - `tests/test_behaviour_compare.py::test_a_root_outside_the_temporary_directory_is_refused_before_anything_runs`
  - `tests/test_behaviour_compare.py::test_the_temporary_directory_itself_is_no_root`

Old text:

```
    if not is_inside(path, temporary_directory()):
```

New text:

```
    if False:
```

### `u297.B2_the_temporary_directory_itself`

is_inside: read a directory as inside itself, so the whole temporary directory can be a capture's root and be emptied

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B2_the_temporary_directory_itself`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_the_temporary_directory_itself_is_no_root`

Old text:

```
    return relative != Path(".")
```

New text:

```
    return True
```

### `u297.B3_somebodys_directory_emptied`

take_root: take a root, or the source directory beside it, that holds files no capture left

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B3_somebodys_directory_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_file_that_is_only_named_like_a_holder_vouches_for_nothing`
  - `tests/test_behaviour_compare.py::test_a_root_that_holds_somebodys_files_is_refused_and_left_alone`
  - `tests/test_behaviour_compare.py::test_the_directory_beside_the_root_is_not_emptied_either`

Old text:

```
        if not left_by_a_capture(folder, holder):
```

New text:

```
        if False:
```

### `u297.B4_a_failed_run_closed_as_a_capture`

run_capture: write the manifest though the scenario run failed, so a capture missing scenarios reads as finished

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B4_a_failed_run_closed_as_a_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_run_that_failed_with_every_record_written_is_not_a_capture`

Old text:

```
    if done.returncode != 0 or not recorded or missing:
```

New text:

```
    if not recorded or missing:
```

### `u297.B5_a_scenario_with_no_record_closed_over`

run_capture: close the capture though a scenario the run collected, or a whole scenario file, left no record

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B5_a_scenario_with_no_record_closed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_run_that_cannot_show_every_scenario_recorded_keeps_the_capture_open[a-file-collected-nothing]`
  - `tests/test_behaviour_compare.py::test_a_run_that_cannot_show_every_scenario_recorded_keeps_the_capture_open[a-scenario-left-no-record]`
  - `tests/test_behaviour_compare.py::test_a_run_that_cannot_show_every_scenario_recorded_keeps_the_capture_open[no-list]`
  - `tests/test_behaviour_compare.py::test_a_run_that_cannot_show_every_scenario_recorded_keeps_the_capture_open[not-a-list]`

Old text:

```
    if done.returncode != 0 or not recorded or missing:
```

New text:

```
    if done.returncode != 0 or not recorded:
```

### `u297.B6_any_two_texts_the_same`

same_but_for: read any two texts as the same once a capture has a word of its own, so no difference in output, a file or a row is seen

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B6_any_two_texts_the_same`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 21 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_changed_cell_is_a_row_gone_and_a_row_come`
  - `tests/test_behaviour_compare.py::test_a_changed_line_of_standard_error_is_reported`
  - `tests/test_behaviour_compare.py::test_a_changed_text_file_shows_the_line_that_changed`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base0-changed0-said0]`
  - `tests/test_behaviour_compare.py::test_a_file_that_only_ends_like_a_sidecar_is_compared_as_a_file`
  - `tests/test_behaviour_compare.py::test_a_long_difference_is_cut_unless_asked_for_whole`
  - `tests/test_behaviour_compare.py::test_a_missing_final_newline_is_a_difference_and_says_how_the_texts_end`
  - `tests/test_behaviour_compare.py::test_a_word_that_stands_for_two_things_keeps_both_counterparts`
  - `tests/test_behaviour_compare.py::test_another_files_inode_in_that_row_is_a_difference`
  - `tests/test_behaviour_compare.py::test_one_changed_character_of_help_is_reported`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[8430 bytes, pid 3409-8431 bytes, pid 3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[lock_3409-lock_3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 13409-pid 13467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 34091-pid 34671-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 3409\n-pid 3467-False]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return re.fullmatch("".join(pattern), second, flags=re.DOTALL) is not None
```

New text:

```
    return True
```

### `u297.B7_a_word_read_inside_a_longer_one`

same_but_for: drop the leading end of the whole word rule, so a process id is read inside a longer number

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B7_a_word_read_inside_a_longer_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[lock_3409-lock_3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 13409-pid 13467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid x3409-pid x3467-False]`

Old text:

```
        r"(?<![0-9A-Za-z_])(?:" + "|".join(re.escape(one) for one in longest_first) + r")(?![0-9A-Za-z_])"
```

New text:

```
        r"(?:" + "|".join(re.escape(one) for one in longest_first) + r")(?![0-9A-Za-z_])"
```

### `u297.B8_a_changed_exit_code_unseen`

compare_commands: stop comparing exit codes

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B8_a_changed_exit_code_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_one_changed_exit_code_is_reported`
  - `tests/test_behaviour_compare.py::test_one_command_more_is_reported_once_and_the_rest_are_still_compared`

Old text:

```
            if one["exit"] != other["exit"]:
```

New text:

```
            if False:
```

### `u297.B9_a_file_in_one_capture_only_unseen`

compare_files: walk only the paths both captures hold, so an extra file and a missing one are never reported

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B9_a_file_in_one_capture_only_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_an_empty_directory_a_verb_made_is_an_entry_of_its_own`
  - `tests/test_behaviour_compare.py::test_one_extra_file_is_reported_and_so_is_one_that_is_gone`

Old text:

```
    for relative in sorted(set(before) | set(after)):
```

New text:

```
    for relative in sorted(set(before) & set(after)):
```

### `u339-composites.C6_census_tombstone`

scan_rows: a tombstoned row is read as live by the census, the layer M6_tombstone_row's guard sits on (its composite)

- File: `src/cratekit/adopt/scan.py`
- Source: `u339-composites.json`, row `C6_census_tombstone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_behaviour_compare.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`
- Collected: 1016 against a baseline of 1016
- Kills: 49 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adoption.py::test_a_soft_deleted_row_is_not_proposed_for_adoption`
  - `tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal`
  - `tests/test_tag_backlog.py::test_a_person_reads_the_backlog`
  - `tests/test_tag_backlog.py::test_a_row_lagging_its_file_is_served_exactly_when_tag_rows_would_write_it`
  - `tests/test_tag_backlog.py::test_a_row_with_no_genre_and_agreeing_neighbours_is_proposed_from_the_neighbours`
  - `tests/test_tag_backlog.py::test_a_row_with_nothing_beside_it_is_left_with_no_votes[a-catch-all]`
  - `tests/test_tag_backlog.py::test_a_row_with_nothing_beside_it_is_left_with_no_votes[nothing-beside-it]`
  - `tests/test_tag_backlog.py::test_a_word_neither_answer_takes_leaves_its_rows_with_the_refusal`
  - `tests/test_tag_backlog.py::test_a_word_with_one_answer_moves_only_the_rows_it_reaches`
  - `tests/test_tag_backlog.py::test_every_needs_genre_row_lands_in_exactly_one_cause_and_a_routed_row_in_none`
  - `tests/test_tag_backlog.py::test_off_taxonomy_words_are_grouped_across_spellings_and_ranked_by_rows`
  - `tests/test_tag_backlog.py::test_only_a_row_with_no_genre_is_asked_of_the_catalogue`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`
  - ... and 34 more, see the JSON sidecar

Old text:

```
        if row.deleted:
            continue
```

New text:

```
(empty)
```

### `u248.L10_built_before_the_builder`

build: count the verb built before its builder returns, so a builder that failed part way hands on a half built verb

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L10_built_before_the_builder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
            ) from exc
        self.built = True
```

New text:

```
            ) from exc
        self.built = self.built
```

### `u248.L1_lazy_off`

build_parser: build every verb eagerly whatever eager says, so every command imports every verb module again

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L1_lazy_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`
- Collected: 1182 against a baseline of 1182
- Kills: 12 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_lazy.py::test_a_broken_module_fails_its_own_verb_and_leaves_every_other_one_working`
  - `tests/test_cli_lazy.py::test_a_defective_builder_is_a_defect_and_never_a_usage_error`
  - `tests/test_cli_lazy.py::test_a_group_help_loads_no_verb_module_when_none_of_its_verbs_declares_an_extra`
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_a_module_that_raises_anything_at_import_is_listed_plainly_and_raises_for_its_verb`
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`
  - `tests/test_cli_lazy.py::test_an_argument_error_raised_by_the_import_is_a_defect_too`
  - `tests/test_cli_lazy.py::test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[bare]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[help]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[version]`

Old text:

```
        if not eager:
            sub = target.add_parser(path[-1], help=entry.summary)
```

New text:

```
        if False:
            sub = target.add_parser(path[-1], help=entry.summary)
```

### `u248.L2_chosen_never_built`

_LazyChoices.__call__: never build the chosen verb, so it parses as an empty subparser with no handler

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L2_chosen_never_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`
- Collected: 1182 against a baseline of 1182
- Kills: 315 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_contract.py::test_a_gate_is_answerable_from_a_different_process_in_a_later_session`
  - `tests/test_cli_contract.py::test_a_profile_that_switches_a_module_off_removes_its_verbs`
  - `tests/test_cli_contract.py::test_a_run_carrying_a_pending_action_reports_it_as_pending`
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_a_run_that_reached_a_gate_reports_it`
  - `tests/test_cli_contract.py::test_a_scripted_run_with_no_terminal_reaches_a_gate_and_exits_with_its_code`
  - `tests/test_cli_contract.py::test_a_verb_blocked_by_an_unverified_pending_action_refuses_before_doing_anything`
  - `tests/test_cli_contract.py::test_a_verb_that_raises_or_exits_becomes_an_internal_cause[exits-the-process-directly]`
  - `tests/test_cli_contract.py::test_a_verb_that_raises_or_exits_becomes_an_internal_cause[something-unexpected]`
  - `tests/test_cli_contract.py::test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable`
  - `tests/test_cli_contract.py::test_an_unconfigured_machine_refuses_with_a_precondition_and_a_remedy`
  - `tests/test_cli_contract.py::test_conformance_1_structured_output_is_actually_emitted[acquire.audit]`
  - `tests/test_cli_contract.py::test_conformance_1_structured_output_is_actually_emitted[acquire.bandcamp-fetch]`
  - ... and 300 more, see the JSON sidecar

Old text:

```
        if waiting is not None:
            waiting.build()
```

New text:

```
        if waiting is not None:
            pass
```

### `u248.L3_listing_asks_everyone`

ask_for_listing: ask every verb, not only those declaring extras, so a group help imports all its verbs

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L3_listing_asks_everyone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_group_help_loads_no_verb_module_when_none_of_its_verbs_declares_an_extra`
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[bare]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[help]`

Old text:

```
        if self.built or self.asked or not self.entry.extras_modules:
```

New text:

```
        if self.built or self.asked:
```

### `u248.L4_listing_drops_the_stub_line`

ask_for_listing: a missing extra no longer makes the stub, so the listing omits (requires the extra)

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L4_listing_drops_the_stub_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`, `tests/test_analysis.py`, `tests/test_vocals_cli.py`
- Collected: 1236 against a baseline of 1236
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_missing_analysis_extra_names_the_install_command`
  - `tests/test_cli_contract.py::test_a_module_with_missing_extras_becomes_a_stub_that_names_the_install_command`
  - `tests/test_cli_lazy.py::test_a_blocked_extra_still_lists_the_stub_line_and_refuses_with_the_install_command`
  - `tests/test_vocals_cli.py::test_a_missing_vocals_extra_names_the_install_command`

Old text:

```
            if _is_missing_extra(exc, self.entry):
                self._stub(exc)
```

New text:

```
            if _is_missing_extra(exc, self.entry):
                pass
```

### `u248.L5_listing_asked_twice`

ask_for_listing: forget it was asked, so one help screen imports the module twice

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L5_listing_asked_twice`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
        self.asked = True
```

New text:

```
        self.asked = False
```

### `u248.L6_built_twice`

build: drop the built check, so a parser asked twice runs the builder twice and argparse refuses a duplicate option

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L6_built_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
        if self.built:
            return
        try:
            try:
                module = self.importer(self.entry.module)
```

New text:

```
        try:
            try:
                module = self.importer(self.entry.module)
```

### `u248.L7_defect_as_stub`

build: treat every import error as a missing extra, so a defect of our own reads as install the extra

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L7_defect_as_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`
- Collected: 1182 against a baseline of 1182
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_lazy.py::test_a_broken_module_fails_its_own_verb_and_leaves_every_other_one_working`

Old text:

```
                if not _is_missing_extra(exc, self.entry):
                    raise
                self._stub(exc)
                return
```

New text:

```
                self._stub(exc)
                return
```

### `u248.L8_listing_raises_a_defect`

ask_for_listing: let a non extra failure escape, so a broken module takes its whole group's help down

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L8_listing_raises_a_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_module_that_raises_anything_at_import_is_listed_plainly_and_raises_for_its_verb`

Old text:

```
        except Exception:  # noqa: BLE001 - see the docstring, the verb itself raises
            pass
```

New text:

```
        except Exception:  # noqa: BLE001 - see the docstring, the verb itself raises
            raise
```

### `u331.S13_doctor_state_loads_the_taxonomy_loader_at_top`

cli/doctor_state: import the active taxonomy loader at the top again, so crate doctor --help loads the foreign tree with it

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u331.json`, row `S13_doctor_state_loads_the_taxonomy_loader_at_top`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports`

Old text:

```
from cratekit.core import (
    config,
    provider_gate,
```

New text:

```
from cratekit.core import (
    active_taxonomy,  # noqa: F401
    config,
    provider_gate,
```

### `u328.S1_a_part_left_out_of_the_table`

ENTRIES: leave the modules part out of the assembly, so adoption, deletion, export and the utilities are not registered

- File: `src/cratekit/cli/registry.py`
- Source: `u328.json`, row `S1_a_part_left_out_of_the_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`, `tests/test_crate_sync_skill.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_docs_current.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_gate_not_reached.py`, `tests/test_gate_siblings.py`, `tests/test_gate_stale_screen.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_import_rules.py`, `tests/test_install_command.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_heard.py`, `tests/test_label_judge.py`, `tests/test_label_playlists.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_pending_units.py`, `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_report_genres.py`, `tests/test_reports_cli.py`, `tests/test_restamp_scored_by.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_run_retire.py`, `tests/test_schedule.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_setup_discogs.py`, `tests/test_sync_all.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_sync_mark.py`, `tests/test_sync_night.py`, `tests/test_sync_removed.py`, `tests/test_sync_removed_gone.py`, `tests/test_sync_unmark.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_tag_guess.py`, `tests/test_tag_remap.py`, `tests/test_tag_rows.py`, `tests/test_tag_second.py`, `tests/test_tag_set.py`, `tests/test_tag_suggest.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_u242_taken.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 8498 against a baseline of 8614
- Kills: 499 (collect-error)
- Note: collection changed: 8498 collected against a baseline of 8614. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/modules/test_tools.py::test_every_declared_verb_is_in_the_static_registry`
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_is_found_by_digest_source_not_by_position`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_workflow_name_and_the_registry_verb_name_cannot_drift`
  - `tests/test_adopt_move.py::test_a_cancelled_move_exits_with_its_own_cause_and_not_ok`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_failure_in_the_additions_writes_nothing_at_all`
  - `tests/test_adopt_move.py::test_a_job_another_verb_queued_is_never_driven_through_this_gate`
  - `tests/test_adopt_move.py::test_a_job_carrying_no_plan_is_refused_rather_than_driven`
  - `tests/test_adopt_move.py::test_a_parked_move_leaves_blocked_and_non_zero`
  - `tests/test_adopt_move.py::test_a_reading_that_changed_after_the_approval_is_a_stale_decision`
  - ... and 484 more, see the JSON sidecar

Old text:

```
    *MODULE_VERBS,

```

New text:

```
(empty)
```

### `u43-author-light.R1_marker_restored`

The planned_in marker is put back on the setbuild entry, which withdraws the verb from every conformance property that only drives landed entries

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u43-author-light.json`, row `R1_marker_restored`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 1025 against a baseline of 1029
- Kills: 3 (collect-error)
- Note: collection changed: 1025 collected against a baseline of 1029. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`

Old text:

```
        emits=frozenset({"plan"}), output_schema="plan/1",
        # Landed (U43).
```

New text:

```
        emits=frozenset({"plan"}), output_schema="plan/1",
        planned_in="U35",
        # Landed (U43).
```

### `u42-author.R1_planned_marker_returns`

Restore planned_in on acquire.download, which is the state that hid rows 6 and 7

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u42-author.json`, row `R1_planned_marker_returns`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1018 against a baseline of 1021
- Kills: 1 (collect-error)
- Note: collection changed: 1018 collected against a baseline of 1021. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`

Old text:

```
        destructive=True, doctor_checks=("credential.provider", "binary.ffmpeg"),
        # Landed (U42).
```

New text:

```
        destructive=True, doctor_checks=("credential.provider", "binary.ffmpeg"),
        planned_in="U15",
        # Landed (U42).
```

### `r395.M11_render_literal`

Put the old bare pip literal back in the parser stub

- File: `src/cratekit/cli/render.py`
- Source: `r395.json`, row `M11_render_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_install_command.py`
- Collected: 1034 against a baseline of 1034
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_module_with_missing_extras_becomes_a_stub_that_names_the_install_command`
  - `tests/test_install_command.py::test_the_parser_stub_and_the_workers_read_one_source`

Old text:

```
    return extras.install_command(entry.extras)
```

New text:

```
    return f"pip install '{registry.DISTRIBUTION}[{entry.extras}]'"
```

### `r679-a.E1_cli_offers_every_verdict`

review resolve: offer the whole enum as --verdict choices

- File: `src/cratekit/cli/review.py`
- Source: `r679-a.json`, row `E1_cli_offers_every_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 834 against a baseline of 834
- Kills: 1 (killed)
- Killed:
  - `tests/test_review_queue.py::test_the_command_line_offers_a_person_only_the_persons_verdicts`

Old text:

```
        choices=tuple(str(member) for member in review.PERSON_VERDICTS),
```

New text:

```
        choices=tuple(str(member) for member in review.Verdict),
```

### `r679-a.A7_person_verdicts_are_all_verdicts`

PERSON_VERDICTS: include the machine's verdict, so the command line offers it

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A7_person_verdicts_are_all_verdicts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 834 against a baseline of 834
- Kills: 2 (killed)
- Killed:
  - `tests/test_review_queue.py::test_resolve_and_the_batch_refuse_the_machines_verdict`
  - `tests/test_review_queue.py::test_the_command_line_offers_a_person_only_the_persons_verdicts`

Old text:

```
    member for member in Verdict if member is not Verdict.SUPERSEDED
```

New text:

```
    member for member in Verdict
```

### `u331.S14_upgrade_loads_the_taxonomy_loader_at_top`

core/taxonomy_upgrade: import the active taxonomy loader at the top again, so crate doctor --help loads the foreign tree with it

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u331.json`, row `S14_upgrade_loads_the_taxonomy_loader_at_top`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports`

Old text:

```
from cratekit.core import config, taxonomy

```

New text:

```
from cratekit.core import active_taxonomy, config, taxonomy  # noqa: F401

```

### `u184.A2_any_actor_accepted`

build_ack: drop the one value restriction, so --as names any actor and is parsed

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A2_any_actor_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[Session]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[a-person]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[cli]`

Old text:

```
        choices=(session.SESSION_ACTOR,),
```

New text:

```
        choices=None,
```

### `u297.S1_a_root_outside_the_scenarios_own_directory`

refuse_a_root_outside: accept a configuration or state directory anywhere in the temporary directory, another test's included

- File: `tests/behaviour/conftest.py`
- Source: `u297.json`, row `S1_a_root_outside_the_scenarios_own_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_root_outside_the_scenarios_own_directory_is_refused[in-another-tests-directory]`

Old text:

```
        if not compare.is_inside(path, scenario_root):
```

New text:

```
        if False:
```

