"""Place new files into a Fresh Export and record routing intents.

New-track intake still arrives as an XML import. This module reads tags,
builds TRACK elements, splices them into a named Fresh Export, and records
each placement through ``routing_pass.record_intents`` at the moment the
destination is decided. U19's deferred-routing mechanism hangs off that
call. Closing a run that still holds a deferred track goes through
``routing_pass.close_run``, never ``session.close_session``.

THE INTAKE TREE HAS TWO MEDIA AND THIS MODULE WRITES ONE (R-746, R-770). On
the xml bridge a file is spliced into an export, here. On a library whose
intake tree has cut over a file becomes a content row through
:mod:`cratekit.intake.native`, and nothing here may splice for it.
:func:`intake_medium` is the one switch every intake verb reads, and
:func:`assert_intake_on_the_bridge` is what a splice asks before its first
byte, so a caller that did not read the switch is refused in this writer's
words and never as a defect. This module does not flip a tree.
"""

from __future__ import annotations

import contextlib
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

from cratekit.cli import output
from cratekit.core import (
    active_taxonomy,
    config,
    locations,
    naming,
    routing,
    session,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Remedy, refuse
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


@dataclass(frozen=True, slots=True)
class IntakeMedium:
    """What was read to choose the intake tree's medium, and the choice.

    ``declared`` and ``registry`` are both None when the library root is not
    there. The registry lives under the root, so an unreachable root decides
    nothing: the bridge path is taken as it was before the second medium
    existed, and its own checks name the library.
    """

    declared: taxonomy.Taxonomy | None
    registry: tree_registry.Registry | None

    @property
    def native(self) -> bool:
        """Whether the intake tree is recorded database native."""
        if self.declared is None or self.registry is None:
            return False
        return self.registry.is_database_native(self.declared.intake.id)


def intake_medium(cfg: config.Config) -> IntakeMedium:
    """THE ONE SWITCH (R-770). Every verb that writes the intake tree reads it.

    The intake tree's recorded mode chooses, the way the routing verbs choose
    theirs: native takes a file into the collection through the guarded
    writer, the bridge splices it into an export. One function, so two verbs
    cannot come to read two rules. ``intake file`` hands what this read to its
    splice, so its check and its write are one read. The bridge landing's
    engine reads both again before its first move, by its own contract
    (R-677), and :func:`assert_intake_on_the_bridge` is what refuses there if
    a cutover was recorded in between.
    """
    if not Path(cfg.library.root).is_dir():
        return IntakeMedium(declared=None, registry=None)
    return IntakeMedium(declared=active_taxonomy.load(cfg), registry=tree_registry.read(cfg))


def assert_intake_on_the_bridge(
    declared: taxonomy.Taxonomy, registry: tree_registry.Registry
) -> None:
    """Refuse a splice for an intake tree the database owns, in this writer's words.

    THE CHECKING PATH, AHEAD OF THE EMITTER GUARD (R-770). The emitter refuses
    the same tree with ``report-defect``, which is true of a writer that arrived
    at the wrong medium by mistake and false of a person who cut the intake tree
    over and then ran a verb that splices. A cutover is a choice, so the refusal
    names the verbs that take the other medium and asks for no bug report.
    """
    if not IntakeMedium(declared=declared, registry=registry).native:
        return
    tree_id = declared.intake.id
    raise refuse(
        "tree-unconverged",
        f"the intake tree {tree_id!r} is database native since its recorded "
        f"cutover, so no intake file is written for it and nothing was spliced "
        f"into an export; crate intake land adds a staged folder to the "
        f"collection through the database, and crate intake file adds one file",
        remedy=Remedy.FIX_COMMAND_LINE,
        steps=(
            "run crate intake land without --export to add a staged folder to "
            "the collection",
            "or run crate intake file without --export for one file already in "
            "the library",
        ),
        origin=("intake.ingest",),
        detail={"tree_id": tree_id, "mode": str(registry.mode(tree_id))},
    )


def bridge_intake_tree(
    declared: taxonomy.Taxonomy, registry: tree_registry.Registry
) -> rbxml.Tree:
    """The intake tree a splice is handed, refused first when the database owns it.

    THE ONE PLACE IN ``src`` THAT BUILDS IT. The write layer names no verb, so
    the refusal that names the landing cannot live beside the emitter guard; it
    lives here, one layer up, in the function every splicer has to go through to
    get a tree to pass the emitter at all. A third splicer therefore meets this
    refusal and not the guard's, without anybody remembering to ask.
    """
    assert_intake_on_the_bridge(declared, registry)
    return rbxml.intake_tree(declared, registry)


def import_steps(destination: Path, intake: str) -> tuple[str, ...]:
    """What a person does with an intake file, end to end, in order.

    END TO END IS THE REQUIREMENT. The steps used to stop at the import, and a
    person who followed every one of them was left with a session and a file
    that each refused the cutover precheck (R-501).

    THE BATCH PLAYLIST LANDS AT THE PLAYLIST ROOT, whatever folder the file puts
    it in, and a routing pass reads only the intake folder, so the drag is a
    step (R-687). The folder itself is never imported: an existing folder
    imported from the file keeps every child it had and appends the file's
    copies, doubling each batch already in it.
    """
    return (
        f"import {destination} into rekordbox as a rekordbox xml library",
        f"import the {destination.stem} playlist from it on its own, never the "
        f"{intake} folder, which would add a second copy of every batch already "
        f"in it",
        f"the {destination.stem} playlist lands at the playlist root, so drag it "
        f"into the {intake} folder, where a routing pass reads its batches",
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
    """COLLECTION metadata from a file already on disk. No network.

    THE NAME CARRIES THE HEAD THE FILE CARRIES (R-740). The head is read from
    the title tag, and from the filename stem when the title has none, as text
    through the head parser and never from a tempo tag, since none is written.
    Its key wins over the key tag so the Name equals the title tag rekordbox
    would read on Reload Tags; the key tag only fills a head that has none. A
    file headed nowhere lands with the bare title, as it always did, because
    nothing here may invent a tempo. ``tonality`` stays the key tag's value.
    A lossy marker inside that head marks the track, and ``lossy`` reports the
    flag the Name was rendered from; a marker in the body is text, and marks
    nothing, so the Name never gains a second marker the title tag lacks.
    """
    assert_not_staging(path, cfg)
    return file_meta(path, cfg=cfg, lossy=lossy)


def file_meta(path: Path, *, cfg: config.Config, lossy: bool = False) -> dict:
    """:func:`read_meta` without the staging refusal, for a file about to move.

    The native landing (R-746) plans a row's Title while the file is still in
    download staging and stamps it on the row once the file is in the library.
    The name is a function of the tags and the stem, which the move does not
    change, so reading it here is reading the same answer early. Every other
    caller wants the refusal and goes through :func:`read_meta`.
    """
    stat = path.stat()
    artist = tags.read_tag(path, "artist") or ""
    title = tags.read_tag(path, "title") or path.stem
    genre = tags.read_genre_from_file(path) or ""
    key = tags.read_tag(path, "initialkey")
    energy = tags.read_energy_from_file(path)
    template = _template_for(cfg)
    head = (
        naming.parse_head(title, template=template)
        or naming.parse_head(path.stem, template=template)
        or {}
    )
    spec = naming.normalize_spec(
        NameSpec(
            stem=path.stem,
            suffix=path.suffix,
            key=head.get("key") or key,
            lossy=lossy,
            title=title,
        ),
        template=template,
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
        "lossy": spec.lossy,
    }


def decide_placement(
    meta: dict, declared: taxonomy.Taxonomy
) -> tuple[str, str, str] | None:
    """(tree, bucket, sub) ids, or None when the taxonomy declares no sub.

    ``declared`` is the library's active taxonomy (R-685), read once by the
    caller rather than once per file.
    """
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


def persisted_pending(
    cfg: config.Config, placed: Sequence[PlacedTrack]
) -> output.PendingHumanAction:
    """The pending action :func:`place_files` persisted on its intake session.

    READ BACK RATHER THAN BUILT AGAIN, so an envelope cannot say one thing while
    the session log holds another. A call that returned with no such record is
    a defect here, and it is reported as one: the intake file is written by now,
    and an envelope claiming an action nothing holds would be the tool saying
    something and forgetting it.
    """
    session_id = placed[0].session_id if placed else ""
    record = session.read_record(session_id, cfg) if session_id else None
    if record is None or record.pending is None:
        raise refuse(
            "internal-error",
            f"the intake file was written and its intake session {session_id!r} "
            f"holds no pending import, so nothing durable says the file is waiting",
            origin=("intake.ingest",),
            detail={"session_id": session_id},
        )
    return record.pending


def place_files(
    paths: list[Path],
    *,
    cfg: config.Config,
    export: Path,
    destination: Path,
    session_id: str | None = None,
    date_added: str | None = None,
    lossy: bool = False,
    declared: taxonomy.Taxonomy | None = None,
    registry: tree_registry.Registry | None = None,
) -> list[PlacedTrack]:
    """Splice each file into ``destination`` and record routing intents.

    The Fresh Export is a path the caller names. This function does not hunt
    for one: a hunt that picked the newest XML would pick a pending intake
    file, including a U22 stub listing.

    ``declared`` is the library's active taxonomy and ``registry`` the tree
    registry, when the caller already read them to check what this writes, so
    the check and the write agree; with none each is read here, the taxonomy
    from the library and never from the shipped template.

    A NATIVE INTAKE TREE IS REFUSED FIRST (R-770), before the export is looked
    for, because on that medium there is no export to find and "export the
    collection again" would be the wrong thing to tell anybody. So the taxonomy
    and the registry are read ahead of every other check here, and one that
    cannot be read refuses with its own cause before a missing export does.
    """
    if declared is None or registry is None:
        medium = intake_medium(cfg)
        declared = declared if declared is not None else medium.declared
        registry = registry if registry is not None else medium.registry
    if declared is not None and registry is not None:
        assert_intake_on_the_bridge(declared, registry)
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
    if declared is None:
        declared = active_taxonomy.load(cfg)
    for offset, path in enumerate(paths):
        meta = read_meta(path, cfg=cfg, lossy=lossy)
        placement = decide_placement(meta, declared)
        if placement is None:
            raise refuse(
                "intake-list-unusable",
                f"{path.name} resolved to a bucket with no declared sub, so "
                f"there is nowhere to record a routing intent for it",
                origin=("intake.ingest",),
            )
        tree_id, bucket_id, sub_id = placement
        tid = next_id + offset
        xml = collection_xml.build_track_xml(tid, meta, added, declared=declared)
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
    if registry is None:
        registry = tree_registry.read(cfg)
    tree = bridge_intake_tree(declared, registry)
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
    # WHAT THE ROLLBACK MAY REMOVE IS DECIDED BEFORE THE WRITE. The write is a
    # plain overwrite, and a file already here is an earlier run's intake file
    # that run's steps still name, so a failure below must not take it away.
    fresh = not destination.exists()
    wrote = False
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(bytes(content))
        wrote = True
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
                steps=import_steps(destination, declared.intake.display),
            ),
            cfg,
        )

        # Recorded at the moment the placement is decided, not at the end of a
        # later verb. U19's ledger is the only subject the deferred-routing
        # suite has. LAST, AND NOTHING FOLLOWS IT: the ledger has no way to
        # withdraw an intent, so a step that could fail after this one would
        # leave an abandoned run's tracks outstanding for ever.
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
    except BaseException:
        # THE CALL REFUSED, SO THE RUN IS GIVEN UP, AND THE RECORD SAYS SO.
        # Abandoning is the ungated close, which is what makes it reachable
        # from here whatever state the run or the ledger is in. The file goes
        # too when this call made it: an intake file with no run behind it
        # refuses the cutover precheck and no verb retires it. Both are
        # attempts. The refusal being raised is the one the caller has to see,
        # and a second failure while cleaning up must not replace it.
        if wrote and fresh:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
        with contextlib.suppress(Exception):
            routing_pass.close_run(record, cfg, state=session.SessionState.ABANDONED)
        raise
    return placed
