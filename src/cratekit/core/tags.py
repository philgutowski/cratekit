"""The one container-correct audio tag reader and writer.

Audio files are the user's irreplaceable data. This module is the only place in
Cratekit that touches them, and it exists because getting container dispatch
wrong does not produce an error, it produces a corrupted file.

THE CORRUPTION THIS PREVENTS, mechanically.

An AIFF file begins with the four bytes ``FORM``, followed by a size and then a
sequence of typed chunks whose positions the size fields describe. WAV is the
same shape with ``RIFF``. In both formats an ID3 tag is not a prefix on the
file, it is the PAYLOAD of a chunk inside the container, accounted for in the
container's own size field.

``mutagen.id3.ID3.save(path)`` is a raw ID3v2 stream writer. It knows nothing
about containers. It writes an ID3 block at offset 0 and shifts everything after
it. Applied to an AIFF the result is a file whose first bytes are ``ID3``, whose
``FORM`` header now sits at a nonzero offset, and whose chunk sizes describe a
layout that no longer exists. rekordbox and most decoders reject it, and
stripping the tag afterwards does not recover the audio because the offsets are
gone. In the source system three near-copies of this dispatch drifted apart and
one of them did exactly this. Consolidating them into one table is the fix, and
the per-container round-trip tests that hash the DECODED audio stream before and
after a write are what keep it fixed.

``mutagen.wave.WAVE`` and ``mutagen.aiff.AIFF`` know they are inside a container:
they insert, resize, and account for the chunk. Only a real ``.mp3`` takes a bare
ID3 stream. MP4 takes atoms and never ID3, for the same reason in a different
format.

WHY THE READERS LIVE HERE TOO (seam decision S5). The four tag readers used to
sit in the shared routing module, which does real file input from what is meant
to be a pure layer. Beyond the layering violation, they belonged here on the
merits: a reader and a writer that disagree about which key a field lives under
in one container lose that field on every round trip, silently, and only in that
container. Here they are driven by the SAME :data:`FIELDS` table through the
SAME container classification, so disagreement is not something a reviewer has
to catch. It is unrepresentable.

WHY THERE IS NO TEMPO FIELD. R17: nothing this product writes may carry a beat
grid or a BPM into anything rekordbox reads, and that is not configurable. The
enforcement is structural rather than conventional. :data:`FIELDS` has no ``bpm``
key and no ``TBPM`` frame, and :func:`write_tags` raises on any field name it
does not know, so there is no code path from the public surface to a tempo frame
at all. Making the field set user-definable would reopen that hole through
configuration, which is why this one table stays a module constant while the
taxonomy around it becomes declared configuration.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

log = logging.getLogger(__name__)


class Dialect(Enum):
    """The tag DIALECT a container speaks.

    Reader and writer both classify by this and only this, which is what makes
    them incapable of disagreeing about where a field lives. The mutagen CLASS
    is a separate, finer decision (FLAC and Ogg share a dialect but not a class;
    WAV, AIFF, and MP3 share a dialect but emphatically not a class).
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
        return {
            Dialect.VORBIS: self.vorbis,
            Dialect.MP4: self.mp4,
            Dialect.ID3: self.id3,
        }[dialect]


# Every logical field a caller may read or write. There is deliberately no
# tempo entry; see the module docstring. Adding one is not a feature.
FIELDS: dict[str, TagSpec] = {
    "title": TagSpec("title", "TIT2", "\xa9nam"),
    # Artist is here rather than read through a second, private code path,
    # because a second path is exactly the drift this table exists to end: any
    # consumer that needed the performer would otherwise open the file with its
    # own container guess, and a container guess is what corrupted an AIFF.
    "artist": TagSpec("artist", "TPE1", "\xa9ART"),
    "initialkey": TagSpec("initialkey", "TKEY", "----:com.apple.iTunes:INITIALKEY"),
    "genre": TagSpec("genre", "TCON", "\xa9gen"),
    "energylevel": TagSpec(
        "energylevel", "TXXX:EnergyLevel", "----:com.apple.iTunes:EnergyLevel"
    ),
    "inizio": TagSpec("inizio", "TXXX:INIZIO", "----:com.apple.iTunes:INIZIO"),
    "voxlevel": TagSpec("voxlevel", "TXXX:VoxLevel", "----:com.apple.iTunes:VoxLevel"),
    "voxgender": TagSpec("voxgender", "TXXX:VoxGender", "----:com.apple.iTunes:VoxGender"),
    "voxgenderconf": TagSpec(
        "voxgenderconf", "TXXX:VoxGenderConf", "----:com.apple.iTunes:VoxGenderConf"
    ),
}

