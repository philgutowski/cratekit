"""``crate analyze``: queue the heavy passes as jobs, and drive them.

Long work is a job (KTD26, R22). The shell freezes the folder and the item
list, and a killed driver resumes by trusting DONE rows and the mark
``analyze run`` leaves on each file it measured (U343), or the head on the
name a run before U343 left. Run by hand, ``analyze run`` and ``analyze
restamp`` drive the job they queue in this process (U192), through
:func:`cratekit.modules.foreground.settle`; ``--queue-only`` leaves the drive
to a caller such as ``crate sync land``.

THE TWO WORKERS LIVE HERE (U58), ``handle_run`` and ``handle_restamp``. Each
reads its subject from the ITEM, never the payload, or every item of a multi
item job would do the same work.

THE ITEM IS A PATH RELATIVE TO THE FROZEN FOLDER, AND THE FOLDER IS FROZEN
ABSOLUTE, because ``jobs.spawn`` starts the resume child in the resuming
process's working directory. ``analyze restamp --recursive`` (U93) makes the
path more than one segment. ``analyze run`` takes no such flag.

THE SEAMS ARE BOUND AT CALL TIME: the detector, the vocal model loader, the
decoder and the feature extractor are module state looked up when a worker
runs, so a test binds a fake, and a fresh process binds the shipped defaults,
each importing the heavy stack lazily. The child ``crate job resume`` spawns
inherits nothing a test patched (R-226).

THE MODEL MODULE IS NEVER IMPORTED AT MODULE SCOPE: ``cli.jobs.argv_for``
imports this module to build a resume line, and the model imports numpy,
which the slim profile does not declare.
"""

from __future__ import annotations

import contextlib
import dataclasses
import functools
from pathlib import Path
from typing import Any, Iterator, Mapping

from cratekit.analysis import ahead, artifacts, decode, detect, energy, light, run, vocals
from cratekit.cli.output import Envelope, load_config, no_job
from cratekit.core import config, jobs, naming, pool, tags
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import NameTemplate
from cratekit.intake import drift as drift_words
from cratekit.modules import extras, foreground

_ORIGIN = ("analysis", "cli")

#: The fallback cut when a folder has too few scored tracks for Otsu to split.
DEFAULT_VOCAL_THRESHOLD = 12.0
#: How many tracks the energy fit measures unless ``--sample`` says otherwise
#: (U94). ``energy.calibrate``'s tightest statistic is its second percentile,
#: and at 500 tracks that rests on the ten tracks a whole fit demands. What a
#: track costs to measure on a real library is owed to an attended sitting.
DEFAULT_CALIBRATION_SAMPLE = 500

#: The handler key of ``crate analyze run``, the one verb here whose drive
#: measures ahead of itself (U241). ``analyze restamp`` shares the resume.
RUN_HANDLER_KEY = "analyze.run"

#: The run report's key naming the calibration its level was scored under (U344).
SCORED_UNDER = "calibration"
#: The run report's key saying the energy's slice did not move with the run's
#: own tag write (U344), and what :func:`slice_length` answers for a file
#: decoded whole, whose length no tag moves.
SLICE_HELD = "slice_held"
DECODED_WHOLE = "decoded-whole"
#: The payload key recording why a restamp told a run's job left nothing out.
PAYLOAD_LEFT_OUT_NOTHING = "left_out_nothing"
#: ``analyze restamp``'s flag naming the ``analyze run`` job of this pass, whose
#: scored files it leaves out (U344), and the payload keys that record them.
SCORED_BY_FLAG = "--scored-by"
PAYLOAD_SCORED_BY = "scored_by"
PAYLOAD_LEFT_OUT = "left_out"
#: The no op ``analyze restamp --scored-by`` answers when the run scored every file.
ALL_SCORED = "scored-by-run"

#: The warning every restamp resume carries, because the registry declares a
#: database write this build does not perform. See ``handle_restamp``.
DB_NOT_WRITTEN = {
    "code": "db-metadata-not-written",
    "message": (
        "this restamp wrote the energylevel file tag only; the rekordbox star "
        "rating half the verb declares is not written by this build"
    ),
}


