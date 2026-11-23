# Mutation table: u325-after-hand

Measured by `scripts/mutate.py` on 2026-11-23 03:24 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 102.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 40, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1709.M25_fallback_identity_fold` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `u223.M1_composite` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 6 | killed |
| `u45-round-1.H2_queueing_plans_first` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r1499.L02_go_kept_after_arrival` | `src/cratekit/cli/label_sync.py` | user | 6 file(s) | 324 | 3 | killed |
| `r338-c.C6_only_the_first_root_is_watched` | `src/cratekit/core/analysis_store.py` | user | 1 file(s) | 32 | 1 | killed |
| `u79-b.B7_identity_without_version` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 56 | 2 | killed |
| `u221.R24_abort_releases` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u287.M10_gone_on_one_read` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 5 | killed |
| `u287.M16_gone_holds_what_was_recorded` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `r816-b.B5_commit_recorded` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `u119.G2_source_folder_counts` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.G3_two_sources_first_wins` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u206.M25_lock_skipped` | `src/cratekit/core/config.py` | maintainer | 9 file(s) | 1135 | 1 | killed |
| `u293.S2_second_holder_refused` | `src/cratekit/core/staging_lock.py` | user | 4 file(s) | 237 | 5 | killed |
| `r235-a.M11_session_lock_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `u79-c.C2_owned_row_searched` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 2 | killed |
| `u107-a.S01_record_not_json` | `src/cratekit/core/config.py` | user | 1 file(s) | 94 | 2 | killed |
| `r356-b.B2_template_declares_no_lossy_marker` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r356-b.B3_empty_marker_no_longer_guarded` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `u220.A3_keep_head` | `src/cratekit/sync/pair_stopped.py` | user | 6 file(s) | 287 | 26 | killed |
| `u220.A4_first_first` | `src/cratekit/sync/pair_stopped.py` | user | 6 file(s) | 287 | 14 | killed |
| `r1394.S3_bool_count_read` | `src/cratekit/cli/output.py` | maintainer | 2 file(s) | 177 | 1 | killed |
| `r1394.S4_negative_count_read` | `src/cratekit/cli/output.py` | maintainer | 2 file(s) | 177 | 1 | killed |
| `r1394.S5_sent_read_as_landed` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 6 | killed |
| `u322.M22_backlog_partly_clause_gone` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `r668-a.M5_missing_list_guard_after_load` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-a.M7_list_compared_as_strings` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r926.G11_mkdir_before_check` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 299 | 9 | killed |
| `r926.G3_document_check_dropped` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 299 | 12 | killed |
| `r926.G4_document_gets_temporary` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 299 | 12 | killed |
| `r926.G5_atomic_write_unchecked` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 299 | 8 | killed |
| `r926.G6_lock_unchecked` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 299 | 8 | killed |
| `r926.G8_target_unresolved` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 299 | 8 | killed |
| `u217.K10_naive_instant` | `src/cratekit/label/kept_reads.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `r375-b.M1_capture_never_attached` | `src/cratekit/write/trees.py` | user | 1 file(s) | 26 | 3 | killed |
| `u219.G1_resort_abort` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `r375-b.T5_witnessed_commit_not_recorded` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 1 | killed |
| `r375-c.T6_every_raise_read_as_a_commit_again` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 1 | killed |
| `u254.M20_mark_unlocked` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u192.A1_run_queue_only_ignored` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 11 | killed |
| `u192.A2_restamp_queue_only_ignored` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u27-reports-round-1.S6_lossy_marker` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 3 | killed |
| `u194.W20_retag_reread` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u194.W21_retag_read_back` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u57-recognition-and-items.C12_stray_file_sorted` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 108 | 1 | killed |
| `r504-b.B5_noop_silent` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 682 | 2 | killed |
| `r515-operator.S10_intake_all_withheld_quiet` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u62.C1_bound_constant_true` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 544 | 1 | killed |
| `r815-c.J8_a_refusal_parks_and_fails_no_item` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 5 | killed |
| `u46-round-2.M2_resume_does_not_drive` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 75 | 15 | killed |
| `u43-author-round-2.H4_template_loses_the_marker` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.V2_marker_position_moved` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R37_artifact_named_by_item_id` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R38_staging_not_cleared` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `r799-b.W1_a_file_is_read_again_before_it_is_written` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-b.W3_a_write_is_read_back` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r290-author.S11_tagging_shell_call_removed` | `src/cratekit/core/jobs.py` | user | 5 file(s) | 390 | 49 | killed |
| `u56-catalogue-searcher-and-tag-workers.R33_no_op_job_id_is_null` | `src/cratekit/cli/output.py` | user | 1 file(s) | 102 | 9 | killed |
| `u56-catalogue-searcher-and-tag-workers.R34_empty_job_is_driven` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 47 | killed |
| `u225.M6_front_keeps_nothing` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |

## Mapped

Recorded rows this batch has no row for, each with the row that covers it. `scripts/killset.py check` holds each mapping to a row that is killed.

