"""``crate analyze vocals``: re-score vocal tags, including Camelot-prefixed names.

R-277. ``analyze.run`` skips a name that already carries the head, which is
the resume marker, so a track finalized with no voxlevel is never scored
again. ``analyze.restamp`` rewrites energy only. This verb is the source
system's force path: it scores every audio file in the folder, head or
not, and writes only the three vocal tags.

THE MODEL MODULE IS NEVER IMPORTED AT MODULE SCOPE. ``cli.jobs.argv_for``
imports this module by name to build a resume line, and the model imports
torch at load time, which the slim profile does not declare. A worker
binds the shipped loader inside the function that needs it. Tests bind a
fake the same way ``analyze.run`` does.

THE ITEM IS A FILENAME, RELATIVE TO THE FROZEN FOLDER, AND THE FOLDER IS
FROZEN ABSOLUTE, for the same resume reason ``cratekit.analysis.cli``
states: ``jobs.spawn`` starts the child in the resuming process's working
directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from cratekit.analysis import artifacts
from cratekit.analysis import vocals as scoring
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS

_ORIGIN = ("vocals", "cli")

INSTALL = "pip install 'cratekit[vocals]'"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=_ORIGIN,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _reported(store, job, extra: Mapping[str, Any] | None = None) -> dict:
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
    return {"job_id": "", "state": state, "cause": None, "progress": {}}


def _folder_of(named: str) -> Path:
    return Path(named).expanduser().absolute()


def _audio_in(folder: Path) -> list[str]:
    """Audio filenames in the folder, sorted, not recursive, no dotfiles."""
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


def extra_available() -> bool:
    """Whether the vocals extra is importable in this process."""
    try:
        import panns_inference  # noqa: F401
        import torch  # noqa: F401
    except ImportError:
        return False
    return True


def _require_extra() -> None:
    """Refuse when the extra is absent here and no fake loader is bound."""
    if scoring.loader_bound() or extra_available():
        return
    raise refuse(
        "module-extras-missing",
        "scoring vocals needs the 'vocals' extra, and it is not installed in "
        "the process running this job",
        remedy=Remedy.INSTALL_MODULE_EXTRA,
        origin=_ORIGIN,
        detail={"extras": "vocals", "install": INSTALL},
    )


def _bind_defaults() -> None:
    if scoring.loader_bound():
        return
    from cratekit.analysis import vocal

    scoring.bind_loader(vocal.default_loader)


def _as_level(text: str | None) -> int | None:
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        return None


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
    folder = Path(str((job.payload or {}).get("folder") or ""))
    return folder, folder / item.item_id


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


def _summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
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


def _unscored_warning(summary: Mapping[str, Any]) -> dict[str, str] | None:
    count = int(summary.get("by_vocal_reason", {}).get(scoring.REASON_MODEL_UNAVAILABLE, 0))
    if not count:
        return None
    return {
        "code": scoring.REASON_MODEL_UNAVAILABLE,
        "message": (
            f"{count} track(s) were scored with no vocal model loaded and carry "
            f"no voxlevel; the model needs the 'vocals' extra, {INSTALL}"
        ),
    }


def build(parser, entry) -> None:
    del entry
    parser.add_argument("folder", help="folder of audio to score for vocals")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the vocals job already queued under this identifier",
    )
    parser.set_defaults(_handler=analyze_vocals)


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
    if not job.is_open() and job.cause is not None:
        raise CratekitError(job.cause)
    return job, warnings


def _resume(ctx, cfg: config.Config) -> Envelope:
    with jobs.open_store() as store:
        job, warnings = _advance(ctx, store, jobs.get(store, ctx.args.job))
        summary = _summary(cfg, job.job_id)
        unscored = _unscored_warning(summary)
        if unscored is not None:
            warnings = (*warnings, unscored)
        return ctx.envelope(
            data=_reported(store, job, {"analysis": summary}),
            warnings=warnings,
        )


def analyze_vocals(ctx) -> Envelope:
    cfg = _load()
    if ctx.args.job:
        return _resume(ctx, cfg)
    folder = _folder_of(ctx.args.folder)
    items = _audio_in(folder)
    if not items:
        return _nothing_to_queue(ctx, folder)
    _require_extra()
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            cfg=cfg,
            item_ids=items,
        )
        return ctx.envelope(data=_reported(store, job))


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
    previous_conf = _as_level(tags.read_tag(path, "voxgenderconf"))
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
