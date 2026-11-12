"""U263: the ffmpeg half of the one decoder, which needs no librosa.

librosa 1.0 reads through libsndfile alone, which cannot open an M4A, so
every M4A came back ``skipped-undecodable``. ``analysis/decode.py`` hands a
file to ffmpeg only when librosa raised on it AND libsndfile cannot open it.

This half needs numpy and ffmpeg and nothing of the extra, so it runs on
every machine the suite runs on: the WAV ffmpeg writes to its pipe is read
right, the samples of a lossless M4A are the PCM it was made from, a damaged
one fails, a cover it cannot read does not, and nothing is written to disk.
The librosa half is ``tests/test_analysis_decode_librosa.py``, skipped where
the extra is absent as the other analysis suites are.

Every file is generated here; no library is read.
"""

from __future__ import annotations

import os
import struct
from pathlib import Path

import pytest

from cratekit.analysis import decode, vocals
from cratekit.core import binaries
from tests._containers import NATIVE_RATE, encode_m4a, ffmpeg, pcm16, write_wav

np = pytest.importorskip("numpy")


# ---------------------------------------------------------------------------
# The ffmpeg half, which needs no librosa
# ---------------------------------------------------------------------------


def _wav_header(fmt: bytes, data: bytes, *, between: bytes = b"") -> bytes:
    body = b"WAVE" + b"fmt " + struct.pack("<I", len(fmt)) + fmt + between
    body += b"data" + struct.pack("<I", 0xFFFFFFFF) + data
    return b"RIFF" + struct.pack("<I", 0xFFFFFFFF) + body


def _fmt(tag: int, channels: int, rate: int, bits: int, *, sub: int | None = None) -> bytes:
    block = channels * bits // 8
    plain = struct.pack("<HHIIHH", tag, channels, rate, rate * block, block, bits)
    if sub is None:
        return plain
    return plain + struct.pack("<HHI", 22, bits, 0) + struct.pack("<H", sub) + bytes(14)


def test_a_float_wav_on_a_pipe_is_read_to_its_end_in_whole_frames():
    samples = np.arange(7, dtype="<f4")  # three stereo frames and a stray sample
    blob = _wav_header(_fmt(3, 2, 48000, 32), samples.tobytes())
    channels, rate, data = decode._parse_float_wav(blob)
    assert (channels, rate) == (2, 48000)
    assert np.array_equal(np.frombuffer(data, dtype="<f4"), samples[:6])


def test_the_extensible_header_and_a_chunk_before_the_data_are_read():
    samples = np.linspace(-1, 1, 12, dtype="<f4")
    listing = b"LIST" + struct.pack("<I", 5) + b"INFOx" + b"\x00"  # odd size, padded
    blob = _wav_header(_fmt(0xFFFE, 6, 44100, 32, sub=3), samples.tobytes(), between=listing)
    channels, rate, data = decode._parse_float_wav(blob)
    assert (channels, rate) == (6, 44100)
    assert np.array_equal(np.frombuffer(data, dtype="<f4"), samples)


@pytest.mark.parametrize(
    "blob",
    [
        b"",
        b"RIFX" + bytes(8),
        _wav_header(_fmt(1, 2, 44100, 16), bytes(8)),  # integer PCM, not float
        _wav_header(_fmt(0xFFFE, 2, 44100, 32, sub=1), bytes(8)),
        b"RIFF" + struct.pack("<I", 4) + b"WAVE",  # no data chunk
    ],
    ids=["empty", "not-riff", "pcm", "extensible-pcm", "no-data"],
)
def test_a_header_that_is_not_32_bit_float_is_refused(blob):
    with pytest.raises(decode.DecodeFailed):
        decode._parse_float_wav(blob)


