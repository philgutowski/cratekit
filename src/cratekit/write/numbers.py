"""Every playlist under this product's nodes numbered 1 to N again (U958).

rekordbox's Remove from Playlist takes out the row whose ``TrackNo`` equals the
selected row's shown position (sitting 107, A218), so a playlist whose live rows
are not numbered 1 to N loses the wrong track to a removal by hand. A removal
this product makes closes its playlist up at the commit
(:func:`rb_writer.close_gaps`); this repair is the same rule over the playlists
earlier removals left gapped, with nothing removed.

**THE SCOPE**: every live ordinary playlist at or under a node this product
writes at the top of the tree (the taxonomy's tree, intake, inspiration,
catalog and long tracks nodes, each ``Custom Playlists <year>`` twin folder),
the folder holding the favourites class's source playlist, and any playlist
named by the caller;
never another app's folder (U185). **THE PLAN** lists each playlist in scope
whose live rows are not 1 to N, with its count and how far its numbers run;
**THE DIGEST** covers every row the write moves and where to. A playlist whose
order cannot be read is held back and shown, never written.

Layer: write.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    foreign_tree,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import refuse
from cratekit.write import genre_favorites, trees

#: The session workflow the repair is recorded under.
WORKFLOW = "repair-numbers"

#: The key its commit is recorded under on the session: rows changed.
CHANGE_KEY = "playlists.numbers"

#: The twin folders ``sync twins`` makes at the top of the tree (U149), ``Custom Playlists 2026``.
TWIN_FOLDER = re.compile(r"Custom Playlists [0-9]{4}")

#: How a path from the top of the tree is shown, folder by folder.
_PATH_SEPARATOR = " / "

_ORIGIN = ("write", "numbers")


@dataclass(frozen=True, slots=True)
class Item:
    """One playlist the repair numbers 1 to N."""

    playlist_id: str
    #: Its path from the top of the tree, ``BY GENRE + ENERGY / Tech House / High``.
    path: str
    #: Live rows, and the lowest and highest live ``TrackNo`` now.
    rows: int
    lowest: int | None
    highest: int | None
    #: Marked rows on a place other than 0, moved to 0 with the rest.
    marked: int
    #: ``(membership id, TrackNo now, TrackNo after)`` for every row that moves.
    moves: tuple[tuple[str, int, int], ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "action": "renumber",
            "playlist": self.path,
            "row": self.playlist_id,
            "rows": self.rows,
            "from": self.lowest,
            "to": self.highest,
            "marked": self.marked,
            "moves": len(self.moves),
        }


@dataclass(frozen=True, slots=True)
class Held:
    """A playlist in scope whose order cannot be read, so it is never written."""

    playlist_id: str
    path: str
    #: The membership rows whose marker or place cannot be read.
    rows: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class NumbersPlan:
    """The playlists in scope that are not 1 to N, and what each moves."""

    items: tuple[Item, ...]
    #: Playlists read in scope, the ones already 1 to N included.
    scanned: int
    held: tuple[Held, ...] = ()
    #: The names the caller asked for, as asked.
    named: tuple[str, ...] = ()
    digest: str = ""

    @property
    def writes(self) -> bool:
        return bool(self.items)

    def identity(self) -> dict[str, Any]:
        """What the digest covers: every row that moves and where to, and the names asked."""
        return {
            "kind": WORKFLOW,
            "named": list(self.named),
            "items": [[one.playlist_id, [list(move) for move in one.moves]] for one in self.items],
        }


def _playlists(db: Any) -> list[tuple[str, str, str, int, bool]]:
    """``(ID, Name, ParentID, Attribute, live)`` for every playlist row, from SQL."""
    from sqlalchemy import text

    marker = rb_writer.SOFT_DELETE_COLUMN
    found = db.session.execute(
        text(
            f'SELECT "ID", "Name", "ParentID", "Attribute", COALESCE("{marker}", 1) '
            f'FROM "{rb_writer.PLAYLIST_TABLE}"'
        )
    ).fetchall()
    return [
        (
            str(row[0]),
            "" if row[1] is None else str(row[1]),
            "" if row[2] is None else str(row[2]),
            -1 if row[3] is None else int(row[3]),
            not bool(row[4]),
        )
        for row in found
    ]


def product_root_names(declared: taxonomy.Taxonomy) -> frozenset[str]:
    """The names of the nodes this product writes at the top of the tree, by the taxonomy."""
    nodes = (
        declared.tree, declared.intake, declared.inspiration, declared.catalog, declared.long_tracks,
    )
    return frozenset(str(node.display) for node in nodes if node is not None)


def favourites_source(declared: taxonomy.Taxonomy) -> str | None:
    """The playlist the taxonomy's favourites class reads, or None when it declares none.

    The favourites verbs fall back to the account's default playlist name,
    which lives above this layer; with no class declared, the folder of the
    favourites is not in scope here and is named with ``--playlist`` instead.
    """
    sub = genre_favorites.favorites_class(declared)
    if sub is not None and sub.signal_playlist:
        return str(sub.signal_playlist)
    return None


def scope(
    db: Any, declared: taxonomy.Taxonomy, named: Sequence[str] = ()
) -> dict[str, str]:
    """Every live ordinary playlist the repair reads, by id, to its path from the top.

    REFUSED BY NAME: a name the caller gave that no live ordinary playlist outside
    another app's folder carries.
    """
    rows = _playlists(db)
    by_id = {row[0]: row for row in rows}
    _roots, foreign = foreign_tree.ids_of((row[0], row[1], row[2], row[3]) for row in rows)
    children: dict[str, list[str]] = {}
    for key, _name, parent, _attribute, live in rows:
        if live and key not in foreign:
            children.setdefault(parent, []).append(key)

    def path(key: str) -> str:
        names: list[str] = []
        seen: set[str] = set()
        while key in by_id and key not in seen:
            seen.add(key)
            names.append(by_id[key][1])
            key = by_id[key][2]
        return _PATH_SEPARATOR.join(reversed(names))

    def under(key: str) -> set[str]:
        found: set[str] = set()
        queue = [key]
        while queue:
            node = queue.pop()
            if node in found:
                continue
            found.add(node)
            queue.extend(children.get(node, ()))
        return found

    tops = product_root_names(declared)
    source = favourites_source(declared)
    reached: set[str] = set()
    for key, name, parent, _attribute, live in rows:
        if not live or key in foreign:
            continue
        at_top = parent in rb_writer.ROOT_PARENT_SENTINELS
        if at_top and (name in tops or TWIN_FOLDER.fullmatch(name)):
            reached |= under(key)
        if source is not None and name == source and int(by_id[key][3]) == 0:
            # The folder that holds the favourites, or the playlist alone at the top.
            reached |= under(key if at_top else parent)
    asked = tuple(dict.fromkeys(str(one) for one in named))
    unknown: list[str] = []
    for wanted in asked:
        hits = {
            key
            for key, name, _parent, attribute, live in rows
            if name == wanted and live and attribute == 0 and key not in foreign
        }
        if not hits:
            unknown.append(wanted)
        reached |= hits
    if unknown:
        raise refuse(
            "decision-stale",
            f"no live playlist outside another app's folder is named "
            f"{', '.join(repr(one) for one in unknown)}, so nothing was planned; name a "
            f"playlist as rekordbox shows it",
            origin=_ORIGIN,
            detail={"named": unknown},
        )
    return {
        key: path(key)
        for key in sorted(reached)
        if key in by_id and by_id[key][3] == 0 and by_id[key][4] and key not in foreign
    }


def plan(db: Any, declared: taxonomy.Taxonomy, *, named: Sequence[str] = ()) -> NumbersPlan:
    """The playlists in scope whose live rows are not 1 to N, planned on this handle."""
    paths = scope(db, declared, named)
    rows = rb_writer.membership_rows(db, paths) if paths else []
    moved = rb_writer.contiguous_positions(rows)
    unreadable = rb_writer.unplaceable(rows)
    items: list[Item] = []
    for playlist, read in sorted(rb_writer.numbering(rows).items(), key=lambda kv: paths[kv[0]]):
        if read.contiguous or playlist in unreadable:
            continue
        items.append(
            Item(
                playlist_id=playlist,
                path=paths[playlist],
                rows=read.rows,
                lowest=read.lowest,
                highest=read.highest,
                marked=read.marked_placed,
                moves=tuple(
                    sorted(
                        (key, was, now)
                        for key, (owner, was, now) in moved.items()
                        if owner == playlist
                    )
                ),
            )
        )
    held = tuple(
        Held(playlist_id=key, path=paths[key], rows=tuple(found))
        for key, found in sorted(unreadable.items(), key=lambda kv: paths[kv[0]])
    )
    planned = NumbersPlan(
        items=tuple(items), scanned=len(paths), held=held, named=tuple(dict.fromkeys(named))
    )
    return replace(planned, digest=digest_of(planned.identity()))


@dataclass(frozen=True, slots=True)
class Written:
    """What one repair wrote, and what the playlists read back after its commit."""

    playlists: int
    moved: int
    session_id: str
    disagreements: tuple[str, ...] = ()


def _record_numbers_commit(record: session.SessionRecord, moved: int, cfg: config.Config) -> None:
    """Record the commit on the session, as rows changed under the repair's key."""
    if moved > 0:
        session.record_commit(
            record,
            CHANGE_KEY,
            session.ChangeSummary((session.TreeChange(tree=CHANGE_KEY, created=0, updated=moved),)),
            cfg,
        )


