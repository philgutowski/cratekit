"""The export path of ``route inbox`` and ``route unplaced`` (U86, U91).

A tree that has not cut over is routed into a new file beside a fresh
collection export, never into the database. The verb handlers stay in
:mod:`cratekit.write.routing_cli`, which imports this module and holds the
apply gate; the route here asks that gate through the module at call time.

ONE READ PER VERB (R-685): a verb passes the declaration it checked the
bridge with, so its plan, write and pending action share one declaration; a
caller that passes none has it read here.

Layer: write.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple

from cratekit.cli.output import Envelope, PendingHumanAction, digest_of, new_pending_id
from cratekit.core import (
    active_taxonomy,
    config,
    locations,
    rb_writer,
    routing,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import metadata_cli, rbxml, rebuild, routing_pass, trees

#: The warning an export sweep gives for the star ratings it did not plan
#: (R-688): an import keeps the database's rating on every row an export holds.
RATING_NOT_LANDABLE = "rating-not-landable"


def _rating_not_landable(owed: int) -> list[dict[str, str]]:
    """The owed rating warning, as a list so a count of zero adds nothing."""
    if not owed:
        return []
    return [{
        "code": RATING_NOT_LANDABLE,
        "message": f"{owed} intake row(s) are owed a star rating from energy and "
        f"none was planned: every row of a collection export is one rekordbox "
        f"already holds, an import keeps the database's rating on such a row, "
        f"and this build writes no rating to the database",
    }]


def _plan(items: list[dict[str, str]], *, kind: str, **totals: Any) -> dict:
    """The plan envelope, with the digest taken over the ITEMS alone.

    The extra totals carry what this run did, not what it offered, so they stay
    outside the digest; ``plan/1`` forbids properties it does not name.
    """
    digest = digest_of({"kind": kind, "items": items})
    return {
        "digest": digest,
        "items": items,
        "totals": {"count": len(items), **totals},
        "chunk": None,
    }


def _native_trees(entries: tree_registry.Registry) -> tuple[str, ...]:
    """Every tree that has cut over, in a stable order. The items of a resort."""
    return tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))


def _column(
    declared: taxonomy.Taxonomy,
    placement: rebuild.DeclaredPlacement,
    *,
    destined: dict[str, str],
    vocal: dict[str, str],
    genre: dict[str, str],
) -> dict[str, str]:
    """Which column of a gate's item one placement is shown in (U155).

    Each of the energy, vocal and genre subs has a column of its own, so a gate
    never shows one place for a track written into two. One answer for both media.
    """
    if placement.sub == trees.VOX_SUB_CLASS:
        return vocal
    if routing.genre_sub_named(declared, placement.bucket, placement.sub):
        return genre
    return destined


def _placed_counts(tracks: list[dict[str, str]]) -> dict[str, int]:
    """How many track items file somewhere, under a vocal sub and under a genre sub."""
    return {
        "routed": sum(1 for item in tracks if item["destination"]),
        "vocal": sum(1 for item in tracks if item["vocal"]),
        "genre sub": sum(1 for item in tracks if item.get("genre")),
    }


def _named(plan: dict, names: dict[str, dict[str, str]]) -> dict:
    """The plan as the export gate shows it, each track named (R-692).

    Each shown item leads with the row's artist and title, which stay outside
    the digest, then every field the digest was taken over.
    """
    return {
        **plan,
        "items": [
            {**names.get(item["track_id"], {"artist": "", "title": ""}), **item}
            for item in plan["items"]
        ],
    }


def _export_facts(
    items: list[dict[str, str]],
    export: Path,
    gaps: tuple[str, ...],
    vox_created: tuple[str, ...],
    warnings: list[dict[str, str]],
) -> dict[str, Any]:
    """The export gate's totals, counted off the items it lists.

    Counted from the items, so a total cannot disagree with the list under it.
    ``not derived`` and the warnings ride so an empty column and a track with no
    destination have their reason before the question.
    """
    tracks = [item for item in items if item["track_id"]]
    return {
        "export": str(export),
        "tracks": len(tracks),
        **_placed_counts(tracks),
        "long tracks": sum(1 for item in tracks if item["long_track"]),
        "vocal subs created": list(vox_created),
        "not derived": list(gaps),
        "warnings": [warning["message"] for warning in warnings],
    }


#: The suffix of the file an export routing writes, beside the export it read.
ROUTED_SUFFIX = "_routed.xml"

#: The warning a library with nothing native carries on the database path,
#: naming what the export medium delivers and no more (R-695, R-687).
EXPORT_REMEDY = (
    "no tree has cut over, so nothing files this library into the routing tree. "
    "Export the collection from rekordbox and run route inbox --export with that "
    "file. It writes a review of the routing, and you file its tracks by hand, "
    "since no import can land a nested playlist"
)


def export_remedy(declared: taxonomy.Taxonomy) -> str:
    """:data:`EXPORT_REMEDY`, naming the long track playlist when one is declared.

    That playlist is the one root playlist the inbox sweep writes and so the one
    thing an import lands (R-694).
    """
    if declared.long_tracks is None:
        return EXPORT_REMEDY
    return (
        f"{EXPORT_REMEDY}. It also adds long tracks to the root playlist "
        f"{declared.long_tracks.display!r}, which one import can land"
    )


#: Why an export routing's file cannot deliver the routing tree, shared by both
#: sweeps' review warning (R-687).
NESTED_UNLANDABLE = (
    "a nested playlist imported from the file lands at the playlist root as a "
    "new playlist, and a folder imported from it keeps every playlist it held "
    "and adds a second copy of each"
)
#: The same reason, as a step of the inbox sweep's pending import.
ROUTING_TREE_UNIMPORTABLE = (
    "leave the routing tree's folders and playlists unimported: " + NESTED_UNLANDABLE
)

#: The warning an export sweep gives for the nested membership it wrote into
#: a file no import can land it from (R-694), in place of a pending import
#: whose own check could never answer.
ROUTING_NOT_LANDABLE = "routing-not-landable"


def _routing_not_landable(
    destination: Path, inserted: int, created: int, remedy: str
) -> list[dict[str, str]]:
    """The review warning, as a list so a file with no nested change adds nothing.

    ``inserted`` and ``created`` are both nested under the routing tree, so
    neither lands through the file; ``remedy`` is the step a person takes instead.
    """
    if not inserted and not created:
        return []
    made = f" and {created} sub-playlist(s) created" if created else ""
    return [{
        "code": ROUTING_NOT_LANDABLE,
        "message": f"{inserted} membership(s) routed{made} under the routing tree "
        f"in {destination.name} are a review that no import can land: "
        f"{NESTED_UNLANDABLE}; {remedy}",
    }]


def _export_refusal(reason: str, message: str, export: Path, **extra: Any) -> CratekitError:
    return refuse(
        reason,
        message,
        steps=("export the collection again from rekordbox and pass that file",),
        origin=("routing_cli",),
        detail={"export": str(export), **extra},
    )


def _read_export(export: Path) -> bytes:
    """The bytes of a collection export, or a refusal naming why they are not one."""
    if not export.is_file():
        raise _export_refusal(
            "library-export-unusable", f"no collection export at {export}", export
        )
    content = export.read_bytes()
    if rbxml.playlists_start(content) == -1:
        raise _export_refusal(
            "library-export-unusable",
            f"{export.name} has no {rbxml.PLAYLISTS_SECTION} section, so it is not "
            f"a collection export",
            export,
        )
    return content


def _inbox_keys(content: bytes, declared: taxonomy.Taxonomy, export: Path) -> list[str]:
    """Every track key the export's intake folder holds, first seen first.

    A direct child of the playlist root, never a deeper namesake. An export with
    no such folder REFUSES, since an empty answer reads as an empty inbox.
    """
    root = rbxml.root_node(content)
    if root is None:
        raise _export_refusal(
            "library-export-unusable",
            f"{export.name} has no playlist tree, so it is not a collection export",
            export,
        )
    display = declared.intake.display
    node = rbxml.direct_child(content, root, display, rbxml.FOLDER_TYPE)
    if not isinstance(node, rbxml.NodeSpan):
        why = node if isinstance(node, str) else f"no folder named {display!r} sits under ROOT"
        raise refuse(
            "intake-flow-absent",
            f"{export.name} carries no intake folder to route: {why}",
            origin=("routing_cli",),
            detail={"export": str(export), "intake": display},
        )
    return list(dict.fromkeys(
        key
        for _path, child in rbxml.walk_nodes(content, node)
        if child.node_type == rbxml.PLAYLIST_TYPE
        for key in rbxml.track_keys(content, child)
    ))


def _collection_rows(content: bytes) -> dict[str, dict[str, str]]:
    """Every collection row's attributes, by track id."""
    return {
        track.track_id: rbxml.attributes(content, track)
        for track in rbxml.collection_tracks(content)
    }


