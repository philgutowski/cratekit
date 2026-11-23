"""Intake's repair scenarios: a doubled file name proposed, accepted and renamed (U307).

`crate repair paths --root` offers a shorter name for each doubled file, and
`--apply` renames only the accepted one behind its gate, or refuses before any
rename over a row the new name would take. Its own file for its ``library``.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.intake.test_repair_apply import LONG, OTHER_LONG, _accept, _audio, _folder
from tests.intake.test_repair_apply import collected as collected  # noqa: PLC0414
from tests.intake.test_repair_apply import configured as configured  # noqa: PLC0414
from tests.intake.test_repair_apply import library as library  # noqa: PLC0414
from tests.test_naming_apply_cli import _record

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)
GATE = "repair.paths.confirm"
APPLY = ["repair", "paths", "--apply"]


def test_an_accepted_proposal_is_renamed_and_an_open_one_is_not(stage, configured):
    folder = _folder(configured)
    accepted = _audio(folder, LONG, b"fLaC the audio")
    _audio(folder, OTHER_LONG, b"fLaC other audio")

    assert stage.crate("repair", "paths", "--root", str(folder)).code == OK
    scanned = stage.json("repair", "paths", "--root", str(folder))
    assert scanned.code == OK, scanned.stdout
    assert len(scanned.envelope["data"]["items"]) == 2
    _accept(configured, accepted)

    assert stage.crate(*APPLY).code == ASKED
    refused = stage.json(*APPLY)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK
    renamed = stage.json("--run", run_id, *APPLY)
    assert renamed.code == OK, renamed.stdout
    assert renamed.envelope["data"]["totals"]["renamed"] == 1


def test_a_dark_row_under_a_proposed_name_refuses_the_repair(stage, collected):
    folder = _folder(collected)
    held = _audio(folder, LONG)
    scanned = stage.json("repair", "paths", "--root", str(folder))
    assert scanned.code == OK, scanned.stdout
    _accept(collected, held)
    _record(collected, f"/mnt/volume/Music/{LONG}", identifier="10")

    refused = stage.json("-d", f"{GATE}=apply", *APPLY)
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    assert refused.envelope["cause"]["reason"] == "collection-row-unmapped"
