# Mutation table: u337-moved

Measured by `scripts/mutate.py` on 2026-11-24 20:32 UTC, branch `cloud/986-every-guard-killed-at-survey-still-killed` at `59cc5358`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23349 collected. pytest invocations for this batch: 16.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `474653bacb22`, and this tree is at `59cc5358d37a`).

Subset baselines: 5, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23349 against 23349. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u125.P1_drop_module_entry` | `tests/ratchets/reserved_causes/core.py` | maintainer | 1 file(s) | 229 | 2 | killed |
| `u125.P3_pin_without_tree_member` | `tests/ratchets/reserved_causes/core.py` | maintainer | 1 file(s) | 229 | 2 | killed |
| `u125.P4_literal_added_to_pinned_module` | `tests/ratchets/reserved_causes/acquire.py` | maintainer | 1 file(s) | 229 | 2 | killed |
| `r658-b.S1_adoption_unreadable_revert` | `tests/test_adoption.py` | user | 1 file(s) | 613 | 1 | killed |
| `r658-b.S2_adoption_unreadable_stamp` | `tests/test_adoption.py` | user | 1 file(s) | 613 | 1 | killed |
| `r658-b.S5_adoption_swap` | `tests/test_adoption.py` | user | 1 file(s) | 613 | 1 | killed |
| `u253.L1_relative_per_node` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 1 | killed |
| `u199.M8_stale_table_applied` | `tests/test_restart_and_residual_files.py` | maintainer | 1 file(s) | 48 | 4 | killed |
| `r658-d.D1_an_undo_comes_back` | `tests/test_restore.py` | maintainer | 1 file(s) | 3 | 1 | killed |

## Row definitions

### `u125.P1_drop_module_entry`

Delete the core/backup_facts.py entry from PINNED_KEBAB_LITERALS_BY_MODULE

- File: `tests/ratchets/reserved_causes/core.py`
- Source: `u125.json`, row `P1_drop_module_entry`
- Moved: moved by 2b058f2c (U296, refactor(u296)) from tests/_pinned_reserved_populations.py to tests/ratchets/reserved_causes/core.py, which _pinned_reserved_populations.py reads back into PINNED_KEBAB_LITERALS_BY_MODULE; the same guard because it is the same core/backup_facts.py entry with the same six literals in the KEBAB_LITERALS table that feeds that name, and deleting it leaves the pins short of a module the tree holds
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    'core/backup_facts.py': [
        'grant-path-access',
        'never-recorded',
        'recorded-in-the-future',
        'repair-backup-facts',
        'upgrade-cratekit',
        'utf-8',
    ],

```

New text:

```
(empty)
```

### `u125.P3_pin_without_tree_member`

Add a fake module pin the tree does not hold

