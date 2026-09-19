"""The art engine: a CDJ safe encoder, and a picture reader and writer per container.

Two rules shape every test in this file.

EXPECTED VALUES COME FROM A SECOND READER, NEVER FROM THE CODE UNDER TEST. What
the encoder produced is judged by Pillow opening the bytes. What the writer put
in a file is judged by mutagen opening the file, and by Pillow opening the
picture mutagen hands back. An assertion comparing the encoder's reported width
with the writer's stored width would be X equals X, and would pass on an encoder
that reports 800 and emits 640.

THE FILES ARE REAL CONTAINERS. They are synthesized with ffmpeg by the same
helper the tag suite uses, because the corruption this module must not cause
(a bare ID3 stream at the front of an AIFF or a WAV) only shows up in a real
chunk table.
"""

from __future__ import annotations

import hashlib
import io
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


# ───────────────────────────── image builders ──────────────────────────────


def _noise(width: int, height: int, mode: str = "RGB") -> Image.Image:
    """Incompressible pixels, so byte caps and quality steps are really exercised."""
    import random

    rng = random.Random(83)
    bands = len(Image.new(mode, (1, 1)).getbands())
    return Image.frombytes(mode, (width, height), rng.randbytes(width * height * bands))


def _encode(img: Image.Image, fmt: str, **options) -> bytes:
    buffer = io.BytesIO()
    img.save(buffer, format=fmt, **options)
    return buffer.getvalue()


def _gradient(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height))
    img.putdata([(x % 256, y % 256, (x + y) % 256) for y in range(height) for x in range(width)])
    return img


def _baseline_jpeg(width: int = 320, height: int = 320) -> bytes:
    return _encode(_gradient(width, height), "JPEG", quality=85, progressive=False)


def _progressive_jpeg(width: int = 320, height: int = 320) -> bytes:
    return _encode(_gradient(width, height), "JPEG", quality=85, progressive=True)


def _is_progressive(data: bytes) -> bool:
    with Image.open(io.BytesIO(data)) as img:
        return bool(img.info.get("progressive") or img.info.get("progression"))


def _decoded_md5(path: Path) -> str:
    """MD5 of the DECODED sample stream, which is the thing that must not change."""
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


# ═══════════════════════════════════════════════════════════════════════════
# The encoder
# ═══════════════════════════════════════════════════════════════════════════


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
    result = to_cdj_jpeg(_progressive_jpeg(900, 900))

    assert not _is_progressive(result.data)


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
    source = _encode(_noise(800, 800), "PNG")
    roomy = to_cdj_jpeg(source, max_bytes=10_000_000)
    # A cap just under the first attempt forces at least one step down.
    cap = len(roomy.data) - 1

    squeezed = to_cdj_jpeg(source, max_bytes=cap)

    assert len(squeezed.data) <= cap
    assert len(squeezed.data) < len(roomy.data)


def test_a_picture_that_cannot_fit_raises_rather_than_exceeding_the_cap():
    source = _encode(_noise(800, 800), "PNG")

    with pytest.raises(ArtError, match="does not fit"):
        to_cdj_jpeg(source, max_bytes=5_000)


def test_the_encoder_never_goes_below_the_quality_floor():
    # The floor is what the refusal protects. Find the size quality 50 really
    # produces with Pillow, then ask for one byte less: a floor lowered to 45
    # would satisfy that cap and return instead of raising.
    pixels = _noise(800, 800)
    at_floor = len(_encode(pixels, "JPEG", quality=50, optimize=True, progressive=False))

    assert len(to_cdj_jpeg(_encode(pixels, "PNG"), max_bytes=at_floor).data) == at_floor
    with pytest.raises(ArtError):
        to_cdj_jpeg(_encode(pixels, "PNG"), max_bytes=at_floor - 1)


def test_an_exif_orientation_is_baked_into_the_pixels():
    # Left half red, right half blue, stored with "rotate 90 to display". The
    # re-encode drops the tag, so unless the rotation is applied first the cover
    # is sideways for good. Expected geometry comes from Pillow's own transpose.
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
    # Fully transparent pixels stored as black, which is how most tools export
    # a logo. A plain mode conversion turns the whole cover black.
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


