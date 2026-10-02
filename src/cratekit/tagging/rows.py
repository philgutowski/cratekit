"""Write a row's genre from its file where the two disagree (R-816).

WHY THIS EXISTS. The source system's research pass wrote a specific genre onto
each file and never reloaded the database rows, so 773 rows of one library went
on carrying a word their files had stopped carrying. Adoption and the genre
report read the row. The only way to bring a row into agreement was a reload in
rekordbox, which overwrites every tag field, and at one sitting changed keys.

WHAT IT WRITES IS ``GenreID`` AND NOTHING ELSE. The plan is built by
:func:`cratekit.write.metadata.plan_genre_retag` and applied by
:func:`cratekit.tagging.retag.apply_library`, under the ``RETAG_GENRE`` policy.
Both sat with no caller in ``src`` from the unit that wrote them until this
one, so their failure paths are this module's to hold, and the read back below
is where they are held: every written row is read again from SQL after the
commit, its genre must be the file's word, and no column other than the genre
and the binding's bookkeeping columns may have moved. A beat grid, a tempo or
a BPM moving refuses there by name, after the guard already refused it before
the commit.

THE FILE IS THE AUTHORITY IN THIS DIRECTION ONLY. Nothing here writes a file.
This module calls the tag reader and no tag writer.

A GENRE LOOKUP ROW IS LINKED AND NEVER CREATED. A file word the library has no
active lookup row for is left alone and counted, for the reason
:func:`cratekit.write.metadata.resolve_genre_id` gives.

EVERY LIVE ROW LANDS IN EXACTLY ONE OUTCOME, :data:`OUTCOMES`, and the counts
are zero filled, so "none of those here" and "this build does not count that"
are never the same output. A file that could not be read is counted apart from
a file that holds no genre, through the checked reader, because folding the two
together reports a damaged file as an untagged one.

THE ROW'S WORD IS READ THE WAY ADOPTION READS IT, through
:func:`cratekit.adopt.collection.genre_of`, because what this verb repairs is
what that reader returns.

Layer: modules. It opens no database of its own and names no verb.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.adopt import collection
from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    locations,
    rb_writer,
    session,
    snapshot,
    tags,
    taxonomy,
)
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import retag
from cratekit.write import metadata, trees

#: The name a session record carries for this write.
WORKFLOW = "tag-rows"

#: What the write is filed under in a session record's change summary. A stable
#: identifier and never a display name, for the reason
#: ``cratekit.write.metadata_cli.CHANGE_KEY`` gives.
CHANGE_KEY = "content.genre"

#: The outcomes, in the order a summary lists them.
AGREE = "agree"
WRITE = "write"
FILE_TOO_COARSE = "file-too-coarse"
GENRE_UNKNOWN = "genre-unknown"
FILE_BLANK = "file-blank"
FILE_UNREADABLE = "file-unreadable"
FILE_MISSING = "file-missing"
PATH_UNMAPPED = "path-unmapped"
NO_PATH = "no-path"

OUTCOMES: tuple[str, ...] = (
    AGREE,
    WRITE,
    FILE_TOO_COARSE,
    GENRE_UNKNOWN,
    FILE_BLANK,
    FILE_UNREADABLE,
    FILE_MISSING,
    PATH_UNMAPPED,
    NO_PATH,
)

#: The outcomes in which the file's genre was never learned. A summary names
#: these apart, because a clean answer over rows nobody could read is not one.
UNREAD: tuple[str, ...] = (FILE_UNREADABLE, FILE_MISSING, PATH_UNMAPPED, NO_PATH)

#: What an item whose row is not written says it does.
LEAVE = "leave"

#: How many word pairs a summary names.
NAMED_PAIRS = 5

#: How many identifiers one SQL statement names. Under every SQLite build's
#: bound parameter limit, the oldest of which is 999.
_CHUNK = 500

_ORIGIN = ("tagging", "rows")


@dataclass(frozen=True, slots=True)
class Item:
    """One row whose word differs from a non blank word on its file.

    ``action`` is :data:`WRITE` or :data:`LEAVE`. ``reason`` is the outcome a
    left row was counted under and is empty on a write. ``genre_id`` is the
    lookup row a write links and is empty on a left row.
    """

    content_id: str
    path: str
    row: str
    file: str
    action: str
    reason: str = ""
    genre_id: str = ""

    def digested(self) -> dict[str, str]:
        """What the digest covers: what is written, and why a row is not."""
        return {
            "content_id": self.content_id,
            "row": self.row,
            "file": self.file,
            "action": self.action,
            "reason": self.reason,
            "genre_id": self.genre_id,
        }

    def to_json(self) -> dict[str, str]:
        """The item as the gate shows it, with the file it was read from."""
        return {**self.digested(), "path": self.path}


@dataclass(frozen=True, slots=True)
class RowsPlan:
    """Every differing row, the count of every outcome, and the write itself."""

    items: tuple[Item, ...]
    counts: Mapping[str, int]
    changes: metadata.Plan

    @property
    def writes(self) -> tuple[Item, ...]:
        return tuple(item for item in self.items if item.action == WRITE)

    @property
    def rows(self) -> int:
        """Every live row the walk counted."""
        return sum(self.counts.values())

    @property
    def unread(self) -> int:
        """Rows whose file's genre was never learned."""
        return sum(self.counts[name] for name in UNREAD)

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to.

        OVER THE ITEMS AND THE COUNTS, AND NOTHING THAT NAMES A COPY. No
        database path, no state path, no resolved file path and no time, so a
        rehearsal on a disposable copy of the database digests equal to the
        live plan when the rows and the files are the same.
        """
        return digest_of(
            {
                "kind": WORKFLOW,
                "items": [item.digested() for item in self.items],
                "counts": dict(self.counts),
            }
        )

    def pairs(self, limit: int = NAMED_PAIRS) -> list[dict[str, Any]]:
        """The most common (row word, file word) pairs among the writes."""
        seen = Counter((item.row, item.file) for item in self.writes)
        ordered = sorted(seen.items(), key=lambda entry: (-entry[1], entry[0]))
        return [{"row": row, "file": file, "rows": rows} for (row, file), rows in ordered[:limit]]


@dataclass(frozen=True, slots=True)
class Written:
    """What one apply did, and what the database says about it afterwards.

    ``wrong`` names each written row whose genre does not read back as its
    file's word. ``moved`` names each written row with a column other than the
    genre and the bookkeeping columns changed. Both are empty on a good run and
    :func:`assert_read_back` refuses when either is not.
    """

    session_id: str
    written: int
    read_back: int
    wrong: tuple[str, ...] = ()
    moved: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


def _prefix_rules(cfg: config.Config) -> list[locations.PrefixRule]:
    return [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]


def _file_of(
    recorded: str, *, root: Path, prefix_map: Sequence[locations.PrefixRule]
) -> tuple[Path | None, str]:
    """The file a recorded path names on this machine, or why there is none.

    A VOLUME THAT IS NOT MOUNTED IS ``file-missing`` AND NEVER A FAILURE. Its
    rows resolve to a path nothing is at, exactly as a deleted file's do, and
    the walk cannot tell the two apart, so it counts them together and goes on.
    """
    try:
        _, resolved = trees.located(recorded, root=root, prefix_map=prefix_map)
    except locations.LocationDecodeError:
        return None, NO_PATH
    if resolved.resolution is locations.Resolution.UNMAPPED:
        return None, PATH_UNMAPPED
    if resolved.path is None:
        return None, NO_PATH
    path = Path(resolved.path)
    if not path.is_file():
        return None, FILE_MISSING
    return path, ""


def _file_word(path: Path) -> tuple[str, str]:
    """The file's genre, or why it has none to give. Answers (word, outcome)."""
    try:
        word = (tags.read_tags_checked(path, ("genre",))["genre"] or "").strip()
    except tags.TagReadFailed:
        return "", FILE_UNREADABLE
    return word, ("" if word else FILE_BLANK)


