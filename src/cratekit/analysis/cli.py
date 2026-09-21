"""``crate analyze``: queue the heavy passes, never run them inline.

Long work is a job (KTD26, R22). The shell freezes the folder and the
item list. A killed driver resumes by trusting DONE rows and the
Camelot-prefixed names those rows left behind.

THE TWO WORKERS LIVE HERE (U58). ``handle_run`` analyses one file and
finalizes it, ``handle_restamp`` rescores one file's energy against the
active calibration, and :mod:`cratekit.cli.handlers` binds them under
``analyze.run`` and ``analyze.restamp``. Each reads its subject from the
ITEM, never from the payload, because a handler that reads its subject from
the payload does the same work for every item of a multi item job.

THE ITEM IS A PATH RELATIVE TO THE FROZEN FOLDER, AND THE FOLDER IS FROZEN
ABSOLUTE. The first version queued absolute paths, which made the frozen
folder a second copy of a fact every item already carried. The folder is
resolved before it is frozen because ``jobs.spawn`` starts the resume child
in the RESUMING process's working directory, not the queueing one's, so a
relative folder would make every item of a resumed job go missing.

``analyze restamp --recursive`` (U93) makes that relative path more than one
segment. ``analyze run`` does NOT take the flag: its last act on a track is a
rename, and its resume marker is the Camelot head on the NAME, so its item
identity is bound to the filename in a way a tree walk would not survive.
``core.discovery`` owns the walk and the join for both verbs.

THE SEAMS ARE BOUND AT CALL TIME. The detector, the vocal model loader, the
decoder and the feature extractor are each module state the worker looks up
when it runs, so a test binds a fake and the whole path runs without the
extra installed. A worker in a fresh process finds nothing bound and binds
the shipped defaults, every one of which imports the heavy stack lazily
inside a function. R-226's limit applies: the child ``crate job resume``
spawns inherits nothing a test patched.

THE MODEL MODULE IS NEVER IMPORTED AT MODULE SCOPE HERE. ``cli.jobs.argv_for``
imports this module by name to build a resume command line, and the model
module imports numpy at import time, which the slim profile does not
declare. A worker binds it inside the function that needs it.
"""

from __future__ import annotations

import functools
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence, TypeVar

from cratekit.analysis import artifacts, detect, energy, light, vocals
from cratekit.cli.output import Envelope
from cratekit.core import config, discovery, jobs, naming, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import MarkerRule, NameBudget, NameSpec, NameTemplate
from cratekit.modules import extras

_ORIGIN = ("analysis", "cli")
_T = TypeVar("_T")

#: The vocal cut is stored beside the energy calibration, in the state file
#: ``core.config`` declares for it. Read by whoever routes with vox; the
#: threshold is PASSED to the router, never imported by it (D7).
STATE_KEY_VOCAL_CALIBRATION = "vocal_calibration"
#: The fallback cut when a folder has too few scored tracks for Otsu to split.
DEFAULT_VOCAL_THRESHOLD = 12.0
#: The presence score's range, the percentage of frames the vocal model hears
#: singing in (``vocal.presence_score``). A cut is a point on this scale, so a
#: cut set by hand outside it is refused (U90).
VOCAL_SCORE_MIN = 0.0
VOCAL_SCORE_MAX = 100.0
#: The ``method`` a cut set by hand is recorded under, beside the fit's "otsu".
VOCAL_METHOD_HAND = "hand"
#: How far apart the two clusters' means must sit for a cut between them to
#: mean anything. An all instrumental folder is one cluster, and Otsu will
#: still split it down the middle and call half of it vocal.
MIN_VOCAL_SEPARATION = 10.0
#: How many measured tracks a calibration needs before its deciles mean anything.
MIN_CALIBRATION_TRACKS = 10
#: How many tracks the energy fit measures unless ``--sample`` says otherwise
#: (U94). Justified on the fit and not on a fixture: the tightest statistic
#: ``energy.calibrate`` takes is ``energy.ONSET_FLOOR_PERCENTILE``, the second
#: percentile, and at 500 tracks that percentile rests on ten tracks beneath it,
#: the count ``MIN_CALIBRATION_TRACKS`` demands of a whole fit, while each of
#: the ten level bins holds fifty. What a measured track costs in seconds on a
#: real library was NOT measured here and is owed to an attended sitting.
DEFAULT_CALIBRATION_SAMPLE = 500

#: The warning a calibration carries when it was fitted over something other
#: than the library wide walk because ``--accept-partial`` said to (U94).
PARTIAL_SAMPLE = "calibration-partial-sample"

