# Mutation table: u337-reanchor

Measured by `scripts/mutate.py` on 2026-11-25 04:59 UTC, branch `HEAD` at `5671db8c8`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23364 collected. pytest invocations for this batch: 34.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-25 04:59 UTC for commit `5671db8c8101`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 14, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23364 against 23364. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1709.M25_fallback_identity_fold` | `src/cratekit/acquire/match_list.py` | user | 2 file(s) | 87 | 2 | killed |
| `r664.G5_key_not_read_from_the_tag_head` | `src/cratekit/acquire/match_library.py` | user | 1 file(s) | 613 | 2 | killed |
| `r731-c.M25_planned_sub_outside_the_set` | `src/cratekit/adopt/plan.py` | maintainer | 1 file(s) | 41 | 1 | killed |
| `r780-b.B2_worker_asks_the_entry_bucket` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 8 | killed |
| `u119.G2_source_folder_counts` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119.G3_two_sources_first_wins` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u196.S1_any_word` | `scripts/board.py` | maintainer | 1 file(s) | 7 | 1 | killed |
| `u196.S2_case_sensitive` | `scripts/board.py` | maintainer | 1 file(s) | 7 | 2 | killed |
| `u219.M1_accept_fingerprint` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 24 | 2 | killed |
| `u223.M1_composite` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 176 | 3 | killed |
| `u250.M1_three_opens_again` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 51 | 49 | killed |
| `u28-skills-independent.X2_mount_rule_removed` | `scripts/scan_repo.py` | user | 1 file(s) | 161 | 4 | killed |
| `u39-author-full.R1_filename_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u39-author-full.R2_title_fallback_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `u41-author-full.R1_filename_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u41-naming-independent.B2_filename_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u79-b.B7_identity_without_version` | `src/cratekit/acquire/match_list.py` | user | 2 file(s) | 87 | 2 | killed |
| `r504-a.A11_boundary_refuses` | `src/cratekit/label/cli.py` | user | 2 file(s) | 290 | 5 | killed |
| `u59.G2_local_names_targets` | `tests/_source_guards.py` | maintainer | 7 file(s) | 2865 | 3 | killed |

## Row definitions

### `r1709.M25_fallback_identity_fold`

the upload question keys the folded title

- File: `src/cratekit/acquire/match_list.py`
- Source: `r1709.json`, row `M25_fallback_identity_fold`
- Moved: 0293c2eb (U305, refactor(u305)) split match.py and moved Wanted.folded_row into acquire/match_list.py, the one identity dict both the upload question and the search question are keyed by; the title is still keyed by title_identity on that line, so folding it makes two emoji titles one question as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`, `tests/test_intake_missing_search.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_upload_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`

Old text:

```
            "artist": fold(self.artist), "title": title_identity(self.title),

```

New text:

```
            "artist": fold(self.artist), "title": fold(self.title),

```

### `r664.G5_key_not_read_from_the_tag_head`

Stop reading the key off a head found only inside the title tag, the first draft's precedence the review reversed

- File: `src/cratekit/acquire/match_library.py`
- Source: `r664.json`, row `G5_key_not_read_from_the_tag_head`
- Moved: 0293c2eb (U305) moved the library index reader into acquire/match_library.py, and bf177ec8 (U327) then put the title tag's head ahead of the stem's; the guard is the same, the tag's head is still read for the key, so reading the stem's head alone breaks it as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-head-found-only-in-the-tag-carries-the-key-when-the-stem-has-none]`
  - `tests/test_match_states.py::test_the_tag_head_outranks_the_stem_head_and_both_outrank_the_initialkey_tag`

Old text:

```
    written_key = tag_head.get("key") or head.get("key")

```

New text:

```
    written_key = head.get("key")

```

### `r731-c.M25_planned_sub_outside_the_set`

a planned sub outside the bucket's competing subs is no longer let through unasked

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-c.json`, row `M25_planned_sub_outside_the_set`
- Moved: 258b33aa (U340, fix(u340)) put a kept_beside line between this guard and the held line the old text ended on; the guard is the same early return for a planned sub outside the competing set, deleted the same way
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_planned_sub_outside_the_competing_set_is_never_withheld`

Old text:

```
    if sub not in competing:
        return NO_COMPETING_PLACE
    kept
```

New text:

```
    kept
```

### `r780-b.B2_worker_asks_the_entry_bucket`

