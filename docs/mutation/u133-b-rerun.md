# Mutation table: u133-b-rerun

Measured by `scripts/mutate.py` on 2026-10-13 02:25 UTC, branch `fable/308-jazz-genre-folder-under` at `aeaa5a10`. Pass kind: light.

Baseline: green, 13745 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/Library/Application Support/cratekit (408201 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 13745 against 13745. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `T6_former_sub` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 991 | 1 | killed |
| `E2_former_place_only` | `src/cratekit/adopt/move.py` | user | 4 file(s) | 242 | 10 | killed |

## Row definitions

### `T6_former_sub`

The former place records the old playlist under another sub identifier

- File: `src/cratekit/templates/taxonomy.default.toml`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy.py`
- Collected: 991 against a baseline of 991
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_the_old_playlist_is_found_under_the_identifier_it_was_recorded_by`

Old text:

```
bucket = "non_electronic"
sub = "jazz"

```

New text:

```
bucket = "non_electronic"
sub = "jazz_style"

```

### `E2_former_place_only`

Existing guard sample: a track sitting only in a former place is never recognised as one

- File: `src/cratekit/adopt/move.py`
- Surface: user
- Subset: test files importing cratekit.adopt.move
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 242 against a baseline of 242
- Kills: 10 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_file_the_census_could_not_read_is_listed_under_no_reading`
  - `tests/test_adopt_former_place.py::test_a_genre_only_the_fallback_tier_lands_is_not_read_as_naming_the_bucket`
  - `tests/test_adopt_former_place.py::test_a_second_run_after_the_move_plans_nothing_and_writes_nothing`
  - `tests/test_adopt_former_place.py::test_a_track_a_verdict_withheld_is_listed_under_the_verdict`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_that_neither_bucket_claims_is_listed_once[another-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_that_neither_bucket_claims_is_listed_once[no-genre]`
  - `tests/test_adopt_former_place.py::test_a_verdict_on_the_holding_bucket_is_the_reason_a_track_there_is_left`
  - `tests/test_adopt_former_place.py::test_an_unreadable_file_whose_genre_names_the_old_folder_is_listed_under_no_reading`
  - `tests/test_adopt_former_place.py::test_the_digest_moves_when_a_track_turns_up_in_the_old_playlist`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`

Old text:

```
    return bool(held) and set(held) <= former

```

New text:

```
    return False

```

