"""Land a folder of acquired files in the library and splice them into one file.

``acquire download`` commits each file flat into download staging, and
``ingest.place_files`` refuses any path under staging, because a Location
stamped from staging dies the moment staging is cleaned (the 2026-06-29
flood). This engine is the step between them: N files in a staging folder
become N files under ``library.root / music_dir / <batch>`` and one intake
file naming every one of them.

THE ORDER IS THE WHOLE CONTRACT. Move first, then splice over the moved
paths. A splice before the rename stamps the staging Location.

Two steps, so a person can see what will move before anything does:

* :func:`plan` lists the folder and fingerprints what it found.
* :func:`apply` lists it again, refuses a stale fingerprint, runs every check
  that can refuse the whole batch, and only then moves.

A move is ``os.replace`` on one filesystem and nothing else. A staging folder
on another device is refused by name rather than copied, since a copy is a
second file whose first one a later clean deletes. A file whose target already
exists is refused alone and never overwritten. A failure after the first move
leaves the moved files where they are, because they are in the library now and
owned, and the refusal names them. No failure leaves an intake file behind.

ONE LANDING PER BATCH NAME AT A TIME, AND THE CALLER HOLDS THE LOCK (R-432).
"Refused alone and never overwritten" is a check followed by a rename, and
``os.replace`` takes an occupied name without a word, so the promise holds only
while nothing else writes into the batch folder. :func:`batch_lock` is that
exclusion. It is the caller's to hold across :func:`apply`, because the verb
owns the run and what a refused run is told, and :func:`apply` does not take it.

A MANIFEST FILES LABEL TRACKS, IN THE SAME FILE. ``acquire download`` stamps no
provider id on a file, so a landed file is tied to its manifest row by the
product's own match rule, :func:`match.resolve_one`, over an index of the batch
folder ONLY. Whether a provider's files carry a usable year tag was never
verified, which is why the year comes from the manifest and never from the
file. Every label row that resolves to a file this call landed is written under
the catalog tree, ``<Label> / <Label> <year>``, into the intake file the splice
just wrote. A row that resolves to nothing is reported by name, and its file,
if it has one, is still in the intake playlist. Everything the tree writer can
refuse is asked of a copy BEFORE the first move, for the reason the export is.
A label the disk then refuses is a warning over an intake file that stays,
because by then every landed file has a routing intent that names it.

Layer: modules.
"""

from __future__ import annotations

import hashlib
import json
import os
import unicodedata
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from cratekit.acquire import listdoc, match, match_cli
from cratekit.core import config, jobs, tags, taxonomy, tree_registry
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.naming import AUDIO_EXTS, NameTemplate
from cratekit.intake import collection_xml, ingest
from cratekit.intake.ingest import PlacedTrack
from cratekit.write import rbxml, trees

#: The per item download directory ``acquire download`` keeps under staging.
#: Whatever is in it belongs to an attempt that did not finish. Named here
#: rather than imported, because the acquisition verbs are not this layer's.
ACQUIRE_STAGING_DIRNAME = ".cratekit-acquire-staging"

#: The manifest ``source`` whose rows are filed under the catalog tree. Spelled
#: by ``label approved`` when it writes the manifest, and read here.
LABEL_SOURCE = "label"

#: Why a label row was filed under nothing. Warning codes, not refusal reasons:
#: the landing succeeded and these name what it could not tie together.
NO_LABEL = "label-row-incomplete"
NO_FILE = "label-row-unmatched"
NOT_EXACT = "label-row-needs-review"
NOT_WRITTEN = "label-tree-unwritten"

_ORIGIN = ("intake.landing",)


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
    """What :func:`plan` would take from ``folder``, without refusing on none.

    For the verb, which answers an empty staging folder with a plan of nothing
    rather than a refusal. ``folder`` must be a directory.
    """
    return _list(folder)


