# Developing Cratekit

For working on Cratekit itself. To run it against a library, the
[README](../README.md) installs it and [`GUIDE.md`](GUIDE.md) runs it.

Develop in an editable environment inside the checkout, kept apart from the
pipx copy you run against a real library.

## Setup

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pre-commit install --hook-type pre-commit --hook-type commit-msg
cp .scan-identity.example .scan-identity
```

- Activate `.venv` in the shell you commit from: the hooks call `ruff` and
  `python3` from your PATH.
- Name both hook types. The `pre-commit` hook runs the repository scan and
  ruff; the `commit-msg` hook runs `scripts/board.py closing`, which a bare
  `pre-commit install` never installs.
- List your own drive, account and machine names in `.scan-identity`
  (gitignored). The scan catches path-shaped personal literals without it;
  bare names need it. Off the cloud it also detects this machine's login, home
  directory, short hostname and mounted volumes and catches each bare, except
  one that is an ordinary English word (`scripts/scan_ordinary_words.txt`),
  which it catches only in a home or volume path, unless the name is a stand
  in such as `Music`, or as a host (`<name>.local` and the other local
  suffixes, `user@<name>`, `smb://<name>`, `<name>:/path`).
  Declare such a name to have it caught bare too. Under `CLAUDE_CODE_REMOTE`
  only the declared names are read.
- In an editable install `crate doctor` fails `repo.commit_hook` until the
  hooks are installed. Never install the copy you run against a library with
  `--editable`.
- Do not symlink `.venv` into a git worktree: the editable install names the
  checkout it came from.

## The battery

Nothing merges until all three are clean:

```bash
.venv/bin/ruff check src tests scripts
.venv/bin/python -m pytest
.venv/bin/python scripts/scan_repo.py
```

- pytest runs with `-q -n auto --dist worksteal` from `pyproject.toml`, so
  a worker that runs out of tests takes queued ones from a busy worker; add
  `-n 0` for a debugger or profiler. While building, run the test files for what you
  touched.
- The suite is a macOS proof. On Linux run `scripts/cloud_battery.py baseline`
  on the base commit and `scripts/cloud_battery.py compare` on the branch; it
  fails on tests the branch newly breaks, and stops first on a red ruff or
  scan or a missing baseline. It compares whole node ids, and refuses a
  baseline measured before U268, whose ids were cut at their first space;
  measure that one again. Each run that reaches its reading leaves
  `.cloud-battery/verdict.json`,
  which `scripts/mutate.py --known-failures` reads in place of its own full
  baseline when it is for the same commit, on a tree clean then and now, on this machine,
  with the same known failures file (U271); `--measure-baseline` measures
  regardless.
  Each run keeps its temporary files in a fresh
  directory of one place, disk unless `baseline --temp memory` names the
  memory filesystem, and `compare` runs where the baseline did, refusing a
  `--temp` naming the other; the baseline names its place in its header, the
  driver keeps every child in the place its known failures name, and a
  baseline naming no place, measured before U273, is measured again. In
  memory the tests on the battery's `ON_DISK` list, the inode bound test alone
  today, run a second time on disk and their disk outcome stands. Memory is
  not for a merge battery until #702 is answered: the inode bound test fails
  on the container's disk alone, so a memory baseline reads it as the
  machine's.
- `scripts/scan_repo.py` scans every tracked file, the vendored tree included,
  for personal literals (home directories, volumes, accounts, machine names)
  and credential-shaped content.
- ruff skips `src/cratekit/_vendor`; see [`vendoring.md`](vendoring.md).
- `scripts/analyze_stages.py` measures where an `analyze run` spends its
  time: `stages` for wall time per stage, `memory` for one light worker's
  peak per track, `batch` for one worker against the pool, each over a folder
  it only reads, or over the fixed synthetic set `synthesize` writes.
  `scripts/head_agreement.py --analyse N` reads the detector's tempo
  agreement with rekordbox; the detector reads no key since U343, so its rows
  count as unkeyed. After a change to `analysis/detect.py`, `separation.py`
  or `light.py`, re-run them and replace the numbers those modules quote.
- `scripts/cyanite_trial.py` is U245's Cyanite trial, a person's command
  rather than a maintainer's, described in the guide. Its suite drives it with
  recorded answers only; the shipped send is detonated for every test in
  `tests/conftest.py`.

## The refactor's measure and its two checks

