"""Where one adoption item's report is staged, and where it lands.

**WHY AN ARTIFACT AT ALL.** ``jobs.drive`` makes a handler's produced file
durable BEFORE it flips the item's row to done, and that ordering is the only
thing that survives a kill. Without a file, a scan that classified four thousand
rows and then died would have nothing to show for any of them, and an apply that
wrote memberships and then died would leave the applied ledger as the only
memory of what happened.

**UNDER THE QUEUE, NOT UNDER THE LIBRARY.** The queue root already holds a lock
and a log per job, so an item's report belongs beside them. Under the library it
would be a new kind of file for ``core/config``'s snapshot roles to classify, and
every one of those roles is a decision about what a rollback does.

**THE ROOT COMES FROM THE FROZEN CONFIGURATION.** ``jobs.store_dir()`` called
with no argument loads the CURRENT configuration, which is the KTD9 defect
wearing an indirection the handler guard in ``tests/test_handlers.py`` cannot
see: that guard reads three spellings of a reload inside the handler body and
cannot follow one through a helper. So the configuration is a parameter here and
this module never loads one.

**THIS IS THE SECOND COPY OF A GENERIC HELPER AND THAT IS RECORDED RATHER THAN
HIDDEN.** ``cratekit.modules.outbound.artifacts`` is the same five functions with
two different directory names. Nothing here is about adoption except those names,
so the honest home is one module in ``core`` that takes the names as arguments,
and moving the outbound one there is a change to another unit's file. Filed as a
residual instead of reached across for.

Layer: modules.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from cratekit.core import config, jobs

#: The directory under the queue root that holds committed item reports.
ARTIFACTS_DIRNAME = "adopt-artifacts"

#: Where an attempt writes before the engine commits it. A SIBLING of the final
#: directory rather than a temp directory, because ``jobs.commit_artifact`` is an
#: ``os.replace`` and that is atomic only within one filesystem.
STAGING_DIRNAME = "adopt-staging"


def _job_dir(parent: str, cfg: config.Config, job_id: str) -> Path:
    return jobs.store_dir(cfg) / parent / job_id


def final_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where this item's report belongs once the engine has committed it.

    THE ORDINAL RATHER THAN THE ITEM IDENTIFIER, because an item identifier here
    is a rekordbox row identifier or an adoption entry identifier and neither
    format constrains what may be in it, while an ordinal is an integer this
    queue assigned. A filename built from arbitrary library data is a path
    traversal wearing a report.
    """
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"


def staged_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """A cleared staging directory for one attempt at one item.

    CLEARED, because whatever is in it belongs to an attempt that did not finish.
    A half written report left behind would be committed by the next attempt as
    though it described that attempt.
    """
    directory = _job_dir(STAGING_DIRNAME, cfg, job_id) / str(ordinal)
    if directory.exists():
        shutil.rmtree(directory)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"


def write(path: Path, payload: dict[str, Any]) -> Path:
    """Serialize one item's report. Sorted keys so two runs produce one file."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def produced(cfg: config.Config, job, item, report: dict[str, Any]) -> jobs.Produced:
    """Stage one item's report and hand the engine both paths.

    ONE FUNCTION RATHER THAN THE SAME FOUR LINES IN EACH SHELL. The staging and
    the destination have to agree about the job and the ordinal, and two copies
    of that agreement is how one of them comes to write where the other does not
    look. The engine owns the flush-then-rename between the two paths, which is
    the ordering a handler must not be able to get wrong.
    """
    return jobs.Produced(
        staged=write(staged_path(cfg, job.job_id, item.ordinal), report),
        final=final_path(cfg, job.job_id, item.ordinal),
    )


def committed(cfg: config.Config, job_id: str) -> tuple[dict[str, Any], ...]:
    """Every committed report for this job, in item order.

    READ BACK RATHER THAN ACCUMULATED IN MEMORY, and the difference is what makes
    the reported summary true across a resume. A run that classified three of five
    rows and is continued tomorrow has two reports in memory and five on disk, and
    the person asking what the scan found means all five.

    A report that cannot be parsed is SKIPPED rather than raised on. The summary
    is a display over work that already happened and its artifacts are already
    committed; refusing to report would turn one unreadable file into a verb that
    cannot tell anybody anything about the whole job.
    """
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    if not directory.is_dir():
        return ()
    found: list[dict[str, Any]] = []
    # SORTED BY THE ORDINAL AS A NUMBER, not by the filename. The name is
    # ``{ordinal:04d}.json``, so four digits sort as text in item order and the
    # ten thousandth does not: ``"10000"`` sorts before ``"9999"``. A census over
    # a real library is tens of thousands of items, so this is reachable input
    # rather than a hypothesis. ``modules/outbound/artifacts`` has the same sort
    # and one item per playlist track, which is R-240's territory rather than
    # this unit's to reach across for.
    for path in sorted(directory.glob("*.json"), key=lambda item: int(item.stem)):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(parsed, dict):
            found.append(parsed)
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