def _readable_file(location: str, cfg: config.Config) -> Path | None:
    """The file a recorded Location names on this machine, or None.

    Through the prefix map first, then as written. None when neither is a file,
    rather than route absent tags to the fallback bucket.
    """
    try:
        decoded = locations.location_to_path(location)
    except locations.LocationDecodeError:
        return None
    resolved = locations.resolve_recorded_path(
        decoded, root=cfg.library.root, prefix_map=trees.prefix_rules(cfg)
    )
    for candidate in (resolved.path, decoded):
        if candidate and candidate.startswith("/") and Path(candidate).is_file():
            return Path(candidate)
    return None


def _unrated(row: dict[str, str]) -> bool:
    """Whether an export row's star rating is still the one nobody set.

    Empty and ``"0"`` are rekordbox's unrated values; any other value is
    somebody's. A row with no ``Rating`` attribute says nothing and is not counted.
    """
    value = row.get("Rating")
    return value is not None and value.strip() in ("", "0")


def _owed_ratings(
    declared: taxonomy.Taxonomy,
    placements: tuple[rebuild.DeclaredPlacement, ...],
    readings: list[rebuild.Truth],
    files: dict[str, list[str]],
    by_id: dict[str, dict[str, str]],
) -> int:
    """How many unrated intake rows are owed a star rating from their energy.

    Through :func:`cratekit.core.routing.energy_rating` and ``rates``. OWED, NOT
    PLANNED (R-688): an import keeps the database's rating on every row an
    export carries, so none is written. Counted in ROWS, only for a placed
    track, and once per file however many places it files into (U155).
    """
    energy = {reading.location: reading.energy for reading in readings}
    owed = 0
    counted: set[str] = set()
    for placement in placements:
        if placement.location in counted:
            continue
        if not routing.rates(declared, placement.bucket):
            continue
        if routing.energy_rating(declared, energy.get(placement.location)) is None:
            continue
        counted.add(placement.location)
        owed += sum(1 for key in files[placement.location] if _unrated(by_id[key]))
    return owed


