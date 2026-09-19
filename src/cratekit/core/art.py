"""Album art: one CDJ safe encoder, one reader and one writer per container.

WHY THIS IS ITS OWN MODULE AND NOT A FIELD IN ``tags``. ``tags.FIELDS`` is a
closed constant of TEXT fields, and its being closed is what enforces the beat
grid rule. A picture is not a text field, so adding one there would mean
loosening the one table that must stay tight. This module borrows the other
half of ``tags`` instead: ``_open`` and ``_save``, so the art writer and the tag
writer classify containers through one table and cannot disagree about which
mutagen class a file needs. That matters for the same reason it does there. A
bare ID3 stream written at the front of an AIFF or a WAV corrupts the container,
and the way to make that impossible is to never choose the class here.

WHAT "CDJ SAFE" MEANS. Pioneer players render a BASELINE JPEG and show a
PROGRESSIVE one as a blank square. They also read the width, height and depth a
FLAC picture block DECLARES, and a block declaring zeroes renders blank even when
the image inside it is fine. So there are two separate ways to ship art a DJ
never sees, and this module closes both: the encoder never emits progressive, and
the writer fills the FLAC block from the image itself rather than from anything a
caller says.

THE WRITER MEASURES, IT DOES NOT TRUST. :func:`write_front_cover` takes bytes and
nothing else. The dimensions it writes into a FLAC block come from Pillow
decoding those bytes, never from the encoder's own report of what it made, so an
encoder defect cannot become a confident wrong number in a file.

FIVE CONTAINERS, NOT SEVEN. ``tags`` also handles ``.ogg`` and ``.opus``. Their
pictures live in a base64 comment this module has no verified handling for, and
the source system never wrote one, so they are refused here rather than guessed.

Nothing in this module reads, writes or deletes a tempo value in any container.
"""

from __future__ import annotations

import io
import logging
from dataclasses import dataclass
from pathlib import Path

from cratekit.core import tags

log = logging.getLogger(__name__)

#: The edge, in pixels, of newly embedded art. The source system's figure.
ART_SIZE = 800
#: The byte cap for one embedded picture, under 500 KB with margin.
ART_MAX_BYTES = 450_000
#: The encoder starts here and steps down until the picture fits the cap.
ART_START_QUALITY = 88
ART_QUALITY_STEP = 5
#: Below this the picture is visibly damaged, so the encoder refuses instead.
ART_MIN_QUALITY = 50

JPEG_MIME = "image/jpeg"
#: The picture type every tag format numbers 3, "Cover (front)".
FRONT_COVER = 3
#: Bits per pixel by Pillow mode, the figure a FLAC picture block declares. A
#: mode missing from this table measures as depth 0, never as a guessed 24.
_DEPTH_BY_MODE = {
    "1": 1, "L": 8, "P": 8, "LA": 16, "PA": 16, "I;16": 16,
    "RGB": 24, "YCbCr": 24, "LAB": 24, "HSV": 24,
    "RGBA": 32, "RGBX": 32, "CMYK": 32, "I": 32, "F": 32,
}
#: What transparent pixels are flattened onto. JPEG has no alpha, and a plain
#: mode conversion exposes whatever colour sits UNDER the transparency, which
#: for most exported logos is black: dark art on a black square.
_FLATTEN_ONTO = (255, 255, 255)

#: The containers with verified picture handling, DERIVED from the tag module's
#: own suffix tuples so a suffix added there is not silently half supported here.
ART_SUFFIXES: tuple[str, ...] = tuple(
    sorted(
        tags.FLAC_SUFFIXES
        + tags.MP3_SUFFIXES
        + tags.AIFF_SUFFIXES
        + tags.WAVE_SUFFIXES
        + tags.MP4_SUFFIXES
    )
)


class ArtError(ValueError):
    """Image bytes that cannot be made into, or are not, CDJ safe art."""


class UnreadableFile(Exception):
    """An audio file whose pictures could not be looked at, for any reason.

    DELIBERATELY NOT AN :class:`ArtError`. That one is a verdict on image bytes.
    This one says nothing was learned about the file, and the cause may be the
    volume or the install rather than the file. A sweep that caught both under
    one name would mark a whole unmounted library as carrying bad art.
    """


