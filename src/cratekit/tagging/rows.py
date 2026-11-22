"""Write a row's genre from its file where the two disagree (R-816).

The source system wrote a specific genre onto each file and never reloaded the
rows, and the only other repair was a reload in rekordbox, which overwrites
every tag field.

WHAT IT WRITES IS ``GenreID`` AND NOTHING ELSE, planned by
:func:`cratekit.write.metadata.plan_genre_retag` and applied by
:func:`cratekit.tagging.retag.apply_library` under the ``RETAG_GENRE`` policy.
Every written row is read again from SQL after the commit: its genre must be
the file's word, and no column but the genre and the binding's bookkeeping may
have moved, so a beat grid, tempo or BPM moving refuses by name. NOTHING HERE
WRITES A FILE, and a genre lookup row is linked and never created.

EVERY DISAGREEMENT IS READ AS THE ROW LAGGING ITS FILE, except a row a person
holds out, a too coarse file word against a specific row word, a file holding
more than one genre, and a word with no lookup row: each is listed with its
reason and left. EVERY LIVE ROW LANDS IN EXACTLY ONE OUTCOME, zero filled, and
an unreadable file is counted apart from a blank one. The row's word is read
as adoption reads it, :func:`cratekit.adopt.collection.genre_of`.

``plan_rows`` AND ``apply_rows`` MEAN SOMETHING ELSE IN
``cratekit.intake.native``, where a row is one the landing adds; neither module
imports the other.

Layer: modules. It opens no database of its own and names no verb.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.adopt import collection
from cratekit.adopt import scan as adopt_scan
from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    locations,
    rb_writer,
    session,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import retag
from cratekit.write import metadata, row_defaults, trees

#: The name a session record carries for this write.
WORKFLOW = "tag-rows"

#: What the write is filed under in a session record's change summary, a stable
#: identifier for the reason ``cratekit.write.metadata_cli.CHANGE_KEY`` gives.
CHANGE_KEY = "content.genre"

#: The outcomes, in the order a summary lists them.
AGREE = "agree"
WRITE = "write"
HELD_OUT = "held-out"
FILE_TOO_COARSE = "file-too-coarse"
FILE_MULTI_VALUED = "file-multi-valued"
GENRE_UNKNOWN = "genre-unknown"
FILE_BLANK = "file-blank"
FILE_UNREADABLE = "file-unreadable"
FILE_ONLINE_ONLY = "file-online-only"
FILE_MISSING = "file-missing"
PATH_UNMAPPED = "path-unmapped"
NO_PATH = "no-path"

OUTCOMES: tuple[str, ...] = (
    AGREE,
    WRITE,
    HELD_OUT,
    FILE_TOO_COARSE,
    FILE_MULTI_VALUED,
    GENRE_UNKNOWN,
    FILE_BLANK,
    FILE_UNREADABLE,
    FILE_ONLINE_ONLY,
    FILE_MISSING,
    PATH_UNMAPPED,
    NO_PATH,
)

#: The outcomes of a row that differs from its file and is left, each an item.
LEFT: tuple[str, ...] = (HELD_OUT, FILE_TOO_COARSE, FILE_MULTI_VALUED, GENRE_UNKNOWN)

#: The outcomes in which the file's genre was never learned, named apart.
UNREAD: tuple[str, ...] = (
    FILE_UNREADABLE,
    FILE_ONLINE_ONLY,
    FILE_MISSING,
    PATH_UNMAPPED,
    NO_PATH,
)

#: What the census's answers about a row's file count as; a new one reads as
#: unreadable until named.
_PROBED: Mapping[adopt_scan.Readability, str] = MappingProxyType(
    {
        adopt_scan.Readability.UNMAPPED: PATH_UNMAPPED,
        adopt_scan.Readability.MISSING: FILE_MISSING,
        adopt_scan.Readability.UNREADABLE: FILE_UNREADABLE,
        adopt_scan.Readability.ONLINE_ONLY: FILE_ONLINE_ONLY,
        adopt_scan.Readability.NOT_A_PATH: NO_PATH,
    }
)

#: What an item whose row is not written says it does.
LEAVE = "leave"

#: How many word pairs a summary names.
NAMED_PAIRS = 5

_ORIGIN = ("tagging", "rows")


@dataclass(frozen=True, slots=True)
class Item:
    """One row whose word differs from a non blank word on its file.

    ``action`` is :data:`WRITE` or :data:`LEAVE`; ``reason`` is a left row's
    outcome, and ``genre_id`` the lookup row a write links.
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


