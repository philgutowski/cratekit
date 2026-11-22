"""Rebuilding a governed tree, and saying whether it matches the declaration (U36).

A database-native tree's one repair path: no XML export can be re-imported (an
import would replace the tree, U9's A2) and an incremental sync sees nothing
to do, so the rebuild derives the whole membership again from the declared
taxonomy and the files on disk, with no watermark. It converges across a
rename (destinations resolve through recorded node identifiers first,
:mod:`cratekit.write.convergence_check`), adds and never removes (a hand made
membership is somebody's data), and is idempotent across a crash.

"LIBRARY TRUTH" is the files on disk and their tags, read live: an export is
stale, and deriving from the database's own playlist rows makes every check a
tautology.

LAYER: write; names no verb (D2). The ``tests/_pending.py`` key relies on the
filename. The ``origin`` labels say ``tree_rebuild`` because ``rebuild`` is a
verb name, which the layering guard forbids as a string constant below the CLI.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass, fields, replace
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.core import (
    active_taxonomy,
    analysis_store,
    config,
    convergence,
    locations,
    rb_writer,
    routing,
    session,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import genre_favorites, routing_pass, trees
from cratekit.write.convergence_check import (
    ConvergenceReport,
    Destination,
    Difference,
    Direction,
    _declared_display,
    _uncompared_playlist_subs,
    _under_recorded_folders,
    assert_addressable,
    by_display_pair,
    check,
    only_one,
    plan_destinations,
    resolve_destinations,
    undeclared_destinations,
)
from cratekit.write.tree_read import DeclaredPlacement, TreeNode, read_tree

logger = logging.getLogger(__name__)

#: The workflow name a rebuild records in the session log. A name for an
#: operation, not a verb: the CLI layer owns verb names (D2).
REBUILD_WORKFLOW = "tree-rebuild"

#: The dimension name reported when this library has no vocal calibration, so
#: the additive vocal sub-playlists could not be derived this run.
VOCAL_DIMENSION = "vocal"

#: The envelope warning code a surface carries when the vocal dimension was not
#: derived this run (R-316).
VOCAL_NOT_COMPARED = "vocal-dimension-not-compared"

#: The envelope warning code a resort carries when it left a membership where it
#: was (R-312). The engine adds and never removes, so a track whose genre or band
#: changed sits in its new sub and its old one until a person takes it out.
LEFT_BEHIND = "membership-left-behind"

#: How many leftovers one warning names before it counts the rest. A back
#: catalogue can leave thousands behind, and an envelope is read by a person.
LEFT_BEHIND_NAMED = 20


# ---------------------------------------------------------------------------
# What the declaration says a tree should hold
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Truth:
    """One file on disk and the three readings the declared rules route on.

    A value rather than a path, so the derivation is pure and testable with no
    audio files, and the file input happens once in :func:`read_truth`.
    """

    location: str
    genre: str | None = None
    energy: int | None = None
    voxlevel: int | None = None


_TRUTH_FIELDS = ("genre", "energylevel", "voxlevel")


def read_truth(path: Path) -> Truth:
    """The three tag readings for one file, through ONE container open (U250).

    Through :mod:`cratekit.core.tags`. It never raises for an unreadable file:
    an absent reading routes to the declared fallback, visibly, where an
    exception would abandon the rebuild over one stray file.
    """
    values = tags.read_tags(path, _TRUTH_FIELDS)
    return Truth(
        location=str(path),
        genre=values["genre"],
        energy=tags.whole_number(values["energylevel"], field="energylevel", path=path),
        voxlevel=tags.whole_number(values["voxlevel"], field="voxlevel", path=path),
    )


def library_truth(
    root: Path | str,
    *,
    suffixes: Sequence[str] = tags.SUPPORTED_SUFFIXES,
    reader: Callable[[Path], Truth] = read_truth,
) -> Iterator[Truth]:
    """Every taggable file under ``root``, in a stable order, with its readings.

    The suffix set comes from the tag module's own table, so a container it
    learns is never silently absent from a rebuild (P3). Sorted, so two runs
    over an unchanged library produce byte-identical plans. A generator: a
    caller needing two passes materializes it.

    AN ABSENT MUSIC DIRECTORY REFUSES RATHER THAN YIELDING NOTHING, which the
    check would read as zero differences and CONVERGED.
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
            steps=("mount the volume the library lives on and run this again",),
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

    The rules are :mod:`cratekit.core.routing`'s, called rather than restated,
    so a rebuild and the routing pass cannot disagree on where a track goes.

    AN ADDITIVE SUB-PLAYLIST THIS DERIVATION HAS NO SIGNAL FOR IS A REFUSAL (P4):
    skipping it would write a tree missing a whole dimension that the check
    never compares, and report it converged.

    A LIBRARY WITH NO VOCAL CALIBRATION IS A GAP, NOT A REFUSAL: the threshold
    is passed in (D7), and with None the dimension is named as not compared.
    """
    # THE VOCAL CLASSES ONLY (U119). A playlist derived class comes from the
    # database through the genre favorites engine, added by callers with a handle.
    additive = tuple(
        entry
        for entry in declared.sub_classes
        if entry.additive and entry.signal == taxonomy.SIGNAL_VOX
    )
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

    gaps = not_derived(declared, vocal_threshold=vocal_threshold)

    out: list[DeclaredPlacement] = []
    for entry in truth:
        resolution = routing.resolve_bucket(declared, entry.genre)
        sub = routing.energy_sub(
            declared, resolution.bucket_id, entry.energy, source_genre=entry.genre or ""
        )
        if sub is not None:
            # None is a real answer: the taxonomy declares no place below that
            # bucket for this track.
            out.append(DeclaredPlacement(entry.location, resolution.bucket_id, sub.id))
        # THE GENRE SUB BESIDE THE BAND (U155), from the same genre reading, so it
        # is never a gap. Both the rebuild and ``route resort`` write it.
        genre = routing.genre_sub(declared, resolution.bucket_id, entry.genre)
        if genre is not None:
            out.append(DeclaredPlacement(entry.location, resolution.bucket_id, genre.id))
        if vocal_threshold is not None and routing.routes_with_vox(
            entry.voxlevel, vocal_threshold
        ):
            out.extend(
                DeclaredPlacement(entry.location, resolution.bucket_id, sub_class.id)
                for sub_class in additive
            )
    return tuple(out), gaps


def _additive_ids(declared: taxonomy.Taxonomy, signal: str) -> set[str]:
    """The additive sub class ids the declaration derives from ``signal``."""
    return {
        entry.id for entry in declared.sub_classes if entry.additive and entry.signal == signal
    }


def not_derived(
    declared: taxonomy.Taxonomy, *, vocal_threshold: float | None
) -> tuple[str, ...]:
    """The declared dimensions a derivation over these inputs does not compare.

    The rule :func:`derive_from_taxonomy` returns as its gaps. It depends on the
    declaration and the threshold alone, so a surface that never held the
    derivation's report can still say what it left out (R-316).
    """
    additive = bool(_additive_ids(declared, taxonomy.SIGNAL_VOX))
    return (VOCAL_DIMENSION,) if additive and vocal_threshold is None else ()


def not_compared_warnings(not_compared: Iterable[str]) -> tuple[dict[str, str], ...]:
    """The envelope warning for a declared vocal dimension this run did not file.

    A warning, not a refusal: the rest of the tree is right. One wording, in
    ``handlers.drift_warnings``' ``{code, message}`` shape. The export route
    reports the gap as ``not_derived`` instead.
    """
    if VOCAL_DIMENSION not in tuple(not_compared):
        return ()
    return (
        {
            "code": VOCAL_NOT_COMPARED,
            "message": (
                "this library's taxonomy declares a vocal sub-playlist and no vocal "
                "calibration was read, so no track was filed into it this run and "
                "nothing checked whether one belonged there"
            ),
        },
    )


def _uncompared_subs(declared: taxonomy.Taxonomy, not_compared: Sequence[str]) -> set[str]:
    """The sub class ids whose dimension a run named as not compared."""
    skipped = _uncompared_playlist_subs(declared, not_compared)
    if VOCAL_DIMENSION in tuple(not_compared):
        skipped |= _additive_ids(declared, taxonomy.SIGNAL_VOX)
    return skipped


def left_behind(
    after: "ConvergenceReport", declared: taxonomy.Taxonomy
) -> tuple["Difference", ...]:
    """The unexpected memberships of one check that a person can act on.

    A dimension this run did not derive is left out, or with no vocal
    calibration a correctly filled vocal playlist would read as unexpected.
    """
    skipped = _uncompared_subs(declared, after.not_compared)
    if not skipped:
        return after.unexpected
    return tuple(entry for entry in after.unexpected if entry.sub not in skipped)


def left_behind_record(entry: "Difference") -> dict[str, str | None]:
    """One leftover as a worker writes it into its item's report."""
    return {
        "bucket": entry.bucket,
        "sub": entry.sub,
        "folder": entry.folder,
        "playlist": entry.playlist,
        "content_id": entry.content_id,
        "location": entry.location,
    }