def _protected(declared: taxonomy.Taxonomy, row_word: str, file_word: str) -> bool:
    """A too coarse file word does not replace a specific word on the row.

    SPECIFIC MEANS NON BLANK AND NOT TOO COARSE ITSELF. A blank row, or a row
    carrying a catch all, loses nothing to another catch all and gains
    agreement with its file, so it is written.
    """
    return (
        declared.is_too_coarse_as_source(file_word)
        and bool(row_word)
        and not declared.is_too_coarse_as_source(row_word)
    )


def plan_rows(cfg: config.Config, db: Any, declared: taxonomy.Taxonomy) -> RowsPlan:
    """Walk the collection once and sort every live row into one outcome.

    A TOMBSTONE IS SKIPPED AND NOT COUNTED, as the genre report skips it: a row
    the person removed is not a row whose genre anybody reads.

    THE ITEMS ARE ORDERED BY CONTENT IDENTIFIER, so two walks of one library
    digest the same whatever order the database returned its rows in.

    NOTHING IS PENDING ON THE HANDLE WHEN THIS RETURNS, AND NO MAPPED ROW
    LEAVES WITH THE PLAN. It reads rows and resolves lookup rows and sets
    nothing, and what it returns is values, so the handle may be a read one
    that is closed before the gate is asked.
    """
    root = Path(cfg.library.root)
    prefix_map = _prefix_rules(cfg)
    counts = dict.fromkeys(OUTCOMES, 0)
    differing: dict[str, tuple[Any, str, str, str]] = {}
    held: dict[str, tuple[str, str, str]] = {}

    for row in db.get_content():
        if trees.soft_delete_marker(row):
            continue
        content_id = str(row.ID)
        path, outcome = _file_of(
            str(getattr(row, "FolderPath", "") or ""), root=root, prefix_map=prefix_map
        )
        if path is None:
            counts[outcome] += 1
            continue
        file_word, outcome = _file_word(path)
        if outcome:
            counts[outcome] += 1
            continue
        row_word = collection.genre_of(row).strip()
        if row_word == file_word:
            counts[AGREE] += 1
            continue
        if _protected(declared, row_word, file_word):
            counts[FILE_TOO_COARSE] += 1
            held[content_id] = (str(path), row_word, file_word)
            continue
        differing[content_id] = (row, str(path), row_word, file_word)

    changes = metadata.plan_genre_retag(
        [entry[0] for entry in differing.values()],
        {content_id: entry[3] for content_id, entry in differing.items()},
        db=db,
    )
    linked = {change.content_id: str(change.new) for change in changes.changes}

    items: list[Item] = [
        Item(content_id, path, row_word, file_word, LEAVE, reason=FILE_TOO_COARSE)
        for content_id, (path, row_word, file_word) in held.items()
    ]
    for content_id, (_row, path, row_word, file_word) in differing.items():
        genre_id = linked.get(content_id)
        if genre_id is None:
            counts[GENRE_UNKNOWN] += 1
            items.append(Item(content_id, path, row_word, file_word, LEAVE, reason=GENRE_UNKNOWN))
            continue
        counts[WRITE] += 1
        items.append(Item(content_id, path, row_word, file_word, WRITE, genre_id=genre_id))
    items.sort(key=lambda item: item.content_id)
    return RowsPlan(items=tuple(items), counts=MappingProxyType(counts), changes=changes)