def _folder_of(named: str) -> Path:
    return Path(named).expanduser().absolute()


def _audio_in(folder: Path) -> list[str]:
    """The item identifiers: audio FILENAMES in the folder, sorted, not recursive.

    No dotfiles: a DJ stick's AppleDouble sidecars carry the audio suffix and
    would fail the job. The rule lives in ``core.discovery`` so every verb
    agrees on it.
    """
    return list(jobs.scan_audio(folder).items)


def walk_folder(ctx) -> tuple[Path, bool, jobs.Scan, tuple[dict[str, str], ...]]:
    """The folder a queueing verb names, its walk, and the folders it left out."""
    folder = _folder_of(ctx.args.folder)
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = jobs.scan_audio(folder, recursive=recursive)
    return folder, recursive, scan, jobs.walk_warnings(scan.skipped_links, scan.unreadable)


def nothing_to_queue(
    ctx, folder: Path, extra: tuple[dict[str, str], ...] = (), *, state: str = "no-audio"
) -> Envelope:
    """The zeros, told apart: an empty folder and a folder that is not there.

    A mistyped path or an unmounted volume must not read as nothing new to
    do. ``extra`` carries the walk's declined folders onto the zero too.
    """
    if folder.is_dir():
        return ctx.envelope(data=no_job(state), outcome=Outcome.NO_OP, warnings=extra)
    return ctx.envelope(
        data=no_job("folder-absent"),
        outcome=Outcome.NO_OP,
        warnings=(
            {
                "code": "folder-absent",
                "message": f"{folder} is not a folder on this machine, so nothing was queued",
            },
            *extra,
        ),
    )


def committed_summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
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

    ``analyze.run`` declares the ``analysis`` extra and the model lives behind
    ``vocals``, so a machine with only the first finalizes every track with no
    vocal tags under a plain success. This lifts that onto the envelope.
    """
    return vocals.unscored_warning(summary, verb="analysed")


def build(parser, entry) -> None:
    parser.add_argument("folder", help="folder of audio to analyse")
    foreground.add_job_options(parser, what="analysis")
    parser.set_defaults(_handler=analyze_run)


def build_calibrate(parser, entry) -> None:
    # One or the other: a folder fits the vocal cut and the flag sets it.
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
        SCORED_BY_FLAG,
        dest="scored_by",
        default=None,
        metavar="JOB_ID",
        help=(
            "leave out each file the analyze run job JOB_ID scored at its present "
            "name under the calibration active now, whose energy tag still reads "
            "that level and whose length did not move with the run's own tag "
            "write, since the run measured it as a restamp would; the tail "
            "passes it"
        ),
    )
    foreground.add_job_options(parser, what="restamp")
    parser.set_defaults(_handler=analyze_restamp)


def analyze_argv(job) -> list[str]:
    folder = job.payload.get("folder", "")
    return ["analyze", "run", folder, "--job", job.job_id]


def restamp_argv(job) -> list[str]:
    folder = job.payload.get("folder", "")
    return ["analyze", "restamp", folder, "--job", job.job_id]


def _advance(ctx, store, job, *, around=None):
    """Reconcile, refuse an empty job, run it, and raise if it did not finish.

    Not named ``drive``: ``tests/test_handlers.py`` counts calls to a callee
    of that name as calls to the job driver. ``around`` is a context manager
    factory held open for exactly the drive, the run ahead of ``analyze run``
    (U241), whose workers must end on every way out.
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
        with around(store, job) if around is not None else contextlib.nullcontext():
            _result, warnings = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
    jobs.raise_for_state(job)
    return job, warnings


def _may_measure_ahead() -> str | None:
    """Why this process cannot hand heads to a worker, or None when it can.

    A test's detector is a closure no spawned child could receive, unless the
    test also bound an importable one, and without the extra there is nothing
    to measure with.
    """
    if ahead.worker_bound():
        return None
    if _fake_detect_bound():
        return ahead.WHY_TEST_DETECTOR
    if not detect.heavy_available():
        return ahead.WHY_NO_EXTRA
    return None


