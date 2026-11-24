"""The one container-correct audio tag reader and writer.

Audio files are the user's irreplaceable data and this module is the only place
in Cratekit that touches them, because wrong container dispatch does not raise,
it corrupts the file.

CONTAINERS. In AIFF (``FORM``) and WAV (``RIFF``) an ID3 tag is the payload of a
chunk the container's size fields account for. ``mutagen.id3.ID3.save(path)``
writes a bare ID3 stream at offset 0, which leaves those size fields describing
a layout that no longer exists, and stripping the tag does not recover the
audio. So every write opens through ``_open``, which picks the mutagen class
that knows its container: only a real ``.mp3`` takes a bare ID3 stream, and MP4
takes atoms. The per-container round-trip tests hash the decoded audio.

ONE TABLE (seam decision S5). Readers and writers are driven by the same
:data:`FIELDS` table through the same container classification, so they cannot
disagree about which key a field lives under.

NO TEMPO FIELD (R17). :data:`FIELDS` has no ``bpm`` key and no ``TBPM`` frame,
and every writer raises on a field name it does not know, so no code path leads
from the public surface to a tempo frame. The table stays a module constant
because a configurable field set would reopen that hole.

TWO READERS AND TWO WRITERS. :func:`read_tag` and :func:`write_tags` are the
convenient pair: single strings, stripped, an empty value read as absent.
:func:`read_tag_values` and :func:`write_tag_values` are the exact pair an undo
log needs (:mod:`cratekit.adopt.revert`), which keeps ``"House "`` apart from
``"House"``, ``""`` apart from absent, and every value of a multi-value field.

ID3v1 TRAILERS. mutagen's ID3 save rewrites an existing ID3v1 trailer from the
v2 frames, losing a v1 genre byte the revert ledger never recorded. So on a real
``.mp3`` the 128 byte trailer is captured before a save and written back in
place after it, only when one is there both before and after. WAV and AIFF keep
their ID3 in a chunk that may grow at the file's end, so they never take this.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Sequence

log = logging.getLogger(__name__)


_ISRC = re.compile(r"[A-Z]{2}[A-Z0-9]{3}[0-9]{7}")


def fold_isrc(value: object) -> str:
    """An ISRC spelling with its whitespace and hyphens dropped, upper cased.

    THE ONE FOLD (U212), so a hyphenated spelling and a bare one are one string.
    Not validated: :func:`isrc_token` says whether it is an ISRC at all.
    """
    return re.sub(r"[\s-]", "", str(value or "")).upper()


def isrc_token(value: object) -> str:
    """The folded ISRC as an identity, or ``""`` when the value is not one."""
    folded = fold_isrc(value)
    return folded if _ISRC.fullmatch(folded) else ""


class Dialect(Enum):
    """The tag DIALECT a container speaks, the one thing reader and writer classify by.

    The mutagen CLASS is a finer decision: WAV, AIFF and MP3 share a dialect but
    not a class.
    """

    VORBIS = "vorbis"
    MP4 = "mp4"
    ID3 = "id3"


@dataclass(frozen=True)
class TagSpec:
    """Where one logical field lives in each dialect."""

    vorbis: str  # Vorbis comment key, lowercase by convention
    id3: str  # an ID3 text frame such as "TIT2", or "TXXX:<Description>"
    mp4: str  # a native atom, or an "----:com.apple.iTunes:" freeform atom

    def key_for(self, dialect: Dialect) -> str:
        return getattr(self, dialect.value)


# Every logical field a caller may read or write. There is deliberately no
# tempo entry (R17); adding one is not a feature.
FIELDS: dict[str, TagSpec] = {
    "title": TagSpec("title", "TIT2", "\xa9nam"),
    "artist": TagSpec("artist", "TPE1", "\xa9ART"),
    "initialkey": TagSpec("initialkey", "TKEY", "----:com.apple.iTunes:INITIALKEY"),
    "genre": TagSpec("genre", "TCON", "\xa9gen"),
    "energylevel": TagSpec("energylevel", "TXXX:EnergyLevel", "----:com.apple.iTunes:EnergyLevel"),
    "inizio": TagSpec("inizio", "TXXX:INIZIO", "----:com.apple.iTunes:INIZIO"),
    "voxlevel": TagSpec("voxlevel", "TXXX:VoxLevel", "----:com.apple.iTunes:VoxLevel"),
    "voxgender": TagSpec("voxgender", "TXXX:VoxGender", "----:com.apple.iTunes:VoxGender"),
    "voxgenderconf": TagSpec(
        "voxgenderconf", "TXXX:VoxGenderConf", "----:com.apple.iTunes:VoxGenderConf"
    ),
    # R-355, the recording's identity the outbound verbs match on.
    "isrc": TagSpec("isrc", "TSRC", "----:com.apple.iTunes:ISRC"),
    # R-572, read beside the ISRC to tell a single from its album cut.
    "album": TagSpec("album", "TALB", "\xa9alb"),
    # U156, read for its year to file a label's tracks under ``<Label> <year>``.
    "date": TagSpec("date", "TDRC", "\xa9day"),
    # U163, the album's own artist a native landing links the album row to.
    "albumartist": TagSpec("albumartist", "TPE2", "aART"),
    # U178, the keys MusicBrainz Picard writes; U177 measures which field
    # rekordbox shows as Label, and the entry moves here if it differs.
    "label": TagSpec("label", "TPUB", "----:com.apple.iTunes:LABEL"),
    # U240, the keys the vendored downloader writes. Nothing in Cratekit writes it.
    "copyright": TagSpec("copyright", "TCOP", "cprt"),
    # U157, the tempo's spread over the track and its verdict word. NEITHER IS A
    # TEMPO, so the table still has no tempo entry; ``core.drift`` says what each is.
    "driftlevel": TagSpec("driftlevel", "TXXX:DriftLevel", "----:com.apple.iTunes:DriftLevel"),
    "drift": TagSpec("drift", "TXXX:Drift", "----:com.apple.iTunes:Drift"),
    # U340, the second genre folder a track is filed into beside the one its
    # genre names. A genre word, never a tempo; ``routing.second_bucket`` reads it.
    "secondgenre": TagSpec(
        "secondgenre", "TXXX:SecondGenre", "----:com.apple.iTunes:SecondGenre"
    ),
    # U343, the mark ``analyze run`` writes on every file it measured, its
    # resume marker now that the run writes no head. A mark, never a tempo.
    "analyzed": TagSpec(
        "cratekitanalyzed", "TXXX:CratekitAnalyzed", "----:com.apple.iTunes:CratekitAnalyzed"
    ),
}

FLAC_SUFFIXES = (".flac",)
VORBIS_FILE_SUFFIXES = (".opus", ".ogg")
MP4_SUFFIXES = (".m4a", ".mp4", ".m4b")
WAVE_SUFFIXES = (".wav",)
AIFF_SUFFIXES = (".aiff", ".aif", ".aifc")
MP3_SUFFIXES = (".mp3",)

# Every container this module will touch, and its dialect. Exhaustive, with no
# fallthrough: an unknown suffix is refused, never guessed as ID3.
_DIALECT_BY_SUFFIX: dict[str, Dialect] = {
    **{s: Dialect.VORBIS for s in FLAC_SUFFIXES + VORBIS_FILE_SUFFIXES},
    **{s: Dialect.MP4 for s in MP4_SUFFIXES},
    **{s: Dialect.ID3 for s in WAVE_SUFFIXES + AIFF_SUFFIXES + MP3_SUFFIXES},
}

#: Every container suffix with verified handling, derived from the table above
#: so a container added there is never missing from a sweep (P3).
SUPPORTED_SUFFIXES: tuple[str, ...] = tuple(sorted(_DIALECT_BY_SUFFIX))


class UnsupportedContainer(ValueError):
    """A suffix with no verified container handling, refused rather than guessed."""


def dialect_of(suffix: str) -> Dialect:
    """The tag dialect for a lowercase file suffix, or :class:`UnsupportedContainer`."""
    try:
        return _DIALECT_BY_SUFFIX[suffix]
    except KeyError:
        raise UnsupportedContainer(
            f"no verified tag handling for {suffix!r}; supported containers are "
            f"{sorted(_DIALECT_BY_SUFFIX)}"
        ) from None


def _open(path: Path):
    """Open ``path`` with the mutagen class that understands its CONTAINER.

    Imports are deferred so the module imports on a slim install with no audio
    stack.
    """
    suffix = path.suffix.lower()
    dialect_of(suffix)  # refuse an unknown container before opening anything
    if suffix in FLAC_SUFFIXES:
        from mutagen.flac import FLAC

        return FLAC(path)
    if suffix in MP4_SUFFIXES:
        from mutagen.mp4 import MP4

        return MP4(path)
    if suffix in VORBIS_FILE_SUFFIXES:
        import mutagen

        return mutagen.File(path)
    if suffix in WAVE_SUFFIXES:
        # An ID3 chunk INSIDE the RIFF container. Never a bare ID3 stream.
        from mutagen.wave import WAVE

        return WAVE(path)
    if suffix in AIFF_SUFFIXES:
        # An ID3 chunk INSIDE the FORM container. Never a bare ID3 stream.
        from mutagen.aiff import AIFF

        return AIFF(path)
    # A real .mp3 is the one container whose ID3 genuinely is a stream prefix.
    from mutagen.mp3 import MP3

    return MP3(path)


#: An ID3v1 tag is exactly the last 128 bytes of the file and opens with this.
_ID3V1_MAGIC = b"TAG"
_ID3V1_LENGTH = 128


def _id3v1_trailer(path: Path) -> bytes | None:
    """The file's ID3v1 tag as raw bytes, or None when it has none."""
    try:
        with path.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            if handle.tell() < _ID3V1_LENGTH:
                return None
            handle.seek(-_ID3V1_LENGTH, os.SEEK_END)
            block = handle.read(_ID3V1_LENGTH)
    except OSError:
        return None
    return block if block[:3] == _ID3V1_MAGIC else None