#: A ``TotalTime`` this pass will read as a length: digits and nothing else.
_SECONDS = re.compile(r"[0-9]+")


def _duration(row: dict[str, str]) -> int | None:
    """A collection row's length in whole seconds, or None when it has none.

    ``TotalTime`` is seconds. An absent, non numeric or zero value is None: zero
    is what the emitter writes for a length it never measured.
    """
    value = row.get("TotalTime")
    if value is None or not _SECONDS.fullmatch(value.strip()):
        return None
    seconds = int(value.strip())
    return seconds if seconds > 0 else None


@dataclass(frozen=True)
class LongPlan:
    """What the pass adds to the long track playlist, and what it could not read.

    ``keys`` excludes every track the playlist holds, so a second run plans
    nothing; ``unreadable`` counts rows with no readable length.
    """

    keys: tuple[str, ...] = ()
    unreadable: int = 0


def _long_tracks(
    declared: taxonomy.Taxonomy,
    content: bytes,
    by_id: dict[str, dict[str, str]],
    warnings: list[dict[str, str]],
) -> LongPlan:
    """Every collection track over the declared length that the playlist lacks.

    The whole collection, not the intake folder. A FOLDER of the playlist's name
    is a warning and nothing is planned, since the writer would refuse it, and the
    warning keeps the run from answering ``nothing-to-route``.
    """
    long_tracks = declared.long_tracks
    if long_tracks is None:
        return LongPlan()
    held = trees.root_playlist_members(content, long_tracks.display)
    if isinstance(held, str):
        warnings.append({
            "code": "route-write-skipped",
            "message": f"the {long_tracks.display!r} playlist was not built: {held}",
        })
        return LongPlan()
    members = set(held)
    keys: list[str] = []
    unreadable = 0
    for key, row in by_id.items():
        seconds = _duration(row)
        if seconds is None:
            unreadable += 1
        elif seconds > long_tracks.over_seconds and key not in members:
            keys.append(key)
    return LongPlan(tuple(keys), unreadable)


