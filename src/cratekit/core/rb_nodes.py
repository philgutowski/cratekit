"""Playlist, membership and tag primitives, and the node move and removal (U111).

Part of :mod:`cratekit.core.rb_writer`, which re-exports every name here; read them there. A
name of the writer outside this file, and every seam a test patches, is read through
``rb_writer`` at call time so a patch on the writer bites here too (U300). The soft-delete
marker is read in the writer itself, by :func:`cratekit.core.rb_writer.soft_deleted`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.rb_call_time import writer as _writer
from cratekit.core.rb_tables import (
    _MOVED_COLUMNS,
    _SIBLING_COLUMNS,
    CONTENT_TABLE,
    MEMBERSHIP_TABLE,
    PLAYLIST_TABLE,
    ROOT_PARENT_SENTINELS,
)


def is_folder(playlist: Any) -> bool:
    """Whether a playlist row is a FOLDER. The one spelling of that question."""
    return int(getattr(playlist, "Attribute", -1)) == 1


def ensure_folder(db: Any, name: str, parent: Any = None) -> Any:
    """Find or create a playlist FOLDER by name, optionally under a parent.

    ``name`` has no default, so no taxonomy name lives here (R19). ``parent``
    scopes the match as :func:`ensure_playlist` does, since two trees may hold
    folders of one name; unscoped is for a top-level folder.
    """
    if parent is None:
        for playlist in db.get_playlist(Name=name):
            if is_folder(playlist):
                return playlist
        return db.create_playlist_folder(name)

    parent_id = str(parent.ID)
    for playlist in db.get_playlist(Name=name):
        if is_folder(playlist) and str(getattr(playlist, "ParentID", "")) == parent_id:
            return playlist
    return db.create_playlist_folder(name, parent=parent)


def top_level_folders(db: Any, name: str) -> tuple[Any, ...]:
    """Every playlist FOLDER named ``name`` sitting directly under the playlist root.

    All of them, so a caller recording an adopted root can require exactly one;
    a nested namesake is not a candidate. IT CREATES NOTHING and reads no soft
    delete marker. The rows are materialized before the caller reads further.
    """
    return tuple(
        playlist
        for playlist in list(db.get_playlist(Name=name))
        if is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
    )


def ensure_playlist(db: Any, name: str, parent: Any) -> Any:
    """Find or create a playlist under a specific parent, never global by name."""
    parent_id = str(parent.ID)
    for playlist in db.get_playlist(Name=name):
        if not is_folder(playlist) and str(getattr(playlist, "ParentID", "")) == parent_id:
            return playlist
    return db.create_playlist(name, parent=parent)


def add_memberships(db: Any, playlist: Any, content_ids: Iterable[str]) -> list[str]:
    """Add each track to a playlist when absent. Returns the ids it inserted, in order.

    THE ONE HOME OF "ONLY WHEN ABSENT" (R-10); a second spelling double inserts
    or skips. One presence query per call, each insert joining the set. Race-free
    ONLY under the write-session lock. A MEMBERSHIP MARKED REMOVED IS NOT PRESENT
    (R-758), or a track moved back would never return.
    """
    songs = list(db.get_playlist_songs(PlaylistID=str(playlist.ID)))
    present = {str(song.ContentID) for song in songs if not _writer().membership_removed(song)}
    highest = max((int(song.TrackNo or 0) for song in songs), default=0)
    inserted: list[str] = []
    for content_id in content_ids:
        key = str(content_id)
        if key in present:
            continue
        added = db.add_to_playlist(playlist, key)
        # AN APPEND GOES PAST THE HIGHEST POSITION, NOT PAST THE ROW COUNT (U288):
        # gaps and removed rows make count plus one collide with a live row.
        number = int(getattr(added, "TrackNo", 0) or 0)
        if added is not None and number <= highest:
            added.TrackNo = highest + 1
            number = highest + 1
        highest = max(highest, number)
        present.add(key)
        inserted.append(key)
    return inserted


def add_membership(db: Any, playlist: Any, content_id: str) -> bool:
    """Add a track to a playlist when absent, through :func:`add_memberships`. True when it inserted."""
    return bool(_writer().add_memberships(db, playlist, [content_id]))


def remove_memberships(db: Any, playlist: Any, content_ids: Iterable[str]) -> list[str]:
    """Mark each track's live membership of one playlist removed. Returns the ids.

    THE ONE REMOVAL THIS PRODUCT MAKES, AND IT IS A SOFT DELETE (R-758): the
    marker set, ``updated_at`` now, ``TrackNo`` kept so nothing renumbers. Not
    the binding's ``remove_from_playlist``, which hard deletes and COMMITS BY
    ITSELF. rekordbox's observed removed rows all sat in removed playlists, so a
    single track out of a living one was not observed (in the ledger). EVERY LIVE
    ROW FOR THE PAIR IS MARKED; unheld ids are skipped. DOES NOT COMMIT: the
    caller commits through :func:`commit_guarded` naming this table in ``removals``.
    """
    from datetime import datetime

    wanted = {str(content_id) for content_id in content_ids}
    now = datetime.now()
    removed: list[str] = []
    for song in list(db.get_playlist_songs(PlaylistID=str(playlist.ID))):
        key = str(song.ContentID)
        if key not in wanted or _writer().membership_removed(song):
            continue
        setattr(song, _writer().SOFT_DELETE_COLUMN, 1)
        song.updated_at = now
        removed.append(key)
    return removed


def _node_refusal(reason: str, message: str, playlist: Any) -> CratekitError:
    return refuse(
        reason,
        message,
        remedy=Remedy.REPORT_DEFECT,
        scope=Scope.RUN,
        origin=("rb_writer",),
        detail={"playlist_id": str(getattr(playlist, "ID", ""))},
    )


def _plain_playlist(playlist: Any, what: str) -> None:
    """Refuse anything but a live, ordinary playlist. A folder carries a tree."""
    if int(getattr(playlist, "Attribute", -1)) != 0:
        raise _node_refusal(
            "whitelist-violation",
            f"{what} the playlist row {getattr(playlist, 'ID', '?')!r}, which is a "
            f"folder or a smart playlist; only an ordinary playlist is moved or "
            f"removed, so a node holding other nodes is never taken with it",
            playlist,
        )
    if _writer().node_removed(playlist):
        raise _node_refusal(
            "whitelist-violation",
            f"{what} the playlist row {getattr(playlist, 'ID', '?')!r}, which "
            f"rekordbox or this product already removed",
            playlist,
        )


def move_playlist_node(db: Any, playlist: Any, parent: Any) -> None:
    """Move one ordinary playlist to the end of a live folder. Never a folder.

    Through the binding's ``move_playlist``: parent and position change, old
    siblings close up, nothing held is touched. REFUSED, NOT SKIPPED: a folder or
    smart playlist, a removed node, a parent not a live folder. DOES NOT COMMIT.
    """
    _plain_playlist(playlist, "asked to move")
    if not is_folder(parent) or _writer().node_removed(parent):
        raise _node_refusal(
            "whitelist-violation",
            f"asked to move a playlist into {getattr(parent, 'ID', '?')!r}, which "
            f"is not a live folder",
            playlist,
        )
    db.move_playlist(playlist, parent=parent)


def remove_playlist_node(db: Any, playlist: Any) -> list[str]:
    """Mark one ordinary playlist removed, with its own memberships. Returns their ids.

    THE SAME SOFT DELETE (R-758), as rekordbox's own removed playlists show. No
    content row and no other playlist's membership is touched; ``Seq`` stays.
    REFUSED: a folder (carries a tree), a smart playlist (no rows), a removed node.
    DOES NOT COMMIT: ``removals`` must name this and the membership table.
    """
    from datetime import datetime

    _plain_playlist(playlist, "asked to remove")
    held = [
        str(song.ContentID)
        for song in list(db.get_playlist_songs(PlaylistID=str(playlist.ID)))
        if not _writer().membership_removed(song)
    ]
    marked = _writer().remove_memberships(db, playlist, held)
    setattr(playlist, _writer().SOFT_DELETE_COLUMN, 1)
    playlist.updated_at = datetime.now()
    return marked


@dataclass(frozen=True)
class NodeTables:
    """The three tables a node change could reach, read from SQL with no mapper, row by row.

    Content is one digest per row, since only "did any row differ" is asked of it.
    """

    content: Mapping[str, str]
    playlists: Mapping[str, tuple]
    memberships: Mapping[str, tuple]
    playlist_columns: tuple[str, ...]
    membership_columns: tuple[str, ...]


def _rows_by_id(session: Any, table: str) -> tuple[dict[str, tuple], tuple[str, ...]]:
    from sqlalchemy import text

    result = session.execute(text(f"SELECT * FROM {table}"))
    columns = tuple(result.keys())
    at = columns.index("ID")
    return {str(row[at]): tuple(row) for row in result}, columns


def _row_digests(session: Any, table: str) -> dict[str, str]:
    import hashlib

    rows, _columns = _rows_by_id(session, table)
    return {key: hashlib.sha256(repr(row).encode("utf-8")).hexdigest() for key, row in rows.items()}


def node_tables(db: Any) -> NodeTables:
    """Read the content, playlist and membership tables from SQL, before and after a node change."""
    session = db.session
    content = _row_digests(session, CONTENT_TABLE)
    playlists, playlist_columns = _rows_by_id(session, PLAYLIST_TABLE)
    memberships, membership_columns = _rows_by_id(session, MEMBERSHIP_TABLE)
    return NodeTables(content, playlists, memberships, playlist_columns, membership_columns)


def _changed(columns: Sequence[str], before: tuple, after: tuple) -> set[str]:
    return {name for name, old, new in zip(columns, before, after) if old != new}


def node_change_violations(
    before: NodeTables,
    after: NodeTables,
    *,
    moved: Mapping[str, str],
    removed: Iterable[str],
    created: Iterable[str] = (),
) -> list[str]:
    """Every difference between two readings that the planned node change does not explain.

    ``moved`` maps playlist to new folder, ``removed`` and ``created`` name rows.
    Empty means the change was confined AND made. PURE. It explains only: no
    content change; membership marker going on inside removed playlists; a moved
    playlist live under its folder changing parent, position and bookkeeping; a
    removed one gaining the marker; EACH ASKED WHETHER IT CHANGED, so an unmade
    write refuses before the commit; others repositioned only in a parent a node
    left or joined; added playlist rows exactly ``created``, nothing else added
    or gone.
    """
    rb_writer = _writer()
    violations: list[str] = []
    gone = {str(key) for key in removed}
    planned_moves = {str(key): str(value) for key, value in moved.items()}
    if before.content != after.content:
        changed = sorted(
            key
            for key in set(before.content) | set(after.content)
            if before.content.get(key) != after.content.get(key)
        )
        violations.append(
            f"{len(changed)} {CONTENT_TABLE} row(s) changed, and a node change "
            f"touches no track: {', '.join(changed[:10])}"
        )

    p_cols = before.playlist_columns
    marker_at = p_cols.index(rb_writer.SOFT_DELETE_COLUMN)
    parent_at = p_cols.index("ParentID")
    for key in sorted(set(before.playlists) - set(after.playlists)):
        violations.append(f"the {PLAYLIST_TABLE} row {key!r} disappeared")
    added = set(after.playlists) - set(before.playlists)
    for key in sorted(added - {str(key) for key in created}):
        violations.append(f"an unplanned {PLAYLIST_TABLE} row {key!r} was added")
    # The parents a node left or joined: the only places a renumbering belongs.
    renumbered = {
        str(before.playlists[key][parent_at]) for key in planned_moves if key in before.playlists
    } | set(planned_moves.values())
    for key in sorted(planned_moves):
        new = after.playlists.get(key)
        if new is None or str(new[parent_at]) != planned_moves[key] or new[marker_at]:
            violations.append(
                f"the moved playlist {key!r} is not live under the planned "
                f"{planned_moves[key]!r}"
            )
    for key in sorted(gone):
        new = after.playlists.get(key)
        if new is None or not new[marker_at]:
            violations.append(f"the removed playlist {key!r} does not carry the marker")
    for key in sorted(set(before.playlists) & set(after.playlists)):
        old, new = before.playlists[key], after.playlists[key]
        changed = _changed(p_cols, old, new)
        if not changed:
            continue
        if key in planned_moves:
            allowed = _MOVED_COLUMNS
        elif key in gone:
            allowed = _writer()._REMOVED_COLUMNS
        elif str(old[parent_at]) in renumbered:
            allowed = _SIBLING_COLUMNS
        else:
            allowed = frozenset()
        stray = changed - allowed
        if stray:
            violations.append(
                f"the {PLAYLIST_TABLE} row {key!r} changed {sorted(stray)}, which the "
                f"planned node change does not explain"
            )

    m_cols = before.membership_columns
    owner_at = m_cols.index("PlaylistID")
    m_marker = m_cols.index(rb_writer.SOFT_DELETE_COLUMN)
    for key in sorted(set(before.memberships) ^ set(after.memberships)):
        violations.append(f"the {MEMBERSHIP_TABLE} row {key!r} was added or disappeared")
    # A REMOVED NODE KEEPS NO LIVE MEMBERSHIP, asked of every row it owns.
    for key, row in sorted(after.memberships.items()):
        if str(row[owner_at]) in gone and not row[m_marker]:
            violations.append(
                f"the {MEMBERSHIP_TABLE} row {key!r} of the removed playlist "
                f"{str(row[owner_at])!r} is still live"
            )
    for key in sorted(set(before.memberships) & set(after.memberships)):
        old, new = before.memberships[key], after.memberships[key]
        changed = _changed(m_cols, old, new)
        if not changed:
            continue
        owner = str(old[owner_at])
        if owner not in gone:
            violations.append(
                f"the {MEMBERSHIP_TABLE} row {key!r} of playlist {owner!r} changed "
                f"{sorted(changed)}, and only a removed playlist's own memberships may"
            )
            continue
        if changed - _writer()._REMOVED_COLUMNS or not new[m_marker]:
            violations.append(
                f"the {MEMBERSHIP_TABLE} row {key!r} of the removed playlist {owner!r} "
                f"changed {sorted(changed)}; only its marker may go on"
            )
    return violations


def assert_node_changes_confined(
    db: Any,
    before: NodeTables,
    *,
    moved: Mapping[str, str],
    removed: Iterable[str],
    created: Iterable[str] = (),
) -> None:
    """Refuse, before the commit, a node change that reached anything it did not plan.

    FROM SQL, after a deliberate flush inside the transaction. It judges rows
    (whose membership, which parent, which position), which the table and column
    whitelist cannot, nor the binding's untracked sibling renumbering. A REFUSAL
    ROLLS THE HANDLE BACK so nothing lands later under another operation's name.
    """
    db.session.flush()
    after = node_tables(db)
    violations = node_change_violations(
        before, after, moved=moved, removed=removed, created=created
    )
    if violations:
        db.rollback()
        raise _writer()._unavailable(
            "whitelist-violation",
            "the node change reached rows it did not plan, or did not make one it "
            "planned, read from SQL before the commit:\n  - " + "\n  - ".join(violations),
            detail={"violations": violations},
        )


def my_tag_writable(db: Any) -> bool:
    """Whether :func:`ensure_my_tag_value` could make a row here, asked before a plan promises one.

    THE WRITER'S OWN QUESTION, so a plan never promises a tag after its file moves (U127).
    """
    try:
        _writer()._mytag_templates(db)
    except _writer().RekordboxUnavailable as exc:
        if exc.cause.reason != "mytag-category-template-missing":
            raise
        return False
    return True


def ensure_my_tag_value(db: Any, category_name: str, value_name: str) -> Any:
    """Find or create a tag category and one value inside it. Returns the value row."""
    from uuid import uuid4

    from pyrekordbox.db6 import tables

    root_parent, category_attr, value_attr = _writer()._mytag_templates(db)

    def created(name: str, attribute: Any, parent: Any) -> Any:
        row = tables.DjmdMyTag.create(
            ID=db.generate_unused_id(tables.DjmdMyTag, is_28_bit=True),
            UUID=str(uuid4()),
            Name=name,
            Attribute=attribute,
            ParentID=parent,
            Seq=0,
        )
        db.add(row)
        return row

    category = next((tag for tag in db.get_my_tag(Name=category_name)), None)
    if category is None:
        category = created(category_name, category_attr, root_parent)

    value = next(
        (
            tag
            for tag in db.get_my_tag(Name=value_name)
            if str(getattr(tag, "ParentID", "")) == str(category.ID)
        ),
        None,
    )
    if value is None:
        value = created(value_name, value_attr, str(category.ID))
    return value


def add_my_tag(db: Any, value_row: Any, content_id: str) -> bool:
    """Associate a track with a tag value when absent. True when it inserted."""
    from uuid import uuid4

    from pyrekordbox.db6 import tables

    existing = db.get_my_tag_songs(
        MyTagID=str(value_row.ID), ContentID=str(content_id)
    ).first()
    if existing is not None:
        return False
    db.add(
        tables.DjmdSongMyTag.create(
            ID=db.generate_unused_id(tables.DjmdSongMyTag),
            UUID=str(uuid4()),
            MyTagID=str(value_row.ID),
            ContentID=str(content_id),
            TrackNo=0,
        )
    )
    return True