#: The warning every restamp resume carries, because the registry declares a
#: database write this build does not perform. See ``handle_restamp``.
DB_NOT_WRITTEN = {
    "code": "db-metadata-not-written",
    "message": (
        "this restamp wrote the energylevel file tag only; the rekordbox star "
        "rating half the verb declares is not written by this build"
    ),
}


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("analysis.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


# ---------------------------------------------------------------------------
# Reporting, the job_state/1 surface
# ---------------------------------------------------------------------------


def _reported(store, job, extra: Mapping[str, Any] | None = None) -> dict:
    """One job as the ``job_state`` payload. ``extra`` rides UNDER ``progress``.

    Both queued verbs declare ``job_state/1`` and ``cli.output`` closes that
    surface, so a per verb detail at the top level is an undeclared field.
    """
    progress = dict(jobs.progress(store, job.job_id))
    if extra:
        progress.update(extra)
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": progress,
    }


def _no_op(state: str) -> dict:
    """The honest zero: a folder with nothing to analyse queues nothing.

    ``job_id`` is the empty string rather than null, because the declared
    surface types it as a string (R-234). Queueing a job with no items would
    drive straight to SUCCEEDED over work nothing did.
    """
    return {"job_id": "", "state": state, "cause": None, "progress": {}}


def _folder_of(named: str) -> Path:
    return Path(named).expanduser().absolute()


def _audio_in(folder: Path) -> list[str]:
    """The item identifiers: audio FILENAMES in the folder, sorted, not recursive.

    The one level reading, which is what ``analyze run`` takes. ``analyze
    calibrate`` took it too until U94 and now asks ``core.discovery`` for the
    walk itself, because it has to say what the walk left out. NO DOTFILES: macOS writes an AppleDouble sidecar,
    ``._track.flac``, beside every file on an exFAT or FAT volume, which is what
    a DJ stick is, and the sidecar carries the audio suffix. Queued as an item it
    is decoded, refused as undecodable, and then, because the finder moves the
    sidecar with the file it shadows when the track is renamed, refused as
    missing on the next claim and the job fails. ``write/routing_cli.py`` skips
    the same names. The rule itself lives in ``core.discovery``, because
    ``analyze vocals`` needs the same one and two copies of a rule that has to
    agree do not stay agreed.
    """
    return list(discovery.scan_audio(folder).items)


def _nothing_to_queue(ctx, folder: Path, extra: tuple[dict[str, str], ...] = ()) -> Envelope:
    """The two zeros, told apart: an empty folder and a folder that is not there.

    A mistyped path or an unmounted volume must not read as "nothing new to
    analyse", which is what one shared no-op would say. The tagging verbs make
    the same split.

    ``extra`` carries the recursive walk's declined links onto the zero as well
    as onto the queue, because "nothing to do" over a tree whose every folder is
    a link is the one place the omission changes the answer completely.
    """
    if folder.is_dir():
        return ctx.envelope(data=_no_op("no-audio"), outcome=Outcome.NO_OP, warnings=extra)
    return ctx.envelope(
        data=_no_op("folder-absent"),
        outcome=Outcome.NO_OP,
        warnings=(
            {
                "code": "folder-absent",
                "message": f"{folder} is not a folder on this machine, so nothing was queued",
            },
            *extra,
        ),
    )


def _summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
    """What the committed reports say the job did, read back off disk."""
    reports = artifacts.committed(cfg, job_id)
    statuses: dict[str, int] = {}
    reasons: dict[str, int] = {}
    for report in reports:
        status = str(report.get("status", "unknown"))
        statuses[status] = statuses.get(status, 0) + 1
        reason = report.get("vocal_reason")
        if reason is not None:
            reasons[str(reason)] = reasons.get(str(reason), 0) + 1
    return {"reports": len(reports), "by_status": statuses, "by_vocal_reason": reasons}


def _unscored_vocals_warning(summary: Mapping[str, Any]) -> dict[str, str] | None:
    """The warning a run carries when the model was never there to score.

    The registry declares the ``analysis`` extra for ``analyze.run`` and the
    model lives behind the separate ``vocals`` extra, so a machine with the
    declared extra and not the other finalizes every track with no vocal tags
    while the job reports plain success. The absence is in every item report
    and this is what lifts it to the envelope, the way the restamp lifts its
    unwritten database half.
    """
    return vocals.unscored_warning(summary, verb="analysed")


# ---------------------------------------------------------------------------
# The parser
# ---------------------------------------------------------------------------


def build(parser, entry) -> None:
    parser.add_argument("folder", help="folder of audio to analyse")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the analysis job already queued under this identifier",
    )
    parser.set_defaults(_handler=analyze_run)