def _waiting(cfg: config.Config, store, job) -> list[str]:
    """The files this drive will measure: unsettled items, present, not yet measured.

    The driver's own three tests, asked ahead of it, so no worker reads a file
    the driver would skip.
    """
    unsettled = (jobs.ItemState.PENDING, jobs.ItemState.CLAIMED)
    found: list[str] = []
    for item in jobs.items(store, job.job_id):
        if item.state not in unsettled:
            continue
        try:
            _folder, path = _folder_and_path(job, item)
        except CratekitError:
            # An identifier the folder rule refuses is refused by its own item.
            continue
        if path.is_file() and not already_measured(path, cfg):
            found.append(str(path))
    return found


def _open_ahead(cfg: config.Config, store, job) -> ahead.Session:
    """Plan the light pool for this drive, or note why everything is measured here."""
    why = _may_measure_ahead()
    if why is not None:
        return ahead.note_unopened(job.job_id, why)
    waiting = _waiting(cfg, store, job)
    try:
        settings = _settings(cfg)
    except CratekitError:
        # AN UNREADABLE CALIBRATION IS EACH ITEM'S TO REFUSE, by name.
        return ahead.note_unopened(job.job_id, "the energy calibration could not be read")
    reserve = pool.DEFAULT_MEMORY_RESERVE_BYTES
    if waiting and (vocals.loader_bound() or vocals.missing_requirement() is None):
        # THE DRIVER WILL HOLD A VOCAL MODEL while the workers run, not yet
        # loaded at planning, so its declared cost is kept back here.
        reserve += vocals.VOCAL_WORKER_BYTES
    return ahead.open_session(job.job_id, waiting, settings, reserve_bytes=reserve)


@contextlib.contextmanager
def _heads_ahead(store, job) -> Iterator[None]:
    """Hold the job's run ahead open for one drive, then record the pool it was.

    Planned under the FROZEN configuration (KTD9), the one each item binds.
    The workers end and the record is written on every way out, since a run
    that failed ran with a pool too; a record that cannot be written is a
    line missing from the answer, never a failed job.
    """
    cfg = jobs.frozen_config(job)
    session = _open_ahead(cfg, store, job)
    drove = True
    try:
        yield
    except jobs.DriverHeld:
        # ANOTHER DRIVER HAS THE JOB, so this call ran nothing; that driver
        # writes its own record.
        drove = False
        raise
    finally:
        ahead.close_session(job.job_id)
        if drove and _worth_recording(cfg, job.job_id, session):
            try:
                artifacts.record_pool(cfg, job.job_id, ahead.report(session))
            except OSError:
                pass


def _worth_recording(cfg: config.Config, job_id: str, session: ahead.Session) -> bool:
    """Whether this drive's pool replaces the one the job already records.

    A DRIVE THAT MEASURED NOTHING DOES NOT OVERWRITE ONE THAT DID: the line is
    about the pool that measured the job's files (U241 review).
    """
    if session.plan is not None:
        return True
    return artifacts.pool_record(cfg, job_id) is None


def _pool_check(record: Mapping[str, Any] | None) -> dict[str, str | None]:
    """The ``analyze.pool`` check line: how many workers the run used, and why (U241)."""
    if record is None or not isinstance(record.get("detail"), str):
        return _check(
            "analyze.pool",
            "analysis pool",
            "info",
            "no pool was recorded for this job, so how many workers ran is not known",
            None,
        )
    status = str(record.get("status") or "info")
    return _check("analyze.pool", "analysis pool", status, str(record["detail"]), None)


