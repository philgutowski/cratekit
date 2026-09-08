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
unit's files; the residual sits beside R-240.

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


def staged_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """A cleared staging directory for one attempt at one item."""
    directory = _job_dir(STAGING_DIRNAME, cfg, job_id) / str(ordinal)
    if directory.exists():
        shutil.rmtree(directory)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"


def write(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


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
    for path in sorted(directory.glob("*.json"), key=lambda item: int(item.stem)):
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(loaded, dict):
            found.append(loaded)
    return tuple(found)


__all__ = [
    "ARTIFACTS_DIRNAME",
    "STAGING_DIRNAME",
    "committed",
    "final_path",
    "produced",
    "staged_path",
    "write",
]
