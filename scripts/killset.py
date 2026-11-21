#!/usr/bin/env python3
"""The recorded mutation kill set: read it, replay it, and check a replay kept it.

Every unit's mutation table is committed under `docs/mutation/` as JSON, and
each row carries the file it mutated, the `old` and `new` text, its deaths and
the tests that died. So what the suite is known to notice is on disk, and a
refactor can be held to it: every mutation a test killed before the refactor
is still killed after it. That is what "mutation strength does not drop" means
under U290, and this script is its three steps.

    .venv/bin/python scripts/killset.py list [PATH ...] [--rows]
    .venv/bin/python scripts/killset.py rows PATH ... --out rows.toml
    .venv/bin/python scripts/killset.py rows --after BEFORE.json --out rows.toml
    .venv/bin/python scripts/killset.py check BEFORE.json AFTER.json

`list` reads every table and prints, per source file, the recorded killed rows
that are live, stale and ambiguous. A row is KILLED when its table recorded at
least one death. It is LIVE when its file exists and its `old` text occurs in
it exactly once, so `scripts/mutate.py` can apply it today as written; STALE
when the text is gone; AMBIGUOUS when it occurs more than once; GONE when its
file is, or it names none. Two tables that recorded the same substitution in
the same file are one live row, the first table's, and the rest are counted
as duplicates.

`rows` writes a row file for the driver's `replay` pass: the live rows of the
files or directories given, each carrying the table and id it came from, its
text, and its tests. The tests are the row's own subset, or the test files its
recorded kills name when it had none or its subset killed nothing and the kill
came from the full suite; a test file that is gone is left out, and a row left
with none is given none, which the driver reads as "derive it". Stale,
ambiguous and gone rows are left out and counted.

`rows --after BEFORE.json` writes the row file for the same kills after a
refactor: every row the BEFORE table killed, anchored where its text now is.
Text still in its file is written as it was. Text that left its file is
written at another file, with a `moved` reason, only when it stands in
exactly one place under the same top directory now and stood in exactly one
at the commit the BEFORE table was measured on. A line that stood in two
places then has a twin, another guard written the same way, and the one place
left now may be the twin's, whatever its file is called today (188 of the
7,093 live rows on `ff8e5ec` have exactly one twin). What the tree held then
is read from git, which is only read, and when git cannot say the row is not
placed. Anything else is written under `[[dropped]]` as unplaced, for the
author to anchor by hand (a row with the same `source`, the new text and a
`moved` reason) or to map onto the row that now covers it (a `[[mapped]]`
entry with its `reason`).

`check` takes the table measured before and the table measured after and
exits 1 unless every row killed before is killed after, or is mapped in the
AFTER table to a row of it that is killed. It reads the driver's own verdict:
a row whose status is `killed`, and one that broke collection with a death
counts for less, so a kill that became a collection error is reported. A row
whose text changed between the two tables must say why in `moved`, and text
alone does not make it the same guard: a deleted guard and a new line written
the same way elsewhere read as one move. So a row at a new anchor must be
killed by at least one test, by name, that killed it before, or carry a
`moved` reason a person wrote in place of the one `rows --after` writes. Exit
2 is a table that cannot be read, is not a finished, valid batch, or holds
two rows for one source.

A replay table is itself a record. A row killed in one is its source's kill at
the text the replay ran, so a guard a refactor moved stays in the kill set at
its new place, and a later `list` or `rows` finds it there with the tests that
replay ran. A row at a new anchor is believed there on the rule `check` holds
it to, a test in common or a reason a person wrote. Replay tables are never
counted as tables of their own: every row in one came from another table.

Nothing here runs a test or writes a source file. `scripts/mutate.py` is the
one driver, and a replay runs through it under every rule it holds.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import tarfile
import tomllib
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TABLES = Path("docs") / "mutation"

#: The driver's pass kind for a row file this script writes, repeated from
#: `scripts/mutate.py` and held to it by a test.
REPLAY = "replay"

LIVE = "live"
STALE = "stale"
AMBIGUOUS = "ambiguous"
GONE = "gone"
DUPLICATE = "duplicate"
STATES = (LIVE, DUPLICATE, STALE, AMBIGUOUS, GONE)

#: Directories a search for moved text never enters.
SKIPPED_DIRECTORIES = frozenset({"__pycache__", "_vendor", "node_modules"})

#: How the `moved` reason `rows --after` writes opens. A reason that opens
#: this way was written by the tool from the text alone; any other was written
#: by a person, who thereby says the row is the same guard.
AUTOMATIC_MOVE = "the same text, now in "


class Refusal(RuntimeError):
    """The script will not proceed, and says why. Exit 2."""


# ---------------------------------------------------------------------------
# Reading the tables
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Anchor:
    """One exact substitution in one file, and the tests known to notice it."""

    file: str
    old: str
    new: str
    tests: tuple[str, ...] = ()

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.file, self.old, self.new)


@dataclass
class Recorded:
    """One killed row of one table, and where it stands in the tree today."""

    table: str
    id: str
    description: str
    surface: str
    anchor: Anchor
    state: str = ""
    #: The tests that killed it, by name, as its own table recorded them.
    killers: frozenset[str] = frozenset()

    @property
    def source(self) -> tuple[str, str]:
        return (self.table, self.id)


@dataclass
class KillSet:
    rows: list[Recorded]
    tables: int = 0
    replay_tables: int = 0
    unreadable: list[str] = field(default_factory=list)
    all_rows: int = 0

    def in_state(self, state: str) -> list[Recorded]:
        return [row for row in self.rows if row.state == state]


def killed(row: object) -> bool:
    """Whether a table's row recorded at least one death."""
    if not isinstance(row, dict):
        return False
    deaths = row.get("deaths")
    return isinstance(deaths, int) and not isinstance(deaths, bool) and deaths > 0


