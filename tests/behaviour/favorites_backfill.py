"""Favorites backfill's scenarios: owned hearts placed into All Favorites behind the gate (U308).

`crate favorites backfill` lists every owned heart All Favorites lacks, dates
it by its job or the account, shows the placement at its explicit gate, and
once the gate is answered places each heart and its month. A second run has
nothing to place. On the backfill suite's own library: hearts landed natively
with no pass, one heart the source system filed deep, the account faked.
"""

from __future__ import annotations

from cratekit.core import session
from cratekit.core.exit_codes import ExitCode
from tests.test_favorites_backfill import GATE, NOV, SEP, VERB, _account, _deep_row, _land, _stage
from tests.test_intake_land_hearts_native import UNKNOWN, _home, hearts_swept
from tests.test_intake_land_hearts_native import pinned_day as pinned_day  # noqa: PLC0414
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


def _landed_hearts(stage, cfg, silence, titles: dict[str, str | None]) -> None:
    """The suite's hearts landed with no pass, the staged files given the pinned instant.

    The landing's digest names each staged file by its time, and the suite's
    own ``_landed_hearts`` stages and lands in one call with no settle between.
    """
    hearts_swept(cfg, {title: UNKNOWN if when is None else when for title, when in titles.items()}, run_id="")
    for title in titles:
        _stage(cfg, silence, title)
    stage.settle()
    _land()


def test_owned_hearts_placed_behind_the_gate(stage, native_library, silence, monkeypatch):
    cfg, _root = native_library
    _home(cfg)
    _deep_row(cfg, silence, "Owned")
    _landed_hearts(stage, cfg, silence, {"Owned": None, "Same Girl": None, "Fractals": "2026-10-04T12:00:00+00:00"})
    _account(monkeypatch, {"Owned": SEP, "Same Girl": NOV, "Fractals": SEP, "Elsewhere": NOV})

    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "approve").code == OK
    placed = stage.crate("--run", run_id, *VERB)
    assert placed.code == OK, placed.stderr
    # Run again: every heart is in, and the gate is asked over a plan of nothing.
    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)


def test_backfill_refused_without_its_acknowledgment(stage, native_library, monkeypatch):
    cfg, _root = native_library
    _home(cfg)
    _account(monkeypatch, {})
    session.ack_path(cfg).unlink()
    assert stage.crate(*VERB).code == int(ExitCode.ACK_REQUIRED)
