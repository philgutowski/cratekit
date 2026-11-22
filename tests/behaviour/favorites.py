"""Favorites' scenarios: the Favorites folder put in order behind its gate (U298).

`crate favorites order` reads the folder's playlists oldest first, stops at its
explicit gate showing the order it would leave, and once the gate is answered
moves the playlists inside one guarded database session. On the order suite's
own library: the native landing suite's disposable database with a Favorites
folder made on a handle. The verb finds its gate by name on its registry entry
and takes its capture through the write layer, the two things U298 gave one
home each.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_favorites_order import GATE, VERB, _fill, _make
from tests.test_intake_land_hearts_native import _home
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_favorites_put_in_order_behind_the_gate(stage, native_library):
    cfg, _root = native_library
    folder_id, source_id = _home(cfg)
    made = _make(cfg, folder_id, "Undated", "2026-08", "2026-09", "2026-10")
    _fill(cfg, source_id)
    _fill(cfg, made["2026-09"])

    # The gate as a person reads it, then as the envelope the two acts answer.
    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "approve").code == OK

    ordered = stage.json("--run", run_id, *VERB)
    assert ordered.code == OK, ordered.stdout
    assert ordered.envelope["data"]["totals"]["moved"] == 4
    # Run again: the folder is in order, so nothing is asked and nothing moves.
    stage.crate(*VERB)