def source_of(row: dict) -> tuple[str, str] | None:
    """The table and id a replay row came from, or None when it names none."""
    source = row.get("source")
    if not isinstance(source, dict):
        return None
    table, row_id = source.get("table"), source.get("id")
    if isinstance(table, str) and table and isinstance(row_id, str) and row_id:
        return (table, row_id)
    return None


def killer_names(row: dict) -> frozenset[str]:
    """The tests that killed a row, each by its function's name.

    A node id without its file and without its parameters, so a test that
    moved to another file with the code it tests is still the same test, and
    one that was renamed is not.
    """
    names = set()
    for node in row.get("killed") or []:
        if isinstance(node, str) and node:
            names.add(node.rsplit("::", 1)[-1].split("[", 1)[0])
    return frozenset(names)


def unvouched_move(killers_before: frozenset[str], after: dict) -> str:
    """Why a row killed at a new anchor is not yet known to be the same guard, or "".

    Its text being the same is not enough: a refactor that deletes a guard
    and leaves, renames or writes an identical line elsewhere produces the
    same text at a new place, killed there by that other line's tests. So one
    of two things must hold. A test that killed the row before kills it now,
    by name. Or a person wrote its `moved` reason, which is them saying it is
    the same guard; the reason `rows --after` writes says only where the text
    is.
    """
    reason = str(after.get("moved") or "").strip()
    if not reason:
        return "it gives no moved reason, so nothing says it is the same guard"
    now = killer_names(after)
    if killers_before & now or not reason.startswith(AUTOMATIC_MOVE):
        return ""
    return (
        f"it is killed there only by tests that did not kill it before "
        f"({', '.join(sorted(killers_before)) or 'none recorded'} then, "
        f"{', '.join(sorted(now)) or 'none recorded'} now), and its moved reason is the "
        f"one `rows --after` wrote from the text alone. If it is the same guard, say "
        f"why in `moved` in your own words; if it is not, the kill is lost"
    )


def kill_files(row: dict) -> list[str]:
    """The test files a row's recorded kills name, in order of first mention."""
    found: dict[str, None] = {}
    for node in row.get("killed") or []:
        if isinstance(node, str) and node:
            found.setdefault(node.split("::", 1)[0], None)
    return list(found)


