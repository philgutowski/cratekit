# Mutation table: r1636-composite

Measured by `scripts/mutate.py` on 2026-11-12 22:52 UTC, branch `cloud/781-a-file-s-dash-part-that-is-not-its-title` at `572361ec`. Pass kind: light.

Baseline: green, 20010 collected. pytest invocations for this batch: 7.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/47b879e7-8759-567f-ab92-aa4b06c609d8/scratchpad/known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 20010 against 20010. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C1_m08_with_m02` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 1029 | 10 | killed |
| `C2_m09_with_tempo_flag` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 1029 | 2 | killed |
| `C3_tempo_flag_alone` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 20010 | 0 (promoted) | zero |

## Zero rows and what they owe

- `C3_tempo_flag_alone` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `C1_m08_with_m02`

The composite for M08_numbered_later_part_an_artist in r1636.md, what it holds behind the credit test: a later part opening with a track number may be the artist AND a part credits the artist when it merely holds one of the names (M02), so "Album - 02 Artist" may take the artist for its credit

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1029 against a baseline of 1029
- Kills: 10 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Bernard Badie-08A - 124 - Bernard Badie Theme - Pt. 2-Bernard Badie Theme (Pt. 2)-Pt. 2]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Bernard Badie-08A - 124 - Bernard Badie Theme - Vocal Mix-Bernard Badie Theme-Vocal Mix]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Bernard Badie-Bernard Badie - Bernard Badie Theme-Bernard Badie Theme-Bernard Badie]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Tide-08A - 124 - Riding The Tide - Intro-Riding The Tide (Intro)-Intro]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Tide-08A - 124 - Riding The Tide - Part 2-Riding The Tide (Part 2)-Part 2]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Tide-08A - 124 - Riding The Tide - Vocal Mix-Riding The Tide-Vocal Mix]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Tide-Tide - Riding The Tide-Riding The Tide-Tide]`
  - `tests/test_title_matcher.py::test_round_two_no_genre_is_written_off_another_recording[Tide-08A - 124 - Riding The Tide - Vocal Mix-Vocal Mix]`
  - `tests/test_title_matcher.py::test_what_is_not_the_artists_credit_is_never_passed_over[Bernard Badie-08A - 124 - Love And Bernard Badie - Sun Path-Sun Path]`
  - `tests/test_title_matcher.py::test_what_is_not_the_artists_credit_is_never_passed_over[Bernard Badie-Bernard Badie - Dancing With Bernard Badie-Bernard Badie]`

Old text:

```
    elif _numbered(words):
        return False
    folded = tuple(_folded(word) for word in _words(text))
    if names & _credited_names(text):
```

New text:

```
    elif False:
        return False
    folded = tuple(_folded(word) for word in _words(text))
    if any(_runs_in(name, folded) for name in names):
```

### `C2_m09_with_tempo_flag`

The composite for M09_head_unbounded in r1636.md, what it holds behind the one key one tempo flags: the head runs to the title's last part AND any number may follow as a tempo, so a title of numbers after a head is eaten

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1029 against a baseline of 1029
- Kills: 2 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Bernard Badie-08A - 124 - 007 - Original Mix-007-Original Mix]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Bernard Badie-08A - 124 - 05 - Original Mix-05-Original Mix]`

Old text:

```
    while end < min(2, len(parts) - 1):
        words = _words(parts[end])
        if len(words) != 1:
            break
        if naming.is_camelot(words[0]) and not keys:
            keys = True
        elif not tempos and (_a_tempo(words[0]) if not keys else words[0].isdecimal()):
```

New text:

```
    while end < len(parts) - 1:
        words = _words(parts[end])
        if len(words) != 1:
            break
        if naming.is_camelot(words[0]) and not keys:
            keys = True
        elif (_a_tempo(words[0]) if not keys else words[0].isdecimal()):
```

### `C3_tempo_flag_alone`

The pair for C2: any number may follow as a tempo, with the head still bounded to two parts, to show what the bound adds

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 20010 against a baseline of 20010
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        elif not tempos and (_a_tempo(words[0]) if not keys else words[0].isdecimal()):
```

New text:

```
        elif (_a_tempo(words[0]) if not keys else words[0].isdecimal()):
```

