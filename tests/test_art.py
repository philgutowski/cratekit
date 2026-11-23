"""The art engine: a CDJ safe encoder, and a picture reader and writer per container.

Expected values come from a second reader, Pillow or mutagen, never the code
under test, over real containers, since a bare ID3 stream in an AIFF or a WAV
only shows in a real chunk table.
"""

from __future__ import annotations

import functools
import hashlib
import io
import random
import shutil
import subprocess
from pathlib import Path

import pytest
from PIL import Image

from cratekit.core import art, tags
from cratekit.core.art import (
    ArtError,
    UnreadableFile,
    read_pictures,
    to_cdj_jpeg,
    write_front_cover,
)
from tests._containers import synth_container

# The five containers the source system embedded art into.
CONTAINERS = [".flac", ".mp3", ".aiff", ".wav", ".m4a"]
ID3_CONTAINERS = [".mp3", ".aiff", ".wav"]


# Image builders


def _noise(width: int, height: int, mode: str = "RGB") -> Image.Image:
    """Incompressible pixels, so byte caps and quality steps are really exercised."""
    rng = random.Random(83)
    bands = len(Image.new(mode, (1, 1)).getbands())
    return Image.frombytes(mode, (width, height), rng.randbytes(width * height * bands))


def _encode(img: Image.Image, fmt: str, **options) -> bytes:
    buffer = io.BytesIO()
    img.save(buffer, format=fmt, **options)
    return buffer.getvalue()


@functools.cache
def _noise_png() -> bytes:
    """800 square noise as a PNG, built once: the tests only read the bytes."""
    return _encode(_noise(800, 800), "PNG")


def _gradient(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height))
    img.putdata([(x % 256, y % 256, (x + y) % 256) for y in range(height) for x in range(width)])
    return img


@functools.cache
def _baseline_jpeg(width: int = 320, height: int = 320) -> bytes:
    return _encode(_gradient(width, height), "JPEG", quality=85, progressive=False)


@functools.cache
def _progressive_jpeg(width: int = 320, height: int = 320) -> bytes:
    return _encode(_gradient(width, height), "JPEG", quality=85, progressive=True)


def _png(width: int = 64, height: int = 64) -> bytes:
    return _encode(_gradient(width, height), "PNG")


def _is_progressive(data: bytes) -> bool:
    with Image.open(io.BytesIO(data)) as img:
        return bool(img.info.get("progressive") or img.info.get("progression"))


def _decoded_md5(path: Path) -> str:
    """MD5 of the decoded sample stream, which is the thing that must not change."""
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-f", "md5", "-"],
        capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def _stored_pictures(path: Path) -> list[bytes]:
    """The raw picture payloads in ``path``, read by mutagen and not by ``art``."""
    import mutagen
    handle = mutagen.File(path)
    suffix = path.suffix.lower()
    if suffix == ".flac":
        return [bytes(p.data) for p in handle.pictures]
    if suffix == ".m4a":
        return [bytes(c) for c in (handle.tags or {}).get("covr", [])]
    return [bytes(f.data) for f in handle.tags.getall("APIC")] if handle.tags else []


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def _pristine(tmp_path_factory):
    """Each container synthesized once per module; every test writes on its own copy."""
    made: dict[str, Path] = {}

    def get(suffix: str) -> Path:
        if suffix not in made:
            made[suffix] = synth_container(tmp_path_factory.mktemp("pristine"), suffix)
        return made[suffix]

    return get


@pytest.fixture
def container(tmp_path, _pristine):
    """A fresh real container in this test's own directory."""
    def make(suffix: str) -> Path:
        path = tmp_path / f"probe{suffix}"
        shutil.copyfile(_pristine(suffix), path)
        return path

    return make


def _planted_mp3(container, *frames: dict) -> Path:
    """An mp3 carrying exactly these APIC frames, planted with mutagen, not ``art``."""
    from mutagen.id3 import APIC, ID3
    path = container(".mp3")
    planted = ID3()
    for frame in frames:
        planted.add(APIC(**{"encoding": 3, "mime": "image/jpeg", "type": 3, "desc": "", **frame}))
    planted.save(path)
    return path


def _planted_flac(container, kind: int, data: bytes) -> Path:
    """A flac carrying one picture block of ``kind``, its dimensions never set."""
    from mutagen.flac import FLAC, Picture
    path = container(".flac")
    handle = FLAC(path)
    block = Picture()
    block.type = kind
    block.mime = "image/jpeg"
    block.data = data
    handle.add_picture(block)
    handle.save()
    return path