def _digest(items: tuple[Path, ...]) -> str:
    """Name, size and modification time of every item, in listing order.

    Not the names alone: a file replaced under the same name between plan and
    apply is a different file, and a digest of names would call it the same.
    """
    hasher = hashlib.sha256()
    for item in items:
        stat = item.stat()
        hasher.update(f"{item.name}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
    return hasher.hexdigest()


def _check_batch(batch: str) -> None:
    if (
        not batch
        or batch != batch.strip()
        or batch.startswith(".")
        or "/" in batch
        or "\\" in batch
        or "\0" in batch
    ):
        raise refuse(
            "intake-list-unusable",
            f"{batch!r} is not a batch name this engine can land under, because "
            f"it must be one plain folder name under the music folder",
            origin=_ORIGIN,
            detail={"batch": batch},
        )


#: The state entry holding one lock file per batch name.
LOCK_KEY = "landing_locks"


def lock_key(batch: str) -> str:
    """The name a batch's lock file goes by, one per NAME and not per spelling.

    ``Deep House`` and ``deep house`` are one folder on the case insensitive
    volumes a library commonly sits on, and so are the composed and decomposed
    spellings of an accented name. A lock keyed on the text as typed would hand
    each spelling its own lock over the same folder. On a volume that does tell
    them apart this refuses two landings that could have run together, which
    costs a retry and no file.

    A digest and not the name, because a batch name may hold anything a folder
    name can and may be as long as one, and the lock file's name gains a suffix.
    """
    folded = unicodedata.normalize("NFC", unicodedata.normalize("NFC", batch).casefold())
    return hashlib.sha256(folded.encode("utf-8")).hexdigest()


def _holder(path: Path) -> str:
    """Who holds a lock, from what the holder wrote in it. Never the liveness
    test, which is the kernel's, and a holder caught between taking the lock
    and writing its name is simply not known."""
    try:
        holder = json.loads(path.read_text(encoding="utf-8"))
        return f"pid {holder['pid']}, since {holder['acquired']}"
    except (OSError, ValueError, TypeError, KeyError):
        return "holder unknown"


@contextmanager
def batch_lock(batch: str) -> Iterator[Path]:
    """Hold the one landing per batch name lock, or refuse without waiting.

    The window this closes is R-432: :func:`apply` asks whether a target is
    free and then renames over it, and it checks the intake file absent long
    before ``place_files`` overwrites it. Neither can be made atomic on the
    volume, since exFAT has no hard link and Python exposes no exclusive
    rename, so two landings into one batch folder are kept apart instead.

    ON THE LOCAL STATE DISK, NOT THE LIBRARY VOLUME, for the reason the state
    entry gives. The primitive is :func:`jobs.driver_lock` and not a second
    one: non blocking, released by the kernel when the holder dies, and never
    unlinked. A held name is ``job-driver-held``, the existing cause for one
    holder at a time, said in this engine's words and not the job engine's:
    a landing has no job and no driver, and the key is a digest nobody typed.

    WAITING IS NOT THE WHOLE REMEDY, so the steps say the rest. A first
    landing that succeeds leaves an intake file under the name, and the second
    is then refused by :func:`apply` over that file however long it waited.

    WHAT IT DOES NOT HOLD, each recorded against R-432's closure. The key is
    the NAME and not the folder, so one name in two libraries on one machine
    waits on itself, which refuses a landing that was safe and never admits one
    that was not. Two landings of ONE staging folder under two names are not
    kept apart. A platform with no ``fcntl`` gets no lock at all, because the
    primitive proceeds unlocked there. And one small file per batch name stays
    behind for good, since unlinking a lock file races its live holder.
    """
    key = lock_key(batch)
    root = config.state_path(LOCK_KEY)
    lock = jobs.driver_lock(key, root=root)
    # Entered by hand so only the TAKING is translated. A ``with`` around the
    # yield would also catch a held job lock raised by whatever the caller runs
    # under this one, and report it as a second landing.
    try:
        path = lock.__enter__()
    except jobs.DriverHeld:
        held = jobs.lock_path(key, root=root)
        who = _holder(held)
        raise refuse(
            "job-driver-held",
            f"another landing under the batch name {batch!r} is running ({who}), "
            f"so nothing was moved; two landings into one batch folder can "
            f"replace each other's files",
            steps=(
                "wait for that landing to finish, then run this one again",
                "if that landing succeeded its intake file now holds the name, "
                "so land this folder under another --name",
            ),
            retryable=True,
            origin=_ORIGIN,
            detail={"batch": batch, "lock": str(held), "holder": who},
        ) from None
    try:
        yield path
    finally:
        lock.__exit__(None, None, None)


def plan(folder: Path, cfg: config.Config, batch: str) -> Plan:
    """List ``folder``, one level deep, and fingerprint what would move.

    ``cfg`` is the verb's call shape. The listing itself reads no config, and
    every check against the library waits for :func:`apply`, which is where
    the library has to be there.
    """
    _check_batch(batch)
    if not folder.is_dir():
        raise refuse(
            "intake-list-unusable",
            f"{folder} is not a folder, so there is nothing to land",
            origin=_ORIGIN,
            detail={"folder": str(folder)},
        )
    items = _list(folder)
    if not items:
        raise refuse(
            "intake-list-unusable",
            f"{folder} holds no audio file to land; dotfiles, subfolders and "
            f"unfinished downloads are skipped",
            origin=_ORIGIN,
            detail={"folder": str(folder)},
        )
    return Plan(folder=folder, batch=batch, items=items, digest=_digest(items))


def target_dir(cfg: config.Config, batch: str) -> Path:
    """Where a batch lands, ``library.root / music_dir / <batch>``."""
    return Path(cfg.library.root) / cfg.library.music_dir / batch


def _device_of(path: Path) -> int | None:
    """The device of ``path``, or of its nearest existing ancestor."""
    probe = path
    while True:
        try:
            return probe.stat().st_dev
        except OSError:
            if probe.parent == probe:
                return None
            probe = probe.parent


def _check_library(cfg: config.Config, folder: Path, target: Path) -> None:
    root = Path(cfg.library.root)
    if not root.is_dir():
        # Before the device probe, because the nearest existing ancestor of an
        # unmounted volume is the boot disk, and a batch landed there is a
        # library nobody imports.
        raise refuse(
            "library-root-unreachable",
            f"the library root {root} is not there, so nothing was moved",
            origin=_ORIGIN,
            detail={"root": str(root)},
        )
    staging = Path(cfg.paths.download_staging).resolve()
    source = folder.resolve()
    in_staging = source == staging or staging in source.parents
    owned = root.resolve()
    if not in_staging and (source == owned or owned in source.parents):
        # A folder the library already owns is referenced by the collection,
        # and moving it strands every one of those rows. Staging configured
        # inside the library root is still staging, so it is let through.
        raise refuse(
            "intake-list-unusable",
            f"{folder} is inside the library at {root} and outside download "
            f"staging, so its files are already owned and nothing was moved",
            origin=_ORIGIN,
            detail={"folder": str(folder), "root": str(root)},
        )
    resolved = target.resolve()
    if resolved == staging or staging in resolved.parents:
        raise refuse(
            "intake-staging-refused",
            f"{target} is under download staging at {staging}, so landing there "
            f"would move nothing out of it",
            origin=_ORIGIN,
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
            origin=_ORIGIN,
            detail={"folder": str(folder), "target": str(target)},
        )


def _check_export(
    export: Path,
    destination: Path,
    registry: tree_registry.Registry,
    label_rows: tuple[listdoc.ManifestRow, ...] = (),
) -> None:
    """Every refusal ``place_files`` can make about the export, made on a copy.

    Here, before any move, because the same refusal after the moves leaves a
    batch in the library with no intake file. The tree writer's refusals are
    asked of the same copy, after the intake playlist is in it, which is the
    document the writer will actually be handed.
    """
    if not export.is_file():
        raise refuse(
            "library-export-unusable",
            f"no Fresh Export at {export}, so nothing was moved",
            steps=("export the collection again from rekordbox and pass that file",),
            origin=_ORIGIN,
        )
    trial = bytearray(export.read_bytes())
    collection_xml.splice_tracks(trial, [])
    tree = rbxml.intake_tree(taxonomy.default_taxonomy(), registry)
    error = rbxml.insert_intake_playlist(trial, destination.stem, [], tree=tree)
    if error:
        raise refuse(
            "library-export-unusable",
            f"the intake playlist could not be written ({error}), so nothing "
            f"was moved",
            steps=(
                "export the collection again from rekordbox so the intake "
                "folder is present, then retry",
            ),
            origin=_ORIGIN,
        )
    # EVERY label and year the manifest names, not only the ones that will
    # land, because which rows land is known only once the batch folder can be
    # indexed, and that is after the moves. So an export holding two folders of
    # a label this batch does not carry still refuses here. Nothing has moved
    # and what it says is true of the export. R-455.
    catalog: dict[str, set[int]] = {}
    for row in label_rows:
        name, year = _label_of(row), row.provenance.year
        if name and year is not None:
            catalog.setdefault(name, set()).add(year)
    try:
        trees.check_record_labels_tree(bytes(trial), catalog, registry=registry)
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
                origin=_ORIGIN,
                detail=detail,
                inner=exc.cause,
            ) from exc
        # The writer has one reason for every layout it will not write into,
        # and it is the one for a defect, because the writer cannot know whose
        # document it was handed. Here it is known: a Fresh Export the person
        # took, holding a label folder twice or a node this product will not
        # write inside, which they mend in rekordbox and export again.
        raise refuse(
            "library-export-unusable",
            said,
            steps=(
                "in rekordbox, under the record labels folder, remove or merge "
                "the folder or playlist the message names",
                "export the collection again and pass that file",
            ),
            origin=_ORIGIN,
            detail=detail,
            inner=exc.cause,
        ) from exc


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

    THE BYTES ARE READ ONCE and both the fingerprint and the rows come from
    that one read. The verb shows the person a plan made from these rows and
    hands the fingerprint back to :func:`apply`, which reads the file again
    and refuses if it is not the same bytes. Fingerprinting one read and
    parsing another let a manifest rewritten in between file tracks under
    labels nobody was shown.
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
            origin=_ORIGIN,
            detail={"manifest": str(manifest)},
        ) from exc
    try:
        rows = listdoc.manifest_rows(raw, manifest)
    except listdoc.ListDocRefused as exc:
        raise refuse(
            "intake-list-unusable",
            f"{exc}, so nothing was moved",
            steps=steps,
            origin=_ORIGIN,
            detail={"manifest": str(manifest)},
        ) from exc
    return LabelManifest(
        path=manifest,
        digest=hashlib.sha256(raw).hexdigest(),
        rows=tuple(row for row in rows if row.provenance.source == LABEL_SOURCE),
    )


