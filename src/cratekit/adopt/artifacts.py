"""Where one adoption item's report is staged, and where it lands.

The base is :class:`cratekit.core.jobs.Artifacts` (U298). Adoption's own are the
two directory names and the order :func:`committed` reads in.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.core import config, jobs

#: The directory under the queue root that holds committed item reports.
ARTIFACTS_DIRNAME = "adopt-artifacts"

#: Where an attempt writes before the engine commits it: a SIBLING of the final
#: directory, because ``jobs.commit_artifact`` is an ``os.replace``, atomic only
#: within one filesystem.
STAGING_DIRNAME = "adopt-staging"


_REPORTS = jobs.Artifacts(final=ARTIFACTS_DIRNAME, staging=STAGING_DIRNAME)
final_path = _REPORTS.final_path
staged_path = _REPORTS.staged_path
produced = _REPORTS.produced
write = _REPORTS.write


def committed(cfg: config.Config, job_id: str) -> tuple[dict[str, Any], ...]:
    """Every committed report for this job, in item order, read back off disk.

    SORTED BY THE ORDINAL AS A NUMBER, since ``"10000"`` sorts before ``"9999"``
    as text. Every ``*.json`` file is taken for a report, so a name that is no
    ordinal raises out of the sort key.
    """
    return _REPORTS.committed(
        cfg, job_id, ordered=lambda paths: sorted(paths, key=lambda item: int(item.stem))
    )