def build_calibrate(parser, entry) -> None:
    # One or the other, because a folder fits the vocal cut and the flag sets
    # it, and both in one call would leave the person guessing which one won.
    chosen = parser.add_mutually_exclusive_group()
    chosen.add_argument(
        "folder", nargs="?", default=None, help="folder whose tracks fit the calibration"
    )
    chosen.add_argument(
        "--vocal-cut",
        type=float,
        default=None,
        metavar="CUT",
        help=(
            "set the with vox cut by hand, a presence score from 0 to 100, "
            "instead of fitting one; the energy calibration is left alone"
        ),
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help=(
            "walk every folder under this one; given the library root, this is "
            "the library wide walk a calibration is fitted over"
        ),
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=DEFAULT_CALIBRATION_SAMPLE,
        metavar="N",
        help=(
            "measure at most N tracks for the energy fit, taken at an even "
            "stride over the sorted walk so the same tree gives the same sample "
            f"(default {DEFAULT_CALIBRATION_SAMPLE}); the vocal cut always reads "
            "every tagged track"
        ),
    )
    parser.add_argument(
        "--accept-partial",
        action="store_true",
        help=(
            "write a calibration fitted over something other than the whole "
            "library, a single genre folder for instance, knowing its numbers "
            "describe that folder rather than the library"
        ),
    )
    parser.set_defaults(_handler=analyze_calibrate)


def build_validate(parser, entry) -> None:
    parser.add_argument(
        "folder", nargs="?", default=None, help="labelled folder to score against"
    )
    parser.set_defaults(_handler=analyze_validate)


def build_restamp(parser, entry) -> None:
    parser.add_argument("folder", help="folder whose analysed values should be restamped")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help=(
            "queue every folder under this one as a single resumable job, "
            "instead of only the tracks directly inside it"
        ),
    )
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the restamp job already queued under this identifier",
    )
    parser.set_defaults(_handler=analyze_restamp)


def analyze_argv(job) -> list[str]:
    folder = job.payload.get("folder", "")
    return ["analyze", "run", folder, "--job", job.job_id]


def restamp_argv(job) -> list[str]:
    folder = job.payload.get("folder", "")
    return ["analyze", "restamp", folder, "--job", job.job_id]


# ---------------------------------------------------------------------------
# The resume, shared by both queued verbs
# ---------------------------------------------------------------------------


def _advance(ctx, store, job):
    """Reconcile, refuse an empty job, run it, and raise if it did not finish.

    The tail every queued verb carries (R-248, this is another copy). Not
    named ``drive``, because ``tests/test_handlers.py`` counts every call to
    a callee of that name as a call to the job driver.
    """
    job = jobs.reconcile(store, job.job_id)
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no items to run, so driving it would report "
                f"an analysis over a folder it never read. It was queued by a build "
                f"that did not record what its items were",
                remedy=Remedy.REPORT_DEFECT,
                origin=_ORIGIN,
                detail={"job_id": job.job_id},
            )
        _result, warnings = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
    jobs.raise_for_state(job)
    return job, warnings


def _resume(ctx, cfg: config.Config) -> Envelope:
    with jobs.open_store() as store:
        job, warnings = _advance(ctx, store, jobs.get(store, ctx.args.job))
        summary = _summary(cfg, job.job_id)
        # THE RESUME IS THE REPORT THAT SAYS THE PASS FINISHED, so what the walk
        # left out rides it too, read back off the frozen payload rather than
        # re-measured. A queue envelope alone would put the omission on the
        # cheaper of the two commands and leave the one a person keeps silent.
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        if job.handler_key == "analyze.restamp":
            warnings = (*warnings, DB_NOT_WRITTEN)
        else:
            unscored = _unscored_vocals_warning(summary)
            if unscored is not None:
                warnings = (*warnings, unscored)
        return ctx.envelope(
            data=_reported(store, job, {"analysis": summary}),
            warnings=warnings,
        )


# ---------------------------------------------------------------------------
# ``crate analyze run``
# ---------------------------------------------------------------------------


def analyze_run(ctx) -> Envelope:
    cfg = _load()
    if ctx.args.job:
        return _resume(ctx, cfg)
    folder = _folder_of(ctx.args.folder)
    items = _audio_in(folder)
    if not items:
        return _nothing_to_queue(ctx, folder)
    # A CORRUPT CALIBRATION REFUSES AT THE QUEUE, as the restamp does. A run
    # needs no calibration, an absent one is an honest uncalibrated level, but
    # an unreadable one would fail every item on the same file after every
    # track had been opened, and the remedy is the same command either way.
    energy.load_calibration(cfg)
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            cfg=cfg,
            item_ids=items,
        )
        return ctx.envelope(data=_reported(store, job))


def _template(cfg: config.Config) -> NameTemplate:
    return NameTemplate(
        markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),)
    )