- `r1709.json` row `M24_intake_identity_fold` is covered by `r1709.M25_fallback_identity_fold`: U298 folded intake/candidates.identity and acquire/fallback.identity, two copies of one dict, into match.Wanted.folded_row; the title line both rows mutated is now that one line, anchored under M25 with the same substitution and the same test list
- `r290-author.json` row `S03_acquire_fallback_call_removed` is covered by `r290-author.S11_tagging_shell_call_removed`: U298 removed the raise_for_state call from acquire/fallback_cli.py's fetch resume, which now leaves through core.jobs.resumed; that function's single call is the same mapping, anchored under S11 with this row's test files added to its list
- `r290-author.json` row `S12_adopt_shell_call_removed` is covered by `r290-author.S11_tagging_shell_call_removed`: U298 removed the raise_for_state call from adopt/shell.py's advance, which now leaves through core.jobs.resumed; that function's single call is the same mapping, anchored under S11 with this row's test files added to its list
- `r290-author.json` row `S01_master_call_removed` is covered by `r290-author.S11_tagging_shell_call_removed`: U298 removed the raise_for_state call from master/cli.py's resume, which now leaves through core.jobs.resumed; that function's single call is the same mapping, anchored under S11 with this row's test files added to its list
- `u220.json` row `A2_keep_nothing` is covered by `u225.M6_front_keeps_nothing`: U298 replaced tidal_account._to_the_front's body with sync.pair_stopped.front_moves, its copy until then, which the adapter now returns; u225.M6 already makes the same keep += 0 substitution on that one line

## Row definitions

### `r1709.M25_fallback_identity_fold`

the upload question keys the folded title

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M25_fallback_identity_fold`
- Moved: U298 replaced the identical identity dict in acquire/fallback.py and intake/candidates.py with match.Wanted.folded_row, which both identity functions now return; the title is keyed by title_identity there, the same line, so folding it breaks both questions as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_upload_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_a_search_question_about_one_emoji_title_is_not_another_ones`

Old text:

```
            "title": title_identity(self.title),

```

New text:

```
            "title": fold(self.title),

```

### `u223.M1_composite`

What M1 holds with the staged report fallback gone too: the shipped bug, through the verb and the printed resume

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M1_composite`
- Moved: Same file and the same two edits, the intent no longer kept by staged_path and staged_report reading nothing. U298 moved write onto core.jobs.Artifacts and renamed config._mkdir_private, both inside the span the old text covered, so the span is re-read at db120fdb
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`

Old text:

```
                entry.name == RENAME_INTENT_FILENAME
                and entry.is_file()
                and not entry.is_symlink()
            ):
                continue
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    elif directory.is_symlink() or directory.exists():
        # WHAT THE FIRST VERSION DID WITH ANYTHING ELSE AT THIS PATH, kept:
        # ``rmtree`` refuses a link and a plain file, loudly, rather than this
        # call deciding to remove or follow one.
        shutil.rmtree(directory)
    config.mkdir_private(directory)
    return directory / _report_name(ordinal)


def intent_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where one item's rename intent lives: in its staging directory.

    THE INTENT IS WRITTEN BEFORE THE RENAME AND OUTLIVES A KILL. The item is
    the pre rename name and the rename lands inside the handler, before the
    engine flips the row to done, so a kill in that window leaves a finished
    file under its head and a pending row under its old name. The intent is
    what lets the resume find the file the item BECAME rath
... truncated ...
```

New text:

```
                entry.name == "never-kept.json"
                and entry.is_file()
                and not entry.is_symlink()
            ):
                continue
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    elif directory.is_symlink() or directory.exists():
        # WHAT THE FIRST VERSION DID WITH ANYTHING ELSE AT THIS PATH, kept:
        # ``rmtree`` refuses a link and a plain file, loudly, rather than this
        # call deciding to remove or follow one.
        shutil.rmtree(directory)
    config.mkdir_private(directory)
    return directory / _report_name(ordinal)


def intent_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where one item's rename intent lives: in its staging directory.

    THE INTENT IS WRITTEN BEFORE THE RENAME AND OUTLIVES A KILL. The item is
    the pre rename name and the rename lands inside the handler, before the
    engine flips the row to done, so a kill in that window leaves a finished
    file under its head and a pending row under its old name. The intent is
    what lets the resume find the file the item BECAME rather th
... truncated ...
```

### `u45-round-1.H2_queueing_plans_first`

Plan inside the handler, so queueing refuses on a machine with no rclone where the work would have run fine

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `H2_queueing_plans_first`
- Moved: Same handler, backup_library; U298 replaced its private _load with cli.output.load_config, so the line the plan is inserted after is reworded and the insertion point is the same
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_queueing_needs_no_rclone_no_remote_and_no_volume`

Old text:

```
    cfg = load_config(("backup.cli",))
    with jobs.open_store() as store:
        if ctx.args.job:
```

New text:

```
    cfg = load_config(("backup.cli",))
    backup.plan_backup(cfg)
    with jobs.open_store() as store:
        if ctx.args.job:
```

### `r1499.L02_go_kept_after_arrival`

_kept: the go keeps its record although something arrived

- File: `src/cratekit/cli/label_sync.py`
- Source: `r1499.json`, row `L02_go_kept_after_arrival`
- Moved: Same _kept guard; U298 replaced this copy of _changed_said with tail.changed_said, which only rewords the line under the condition the row mutates
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_a_gos_landing_is_planned_refuses_it`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_gos_tail_that_fails_while_a_download_arrives_says_its_record_was_not_kept`

Old text:

```
    if changed is not None:
        return [_unkept(folder, job, tail.changed_said(changed))]
```

New text:

```
    if False:
        return [_unkept(folder, job, tail.changed_said(changed))]
```

### `r338-c.C6_only_the_first_root_is_watched`

is_watched: ask the library root alone, so a share aimed at the live share's own parent is pulled under the watch that refuses it

- File: `src/cratekit/core/analysis_store.py`
- Source: `r338-c.json`, row `C6_only_the_first_root_is_watched`
- Moved: Same is_watched line; U298 replaced the module's own _is_within with config.is_inside, the same textual containment test, so asking only the first root is the same mutation
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_store.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_that_would_land_under_the_analysis_watch_is_withheld_and_not_asked_about`