def _vox_subs(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    content: bytes,
    threshold: float | None,
    warnings: list[dict[str, str]],
) -> tuple[bytes, tuple[str, ...]]:
    """Give every genre folder its vocal sub-playlist, before anything is routed.

    Returns the bytes with the subs in place and each ``folder/sub`` created. The
    routing writer creates no sub, so this runs first, only on a calibrated
    library that declares the vocal sub. Idempotent. An unreachable tree is a
    warning, since the routing writer reports the same tree.
    """
    if threshold is None or not any(
        entry.additive and entry.id == trees.VOX_SUB_CLASS for entry in declared.sub_classes
    ):
        return content, ()
    tree = rbxml.routing_tree(declared, tree_registry.read(cfg))
    try:
        written, report = trees.add_vox_playlists(content, declared, tree=tree)
    except (trees.TreeUnreachable, trees.DuplicateFolders) as exc:
        warnings.append({
            "code": "route-write-skipped",
            "message": f"no vocal sub-playlist was created: {exc}",
        })
        return content, ()
    warnings.extend(
        {"code": "route-write-skipped", "message": text} for text in report.warnings
    )
    sub = declared.sub_class(trees.VOX_SUB_CLASS).display
    return written, tuple(f"{folder}/{sub}" for folder in report.modified)


@dataclass(frozen=True)
class Decision:
    """Where the routing decision puts a set of export tracks, and what it read.

    ``plan`` is what a bridge writer takes, keyed on ``(folder, sub)``;
    ``destined``, ``vocal`` and ``genre`` are each track's subs as shown;
    ``files`` maps each readable file to its keys; ``readings`` and ``placements``
    are kept for counting owed ratings from the same reading.
    """

    plan: dict[tuple[str, str], list[str]]
    destined: dict[str, str]
    vocal: dict[str, str]
    files: dict[str, list[str]]
    readings: list[rebuild.Truth]
    placements: tuple[rebuild.DeclaredPlacement, ...]
    gaps: tuple[str, ...]
    genre: dict[str, str]


def _decide(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    rows: list[tuple[str, dict[str, str]]],
    threshold: float | None,
    warnings: list[dict[str, str]],
) -> Decision:
    """Route export rows by the native path's decision, called rather than restated.

    One decision for both export sweeps and the database medium (U91). A row
    whose Location names no file here is a warning and is not routed.
    """
    files: dict[str, list[str]] = {}
    for key, row in rows:
        path = _readable_file(row.get("Location", ""), cfg)
        if path is None:
            warnings.append({
                "code": "track-file-unreadable",
                "message": f"track {key} names {row.get('Location', '')!r}, which is not "
                f"a file on this machine, so its tags could not be read and it was "
                f"not routed",
            })
            continue
        files.setdefault(str(path), []).append(key)

    readings = [rebuild.read_truth(Path(path)) for path in files]
    placements, gaps = rebuild.derive_from_taxonomy(
        declared, readings, vocal_threshold=threshold
    )
    plan: dict[tuple[str, str], list[str]] = {}
    destined: dict[str, str] = {}
    vocal: dict[str, str] = {}
    genre: dict[str, str] = {}
    for placement in placements:
        folder, sub = routing_pass.destination(declared, placement.bucket, placement.sub)
        named = _column(declared, placement, destined=destined, vocal=vocal, genre=genre)
        for key in files[placement.location]:
            plan.setdefault((folder, sub), []).append(key)
            named[key] = f"{folder}/{sub}"
    return Decision(plan, destined, vocal, files, readings, placements, gaps, genre)


class ExportPlan(NamedTuple):
    """What :func:`plan_export` decided, by name and still unpackable in order.

    ``content`` already holds any vocal sub-playlist added; ``owed`` counts rows
    owed a rating; ``items`` are what the digest covers; ``names`` are each track's
    artist and title, for :func:`_named` alone (R-692).
    """

    content: bytes
    plan: dict[tuple[str, str], list[str]]
    owed: int
    long_plan: LongPlan
    items: list[dict[str, str]]
    warnings: list[dict[str, str]]
    gaps: tuple[str, ...]
    vox_created: tuple[str, ...]
    names: dict[str, dict[str, str]]


