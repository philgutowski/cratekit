"""The parts of `scripts/mutate.py` that run no test: the row file, the file surgery
verified against `git show HEAD`, the derived subset, and the table written out.

Imports nothing from the driver, which loads it by path and reads every name here
off itself.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import tomllib
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

#: METHOD's hard row caps, enforced because a cap nobody enforced did not hold.
ROW_CAPS = {"light": 25, "full": 45}

#: The pass that measures recorded rows again (U297). It has no cap because it
#: chooses nothing: every row names the table and id it came from.
REPLAY = "replay"
PASS_KINDS = (*ROW_CAPS, REPLAY)

#: Where the recorded tables a replay row's source names live.
RECORDED_TABLES = Path("docs") / "mutation"


class DriverRefusal(RuntimeError):
    """The driver will not proceed. Loud on purpose, never a warning."""


class RestoreVerificationError(RuntimeError):
    """A restored file does not match ``git show HEAD``. Nothing continues."""


class MeasurementFailure(RuntimeError):
    """pytest ran and produced nothing readable: an error, never a refused row or a zero."""


class StateLeak(RuntimeError):
    """A child wrote to the REAL installation state, or changed an entry directly under
    the filesystem root (R-1917), and the batch stops. Not a
    ``DriverRefusal``, which ``measure_row`` would file as one refused row."""


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
    #: The table and row id a replay row came from, and why its text differs
    #: from what that table recorded, when it does (U297).
    source: tuple[str, str] | None = None
    moved: str = ""

    def fingerprint(self) -> str:
        """What ``--resume`` matches on, so an edited row's old number is not inherited."""
        payload = "\0".join([self.id, self.file, self.old, self.new, self.kind])
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class Dropped:
    """A row that was considered and not run, with the reason it was not."""
    id: str
    description: str
    reason: str


@dataclass(frozen=True)
class Mapped:
    """A recorded row a replay batch has no row for, and the row that covers it."""
    source: tuple[str, str]
    to: str
    reason: str

    def to_dict(self) -> dict:
        source = {"table": self.source[0], "id": self.source[1]}
        return {"source": source, "to": self.to, "reason": self.reason}


def read_source(entry: dict, what: str) -> tuple[str, str] | None:
    """The ``source`` of a row or a mapped entry, None when absent, refused when half named."""
    if "source" not in entry:
        return None
    source = entry["source"]
    table = source.get("table") if isinstance(source, dict) else None
    row_id = source.get("id") if isinstance(source, dict) else None
    if not (isinstance(table, str) and table and isinstance(row_id, str) and row_id):
        raise DriverRefusal(
            f"{what}: source must name the table and the row it came from, "
            f'source = {{ table = "u114.json", id = "G3" }}'
        )
    return (table, row_id)


def read_spec(spec_path: Path) -> dict:
    """A row file's contents, TOML or JSON by its suffix."""
    text = spec_path.read_text(encoding="utf-8")
    if spec_path.suffix == ".toml":
        return tomllib.loads(text)
    if spec_path.suffix == ".json":
        return json.loads(text)
    raise DriverRefusal(f"{spec_path.name}: row files are .toml or .json, not {spec_path.suffix!r}")


def refuse_unrecorded_sources(repo_root: Path, rows: list[Row], mapped: list[Mapped]) -> None:
    """Refuse a replay naming a source that is not a recorded kill, or a row whose file or
    text is not its source's and says no ``moved``: new rows would pass the caps under a
    borrowed name. Read before anything runs."""
    tables: dict[str, dict[str, dict] | None] = {}

    def recorded(table: str) -> dict[str, dict] | None:
        if table not in tables:
            path = repo_root / RECORDED_TABLES / table
            try:
                data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
            except (OSError, UnicodeDecodeError, ValueError):
                data = None
            held = data.get("rows") if isinstance(data, dict) else None
            tables[table] = (
                {str(one.get("id")): one for one in held if isinstance(one, dict)}
                if isinstance(held, list) and Path(table).name == table
                else None
            )
        return tables[table]
    named = [(f"row {row.id}", row.source, row) for row in rows if row.source]
    named += [(f"the mapping to {one.to}", one.source, None) for one in mapped]
    for what, (table, row_id), replayed in named:
        held = recorded(table)
        shown = (RECORDED_TABLES / table).as_posix()
        if held is None:
            raise DriverRefusal(f"{what}: its source {shown} is not a recorded table")
        row = held.get(row_id)
        if row is None:
            raise DriverRefusal(f"{what}: {shown} holds no row {row_id!r}")
        deaths = row.get("deaths")
        if not (isinstance(deaths, int) and not isinstance(deaths, bool) and deaths > 0):
            raise DriverRefusal(
                f"{what}: {shown} row {row_id!r} recorded no death, so there is no kill "
                f"of it to replay"
            )
        if replayed is None or replayed.moved.strip():
            continue
        written = (replayed.file, replayed.old, replayed.new)
        if written != (row.get("file"), row.get("old"), row.get("new")):
            raise DriverRefusal(
                f"{what}: its file or text is not what {shown} recorded for {row_id!r}, "
                f"and it gives no moved reason. A guard anchored again by hand says so "
                f"in moved; a new row belongs in a light or a full pass."
            )


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=repo_root, capture_output=True, check=False)


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