def _restore_id3v1_trailer(path: Path, trailer: bytes) -> None:
    """Put a captured ID3v1 tag back over the one mutagen just rewrote.

    In place and never appended: only written where a trailer already is, so the
    file's length never changes and a tag the save removed is not invented.
    """
    try:
        with path.open("r+b") as handle:
            handle.seek(0, os.SEEK_END)
            if handle.tell() < _ID3V1_LENGTH:
                return
            handle.seek(-_ID3V1_LENGTH, os.SEEK_END)
            if handle.read(_ID3V1_LENGTH)[:3] != _ID3V1_MAGIC:
                return
            handle.seek(-_ID3V1_LENGTH, os.SEEK_END)
            handle.write(trailer)
    except OSError as exc:  # pragma: no cover - the save above already succeeded
        log.debug("could not preserve the ID3v1 trailer on %s: %s", path, exc)


def _save(path: Path, handle) -> None:
    """Save ``handle``, keeping a real ``.mp3``'s ID3v1 trailer verbatim. The one save seam."""
    if path.suffix.lower() not in MP3_SUFFIXES:
        handle.save()
        return
    trailer = _id3v1_trailer(path)
    handle.save()
    if trailer is not None:
        _restore_id3v1_trailer(path, trailer)


def _refuse_unknown(names: Iterable[str]) -> None:
    """Raise for a field name the table lacks, the beat grid rule's enforcement point."""
    unknown = set(names) - set(FIELDS)
    if unknown:
        raise ValueError(
            f"unknown tag fields: {sorted(unknown)}. The writable field set is a "
            f"module constant, not configuration, because a configurable field "
            f"set would reopen the beat-grid rule through the config file (R17)."
        )


