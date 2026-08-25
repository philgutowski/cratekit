# Mutation table: u41-naming-independent

Measured by `scripts/mutate.py` on 2026-08-25 21:01 UTC, branch `HEAD` at `79b172f`. Pass kind: full.

Baseline: green, 6266 collected. pytest invocations for this batch: 29.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6266 against 6266. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A1_stem_from_title_again` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 8 | killed |
| `A2_title_fed_the_filename_body` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `A3_stem_not_stripped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6266 | 0 (promoted) | zero |
| `A4_title_not_stripped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6266 | 0 (promoted) | zero |
| `A5_title_field_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `A6_stem_from_path_name` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 19 | killed |
| `A7_title_fallback_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6266 | 0 (promoted) | zero |
| `A8_title_fallback_is_path_name` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `B1_head_precedence_swapped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `B2_filename_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 2 | killed |
| `B3_title_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `B4_bpm_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 14 | killed |
| `B5_key_head_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `B6_camelot_check_on_the_tag_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `B7_lossy_filename_operand_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `B8_lossy_title_operand_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `C1_plan_no_op_filter_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 7 | killed |
| `C3_apply_isfile_recheck_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6266 | 0 (promoted) | zero |
| `C4_claim_target_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6266 | 0 (promoted) | zero |
| `C5_failed_rename_leaves_the_claim` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6266 | 0 (promoted) | zero |
| `C6_target_identity_guard_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6266 | 0 (promoted) | zero |
| `C7_title_tag_write_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 20 | 4 | killed |
| `D1_dedupe_disabled` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 3 | killed |
| `D2_structural_min_parts_lowered` | `src/cratekit/core/naming.py` | user | 10 file(s) | 6266 | 0 (promoted) | zero |
| `D3_endswith_widened_to_containment` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 4 | killed |
| `D4_empty_lead_guard_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 6266 | 0 (promoted) | zero |
| `D5_candidate_separator_guard_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 6266 | 0 (promoted) | zero |
| `D6_repeat_widened_to_prefix` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 2 | killed |
| `D7_dedupe_title_argument_from_the_stem` | `src/cratekit/core/naming.py` | maintainer | 10 file(s) | 6266 | 0 (promoted) | zero |
| `E1_budget_bypassed` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 3 | killed |
| `E2_hash_source_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 6266 | 0 (promoted) | zero |
| `E3_budget_min_becomes_max` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 8 | killed |
| `E4_path_separator_byte_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 3 | killed |
| `E5_truncation_tail_not_reserved` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 5 | killed |
| `E6_dangling_trim_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 6266 | 0 (promoted) | zero |
| `E7_filename_ceiling_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 6266 | 0 (promoted) | zero |
| `F1_normalize_stem_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 1 | killed |
| `F2_normalize_title_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 1 | killed |
| `F3_body_tag_preference_flipped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 27 | killed |
| `F4_body_tag_fallback_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 52 | killed |
| `F5_body_tag_truthiness_becomes_identity` | `src/cratekit/core/naming.py` | user | 10 file(s) | 6266 | 0 (promoted) | zero |
| `F6_filename_prefers_the_title_body` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 34 | killed |
| `F7_library_name_split_from_the_tag` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1122 | 1 | killed |

## Zero rows and what they owe

- `A3_stem_not_stripped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `A4_title_not_stripped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `A7_title_fallback_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `C3_apply_isfile_recheck_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `C4_claim_target_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `C5_failed_rename_leaves_the_claim` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `C6_target_identity_guard_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D2_structural_min_parts_lowered` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D4_empty_lead_guard_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D5_candidate_separator_guard_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D7_dedupe_title_argument_from_the_stem` (maintainer facing): maintainer facing, composite not required
- `E2_hash_source_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `E6_dangling_trim_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `E7_filename_ceiling_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `F5_body_tag_truthiness_becomes_identity` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `C2_audio_extension_case_fold_dropped`: Drop .lower() from the AUDIO_EXTS membership test in _plan_for Dropped because: ranked below the cap: pre-dates U41, untouched by this diff, and the extension filter has no bearing on what a body is composed from
- `C8_apply_parent_dir_blanked`: Pass an empty parent_dir into naming.build from the apply pass, so the budget is measured against the wrong directory Dropped because: ranked below the cap: the budget arithmetic is already covered by E3 through E7, and the plan pass carries the identical call
- `C9_plan_iteration_order_unsorted`: Drop sorted() from the rglob in _plan_for Dropped because: ranked below the cap and deliberately not run: the result would be filesystem order dependent, so a death or a zero would not be reproducible, which METHOD's timing rule forbids in spirit
- `G1_pad_head_key_span_widened`: Splice the whole leading match rather than the key's own span in naming.pad_head Dropped because: ranked below the cap: U39 owns pad_head, its independent table already measured it, and this unit does not touch the head
- `G2_camelot_end_anchor_dropped`: Remove the trailing anchor from _CAMELOT_RE Dropped because: ranked below the cap: already measured at zero by the U39 independent pass and filed as R-167; re-running it buys a second copy of a known number
- `H1_sanitize_segment_slash_rule_dropped`: Stop folding a slash to a dash in sanitize_segment Dropped because: ranked below the cap: it is a body helper this unit does not reach, since _spec_for never calls it and dedupe only uses it on the tag-confirmed branch that this verb cannot enter with album unset

## Row definitions

### `A1_stem_from_title_again`

R-168 restored: the filename body is rebuilt from the title tag, which is the truncation this unit exists to stop

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 8 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
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

### `A2_title_fed_the_filename_body`

The other direction of the same collapse: the title tag is rebuilt from the filename body, stuffing artist and album into every tag the apply pass rewrites

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
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

### `A3_stem_not_stripped`

The filename body is carried WITHOUT stripping its existing head, so a head stacks on a head

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        stem=naming.strip_head(path.stem, template=template),

```

