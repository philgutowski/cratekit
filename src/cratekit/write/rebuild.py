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

THE MODULE FILENAME IS THE ONE ISSUE #36'S BRIEF NAMES, and the detour taken to
avoid it is recorded because the reasoning behind it was WRONG. This file shipped
once as ``tree_rebuild.py``, justified as "the layering guard forbids a below-CLI
module from spelling the string ``rebuild``". It does not.
``higher_concept_violations`` in ``tests/test_layering.py`` walks the AST for
STRING CONSTANTS and compares each against ``registry.VERB_NAMES``. Nothing in it
keys on a module's filename, and ``layer_of("cratekit.write.rebuild")`` resolves
through the existing ``^cratekit\\.write\\.`` rule with no edit at all. A reviewer
disproved the claim by experiment: renaming the file back failed on exactly two
string constants, both produced by the mechanical rename, and restoring those
gave a green suite with the file named ``rebuild.py``.

THE COST OF THE DETOUR WAS NOT COSMETIC, which is why it was reversed rather than
left. U32 registered ``cratekit.write.rebuild`` against this unit in
``tests/_pending.py``. A module shipped under any other name leaves that
countdown's probe permanently answering "absent", so ``_pending.py`` auto-merges
clean, the suite goes green over a guard that is switched off, and closing issue
#36 raises a board contradiction whose documented remedy is to clear the entry,
which destroys the obligation instead of meeting it.

