#!/usr/bin/env python3
"""Mutation table driver. Rows go in as data, a measured table comes out.

Each row is applied as an exact string replacement, its test subset run, its
deaths counted off pytest report objects, and the file restored and verified
against `git show HEAD`. Run as `scripts/mutate.py rows.toml [--name N] [--resume]
[--known-failures FILE]`; it writes `docs/mutation/<name>.md` and `.json`.

A row file, TOML or JSON, holds `name`, `pass_kind` and `[[rows]]` (`id`,
`description`, `file`, `old`, `new`, optional `tests`, `surface`, `pairs_with`),
and `[[dropped]]` with a `reason`. `light` caps at 25 rows and `full` at 45;
`replay` (U297) has none, since each row names the recorded table and id in
`source`, says `moved` when its text differs, and may carry `[[mapped]]` entries.
Each batch takes a green baseline (U271 may read it from the cloud battery), a
null control that must kill zero, and promotes a zero to the full suite. The
rules, and why, are METHOD's Driver rules and The mutation table in
`docs/METHOD.md`. What runs no test is in `scripts/mutate_table.py`.

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
import hashlib
import importlib.util
import json
import os
import shlex
import socket
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import platformdirs

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load(filename: str, name: str):
    """A script beside this one, loaded by path and registered, since it declares dataclasses."""
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


#: The battery's places for temporary files, one definition for the battery and the driver.
BATTERY = _load("cloud_battery.py", "cratekit_cloud_battery_places")
_table = _load("mutate_table.py", "cratekit_mutate_table")

ROW_CAPS, REPLAY, PASS_KINDS = _table.ROW_CAPS, _table.REPLAY, _table.PASS_KINDS
DriverRefusal, RestoreVerificationError = _table.DriverRefusal, _table.RestoreVerificationError
MeasurementFailure, StateLeak = _table.MeasurementFailure, _table.StateLeak
Row, Dropped, Mapped = _table.Row, _table.Dropped, _table.Mapped
read_source, read_spec = _table.read_source, _table.read_spec
refuse_unrecorded_sources = _table.refuse_unrecorded_sources
_git, git_head_bytes, verify_restore = _table._git, _table.git_head_bytes, _table.verify_restore
dirty_targets, head_sha, branch_name = _table.dirty_targets, _table.head_sha, _table.branch_name
apply_mutation, mutated = _table.apply_mutation, _table.mutated
dotted_module, derive_subset = _table.dotted_module, _table.derive_subset
RunResult, RowResult, Batch = _table.RunResult, _table.RowResult, _table.Batch
composite_note = _table.composite_note

#: Appended by the null control row: invisible to the interpreter and to an AST walk.
NULL_CONTROL_COMMENT = "\n# mutation driver null control, restored automatically\n"

PLUGIN_MODULE = "mutate_report_plugin"

#: Environment variables REMOVED from the child, which otherwise inherits
#: ``os.environ`` whole, and why. Named in the table: a silent scrub is a defect.
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

#: What every child is pointed AWAY from, into a sandbox in its workspace (R-343), so a
#: test undoing the suite's isolation lands there. The app name is not imported from a target.
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
    # U278: the provider gate never follows CRATEKIT_STATE_DIR, so it has its own.
    "CRATEKIT_PROVIDER_GATE_DIR": f"state/{APP_NAME}",
}

#: Added on top of the inherited environment, never as a fresh dict.
ADDED_ENV = (
    "PYTHONDONTWRITEBYTECODE=1",
    "PYTHONPATH (the plugin's temp directory, prepended)",
    "MUTATE_REPORT_PATH (the plugin's output file)",
    "TMPDIR, with a known failures file only (a fresh directory in the place its "
    "baseline was measured in, or on disk for the tests rerun there, U273)",
    "the installation state sandbox: "
    + ", ".join(sorted(SANDBOXED_ENV))
    + " (all pointed inside the run's workspace, R-343)",
)

#: The in-subprocess plugin, so death counts come off report OBJECTS. It rewrites
#: its file on every event, so a run that dies partway leaves evidence. Under
#: pytest-xdist only the controller writes: it sees every worker's reports, and
#: its count comes off the hook xdist fires when a worker finishes collecting.
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


def load_spec(spec_path: Path) -> tuple[str, str, list[Row], list[Dropped]]:
    """Read a row file and return ``(name, pass_kind, rows, dropped)``."""
    data = read_spec(spec_path)
    name = str(data.get("name") or spec_path.stem)
    pass_kind = str(data.get("pass_kind", "full"))
    if pass_kind not in PASS_KINDS:
        raise DriverRefusal(f"pass_kind must be one of {sorted(PASS_KINDS)}, got {pass_kind!r}")
    rows: list[Row] = []
    seen: set[str] = set()
    sources: set[tuple[str, str]] = set()
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
        source = read_source(entry, f"row {row_id}")
        if pass_kind == REPLAY:
            if source is None:
                raise DriverRefusal(
                    f"row {row_id}: a replay row names where it came from and this one "
                    f"names no source. A replay pass has no row cap because it measures "
                    f"recorded rows again; a new row belongs in a light or a full pass."
                )
            if source in sources:
                raise DriverRefusal(
                    f"row {row_id}: {source[0]} row {source[1]} is already the source of "
                    f"another row in this batch, and one recorded row is replayed once"
                )
            sources.add(source)
        rows.append(Row(
            id=row_id, description=str(entry["description"]), file=str(entry["file"]),
            old=str(entry["old"]), new=str(entry["new"]),
            tests=tuple(str(one) for one in tests) if tests else None, surface=surface,
            pairs_with=str(entry["pairs_with"]) if entry.get("pairs_with") else None,
            source=source, moved=str(entry.get("moved") or ""),
        ))
    if not rows:
        raise DriverRefusal(f"{spec_path.name} declares no rows")
    cap = ROW_CAPS.get(pass_kind, len(rows))
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
        Dropped(str(entry.get("id", f"dropped-{index}")), str(entry.get("description", "")),
                str(entry.get("reason", "")))
        for index, entry in enumerate(data.get("dropped", []))
    ]
    return name, pass_kind, rows, dropped


def load_mapped(spec_path: Path, pass_kind: str, rows: list[Row]) -> list[Mapped]:
    """A replay's ``[[mapped]]`` entries: each a source no row replays, a target that is a
    row here and a reason, or `killset.py check` would read a mapping nothing backs."""
    entries = read_spec(spec_path).get("mapped", [])
    if entries and pass_kind != REPLAY:
        raise DriverRefusal(f"[[mapped]] belongs to a replay pass, and this is a {pass_kind} pass")
    ids = {row.id for row in rows}
    replayed = {row.source for row in rows}
    mapped: list[Mapped] = []
    seen: set[tuple[str, str]] = set()
    for index, entry in enumerate(entries):
        what = f"mapped entry {index}"
        source = read_source(entry, what) if isinstance(entry, dict) else None
        if source is None:
            raise DriverRefusal(f"{what}: it names no source, the recorded row it stands for")
        target = str(entry.get("to") or "")
        reason = str(entry.get("reason") or "").strip()
        if source in replayed:
            raise DriverRefusal(
                f"{what}: {source[0]} row {source[1]} has a row of its own in this batch, "
                f"so it is replayed, not mapped"
            )
        if source in seen:
            raise DriverRefusal(f"{what}: {source[0]} row {source[1]} is mapped twice")
        if target not in ids:
            raise DriverRefusal(f"{what}: it maps to {target!r}, which is no row in this batch")
        if not reason:
            raise DriverRefusal(
                f"{what}: it gives no reason; say what became of the guard, moved or "
                f"merged into the row it names"
            )
        seen.add(source)
        mapped.append(Mapped(source=source, to=target, reason=reason))
    return mapped


def replay_resume_refusal(repo_root: Path, prior: dict | None) -> str:
    """Why a replay reuses nothing of a prior sidecar, or "" when it may: it reads what
    THIS commit's tests kill, so only a sidecar of this commit with no tracked file changed."""
    if prior is None:
        return ""
    here = head_sha(repo_root)
    if prior.get("head") != here:
        return f"it was measured at {prior.get('head')!r} and this is {here!r}"
    status = _git(repo_root, "status", "--porcelain", "--untracked-files=no")
    if status.returncode != 0:
        return "git could not say whether a tracked file changed since this commit"
    if status.stdout.strip():
        return "a tracked file differs from this commit, so what it measured may not hold"
    return ""