def head_sha(repo_root: Path, how: str = "--short") -> str:
    done = _git(repo_root, "rev-parse", how, "HEAD")
    return done.stdout.decode("utf-8", "replace").strip() or "unknown"


def branch_name(repo_root: Path) -> str:
    return head_sha(repo_root, "--abbrev-ref")


def apply_mutation(text: str, old: str, new: str, *, allow_append: bool = False) -> str:
    """Return ``text`` with ``old`` replaced by ``new``; absent or ambiguous text is refused."""
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
    repo_root: Path, rel: str, old: str, new: str, *, allow_append: bool = False,
    head_verify: bool = True,
):
    """Apply a mutation for the block, then always restore and verify against HEAD, or
    with ``head_verify=False`` (a target declared dirty) against the snapshot, the weaker
    check the table names per row."""
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
    """Every module path a source file imports, lazy ones included; ``from a import b``
    adds both ``a`` and ``a.b``, since ``b`` may be a submodule."""
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
    """``(test paths, why)``, None for the whole suite: a test file itself, a source
    module's importers, or else the test files naming the file."""
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
    source: dict | None = None
    moved: str = ""

    def to_dict(self) -> dict:
        """The sidecar's row; ``source`` and ``moved`` only when set, as before replay (U297)."""
        data = dict(self.__dict__)
        for key in ("source", "moved"):
            if not data[key]:
                del data[key]
        return data


