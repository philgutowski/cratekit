# Mutation table: u93-recursive-analysis

Measured by `scripts/mutate.py` on 2026-09-20 21:34 UTC, branch `relay/138` at `419e5e6`. Pass kind: light.

Baseline: green, 9329 collected. pytest invocations for this batch: 32.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 9329 against 9329. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `D1_dotfile` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 2 | killed |
| `D2_is_file` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 1 | killed |
| `D3_suffix` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 1 | killed |
| `D4_default_mode` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 3 | killed |
| `D5_dot_directory` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 2 | killed |
| `D6_link_declined` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 6 | killed |
| `D7_prune_in_place` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 2 | killed |
| `D8_followlinks` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 9329 | 0 (promoted) | zero |
| `D9_onerror` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 1 | killed |
| `D10_sorted_items` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 1 | killed |
| `D11_absolute_id` | `src/cratekit/core/discovery.py` | maintainer | 2 file(s) | 55 | 1 | killed |
| `D12_parent_id` | `src/cratekit/core/discovery.py` | maintainer | 2 file(s) | 55 | 3 | killed |
| `D13_singular` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 2 | killed |
| `D14_link_empty` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 7 | killed |
| `D15_unreadable_empty` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 8 | killed |
| `D16_none_filter` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 23 | killed |
| `D17_and_more` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 1 | killed |
| `D18_strings_shape` | `src/cratekit/core/discovery.py` | maintainer | 2 file(s) | 55 | 1 | killed |
| `D19_resume_half` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 9329 | 0 (promoted) | zero |
| `D20_frozen_links` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 55 | 2 | killed |
| `D21_restamp_flag` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 146 | 11 | killed |
| `D22_restamp_resume_warning` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 146 | 1 | killed |
| `D23_vocals_resume_warning` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `D24_restamp_join` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 146 | 1 | killed |
| `D25_vocals_join` | `src/cratekit/vocals/cli.py` | maintainer | 1 file(s) | 23 | 1 | killed |

## Zero rows and what they owe

- `D8_followlinks` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D19_resume_half` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `D26_as_posix`: _relative returns str(relative_to(...)) instead of as_posix() Dropped because: ranked below the cap because it is INERT on this platform: on darwin PurePath.__str__ already joins with '/', so the mutation is a null control wearing a guard's name and would report a zero that means nothing. The separator claim is a statement about a Windows checkout and this suite cannot measure it here.
- `D27_shown_cap`: SHOWN drops from 5 to 3 Dropped because: ranked below the cap because the coefficient carries no correctness claim: the count in the sentence is measured by D13's neighbour test and the 'and N more' tail by D17, so the only thing 5 decides is how long a line is.
- `D28_unreadable_dedupe`: Drop the set() around unreadable, so one folder erroring twice is named twice Dropped because: ranked below the cap because os.walk calls onerror at most once per unlistable directory, so the dedupe is belt and braces over a producer that was driven and does not produce the duplicate.

## Row definitions

### `D1_dotfile`

Drop the dotfile clause from _is_audio, which is what lets an AppleDouble sidecar become an item

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_an_appledouble_sidecar_under_a_nested_folder_is_skipped`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`

Old text:

```
        path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
```

New text:

```
        path.is_file()
        and path.suffix.lower() in AUDIO_EXTS
```

### `D2_is_file`

is_file becomes exists, so a directory named track.flac becomes an item

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_directory_carrying_an_audio_suffix_is_not_an_item`

Old text:

```
        path.is_file()
        and not path.name.startswith(".")
```

New text:

```
        path.exists()
        and not path.name.startswith(".")
```

### `D3_suffix`

Drop the audio suffix clause, so cover art and text files become items

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_non_audio_suffix_is_not_an_item`

Old text:

```
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
    )
```

New text:

```
        and not path.name.startswith(".")
    )
```

### `D4_default_mode`

Drop the one level early return, so every caller walks the tree whether it asked or not

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 3 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_one_level_scan_reports_no_links_even_when_one_is_there`
  - `tests/test_discovery.py::test_one_level_is_the_default_and_a_subfolder_is_invisible`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_without_the_flag_stays_one_level`

Old text:

```
    if not recursive:
        return Scan(
            items=tuple(sorted(path.name for path in folder.iterdir() if _is_audio(path))),
            skipped_links=(),
            unreadable=(),
        )

