"""Intake's bridge scenarios: a landing through the XML bridge and its import verified (U307).

`crate intake land --export` on a library whose intake tree is still on the
bridge: the gate as a person reads it and as the envelope, the answer, and
the landing that moves the batch into the music folder and writes the intake
file rekordbox imports, ending pending on that import. `crate intake
imported` then reads a Fresh Export taken after the import and retires the
intake file. Beside it what refuses and moves nothing: an answer whose
staging folder gained a file, and a staging folder that is not there. On the
bridge landing suite's own configuration, export and FLAC containers.

A file of its own, because the bridge suites call their configuration
``cfg`` and their container ``silence``, and the native suite's ``silence``
is another fixture of that name.

THE LIBRARY FOLDER IS LEFT FOR THE SUITE TO MAKE. The stage moves the library
root into the scenario's own directory and makes it there, and a bridge
suite's ``cfg`` makes that same folder itself and refuses one already there.
So ``_library_left_to_the_suite`` takes the stage's empty folder away before
the suite's fixture runs, which then makes it as it does in the suite.
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
