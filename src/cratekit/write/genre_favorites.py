"""The genre Favorites: one Favorites playlist in every genre folder, mirroring All Favorites (U119).

Every genre folder under the routing tree holds one playlist named Favorites
whose members are exactly that folder's tracks also in All Favorites, and it
MIRRORS: a track leaving All Favorites leaves at the next refresh, and one added
by hand is taken out. The declaration is a sub class derived from a playlist
beside the vocal class, so nothing here carries a display name (R19); an
undeclared class, and a source that is absent, doubled or empty, refuse by name
rather than empty every Favorites. A favourite files by the folder it already
sits in, never by its tag.

The plan digests the target state, not the adds, so a stopped run re-plans to
the same digest (R-788). Additions and removals are two commits, the second
admitting the membership table alone, so a run stopped between them has taken
nothing out. Only the refresh verb removes; an adoption's end runs the additive
half. Layer: write; names no verb.
"""

from __future__ import annotations

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
    taxonomy_upgrade,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.write import tree_read, trees

#: The session workflow a refresh is recorded under, its own, so a session that
#: removed a favourite is told apart from a membership write and a move.
WORKFLOW = "genre-favorites"

#: The dimension a convergence report names as not compared when the source
#: playlist could not be read, beside the vocal one.
FAVORITES_DIMENSION = "favorites"

#: The refusal reasons this module owns, reserved in the cause vocabulary.
CLASS_UNDECLARED = "favorites-class-undeclared"
SOURCE_MISSING = "favorites-source-missing"

_ORIGIN = ("genre_favorites",)


# ---------------------------------------------------------------------------
# The declaration
# ---------------------------------------------------------------------------


def favorites_class(declared: taxonomy.Taxonomy) -> taxonomy.SubClass | None:
    """The one additive sub class derived from a playlist, or None when the taxonomy declares none."""
    for entry in declared.sub_classes:
        if entry.additive and entry.signal == taxonomy.SIGNAL_PLAYLIST:
            return entry
    return None


def require_class(declared: taxonomy.Taxonomy) -> taxonomy.SubClass:
    """The declared class, or the refusal that says to declare it."""
    found = favorites_class(declared)
    if found is None:
        raise refuse(
            CLASS_UNDECLARED,
            "this library's taxonomy declares no sub class derived from a playlist, "
            "so there is no genre Favorites to refresh; the class is declared beside "
            "the vocal one and this verb will not invent a playlist in every folder",
            remedy=Remedy.FIX_CONFIG_VALUES,
            steps=(
                f"run {taxonomy_upgrade.VERB}, which adds the class the shipped template "
                "declares and states its schema version, keeping the copy as it was "
                "beside it",
                "or add a [[sub_class]] with signal = \"playlist\" and the playlist it "
                "mirrors in signal_playlist to the library's active taxonomy by hand, as "
                "the shipped template carries, and state schema_version = 4",
            ),
            origin=_ORIGIN,
        )
    return found


def undeclared_note(schema_version: int | None = None) -> dict[str, str]:
    """The note a verb that ran the genre Favorites step carries when the class was undeclared (U132).

    The skip is named, with the refusal's own code, never silent. One wording
    for every surface.
    """
    stated = f"states schema_version {schema_version} and " if schema_version is not None else ""
    return {
        "code": CLASS_UNDECLARED,
        "message": (
            f"the genre Favorites step was skipped: this library's taxonomy {stated}"
            f"declares no sub class derived from a playlist, so no genre folder's "
            f"Favorites was written or checked; {taxonomy_upgrade.VERB} adds the class "
            f"the shipped template declares, and doctor's taxonomy.schema names what "
            f"else the copy lacks"
        ),
    }


def undeclared_warnings(declared: taxonomy.Taxonomy) -> tuple[dict[str, str], ...]:
    """:func:`undeclared_note` for a declaration without the class, and nothing for one with it."""
    if favorites_class(declared) is not None:
        return ()
    return (undeclared_note(declared.schema_version),)


# ---------------------------------------------------------------------------
# The source
# ---------------------------------------------------------------------------


