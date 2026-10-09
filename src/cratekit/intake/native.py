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

A PLAYLIST THE AUTHOR MADE ON THE ACCOUNT GETS ITS OWN (U113). A landing hands
the plan its account playlists, each named against :func:`inbox_held` and each
holding the rows it claimed; they are created under the root, never found by
name, so two landings never share one, and the batch playlist keeps the rest.
The record names every one by identifier, which is what ``inbox rotate`` ages
them by.

``plan_rows`` AND ``apply_rows`` MEAN SOMETHING ELSE IN ``cratekit.tagging.rows``,
where a row is one that exists and whose genre is written from its file. Here
a row is a content row this engine adds. The two are not interchangeable.

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

#: What a planned row will do. A file whose suffix the binding has no file
#: type for is planned as UNSUPPORTED and left in staging by the landing, the
#: way a file whose target is occupied is: refused alone, and the batch lands.
ADD = "add"
PRESENT = "already present"
UNSUPPORTED = "unsupported"

#: The columns a landed row leaves for rekordbox, named once for the plan, the
#: record and the read back. THE WRITER'S LIST, not a copy of it: the guard is
#: what refuses a value here, and a second spelling is how the answer a person
#: reads and the answer the guard enforces come to differ.
LEFT_EMPTY: tuple[str, ...] = tuple(sorted(rb_writer.CONTENT_ROW_EMPTY_COLUMNS))

#: The session workflow a native landing is recorded under, the intake's own.
WORKFLOW = ingest.INTAKE_WORKFLOW

#: The session record field naming the batch playlist a landing wrote, its
#: identifier and its name. Read by ``inbox rotate`` for the landing date.
BATCH_PLAYLIST_KEY = "batch_playlist"
#: The session record field naming the sync pass a landing was given with
#: ``--pass`` (R-777). Written with the commit, so ``sync mark --pass`` reads a
#: closed record naming the pass as the proof the pass landed, the one an
#: intake file is on the bridge.
PASS_KEY = "pass"

#: The session record field listing the account playlists a landing wrote, each
#: by identifier and name (U113). The intake's one spelling, shared with the
#: intake file's record.
INBOX_PLAYLISTS_KEY = ingest.INBOX_PLAYLISTS_KEY

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
    #: Why the file is planned as ``UNSUPPORTED``, in a sentence, else empty.
    why: str = ""

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
class PlaylistPlan:
    """One INBOX playlist a landing writes for a playlist the author made on the account (U113)."""

    #: The name it is created under, chosen against what INBOX holds.
    name: str
    #: The account's identifier for the playlist it carries.
    account: str
    #: The planned targets it holds, in the order the landing planned them.
    targets: tuple[Path, ...]
    #: The account's own name for it, which ``name`` differs from only by a count.
    account_name: str = ""


@dataclass(frozen=True, slots=True)
class WrittenPlaylist:
    """One INBOX playlist the commit wrote for an account playlist, read for the report."""

    name: str
    playlist_id: str
    account: str
    tracks: int


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
    #: The account playlists, each its own INBOX playlist (U113). The batch
    #: playlist, ``playlist``, holds only the rows none of them holds.
    playlists: tuple[PlaylistPlan, ...] = ()
    #: The sync pass the landing was given with ``--pass``, recorded with the
    #: commit under :data:`PASS_KEY` (R-777). None for a landing of no pass.
    pass_name: str | None = None

    def to_add(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == ADD)

    def present(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == PRESENT)

    def unsupported(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == UNSUPPORTED)


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
    #: The account playlists written (U113). ``playlist_id`` is empty when every
    #: row went into one of these and the batch playlist held none.
    playlists: tuple[WrittenPlaylist, ...] = ()

    def names(self) -> tuple[str, ...]:
        """Every INBOX playlist the commit wrote, the batch's first when it wrote one."""
        batch = (self.playlist,) if self.playlist_id else ()
        return (*batch, *(written.name for written in self.playlists))


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