def _budget(cfg: config.Config) -> NameBudget:
    return NameBudget(
        path_budget_bytes=cfg.naming.path_budget_bytes,
        filename_max_bytes=cfg.naming.filename_max_bytes,
    )


def _refuse_missing(item, folder: Path, path: Path, what: str) -> CratekitError:
    return refuse(
        "source-missing",
        f"{path} is no longer a file, so there is nothing to {what} for this "
        f"item. Nothing was read and nothing was written",
        steps=(
            "run the analysis verb again over the folder as it now stands; "
            "this job was queued against a folder that has since changed",
        ),
        origin=_ORIGIN,
        detail={"item": item.item_id, "folder": str(folder)},
    )


def _folder_and_path(job, item) -> tuple[Path, Path]:
    """The frozen folder and the item's path in it, the one rule both workers use.

    Through ``core.discovery.item_path``, which refuses an id that would leave
    the folder. Since U93 an id may carry separators, and a plain join with an
    absolute right hand side discards the base without saying so.
    """
    folder = Path(str((job.payload or {}).get("folder") or ""))
    return folder, discovery.item_path(folder, str(item.item_id))


def _item_path(job, item, what: str) -> Path:
    folder, path = _folder_and_path(job, item)
    if not path.is_file():
        raise _refuse_missing(item, folder, path, what)
    return path


def _finalized_twin(cfg: config.Config, job, item) -> Path | None:
    """The file this item became, if a finalize renamed it before its row moved.

    The item is the PRE-rename name and the rename lands inside the handler,
    before the engine flips the row to done. A kill in that window leaves a
    finished file under its head and a pending row under its old name, and
    the resume would otherwise refuse the item as missing over work that is
    complete on disk.

    THE ANSWER COMES FROM THE RENAME INTENT THIS ITEM'S OWN ATTEMPT WROTE,
    never from a scan of the folder. The first version matched any headed
    file whose stripped stem equalled the item, which reported a deleted
    source as analysed when an older twin of it sat in the folder, and found
    nothing when the template had deduped or truncated the stem.
    """
    target = artifacts.rename_intent(cfg, job, item)
    if target is None or not target.is_file():
        return None
    return target


def _require_heavy(seam_bound: bool, what: str) -> None:
    """Refuse the item when the extra is absent HERE and no fake is bound.

    The detector answers a missing extra with None, so without this a job on
    a machine with no librosa would skip every file as keyless and report
    done.
    """
    if seam_bound or detect.heavy_available():
        return
    # THE SAME REMEDY THE PARSER STUB RENDERS FOR THIS SLUG. The first version
    # said report a defect, so the same absence read as an installation gap
    # at the parser and as a bug in the worker.
    raise refuse(
        "module-extras-missing",
        f"{what} needs the 'analysis' extra, and it is not installed in the "
        f"process running this job",
        remedy=Remedy.INSTALL_MODULE_EXTRA,
        origin=_ORIGIN,
        detail={"extras": "analysis", "install": extras.install_command("analysis")},
    )


#: The detector THIS module bound, so it can tell its own binding from a
#: test's and rebind with a fresh calibration on every item.
_BOUND_DETECT: Any = None


def _fake_detect_bound() -> bool:
    return light.bound() and light._DETECT is not _BOUND_DETECT


def _bind_defaults(cfg: config.Config) -> None:
    """Bind the shipped seams where nothing else is bound, PER ITEM.

    The detector is rebound on every call rather than once per process,
    because the partial carries the calibration, and a calibration written
    between two jobs driven by one process would otherwise stay invisible to
    the second. A test's binding is left alone.
    """
    global _BOUND_DETECT
    if not _fake_detect_bound():
        _BOUND_DETECT = functools.partial(
            detect.analyse_file, calibration=energy.load_calibration(cfg)
        )
        light.bind_detect(_BOUND_DETECT)
    if not vocals.loader_bound():
        from cratekit.analysis import vocal

        vocals.bind_loader(vocal.default_loader)


def _write_or_refuse(path: Path, fields: dict[str, Any], *, untouched: str) -> None:
    """A tag write that did not land refuses under the analysis slug.

    ``write_tags`` returns False for a file it could not write and RAISES
    ``UnsupportedContainer`` for a container it does not know, and
    ``AUDIO_EXTS`` is wider than the containers it knows, so both shapes are
    one refusal here rather than one refusal and one defect report. ONLY THAT
    SUBCLASS is caught: the writer raises a plain ``ValueError`` for a field
    the tag table does not know, which is the beat grid enforcement point
    (R17), and that is a defect in this module that must stay loud rather
    than read as a folder of awkward files.
    """
    try:
        written = tags.write_tags(path, fields)
    except tags.UnsupportedContainer as exc:
        raise refuse(
            "analysis-write-failed",
            f"the analysed values cannot be written onto {path.name}: {exc}. {untouched}",
            origin=_ORIGIN,
            detail={"path": str(path), "stage": "tags", "kind": type(exc).__name__},
        ) from exc
    if not written:
        raise refuse(
            "analysis-write-failed",
            f"the analysed values could not be written onto {path.name}. {untouched}",
            origin=_ORIGIN,
            detail={"path": str(path), "stage": "tags"},
        )


