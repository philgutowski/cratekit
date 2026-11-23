# Mutation table: u306-replay-after-c

Measured by `scripts/mutate.py` on 2026-11-22 22:33 UTC, branch `HEAD` at `639d853c`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22940 collected. pytest invocations for this batch: 45.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 2, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/home/user/tools/known-failures-inode.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22940 against 22940. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r650-a.B5_artifact_drops_the_key` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 3 | killed |
| `r650-a.C1_summary_counts_nothing` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C3_summary_drops_the_key` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 4 | killed |
| `r650-a.C4_warning_fires_on_a_clean_sweep` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C6_warning_names_no_strings` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C7_warning_order_is_the_walk_order` | `src/cratekit/tagging/cli.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `r650-a.C8_warning_code_reworded` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r650-a.C9_warning_counts_the_wrong_total` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r650-a.D3_unresolved_is_fed_by_declines` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 1 | killed |
| `u281.C2_challenge_never_named` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 1 | killed |
| `u281.C3_unsent_never_counted` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 2 | killed |
| `u281.C4_source_blocked_counts_unsent_as_sent` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u281.C5_partial_challenge_called_whole` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R20_unnamed_folder_sweeps_cwd` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R21_two_zeroes_read_as_one` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R22_vanished_file_reports_done` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 27 | killed |
| `u84-b.C1_artifact_carries_status` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u84-b.C2_summary_zero_filled` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 2 | killed |
| `u84-b.C3_old_reports_uncounted` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 1 | killed |
| `u85-a.A15_worker_hands_in_the_fetch` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 3 | killed |
| `u85-a.A16_summary_counts_art` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 1 | killed |
| `r1103.H3_message_names_no_file` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r1103.H4_detail_path` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r1103.H5_detail_genre` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r1103.H6_detail_current` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r816-e.E1_retag_names_the_verb` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R28_worker_trusts_the_frozen_row` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R29_blank_genre_is_corrected` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R30_specific_genre_is_overwritten` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R31_artifact_drops_the_previous_value` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u263.D10_first_stream` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 1 | killed |
| `u263.D11_mono_shape` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 2 | killed |
| `u263.D12_channels_first` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 7 | killed |
| `u263.D13_extensible` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 52 | 11 | killed |
| `u263.D14_whole_frames` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 52 | 1 | killed |
| `u263.D15_chunk_padding` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 52 | 1 | killed |
| `u263.D23_cover_lines` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 4 | killed |
| `u263.D7_stderr_fails` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 2 | killed |
| `u263.D9_file_protocol` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 1 | killed |

## Row definitions

### `r650-a.B5_artifact_drops_the_key`

The committed item report stops carrying the flag, so the summary reads it back as absent

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `B5_artifact_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
            "off_taxonomy": result.off_taxonomy,
```

New text:

```
(empty)
```

### `r650-a.C1_summary_counts_nothing`

The report stops counting the strings, leaving the map empty on a folder that has them

- File: `src/cratekit/tagging/summary.py`
- Source: `r650-a.json`, row `C1_summary_counts_nothing`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
            if report.get("off_taxonomy") and source_genre:
                off_taxonomy[source_genre] = off_taxonomy.get(source_genre, 0) + 1
```

New text:

```
(empty)
```

### `r650-a.C3_summary_drops_the_key`

The payload stops carrying the map at all

- File: `src/cratekit/tagging/summary.py`
- Source: `r650-a.json`, row `C3_summary_drops_the_key`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
        "off_taxonomy": off_taxonomy,
```

New text:

```
(empty)
```

### `r650-a.C4_warning_fires_on_a_clean_sweep`

The empty check goes, so an ordinary folder is warned about a gap it does not have

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C4_warning_fires_on_a_clean_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning`

Old text:

```
    if not counted:
        return ()
```

New text:

```
(empty)
```

### `r650-a.C6_warning_names_no_strings`

The warning says a gap exists and not which word, which is the R24 mistake one verb over

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C6_warning_names_no_strings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
                f"these catalogue answers: {words}. Each word was written onto "
```

New text:

```
                f"these catalogue answers. Each word was written onto "
