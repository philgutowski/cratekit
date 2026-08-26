# Mutation table: u43-author-light

Measured by `scripts/mutate.py` on 2026-08-26 20:18 UTC, branch `unit/u43-the-setbuild-command-line-shell-row-29` at `17b758d`. Pass kind: light.

Baseline: green, 6351 collected. pytest invocations for this batch: 38.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6351 against 6351. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `N0_null_control` | `src/cratekit/setbuilder/cli.py` | maintainer | 1 file(s) | 6351 | 0 (promoted) | zero |
| `A1_first_track_wins` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 3 | killed |
| `A2_no_resolved_second_pass` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 6351 | 0 (promoted) | zero |
| `A3_containment_not_checked` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 2 | killed |
| `A4_empty_anchor_defaults` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 2 | killed |
| `C1_no_lower_bound` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 4 | killed |
| `C2_bound_off_by_one` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 2 | killed |
| `P1_anchor_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 1 | killed |
| `P2_items_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 6351 | 0 (promoted) | zero |
| `P3_pool_leads_the_items` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 1 | killed |
| `P4_no_positions_at_all` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 3 | killed |
| `P5_role_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 2 | killed |
| `P6_count_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 6351 | 0 (promoted) | zero |
| `P7_vox_threshold_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 1 | killed |
| `P8_anchor_not_owned` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 6 | killed |
| `P9_totals_lose_the_anchor` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 3 | killed |
| `H1_the_cache_is_written` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 30 | 1 | killed |
| `H2_empty_is_a_no_op` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 6351 | 0 (promoted) | zero |
| `H3_missing_root_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 6351 | 0 (promoted) | zero |
| `H4_template_loses_the_marker` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 6351 | 0 (promoted) | zero |
| `R1_marker_restored` | `src/cratekit/cli/registry.py` | maintainer | 21 file(s) | 2903 | collection error | collect-error |
| `R2_undeclared_refusal_slug` | `src/cratekit/core/cause.py` | user | 31 file(s) | 3738 | 3 | killed |
| `E1_anchor_is_its_own_companion` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 155 | 5 | killed |
| `E2_tempo_band_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 155 | 1 | killed |
| `E3_tempo_serialized_as_bpm` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 155 | 3 | killed |

## Zero rows and what they owe

- `N0_null_control` (maintainer facing): maintainer facing, composite not required
- `A2_no_resolved_second_pass` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `P2_items_absent_from_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `P6_count_ignored` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `H2_empty_is_a_no_op` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `H3_missing_root_not_refused` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `H4_template_loses_the_marker` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `A5_relative_against_the_process`: A relative anchor is taken against the working directory instead of the library root Dropped because: THE TWENTY-SIXTH ROW, cut to the light pass cap, and cut on information value rather than on importance. It is a certain kill: test_a_relative_anchor_is_taken_against_the_library_and_not_the_process asserts exactly that resolution, was written in the same sitting as the guard, and would have reported a number nobody could be surprised by. The rows kept in its place are ones whose outcome was genuinely unknown, P2 above especially.
- `D1_find_in_index_threshold`: Lower MATCH_THRESHOLD in the engine's fuzzy anchor lookup Dropped because: RANKED BELOW THE CAP BECAUSE NOTHING IN src REACHES IT. find_in_index is called only from resolve_anchor, which is called only from build_set, and no module under src calls either: this shell resolves by path. A row here would measure the engine's own suite and say nothing about the shipped verb. The mis-resolution it would probe is filed as a residual with its reachability stated.
- `D2_energy_order_unknown_first`: Sort unknown energy first rather than last in _energy_order Dropped because: Ranked below the cap: same guard family as E1 and E2, which are measured, and the sequence-ordering property it touches is already exercised by P3 and P4 from the shell's side. A light pass caps at 25 and this was the twenty-sixth.
- `D3_weights_do_not_sum`: Move a Weights coefficient so the five no longer sum to one Dropped because: Ranked below the cap: Weights.__post_init__ raises on construction, so the mutation is a collect error rather than a death, and mutate.py would report drift instead of a number. The coefficient-mutation rule METHOD asks for is served by C2 instead, which moves a bound by one rather than removing it.
- `D4_second_template_copy`: Change the lossy marker literal in write/naming_cli.py rather than in this shell Dropped because: Ranked below the cap and it belongs to a different unit. H4 measures this shell's own copy. That six sites in src construct the same template independently is filed as a residual rather than measured here, because a row proving the sixth copy drifts would be a row about naming_cli's guards.

## Row definitions

### `N0_null_control`

