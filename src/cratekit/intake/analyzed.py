"""Clear INBOX / Analyze of every row rekordbox has analysed (U166).

Every native landing adds each row it creates to one playlist directly under
the intake root, :data:`cratekit.intake.native.ANALYZE`, so the rekordbox visit
selects that one playlist and runs Analyze Track over it. Nothing else adds to
it. This is the other half: a row rekordbox has analysed leaves it, and a row
still waiting stays, so the next visit selects exactly what is owed.

WHAT ANALYSED MEANS, decided here and nowhere else. A row is cleared only when
its collection row is live, ``Analysed`` is set (nonzero) and
``AnalysisDataPath`` names a file. Each is rekordbox's own column and rekordbox
writes both on an analysis; a row lacking either is left in the playlist and
listed with why. NOTHING IS CLEARED ON A GUESS: a row that cannot be read, or
that is gone from the collection, stays where a person can see it.

A MEMBERSHIP IS REMOVED, NEVER A TRACK. The removal is
:func:`cratekit.core.rb_writer.remove_memberships`, the product's one soft
delete of a membership, under a commit that admits a removal in the membership
table and nowhere else. The content row, its file and every other playlist it
sits in are untouched, and the read back holds the playlist to exactly the rows
that were waiting.

THE PLAN IS TAKEN AGAIN ON THE WRITE HANDLE, the rotation's and the refill's
rule, and a digest that moved refuses with nothing written: an analysis that
finished between the approval and the apply is another plan.

Layer: modules. It opens no database of its own: the verb hands it a handle.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable

from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, rb_writer, session, snapshot, taxonomy, tree_registry
from cratekit.core.cause import refuse
from cratekit.intake import native, refill
from cratekit.write import trees

#: The session workflow a clear is recorded under.
WORKFLOW = "inbox-analyzed"

#: The session record field naming the playlist a clear wrote and what it removed.
RECORD_KEY = "inbox_analyzed"

#: What a planned row will do: leave the playlist, or stay in it.
CLEAR = "clear"
WAIT = "wait"

#: Why a row stays, each a sentence the screen and the envelope name it with.
NOT_ANALYSED = "rekordbox has not analysed it"
NO_ANALYSIS_PATH = "rekordbox marked it analysed and names no analysis file"
NO_ROW = "its collection row is missing"
ROW_REMOVED = "its collection row was removed"

_ORIGIN = ("intake.analyzed",)


@dataclass(frozen=True, slots=True)
class Member:
    """One track the playlist holds, and what the clear does with it."""

    content_id: str
    title: str
    action: str
    #: Why a row stays, empty for a row cleared.
    why: str = ""

    def identity(self) -> dict[str, Any]:
        return {
            "content_id": self.content_id,
            "title": self.title,
            "action": self.action,
            "why": self.why,
        }


@dataclass(frozen=True, slots=True)
class AnalyzedPlan:
    """What a clear removes and what it leaves, every row named, digested."""

    tree_id: str
    root_id: str
    root_name: str
    #: The playlist under the root, empty when the root holds none.
    playlist_id: str
    members: tuple[Member, ...]
    digest: str = ""

    def clears(self) -> tuple[str, ...]:
        return tuple(one.content_id for one in self.members if one.action == CLEAR)

    def waits(self) -> tuple[Member, ...]:
        return tuple(one for one in self.members if one.action == WAIT)

    @property
    def name(self) -> str:
        return f"{self.root_name} / {native.ANALYZE}"


@dataclass(frozen=True, slots=True)
class Cleared:
    """What a clear's one commit removed, read back from SQL after it."""

    session_id: str
    playlist_id: str
    removed: tuple[str, ...]
    #: Every content row read back live under the playlist after the commit.
    read_back: tuple[str, ...]


def identity(plan: AnalyzedPlan) -> dict[str, Any]:
    """What the digest covers: the root, the playlist and every row of it with its answer."""
    return {
        "kind": "inbox-analyzed",
        "tree": plan.tree_id,
        "root": plan.root_id,
        "playlist": plan.playlist_id,
        "members": [one.identity() for one in plan.members],
    }


def _member(db: Any, content_id: str) -> Member:
    """Read one row's answer off its collection row. A row that cannot answer stays."""
    row = db.get_content(ID=content_id)
    if row is None:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
    title = str(getattr(row, "Title", "") or "")
    removed = rb_writer.soft_deleted(
        row,
        message=(
            f"the collection row {content_id!r} in INBOX / {native.ANALYZE} cannot say "
            f"whether rekordbox removed it, so whether it was analysed was not read"
        ),
        origin=_ORIGIN,
        detail={"content_id": content_id},
    )
    if removed:
        return Member(content_id=content_id, title=title, action=WAIT, why=ROW_REMOVED)
    if not int(getattr(row, "Analysed", 0) or 0):
        return Member(content_id=content_id, title=title, action=WAIT, why=NOT_ANALYSED)
    if not str(getattr(row, "AnalysisDataPath", "") or "").strip():
        return Member(content_id=content_id, title=title, action=WAIT, why=NO_ANALYSIS_PATH)
    return Member(content_id=content_id, title=title, action=CLEAR)


