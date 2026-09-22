#!/usr/bin/env python3
"""Mutation table driver. Rows go in as data, a measured table comes out.

Every review agent on this project has hand rolled this loop, and three of the
project's recorded incidents were hand rolled driver mistakes: a `git checkout`
restore that ate a fix round's uncommitted edits, a second `-q` that became
`-qq` and hid the summary line, and a batch measured against a red baseline that
read every row as a death. The judgement in a mutation table is choosing which
guards to revert. Everything after that choice is obedience, and obedience is
what a script is for.

So: the agent supplies the rows. This supplies apply, run, count, restore and
verify, identically every time.


WHAT A MUTATION TABLE IS, IF YOU HAVE NOT MET ONE
-------------------------------------------------
A green test suite tells you the tests pass. It does not tell you the tests
would NOTICE if the code broke. Mutation testing answers the second question by
breaking the code on purpose: revert one guard, run the suite, count how many
tests fail. That count is the guard's "death count". A guard whose removal kills
zero tests is not tested, whatever the coverage report says, because coverage
measures which lines RAN and a mutation table measures which lines MATTER.


HOW TO RUN IT
-------------
    ./.venv/bin/python scripts/mutate.py rows.toml

    ./.venv/bin/python scripts/mutate.py rows.toml --name u34-round-2
    ./.venv/bin/python scripts/mutate.py rows.toml --resume
    ./.venv/bin/python scripts/mutate.py rows.toml --allow-dirty

It writes `docs/mutation/<name>.md`, the table a human and a later verifier
read, and `docs/mutation/<name>.json`, the same numbers as data so a later agent
can read counts without re-reading prose.


THE ROW FORMAT
--------------
TOML or JSON, chosen by the file suffix. TOML is easier to author because its
triple quoted literal strings hold code exactly, with no escaping. A worked
example, complete:

    name = "u34-round-2"
    pass_kind = "light"          # "light" caps at 25 rows, "full" at 45

    [[rows]]
    id = "G1_empty_name"
    description = "Drop the empty-name guard in tree_registry.register"
    file = "src/cratekit/core/tree_registry.py"
    surface = "user"             # "user" or "maintainer"; default "maintainer"
    old = '''
        if not name.strip():
            raise ValueError("a tree needs a name")
    '''
    new = ""

    [[rows]]
    id = "G1_composite"
    description = "What G1 does hold: register an empty name and read it back"
    file = "src/cratekit/core/tree_registry.py"
    pairs_with = "G1_empty_name"     # this row is G1_empty_name's composite
    old = '''    return sorted(entries)'''
    new = '''    return list(entries)'''

    [[rows]]
    id = "R4_message"
    description = "Reword the refusal message, do not append to it"
    file = "src/cratekit/core/restore.py"
    tests = ["tests/test_restore.py"]     # optional; derived when omitted
    old = '''"nothing staged to restore"'''
    new = '''"no staged restore was found"'''

    [[dropped]]
    id = "G7_lock_timeout"
    description = "Halve the lock timeout coefficient"
    reason = "ranked below the cap: same guard family as G3, which is measured"

Row fields. `id`, `description`, `file`, `old` and `new` are required; `new`
may be the empty string, which is how you delete a guard. `tests` is an optional
explicit subset. `surface` is `user` or `maintainer` and decides whether a zero
row owes a composite. `pairs_with` names the row this one is the composite for.

`dropped` entries are rows you CONSIDERED and did not run. METHOD caps a light
pass at 25 rows and a full pass at 45, and a truncation nobody logged reads as
coverage. Logging it is what makes the gap visible.


WHAT HAPPENS PER ROW, AND WHY EACH STEP IS THERE
------------------------------------------------
1.  Snapshot the target file's bytes in memory. Not a scratch copy, not a git
    stash, not a branch. The driver never uses git to WRITE, because
    `git checkout` silently discards the uncommitted edits a fix round is
    holding, and that has already cost a round of work here.

2.  Apply the mutation as an exact string replacement, and REFUSE the row if the
    old text is absent or appears more than once. An ambiguous match does not
    fail; it silently mutates the wrong site and hands you a confident number
    about an experiment you did not run. The refusal happens before anything is
    written, so a refused row never touches the disk.

3.  Run the test subset. When the row does not name one it is derived: the
    target's dotted module path is computed, every file under `tests/` is
    parsed, and the ones whose imports name that module are the subset. Derived
    rather than caller-supplied because a caller-supplied subset is a place for
    a typo to look like a result.

4.  Count deaths from pytest REPORT OBJECTS, not from stdout. A tiny plugin is
    written to a temp directory and loaded with `-p`; its hooks read
    `report.nodeid` straight off the report and write JSON. The alternative
    everyone reaches for, splitting a `FAILED` line on `" - "`, is wrong on this
    repository specifically, because that separator appears INSIDE parametrized
    test ids and the split truncates them.

5.  Record the COLLECTED count on every row and flag any drift from the
    baseline's. This is the step most hand rolled drivers skip and it is the one
    that matters most: a mutation that breaks a module's import takes that whole
    test file out of collection, so the tests that would have died never run,
    and the row reports a clean, calm, entirely false zero.

6.  Restore by rewriting the snapshotted bytes, then VERIFY against
    `git show HEAD:<path>`. Reading git is fine. The rule is that the driver
    never uses git to write. Verifying against a scratch copy instead is
    circular: a contaminated copy certifies itself.

7.  Promote a zero to a full suite run before reporting it as a zero. A death on
    a subset is a real death, so a killing row stops there and stays cheap. A
    zero on a subset is only a zero within that subset. Promoted zeros are
    marked as promoted in the output.


WHAT HAPPENS ONCE PER BATCH
---------------------------
*   A full suite BASELINE, and the batch refuses to start if it is not green,
    naming the failures. A red baseline makes every row look like a death,
    including rows that cannot possibly kill anything. That exact trap cost a
    verifier a full batch on 2026-08-10, when a scratch copy carrying no `.git`
    failed a repository cleanliness test.

*   A subset baseline per distinct subset, for the same reason at row scale, and
    to give the collected count each row is compared against.

*   A NULL CONTROL row, generated automatically, which appends a comment line to
    a Python target. It changes nothing semantically, so it MUST kill zero. If
    it kills anything, the measuring apparatus is broken rather than the code,
    the batch is declared invalid and the run stops. This is the check that
    would have caught the 2026-08-10 trap in the first minute instead of the
    last.

*   `PYTHONDONTWRITEBYTECODE=1` on every run without exception. Two mutations of
    identical byte length written a second apart leave the source mtime and size
    unchanged, so CPython reuses the cached bytecode from the PREVIOUS mutation
    and the driver measures a result that never existed.

*   `addopts` is read out of `pyproject.toml`, stripped of `-q`, and passed back
    with `-o`. The ini file already sets `-q`; a second one becomes `-qq`, which
    suppresses the summary line entirely. Stripping rather than clearing means a
    future addition to `addopts` is not silently dropped.

*   Rows run synchronously, in the foreground, one at a time. A backgrounded
    driver outlived its parent twice on this project and contaminated later
    rows, which is a failure that presents as an inexplicable number rather than
    as an error.


THE SHAPE OF THE CODE
---------------------
Four layers, each testable without the one above it:

    load_rows / derive_subset        pure functions over text and paths
    apply_mutation / mutated         the file surgery, with try/finally
    run_pytest                       one subprocess, one RunResult
    measure_row / measure_batch      the loop, the baselines, the control

`mutated` is the load bearing piece and it is nine lines: snapshot, write,
`yield`, and a `finally` that rewrites the snapshot and verifies it. A `finally`
runs on a normal exit, on an exception, and on the KeyboardInterrupt an
impatient operator sends, which is why a crash mid row cannot leave a mutated
file behind. All three paths are driven by tests, because the one path nobody
tests is the one that leaves a mutation committed to somebody's branch.

The tests run against a throwaway fixture package with its own tiny suite and
its own git repository, never against Cratekit's suite. A driver tested only
against the suite it was written for is a driver whose measurements have never
been checked against a known answer.

Exit codes
----------
    0  every row measured
    2  a refusal, decided before any row ran
    3  a restore did not match git show HEAD
    4  the batch is invalid, the null control killed something
    5  pytest produced nothing readable
    6  a child reached the real installation state (R-343)
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile
import tomllib
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import platformdirs

REPO_ROOT = Path(__file__).resolve().parent.parent

#: Appended by the null control row. A Python comment is invisible to the
#: interpreter and to an AST walk, which is what makes the control a control.
NULL_CONTROL_COMMENT = "\n# mutation driver null control, restored automatically\n"

#: METHOD's hard row caps. A cap with no enforcement was tried and did not hold:
#: light passes ran 50 and 89 rows on 2026-08-10.
ROW_CAPS = {"light": 25, "full": 45}

PLUGIN_MODULE = "mutate_report_plugin"

#: Environment variables the driver REMOVES from the child, and why. The child
#: otherwise inherits ``os.environ`` whole. That is not a convenience: a review
#: agent ran its rows under ``PATH=/usr/bin:/bin`` on 2026-08-10, which dropped
#: ffmpeg off the path, reddened 28 audio tests on every full run including the
#: baseline, and cost seven rows. The subset rows were unaffected, so the damage
#: looked selective rather than systemic. Anything scrubbed is named here and
#: printed in the table, because a silent scrub is the same defect one variable
#: smaller.
SCRUBBED_ENV = {
    "PYTEST_ADDOPTS": "an inherited value would edit the command after the driver built it",
    "PYTEST_XDIST_WORKER": (
        "the reporting plugin reads it to tell a worker from the controller, so a driver "
        "started from inside a parallel worker would hand its child a controller that "
        "believes it is a worker and writes no report; xdist sets it afresh in each "
        "worker the child starts"
    ),
    "PYTEST_XDIST_WORKER_COUNT": "the same inherited worker identity, scrubbed with it",
    "PYTEST_XDIST_TESTRUNUID": "the same inherited worker identity, scrubbed with it",
}

#: The installation-scoped directories every child is pointed AWAY from, into a
#: throwaway sandbox inside the run's own workspace. R-343 is why.
#:
#: On 2026-09-20 a child of this driver overwrote the real configuration with a
#: test fixture one, destroying what four attended sittings had established. The
#: conftest already redirects all of these, but it does so with ``monkeypatch``,
#: and ``monkeypatch.undo()`` inside a test rolls the autouse isolation back with
#: everything else it undoes. What ``undo()`` restores is the value the PROCESS
#: started with, so the fix is to make the process start in a sandbox: after
#: that, an undo lands in the sandbox rather than on the real machine.
#:
#: The app name is duplicated from ``cratekit.core.config`` on purpose. Importing
#: that module here would make the guard depend on a mutation target, and a guard
#: that imports what it guards can be mutated out from under itself.
APP_NAME = "cratekit"
SANDBOXED_ENV = {
    "HOME": "home",
    "USERPROFILE": "home",
    "XDG_CONFIG_HOME": "config",
    "XDG_STATE_HOME": "state",
    "XDG_DATA_HOME": "data",
    "XDG_CACHE_HOME": "cache",
    "CRATEKIT_CONFIG_DIR": f"config/{APP_NAME}",
    "CRATEKIT_STATE_DIR": f"state/{APP_NAME}",
}

#: Added on top of the inherited environment, never as a fresh dict.
ADDED_ENV = (
    "PYTHONDONTWRITEBYTECODE=1",
    "PYTHONPATH (the plugin's temp directory, prepended)",
    "MUTATE_REPORT_PATH (the plugin's output file)",
    "the installation state sandbox: "
    + ", ".join(sorted(SANDBOXED_ENV))
    + " (all pointed inside the run's workspace, R-343)",
)

#: The in-subprocess plugin. It exists so death counts come off report OBJECTS.
#: It rewrites its JSON file on every event rather than at the end, so a run that
#: dies partway still leaves readable evidence of how far it got.
#:
#: **Under pytest-xdist only the controller writes.** ``-p`` loads this module in
#: every worker as well, and each worker holds its own ``_STATE``, so eight
#: processes rewriting one file would leave whichever partial count flushed last.
#: The controller is the one process that sees everything: xdist forwards each
#: worker's test reports and failed collect reports to the ordinary hooks there.
#: It collects nothing itself, so its ``session.items`` is empty and the count
#: comes off the hook xdist fires when a worker finishes collecting. Every worker
#: collects the same ids or xdist aborts the run, so any one of them is the count.
PLUGIN_SOURCE = '''
import json
import os

import pytest

_OUT = os.environ["MUTATE_REPORT_PATH"]
_IS_WORKER = bool(os.environ.get("PYTEST_XDIST_WORKER"))
_STATE = {"collected": 0, "failed": [], "errored": [], "collect_errors": []}


def _flush():
    if _IS_WORKER:
        return
    with open(_OUT, "w", encoding="utf-8") as handle:
        json.dump(_STATE, handle)


def pytest_collection_finish(session):
    if session.items:
        _STATE["collected"] = len(session.items)
    _flush()


@pytest.hookimpl(optionalhook=True)
def pytest_xdist_node_collection_finished(node, ids):
    _STATE["collected"] = len(ids)
    _flush()


def pytest_collectreport(report):
    if report.failed:
        _STATE["collect_errors"].append(report.nodeid)
        _flush()


def pytest_runtest_logreport(report):
    if not report.failed:
        return
    bucket = _STATE["failed"] if report.when == "call" else _STATE["errored"]
    if report.nodeid not in bucket:
        bucket.append(report.nodeid)
    _flush()
'''


class DriverRefusal(RuntimeError):
    """The driver will not proceed. Loud on purpose, never a warning."""


class RestoreVerificationError(RuntimeError):
    """A restored file does not match ``git show HEAD``. Nothing continues."""


class MeasurementFailure(RuntimeError):
    """pytest could not be measured at all, which is not the same as a zero.

    Deliberately NOT a ``DriverRefusal``. A refusal means the row was rejected
    before it ran and the tree is untouched. This means the run happened and
    produced nothing readable, which has to be recorded as an error rather than
    quietly filed beside the rows that were legitimately refused.
    """


class StateLeak(RuntimeError):
    """A child wrote to the REAL installation state. The batch stops here.

    Deliberately NOT a ``DriverRefusal`` and not a ``MeasurementFailure``.
    ``measure_row`` catches ``DriverRefusal`` and turns it into a refused row, so
    a leak filed under that class would be recorded as one unremarkable row and
    the driver would carry on running more children against a machine it had
    just damaged. This class is caught nowhere but the row loop, which names the
    row, and ``main``, which stops.

    It aborts the whole batch rather than failing one row because the damage is
    already done by the time it is observed. The question after a leak is not
    which of the remaining rows still measures, it is what was overwritten.
    """


# ---------------------------------------------------------------------------
# Rows
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Row:
    """One exact textual substitution in one file."""

    id: str
    description: str
    file: str
    old: str
    new: str
    tests: tuple[str, ...] | None = None
    surface: str = "maintainer"
    pairs_with: str | None = None
    kind: str = "mutation"

    def fingerprint(self) -> str:
        """A stable digest of everything that changes the measurement.

        ``--resume`` reuses a stored result only when this matches, so editing a
        row's text invalidates its old number instead of inheriting it.
        """
        payload = "\0".join([self.id, self.file, self.old, self.new, self.kind])
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class Dropped:
    """A row that was considered and not run, with the reason it was not."""

    id: str
    description: str
    reason: str


def load_spec(spec_path: Path) -> tuple[str, str, list[Row], list[Dropped]]:
    """Read a row file and return ``(name, pass_kind, rows, dropped)``."""
    text = spec_path.read_text(encoding="utf-8")
    if spec_path.suffix == ".toml":
        data = tomllib.loads(text)
    elif spec_path.suffix == ".json":
        data = json.loads(text)
    else:
        raise DriverRefusal(
            f"{spec_path.name}: row files are .toml or .json, not {spec_path.suffix!r}"
        )

    name = str(data.get("name") or spec_path.stem)
    pass_kind = str(data.get("pass_kind", "full"))
    if pass_kind not in ROW_CAPS:
        raise DriverRefusal(f"pass_kind must be one of {sorted(ROW_CAPS)}, got {pass_kind!r}")

    rows: list[Row] = []
    seen: set[str] = set()
    for index, entry in enumerate(data.get("rows", [])):
        missing = [key for key in ("id", "description", "file", "old", "new") if key not in entry]
        if missing:
            raise DriverRefusal(f"row {index}: missing required field(s) {', '.join(missing)}")
        row_id = str(entry["id"])
        if row_id in seen:
            raise DriverRefusal(f"duplicate row id {row_id!r}; ids are how a row is re-run later")
        seen.add(row_id)
        if not entry["old"]:
            raise DriverRefusal(f"row {row_id}: empty old text; a row names the text it replaces")
        surface = str(entry.get("surface", "maintainer"))
        if surface not in {"user", "maintainer"}:
            raise DriverRefusal(f"row {row_id}: surface must be 'user' or 'maintainer'")
        tests = entry.get("tests")
        rows.append(
            Row(
                id=row_id,
                description=str(entry["description"]),
                file=str(entry["file"]),
                old=str(entry["old"]),
                new=str(entry["new"]),
                tests=tuple(str(one) for one in tests) if tests else None,
                surface=surface,
                pairs_with=str(entry["pairs_with"]) if entry.get("pairs_with") else None,
            )
        )

    if not rows:
        raise DriverRefusal(f"{spec_path.name} declares no rows")
    cap = ROW_CAPS[pass_kind]
    if len(rows) > cap:
        raise DriverRefusal(
            f"{len(rows)} rows exceeds the {pass_kind} pass cap of {cap} (METHOD). "
            f"Cut to the cap and log what you dropped in [[dropped]], so the "
            f"truncation is visible rather than read as coverage."
        )

    unknown = {row.pairs_with for row in rows if row.pairs_with} - seen
    if unknown:
        raise DriverRefusal(f"pairs_with names no row in this batch: {sorted(unknown)}")

    dropped = [
        Dropped(
            id=str(entry.get("id", f"dropped-{index}")),
            description=str(entry.get("description", "")),
            reason=str(entry.get("reason", "")),
        )
        for index, entry in enumerate(data.get("dropped", []))
    ]
    return name, pass_kind, rows, dropped


def null_control_row(rows: list[Row]) -> Row:
    """Build the control row: a change that cannot possibly kill a test.

    It targets a Python file among the batch's own targets, so the control runs
    through the same apply, restore and verify path the real rows do. A control
    measured somewhere else is not a control of this batch.
    """
    target = next((row.file for row in rows if row.file.endswith(".py")), None)
    if target is None:
        raise DriverRefusal(
            "the null control needs a Python target and no row names one; "
            "the control is what proves the apparatus, so the batch cannot run without it"
        )
    return Row(
        id="NULL_CONTROL",
        description=(
            "Automatic control: append a comment line to "
            f"{target}. Semantically empty, so it must kill zero. Any death here "
            "means the measuring apparatus is broken, not the code."
        ),
        file=target,
        old="",
        new=NULL_CONTROL_COMMENT,
        kind="null-control",
    )


# ---------------------------------------------------------------------------
# Git, read only, always
# ---------------------------------------------------------------------------


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args], cwd=repo_root, capture_output=True, check=False
    )


def git_head_bytes(repo_root: Path, rel: str) -> bytes:
    """The committed bytes of one tracked path, from HEAD."""
    done = _git(repo_root, "show", f"HEAD:{rel}")
    if done.returncode != 0:
        raise DriverRefusal(
            f"cannot read HEAD:{rel} ({done.stderr.decode('utf-8', 'replace').strip()}); "
            f"a mutation target must be tracked and committed, because an "
            f"uncommitted edit is exactly what the restore check cannot see"
        )
    return done.stdout


def verify_restore(repo_root: Path, rel: str) -> None:
    """Raise unless the file on disk matches HEAD byte for byte."""
    on_disk = (repo_root / rel).read_bytes()
    committed = git_head_bytes(repo_root, rel)
    if on_disk != committed:
        raise RestoreVerificationError(
            f"{rel} does not match git show HEAD after restore: "
            f"{len(on_disk)} bytes on disk against {len(committed)} committed. "
            f"Stop and inspect the file. Every later row in this batch would be "
            f"measured against a contaminated tree."
        )


def dirty_targets(repo_root: Path, rels: list[str]) -> list[str]:
    """Which of ``rels`` have uncommitted changes."""
    if not rels:
        return []
    done = _git(repo_root, "status", "--porcelain", "--", *rels)
    if done.returncode != 0:
        raise DriverRefusal(f"git status failed: {done.stderr.decode('utf-8', 'replace').strip()}")
    found: list[str] = []
    for line in done.stdout.decode("utf-8", "replace").splitlines():
        entry = line[3:].strip()
        if entry:
            found.append(entry.split(" -> ")[-1])
    return found


def head_sha(repo_root: Path) -> str:
    done = _git(repo_root, "rev-parse", "--short", "HEAD")
    return done.stdout.decode("utf-8", "replace").strip() or "unknown"


def branch_name(repo_root: Path) -> str:
    done = _git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    return done.stdout.decode("utf-8", "replace").strip() or "unknown"


# ---------------------------------------------------------------------------
# The file surgery
# ---------------------------------------------------------------------------


def apply_mutation(text: str, old: str, new: str, *, allow_append: bool = False) -> str:
    """Return ``text`` with ``old`` replaced by ``new``, or refuse.

    Absent text and ambiguous text are both refusals rather than best efforts. A
    replacement that hit the wrong one of two identical sites still produces a
    number, and the number is about an experiment nobody chose to run.
    """
    if old == "":
        if not allow_append:
            raise DriverRefusal("empty old text is reserved for the null control row")
        return text + new
    count = text.count(old)
    if count == 0:
        raise DriverRefusal(
            "old text is not present in the target; the row cannot be applied. "
            "Copy the text out of the file rather than retyping it."
        )
    if count > 1:
        raise DriverRefusal(
            f"old text appears {count} times in the target, so the site is ambiguous. "
            f"Widen the old text with surrounding lines until it is unique."
        )
    return text.replace(old, new, 1)


@contextmanager
def mutated(
    repo_root: Path,
    rel: str,
    old: str,
    new: str,
    *,
    allow_append: bool = False,
    head_verify: bool = True,
):
    """Apply a mutation for the duration of the block, then always restore.

    The ``finally`` is the point. It runs on a normal exit, on any exception,
    and on KeyboardInterrupt, so no path through this block leaves a mutated
    file on disk. The restore is verified against HEAD inside the same
    ``finally``, because a restore nobody checked is a hope.

    ``head_verify=False`` is the ONLY concession, and it is reserved for a
    target the caller explicitly declared dirty. It falls back to comparing
    against the in-memory snapshot, which is a weaker check for the reason
    METHOD names: a copy certifying itself. The output says so per row rather
    than letting the weaker guarantee pass as the stronger one.
    """
    path = repo_root / rel
    snapshot = path.read_bytes()
    # Applied before any write, so a refused row never touches the file.
    mutant = apply_mutation(snapshot.decode("utf-8"), old, new, allow_append=allow_append)
    path.write_bytes(mutant.encode("utf-8"))
    try:
        yield path
    finally:
        path.write_bytes(snapshot)
        if head_verify:
            verify_restore(repo_root, rel)
        elif path.read_bytes() != snapshot:
            raise RestoreVerificationError(f"{rel} does not match its own snapshot after restore")


# ---------------------------------------------------------------------------
# Subset derivation
# ---------------------------------------------------------------------------


def dotted_module(rel: str, src_root: str = "src") -> str | None:
    """The dotted import path for a source file, or None if it is not one."""
    prefix = f"{src_root}/"
    if not rel.startswith(prefix) or not rel.endswith(".py"):
        return None
    parts = rel[len(prefix) : -len(".py")].split("/")
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts) if parts else None


def imported_modules(source: str) -> set[str]:
    """Every module path a source file imports, lazy imports included.

    ``from pkg.mod import name`` contributes both ``pkg.mod`` and
    ``pkg.mod.name``, because from the outside there is no telling whether the
    imported name is a submodule or a symbol, and the caller only ever asks
    whether a known module is in the set.
    """
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            found.add(node.module)
            found.update(f"{node.module}.{alias.name}" for alias in node.names)
    return found


def derive_subset(
    repo_root: Path, rel: str, *, src_root: str = "src", tests_root: str = "tests"
) -> tuple[list[str] | None, str]:
    """Return ``(test paths, why)``, where None means the whole suite.

    Three cases, in order. A test file is its own subset. A source module's
    subset is the test files importing it. Anything else, a script or a
    document, falls back to the test files mentioning its name.
    """
    if rel.startswith(f"{tests_root}/"):
        return [rel], "the mutated test file itself"

    candidates = sorted((repo_root / tests_root).rglob("test_*.py"))
    dotted = dotted_module(rel, src_root=src_root)
    picked: list[str] = []

    if dotted:
        for path in candidates:
            try:
                names = imported_modules(path.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue
            if dotted in names or any(name.startswith(f"{dotted}.") for name in names):
                picked.append(path.relative_to(repo_root).as_posix())
        why = f"test files importing {dotted}"
    else:
        needle = Path(rel).name
        for path in candidates:
            if needle in path.read_text(encoding="utf-8", errors="replace"):
                picked.append(path.relative_to(repo_root).as_posix())
        why = f"test files naming {needle}"

    if not picked:
        return None, f"full suite ({why}: none found)"
    return picked, why


# ---------------------------------------------------------------------------
# Running pytest
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunResult:
    collected: int
    failed: tuple[str, ...]
    errored: tuple[str, ...]
    collect_errors: tuple[str, ...]
    exit_code: int

    @property
    def deaths(self) -> int:
        return len(set(self.failed) | set(self.errored))

    @property
    def is_green(self) -> bool:
        return not (self.failed or self.errored or self.collect_errors)

    def failure_ids(self) -> list[str]:
        return sorted(set(self.failed) | set(self.errored))


def pytest_addopts(repo_root: Path) -> str:
    """``addopts`` from pyproject with every quiet flag removed.

    Stripping rather than clearing: clearing would silently drop a future
    addition to ``addopts``, and stripping removes only the flag that is
    actively harmful here. A second ``-q`` becomes ``-qq`` and suppresses the
    summary line, which is how a hand rolled driver comes to report zero.
    """
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        return ""
    with pyproject.open("rb") as handle:
        data = tomllib.load(handle)
    raw = data.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("addopts", "")
    if isinstance(raw, list):
        tokens = [str(one) for one in raw]
    else:
        tokens = shlex.split(str(raw))
    return " ".join(token for token in tokens if token not in {"-q", "-qq", "--quiet"})


def installation_state_roots() -> tuple[Path, ...]:
    """The REAL installation-scoped directories, resolved as the product resolves them.

    Read from THIS process's environment, which no mutation touches, and resolved
    once before any child runs.

    The two Cratekit overrides win over platformdirs, exactly as the product's
    config module reads them, and that is what makes this guard safe to exercise
    from the test suite: under pytest the conftest has already pointed both at
    that test's own temporary roots, so the driver guards a temp directory and
    never the machine's own. Run for real, this process carries neither variable
    and the true platformdirs path is resolved.

    macOS answers both platformdirs calls with one directory, so the result is
    deduplicated and is not always two entries long.

    These two are what the guard WATCHES. The sandbox in ``SANDBOXED_ENV`` points
    a child away from more than these, HOME and the data root among them, and a
    child reaching one of those, the real trash directory say, is not seen here.
    The table says so in as many words rather than claiming the whole home was
    guarded.
    """
    config_override = os.environ.get("CRATEKIT_CONFIG_DIR")
    state_override = os.environ.get("CRATEKIT_STATE_DIR")
    roots = (
        Path(config_override)
        if config_override
        else Path(platformdirs.user_config_dir(APP_NAME)),
        Path(state_override)
        if state_override
        else Path(platformdirs.user_state_dir(APP_NAME)),
    )
    return tuple(dict.fromkeys(roots))


#: Files at or under this size are hashed by content as well as by stat. A
#: configuration is a few hundred bytes and is the file whose overwrite this
#: guard exists to catch, and a stat alone misses a same-size rewrite inside one
#: timestamp tick on a filesystem with coarse timestamps. A job queue is
#: megabytes and is left to its stat, because hashing it once per child to learn
#: a fact ``st_mtime_ns`` already answers on this machine is time spent for
#: nothing.
SMALL_FILE_BYTES = 64 * 1024


def state_fingerprint(root: Path) -> tuple[str, int]:
    """Digest everything under ``root``. Returns (digest, entry count).

    Every directory and file is an entry, by relative path. A file carries its
    size, inode, mtime and ctime, and a small one carries a content hash too,
    see ``SMALL_FILE_BYTES``. A directory is an entry in its own right, so a
    child that creates an empty one inside the real root has reached the real
    path and is seen, even on the pass where it writes no file into it.

    ``lstat``, not ``stat``: a symlink is fingerprinted as itself, so repointing
    one at a different target is a change rather than an invisible one.

    Whether the root itself EXISTS is part of the digest, for the same reason a
    directory inside it is.
    """
    entries: list[str] = [f"exists={root.is_dir()}"]
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        here = Path(current)
        for name in dirnames:
            entries.append(f"{(here / name).relative_to(root).as_posix()}\tdir")
        for name in sorted(filenames):
            path = here / name
            relative = path.relative_to(root).as_posix()
            try:
                info = path.lstat()
            except OSError:
                # Unreadable is still a fact about the tree, and swallowing it
                # would let a file that cannot be stat'd hide a change.
                entries.append(f"{relative}\tunreadable")
                continue
            line = (
                f"{relative}\t{info.st_size}\t{info.st_ino}"
                f"\t{info.st_mtime_ns}\t{info.st_ctime_ns}"
            )
            if info.st_size <= SMALL_FILE_BYTES and not os.path.islink(path):
                try:
                    line += "\t" + hashlib.sha256(path.read_bytes()).hexdigest()
                except OSError:
                    line += "\tunreadable-content"
            entries.append(line)
    digest = hashlib.sha256("\n".join(entries).encode("utf-8")).hexdigest()
    # The existence marker is not an entry in the tree, so it is not counted.
    return digest, len(entries) - 1


@dataclass(frozen=True)
class StateGuard:
    """The real installation state as it stood before any child of this batch ran."""

    roots: tuple[Path, ...]
    digests: tuple[str, ...]
    counts: tuple[int, ...]

    def describe(self) -> str:
        return "; ".join(
            f"{root} ({count} entries)"
            for root, count in zip(self.roots, self.counts, strict=True)
        )


def take_state_guard(roots: tuple[Path, ...] | None = None) -> StateGuard:
    """Fingerprint the real installation state before the batch touches anything."""
    resolved = installation_state_roots() if roots is None else tuple(roots)
    taken = [state_fingerprint(root) for root in resolved]
    return StateGuard(
        roots=resolved,
        digests=tuple(digest for digest, _ in taken),
        counts=tuple(count for _, count in taken),
    )


def check_state_guard(guard: StateGuard, *, label: str) -> None:
    """Raise ``StateLeak`` if the real installation state moved under a child.

    The comparison is against the batch's starting fingerprint, and the driver
    cannot tell a child's write from a concurrent one: a ``crate`` run in another
    terminal writes a run record into the same directory and trips this exactly
    as a leak would. The batch still stops, because either way the machine is
    no longer the one the batch started on, but the message says which of the
    two it could not tell rather than accusing the row outright.
    """
    for root, before, counted in zip(guard.roots, guard.digests, guard.counts, strict=True):
        now, count_now = state_fingerprint(root)
        if now == before:
            continue
        raise StateLeak(
            f"the real installation state changed while running {label}. "
            f"{root} held {counted} entries before this child and holds "
            f"{count_now} now. Either a child of this driver reached the real "
            "machine, which is R-343 and on 2026-09-20 overwrote a real "
            "configuration with a fixture one, or something else wrote there "
            "while the child ran, and the driver cannot tell which. The batch is "
            "stopped and nothing after this point was measured. Read that "
            "directory before rerunning, and rerun with nothing else using it."
        )


def run_pytest(
    repo_root: Path,
    paths: list[str] | None,
    *,
    timeout: int = 3600,
    guard: StateGuard | None = None,
    label: str = "a child run",
) -> RunResult:
    """Run pytest once, synchronously, and read the result off report objects."""
    with tempfile.TemporaryDirectory(prefix="mutate-run-") as tmp:
        workspace = Path(tmp)
        (workspace / f"{PLUGIN_MODULE}.py").write_text(PLUGIN_SOURCE, encoding="utf-8")
        report_path = workspace / "report.json"

        # INHERIT, then add. Never a fresh dict: a hand-built environment is how
        # ffmpeg fell off PATH and reddened 28 audio tests under a driver whose
        # subset rows all looked fine.
        env = os.environ.copy()
        # Non-negotiable: identical byte lengths a second apart otherwise make
        # CPython serve the previous mutation's cached bytecode.
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["MUTATE_REPORT_PATH"] = str(report_path)
        env["PYTHONPATH"] = os.pathsep.join(
            [str(workspace), env.get("PYTHONPATH", "")]
        ).rstrip(os.pathsep)
        # The child starts life in a throwaway installation state, so that a test
        # which undoes the conftest's isolation lands here rather than on the real
        # machine. R-343, and see SANDBOXED_ENV.
        sandbox = workspace / "installation-state"
        for name, relative in SANDBOXED_ENV.items():
            path = sandbox / relative
            path.mkdir(parents=True, exist_ok=True)
            env[name] = str(path)
        for name in SCRUBBED_ENV:
            env.pop(name, None)

        command = [
            sys.executable,
            "-m",
            "pytest",
            "-p",
            PLUGIN_MODULE,
            "-p",
            "no:cacheprovider",
            "--tb=no",
            "-o",
            f"addopts={pytest_addopts(repo_root)}",
        ]
        command += paths or []

        try:
            done = subprocess.run(
                command,
                cwd=repo_root,
                env=env,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout,
            )
        finally:
            # In a finally, so a child that leaks and then hangs past the
            # timeout is still checked: TimeoutExpired would otherwise leave
            # here first, the row loop would file it as an ordinary error row,
            # and the NEXT row's child would be the one blamed. A leak raised
            # from here outranks the timeout it interrupts, on purpose. It also
            # outranks a missing report: the report says what was measured, and
            # this says whether the machine it was measured on is still the one
            # the batch started on.
            if guard is not None:
                check_state_guard(guard, label=label)
        if not report_path.is_file():
            raise MeasurementFailure(
                "pytest produced no report file, so nothing was measured. "
                f"exit {done.returncode}\n{done.stdout[-2000:]}\n{done.stderr[-2000:]}"
            )
        state = json.loads(report_path.read_text(encoding="utf-8"))

    # 3 internal error, 4 usage error, 5 nothing collected. Each of these comes
    # back with an EMPTY report: zero collected, zero failures, nothing flagged.
    # Read as a RunResult it is indistinguishable from a green run, so a subset
    # path with a typo in it would report a serene zero for every row that named
    # it. Exit 2 is deliberately NOT here: that is how a collection error
    # arrives, and a collection error is a measurement this driver wants.
    if done.returncode in {3, 4, 5}:
        raise MeasurementFailure(
            f"pytest exited {done.returncode} and nothing was measured. That is a "
            f"usage, internal or empty-collection failure, not a zero row.\n"
            f"{done.stdout[-1500:]}\n{done.stderr[-1500:]}"
        )

    return RunResult(
        collected=int(state["collected"]),
        failed=tuple(state["failed"]),
        errored=tuple(state["errored"]),
        collect_errors=tuple(state["collect_errors"]),
        exit_code=done.returncode,
    )


# ---------------------------------------------------------------------------
# Measuring
# ---------------------------------------------------------------------------


@dataclass
class RowResult:
    id: str
    description: str
    file: str
    kind: str
    surface: str
    pairs_with: str | None
    fingerprint: str
    subset: list[str] | None
    subset_reason: str
    status: str
    deaths: int
    collected: int
    baseline_collected: int
    collect_drift: bool
    collect_errors: list[str] = field(default_factory=list)
    killed: list[str] = field(default_factory=list)
    promoted: bool = False
    subset_deaths: int | None = None
    note: str = ""
    runs: int = 0
    head_verified: bool = True
    old: str = ""
    new: str = ""

    def to_dict(self) -> dict:
        return dict(self.__dict__)


def measure_row(
    repo_root: Path,
    row: Row,
    subset: list[str] | None,
    subset_reason: str,
    subset_baseline: RunResult,
    full_baseline: RunResult,
    *,
    timeout: int = 3600,
    head_verify: bool = True,
    guard: StateGuard | None = None,
) -> RowResult:
    """Apply one row, measure it, restore it, and describe what happened."""
    common = dict(
        id=row.id,
        description=row.description,
        file=row.file,
        kind=row.kind,
        surface=row.surface,
        pairs_with=row.pairs_with,
        fingerprint=row.fingerprint(),
        subset=list(subset) if subset else None,
        subset_reason=subset_reason,
        old=row.old,
        new=row.new,
        head_verified=head_verify,
    )

    try:
        with mutated(
            repo_root,
            row.file,
            row.old,
            row.new,
            allow_append=row.kind == "null-control",
            head_verify=head_verify,
        ):
            result = run_pytest(
                repo_root, subset, timeout=timeout, guard=guard, label=f"row {row.id}"
            )
            promoted = False
            final = result
            if (
                subset is not None
                and result.deaths == 0
                and not result.collect_errors
                and result.collected == subset_baseline.collected
            ):
                # A zero on a subset is not yet a zero.
                final = run_pytest(
                    repo_root,
                    None,
                    timeout=timeout,
                    guard=guard,
                    label=f"row {row.id}, promoted to the full suite",
                )
                promoted = True
    except DriverRefusal as refusal:
        return RowResult(
            status="refused",
            deaths=0,
            collected=0,
            baseline_collected=subset_baseline.collected,
            collect_drift=False,
            note=str(refusal),
            runs=0,
            **common,
        )

    reference = full_baseline if promoted else subset_baseline
    drift = final.collected != reference.collected
    if final.collect_errors or drift:
        status = "collect-error"
        note = (
            f"collection changed: {final.collected} collected against a baseline of "
            f"{reference.collected}. A file that fails to collect takes its tests "
            f"with it and the run still looks green, so this is not a zero."
        )
    elif final.deaths:
        status = "killed"
        note = ""
    else:
        status = "zero"
        note = "confirmed on the full suite" if promoted else "measured on the full suite"

    return RowResult(
        status=status,
        deaths=final.deaths,
        collected=final.collected,
        baseline_collected=reference.collected,
        collect_drift=drift,
        collect_errors=list(final.collect_errors),
        killed=final.failure_ids(),
        promoted=promoted,
        subset_deaths=result.deaths if promoted else None,
        note=note,
        runs=2 if promoted else 1,
        **common,
    )


@dataclass
class Batch:
    name: str
    pass_kind: str
    branch: str
    head: str
    when: str
    valid: bool
    invalid_reason: str
    baseline_collected: int
    baseline_exit: int
    control: RowResult | None
    results: list[RowResult]
    dropped: list[Dropped]
    pytest_runs: int
    state_guarded: str = ""
    reused_rows: int = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "pass_kind": self.pass_kind,
            "branch": self.branch,
            "head": self.head,
            "when": self.when,
            "valid": self.valid,
            "invalid_reason": self.invalid_reason,
            "baseline_collected": self.baseline_collected,
            "baseline_exit": self.baseline_exit,
            "pytest_runs": self.pytest_runs,
            "state_guarded": self.state_guarded,
            "reused_rows": self.reused_rows,
            "control": self.control.to_dict() if self.control else None,
            "rows": [one.to_dict() for one in self.results],
            "dropped": [one.__dict__ for one in self.dropped],
        }


def measure_batch(
    repo_root: Path,
    name: str,
    rows: list[Row],
    dropped: list[Dropped] | None = None,
    *,
    pass_kind: str = "full",
    allow_dirty: bool = False,
    timeout: int = 3600,
    prior: dict | None = None,
    progress_path: Path | None = None,
    guard: StateGuard | None = None,
) -> Batch:
    """Run a whole batch: preflight, baselines, the control, then the rows.

    ``progress_path`` is rewritten after EVERY row, not at the end. A batch on
    this suite is minutes long, and a sidecar written only on success means an
    interrupted batch resumes from nothing, which is the same as not being
    resumable.
    """
    dropped = list(dropped or [])
    runs = 0
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = dict(
        name=name,
        pass_kind=pass_kind,
        branch=branch_name(repo_root),
        head=head_sha(repo_root),
        when=when,
        dropped=dropped,
    )

    control = null_control_row(rows)
    targets = sorted({row.file for row in [*rows, control]})
    for rel in targets:
        if not (repo_root / rel).is_file():
            raise DriverRefusal(f"row target does not exist: {rel}")
        git_head_bytes(repo_root, rel)  # refuses an untracked or uncommitted target

    dirty = dirty_targets(repo_root, targets)
    if dirty and not allow_dirty:
        raise DriverRefusal(
            f"uncommitted changes to mutation targets: {', '.join(dirty)}. "
            f"Restores are verified against git show HEAD, which cannot see an "
            f"uncommitted edit, so the verification would either fail on every row "
            f"or certify the wrong bytes. Commit them, or pass --allow-dirty and "
            f"accept that the restore check is measuring against HEAD."
        )

    # Taken AFTER preflight and before the first child, so the fingerprint
    # describes the machine as the batch found it. R-343.
    if guard is None:
        guard = take_state_guard()
    header["state_guarded"] = guard.describe()

    # ---- baselines ------------------------------------------------------
    full_baseline = run_pytest(
        repo_root, None, timeout=timeout, guard=guard, label="the full baseline"
    )
    runs += 1
    if not full_baseline.is_green:
        detail = ", ".join(full_baseline.failure_ids()[:10]) or ", ".join(
            full_baseline.collect_errors[:10]
        )
        raise DriverRefusal(
            f"BASELINE IS NOT GREEN: {full_baseline.deaths} failing, "
            f"{len(full_baseline.collect_errors)} collection errors, "
            f"{full_baseline.collected} collected. THE BATCH IS INVALID and no row "
            f"ran. Every row measured against this would read as a death, including "
            f"rows that cannot kill anything.\n"
            f"Failing: {detail}\n"
            f"Before suspecting the code, suspect the ENVIRONMENT. A red baseline "
            f"here has twice been a missing binary rather than a broken tree: a "
            f"trimmed PATH dropped ffmpeg and reddened 28 audio tests on the full "
            f"run while every subset row stayed green, which reads as selective "
            f"damage and is not. Run the suite by hand in this shell first."
        )

    plans: list[tuple[Row, list[str] | None, str]] = []
    for row in rows:
        if row.tests:
            plans.append((row, list(row.tests), "explicit subset from the row"))
        else:
            subset, why = derive_subset(repo_root, row.file)
            plans.append((row, subset, why))

    subset_baselines: dict[tuple[str, ...], RunResult] = {}
    for _, subset, _ in plans:
        if subset is None:
            continue
        key = tuple(subset)
        if key not in subset_baselines:
            measured = run_pytest(
                repo_root,
                list(subset),
                timeout=timeout,
                guard=guard,
                label=f"the subset baseline for {', '.join(subset)}",
            )
            runs += 1
            if not measured.is_green:
                raise DriverRefusal(
                    f"the subset baseline for {', '.join(subset)} is not green: "
                    f"{', '.join(measured.failure_ids()[:10]) or 'collection error'}. "
                    f"Every row measured against it would read as a death."
                )
            subset_baselines[key] = measured

    # ---- the control ----------------------------------------------------
    control_result = measure_row(
        repo_root,
        control,
        None,
        "full suite",
        full_baseline,
        full_baseline,
        timeout=timeout,
        head_verify=control.file not in set(dirty),
        guard=guard,
    )
    runs += control_result.runs
    if control_result.deaths or control_result.status != "zero":
        return Batch(
            valid=False,
            invalid_reason=(
                f"the null control killed {control_result.deaths} and collected "
                f"{control_result.collected} against a baseline of "
                f"{full_baseline.collected}. A change with no semantic content "
                f"cannot kill a test, so the apparatus is what is broken, not the "
                f"code. Every row in this batch would be wrong in the same "
                f"direction. Stop and find the environmental cause."
            ),
            baseline_collected=full_baseline.collected,
            baseline_exit=full_baseline.exit_code,
            control=control_result,
            results=[],
            pytest_runs=runs,
            **header,
        )

    # ---- the rows -------------------------------------------------------
    reused = {
        entry["fingerprint"]: entry
        for entry in (prior or {}).get("rows", [])
        if entry.get("status") not in {None, "error"}
    }
    results: list[RowResult] = []
    for row, subset, why in plans:
        cached = reused.get(row.fingerprint())
        if cached is not None and cached.get("id") == row.id:
            results.append(RowResult(**cached))
            header["reused_rows"] = header.get("reused_rows", 0) + 1
            continue
        baseline = subset_baselines[tuple(subset)] if subset is not None else full_baseline
        try:
            results.append(
                measure_row(
                    repo_root,
                    row,
                    subset,
                    why,
                    baseline,
                    full_baseline,
                    timeout=timeout,
                    head_verify=row.file not in set(dirty),
                    guard=guard,
                )
            )
        except RestoreVerificationError:
            raise
        except StateLeak:
            # Must outrank the blanket handler below. Recorded as an error row,
            # a leak would read as one unremarkable row and the loop would keep
            # spending children against a machine it had just damaged.
            raise
        except KeyboardInterrupt:
            raise
        except Exception as failure:  # noqa: BLE001 - recorded, never swallowed silently
            results.append(
                RowResult(
                    id=row.id,
                    description=row.description,
                    file=row.file,
                    kind=row.kind,
                    surface=row.surface,
                    pairs_with=row.pairs_with,
                    fingerprint=row.fingerprint(),
                    subset=list(subset) if subset else None,
                    subset_reason=why,
                    status="error",
                    deaths=0,
                    collected=0,
                    baseline_collected=baseline.collected,
                    collect_drift=False,
                    note=f"{type(failure).__name__}: {failure}",
                    runs=1,
                    old=row.old,
                    new=row.new,
                )
            )
        runs += results[-1].runs
        if progress_path is not None:
            partial = Batch(
                valid=True,
                invalid_reason="in progress",
                baseline_collected=full_baseline.collected,
                baseline_exit=full_baseline.exit_code,
                control=control_result,
                results=results,
                pytest_runs=runs,
                **header,
            )
            progress_path.parent.mkdir(parents=True, exist_ok=True)
            progress_path.write_text(
                json.dumps(partial.to_dict(), indent=2) + "\n", encoding="utf-8"
            )

    return Batch(
        valid=True,
        invalid_reason="",
        baseline_collected=full_baseline.collected,
        baseline_exit=full_baseline.exit_code,
        control=control_result,
        results=results,
        pytest_runs=runs,
        **header,
    )


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def composite_note(batch: Batch, result: RowResult) -> str:
    """What a zero row owes, per METHOD's severity floor.

    A zero on a USER FACING guard is acceptable only when a composite shows what
    the guard does hold. A zero on a maintainer facing guard gets one line,
    because the floor says such a row can never block a merge and a composite
    there buys documentation rather than a decision.
    """
    if result.status != "zero":
        return ""
    if result.surface != "user":
        return "maintainer facing, composite not required"
    pair = next((one for one in batch.results if one.pairs_with == result.id), None)
    if pair is None:
        return "USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it"
    return f"paired with `{pair.id}`, which killed {pair.deaths}"


def _block(text: str, limit: int = 1200) -> str:
    body = text if len(text) <= limit else text[:limit] + "\n... truncated ..."
    return "```\n" + (body if body.strip() else "(empty)") + "\n```"


def render_markdown(batch: Batch) -> str:
    lines: list[str] = []
    add = lines.append

    add(f"# Mutation table: {batch.name}")
    add("")
    add(
        f"Measured by `scripts/mutate.py` on {batch.when}, branch `{batch.branch}` "
        f"at `{batch.head}`. Pass kind: {batch.pass_kind}."
    )
    add("")
    add(
        f"Baseline: green, {batch.baseline_collected} collected. "
        f"pytest invocations for this batch: {batch.pytest_runs}."
    )
    add("")
    add(
        "Environment: inherited from the calling shell, then added to. Added: "
        + "; ".join(ADDED_ENV)
        + ". Removed: "
        + "; ".join(f"{name} ({why})" for name, why in SCRUBBED_ENV.items())
        + ". Nothing else was scrubbed, because a hand built environment is how a "
        "missing binary reddens a baseline and every row after it."
    )
    add("")
    if batch.state_guarded:
        reused = (
            f" {batch.reused_rows} row(s) were reused from a prior sidecar and were "
            "measured by an earlier process, whose children this run did not watch."
            if batch.reused_rows
            else ""
        )
        add(
            "Installation state: the watched roots are unchanged. Fingerprinted "
            "before the first child this run started and after every one of "
            f"them: {batch.state_guarded}. A change would have stopped the batch "
            "at the child that was running. Every child ran with its own throwaway "
            "installation state, so a test that undoes the suite's isolation "
            "lands there rather than on this machine (R-343). Only those roots "
            "are watched; the sandbox also redirects HOME and the data root, and "
            f"a child reaching one of those is not seen by this guard.{reused}"
        )
        add("")

    if not batch.valid:
        add("## THIS BATCH IS INVALID")
        add("")
        add(batch.invalid_reason)
        add("")
        return "\n".join(lines) + "\n"

    control = batch.control
    if control is not None:
        add(
            f"Null control `{control.id}`: killed {control.deaths}, collected "
            f"{control.collected} against {control.baseline_collected}. The control "
            f"is a semantically empty change, so a zero here is what makes every "
            f"other number in this table believable."
        )
        add("")

    add("## Summary")
    add("")
    add("| id | file | surface | subset | collected | kills | status |")
    add("| --- | --- | --- | --- | --- | --- | --- |")
    for one in batch.results:
        subset = "full suite" if one.subset is None else f"{len(one.subset)} file(s)"
        kills = "collection error" if one.status == "collect-error" else str(one.deaths)
        if one.promoted:
            kills += " (promoted)"
        add(
            f"| `{one.id}` | `{one.file}` | {one.surface} | {subset} | "
            f"{one.collected} | {kills} | {one.status} |"
        )
    add("")

    zeros = [one for one in batch.results if one.status == "zero"]
    if zeros:
        add("## Zero rows and what they owe")
        add("")
        for one in zeros:
            add(f"- `{one.id}` ({one.surface} facing): {composite_note(batch, one)}")
        add("")

    if batch.dropped:
        add("## Considered and dropped")
        add("")
        add(
            f"METHOD caps a {batch.pass_kind} pass at {ROW_CAPS[batch.pass_kind]} rows. "
            f"These were ranked below the cap and NOT measured. They are not coverage."
        )
        add("")
        for one in batch.dropped:
            add(f"- `{one.id}`: {one.description} Dropped because: {one.reason}")
        add("")

    add("## Row definitions")
    add("")
    for one in batch.results:
        add(f"### `{one.id}`")
        add("")
        add(one.description)
        add("")
        add(f"- File: `{one.file}`")
        add(f"- Surface: {one.surface}")
        add(f"- Subset: {one.subset_reason}")
        if one.subset:
            add(f"- Ran: {', '.join(f'`{path}`' for path in one.subset)}")
        add(f"- Collected: {one.collected} against a baseline of {one.baseline_collected}")
        add(f"- Kills: {one.deaths} ({one.status})")
        if one.promoted:
            add(f"- Promoted: subset killed {one.subset_deaths}, full suite killed {one.deaths}")
        if one.note:
            add(f"- Note: {one.note}")
        if not one.head_verified:
            add(
                "- WEAKER RESTORE CHECK: this target was dirty and --allow-dirty was "
                "passed, so the restore was verified against the in-memory snapshot "
                "rather than against git show HEAD."
            )
        if one.pairs_with:
            add(f"- Composite for: `{one.pairs_with}`")
        if one.killed:
            shown = one.killed[:15]
            add("- Killed:")
            for node in shown:
                add(f"  - `{node}`")
            if len(one.killed) > len(shown):
                add(f"  - ... and {len(one.killed) - len(shown)} more, see the JSON sidecar")
        if one.collect_errors:
            add(f"- Collection errors: {', '.join(f'`{e}`' for e in one.collect_errors)}")
        add("")
        add("Old text:")
        add("")
        add(_block(one.old))
        add("")
        add("New text:")
        add("")
        add(_block(one.new))
        add("")

    return "\n".join(lines) + "\n"


def write_outputs(batch: Batch, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    markdown = out_dir / f"{batch.name}.md"
    sidecar = out_dir / f"{batch.name}.json"
    markdown.write_text(render_markdown(batch), encoding="utf-8")
    sidecar.write_text(json.dumps(batch.to_dict(), indent=2) + "\n", encoding="utf-8")
    return markdown, sidecar


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Measure a mutation table from a row file.")
    parser.add_argument("spec", type=Path, help="a .toml or .json row file")
    parser.add_argument("--name", default=None, help="output name; defaults to the spec's")
    parser.add_argument("--out-dir", type=Path, default=REPO_ROOT / "docs" / "mutation")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="measure with uncommitted changes to a target; the restore check still uses HEAD",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="reuse rows already in the JSON sidecar whose text has not changed",
    )
    parser.add_argument("--timeout", type=int, default=3600, help="seconds per pytest run")
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])
    try:
        name, pass_kind, rows, dropped = load_spec(args.spec)
    except DriverRefusal as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 2
    name = args.name or name

    prior = None
    sidecar = args.out_dir / f"{name}.json"
    if args.resume and sidecar.is_file():
        prior = json.loads(sidecar.read_text(encoding="utf-8"))

    try:
        batch = measure_batch(
            args.repo_root,
            name,
            rows,
            dropped,
            pass_kind=pass_kind,
            allow_dirty=args.allow_dirty,
            timeout=args.timeout,
            prior=prior,
            progress_path=sidecar,
        )
    except DriverRefusal as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 2
    except RestoreVerificationError as broken:
        print(f"RESTORE FAILED: {broken}", file=sys.stderr)
        return 3
    except StateLeak as leak:
        print(f"STATE LEAK: {leak}", file=sys.stderr)
        return 6
    except MeasurementFailure as broken:
        print(f"NOTHING MEASURED: {broken}", file=sys.stderr)
        return 5

    markdown, written = write_outputs(batch, args.out_dir)
    print(f"table:   {markdown}")
    print(f"sidecar: {written}")
    if not batch.valid:
        print(f"INVALID BATCH: {batch.invalid_reason}", file=sys.stderr)
        return 4
    for one in batch.results:
        print(f"{one.id:<28} {one.status:<14} kills={one.deaths} collected={one.collected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