def null_control_row(rows: list[Row]) -> Row:
    """The control row: a comment appended to one of the batch's own Python targets."""
    target = next((row.file for row in rows if row.file.endswith(".py")), None)
    if target is None:
        raise DriverRefusal(
            "the null control needs a Python target and no row names one; "
            "the control is what proves the apparatus, so the batch cannot run without it"
        )
    description = (
        "Automatic control: append a comment line to "
        f"{target}. Semantically empty, so it must kill zero. Any death here "
        "means the measuring apparatus is broken, not the code."
    )
    return Row("NULL_CONTROL", description, target, "", NULL_CONTROL_COMMENT, kind="null-control")


def pytest_addopts(repo_root: Path) -> str:
    """``addopts`` from pyproject with every quiet flag removed, and nothing else: a second
    ``-q`` becomes ``-qq`` and suppresses the summary line."""
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        return ""
    with pyproject.open("rb") as handle:
        data = tomllib.load(handle)
    raw = data.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("addopts", "")
    tokens = [str(one) for one in raw] if isinstance(raw, list) else shlex.split(str(raw))
    return " ".join(token for token in tokens if token not in {"-q", "-qq", "--quiet"})


def installation_state_roots() -> tuple[Path, ...]:
    """The REAL installation directories the guard watches, resolved as the product does:
    the overrides first (under pytest, the conftest's temporary roots), deduplicated."""
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


