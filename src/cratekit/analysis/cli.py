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

THE ITEM IS A FILENAME, RELATIVE TO THE FROZEN FOLDER, AND THE FOLDER IS
FROZEN ABSOLUTE. The first version queued absolute paths, which made the
frozen folder a second copy of a fact every item already carried. The folder
is resolved before it is frozen because ``jobs.spawn`` starts the resume
child in the RESUMING process's working directory, not the queueing one's,
so a relative folder would make every item of a resumed job go missing.

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
from pathlib import Path
from typing import Any, Mapping

from cratekit.analysis import artifacts, detect, energy, light, vocals
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, naming, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS, MarkerRule, NameBudget, NameSpec, NameTemplate

_ORIGIN = ("analysis", "cli")

#: The vocal cut is stored beside the energy calibration, in the state file
#: ``core.config`` declares for it. Read by whoever routes with vox; the
#: threshold is PASSED to the router, never imported by it (D7).
STATE_KEY_VOCAL_CALIBRATION = "vocal_calibration"
#: The fallback cut when a folder has too few scored tracks for Otsu to split.
DEFAULT_VOCAL_THRESHOLD = 12.0
#: How far apart the two clusters' means must sit for a cut between them to
#: mean anything. An all instrumental folder is one cluster, and Otsu will
#: still split it down the middle and call half of it vocal.
MIN_VOCAL_SEPARATION = 10.0
#: How many measured tracks a calibration needs before its deciles mean anything.
MIN_CALIBRATION_TRACKS = 10

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

    NO DOTFILES. macOS writes an AppleDouble sidecar, ``._track.flac``, beside
    every file on an exFAT or FAT volume, which is what a DJ stick is, and the
    sidecar carries the audio suffix. Queued as an item it is decoded, refused
    as undecodable, and then, because the finder moves the sidecar with the
    file it shadows when the track is renamed, refused as missing on the next
    claim and the job fails. ``write/routing_cli.py`` skips the same names.
    """
    if not folder.is_dir():
        return []
    return sorted(
        path.name
        for path in folder.iterdir()
        if path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
    )


def _nothing_to_queue(ctx, folder: Path) -> Envelope:
    """The two zeros, told apart: an empty folder and a folder that is not there.

    A mistyped path or an unmounted volume must not read as "nothing new to
    analyse", which is what one shared no-op would say. The tagging verbs make
    the same split.
    """
    if folder.is_dir():
        return ctx.envelope(data=_no_op("no-audio"), outcome=Outcome.NO_OP)
    return ctx.envelope(
        data=_no_op("folder-absent"),
        outcome=Outcome.NO_OP,
        warnings=(
            {
                "code": "folder-absent",
                "message": f"{folder} is not a folder on this machine, so nothing was queued",
            },
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
    count = int(summary.get("by_vocal_reason", {}).get(vocals.REASON_MODEL_UNAVAILABLE, 0))
    if not count:
        return None
    return {
        "code": vocals.REASON_MODEL_UNAVAILABLE,
        "message": (
            f"{count} track(s) were analysed with no vocal model loaded and carry "
            f"no voxlevel; the model needs the 'vocals' extra, "
            f"pip install 'cratekit[vocals]', and the planned re-score verb"
        ),
    }


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
    parser.add_argument(
        "folder", nargs="?", default=None, help="folder whose tracks fit the calibration"
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
    if not job.is_open() and job.cause is not None:
        raise CratekitError(job.cause)
    return job, warnings


def _resume(ctx, cfg: config.Config) -> Envelope:
    with jobs.open_store() as store:
        job, warnings = _advance(ctx, store, jobs.get(store, ctx.args.job))
        summary = _summary(cfg, job.job_id)
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
    """The frozen folder and the item's path in it, the one rule both workers use."""
    folder = Path(str((job.payload or {}).get("folder") or ""))
    return folder, folder / item.item_id


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
        detail={"extras": "analysis", "install": "pip install 'cratekit[analysis]'"},
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
            steps=("run `crate analyze calibrate FOLDER` over a representative folder first",),
            origin=_ORIGIN,
            detail={"calibration": str(energy.calibration_path(cfg))},
        )
    return calibration


def analyze_restamp(ctx) -> Envelope:
    cfg = _load()
    if ctx.args.job:
        return _resume(ctx, cfg)
    folder = _folder_of(ctx.args.folder)
    items = _audio_in(folder)
    if not items:
        # BEFORE THE CALIBRATION CHECK: a folder with nothing to restamp is a
        # complete answer whether or not the library is calibrated.
        return _nothing_to_queue(ctx, folder)
    # REFUSED AT THE QUEUE, not only in the worker: a job whose every item
    # would fail on the same absence is a report over work nothing could do.
    _calibration_or_refuse(cfg)
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            cfg=cfg,
            item_ids=items,
        )
        return ctx.envelope(data=_reported(store, job), warnings=(DB_NOT_WRITTEN,))


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
    hist, edges = np.histogram(values, bins=bins, range=(0.0, 100.0))
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


