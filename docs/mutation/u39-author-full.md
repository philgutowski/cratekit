# Mutation table: u39-author-full

Measured by `scripts/mutate.py` on 2026-08-24 15:55 UTC, branch `unit/u39-camelot-padding-at-write-time-and-name-a` at `311ab67`. Pass kind: full.

Baseline: green, 6254 collected. pytest invocations for this batch: 18.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6254 against 6254. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `D1_default_pad_reverted` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1102 | 12 | killed |
| `D2_pad_unguarded` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1102 | 2 | killed |
| `D3_pad_never_runs` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1102 | 13 | killed |
| `R1_filename_source_dropped` | `src/cratekit/write/naming_cli.py` | user | full suite | 6254 | 1 | killed |
| `R2_title_fallback_dropped` | `src/cratekit/write/naming_cli.py` | user | full suite | 6254 | 1 | killed |
| `R3_bpm_dropped` | `src/cratekit/write/naming_cli.py` | user | full suite | 6254 | 6 | killed |
| `R4_head_key_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | full suite | 6254 | 1 | killed |
| `R5_junk_tag_admitted` | `src/cratekit/write/naming_cli.py` | user | full suite | 6254 | 1 | killed |
| `R6_lossy_flag_dropped` | `src/cratekit/write/naming_cli.py` | user | full suite | 6254 | 1 | killed |
| `W1_db_surface_restored` | `src/cratekit/cli/registry.py` | user | 19 file(s) | 2820 | 1 | killed |
| `W2_unreachable_gate_restored` | `src/cratekit/cli/registry.py` | user | 19 file(s) | 2820 | 1 | killed |
| `M1_refusal_reworded` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1102 | 2 | killed |
| `E1_budget_ordering_dropped` | `src/cratekit/core/naming.py` | maintainer | 9 file(s) | 1102 | 1 | killed |
| `E2_wheel_bound_widened` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1102 | 10 | killed |

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `S1_constructor_sites`: Mutate each of the six template constructor call sites Dropped because: the round changed no constructor; every site inherits the default D1 already measures, so six rows would re-measure one guard
- `S2_strip_and_claim_guards`: Mutate strip_head, dedupe_stem and claim_target internals Dropped because: untouched by this round and measured by prior tables; ranked below the two existing guard samples taken (E1, E2)

## Row definitions

### `D1_default_pad_reverted`

Revert the key_pad default to none, the pre U39 written form

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1102 against a baseline of 1102
- Kills: 12 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_budget_head_equals_the_written_head_since_the_pad_moved_in`
  - `tests/test_naming.py::TestRender::test_an_already_fitted_stem_passes_through_verbatim`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::TestRender::test_the_stem_is_the_fallback_when_there_is_no_title_tag`
  - `tests/test_naming.py::TestWriteTimePadding::test_a_code_read_as_data_is_normalized_by_the_padding_stage`
  - `tests/test_naming.py::TestWriteTimePadding::test_rendering_the_padded_output_again_changes_nothing`
  - `tests/test_naming.py::TestWriteTimePadding::test_the_default_template_writes_the_padded_form`
  - `tests/test_naming.py::test_a_second_template_produces_a_different_correct_tree_with_no_code_change`
  - `tests/test_naming.py::test_an_optional_field_widens_render_and_parse_together`

Old text:

```
    key_pad: str = "camelot2"

```

New text:

```
    key_pad: str = "none"

```

### `D2_pad_unguarded`

Pad unconditionally, so an off wheel key raises from pad_camelot instead of the one refusal path

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1102 against a baseline of 1102
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted`
  - `tests/test_naming.py::TestWriteTimePadding::test_an_off_wheel_key_is_still_refused_not_padded`

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if key_pad == "camelot2":

```

### `D3_pad_never_runs`

Padding stage disabled entirely, even for explicit camelot2 templates

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1102 against a baseline of 1102
- Kills: 13 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_an_already_fitted_stem_passes_through_verbatim`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::TestRender::test_the_stem_is_the_fallback_when_there_is_no_title_tag`
  - `tests/test_naming.py::TestWriteTimePadding::test_a_code_read_as_data_is_normalized_by_the_padding_stage`
  - `tests/test_naming.py::TestWriteTimePadding::test_rendering_the_padded_output_again_changes_nothing`
  - `tests/test_naming.py::TestWriteTimePadding::test_the_default_template_writes_the_padded_form`
  - `tests/test_naming.py::test_a_second_template_produces_a_different_correct_tree_with_no_code_change`
  - `tests/test_naming.py::test_an_optional_field_widens_render_and_parse_together`

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if False:

```

### `R1_filename_source_dropped`

Head recovery loses the filename source and keeps only the title fallback

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.write.naming_cli: none found)
- Collected: 6254 against a baseline of 6254
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`

Old text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
    )

```