WHAT THE ``origin`` CONSTANTS BELOW ARE, AND WHY THEY DO NOT SPELL "rebuild".
``rebuild`` IS a verb name, so a string constant spelling it in a module below
the CLI layer is exactly what the layering guard is for. The origin trail is a
label for a reader of a refusal rather than an import path, so it stays
``tree_rebuild``: a non-verb spelling, in a file named for what the brief asked
for.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.core import (
    config,
    convergence,
    locations,
    routing,
    session,
    tags,
    taxonomy,
    tree_registry,
)
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

    AN ABSENT MUSIC DIRECTORY REFUSES RATHER THAN YIELDING NOTHING, which is the
    same sentence as everything else in this unit and was the one place it was
    not being said. Returning early meant "the volume is not mounted" and "the
    library is empty" arrived at the derivation as one answer, and the derivation
    then handed the check zero placements, which the check read as zero
    destinations, which it read as zero differences, which it read as CONVERGED.
    An empty read is not evidence that a tree is right; it is evidence that
    nothing could be read.
    """
    wanted = {suffix.lower() for suffix in suffixes}
    base = Path(root)
    if not base.is_dir():
        raise refuse(
            "rebuild-derivation-empty",
            f"this library's music directory {str(base)!r} is not there, so "
            f"nothing on disk could be read and no membership could be derived; "
            f"a derivation that read nothing is not evidence that a tree matches "
            f"what this library declares, it is evidence that the question could "
            f"not be asked",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            steps=(
                "mount the volume the library lives on and run this again",
            ),
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"music_dir": str(base)},
        )
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

    A DERIVATION THAT PLACED NOTHING IS A REFUSAL, NOT AN ANSWER, and this is the
    single most expensive thing in the unit. Every question downstream is scoped
    to the destinations this derivation produced: the check compares the
    destinations it names, the write plans on them, and a node under the governed
    root that no destination names is reported as somebody's own playlist rather
    than as damage. So zero placements collapses the whole comparison to nothing
    and every branch reads it the permissive way. Zero destinations gives zero
    differences, zero differences reads as CONVERGED, and a rebuild that derived
    nothing at all then clears the safety flag on a tree it never looked at, with
    the plan empty so the acknowledgment, the volume assertion, the session lock,
    the verified capture and the analysis watch are all skipped on the way past.

    An empty music directory, an unmounted volume, a library whose files were all
    moved, and a taxonomy that places nothing all arrive here as the same value,
    and none of them is evidence about the tree. The honest answer is that the
    question could not be asked.
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
    music = Path(cfg.library.root) / cfg.library.music_dir
    readings = library_truth(music) if truth is None else truth
    placements, gaps = derive(declared, readings, vocal_threshold=vocal_threshold)
    if not placements:
        raise refuse(
            "rebuild-derivation-empty",
            f"deriving this tree's declared membership from "
            f"{str(source)!r} placed no track at all, so there is nothing to "
            f"compare the database against and nothing to write; an empty "
            f"derivation is not evidence that the tree matches what this library "
            f"declares, it is evidence that the derivation could not be made, and "
            f"treating the two as one is what would let a run that read nothing "
            f"clear the flag that says this tree is short",
            # RUN_DOCTOR RATHER THAN MOUNT_LIBRARY_VOLUME, and the difference is
            # a real case rather than a nicety. The unmounted volume is refused
            # one step earlier, by ``library_truth``, which is the only place
            # that knows the directory was not there and which carries the mount
            # remedy. By here the walk SUCCEEDED and returned nothing, so the
            # music directory is present and holds no audio files this build can
            # read. Telling that person to mount a volume they have already
            # mounted sends them to fix something that is not broken.
            remedy=Remedy.RUN_DOCTOR,
            steps=(
                "check that this library's music directory holds the files it is "
                "supposed to; it is present and this walk found nothing in it "
                "that carries tags",
                "run the convergence check, which reports what was and was not "
                "compared without writing anything",
            ),
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"source": str(source), "music_dir": str(music), "not_compared": list(gaps)},
        )
    return placements, gaps


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
    #: Every content identifier this playlist holds MORE THAN ONE row for.
    #:
    #: Carried beside the set rather than being lost inside it. A frozenset over
    #: the rows answers "is this track in this playlist", which is the question
    #: the comparison asks, and silently answers "yes" for a track sitting there
    #: twice. Two ``djmdSongPlaylist`` rows for one pair is a doubled tree inside
    #: one playlist: rekordbox shows the track twice, removing it once leaves the
    #: other, and the additive write cannot take either away. The check that
    #: exists to catch a doubled tree could not see doubling at this depth at all,
    #: and reported such a tree converged.
    doubled: frozenset[str] = frozenset()


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
            members = [str(row.ContentID) for row in db.get_playlist_songs(
                PlaylistID=str(playlist.ID)
            )]
            # COUNTED BEFORE IT IS COLLAPSED. The set is what the comparison
            # needs; the multiplicity is a fact that only exists before the set
            # is taken, and it is the one this walk used to throw away.
            seen: dict[str, int] = {}
            for content_id in members:
                seen[content_id] = seen.get(content_id, 0) + 1
            out.append(
                TreeNode(
                    folder_id=str(folder.ID),
                    folder_display=str(folder.Name),
                    playlist_id=str(playlist.ID),
                    playlist_display=str(playlist.Name),
                    content_ids=frozenset(seen),
                    doubled=frozenset(
                        content_id for content_id, count in seen.items() if count > 1
                    ),
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

    THE DESTINATION SET IS THE UNION OF WHAT THIS RUN DERIVED AND WHAT A PREVIOUS
    WRITE RECORDED, and taking only the first half is what let a shrinking
    library go unnoticed. Iterating the placements alone means a destination that
    loses ALL of its declared tracks simply stops being a destination: nothing
    resolves to its node, so the node falls into ``foreign``, which is the set
    reserved for playlists a person curated and which is deliberately not a
    difference. Its whole contents leave the comparison in silence and the tree
    reports converged with a playlist full of tracks nothing declares. Carrying
    the recorded destinations forward means that playlist is still compared, its
    contents are reported as unexpected, and a person decides.
    """
    by_ids = {(node.folder_id, node.playlist_id): node for node in nodes}
    by_display: dict[tuple[str, str], list[TreeNode]] = {}
    for node in nodes:
        by_display.setdefault(
            (node.folder_display, node.playlist_display), []
        ).append(node)

    derived = {(entry.bucket, entry.sub) for entry in placements}
    wanted = set(derived)
    if record is not None:
        wanted |= {(entry.bucket, entry.sub) for entry in record.nodes}

    out: list[Destination] = []
    for bucket, sub in sorted(wanted):
        names = _declared_display(declared, bucket, sub, derived=(bucket, sub) in derived)
        if names is None:
            # A RECORDED DESTINATION THIS TAXONOMY NO LONGER DECLARES IS SKIPPED,
            # not refused, and this is where an ordinary edit stopped being a
            # one-way door. Removing an additive sub-class, or re-declaring the
            # energy band identifiers, leaves a node record naming destinations
            # the template no longer has. Refusing on that took out BOTH verbs:
            # the rebuild refused, and so did the read-only check somebody is
            # told to run instead, so the remedy refused along with the problem.
            # Skipped, the destination is simply not declared any more: its node
            # is reported as ``undeclared`` so nobody has to guess where it went,
            # its contents fall to ``foreign`` exactly as a playlist a person
            # curated does, and the run continues.
            continue
        folder_display, sub_display = names
        recorded = None if record is None else record.node(bucket, sub)
        node = None
        if recorded is not None:
            node = by_ids.get((recorded.folder_id, recorded.playlist_id))
        if node is None:
            # AMBIGUITY IS NOT RESOLVED BY POSITION. Two nodes under the governed
            # root carrying one display pair leave nothing to choose between, and
            # picking either one sends the write into a playlist that may not be
            # the one holding the tracks. Left unresolved here, it is refused by
            # ``assert_addressable`` with both candidates named.
            candidates = by_display.get((folder_display, sub_display), ())
            node = candidates[0] if len(candidates) == 1 else None
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


