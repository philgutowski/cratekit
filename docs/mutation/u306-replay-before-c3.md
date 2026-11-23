# Mutation table: u306-replay-before-c3

Measured by `scripts/mutate.py` on 2026-11-22 21:48 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 75.

Full baseline: measured by this driver (the battery's verdict was not read: this tree has uncommitted or untracked changes).

Subset baselines: 4, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/known.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u264.M13_float64_halving` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 4 | killed |
| `u264.M2_leading_zero_dropped` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 1 | killed |
| `u264.M3_trailing_zero_dropped` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 2 | killed |
| `u264.M4_table_rule_1_0` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 1 | killed |
| `u264.M5_halving` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 7 | killed |
| `u264.M6_any_release_measured` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 52 | 8 | killed |
| `u114.M10_file_has_genre` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 4 | killed |
| `u114.M11_file_word_votes` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M12_below_band` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M13_band_order` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M14_genre_unknown` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M15_file_moved` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M16_file_read_back` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M17_rows_follow_files` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 3 | killed |
| `u114.M1_suggestable_routes_only` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 5 | killed |
| `u114.M21_kept_days` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M22_unread_day` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M23_breaker` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M24_retry_unread` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 2 | killed |
| `u114.M25_settled_not_asked` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M2_high_share` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M3_high_votes` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 2 | killed |
| `u114.M4_split` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 3 | killed |
| `u114.M5_total_declared_only` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M6_folder_weight` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M7_votes_once` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M9_catalogue_declared` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u244.M03_kept_passed_over_reasked` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M19_write_intent` | `src/cratekit/tagging/suggest_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M20_pick_declared` | `src/cratekit/tagging/suggest_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `r796-c.V1_the_worker_hands_the_seam_over` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 10 | killed |
| `r796-c.V2_blocked_warning_is_the_shops_only` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V3_some_unread_is_said` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V4_no_isrc_is_warned_about` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V5_parse_break_sentence_said_once` | `src/cratekit/tagging/cli.py` | maintainer | 4 file(s) | 381 | 1 | killed |
| `r796-a.L1_no_data_is_a_miss` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 6 | killed |
| `r796-a.L2_quota_is_blocked` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 5 | killed |
| `r796-a.L3_unknown_error_is_not_a_miss` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 2 | killed |
| `r796-a.L4_refusal_check_on_a_200` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-a.L5_answer_is_about_the_isrc_asked` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 3 | killed |
| `r796-a.L6_album_id_is_a_positive_integer` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 6 | killed |
| `r796-a.L7_a_refusal_is_remembered` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 4 | killed |
| `r796-a.L8_only_a_refusal_is_remembered` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 4 | killed |
| `r796-b.O3_a_usable_answer_is_never_replaced` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 2 | killed |
| `r796-b.O5_a_declined_beatport_match_is_asked_about` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 5 | killed |
| `r796-b.O6_unread_joins_the_unread_names` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 7 | killed |
| `r796-c.V6_one_lookup_per_process` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 3 | killed |
| `r796-c.V7_the_request_names_this_tool` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-d.L9_first_isrc_of_several_again` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 9 | killed |
| `r796-d.O7_a_decline_keeps_the_shops_word_again` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 381 | 3 | killed |
| `r796-b.O9_no_isrc_is_not_no_hit` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 381 | 3 | killed |
| `r1476.M10_no_name_slug_step` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 4 | killed |
| `r1476.M11_slug_step_beats_exact_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M12_no_identifier_fallback` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 3 | killed |
| `r1476.M13_needles_not_held` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 11 | killed |
| `r1476.M14_genre_join_by_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M15_answer_without_genre` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 5 | killed |
| `r1476.M16_unsluggable_raises` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M17_remedy_names_display_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 3 | killed |
| `r1476.M18_remedy_head_never_shared` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M19_outranked_wording` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M1_identifier_not_frozen` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 7 | killed |
| `r1476.M2_folder_seam_by_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M3_folder_seam_with_no_identifier` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M6_worker_hands_no_folder_seam` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M7_worker_hands_identifier_as_label` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M8_shared_name_takes_first` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 10 | killed |
| `r1476.M9_identifier_first` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 5 | killed |
| `r1476.M4_engine_ignores_folder_seam` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 286 | 2 | killed |

## Row definitions

### `u264.M13_float64_halving`

_mean_of_two: add and halve in float64 and round once, so a finite pair whose float32 sum overflows mixes to a finite value

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M13_float64_halving`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-0.0-right5-80000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-3e+38--3e+38-ff800000-ff800000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[3e+38-3e+38-7f800000-7f800000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left4-0.0-80000000-00000000]`

Old text:

```
    out = np.add(stereo[0], stereo[1])
    # numpy's reduction starts from plus zero: minus zero plus minus zero is
    # minus zero here and plus zero in the mean, and no other sum changes.
    out += out.dtype.type(0)
    out /= out.dtype.type(2)
```

New text:

```
    out = ((stereo[0].astype(np.float64) + stereo[1]) / 2).astype(stereo.dtype)
    out += out.dtype.type(0)
```

### `u264.M2_leading_zero_dropped`

_mean_of_two: drop the plus zero numpy's reduction starts from, so two minus zero channels mix to minus zero

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M2_leading_zero_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-0.0--0.0-00000000-00000000]`

Old text:

```
    out = np.add(stereo[0], stereo[1])
    # numpy's reduction starts from plus zero: minus zero plus minus zero is
    # minus zero here and plus zero in the mean, and no other sum changes.
    out += out.dtype.type(0)