# ═══════════════════════════════════════════════════════════════════════════
# The writer, per container
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_an_art_write_leaves_the_decoded_audio_unchanged(tmp_path, suffix):
    path = synth_container(tmp_path, suffix)
    before = _decoded_md5(path)

    assert write_front_cover(path, _baseline_jpeg()) is True

    assert _decoded_md5(path) == before


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_the_written_picture_is_the_bytes_that_were_given(tmp_path, suffix):
    path = synth_container(tmp_path, suffix)
    jpeg = _baseline_jpeg()

    assert write_front_cover(path, jpeg) is True

    assert _stored_pictures(path) == [jpeg]


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_a_second_write_replaces_the_picture_rather_than_appending(tmp_path, suffix):
    path = synth_container(tmp_path, suffix)
    first, second = _baseline_jpeg(300, 300), _baseline_jpeg(200, 200)

    assert write_front_cover(path, first) is True
    assert write_front_cover(path, second) is True

    assert _stored_pictures(path) == [second]


def test_the_flac_block_carries_nonzero_width_height_and_depth(tmp_path):
    from mutagen.flac import FLAC

    path = synth_container(tmp_path, ".flac")
    jpeg = _baseline_jpeg(320, 240)

    assert write_front_cover(path, jpeg) is True

    (block,) = FLAC(path).pictures
    with Image.open(io.BytesIO(block.data)) as img:
        assert (block.width, block.height) == img.size == (320, 240)
    assert block.depth == 24
    assert block.colors == 0
    assert block.type == 3
    assert block.mime == "image/jpeg"


def test_a_flac_picture_of_another_type_is_replaced_too(tmp_path):
    from mutagen.flac import FLAC, Picture

    path = synth_container(tmp_path, ".flac")
    handle = FLAC(path)
    back = Picture()
    back.type = 4
    back.mime = "image/jpeg"
    back.data = _baseline_jpeg(100, 100)
    handle.add_picture(back)
    handle.save()

    jpeg = _baseline_jpeg()
    assert write_front_cover(path, jpeg) is True

    assert _stored_pictures(path) == [jpeg]


@pytest.mark.parametrize("suffix", ID3_CONTAINERS)
def test_an_id3_picture_another_tool_embedded_is_replaced_too(tmp_path, suffix):
    # A frame under a DIFFERENT description, which is the case that matters:
    # ID3 keys a picture by its description, so re-adding "Cover" replaces
    # "Cover" with no help from anybody and proves nothing about the clearing.
    import mutagen
    from mutagen.id3 import APIC

    path = synth_container(tmp_path, suffix)
    handle = mutagen.File(path)
    if handle.tags is None:
        handle.add_tags()
    handle.tags.add(
        APIC(encoding=3, mime="image/jpeg", type=4, desc="from elsewhere",
             data=_progressive_jpeg(100, 100))
    )
    handle.save()
    assert len(_stored_pictures(path)) == 1

    jpeg = _baseline_jpeg()
    assert write_front_cover(path, jpeg) is True

    assert _stored_pictures(path) == [jpeg]


@pytest.mark.parametrize("suffix", ID3_CONTAINERS)
def test_the_id3_frame_is_a_front_cover_jpeg(tmp_path, suffix):
    import mutagen

    path = synth_container(tmp_path, suffix)

    assert write_front_cover(path, _baseline_jpeg()) is True

    (frame,) = mutagen.File(path).tags.getall("APIC")
    assert frame.type == 3
    assert frame.mime == "image/jpeg"


def test_the_mp4_cover_is_declared_jpeg(tmp_path):
    from mutagen.mp4 import MP4, MP4Cover

    path = synth_container(tmp_path, ".m4a")

    assert write_front_cover(path, _baseline_jpeg()) is True

    (cover,) = MP4(path).tags["covr"]
    assert cover.imageformat == MP4Cover.FORMAT_JPEG


@pytest.mark.parametrize("suffix,magic", [(".aiff", b"FORM"), (".wav", b"RIFF")])
def test_a_chunk_container_never_receives_a_bare_id3_stream(tmp_path, suffix, magic):
    path = synth_container(tmp_path, suffix)

    assert write_front_cover(path, _baseline_jpeg()) is True

    head = path.read_bytes()[:4]
    assert head == magic, f"{suffix} now opens with {head!r}, the container is corrupt"


def test_an_mp3_id3v1_trailer_survives_the_write(tmp_path):
    path = synth_container(tmp_path, ".mp3")
    trailer = b"TAG" + b"Legacy Title".ljust(30, b"\0") + b"\0" * 94 + bytes([17])
    assert len(trailer) == 128
    with path.open("ab") as handle:
        handle.write(trailer)

    assert write_front_cover(path, _baseline_jpeg()) is True

    assert path.read_bytes()[-128:] == trailer


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_text_tags_written_before_the_art_survive_it(tmp_path, suffix):
    path = synth_container(tmp_path, suffix)
    assert tags.write_tags(path, {"genre": "Probe Genre", "artist": "Probe Artist"})

    assert write_front_cover(path, _baseline_jpeg()) is True

    assert tags.read_tag(path, "genre") == "Probe Genre"
    assert tags.read_tag(path, "artist") == "Probe Artist"


