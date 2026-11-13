# Mutation table: r1646-composite

Measured by `scripts/mutate.py` on 2026-11-13 01:24 UTC, branch `cloud/788-artist-then-version-part` at `55c4745a`. Pass kind: light.

Baseline: green, 20131 collected. pytest invocations for this batch: 6.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/6be4e773-4f11-5e51-9ca2-872b2b21417c/scratchpad/mut/known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 20131 against 20131. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C1_m05_with_title_after_head` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 1116 | 11 | killed |
| `C2_title_after_head_alone` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 20131 | 0 (promoted) | zero |

## Zero rows and what they owe

- `C2_title_after_head_alone` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `C1_m05_with_title_after_head`

The composite for M05_shape_without_artist in r1646.md, what it holds behind the title start: the shape needs neither the artist's part nor a title after the head, so any title ending in a version, "Sunrise Mood Extended Mix", is read by its splits only

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1116 against a baseline of 1116
- Kills: 11 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_headed_file_title_matches_its_own_row[04A - 126 - Dub-Dub (Original Mix)]`
  - `tests/test_title_matcher.py::test_a_headed_file_title_matches_its_own_row[08A - 124 - Interlude-Interlude]`
  - `tests/test_title_matcher.py::test_a_title_matches_its_own_recording_either_way_round[Dub-Dub - 2014 Remaster]`
  - `tests/test_title_matcher.py::test_a_title_matches_its_own_recording_either_way_round[Radio - Radio Edit-Radio]`
  - `tests/test_title_matcher.py::test_beatport_still_matches_a_title_to_its_own_row[Radio - Radio Edit-Radio-Original Mix]`
  - `tests/test_title_matcher.py::test_discogs_still_matches_a_title_to_its_own_track[04A - 126 - Dub-Dub (Original Mix)]`
  - `tests/test_title_matcher.py::test_discogs_still_matches_a_title_to_its_own_track[08A - 124 - Interlude-Interlude]`
  - `tests/test_title_matcher.py::test_discogs_still_matches_a_title_to_its_own_track[Radio - Radio Edit-Radio]`
  - `tests/test_title_matcher.py::test_the_scraped_parsers_still_match_a_title_to_its_own_row[04A - 126 - Dub-Dub (Original Mix)]`
  - `tests/test_title_matcher.py::test_the_scraped_parsers_still_match_a_title_to_its_own_row[08A - 124 - Interlude-Interlude]`
  - `tests/test_title_matcher.py::test_the_scraped_parsers_still_match_a_title_to_its_own_row[Radio - Radio Edit-Radio]`

Old text:

```
        title > head
        and head in artists
        and not numbered
```

New text:

```
        True
        and not numbered
```

### `C2_title_after_head_alone`

The other half of C1: the shape keeps the artist's part but not a title after the head, so a self titled first part before nothing is the shape

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 20131 against a baseline of 20131
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        title > head
        and head in artists
        and not numbered
```

New text:

```
        head in artists
        and not numbered
```

