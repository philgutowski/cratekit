"""The four ``route.*`` verbs: inbox, unplaced, resort, pending (U20).

WHY THIS MODULE LIVES UNDER WRITE. The registry names
``cratekit.write.routing_cli``, and the countdown in ``tests/_pending.py``
keys on that string. A second path would leave the register armed over a
module that exists, which is a green countdown.

WHAT IT MUST NOT IMPORT. ``cratekit.cli.registry`` is the CLI layer. Naming
that type here is an upward import. The legal shape is the one
``cratekit.adopt.scan_cli`` uses: :mod:`cratekit.cli.output` alone, which is
foundation-ranked, and unannotated builder parameters.

EVERY CLOSE GOES THROUGH :func:`cratekit.write.routing_pass.close_run`.
``session.close_session`` is exported and bypasses the two gates that refuse
a run still holding a track nowhere or an export nobody has imported. A
call of that name in this file is the defect the armed guard is waiting for.

A RE-RUN AFTER A DESTINATION RENAME CONVERGES. The engine reads the node
map U36 recorded, through :func:`cratekit.write.rebuild.resolve_destinations`.
This surface does not build a second map.

THREE OF THE FOUR VERBS REPORTED WORK THEY HAD NOT DONE, until U53. ``inbox``
built a plan, asked its apply gate and returned the same plan whichever way
the person answered, so somebody who confirmed saw a plan and believed it had
happened. ``unplaced`` was the constant empty plan, which reads as "your
library is fully filed" on a library nobody had looked at. ``resort`` queued a
job with no items, which the driver walks in one empty pass and transitions
straight to succeeded. All three are the same failure wearing three faces: a
green report over an act nobody performed.

WHAT THE APPLY WRITES IS NOT A SECOND ROUTER. The intake files are read for
their tags, the placements come from
:func:`cratekit.write.rebuild.declared_membership` through the derivation the
REGISTRY records for the tree, the destinations resolve through
:func:`cratekit.write.rebuild.plan_destinations`, and the write goes through
:func:`cratekit.write.trees.write_tree_membership`, which owns the session
gates. Nothing about where a track goes is decided in this file.

Layer: write.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, PendingHumanAction, digest_of, new_pending_id
from cratekit.core import (
    analysis_store,
    config,
    convergence,
    jobs,
    locations,
    rb_writer,
    routing,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import metadata_cli, rbxml, rebuild, routing_pass, trees

#: The session log's name for a write this verb performed, one per verb, so a
#: person reading the log can tell which act touched their library. Not shared
#: with the rebuild's own workflow: two verbs writing under one name is a log
#: that cannot answer the only question anybody asks it.
INBOX_WORKFLOW = "route-inbox"
RESORT_WORKFLOW = "route-resort"

#: What each driven resort left where it was, by job, from the worker to the
#: resume that drove it (R-312). PROCESS LOCAL ON PURPOSE. The driver runs the
#: worker inside the resume's own process, and a worker's return is the artifact
#: channel and nothing else, so this is the one way the engine's measurement
#: reaches the envelope without a second walk of the library. The resume drains
#: its own job's entry, so nothing outlives the run that measured it.
_LEFT_BEHIND: dict[str, list[rebuild.Difference]] = {}


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("routing_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


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


def _no_op(state: str, **progress: Any) -> dict[str, Any]:
    """A run that correctly queued nothing. ``job_id`` is "" because the schema
    types it as a string (R-234)."""
    return {"job_id": "", "state": state, "cause": None, "progress": dict(progress)}


def _inbox_items(cfg: config.Config) -> list[dict[str, str]]:
    declared = taxonomy.default_taxonomy()
    folder = Path(cfg.library.root) / declared.intake.display
    if not folder.is_dir():
        return []
    items: list[dict[str, str]] = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and not path.name.startswith("."):
            items.append({"path": str(path), "name": path.name})
    return items


def _apply_gate(ctx, plan: dict) -> str:
    spec = ctx.entry.gates[0]
    return ctx.gate.require(spec, digest=plan["digest"])


def _close_run(record, cfg: config.Config):
    """The one close this surface may perform.

    Named so the AST walk that forbids ``close_session`` finds this call and
    not a bypass.
    """
    return routing_pass.close_run(record, cfg)


#: What is recorded as the evidence when the routing pass is what proved an
#: import. No verb is named, because the record outlives any one verb's name.
#: It says what was seen and no more: a track a person acknowledged as gone
#: reached no row, and the sentence does not claim it did.
PLACED_EVIDENCE = (
    "the routing pass reached a row for every track this run landed that nobody "
    "acknowledged as gone"
)


def _close_if_settled(cfg: config.Config, session_id: str) -> None:
    for record in session.records(cfg):
        if record.session_id != session_id or record.terminal:
            continue
        if record.state is session.SessionState.AWAITING_IMPORT and _all_settled(
            cfg, session_id
        ):
            # AN INTAKE RUN NOW ENDS ``awaiting-import`` (R-501), and the gated
            # close refuses that state. Here the pass has reached a row for
            # every track the run recorded, which is stronger proof of the
            # import than any export, so the proof is recorded and the close
            # goes ahead. A run with no ROUTED track proves nothing, and is
            # left for the close to refuse.
            session.mark_import_verified(record, cfg, evidence=PLACED_EVIDENCE)
        _close_run(record, cfg)
        return


def _all_settled(cfg: config.Config, session_id: str) -> bool:
    """True when nothing is outstanding for this run AND the pass reached a row for it.

    SETTLED IS NOT IMPORTED. A track settles by being routed, which takes a
    row, or by a person acknowledging it is gone, which takes none. A run whose
    every track was acknowledged settled without any import, so at least one
    routed track is required before the pass counts as proof of one.
    """
    ledger = routing_pass.read(cfg)
    routed = [
        entry
        for entry in ledger.intents
        if entry.session_id == session_id and entry.state is routing_pass.TrackState.ROUTED
    ]
    return bool(routed) and not ledger.outstanding(session_id)


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def build_inbox(parser, entry) -> None:
    parser.add_argument(
        "--export",
        default=None,
        metavar="PATH",
        help="route the INBOX playlist of this fresh export and write "
        "<name>_routed.xml beside it, for a tree that has not cut over",
    )
    parser.set_defaults(_handler=route_inbox)


def build_unplaced(parser, entry) -> None:
    parser.add_argument(
        "--export",
        default=None,
        metavar="PATH",
        help="place every track the routing tree of this fresh export does not "
        "hold and write <name>_placed.xml beside it, for a tree that has not cut over",
    )
    parser.set_defaults(_handler=route_unplaced)


def build_resort(parser, entry) -> None:
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the resort already queued under this identifier",
    )
    parser.set_defaults(_handler=route_resort)


def build_pending(parser, entry) -> None:
    parser.add_argument(
        "--session",
        default=None,
        metavar="SESSION_ID",
        help="place outstanding tracks for this run only; every open run by default",
    )
    parser.set_defaults(_handler=route_pending)


def resort_argv(job) -> list[str]:
    return ["route", "resort", "--job", job.job_id]


def apply_inbox(cfg: config.Config, items: list[dict[str, str]]) -> dict[str, Any]:
    """File the intake folder into every tree that has cut over.

    THE ONE THING THIS FUNCTION EXISTS FOR is that it is the call the confirmed
    branch was missing. Everything it does is a call into an engine that already
    owns the rule: the tag readings come from
    :func:`cratekit.write.rebuild.read_truth`, the placements from
    ``declared_membership`` through the derivation the registry records, the
    destinations from ``plan_destinations``, and the write from
    ``write_tree_membership``, which takes the acknowledgment, the volume
    identity, the session lock, the verified capture and the analysis watch.

    A LIBRARY WITH NOTHING NATIVE WRITES NOTHING AND SAYS SO. Every tree is on
    the XML bridge until its cutover, and membership written into the database
    for one of those is membership the next import overwrites. Reported as its
    own answer rather than as an empty success, because "nothing needed doing"
    and "there is nowhere to put this yet" are different sentences with different
    remedies.

    THE READINGS ARE TAKEN ONCE AND REUSED FOR EVERY TREE. ``read_truth`` never
    raises for an unreadable file, so a stray file in the intake folder routes to
    the declared fallback and is visible in the result rather than abandoning the
    run.
    """
    entries = tree_registry.read(cfg)
    native = _native_trees(entries)
    if not native:
        return {"applied": False, "reason": "no-native-tree", "added": 0, "skipped": 0}
    # THE CALIBRATED CUT, read before the database is opened so a corrupt
    # calibration refuses before anything is written (U89). None on a library
    # never calibrated, and the engine then names the dimension it left out.
    threshold = metadata_cli.load_vocal_threshold(cfg)
    readings = [rebuild.read_truth(Path(item["path"])) for item in items]
    declared = taxonomy.default_taxonomy()
    added = 0
    skipped = 0
    # WHAT THE ENGINE SAID IT DID NOT COMPARE, kept rather than dropped (R-316).
    # Dropping it is how a confirmed apply over a taxonomy that declares a vocal
    # sub-playlist reported an ordinary write while filing nothing into it.
    not_compared: set[str] = set()
    handle = rb_writer.open_db(cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        for tree_id in native:
            placements, gaps = rebuild.declared_membership(
                cfg,
                declared,
                source=entries.derivation_source(tree_id),
                vocal_threshold=threshold,
                truth=readings,
            )
            not_compared.update(gaps)
            root_id = tree_registry.anchored_root(
                tree_id, entries, root_exists=lambda root: root in known
            )
            standing = rebuild.read_tree(handle, root_id)
            # THE NODE MAP U36 RECORDED, read rather than rebuilt, which is what
            # makes a re-run after a destination rename converge on the same
            # playlist instead of creating a second one.
            record = convergence.read(cfg).tree(tree_id)
            _destinations, plan = rebuild.plan_destinations(
                declared, placements, standing, record, tree_id=tree_id
            )
            report = trees.write_tree_membership(
                cfg,
                handle,
                tree_id=tree_id,
                registry=entries,
                plan=plan,
                rows=rows,
                root_exists=lambda root: root in known,
                # THE LIBRARY ROOT, which is what ``route_pending`` twelve
                # functions below already names and for the same reason: the
                # watch walks for ANLZ files by name and those do not sit beside
                # the audio, so naming a narrower directory arms a watch over
                # nothing and reports a clean session whatever happened to the
                # grids. The empty-list refusal cannot catch that, because a
                # barren list is not an empty one.
                analysis_roots=analysis_store.watch_roots(cfg),
                workflow=INBOX_WORKFLOW,
            )
            added += report.added
            skipped += len(report.skipped)
    finally:
        rb_writer.close_db(handle)
    return {
        "applied": True,
        "reason": None,
        "added": added,
        "skipped": skipped,
        "trees": len(native),
        "not_compared": tuple(sorted(not_compared)),
    }


#: The suffix of the file an export routing writes, beside the export it read.
ROUTED_SUFFIX = "_routed.xml"

#: The warning a library with nothing native carries on the database path, so
#: the answer names the medium that does work today rather than only the one
#: that does not.
EXPORT_REMEDY = (
    "no tree has cut over, so this library is still filed through an export: "
    "export the collection from rekordbox and run route inbox --export with that file"
)

#: The same, for the deferred placements. They wait for a cutover, and what a
#: person can settle before one is the import itself.
PENDING_REMEDY = (
    "no tree has cut over, so no deferred placement can be made and none was "
    "read: these tracks are placed once a tree is database native. An import is "
    "proven by intake imported --export with a Fresh Export, not by this verb"
)


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
    planned either: the writer patches a value in place and cannot add one, so a
    rating planned there would be a write the run declares and never performs.
    """
    value = row.get("Rating")
    return value is not None and value.strip() in ("", "0")