def left_behind_message(records: Iterable[Mapping[str, Any]], *, listed_in: str) -> str | None:
    """The sentence naming what an additive write left in the tree, or None.

    Named so a person can remove it, because nothing in this build deletes a
    membership row (R-312). The count is the whole set, the names are capped,
    ``listed_in`` holds them all; sorted.
    """
    found = sorted(
        f"{entry['folder']}/{entry['playlist']}: "
        f"{entry.get('location') or 'row ' + str(entry.get('content_id'))}"
        for entry in records
    )
    if not found:
        return None
    named = found[:LEFT_BEHIND_NAMED]
    rest = len(found) - len(named)
    return (
        f"this verb adds and never removes, so {len(found)} membership(s) the "
        f"declaration does not place are still in the tree: {'; '.join(named)}"
        + (f"; and {rest} more" if rest else "")
        + ". A track whose genre or energy band changed is in its new playlist and "
        "its old one. Remove one in rekordbox if it no longer belongs there. "
        f"Every one is listed in {listed_in}"
    )


def left_behind_warnings(
    records: Iterable[Mapping[str, Any]], *, listed_in: str
) -> tuple[dict[str, str], ...]:
    """The envelope warning over :func:`left_behind_message`, or nothing."""
    message = left_behind_message(records, listed_in=listed_in)
    return () if message is None else ({"code": LEFT_BEHIND, "message": message},)