#: Files this small are hashed too, so a same size rewrite in one timestamp tick is seen.
SMALL_FILE_BYTES = 64 * 1024


def state_fingerprint(root: Path) -> tuple[str, int]:
    """(digest, entry count) of every directory and file under ``root``, by ``lstat``, and
    of whether the root exists."""
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


def portable(path: Path) -> str:
    """``path`` with the home directory folded to ``~``, for anything written into the tree."""
    home = Path.home()
    try:
        return "~/" + path.relative_to(home).as_posix()
    except ValueError:
        return str(path)


@dataclass(frozen=True)
class StateGuard:
    """The real installation state as it stood before any child of this batch ran."""
    roots: tuple[Path, ...]
    digests: tuple[str, ...]
    counts: tuple[int, ...]

    def describe(self) -> str:
        """The roots with home folded to ``~``: the scan refuses a home path under docs/."""
        pairs = zip(self.roots, self.counts, strict=True)
        return "; ".join(f"{portable(root)} ({count} entries)" for root, count in pairs)


def take_state_guard(roots: tuple[Path, ...] | None = None) -> StateGuard:
    """Fingerprint the real installation state before the batch touches anything."""
    resolved = installation_state_roots() if roots is None else tuple(roots)
    taken = [state_fingerprint(root) for root in resolved]
    return StateGuard(resolved, tuple(one for one, _ in taken), tuple(one for _, one in taken))


def check_state_guard(guard: StateGuard, *, label: str) -> None:
    """Raise ``StateLeak`` if the real installation state moved under a child, or under a
    concurrent writer, which the driver cannot tell apart."""
    for root, before, counted in zip(guard.roots, guard.digests, guard.counts, strict=True):
        now, count_now = state_fingerprint(root)
        if now == before:
            continue
        raise StateLeak(
            f"the real installation state changed while running {label}. "
            f"{portable(root)} held {counted} entries before this child and holds "
            f"{count_now} now. Either a child of this driver reached the real "
            "machine, which is R-343 and on 2026-09-20 overwrote a real "
            "configuration with a fixture one, or something else wrote there "
            "while the child ran, and the driver cannot tell which. The batch is "
            "stopped and nothing after this point was measured. Read that "
            "directory before rerunning, and rerun with nothing else using it."
        )


def run_pytest(
    repo_root: Path, paths: list[str] | None, *, timeout: int = 3600,
    guard: StateGuard | None = None, label: str = "a child run",
    known: frozenset[str] = frozenset(),
) -> RunResult:
    """Run pytest once, synchronously, and read the result off report objects.

    ``known``, the machine's failures from ``cloud_battery.py baseline``, is
    subtracted. Given a place (U273) the run keeps its ``TMPDIR`` there, and after
    a run in memory the baseline's disk tests it collected run again on disk.
    """
    place = getattr(known, "place", "")
    root = None
    if place:
        root, why = BATTERY.place_root(place)
        if root is None:
            raise DriverRefusal(
                f"{label} cannot keep its temporary files "
                f"{'in memory' if place == BATTERY.MEMORY else 'on disk'} on this machine: {why}"
            )
    with tempfile.TemporaryDirectory(prefix="mutate-run-", dir=root) as tmp:
        workspace = Path(tmp)
        (workspace / f"{PLUGIN_MODULE}.py").write_text(PLUGIN_SOURCE, encoding="utf-8")
        report_path = workspace / "report.json"
        # INHERIT, then add: a hand built environment once dropped ffmpeg off PATH.
        env = os.environ.copy()
        # Identical byte lengths a second apart otherwise serve stale bytecode.
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["MUTATE_REPORT_PATH"] = str(report_path)
        env["PYTHONPATH"] = os.pathsep.join([str(workspace), env.get("PYTHONPATH", "")])
        env["PYTHONPATH"] = env["PYTHONPATH"].rstrip(os.pathsep)
        sandbox = workspace / "installation-state"
        for name, relative in SANDBOXED_ENV.items():
            path = sandbox / relative
            path.mkdir(parents=True, exist_ok=True)
            env[name] = str(path)
        for name in SCRUBBED_ENV:
            env.pop(name, None)
        if place:
            temp = workspace / "tmp"
            temp.mkdir()
            env["TMPDIR"] = str(temp)
        command = [sys.executable, "-m", "pytest", "-p", PLUGIN_MODULE, "-p", "no:cacheprovider"]
        command += ["--tb=no", "-o", f"addopts={pytest_addopts(repo_root)}", *(paths or [])]
        try:
            done = subprocess.run(
                command, cwd=repo_root, env=env, capture_output=True, text=True, check=False,
                timeout=timeout,
            )
        finally:
            # In a finally, so a child that leaks and then hangs past the
            # timeout is still checked, and its leak is not blamed on the next
            # row. A leak outranks the timeout and a missing report alike.
            if guard is not None:
                check_state_guard(guard, label=label)
        if not report_path.is_file():
            raise MeasurementFailure(
                "pytest produced no report file, so nothing was measured. "
                f"exit {done.returncode}\n{done.stdout[-2000:]}\n{done.stderr[-2000:]}"
            )
        state = json.loads(report_path.read_text(encoding="utf-8"))
    # 3 internal, 4 usage, 5 nothing collected: each leaves an EMPTY report that
    # would read as green. Exit 2 is how a collection error arrives, a measurement.
    if done.returncode in {3, 4, 5}:
        raise MeasurementFailure(
            f"pytest exited {done.returncode} and nothing was measured. That is a "
            f"usage, internal or empty-collection failure, not a zero row.\n"
            f"{done.stdout[-1500:]}\n{done.stderr[-1500:]}"
        )
    failed = tuple(i for i in state["failed"] if i not in known)
    errored = tuple(i for i in state["errored"] if i not in known)
    collect_errors = tuple(state["collect_errors"])
    on_disk = getattr(known, "on_disk", ())
    rerun = [one for one in on_disk if runs_node(one, paths)] if place == BATTERY.MEMORY else []
    if rerun:
        again = run_pytest(
            repo_root, rerun, timeout=timeout, guard=guard, label=f"{label}, its tests on disk",
            known=KnownFailures(known, place=BATTERY.DISK),
        )
        if again.collected != len(rerun) and not again.collect_errors:
            raise MeasurementFailure(
                f"the run on disk of {rerun} collected {again.collected}, so it cannot stand "
                f"for them"
            )
        failed = tuple(i for i in failed if i not in rerun) + again.failed
        errored = tuple(i for i in errored if i not in rerun) + again.errored
        collect_errors = collect_errors + again.collect_errors
    return RunResult(int(state["collected"]), failed, errored, collect_errors, done.returncode)