def _rewrite(path: Path, edit, failure: str) -> bool:
    """Open ``path`` by its container, apply ``edit`` and save, True on success.

    ``edit(handle)`` answering False means the file already agrees, so nothing is
    saved. Any failure is logged with ``failure`` and answers False.
    """
    try:
        handle = _open(path)
        if edit(handle) is not False:
            _save(path, handle)
        return True
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort a batch
        log.debug(failure, path, exc)
        return False


def _set_field(handle, dialect: Dialect, spec: TagSpec, text: list[str], txxx_text) -> None:
    """Store ``text`` under ``spec``'s key in ``dialect``.

    A TXXX frame takes ``txxx_text`` as given: :func:`write_tags` hands it one
    string, which mutagen splits on a NUL, where other frames take the list.
    """
    if dialect is Dialect.VORBIS:
        handle[spec.vorbis] = text
    elif dialect is Dialect.MP4:
        from mutagen.mp4 import MP4FreeForm

        atom = spec.mp4
        handle[atom] = (
            [MP4FreeForm(value.encode("utf-8")) for value in text]
            if atom.startswith("----")
            else list(text)
        )
    else:
        import mutagen.id3 as id3

        if handle.tags is None:
            # The container's own way to add a block. A bare ID3 object built
            # instead is the corruption path for the chunk containers.
            handle.add_tags()
        frame_spec = spec.id3
        if frame_spec.startswith("TXXX:"):
            handle.tags[frame_spec] = id3.TXXX(
                encoding=3, desc=frame_spec[len("TXXX:"):], text=txxx_text
            )
        else:
            handle.tags[frame_spec] = getattr(id3, frame_spec)(encoding=3, text=text)


