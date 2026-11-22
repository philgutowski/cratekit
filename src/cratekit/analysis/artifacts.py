"""Where one analysed file's report is staged, and where it lands.

The base is :class:`cratekit.core.jobs.Artifacts`. The report is also the only
record of what was deliberately NOT written, an honest energy absence or an
unscored vocal pass. Analysis's own: the two directory names, a staging
directory that keeps an interrupted rename's evidence, and a run's pool record.

Layer: modules.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from cratekit.core import config, jobs

ARTIFACTS_DIRNAME = "analysis-artifacts"
#: A SIBLING of the final directory, because ``jobs.commit_artifact`` is an
#: ``os.replace`` and that is atomic only within one filesystem.
STAGING_DIRNAME = "analysis-staging"

#: Staging is this module's own (U298): it keeps an interrupted rename's
#: evidence, which the base's cleared directory would not.
_REPORTS = jobs.Artifacts(final=ARTIFACTS_DIRNAME, staging=STAGING_DIRNAME)
final_path, committed, write = _REPORTS.final_path, _REPORTS.committed, _REPORTS.write


RENAME_INTENT_FILENAME = "rename-intent.json"


def _staging_dir(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    return _REPORTS.staging_dir(cfg, job_id) / str(ordinal)


def _report_name(ordinal: int) -> str:
    return f"{ordinal:04d}.json"


def staged_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """A cleared staging directory for one attempt at one item.

    CLEARED OF EVERYTHING BUT THE RENAME INTENT (U223): this call comes after
    the rename in the attempt that renamed, so removing the intent would leave
    an interrupted resume with the source gone and no evidence. The intent is
    dropped where it is known false, :func:`discard_rename_evidence`.
    """
    directory = _staging_dir(cfg, job_id, ordinal)
    if directory.is_dir() and not directory.is_symlink():
        for entry in directory.iterdir():
            if (
                entry.name == RENAME_INTENT_FILENAME
                and entry.is_file()
                and not entry.is_symlink()
            ):
                continue
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    elif directory.is_symlink() or directory.exists():
        # ``rmtree`` refuses a link and a plain file, loudly, rather than this
        # call deciding to remove or follow one.
        shutil.rmtree(directory)
    config.mkdir_private(directory)
    return directory / _report_name(ordinal)


def intent_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where one item's rename intent lives: in its staging directory.

    Written before the rename, so a kill between the rename and the row
    flipping to done leaves the resume the file the item BECAME, never a guess
    from the folder. It outlives the attempt (U223) and is removed only where
    known false: a rename that did not land, or a source still a file.
    """
    return _staging_dir(cfg, job_id, ordinal) / RENAME_INTENT_FILENAME


def record_rename_intent(cfg: config.Config, job, item, target: Path) -> Path:
    path = intent_path(cfg, job.job_id, item.ordinal)
    config.mkdir_private(path.parent)
    return write(path, {"item": item.item_id, "target": str(target)})


def _item_record(path: Path, item) -> dict[str, Any] | None:
    """The mapping ``path`` holds for this item, or None when it holds none."""
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded


def rename_intent(cfg: config.Config, job, item) -> Path | None:
    """The target this item's last attempt meant to rename it to, if recorded.

    A link is no record: it would name whatever its far end says as the twin.
    """
    path = intent_path(cfg, job.job_id, item.ordinal)
    if path.is_symlink() or not path.is_file():
        return None
    target = (_item_record(path, item) or {}).get("target")
    return Path(str(target)) if target else None


def discard_rename_evidence(cfg: config.Config, job, item) -> None:
    """Drop this item's intent AND its staged report, once neither can be true.

    Called where the rename is known not to stand. Left behind, either would
    name whatever later sits at that target as this item's twin. The report
    goes too because :func:`staged_report` is read as the same proof.
    """
    directory = _staging_dir(cfg, job.job_id, item.ordinal)
    if directory.is_symlink() or not directory.is_dir():
        # NOT THROUGH A LINK: its far end is not this item's staging, and
        # ``staged_path`` refuses the link loudly when the attempt reaches it.
        return
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
        entry = directory / name
        # A DIRECTORY AT EITHER NAME IS LEFT for ``staged_path`` to remove; an
        # ``unlink`` would fail the item for good.
        if entry.is_symlink() or not entry.is_dir():
            entry.unlink(missing_ok=True)


def staged_report(cfg: config.Config, job, item) -> dict[str, Any] | None:
    """This item's report, staged by an attempt whose row never moved, if any.

    Read in place, never cleared. A report that says it renamed is staged only
    after the rename, so it is the item's record when the intent is gone
    (U223). Another item's report, a non mapping, or a link is no report.
    """
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
    if path.is_symlink() or not path.is_file():
        return None
    return _item_record(path, item)


def produced(cfg: config.Config, job, item, report: dict[str, Any]) -> jobs.Produced:
    return jobs.Produced(
        staged=write(staged_path(cfg, job.job_id, item.ordinal), report),
        final=final_path(cfg, job.job_id, item.ordinal),
    )


#: The run's pool, beside the item reports (U241). Not an ordinal, so
#: :func:`committed` never reads it as a report.
POOL_FILENAME = "pool.json"


def record_pool(cfg: config.Config, job_id: str, record: dict[str, Any]) -> Path:
    """Write what pool the job's last drive ran with, replacing the one before.

    A file, so a resume of a finished job can still say it. Written to a
    sibling and moved into place, so a reader never meets half of it.
    """
    directory = _REPORTS.final_dir(cfg, job_id)
    config.mkdir_private(directory)
    target = directory / POOL_FILENAME
    staged = directory / f".{POOL_FILENAME}.writing"
    write(staged, record)
    staged.replace(target)
    return target


def pool_record(cfg: config.Config, job_id: str) -> dict[str, Any] | None:
    """The pool the job's last drive ran with, or None when none was recorded.

    A link or a file that is not a mapping is no record: an absent line on
    the answer, never an invented one.
    """
    path = _REPORTS.final_dir(cfg, job_id) / POOL_FILENAME
    if path.is_symlink() or not path.is_file():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return loaded if isinstance(loaded, dict) else None


__all__ = [
    "ARTIFACTS_DIRNAME",
    "POOL_FILENAME",
    "RENAME_INTENT_FILENAME",
    "STAGING_DIRNAME",
    "committed",
    "discard_rename_evidence",
    "final_path",
    "intent_path",
    "pool_record",
    "produced",
    "record_pool",
    "record_rename_intent",
    "rename_intent",
    "staged_path",
    "staged_report",
    "write",
]
