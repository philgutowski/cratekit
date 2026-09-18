# Mutation table: r368-round-2

Measured by `scripts/mutate.py` on 2026-09-18 17:42 UTC, branch `relay/101` at `6dd3302`. Pass kind: light.

Baseline: green, 7651 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7651 against 7651. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `G6_ancestors_not_walked` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `G14_the_destination_check_is_equality_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `R1_the_live_root_refusal_is_reworded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `G7_target_not_resolved` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `G7_composite` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 53 | 1 | killed |

## Row definitions

### `G6_ancestors_not_walked`

re-measured: ask samefile of the candidate alone, so a differently cased ancestor is missed

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_differently_cased_ancestor_still_puts_the_target_inside_the_library`

Old text:

```
    return any(_same_place(ancestor, root) for ancestor in (place, *place.parents))

```

New text:

```
    return _same_place(place, root)

```

### `G14_the_destination_check_is_equality_only`

re-measured: drop the name-plus-parent half, so a landing path that is not on disk yet passes

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_that_is_not_on_disk_yet_is_still_the_live_database`

Old text:

```
    if _same_place(landing, live) or (
        landing.name == live.name and _same_place(landing.parent, live.parent)
    ):

```

New text:

```
    if _same_place(landing, live):

```

### `R1_the_live_root_refusal_is_reworded`

re-measured: reword the destination refusal rather than appending to it

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_whose_database_lands_on_the_live_one_is_refused`

Old text:

```
            f"the database would land on {landing}, which is this library's live "
            f"database; the target is outside the library root and the database "
            f"is too, so naming its directory restores over it in place",

```

New text:

```
            f"the chosen folder resolves to somewhere this installation already "
            f"reads from, so the copy would replace what is there",

```

### `G7_target_not_resolved`

re-measured: compare the raw argument, leaving samefile to answer for a relative spelling

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_relative_target_is_compared_as_the_place_it_names`

Old text:

```
    resolved = Path(raw).expanduser().resolve()

```

New text:

```
    resolved = Path(raw).expanduser()

```

### `G7_composite`

what the resolution does hold now that samefile answers the comparison: report the word somebody typed rather than the directory it named

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Composite for: `G7_target_not_resolved`
- Killed:
  - `tests/test_restore_cli.py::test_a_relative_target_is_compared_as_the_place_it_names`

Old text:

```
            target=str(resolved),
            library_root=str(root),

```

New text:

```
            target=str(raw),
            library_root=str(root),

```