#: One derivation per source a tree may cut over on. Its key set is asserted to
#: be exactly ``tree_registry.REBUILDABLE``: a rebuildable source with no
#: derivation fails at the moment the rebuild is needed.
DERIVATIONS: Mapping[tree_registry.DerivationSource, Callable[..., Any]] = MappingProxyType(
    {tree_registry.DerivationSource.TAXONOMY: derive_from_taxonomy}
)


def other_declared_trees(declared: taxonomy.Taxonomy) -> dict[str, str]:
    """Every place the declaration names that is not the routing tree, id to display (U219).

    Derived from the taxonomy's own ``Node`` fields, never listed, so a node a
    later template adds is never handed the routing tree's membership.
    """
    out: dict[str, str] = {}
    for entry in fields(declared):
        value = getattr(declared, entry.name)
        if entry.name == "tree" or not isinstance(value, taxonomy.Node):
            continue
        out[value.id] = value.display
    out.pop(declared.tree.id, None)
    return out


def derivable(declared: taxonomy.Taxonomy, tree_id: str) -> bool:
    """Whether the taxonomy derivation describes this tree's membership (U219).

    The derivation has the ROUTING tree's shape. A tree the declaration names
    as something else holds what its verbs put there; a tree it does not name
    is read as a routing tree under another identifier.
    """
    return tree_id not in other_declared_trees(declared)


def assert_derivable(declared: taxonomy.Taxonomy, tree_id: str) -> None:
    """Refuse to derive membership for a tree the taxonomy derivation does not describe.

    At the derivation, the one call every reader and writer makes (R-789).
    """
    others = other_declared_trees(declared)
    if tree_id not in others:
        return
    raise refuse(
        "rebuild-tree-not-derivable",
        f"the tree {tree_id!r} is this library's {others[tree_id]!r}, which holds "
        f"what the verbs that write it put there and not anything a tag decides, "
        f"so no rebuild can reproduce it; deriving it from the taxonomy would file "
        f"the routing tree's genre and energy folders under {others[tree_id]!r}",
        remedy=Remedy.FIX_COMMAND_LINE,
        steps=(
            f"rebuild or resort the routing tree, {declared.tree.id!r}, which is "
            f"the one tree the taxonomy derives",
        ),
        scope=Scope.RUN,
        origin=("tree_rebuild",),
        detail={"tree_id": tree_id, "routing_tree": declared.tree.id},
    )


def detect_restore(cfg: config.Config) -> None:
    """Run the restore detection over the database as it now stands, and close it.

    Read only on the database; it writes the convergence record, so the
    acceptance gate asked after it shows a current record (U219).
    """
    handle = rb_writer.open_db(cfg=cfg)
    try:
        convergence.detect_out_of_band_restore(cfg, handle, tree_registry.read(cfg))
    finally:
        rb_writer.close_db(handle)