def _with_pool(error: CratekitError, record: Mapping[str, Any]) -> CratekitError:
    """The same refusal, also saying what pool the run that did not finish ran with.

    The check line rides only the envelope, so a failed run says it as an
    appended step and the record in the detail. The cause and its type are
    otherwise carried through.
    """
    cause = error.cause
    line = f"the pool: {_pool_check(record)['detail']}"
    return rebuilt(
        error,
        dataclasses.replace(
            cause,
            remediation=dataclasses.replace(
                cause.remediation, steps=(*cause.remediation.steps, line)
            ),
            detail={**cause.detail, "pool": dict(record)},
        ),
    )


def _resume(ctx, cfg: config.Config, job_id: str) -> Envelope:
    with jobs.open_store() as store:
        queued = jobs.get(store, job_id)
        if queued.handler_key != RUN_HANDLER_KEY:
            job, warnings = _advance(ctx, store, queued)
        else:
            try:
                job, warnings = _advance(ctx, store, queued, around=_heads_ahead)
            except jobs.DriverHeld:
                # This call drove nothing, so it has no pool of its own to add.
                raise
            except CratekitError as failed:
                # A run that failed or was stopped ran with a pool as well.
                pooled = artifacts.pool_record(cfg, job_id)
                if pooled is None:
                    raise
                raise _with_pool(failed, pooled) from failed
        summary = committed_summary(cfg, job.job_id)
        # THE RESUME IS THE REPORT A PERSON KEEPS, so what the walk left out
        # rides it too, read back off the frozen payload.
        warnings = (*warnings, *jobs.warnings_of(job.payload))
        if job.handler_key == "analyze.restamp":
            warnings = (*warnings, DB_NOT_WRITTEN)
            # What a tail's restamp left out because the run scored it (U344).
            summary.update(left_out_of(job.payload))
            why = (job.payload or {}).get(PAYLOAD_LEFT_OUT_NOTHING)
            if isinstance(why, str):
                warnings = (*warnings, left_out_nothing(why))
        else:
            # THE TEMPO IS A MEASUREMENT WITH A KNOWN ERROR (R-744): rekordbox
            # will not always agree, so the answer carries the measured rate.
            summary["head_agreement"] = detect.head_agreement(
                window=(cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling)
            )
            # HOW MANY WORKERS THE RUN USED, AND WHY (U241), off the record.
            summary["checks"] = [_pool_check(artifacts.pool_record(cfg, job.job_id))]
            unscored = _unscored_vocals_warning(summary)
            if unscored is not None:
                warnings = (*warnings, unscored)
        return ctx.envelope(
            data=jobs.reported(store, job, {"analysis": summary}),
            warnings=warnings,
        )


def _settle(ctx, cfg: config.Config, job, argv: list[str]) -> Envelope:
    """Drive the job this call just queued through the resume, in this process (U192)."""
    return foreground.settle(
        job.job_id, lambda: _resume(ctx, cfg, job.job_id), argv=argv, origin="analysis.cli"
    )


def analyze_run(ctx) -> Envelope:
    cfg = load_config(("analysis.cli",))
    if ctx.args.job:
        return _resume(ctx, cfg, ctx.args.job)
    folder = _folder_of(ctx.args.folder)
    items = _audio_in(folder)
    if not items:
        return nothing_to_queue(ctx, folder)
    # A CORRUPT CALIBRATION REFUSES AT THE QUEUE, as the restamp does, rather
    # than failing every item on the same file. An absent one is honest.
    energy.load_calibration(cfg)
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            cfg=cfg,
            item_ids=items,
        )
        if foreground.queue_only(ctx.args):
            return ctx.envelope(data=jobs.reported(store, job))
    return _settle(ctx, cfg, job, analyze_argv(job))


def _template(cfg: config.Config) -> NameTemplate:
    return NameTemplate.lossy(cfg.naming.lossy_marker)


