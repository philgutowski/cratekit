"""Land a folder of acquired files in the library and splice them into one file.

``ingest.place_files`` refuses any path under download staging, because a
Location stamped from staging dies when staging is cleaned. This engine moves
N staged files to ``library.root / music_dir / <batch>`` (on the native medium,
the folder :func:`cratekit.intake.shelve.landing_target` chose) and then writes
one intake file naming them. MOVE FIRST, THEN SPLICE: a splice before the
rename stamps the staging Location.

:func:`plan` lists and fingerprints the folder; :func:`apply` lists it again,
refuses a stale fingerprint, runs every check that can refuse the whole batch,
and only then moves. A move is ``os.replace`` on one filesystem: another device
is refused, since a copy is a second file a later clean deletes. An occupied
target is refused alone and never overwritten. A failure after the first move
leaves the moved files in the library, named by the refusal, and no failure
leaves an intake file behind.

The caller holds :func:`batch_lock` across :func:`apply` (R-432), because a
check followed by ``os.replace`` holds only while nothing else writes the batch
folder.

A manifest's label rows are tied to landed files by :func:`match.resolve_one`
over the batch folder only, and filed under ``<Label> / <Label> <year>`` in the
same intake file, the year from the manifest since a file's year tag was never
verified. Everything the tree writer can refuse is asked of a copy before the
first move; a disk refusal after it is a warning over an intake file that stays.

On a native intake tree (R-746) :func:`apply_native` moves the same way and
adds the files through :mod:`cratekit.intake.native`. The verb chooses.

Layer: modules.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import unicodedata
from contextlib import contextmanager
from dataclasses import dataclass, replace
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Iterator, Mapping, Sequence, TypeVar

from cratekit.acquire import listdoc, match, match_cli
from cratekit.core import (
    active_taxonomy,
    analysis_store,
    cause,
    config,
    jobs,
    locations,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError
from cratekit.core.naming import AUDIO_EXTS, NameTemplate
from cratekit.core.preflight import device_of as _device_of
from cratekit.intake import collection_xml, ingest, native
from cratekit.intake.ingest import PlacedTrack
from cratekit.write import rbxml, trees

if TYPE_CHECKING:
    from cratekit.intake.account_playlists import Claimed, Left

#: The per item download directory ``acquire download`` keeps under staging,
#: an unfinished attempt. Named here, since the acquisition verbs are not this layer's.
ACQUIRE_STAGING_DIRNAME = ".cratekit-acquire-staging"

#: The manifest ``source`` whose rows are filed under the catalog tree.
LABEL_SOURCE = "label"

#: Why a label row was filed under nothing. Warning codes, not refusal reasons.
NO_LABEL = "label-row-incomplete"
NO_FILE = "label-row-unmatched"
NOT_EXACT = "label-row-needs-review"
NOT_WRITTEN = "label-tree-unwritten"

_ORIGIN = ("intake.landing",)

#: Every refusal here carries this engine's origin.
refuse = partial(cause.refuse, origin=_ORIGIN)


@dataclass(frozen=True, slots=True)
class Plan:
    """What :func:`apply` will move, and the fingerprint it was listed at."""

    folder: Path
    batch: str
    items: tuple[Path, ...]
    digest: str


@dataclass(frozen=True, slots=True)
class Refused:
    """One file that did not land, and the sentence that says why."""

    path: Path
    reason: str
    sentence: str


@dataclass(frozen=True, slots=True)
class Moved:
    """One file that left staging, by both of its names."""

    source: Path
    target: Path


@dataclass(frozen=True, slots=True)
class Labelled:
    """One year playlist written under a label, and the ids it was given."""

    label: str
    year: int
    playlist: str
    track_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class Checked:
    """The registry and active taxonomy :func:`preflight` read, handed to the write (R-685)."""

    registry: tree_registry.Registry
    declared: taxonomy.Taxonomy


@dataclass(frozen=True, slots=True)
class Unlabelled:
    """One label row of the manifest that was filed under no label, by name."""

    ref: str
    artist: str
    title: str
    label: str
    year: int | None
    reason: str
    sentence: str


@dataclass(frozen=True, slots=True)
class Landed:
    """A batch that reached the library and one intake file."""

    destination: Path
    placed: tuple[PlacedTrack, ...]
    moved: tuple[Moved, ...]
    refused: tuple[Refused, ...]
    labelled: tuple[Labelled, ...] = ()
    unlabelled: tuple[Unlabelled, ...] = ()
    #: The account playlists written into the intake file, each with its count.
    split: tuple[tuple[Claimed, int], ...] = ()
    #: Each account playlist track the intake file does not hold, by playlist name.
    left: tuple[tuple[str, Left], ...] = ()


def export_rows(content: bytes) -> list[trees.ContentRow]:
    """The export's collection entries as the row matcher reads them (U128).

    An entry whose Location names another machine is dropped before the index,
    which would refuse it, since it is no file of this library.
    """
    found: list[trees.ContentRow] = []
    for track in rbxml.collection_tracks(content):
        recorded = rbxml.attributes(content, track).get("Location", "")
        try:
            locations.location_to_path(recorded)
        except locations.LocationDecodeError:
            continue
        found.append(trees.ContentRow(content_id=track.track_id, recorded=recorded, deleted=False))
    return found


def owned_in_export(
    cfg: config.Config, split: Sequence[Claimed], export: Path
) -> tuple[tuple[Claimed, ...], tuple[tuple[str, Left], ...]]:
    """Each account playlist with its owned tracks found in the export by path (U128).

    The export's TrackID is the row the import joins to the playlist. An export
    that cannot be read finds nothing here, and the preflight refuses it.
    """
    from cratekit.intake import account_playlists

    if not any(one.owned for one in split):
        return tuple(split), ()
    try:
        content = export.read_bytes()
    except OSError:
        content = b""
    return account_playlists.resolve_owned(cfg, split, export_rows(content))


def _assert_owned_unchanged(cfg: config.Config, split: Sequence[Claimed], export: Path) -> None:
    """Refuse when the export's entries for the owned tracks moved since the plan.

    An export rewritten since the gate could give another track the same
    TrackID, and the playlist would name the wrong track.
    """
    if not any(one.owned for one in split):
        return
    planned = {(one.name, m.paths): m.row for one in split for m in one.members if m.file is None}
    again, _emptied = owned_in_export(
        cfg, [replace(one, left=()) for one in split], export
    )
    now = {(one.name, m.paths): m.row for one in again for m in one.members if m.file is None}
    if now != planned:
        raise refuse(
            "decision-stale",
            f"{export} no longer lists the owned tracks of the account playlists as it "
            f"did when this landing was planned, so nothing was moved; run the landing "
            f"again against the export as it is",
            detail={"export": str(export)},
        )


def _inbox_playlists(
    split: Sequence[Claimed], *, target: Path, pass_name: str | None
) -> list[ingest.InboxPlaylist]:
    """Each account playlist as the intake file writes it, new members by landed path."""
    return [
        ingest.InboxPlaylist(
            name=one.name,
            members=tuple(
                target / member.file.name if member.file is not None else member.row
                for member in one.members
            ),
            account=one.playlist_id,
            pass_name=pass_name or "",
        )
        for one in split
    ]


def _listable(entry: Path) -> bool:
    name = entry.name
    if name.startswith(".") or name == ACQUIRE_STAGING_DIRNAME:
        return False
    if entry.suffix.lower() not in AUDIO_EXTS:
        return False
    return entry.is_file() and not entry.is_symlink()


def _list(folder: Path) -> tuple[Path, ...]:
    return tuple(sorted((e for e in folder.iterdir() if _listable(e)), key=lambda p: p.name))


def listing(folder: Path) -> tuple[Path, ...]:
    """What :func:`plan` would take from the directory ``folder``, without refusing on none."""
    return _list(folder)


def _digest(items: tuple[Path, ...]) -> str:
    """Name, size and mtime of every item, so a file replaced under its name differs."""
    hasher = hashlib.sha256()
    for item in items:
        stat = item.stat()
        hasher.update(f"{item.name}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
    return hasher.hexdigest()


def plain_name(text: str) -> bool:
    """Whether ``text`` is one plain folder or file name: the batch and the pass rule (U110)."""
    return bool(
        text
        and text == text.strip()
        and not text.startswith(".")
        and not any(char in text for char in ("/", "\\", "\0"))
    )


def _check_batch(batch: str) -> None:
    if not plain_name(batch):
        raise refuse(
            "intake-list-unusable",
            f"{batch!r} is not a batch name this engine can land under, because "
            f"it must be one plain folder name under the music folder",
            detail={"batch": batch},
        )


#: The state entry holding one lock file per batch name.
LOCK_KEY = "landing_locks"


def lock_key(batch: str) -> str:
    """A batch's lock file name, one per NAME and not per spelling.

    Case and Unicode composition fold, since case insensitive volumes hold one
    folder for both spellings; a digest, since a batch name may be long or odd.
    """
    folded = unicodedata.normalize("NFC", batch.casefold())
    return hashlib.sha256(folded.encode("utf-8")).hexdigest()


def _holder(path: Path) -> str:
    """Who holds a lock, from what the holder wrote in it, never a liveness test."""
    try:
        holder = json.loads(path.read_text(encoding="utf-8"))
        return f"pid {holder['pid']}, since {holder['acquired']}"
    except (OSError, ValueError, TypeError, KeyError):
        return "holder unknown"


@contextmanager
def _held(key: str, refusal: Callable[[str, Path], CratekitError]) -> Iterator[Path]:
    """Hold one landing lock, or raise ``refusal(who, path)`` without waiting."""
    root = config.state_path(LOCK_KEY)
    lock = jobs.driver_lock(key, root=root)
    # Entered by hand so only the TAKING is translated: a held job lock raised
    # by the caller's body is not a second landing.
    try:
        path = lock.__enter__()
    except jobs.DriverHeld:
        held = jobs.lock_path(key, root=root)
        raise refusal(_holder(held), held) from None
    try:
        yield path
    finally:
        lock.__exit__(None, None, None)


@contextmanager
def batch_lock(batch: str) -> Iterator[Path]:
    """Hold the one landing per batch name lock, or refuse without waiting (R-432).

    :func:`apply` checks a target free and then renames over it, which cannot be
    atomic on exFAT, so two landings into one batch folder are kept apart. The
    lock is :func:`jobs.driver_lock` on the local state disk: non blocking,
    released when the holder dies, never unlinked. Keyed by name, not folder,
    so one name in two libraries waits on itself; a platform with no ``fcntl``
    gets no lock.
    """

    def refusal(who: str, held: Path) -> CratekitError:
        return refuse(
            "job-driver-held",
            f"another landing under the batch name {batch!r} is running ({who}), "
            f"so nothing was moved; two landings into one batch folder can "
            f"replace each other's files",
            steps=(
                "wait for that landing to finish, then run this one again",
                "if that landing succeeded its folder now holds the name, so land "
                "this folder under another --name, or with none and the next free "
                "name is taken",
            ),
            retryable=True,
            origin=_ORIGIN,
            detail={"batch": batch, "lock": str(held), "holder": who},
        )

    with _held(lock_key(batch), refusal) as path:
        yield path


@contextmanager
def intake_lock(stem: str) -> Iterator[Path]:
    """Hold the one landing per intake file lock, or refuse without waiting.

    The intake file is named for the pass, so two batch names can still write
    one intake file. The key holds a NUL, which no batch name can.
    """

    def refusal(who: str, held: Path) -> CratekitError:
        return refuse(
            "job-driver-held",
            f"another landing writing the intake file for {stem!r} is running "
            f"({who}), so nothing was moved; two landings writing one intake file "
            f"replace each other's importable file",
            steps=(
                "wait for that landing to finish, then run this one again",
                "if that landing succeeded this pass has its intake file, so land "
                "this folder under another --pass",
            ),
            retryable=True,
            detail={"intake": stem, "lock": str(held), "holder": who},
        )

    with _held(lock_key("intake file\0" + stem), refusal) as path:
        yield path


def plan(folder: Path, cfg: config.Config, batch: str) -> Plan:
    """List ``folder``, one level deep, and fingerprint it; library checks wait for apply."""
    _check_batch(batch)
    if not folder.is_dir():
        raise refuse(
            "intake-list-unusable",
            f"{folder} is not a folder, so there is nothing to land",
            detail={"folder": str(folder)},
        )
    items = _list(folder)
    if not items:
        raise refuse(
            "intake-list-unusable",
            f"{folder} holds no audio file to land; dotfiles, subfolders and "
            f"unfinished downloads are skipped",
            detail={"folder": str(folder)},
        )
    return Plan(folder=folder, batch=batch, items=items, digest=_digest(items))


def target_dir(cfg: config.Config, batch: str) -> Path:
    """Where a batch lands, ``library.root / music_dir / <batch>``."""
    return Path(cfg.library.root) / cfg.library.music_dir / batch


def _check_library(cfg: config.Config, folder: Path, target: Path) -> None:
    root = Path(cfg.library.root)
    if not root.is_dir():
        # Before the device probe: an unmounted volume's nearest ancestor is
        # the boot disk.
        raise refuse(
            "library-root-unreachable",
            f"the library root {root} is not there, so nothing was moved",
            detail={"root": str(root)},
        )
    staging = Path(cfg.paths.download_staging).resolve()
    source = folder.resolve()
    in_staging = source == staging or staging in source.parents
    owned = root.resolve()
    if not in_staging and (source == owned or owned in source.parents):
        # Moving a folder the library owns strands its collection rows.
        # Staging configured inside the root is still staging.
        raise refuse(
            "intake-list-unusable",
            f"{folder} is inside the library at {root} and outside download "
            f"staging, so its files are already owned and nothing was moved",
            detail={"folder": str(folder), "root": str(root)},
        )
    resolved = target.resolve()
    if resolved == staging or staging in resolved.parents:
        raise refuse(
            "intake-staging-refused",
            f"{target} is under download staging at {staging}, so landing there "
            f"would move nothing out of it",
            detail={"target": str(target), "staging": str(staging)},
        )
    here = _device_of(folder)
    there = _device_of(target)
    if here is None or there is None or here != there:
        raise refuse(
            "intake-staging-refused",
            f"{folder} is on a different device from the library at {target}, so "
            f"a move would be a copy and nothing was moved; put download staging "
            f"on the library's volume",
            detail={"folder": str(folder), "target": str(target)},
        )


def _check_export(
    export: Path, playlist: str, checked: Checked, label_rows: tuple[listdoc.ManifestRow, ...] = ()
) -> None:
    """Every refusal ``place_files`` and the tree writer can make, made on a copy.

    Before any move, since the same refusal after the moves leaves a batch in
    the library with no intake file.
    """
    # BEFORE THE EXPORT IS LOOKED FOR (R-770), so a native intake tree is
    # refused naming the landing that takes it, not as a defect.
    tree = ingest.bridge_intake_tree(checked.declared, checked.registry)
    if not export.is_file():
        raise refuse(
            "library-export-unusable",
            f"no Fresh Export at {export}, so nothing was moved",
            steps=("export the collection again from rekordbox and pass that file",),
        )
    trial = bytearray(export.read_bytes())
    collection_xml.splice_tracks(trial, [])
    registry = checked.registry
    error = rbxml.insert_intake_playlist(trial, playlist, [], tree=tree)
    if error:
        raise refuse(
            "library-export-unusable",
            f"the intake playlist could not be written ({error}), so nothing was moved",
            steps=(
                "export the collection again from rekordbox so the intake "
                "folder is present, then retry",
            ),
        )
    # EVERY label and year the manifest names, since which rows land is known
    # only after the moves (R-455).
    catalog: dict[str, set[int]] = {}
    for row in label_rows:
        name, year = _label_of(row), row.provenance.year
        if name and year is not None:
            catalog.setdefault(name, set()).add(year)
    try:
        trees.check_record_labels_tree(
            bytes(trial), catalog, declared=checked.declared, registry=registry
        )
    except CratekitError as exc:
        said = (
            f"the label tree could not be written into {export.name} "
            f"({exc.cause.message}), so nothing was moved"
        )
        detail = {"export": str(export)}
        if exc.cause.reason != "internal-error":
            raise refuse(
                exc.cause.reason,
                said,
                remedy=exc.cause.remediation.remedy,
                steps=exc.cause.remediation.steps,
                detail=detail,
                inner=exc.cause,
            ) from exc
        # The writer calls every layout it will not write into a defect; here
        # it is a Fresh Export the person mends in rekordbox.
        raise refuse(
            "library-export-unusable",
            said,
            steps=(
                "in rekordbox, under the record labels folder, remove or merge "
                "the folder or playlist the message names",
                "export the collection again and pass that file",
            ),
            detail=detail,
            inner=exc.cause,
        ) from exc


def preflight(
    plan: Plan,
    *,
    cfg: config.Config,
    export: Path,
    destination: Path,
    label_rows: tuple[listdoc.ManifestRow, ...] = (),
    names: Sequence[str] = (),
) -> Checked:
    """Every check :func:`apply` makes before its first move, in its order (R-677).

    One place, since a caller asks these before its gate and :func:`apply` again.
    The library goes before the export, so an unmounted volume is named as such.
    ``names`` are the account playlists the landing writes (U113). Moves nothing.
    """
    _check_batch(plan.batch)
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
    if destination.exists():
        raise refuse(
            "output-exists",
            f"{destination} already exists and is never overwritten, so nothing was moved",
            detail={"path": str(destination)},
        )
    # READ ONCE, BEFORE THE FIRST MOVE, for the check and the write alike.
    checked = Checked(registry=tree_registry.read(cfg), declared=active_taxonomy.load(cfg))
    _check_export(export, plan.batch, checked, label_rows)
    _check_names_free(export, checked, names)
    return checked


def inbox_held(export: Path, checked: Checked) -> tuple[str, ...] | str:
    """Every name an imported playlist could meet, or a sentence naming why it could not be read.

    The names under the export's intake tree and at its playlist root, where an
    imported playlist lands before it is dragged into the intake folder (U113).
    """
    try:
        content = export.read_bytes()
    except OSError as exc:
        return f"{export} could not be read ({exc.strerror or exc})"
    try:
        tree = ingest.bridge_intake_tree(checked.declared, checked.registry)
    except CratekitError as exc:
        return exc.cause.message
    held = rbxml.intake_names(content, tree=tree)
    if isinstance(held, str):
        return held
    root = rbxml.root_node(content)
    at_root = tuple(node.name for node in rbxml.child_nodes(content, root)) if root else ()
    return (*held, *at_root)


def _check_names_free(export: Path, checked: Checked, names: Sequence[str]) -> None:
    """Refuse an account playlist name the export holds since it was chosen (U113)."""
    if not names:
        return
    held = inbox_held(export, checked)
    if isinstance(held, str):
        return
    clash = sorted(set(names) & set(held))
    if clash:
        raise refuse(
            "decision-stale",
            f"{export} holds {', '.join(repr(name) for name in clash)} under the intake "
            f"folder since this landing chose those names, so nothing was moved; run "
            f"the landing again and it takes the next free name",
            detail={"export": str(export), "names": clash},
        )


def _label_of(row: listdoc.ManifestRow) -> str:
    return (row.provenance.label_name or "").strip()


@dataclass(frozen=True, slots=True)
class LabelManifest:
    """A manifest's label rows, and the fingerprint of the bytes they came from."""

    path: Path
    digest: str
    rows: tuple[listdoc.ManifestRow, ...]

    def playlists(self) -> dict[str, int]:
        """Every ``<Label> <year>`` the rows name, and how many rows name it."""
        counted: dict[str, int] = {}
        for row in self.rows:
            label, year = _label_of(row), row.provenance.year
            if label and year is not None:
                name = f"{label} {year}"
                counted[name] = counted.get(name, 0) + 1
        return counted