def _calibrate_energy(cfg: config.Config, folder: Path, paths: list[Path]) -> dict[str, str | None]:
    measured: list[dict[str, float]] = []
    unreadable = 0
    for path in paths:
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
            f"{len(measured)} of {len(paths)} tracks in {folder} could be measured, "
            f"and a calibration needs at least {MIN_CALIBRATION_TRACKS}; nothing "
            f"was written",
            Remedy.FIX_COMMAND_LINE,
        )
    calibration = energy.calibrate(measured, note=f"fitted over {folder}")
    written = energy.save_calibration(cfg, calibration)
    levels = [energy.level_for(features, calibration) for features in measured]
    counts = energy.distribution(levels)
    return _check(
        "calibrate.energy",
        "energy calibration",
        "ok",
        f"fitted over {len(measured)} tracks ({unreadable} unreadable), written to "
        f"{written}; level distribution {json.dumps(counts, sort_keys=True)}",
        None,
    )


def _calibrate_vocals(cfg: config.Config, folder: Path, paths: list[Path]) -> dict[str, str | None]:
    from cratekit.analysis import vocal

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
            f"no track in {folder} carries a vocal score yet, so there is no "
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
            f"the {len(scores)} scored tracks in {folder} do not split into two "
            f"clusters (best cut {threshold:.1f}, separation "
            f"{0.0 if separation is None else separation:.1f} of the "
            f"{MIN_VOCAL_SEPARATION:.0f} needed), so no cut was written; a folder "
            f"holding both instrumental and vocal tracks is what a cut needs",
            Remedy.FIX_COMMAND_LINE,
        )
    target = energy.write_json(
        vocal_calibration_path(cfg),
        {
            "threshold": threshold,
            "gender_margin": vocal.DEFAULT_GENDER_MARGIN,
            "n_tracks": len(scores),
            "method": "otsu",
            "note": f"fitted over {folder}",
        },
    )
    above = sum(1 for score in scores if score >= threshold)
    return _check(
        "calibrate.vocals",
        "vocal cut",
        "ok",
        f"cut at {threshold:.1f} over {len(scores)} scored tracks, {above} above it, "
        f"written to {target}; no routing pass in this build reads it yet",
        None,
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


def analyze_calibrate(ctx) -> Envelope:
    """Fit this library's energy reference and vocal cut over one folder.

    IMPLEMENTED rather than left as a stub (U58). Calibration is a property of
    one library, and until it exists no track has an energy level, so a stub
    here left every analysis uncalibrated while the parity table read the
    rows as covered. Both halves report what they wrote, and a folder that
    cannot support either says so in the check rather than in a warning.
    """
    cfg = _load()
    if not ctx.args.folder:
        return ctx.envelope(
            data={
                "checks": [
                    _check(
                        "calibrate.folder",
                        "calibration folder",
                        "skipped",
                        "no folder given, so nothing was measured and nothing was written",
                        Remedy.FIX_COMMAND_LINE,
                    )
                ],
                "summary": {"folder": None, "calibrated": False},
            },
            outcome=Outcome.NO_OP,
        )
    folder = _folder_of(ctx.args.folder)
    paths = [folder / name for name in _audio_in(folder)]
    if not paths:
        detail = (
            f"{folder} holds no audio files, so nothing was measured"
            if folder.is_dir()
            else f"{folder} is not a folder on this machine, so nothing was measured"
        )
        return ctx.envelope(
            data={
                "checks": [
                    _check(
                        "calibrate.folder",
                        "calibration folder",
                        "failed",
                        detail,
                        Remedy.FIX_COMMAND_LINE,
                    )
                ],
                "summary": {"folder": str(folder), "calibrated": False},
            },
            outcome=Outcome.NO_OP,
        )
    _require_heavy(energy.extractor_bound(), "measuring a folder's energy")
    _require_library_root(cfg)
    checks = [_calibrate_energy(cfg, folder, paths), _calibrate_vocals(cfg, folder, paths)]
    calibrated = checks[0]["status"] == "ok"
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {"folder": str(folder), "calibrated": calibrated, "tracks": len(paths)},
        },
        outcome=Outcome.OK if calibrated else Outcome.NO_OP,
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