def tests_of(row: dict, repo_root: Path) -> tuple[str, ...]:
    """The tests a replay of ``row`` runs: its subset, else what its kills name.

    The subset is what the row was measured on, so it is the first choice. A
    row promoted to the full suite killed nothing on its subset, and a row
    with no subset ran the whole suite, so for those the kill files are where
    the deaths are. An entry whose file is gone is left out: a path pytest
    cannot find is a usage error, which the driver reads as nothing measured.
    """
    subset = [one for one in row.get("subset") or [] if isinstance(one, str)]
    choices = [kill_files(row)] if row.get("promoted") or not subset else [subset, kill_files(row)]
    for choice in choices:
        present = [one for one in choice if (repo_root / one.split("::", 1)[0]).exists()]
        if present:
            return tuple(present)
    return ()


def anchor_of(row: dict, repo_root: Path) -> Anchor:
    old, new = row.get("old"), row.get("new")
    return Anchor(
        file=row["file"] if isinstance(row.get("file"), str) else "",
        old=old if isinstance(old, str) else "",
        new=new if isinstance(new, str) else "",
        tests=tests_of(row, repo_root),
    )


class Tree:
    """The checkout's files, each read once."""

    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self._texts: dict[str, str | None] = {}

    def text(self, rel: str) -> str | None:
        """A file's text, or None when there is no such file to mutate."""
        if rel not in self._texts:
            path = self.root / rel if rel else None
            try:
                self._texts[rel] = (
                    path.read_text(encoding="utf-8") if path and path.is_file() else None
                )
            except (OSError, UnicodeDecodeError):
                self._texts[rel] = None
        return self._texts[rel]

    def state(self, anchor: Anchor) -> str:
        text = self.text(anchor.file)
        if text is None:
            return GONE
        count = text.count(anchor.old) if anchor.old else 0
        return LIVE if count == 1 else STALE if count == 0 else AMBIGUOUS

    def holders(self, anchor: Anchor) -> list[str]:
        """The files under the anchor's top directory that hold its text exactly once.

        Empty when any file under it holds the text more than once: a guard
        written twice has no one place it moved to.
        """
        top = anchor.file.split("/", 1)[0]
        suffix = Path(anchor.file).suffix
        if not anchor.old or not top or not (self.root / top).is_dir():
            return []
        found: list[str] = []
        for current, directories, files in os.walk(self.root / top):
            directories[:] = sorted(
                one
                for one in directories
                if not one.startswith(".") and one not in SKIPPED_DIRECTORIES
            )
            for name in sorted(files):
                if Path(name).suffix != suffix:
                    continue
                rel = (Path(current) / name).relative_to(self.root).as_posix()
                text = self.text(rel)
                count = text.count(anchor.old) if text is not None else 0
                if count > 1:
                    return []
                if count == 1:
                    found.append(rel)
        return found