def read_back(db: Any, approved: NumbersPlan) -> tuple[str, ...]:
    """Each planned playlist that does not read 1 to N, with no marked row on a place, from SQL."""
    ids = [one.playlist_id for one in approved.items]
    paths = {one.playlist_id: one.path for one in approved.items}
    read = rb_writer.numbering(rb_writer.membership_rows(db, ids)) if ids else {}
    found: list[str] = []
    for key in ids:
        one = read.get(key)
        if one is None or not one.contiguous or one.marked_placed:
            found.append(
                f"{paths[key]!r} reads "
                + (
                    "no rows"
                    if one is None
                    else f"{one.rows} live row(s) from {one.lowest} to {one.highest}, "
                    f"{one.marked_placed} marked row(s) on a place"
                )
            )
    return tuple(found)


def apply(
    cfg: config.Config,
    db: Any,
    approved: NumbersPlan,
    *,
    declared: taxonomy.Taxonomy,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Number every approved playlist 1 to N in one guarded commit, and read it back.

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST and a digest that moved
    refuses ``decision-stale``. The write is :func:`rb_writer.close_gaps`, run
    by :func:`rb_writer.commit_guarded` over the playlists recorded here and
    proven there from SQL before the commit.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    again = plan(db, declared, named=approved.named)
    if again.digest != approved.digest:
        raise refuse(
            "decision-stale",
            "the playlists to number are not as the approved plan read them, so nothing "
            "was written; run it again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": approved.digest, "now": again.digest},
        )
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    moved = sum(len(one.moves) for one in again.items)
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record, _capture = trees.attached_capture(gates, cfg, db)
        try:
            for one in again.items:
                rb_writer.record_touched(db, one.playlist_id)
            rb_writer.commit_guarded(db)
        except BaseException:
            trees.rollback_quietly(db)
            # An exception is not proof nothing landed; the witness is.
            if witness.landed:
                _record_numbers_commit(record, moved, cfg)
            raise
        _record_numbers_commit(record, moved, cfg)
        if moved:
            convergence.record_fingerprint(cfg, db)
        session_id = record.session_id
    return Written(
        playlists=len(again.items),
        moved=moved,
        session_id=session_id,
        disagreements=read_back(db, again),
    )


def assert_read_back(written: Written) -> None:
    """Refuse an answer the database does not hold."""
    if written.disagreements:
        raise refuse(
            "session-committed-unverified",
            "the playlists read back from the database are not numbered 1 to N: "
            + "; ".join(written.disagreements)
            + "; the commit landed and this answer cannot be vouched for",
            origin=_ORIGIN,
            detail={"disagreements": list(written.disagreements), "session": written.session_id},
        )


def summary(planned: NumbersPlan) -> Mapping[str, Any]:
    """The plan's counts, for the gate's facts and the envelope's totals."""
    return {
        "count": len(planned.items),
        "playlists_read": planned.scanned,
        "moves": sum(len(one.moves) for one in planned.items),
        "held": len(planned.held),
    }


__all__ = [
    "CHANGE_KEY",
    "Held",
    "Item",
    "NumbersPlan",
    "TWIN_FOLDER",
    "WORKFLOW",
    "Written",
    "apply",
    "assert_read_back",
    "favourites_source",
    "plan",
    "product_root_names",
    "read_back",
    "scope",
    "summary",
]