New text:

```
        stem=path.stem,

```

### `A4_title_not_stripped`

The tag body is carried without stripping its head, so the tag stacks a head on a head

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=title,

```

### `A5_title_field_dropped`

The spec carries no title at all, so render_all falls back to the filename body for the tag

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
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

### `A6_stem_from_path_name`

The filename body is taken from path.name rather than path.stem, so the suffix leaks into the body

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 19 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_file_with_no_title_tag_takes_its_body_from_the_filename`
  - `tests/test_naming_apply_cli.py::test_a_folder_already_in_convention_proposes_no_rename`
  - `tests/test_naming_apply_cli.py::test_a_key_tag_that_is_not_camelot_does_not_poison_the_pass`
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_filename_alone_is_not_stripped_off`
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_title_alone_is_still_recovered`
  - `tests/test_naming_apply_cli.py::test_a_name_with_no_parseable_head_is_left_as_it_arrives`
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
  - `tests/test_naming_apply_cli.py::test_an_unpadded_head_is_carried_and_padded_with_the_tempo_intact`
  - `tests/test_naming_apply_cli.py::test_both_library_grammars_survive_a_rename`
  - `tests/test_naming_apply_cli.py::test_the_filename_body_is_carried_through_a_padding_rename`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        stem=naming.strip_head(path.stem, template=template),

```

New text:

```
        stem=naming.strip_head(path.name, template=template),

```

### `A7_title_fallback_dropped`

An absent title tag no longer falls back to the filename stem; the title source becomes the empty string

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    title = tags.read_tag(path, "title") or path.stem

```

New text:

```
    title = tags.read_tag(path, "title") or ""

```

### `A8_title_fallback_is_path_name`

The absent-tag fallback uses path.name instead of path.stem, so the suffix reaches the title tag

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_with_no_title_tag_takes_its_body_from_the_filename`

Old text:

```
    title = tags.read_tag(path, "title") or path.stem

```

New text:

```
    title = tags.read_tag(path, "title") or path.name

```

### `B1_head_precedence_swapped`

The title's head is parsed before the filename's, so a stale tag head drags a correct filename backwards

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`

Old text:

```
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)

```

New text:

```
        naming.parse_head(title, template=template)
        or naming.parse_head(path.name, template=template)

```

### `B2_filename_head_source_dropped`

The filename is no longer a head source, so only a tag-carried head is recovered

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`

Old text:

```
        naming.parse_head(path.name, template=template)

```

New text:

```
        None

```

### `B3_title_head_source_dropped`

The title is no longer a head source, so the tag-then-rename crash window stops healing

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_head_is_recovered_from_the_title_when_the_filename_lost_it`

Old text:

```
        or naming.parse_head(title, template=template)

```

New text:

```
        or None

```

### `B4_bpm_dropped`

The recovered tempo never reaches the spec, so the head degrades to key only

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 14 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_file_with_no_title_tag_takes_its_body_from_the_filename`
  - `tests/test_naming_apply_cli.py::test_a_folder_already_in_convention_proposes_no_rename`
  - `tests/test_naming_apply_cli.py::test_a_key_tag_that_is_not_camelot_does_not_poison_the_pass`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
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

### `B5_key_head_overrules_tag`

The head's key wins over a corrected initialkey tag, so renaming from metadata stops working

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
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

### `B6_camelot_check_on_the_tag_key_dropped`

A non-Camelot initialkey tag is trusted, so junk reaches the head renderer

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
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

### `B7_lossy_filename_operand_dropped`

U39's K2: the lossy OR loses its filename operand, so a file marked only in its name is renamed to its unmarked form

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_filename_alone_is_not_stripped_off`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=marker in title,

