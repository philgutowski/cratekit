#!/usr/bin/env python3
"""Capture what `crate` prints and writes on a disposable library, and compare two captures.

A refactor under U290 freezes behaviour: every verb's output, exit code and
written file is unchanged. This is how a branch shows it. `capture` runs the
scenarios under `tests/behaviour/` and records what each did; `compare` reads
two captures and prints every difference (U297).

    .venv/bin/python scripts/behaviour_compare.py capture --out before --rev origin/main
    .venv/bin/python scripts/behaviour_compare.py capture --out after
    .venv/bin/python scripts/behaviour_compare.py compare before after


WHAT A CAPTURE IS
-----------------
A scenario is a test function in a file under `tests/behaviour/`, one file per
package, that drives real `crate` commands through the dispatcher on a library
the suite's own fixtures build. Per command the capture holds the arguments,
standard output, standard error and the exit code. After the scenario it holds
every file under the scenario's temporary directory, by path and bytes, and
every SQLite database there as a sorted dump of every table.

`capture` runs those files as a pytest run of their own, so the isolation is
the suite's and not a second copy of it: `tests/conftest.py` redirects every
installation root, replaces the keychain, refuses every live provider and
reads the host as a machine with no rekordbox, for these scenarios as for any
test. `tests/behaviour/conftest.py` adds what a comparison needs on top: the
roots moved into the scenario's own directory, the clock held at one instant,
generated ids drawn from a counted sequence, and the terminal width and time
zone fixed. It never opens a real library and never launches rekordbox.

Two captures are comparable because nothing in them depends on when or where
they ran. The run's base temporary directory is `--root`, one fixed directory
inside the system's temporary directory, and the product source it imports is
a copy at a fixed directory beside it, so every path a scenario prints or
writes is the same text in both. `--rev` copies that revision's `src/` out of
git instead of the working tree's, and the same scenarios, fixtures and
harness then run against it: that is how a branch is compared with its base
even when the branch changed a test helper a scenario uses.


WHAT IT REFUSES
---------------
`capture` refuses a `--root` that is not inside the system's temporary
directory, before anything runs, and a root another capture holds. Inside the
run, before every command, the scenario refuses unless the configuration and
state directories the product itself resolves are inside the scenario's own
temporary directory. A scenario that fails fails the capture, which then
writes no manifest, and `compare` refuses a directory with none.


WHAT COMPARE READS AS A DIFFERENCE
----------------------------------
A scenario or a command in one capture only; an exit code, standard output or
standard error that differs by one character; a file in one capture only; a
file whose bytes differ; a table or a row in one capture's dump only.

A SQLite database is compared by its dump, every table, every row and every
column, and not by its bytes: the file also holds its free pages, a change
counter and whichever layout the page allocator chose, and the WAL beside it
is salted at random, so two runs that wrote the same rows do not write the
same bytes. Every other file is compared byte for byte.

ONE EQUIVALENCE IS DECLARED, and it is the only one: a capture's own words
for what the operating system gave it. The scenario run is one process, and
the product writes that process's id and start time into a session's holder,
a lock file and the job queue; and it writes a landed file's inode into the
row rekordbox loads it by. Each capture records its process's two words and
every file's inode by path, and `compare` reads a text or a row as the same
when the two differ only where the first holds one of its own words and the
second holds its own word for the same thing, at the same place. Nothing is
scrubbed out of a capture to arrange this: what a capture holds is what the
commands printed and wrote. What is not covered is a file's own times read
back within the command that wrote it, which no scenario here records.

Exit codes
----------
    0  capture: every scenario ran and was recorded; compare: no difference
    1  capture: a scenario failed; compare: at least one difference
    2  a refusal, decided before anything was compared or run
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCENARIOS = Path("tests") / "behaviour"

FORMAT = 1
MANIFEST = "capture.json"
COMMANDS = "commands.json"
PROCESS = "process.json"
LISTING = "files.json"
DATABASES = "databases.json"
TREE = "tree"

#: The name of the default root, inside the system's temporary directory.
ROOT_NAME = "cratekit-behaviour"
#: The directory beside the root that holds the product source a capture imports.
SOURCE_SUFFIX = "-source"
#: The file beside the root that names the process holding it.
HOLDER_SUFFIX = "-holder"

#: Handed to the scenario run: where to write the record, and the source
#: directory the product must have been imported from.
ENV_OUT = "CRATEKIT_BEHAVIOUR_OUT"
ENV_SOURCE = "CRATEKIT_BEHAVIOUR_SOURCE"

#: Removed from the scenario run's environment. Each would edit the run after
#: this script built it, and a capture started from inside a parallel worker
#: would otherwise hand its child that worker's identity.
SCRUBBED_ENV = (
    "PYTEST_ADDOPTS",
    "PYTEST_CURRENT_TEST",
    "PYTEST_XDIST_WORKER",
    "PYTEST_XDIST_WORKER_COUNT",
    "PYTEST_XDIST_TESTRUNUID",
)

SQLITE_HEADER = b"SQLite format 3\x00"
#: The files SQLite keeps beside a database in WAL mode. A WAL's header holds
#: a random salt, so their bytes differ between two runs that did the same.
SIDECARS = ("-wal", "-shm")

FILE = "file"
DIRECTORY = "directory"
LINK = "link"
DATABASE = "database"
SIDECAR = "database sidecar"

#: How many lines of one text difference are printed before it is cut.
SHOWN_LINES = 40


class Refusal(RuntimeError):
    """The script will not proceed, and says why. Exit 2."""


# ---------------------------------------------------------------------------
# Temporary directories
# ---------------------------------------------------------------------------


def temporary_directory() -> Path:
    """The system's temporary directory, resolved, since macOS reaches it by a link."""
    return Path(tempfile.gettempdir()).resolve()