`scripts/refactor_measure.py` is the one measure of the refactor epic (U290),
standard library only, and the two suite checks below call its functions, so
the suite and the audit read the same thing. [`CONCEPTS.md`](../CONCEPTS.md)
defines package, logical line, copied block, window, allowance, named
interface, seam crossing, toggle home and dangling verb.

| Command | Prints |
|---|---|
| `lines [PATH ...]` | lines, code, docstring, comment and blank per package, every file over 1,500 lines, and with `--files` every file; `src/cratekit` and `tests` by default; exit 2 for a path that names no Python file it reads |
| `duplicates [PATH ...]` | exact copied blocks of six logical lines or more, per package; `--min N` for another size, `--list N` for the longest, `--renamed` for the reading with names normalised, `--where DIGEST` for where one allowed window stands |
| `imports` | the seam counts the import rules hold; `--names` lists every core name a feature package uses, `--drive` also drives each toggle off in a fresh interpreter and sets it beside the static reading |
| `outside FILE ...` | every name of those files that code or tests outside them use, private ones marked, `--where` for each file and line; read it before moving a name |
| `table` | points 2 to 5 of U290 in one print, exit 1 when something stands beyond an allowance or the core names are over their ceiling |
| `prune PACKAGE ...` | lowers those packages' allowance files to what is still found; it can add no line |

- `tests/test_duplication.py` fails when a package holds a copied block beyond
  its allowance, `tests/ratchets/duplication/<package>.txt`. Give the lines
  one home; never add a line to an allowance. Every allowance is empty since
  U329. It also fails on a function body of three lines or more, its arguments
  and statements compared as syntax trees with the docstring dropped, defined
  identically in two files under `src/cratekit`, which has no allowance.
- `tests/test_import_rules.py` fails on any seam crossing, and when feature
  packages use more distinct core names than `CORE_NAMES_CEILING`.
  `CORE_INTERFACE` and `TOGGLE_HOMES` live in that file; a toggle added to
  `core.profiles.MODULES` must be given its homes there. A home never holds
  what builds a verb its toggle does not gate, so `favorites` owns its one
  verb's module and not the package. A verb a toggle gates may be built
  outside any home, as `label.sync` is in the shell, and no test holds the
  table to the registry.
- Every allowance, of either kind, is empty (U329, U331), and a line in one
  fails. `prune` remains for a branch built before that.
