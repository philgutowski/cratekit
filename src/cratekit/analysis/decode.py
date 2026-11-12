"""The one decoder the analysis reads audio through (U263).

WHAT WAS WRONG. Every site that turned a file into samples called
``librosa.load`` and nothing else. librosa 1.0, the release a fresh install
of the analysis extra resolves, reads through libsndfile alone and dropped the
fallback decoder its older releases carried, and libsndfile cannot open an
M4A, AAC or ALAC. So every M4A in a landing came back ``skipped-undecodable``
from the head and vocal inactive from the vocal pass, a reason that reads like
a damaged file, while the same audio as FLAC or MP3 was analysed.

THE ORDER IS THE GUARANTEE THAT NOTHING ANALYSED TODAY CHANGES.

1. ``librosa.load`` is called first, exactly as each site called it before
   this module, and whatever it returns is returned untouched. On librosa 1.0
   that is every file libsndfile reads; on an older release it is those and
   the files its own fallback reads, an M4A among them. So no file the
   installed librosa decodes is decoded any other way.
2. Only when that raises AND libsndfile itself cannot open the file is the
   file handed to ffmpeg. A failure on a file libsndfile does open, a FLAC
   truncated mid frame, is raised as before, so a damaged file in a format
   that decodes today is still the caller's undecodable.
3. ffmpeg decodes the first audio stream to 32 bit float at the file's own
   rate and channels, into a pipe; nothing is written to disk. The samples
   then take the two calls ``librosa.load`` makes after its own read,
   ``to_mono`` and ``resample`` with ``soxr_hq``, so the arithmetic after the
   decode is librosa's on every path.
4. No ffmpeg, for a file librosa did not read and libsndfile cannot open,
   raises :class:`DecoderMissing`, which the head reports as
   ``skipped-no-decoder`` and the vocal pass as ``vocal-no-decoder``: the
   decoder that was never tried is named as the fault, not the file. That is
   an M4A, and also any file too damaged for libsndfile to open, which only
   ffmpeg could have judged. The energy measure of restamp and calibrate
   reports it as ``features-unavailable``, as it reports every failure. ``crate doctor`` reports the missing binary on the
   ``binary.ffmpeg`` row, which every analysis verb that decodes declares.

WHY FFMPEG AND NOT A BOUND ON LIBROSA. The downloader already needs the
binary and ``analyze run`` already declared it, so this adds no dependency and
no install step, where a ceiling below 1.0 would hold the analysis on releases
whose fallback, audioread, they themselves mark for removal.

WHAT IS LEFT AS IT WAS. An older librosa still decodes an M4A through its own
fallback, so on such a copy an M4A's samples are audioread's, not ffmpeg's.
That keeps every result on that copy as it is; the record of U263 says so.

THE MONO MIX OF U264 LANDS HERE, so the two cards build one decoder.

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

#: The decoders ffmpeg's MP4 reader gives a cover image, whatever bytes the
#: cover holds: JPEG, PNG and BMP are the three it maps ``covr`` to. ffmpeg
#: probes every stream before it decodes the one mapped, so a cover it cannot
#: read is reported on these and says nothing about the audio (U263).
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

    ``offset`` and ``duration`` are seconds, as ``librosa.load`` takes them,
    and are passed to it only when given, so a call without them is the call
    the sites made before this module. Raises when nothing can decode the
    file; :class:`DecoderMissing` when the one decoder that could is absent.
    """
    import librosa

    window: dict[str, float] = {}
    if offset:
        window["offset"] = offset
    if duration is not None:
        window["duration"] = duration
    try:
        return librosa.load(str(path), sr=rate, mono=True, **window)
    except Exception:
        if libsndfile_opens(path):
            raise
    native, native_rate = _ffmpeg_samples(path)
    native = _window(native, native_rate, offset=offset, duration=duration)
    samples = librosa.to_mono(native)
    samples = librosa.resample(samples, orig_sr=native_rate, target_sr=rate, res_type="soxr_hq")
    return samples, rate


def duration(path: Any) -> float:
    """The length of ``path`` in seconds, as ``librosa.get_duration`` reads it.

    The same order as :func:`load`: librosa's answer first, and ffmpeg's
    decoded length only for a file libsndfile cannot open and librosa did
    not read.
    """
    import librosa

    try:
        return float(librosa.get_duration(path=str(path)))
    except Exception:
        if libsndfile_opens(path):
            raise
    native, native_rate = _ffmpeg_samples(path)
    return native.shape[-1] / float(native_rate)


def libsndfile_opens(path: Any) -> bool:
    """Whether libsndfile reads the header of ``path``.

    The test that sends a file to ffmpeg. A file it opens is libsndfile's, and
    a failure reading it is that file's, reported as it always was.
    """
    import soundfile

    try:
        soundfile.info(str(path))
    except Exception:
        return False
    return True


def _window(native: Any, native_rate: int, *, offset: float, duration: float | None) -> Any:
    """The frames a soundfile read with this offset and duration returns.

    Cut in native frames with ``int(seconds * rate)``, the arithmetic
    librosa's own soundfile read uses for its seek and its frame count.
    """
    start = int(offset * native_rate) if offset > 0 else 0
    if duration is None:
        return native[..., start:]
    return native[..., start : start + int(duration * native_rate)]


def _ffmpeg_samples(path: Any) -> tuple[Any, int]:
    """The first audio stream of ``path`` as float32, channels first, and its rate.

    Nothing touches the disk: ffmpeg writes a WAV to a pipe, and the rate and
    channels come from the header it wrote, which describes the samples it
    emitted. ``-xerror`` stops it at the first decode error, and any error it
    reports about the audio fails the decode, so a file damaged inside its
    audio fails rather than yielding the part before the damage. A file cut
    exactly on a packet boundary, with its index first, gives ffmpeg nothing
    to report and decodes short; the record of U263 files it.
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
    # ANY ERROR ABOUT THE AUDIO IS A FAILED DECODE, whatever the exit code.
    # Measured on ffmpeg 6.1 in the review of U263: ``-xerror`` stops at a
    # decoder error in the middle of an M4A and exits 0 with the part before
    # it on the pipe, so the exit code alone measured the first half of a
    # damaged track and wrote its key. At ``-v error`` a clean decode says
    # nothing, so what it says is a fault, except a complaint about a cover
    # image it cannot read, which round two found on a playable track with a
    # WebP cover and which leaves the audio whole.
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
    """What ffmpeg said, less the lines its cover image decoders said.

    A line ffmpeg logs carries its source as ``[name @ 0x...]``. The lines a
    cover decoder writes are dropped; every other line, the audio decoder's,
    the reader's and ffmpeg's own, is kept as a fault.
    """
    kept = [
        line
        for line in stderr.strip().splitlines()
        if line.strip() and not line.startswith(tuple(f"[{name} @ " for name in _COVER_DECODERS))
    ]
    return "\n".join(kept)


def _parse_float_wav(blob: bytes) -> tuple[int, int, memoryview]:
    """The channels, rate and sample bytes of a 32 bit float WAV in ``blob``.

    Written for the stream ffmpeg writes to a pipe, whose data chunk carries
    a placeholder size because a pipe cannot be seeked back to fill it in: the
    data is read to the end of the blob, cut to whole frames.
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