def _ratings(
    declared: taxonomy.Taxonomy,
    placements: tuple[rebuild.DeclaredPlacement, ...],
    readings: list[rebuild.Truth],
    files: dict[str, list[str]],
    by_id: dict[str, dict[str, str]],
) -> dict[str, int]:
    """The star rating each unrated intake track takes from its energy.

    THE SOURCE SYSTEM'S RULE, IN THE SAME PASS AS THE FILING: every sort set a
    rating from energy on a track whose rating was still zero. The energy is the
    reading the routing decision already took, so the two cannot disagree about
    which track is which level, and the curve and the bucket flag are
    :func:`cratekit.core.routing.energy_rating` and
    :func:`cratekit.core.routing.rates`, called rather than restated.

    THE EXPORT SCALE, which is the taxonomy's own. The cuts are written as 51 to
    255, the values an export carries, so nothing is converted here, and the
    database planner's unconfirmed scale (R-414) is not on this path at all.

    Only a track the pass PLACES is rated. A track with no placement is one the
    declaration has nowhere to put, and a rating is part of filing it.
    """
    energy = {reading.location: reading.energy for reading in readings}
    plan: dict[str, int] = {}
    for placement in placements:
        if not routing.rates(declared, placement.bucket):
            continue
        rating = routing.energy_rating(declared, energy.get(placement.location))
        if rating is None:
            continue
        for key in files[placement.location]:
            if _unrated(by_id[key]):
                plan[key] = rating
    return plan


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
    ``nothing-to-route``, the answer the import check reads as done.
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
    ``destined`` and ``vocal`` name each track's energy sub and vocal sub as a
    person is shown them. ``files`` maps each readable file to the keys that
    name it, and ``readings`` and ``placements`` are the engine's own answers,
    kept for a caller that rates from the same reading.
    """

    plan: dict[tuple[str, str], list[str]]
    destined: dict[str, str]
    vocal: dict[str, str]
    files: dict[str, list[str]]
    readings: list[rebuild.Truth]
    placements: tuple[rebuild.DeclaredPlacement, ...]
    gaps: tuple[str, ...]


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
    for placement in placements:
        folder, sub = routing_pass.destination(declared, placement.bucket, placement.sub)
        named = vocal if placement.sub == trees.VOX_SUB_CLASS else destined
        for key in files[placement.location]:
            plan.setdefault((folder, sub), []).append(key)
            named[key] = f"{folder}/{sub}"
    return Decision(plan, destined, vocal, files, readings, placements, gaps)


def plan_export(
    cfg: config.Config, export: Path
) -> tuple[
    bytes,
    dict[tuple[str, str], list[str]],
    dict[str, int],
    LongPlan,
    list[dict[str, str]],
    list[dict[str, str]],
    tuple[str, ...],
    tuple[str, ...],
]:
    """Read one fresh export and decide where each intake track goes.

    Returns the bytes to write into, the plan the bridge writer takes, the star
    ratings to fill, the long track additions, the items a person is shown, the
    warnings, the dimensions not derived, and the vocal sub-playlists created.
    The bytes are the export's with any vocal sub-playlist already added, which
    is why they are returned rather than read again.

    THE ROUTING DECISION IS THE NATIVE PATH'S, called rather than restated. The
    readings come from :func:`cratekit.write.rebuild.read_truth`, the placements
    from :func:`cratekit.write.rebuild.derive_from_taxonomy`, and the display
    names from :func:`cratekit.write.routing_pass.destination`, which are the
    three calls :func:`apply_inbox` makes through ``declared_membership``. So the
    two media cannot disagree about where a track goes. The genre is the FILE's,
    not the export's ``Genre`` attribute, for the reason
    :func:`cratekit.core.tags.read_genre_from_file` gives.

    THE CALIBRATED CUT IS THE ONE LOADER'S, the same read :func:`apply_inbox`
    makes (U89). With none the vocal dimension is named in ``gaps`` rather than
    derived. With one, a vocal track files under the vocal sub as well as its
    energy sub, and :func:`_vox_subs` has made that sub first.
    """
    content = _read_export(export)
    declared = taxonomy.default_taxonomy()
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
    ratings = _ratings(
        declared, decision.placements, decision.readings, decision.files, by_id
    )
    long_plan = _long_tracks(declared, content, by_id, warnings)
    lengthy = set(long_plan.keys)
    playlist = declared.long_tracks.display if declared.long_tracks else ""
    # The rating and the long track playlist ride the item, so both are inside
    # the digest a person approves: a write nobody was shown is a write nobody
    # agreed to. A long track outside the intake gets an item of its own, and so
    # does each vocal sub-playlist this run creates, with no track and the new
    # playlist as its destination. A vocal track's second placement rides as
    # ``vocal``, beside the energy sub it also files into.
    items = [
        {
            "track_id": key,
            "destination": destined.get(key, ""),
            "vocal": vocal.get(key, ""),
            "rating": str(ratings[key]) if key in ratings else "",
            "long_track": playlist if key in lengthy else "",
        }
        for key in keys
    ]
    intake = set(keys)
    items += [
        {"track_id": key, "destination": "", "vocal": "", "rating": "", "long_track": playlist}
        for key in long_plan.keys
        if key not in intake
    ]
    items += [
        {"track_id": "", "destination": created, "vocal": "", "rating": "", "long_track": ""}
        for created in vox_created
    ]
    return content, plan, ratings, long_plan, items, warnings, gaps, vox_created


def apply_export(
    cfg: config.Config,
    export: Path,
    content: bytes,
    plan: dict[tuple[str, str], list[str]],
    ratings: dict[str, int],
    long_plan: LongPlan = LongPlan(),
    vox_created: tuple[str, ...] = (),
) -> tuple[Path | None, trees.RouteReport, int, int, str | None]:
    """Write the plan into a copy of the export, beside it, never in place.

    Returns the file written or None, the membership report, how many star
    ratings the writer actually set, how many tracks the long track playlist
    gained, and the warning its writer gave. Both counts are the writers' and
    not the plan's.

    THE MEDIUM FOLLOWS THE REGISTRY. The tree is the governed routing tree, so
    the emitter guard in :func:`cratekit.write.rbxml.splice_into_subplaylist`
    refuses a tree that has cut over, and the caller has already refused it by
    name before offering a plan.

    THE NON CREATING WRITER, because this sweep runs against a tree a person
    curated: a sub that is not there is a warning naming the bucket, never a
    playlist invented in somebody's library.

    THE RATINGS GO INTO THE SAME BYTES, after the membership, as the source
    system applied them. A rating is an attribute of a track and membership of
    nothing, so a sub the writer skipped does not un-rate the track it held.

    NOTHING CHANGED IS NOTHING WRITTEN. A file identical in every routed byte
    to the export would still be a file somebody is told to import. A track
    already filed and still unrated is a change, so a pass that only rates
    writes a file, and so is a long track the playlist lacks. So is a vocal
    sub-playlist ``content`` already gained from :func:`_vox_subs`, which is
    the new node this file exists to carry into rekordbox.

    THE LONG TRACK PLAYLIST IS WRITTEN LAST and ONCE, add only, as the source
    system wrote it after the ratings. It is a direct child of the playlist
    root and no tree, so no registry answer governs it.
    """
    declared = taxonomy.default_taxonomy()
    tree = rbxml.routing_tree(declared, tree_registry.read(cfg))
    buffer = bytearray(content)
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
    rated = trees.apply_rating_changes(ratings, buffer)
    lengthened, long_warning = 0, None
    if long_plan.keys and declared.long_tracks is not None:
        lengthened, long_warning = trees.add_to_root_playlist(
            declared.long_tracks.display, long_plan.keys, buffer
        )
    if not report.inserted and not rated and not lengthened and not vox_created:
        return None, report, rated, lengthened, long_warning
    destination = export.with_name(export.stem + ROUTED_SUFFIX)
    config.atomic_write_bytes(bytes(buffer), destination)
    return destination, report, rated, lengthened, long_warning


def _export_pending(
    run_id: str,
    verb: str,
    destination: Path,
    inserted: int,
    rated: int,
    lengthened: int = 0,
    playlist: str = "",
    vox_created: int = 0,
) -> PendingHumanAction:
    added = (
        f", and {lengthened} long track(s) were added to the {playlist!r} playlist"
        if lengthened
        else ""
    )
    if vox_created:
        added += f", and {vox_created} vocal sub-playlist(s) were created"
    return PendingHumanAction(
        kind="rekordbox_import",
        id=new_pending_id(run_id),
        summary=(
            f"{inserted} track(s) were routed and {rated} unrated track(s) were "
            f"given a star rating from energy{added} in {destination.name}, which "
            f"rekordbox has not imported yet"
        ),
        # THIS VERB IS ITS OWN CHECK. Over a fresh export taken after the import,
        # a second run inserts nothing and rates nothing, and that is the only
        # reading in this build that the import happened. Named by the caller
        # from its registry entry, because this layer may not spell a verb (KTD23).
        verify_verb=verb,
        artifact=str(destination),
        steps=(
            f"import {destination} into rekordbox as a rekordbox xml library and "
            f"import the routing tree, the tracks' ratings and any root playlist "
            f"this run added tracks to from it",
            "then export the collection again and run route inbox --export with "
            "that file, which routes, rates and adds nothing once the import has "
            "landed",
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
    declared = taxonomy.default_taxonomy()
    _refuse_off_the_bridge(
        cfg, declared, export, instead="run route inbox without --export, which "
        "writes the database",
    )
    content, plan, ratings, long_plan, items, warnings, gaps, vox_created = plan_export(
        cfg, export
    )
    offered = _plan(items, kind="inbox-export")
    option = _apply_gate(ctx, offered)
    if option != "apply":
        return ctx.envelope(
            data=_plan(items, kind="inbox-export", applied=False),
            outcome=Outcome.NO_OP,
            warnings=warnings,
        )
    destination, report, rated, lengthened, long_warning = apply_export(
        cfg, export, content, plan, ratings, long_plan, vox_created
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
    # "NOTHING TO ROUTE" ONLY WHEN NOTHING WAS LEFT BEHIND. It is the answer the
    # pending action names as proof an import landed, so a run whose every write
    # was skipped, or whose every track could not be read, must not give it:
    # that is a run that could not route, not a library already filed. A run
    # that only rated wrote a file, so it is pending like any other, and its
    # skipped writes still ride as warnings.
    if destination is not None:
        reason = None
    elif warnings:
        reason = "route-blocked"
    else:
        reason = "nothing-to-route"
    data = _plan(
        items,
        kind="inbox-export",
        applied=destination is not None,
        reason=reason,
        inserted=report.inserted,
        rated=rated,
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
    return ctx.envelope(
        data=data,
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=_export_pending(
            ctx.run.run_id,
            ctx.entry.name,
            destination,
            report.inserted,
            rated,
            lengthened,
            declared.long_tracks.display if declared.long_tracks else "",
            len(vox_created),
        ),
        warnings=warnings,
    )


def route_inbox(ctx) -> Envelope:
    """Offer a plan for the intake folder, then apply it if the person says so.

    THE BRANCH IS WRITTEN AS "not apply" RATHER THAN AS "is abort", which is the
    same direction the readiness answers in :mod:`cratekit.write.routing_pass`
    are derived in and for the same reason: only the one answer that means yes
    may write, so an option added to this gate later cannot acquire the writing
    behaviour by nobody having classified it.

    WITH ``--export`` THE INTAKE IS THE EXPORT'S, not the disk folder, and the
    write is a new file rather than the database. See :func:`route_inbox_export`.
    """
    cfg = _load()
    if ctx.args.export:
        return route_inbox_export(ctx, cfg, Path(ctx.args.export))
    items = _inbox_items(cfg)
    plan = _plan(items, kind="inbox")
    option = _apply_gate(ctx, plan)
    if option != "apply":
        return ctx.envelope(data=_plan(items, kind="inbox", applied=False), outcome=Outcome.NO_OP)
    if not items:
        # AN EMPTY FOLDER IS NOT A WRITE. Nothing is opened, no session is taken
        # and the declaration is never derived, which is what makes this true on
        # the disk rather than approximately true.
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False, reason="inbox-empty"),
            outcome=Outcome.NO_OP,
        )
    result = apply_inbox(cfg, items)
    # THE GAPS RIDE AS A WARNING, NOT IN THE TOTALS. They are what this run did
    # not compare rather than a count of what it did, and the warning is the one
    # place every surface over this engine says so in the same words.
    not_compared = result.pop("not_compared", ())
    return ctx.envelope(
        data=_plan(items, kind="inbox", **result),
        outcome=Outcome.OK if result["applied"] else Outcome.NO_OP,
        warnings=(
            [{"code": "no-native-tree", "message": EXPORT_REMEDY}]
            if result["reason"] == "no-native-tree"
            else list(rebuild.not_compared_warnings(not_compared))
        ),
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

#: The warning the report carries when no tree has cut over, so the answer
#: names the medium that places tracks today rather than only saying it did
#: not compare.
UNPLACED_EXPORT_REMEDY = (
    "no tree has cut over, so this library is still filed through an export: "
    "export the collection from rekordbox and run route unplaced --export with "
    "that file, which places what the routing tree does not hold"
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
    cfg: config.Config, export: Path
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
    declared = taxonomy.default_taxonomy()
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
        }
        for key in keys
    ]
    return content, decision.plan, items, warnings, decision.gaps


def apply_unplaced_export(
    cfg: config.Config,
    export: Path,
    content: bytes,
    plan: dict[tuple[str, str], list[str]],
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
    still be a file somebody is told to import.
    """
    declared = taxonomy.default_taxonomy()
    tree = rbxml.routing_tree(declared, tree_registry.read(cfg))
    buffer = bytearray(content)
    report = trees.apply_unplaced_changes(plan, buffer, tree=tree)
    if not report.inserted:
        return None, report
    destination = export.with_name(export.stem + PLACED_SUFFIX)
    config.atomic_write_bytes(bytes(buffer), destination)
    return destination, report


