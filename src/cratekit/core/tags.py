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

TWO READERS AND TWO WRITERS, AND WHY THAT IS NOT DUPLICATION.
:func:`read_tag` and :func:`write_tags` are the CONVENIENT pair. They speak in
single strings, the reader strips surrounding whitespace and reports an empty
value as absent, and the writer coerces whatever it is handed to text. That is
the right shape for every consumer that asks a file a question ("what genre does
this claim to be") and for every producer that states an answer.

:func:`read_tag_values` and :func:`write_tag_values` are the EXACT pair, and
they exist because an undo log cannot use the convenient one. A ledger recording
what a file held before an irreversible write has to be able to tell ``"House "``
from ``"House"``, ``""`` from absent, and ``["House", "Techno"]`` from
``"House"``. Each of those three is a difference the convenient reader
deliberately erases, and each erasure turns a restore into a silent edit: a
stripped value comes back stripped, an empty value comes back DELETED, and a
second value comes back not at all. The exact pair is driven by the same
:data:`FIELDS` table and the same ``_open``, so it cannot disagree with its
sibling about where a field lives; it only disagrees about how much of what is
there it is willing to lose. :mod:`cratekit.adopt.revert` is the caller that
needs the difference.

WHY AN ID3v1 TRAILER IS PUT BACK BYTE FOR BYTE. ``mutagen``'s ID3 save defaults
to ``v1=1``, which means "if this file already carries an ID3v1 trailer, rewrite
it from the ID3v2 frames". That is a reasonable default and it destroys data this
module never recorded: an ID3v1 genre is a single byte indexing a fixed list, so
any v2 genre outside that list rewrites the byte to 255, and the original index
is gone. A legacy library whose files carry both tags therefore loses the v1
genre on the first write and never gets it back, because the revert ledger tracks
the v2 field alone. So the 128-byte trailer is captured before the save and
written back over itself afterwards, in place and only when a trailer was there
both before and after. That is confined to a real ``.mp3``: WAV and AIFF keep
their ID3 in a CHUNK, mutagen may legitimately grow that chunk at the end of the
file, and rewriting their last 128 bytes would be the corruption this module
exists to prevent.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Sequence

log = logging.getLogger(__name__)


_ISRC = re.compile(r"[A-Z]{2}[A-Z0-9]{3}[0-9]{7}")


def fold_isrc(value: object) -> str:
    """An ISRC spelling with its whitespace and hyphens dropped, upper cased.

    THE ONE FOLD, called by the outbound source, the missing verb, the index
    and the naming verb (U212, which moved it here from the match engine), so a
    hyphenated spelling on one side and a bare one on the other are one
    string. Not validated: a verb that has to say a value was malformed rather
    than absent reads this and then asks :func:`isrc_token`.
    """
    return re.sub(r"[\s-]", "", str(value or "")).upper()


def isrc_token(value: object) -> str:
    """The folded ISRC as an identity, or ``""`` when the value is not one.

    A value that does not read as an ISRC once folded, a catalogue number or a
    stray label, is NOT an identity and folds to empty rather than to a key
    nothing else could share by accident.
    """
    folded = fold_isrc(value)
    return folded if _ISRC.fullmatch(folded) else ""


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
    # R-355. The recording's identity, which the outbound verbs hand the account
    # to match on, because a rekordbox collection export carries none. ``TSRC``
    # is the ID3 frame the standard names for it, and the downloader writes the
    # Vorbis ``isrc`` comment on every file it delivers.
    "isrc": TagSpec("isrc", "TSRC", "----:com.apple.iTunes:ISRC"),
    # R-572. The release the file was cut from, read beside the ISRC so the
    # account can tell a single from its album cut when both are spelled alike.
    # ``TALB`` is the ID3 frame for it and the Vorbis comment is ``album``.
    "album": TagSpec("album", "TALB", "\xa9alb"),
    # U156. The release date, read for its year when a landing files a label's
    # tracks under ``<Label> <year>`` without a manifest. ``TDRC`` is the ID3
    # recording time frame, and the downloader writes the Vorbis ``date``
    # comment and the MP4 day atom on every file it delivers.
    "date": TagSpec("date", "TDRC", "\xa9day"),
    # U163. The album's own artist, which a native landing links the album row
    # to as Reload Tags does. ``TPE2`` is the ID3 frame every tagger writes it
    # to, ``albumartist`` the Vorbis comment and ``aART`` the MP4 atom.
    "albumartist": TagSpec("albumartist", "TPE2", "aART"),
    # U178. The record label a file was released on, read so ``tag folder`` can
    # give a registered label's genre to every file of it. The keys are the
    # ones MusicBrainz Picard writes, the Vorbis ``label`` comment, the ID3
    # publisher frame ``TPUB`` and a freeform MP4 atom. Which field rekordbox
    # shows in its Label column is U177's to measure on a copy, and the entry
    # moves here, for reader and writer at once, if the measurement differs.
    "label": TagSpec("label", "TPUB", "----:com.apple.iTunes:LABEL"),
    # U240. The release's copyright line, read so ``tag folder`` can name the
    # registered label of a file that carries no label tag. The keys are the
    # ones the vendored downloader writes on every file it delivers
    # (``_vendor/downloader/metadata.py``): the Vorbis ``COPYRIGHT`` comment,
    # which Vorbis reads in any case, the ID3 ``TCOP`` frame and the MP4
    # ``cprt`` atom. Nothing in Cratekit writes it.
    "copyright": TagSpec("copyright", "TCOP", "cprt"),
    # U157. How far the track's tempo moves over its length and the verdict
    # that reading takes, written by ``analyze run`` beside ``voxlevel`` so a
    # landing can mark the rows rekordbox should analyse with Dynamic. The
    # level is a percent spread and the verdict a word, so NEITHER IS A TEMPO
    # and the table still has no tempo entry; ``core.drift`` says what each is.
    "driftlevel": TagSpec(
        "driftlevel", "TXXX:DriftLevel", "----:com.apple.iTunes:DriftLevel"
    ),
    "drift": TagSpec("drift", "TXXX:Drift", "----:com.apple.iTunes:Drift"),
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

#: Every container suffix this module has verified handling for, DERIVED from
#: the table above rather than listed a second time. A caller that walks a music
#: directory needs to know which files carry tags, and a hand-kept copy of that
#: answer is a copy that misses the next container added here, which shows up as
#: a whole format silently absent from a sweep (P3).
SUPPORTED_SUFFIXES: tuple[str, ...] = tuple(sorted(_DIALECT_BY_SUFFIX))


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


#: An ID3v1 tag is exactly the last 128 bytes of the file and opens with this.
_ID3V1_MAGIC = b"TAG"
_ID3V1_LENGTH = 128


def _id3v1_trailer(path: Path) -> bytes | None:
    """The file's ID3v1 tag as raw bytes, or None when it has none.

    Read rather than parsed. What has to survive a save is the exact byte the
    genre index lives in, and every other field beside it, so nothing here needs
    to know what any of them mean.
    """
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

    IN PLACE AND NEVER APPENDED. The trailer is only written where a trailer
    already is, so this can change 128 bytes and can never change the file's
    length. If the save removed the tag outright, re-adding it here would be this
    module inventing a tag rather than preserving one, so it declines.
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
    """Save ``handle``, preserving a real ``.mp3``'s ID3v1 trailer verbatim.

    The one save seam, so the writer and the deleter cannot disagree about
    whether the legacy tag survives. See the module docstring for why mutagen's
    own default destroys it and why only ``.mp3`` takes this branch.
    """
    if path.suffix.lower() not in MP3_SUFFIXES:
        handle.save()
        return
    trailer = _id3v1_trailer(path)
    handle.save()
    if trailer is not None:
        _restore_id3v1_trailer(path, trailer)


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

        _save(path, handle)
        return True
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort a batch
        log.debug("tag write failed for %s: %s", path, exc)
        return False


def write_genre(path: Path, genre: str) -> bool:
    """Write just the genre field. The one genre writer."""
    return write_tags(path, {"genre": genre})


def clear_tags(path: Path, fields: Sequence[str]) -> bool:
    """Remove logical fields from ``path``. Absent ones are already correct.

    THE UNDO OF :func:`write_tags`, AND IT CANNOT BE EXPRESSED THROUGH IT.
    ``write_tags`` skips a None value on purpose, so that a caller may pass
    everything it might have detected without filtering first. That default is
    right for a detection pass and it leaves one operation unreachable: putting a
    field back to ABSENT. The two are different facts about a file, and a revert
    that wrote an empty string where a field had never existed would leave a tag
    the user never had while reporting the file restored exactly (U23's revert
    ledger is the caller that needs the difference).

    It lives HERE rather than in the module that needs it, for seam decision S5's
    reason: the reader and the writer classify containers through one table and
    one ``_open``, so they are incapable of disagreeing about where a field
    lives. A deletion written anywhere else would be a third classification, and
    the AIFF corruption this module exists to prevent came from exactly one
    caller guessing at a container for itself.

    Returns True on success and False on any failure, matching its sibling: one
    awkward file must not abort a batch. An unknown FIELD still raises, because
    that is the beat-grid rule's enforcement point and a deletion path that
    accepted an unknown name would be a way around the table.
    """
    unknown = set(fields) - set(FIELDS)
    if unknown:
        raise ValueError(
            f"unknown tag fields: {sorted(unknown)}. The writable field set is a "
            f"module constant, not configuration, because a configurable field "
            f"set would reopen the beat-grid rule through the config file (R17)."
        )
    if not fields:
        return True

    suffix = path.suffix.lower()
    dialect = dialect_of(suffix)
    try:
        handle = _open(path)
        if dialect is Dialect.VORBIS:
            for name in fields:
                handle.pop(FIELDS[name].vorbis, None)
        elif dialect is Dialect.MP4:
            for name in fields:
                handle.pop(FIELDS[name].mp4, None)
        else:
            if handle.tags is None:
                # Nothing to remove, and adding a tag block in order to delete
                # from it would write a change where the file already agrees.
                return True
            for name in fields:
                handle.tags.pop(FIELDS[name].id3, None)
        _save(path, handle)
        return True
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort a batch
        log.debug("tag clear failed for %s: %s", path, exc)
        return False


def strip_tags(path: Path) -> bool:
    """Remove EVERY tag block ``path`` carries, known field or not.

    FOR A FILE THIS PRODUCT DID NOT TAG AND WILL TAG FROM SCRATCH, and for
    nothing else. :func:`clear_tags` removes only fields the table names, and
    the table has no tempo field on purpose, so a tempo frame somebody else
    wrote is exactly the one thing it cannot reach. A second source upload is
    that file: an uploader's container can carry a BPM frame, the download tool
    keeps it whenever the upload is already in the target format, and adding
    the row's artist and title on top would commit it (R17). Stripping the
    whole block first is the only way the table's refusal to name a tempo
    becomes a file that carries none.

    Container dispatch goes through ``_open`` like every other writer here, so
    an ID3 chunk inside WAV or AIFF is removed by the class that accounts for
    the chunk, never by a bare ID3 stream writer. Returns True on success and
    False on any failure, matching its siblings.
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

    ONE FIELD OF :func:`read_tags`, so there is one reader and not two opinions
    about what a stored value reads as.
    """
    return read_tags(path, (field,))[field]


def read_tags(path: Path, fields: Sequence[str]) -> dict[str, str | None]:
    """Read several logical fields from ``path`` through ONE container open.

    Each field answers exactly what :func:`read_tag` answers for it, absent
    fields included, because the two are one reader. The library index reads
    four fields per file over the whole music folder, and four opens per file
    over ten thousand files on an external volume is the cost this exists to
    remove. The finding is the residual titled "The index reader opens every
    container three times, and the walk is the library".

    An unknown field is refused before anything is opened, the way
    :func:`read_tag` refuses it, so a misspelled field name in a four field
    read cannot be answered as absent.
    """
    return _read_tags(path, fields, strict=False)


class TagReadFailed(Exception):
    """The file's tags could not be read, which is not the same as it holding none.

    Raised only by the checked readers. Every other reader here folds it into
    None, for the reason the note above :func:`read_tag` gives.
    """


def read_tags_checked(path: Path, fields: Sequence[str]) -> dict[str, str | None]:
    """:func:`read_tags` with a failed read kept apart from an absent field.

    ONE BODY WITH :func:`read_tags`, which folds each failure into None where
    this raises it, so the two cannot disagree about a value both read. A caller that routes a whole library on one field needs to tell "the
    file holds no value" from "the file could not be read", because the first is
    a fact about the track and the second is a fact about the read, and filing
    both into the same fallback reports a damaged file as an untagged one. The
    residual titled "Adoption files every track as if it had no energy reading,
    and the library's files carry one" is the caller that needed it.

    None for a field still means absent. :class:`TagReadFailed` means the
    container is one this module does not read, mutagen could not open it or
    did not recognise it, or a stored value could not be decoded. A file mutagen
    opens that carries no tag block at all holds no values, and reads as absent.
    """
    return _read_tags(path, fields, strict=True)


def read_tags_noting(path: Path, fields: Sequence[str]) -> tuple[dict[str, str | None], bool]:
    """:func:`read_tags`'s answer, through the same one open, and whether it is whole.

    The second value is True when nothing failed, False wherever
    :func:`read_tags_checked` would have raised: a container this module does
    not read, one mutagen could not open or did not recognise, or a stored value
    that could not be decoded. The values are exactly what :func:`read_tags`
    answers in every case. The library index's reader needs both at once (U249):
    the lenient answer to index the file by, and whether that answer may be
    remembered, since a failed read on an external volume can be a moment's I/O
    error. Asking the checked reader and then the lenient one opened a refused
    file twice on every walk.
    """
    failed: list[str] = []
    values = _read_tags(path, fields, strict=False, failed=failed)
    return values, not failed


def _read_tags(
    path: Path, fields: Sequence[str], *, strict: bool, failed: list[str] | None = None
) -> dict[str, str | None]:
    """The body of both readers. Not strict, every failure reads as absent.

    Per field in the lenient mode, deliberately: one undecodable field reads as
    None and its neighbours still come back, which is what :func:`read_tags`
    has always answered. A ``failed`` list given in the lenient mode gains one
    line for each failure the strict mode would have raised on.
    """
    specs: dict[str, TagSpec] = {}
    for field in fields:
        spec = FIELDS.get(field)
        if spec is None:
            raise ValueError(
                f"unknown tag field: {field!r}; known fields are {sorted(FIELDS)}"
            )
        specs[field] = spec

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

    THE EXACT SIBLING OF :func:`read_tag`, and the three differences are the
    whole reason it exists. Nothing is stripped, nothing empty is folded into
    absence, and a field holding more than one value comes back holding more than
    one value. A caller recording what a file said before overwriting it needs all
    three, because each one it did not get back is a difference a later restore
    would silently introduce.

    None means the field IS NOT THERE. That is a different fact from a field
    holding one empty string, which comes back as ``("",)``, and the whole point
    of separating them is that restoring the first means deleting the field while
    restoring the second means writing an empty value.

    The ID3 branch reads the frame's own ``text`` list rather than stringifying
    the frame. Stringifying joins the values on a null byte, which round-trips by
    accident through mutagen and reads as one corrupted value everywhere else.

    Shares :func:`read_tag`'s asymmetry with the writers: an unsupported
    container reads as None rather than raising, because reading damages nothing.
    """
    return _read_tag_values(path, field, strict=False)


def read_tag_values_checked(path: Path, field: str) -> tuple[str, ...] | None:
    """:func:`read_tag_values` with a failed read kept apart from an absent field.

    ONE BODY WITH IT, for the reason :func:`read_tags_checked` gives. None
    still means the field is not there. :class:`TagReadFailed` means the
    container is one this module does not read, or the tag library could not
    open it, did not recognise it or could not decode what it holds. A caller
    about to decide whether a file still carries what somebody wrote needs
    every value AND needs to know the read happened, and two opens to learn
    both is a second chance for the answers to disagree.
    """
    return _read_tag_values(path, field, strict=True)


def _read_tag_values(path: Path, field: str, *, strict: bool) -> tuple[str, ...] | None:
    """The body of both exact readers. Not strict, every failure reads as absent."""
    spec = FIELDS.get(field)
    if spec is None:
        raise ValueError(f"unknown tag field: {field!r}; known fields are {sorted(FIELDS)}")

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
        if handle.tags is None:
            return None
        tags = handle.tags
        if key not in tags:
            return None
        raw = tags[key]
        if dialect is Dialect.ID3:
            # Every frame this table can name is a text frame, so its values are
            # the ``text`` list. A frame with no text list at all is not
            # something this module wrote and is reported as absent rather than
            # guessed at.
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

    THE EXACT SIBLING OF :func:`write_tags`, which coerces to text and writes one
    value per field because that is what a detection pass has to give. A restore
    has something better: the values it read off the file itself, unmodified, and
    handing those to a writer that can only hold one of them loses the rest with
    no record that it happened.

    AN EMPTY SEQUENCE CLEARS THE FIELD, through :func:`clear_tags` rather than by
    writing nothing. A field present with zero values is not a state any of these
    containers represents distinguishably from absence, so the honest write for
    it is the deletion, taken through the one deleter so the container
    classification stays single.

    Returns True on success and False on any failure, matching both siblings: one
    awkward file must not abort a batch. An unknown FIELD still raises, because
    that is the beat-grid rule's enforcement point.
    """
    if field not in FIELDS:
        raise ValueError(
            f"unknown tag fields: {[field]}. The writable field set is a module "
            f"constant, not configuration, because a configurable field set would "
            f"reopen the beat-grid rule through the config file (R17)."
        )
    if not values:
        return clear_tags(path, [field])

    suffix = path.suffix.lower()
    dialect = dialect_of(suffix)
    text = [str(value) for value in values]
    try:
        handle = _open(path)
        if dialect is Dialect.VORBIS:
            handle[FIELDS[field].vorbis] = text
        elif dialect is Dialect.MP4:
            from mutagen.mp4 import MP4FreeForm

            atom = FIELDS[field].mp4
            handle[atom] = (
                [MP4FreeForm(value.encode("utf-8")) for value in text]
                if atom.startswith("----")
                else list(text)
            )
        else:
            import mutagen.id3 as id3

            if handle.tags is None:
                handle.add_tags()
            frame_spec = FIELDS[field].id3
            if frame_spec.startswith("TXXX:"):
                handle.tags[frame_spec] = id3.TXXX(
                    encoding=3, desc=frame_spec[len("TXXX:"):], text=text
                )
            else:
                handle.tags[frame_spec] = getattr(id3, frame_spec)(encoding=3, text=text)
        _save(path, handle)
        return True
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort a batch
        log.debug("exact tag write failed for %s: %s", path, exc)
        return False


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
    try:
        return read_energy_checked(path)
    except TagReadFailed as exc:
        log.debug("energy read failed for %s: %s", path, exc)
        return None


def read_energy_checked(path: Path) -> int | None:
    """The stored energy rating, None only when the file holds none.

    Raises :class:`TagReadFailed` when the file cannot be read or the stored
    value is not a number, so a caller can report a damaged file rather than
    file it as untagged. :func:`read_energy_from_file` is this with that folded
    into None, so the two cannot disagree about what a stored value reads as.
    """
    value = read_tags_checked(path, ("energylevel",))["energylevel"]
    if value is None:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise TagReadFailed(f"energylevel is not a number: {value!r}") from exc


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


def audio_shape(path: Path) -> tuple[float | None, int | None, int | None]:
    """What the header says of the audio in ``path``: seconds, sample rate, channels.

    The container's own statement, never a decode: a pass that is about to
    decode a folder asks this first, to know how much memory each file will
    need (U241). Each of the three is None when the header does not say it,
    cannot be read, or says something that is not a positive number, and the
    caller decides what not knowing means. Reads nothing but the header and
    writes nothing.
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