# ---------------------------------------------------------------------------
# The apply and the read back
# ---------------------------------------------------------------------------


def _chunks(values: Sequence[str]) -> Iterable[Sequence[str]]:
    for start in range(0, len(values), _CHUNK):
        yield values[start : start + _CHUNK]


def _columns(db: Any, content_ids: Sequence[str]) -> dict[str, dict[str, Any]]:
    """Every column of the named content rows, from SQL, by content identifier.

    FROM SQL AND NOT FROM THE MAPPED ROWS, so what is compared across the write
    is what the table holds and not what the session remembers setting.
    """
    from sqlalchemy import text

    found: dict[str, dict[str, Any]] = {}
    for chunk in _chunks(content_ids):
        marks = ", ".join(f":id{index}" for index in range(len(chunk)))
        result = db.session.execute(
            text(f"SELECT * FROM {rb_writer.CONTENT_TABLE} WHERE ID IN ({marks})"),
            {f"id{index}": value for index, value in enumerate(chunk)},
        )
        for row in result.mappings():
            found[str(row["ID"])] = dict(row)
    return found


def _genre_names(db: Any) -> dict[str, str]:
    """Every genre lookup row's name by identifier, from SQL."""
    from sqlalchemy import text

    result = db.session.execute(text("SELECT ID, Name FROM djmdGenre"))
    return {str(row[0]): str(row[1] or "").strip() for row in result}


