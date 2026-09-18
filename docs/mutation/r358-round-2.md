# Mutation table: r358-round-2

Measured by `scripts/mutate.py` on 2026-09-18 20:39 UTC, branch `relay/105` at `abbcbf4`. Pass kind: light.

Baseline: green, 7674 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7674 against 7674. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A3_editor_check` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 54 | 1 | killed |
| `A5_absent_answer` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 54 | 1 | killed |
| `A7_empty_title_message` | `src/cratekit/modules/outbound/tidal_account.py` | maintainer | 1 file(s) | 54 | 3 | killed |
| `S3_gone_from_the_listing` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 45 | 1 | killed |

## Row definitions

### `A3_editor_check`

Drop the editor check, so a playlist the account cannot edit is renamed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 54 against a baseline of 54
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_the_account_cannot_edit_refuses_rather_than_reporting_a_rename`

Old text:

```
        if not callable(retitle):
            raise account.provider_failure(
                LookupError(
                    f"the provider's playlist {playlist_id!r} cannot be retitled by "
                    f"this account"
                ),
                doing,
            )

```

New text:

```
(empty)
```

### `A5_absent_answer`

Accept an explicit not found as a rename that landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 54 against a baseline of 54
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_deleted_between_the_open_and_the_edit_is_the_items_cause`

Old text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False or accepted is _ABSENT:
```

New text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False:
```

### `A7_empty_title_message`

Reword the empty-title refusal, never append to it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 54 against a baseline of 54
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[   ]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[\n]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[]`

Old text:

```
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
```

New text:

```
                f"the playlist {playlist_id} was given a blank title, which the "
                f"client would read as an instruction to keep the current one",
```

### `S3_gone_from_the_listing`

Drop the listed check, so a playlist the account no longer lists is pending

- File: `src/cratekit/sync/playlists.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_the_pass_never_listed_is_not_pending_at_all`

Old text:

```
        if listed.get(identity) and not is_swept_name(listed[identity])
```

New text:

```
        if not is_swept_name(listed.get(identity) or "")
```

