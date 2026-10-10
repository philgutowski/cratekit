# Mutation table: u117-operator

Measured by `scripts/mutate.py` on 2026-10-10 03:48 UTC, branch `HEAD` at `494b599`. Pass kind: light.

Baseline: green, 13017 collected. pytest invocations for this batch: 21.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/Library/Application Support/cratekit (365158 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 13017 against 13017. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `D1_heard_left_out` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `D2_unsettled_taken` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `D3_not_now_taken` | `src/cratekit/label/dated.py` | maintainer | 1 file(s) | 13017 | 0 (promoted) | zero |
| `D4_local_day` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 11 | killed |
| `D5_reuse_by_name` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 5 | killed |
| `D6_reuse_adds_only_missing` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 4 | killed |
| `D7_ambiguous` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `D8_age_bound` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 2 | killed |
| `D9_age_configured` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `D10_no_folder_refusal` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `D11_part_way_named` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 2 | killed |
| `D12_move_into_folder` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 8 | killed |
| `D13_config_validation` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 22 | 1 | killed |
| `D14_organize_call` | `src/cratekit/organize/account.py` | user | 2 file(s) | 54 | 3 | killed |
| `D15_playable_only` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `D16_recorded_before_move` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |

## Zero rows and what they owe

- `D3_not_now_taken` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `D1_heard_left_out`

plan: drop the heard check, so a release the record lists as heard is filed into the dated playlist again

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_heard_release_is_left_out_and_the_record_is_not_written`

Old text:

```
        if identity in gone:
```

New text:

```
        if False:
```

### `D2_unsettled_taken`

taken_by_goes: drop the settled check, so an answer no go has taken files its releases as downloaded

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unsettled_or_not_now_answer_took_nothing`

Old text:

```
        if not isinstance(settled, Mapping):
            continue
```

New text:

```
        if not isinstance(settled, Mapping):
            settled = {"at": "2026-10-09T12:00:00+00:00"}
```

### `D3_not_now_taken`

taken_by_goes: drop the taking answer check. Driven with the shape sync_cli writes, where a not now or stop answer records taken as an empty list, so this row is expected to kill nothing: the check is defence over a record no producer writes, a maintainer facing zero

- File: `src/cratekit/label/dated.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 13017 against a baseline of 13017
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if entry.get("answer") not in TAKING:
            continue
```

New text:

```
(empty)
```

### `D4_local_day`

_local_day: keep the recorded UTC day instead of the local one, so a go at 22:00 local west of UTC is filed under tomorrow; killed by the evening instant test

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_go_into_an_existing_year_makes_a_dated_playlist_and_leaves_the_year`
  - `tests/test_label_dated.py::test_a_go_on_another_day_makes_its_own_dated_playlist`
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_an_evening_go_west_of_utc_keeps_its_local_day`
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`
  - `tests/test_label_dated.py::test_the_go_day_is_the_local_day_of_the_settling`
  - `tests/test_label_dated.py::test_two_playlists_with_the_dated_name_are_left_alone`

Old text:

```
    if moment.tzinfo is not None:
        moment = moment.astimezone()
```

New text:

```
    if moment.tzinfo is not None:
        moment = moment
```

### `D5_reuse_by_name`

plan: never reuse a dated playlist by its name, so a second go the same day makes a second playlist

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`
  - `tests/test_label_dated.py::test_two_playlists_with_the_dated_name_are_left_alone`

Old text:

```
        matching = sorted(pid for pid, title in inside.items() if title == name)
```

New text:

```
        matching = []
```

### `D6_reuse_adds_only_missing`

plan: a reused dated playlist adds every track again rather than only the missing ones

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`

Old text:

```
                    add=tuple(one for one in tracks if one not in have),
```

New text:

```
                    add=tuple(tracks),
```

### `D7_ambiguous`

plan: two playlists with the dated name reuse the first instead of being left alone

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_two_playlists_with_the_dated_name_are_left_alone`

Old text:

```
        if len(matching) > 1:
```

New text:

```
        if len(matching) > 99:
```

### `D8_age_bound`

_aged: report at the age rather than past it, an off by one on the bound

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
        if days > limit:
```

New text:

```
        if days > limit * 2:
```

### `D9_age_configured`

plan: ignore the configured age and use the default

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
        aged=_aged(catalogue.name, inside, today, cfg.labels.new_playlist_age_days),
```

New text:

```
        aged=_aged(catalogue.name, inside, today, 30),
```

### `D10_no_folder_refusal`

apply: drop the missing folder refusal, so a dated playlist is made at the account root

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_label_with_no_folder_yet_refuses_the_apply_before_any_write`

Old text:

```
    if not folder_id:
        raise _no_folder(planned)
```

New text:

```
(empty)
```

### `D11_part_way_named`

apply: a failure part way is raised bare, without what was written

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`

Old text:

```
        raise _failed_part_way(exc, done, planned) from exc
```

New text:

```
        raise
```

### `D12_move_into_folder`

apply: a created dated playlist is not moved into the label's folder

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_go_into_an_existing_year_makes_a_dated_playlist_and_leaves_the_year`
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
                account.move_to_folder(remote_id, folder_id)
```

New text:

```
                pass
```

### `D13_config_validation`

config: accept a zero age

- File: `src/cratekit/core/config.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_the_age_key_defaults_to_thirty_and_refuses_zero`

Old text:

```
    if age is not None and (not isinstance(age, int) or isinstance(age, bool) or age < 1):
```

New text:

```
    if age is not None and (not isinstance(age, int) or isinstance(age, bool) or age < 0):
```

### `D14_organize_call`

organize: drop the one call line, so organize never plans a dated playlist

- File: `src/cratekit/organize/account.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 54 against a baseline of 54
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unreadable_record_refuses_the_dated_step_alone`
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`
  - `tests/test_label_dated.py::test_organize_with_nothing_taken_plans_nothing`

Old text:

```
        dated.add_step(cfg, area, entry, planned, remote_of)

```

New text:

```
        pass

```

### `D15_playable_only`

plan: take every track of a release, playable or not, so an unplayable track is planned on every run

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`

Old text:

```
        held.extend(one for one in tracks if one in playable and one not in held)
```

New text:

```
        held.extend(one for one in tracks if one not in held)
```

### `D16_recorded_before_move`

apply: record the created playlist only after the move, so a move refused after the create reports nothing written

- File: `src/cratekit/label/dated.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`

Old text:

```
                done.unplaced.append(step.name)
                account.move_to_folder(remote_id, folder_id)
```

New text:

```
                account.move_to_folder(remote_id, folder_id)
                done.unplaced.append(step.name)
```