def already_measured(path: Path, cfg: config.Config) -> bool:
    """Whether ``analyze run`` measured ``path`` already, its resume marker.

    The mark the run writes (U343), or a head on the name, which a run before
    U343 left. Named so ``crate analyze vocals --unscored`` picks exactly the
    files a run will never score again (U181, R-277).
    """
    return run.already_analyzed(path, template=_template(cfg))


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

    ``core.jobs.item_path`` refuses an id that would leave the folder: an
    absolute right hand side would discard the base silently (U93).
    """
    folder = Path(str((job.payload or {}).get("folder") or ""))
    return folder, jobs.item_path(folder, str(item.item_id))


def _item_path(job, item, what: str) -> Path:
    folder, path = _folder_and_path(job, item)
    if not path.is_file():
        raise _refuse_missing(item, folder, path, what)
    return path


def _finalized_twin(cfg: config.Config, job, item) -> Path | None:
    """The file this item became, if a finalize renamed it before its row moved.

    ONLY A BUILD BEFORE U343 RENAMED, so this recovers a job such a build left
    half done. A kill between the rename and the row flipping to done leaves a
    finished file under its head and a pending row under its old name. The answer
    comes from this item's own rename intent, never a scan of the folder,
    which matched unrelated twins. With the intent gone, from the item's own
    staged report (U223).
    """
    target = artifacts.rename_intent(cfg, job, item)
    if target is None:
        target = _staged_twin(cfg, job, item)
    if target is None or not target.is_file():
        return None
    return target


def _staged_twin(cfg: config.Config, job, item) -> Path | None:
    """The renamed file an uncommitted staged report of this item names, if any.

    Only a report that says it renamed, naming a path in the item's own
    folder, where a build before U343 renamed to.
    """
    report = artifacts.staged_report(cfg, job, item)
    if report is None:
        return None
    recorded = report.get("path")
    if not isinstance(recorded, str) or not recorded:
        return None
    target = Path(recorded)
    status = report.get("status")
    if status == "analyzed":
        if report.get("renamed_to") != target.name:
            return None
    elif status != "skipped-prefixed" or report.get("resumed_after_rename") is not True:
        return None
    _, source = _folder_and_path(job, item)
    if target.parent != source.parent:
        return None
    return target


def _require_heavy(seam_bound: bool, what: str) -> None:
    """Refuse the item when the extra is absent HERE and no fake is bound.

    The detector answers a missing extra with None, so without this a job
    with no librosa would settle every file ``skipped-no-key`` and report done. The
    remedy is the parser stub's for the same slug.
    """
    if seam_bound or detect.heavy_available():
        return
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


def _settings(cfg: config.Config) -> ahead.Settings | None:
    """What a head is measured under right now, or None under a test's detector.

    Read per call, as the binding below reads it per item. A test's own
    detector is measured under whatever the test chose, compared only with itself.
    """
    if _fake_detect_bound():
        return None
    return ahead.Settings.of(energy.load_calibration(cfg), cfg)


def _bind_defaults(cfg: config.Config) -> ahead.Settings | None:
    """Bind the shipped seams where nothing else is bound, PER ITEM.

    Rebound every call because the partial carries the calibration, which may
    change between two jobs one process drives. A test's binding is left
    alone. Answers the settings the detector was bound under (U241).
    """
    global _BOUND_DETECT
    settings: ahead.Settings | None = None
    if not _fake_detect_bound():
        calibration = energy.load_calibration(cfg)
        settings = ahead.Settings.of(calibration, cfg)
        _BOUND_DETECT = functools.partial(
            detect.analyse_file,
            calibration=calibration,
            tempo_window=(cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling),
            drift_cut=cfg.analysis.drift_cut,
        )
        light.bind_detect(_BOUND_DETECT)
    if not vocals.loader_bound():
        from cratekit.analysis import vocal

        vocals.bind_loader(vocal.default_loader)
    return settings


def _write_or_refuse(path: Path, fields: dict[str, Any], *, untouched: str) -> None:
    """A tag write that did not land refuses under the analysis slug.

    ``write_tags`` returns False for a file it could not write and raises
    ``UnsupportedContainer`` for a container it does not know. ONLY THAT
    SUBCLASS is caught: a plain ``ValueError`` for an unknown field is the
    beat grid enforcement point (R17) and must stay loud.
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


