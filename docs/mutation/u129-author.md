# Mutation table: u129-author

Measured by `scripts/mutate.py` on 2026-10-10 22:30 UTC, branch `HEAD` at `dad0fea9`. Pass kind: light.

Baseline: green, 13605 collected. pytest invocations for this batch: 21.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/Library/Application Support/cratekit (387101 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 13605 against 13605. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A1_gate_after_enqueue` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 0 | 0 | refused |
| `A2_gate_ask_dropped` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 0 | 0 | refused |
| `A3_abort_still_writes` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `A4_archive_raise_fails_landing` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 77 | 2 | killed |
| `A5_archive_return_discarded` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 77 | 2 | killed |
| `A6_archive_notes_not_on_envelope` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 77 | 2 | killed |
| `A7_with_archive_omits_digest` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 13605 | 1 (promoted) | killed |
| `A8_land_writes_without_remote` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 23 | 1 | killed |
| `A9_land_without_provider_check` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 23 | 1 | killed |
| `A10_export_set_without_library_mounted` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 23 | 1 | killed |
| `A11_export_archive_without_library_mounted` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 23 | 1 | killed |
| `A12_archive_backfill_swallows_all` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `A13_job_lookup_uses_today` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 23 | 2 | killed |
| `A14_backfill_apply_hides_made` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 0 | 0 | refused |
| `A15_archive_backfill_hides_filed` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 0 | 0 | refused |
| `A16_soft_skip_re_raises` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 0 | 0 | refused |
| `A17_empty_add_still_writes` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 23 | 3 | killed |
| `A18_frozen_name_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 23 | 2 | killed |
| `A19_plan_archive_always_none` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 13605 | 3 (promoted) | killed |
| `A20_apply_archive_skips_rename` | `src/cratekit/modules/outbound/sets.py` | user | 2 file(s) | 77 | 4 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `A26_unnamed_skips_without_warning`: Queue an unnamed local set without the account unnamed warning Dropped because: ranked below the cap after archive backfill naming took the slot; the unnamed path stays covered by its own test
- `A21_inspiration_scan_skips_sort`: Leave inspiration playlists unsorted Dropped because: display order only; no wrong outcome word
- `A22_backfill_waiting_quiet`: Drop waiting sets from the archive backfill shown context Dropped because: ranked below the cap; the soft skip and apply naming rows cover the user facing paths
- `A23_tracklist_after_apply`: Write the tracklist before the account playlist apply Dropped because: ordering only; the gate before queue and the soft skip are the load bearing guards
- `A24_abort_outcome_no_op`: Report no_op when the account gate aborts even though the set queued Dropped because: outcome word taste; the abort still queues and writes nothing, covered by A3
- `A25_session_scan_skipped`: Skip the session log fallback in job lookup Dropped because: frozen name and naming day cover the October backfill case

## Row definitions

### `A1_gate_after_enqueue`

Ask the account gate after the set is queued, so an explicit first refusal leaves a job a resume queues again

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 0 against a baseline of 23
- Kills: 0 (refused)
- Note: old text is not present in the target; the row cannot be applied. Copy the text out of the file rather than retyping it.

Old text:

```
            # THE ACCOUNT GATE BEFORE THE QUEUE (U129). An explicit gate always
            # stops the first run; asking it after enqueue left a job that the
            # resume queued a second time with the same tracks.
            account_notes, built, option = _ask_account_playlist(
                ctx,
                cfg,
                name=playlist.name if playlist.name else "",
                rows=result.rows if tracks else (),
            )
            if tracks:
                payload = {
                    SOURCE: held.ref,
                    TRACKS: tracks,
                    CALLS: result.calls,
                    UNREACHED: result.unreached,
                    PARTS: result.parts,
                    PAGE: dict(held.page),
                }
                # U129. Freeze the INSPIRATION name so the account playlist and
                # the landing's playlist agree, even when they run on different days.
                if playlist.name:
                    payload[PLAYLIST_NAME] = playlist.name
                job = jobs.enqueue(
                    store,
                    handler_key=ctx.entry.handler_key,
                    payload=payload,
           
... truncated ...
```

New text:

```
            if tracks:
                payload = {
                    SOURCE: held.ref,
                    TRACKS: tracks,
                    CALLS: result.calls,
                    UNREACHED: result.unreached,
                    PARTS: result.parts,
                    PAGE: dict(held.page),
                }
                # U129. Freeze the INSPIRATION name so the account playlist and
                # the landing's playlist agree, even when they run on different days.
                if playlist.name:
                    payload[PLAYLIST_NAME] = playlist.name
                job = jobs.enqueue(
                    store,
                    handler_key=ctx.entry.handler_key,
                    payload=payload,
                    cfg=cfg,
                    item_ids=tuple(tracks),
                )
            # THE ACCOUNT GATE BEFORE THE QUEUE (U129). An explicit gate always
            # stops the first run; asking it after enqueue left a job that the
            # resume queued a second time with the same tracks.
            account_notes, built, option = _ask_account_playlist(
                ctx,
                cfg,
                name=playlist.name if playlist.
... truncated ...
```

### `A2_gate_ask_dropped`

Drop the account gate ask so an explicit write is never refused

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 0 against a baseline of 23
- Kills: 0 (refused)
- Note: old text is not present in the target; the row cannot be applied. Copy the text out of the file rather than retyping it.

Old text:

```
    option = ctx.gate.require(spec, plan=built.payload, context=built.shown)
    notes = tuple(set_cli._unmatched_warnings(built.planned))
    return notes, built, option

```

New text:

```
    notes = tuple(set_cli._unmatched_warnings(built.planned))
    return notes, built, "apply"

```

### `A3_abort_still_writes`

Apply the account playlist even when the gate said abort

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_an_abort_on_the_account_gate_queues_the_set_and_writes_no_playlist`

Old text:

```
    if option != "apply" or not built.writes:
        return notes, built.payload

```

New text:

```
    if not built.writes:
        return notes, built.payload

```

### `A4_archive_raise_fails_landing`

Let an account archive raise escape the landing write after rows are in the library

- File: `src/cratekit/intake/land_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_failure_after_write_is_a_warning`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:
        message = (
            exc.cause.message if isinstance(exc, CratekitError) else f"{type(exc).__name__}: {exc}"
        )
        return [
            {
                "code": LAND_ARCHIVE_FAILED,
                "message": (
                    f"the account archive could not finish after the landing wrote "
                    f"({message}); the batch is in the library, run crate export "
                    f"archive over the set once the account can be reached"
                ),
            }
        ]
    return list(warnings)

```

New text:

```
    _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    return list(warnings)

```

### `A5_archive_return_discarded`

Discard apply_archive warnings so a not-renamed return is silent on the landed envelope

- File: `src/cratekit/intake/land_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_surfaces_changed_since_plan_as_a_warning`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:

```

New text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
        warnings = []
    except Exception as exc:

```

### `A6_archive_notes_not_on_envelope`

Drop archive notes from the landed envelope warnings

- File: `src/cratekit/intake/land_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope`

Old text:

```
    warnings.extend(favorites_notes(payload, landed.collection))
    warnings.extend(archive_notes)
    kept = landed.collection.set_playlist

```

New text:

```
    warnings.extend(favorites_notes(payload, landed.collection))
    kept = landed.collection.set_playlist

```

### `A7_with_archive_omits_digest`

Fold archive items into the landing without changing the digest

- File: `src/cratekit/intake/land_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 13605 against a baseline of 13605
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/intake/test_set_progress.py::test_the_watcher_reports_the_bytes_written_while_the_download_runs`

Old text:

```
    identity = {
        "land": payload["digest"],
        "archive": archived.payload["digest"],
    }

```

New text:

```
    identity = {
        "land": payload["digest"],
    }

```

### `A8_land_writes_without_remote`

Declare intake.land without the remote write surface the archive needs

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_intake_land_declares_remote_and_provider_for_the_archive`

Old text:

```
        writes=frozenset({"xml", "files", "db_tree", "remote"}),

```

New text:

```
        writes=frozenset({"xml", "files", "db_tree"}),

```

### `A9_land_without_provider_check`

Drop credential.provider from intake.land so doctor never names the archive's session

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_intake_land_declares_remote_and_provider_for_the_archive`

Old text:

```
            "library.paths_resolved",
            "credential.provider",
        ),

```

New text:

```
            "library.paths_resolved",
        ),

```

### `A10_export_set_without_library_mounted`

Drop library.mounted from export.set so the INSPIRATION backfill opens a database doctor never checked

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_set_and_archive_declare_library_mounted_for_backfill`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.set.confirm",

```

New text:

```
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.set.confirm",

```

### `A11_export_archive_without_library_mounted`

Drop library.mounted from export.archive so the no-name backfill opens library paths doctor never checked

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_set_and_archive_declare_library_mounted_for_backfill`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.archive.confirm",

```

New text:

```
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.archive.confirm",

```

### `A12_archive_backfill_swallows_all`

Catch Exception around plan_archive so a credential refusal becomes a warning

- File: `src/cratekit/export/set_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_archive_backfill_refuses_a_credential_error`

Old text:

```
        except CratekitError as exc:
            # Soft skip per set, as a landing's _plan_set_archive does. A
            # CredentialError (not a CratekitError) still refuses the verb.
            warnings.append(
                {
                    "code": "export-archive-backfill-refused",
                    "message": f"{name}: {exc.cause.message}",
                }
            )
            continue

```

New text:

```
        except Exception as exc:
            warnings.append(
                {
                    "code": "export-archive-backfill-refused",
                    "message": f"{name}: {exc}",
                }
            )
            continue

```

### `A13_job_lookup_uses_today`

Rebuild a pre-freeze set name from today so a job from another day never matches

- File: `src/cratekit/export/set_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_job_for_inspiration_name_matches_a_set_from_another_day`
  - `tests/test_u129_set_account_playlist.py::test_job_for_inspiration_name_uses_the_local_day_at_half_past_eleven`

Old text:

```
            made = _naming_day(job)
            # Local calendar day: a UTC stamp after about 20:00 Eastern is the
            # next UTC day, and .date() on it would miss the set (U129).
            on = made.astimezone().date() if made is not None else None
            if set_name(set_playlist.playlist_name(words, on=on)) == wanted:
                return job

```

New text:

```
            if set_name(set_playlist.playlist_name(words)) == wanted:
                return job

```

### `A14_backfill_apply_hides_made`

Drop the naming of already made playlists when a later backfill apply fails

- File: `src/cratekit/export/set_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 0 against a baseline of 23
- Kills: 0 (refused)
- Note: old text is not present in the target; the row cannot be applied. Copy the text out of the file rather than retyping it.

Old text:

```
    except Exception as exc:
        # Name what already landed so a mid-loop failure does not hide it (U129).
        # CredentialError is a plain Exception, not a CratekitError.
        if not applied:
            raise
        made = ", ".join(applied)
        again = (
            "the playlists named above are on the account; resume or "
            "run crate export set again for the rest"
        )
        if isinstance(exc, CratekitError):
            raise refuse(
                exc.cause.reason,
                f"before this failed the backfill already made {made}. {exc.cause.message}",
                remedy=exc.cause.remediation.remedy,
                steps=(*exc.cause.remediation.steps, again),
                scope=Scope.RUN,
                retryable=exc.cause.retryable,
                origin=_SET,
                detail={**dict(exc.cause.detail), "applied": list(applied)},
                inner=exc.cause,
            ) from exc
        raise refuse(
            "internal-error",
            f"before this failed the backfill already made {made}. "
            f"{type(exc).__name__}: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            steps=(again,),
     
... truncated ...
```

New text:

```
    except Exception:
        raise

```

### `A15_archive_backfill_hides_filed`

Drop the naming of already archived playlists when a later archive backfill apply fails

- File: `src/cratekit/export/set_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 0 against a baseline of 23
- Kills: 0 (refused)
- Note: old text is not present in the target; the row cannot be applied. Copy the text out of the file rather than retyping it.

Old text:

```
    except Exception as exc:
        # Name renames already done so a mid-loop failure does not hide them (U129).
        if not filed:
            raise
        made = ", ".join(filed)
        again = (
            "the playlists named above are already archived on the account; "
            "resume or run crate export archive again for the rest"
        )
        if isinstance(exc, CratekitError):
            raise refuse(
                exc.cause.reason,
                f"before this failed the backfill already archived {made}. "
                f"{exc.cause.message}",
                remedy=exc.cause.remediation.remedy,
                steps=(*exc.cause.remediation.steps, again),
                scope=Scope.RUN,
                retryable=exc.cause.retryable,
                origin=_ARCHIVE,
                detail={**dict(exc.cause.detail), "archived": list(filed)},
                inner=exc.cause,
            ) from exc
        raise refuse(
            "internal-error",
            f"before this failed the backfill already archived {made}. "
            f"{type(exc).__name__}: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            steps=(again,),
            scope=Scope
... truncated ...
```

New text:

```
    except Exception:
        raise

```

### `A16_soft_skip_re_raises`

Re-raise a plan_from_wanted refusal so a missing credential takes the set away

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 0 against a baseline of 23
- Kills: 0 (refused)
- Note: old text is not present in the target; the row cannot be applied. Copy the text out of the file rather than retyping it.

Old text:

```
    except CratekitError as exc:
        return (
            (
                {
                    "code": ACCOUNT_UNREACHABLE,
                    "message": (
                        f"the account playlist {name!r} was not planned "
                        f"({exc.cause.reason}: {exc.cause.message}); the set will "
                        f"still be queued, run crate export set over its "
                        f"tracklist once the account is reachable"
                    ),
                },
            ),
            None,
            None,
        )

```

New text:

```
    except CratekitError:
        raise

```

### `A17_empty_add_still_writes`

Force writes true when every row of the set is unmatched

- File: `src/cratekit/modules/outbound/sets.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 3 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_a_rerun_of_export_set_plans_nothing_when_every_matched_track_is_on_it`
  - `tests/test_u129_set_account_playlist.py::test_a_rerun_of_intake_set_plans_nothing_when_the_playlist_already_holds_the_tracks`
  - `tests/test_u129_set_account_playlist.py::test_a_set_with_no_matches_makes_nothing_and_says_so`

Old text:

```
        return bool(self.add)

```

New text:

```
        return True

```

### `A18_frozen_name_ignored`

Ignore the frozen INSPIRATION name on the job and recompute it

- File: `src/cratekit/intake/set_playlist.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_set_backfill_names_playlists_already_made_when_a_credential_fails`
  - `tests/test_u129_set_account_playlist.py::test_export_set_backfill_names_playlists_already_made_when_one_fails`

Old text:

```
    return str(payload.get(intake_cli.PLAYLIST_NAME) or "").strip()

```

New text:

```
    return ""

```

### `A19_plan_archive_always_none`

A set landing never plans the account archive

- File: `src/cratekit/intake/land_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 13605 against a baseline of 13605
- Kills: 3 (killed)
- Promoted: subset killed 0, full suite killed 3
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_with_prefix_and_year_folder`

Old text:

```
    try:
        return set_cli.plan_archive_named(cfg, name, pass_name=pass_name)
    except CratekitError:
        # Soft: the landing still lands; archive can run later via export archive.
        return None

```

New text:

```
    return None

```

### `A20_apply_archive_skips_rename`

Skip the playlist rename so DOWNLOADED never lands on the account

- File: `src/cratekit/modules/outbound/sets.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 77 against a baseline of 77
- Kills: 4 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_with_prefix_and_year_folder`
  - `tests/test_u129_set_account_playlist.py::test_export_archive_backfill_names_playlists_already_archived_when_a_credential_fails`
  - `tests/test_u129_set_account_playlist.py::test_export_archive_backfill_names_playlists_already_archived_when_one_fails`
  - `tests/test_u129_set_account_playlist.py::test_export_archive_prefixes_the_set_in_its_year_folder`

Old text:

```
    account.rename_playlist(playlist.remote_id, planned.to)
    done.marked = True

```

New text:

```
    done.marked = False

```

