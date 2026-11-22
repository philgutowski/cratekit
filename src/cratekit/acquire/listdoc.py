"""The one writer of the list document ``acquire download`` reads (R-400).

One writer, since :func:`cratekit.acquire.match_cli.read_list` reads one closed
format. ``<name>.list.json`` carries only what the reader reads,
``<name>.manifest.json`` the provenance per id, and ``<name>.unlisted.json`` the
rows handed on as a text list (U78). Every row is read back through the reader
before anything is written, since the reader refuses a whole document over one
row; a row without a provider id comes back in ``unlisted``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from cratekit.acquire import match
from cratekit.acquire.match_cli import LIST_VERSION
from cratekit.core import config

#: The two file names a list called ``name`` occupies.
LIST_SUFFIX = ".list.json"
MANIFEST_SUFFIX = ".manifest.json"

#: The third, the text list of the rows the provider cannot name exactly (U78).
UNLISTED_SUFFIX = ".unlisted.json"

#: The provenance sidecar version. :func:`read_manifest` refuses any other, so
#: raise it only with a reader for the version it leaves behind.
MANIFEST_VERSION = 1


class ListDocRefused(ValueError):
    """A list this module will not write, and nothing was written. The calling
    verb converts it to a cause."""

    def __init__(self, message: str, *, position: int | None = None) -> None:
        super().__init__(message)
        self.position = position


@dataclass(frozen=True, slots=True)
class Row:
    """One track a source resolved, in the shape the provider's own rows use.

    ``title`` is as the source spelled it and ``version`` is the source's own
    field, so the re-read is identical.
    """

    ref: str
    artist: str
    title: str
    version: str = ""
    isrc: str | None = None
    key: str | None = None


@dataclass(frozen=True, slots=True)
class Provenance:
    """Where a listed id came from. None of it is read to acquire anything.

    ``source_refs`` is every reference that asked for the id, in order; empty
    means ``source_ref`` alone. The manifest writes it only when there is more
    than one, so an older manifest still compares byte for byte.
    """

    source: str
    source_ref: str | None = None
    label_id: str | None = None
    label_name: str | None = None
    year: int | None = None
    release_id: str | None = None
    source_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class HandedOn:
    """A row the provider cannot name exactly, and why (U78). Written to the
    text list, the reason as a ``#`` row above it."""

    row: Row
    reason: str


@dataclass(frozen=True, slots=True)
class Written:
    """What :func:`write` did. A path is ``None`` when its file was not written,
    so an empty result leaves no empty document."""

    list_path: Path | None
    manifest_path: Path | None
    listed: tuple[str, ...]
    unlisted: tuple[Row, ...]
    unlisted_path: Path | None = None


# ---------------------------------------------------------------------------
# Rows
# ---------------------------------------------------------------------------


def _reads_back(title: str, version: str, wanted: match.Wanted) -> bool:
    """Whether a row spelled this way re-reads to ``wanted``'s version.

    Only the version is compared: both spellings re-read to the same title by
    construction (``docs/mutation/u68-notes.md``).
    """
    try:
        again = match.read_row(
            {"title": title, "version": version, "artist": wanted.artist},
            origin=match.TIDAL,
            position=1,
        )
    except match.UnreadableList:
        return False
    return again.version_key == wanted.version_key


def _spellings(wanted: match.Wanted) -> list[tuple[str, str]]:
    """The (title, version) pairs that might re-read to ``wanted``, best first.

    The source's own spelling, then the raw title and declared version, never
    the split title, which loses brackets and featured credits.
    """
    found: list[tuple[str, str]] = []
    if wanted.spelled:
        found.append((wanted.spelled, ""))
        suffix = f" ({wanted.version})"
        if wanted.version and wanted.spelled.endswith(suffix):
            found.append((wanted.spelled[: -len(suffix)], wanted.version))
    return found


