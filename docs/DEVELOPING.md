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
  bare names need it.
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
  `scripts/head_agreement.py --analyse N` reads the shipped key method's
  agreement with rekordbox, `plain` since U276, and `--key whole|windows`
  reads one of the other two over the same sample. After a change to
  `analysis/detect.py`, `separation.py` or `light.py`, re-run them and replace
  the numbers those modules quote.
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
  one home; never add a line to an allowance.
- `tests/test_import_rules.py` fails on a new seam crossing beyond
  `tests/ratchets/imports/<package>.txt`, and when feature packages use more
  distinct core names than `CORE_NAMES_CEILING`. `CORE_INTERFACE` and
  `TOGGLE_HOMES` live in that file; a toggle added to `core.profiles.MODULES`
  must be given its homes there.
- An allowance line is removed by the card that removes its finding, by hand
  or with `prune`. A stale line fails nothing.
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
| the device a path is on, read off its nearest ancestor that exists | `core.preflight.device_of` |
| the lossy name template and the name budget from configuration | `core.naming.NameTemplate.lossy`, `.lossy_if_marked`, `core.naming.NameBudget.of` |
| the capture a guarded database write opens with | `write.trees.attached_capture(gates, cfg, db)` |
| undo pending work on a handle after a failed write, never masking its cause | `write.trees.rollback_quietly(db)` |
| the commit a content row write records | `write.row_defaults.record_commit` |

## The guarded writer, the session and the restore, in parts

`core/rb_writer.py`, `core/session.py` and `core/restore.py` are each split
into parts (U300), and each still answers for every name it had: code,
scripts and tests import and patch `rb_writer`, `session` and `restore`,
never a part. A part is re-exported by its module and is not imported from
anywhere else.

| Module | Its parts |
|---|---|
| `core.rb_writer` | `rb_tables` (the whitelist's tables, the column registry), `rb_probes` (the installed version, the processes, the sync setting), `rb_copies` (the snapshot, disposable and read-only copies, the integrity check, prune), `rb_nodes` (playlist, membership and tag primitives, the node move and removal), `rb_changes` (what a session would write, and its judge), `rb_removal` (Remove from Collection's reads and proof) |
| `core.session` | `session_holders` (the holder and the library lock), `session_ack` (the backup acknowledgment), `session_volumes` (the volume gates), `session_analysis` (the analysis-file fingerprint) |
| `core.restore` | `restore_perform`, `restore_retention`, `restore_recovery` |

Four rules keep the split invisible:

- **A part reads its module's seams through the module, at call time.** A
  name defined in the module, in another part, or patched on the module by a
  test is written `_writer().name`, `_session().name` or `_restore().name`
  inside a part, so a `monkeypatch.setattr(rb_writer, ...)` bites there too.
  `restore`'s parts read `os` and `shutil` the same way, since a capacity test
  patches them on `restore`. Only `rb_tables`, which reads nothing back, is
  imported directly.
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
  import, or that holds an accessor in the parts' spelling. The beat grid suite's writer scans are applied to the parts by
  `tests/test_rb_writer_parts_guard.py`, since that suite is not edited.
- **A restore part takes `restore`'s write rank** by one line of its own in
  `tests/test_layering.py`, as the ladder provides.

## CI

`.github/workflows/ci.yml` proves packaging and portability, not the suite:

| Job | Runs |
|---|---|
| `scan` | `scan_repo.py`, then `board.py closing` over the pushed range or pull request |
| `portable` | slim install on 3.12 and 3.13, a check that no heavy extra came with it, ruff |
| `cold-install` | a clean `pip install .` on 3.12 and 3.13, `crate --help`, the eager parser on the full preset (since U248 it, and not `crate --help`, proves every verb's module imports), and an import of the vendored downloader from the installed package |

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
