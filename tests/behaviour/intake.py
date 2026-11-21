"""Intake's scenarios: a rehearsed landing and the gate it feeds (U297).

`crate intake land --rehearse` applies the landing to a copy of the database
and reports the plan's digest; the live command then stops at its gate, which
names that rehearsal; the gate is answered by its separate act and the landing
writes the rows, the playlist and the files. On the native landing suite's own
library, with its two staged containers.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_intake_land_native import GATE, _land, _stage
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_rehearsal_and_the_gate_it_feeds(stage, native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")

    rehearsed = stage.json(*_land("--rehearse"))
    assert rehearsed.code == OK, rehearsed.stdout
    assert rehearsed.envelope["data"]["totals"]["rehearsal"]["landed"] == 2

    # The gate as a person reads it, then as the envelope the two acts answer.
    assert stage.crate(*_land()).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*_land())
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    shown = refused.envelope["cause"]["detail"]["shown"]
    assert shown["digest"] == rehearsed.envelope["data"]["digest"]
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    landed = stage.json("--run", run_id, *_land())
    assert landed.code == OK, landed.stdout