def runs_node(nodeid: str, paths: list[str] | None) -> bool:
    """Whether a run over ``paths`` collects ``nodeid``; every run over no paths does."""
    if not paths:
        return True
    for path in paths:
        path = path.rstrip("/")
        if nodeid == path or nodeid.startswith((f"{path}::", f"{path}[", f"{path}/")):
            return True
    return False


#: The battery's run record and format, held equal to ``cloud_battery.py``'s by a test.
BATTERY_VERDICT = Path(".cloud-battery") / "verdict.json"
BATTERY_VERDICT_FORMAT = 1
#: The boot id the battery records: every cloud container's host name is `vm`.
BOOT_ID = Path("/proc/sys/kernel/random/boot_id")


def file_digest(path: Path) -> str:
    """The sha256 of a file's bytes, the key a battery verdict names its known failures by."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def boot_id() -> str:
    """This boot's id, or empty where the kernel keeps none (macOS)."""
    try:
        return BOOT_ID.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def tree_state(repo_root: Path) -> tuple[str, bool | None]:
    """HEAD's full sha and whether the checkout is clean, untracked files included, None
    when git could not read the status: no answer is not an empty status."""
    sha = _git(repo_root, "rev-parse", "HEAD")
    commit = sha.stdout.decode("utf-8", "replace").strip() if sha.returncode == 0 else ""
    status = _git(repo_root, "status", "--porcelain", "--untracked-files=all")
    if not commit or status.returncode != 0:
        return commit, None
    return commit, not status.stdout.strip()


def _strings(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(one, str) for one in value)


