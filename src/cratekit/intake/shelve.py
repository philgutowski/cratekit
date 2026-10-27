"""An imported batch folder moves into the processed tree, and its rows follow (U154).

THE HAND CONVENTION, MADE A VERB. The author kept every track under
``Music/Processed_Tracks/<year>/<MM_DD_YY subject>``, one folder per download,
and moved each folder there himself once rekordbox had imported and analysed
it. The landing puts a batch at ``Music/<batch>`` and nothing moved it on, so
the music folder filled with batch folders beside the tree they belonged in.

WHAT A SHELVE IS. One folder rename on the library's filesystem, and one
``FolderPath`` rewrite on every content row the folder's files hold, in one
guarded commit. rekordbox keys a row's file by that column, so a folder moved
without the rewrite leaves every row pointing at nothing, and a rewrite without
the move points every row at nothing yet. Both happen here or neither does:

* the folder is renamed first, one ``os.rename`` on one filesystem, then the
  rows are written and the commit is asked. A commit that fails renames the
  folder back and says so. A rename that fails writes nothing;
* the rows' other columns are left alone. ``FileNameL`` is the file's own name
  and does not change. The file id is the inode (U115), which a rename on one
  filesystem keeps. ``AnalysisDataPath`` is relative to the share and keyed by
  UUID (R-14), so the grids stay where they are. All three are read back after
  the commit rather than assumed.

THE FOLDER NAME IS THE HAND CONVENTION'S. ``MM_DD_YY``, zero padded, a space,
the subject. The date is the leading ``YYYY-MM-DD`` of the batch name, which is
the landing's default shape since U110, or the date inside a run identifier
shaped name, which is what a batch was called before U110. The subject is what
follows the date, or ``Downloads`` when nothing does, or the one the person
gave. The year folder is the date's year. A name that fits neither shape is
reported and skipped, never guessed.

A BATCH IS SHELVED WHOLE OR NOT AT ALL. Every audio file in the folder has to
resolve to exactly one active content row, the way the landing matches a file
against the collection. A file with no row is an import that has not happened,
or a row under a prefix rule the configuration does not carry, and moving the
folder would strand it either way. The batch is left and the plan says which
file and why. The rest of a ``--all`` plan still goes.

NOTHING UNDER THE PROCESSED TREE IS EVER MOVED OR RENAMED BY THIS MODULE. It
adds a folder; it reads what is there only to choose a free name.

Layer: modules.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Sequence

from cratekit.cli.output import digest_of
from cratekit.core import config, locations, rb_writer, session, snapshot
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.intake import batch_name, landing, native
from cratekit.write import routing_pass, trees

#: The session workflow a shelve records under, and the one the landing's name
#: rule reads back to keep a shelved batch's name taken.
WORKFLOW = "shelve"
#: The record key naming every batch a shelve moved, ``[{batch, to, rows}]``.
SHELVED_KEY = "shelved_batches"

#: The landing's default name, ``2026-10-08 Tidal playlists and Favorites``,
#: and the two other separators a person has typed after the date.
_DATED = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:[ _-]+(?P<subject>.+))?$")
#: A run identifier, what a batch was named before U110.
_RUN_ID = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T\d{6}Z-[0-9a-f]{4}$")

_ORIGIN = ("intake.shelve",)

#: Every column read back after the commit beside the one written, so the
#: report says the rename moved nothing it should not have.
_KEPT_COLUMNS = ("FileNameL", rb_writer.FILE_ID_COLUMN, "AnalysisDataPath")


# ---------------------------------------------------------------------------
# Names
# ---------------------------------------------------------------------------


def parse_name(batch: str) -> tuple[date, str] | None:
    """The date a batch name carries and the words after it, or None for neither shape.

    The subject is empty when the name is the date alone or a run identifier,
    and :func:`filed_name` gives it the landing's own word for a batch that
    says nothing about its source.
    """
    run = _RUN_ID.match(batch)
    if run is not None:
        year, month, day = (int(group) for group in run.groups()[:3])
        try:
            return date(year, month, day), ""
        except ValueError:
            return None
    dated = _DATED.match(batch)
    if dated is None:
        return None
    year, month, day = (int(group) for group in dated.groups()[:3])
    try:
        when = date(year, month, day)
    except ValueError:
        return None
    return when, " ".join((dated.group("subject") or "").split())


def filed_name(when: date, subject: str) -> str:
    """``MM_DD_YY subject``, the hand convention, zero padded so a listing sorts."""
    return f"{when:%m_%d_%y} {subject}"


def processed_root(cfg: config.Config) -> Path:
    """Where filed batches live, ``root / music_dir / processed_dir``."""
    return Path(cfg.library.root) / cfg.library.music_dir / cfg.library.processed_dir


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ShelfRow:
    """One file of a batch, the row that holds it, and the path the row will carry."""

    content_id: str
    file_name: str
    #: The row's ``FolderPath`` now, as stored, and the one the plan writes.
    recorded: str
    folder_path: str


@dataclass(frozen=True, slots=True)
class ShelfBatch:
    """One batch folder the plan moves, and every row that follows it."""

    batch: str
    source: Path
    target: Path
    #: ``target`` as rekordbox stores a path under it, under the base drive
    #: and NFC, so the confinement check reads rows the way they are written.
    stored_target: str
    filed_on: date
    subject: str
    rows: tuple[ShelfRow, ...]


@dataclass(frozen=True, slots=True)
class Skipped:
    """One batch the plan leaves where it is, and the sentence that says why."""

    batch: str
    why: str


@dataclass(frozen=True, slots=True)
class ShelfPlan:
    batches: tuple[ShelfBatch, ...]
    skipped: tuple[Skipped, ...]
    #: Over every batch, its rows and the folder's own listing, so an answer
    #: given for one set of files or one collection is stale for another.
    digest: str

    def rows(self) -> int:
        return sum(len(one.rows) for one in self.batches)


def _candidates(cfg: config.Config) -> list[str]:
    """Every folder directly under the music folder that could be a batch, by name."""
    music = Path(cfg.library.root) / cfg.library.music_dir
    reserved = {cfg.library.processed_dir, cfg.library.sets_dir}
    names: list[str] = []
    for entry in sorted(music.iterdir(), key=lambda p: p.name):
        if entry.name.startswith(".") or entry.name in reserved:
            continue
        if entry.is_dir() and not entry.is_symlink():
            names.append(entry.name)
    return names


def _folder_of(cfg: config.Config, batch: str) -> Path:
    """The batch's folder under the music folder, or the refusal naming what was given."""
    if not batch or batch in {".", ".."} or os.sep in batch or (os.altsep and os.altsep in batch):
        raise refuse(
            "intake-list-unusable",
            f"{batch!r} is not the name of a folder directly under the music folder; "
            f"a batch is named by its folder's name alone",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"batch": batch},
        )
    if batch in {cfg.library.processed_dir, cfg.library.sets_dir}:
        raise refuse(
            "intake-list-unusable",
            f"{batch!r} is the library's own folder, not a batch, so nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"batch": batch},
        )
    folder = landing.target_dir(cfg, batch)
    if not folder.is_dir() or folder.is_symlink():
        raise refuse(
            "intake-list-unusable",
            f"{folder} is not a folder under the music folder, so there is nothing to shelve",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"batch": batch, "folder": str(folder)},
        )
    return folder