Old text:

```
    return any(config.is_inside(Path(path), root) for root in watch_roots(cfg))
```

New text:

```
    return config.is_inside(Path(path), watch_roots(cfg)[0])
```

### `u79-b.B7_identity_without_version`

The question is keyed without the version, so two versions are one item

- File: `src/cratekit/acquire/match.py`
- Source: `u79-b.json`, row `B7_identity_without_version`
- Moved: U298 moved intake/candidates.identity's dict into match.Wanted.folded_row, which candidates.identity now returns; the version key is the same field, so blanking it makes two versions one question as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`

Old text:

```
            "version": self.version_key,

```

New text:

```
            "version": "",

```

### `u221.R24_abort_releases`

sync_release: read an abort as an approval, so the hold is emptied without the choice

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R24_abort_releases`
- Moved: Same gate check in sync_release; U298 replaced the local _gate lookup with cli.output.declared_gate, so only the argument is reworded
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`

Old text:

```
    if ctx.gate.require(declared_gate(ctx.entry, APPROVE_GATE), plan=data, context=facts(planned)) != "approve":
```

New text:

```
    if ctx.gate.require(declared_gate(ctx.entry, APPROVE_GATE), plan=data, context=facts(planned)) == "never":
```

### `u287.M10_gone_on_one_read`

read_one: read a playlist the account's list omits as gone without opening it by its id

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M10_gone_on_one_read`
- Moved: Same read_one; the merged U320 work made the name a multi line expression that also reads a remembered name, and the row still inserts the early GONE return right after it, before the playlist is opened by its id
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`

Old text:

```
    name = (
        shown.name
        if shown is not None
        else (names or {}).get(account) or (prior.name if prior is not None else "")
    )

```

New text:

```
    name = (
        shown.name
        if shown is not None
        else (names or {}).get(account) or (prior.name if prior is not None else "")
    )
    if shown is None:
        return Listing(account=account, name=name, state=GONE, why="")

```

### `u287.M16_gone_holds_what_was_recorded`

Listing.holds: a gone playlist holds nothing, so a track its pass recorded on it can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M16_gone_holds_what_was_recorded`
- Moved: Same Listing.holds guard; the merged U320 work named the holding states HOLDING and added WITHHELD to it, so the mutation takes GONE out of that set and leaves the rest, which is what removing GONE from (READ, GONE) did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`

Old text:

```
        if self.state not in HOLDING:
```

New text:

```
        if self.state not in HOLDING - {GONE}:
```

### `r816-b.B5_commit_recorded`

apply_rows: leave the landed commit off the session record

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B5_commit_recorded`
- Moved: Same call site in apply_rows; U298 replaced the module's _record_commit with write.row_defaults.record_commit, so the deleted line is reworded and still the record of the landed commit
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_apply_is_a_recorded_session_a_restore_can_undo`

Old text:

```
        # RECORDED THE INSTANT THE COMMIT RETURNS.
        row_defaults.record_commit(record, CHANGE_KEY, written, cfg)

```

New text:

```
        # RECORDED THE INSTANT THE COMMIT RETURNS.

```

### `u119.G2_source_folder_counts`

source_playlist: a source playlist holding no live track is mirrored, emptying every Favorites

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G2_source_folder_counts`
- Moved: Same source_playlist guard; U298 renamed _live_members to the public live_members
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_smart_playlist_or_an_emptied_playlist_of_the_source_name_is_not_the_source`

Old text:

```
        if not live_members(db, str(live[0].ID)):
```

New text:

```
        if False:
```

### `u119.G3_two_sources_first_wins`

source_playlist: two live sources, the first is taken

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G3_two_sources_first_wins`
- Moved: Same source_playlist guard; U298 renamed _live_members to the public live_members
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_two_source_playlists_are_refused_rather_than_one_chosen`

Old text:

```
    if len(live) == 1:
        if not live_members(db, str(live[0].ID)):
```

New text:

```
    if len(live) >= 1:
        if not live_members(db, str(live[0].ID)):
```

### `u206.M25_lock_skipped`

Cache._locked: yield as held without taking the lock

- File: `src/cratekit/core/config.py`
- Source: `u206.json`, row `M25_lock_skipped`
- Moved: U298 replaced isrc_cache.Cache._locked's body with config.lock_within, which _locked now returns; the same non blocking flock in the same poll loop, so dropping it yields held without the lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`

Old text:

```
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                had = True
```

New text:

```
            try:
                had = True
```

### `u293.S2_second_holder_refused`

held: a second holder goes on beside the first rather than refusing

- File: `src/cratekit/core/staging_lock.py`
- Source: `u293.json`, row `S2_second_holder_refused`
- Moved: Same refusal in held; U298 moved the non blocking flock into config.lock_now, which returns whether the lock was had, and the raise now sits under if not had, one level shallower, still the refusal of a second holder
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_staging_lock.py`, `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 237 against a baseline of 237
- Kills: 5 (killed)
- Killed:
  - `tests/test_staging_lock.py::test_a_holder_that_cannot_be_read_still_refuses`
  - `tests/test_staging_lock.py::test_a_second_holder_refuses_naming_the_first`
  - `tests/test_sync_night.py::test_a_label_go_refuses_while_another_pass_holds_the_lock`
  - `tests/test_sync_night.py::test_a_pass_by_hand_refuses_while_the_night_holds_the_lock`
  - `tests/test_sync_night.py::test_another_pass_holding_the_staging_lock_refuses_the_night_naming_it`