#: The sidecar's leading keys, in the order they are written.
SIDECAR_KEYS = (
    "name", "pass_kind", "branch", "head", "when", "valid", "invalid_reason",
    "baseline_collected", "baseline_exit", "pytest_runs", "state_guarded", "reused_rows",
    "known_failures", "known_source", "temp_place", "temp_on_disk", "baseline_source",
    "baseline_note", "subset_baselines",
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
    known_failures: int = 0
    known_source: str = ""
    temp_place: str = ""
    temp_on_disk: int = 0
    baseline_source: str = "measured"
    baseline_note: str = ""
    subset_baselines: int = 0
    mapped: list[Mapped] = field(default_factory=list)

    def to_dict(self) -> dict:
        """The sidecar. ``mapped`` is a replay pass's key and no other pass writes it."""
        data = {key: getattr(self, key) for key in SIDECAR_KEYS}
        data["control"] = self.control.to_dict() if self.control else None
        data["rows"] = [one.to_dict() for one in self.results]
        data["dropped"] = [one.__dict__ for one in self.dropped]
        if self.pass_kind == REPLAY:
            data["mapped"] = [one.to_dict() for one in self.mapped]
        return data


def composite_note(batch: Batch, result: RowResult) -> str:
    """What a zero row owes: a user facing one a composite, a maintainer facing one a line."""
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


def render_markdown(batch: Batch, added_env, scrubbed_env: dict[str, str]) -> str:
    """The table, naming what every child's environment was given and what it lost."""
    lines: list[str] = []

    def add(*texts: str) -> None:
        lines.extend(texts)
    add(f"# Mutation table: {batch.name}", "")
    add(
        f"Measured by `scripts/mutate.py` on {batch.when}, branch `{batch.branch}` "
        f"at `{batch.head}`. Pass kind: {batch.pass_kind}.",
        "",
    )
    if batch.pass_kind == REPLAY:
        add(
            "A replay pass measures again rows a table under `docs/mutation/` already "
            "recorded, so it has no row cap and chooses no rows: every row below names "
            "the table and the id it came from. One full baseline and one null control "
            "serve the batch, and each row ran on its own subset (U297).",
            "",
        )
    add(
        f"Baseline: green, {batch.baseline_collected} collected. "
        f"pytest invocations for this batch: {batch.pytest_runs}.",
        "",
    )
    if batch.baseline_source == "read":
        add(
            f"Full baseline: READ, not measured by this driver; {batch.baseline_note}. "
            "The null control below ran the full suite in this driver's own "
            "environment and was held to that collected count (U271)."
        )
    else:
        why = f" ({batch.baseline_note})" if batch.baseline_note else ""
        add(f"Full baseline: measured by this driver{why}.")
    add("", f"Subset baselines: {batch.subset_baselines}, each measured by this driver.")
    if batch.known_failures:
        add(
            "",
            f"Known failures: {batch.known_failures} node ids whose failure is this "
            f"machine's and not the tree's, read from `{batch.known_source}` and "
            "subtracted from every run, the baselines and the rows alike. The "
            "baseline is green net of them, and a death among them is not counted. "
            "This is a Linux measure of a macOS suite; the full battery is owed on "
            "a Mac.",
        )
    if batch.temp_place:
        again = (
            f", and after each run that collected them the {batch.temp_on_disk} test(s) "
            "the baseline ran on disk ran again on disk, their outcome there standing, "
            "in runs the invocation count above does not include"
            if batch.temp_on_disk
            else ""
        )
        add(
            "",
            f"Temporary files: {'in memory' if batch.temp_place == 'memory' else 'on disk'}, "
            "the place the known failures were "
            f"measured in, each run given a fresh directory there as `TMPDIR`{again} (U273).",
        )
    add(
        "",
        "Environment: inherited from the calling shell, then added to. Added: "
        + "; ".join(added_env)
        + ". Removed: "
        + "; ".join(f"{name} ({why})" for name, why in scrubbed_env.items())
        + ". Nothing else was scrubbed, because a hand built environment is how a "
        "missing binary reddens a baseline and every row after it.",
        "",
    )
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
            "lands there rather than on this machine (R-343). Only those roots, and "
            "the names directly under the filesystem root (R-1917), are watched; "
            "the sandbox also redirects HOME and the data root, and "
            f"a child reaching one of those is not seen by this guard.{reused}",
            "",
        )
    if not batch.valid:
        add("## THIS BATCH IS INVALID", "", batch.invalid_reason, "")
        return "\n".join(lines) + "\n"
    control = batch.control
    if control is not None:
        add(
            f"Null control `{control.id}`: killed {control.deaths}, collected "
            f"{control.collected} against {control.baseline_collected}. The control "
            f"is a semantically empty change, so a zero here is what makes every "
            f"other number in this table believable.",
            "",
        )
    add("## Summary", "", "| id | file | surface | subset | collected | kills | status |")
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
        add("## Zero rows and what they owe", "")
        for one in zeros:
            add(f"- `{one.id}` ({one.surface} facing): {composite_note(batch, one)}")
        add("")
    if batch.mapped:
        add(
            "## Mapped",
            "",
            "Recorded rows this batch has no row for, each with the row that covers it. "
            "`scripts/killset.py check` holds each mapping to a row that is killed.",
            "",
        )
        for one in batch.mapped:
            add(f"- `{one.source[0]}` row `{one.source[1]}` is covered by `{one.to}`: {one.reason}")
        add("")
    if batch.dropped:
        add("## Considered and dropped", "")
        if batch.pass_kind == REPLAY:
            add(
                "Recorded rows this replay left out and did NOT measure. They are not "
                "coverage, and `scripts/killset.py check` fails on one that was killed "
                "before and is neither a row nor mapped here."
            )
        else:
            add(
                f"METHOD caps a {batch.pass_kind} pass at {ROW_CAPS[batch.pass_kind]} rows. "
                f"These were ranked below the cap and NOT measured. They are not coverage."
            )
        add("")
        for one in batch.dropped:
            add(f"- `{one.id}`: {one.description} Dropped because: {one.reason}")
        add("")
    add("## Row definitions", "")
    for one in batch.results:
        add(f"### `{one.id}`", "", one.description, "", f"- File: `{one.file}`")
        if one.source:
            add(f"- Source: `{one.source['table']}`, row `{one.source['id']}`")
        if one.moved:
            add(f"- Moved: {one.moved}")
        add(f"- Surface: {one.surface}", f"- Subset: {one.subset_reason}")
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
            add("- Killed:", *(f"  - `{node}`" for node in shown))
            if len(one.killed) > len(shown):
                add(f"  - ... and {len(one.killed) - len(shown)} more, see the JSON sidecar")
        if one.collect_errors:
            add(f"- Collection errors: {', '.join(f'`{e}`' for e in one.collect_errors)}")
        for label, text in (("Old text:", one.old), ("New text:", one.new)):
            add("", label, "", _block(text))
        add("")
    return "\n".join(lines) + "\n"


def write_outputs(batch: Batch, out_dir: Path, markdown_text: str) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    markdown = out_dir / f"{batch.name}.md"
    sidecar = out_dir / f"{batch.name}.json"
    markdown.write_text(markdown_text, encoding="utf-8")
    sidecar.write_text(json.dumps(batch.to_dict(), indent=2) + "\n", encoding="utf-8")
    return markdown, sidecar