def source_playlist(db: Any, name: str) -> Any:
    """The one live playlist named ``name`` anywhere in the library, or the refusal.

    None, several and empty refuse alike, under one reason. Only a PLAIN
    playlist matches, since a smart playlist holds no membership rows.
    """
    live = [
        row
        for row in list(db.get_playlist(Name=name))
        if int(getattr(row, "Attribute", -1) or 0) == 0 and not rb_writer.node_removed(row)
    ]
    # U185. One another app pushed into its own folder is not the source,
    # whatever it is called, for the reason the Favorites home gives.
    live = foreign_tree.outside(live, list(db.get_playlist()))
    if len(live) == 1 and live_members(db, str(live[0].ID)):
        return live[0]
    if len(live) == 1:
        message = (
            f"the playlist {name!r} holds no live track, so there is nothing for the "
            f"genre Favorites to mirror and a refresh would empty every one of them; "
            f"nothing was written"
        )
        steps = (
            f"heart something into {name!r} in rekordbox first, or name the "
            f"playlist that holds the favourites in the class's signal_playlist",
        )
        detail: dict[str, Any] = {"playlist": name, "id": str(live[0].ID)}
    elif not live:
        message = (
            f"this library holds no live playlist named {name!r}, which is the one "
            f"signal the genre Favorites mirror, so nothing was written; a refresh "
            f"over an absent source would empty every Favorites"
        )
        steps = (
            f"make the playlist {name!r} in rekordbox, or name the playlist that "
            f"holds the favourites in the class's signal_playlist",
        )
        detail = {"playlist": name}
    else:
        message = (
            f"this library holds {len(live)} live playlists named {name!r}, so the genre "
            f"Favorites have no one source to mirror; nothing was written"
        )
        steps = ("merge or rename the playlists in rekordbox so one carries the name",)
        detail = {"playlist": name, "count": len(live)}
    raise refuse(
        SOURCE_MISSING, message, remedy=Remedy.FIX_CONFIG_VALUES, steps=steps,
        origin=_ORIGIN, detail=detail,
    )


def live_members(db: Any, playlist_id: str) -> frozenset[str]:
    """The content ids a playlist holds live, the soft deleted rows left out (R-758)."""
    return frozenset(
        str(song.ContentID)
        for song in db.get_playlist_songs(PlaylistID=str(playlist_id))
        if not rb_writer.membership_removed(song)
    )


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FolderPlan:
    """One genre folder: what its Favorites should hold, and what it holds now."""

    bucket: str
    folder_id: str
    folder_display: str
    #: The Favorites playlist's row, or empty when the write creates it.
    playlist_id: str
    playlist_display: str
    #: The members the folder's other playlists hold, live.
    members: tuple[str, ...]
    #: ``members`` intersected with the source: what Favorites should hold.
    wanted: tuple[str, ...]
    #: What Favorites holds now, live.
    present: tuple[str, ...]

    @property
    def adds(self) -> tuple[str, ...]:
        held = set(self.present)
        return tuple(one for one in self.wanted if one not in held)

    @property
    def removes(self) -> tuple[str, ...]:
        kept = set(self.wanted)
        return tuple(one for one in self.present if one not in kept)

    def identity(self) -> dict[str, Any]:
        """What the digest covers for this folder: the target, and what leaves.

        The adds shrink as an apply proceeds and are not digested (R-788); the
        removes do not move until their commit lands.
        """
        return {
            "bucket": self.bucket,
            "folder": self.folder_id,
            "wanted": list(self.wanted),
            "removes": list(self.removes),
        }


@dataclass(frozen=True, slots=True)
class RefreshPlan:
    """Every genre folder's Favorites, planned against one source on one handle."""

    tree_id: str
    root_id: str
    sub_class: str
    source_name: str
    source_id: str
    #: How many tracks the source holds live.
    favourites: int
    folders: tuple[FolderPlan, ...]
    #: Folders under the root that no declared bucket's name or record claims,
    #: and folders two buckets would claim. Listed, never written.
    unclaimed: tuple[str, ...] = ()
    digest: str = ""

    @property
    def adds(self) -> int:
        return sum(len(folder.adds) for folder in self.folders)

    @property
    def removes(self) -> int:
        return sum(len(folder.removes) for folder in self.folders)

    @property
    def creates(self) -> int:
        return sum(1 for folder in self.folders if not folder.playlist_id and folder.wanted)

    @property
    def writes(self) -> bool:
        return bool(self.adds or self.removes)


