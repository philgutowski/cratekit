"""Where one tagged file's report is staged, and where it lands.

**WHY A FILE PER ITEM AT ALL.** ``jobs.drive`` makes a handler's produced file
durable BEFORE it flips the item's row to done, and that ordering is the only
part of a sweep that survives a kill. Without it, a run that read the catalogue
for six hundred files and then died would have nothing to show for any of them,
and the next run would ask the catalogue all six hundred questions again. The
report is also the only record of the files that were deliberately NOT written,
which is what R16 asks for: a skip reason has to reach the job's artifact and the
verb's report, and an in-memory count cannot survive to either.

**UNDER THE QUEUE, NOT UNDER THE LIBRARY.** The queue root already holds a lock
and a log per job, so an item's report belongs beside them. Under the library it
would be a new kind of file for ``core/config``'s snapshot roles to classify, and
every one of those roles is a decision about what a rollback does to it.

**THE ROOT COMES FROM THE FROZEN CONFIGURATION, PASSED IN.** ``jobs.store_dir()``
called with no argument loads the CURRENT configuration, which is the KTD9 defect
wearing an indirection the handler guard in ``tests/test_handlers.py`` cannot see:
that guard reads spellings of a reload inside a handler BODY and cannot follow one
through a helper. So the configuration is a parameter here and this module never
loads one. ``tests/test_tag_workers.py`` guards the call shape by parsing this
file, because the queue is installation scoped and no behaviour distinguishes the
two calls today.

**THIS IS THE THIRD COPY OF A GENERIC HELPER AND THAT IS RECORDED RATHER THAN
HIDDEN.** :mod:`cratekit.adopt.artifacts` and
:mod:`cratekit.modules.outbound.artifacts` are the same five functions with
different directory names. Nothing here is about tagging except those two names,
so the honest home is one module in ``core`` taking them as arguments, and moving
either of the other two there is another unit's files. Filed as a residual beside
R-240 rather than reached across for (KTD9x).
 ``cratekit.core.artifacts`` is now that module, landed by U57 with the
directory names as parameters; this copy is not yet migrated onto it.

Layer: modules.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from cratekit.core import config, jobs

#: The directory under the queue root that holds committed item reports.
ARTIFACTS_DIRNAME = "tag-artifacts"

#: Where an attempt writes before the engine commits it. A SIBLING of the final
#: directory rather than a temp directory, because ``jobs.commit_artifact`` is an
#: ``os.replace`` and that is atomic only within one filesystem.
STAGING_DIRNAME = "tag-staging"


def _job_dir(parent: str, cfg: config.Config, job_id: str) -> Path:
    return jobs.store_dir(cfg) / parent / job_id


def final_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where this item's report belongs once the engine has committed it.

    THE ORDINAL RATHER THAN THE ITEM IDENTIFIER, and here that is not a
    precaution. A tagging item identifier is a file path relative to the folder
    being swept, so it holds separators as a matter of course and may hold ``..``
    as well, which makes a filename built from it a path traversal wearing a
    report. An ordinal is an integer this queue assigned. The adoption copy of
    this helper states the same rule against a database row identifier, where it
    was easier to take on faith.
    """
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"


def staged_path(cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """A cleared staging directory for one attempt at one item.

    CLEARED, because whatever is in it belongs to an attempt that did not finish.
    A half written report left behind would be committed by the next attempt as
    though it described that attempt, which is a report that is wrong rather than
    one that is missing.
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

    ONE FUNCTION RATHER THAN THE SAME FOUR LINES IN EACH WORKER. The staging path
    and the destination have to agree about the job and the ordinal, and two
    copies of that agreement is how one of them comes to write where the other
    does not look. The engine owns the flush-then-rename between the two, which is
    the ordering a worker must not be able to get wrong.
    """
    return jobs.Produced(
        staged=write(staged_path(cfg, job.job_id, item.ordinal), report),
        final=final_path(cfg, job.job_id, item.ordinal),
    )


def committed(cfg: config.Config, job_id: str) -> tuple[dict[str, Any], ...]:
    """Every committed report for this job, in item order.

    READ BACK RATHER THAN ACCUMULATED IN MEMORY, and the difference is what makes
    a tagging report true across a resume. A sweep that wrote genres onto three
    hundred of a thousand files and is continued tomorrow has seven hundred
    reports in memory and a thousand on disk, and the person asking what the sweep
    did means all thousand.

    A report that cannot be parsed is SKIPPED rather than raised on. The summary
    is a display over work that already happened and whose artifacts are already
    committed, so refusing to report would turn one unreadable file into a verb
    that can tell a person nothing about any of the others.
    """
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    if not directory.is_dir():
        return ()
    found: list[dict[str, Any]] = []
    # SORTED BY THE ORDINAL AS A NUMBER, not by the filename. The name is
    # ``{ordinal:04d}.json``, so four digits sort as text in item order and the
    # ten thousandth does not: ``"10000"`` sorts before ``"9999"``. One item is
    # one audio file here, and a folder holding ten thousand of them is a normal
    # download directory rather than a hypothesis.
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