class Tallied:
    """What a plan of items and zero filled outcome counts answers, here and in
    :class:`cratekit.tagging.suggest.SuggestPlan`."""

    __slots__ = ()

    @property
    def writes(self) -> tuple[Any, ...]:
        return tuple(item for item in self.items if item.action == WRITE)

    @property
    def rows(self) -> int:
        """Every live row the walk counted."""
        return sum(self.counts.values())

    @property
    def unread(self) -> int:
        """Rows whose file's genre was never learned."""
        return sum(self.counts[name] for name in UNREAD)


@dataclass(frozen=True, slots=True)
class RowsPlan(Tallied):
    """Every differing row, the count of every outcome, and the write itself."""

    items: tuple[Item, ...]
    counts: Mapping[str, int]
    changes: metadata.Plan
    #: ``--leave`` identifiers naming no differing row, shown and digested, since
    #: a mistyped one is a row the person meant to hold and the plan writes.
    leave_unmatched: tuple[str, ...] = ()

    def unknown_words(self) -> list[tuple[str, int]]:
        """The file words with no lookup row, each with its rows, largest first."""
        seen = Counter(item.file for item in self.items if item.reason == GENRE_UNKNOWN)
        return sorted(seen.items(), key=lambda entry: (-entry[1], entry[0]))

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to: the items and the counts and
        NOTHING THAT NAMES A COPY, no path and no time, so a rehearsal on a copy
        digests equal to the live plan."""
        return digest_of(
            {
                "kind": WORKFLOW,
                "items": [item.digested() for item in self.items],
                "counts": dict(self.counts),
                "leave_unmatched": list(self.leave_unmatched),
            }
        )

    def pairs(self, limit: int = NAMED_PAIRS) -> list[dict[str, Any]]:
        """The most common (row word, file word) pairs among the writes."""
        seen = Counter((item.row, item.file) for item in self.writes)
        ordered = sorted(seen.items(), key=lambda entry: (-entry[1], entry[0]))
        return [{"row": row, "file": file, "rows": rows} for (row, file), rows in ordered[:limit]]


@dataclass(frozen=True, slots=True)
class Written(row_defaults.RowsWritten):
    """What one apply did, and what the database says about it afterwards.

    ``wrong`` names a written row whose genre does not read back as its file's,
    ``moved`` one with another column changed; :func:`assert_read_back` refuses
    over either.
    """


def _no_energy(path: Path) -> int | None:
    """The energy reader the census is handed: this walk does not route, so it
    opens nothing."""
    del path
    return None


def scanned(
    cfg: config.Config,
    mapped: Mapping[str, Any],
    declared: taxonomy.Taxonomy,
    probe: Callable[[Path], adopt_scan.Readability],
) -> Iterable[adopt_scan.ScannedTrack]:
    """Adoption's census over the mapped rows, the walk ``tag rows``, ``tag
    suggest`` and ``tag backlog`` share, its probe handed through."""
    return adopt_scan.scan_rows(
        collection.collection_rows(mapped.values()),
        declared,
        root=Path(cfg.library.root),
        prefix_map=locations.prefix_rules(cfg.resolved_prefix_map()),
        probe=probe,
        energy_reader=_no_energy,
    )


def _file_word(path: Path) -> tuple[str, str]:
    """The file's genre, or why it has none to give. Answers (word, outcome).

    THE FIRST NON EMPTY VALUE, ON EVERY CONTAINER: the checked reader answers
    ID3's values joined on a null byte, so that text is split, as the other
    containers already answer their first value.
    """
    try:
        text = tags.read_tags_checked(path, ("genre",))["genre"] or ""
    except tags.TagReadFailed:
        return "", FILE_UNREADABLE
    word = next((part.strip() for part in text.split("\x00") if part.strip()), "")
    return word, ("" if word else FILE_BLANK)


def _file_words(path: Path) -> tuple[str, ...]:
    """Every genre value the file holds, when it holds more than one, else empty.

    :func:`_file_word` answers the first value, so a row about to be written has
    its file asked again, and one holding several is left. Only differing rows
    pay this second open.
    """
    values = tags.read_tag_values(path, "genre") or ()
    words = tuple(word for word in (value.strip() for value in values) if word)
    return words if len(words) > 1 else ()


def _protected(declared: taxonomy.Taxonomy, row_word: str, file_word: str) -> bool:
    """A too coarse file word does not replace a specific (non blank, not too
    coarse) word on the row; a blank or catch all row is written."""
    return (
        declared.is_too_coarse_as_source(file_word)
        and bool(row_word)
        and not declared.is_too_coarse_as_source(row_word)
    )


def plan_rows(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    *,
    leave: Iterable[str] = (),
    probe: Callable[[Path], adopt_scan.Readability] = adopt_scan.probe_readability,
) -> RowsPlan:
    """Walk the collection once and sort every live row into one outcome.

    THE WALK IS ADOPTION'S CENSUS, :func:`cratekit.adopt.scan.scan_rows`, whose
    probe is total and reads no bytes: a directory this account cannot enter is
    counted, an evicted file is ``file-online-only`` and never opened, a
    tombstone is skipped uncounted, and an unmounted volume is ``file-missing``.
    ``probe`` is the census's own parameter, handed through.

    ``leave`` NAMES ROWS A PERSON HOLDS OUT, for a genre set by hand, since the
    gate is apply or abort over the whole plan; an identifier naming no
    differing row is carried, shown and digested. A differing row is asked in
    order whether it is held, whether its file's word is too coarse, whether its
    file holds several genres, and whether the word has a lookup row.

    Items are ordered by content identifier so the digest is stable. Nothing is
    set on the handle and only values are returned, so it may be a read handle
    closed before the gate.
    """
    held_out = frozenset(str(content_id) for content_id in leave)
    counts = dict.fromkeys(OUTCOMES, 0)
    mapped = {str(row.ID): row for row in db.get_content()}
    differing: dict[str, tuple[Any, str, str, str]] = {}
    items: list[Item] = []

    census = scanned(cfg, mapped, declared, probe)
    for track in census:
        content_id = track.content_id
        if track.readability is not adopt_scan.Readability.READABLE or track.path is None:
            counts[_PROBED.get(track.readability, FILE_UNREADABLE)] += 1
            continue
        path = Path(track.path)
        file_word, outcome = _file_word(path)
        if outcome:
            counts[outcome] += 1
            continue
        row_word = track.genre.strip()
        if row_word == file_word:
            counts[AGREE] += 1
            continue
        reason = ""
        if content_id in held_out:
            reason = HELD_OUT
        elif _protected(declared, row_word, file_word):
            reason = FILE_TOO_COARSE
        else:
            several = _file_words(path)
            if several:
                reason, file_word = FILE_MULTI_VALUED, "; ".join(several)
        if reason:
            counts[reason] += 1
            items.append(Item(content_id, str(path), row_word, file_word, LEAVE, reason=reason))
            continue
        differing[content_id] = (mapped[content_id], str(path), row_word, file_word)

    changes = metadata.plan_genre_retag(
        [entry[0] for entry in differing.values()],
        {content_id: entry[3] for content_id, entry in differing.items()},
        db=db,
    )
    linked = {change.content_id: str(change.new) for change in changes.changes}

    for content_id, (_row, path, row_word, file_word) in differing.items():
        genre_id = linked.get(content_id)
        if genre_id is None:
            counts[GENRE_UNKNOWN] += 1
            items.append(Item(content_id, path, row_word, file_word, LEAVE, reason=GENRE_UNKNOWN))
            continue
        counts[WRITE] += 1
        items.append(Item(content_id, path, row_word, file_word, WRITE, genre_id=genre_id))
    items.sort(key=lambda item: item.content_id)
    listed = {item.content_id for item in items}
    return RowsPlan(
        items=tuple(items),
        counts=MappingProxyType(counts),
        changes=changes,
        leave_unmatched=tuple(sorted(held_out - listed)),
    )


def narrowed(plan: RowsPlan, keep: Iterable[str]) -> RowsPlan:
    """The plan with every write not named in ``keep`` held out, as ``--leave`` holds it.

    For ``tag campaign``, which writes only the rows the backlog named (U294). A
    held write becomes a :data:`HELD_OUT` item and its change leaves the write,
    so :func:`apply_rows` cannot reach it. Pure.
    """
    kept = frozenset(str(content_id) for content_id in keep)
    held = {item.content_id for item in plan.writes if item.content_id not in kept}
    if not held:
        return plan
    items = tuple(
        Item(item.content_id, item.path, item.row, item.file, LEAVE, reason=HELD_OUT)
        if item.content_id in held
        else item
        for item in plan.items
    )
    counts = dict(plan.counts)
    counts[WRITE] -= len(held)
    counts[HELD_OUT] += len(held)
    changes = metadata.Plan(
        owner=plan.changes.owner,
        changes=tuple(change for change in plan.changes.changes if change.content_id not in held),
        skipped=plan.changes.skipped,
    )
    return RowsPlan(
        items=items,
        counts=MappingProxyType(counts),
        changes=changes,
        leave_unmatched=plan.leave_unmatched,
    )


def _genre_names(db: Any) -> dict[str, str]:
    """Every genre lookup row's name by identifier, from SQL."""
    from sqlalchemy import text

    result = db.session.execute(text("SELECT ID, Name FROM djmdGenre"))
    return {str(row[0]): str(row[1] or "").strip() for row in result}


