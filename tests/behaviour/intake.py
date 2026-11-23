"""Intake's scenarios: the native landing, what it tags and files, and its refusals (U297, U307).

`crate intake land --rehearse` reports the plan's digest, the live command's
gate names that rehearsal, and the answered landing writes rows, playlist and
files. Beside it: label filing, the vox and dyn My Tags, `crate intake shelve`,
and what refuses and writes nothing (U307). The pass landings, whose suite pins
the batch day, are in ``intake_pass.py``.
"""

from __future__ import annotations

import pytest

from cratekit.core import rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import drift, shelve_cli
from tests.test_intake_land_dyn_native import _read
from tests.test_intake_land_dyn_native import writable as writable  # noqa: PLC0414
from tests.test_intake_land_labels_native import _dated, _manifest
from tests.test_intake_land_native import BATCH, GATE, _cut_over_intake, _land, _stage
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_intake_land_vox_native import _scored
from tests.test_intake_land_vox_native import calibrated as calibrated  # noqa: PLC0414
from tests.test_intake_shelve import FILES, _as_landed_before_u164, _shelve

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)


def _two_acts(stage, verb: list[str], gate: str = GATE):
    """The gate as the envelope, its answer, and the acting drive. Answers (refused, acted)."""
    refused = stage.json(*verb)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, gate, "apply").code == OK
    return refused, stage.json("--run", run_id, *verb)


def _refused(ran, reason: str) -> None:
    """A command that refused for ``reason``, which is not a gate."""
    assert ran.code not in (OK, ASKED), ran.stdout
    assert ran.envelope["cause"]["reason"] == reason, ran.stdout


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


def test_a_manifest_and_a_label_file_the_landed_rows(stage, native_library, silence, tmp_path):
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    manifest = _manifest(
        tmp_path,
        [
            ("1", "Probe", "One", "Kompakt", 2025),
            ("2", "Probe", "Two", "Kompakt", 2024),
            ("3", "Probe", "Absent", "Kompakt", 2024),
        ],
    )
    _refused_by_manifest, acted = _two_acts(stage, _land("--manifest", str(manifest)))
    assert acted.code == OK, acted.stdout
    assert acted.envelope["data"]["totals"]["label playlists"] == 2

    # A second batch under --label, filed by each file's date tag.
    _dated(cfg, silence, "Three.flac", "2019-03-15")
    _dated(cfg, silence, "Four.flac", None)
    verb = ["intake", "land", "--name", "2026-09-30_label", "--label", "PULS"]
    assert stage.crate(*verb).code == ASKED
    _refused_by_label, acted = _two_acts(stage, verb)
    assert acted.code == OK, acted.stdout


def test_a_calibrated_landing_tags_the_rows_that_clear_the_cut(stage, calibrated, silence):
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    _scored(cfg, silence, "Two.flac", 0)
    _scored(cfg, silence, "Three.flac", None)

    assert stage.crate(*_land()).code == ASKED
    _refused_gate, acted = _two_acts(stage, _land())
    assert acted.code == OK, acted.stdout
    assert acted.envelope["data"]["totals"]["vox tagged"] == 1


def test_a_landing_tags_the_rows_whose_drift_reads_variable(stage, writable, silence):
    cfg = writable
    _read(cfg, silence, "Live.flac", "6.2", drift.VARIABLE)
    _read(cfg, silence, "Straight.flac", "0.1", drift.STEADY)
    _read(cfg, silence, "Unread.flac", None, None)

    assert stage.crate(*_land()).code == ASKED
    _refused_gate, acted = _two_acts(stage, _land())
    assert acted.code == OK, acted.stdout
    assert acted.envelope["data"]["totals"]["dyn tagged"] == 1


def test_an_answer_whose_plan_moved_is_stale_and_writes_nothing(stage, native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    rehearsed = stage.json(*_land("--rehearse"))
    assert rehearsed.code == OK, rehearsed.stdout

    # One more file since the rehearsal: the gate names the rehearsal it differs from.
    _stage(cfg, silence, "Two.flac")
    assert stage.crate(*_land()).code == ASKED
    refused = stage.json(*_land())
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    # And one more since the answer: the answer is to a plan that is not this one.
    _stage(cfg, silence, "Three.flac")
    stale = stage.json("--run", run_id, *_land())
    _refused(stale, "decision-stale")
    assert stage.crate("--run", run_id, *_land()).code == stale.code


def test_a_file_already_landed_staged_again_is_refused_at_the_move(stage, native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _first, acted = _two_acts(stage, _land())
    assert acted.code == OK, acted.stdout

    _stage(cfg, silence, "One.flac")
    refused, again = _two_acts(stage, _land())
    assert refused.envelope["cause"]["detail"]["shown"]["already present"] == 1
    _refused(again, "intake-list-unusable")


def test_what_refuses_before_the_gate_and_writes_nothing(stage, native_library, silence, tmp_path):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")

    _refused(stage.json(*_land(str(tmp_path / "absent"))), "intake-list-unusable")
    export = tmp_path / "fresh.xml"
    export.write_text("<DJ_PLAYLISTS/>\n", encoding="utf-8")
    _refused(stage.json(*_land("--export", str(export))), "intake-list-unusable")
    assert stage.crate(*_land("--export", str(export))).code not in (OK, ASKED)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
        _refused(stage.json(*_land("--rehearse")), "rekordbox-running")
        _refused(stage.json(*_land()), "rekordbox-running")


def test_no_acknowledgment_refuses_before_the_gate(stage, machine, silence):
    cfg = machine
    _cut_over_intake(cfg)
    _stage(cfg, silence, "One.flac")

    refused = stage.json(*_land())
    _refused(refused, "backup-acknowledgment-missing")
    assert stage.crate(*_land()).code == refused.code


def test_a_batch_is_shelved_into_the_processed_tree(stage, native_library, silence):
    cfg, _root = native_library
    for name in FILES:
        _stage(cfg, silence, name)
    _first, landed = _two_acts(stage, _land())
    assert landed.code == OK, landed.stdout
    _as_landed_before_u164(cfg, BATCH)

    assert stage.crate(*_shelve("--report", BATCH)).code == OK
    assert stage.crate(*_shelve(BATCH)).code == ASKED
    _refused_gate, shelved = _two_acts(stage, _shelve(BATCH), shelve_cli.SHELVE_GATE)
    assert shelved.code == OK, shelved.stdout
    assert shelved.envelope["data"]["totals"]["rows"] == 3


def test_a_shelve_of_nothing_refuses_before_a_gate(stage, native_library):
    refused = stage.json(*_shelve("--all"))
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    assert stage.json(*_shelve()).code == int(ExitCode.PRECONDITION)