Old text:

```
            raise _held_error(what or verb, _read_holder(handle.read()), path) from None
```

New text:

```
            pass
```

### `r235-a.M11_session_lock_dropped`

a revert holds the registry lock and not the session lock

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M11_session_lock_dropped`
- Moved: Same with statement in revert_cutover; U298 renamed config._exclusive_lock to exclusive_lock
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_the_revert_holds_the_session_lock_while_it_asks_and_writes`

Old text:

```
    with session.session_lock(cfg), config.exclusive_lock(lock_path(cfg)):
```

New text:

```
    with config.exclusive_lock(lock_path(cfg)):
```

### `u79-c.C2_owned_row_searched`

A row the library holds is counted missing and searched for

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C2_owned_row_searched`
- Moved: Same loop in _missing_for_list; U298 replaced its three state branches with a lookup in match_cli.SETTLED_WORDS, whose MATCHED entry is owned, so excluding owned sends a matched row to the missing branch, which is what disabling the MATCHED branch did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_list_the_library_holds_entirely_is_a_no_op_that_spends_no_login`
  - `tests/test_intake_missing_search.py::test_an_owned_row_is_never_searched_for`

Old text:

```
        word = match_cli.SETTLED_WORDS.get(settled.state)
        if word is not None:
            counts[word] += 1
```

New text:

```
        word = match_cli.SETTLED_WORDS.get(settled.state)
        if word is not None and word != "owned":
            counts[word] += 1
```

### `u107-a.S01_record_not_json`

sync_cli.load_record: read a record that is not JSON as an empty one, so every question is asked again and every answer is lost

- File: `src/cratekit/core/config.py`
- Source: `u107-a.json`, row `S01_record_not_json`
- Moved: U298 replaced label/sync_cli.load_record's own JSON read with config.read_json_map over config.read_json; the not JSON refusal is read_json's, and answering absent there makes load_record return its empty record, the same outcome the original return of _empty gave
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_record_that_cannot_be_read_refuses_rather_than_asking_everything_again`
  - `tests/test_label_sync.py::test_the_labels_sweep_refuses_an_unreadable_record_before_any_login`

Old text:

```
    except ValueError as exc:
        raise unusable("it is not JSON") from exc


def read_json_map(
```

New text:

```
    except ValueError as exc:
        return False, None


def read_json_map(
```

### `r356-b.B2_template_declares_no_lossy_marker`

The template never declares the marker, so a marked lossy copy keeps it in its release title

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B2_template_declares_no_lossy_marker`
- Moved: U298 folded this function's strip, empty check and marker rule into naming.NameTemplate.lossy_if_marked, which it now returns; returning the plain template here is what forcing the empty branch did, local to this caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_release_title_is_the_display_title_with_the_naming_head_off`

Old text:

```
    return naming.NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)
```

New text:

```
    return naming.NameTemplate()
```

### `r356-b.B3_empty_marker_no_longer_guarded`

A configuration with no marker text builds a marker rule with an empty literal, which is refused at construction, so every item fails over a naming policy

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B3_empty_marker_no_longer_guarded`
- Moved: U298 folded this function's strip, empty check and marker rule into naming.NameTemplate.lossy_if_marked; calling NameTemplate.lossy on the stripped text here skips only the empty check, so an empty marker reaches the rule's construction as it did, local to this caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_configuration_with_no_marker_text_still_strips_the_head`

Old text:

```
    return naming.NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)
```

New text:

```
    return naming.NameTemplate.lossy((cfg.naming.lossy_marker or "").strip())
```

### `u220.A3_keep_head`

_to_the_front: match the asked order's head rather than its tail, the old to the end rule

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u220.json`, row `A3_keep_head`
- Moved: U298 replaced tidal_account._to_the_front's body with sync.pair_stopped.front_moves, its copy until then, which the adapter now returns; the same tail match
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 26 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_nothing_to_move_tells_the_caller_nothing`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before2-order2]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before3-order3]`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - ... and 11 more, see the JSON sidecar

Old text:

```
one == wanted[len(wanted) - 1 - keep]
```

New text:

```
one == wanted[keep]
```

### `u220.A4_first_first`

_to_the_front: move the tracks first first rather than last first, so the moved ones land reversed

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u220.json`, row `A4_first_first`
- Moved: U298 replaced tidal_account._to_the_front's body with sync.pair_stopped.front_moves, its copy until then, which the adapter now returns; the same reversal of the moves
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before2-order2]`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
    return wanted[: len(wanted) - keep]
```

### `r1394.S3_bool_count_read`

stopped write: a count written as true or false is read as a number

- File: `src/cratekit/cli/output.py`
- Source: `r1394.json`, row `S3_bool_count_read`
- Moved: U298 replaced pair_stopped's _count with cli.output.count_of, the same three part check, which _moving now calls for both counts
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
```

New text:

```
    if not isinstance(value, int) or value < 0:
```

### `r1394.S4_negative_count_read`

stopped write: a negative count is read as one

- File: `src/cratekit/cli/output.py`
- Source: `r1394.json`, row `S4_negative_count_read`
- Moved: U298 replaced pair_stopped's _count with cli.output.count_of, the same three part check, which _moving now calls for both counts
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`

Old text:

```
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
```

New text:

```
    if isinstance(value, bool) or not isinstance(value, int):
```

### `r1394.S5_sent_read_as_landed`