def read_label_manifest(manifest: Path) -> LabelManifest:
    """The manifest's label rows, or a refusal before anything has moved.

    The fingerprint and the rows come from ONE read, so a manifest rewritten
    between two reads cannot file tracks under labels nobody was shown.
    """
    steps = (
        "pass the manifest that label approved wrote beside the list, "
        "or land without one to file nothing under a label",
    )
    try:
        raw = manifest.read_bytes()
    except OSError as exc:
        raise refuse(
            "intake-list-unusable",
            f"the manifest {manifest} could not be read ({exc.strerror or exc}), "
            f"so nothing was moved",
            steps=steps,
            detail={"manifest": str(manifest)},
        ) from exc
    try:
        rows = listdoc.manifest_rows(raw, manifest)
    except listdoc.ListDocRefused as exc:
        raise refuse(
            "intake-list-unusable",
            f"{exc}, so nothing was moved",
            steps=steps,
            detail={"manifest": str(manifest)},
        ) from exc
    return LabelManifest(
        path=manifest,
        digest=hashlib.sha256(raw).hexdigest(),
        rows=tuple(row for row in rows if row.provenance.source == LABEL_SOURCE),
    )


def _never_suppressed(_recording: str, _address: object) -> bool:
    """No tombstone is consulted: an unmatched row is reported the same either way."""
    return False