FLAC_SUFFIXES = (".flac",)
VORBIS_FILE_SUFFIXES = (".opus", ".ogg")
MP4_SUFFIXES = (".m4a", ".mp4", ".m4b")
WAVE_SUFFIXES = (".wav",)
AIFF_SUFFIXES = (".aiff", ".aif", ".aifc")
MP3_SUFFIXES = (".mp3",)

# Every container this module will touch, and the dialect each one speaks. The
# table is exhaustive rather than a set of branches with a fallthrough. The
# source system's fallthrough case wrote a bare ID3 stream into ANY unrecognized
# suffix, which is the corruption path aimed at a container nobody had thought
# about yet.
_DIALECT_BY_SUFFIX: dict[str, Dialect] = {
    **{s: Dialect.VORBIS for s in FLAC_SUFFIXES + VORBIS_FILE_SUFFIXES},
    **{s: Dialect.MP4 for s in MP4_SUFFIXES},
    **{s: Dialect.ID3 for s in WAVE_SUFFIXES + AIFF_SUFFIXES + MP3_SUFFIXES},
}


class UnsupportedContainer(ValueError):
    """A suffix this module has no verified container handling for.

    Refusing is the safe answer and the source system's was not. Guessing ID3
    for an unrecognized container is the exact mistake that corrupted AIFF, so
    an unknown suffix produces a failed write, never a damaged file.
    """


def dialect_of(suffix: str) -> Dialect:
    """The tag dialect for a lowercase file suffix.

    Raises :class:`UnsupportedContainer` rather than guessing.
    """
    try:
        return _DIALECT_BY_SUFFIX[suffix]
    except KeyError:
        raise UnsupportedContainer(
            f"no verified tag handling for {suffix!r}; supported containers are "
            f"{sorted(_DIALECT_BY_SUFFIX)}"
        ) from None