stopped write: the sent count is read from the landed field, so a move in flight reads as known not sent

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S5_sent_read_as_landed`
- Moved: Same return in _moving; U298 replaced the module's _count with cli.output.count_of
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_stopped.py::test_a_moving_step_reads_back_its_counts`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
    return at, start, end, count_of(value.get(SENT)), count_of(value.get(LANDED))
```

New text:

```
    return at, start, end, count_of(value.get(LANDED)), count_of(value.get(LANDED))
```

### `u322.M22_backlog_partly_clause_gone`

backlog_cli.advisories: the partly read clause is dropped, so the campaign's gate says nothing of Beatport

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M22_backlog_partly_clause_gone`
- Moved: Same clause in advisories; U298 renamed _named to the public named
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`

Old text:

```
    if unread.partly:
        parts.append(
            f"{unread.partly_by} could not be read for {len(unread.partly)} row(s) "
            f"another catalogue answered, {named(list(unread.partly))}, so those were "
```

New text:

```
    if False:
        parts.append(
            f"{unread.partly_by} could not be read for {len(unread.partly)} row(s) "
            f"another catalogue answered, {named(list(unread.partly))}, so those were "
```

### `r668-a.M5_missing_list_guard_after_load`

the missing list refusal runs after the configuration is read, so a command naming nothing has side effects first

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M5_missing_list_guard_after_load`
- Moved: Same order in acquire_download; U298 replaced the private _load with cli.output.load_config, so the configuration read the guard is moved after is reworded
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`

Old text:

```
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
            "no list was named and no job was given, so there is nothing to acquire",
            "name the list of tracks to acquire",
            "or continue an acquisition already queued with --job JOB_ID",
        )
    cfg = load_config(("acquire.cli",))

```

New text:

```
    cfg = load_config(("acquire.cli",))
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
            "no list was named and no job was given, so there is nothing to acquire",
            "name the list of tracks to acquire",
            "or continue an acquisition already queued with --job JOB_ID",
        )

```

### `r668-a.M7_list_compared_as_strings`

the named and frozen lists are compared as strings, so a symlinked or /private spelling of the frozen list is refused

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M7_list_compared_as_strings`
- Moved: Same comparison in _same_list_or_refuse; U298 renamed preflight._names_one_path to names_one_path
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_frozen_list_spelled_through_a_symlink_still_drives`

Old text:

```
    if preflight.names_one_path(given, Path(frozen)):
```

New text:

```
    if str(given) == frozen:
```

### `r926.G11_mkdir_before_check`

save creates the configuration directory before the lock is built, so a refused write leaves a directory behind

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G11_mkdir_before_check`
- Moved: Same lines in save; U298 renamed _mkdir_private to the public mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 299 against a baseline of 299
- Kills: 9 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_an_append_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_an_append_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`

Old text:

```
    with _write_lock(target):
        mkdir_private(target.parent)
        atomic_write_bytes(config.to_toml_bytes(), target)
```

New text:

```
    mkdir_private(target.parent)
    with _write_lock(target):
        atomic_write_bytes(config.to_toml_bytes(), target)
```

### `r926.G3_document_check_dropped`

_write_lock no longer checks, so the configuration document is held only by the primitives' temporary allowance

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G3_document_check_dropped`
- Moved: Same lines in _write_lock; U298 renamed _exclusive_lock to the public exclusive_lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 299 against a baseline of 299
- Kills: 12 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_an_append_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_an_append_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

New text:

```
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

### `r926.G4_document_gets_temporary`

The configuration document is given the system temporary allowance the primitives have

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G4_document_gets_temporary`
- Moved: Same lines in _write_lock; U298 renamed _exclusive_lock to the public exclusive_lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 299 against a baseline of 299
- Kills: 12 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_an_append_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_an_append_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

New text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

### `r926.G5_atomic_write_unchecked`

atomic_write_bytes no longer checks, so a ledger or token write from an unisolated test lands anywhere

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G5_atomic_write_unchecked`
- Moved: Same lines in atomic_write_bytes; U298 renamed _mkdir_private to the public mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 299 against a baseline of 299
- Kills: 8 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_an_append_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_an_append_outside_the_root_is_refused_with_the_isolation_in_place`