def _row_of_wanted(wanted: match.Wanted) -> Row:
    # Another service's id is not a provider id, so such a row lands in unlisted.
    ref = wanted.ref if wanted.origin == match.TIDAL else ""
    # The first spelling that re-reads to the same track, else title and version.
    title, version = next(
        (pair for pair in _spellings(wanted) if _reads_back(*pair, wanted)),
        (wanted.title, wanted.version),
    )
    return Row(
        ref=ref,
        artist=wanted.artist,
        title=title,
        version=version,
        isrc=wanted.isrc,
        key=wanted.key,
    )


def rows_of(
    source: Iterable[match.Wanted] | Mapping[str, Mapping[str, Any]],
) -> tuple[Row, ...]:
    """Rows from read ``Wanted`` tracks, or from a frozen mapping.

    A mapping is :func:`cratekit.acquire.cli.frozen_tracks`'s output and lost the
    version and spelling, so it serves only as a download list; prefer the
    ``Wanted`` tracks when held.
    """
    if isinstance(source, Mapping):
        return tuple(
            Row(
                ref=str(ref),
                artist=str(fields.get("artist") or ""),
                title=str(fields.get("title") or ""),
                isrc=fields.get("isrc") or None,
            )
            for ref, fields in source.items()
        )
    return tuple(_row_of_wanted(wanted) for wanted in source)


# ---------------------------------------------------------------------------
# The document
# ---------------------------------------------------------------------------


def _track(row: Row, ref: str) -> dict[str, Any]:
    track: dict[str, Any] = {"id": ref, "title": row.title.strip(), "artist": row.artist.strip()}
    if row.version.strip():
        track["version"] = row.version.strip()
    if row.isrc and row.isrc.strip():
        track["isrc"] = row.isrc.strip()
    if row.key and row.key.strip():
        track["key"] = row.key.strip()
    return track


def _checked(track: dict[str, Any], position: int) -> None:
    """Refuse a track the reader would refuse, by the reader's own rule, not a copy."""
    try:
        match.read_row(track, origin=match.TIDAL, position=position)
    except match.UnreadableList as exc:
        raise ListDocRefused(
            f"row {position} would make the whole list unreadable: {exc}",
            position=position,
        ) from exc


def document(rows: Iterable[Row]) -> tuple[dict[str, Any], tuple[str, ...], tuple[Row, ...]]:
    """The list document, the ids it lists in order, and the rows it could not.

    An id is written once, first wins, compared stripped as the reader strips it.
    """
    tracks: list[dict[str, Any]] = []
    listed: list[str] = []
    unlisted: list[Row] = []
    seen: set[str] = set()
    for position, row in enumerate(rows, start=1):
        ref = str(row.ref or "").strip()
        if not ref:
            unlisted.append(row)
            continue
        track = _track(row, ref)
        _checked(track, position)
        if ref in seen:
            continue
        seen.add(ref)
        listed.append(ref)
        tracks.append(track)
    body = {"list": LIST_VERSION, "origin": match.TIDAL, "tracks": tracks}
    return body, tuple(listed), tuple(unlisted)


#: The separator the text reader splits a line on.
_SEPARATOR = " - "


def _line(row: Row) -> str:
    title = row.title.strip()
    if row.version.strip():
        title = f"{title} ({row.version.strip()})"
    return f"{row.artist.strip()}{_SEPARATOR}{title}"


def text_line(row: Row) -> str:
    """The ``Artist - Title`` line for one row, or a refusal if it re-reads wrong.

    Read back by the text reader, since a separator in the artist, a leading
    ordinal or a leading ``#`` would match the wrong track rather than refuse.
    """
    line = _line(row)
    try:
        wanted = match.read_row(
            {"artist": row.artist, "title": row.title, "version": row.version},
            origin=match.TIDAL,
            position=1,
        )
        again = match.read_text_rows([line])
    except match.UnreadableList as exc:
        raise ListDocRefused(f"{line!r} cannot be written as a text line: {exc}") from exc
    if len(again) != 1 or (again[0].recording, again[0].version_key) != (
        wanted.recording,
        wanted.version_key,
    ):
        raise ListDocRefused(f"{line!r} would read back as another track, or as none")
    return line


