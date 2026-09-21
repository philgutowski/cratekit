"""Feature Inventory row 30: mastering a live set recording.

One recording at a time, touching no core surface. It reads a source file, writes
a new lossless FLAC beside it, and never modifies or deletes the source. That
last clause is R18 and it is the reason this module is worth porting carefully:
the input is a recording of a performance that happened once, so a mistake here
is not recoverable from anywhere.

WHAT IT ACTUALLY DOES, and why in that order.

1. **Archive the source and verify the copy** before touching anything. Verified
   by content hash rather than by a byte comparison utility, so the check is the
   same on every platform and does not depend on an external tool.
2. **Drift correction.** A live set is recorded with somebody's hand on the
   master knob, so the level steps up and down across the recording. A long
   smoothing window pulls those slow steps flat while leaving the short-term
   musical dynamics alone. A short window would flatten the music itself.
3. **Measure, then normalize linearly.** Two passes: the first measures the
   corrected signal, the second applies a single gain offset with a true-peak
   ceiling. Linear mode matters. A one-pass normalization compresses to reach the
   target, which changes how the set sounds; a measured linear offset only moves
   it.
4. **Encode FLAC at the source's own bit depth.** Sixteen-bit sources are
   dithered back to sixteen; deeper sources stay at twenty-four. Forcing
   twenty-four on a sixteen-bit recording produces a file LARGER than the source
   WAV, which defeats the point of the conversion, and adds no information.

FIVE THINGS THIS PORT CHANGES.

* **The binaries are resolved, not assumed.** The source shell script tests
  ``command -v ffmpeg``, so it works in a login shell and fails inside an
  application launched from a graphical file manager, where none of the usual
  install directories are on PATH.
* **The loudness report is parsed as JSON.** The source greps for a key across
  the whole of ffmpeg's stderr and takes the last hit, so a value from the
  measurement block can be read as a value from the apply block, silently.
* **An existing output is not overwritten.** The source passes ``-y``
  unconditionally, so a second run at a different target loudness replaces a
  master the user may already have kept.
* **An existing archive entry is verified, not trusted.** The source skips the
  copy when a file of that name is already in the archive. Two different
  recordings called ``REC001.WAV``, which is exactly what a recorder produces,
  therefore leave the second one unarchived while reporting that it is safe.
* **Settings are validated at construction.** A drift window outside the filter's
  accepted range makes ffmpeg fail several minutes into a long encode, naming its
  own filter rather than the option the user typed.

WHY THE EXECUTION IS A SEAM. Every subprocess goes through an injected runner, so
the decisions above (which filter chain, which encoder arguments, which output
name, whether to refuse) are all testable without encoding audio, and the one
test that does encode audio exercises the same code path rather than a parallel
one.
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

#: Containers this module will accept as a source. Deliberately narrow: these are
#: what a DJ recorder writes, and the two-pass measurement assumes a single
#: continuous audio stream.
SOURCE_SUFFIXES: tuple[str, ...] = (".wav", ".aiff", ".aif", ".flac")

#: Where a verified copy of each source is kept, relative to the source's own
#: directory. Beside the recording rather than in a state root: it is the user's
#: own audio, not Cratekit's bookkeeping, and it must survive uninstalling this.
ARCHIVE_DIRNAME = "_originals"

OUTPUT_SUFFIX = "_mastered.flac"

#: The drift filter's accepted smoothing window, in frames. ffmpeg refuses
#: outside this and refuses an even value.
DRIFT_WINDOW_RANGE = (3, 301)

#: The integrated loudness targets loudnorm accepts, LUFS. ffmpeg refuses a
#: value outside this, and it refuses at the first measure pass rather than at
#: the command line, so a mistyped ``--lufs`` would otherwise surface as an
#: encoder failure naming the filter. U105 added the check: before it the target
#: was a constant nobody could reach, so there was nothing to validate.
LUFS_RANGE = (-70.0, -5.0)

#: What a joined recording is called, after the first part's stem. The source
#: system's ``master_set.sh`` names a joined set ``<first>_set`` for the same
#: reason: the master of a joined set must not take the name the first part's
#: own master would have, or mastering part one alone and then the whole set
#: meets ``output-exists`` against a file that holds something else.
JOINED_SUFFIX = "_set"


class Refusal(StrEnum):
    """Why a mastering run will not proceed, as a structured cause (KTD25).

    Every member is a distinct diagnosis with a distinct fix, and none of them
    carries the text a user types: the CLI renders a member into a sentence and
    reserves an exit code for it (D2, S4).
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
    """Loudness targets and the drift window, validated at construction.

    Validated here rather than at the ffmpeg call because the alternative is a
    filter error arriving minutes into an encode, naming ``dynaudnorm`` rather
    than the option the user typed.
    """

    #: Integrated loudness target, LUFS. -14 suits general playback; a louder
    #: target suits streaming platforms that normalize upward.
    target_lufs: float = -14.0
    #: True-peak ceiling, dBTP. Below zero on purpose: inter-sample peaks in a
    #: lossy transcode of this file can exceed the sample peak.
    true_peak_db: float = -1.0
    #: Loudness range target, LU. Part of what keeps the normalization linear.
    loudness_range: float = 11.0
    #: Drift smoothing window, in frames. Odd, within DRIFT_WINDOW_RANGE. Lower
    #: flattens drift harder and costs dynamics; higher preserves dynamics and
    #: may leave drift behind.
    drift_window: int = 63
    #: Analysis frame length, milliseconds.
    frame_ms: int = 500

    def __post_init__(self) -> None:
        low, high = DRIFT_WINDOW_RANGE
        if not low <= self.drift_window <= high:
            raise ValueError(
                f"drift_window must be between {low} and {high}, found "
                f"{self.drift_window}"
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
        # WRITTEN AS A NEGATED RANGE so a NaN fails it: every comparison with
        # NaN is false, so ``x < low or x > high`` would admit one and hand
        # loudnorm a target of ``nan``.
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
    #: The parts a joined run was built from, in the order they were joined, and
    #: the verified archive copy of each. Both empty for a single recording,
    #: whose one source and one archive are the two fields above.
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
    #: True when the caller needs the process's stderr, which is where ffmpeg
    #: prints its loudness JSON.
    capture: bool = True


@dataclass(frozen=True, slots=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


Runner = Callable[[Command], CommandResult]


def subprocess_runner(command: Command) -> CommandResult:
    """Run one command with the fallback directories on PATH.

    ``binaries.subprocess_env`` is what makes a child process able to resolve its
    own children, and it strips opted-in credentials from the environment: ffmpeg
    has no use for a Cratekit credential and a process listing is a place they
    leak from.
    """
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


# ---------------------------------------------------------------------------
# Pure decisions
# ---------------------------------------------------------------------------


def output_path(source: Path, *, output_dir: Path | None = None) -> Path:
    """Where the mastered file lands: beside the source unless told otherwise."""
    directory = output_dir if output_dir is not None else source.parent
    return directory / f"{source.stem}{OUTPUT_SUFFIX}"


def joined_name(parts: Sequence[Path]) -> str:
    """The file name a joined recording is written under, before it is mastered.

    The first part's stem and container, because the join is a stream copy and
    the joined file is therefore in the first part's container.
    """
    first = parts[0]
    return f"{first.stem}{JOINED_SUFFIX}{first.suffix}"


def planned_output(parts: Sequence[Path | str], *, output_dir: Path | None = None) -> Path:
    """Where the master of these parts lands. The one name builder for both shapes.

    One part is exactly :func:`output_path`. Several are named for the joined
    recording and land beside the FIRST part unless told otherwise, which is
    where the person's recording already is. The shell checks the destination
    with this before staging the encode, so the check and the encode cannot
    disagree about which file they mean.
    """
    paths = [Path(p) for p in parts]
    if len(paths) == 1:
        return output_path(paths[0], output_dir=output_dir)
    return output_path(paths[0].parent / joined_name(paths), output_dir=output_dir)


def drift_filter(settings: Settings) -> str:
    """The level-drift correction stage.

    ``p`` and ``m`` bound how far the filter may push any one frame, so a quiet
    passage is not dragged up to match a loud one. ``s=0.0`` disables the
    filter's own extra smoothing, because the window above is already the
    smoothing and stacking a second one is how musical dynamics disappear.
    """
    return (
        f"dynaudnorm=f={settings.frame_ms}:g={settings.drift_window}"
        f":p=0.95:m=10.0:s=0.0"
    )


def measure_filter(settings: Settings) -> str:
    """Pass one: measure only, and print the result as JSON."""
    return (
        f"loudnorm=I={settings.target_lufs}:TP={settings.true_peak_db}"
        f":LRA={settings.loudness_range}:print_format=json"
    )


def apply_filter(settings: Settings, measured: Loudness) -> str:
    """Pass two: apply the measured offset linearly, with the peak ceiling.

    Every measured value is fed back in. Omitting one silently drops the filter
    out of linear mode into its dynamic mode, which compresses to hit the target
    instead of moving the whole set, and the output is quieter-sounding and
    flatter with nothing reported.
    """
    missing = [
        name
        for name, value in (
            ("integrated", measured.integrated_lufs),
            ("true peak", measured.true_peak_db),
            ("loudness range", measured.loudness_range),
            ("threshold", measured.threshold),
            ("target offset", measured.target_offset),
        )
        if value is None
    ]
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

    A sixteen-bit source is dithered back to sixteen. The dither is not optional:
    the filter chain runs in floating point, so truncating to sixteen bits
    without it adds correlated quantization distortion, which is audible on the
    quiet passages a DJ set has plenty of.
    """
    if probe.is_16_bit:
        return (
            ("-c:a", "flac", "-compression_level", "8"),
            "aresample=out_sample_fmt=s16:dither_method=triangular_hp",
            "16-bit, dithered",
        )
    return (
        ("-c:a", "flac", "-compression_level", "8", "-sample_fmt", "s32",
         "-bits_per_raw_sample", "24"),
        "",
        "24-bit",
    )


_JSON_BLOCK = re.compile(r"\{[^{}]*\}")


def parse_loudness(stderr_text: str) -> Loudness:
    """Read ffmpeg's loudnorm report out of stderr.

    The LAST JSON object is taken because ffmpeg prints its block after the
    encode, and a two-pass run can put more than one in a single stream. Parsing
    it as JSON rather than grepping for each key is the fix for a real ambiguity:
    a key-by-key grep across the whole stream can pair a value from the
    measurement block with a value from the apply block, and the resulting
    "measurement" describes no signal that ever existed.
    """
    blocks = _JSON_BLOCK.findall(stderr_text or "")
    for raw in reversed(blocks):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict) or "input_i" not in data:
            continue
        return Loudness(
            integrated_lufs=_as_float(data.get("input_i")),
            loudness_range=_as_float(data.get("input_lra")),
            true_peak_db=_as_float(data.get("input_tp")),
            threshold=_as_float(data.get("input_thresh")),
            target_offset=_as_float(data.get("target_offset")),
        )
    return Loudness()


def parse_output_loudness(stderr_text: str) -> Loudness:
    """The same report read from its OUTPUT half, for the after-figures."""
    blocks = _JSON_BLOCK.findall(stderr_text or "")
    for raw in reversed(blocks):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict) or "output_i" not in data:
            continue
        return Loudness(
            integrated_lufs=_as_float(data.get("output_i")),
            loudness_range=_as_float(data.get("output_lra")),
            true_peak_db=_as_float(data.get("output_tp")),
        )
    return Loudness()


def _as_float(value: object) -> float | None:
    """A finite float, or None. Non-finite is UNKNOWN, not a value.

    loudnorm reports ``-inf`` for a silent signal, and Python parses that
    happily. Carrying it forward would put negative infinity into the apply
    stage's own options, where ffmpeg either rejects it or normalizes against a
    measurement that describes no signal. None makes the apply stage refuse with
    a sentence naming what is missing.
    """
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if parsed == parsed and abs(parsed) != float("inf") else None


# ---------------------------------------------------------------------------
# The archive: copy first, verify, never trust a name
# ---------------------------------------------------------------------------


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

    An entry already present under the same name is VERIFIED rather than assumed.
    Recorders name their files by counter, so two different sets called
    ``REC001.WAV`` is the normal case, not the exotic one, and the source
    system's "archive exists, skipping" leaves the second recording unarchived
    while reporting that it is safe.
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
        # Verify before proceeding, not after: the whole reason the archive is
        # taken first is so the rest of the run has something to fall back on.
        destination.unlink(missing_ok=True)
        raise MasteringRefused(
            Refusal.ARCHIVE_VERIFY_FAILED,
            f"the archived copy of {source.name} did not match the source, so the "
            f"safety copy this run depends on does not exist",
            path=destination,
        )
    return destination


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------


def probe_source(source: Path, *, runner: Runner, ffprobe: str) -> SourceProbe:
    """Sample rate, sample format, and size. Refuses rather than guessing."""
    command = Command(
        label="probe",
        argv=(
            ffprobe, "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=sample_rate,sample_fmt",
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
    values = dict(
        line.split("=", 1)
        for line in result.stdout.splitlines()
        if "=" in line
    )
    try:
        rate = int(values["sample_rate"])
    except (KeyError, ValueError) as exc:
        raise MasteringRefused(
            Refusal.ENCODER_FAILED,
            f"{source.name} reported no usable sample rate, so the encode cannot "
            f"preserve it",
            path=source,
        ) from exc
    return SourceProbe(
        sample_rate=rate,
        sample_fmt=values.get("sample_fmt", ""),
        size_bytes=source.stat().st_size,
    )


def master(
    source: Path | str,
    *,
    settings: Settings = DEFAULT_SETTINGS,
    output_dir: Path | None = None,
    archive: bool = True,
    archive_dir: Path | None = None,
    overwrite: bool = False,
    runner: Runner = subprocess_runner,
    workspace: Path | None = None,
) -> Report:
    """Master one recording. The source is opened read-only and never modified.

    The order is load-bearing and is asserted by the tests: refuse, archive,
    then process. Archiving after the first ffmpeg stage would mean a crash
    between them leaves the user with a half-written intermediate and no verified
    copy, which is the one state this whole module exists to make impossible.

    ``workspace`` is where the intermediate drift-corrected file is written. It
    defaults to the OUTPUT directory rather than the system temp directory,
    because a set recording is measured in gigabytes and a small temp filesystem
    is a failure that arrives at the end of a long stage.
    """
    source = Path(source)
    if not source.is_file():
        raise MasteringRefused(
            Refusal.SOURCE_MISSING, f"no such recording: {source}", path=source
        )
    if source.suffix.lower() not in SOURCE_SUFFIXES:
        raise MasteringRefused(
            Refusal.SOURCE_UNSUPPORTED,
            f"{source.suffix!r} is not a container this reads; supported: "
            f"{', '.join(SOURCE_SUFFIXES)}",
            path=source,
        )

    target = output_path(source, output_dir=output_dir)
    if target.exists() and not overwrite:
        raise MasteringRefused(
            Refusal.OUTPUT_EXISTS,
            f"{target} already exists. Replacing it silently would discard a "
            f"master that may already have been kept, and the settings that "
            f"produced it are not recorded anywhere.",
            path=target,
        )

    try:
        ffmpeg = binaries.resolve("ffmpeg")
        ffprobe = binaries.resolve("ffprobe")
    except binaries.BinaryNotFound as exc:
        raise MasteringRefused(Refusal.ENCODER_MISSING, str(exc), path=source) from exc

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
                    "-c:a", "pcm_s24le", str(intermediate),
                ),
            ),
        )
        measured = _measure(
            intermediate, ffmpeg=ffmpeg, settings=settings, runner=runner
        )
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
        # The intermediate is Cratekit's, not the user's. Leaving a
        # multi-gigabyte scratch WAV beside the recording after a failure is how
        # a volume fills up between one run and the next.
        intermediate.unlink(missing_ok=True)

    _wrote_or_refuse(target, "normalize-and-encode")
    return Report(
        source=source,
        output=target,
        archived_to=archived_to,
        before=before,
        after=parse_output_loudness(applied.stderr),
        source_bytes=probe.size_bytes,
        output_bytes=target.stat().st_size if target.exists() else 0,
        bit_depth=depth,
    )


def _measure(
    path: Path, *, ffmpeg: str, settings: Settings, runner: Runner
) -> Loudness:
    result = _run_or_refuse(
        runner,
        Command(
            label="measure",
            argv=(
                ffmpeg, "-hide_banner", "-nostats", "-i", str(path),
                "-af", measure_filter(settings), "-f", "null", "-",
            ),
        ),
    )
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

    U44 DROVE THIS RATHER THAN ARGUING IT. An encoder that exits 0 and writes
    nothing left ``master`` returning a Report whose ``output`` named a file that
    was not there, whose ``output_bytes`` was 0 because the construction below
    falls back to zero when the target is missing, and whose ``size_reduction``
    was therefore 1.0. The shell rendered that as a success: a master that saved
    one hundred percent of the source's bytes. Two of METHOD's named user facing
    costs at once, told something false and shown a clean report over state the
    tool could not read.

    THE READING IS HERE RATHER THAN IN THE CALLER, which is the placement the
    corpus entry on first callers argues for: the caller that found it is one
    caller, and the checking path covers every future one. It is the same shape
    as ``run_restore``'s unread return codes, one module over in this package,
    and the same fix.

    REACHABLE, AND NAMED. ``core.binaries`` reads ``CRATEKIT_BIN_FFMPEG`` before
    PATH, so the program that answers these commands is a value the user sets.
    ``override_problem`` rejects one that is not executable and cannot reject one
    that runs and does nothing useful, which is the state a wrapper script, a
    stub, or a build missing the flac encoder is in.

    An empty file is treated as no file. A zero-byte FLAC is not a master, and
    reporting a saving of exactly 1.0 over one is the same false claim.
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
    parts: Sequence[Path | str],
    destination: Path | str,
    *,
    runner: Runner = subprocess_runner,
) -> Path:
    """Join a recording a device split across several files into one source.

    Stream copy, not a re-encode: the parts came off one continuous recording and
    re-encoding them before mastering would introduce a generation loss for no
    reason. The list file is written next to the DESTINATION rather than in the
    system temp directory, for the same size reason the intermediate is.
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
    # ffmpeg's concat demuxer reads single-quoted paths and unescapes a doubled
    # quote. A path containing an apostrophe is ordinary in track titles, and
    # writing it raw silently truncates the entry.
    listing.write_text(
        "".join(f"file '{str(p.resolve()).replace(chr(39), chr(39) * 2)}'\n" for p in ordered),
        encoding="utf-8",
    )
    try:
        ffmpeg = binaries.resolve("ffmpeg")
    except binaries.BinaryNotFound as exc:
        raise MasteringRefused(Refusal.ENCODER_MISSING, str(exc)) from exc
    try:
        _run_or_refuse(
            runner,
            Command(
                label="join",
                argv=(
                    ffmpeg, "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-c", "copy", str(destination),
                ),
            ),
        )
    finally:
        listing.unlink(missing_ok=True)
    # THE SAME SHAPE ONE FUNCTION OVER, found by sweeping for it rather than by
    # anybody reporting it (METHOD's fifth pattern). This branch also read a zero
    # exit status as proof that the join happened and returned a path it never
    # looked at, so a caller would go on to master a file that is not there. It
    # has no caller in ``src`` today, which is what kept it quiet, and that is
    # exactly the condition the first-caller rule says not to trust.
    _wrote_or_refuse(destination, "join")
    return destination


def master_parts(
    parts: Sequence[Path | str],
    *,
    settings: Settings = DEFAULT_SETTINGS,
    output_dir: Path | None = None,
    overwrite: bool = False,
    runner: Runner = subprocess_runner,
    workspace: Path | None = None,
) -> Report:
    """Master a recording a player split into several files, as one set.

    ONE PART IS :func:`master` AND NOTHING ELSE, so a single recording takes
    exactly the path it took before a join existed.

    THE PARTS ARE JOINED IN THE ORDER GIVEN, NEVER SORTED. Only the person knows
    the order: a recorder's counter rolls over, and a name sort puts
    ``REC10`` before ``REC2``. The shell prints the order back before anything
    runs, so a wrong order is seen rather than mastered.

    THE ORDER OF THE STEPS IS THE ONE :func:`master` STATES, widened: refuse,
    archive, then process. Every refusal that can be decided by reading comes
    before the first write, including the probe of every part, because a stream
    copy across parts at different sample rates does not fail. It writes a file
    whose header claims one rate over samples taken at another, and the master of
    that file plays part of the set at the wrong speed with nothing reported.
    ffmpeg's concat demuxer does not resample, so this refuses instead of
    inventing a conversion the person did not ask for.

    EVERY PART IS ARCHIVED, each into the ``_originals`` beside it, which is the
    rule :func:`master` applies to its one source. The joined file is this
    module's own intermediate, so it is not archived and it does not survive the
    run.

    THE JOINED FILE IS WRITTEN INTO A PRIVATE DIRECTORY under the workspace,
    created fresh and removed afterwards. It has to carry the name the master is
    derived from, and writing ``REC001_set.wav`` straight into the person's
    folder with ffmpeg's ``-y`` would replace a file of theirs that happened to
    have that name.
    """
    paths = [Path(p) for p in parts]
    if not paths:
        raise MasteringRefused(Refusal.SOURCE_MISSING, "no recording was named")
    if len(paths) == 1:
        return master(
            paths[0],
            settings=settings,
            output_dir=output_dir,
            overwrite=overwrite,
            runner=runner,
            workspace=workspace,
        )

    for path in paths:
        if not path.is_file():
            raise MasteringRefused(
                Refusal.SOURCE_MISSING, f"no such recording: {path}", path=path
            )
        if path.suffix.lower() not in SOURCE_SUFFIXES:
            raise MasteringRefused(
                Refusal.SOURCE_UNSUPPORTED,
                f"{path.suffix!r} is not a container this reads; supported: "
                f"{', '.join(SOURCE_SUFFIXES)}",
                path=path,
            )
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
        raise MasteringRefused(
            Refusal.OUTPUT_EXISTS,
            f"{target} already exists. Replacing it silently would discard a "
            f"master that may already have been kept, and the settings that "
            f"produced it are not recorded anywhere.",
            path=target,
        )

    try:
        binaries.resolve("ffmpeg")
        ffprobe = binaries.resolve("ffprobe")
    except binaries.BinaryNotFound as exc:
        raise MasteringRefused(Refusal.ENCODER_MISSING, str(exc), path=paths[0]) from exc

    probes = [probe_source(p, runner=runner, ffprobe=ffprobe) for p in paths]
    shapes = {(p.sample_rate, p.sample_fmt) for p in probes}
    if len(shapes) > 1:
        described = "; ".join(
            f"{path.name} is {probe.sample_rate} Hz {probe.sample_fmt or 'unknown format'}"
            for path, probe in zip(paths, probes, strict=True)
        )
        raise MasteringRefused(
            Refusal.SOURCE_UNSUPPORTED,
            f"the parts do not share one sample rate and sample format ({described}). "
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
            joined,
            settings=settings,
            output_dir=target.parent,
            archive=False,
            overwrite=overwrite,
            runner=runner,
            workspace=join_dir,
        )
    finally:
        # The joined file is as large as the whole set and is this module's, not
        # the person's, for the reason the drift intermediate is removed.
        shutil.rmtree(join_dir, ignore_errors=True)
    return replace(
        report,
        source=paths[0],
        archived_to=archives[0],
        parts=tuple(paths),
        archives=archives,
    )


# ---------------------------------------------------------------------------
# Structured output (R32)
# ---------------------------------------------------------------------------

PAYLOAD_VERSION = 1


def as_payload(report: Report) -> dict:
    """The report as plain data. Human rendering stays with the CLI.

    ``parts`` and ``archives`` appear only for a joined run, so a single
    recording's payload is the one it was before a join existed.
    """
    payload = {
        "payload_version": PAYLOAD_VERSION,
        "source": str(report.source),
        "output": str(report.output),
        "archived_to": str(report.archived_to) if report.archived_to else None,
        "bit_depth": report.bit_depth,
        "before": {
            "integrated_lufs": report.before.integrated_lufs,
            "loudness_range": report.before.loudness_range,
            "true_peak_db": report.before.true_peak_db,
        },
        "after": {
            "integrated_lufs": report.after.integrated_lufs,
            "loudness_range": report.after.loudness_range,
            "true_peak_db": report.after.true_peak_db,
        },
        "source_bytes": report.source_bytes,
        "output_bytes": report.output_bytes,
        "size_reduction": round(report.size_reduction, 6),
    }
    if report.parts:
        payload["parts"] = [str(p) for p in report.parts]
        payload["archives"] = [str(p) for p in report.archives]
    return payload


__all__ = [
    "ARCHIVE_DIRNAME",
    "DEFAULT_SETTINGS",
    "DRIFT_WINDOW_RANGE",
    "JOINED_SUFFIX",
    "LUFS_RANGE",
    "OUTPUT_SUFFIX",
    "PAYLOAD_VERSION",
    "SOURCE_SUFFIXES",
    "Command",
    "CommandResult",
    "Loudness",
    "MasteringRefused",
    "Refusal",
    "Report",
    "Settings",
    "SourceProbe",
    "apply_filter",
    "archive_source",
    "as_payload",
    "concatenate",
    "digest",
    "drift_filter",
    "encoder_args",
    "joined_name",
    "master",
    "master_parts",
    "measure_filter",
    "output_path",
    "parse_loudness",
    "parse_output_loudness",
    "planned_output",
    "probe_source",
    "subprocess_runner",
]
