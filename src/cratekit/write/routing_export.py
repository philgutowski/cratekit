"""The export path of ``route inbox`` and ``route unplaced`` (U86, U91).

A tree that has not cut over is routed into a new file beside a fresh
collection export, never into the database. The verb handlers stay in
:mod:`cratekit.write.routing_cli`, which imports this module and holds the
apply gate; the route here asks that gate through the module at call time.

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
#: (R-688). Every row of a collection export is one rekordbox already holds,
#: and an import keeps the database's rating on such a row, so the sitting
#: that wrote four ratings into a file read all four back as zero.
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

    THE EXTRA TOTALS ARE OUTSIDE THE DIGEST ON PURPOSE. A decision is bound to
    the digest of the plan it was made against, and the totals carry what this
    run did or could not do rather than what it offered, so folding them in would
    make an answer stale for a reason that has nothing to do with the offer.

    ``plan/1`` forbids properties it does not name, so anything a caller needs
    beyond the item list rides here rather than beside it.
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

    A track files into at most three places a person approves: its energy sub,
    the vocal sub beside it, and a genre sub beside that. Each has a column of
    its own, so a gate never shows one place for a track the write files into
    two, and the digest is taken over every one of them. ONE ANSWER for both
    media, so the database gate and the export gate split a track's
    placements the same way.
    """
    if placement.sub == trees.VOX_SUB_CLASS:
        return vocal
    if routing.genre_sub_named(declared, placement.bucket, placement.sub):
        return genre
    return destined


def _placed_counts(tracks: list[dict[str, str]]) -> dict[str, int]:
    """How many of these track items file somewhere, under a vocal sub and under a genre sub.

    One counter for both gates, so a change to what counts as routed lands on
    both screens or on neither.
    """
    return {
        "routed": sum(1 for item in tracks if item["destination"]),
        "vocal": sum(1 for item in tracks if item["vocal"]),
        "genre sub": sum(1 for item in tracks if item.get("genre")),
    }


def _named(plan: dict, names: dict[str, dict[str, str]]) -> dict:
    """The plan as the export gate shows it, each track named (R-692).

    An export id is a number a person has to look up in the export to know
    which song a line files, so each shown item leads with the artist and the
    title the collection row carries, then every field the digest was taken
    over, unchanged. A row with no track, a vocal sub this run creates, and an
    intake key with no collection row get empty names rather than a missing
    column.

    THE NAMES ARE THE SCREEN'S ALONE. The digest and the answered envelope's
    items are the plan's, so a name is outside what a decision is bound to,
    and a JSON reader drops ``artist`` and ``title`` to compare the screen
    with a declined run's items.
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

    The track totals are counted from the items rather than from the planner's
    own structures, so a total cannot disagree with the list printed under it.
    ``count`` below them is every item, playlists created included, so
    ``tracks`` says how many are tracks. The subs a run creates are named,
    because on the list they are a row with no track. ``not derived`` rides
    too, because an empty vocal column on an uncalibrated library means the
    dimension was not read, not that no track is vocal. So do the planner's
    warnings: an intake track with no destination is one it could not read,
    and the reason exists before the question is asked.
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

#: The warning a library with nothing native carries on the database path. It
#: names what the export medium delivers and no more (R-695): a review of the
#: routing, since no import lands nested membership (R-687), and, through
#: :func:`export_remedy`, the one root playlist the inbox sweep writes, which
#: an import does land. This is the whole text when no such playlist is declared.
EXPORT_REMEDY = (
    "no tree has cut over, so nothing files this library into the routing tree. "
    "Export the collection from rekordbox and run route inbox --export with that "
    "file. It writes a review of the routing, and you file its tracks by hand, "
    "since no import can land a nested playlist"
)


def export_remedy(declared: taxonomy.Taxonomy) -> str:
    """:data:`EXPORT_REMEDY`, naming the long track playlist when one is declared.

    ONE TEXT PER DECLARATION, built here so every answer of the verb carries
    the same words. The long track playlist is the one root playlist the inbox
    sweep writes and so the one thing an import lands (R-694); a taxonomy that
    declares none gets the review alone, rather than a playlist it never writes.
    """
    if declared.long_tracks is None:
        return EXPORT_REMEDY
    return (
        f"{EXPORT_REMEDY}. It also adds long tracks to the root playlist "
        f"{declared.long_tracks.display!r}, which one import can land"
    )


#: Why an export routing's file cannot deliver the routing tree, shared by both
#: sweeps' review warning. Measured at the tenth attended sitting (R-687), and
#: the folder half is the source system's paid for learning on the label tree.
NESTED_UNLANDABLE = (
    "a nested playlist imported from the file lands at the playlist root as a "
    "new playlist, and a folder imported from it keeps every playlist it held "
    "and adds a second copy of each"
)
#: The same reason as the step the inbox sweep's pending import gives, since a
#: person importing the root playlist has the routing tree in front of them.
ROUTING_TREE_UNIMPORTABLE = (
    "leave the routing tree's folders and playlists unimported: " + NESTED_UNLANDABLE
)

#: The warning an export sweep gives for the nested membership it wrote into
#: a file no import can land it from (R-694). It stands in for a pending
#: import, since a pending action whose own check could never answer told a
#: person who had done every step the same thing as one who had done none.
ROUTING_NOT_LANDABLE = "routing-not-landable"


def _routing_not_landable(
    destination: Path, inserted: int, created: int, remedy: str
) -> list[dict[str, str]]:
    """The review warning, as a list so a file with no nested change adds nothing.

    ``inserted`` counts the memberships under the routing tree and ``created``
    the sub-playlists made there, both nested, so neither lands through the
    file. ``remedy`` is the step a person takes instead, which differs by verb.
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

    THE INTAKE FOLDER IS A DIRECT CHILD OF THE PLAYLIST ROOT, which is where
    :func:`cratekit.write.rbxml.intake_tree` puts it, so a namesake deeper in
    somebody's tree is never read as their inbox. An export with no such folder
    REFUSES: an empty answer would read as "your inbox is empty", which is the
    one sentence a person would not check.
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
    keys: list[str] = []
    seen: set[str] = set()
    for _path, child in rbxml.walk_nodes(content, node):
        if child.node_type != rbxml.PLAYLIST_TYPE:
            continue
        for key in rbxml.track_keys(content, child):
            if key not in seen:
                seen.add(key)
                keys.append(key)
    return keys


