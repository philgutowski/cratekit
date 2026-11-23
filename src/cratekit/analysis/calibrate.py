"""``crate analyze calibrate``: fit the energy reference and the vocal cut.

The verb's parser and its registered names stay in :mod:`cratekit.analysis.cli`;
this is the body, imported by the handler when the verb runs.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence, TypeVar

from cratekit.analysis import energy
from cratekit.analysis.cli import (
    _ORIGIN,
    DEFAULT_VOCAL_THRESHOLD,
    _check,
    _folder_of,
    _require_heavy,
)
from cratekit.cli.output import Envelope, load_config
from cratekit.core import config, jobs, tags
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import Remedy

_T = TypeVar("_T")

#: The vocal cut is stored beside the energy calibration, in the state file
#: ``core.config`` declares for it. The threshold is PASSED to the router,
#: never imported by it (D7).
STATE_KEY_VOCAL_CALIBRATION = "vocal_calibration"
#: The presence score's range, the percentage of frames the model hears
#: singing in. A cut set by hand outside it is refused (U90).
VOCAL_SCORE_MIN = 0.0
VOCAL_SCORE_MAX = 100.0
#: The ``method`` a cut set by hand is recorded under, beside the fit's "otsu".
VOCAL_METHOD_HAND = "hand"
#: How far apart the two clusters' means must sit for a cut between them to
#: mean anything: Otsu splits even a one cluster folder down the middle.
MIN_VOCAL_SEPARATION = 10.0
#: How many measured tracks a calibration needs before its deciles mean anything.
MIN_CALIBRATION_TRACKS = 10

#: The warning a calibration fitted over less than the library wide walk
#: carries, when ``--accept-partial`` said to (U94).
PARTIAL_SAMPLE = "calibration-partial-sample"


def otsu_threshold(scores: list[float], *, bins: int = 100) -> float:
    """The cut that best separates two clusters of presence scores (0 to 100).

    Maximizes the between class variance over a histogram. Whether the input
    HAS two clusters is :func:`cluster_separation`'s question.
    """
    import numpy as np

    values = np.asarray(scores, dtype=float)
    hist, edges = np.histogram(values, bins=bins, range=(VOCAL_SCORE_MIN, VOCAL_SCORE_MAX))
    total = float(hist.sum())
    if total <= 0:
        return DEFAULT_VOCAL_THRESHOLD
    probability = hist / total
    centers = (edges[:-1] + edges[1:]) / 2.0
    best_cut = DEFAULT_VOCAL_THRESHOLD
    best_variance = -1.0
    weight_low = 0.0
    mean_low_sum = 0.0
    overall_mean = float((probability * centers).sum())
    for index, (p, center) in enumerate(zip(probability, centers)):
        weight_low += p
        mean_low_sum += p * center
        weight_high = 1.0 - weight_low
        if weight_low <= 0 or weight_high <= 0:
            continue
        mean_low = mean_low_sum / weight_low
        mean_high = (overall_mean - mean_low_sum) / weight_high
        variance = weight_low * weight_high * (mean_low - mean_high) ** 2
        if variance > best_variance:
            best_variance = variance
            best_cut = float(edges[index + 1])
    return best_cut


def cluster_separation(scores: list[float], threshold: float) -> float | None:
    """How far apart the means either side of ``threshold`` sit, or None.

    None when one side is empty: a cut with nothing on one side of it.
    """
    low = [score for score in scores if score < threshold]
    high = [score for score in scores if score >= threshold]
    if not low or not high:
        return None
    return sum(high) / len(high) - sum(low) / len(low)


def vocal_calibration_path(cfg: config.Config) -> Path:
    return config.state_path(STATE_KEY_VOCAL_CALIBRATION, cfg)


def stride_sample(items: Sequence[_T], count: int) -> list[_T]:
    """At most ``count`` of ``items``, taken at an even stride, in their order.

    DETERMINISTIC ON PURPOSE (U94): the same tree must give the same fit, the
    only evidence a person has that nothing moved. Over the SORTED walk an
    even stride takes from every genre folder in proportion to its size.
    ``index * len // count`` rather than a fixed step, which stops short of
    the tail whenever the division has a remainder.
    """
    total = len(items)
    if count <= 0:
        return []
    if total <= count:
        return list(items)
    return [items[index * total // count] for index in range(count)]


def fitted_note(fitted: int, walked: int, folder: Path, left_out: int = 0) -> str:
    """The provenance a calibration file records about itself (U94).

    ``left_out`` counts folders the walk declined or could not list: the file
    outlives the run's warnings, and a later restamp trusts it.
    """
    note = f"fitted over {fitted} of {walked} under {folder}"
    if left_out:
        note += f", with {left_out} folder{'' if left_out == 1 else 's'} not walked"
    return note


def _calibrate_energy(
    cfg: config.Config, folder: Path, sampled: list[Path], walked: int, left_out: int = 0
) -> dict[str, str | None]:
    measured: list[dict[str, float]] = []
    unreadable = 0
    for path in sampled:
        features = energy.measure(path)
        if features is None:
            unreadable += 1
            continue
        measured.append(features)
    if len(measured) < MIN_CALIBRATION_TRACKS:
        return _check(
            "calibrate.energy",
            "energy calibration",
            "failed",
            f"{len(measured)} of the {len(sampled)} tracks sampled under {folder} "
            f"could be measured, and a calibration needs at least "
            f"{MIN_CALIBRATION_TRACKS}; nothing was written",
            Remedy.FIX_COMMAND_LINE,
        )
    calibration = energy.calibrate(
        measured, note=fitted_note(len(measured), walked, folder, left_out)
    )
    written = energy.save_calibration(cfg, calibration)
    levels = [energy.level_for(features, calibration) for features in measured]
    counts = energy.distribution(levels)
    return _check(
        "calibrate.energy",
        "energy calibration",
        "ok",
        f"fitted over {len(measured)} tracks ({unreadable} unreadable), a sample "
        f"of {len(sampled)} from the {walked} under {folder}, written to "
        f"{written}; level distribution {json.dumps(counts, sort_keys=True)}",
        None,
    )


def _calibrate_vocals(
    cfg: config.Config, folder: Path, paths: list[Path], left_out: int = 0
) -> dict[str, str | None]:
    scores = [
        float(level)
        for level in (tags.read_vox_from_file(path) for path in paths)
        if level is not None
    ]
    if not scores:
        return _check(
            "calibrate.vocals",
            "vocal cut",
            "skipped",
            f"no track under {folder} carries a vocal score yet, so there is no "
            f"distribution to cut; run `crate analyze run` over it first",
            Remedy.FIX_COMMAND_LINE,
        )
    threshold = otsu_threshold(scores)
    separation = cluster_separation(scores, threshold)
    if separation is None or separation < MIN_VOCAL_SEPARATION:
        return _check(
            "calibrate.vocals",
            "vocal cut",
            "skipped",
            f"the {len(scores)} scored tracks under {folder} do not split into two "
            f"clusters (best cut {threshold:.1f}, separation "
            f"{0.0 if separation is None else separation:.1f} of the "
            f"{MIN_VOCAL_SEPARATION:.0f} needed), so no cut was written; a walk "
            f"holding both instrumental and vocal tracks is what a cut needs",
            Remedy.FIX_COMMAND_LINE,
        )
    try:
        _, before = _previous_vocal_cut(cfg)
    except CratekitError as exc:
        # The energy half is already written, so a refusal here would report
        # the whole verb failed over a write that happened (U90).
        return _check(
            "calibrate.vocals",
            "vocal cut",
            "failed",
            f"the vocal cut on record could not be opened ({exc.cause.message}), "
            f"so no cut was written over it",
            exc.cause.remediation.remedy,
        )
    target = _write_vocal_calibration(
        cfg,
        threshold,
        method="otsu",
        note=fitted_note(len(scores), len(paths), folder, left_out),
        n_tracks=len(scores),
    )
    above = sum(1 for score in scores if score >= threshold)
    return _check(
        "calibrate.vocals",
        "vocal cut",
        "ok",
        f"cut at {threshold:.1f} over {len(scores)} scored tracks, {above} above it, "
        f"written to {target}; {before}",
        None,
    )


def _today() -> str:
    """The UTC date a hand cut is recorded under. A function so a test can pin it."""
    return datetime.now(timezone.utc).date().isoformat()


def _write_vocal_calibration(
    cfg: config.Config, threshold: float, *, method: str, note: str, **extra: Any
) -> Path:
    """THE ONE WRITER of the vocal calibration, for the fit and the hand cut alike.

    Atomic through ``energy.write_json``. Neither path fits a gender margin,
    so both record the model's default. The one reader is
    ``write.metadata_cli.load_vocal_calibration``.
    """
    from cratekit.analysis import vocal

    return energy.write_json(
        vocal_calibration_path(cfg),
        {
            "threshold": threshold,
            "gender_margin": vocal.DEFAULT_GENDER_MARGIN,
            "method": method,
            "note": note,
            **extra,
        },
    )


def _previous_vocal_cut(cfg: config.Config) -> tuple[float | None, str]:
    """The cut a write is about to replace, as a number and a clause for the report.

    An unreadable file is reported rather than refused, because writing a new
    cut over it is the remedy. A file the account cannot open still refuses,
    as ``path-permission-denied`` (U90).
    """
    from cratekit.write import metadata_cli

    try:
        record = metadata_cli.load_vocal_calibration(cfg)
    except CratekitError as exc:
        if exc.cause.reason != "vocal-calibration-unreadable":
            raise
        return None, "the calibration on record before could not be read, and this replaces it"
    if record is None:
        return None, (
            f"no cut was on record before, so My Tags used the default "
            f"{DEFAULT_VOCAL_THRESHOLD:g}"
        )
    threshold = record["threshold"]
    if record.get("method") == VOCAL_METHOD_HAND:
        return threshold, (
            f"this replaces the cut of {threshold:g} {record.get('note') or 'set by hand'}"
        )
    origin = record.get("note") or record.get("method") or "origin not recorded"
    return threshold, f"this replaces the cut of {threshold:g} ({origin})"


def _set_vocal_cut(ctx, cfg: config.Config, cut: float) -> Envelope:
    """``--vocal-cut``: record a cut a person chose, through the fit's own writer.

    The library's real cut was chosen by hand after the fitted one proved too
    tight (R-374). The energy calibration is not touched.
    """
    # NaN fails both comparisons, so it is refused here with the infinities.
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
        raise refuse(
            "vocal-cut-out-of-range",
            f"a with vox cut of {cut} is outside the presence score's range, "
            f"{VOCAL_SCORE_MIN:g} to {VOCAL_SCORE_MAX:g}, so nothing was written",
            steps=(
                f"give a cut from {VOCAL_SCORE_MIN:g} to {VOCAL_SCORE_MAX:g}, the "
                f"percentage of a track the model hears singing in",
            ),
            origin=_ORIGIN,
            detail={"cut": str(cut)},
        )
    _require_library_root(cfg)
    previous, before = _previous_vocal_cut(cfg)
    today = _today()
    target = _write_vocal_calibration(
        cfg, cut, method=VOCAL_METHOD_HAND, note=f"set by hand on {today}", set_on=today
    )
    return ctx.envelope(
        data={
            "checks": [
                _check(
                    "calibrate.vocals",
                    "vocal cut",
                    "ok",
                    f"cut set by hand at {cut:g}, written to {target}; {before}; "
                    f"the energy calibration was not touched",
                    None,
                )
            ],
            "summary": {"folder": None, "vocal_cut": cut, "previous_vocal_cut": previous},
        },
        outcome=Outcome.OK,
    )


def _require_library_root(cfg: config.Config) -> None:
    """Refuse to write a library scoped state file with the library away.

    The atomic writer creates the directories on the way, so with the volume
    unmounted a calibration would land on the boot disk under the mount
    point. This is the ``library.mounted`` check the registry declares.
    """
    root = Path(cfg.library.root)
    if root.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",
        f"the library root {root} is not a directory on this machine, so the "
        f"calibration has nowhere to be written; nothing was measured",
        steps=("mount the library volume and run the calibration again",),
        origin=_ORIGIN,
        detail={"library": str(root)},
    )


def _is_library_wide(cfg: config.Config, folder: Path) -> bool:
    """Whether ``folder`` holds the WHOLE library: the root or its music folder.

    Every module places tracks under ``root / music_dir``, so that folder is
    the library as much as the root is. ``samefile`` rather than spellings,
    because a library volume is case insensitive and often reached through a
    link. Both candidates are effective config values (P2). A candidate that
    cannot be statted is not this folder, so the check refuses.
    """
    root = Path(cfg.library.root)
    for candidate in (root, root / cfg.library.music_dir):
        try:
            if os.path.samefile(folder, candidate):
                return True
        except OSError:
            continue
    return False


def _sample_row(status: str, detail: str, remedy: Remedy | None) -> dict[str, str | None]:
    return _check("calibrate.sample", "calibration sample", status, detail, remedy)


def _partial_before_walk(
    cfg: config.Config, folder: Path, *, recursive: bool
) -> tuple[str, str] | None:
    """Why this walk cannot be the library, known BEFORE it, as (what, fix), or None.

    One ``samefile`` and no walk, so nobody waits on a library wide stat to
    hear the folder was wrong. One level of the library is only its loose
    files, and a recursive walk of one genre is still one genre.
    """
    wide = _is_library_wide(cfg, folder)
    if wide and recursive:
        return None
    if wide:
        return (
            f"{folder} holds the whole library but was read one level deep, so "
            f"only the tracks loose in it would be fitted",
            "add --recursive to walk the whole library",
        )
    root = Path(cfg.library.root)
    return (
        f"{folder} is not the library root {root} or the music folder under it, "
        f"so a fit over it describes that folder and not the library",
        f"run `crate analyze calibrate {root} --recursive` for the whole library",
    )


def _partial_after_walk(scan: jobs.Scan) -> tuple[str, str] | None:
    """Why this walk was not the library, known only AFTER it, or None.

    A linked genre folder is declined and an unlistable one contributes
    nothing, so the fit would be over a library missing a genre (U94).
    """
    left_out = len(scan.skipped_links) + len(scan.unreadable)
    if not left_out:
        return None
    return (
        f"the walk left out {left_out} folder{'' if left_out == 1 else 's'} it "
        f"could not or would not enter, named in the warnings, so the fit would "
        f"be over a library missing whatever they hold",
        "replace a linked folder with the folder itself and fix the permissions "
        "on an unreadable one, then run it again",
    )


def _partial_refused(partial: tuple[str, str]) -> dict[str, str | None]:
    what, fix = partial
    return _sample_row(
        "failed",
        f"{what}; nothing was measured and nothing was written. {fix}, or give "
        f"--accept-partial to fit over what was walked anyway",
        Remedy.FIX_COMMAND_LINE,
    )


def _partial_accepted(partial: tuple[str, str]) -> dict[str, str | None]:
    """NOT ``ok``. An accepted partial must not read as the library wide fit."""
    what, fix = partial
    return _sample_row(
        "skipped",
        f"{what}; fitted anyway because --accept-partial was given. {fix}",
        Remedy.FIX_COMMAND_LINE,
    )


def _partial_warning(folder: Path) -> dict[str, str]:
    return {
        "code": PARTIAL_SAMPLE,
        "message": (
            f"what was written was fitted over part of the library, the walk of "
            f"{folder}, so every level and every with vox tag scored against it "
            f"is on that part's scale"
        ),
    }


def _calibrate_refusal(ctx, check: dict[str, str | None], summary: Mapping[str, Any], warnings=()):
    return ctx.envelope(
        data={"checks": [check], "summary": dict(summary)},
        outcome=Outcome.NO_OP,
        warnings=tuple(warnings),
    )


def analyze_calibrate(ctx) -> Envelope:
    """Fit this library's energy reference and vocal cut over a library wide sample.

    THE ``calibrate.sample`` CHECK (U94): a fit over one genre folder is wrong
    in a way nobody can see, so the check fails, measuring and writing
    nothing, unless the walk is the library. ``--accept-partial`` is the
    person saying they know, and the answer says it back on the check, the
    envelope and the file's note. The flag does not waive the sample floor.

    CHEAPEST REFUSAL FIRST: the floor and the folder's standing are answered
    before the walk, which is a stat per file.

    SYNCHRONOUS AND BOUNDED, NOT A JOB: the energy half measures a stride
    sample, the vocal half reads a tag per file, and each half writes once at
    its end, so a killed calibrate wrote nothing.
    """
    cfg = load_config(("analysis.cli",))
    if ctx.args.vocal_cut is not None:
        return _set_vocal_cut(ctx, cfg, ctx.args.vocal_cut)
    if not ctx.args.folder:
        return _calibrate_refusal(
            ctx,
            _check(
                "calibrate.folder",
                "calibration folder",
                "skipped",
                "no folder given, so nothing was measured and nothing was written",
                Remedy.FIX_COMMAND_LINE,
            ),
            {"folder": None, "calibrated": False},
        )
    folder = _folder_of(ctx.args.folder)
    recursive = bool(ctx.args.recursive)
    sample = int(ctx.args.sample)
    accepted = bool(ctx.args.accept_partial)
    summary: dict[str, Any] = {"folder": str(folder), "calibrated": False}
    if not folder.is_dir():
        return _calibrate_refusal(
            ctx,
            _check(
                "calibrate.folder",
                "calibration folder",
                "failed",
                f"{folder} is not a folder on this machine, so nothing was measured",
                Remedy.FIX_COMMAND_LINE,
            ),
            summary,
        )
    if sample < MIN_CALIBRATION_TRACKS:
        return _calibrate_refusal(
            ctx,
            _sample_row(
                "failed",
                f"a sample of {sample} is below the {MIN_CALIBRATION_TRACKS} "
                f"tracks a calibration needs, so nothing was measured and nothing "
                f"was written; give --sample {MIN_CALIBRATION_TRACKS} or more",
                Remedy.FIX_COMMAND_LINE,
            ),
            summary,
        )
    # BEFORE THE FOLDER'S STANDING: with the volume away no folder is the
    # root, and the answer would blame the folder for it.
    _require_library_root(cfg)
    partial = _partial_before_walk(cfg, folder, recursive=recursive)
    if partial is not None and not accepted:
        return _calibrate_refusal(ctx, _partial_refused(partial), summary)

    scan = jobs.scan_audio(folder, recursive=recursive)
    # SAID ON EVERY ANSWER BELOW, the empty one included.
    omitted = jobs.walk_warnings(scan.skipped_links, scan.unreadable, verb="read")
    paths = [jobs.item_path(folder, item) for item in scan.items]
    summary.update({"tracks": len(paths), "recursive": recursive})
    if not paths:
        return _calibrate_refusal(
            ctx,
            _check(
                "calibrate.folder",
                "calibration folder",
                "failed",
                f"{folder} holds no audio files, so nothing was measured",
                Remedy.FIX_COMMAND_LINE,
            ),
            {"folder": str(folder), "calibrated": False},
            omitted,
        )
    left_out = len(scan.skipped_links) + len(scan.unreadable)
    if partial is None:
        partial = _partial_after_walk(scan)
        if partial is not None and not accepted:
            return _calibrate_refusal(ctx, _partial_refused(partial), summary, omitted)
    _require_heavy(energy.extractor_bound(), "measuring a folder's energy")

    sampled = stride_sample(paths, sample)
    checks = [
        _sample_row(
            "ok",
            f"{folder} holds the whole library and was walked recursively with "
            f"nothing left out, so the fit is over the library's own distribution",
            None,
        )
        if partial is None
        else _partial_accepted(partial),
        _calibrate_energy(cfg, folder, sampled, len(paths), left_out),
        _calibrate_vocals(cfg, folder, paths, left_out),
    ]
    calibrated = checks[1]["status"] == "ok"
    wrote = any(check["status"] == "ok" for check in checks[1:])
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {**summary, "calibrated": calibrated, "sampled": len(sampled)},
        },
        # OK WHEN EITHER HALF WROTE, or a run that replaced the with vox cut
        # would tell a machine reader nothing changed (U94). The summary's
        # ``calibrated`` stays the energy half's, which is what it names.
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
        # ONLY WHEN SOMETHING WAS WRITTEN: the warning speaks of what was.
        warnings=((_partial_warning(folder),) if partial is not None and wrote else ())
        + tuple(omitted),
    )