def plan_export(
    cfg: config.Config, export: Path, *, declared: taxonomy.Taxonomy | None = None
) -> ExportPlan:
    """Read one fresh export and decide where each intake track goes.

    No star rating is planned (R-688), only counted: see :func:`_owed_ratings`.
    The decision is :func:`_decide`'s, the same calls :func:`plan_inbox` makes, and
    the genre is the FILE's. The calibrated cut is the one loader's (U89); with
    none the vocal dimension is named in ``gaps``.
    """
    content = _read_export(export)
    if declared is None:
        declared = active_taxonomy.load(cfg)
    keys = _inbox_keys(content, declared, export)
    by_id = _collection_rows(content)
    warnings: list[dict[str, str]] = []
    threshold = metadata_cli.load_vocal_threshold(cfg)
    content, vox_created = _vox_subs(cfg, declared, content, threshold, warnings)
    rows: list[tuple[str, dict[str, str]]] = []
    for key in keys:
        row = by_id.get(key)
        if row is None:
            warnings.append({
                "code": "track-row-absent",
                "message": f"track {key} is in the intake folder and has no collection "
                f"row in {export.name}, so it was not routed",
            })
            continue
        rows.append((key, row))
    decision = _decide(cfg, declared, rows, threshold, warnings)
    destined, vocal = decision.destined, decision.vocal
    owed = _owed_ratings(
        declared, decision.placements, decision.readings, decision.files, by_id
    )
    long_plan = _long_tracks(declared, content, by_id, warnings)
    lengthy = set(long_plan.keys)
    playlist = declared.long_tracks.display if declared.long_tracks else ""
    # The long track playlist rides the item, inside the digest a person
    # approves. A long track outside the intake gets an item of its own, and so
    # does each vocal sub-playlist created, with no track.
    items = [
        {
            "track_id": key,
            "destination": destined.get(key, ""),
            "vocal": vocal.get(key, ""),
            "genre": decision.genre.get(key, ""),
            "long_track": playlist if key in lengthy else "",
        }
        for key in keys
    ]
    intake = set(keys)
    items += [
        {"track_id": key, "destination": "", "vocal": "", "genre": "", "long_track": playlist}
        for key in long_plan.keys
        if key not in intake
    ]
    items += [
        {"track_id": "", "destination": created, "vocal": "", "genre": "", "long_track": ""}
        for created in vox_created
    ]
    names = {
        key: {"artist": by_id[key].get("Artist", ""), "title": by_id[key].get("Name", "")}
        for key in (item["track_id"] for item in items)
        if key in by_id
    }
    return ExportPlan(
        content, decision.plan, owed, long_plan, items, warnings, decision.gaps,
        vox_created, names,
    )


def apply_export(
    cfg: config.Config,
    export: Path,
    content: bytes,
    plan: dict[tuple[str, str], list[str]],
    long_plan: LongPlan = LongPlan(),
    vox_created: tuple[str, ...] = (),
    *,
    declared: taxonomy.Taxonomy | None = None,
) -> tuple[Path | None, trees.RouteReport, int, str | None]:
    """Write the plan into a copy of the export, beside it, never in place.

    Returns the file written or None, the membership report, how many tracks the
    long track playlist gained, and its writer's warning. The governed tree, so
    the emitter guard refuses one that has cut over; the non creating writer,
    since a person curated this tree. No rating is written (R-688). Nothing
    changed is nothing written. The long track playlist is written last, add only.
    """
    if declared is None:
        declared = active_taxonomy.load(cfg)
    tree = rbxml.routing_tree(declared, tree_registry.read(cfg))
    buffer = bytearray(content)
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
    lengthened, long_warning = 0, None
    if long_plan.keys and declared.long_tracks is not None:
        lengthened, long_warning = trees.add_to_root_playlist(
            declared.long_tracks.display, long_plan.keys, buffer
        )
    if not report.inserted and not lengthened and not vox_created:
        return None, report, lengthened, long_warning
    destination = export.with_name(export.stem + ROUTED_SUFFIX)
    config.atomic_write_bytes(bytes(buffer), destination)
    return destination, report, lengthened, long_warning