@dataclass(frozen=True)
class CdjJpeg:
    """A baseline JPEG and what Pillow measured on reading it back."""

    data: bytes
    width: int
    height: int
    depth: int


@dataclass(frozen=True)
class EmbeddedPicture:
    """One picture found inside an audio file.

    ``width``, ``height`` and ``depth`` are WHAT A PLAYER IS TOLD. A FLAC block
    declares them, so for FLAC they are the block's own values, zeroes included,
    because a zeroed block is exactly what a repair pass has to find. ID3 and MP4
    declare nothing and a player decodes the image, so for those they are the
    decoded values, and zero when the data does not decode.

    ``decoded`` says whether Pillow could read ``data`` at all. ``progressive``
    is only meaningful when it could: an undecodable picture reports False there
    and must never be read as "baseline, therefore fine".
    """

    mime: str
    width: int
    height: int
    depth: int
    progressive: bool
    decoded: bool
    data: bytes
    #: What Pillow found the bytes to BE, "JPEG" or "PNG", or None when they did
    #: not decode. ``mime`` is only what the container claims, and a block
    #: claiming image/jpeg over PNG bytes is a thing other taggers produce.
    format: str | None = None


@dataclass(frozen=True)
class _Measured:
    format: str | None
    mode: str
    width: int
    height: int
    depth: int
    progressive: bool


def _measure(data: bytes) -> _Measured | None:
    """What Pillow reads from ``data``, or None when it reads nothing.

    A FULL decode, not a header read. A truncated picture opens cleanly and
    fails only on ``load``, and it renders as blank as a progressive one, so a
    header read would call it fine. That costs a decode per picture on a sweep.
    """
    from PIL import Image

    try:
        with Image.open(io.BytesIO(data)) as img:
            img.load()
            progressive = bool(img.info.get("progressive") or img.info.get("progression"))
            width, height = img.size
            return _Measured(
                format=img.format,
                mode=img.mode,
                width=width,
                height=height,
                depth=_DEPTH_BY_MODE.get(img.mode, 0),
                progressive=progressive,
            )
    except Exception as exc:  # noqa: BLE001 - Pillow raises many types on bad bytes
        log.debug("image bytes did not decode: %s", exc)
        return None


def _require_art_container(path: Path) -> str:
    """The lowercase suffix, or :class:`tags.UnsupportedContainer`."""
    suffix = path.suffix.lower()
    if suffix not in ART_SUFFIXES:
        raise tags.UnsupportedContainer(
            f"no verified picture handling for {suffix!r}; supported containers "
            f"are {list(ART_SUFFIXES)}"
        )
    return suffix


def _quality_ladder() -> list[int]:
    """The qualities to try, highest first, ENDING ON THE FLOOR EXACTLY.

    Stepping 88 down by 5 lands on 53 and then 48, so a plain countdown never
    tries 50 and refuses a picture that would have fit. The source system
    covered that with a second save after its loop. Here the floor is simply the
    last rung.
    """
    rungs = list(range(ART_START_QUALITY, ART_MIN_QUALITY, -ART_QUALITY_STEP))
    return [*rungs, ART_MIN_QUALITY]


def _flatten_to_rgb(img):
    """``img`` as RGB, with any transparency composited onto white first."""
    from PIL import Image

    has_alpha = img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info
    if not has_alpha:
        return img.convert("RGB")
    rgba = img.convert("RGBA")
    flat = Image.new("RGB", rgba.size, _FLATTEN_ONTO)
    flat.paste(rgba, mask=rgba.getchannel("A"))
    return flat