def _declared_display(
    declared: taxonomy.Taxonomy, bucket: str, sub: str, *, derived: bool
) -> tuple[str, str] | None:
    """The two display names a destination means, None, or a structured refusal.

    THE SAME MISSING IDENTIFIER MEANS TWO DIFFERENT THINGS depending on where it
    came from, and treating them alike turned an ordinary taxonomy edit into a
    permanent refusal of both verbs.

    ``derived=True`` means this destination came out of THIS RUN'S derivation,
    which reads the active taxonomy and applies its own rules. An identifier that
    derivation produced and that the same taxonomy cannot name is a contradiction
    inside one document, which is a defect rather than a user's edit, and it
    refuses. A bare ``KeyError`` would reach the command-line boundary as an
    internal defect with "report a defect" attached (S4), which is the right
    remedy here and the wrong sentence in the other case.

    ``derived=False`` means it came only from the NODE RECORD, which is a note
    about where a previous write landed and which outlives any edit to the
    template. Removing an additive sub-class or re-declaring the energy bands
    leaves exactly this shape, and it is somebody curating their own library
    rather than anything being wrong. It answers None, and the caller reports it
    instead of refusing.

    THE RECORD ENTRY IS NOT DELETED ON THE STRENGTH OF THIS. A taxonomy edit can
    be reverted, and the node identifier is the only thing that stops a rebuild
    doubling the tree after a rename, so throwing it away the first time somebody
    tries an edit would make the revert expensive. See ``rebuild_tree``.
    """
    try:
        return routing_pass.destination(declared, bucket, sub)
    except KeyError as exc:
        if not derived:
            return None
        raise refuse(
            "routing-destination-renamed",
            f"this rebuild's own derivation placed a track in {bucket}/{sub} and "
            f"this library's taxonomy declares no such destination; one document "
            f"has contradicted itself, and inventing a name for it would create a "
            f"folder nobody chose",
            remedy=Remedy.REPORT_DEFECT,
            steps=(
                "run the convergence check, which reports what this tree holds "
                "and writes nothing",
            ),
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"bucket": bucket, "sub": sub},
        ) from exc


def undeclared_destinations(
    declared: taxonomy.Taxonomy, record: convergence.TreeConvergence | None
) -> tuple[str, ...]:
    """Recorded destinations this taxonomy no longer declares, as stable identifiers.

    REPORTED RATHER THAN REFUSED AND RATHER THAN SILENT. A person who removes a
    sub-playlist from their template has done something ordinary and reversible,
    and the tree still holds the playlist that destination used to name. Refusing
    made the edit a one-way door; saying nothing would leave a playlist under a
    governed root that the report never mentions.
    """
    if record is None:
        return ()
    return tuple(
        sorted(
            f"{entry.bucket}/{entry.sub}"
            for entry in record.nodes
            if _declared_display(declared, entry.bucket, entry.sub, derived=False) is None
        )
    )


