"""Land a batch in the collection through the guarded database writer (R-746).

The xml landing ends on five hand steps in rekordbox: point it at the intake
file, import one playlist, drag it into the intake folder, export again, run
``intake imported``. On a library whose intake tree has cut over, this engine
is the other medium: one content row per landed file and one batch playlist
under the adopted intake root, through the same session spine every database
tree writer uses, behind a plan and an approval the verb owns.

THIS IS A NEW KIND OF WRITE, and it is treated the way the cutover was. Every
row the guarded writer added before this unit was a membership, a playlist, a
folder or a tag association on rows rekordbox created. A CONTENT row is the
row rekordbox analyses into, so what it may carry is stated as a column policy
and asserted from SQL before the commit, in ``rb_writer``, and read back after
it here. The row carries what the file's tags and the filesystem say: a title,
a path, a name, a size, a type. Every column an analysis pass fills stays
empty for rekordbox to fill, and :data:`LEFT_EMPTY` names them so the record
and the envelope can say so.

WHAT SITTING 17 SETTLED, and this module obeys (A8, 2026-09-29, rekordbox
7.2.19, the live library):

* the stored path is under ``djmdProperty.BaseDBDrive``, which on a renamed
  volume is not the mounted path; rekordbox's own rows are, including rows it
  imported the same day. The binding is handed the mounted path to stat and the
  row is restamped with the base drive form before the commit;
* the device is the one whose ``MasterDBID`` equals the property table's
  ``DBID``. A library can hold two devices and the binding's default is order
  dependent, so the choice is made here and asserted, never trusted;
* the binding's bare row, ``add_content(path, Title=...)`` with every analysis
  column NULL, behaved exactly as a row dressed in rekordbox's own not yet
  analysed shape, so the simpler row is the one written;
* rekordbox analyses nothing on its own with Auto Analysis off. The answer
  says the rows await analysis. Triggering it is not this engine's.

THE PLAN IS BUILT AGAINST THE DATABASE AND THE APPLY REBUILDS NOTHING. The
verb opens the database with write intent, so an open rekordbox refuses before
anything is shown, plans every row and its columns, and digests them; the
person approves that digest. The apply takes the plan as approved and writes
it, and asks the database again only for what the plan could not know, which
is whether a row appeared between the two.

Layer: modules. It reads configuration through the objects it is handed and
opens no database of its own.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Sequence

from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    locations,
    rb_writer,
    session,
    snapshot,
    tree_registry,
)
from cratekit.core.cause import Remedy, refuse
from cratekit.intake import ingest
from cratekit.write import routing_pass, trees

#: What a planned row will do.
ADD = "add"
PRESENT = "already present"

#: The columns a landed row leaves for rekordbox, named once for the plan, the
#: record and the read back. THE WRITER'S LIST, not a copy of it: the guard is
#: what refuses a value here, and a second spelling is how the answer a person
#: reads and the answer the guard enforces come to differ.
LEFT_EMPTY: tuple[str, ...] = tuple(sorted(rb_writer.CONTENT_ROW_EMPTY_COLUMNS))

#: The session workflow a native landing is recorded under, the intake's own.
WORKFLOW = ingest.INTAKE_WORKFLOW

_ORIGIN = ("intake.native",)


@dataclass(frozen=True, slots=True)
class RowPlan:
    """One file, the row it would add, and every column that row would carry."""

    source: Path
    target: Path
    action: str
    title: str
    folder_path: str
    file_name: str
    file_size: int
    file_type: int
    #: The row already holding this file, when ``action`` is ``PRESENT``.
    content_id: str | None = None

    def columns(self) -> dict[str, Any]:
        """Every column the writer sets on the row, by name, for the screen."""
        return {
            "Title": self.title,
            "FolderPath": self.folder_path,
            "FileNameL": self.file_name,
            "FileSize": self.file_size,
            "FileType": self.file_type,
        }


@dataclass(frozen=True, slots=True)
class NativePlan:
    """What :func:`apply_rows` will write, and the fingerprint it was planned at."""

    tree_id: str
    root_id: str
    root_name: str
    playlist: str
    database: Path
    device_id: str
    master_db_id: str
    base_drive: str | None
    current_drive: str | None
    rows: tuple[RowPlan, ...]
    digest: str

    def to_add(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == ADD)

    def present(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == PRESENT)


@dataclass(frozen=True, slots=True)
class AddedRow:
    """One row the commit landed, read back from SQL after it."""

    target: Path
    content_id: str
    title: str
    folder_path: str
    #: The analysis columns and what each holds, every one expected empty.
    empty: dict[str, Any]


@dataclass(frozen=True, slots=True)
class NativeLanded:
    """What the commit landed: the rows, the playlist, and the memberships."""

    tree_id: str
    playlist: str
    playlist_id: str
    added: tuple[AddedRow, ...]
    present: tuple[RowPlan, ...]
    memberships_added: int
    session_id: str


def _property(db: Any) -> Any:
    from pyrekordbox.db6 import tables

    return db.session.query(tables.DjmdProperty).first()


def choose_device(db: Any) -> tuple[str, str]:
    """The device whose ``MasterDBID`` is the library's own, as (device id, master id).

    ASSERTED, NEVER TRUSTED. ``add_content`` stamps the first device the query
    returns, and the author's library holds two, one per machine that has ever
    opened it. A row stamped with the other machine's device is a plausible way
    to get an invisible or cloud confused row, so the device is chosen here by
    the one rule that identifies the library, and the row is restamped when the
    binding chose differently. Several matches take the lowest identifier, so
    the answer is a function of the database and not of query order.
    """
    from pyrekordbox.db6 import tables

    property_row = _property(db)
    dbid = None if property_row is None else str(getattr(property_row, "DBID", "") or "")
    devices = list(db.session.query(tables.DjmdDevice).all())
    matching = sorted(
        (device for device in devices if dbid and str(device.MasterDBID) == dbid),
        key=lambda device: str(device.ID),
    )
    if not matching:
        raise refuse(
            "collection-unreadable",
            f"no device row in the database carries the library's own identifier "
            f"{dbid!r}, so a content row could not be stamped with the device that "
            f"owns this library; {len(devices)} device row(s) were read",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"dbid": dbid, "devices": [str(device.ID) for device in devices]},
        )
    return str(matching[0].ID), str(matching[0].MasterDBID)


def stored_folder_path(path: Path, *, base_drive: str | None, current_drive: str | None) -> str:
    """The ``FolderPath`` rekordbox's own rows would carry for a mounted ``path``.

    UNDER THE BASE DRIVE, NOT THE MOUNTED ONE. ``djmdProperty`` records where
    the database was made and where it is now, and rekordbox remaps the first
    to the second at runtime, so a row stored under the mounted path on a
    renamed volume is the odd one out. When the two differ and the path is
    under the current drive, the prefix is swapped; a library whose drive has
    never moved, and a path outside the drive, are stored as they are. NFC,
    because rekordbox stores NFC and the filesystem may hand back NFD, and one
    byte of difference is a second row for one file (KTD27).
    """
    text = locations.norm_for_compare(str(path))
    if base_drive and current_drive and base_drive != current_drive:
        current = locations.norm_for_compare(current_drive).rstrip("/\\")
        if text == current or text.startswith(current + os.sep):
            return locations.norm_for_compare(base_drive).rstrip("/\\") + text[len(current) :]
    return text


def file_type_of(path: Path) -> int:
    """The binding's file type for ``path``'s suffix, or a refusal naming it.

    The binding's own lookup raises the wrong exception class on a suffix it
    does not know, and it does so after the duplicate check, so it is asked
    here at plan time, where a refusal moves nothing.
    """
    from pyrekordbox.db6.tables import FileType

    name = path.suffix.lstrip(".").upper()
    found = getattr(FileType, name, None) if name else None
    if found is None:
        raise refuse(
            "intake-list-unusable",
            f"{path.name} has a suffix rekordbox's database has no file type for, so "
            f"no content row can name it; the xml landing takes it on a library "
            f"whose intake tree is on the bridge",
            origin=_ORIGIN,
            detail={"path": str(path), "suffix": path.suffix},
        )
    return int(found.value)


def anchored_intake_root(db: Any, tree_id: str, registry: tree_registry.Registry) -> str:
    """The intake tree's adopted root, or the refusal that names ``tree cutover``.

    THROUGH THE SHARED ASSERTION, which refuses a tree still on the bridge, a
    native record naming no root, and a root this library does not have. The
    first is rephrased in this verb's words with the verb that fixes it,
    because the shared refusal is written for a writer that arrived at the
    wrong medium by mistake and this one arrives there because the person has
    not cut the intake tree over yet.
    """
    try:
        return tree_registry.anchored_root(
            tree_id, registry, root_exists=lambda root_id: db.get_playlist(ID=root_id) is not None
        )
    except tree_registry.TreeModeRefused as exc:
        if exc.cause.reason != "tree-unconverged" or exc.mode != tree_registry.Mode.XML:
            raise
        raise refuse(
            "tree-unconverged",
            f"the intake tree {tree_id!r} is still on the xml bridge, so a landing "
            f"adds nothing to the collection through the database; the xml landing "
            f"takes --export, or cut the intake tree over first",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=(
                f"run crate tree cutover {tree_id} --export with a Fresh Export to "
                f"move the intake tree to the database",
                "or land with --export to splice the batch into that export as before",
            ),
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "mode": str(exc.mode)},
            inner=exc.cause,
        ) from exc


def plan_rows(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    batch: str,
    files: Sequence[tuple[Path, Path]],
) -> NativePlan:
    """Plan one row per file and one playlist, against the open database.

    ``files`` pairs where each file is now with where the landing will put it.
    The row is planned for the target, since that is the path rekordbox will
    open, and the title is read off the source, since the tags do not move.

    A FILE THE COLLECTION HOLDS IS PRESENT, NOT ADDED TWICE. The target is
    matched against every active row the way the membership writers match,
    through one index of the collection resolved on this machine, so a row
    stored under the base drive and a row stored under the mounted path both
    count. Two active rows on one path count as present too: adding a third
    is not the answer to a duplicate.
    """
    root_id = anchored_intake_root(db, tree_id, registry)
    root = db.get_playlist(ID=root_id)
    device_id, master_db_id = choose_device(db)
    base_drive, current_drive = rb_writer.recorded_db_drives(db)
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    index = trees.index_active_rows(
        routing_pass.content_rows(db), root=cfg.library.root, prefix_map=prefix_map
    )
    matches = trees.match_indexed_rows(
        [target for _source, target in files], index, root=cfg.library.root, prefix_map=prefix_map
    )
    rows: list[RowPlan] = []
    for (source, target), match in zip(files, matches):
        held = _holding(match)
        rows.append(
            RowPlan(
                source=source,
                target=target,
                action=ADD if held is None else PRESENT,
                title=str(ingest.file_meta(source, cfg=cfg)["name"]),
                folder_path=stored_folder_path(
                    target, base_drive=base_drive, current_drive=current_drive
                ),
                file_name=target.name,
                file_size=source.stat().st_size,
                file_type=file_type_of(target),
                content_id=held,
            )
        )
    planned = NativePlan(
        tree_id=tree_id,
        root_id=str(root_id),
        root_name=str(getattr(root, "Name", "") or ""),
        playlist=batch,
        database=Path(rb_writer.handle_path(db) or rb_writer.live_db_path(cfg)),
        device_id=device_id,
        master_db_id=master_db_id,
        base_drive=base_drive,
        current_drive=current_drive,
        rows=tuple(rows),
        digest="",
    )
    return replace(planned, digest=digest_of(identity(planned)))


def identity(plan: NativePlan) -> dict[str, Any]:
    """What the digest covers: every fact the screen shows and the apply writes."""
    return {
        "kind": "land-native",
        "tree": plan.tree_id,
        "root": plan.root_id,
        "playlist": plan.playlist,
        "database": str(plan.database),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
        "rows": [
            {
                "from": str(row.source),
                "to": str(row.target),
                "action": row.action,
                "content_id": row.content_id,
                "columns": row.columns(),
            }
            for row in plan.rows
        ],
        "left_empty": list(LEFT_EMPTY),
    }


def _restamp(content: Any, row: RowPlan, plan: NativePlan) -> None:
    """Put the planned path and device on the row the binding made.

    The binding stores the path it was given to stat and the first device it
    finds. Both are corrected here when they differ from the plan, on the
    object before the flush the guard performs, so the guard judges the row as
    it will be stored. A row the binding got right is left alone.
    """
    if str(content.FolderPath) != row.folder_path:
        content.FolderPath = row.folder_path
    if str(content.DeviceID) != plan.device_id:
        content.DeviceID = plan.device_id
    if str(content.MasterDBID) != plan.master_db_id:
        content.MasterDBID = plan.master_db_id


def _read_back(db: Any, content_id: str) -> tuple[dict[str, Any], str, str]:
    """The analysis columns, title and path of one row, from SQL after the commit."""
    from sqlalchemy import text

    selected = ", ".join(LEFT_EMPTY)
    row = db.session.execute(
        text(f"SELECT Title, FolderPath, {selected} FROM djmdContent WHERE ID = :id"),
        {"id": content_id},
    ).first()
    if row is None:
        raise refuse(
            "internal-error",
            f"the content row {content_id!r} was committed and could not be read "
            f"back, so the landing cannot say what it holds",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"content_id": content_id},
        )
    values = dict(zip(LEFT_EMPTY, row[2:]))
    return values, str(row[0] or ""), str(row[1] or "")


def _holding(match: trees.RowMatch) -> str | None:
    """The active row a match names, the first of several when two claim it."""
    if match.content_id:
        return str(match.content_id)
    if match.content_ids:
        return str(match.content_ids[0])
    return None


def _taken_since_the_plan(db: Any, cfg: config.Config, rows: Sequence[RowPlan]) -> dict[str, str]:
    """Each planned target a row has taken since the plan was made, by target.

    The plan is what was approved and it is not rebuilt, so the one thing the
    apply asks the database again is the question whose answer can change
    under an approval: whether the file is in the collection now. A row that
    appeared is counted present rather than doubled. ONE walk of the collection,
    before the first row is added, so nothing pending is flushed by the read.
    """
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    matches = trees.match_active_rows(
        [row.target for row in rows],
        routing_pass.content_rows(db),
        root=cfg.library.root,
        prefix_map=prefix_map,
    )
    taken: dict[str, str] = {}
    for row, match in zip(rows, matches):
        held = _holding(match)
        if held is not None:
            taken[str(row.target)] = held
    return taken


def apply_rows(
    cfg: config.Config,
    db: Any,
    plan: NativePlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> NativeLanded:
    """Write the plan: the rows, the playlist under the root, the memberships.

    THE SESSION SPINE IS CALLED, NOT REBUILT, and it is the one the membership
    writers use: the three gates in their argued order with a record kept, a
    capture the commit happens behind, the analysis watch over the roots named,
    the commit witness, and the guarded commit. The one thing this commit says
    that no other does is ``creations``, which names the content table and
    admits the rows the whitelist would otherwise refuse (R-760).

    ALL OR NOTHING IN THE DATABASE. Every row and every membership is pending on
    one handle until one commit, and a refusal anywhere before it rolls the
    handle back, so a failure on the second of three files leaves the table as
    it was. The files are in the library by then, which the caller reports.

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
    registry = tree_registry.read(cfg)
    root_id = anchored_intake_root(db, plan.tree_id, registry)
    if root_id != plan.root_id:
        raise refuse(
            "decision-stale",
            f"the intake tree {plan.tree_id!r} is anchored to root {root_id!r} and the "
            f"plan was made against {plan.root_id!r}, so nothing was written",
            origin=_ORIGIN,
            detail={"planned": plan.root_id, "anchored": root_id},
        )
    convergence.assert_tree_writable(cfg, db, plan.tree_id, registry)

    added_ids: list[tuple[RowPlan, str]] = []
    present: list[RowPlan] = list(plan.present())
    memberships = 0
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

        anchor = db.get_playlist(ID=plan.root_id)
        if anchor is None:
            raise tree_registry.RegistrySkew(
                f"the adopted intake root {plan.root_id!r} was reported present and "
                f"could not be read back, so the batch playlist has nothing to hang "
                f"from and would be created beside the tree instead",
                tree_id=plan.tree_id,
                root_id=plan.root_id,
            )
        playlist_id = ""
        try:
            to_add = plan.to_add()
            taken = _taken_since_the_plan(db, cfg, to_add)
            for row in to_add:
                held = taken.get(str(row.target))
                if held is not None:
                    present.append(replace(row, action=PRESENT, content_id=held))
                    continue
                content = db.add_content(row.target, Title=row.title)
                _restamp(content, row, plan)
                added_ids.append((row, str(content.ID)))
            playlist = rb_writer.ensure_playlist(db, plan.playlist, anchor)
            # In listing order: the files the plan named, in the order it named
            # them, whether the row is new or was already there.
            by_target = {str(row.target): content_id for row, content_id in added_ids}
            by_target.update({str(row.target): row.content_id for row in present if row.content_id})
            ordered = [
                by_target[str(row.target)] for row in plan.rows if str(row.target) in by_target
            ]
            memberships = len(rb_writer.add_memberships(db, playlist, ordered))
            playlist_id = str(playlist.ID)
            rb_writer.commit_guarded(db, creations=(rb_writer.CONTENT_TABLE,))
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record(record, plan, len(added_ids), memberships, cfg)
            raise

        _record(record, plan, len(added_ids), memberships, cfg)
        convergence.record_fingerprint(cfg, db)

        landed = []
        for row, content_id in added_ids:
            values, title, folder_path = _read_back(db, content_id)
            landed.append(
                AddedRow(
                    target=row.target,
                    content_id=content_id,
                    title=title,
                    folder_path=folder_path,
                    empty=values,
                )
            )
        session_id = record.session_id

    return NativeLanded(
        tree_id=plan.tree_id,
        playlist=plan.playlist,
        playlist_id=playlist_id,
        added=tuple(landed),
        present=tuple(present),
        memberships_added=memberships,
        session_id=session_id,
    )