def to_cdj_jpeg(
    data: bytes, *, size: int | None = ART_SIZE, max_bytes: int = ART_MAX_BYTES
) -> CdjJpeg:
    """Re-encode any image bytes as a baseline RGB JPEG no larger than ``max_bytes``.

    ``size`` is the square edge for NEW art. ``None`` keeps the native
    resolution, which is what a repair of art already in a file wants, since
    upscaling only invents detail. A non square image is resized to the square
    without cropping, which is what the source system did.

    Two things a re-encode would otherwise lose are applied first. An EXIF
    orientation is baked into the pixels, because the tag does not survive and
    the cover would come out sideways for good. Transparency is flattened onto
    white, because JPEG has no alpha.

    Quality steps down from :data:`ART_START_QUALITY` until the picture fits.
    If it still does not fit at :data:`ART_MIN_QUALITY` this raises rather than
    returning bytes over the cap, because a function that takes a cap and
    silently exceeds it has told its caller something false.

    The returned dimensions and depth are measured by reading the encoded bytes
    back, not copied from the image that went in.
    """
    from PIL import Image, ImageOps

    try:
        with Image.open(io.BytesIO(data)) as source:
            img = _flatten_to_rgb(ImageOps.exif_transpose(source))
    except Exception as exc:  # noqa: BLE001 - Pillow raises many types on bad bytes
        raise ArtError(f"the image bytes could not be decoded: {exc}") from exc

    if size is not None and img.size != (size, size):
        img = img.resize((size, size), Image.LANCZOS)

    for quality in _quality_ladder():
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True, progressive=False)
        encoded = buffer.getvalue()
        if len(encoded) <= max_bytes:
            measured = _measure(encoded)
            if measured is None:  # pragma: no cover - Pillow reading its own output
                raise ArtError("the encoded JPEG could not be read back")
            return CdjJpeg(encoded, measured.width, measured.height, measured.depth)

    raise ArtError(
        f"the image does not fit in {max_bytes} bytes even at quality "
        f"{ART_MIN_QUALITY}, at {img.size[0]} by {img.size[1]} pixels"
    )


def _picture(mime: str, data: bytes, declared: tuple[int, int, int] | None) -> EmbeddedPicture:
    measured = _measure(data)
    if declared is not None:
        width, height, depth = declared
    elif measured is not None:
        width, height, depth = measured.width, measured.height, measured.depth
    else:
        width = height = depth = 0
    return EmbeddedPicture(
        mime=mime,
        width=width,
        height=height,
        depth=depth,
        progressive=measured.progressive if measured is not None else False,
        decoded=measured is not None,
        data=data,
        format=measured.format if measured is not None else None,
    )


def read_pictures(path: Path) -> list[EmbeddedPicture]:
    """Every picture embedded in ``path``, in the order the container holds them.

    An empty list means the file was read and holds no picture. A file that
    could not be read raises :class:`UnreadableFile` instead, so "no art" and
    "could not look" stay two different answers. An unknown container raises
    :class:`tags.UnsupportedContainer`.
    """
    suffix = _require_art_container(path)
    try:
        handle = tags._open(path)
    except Exception as exc:  # noqa: BLE001 - mutagen raises many types
        raise UnreadableFile(f"could not read {path.name}: {exc}") from exc

    if suffix in tags.FLAC_SUFFIXES:
        return [
            _picture(pic.mime, bytes(pic.data), (pic.width, pic.height, pic.depth))
            for pic in handle.pictures
        ]

    if handle.tags is None:
        return []

    if suffix in tags.MP4_SUFFIXES:
        from mutagen.mp4 import MP4Cover

        mime_by_format = {MP4Cover.FORMAT_JPEG: JPEG_MIME, MP4Cover.FORMAT_PNG: "image/png"}
        return [
            _picture(mime_by_format.get(getattr(cover, "imageformat", None), ""), bytes(cover), None)
            for cover in handle.tags.get("covr", [])
        ]

    return [
        _picture(frame.mime, bytes(frame.data), None)
        for frame in handle.tags.getall("APIC")
    ]