the worker asks the plan's rule of the entry's own bucket rather than the bucket the move names, so every tree path move is refused as one the plan does not make

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B2_worker_asks_the_entry_bucket`
- Moved: 76b5dcf2 (U339) added moved= and 258b33aa (U340) added elsewhere= to the worker's standing_in call; the same call asks the bucket the move names, and calling standing (the entry's own bucket) in its place, keeping elsewhere which standing still takes, is the same substitution
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 8 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`
  - `tests/test_adopt_move.py::test_a_track_filed_somewhere_nobody_was_shown_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_tree_path_move_is_checked_by_the_worker_in_the_bucket_it_names`
  - `tests/test_adopt_move.py::test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`

Old text:

```
        now = move_engine.standing_in(
            entry, move.bucket, current.placements, declared, tree=current.tree, refused=refused,
            elsewhere=move_engine.elsewhere_of(claimed, entry), moved=moved,
        )

```

New text:

```
        now = move_engine.standing(
            entry, current.placements, declared, tree=current.tree,
            elsewhere=move_engine.elsewhere_of(claimed, entry),
        )

```

### `u119.G2_source_folder_counts`

source_playlist: a source playlist holding no live track is mirrored, emptying every Favorites

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G2_source_folder_counts`
- Moved: 6ecbd2c0 (U302, refactor(u302)) folded the nested empty check into one condition, len(live) == 1 and live_members(...), with the empty refusal as the branch after it; dropping the live_members half returns an empty source as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_smart_playlist_or_an_emptied_playlist_of_the_source_name_is_not_the_source`

Old text:

```
    if len(live) == 1 and live_members(db, str(live[0].ID)):

```

New text:

```
    if len(live) == 1:

```

### `u119.G3_two_sources_first_wins`

source_playlist: two live sources, the first is taken

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G3_two_sources_first_wins`
- Moved: 6ecbd2c0 (U302, refactor(u302)) folded the nested check into one condition on the same len(live) == 1 test; widening it to >= 1 takes the first of two live sources as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_two_source_playlists_are_refused_rather_than_one_chosen`

Old text:

```
    if len(live) == 1 and live_members(db, str(live[0].ID)):

```

New text:

```
    if len(live) >= 1 and live_members(db, str(live[0].ID)):

```

### `u196.S1_any_word`

search_residuals: match a heading carrying any word rather than every word

- File: `scripts/board.py`
- Source: `u196.json`, row `S1_any_word`
- Moved: e5e9252b (U314, feat(u314)) made search_residuals read every ledger file as (number, title, path) hits, so the every word test is the same all() over hit[1]; any() matches a heading with any word as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 7 against a baseline of 7
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_every_word_must_appear_in_any_case_newest_first[words1-25-found1-0]`

Old text:

```
all(w in hit[1].casefold() for w in wanted)
```

New text:

```
any(w in hit[1].casefold() for w in wanted)
```

### `u196.S2_case_sensitive`

search_residuals: compare without folding case, so a heading in capitals is missed

- File: `scripts/board.py`
- Source: `u196.json`, row `S2_case_sensitive`
- Moved: e5e9252b (U314, feat(u314)) made search_residuals read every ledger file as (number, title, path) hits; the same comparison now folds hit[1], and dropping the fold misses a heading in capitals as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 7 against a baseline of 7
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_every_word_must_appear_in_any_case_newest_first[words0-25-found0-0]`
  - `tests/test_board_residual_search.py::test_every_word_must_appear_in_any_case_newest_first[words1-25-found1-0]`

Old text:

```
all(w in hit[1].casefold() for w in wanted)
```

New text:

```
all(w in hit[1] for w in wanted)
```

### `u219.M1_accept_fingerprint`