def is_inside(path: Path, parent: Path) -> bool:
    """Whether ``path`` is strictly below ``parent``, both resolved."""
    try:
        relative = path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return relative != Path(".")


def refuse_outside_temporary(path: Path, what: str) -> None:
    """Raise unless ``path`` is below the system's temporary directory.

    A capture drives verbs that write. The one thing that keeps that from ever
    being somebody's library is that every root it uses is a directory under
    the system's temporary directory, so a root anywhere else is refused
    whatever it holds, the temporary directory itself included.
    """
    if not is_inside(path, temporary_directory()):
        raise Refusal(
            f"{what} is {path}, which is not inside the temporary directory "
            f"{temporary_directory()}; a capture runs only where nothing is kept"
        )


def default_root() -> Path:
    return temporary_directory() / ROOT_NAME


def source_directory(root: Path) -> Path:
    """Where the product source a capture imports is copied to: beside the root."""
    return root.with_name(root.name + SOURCE_SUFFIX)


# ---------------------------------------------------------------------------
# Recording, called by the scenario run
# ---------------------------------------------------------------------------


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def is_database(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(len(SQLITE_HEADER)) == SQLITE_HEADER
    except OSError:
        return False


def list_tree(root: Path) -> dict[str, dict]:
    """Every entry under ``root`` by its path from it: kind, and size and digest for a file.

    A directory is an entry of its own, so an empty one a verb created is
    seen. A link is recorded as a link with its target and never followed. A
    file's inode is kept beside its digest: it is this capture's word for the
    file, never compared, and read past where the product wrote it down.
    """
    entries: dict[str, dict] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        directories.sort()
        here = Path(current)
        for name in sorted([*directories, *files]):
            path = here / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                entries[relative] = {"kind": LINK, "target": os.readlink(path)}
            elif path.is_dir():
                entries[relative] = {"kind": DIRECTORY}
            else:
                status = path.stat()
                entries[relative] = {
                    "kind": DATABASE if is_database(path) else FILE,
                    "size": status.st_size,
                    "sha256": sha256(path),
                    "inode": status.st_ino,
                }
    for relative, entry in entries.items():
        for suffix in SIDECARS:
            if relative.endswith(suffix):
                main = entries.get(relative[: -len(suffix)])
                if main is not None and main["kind"] == DATABASE:
                    entry["kind"] = SIDECAR
    return entries


def _cell(value: object) -> object:
    if isinstance(value, bytes):
        return {"bytes": value.hex()}
    return value


def dump_database(path: Path) -> dict[str, list[str]]:
    """Every table of one SQLite database, each row as JSON text by column, the rows sorted.

    Read from a copy, so the capture never opens a scenario's own file, and
    the copy takes the WAL with it, so rows not yet checkpointed are read. The
    shared memory file is left behind: SQLite rebuilds it from the WAL.
    """
    with tempfile.TemporaryDirectory(prefix="cratekit-behaviour-dump-") as folder:
        copy = Path(folder) / path.name
        shutil.copyfile(path, copy)
        wal = path.with_name(path.name + "-wal")
        if wal.is_file():
            shutil.copyfile(wal, copy.with_name(copy.name + "-wal"))
        connection = sqlite3.connect(copy)
        try:
            names = [
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
                )
            ]
            tables: dict[str, list[str]] = {}
            for name in names:
                quoted = '"' + name.replace('"', '""') + '"'
                cursor = connection.execute(f"SELECT * FROM {quoted}")
                columns = [column[0] for column in cursor.description]
                tables[name] = sorted(
                    json.dumps(
                        {column: _cell(value) for column, value in zip(columns, row)},
                        ensure_ascii=False,
                    )
                    for row in cursor.fetchall()
                )
            return tables
        finally:
            connection.close()