```

New text:

```
    out = np.add(stereo[0], stereo[1])
```

### `u264.M3_trailing_zero_dropped`

_mean_of_two: drop librosa 1.0's buffer of zeros, so a half sum that rounds to minus zero stays minus zero on 1.0

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M3_trailing_zero_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-0.0-right5-80000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left4-0.0-80000000-00000000]`

Old text:

```
    if zero_after:
        # librosa 1.0 adds the mean into zeros: a half sum that rounds to
        # minus zero, minus the smallest subnormal and zero, is plus zero.
        out += out.dtype.type(0)
```

New text:

```
    if zero_after:
        pass
```

### `u264.M4_table_rule_1_0`

_MEASURED_MIX: give 1.0.0 the rule of the releases before it

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M4_table_rule_1_0`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[1.0.0-True]`

Old text:

```
    "1.0.0": True,
```

New text:

```
    "1.0.0": False,
```

### `u264.M5_halving`

_mean_of_two: return the sum of the two channels, not its half

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M5_halving`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-0.0-right5-80000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left4-0.0-80000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left6--0.0-00000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left7-0.0-00000002-00000002]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left8--0.0-80000002-80000002]`
  - `tests/test_analysis_decode.py::test_the_half_sum_of_two_channels_rounds_once_like_float64[0.10-0.11]`
  - `tests/test_analysis_decode.py::test_the_half_sum_of_two_channels_rounds_once_like_float64[1.0]`

Old text:

```
    out /= out.dtype.type(2)
```

New text:

```
    out /= out.dtype.type(1)
```

### `u264.M6_any_release_measured`