def _free_target(root: Path, name: str, planned: set[Path]) -> Path:
    """``root / name``, or `` 2``, `` 3`` and on, the first neither disk nor this plan holds."""
    candidate, count = root / name, 1
    while os.path.lexists(candidate) or candidate in planned:
        count += 1
        candidate = root / f"{name} {count}"
    return candidate


def _why_unmatched(file: Path, match: trees.RowMatch) -> str:
    if match.outcome is trees.MatchOutcome.UNRESOLVED:
        return (
            f"{file.name} resolves nowhere under the library root or its prefix rules, "
            f"so the collection could not be asked whether it holds the file"
        )
    if match.outcome is trees.MatchOutcome.AMBIGUOUS:
        return (
            f"{file.name} is held by {len(match.content_ids)} active rows "
            f"({', '.join(match.content_ids)}), and a batch with a duplicate row is "
            f"not moved until one of them is removed"
        )
    return (
        f"{file.name} has no row in the collection, so the batch has not been imported, "
        f"or not wholly; import it and shelve it again"
    )


def plan(
    cfg: config.Config,
    db: Any,
    names: Sequence[str],
    *,
    subject: str | None = None,
    everything: bool = False,
) -> ShelfPlan:
    """What a shelve of ``names``, or of every batch folder, would move and write.

    A NAMED BATCH THAT CANNOT BE SHELVED REFUSES, since the person asked for
    that one and a plan of nothing would ask a gate over nothing. Under
    ``everything`` a batch that cannot be shelved is skipped with its reason
    and the rest of the plan goes.

    ``subject`` replaces the words the batch name carries, and is accepted for
    one named batch only, which the shell holds to.
    """
    wanted = _candidates(cfg) if everything else list(names)
    base_drive, current_drive = rb_writer.recorded_db_drives(db)
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    content = list(routing_pass.content_rows(db))
    recorded = {row.content_id: row.recorded for row in content}
    index = trees.index_active_rows(content, root=cfg.library.root, prefix_map=prefix_map)
    root = processed_root(cfg)

    batches: list[ShelfBatch] = []
    skipped: list[Skipped] = []
    planned: set[Path] = set()

    def leave(batch: str, why: str) -> None:
        if everything:
            skipped.append(Skipped(batch=batch, why=why))
            return
        raise refuse(
            "intake-list-unusable",
            f"{batch!r} was not shelved: {why}; nothing was moved",
            origin=_ORIGIN,
            detail={"batch": batch},
        )

    for batch in wanted:
        folder = _folder_of(cfg, batch)
        parsed = parse_name(batch)
        if parsed is None:
            leave(
                batch,
                "its name carries no date in the landing's shape or a run identifier's, "
                "so no folder name could be composed for it",
            )
            continue
        when, words = parsed
        if any(entry.is_dir() for entry in folder.iterdir()):
            leave(batch, "the folder holds a subfolder, and a batch is one flat folder of files")
            continue
        files = landing.listing(folder)
        if not files:
            leave(batch, "the folder holds no audio file")
            continue
        matches = trees.match_indexed_rows(
            files, index, root=cfg.library.root, prefix_map=prefix_map
        )
        unmatched = next(
            (
                (file, match)
                for file, match in zip(files, matches)
                if match.outcome is not trees.MatchOutcome.MATCHED or match.content_id is None
            ),
            None,
        )
        if unmatched is not None:
            leave(batch, _why_unmatched(*unmatched))
            continue
        said = (subject if subject is not None else words).strip() or batch_name.DOWNLOADS
        target = _free_target(root / f"{when.year}", filed_name(when, said), planned)
        planned.add(target)
        rows = tuple(
            ShelfRow(
                content_id=str(match.content_id),
                file_name=file.name,
                recorded=recorded.get(str(match.content_id), ""),
                folder_path=native.stored_folder_path(
                    target / file.name, base_drive=base_drive, current_drive=current_drive
                ),
            )
            for file, match in zip(files, matches)
        )
        batches.append(
            ShelfBatch(
                batch=batch,
                source=folder,
                target=target,
                stored_target=native.stored_folder_path(
                    target, base_drive=base_drive, current_drive=current_drive
                ),
                filed_on=when,
                subject=said,
                rows=rows,
            )
        )
    return ShelfPlan(
        batches=tuple(batches),
        skipped=tuple(skipped),
        digest=digest_of(_identity(batches, skipped)),
    )