def _no_suppression_id(_recording: str, _address: object) -> str:
    return ""


def _unlabelled(row: listdoc.ManifestRow, reason: str, because: str) -> Unlabelled:
    artist = str(row.track.get("artist", ""))
    title = str(row.track.get("title", ""))
    version = str(row.track.get("version", ""))
    spelled = f"{artist} - {title}" + (f" ({version})" if version else "")
    return Unlabelled(
        ref=row.ref,
        artist=artist,
        title=title,
        label=_label_of(row),
        year=row.provenance.year,
        reason=reason,
        sentence=f"{spelled} was filed under no label playlist by this run, because {because}",
    )


#: A label's years, and under each the rows filed there with their track ids.
_Filed = dict[str, dict[int, list[tuple[listdoc.ManifestRow, list[int]]]]]

_Key = TypeVar("_Key")


def _file_labels(
    label_rows: tuple[listdoc.ManifestRow, ...],
    placed: list[PlacedTrack],
    batch_dir: Path,
    template: NameTemplate,
) -> tuple[_Filed, list[Unlabelled]]:
    """Each label row tied to the track ids of the files this call landed.

    THE INDEX IS OF THE BATCH FOLDER ONLY, and a match is looked up among THIS
    call's placed tracks, so no row resolves to a copy the library held before.
    ``template`` is the library's own, lossy marker included, as ``acquire match``.
    """
    ids = {item.path.resolve(): item.track_id for item in placed}
    index = match.index_library(batch_dir, template=template)
    return match_label_rows(label_rows, index, ids)