New text:

```
    head = (
        naming.parse_head(title, template=template)
        or {}
    )

```

### `R2_title_fallback_dropped`

Head recovery loses the title fallback that heals the tag then rename crash window

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.write.naming_cli: none found)
- Collected: 6254 against a baseline of 6254
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_head_is_recovered_from_the_title_when_the_filename_lost_it`

Old text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
    )

```

New text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or {}
    )

```

### `R3_bpm_dropped`

The recovered tempo is discarded, reproducing the head destroying defect

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.write.naming_cli: none found)
- Collected: 6254 against a baseline of 6254
- Kills: 6 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_already_in_convention_proposes_no_rename`
  - `tests/test_naming_apply_cli.py::test_a_key_tag_that_is_not_camelot_does_not_poison_the_pass`
  - `tests/test_naming_apply_cli.py::test_an_unpadded_head_is_carried_and_padded_with_the_tempo_intact`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_head_is_recovered_from_the_title_when_the_filename_lost_it`
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`

Old text:

```
        bpm=int(head["bpm"]) if "bpm" in head else None,

```

New text:

```
        bpm=None,

```

### `R4_head_key_overrules_tag`

The stale head key wins over a corrected initialkey tag

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.write.naming_cli: none found)
- Collected: 6254 against a baseline of 6254
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = head.get("key") or tag_key

```

### `R5_junk_tag_admitted`

A non Camelot initialkey tag reaches the renderer instead of being ignored

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.write.naming_cli: none found)
- Collected: 6254 against a baseline of 6254
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_key_tag_that_is_not_camelot_does_not_poison_the_pass`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = tag_key if tag_key else head.get("key")

```

### `R6_lossy_flag_dropped`

The shared spec loses the lossy flag, recreating the plan and apply disagreement

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.write.naming_cli: none found)
- Collected: 6254 against a baseline of 6254
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_plan_and_the_apply_agree_on_a_marked_file`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=False,

```

### `W1_db_surface_restored`

name.apply reclaims db_metadata it never writes, now with no cloud sync gate

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 2820 against a baseline of 2820
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`

Old text:

```
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),

```

New text:

```
        writes=frozenset({"db_metadata", "files"}),
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),

```

### `W2_unreachable_gate_restored`

name.apply redeclares the cloud sync decision its work can never raise

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 2820 against a baseline of 2820
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`

Old text:

```
            GateSpec(
                name="name.apply.confirm",
                options=("apply", "abort"),
                prompt="Apply these renames?",
                digest_source="plan",
            ),
        ),

```

New text:

```
            GateSpec(
                name="name.apply.confirm",
                options=("apply", "abort"),
                prompt="Apply these renames?",
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),

```

### `M1_refusal_reworded`

Reword the unwritable key refusal, do not append to it

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1102 against a baseline of 1102
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted`
  - `tests/test_naming.py::TestWriteTimePadding::test_an_off_wheel_key_is_still_refused_not_padded`

Old text:

```
            f"{name}={value!r} renders as {rendered!r}, which this engine cannot "

```

New text:

```
            f"{name}={value!r} renders as {rendered!r}, which this engine declines to "

```

### `E1_budget_ordering_dropped`

Existing guard sample: the budget narrower than written refusal is disabled

- File: `src/cratekit/core/naming.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1102 against a baseline of 1102
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestTemplateValidation::test_measuring_narrower_than_writing_is_refused`

Old text:

```
        if KEY_PADS.index(self.budget_key_pad) < KEY_PADS.index(self.key_pad):

```

New text:

```
        if False:

```

### `E2_wheel_bound_widened`

Existing guard sample: the Camelot number bound admits 13 through 19

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1102 against a baseline of 1102
- Kills: 10 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_off_wheel_key_is_rejected_rather_than_normalized[13A]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted`
  - `tests/test_naming.py::TestSplitAndPadHead::test_split_refuses_a_head_the_engine_could_not_have_written`
  - `tests/test_naming.py::TestTheDeletedDuplicate::test_it_accepted_keys_that_are_not_on_the_wheel[13A - 124 - Off Wheel]`
  - `tests/test_naming.py::TestTrailingHead::test_the_trailing_form_holds_the_same_bound_as_the_leading_form[Cola - 13A - 124]`
  - `tests/test_naming.py::TestWriteTimePadding::test_an_off_wheel_key_is_still_refused_not_padded`
  - `tests/test_naming.py::test_is_camelot_agrees_with_parse_camelot`
  - `tests/test_naming.py::test_pad_camelot_normalizes_and_refuses`
  - `tests/test_naming.py::test_parse_and_strip_head[13 is off the wheel]`
  - `tests/test_naming.py::test_parse_camelot[13A]`

Old text:

```
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-2])"

```

New text:

```
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-9])"

```

