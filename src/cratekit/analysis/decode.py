"""The one decoder the analysis reads audio through (U263).

WHAT WAS WRONG. Every site that turned a file into samples called
``librosa.load`` and nothing else. librosa 1.0, the release a fresh install
of the analysis extra resolves, reads through libsndfile alone and dropped the
fallback decoder its older releases carried, and libsndfile cannot open an
M4A, AAC or ALAC. So every M4A in a landing came back ``skipped-undecodable``
from the head and vocal inactive from the vocal pass, a reason that reads like
a damaged file, while the same audio as FLAC or MP3 was analysed.

THE ORDER IS THE GUARANTEE THAT NOTHING ANALYSED TODAY CHANGES.

1. ``librosa.load`` reads the file first, at its own rate and channels,
   and its samples take the two calls ``librosa.load`` makes after its read,
   the mix to mono and ``resample`` with ``soxr_hq``, so the result is the
   bits the call each site made before this module returns (U264 made the
   mix one add, :func:`mono`). On librosa 1.0 that is every file libsndfile
   reads; on an older release it is those and the files its own fallback
   reads, an M4A among them. So no file the installed librosa decodes is
   decoded any other way.
2. Only when that raises AND libsndfile itself cannot open the file is the
   file handed to ffmpeg. A failure on a file libsndfile does open, a FLAC
   truncated mid frame, is raised as before, so a damaged file in a format
   that decodes today is still the caller's undecodable.
3. ffmpeg decodes the first audio stream to 32 bit float at the file's own
   rate and channels, into a pipe; nothing is written to disk. The samples
   then take the same mix and resampler as in 1, so the arithmetic after the
   decode is the same on every path.
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

THE MONO MIX IS ONE ADD (U264). Every path mixes through :func:`mono`,
which gives the bits ``librosa.to_mono`` gives in a tenth of its time, for two
channels on a librosa release it was measured on, and is ``to_mono`` itself
for anything else.

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
        # ``librosa.load`` at the file's own rate and channels is the read
        # ``librosa.load(sr=rate, mono=True)`` makes, fallback and all; the
        # mix and the resampler after it are the two calls it makes next,
        # with the mix one add (U264). All three stay inside the ``try``, so
        # a refusal is handled where it was.
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
#: rule for a zero, as a release names itself in ``librosa.__version__``.
#: Every release adds the two channels through numpy's add reduction, which
#: starts from its identity, plus zero, so a frame whose two channels are both
#: minus zero mixes to plus zero; 1.0 then adds the mean into a buffer of
#: zeros, so a mean that rounds to minus zero is plus zero as well (True
#: here). Every other value is the correctly rounded half sum on every
#: release. Any other release, a patch or a pre release included, mixes
#: through its own ``to_mono``: it can lose the speed, never change a sample.
#: Measuring a new release and naming it here is what gives it the speed.
_MEASURED_MIX: dict[str, bool] = {
    "0.10.2": False,
    "0.10.2.post1": False,
    "0.11.0": False,
    "1.0.0": True,
}


def mono(samples: Any) -> Any:
    """``samples`` mixed to one channel, bit for bit as ``librosa.to_mono``.

    WHAT IS FASTER. ``to_mono`` takes ``np.mean`` over a transposed view of
    the stereo buffer, the slowest way to add two float arrays: 271 ms of a
    345 second track's decode, measured on the speed survey of 2026-11-12,
    paid once at each rate. Two channels of float32 on a measured release are
    added with one add instead, in a tenth of the time, after librosa's own
    ``valid_audio``, so audio that is not finite is refused with the same
    error, where it was.

    WHY IT IS THE SAME BITS. A sum of two and a halving round once whichever
    way they are done, so the half sum is the one value of its frame, in
    float32 or through float64, on numpy 1 and 2. What the ways differ in is
    a zero's sign, which :data:`_MEASURED_MIX` holds per release, measured on
    0.10.2, 0.10.2.post1, 0.11.0 and 1.0.0. Anything else, mono, three or more
    channels, another dtype, a release not measured, is ``to_mono``'s.
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
    """The half sum of two channels, with the zero rule of a measured release.

    ``stereo`` is channels first; a fresh float32 array is returned and the
    buffer is not touched.
    """
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