# The encoder


def test_the_fixture_builders_make_what_they_say():
    # Every progressive test below is vacuous if Pillow quietly wrote baseline.
    assert _is_progressive(_progressive_jpeg())
    assert not _is_progressive(_baseline_jpeg())


def test_a_progressive_rgba_png_comes_out_a_baseline_rgb_jpeg_under_the_cap():
    source = _encode(_noise(1200, 1200, "RGBA"), "PNG")
    cap = 200_000
    result = to_cdj_jpeg(source, max_bytes=cap)
    assert len(result.data) <= cap
    with Image.open(io.BytesIO(result.data)) as img:
        assert img.format == "JPEG"
        assert img.mode == "RGB"
        assert img.size == (800, 800)
    assert not _is_progressive(result.data)


def test_a_progressive_jpeg_input_comes_out_baseline():
    assert not _is_progressive(to_cdj_jpeg(_progressive_jpeg(900, 900)).data)


def test_the_reported_dimensions_match_what_pillow_reads_back():
    result = to_cdj_jpeg(_baseline_jpeg(500, 400))
    with Image.open(io.BytesIO(result.data)) as img:
        assert (result.width, result.height) == img.size == (800, 800)
    assert result.depth == 24


def test_size_none_keeps_the_native_resolution():
    result = to_cdj_jpeg(_baseline_jpeg(640, 480), size=None)
    with Image.open(io.BytesIO(result.data)) as img:
        assert img.size == (640, 480)
    assert (result.width, result.height) == (640, 480)


def test_quality_steps_down_until_the_picture_fits():
    roomy = to_cdj_jpeg(_noise_png(), max_bytes=10_000_000)
    cap = len(roomy.data) - 1  # just under the first attempt forces a step down
    squeezed = to_cdj_jpeg(_noise_png(), max_bytes=cap)
    assert len(squeezed.data) <= cap
    assert len(squeezed.data) < len(roomy.data)


def test_a_picture_that_cannot_fit_raises_rather_than_exceeding_the_cap():
    with pytest.raises(ArtError, match="does not fit"):
        to_cdj_jpeg(_noise_png(), max_bytes=5_000)


def test_the_encoder_never_goes_below_the_quality_floor():
    # One byte under what quality 50 really produces: a floor lowered to 45
    # would satisfy that cap and return instead of raising.
    pixels = _noise(800, 800)
    at_floor = len(_encode(pixels, "JPEG", quality=50, optimize=True, progressive=False))
    assert len(to_cdj_jpeg(_noise_png(), max_bytes=at_floor).data) == at_floor
    with pytest.raises(ArtError):
        to_cdj_jpeg(_noise_png(), max_bytes=at_floor - 1)


def test_an_exif_orientation_is_baked_into_the_pixels():
    # Red left, blue right, stored "rotate 90 to display": the re-encode drops
    # the tag, so the rotation must be applied first. Judged by Pillow's transpose.
    from PIL import ImageOps

    img = Image.new("RGB", (400, 200), (255, 0, 0))
    img.paste((0, 0, 255), (200, 0, 400, 200))
    exif = Image.Exif()
    exif[0x0112] = 6
    source = _encode(img, "JPEG", quality=95, exif=exif)
    with Image.open(io.BytesIO(source)) as tagged:
        upright = ImageOps.exif_transpose(tagged).convert("RGB")
    assert upright.size == (200, 400)

    result = to_cdj_jpeg(source, size=None)

    with Image.open(io.BytesIO(result.data)) as out:
        assert out.size == upright.size
        for spot in [(100, 50), (100, 350)]:
            got, want = out.convert("RGB").getpixel(spot), upright.getpixel(spot)
            assert all(abs(a - b) < 40 for a, b in zip(got, want)), (spot, got, want)


@pytest.mark.parametrize("mode", ["RGBA", "LA", "P"])
def test_transparency_is_flattened_onto_white_not_onto_what_lies_under_it(mode):
    # Clear pixels stored as black, as most tools export a logo.
    clear = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    if mode == "P":
        clear = Image.new("P", (64, 64), 0)
        clear.putpalette([0, 0, 0] * 256)
        source = _encode(clear, "PNG", transparency=0)
    else:
        source = _encode(clear.convert(mode), "PNG")
    result = to_cdj_jpeg(source, size=None)
    with Image.open(io.BytesIO(result.data)) as out:
        assert all(channel > 240 for channel in out.convert("RGB").getpixel((32, 32)))


