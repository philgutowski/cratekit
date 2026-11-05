"""The rekordbox side of a pair whose account playlist came first (U202).

Decided by Phillip on 2026-11-04: a playlist he makes on the account inside one
of the root folders a sync of every pair made (U198) comes into rekordbox at
the next ``crate sync pair``, in the matching rekordbox folder, and is paired as
one the product made. ``sync/pair_discover.home_of`` says where it goes; this
module makes it: one plain playlist, holding the library rows the account
playlist's tracks matched, in the account's order.

**ADD ONLY, CONFINED FROM SQL.** One playlist row and its memberships are
made, in a folder that is already there, and nothing else: no folder is made,
and no row of the collection, no other playlist and no other membership is
touched. The write is judged before its commit by the twins' confinement check
(``sync/twins.assert_confined``), which reads both node tables from SQL and
refuses any difference the playlist made does not explain.

**THE SESSION SPINE IS CALLED, NOT REBUILT**, as every database membership
writer calls it: the gates with a record kept, a capture verified before
anything is written, the analysis watch over the roots named, the commit
witness, and the guarded commit. The parent, the name and the rows are read
again on the write handle first, and a parent gone, a name taken or a row gone
since the plan was approved refuses with nothing written.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

from cratekit.core import config, convergence, rb_writer, session, snapshot, tree_registry
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

    ``source`` is the stable identifier the session records the commit under.
    ``on_commit`` is told the new playlist's identifier once the commit has
    landed, whether ``commit_guarded`` returned or raised after the witness
    saw it land, so a caller can pair it even when a later step fails. The playlist
    is read back after the commit; the caller checks it.
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
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)
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
                trees._rollback_quietly(db)
                if witness.landed:
                    _record_commit(record, source, created=len(added) + 1, cfg=cfg)
                    # A COMMIT THAT LANDED AND THEN RAISED still made the
                    # playlist (U202, from the second review), so the caller
                    # is told, as the session record is, by the witness.
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
