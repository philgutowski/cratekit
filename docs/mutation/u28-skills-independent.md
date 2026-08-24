# Mutation table: u28-skills-independent

Measured by `scripts/mutate.py` on 2026-08-24 04:08 UTC, branch `HEAD` at `ffded5c`. Pass kind: full.

Baseline: green, 6225 collected. pytest invocations for this batch: 27.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

> SCRUBBED AFTER MEASUREMENT. Row `X2_mount_rule_removed` kills three
> parametrized cases in `tests/test_portability.py` whose test IDS EMBED the
> synthetic volume literal that file assembles at runtime precisely so it never
> appears in the tree. Recording the killed node ids therefore materialized it
> here, and `scripts/scan_repo.py` failed on this file, which reddens one third
> of the merge battery. The literal is replaced by a placeholder above. The
> counts are untouched.

Null control `NULL_CONTROL`: killed 0, collected 6225 against 6225. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `S1_shipped_names_dir_filter` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 6225 | 0 (promoted) | zero |
| `S2_shipped_names_sorted` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 6225 | 0 (promoted) | zero |
| `S3_files_regular_only` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 6225 | 0 (promoted) | zero |
| `S4_stamp_is_file` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 6225 | 0 (promoted) | zero |
| `S5_stamp_quote_strip` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 5 | killed |
| `S6_stamp_key_exact` | `src/cratekit/skills/cli.py` | maintainer | 1 file(s) | 6225 | 0 (promoted) | zero |
| `S7_replace_whole` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 1 | killed |
| `S8_outcome_collapse_refreshed` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 3 | killed |
| `S9_previous_always_none` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 3 | killed |
| `S10_stamp_skill_name` | `src/cratekit/skills/cli.py` | maintainer | 1 file(s) | 6225 | 1 (promoted) | killed |
| `S11_typed_cause_lost` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 2 | killed |
| `S12_reason_slug` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 2 | killed |
| `S13_expanduser` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 6225 | 1 (promoted) | killed |
| `S14_into_ignored` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 8 | killed |
| `S15_drift_never_warns` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 1 | killed |
| `S16_counts_miscounted` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 3 | killed |
| `S17_outcome_always_ok` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 6225 | 1 (promoted) | killed |
| `S18_detail_reworded` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 1 | killed |
| `S19_default_target_literal` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 1 | killed |
| `S20_packaged_root_via_file` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 6225 | 1 (promoted) | killed |
| `L1_rule_g_removed` | `tests/test_skills_lint.py` | user | 1 file(s) | 24 | 2 | killed |
| `L2_rule_g_root_flag_union` | `tests/test_skills_lint.py` | maintainer | 1 file(s) | 24 | 2 | killed |
| `L3_rule_g_continuation_skip` | `tests/test_skills_lint.py` | maintainer | 1 file(s) | 6225 | 1 (promoted) | killed |
| `L4_rule_g_value_flag_skip` | `tests/test_skills_lint.py` | maintainer | 1 file(s) | 24 | 2 | killed |
| `L5_rule_g_entry_point_filter` | `tests/test_skills_lint.py` | maintainer | 1 file(s) | 24 | 3 | killed |
| `L6_rule_h_fenced_half` | `tests/test_skills_lint.py` | user | 1 file(s) | 24 | 1 | killed |
| `L7_rule_h_code_span_half` | `tests/test_skills_lint.py` | user | 1 file(s) | 24 | 1 | killed |
| `L8_rule_h_substring_to_equality` | `tests/test_skills_lint.py` | user | 1 file(s) | 24 | 1 | killed |
| `L9_command_comment_split` | `tests/test_skills_lint.py` | maintainer | 1 file(s) | 6225 | 1 (promoted) | killed |
| `L10_fence_info_string` | `tests/test_skills_lint.py` | user | 1 file(s) | 24 | 1 | killed |
| `L11_rule_d_scanner` | `tests/test_skills_lint.py` | user | 1 file(s) | 24 | 2 | killed |
| `L12_verb_table_nargs` | `tests/test_skills_lint.py` | maintainer | 1 file(s) | 6225 | 1 (promoted) | killed |
| `L13_taxonomy_energy_bands` | `tests/test_skills_lint.py` | user | 1 file(s) | 6225 | 0 (promoted) | zero |
| `L14_rule_a_name_match` | `tests/test_skills_lint.py` | user | 1 file(s) | 24 | 1 | killed |
| `L15_skills_root_moved_back` | `tests/test_skills_lint.py` | user | 1 file(s) | 6225 | 0 (promoted) | zero |
| `P1_annassign_branch` | `tests/test_pending_units.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `P2_empty_call_args` | `tests/test_pending_units.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `P3_empty_register_assertion` | `tests/test_pending_units.py` | maintainer | 1 file(s) | 6225 | 0 (promoted) | zero |
| `P4_is_absent_path_key` | `tests/_pending.py` | maintainer | 1 file(s) | 6225 | 0 (promoted) | zero |
| `C1_at_risk_population_pin` | `tests/test_reserved_causes.py` | maintainer | 1 file(s) | 228 | 1 | killed |
| `R1_planned_in_restored` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 520 | collection error | collect-error |
| `K1_package_data_removed` | `pyproject.toml` | user | 2 file(s) | 6225 | 0 (promoted) | zero |
| `K1_composite` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 14 | 9 | killed |
| `X1_placeholder_exemption` | `scripts/scan_repo.py` | user | 1 file(s) | 56 | 2 | killed |
| `X2_mount_rule_removed` | `scripts/scan_repo.py` | user | 1 file(s) | 56 | 4 | killed |