```

New text:

```
(empty)
```

### `D5_dot_directory`

Stop pruning dot directories, so .Trashes and .Spotlight-V100 are walked

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_dot_directory_is_not_descended`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`

Old text:

```
            if name.startswith("."):
                continue
            if (here / name).is_symlink():
```

New text:

```
            if (here / name).is_symlink():
```

### `D6_link_declined`

Walk a directory symlink and report nothing, which is the loop hazard and the silent skip at once

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 6 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_symlinked_directory_is_not_walked_and_is_reported`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_frozen_payload_carries_the_mode_and_both_omissions`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
            if (here / name).is_symlink():
                skipped.append(_relative(folder, here / name))
                continue
            kept.append(name)
```

New text:

```
            kept.append(name)
```

### `D7_prune_in_place`

Assign the filtered list to a new name instead of the slice, which leaves os.walk descending everything

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_dot_directory_is_not_descended`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`

Old text:

```
        dirnames[:] = kept
```

New text:

```
        dirnames = kept  # noqa: F841
```

### `D8_followlinks`

Follow links in the walk itself, which is the symlink loop

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 9329 against a baseline of 9329
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
os.walk(root, followlinks=False, onerror=note)
```

New text:

```
os.walk(root, followlinks=True, onerror=note)
```

### `D9_onerror`

Drop the error callback, so an unreadable folder contributes nothing and is never named

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_an_unreadable_folder_is_collected_rather_than_silently_dropped`

Old text:

```
os.walk(root, followlinks=False, onerror=note)
```

New text:

```
os.walk(root, followlinks=False)
```

### `D10_sorted_items`

Return the items in walk order rather than sorted

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_nested_tree_queues_every_file_once_in_sorted_order`

Old text:

```
        items=tuple(sorted(items)),
```

New text:

```
        items=tuple(items),
```

### `D11_absolute_id`

Drop the absolute clause from item_path, so an absolute id discards the frozen folder

- File: `src/cratekit/core/discovery.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_an_absolute_id_is_refused_rather_than_discarding_the_folder`

Old text:

```
    if candidate.is_absolute() or ".." in candidate.parts:
```

New text:

```
    if ".." in candidate.parts:
```

### `D12_parent_id`

Drop the dot dot clause from item_path, so an id walks out of the frozen folder

- File: `src/cratekit/core/discovery.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 3 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_parent_segment_is_refused`
  - `tests/test_discovery.py::test_the_refusal_names_the_folder_it_was_leaving`
  - `tests/test_vocals_cli.py::test_a_vocals_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    if candidate.is_absolute() or ".." in candidate.parts:
        raise _escapes(folder, item_id)
```

New text:

```
    if candidate.is_absolute():
        raise _escapes(folder, item_id)
```

### `D13_singular`

Drop the singular branch, so one declined folder reads as 1 folders

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_unreadable_warning_is_its_own_code_with_its_own_remedy`

Old text:

```
    return f"{count} folder" if count == 1 else f"{count} folders"
```

New text:

```
    return f"{count} folders"
```

### `D14_link_empty`

link_warning reports over an empty list, so every non recursive call carries a false omission

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 7 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_an_error_carrying_no_filename_is_still_reported`
  - `tests/test_discovery.py::test_the_unreadable_warning_is_its_own_code_with_its_own_remedy`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`
  - `tests/test_vocals_cli.py::test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    """What a recursive walk declined to enter, phrased for an envelope."""
    if not paths:
        return None

```

New text:

```
    """What a recursive walk declined to enter, phrased for an envelope."""

```

### `D15_unreadable_empty`

unreadable_warning reports over an empty list, the same false omission on the other code

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 8 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_a_resume_says_what_the_queue_said_from_the_payload_alone`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`
  - `tests/test_vocals_cli.py::test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    """What a recursive walk could not list, phrased for an envelope."""
    if not paths:
        return None

```

New text:

```
    """What a recursive walk could not list, phrased for an envelope."""

```

### `D16_none_filter`