def _readable_file(location: str, cfg: config.Config) -> Path | None:
    """The file a recorded Location names on this machine, or None.

    Through the configured prefix map first, because rekordbox keeps recording
    a volume name long after the drive stopped using it. A Location the map does
    not cover is tried as written, since that is the path rekordbox recorded
    rather than a guess. None when neither is a file here, and the caller routes
    nothing for it: tags read off a file that is not there are all absent, and
    absent tags route to the fallback bucket, which would file a track by the
    one fact nobody measured.
    """
    try:
        decoded = locations.location_to_path(location)
    except locations.LocationDecodeError:
        return None
    rules = [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
    resolved = locations.resolve_recorded_path(decoded, root=cfg.library.root, prefix_map=rules)
    for candidate in (resolved.path, decoded):
        if candidate and candidate.startswith("/") and Path(candidate).is_file():
            return Path(candidate)
    return None


def _unrated(row: dict[str, str]) -> bool:
    """Whether an export row's star rating is still the one nobody set.

    FILL IF EMPTY, and nothing wider. Empty and ``"0"`` are what rekordbox
    writes for a track nobody rated. Any other value, including one this reader
    cannot parse, is somebody's, and overwriting it would need a record of who
    set it that nothing keeps. A row with no ``Rating`` attribute at all is not
    counted either: a rekordbox export writes the attribute on every row, so its
    absence says nothing about whether somebody rated the track.
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

    THE SOURCE SYSTEM'S RULE, IN THE SAME PASS AS THE FILING: every sort set a
    rating from energy on a track whose rating was still zero. The energy is the
    reading the routing decision already took, so the two cannot disagree about
    which track is which level, and the curve and the bucket flag are
    :func:`cratekit.core.routing.energy_rating` and
    :func:`cratekit.core.routing.rates`, called rather than restated.

    OWED, NOT PLANNED (R-688). Every row of a collection export is one
    rekordbox already holds, and an import keeps the database's rating on such
    a row, so a rating written into the file never lands. The export sweep
    counts these into :data:`RATING_NOT_LANDABLE` and writes none of them.
    ROWS, not files: rekordbox rates each row, so two rows naming one file are
    two ratings a person sets.

    THE EXPORT SCALE, which is the taxonomy's own. The cuts are written as 51 to
    255, the values an export carries, so nothing is converted here, and the
    database planner's unconfirmed scale (R-414) is not on this path at all.

    Only a track the pass PLACES is counted. A track with no placement is one
    the declaration has nowhere to put, and the source system rated a track as
    part of filing it.
    ONCE PER FILE, however many places it files into. A vocal track and a
    genre sub track carry a second placement beside their energy sub, and the
    rating is the row's, set once; counting per placement told a person two
    rows owed a rating for one (U155's review).
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

    ``TotalTime`` IS SECONDS. The export fixture carries ``TotalTime="300"`` for
    a five minute track, and :mod:`cratekit.intake.collection_xml` writes a
    file's ``duration_s`` into the same attribute.

    NOTHING IS GUESSED. An absent attribute, one that is not a whole number, and
    zero are all None: zero is what that same emitter writes for a length it
    never measured, so it is "unknown", not "short".
    """
    value = row.get("TotalTime")
    if value is None or not _SECONDS.fullmatch(value.strip()):
        return None
    seconds = int(value.strip())
    return seconds if seconds > 0 else None


@dataclass(frozen=True)
class LongPlan:
    """What the pass adds to the long track playlist, and what it could not read.

    ``keys`` excludes every track the playlist already holds, so a second run
    over its own output plans nothing. ``unreadable`` counts the rows skipped
    for having no readable length.
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

    THE WHOLE COLLECTION, not the intake folder, as the source system read it:
    a set imported before this pass existed is still a set.

    A FOLDER of the playlist's name under the root is a warning and nothing is
    planned. The writer would refuse it anyway, and planning over it would offer
    a write that cannot happen. The warning keeps the run from answering
    ``nothing-to-route``, which says the library is filed, over a playlist it
    could not build.
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

    Returns the bytes with the subs in place and each ``folder/sub`` created.

    THE ROUTING WRITER DOES NOT CREATE A SUB, by design, so a vocal track could
    only land under "with vox" in a folder that already had one. This is the
    source system's ``dj-create-vox-playlists`` run first, on the same bytes, as
    that system ran it before its vocal routing. It runs only on a CALIBRATED
    library whose taxonomy declares the vocal sub: with no cut nothing is filed
    as vocal, and an empty playlist per folder would be a change nobody asked
    for. It is idempotent, so a second run over its own output creates none.

    The tree is the governed routing tree :func:`apply_export` writes, so the
    emitter guard is armed for this write as it is for the routing. A tree the
    vocal writer cannot reach is a warning and the routing still runs, because
    the routing writer reports the same tree for itself.
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

    ``plan`` is what a bridge writer takes, keyed on ``(folder, sub)``.
    ``destined``, ``vocal`` and ``genre`` name each track's energy sub, vocal
    sub and genre sub as a person is shown them. ``files`` maps each readable file to the keys that
    name it, and ``readings`` and ``placements`` are the engine's own answers,
    kept for a caller that counts owed ratings from the same reading.
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

    ONE DECISION FOR BOTH EXPORT SWEEPS, the inbox and the unplaced (U91). The
    readings come from :func:`cratekit.write.rebuild.read_truth`, the placements
    from :func:`cratekit.write.rebuild.derive_from_taxonomy`, and the display
    names from :func:`cratekit.write.routing_pass.destination`, so the two sweeps
    and the database medium cannot disagree about where a track goes.

    A row whose Location names no file here is a warning and is not routed:
    tags read off a file that is not there are all absent, and absent tags route
    to the fallback bucket, which would file a track by the one fact nobody
    measured.
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

    ``content`` is the export's bytes with any vocal sub-playlist already
    added, which is why they are returned rather than read again. ``plan`` is
    what the bridge writer takes, ``owed`` how many rows are owed a star
    rating, ``items`` what the digest is taken over, and ``names`` each planned
    track's artist and title by export id, for :func:`_named` alone (R-692).
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

    Returns an :class:`ExportPlan`, the fields named there.

    NO STAR RATING IS PLANNED (R-688). The ratings the source system's sort
    would have set are only counted, because the medium cannot carry them: see
    :func:`_owed_ratings`. The count is not a warning here, because the
    warnings decide whether a run was blocked and an owed rating never blocks
    one; the verb gives it as :data:`RATING_NOT_LANDABLE` beside them.

    THE ROUTING DECISION IS THE NATIVE PATH'S, called rather than restated. The
    readings come from :func:`cratekit.write.rebuild.read_truth`, the placements
    from :func:`cratekit.write.rebuild.derive_from_taxonomy`, and the display
    names from :func:`cratekit.write.routing_pass.destination`, which are the
    three calls :func:`plan_inbox` makes through ``declared_membership``. So the
    two media cannot disagree about where a track goes. The genre is the FILE's,
    not the export's ``Genre`` attribute, for the reason
    :func:`cratekit.core.tags.read_genre_from_file` gives.

    THE CALIBRATED CUT IS THE ONE LOADER'S, the same read :func:`plan_inbox`
    makes (U89). With none the vocal dimension is named in ``gaps`` rather than
    derived. With one, a vocal track files under the vocal sub as well as its
    energy sub, and :func:`_vox_subs` has made that sub first.
    """
    content = _read_export(export)
    if declared is None:
        # ONE READ PER VERB (R-685): the verb passes the declaration it
        # checked the bridge with, so the plan, the write and the pending
        # action are one declaration. A caller that has none reads it here.
        declared = active_taxonomy.load(cfg)
    keys = _inbox_keys(content, declared, export)
    by_id = {
        track.track_id: rbxml.attributes(content, track)
        for track in rbxml.collection_tracks(content)
    }
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
    plan, destined, vocal = decision.plan, decision.destined, decision.vocal
    gaps = decision.gaps
    owed = _owed_ratings(
        declared, decision.placements, decision.readings, decision.files, by_id
    )
    long_plan = _long_tracks(declared, content, by_id, warnings)
    lengthy = set(long_plan.keys)
    playlist = declared.long_tracks.display if declared.long_tracks else ""
    # The long track playlist rides the item, so it is inside the digest a
    # person approves: a write nobody was shown is a write nobody agreed to. A
    # long track outside the intake gets an item of its own, and so does each
    # vocal sub-playlist this run creates, with no track and the new playlist
    # as its destination. A vocal track's second placement rides as ``vocal``,
    # beside the energy sub it also files into.
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
        item["track_id"]: {
            "artist": by_id[item["track_id"]].get("Artist", ""),
            "title": by_id[item["track_id"]].get("Name", ""),
        }
        for item in items
        if item["track_id"] in by_id
    }
    return ExportPlan(
        content, plan, owed, long_plan, items, warnings, gaps, vox_created, names
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

    Returns the file written or None, the membership report, how many tracks
    the long track playlist gained, and the warning its writer gave. The count
    is the writer's and not the plan's.

    THE MEDIUM FOLLOWS THE REGISTRY. The tree is the governed routing tree, so
    the emitter guard in :func:`cratekit.write.rbxml.splice_into_subplaylist`
    refuses a tree that has cut over, and the caller has already refused it by
    name before offering a plan.

    THE NON CREATING WRITER, because this sweep runs against a tree a person
    curated: a sub that is not there is a warning naming the bucket, never a
    playlist invented in somebody's library.

    NO RATING IS WRITTEN (R-688). The source system set ratings in these
    bytes, and an import keeps the database's rating on every row an export
    carries, so a patched ``Rating`` is a write that never lands.

    NOTHING CHANGED IS NOTHING WRITTEN. A file identical in every routed byte
    to the export would still be a file somebody is told to read. A long
    track the playlist lacks is a change, and so is a vocal sub-playlist
    ``content`` already gained from :func:`_vox_subs`, which the review names
    though no import can land it, since it is nested (R-694).

    THE LONG TRACK PLAYLIST IS WRITTEN LAST and ONCE, add only, as the source
    system wrote it last. It is a direct child of the playlist
    root and no tree, so no registry answer governs it.
    """
    if declared is None:
        # ONE READ PER VERB (R-685): the verb passes the declaration it
        # checked the bridge with, so the plan, the write and the pending
        # action are one declaration. A caller that has none reads it here.
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
    """The import an inbox sweep owes, which is the root playlist it added to alone.

    ONLY A ROOT PLAYLIST LANDS through the file (R-687), and the long track
    playlist is the one root playlist this sweep writes, so the caller asks for
    this only when that playlist gained tracks (R-694). The nested routing the
    same file carries is a review, and :func:`_routing_not_landable` says so
    beside this rather than inside a promise no import can keep.
    """
    return PendingHumanAction(
        kind="rekordbox_import",
        id=new_pending_id(run_id),
        # NO RATING IS CLAIMED (R-688): this file carries none, since an
        # import keeps the database's rating on every row an export holds.
        summary=(
            f"{lengthened} long track(s) were added to the root playlist "
            f"{playlist!r} in {destination.name}, which rekordbox has not imported yet"
        ),
        # THIS VERB IS ITS OWN CHECK, and since R-694 it can answer. Over a
        # fresh export taken after the import the playlist holds its tracks, so
        # a second run adds none and owes no import; the routing it plans
        # again is a review, since nested membership never lands through the
        # file (R-687). Named by the caller from its registry entry, because
        # this layer may not spell a verb (KTD23).
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


def _refuse_off_the_bridge(
    cfg: config.Config, declared: taxonomy.Taxonomy, export: Path, *, instead: str
) -> None:
    """Refuse an export sweep the bridge cannot serve, before anything is read.

    A TREE THAT HAS CUT OVER is the database's, and an export carrying new
    membership for it would put a second tree beside the real one on import.
    ``instead`` is the step a person takes, which differs by verb.

    AN ABSENT LIBRARY ROOT is the source system's mount guard. With the volume
    gone every Location names nothing, every track warns, and a plan that routed
    nothing would be the only thing a person saw.
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

    THE ROUTING TREE HAS TO BE ON THE BRIDGE, and the volume has to be there,
    both asked by :func:`_refuse_off_the_bridge` before the plan is offered, so a
    person is never asked to approve a write the guard would stop.
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
    # ONE CODE FOR EVERY SKIPPED WRITE, because the writer reports a missing
    # tree, a missing genre folder and a missing sub as sentences and the
    # sentence already names which. A code naming only the sub would call an
    # export with no routing tree at all a missing playlist.
    warnings = [
        *warnings,
        *({"code": "route-write-skipped", "message": text} for text in report.warnings),
        *(
            [{"code": "route-write-skipped", "message": long_warning}]
            if long_warning
            else []
        ),
    ]
    # "NOTHING TO ROUTE" ONLY WHEN NOTHING WAS LEFT BEHIND. It says the library
    # is filed, so a run whose every write was skipped, or whose every track
    # could not be read, must not give it: that is a run that could not route,
    # not a library already filed. The owed
    # ratings are not in ``warnings`` yet: no run of this medium can ever land
    # one (R-688), so counting them would answer route-blocked over a library
    # already filed, every time. They join the warnings after the answer.
    if destination is not None:
        reason = None
    elif warnings:
        reason = "route-blocked"
    else:
        reason = "nothing-to-route"
    warnings += unrated
    data = _plan(
        items,
        kind="inbox-export",
        applied=destination is not None,
        reason=reason,
        inserted=report.inserted,
        long_added=lengthened,
        duration_unreadable=long_plan.unreadable,
        # THE PLAN'S LIST, and the writer's too: the subs are in the bytes the
        # writer was handed, and a sub created is a change, so whenever this
        # list is not empty a file was written and carries every one of them.
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
    # A PENDING IMPORT ONLY FOR WHAT AN IMPORT CAN LAND (R-694). The long track
    # playlist is the one root playlist this sweep writes, so a file that added
    # nothing to it owes no import: it is a review, and ends ok. Before this,
    # every run with a routing ended pending, and so did the check run a person
    # makes after importing, since the routing never lands and plans again.
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

    THE QUESTION IS ASKED OF THE DATABASE, not answered with a constant. Until
    U53 this was ``_plan([], ...)``, which reports "your library is fully filed"
    for a library nobody looked at, and no green suite can tell that apart from a
    library that really is filed.

    COVERAGE IS MEMBERSHIP UNDER THE GOVERNED ROOT, read by walking DOWN from the
    adopted root identifier through :func:`cratekit.write.rebuild.read_tree`,
    never by finding a folder with the declared name. A walk by name finds a
    namesake anywhere in the library and reports on that instead.

    A LIBRARY WITH NOTHING NATIVE IS NOT COMPARED, and the totals say so. An
    empty answer there would be the constant defect arriving by a different
    route: nothing was read, so nothing about the tree was learned.
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
    # THE TOMBSTONED HALF IS NOT UNPLACED. A row rekordbox has soft-deleted is
    # not a track waiting to be filed, and reporting one would send somebody to
    # place something they removed on purpose.
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
#: Not ``ROUTED_SUFFIX``: a sweep of the same export would replace an inbox
#: routing nobody has imported yet, and the intake filing would go with it.
PLACED_SUFFIX = "_placed.xml"

#: The warning the report carries when no tree has cut over. It names what the
#: export medium delivers here (R-695), a review and nothing an import lands,
#: since every placement is nested membership under the routing tree (R-694).
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

    THE WRITER'S OWN SCOPE. :func:`cratekit.write.rbxml.splice_into_subplaylist`
    looks for the tree among the root's children and nowhere deeper, so the set
    of tracks it could place is read from the same node. The coverage audit
    widens this to a tree filed inside another folder, which it can report on
    and this sweep could not write into.

    AN ABSENT TREE REFUSES. Every track would read as unplaced and every write
    would be skipped, so the one answer a person would see is a plan to re-file
    a whole library into a tree the file does not hold.
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

    THE COVERAGE AUDIT'S RULE, and the source system's: a track is placed when a
    playlist ANYWHERE under the tree holds it, whatever the sub, so a track a
    person filed by hand into a sub the declaration would not choose is left
    where it is. Only playlists are read, because a folder's byte range holds
    its children's keys and would count them twice as its own.

    A track in the intake folder and not under the tree is unplaced, which is
    what the source system's sweep read too.
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

    Returns the bytes to write into, the plan the creating writer takes, the
    items a person is shown, the warnings, and the dimensions not derived.

    THE DECISION IS :func:`_decide`'s, the one the inbox sweep makes, over the
    calibrated cut the one loader reads. A vocal track files under the vocal sub
    as well, and the creating writer makes that sub where it is absent, so no
    separate vocal pass runs first.
    """
    content = _read_export(export)
    if declared is None:
        # ONE READ PER VERB (R-685): the verb passes the declaration it
        # checked the bridge with, so the plan, the write and the review
        # warning are one declaration. A caller that has none reads it here.
        declared = active_taxonomy.load(cfg)
    tree_node = _routing_tree_node(content, declared, export)
    by_id = {
        track.track_id: rbxml.attributes(content, track)
        for track in rbxml.collection_tracks(content)
    }
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

    THE CREATING WRITER, :func:`cratekit.write.trees.apply_unplaced_changes`,
    and this is its first caller. The sweep exists to leave nothing unplaced,
    so a bucket with no sub yet is the ordinary case, and refusing to create one
    would leave behind exactly the tracks the sweep was run for. A missing GENRE
    folder is still a warning: the writer creates a playlist, never a folder.

    THE TREE IS NAMED, so the emitter guard refuses a tree that has cut over
    behind the refusal the caller already made by name.

    NOTHING INSERTED IS NOTHING WRITTEN. A file identical to the export would
    still be a review somebody is told to read.
    """
    if declared is None:
        # ONE READ PER VERB (R-685): the verb passes the declaration it
        # checked the bridge with, so the plan, the write and the review
        # warning are one declaration. A caller that has none reads it here.
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

    NO GATE, and that is the brief's decision (U91). The export and the
    database are never written; the plan lands beside the export as a review,
    written by :func:`apply_unplaced_export`, which owes no import.
    The report without ``--export`` is unchanged.

    NO PENDING IMPORT, EVER (R-694). Every placement is nested membership
    under the routing tree, which never lands through the file (R-687), so a
    written file ends ok with a :data:`ROUTING_NOT_LANDABLE` warning naming the
    step a person takes instead. A pending import here could never be proven,
    since the check run plans the same placements until they are filed by hand.
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
    # rule and for its reason: it says the tree already holds every track.
    if destination is not None:
        reason = None
    elif warnings:
        reason = "route-blocked"
    else:
        reason = "nothing-to-route"
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

