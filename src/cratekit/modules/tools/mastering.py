"""Mastering a live set recording, one at a time (Feature Inventory row 30).

It reads a source, writes a new lossless FLAC beside it, and never modifies or
deletes the source (R18): a recording of a performance happened once and is not
recoverable from anywhere.

The run, in order: archive the source and verify the copy by content hash;
correct level drift with a long smoothing window (a short one flattens the music
itself); measure, then normalize with one linear gain offset under a true peak
ceiling (a one pass normalization compresses); encode FLAC at the source's own
bit depth (24 bits on a 16 bit source only makes the file larger than the WAV).

Binaries are resolved rather than assumed on PATH, the loudness report is parsed
as JSON, an existing output or archive entry is never overwritten or trusted by
name, and settings are validated at construction rather than minutes into an
encode. Every subprocess goes through an injected runner, so each decision is
testable without encoding audio.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from enum import StrEnum
from pathlib import Path

from cratekit.core import binaries

#: Containers accepted as a source: what a DJ recorder writes, one continuous
#: audio stream, which the two pass measurement assumes.
SOURCE_SUFFIXES: tuple[str, ...] = (".wav", ".aiff", ".aif", ".flac")

#: Where a verified copy of each source is kept, beside the recording: it is the
#: user's own audio and must survive uninstalling Cratekit.
ARCHIVE_DIRNAME = "_originals"

OUTPUT_SUFFIX = "_mastered.flac"

#: The drift filter's accepted smoothing window, in frames. ffmpeg refuses
#: outside this and refuses an even value.
DRIFT_WINDOW_RANGE = (3, 301)

#: The integrated loudness targets loudnorm accepts, LUFS. ffmpeg refuses
#: outside this only at the first measure pass, naming the filter.
LUFS_RANGE = (-70.0, -5.0)

#: What a joined recording is called, after the first part's stem, so its master
#: never takes the name the first part's own master would have.
JOINED_SUFFIX = "_set"


class Refusal(StrEnum):
    """Why a mastering run will not proceed, as a structured cause (KTD25).

    Each member is a distinct diagnosis; the CLI renders it into a sentence and
    reserves an exit code for it.
    """

    SOURCE_MISSING = "source-missing"
    SOURCE_UNSUPPORTED = "source-unsupported"
    OUTPUT_EXISTS = "output-exists"
    ARCHIVE_HOLDS_A_DIFFERENT_RECORDING = "archive-holds-a-different-recording"
    ARCHIVE_VERIFY_FAILED = "archive-verify-failed"
    ENCODER_MISSING = "encoder-missing"
    ENCODER_FAILED = "encoder-failed"


class MasteringRefused(Exception):
    """A refusal carrying its structured cause and the file it is about."""

    def __init__(self, refusal: Refusal, detail: str, *, path: Path | None = None) -> None:
        super().__init__(detail)
        self.refusal = refusal
        self.detail = detail
        self.path = path


@dataclass(frozen=True, slots=True)
class Settings:
    """Loudness targets and the drift window, validated at construction."""

    #: Integrated loudness target, LUFS.
    target_lufs: float = -14.0
    #: True peak ceiling, dBTP. Below zero because inter-sample peaks in a lossy
    #: transcode of this file can exceed the sample peak.
    true_peak_db: float = -1.0
    #: Loudness range target, LU. Part of what keeps the normalization linear.
    loudness_range: float = 11.0
    #: Drift smoothing window, in frames. Odd, within DRIFT_WINDOW_RANGE.
    drift_window: int = 63
    #: Analysis frame length, milliseconds.
    frame_ms: int = 500

    def __post_init__(self) -> None:
        low, high = DRIFT_WINDOW_RANGE
        if not low <= self.drift_window <= high:
            raise ValueError(
                f"drift_window must be between {low} and {high}, found {self.drift_window}"
            )
        if self.drift_window % 2 == 0:
            raise ValueError(
                f"drift_window must be odd, found {self.drift_window}; the filter "
                f"centres its window on the current frame and has no centre for "
                f"an even one"
            )
        if self.true_peak_db > 0:
            raise ValueError(
                f"true_peak_db is a ceiling below full scale and must not be "
                f"positive, found {self.true_peak_db}"
            )
        low_lufs, high_lufs = LUFS_RANGE
        # A negated range so a NaN fails it: ``x < low or x > high`` admits NaN.
        if not low_lufs <= self.target_lufs <= high_lufs:
            raise ValueError(
                f"target_lufs must be between {low_lufs:g} and {high_lufs:g} "
                f"LUFS, found {self.target_lufs}"
            )


DEFAULT_SETTINGS = Settings()


@dataclass(frozen=True, slots=True)
class Loudness:
    """One measurement of a signal, in the units the report quotes."""

    integrated_lufs: float | None = None
    loudness_range: float | None = None
    true_peak_db: float | None = None
    threshold: float | None = None
    target_offset: float | None = None


@dataclass(frozen=True, slots=True)
class SourceProbe:
    """What ffprobe says about the source, and what the encoder needs from it."""

    sample_rate: int
    sample_fmt: str
    size_bytes: int
    #: Read for the join, a stream copy, which needs every part in one layout.
    channels: int | None = None
    codec: str = ""

    @property
    def is_16_bit(self) -> bool:
        return self.sample_fmt.startswith("s16")


@dataclass(frozen=True, slots=True)
class Report:
    """Before and after, so the result is checkable rather than asserted."""

    source: Path
    output: Path
    archived_to: Path | None
    before: Loudness
    after: Loudness
    source_bytes: int
    output_bytes: int
    bit_depth: str
    #: A joined run's parts in join order and each one's archive copy; both
    #: empty for a single recording.
    parts: tuple[Path, ...] = ()
    archives: tuple[Path, ...] = ()

    @property
    def size_reduction(self) -> float:
        """Fraction of the source's bytes the output saves. Negative means larger."""
        if self.source_bytes <= 0:
            return 0.0
        return 1.0 - (self.output_bytes / self.source_bytes)