def _unplaced_pending(
    run_id: str, verb: str, destination: Path, inserted: int, created: int
) -> PendingHumanAction:
    made = f", and {created} sub-playlist(s) were created" if created else ""
    return PendingHumanAction(
        kind="rekordbox_import",
        id=new_pending_id(run_id),
        summary=(
            f"{inserted} unplaced track(s) were placed{made} in {destination.name}, "
            f"which rekordbox has not imported yet"
        ),
        # THIS VERB IS ITS OWN CHECK, as the inbox sweep is: over a fresh export
        # taken after the import, a second run places nothing. Named by the
        # caller from its registry entry, because this layer may not spell a
        # verb (KTD23).
        verify_verb=verb,
        artifact=str(destination),
        steps=(
            f"import {destination} into rekordbox as a rekordbox xml library and "
            f"import the routing tree from it",
            "then export the collection again and run route unplaced --export "
            "with that file, which places nothing once the import has landed",
        ),
    )


def route_unplaced_export(ctx, cfg: config.Config, export: Path) -> Envelope:
    """Place every track a fresh export's routing tree does not hold, into a new file.

    NO GATE, and that is the brief's decision (U91). The export and the
    database are never written; the file lands beside the export and reaches
    rekordbox only when a person imports it, which is the review. The report
    without ``--export`` is unchanged.
    """
    declared = taxonomy.default_taxonomy()
    _refuse_off_the_bridge(
        cfg, declared, export, instead="run route unplaced without --export, which "
        "reports what the database's tree does not hold",
    )
    content, plan, items, warnings, gaps = plan_unplaced_export(cfg, export)
    destination, report = apply_unplaced_export(cfg, export, content, plan)
    warnings = [
        *warnings,
        *({"code": "route-write-skipped", "message": text} for text in report.warnings),
    ]
    # "NOTHING TO ROUTE" ONLY WHEN NOTHING WAS LEFT BEHIND, the inbox sweep's
    # rule and for its reason: it is the answer the pending action reads as
    # proof the import landed.
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
    return ctx.envelope(
        data=data,
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=_unplaced_pending(
            ctx.run.run_id,
            ctx.entry.name,
            destination,
            report.inserted,
            len(report.created),
        ),
        warnings=warnings,
    )


