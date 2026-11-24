"""``crate analyze vocals``: re-score vocal tags, including on files already analysed.

R-277: ``analyze.run`` skips a file it already measured, its resume marker (its
mark since U343, or a head on the name before), so a track finalized with no
voxlevel is never scored again, and ``analyze.restamp`` rewrites energy only.
This verb scores every audio file, measured or not, and writes only the three
vocal tags.

THE MODEL MODULE IS NEVER IMPORTED AT MODULE SCOPE: ``cli.jobs.argv_for``
imports this module to build a resume line, and the model imports torch,
which the slim profile does not declare. The item is a path relative to the
frozen absolute folder, for the reason ``cratekit.analysis.cli`` states, and
``--recursive`` (U93) walks the library in one job through ``core.discovery``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from cratekit.analysis import artifacts
from cratekit.analysis import cli as analysis_cli
from cratekit.analysis import vocals as scoring
from cratekit.cli.output import Envelope, load_config
from cratekit.core import config, discovery, jobs, tags
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy

_ORIGIN = ("vocals", "cli")

#: Every file the folder held carries a vocal score already, so ``--unscored``
#: queued nothing (U181).
NONE_UNSCORED = "none-unscored"

#: The flag that queues only what ``analyze run`` will never score again.
UNSCORED = "--unscored"


def _require_extra() -> None:
    """Refuse when the model cannot load here and no fake loader is bound.

    ``scoring.missing_requirement`` names the first missing piece, so a job
    that could score nothing is refused before it is filed (R-370).
    """
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if missing is None:
        return
    raise refuse(
        "module-extras-missing",
        f"scoring vocals cannot start in the process running this job: {missing}",
        remedy=Remedy.INSTALL_MODULE_EXTRA,
        origin=_ORIGIN,
        detail={"extras": "vocals", "install": scoring.install(), "missing": missing},
    )


def _bind_defaults() -> None:
    if scoring.loader_bound():
        return
    from cratekit.analysis import vocal

    scoring.bind_loader(vocal.default_loader)


def _write_or_refuse(path: Path, fields: dict[str, Any]) -> None:
    try:
        written = tags.write_tags(path, fields)
    except tags.UnsupportedContainer as exc:
        raise refuse(
            "analysis-write-failed",
            f"the vocal scores cannot be written onto {path.name}: {exc}. "
            f"The file is untouched",
            origin=_ORIGIN,
            detail={"path": str(path), "stage": "tags", "kind": type(exc).__name__},
        ) from exc
    if not written:
        raise refuse(
            "analysis-write-failed",
            f"the vocal scores could not be written onto {path.name}. "
            f"The file is untouched",
            origin=_ORIGIN,
            detail={"path": str(path), "stage": "tags"},
        )


def _folder_and_path(job, item) -> tuple[Path, Path]:
    """The frozen folder and the item's file in it, joined by the checked rule.

    ``discovery.item_path`` rather than an operator, which an absolute id would
    turn into a file the job never queued (U93).
    """
    folder = Path(str((job.payload or {}).get("folder") or ""))
    return folder, discovery.item_path(folder, str(item.item_id))


def _item_path(job, item) -> Path:
    folder, path = _folder_and_path(job, item)
    if not path.is_file():
        raise refuse(
            "source-missing",
            f"{path} is no longer a file, so there is nothing to score for this "
            f"item. Nothing was read and nothing was written",
            steps=(
                "run the vocals verb again over the folder as it now stands; "
                "this job was queued against a folder that has since changed",
            ),
            origin=_ORIGIN,
            detail={"item": item.item_id, "folder": str(folder)},
        )
    return path


def _unscored_warning(summary: Mapping[str, Any]) -> dict[str, str] | None:
    return scoring.unscored_warning(summary, verb="scored")


def build(parser, entry) -> None:
    del entry
    parser.add_argument("folder", help="folder of audio to score for vocals")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help=(
            "queue every folder under this one as a single resumable job, "
            "instead of only the tracks directly inside it"
        ),
    )
    parser.add_argument(
        UNSCORED,
        action="store_true",
        help=(
            "queue only the files crate analyze run already measured and which "
            "carry no voxlevel, the ones it finalized with no vocal score and now skips"
        ),
    )
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the vocals job already queued under this identifier",
    )
    parser.set_defaults(_handler=analyze_vocals)


def _unscored(cfg: config.Config, folder: Path, items: tuple[str, ...]) -> list[str]:
    """The items ``analyze run`` will never score again: measured, and no voxlevel (U181).

    Measured is the run's own resume marker, its mark or a head on the name
    (U343). A file not yet measured is the run's to analyse, and one carrying a
    score is left alone.
    """
    chosen = []
    for item in items:
        path = discovery.item_path(folder, item)
        if analysis_cli.already_measured(path, cfg) and tags.read_vox_from_file(path) is None:
            chosen.append(item)
    return chosen


def vocals_argv(job) -> list[str]:
    folder = job.payload.get("folder", "")
    return ["analyze", "vocals", folder, "--job", job.job_id]


def _advance(ctx, store, job):
    """Reconcile, refuse an empty or foreign job, run it, raise if it failed."""
    job = jobs.reconcile(store, job.job_id)
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not "
            f"a vocals restamp, so this verb will not drive it",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=(
                "resume this job through the verb that queued it, or through the "
                "job resume verb, which reads the worker off the job itself",
            ),
            origin=_ORIGIN,
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no items to run, so driving it would report "
                f"a vocal restamp over a folder it never read. It was queued by a "
                f"build that did not record what its items were",
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
        summary = analysis_cli.committed_summary(cfg, job.job_id)
        # THE RESUME CARRIES THE WALK'S OMISSIONS TOO, off the frozen payload.
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        unscored = _unscored_warning(summary)
        if unscored is not None:
            warnings = (*warnings, unscored)
        return ctx.envelope(
            data=jobs.reported(store, job, {"analysis": summary}),
            warnings=warnings,
        )


def analyze_vocals(ctx) -> Envelope:
    cfg = load_config(_ORIGIN)
    if ctx.args.job:
        return _resume(ctx, cfg)
    folder, recursive, scan, extra = analysis_cli.walk_folder(ctx)
    if not scan.items:
        return analysis_cli.nothing_to_queue(ctx, folder, extra)
    items = list(scan.items)
    unscored = bool(getattr(ctx.args, "unscored", False))
    if unscored:
        items = _unscored(cfg, folder, scan.items)
        if not items:
            return analysis_cli.nothing_to_queue(ctx, folder, extra, state=NONE_UNSCORED)
    _require_extra()
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            # FROZEN WITH THE FOLDER: the resume replays the store, never a scan.
            payload={
                "folder": str(folder),
                **discovery.frozen_walk(scan, recursive=recursive),
                **({"unscored": True} if unscored else {}),
            },
            cfg=cfg,
            item_ids=items,
        )
        return ctx.envelope(data=jobs.reported(store, job), warnings=extra)


def handle(job, item, cfg) -> jobs.Produced:
    """Score ONE file's vocals and stamp the three vocal tags.

    A Camelot-prefixed name is NOT skipped. That skip is ``analyze.run``'s
    resume marker and is the whole of R-277. This worker scores the file
    that is already there, writes voxlevel, voxgender and voxgenderconf,
    and renames nothing.
    """
    path = _item_path(job, item)
    _require_extra()
    _bind_defaults()
    previous_level = tags.read_vox_from_file(path)
    previous_gender = tags.read_voxgender_from_file(path)
    previous_conf = analysis_cli.as_level(tags.read_tag(path, "voxgenderconf"))
    scored = scoring.analyse({"path": str(path)})
    if not scored.get("vocal_active"):
        return artifacts.produced(
            cfg,
            job,
            item,
            {
                "item": item.item_id,
                "path": str(path),
                "status": "inactive",
                "vocal_active": False,
                "vocal_reason": scored.get("vocal_reason"),
                "previous": previous_level,
                "voxlevel": None,
                "voxgender": None,
                "written": False,
            },
        )
    level = scored.get("voxlevel")
    gender = scored.get("voxgender")
    conf = scored.get("voxgenderconf")
    written = False
    if (previous_level, previous_gender, previous_conf) != (level, gender, conf):
        _write_or_refuse(
            path,
            {"voxlevel": level, "voxgender": gender, "voxgenderconf": conf},
        )
        written = True
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "item": item.item_id,
            "path": str(path),
            "status": "scored" if written else "unchanged",
            "vocal_active": True,
            "vocal_reason": None,
            "previous": previous_level,
            "voxlevel": level,
            "voxgender": gender,
            "written": written,
        },
    )