Old text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(
```

New text:

```
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(
```

### `r926.G6_lock_unchecked`

_exclusive_lock no longer checks, so a session lock from an unisolated test is created anywhere

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G6_lock_unchecked`
- Moved: Same lines in the lock's __enter__; U298 renamed the class to exclusive_lock and _mkdir_private to mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 299 against a baseline of 299
- Kills: 8 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_an_append_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_an_append_outside_the_root_is_refused_with_the_isolation_in_place`

Old text:

```
        _refuse_write_outside_test_root(self.path, system_temporary=True)
        mkdir_private(self.path.parent)
```

New text:

```
        mkdir_private(self.path.parent)
```

### `r926.G8_target_unresolved`

The target is compared as spelled, so a link inside the root aimed outside it passes

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G8_target_unresolved`
- Moved: Same lines in _refuse_write_outside_test_root; U298 renamed _is_inside to the public is_inside
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 299 against a baseline of 299
- Kills: 8 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_an_append_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_an_append_outside_the_root_is_refused_with_the_isolation_in_place`

Old text:

```
    target = path.resolve()
    if any(is_inside(target, each) for each in allowed):
```

New text:

```
    target = path
    if any(is_inside(target, each) for each in allowed):
```

### `u217.K10_naive_instant`

_instant: accept an instant with no zone

- File: `src/cratekit/label/kept_reads.py`
- Source: `u217.json`, row `K10_naive_instant`
- Moved: U298 deleted kept_listing's copy of _instant and has KeptListing read through kept_reads._instant, the identical function; the zone check is the same line there
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_kept_listing_that_cannot_be_read_refuses_before_any_call[written5]`

Old text:

```
    return moment if moment.tzinfo is not None else None
```

New text:

```
    return moment
```

### `r375-b.M1_capture_never_attached`

mytags_vocals: take the capture and never attach it, which is R-375 itself with a record beside it

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `M1_capture_never_attached`
- Moved: U298 replaced mytags_vocals' own capture, attach and verify lines with trees.attached_capture, which it now calls; the attach is the same line there, so dropping it takes the capture and never attaches it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
    capture = snapshot.capture(cfg, db=db)
    session.attach_capture(record, capture.root, cfg)
    snapshot.assert_verified(capture)
    return record, capture
```

New text:

```
    capture = snapshot.capture(cfg, db=db)
    snapshot.assert_verified(capture)
    return record, capture
```

### `u219.G1_resort_abort`

route resort: an abort at the gate queues the resort anyway

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G1_resort_abort`
- Moved: Same gate answer in route_resort; U298 replaced the local _no_op with cli.output.no_job
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_an_abort_queues_nothing_and_writes_nothing`

Old text:

```
    if option != "apply":
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP, warnings=warnings)
```

New text:

```
    if option == "never":
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP, warnings=warnings)
```

### `r375-b.T5_witnessed_commit_not_recorded`

write_tree_membership: ignore the witness, so a commit that landed and then raised closes as though nothing landed

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T5_witnessed_commit_not_recorded`
- Moved: U298 moved write_tree_membership's failure path, the quiet rollback and the witnessed commit record, into trees._undo_unless_landed, which its except branch now calls; the same witness check
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`

Old text:

```
    if witness.landed:
        _record_membership_commit(record, tree_id, added, cfg)
```

New text:

```
    if False:
        _record_membership_commit(record, tree_id, added, cfg)
```

### `r375-c.T6_every_raise_read_as_a_commit_again`

write_tree_membership: record a commit on every raise. Batch B read this as ZERO; measured again after test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit

- File: `src/cratekit/write/trees.py`
- Source: `r375-c.json`, row `T6_every_raise_read_as_a_commit_again`
- Moved: U298 moved write_tree_membership's failure path, the quiet rollback and the witnessed commit record, into trees._undo_unless_landed, which its except branch now calls; the same witness check
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit`

Old text:

```
    if witness.landed:
        _record_membership_commit(record, tree_id, added, cfg)
```

New text:

```
    if True:
        _record_membership_commit(record, tree_id, added, cfg)
```

### `u254.M20_mark_unlocked`

mark_applied: take no lock around the read, the choice and the write

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M20_mark_unlocked`
- Moved: Same with statement in mark_applied; U298 renamed config._exclusive_lock to exclusive_lock
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 770 against a baseline of 770
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_every_ledger_write_happens_under_the_exclusive_lock`

Old text:

```
    with config.exclusive_lock(lock_path(cfg)):
        known = _LEFT.pop(key, None)
```

New text:

```
    if True:
        known = _LEFT.pop(key, None)
```

### `u192.A1_run_queue_only_ignored`

analyze_run: ignore --queue-only and drive the job

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A1_run_queue_only_ignored`
- Moved: Same branch in analyze_run; U298 replaced the local _reported with core.jobs.reported
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_item_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[run]`
  - `tests/test_analysis_workers.py::test_the_shared_tail_step_queues_only_and_drives_its_job_once`

Old text:

```
        if foreground.queue_only(ctx.args):
            return ctx.envelope(data=jobs.reported(store, job))
```

New text:

```
        if False:
            return ctx.envelope(data=jobs.reported(store, job))
```

### `u192.A2_restamp_queue_only_ignored`

analyze_restamp: ignore --queue-only and drive the job

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A2_restamp_queue_only_ignored`
- Moved: Same branch in analyze_restamp; U298 replaced the local _reported with core.jobs.reported
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[restamp]`

Old text:

```
        if foreground.queue_only(ctx.args):
            return ctx.envelope(
                data=jobs.reported(store, job), warnings=(DB_NOT_WRITTEN, *extra)
```

New text:

```
        if False:
            return ctx.envelope(
                data=jobs.reported(store, job), warnings=(DB_NOT_WRITTEN, *extra)
```

### `u27-reports-round-1.S6_lossy_marker`

Build the naming template without the configured lossy marker

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S6_lossy_marker`
- Moved: U298 folded this template's strip, empty check and marker rule into naming.NameTemplate.lossy_if_marked, which it now returns; the plain template here drops the configured marker as before, local to this verb
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_rejected_pair_comes_back_suppressed_rather_than_as_a_question`
  - `tests/test_reports_cli.py::test_a_second_run_re_offers_the_same_item_rather_than_a_second_one`
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`

Old text:

```
    return NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)
```

New text:

```
    return NameTemplate()
```

### `u194.W20_retag_reread`

_retag: drop the read before the write, so a file changed since the second plan is written over

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W20_retag_reread`
- Moved: Same read before the write in _retag; U298 replaced the local _genres with tagging.tag.file_genres, the identical exact reader
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_changed_after_the_second_plan_is_left_and_named`

Old text:

```
        if file_genres(item.path) != (item.current,):
            done.moved.append(item)
```

New text:

```
        if False:
            done.moved.append(item)
