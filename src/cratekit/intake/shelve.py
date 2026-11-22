"""An imported batch folder moves into the processed tree, and its rows follow (U154).

The author's hand convention as a verb: ``<processed>/<year>/<MM_DD_YY subject>``.
ONE FOLDER RENAME AND ONE ``FolderPath`` REWRITE per row, in one guarded commit,
since rekordbox keys a row's file by that column and either half alone strands
every row; a commit that fails renames the folder back. The file id (an inode)
and ``AnalysisDataPath`` survive a rename on one filesystem and are read back.

The date leads the batch name or sits in a run identifier shaped name, and a
name of neither shape is skipped, never guessed. A BATCH IS SHELVED WHOLE OR
NOT AT ALL: every audio file must resolve to exactly one active row. Nothing
under the processed tree is moved; it is read only to choose a free name.

Layer: modules.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from cratekit.cli.output import digest_of
from cratekit.core import config, locations, rb_writer, session
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.intake import batch_name, landing, native, rotate
from cratekit.write import routing_pass, trees

#: The session workflow a shelve records under, and the one the landing's name
#: rule reads back to keep a shelved batch's name taken.
WORKFLOW = "shelve"
#: The record key naming every batch a shelve moved, ``[{batch, to, rows}]``.
SHELVED_KEY = "shelved_batches"

#: The landing's default name, and the two other separators a person has typed.
_DATED = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:[ _-]+(?P<subject>.+))?$")
#: A run identifier without its colons, a batch's name before U110; its tail
#: is four hex characters before U235 and sixteen since.
_RUN_ID = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")

_ORIGIN = ("intake.shelve",)

#: Every column read back after the commit beside the one written.
_KEPT_COLUMNS = ("FileNameL", rb_writer.FILE_ID_COLUMN, "AnalysisDataPath")


def parse_name(batch: str) -> tuple[date, str] | None:
    """The date a batch name carries and the words after it, or None for neither shape.

    The subject is empty for the date alone or a run identifier.
    """
    run = _RUN_ID.match(batch)
    if run is not None:
        matched, subject = run, ""
    else:
        matched = _DATED.match(batch)
        if matched is None:
            return None
        subject = " ".join((matched.group("subject") or "").split())
    year, month, day = (int(group) for group in matched.groups()[:3])
    try:
        return date(year, month, day), subject
    except ValueError:
        return None


def filed_name(when: date, subject: str) -> str:
    """``MM_DD_YY subject``, the hand convention, zero padded so a listing sorts."""
    return f"{when:%m_%d_%y} {subject}"


def processed_root(cfg: config.Config) -> Path:
    """Where filed batches live, ``root / music_dir / processed_dir``."""
    return Path(cfg.library.root) / cfg.library.music_dir / cfg.library.processed_dir


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
    #: ``target`` as rekordbox stores it, so the confinement check reads rows as written.
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
    #: Over every batch and its rows, so an answer for one set of files is stale for another.
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

    def unusable(message: str, **detail: str) -> Exception:
        return refuse(
            "intake-list-unusable",
            message,
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"batch": batch, **detail},
        )

    if not batch or batch in {".", ".."} or os.sep in batch or (os.altsep and os.altsep in batch):
        raise unusable(
            f"{batch!r} is not the name of a folder directly under the music folder; "
            f"a batch is named by its folder's name alone"
        )
    if batch in {cfg.library.processed_dir, cfg.library.sets_dir}:
        raise unusable(f"{batch!r} is the library's own folder, not a batch, so nothing was moved")
    folder = landing.target_dir(cfg, batch)
    if not folder.is_dir() or folder.is_symlink():
        raise unusable(
            f"{folder} is not a folder under the music folder, so there is nothing to shelve",
            folder=str(folder),
        )
    return folder


def _free_target(
    root: Path,
    name: str,
    planned: set[Path],
    *,
    stored_dirs: frozenset[str],
    spell: Callable[[Path], str],
) -> Path:
    """``root / name``, or `` 2``, `` 3`` and on, the first that disk, this plan and the collection all leave free.

    The collection is asked, in its stored spelling, since a folder moved away
    by hand leaves rows under its name that the confinement check would refuse.
    """
    candidate, count = root / name, 1
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:
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


def _speller(db: Any) -> Callable[[Path], str]:
    """A path as rekordbox stores one under this library's drives."""
    base_drive, current_drive = rb_writer.recorded_db_drives(db)

    return lambda path: native.stored_folder_path(
        path, base_drive=base_drive, current_drive=current_drive
    )