def accept_as_it_stands(
    cfg: config.Config, declared: taxonomy.Taxonomy, tree_id: str, *, actor: str
) -> None:
    """Record a named person accepting a marked tree no rebuild can reproduce (U219).

    Only a tree :func:`derivable` rules out, so this is never the flag's off
    switch for a tree a rebuild can repair. A disposition, not a clearing: the
    flag stays set, the refusal is answered by ``actor``, and a later restore
    clears the answer and marks it again.
    """
    if derivable(declared, tree_id):
        # No surface asks this for a routing tree; one that did is a defect.
        raise refuse(
            "refused-by-policy",
            f"the tree {tree_id!r} is one a rebuild reproduces, so it is cleared "
            f"by a rebuild on the evidence of a check and never accepted as it stands",
            remedy=Remedy.REPORT_DEFECT,
            steps=(f"run the rebuild for {tree_id!r}",),
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"tree_id": tree_id},
        )
    registry = tree_registry.read(cfg)
    handle = rb_writer.open_db(cfg=cfg)
    try:
        # The detection first, as a rebuild runs it, so the fingerprint recorded
        # below blesses nothing it has not marked.
        convergence.detect_out_of_band_restore(cfg, handle, registry)
        record = convergence.read(cfg).tree(tree_id)
        reason = "a restore" if record is None or not record.reason else record.reason
        convergence.clear_unconverged(
            cfg,
            tree_id,
            differences=(),
            disposition=convergence.Disposition(
                actor=actor,
                note=f"accepted as it stands after {reason}; no rebuild can reproduce it",
            ),
        )
        # The latch as well as the flag: ``assert_tree_writable`` refuses on a
        # fingerprint the database has gone behind, and an acceptance writes
        # nothing, so it records the database as it now stands.
        convergence.record_fingerprint(cfg, handle)
    finally:
        rb_writer.close_db(handle)


def declared_membership(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    *,
    tree_id: str,
    source: tree_registry.DerivationSource | None,
    vocal_threshold: float | None,
    truth: Iterable[Truth] | None = None,
) -> tuple[tuple[DeclaredPlacement, ...], tuple[str, ...]]:
    """What the declaration says the tree holds, by the source the registry records.

    ``tree_id`` is checked first (U219) by :func:`assert_derivable`, before a
    file is read. ``truth`` defaults to a live walk of the music directory; a
    caller supplying it supplies the READINGS, never the rules.

    A DERIVATION THAT PLACED NOTHING IS A REFUSAL, NOT AN ANSWER, since zero
    placements reads downstream as CONVERGED and clears the flag.
    """
    assert_derivable(declared, tree_id)
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
            # Not the mount remedy: ``library_truth`` refuses an absent directory,
            # so by here the walk succeeded and found nothing tagged.
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
# The rebuild
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RebuildReport:
    """What one rebuild wrote, and where the tree stood after it.

    ``before`` and ``after`` are both kept, so "nothing was wrong" and "it was
    wrong and is fixed" read differently.
    """

    tree_id: str
    root_id: str
    before: ConvergenceReport
    after: ConvergenceReport
    membership: trees.MembershipReport | None = None
    cleared: bool = False
    #: Whether the restore-reconciliation marker for this tree was also closed.
    #: True: one was open and is closed on the check's evidence. False: none was
    #: open. None: not asked, because the ``reconcile`` module is absent from
    #: this build, or because the rebuild did not converge (``cleared`` False).
    #: See :func:`close_restore_marker`.
    restore_marker_closed: bool | None = None

    @property
    def repaired(self) -> int:
        return 0 if self.membership is None else self.membership.added


#: The actor a rebuild records when it closes a restore-reconciliation marker:
#: an operation, since the closure is a check reporting no difference.
REBUILD_ACTOR = "tree-rebuild"


def _reconcile():  # type: ignore[no-untyped-def]
    """``cratekit.core.reconcile`` if this build has it, else None. Never raises.

    Resolved at call time so this module imports on a build without it; every
    caller reports the absence rather than treating it as an answer.
    """
    try:
        from cratekit.core import reconcile  # noqa: PLC0415
    except ImportError:
        return None
    return reconcile


#: The reconciliation marker kind whose ONLY remedy is this rebuild. A name, not
#: a member, so a build whose ``reconcile`` lacks it exempts nothing.
REBUILD_ANSWERS_KIND = "unconverged-tree"


def assert_no_latched_restore(cfg: config.Config) -> None:
    """Refuse a rebuild while a restore holds a latch this rebuild does not answer.

    The membership write's ``Intent.RECOVERY`` sheds the restore-reconciliation
    latch WHOLE, so this puts it back: every kind ``reconcile.LATCHING_KINDS``
    holds except the unconverged-tree kind, whose only remedy is this rebuild.
    Derived from the latch's own set, so a kind added later is held by default.
    """
    reconcile = _reconcile()
    if reconcile is None:
        return
    outstanding = reconcile.outstanding(cfg)
    # No LATCHING_KINDS: a shape this build cannot interrogate, so hold on
    # everything outstanding rather than on nothing.
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

    ``convergence`` owns the condition (U32), so this normally answers False; it
    closes a marker a build with ``reconcile`` and no ``convergence`` left
    behind. Reached only after a check reported no difference. None means the
    module is absent, logged, because "nothing open" and "not reached" differ.
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