def _finalize(cfg: config.Config, job, item, path: Path, scored: Mapping[str, Any]) -> Path:
    """Write the analysed values onto the file and rename it to its head.

    TAGS FIRST, THEN THE RENAME, the source system's order: a kill between the
    two leaves the head in the title and not in the filename, and the naming
    module's ``normalize_spec`` heals exactly that window on the next pass.

    THE INTENT BEFORE THE RENAME. The target name is recorded in the item's
    staging directory before the file moves, so a kill between the rename and
    the row flipping to done leaves a resume something exact to read.

    NO ENERGY TAG FOR AN ABSENT LEVEL. ``write_tags`` skips None, so an
    uncalibrated library's files carry no ``energylevel``, and the routing
    pass reads that absence as the taxonomy's no-energy sink rather than as a
    level. Same for an unscored vocal pass.
    """
    template = _template(cfg)
    camelot = str(scored["camelot"])
    key = naming.pad_camelot(camelot)
    # ``rate`` is the shipped detector's key and ``bpm`` the shape the older
    # batch fakes use; ``run._as_result`` accepts both and so does this.
    tempo = scored.get("rate", scored.get("bpm"))
    title = tags.read_tag(path, "title") or ""
    marker = cfg.naming.lossy_marker
    spec = NameSpec(
        stem=path.stem,
        suffix=path.suffix,
        key=key,
        bpm=int(tempo),
        title=naming.strip_head(title, template=template) if title else None,
        lossy=bool(marker) and (marker in path.stem or marker in title),
    )
    rendered = naming.build(
        spec, template=template, budget=_budget(cfg), parent_dir=str(path.parent)
    )
    fields = {
        "initialkey": key,
        "title": rendered.title_tag,
        "energylevel": scored.get("energy"),
        "voxlevel": scored.get("voxlevel"),
        "voxgender": scored.get("voxgender"),
        "voxgenderconf": scored.get("voxgenderconf"),
    }
    _write_or_refuse(path, fields, untouched="The file is untouched and was not renamed")
    target = path.with_name(rendered.filename)
    if target == path:
        return path
    artifacts.record_rename_intent(cfg, job, item, target)
    if not naming.claim_target(target):
        raise refuse(
            "analysis-write-failed",
            f"{path.name} could not be renamed to {rendered.filename}: that name "
            f"is already taken in the folder. The tags were written and the "
            f"title carries the head, so the next pass converges",
            origin=_ORIGIN,
            detail={"path": str(path), "target": str(target), "stage": "rename"},
        )
    try:
        path.rename(target)
    except OSError as exc:
        target.unlink(missing_ok=True)
        raise refuse(
            "analysis-write-failed",
            f"{path.name} could not be renamed to {rendered.filename}: {exc}",
            origin=_ORIGIN,
            detail={"path": str(path), "target": str(target), "stage": "rename"},
        ) from exc
    return target


def handle_run(job, item, cfg) -> jobs.Produced:
    """Analyse ONE file. The per item worker behind ``analyze.run``.

    A name already carrying the head is the resume marker and is skipped
    without a read. Otherwise the light head runs, then the vocal score, then
    the finalize. A head that found no key, or could not decode the file, is
    a terminal skip, reported under its own name with nothing written. THE
    CONFIGURATION IS THE FROZEN ONE and is not loaded here (KTD9).
    """
    template = _template(cfg)
    folder, path = _folder_and_path(job, item)
    if not path.is_file():
        twin = _finalized_twin(cfg, job, item)
        if twin is None:
            raise _refuse_missing(item, folder, path, "analyse")
        return artifacts.produced(
            cfg,
            job,
            item,
            {
                "item": item.item_id,
                "path": str(twin),
                "status": "skipped-prefixed",
                "resumed_after_rename": True,
            },
        )
    if naming.has_head(path.name, template=template):
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": "skipped-prefixed"}
        )
    _require_heavy(_fake_detect_bound(), "analysing a track")
    _bind_defaults(cfg)
    partial = light.analyse(str(path))
    if partial.get("terminal") is not None:
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": partial["terminal"]}
        )
    scored = vocals.analyse(partial)
    final = _finalize(cfg, job, item, path, scored)
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "item": item.item_id,
            "path": str(final),
            "renamed_to": final.name if final != path else None,
            "status": "analyzed",
            "camelot": scored["camelot"],
            "tempo": int(scored.get("rate", scored.get("bpm"))),
            "energy": scored.get("energy"),
            "energy_status": scored.get("energy_status"),
            "vocal_active": bool(scored.get("vocal_active")),
            "vocal_reason": scored.get("vocal_reason"),
            "voxlevel": scored.get("voxlevel"),
            "voxgender": scored.get("voxgender"),
        },
    )