## Zero rows and what they owe

- `S1_shipped_names_dir_filter` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S2_shipped_names_sorted` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S3_files_regular_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S4_stamp_is_file` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S6_stamp_key_exact` (maintainer facing): maintainer facing, composite not required
- `L13_taxonomy_energy_bands` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `L15_skills_root_moved_back` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `P3_empty_register_assertion` (maintainer facing): maintainer facing, composite not required
- `P4_is_absent_path_key` (maintainer facing): maintainer facing, composite not required
- `K1_package_data_removed` (user facing): paired with `K1_composite`, which killed 9

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `S21_stamp_name_constant`: rename STAMP_NAME to a non-dot file Dropped because: ranked below the cap: the stamp's content and its is_file gate are already measured by S4, S5, S6 and S10, and a rename only re-measures the same read path
- `L16_rule_b_command_token`: widen _COMMAND_TOKEN so it stops recognising the product's own scripts Dropped because: ranked below the cap: rule (b) is not part of this commit's diff and its fixtures are unchanged, so the row would measure a pre-existing guard the round did not touch
- `L17_rule_f_deep_ref`: drop the deep-reference existence check Dropped because: ranked below the cap: rule (f) is unchanged by this commit and no shipped skill currently carries a deep reference, so the row measures a rule with no live input
- `L18_rule_e_year`: drop the year-literal path segment rule Dropped because: ranked below the cap: rule (e) is unchanged by this commit and the commit's own claim rests on rules (g) and (h), which are measured across nine rows
- `S22_build_flag_default`: change the --into default from None to a literal path Dropped because: ranked below the cap: S13, S14 and S19 already measure the three ways the target can be resolved wrongly, and the default is read only through the branch S14 removes
- `X3_beat_grid_guard`: revert one of the two beat-grid suites' write refusals Dropped because: ranked below the cap: no line in this commit touches a write path, and the twelve skills were read for grid-writing instructions separately and carry none

## Row definitions

### `S1_shipped_names_dir_filter`

shipped_names stops filtering to directories, so a stray file beside the skills is offered as a skill

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return tuple(sorted(entry.name for entry in root.iterdir() if entry.is_dir()))
```

New text:

```
    return tuple(sorted(entry.name for entry in root.iterdir()))
```

### `S2_shipped_names_sorted`

shipped_names drops sorted(), so the install order and the reported order become filesystem order

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return tuple(sorted(entry.name for entry in root.iterdir() if entry.is_dir()))
```

New text:

```
    return tuple(entry.name for entry in root.iterdir() if entry.is_dir())
```

### `S3_files_regular_only`

_files stops filtering to regular files, so a nested directory is handed to write_bytes

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    yield from (entry for entry in directory.iterdir() if entry.is_file())
```

New text:

```
    yield from directory.iterdir()
```

### `S4_stamp_is_file`

installed_version accepts any existing stamp path, including a directory named like the stamp

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not stamp.is_file():
        return None
```

New text:

```
    if not stamp.exists():
        return None
```

### `S5_stamp_quote_strip`

installed_version stops stripping the TOML quotes, so every stamped copy reads as a different version

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 5 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
            return value.strip().strip('"')
```

New text:

```
            return value.strip()
```

### `S6_stamp_key_exact`

installed_version matches the version key by prefix rather than exactly, so a 'version_written_by' line wins

- File: `src/cratekit/skills/cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if name.strip() == "version":
```

New text:

```
        if name.strip().startswith("version"):
```

### `S7_replace_whole`