def load_table(path: Path) -> dict | None:
    """One table as a mapping holding a list of rows, or None when it is not one."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("rows"), list):
        return None
    return data


def read_kill_set(repo_root: Path) -> KillSet:
    """Every recorded killed row under ``docs/mutation/``, with its state today."""
    tree = Tree(repo_root)
    found = KillSet(rows=[])
    moves: dict[tuple[str, str], list[tuple[str, str, Anchor, dict]]] = {}
    for path in sorted((repo_root / TABLES).glob("*.json")):
        table = load_table(path)
        if table is None:
            found.unreadable.append(path.name)
            continue
        if table.get("pass_kind") == REPLAY:
            found.replay_tables += 1
            when = table.get("when") if isinstance(table.get("when"), str) else ""
            for row in table["rows"]:
                source = source_of(row) if killed(row) else None
                if source is not None:
                    moves.setdefault(source, []).append(
                        (when, path.name, anchor_of(row, repo_root), row)
                    )
            continue
        found.tables += 1
        for row in table["rows"]:
            found.all_rows += 1
            if not killed(row):
                continue
            found.rows.append(
                Recorded(
                    table=path.name,
                    id=str(row.get("id", "")),
                    description=str(row.get("description", "")),
                    surface="user" if row.get("surface") == "user" else "maintainer",
                    anchor=anchor_of(row, repo_root),
                    killers=killer_names(row),
                )
            )

    seen: set[tuple[str, str, str]] = set()
    for row in found.rows:
        row.state = tree.state(row.anchor)
        # The newest replay that still applies speaks for the row: its text
        # when the recorded text left, and its tests either way, since they
        # are the ones that last killed it. A replay at another text is
        # believed only on the rule `check` holds it to.
        for _, _, anchor, replayed in sorted(moves.get(row.source, []), key=_dated, reverse=True):
            if tree.state(anchor) != LIVE:
                continue
            in_place = anchor.key == row.anchor.key
            if in_place or (row.state != LIVE and not unvouched_move(row.killers, replayed)):
                row.anchor = anchor if anchor.tests else Anchor(*anchor.key, row.anchor.tests)
                row.state = LIVE
                break
        if row.state == LIVE:
            if row.anchor.key in seen:
                row.state = DUPLICATE
            seen.add(row.anchor.key)
    return found


def _dated(move: tuple) -> tuple[str, str]:
    return (move[0], move[1])


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def chosen(paths: list[str], repo_root: Path):
    """A test of whether a file is one of the paths given, or under one."""
    if not paths:
        return lambda rel: True
    wanted = []
    for one in paths:
        path = Path(one)
        if path.is_absolute():
            try:
                path = path.resolve().relative_to(repo_root.resolve())
            except ValueError as outside:
                raise Refusal(f"{one} is not inside {repo_root}") from outside
        wanted.append(path.as_posix().rstrip("/"))
    return lambda rel: any(rel == one or rel.startswith(f"{one}/") for one in wanted)


def summary_lines(found: KillSet) -> list[str]:
    counts = Counter(row.state for row in found.rows)
    files = {row.anchor.file for row in found.in_state(LIVE)}
    nameless = sum(1 for row in found.in_state(GONE) if not row.anchor.file)
    lines = [
        f"{found.tables} tables, {found.all_rows} rows, {len(found.rows)} recorded as killed",
        f"{counts[LIVE]} live in {len(files)} files: the text occurs once, so the row "
        "applies today",
        f"{counts[DUPLICATE]} duplicates of a live row: the same substitution in the "
        "same file, recorded by another table",
        f"{counts[STALE]} stale: the text is gone from the file",
        f"{counts[AMBIGUOUS]} ambiguous: the text occurs more than once",
        f"{counts[GONE]} gone: the file no longer exists ({nameless} of them name no file)",
    ]
    if found.replay_tables:
        lines.append(
            f"{found.replay_tables} replay tables read for where a row now lives, "
            "counted as no table of their own"
        )
    if found.unreadable:
        lines.append(
            f"{len(found.unreadable)} files under {TABLES.as_posix()} are not tables: "
            + ", ".join(found.unreadable)
        )
    return lines


def cmd_list(args) -> int:
    found = read_kill_set(args.repo_root)
    wanted = chosen(args.paths, args.repo_root)
    print("\n".join(summary_lines(found)))
    per_file: dict[str, Counter] = {}
    for row in found.rows:
        if row.state == DUPLICATE or not wanted(row.anchor.file):
            continue
        per_file.setdefault(row.anchor.file or "(no file named)", Counter())[row.state] += 1
    print()
    print(f"{'live':>5} {'stale':>5} {'ambiguous':>9} {'gone':>5}  file")
    for name in sorted(per_file, key=lambda one: (-per_file[one][LIVE], one)):
        count = per_file[name]
        print(
            f"{count[LIVE]:>5} {count[STALE]:>5} {count[AMBIGUOUS]:>9} {count[GONE]:>5}  {name}"
        )
    if args.rows:
        print()
        for row in sorted(found.rows, key=lambda one: (one.anchor.file, one.table, one.id)):
            if wanted(row.anchor.file):
                print(f"{row.state:<9} {row.anchor.file}  {row.table}  {row.id}")
    return 0


# ---------------------------------------------------------------------------
# rows
# ---------------------------------------------------------------------------


def toml_string(text: str) -> str:
    """``text`` as a TOML basic string, exact for any text at all."""
    out = ['"']
    for char in text:
        code = ord(char)
        if char in ('"', "\\"):
            out.append("\\" + char)
        elif char == "\n":
            out.append("\\n")
        elif char == "\t":
            out.append("\\t")
        elif code < 0x20 or code == 0x7F:
            out.append(f"\\u{code:04X}")
        else:
            out.append(char)
    out.append('"')
    return "".join(out)


def toml_text(text: str) -> str:
    """Code as TOML: a literal string when that holds it exactly, else escaped.

    A literal string shows the code as it stands in the file, which is what an
    author anchoring a row by hand compares against. It cannot hold a control
    character or a carriage return, one line of it cannot hold its own quote,
    and a block cannot hold three quotes in a row or end in one, which would
    run into the closing delimiter, so those are written as one escaped line.
    The newline after a block's opening delimiter is the one TOML trims, so
    the text itself starts on the next line.
    """
    plain = all(char in "\n\t" or (ord(char) >= 0x20 and ord(char) != 0x7F) for char in text)
    block = "'''" not in text and not text.endswith("'")
    if plain and "\n" not in text and "'" not in text:
        return f"'{text}'"
    if plain and block:
        return f"'''\n{text}'''" if "\n" in text else f"'''{text}'''"
    return toml_string(text)


def row_id(source: tuple[str, str]) -> str:
    """A replay row's id: the table it came from, without its suffix, and its id there."""
    return f"{Path(source[0]).stem}.{source[1]}"