A comment reworded and nothing else. Must kill zero, or the baseline is red and every number below it is noise.

- File: `src/cratekit/setbuilder/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 6351 against a baseline of 6351
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

### `A1_first_track_wins`

anchor_in_index returns the first indexed track instead of the one at the path, which is exactly what the fuzzy lookup this design replaces does when a version suffix is present

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_is_not_in_the_library_refuses_with_a_vocabulary_code`
  - `tests/test_setbuilder_cli.py::test_an_anchor_the_index_does_not_hold_is_absent_rather_than_approximated`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_found_by_path_and_never_by_title`

Old text:

```
    wanted = str(path)
    for track in index:
        if track.path == wanted:
            return track
```

New text:

```
    wanted = str(path)
    for track in index:
        if track.path or wanted:
            return track
```

### `A2_no_resolved_second_pass`

Drop the resolved second pass in anchor_in_index, so a path spelled through a symlink or a different absolute form never matches

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 6351 against a baseline of 6351
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `A3_containment_not_checked`

anchor_path stops checking that the anchor is inside the library, so a path walking out with .. is scanned for and refused as unindexed rather than refused as outside

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_walks_out_of_the_library_is_refused`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if _within(candidate, root) and False:
```

### `A4_empty_anchor_defaults`

anchor_path stops refusing an empty anchor, which turns it into the library root and asks the index for a directory

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_is_refused_rather_than_defaulted`
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_refuses_through_the_dispatcher`

Old text:

```
    if not anchor:
        raise refuse(
```

New text:

```
    if anchor and not anchor:
        raise refuse(
```

### `C1_no_lower_bound`

positive_count stops refusing zero and negatives, so build_plan's pool[: count or DEFAULT_POOL] silently turns 0 into 8 and -1 into a dropped last companion

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[-1]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[-8]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[0]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`

Old text:

```
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive count")
    return value
```

New text:

```
    return int(text)
```

### `C2_bound_off_by_one`

The bound is loosened by one rather than removed, so zero passes and negatives do not. A guard whose constant can be moved without a death is a guard that pins nothing.

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[0]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`

Old text:

```
    if value < 1:
```

New text:

```
    if value < 0:
```

### `P1_anchor_absent_from_digest`

The digest stops covering the anchor, so two plans over the same companions and different anchors are indistinguishable

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "items": items}),
```

### `P2_items_absent_from_digest`

The digest stops covering the items, so a plan and a completely different plan over the same anchor digest identically

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 6351 against a baseline of 6351
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"]}),
```

### `P3_pool_leads_the_items`

The pool leads and the sequence follows, so the recommendation is no longer at the top of the array a consumer reads

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
    ordered = list(plan.sequence) + [s for s in plan.pool if id(s) not in placed]
```

New text:

```
    ordered = [s for s in plan.pool if id(s) not in placed] + list(plan.sequence)
```

### `P4_no_positions_at_all`

Every item reports position null, so the suggested sequence is not recoverable from the payload

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`
  - `tests/test_setbuilder_cli.py::test_plan_for_composes_the_engine_exactly_as_build_set_does`
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
        {**entry, "position": placed.get(id(scored))}
```

New text:

```
        {**entry, "position": None}
```

### `P5_role_ignored`

The role flag is dropped on the way to the engine, so --role before answers with both sides

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_role_narrows_the_answer_to_one_side`
  - `tests/test_setbuilder_cli.py::test_the_role_flag_reaches_the_engine`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=None)
```

### `P6_count_ignored`

The count flag is dropped on the way to the engine, so the pool is always the default eight

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 6351 against a baseline of 6351
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=None, role=role)
```

### `P7_vox_threshold_ignored`

The vocal threshold is dropped on the way to the ranker, which makes the fifth ranking signal permanently neutral and its whole weight dead

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_vocal_signal_is_reachable_only_because_a_threshold_can_be_supplied`

Old text:

```
        vox_threshold=vox_threshold,
    )
    plan = setbuilder.build_plan
```

New text:

```
        vox_threshold=None,
    )
    plan = setbuilder.build_plan
```

### `P8_anchor_not_owned`

The Anchor is built unowned, which drops its track and with it the genre, energy and vocal signals AND the exclusion that keeps the anchor out of its own pool

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 6 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_plan_for_composes_the_engine_exactly_as_build_set_does`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`
  - `tests/test_setbuilder_cli.py::test_the_vocal_signal_is_reachable_only_because_a_threshold_can_be_supplied`

Old text:

```
        owned=True,
        track=anchor,
```

New text:

```
        owned=False,
        track=None,
```

### `P9_totals_lose_the_anchor`

The resolved anchor is dropped from totals, which is the only place the closed plan surface has for it, so a consumer cannot tell what the plan was computed for

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_the_payload_validates_against_the_declared_plan_surface`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
        "anchor": rendered["anchor"],
    }
    return {
```

New text:

```
    }
    return {
```

### `H1_the_cache_is_written`

build_index is handed the declared cache path, which is a files write from a verb whose registry entry declares none and would make it destructive by the registry's own invariant

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_verb_writes_nothing_at_all`

Old text:

```
    index = setbuilder.build_index(root, template=_template(cfg))
```

New text:

```
    index = setbuilder.build_index(
        root, template=_template(cfg), cache_path=root / "setbuilder_index.json"
    )
```

### `H2_empty_is_a_no_op`

A plan with no companions reports NO_OP rather than OK, which tells a consumer nothing happened when the question was answered

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 6351 against a baseline of 6351
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

The configured library root is no longer checked before the scan, so an unmounted volume scans zero files and every anchor comes back unindexed

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 6351 against a baseline of 6351
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not root.is_dir():
```

New text:

```
    if root.is_dir() and False:
```

### `H4_template_loses_the_marker`

The name template stops declaring the lossy marker, so a marked file's clean title keeps the marker and its head parses differently

- File: `src/cratekit/setbuilder/cli.py`
- Surface: user
- Subset: test files importing cratekit.setbuilder.cli
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 6351 against a baseline of 6351
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))
```

New text:

```
    return NameTemplate()
