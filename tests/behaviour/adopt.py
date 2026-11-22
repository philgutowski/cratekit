"""Adoption's scenarios: the scan job and the apply job, queued, driven and reported (U298).

`crate adopt scan` queues one item per live row and drives them, each item's
report staged and then committed beside the queue; `crate adopt apply` stops
at its explicit gate, queues one item for the plan it approved, and its
worker writes the memberships inside one guarded database session. On the
adoption workers suite's own cut over library. The job report, the job
shell and the two report directories are three of the things U298 gave one
home each, and this scenario holds what a job prints at each step and every
report file it leaves.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_adopt_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_adopt_workers import _reader_cache as _reader_cache  # noqa: PLC0414
from tests.test_adopt_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_adopt_workers import cut_over as cut_over  # noqa: PLC0414
from tests.test_adopt_workers import library as library  # noqa: PLC0414
from tests.test_adopt_workers import machine as machine  # noqa: PLC0414

OK = int(ExitCode.OK)
APPROVE = "adopt.apply.approve"


def test_scan_and_apply_jobs_queued_driven_and_reported(stage, cut_over):
    queued = stage.json("adopt", "scan")
    assert queued.code == OK, queued.stdout
    scan = queued.envelope["data"]["job_id"]
    driven = stage.json("adopt", "scan", "--job", scan)
    assert driven.code == OK, driven.stdout
    # The finished job as a person reads it: a second ask drives nothing.
    assert stage.crate("adopt", "scan", "--job", scan).code == OK

    assert stage.crate("adopt", "apply").code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json("adopt", "apply")
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    option = refused.envelope["cause"]["detail"]["options"][0]
    assert stage.decide(run_id, APPROVE, option).code == OK

    approved = stage.json("--run", run_id, "adopt", "apply")
    assert approved.code == OK, approved.stdout
    apply = approved.envelope["data"]["job_id"]
    applied = stage.json("--run", run_id, "adopt", "apply", "--job", apply)
    assert applied.code == OK, applied.stdout
    assert applied.envelope["data"]["state"] == "succeeded", applied.stdout
    stage.crate("--run", run_id, "adopt", "apply", "--job", apply)