def _whole_number(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def read_battery_verdict(
    repo_root: Path, path: Path, *, known: frozenset[str], known_digest: str
) -> tuple[RunResult | None, str]:
    """The battery's last run as this batch's full baseline, or None and the reason it is not.

    Phillip's answer of 2026-11-13: only for this commit on a clean tree, this
    machine, checkout and interpreter, the same known failures file, and a whole
    run. The note names no host or path, since the table is published.
    """
    prefix = "the battery's verdict was not read: "
    if not known_digest:
        return None, (
            prefix + "no known failures file was passed, and the battery's verdict is read "
            "net of one"
        )
    shown = BATTERY_VERDICT.as_posix()
    if not path.is_file():
        return None, prefix + f"no battery verdict at `{shown}`"
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        record = None
    unreadable = prefix + f"`{shown}` is a record this driver cannot read"
    if not isinstance(record, dict) or record.get("format") != BATTERY_VERDICT_FORMAT:
        return None, unreadable
    failing = record.get("failing")
    collect_errors = record.get("collect_errors")
    if not (
        _strings(failing)
        and _strings(collect_errors)
        and isinstance(record.get("commit"), str)
        and record.get("verdict") in {"clean", "red"}
    ):
        return None, unreadable
    commit, clean_now = tree_state(repo_root)
    recorded = record["commit"]
    checks = (
        (
            bool(commit) and recorded == commit,
            f"it is for commit `{recorded[:12] or 'none'}`, and this tree is at "
            f"`{commit[:12] or 'a commit git could not name'}`",
        ),
        (record.get("clean_tree") is True, "the tree was not clean throughout the battery's run"),
        (clean_now is not None, "git could not read this tree's status"),
        (clean_now is True, "this tree has uncommitted or untracked changes"),
        (
            record.get("host") == socket.gethostname() and record.get("boot_id") == boot_id(),
            "it was measured on another machine, or before this one last started",
        ),
        (record.get("root") == str(repo_root.resolve()), "it was measured in another checkout"),
        (record.get("python") == sys.executable, "it was measured with another interpreter"),
        (
            record.get("known_failures_sha256") == known_digest,
            "it was read against another known failures file",
        ),
        (
            _whole_number(record.get("exit_code")) and record["exit_code"] in {0, 1},
            f"pytest exited {record.get('exit_code')!r} in that run, so it did not complete",
        ),
        (
            _whole_number(record.get("collected")) and record["collected"] > 0,
            "it records no collected count",
        ),
        (
            _whole_number(record.get("ran")) and record["ran"] == record["collected"],
            f"{record.get('ran')!r} of its {record.get('collected')!r} collected tests "
            "reported, so the run stopped early",
        ),
        (
            record.get("pytest_addopts") == "",
            "that run inherited PYTEST_ADDOPTS, which edits what the suite runs",
        ),
    )
    for ok, why in checks:
        if not ok:
            return None, prefix + why
    beyond = sorted(set(failing) - known)
    green = not beyond and not collect_errors
    if green != (record["verdict"] == "clean"):
        return None, prefix + (
            f"it says {record['verdict']}, which disagrees with the ids it lists"
        )
    when = record.get("when") if isinstance(record.get("when"), str) else "an unrecorded time"
    source = record.get("source") if record.get("source") in {"compare", "baseline"} else "a run"
    note = (
        f"read from the battery's verdict, `{shown}`, written by `cloud_battery.py {source}` "
        f"at {when} for commit `{commit[:12]}`: the same commit on a clean tree, the same "
        "machine, checkout and interpreter, and the same known failures file"
    )
    result = RunResult(
        record["collected"],
        failed=tuple(beyond),
        errored=(), collect_errors=tuple(sorted(collect_errors)), exit_code=record["exit_code"],
    )
    return result, note


def replay_fields(row: Row) -> dict:
    """What a replay row carries into its result: where it came from, and why it moved."""
    source = {"table": row.source[0], "id": row.source[1]} if row.source else None
    return {"source": source, "moved": row.moved}


def _described(row: Row, subset: list[str] | None, why: str) -> dict:
    return dict(
        id=row.id, description=row.description, file=row.file, kind=row.kind,
        surface=row.surface, pairs_with=row.pairs_with, fingerprint=row.fingerprint(),
        subset=list(subset) if subset else None, subset_reason=why, old=row.old, new=row.new,
    )


def measure_row(
    repo_root: Path, row: Row, subset: list[str] | None, subset_reason: str,
    subset_baseline: RunResult, full_baseline: RunResult, *, timeout: int = 3600,
    head_verify: bool = True, guard: StateGuard | None = None,
    known: frozenset[str] = frozenset(),
) -> RowResult:
    """Apply one row, measure it, restore it, and describe what happened."""
    common = dict(
        _described(row, subset, subset_reason),
        head_verified=head_verify,
        **replay_fields(row),
    )
    try:
        appended = row.kind == "null-control"
        with mutated(repo_root, row.file, row.old, row.new, allow_append=appended,
                     head_verify=head_verify):
            result = run_pytest(
                repo_root, subset, timeout=timeout, guard=guard, label=f"row {row.id}",
                known=known,
            )
            promoted = False
            final = result
            unbroken = result.collected == subset_baseline.collected
            if subset is not None and result.deaths == 0 and not result.collect_errors and unbroken:
                # A zero on a subset is not yet a zero.
                final = run_pytest(
                    repo_root, None, timeout=timeout, guard=guard,
                    label=f"row {row.id}, promoted to the full suite", known=known,
                )
                promoted = True
    except DriverRefusal as refusal:
        return RowResult(
            status="refused", deaths=0, collected=0, baseline_collected=subset_baseline.collected,
            collect_drift=False, note=str(refusal), runs=0, **common,
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
        status=status, deaths=final.deaths, collected=final.collected,
        baseline_collected=reference.collected, collect_drift=drift,
        collect_errors=list(final.collect_errors), killed=final.failure_ids(), promoted=promoted,
        subset_deaths=result.deaths if promoted else None, note=note, runs=2 if promoted else 1,
        **common,
    )


def measure_batch(
    repo_root: Path, name: str, rows: list[Row], dropped: list[Dropped] | None = None, *,
    pass_kind: str = "full", allow_dirty: bool = False, timeout: int = 3600,
    prior: dict | None = None, progress_path: Path | None = None, guard: StateGuard | None = None,
    known: frozenset[str] = frozenset(), known_source: str = "", known_digest: str = "",
    battery_verdict: Path | None = None, baseline_note: str = "",
    mapped: list[Mapped] | None = None,
) -> Batch:
    """Run a whole batch: preflight, baselines, the control, then the rows.

    ``battery_verdict``, when ``read_battery_verdict`` accepts it, stands for the
    full baseline. ``progress_path`` is rewritten after EVERY row, so it resumes.
    """
    dropped = list(dropped or [])
    runs = 0
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = dict(
        name=name, pass_kind=pass_kind, branch=branch_name(repo_root), head=head_sha(repo_root),
        when=when, dropped=dropped, known_failures=len(known), known_source=known_source,
        temp_place=getattr(known, "place", ""), temp_on_disk=len(getattr(known, "on_disk", ())),
        mapped=list(mapped or []),
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
    # After preflight and before the first child, so it describes the machine
    # as the batch found it. R-343.
    if guard is None:
        guard = take_state_guard()
    header["state_guarded"] = guard.describe()
    read: RunResult | None = None
    if battery_verdict is not None:
        read, baseline_note = read_battery_verdict(
            repo_root, battery_verdict, known=known, known_digest=known_digest
        )
    if read is not None:
        full_baseline = read
        header["baseline_source"] = "read"
        source = f"{baseline_note}. "
        hint = (
            "That run is the battery's own reading of this commit on this machine, so "
            "the branch is red: fix it, or measure the baseline here with "
            "--measure-baseline if the reading is in doubt."
        )
    else:
        full_baseline = run_pytest(
            repo_root, None, timeout=timeout, guard=guard, label="the full baseline", known=known
        )
        runs += 1
        source = ""
        hint = (
            "Before suspecting the code, suspect the ENVIRONMENT. A red baseline "
            "here has twice been a missing binary rather than a broken tree: a "
            "trimmed PATH dropped ffmpeg and reddened 28 audio tests on the full "
            "run while every subset row stayed green, which reads as selective "
            "damage and is not. Run the suite by hand in this shell first."
        )
    header["baseline_note"] = baseline_note
    if not full_baseline.is_green:
        detail = ", ".join(full_baseline.failure_ids()[:10]) or ", ".join(
            full_baseline.collect_errors[:10]
        )
        raise DriverRefusal(
            f"BASELINE IS NOT GREEN: {full_baseline.deaths} failing, "
            f"{len(full_baseline.collect_errors)} collection errors, "
            f"{full_baseline.collected} collected. {source}THE BATCH IS INVALID and no "
            f"row ran. Every row measured against this would read as a death, "
            f"including rows that cannot kill anything.\n"
            f"Failing: {detail}\n"
            f"{hint}"
        )

    def batch(**fields) -> Batch:
        return Batch(
            baseline_collected=full_baseline.collected, baseline_exit=full_baseline.exit_code,
            pytest_runs=runs, **header, **fields,
        )
    plans = [
        (row, list(row.tests), "explicit subset from the row")
        if row.tests
        else (row, *derive_subset(repo_root, row.file))
        for row in rows
    ]
    subset_baselines: dict[tuple[str, ...], RunResult] = {}
    for _, subset, _ in plans:
        if subset is None or tuple(subset) in subset_baselines:
            continue
        measured = run_pytest(
            repo_root, list(subset), timeout=timeout, guard=guard,
            label=f"the subset baseline for {', '.join(subset)}", known=known,
        )
        runs += 1
        if not measured.is_green:
            raise DriverRefusal(
                f"the subset baseline for {', '.join(subset)} is not green: "
                f"{', '.join(measured.failure_ids()[:10]) or 'collection error'}. "
                f"Every row measured against it would read as a death."
            )
        subset_baselines[tuple(subset)] = measured
    header["subset_baselines"] = len(subset_baselines)
    control_result = measure_row(
        repo_root, control, None, "full suite", full_baseline, full_baseline, timeout=timeout,
        head_verify=control.file not in set(dirty), guard=guard, known=known,
    )
    runs += control_result.runs
    if control_result.deaths or control_result.status != "zero":
        return batch(
            valid=False,
            invalid_reason=(
                f"the null control killed {control_result.deaths} and collected "
                f"{control_result.collected} against a baseline of "
                f"{full_baseline.collected}. A change with no semantic content "
                f"cannot kill a test, so the apparatus is what is broken, not the "
                f"code. Every row in this batch would be wrong in the same "
                f"direction. Stop and find the environmental cause."
            ),
            control=control_result,
            results=[],
        )
    stale = pass_kind == REPLAY and bool(replay_resume_refusal(repo_root, prior))
    reused = {
        entry["fingerprint"]: entry
        for entry in ({} if stale else prior or {}).get("rows", [])
        if entry.get("status") not in {None, "error"}
    }
    results: list[RowResult] = []
    for row, subset, why in plans:
        cached = reused.get(row.fingerprint())
        if cached is not None and cached.get("id") == row.id:
            # Where a row came from and why it moved are the row file's to say now.
            results.append(RowResult(**{**cached, **replay_fields(row)}))
            header["reused_rows"] = header.get("reused_rows", 0) + 1
            continue
        baseline = subset_baselines[tuple(subset)] if subset is not None else full_baseline
        try:
            results.append(measure_row(
                repo_root, row, subset, why, baseline, full_baseline, timeout=timeout,
                head_verify=row.file not in set(dirty), guard=guard, known=known,
            ))
        except (RestoreVerificationError, StateLeak, KeyboardInterrupt):
            # A leak must outrank the blanket handler below, or the loop would keep
            # spending children against a machine it had just damaged.
            raise
        except Exception as failure:  # noqa: BLE001 - recorded, never swallowed silently
            results.append(RowResult(
                status="error", deaths=0, collected=0, baseline_collected=baseline.collected,
                collect_drift=False, note=f"{type(failure).__name__}: {failure}", runs=1,
                **_described(row, subset, why), **replay_fields(row),
            ))
        runs += results[-1].runs
        if progress_path is not None:
            partial = batch(valid=True, invalid_reason="in progress", control=control_result,
                            results=results)
            progress_path.parent.mkdir(parents=True, exist_ok=True)
            progress_path.write_text(json.dumps(partial.to_dict(), indent=2) + "\n", "utf-8")
    return batch(valid=True, invalid_reason="", control=control_result, results=results)


def render_markdown(batch: Batch) -> str:
    return _table.render_markdown(batch, ADDED_ENV, SCRUBBED_ENV)


def write_outputs(batch: Batch, out_dir: Path) -> tuple[Path, Path]:
    return _table.write_outputs(batch, out_dir, render_markdown(batch))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Measure a mutation table from a row file.")
    parser.add_argument("spec", type=Path, help="a .toml or .json row file")
    parser.add_argument("--name", default=None, help="output name; defaults to the spec's")
    parser.add_argument("--out-dir", type=Path, default=REPO_ROOT / "docs" / "mutation")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--allow-dirty", action="store_true", help=(
        "measure with uncommitted changes to a target; the restore check still uses HEAD"
    ))
    parser.add_argument("--resume", action="store_true", help=(
        "reuse rows already in the JSON sidecar whose text has not changed; a replay "
        "reuses them only from a sidecar measured at this commit with no tracked "
        "file changed since"
    ))
    parser.add_argument("--timeout", type=int, default=3600, help="seconds per pytest run")
    parser.add_argument("--known-failures", type=Path, default=None, help=(
        "a file of whole node ids that fail on this machine and not for the tree, one "
        "a line, # comments allowed, as scripts/cloud_battery.py baseline writes "
        "it with full history and whole ids; subtracted from every run, and refused "
        "on a shallow clone. It also names where its temporary files were, memory or "
        "disk: every child keeps its own there, the tests it ran on disk run again on "
        "disk after a run in memory, and a file naming no place is refused"
    ))
    parser.add_argument("--measure-baseline", action="store_true", help=(
        "measure the full baseline here even when the cloud battery's verdict for "
        "this commit could stand for it (U271)"
    ))
    return parser


