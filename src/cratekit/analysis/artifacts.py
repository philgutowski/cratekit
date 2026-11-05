"""Where one analysed file's report is staged, and where it lands.

The same five functions :mod:`cratekit.tagging.artifacts` carries, with the
analysis directory names, and the reasons are that module's: ``jobs.drive``
makes a produced file durable BEFORE the item's row flips to done, so a run
killed after six hundred decodes has six hundred reports to show for it, and
the report is the only record of what was deliberately NOT written, which is
where an honest energy absence and an unscored vocal pass have to land.

**THIS IS THE FOURTH COPY, RECORDED RATHER THAN HIDDEN** (KTD9x). Adoption,
outbound and tagging each carry one, and the honest home is one module in
``core`` taking the two directory names as arguments. That move is another
unit's files; the residual sits beside R-240. ``cratekit.core.artifacts`` is
now that module, landed by U57 with the directory names as parameters;
this copy is not yet migrated onto it.

**THE ROOT COMES FROM THE FROZEN CONFIGURATION, PASSED IN.** ``jobs.store_dir()``
with no argument loads the CURRENT configuration, which is the KTD9 defect
wearing an indirection the handler guard cannot see. Nothing here loads one.

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


def _job_dir(parent: str, cfg: config.Config, job_id: str) -> Path:
    return jobs.store_dir(cfg) / parent / job_id


def final_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Named after the ORDINAL, never the item, which is a filename with a suffix."""
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"


RENAME_INTENT_FILENAME = "rename-intent.json"


def _staging_dir(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    return _job_dir(STAGING_DIRNAME, cfg, job_id) / str(ordinal)


def _report_name(ordinal: int) -> str:
    return f"{ordinal:04d}.json"


def staged_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """A cleared staging directory for one attempt at one item.

    CLEARED OF EVERYTHING BUT THE RENAME INTENT (U223). A stale report from an
    earlier attempt never leaks into this one, but the intent is the resume's
    evidence and this call comes AFTER the rename, in the very attempt that
    renamed the file. The first version removed the whole directory here, so
    an interrupt landing between the staged report and the commit left a
    resume with the source gone and no intent, and the item failed for ever
    as ``source-missing`` over a file analysed and renamed on disk (A60's live
    run, #423). The intent is dropped where it is known false instead:
    :func:`discard_rename_intent`.
    """
    directory = _staging_dir(cfg, job_id, ordinal)
    if directory.is_dir() and not directory.is_symlink():
        for entry in directory.iterdir():
            if entry.name == RENAME_INTENT_FILENAME and entry.is_file():
                continue
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    elif directory.is_symlink() or directory.exists():
        # WHAT THE FIRST VERSION DID WITH ANYTHING ELSE AT THIS PATH, kept:
        # ``rmtree`` refuses a link and a plain file, loudly, rather than this
        # call deciding to remove or follow one.
        shutil.rmtree(directory)
    config._mkdir_private(directory)
    return directory / _report_name(ordinal)


def write(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def intent_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where one item's rename intent lives: in its staging directory.

    THE INTENT IS WRITTEN BEFORE THE RENAME AND OUTLIVES A KILL. The item is
    the pre rename name and the rename lands inside the handler, before the
    engine flips the row to done, so a kill in that window leaves a finished
    file under its head and a pending row under its old name. The intent is
    what lets the resume find the file the item BECAME rather than guessing
    from the folder, because a guess matched any headed file whose stripped
    stem equalled the item, which is an unrelated file when the source was
    deleted, and matched nothing when the template deduped or truncated the
    stem.

    IT OUTLIVES THE ATTEMPT THAT WROTE IT (U223). ``staged_path`` keeps it
    when it clears the directory for a report, so the attempt that renamed
    the file, and a resume interrupted in the same window, both leave it for
    the next. It is removed only where it is known false: a rename that did
    not land, and an attempt whose source is still a file.
    """
    return _staging_dir(cfg, job_id, ordinal) / RENAME_INTENT_FILENAME


def record_rename_intent(cfg: config.Config, job, item, target: Path) -> Path:
    path = intent_path(cfg, job.job_id, item.ordinal)
    config._mkdir_private(path.parent)
    return write(path, {"item": item.item_id, "target": str(target)})


def rename_intent(cfg: config.Config, job, item) -> Path | None:
    """The target this item's last attempt meant to rename it to, if recorded."""
    path = intent_path(cfg, job.job_id, item.ordinal)
    if not path.is_file():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    target = loaded.get("target")
    return Path(str(target)) if target else None


def discard_rename_intent(cfg: config.Config, job, item) -> None:
    """Drop this item's intent, once the rename it recorded is known not to stand.

    Left behind, an intent whose rename never landed names whatever later
    sits at that target, an unrelated file a person put there, as this
    item's twin once the source is gone.
    """
    intent_path(cfg, job.job_id, item.ordinal).unlink(missing_ok=True)


def staged_report(cfg: config.Config, job, item) -> dict[str, Any] | None:
    """This item's report, staged by an attempt whose row never moved, if any.

    Read in place and never cleared here. A report is staged only after the
    file was renamed, so it is the item's own record of the rename when the
    intent is gone, which is the state the shipped ``staged_path`` left
    every job interrupted in that window (U223). A report for another item,
    or one that does not parse to a mapping, is no report.
    """
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
    if not path.is_file():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded


def produced(cfg: config.Config, job, item, report: dict[str, Any]) -> jobs.Produced:
    return jobs.Produced(
        staged=write(staged_path(cfg, job.job_id, item.ordinal), report),
        final=final_path(cfg, job.job_id, item.ordinal),
    )


def committed(cfg: config.Config, job_id: str) -> tuple[dict[str, Any], ...]:
    """Every committed report for this job, in item order, read back off disk."""
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    if not directory.is_dir():
        return ()
    found: list[dict[str, Any]] = []
    # Only ordinal named files are reports. A stray ``notes.json`` beside them
    # once raised out of the sort key and took the whole resume envelope down
    # after every item had finished.
    reports = [path for path in directory.glob("*.json") if path.stem.isdigit()]
    for path in sorted(reports, key=lambda item: int(item.stem)):
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(loaded, dict):
            found.append(loaded)
    return tuple(found)


__all__ = [
    "ARTIFACTS_DIRNAME",
    "RENAME_INTENT_FILENAME",
    "STAGING_DIRNAME",
    "committed",
    "discard_rename_intent",
    "final_path",
    "intent_path",
    "produced",
    "record_rename_intent",
    "rename_intent",
    "staged_path",
    "staged_report",
    "write",
]
