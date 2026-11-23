"""Intake's bridge scenarios: a landing through the XML bridge and its import verified (U307).

`crate intake land --export` on a bridge tree ends pending on rekordbox's
import, and `crate intake imported` reads a later export and retires the intake
file; a moved staging folder and a missing one refuse. Its own file because the
bridge suites' ``silence`` is another fixture of that name. The library folder
is left for the suite's ``cfg`` to make, which refuses one already there.
"""

from __future__ import annotations

import pytest

from cratekit.core.exit_codes import ExitCode
from tests.test_intake_imported import _export_after_import, _intake_file
from tests.test_intake_land import BATCH, GATE, _land, _stage
from tests.test_intake_land import cfg as cfg  # noqa: PLC0414
from tests.test_intake_land import export as export  # noqa: PLC0414
from tests.test_intake_land import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)


@pytest.fixture(autouse=True)
def _library_left_to_the_suite(_scenario_world, tmp_path):
    """Take away the stage's empty library folder, which the suite's ``cfg`` makes itself."""
    library = tmp_path / "library"
    if library.is_dir() and not any(library.iterdir()):
        library.rmdir()


def test_a_bridge_landing_and_the_import_that_verifies_it(stage, cfg, silence, export, tmp_path):
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    verb = _land(export, "--name", BATCH)

    assert stage.crate(*verb).code == ASKED
    refused = stage.json(*verb)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK
    landed = stage.crate("--run", run_id, *verb)
    assert landed.code == int(ExitCode.PENDING_HUMAN), landed.stderr

    after = _export_after_import(tmp_path, _intake_file(cfg, BATCH))
    imported = stage.json("intake", "imported", "--export", str(after))
    assert imported.code == OK, imported.stdout
    assert imported.envelope["data"]["items"][0]["count"] == 2
    # Nothing waits now, and the verb says so.
    assert stage.crate("intake", "imported", "--export", str(after)).code == OK


def test_a_bridge_landing_refuses_a_stale_answer_and_an_absent_folder(
    stage, cfg, silence, export, tmp_path
):
    _stage(cfg, silence, "One.flac")
    verb = _land(export, "--name", BATCH)
    refused = stage.json(*verb)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK
    _stage(cfg, silence, "Arrived.flac")

    stale = stage.json("--run", run_id, *verb)
    assert stale.code not in (OK, ASKED), stale.stdout
    assert stale.envelope["cause"]["reason"] == "decision-stale"

    absent = stage.json(*_land(export, str(tmp_path / "absent"), "--name", BATCH))
    assert absent.code not in (OK, ASKED), absent.stdout
    assert absent.envelope["cause"]["reason"] == "intake-list-unusable"