def judge(
    writes: Sequence[Item],
    before: Mapping[str, Mapping[str, Any]],
    after: Mapping[str, Mapping[str, Any]],
    names: Mapping[str, str],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """What the read back found wrong. Answers (wrong, moved). Pure.

    ``wrong`` is a written row not now carrying its file's word, or not found;
    ``moved`` one with a column changed other than the genre and
    :data:`cratekit.core.rb_writer.BOOKKEEPING_COLUMNS`.
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
    """Refuse, writing nothing, when a row to be written no longer carries the
    genre the plan read or is no longer live: the plan was made on another handle.

    ``mapped`` is the write handle's rows; the tombstone is read through
    :func:`cratekit.write.trees.soft_delete_marker`, which refuses a row that
    cannot say.
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
            f"not as the plan read them, so nothing was written: " + row_defaults.named(moved),
            steps=("run the verb again and approve the plan as it is now",),
            origin=_ORIGIN,
            detail={"moved": moved},
        )


def apply_rows(
    cfg: config.Config,
    db: Any,
    plan: RowsPlan,
    *,
    analysis_roots: Iterable[Path | str],
    workflow: str = WORKFLOW,
    narrow: Callable[[RowsPlan], RowsPlan] | None = None,
) -> Written:
    """Write the plan's genres, commit behind the guard, and read them back.

    THE SESSION SPINE IS CALLED, NOT REBUILT: the gates with a record, the
    capture, the analysis watch, the commit witness and the guarded commit. The
    rows are checked against the plan before it is entered, and an out of band
    restore is looked for first, since this write records a fingerprint.

    NOTHING IS READ BETWEEN THE FIRST SET AND THE COMMIT, which would flush the
    work before the whitelist judged it. THE READ BACK IS JUDGED BY THE CALLER,
    :func:`assert_read_back`, after the session closed, so a refusal leaves the
    capture as the undo. ``analysis_roots`` has no default: a watch over nothing
    reports every session clean. ``workflow`` is the name the record carries.

    ``narrow`` IS CALLED INSIDE THE SESSION, after the capture and before the
    first set, and answers the part of the plan to write; ``tag suggest`` writes
    its files there, behind the library lock and the volume check. It reads no
    row.
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
    mapped = row_defaults.read_mapped(db, content_ids)
    assert_rows_as_planned(plan, mapped)
    # THE EVIDENCE IS READ BEFORE IT IS REPLACED: a fingerprint recorded over a
    # restored database would leave the trees it emptied unmarked. It marks and
    # never refuses.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    with (
        session.assert_gates(
            cfg, workflow=workflow, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record, capture = trees.attached_capture(gates, cfg, db)

        if narrow is not None:
            plan = narrow(plan)
            writes = plan.writes
            content_ids = [item.content_id for item in writes]
        before = row_defaults.read_columns(db, content_ids)
        written = 0
        try:
            report = retag.apply_library(retag.LibraryPlan(plan=plan.changes), mapped)
            written = len(report.written)
            rb_writer.commit_guarded(db)
        except BaseException:
            trees.rollback_quietly(db)
            # AN EXCEPTION IS NOT PROOF NOTHING LANDED. The witness is the
            # engine's own answer, for the reason the membership writer gives.
            if witness.landed:
                row_defaults.record_commit(record, CHANGE_KEY, written, cfg)
            raise
        # RECORDED THE INSTANT THE COMMIT RETURNS.
        row_defaults.record_commit(record, CHANGE_KEY, written, cfg)
        convergence.record_fingerprint(cfg, db)

        after = row_defaults.read_columns(db, content_ids)
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

    A moved column is the guard's defect, a wrong genre this module's; the write
    is durable either way, so the refusal names the session that undoes it.
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
            + row_defaults.named(written.moved),
            remedy=Remedy.REPORT_DEFECT,
            steps=undo,
            origin=_ORIGIN,
            detail={"moved": list(written.moved), "session": written.session_id},
        )
    raise refuse(
        "internal-error",
        f"{len(written.wrong)} of {written.written} row(s) written do not read "
        f"back as their file's genre: " + row_defaults.named(written.wrong),
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
    "FILE_MULTI_VALUED",
    "FILE_ONLINE_ONLY",
    "FILE_TOO_COARSE",
    "FILE_UNREADABLE",
    "GENRE_UNKNOWN",
    "HELD_OUT",
    "LEAVE",
    "LEFT",
    "NAMED_PAIRS",
    "NO_PATH",
    "OUTCOMES",
    "PATH_UNMAPPED",
    "UNREAD",
    "WORKFLOW",
    "WRITE",
    "Item",
    "RowsPlan",
    "Tallied",
    "Written",
    "apply_rows",
    "assert_read_back",
    "assert_rows_as_planned",
    "judge",
    "narrowed",
    "plan_rows",
    "scanned",
]