```

### `B8_lossy_title_operand_dropped`

U39's K1: the lossy OR loses its title operand, so a marker surviving only in the tag stops being restored

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_title_alone_is_still_recovered`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=marker in path.stem,

```

### `C1_plan_no_op_filter_dropped`

Every audio file enters the plan, including the ones already in convention

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 7 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_folder_already_in_convention_proposes_no_rename`
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_filename_alone_is_not_stripped_off`
  - `tests/test_naming_apply_cli.py::test_a_name_with_no_parseable_head_is_left_as_it_arrives`
  - `tests/test_naming_apply_cli.py::test_an_unpadded_head_is_carried_and_padded_with_the_tempo_intact`
  - `tests/test_naming_apply_cli.py::test_the_plan_and_the_apply_agree_on_a_marked_file`
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`

Old text:

```
            if rendered.filename != path.name:

```

New text:

```
            if True:

```

### `C3_apply_isfile_recheck_dropped`

The apply pass no longer re-checks that the planned path still exists across the confirm gate

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if not path.is_file():
            continue

```

New text:

```
(empty)
```

### `C4_claim_target_dropped`

R-172's guard: the rename no longer claims its target first, so POSIX rename silently overwrites the loser of a collision

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if not naming.claim_target(target):
                continue

```

New text:

```
(empty)
```

### `C5_failed_rename_leaves_the_claim`

A rename that raises leaves the zero-byte claim stub behind as a phantom track

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                target.unlink(missing_ok=True)

```

New text:

```
                pass

```

### `C6_target_identity_guard_dropped`

The rename branch is entered even when the target equals the source

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if target != path:

```

New text:

```
        if True:

```

### `C7_title_tag_write_dropped`

The apply pass renames and never writes the title tag, so the two surfaces diverge

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.naming_cli
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 20 against a baseline of 20
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_with_no_title_tag_takes_its_body_from_the_filename`
  - `tests/test_naming_apply_cli.py::test_an_unpadded_head_is_carried_and_padded_with_the_tempo_intact`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_title_tag_is_not_given_the_filename_body`

Old text:

```
        tags.write_tags(path, {"title": rendered.title_tag})

```

New text:

```
        pass

```

### `D1_dedupe_disabled`

The stem is never deduped, so a trailing segment repeating the lead survives

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_dedupe_runs_before_the_fit_and_the_hash_uses_the_original`
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`

Old text:

```
    deduped = dedupe_stem(spec.stem, spec.title, spec.album, sep=template.segment_sep)

```

New text:

```
    deduped = spec.stem

```

### `D2_structural_min_parts_lowered`

The structural rule fires on two segments instead of three, so a two segment name loses its second half

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if len(parts) >= 3:

```

New text:

```
    if len(parts) >= 2:

```

### `D3_endswith_widened_to_containment`

The repeat test becomes containment rather than a trailing match, so a lead appearing mid name triggers a cut

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
  - `tests/test_naming_budget.py::TestDedupeStem::test_identity_on_near_match_album`
  - `tests/test_naming_budget.py::TestDedupeStem::test_title_containing_the_separator_is_ambiguous_structurally`
  - `tests/test_naming_budget.py::TestDedupeStem::test_title_containing_the_separator_is_deduped_via_tags`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead and (sep + lead) in stem:

```

### `D4_empty_lead_guard_dropped`

An empty lead segment no longer blocks the structural rule

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if stem.endswith(sep + lead):

```

### `D5_candidate_separator_guard_dropped`

The structural rule stops requiring that something survives the cut, so a two segment name can be reduced to one

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if sep in candidate:

```

New text:

```
            if True:

```

### `D6_repeat_widened_to_prefix`

AMBIGUITY MEANS IDENTITY is inverted: a trailing segment that merely BEGINS with the lead counts as a repeat

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
  - `tests/test_naming_budget.py::TestDedupeStem::test_identity_on_near_match_album`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead and parts[-1].startswith(lead):

```

### `D7_dedupe_title_argument_from_the_stem`

dedupe's tag-confirmed rule is fed the filename body instead of the title tag, which is the collapse this unit undid, one layer down

- File: `src/cratekit/core/naming.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    deduped = dedupe_stem(spec.stem, spec.title, spec.album, sep=template.segment_sep)

```

New text:

```
    deduped = dedupe_stem(spec.stem, spec.stem, spec.album, sep=template.segment_sep)

```

### `E1_budget_bypassed`

The fitted stem is discarded and the deduped one is returned, so nothing is ever shortened to the path ceiling

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_an_absent_field_contributes_zero_bytes_including_its_separator`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`

Old text:

```
    return replace(spec, stem=fitted)

```

New text:

```
    return replace(spec, stem=deduped)

```

### `E2_hash_source_dropped`

The truncation hash is taken from the deduped stem rather than the original, so two sources that dedupe alike also hash alike

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        hash_source=spec.stem,

```

New text:

```
        hash_source=None,

```

### `E3_budget_min_becomes_max`

The two ceilings are combined with max rather than min, so the looser one wins

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 8 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_a_character_count_would_have_passed_this_and_the_byte_count_does_not`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_an_unsatisfiable_budget_raises_rather_than_emitting`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_multibyte_never_splits_a_codepoint`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_two_budgets_in_one_process_give_two_answers`

Old text:

```
    max_stem = min(

```

New text:

```
    max_stem = max(

```

### `E4_path_separator_byte_dropped`

The path separator's byte is no longer counted against the path budget

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`

Old text:

```
        + 1  # the path separator

```

New text:

```
        + 0  # the path separator

```

### `E5_truncation_tail_not_reserved`

The disambiguating tail's bytes are not reserved, so the assembled name overshoots the ceiling by its length

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_a_character_count_would_have_passed_this_and_the_byte_count_does_not`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_multibyte_never_splits_a_codepoint`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`

Old text:

```
    avail = max_stem - len(tail)

```

New text:

```
    avail = max_stem

```

### `E6_dangling_trim_dropped`

A byte cut may end mid phrase, on a space, a dash or an open bracket

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    visible = trim_dangling(truncated) or truncated.strip() or "x"

```

New text:

```
    visible = truncated or "x"

```

### `E7_filename_ceiling_dropped`

Only the total path budget is enforced; the per filename ceiling stops constraining anything

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        budget.filename_max_bytes - fixed_name,

```

New text:

```
        budget.path_budget_bytes - fixed_path,

```

### `F1_normalize_stem_dropped`

The engine stops stripping a head off the stem, so idempotency over the crash window depends on the shell alone

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_rendering_is_idempotent`

Old text:

```
    stem = strip_head(spec.stem, template=template)

```

New text:

```
    stem = spec.stem

```

### `F2_normalize_title_dropped`

The engine stops stripping a head off the title, so a second head compounds on the tag

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_rendering_is_idempotent`

Old text:

```
    title = strip_head(spec.title, template=template) if spec.title else spec.title

```

New text:

```
    title = spec.title

```

### `F3_body_tag_preference_flipped`

The tag body prefers the filename's stem over the title, which is A2 reproduced inside the engine

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 27 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[None-124-Title Tag-False-custom]`
  - ... and 12 more, see the JSON sidecar

Old text:

```
    body_tag = spec.title if spec.title else spec.stem

```

New text:

```
    body_tag = spec.stem if spec.stem else spec.title

```

### `F4_body_tag_fallback_dropped`

The tag body has no fallback at all, so a spec with no title renders None into the tag

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 52 (killed)
- Killed:
  - `tests/test_naming.py::TestAnalysisOff::test_a_lossy_file_is_still_marked_with_analysis_off`
  - `tests/test_naming.py::TestAnalysisOff::test_a_tempo_without_a_key_renders_no_head_at_all`
  - `tests/test_naming.py::TestAnalysisOff::test_absent_fields_are_omitted_not_rendered_empty`
  - `tests/test_naming.py::TestAnalysisOff::test_it_round_trips_through_the_parser`
  - `tests/test_naming.py::TestAnalysisOff::test_no_key_and_no_tempo_renders_the_body_alone`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_budget_head_equals_the_written_head_since_the_pad_moved_in`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_same_input_twice_yields_the_same_path`
  - `tests/test_naming.py::TestMarkerCoupling::test_a_lossless_file_renders_fine_under_the_same_template`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-124-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-124-True]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-None-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-None-True]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-None-None-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-None-None-True]`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    body_tag = spec.title if spec.title else spec.stem

```

New text:

```
    body_tag = spec.title

```

### `F5_body_tag_truthiness_becomes_identity`

R-171's proposed fix applied as a mutation: a PRESENT but empty title stops inheriting the filename body

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 6266 against a baseline of 6266
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    body_tag = spec.title if spec.title else spec.stem

```

New text:

```
    body_tag = spec.title if spec.title is not None else spec.stem

```

### `F6_filename_prefers_the_title_body`

R-168 reproduced one file over: the FILENAME is rendered from the title body when there is one, inside the engine rather than in the shell

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 34 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[None-124-Title Tag-False-custom]`
  - ... and 19 more, see the JSON sidecar

Old text:

```
        filename=head + spec.stem + spec.suffix,

```

New text:

```
        filename=head + (spec.title or spec.stem) + spec.suffix,

```

### `F7_library_name_split_from_the_tag`

The library name is derived from the stem rather than from the rendered title tag, so the marker can go missing from one surface only

- File: `src/cratekit/core/naming.py`
- Surface: user
- Subset: test files importing cratekit.core.naming
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1122 against a baseline of 1122
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`

Old text:

```
        library_name=title_tag,

```

New text:

```
        library_name=head + spec.stem,

```