walk_warnings stops dropping the Nones, so an envelope carries a null warning

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 23 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_a_resume_says_what_the_queue_said_from_the_payload_alone`
  - `tests/test_discovery.py::test_an_error_carrying_no_filename_is_still_reported`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_unreadable_warning_is_its_own_code_with_its_own_remedy`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`
  - `tests/test_vocals_cli.py::test_a_file_finalized_with_no_voxlevel_is_scored_once_the_model_is_bound`
  - `tests/test_vocals_cli.py::test_a_folder_with_no_audio_queues_nothing`
  - `tests/test_vocals_cli.py::test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`
  - `tests/test_vocals_cli.py::test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did`
  - `tests/test_vocals_cli.py::test_a_prefixed_file_is_scored_by_analyze_vocals_and_not_skipped`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_queues_every_nested_file_once_in_sorted_order`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    return tuple(one for one in said if one is not None)
```

New text:

```
    return said
```

### `D17_and_more`

Drop the and N more tail, so a warning names five and silently omits the rest

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`

Old text:

```
    return ", ".join(shown) + (f", and {rest} more" if rest else "")
```

New text:

```
    return ", ".join(shown)
```

### `D18_strings_shape`

Drop the shape check on a frozen payload list, so a string payload is read character by character

- File: `src/cratekit/core/discovery.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`

Old text:

```
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(one) for one in value)
```

New text:

```
    return tuple(str(one) for one in value or ())
```

### `D19_resume_half`

warnings_of reads only the links, so an unreadable folder is on the queue and never on the resume

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 9329 against a baseline of 9329
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return walk_warnings(
        _strings(held.get(PAYLOAD_SKIPPED_LINKS)),
        _strings(held.get(PAYLOAD_UNREADABLE)),
    )
```

New text:

```
    return walk_warnings(_strings(held.get(PAYLOAD_SKIPPED_LINKS)))
```

### `D20_frozen_links`

frozen stops recording the declined links, so the resume has nothing to read back

- File: `src/cratekit/core/discovery.py`
- Surface: user
- Subset: test files importing cratekit.core.discovery
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_the_frozen_payload_carries_the_mode_and_both_omissions`
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
        PAYLOAD_SKIPPED_LINKS: list(scan.skipped_links),
```

New text:

```
        PAYLOAD_SKIPPED_LINKS: [],
```

### `D21_restamp_flag`

The restamp queue ignores the flag and always scans one level

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 146 against a baseline of 146
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_appledouble_sidecar_and_a_dot_directory_are_not_items`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_freezes_the_flag_in_the_payload`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_runs_every_nested_item_to_done_and_writes_the_right_file`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_says_which_linked_folders_it_did_not_walk`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_analysis_workers.py::test_an_unreadable_nested_folder_is_named_rather_than_quietly_contributing_nothing`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`
  - `tests/test_analysis_workers.py::test_two_nested_folders_holding_the_same_filename_are_two_items`

Old text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=recursive)
```

New text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=False)
```

### `D22_restamp_resume_warning`

The restamp resume drops the walk's omissions, leaving them on the queue envelope only

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`

Old text:

```
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        if job.handler_key == "analyze.restamp":
```

New text:

```
        if job.handler_key == "analyze.restamp":
```

### `D23_vocals_resume_warning`

The vocals resume drops the walk's omissions, the same hole on the other verb

- File: `src/cratekit/vocals/cli.py`
- Surface: user
- Subset: test files importing cratekit.vocals.cli
- Ran: `tests/test_vocals_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        unscored = _unscored_warning(summary)
```

New text:

```
        unscored = _unscored_warning(summary)
```

### `D24_restamp_join`

The restamp worker joins the item id with the operator instead of the checked rule

- File: `src/cratekit/analysis/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_restamp_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    return folder, discovery.item_path(folder, str(item.item_id))
```

New text:

```
    return folder, folder / item.item_id
```

### `D25_vocals_join`

The vocals worker joins with the operator, the same reversion one file over

- File: `src/cratekit/vocals/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.vocals.cli
- Ran: `tests/test_vocals_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_vocals_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    return folder, discovery.item_path(folder, str(item.item_id))
```

New text:

```
    return folder, folder / item.item_id
```