- A feature package reaches a core module in one of three ways (U331): the
  module is on `CORE_INTERFACE` and is imported itself; a listed module
  re-exports the names, which is how a module leaves the list or stays off it;
  or the module is no part of core and lives in the feature package that
  owns it, as `sync/held_plan.py`, `intake/rehearsal.py` and `intake/drift.py`
  do (analysis and the shell's tail import the last from intake). A
  re-export is never free: the listed module imports the other with every
  command that imports it, a guard that follows imports follows it there (the
  reports audit, the lazy shell's ceiling in `tests/test_cli_lazy.py`), and a
  test that patches the name patches it where the caller reads it. So it is
  given only where the listed module imported the other already or the cost
  was measured, and a heavy module, or one a guard is keyed on, takes a place
  on the list instead (`pool`, `taxonomy_word`). Loading a module on demand
  behind `__getattr__` hides it from those guards and is not done. A module
  a listed module imports at its top level is no way round the list:
  `tags.art.read` and `from cratekit.core.tags import art` are read as reaches
  of `core.art`. A module bound any other way (an assignment, a star import,
  `getattr`, a function that returns it) is not followed by the measure, and
  is not written.
- When a module is split or added, three registers are per package or per
  line, so no other package's card edits the same lines: the reserved cause
  pins in `tests/ratchets/reserved_causes/<package>.py` (read by
  `tests/_pinned_reserved_populations.py`), the allowances above, which a
  split does not edit, and `_PLACED` in `tests/test_layering.py`, where a part
  split from a module placed by name gets one line of its own.
- A part split from a module is a new module to the import rules. While every
  name stays importable from where it was, nothing changes; a package that
  imports the part itself can cross a seam it had not, a core part off the
  named interface or a private name of it, and add a core name to the count.
- A copied block is read across function boundaries, so a split that sets two
  functions side by side, or a deletion between two stretches of lines, can
  form a window that stands elsewhere already. That is a new copy and fails:
  keep the order the lines had, or give the lines their one home.

## The refactor's proof: recorded kills and compared behaviour

Two scripts hold a card that restructures code to what the suite caught and
the verbs did before it (U297), both standard library only. METHOD's mutation
table section says when a card owes them, and the cloud-unit skill has the
commands in order. [`CONCEPTS.md`](../CONCEPTS.md) defines kill set, replay
pass, scenario and capture.

| Command | Does |
|---|---|
| `killset.py list [PATH ...]` | reads every table under `docs/mutation/` and counts, per source file, the recorded kills that are live, stale, ambiguous or gone; `--rows` lists each row and its state |
| `killset.py rows PATH ... --out FILE` | writes the live recorded kills of those files or directories as a row file for the driver's `replay` pass, each row naming the table and id it came from |
| `killset.py rows --after BEFORE.json --out FILE` | writes the same kills after a refactor, each anchored where its text stands now, following text to another file only when that file did not hold it at the commit the first table was measured on, and lists the ones it could not place |
| `killset.py check BEFORE.json AFTER.json` | exit 1 unless every row killed before is killed after, or is mapped there, with a reason, to a row that is; exit 2 for a table it cannot read |
| `behaviour_compare.py capture --out DIR` | runs the scenarios under `tests/behaviour/` on a disposable library and keeps what each command printed and wrote; `--rev REV` runs them against that revision's `src/`, `--only EXPR` runs a selection |
| `behaviour_compare.py compare A B` | prints each difference between two captures, exit 1 on any and 2 for a capture it cannot read; `--full` prints each difference whole |

- A replay is a pass kind of `scripts/mutate.py`, `pass_kind = "replay"`, with
  no row cap. `rows` names the batch for its row file without the closing
  `-rows`, so the driver writes the tables the next command reads. The driver
  checks every replay row's source against the table it names, refusing a
  replay row that names no source, or one
  whose source no table under `docs/mutation/` recorded as killed, and a
  replay resumes only from a sidecar of the same commit. It is never a unit's
  own table, whose cap stands.
- A replay table committed under `docs/mutation/` is read by `killset.py` as
  where its sources live now and counted as no table of its own, so a guard
  one card moves stays in the kill set for the next.
- A scenario file is `tests/behaviour/<package>.py`. It is not named
  `test_*.py`, so the suite does not collect it, and `capture` runs the files
  as a pytest run of its own under the suite's isolation. A scenario takes
  the `stage` fixture and runs every command through it; a card adds one for
  any verb it touches that has none. A file can hold one fixture of a name,
  so a package whose scenarios borrow from two suites that each call their
  machine `machine` keeps the second suite's in `<package>_<verb>.py`, as
  `tagging_rows.py` is.
- `--rev` runs the branch's scenarios and the branch's test helpers against
  the other revision's `src/`, so a scenario file names nothing the base
  does not have: a module, a function or a constant the branch added is read
  through a verb, never imported.
- A capture's root is one fixed directory inside the system's temporary
  directory. `capture` refuses a root outside it, and a root holding files no
  capture left.
- `tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal`
  captures every scenario twice and fails on any difference, so a scenario
  that prints or writes a value nothing pinned fails there, with the value
  shown. `tests/behaviour/__init__.py` holds the pins.

## Where the shared plumbing lives

What every package once wrote for itself has one home (U298), each in the
lowest layer that can host it. A feature package may import `cli.output`,
`cli.exit_codes` and `cli.prompt` from the shell and nothing else of it, and
the core modules on `CORE_INTERFACE`. Before writing a helper in a feature
package, look here first. `tests/test_shared_homes.py` holds the homes U298
added; the capture is held in `tests/test_write_session.py`, and the locks,
`mkdir_private` and `is_inside`, which were public spellings of what core
already had, through the config and writer suites that drove them before.

| Need | Home |
|---|---|
| load the configuration and refuse `config-unusable` with the verb's own origin | `cli.output.load_config(origin)` |
| find a verb's gate by name on its registry entry | `cli.output.declared_gate` (raises `RuntimeError` when absent) and `cli.output.confirm_gate` (refuses `internal-error`); the two answers differ, so a verb keeps the one it had |
| who approved a gate | `cli.output.approving_actor(ctx, spec)` |
| the `job_state` payload of a run that queued nothing | `cli.output.no_job(state, **progress)` |
| a count read off a stored document | `cli.output.count_of` |
| a job's report for an envelope, and the reconcile, drive and raise of a resume | `core.jobs.reported`, `core.jobs.advance`, `core.jobs.resumed` |
| where one item's report is staged and where it lands | `core.jobs.Artifacts(final=..., staging=...)`, bound once per feature |
| a private SQLite store opened on the queue's pragmas | `core.private_store.PrivateStore` |
| a lock held across one read then write cycle of a state document | `core.config.held(lock_path, refused)` |
| a lock a writer would rather skip than wait for | `core.config.lock_within(...)` yields whether it was had |
| a lock taken without waiting, the holder's words left readable | `core.config.lock_now(path)` |
| a lock that waits for its holder, made under a private directory | `core.config.exclusive_lock(path)`, and `core.config.mkdir_private` for the directory |
| a lock file opened owner only, hardened by the caller, then taken | `core.config.flock_exclusive(target, harden)` |
| a state document read as JSON, refused rather than read as empty | `core.config.read_json`, `read_json_map`, `read_bytes_if_present`, and `read_json_as_text` for the two stores that read in the platform's encoding |
| whether one path is inside another | `core.config.is_inside(child, parent)` |
| the device a path is on, read off its nearest ancestor that exists | `core.preflight.device_of`, which a feature package reads as `core.session.device_of` (U331) |
| which volume this is, what is mounted, and whether two spellings name one path | `core.session.IdentityProvider`, `MountEnumerator`, `normalize_identity`, `names_one_path`, re-exported from `core.preflight` (U331) |
| whether rekordbox is gone, asked without the rekordbox extra | `core.session.rekordbox_processes_running`, `running_process_names`, `REKORDBOX_PROCESSES`, `ProcessLister`, `AbsenceUnconfirmed`, re-exported from `core.processes` (U331) |
| the room a check's copy needs | `core.session.assert_room_for_check`, `check_had_no_room`, re-exported from `core.snapshot` (U331) |
| the folder a queued verb walks, its item ids and where an item's file is | `core.jobs.scan_audio`, `frozen_walk`, `item_path`, `walk_warnings`, `warnings_of`, `Scan`, re-exported from `core.discovery` (U331) |
| the ceiling a pool takes from the cores | `core.pool.worker_ceiling`, re-exported from `core.cores` (U331), beside the pool it sizes, so a spawned worker loads nothing more for it |
| another app's nodes, told from the tree's own | `core.active_taxonomy.outside_foreign`, `foreign_roots_in`, `FOREIGN_OWNER`, `FOREIGN_LEFT_AS_IT_IS`, re-exported from `core.foreign_tree` (U331) |
| the membership a configuration resolves to, and the extras group a module installs with | `cfg.membership()`, `core.config.Membership`, `core.config.install_command`, from `core.profiles` (U331) |
| a missing `yt-dlp` as the calling verb's refusal | `core.binaries.yt_dlp_missing` (U331) |
| the lossy name template and the name budget from configuration | `core.naming.NameTemplate.lossy`, `.lossy_if_marked`, `core.naming.NameBudget.of` |
| the capture a guarded database write opens with | `write.trees.attached_capture(gates, cfg, db)` |
| undo pending work on a handle after a failed write, never masking its cause | `write.trees.rollback_quietly(db)` |
| the commit a content row write records | `write.row_defaults.record_commit` |
| the roots a write's analysis-file watch covers, refused when empty | `write.row_defaults.watched_roots`, which `intake.rotate` imports (U329) |
| a remedy token a configuration failure names | `core.exit_codes.Remedy`, which `core.config` re-exports as `config.Remedy` (U329) |

## Config and the taxonomy, in parts

`core.config` and `core.taxonomy` are each split into parts (U299), and every
name a caller used stays importable from the module it always came from, which
is the one to import from. `core.config_base` holds the schema version, the
volume and template keys, the environment variables and the two installation
directories;
`core.state_files` the state inventory and its resolvers, so a new state entry
is declared there; `core.config_schema` the section classes and `Config`; and
`core.config_validate` validation and the environment overrides. `core.config`
keeps the failure types, `from_dict`, migration, loading, saving and the
durable write and lock helpers, because the suite patches those on `config`
and they call each other. `core.taxonomy_model` holds the taxonomy's classes,
`core.taxonomy_build` the build and its checks, and `core.taxonomy` the shipped
templates and the loader. A test that patches a name patches it in the module
whose code calls it.

## The guarded writer, the session and the restore, in parts

`core/rb_writer.py`, `core/session.py` and `core/restore.py` are each split
into parts (U300), and each answers for every name code, scripts and tests
read through it: they import and patch `rb_writer`, `session` and `restore`,
never a part. A name nothing reads through its module is not re-exported
(U953), and a part is imported only by its module and its module's other
parts.

| Module | Its parts |
|---|---|
| `core.rb_writer` | `rb_tables` (the whitelist's tables, the column registry), `rb_call_time` (the one call time accessor the other parts share), `rb_probes` (the installed version, the processes, the sync setting), `rb_copies` (the snapshot, disposable and read-only copies, the integrity check, prune), `rb_nodes` (playlist, membership and tag primitives, the node move and removal), `rb_changes` (what a session would write, and its judge), `rb_removal` (Remove from Collection's reads and proof), `rb_positions` (the closing up of a playlist a removal touched, U958) |
| `core.session` | `session_call_time` (the one call time accessor the other parts share), `session_holders` (the holder and the library lock), `session_ack` (the backup acknowledgment), `session_volumes` (the volume gates), `session_analysis` (the analysis-file fingerprint) |
| `core.restore` | `restore_perform`, `restore_retention`, `restore_recovery`, `restore_tags` |

Four rules keep the split invisible:

- **A part reads its module's seams through the module, at call time.** A
  name defined in the module, in another part, or patched on the module by a
  test is written `_writer().name`, `_session().name` or `_restore().name`
  inside a part, so a `monkeypatch.setattr(rb_writer, ...)` bites there too.
  The writer's parts bind `_writer` to `rb_call_time.writer` and the
  session's bind `_session` to `session_call_time.session` (U329), one
  accessor per family rather than a copy in each part, and the soft delete
  guard in `tests/_source_guards.py` reads `_writer()` imported from there.
  `restore`'s parts read `os` and `shutil` the same way, since a capacity test
  patches them on `restore`. Of the writer's parts, only `rb_tables`, which
  reads nothing back, and `rb_call_time` are imported by the others directly;
  the session's parts import none of each other but `session_call_time`;
  `restore_retention` and `restore_recovery`
  import `restore_perform` for its accessor and logger rather than holding
  their own.
- **What the beat grid suites and the source guards read stays in the module
  itself**: every writer refusal slug `test_rb_writer_guard.py` scans for, the
  one read of the soft-delete marker, `commit_guarded`, the write lock, and
  `CollectionRemoval`, whose two calls `test_sync_removed.py` pins to
  `core/rb_writer.py`.
- **Every scan that forbids a shape in a split module reads its parts too**
  (R-1890): such a guard reads the module by way of `tests/_split_modules.py`,
  which finds the parts by the glob of the module's file name (`rb_*.py`,
  `session*.py`, `restore*.py`), so a part must be named that way.
  `tests/test_split_modules.py` fails on a part the glob misses that this
  table names, that only its module and its parts import by an absolute
  import, or that defines an accessor in the parts' spelling or imports one
  from its family's call time part. The beat grid suite's writer scans are applied to the parts by
  `tests/test_rb_writer_parts_guard.py`, since that suite is not edited.
- **A restore part takes `restore`'s write rank** by one line of its own in
  `tests/test_layering.py`, as the ladder provides.

## The verb table, in parts

`cli/registry.py` defines every name code, scripts and tests read (`Entry`,
`GateSpec`, `ENTRIES`, the indexes and the lookups), and the table's rows live
in five parts beside it (U328), so no file of it passes 1,500 lines. Each part
is one literal tuple of `Entry(...)` calls and a contiguous slice of the
table; `registry.py` imports the parts once the names they read are bound and
assembles `ENTRIES` in this order, which is the order `crate --help` lists the
commands in:

| Part | Its tuple | Holds |
|---|---|---|
| `cli.registry_state` | `STATE_VERBS` | setup, profiles and runs, the row repairs, the write session and its safety spine, jobs, review |
| `cli.registry_pipeline` | `PIPELINE_VERBS` | intake, tagging and naming, acquisition, routing and the audits, analysis |
| `cli.registry_sync` | `SYNC_VERBS` | the sync pass and its schedule, the label registry and its sweeps, a label's playlists on the account |
| `cli.registry_modules` | `MODULE_VERBS` | adoption, deletion, export, the set builder, mastering, backup, the skills |
| `cli.registry_later` | `LATER_VERBS` | every block appended since, in the order it landed |

- **A new verb's block is appended to `cli/registry_later.py`**, so two
  branches that add a verb conflict where a person reads it. Before that file
  passes 1,500 lines the next block opens a new part, in three edits: the
  part, named `registry_*.py`, imported and starred into `ENTRIES` after it;
  its tuple's name added to `order` in
  `test_the_table_is_every_part_in_order_and_each_file_is_under_the_bar`
  (`tests/test_cli_contract.py`), which fails on a part nobody assembles, on
  one its list does not name, on a changed order and on a file over the bar;
  and `DOCTOR_HELP_CEILING` in `tests/test_cli_lazy.py` raised by one, since
  every part loads at every start. The table above and each part's "part N of
  5" line then take the new part too, which no test holds.
- **A part is a tuple of calls and `ENTRIES` a tuple of starred part names**,
  because two scripts read the table as text and cannot import it:
  `refactor_measure.py` (`verbs_from`) follows each starred name into the
  tuple of that name, and `board.py` (`planned_units`) reads the `planned_in`
  markers of every `registry*.py`. Both raise or are held to the live registry
  by a test, so a shape they cannot read fails the battery.
- **A verb is read through `cli.registry`, never from a part.** A part imports
  `Entry`, `GateSpec` and the shared constants from `cli.registry`, so only
  the registry imports a part, and every name a test patches stays there.
  `tests/test_import_rules.py` fails on an import of a part from any other
  source file; it cannot see `importlib.import_module`, a part reached as an
  attribute of the `cli` package, nor a part's tuple read off `cli.registry`
  by name, each of which skips a patch of `ENTRIES` as well.

## CI

`.github/workflows/ci.yml` proves packaging and portability, not the suite
(`.github/workflows/app.yml` is the menu bar app's, below):

| Job | Runs |
|---|---|
| `scan` | `scan_repo.py`, then `board.py closing` over the pushed range or pull request |
| `portable` | slim install on 3.12 and 3.13, a check that no heavy extra came with it, ruff |
| `cold-install` | a clean `pip install .` on 3.12 and 3.13, `crate --help`, the eager parser on the full preset (since U248 it, and not `crate --help`, proves every verb's module imports), and an import of the vendored downloader from the installed package |

## The menu bar app

`app/` is a Swift package for a macOS menu bar app, built with SwiftPM alone
(no Xcode project), macOS 13 the floor (U965). The engine stays the authority:
the app reads and calls verbs and holds no logic about the library, and no
LLM connection.

| Target | What it is |
|---|---|
| `CrateEngine` | runs a verb as `crate --output json <verb>` by the absolute path in the app's settings (the `cratePath` default), never a shell or a search of `PATH`; a minimal environment (`HOME`, the locale keys, `TMPDIR`, and `PATH` of crate's own directory then the system directories); a timeout per call that terminates, then kills; and the version 1 envelope decoded, a refusal included, as a value. A missing, relative, folder or non executable path is a setup state the UI shows |
| `CrateEngine`, status (U966) | `Glance.swift` decodes `crate status`'s `data.summary.glance` against `tests/schemas/status_glance.v1.json` (a key absent is malformed, a glance of another version refused by name, an `attention` word it does not know kept as unknown); `StatusReading.swift` turns a status call into a reading or a failure with its message, picks the icon per `attention`, and projects the menu as lines; `StatusRefresher.swift` runs at most one `crate status` at a time and keeps the last good reading with its time |
| `CratekitBar` | the `MenuBarExtra` app, no Dock icon: the status icon and menu, refreshed every minute and when the menu opens |
| `CrateEngineTests` | XCTest over the envelope fixtures and fake `crate` scripts |

The fixtures in `app/Tests/CrateEngineTests/Fixtures` are written from the real
verbs by `tests/test_app_fixtures.py`, which fails the battery when a verb no
longer emits its fixture; the `status_*` fixtures are `crate status` once per
`attention` word, built as `tests/test_status_glance.py` builds each state and
read at a held clock. Regenerate with `REGEN=1 .venv/bin/python -m pytest
tests/test_app_fixtures.py` and read the diff. On a Mac with a Swift toolchain,
from `app/`: `swift build`, `swift test`, and `scripts/bundle.sh`, which
bundles the release build into `build/CratekitBar.app` with `LSUIElement` set,
signs it ad hoc (no Apple account), and zips it. No container compiles Swift,
so `.github/workflows/app.yml` does all three on a macOS runner whenever `app/`,
the fixture test or the workflow changes, and uploads the zip for seven days;
the repository is public, so those minutes cost nothing.

## Deferred guards

A test written before its module exists keeps its full assertion and is
skipped with a reason naming the unit that arms it. `tests/_pending.py` is the
register and `tests/test_pending_units.py` fails an unrecorded skip and a skip
kept after its module lands. `pytest -rs` lists skips. The register is empty.

## Process

[`CLAUDE.md`](../CLAUDE.md) is the session contract and
[`METHOD.md`](METHOD.md) the pipeline and merge bar;
[`BOARD.md`](BOARD.md) explains the queue. `AGENTS.md` routes other agents to
the same place.