install_one copies over the top instead of removing the destination, so a withdrawn file survives looking current

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_file_this_build_no_longer_ships_disappears`

Old text:

```
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
```

New text:

```
    destination.mkdir(parents=True, exist_ok=True)
```

### `S8_outcome_collapse_refreshed`

install_one calls every pre-existing copy current, so drift is never reported

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 3 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`

Old text:

```
        else "current"
        if previous == __version__
        else "refreshed"
```

New text:

```
        else "current"
```

### `S9_previous_always_none`

install_one never reads the existing stamp, so a copy from this same build reports as refreshed

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 3 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
    previous = installed_version(destination) if destination.exists() else None
```

New text:

```
    previous = None
```

### `S10_stamp_skill_name`

the stamp stops recording which skill it belongs to, so a copied stamp cannot be told from its own

- File: `src/cratekit/skills/cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
\nskill = "{name}"
```

New text:

```
(empty)
```

### `S11_typed_cause_lost`

install_skills stops converting the mkdir OSError into a typed cause, so an unwritable target arrives as an internal error

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_refusal_leaves_no_half_written_target`
  - `tests/test_skills_install.py::test_a_target_that_cannot_be_created_refuses_with_a_typed_cause`

Old text:

```
    try:
        into.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CratekitError(
            Cause(
                reason="path-permission-denied",
```

New text:

```
    if True:
        into.mkdir(parents=True, exist_ok=True)
    if False:
        raise CratekitError(
            Cause(
                reason="path-permission-denied",
```

### `S12_reason_slug`

the refusal's reason slug is changed to a neighbouring one, so the typed cause names the wrong condition

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_refusal_leaves_no_half_written_target`
  - `tests/test_skills_install.py::test_a_target_that_cannot_be_created_refuses_with_a_typed_cause`

Old text:

```
                reason="path-permission-denied",
```

New text:

```
                reason="path-not-found",
```

### `S13_expanduser`

--into stops expanding a tilde, so a target given as ~/skills is created as a literal directory named ~

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
    into = Path(ctx.args.into).expanduser() if ctx.args.into else default_target()
```

New text:

```
    into = Path(ctx.args.into) if ctx.args.into else default_target()
```

### `S14_into_ignored`

--into is ignored and the default target is always used, so a caller's chosen destination is silently overridden

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 8 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_this_build_no_longer_ships_disappears`
  - `tests/test_skills_install.py::test_a_refusal_leaves_no_half_written_target`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_a_target_that_cannot_be_created_refuses_with_a_typed_cause`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_every_shipped_skill_is_installed_and_the_set_is_walked_not_listed`
  - `tests/test_skills_install.py::test_the_copies_are_copies_and_not_symlinks`

Old text:

```
    into = Path(ctx.args.into).expanduser() if ctx.args.into else default_target()
```

New text:

```
    into = default_target()
```

### `S15_drift_never_warns`

every check reports ok, so a refreshed copy no longer tells the person their agent was reading an older build

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`

Old text:

```
                "status": "ok" if was in {"installed", "current"} else "info",
```

New text:

```
                "status": "ok",
```

### `S16_counts_miscounted`

every skill is counted as installed, so the summary claims a first install on every re-run

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 3 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
        counts[was] += 1
```

New text:

```
        counts["installed"] += 1
```

### `S17_outcome_always_ok`

the envelope reports OK even when nothing was installed, so an empty package reads as a successful install

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
        outcome=Outcome.OK if checks else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `S18_detail_reworded`

the refreshed detail sentence is reworded, dropping the phrase the drift test reads

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`

Old text:

```
        f"the copy at {where} was written by a different build and has been "
        f"replaced; anything reading it was following older instructions"
```

New text:

```
        f"the copy at {where} came from another release of this tool and was "
        f"overwritten; whatever read it was following older instructions"
```

### `S19_default_target_literal`

default_target stops composing from home and returns a relative path, which R1 exists to forbid

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_the_default_target_is_composed_from_home_and_is_not_a_literal`

Old text:

```
    return Path.home().joinpath(*DEFAULT_TARGET)
```

New text:

```
    return Path(*DEFAULT_TARGET)
```

### `S20_packaged_root_via_file`

packaged_root resolves by path arithmetic from __file__ rather than through importlib.resources

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 6225 against a baseline of 6225
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
    return resources.files("cratekit.skills") / "assets"
```

New text:

```
    return Path(__file__).resolve().parent / "assets"
```

### `L1_rule_g_removed`

rule (g) is removed entirely, so no fenced crate invocation is checked against the parser

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_command_naming_a_flag_the_verb_does_not_declare_fails`
  - `tests/test_skills_lint.py::test_a_command_naming_no_real_verb_fails`

Old text:

```
        for line in command_text.split("\n"):
            problems += _verb_problems(line, directory.name, verbs)
