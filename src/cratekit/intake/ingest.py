"""Place new files into a Fresh Export and record routing intents.

Reads tags, builds TRACK elements, splices them into a named Fresh Export, and
records each placement through ``routing_pass.record_intents`` as its
destination is decided (U19's deferred routing). A run that still holds a
deferred track closes through ``routing_pass.close_run``, never
``session.close_session``.

TWO MEDIA, AND THIS MODULE WRITES ONE (R-746, R-770). :func:`intake_medium` is
the switch every intake verb reads; a native intake tree takes a file through
:mod:`cratekit.intake.native`, and :func:`assert_intake_on_the_bridge` refuses
a splice for it in this writer's words, never as a defect.
"""

from __future__ import annotations

import contextlib
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import date
from functools import partial
from pathlib import Path

from cratekit.cli import output
from cratekit.core import (
    active_taxonomy,
    cause,
    config,
    locations,
    naming,
    routing,
    session,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Remedy
from cratekit.core.naming import AUDIO_EXTS, NameSpec, NameTemplate
from cratekit.intake import collection_xml
from cratekit.write import rbxml, routing_pass
from cratekit.write.routing_pass import RoutingIntent

INTAKE_WORKFLOW = "intake"

#: Every refusal here carries this module's origin.
refuse = partial(cause.refuse, origin=("intake.ingest",))

#: The verb that proves an intake file imported, spelled once for both callers
#: of :func:`place_files` (R-436).
VERIFY_VERB = "intake.imported"

#: The session record field listing the INBOX playlists a landing wrote for the
#: account playlists (U113), so ``inbox rotate`` ages each from the day it
#: landed. A native entry has ``id`` and ``name``; an intake file's has ``name``
#: and ``batch``, since its playlist has no id until imported.
INBOX_PLAYLISTS_KEY = "inbox_playlists"
#: The account and pass keys both media write on each entry (U128), how a
#: rerun of a pass finds what it mirrored.
INBOX_ACCOUNT_KEY = "account"
INBOX_PASS_KEY = "pass"


@dataclass(frozen=True, slots=True)
class InboxPlaylist:
    """One account playlist an intake file writes (U113, U128).

    ``members`` in the account's order: a :class:`Path` is a file this call
    places, a string the export's TrackID of a track the library held.
    """

    name: str
    members: tuple[Path | str, ...]
    account: str = ""
    pass_name: str = ""

    def track_ids(self, ids_by_path: dict[Path, int]) -> list[int | str]:
        """The TrackIDs it holds, each once, a file this call did not place left out."""
        held: list[int | str] = []
        for member in self.members:
            if isinstance(member, Path):
                if member in ids_by_path:
                    held.append(ids_by_path[member])
            else:
                held.append(member)
        return list(dict.fromkeys(held))


@dataclass(frozen=True, slots=True)
class IntakeMedium:
    """What was read to choose the intake tree's medium, and the choice.

    Both None when the library root is not there: the registry lives under it,
    so the bridge path is taken and its own checks name the library.
    """

    declared: taxonomy.Taxonomy | None
    registry: tree_registry.Registry | None

    @property
    def native(self) -> bool:
        """Whether the intake tree is recorded database native."""
        if self.declared is None or self.registry is None:
            return False
        return self.registry.is_database_native(self.declared.intake.id)

    @property
    def files_natively(self) -> bool:
        """Whether the routing tree a landing files into is recorded database native (U165)."""
        if self.declared is None or self.registry is None:
            return False
        return self.registry.is_database_native(self.declared.tree.id)


def intake_medium(cfg: config.Config) -> IntakeMedium:
    """THE ONE SWITCH (R-770). Every verb that writes the intake tree reads it.

    The intake tree's recorded mode chooses: native writes through the guarded
    writer, the bridge splices into an export. One function, so two verbs
    cannot read two rules.
    """
    if not Path(cfg.library.root).is_dir():
        return IntakeMedium(declared=None, registry=None)
    return IntakeMedium(declared=active_taxonomy.load(cfg), registry=tree_registry.read(cfg))


def assert_intake_on_the_bridge(
    declared: taxonomy.Taxonomy, registry: tree_registry.Registry
) -> None:
    """Refuse a splice for an intake tree the database owns, in this writer's words.

    Ahead of the emitter guard, whose ``report-defect`` is false of a person
    who chose a cutover (R-770), so this names the verbs that take the medium.
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
            "run crate intake land without --export to add a staged folder to the collection",
            "or run crate intake file without --export for one file already in the library",
        ),
        detail={"tree_id": tree_id, "mode": str(registry.mode(tree_id))},
    )


def bridge_intake_tree(
    declared: taxonomy.Taxonomy, registry: tree_registry.Registry
) -> rbxml.Tree:
    """The intake tree a splice is handed, refused first when the database owns it.

    THE ONE PLACE IN ``src`` THAT BUILDS IT, so every splicer meets this
    refusal, which names verbs the write layer cannot, before the guard's.
    """
    assert_intake_on_the_bridge(declared, registry)
    return rbxml.intake_tree(declared, registry)


def spoken(names: Sequence[str]) -> str:
    """Several names as a person says the list, ``A, B and C``."""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


def import_steps(
    destination: Path, intake: str, playlist: str | None = None, *, playlists: Sequence[str] = ()
) -> tuple[str, ...]:
    """What a person does with an intake file, end to end, in order (R-501).

    ``playlist`` is the batch playlist, the stem when none is named; several
    ``playlists`` (U113) are each imported and dragged on their own. A playlist
    lands at the playlist root and a routing pass reads only the intake folder,
    so the drag is a step (R-687); the folder itself is never imported, since
    an import appends copies of every batch already in it.
    """
    if len(playlists) > 1:
        said = spoken(playlists)
        which, lands = f"each of the {said} playlists", f"the {said} playlists land"
        drag = "drag each one"
    else:
        named = (
            playlists[0] if playlists else playlist if playlist is not None else destination.stem
        )
        which, lands, drag = f"the {named} playlist", f"the {named} playlist lands", "drag it"
    return (
        f"import {destination} into rekordbox as a rekordbox xml library",
        f"import {which} from it on its own, never the "
        f"{intake} folder, which would add a second copy of every batch already "
        f"in it",
        f"{lands} at the playlist root, so {drag} "
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
    #: The intake session this placement was recorded under, holding its pending action.
    session_id: str = ""


def _template_for(cfg: config.Config) -> NameTemplate:
    return NameTemplate.lossy(cfg.naming.lossy_marker)


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
            detail={"path": str(path), "staging": str(staging)},
        )


def read_meta(path: Path, *, cfg: config.Config, lossy: bool = False) -> dict:
    """COLLECTION metadata from a file already on disk. No network.

    THE NAME CARRIES THE HEAD THE FILE CARRIES (R-740), parsed from the title
    tag or else the stem, never a tempo tag. Its key wins over the key tag, so
    the Name equals what rekordbox reads on Reload Tags; ``tonality`` stays the
    key tag's. A lossy marker in the head marks the track; one in the body is
    text, so the Name never gains a marker the title tag lacks.
    """
    assert_not_staging(path, cfg)
    return file_meta(path, cfg=cfg, lossy=lossy)


def file_meta(path: Path, *, cfg: config.Config, lossy: bool = False) -> dict:
    """:func:`read_meta` without the staging refusal, for a file about to move.

    The native landing (R-746) plans a row's Title while the file is staged;
    the move changes neither tags nor stem, so the answer is the same.
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


def decide_placement(meta: dict, declared: taxonomy.Taxonomy) -> tuple[str, str, str] | None:
    """(tree, bucket, sub) ids, or None when the active taxonomy (R-685) declares no sub."""
    resolved = routing.resolve_bucket(declared, meta.get("genre"))
    sub = routing.energy_sub(
        declared, resolved.bucket_id, meta.get("energy"), source_genre=str(meta.get("genre") or "")
    )
    if sub is None:
        return None
    return declared.tree.id, resolved.bucket_id, sub.id


def persisted_pending(
    cfg: config.Config, placed: Sequence[PlacedTrack]
) -> output.PendingHumanAction:
    """The pending action :func:`place_files` persisted on its intake session.

    READ BACK RATHER THAN BUILT AGAIN, so the envelope cannot differ from the
    session log; no record by now is a defect.
    """
    session_id = placed[0].session_id if placed else ""
    record = session.read_record(session_id, cfg) if session_id else None
    if record is None or record.pending is None:
        raise refuse(
            "internal-error",
            f"the intake file was written and its intake session {session_id!r} "
            f"holds no pending import, so nothing durable says the file is waiting",
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
    playlist: str | None = None,
    split: Sequence[InboxPlaylist] = (),
) -> list[PlacedTrack]:
    """Splice each file into ``destination`` and record routing intents.

    ``playlist`` names the batch playlist, the stem when none (U110). ``split``
    is the account playlists (U113, U128), each its own playlist; the batch
    playlist keeps the rest and an empty playlist is not written. Each written
    is listed under :data:`INBOX_PLAYLISTS_KEY`. The Fresh Export is named by
    the caller, never hunted, since the newest XML may be a pending intake
    file. ``declared`` and ``registry`` are the caller's read, so its check and
    this write agree; with none each is read from the library.

    A NATIVE INTAKE TREE IS REFUSED FIRST (R-770), before the export is looked
    for, since "export the collection again" would be wrong on that medium.
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
            steps=("export the collection again from rekordbox and pass that file",),
        )
    for path in paths:
        assert_not_staging(path, cfg)
        if path.suffix.lower() not in AUDIO_EXTS:
            raise refuse(
                "intake-list-unusable", f"{path.name} is not an audio file this pipeline ingests"
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
    named = playlist if playlist is not None else destination.stem
    ids_by_path = {item.path: item.track_id for item in placed}
    claimed: set[Path] = set()
    accounts: list[tuple[InboxPlaylist, list[int | str]]] = []
    for one in split:
        claimed.update(member for member in one.members if isinstance(member, Path))
        held = one.track_ids(ids_by_path)
        if held:
            accounts.append((one, held))
    rest = [item.track_id for item in placed if item.path not in claimed]
    written = ([(named, rest)] if rest or not accounts else []) + [
        (one.name, held) for one, held in accounts
    ]
    for name, track_ids in written:
        playlist_error = rbxml.insert_intake_playlist(content, name, track_ids, tree=tree)
        if playlist_error:
            raise refuse(
                "library-export-unusable",
                f"the intake playlist could not be written ({playlist_error})",
                steps=(
                    "export the collection again from rekordbox so the intake "
                    "folder is present, then retry",
                ),
            )
    # OPENED AFTER THE LAST REFUSAL THAT NEEDS NO SESSION, so those leave no
    # record, and before the write, since the intents carry its identifier.
    record = session.open_session(cfg, workflow=INTAKE_WORKFLOW, session_id=session_id)
    placed = [replace(item, session_id=record.session_id) for item in placed]
    if accounts:
        # Persisted by the awaiting state's write below.
        record.detail[INBOX_PLAYLISTS_KEY] = [
            {
                "name": one.name,
                "batch": named,
                INBOX_ACCOUNT_KEY: one.account,
                INBOX_PASS_KEY: one.pass_name,
            }
            for one, _ids in accounts
        ]
    # DECIDED BEFORE THE WRITE: a file already here is an earlier run's intake
    # file its steps still name, so a rollback must not take it away.
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
                steps=import_steps(
                    destination,
                    declared.intake.display,
                    named,
                    playlists=[name for name, _ids in written] if accounts else (),
                ),
            ),
            cfg,
        )

        # LAST, AND NOTHING FOLLOWS IT: the ledger cannot withdraw an intent,
        # so a later failure would leave an abandoned run's tracks outstanding.
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
        # THE RUN IS GIVEN UP through the ungated close, reachable whatever its
        # state, and a file this call made goes too, since one with no run
        # behind it refuses the cutover precheck. Both are attempts, so the
        # refusal raised is the one the caller sees.
        if wrote and fresh:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
        with contextlib.suppress(Exception):
            routing_pass.close_run(record, cfg, state=session.SessionState.ABANDONED)
        raise
    return placed