@dataclass(frozen=True, slots=True)
class Command:
    """One external invocation, as data, so a plan can be shown before it runs."""

    label: str
    argv: tuple[str, ...]
    #: True when the caller needs stderr, where ffmpeg prints its loudness JSON.
    capture: bool = True


@dataclass(frozen=True, slots=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


Runner = Callable[[Command], CommandResult]


def subprocess_runner(command: Command) -> CommandResult:
    """Run one command with the fallback directories on PATH and credentials stripped."""
    completed = subprocess.run(
        list(command.argv),
        capture_output=True,
        text=True,
        env=binaries.subprocess_env(),
        check=False,
    )
    return CommandResult(
        returncode=completed.returncode,
        stdout=completed.stdout or "",
        stderr=completed.stderr or "",
    )


# Pure decisions


def output_path(source: Path, *, output_dir: Path | None = None) -> Path:
    """Where the mastered file lands: beside the source unless told otherwise."""
    directory = output_dir if output_dir is not None else source.parent
    return directory / f"{source.stem}{OUTPUT_SUFFIX}"


def joined_name(parts: Sequence[Path]) -> str:
    """The joined recording's file name: the first part's stem and container."""
    first = parts[0]
    return f"{first.stem}{JOINED_SUFFIX}{first.suffix}"


def planned_output(parts: Sequence[Path | str], *, output_dir: Path | None = None) -> Path:
    """Where the master of these parts lands. The one name builder for both shapes.

    Several parts are named for the joined recording, beside the first part. The
    shell checks the destination with this, so check and encode cannot disagree.
    """
    paths = [Path(p) for p in parts]
    if len(paths) == 1:
        return output_path(paths[0], output_dir=output_dir)
    return output_path(paths[0].parent / joined_name(paths), output_dir=output_dir)


def drift_filter(settings: Settings) -> str:
    """The level drift correction stage.

    ``p`` and ``m`` bound how far one frame may be pushed; ``s=0.0`` disables a
    second smoothing on top of the window, which would flatten the dynamics.
    """
    return f"dynaudnorm=f={settings.frame_ms}:g={settings.drift_window}:p=0.95:m=10.0:s=0.0"


def measure_filter(settings: Settings) -> str:
    """Pass one: measure only, and print the result as JSON."""
    return (
        f"loudnorm=I={settings.target_lufs}:TP={settings.true_peak_db}"
        f":LRA={settings.loudness_range}:print_format=json"
    )


def apply_filter(settings: Settings, measured: Loudness) -> str:
    """Pass two: apply the measured offset linearly, with the peak ceiling.

    Every measured value is required: omitting one drops loudnorm silently into
    its dynamic mode, which compresses the set instead of moving it.
    """
    named = (
        ("integrated", measured.integrated_lufs), ("true peak", measured.true_peak_db),
        ("loudness range", measured.loudness_range), ("threshold", measured.threshold),
        ("target offset", measured.target_offset),
    )
    missing = [name for name, value in named if value is None]
    if missing:
        raise MasteringRefused(
            Refusal.ENCODER_FAILED,
            f"the measurement pass did not report {', '.join(missing)}, so a "
            f"linear normalization cannot be built; applying without them would "
            f"fall back to dynamic mode and compress the set instead of moving it",
        )
    return (
        f"loudnorm=I={settings.target_lufs}:TP={settings.true_peak_db}"
        f":LRA={settings.loudness_range}"
        f":measured_I={measured.integrated_lufs}"
        f":measured_TP={measured.true_peak_db}"
        f":measured_LRA={measured.loudness_range}"
        f":measured_thresh={measured.threshold}"
        f":offset={measured.target_offset}"
        f":linear=true:print_format=json"
    )


def encoder_args(probe: SourceProbe) -> tuple[tuple[str, ...], str, str]:
    """``(encoder argv fragment, extra filter, human bit depth)`` for the source.

    A 16 bit source is dithered back to 16: the chain runs in floating point, and
    truncating without dither adds audible distortion on quiet passages.
    """
    flac = ("-c:a", "flac", "-compression_level", "8")
    if probe.is_16_bit:
        return flac, "aresample=out_sample_fmt=s16:dither_method=triangular_hp", "16-bit, dithered"
    return (*flac, "-sample_fmt", "s32", "-bits_per_raw_sample", "24"), "", "24-bit"


_JSON_BLOCK = re.compile(r"\{[^{}]*\}")


def _last_report(stderr_text: str, marker: str) -> dict | None:
    """The last JSON object in ffmpeg's stderr carrying ``marker``.

    The last, because ffmpeg prints its block after the encode. Parsed as JSON
    rather than grepped per key, which could pair values from two blocks.
    """
    for raw in reversed(_JSON_BLOCK.findall(stderr_text or "")):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and marker in data:
            return data
    return None


def parse_loudness(stderr_text: str) -> Loudness:
    """Read the INPUT half of ffmpeg's loudnorm report out of stderr."""
    data = _last_report(stderr_text, "input_i")
    if data is None:
        return Loudness()
    return Loudness(
        integrated_lufs=_as_float(data.get("input_i")),
        loudness_range=_as_float(data.get("input_lra")),
        true_peak_db=_as_float(data.get("input_tp")),
        threshold=_as_float(data.get("input_thresh")),
        target_offset=_as_float(data.get("target_offset")),
    )


def parse_output_loudness(stderr_text: str) -> Loudness:
    """The same report read from its OUTPUT half, for the after figures."""
    data = _last_report(stderr_text, "output_i")
    if data is None:
        return Loudness()
    return Loudness(
        integrated_lufs=_as_float(data.get("output_i")),
        loudness_range=_as_float(data.get("output_lra")),
        true_peak_db=_as_float(data.get("output_tp")),
    )


def _as_float(value: object) -> float | None:
    """A finite float, or None. Non-finite is UNKNOWN, not a value.

    loudnorm reports ``-inf`` for silence; None makes the apply stage refuse with
    a sentence naming what is missing instead of passing infinity to ffmpeg.
    """
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if parsed == parsed and abs(parsed) != float("inf") else None


# The archive: copy first, verify, never trust a name


def digest(path: Path, *, chunk: int = 1 << 20) -> str:
    """A content hash, read in chunks so a multi-gigabyte set does not load."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(chunk)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def archive_source(source: Path, archive_dir: Path) -> Path:
    """Copy the source into the archive and prove the copy is identical.

    An entry already there under the same name is verified, not assumed:
    recorders name files by counter, so two sets called ``REC001.WAV`` is normal.
    """
    archive_dir.mkdir(parents=True, exist_ok=True)
    destination = archive_dir / source.name
    source_digest = digest(source)

    if destination.exists():
        if digest(destination) == source_digest:
            return destination
        raise MasteringRefused(
            Refusal.ARCHIVE_HOLDS_A_DIFFERENT_RECORDING,
            f"{destination} already holds a different recording with this name. "
            f"Archiving over it would destroy the earlier one, and skipping the "
            f"copy would leave this recording unarchived while reporting it safe.",
            path=destination,
        )

    shutil.copy2(source, destination)
    if digest(destination) != source_digest:
        # Verified before proceeding: the rest of the run falls back on this copy.
        destination.unlink(missing_ok=True)
        raise MasteringRefused(
            Refusal.ARCHIVE_VERIFY_FAILED,
            f"the archived copy of {source.name} did not match the source, so the "
            f"safety copy this run depends on does not exist",
            path=destination,
        )
    return destination


# The run


def _check_source(path: Path) -> None:
    """Refuse a recording that is not there or is in a container this does not read."""
    if not path.is_file():
        raise MasteringRefused(Refusal.SOURCE_MISSING, f"no such recording: {path}", path=path)
    if path.suffix.lower() not in SOURCE_SUFFIXES:
        raise MasteringRefused(
            Refusal.SOURCE_UNSUPPORTED,
            f"{path.suffix!r} is not a container this reads; supported: "
            f"{', '.join(SOURCE_SUFFIXES)}",
            path=path,
        )


def output_exists_detail(target: Path) -> str:
    """The sentence an ``output-exists`` refusal carries, here and in the shell."""
    return (
        f"{target} already exists. Replacing it silently would discard a "
        f"master that may already have been kept, and the settings that "
        f"produced it are not recorded anywhere."
    )


def _output_exists(target: Path) -> MasteringRefused:
    return MasteringRefused(Refusal.OUTPUT_EXISTS, output_exists_detail(target), path=target)


def _resolve(*names: str, path: Path | None = None) -> list[str]:
    """Each binary's absolute path, in order, or ``encoder-missing``."""
    try:
        return [binaries.resolve(name) for name in names]
    except binaries.BinaryNotFound as exc:
        raise MasteringRefused(Refusal.ENCODER_MISSING, str(exc), path=path) from exc


def probe_source(source: Path, *, runner: Runner, ffprobe: str) -> SourceProbe:
    """Sample rate, sample format, and size. Refuses rather than guessing."""
    command = Command(
        label="probe",
        argv=(
            ffprobe, "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=sample_rate,sample_fmt,channels,codec_name",
            "-of", "default=noprint_wrappers=1:nokey=0", str(source),
        ),
    )
    result = runner(command)
    if result.returncode != 0:
        raise MasteringRefused(
            Refusal.ENCODER_FAILED,
            f"could not read the audio stream of {source.name}: "
            f"{result.stderr.strip()[-400:]}",
            path=source,
        )
    values = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    try:
        rate = int(values["sample_rate"])
    except (KeyError, ValueError) as exc:
        raise MasteringRefused(
            Refusal.ENCODER_FAILED,
            f"{source.name} reported no usable sample rate, so the encode cannot "
            f"preserve it",
            path=source,
        ) from exc
    try:
        channels: int | None = int(values["channels"])
    except (KeyError, ValueError):
        channels = None
    return SourceProbe(
        sample_rate=rate, sample_fmt=values.get("sample_fmt", ""), size_bytes=source.stat().st_size,
        channels=channels, codec=values.get("codec_name", ""),
    )


def master(
    source: Path | str, *, settings: Settings = DEFAULT_SETTINGS, output_dir: Path | None = None,
    archive: bool = True, archive_dir: Path | None = None, overwrite: bool = False,
    runner: Runner = subprocess_runner, workspace: Path | None = None,
) -> Report:
    """Master one recording. The source is opened read-only and never modified.

    The order is load-bearing: refuse, archive, then process, so a crash never
    leaves an intermediate without a verified copy. ``workspace`` holds the drift
    corrected intermediate and defaults to the output directory, since a set is
    gigabytes and a small temp filesystem fails at the end of a long stage.
    """
    source = Path(source)
    _check_source(source)
    target = output_path(source, output_dir=output_dir)
    if target.exists() and not overwrite:
        raise _output_exists(target)
    ffmpeg, ffprobe = _resolve("ffmpeg", "ffprobe", path=source)

    archived_to = None
    if archive:
        archived_to = archive_source(
            source, archive_dir or (source.parent / ARCHIVE_DIRNAME)
        )

    probe = probe_source(source, runner=runner, ffprobe=ffprobe)
    target.parent.mkdir(parents=True, exist_ok=True)
    scratch_dir = workspace or target.parent
    scratch_dir.mkdir(parents=True, exist_ok=True)
    intermediate = scratch_dir / f".{source.stem}.cratekit-drift.wav"

    try:
        before = _measure(source, ffmpeg=ffmpeg, settings=settings, runner=runner)
        _run_or_refuse(
            runner,
            Command(
                label="drift-correction",
                argv=(
                    ffmpeg, "-v", "error", "-y", "-i", str(source),
                    "-af", drift_filter(settings),
                    # RF64 when needed: a 24 bit intermediate of a long set passes
                    # 4 GiB, and a wrapped header truncates the master silently.
                    "-c:a", "pcm_s24le", "-rf64", "auto", str(intermediate),
                ),
            ),
        )
        measured = _measure(intermediate, ffmpeg=ffmpeg, settings=settings, runner=runner)
        encoder, extra_filter, depth = encoder_args(probe)
        chain = apply_filter(settings, measured)
        if extra_filter:
            chain = f"{chain},{extra_filter}"
        applied = _run_or_refuse(
            runner,
            Command(
                label="normalize-and-encode",
                argv=(
                    ffmpeg, "-hide_banner", "-nostats", "-y",
                    "-i", str(intermediate), "-af", chain,
                    *encoder, "-ar", str(probe.sample_rate), str(target),
                ),
            ),
        )
    finally:
        # The intermediate is Cratekit's: left after a failure it fills the volume.
        intermediate.unlink(missing_ok=True)

    _wrote_or_refuse(target, "normalize-and-encode")
    return Report(
        source=source, output=target, archived_to=archived_to, before=before,
        after=parse_output_loudness(applied.stderr), source_bytes=probe.size_bytes,
        output_bytes=target.stat().st_size if target.exists() else 0, bit_depth=depth,
    )


def _measure(path: Path, *, ffmpeg: str, settings: Settings, runner: Runner) -> Loudness:
    argv = (ffmpeg, "-hide_banner", "-nostats", "-i", str(path), "-af", measure_filter(settings))
    result = _run_or_refuse(runner, Command(label="measure", argv=(*argv, "-f", "null", "-")))
    return parse_loudness(result.stderr)


def _run_or_refuse(runner: Runner, command: Command) -> CommandResult:
    result = runner(command)
    if result.returncode != 0:
        raise MasteringRefused(
            Refusal.ENCODER_FAILED,
            f"the {command.label} stage failed: {result.stderr.strip()[-400:]}",
        )
    return result


def _wrote_or_refuse(target: Path, label: str) -> None:
    """A zero exit status is a CLAIM about the output, so check the output.

    The encoder is whatever ``CRATEKIT_BIN_FFMPEG`` or PATH names, and a stub or
    a build without FLAC can exit 0 and write nothing, which would otherwise be
    reported as a master saving every byte. An empty file counts as no file.
    """
    if not target.exists() or target.stat().st_size == 0:
        raise MasteringRefused(
            Refusal.ENCODER_FAILED,
            f"the {label} stage reported success and produced no output at "
            f"{target}. The source is unchanged and its archive is intact, so "
            f"nothing was lost; check that the encoder on PATH, or the one named "
            f"by CRATEKIT_BIN_FFMPEG, is a working ffmpeg with FLAC support.",
            path=target,
        )


def concatenate(
    parts: Sequence[Path | str], destination: Path | str, *, runner: Runner = subprocess_runner
) -> Path:
    """Join a recording a device split across several files into one source.

    A stream copy, not a re-encode, so there is no generation loss. The list file
    is written beside the destination, for the size reason the intermediate is.
    """
    ordered = [Path(p) for p in parts]
    missing = [p for p in ordered if not p.is_file()]
    if missing:
        raise MasteringRefused(
            Refusal.SOURCE_MISSING,
            f"cannot join: {', '.join(str(p) for p in missing)} not found",
        )
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    listing = destination.parent / f".{destination.stem}.cratekit-parts.txt"
    # The concat demuxer reads single quoted paths and unescapes a doubled quote;
    # an apostrophe written raw silently truncates the entry.
    listing.write_text(
        "".join(f"file '{str(p.resolve()).replace(chr(39), chr(39) * 2)}'\n" for p in ordered),
        encoding="utf-8",
    )
    (ffmpeg,) = _resolve("ffmpeg")
    # A joined WAV is written as RF64 when it needs to be: a split recording is
    # long, and a plain header's 32 bit length wraps past 4 GiB, so the next
    # stage would master only part of the set and report it as the whole.
    container = ("-rf64", "auto") if destination.suffix.lower() == ".wav" else ()
    try:
        _run_or_refuse(
            runner,
            Command(
                label="join",
                argv=(
                    ffmpeg, "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-c", "copy", *container, str(destination),
                ),
            ),
        )
    finally:
        listing.unlink(missing_ok=True)
    _wrote_or_refuse(destination, "join")
    return destination


def master_parts(
    parts: Sequence[Path | str], *, settings: Settings = DEFAULT_SETTINGS,
    output_dir: Path | None = None, overwrite: bool = False, runner: Runner = subprocess_runner,
    workspace: Path | None = None,
) -> Report:
    """Master a recording a player split into several files, as one set.

    One part is :func:`master` alone. Parts join in the order given, never
    sorted (``REC10`` sorts before ``REC2``). Every refusal decidable by reading,
    a probe of every part included, comes before the first write: a stream copy
    across layouts does not fail, it plays at the wrong speed. Each part is
    archived beside itself; the join is written in a fresh private directory.
    """
    paths = [Path(p) for p in parts]
    if not paths:
        raise MasteringRefused(Refusal.SOURCE_MISSING, "no recording was named")
    if len(paths) == 1:
        return master(
            paths[0], settings=settings, output_dir=output_dir, overwrite=overwrite,
            runner=runner, workspace=workspace,
        )

    for path in paths:
        _check_source(path)
    seen: dict[Path, Path] = {}
    for path in paths:
        key = path.resolve()
        if key in seen:
            raise MasteringRefused(
                Refusal.SOURCE_UNSUPPORTED,
                f"{path} is named twice. Joining it twice would repeat that part "
                f"of the set in the master; name each part once, in order.",
                path=path,
            )
        seen[key] = path
    containers = sorted({p.suffix.lower() for p in paths})
    if len(containers) > 1:
        raise MasteringRefused(
            Refusal.SOURCE_UNSUPPORTED,
            f"the parts are in different containers ({', '.join(containers)}). "
            f"They are joined by stream copy, which cannot put one container's "
            f"audio into another; convert them to one container first.",
            path=paths[0],
        )

    target = planned_output(paths, output_dir=output_dir)
    if target.exists() and not overwrite:
        raise _output_exists(target)
    _, ffprobe = _resolve("ffmpeg", "ffprobe", path=paths[0])

    probes = [probe_source(p, runner=runner, ffprobe=ffprobe) for p in paths]
    # Every field the stream copy depends on, not only the rate.
    shapes = {(p.sample_rate, p.sample_fmt, p.channels, p.codec) for p in probes}
    if len(shapes) > 1:
        described = "; ".join(
            f"{path.name} is {probe.sample_rate} Hz "
            f"{probe.codec or probe.sample_fmt or 'unknown format'}, "
            f"{probe.channels if probe.channels is not None else 'unknown'} channels"
            for path, probe in zip(paths, probes, strict=True)
        )
        raise MasteringRefused(
            Refusal.SOURCE_UNSUPPORTED,
            f"the parts do not share one audio layout ({described}). "
            f"A stream copy across them would play part of the set at the wrong "
            f"speed, and nothing is resampled without being asked; nothing was "
            f"archived and nothing was written.",
            path=paths[0],
        )

    archives = tuple(archive_source(p, p.parent / ARCHIVE_DIRNAME) for p in paths)

    scratch = workspace or target.parent
    scratch.mkdir(parents=True, exist_ok=True)
    join_dir = Path(tempfile.mkdtemp(prefix=".cratekit-join-", dir=scratch))
    try:
        joined = concatenate(paths, join_dir / joined_name(paths), runner=runner)
        report = master(
            joined, settings=settings, output_dir=target.parent, archive=False,
            overwrite=overwrite, runner=runner, workspace=join_dir,
        )
    finally:
        shutil.rmtree(join_dir, ignore_errors=True)
    return replace(
        report, source=paths[0], archived_to=archives[0], parts=tuple(paths), archives=archives
    )


# Structured output (R32)

PAYLOAD_VERSION = 1


def _loudness_payload(loudness: Loudness) -> dict:
    return {
        "integrated_lufs": loudness.integrated_lufs,
        "loudness_range": loudness.loudness_range,
        "true_peak_db": loudness.true_peak_db,
    }


def as_payload(report: Report) -> dict:
    """The report as plain data; ``parts`` and ``archives`` only for a joined run."""
    payload = {
        "payload_version": PAYLOAD_VERSION, "source": str(report.source),
        "output": str(report.output),
        "archived_to": str(report.archived_to) if report.archived_to else None,
        "bit_depth": report.bit_depth,
        "before": _loudness_payload(report.before), "after": _loudness_payload(report.after),
        "source_bytes": report.source_bytes, "output_bytes": report.output_bytes,
        "size_reduction": round(report.size_reduction, 6),
    }
    if report.parts:
        payload["parts"] = [str(p) for p in report.parts]
        payload["archives"] = [str(p) for p in report.archives]
    return payload


__all__ = [
    "ARCHIVE_DIRNAME", "DEFAULT_SETTINGS", "DRIFT_WINDOW_RANGE", "JOINED_SUFFIX", "LUFS_RANGE",
    "OUTPUT_SUFFIX", "PAYLOAD_VERSION", "SOURCE_SUFFIXES", "Command", "CommandResult",
    "Loudness", "MasteringRefused", "Refusal", "Report", "Settings", "SourceProbe",
    "apply_filter", "archive_source", "as_payload", "concatenate", "digest", "drift_filter",
    "encoder_args", "joined_name", "master", "master_parts", "measure_filter",
    "output_exists_detail", "output_path", "parse_loudness", "parse_output_loudness",
    "planned_output", "probe_source", "subprocess_runner",
]