def test_a_tempo_frame_another_tool_wrote_is_left_exactly_alone(tmp_path):
    # This module must never touch a tempo value, and that includes never
    # DELETING one. The frame is planted here with mutagen directly, because
    # nothing in the package can write one.
    from mutagen.id3 import ID3, TBPM

    path = synth_container(tmp_path, ".mp3")
    planted = ID3()
    planted.add(TBPM(encoding=3, text=["124"]))
    planted.save(path)

    assert write_front_cover(path, _baseline_jpeg()) is True

    assert [str(t) for t in ID3(path).getall("TBPM")[0].text] == ["124"]


# ═══════════════════════════════════════════════════════════════════════════
# What the writer refuses
# ═══════════════════════════════════════════════════════════════════════════


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_an_unreadable_image_fails_and_leaves_the_file_untouched(tmp_path, suffix):
    path = synth_container(tmp_path, suffix)
    before = _digest(path)

    with pytest.raises(ArtError, match="could not be decoded"):
        write_front_cover(path, b"\xff\xd8 not really a jpeg")

    assert _digest(path) == before


def test_a_progressive_jpeg_is_refused_and_the_file_untouched(tmp_path):
    path = synth_container(tmp_path, ".flac")
    before = _digest(path)

    with pytest.raises(ArtError, match="progressive"):
        write_front_cover(path, _progressive_jpeg())

    assert _digest(path) == before


def test_a_png_is_refused_and_the_file_untouched(tmp_path):
    path = synth_container(tmp_path, ".mp3")
    before = _digest(path)

    with pytest.raises(ArtError, match="not JPEG"):
        write_front_cover(path, _encode(_gradient(64, 64), "PNG"))

    assert _digest(path) == before


@pytest.mark.parametrize("mode", ["L", "CMYK"])
def test_a_jpeg_that_is_not_rgb_is_refused_and_the_file_untouched(tmp_path, mode):
    path = synth_container(tmp_path, ".aiff")
    before = _digest(path)
    jpeg = _encode(_gradient(64, 64).convert(mode), "JPEG", progressive=False)
    with Image.open(io.BytesIO(jpeg)) as check:
        assert check.mode == mode and check.format == "JPEG"

    with pytest.raises(ArtError, match="only RGB"):
        write_front_cover(path, jpeg)

    assert _digest(path) == before


def test_a_picture_over_the_cap_is_refused_and_the_file_untouched(tmp_path):
    path = synth_container(tmp_path, ".wav")
    before = _digest(path)
    jpeg = _baseline_jpeg()

    with pytest.raises(ArtError, match="over the"):
        write_front_cover(path, jpeg, max_bytes=len(jpeg) - 1)

    assert _digest(path) == before
    # The cap is inclusive, the same way the encoder's is.
    assert write_front_cover(path, jpeg, max_bytes=len(jpeg)) is True


def test_the_writer_default_cap_is_the_encoder_default_cap(tmp_path):
    path = synth_container(tmp_path, ".flac")
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
    # An unknown container with a bad image must say the container, since that
    # is the refusal no better image would ever clear.
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


# ═══════════════════════════════════════════════════════════════════════════
# The reader
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_a_file_with_no_art_reads_as_an_empty_list(tmp_path, suffix):
    assert read_pictures(synth_container(tmp_path, suffix)) == []


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_a_written_cover_reads_back_with_its_measurements(tmp_path, suffix):
    path = synth_container(tmp_path, suffix)
    jpeg = _baseline_jpeg(320, 240)
    assert write_front_cover(path, jpeg) is True

    (picture,) = read_pictures(path)

    assert picture.data == jpeg
    assert picture.mime == "image/jpeg"
    assert (picture.width, picture.height, picture.depth) == (320, 240, 24)
    assert picture.decoded is True
    assert picture.progressive is False
    assert picture.format == "JPEG"


def test_a_png_mislabelled_as_jpeg_reads_with_both_facts(tmp_path):
    # What the container claims and what the bytes are, side by side, so a
    # repair pass cannot read a claimed mime as a measured format.
    from mutagen.id3 import APIC, ID3

    path = synth_container(tmp_path, ".mp3")
    planted = ID3()
    png = _encode(_gradient(64, 64), "PNG")
    planted.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="", data=png))
    planted.save(path)

    (picture,) = read_pictures(path)

    assert picture.mime == "image/jpeg"
    assert picture.format == "PNG"