def _identity(batches: Iterable[ShelfBatch], skipped: Iterable[Skipped]) -> dict[str, Any]:
    return {
        "kind": "shelve",
        "batches": [
            {
                "batch": one.batch,
                "from": str(one.source),
                "to": str(one.target),
                "rows": [
                    [row.content_id, row.file_name, row.recorded, row.folder_path]
                    for row in one.rows
                ],
            }
            for one in batches
        ],
        "skipped": [[one.batch, one.why] for one in skipped],
    }


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ReadBack:
    """One row after the commit, from SQL."""

    content_id: str
    folder_path: str
    kept: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Shelved:
    batches: tuple[ShelfBatch, ...]
    rows: tuple[ReadBack, ...]
    session_id: str


def _kept(db: Any, content_ids: Sequence[str]) -> dict[str, tuple[Any, ...]]:
    """The columns a shelve must not change, per row, from SQL."""
    from sqlalchemy import text

    out: dict[str, tuple[Any, ...]] = {}
    selected = ", ".join(_KEPT_COLUMNS)
    for content_id in content_ids:
        row = db.session.execute(
            text(f"SELECT {selected} FROM {rb_writer.CONTENT_TABLE} WHERE ID = :id"),
            {"id": content_id},
        ).first()
        out[content_id] = tuple(row) if row is not None else ()
    return out


