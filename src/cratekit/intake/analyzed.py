"""Clear INBOX / Analyze of every row rekordbox has analysed (U166).

Every native landing adds each row it creates to one playlist under the intake
root, :data:`cratekit.intake.native.ANALYZE`, which the rekordbox visit
analyses. A row rekordbox has analysed leaves it and a row still waiting
stays, so the next visit selects exactly what is owed.

WHAT ANALYSED MEANS, decided here and nowhere else: the collection row is live,
``Analysed`` is set and ``AnalysisDataPath`` names a file, both of which
rekordbox writes on an analysis. NOTHING IS CLEARED ON A GUESS: a row that
cannot be read, or is gone, stays where a person can see it.

A MEMBERSHIP IS REMOVED, NEVER A TRACK, by
:func:`cratekit.core.rb_writer.remove_memberships` under a commit admitting a
removal in the membership table only, and the read back holds the playlist to
exactly the rows that were waiting. The plan is taken again on the write
handle, so an analysis finished after the approval is another plan.

Layer: modules. It opens no database of its own: the verb hands it a handle.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable

from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import refuse
from cratekit.intake import native, refill, rotate
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


def member(db: Any, content_id: str) -> Member:
    """Read one row's answer off its collection row. A row that cannot answer stays.

    Public so ``crate analyze check`` asks the one rule rather than a second
    (U167); the judgment is :func:`judge`, for a caller holding the row (U259).
    """
    return judge(content_id, db.get_content(ID=content_id))


def judge(content_id: str, row: Any) -> Member:
    """Judge one collection row already in hand; ``None`` is a row the collection lacks.

    :func:`member`'s judgment split from its read (U259), not a second rule. A
    row whose removal marker cannot be read refuses here, for both.
    """
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
    playlist = native.analyze_playlist(db, str(root_id))
    held = live_members(db, str(playlist.ID)) if playlist is not None else ()
    members = [member(db, content_id) for content_id in dict.fromkeys(held)]
    plan = AnalyzedPlan(
        tree_id=tree_id,
        root_id=str(root_id),
        root_name=str(getattr(db.get_playlist(ID=root_id), "Name", "") or ""),
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

    The session spine is every tree writer's; the guarded commit admits a
    removal in the membership table and nowhere else.
    """
    watched = rotate.watched_roots(analysis_roots)
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
        record, capture = trees.attached_capture(gates, cfg, db)
        try:
            playlist = db.get_playlist(ID=plan.playlist_id)
            # ONE PER ROW: a track held twice has both memberships marked.
            removed = list(
                dict.fromkeys(rb_writer.remove_memberships(db, playlist, plan.clears()))
            )
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
        except BaseException:
            trees.rollback_quietly(db)
            if witness.landed:
                _record_clear_commit(record, plan, removed, cfg)
            raise
        _record_clear_commit(record, plan, removed, cfg)
        convergence.record_fingerprint(cfg, db)
        read_back = live_members(db, plan.playlist_id)
        session_id = record.session_id
    return Cleared(session_id, plan.playlist_id, tuple(removed), read_back)


def _record_clear_commit(
    record: session.SessionRecord, plan: AnalyzedPlan, removed: list[str], cfg: config.Config
) -> None:
    """Record the commit under the intake tree, the playlist named and each row it removed.

    ``updated`` per membership, whose row stays with its marker set; only when
    a row was removed, since a no change commit would mislead a restore.
    """
    if not removed:
        return
    record.detail[RECORD_KEY] = {
        "playlist": {"id": plan.playlist_id, "name": plan.name},
        "removed": list(removed),
    }
    change = session.TreeChange(tree=plan.tree_id, updated=len(removed))
    session.record_commit(record, plan.tree_id, session.ChangeSummary((change,)), cfg)


def assert_read_back(plan: AnalyzedPlan, cleared: Cleared) -> None:
    """Refuse an answer the database does not hold: the playlist holds exactly the waiting rows."""
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