def plan_clear(
    cfg: config.Config,
    db: Any,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
) -> AnalyzedPlan:
    """Plan the clear of the intake root's Analyze playlist. Reads, writes nothing."""
    del cfg
    tree_id = declared.intake.id
    root_id = refill.anchored_root(db, tree_id, registry)
    root = db.get_playlist(ID=root_id)
    playlist = native.analyze_playlist(db, str(root_id))
    members: list[Member] = []
    if playlist is not None:
        seen: set[str] = set()
        for content_id in live_members(db, str(playlist.ID)):
            if content_id in seen:
                continue
            seen.add(content_id)
            members.append(_member(db, content_id))
    plan = AnalyzedPlan(
        tree_id=tree_id,
        root_id=str(root_id),
        root_name=str(getattr(root, "Name", "") or ""),
        playlist_id=str(playlist.ID) if playlist is not None else "",
        members=tuple(members),
    )
    return replace(plan, digest=digest_of(identity(plan)))


def live_members(db: Any, playlist_id: str) -> tuple[str, ...]:
    """Every content row a playlist holds live, in its track order, a repeat kept."""
    songs = [
        song
        for song in db.get_playlist_songs(PlaylistID=str(playlist_id))
        if not rb_writer.membership_removed(song)
    ]
    songs.sort(key=lambda song: int(getattr(song, "TrackNo", 0) or 0))
    return tuple(str(song.ContentID) for song in songs)


def apply_clear(
    cfg: config.Config,
    db: Any,
    plan: AnalyzedPlan,
    *,
    declared: taxonomy.Taxonomy,
    analysis_roots: Iterable[Path | str],
) -> Cleared:
    """Remove the approved plan's analysed rows from the playlist in one guarded commit.

    THE SESSION SPINE IS CALLED, NOT REBUILT, as every database tree writer
    calls it: the gates with a record kept, a capture verified before anything
    is written, the analysis watch over the roots named, the commit witness,
    and the guarded commit, which admits a removal in the membership table and
    nowhere else.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    registry = tree_registry.read(cfg)
    again = plan_clear(cfg, db, declared=declared, registry=registry)
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            f"INBOX / {native.ANALYZE} or the collection is not as the approved plan "
            f"read it, so nothing was written; run it again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": plan.digest, "now": again.digest},
        )
    convergence.assert_tree_writable(cfg, db, plan.tree_id, registry)

    removed: list[str] = []
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
            playlist = db.get_playlist(ID=plan.playlist_id)
            # ONE PER ROW, though a track the playlist held twice has each of
            # its memberships marked, so the count is the plan's rows.
            removed = list(
                dict.fromkeys(rb_writer.remove_memberships(db, playlist, plan.clears()))
            )
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record_clear_commit(record, plan, removed, cfg)
            raise
        _record_clear_commit(record, plan, removed, cfg)
        convergence.record_fingerprint(cfg, db)
        read_back = live_members(db, plan.playlist_id)
        session_id = record.session_id
    return Cleared(
        session_id=session_id,
        playlist_id=plan.playlist_id,
        removed=tuple(removed),
        read_back=read_back,
    )


def _record_clear_commit(
    record: session.SessionRecord, plan: AnalyzedPlan, removed: list[str], cfg: config.Config
) -> None:
    """Record the commit under the intake tree, the playlist named and each row it removed.

    ``updated`` for each membership, the rotation's count for a node it
    removed, since the row is still there with its marker set and a restore
    that discards the session discards that change to it. ONLY WHEN A ROW WAS
    REMOVED, the landing's rule: a record saying the tree committed with no
    change would tell a restore otherwise.
    """
    if not removed:
        return
    record.detail[RECORD_KEY] = {
        "playlist": {"id": plan.playlist_id, "name": plan.name},
        "removed": list(removed),
    }
    session.record_commit(
        record,
        plan.tree_id,
        session.ChangeSummary((session.TreeChange(tree=plan.tree_id, updated=len(removed)),)),
        cfg,
    )


def assert_read_back(plan: AnalyzedPlan, cleared: Cleared) -> None:
    """Refuse an answer the database does not hold: the playlist holds exactly the waiting rows.

    EVERY ROW THE PLAN LEFT IS STILL THERE AND NO ROW IT CLEARED IS, read back
    from SQL after the commit, so a removal that took a waiting row or missed
    an analysed one is said rather than reported as done.
    """
    live = set(cleared.read_back)
    waiting = {one.content_id for one in plan.waits()}
    lost = sorted(waiting - live)
    kept = sorted(set(plan.clears()) & live)
    if lost or kept:
        raise refuse(
            "session-committed-unverified",
            f"{plan.name} ({plan.playlist_id}) read back from the database holds "
            f"{len(live)} live track(s): {len(lost)} the plan left are gone and "
            f"{len(kept)} it cleared are still there; the commit landed and this "
            f"answer cannot be vouched for",
            origin=_ORIGIN,
            detail={
                "playlist_id": plan.playlist_id,
                "lost": lost,
                "kept": kept,
                "read": list(cleared.read_back),
            },
        )


__all__ = [
    "CLEAR",
    "NOT_ANALYSED",
    "NO_ANALYSIS_PATH",
    "NO_ROW",
    "RECORD_KEY",
    "ROW_REMOVED",
    "WAIT",
    "WORKFLOW",
    "AnalyzedPlan",
    "Cleared",
    "Member",
    "apply_clear",
    "assert_read_back",
    "identity",
    "live_members",
    "plan_clear",
]