def write_front_cover(path: Path, jpeg: bytes, *, max_bytes: int = ART_MAX_BYTES) -> bool:
    """Make ``jpeg`` the file's one embedded picture, a front cover.

    ``jpeg`` must already be what :func:`to_cdj_jpeg` returns: a baseline RGB
    JPEG no larger than ``max_bytes``. All of that is checked HERE, before the
    file is opened, so an unreadable image, a PNG, a progressive, greyscale or
    CMYK JPEG, or a picture over the cap raises :class:`ArtError` and the audio
    file is never touched. Embedding what a CDJ may render blank would be a
    write that reports success over art nobody sees. A caller that encoded to a
    different cap passes the same figure here.

    EVERY existing picture is removed, of any type, not only a previous front
    cover. That is the source system's behaviour and it is what makes a second
    write a replacement instead of an append.

    Returns True on success and False on any failure of the file itself,
    matching ``tags.write_tags``: one awkward file must not abort a batch. An
    unknown container raises rather than being guessed at.
    """
    suffix = _require_art_container(path)
    measured = _measure(jpeg)
    if measured is None:
        raise ArtError("the picture bytes could not be decoded, so nothing was written")
    if measured.format != "JPEG":
        raise ArtError(
            f"the picture is {measured.format}, not JPEG; pass it through to_cdj_jpeg first"
        )
    if measured.progressive:
        raise ArtError(
            "the picture is a progressive JPEG, which Pioneer players render "
            "blank; pass it through to_cdj_jpeg first"
        )
    if measured.mode != "RGB":
        raise ArtError(
            f"the picture is a {measured.mode} JPEG and only RGB is verified on "
            f"a player; pass it through to_cdj_jpeg first"
        )
    if len(jpeg) > max_bytes:
        raise ArtError(
            f"the picture is {len(jpeg)} bytes, over the {max_bytes} byte cap; "
            f"pass it through to_cdj_jpeg first"
        )

    try:
        handle = tags._open(path)

        if suffix in tags.FLAC_SUFFIXES:
            from mutagen.flac import Picture

            block = Picture()
            block.type = FRONT_COVER
            block.mime = JPEG_MIME
            block.desc = "Cover"
            block.data = jpeg
            block.width = measured.width
            block.height = measured.height
            block.depth = measured.depth
            block.colors = 0  # not an indexed image
            handle.clear_pictures()
            handle.add_picture(block)

        elif suffix in tags.MP4_SUFFIXES:
            from mutagen.mp4 import MP4Cover

            if handle.tags is None:
                handle.add_tags()
            handle.tags["covr"] = [MP4Cover(jpeg, imageformat=MP4Cover.FORMAT_JPEG)]

        else:
            from mutagen.id3 import APIC

            if handle.tags is None:
                # The chunk containers corrupt when a bare ID3 object is built
                # and saved against them. add_tags() is the container's own way.
                handle.add_tags()
            handle.tags.delall("APIC")
            handle.tags.add(
                APIC(encoding=3, mime=JPEG_MIME, type=FRONT_COVER, desc="Cover", data=jpeg)
            )

        tags._save(path, handle)
        return True
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort a batch
        log.debug("art write failed for %s: %s", path, exc)
        return False


#: What :func:`repair_in_place` found and did. ``UNCHECKED`` is not a kind of
#: ``NONE``: it says the repair did not look, because the container is not one
#: it repairs, and reporting that as "no art" would be absence read as evidence.
REPAIR_FIXED = "fixed"
REPAIR_OK = "ok"
REPAIR_NONE = "none"
REPAIR_ERROR = "error"
REPAIR_UNCHECKED = "unchecked"
REPAIR_STATUSES: tuple[str, ...] = (
    REPAIR_FIXED,
    REPAIR_OK,
    REPAIR_NONE,
    REPAIR_ERROR,
    REPAIR_UNCHECKED,
)


@dataclass(frozen=True)
class ArtRepair:
    """One file's repair status, and why, when the why is worth a sentence."""

    status: str
    detail: str = ""