def assert_addressable(
    tree_id: str, destinations: Sequence[Destination], nodes: Sequence[TreeNode]
) -> None:
    """Refuse a destination set a name-targeted write cannot tell apart.

    THE XML HALF OF THIS REPOSITORY ALREADY REFUSES THIS EXACT CONDITION and the
    database half did not. ``cratekit.write.trees.DuplicateFolders`` says it
    plainly: "a writer that targets a folder by name cannot tell them apart, so
    it would write to the first one twice and to the second one never". Every
    find-or-create in the guarded writer targets a playlist by the name rekordbox
    shows, so the same sentence is true here and the consequence is worse,
    because this write also records where each destination landed.

    THE THREE WAYS IT GOES WRONG, and all three are refused before anything is
    written.

    **Two declared destinations on one display pair.** An ordinary bucket
    consolidation produces it: somebody renames the Deep House folder to Techno
    in rekordbox, and now two declared destinations both resolve to "Techno" and
    "High". A plan keyed on the display pair merges them into one entry, both
    sets of tracks are written into whichever node the name lookup reaches first,
    and every track in one bucket ends up in two playlists at once.

    **Two declared destinations on one node.** The same collision seen from the
    record's side, and the reason it is permanent: the node map is then rewritten
    so both destinations name one playlist, every later rebuild resolves both to
    it, and the check reports the other one short forever. The rebuild is
    additive, so it cannot undo what it did. A single wrong map entry produces
    the same misfiling with no rename involved at all.

    **One display pair carried by two nodes under the root.** The
    ``DuplicateFolders`` shape itself: the write reaches one of them twice and
    the other never, and which one is decided by row order.

    REFUSED RATHER THAN HALF SERVED. A tree in this condition needs a person to
    say which node is the real one, and doing half the job silently hides that
    until the counts stop adding up.
    """
    by_pair: dict[tuple[str, str], Destination] = {}
    by_node: dict[tuple[str, str], Destination] = {}
    for entry in destinations:
        pair = (entry.folder, entry.playlist)
        clash = by_pair.get(pair)
        if clash is not None:
            raise refuse(
                "tree-unconverged",
                f"the tree {tree_id!r} resolves the declared destinations "
                f"{clash.bucket}/{clash.sub} and {entry.bucket}/{entry.sub} to "
                f"one folder and playlist named {entry.folder!r} and "
                f"{entry.playlist!r}; every write here targets a playlist by the "
                f"name rekordbox shows, so both sets of tracks would go into "
                f"whichever node that name reaches first and each track would sit "
                f"in two playlists at once, and the record written afterwards "
                f"would name one node for both destinations, after which no "
                f"rebuild could ever converge this tree again",
                remedy=Remedy.FIX_CONFIG_VALUES,
                steps=(
                    "give the two folders distinct names in rekordbox, or make "
                    "this library's taxonomy declare distinct names for them",
                    "run the convergence check again, which writes nothing",
                ),
                scope=Scope.RUN,
                origin=("tree_rebuild",),
                detail={
                    "tree_id": tree_id,
                    "folder": entry.folder,
                    "playlist": entry.playlist,
                    "destinations": [
                        f"{clash.bucket}/{clash.sub}",
                        f"{entry.bucket}/{entry.sub}",
                    ],
                },
            )
        by_pair[pair] = entry
        if entry.node is None:
            continue
        node = (entry.node.folder_id, entry.node.playlist_id)
        collided = by_node.get(node)
        if collided is not None:
            raise refuse(
                "tree-unconverged",
                f"the tree {tree_id!r} resolves the declared destinations "
                f"{collided.bucket}/{collided.sub} and "
                f"{entry.bucket}/{entry.sub} to one playlist row; a rebuild would "
                f"file both sets of tracks into it and report the other "
                f"destination short forever, and an additive rebuild cannot take "
                f"either set back out",
                remedy=Remedy.FIX_CONFIG_VALUES,
                steps=(
                    "separate the two destinations in rekordbox, then run the "
                    "rebuild, which rebuilds the node record from what it finds",
                ),
                scope=Scope.RUN,
                origin=("tree_rebuild",),
                detail={
                    "tree_id": tree_id,
                    "node": f"{entry.node.folder_id}/{entry.node.playlist_id}",
                    "destinations": [
                        f"{collided.bucket}/{collided.sub}",
                        f"{entry.bucket}/{entry.sub}",
                    ],
                },
            )
        by_node[node] = entry

    counted: dict[tuple[str, str], int] = {}
    for node in nodes:
        pair = (node.folder_display, node.playlist_display)
        counted[pair] = counted.get(pair, 0) + 1
    doubled = sorted(pair for pair in by_pair if counted.get(pair, 0) > 1)
    if doubled:
        raise refuse(
            "tree-unconverged",
            f"the tree {tree_id!r} holds more than one playlist named "
            + ", ".join(f"{folder!r}/{playlist!r}" for folder, playlist in doubled)
            + "; a writer that targets a playlist by name cannot tell them apart, "
            "so it would write to the first one twice and to the second one never",
            remedy=Remedy.FIX_CONFIG_VALUES,
            steps=(
                "rename or remove the duplicate folder or playlist in rekordbox",
                "run the convergence check again, which writes nothing",
            ),
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={
                "tree_id": tree_id,
                "duplicated": [f"{folder}/{playlist}" for folder, playlist in doubled],
            },
        )


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
    #: How many placements the derivation produced. ZERO IS NOT CONVERGED.
    #:
    #: Carried on the report rather than checked only at the derivation, so the
    #: value is visible to anybody holding one of these and so ``converged``
    #: cannot answer True for a comparison that had nothing on one side. The
    #: derivation refuses before it gets here, and this is the same sentence said
    #: where the answer is actually read.
    derived: int = 0
    #: Every declared destination holding a track more than once, as
    #: ``bucket/sub:content_id``. A doubling an additive write cannot undo.
    doubled: tuple[str, ...] = ()
    #: Destinations the NODE RECORD names that this taxonomy no longer declares.
    #:
    #: NOT A DIFFERENCE, for the same reason ``foreign`` is not one: a person who
    #: edits their template has changed what the declaration says, and the
    #: playlist the old destination named is now an undeclared playlist under a
    #: governed root, which is somebody's own data. Reported so the edit is
    #: visible rather than silent, and so a reader can tell "this playlist is not
    #: compared because nobody declares it" from "this playlist matched".
    undeclared: tuple[str, ...] = ()

    @property
    def differences(self) -> tuple[Difference, ...]:
        """Both directions, in one tuple, because R39 asks for both."""
        return self.missing + self.unexpected

    @property
    def converged(self) -> bool:
        """Whether this tree matches what the library declares. THREE conditions.

        No difference in either direction is the obvious one and it was the only
        one. The other two are the ones that made "converged" mean less than it
        said:

        * a derivation that placed nothing produces no differences BECAUSE it
          produced no destinations, so an empty answer read as a clean one;
        * a playlist holding one track twice produces no difference either, since
          both directions are asked as set membership, and the doubling is
          exactly what an additive rebuild cannot repair.
        """
        return not self.differences and self.derived > 0 and not self.doubled

    def summaries(self) -> tuple[str, ...]:
        """Everything that stands between this tree and a cleared flag.

        THE DOUBLED ROWS ARE IN HERE, not only in their own field, because this
        is the list the clearing call is handed as its evidence. A fact that
        blocks convergence and is absent from the evidence list would let the
        flag be cleared over it.
        """
        return tuple(entry.summary() for entry in self.differences) + tuple(
            f"doubled:{entry}" for entry in self.doubled
        )


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

    IT REFUSES AN UNADDRESSABLE TREE FOR THE SAME REASON THE REBUILD DOES, and
    running it here first is what lets somebody see that condition without
    writing anything. Read-only does not mean permissive: a tree whose
    destinations cannot be told apart has no answer to "does this match", and
    reporting one anyway would be the check agreeing with a write that is about
    to go wrong.
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
    assert_addressable(tree_id, destinations, nodes)
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
    doubled: list[str] = []
    for node in nodes:
        destination = governed.get((node.folder_id, node.playlist_id))
        if destination is None:
            foreign.append(f"{node.folder_display}/{node.playlist_display}")
            continue
        # A DOUBLED ROW IS REPORTED WHETHER OR NOT THE DECLARATION PLACES IT
        # THERE. It is damage in both cases: the declaration asks for the track
        # to be in this playlist ONCE, and a second row is a second copy nobody
        # asked for and nothing here can remove.
        for content_id in sorted(node.doubled & active):
            doubled.append(f"{destination.bucket}/{destination.sub}:{content_id}")
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
        derived=len(placements),
        doubled=tuple(sorted(doubled)),
        undeclared=undeclared_destinations(declared, record),
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
    #: Whether the restore-reconciliation marker for this tree was also closed.
    #:
    #: THREE ANSWERS, AND None COVERS TWO WAYS OF NOT ASKING. True means a marker
    #: was open and this rebuild closed it on the evidence of the check. False
    #: means the question was asked and there was nothing open to close.
    #:
    #: None means the question WAS NOT ASKED, and there are exactly two reasons,
    #: named here because a caller reading None as only the first would be wrong:
    #:
    #: 1. the module holding those markers is not present in this build, so there
    #:    was nothing to ask;
    #: 2. this rebuild did not converge, so there was no evidence to ask on. A
    #:    marker is closed only by a check reporting no difference, never by a
    #:    rebuild having run, so a rebuild that still differs must leave it alone.
    #:
    #: ``cleared`` distinguishes them: False there means the second reason.
    #: See :func:`close_restore_marker`.
    restore_marker_closed: bool | None = None

    @property
    def repaired(self) -> int:
        return 0 if self.membership is None else self.membership.added


