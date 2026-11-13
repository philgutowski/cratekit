# Mutation table: u280-pinned

Measured by `scripts/mutate.py` on 2026-11-13 04:55 UTC, branch `cloud/791-title-matcher-typed-fields` at `a7aa1822`. Pass kind: light.

Baseline: green, 20225 collected. pytest invocations for this batch: 6.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/8b75c8ef-f266-5e75-a31a-808c11d65ccb/scratchpad/mut/known.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 20225 against 20225. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `M06_marker_read_anywhere` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1210 | 1 | killed |
| `M11_ambiguity_featured_credits` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1210 | 1 | killed |
| `M29_marker_number_from_all_words` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1210 | 1 | killed |

## Row definitions

### `M06_marker_read_anywhere`

read_title: a square bracketed group is read past at any part, not only where the naming verb writes its marker

- File: `src/cratekit/tagging/titles.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1210 against a baseline of 1210
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-Bernard Badie - [Love] Is The Message-(Hate) Is The Message]`

Old text:

```
    found = _MARKER.match(text) if marker else None

```

New text:

```
    found = _MARKER.match(text)

```

### `M11_ambiguity_featured_credits`

_only_a_list_reads: a part naming the artist only as featured counts among several credits

- File: `src/cratekit/tagging/titles.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1210 against a baseline of 1210
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_what_the_whole_name_found_the_parse_still_reads[Bernard Badie & Tide-08A - 124 - Sunrise Mood (feat. Tide) - Bernard Badie - Vocal Mix-Sunrise Mood]`

Old text:

```
    if len(credits) > 1 and not all(_credits_before_featuring(parts[index], names) for index in credits):

```

New text:

```
    if False:

```

### `M29_marker_number_from_all_words`

read_title: past the marker a track number is decided from all remaining words, "[MP3] 01 - Artist - (Intro)" (round one's BLOCKING F1, as a row)

- File: `src/cratekit/tagging/titles.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1210 against a baseline of 1210
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-[MP3] 01 - Original Mix-Original Mix]`

Old text:

```
            numbered=_numbered(words(text[found.end() :].split(DASH)[0])),

```

New text:

```
            numbered=_numbered(words(text[found.end() :])),

```