def test_unreadable_image_bytes_raise_from_the_encoder():
    with pytest.raises(ArtError, match="could not be decoded"):
        to_cdj_jpeg(b"this is not an image")


# The writer, per container


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_an_art_write_leaves_the_decoded_audio_unchanged(container, suffix):
    path = container(suffix)
    before = _decoded_md5(path)
    assert write_front_cover(path, _baseline_jpeg()) is True
    assert _decoded_md5(path) == before


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next(
    container, suffix
):
    path = container(suffix)
    first, second = _baseline_jpeg(320, 240), _baseline_jpeg(200, 200)
    assert write_front_cover(path, first) is True
    assert _stored_pictures(path) == [first]

    (picture,) = read_pictures(path)
    assert picture.data == first
    assert picture.mime == "image/jpeg"
    assert (picture.width, picture.height, picture.depth) == (320, 240, 24)
    assert picture.decoded is True
    assert picture.progressive is False
    assert picture.format == "JPEG"

    assert write_front_cover(path, second) is True
    assert _stored_pictures(path) == [second]


def test_the_flac_block_carries_nonzero_width_height_and_depth(container):
    from mutagen.flac import FLAC
    path = container(".flac")
    assert write_front_cover(path, _baseline_jpeg(320, 240)) is True
    (block,) = FLAC(path).pictures
    with Image.open(io.BytesIO(block.data)) as img:
        assert (block.width, block.height) == img.size == (320, 240)
    assert block.depth == 24
    assert block.colors == 0
    assert block.type == 3
    assert block.mime == "image/jpeg"


def test_a_flac_picture_of_another_type_is_replaced_too(container):
    path = _planted_flac(container, 4, _baseline_jpeg(100, 100))
    assert write_front_cover(path, _baseline_jpeg()) is True
    assert _stored_pictures(path) == [_baseline_jpeg()]


@pytest.mark.parametrize("suffix", ID3_CONTAINERS)
def test_an_id3_picture_another_tool_embedded_is_replaced_too(container, suffix):
    # Under a different description: ID3 keys a picture by it, so re-adding
    # "Cover" over "Cover" would prove nothing about the clearing.
    import mutagen
    from mutagen.id3 import APIC

    path = container(suffix)
    handle = mutagen.File(path)
    if handle.tags is None:
        handle.add_tags()
    handle.tags.add(
        APIC(encoding=3, mime="image/jpeg", type=4, desc="from elsewhere",
             data=_progressive_jpeg(100, 100))
    )
    handle.save()
    assert len(_stored_pictures(path)) == 1

    assert write_front_cover(path, _baseline_jpeg()) is True

    assert _stored_pictures(path) == [_baseline_jpeg()]


@pytest.mark.parametrize("suffix", ID3_CONTAINERS)
def test_the_id3_frame_is_a_front_cover_jpeg(container, suffix):
    import mutagen
    path = container(suffix)
    assert write_front_cover(path, _baseline_jpeg()) is True
    (frame,) = mutagen.File(path).tags.getall("APIC")
    assert frame.type == 3
    assert frame.mime == "image/jpeg"


def test_the_mp4_cover_is_declared_jpeg(container):
    from mutagen.mp4 import MP4, MP4Cover
    path = container(".m4a")
    assert write_front_cover(path, _baseline_jpeg()) is True
    (cover,) = MP4(path).tags["covr"]
    assert cover.imageformat == MP4Cover.FORMAT_JPEG


@pytest.mark.parametrize("suffix,magic", [(".aiff", b"FORM"), (".wav", b"RIFF")])
def test_a_chunk_container_never_receives_a_bare_id3_stream(container, suffix, magic):
    path = container(suffix)
    assert write_front_cover(path, _baseline_jpeg()) is True
    head = path.read_bytes()[:4]
    assert head == magic, f"{suffix} now opens with {head!r}, the container is corrupt"