def _export_pending(
    run_id: str, verb: str, destination: Path, lengthened: int, playlist: str
) -> PendingHumanAction:
    """The import an inbox sweep owes: the root playlist it added to, alone.

    Only a root playlist lands through the file (R-687), so the caller asks this
    only when the long track playlist gained tracks (R-694).
    """
    return PendingHumanAction(
        kind="rekordbox_import",
        id=new_pending_id(run_id),
        # NO RATING IS CLAIMED (R-688): this file carries none.
        summary=(
            f"{lengthened} long track(s) were added to the root playlist "
            f"{playlist!r} in {destination.name}, which rekordbox has not imported yet"
        ),
        # THIS VERB IS ITS OWN CHECK (R-694): after the import a second run
        # adds none and owes none. Named by the caller, since this layer may
        # not spell a verb (KTD23).
        verify_verb=verb,
        artifact=str(destination),
        steps=(
            f"import {destination} into rekordbox as a rekordbox xml library and "
            f"import from it the {playlist!r} playlist alone, and nothing else",
            ROUTING_TREE_UNIMPORTABLE,
            "then export the collection again and run route inbox --export with "
            "that file, which owes no import once the playlist's import has "
            "landed, and whose routing is a review, since the bridge cannot "
            "land it",
        ),
    )


def _route_reason(destination: Path | None, warnings: list[dict[str, str]]) -> str | None:
    """Why an export sweep wrote no file, or None when it wrote one.

    ``nothing-to-route`` says the library is filed, so a run that skipped a
    write or could not read a track answers ``route-blocked`` instead.
    """
    if destination is not None:
        return None
    if warnings:
        return "route-blocked"
    return "nothing-to-route"


def _refuse_off_the_bridge(
    cfg: config.Config, declared: taxonomy.Taxonomy, export: Path, *, instead: str
) -> None:
    """Refuse an export sweep the bridge cannot serve, before anything is read.

    A tree that has cut over is the database's, and an absent library root would
    leave every track unreadable. ``instead`` is the step a person takes.
    """
    if tree_registry.read(cfg).is_database_native(declared.tree.id):
        raise refuse(
            "tree-unconverged",
            f"the tree {declared.tree.id!r} has cut over to the database, so an "
            f"export must not carry its membership; importing one would replace "
            f"the tree the database owns",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=(instead,),
            origin=("routing_cli",),
            detail={"tree_id": declared.tree.id, "export": str(export)},
        )
    if not Path(cfg.library.root).is_dir():
        raise refuse(
            "library-volume-unmounted",
            f"this library's root {cfg.library.root!r} is not there, so no track "
            f"the export names can be read",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            origin=("routing_cli",),
            detail={"root": str(cfg.library.root), "export": str(export)},
        )


def route_inbox_export(ctx, cfg: config.Config, export: Path) -> Envelope:
    """Route a fresh export's intake folder into a new file, behind the apply gate.

    The bridge and the volume are checked before the plan is offered, so a person
    is never asked to approve a write the guard would stop.
    """
    declared = active_taxonomy.load(cfg)
    _refuse_off_the_bridge(
        cfg, declared, export, instead="run route inbox without --export, which "
        "writes the database",
    )
    content, plan, owed, long_plan, items, warnings, gaps, vox_created, names = (
        plan_export(cfg, export, declared=declared)
    )
    unrated = _rating_not_landable(owed)
    offered = _plan(items, kind="inbox-export")
    facts = _export_facts(items, export, gaps, vox_created, [*warnings, *unrated])
    from cratekit.write import routing_cli  # the gate tests patch there

    option = routing_cli._apply_gate(ctx, _named(offered, names), facts)
    if option != "apply":
        return ctx.envelope(
            data=_plan(items, kind="inbox-export", applied=False),
            outcome=Outcome.NO_OP,
            warnings=[*warnings, *unrated],
        )
    destination, report, lengthened, long_warning = apply_export(
        cfg, export, content, plan, long_plan, vox_created, declared=declared
    )
    # ONE CODE FOR EVERY SKIPPED WRITE: the writer's sentence already names
    # whether a tree, a genre folder or a sub was missing.
    warnings = [
        *warnings,
        *({"code": "route-write-skipped", "message": text} for text in report.warnings),
        *(
            [{"code": "route-write-skipped", "message": long_warning}]
            if long_warning
            else []
        ),
    ]
    # The owed ratings join the warnings only after the answer, since no run of
    # this medium can land one (R-688).
    reason = _route_reason(destination, warnings)
    warnings += unrated
    data = _plan(
        items,
        kind="inbox-export",
        applied=destination is not None,
        reason=reason,
        inserted=report.inserted,
        long_added=lengthened,
        duration_unreadable=long_plan.unreadable,
        # THE PLAN'S LIST, and the writer's too: a sub created is a change, so
        # a non empty list means a file was written carrying every one.
        vox_created=list(vox_created),
        created=list(report.created),
        output=None if destination is None else str(destination),
        not_derived=list(gaps),
    )
    if destination is None:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    warnings += _routing_not_landable(
        destination,
        report.inserted,
        len(vox_created),
        "file the intake tracks into the subs this review names by hand in "
        "rekordbox; until they are filed, route inbox --export plans the same "
        "routing on every fresh export, and this build writes nested membership "
        "only to a tree that has cut over to the database",
    )
    # A PENDING IMPORT ONLY FOR WHAT AN IMPORT CAN LAND (R-694): the long track
    # playlist is the one root playlist written, so a file that added nothing
    # to it is a review, and ends ok.
    if not lengthened or declared.long_tracks is None:
        return ctx.envelope(data=data, outcome=Outcome.OK, warnings=warnings)
    return ctx.envelope(
        data=data,
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=_export_pending(
            ctx.run.run_id,
            ctx.entry.name,
            destination,
            lengthened,
            declared.long_tracks.display,
        ),
        warnings=warnings,
    )