def test_each_listed_mode_reads_with_its_own_depth(tmp_path):
    from mutagen.id3 import APIC, ID3

    path = synth_container(tmp_path, ".mp3")
    planted = ID3()
    one_bit = _encode(Image.new("1", (32, 32), 1), "PNG")
    wide = _encode(Image.new("I;16", (32, 32), 1000), "PNG")
    planted.add(APIC(encoding=3, mime="image/png", type=3, desc="a", data=one_bit))
    planted.add(APIC(encoding=3, mime="image/png", type=4, desc="b", data=wide))
    planted.save(path)

    depths = {p.data: p.depth for p in read_pictures(path)}

    assert depths[one_bit] == 1
    assert depths[wide] == 16


def test_a_mode_with_no_known_depth_reads_as_zero_not_as_a_guess(tmp_path, monkeypatch):
    # Pillow can add a mode this table has never heard of. Stand in for that day
    # by taking a real mode OUT of the table, then read a picture in it.
    from mutagen.id3 import APIC, ID3

    path = synth_container(tmp_path, ".mp3")
    planted = ID3()
    one_bit = _encode(Image.new("1", (32, 32), 1), "PNG")
    planted.add(APIC(encoding=3, mime="image/png", type=3, desc="", data=one_bit))
    planted.save(path)
    monkeypatch.delitem(art._DEPTH_BY_MODE, "1")

    (picture,) = read_pictures(path)

    assert picture.decoded is True
    assert picture.depth == 0


def test_a_zeroed_flac_block_reads_as_zeroes_not_as_the_decoded_size(tmp_path):
    # The vendored downloader's defect, reproduced with mutagen: a block that
    # sets a mime type and never sets a dimension. The reader must report what
    # the BLOCK says, because that is what a player is told.
    from mutagen.flac import FLAC, Picture

    path = synth_container(tmp_path, ".flac")
    handle = FLAC(path)
    block = Picture()
    block.type = 3
    block.mime = "image/jpeg"
    block.data = _baseline_jpeg(320, 320)
    handle.add_picture(block)
    handle.save()

    (picture,) = read_pictures(path)

    assert (picture.width, picture.height, picture.depth) == (0, 0, 0)
    assert picture.decoded is True


def test_a_progressive_picture_another_tool_embedded_is_flagged(tmp_path):
    from mutagen.id3 import APIC, ID3

    path = synth_container(tmp_path, ".mp3")
    planted = ID3()
    planted.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="", data=_progressive_jpeg()))
    planted.save(path)

    (picture,) = read_pictures(path)

    assert picture.progressive is True
    assert picture.decoded is True


def test_an_undecodable_embedded_picture_says_so(tmp_path):
    from mutagen.id3 import APIC, ID3

    path = synth_container(tmp_path, ".mp3")
    planted = ID3()
    planted.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="", data=b"garbage"))
    planted.save(path)

    (picture,) = read_pictures(path)

    assert picture.decoded is False
    assert picture.format is None
    assert (picture.width, picture.height, picture.depth) == (0, 0, 0)
    assert picture.data == b"garbage"


def test_a_truncated_picture_does_not_read_as_decoded(tmp_path):
    # It opens cleanly and only fails on a full decode, which is why the reader
    # pays for one: a player shows this as blank too.
    from mutagen.id3 import APIC, ID3

    path = synth_container(tmp_path, ".mp3")
    planted = ID3()
    whole = _baseline_jpeg(320, 320)
    cut = whole[: len(whole) // 2]
    with Image.open(io.BytesIO(cut)) as opens:
        assert opens.size == (320, 320)
    planted.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="", data=cut))
    planted.save(path)

    (picture,) = read_pictures(path)

    assert picture.decoded is False


def test_an_mp4_png_cover_reads_with_its_own_mime(tmp_path):
    from mutagen.mp4 import MP4, MP4Cover

    path = synth_container(tmp_path, ".m4a")
    handle = MP4(path)
    handle.tags["covr"] = [MP4Cover(_encode(_gradient(64, 48), "PNG"), MP4Cover.FORMAT_PNG)]
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
    # A verdict on a file is not a verdict on an image, so a sweep catching one
    # must not catch the other.
    assert not issubclass(UnreadableFile, ArtError)