def _open(path: Path):
    """Open ``path`` with the mutagen class that understands its CONTAINER.

    Every import is deferred into this function on purpose. It keeps the module
    importable on a slim install that has no audio stack, so a CLI that merely
    lists its subcommands never pays for, or crashes on, an optional dependency.

    The class choice is finer than the dialect: WAV, AIFF, and MP3 all speak ID3
    and all need a DIFFERENT class, because two of the three hold their ID3
    inside a container that has to be resized and re-accounted around it.
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


def write_tags(path: Path, fields: dict[str, object]) -> bool:
    """Write logical fields into ``path`` using its container's own tag format.

    Values are coerced to text and a None value is skipped, so a caller may pass
    everything it might have detected without first filtering out what it did
    not. Returns True on success and False on any failure, rather than raising:
    a tag write is one step of a long batch, and one unreadable file must not
    abort the run. Audio samples are untouched in every branch, which the
    per-container tests prove by hashing the decoded stream rather than the file.

    Exactly two things raise instead of returning False, because both are the
    caller asking for something that cannot be done safely rather than a file
    being awkward:

    * an unknown FIELD name, which is the beat-grid rule's enforcement point.
      ``write_tags(p, {"bpm": 124})`` cannot succeed;
    * an unknown CONTAINER, because the only way to proceed would be to guess,
      and guessing the container is what corrupted AIFF in the first place.
    """
    todo = {k: str(v) for k, v in fields.items() if v is not None}
    unknown = set(todo) - set(FIELDS)
    if unknown:
        raise ValueError(
            f"unknown tag fields: {sorted(unknown)}. The writable field set is a "
            f"module constant, not configuration, because a configurable field "
            f"set would reopen the beat-grid rule through the config file (R17)."
        )
    if not todo:
        return True

    suffix = path.suffix.lower()
    dialect = dialect_of(suffix)
    try:
        handle = _open(path)

        if dialect is Dialect.VORBIS:
            for name, value in todo.items():
                handle[FIELDS[name].vorbis] = [value]

        elif dialect is Dialect.MP4:
            from mutagen.mp4 import MP4FreeForm

            for name, value in todo.items():
                atom = FIELDS[name].mp4
                handle[atom] = (
                    [MP4FreeForm(value.encode("utf-8"))]
                    if atom.startswith("----")
                    else [value]
                )

        else:
            import mutagen.id3 as id3

            if handle.tags is None:
                # The step a naive writer skips. Skipping it is what pushes a
                # caller toward constructing a bare ID3 object instead, which is
                # the corruption path for the chunk containers.
                handle.add_tags()
            for name, value in todo.items():
                frame_spec = FIELDS[name].id3
                if frame_spec.startswith("TXXX:"):
                    description = frame_spec[len("TXXX:"):]
                    handle.tags[frame_spec] = id3.TXXX(
                        encoding=3, desc=description, text=value
                    )
                else:
                    handle.tags[frame_spec] = getattr(id3, frame_spec)(
                        encoding=3, text=[value]
                    )

        handle.save()
        return True
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort a batch
        log.debug("tag write failed for %s: %s", path, exc)
        return False


def write_genre(path: Path, genre: str) -> bool:
    """Write just the genre field. The one genre writer."""
    return write_tags(path, {"genre": genre})


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------
#
# A NOTE ON THE None DEGRADE, because it looks careless and is not. An
# unreadable file reads as "no value", and a router then treats the track as
# untagged and files it in the fallback bucket. That is the right behaviour for
# ONE damaged file and a catastrophe for a whole library, because an unmounted
# volume makes every file unreadable at once and the whole collection silently
# lands in the fallback bucket with no warning. The guard against that is not
# here, it is the mount precondition in ``preflight``, asserted BEFORE any batch
# of reads. These two modules are a pair; neither is safe without the other.


def read_tag(path: Path, field: str) -> str | None:
    """Read one logical field from ``path`` as text, or None if absent.

    Driven by the same :data:`FIELDS` table and the same container
    classification as the writer, which is the whole reason the reader lives in
    this module (S5). A field renamed in one place cannot be looked up under its
    old name in the other, because there is only one place.

    Asymmetric with the writer on one point, deliberately: an unsupported
    container READS as None rather than raising. Reading cannot damage anything,
    and a sweep across a directory that happens to contain one stray file should
    report no tags rather than abort. Writing into an unknown container can
    damage something, so that one refuses.
    """
    spec = FIELDS.get(field)
    if spec is None:
        raise ValueError(f"unknown tag field: {field!r}; known fields are {sorted(FIELDS)}")

    try:
        dialect = dialect_of(path.suffix.lower())
    except UnsupportedContainer:
        return None
    key = spec.key_for(dialect)
    try:
        import mutagen

        handle = mutagen.File(path)
        if handle is None or handle.tags is None:
            return None
        tags = handle.tags
        if key not in tags:
            return None
        raw = tags[key]
        if dialect is Dialect.ID3:
            # A text frame stringifies to its joined text; TXXX likewise.
            return str(raw).strip() or None
        value = raw[0] if isinstance(raw, list) else raw
        if isinstance(value, (bytes, bytearray)):
            # An MP4 freeform atom carries bytes, not text.
            return bytes(value).decode("utf-8").strip() or None
        return str(value).strip() or None
    except Exception as exc:  # noqa: BLE001 - see the note above this function
        log.debug("tag read failed for %s: %s", path, exc)
        return None


def _read_int(path: Path, field: str) -> int | None:
    value = read_tag(path, field)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
        return None


def read_energy_from_file(path: Path) -> int | None:
    """The stored energy rating (1 to 10), or None when absent or unreadable."""
    return _read_int(path, "energylevel")


def read_genre_from_file(path: Path) -> str | None:
    """The file's own genre tag, or None.

    Read from the file rather than from an export because the file is the live
    value: an export can be hours stale, and re-deriving placement from a stale
    genre moves a track the user already re-tagged.
    """
    return read_tag(path, "genre")


def read_vox_from_file(path: Path) -> int | None:
    """The vocal-prominence level (0 to 100), or None."""
    return _read_int(path, "voxlevel")


def read_voxgender_from_file(path: Path) -> str | None:
    """The singer-gender call, or None.

    Never consumed by routing, only by tagging. Routing that branched on gender
    would encode a judgement about singers into the library's structure, which
    is not a thing this product does.
    """
    return read_tag(path, "voxgender")