def test_an_mp3_id3v1_trailer_survives_the_write(container):
    # Both tags, disagreeing: a lone v1 trailer survives a plain save, which
    # rewrites a v1 genre byte beside an unlisted v2 genre to 255.
    import mutagen.id3 as id3
    from mutagen.mp3 import MP3

    path = container(".mp3")
    handle = MP3(path)
    if handle.tags is None:
        handle.add_tags()
    handle.tags["TCON"] = id3.TCON(encoding=3, text=["A Genre ID3v1 Never Listed"])
    handle.save(v1=2)
    raw = bytearray(path.read_bytes())
    assert raw[-128:-125] == b"TAG"
    raw[-1] = 31
    path.write_bytes(bytes(raw))
    trailer = bytes(raw[-128:])

    assert write_front_cover(path, _baseline_jpeg()) is True

    assert path.read_bytes()[-128:] == trailer


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_text_tags_written_before_the_art_survive_it(container, suffix):
    path = container(suffix)
    assert tags.write_tags(path, {"genre": "Probe Genre", "artist": "Probe Artist"})
    assert write_front_cover(path, _baseline_jpeg()) is True
    assert tags.read_tag(path, "genre") == "Probe Genre"
    assert tags.read_tag(path, "artist") == "Probe Artist"


def test_a_tempo_frame_another_tool_wrote_is_left_exactly_alone(container):
    # Never touching a tempo includes never deleting one; planted with mutagen,
    # since nothing in the package can write one.
    from mutagen.id3 import ID3, TBPM
    path = container(".mp3")
    planted = ID3()
    planted.add(TBPM(encoding=3, text=["124"]))
    planted.save(path)
    assert write_front_cover(path, _baseline_jpeg()) is True
    assert [str(t) for t in ID3(path).getall("TBPM")[0].text] == ["124"]


# What the writer refuses


REFUSALS = [
    *[(suffix, lambda: b"\xff\xd8 not really a jpeg", "could not be decoded", None)
      for suffix in CONTAINERS],
    (".flac", _progressive_jpeg, "progressive", None),
    (".mp3", _png, "not JPEG", None),
    *[(".aiff", lambda m=mode: _encode(_gradient(64, 64).convert(m), "JPEG", progressive=False),
       "only RGB", mode) for mode in ("L", "CMYK")],
]


@pytest.mark.parametrize(
    "suffix,picture,match,mode",
    REFUSALS,
    ids=[f"unreadable{s}" for s in CONTAINERS] + ["progressive", "png", "jpeg-L", "jpeg-CMYK"],
)
def test_a_refused_picture_fails_and_leaves_the_file_untouched(
    container, suffix, picture, match, mode
):
    path = container(suffix)
    before = _digest(path)
    data = picture()
    if mode is not None:
        with Image.open(io.BytesIO(data)) as check:
            assert check.mode == mode and check.format == "JPEG"
    with pytest.raises(ArtError, match=match):
        write_front_cover(path, data)
    assert _digest(path) == before


def test_a_picture_over_the_cap_is_refused_and_the_file_untouched(container):
    path = container(".wav")
    before = _digest(path)
    jpeg = _baseline_jpeg()
    with pytest.raises(ArtError, match="over the"):
        write_front_cover(path, jpeg, max_bytes=len(jpeg) - 1)
    assert _digest(path) == before
    # The cap is inclusive, the same way the encoder's is.
    assert write_front_cover(path, jpeg, max_bytes=len(jpeg)) is True


def test_the_writer_default_cap_is_the_encoder_default_cap(container):
    path = container(".flac")
    big = _encode(_noise(1600, 1600), "JPEG", quality=95, progressive=False)
    assert len(big) > 450_000
    with pytest.raises(ArtError, match="over the"):
        write_front_cover(path, big)


@pytest.mark.parametrize("suffix", [".ogg", ".opus", ".xyz", ""])
def test_a_container_without_verified_picture_handling_raises(tmp_path, suffix):
    path = tmp_path / f"probe{suffix}"
    path.write_bytes(b"anything")
    with pytest.raises(tags.UnsupportedContainer):
        write_front_cover(path, _baseline_jpeg())
    with pytest.raises(tags.UnsupportedContainer):
        read_pictures(path)
    assert path.read_bytes() == b"anything"


def test_the_container_check_comes_before_the_image_check(tmp_path):
    # The container is the refusal no better image would ever clear.
    with pytest.raises(tags.UnsupportedContainer):
        write_front_cover(tmp_path / "probe.ogg", b"junk")


def test_a_write_to_a_missing_file_returns_false(tmp_path):
    assert write_front_cover(tmp_path / "absent.flac", _baseline_jpeg()) is False