@pytest.mark.parametrize("channels", [1, 2, 6])
def test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from(tmp_path, channels):
    """The scaling, the channel order and the length, bit for bit.

    ALAC is lossless, so the samples ffmpeg hands back must be the 16 bit PCM
    divided by 32768, which is how libsndfile reads the same PCM as float.
    """
    pcm = pcm16(1.37, channels=channels, seed=channels)
    alac = encode_m4a(tmp_path, write_wav(tmp_path / "source.wav", pcm), "alac")
    native, rate = decode._ffmpeg_samples(alac)
    expected = pcm.astype(np.float32) / np.float32(32768)
    assert rate == NATIVE_RATE
    assert native.dtype == np.float32
    if channels == 1:
        assert native.shape == (pcm.shape[0],)
        assert np.array_equal(native, expected[:, 0])
    else:
        assert native.shape == (channels, pcm.shape[0])
        assert np.array_equal(native, expected.T)


def test_a_path_with_a_colon_is_read_as_a_file(tmp_path, monkeypatch):
    """ffmpeg reads ``name:rest`` as a protocol, so a relative name like this
    one would be refused as an unknown protocol without the ``file:`` prefix."""
    pcm = pcm16(0.5)
    encode_m4a(tmp_path, write_wav(tmp_path / "source.wav", pcm), "alac", name="Artist: Title.m4a")
    monkeypatch.chdir(tmp_path)
    native, _rate = decode._ffmpeg_samples(Path("Artist: Title.m4a"))
    assert native.shape == (2, pcm.shape[0])