accept_as_it_stands: record no fingerprint, so an accepted INBOX still meets the restore latch (round two's first hold)

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `M1_accept_fingerprint`
- Moved: 3f0175b1 (R2056) put the Membership class after accept_as_it_stands, so the old text's trailing def declared_membership no longer follows; the same record_fingerprint call, the only one in rebuild.py, is deleted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`

Old text:

```
        convergence.record_fingerprint(cfg, handle)
    finally:

```

New text:

```
    finally:

```

### `u223.M1_composite`

What M1 holds with the staged report fallback gone too: the shipped bug, through the verb and the printed resume

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M1_composite`
- Moved: c474d295 (U306, refactor(u306)) gave the intent and the staged report one record reader, _item_record, and shortened the docstrings inside the span; the same two edits, staged_path no longer keeping the intent and staged_report reading nothing, applied to the span as it reads at HEAD
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
                entry.name == RENAME_INTENT_FILENAME
                and entry.is_file()
                and not entry.is_symlink()
            ):
                continue
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    elif directory.is_symlink() or directory.exists():
        # ``rmtree`` refuses a link and a plain file, loudly, rather than this
        # call deciding to remove or follow one.
        shutil.rmtree(directory)
    config.mkdir_private(directory)
    return directory / _report_name(ordinal)


def intent_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where one item's rename intent lives: in its staging directory.

    Written before the rename, so a kill between the rename and the row
    flipping to done leaves the resume the file the item BECAME, never a guess
    from the folder. It outlives the attempt (U223) and is removed only where
    known false: a rename that did not land, or a source still a file.
    """
    return _staging_dir(cfg, job_id, ordinal) / RENAME_INTENT_FILENAME


def record_rename_intent(cfg: config.Config, job, item, targ
... truncated ...
```

New text:

```
                entry.name == "never-kept.json"
                and entry.is_file()
                and not entry.is_symlink()
            ):
                continue
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    elif directory.is_symlink() or directory.exists():
        # ``rmtree`` refuses a link and a plain file, loudly, rather than this
        # call deciding to remove or follow one.
        shutil.rmtree(directory)
    config.mkdir_private(directory)
    return directory / _report_name(ordinal)


def intent_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where one item's rename intent lives: in its staging directory.

    Written before the rename, so a kill between the rename and the row
    flipping to done leaves the resume the file the item BECAME, never a guess
    from the folder. It outlives the attempt (U223) and is removed only where
    known false: a rename that did not land, or a source still a file.
    """
    return _staging_dir(cfg, job_id, ordinal) / RENAME_INTENT_FILENAME


def record_rename_intent(cfg: config.Config, job, item, target: P
... truncated ...
```

### `u250.M1_three_opens_again`

read_truth: go back to the three single field readers, three opens a file, the regression the card removes

- File: `src/cratekit/write/rebuild.py`
- Source: `u250.json`, row `M1_three_opens_again`
- Moved: e64715d6 (U340, feat(u340)) added second_genre to the one read_tags call in read_truth; going back to a reader per field, the three single field readers and read_tag for the fourth, opens the file once per field as the old regression did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`
- Collected: 51 against a baseline of 51
- Kills: 49 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_derivation_over_n_files_makes_n_opens`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[empty.flac-]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.aiff-FORM\x00\x00\x00\x04AIFX]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.m4a-\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.mp3-content1]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[truncated.wav-RIFF$\x00\x00\x00WAVEfmt ]`
  - `tests/test_rebuild_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.flac]`
  - ... and 34 more, see the JSON sidecar

Old text:

```
    values = tags.read_tags(path, _TRUTH_FIELDS)
    return Truth(
        location=str(path),
        genre=values["genre"],
        energy=tags.whole_number(values["energylevel"], field="energylevel", path=path),
        voxlevel=tags.whole_number(values["voxlevel"], field="voxlevel", path=path),
        second_genre=values["secondgenre"],
    )
```

New text:

```
    return Truth(
        location=str(path),
        genre=tags.read_genre_from_file(path),
        energy=tags.read_energy_from_file(path),
        voxlevel=tags.read_vox_from_file(path),
        second_genre=tags.read_tag(path, "secondgenre"),
    )
```

### `u28-skills-independent.X2_mount_rule_removed`

the portability scanner stops looking for a hardcoded volume path at all

- File: `scripts/scan_repo.py`
- Source: `u28-skills-independent.json`, row `X2_mount_rule_removed`
- Moved: fc06797b (U957) added a segments.add line inside the mount loop for the shape only tokens; the volume path report is the same problems.append, deleted here while the segment collection, another guard, is kept
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 161 against a baseline of 161
- Kills: 4 (killed)
- Killed:
  - `tests/test_portability.py::test_any_volume_is_caught_not_just_one`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[docs/install.md-Put the library at /Volumes/BigAudioDrive/Music\n]`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[scripts/backup.sh-VOLUME=/Volumes/BigAudioDrive/Music\n]`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[src/cratekit/core/config.py-ROOT = "/Volumes/BigAudioDrive/Music"\n]`

Old text:

```
        segments.add(segment.lower())
        problems.append(
            f"hardcoded volume path {match.group(0)!r}; the library root is "
            f"configuration, not a literal"
        )

```

New text:

```
        segments.add(segment.lower())

```

### `u39-author-full.R1_filename_source_dropped`

Head recovery loses the filename source and keeps only the title fallback

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R1_filename_source_dropped`
- Moved: bf177ec8 (U327, feat(u327)) reversed the head order in _spec_for so the title tag's head is read first and the filename's second, since analyze adopt corrects the tag and never renames the file; the filename is still a head source, now the second, so dropping it leaves the title tag the only one as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-filename-head-alone-is-enough]`