#: The fields `cloud_battery.py baseline` ends its first line with: the clone's
#: whole history was present (U200), and every id was stored whole (U268).
KNOWN_FAILURES_FULL_HISTORY = "history full"
KNOWN_FAILURES_WHOLE_IDS = "ids whole"


class KnownFailures(frozenset):
    """A baseline's failing ids, the place of its temporary files and its tests on disk."""

    def __new__(cls, ids=(), *, place: str = "", on_disk=()):
        made = super().__new__(cls, ids)
        made.place, made.on_disk = place, tuple(on_disk)
        return made


def read_known_failures(path: Path) -> KnownFailures:
    """A baseline's node ids, refused unless measured with full history (R-1191), with
    whole ids (U268) and naming the place of its temporary files (U273)."""
    text = path.read_text(encoding="utf-8").splitlines()
    first = text[0].strip() if text else ""
    measured = first.startswith("# commit ")
    whole = f" {KNOWN_FAILURES_FULL_HISTORY} {KNOWN_FAILURES_WHOLE_IDS}"
    if not (measured and first.endswith(whole)):
        if measured and first.endswith(f" {KNOWN_FAILURES_FULL_HISTORY}"):
            raise DriverRefusal(
                f"{path} was measured before U268 and holds each id only up to its first "
                f"space; measure it again with `scripts/cloud_battery.py baseline`, never "
                f"write one by hand"
            )
        raise DriverRefusal(
            f"{path} does not say it was measured with full history; measure it with "
            f"`scripts/cloud_battery.py baseline`, never write one by hand"
        )
    fields = first[: -len(whole)].split()
    place = fields[-1] if len(fields) >= 2 and fields[-2] == BATTERY.TEMP_FIELD else ""
    if place not in BATTERY.PLACES:
        raise DriverRefusal(
            f"{path} does not say where its temporary files were: it was measured before "
            f"U273, so whether its failures are the memory filesystem's or the disk's is "
            f"unknown; measure it again with `scripts/cloud_battery.py baseline`, never "
            f"write one by hand"
        )
    prefix = BATTERY.ON_DISK_PREFIX
    on_disk = [line[len(prefix) :] for line in text if line.startswith(prefix)]
    lines = (line.strip() for line in text)
    ids = (line for line in lines if line and not line.startswith("#"))
    return KnownFailures(ids, place=place, on_disk=on_disk)