def _mapped(db: Any, content_ids: Sequence[str]) -> dict[str, Any]:
    """The mapped content rows the write sets a field on, by identifier."""
    from pyrekordbox.db6 import tables

    found: dict[str, Any] = {}
    for chunk in _chunks(content_ids):
        query = db.session.query(tables.DjmdContent).filter(tables.DjmdContent.ID.in_(chunk))
        for row in query.all():
            found[str(row.ID)] = row
    return found


def judge(
    writes: Sequence[Item],
    before: Mapping[str, Mapping[str, Any]],
    after: Mapping[str, Mapping[str, Any]],
    names: Mapping[str, str],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """What the read back found wrong. Answers (wrong, moved). Pure.

    ``wrong`` is a written row whose genre is not its file's word now, or that
    cannot be found. ``moved`` is a written row with any column changed other
    than the genre and :data:`cratekit.core.rb_writer.BOOKKEEPING_COLUMNS`,
    which the binding bumps on every commit.
    """
    wrong: list[str] = []
    moved: list[str] = []
    for item in writes:
        was, now = before.get(item.content_id), after.get(item.content_id)
        if was is None or now is None:
            wrong.append(f"{item.content_id}: the row could not be read")
            continue
        word = names.get(str(now.get("GenreID") or ""), "")
        if word != item.file:
            wrong.append(f"{item.content_id}: reads {word!r}, the file says {item.file!r}")
        changed = sorted(
            column
            for column in now
            if column != "GenreID"
            and column not in rb_writer.BOOKKEEPING_COLUMNS
            and now[column] != was.get(column)
        )
        if changed:
            moved.append(f"{item.content_id}: {', '.join(changed)}")
    return tuple(wrong), tuple(moved)


def _empty(value: Any) -> bool:
    return value in rb_writer.FIELD_EMPTIES["GenreID"]


def assert_rows_as_planned(plan: RowsPlan, mapped: Mapping[str, Any]) -> None:
    """Refuse when a row to be written is not the row the plan read.

    THE PLAN IS MADE ON A READ HANDLE AND THE WRITE ON ANOTHER, so the one thing
    the apply asks the database again is whether each row still carries the
    genre the plan saw it carrying, and is still a live row. A row that moved
    is a row nobody was shown, and nothing is written for any of them.

    ``mapped`` is the write handle's own rows, so the tombstone is read through
    :func:`cratekit.write.trees.soft_delete_marker`, the one reader of that
    column, which refuses a row that cannot say.
    """
    moved: list[str] = []
    for change in plan.changes.changes:
        row = mapped.get(change.content_id)
        if row is None or trees.soft_delete_marker(row):
            moved.append(f"{change.content_id}: no longer a live row")
            continue
        held, planned = getattr(row, "GenreID", None), change.current
        if (_empty(held) and _empty(planned)) or str(held) == str(planned):
            continue
        moved.append(f"{change.content_id}: its genre changed since the plan")
    if moved:
        raise refuse(
            "decision-stale",
            f"{len(moved)} of {len(plan.changes.changes)} row(s) to be written are "
            f"not as the plan read them, so nothing was written: " + "; ".join(moved),
            steps=("run the verb again and approve the plan as it is now",),
            origin=_ORIGIN,
            detail={"moved": moved},
        )


def _record_commit(record: session.SessionRecord, written: int, cfg: config.Config) -> None:
    """Record this write's commit on its session record, when it wrote anything.

    A RUN THAT WROTE NOTHING CLAIMS NO COMMIT, for the reason
    :func:`cratekit.write.trees._record_membership_commit` gives: a restore
    reads a committed source as work it would discard.
    """
    if written <= 0:
        return
    session.record_commit(
        record,
        CHANGE_KEY,
        session.ChangeSummary((session.TreeChange(tree=CHANGE_KEY, updated=written),)),
        cfg,
    )


def apply_rows(
    cfg: config.Config,
    db: Any,
    plan: RowsPlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Write the plan's genres, commit behind the guard, and read them back.

    THE SESSION SPINE IS CALLED, NOT REBUILT, and it is the one every database
    writer here uses: the three gates with a record kept, a capture the commit
    happens behind, the analysis watch over the roots named, the commit
    witness, and the guarded commit.

    THE ROWS ARE CHECKED AGAINST THE PLAN BEFORE THE CAPTURE IS TAKEN, by
    :func:`assert_rows_as_planned`, so a stale plan refuses with no capture and
    nothing pending.

    THE MAPPED ROWS AND THE SNAPSHOT ARE READ BEFORE THE FIRST FIELD IS SET,
    and nothing is read between the first set and the commit. A query there
    would flush the pending work before the whitelist has judged it.

    THE READ BACK IS TAKEN HERE AND JUDGED BY THE CALLER, through
    :func:`assert_read_back`, after the session has closed. The commit has
    landed by then and the record says so, so a refusal over what was read
    back leaves the capture as the undo instead of an abandoned session over
    rows that are durable.

    ``analysis_roots`` has no default for the reason the membership writer
    gives: a watch that watches nothing reports every session clean.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    writes = plan.writes
    content_ids = [item.content_id for item in writes]
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record = gates.record
        mapped = _mapped(db, content_ids)
        assert_rows_as_planned(plan, mapped)

        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)

        before = _columns(db, content_ids)
        written = 0
        try:
            report = retag.apply_library(retag.LibraryPlan(plan=plan.changes), mapped)
            written = len(report.written)
            rb_writer.commit_guarded(db)
        except BaseException:
            trees._rollback_quietly(db)
            # AN EXCEPTION IS NOT PROOF NOTHING LANDED. The witness is the
            # engine's own answer, for the reason the membership writer gives.
            if witness.landed:
                _record_commit(record, written, cfg)
            raise
        # RECORDED THE INSTANT THE COMMIT RETURNS.
        _record_commit(record, written, cfg)
        convergence.record_fingerprint(cfg, db)

        after = _columns(db, content_ids)
        names = _genre_names(db)
        session_id = record.session_id

    # The process wide collection cache holds the words as they were.
    collection.reset_cache()
    wrong, moved = judge(writes, before, after, names)
    return Written(
        session_id=session_id,
        written=written,
        read_back=len(writes) - len(wrong),
        wrong=wrong,
        moved=moved,
    )


def assert_read_back(written: Written) -> None:
    """Refuse when the database does not say what the plan said it would.

    A COLUMN THAT MOVED IS REPORTED AS THE GUARD'S DEFECT, because the guard
    holds that before the commit and reaching here means it did not. A genre
    that reads wrong is this module's. Either way the write is durable, so the
    refusal names the session whose capture undoes it.
    """
    if not written.wrong and not written.moved:
        return
    undo = (
        f"the write is durable; restore session {written.session_id} to undo it",
    )
    if written.moved:
        raise refuse(
            "whitelist-violation",
            "a row written for its genre has another column changed after the "
            "commit, which the guard should have refused before it: "
            + "; ".join(written.moved),
            remedy=Remedy.REPORT_DEFECT,
            steps=undo,
            origin=_ORIGIN,
            detail={"moved": list(written.moved), "session": written.session_id},
        )
    raise refuse(
        "internal-error",
        f"{len(written.wrong)} of {written.written} row(s) written do not read "
        f"back as their file's genre: " + "; ".join(written.wrong),
        remedy=Remedy.REPORT_DEFECT,
        steps=undo,
        origin=_ORIGIN,
        detail={"wrong": list(written.wrong), "session": written.session_id},
    )


__all__ = [
    "AGREE",
    "CHANGE_KEY",
    "FILE_BLANK",
    "FILE_MISSING",
    "FILE_TOO_COARSE",
    "FILE_UNREADABLE",
    "GENRE_UNKNOWN",
    "LEAVE",
    "NAMED_PAIRS",
    "NO_PATH",
    "OUTCOMES",
    "PATH_UNMAPPED",
    "UNREAD",
    "WORKFLOW",
    "WRITE",
    "Item",
    "RowsPlan",
    "Written",
    "apply_rows",
    "assert_read_back",
    "assert_rows_as_planned",
    "judge",
    "plan_rows",
]
