"""Organize's edit pass: a move made on the account carried into the library (U309).

`crate organize --only mirror-edits --only mirror` carries a move made on the
account into the library behind the rekordbox gate, and the mirror writes
nothing back over it. Its own file because both borrowed suites name
``machine``.
"""

from __future__ import annotations

from cratekit.core import tags
from cratekit.core.exit_codes import ExitCode
from cratekit.organize import cli as organize_cli
from cratekit.organize import mirror_edits
from tests.behaviour.outbound import account_calls
from tests.test_organize_mirror_edits import GENRES
from tests.test_organize_mirror_edits import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_organize_mirror_edits import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_organize_mirror_edits import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_organize_mirror_edits import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_organize_mirror_edits import configured as configured  # noqa: PLC0414
from tests.test_organize_mirror_edits import library as library  # noqa: PLC0414
from tests.test_organize_mirror_edits import machine as machine  # noqa: PLC0414
from tests.test_outbound_workers import bind

OK = int(ExitCode.OK)
DECISION = int(ExitCode.DECISION_REQUIRED)
VERB = ("organize", "--only", mirror_edits.KIND, "--only", "mirror")


def test_a_track_moved_on_the_account_is_retagged_and_refiled_in_the_library(
    stage, machine, monkeypatch
):
    bind(monkeypatch, machine.account)
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")

    assert stage.crate(*VERB).code == DECISION
    refused = stage.json(*VERB)
    assert refused.code == DECISION, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, organize_cli.REKORDBOX_GATE, "approve").code == OK
    second = stage.json("--run", run_id, *VERB)
    assert second.code == DECISION, second.stdout
    assert stage.decide(run_id, organize_cli.ACCOUNT_GATE, "apply").code == OK
    done = stage.crate("--run", run_id, *VERB)
    assert done.code == OK, done.stdout + done.stderr

    assert tags.read_genre_from_file(machine.files["1"]) == "Tech House"
    assert machine.genre_row("1") == GENRES["Tech House"]
    assert machine.places("1") == {("Tech House", "Med")}
    assert machine.held("Tech House Med") == ["r1"]
    # Run again: the edit is the library's now, so neither side plans anything.
    assert stage.crate(*VERB, "--report").code == OK
    account_calls(stage, machine.account)