def _stored_dirs(recorded: Iterable[str]) -> frozenset[str]:
    """Every folder the collection's rows are stored under, compared as stored."""
    return frozenset(os.path.dirname(locations.norm_for_compare(path)) for path in recorded if path)


def filed_parts(batch: str, *, on: date) -> tuple[date, str]:
    """The date and the subject a landed batch is filed by, as :func:`landing_target` reads them."""
    parsed = parse_name(batch)
    when, words = parsed if parsed is not None else (on, " ".join(batch.split()))
    return when, words or batch_name.DOWNLOADS


def landing_target(cfg: config.Config, db: Any, batch: str, *, on: date) -> Path:
    """The folder a database native landing puts ``batch`` in, filed from the first commit (U164).

    THE SHELVE'S OWN RULE, so a landed batch is where a shelve would have put
    it; a name :func:`parse_name` cannot read is filed on ``on`` with the whole
    name as its subject. A batch landed into again by its own name goes back
    to its recorded folder while that folder is there. Asked on the plan's
    handle, so a continuation asks the same question of the same library.
    """
    again = batch_name.filed_folders(cfg).get(batch)
    if again is not None and os.path.isdir(again) and not os.path.islink(again):
        return Path(again)
    when, said = filed_parts(batch, on=on)
    spell = _speller(db)
    recorded = (row.recorded for row in routing_pass.content_rows(db))
    return _free_target(
        processed_root(cfg) / f"{when.year}",
        filed_name(when, said),
        set(),
        stored_dirs=_stored_dirs(recorded),
        spell=spell,
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

    A named batch that cannot be shelved refuses, since a person asked for it;
    under ``everything`` it is skipped with its reason. ``subject`` replaces
    the batch name's words, for one named batch only.
    """
    wanted = _candidates(cfg) if everything else list(dict.fromkeys(names))
    spell = _speller(db)
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    content = list(routing_pass.content_rows(db))
    recorded = {row.content_id: row.recorded for row in content}
    stored_dirs = _stored_dirs(recorded.values())
    index = trees.index_active_rows(content, root=cfg.library.root, prefix_map=prefix_map)
    root = processed_root(cfg)
    _assert_one_device(cfg, root)

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
        name = filed_name(when, said)
        target = _free_target(
            root / f"{when.year}", name, planned, stored_dirs=stored_dirs, spell=spell
        )
        planned.add(target)
        rows: list[ShelfRow] = []
        for file, match in zip(files, matches):
            cid = str(match.content_id)
            rows.append(ShelfRow(cid, file.name, recorded.get(cid, ""), spell(target / file.name)))
        batches.append(ShelfBatch(batch, folder, target, spell(target), when, said, tuple(rows)))
    return ShelfPlan(tuple(batches), tuple(skipped), digest_of(_identity(batches, skipped)))


def _assert_one_device(cfg: config.Config, root: Path) -> None:
    """Refuse a processed tree on another device, since a rename there would be a copy.

    Asked before any target is named, so it arrives with its remedy and not as
    an EXDEV wrapped as a defect.
    """
    music = Path(cfg.library.root) / cfg.library.music_dir
    here, there = landing._device_of(music), landing._device_of(root)
    if here is None or there is None or here != there:
        raise refuse(
            "intake-staging-refused",
            f"{root} is on a different device from the music folder at {music}, so a "
            f"shelve would be a copy and not a move; keep library.processed_dir on the "
            f"library's volume, nothing was moved",
            remedy=Remedy.FIX_CONFIG_VALUES,
            origin=_ORIGIN,
            detail={"music": str(music), "processed": str(root)},
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


def _select_rows(db: Any, content_ids: Sequence[str]) -> dict[str, tuple[str, tuple[Any, ...]]]:
    """Each row's path and the columns a shelve must not change, from SQL, in one query."""
    from sqlalchemy import bindparam, text

    if not content_ids:
        return {}
    selected = ", ".join(_KEPT_COLUMNS)
    statement = text(
        f"SELECT ID, {rb_writer.FOLDER_PATH_COLUMN}, {selected} FROM {rb_writer.CONTENT_TABLE} "
        f"WHERE ID IN :ids"
    ).bindparams(bindparam("ids", expanding=True))
    rows = db.session.execute(statement, {"ids": list(content_ids)}).all()
    return {str(row[0]): (str(row[1] or ""), tuple(row[2:])) for row in rows}


def _assert_confined(db: Any, plan: ShelfPlan) -> None:
    """Refuse, before the commit, a path change on any row the plan did not name.

    FROM SQL, after a flush, since the mapped objects say only what the writer
    intended. Every row under a target must be planned, and carry its path.
    """
    from sqlalchemy import text

    db.session.flush()
    violations: list[str] = []
    for one in plan.batches:
        planned = {row.content_id: row.folder_path for row in one.rows}
        # EVERY ROW UNDER THE NEW TARGET, TOMBSTONES INCLUDED: only planned rows belong.
        under = db.session.execute(
            text(
                f"SELECT ID, {rb_writer.FOLDER_PATH_COLUMN} FROM {rb_writer.CONTENT_TABLE} "
                f"WHERE {rb_writer.FOLDER_PATH_COLUMN} LIKE :prefix ESCAPE '\\'"
            ),
            {"prefix": _like_prefix(one.stored_target)},
        ).all()
        # LIKE IS CASE BLIND FOR ASCII, so the fetch is broad and the judgement exact.
        found = {
            str(row[0]): str(row[1] or "")
            for row in under
            if str(row[1] or "").startswith(one.stored_target + os.sep)
        }
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

    The session spine is the landing's, with the path policy registered for
    this commit alone. THE RENAMES COME FIRST AND ARE UNDONE ON ANY FAILURE
    PAST THEM, newest first, since the filesystem has no transaction; a rename
    that will not go back is named in the refusal.
    """
    watched = rotate.watched_roots(analysis_roots)
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
        record, capture = trees.attached_capture(gates, cfg, db)
        before = {cid: kept for cid, (_path, kept) in _select_rows(db, content_ids).items()}
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
            trees.rollback_quietly(db)
            if witness.landed:
                _record_shelve_commit(record, plan, cfg)
                raise
            if not moved and isinstance(exc, CratekitError):
                # A refusal before the first rename keeps its own words: nothing changed.
                raise
            failed = _rename_back(moved)
            if not isinstance(exc, Exception):
                # An interrupt is put back as far as it can be and re-raised as
                # itself, so nobody is asked to report pressing Ctrl-C as a defect.
                raise
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
        _record_shelve_commit(record, plan, cfg)
        read = _read_back(db, plan, before)
        session_id = record.session_id
    return Shelved(batches=plan.batches, rows=tuple(read), session_id=session_id)


def _assert_still_as_planned(db: Any, one: ShelfBatch) -> None:
    """Refuse a batch whose folder, target or rows moved since the plan was shown."""

    def stale(message: str, **detail: str) -> Exception:
        return refuse(
            "decision-stale", message, origin=_ORIGIN, detail={"batch": one.batch, **detail}
        )

    if not one.source.is_dir():
        raise stale(
            f"{one.source} is no longer a folder under the music folder, so the plan "
            f"that moved it is stale and nothing was moved",
            folder=str(one.source),
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
            raise stale(
                f"row {row.content_id} for {row.file_name} no longer carries the path the "
                f"plan was made against, so nothing was moved",
                content_id=row.content_id,
            )


def _record_shelve_commit(
    record: session.SessionRecord, plan: ShelfPlan, cfg: config.Config
) -> None:
    """Name every batch moved on the record, and the rows under the content table."""
    record.detail[SHELVED_KEY] = [
        {"batch": one.batch, "to": str(one.target), "rows": len(one.rows)} for one in plan.batches
    ]
    change = session.TreeChange(tree=rb_writer.CONTENT_TABLE, updated=plan.rows())
    session.record_commit(record, rb_writer.CONTENT_TABLE, session.ChangeSummary((change,)), cfg)


def _read_back(db: Any, plan: ShelfPlan, before: dict[str, tuple[Any, ...]]) -> list[ReadBack]:
    """Every planned row after the commit, refusing one that did not take or lost a column."""
    out: list[ReadBack] = []
    selected = _select_rows(db, [row.content_id for one in plan.batches for row in one.rows])
    after = {cid: kept for cid, (_path, kept) in selected.items()}
    for one in plan.batches:
        for row in one.rows:
            stored = selected.get(row.content_id, ("", ()))[0]
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
            kept = dict(zip(_KEPT_COLUMNS, after.get(row.content_id, ())))
            out.append(ReadBack(row.content_id, str(stored or ""), kept))
    return out
