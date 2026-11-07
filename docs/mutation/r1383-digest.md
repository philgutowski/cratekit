# Mutation table: r1383-digest

Measured by `scripts/mutate.py` on 2026-11-07 04:11 UTC, branch `cloud/599-a-landing-record-the-session-log` at `818cbf25`. Pass kind: light.

Baseline: green, 17287 collected. pytest invocations for this batch: 5.

Known failures: 161 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 17287 against 17287. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `M8_digest_drops_hold` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 145 | 1 | killed |
| `M9_digest_always_keyed` | `src/cratekit/sync/pair_cli.py` | maintainer | 5 file(s) | 145 | 1 | killed |

## Row definitions

### `M8_digest_drops_hold`

PairPlan.identity: leave the held tracks out of the digest, so a plan whose hold moved is not stale at its gate

- File: `src/cratekit/sync/pair_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_the_pairs_digest_moves_with_the_landing_hold_and_only_when_any`

Old text:

```
                {"landing_unread": sorted(named.remote_id for named in self.landing_unread)}
                if self.landing_unread
                else {}
```

New text:

```
                {}
```

### `M9_digest_always_keyed`

PairPlan.identity: put the key in every digest, so a plan reading every record no longer digests as it did (round one's zero)

- File: `src/cratekit/sync/pair_cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_the_pairs_digest_moves_with_the_landing_hold_and_only_when_any`

Old text:

```
                if self.landing_unread
                else {}
```

New text:

```
                if True
                else {}
```