def identity(plan: RefreshPlan) -> dict[str, Any]:
    """What the digest covers: the source, the class, and each folder's target state."""
    return {
        "kind": "genre-favorites",
        "tree": plan.tree_id,
        "root": plan.root_id,
        "class": plan.sub_class,
        "source": plan.source_id,
        "folders": [folder.identity() for folder in plan.folders],
    }


def _root_exists(db: Any):
    return lambda root_id: db.get_playlist(ID=root_id) is not None


def _recorded(
    entries: Sequence[Any], by_folder: Mapping[str, Any], sub_id: str
) -> tuple[dict[str, str], dict[str, str], set[str]]:
    """Each bucket's recorded folder and Favorites playlist, and the torn buckets.

    One folder per bucket in the record, or none: a bucket whose live entries
    name two folders is torn, and nothing is written there.
    """
    recorded_folder: dict[str, str] = {}
    recorded_playlist: dict[str, str] = {}
    torn: set[str] = set()
    for entry in entries:
        if entry.folder_id not in by_folder:
            continue
        held = recorded_folder.setdefault(entry.bucket, entry.folder_id)
        if held != entry.folder_id:
            torn.add(entry.bucket)
        if entry.sub == sub_id and held == entry.folder_id:
            recorded_playlist[entry.bucket] = entry.playlist_id
    return recorded_folder, recorded_playlist, torn


def _bound(
    buckets: Sequence[taxonomy.Bucket],
    entries: Sequence[Any],
    display_of: Mapping[str, str],
    recorded_folder: Mapping[str, str],
    torn: set[str],
) -> tuple[dict[str, str], set[str], list[str]]:
    """Each bucket's folder, the folders claimed, and the folders left unclaimed.

    The record first, then by name only for a folder no record claims, so one
    folder is never two buckets'.
    """
    bound: dict[str, str] = {
        bucket.id: recorded_folder[bucket.id]
        for bucket in buckets
        if bucket.id in recorded_folder and bucket.id not in torn
    }
    claimed: set[str] = set(bound.values())
    unclaimed: list[str] = []
    for bucket in buckets:
        if bucket.id in torn:
            named = sorted(
                {entry.folder_id for entry in entries if entry.bucket == bucket.id}
                & set(display_of)
            )
            unclaimed.extend(
                f"{display_of[fid]} (row {fid}, the record names it for {bucket.display} "
                f"beside another folder)"
                for fid in named
            )
            claimed.update(named)
            continue
        if bucket.id in bound:
            continue
        named = [
            fid
            for fid, display in display_of.items()
            if display == bucket.display and fid not in claimed
        ]
        if len(named) > 1:
            unclaimed.extend(f"{bucket.display} (row {fid})" for fid in named)
            claimed.update(named)
            continue
        if named:
            bound[bucket.id] = named[0]
            claimed.add(named[0])
    return bound, claimed, unclaimed