def render_row(
    source: tuple[str, str],
    description: str,
    surface: str,
    anchor: Anchor,
    moved: str = "",
) -> list[str]:
    lines = [
        "[[rows]]",
        f"id = {toml_string(row_id(source))}",
        f"source = {{ table = {toml_string(source[0])}, id = {toml_string(source[1])} }}",
        f"description = {toml_string(description)}",
        f"file = {toml_string(anchor.file)}",
        f"surface = {toml_string(surface)}",
    ]
    if moved:
        lines.append(f"moved = {toml_string(moved)}")
    if anchor.tests:
        lines.append("tests = [" + ", ".join(toml_string(one) for one in anchor.tests) + "]")
    lines.append(f"old = {toml_text(anchor.old)}")
    lines.append(f"new = {toml_text(anchor.new)}")
    lines.append("")
    return lines


def render_dropped(source: tuple[str, str], description: str, reason: str) -> list[str]:
    return [
        "[[dropped]]",
        f"id = {toml_string(row_id(source))}",
        f"description = {toml_string(description)}",
        f"reason = {toml_string(reason)}",
        "",
    ]


def batch_name(args) -> str:
    """The batch's name: the one given, else the row file's stem without a closing ``-rows``.

    The driver names its table and sidecar for the batch, and a unit's row
    file is ``uN-rows.toml`` beside its table ``uN.json``, so a row file
    written as ``uN-replay-before-rows.toml`` measures ``uN-replay-before``.
    """
    return args.name or args.out.stem.removesuffix("-rows") or args.out.stem


