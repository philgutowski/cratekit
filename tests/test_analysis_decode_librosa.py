"""U263: the librosa half of the one decoder, an M4A analysed on librosa 1.0.

The head of an AAC and an ALAC M4A, the refusals, and the proof, by
``array_equal``, that every format libsndfile reads decodes exactly as
``librosa.load`` decodes it, which is the card's merge bar: nothing analysed
today changes. Skipped where the analysis extra is absent, as the other
analysis suites are. The ffmpeg half is ``tests/test_analysis_decode.py``.

Every file is generated here; no library is read.
"""

from __future__ import annotations

import pytest

from cratekit.analysis import decode, detect, energy, vocal
from cratekit.core import binaries
from tests._containers import NATIVE_RATE, encode_m4a, ffmpeg, write_wav

np = pytest.importorskip("numpy")
librosa = pytest.importorskip("librosa")
soundfile = pytest.importorskip("soundfile")
pytest.importorskip("scipy")


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
    source = write_wav(root / "track.wav", _in_key(0, 30.0))
    made = {"wav": source}
    for name, codec in (("flac", "flac"), ("aiff", "pcm_s16be"), ("mp3", "libmp3lame")):
        out = root / f"track.{name}"
        ffmpeg("-i", str(source), "-c:a", codec, str(out))
        made[name] = out
    made["aac"] = encode_m4a(root, source, "aac")
    made["alac"] = encode_m4a(root, source, "alac")
    return made


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


def test_an_alac_m4a_measures_exactly_what_its_wav_measures(keyed):
    """Lossless in, so the samples, and so every number, are the WAV's."""
    for rate in (detect.MEASURE_RATE, vocal.MODEL_SAMPLE_RATE):
        from_m4a, got = decode.load(keyed["alac"], rate)
        from_wav, _ = librosa.load(str(keyed["wav"]), sr=rate, mono=True)
        assert got == rate
        assert np.array_equal(from_m4a, from_wav)
    assert detect.analyse_file(keyed["alac"]) == {
        **detect.analyse_file(keyed["wav"]),
        "path": keyed["alac"],
    }


@pytest.mark.parametrize("name", ["wav", "flac", "aiff", "mp3"])
@pytest.mark.parametrize("rate", [detect.MEASURE_RATE, vocal.MODEL_SAMPLE_RATE])
def test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load(keyed, name, rate, monkeypatch):
    """The card's merge bar: nothing changes for a format that decodes today.

    Bit for bit against the call each site made before this unit, and ffmpeg
    is never started for such a file.
    """
    expected, expected_rate = librosa.load(str(keyed[name]), sr=rate, mono=True)
    monkeypatch.setattr(decode, "_ffmpeg_samples", _never)
    samples, got_rate = decode.load(keyed[name], rate)
    assert got_rate == expected_rate
    assert samples.dtype == expected.dtype
    assert np.array_equal(samples, expected)


@pytest.mark.parametrize("name", ["wav", "flac", "aiff", "mp3"])
def test_the_energy_segment_and_duration_are_librosas_for_those_formats(keyed, name, monkeypatch):
    monkeypatch.setattr(decode, "_ffmpeg_samples", _never)
    assert decode.duration(keyed[name]) == float(librosa.get_duration(path=str(keyed[name])))
    expected, _ = librosa.load(
        str(keyed[name]), sr=energy.MEASURE_RATE, mono=True, offset=7.3, duration=11.1
    )
    samples, _ = decode.load(keyed[name], energy.MEASURE_RATE, offset=7.3, duration=11.1)
    assert np.array_equal(samples, expected)


def test_the_energy_segment_of_an_alac_m4a_is_its_wavs(keyed):
    """The offset and duration are cut in native frames as the soundfile read cuts them."""
    assert decode.duration(keyed["alac"]) == float(librosa.get_duration(path=str(keyed["wav"])))
    expected, _ = librosa.load(
        str(keyed["wav"]), sr=energy.MEASURE_RATE, mono=True, offset=7.3, duration=11.1
    )
    samples, _ = decode.load(keyed["alac"], energy.MEASURE_RATE, offset=7.3, duration=11.1)
    assert np.array_equal(samples, expected)
    assert energy.features_from_path(keyed["alac"]) == energy.features_from_path(keyed["wav"])


