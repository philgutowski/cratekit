"""One synthesizer for a real audio container, shared by every suite that needs one.

A second synthesizer would be a second opinion about what a valid file is, and
the tag suite's opinion is the one the tag reader is proven against. So there is
one, and it lives here rather than inside a test module.

WHY NOT ``from tests.test_tags import _synth``. That binding reached across test
modules for a private name, which is a coupling nothing declares, and importing a
test module runs its top-level code as a side effect of an unrelated suite. The
tag suite's top level builds a container table and a field table; none of that is
wrong, and none of it is any business of the match suite. A helper module has no
top level worth running and no tests to collect.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


def require_ffmpeg() -> str:
    binary = shutil.which("ffmpeg")
    if binary is None:
        pytest.fail(
            "ffmpeg is required to prove that a tag write leaves audio bytes "
            "unchanged. Install it (the CI workflow does this in a dedicated "
            "step). This fails rather than skips because a skipped audio-safety "
            "proof is indistinguishable from a passing one in every summary "
            "anybody reads."
        )
    return binary


def synth_container(tmp_path: Path, suffix: str) -> Path:
    """One second of silence in the given container."""
    require_ffmpeg()
    out = tmp_path / f"probe{suffix}"
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-t", "1", str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0 and out.exists(), (
        f"ffmpeg could not encode {suffix}, so this container's audio-safety "
        f"proof cannot run: {proc.stderr[-400:]}"
    )
    return out


def tagged_container(tmp_path: Path, target: Path, **fields: str) -> Path:
    """A real container at ``target`` carrying ``fields`` as its tags.

    One synthesizer, one tag writer, one copy. Three tests had written this
    sequence by hand with three signatures, and the point of this module is that
    there is one opinion about what a valid file is.
    """
    from cratekit.core import tags

    probe = synth_container(tmp_path, target.suffix)
    assert tags.write_tags(probe, dict(fields))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(probe, target)
    return target


#: The rate the decode suites write their sources at (U263).
NATIVE_RATE = 44100


def ffmpeg(*arguments: str) -> None:
    """Run ffmpeg quietly over ``arguments`` and fail with what it said."""
    binary = require_ffmpeg()
    proc = subprocess.run(
        [binary, "-nostdin", "-hide_banner", "-v", "error", "-y", *arguments],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr[-400:]


def pcm16(seconds: float, *, channels: int = 2, seed: int = 0):
    """Frames by channels of 16 bit PCM: a tone per channel, noise, a clipped run and silence."""
    import numpy as np

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


def write_wav(path: Path, pcm) -> Path:
    """``pcm``, frames by channels of 16 bit samples, as a WAV at :data:`NATIVE_RATE`."""
    import wave

    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(pcm.shape[1])
        handle.setsampwidth(2)
        handle.setframerate(NATIVE_RATE)
        handle.writeframes(pcm.astype("<i2").tobytes())
    return path


def encode_m4a(directory: Path, source: Path, codec: str, name: str | None = None) -> Path:
    """``source`` encoded as an M4A of ``codec``, ``aac`` or ``alac``, in ``directory``."""
    out = directory / (name or f"{codec}.m4a")
    extra = ["-b:a", "192k"] if codec == "aac" else []
    ffmpeg("-i", str(source), "-c:a", codec, *extra, str(out))
    return out


__all__ = [
    "NATIVE_RATE",
    "encode_m4a",
    "ffmpeg",
    "pcm16",
    "require_ffmpeg",
    "synth_container",
    "tagged_container",
    "write_wav",
]