def dump_databases(root: Path, listing: dict[str, dict]) -> dict[str, dict]:
    """The dump of every database in a listing, or the reason one could not be read."""
    dumps: dict[str, dict] = {}
    for relative, entry in listing.items():
        if entry["kind"] != DATABASE:
            continue
        try:
            dumps[relative] = {"tables": dump_database(root / relative)}
        except sqlite3.Error as unread:
            dumps[relative] = {"unreadable": f"{type(unread).__name__}: {unread}"}
    return dumps


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )


def record_scenario(
    out: Path, name: str, commands: list[dict], root: Path, process: list[str]
) -> Path:
    """Write one scenario's record under ``out``: its commands, its files and its dumps.

    ``process`` is the words the scenario's process is known by in what it
    wrote, its id and its start time, kept so two captures can be read past
    them and never to change what either holds.
    """
    target = out / name
    if target.exists():
        raise Refusal(f"{name} was already recorded in {out}; two scenarios share a name")
    listing = list_tree(root)
    write_json(target / COMMANDS, commands)
    write_json(target / PROCESS, [str(word) for word in process])
    write_json(target / LISTING, listing)
    write_json(target / DATABASES, dump_databases(root, listing))
    shutil.copytree(root, target / TREE, symlinks=True)
    return target


# ---------------------------------------------------------------------------
# capture
# ---------------------------------------------------------------------------


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=repo_root, capture_output=True, check=False)


def head_commit(repo_root: Path) -> str:
    done = _git(repo_root, "rev-parse", "HEAD")
    return done.stdout.decode("utf-8", "replace").strip() if done.returncode == 0 else ""


def place_source(repo_root: Path, rev: str | None, target: Path) -> str:
    """Put the product source a capture runs against at ``target``; say which it is.

    The working tree's `src/` as it stands, or a revision's as git holds it.
    Git is only read: `git archive` writes a tar to this process and nothing
    in the repository. Either way the scenarios import the product from the
    same directory, so no path it prints differs between two captures.
    """
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    if rev is None:
        shutil.copytree(
            repo_root / "src",
            target / "src",
            ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"),
        )
        return "the working tree"
    resolved = _git(repo_root, "rev-parse", "--verify", f"{rev}^{{commit}}")
    if resolved.returncode != 0:
        raise Refusal(f"git knows no commit {rev!r}")
    commit = resolved.stdout.decode("utf-8", "replace").strip()
    archived = _git(repo_root, "archive", "--format=tar", commit, "src")
    if archived.returncode != 0:
        raise Refusal(
            f"git could not archive src at {rev}: "
            f"{archived.stderr.decode('utf-8', 'replace').strip()}"
        )
    tar_path = target / "src.tar"
    tar_path.write_bytes(archived.stdout)
    with tarfile.open(tar_path) as archive:
        archive.extractall(target, filter="data")
    tar_path.unlink()
    return f"commit {commit}"