def test_an_offset_and_a_duration_between_frames_cut_as_libsndfile_cuts(keyed):
    """Seconds that land between two native frames, past the half, so
    ``int`` and ``round`` disagree: the cut is libsndfile's ``int``."""
    offset = 7.3 + 0.6 / NATIVE_RATE
    duration = 11.1 + 0.7 / NATIVE_RATE
    assert round(offset * NATIVE_RATE) != int(offset * NATIVE_RATE)
    assert round(duration * NATIVE_RATE) != int(duration * NATIVE_RATE)
    expected, _ = librosa.load(
        str(keyed["wav"]), sr=energy.MEASURE_RATE, mono=True, offset=offset, duration=duration
    )
    samples, _ = decode.load(keyed["alac"], energy.MEASURE_RATE, offset=offset, duration=duration)
    assert np.array_equal(samples, expected)


def test_the_energy_measure_takes_the_centre_of_an_m4a(keyed, monkeypatch, no_fallback):
    """The segment is centred on the length ``decode.duration`` reads, which
    for an M4A on librosa 1.0 only the ffmpeg decode can give. Shortened so
    the 30 second fixture is longer than it."""
    monkeypatch.setattr(energy, "SEGMENT_SECONDS", 10.0)
    # The middle ten seconds of the thirty, read and measured without the
    # code under test choosing where they are.
    middle, rate = librosa.load(
        str(keyed["wav"]), sr=energy.MEASURE_RATE, mono=True, offset=10.0, duration=10.0
    )
    centred = energy.features_from_samples(middle, int(rate))
    assert centred is not None
    assert energy.features_from_path(keyed["alac"]) == centred


def test_a_file_libsndfile_opens_and_cannot_read_is_never_handed_to_ffmpeg(keyed, monkeypatch):
    """A damaged FLAC is still the caller's undecodable, as it was."""
    def refuses(*_a, **_k):
        raise RuntimeError("a read that failed part way")

    monkeypatch.setattr(librosa, "load", refuses)
    monkeypatch.setattr(decode, "_ffmpeg_samples", _never)
    with pytest.raises(RuntimeError, match="part way"):
        decode.load(keyed["flac"], detect.MEASURE_RATE)


def test_an_m4a_an_older_librosa_reads_itself_is_left_to_it(keyed, monkeypatch):
    """An older librosa decodes an M4A through its own fallback, and whatever
    it returns is what the analysis measures, so no result on such a copy
    moves. Simulated here by a load that succeeds."""
    own = np.zeros(1000, dtype=np.float32)
    monkeypatch.setattr(librosa, "load", lambda *_a, **_k: (own, 22050))
    monkeypatch.setattr(decode, "_ffmpeg_samples", _never)
    samples, rate = decode.load(keyed["aac"], 22050)
    assert samples is own and rate == 22050


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
    shipped = librosa.load

    def load(path, *args, **kwargs):
        if not decode.libsndfile_opens(path):
            raise RuntimeError("libsndfile cannot open this file, and there is no fallback")
        return shipped(path, *args, **kwargs)

    monkeypatch.setattr(librosa, "load", load)


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


def test_the_vocal_pass_decodes_an_m4a_at_the_models_rate(keyed):
    samples = vocal.decode(keyed["alac"])
    assert samples is not None and samples.dtype == np.float32
    expected, _ = librosa.load(str(keyed["wav"]), sr=vocal.MODEL_SAMPLE_RATE, mono=True)
    assert np.array_equal(samples, expected)


def _never(*_a, **_k):
    raise AssertionError("ffmpeg was asked to decode a file libsndfile reads")