# ---------------------------------------------------------------------------
# ``crate analyze restamp``
# ---------------------------------------------------------------------------


def _as_level(text: str | None) -> int | None:
    """The integer a tag text carries, or None, ``tags._read_int``'s reading."""
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _calibration_or_refuse(cfg: config.Config) -> energy.Calibration:
    calibration = energy.load_calibration(cfg)
    if calibration is None:
        raise refuse(
            "energy-calibration-missing",
            "this library has no energy calibration, so there is no scale to "
            "restamp onto",
            steps=(
                "run `crate analyze calibrate LIBRARY_ROOT --recursive` first, which "
                "fits over a sample of the whole library",
            ),
            origin=_ORIGIN,
            detail={"calibration": str(energy.calibration_path(cfg))},
        )
    return calibration


def analyze_restamp(ctx) -> Envelope:
    cfg = _load()
    if ctx.args.job:
        return _resume(ctx, cfg)
    folder = _folder_of(ctx.args.folder)
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=recursive)
    extra = discovery.walk_warnings(scan.skipped_links, scan.unreadable)
    if not scan.items:
        # BEFORE THE CALIBRATION CHECK: a folder with nothing to restamp is a
        # complete answer whether or not the library is calibrated.
        return _nothing_to_queue(ctx, folder, extra)
    # REFUSED AT THE QUEUE, not only in the worker: a job whose every item
    # would fail on the same absence is a report over work nothing could do.
    _calibration_or_refuse(cfg)
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            # FROZEN WITH THE FOLDER, because a resume must not be able to
            # disagree with the queue about what the item list meant, and
            # because the resume is the report that says the pass finished.
            # The resume never re-scans: it would be measuring the tree as it
            # is now over a job queued against the tree as it was.
            payload={"folder": str(folder), **discovery.frozen_walk(scan, recursive=recursive)},
            cfg=cfg,
            item_ids=list(scan.items),
        )
        return ctx.envelope(
            data=_reported(store, job), warnings=(DB_NOT_WRITTEN, *extra)
        )


def handle_restamp(job, item, cfg) -> jobs.Produced:
    """Rescore ONE file's energy against the active calibration and stamp it.

    THE PREVIOUS VALUE IS RECORDED BEFORE THE WRITE, once per file, as the tag
    TEXT the file carried, in the undo log ``core.config`` declares as the
    only surviving copy of it. A file whose level did not move is reported
    unchanged and not rewritten. A write that then fails leaves a log entry
    for a file still carrying exactly that value, which is a true record.

    FILE TAG ONLY. The registry declares ``db_metadata`` for this verb too,
    after the source system's separate re-rate step; that half is not written
    by this build, every report says ``db_written: false``, and the resume
    envelope carries the warning. The residual is recorded with U58.
    """
    path = _item_path(job, item, "restamp")
    calibration = _calibration_or_refuse(cfg)
    _require_heavy(energy.extractor_bound(), "measuring a track's energy")
    features = energy.measure(path)
    # ONE READ OF THE TAG. The text is what the undo log records and the
    # integer is what the comparison uses, and they come from one open so
    # the two cannot disagree about what the file carried.
    previous_text = tags.read_tag(path, "energylevel")
    previous = _as_level(previous_text)
    if features is None:
        return artifacts.produced(
            cfg,
            job,
            item,
            {
                "item": item.item_id,
                "path": str(path),
                "status": energy.STATUS_FEATURES_UNAVAILABLE,
                "previous": previous,
                "level": None,
                "written": False,
                "db_written": False,
            },
        )
    level = energy.level_for(features, calibration)
    energy.record_previous(cfg, path, previous_text)
    written = False
    if previous != level:
        _write_or_refuse(path, {"energylevel": level}, untouched="The file is untouched")
        written = True
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "item": item.item_id,
            "path": str(path),
            "status": "restamped" if written else "unchanged",
            "previous": previous,
            "level": level,
            "written": written,
            "db_written": False,
        },
    )


# ---------------------------------------------------------------------------
# ``crate analyze calibrate`` and ``crate analyze validate``
# ---------------------------------------------------------------------------


