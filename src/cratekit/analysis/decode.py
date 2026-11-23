"""The one decoder the analysis reads audio through (U263).

librosa 1.0 reads through libsndfile alone, which cannot open an M4A, AAC or
ALAC, so those decode through ffmpeg. THE ORDER IS THE GUARANTEE THAT NOTHING
ANALYSED TODAY CHANGES:

1. ``librosa.load`` reads first, at the file's own rate and channels, then the
   two calls it makes after its read, the mix (one add since U264,
   :func:`mono`) and ``resample`` with ``soxr_hq``: the same bits as before.
2. Only when that raises AND libsndfile cannot open the file is it handed to
   ffmpeg, so a damaged file in a readable format is still undecodable.
3. ffmpeg decodes the first audio stream to 32 bit float into a pipe, and the
   samples take the same mix and resampler.
4. No ffmpeg raises :class:`DecoderMissing`, reported as ``skipped-no-decoder``
   and ``vocal-no-decoder``: the missing decoder is the fault, not the file.

ffmpeg rather than a bound on librosa: the downloader needs it already. An
older librosa still decodes an M4A through its own fallback (U263's record).

Layer: modules. librosa, soundfile and numpy are imported inside the
functions, so a slim install can still import the package.
"""

from __future__ import annotations

import struct
import subprocess
from pathlib import Path
from typing import Any

from cratekit.core import binaries

#: The binary a file libsndfile cannot open is decoded through.
DECODER = "ffmpeg"

#: How long one decode may take. A two hour set decodes in seconds; a decoder
#: still running after this is stuck, and its file is undecodable.
DECODE_TIMEOUT_SECONDS = 600

#: The decoders ffmpeg's MP4 reader gives a cover image; a complaint from one
#: says nothing about the audio (U263).
_COVER_DECODERS = ("mjpeg", "png", "bmp")

#: The two format tags a 32 bit float WAV header carries: plain IEEE float,
#: and the extensible form ffmpeg writes for more than two channels, whose sub
#: format begins with the same tag.
_WAVE_FORMAT_IEEE_FLOAT = 3
_WAVE_FORMAT_EXTENSIBLE = 0xFFFE


class DecoderMissing(RuntimeError):
    """The file needs ffmpeg to decode and ffmpeg is not found."""


class DecodeFailed(RuntimeError):
    """ffmpeg ran and could not decode the file."""


def load(
    path: Any,
    rate: int,
    *,
    offset: float = 0.0,
    duration: float | None = None,
) -> tuple[Any, int]:
    """The mono samples of ``path`` at ``rate``, and the rate, as ``librosa.load``.

    ``offset`` and ``duration`` are passed to librosa only when given. Raises
    when nothing can decode the file; :class:`DecoderMissing` when the one
    decoder that could is absent.
    """
    import librosa

    window: dict[str, float] = {}
    if offset:
        window["offset"] = offset
    if duration is not None:
        window["duration"] = duration
    try:
        # The read ``librosa.load(sr=rate, mono=True)`` makes, then its two
        # next calls, all inside the ``try`` so a refusal is handled where it was.
        native, native_rate = librosa.load(str(path), sr=None, mono=False, **window)
        return _mono_at(librosa, native, native_rate, rate), rate
    except Exception:
        if libsndfile_opens(path):
            raise
    native, native_rate = _ffmpeg_samples(path)
    native = _window(native, native_rate, offset=offset, duration=duration)
    return _mono_at(librosa, native, native_rate, rate), rate


def _mono_at(librosa: Any, native: Any, native_rate: int, rate: int) -> Any:
    """``native`` mixed to one channel and resampled to ``rate``, as
    ``librosa.load`` does after its read."""
    return librosa.resample(mono(native), orig_sr=native_rate, target_sr=rate, res_type="soxr_hq")


#: THE librosa RELEASES WHOSE ``to_mono`` WAS MEASURED (U264), each with its
#: rule for a zero: True where the mean is added into zeros after (1.0), so a
#: mean that rounds to minus zero is plus zero. Any other release mixes
#: through its own ``to_mono``: it can lose the speed, never change a sample.
_MEASURED_MIX: dict[str, bool] = {
    "0.10.2": False,
    "0.10.2.post1": False,
    "0.11.0": False,
    "1.0.0": True,
}


def mono(samples: Any) -> Any:
    """``samples`` mixed to one channel, bit for bit as ``librosa.to_mono``.

    Two float32 channels on a measured release take one add, a tenth of
    ``to_mono``'s mean over a transposed view, after librosa's own
    ``valid_audio``. The same bits: a sum of two and a halving round once
    either way, a float32 overflow is an infinity in both, and a zero's sign
    is :data:`_MEASURED_MIX`'s. Anything else is ``to_mono``'s.
    """
    import librosa

    zero_after = _measured_zero_rule(librosa.__version__)
    if zero_after is None or not _two_float32_channels(samples):
        return librosa.to_mono(samples)
    librosa.util.valid_audio(samples)
    return _mean_of_two(samples, zero_after=zero_after)


def _measured_zero_rule(version: str) -> bool | None:
    """The zero rule of a measured release, or None for one not measured."""
    return _MEASURED_MIX.get(version)


def _two_float32_channels(samples: Any) -> bool:
    import numpy as np

    return (
        isinstance(samples, np.ndarray)
        and samples.ndim == 2
        and samples.shape[0] == 2
        and samples.dtype == np.float32
    )