def with_favorites(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    rows: Sequence[trees.ContentRow],
    placements: Sequence[DeclaredPlacement],
    not_compared: Sequence[str],
    *,
    tree_id: str,
) -> tuple[tuple[DeclaredPlacement, ...], tuple[str, ...]]:
    """The derived placements with the genre Favorites beside them (U119).

    The one dimension derived from the database: which tracks are favourites is
    a playlist and which folder they sit in is the tree. Only for the routing
    tree the class is declared under. An unreadable source is named as not
    compared, the vocal gap's shape, so the check never reads "matching" over it.
    """
    if tree_id != declared.tree.id or genre_favorites.favorites_class(declared) is None:
        return tuple(placements), tuple(not_compared)
    extra, gaps = genre_favorites.placements(cfg, db, declared, registry, rows)
    return (*placements, *extra), (*not_compared, *gaps)


@dataclass(frozen=True, slots=True)
class _Tree:
    """The fixed inputs of one rebuild or check of one tree, so each step names only what varies."""

    cfg: config.Config
    db: Any
    tree_id: str
    registry: tree_registry.Registry
    declared: taxonomy.Taxonomy
    rows: tuple[trees.ContentRow, ...]
    root_exists: Callable[[str], bool]
    prefix_map: Sequence[locations.PrefixRule] | None = None
    analysis_roots: Iterable[Path | str] = ()
    workflow: str = REBUILD_WORKFLOW

    def favorites(
        self, placements: Sequence[DeclaredPlacement], not_compared: Sequence[str]
    ) -> tuple[tuple[DeclaredPlacement, ...], tuple[str, ...]]:
        return with_favorites(
            self.cfg, self.db, self.declared, self.registry, self.rows, placements,
            not_compared, tree_id=self.tree_id,
        )

    def compare(
        self, placements: Sequence[DeclaredPlacement], not_compared: Sequence[str]
    ) -> ConvergenceReport:
        return check(
            self.cfg,
            self.db,
            tree_id=self.tree_id,
            registry=self.registry,
            declared=self.declared,
            placements=placements,
            rows=self.rows,
            root_exists=self.root_exists,
            prefix_map=self.prefix_map,
            not_compared=not_compared,
        )

    def write(self, plan: dict[tuple[str, str], list[str]]) -> trees.MembershipReport:
        """One membership write under the rebuild purpose and the recovery intent."""
        return trees.write_tree_membership(
            self.cfg,
            self.db,
            tree_id=self.tree_id,
            registry=self.registry,
            plan=plan,
            rows=self.rows,
            root_exists=self.root_exists,
            prefix_map=self.prefix_map,
            analysis_roots=self.analysis_roots,
            workflow=self.workflow,
            purpose=convergence.Purpose.REBUILD,
            intent=session.Intent.RECOVERY,
        )


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

    The read-only entry point a diagnostic calls. It derives through the source
    the REGISTRY records, never one a caller names.
    """
    tree = _Tree(cfg, db, tree_id, registry, declared, tuple(rows), root_exists, prefix_map)
    placements, gaps = declared_membership(
        cfg,
        declared,
        tree_id=tree_id,
        source=registry.derivation_source(tree_id),
        vocal_threshold=vocal_threshold,
        truth=truth,
    )
    return tree.compare(*tree.favorites(placements, gaps))


def additions(report: ConvergenceReport) -> list[dict[str, str]]:
    """What a rebuild over this report adds, one row per track and destination (U219).

    The check's missing direction: the writer skips what a playlist holds and
    what reaches no row, so it adds exactly these. Sorted and plain, so a gate's
    digest is stable and a payload through JSON compares equal.
    """
    rows = [
        {
            "tree": report.tree_id,
            "folder": entry.folder,
            "playlist": entry.playlist,
            "path": entry.location or entry.content_id or "",
        }
        for entry in report.missing
    ]
    return sorted(rows, key=lambda row: (row["tree"], row["folder"], row["playlist"], row["path"]))


@contextmanager
def _opened(cfg: config.Config) -> Iterator[tuple[Any, ...]]:
    """The registry, declaration, open handle, rows and root test one library read takes."""
    entries = tree_registry.read(cfg)
    declared = active_taxonomy.load(cfg)
    handle = rb_writer.open_db(cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        yield entries, declared, handle, rows, lambda root_id: root_id in known
    finally:
        rb_writer.close_db(handle)


def preview_governed_trees(
    cfg: config.Config,
    *,
    tree_ids: Sequence[str],
    vocal_threshold: float | None,
) -> tuple[tuple[ConvergenceReport, ...], str]:
    """What a rebuild of each tree would find, read only, and the file it read (U219).

    The gate's half of :func:`rebuild_governed_tree`: the same opener and the
    same check the rebuild runs before its write, with nothing written, so a
    resort shows every add before anything is queued. The database path pins
    the gate's answer to the file it was taken over (U161).
    """
    with _opened(cfg) as (entries, declared, handle, rows, root_exists):
        opened = str(rb_writer.handle_path(handle) or rb_writer.live_db_path(cfg))
        reports = tuple(
            report_convergence(
                cfg,
                handle,
                tree_id=tree_id,
                registry=entries,
                declared=declared,
                rows=rows,
                root_exists=root_exists,
                vocal_threshold=vocal_threshold,
            )
            for tree_id in tree_ids
        )
    return reports, opened


def _plan_key(rows: Iterable[Mapping[str, Any]]) -> list[tuple[str, str, str, str]]:
    return sorted(
        (str(row.get("tree")), str(row.get("folder")), str(row.get("playlist")), str(row.get("path")))
        for row in rows
    )


def assert_as_approved(before: ConvergenceReport, approved: Sequence[Mapping[str, Any]]) -> None:
    """Refuse a write that would add anything other than what a person approved (U219).

    The plan is consumed, not remade (R-691), so a library that moved between
    the gate and the worker writes nothing. Checked on the before check.
    """
    planned = _plan_key(additions(before))
    wanted = _plan_key(approved)
    if planned == wanted:
        return
    raise refuse(
        "resort-plan-stale",
        f"the tree {before.tree_id!r} would now take {len(planned)} add(s) and the "
        f"plan that was approved named {len(wanted)}, or named different ones, so "
        f"the library or its taxonomy moved after the gate; nothing was written",
        remedy=Remedy.REPLAN_THEN_DECIDE,
        steps=("run the resort again, read the new plan, and answer its gate",),
        scope=Scope.RUN,
        origin=("tree_rebuild",),
        detail={"tree_id": before.tree_id, "approved": len(wanted), "planned": len(planned)},
    )


def _write_derived(
    tree: _Tree,
    root_id: str,
    derived: Sequence[DeclaredPlacement],
    record: convergence.TreeConvergence | None,
    placed: int,
) -> tuple[tuple[Destination, ...], trees.MembershipReport]:
    """Plan the derived placements on the tree as it stands and write them."""
    standing = read_tree(tree.db, root_id)
    destinations, plan = plan_destinations(
        tree.declared, derived, standing, record, tree_id=tree.tree_id
    )
    if not plan:
        # Unreachable while ``declared_membership`` refuses an empty derivation,
        # and refused anyway: an empty plan would skip every write gate on the
        # path that then clears the flag.
        raise refuse(
            "rebuild-derivation-empty",
            f"the rebuild for {tree.tree_id!r} produced no plan, so no gate would be "
            f"taken and nothing would be written, and the run would still be in "
            f"a position to clear this tree's unconverged flag",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"tree_id": tree.tree_id, "derived": placed},
        )
    return destinations, tree.write(plan)


def _favorites_to_file(
    derived: Sequence[DeclaredPlacement],
    placements: Sequence[DeclaredPlacement],
    before: ConvergenceReport,
    approved: Sequence[Mapping[str, Any]] | None,
) -> tuple[DeclaredPlacement, ...]:
    """The second pass's placements: the Favorites over the tree the first write left (U119)."""
    # One set, built once (U246), not per placement.
    first_pass = set(derived)
    favorites = tuple(entry for entry in placements if entry not in first_pass)
    if approved is not None:
        # A RESORT WRITES ONLY WHAT ITS GATE SHOWED (U219). A favourite derived
        # only now, from the tree this run left, is left for the next resort.
        shown = {(entry.location, entry.bucket, entry.sub) for entry in before.missing}
        favorites = tuple(
            entry for entry in favorites if (entry.location, entry.bucket, entry.sub) in shown
        )
    return favorites


