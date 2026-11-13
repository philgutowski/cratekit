# Mutation table: u284-composite

Measured by `scripts/mutate.py` on 2026-11-13 19:38 UTC, branch `cloud/790-sync-lands-with-discogs-only` at `6b712c24`. Pass kind: light.

Baseline: green, 20503 collected. pytest invocations for this batch: 4.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 20503 against 20503. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C3x_unread_discogs_and_outage_named` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |

## Row definitions

### `C3x_unread_discogs_and_outage_named`

tagging.cli._refused_out: the composite for C3's zero, both the Discogs was read guard and the every other catalogue refused guard removed, so any file left with no genre is named as one the catalogues refused

- File: `src/cratekit/tagging/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_pass_whose_catalogues_answered_says_nothing_of_refusals`
  - `tests/test_sync_refused.py::test_a_sweep_beatport_never_refused_names_nothing`

Old text:

```
    if said.get(searchers.DISCOGS) not in (searchers.Answer.MISS.value, searchers.Answer.MATCHED.value):
        return ()
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others or any(said[source] != searchers.Answer.BLOCKED.value for source in others):
        return ()
```

New text:

```
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others:
        return ()
```