def write_rows(out: Path, name: str, body: list[str]) -> None:
    head = [f"name = {toml_string(name)}", f'pass_kind = "{REPLAY}"', ""]
    text = "\n".join([*head, *body])
    tomllib.loads(text)  # what was written is what the driver will read, or nothing is written
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def cmd_rows(args) -> int:
    if args.after is not None:
        return rows_after(args)
    if not args.paths:
        raise Refusal("name the files or directories whose live rows to write, or pass --after")
    found = read_kill_set(args.repo_root)
    wanted = chosen(args.paths, args.repo_root)
    mine = [row for row in found.rows if wanted(row.anchor.file)]
    live = sorted(
        (row for row in mine if row.state == LIVE),
        key=lambda one: (one.anchor.file, one.table, one.id),
    )
    if not live:
        raise Refusal(
            f"no live row names {', '.join(args.paths)}; `killset.py list` shows what is recorded"
        )
    body: list[str] = []
    for row in live:
        body += render_row(row.source, row.description, row.surface, row.anchor)
    write_rows(args.out, batch_name(args), body)
    counts = Counter(row.state for row in mine)
    files = len({row.anchor.file for row in live})
    print(f"{len(live)} live rows in {files} files written to {args.out}")
    print(
        f"left out: {counts[STALE]} stale, {counts[AMBIGUOUS]} ambiguous, {counts[GONE]} gone, "
        f"{counts[DUPLICATE]} duplicates of a live row"
    )
    for row in sorted(mine, key=lambda one: (one.anchor.file, one.table, one.id)):
        if row.state in (STALE, AMBIGUOUS, GONE):
            print(f"  {row.state:<9} {row.anchor.file}  {row.table}  {row.id}")
    return 0


def read_measured(path: Path) -> dict:
    """A table a batch finished and found valid, or a refusal naming what it is instead."""
    table = load_table(path)
    if table is None:
        raise Refusal(f"{path} is not a mutation table")
    if table.get("valid") is not True or table.get("invalid_reason"):
        why = table.get("invalid_reason") or "it does not say it is valid"
        raise Refusal(f"{path} is not a finished, valid batch: {why}")
    return table


def key_of(row: dict) -> tuple[str, str]:
    """What a row is matched by across two tables: where it came from, else its id."""
    return source_of(row) or ("", str(row.get("id", "")))


class Commit:
    """The files a commit held, read from git once per top directory. Git is only read."""

    def __init__(self, repo_root: Path, head: str) -> None:
        self.root = repo_root
        self.head = head
        self._tops: dict[str, dict[str, str] | None] = {}

    def _git(self, *args: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, check=False
        )

    def texts(self, top: str) -> dict[str, str] | None:
        """Every file under ``top`` at the commit, by path, or None when git cannot say.

        A commit git knows that holds no such directory answers with nothing
        in it. A commit git does not know, or none named at all, answers
        None, which a caller must not read as nothing.
        """
        if top not in self._tops:
            self._tops[top] = self._read(top)
        return self._tops[top]

    def _read(self, top: str) -> dict[str, str] | None:
        if not self.head or not top:
            return None
        if self._git("cat-file", "-e", f"{self.head}^{{commit}}").returncode != 0:
            return None
        archived = self._git("archive", "--format=tar", self.head, "--", top)
        if archived.returncode != 0:
            return {}
        texts: dict[str, str] = {}
        with tarfile.open(fileobj=io.BytesIO(archived.stdout)) as archive:
            for member in archive:
                if member.isfile():
                    texts[member.name] = archive.extractfile(member).read().decode(
                        "utf-8", "replace"
                    )
        return texts

    def stood(self, anchor: Anchor) -> int | None:
        """How many places a row's text stood in, under its top directory, at the commit."""
        texts = self.texts(anchor.file.split("/", 1)[0])
        if texts is None:
            return None
        suffix = Path(anchor.file).suffix
        return sum(
            text.count(anchor.old) for name, text in texts.items() if Path(name).suffix == suffix
        )


