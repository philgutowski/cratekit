# Mutation table: u27-round-8-independent

Measured by `scripts/mutate.py` on 2026-08-14 13:19 UTC, branch `unit/u27-setup-wizard-and-doctor` at `44ced7e`. Pass kind: full.

Baseline: green, 3445 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3445 against 3445. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C1_immutable_valueerror` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1264 | 1 | killed |
| `C2_probe_valueerror` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1264 | 1 | killed |
| `C3_spelled_bytes` | `src/cratekit/core/cause.py` | maintainer | 11 file(s) | 3445 | 0 (promoted) | zero |
| `C4_two_path_order` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `C5_two_path_probe_mode` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `C6_two_path_unmeasured` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1264 | 1 | killed |
| `C7_erofs_measured` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `C8_two_path_precondition` | `src/cratekit/core/cause.py` | maintainer | 11 file(s) | 1264 | 22 | killed |
| `C9_copy_error_name` | `src/cratekit/core/cause.py` | maintainer | 11 file(s) | 3445 | 0 (promoted) | zero |
| `C10_copy_error_side` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1264 | 1 | killed |
| `C11_copy_error_probe_mode` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `C12_copy_error_order` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `C13_name_db_top_only` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3445 | 1 (promoted) | killed |
| `C14_cantopen_probe_mode` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `W1_handle_path_none` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `W2_canary_ignores_caller_path` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `W3_canary_no_name_the_database` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 847 | 1 | killed |
| `W4_canary_no_detail_path` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `W5_canary_message_no_path` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 847 | 1 | killed |
| `W6_open_db_no_path` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 3445 | 0 (promoted) | zero |
| `D1_finding_no_classification` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 858 | 2 | killed |
| `D2_finding_no_remedy_override` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 858 | 2 | killed |
| `D3_finding_cause_any_status` | `src/cratekit/cli/doctor.py` | maintainer | 4 file(s) | 3445 | 0 (promoted) | zero |
| `D4_finding_cause_overwrites` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 3445 | 0 (promoted) | zero |
| `D5_finding_error_compared` | `src/cratekit/cli/doctor.py` | maintainer | 4 file(s) | 3445 | 0 (promoted) | zero |
| `S1_act_always_generic` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 248 | 5 | killed |
| `S2_template_write_no_error` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 248 | 1 | killed |
| `S3_unreachable_root_hardcoded` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 248 | 2 | killed |
| `S4_resolve_root_no_error` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 3445 | 0 (promoted) | zero |
| `S5_already_there_no_error` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 3445 | 0 (promoted) | zero |
| `E1_mount_detail_swapped` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 858 | 1 | killed |
| `E2_identity_verdict_green` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 858 | 3 | killed |
| `E3_found_at_dropped` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 858 | 1 | killed |
| `E4_path_missing_reads_ok` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 472 | 2 | killed |
| `E5_unmounted_reads_foreign` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 472 | 4 | killed |
| `E6_write_table_shares_read` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 472 | 3 | killed |
| `E7_readonly_sentence_is_permission` | `src/cratekit/cli/render.py` | user | 2 file(s) | 690 | 1 | killed |
| `E8_no_mount_enumeration` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 472 | 5 | killed |
| `W2_composite_wrong_file` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 847 | 1 | killed |
| `C7_composite_kind` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1264 | 3 | killed |
| `C14_composite_probe_blind` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1264 | 3 | killed |
| `D4_composite_reason` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 858 | 2 | killed |

## Zero rows and what they owe

- `C3_spelled_bytes` (maintainer facing): maintainer facing, composite not required
- `C4_two_path_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `C5_two_path_probe_mode` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `C7_erofs_measured` (user facing): paired with `C7_composite_kind`, which killed 3
- `C9_copy_error_name` (maintainer facing): maintainer facing, composite not required
- `C11_copy_error_probe_mode` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `C12_copy_error_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `C14_cantopen_probe_mode` (user facing): paired with `C14_composite_probe_blind`, which killed 3
- `W1_handle_path_none` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `W2_canary_ignores_caller_path` (user facing): paired with `W2_composite_wrong_file`, which killed 1
- `W4_canary_no_detail_path` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `W6_open_db_no_path` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D3_finding_cause_any_status` (maintainer facing): maintainer facing, composite not required
- `D4_finding_cause_overwrites` (user facing): paired with `D4_composite_reason`, which killed 2
- `D5_finding_error_compared` (maintainer facing): maintainer facing, composite not required
- `S4_resolve_root_no_error` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S5_already_there_no_error` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `C15_copy_error_empty_entry`: Drop the empty-entry guard inside _from_copy_error's loop Dropped because: ranked below the cap: same guard family as C9 and C10, both measured, and an empty triple is not a shape shutil produces
- `C16_chain_depth`: Cap _chain at one link Dropped because: ranked below the cap: C13 measures the same coupling from the writing side, which is the side round 8 changed
- `C17_permission_errnos`: Remove EPERM from PERMISSION_ERRNOS Dropped because: ranked below the cap: a pre-existing constant untouched by round 8, and its consumers are exercised through C7 and C8
- `W7_handle_path_falsy`: Return str(spelled) unconditionally in handle_path, so an empty URL becomes the string None Dropped because: ranked below the cap: W1 already measures whether anything asserts on handle_path's answer
- `W8_open_db_name_the_database`: Remove name_the_database from open_db Dropped because: ranked below the cap: the author's own round 8 comment declares this site kills nothing today, so the row buys a number already claimed
- `D6_cause_detail_key`: Put the refusal kind under the detail path key Dropped because: ranked below the cap: D3 and D4 already measure whether anything reads the constructed cause at all
- `D7_cause_scope`: Widen the constructed cause's scope from RUN Dropped because: ranked below the cap: scope is a pre-existing contract with its own suite, untouched by round 8
- `S6_act_spacing`: Drop the leading space _act puts before its clause Dropped because: ranked below the cap: cosmetic, and S1 measures whether the clause is asserted at all
- `E9_identity_unavailable_verdict`: Flip IDENTITY_UNAVAILABLE to OK in the identity verdict table Dropped because: ranked below the cap: E2 samples the same table on the two rows the unmounted-versus-moved distinction turns on
- `E10_foreign_volume_remedy`: Give FOREIGN_VOLUME the RUN_SETUP remedy Dropped because: ranked below the cap: E2 and E5 already sample this table and this resolver branch
- `C4_composite_no_path_at_all`: COMPOSITE for C4 and C5: _refused_path answers None, so no refusal is claimed at all Dropped because: ranked below the cap: C6 and C8 are the family's composite and are measured at 1 and 22, so what the two-path measurement holds is already a number
- `C12_composite_copy_blind`: COMPOSITE for C9, C11 and C12: _from_copy_error answers None always Dropped because: ranked below the cap: C10 is the family's composite and is measured at 1, which is the count that says one test pins the copytree classification
- `W6_composite_no_path_anywhere`: COMPOSITE for W1, W4 and W6: neither the caller nor the handle supplies a path Dropped because: ranked below the cap: W3 and W5 are the family's composite and are measured at 1 each, and W2_composite_wrong_file measures the same property from the value side at 1
- `S5_composite_no_error_anywhere`: COMPOSITE for S4 and S5: _Wizard.note drops the exception at all three call sites at once Dropped because: ranked below the cap: S1, S2 and S3 are the family's composite and are measured at 5, 1 and 2, so the wizard's hand-off is pinned at the site that writes to the library volume and unpinned at the two that only read
- `D3_composite_status_gate`: COMPOSITE for D3 and D5: a cause is attached to an OK finding and read back Dropped because: ranked below the cap and MAINTAINER surface, which METHOD says gets one line rather than a composite

## Row definitions

### `C1_immutable_valueerror`

Drop the ValueError catch in _immutable, so an embedded-null path raises out of the refusal handler

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1264 against a baseline of 1264
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_path_no_filesystem_can_represent_is_answered_rather_than_raised`

