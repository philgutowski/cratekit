"""The one writer of the list document ``acquire download`` reads.

R-400: every acquisition entrance in this product resolves work and then stops,
because nothing wrote the file the download verb reads. The only writer of the
format was a test helper. This module is the writer, and there is ONE of it on
purpose: the reader, :func:`cratekit.acquire.match_cli.read_list`, is a single
closed and versioned format, so a document per source would be five writers
drifting from one reader, and a fix round would repair one of them and leave
the other four.

WHAT IT WRITES, and why the two files are two.

``<name>.list.json`` is the list document, ``{"list": 1, "origin": "tidal",
"tracks": [...]}``, and carries nothing the reader does not read. The reader
refuses an unknown top level key, so provenance cannot ride along in it.

``<name>.manifest.json`` is the provenance sidecar: which source, playlist,
label and year each listed id came from. Nothing reads it to acquire, which is
the point: it answers "why is this in the list" without the list's closed format
having to know the question exists.

THE EMITTER IS STRICTER THAN THE READER, NEVER LOOSER. The reader refuses the
WHOLE document over one row it cannot recognise, so a row this module let
through would cost every other row in the list. Every listed row is therefore
read back through the reader's own row recognition before anything is written,
and refused here by position if the reader would refuse it there.

A row without a provider identifier is not written to the provider document at
all. It comes back in ``unlisted``, because the download verb refuses a list
holding one such row, and a list that quietly dropped it would report every
item done over a list it did not finish.

The emitter writes a file and stops. Nothing here composes ``acquire download``,
so nothing here can spend a download.
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

#: The version of the provenance sidecar. Nothing reads the sidecar yet, so
#: nothing refuses an unknown version of it; a reader, when one lands, should
#: refuse the way ``read_list`` refuses the list's own.
MANIFEST_VERSION = 1


class ListDocRefused(ValueError):
    """A list this module will not write, and nothing was written.

    A plain exception rather than a structured cause, for the reason
    :class:`match.UnreadableList` gives: the verb that calls this converts it,
    in the one place allowed to know what a remediation looks like.
    """

    def __init__(self, message: str, *, position: int | None = None) -> None:
        super().__init__(message)
        self.position = position


@dataclass(frozen=True, slots=True)
class Row:
    """One track a source resolved, in the shape the provider's own rows use.

    ``title`` is the title AS THE SOURCE SPELLED IT, a version embedded in it or
    not, and ``version`` is a version the source declared in its own field. The
    reader reads both conventions, and writing what the source said rather than
    something recomposed is what keeps the re-read identical.
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

    ``source_ref`` is the reference the listed row was taken from, and
    ``source_refs`` is every reference that asked for the same id, in order. A
    list built from several jobs writes one row per id, first source wins, and
    without the second field the other playlists that wanted the track would
    vanish from the record. Left empty, it is ``source_ref`` alone.

    THE MANIFEST CARRIES ``source_refs`` ONLY WHEN THERE IS MORE THAN ONE. A
    manifest this module wrote before the field existed is compared byte for
    byte on the next identical write, and a key added to every entry would
    turn that harmless repeat into a refusal. An entry without the key came
    from its ``source_ref`` alone.
    """

    source: str
    source_ref: str | None = None
    label_id: str | None = None
    label_name: str | None = None
    year: int | None = None
    release_id: str | None = None
    source_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Written:
    """What :func:`write` did.

    Both paths are ``None`` when nothing was listable and nothing was written,
    which is how an empty result says so rather than leaving an empty document
    somebody would read as a list that was all owned.
    """

    list_path: Path | None
    manifest_path: Path | None
    listed: tuple[str, ...]
    unlisted: tuple[Row, ...]


# ---------------------------------------------------------------------------
# Rows
# ---------------------------------------------------------------------------


def _reads_back(title: str, version: str, wanted: match.Wanted) -> bool:
    """Whether a row spelled this way re-reads to ``wanted``'s version.

    THE VERSION TOKEN IS THE ONLY THING COMPARED, and that is measured rather
    than assumed. Both spellings :func:`_spellings` offers re-read to the same
    matching title and the same addressed title by construction: the source's
    own spelling read with no declared version is its own address, and the raw
    title read with the declared version recomposes to exactly ``spelled``.
    Mutation rows W3 and W5 removed a title and an address comparison here and
    neither killed a test in the full suite, see ``docs/mutation/u68-notes.md``.
    What CAN differ is the version: a raw title that carried its own bracketed
    version beside a declared one re-reads, spelled together, as both.
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

    The source's own spelling, version embedded. Then, for a row that declared
    its version in its own field, the row's raw title and that version: the
    reader composed ``spelled`` as ``<raw> (<version>)``, so the suffix comes
    off and the pair re-reads to the same composition. Writing the ALREADY
    SPLIT title instead drops every other bracketed part and every featured
    credit the raw title carried, which is what this module did first.
    """
    found: list[tuple[str, str]] = []
    if wanted.spelled:
        found.append((wanted.spelled, ""))
        suffix = f" ({wanted.version})"
        if wanted.version and wanted.spelled.endswith(suffix):
            found.append((wanted.spelled[: -len(suffix)], wanted.version))
    return found


def _row_of_wanted(wanted: match.Wanted) -> Row:
    # ONLY THE PROVIDER'S OWN IDENTIFIER IS A PROVIDER IDENTIFIER. A row from
    # another service carries that service's id in ``ref``, and written into a
    # provider document it would ask the provider for a different track, or for
    # none. Such a row is returned with no ref, so it lands in ``unlisted``.
    ref = wanted.ref if wanted.origin == match.TIDAL else ""
    # The first spelling that re-reads to the same addressed track. A ``Wanted``
    # built by hand carries no spelling, and then its title and version are all
    # there is to write.
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
    """Rows from what the product already holds: read tracks, or frozen ones.

    A MAPPING is :func:`cratekit.acquire.cli.frozen_tracks`'s output, keyed by
    the provider identifier and carrying artist, title and isrc. Anything else
    is read as ``Wanted`` tracks, in order.

    A FROZEN MAPPING IS A DOWNLOAD LIST AND NOTHING MORE. The freeze kept the
    split title and dropped the version, the key and the source's spelling, so a
    list written from it freezes back identically and re-reads to the PLAIN
    record for anything that matches or tombstones by title. Write from the
    ``Wanted`` tracks whenever they are still held.
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
    """Refuse a track the reader would refuse, by the reader's own rule.

    The reader's rule and not a copy of it: a title of ``(Extended)`` is not
    empty, and the reader still refuses it, because what is left once the
    version comes off is. A copied check would pass that row and cost the list.
    """
    try:
        match.read_row(track, origin=match.TIDAL, position=position)
    except match.UnreadableList as exc:
        raise ListDocRefused(
            f"row {position} would make the whole list unreadable: {exc}",
            position=position,
        ) from exc


