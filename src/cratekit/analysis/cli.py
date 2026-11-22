"""``crate analyze``: queue the heavy passes as jobs, and drive them.

Long work is a job (KTD26, R22). The shell freezes the folder and the item
list, and a killed driver resumes by trusting DONE rows and the Camelot
prefixed names they left. Run by hand, ``analyze run`` and ``analyze
restamp`` drive the job they queue in this process (U192), through
:func:`cratekit.modules.foreground.settle`; ``--queue-only`` leaves the drive
to a caller such as ``crate sync land``.

THE TWO WORKERS LIVE HERE (U58), ``handle_run`` and ``handle_restamp``. Each
reads its subject from the ITEM, never the payload, or every item of a multi
item job would do the same work.

THE ITEM IS A PATH RELATIVE TO THE FROZEN FOLDER, AND THE FOLDER IS FROZEN
ABSOLUTE, because ``jobs.spawn`` starts the resume child in the resuming
process's working directory. ``analyze restamp --recursive`` (U93) makes the
path more than one segment. ``analyze run`` takes no such flag: its resume
marker is the head on the NAME, which a tree walk would not survive.

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

from cratekit.analysis import ahead, artifacts, detect, energy, light, vocals
from cratekit.cli.output import Envelope, load_config, no_job
from cratekit.core import config, discovery, jobs, naming, pool, tags
from cratekit.core import drift as drift_words
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import NameBudget, NameSpec, NameTemplate
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
    return list(discovery.scan_audio(folder).items)


def walk_folder(ctx) -> tuple[Path, bool, discovery.Scan, tuple[dict[str, str], ...]]:
    """The folder a queueing verb names, its walk, and the folders it left out."""
    folder = _folder_of(ctx.args.folder)
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=recursive)
    return folder, recursive, scan, discovery.walk_warnings(scan.skipped_links, scan.unreadable)


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
    """The files this drive will measure: unsettled items, present, with no head yet.

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
        if path.is_file() and not carries_head(path, cfg):
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
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        if job.handler_key == "analyze.restamp":
            warnings = (*warnings, DB_NOT_WRITTEN)
        else:
            # THE HEAD IS A MEASUREMENT WITH A KNOWN ERROR (R-744): rekordbox
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


def carries_head(path: Path, cfg: config.Config) -> bool:
    """Whether ``path``'s name carries the head, ``analyze run``'s resume marker.

    Named so ``crate analyze vocals --unscored`` picks exactly the files a run
    will never score again (U181, R-277).
    """
    return naming.has_head(path.name, template=_template(cfg))


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

    ``core.discovery.item_path`` refuses an id that would leave the folder: an
    absolute right hand side would discard the base silently (U93).
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

    A kill between the rename and the row flipping to done leaves a finished
    file under its head and a pending row under its old name. The answer
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
    folder, where ``_finalize`` renames to.
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
    with no librosa would skip every file as keyless and report done. The
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


def _finalize(cfg: config.Config, job, item, path: Path, scored: Mapping[str, Any]) -> Path:
    """Write the analysed values onto the file and rename it to its head.

    TAGS FIRST, THEN THE RENAME: a kill between leaves the head in the title,
    which ``naming.normalize_spec`` heals on the next pass. The intent is
    recorded before the file moves. An absent level or vocal score writes no
    tag, which routing reads as unscored. The drift level only when measured,
    its verdict whenever given (U157).
    """
    template = _template(cfg)
    camelot = str(scored["camelot"])
    key = naming.pad_camelot(camelot)
    # ``rate`` is the shipped detector's key and ``bpm`` the older fakes'.
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
        spec, template=template, budget=NameBudget.of(cfg.naming), parent_dir=str(path.parent)
    )
    fields = {
        "initialkey": key,
        "title": rendered.title_tag,
        "energylevel": scored.get("energy"),
        "voxlevel": scored.get("voxlevel"),
        "voxgender": scored.get("voxgender"),
        "voxgenderconf": scored.get("voxgenderconf"),
        "driftlevel": _drift_level(scored.get("drift")),
        "drift": scored.get("drift_verdict"),
    }
    _write_or_refuse(path, fields, untouched="The file is untouched and was not renamed")
    target = path.with_name(rendered.filename)
    if target == path:
        return path
    artifacts.record_rename_intent(cfg, job, item, target)
    if not naming.claim_target(target):
        # THE RENAME WILL NOT LAND, so the intent is false, and a retry once the source is gone would
        # read that unrelated file as this item's twin (U223).
        artifacts.discard_rename_evidence(cfg, job, item)
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
        artifacts.discard_rename_evidence(cfg, job, item)
        raise refuse(
            "analysis-write-failed",
            f"{path.name} could not be renamed to {rendered.filename}: {exc}",
            origin=_ORIGIN,
            detail={"path": str(path), "target": str(target), "stage": "rename"},
        ) from exc
    return target


def _drift_level(measured: Any) -> str | None:
    """A measured drift as its tag spells it, or None for no measurement (U157)."""
    if measured is None:
        return None
    return drift_words.shown(float(measured))


def handle_run(job, item, cfg) -> jobs.Produced:
    """Analyse ONE file, the per item worker behind ``analyze.run``.

    A name carrying the head is skipped unread. Otherwise the light head, the
    vocal score, then the finalize; a head with no key or no decode is a
    terminal skip with nothing written. The configuration is the frozen one
    (KTD9).
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
    # that did not land; this attempt starts clean and records its own if
    # it renames (U223).
    artifacts.discard_rename_evidence(cfg, job, item)
    if carries_head(path, cfg):
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
            "drift": scored.get("drift"),
            "drift_verdict": scored.get("drift_verdict"),
        },
    )


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
    _calibration_or_refuse(cfg)
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            # FROZEN WITH THE FOLDER: the resume never re-scans, so it reports
            # the tree the job was queued against.
            payload={"folder": str(folder), **discovery.frozen_walk(scan, recursive=recursive)},
            cfg=cfg,
            item_ids=list(scan.items),
        )
        if foreground.queue_only(ctx.args):
            return ctx.envelope(
                data=jobs.reported(store, job), warnings=(DB_NOT_WRITTEN, *extra)
            )
    # NOT ``extra`` AGAIN: the resume reads the walk's warnings off the payload.
    return _settle(ctx, cfg, job, restamp_argv(job))


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