def route_unplaced(ctx) -> Envelope:
    """Report tracks no governed tree places, or place them through an export.

    WITHOUT ``--export`` IT IS READ ONLY (R-313). The open carries no write
    intent and no session is entered, so the report is safe with rekordbox
    open. On a library with nothing native it compares nothing and says which
    medium would place the tracks.

    WITH ``--export`` THE ACT IS BACK (U91), on the medium that needs no
    database write. See :func:`route_unplaced_export`.
    """
    cfg = _load()
    if ctx.args.export:
        return route_unplaced_export(ctx, cfg, Path(ctx.args.export))
    items, totals = unplaced_items(cfg)
    return ctx.envelope(
        data=_plan(items, kind="unplaced", **totals),
        outcome=Outcome.OK if totals["compared"] else Outcome.NO_OP,
        warnings=(
            [{"code": "no-native-tree", "message": UNPLACED_EXPORT_REMEDY}]
            if totals["reason"] == "no-native-tree"
            else []
        ),
    )


def _resume(ctx, store, job_id: str) -> Envelope:
    """Reconcile, refuse a foreign or itemless job, drive it, and report how it ended.

    RECONCILE FIRST, because a resume arrives after something stopped and a claim
    a dead driver left behind is state the queue cannot see for itself.

    THE JOB HAS TO BE A RESORT. ``handlers.run_job`` resolves the worker from the
    JOB ROW rather than from this verb, and this verb takes no other required
    input, so without this line any queued job of any verb could be driven
    through it, under this envelope and without that verb's own resume checks.

    THE ZERO ITEM RULE ON THE RESUME SIDE. A resort queued by any build before
    U53 carries no items, and ``jobs.drive`` walks an itemless job in one empty
    pass and records it SUCCEEDED, which is the defect this unit closed arriving
    through the one door that predates the fix.

    A JOB THAT ENDED BADLY IS NOT AN OK EXIT, which is R-225. ``drive`` raises
    only when EVERY attempted item failed, and this verb queues one item per
    governed tree, so a partial failure is the ordinary shape here rather than
    the edge one: without this an exit of 0 covers a sweep that finished half a
    library. It sits outside the ``is_open`` branch so a job already failed on
    entry is caught too.
    """
    job = jobs.reconcile(store, job_id)
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not a "
            f"resort, so this verb will not drive it",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("resume this job through the verb that queued it, or through the "
                   "job resume verb, which reads the worker off the job itself",),
            origin=("routing_cli",),
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no tree to re-place, so driving it would "
                f"report a resort that swept a library nothing read. It was queued "
                f"by a build that did not record its items",
                remedy=Remedy.REPORT_DEFECT,
                steps=(
                    "cancel this job, then queue the resort again, which records "
                    "one item per governed tree",
                ),
                origin=("routing_cli",),
                detail={"job_id": job.job_id},
            )
        # THE CUT THE WORKER WILL READ, read the same way first (U89): the one
        # loader, at the path the frozen configuration names. The file itself
        # is read as it stands, not frozen with the job. A corrupt calibration
        # refuses here before any item is claimed.
        threshold = metadata_cli.load_vocal_threshold(jobs.frozen_config(job))
        try:
            _, warnings = ctx.run_job(store, job)
        finally:
            # DRAINED WHETHER OR NOT THE DRIVE RETURNED, so a job that raised
            # leaves nothing behind for a later one in this process to inherit.
            left_behind = _LEFT_BEHIND.pop(job.job_id, [])
        job = jobs.get(store, job.job_id)
        # THE SAME ENGINE AS THE REBUILD, SO THE SAME GAP (R-316). Only on the
        # branch that drove, because a job finished on entry was compared by an
        # earlier run and this one compared nothing at all. The leftovers sit
        # on the same branch for the same reason (R-312).
        warnings = (
            *warnings,
            *rebuild.not_compared_warnings(rebuild.governed_not_compared(threshold)),
            *rebuild.left_behind_warnings(left_behind),
        )
    jobs.raise_for_state(job)
    return ctx.envelope(data=_reported(store, job), warnings=warnings)