def document(rows: Iterable[Row]) -> tuple[dict[str, Any], tuple[str, ...], tuple[Row, ...]]:
    """The list document, the ids it lists in order, and the rows it could not.

    THE SAME IDENTIFIER TWICE IS WRITTEN ONCE, first occurrence wins, which is
    what :func:`cratekit.acquire.cli.frozen_tracks` does on the way back in. An
    identifier is compared stripped, because the reader strips it.
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


# ---------------------------------------------------------------------------
# The files
# ---------------------------------------------------------------------------


def _encoded(body: Mapping[str, Any]) -> bytes:
    # Deterministic, so writing the same list twice is the same bytes twice and
    # the second write is recognised as a no-op rather than refused.
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

    A file holding anything else is refused: a list of the same name somebody
    else wrote, or this product wrote from different work, is not this module's
    to replace.
    """
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
) -> Written:
    """Write ``<name>.list.json`` and its manifest into ``directory``, or nothing.

    EVERY CHECK BEFORE EITHER WRITE. A refused row, a missing provenance and an
    existing file holding something else all refuse with nothing written, so a
    refusal never leaves one half of the pair behind. The manifest is written
    first, so a list on disk always has its provenance beside it; a crash
    between the two leaves a manifest the next identical write completes.
    """
    name = _checked_name(name)
    body, listed, unlisted = document(rows)
    if not listed:
        return Written(None, None, (), unlisted)
    list_path = Path(directory) / f"{name}{LIST_SUFFIX}"
    manifest_path = Path(directory) / f"{name}{MANIFEST_SUFFIX}"
    list_bytes = _encoded(body)
    manifest_bytes = _encoded(manifest(list_path.name, body, provenance))
    pending = [
        (path, payload)
        for path, payload in ((manifest_path, manifest_bytes), (list_path, list_bytes))
        if not _unchanged(path, payload)
    ]
    for path, payload in pending:
        config.atomic_write_bytes(payload, path)
    return Written(list_path, manifest_path, listed, unlisted)