def write_tags(path: Path, fields: dict[str, object]) -> bool:
    """Write logical fields into ``path`` using its container's own tag format.

    Values are coerced to text and a None value is skipped. Returns True on
    success and False on any failure, since one bad file must not abort a batch.
    Two things raise instead: an unknown FIELD (``write_tags(p, {"bpm": 124})``
    cannot succeed, R17) and an unknown CONTAINER, which could only be guessed.
    """
    todo = {k: str(v) for k, v in fields.items() if v is not None}
    _refuse_unknown(todo)
    if not todo:
        return True
    dialect = dialect_of(path.suffix.lower())

    def edit(handle) -> None:
        for name, value in todo.items():
            _set_field(handle, dialect, FIELDS[name], [value], value)

    return _rewrite(path, edit, "tag write failed for %s: %s")


def write_genre(path: Path, genre: str) -> bool:
    """Write just the genre field. The one genre writer."""
    return write_tags(path, {"genre": genre})


def clear_tags(path: Path, fields: Sequence[str]) -> bool:
    """Remove logical fields from ``path``. Absent ones are already correct.

    The undo of :func:`write_tags`, which skips None and so cannot put a field
    back to ABSENT; a revert writing an empty string would leave a tag the user
    never had (U23). Returns True or False like its sibling, and an unknown
    FIELD still raises.
    """
    _refuse_unknown(fields)
    if not fields:
        return True
    dialect = dialect_of(path.suffix.lower())

    def edit(handle) -> bool:
        if dialect is Dialect.ID3 and handle.tags is None:
            # Nothing to remove, and adding a tag block in order to delete
            # from it would write a change where the file already agrees.
            return False
        target = handle.tags if dialect is Dialect.ID3 else handle
        for name in fields:
            target.pop(FIELDS[name].key_for(dialect), None)
        return True

    return _rewrite(path, edit, "tag clear failed for %s: %s")


def strip_tags(path: Path) -> bool:
    """Remove EVERY tag block ``path`` carries, known field or not.

    Only for a file this product did not tag and will tag from scratch: a
    tempo frame an uploader wrote is the one thing :func:`clear_tags` cannot
    reach, so the whole block goes first (R17). Dispatch goes through ``_open``
    like every writer here. True on success, False on any failure.
    """
    dialect_of(path.suffix.lower())
    try:
        handle = _open(path)
        if handle.tags is None:
            return True
        handle.delete()
        return True
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort a batch
        log.debug("tag strip failed for %s: %s", path, exc)
        return False


# Reading. An unreadable file reads as "no value", right for one damaged file
# and a catastrophe for an unmounted volume, so the mount precondition in
# ``preflight`` is asserted before any batch of reads. Neither is safe alone.


def read_tag(path: Path, field: str) -> str | None:
    """Read one logical field from ``path`` as text, or None if absent.

    One field of :func:`read_tags`. An unsupported container READS as None
    rather than raising, because reading damages nothing.
    """
    return read_tags(path, (field,))[field]


def read_tags(path: Path, fields: Sequence[str]) -> dict[str, str | None]:
    """Read several logical fields from ``path`` through ONE container open.

    Each field answers what :func:`read_tag` answers for it. An unknown field
    is refused before anything is opened.
    """
    return _read_tags(path, fields, strict=False)


class TagReadFailed(Exception):
    """The file's tags could not be read, which is not the same as it holding none.

    Raised only by the checked readers; every other reader folds it into None.
    """


def read_tags_checked(path: Path, fields: Sequence[str]) -> dict[str, str | None]:
    """:func:`read_tags` with a failed read kept apart from an absent field.

    One body with :func:`read_tags`, so the two cannot disagree. None still
    means absent. :class:`TagReadFailed` means the container is one this module
    does not read, mutagen could not open or recognise it, or a stored value
    could not be decoded. A file with no tag block at all reads as absent.
    """
    return _read_tags(path, fields, strict=True)