def _untitled(cfg: config.Config, path: Path) -> str | None:
    """The title a file with no title tag is given, or None for a file that has one.

    The naming engine's title for the file with no head: its stem, a lossy
    marker in it set before it as R21 marks a lossy title, so the title
    the landing lands and the file's title tag are one, the equality ``analyze
    adopt`` asks of a bare title before it stamps one (review round one): a run
    before U343 gave every file a title in its headed write.
    """
    if (tags.read_tag(path, "title") or "").strip():
        return None
    template = _template(cfg)
    marker = cfg.naming.lossy_marker
    spec = naming.NameSpec(
        stem=path.stem, suffix=path.suffix, lossy=bool(marker) and marker in path.stem
    )
    return naming.render_all(spec, template=template).title_tag or None


def _finalize(cfg: config.Config, path: Path, scored: Mapping[str, Any]) -> None:
    """Write the measured values onto the file, with the mark, in one write.

    NO HEAD, NO KEY AND NO RENAME (U343): the head comes from rekordbox after
    the visit, through ``analyze adopt``. A title is written only on a file
    with none, its stem, so adopt can stamp it (:func:`_untitled`). The mark
    rides the same write, so a file is marked exactly when its values landed.
    An absent level or vocal score writes no tag, which routing reads as
    unscored. The drift level only when measured, its verdict whenever given
    (U157).
    """
    fields = {
        "title": _untitled(cfg, path),
        "energylevel": scored.get("energy"),
        "voxlevel": scored.get("voxlevel"),
        "voxgender": scored.get("voxgender"),
        "voxgenderconf": scored.get("voxgenderconf"),
        "driftlevel": _drift_level(scored.get("drift")),
        "drift": scored.get("drift_verdict"),
        run.MARK_FIELD: run.MARK_VALUE,
    }
    _write_or_refuse(path, fields, untouched="The file is untouched")


def _drift_level(measured: Any) -> str | None:
    """A measured drift as its tag spells it, or None for no measurement (U157)."""
    if measured is None:
        return None
    return drift_words.shown(float(measured))


def handle_run(job, item, cfg) -> jobs.Produced:
    """Analyse ONE file, the per item worker behind ``analyze.run``.

    A file already measured is skipped unread. Otherwise the light measure,
    the vocal score, then the finalize; a measure with no decode or no tempo
    is a terminal skip with nothing written. The file keeps its name (U343).
    The configuration is the frozen one (KTD9).
    """
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
    # THE SOURCE IS A FILE, so evidence an earlier attempt left names a rename
    # that did not land; this attempt starts clean, and renames nothing (U223, U343).
    artifacts.discard_rename_evidence(cfg, job, item)
    if already_measured(path, cfg):
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": "skipped-prefixed"}
        )
    _require_heavy(_fake_detect_bound(), "analysing a track")
    settings = _bind_defaults(cfg)
    # Measured ahead when the run has a pool and the head still stands (U241).
    partial = ahead.head(job.job_id, str(path), settings)
    if partial.get("terminal") is not None:
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": partial["terminal"]}
        )
    scored = vocals.analyse(partial)
    # THE SLICE THE ENERGY WAS MEASURED OVER IS CENTRED ON THE FILE'S LENGTH,
    # which libsndfile estimates from the size of an MP3 with no Xing header,
    # so the tag write below can move it (U344 review): read before and after.
    measured = scored.get("energy") is not None
    before = slice_length(path) if measured else None
    _finalize(cfg, path, scored)
    held = measured and before is not None and slice_length(path) == before
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "item": item.item_id,
            "path": str(path),
            "status": "analyzed",
            "tempo": int(scored.get("rate", scored.get("bpm"))),
            "energy": scored.get("energy"),
            "energy_status": scored.get("energy_status"),
            "vocal_active": bool(scored.get("vocal_active")),
            "vocal_reason": scored.get("vocal_reason"),
            "voxlevel": scored.get("voxlevel"),
            "voxgender": scored.get("voxgender"),
            "drift": scored.get("drift"),
            "drift_verdict": scored.get("drift_verdict"),
            # WHICH CALIBRATION THE LEVEL IS UNDER, so the tail's restamp leaves
            # this file out only while that calibration is still the one (U344).
            SCORED_UNDER: _scored_under(cfg, settings),
            SLICE_HELD: held,
        },
    )