def _mean_of_two(stereo: Any, *, zero_after: bool) -> Any:
    """The half sum of two channels first, a fresh float32 array, with a release's zero rule."""
    import numpy as np

    out = np.add(stereo[0], stereo[1])
    # numpy's reduction starts from plus zero: minus zero plus minus zero is
    # minus zero here and plus zero in the mean, and no other sum changes.
    out += out.dtype.type(0)
    out /= out.dtype.type(2)
    if zero_after:
        # librosa 1.0 adds the mean into zeros: a half sum that rounds to
        # minus zero, minus the smallest subnormal and zero, is plus zero.
        out += out.dtype.type(0)
    return out


def duration(path: Any) -> float:
    """The length of ``path`` in seconds, as ``librosa.get_duration`` reads it, in :func:`load`'s order."""
    import librosa

    try:
        return float(librosa.get_duration(path=str(path)))
    except Exception:
        if libsndfile_opens(path):
            raise
    native, native_rate = _ffmpeg_samples(path)
    return native.shape[-1] / float(native_rate)


def libsndfile_opens(path: Any) -> bool:
    """Whether libsndfile reads the header of ``path``: if not, ffmpeg decodes it."""
    import soundfile

    try:
        soundfile.info(str(path))
    except Exception:
        return False
    return True


def _window(native: Any, native_rate: int, *, offset: float, duration: float | None) -> Any:
    """The frames a soundfile read with this offset and duration returns, cut as librosa cuts."""
    start = int(offset * native_rate) if offset > 0 else 0
    if duration is None:
        return native[..., start:]
    return native[..., start : start + int(duration * native_rate)]


def _ffmpeg_samples(path: Any) -> tuple[Any, int]:
    """The first audio stream of ``path`` as float32, channels first, and its rate.

    A WAV on a pipe, nothing on disk. Any error ffmpeg reports about the audio
    fails the decode, so a damaged file never yields the part before the
    damage. A file cut exactly on a packet boundary decodes short (U263).
    """
    import numpy as np

    binary = binaries.find(DECODER)
    if binary is None:
        raise DecoderMissing(
            f"{Path(str(path)).name} needs {DECODER} to decode, and {DECODER} was not found"
        )
    command = [
        binary,
        "-nostdin",
        "-hide_banner",
        "-v", "error",
        "-xerror",
        "-i", f"file:{path}",
        "-map", "0:a:0",
        "-map_metadata", "-1",
        "-fflags", "+bitexact",
        "-flags:a", "+bitexact",
        "-c:a", "pcm_f32le",
        "-f", "wav",
        "-",
    ]
    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            timeout=DECODE_TIMEOUT_SECONDS,
            env=binaries.subprocess_env(),
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise DecodeFailed(f"{DECODER} did not finish decoding: {exc}") from exc
    # ANY ERROR ABOUT THE AUDIO IS A FAILED DECODE, whatever the exit code:
    # ``-xerror`` can exit 0 with half a track on the pipe (U263 review). A
    # cover image it cannot read leaves the audio whole.
    said = _audio_faults(proc.stderr.decode("utf-8", "replace"))
    if proc.returncode != 0 or said:
        raise DecodeFailed(f"{DECODER} could not decode the file: {said[-400:]}")
    channels, native_rate, data = _parse_float_wav(proc.stdout)
    frames = np.frombuffer(data, dtype="<f4", count=len(data) // 4)
    if frames.size == 0:
        raise DecodeFailed(f"{DECODER} decoded no samples")
    # (frames, channels) to channels first, librosa's layout, and a mono file
    # to one dimension, as a soundfile read with always_2d off returns it.
    native = frames.reshape(-1, channels).T
    if channels == 1:
        native = native[0]
    return native.astype(np.float32, copy=False), native_rate


def _audio_faults(stderr: str) -> str:
    """What ffmpeg said, less the ``[name @ 0x...]`` lines its cover image decoders said."""
    kept = [
        line
        for line in stderr.strip().splitlines()
        if line.strip() and not line.startswith(tuple(f"[{name} @ " for name in _COVER_DECODERS))
    ]
    return "\n".join(kept)


def _parse_float_wav(blob: bytes) -> tuple[int, int, memoryview]:
    """The channels, rate and sample bytes of a 32 bit float WAV in ``blob``.

    A pipe's data chunk carries a placeholder size, so the data runs to the
    end of the blob, cut to whole frames.
    """
    if len(blob) < 12 or blob[:4] != b"RIFF" or blob[8:12] != b"WAVE":
        raise DecodeFailed(f"{DECODER} wrote no WAV header")
    position = 12
    channels = native_rate = bits = fmt_tag = None
    while position + 8 <= len(blob):
        chunk_id = blob[position : position + 4]
        (size,) = struct.unpack("<I", blob[position + 4 : position + 8])
        body = position + 8
        if chunk_id == b"fmt ":
            fmt_tag, channels, native_rate = struct.unpack("<HHI", blob[body : body + 8])
            (bits,) = struct.unpack("<H", blob[body + 14 : body + 16])
            if fmt_tag == _WAVE_FORMAT_EXTENSIBLE:
                (fmt_tag,) = struct.unpack("<H", blob[body + 24 : body + 26])
        elif chunk_id == b"data":
            if fmt_tag != _WAVE_FORMAT_IEEE_FLOAT or bits != 32 or not channels or not native_rate:
                raise DecodeFailed(
                    f"{DECODER} wrote a WAV that is not 32 bit float "
                    f"(format {fmt_tag}, {bits} bits, {channels} channels)"
                )
            available = len(blob) - body
            whole = available - available % (4 * channels)
            # A view, not a copy: the samples are the bulk of the blob.
            return channels, native_rate, memoryview(blob)[body : body + whole]
        position = body + size + (size & 1)
    raise DecodeFailed(f"{DECODER} wrote a WAV with no data")