def unplaced_items(cfg: config.Config) -> tuple[list[dict[str, str]], dict[str, Any]]:
    """Every active collection row that no governed tree holds, and the totals.

    Asked of the database (U53), and coverage is membership walked DOWN from the
    adopted root, never a folder found by name. A library with nothing native is
    not compared, and the totals say so.
    """
    entries = tree_registry.read(cfg)
    native = _native_trees(entries)
    if not native:
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        held: set[str] = set()
        for tree_id in native:
            root_id = tree_registry.anchored_root(
                tree_id, entries, root_exists=lambda root: root in known
            )
            for node in rebuild.read_tree(handle, root_id):
                held |= set(node.content_ids)
    finally:
        rb_writer.close_db(handle)
    # THE TOMBSTONED HALF IS NOT UNPLACED: a soft-deleted row was removed on
    # purpose.
    active = [row for row in rows if not row.deleted]
    items = [
        {"content_id": row.content_id, "path": row.recorded}
        for row in active
        if row.content_id not in held
    ]
    return items, {
        "compared": True,
        "reason": None,
        "collection": len(active),
        "trees": len(native),
    }


#: The suffix of the file the unplaced sweep writes, beside the export it read.
#: Not ``ROUTED_SUFFIX``, which would replace an inbox routing not yet imported.
PLACED_SUFFIX = "_placed.xml"

#: The warning the report carries when no tree has cut over, naming what the
#: export medium delivers here (R-695, R-694).
UNPLACED_EXPORT_REMEDY = (
    "no tree has cut over, so nothing places what the routing tree does not hold. "
    "Export the collection from rekordbox and run route unplaced --export with "
    "that file. It writes a review of where each unplaced track belongs, and you "
    "file those tracks by hand, since no import can land a nested playlist. It "
    "adds to no root playlist and owes no import"
)


def _routing_tree_node(
    content: bytes, declared: taxonomy.Taxonomy, export: Path
) -> rbxml.NodeSpan:
    """The export's routing tree, a folder that is a direct child of the root.

    The writer's own scope. An absent tree refuses: every track would read as
    unplaced and every write would be skipped.
    """
    display = declared.tree.display
    root = rbxml.root_node(content)
    node = (
        None
        if root is None
        else rbxml.direct_child(content, root, display, rbxml.FOLDER_TYPE)
    )
    if isinstance(node, rbxml.NodeSpan):
        return node
    why = node if isinstance(node, str) else f"no folder named {display!r} sits under ROOT"
    raise refuse(
        "governed-tree-absent",
        f"{export.name} carries no routing tree to place tracks into: {why}",
        steps=(
            "check that the export is the current one and holds the routing tree "
            "the taxonomy declares, directly under the playlist root",
        ),
        origin=("routing_cli",),
        detail={"export": str(export), "declared": display, "tree": declared.tree.id},
    )


