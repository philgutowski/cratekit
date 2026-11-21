"""Where one adoption item's report is staged, and where it lands.

The base is :class:`cratekit.core.jobs.Artifacts`, which says why an item has a
report at all, why it sits under the queue and why the configuration is passed
in. What is adoption's own is the two directory names and how :func:`committed`
orders what it reads.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.core import config, jobs

#: The directory under the queue root that holds committed item reports.
ARTIFACTS_DIRNAME = "adopt-artifacts"

#: Where an attempt writes before the engine commits it. A SIBLING of the final
#: directory rather than a temp directory, because ``jobs.commit_artifact`` is an
#: ``os.replace`` and that is atomic only within one filesystem.
STAGING_DIRNAME = "adopt-staging"


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
    """Every committed report for this job, in item order, read back off disk.

    SORTED BY THE ORDINAL AS A NUMBER, not by the filename: ``"10000"`` sorts
    before ``"9999"`` as text, and a census over a real library is tens of
    thousands of items. Every ``*.json`` file is taken for a report here, so a
    name that is no ordinal raises out of the sort key.
    """
    return _REPORTS.committed(
        cfg, job_id, ordered=lambda paths: sorted(paths, key=lambda item: int(item.stem))
    )


__all__ = [
    "ARTIFACTS_DIRNAME",
    "STAGING_DIRNAME",
    "committed",
    "final_path",
    "produced",
    "staged_path",
    "write",
]
