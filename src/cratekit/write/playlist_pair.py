"""The rekordbox side of a playlist pair: read one playlist in order, and write it.

U130. ``sync pair`` keeps one of the author's account playlists and one
rekordbox playlist the same list. This module is everything that pair needs from
the database: one plain playlist read with its live memberships in track order,
the facts of the rows it holds, the rows the library holds by ISRC, and the one
write, which adds memberships, takes memberships out and numbers the live
memberships in the merged order.

**MEMBERSHIPS ONLY. NO ROW OF THE COLLECTION IS MADE, CHANGED OR REMOVED.** An
addition names a content row the library already holds, a removal is
``rb_writer.remove_memberships``'s soft delete of a membership, and an order is
a ``TrackNo`` on a live membership. A track taken off the playlist is still in
the collection and in every other playlist that holds it.

**THE ORDER IS ONE THROUGH N OVER THE LIVE MEMBERSHIPS.** A removed membership
keeps the number it had, which ``rb_writer.remove_memberships`` says on purpose,
and the binding numbers a new membership from the count of every row, removed
ones included, so a number one past the live ones is never one a live row
holds. What rekordbox makes of a live number a removed row also carries was not
observed on a real library and is the attended sitting's to read.

**THE SESSION SPINE IS CALLED, NOT REBUILT**, as every database membership
writer calls it: the gates with a record kept, a capture verified before
anything is written, the analysis watch over the roots named, the commit
witness, and the guarded commit admitting the membership table for the
removals. The playlist is read again on the write handle first, and one whose
memberships moved since the plan was approved refuses with nothing written.

Layer: write.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from cratekit.core import config, convergence, rb_writer, session, snapshot
from cratekit.core.cause import refuse
from cratekit.write import trees

#: The workflow a pair's write session is recorded under. Not the verb's name,
#: which this layer does not spell.
WORKFLOW = "playlist-pair"

_ORIGIN = ("playlist_pair",)

#: The ``Attribute`` of a plain playlist. A folder and a smart playlist carry
#: another, and neither holds memberships a pair could keep.
PLAIN_PLAYLIST = 0

#: The ``ParentID`` of a node at the top of the playlist tree.
ROOT_PARENT = "root"


@dataclass(frozen=True, slots=True)
class Row:
    """One live membership and the facts of the content row it holds."""

    row_id: str
    content_id: str
    title: str = ""
    artist: str = ""
    isrc: str = ""
    path: str = ""


@dataclass(frozen=True, slots=True)
class Playlist:
    """One playlist node and, for a plain playlist, its live memberships in order."""

    playlist_id: str
    name: str
    attribute: int
    removed: bool
    #: Every node above this one, nearest first, as ``(id, name)``.
    ancestors: tuple[tuple[str, str], ...]
    rows: tuple[Row, ...] = ()

    @property
    def plain(self) -> bool:
        return self.attribute == PLAIN_PLAYLIST

    @property
    def top(self) -> tuple[str, str]:
        """The node at the top of the tree this playlist sits under, or itself."""
        return self.ancestors[-1] if self.ancestors else (self.playlist_id, self.name)

    def memberships(self) -> tuple[tuple[str, str], ...]:
        """``(content_id, row_id)`` in track order, what a stale check compares."""
        return tuple((row.content_id, row.row_id) for row in self.rows)


def _text(value: Any) -> str:
    return "" if value is None else str(value)


def _node(db: Any, playlist_id: str) -> tuple[str, str, str, int, bool] | None:
    from sqlalchemy import text

    found = db.session.execute(
        text(
            f"SELECT ID, Name, ParentID, Attribute, COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) "
            f"FROM {rb_writer.PLAYLIST_TABLE} WHERE ID = :id"
        ),
        {"id": str(playlist_id)},
    ).fetchone()
    if found is None:
        return None
    return (
        _text(found[0]),
        _text(found[1]),
        _text(found[2]),
        int(found[3] or 0),
        bool(found[4]),
    )


def read_playlist(db: Any, playlist_id: str) -> Playlist | None:
    """The node and its live memberships in track order, or None when no row has the id.

    The ancestors are walked by ``ParentID`` to the top, and a walk that meets
    a node twice stops, so a damaged tree cannot hang the read.
    """
    node = _node(db, playlist_id)
    if node is None:
        return None
    node_id, name, parent, attribute, removed = node
    ancestors: list[tuple[str, str]] = []
    seen = {node_id}
    while parent and parent != ROOT_PARENT and parent not in seen:
        seen.add(parent)
        above = _node(db, parent)
        if above is None:
            break
        ancestors.append((above[0], above[1]))
        parent = above[2]
    rows = members(db, node_id) if attribute == PLAIN_PLAYLIST and not removed else ()
    return Playlist(
        playlist_id=node_id,
        name=name,
        attribute=attribute,
        removed=removed,
        ancestors=tuple(ancestors),
        rows=rows,
    )


def members(db: Any, playlist_id: str) -> tuple[Row, ...]:
    """The live memberships of one playlist in track order, with their rows' facts.

    A membership whose content row is itself removed is left out, since
    rekordbox shows no such track in the playlist. Ties on ``TrackNo`` fall to
    the membership's own identifier, so one read always orders one way.
    """
    from sqlalchemy import text

    found = db.session.execute(
        text(
            f"SELECT s.ID, s.ContentID, c.Title, a.Name, c.{rb_writer.ISRC_COLUMN}, "
            f"c.FolderPath FROM {rb_writer.MEMBERSHIP_TABLE} s "
            f"JOIN {rb_writer.CONTENT_TABLE} c ON c.ID = s.ContentID "
            f"LEFT JOIN djmdArtist a ON a.ID = c.ArtistID "
            f"WHERE s.PlaylistID = :id "
            f"AND COALESCE(s.{rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 "
            f"AND COALESCE(c.{rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 "
            f"ORDER BY s.TrackNo, s.ID"
        ),
        {"id": str(playlist_id)},
    ).fetchall()
    return tuple(
        Row(
            row_id=_text(one[0]),
            content_id=_text(one[1]),
            title=_text(one[2]),
            artist=_text(one[3]),
            isrc=_text(one[4]),
            path=_text(one[5]),
        )
        for one in found
    )


def content(db: Any, content_ids: Iterable[str]) -> dict[str, Row]:
    """The live content rows among ``content_ids``, by id, with their facts.

    A row the library removed is left out, so a link to a track that has since
    left the collection is a link to nothing rather than a membership added to
    a row nobody can see.
    """
    from sqlalchemy import bindparam, text

    wanted = sorted({str(one) for one in content_ids if str(one)})
    if not wanted:
        return {}
    statement = text(
        f"SELECT c.ID, c.Title, a.Name, c.{rb_writer.ISRC_COLUMN}, c.FolderPath "
        f"FROM {rb_writer.CONTENT_TABLE} c LEFT JOIN djmdArtist a ON a.ID = c.ArtistID "
        f"WHERE c.ID IN :ids AND COALESCE(c.{rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
    ).bindparams(bindparam("ids", expanding=True))
    return {
        _text(one[0]): Row(
            row_id="",
            content_id=_text(one[0]),
            title=_text(one[1]),
            artist=_text(one[2]),
            isrc=_text(one[3]),
            path=_text(one[4]),
        )
        for one in db.session.execute(statement, {"ids": wanted}).fetchall()
    }


def rows_by_isrc(db: Any, fold) -> dict[str, tuple[str, ...]]:
    """Every live content row carrying an ISRC, by the folded code, ids in id order.

    ``fold`` is the caller's ISRC fold, so this layer does not import the
    matcher's. A code two rows carry maps to both, and choosing between them is
    the caller's refusal to make.
    """
    from sqlalchemy import text

    found: dict[str, list[str]] = {}
    for one in db.session.execute(
        text(
            f"SELECT ID, {rb_writer.ISRC_COLUMN} FROM {rb_writer.CONTENT_TABLE} "
            f"WHERE COALESCE({rb_writer.ISRC_COLUMN}, '') != '' "
            f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 ORDER BY ID"
        )
    ).fetchall():
        token = fold(_text(one[1]))
        if token:
            found.setdefault(token, []).append(_text(one[0]))
    return {token: tuple(ids) for token, ids in found.items()}


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Change:
    """What one pair's sync writes to its rekordbox playlist.

    ``before`` is the playlist's live memberships as the approved plan read
    them. ``order`` is every content id the playlist should hold once written,
    in the merged order, and a write numbers the live memberships to it.
    """

    playlist_id: str
    before: tuple[tuple[str, str], ...]
    adds: tuple[str, ...] = ()
    removes: tuple[str, ...] = ()
    order: tuple[str, ...] = ()

    @property
    def empty(self) -> bool:
        return not self.adds and not self.removes and self.order == tuple(
            dict.fromkeys(content_id for content_id, _row in self.before)
        )


@dataclass(frozen=True, slots=True)
class Written:
    """What one write did, read back from the database after its commit."""

    playlist_id: str
    added: int
    removed: int
    renumbered: int
    session_id: str
    read_back: tuple[Row, ...] = ()


def renumber(db: Any, playlist_id: str, order: Sequence[str]) -> int:
    """Number the live memberships one through N in ``order``. Returns how many moved.

    A track ``order`` does not name keeps its place after the named ones, in
    the order it stood, and a second live membership of one track goes after
    the first. Only a membership whose number changes is touched.
    """
    rank = {content_id: index for index, content_id in enumerate(dict.fromkeys(order))}
    live = [
        song
        for song in db.get_playlist_songs(PlaylistID=str(playlist_id))
        if not rb_writer.membership_removed(song)
    ]
    live.sort(key=lambda song: (int(song.TrackNo or 0), str(song.ID)))
    first: dict[str, Any] = {}
    named: list[Any] = []
    rest: list[Any] = []
    for song in live:
        key = str(song.ContentID)
        if key in rank and key not in first:
            first[key] = song
            named.append(song)
        else:
            rest.append(song)
    named.sort(key=lambda song: rank[str(song.ContentID)])
    now = datetime.now()
    moved = 0
    for number, song in enumerate([*named, *rest], start=1):
        if int(song.TrackNo or 0) != number:
            song.TrackNo = number
            song.updated_at = now
            moved += 1
    return moved


def _record_pair_commit(
    record: session.SessionRecord,
    source: str,
    *,
    added: int,
    changed: int,
    cfg: config.Config,
) -> None:
    """Record a commit on the session under the pair's own source, when one landed."""
    if added <= 0 and changed <= 0:
        return
    session.record_commit(
        record,
        source,
        session.ChangeSummary((session.TreeChange(tree=source, created=added, updated=changed),)),
        cfg,
    )