def _record(
    record: session.SessionRecord, plan: NativePlan, rows: int, memberships: int, cfg: config.Config
) -> None:
    """Record the commit on the session, once anything landed.

    TWO COUNTS UNDER TWO NAMES. The intake tree's entry is the memberships, the
    number ``restore list`` asks for and the one ``tree cutover`` reads to
    refuse a revert after a native write. The content table's entry is the rows,
    kept apart because a restore that discards them discards tracks, not
    memberships, and a person weighing that should see the difference.
    """
    if rows <= 0 and memberships <= 0:
        return
    changes = []
    if memberships > 0:
        changes.append(session.TreeChange(tree=plan.tree_id, created=memberships))
    if rows > 0:
        changes.append(session.TreeChange(tree=rb_writer.CONTENT_TABLE, created=rows))
    session.record_commit(record, plan.tree_id, session.ChangeSummary(tuple(changes)), cfg)


def assert_rows_gridless(landed: NativeLanded) -> None:
    """Refuse when a row read back after the commit carries an analysis value.

    THE GUARD HOLDS THIS BEFORE THE COMMIT, so reaching here is a defect in the
    guard rather than in the landing, and it is reported as one. The read is
    made anyway, because the record promises a column by column statement about
    the rows as rekordbox will find them, and a promise checked only before the
    write is a promise about a different moment.
    """
    carried = [
        f"{row.content_id}: {name} = {value!r}"
        for row in landed.added
        for name, value in row.empty.items()
        if value not in (None, 0, 0.0, "", "0")
    ]
    if carried:
        raise refuse(
            "whitelist-violation",
            "a landed row carries an analysis value after the commit, which the "
            "guard should have refused before it: " + "; ".join(carried),
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"carried": carried},
        )


__all__ = [
    "ADD",
    "LEFT_EMPTY",
    "PRESENT",
    "WORKFLOW",
    "AddedRow",
    "NativeLanded",
    "NativePlan",
    "RowPlan",
    "anchored_intake_root",
    "apply_rows",
    "assert_rows_gridless",
    "choose_device",
    "file_type_of",
    "identity",
    "plan_rows",
    "stored_folder_path",
]