def _file_favorites(
    tree: _Tree,
    root_id: str,
    favorites: Sequence[DeclaredPlacement],
    membership: trees.MembershipReport,
    destinations: tuple[Destination, ...],
) -> tuple[trees.MembershipReport, tuple[Destination, ...]]:
    """Write the second pass in a session of its own; its destinations join the record."""
    if favorites:
        standing_now = read_tree(tree.db, root_id)
        record_now = convergence.read(tree.cfg).tree(tree.tree_id)
        more, second_plan = plan_destinations(
            tree.declared, favorites, standing_now, record_now, tree_id=tree.tree_id
        )
        more, second_plan = _under_recorded_folders(more, second_plan, record_now, standing_now)
        second = tree.write(second_plan)
        membership = replace(
            membership,
            added=membership.added + second.added,
            already_present=membership.already_present + second.already_present,
            skipped=(*membership.skipped, *second.skipped),
            playlists=(*membership.playlists, *second.playlists),
        )
        known = {(entry.bucket, entry.sub) for entry in destinations}
        destinations = (
            *destinations,
            *(entry for entry in more if (entry.bucket, entry.sub) not in known),
        )
    return membership, destinations


def _record_landed(
    tree: _Tree,
    root_id: str,
    destinations: Sequence[Destination],
    record: convergence.TreeConvergence | None,
) -> None:
    """Record the node each destination landed in, after the commit and never before.

    From the destination's own resolved node first, and from the freshly read
    tree only where it had none, exactly one candidate or nothing. A recorded
    destination the taxonomy no longer declares is carried forward (a template
    edit is reversible, and the identifier is what stops a rename doubling the
    tree); a declared one that resolved to no node is dropped as dangling, as
    is an undeclared one whose node a declared destination now holds.
    """
    by_display = by_display_pair(read_tree(tree.db, root_id))
    recorded: list[convergence.DestinationNode] = []
    for entry in destinations:
        node = entry.node
        if node is None:
            node = only_one(by_display.get((entry.folder, entry.playlist), ()))
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
    taken = {(entry.bucket, entry.sub) for entry in recorded}
    claimed = {(entry.folder_id, entry.playlist_id) for entry in recorded}
    recorded += [
        entry
        for entry in (() if record is None else record.nodes)
        if (entry.bucket, entry.sub) not in taken
        and _declared_display(tree.declared, entry.bucket, entry.sub, derived=False) is None
        and (entry.folder_id, entry.playlist_id) not in claimed
    ]

    if recorded:
        # Validated as a bijection before it is persisted, then REPLACED, not
        # merged: this run resolved the union of derived and recorded
        # destinations, so a missing entry is one whose node no longer exists.
        convergence.assert_injective(tree.tree_id, recorded)
        convergence.record_nodes(tree.cfg, tree.tree_id, recorded, replace_all=True)


