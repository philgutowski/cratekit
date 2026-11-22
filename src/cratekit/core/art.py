"""Album art: one CDJ safe encoder, one reader and one writer per container.

Not a field in ``tags``: ``tags.FIELDS`` is a closed table of TEXT fields and
its being closed enforces the beat grid rule. This module borrows ``tags._open``
and ``tags._save`` instead, so art and tags classify containers through one
table and a bare ID3 stream is never written into an AIFF or a WAV.

CDJ SAFE. Pioneer players show a PROGRESSIVE JPEG as a blank square, and a FLAC
picture block that DECLARES zero width, height or depth renders blank over a
sound image. So the encoder never emits progressive, and the writer fills the
FLAC block from Pillow decoding the bytes it is given, never from a caller.

``.ogg`` and ``.opus`` pictures (a base64 comment) are refused, unverified.
Nothing here reads, writes or deletes a tempo value in any container.
"""

from __future__ import annotations

import hashlib
import io
import logging
import threading
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

from cratekit.core import tags

log = logging.getLogger(__name__)

#: The edge, in pixels, of newly embedded art.
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
#: conversion exposes the colour under the transparency, usually black.
_FLATTEN_ONTO = (255, 255, 255)

#: The containers with verified picture handling, derived from the tag module's
#: own suffix tuples so a suffix added there is not half supported here.
ART_SUFFIXES: tuple[str, ...] = tuple(sorted(
    tags.FLAC_SUFFIXES + tags.MP3_SUFFIXES + tags.AIFF_SUFFIXES + tags.WAVE_SUFFIXES
    + tags.MP4_SUFFIXES
))


class ArtError(ValueError):
    """Image bytes that cannot be made into, or are not, CDJ safe art."""


class UnreadableFile(Exception):
    """An audio file whose pictures could not be looked at, for any reason.

    Not an :class:`ArtError`, a verdict on image bytes: an unmounted library is not bad art.
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

    ``width``, ``height`` and ``depth`` are WHAT A PLAYER IS TOLD: a FLAC block's
    declared values, zeroes included, else the decoded values, zero when the data
    does not decode. ``progressive`` means something only when ``decoded``.
    """

    mime: str
    width: int
    height: int
    depth: int
    progressive: bool
    decoded: bool
    data: bytes
    #: What Pillow found the bytes to BE, "JPEG" or "PNG", or None when they did
    #: not decode. ``mime`` is only what the container claims.
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

    A FULL decode, since a truncated picture opens cleanly, fails only on
    ``load`` and renders blank on a player.
    """
    from PIL import Image

    try:
        with Image.open(io.BytesIO(data)) as img:
            img.load()
            progressive = bool(img.info.get("progressive") or img.info.get("progression"))
            width, height = img.size
            return _Measured(
                format=img.format, mode=img.mode, width=width, height=height,
                depth=_DEPTH_BY_MODE.get(img.mode, 0), progressive=progressive,
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

    Stepping 88 down by 5 skips 50, so the floor is added as the last rung.
    """
    rungs = list(range(ART_START_QUALITY, ART_MIN_QUALITY, -ART_QUALITY_STEP))
    return [*rungs, ART_MIN_QUALITY]