Old text:

```
        flags = getattr(os.lstat(path), "st_flags", 0)
    except (OSError, ValueError):
```

New text:

```
        flags = getattr(os.lstat(path), "st_flags", 0)
    except OSError:
```

### `C2_probe_valueerror`

Drop the ValueError catch in _probe, so an embedded-null path raises out of the refusal handler

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1264 against a baseline of 1264
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_path_no_filesystem_can_represent_is_answered_rather_than_raised`

Old text:

```
    except OSError as probe:
        return _from_os_error(probe)
    except ValueError:
        return None
```

New text:

```
    except OSError as probe:
        return _from_os_error(probe)
```

### `C3_spelled_bytes`

Drop the bytes branch in _spelled, so a bytes filename renders as its repr

- File: `src/cratekit/core/cause.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if isinstance(candidate, bytes):
        return os.fsdecode(candidate)
    return str(candidate)
```

New text:

```
    return str(candidate)
```

### `C4_two_path_order`

Reverse _refused_of_two's candidate order, so the source is asked before the destination

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for candidate in (exc.filename2, exc.filename):
        spelled = _spelled(candidate)
        if spelled is None:
            continue
        if _probe(spelled, writing=False) is not None:
            return spelled
    return fallback
```

New text:

```
    for candidate in (exc.filename, exc.filename2):
        spelled = _spelled(candidate)
        if spelled is None:
            continue
        if _probe(spelled, writing=False) is not None:
            return spelled
    return fallback
```