def test_a_truncated_m4a_fails_rather_than_yielding_the_part_before_the_damage(tmp_path):
    whole = encode_m4a(tmp_path, write_wav(tmp_path / "source.wav", pcm16(3.0)), "aac")
    cut = tmp_path / "cut.m4a"
    cut.write_bytes(whole.read_bytes()[: whole.stat().st_size // 2])
    with pytest.raises(decode.DecodeFailed):
        decode._ffmpeg_samples(cut)


@pytest.mark.parametrize("codec", ["aac", "alac"])
def test_an_m4a_damaged_in_the_middle_fails_rather_than_yielding_its_first_half(
    tmp_path, codec
):
    """Driven by the review of U263: with the index first and the damage in
    the middle of the audio, ffmpeg 6.1 under ``-xerror`` stops at the error
    and exits 0 with the part before it on the pipe. The error it reports is
    what fails the decode."""
    source = write_wav(tmp_path / "source.wav", pcm16(12.0))
    whole = tmp_path / f"whole-{codec}.m4a"
    extra = ["-b:a", "192k"] if codec == "aac" else []
    ffmpeg("-i", str(source), "-c:a", codec, *extra, "-movflags", "+faststart", str(whole))
    data = bytearray(whole.read_bytes())
    middle = len(data) // 2
    data[middle : middle + 2000] = bytes(2000)
    damaged = tmp_path / f"damaged-{codec}.m4a"
    damaged.write_bytes(bytes(data))
    with pytest.raises(decode.DecodeFailed):
        decode._ffmpeg_samples(damaged)


def test_an_m4a_with_its_index_first_cut_inside_a_packet_fails(tmp_path):
    """The other truncation: the index is whole and promises audio the file
    no longer holds, so ffmpeg has decoded most of it before it fails. A cut
    at 95 percent lands inside a packet; one exactly on a packet boundary
    decodes short with nothing said, which is a residual of U263."""
    source = write_wav(tmp_path / "source.wav", pcm16(12.0))
    whole = tmp_path / "whole.m4a"
    ffmpeg("-i", str(source), "-c:a", "aac", "-movflags", "+faststart", str(whole))
    cut = tmp_path / "cut.m4a"
    cut.write_bytes(whole.read_bytes()[: int(whole.stat().st_size * 0.95)])
    with pytest.raises(decode.DecodeFailed):
        decode._ffmpeg_samples(cut)


def test_the_first_audio_stream_is_the_one_decoded(tmp_path):
    first = pcm16(1.0, seed=1)
    second = pcm16(1.0, seed=2)
    a = write_wav(tmp_path / "a.wav", first)
    b = write_wav(tmp_path / "b.wav", second)
    both = tmp_path / "both.m4a"
    ffmpeg("-i", str(a), "-i", str(b), "-map", "0:a", "-map", "1:a", "-c:a", "alac", str(both))
    native, _rate = decode._ffmpeg_samples(both)
    assert np.array_equal(native, (first.astype(np.float32) / np.float32(32768)).T)


@pytest.mark.parametrize(
    "cover, kind",
    [
        (b"RIFF\x00\x00\x00\x00WEBPVP8 " + bytes(64), "jpeg"),  # WebP labelled JPEG
        (b"GIF89a" + bytes(64), "jpeg"),
        (b"\x89PNG\r\n\x1a\n" + b"\xff" * 64, "png"),  # a PNG cut short
    ],
    ids=["webp-as-jpeg", "gif-as-jpeg", "broken-png"],
)
def test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable(tmp_path, cover, kind):
    """Driven by round two of the review: ffmpeg probes the cover before it
    decodes the audio, and logs a cover it cannot read as an error while the
    audio comes out whole. The vendored downloader embeds whatever bytes a
    cover URL returned, so such a cover is a tag, not damage."""
    from mutagen import mp4

    pcm = pcm16(1.0)
    alac = encode_m4a(tmp_path, write_wav(tmp_path / "source.wav", pcm), "alac")
    tagged = mp4.MP4(str(alac))
    form = mp4.MP4Cover.FORMAT_JPEG if kind == "jpeg" else mp4.MP4Cover.FORMAT_PNG
    tagged["covr"] = [mp4.MP4Cover(cover, imageformat=form)]
    tagged.save()
    native, _rate = decode._ffmpeg_samples(alac)
    assert np.array_equal(native, (pcm.astype(np.float32) / np.float32(32768)).T)


def test_a_cover_complaint_is_dropped_and_an_audio_complaint_is_kept():
    said = (
        "[mjpeg @ 0x55] bits 255 is invalid\n"
        "[png @ 0x56] chunk too big\n"
        "[aac @ 0x57] channel element 0.0 is not allocated\n"
    )
    assert decode._audio_faults(said) == "[aac @ 0x57] channel element 0.0 is not allocated"
    assert decode._audio_faults("[mjpeg @ 0x55] No JPEG data found in image\n") == ""


def test_the_first_audio_stream_is_taken_even_when_another_is_the_default(tmp_path):
    """Without the map ffmpeg picks the default stream, here the second."""
    first = pcm16(1.0, channels=1, seed=3)
    second = pcm16(1.0, channels=2, seed=4)
    a = write_wav(tmp_path / "a.wav", first)
    b = write_wav(tmp_path / "b.wav", second)
    both = tmp_path / "both.m4a"
    ffmpeg(
        "-i", str(a), "-i", str(b), "-map", "0:a", "-map", "1:a", "-c:a", "alac",
        "-disposition:a:0", "0", "-disposition:a:1", "default", str(both),
    )
    native, _rate = decode._ffmpeg_samples(both)
    assert native.shape == (first.shape[0],)
    assert np.array_equal(native, first[:, 0].astype(np.float32) / np.float32(32768))


def test_an_ffmpeg_that_exits_non_zero_saying_nothing_fails(tmp_path, monkeypatch):
    """The exit code is half the rule on its own: an ffmpeg that wrote a
    whole, valid stream and then failed in silence is not trusted. Bound
    through the override variable every binary obeys."""
    samples = np.linspace(-0.5, 0.5, 64, dtype="<f4")
    stream = tmp_path / "stream.wav"
    stream.write_bytes(_wav_header(_fmt(3, 2, 44100, 32), samples.tobytes()))
    fake = tmp_path / "ffmpeg"
    fake.write_text(f"#!/bin/sh\ncat '{stream}'\nexit 1\n")
    fake.chmod(0o755)
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(fake))
    with pytest.raises(decode.DecodeFailed):
        decode._ffmpeg_samples(tmp_path / "track.m4a")
    fake.write_text(f"#!/bin/sh\ncat '{stream}'\nexit 0\n")
    native, rate = decode._ffmpeg_samples(tmp_path / "track.m4a")
    assert rate == 44100 and np.array_equal(native, samples.reshape(-1, 2).T)


def test_a_file_that_is_not_audio_fails(tmp_path):
    junk = tmp_path / "junk.m4a"
    junk.write_bytes(b"not an audio file at all" * 40)
    with pytest.raises(decode.DecodeFailed):
        decode._ffmpeg_samples(junk)


def test_no_ffmpeg_raises_the_missing_decoder_and_runs_nothing(tmp_path, monkeypatch):
    ran: list[object] = []
    monkeypatch.setattr(binaries, "find", lambda name: None)
    monkeypatch.setattr(decode.subprocess, "run", lambda *a, **k: ran.append(a))
    with pytest.raises(decode.DecoderMissing) as caught:
        decode._ffmpeg_samples(tmp_path / "track.m4a")
    assert "ffmpeg" in str(caught.value)
    assert ran == []


def test_the_decoder_is_found_where_every_other_binary_is(tmp_path, monkeypatch):
    """The override variable a person sets for ffmpeg is the one this decode
    obeys, so doctor's ``binary.ffmpeg`` row and the decode agree."""
    asked: list[str] = []
    monkeypatch.setattr(binaries, "find", lambda name: asked.append(name))
    with pytest.raises(decode.DecoderMissing):
        decode._ffmpeg_samples(tmp_path / "track.m4a")
    assert asked == ["ffmpeg"]


def test_the_decode_writes_no_file(tmp_path, monkeypatch):
    """The card's rule: nothing is written by the decode, beside the track or
    in a temporary directory. The temporary directory ffmpeg would reach for
    is pointed at an empty one and read after."""
    source = tmp_path / "in"
    source.mkdir()
    alac = encode_m4a(source, write_wav(source / "source.wav", pcm16(1.0)), "alac")
    scratch = tmp_path / "tmp"
    scratch.mkdir()
    monkeypatch.setenv("TMPDIR", str(scratch))
    before = sorted(os.listdir(source))
    decode._ffmpeg_samples(alac)
    assert sorted(os.listdir(source)) == before
    assert os.listdir(scratch) == []



def test_the_vocal_pass_names_the_missing_decoder(monkeypatch):
    def missing(path):
        raise decode.DecoderMissing("track.m4a needs ffmpeg to decode")

    monkeypatch.setattr(vocals, "_VOCAL_MODEL", object())
    monkeypatch.setattr(vocals, "_VOCAL_COLUMNS", (0, 1, 2))
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_DECODER", missing)
    scored = vocals.analyse({"path": "track.m4a", "terminal": None})
    assert scored["vocal_active"] is False
    assert scored["vocal_reason"] == vocals.REASON_NO_DECODER == "vocal-no-decoder"
    assert scored["voxlevel"] is None


# ---------------------------------------------------------------------------
# U264: the mono mix, one add, which needs no librosa for its arithmetic
# ---------------------------------------------------------------------------

#: The smallest float32 subnormal, whose half is a tie that rounds to zero.
_TINY = np.float32(1.401298464324817e-45)


def _bits(values) -> list[str]:
    return [f"{int(v):08x}" for v in np.asarray(values, dtype=np.float32).view(np.uint32)]


@pytest.mark.parametrize("zero_after", [False, True], ids=["0.10-0.11", "1.0"])
def test_the_half_sum_of_two_channels_rounds_once_like_float64(zero_after):
    """Every value that is not a zero is the correctly rounded half sum.

    The expectation is taken in float64, where a sum of two float32 values
    and its halving are exact, and rounded to float32 once: a value the code
    under test does not compute. Random bit patterns reach subnormals and
    every exponent. A sum past float32's largest value is the one place
    float64 differs, and librosa's float32 reduction overflows there as the
    one add does; the table below pins it.
    """
    rng = np.random.default_rng(264)
    frames = 200_003  # odd, so no length is a power of two
    raw = np.frombuffer(rng.integers(0, 2**32, 2 * frames, dtype=np.uint32).tobytes(), "<f4")
    raw = raw.reshape(frames, 2)
    raw = raw[np.isfinite(raw).all(axis=1)]
    uniform = rng.uniform(-1, 1, (frames, 2)).astype(np.float32)
    stereo = np.concatenate([raw, uniform]).T  # channels first, a transposed view
    exact = stereo[0].astype(np.float64) + stereo[1]
    with np.errstate(over="ignore"):
        expected = (exact / 2).astype(np.float32)
        overflows = ~np.isfinite(exact.astype(np.float32))
    kept = stereo.copy()
    got = decode._mean_of_two(stereo, zero_after=zero_after)
    assert got.dtype == np.float32 and got.shape == (stereo.shape[1],)
    compared = (expected != 0) & ~overflows
    assert compared.sum() > 390_000
    assert np.array_equal(got[compared].view(np.uint32), expected[compared].view(np.uint32))
    assert np.array_equal(kept.view(np.uint32), stereo.view(np.uint32))  # the buffer is untouched


@pytest.mark.parametrize(
    ("left", "right", "before_1_0", "on_1_0"),
    [
        # numpy's add reduction starts from plus zero, so both minus zero is plus.
        (-0.0, -0.0, "00000000", "00000000"),
        (0.0, -0.0, "00000000", "00000000"),
        (-0.0, 0.0, "00000000", "00000000"),
        (0.5, -0.5, "00000000", "00000000"),
        # A half sum of minus the smallest subnormal rounds to minus zero, which
        # librosa 1.0's buffer of zeros turns to plus zero.
        (-_TINY, 0.0, "80000000", "00000000"),
        (-0.0, -_TINY, "80000000", "00000000"),
        (_TINY, -0.0, "00000000", "00000000"),
        # Three halves of the smallest subnormal is a tie, to the even two.
        (3 * _TINY, 0.0, "00000002", "00000002"),
        (-3 * _TINY, -0.0, "80000002", "80000002"),
        # A sum past float32's largest value overflows in librosa's float32
        # reduction as in the one add, and the resampler then refuses it.
        (3e38, 3e38, "7f800000", "7f800000"),
        (-3e38, -3e38, "ff800000", "ff800000"),
    ],
)
def test_a_zero_takes_the_sign_each_measured_release_gives_it(left, right, before_1_0, on_1_0):
    """The sign of a zero is the one place the ways of mixing differ, and an
    overflow the one place float64 would.

    The expected bits were read from ``librosa.to_mono`` on 0.10.2,
    0.10.2.post1 and 0.11.0 (``before_1_0``) and on 1.0.0 (``on_1_0``), on
    numpy 2.5 and 1.26; the librosa half of this file checks the installed
    release against its own ``to_mono``.
    """
    stereo = np.array([[left], [right]], dtype=np.float32)
    assert _bits(decode._mean_of_two(stereo, zero_after=False)) == [before_1_0]
    assert _bits(decode._mean_of_two(stereo, zero_after=True)) == [on_1_0]


@pytest.mark.parametrize(
    ("version", "rule"),
    [
        ("0.10.2", False),
        ("0.10.2.post1", False),
        ("0.11.0", False),
        ("1.0.0", True),
        ("1.0.1", None),
        ("1.0.0rc0", None),
        ("0.11.0rc1", None),
        ("1.1.0", None),
        ("2.0.0", None),
        ("0.12.0.dev0", None),
        ("0.9.2", None),
        ("", None),
    ],
)
def test_only_a_measured_release_takes_the_one_add(version, rule):
    """A release not measured, a patch or a pre release, is mixed by its own ``to_mono``."""
    assert decode._measured_zero_rule(version) is rule