#: The actor a rebuild records when it closes a restore-reconciliation marker.
#: A name for an operation, not a person and not a verb: the closure is not
#: somebody's judgement, it is a check reporting no difference.
REBUILD_ACTOR = "tree-rebuild"


def _reconcile():  # type: ignore[no-untyped-def]
    """``cratekit.core.reconcile`` if this build has it, else None. Never raises.

    RESOLVED AT CALL TIME AND THAT IS DELIBERATE. That module lands with U32, on
    a branch this one has not met yet, so a module-level import would make this
    module unimportable until it does, and a hard requirement on a module that
    does not exist is not a handoff, it is a breakage. The same shape U32's own
    ``restore._convergence_module`` uses to reach this half from the other side,
    written the same way on purpose. Every caller REPORTS the absence rather than
    treating it as an answer.
    """
    try:
        from cratekit.core import reconcile  # noqa: PLC0415
    except ImportError:
        return None
    return reconcile


#: The reconciliation marker kind whose ONLY remedy is this rebuild, and the one
#: thing a rebuild may therefore be exempt from. Spelled here as a NAME rather
#: than as a member so that a build whose ``reconcile`` does not have it exempts
#: NOTHING, which is the restrictive direction.
REBUILD_ANSWERS_KIND = "unconverged-tree"