def _decoded_rgb(data: bytes):
    """``data`` decoded, its EXIF orientation baked in and flattened to RGB, or ArtError."""
    from PIL import Image, ImageOps

    try:
        with Image.open(io.BytesIO(data)) as source:
            return _flatten_to_rgb(ImageOps.exif_transpose(source))
    except Exception as exc:  # noqa: BLE001 - Pillow raises many types on bad bytes
        raise ArtError(f"the image bytes could not be decoded: {exc}") from exc


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

    ``size`` is the square edge for NEW art, a non square image resized without
    cropping; ``None`` keeps the native resolution, for a repair. An EXIF
    orientation is baked in and transparency flattened onto white first.
    Quality steps down until the picture fits, and one that does not fit at
    :data:`ART_MIN_QUALITY` raises rather than exceeding the cap. The returned
    dimensions and depth are measured from the encoded bytes.
    """
    from PIL import Image

    img = _decoded_rgb(data)

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


# The encode, remembered for the life of the process (U260).

#: How many encoded covers one process keeps, the least recently used dropped
#: first. An album's files usually sit together in a sweep.
COVER_MEMORY = 4

_remembered: OrderedDict[tuple[bytes, int, int | None, int], CdjJpeg] = OrderedDict()
_remembered_lock = threading.Lock()


def to_cdj_jpeg_remembered(
    data: bytes, *, size: int | None = ART_SIZE, max_bytes: int = ART_MAX_BYTES
) -> CdjJpeg:
    """:func:`to_cdj_jpeg`, made once per picture while the picture is remembered.

    The encode is a pure function of its arguments, so the first answer is
    every later one. KEYED ON WHAT MAKES THE PICTURE: a SHA 256 digest of the
    bytes and their length, with the edge and the byte cap, never on where it
    came from. A REFUSAL IS NEVER REMEMBERED, so :class:`ArtError` propagates
    and the next call encodes again. Holds :data:`COVER_MEMORY` pictures, the
    least recently used dropped first, and nothing across processes.
    """
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
    with _remembered_lock:
        made = _remembered.get(key)
        if made is not None:
            _remembered.move_to_end(key)
            return made
    made = to_cdj_jpeg(data, size=size, max_bytes=max_bytes)
    with _remembered_lock:
        _remembered[key] = made
        _remembered.move_to_end(key)
        while len(_remembered) > COVER_MEMORY:
            _remembered.popitem(last=False)
    return made


def reset_cache() -> None:
    """Forget every remembered encode. The suite calls it around every test."""
    with _remembered_lock:
        _remembered.clear()


def decodes(data: bytes) -> bool:
    """Whether Pillow decodes ``data`` in full, the test a remembered fetch admits by (U260)."""
    return _measure(data) is not None


def _picture(mime: str, data: bytes, declared: tuple[int, int, int] | None) -> EmbeddedPicture:
    measured = _measure(data)
    if declared is not None:
        width, height, depth = declared
    elif measured is not None:
        width, height, depth = measured.width, measured.height, measured.depth
    else:
        width = height = depth = 0
    return EmbeddedPicture(
        mime=mime, width=width, height=height, depth=depth,
        progressive=measured.progressive if measured is not None else False,
        decoded=measured is not None, data=data,
        format=measured.format if measured is not None else None,
    )


def read_pictures(path: Path) -> list[EmbeddedPicture]:
    """Every picture embedded in ``path``, in the order the container holds them.

    An empty list means the file holds no picture; a file that could not be
    read raises :class:`UnreadableFile`, and an unknown container
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

    ``jpeg`` must already be what :func:`to_cdj_jpeg` returns, a baseline RGB
    JPEG no larger than ``max_bytes``, checked HERE before the file is opened:
    anything else raises :class:`ArtError` and the audio file is never touched.
    EVERY existing picture is removed, of any type, so a second write replaces.
    True on success, False on any failure of the file itself; an unknown
    container raises.
    """
    suffix = _require_art_container(path)
    measured = _measure(jpeg)
    if measured is None:
        raise ArtError("the picture bytes could not be decoded, so nothing was written")
    fix = "; pass it through to_cdj_jpeg first"
    if measured.format != "JPEG":
        raise ArtError(f"the picture is {measured.format}, not JPEG{fix}")
    if measured.progressive:
        raise ArtError(
            f"the picture is a progressive JPEG, which Pioneer players render blank{fix}"
        )
    if measured.mode != "RGB":
        raise ArtError(
            f"the picture is a {measured.mode} JPEG and only RGB is verified on a player{fix}"
        )
    if len(jpeg) > max_bytes:
        raise ArtError(f"the picture is {len(jpeg)} bytes, over the {max_bytes} byte cap{fix}")

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
#: ``NONE``: the repair did not look, so it says nothing about the art.
REPAIR_FIXED = "fixed"
REPAIR_OK = "ok"
REPAIR_NONE = "none"
REPAIR_ERROR = "error"
REPAIR_UNCHECKED = "unchecked"
REPAIR_STATUSES: tuple[str, ...] = (
    REPAIR_FIXED, REPAIR_OK, REPAIR_NONE, REPAIR_ERROR, REPAIR_UNCHECKED
)


@dataclass(frozen=True)
class ArtRepair:
    """One file's repair status, and why, when the why is worth a sentence."""

    status: str
    detail: str = ""


def _repaired(data: bytes) -> tuple[CdjJpeg, bool]:
    """``data`` as CDJ safe art at native resolution, or shrunk when it must be.

    Native first, since upscaling only invents detail. A picture over the byte
    cap even at the lowest quality is SHRUNK inside :data:`ART_SIZE` on its
    longer edge, keeping its shape, rather than left blank on a player. Never
    enlarged. The flag says whether it was shrunk.
    """
    try:
        return to_cdj_jpeg(data, size=None), False
    except ArtError:
        if _measure(data) is None:
            raise
    from PIL import Image

    img = _decoded_rgb(data)
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
    """A zeroed declared dimension, or data that is not a decodable baseline JPEG.

    Either renders blank on a Pioneer player.
    """
    if block.width == 0 or block.height == 0 or block.depth == 0:
        return True
    measured = _measure(bytes(block.data))
    return measured is None or measured.format != "JPEG" or measured.progressive


def repair_in_place(path: Path) -> ArtRepair:
    """Make a FLAC's EXISTING pictures CDJ safe, without the web. Never raises.

    The vendored downloader embeds blocks declaring zero dimensions. Every
    broken block is re-encoded by :func:`_repaired` and its dimensions measured
    from the new bytes; its type and description are kept, and so is every
    sound block, in order. A FILE WITH SOUND ART IS NOT WRITTEN, and if any
    block cannot be repaired the result is ``error`` and NOTHING is written.
    FLAC only; any other container is ``unchecked``. Never raises, since the
    caller is one item of a tagging sweep: every failure is an ``error``.
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
    "ART_MAX_BYTES", "ART_SIZE", "ART_SUFFIXES", "COVER_MEMORY", "REPAIR_ERROR", "REPAIR_FIXED",
    "REPAIR_NONE", "REPAIR_OK", "REPAIR_STATUSES", "REPAIR_UNCHECKED", "ArtError", "ArtRepair",
    "CdjJpeg", "EmbeddedPicture", "UnreadableFile", "decodes", "read_pictures", "repair_in_place",
    "reset_cache", "to_cdj_jpeg", "to_cdj_jpeg_remembered", "write_front_cover",
]