Old text:

```
    head = (
        naming.parse_head(title, template=template)
        or naming.parse_head(path.name, template=template)
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

### `u39-author-full.R2_title_fallback_dropped`

Head recovery loses the title fallback that heals the tag then rename crash window

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R2_title_fallback_dropped`
- Moved: bf177ec8 (U327, feat(u327)) reversed the head order in _spec_for so the title tag's head is read first and the filename's second, since analyze adopt corrects the tag and never renames the file; the title tag is still a head source, now the first, so dropping it loses the head recovered from the title tag when the filename lost it, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-head-is-recovered-from-the-title-tag]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-head-in-the-title-tag-stays-out-of-the-body]`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[the-title-head-wins-over-the-filename-head]`

Old text:

```
    head = (
        naming.parse_head(title, template=template)
        or naming.parse_head(path.name, template=template)
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

### `u41-author-full.R1_filename_head_source_dropped`

The filename is no longer a head source, leaving the title as the only one

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `R1_filename_head_source_dropped`
- Moved: bf177ec8 (U327, feat(u327)) reversed the head order in _spec_for so the title tag's head is read first and the filename's second, since analyze adopt corrects the tag and never renames the file; the same two lines in the other order, and dropping the filename line leaves the title as the only source as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-filename-head-alone-is-enough]`

Old text:

```
        naming.parse_head(title, template=template)
        or naming.parse_head(path.name, template=template)

```

New text:

```
        naming.parse_head(title, template=template)

```

### `u41-naming-independent.B2_filename_head_source_dropped`

The filename is no longer a head source, so only a tag-carried head is recovered

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B2_filename_head_source_dropped`
- Moved: bf177ec8 (U327, feat(u327)) reversed the head order in _spec_for so the title tag's head is read first and the filename's second, since analyze adopt corrects the tag and never renames the file; the filename line is now the second operand, so it becomes or None rather than None, which drops the filename as a head source as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-filename-head-alone-is-enough]`

Old text:

```
        or naming.parse_head(path.name, template=template)

```

New text:

```
        or None

```

### `u79-b.B7_identity_without_version`

The question is keyed without the version, so two versions are one item

- File: `src/cratekit/acquire/match_list.py`
- Source: `u79-b.json`, row `B7_identity_without_version`
- Moved: 0293c2eb (U305, refactor(u305)) split match.py and moved Wanted.folded_row, which candidates.identity returns, into acquire/match_list.py; the version key is the same field, so blanking it makes two versions one question as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_acquire_fallback.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_upload_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`

Old text:

```
            "version": self.version_key,

```

New text:

```
            "version": "",

```

### `r504-a.A11_boundary_refuses`

The verb boundary no longer catches the shortfall, so it is refused as an unreadable listing

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A11_boundary_refuses`
- Moved: The same guard at a new text: b4468190 (U308, the second pass) folded the broad except Exception and the CratekitError re-raise into catalogue.translated, leaving the HeartsShortfall clause of favourite_tracks_or_refuse the try's only handler, so the recorded deletion of that clause no longer parses. Narrowing translated's passing to CratekitError alone has the shortfall refused as the unreadable listing, as the recorded deletion had it through the broad except, and the clause is never reached
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`
- Collected: 290 against a baseline of 290
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        ), passing=(CratekitError, catalogue.HeartsShortfall)):

```

New text:

```
        ), passing=(CratekitError,)):

```

### `u59.G2_local_names_targets`

Recognize only a bare Name target, reopening the four shadowing routes

- File: `tests/_source_guards.py`
- Source: `u59.json`, row `G2_local_names_targets`
- Moved: 76f82246 (U326, perf(u326)) replaced ast.walk with the module's _walk in _local_names, which docs/mutation/u326.json row W3_u59_g2_local_names_targets measured at this text; the same bind loop, and binding a bare Name target alone reopens the shadowing routes as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_reserved_causes.py`, `tests/test_review_queue.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_pool_sizing.py`, `tests/modules/test_reports.py`
- Collected: 2865 against a baseline of 2865
- Kills: 3 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[for target-    for TABLE, _ in rows:\n        return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[nested unpacking-    (a, [TABLE, b]) = rows[0]\n    return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[tuple unpacking-    TABLE, meta = rows[0]\n    return TABLE.get(COLUMN, 0)\n]`

Old text:

```
        for node in _walk(target):
            if isinstance(node, ast.Name):
                found.add(node.id)
```

New text:

```
        if isinstance(target, ast.Name):
            found.add(target.id)
```