def _check(
    key: str, title: str, status: str, detail: str, remedy: Remedy | None
) -> dict[str, str | None]:
    """One diagnostic check, the doctor's shape. An ok check carries no remedy."""
    return {
        "key": key,
        "title": title,
        "status": status,
        "detail": detail,
        "remedy": str(remedy) if remedy is not None else None,
    }


def otsu_threshold(scores: list[float], *, bins: int = 100) -> float:
    """The cut that best separates two clusters of presence scores (0 to 100).

    Maximizes the between-class variance over a histogram of the scores. A
    vocal library is bimodal on presence, instrumentals near zero and vocal
    tracks well above, and this is the unsupervised cut between them. Whether
    the input HAS two clusters is the caller's question, answered by
    :func:`cluster_separation`.
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

    None when one side is empty, which is a cut with nothing on one side of
    it rather than a cut between two things.
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

    DETERMINISTIC ON PURPOSE (U94). A random sample would make two calibrations
    of one unchanged library disagree, and the numbers a calibration writes are
    ones nobody can check by eye, so the only evidence a person has that nothing
    moved is that the same tree gives the same fit. The caller hands in the
    SORTED walk, and a genre folder is a contiguous run of a sorted walk, so an
    even stride takes from every folder in proportion to its size, where the
    first ``count`` items would be the first few folders of the alphabet.

    ``index * len // count`` and not a fixed step, because a fixed step of
    ``len // count`` stops short of the end whenever the division has a
    remainder, and the tail it never reaches is again whole folders. With more
    items than ``count`` the indices are strictly increasing, so nothing is
    taken twice.
    """
    total = len(items)
    if count <= 0:
        return []
    if total <= count:
        return list(items)
    return [items[index * total // count] for index in range(count)]


def fitted_note(fitted: int, walked: int, folder: Path, left_out: int = 0) -> str:
    """The provenance a calibration file records about itself (U94).

    Both halves write it, each with its own count, and ``_previous_vocal_cut``
    reads it back into the next run's report, so the sentence a person sees for
    "this replaces" names how much of what the old number was fitted over.

    ``left_out`` is how many folders the walk declined or could not list. An
    envelope warning is gone when the terminal scrolls, and the file is what a
    later restamp trusts, so a fit over a tree missing folders says so in the
    one place that outlives the run.
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
        # The energy half is already written by now, so a refusal raised from
        # here would report the whole verb as failed over a write that
        # happened. The vocal half fails in its own check instead (U90, driven).
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

    Atomic through ``energy.write_json``, so a reader meets the old file or the
    new one and never half of either. Neither path fits a gender margin, so
    both record the model's default. The reader is
    ``write.metadata_cli.load_vocal_calibration``, and nothing else reads it.
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

    Read through the one reader. An unreadable file is reported rather than
    refused, because writing a new cut over it is the remedy that refusal
    names. A file the account cannot open still refuses: ``cause.classified``
    turns a refusal chained from a PermissionError into
    ``path-permission-denied`` at the raise, so it is not the slug caught here,
    and a cut is never written over a file nobody could read (driven, U90).
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

    The source system's calibrate verb took a threshold, and the library's
    real cut, 5.0, was chosen by hand after reading named tracks because the
    fitted one was too tight (R-374). The energy calibration is not touched.
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

    Both calibration files live under the library root, and the atomic writer
    creates the directories on the way to them, so with the volume unmounted
    the first version wrote the calibration onto the boot disk under the
    mount point, where it was invisible the moment the drive came back. The
    registry declares ``library.mounted`` for this verb, and this is the
    check that declaration names, at the strength a state file needs.
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
    """Whether ``folder`` is a folder that holds the WHOLE library, asked of the filesystem.

    TWO FOLDERS QUALIFY: the library root, and the music folder under it. Every
    module that places a track places it under ``root / music_dir``, so that
    folder walked recursively is the library as much as the root is, and
    refusing it as "not the library" was false (U94 review). The root stays
    accepted because it is the one folder that holds the whole library under
    every layout, including one whose tracks were put somewhere the
    configuration has no name for.

    ``samefile`` and not a comparison of two spellings. The volume a DJ library
    sits on is case insensitive, the root is often reached through a link, and
    ``_folder_of`` does not resolve, so the root spelled in lower case, spelled
    in upper case, and reached through a link are one folder that three strings
    would call three. Both candidates are EFFECTIVE values, read off the loaded
    configuration after every override, because a check and its consumer that
    can disagree about an input eventually will (seam decision P2). A candidate
    that cannot be statted is not this folder, which is the conservative
    answer: the check then refuses.
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
    """Why this walk cannot be the library, known BEFORE it is made, or None.

    Returned as what is wrong and what fixes it. Needs one ``samefile`` and no
    walk, so a refusal from here costs nothing: a recursive walk of a library
    on an external volume is a stat per file, and nobody should wait for it to
    be told the folder was the wrong one.

    One level of a folder that holds genre folders is only its loose files,
    and a recursive walk of one genre is still one genre, so both are partial.
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


def _partial_after_walk(scan: discovery.Scan) -> tuple[str, str] | None:
    """Why this walk was not the library, known only AFTER it, or None.

    A genre folder kept as a link to another volume is declined by the walker,
    and a folder the account cannot list contributes nothing, so a recursive
    walk of the root over either is a fit over a library missing a genre. That
    is this unit's whole defect arriving by another road, and the first version
    reported it as ``ok`` with a passing warning beside it (U94 review).
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

    IMPLEMENTED rather than left as a stub (U58). Calibration is a property of
    one library, and until it exists no track has an energy level, so a stub
    here left every analysis uncalibrated while the parity table read the
    rows as covered. Both halves report what they wrote, and a folder that
    cannot support either says so in the check rather than in a warning.

    THE ``calibrate.sample`` CHECK (U94). A calibration fitted over one genre
    folder is not wrong in a way anyone can see. The deciles spread that
    folder's tracks evenly over ten levels, the file loads, every later restamp
    succeeds, and a whole library is rated on the scale of its ambient shelf.
    So the verb asks whether what it is about to fit over is the library, and
    fails the check, measuring nothing and writing nothing, when it is not.
    ``--accept-partial`` is the person saying they know, and then the answer
    says it back on the check, on the envelope and in the file's own note,
    rather than reading as a clean fit.

    THE SAMPLE FLOOR IS NOT WAIVED BY THE FLAG. ``--accept-partial`` answers
    "this is not the whole library", and a sample below
    ``MIN_CALIBRATION_TRACKS`` is a different question with one answer: the
    energy half could never fit, so it is said before anything is measured.

    CHEAPEST REFUSAL FIRST. The floor needs an integer and the folder's
    standing needs one ``samefile``, so both are answered before the walk,
    which on a library is a stat per file. Only what the walk left out has to
    wait for it.

    SYNCHRONOUS AND BOUNDED, NOT A JOB (U94). The energy half measures a
    deterministic stride sample, ``--sample``, so a library of any size costs
    the same run, and the vocal half reads a tag per file, which is cheap, so it
    reads every file under the walk. There is no feature cache and no resume: a
    killed calibrate wrote nothing, because each half writes once at its end.
    """
    cfg = _load()
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
    # BEFORE THE STANDING OF THE FOLDER IS ASKED, because with the volume away
    # no folder is the root and the answer would blame the folder for it.
    _require_library_root(cfg)
    partial = _partial_before_walk(cfg, folder, recursive=recursive)
    if partial is not None and not accepted:
        return _calibrate_refusal(ctx, _partial_refused(partial), summary)

    scan = discovery.scan_audio(folder, recursive=recursive)
    # SAID ON EVERY ANSWER BELOW, the empty one included.
    omitted = discovery.walk_warnings(scan.skipped_links, scan.unreadable, verb="read")
    paths = [discovery.item_path(folder, item) for item in scan.items]
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
        # OK WHEN EITHER HALF WROTE. The first version read the energy half
        # alone, so a run whose tracks would not decode and whose vocal scores
        # split cleanly replaced the library's with vox cut and answered no_op,
        # which tells a machine reader nothing changed (U94 review).
        # ``summary.calibrated`` stays the energy half's, which is what it names.
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
        # ONLY WHEN SOMETHING WAS WRITTEN. The warning speaks of what was
        # written, and over a run where neither half wrote there is no such
        # thing for it to be true of.
        warnings=((_partial_warning(folder),) if partial is not None and wrote else ())
        + tuple(omitted),
    )


def analyze_validate(ctx) -> Envelope:
    """Say plainly that no validation scorer ships in this build.

    NOT IMPLEMENTED, on purpose, and the output says so rather than reporting
    an awaiting check with a report-defect remedy, which read as a tool that
    had failed. The source system's harness scored the detectors against an
    incumbent's tags on a library that carried them, and this build has no
    labelled set format and no incumbent to score against. The residual is
    recorded with U58.
    """
    return ctx.envelope(
        data={
            "checks": [
                _check(
                    "validate.scorer",
                    "validation against labelled ground truth",
                    "unavailable",
                    "no validation scorer ships in this build, so nothing was scored; "
                    "the analysers' agreement with a labelled set has not been measured",
                    None,
                )
            ],
            "summary": {"folder": ctx.args.folder, "validated": False},
        },
        outcome=Outcome.NO_OP,
    )