def slice_length(path: Path) -> float | str | None:
    """The length the energy measure centres its slice on, or None when unread.

    A file libsndfile opens answers its header's length, a read of the header
    alone. Any other is decoded whole (by ffmpeg, or by audioread under a
    librosa before 1.0), whose length is the decoded samples' and no tag can
    move, so it answers that it is decoded, with no decode here; a file nothing
    can read answers so too, and the run measured no energy for it to keep.
    None when the analysis stack is absent or the length cannot be read: a
    length not read is not a length that held.
    """
    try:
        if not decode.libsndfile_opens(path):
            return DECODED_WHOLE
        return decode.duration(path)
    except Exception:  # noqa: BLE001 - an unread length leaves the file to the restamp
        return None


def _scored_under(cfg: config.Config, settings: ahead.Settings | None) -> str | None:
    """The fingerprint of the calibration this item's level was scored under, or None.

    The settings the detector was bound under; under a test's own detector,
    which binds none, the calibration active now.
    """
    if settings is not None:
        held = settings.calibration
        return None if held is None else energy.fingerprint(held)
    active = energy.load_calibration(cfg)
    return None if active is None else energy.fingerprint(active)


def as_level(text: str | None) -> int | None:
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
    cfg = load_config(("analysis.cli",))
    if ctx.args.job:
        return _resume(ctx, cfg, ctx.args.job)
    folder, recursive, scan, extra = walk_folder(ctx)
    if not scan.items:
        # Before the calibration check: nothing to restamp is a full answer.
        return nothing_to_queue(ctx, folder, extra)
    # REFUSED AT THE QUEUE, not only in the worker: a job whose every item
    # would fail on the same absence is a report over work nothing could do.
    calibration = _calibration_or_refuse(cfg)
    items: list[str] = list(scan.items)
    scored_by: dict[str, Any] = {}
    if ctx.args.scored_by:
        left_out, why = scored_in_pass(cfg, ctx.args.scored_by, folder, items, calibration)
        items = [item for item in items if item not in left_out]
        scored_by = {
            PAYLOAD_SCORED_BY: ctx.args.scored_by,
            PAYLOAD_LEFT_OUT: sorted(left_out),
        }
        if why is not None:
            # ON THE PAYLOAD as well, since the foreground answer is the resume's.
            scored_by[PAYLOAD_LEFT_OUT_NOTHING] = why
            extra = (*extra, left_out_nothing(why))
        if not items:
            return ctx.envelope(
                data=no_job(ALL_SCORED, left_out=len(left_out), scored_by=ctx.args.scored_by),
                outcome=Outcome.NO_OP,
                warnings=extra,
            )
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            # FROZEN WITH THE FOLDER: the resume never re-scans, so it reports
            # the tree the job was queued against.
            payload={
                "folder": str(folder),
                **jobs.frozen_walk(scan, recursive=recursive),
                **scored_by,
            },
            cfg=cfg,
            item_ids=items,
        )
        if foreground.queue_only(ctx.args):
            return ctx.envelope(
                data=jobs.reported(store, job, left_out_of(job.payload)),
                warnings=(DB_NOT_WRITTEN, *extra),
            )
    # NOT ``extra`` AGAIN: the resume reads the walk's warnings off the payload.
    return _settle(ctx, cfg, job, restamp_argv(job))