def test_the_supported_set_is_the_five_source_containers_and_derived_from_tags():
    assert set(art.ART_SUFFIXES) == set(
        tags.FLAC_SUFFIXES
        + tags.MP3_SUFFIXES
        + tags.AIFF_SUFFIXES
        + tags.WAVE_SUFFIXES
        + tags.MP4_SUFFIXES
    )
    assert not set(art.ART_SUFFIXES) & set(tags.VORBIS_FILE_SUFFIXES)
    assert set(art.ART_SUFFIXES) <= set(tags.SUPPORTED_SUFFIXES)


# The reader


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_a_file_with_no_art_reads_as_an_empty_list(container, suffix):
    assert read_pictures(container(suffix)) == []


def test_a_png_mislabelled_as_jpeg_reads_with_both_facts(container):
    # The claimed mime and the measured format side by side, so neither is read as the other.
    (picture,) = read_pictures(_planted_mp3(container, {"data": _png()}))
    assert picture.mime == "image/jpeg"
    assert picture.format == "PNG"


def test_each_listed_mode_reads_with_its_own_depth(container):
    one_bit = _encode(Image.new("1", (32, 32), 1), "PNG")
    wide = _encode(Image.new("I;16", (32, 32), 1000), "PNG")
    path = _planted_mp3(
        container,
        {"mime": "image/png", "desc": "a", "data": one_bit},
        {"mime": "image/png", "type": 4, "desc": "b", "data": wide},
    )
    depths = {p.data: p.depth for p in read_pictures(path)}
    assert depths[one_bit] == 1
    assert depths[wide] == 16


def test_a_mode_with_no_known_depth_reads_as_zero_not_as_a_guess(container, monkeypatch):
    # A mode Pillow adds one day, stood in for by taking a real one out of the table.
    one_bit = _encode(Image.new("1", (32, 32), 1), "PNG")
    path = _planted_mp3(container, {"mime": "image/png", "data": one_bit})
    monkeypatch.delitem(art._DEPTH_BY_MODE, "1")
    (picture,) = read_pictures(path)
    assert picture.decoded is True
    assert picture.depth == 0


def test_a_zeroed_flac_block_reads_as_zeroes_not_as_the_decoded_size(container):
    # The vendored downloader's defect: the reader reports what the block tells a player.
    (picture,) = read_pictures(_planted_flac(container, 3, _baseline_jpeg(320, 320)))
    assert (picture.width, picture.height, picture.depth) == (0, 0, 0)
    assert picture.decoded is True


def test_a_progressive_picture_another_tool_embedded_is_flagged(container):
    (picture,) = read_pictures(_planted_mp3(container, {"data": _progressive_jpeg()}))
    assert picture.progressive is True
    assert picture.decoded is True


def test_an_undecodable_embedded_picture_says_so(container):
    (picture,) = read_pictures(_planted_mp3(container, {"data": b"garbage"}))
    assert picture.decoded is False
    assert picture.format is None
    assert (picture.width, picture.height, picture.depth) == (0, 0, 0)
    assert picture.data == b"garbage"


def test_a_truncated_picture_does_not_read_as_decoded(container):
    # It opens cleanly and fails only on a full decode, which the reader pays for.
    whole = _baseline_jpeg(320, 320)
    cut = whole[: len(whole) // 2]
    with Image.open(io.BytesIO(cut)) as opens:
        assert opens.size == (320, 320)
    (picture,) = read_pictures(_planted_mp3(container, {"data": cut}))
    assert picture.decoded is False


def test_an_mp4_png_cover_reads_with_its_own_mime(container):
    from mutagen.mp4 import MP4, MP4Cover
    path = container(".m4a")
    handle = MP4(path)
    handle.tags["covr"] = [MP4Cover(_png(64, 48), MP4Cover.FORMAT_PNG)]
    handle.save()
    (picture,) = read_pictures(path)
    assert picture.mime == "image/png"
    assert (picture.width, picture.height) == (64, 48)


def test_a_file_that_cannot_be_read_raises_rather_than_reading_as_no_art(tmp_path):
    broken = tmp_path / "broken.flac"
    broken.write_bytes(b"not a flac at all")
    with pytest.raises(UnreadableFile, match="could not read"):
        read_pictures(broken)
    with pytest.raises(UnreadableFile, match="could not read"):
        read_pictures(tmp_path / "absent.mp3")
    # A verdict on a file is not a verdict on an image.
    assert not issubclass(UnreadableFile, ArtError)