```

New text:

```
        for line in command_text.split("\n"):
            del line
```

### `L2_rule_g_root_flag_union`

rule (g) stops unioning the root flags into the allowed set, which is what lets a root flag be written after the verb

- File: `tests/test_skills_lint.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_real_verb_with_real_flags_and_a_positional_passes`
  - `tests/test_skills_lint.py::test_real_skills_pass_lint`

Old text:

```
    allowed = set(verbs[path]) | set(verbs[()])
```

New text:

```
    allowed = set(verbs[path])
```

### `L3_rule_g_continuation_skip`

rule (g) stops skipping a continuation line, so a long invocation written across lines is reported

- File: `tests/test_skills_lint.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 6225 against a baseline of 6225
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
    if line.rstrip().endswith("\\"):
        return []
```

New text:

```
    if False:
        return []
```

### `L4_rule_g_value_flag_skip`

rule (g) stops skipping a value-taking flag's argument, which is the defect the fixtures found before the tree did

- File: `tests/test_skills_lint.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_real_verb_with_real_flags_and_a_positional_passes`
  - `tests/test_skills_lint.py::test_real_skills_pass_lint`

Old text:

```
            index += 2 if takes_value and "=" not in token else 1
```

New text:

```
            index += 1
```

### `L5_rule_g_entry_point_filter`

rule (g) checks every fenced line rather than only the ones invoking the product's entry point

- File: `tests/test_skills_lint.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_continuation_line_is_not_read_as_a_verb`
  - `tests/test_skills_lint.py::test_extra_files_in_a_skill_directory_pass`
  - `tests/test_skills_lint.py::test_year_literal_in_fenced_block_fails_prose_passes`

Old text:

```
    if not tokens or tokens[0] != "crate":
        return []
```

New text:

```
    if not tokens:
        return []
```

### `L6_rule_h_fenced_half`

rule (h) stops looking inside fenced blocks and checks only inline code spans

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_hardcoded_taxonomy_name_in_a_command_fails`

Old text:

```
        for span in _CODE_SPANS.findall(text) + _FENCED.findall(text):
```

New text:

```
        for span in _CODE_SPANS.findall(text):
```

### `L7_rule_h_code_span_half`

rule (h) stops looking inside inline code spans and checks only fenced blocks

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_hardcoded_taxonomy_name_in_an_inline_code_span_fails`

Old text:

```
        for span in _CODE_SPANS.findall(text) + _FENCED.findall(text):
```

New text:

```
        for span in _FENCED.findall(text):
```

### `L8_rule_h_substring_to_equality`

rule (h) matches a display name only when it is the whole span, so a name used as a path segment passes

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_hardcoded_taxonomy_name_in_a_command_fails`

Old text:

```
                if name in span:
```

New text:

```
                if name == span:
```

### `L9_command_comment_split`

the fenced text stops being split into command and comment, so a retired name in a history note is checked as a command

- File: `tests/test_skills_lint.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 6225 against a baseline of 6225
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
            elif " #" in line:
                command, _, tail = line.partition(" #")
                command_parts.append(command)
                comment_parts.append(tail)
```

New text:

```
            elif " #" in line:
                command_parts.append(line)
```

### `L10_fence_info_string`

the fence regex reverts to the source system's [a-z]* form, which silently skips a fence carrying an info-string tail

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_info_string_fence_is_not_a_blind_spot`

Old text:

```
_FENCED = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
```

New text:

```
_FENCED = re.compile(r"```[a-z]*\n(.*?)```", re.DOTALL)
```

### `L11_rule_d_scanner`

rule (d) stops delegating to the portability scanner, so no personal literal in a shipped skill is found

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_home_directory_literal_in_a_skill_fails`
  - `tests/test_skills_lint.py::test_a_volume_literal_in_any_skill_fails`

Old text:

```
        for violation in scan.portability_violations(
            text, identity_tokens=scan.machine_identity_tokens()
        ):
```

New text:

```
        for violation in []:
```

### `L12_verb_table_nargs`

verb_table records every flag as value-taking, so a boolean flag swallows the token after it

- File: `tests/test_skills_lint.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 6225 against a baseline of 6225
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
                name: action.nargs != 0
```

New text:

```
                name: True
```

### `L13_taxonomy_energy_bands`

taxonomy_display_names drops the energy bands, so rule (h) stops knowing three of the names

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        | {band.display for band in declared.energy.bands}
```

New text:

```
        | set()
