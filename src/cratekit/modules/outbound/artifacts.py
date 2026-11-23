"""Where one outbound item's report is staged, and where it lands.

:class:`cratekit.core.jobs.Artifacts` is the base and says why; the outbound
module's own are the two directory names and :func:`committed`'s order.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.core import config, jobs

#: The directory under the queue root that holds committed item reports.
ARTIFACTS_DIRNAME = "outbound-artifacts"

#: Where an attempt writes before the engine commits it: a sibling of the final
#: directory, since the commit is an ``os.replace``, atomic within one filesystem.
STAGING_DIRNAME = "outbound-staging"

#: The four names every caller uses, bound to this feature's directories (U298).
_REPORTS = jobs.Artifacts(final=ARTIFACTS_DIRNAME, staging=STAGING_DIRNAME)
final_path, staged_path, produced, write = (
    _REPORTS.final_path,
    _REPORTS.staged_path,
    _REPORTS.produced,
    _REPORTS.write,
)


def committed(cfg: config.Config, job_id: str) -> tuple[dict[str, Any], ...]:
    """Every committed report for this job, read back off disk, in filename order."""
    return _REPORTS.committed(cfg, job_id, ordered=sorted)


__all__ = [
    "ARTIFACTS_DIRNAME", "STAGING_DIRNAME", "committed", "final_path", "produced",
    "staged_path", "write",
]