def match_label_rows(
    label_rows: Sequence[listdoc.ManifestRow], index: match.LibraryIndex, ids: Mapping[Path, _Key]
) -> tuple[dict[str, dict[int, list[tuple[listdoc.ManifestRow, list[_Key]]]]], list[Unlabelled]]:
    """Each label row tied to the keys of the files it matched, and every row filed nowhere.

    The one rule both media file a manifest by (U156). ``ids`` maps each moved
    file, resolved, to the caller's key; a match ``ids`` does not name is unfiled.
    """
    filed: dict[str, dict[int, list[tuple[listdoc.ManifestRow, list[_Key]]]]] = {}
    unfiled: list[Unlabelled] = []
    for position, row in enumerate(label_rows, start=1):
        label, year = _label_of(row), row.provenance.year
        if not label or year is None:
            absent = "label name" if not label else "year"
            unfiled.append(
                _unlabelled(
                    row,
                    NO_LABEL,
                    f"its manifest row carries no {absent}; a file that landed "
                    f"for it is in the intake playlist",
                )
            )
            continue
        try:
            wanted = match.read_row(row.track, origin=match.TIDAL, position=position)
        except match.UnreadableList as exc:
            unfiled.append(
                _unlabelled(
                    row,
                    NO_LABEL,
                    f"its manifest row could not be read ({exc}); a file that "
                    f"landed for it is in the intake playlist",
                )
            )
            continue
        found = match.resolve_one(
            wanted, index, suppresses=_never_suppressed, suppression_id=_no_suppression_id
        )
        if found.state is match.MatchState.NEEDS_REVIEW:
            # Filing a near match would answer a question only a person may.
            unfiled.append(
                _unlabelled(
                    row,
                    NOT_EXACT,
                    f"the batch holds something close to it and not it "
                    f"({found.why}); that file is in the intake playlist",
                )
            )
            continue
        landed = [
            ids[Path(path).resolve()]
            for path in (found.paths if found.state is match.MatchState.MATCHED else ())
            if Path(path).resolve() in ids
        ]
        if not landed:
            # TRUE OF BOTH ROWS IT IS SAID ABOUT: a download that never arrived
            # and a row an earlier landing filed look the same here (R-457).
            unfiled.append(
                _unlabelled(
                    row,
                    NO_FILE,
                    "no file it landed matches it; a track an earlier landing "
                    "filed keeps the playlist it was given",
                )
            )
            continue
        filed.setdefault(label, {}).setdefault(year, []).append((row, landed))
    return filed, unfiled