### `C5_two_path_probe_mode`

Probe the two named paths for WRITE rather than read in _refused_of_two

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if _probe(spelled, writing=False) is not None:
            return spelled
    return fallback
```

New text:

```
        if _probe(spelled, writing=True) is not None:
            return spelled
    return fallback
```

### `C6_two_path_unmeasured`

Drop the measurement in _refused_of_two: name the first path present rather than the one actually refused

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1264 against a baseline of 1264
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_two_path_refusal_names_the_side_the_operating_system_refused`

Old text:

```
        if spelled is None:
            continue
        if _probe(spelled, writing=False) is not None:
            return spelled
    return fallback
```

New text:

```
        if spelled is None:
            continue
        return spelled
    return fallback
```

### `C7_erofs_measured`

Measure which of two paths EROFS refused, instead of taking the destination unmeasured

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)
```

New text:

```
        return AccessRefusal(kind=AccessKind.READ_ONLY, path=_refused_of_two(exc, path))
```

### `C8_two_path_precondition`

Drop the both-paths-present precondition, so a one-path permission error is re-measured

- File: `src/cratekit/core/cause.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1264 against a baseline of 1264
- Kills: 22 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_check_whose_probe_raises_becomes_a_failed_check_not_a_lost_report`
  - `tests/test_doctor.py::test_a_commit_hook_that_exists_and_cannot_be_read_is_not_a_missing_hook`
  - `tests/test_doctor.py::test_a_commondir_that_cannot_be_read_is_reported_rather_than_swallowed`
  - `tests/test_doctor.py::test_a_copy_that_gave_up_on_one_member_is_classified_by_its_paths`
  - `tests/test_doctor.py::test_a_finding_that_carries_a_refusal_is_classified_where_it_is_built`
  - `tests/test_doctor.py::test_a_git_marker_that_cannot_be_read_is_not_a_marker_that_names_nothing`
  - `tests/test_doctor.py::test_a_library_root_this_account_cannot_traverse_is_reported_not_raised`
  - `tests/test_doctor.py::test_a_sealed_state_database_answers_with_its_path_and_an_act`
  - `tests/test_doctor.py::test_a_two_path_refusal_names_the_side_the_operating_system_refused`
  - `tests/test_doctor.py::test_a_verb_that_lets_a_config_error_escape_is_classified_too`
  - `tests/test_doctor.py::test_an_active_template_that_exists_and_cannot_be_read_is_not_a_missing_one`
  - `tests/test_doctor.py::test_both_verbs_answer_a_real_permission_with_an_act_the_user_can_perform[configuration-directory]`
  - `tests/test_doctor.py::test_both_verbs_answer_a_real_permission_with_an_act_the_user_can_perform[library-root]`
  - `tests/test_doctor.py::test_doctor_still_answers_every_check_over_an_unreachable_root`
  - `tests/test_doctor.py::test_doctors_configuration_check_does_not_call_an_intact_file_corrupt`
  - ... and 7 more, see the JSON sidecar

Old text:

```
        if exc.filename2 is not None and exc.filename is not None:
            path = _refused_of_two(exc, path)
```

New text:

```
        path = _refused_of_two(exc, path)
```

### `C9_copy_error_name`

Drop the class-name half of the shutil.Error identity check in _from_copy_error

- File: `src/cratekit/core/cause.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if type(exc).__module__ != "shutil" or type(exc).__name__ != "Error":
```

New text:

```
    if type(exc).__module__ != "shutil":