```

### `r650-a.C7_warning_order_is_the_walk_order`

The strings are listed in commit order, so two runs over one folder disagree

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C7_warning_order_is_the_walk_order`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
    words = ", ".join(sorted(counted))
```

New text:

```
    words = ", ".join(counted)
```

### `r650-a.C8_warning_code_reworded`

The code a log filter reads is reworded, never appended to

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C8_warning_code_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
OFF_TAXONOMY = "tag-folder-off-taxonomy"
```

New text:

```
OFF_TAXONOMY = "tag-folder-unknown-word"
```

### `r650-a.C9_warning_counts_the_wrong_total`

The warning names the file count as the sweep's whole tagged total

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C9_warning_counts_the_wrong_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
    files = sum(counted.values())
```

New text:

```
    files = summary.get("tagged", 0)
```

### `r650-a.D3_unresolved_is_fed_by_declines`

Existing: the unresolved map is filled from unmapped-genre and from nothing else

- File: `src/cratekit/tagging/summary.py`
- Source: `r650-a.json`, row `D3_unresolved_is_fed_by_declines`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
        if reason == tag_engine.UNMAPPED_GENRE and source_genre:
```

New text:

```
        if source_genre:
```

### `u281.C2_challenge_never_named`

_summary: never count a Cloudflare challenge, so the warning cannot name one

- File: `src/cratekit/tagging/summary.py`
- Source: `u281.json`, row `C2_challenge_never_named`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                if searchers.CLOUDFLARE_CHALLENGE in note:
                    challenged[source] += 1
```

New text:

```
                if False:
                    challenged[source] += 1
```

### `u281.C3_unsent_never_counted`

_summary: never count a file a catalogue was not sent

- File: `src/cratekit/tagging/summary.py`
- Source: `u281.json`, row `C3_unsent_never_counted`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                if note.startswith(searchers.NOT_SENT):
                    not_sent[source] += 1
```

New text:

```
                if False:
                    not_sent[source] += 1
```

### `u281.C4_source_blocked_counts_unsent_as_sent`

_unread_warnings: count the unsent files among the searches sent, so the warning claims searches never made

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C4_source_blocked_counts_unsent_as_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
        sent = asked - held
```

New text:

```
        sent = asked
```

### `u281.C5_partial_challenge_called_whole`

_unread_phrase: call every refusal a challenge when any one was

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C5_partial_challenge_called_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many`

Old text:

```
    if challenged >= count:
```

New text:

```
    if challenged:
```

### `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items`

The zero item rule broken at its source: a job with nothing to claim drives straight to SUCCEEDED over a folder nothing walked

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R19_folder_queues_no_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 41 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_fails_only_its_own_item`
  - ... and 26 more, see the JSON sidecar

Old text:

```
            item_ids=tuple(str(path.relative_to(folder)) for path in files),
```

New text:

```
            item_ids=(),
```

### `u56-catalogue-searcher-and-tag-workers.R20_unnamed_folder_sweeps_cwd`

Path("") is the current directory, so an unnamed folder writes genres into whatever the person is standing in

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R20_unnamed_folder_sweeps_cwd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_empty_folder_argument_never_sweeps_the_working_directory`

Old text:

```
    named = str(ctx.args.folder or "")
    if not named.strip():
```

New text:

```
    named = str(ctx.args.folder or "")
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R21_two_zeroes_read_as_one`