def _clear_on_evidence(
    cfg: config.Config, tree_id: str, after: ConvergenceReport, now: datetime | None
) -> tuple[bool, bool | None]:
    """Clear the flag and close the restore marker when the after check converged."""
    if not after.converged:
        logger.warning(
            "the tree %s still differs from what this library declares in %d "
            "place(s) after a rebuild, so it stays unconverged",
            tree_id,
            len(after.summaries()),
        )
        return False, None
    # The check's own (empty) list, so the clearing call is handed evidence and
    # never an emptiness asserted on the check's behalf.
    convergence.clear_unconverged(cfg, tree_id, differences=after.summaries(), now=now)
    return True, close_restore_marker(cfg, tree_id)


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
    approved: Sequence[Mapping[str, Any]] | None = None,
) -> RebuildReport:
    """Write back everything the declaration places in this tree and the database lacks.

    THE ORDER IS THE UNIT: refuse an unrebuildable tree, derive, check, write,
    record where it landed, check again, and only then clear the flag. The
    node record comes after the commit (a recorded identifier for an
    uncommitted row is a dangling pointer); the flag is cleared last and only
    on the second check's evidence.

    ``approved`` is a resort's frozen plan (U219): the before check must add
    exactly those rows or nothing is written (:func:`assert_as_approved`).
    The placements are derived here from the source the registry records and
    are never a parameter; ``truth`` supplies tag READINGS only. ``rows`` is
    materialized once, since a cursor reads empty to its second walker.

    The session is the membership writer's to open. It is handed
    ``Purpose.REBUILD`` (sheds this tree's convergence flag and the out-of-band
    restore refusal; the detection still runs) and ``Intent.RECOVERY`` (sheds
    the unresolved-session and restore-reconciliation latches whole). The
    surplus is put back before anything is written, by
    ``session.assert_no_unresolved_session`` and :func:`assert_no_latched_restore`.
    """
    source = registry.derivation_source(tree_id)
    tree_registry.assert_rebuildable(tree_id, source)
    session.assert_no_unresolved_session(cfg)
    assert_no_latched_restore(cfg)
    tree = _Tree(
        cfg, db, tree_id, registry, declared, tuple(rows), root_exists, prefix_map,
        analysis_roots, workflow,
    )
    root_id = tree_registry.anchored_root(tree_id, registry, root_exists=root_exists)
    derived, not_compared = declared_membership(
        cfg,
        declared,
        tree_id=tree_id,
        source=source,
        vocal_threshold=vocal_threshold,
        truth=truth,
    )
    # THE GENRE FAVORITES ARE READ OFF THE TREE AS IT STANDS for the before
    # check, and again off the tree the first write leaves for the second write
    # and the after check (U119): a favourite whose tag moved it is in its new
    # folder only once the first write has moved it.
    placements, not_compared = tree.favorites(derived, not_compared)
    before = tree.compare(placements, not_compared)

    if approved is not None:
        assert_as_approved(before, approved)

    record = convergence.read(cfg).tree(tree_id)
    destinations, membership = _write_derived(tree, root_id, derived, record, len(placements))
    placements, not_compared = tree.favorites(derived, not_compared)
    favorites = _favorites_to_file(derived, placements, before, approved)
    membership, destinations = _file_favorites(tree, root_id, favorites, membership, destinations)
    _record_landed(tree, root_id, destinations, record)
    after = tree.compare(placements, not_compared)
    cleared, marker_closed = _clear_on_evidence(cfg, tree_id, after, now)
    return RebuildReport(
        tree_id=tree_id,
        root_id=root_id,
        before=before,
        after=after,
        membership=membership,
        cleared=cleared,
        restore_marker_closed=marker_closed,
    )