def text_document(handed_on: Iterable[HandedOn]) -> dict[str, Any]:
    """The text list document for the rows handed on, reasons as ``#`` rows.

    A line is written once, first reason wins; a refused row refuses by position.
    """
    tracks: list[str] = []
    seen: set[str] = set()
    for position, entry in enumerate(handed_on, start=1):
        try:
            line = text_line(entry.row)
        except ListDocRefused as exc:
            raise ListDocRefused(f"handed on row {position}: {exc}", position=position) from exc
        if line in seen:
            continue
        seen.add(line)
        tracks.extend((f"# {' '.join(str(entry.reason).split())}", line))
    return {"list": LIST_VERSION, "origin": match.TEXT, "tracks": tracks}


# ---------------------------------------------------------------------------
# The files
# ---------------------------------------------------------------------------


def _encoded(body: Mapping[str, Any]) -> bytes:
    # Deterministic, so an identical second write is a no-op rather than refused.
    return (json.dumps(body, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _checked_name(name: str) -> str:
    """One plain file name component, or a refusal before any path is built."""
    if (
        not isinstance(name, str)
        or not name.strip()
        or name != name.strip()
        or name in {".", ".."}
        or "/" in name
        or "\\" in name
        or "\x00" in name
    ):
        raise ListDocRefused(f"{name!r} is not a list name this module can write")
    return name


def _provenance_for(
    provenance: Provenance | Mapping[str, Provenance], ref: str
) -> Provenance:
    found = provenance if isinstance(provenance, Provenance) else provenance.get(ref)
    if found is None:
        raise ListDocRefused(f"no provenance was given for listed id {ref!r}")
    if not isinstance(found.source, str) or not found.source.strip():
        raise ListDocRefused(f"the provenance of listed id {ref!r} names no source")
    return found


def manifest(
    list_name: str,
    body: Mapping[str, Any],
    provenance: Provenance | Mapping[str, Provenance],
) -> dict[str, Any]:
    """The provenance sidecar for a list document, one entry per listed id."""
    entries: dict[str, dict[str, Any]] = {}
    for track in body["tracks"]:
        origin = _provenance_for(provenance, track["id"])
        entry = entries[track["id"]] = {
            "source": origin.source,
            "source_ref": origin.source_ref,
            "label_id": origin.label_id,
            "label_name": origin.label_name,
            "year": origin.year,
            "release_id": origin.release_id,
            "artist": track["artist"],
            "title": track["title"],
            "version": track.get("version", ""),
            "isrc": track.get("isrc"),
        }
        if len(origin.source_refs) > 1:
            entry["source_refs"] = list(origin.source_refs)
    return {"manifest": MANIFEST_VERSION, "list": list_name, "rows": entries}


def _unchanged(path: Path, payload: bytes) -> bool:
    """True when ``path`` already holds ``payload``, False when it is absent.
    Anything else is refused, not replaced."""
    try:
        present = path.read_bytes()
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise ListDocRefused(f"{path} exists and could not be read: {exc.strerror}") from exc
    if present != payload:
        raise ListDocRefused(
            f"{path} already exists and holds something else; it is left as it is"
        )
    return True


def write(
    directory: Path,
    name: str,
    rows: Iterable[Row],
    provenance: Provenance | Mapping[str, Provenance],
    *,
    handed_on: Iterable[HandedOn] = (),
) -> Written:
    """Write ``<name>.list.json`` and its manifest into ``directory``, or nothing.

    Every check runs before any write. The manifest is written first, so a list
    always has its provenance beside it; ``handed_on`` rows go last, to
    ``<name>.unlisted.json``.
    """
    name = _checked_name(name)
    body, listed, unlisted = document(rows)
    handed = tuple(handed_on)
    files: list[tuple[Path, bytes]] = []
    list_path = manifest_path = unlisted_path = None
    if listed:
        list_path = Path(directory) / f"{name}{LIST_SUFFIX}"
        manifest_path = Path(directory) / f"{name}{MANIFEST_SUFFIX}"
        files.append((manifest_path, _encoded(manifest(list_path.name, body, provenance))))
        files.append((list_path, _encoded(body)))
    if handed:
        unlisted_path = Path(directory) / f"{name}{UNLISTED_SUFFIX}"
        files.append((unlisted_path, _encoded(text_document(handed))))
    pending = [(path, payload) for path, payload in files if not _unchanged(path, payload)]
    for path, payload in pending:
        config.atomic_write_bytes(payload, path)
    return Written(list_path, manifest_path, listed, unlisted, unlisted_path)


# ---------------------------------------------------------------------------
# Reading the manifest back
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ManifestRow:
    """One manifest entry: the listed id, its provenance, and ``track`` in the
    list document's shape for :func:`match.read_row`."""

    ref: str
    provenance: Provenance
    track: Mapping[str, Any]


def _text_or_none(entry: Mapping[str, Any], key: str, ref: str) -> str | None:
    value = entry.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ListDocRefused(f"manifest entry {ref!r} carries a {key} that is not text")
    return value


def _manifest_row(ref: str, entry: object) -> ManifestRow:
    if not isinstance(entry, Mapping):
        raise ListDocRefused(f"manifest entry {ref!r} is not an object")
    source = entry.get("source")
    if not isinstance(source, str) or not source.strip():
        raise ListDocRefused(f"manifest entry {ref!r} names no source")
    year = entry.get("year")
    # ``bool`` is an ``int`` to Python, and a year of ``true`` is not a year.
    if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
        raise ListDocRefused(f"manifest entry {ref!r} carries a year that is not a number")
    track: dict[str, Any] = {
        "id": ref,
        "artist": _text_or_none(entry, "artist", ref) or "",
        "title": _text_or_none(entry, "title", ref) or "",
        "version": _text_or_none(entry, "version", ref) or "",
    }
    isrc = _text_or_none(entry, "isrc", ref)
    if isrc:
        track["isrc"] = isrc
    # Present only when more than one source asked, read back as written.
    asked = entry.get("source_refs", [])
    if not isinstance(asked, list) or not all(isinstance(one, str) for one in asked):
        raise ListDocRefused(f"manifest entry {ref!r} carries source_refs that are not text")
    return ManifestRow(
        ref=ref,
        provenance=Provenance(
            source=source,
            source_ref=_text_or_none(entry, "source_ref", ref),
            label_id=_text_or_none(entry, "label_id", ref),
            label_name=_text_or_none(entry, "label_name", ref),
            year=year,
            release_id=_text_or_none(entry, "release_id", ref),
            source_refs=tuple(asked),
        ),
        track=track,
    )


def read_manifest(path: Path) -> tuple[ManifestRow, ...]:
    """Every entry of a provenance sidecar, in the order it was written.

    Another version, or a file that is not a manifest, is refused whole.
    """
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise ListDocRefused(
            f"the manifest {path} could not be read: {exc.strerror or exc}"
        ) from exc
    return manifest_rows(raw, path)


def manifest_rows(raw: bytes, path: Path | str) -> tuple[ManifestRow, ...]:
    """:func:`read_manifest` over bytes already held, for a caller that
    fingerprinted them. ``path`` only names the file in refusals."""
    try:
        body = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ListDocRefused(f"the manifest {path} is not JSON: {exc}") from exc
    if not isinstance(body, Mapping) or "manifest" not in body:
        raise ListDocRefused(
            f"{path} is not a manifest; pass the file ending in {MANIFEST_SUFFIX} "
            f"that was written beside the list"
        )
    version = body["manifest"]
    if isinstance(version, bool) or version != MANIFEST_VERSION:
        raise ListDocRefused(
            f"the manifest {path} is version {version!r} and this build reads "
            f"version {MANIFEST_VERSION}"
        )
    rows = body.get("rows")
    if not isinstance(rows, Mapping):
        raise ListDocRefused(f"the manifest {path} carries no rows object")
    return tuple(_manifest_row(str(ref), entry) for ref, entry in rows.items())