def apply(
    cfg: config.Config,
    db: Any,
    change: Change,
    *,
    source: str,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Write one pair's rekordbox side in one guarded commit, and read it back.

    ``source`` is the stable identifier the session records the commit under.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    now = read_playlist(db, change.playlist_id)
    if now is None or now.removed or not now.plain or now.memberships() != change.before:
        raise refuse(
            "decision-stale",
            f"the rekordbox playlist {change.playlist_id} is not as the approved plan "
            f"read it, so nothing was written to it; sync the pair again and approve "
            f"what it shows now",
            origin=_ORIGIN,
            detail={"playlist": change.playlist_id},
        )
    held = content(db, change.adds)
    gone = [content_id for content_id in change.adds if content_id not in held]
    if gone:
        raise refuse(
            "decision-stale",
            f"{len(gone)} track(s) the plan adds to the rekordbox playlist "
            f"{change.playlist_id} are no longer live rows of the collection, so "
            f"nothing was written to it",
            origin=_ORIGIN,
            detail={"playlist": change.playlist_id, "gone": gone},
        )

    added: list[str] = []
    removed: list[str] = []
    moved = 0
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
        try:
            playlist = db.get_playlist(ID=change.playlist_id)
            removed = rb_writer.remove_memberships(db, playlist, change.removes)
            added = rb_writer.add_memberships(db, playlist, change.adds)
            db.session.flush()
            moved = renumber(db, change.playlist_id, change.order)
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record_pair_commit(
                    record, source, added=len(added), changed=len(removed) + moved, cfg=cfg
                )
            raise
        _record_pair_commit(
            record, source, added=len(added), changed=len(removed) + moved, cfg=cfg
        )
        if added or removed or moved:
            convergence.record_fingerprint(cfg, db)
        session_id = record.session_id
    return Written(
        playlist_id=change.playlist_id,
        added=len(added),
        removed=len(removed),
        renumbered=moved,
        session_id=session_id,
        read_back=members(db, change.playlist_id),
    )


def assert_read_back(written: Written, change: Change) -> None:
    """Refuse an answer the database does not hold: the planned tracks, in order."""
    read = [row.content_id for row in written.read_back]
    wanted = list(dict.fromkeys(change.order))
    if list(dict.fromkeys(read)) != wanted:
        raise refuse(
            "session-committed-unverified",
            f"the rekordbox playlist {change.playlist_id} read back from the database "
            f"holds {len(read)} live track(s) and is not the {len(wanted)} the plan "
            f"named in the plan's order; the commit landed in session "
            f"{written.session_id} and this answer cannot be vouched for",
            origin=_ORIGIN,
            detail={"playlist_id": change.playlist_id, "planned": wanted, "read": read},
        )


def by_content(rows: Iterable[Row]) -> Mapping[str, Row]:
    """The first live membership of each track, by content id."""
    found: dict[str, Row] = {}
    for row in rows:
        found.setdefault(row.content_id, row)
    return found


__all__ = [
    "PLAIN_PLAYLIST",
    "ROOT_PARENT",
    "WORKFLOW",
    "Change",
    "Playlist",
    "Row",
    "Written",
    "apply",
    "assert_read_back",
    "by_content",
    "content",
    "members",
    "read_playlist",
    "renumber",
    "rows_by_isrc",
]