- File: `tests/ratchets/reserved_causes/core.py`
- Source: `u125.json`, row `P3_pin_without_tree_member`
- Moved: moved by 2b058f2c (U296, refactor(u296)) from tests/_pinned_reserved_populations.py to tests/ratchets/reserved_causes/core.py; core/artifacts.py has since left the pins, so the fake pin is anchored after the first KEBAB_LITERALS entry, core/active_taxonomy.py; the fake module is named under core/ because the reader now refuses a key filed under another package's file at import, and a core path keeps the planted pin reaching the same comparison of the pins with the tree that the original row broke
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    'core/active_taxonomy.py': ['config-unusable', 'library-volume-unmounted', 'utf-8'],
    'core/backup_facts.py': [

```

New text:

```
    'core/active_taxonomy.py': ['config-unusable', 'library-volume-unmounted', 'utf-8'],
    'core/zz_fake_u125.py': ['not-a-real-cause'],
    'core/backup_facts.py': [

```

### `u125.P4_literal_added_to_pinned_module`

Add a kebab literal to acquire/adapter.py that the module does not carry

- File: `tests/ratchets/reserved_causes/acquire.py`
- Source: `u125.json`, row `P4_literal_added_to_pinned_module`
- Moved: moved by 2b058f2c (U296, refactor(u296)) from tests/_pinned_reserved_populations.py to tests/ratchets/reserved_causes/acquire.py; the same guard because it is the same acquire/adapter.py entry of the KEBAB_LITERALS table, read back into PINNED_KEBAB_LITERALS_BY_MODULE, and the planted literal is one the module does not carry
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    'acquire/adapter.py': [
        'adapter-broken',
        'auth-failed',
        'choose-known-adapter',
        'install-adapter',

```

New text:

```
    'acquire/adapter.py': [
        'adapter-broken',
        'auth-failed',
        'zz-fake-literal-u125',
        'choose-known-adapter',
        'install-adapter',

```

### `r658-b.S1_adoption_unreadable_revert`

Drop the scoped unreadable digest around revert_tags; the refusal it pins must not be produced

- File: `tests/test_adoption.py`
- Source: `r658-b.json`, row `S1_adoption_unreadable_revert`
- Moved: rewritten in place by ad92ab53 (U310, refactor(u310)), which split digest_of out of adopt/revert.py into adopt/revert_changed.py, so the scoped patch now names adopt_changed rather than adopt_revert; the same guard because it is the same scoped unreadable digest around revert_tags in test_a_file_that_cannot_be_READ_is_not_reported_as_somebody_elses_bytes, now patched where the read happens
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_file_that_cannot_be_READ_is_not_reported_as_somebody_elses_bytes`

Old text:

```
        unreadable.setattr(adopt_changed, "digest_of", lambda _p: "")
        report = adopt_revert.revert_tags(cfg)

```

New text:

```
        report = adopt_revert.revert_tags(cfg)

```

### `r658-b.S2_adoption_unreadable_stamp`

Drop the scoped unreadable digest around the stamping write

- File: `tests/test_adoption.py`
- Source: `r658-b.json`, row `S2_adoption_unreadable_stamp`
- Moved: rewritten in place by ad92ab53 (U310, refactor(u310)), which moved digest_of to adopt/revert_changed.py so the patch names adopt_changed, and the stamping call became the _adopt helper (9f781441, U310, and 060353bf, U332), which still calls adopt_revert.write_tag_with_record; the same guard because it is the same scoped unreadable digest around the stamping write in test_a_stamping_read_that_FAILS_is_recorded_as_its_own_state
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_stamping_read_that_FAILS_is_recorded_as_its_own_state`

Old text:

```
        unreadable.setattr(adopt_changed, "digest_of", lambda _p: "")
        record, landed = _adopt(cfg, path, written="Adopted", entry_id="e1")

```

New text:

```
        record, landed = _adopt(cfg, path, written="Adopted", entry_id="e1")

```

### `r658-b.S5_adoption_swap`

Drop the scoped byte swap between the two reads

- File: `tests/test_adoption.py`
- Source: `r658-b.json`, row `S5_adoption_swap`
- Moved: rewritten in place by ad92ab53 (U310, refactor(u310)), which moved digest_of to adopt/revert_changed.py, so the swap is now patched onto adopt_changed; the same guard because it is the same scoped byte swap between the two reads in test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught`

Old text:

```
        swapping.setattr(adopt_changed, "digest_of", swap_the_bytes_after_the_first_read)

```

New text:

```
(empty)
```

### `u253.L1_relative_per_node`

_location_codec_offenders: compute the relative path inside the node loop again, main's shape, so a run makes one relative_to per node

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L1_relative_per_node`
- Moved: rewritten in place by 56bea733 (U299, test(u299)), which parses through the shared cached parsed() rather than ast.parse, and then by b28fac9a (U299), which reads the text first and skips a file that never spells quote; the same guard because relative is still computed once per file in _location_codec_offenders before the node walk, and moving it inside the walk again makes one relative_to per node, which test_the_sweep_computes_each_relative_path_once_per_file counts
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_locations.py::test_the_sweep_computes_each_relative_path_once_per_file`

Old text:

```
        relative = path.relative_to(root).as_posix()
        text = path.read_text()
        if "quote" not in unicodedata.normalize("NFKC", text):
            continue
        for node in ast.walk(parsed(text)):

```

New text:

```
        text = path.read_text()
        if "quote" not in unicodedata.normalize("NFKC", text):
            continue
        for node in ast.walk(parsed(text)):
            relative = path.relative_to(root).as_posix()

```

### `u199.M8_stale_table_applied`

_problems: compare with a stale table rather than report it, so an entry whose old text is in no moved paragraph excuses nothing and passes

- File: `tests/test_restart_and_residual_files.py`
- Source: `u199.json`, row `M8_stale_table_applied`
- Moved: rewritten in place by 899ee372 (U313, refactor(u313)), which folded _problems and _lost_paragraphs into one _lost with a check flag; the same guard because _lost still returns the stale table entries before comparing, and skipping that return applies a stale rewording rather than reporting it, which test_a_stale_rewording_fails_rather_than_excusing_nothing catches
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry0-in the split base 0 times]`
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry1-times, not once]`
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry2-its new text is not in r301.md]`
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry3-its new text is not in r999.md]`

Old text:

```
    if stale and check:
        return stale

```

New text:

```
    if False:
        return stale

```

### `r658-d.D1_an_undo_comes_back`

Put a body monkeypatch.undo() back into the restore retry test; the ban must name it

- File: `tests/test_restore.py`
- Source: `r658-d.json`, row `D1_an_undo_comes_back`
- Moved: the comment the old text began with was cut by 21a862f4 (U300, refactor(u300)), which kept the code of test_round6_a_retry_after_a_partial_failure_still_runs; the same guard because the planted monkeypatch.undo() goes into the same retry test at the same point, before the second attempt's log is written, and the ban in tests/test_isolation_survives_undo.py scans every test file's text for it
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_no_test_undoes_the_shared_monkeypatch`

Old text:

```
    assert stranded.read_bytes() == b"the first attempt's log"
    log.write_bytes(b"the second attempt's log")

```

New text:

```
    assert stranded.read_bytes() == b"the first attempt's log"
    monkeypatch.undo()
    log.write_bytes(b"the second attempt's log")

```