def scored_in_pass(
    cfg: config.Config,
    run_job_id: str,
    folder: Path,
    items: list[str],
    calibration: energy.Calibration,
) -> tuple[set[str], str | None]:
    """The items ``run_job_id`` scored that a restamp would leave as they are, and why none.

    An item is left out only when the run's committed report says it was
    analysed at exactly this path with a level under the calibration active
    now, the slice its energy was measured over did not move with the run's
    own tag write, and the file's energy tag still reads that level: the run
    measures through the restamp's own :func:`energy.measure` (U344), over
    the same samples, so the restamp would answer the same level and write
    nothing. Anything else, a job that
    is not a finished run over this folder included, is restamped as it
    always was; the second answer says why nothing was left out, when so.
    """
    with jobs.open_store() as store:
        try:
            run = jobs.get(store, run_job_id)
        except CratekitError:
            # An identifier the queue does not hold, or a queue that cannot
            # answer: nothing is known to be scored, so nothing is left out.
            run = None
    if run is None:
        return set(), f"no job {run_job_id} is recorded, so every file is restamped"
    if run.handler_key != RUN_HANDLER_KEY or run.state is not jobs.JobState.SUCCEEDED:
        return set(), (
            f"job {run_job_id} is not a finished analyze run ({run.handler_key}, "
            f"{run.state}), so every file is restamped"
        )
    if _folder_of(str(run.payload.get("folder") or "")) != folder:
        return set(), (
            f"job {run_job_id} analysed {run.payload.get('folder')}, not {folder}, so "
            f"every file is restamped"
        )
    active = energy.fingerprint(calibration)
    scored: dict[Path, int] = {}
    for report in artifacts.committed(cfg, run.job_id):
        level = report.get("energy")
        if (
            report.get("status") == "analyzed"
            and report.get("energy_status") == energy.STATUS_CALIBRATED
            and isinstance(level, int)
            and not isinstance(level, bool)
            and report.get(SCORED_UNDER) == active
            and report.get(SLICE_HELD) is True
            and isinstance(report.get("path"), str)
        ):
            scored[Path(report["path"])] = level
    left_out: set[str] = set()
    for item in items:
        path = folder / item
        level = scored.get(path)
        if level is not None and as_level(tags.read_tag(path, "energylevel")) == level:
            left_out.add(item)
    return left_out, None


def left_out_nothing(why: str) -> dict[str, str]:
    """The warning a restamp told a run's job carries when it could leave nothing out."""
    return {"code": "restamp-left-out-nothing", "message": why}


def left_out_of(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    """What a restamp queued with ``--scored-by`` left out, read off its payload."""
    held = payload or {}
    if PAYLOAD_SCORED_BY not in held:
        return {}
    names = held.get(PAYLOAD_LEFT_OUT)
    return {
        PAYLOAD_LEFT_OUT: len(names) if isinstance(names, list) else 0,
        PAYLOAD_SCORED_BY: str(held[PAYLOAD_SCORED_BY]),
    }


def handle_restamp(job, item, cfg) -> jobs.Produced:
    """Rescore ONE file's energy against the active calibration and stamp it.

    THE PREVIOUS TAG TEXT IS RECORDED BEFORE THE WRITE in the undo log, the
    only surviving copy of it. A level that did not move is not rewritten.
    FILE TAG ONLY: the registry's ``db_metadata`` half is not written by this
    build, so every report says ``db_written: false`` (U58).
    """
    path = _item_path(job, item, "restamp")
    calibration = _calibration_or_refuse(cfg)
    _require_heavy(energy.extractor_bound(), "measuring a track's energy")
    features = energy.measure(path)
    # ONE READ OF THE TAG, so the logged text and the compared integer agree.
    previous_text = tags.read_tag(path, "energylevel")
    previous = as_level(previous_text)
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


def analyze_calibrate(ctx) -> Envelope:
    """``crate analyze calibrate``, whose body is :mod:`cratekit.analysis.calibrate`."""
    from cratekit.analysis import calibrate

    return calibrate.analyze_calibrate(ctx)


def analyze_validate(ctx) -> Envelope:
    """Say plainly that no validation scorer ships in this build.

    NOT IMPLEMENTED, on purpose: this build has no labelled set format and no
    incumbent to score against, and an awaiting check read as a failed tool.
    The residual is recorded with U58.
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
