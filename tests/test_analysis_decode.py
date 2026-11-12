"""U263: an M4A is analysed on a current librosa, and nothing else decodes differently.

librosa 1.0 reads through libsndfile alone, which cannot open an M4A, so
every M4A came back ``skipped-undecodable``. ``analysis/decode.py`` hands a
file to ffmpeg only when librosa raised on it AND libsndfile cannot open it.

Two halves. The first needs numpy and ffmpeg and nothing of the extra, so it
runs on every machine the suite runs on: the WAV ffmpeg writes to its pipe is
read right, the samples of a lossless M4A are the PCM it was made from, a
damaged one fails, and nothing is written to disk. The second needs librosa,
and is skipped where the extra is absent as the other analysis suites are:
the head of an AAC and an ALAC M4A, the refusals, and the proof, by
``array_equal``, that every format libsndfile reads decodes exactly as
``librosa.load`` decodes it.

Every file is generated here; no library is read.
"""

from __future__ import annotations

import importlib.util
import os
import struct
import subprocess
import wave
from pathlib import Path

import pytest

from cratekit.analysis import decode, detect, energy, vocal, vocals
from cratekit.core import binaries
from tests._containers import require_ffmpeg

np = pytest.importorskip("numpy")

NATIVE_RATE = 44100


def _ffmpeg(*arguments: str) -> None:
    binary = require_ffmpeg()
    proc = subprocess.run(
        [binary, "-nostdin", "-hide_banner", "-v", "error", "-y", *arguments],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr[-400:]


def _pcm16(seconds: float, *, channels: int = 2, seed: int = 0) -> np.ndarray:
    """Frames by channels of 16 bit PCM: a tone per channel, noise and a clipped run."""
    rng = np.random.default_rng(seed)
    frames = int(seconds * NATIVE_RATE)
    t = np.arange(frames) / NATIVE_RATE
    out = np.empty((frames, channels), dtype=np.int16)
    for channel in range(channels):
        tone = 0.4 * np.sin(2 * np.pi * (220.0 * (channel + 1)) * t)
        tone += 0.05 * rng.standard_normal(frames)
        tone[frames // 3 : frames // 3 + 500] = 1.5  # clipped
        tone[frames // 2 : frames // 2 + 4000] = 0.0  # silence
        out[:, channel] = np.clip(np.round(tone * 32767), -32768, 32767).astype(np.int16)
    return out


def _write_wav(path: Path, pcm: np.ndarray) -> Path:
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(pcm.shape[1])
        handle.setsampwidth(2)
        handle.setframerate(NATIVE_RATE)
        handle.writeframes(pcm.astype("<i2").tobytes())
    return path


def _m4a(tmp_path: Path, source: Path, codec: str, name: str | None = None) -> Path:
    out = tmp_path / (name or f"{codec}.m4a")
    extra = ["-b:a", "192k"] if codec == "aac" else []
    _ffmpeg("-i", str(source), "-c:a", codec, *extra, str(out))
    return out


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
    pcm = _pcm16(1.37, channels=channels, seed=channels)
    alac = _m4a(tmp_path, _write_wav(tmp_path / "source.wav", pcm), "alac")
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
    pcm = _pcm16(0.5)
    _m4a(tmp_path, _write_wav(tmp_path / "source.wav", pcm), "alac", name="Artist: Title.m4a")
    monkeypatch.chdir(tmp_path)
    native, _rate = decode._ffmpeg_samples(Path("Artist: Title.m4a"))
    assert native.shape == (2, pcm.shape[0])


def test_a_truncated_m4a_fails_rather_than_yielding_the_part_before_the_damage(tmp_path):
    whole = _m4a(tmp_path, _write_wav(tmp_path / "source.wav", _pcm16(3.0)), "aac")
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
    source = _write_wav(tmp_path / "source.wav", _pcm16(12.0))
    whole = tmp_path / f"whole-{codec}.m4a"
    extra = ["-b:a", "192k"] if codec == "aac" else []
    _ffmpeg("-i", str(source), "-c:a", codec, *extra, "-movflags", "+faststart", str(whole))
    data = bytearray(whole.read_bytes())
    middle = len(data) // 2
    data[middle : middle + 2000] = bytes(2000)
    damaged = tmp_path / f"damaged-{codec}.m4a"
    damaged.write_bytes(bytes(data))
    with pytest.raises(decode.DecodeFailed):
        decode._ffmpeg_samples(damaged)


def test_an_m4a_with_its_index_first_cut_short_fails(tmp_path):
    """The other truncation: the index is whole and promises audio the file
    no longer holds, so ffmpeg has decoded most of it before it fails."""
    source = _write_wav(tmp_path / "source.wav", _pcm16(12.0))
    whole = tmp_path / "whole.m4a"
    _ffmpeg("-i", str(source), "-c:a", "aac", "-movflags", "+faststart", str(whole))
    cut = tmp_path / "cut.m4a"
    cut.write_bytes(whole.read_bytes()[: int(whole.stat().st_size * 0.95)])
    with pytest.raises(decode.DecodeFailed):
        decode._ffmpeg_samples(cut)


def test_the_first_audio_stream_is_the_one_decoded(tmp_path):
    first = _pcm16(1.0, seed=1)
    second = _pcm16(1.0, seed=2)
    a = _write_wav(tmp_path / "a.wav", first)
    b = _write_wav(tmp_path / "b.wav", second)
    both = tmp_path / "both.m4a"
    _ffmpeg("-i", str(a), "-i", str(b), "-map", "0:a", "-map", "1:a", "-c:a", "alac", str(both))
    native, _rate = decode._ffmpeg_samples(both)
    assert np.array_equal(native, (first.astype(np.float32) / np.float32(32768)).T)


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
    alac = _m4a(source, _write_wav(source / "source.wav", _pcm16(1.0)), "alac")
    scratch = tmp_path / "tmp"
    scratch.mkdir()
    monkeypatch.setenv("TMPDIR", str(scratch))
    before = sorted(os.listdir(source))
    decode._ffmpeg_samples(alac)
    assert sorted(os.listdir(source)) == before
    assert os.listdir(scratch) == []


# ---------------------------------------------------------------------------
# The librosa half
# ---------------------------------------------------------------------------

librosa_needed = pytest.mark.skipif(
    any(importlib.util.find_spec(name) is None for name in ("librosa", "soundfile", "scipy")),
    reason="the analysis extra is absent",
)


def _in_key(tonic: int, seconds: float) -> np.ndarray:
    """A major key's I, IV, V, I in triads with a bass and a kick, stereo, at 44.1k."""
    rate = NATIVE_RATE
    scale = [0, 2, 4, 5, 7, 9, 11]
    out = np.zeros(int(seconds * rate), dtype=np.float64)
    chord = int(2.0 * rate)
    t = np.arange(chord) / rate
    fade = np.minimum(1.0, np.minimum(t, t[::-1]) / 0.05)
    for index, start in enumerate(range(0, out.size, chord)):
        degree = (0, 3, 4, 0)[index % 4]
        notes = [tonic + scale[(degree + s) % 7] + (12 if degree + s >= 7 else 0) for s in (0, 2, 4)]
        tone = sum(np.sin(2 * np.pi * 261.63 * 2 ** (n / 12.0) * t) for n in notes)
        tone = tone + 1.5 * np.sin(2 * np.pi * 65.41 * 2 ** (notes[0] / 12.0) * t)
        piece = 0.06 * tone * fade
        stop = min(out.size, start + chord)
        out[start:stop] += piece[: stop - start]
    # A kick on every beat at 124, with a sharp attack, so the tempo survives
    # a lossy encode and the head is compared on its key and its tempo.
    beat = 60.0 / 124.0
    length = int(0.12 * rate)
    k = np.arange(length) / rate
    kick = 0.8 * np.sin(2 * np.pi * (50 + 120 * np.exp(-k * 40)) * k) * np.exp(-k * 25)
    hit = 0
    while int(round(hit * beat * rate)) + length <= out.size:
        start = int(round(hit * beat * rate))
        out[start : start + length] += kick
        hit += 1
    stereo = np.stack([out, out * 0.9], axis=1)
    return np.clip(np.round(stereo * 32767), -32768, 32767).astype(np.int16)


@pytest.fixture(scope="module")
def keyed(tmp_path_factory):
    """One C major track as WAV, FLAC, AIFF, MP3, AAC M4A and ALAC M4A."""
    root = tmp_path_factory.mktemp("keyed")
    source = _write_wav(root / "track.wav", _in_key(0, 30.0))
    made = {"wav": source}
    for name, codec in (("flac", "flac"), ("aiff", "pcm_s16be"), ("mp3", "libmp3lame")):
        out = root / f"track.{name}"
        _ffmpeg("-i", str(source), "-c:a", codec, str(out))
        made[name] = out
    made["aac"] = _m4a(root, source, "aac")
    made["alac"] = _m4a(root, source, "alac")
    return made


@librosa_needed
@pytest.mark.parametrize("fallback", ["installed", "none"])
@pytest.mark.parametrize("codec", ["aac", "alac"])
def test_an_m4a_gets_a_head_and_the_key_the_flac_gets(keyed, codec, fallback, request):
    """The card's defect, red on librosa 1.0 before this unit: the M4A was
    ``skipped-undecodable`` while the same audio as FLAC was analysed.

    Once with the installed librosa as it is, and once with its fallback taken
    away, so the decode through ffmpeg is driven whichever release is here."""
    if fallback == "none":
        request.getfixturevalue("no_fallback")
    flac = detect.analyse_file(keyed["flac"])
    m4a = detect.analyse_file(keyed[codec])
    assert flac is not None and flac.get("terminal") is None, flac
    assert m4a is not None and m4a.get("terminal") is None, m4a
    assert (flac["camelot"], flac["rate"]) == ("8B", 124)
    assert (m4a["camelot"], m4a["rate"]) == ("8B", 124)


@librosa_needed
def test_an_alac_m4a_measures_exactly_what_its_wav_measures(keyed):
    """Lossless in, so the samples, and so every number, are the WAV's."""
    import librosa

    for rate in (detect.MEASURE_RATE, vocal.MODEL_SAMPLE_RATE):
        from_m4a, got = decode.load(keyed["alac"], rate)
        from_wav, _ = librosa.load(str(keyed["wav"]), sr=rate, mono=True)
        assert got == rate
        assert np.array_equal(from_m4a, from_wav)
    assert detect.analyse_file(keyed["alac"]) == {
        **detect.analyse_file(keyed["wav"]),
        "path": keyed["alac"],
    }


@librosa_needed
@pytest.mark.parametrize("name", ["wav", "flac", "aiff", "mp3"])
@pytest.mark.parametrize("rate", [detect.MEASURE_RATE, vocal.MODEL_SAMPLE_RATE])
def test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load(keyed, name, rate, monkeypatch):
    """The card's merge bar: nothing changes for a format that decodes today.

    Bit for bit against the call each site made before this unit, and ffmpeg
    is never started for such a file.
    """
    import librosa

    expected, expected_rate = librosa.load(str(keyed[name]), sr=rate, mono=True)
    monkeypatch.setattr(decode, "_ffmpeg_samples", _never)
    samples, got_rate = decode.load(keyed[name], rate)
    assert got_rate == expected_rate
    assert samples.dtype == expected.dtype
    assert np.array_equal(samples, expected)


@librosa_needed
@pytest.mark.parametrize("name", ["wav", "flac", "aiff", "mp3"])
def test_the_energy_segment_and_duration_are_librosas_for_those_formats(keyed, name, monkeypatch):
    import librosa

    monkeypatch.setattr(decode, "_ffmpeg_samples", _never)
    assert decode.duration(keyed[name]) == float(librosa.get_duration(path=str(keyed[name])))
    expected, _ = librosa.load(
        str(keyed[name]), sr=energy.MEASURE_RATE, mono=True, offset=7.3, duration=11.1
    )
    samples, _ = decode.load(keyed[name], energy.MEASURE_RATE, offset=7.3, duration=11.1)
    assert np.array_equal(samples, expected)


@librosa_needed
def test_the_energy_segment_of_an_alac_m4a_is_its_wavs(keyed):
    """The offset and duration are cut in native frames as the soundfile read cuts them."""
    import librosa

    assert decode.duration(keyed["alac"]) == float(librosa.get_duration(path=str(keyed["wav"])))
    expected, _ = librosa.load(
        str(keyed["wav"]), sr=energy.MEASURE_RATE, mono=True, offset=7.3, duration=11.1
    )
    samples, _ = decode.load(keyed["alac"], energy.MEASURE_RATE, offset=7.3, duration=11.1)
    assert np.array_equal(samples, expected)
    assert energy.features_from_path(keyed["alac"]) == energy.features_from_path(keyed["wav"])


@librosa_needed
def test_an_offset_and_a_duration_between_frames_cut_as_libsndfile_cuts(keyed):
    """Seconds that land between two native frames, past the half, so
    ``int`` and ``round`` disagree: the cut is libsndfile's ``int``."""
    import librosa

    offset = 7.3 + 0.6 / NATIVE_RATE
    duration = 11.1 + 0.7 / NATIVE_RATE
    assert round(offset * NATIVE_RATE) != int(offset * NATIVE_RATE)
    assert round(duration * NATIVE_RATE) != int(duration * NATIVE_RATE)
    expected, _ = librosa.load(
        str(keyed["wav"]), sr=energy.MEASURE_RATE, mono=True, offset=offset, duration=duration
    )
    samples, _ = decode.load(keyed["alac"], energy.MEASURE_RATE, offset=offset, duration=duration)
    assert np.array_equal(samples, expected)


@librosa_needed
def test_the_energy_measure_takes_the_centre_of_an_m4a(keyed, monkeypatch, no_fallback):
    """The segment is centred on the length ``decode.duration`` reads, which
    for an M4A on librosa 1.0 only the ffmpeg decode can give. Shortened so
    the 30 second fixture is longer than it."""
    monkeypatch.setattr(energy, "SEGMENT_SECONDS", 10.0)
    centred = energy.features_from_path(keyed["wav"])
    assert centred is not None
    assert energy.features_from_path(keyed["alac"]) == centred


@librosa_needed
def test_a_file_libsndfile_opens_and_cannot_read_is_never_handed_to_ffmpeg(keyed, monkeypatch):
    """A damaged FLAC is still the caller's undecodable, as it was."""
    import librosa

    def refuses(*_a, **_k):
        raise RuntimeError("a read that failed part way")

    monkeypatch.setattr(librosa, "load", refuses)
    monkeypatch.setattr(decode, "_ffmpeg_samples", _never)
    with pytest.raises(RuntimeError, match="part way"):
        decode.load(keyed["flac"], detect.MEASURE_RATE)


@librosa_needed
def test_an_m4a_an_older_librosa_reads_itself_is_left_to_it(keyed, monkeypatch):
    """An older librosa decodes an M4A through its own fallback, and whatever
    it returns is what the analysis measures, so no result on such a copy
    moves. Simulated here by a load that succeeds."""
    import librosa

    own = np.zeros(1000, dtype=np.float32)
    monkeypatch.setattr(librosa, "load", lambda *_a, **_k: (own, 22050))
    monkeypatch.setattr(decode, "_ffmpeg_samples", _never)
    samples, rate = decode.load(keyed["aac"], 22050)
    assert samples is own and rate == 22050


@librosa_needed
def test_a_truncated_m4a_is_still_undecodable(keyed, tmp_path, no_fallback):
    cut = tmp_path / "cut.m4a"
    whole = keyed["aac"].read_bytes()
    cut.write_bytes(whole[: len(whole) // 2])
    assert detect.analyse_file(cut) == {"path": cut, "terminal": detect.TERMINAL_UNDECODABLE}
    assert vocal.decode(cut) is None


@pytest.fixture
def no_fallback(monkeypatch):
    """librosa as 1.0 ships it, whichever release is installed.

    An older librosa reads an M4A through its own fallback, which finds
    ffmpeg by itself, so a test of what this package does when librosa
    cannot read a file has to take that fallback away. Its own read of a file
    libsndfile opens is left as it is.
    """
    import librosa

    shipped = librosa.load

    def load(path, *args, **kwargs):
        if not decode.libsndfile_opens(path):
            raise RuntimeError("libsndfile cannot open this file, and there is no fallback")
        return shipped(path, *args, **kwargs)

    monkeypatch.setattr(librosa, "load", load)


@librosa_needed
def test_no_ffmpeg_names_the_decoder_for_an_m4a_and_spares_a_flac(keyed, monkeypatch, no_fallback):
    monkeypatch.setattr(binaries, "find", lambda name: None)
    assert detect.analyse_file(keyed["aac"]) == {
        "path": keyed["aac"],
        "terminal": detect.TERMINAL_NO_DECODER,
    }
    flac = detect.analyse_file(keyed["flac"])
    assert flac is not None and flac["camelot"] == "8B"
    with pytest.raises(decode.DecoderMissing):
        vocal.decode(keyed["aac"])


@librosa_needed
def test_the_vocal_pass_decodes_an_m4a_at_the_models_rate(keyed):
    samples = vocal.decode(keyed["alac"])
    assert samples is not None and samples.dtype == np.float32
    import librosa

    expected, _ = librosa.load(str(keyed["wav"]), sr=vocal.MODEL_SAMPLE_RATE, mono=True)
    assert np.array_equal(samples, expected)


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


def _never(*_a, **_k):
    raise AssertionError("ffmpeg was asked to decode a file libsndfile reads")
