"""Two refusals a gated database verb meets after its gate (U300), each writing nothing.

A digest moved by a second staged container, and an application off its recorded pin.
"""

from __future__ import annotations

from cratekit.core import rb_writer
from cratekit.core.exit_codes import ExitCode
from tests.test_favorites_order import GATE as ORDER_GATE
from tests.test_favorites_order import VERB as ORDER
from tests.test_favorites_order import _fill, _make
from tests.test_intake_land_hearts_native import _home
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
DECISION = int(ExitCode.DECISION_REQUIRED)


def test_a_plan_that_moved_after_its_gate(stage, native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")

    rehearsed = stage.json(*_land("--rehearse"))
    assert rehearsed.code == OK, rehearsed.stdout
    refused = stage.json(*_land())
    assert refused.code == DECISION, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    _stage(cfg, silence, "Two.flac")
    moved = stage.json("--run", run_id, *_land())
    assert moved.code != OK, moved.stdout
    stage.crate("--run", run_id, *_land())


def test_an_application_version_off_its_pin(stage, native_library, monkeypatch):
    cfg, _root = native_library
    folder_id, source_id = _home(cfg)
    _make(cfg, folder_id, "Undated", "2026-08", "2026-09")
    _fill(cfg, source_id)

    refused = stage.json(*ORDER)
    assert refused.code == DECISION, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, ORDER_GATE, "approve").code == OK

    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: "6.0.0")
    drifted = stage.json("--run", run_id, *ORDER)
    assert "app-version-pin-drift" in drifted.stdout, drifted.stdout
    stage.crate("--run", run_id, *ORDER)