def file_type_of(path: Path) -> int | None:
    """The binding's file type for ``path``'s suffix, or None when it has none.

    The binding's own lookup raises the wrong exception class on a suffix it
    does not know, and it does so after the duplicate check, so it is asked
    here at plan time. None rather than a refusal, because the answer is one
    file's and the batch still lands: the file is planned as
    :data:`UNSUPPORTED` and stays in staging, the way an occupied target does.
    The xml landing takes every suffix ``AUDIO_EXTS`` names, since a Location
    is text, so a file this medium cannot name is not lost to the library.
    """
    from pyrekordbox.db6.tables import FileType

    name = path.suffix.lstrip(".").upper()
    found = getattr(FileType, name, None) if name else None
    return None if found is None else int(found.value)


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
    split: Sequence[PlaylistPlan] = (),
    pass_name: str | None = None,
) -> NativePlan:
    """Plan one row per file and one playlist, against the open database.

    ``files`` pairs where each file is now with where the landing will put it.
    The row is planned for the target, since that is the path rekordbox will
    open, and the title is read off the source, since the tags do not move.

    ``split`` is a landing's account playlists (U113), named by the caller
    against :func:`inbox_held` on this same handle, each holding targets of
    ``files``. They are part of the plan and of its digest.

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
        if match.outcome is trees.MatchOutcome.UNRESOLVED:
            # NOT ABSENT, UNASKED (R-770). The matcher could not put the target
            # under the library root or a prefix rule, so it never looked for a
            # row, and planning an add over that is planning a second row for a
            # file the collection may hold. Every reader that resolves against
            # the root would drop the row it made, too.
            raise refuse(
                "intake-list-unusable",
                f"{target} resolves nowhere under the library at "
                f"{cfg.library.root} or its prefix rules, so the collection could "
                f"not be asked whether it already holds that file and no row was "
                f"planned for it",
                origin=_ORIGIN,
                detail={"target": str(target), "root": str(cfg.library.root)},
            )
        held = _holding(match)
        file_type = file_type_of(target)
        if file_type is None:
            action, why = (
                UNSUPPORTED,
                (
                    f"{target.name} has a suffix rekordbox's database has no file type "
                    f"for, so no content row can name it and it was left in staging; "
                    f"convert it, or land it through the xml bridge"
                ),
            )
        else:
            action, why = (ADD if held is None else PRESENT), ""
        rows.append(
            RowPlan(
                source=source,
                target=target,
                action=action,
                title=str(ingest.file_meta(source, cfg=cfg)["name"]),
                folder_path=stored_folder_path(
                    target, base_drive=base_drive, current_drive=current_drive
                ),
                file_name=target.name,
                file_size=source.stat().st_size,
                file_type=file_type or 0,
                content_id=held,
                why=why,
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
        playlists=_supported_only(split, rows),
        pass_name=pass_name,
    )
    return replace(planned, digest=digest_of(identity(planned)))


def _supported_only(
    split: Sequence[PlaylistPlan], rows: Sequence[RowPlan]
) -> tuple[PlaylistPlan, ...]:
    """The account playlists over only the targets a row can be written for.

    A file planned ``UNSUPPORTED`` stays in staging and no playlist can hold it,
    so it is not counted on the screen as one of a playlist's, and a playlist
    holding nothing else is not planned.
    """
    unsupported = {str(row.target) for row in rows if row.action == UNSUPPORTED}
    kept = (
        replace(one, targets=tuple(t for t in one.targets if str(t) not in unsupported))
        for one in split
    )
    return tuple(one for one in kept if one.targets)


def inbox_held(db: Any, root_id: str) -> tuple[str, ...]:
    """Every name a live node anywhere under the intake root carries (U113).

    What a landing's account playlists are named against. Every descendant and
    not only the root's children, so a batch the rotation moved into ``Old``
    still holds its name. A removed node holds none: rekordbox no longer shows
    it, and an account playlist is created, never found by its name, so a
    removed node of that name is never written into.
    """
    # ONE READ OF THE TABLE, walked in memory, rather than a query per node.
    children: dict[str, list[Any]] = {}
    for row in list(db.get_playlist()):
        if not rb_writer.node_removed(row):
            children.setdefault(str(getattr(row, "ParentID", "") or ""), []).append(row)
    names: list[str] = []
    pending = [str(root_id)]
    while pending:
        for row in children.get(pending.pop(), ()):
            names.append(str(getattr(row, "Name", "") or ""))
            pending.append(str(row.ID))
    return tuple(names)


def identity(plan: NativePlan) -> dict[str, Any]:
    """What the digest covers: every fact the screen shows and the apply writes."""
    split = (
        {
            "playlists": [
                {
                    "name": one.name,
                    "account": one.account,
                    "targets": [str(target) for target in one.targets],
                }
                for one in plan.playlists
            ]
        }
        if plan.playlists
        else {}
    )
    return {
        **split,
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
    """Put the planned path and device, and rekordbox's defaults, on the row the binding made.

    The binding stores the path it was given to stat and the first device it
    finds. Both are corrected here when they differ from the plan, on the
    object before the flush the guard performs, so the guard judges the row as
    it will be stored. A row the binding got right is left alone. Every column
    of :data:`cratekit.core.rb_writer.CONTENT_ROW_DEFAULTS` the binding left
    NULL is given rekordbox's own value the same way (R-923).
    """
    if str(content.FolderPath) != row.folder_path:
        content.FolderPath = row.folder_path
    if str(content.DeviceID) != plan.device_id:
        content.DeviceID = plan.device_id
    if str(content.MasterDBID) != plan.master_db_id:
        content.MasterDBID = plan.master_db_id
    # REKORDBOX'S OWN DEFAULTS, ON THE SAME OBJECT BEFORE THE SAME FLUSH (R-923).
    # The binding leaves these NULL, and rekordbox will not load such a row to a
    # deck. Only a NULL is filled, so a value the binding chose stands.
    for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items():
        if getattr(content, column, None) is None:
            setattr(content, column, value)


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


def _candidate_rows(db: Any, names: Iterable[str]) -> list[trees.ContentRow]:
    """The active rows whose stored path ends in one of ``names``, as the matcher reads them.

    A CANDIDATE SET, NOT THE ANSWER. The rows are found by the file name at
    the end of the stored path, which is the one part of it the base drive and
    the mounted spelling share, and every candidate is then put through the
    same resolver the plan used. That keeps the one rule for comparing a path
    on this machine with a path rekordbox wrote down, and reads a handful of
    rows instead of the collection.
    """
    from pyrekordbox.db6 import tables

    found: list[trees.ContentRow] = []
    for name in set(names):
        query = db.session.query(tables.DjmdContent).filter(
            tables.DjmdContent.FolderPath.like(f"%{name}")
        )
        for row in query.all():
            found.append(
                trees.ContentRow(
                    content_id=str(row.ID),
                    recorded=str(getattr(row, "FolderPath", "") or ""),
                    deleted=trees.soft_delete_marker(row),
                )
            )
    return found


def _taken_since_the_plan(db: Any, cfg: config.Config, rows: Sequence[RowPlan]) -> dict[str, str]:
    """Each planned target a row has taken since the plan was made, by target.

    The plan is what was approved and it is not rebuilt, so the one thing the
    apply asks the database again is the question whose answer can change
    under an approval: whether the file is in the collection now. A row that
    appeared is counted present rather than doubled. Asked before the first
    row is added, so nothing pending is flushed by the read, and asked of the
    candidate rows rather than the whole collection.
    """
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    matches = trees.match_active_rows(
        [row.target for row in rows],
        _candidate_rows(db, (row.target.name for row in rows)),
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
        written: list[WrittenPlaylist] = []
        try:
            # BEFORE THE FIRST ROW, so a refusal adds nothing. A name the plan
            # chose free that INBOX holds now would show two playlists of one
            # name, and an account playlist is created rather than found.
            assert_names_still_free(db, plan)
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
            # In listing order: the files the plan named, in the order it named
            # them, whether the row is new or was already there.
            by_target = {str(row.target): content_id for row, content_id in added_ids}
            by_target.update({str(row.target): row.content_id for row in present if row.content_id})
            claimed = {str(target) for one in plan.playlists for target in one.targets}
            accounts = [
                (one, [by_target[str(t)] for t in one.targets if str(t) in by_target])
                for one in plan.playlists
            ]
            accounts = [(one, ids) for one, ids in accounts if ids]
            ordered = [
                by_target[str(row.target)]
                for row in plan.rows
                if str(row.target) in by_target and str(row.target) not in claimed
            ]
            # THE BATCH PLAYLIST HOLDS WHAT NO ACCOUNT PLAYLIST CLAIMED, and is
            # not written when that is nothing, as the intake file does it.
            if ordered or not accounts:
                playlist = rb_writer.ensure_playlist(db, plan.playlist, anchor)
                memberships = len(rb_writer.add_memberships(db, playlist, ordered))
                playlist_id = str(playlist.ID)
            for one, ids in accounts:
                created = db.create_playlist(one.name, parent=anchor)
                count = len(rb_writer.add_memberships(db, created, ids))
                memberships += count
                written.append(
                    WrittenPlaylist(
                        name=one.name,
                        playlist_id=str(created.ID),
                        account=one.account,
                        tracks=count,
                    )
                )
            rb_writer.commit_guarded(db, creations=(rb_writer.CONTENT_TABLE,))
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record_landing_commit(
                    record,
                    plan,
                    len(added_ids),
                    memberships,
                    cfg,
                    playlist_id=playlist_id,
                    written=written,
                )
            raise

        _record_landing_commit(
            record, plan, len(added_ids), memberships, cfg, playlist_id=playlist_id, written=written
        )
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
        playlists=tuple(written),
    )


def assert_names_still_free(db: Any, plan: NativePlan) -> None:
    """Refuse an account playlist name INBOX came to hold after the plan chose it.

    ASKED BY THE LANDING BEFORE ITS FIRST MOVE, so a refusal leaves the files in
    staging for the landing to be run again, and asked again here before the
    first row, inside the session, for whatever took a name in between.
    """
    if not plan.playlists:
        return
    held = set(inbox_held(db, plan.root_id))
    clash = sorted(one.name for one in plan.playlists if one.name in held)
    if clash:
        raise refuse(
            "decision-stale",
            f"the intake folder holds {', '.join(repr(name) for name in clash)} since "
            f"this landing chose those names, so nothing was written; run the landing "
            f"again and it takes the next free name",
            origin=_ORIGIN,
            detail={"names": clash, "root": plan.root_id},
        )


def _record_landing_commit(
    record: session.SessionRecord,
    plan: NativePlan,
    rows: int,
    memberships: int,
    cfg: config.Config,
    *,
    playlist_id: str,
    written: Sequence[WrittenPlaylist] = (),
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
    # THE BATCH PLAYLIST IS NAMED ON THE RECORD (U111), by identifier as well
    # as by name, so ``inbox rotate`` ages a batch from the day it landed
    # rather than from whatever the playlist row says. Written with the commit,
    # by the call that persists it.
    if playlist_id:
        record.detail[BATCH_PLAYLIST_KEY] = {"id": playlist_id, "name": plan.playlist}
    # AND THE PASS (R-777), which is what ``sync mark --pass`` reads as the
    # proof this pass landed. Only with the commit, never for a plan.
    if plan.pass_name:
        record.detail[PASS_KEY] = plan.pass_name
    # AND EACH ACCOUNT PLAYLIST (U113), whose name carries no date to age it by.
    if written:
        record.detail[INBOX_PLAYLISTS_KEY] = [
            {"id": one.playlist_id, "name": one.name} for one in written
        ]
    changes = []
    if memberships > 0:
        changes.append(session.TreeChange(tree=plan.tree_id, created=memberships))
    if rows > 0:
        changes.append(session.TreeChange(tree=rb_writer.CONTENT_TABLE, created=rows))
    session.record_commit(record, plan.tree_id, session.ChangeSummary(tuple(changes)), cfg)


def landings_of_pass(cfg: config.Config, name: str) -> tuple[str, ...]:
    """The session ids of every closed native landing that committed ``name``.

    THE PROOF ``sync mark --pass`` WAITS FOR (R-777), the native counterpart of
    an intake file: a record of this workflow, closed, whose intake source
    committed and whose detail names the pass. A landing refused after its
    moves leaves its files in the library and adds no row, and its record
    names no pass, so its files cannot mark a playlist by being on disk.
    """
    records, _unreadable = session.scan_log(cfg)
    return tuple(
        sorted(
            record.session_id
            for record in records
            if record.workflow == WORKFLOW
            and record.state is session.SessionState.CLOSED
            and str(session.SourceState.COMMITTED) in record.sources.values()
            and record.detail.get(PASS_KEY) == name
        )
    )


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
        if value not in rb_writer.EMPTY_ON_CREATE
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
    "BATCH_PLAYLIST_KEY",
    "INBOX_PLAYLISTS_KEY",
    "LEFT_EMPTY",
    "PRESENT",
    "UNSUPPORTED",
    "WORKFLOW",
    "AddedRow",
    "NativeLanded",
    "NativePlan",
    "PlaylistPlan",
    "RowPlan",
    "WrittenPlaylist",
    "anchored_intake_root",
    "apply_rows",
    "assert_names_still_free",
    "assert_rows_gridless",
    "choose_device",
    "file_type_of",
    "identity",
    "inbox_held",
    "plan_rows",
    "stored_folder_path",
]
