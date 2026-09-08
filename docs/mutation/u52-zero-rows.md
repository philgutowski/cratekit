# Mutation table: u52-zero-rows

Measured by `scripts/mutate.py` on 2026-09-08 01:34 UTC, branch `relay/70` at `cb5dba7`. Pass kind: full.

Baseline: green, 6852 collected. pytest invocations for this batch: 13.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6852 against 6852. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `I4_registry_empty_message` | `src/cratekit/label/cli.py` | user | 2 file(s) | 82 | 1 | killed |
| `S4_and_shortfall_conjunct_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 82 | 1 | killed |
| `L5_artist_for_missing_returns_none` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 99 | 1 | killed |
| `L6_verifier_missing_returns_stub` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 99 | 1 | killed |
| `L8_verifier_passthrough_gone` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 99 | 1 | killed |
| `R3_closed_cause_narrowed_to_failed` | `src/cratekit/label/cli.py` | user | 2 file(s) | 82 | 1 | killed |
| `H5_verifier_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 82 | 1 | killed |
| `P1_revoked_tombstones_suppress` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 99 | 1 | killed |
| `P2_snapshot_read_eagerly` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 99 | 1 | killed |

## Row definitions

### `I4_registry_empty_message`

Reword the label-registry-empty sentence, never append to it, because the suite asserts with in

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_the_empty_registry_refusal_says_that_no_label_is_registered`

Old text:

```
        "no favourite label is registered, so a sweep would queue a job with "
        "nothing to claim and would then report that it succeeded",
```

New text:

```
        "the favourite label list holds nothing, so this sweep has no work in "
        "it and would finish by claiming a result it never produced",
```

### `S4_and_shortfall_conjunct_gone`

MUTATE THE AND, second arm: drop the shortfall conjunct, so a sweep that offered plenty and dropped one release refuses

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_that_confirmed_some_of_what_it_read_succeeds_and_offers_those`

Old text:

```
    if result.shortfall == "empty" and source.dropped:
```

New text:

```
    if source.dropped:
```

### `L5_artist_for_missing_returns_none`

The bare skip R-135 named in miniature: a label with no catalogue object at all returns None rather than refusing

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_missing_artist_refusal_names_the_missing_object_not_the_listing`

Old text:

```
        raise run.LookupFailure(
            f"no catalogue object was available for the registered label "
            f"{entry.name!r}, so its releases were never listed; that is not "
            f"a label with nothing new"
        )
```

New text:

```
        return None
```

### `L6_verifier_missing_returns_stub`

A source built with neither verifier nor catalogue confirms nothing instead of refusing, so every release is dropped as unconfirmed

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_source_with_neither_verifier_nor_catalogue_refuses_rather_than_confirming_nothing`

Old text:

```
        raise run.LookupFailure(
            "this labels source was built with neither a verification callable "
            "nor a catalogue, so no release it listed could be confirmed"
        )
```

New text:

```
        def unconfirmed(claimed: str, release: Any) -> Mapping[str, Any]:
            return {}

        return unconfirmed
```

### `L8_verifier_passthrough_gone`

REMOVE THE LAYER ALONE: an adapter's credential-missing refusal is flattened into this source could not list

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason`

Old text:

```
                except CratekitError:
                    raise
                except Exception as exc:
```

New text:

```
                except Exception as exc:
```

### `R3_closed_cause_narrowed_to_failed`

Narrow the predicate back to FAILED alone, which exits 0 over a CANCELLED job with 0 of 3 items done

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_resume_of_a_cancelled_sweep_does_not_exit_ok_over_the_items_it_never_ran`

Old text:

```
        if not job.is_open() and job.cause is not None:
```

New text:

```
        if job.state is jobs.JobState.FAILED and job.cause is not None:
```

### `H5_verifier_passthrough_gone`

REMOVE THE LAYER ALONE: the verification boundary swallows an adapter's own refusal into label-playlist-unreadable

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason`

Old text:

```
        except CratekitError:
            raise
        except Exception as exc:
```

New text:

```
        except Exception as exc:
```

### `P1_revoked_tombstones_suppress`

Snapshot revoked tombstones too, so a lifted suppression silently keeps a release out of the review queue

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_revoked_tombstone_no_longer_keeps_a_release_out_of_the_queue`

Old text:

```
            snapshot = {record.suppression_id for record in store.suppressions()}
```

New text:

```
            snapshot = {
                record.suppression_id
                for record in store.suppressions(include_revoked=True)
            }
```

### `P2_snapshot_read_eagerly`

THE LAZY READ: take the snapshot when the reader is built, which fires the unreadable store refusal on a label that has no confirmed release to ask about

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_unreadable_tombstone_store_does_not_fail_a_label_with_nothing_to_ask`

Old text:

```
    snapshot: set[str] | None = None
```

New text:

```
    snapshot: set[str] | None = {
        record.suppression_id
        for record in DecisionStore(tombstone.STORE_KEY, cfg).suppressions()
    }
```