def assert_no_latched_restore(cfg: config.Config) -> None:
    """Refuse a rebuild while a restore holds a latch this rebuild does not answer.

    THE OTHER HALF OF A BOUNDED EXEMPTION, and the previous version of it named
    the wrong set, which is the whole reason this is written by DERIVATION now.

    The membership write is made with ``Intent.RECOVERY`` so the
    restore-reconciliation latch cannot refuse the rebuild that latch's refusal
    names. ``RECOVERY`` sheds that latch WHOLE, and the latch does not hold on one
    kind of marker, it holds on ``reconcile.LATCHING_KINDS``. Listing the kinds to
    put back by hand meant naming ``EFFECT`` and missing ``IN_FLIGHT_RESTORE``,
    which is the record that a restore started and was not seen to finish. That
    marker is reachable without contrivance: a restore writes it before its first
    destructive step and retracts it at the step that completes, so a process
    killed between marking the trees unconverged and finishing leaves the trees
    flagged AND the latch standing. The user is then told to rebuild, and the
    rebuild proceeded against a library whose database and coupled state are at
    different generations, which is exactly what that latch exists to refuse. U32
    argued its RECOVERY exemption for a restore that FINISHES; a rebuild borrowed
    it for a different act.

    SO THE SET IS DERIVED FROM THE LATCH'S OWN, MINUS ONE NAMED KIND, in the
    direction that makes a kind added later HELD by default. That is the same
    argument ``tree_registry.NOT_REBUILDABLE`` makes for deriving its half rather
    than listing it: a member nobody has classified must land on the restrictive
    side. The one subtraction is the unconverged-tree kind, whose only remedy is
    this function, and it is subtracted by NAME so that a build without it
    subtracts nothing.

    IT MAY WELL SUBTRACT NOTHING TODAY. U32 settled ownership of tree shortness
    on ``core.convergence`` and its ``LATCHING_KINDS`` does not include the tree
    kind, so on a merged build this puts the entire latch back and the exemption
    is inert. That is the correct outcome rather than a wasted mechanism: the
    exemption exists so that a latch cannot condemn its own remedy, and it costs
    nothing when no latch is doing so.
    """
    reconcile = _reconcile()
    if reconcile is None:
        return
    outstanding = reconcile.outstanding(cfg)
    # An absent LATCHING_KINDS means an older or newer shape this build cannot
    # interrogate, and the answer is to hold on EVERYTHING outstanding rather
    # than on nothing. A default that shrank the held set would be this rebuild
    # deciding, on no evidence, that a marker it has never heard of is its own
    # business to ignore.
    latching = getattr(reconcile, "LATCHING_KINDS", None)
    held = [
        record
        for record in outstanding
        if (latching is None or record.marker.kind in latching)
        and str(record.marker.kind) != REBUILD_ANSWERS_KIND
    ]
    if not held:
        return
    raise refuse(
        "tree-unconverged",
        f"a restore of this library left {len(held)} thing(s) latched that a "
        f"rebuild does not answer for: an effect it could not undo out in the "
        f"world, or a restore that started and was not seen to finish. A rebuild "
        f"is exempt from the markers whose own remedy it is and from nothing "
        f"else, because writing membership into a library whose database and "
        f"coupled state are at different generations is what that latch exists "
        f"to refuse",
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=(
            "finish or restart the restore that did not complete, if one is "
            "recorded as in flight",
            "close each outstanding restore effect by deciding what to do about "
            "it, then run this rebuild again",
        ),
        scope=Scope.RUN,
        origin=("tree_rebuild",),
        detail={
            "markers": [record.marker.marker_id for record in held],
            "kinds": sorted({str(record.marker.kind) for record in held}),
        },
    )