def _label(
    cfg: config.Config,
    destination: Path,
    checked: Checked,
    label_rows: tuple[listdoc.ManifestRow, ...],
    placed: list[PlacedTrack],
    batch_dir: Path,
) -> tuple[list[Labelled], list[Unlabelled]]:
    """Write every label the batch carries into the intake file, and say which (R-456).

    A TREE THAT CANNOT BE WRITTEN IS REPORTED, NOT RAISED: the files have moved
    and ``place_files`` recorded a routing intent for each, so the intake file
    stays, whole, since the writer replaces it atomically.
    """
    if not label_rows:
        return [], []
    try:
        filed, unlabelled = _file_labels(
            label_rows, placed, batch_dir, match_cli.library_template(cfg)
        )
    except OSError as exc:
        said = f"the batch folder could not be read ({exc.strerror or exc})"
        return [], [_unlabelled(row, NOT_WRITTEN, said) for row in label_rows]
    if not filed:
        return [], unlabelled
    years = {
        label: {
            year: [track_id for _, ids in rows for track_id in ids]
            for year, rows in by_year.items()
        }
        for label, by_year in filed.items()
    }
    try:
        # One album per year; the writer dedupes across the year. The intake
        # file is this call's own product, so no Fresh Export is written over.
        trees.insert_record_labels_trees(
            destination,
            {
                label: {year: [{"track_ids": ids}] for year, ids in by_year.items()}
                for label, by_year in years.items()
            },
            destination,
            declared=checked.declared,
            registry=checked.registry,
        )
    except (CratekitError, OSError) as exc:
        said = f"the label tree could not be written ({exc})"
        unlabelled.extend(
            _unlabelled(row, NOT_WRITTEN, said)
            for label in sorted(filed)
            for year in sorted(filed[label], reverse=True)
            for row, _ in filed[label][year]
        )
        return [], unlabelled
    labelled = [
        Labelled(
            label=label,
            year=year,
            playlist=f"{label} {year}",
            track_ids=tuple(rbxml.dedupe_track_ids(years[label][year])),
        )
        for label in sorted(years)
        for year in sorted(years[label], reverse=True)
    ]
    return labelled, unlabelled