def refuse_a_shallow_clone(repo_root: Path) -> None:
    """Known failures are subtracted only from a clone with its full history."""
    done = _git(repo_root, "rev-parse", "--is-shallow-repository")
    answer = done.stdout.decode("utf-8", "replace").strip()
    if done.returncode != 0 or answer != "false":
        raise DriverRefusal(
            f"{repo_root} is a shallow clone, or git could not say ({answer or done.returncode}); "
            f"a test the missing history holds red would be subtracted unread, so run "
            f"`git fetch --unshallow origin main` first"
        )


def refuse_a_place_this_machine_cannot_give(known: KnownFailures) -> None:
    """Before anything runs: every place a run in the known failures' place uses
    must be one this machine can give, the disk for the tests rerun there included."""
    needed = [known.place]
    if known.place == BATTERY.MEMORY and known.on_disk:
        needed.append(BATTERY.DISK)
    for place in needed:
        root, why = BATTERY.place_root(place)
        if root is None:
            run = (
                f"temporary files in {place}"
                if place == known.place
                else "the tests the baseline ran on disk run again on disk"
            )
            raise DriverRefusal(
                f"the known failures were measured with their temporary files in "
                f"{known.place}, and this machine cannot now give a run with {run}: {why}"
            )


#: How main reports each way a batch stops, and its exit code.
STOPS = {
    DriverRefusal: ("refused", 2),
    RestoreVerificationError: ("RESTORE FAILED", 3),
    StateLeak: ("STATE LEAK", 6),
    MeasurementFailure: ("NOTHING MEASURED", 5),
}


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])
    try:
        name, pass_kind, rows, dropped = load_spec(args.spec)
        mapped = load_mapped(args.spec, pass_kind, rows)
        if pass_kind == REPLAY:
            refuse_unrecorded_sources(args.repo_root, rows, mapped)
    except DriverRefusal as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 2
    name = args.name or name
    known: frozenset[str] = frozenset()
    known_digest = ""
    if args.known_failures is not None:
        if not args.known_failures.is_file():
            print(f"refused: no known failures file at {args.known_failures}", file=sys.stderr)
            return 2
        try:
            known = read_known_failures(args.known_failures)
            known_digest = file_digest(args.known_failures)
            refuse_a_shallow_clone(args.repo_root)
            refuse_a_place_this_machine_cannot_give(known)
        except DriverRefusal as refusal:
            print(f"refused: {refusal}", file=sys.stderr)
            return 2
    # The battery's verdict is read net of the machine's known failures, so it
    # is offered only to a run that subtracts them (U271).
    battery_verdict = None
    baseline_note = ""
    if args.measure_baseline:
        baseline_note = "--measure-baseline was passed"
    elif args.known_failures is not None:
        battery_verdict = args.repo_root / BATTERY_VERDICT
    prior = None
    sidecar = args.out_dir / f"{name}.json"
    if args.resume and sidecar.is_file():
        prior = json.loads(sidecar.read_text(encoding="utf-8"))
        why = replay_resume_refusal(args.repo_root, prior) if pass_kind == REPLAY else ""
        if why:
            print(
                f"resume: nothing of {sidecar.name} is reused: {why}. A replay reuses "
                f"rows only from this commit as committed, so every row is measured again",
                file=sys.stderr,
            )
    try:
        batch = measure_batch(
            args.repo_root, name, rows, dropped, pass_kind=pass_kind,
            allow_dirty=args.allow_dirty, timeout=args.timeout, prior=prior,
            progress_path=sidecar, known=known,
            known_source=str(args.known_failures) if args.known_failures else "",
            known_digest=known_digest, battery_verdict=battery_verdict,
            baseline_note=baseline_note, mapped=mapped,
        )
    except (DriverRefusal, RestoreVerificationError, StateLeak, MeasurementFailure) as stop:
        heading, code = STOPS[type(stop)]
        print(f"{heading}: {stop}", file=sys.stderr)
        return code
    markdown, written = write_outputs(batch, args.out_dir)
    print(
        f"full baseline: {batch.baseline_source}"
        + (f", {batch.baseline_note}" if batch.baseline_note else "")
    )
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
