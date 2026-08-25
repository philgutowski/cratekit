# Mutation table: u41-author-full

Measured by `scripts/mutate.py` on 2026-08-25 18:32 UTC, branch `unit/u41-what-the-filename-body-is-composed-from-` at `fe47197`. Pass kind: full.

Baseline: green, 6262 collected. pytest invocations for this batch: 12.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6262 against 6262. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `R8_stem_from_title_again` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 16 | 5 | killed |
| `T1_title_tag_fed_the_filename_body` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `T2_title_field_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `R4_bpm_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 16 | 11 | killed |
| `R6_head_key_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `R1_filename_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 16 | 2 | killed |
| `D1_dedupe_disabled` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1118 | 2 | killed |
| `D2_dedupe_structural_rule_widened` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1118 | 7 | killed |

## Row definitions

### `R8_stem_from_title_again`

The body is taken from the title tag again, which is R-168 exactly and the reason this unit exists

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`
  - `tests/test_naming_apply_cli.py::test_both_library_grammars_survive_a_rename`
  - `tests/test_naming_apply_cli.py::test_the_filename_body_is_carried_through_a_padding_rename`
  - `tests/test_naming_apply_cli.py::test_the_title_tag_is_not_given_the_filename_body`

Old text:

```
        stem=naming.strip_head(path.stem, template=template),

```

New text:

```
        stem=naming.strip_head(title, template=template),

```

### `T1_title_tag_fed_the_filename_body`

The title tag is rebuilt from the filename body, which stuffs the artist and the album into every tag the apply pass rewrites

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_title_tag_is_not_given_the_filename_body`

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=naming.strip_head(path.stem, template=template),

```

### `T2_title_field_dropped`

The spec stops carrying a title at all, so render_all falls back to the stem for the tag surface

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_title_tag_is_not_given_the_filename_body`

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=None,

```

### `R4_bpm_dropped`

The recovered tempo is dropped, which is the pre-U39 hazard and must stay dead

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 11 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_already_in_convention_proposes_no_rename`
  - `tests/test_naming_apply_cli.py::test_a_key_tag_that_is_not_camelot_does_not_poison_the_pass`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`
  - `tests/test_naming_apply_cli.py::test_an_unpadded_head_is_carried_and_padded_with_the_tempo_intact`
  - `tests/test_naming_apply_cli.py::test_both_library_grammars_survive_a_rename`
  - `tests/test_naming_apply_cli.py::test_the_filename_body_is_carried_through_a_padding_rename`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`
  - `tests/test_naming_apply_cli.py::test_the_head_is_recovered_from_the_title_when_the_filename_lost_it`
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`
  - `tests/test_naming_apply_cli.py::test_the_title_tag_is_not_given_the_filename_body`

Old text:

```
        bpm=int(head["bpm"]) if "bpm" in head else None,

```

New text:

```
        bpm=None,

```

### `R6_head_key_overrules_tag`

Key precedence reversed, so a corrected key tag can no longer move a file

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = head.get("key") or (tag_key if tag_key and naming.is_camelot(tag_key) else None)

```

### `R1_filename_head_source_dropped`

The filename is no longer a head source, leaving the title as the only one

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`

Old text:

```
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)

```

New text:

```
        naming.parse_head(title, template=template)

```

### `D1_dedupe_disabled`

dedupe_stem stops dropping a trailing segment that repeats the lead; an existing guard this unit switched on for real input

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1118 against a baseline of 1118
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_dedupe_runs_before_the_fit_and_the_hash_uses_the_original`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`

Old text:

```
    deduped = dedupe_stem(spec.stem, spec.title, spec.album, sep=template.segment_sep)

```

New text:

```
    deduped = spec.stem

```

### `D2_dedupe_structural_rule_widened`

The structural dedupe rule drops its exact trailing match, so an unrelated trailing segment is mutilated

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1118 against a baseline of 1118
- Kills: 7 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_name_with_no_parseable_head_is_left_as_it_arrives`
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_both_library_grammars_survive_a_rename`
  - `tests/test_naming_budget.py::TestDedupeStem::test_identity_on_near_match_album`
  - `tests/test_naming_budget.py::TestDedupeStem::test_identity_when_segments_differ`
  - `tests/test_naming_budget.py::TestDedupeStem::test_title_containing_the_separator_is_ambiguous_structurally`
  - `tests/test_naming_budget.py::TestDedupeStem::test_title_containing_the_separator_is_deduped_via_tags`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead:

```