```

### `R1_marker_restored`

The planned_in marker is put back on the setbuild entry, which withdraws the verb from every conformance property that only drives landed entries

- File: `src/cratekit/cli/registry.py`
- Surface: maintainer
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 2903 against a baseline of 2905
- Kills: 12 (collect-error)
- Note: collection changed: 2903 collected against a baseline of 2905. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker[setbuild]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_is_not_in_the_library_refuses_with_a_vocabulary_code`
  - `tests/test_setbuilder_cli.py::test_an_anchor_with_no_camelot_key_is_not_indexed`
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_refuses_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_the_entry_has_lost_its_planned_marker_and_declares_no_write`
  - `tests/test_setbuilder_cli.py::test_the_role_flag_reaches_the_engine`
  - `tests/test_setbuilder_cli.py::test_the_verb_appears_in_help_under_the_full_profile`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`
  - `tests/test_setbuilder_cli.py::test_the_verb_writes_nothing_at_all`

Old text:

```
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        # U43 LANDED IT.
```

New text:

```
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        planned_in="U35",
        # U43 LANDED IT.
```

### `R2_undeclared_refusal_slug`

setbuild-anchor-not-indexed leaves cause.REASONS, so refuse raises UnknownReason at the boundary instead of refusing

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3738 against a baseline of 3738
- Kills: 3 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_is_not_in_the_library_refuses_with_a_vocabulary_code`
  - `tests/test_setbuilder_cli.py::test_an_anchor_with_no_camelot_key_is_not_indexed`

Old text:

```
        "setbuild-anchor-not-indexed": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `E1_anchor_is_its_own_companion`

build_pool stops excluding the anchor by match key, so the best companion for a track is itself

- File: `src/cratekit/modules/tools/setbuilder.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.setbuilder
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 155 against a baseline of 155
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_set_builder_produces_a_sequence_from_a_snapshot_index`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
        if anchor_match and track.match == anchor_match:
            continue
```

New text:

```
        if anchor_match and track.match != anchor_match:
            pass
```

### `E2_tempo_band_dropped`

in_band returns True for everything, so a track a hundred BPM away enters the pool on its key alone

- File: `src/cratekit/modules/tools/setbuilder.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.setbuilder
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 155 against a baseline of 155
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_anchor_with_no_tempo_drops_the_tempo_constraint`

Old text:

```
    if anchor_bpm is None:
        return True
    if candidate_bpm is None:
        return False
```

New text:

```
    if anchor_bpm is None or candidate_bpm is None:
        return True
```

### `E3_tempo_serialized_as_bpm`

as_payload spells the tempo key the way the Vorbis tag dialect does, which is one splat from handing a tempo to a tag writer and seeding a grid at half or double time (R17)

- File: `src/cratekit/modules/tools/setbuilder.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.setbuilder
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 155 against a baseline of 155
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_no_structured_payload_in_this_unit_carries_a_tempo_TAG_key`
  - `tests/modules/test_tools.py::test_the_structured_payload_carries_a_version`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
            "tempo": plan.anchor.bpm,
```

New text:

```
            "bpm": plan.anchor.bpm,
```