def scenario_files(repo_root: Path) -> list[str]:
    """The scenario files, one per package: every module there but the harness's own two."""
    folder = repo_root / SCENARIOS
    return sorted(
        (SCENARIOS / path.name).as_posix()
        for path in folder.glob("*.py")
        if path.name not in {"__init__.py", "conftest.py"}
    )


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def take_root(root: Path) -> Path:
    """Hold ``root`` for this process, or refuse one a running capture holds.

    The holder is a file beside the root, since the run empties the root
    itself, and it is created exclusively, so of two captures started together
    one is refused. A holder whose process is gone is a capture that died, and
    its root is taken over.
    """
    holder = root.with_name(root.name + HOLDER_SUFFIX)
    holder.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(2):
        try:
            descriptor = os.open(holder, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            try:
                pid = int(holder.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                pid = 0
            if pid and _alive(pid):
                raise Refusal(
                    f"{root} is held by a capture that is still running, process {pid}; "
                    f"two captures in one root would write over each other, so wait or "
                    f"pass --root"
                ) from None
            holder.unlink(missing_ok=True)
            continue
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(f"{os.getpid()}\n")
        return holder
    raise Refusal(f"{holder} could not be taken; another capture keeps writing it")


def capture_command(files: list[str], root: Path, source: Path, only: str | None) -> list[str]:
    """The scenario run: pytest over the scenario files alone, in this process's interpreter.

    ``addopts`` is emptied, so the run is serial and in one process, where the
    clock and the ids are pinned. The base temporary directory is the root,
    which pytest empties as it starts, and the product is imported from the
    placed source and from nowhere else.
    """
    command = [
        sys.executable,
        "-m",
        "pytest",
        *files,
        "--basetemp",
        str(root),
        "-p",
        "no:cacheprovider",
        "--tb=short",
        "-o",
        "addopts=",
        "-o",
        f"pythonpath={source / 'src'}",
    ]
    if only:
        command += ["-k", only]
    return command


def recorded_scenarios(out: Path) -> list[str]:
    """The scenarios a run wrote a record for, by name."""
    return sorted(path.parent.relative_to(out).as_posix() for path in out.glob(f"*/*/{COMMANDS}"))


def write_manifest(out: Path, *, root: Path, source: str, checkout: str, only: str) -> None:
    """Close a capture: the file whose presence says every scenario ran and was recorded."""
    write_json(
        out / MANIFEST,
        {
            "format": FORMAT,
            "root": str(root),
            "source": source,
            "checkout": checkout,
            "python": sys.version.split()[0],
            "only": only,
            "scenarios": recorded_scenarios(out),
        },
    )


def cmd_capture(args) -> int:
    repo_root = args.repo_root.resolve()
    root = (args.root or default_root()).resolve()
    out = args.out.resolve()
    refuse_outside_temporary(root, "the capture root")
    source = source_directory(root)
    if is_inside(out, root) or is_inside(out, source) or out in (root, source):
        raise Refusal(f"--out {out} is inside the capture's own root, which every run empties")
    if out.exists() and any(out.iterdir()):
        raise Refusal(f"--out {out} is not empty; a capture is written into a new directory")
    files = scenario_files(repo_root)
    if not files:
        raise Refusal(f"no scenario files under {repo_root / SCENARIOS}")
    holder = take_root(root)
    try:
        return run_capture(args, repo_root, root, source, out, files)
    finally:
        holder.unlink(missing_ok=True)


def run_capture(args, repo_root: Path, root: Path, source: Path, out: Path, files: list[str]) -> int:
    described = place_source(repo_root, args.rev, source)
    out.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    for name in SCRUBBED_ENV:
        env.pop(name, None)
    env[ENV_OUT] = str(out)
    env[ENV_SOURCE] = str(source / "src")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Set iteration order follows the hash seed, and a seed drawn per process
    # would make two captures of one commit differ wherever a set is printed.
    env["PYTHONHASHSEED"] = "0"
    command = capture_command(files, root, source, args.only)
    try:
        done = subprocess.run(
            command, cwd=repo_root, env=env, capture_output=True, text=True, check=False,
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"capture: the scenario run passed {args.timeout} seconds and was stopped")
        return 1
    finally:
        if not args.keep:
            shutil.rmtree(source, ignore_errors=True)
    recorded = recorded_scenarios(out)
    if done.returncode != 0 or not recorded:
        print(done.stdout[-6000:])
        print(done.stderr[-2000:], file=sys.stderr)
        print(
            f"capture: the scenario run exited {done.returncode} with {len(recorded)} "
            f"scenarios recorded, so {out} is not a capture and holds no manifest; what "
            f"the scenarios wrote is left under {root} for reading"
        )
        return 1
    if not args.keep:
        shutil.rmtree(root, ignore_errors=True)
    write_manifest(
        out, root=root, source=described, checkout=head_commit(repo_root), only=args.only or ""
    )
    commands = sum(len(json.loads((out / name / COMMANDS).read_text())) for name in recorded)
    print(
        f"captured {len(recorded)} scenarios and {commands} commands from {described} "
        f"into {out}"
    )
    return 0


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------


def load_capture(folder: Path) -> dict:
    """A capture's manifest, or a refusal when the directory is not a finished capture."""
    path = folder / MANIFEST
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as unread:
        raise Refusal(
            f"{folder} holds no manifest, so it is not a finished capture; a capture whose "
            f"scenarios failed writes none"
        ) from unread
    if not isinstance(manifest, dict) or manifest.get("format") != FORMAT:
        raise Refusal(f"{path} is not a capture this script reads (format {FORMAT})")
    if not isinstance(manifest.get("scenarios"), list) or not isinstance(
        manifest.get("root"), str
    ):
        raise Refusal(f"{path} names no scenarios or no root")
    return manifest


def _read(folder: Path, name: str, part: str):
    return json.loads((folder / name / part).read_text(encoding="utf-8"))


def text_difference(before: str, after: str, limit: int) -> list[str]:
    """A unified diff of two texts, indented, cut at ``limit`` lines when it is positive."""
    lines = list(
        difflib.unified_diff(
            before.splitlines(), after.splitlines(), "first", "second", lineterm="", n=1
        )
    )
    if not lines:
        # The same lines, so the difference is in how they end.
        lines = [f"first ends {before[-20:]!r}", f"second ends {after[-20:]!r}"]
    shown = lines if limit <= 0 else lines[:limit]
    cut = len(lines) - len(shown)
    return [f"    {line}" for line in shown] + ([f"    ... {cut} more lines"] if cut else [])


def same_but_for(first: str, second: str, words: list[tuple[str, str]]) -> bool:
    """Whether two texts are equal, or differ only in each capture's own words.

    ``words`` pairs a word the first capture's process is known by with the
    second's. The texts are the same when, at every place the first holds one
    of its words, the second holds that word or its own, and they agree
    everywhere else. So a number that merely happens to equal a process id
    still has to be the same number in both, and a real change can hide only
    if it turned exactly one capture's word into the other's.
    """
    if first == second:
        return True
    # One word can stand for two things, a process id that is also some
    # file's inode, so a word keeps every counterpart it was paired with.
    others: dict[str, set[str]] = {}
    for one, two in words:
        if one and two and one != two:
            others.setdefault(one, set()).add(two)
    if not others:
        return False
    splitter = re.compile("|".join(re.escape(one) for one in sorted(others, key=len, reverse=True)))
    pattern: list[str] = []
    position = 0
    for match in splitter.finditer(first):
        word = match.group(0)
        either = "|".join(re.escape(one) for one in (word, *sorted(others[word])))
        pattern.append(re.escape(first[position : match.start()]))
        pattern.append(f"(?:{either})")
        position = match.end()
    pattern.append(re.escape(first[position:]))
    return re.fullmatch("".join(pattern), second, flags=re.DOTALL) is not None


def own_words(
    process: list[str], other_process: list[str], listing: dict, other_listing: dict
) -> list[tuple[str, str]]:
    """Each capture's word for the same thing, paired: the process's, then each file's inode."""
    words = list(zip(process, other_process))
    for relative, entry in listing.items():
        other = other_listing.get(relative, {})
        if "inode" in entry and "inode" in other:
            words.append((str(entry["inode"]), str(other["inode"])))
    return words


def first_difference(before: bytes, after: bytes) -> int:
    for offset, (one, other) in enumerate(zip(before, after)):
        if one != other:
            return offset
    return min(len(before), len(after))


def shown_command(argv: list[str]) -> str:
    return "crate " + " ".join(argv)


def compare_commands(
    name: str, before: list[dict], after: list[dict], words: list, limit: int
) -> list[str]:
    """The two runs of one scenario, command by command.

    The commands are lined up by what was run before any is compared, so one
    command a capture has and the other lacks is reported once, as that, and
    every command after it is still read against its own counterpart.
    """
    found: list[str] = []
    ran = [shown_command(one["argv"]) for one in before]
    then = [shown_command(one["argv"]) for one in after]
    matcher = difflib.SequenceMatcher(None, ran, then, autojunk=False)
    for tag, start, end, other_start, other_end in matcher.get_opcodes():
        if tag != "equal":
            found += [
                f"{name}: command {index + 1}, `{ran[index]}`: only in the first capture"
                for index in range(start, end)
            ]
            found += [
                f"{name}: command {index + 1}, `{then[index]}`: only in the second capture"
                for index in range(other_start, other_end)
            ]
            continue
        for index, other_index in zip(range(start, end), range(other_start, other_end)):
            one, other = before[index], after[other_index]
            where = f"{name}: command {index + 1}, `{ran[index]}`"
            if one["exit"] != other["exit"]:
                found.append(f"{where}: exit code {one['exit']} became {other['exit']}")
            for stream in ("stdout", "stderr"):
                if not same_but_for(one[stream], other[stream], words):
                    found.append(f"{where}: {stream} differs")
                    found += text_difference(one[stream], other[stream], limit)
    return found


def compare_files(
    name: str, first: Path, second: Path, before: dict, after: dict, words: list, limit: int
) -> list[str]:
    """Paths, kinds and links for every entry; bytes for a file that is not a database."""
    found: list[str] = []
    for relative in sorted(set(before) | set(after)):
        where = f"{name}: file {relative}"
        one, other = before.get(relative), after.get(relative)
        if one is None or other is None:
            found.append(f"{where}: only in the {'second' if one is None else 'first'} capture")
            continue
        if one["kind"] != other["kind"]:
            found.append(f"{where}: a {one['kind']} became a {other['kind']}")
            continue
        if one["kind"] == LINK and one["target"] != other["target"]:
            found.append(f"{where}: the link to {one['target']} now points to {other['target']}")
        if one["kind"] != FILE or one["sha256"] == other["sha256"]:
            continue
        old = (first / name / TREE / relative).read_bytes()
        new = (second / name / TREE / relative).read_bytes()
        try:
            texts = old.decode("utf-8"), new.decode("utf-8")
        except UnicodeDecodeError:
            texts = None
        if texts is not None and same_but_for(*texts, words):
            continue
        found.append(
            f"{where}: bytes differ, first at offset {first_difference(old, new)} "
            f"({one['size']} bytes and {other['size']})"
        )
        if texts is not None:
            found += text_difference(*texts, limit)
    return found


def unmatched_rows(old: list[str], new: list[str], words: list) -> tuple[list[str], list[str]]:
    """The rows of each dump the other does not hold, read past each capture's own words."""
    gone = sorted((Counter(old) - Counter(new)).elements())
    come = sorted((Counter(new) - Counter(old)).elements())
    left: list[str] = []
    for row in gone:
        match = next((other for other in come if same_but_for(row, other, words)), None)
        if match is None:
            left.append(row)
        else:
            come.remove(match)
    return left, come


def compare_databases(name: str, before: dict, after: dict, words: list, limit: int) -> list[str]:
    found: list[str] = []
    for relative in sorted(set(before) & set(after)):
        where = f"{name}: database {relative}"
        one, other = before[relative], after[relative]
        if "tables" not in one or "tables" not in other:
            if one != other:
                found.append(
                    f"{where}: could not be dumped alike: {one.get('unreadable', 'read')} "
                    f"and {other.get('unreadable', 'read')}"
                )
            continue
        for table in sorted(set(one["tables"]) | set(other["tables"])):
            old, new = one["tables"].get(table), other["tables"].get(table)
            if old is None or new is None:
                found.append(
                    f"{where}: table {table} is only in the "
                    f"{'second' if old is None else 'first'} capture"
                )
                continue
            gone, come = unmatched_rows(old, new, words)
            for rows, which in ((gone, "first"), (come, "second")):
                if not rows:
                    continue
                found.append(
                    f"{where}: table {table}: {len(rows)} row(s) only in the {which} capture"
                )
                kept = rows if limit <= 0 else rows[:limit]
                found += [f"    {row}" for row in kept]
                if len(rows) > len(kept):
                    found.append(f"    ... {len(rows) - len(kept)} more rows")
    return found


def compare_captures(first: Path, second: Path, *, limit: int = SHOWN_LINES) -> tuple[list[str], str]:
    """Every difference between two captures, and one line saying what was compared."""
    before, after = load_capture(first), load_capture(second)
    if before["root"] != after["root"]:
        raise Refusal(
            f"the captures were taken under different roots, {before['root']} and "
            f"{after['root']}, so every path they hold differs; capture both with one --root"
        )
    found: list[str] = []
    ours, theirs = set(before["scenarios"]), set(after["scenarios"])
    for name in sorted(ours ^ theirs):
        found.append(
            f"{name}: the scenario is only in the {'first' if name in ours else 'second'} capture"
        )
    commands = files = databases = 0
    for name in sorted(ours & theirs):
        ran = _read(first, name, COMMANDS), _read(second, name, COMMANDS)
        listed = _read(first, name, LISTING), _read(second, name, LISTING)
        dumped = _read(first, name, DATABASES), _read(second, name, DATABASES)
        words = own_words(
            _read(first, name, PROCESS), _read(second, name, PROCESS), *listed
        )
        commands += len(ran[0])
        files += len(listed[0])
        databases += len(dumped[0])
        found += compare_commands(name, *ran, words, limit)
        found += compare_files(name, first, second, *listed, words, limit)
        found += compare_databases(name, *dumped, words, limit)
    summary = (
        f"{len(ours & theirs)} scenarios, {commands} commands, {files} files and "
        f"{databases} databases compared: {before['source']} against {after['source']}"
    )
    if before.get("python") != after.get("python"):
        summary += (
            f"; taken with Python {before.get('python')} and {after.get('python')}, and "
            "argparse words its help by version"
        )
    return found, summary


def cmd_compare(args) -> int:
    found, summary = compare_captures(args.first, args.second, limit=0 if args.full else SHOWN_LINES)
    for line in found:
        print(line)
    differences = sum(1 for line in found if not line.startswith("    "))
    print(summary)
    print(f"{differences} difference(s)" if differences else "no difference")
    return 1 if found else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture what crate prints and writes on a disposable library, and compare."
    )
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    verbs = parser.add_subparsers(dest="verb", required=True)

    capture = verbs.add_parser("capture", help="run the scenarios and record what they did")
    capture.add_argument("--out", type=Path, required=True, help="a new directory for the capture")
    capture.add_argument(
        "--root",
        type=Path,
        default=None,
        help="the run's base temporary directory; must be inside the system's, and two "
        "captures are comparable only under the same one",
    )
    capture.add_argument(
        "--rev", default=None, help="run against this revision's src/ instead of the tree's"
    )
    capture.add_argument("--only", default=None, help="a pytest -k expression choosing scenarios")
    capture.add_argument("--keep", action="store_true", help="leave the root and source in place")
    capture.add_argument("--timeout", type=int, default=3600, help="seconds for the scenario run")
    capture.set_defaults(run=cmd_capture)

    compare = verbs.add_parser("compare", help="print every difference between two captures")
    compare.add_argument("first", type=Path)
    compare.add_argument("second", type=Path)
    compare.add_argument("--full", action="store_true", help="print each difference whole")
    compare.set_defaults(run=cmd_compare)
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])
    try:
        return args.run(args)
    except Refusal as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