A mistyped path reports as a folder with nothing to tag, which is the answer most likely to stop somebody looking

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R21_two_zeroes_read_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`

Old text:

```
            if folder.is_dir()
            else _empty(
                "tag-folder-absent",
```

New text:

```
            if True
            else _empty(
                "tag-folder-absent",
```

### `u56-catalogue-searcher-and-tag-workers.R22_vanished_file_reports_done`

An item whose file is gone reports done having tagged nothing, which is the clean report over unreadable state the merge bar names

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R22_vanished_file_reports_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`

Old text:

```
    path = folder / item.item_id
    if not path.is_file():
```

New text:

```
    path = folder / item.item_id
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue`

The report counts what was queued rather than what ran, so a half finished sweep reports every file as handled

- File: `src/cratekit/tagging/summary.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R23_summary_from_the_queue`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 27 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - ... and 12 more, see the JSON sidecar

Old text:

```
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

New text:

```
    for report in []:
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

### `u84-b.C1_artifact_carries_status`

The item artifact drops the repair status, so nothing on disk records what the repair did

- File: `src/cratekit/tagging/cli.py`
- Source: `u84-b.json`, row `C1_artifact_carries_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`

Old text:

```
            "art_repair": result.art_repair,

```

New text:

```
(empty)
```

### `u84-b.C2_summary_zero_filled`

The summary lists only the statuses it saw, so none repaired and not counted read the same

- File: `src/cratekit/tagging/summary.py`
- Source: `u84-b.json`, row `C2_summary_zero_filled`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`

Old text:

```
        "art_repair": art_repair,
```

New text:

```
        "art_repair": {key: value for key, value in art_repair.items() if value},
```

### `u84-b.C3_old_reports_uncounted`

A report committed before the repair existed is counted as ok, a status nobody measured

- File: `src/cratekit/tagging/summary.py`
- Source: `u84-b.json`, row `C3_old_reports_uncounted`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`

Old text:

```
        status = str(report.get("art_repair") or "")
```

New text:

```
        status = str(report.get("art_repair") or art.REPAIR_OK)
```

### `u85-a.A15_worker_hands_in_the_fetch`

The worker passes no image fetch, so the verb never embeds art

- File: `src/cratekit/tagging/cli.py`
- Source: `u85-a.json`, row `A15_worker_hands_in_the_fetch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`

Old text:

```
        fetch_image=searchers.for_images(),

```

New text:

```
(empty)
```

### `u85-a.A16_summary_counts_art`

The job summary never counts an art status

- File: `src/cratekit/tagging/summary.py`
- Source: `u85-a.json`, row `A16_summary_counts_art`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`

Old text:

```
            art_fetch[fetched] += 1
```

New text:

```
            pass
```

### `r1103.H3_message_names_no_file`

handle: reword the refusal so it names no file

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H3_message_names_no_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`

Old text:

```
            f"{path} would not take the genre {result.proposed!r}, so it still "
```

New text:

```
            f"the file would not take the genre {result.proposed!r}, so it still "
```

### `r1103.H4_detail_path`

handle: the refusal's detail loses the file's path

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H4_detail_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
                "path": str(path),
```

New text:

```
                "path": "",
```

### `r1103.H5_detail_genre`

handle: the refusal's detail names the genre the file still carries as the one it would not take

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H5_detail_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
                "genre": result.proposed,
```

New text:

```
                "genre": result.current,
```

### `r1103.H6_detail_current`

handle: the refusal's detail loses the genre the file still carries

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H6_detail_current`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
                "current": result.current,
```

New text:

```
                "current": "",
```

### `r816-e.E1_retag_names_the_verb`

library_row_warning: name no verb, reworded

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r816-e.json`, row `E1_retag_names_the_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`

Old text:

```
because this verb writes the file half only; run `crate tag "
            f"rows` so the rows catch up
```

New text:

```
because this verb writes the file half only; run the row "
            f"verb so the rows catch up
```

### `u56-catalogue-searcher-and-tag-workers.R28_worker_trusts_the_frozen_row`

The genre is not re-read at drive time, so a file somebody corrected by hand between the confirmation and the drive is corrected again

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R28_worker_trusts_the_frozen_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`

Old text:

```
    current = tags.read_genre_from_file(path) or ""
    if not current:
```

New text:

```
    current = tags.read_genre_from_file(path) or ""
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R29_blank_genre_is_corrected`

The retag writes into a field tag.folder owns under fill if empty, which is one field under two policies

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R29_blank_genre_is_corrected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`

Old text:

```
    if not current:
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

New text:

```
    if current == "\\u0000":
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

### `u56-catalogue-searcher-and-tag-workers.R30_specific_genre_is_overwritten`

A queued job overwrites somebody's own curation, which is the write this verb exists to avoid making

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R30_specific_genre_is_overwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[Ambient-read_back0-genre-specific]`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`

Old text:

```
    elif not declared.is_too_coarse_as_source(current):
```

New text:

```
    elif False:
```

### `u56-catalogue-searcher-and-tag-workers.R31_artifact_drops_the_previous_value`

R-185's only record: without the previous genre the artifacts stop naming which library rows went stale, so the deferred database half has no population to read

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R31_artifact_drops_the_previous_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it`

Old text:

```
            "current": result.current,
            "written": result.written,
```

New text:

```
            "written": result.written,
```

### `u263.D10_first_stream`

_ffmpeg_samples: drop the map to the first audio stream

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D10_first_stream`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_taken_even_when_another_is_the_default`

Old text:

```
        "-map", "0:a:0",

```

New text:

```
(empty)
```

### `u263.D11_mono_shape`

_ffmpeg_samples: keep a mono file two dimensional

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D11_mono_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[1]`
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_taken_even_when_another_is_the_default`

Old text:

```
    if channels == 1:
        native = native[0]
```

New text:

```
(empty)
```

### `u263.D12_channels_first`

_ffmpeg_samples: leave the samples frames first, not librosa's channels first

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D12_channels_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[broken-png]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[gif-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[webp-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[2]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[6]`
  - `tests/test_analysis_decode.py::test_an_ffmpeg_that_exits_non_zero_saying_nothing_fails`
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_the_one_decoded`

Old text:

```
    native = frames.reshape(-1, channels).T
```

New text:

```
    native = frames.reshape(channels, -1)
```

### `u263.D13_extensible`

_parse_float_wav: read the extensible tag without its sub format

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D13_extensible`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[broken-png]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[gif-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[webp-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[1]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[2]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[6]`
  - `tests/test_analysis_decode.py::test_a_path_with_a_colon_is_read_as_a_file`
  - `tests/test_analysis_decode.py::test_the_decode_writes_no_file`
  - `tests/test_analysis_decode.py::test_the_extensible_header_and_a_chunk_before_the_data_are_read`
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_taken_even_when_another_is_the_default`
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_the_one_decoded`

Old text:

```
            if fmt_tag == _WAVE_FORMAT_EXTENSIBLE:
                (fmt_tag,) = struct.unpack("<H", blob[body + 24 : body + 26])
```

New text:

```
(empty)
```

### `u263.D14_whole_frames`

_parse_float_wav: keep a stray sample past the last whole frame

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D14_whole_frames`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_float_wav_on_a_pipe_is_read_to_its_end_in_whole_frames`

Old text:

```
            whole = available - available % (4 * channels)
```

New text:

```
            whole = available - available % 4
```

### `u263.D15_chunk_padding`

_parse_float_wav: skip an odd sized chunk without its pad byte

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D15_chunk_padding`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_the_extensible_header_and_a_chunk_before_the_data_are_read`

Old text:

```
        position = body + size + (size & 1)
```

New text:

```
        position = body + size
```

### `u263.D23_cover_lines`

_audio_faults: keep the cover decoders' lines, so a cover ffmpeg cannot read fails a whole track

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D23_cover_lines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_cover_complaint_is_dropped_and_an_audio_complaint_is_kept`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[broken-png]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[gif-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[webp-as-jpeg]`

Old text:

```
        if line.strip() and not line.startswith(tuple(f"[{name} @ " for name in _COVER_DECODERS))
```

New text:

```
        if line.strip()
```

### `u263.D7_stderr_fails`

_ffmpeg_samples: trust the exit code alone, so a mid file error yields the first half

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D7_stderr_fails`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_an_m4a_damaged_in_the_middle_fails_rather_than_yielding_its_first_half[aac]`
  - `tests/test_analysis_decode.py::test_an_m4a_damaged_in_the_middle_fails_rather_than_yielding_its_first_half[alac]`

Old text:

```
    if proc.returncode != 0 or said:
```

New text:

```
    if proc.returncode != 0:
```

### `u263.D9_file_protocol`

_ffmpeg_samples: pass the path bare, so a name with a colon is read as a protocol

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D9_file_protocol`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_path_with_a_colon_is_read_as_a_file`

Old text:

```
        "-i", f"file:{path}",
```

New text:

```
        "-i", f"{path}",
```