def _assert_confined(db: Any, plan: ShelfPlan) -> None:
    """Refuse, before the commit, a path change on any row the plan did not name.

    FROM SQL, as the node guard is and for its reason: the mapped objects say
    what the writer intended, and the pending work is flushed deliberately so
    the second reading sees it and a violation still rolls back. Every row now
    stored under a target folder has to be one the plan put there, and every
    planned row has to carry exactly its planned path.
    """
    from sqlalchemy import text

    db.session.flush()
    violations: list[str] = []
    for one in plan.batches:
        planned = {row.content_id: row.folder_path for row in one.rows}
        # EVERY ROW UNDER THE TARGET, TOMBSTONES INCLUDED. The target folder is
        # new, so nothing has any business being stored under it but the rows
        # this plan put there, and a tombstone there is as unplanned as a row.
        under = db.session.execute(
            text(
                f"SELECT ID, {rb_writer.FOLDER_PATH_COLUMN} FROM {rb_writer.CONTENT_TABLE} "
                f"WHERE {rb_writer.FOLDER_PATH_COLUMN} LIKE :prefix ESCAPE '\\'"
            ),
            {"prefix": _like_prefix(one.stored_target)},
        ).all()
        found = {str(row[0]): str(row[1] or "") for row in under}
        for content_id, path in found.items():
            if content_id not in planned:
                violations.append(
                    f"row {content_id} is stored under {one.target} and the plan did not put it there"
                )
            elif path != planned[content_id]:
                violations.append(
                    f"row {content_id} carries {path!r}, not the planned {planned[content_id]!r}"
                )
        for content_id in planned:
            if content_id not in found:
                violations.append(
                    f"row {content_id} was planned under {one.target} and is not stored there"
                )
    if violations:
        db.rollback()
        raise refuse(
            "whitelist-violation",
            "the shelve reached a row it did not plan, or missed one it did, read from "
            "SQL before the commit:\n  - " + "\n  - ".join(violations),
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"violations": violations},
        )


def _like_prefix(stored_target: str) -> str:
    """A LIKE pattern for every path directly under the stored folder, every wildcard escaped."""
    escaped = stored_target.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return escaped + os.sep + "%"


def _rename_back(moved: list[tuple[Path, Path]]) -> list[str]:
    """Undo every rename, newest first. Answers what could not be put back."""
    failed: list[str] = []
    for source, target in reversed(moved):
        try:
            os.rename(target, source)
        except OSError as exc:
            failed.append(f"{target} could not be renamed back to {source}: {exc}")
    return failed