def _unplaceable(path: Path, declared: taxonomy.Taxonomy) -> Refused | None:
    """A file ``place_files`` would refuse, asked of its tags before it moves."""
    meta = {
        "genre": tags.read_genre_from_file(path) or "",
        "energy": tags.read_energy_from_file(path),
    }
    if ingest.decide_placement(meta, declared) is not None:
        return None
    return Refused(
        path=path,
        reason="intake-list-unusable",
        sentence=(
            f"{path.name} resolves to a bucket with no declared sub, so it was "
            f"left in staging; run crate tag folder over it and land it again"
        ),
    )


def _occupied(item: Path, final: Path) -> Refused | None:
    """A target that already holds something, which is never replaced."""
    if not (final.exists() or final.is_symlink()):
        return None
    return Refused(
        path=item,
        reason="output-exists",
        sentence=(
            f"{final} already exists, so {item.name} was left in staging and "
            f"the library copy was not replaced"
        ),
    )


def _remove_if_empty(folder: Path) -> None:
    """Take back a batch folder this call made and put nothing in."""
    with contextlib.suppress(OSError):
        folder.rmdir()


def _moved_detail(moved: list[Moved], refused: list[Refused]) -> dict:
    return {
        "moved": [str(item.target) for item in moved],
        "refused": [str(item.path) for item in refused],
    }


def _moved_sentence(moved: list[Moved]) -> str:
    if not moved:
        return "nothing was moved"
    names = ", ".join(item.target.name for item in moved)
    return f"{len(moved)} file(s) were already moved into the library and stay there: {names}"


def _none_landed(
    plan: Plan, nothing_after: str, moved: list[Moved], refused: list[Refused]
) -> CratekitError:
    return refuse(
        "intake-list-unusable",
        f"no file in {plan.folder} could land, so nothing was moved and "
        f"{nothing_after}: " + "; ".join(entry.sentence for entry in refused),
        detail=_moved_detail(moved, refused),
    )


def _assert_unchanged(plan: Plan) -> None:
    """Refuse a plan whose folder is not what it was listed as, before any move."""
    items = _list(plan.folder) if plan.folder.is_dir() else ()
    if items != plan.items or _digest(items) != plan.digest:
        raise refuse(
            "decision-stale",
            f"{plan.folder} changed after it was planned, so nothing was moved",
            detail={"folder": str(plan.folder)},
        )