def read_tags_noting(path: Path, fields: Sequence[str]) -> tuple[dict[str, str | None], bool]:
    """:func:`read_tags`'s answer through the same one open, and whether it is whole.

    The flag is False wherever :func:`read_tags_checked` would have raised, so
    the library index may remember only a whole read (U249).
    """
    failed: list[str] = []
    values = _read_tags(path, fields, strict=False, failed=failed)
    return values, not failed


def _spec(field: str) -> TagSpec:
    spec = FIELDS.get(field)
    if spec is None:
        raise ValueError(f"unknown tag field: {field!r}; known fields are {sorted(FIELDS)}")
    return spec


def _read_tags(
    path: Path, fields: Sequence[str], *, strict: bool, failed: list[str] | None = None
) -> dict[str, str | None]:
    """The body of both readers. Not strict, every failure reads as absent.

    Per field when lenient: one undecodable field reads as None and its
    neighbours still come back. A ``failed`` list gains a line for each
    failure the strict mode would have raised on.
    """
    specs = {field: _spec(field) for field in fields}
    absent: dict[str, str | None] = dict.fromkeys(specs)
    try:
        dialect = dialect_of(path.suffix.lower())
    except UnsupportedContainer as exc:
        if strict:
            raise TagReadFailed(str(exc)) from exc
        if failed is not None:
            failed.append(str(exc))
        return absent
    try:
        import mutagen

        handle = mutagen.File(path)
    except Exception as exc:  # noqa: BLE001, see the note above read_tag
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
        if failed is not None:
            failed.append(f"{type(exc).__name__}: {exc}")
        return absent
    if handle is None:
        if strict:
            raise TagReadFailed("not a container the tag library recognises")
        if failed is not None:
            failed.append("not a container the tag library recognises")
        return absent
    if handle.tags is None:
        return absent
    values: dict[str, str | None] = {}
    for field, spec in specs.items():
        key = spec.key_for(dialect)
        try:
            values[field] = _one_text(handle.tags, key, dialect)
        except Exception as exc:  # noqa: BLE001, see the note above read_tag
            if strict:
                raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
            log.debug("tag read failed for %s %s: %s", path, key, exc)
            if failed is not None:
                failed.append(f"{key}: {type(exc).__name__}: {exc}")
            values[field] = None
    return values


def _one_text(tags: object, key: str, dialect: Dialect) -> str | None:
    """One stored field as stripped text, or None when absent. Raises when undecodable."""
    if key not in tags:  # type: ignore[operator]
        return None
    raw = tags[key]  # type: ignore[index]
    if dialect is Dialect.ID3:
        # A text frame stringifies to its joined text; TXXX likewise.
        return str(raw).strip() or None
    value = raw[0] if isinstance(raw, list) else raw
    if isinstance(value, (bytes, bytearray)):
        # An MP4 freeform atom carries bytes, not text.
        return bytes(value).decode("utf-8").strip() or None
    return str(value).strip() or None


def read_tag_values(path: Path, field: str) -> tuple[str, ...] | None:
    """Every value one logical field holds, EXACTLY, or None when it is absent.

    The exact sibling of :func:`read_tag`: nothing stripped, an empty value
    kept as ``("",)`` apart from absence, and every value of a multi-value
    field. The ID3 branch reads the frame's ``text`` list, since stringifying
    joins values on a NUL. An unsupported container reads as None.
    """
    return _read_tag_values(path, field, strict=False)


def read_tag_values_checked(path: Path, field: str) -> tuple[str, ...] | None:
    """:func:`read_tag_values` with a failed read kept apart from an absent field.

    One body with it. None still means the field is not there;
    :class:`TagReadFailed` means the read did not happen.
    """
    return _read_tag_values(path, field, strict=True)