def apply(
    cfg: config.Config, db: Any, plan: ShelfPlan, *, analysis_roots: Iterable[Path | str]
) -> Shelved:
    """Move every planned folder and write every planned row, in one commit.

    THE SESSION SPINE IS THE LANDING'S: the gates in their argued order with a
    record kept, a capture the commit happens behind, the analysis watch over
    the roots named, the commit witness, and the guarded commit with the path
    policy registered for this commit alone.

    THE RENAMES COME FIRST AND ARE UNDONE ON ANY FAILURE PAST THEM. The commit
    is all or nothing in the database. The filesystem has no transaction, so a
    failure after a rename renames back, newest first, and a rename that will
    not go back is named in the refusal rather than left for a person to find.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    if not plan.batches:
        raise refuse(
            "intake-list-unusable",
            "the plan moves no batch, so there is nothing to apply",
            origin=_ORIGIN,
            detail={"skipped": [[one.batch, one.why] for one in plan.skipped]},
        )
    content_ids = [row.content_id for one in plan.batches for row in one.rows]
    moved: list[tuple[Path, Path]] = []
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)
        before = _kept(db, content_ids)
        try:
            for one in plan.batches:
                _assert_still_as_planned(db, one)
            for one in plan.batches:
                one.target.parent.mkdir(parents=True, exist_ok=True)
                os.rename(one.source, one.target)
                moved.append((one.source, one.target))
            for one in plan.batches:
                for row in one.rows:
                    content = db.get_content(ID=row.content_id)
                    setattr(content, rb_writer.FOLDER_PATH_COLUMN, row.folder_path)
            with rb_writer.field_policies_for_commit(rb_writer.SHELVE_POLICY):
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)
        except BaseException as exc:
            trees._rollback_quietly(db)
            if witness.landed:
                _record(record, plan, cfg)
                raise
            if not moved and isinstance(exc, CratekitError):
                # A refusal before the first rename, a stale plan or a row that
                # moved since, keeps its own words: nothing here changed.
                raise
            failed = _rename_back(moved)
            inner = exc.cause if isinstance(exc, CratekitError) else None
            put_back = [str(source) for source, _target in moved if str(source) not in failed]
            raise refuse(
                inner.reason if inner is not None else "internal-error",
                f"the collection could not be written "
                f"({inner.message if inner is not None else exc}); no row was changed, "
                + (
                    f"{len(put_back)} folder(s) renamed back to where they were"
                    if not failed
                    else f"and {len(failed)} folder(s) could not be renamed back: "
                    + "; ".join(failed)
                ),
                remedy=inner.remediation.remedy if inner is not None else Remedy.REPORT_DEFECT,
                steps=inner.remediation.steps if inner is not None else (),
                origin=_ORIGIN,
                detail={
                    "renamed_back": put_back,
                    "not_renamed_back": failed,
                    **(dict(inner.detail) if inner is not None else {}),
                },
                inner=inner,
            ) from exc
        _record(record, plan, cfg)
        read = _read_back(db, plan, before)
        session_id = record.session_id
    return Shelved(batches=plan.batches, rows=tuple(read), session_id=session_id)


def _assert_still_as_planned(db: Any, one: ShelfBatch) -> None:
    """Refuse a batch whose folder, target or rows moved since the plan was shown."""
    if not one.source.is_dir():
        raise refuse(
            "decision-stale",
            f"{one.source} is no longer a folder under the music folder, so the plan "
            f"that moved it is stale and nothing was moved",
            origin=_ORIGIN,
            detail={"batch": one.batch, "folder": str(one.source)},
        )
    if os.path.lexists(one.target):
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "
            f"was moved; run the shelve again and it takes the next free name",
            origin=_ORIGIN,
            detail={"batch": one.batch, "target": str(one.target)},
        )
    for row in one.rows:
        content = db.get_content(ID=row.content_id)
        if (
            content is None
            or str(getattr(content, rb_writer.FOLDER_PATH_COLUMN, "") or "") != row.recorded
        ):
            raise refuse(
                "decision-stale",
                f"row {row.content_id} for {row.file_name} no longer carries the path the "
                f"plan was made against, so nothing was moved",
                origin=_ORIGIN,
                detail={"batch": one.batch, "content_id": row.content_id},
            )


def _record(record: session.SessionRecord, plan: ShelfPlan, cfg: config.Config) -> None:
    """Name every batch moved on the record, and the rows under the content table."""
    record.detail[SHELVED_KEY] = [
        {"batch": one.batch, "to": str(one.target), "rows": len(one.rows)} for one in plan.batches
    ]
    session.record_commit(
        record,
        rb_writer.CONTENT_TABLE,
        session.ChangeSummary(
            (session.TreeChange(tree=rb_writer.CONTENT_TABLE, updated=plan.rows()),)
        ),
        cfg,
    )


def _read_back(db: Any, plan: ShelfPlan, before: dict[str, tuple[Any, ...]]) -> list[ReadBack]:
    """Every planned row after the commit, refusing one that did not take or lost a column."""
    from sqlalchemy import text

    out: list[ReadBack] = []
    after = _kept(db, [row.content_id for one in plan.batches for row in one.rows])
    for one in plan.batches:
        for row in one.rows:
            stored = db.session.execute(
                text(
                    f"SELECT {rb_writer.FOLDER_PATH_COLUMN} FROM {rb_writer.CONTENT_TABLE} "
                    f"WHERE ID = :id"
                ),
                {"id": row.content_id},
            ).scalar()
            if str(stored or "") != row.folder_path:
                raise refuse(
                    "internal-error",
                    f"row {row.content_id} was committed carrying {stored!r}, not the "
                    f"planned {row.folder_path!r}; the folder is at {one.target}",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=_ORIGIN,
                    detail={"content_id": row.content_id, "stored": str(stored or "")},
                )
            if before.get(row.content_id) != after.get(row.content_id):
                raise refuse(
                    "internal-error",
                    f"row {row.content_id} changed a column the shelve does not own: "
                    f"{dict(zip(_KEPT_COLUMNS, before.get(row.content_id, ())))} became "
                    f"{dict(zip(_KEPT_COLUMNS, after.get(row.content_id, ())))}",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=_ORIGIN,
                    detail={"content_id": row.content_id},
                )
            out.append(
                ReadBack(
                    content_id=row.content_id,
                    folder_path=str(stored or ""),
                    kept=dict(zip(_KEPT_COLUMNS, after.get(row.content_id, ()))),
                )
            )
    return out


__all__ = [
    "SHELVED_KEY",
    "WORKFLOW",
    "ReadBack",
    "ShelfBatch",
    "ShelfPlan",
    "ShelfRow",
    "Shelved",
    "Skipped",
    "apply",
    "filed_name",
    "parse_name",
    "plan",
    "processed_root",
]
