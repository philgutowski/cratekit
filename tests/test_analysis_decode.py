"""U263: an M4A is analysed on a current librosa.

librosa 1.0 reads through libsndfile alone, which cannot open an M4A, so
every M4A came back ``skipped-undecodable``. Skipped where the analysis extra
is absent, as the other analysis suites are. Every file is generated here.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from cratekit.analysis import detect
from tests._containers import require_ffmpeg

np = pytest.importorskip("numpy")
librosa = pytest.importorskip("librosa")

RATE = 44100


def _write_wav(path: Path, seconds: float) -> Path:
    import wave

    t = np.arange(int(seconds * RATE)) / RATE
    tone = sum(0.1 * np.sin(2 * np.pi * hz * t) for hz in (261.63, 329.63, 392.0, 65.41))
    pcm = np.round(np.stack([tone, tone], axis=1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(RATE)
        handle.writeframes(pcm.tobytes())
    return path


@pytest.mark.parametrize("codec", ["aac", "alac"])
def test_an_m4a_gets_a_head(tmp_path, codec):
    source = _write_wav(tmp_path / "source.wav", 20.0)
    m4a = tmp_path / f"{codec}.m4a"
    subprocess.run(
        [require_ffmpeg(), "-v", "error", "-y", "-i", str(source), "-c:a", codec, str(m4a)],
        check=True,
    )
    found = detect.analyse_file(m4a)
    assert found is not None and found.get("terminal") is None, found
