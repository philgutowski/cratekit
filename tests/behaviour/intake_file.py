"""Intake's file scenarios: one file already in the library filed on either medium (U307).

`crate intake file` writes one row and one batch playlist behind its gate, and a
retag makes the answer stale; on the bridge it splices the intake file or plans
without a gate. Its own file because the writers suite builds its own fixtures.
"""

from __future__ import annotations

from cratekit.core import tags
from cratekit.core.exit_codes import ExitCode
from tests.test_intake_writers_native import GATE, _file, _single
from tests.test_intake_writers_native import _forget_libraries as _forget_libraries  # noqa: PLC0414
from tests.test_intake_writers_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_writers_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_writers_native import bridge_library as bridge_library  # noqa: PLC0414
from tests.test_intake_writers_native import export as export  # noqa: PLC0414
from tests.test_intake_writers_native import machine as machine  # noqa: PLC0414
from tests.test_intake_writers_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_writers_native import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)


def test_a_native_file_is_one_row_and_one_playlist(stage, native_library, silence):
    cfg, _root = native_library
    verb = _file(_single(cfg, silence))

    assert stage.crate(*verb).code == ASKED
    refused = stage.json(*verb)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK
    filed = stage.json("--run", run_id, *verb)
    assert filed.code == OK, filed.stdout
    assert filed.envelope["data"]["totals"]["added"] == 1


def test_an_answer_over_one_title_is_stale_once_the_file_is_retagged(
    stage, native_library, silence
):
    cfg, _root = native_library
    path = _single(cfg, silence)
    refused = stage.json(*_file(path))
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK
    assert tags.write_tags(path, {"title": "02A - 126 - Renamed"})

    stale = stage.json("--run", run_id, *_file(path))
    assert stale.code not in (OK, ASKED), stale.stdout
    assert stale.envelope["cause"]["reason"] == "decision-stale"


def test_on_the_bridge_an_export_is_spliced_and_none_is_a_plan(
    stage, bridge_library, silence, export
):
    cfg = bridge_library
    path = _single(cfg, silence)
    planned = stage.json(*_file(path))
    assert planned.code == OK, planned.stdout
    spliced = stage.json(*_file(path, "--export", str(export)))
    assert spliced.code == int(ExitCode.PENDING_HUMAN), spliced.stdout
