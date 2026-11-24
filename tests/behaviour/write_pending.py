"""The write layer's deferred routing scenario: the pass after a native landing (U302).

Nothing is deferred, since the native landing files its own track. Its own file for
the landing suite's ``machine`` and ``acknowledged``; the import suite makes its own
library folder, which the stage has already made.
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


def test_route_pending_after_a_native_landing(stage, native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    refused = stage.json(*_land())
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK
    landed = stage.json("--run", run_id, *_land())
    assert landed.code == OK, landed.stdout

    assert stage.crate("route", "pending").code == OK
    passed = stage.json("route", "pending")
    assert passed.code == OK, passed.stdout
    assert passed.envelope["outcome"] == "no_op"