```

### `C10_copy_error_side`

Ask the DESTINATION of each failed copytree member rather than the source

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1264 against a baseline of 1264
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_copy_that_gave_up_on_one_member_is_classified_by_its_paths`

Old text:

```
        found = _probe(str(entry[0]), writing=False)
```

New text:

```
        found = _probe(str(entry[1]), writing=False)
```

### `C11_copy_error_probe_mode`

Probe a failed copytree member for WRITE rather than read

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        found = _probe(str(entry[0]), writing=False)
        if found is not None:
            return found
```

New text:

```
        found = _probe(str(entry[0]), writing=True)
        if found is not None:
            return found
```

### `C12_copy_error_order`

Ask _from_copy_error LAST, so shutil.Error is answered by the OSError rule that sees no errno

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        found = (
            _from_copy_error(current)
            or _from_os_error(current)
            or _from_database_error(current)
        )
```

New text:

```
        found = (
            _from_os_error(current)
            or _from_database_error(current)
            or _from_copy_error(current)
        )
```

### `C13_name_db_top_only`

Record the database path on the handed-in exception only, not along the declared chain

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_rb_writer_db.py::test_a_sealed_database_is_a_grant_rather_than_an_order_to_overwrite_it`

Old text:

```
    for current in _chain(exc):
        try:
            setattr(current, DATABASE_PATH_ATTRIBUTE, spelled)
        except AttributeError:  # pragma: no cover - defensive
            continue
    return exc
```

New text:

```
    try:
        setattr(exc, DATABASE_PATH_ATTRIBUTE, spelled)
    except AttributeError:  # pragma: no cover - defensive
        pass
    return exc
```

### `C14_cantopen_probe_mode`

Probe a named database for WRITE even when the driver said SQLITE_CANTOPEN

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return _probe(str(path), writing=not name.startswith("SQLITE_CANTOPEN"))
```

New text:

```
    return _probe(str(path), writing=True)
```

### `W1_handle_path_none`

handle_path answers None always, so a handed-in handle's failure names no file

- File: `src/cratekit/core/rb_writer.py`
- Surface: user
- Subset: test files importing cratekit.core.rb_writer
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    database = getattr(getattr(db, "engine", None), "url", None)
    spelled = getattr(database, "database", None)
    return str(spelled) if spelled else None
```

New text:

```
    return None
```

### `W2_canary_ignores_caller_path`

The canary reads the handle's engine URL and ignores the path its caller opened

- File: `src/cratekit/core/rb_writer.py`
- Surface: user
- Subset: test files importing cratekit.core.rb_writer
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        named = path if path is not None else handle_path(db)
```

New text:

```
        named = handle_path(db)
```

### `W3_canary_no_name_the_database`

Drop the name_the_database hand-off in the canary, so a chmod 000 database is unclassifiable

- File: `src/cratekit/core/rb_writer.py`
- Surface: user
- Subset: test files importing cratekit.core.rb_writer
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 847 against a baseline of 847
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_sealed_database_is_a_grant_rather_than_an_order_to_overwrite_it`

Old text:

```
        if named is not None:
            name_the_database(exc, named)
```

New text:

```
(empty)
```

### `W4_canary_no_detail_path`

Drop the path out of the canary refusal's machine-readable detail

- File: `src/cratekit/core/rb_writer.py`
- Surface: user
- Subset: test files importing cratekit.core.rb_writer
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            detail={"path": str(named)} if named is not None else None,
```

New text:

```
            detail=None,
```

### `W5_canary_message_no_path`

Reword the canary refusal so its sentence no longer names the database file

- File: `src/cratekit/core/rb_writer.py`
- Surface: user
- Subset: test files importing cratekit.core.rb_writer
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 847 against a baseline of 847
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_sealed_database_is_a_grant_rather_than_an_order_to_overwrite_it`

Old text:

```
            f"the rekordbox database{where} opened but could not be read as "
            f"expected: {exc}",
```

New text:

```
            f"the rekordbox database could not be read as expected after it "
            f"opened: {exc}",
```

### `W6_open_db_no_path`

open_db stops telling the canary which file it opened

- File: `src/cratekit/core/rb_writer.py`
- Surface: user
- Subset: test files importing cratekit.core.rb_writer
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    canary(
        db,
        write_intent=require_closed,
        force_cloud_canary=force_cloud_canary,
        path=target,
    )
```

New text:

