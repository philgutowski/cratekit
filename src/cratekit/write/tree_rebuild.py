"""Rebuilding a governed tree, and saying whether it matches the declaration (U36).

WHAT THIS MODULE IS FOR. A database-native tree has exactly one repair path. The
XML bridge is gone for it, so there is no export to re-import, and under U9's A2
verdict importing one would replace the tree rather than merge into it.
Incremental sync cannot help either: its scope is a watermark plus deduplication
against what the library already owns, and the files a recovered database no
longer places are still sitting on disk and still read as owned, so a sync sees
nothing to do. What is left is deriving the tree's whole membership again, from
the declared taxonomy and from what is actually on the disk, with no watermark
anywhere in it. That is the rebuild.

THE THREE PROPERTIES, each one a failure the naive version produces.

**It converges across a rename, or it doubles the tree.** Every find-or-create in
the guarded writer targets a playlist by the name rekordbox shows. So a rebuild
that resolved its destinations from the taxonomy's display names would, the first
time somebody renamed a folder in rekordbox, find nothing under the new name,
create the destination a second time, and file every track twice. The previous
unit hit this exact wall and refused rather than duplicating, registering the
obligation on the unit that owns the record. This is that record being used: the
node identifiers a previous write landed in are persisted, and a destination is
resolved through them first and by display name only when nothing was recorded.

**It adds and never removes.** A membership somebody made by hand under a
governed tree is their data, not damage, and a rebuild that "made the tree match"
by deleting it would be the one operation in this product that destroys work
nobody can get back. So the write is additive, the check reports the other
direction honestly, and a difference the derivation cannot account for is settled
by a person rather than by a delete.

**It is idempotent, including across a crash.** The write goes through the one
membership writer, whose add is a read-then-insert under the session lock, so a
second pass over the same plan inserts nothing. A crash anywhere leaves the tree
either as it was or partly repaired, and re-running finishes the job.

WHAT "LIBRARY TRUTH" MEANS HERE, PRECISELY. The files on disk and the tags on
them, read live rather than from an export, because an export is hours stale and
re-deriving from a stale genre moves a track the user has already re-tagged. It
is deliberately NOT the database's own playlist rows: deriving the tree from the
tree would make every check a tautology and every rebuild a no-op.

LAYER: write. It reads state and files, calls the session spine through the
membership writer rather than rebuilding it, and names no verb (D2).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.core import config, convergence, locations, routing, tags, taxonomy, tree_registry
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import routing_pass, trees

logger = logging.getLogger(__name__)

#: The workflow name a rebuild records in the session log. A name for an
#: operation, not a verb: the CLI layer owns verb names (D2).
REBUILD_WORKFLOW = "tree-rebuild"

#: The dimension name reported when this library has no vocal calibration, so
#: the additive vocal sub-playlists could not be derived this run. Named rather
#: than spelled at the two places that produce and consume it.
VOCAL_DIMENSION = "vocal"


# ---------------------------------------------------------------------------
# What the declaration says a tree should hold
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Truth:
    """One file on disk and the three readings the declared rules route on.

    A value rather than a path, so the derivation below is pure and testable
    with no audio files at all, and so the file input happens once in a function
    whose only job is that.
    """

    location: str
    genre: str | None = None
    energy: int | None = None
    voxlevel: int | None = None


@dataclass(frozen=True, slots=True)
class DeclaredPlacement:
    """One file and the ONE destination the declaration puts it in.

    ``bucket`` and ``sub`` are stable taxonomy identifiers, never display names
    (R19, D5). A track that belongs in two places, which is what an additive
    sub-playlist means, produces two of these rather than one carrying a list:
    the pair is the unit the check compares and the write plans on, and folding
    them would make "this track is missing from one of its two playlists"
    inexpressible.
    """

    location: str
    bucket: str
    sub: str


def read_truth(path: Path) -> Truth:
    """The three tag readings for one file, through the one container-correct reader.

    Through :mod:`cratekit.core.tags` rather than mutagen directly, because that
    module is the only place that knows which container takes which dialect, and
    a second reader here would be a second answer to which key a field lives
    under. It never raises for an unreadable file: an absent reading routes to
    the declared fallback, which is visible in the result, while an exception
    would abandon the rebuild over one stray file.
    """
    return Truth(
        location=str(path),
        genre=tags.read_genre_from_file(path),
        energy=tags.read_energy_from_file(path),
        voxlevel=tags.read_vox_from_file(path),
    )


def library_truth(
    root: Path | str,
    *,
    suffixes: Sequence[str] = tags.SUPPORTED_SUFFIXES,
    reader: Callable[[Path], Truth] = read_truth,
) -> Iterator[Truth]:
    """Every taggable file under ``root``, in a stable order, with its readings.

    THE SUFFIX SET IS DERIVED FROM THE TAG MODULE'S OWN TABLE, never listed here.
    A hand-kept copy is a copy that misses the next container that module learns,
    and the symptom would be a whole format silently absent from a rebuild while
    the rebuild reported the tree converged (P3).

    Sorted, so a rebuild's plan is a function of the library's content rather
    than of the order the filesystem happened to hand back, and so two runs over
    an unchanged library produce byte-identical plans.

    A GENERATOR, and the caller materializes it if it needs two passes. The whole
    library is the natural input here and a caller that walks an exhausted one
    twice sees an empty library the second time, which is the shape that reported
    a run clean over a library it never read.
    """
    wanted = {suffix.lower() for suffix in suffixes}
    base = Path(root)
    if not base.is_dir():
        return
    for path in sorted(base.rglob("*")):
        if path.is_file() and path.suffix.lower() in wanted:
            yield reader(path)


def derive_from_taxonomy(
    declared: taxonomy.Taxonomy,
    truth: Iterable[Truth],
    *,
    vocal_threshold: float | None,
) -> tuple[tuple[DeclaredPlacement, ...], tuple[str, ...]]:
    """Route every file through the declared rules. Returns placements and gaps.

    THE RULES ARE THE ONES THE ROUTING PASS USES, called rather than restated.
    Bucket resolution, the energy split and the vocal cut all live in
    :mod:`cratekit.core.routing`, and a second implementation here would be two
    answers to "where does this track go" that agree until the day they do not,
    at which point a rebuild would move a library's worth of tracks.

    AN ADDITIVE SUB-PLAYLIST THIS DERIVATION HAS NO SIGNAL FOR IS A REFUSAL, not
    an omission, and this is P4 applied to the one place it bites. A taxonomy may
    declare additive sub-playlists; this derivation knows the signal for exactly
    one of them. Silently skipping a second would produce a tree missing a whole
    dimension, and nothing would notice: the playlists it never wrote belong to
    no declared destination, so the check would treat them as somebody else's and
    report the tree converged. A derivation that is 90 percent complete is worse
    than an honest refusal, because it invites trust.

    A LIBRARY WITH NO VOCAL CALIBRATION IS A GAP, NOT A REFUSAL. The threshold is
    passed in and never imported (D7), and None is a real answer: a slim install
    has no vocals module and no calibration. That dimension is then not derived
    and is NAMED in the second return value, so a reader of a converged answer
    can see what was not compared rather than being told everything matched.
    """
    additive = tuple(entry for entry in declared.sub_classes if entry.additive)
    unknown = sorted(entry.id for entry in additive if entry.id != trees.VOX_SUB_CLASS)
    if unknown:
        raise refuse(
            "rebuild-derivation-incomplete",
            f"this library's taxonomy declares the additive sub-playlists "
            f"{unknown!r}, and this rebuild has no signal it can derive them "
            f"from; rebuilding anyway would write a tree missing them and then "
            f"report it converged, because a playlist no declared destination "
            f"names is not compared at all",
            remedy=Remedy.FIX_CONFIG_VALUES,
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"sub_classes": unknown},
        )

    gaps: list[str] = []
    if additive and vocal_threshold is None:
        gaps.append(VOCAL_DIMENSION)

    out: list[DeclaredPlacement] = []
    for entry in truth:
        resolution = routing.resolve_bucket(declared, entry.genre)
        sub = routing.energy_sub(
            declared, resolution.bucket_id, entry.energy, source_genre=entry.genre or ""
        )
        if sub is not None:
            # A None sub is a real answer from the routing rules: this taxonomy
            # declares no place below that bucket for this track. Treating it as
            # an error here would crash a rebuild over a declaration that is
            # simply narrower than the library.
            out.append(DeclaredPlacement(entry.location, resolution.bucket_id, sub.id))
        if vocal_threshold is not None and routing.routes_with_vox(
            entry.voxlevel, vocal_threshold
        ):
            for sub_class in additive:
                out.append(
                    DeclaredPlacement(entry.location, resolution.bucket_id, sub_class.id)
                )
    return tuple(out), tuple(gaps)


#: One derivation per source a tree may cut over on. A MAPPING rather than a
#: chain of branches, and the test beside it asserts this mapping's key set is
#: exactly ``tree_registry.REBUILDABLE``: a source declared rebuildable with no
#: derivation behind it would let a tree flip and then fail at the one moment the
#: rebuild is needed, and a derivation for a source nothing may flip on is dead
#: code claiming coverage it can never be asked for.
DERIVATIONS: Mapping[tree_registry.DerivationSource, Callable[..., Any]] = MappingProxyType(
    {tree_registry.DerivationSource.TAXONOMY: derive_from_taxonomy}
)


def declared_membership(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    *,
    source: tree_registry.DerivationSource | None,
    vocal_threshold: float | None,
    truth: Iterable[Truth] | None = None,
) -> tuple[tuple[DeclaredPlacement, ...], tuple[str, ...]]:
    """What the declaration says the tree holds, by the source the registry records.

    ``truth`` defaults to a live walk of the library's music directory, and a
    caller supplying its own is supplying the READINGS rather than the rules:
    the derivation is the same function either way. That is the seam a test uses
    and it cannot weaken the guard, because nothing about which destinations
    exist or how a reading routes travels through it.
    """
    derive = None if source is None else DERIVATIONS.get(source)
    if derive is None:
        raise refuse(
            "rebuild-derivation-incomplete",
            f"no rebuild derivation is registered for the source "
            f"{'none at all' if source is None else str(source)!r}, so this "
            f"tree's membership cannot be reproduced; a tree may only cut over "
            f"on a source a rebuild can derive",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"source": str(source)},
        )
    readings = (
        library_truth(Path(cfg.library.root) / cfg.library.music_dir)
        if truth is None
        else truth
    )
    return derive(declared, readings, vocal_threshold=vocal_threshold)


# ---------------------------------------------------------------------------
# What the database actually holds
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TreeNode:
    """One playlist inside a governed tree, its folder, and what it holds.

    Both identifiers AND both display names, deliberately. The identifiers are
    what a destination is resolved through, so a rename cannot orphan it; the
    display names are what the membership writer's find-or-create targets, so
    they are what a plan has to be phrased in. Carrying only one of the two
    would mean re-reading the database to get the other, from a walk that has
    already been done.
    """

    folder_id: str
    folder_display: str
    playlist_id: str
    playlist_display: str
    content_ids: frozenset[str] = frozenset()


def read_tree(db: Any, root_id: str) -> tuple[TreeNode, ...]:
    """Every playlist two levels under the adopted root, with its membership.

    THE WALK GOES DOWN FROM THE ADOPTED ROOT BY IDENTIFIER, never by name. A walk
    that resolved the tree by its display name would find a namesake anywhere in
    the library and report on that instead, which is the silent parallel tree
    arriving through the check meant to detect it.

    TWO LEVELS, because that is the depth the taxonomy declares: a tree holds
    folders and a folder holds playlists. A playlist sitting directly under the
    root is not a shape any declared destination can name, so its membership is
    not part of this comparison and is left alone rather than being reported as a
    difference nobody can act on.

    The folder list is MATERIALIZED before the inner queries run. Iterating one
    query while issuing others on the same session is the shape that made a
    previous unit's row index report an empty library on its second pass.
    """
    out: list[TreeNode] = []
    folders = list(db.get_playlist(ParentID=str(root_id)))
    for folder in folders:
        playlists = list(db.get_playlist(ParentID=str(folder.ID)))
        for playlist in playlists:
            members = db.get_playlist_songs(PlaylistID=str(playlist.ID))
            out.append(
                TreeNode(
                    folder_id=str(folder.ID),
                    folder_display=str(folder.Name),
                    playlist_id=str(playlist.ID),
                    playlist_display=str(playlist.Name),
                    content_ids=frozenset(str(row.ContentID) for row in members),
                )
            )
    return tuple(out)


@dataclass(frozen=True, slots=True)
class Destination:
    """One declared destination and the node in the database it means.

    ``folder`` and ``playlist`` are the names a write must use, which is not
    always what the taxonomy says: when a recorded node is found, they are that
    node's CURRENT names, so a folder somebody renamed in rekordbox is written
    into rather than created again beside itself.
    """

    bucket: str
    sub: str
    folder: str
    playlist: str
    node: TreeNode | None = None
    renamed: bool = False


def resolve_destinations(
    declared: taxonomy.Taxonomy,
    placements: Sequence[DeclaredPlacement],
    nodes: Sequence[TreeNode],
    record: convergence.TreeConvergence | None,
) -> tuple[Destination, ...]:
    """Bind each declared destination to the node a previous write actually used.

    THE RESOLUTION ORDER IS THE WHOLE UNIT, and it is: recorded identifier, then
    declared display name, then nothing.

    The recorded identifier first, because it is the only thing a rename does not
    move. A tree whose folder somebody renamed in rekordbox still has the same
    playlist rows, and resolving through them is what lets the rebuild write into
    the tree the library actually has instead of building a second one beside it
    under the taxonomy's names.

    The declared display name second, for the case there is nothing recorded:
    the first rebuild after a cutover, or a destination that has never been
    written. That is the ordinary adoption path the membership writer already
    relies on, and it is correct precisely when no rename has happened.

    Nothing third. A destination with no node at all is one the write will
    create, under the declared name, which is the right name for a playlist
    nobody has ever seen.

    A RECORDED IDENTIFIER THAT NO LONGER RESOLVES FALLS BACK RATHER THAN
    REFUSING. Somebody deleted the playlist, or a restore removed it; either way
    the declared name is the best remaining answer and creating it is the repair.
    Refusing there would turn the one operation that fixes a damaged tree into
    another thing the damage breaks.
    """
    by_ids = {(node.folder_id, node.playlist_id): node for node in nodes}
    by_display = {(node.folder_display, node.playlist_display): node for node in nodes}

    out: list[Destination] = []
    for bucket, sub in sorted({(entry.bucket, entry.sub) for entry in placements}):
        folder_display, sub_display = routing_pass.destination(declared, bucket, sub)
        recorded = None if record is None else record.node(bucket, sub)
        node = None
        if recorded is not None:
            node = by_ids.get((recorded.folder_id, recorded.playlist_id))
        if node is None:
            node = by_display.get((folder_display, sub_display))
        if node is None:
            out.append(Destination(bucket=bucket, sub=sub, folder=folder_display, playlist=sub_display))
            continue
        out.append(
            Destination(
                bucket=bucket,
                sub=sub,
                folder=node.folder_display,
                playlist=node.playlist_display,
                node=node,
                renamed=(node.folder_display, node.playlist_display)
                != (folder_display, sub_display),
            )
        )
    return tuple(out)


# ---------------------------------------------------------------------------
# The convergence check
# ---------------------------------------------------------------------------


class Direction(StrEnum):
    """Which way a difference points. Both are reported; only one is repairable."""

    #: The declaration places a track here and the database does not hold it.
    MISSING = "missing"
    #: The database holds a track in a declared destination that the declaration
    #: does not place there.
    UNEXPECTED = "unexpected"


@dataclass(frozen=True, slots=True)
class Difference:
    """One track, one destination, and which way the two sides disagree."""

    direction: Direction
    bucket: str
    sub: str
    folder: str
    playlist: str
    content_id: str | None = None
    location: str | None = None

    def summary(self) -> str:
        """One line naming the difference by its STABLE identifiers.

        The display names are carried on the record for a person to read; the
        summary keys on the identifiers because it is what the clear-the-flag
        refusal repeats back, and a refusal that named a folder somebody has
        since renamed would name something they cannot find.
        """
        what = self.content_id or self.location or "?"
        return f"{self.direction}:{self.bucket}/{self.sub}:{what}"


@dataclass(frozen=True, slots=True)
class ConvergenceReport:
    """What one tree's declaration and one tree's database rows say, side by side.

    ``unmatched`` IS NOT A DIFFERENCE, and that is a decision rather than an
    oversight. It carries every declared file that reached no single active row:
    a track on disk nobody has imported yet, one claimed by two rows, one whose
    recorded path no prefix maps. A playlist cannot hold a row the library does
    not have, so counting those as differences would make convergence
    unreachable for every library that has ever downloaded a track it has not yet
    imported, and an unreachable convergence is a flag that can never be cleared.
    The membership writer already skips and surfaces exactly this set, and this
    is the same fact reported by the same rule.

    ``foreign`` is the other set that is reported and is not a difference: nodes
    under the governed root that no declared destination resolves to. A person's
    own playlist under a governed tree, and every sub-playlist the taxonomy marks
    as curated rather than derived, land here. Reporting them as damage would
    make a guard that fires on ordinary correct libraries, which is a guard
    people learn to route around.

    THE ACTIVE-ROW RULE APPLIES TO BOTH DIRECTIONS. A declared file that reaches
    no active row is not missing, and a membership pointing at a row that is no
    longer active is not unexpected. Applying it to one side only would be two
    rules for one question, and the asymmetry always resolves the same way: the
    flag stays shut over something nobody can act on.
    """

    tree_id: str
    root_id: str
    missing: tuple[Difference, ...] = ()
    unexpected: tuple[Difference, ...] = ()
    unmatched: tuple[trees.RowMatch, ...] = ()
    foreign: tuple[str, ...] = ()
    renamed: tuple[str, ...] = ()
    not_compared: tuple[str, ...] = ()

    @property
    def differences(self) -> tuple[Difference, ...]:
        """Both directions, in one tuple, because R39 asks for both."""
        return self.missing + self.unexpected

    @property
    def converged(self) -> bool:
        return not self.differences

    def summaries(self) -> tuple[str, ...]:
        return tuple(entry.summary() for entry in self.differences)


def check(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    declared: taxonomy.Taxonomy,
    placements: Sequence[DeclaredPlacement],
    rows: Iterable[trees.ContentRow],
    root_exists: Callable[[str], bool],
    prefix_map: Sequence[locations.PrefixRule] | None = None,
    not_compared: Sequence[str] = (),
) -> ConvergenceReport:
    """Report, for one governed tree, how the declaration and the database differ.

    READ ONLY. Nothing here opens a session, takes a lock, or writes a byte, so
    it can be run against a library at any moment, including one that is already
    refusing every write. That is not a convenience: the check is what a person
    is told to run when a tree is flagged, and a diagnostic that needed the gates
    the flag is holding shut would be a diagnostic nobody can reach.

    IT RESOLVES DESTINATIONS THROUGH THE RECORDED NODE IDENTIFIERS, exactly as
    the rebuild does. A check that resolved by display name while the rebuild
    resolved by identifier would be two locates, and two locates that answer
    differently is how a check reports a tree short that the rebuild has just
    finished repairing.
    """
    root_id = tree_registry.anchored_root(tree_id, registry, root_exists=root_exists)
    rules = (
        [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
        if prefix_map is None
        else list(prefix_map)
    )

    # ONE walk of the library, before anything is compared. Rebuilt per
    # destination it would re-normalize every row once per destination, and it
    # would report an empty library on the second pass for the caller whose rows
    # are a database cursor, which is the natural way to pass every content row.
    index = trees.index_active_rows(rows, root=cfg.library.root, prefix_map=rules)
    matches = trees.match_indexed_rows(
        [entry.location for entry in placements],
        index,
        root=cfg.library.root,
        prefix_map=rules,
    )
    resolved_id: dict[str, str] = {}
    unmatched: list[trees.RowMatch] = []
    for match in matches:
        if match.outcome is trees.MatchOutcome.MATCHED and match.content_id:
            resolved_id[match.requested] = match.content_id
        else:
            unmatched.append(match)

    nodes = read_tree(db, root_id)
    record = convergence.read(cfg).tree(tree_id)
    destinations = resolve_destinations(declared, placements, nodes, record)
    by_key = {(entry.bucket, entry.sub): entry for entry in destinations}

    wanted: dict[tuple[str, str], set[str]] = {}
    missing: list[Difference] = []
    for entry in placements:
        content_id = resolved_id.get(entry.location)
        if content_id is None:
            # Surfaced through ``unmatched`` above rather than counted here. See
            # the report's own docstring for why a file with no row is a fact
            # about the collection and not about the tree.
            continue
        destination = by_key[(entry.bucket, entry.sub)]
        wanted.setdefault((entry.bucket, entry.sub), set()).add(content_id)
        held = frozenset() if destination.node is None else destination.node.content_ids
        if content_id not in held:
            missing.append(
                Difference(
                    direction=Direction.MISSING,
                    bucket=entry.bucket,
                    sub=entry.sub,
                    folder=destination.folder,
                    playlist=destination.playlist,
                    content_id=content_id,
                    location=entry.location,
                )
            )

    governed = {
        (entry.node.folder_id, entry.node.playlist_id): entry
        for entry in destinations
        if entry.node is not None
    }
    # ONLY ACTIVE ROWS COUNT ON THIS SIDE TOO, which is the same rule the other
    # direction already applies from the other end. A membership row pointing at
    # a track the user soft-deleted is a leftover the declaration cannot place
    # and an additive rebuild cannot remove, so calling it a difference would
    # hold the flag shut over something nobody can act on.
    active = {content_id for ids in index.values() for content_id in ids}
    unexpected: list[Difference] = []
    foreign: list[str] = []
    for node in nodes:
        destination = governed.get((node.folder_id, node.playlist_id))
        if destination is None:
            foreign.append(f"{node.folder_display}/{node.playlist_display}")
            continue
        declared_here = wanted.get((destination.bucket, destination.sub), set())
        for content_id in sorted((node.content_ids & active) - declared_here):
            unexpected.append(
                Difference(
                    direction=Direction.UNEXPECTED,
                    bucket=destination.bucket,
                    sub=destination.sub,
                    folder=destination.folder,
                    playlist=destination.playlist,
                    content_id=content_id,
                )
            )

    return ConvergenceReport(
        tree_id=tree_id,
        root_id=root_id,
        missing=tuple(missing),
        unexpected=tuple(unexpected),
        unmatched=tuple(unmatched),
        foreign=tuple(sorted(foreign)),
        renamed=tuple(
            sorted(f"{entry.bucket}/{entry.sub}" for entry in destinations if entry.renamed)
        ),
        not_compared=tuple(not_compared),
    )


# ---------------------------------------------------------------------------
# The rebuild
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RebuildReport:
    """What one rebuild wrote, and where the tree stood after it.

    ``before`` and ``after`` are both kept. A rebuild that reports only the end
    state cannot tell "there was nothing wrong" from "there was something wrong
    and it is fixed", and those are the two answers a person actually wants.
    """

    tree_id: str
    root_id: str
    before: ConvergenceReport
    after: ConvergenceReport
    membership: trees.MembershipReport | None = None
    cleared: bool = False

    @property
    def repaired(self) -> int:
        return 0 if self.membership is None else self.membership.added


def report_convergence(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    declared: taxonomy.Taxonomy,
    rows: Iterable[trees.ContentRow],
    root_exists: Callable[[str], bool],
    vocal_threshold: float | None,
    truth: Iterable[Truth] | None = None,
    prefix_map: Sequence[locations.PrefixRule] | None = None,
) -> ConvergenceReport:
    """Derive this tree's declared membership and compare it against the database.

    THE READ-ONLY ENTRY POINT, and the one a diagnostic calls. It derives through
    the source the REGISTRY records for this tree rather than through anything a
    caller names, which is the same reason the medium check reads the registry:
    a caller that supplies the answer supplies the answer to the question.
    """
    placements, gaps = declared_membership(
        cfg,
        declared,
        source=registry.derivation_source(tree_id),
        vocal_threshold=vocal_threshold,
        truth=truth,
    )
    return check(
        cfg,
        db,
        tree_id=tree_id,
        registry=registry,
        declared=declared,
        placements=placements,
        rows=rows,
        root_exists=root_exists,
        prefix_map=prefix_map,
        not_compared=gaps,
    )


def rebuild_tree(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    declared: taxonomy.Taxonomy,
    rows: Iterable[trees.ContentRow],
    root_exists: Callable[[str], bool],
    analysis_roots: Iterable[Path | str],
    vocal_threshold: float | None,
    truth: Iterable[Truth] | None = None,
    prefix_map: Sequence[locations.PrefixRule] | None = None,
    workflow: str = REBUILD_WORKFLOW,
    now: datetime | None = None,
) -> RebuildReport:
    """Write back everything the declaration places in this tree and the database lacks.

    THE ORDER IS THE UNIT, and it is: refuse if this tree is not rebuildable,
    derive, check, write, record where it landed, check again, and only then
    clear the flag.

    * **Rebuildability first**, because a tree that cut over on a source nothing
      can derive was never repairable, and finding that out after the write has
      already restructured a library is finding it out too late.
    * **The check before the write**, so the report can say what was wrong rather
      than only that something now looks right.
    * **The node record after the commit**, never before. A node identifier
      written down for a row that was never committed is a dangling pointer, and
      the next rebuild would resolve a destination to a playlist that does not
      exist. Recorded after, a crash in the window leaves the previous record
      standing, the next run falls back to resolving by display name, and it
      finds the same playlists because nothing renamed them in that window.
    * **The flag cleared last, and only on evidence.** The second check is run
      against the database as it now stands, and a tree that still differs keeps
      its flag. Clearing first and re-setting on failure would leave a crash in
      the middle looking exactly like a repair.

    THE PLACEMENTS ARE DERIVED HERE AND ARE NOT A PARAMETER. That is the whole
    point of recording a derivation source on the tree: the membership a rebuild
    writes comes from the source the registry names, every time. Accepting a
    caller's list instead would be the softening path in its purest form, since
    the one thing this function exists to guarantee is exactly the thing the
    parameter would let somebody supply. ``truth`` is the seam that remains, and
    it supplies the tag READINGS rather than the destinations: the rules, the
    identifiers and the display names all still come from the declaration.

    ``rows`` IS MATERIALIZED ONCE, HERE. Both the checks and the write need it,
    and the natural way to pass every content row is a database cursor, which
    reports an empty library to whoever walks it second.

    THE SESSION IS NOT THIS FUNCTION'S TO OPEN. The write goes through
    :func:`cratekit.write.trees.write_tree_membership`, which owns its own gates
    for the reason R29 gives, and which is handed the rebuild purpose so the
    convergence latches whose remedy is this function do not refuse it.
    """
    source = registry.derivation_source(tree_id)
    tree_registry.assert_rebuildable(tree_id, source)
    collection = tuple(rows)
    root_id = tree_registry.anchored_root(tree_id, registry, root_exists=root_exists)
    placements, not_compared = declared_membership(
        cfg,
        declared,
        source=source,
        vocal_threshold=vocal_threshold,
        truth=truth,
    )

    before = check(
        cfg,
        db,
        tree_id=tree_id,
        registry=registry,
        declared=declared,
        placements=placements,
        rows=collection,
        root_exists=root_exists,
        prefix_map=prefix_map,
        not_compared=not_compared,
    )

    record = convergence.read(cfg).tree(tree_id)
    destinations = resolve_destinations(
        declared, placements, read_tree(db, root_id), record
    )
    by_key = {(entry.bucket, entry.sub): entry for entry in destinations}

    plan: dict[tuple[str, str], list[str]] = {}
    for entry in placements:
        destination = by_key[(entry.bucket, entry.sub)]
        plan.setdefault((destination.folder, destination.playlist), []).append(entry.location)

    membership = (
        trees.write_tree_membership(
            cfg,
            db,
            tree_id=tree_id,
            registry=registry,
            plan=plan,
            rows=collection,
            root_exists=root_exists,
            prefix_map=prefix_map,
            analysis_roots=analysis_roots,
            workflow=workflow,
            purpose=convergence.Purpose.REBUILD,
        )
        if plan
        else None
    )

    landed = read_tree(db, root_id)
    by_display = {(node.folder_display, node.playlist_display): node for node in landed}
    recorded = [
        convergence.DestinationNode(
            bucket=entry.bucket,
            sub=entry.sub,
            folder_id=by_display[(entry.folder, entry.playlist)].folder_id,
            playlist_id=by_display[(entry.folder, entry.playlist)].playlist_id,
        )
        for entry in destinations
        if (entry.folder, entry.playlist) in by_display
    ]
    if recorded:
        convergence.record_nodes(cfg, tree_id, recorded)

    after = check(
        cfg,
        db,
        tree_id=tree_id,
        registry=registry,
        declared=declared,
        placements=placements,
        rows=collection,
        root_exists=root_exists,
        prefix_map=prefix_map,
        not_compared=not_compared,
    )

    cleared = False
    if after.converged:
        # THE CHECK'S OWN LIST, not a literal empty tuple. It is empty here by
        # construction and passing it that way is the point: the clearing call
        # says "this is what the check found" rather than asserting emptiness on
        # the check's behalf, so the refusal on the other side of that call can
        # never be satisfied by a caller fabricating the evidence for it.
        convergence.clear_unconverged(
            cfg, tree_id, differences=after.summaries(), now=now
        )
        cleared = True
    else:
        logger.warning(
            "the tree %s still differs from what this library declares in %d "
            "place(s) after a rebuild, so it stays unconverged",
            tree_id,
            len(after.differences),
        )

    return RebuildReport(
        tree_id=tree_id,
        root_id=root_id,
        before=before,
        after=after,
        membership=membership,
        cleared=cleared,
    )


__all__ = [
    "DERIVATIONS",
    "REBUILD_WORKFLOW",
    "VOCAL_DIMENSION",
    "ConvergenceReport",
    "DeclaredPlacement",
    "Destination",
    "Difference",
    "Direction",
    "RebuildReport",
    "TreeNode",
    "Truth",
    "check",
    "declared_membership",
    "derive_from_taxonomy",
    "library_truth",
    "read_tree",
    "read_truth",
    "rebuild_tree",
    "report_convergence",
    "resolve_destinations",
]