def rebuild_governed_tree(
    cfg: config.Config,
    *,
    tree_id: str,
    workflow: str = REBUILD_WORKFLOW,
    vocal_threshold: float | None,
    approved: Sequence[Mapping[str, Any]] | None = None,
) -> RebuildReport:
    """Open this library's database, rebuild one governed tree, and close it again.

    The composition only, here because the ``rebuild`` and ``route.resort``
    workers cannot import each other. One tree per call, so a refusal on the
    second tree leaves the first one's item done.

    No configuration is loaded: the job's frozen one is passed in (KTD9).
    ``vocal_threshold`` is required (D7, R-276), never defaulted. The rows come from
    :func:`cratekit.write.routing_pass.content_rows`, which refuses a row that
    cannot report its soft-delete marker.
    """
    with _opened(cfg) as (entries, declared, handle, rows, root_exists):
        return rebuild_tree(
            cfg,
            handle,
            tree_id=tree_id,
            registry=entries,
            declared=declared,
            rows=rows,
            root_exists=root_exists,
            # THE LIBRARY ROOT, never the music directory: the watch walks for
            # ANLZ files by name, which rekordbox keeps under its own directory,
            # and a watch over an empty set reports a clean session whatever
            # happened to the grids (R17), with the share beside it (R-14).
            analysis_roots=analysis_store.watch_roots(cfg),
            vocal_threshold=vocal_threshold,
            workflow=workflow,
            approved=approved,
        )


def favorites_skipped_warnings(
    declared: taxonomy.Taxonomy, tree_ids: Iterable[str]
) -> tuple[dict[str, str], ...]:
    """The note a rebuild that drove the routing tree carries when no genre Favorites class is declared (U132).

    :func:`with_favorites` passes over an undeclared class silently. Only when
    the routing tree is among ``tree_ids``, the trees the job drove this run.
    """
    if declared.tree.id not in {str(tree_id) for tree_id in tree_ids}:
        return ()
    return genre_favorites.undeclared_warnings(declared)


def governed_not_compared(
    vocal_threshold: float | None, declared: taxonomy.Taxonomy
) -> tuple[str, ...]:
    """What :func:`rebuild_governed_tree` leaves uncompared, asked without a library.

    The same two inputs it derives with, the active taxonomy (R-685) and the
    threshold read as the worker reads it (U89). A resume asks this because the
    worker's report does not outlive its item.
    """
    return not_derived(declared, vocal_threshold=vocal_threshold)


__all__ = [
    "DERIVATIONS",
    "accept_as_it_stands",
    "additions",
    "detect_restore",
    "assert_as_approved",
    "assert_derivable",
    "preview_governed_trees",
    "derivable",
    "other_declared_trees",
    "LEFT_BEHIND",
    "LEFT_BEHIND_NAMED",
    "REBUILD_ACTOR",
    "REBUILD_ANSWERS_KIND",
    "REBUILD_WORKFLOW",
    "VOCAL_DIMENSION",
    "VOCAL_NOT_COMPARED",
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
    "favorites_skipped_warnings",
    "governed_not_compared",
    "left_behind",
    "left_behind_message",
    "left_behind_record",
    "left_behind_warnings",
    "library_truth",
    "not_compared_warnings",
    "not_derived",
    "plan_destinations",
    "read_tree",
    "read_truth",
    "rebuild_governed_tree",
    "rebuild_tree",
    "report_convergence",
    "resolve_destinations",
    "undeclared_destinations",
    "with_favorites",
]
