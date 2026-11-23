"""The rekordbox side of a pair whose account playlist came first (U202).

An account playlist made inside a root folder a sync of every pair made (U198)
comes into rekordbox in the matching folder and is paired as the product's.
``sync/pair_discover.home_of`` says where; this makes one plain playlist of
the matched library rows, in the account's order.

**ADD ONLY, CONFINED FROM SQL.** One playlist row and its memberships, in a
folder already there, and nothing else. ``sync/twins.assert_confined`` reads
both node tables before the commit and refuses any other difference.

**THE SESSION SPINE IS CALLED, NOT REBUILT**: gates with a record, a verified
capture, the analysis watch, the commit witness and the guarded commit. The
parent, name and rows are read again on the write handle first, and any of
them moved since the plan refuses with nothing written.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

from cratekit.core import config, convergence, rb_writer, session, tree_registry
from cratekit.core.cause import refuse
from cratekit.sync import twins
from cratekit.sync.pair_discover import FOLDER, Home
from cratekit.write import playlist_pair, trees

_ORIGIN = ("sync", "pair_reverse")


def _stale(message: str, **detail: Any) -> Exception:
    return refuse(
        "decision-stale",
        message + "; sync the pairs again and approve what it shows now",
        origin=_ORIGIN,
        detail=dict(detail),
    )


def recheck(db: Any, home: Home, rows: Sequence[str]) -> None:
    """Refuse a write whose parent, name or rows moved since the plan was approved."""
    if home.parent_id:
        parent = playlist_pair.read_playlist(db, home.parent_id)
        if parent is None or parent.removed or parent.attribute != FOLDER:
            raise _stale(
                f"the rekordbox folder {home.where.rsplit(' / ', 1)[0]!r} the plan named is "
                f"no longer a live folder, so nothing was made",
                parent=home.parent_id,
            )
    taken = [
        row
        for row in db.get_playlist()
        if not rb_writer.node_removed(row)
        and str(getattr(row, "Name", "") or "") == home.name
        and (
            str(getattr(row, "ParentID", "") or "") == home.parent_id
            if home.parent_id
            else str(getattr(row, "ParentID", "") or "") in rb_writer.ROOT_PARENT_SENTINELS
        )
    ]
    if taken:
        raise _stale(
            f"{home.where!r} is taken by a node made since the plan, so nothing was made",
            name=home.name,
        )
    wanted = set(rows)
    gone = sorted(wanted - set(playlist_pair.content(db, wanted)))
    if gone:
        raise _stale(
            f"{len(gone)} row(s) the playlist {home.where!r} would hold are no longer "
            f"live rows of the collection, so nothing was made",
            gone=gone,
        )


def _record_commit(
    record: session.SessionRecord, source: str, *, created: int, cfg: config.Config
) -> None:
    if created <= 0:
        return
    session.record_commit(
        record,
        source,
        session.ChangeSummary((session.TreeChange(tree=source, created=created),)),
        cfg,
    )


def create(
    cfg: config.Config,
    db: Any,
    home: Home,
    rows: Sequence[str],
    *,
    source: str,
    analysis_roots: Iterable[Path | str],
    on_commit: Callable[[str], None] | None = None,
) -> playlist_pair.Written:
    """Make the playlist at ``home`` holding ``rows`` in order, in one guarded commit.

    ``source`` is what the session records the commit under. ``on_commit`` is
    told the new playlist's id once the commit landed, even if a later step
    raised, so the caller can pair it. The caller checks the read back.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    order = tuple(dict.fromkeys(str(row) for row in rows))
    recheck(db, home, order)
    # THE PLAYLIST IS NO TREE, so an out of band restore is detected and
    # marked, never refused, as the twins' writer does.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    added: list[str] = []
    playlist_id = ""
    with session.assert_gates(
        cfg, workflow=playlist_pair.WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
    ) as gates:
        record, capture = trees.attached_capture(gates, cfg, db)
        with rb_writer.commit_witness(db) as witness:
            try:
                before = rb_writer.node_tables(db)
                parent = db.get_playlist(ID=home.parent_id) if home.parent_id else None
                playlist = db.create_playlist(home.name, parent=parent)
                db.session.flush()
                playlist_id = str(playlist.ID)
                added = rb_writer.add_memberships(db, playlist, order)
                twins.assert_confined(
                    db,
                    before,
                    folders={},
                    playlists={playlist_id: (home.name, home.parent, frozenset(order))},
                )
                rb_writer.commit_guarded(db)
                if on_commit is not None:
                    on_commit(playlist_id)
            except BaseException:
                trees.rollback_quietly(db)
                if witness.landed:
                    _record_commit(record, source, created=len(added) + 1, cfg=cfg)
                    # A COMMIT THAT LANDED AND THEN RAISED still made the
                    # playlist, so the caller is told (U202).
                    if on_commit is not None and playlist_id:
                        on_commit(playlist_id)
                raise
        _record_commit(record, source, created=len(added) + 1, cfg=cfg)
        convergence.record_fingerprint(cfg, db)
        session_id = record.session_id
    return playlist_pair.Written(
        playlist_id=playlist_id,
        added=len(added),
        removed=0,
        renumbered=0,
        session_id=session_id,
        read_back=playlist_pair.members(db, playlist_id),
    )


__all__ = ["create", "recheck"]
