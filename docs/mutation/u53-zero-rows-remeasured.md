# Mutation table: u53-zero-rows-remeasured

Measured by `scripts/mutate.py` on 2026-09-10 14:04 UTC, branch `relay/71` at `58c3e5e`. Pass kind: light.

Baseline: green, 7140 collected. pytest invocations for this batch: 12.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7140 against 7140. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A2_abort_instead_of_not_apply` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 30 | 1 | killed |
| `I1_native_filter_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 30 | 1 | killed |
| `I6_tree_items_ignores_native` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 30 | 1 | killed |
| `I7_tree_items_ignores_the_named_tree` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 30 | 1 | killed |
| `E1_addressability_check_dropped` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 7140 | 0 (promoted) | zero |
| `E1c_composite_the_thing_it_guards` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 7140 | 0 (promoted) | zero |

## Zero rows and what they owe

- `E1_addressability_check_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `E1c_composite_the_thing_it_guards` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `A2_abort_instead_of_not_apply`

The branch tests for abort rather than for apply, so an option nobody classified acquires the write

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_gate_answer_this_verb_does_not_recognise_writes_nothing`

Old text:

```
    if option != "apply":
        return ctx.envelope(data=_plan(items, kind="inbox", applied=False), outcome=Outcome.NO_OP)
```

New text:

```
    if option == "abort":
        return ctx.envelope(data=_plan(items, kind="inbox", applied=False), outcome=Outcome.NO_OP)
```

### `I1_native_filter_dropped`

A resort queues an item for a tree still on the bridge, which no rebuild can write

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_queued_verb_takes_an_item_for_a_tree_still_on_the_bridge[resort]`

Old text:

```
    return tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
```

New text:

```
    return tuple(sorted(entries.tree_ids()))
```

### `I6_tree_items_ignores_native`

The rebuild's items include trees the registry says are still on the bridge

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_queued_verb_takes_an_item_for_a_tree_still_on_the_bridge[rebuild]`

Old text:

```
    native = tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
```

New text:

```
    native = tuple(sorted(entries.tree_ids()))
```

### `I7_tree_items_ignores_the_named_tree`

A rebuild of one named tree quietly rebuilds every tree in the library

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_rebuild_of_one_named_tree_queues_that_tree_alone`

Old text:

```
    if tree_id is None:
        return native
    return tuple(t for t in native if t == tree_id)
```

New text:

```
    return native
```

### `E1_addressability_check_dropped`

Two destinations sharing one display pair are merged rather than refused

- File: `src/cratekit/write/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.write.rebuild
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 7140 against a baseline of 7140
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    destinations = resolve_destinations(declared, placements, standing, record)
    assert_addressable(tree_id, destinations, standing)
```

New text:

```
    destinations = resolve_destinations(declared, placements, standing, record)
```

### `E1c_composite_the_thing_it_guards`

COMPOSITE for E1: the duplicate node refusal inside assert_addressable stops firing, which is one of the three shapes E1's call site exists to reach

- File: `src/cratekit/write/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.write.rebuild
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 7140 against a baseline of 7140
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        collided = by_node.get(node)
        if collided is not None:
```

New text:

```
        collided = by_node.get(node)
        if False:
```