def plan_refresh(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
) -> RefreshPlan:
    """Plan every genre folder's Favorites against the database on this handle.

    A folder is bound as the rebuild binds a destination, by its recorded node
    first. A folder no bucket claims, and a name two live folders carry, are
    listed as unclaimed and left alone.
    """
    sub = require_class(declared)
    tree_id = declared.tree.id
    root_id = tree_registry.anchored_root(tree_id, registry, root_exists=_root_exists(db))
    source = source_playlist(db, sub.signal_playlist)
    favourites = live_members(db, str(source.ID))
    nodes = tuple(node for node in tree_read.read_tree(db, root_id) if not node.removed)
    record = convergence.read(cfg).tree(tree_id)

    by_folder: dict[str, list[tree_read.TreeNode]] = {}
    display_of: dict[str, str] = {}
    for node in nodes:
        by_folder.setdefault(node.folder_id, []).append(node)
        display_of[node.folder_id] = node.folder_display
    entries = () if record is None else tuple(record.nodes)
    recorded_folder, recorded_playlist, torn = _recorded(entries, by_folder, sub.id)
    # Every bucket, ``present_in`` unread: no tree writer reads it, and a second
    # reader would give a second answer to where a class sits.
    buckets = tuple(declared.buckets)
    bound, claimed, unclaimed = _bound(buckets, entries, display_of, recorded_folder, torn)

    folders: list[FolderPlan] = []
    for bucket in buckets:
        folder_id = bound.get(bucket.id)
        if folder_id is None:
            continue
        children = by_folder[folder_id]
        favorites_node = next(
            (node for node in children if node.playlist_id == recorded_playlist.get(bucket.id)),
            None,
        ) or next((node for node in children if node.playlist_display == sub.display), None)
        members: set[str] = set()
        for node in children:
            if favorites_node is not None and node.playlist_id == favorites_node.playlist_id:
                continue
            members.update(node.content_ids)
        # The walk's own reading, under the same soft delete rule.
        present = favorites_node.content_ids if favorites_node is not None else frozenset()
        folders.append(
            FolderPlan(
                bucket=bucket.id,
                folder_id=folder_id,
                folder_display=display_of[folder_id],
                playlist_id=favorites_node.playlist_id if favorites_node is not None else "",
                playlist_display=sub.display,
                members=tuple(sorted(members)),
                wanted=tuple(sorted(members & favourites)),
                present=tuple(sorted(present)),
            )
        )
    unclaimed.extend(f"{display_of[fid]} (row {fid})" for fid in by_folder if fid not in claimed)
    planned = RefreshPlan(
        tree_id=tree_id, root_id=str(root_id), sub_class=sub.id,
        source_name=sub.signal_playlist, source_id=str(source.ID), favourites=len(favourites),
        folders=tuple(folders), unclaimed=tuple(sorted(unclaimed)),
    )
    return replace(planned, digest=digest_of(identity(planned)))


def placements(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    rows: Sequence[trees.ContentRow],
) -> tuple[tuple[tree_read.DeclaredPlacement, ...], tuple[str, ...]]:
    """The genre Favorites as declared placements, for the rebuild and the check.

    The location is the row's recorded path. A source that cannot be read
    places nothing and names :data:`FAVORITES_DIMENSION` as not compared.
    """
    sub = favorites_class(declared)
    if sub is None:
        return (), ()
    try:
        plan = plan_refresh(cfg, db, declared, registry)
    except (rb_writer.RekordboxUnavailable, tree_registry.TreeModeRefused):
        raise
    except Exception as exc:  # noqa: BLE001 - every refusal of the source is one gap
        reason = getattr(getattr(exc, "cause", None), "reason", None)
        if reason != SOURCE_MISSING:
            raise
        return (), (FAVORITES_DIMENSION,)
    recorded = {row.content_id: row.recorded for row in rows if not row.deleted}
    out = [
        tree_read.DeclaredPlacement(recorded[content_id], folder.bucket, sub.id)
        for folder in plan.folders
        for content_id in folder.wanted
        if content_id in recorded
    ]
    return tuple(out), ()


# ---------------------------------------------------------------------------
# The screen
# ---------------------------------------------------------------------------


def payload(plan: RefreshPlan) -> dict[str, Any]:
    """The plan as the gate shows it: one item per folder, adds and removes named."""
    items = [
        {
            "action": "refresh",
            "bucket": folder.bucket,
            "folder": folder.folder_display,
            "folder_id": folder.folder_id,
            "playlist": folder.playlist_display,
            "playlist_id": folder.playlist_id,
            "creates": not folder.playlist_id and bool(folder.wanted),
            "members": len(folder.members),
            "wanted": len(folder.wanted),
            "adds": list(folder.adds),
            "removes": list(folder.removes),
        }
        for folder in plan.folders
    ]
    items.extend({"action": "leave", "folder": name} for name in plan.unclaimed)
    return {
        "digest": plan.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "folders": len(plan.folders),
            "favourites": plan.favourites,
            "adds": plan.adds,
            "removes": plan.removes,
            "creates": plan.creates,
            "unclaimed": len(plan.unclaimed),
        },
        "chunk": None,
    }