def close_restore_marker(cfg: config.Config, tree_id: str) -> bool | None:
    """Close a legacy UNCONVERGED_TREE marker for this tree, on evidence. Three answers.

    TWO RECORDS EXISTED FOR ONE FACT AND THIS IS THE JOINT BETWEEN THEM.
    ``cratekit.core.convergence`` holds a per-tree unconverged flag, set by the
    out-of-band restore detection and read by every governed write to that tree.
    ``cratekit.core.reconcile`` holds an ``UNCONVERGED_TREE`` marker, set by a
    Cratekit restore that landed on the far side of a cutover and read by the
    session gate every destructive session passes through. They describe one
    condition from two sides, and a rebuild that cleared only one of them left
    the library refusing every destructive session with no exit except a bare
    disposition, which is the softening path U32's own register entry warns
    against.

    U32'S FIX ROUND SETTLED THE OWNERSHIP ON ``convergence``, and this function is
    what makes the transition safe rather than a second answer. Its restore now
    hands the trees over with ``convergence.mark_unconverged`` and only falls back
    to writing its own marker on a build where ``convergence`` is absent. So on a
    merged build there should be no tree marker to close, and this normally
    answers False. What it exists for is the window: a marker written by a build
    that had ``reconcile`` and not ``convergence`` outlives the merge, and without
    this it would stand open forever because the fact it records is now cleared
    somewhere else.

    IT CLOSES ONLY ON THE EVIDENCE OF A REAL CHECK. The caller reaches this after
    the second convergence check reported no difference at all. A marker closed
    with a verdict and no check would satisfy every test in this repository and
    leave the tree exactly as short as it was.

    IT RETURNS None WHEN THE MODULE IS NOT PRESENT, reported up the return value
    and into the log rather than swallowed, because "the other record had nothing
    open" and "the other record was not reached" are different facts and reading
    one as the other is the defect shape this whole round is about.

    THE DUPLICATION IS NOT FULLY RESOLVED AND NEEDS A FOLLOW-UP. U32 registered
    it: the commit that discharges its pending entry deletes the fallback branch
    in ``restore._hand_tree_shortness_over`` and the whole
    ``reconcile.Kind.UNCONVERGED_TREE`` path behind it, at which point this
    function has nothing left to close and comes out with them.
    """
    reconcile = _reconcile()
    if reconcile is None:
        logger.warning(
            "the restore reconciliation record is not part of this build, so the "
            "tree %s may still carry an open marker there; the convergence flag "
            "was cleared and the other record was NOT reached",
            tree_id,
        )
        return None
    open_ids = [
        record.marker.marker_id
        for record in reconcile.outstanding(cfg)
        if record.marker.kind is reconcile.Kind.UNCONVERGED_TREE
        and record.marker.identity == tree_id
    ]
    for marker_id in open_ids:
        reconcile.close_marker(
            cfg,
            marker_id,
            disposition=reconcile.Disposition.REPAIRED,
            actor=REBUILD_ACTOR,
            note=(
                "a full-scope rebuild derived this tree's membership again and "
                "the convergence check that followed it reported no difference"
            ),
        )
    return bool(open_ids)


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

    THE LATCHES THIS RUN IS AND IS NOT HELD BY, stated as what is SHED rather
    than as what is declared, because those are different lists and an earlier
    version of this docstring counted the declarations and called it the
    exemption. That sentence claimed three shed things, all naming this function
    as their remedy. One of them was never held at all, and a fourth thing was
    shed and not named.

    Two declarations are made, and each sheds more than this function needs:

    * ``purpose=Purpose.REBUILD`` on the membership write, which sheds the
      convergence flag on THIS tree and the out-of-band restore REFUSAL. The
      detection behind that refusal still runs and still marks every native tree.
    * ``intent=Intent.RECOVERY`` on the session gate, which sheds the
      unresolved-session latch and the restore-reconciliation latch, both whole.

    Both of those are wider than the remedy, so the surplus is put back HERE and
    by name, before anything is written:

    * ``session.assert_no_unresolved_session``, whose remedy is a restore rather
      than a rebuild. A rebuild over a library whose last commit could not be
      read back would be adding to something nobody can vouch for.
    * :func:`assert_no_latched_restore`, which puts back everything
      ``reconcile.LATCHING_KINDS`` holds except the unconverged-tree kind. That
      derivation is the fix for the gap: the hand-written version named EFFECT
      and silently shed IN_FLIGHT_RESTORE, so a rebuild ran over a library whose
      database and coupled state were at different generations.

    SO WHAT IS ACTUALLY SHED IS TWO THINGS, and on a merged build possibly three:
    this tree's convergence flag, the out-of-band restore refusal, and the
    reconciliation latch's unconverged-tree markers IF that build latches on them
    at all. U32's current shape does not, which makes the third one inert rather
    than wrong.
    """
    source = registry.derivation_source(tree_id)
    tree_registry.assert_rebuildable(tree_id, source)
    session.assert_no_unresolved_session(cfg)
    assert_no_latched_restore(cfg)
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
    standing = read_tree(db, root_id)
    destinations = resolve_destinations(declared, placements, standing, record)
    assert_addressable(tree_id, destinations, standing)
    by_key = {(entry.bucket, entry.sub): entry for entry in destinations}

    # THE PLAN IS KEYED ON THE DISPLAY PAIR BECAUSE THE WRITER TARGETS BY NAME,
    # and that is safe only because ``assert_addressable`` has just refused every
    # way two destinations could share one pair. Without it two destinations
    # merged into one entry here and every track in one bucket was written into
    # the other bucket's playlist as well.
    plan: dict[tuple[str, str], list[str]] = {}
    for entry in placements:
        destination = by_key[(entry.bucket, entry.sub)]
        plan.setdefault((destination.folder, destination.playlist), []).append(entry.location)

    if not plan:
        # UNREACHABLE BY CONSTRUCTION AND REFUSED ANYWAY. ``declared_membership``
        # already refuses an empty derivation and a non-empty one always produces
        # a plan, so this cannot fire today. It is here because of what the old
        # ``if plan else None`` did when it could: an empty plan skipped
        # ``write_tree_membership`` entirely, and with it the acknowledgment, the
        # volume identity assertion, the session lock, the verified capture and
        # the analysis watch, on the exact path that then went on to clear the
        # safety flag. A guard whose absence costs every gate at once is worth
        # keeping after the reason it fired is gone.
        raise refuse(
            "rebuild-derivation-empty",
            f"the rebuild for {tree_id!r} produced no plan, so no gate would be "
            f"taken and nothing would be written, and the run would still be in "
            f"a position to clear this tree's unconverged flag",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"tree_id": tree_id, "derived": len(placements)},
        )

    membership = trees.write_tree_membership(
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
        intent=session.Intent.RECOVERY,
    )

    # THE NODE RECORD COMES FROM THE DESTINATION'S OWN NODE FIRST, and from the
    # freshly read tree only for the destinations that had none. Rebuilding the
    # whole record from a display-name lookup discarded the resolved identifier
    # this unit exists to preserve: the lookup was a dict comprehension, so where
    # two nodes carried one display pair the last one won and BOTH destinations
    # were recorded against it. ``assert_addressable`` now refuses that shape, and
    # taking the identifier from ``entry.node`` means the resolved answer is never
    # thrown away and re-derived by the weaker method in the first place.
    landed = read_tree(db, root_id)
    by_display: dict[tuple[str, str], list[TreeNode]] = {}
    for node in landed:
        by_display.setdefault(
            (node.folder_display, node.playlist_display), []
        ).append(node)
    recorded: list[convergence.DestinationNode] = []
    for entry in destinations:
        node = entry.node
        if node is None:
            fresh = by_display.get((entry.folder, entry.playlist), ())
            # Exactly one, or nothing is recorded for this destination. Two
            # candidates would be the ambiguity refused above arriving after the
            # write, and recording either is recording a guess.
            node = fresh[0] if len(fresh) == 1 else None
        if node is None:
            continue
        recorded.append(
            convergence.DestinationNode(
                bucket=entry.bucket,
                sub=entry.sub,
                folder_id=node.folder_id,
                playlist_id=node.playlist_id,
            )
        )
    # A RECORDED DESTINATION THIS TAXONOMY NO LONGER DECLARES IS CARRIED FORWARD
    # rather than dropped, and the reason is the one this record exists for. It
    # was skipped above, so it is not in ``destinations``, and a whole-record
    # replacement would therefore delete it. A taxonomy edit is reversible, and
    # the node identifier is the only thing that stops a rebuild doubling the
    # tree after somebody renames a folder, so deleting it the first time an edit
    # is tried would make the revert expensive in exactly the way this unit
    # exists to prevent. Kept, the entry is inert: nothing resolves through it
    # while its destination is undeclared, and the report names it.
    taken = {(entry.bucket, entry.sub) for entry in recorded}
    claimed = {(entry.folder_id, entry.playlist_id) for entry in recorded}
    for entry in () if record is None else record.nodes:
        if (entry.bucket, entry.sub) in taken:
            continue
        if _declared_display(declared, entry.bucket, entry.sub, derived=False) is not None:
            # Declared, and not written back, which means it resolved to no node
            # this run: the playlist it named is gone. That entry IS dropped,
            # because it is a dangling pointer rather than a note about an edit.
            continue
        if (entry.folder_id, entry.playlist_id) in claimed:
            # Its node now belongs to a destination that IS declared. Keeping
            # both would be the two-destinations-one-node record the injectivity
            # check refuses, and the live one is the one worth keeping.
            continue
        recorded.append(entry)

    if recorded:
        # The map is validated as a bijection on construction, so a record that
        # would name one node for two destinations is refused HERE, before it can
        # be persisted and read back by every later rebuild.
        convergence.assert_injective(tree_id, recorded)
        # REPLACED, NOT MERGED, because this run resolved the union of every
        # destination it derived and every destination the record already held,
        # so a recorded destination missing from this list is one whose node no
        # longer exists. Merging keeps that dangling entry, and a dangling entry
        # holding an identifier some other destination now resolves to is exactly
        # the two-destinations-one-node record the injectivity check refuses.
        convergence.record_nodes(cfg, tree_id, recorded, replace_all=True)

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
    marker_closed: bool | None = None
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
        # BOTH RECORDS, on one piece of evidence. See ``close_restore_marker``
        # for why there are two and what still owes a collapse.
        marker_closed = close_restore_marker(cfg, tree_id)
    else:
        logger.warning(
            "the tree %s still differs from what this library declares in %d "
            "place(s) after a rebuild, so it stays unconverged",
            tree_id,
            len(after.summaries()),
        )

    return RebuildReport(
        tree_id=tree_id,
        root_id=root_id,
        before=before,
        after=after,
        membership=membership,
        cleared=cleared,
        restore_marker_closed=marker_closed,
    )


__all__ = [
    "DERIVATIONS",
    "REBUILD_ACTOR",
    "REBUILD_ANSWERS_KIND",
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
    "assert_addressable",
    "assert_no_latched_restore",
    "check",
    "close_restore_marker",
    "declared_membership",
    "derive_from_taxonomy",
    "library_truth",
    "read_tree",
    "read_truth",
    "rebuild_tree",
    "report_convergence",
    "resolve_destinations",
    "undeclared_destinations",
]