def _read_tag_values(path: Path, field: str, *, strict: bool) -> tuple[str, ...] | None:
    """The body of both exact readers. Not strict, every failure reads as absent."""
    spec = _spec(field)
    try:
        dialect = dialect_of(path.suffix.lower())
    except UnsupportedContainer as exc:
        if strict:
            raise TagReadFailed(str(exc)) from exc
        return None
    key = spec.key_for(dialect)
    try:
        import mutagen

        handle = mutagen.File(path)
        if handle is None:
            if strict:
                raise TagReadFailed("not a container the tag library recognises")
            return None
        if handle.tags is None or key not in handle.tags:
            return None
        raw = handle.tags[key]
        if dialect is Dialect.ID3:
            # A frame with no text list is not one this module wrote: absent.
            values = getattr(raw, "text", None)
            if values is None:
                return None
            return tuple(str(value) for value in values)
        if not isinstance(raw, list):
            raw = [raw]
        return tuple(_as_text(value) for value in raw)
    except TagReadFailed:
        raise
    except Exception as exc:  # noqa: BLE001 - see the note above read_tag
        if strict:
            raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
        log.debug("exact tag read failed for %s: %s", path, exc)
        return None


def _as_text(value: object) -> str:
    """One stored value as text. An MP4 freeform atom carries bytes, not text."""
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8")
    return str(value)


def write_tag_values(path: Path, field: str, values: Sequence[str]) -> bool:
    """Write one logical field's values EXACTLY, multi-value included.

    The exact sibling of :func:`write_tags`, for a restore. An empty sequence
    clears the field through :func:`clear_tags`. True or False like its
    siblings, and an unknown FIELD still raises.
    """
    _refuse_unknown([field])
    if not values:
        return clear_tags(path, [field])
    dialect = dialect_of(path.suffix.lower())
    text = [str(value) for value in values]
    return _rewrite(
        path,
        lambda handle: _set_field(handle, dialect, FIELDS[field], text, text),
        "exact tag write failed for %s: %s",
    )


def _read_int(path: Path, field: str) -> int | None:
    return whole_number(read_tag(path, field), field=field, path=path)


def whole_number(value: str | None, *, field: str, path: Path) -> int | None:
    """A field's text as a whole number, or None when absent or not a number.

    THE ONE CONVERSION the energy and vocal readers take (U250).
    :func:`read_energy_checked` raises where this answers None for a present
    value. ``field`` and ``path`` only name the reading in the debug line.
    """
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
        return None


def read_energy_from_file(path: Path) -> int | None:
    """The stored energy rating (1 to 10), or None when absent or unreadable."""
    try:
        return read_energy_checked(path)
    except TagReadFailed as exc:
        log.debug("energy read failed for %s: %s", path, exc)
        return None


def read_energy_checked(path: Path) -> int | None:
    """The stored energy rating, None only when the file holds none.

    Raises :class:`TagReadFailed` when the file cannot be read or the stored
    value is not a number.
    """
    value = read_tags_checked(path, ("energylevel",))["energylevel"]
    if value is None:
        return None
    number = whole_number(value, field="energylevel", path=path)
    if number is None:
        raise TagReadFailed(f"energylevel is not a number: {value!r}")
    return number


def read_genre_from_file(path: Path) -> str | None:
    """The file's own genre tag, or None. The file is live where an export can be stale."""
    return read_tag(path, "genre")


def read_vox_from_file(path: Path) -> int | None:
    """The vocal-prominence level (0 to 100), or None."""
    return _read_int(path, "voxlevel")


def read_voxgender_from_file(path: Path) -> str | None:
    """The singer-gender call, or None. Read by tagging, never by routing."""
    return read_tag(path, "voxgender")


def audio_shape(path: Path) -> tuple[float | None, int | None, int | None]:
    """What the header says of the audio in ``path``: seconds, sample rate, channels.

    Never a decode (U241). Each is None when the header does not say it, cannot
    be read, or says something that is not a positive number.
    """
    try:
        import mutagen

        info = getattr(mutagen.File(path), "info", None)
    except Exception as exc:  # noqa: BLE001 - an unreadable header is an unknown shape
        log.debug("header read failed for %s: %s", path, exc)
        return None, None, None
    return (
        _positive(getattr(info, "length", None)),
        _positive_count(getattr(info, "sample_rate", None)),
        _positive_count(getattr(info, "channels", None)),
    )


def _positive(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    if not number > 0.0 or number == float("inf"):
        return None
    return number


def _positive_count(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        return None
    return value


def audio_seconds(path: Path) -> float | None:
    """How long the audio in ``path`` runs, read off its header, or None."""
    return audio_shape(path)[0]