def _repaired(data: bytes) -> tuple[CdjJpeg, bool]:
    """``data`` as CDJ safe art at native resolution, or shrunk when it must be.

    Native first, because upscaling only invents detail and a repair should not
    lose any either. A picture that does not fit the byte cap even at the lowest
    quality is then SHRUNK to fit inside :data:`ART_SIZE` on its longer edge,
    keeping its shape. Refusing it instead would leave the block blank on a
    player for good, which is worse than the source system, whose repair saved
    an over cap picture rather than none. Never enlarged: a picture already
    inside the box that does not fit has nothing a shrink can do for it.

    The flag says whether it was shrunk, so the report can say so.
    """
    try:
        return to_cdj_jpeg(data, size=None), False
    except ArtError:
        if _measure(data) is None:
            raise
    from PIL import Image, ImageOps

    try:
        with Image.open(io.BytesIO(data)) as source:
            img = _flatten_to_rgb(ImageOps.exif_transpose(source))
    except Exception as exc:  # noqa: BLE001 - Pillow raises many types on bad bytes
        raise ArtError(f"the image bytes could not be decoded: {exc}") from exc
    if max(img.size) <= ART_SIZE:
        raise ArtError(
            f"the picture does not fit in {ART_MAX_BYTES} bytes at {img.size[0]} by "
            f"{img.size[1]} pixels, and it is too small to shrink"
        )
    img.thumbnail((ART_SIZE, ART_SIZE), Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")  # lossless, so the one lossy step is the encoder's
    return to_cdj_jpeg(buffer.getvalue(), size=None), True


def _needs_repair(block) -> bool:
    """The source system's test: a zeroed dimension, or not a baseline JPEG.

    A block that declares any zero is what a Pioneer player renders blank even
    over a sound image. Data that does not decode, is not JPEG, or is
    progressive renders blank however the block is filled.
    """
    if block.width == 0 or block.height == 0 or block.depth == 0:
        return True
    measured = _measure(bytes(block.data))
    return measured is None or measured.format != "JPEG" or measured.progressive


def repair_in_place(path: Path) -> ArtRepair:
    """Make a FLAC's EXISTING pictures CDJ safe, without the web. Never raises.

    The vendored downloader embeds a picture block that declares a width,
    height and depth of zero, and the source system repaired exactly that. Every
    broken block is re-encoded at its NATIVE resolution, because upscaling only
    invents detail, and shrunk only when it cannot fit the byte cap otherwise,
    see :func:`_repaired`. Its dimensions are measured from the new bytes. Its
    type and description are kept, and so is every block that was sound, in
    order.

    A FILE WITH SOUND ART IS NOT WRITTEN, so its bytes and its mtime are what
    they were. If any block cannot be repaired the result is ``error`` and
    NOTHING is written, which is the source system's behaviour: a half repaired
    file would report fixed over a picture that still renders blank.

    FLAC only, which is parity. Any other container is ``unchecked``.

    NEVER RAISES, because the caller is one item of a tagging sweep and a
    picture that cannot be repaired must not stop the genre work on that file.
    Every failure, the file's or the image's, is an ``error`` with a sentence.
    """
    if path.suffix.lower() not in tags.FLAC_SUFFIXES:
        return ArtRepair(REPAIR_UNCHECKED, f"{path.suffix or 'no suffix'} is not repaired")
    try:
        handle = tags._open(path)
        blocks = list(handle.pictures)
    except Exception as exc:  # noqa: BLE001 - mutagen raises many types
        return ArtRepair(REPAIR_ERROR, f"could not read {path.name}: {exc}")
    if not blocks:
        return ArtRepair(REPAIR_NONE)
    broken = [block for block in blocks if _needs_repair(block)]
    if not broken:
        return ArtRepair(REPAIR_OK)
    shrunk = 0
    try:
        for block in broken:
            cdj, was_shrunk = _repaired(bytes(block.data))
            shrunk += was_shrunk
            block.data = cdj.data
            block.mime = JPEG_MIME
            block.width, block.height, block.depth = cdj.width, cdj.height, cdj.depth
            block.colors = 0  # not an indexed image
    except Exception as exc:  # noqa: BLE001 - the contract is never raises, not only ArtError
        return ArtRepair(REPAIR_ERROR, f"a picture could not be repaired: {exc}")
    try:
        handle.clear_pictures()
        for block in blocks:
            handle.add_picture(block)
        tags._save(path, handle)
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort a batch
        return ArtRepair(REPAIR_ERROR, f"the repaired art could not be saved: {exc}")
    detail = f"{len(broken)} of {len(blocks)} pictures re-encoded"
    if shrunk:
        detail += f", {shrunk} shrunk to fit {ART_SIZE} pixels"
    return ArtRepair(REPAIR_FIXED, detail)


__all__ = [
    "ART_MAX_BYTES",
    "ART_SIZE",
    "ART_SUFFIXES",
    "REPAIR_ERROR",
    "REPAIR_FIXED",
    "REPAIR_NONE",
    "REPAIR_OK",
    "REPAIR_STATUSES",
    "REPAIR_UNCHECKED",
    "ArtError",
    "ArtRepair",
    "CdjJpeg",
    "EmbeddedPicture",
    "UnreadableFile",
    "read_pictures",
    "repair_in_place",
    "to_cdj_jpeg",
    "write_front_cover",
]