def _screen(
    plan: Plan,
    target: Path,
    declared: taxonomy.Taxonomy,
    *,
    nothing_after: str,
    also_refused: Mapping[Path, Refused] | None = None,
) -> tuple[list[Path], list[Refused]]:
    """Which planned files may move, and which are refused alone, on both media.

    A file is refused when the medium refuses it (``also_refused``, by staged
    path), its tags resolve to no declared sub, or its target is occupied. A
    batch where nothing may move refuses before the batch folder is made.
    """
    named = dict(also_refused or {})
    refused: list[Refused] = []
    movable: list[Path] = []
    for item in plan.items:
        blocked = (
            named.get(item) or _unplaceable(item, declared) or _occupied(item, target / item.name)
        )
        if blocked is not None:
            refused.append(blocked)
        else:
            movable.append(item)
    if not movable:
        raise _none_landed(plan, nothing_after, [], refused)
    return movable, refused


def _move(
    plan: Plan, target: Path, movable: list[Path], refused: list[Refused], *, nothing_after: str
) -> list[Moved]:
    """Rename every movable file into ``target``, or refuse with the moves named.

    The one move loop for both media; ``nothing_after`` names what a refusal
    here says was not done. A target is asked again at the move, since a file
    can arrive there and ``os.replace`` would take its place silently (R-432).
    """
    made = not target.exists()
    target.mkdir(parents=True, exist_ok=True)
    moved: list[Moved] = []
    for item in movable:
        final = target / item.name
        occupied = _occupied(item, final)
        if occupied is not None:
            refused.append(occupied)
            continue
        try:
            os.replace(item, final)
        except OSError as exc:
            if made and not moved:
                _remove_if_empty(target)
            raise refuse(
                "path-permission-denied"
                if isinstance(exc, PermissionError)
                else "intake-list-unusable",
                f"{item.name} could not be moved to {final} ({exc.strerror or exc}); "
                f"{nothing_after} and {_moved_sentence(moved)}",
                detail=_moved_detail(moved, refused),
            ) from exc
        moved.append(Moved(source=item, target=final))

    if not moved:
        if made:
            _remove_if_empty(target)
        raise _none_landed(plan, nothing_after, moved, refused)
    return moved


def apply(
    plan: Plan,
    *,
    cfg: config.Config,
    export: Path,
    destination: Path,
    manifest: Path | None = None,
    manifest_digest: str | None = None,
    split: Sequence[Claimed] = (),
    pass_name: str | None = None,
) -> Landed:
    """Move the planned files into the library, then write one intake file.

    ``split`` is the account playlists (U113), each its own playlist in the
    intake file with its owned tracks the export lists (U128); the batch
    playlist keeps the rest, and ``pass_name`` is recorded beside each.
    ``manifest`` files its label rows under the catalog tree; a
    ``manifest_digest`` that is not the bytes read here refuses as stale.
    """
    _assert_unchanged(plan)
    label_rows: tuple[listdoc.ManifestRow, ...] = ()
    if manifest is not None:
        read = read_label_manifest(manifest)
        if manifest_digest is not None and read.digest != manifest_digest:
            raise refuse(
                "decision-stale",
                f"{manifest} changed after it was planned, so nothing was moved",
                detail={"manifest": str(manifest)},
            )
        label_rows = read.rows
    checked = preflight(
        plan,
        cfg=cfg,
        export=export,
        destination=destination,
        label_rows=label_rows,
        names=[claimed.name for claimed in split],
    )
    target = target_dir(cfg, plan.batch)
    movable, refused = _screen(
        plan, target, checked.declared, nothing_after="no intake file was written"
    )
    _assert_owned_unchanged(cfg, split, export)
    moved = _move(plan, target, movable, refused, nothing_after="no intake file was written")
    inbox = _inbox_playlists(split, target=target, pass_name=pass_name)
    left: list[tuple[str, Left]] = [(one.name, row) for one in split for row in one.left]

    try:
        placed = ingest.place_files(
            [item.target for item in moved],
            cfg=cfg,
            export=export,
            destination=destination,
            declared=checked.declared,
            registry=checked.registry,
            # The batch's own name (U110), not the pass's intake file stem.
            playlist=plan.batch,
            split=inbox,
        )
    except Exception as exc:
        # The intake file may be written before a ledger refusal; it was
        # checked absent above, so the one there now is this call's.
        destination.unlink(missing_ok=True)
        inner = exc.cause if isinstance(exc, CratekitError) else None
        raise refuse(
            exc.cause.reason if isinstance(exc, CratekitError) else "internal-error",
            f"the intake file could not be written ({exc}); none was left "
            f"behind and {_moved_sentence(moved)}",
            detail=_moved_detail(moved, refused),
            inner=inner,
        ) from exc

    labelled, unlabelled = _label(cfg, destination, checked, label_rows, placed, target)
    # Each playlist's count is what the intake file holds for it (U128); a
    # playlist holding nothing is not written, so not reported.
    from cratekit.intake import account_playlists

    ids_by_path = {item.path: item.track_id for item in placed}
    counted: list[tuple[Claimed, int]] = []
    for claimed, written in zip(split, inbox, strict=True):
        left.extend(
            (claimed.name, member.left(account_playlists.NOT_LANDED))
            for member in claimed.members
            if member.file is not None and target / member.file.name not in ids_by_path
        )
        count = len(written.track_ids(ids_by_path))
        if count:
            counted.append((claimed, count))
    return Landed(
        destination=destination,
        placed=tuple(placed),
        moved=tuple(moved),
        refused=tuple(refused),
        labelled=tuple(labelled),
        unlabelled=tuple(unlabelled),
        split=tuple(counted),
        left=tuple(left),
    )


