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
  baseline when it is for the same commit, on a clean tree, on this machine,
  with the same known failures file (U271); `--measure-baseline` measures
  regardless.
  Each run keeps its temporary files in a fresh
  directory of one place, disk unless `baseline --temp memory` names the
  memory filesystem, and `compare` runs where the baseline did, refusing a
  `--temp` naming the other; a baseline naming no place, measured before
  U273, is measured again. Memory is not for a merge battery until #702 is
  answered: the inode bound test fails on the container's disk alone, so a
  memory baseline reads it as the machine's.
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