```

### `L14_rule_a_name_match`

rule (a) stops requiring the frontmatter name to match the directory

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_missing_frontmatter_and_name_mismatch_fail`

Old text:

```
            if not match or match.group(1) != directory.name:
```

New text:

```
            if not match:
```

### `L15_skills_root_moved_back`

SKILLS_ROOT points back at a repository-root skills directory, the location this unit decided against

- File: `tests/test_skills_lint.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
SKILLS_ROOT = SRC_ROOT / "cratekit" / "skills" / "assets"
```

New text:

```
SKILLS_ROOT = REPO_ROOT / "skills"
```

### `P1_annassign_branch`

the duplicate guard stops reading an AnnAssign, which is the node the annotated empty register became

- File: `tests/test_pending_units.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_intended_pending_set_has_no_duplicate_element`

Old text:

```
        if isinstance(node, ast.AnnAssign):
            target = getattr(node.target, "id", None)
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
```

New text:

```
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
```

### `P2_empty_call_args`

the duplicate guard stops tolerating frozenset() with no argument, which is the empty register's own spelling

- File: `tests/test_pending_units.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_intended_pending_set_has_no_duplicate_element`

Old text:

```
        elements = literal.args[0].elts if literal.args else []
```

New text:

```
        elements = literal.args[0].elts
```

### `P3_empty_register_assertion`

the new not-skipped test stops asserting the register is empty, so it states nothing in a run summary

- File: `tests/test_pending_units.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    assert _pending.PENDING == {}, (
```

New text:

```
    assert _pending.PENDING is not None, (
```

### `P4_is_absent_path_key`

_is_absent resolves a path: key against src rather than the repository root, the coupling R-158 records

- File: `tests/_pending.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return not (REPO_ROOT / key[len("path:") :]).exists()
```

New text:

```
        return not (REPO_ROOT / "src" / key[len("path:") :]).exists()
```

### `C1_at_risk_population_pin`

the at-risk holder population pin is put back to the pre-U28 number

- File: `tests/test_reserved_causes.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    assert (len(literal_holders), len(literal_both)) == (74, 15), (
```

New text:

```
    assert (len(literal_holders), len(literal_both)) == (73, 15), (
```

### `R1_planned_in_restored`

the skills.install registry entry gets planned_in back, so the conformance properties skip it again

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 520 against a baseline of 522
- Kills: 1 (collect-error)
- Note: collection changed: 520 collected against a baseline of 522. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker[skills.install]`

Old text:

```
        module_id="skills",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
```

New text:

```
        module_id="skills",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U28",
```

### `K1_package_data_removed`

the package-data line for the skills is removed, so no wheel carries a SKILL.md

- File: `pyproject.toml`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`, `tests/test_packaging.py`
- Collected: 6225 against a baseline of 6225
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
"cratekit.skills" = ["assets/*/SKILL.md"]
```

New text:

```
(empty)
```

### `K1_composite`

What K1 does hold: break the packaged root's package name so the shipped assets cannot be resolved

- File: `src/cratekit/skills/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 14 against a baseline of 14
- Kills: 9 (killed)
- Composite for: `K1_package_data_removed`
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_this_build_no_longer_ships_disappears`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_every_shipped_skill_is_installed_and_the_set_is_walked_not_listed`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`
  - `tests/test_skills_install.py::test_the_copies_are_copies_and_not_symlinks`
  - `tests/test_skills_install.py::test_the_packaged_root_resolves_through_the_package`

Old text:

```
    return resources.files("cratekit.skills") / "assets"
```

New text:

```
    return resources.files("cratekit.skills") / "skills"
```

### `X1_placeholder_exemption`

the portability scanner stops exempting a placeholder home segment, so a documented path shape is reported

- File: `scripts/scan_repo.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_portability.py::test_placeholder_paths_are_allowed`
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
```

New text:

```
    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        del segment
```

### `X2_mount_rule_removed`

the portability scanner stops looking for a hardcoded volume path at all

- File: `scripts/scan_repo.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_portability.py::test_any_volume_is_caught_not_just_one`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[docs/install.md-Put the library at /Volumes/<a-synthetic-volume>/Music\n]`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[scripts/backup.sh-VOLUME=/Volumes/<a-synthetic-volume>/Music\n]`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[src/cratekit/core/config.py-ROOT = "/Volumes/<a-synthetic-volume>/Music"\n]`

Old text:

```
    for match in _MOUNT.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
        problems.append(
            f"hardcoded volume path {match.group(0)!r}; the library root is "
            f"configuration, not a literal"
        )
```

New text:

```
(empty)
```