def route_resort(ctx) -> Envelope:
    """Queue a resort. Long work is a job, never an inline sweep.

    ONE TREE IS ONE ITEM, and until U53 this queued none. A job with nothing to
    claim is walked by the driver in a single empty pass and transitioned to
    succeeded, so the queue reported a resort that swept a library nothing read.

    A LIBRARY WITH NOTHING NATIVE FILES NO JOB AT ALL, and that is not a refusal:
    a library that has never flipped a tree has nothing to re-place, which is
    ordinary rather than wrong.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        items = _native_trees(tree_registry.read(cfg))
        if not items:
            return ctx.envelope(
                data=_no_op("no-native-tree", native=0),
                outcome=Outcome.NO_OP,
            )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={},
            item_ids=items,
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


def handle_resort(job, item, cfg) -> None:
    """Re-place one governed tree from the declaration. The ``route.resort`` worker.

    IT IS THE REBUILD ENGINE, and calling it anything else would be this file
    claiming a second router. A genre or an energy change moves where the
    declaration puts a track, and re-deriving the declaration and writing back
    what the database lacks is exactly what that costs on the additive side.

    WHAT IT DOES NOT DO IS TAKE THE TRACK OUT OF WHERE IT WAS. The membership
    writer is additive by construction, so after a genre change the track is in
    its new sub AND still in its old one until somebody removes it. This build
    has no database removal path to offer, so the verb's summary says additive
    and the resume NAMES what was left, which is R-312.

    THE ENGINE'S OWN MEASUREMENT IS WHAT GETS NAMED. ``after.unexpected`` is the
    check the engine ran on the handle it had just written through, so keeping
    it costs no second walk of the library and cannot refuse after a job that
    succeeded. It is kept in :data:`_LEFT_BEHIND` rather than returned, because
    a worker's return is the artifact channel and nothing else.

    ``cfg`` is the configuration this job was FROZEN against (KTD9). Nothing here
    loads one.
    """
    del job
    report = rebuild.rebuild_governed_tree(
        cfg,
        tree_id=str(item.item_id),
        workflow=RESORT_WORKFLOW,
        # THE CALIBRATED CUT, through the one loader, at the path the frozen
        # configuration names. None on a library never calibrated (U89, D7).
        vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
    )
    _LEFT_BEHIND.setdefault(item.job_id, []).extend(report.after.unexpected)
    return None


def route_pending(ctx) -> Envelope:
    """Place tracks whose routing was decided before the library held a row.

    On a library with no outstanding intents this is a no-op: nothing is
    opened and no session is closed. On a library with no database native
    tree it is a no-op too, and says so. When a named session's outstanding
    set becomes empty, the run closes through :func:`_close_run`.
    """
    cfg = _load()
    ledger = routing_pass.read(cfg)
    wanted = ctx.args.session
    session_ids = (
        (wanted,)
        if wanted
        else tuple(sorted({entry.session_id for entry in ledger.outstanding()}))
    )
    if not session_ids:
        return ctx.envelope(data=_plan([], kind="pending"), outcome=Outcome.NO_OP)

    items = [{"session_id": session_id} for session_id in session_ids]
    entries = tree_registry.read(cfg)
    native = [
        tree_id for tree_id in entries.tree_ids() if entries.is_database_native(tree_id)
    ]
    if not native:
        # NOTHING WAS READ, SO NOTHING IS CLAIMED (R-436, R-501). This answered
        # OK over runs it had not opened, and a landing named it as the proof
        # of an import. With no native tree there is nowhere to place a track,
        # so it is a no-op that says why and names what does work today.
        return ctx.envelope(
            data=_plan(items, kind="pending"),
            outcome=Outcome.NO_OP,
            warnings=[{"code": "no-native-tree", "message": PENDING_REMEDY}],
        )

    declared = taxonomy.default_taxonomy()
    handle = rb_writer.open_db(cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        for session_id in session_ids:
            if not routing_pass.read(cfg).outstanding(session_id):
                _close_if_settled(cfg, session_id)
                continue
            routing_pass.route(
                cfg,
                handle,
                session_id=session_id,
                registry=entries,
                declared=declared,
                rows=rows,
                root_exists=lambda root_id: root_id in known,
                analysis_roots=analysis_store.watch_roots(cfg),
            )
            if not routing_pass.read(cfg).outstanding(session_id):
                _close_if_settled(cfg, session_id)
    finally:
        rb_writer.close_db(handle)
    return ctx.envelope(data=_plan(items, kind="pending"), outcome=Outcome.OK)