```

### `u194.W21_retag_read_back`

_retag: drop the read back, so a write that did not take is counted as retagged

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W21_retag_read_back`
- Moved: Same read back in _retag; U298 replaced the local _genres with tagging.tag.file_genres, the identical exact reader
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_write_that_does_not_read_back_is_named_apart_from_one_never_made`

Old text:

```
        if file_genres(item.path) != (display,):
            done.wrong.append(item)
```

New text:

```
        if False:
            done.wrong.append(item)
```

### `u57-recognition-and-items.C12_stray_file_sorted`

The report reader sorts every json file by its stem as a number again

- File: `src/cratekit/core/jobs.py`
- Source: `u57-recognition-and-items.json`, row `C12_stray_file_sorted`
- Moved: U298 deleted core/artifacts.py and folded its committed reader into core.jobs.Artifacts.committed, whose default order is by_ordinal; the filter to ordinal named files before the numeric sort is that function's, and dropping it lets a stray json file reach int() as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_stray_file_beside_the_reports_does_not_take_the_summary_down`

Old text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: int(item.stem))
```

New text:

```
    return sorted(paths, key=lambda item: int(item.stem))
```

### `r504-b.B5_noop_silent`

Every heart withheld is the quiet no-op again, with no warning

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B5_noop_silent`
- Moved: Same no-tracks return in intake_playlist; U298 replaced the local _no_op with cli.output.no_job
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 682 against a baseline of 682
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
                warnings=warnings,
            )
```

New text:

```
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
            )
```

### `r515-operator.S10_intake_all_withheld_quiet`

An intake playlist with every track withheld is a quiet no op

- File: `src/cratekit/intake/cli.py`
- Source: `r515-operator.json`, row `S10_intake_all_withheld_quiet`
- Moved: Same no-tracks return in intake_playlist; U298 replaced the local _no_op with cli.output.no_job
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        if not tracks:
            return ctx.envelope(
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
                warnings=warnings,
```

New text:

```
        if not tracks:
            return ctx.envelope(
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
```

### `u62.C1_bound_constant_true`

Answer bound() True without asking whether the adapter imports

- File: `src/cratekit/label/catalogue.py`
- Source: `u62.json`, row `C1_bound_constant_true`
- Moved: Same bound(); U298 replaced its try import with provider_session.importable, the same question, so answering True here skips it as before, local to this function
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/intake/test_workers.py`
- Collected: 544 against a baseline of 544
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_catalogue_seam_answers_bound_without_reading_a_credential`

Old text:

```
    return provider_session.importable(ADAPTER_MODULE)
```

New text:

```
    return True
```

### `r815-c.J8_a_refusal_parks_and_fails_no_item`

handle: let a refusal fail the item

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J8_a_refusal_parks_and_fails_no_item`
- Moved: Same except clause in handle; U298 replaced artifacts.produced(ARTIFACTS, ...) with the bound ARTIFACTS.produced on core.jobs.Artifacts, only the line after the guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_refusal_from_the_provider_parks_the_run_on_that_refusal`
  - `tests/test_label_judge.py::test_a_taxonomy_that_stops_being_readable_parks_the_run_and_fails_no_release`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    except CratekitError as exc:
        raise _parked(job, exc) from exc
    return ARTIFACTS.produced(cfg, job, item, report)
```

New text:

```
    except CratekitError:
        raise
    return ARTIFACTS.produced(cfg, job, item, report)
```

### `u46-round-2.M2_resume_does_not_drive`

Report the queued job on resume without running any of it, which is the state R-198 describes

- File: `src/cratekit/core/jobs.py`
- Source: `u46-round-2.json`, row `M2_resume_does_not_drive`
- Moved: U298 replaced master's resume with core.jobs.resumed, which master_recording now calls after its reconcile; the drive inside its is_open branch is the same two lines, so removing it reports the queued job without running any of it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 15 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`

Old text:

```
        _result, warnings = ctx.run_job(store, job)
        job = get(store, job.job_id)
```

New text:

```
        pass
```

### `u43-author-round-2.H4_template_loses_the_marker`

ROUND ONE: zero. The name template stops declaring the lossy marker, so a marked file's clean title keeps the marker and its match key gains a token

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H4_template_loses_the_marker`
- Moved: Same template function; U298 spelled its marker rule as naming.NameTemplate.lossy, which builds the same lossy MarkerRule, so the plain template drops it as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`

Old text:

```
    return NameTemplate.lossy(cfg.naming.lossy_marker)
```

New text:

```
    return NameTemplate()
```

### `u43-author-round-2.V2_marker_position_moved`

The marker rule is declared with a separator that puts it somewhere the head parser does not strip. If the lossy guard passes this, its fixture is in a position where the declaration cannot matter, which is the mistake the first attempt at it made

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V2_marker_position_moved`
- Moved: Same template function; U298 spelled its marker rule as naming.NameTemplate.lossy, so the wrong literal is passed to it in place of the configured marker, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`

Old text:

```
    return NameTemplate.lossy(cfg.naming.lossy_marker)
```

New text:

```
    return NameTemplate.lossy("[NOTAMARKER]")
```

### `u56-catalogue-searcher-and-tag-workers.R37_artifact_named_by_item_id`

A filename built from a tagging item identifier is a path traversal wearing a report, because the identifier is a path relative to a folder

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R37_artifact_named_by_item_id`
- Moved: U298 folded tagging/artifacts.final_path into core.jobs.Artifacts.final_path, which tagging binds as final_path; the same name built from the ordinal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_item_identifier_holding_a_separator_cannot_escape_the_directory`

Old text:

```
        directory = self.final_dir(cfg, job_id)
        config.mkdir_private(directory)
        return directory / f"{ordinal:04d}.json"
```

New text:

```
        directory = self.final_dir(cfg, job_id)
        config.mkdir_private(directory)
        return directory / f"{ordinal}.json"
```

### `u56-catalogue-searcher-and-tag-workers.R38_staging_not_cleared`

A half written report from an attempt that did not finish is committed by the next attempt as though it described that attempt

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R38_staging_not_cleared`
- Moved: U298 folded tagging/artifacts.staged_path into core.jobs.Artifacts.staged_path, which tagging binds as staged_path and produced calls; the same clearing of a stale attempt
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_staging_is_cleared_before_an_attempt_writes_into_it`

Old text:

```
        if directory.exists():
            shutil.rmtree(directory)
```

New text:

```
        if False:
            shutil.rmtree(directory)
```

### `r799-b.W1_a_file_is_read_again_before_it_is_written`

apply: write over whatever the file carries by now

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W1_a_file_is_read_again_before_it_is_written`
- Moved: Same read before the write in apply; U298 replaced the local _file_genres with tagging.tag.file_genres, the identical exact reader
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_that_moved_since_the_plan_is_named_and_not_written`

Old text:

```
        if file_genres(target) != (item.current,):
            moved.append(item.path)
            continue
```

New text:

```
(empty)
```

### `r799-b.W3_a_write_is_read_back`

apply: take the writer's word that the genre is on the file

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W3_a_write_is_read_back`
- Moved: Same read back in apply; U298 replaced the local _file_genres with tagging.tag.file_genres, the identical exact reader
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_written_that_does_not_read_back_is_named_as_wrong`

Old text:

```
        if file_genres(target) != (item.wanted,):
            wrong.append(item.path)
            continue
```

New text:

```
(empty)
```

### `r290-author.S11_tagging_shell_call_removed`

Remove the one jobs.raise_for_state call from tagging/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `S11_tagging_shell_call_removed`
- Moved: U298 replaced the resume tails of tagging.shell.advance, adopt.shell.advance, acquire fallback-fetch and master with core.jobs.resumed, which advance calls; its one raise_for_state call is the mapping each of those four shells made, and tests/test_job_outcome.py names that function as the shared tail. The tests are this row's own plus those of the three rows mapped to it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`, `tests/test_adopt_workers.py`, `tests/test_master_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 390 against a baseline of 390
- Kills: 49 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.apply]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[master]`
  - ... and 34 more, see the JSON sidecar

Old text:

```
    raise_for_state(job)
    return job, warnings
```

New text:

```
    get  # the mapping call, removed
    return job, warnings
```

### `u56-catalogue-searcher-and-tag-workers.R33_no_op_job_id_is_null`

R-234 reintroduced: cli.output types job_id as a required string, so a null fails the verb's own schema on every zero path

- File: `src/cratekit/cli/output.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R33_no_op_job_id_is_null`
- Moved: U298 replaced tagging.shell.no_op with cli.output.no_job, which the tagging shell imports as no_op; the same empty string job_id
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 9 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_holding_no_audio_queues_nothing_and_says_which_zero_it_is`
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_one_with_nothing_coarse`
  - `tests/test_tag_workers.py::test_an_empty_folder_argument_never_sweeps_the_working_directory`
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_still_queues_nothing`
  - `tests/test_tag_workers.py::test_answering_the_confirmation_with_abort_queues_nothing_and_writes_nothing`
  - `tests/test_tag_workers.py::test_tagging_the_download_root_queues_nothing_from_the_acquisition_staging_tree`
  - `tests/test_tag_workers.py::test_the_honest_zero_names_an_empty_job_id_rather_than_a_null`
  - `tests/test_tag_workers.py::test_the_honest_zero_validates_against_the_job_state_surface`

Old text:

```
    return {"job_id": "", "state": state, "cause": None, "progress": dict(progress)}
```

New text:

```
    return {"job_id": None, "state": state, "cause": None, "progress": dict(progress)}
```

### `u56-catalogue-searcher-and-tag-workers.R34_empty_job_is_driven`

A job frozen with no items drives straight to SUCCEEDED, which is a clean report over work it never did

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R34_empty_job_is_driven`
- Moved: U298 replaced tagging.shell.advance with core.jobs.advance, which the tagging shell imports under the same name; the refusal of an open job with no items is the same check, now one condition, and the mutation drops only its items half
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_job_with_no_items_is_refused_rather_than_driven`

Old text:

```
    if job.is_open() and not items(store, job.job_id):
```

New text:

```
    if job.is_open() and False:
```

### `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress`

A per verb detail at the top level is an undeclared field on job_state/1, so a consumer generated from the committed schema rejects every envelope

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R35_extra_rides_beside_progress`
- Moved: U298 replaced tagging.shell.reported with core.jobs.reported, which the tagging shell imports under the same name; the same placement of extra under progress, with the local renamed counted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 47 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - ... and 32 more, see the JSON sidecar

Old text:

```
    counted = dict(progress(store, job.job_id))
    if extra:
        counted.update(extra)
    return {
        "job_id": job.job_id,
```

New text:

```
    counted = dict(progress(store, job.job_id))
    return {
        **dict(extra or {}),
        "job_id": job.job_id,
```

### `u225.M6_front_keeps_nothing`

front_moves: no tail is kept, every asked track is moved

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M6_front_keeps_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`

Old text:

```
            keep += 1
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
            keep += 0
    return list(reversed(wanted[: len(wanted) - keep]))
```