```
    canary(
        db,
        write_intent=require_closed,
        force_cloud_canary=force_cloud_canary,
    )
```

### `D1_finding_no_classification`

Invert the entry guard so a Finding carrying an exception is never classified

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 858 against a baseline of 858
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_finding_that_carries_a_refusal_is_classified_where_it_is_built`
  - `tests/test_doctor.py::test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access`

Old text:

```
        if self.error is None:
            return
```

New text:

```
        if self.error is not None:
            return
```

### `D2_finding_no_remedy_override`

Keep the branch's hard coded remedy token instead of the one the refusal kind chooses

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 858 against a baseline of 858
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_finding_that_carries_a_refusal_is_classified_where_it_is_built`
  - `tests/test_doctor.py::test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access`

Old text:

```
        if self.remedy is not refusal.remedy:
            object.__setattr__(self, "remedy", refusal.remedy)
```

New text:

```
(empty)
```

### `D3_finding_cause_any_status`

Build a cause for any status, not only for a failing finding

- File: `src/cratekit/cli/doctor.py`
- Surface: maintainer
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.cause is None and self.status is Status.FAIL:
```

New text:

```
        if self.cause is None:
```

### `D4_finding_cause_overwrites`

Overwrite a cause the branch already built, rather than only filling an absent one

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.cause is None and self.status is Status.FAIL:
```

New text:

```
        if self.status is Status.FAIL:
```

### `D5_finding_error_compared`

Let the carried exception take part in Finding equality and repr

- File: `src/cratekit/cli/doctor.py`
- Surface: maintainer
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    error: BaseException | None = field(default=None, compare=False, repr=False)
```

New text:

```
    error: BaseException | None = field(default=None)
```

### `S1_act_always_generic`

_act stops asking render.access_note and always closes with the generic clause

- File: `src/cratekit/cli/setup.py`
- Surface: user
- Subset: test files importing cratekit.cli.setup
- Ran: `tests/test_doctor.py`
- Collected: 248 against a baseline of 248
- Kills: 5 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access`
  - `tests/test_doctor.py::test_the_seed_reports_a_state_directory_it_could_not_look_into`
  - `tests/test_doctor.py::test_the_seed_reports_a_write_it_was_refused_rather_than_filing_a_defect`
  - `tests/test_doctor.py::test_the_taxonomy_seed_reports_an_unreachable_root_rather_than_raising`
  - `tests/test_doctor.py::test_the_wizard_refuses_an_unreachable_ancestor_rather_than_filing_a_defect`

Old text:

```
    note = render.access_note(exc)
    return f" {note}" if note is not None else f" {otherwise}"
```

New text:

```
    return f" {otherwise}"
```

### `S2_template_write_no_error`

The wizard's template WRITE site stops handing its exception to the finding

- File: `src/cratekit/cli/setup.py`
- Surface: user
- Subset: test files importing cratekit.cli.setup
- Ran: `tests/test_doctor.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access`

Old text:

```
            + _act(exc, "Choose a library root this account can already write"),
            Remedy.GRANT_PATH_ACCESS,
            error=exc,
```

New text:

```
            + _act(exc, "Choose a library root this account can already write"),
            Remedy.GRANT_PATH_ACCESS,
```

### `S3_unreachable_root_hardcoded`

Put the hard coded Full Disk Access advice back into _unreachable_root

- File: `src/cratekit/cli/setup.py`
- Surface: user
- Subset: test files importing cratekit.cli.setup
- Ran: `tests/test_doctor.py`
- Collected: 248 against a baseline of 248
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_taxonomy_seed_reports_an_unreachable_root_rather_than_raising`
  - `tests/test_doctor.py::test_the_wizard_refuses_an_unreachable_ancestor_rather_than_filing_a_defect`

Old text:

```
        f"defect and it is not a missing drive."
    ) + _act(exc, "Choose a library root this account can already reach")
```

New text:

```
        f"defect and it is not a missing drive. Grant this interpreter access "
        f"to the path, or choose a library root it can already reach"
    )
```

### `S4_resolve_root_no_error`

The wizard's mount-resolution branch stops handing its exception to the finding

- File: `src/cratekit/cli/setup.py`
- Surface: user
- Subset: test files importing cratekit.cli.setup
- Ran: `tests/test_doctor.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            + _unreachable_root(str(cfg.library.root), exc),
            Remedy.GRANT_PATH_ACCESS,
            error=exc,
