"""Where one tagged file's report is staged, and where it lands.

The base is :class:`cratekit.core.jobs.Artifacts`, which says why an item has a
report at all, why it sits under the queue and why the configuration is passed
in: ``tests/test_tag_workers.py`` guards that last by parsing this file and the
base. What is tagging's own is the two directory names, a reader that counts
what it could not read, a reader over every job, and a commit for a writer
that is not a job's worker.

Layer: modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cratekit.core import config, jobs

#: The directory under the queue root that holds committed item reports.
ARTIFACTS_DIRNAME = "tag-artifacts"

#: Where an attempt writes before the engine commits it. A SIBLING of the final
#: directory rather than a temp directory, because ``jobs.commit_artifact`` is an
#: ``os.replace`` and that is atomic only within one filesystem.
STAGING_DIRNAME = "tag-staging"


#: The four names every caller here uses, bound to this feature's two
#: directories on the one base ``core.jobs`` holds (U298).
_REPORTS = jobs.Artifacts(final=ARTIFACTS_DIRNAME, staging=STAGING_DIRNAME)
final_path, staged_path, produced, write = (
    _REPORTS.final_path,
    _REPORTS.staged_path,
    _REPORTS.produced,
    _REPORTS.write,
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
    directory = _REPORTS.final_dir(cfg, job_id)
    if not directory.is_dir():
        return ()
    return _reports(directory)[0]


def _item_order(path: Path) -> tuple[int, int, str]:
    """A report's place among its job's: by its ordinal as a NUMBER.

    SORTED BY THE ORDINAL AS A NUMBER, not by the filename. The name is
    ``{ordinal:04d}.json``, so four digits sort as text in item order and the
    ten thousandth does not: ``"10000"`` sorts before ``"9999"``. One item is
    one audio file here, and a folder holding ten thousand of them is a normal
    download directory rather than a hypothesis.

    A file whose name is no ordinal sorts after every one that is, by name,
    and is never a reason to raise: one stray file must not hide the rest.
    """
    stem = path.stem
    return (0, int(stem), "") if stem.isdigit() else (1, 0, stem)


def _reports(directory: Path) -> tuple[tuple[dict[str, Any], ...], int]:
    """One job directory's reports in item order, and how many could not be read.

    The one parse loop both readers below use, so they cannot come to disagree
    about which files are reports or what order they are in.
    """
    found: list[dict[str, Any]] = []
    unread = 0
    for path in sorted(directory.glob("*.json"), key=_item_order):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            unread += 1
            continue
        if not isinstance(parsed, dict):
            unread += 1
            continue
        found.append(parsed)
    return tuple(found), unread


def every_committed(cfg: config.Config) -> tuple[tuple[tuple[str, dict[str, Any]], ...], int]:
    """Every committed report of every job, with its job, and how many were unread.

    OFF THE DIRECTORY AND NOT OFF THE QUEUE (R-799). A reader that asks what
    tagging jobs ever wrote onto a file must not lose a job the queue no longer
    lists, since a job it cannot see is a file it never looks at and reports
    nothing about. Both tagging verbs commit here, and a reader tells their
    reports apart by what each carries.

    THE UNREAD ARE COUNTED, where :func:`committed` skips them. That function
    is a display over one job's work. This one is read to decide which files a
    correction looks at, so a report that cannot be parsed is a file that
    might have needed one, and the caller has to be able to say how many.

    Jobs in name order and reports in item order, so two reads of one
    unchanged queue agree and a digest over the result is stable. THE ORDER IS
    NOT THE ORDER THINGS HAPPENED IN: a job's name says nothing about when it
    ran, and a reader must not take the last report for the latest.
    """
    root = jobs.store_dir(cfg) / ARTIFACTS_DIRNAME
    if not root.is_dir():
        return (), 0
    found: list[tuple[str, dict[str, Any]]] = []
    unread = 0
    for directory in sorted(entry for entry in root.iterdir() if entry.is_dir()):
        reports, skipped = _reports(directory)
        unread += skipped
        found.extend((directory.name, report) for report in reports)
    return tuple(found), unread


def commit(cfg: config.Config, name: str, ordinal: int, report: dict[str, Any]) -> Path:
    """Stage one report and put it in place, for a writer that is not a job's worker.

    THE ENGINE'S OWN COMMIT, flush then rename then flush the directory, so a
    record written outside a drive is as whole as one written inside it. A
    writer that went straight to the final path could be killed half way and
    leave a truncated report every later reader counts as unread for good.
    ``name`` is the directory the reports sit under, where a job's identifier
    goes for a worker.
    """
    staged = write(staged_path(cfg, name, ordinal), report)
    return jobs.commit_artifact(staged, final_path(cfg, name, ordinal))


__all__ = [
    "ARTIFACTS_DIRNAME",
    "STAGING_DIRNAME",
    "commit",
    "committed",
    "every_committed",
    "final_path",
    "produced",
    "staged_path",
    "write",
]