def _never_suppressed(_recording: str, _address: object) -> bool:
    """No tombstone is consulted, and that is the right answer HERE only.

    ``resolve_one`` asks the tombstones last, immediately before calling a row
    missing. A row this engine cannot tie to a landed file is reported the same
    way whether somebody once deleted the track or not, so the store would
    change no answer, and opening it would make a landing depend on it.
    """
    return False


def _no_suppression_id(_recording: str, _address: object) -> str:
    return ""


def _unlabelled(row: listdoc.ManifestRow, reason: str, because: str) -> Unlabelled:
    artist = str(row.track.get("artist", ""))
    title = str(row.track.get("title", ""))
    version = str(row.track.get("version", ""))
    spelled = f"{artist} - {title}" + (f" ({version})" if version else "")
    label = _label_of(row)
    return Unlabelled(
        ref=row.ref,
        artist=artist,
        title=title,
        label=label,
        year=row.provenance.year,
        reason=reason,
        sentence=f"{spelled} was filed under no label playlist by this run, because {because}",
    )


#: A label's years, and under each the rows filed there with their track ids.
_Filed = dict[str, dict[int, list[tuple[listdoc.ManifestRow, list[int]]]]]


def _file_labels(
    label_rows: tuple[listdoc.ManifestRow, ...],
    placed: list[PlacedTrack],
    batch_dir: Path,
    template: NameTemplate,
) -> tuple[_Filed, list[Unlabelled]]:
    """Each label row tied to the track ids of the files this call landed.

    THE INDEX IS OF THE BATCH FOLDER ONLY. Against the whole library a row
    would resolve to a copy held for years, which this intake file never gave
    an id, and a label playlist naming no id is a row that silently vanished.
    A batch folder landed into twice still holds the first landing's files, so
    a matched path is looked up among THIS call's placed tracks and a path that
    is not there is an unmatched row, said by name.

    ``template`` is the library's own, lossy marker included, which is
    ``match_cli.library_view``'s one builder rule: read with the bare default, a
    marked lossy file with a missing tag folds to another recording here and to
    the right one in ``acquire match``.
    """
    ids = {item.path.resolve(): item.track_id for item in placed}
    index = match.index_library(batch_dir, template=template)
    filed: _Filed = {}
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
            wanted,
            index,
            suppresses=_never_suppressed,
            suppression_id=_no_suppression_id,
        )
        if found.state is match.MatchState.NEEDS_REVIEW:
            # A different version, or a title that merely resembles. Filing it
            # would be this engine answering a question only a person may.
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
            # TRUE OF BOTH ROWS IT IS SAID ABOUT. A row whose download never
            # arrived and a row an earlier landing already filed look the same
            # from inside one batch folder, so the sentence claims neither that
            # a file landed nor that the track is filed nowhere. R-457.
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
    registry: tree_registry.Registry,
    label_rows: tuple[listdoc.ManifestRow, ...],
    placed: list[PlacedTrack],
    batch_dir: Path,
) -> tuple[list[Labelled], list[Unlabelled]]:
    """Write every label the batch carries into the intake file, and say which.

    A TREE THAT CANNOT BE WRITTEN IS REPORTED, NOT RAISED, and the intake file
    stays. By now the files are in the library, the intake file names every one
    of them and ``place_files`` has recorded a routing intent for each. Taking
    the file back would leave those intents pointing at rows nothing will ever
    import, to protect a tree the person can live without for one import. The
    writer makes one atomic replace for every label together, so what is there
    after a failure is the file as the splice left it, whole and importable.
    What the writer itself refuses was asked of a copy before the first move,
    and the registry was read then too, so what arrives here should be a disk
    that refused. Nothing below reads anything it could have read earlier.
    R-456.
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
        # One album per year, because the manifest says which release a row
        # came from and the playlist does not: the writer dedupes across the
        # whole year either way. The intake file is read and replaced. It is
        # this call's own product and nobody has imported it, so the writer's
        # rule against writing over a Fresh Export is not in play.
        trees.insert_record_labels_trees(
            destination,
            {
                label: {year: [{"track_ids": ids}] for year, ids in by_year.items()}
                for label, by_year in years.items()
            },
            destination,
            registry=registry,
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


def _unplaceable(path: Path) -> Refused | None:
    """A file ``place_files`` would refuse, asked of its tags before it moves."""
    meta = {
        "genre": tags.read_genre_from_file(path) or "",
        "energy": tags.read_energy_from_file(path),
    }
    if ingest.decide_placement(meta) is not None:
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
    try:
        folder.rmdir()
    except OSError:
        pass


def _moved_detail(moved: list[Moved], refused: list[Refused]) -> dict:
    return {
        "moved": [str(item.target) for item in moved],
        "refused": [str(item.path) for item in refused],
    }


def _moved_sentence(moved: list[Moved]) -> str:
    if not moved:
        return "nothing was moved"
    names = ", ".join(item.target.name for item in moved)
    return (
        f"{len(moved)} file(s) were already moved into the library and stay "
        f"there: {names}"
    )


def _reason_for(exc: OSError) -> str:
    if isinstance(exc, PermissionError):
        return "path-permission-denied"
    return "intake-list-unusable"


def apply(
    plan: Plan,
    *,
    cfg: config.Config,
    export: Path,
    destination: Path,
    manifest: Path | None = None,
    manifest_digest: str | None = None,
) -> Landed:
    """Move the planned files into the library, then write one intake file.

    ``manifest`` is the provenance sidecar of the list the batch was acquired
    from. With one, its label rows are filed under the catalog tree in the same
    intake file. Without one, nothing is, and nothing about a label is asked.
    ``manifest_digest`` is the fingerprint :func:`read_label_manifest` gave the
    caller that showed somebody a plan. The file is read again here, and bytes
    that are not the ones that were shown refuse as stale with nothing moved,
    which is what the folder's own digest does for the files.
    """
    items = _list(plan.folder) if plan.folder.is_dir() else ()
    if items != plan.items or _digest(items) != plan.digest:
        raise refuse(
            "decision-stale",
            f"{plan.folder} changed after it was planned, so nothing was moved",
            origin=_ORIGIN,
            detail={"folder": str(plan.folder)},
        )
    target = target_dir(cfg, plan.batch)
    _check_batch(plan.batch)
    _check_library(cfg, plan.folder, target)
    if destination.exists():
        raise refuse(
            "output-exists",
            f"{destination} already exists and is never overwritten, so nothing "
            f"was moved",
            origin=_ORIGIN,
            detail={"path": str(destination)},
        )
    label_rows: tuple[listdoc.ManifestRow, ...] = ()
    if manifest is not None:
        read = read_label_manifest(manifest)
        if manifest_digest is not None and read.digest != manifest_digest:
            raise refuse(
                "decision-stale",
                f"{manifest} changed after it was planned, so nothing was moved",
                origin=_ORIGIN,
                detail={"manifest": str(manifest)},
            )
        label_rows = read.rows
    # READ ONCE, BEFORE THE FIRST MOVE, and handed to both the check and the
    # write. A registry that cannot be read refuses here, with nothing moved,
    # and cannot refuse after the moves because nothing reads it again.
    registry = tree_registry.read(cfg)
    _check_export(export, destination, registry, label_rows)

    refused: list[Refused] = []
    movable: list[Path] = []
    for item in plan.items:
        blocked = _unplaceable(item) or _occupied(item, target / item.name)
        if blocked is not None:
            refused.append(blocked)
        else:
            movable.append(item)
    if not movable:
        # Before the batch folder is made, so a batch where nothing lands
        # leaves nothing in the library, not even an empty folder.
        raise refuse(
            "intake-list-unusable",
            f"no file in {plan.folder} could land, so nothing was moved and no "
            f"intake file was written: "
            + "; ".join(entry.sentence for entry in refused),
            origin=_ORIGIN,
            detail=_moved_detail([], refused),
        )

    made = not target.exists()
    target.mkdir(parents=True, exist_ok=True)
    moved: list[Moved] = []
    for item in movable:
        final = target / item.name
        # Asked again at the move, not only in the pass above. Between the
        # two a file of that name can arrive, and os.replace would take its
        # place without a word. The window after THIS check is closed by the
        # caller holding ``batch_lock``, not here (R-432).
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
                _reason_for(exc),
                f"{item.name} could not be moved to {final} ({exc.strerror or exc}); "
                f"no intake file was written and {_moved_sentence(moved)}",
                origin=_ORIGIN,
                detail=_moved_detail(moved, refused),
            ) from exc
        moved.append(Moved(source=item, target=final))

    if not moved:
        if made:
            _remove_if_empty(target)
        raise refuse(
            "intake-list-unusable",
            f"no file in {plan.folder} could land, so nothing was moved and no "
            f"intake file was written: "
            + "; ".join(entry.sentence for entry in refused),
            origin=_ORIGIN,
            detail=_moved_detail(moved, refused),
        )

    try:
        placed = ingest.place_files(
            [item.target for item in moved],
            cfg=cfg,
            export=export,
            destination=destination,
        )
    except Exception as exc:
        # ``place_files`` writes the intake file before it records the routing
        # intents, so a refusal from the ledger arrives after the write. The
        # file was checked absent above, so the one there now is this call's.
        destination.unlink(missing_ok=True)
        inner = exc.cause if isinstance(exc, CratekitError) else None
        raise refuse(
            exc.cause.reason if isinstance(exc, CratekitError) else "internal-error",
            f"the intake file could not be written ({exc}); none was left "
            f"behind and {_moved_sentence(moved)}",
            origin=_ORIGIN,
            detail=_moved_detail(moved, refused),
            inner=inner,
        ) from exc

    labelled, unlabelled = _label(cfg, destination, registry, label_rows, placed, target)
    return Landed(
        destination=destination,
        placed=tuple(placed),
        moved=tuple(moved),
        refused=tuple(refused),
        labelled=tuple(labelled),
        unlabelled=tuple(unlabelled),
    )