```

New text:

```
            + _unreachable_root(str(cfg.library.root), exc),
            Remedy.GRANT_PATH_ACCESS,
```

### `S5_already_there_no_error`

The wizard's already-there probe branch stops handing its exception to the finding

- File: `src/cratekit/cli/setup.py`
- Surface: user
- Subset: test files importing cratekit.cli.setup
- Ran: `tests/test_doctor.py`
- Collected: 3445 against a baseline of 3445
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            + _act(exc, "Choose a library root this account can already reach"),
            Remedy.GRANT_PATH_ACCESS,
            error=exc,
```

New text:

```
            + _act(exc, "Choose a library root this account can already reach"),
            Remedy.GRANT_PATH_ACCESS,
```

### `E1_mount_detail_swapped`

Swap the NOT_MOUNTED and MOUNTED_ELSEWHERE sentences, conflating unmounted with moved

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 858 against a baseline of 858
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`

Old text:

```
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
```

New text:

```
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
```

### `E2_identity_verdict_green`

Report the identity check GREEN for an absent and for a relocated volume

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 858 against a baseline of 858
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_mounted_elsewhere_is_one_problem_reported_once`
  - `tests/test_doctor.py::test_an_unmounted_volume_never_reports_a_matching_identity`
  - `tests/test_doctor.py::test_the_identity_check_never_reports_green_over_an_identity_that_did_not_match`

Old text:

```
            preflight.MountState.NOT_MOUNTED: (Status.INFO, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.INFO, None),
```

New text:

```
            preflight.MountState.NOT_MOUNTED: (Status.OK, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.OK, None),
```

### `E3_found_at_dropped`

Stop telling the user where a relocated volume actually is

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 858 against a baseline of 858
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`

Old text:

```
    if status.state is preflight.MountState.MOUNTED_ELSEWHERE:
        where = f" (configured root {status.configured_root}, found at {status.found_at})"
```

New text:

```
(empty)
```

### `E4_path_missing_reads_ok`

A matching identity with an absent root resolves to OK instead of LIBRARY_PATH_MISSING

- File: `src/cratekit/core/preflight.py`
- Surface: user
- Subset: test files importing cratekit.core.preflight
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 472 against a baseline of 472
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unresolved_session_is_never_reported_clean_because_its_disk_is_gone`
  - `tests/test_preflight.py::test_the_right_volume_with_a_missing_library_subdirectory_is_its_own_cause`

Old text:

```
            MountState.OK if root_exists else MountState.LIBRARY_PATH_MISSING,
```

New text:

```
            MountState.OK,
```

### `E5_unmounted_reads_foreign`

An absent volume resolves to FOREIGN_VOLUME instead of NOT_MOUNTED

- File: `src/cratekit/core/preflight.py`
- Surface: user
- Subset: test files importing cratekit.core.preflight
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 472 against a baseline of 472
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`
  - `tests/test_doctor.py::test_the_wizard_refuses_to_write_when_the_volume_is_not_mounted_at_all`
  - `tests/test_preflight.py::test_a_volume_that_is_not_mounted_refuses_with_its_own_cause`
  - `tests/test_preflight.py::test_the_three_refusals_are_distinguishable_from_each_other`

Old text:

```
        MountState.NOT_MOUNTED if not root_exists else MountState.FOREIGN_VOLUME,
```

New text:

```
        MountState.FOREIGN_VOLUME,
```

### `E6_write_table_shares_read`

Make the write table refuse LIBRARY_PATH_MISSING, the row it differs from the read table on

- File: `src/cratekit/core/preflight.py`
- Surface: user
- Subset: test files importing cratekit.core.preflight
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 472 against a baseline of 472
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_renamed_library_folder_on_the_right_volume_is_written_not_refused`
  - `tests/test_doctor.py::test_every_mount_outcome_permits_exactly_what_it_is_declared_to[_STATE_WRITABLE-expected1]`
  - `tests/test_doctor.py::test_the_two_tables_differ_in_three_rows_and_every_one_is_a_read_signal_removed`

Old text:

```
    MountState.LIBRARY_PATH_MISSING: Reach.ALWAYS,
```

New text:

```
    MountState.LIBRARY_PATH_MISSING: Reach.NEVER,
```

### `E7_readonly_sentence_is_permission`