@dataclass(frozen=True, slots=True)
class LandedNative:
    """A batch that reached the library and the collection, with no intake file."""

    moved: tuple[Moved, ...]
    refused: tuple[Refused, ...]
    collection: native.NativeLanded


def preflight_native(plan: Plan, *, cfg: config.Config, target: Path | None = None) -> None:
    """The library half of :func:`preflight`; ``target`` the folder the plan chose (U164)."""
    _check_batch(plan.batch)
    _check_library(cfg, plan.folder, target if target is not None else target_dir(cfg, plan.batch))


def refuse_past(
    exc: Exception, head: str, tail: str, *, origin: tuple[str, ...], detail: Mapping[str, Any]
) -> CratekitError:
    """A failure past the moves or the gate, saying what it leaves.

    A cause this product raised keeps its reason, remedy and detail; anything
    else is reported as the defect it is, with the same sentence.
    """
    inner = exc.cause if isinstance(exc, CratekitError) else None
    return cause.refuse(
        inner.reason if inner is not None else "internal-error",
        f"{head} ({inner.message if inner is not None else exc}); {tail}",
        remedy=inner.remediation.remedy if inner is not None else None,
        steps=inner.remediation.steps if inner is not None else (),
        origin=origin,
        detail={**detail, **(dict(inner.detail) if inner is not None else {})},
        inner=inner,
    )


def apply_native(
    plan: Plan, *, cfg: config.Config, db: Any, rows: native.NativePlan, declared: taxonomy.Taxonomy
) -> LandedNative:
    """Move the planned files into the library, then add them to the collection.

    Move first, then write rows over the moved paths, as on the bridge. ``rows``
    is the approved plan and a target it does not name refuses. The database is
    all or nothing on one handle, so a failure after the moves leaves the files
    in the library and no row. A file the move refuses (no declared sub, an
    occupied target, an unsupported suffix) is refused alone and its row dropped.
    ``declared`` is the taxonomy the verb read with the registry (R-685).
    """
    _assert_unchanged(plan)
    # INTO THE FOLDER THE PLAN CHOSE (U164), which every planned row names.
    target = rows.folder if rows.folder is not None else target_dir(cfg, plan.batch)
    preflight_native(plan, cfg=cfg, target=target)
    planned = {str(row.target): row for row in rows.rows}
    unplanned = [item.name for item in plan.items if str(target / item.name) not in planned]
    if unplanned:
        raise refuse(
            "decision-stale",
            f"{len(unplanned)} file(s) in {plan.folder} have no planned row "
            f"({', '.join(unplanned)}), so nothing was moved",
            detail={"folder": str(plan.folder), "unplanned": unplanned},
        )

    # BEFORE THE FIRST MOVE, so a name taken since the plan leaves the files staged.
    native.assert_names_still_free(db, rows)
    unsupported = {
        item: Refused(path=item, reason="intake-list-unusable", sentence=row.why)
        for item in plan.items
        for row in (planned[str(target / item.name)],)
        if row.action == native.UNSUPPORTED
    }
    movable, refused = _screen(
        plan, target, declared, nothing_after="no row was added", also_refused=unsupported
    )
    moved = _move(plan, target, movable, refused, nothing_after="no row was added")

    landed_targets = {str(item.target) for item in moved}
    kept = replace_rows(rows, tuple(row for row in rows.rows if str(row.target) in landed_targets))
    try:
        collection = native.apply_rows(
            cfg, db, kept, analysis_roots=analysis_store.watch_roots(cfg)
        )
    except Exception as exc:
        raise refuse_past(
            exc,
            "the collection could not be written",
            f"no row was added and {_moved_sentence(moved)}",
            origin=_ORIGIN,
            detail=_moved_detail(moved, refused),
        ) from exc
    return LandedNative(moved=tuple(moved), refused=tuple(refused), collection=collection)


def replace_rows(rows: native.NativePlan, kept: tuple[native.RowPlan, ...]) -> native.NativePlan:
    """The plan over only the rows whose files this call moved.

    THE DIGEST IS KEPT: the approved plan minus what could not land and was
    reported by name, not a new plan nobody saw.
    """
    return replace(rows, rows=kept)
