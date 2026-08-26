# Mutation table: u43-author-round-2

Measured by `scripts/mutate.py` on 2026-08-26 21:13 UTC, branch `unit/u43-the-setbuild-command-line-shell-row-29` at `d285a46`. Pass kind: light.

Baseline: green, 6355 collected. pytest invocations for this batch: 14.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6355 against 6355. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `N0_null_control` | `src/cratekit/setbuilder/cli.py` | maintainer | 1 file(s) | 6355 | 0 (promoted) | zero |
| `A2_no_resolved_second_pass` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `P2_items_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `P6_count_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `H2_empty_is_a_no_op` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `H3_missing_root_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `H4_template_loses_the_marker` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `V1_pool_total_is_the_union` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `V2_marker_position_moved` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `V3_root_check_reports_instead_of_refusing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 34 | 1 | killed |

## Zero rows and what they owe

- `N0_null_control` (maintainer facing): maintainer facing, composite not required

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `D5_rerun_the_eighteen_killed_rows`: Re-measure round one's eighteen killing rows Dropped because: Not re-run on purpose. METHOD scopes a round to its own diff, and round two's diff is six guards and one totals field. A killing row does not become less killing because a guard was added beside it, and re-running eighteen of them would spend the whole light-pass cap on numbers already measured. The cap is 25 and this round uses 10.
- `D6_independent_pass`: An independent verifier's own table over this unit Dropped because: NOT RUN, AND THIS IS THE GAP IN THIS UNIT'S VERIFICATION RATHER THAN A ROW THAT DID NOT FIT. METHOD asks a light pass to be run by an agent that did not write the code, and this session was instructed not to spawn one. Both tables here are the author's. The measured gaps between an author's table and an independent one on this project are 10 against 17, 39 against 49 and 49 against 83, so every zero below reads as 'the author could not kill it' and never as 'nothing can'.

## Row definitions

### `N0_null_control`

A comment reworded and nothing else. Must kill zero, or the baseline is red and every number below it is noise.

- File: `src/cratekit/setbuilder/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 6355 against a baseline of 6355
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
Layer: modules.
```

New text:

```
Layer: the modules layer.
```

### `A2_no_resolved_second_pass`

ROUND ONE: zero. Drop the resolved second pass in anchor_in_index, so a path spelled through a symlink or a different absolute form never matches

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_spelled_through_a_symlink_still_resolves`

Old text:

```
    try:
        resolved = path.resolve()
    except OSError:
        return None
    for track in index:
        if not track.path:
            continue
        try:
            if Path(track.path).resolve() == resolved:
                return track
        except OSError:
            continue
    return None
```

New text:

```
    return None
```

### `P2_items_absent_from_digest`

ROUND ONE: zero. The digest stops covering the items, so two entirely different sets of recommendations for one anchor carry one identity

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_two_plans_over_the_same_anchor_and_different_companions_digest_apart`

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"]}),
```

### `P6_count_ignored`

ROUND ONE: zero. The count flag is dropped on the way to the engine, so the pool is always the default eight

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=None, role=role)
```

### `H2_empty_is_a_no_op`

ROUND ONE: zero. A plan with no companions reports NO_OP rather than OK, which tells a consumer nothing happened when the question was answered

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`

Old text:

```
    return ctx.envelope(data=plan, outcome=Outcome.OK)
```

New text:

```
    return ctx.envelope(
        data=plan, outcome=Outcome.OK if plan["items"] else Outcome.NO_OP
    )
```

### `H3_missing_root_not_refused`

ROUND ONE: zero. The configured library root is no longer checked before the scan, so an unmounted volume scans zero files and every anchor comes back unindexed

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if root.is_dir() and False:
```

### `H4_template_loses_the_marker`

ROUND ONE: zero. The name template stops declaring the lossy marker, so a marked file's clean title keeps the marker and its match key gains a token

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`

Old text:

```
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))
```

New text:

```
    return NameTemplate()
```

### `V1_pool_total_is_the_union`

totals reports the union size where it says pool, which is the wrong number and the one a reader would otherwise have to derive. The round-one arithmetic surprise is exactly this confusion, so the new count guard owes a death here

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`

Old text:

```
        "pool": len(plan.pool),
```

New text:

```
        "pool": len(items),
```

### `V2_marker_position_moved`

The marker rule is declared with a separator that puts it somewhere the head parser does not strip. If the lossy guard passes this, its fixture is in a position where the declaration cannot matter, which is the mistake the first attempt at it made

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`

Old text:

```
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))
```

New text:

```
    return NameTemplate(markers=(MarkerRule(field="lossy", literal="[NOTAMARKER]"),))
```

### `V3_root_check_reports_instead_of_refusing`

The missing root produces an empty plan and an OK exit rather than a refusal, which is the clean-report-over-unreadable-state shape rather than the crash shape. A guard that only catches the crash is not the guard this row needs

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
        raise refuse(
```

New text:

```
    if not root.is_dir():
        return ctx.envelope(
            data=plan_for(
                setbuilder.Track(
                    artist="", title="", key="", bpm=None, genre="",
                    energy=None, vox=None, voxgender=None, match="",
                ),
                (),
                declared=taxonomy.default_taxonomy(),
            ),
            outcome=Outcome.OK,
        )
    if False:
        raise refuse(
```