def moved_to(tree: Tree, anchor: Anchor, commit: Commit) -> tuple[str | None, str]:
    """The file a row's text moved to, or None and why nothing says it moved.

    Text that occurs once in one other file is not yet text that moved there.
    A deleted guard often has a twin, the same line in a neighbouring file,
    and anchoring the deleted row on its twin would replay another guard's
    kill under this one's name; the twin's file may itself have been renamed
    or split since, so asking whether today's holder held the text then does
    not find it. What does is counting: the text must have stood in exactly
    one place at the commit the row was measured on, its own, and stand in
    exactly one now. A line written new elsewhere after its guard was deleted
    still passes this, which is why `check` asks a moved row for more.
    """
    holders = tree.holders(anchor)
    absent = f"the text is {describe_absence(tree.state(anchor))} in {anchor.file}"
    if len(holders) != 1:
        return None, f"{absent} and occurs once in {len(holders)} other files"
    stood = commit.stood(anchor)
    if stood is None:
        return None, (
            f"{absent} and occurs once in {holders[0]}, but git cannot read the tree at "
            f"the commit the table was measured on ({commit.head or 'none named'}), so "
            "nothing says the text moved there"
        )
    if stood != 1:
        return None, (
            f"{absent} and occurs once in {holders[0]}, but it stood in {stood} places at "
            f"{commit.head}, so the one left may be another guard's line and not this "
            "one moved"
        )
    return holders[0], ""


def rows_after(args) -> int:
    """The BEFORE table's kills, anchored where their text is in the tree now."""
    before = read_measured(args.after)
    head = before.get("head") if isinstance(before.get("head"), str) else ""
    tree = Tree(args.repo_root)
    commit = Commit(args.repo_root, head)
    body: list[str] = []
    dropped: list[str] = []
    counts: Counter = Counter()
    for row in before["rows"]:
        if not killed(row):
            continue
        source = source_of(row)
        if source is None:
            raise Refusal(
                f"{args.after} row {row.get('id')!r} names no source; --after reads a table "
                f"measured from a row file `killset.py rows` wrote"
            )
        anchor = anchor_of(row, args.repo_root)
        description = str(row.get("description", ""))
        surface = "user" if row.get("surface") == "user" else "maintainer"
        moved = str(row.get("moved") or "")
        if tree.state(anchor) != LIVE:
            holder, why = moved_to(tree, anchor, commit)
            if holder is None:
                counts["unplaced"] += 1
                dropped += render_dropped(
                    source,
                    description,
                    f"unplaced: {why}. Anchor it by hand, a row with this source, the new "
                    "text and a moved reason, or map it to the row that covers it.",
                )
                continue
            moved = f"{AUTOMATIC_MOVE}{holder}, was in {anchor.file}"
            anchor = Anchor(holder, anchor.old, anchor.new, anchor.tests)
            counts["moved"] += 1
        else:
            counts["in place"] += 1
        body += render_row(source, description, surface, anchor, moved)
    if not body and not dropped:
        raise Refusal(f"{args.after} killed nothing, so there is nothing to replay")
    write_rows(args.out, batch_name(args), [*body, *dropped])
    print(
        f"{counts['in place']} rows in place and {counts['moved']} moved written to {args.out}; "
        f"{counts['unplaced']} unplaced, listed under [[dropped]] and owed an anchor or a mapping"
    )
    return 0


def describe_absence(state: str) -> str:
    return {STALE: "gone", AMBIGUOUS: "ambiguous", GONE: "gone with its file"}.get(state, state)


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------


@dataclass
class Verdict:
    kept: int = 0
    moved: int = 0
    covered: int = 0
    lost: list[str] = field(default_factory=list)


def text_of(row: dict) -> tuple[object, object, object]:
    return (row.get("file"), row.get("old"), row.get("new"))


def strength(row: dict) -> int:
    """How firmly a measured row was killed: 2 killed, 1 a death beside a broken
    collection, 0 nothing.

    The driver calls a row ``killed`` only when a test died and the collected
    count held. A row that broke collection may record deaths too, and the
    driver says of it that it is neither a zero nor a clean kill, so it ranks
    under one. A table of the older form, with no status, is read by its
    deaths alone.
    """
    if not killed(row):
        return 0
    return 2 if row.get("status") in (None, "killed") else 1


def keyed(table: dict, path: Path) -> dict[tuple[str, str], dict]:
    """A table's rows by what they are matched by, refusing two rows under one key."""
    rows: dict[tuple[str, str], dict] = {}
    for row in table["rows"]:
        if not isinstance(row, dict):
            continue
        key = key_of(row)
        if key in rows:
            raise Refusal(
                f"{path} holds two rows for {' '.join(key).strip()}, so which one is the "
                "recorded kill cannot be said"
            )
        rows[key] = row
    return rows


