"""Favorites split's scenarios: the quarter playlists turned into months behind the gate (U308).

`crate favorites split` dates each member of a quarter playlist under the
Favorites folder by its hearts job, else by the account, else leaves it
undated, shows each month and each quarter at its explicit gate, and once the
gate is answered fills the months and retires the quarters. On the split
suite's own library: hearts landed natively with no pass, quarters made on a
handle, the account faked.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_favorites_backfill import _account, _land, _stage
from tests.test_favorites_split import AUG, GATE, NOV, OCT, VERB, _quarter
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


def test_quarters_split_into_months_behind_the_gate(stage, native_library, silence, monkeypatch):
    cfg, _root = native_library
    folder_id, _source_id = _home(cfg)
    # Nothing to split yet: no quarter, so no gate and no account read.
    assert stage.crate(*VERB).code == OK
    titles = {"Oct A": OCT.format(day=1), "Oct B": OCT.format(day=2), "Nov A": NOV}
    _landed_hearts(stage, cfg, silence, {**titles, "Summer": None, "Nowhere": None})
    _quarter(cfg, folder_id, "2026-Q4", *titles)
    _quarter(cfg, folder_id, "2026-Q3", "Summer", "Nowhere", "Oct A")
    _account(monkeypatch, {"Summer": AUG, "Nowhere": None})

    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "approve").code == OK
    split = stage.crate("--run", run_id, *VERB)
    assert split.code == OK, split.stderr
    # Run again: every quarter is retired, so nothing is asked and nothing is written.
    assert stage.json(*VERB).code == OK