Give a read only volume the permission-grant sentence, the defect round 8 closed one layer up

- File: `src/cratekit/cli/render.py`
- Surface: user
- Subset: test files importing cratekit.cli.render
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 690 against a baseline of 690
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access`

Old text:

```
        cause_module.AccessKind.READ_ONLY: (
            "The volume holding it is mounted read only, so it refuses every writer on "
            "this machine and no permission grant can change that. Remount it read write, "
            "release the medium's write protection, or write somewhere else"
        ),
```

New text:

```
        cause_module.AccessKind.READ_ONLY: (
            "The operating system refused this account, which is a permission to grant "
            "rather than a defect in this program. Grant this interpreter access to the "
            "path, or choose one it can already reach"
        ),
```

### `E8_no_mount_enumeration`

Stop enumerating mounts, so a relocated volume can never be reported as relocated

- File: `src/cratekit/core/preflight.py`
- Surface: user
- Subset: test files importing cratekit.core.preflight
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 472 against a baseline of 472
- Kills: 5 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_mounted_elsewhere_is_one_problem_reported_once`
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`
  - `tests/test_doctor.py::test_the_wizard_refuses_to_write_when_the_volume_is_mounted_somewhere_else`
  - `tests/test_preflight.py::test_a_volume_mounted_elsewhere_refuses_and_names_where_it_actually_is`
  - `tests/test_preflight.py::test_the_three_refusals_are_distinguishable_from_each_other`

Old text:

```
    for candidate in enumerate_mounts():
        if identity_of(Path(candidate)) == recorded_identity:
```

New text:

```
    for candidate in ():
        if identity_of(Path(candidate)) == recorded_identity:
```

### `W2_composite_wrong_file`

COMPOSITE for W2: the canary names a file that is not the one it opened

- File: `src/cratekit/core/rb_writer.py`
- Surface: user
- Subset: test files importing cratekit.core.rb_writer
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 847 against a baseline of 847
- Kills: 1 (killed)
- Composite for: `W2_canary_ignores_caller_path`
- Killed:
  - `tests/test_rb_writer_db.py::test_a_sealed_database_is_a_grant_rather_than_an_order_to_overwrite_it`

Old text:

```
        named = path if path is not None else handle_path(db)
```

New text:

```
        named = (str(path) + "-not-this-file") if path is not None else handle_path(db)
```

### `C7_composite_kind`

COMPOSITE for C7: a read only volume is classified as a permission to grant

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1264 against a baseline of 1264
- Kills: 3 (killed)
- Composite for: `C7_erofs_measured`
- Killed:
  - `tests/test_doctor.py::test_a_finding_that_carries_a_refusal_is_classified_where_it_is_built`
  - `tests/test_doctor.py::test_a_read_only_volume_is_not_sent_to_full_disk_access`
  - `tests/test_doctor.py::test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access`

Old text:

```
        return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)
```

New text:

```
        return AccessRefusal(kind=AccessKind.PERMISSION, path=path)
```

### `C14_composite_probe_blind`

COMPOSITE for C14: the probe answers None for every refusal, so nothing is measured at all

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1264 against a baseline of 1264
- Kills: 3 (killed)
- Composite for: `C14_cantopen_probe_mode`
- Killed:
  - `tests/test_doctor.py::test_a_copy_that_gave_up_on_one_member_is_classified_by_its_paths`
  - `tests/test_doctor.py::test_a_sealed_state_database_answers_with_its_path_and_an_act`
  - `tests/test_doctor.py::test_a_two_path_refusal_names_the_side_the_operating_system_refused`

Old text:

```
    try:
        handle = os.open(path, flags)
    except OSError as probe:
        return _from_os_error(probe)
```

New text:

```
    try:
        handle = os.open(path, flags)
    except OSError:
        return None
```

### `D4_composite_reason`

COMPOSITE for D4: the cause a finding gains carries the wrong reason slug

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 858 against a baseline of 858
- Kills: 2 (killed)
- Composite for: `D4_finding_cause_overwrites`
- Killed:
  - `tests/test_doctor.py::test_a_finding_that_carries_a_refusal_is_classified_where_it_is_built`
  - `tests/test_doctor.py::test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access`

Old text:

```
                Cause(
                    reason=refusal.reason,
```

New text:

```
                Cause(
                    reason="internal-error",
```

