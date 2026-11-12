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
  measure that one again.
- `scripts/scan_repo.py` scans every tracked file, the vendored tree included,
  for personal literals (home directories, volumes, accounts, machine names)
  and credential-shaped content.
- ruff skips `src/cratekit/_vendor`; see [`vendoring.md`](vendoring.md).
- `scripts/analyze_stages.py` measures where an `analyze run` spends its
  time: `stages` for wall time per stage, `memory` for one light worker's
  peak per track, `batch` for one worker against the pool, each over a folder
  it only reads, or over the fixed synthetic set `synthesize` writes.
  `scripts/head_agreement.py --analyse N --key windows|plain` reads a cheaper
  key method's agreement with rekordbox. After a change to
  `analysis/detect.py`, `separation.py` or `light.py`, re-run them and replace
  the numbers those modules quote.

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
