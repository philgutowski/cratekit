"""Where one tagged file's report is staged, and where it lands.

Bound on :class:`cratekit.core.jobs.Artifacts`, the one home (U298), whose
configuration is passed in: ``tests/test_tag_workers.py`` parses this file to
guard that. Tagging's own are its two directory names, an order that keeps a
report named for no ordinal, a reader over every job that counts what it
could not read, and a commit for a writer that is not a job's worker.

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from cratekit.core import config, jobs

#: The directory under the queue root that holds committed item reports.
ARTIFACTS_DIRNAME = "tag-artifacts"

#: Where an attempt writes before the engine commits it, a sibling of the
#: final directory so ``jobs.commit_artifact``'s ``os.replace`` stays atomic.
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

    Read back, so a resumed sweep's report covers every file; one that cannot
    be parsed is skipped, since the summary is a display over work done.
    """
    return _REPORTS.committed(cfg, job_id, ordered=_in_item_order)


def _item_order(path: Path) -> tuple[int, int, str]:
    """A report's place among its job's: by its ordinal as a NUMBER.

    Four digits sort as text and the ten thousandth does not. A name that is
    no ordinal sorts after every one that is, by name, and never raises.
    """
    stem = path.stem
    return (0, int(stem), "") if stem.isdigit() else (1, 0, stem)


def _in_item_order(paths: Iterable[Path]) -> list[Path]:
    return sorted(paths, key=_item_order)


def _reports(directory: Path) -> tuple[tuple[dict[str, Any], ...], int]:
    """One job directory's reports in item order, and how many could not be read."""
    found: list[dict[str, Any]] = []
    unread = 0
    for path in _in_item_order(directory.glob("*.json")):
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

    Off the directory, not the queue (R-799), so a job the queue no longer
    lists is still read. The unread are counted, since a caller deciding which
    files a correction looks at must say how many it could not. Jobs in name
    order and reports in item order, which is not the order things happened.
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

    The engine's own staged commit, so a record written outside a drive is
    never left truncated. ``name`` is the directory the reports sit under.
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
