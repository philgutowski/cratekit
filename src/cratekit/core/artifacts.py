"""Where one queued item's report is staged, and where it lands. Generic.

**WHY A FILE PER ITEM AT ALL.** ``jobs.drive`` makes a handler's produced file
durable BEFORE it flips the item's row to done, and that ordering is the only
part of a run that survives a kill. Without it, a run that asked a paid service
six hundred questions and then died would have nothing to show for any of them,
and the next run would ask all six hundred again. The report is also the only
record of the items that were deliberately NOT written, which is what R16 asks
for: a skip reason has to reach the job's artifact and the verb's report, and an
in-memory count cannot survive to either.

**UNDER THE QUEUE, NOT UNDER THE LIBRARY.** The queue root already holds a lock
and a log per job, so an item's report belongs beside them. Under the library it
would be a new kind of file for ``core/config``'s snapshot roles to classify, and
every one of those roles is a decision about what a rollback does to it.

**THE ROOT COMES FROM THE FROZEN CONFIGURATION, PASSED IN.** ``jobs.store_dir()``
called with no argument loads the CURRENT configuration, which is the KTD9
defect wearing an indirection the handler guard in ``tests/test_handlers.py``
cannot see. So the configuration is a parameter here and this module never
loads one.

**THIS IS THE HOME THE FOUR FEATURE COPIES NAME.** Four feature packages each
carry an ``artifacts`` module that is these same five functions with their own
directory names, and each records that the honest home is one module in
``core`` taking the names as arguments. This is that module. The DIRECTORY
NAMES ARE PARAMETERS rather than constants because a core module may not name
a feature package, even as a string (KTD23, and the layering guard reads
strings), which is also why the four are not named here. They are not migrated
here either: each is another unit's files, and a migration is a rename that
moves where a committed report is read from. Each copy's docstring now points
at this module so the next worker reaches for it rather than for a fifth copy.

Layer: core.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.core import config, jobs


@dataclass(frozen=True, slots=True)
class Location:
    """The two directory names under the queue root one feature's reports use.

    ``final`` holds committed reports, ``staging`` holds attempts. A SIBLING of
    the final directory rather than a temp directory, because
    ``jobs.commit_artifact`` is an ``os.replace`` and that is atomic only within
    one filesystem.
    """

    final: str
    staging: str

    def __post_init__(self) -> None:
        for name in (self.final, self.staging):
            if not name or "/" in name or name in {".", ".."}:
                raise ValueError(
                    f"{name!r} is not a directory name; a report location is one "
                    f"path component under the queue root"
                )
        if self.final == self.staging:
            raise ValueError(
                "the staging and final directories must differ, or a commit is an "
                "os.replace of a file onto itself"
            )


def _job_dir(parent: str, cfg: config.Config, job_id: str) -> Path:
    return jobs.store_dir(cfg) / parent / job_id


def final_path(where: Location, cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """Where this item's report belongs once the engine has committed it.

    THE ORDINAL RATHER THAN THE ITEM IDENTIFIER, and it is not a precaution. An
    item identifier is whatever the queueing verb chose, and two of the three
    feature copies record why theirs could not be a filename: one is a path with
    separators and possibly ``..`` in it, the other a database row identifier.
    An ordinal is an integer this queue assigned.
    """
    directory = _job_dir(where.final, cfg, job_id)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"


def staged_path(where: Location, cfg: config.Config, job_id: str, ordinal: int) -> Path:
    """A cleared staging directory for one attempt at one item.

    CLEARED, because whatever is in it belongs to an attempt that did not finish.
    A half written report left behind would be committed by the next attempt as
    though it described that attempt, which is a report that is wrong rather than
    one that is missing.
    """
    directory = _job_dir(where.staging, cfg, job_id) / str(ordinal)
    if directory.exists():
        shutil.rmtree(directory)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"


def write(path: Path, payload: dict[str, Any]) -> Path:
    """Serialize one item's report. Sorted keys so two runs produce one file."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def produced(
    where: Location, cfg: config.Config, job, item, report: dict[str, Any]
) -> jobs.Produced:
    """Stage one item's report and hand the engine both paths.

    ONE FUNCTION RATHER THAN THE SAME FOUR LINES IN EACH WORKER. The staging path
    and the destination have to agree about the job and the ordinal, and two
    copies of that agreement is how one of them comes to write where the other
    does not look. The engine owns the flush-then-rename between the two.
    """
    return jobs.Produced(
        staged=write(staged_path(where, cfg, job.job_id, item.ordinal), report),
        final=final_path(where, cfg, job.job_id, item.ordinal),
    )


def committed(where: Location, cfg: config.Config, job_id: str) -> tuple[dict[str, Any], ...]:
    """Every committed report for this job, in item order.

    READ BACK RATHER THAN ACCUMULATED IN MEMORY, which is what makes a report
    true across a resume: the person asking what the run did means every item,
    including the ones a previous process finished.

    A report that cannot be parsed is SKIPPED rather than raised on. The summary
    is a display over work that already happened and whose artifacts are already
    committed, so refusing to report would turn one unreadable file into a verb
    that can tell a person nothing about any of the others.
    """
    directory = _job_dir(where.final, cfg, job_id)
    if not directory.is_dir():
        return ()
    found: list[dict[str, Any]] = []
    # ONLY ORDINAL NAMED FILES ARE REPORTS, and the filter runs before the sort
    # key does. A stray ``notes.json`` beside them once raised out of the sort
    # key in a feature copy and took the whole resume envelope down after every
    # item had finished, which is the promise two lines up broken by the line
    # that was meant to keep it.
    reports = [path for path in directory.glob("*.json") if path.stem.isdigit()]
    # SORTED BY THE ORDINAL AS A NUMBER, not by the filename: four digits sort as
    # text in item order and the ten thousandth does not.
    for path in sorted(reports, key=lambda item: int(item.stem)):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(parsed, dict):
            found.append(parsed)
    return tuple(found)


__all__ = [
    "Location",
    "committed",
    "final_path",
    "produced",
    "staged_path",
    "write",
]
