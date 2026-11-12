# Mutation table: r1534-composite

Measured by `scripts/mutate.py` on 2026-11-12 18:51 UTC, branch `cloud/713-title-strips-to-nothing` at `3a3209c3`. Pass kind: light.

Baseline: green, 19288 collected. pytest invocations for this batch: 4.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 19288 against 19288. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C1_m15_composite` | `src/cratekit/tagging/searchers.py` | user | 5 file(s) | 567 | 7 | killed |

## Row definitions

### `C1_m15_composite`

The composite for M15_beatport_title_noise in r1534.md, what it holds with exact_only: drop both the noise title refusal and the exact only refusal in _beatport_best, so a blank or punctuation title scores rows by containment

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`
- Collected: 567 against a baseline of 567
- Kills: 7 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_beatport_scores_no_row_for_a_title_with_no_letter_or_digit[   ]`
  - `tests/test_title_matcher.py::test_beatport_scores_no_row_for_a_title_with_no_letter_or_digit[( )]`
  - `tests/test_title_matcher.py::test_beatport_scores_no_row_for_a_title_with_no_letter_or_digit[()]`
  - `tests/test_title_matcher.py::test_beatport_scores_no_row_for_a_title_with_no_letter_or_digit[]`
  - `tests/test_title_matcher.py::test_beatport_writes_no_genre_off_another_track_by_the_artist[(Intro)-Intro Theme]`
  - `tests/test_title_matcher.py::test_beatport_writes_no_genre_off_another_track_by_the_artist[(Intro)-Introspection]`
  - `tests/test_title_matcher.py::test_beatport_writes_no_genre_off_another_track_by_the_artist[(Intro)-Sunrise Mood (Intro)]`

Old text:

```
    if not _identifies(title_normalized):
        return None
    bare_title, exact_only = _title_core(title_normalized)
    loose_title = _unbracketed(bare_title)
    searched = _artist_parts(artist, r"[,&]")

    best_score = 0
    best: _Pick | None = None
    for track in tracks:
        genre = _beatport_genre(track)
        if not genre:
            continue
        name = _normalized(track.get("track_name", ""))
        if not _identifies(name):
            continue
        name_core, _ = _title_core(name)
        mix = _normalized(track.get("mix_name", ""))
        credited = [_normalized(entry.get("artist_name", "")) for entry in track.get("artists", [])]
        credited = [other for other in credited if other]

        artist_score = 0
        for part in searched:
            if any(part == other or part in other or other in part for other in credited):
                artist_score += 1
        if artist_score == 0:
            continue

        if loose_title == _unbracketed(name) or title_normalized == f"{name} ({mix})":
            title_score = 3
        elif exact_only:
            continue

```

New text:

```
    bare_title, exact_only = _title_core(title_normalized)
    loose_title = _unbracketed(bare_title)
    searched = _artist_parts(artist, r"[,&]")

    best_score = 0
    best: _Pick | None = None
    for track in tracks:
        genre = _beatport_genre(track)
        if not genre:
            continue
        name = _normalized(track.get("track_name", ""))
        if not _identifies(name):
            continue
        name_core, _ = _title_core(name)
        mix = _normalized(track.get("mix_name", ""))
        credited = [_normalized(entry.get("artist_name", "")) for entry in track.get("artists", [])]
        credited = [other for other in credited if other]

        artist_score = 0
        for part in searched:
            if any(part == other or part in other or other in part for other in credited):
                artist_score += 1
        if artist_score == 0:
            continue

        if loose_title == _unbracketed(name) or title_normalized == f"{name} ({mix})":
            title_score = 3

```