def unplaced_keys(
    content: bytes, tree_node: rbxml.NodeSpan, by_id: dict[str, dict[str, str]]
) -> list[str]:
    """Every collection track no playlist under the routing tree holds, in order.

    A track is placed when any playlist under the tree holds it, whatever the sub.
    Only playlists are read, since a folder's range holds its children's keys.
    """
    held: set[str] = set()
    for _path, child in rbxml.walk_nodes(content, tree_node):
        if child.node_type == rbxml.PLAYLIST_TYPE:
            held.update(rbxml.track_keys(content, child))
    return [key for key in by_id if key not in held]


def plan_unplaced_export(
    cfg: config.Config, export: Path, *, declared: taxonomy.Taxonomy | None = None
) -> tuple[
    bytes,
    dict[tuple[str, str], list[str]],
    list[dict[str, str]],
    list[dict[str, str]],
    tuple[str, ...],
]:
    """Read one fresh export and decide where each unplaced track goes.

    Returns the bytes, the plan, the items shown, the warnings and the dimensions
    not derived. The decision is :func:`_decide`'s; the creating writer makes a
    missing vocal sub, so no separate vocal pass runs.
    """
    content = _read_export(export)
    if declared is None:
        declared = active_taxonomy.load(cfg)
    tree_node = _routing_tree_node(content, declared, export)
    by_id = _collection_rows(content)
    keys = unplaced_keys(content, tree_node, by_id)
    warnings: list[dict[str, str]] = []
    threshold = metadata_cli.load_vocal_threshold(cfg)
    decision = _decide(cfg, declared, [(key, by_id[key]) for key in keys], threshold, warnings)
    items = [
        {
            "track_id": key,
            "destination": decision.destined.get(key, ""),
            "vocal": decision.vocal.get(key, ""),
            "genre": decision.genre.get(key, ""),
        }
        for key in keys
    ]
    return content, decision.plan, items, warnings, decision.gaps


def apply_unplaced_export(
    cfg: config.Config,
    export: Path,
    content: bytes,
    plan: dict[tuple[str, str], list[str]],
    *,
    declared: taxonomy.Taxonomy | None = None,
) -> tuple[Path | None, trees.RouteReport]:
    """Write the plan into a copy of the export, beside it, never in place.

    The creating writer: the sweep exists to leave nothing unplaced, so a missing
    sub is made; a missing genre folder is still a warning. The tree is named for
    the emitter guard. Nothing inserted is nothing written.
    """
    if declared is None:
        declared = active_taxonomy.load(cfg)
    tree = rbxml.routing_tree(declared, tree_registry.read(cfg))
    buffer = bytearray(content)
    report = trees.apply_unplaced_changes(plan, buffer, tree=tree)
    if not report.inserted:
        return None, report
    destination = export.with_name(export.stem + PLACED_SUFFIX)
    config.atomic_write_bytes(bytes(buffer), destination)
    return destination, report


def route_unplaced_export(ctx, cfg: config.Config, export: Path) -> Envelope:
    """Plan where every track a fresh export's routing tree does not hold belongs.

    No gate (U91): neither the export nor the database is written. No pending
    import, ever (R-694): every placement is nested, so a written file ends ok
    with a :data:`ROUTING_NOT_LANDABLE` warning.
    """
    declared = active_taxonomy.load(cfg)
    _refuse_off_the_bridge(
        cfg, declared, export, instead="run route unplaced without --export, which "
        "reports what the database's tree does not hold",
    )
    content, plan, items, warnings, gaps = plan_unplaced_export(cfg, export, declared=declared)
    destination, report = apply_unplaced_export(cfg, export, content, plan, declared=declared)
    warnings = [
        *warnings,
        *({"code": "route-write-skipped", "message": text} for text in report.warnings),
    ]
    # "NOTHING TO ROUTE" ONLY WHEN NOTHING WAS LEFT BEHIND, the inbox sweep's
    # rule: it says the tree already holds every track.
    reason = _route_reason(destination, warnings)
    data = _plan(
        items,
        kind="unplaced-export",
        applied=destination is not None,
        reason=reason,
        inserted=report.inserted,
        created=list(report.created),
        output=None if destination is None else str(destination),
        not_derived=list(gaps),
    )
    if destination is None:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    warnings += _routing_not_landable(
        destination,
        report.inserted,
        len(report.created),
        "file the tracks this review names by hand in rekordbox, and route "
        "unplaced without --export only reports; until they are filed, route "
        "unplaced --export plans the same placements on every fresh export",
    )
    return ctx.envelope(data=data, outcome=Outcome.OK, warnings=warnings)