def facts(plan: RefreshPlan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    return {
        "mirrors": f"{plan.source_name} (row {plan.source_id}), {plan.favourites} track(s)",
        "under": f"the tree {plan.tree_id!r} (root {plan.root_id})",
        "folders": len(plan.folders),
        "adds": plan.adds,
        "removes": plan.removes,
        "playlists to create": plan.creates,
        "folders left alone": len(plan.unclaimed),
    }


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


class RefreshInterrupted(Exception):
    """The refresh stopped after its additions landed and before it was done.

    Carries the refresh as far as it got and its session, the failure as
    ``__cause__``, for that window only, whatever the failure's type.
    """

    def __init__(self, partial: "Refreshed") -> None:
        self.partial = partial
        super().__init__(
            f"the genre Favorites refresh of tree {partial.tree_id!r} added "
            f"{partial.added} membership(s) in session {partial.session_id} and "
            f"removed none"
        )


@dataclass(frozen=True, slots=True)
class Refreshed:
    """What one refresh wrote, read back from the database after its commits."""

    tree_id: str
    added: int
    removed: int
    created: tuple[str, ...]
    #: The removals the plan held that this run was not asked to make.
    removals_owed: int
    session_id: str
    #: Every folder whose Favorites, read back live, is not its planned target.
    disagreements: tuple[str, ...] = ()


def _playlist_row(db: Any, folder: FolderPlan, parent: Any) -> tuple[Any, bool]:
    """The folder's Favorites row: the planned one, else found live by name, else made."""
    if folder.playlist_id:
        row = db.get_playlist(ID=folder.playlist_id)
        if row is None or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the Favorites playlist of {folder.folder_display!r} (row "
                f"{folder.playlist_id}) is not live any more, so nothing was written",
                origin=_ORIGIN,
                detail={"folder": folder.folder_id, "playlist": folder.playlist_id},
            )
        return row, False
    parent_id = str(parent.ID)
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
            return row, False
    return db.create_playlist(folder.playlist_display, parent=parent), True


def _record_favorites_commit(
    record: session.SessionRecord, tree_id: str, *, added: int, removed: int, cfg: config.Config
) -> None:
    """Record a commit on the session, as rows created and rows changed under the tree."""
    if added <= 0 and removed <= 0:
        return
    session.record_commit(
        record,
        tree_id,
        session.ChangeSummary((session.TreeChange(tree=tree_id, created=added, updated=removed),)),
        cfg,
    )


def _add_favorites(
    cfg: config.Config, db: Any, plan: RefreshPlan, record: session.SessionRecord
) -> tuple[int, list[str], list[convergence.DestinationNode]]:
    """The additions and their own commit: how many, the playlists made, the nodes written."""
    added = 0
    created: list[str] = []
    nodes: list[convergence.DestinationNode] = []
    with rb_writer.commit_witness(db) as witness:
        try:
            for folder in plan.folders:
                if not folder.adds:
                    continue
                parent = db.get_playlist(ID=folder.folder_id)
                if parent is None or rb_writer.node_removed(parent):
                    raise refuse(
                        "decision-stale",
                        f"the folder {folder.folder_display!r} (row {folder.folder_id}) "
                        f"is not live any more, so nothing was written",
                        origin=_ORIGIN,
                        detail={"folder": folder.folder_id},
                    )
                playlist, made = _playlist_row(db, folder, parent)
                if made:
                    created.append(folder.folder_display)
                added += len(rb_writer.add_memberships(db, playlist, folder.adds))
                nodes.append(
                    convergence.DestinationNode(
                        bucket=folder.bucket, sub=plan.sub_class,
                        folder_id=folder.folder_id, playlist_id=str(playlist.ID),
                    )
                )
            rb_writer.commit_guarded(db)
        except BaseException:
            trees.rollback_quietly(db)
            if witness.landed:
                _record_favorites_commit(record, plan.tree_id, added=added, removed=0, cfg=cfg)
            raise
    return added, created, nodes


def _remove_favorites(
    cfg: config.Config, db: Any, plan: RefreshPlan, record: session.SessionRecord
) -> int:
    """The removals behind the additions, in a commit of their own: how many."""
    removed = 0
    with rb_writer.commit_witness(db) as witness:
        try:
            for folder in plan.folders:
                if not folder.removes or not folder.playlist_id:
                    continue
                playlist = db.get_playlist(ID=folder.playlist_id)
                if playlist is None:
                    continue
                removed += len(rb_writer.remove_memberships(db, playlist, folder.removes))
            # THE MEMBERSHIP TABLE ALONE, never the whole removable set.
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
        except BaseException:
            trees.rollback_quietly(db)
            if witness.landed:
                _record_favorites_commit(record, plan.tree_id, added=0, removed=removed, cfg=cfg)
                convergence.record_fingerprint(cfg, db)
            raise
    return removed


def apply_refresh(
    cfg: config.Config,
    db: Any,
    plan: RefreshPlan,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    analysis_roots: Iterable[Path | str],
    remove: bool,
) -> Refreshed:
    """Write the plan: the additions in one commit, the removals in a second.

    The plan is taken again on this handle first, and a digest that moved
    refuses. The session spine is called as the membership move calls it.
    ``remove`` declares which half the caller was approved for.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    again = plan_refresh(cfg, db, declared, registry)
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them, so nothing was "
            "written; run it again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": plan.digest, "now": again.digest},
        )
    plan = again
    convergence.assert_tree_writable(cfg, db, plan.tree_id, registry)

    removed = 0
    with session.assert_gates(
        cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
    ) as gates:
        record, capture = trees.attached_capture(gates, cfg, db)
        added, created, nodes = _add_favorites(cfg, db, plan, record)
        _record_favorites_commit(record, plan.tree_id, added=added, removed=0, cfg=cfg)
        landed = Refreshed(
            tree_id=plan.tree_id, added=added, removed=0, created=tuple(created),
            removals_owed=plan.removes, session_id=record.session_id,
        )
        # Everything past the additions' commit is reported as half written when
        # it fails, whatever its type.
        try:
            if added:
                convergence.record_fingerprint(cfg, db)
            if nodes:
                convergence.record_nodes(cfg, plan.tree_id, nodes)
            owed = plan.removes
            if remove and owed:
                removed = _remove_favorites(cfg, db, plan, record)
                _record_favorites_commit(record, plan.tree_id, added=0, removed=removed, cfg=cfg)
                if removed:
                    convergence.record_fingerprint(cfg, db)
                owed = 0
            disagreements = _read_back(db, plan, removed_too=remove)
        except Exception as exc:
            raise RefreshInterrupted(landed) from exc
        session_id = record.session_id

    return Refreshed(
        tree_id=plan.tree_id, added=added, removed=removed, created=tuple(created),
        removals_owed=owed, session_id=session_id, disagreements=disagreements,
    )


def _read_back(db: Any, plan: RefreshPlan, *, removed_too: bool) -> tuple[str, ...]:
    """Each folder whose Favorites, read live from SQL, is not what the plan wanted."""
    from sqlalchemy import text

    problems: list[str] = []
    for folder in plan.folders:
        playlist_id = folder.playlist_id
        if not playlist_id:
            if not folder.wanted:
                continue
            rows = db.session.execute(
                text(
                    f"SELECT ID FROM {rb_writer.PLAYLIST_TABLE} WHERE ParentID = :parent "
                    f"AND Name = :name AND Attribute = 0 "
                    f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
                ),
                {"parent": folder.folder_id, "name": folder.playlist_display},
            ).fetchall()
            if len(rows) != 1:
                problems.append(f"{folder.folder_display}: {len(rows)} live Favorites playlist(s)")
                continue
            playlist_id = str(rows[0][0])
        live = {
            str(row[0])
            for row in db.session.execute(
                text(
                    f"SELECT ContentID FROM {rb_writer.MEMBERSHIP_TABLE} WHERE PlaylistID = :id "
                    f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
                ),
                {"id": playlist_id},
            ).fetchall()
        }
        wanted = set(folder.wanted)
        if not wanted <= live:
            problems.append(
                f"{folder.folder_display}: {len(wanted - live)} planned track(s) not in Favorites"
            )
        if removed_too and live - wanted:
            problems.append(
                f"{folder.folder_display}: {len(live - wanted)} track(s) still in Favorites"
            )
    return tuple(problems)


def assert_read_back(refreshed: Refreshed) -> None:
    """Refuse an answer the database does not hold."""
    if refreshed.disagreements:
        raise refuse(
            "session-committed-unverified",
            f"the genre Favorites read back from the database are not the plan's in "
            f"{len(refreshed.disagreements)} folder(s): "
            + "; ".join(refreshed.disagreements)
            + "; the commits landed and this answer cannot be vouched for",
            origin=_ORIGIN,
            detail={"disagreements": list(refreshed.disagreements)},
        )


# ---------------------------------------------------------------------------
# The additive half, for the end of an adoption
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AdditiveOutcome:
    """What the additive half did at the end of another writer's run, or why it did nothing."""

    refreshed: Refreshed | None = None
    #: Why nothing ran: the class undeclared, the source missing, the tree on the
    #: bridge. Empty when it ran.
    skipped: str = ""
    #: The refusal's code behind ``skipped`` when it had one (U132), so the note
    #: an adoption carries names the cause and not only its sentence.
    cause: str = ""


def refresh_additive(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    *,
    analysis_roots: Iterable[Path | str],
) -> AdditiveOutcome:
    """Add every favourite to its genre Favorites, through a write handle of its own.

    For the end of an adoption that filed a track. It removes nothing, as
    adoption's contract holds, and says how many removals it left owed.
    """
    sub = favorites_class(declared)
    if sub is None:
        return AdditiveOutcome(
            skipped="the taxonomy declares no sub class derived from a playlist",
            cause=CLASS_UNDECLARED,
        )
    # Every refusal is a skip with its reason: the adoption's own writes have
    # landed.
    try:
        registry = tree_registry.read(cfg)
        db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    except CratekitError as exc:
        return AdditiveOutcome(skipped=exc.cause.message, cause=exc.cause.reason)
    try:
        try:
            plan = plan_refresh(cfg, db, declared, registry)
        except CratekitError as exc:
            return AdditiveOutcome(skipped=exc.cause.message, cause=exc.cause.reason)
        if not plan.adds:
            return AdditiveOutcome(
                refreshed=Refreshed(
                    tree_id=plan.tree_id, added=0, removed=0, created=(),
                    removals_owed=plan.removes, session_id="",
                )
            )
        try:
            refreshed = apply_refresh(
                cfg, db, plan, declared=declared, registry=registry,
                analysis_roots=analysis_roots, remove=False,
            )
        except RefreshInterrupted as exc:
            # The additions landed and are reported, the failure beside them.
            inner = exc.__cause__
            return AdditiveOutcome(
                refreshed=exc.partial,
                skipped=str(inner or exc),
                cause=inner.cause.reason if isinstance(inner, CratekitError) else "",
            )
        except CratekitError as exc:
            return AdditiveOutcome(skipped=exc.cause.message, cause=exc.cause.reason)
        return AdditiveOutcome(refreshed=refreshed)
    finally:
        rb_writer.close_db(db)


__all__ = [
    "CLASS_UNDECLARED", "FAVORITES_DIMENSION", "SOURCE_MISSING", "WORKFLOW", "AdditiveOutcome",
    "FolderPlan", "RefreshInterrupted", "RefreshPlan", "Refreshed", "apply_refresh",
    "assert_read_back", "facts", "favorites_class", "identity", "live_members", "payload",
    "placements", "plan_refresh", "refresh_additive", "require_class", "source_playlist",
    "undeclared_note", "undeclared_warnings",
]