_measured_zero_rule: treat a release not measured as measured, with the 1.0 rule

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M6_any_release_measured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 52 against a baseline of 52
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[0.11.0rc1-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[0.12.0.dev0-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[0.9.2-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[1.0.0rc0-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[1.0.1-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[1.1.0-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[2.0.0-None]`

Old text:

```
    return _MEASURED_MIX.get(version)
```

New text:

```
    return _MEASURED_MIX.get(version, True)
```

### `u114.M10_file_has_genre`

A row whose file carries a genre is offered a suggestion instead of being left to tag rows

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M10_file_has_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_row_whose_file_carries_a_genre_its_row_lacks_votes_with_the_files_word`
  - `tests/test_tag_suggest.py::test_a_row_with_a_genre_on_the_file_and_not_the_row_is_left_to_tag_rows`
  - `tests/test_tag_suggest.py::test_every_live_row_lands_in_exactly_one_outcome`
  - `tests/test_tag_suggest.py::test_the_gate_refuses_a_plan_that_changed`

Old text:

```
        if word:
            counts[FILE_HAS_GENRE] += 1
            # IT VOTES WITH ITS FILE'S WORD. The row lags its file, which is
            # what ``tag rows`` repairs, and the file is the newer of the two.
            live[track.content_id].genre = word
            continue

```

New text:

```
(empty)
```

### `u114.M11_file_word_votes`

A row whose file carries a genre its row lacks no longer votes with the file's word

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M11_file_word_votes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_row_whose_file_carries_a_genre_its_row_lacks_votes_with_the_files_word`

Old text:

```
            live[track.content_id].genre = word

```

New text:

```
(empty)
```

### `u114.M12_below_band`

The band threshold is ignored and every suggestion with a band is written

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M12_below_band`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_suggestion_below_the_band_is_offered_and_written_only_when_widened`

Old text:

```
        elif not _at_or_above(earned, band):
```

New text:

```
        elif not _at_or_above(earned, LOW):
```

### `u114.M13_band_order`

The band comparison is reversed, so a weaker band passes a stronger threshold

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M13_band_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_suggestion_below_the_band_is_offered_and_written_only_when_widened`

Old text:

```
    return BANDS.index(band) <= BANDS.index(least)
```

New text:

```
    return BANDS.index(band) >= BANDS.index(least)
```

### `u114.M14_genre_unknown`

A genre with no lookup row is planned as a write with an empty identifier

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M14_genre_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_declared_genre_the_library_has_no_lookup_row_for_is_left`

Old text:

```
                replace(item, action=LEAVE, reason=GENRE_UNKNOWN)
                if genre_id is None
                else replace(item, genre_id=genre_id)
```

New text:

```
                replace(item, genre_id=genre_id or "")
```

### `u114.M15_file_moved`

A file that carries a genre by the time the write reaches it is written over

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M15_file_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_file_given_a_genre_after_the_gate_is_left_and_named`

Old text:

```
        if word or outcome != rows.FILE_BLANK:
```

New text:

```
        if outcome == rows.FILE_UNREADABLE:
```

### `u114.M16_file_read_back`

A file is not read back after the write, so its row is written whatever the file holds

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M16_file_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_file_the_writer_says_it_wrote_and_that_does_not_read_back_leaves_its_row`

Old text:

```
        if rows._file_word(target)[0] != item.genre:
            wrong.append(item.content_id)
            continue

```

New text:

```
(empty)
```

### `u114.M17_rows_follow_files`

Every planned row is written, the ones whose file did not take the genre included

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M17_rows_follow_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_file_given_a_genre_after_the_gate_is_left_and_named`
  - `tests/test_tag_suggest.py::test_a_file_that_will_not_take_its_genre_leaves_its_row_and_the_rest_land`
  - `tests/test_tag_suggest.py::test_a_file_the_writer_says_it_wrote_and_that_does_not_read_back_leaves_its_row`

Old text:

```
        if item.content_id in wanted

```

New text:

```
(empty)
```

### `u114.M1_suggestable_routes_only`

suggestable accepts any word adoption routes, a keyword or catch all placement included, so Dance is suggested

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M1_suggestable_routes_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_catalogue_answer_outside_the_taxonomy_is_never_suggested`
  - `tests/test_tag_suggest.py::test_a_pick_outside_the_taxonomy_is_refused_before_any_row_is_read`
  - `tests/test_tag_suggest.py::test_a_tie_between_declared_genres_is_a_split_with_no_default`
  - `tests/test_tag_suggest.py::test_an_undeclared_word_lowers_the_agreement_and_is_never_suggested`
  - `tests/test_tag_suggest.py::test_only_a_genre_adoption_files_by_its_exact_name_is_suggestable`

Old text:

```
    return disposition is adopt_scan.Disposition.ROUTE and declared.named_folder(word) is not None
```

New text:

```
    return disposition is adopt_scan.Disposition.ROUTE
```

### `u114.M21_kept_days`

A kept catalogue answer lives five times as long

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M21_kept_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_kept_answer_is_reused_and_one_a_week_old_is_asked_again`

Old text:

```
    if not 0 <= age < CATALOGUE_DAYS:
```

New text:

```
    if not 0 <= age < CATALOGUE_DAYS * 5:
```

### `u114.M22_unread_day`

An unread answer is kept the whole week, so a later day never asks again

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M22_unread_day`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_an_answer_nobody_could_read_is_kept_for_the_day_only`

Old text:

```
    if answer.said == UNREAD and age != 0:
```

New text:

```
    if answer.said == UNREAD and age > CATALOGUE_DAYS:
```

### `u114.M23_breaker`

The walk stops asking after four unread rows in a row and not three

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M23_breaker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_three_rows_in_a_row_nobody_could_read_stop_the_walk_asking`

Old text:

```
            self.stopped = self._unread_running >= STOP_AFTER_UNREAD
```

New text:

```
            self.stopped = self._unread_running > STOP_AFTER_UNREAD
```

### `u114.M24_retry_unread`

A catalogue that could not be read is asked again, the behaviour before the review

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M24_retry_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_catalogue_that_cannot_be_read_is_this_rows_answer_and_is_not_asked_twice`
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
        if first.said != DECLINED or first.source_genre:
```

New text:

```
        if first.said == MATCHED or first.source_genre:
```

### `u114.M25_settled_not_asked`

A row held out or picked is looked up anyway

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M25_settled_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_row_held_out_or_picked_is_not_looked_up`

Old text:

```
        if catalogue is not None and not settled_by_person:
```

New text:

```
        if catalogue is not None:
```

### `u114.M2_high_share`

The high band's share bound drops from 0.8 to 0.7

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M2_high_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_the_band_is_the_share_over_enough_votes[7-10-medium]`

Old text:

```
((HIGH, 0.8, 6), (MEDIUM, 0.6, 3))
```

New text:

```
((HIGH, 0.7, 6), (MEDIUM, 0.6, 3))
```

### `u114.M3_high_votes`

The high band's least vote count halves from 6 to 3

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M3_high_votes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_the_band_is_the_share_over_enough_votes[3-3-medium]`
  - `tests/test_tag_suggest.py::test_the_band_is_the_share_over_enough_votes[5-5-medium]`

Old text:

```
((HIGH, 0.8, 6), (MEDIUM, 0.6, 3))
```

New text:

```
((HIGH, 0.8, 3), (MEDIUM, 0.6, 3))
```

### `u114.M4_split`

A two way tie at the top is no longer a split and the first tied genre becomes the default

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M4_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_folder_that_splits_evenly_offers_both_genres_and_no_default`
  - `tests/test_tag_suggest.py::test_a_person_picks_a_genre_for_a_split`
  - `tests/test_tag_suggest.py::test_a_tie_between_declared_genres_is_a_split_with_no_default`

Old text:

```
    if len(tied) > 1:
```

New text:

```
    if len(tied) > 2:
```

### `u114.M5_total_declared_only`

The total counts only declared votes, so an undeclared word no longer lowers the agreement

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M5_total_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_an_undeclared_word_lowers_the_agreement_and_is_never_suggested`

Old text:

```
    total = sum(votes.values())
```

New text:

```
    total = sum(weight for word, weight in votes.items() if suggestable(declared, word))
```

### `u114.M6_folder_weight`

A folder neighbour votes at the artist's weight

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M6_folder_weight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_the_artist_outweighs_the_folder`

Old text:

```
        weights[other] = FOLDER_WEIGHT
```

New text:

```
        weights[other] = ARTIST_WEIGHT
```

### `u114.M7_votes_once`

A neighbour by the artist in the same folder votes twice, its weights added

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M7_votes_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_neighbour_by_the_artist_in_the_same_folder_votes_once_at_the_artist_weight`

Old text:

```
        weights[other] = max(weights.get(other, 0), ARTIST_WEIGHT)
```

New text:

```
        weights[other] = weights.get(other, 0) + ARTIST_WEIGHT
```

### `u114.M9_catalogue_declared`

A catalogue answer is a vote whether or not the taxonomy declares it

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M9_catalogue_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_catalogue_answer_outside_the_taxonomy_is_never_suggested`

Old text:

```
        and suggestable(declared, asked.genre)

```

New text:

```
(empty)
```

### `u244.M03_kept_passed_over_reasked`

KeptCatalogue.answer: keep the day's answer that passed over Discogs after a token is recorded, round two's B2

- File: `src/cratekit/tagging/suggest.py`
- Source: `u244.json`, row `M03_kept_passed_over_reasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_kept_row_that_passed_over_discogs_is_asked_again_once_a_token_is_recorded`

Old text:

```
        if kept is not None and not self._askable_now(kept):
```

New text:

```
        if kept is not None:
```

### `u114.M19_write_intent`

The apply opens the database without write intent, so a running rekordbox is not refused by the opener

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u114.json`, row `M19_write_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_with_rekordbox_open_the_plan_is_read_and_no_file_is_written`

Old text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=False, cfg=cfg)
```

### `u114.M20_pick_declared`

A --set genre the taxonomy does not declare is accepted

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u114.json`, row `M20_pick_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_pick_outside_the_taxonomy_is_refused_before_any_row_is_read`

Old text:

```
        if not suggest.suggestable(declared, genre):
```

New text:

```
        if not genre.strip():
```

### `r796-c.V1_the_worker_hands_the_seam_over`

handle: stop passing the general catalogue's seam to tag_one, so the verb never asks it

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V1_the_worker_hands_the_seam_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`

Old text:

```
        published=published.for_taxonomy(declared),
```

New text:

```
        published=None,
```

### `r796-c.V2_blocked_warning_is_the_shops_only`

_unread_warnings: name every source blocked throughout, the general catalogue included, so one refusal is said under two codes

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V2_blocked_warning_is_the_shops_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`

Old text:

```
    for source in searchers.SOURCES:
        counted = answers.get(source) or {}
```

New text:

```
    for source in answers:
        counted = answers.get(source) or {}
```

### `r796-c.V3_some_unread_is_said`

_published_warnings: warn only when the catalogue was unread on every file asked about, so a partial block is counts and no sentence

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V3_some_unread_is_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`

Old text:

```
    if failed:
        seen = "; ".join(f"{word} on {count}" for word, count in unread.items() if count)
```

New text:

```
    if failed and failed == asked:
        seen = "; ".join(f"{word} on {count}" for word, count in unread.items() if count)
```

### `r796-c.V4_no_isrc_is_warned_about`

_published_warnings: never warn about files with no ISRC

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V4_no_isrc_is_warned_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`

Old text:

```
    if bare:
```

New text:

```
    if False:
```

### `r796-c.V5_parse_break_sentence_said_once`

_unread_warnings: read the general catalogue's parse break into the shops' sentence too

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V5_parse_break_sentence_said_once`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`

Old text:

```
            for source in searchers.SOURCES
        )
```

New text:

```
            for source in answers
        )
```

### `r796-a.L1_no_data_is_a_miss`

_error: stop reading the catalogue's 'no data' as a miss, so an ISRC it does not know is an error nobody recognises

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L1_no_data_is_a_miss`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 6 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_track_no_catalogue_knows_with_every_source_read_is_still_no_hit`
  - `tests/test_published_genre.py::test_a_track_whose_album_the_catalogue_does_not_list_is_not_a_miss`
  - `tests/test_published_genre.py::test_an_isrc_the_catalogue_does_not_know_is_a_miss_and_asks_for_no_album`
  - `tests/test_published_genre.py::test_the_request_names_this_tool_and_not_a_browser`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`

Old text:

```
    if code == _NO_DATA:
```

New text:

```
    if False:
```

### `r796-a.L2_quota_is_blocked`

_error: stop reading the quota error as a refusal, so a rate limit in a 200 body is a parse break

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L2_quota_is_blocked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 5 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_known_track_whose_album_could_not_be_read_is_unread_and_not_a_match[{"error": {"type": "Exception", "message": "Quota limit exceeded", "code": 4}}-blocked]`
  - `tests/test_published_genre.py::test_a_refusal_is_remembered_and_nothing_more_is_asked_in_the_run`
  - `tests/test_published_genre.py::test_a_refusal_on_one_file_reaches_the_next_files_seam`
  - `tests/test_published_genre.py::test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss[{"error": {"type": "Exception", "message": "Quota limit exceeded", "code": 4}}-blocked-Quota limit exceeded]`
  - `tests/test_published_genre.py::test_the_quota_error_is_not_retried_at_all`

Old text:

```
    if code == _QUOTA:
```

New text:

```
    if False:
```

### `r796-a.L3_unknown_error_is_not_a_miss`

_error: answer MISS for an error this reader does not know, the guess the module forbids

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L3_unknown_error_is_not_a_miss`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 2 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss[{"error": "a string"}-parse-break-does not know]`
  - `tests/test_published_genre.py::test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss[{"error": {"type": "InvalidQueryException", "message": "bad", "code": 600}}-parse-break-code 600]`

Old text:

```
    return _said(
        Answer.PARSE_BREAK,
        f"the catalogue answered with an error this reader does not know, {described}",
```

New text:

```
    return _said(
        Answer.MISS,
        f"the catalogue answered with an error this reader does not know, {described}",
```

### `r796-a.L4_refusal_check_on_a_200`

_read: run the refusal check only on a page with no text, so a challenge page served with 200 is parsed as JSON

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L4_refusal_check_on_a_200`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss[page2-blocked-bot check]`

Old text:

```
    refused = searchers.unread_outcome(SOURCE, page)
```

New text:

```
    refused = None if page.text is not None else searchers.unread_outcome(SOURCE, page)
```

### `r796-a.L5_answer_is_about_the_isrc_asked`

_ask: accept a track answer naming another ISRC, or none, as this track's

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L5_answer_is_about_the_isrc_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_an_answer_about_another_recording_is_not_read_as_this_tracks[track0]`
  - `tests/test_published_genre.py::test_an_answer_about_another_recording_is_not_read_as_this_tracks[track1]`
  - `tests/test_published_genre.py::test_an_answer_about_another_recording_is_not_read_as_this_tracks[track2]`

Old text:

```
    if isrc_token(track.get("isrc")) != isrc:
```

New text:

```
    if False:
```

### `r796-a.L6_album_id_is_a_positive_integer`

_ask: let any album identifier that is not None become a URL

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L6_album_id_is_a_positive_integer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 6 (killed)
- Killed:
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[-4]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[0]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[1/../../track/9]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[3.5]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[302127]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[True]`

Old text:

```
    if not isinstance(album_id, int) or isinstance(album_id, bool) or album_id <= 0:
```

New text:

```
    if album_id is None:
```

### `r796-a.L7_a_refusal_is_remembered`

genre_lookup: forget a BLOCKED answer, so the next file asks a catalogue that said stop

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L7_a_refusal_is_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 4 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_block_on_the_album_is_remembered_too`
  - `tests/test_published_genre.py::test_a_refusal_is_remembered_and_nothing_more_is_asked_in_the_run`
  - `tests/test_published_genre.py::test_a_refusal_on_one_file_reaches_the_next_files_seam`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`

Old text:

```
        if said.answer == Answer.BLOCKED.value:
            refusals.append(said)
```

New text:

```
        if False:
            refusals.append(said)
```

### `r796-a.L8_only_a_refusal_is_remembered`

genre_lookup: remember every unread answer, so one outage or parse break ends the catalogue's part in the run

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L8_only_a_refusal_is_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 4 (killed)
- Killed:
  - `tests/test_published_genre.py::test_an_album_that_could_not_be_read_is_asked_for_again`
  - `tests/test_published_genre.py::test_only_a_refusal_is_remembered[<html>not json</html>]`
  - `tests/test_published_genre.py::test_only_a_refusal_is_remembered[page0]`
  - `tests/test_published_genre.py::test_only_a_refusal_is_remembered[{"error": {"type": "Exception", "message": "Service busy", "code": 700}}]`

Old text:

```
        if said.answer == Answer.BLOCKED.value:
            refusals.append(said)
```

New text:

```
        if said.answer in UNREAD:
            refusals.append(said)
```

### `r796-b.O3_a_usable_answer_is_never_replaced`

second_opinion: ask the general catalogue about a hit that already has a genre (R4)

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O3_a_usable_answer_is_never_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 2 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_file_with_no_isrc_whose_genre_a_shop_settled_is_still_not_asked`
  - `tests/test_published_genre.py::test_a_usable_answer_is_never_replaced_and_the_record_says_not_asked`

Old text:

```
        if hit.genre or isrc is None:
```

New text:

```
        if isrc is None:
```

### `r796-b.O5_a_declined_beatport_match_is_asked_about`

_BEATPORT_ANSWERED: count only a miss, so a track Beatport calls by a catch-all is never asked about (R1, AE2)

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O5_a_declined_beatport_match_is_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 5 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_declined_answer_beside_beatports_own_declined_word_keeps_beatports`
  - `tests/test_published_genre.py::test_a_published_genre_over_beatports_declined_word_is_written_and_keeps_beatports_picture`
  - `tests/test_published_genre.py::test_ae2_two_coarse_answers_write_nothing_and_the_record_shows_both`
  - `tests/test_published_genre.py::test_beatports_picture_is_embedded_under_a_published_genre_and_says_whose_it_is`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`

Old text:

```
_BEATPORT_ANSWERED = (Answer.MATCHED.value, Answer.MISS.value)
```

New text:

```
_BEATPORT_ANSWERED = (Answer.MISS.value,)
```

### `r796-b.O6_unread_joins_the_unread_names`

second_opinion: leave the general catalogue out of the hit's unread names when it could not be read

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O6_unread_joins_the_unread_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 7 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_blocked_general_catalogue_leaves_the_file_untagged_and_askable`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[blocked]`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[parse-break]`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[unreachable]`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`

Old text:

```
            unread = (*hit.unread, SOURCE) if said.answer in UNREAD else hit.unread
```

New text:

```
            unread = hit.unread
```

### `r796-c.V6_one_lookup_per_process`

for_lookup: build a fresh lookup per call, so a refusal on one file is forgotten by the next file's seam

- File: `src/cratekit/tagging/published.py`
- Source: `r796-c.json`, row `V6_one_lookup_per_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_refusal_on_one_file_reaches_the_next_files_seam`
  - `tests/test_published_genre.py::test_the_lookup_binder_hands_back_one_lookup_per_process`
  - `tests/test_published_genre.py::test_the_suite_cannot_reach_the_live_catalogue_through_the_shared_lookup`

Old text:

```
    if not _shared:
        _shared.append(genre_lookup())
    return _shared[0]
```

New text:

```
    return genre_lookup()
```

### `r796-c.V7_the_request_names_this_tool`

genre_lookup: build the default fetch without this module's headers, so the API is asked under the browser identity

- File: `src/cratekit/tagging/published.py`
- Source: `r796-c.json`, row `V7_the_request_names_this_tool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_published_genre.py::test_the_request_names_this_tool_and_not_a_browser`

Old text:

```
    touch = searchers.default_fetch(sleep=naps, headers=HEADERS) if fetch is None else fetch
```

New text:

```
    touch = searchers.default_fetch(sleep=naps) if fetch is None else fetch
```

### `r796-d.L9_first_isrc_of_several_again`

re-measure of r796-a L9 after the second review round rewrote the line: _first_isrc never looks inside a value, so two ISRCs in one field read as no ISRC

- File: `src/cratekit/tagging/published.py`
- Source: `r796-d.json`, row `L9_first_isrc_of_several_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 9 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[CAT-0042,USRC17607839]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[ISRC: USRC17607839]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839 / GBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839 GBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839; GBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839\nGBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839\x00GBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[isrc US-RC1-76-07839 (remaster)]`
  - `tests/test_published_genre.py::test_the_two_value_id3_frame_is_the_shape_the_reader_really_hands_back`

Old text:

```
    for found in _ISRC_WITHIN.finditer(str(value or "")):
```

New text:

```
    for found in ():
```

### `r796-d.O7_a_decline_keeps_the_shops_word_again`

re-measure of r796-b O7 after the second review round rewrote the line: a declined answer always takes over the file's source, over Beatport's word and when it published no word at all

- File: `src/cratekit/tagging/published.py`
- Source: `r796-d.json`, row `O7_a_decline_keeps_the_shops_word_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_declined_answer_beside_beatports_own_declined_word_keeps_beatports`
  - `tests/test_published_genre.py::test_a_match_that_publishes_no_genre_is_a_decline_with_no_word`
  - `tests/test_published_genre.py::test_a_match_with_no_genre_leaves_the_file_as_the_shops_left_it`

Old text:

```
        if picked is None and (hit.source_genre or not word):
```

New text:

```
        if False:
```

### `r796-b.O9_no_isrc_is_not_no_hit`

tag_one: drop the no-isrc skip reason, so a file the general catalogue could not be asked about is no-hit (AE4)

- File: `src/cratekit/tagging/tag.py`
- Source: `r796-b.json`, row `O9_no_isrc_is_not_no_hit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_malformed_isrc_tag_is_reported_with_what_it_held`
  - `tests/test_published_genre.py::test_ae4_a_file_with_no_isrc_is_reported_as_that_and_not_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`

Old text:

```
        elif any(said.answer == NO_ISRC for said in hit.answers):
```

New text:

```
        elif False:
```

### `r1476.M10_no_name_slug_step`

_label_seam: drop the name slug step, so Some*Label no longer names Some Label

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M10_no_name_slug_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`

Old text:

```
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

New text:

```
            named = ()
```

### `r1476.M11_slug_step_beats_exact_name`

_label_seam: run the name slug step even when a label is called the tag exactly

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M11_slug_step_beats_exact_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`

Old text:

```
        if not named and wanted:
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

New text:

```
        if wanted:
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

### `r1476.M12_no_identifier_fallback`

_label_seam: drop the identifier step, so a renamed label's old name reaches nothing

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M12_no_identifier_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`

Old text:

```
            named = tuple(entry for entry in (held.labels.get(wanted),) if entry is not None)
```

New text:

```
            named = ()
```

### `r1476.M13_needles_not_held`

_frozen_labels: hold only the labels with a genre, so a lookup falls through to another label

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M13_needles_not_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
    for rows in (needles if isinstance(needles, Mapping) else {}, frozen):
```

New text:

```
    for rows in (frozen,):
```

### `r1476.M14_genre_join_by_name`

_frozen_labels: give each frozen label the genre of the first label with a genre sharing its name

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M14_genre_join_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
                    genre=genres.get(str(label_id)),
```

New text:

```
                    genre=next((genres[other] for other, them in frozen.items() if other in genres and isinstance(them, Mapping) and them.get("name") == row.get("name")), None),
```

### `r1476.M15_answer_without_genre`

_answered: answer a label with no genre as one

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M15_answer_without_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
    if entry is None or not entry.genre:
        return None
    return tag_engine.LabelAnswer
```

New text:

```
    if entry is None:
        return None
    return tag_engine.LabelAnswer
```

### `r1476.M16_unsluggable_raises`

_name_slug: let a name that could never be a label raise rather than read as none

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M16_unsluggable_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_tag_that_could_never_name_a_label_is_searched_and_never_fails`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`

Old text:

```
    except CratekitError:
        return ""


def _label_seam
```

New text:

```
    except CratekitError:
        raise


def _label_seam
```

### `r1476.M17_remedy_names_display_name`

_label_payload: the no genre remedy names the label by its display name

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M17_remedy_names_display_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_the_remedy_names_the_label_by_its_identifier`

Old text:

```
            handle = entry.label_id
```

New text:

```
            handle = entry.name
```

### `r1476.M18_remedy_head_never_shared`

_label_payload: never name the identifier beside a shared display name in the warning's head

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M18_remedy_head_never_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`

Old text:

```
            shared = len(held.named(entry.name)) > 1
```

New text:

```
            shared = False
```

### `r1476.M19_outranked_wording`

_label_warnings: the outranked warning no longer says a tag can name two labels

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M19_outranked_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`

Old text:

```
names two labels or "
```

New text:

```
names a retired label "
```

### `r1476.M1_identifier_not_frozen`

_label_payload: freeze the label's display name where its identifier goes, so the sweep answers --label by a name another label may share

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M1_identifier_not_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        frozen["label_id"] = entry.label_id
```

New text:

```
        frozen["label_id"] = entry.name
```

### `r1476.M2_folder_seam_by_name`

_folder_seam: look the folder's label up again by the name the engine hands it, the card's defect

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M2_folder_seam_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
        return _answered(held.labels.get(wanted))
```

New text:

```
        return _answered(held.by_name(_name) or held.labels.get(wanted))
```

### `r1476.M3_folder_seam_with_no_identifier`

_folder_seam: hand a seam for a job frozen with no identifier, so its --label answers nothing

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M3_folder_seam_with_no_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_frozen_with_no_identifier_reads_its_label_as_a_name`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`

Old text:

```
    if held is None or not wanted:
```

New text:

```
    if held is None:
```

### `r1476.M6_worker_hands_no_folder_seam`

handle: hand the engine no folder seam

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M6_worker_hands_no_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        folder_genre=_folder_seam(payload),
```

New text:

```
        folder_genre=None,
```

### `r1476.M7_worker_hands_identifier_as_label`

handle: hand the engine the frozen identifier as the folder's label text, round one's shape

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M7_worker_hands_identifier_as_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`

Old text:

```
        label=str(payload.get("label") or "") or None,
```

New text:

```
        label=str(payload.get("label_id") or "") or None,
```

### `r1476.M8_shared_name_takes_first`

_label_seam: a name two labels hold answers the first holder

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M8_shared_name_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
        return _answered(named[0]) if len(named) == 1 else None
```

New text:

```
        return _answered(named[0]) if named else None
```

### `r1476.M9_identifier_first`

_label_seam: read a tag as an identifier before a name, round one's blockers

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M9_identifier_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`

Old text:

```
        named = held.named(name)
        wanted = _name_slug(name)
```

New text:

```
        named = tuple(entry for entry in (held.labels.get(name),) if entry is not None) or held.named(name)
        wanted = _name_slug(name)
```

### `r1476.M4_engine_ignores_folder_seam`

_by_label: answer --label through the tag seam, never the folder seam

- File: `src/cratekit/tagging/tag.py`
- Source: `r1476.json`, row `M4_engine_ignores_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        return _Labelled((folder_genre or label_genre)(typed), own, NAMED_BY_FOLDER)
```

New text:

```
        return _Labelled(label_genre(typed), own, NAMED_BY_FOLDER)
```