def compare_tables(
    before: dict, after: dict, *, before_path: Path = Path("the first table"),
    after_path: Path = Path("the second table"),
) -> Verdict:
    """Every row killed in ``before``, read against ``after``."""
    before_rows = keyed(before, before_path)
    after_rows = keyed(after, after_path)
    by_id = {str(row.get("id", "")): row for row in after_rows.values()}
    mapped: dict[tuple[str, str], dict] = {}
    for entry in after.get("mapped") or []:
        source = source_of(entry) if isinstance(entry, dict) else None
        if source is not None:
            mapped.setdefault(source, entry)

    verdict = Verdict()
    for key, row in before_rows.items():
        held = strength(row)
        if not held:
            continue
        was = "killed" if held == 2 else str(row.get("status"))
        name = f"{key[0]} {key[1]}".strip()
        now = after_rows.get(key)
        if now is not None:
            if strength(now) < held:
                verdict.lost.append(
                    f"{name}: {was} before, {now.get('status', 'not killed')} after "
                    f"({now.get('deaths', 0)} deaths)"
                )
            elif text_of(now) != text_of(row) and unvouched_move(killer_names(row), now):
                verdict.lost.append(
                    f"{name}: its text differs between the two tables, and "
                    f"{unvouched_move(killer_names(row), now)}"
                )
            elif text_of(now) != text_of(row):
                verdict.moved += 1
            else:
                verdict.kept += 1
            continue
        entry = mapped.get(key)
        if entry is None:
            verdict.lost.append(f"{name}: {was} before, and no row and no mapping after")
            continue
        target = by_id.get(str(entry.get("to", "")))
        reason = str(entry.get("reason") or "").strip()
        if target is None:
            verdict.lost.append(f"{name}: mapped to {entry.get('to')!r}, which is no row after")
        elif strength(target) < held:
            verdict.lost.append(
                f"{name}: mapped to {entry.get('to')!r}, which is "
                f"{target.get('status', 'not killed')} after"
            )
        elif not reason:
            verdict.lost.append(f"{name}: mapped to {entry.get('to')!r} with no reason")
        else:
            verdict.covered += 1
    return verdict


def cmd_check(args) -> int:
    before = read_measured(args.before)
    after = read_measured(args.after)
    verdict = compare_tables(before, after, before_path=args.before, after_path=args.after)
    total = verdict.kept + verdict.moved + verdict.covered + len(verdict.lost)
    print(
        f"{total} rows killed before: {verdict.kept} killed after as written, "
        f"{verdict.moved} killed after at a new anchor, {verdict.covered} covered by a "
        f"mapped row that is killed, {len(verdict.lost)} lost"
    )
    for line in verdict.lost:
        print(f"LOST {line}")
    return 1 if verdict.lost else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read, replay and check the recorded kill set.")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    verbs = parser.add_subparsers(dest="verb", required=True)

    listing = verbs.add_parser("list", help="count the recorded kills per source file")
    listing.add_argument("paths", nargs="*", help="files or directories; all when none")
    listing.add_argument("--rows", action="store_true", help="also list every row and its state")
    listing.set_defaults(run=cmd_list)

    rows = verbs.add_parser("rows", help="write a replay row file for the driver")
    rows.add_argument("paths", nargs="*", help="files or directories whose live rows to write")
    rows.add_argument("--after", type=Path, default=None, help="a table measured before a refactor")
    rows.add_argument("--out", type=Path, required=True, help="the .toml row file to write")
    rows.add_argument(
        "--name",
        default=None,
        help="the batch name; defaults to the row file's stem without a closing -rows",
    )
    rows.set_defaults(run=cmd_rows)

    check = verbs.add_parser("check", help="every row killed before is killed after")
    check.add_argument("before", type=Path, help="the table measured on the base")
    check.add_argument("after", type=Path, help="the table measured on the branch")
    check.set_defaults(run=cmd_check)
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
