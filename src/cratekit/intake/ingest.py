"""Place new files into a Fresh Export and record routing intents.

New-track intake still arrives as an XML import. This module reads tags,
builds TRACK elements, splices them into a named Fresh Export, and records
each placement through ``routing_pass.record_intents`` at the moment the
destination is decided. U19's deferred-routing mechanism hangs off that
call. Closing a run that still holds a deferred track goes through
``routing_pass.close_run``, never ``session.close_session``.

Inbox stays on the XML bridge. This module does not flip a tree.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

from cratekit.cli import output
from cratekit.core import (
    config,
    locations,
    naming,
    routing,
    session,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import refuse
from cratekit.core.naming import AUDIO_EXTS, MarkerRule, NameSpec, NameTemplate
from cratekit.intake import collection_xml
from cratekit.write import rbxml, routing_pass
from cratekit.write.routing_pass import RoutingIntent

INTAKE_WORKFLOW = "intake"

#: The verb that proves an intake file imported, and the one a person runs to
#: say so. SPELLED ONCE, HERE, beside the session it is persisted on, because
#: both callers of :func:`place_files` owe the same action and two spellings is
#: how one of them goes stale. It was ``route.pending``, which before a cutover
#: answers without reading anything (R-436).
VERIFY_VERB = "intake.imported"


def import_steps(destination: Path) -> tuple[str, ...]:
    """What a person does with an intake file, end to end, in order.

    END TO END IS THE REQUIREMENT. The steps used to stop at the import, and a
    person who followed every one of them was left with a session and a file
    that each refused the cutover precheck (R-501).
    """
    return (
        f"import {destination} into rekordbox as a rekordbox xml library",
        "take a Fresh Export of the collection from rekordbox",
        "run crate intake imported --export with that Fresh Export, which "
        "proves the import, retires the intake file and settles this run",
    )


@dataclass(frozen=True, slots=True)
class PlacedTrack:
    """One file that became a COLLECTION row and a routing intent."""

    path: Path
    track_id: int
    location: str
    tree: str
    bucket: str
    sub: str
    xml: str
    #: The intake session this placement was recorded under, which is where its
    #: pending action is persisted. Every track of one call carries the same one.
    session_id: str = ""


def _template_for(cfg: config.Config) -> NameTemplate:
    return NameTemplate(
        markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),)
    )


def assert_not_staging(path: Path, cfg: config.Config) -> None:
    """Refuse files still under download staging (the 2026-06-29 flood)."""
    staging = Path(cfg.paths.download_staging).resolve()
    resolved = path.resolve()
    if resolved == staging or staging in resolved.parents:
        raise refuse(
            "intake-staging-refused",
            f"{path} is still under download staging at {staging}, so a "
            f"Location stamped from it would die the moment staging is "
            f"cleaned",
            origin=("intake.ingest",),
            detail={"path": str(path), "staging": str(staging)},
        )


def read_meta(path: Path, *, cfg: config.Config, lossy: bool = False) -> dict:
    """COLLECTION metadata from a file already on disk. No network."""
    assert_not_staging(path, cfg)
    stat = path.stat()
    artist = tags.read_tag(path, "artist") or ""
    title = tags.read_tag(path, "title") or path.stem
    genre = tags.read_genre_from_file(path) or ""
    key = tags.read_tag(path, "initialkey")
    energy = tags.read_energy_from_file(path)
    template = _template_for(cfg)
    body = naming.strip_head(title, template=template)
    spec = NameSpec(
        stem=body,
        suffix=path.suffix,
        key=key,
        lossy=lossy,
        title=body,
    )
    rendered = naming.render_all(spec, template=template)
    return {
        "name": rendered.library_name,
        "artist": artist,
        "album": "",
        "genre": genre,
        "size_bytes": stat.st_size,
        "duration_s": 0,
        "bitrate_kbps": 0,
        "sample_rate": 0,
        "location": locations.location_url(path.resolve()),
        "tonality": key or "",
        "energy": energy,
        "inizio": tags.read_tag(path, "inizio"),
        "lossy": lossy,
    }


def decide_placement(meta: dict) -> tuple[str, str, str] | None:
    """(tree, bucket, sub) ids, or None when the taxonomy declares no sub."""
    declared = taxonomy.default_taxonomy()
    resolved = routing.resolve_bucket(declared, meta.get("genre"))
    sub = routing.energy_sub(
        declared,
        resolved.bucket_id,
        meta.get("energy"),
        source_genre=str(meta.get("genre") or ""),
    )
    if sub is None:
        return None
    return declared.tree.id, resolved.bucket_id, sub.id


def place_files(
    paths: list[Path],
    *,
    cfg: config.Config,
    export: Path,
    destination: Path,
    session_id: str | None = None,
    date_added: str | None = None,
    lossy: bool = False,
) -> list[PlacedTrack]:
    """Splice each file into ``destination`` and record routing intents.

    The Fresh Export is a path the caller names. This function does not hunt
    for one: a hunt that picked the newest XML would pick a pending intake
    file, including a U22 stub listing.
    """
    if not export.is_file():
        raise refuse(
            "library-export-unusable",
            f"no Fresh Export at {export}",
            steps=(
                "export the collection again from rekordbox and pass that file",
            ),
            origin=("intake.ingest",),
        )
    for path in paths:
        assert_not_staging(path, cfg)
        if path.suffix.lower() not in AUDIO_EXTS:
            raise refuse(
                "intake-list-unusable",
                f"{path.name} is not an audio file this pipeline ingests",
                origin=("intake.ingest",),
            )

    content = bytearray(export.read_bytes())
    if collection_xml.is_stub_listing(bytes(content)):
        raise refuse(
            "intake-export-is-stub",
            "this file is a U22 stub listing, not a Fresh Export, so it is "
            "not an importable splice and new tracks cannot be added to it",
            steps=(
                "take a Fresh Export from rekordbox",
                "do not treat a U22 stub listing as an importable splice",
            ),
            origin=("intake.ingest",),
        )

    added = date_added or date.today().isoformat()
    next_id = collection_xml.next_track_id(bytes(content))
    placed: list[PlacedTrack] = []
    xml_rows: list[str] = []
    declared = taxonomy.default_taxonomy()
    for offset, path in enumerate(paths):
        meta = read_meta(path, cfg=cfg, lossy=lossy)
        placement = decide_placement(meta)
        if placement is None:
            raise refuse(
                "intake-list-unusable",
                f"{path.name} resolved to a bucket with no declared sub, so "
                f"there is nowhere to record a routing intent for it",
                origin=("intake.ingest",),
            )
        tree_id, bucket_id, sub_id = placement
        tid = next_id + offset
        xml = collection_xml.build_track_xml(tid, meta, added)
        xml_rows.append(xml)
        placed.append(
            PlacedTrack(
                path=path,
                track_id=tid,
                location=str(meta["location"]),
                tree=tree_id,
                bucket=bucket_id,
                sub=sub_id,
                xml=xml,
            )
        )

    collection_xml.splice_tracks(content, xml_rows)
    tree = rbxml.intake_tree(declared, tree_registry.read(cfg))
    playlist_error = rbxml.insert_intake_playlist(
        content,
        destination.stem,
        [item.track_id for item in placed],
        tree=tree,
    )
    if playlist_error:
        raise refuse(
            "library-export-unusable",
            f"the intake playlist could not be written ({playlist_error})",
            steps=(
                "export the collection again from rekordbox so the intake "
                "folder is present, then retry",
            ),
            origin=("intake.ingest",),
        )
    # OPENED AFTER THE LAST REFUSAL THAT NEEDS NO SESSION, so a file with a
    # bad tag or an export with no intake folder leaves no record at all. It
    # cannot move below the write, because the intents carry its identifier.
    record = session.open_session(
        cfg,
        workflow=INTAKE_WORKFLOW,
        session_id=session_id,
    )
    placed = [replace(item, session_id=record.session_id) for item in placed]
    wrote = False
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(bytes(content))
        wrote = True

        # Recorded at the moment the placement is decided, not at the end of a
        # later verb. U19's ledger is the only subject the deferred-routing
        # suite has.
        routing_pass.record_intents(
            cfg,
            [
                RoutingIntent(
                    track=routing_pass.track_id(item.location),
                    session_id=record.session_id,
                    location=item.location,
                    tree=item.tree,
                    bucket=item.bucket,
                    sub=item.sub,
                    decided=output.timestamp(),
                )
                for item in placed
            ],
        )
        session.mark_awaiting_import(
            record,
            session.pending_import(
                record,
                artifact=destination,
                summary=(
                    f"{len(placed)} file(s) are named in {destination.name}, "
                    f"which rekordbox has not imported yet"
                ),
                verify_verb=VERIFY_VERB,
                steps=import_steps(destination),
            ),
            cfg,
        )
    except BaseException:
        # THE CALL REFUSED, SO THE RUN IS GIVEN UP, AND THE RECORD SAYS SO.
        # Abandoning is the ungated close, which is what makes it reachable
        # from here whatever state the ledger is in. The file goes too when
        # this call wrote it: an intake file with no run behind it refuses the
        # cutover precheck and no verb retires it. Both are attempts. The
        # refusal being raised is the one the caller has to see, and a second
        # failure while cleaning up must not replace it.
        if wrote:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
        with contextlib.suppress(Exception):
            routing_pass.close_run(record, cfg, state=session.SessionState.ABANDONED)
        raise
    return placed
