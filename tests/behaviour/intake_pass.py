"""Intake's pass scenarios: a sync pass landed with its account playlists and hearts (U307).

`crate intake land --pass` files each account playlist under its own name
(U113, U175) and hearts into All Favorites, Pink (U120, U153); `crate inbox
refill --pass` refills an emptied playlist (U134); `crate inbox analyzed`
clears what rekordbox analysed (U166). Its own file because the suite pins the
batch day with an autouse fixture.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from cratekit.intake import analyzed_cli, refill_cli
from tests.test_inbox_analyzed import _analysed
from tests.test_inbox_refill import ACCOUNT, _emptied, _refill
from tests.test_inbox_refill import offline as offline  # noqa: PLC0414
from tests.test_intake_land_account_playlists_native import _land, _stage, swept
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
from tests.test_intake_land_hearts_native import NOV, SEP, _home, hearts_swept
from tests.test_intake_land_native import GATE
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import _stage as _stage_named
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_intake_land_owned_hearts_native import _owned

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)


def _two_acts(stage, verb: list[str], gate: str = GATE):
    """The gate as a person reads it and as the envelope, its answer, and the acting drive."""
    assert stage.crate(*verb).code == ASKED
    refused = stage.json(*verb)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, gate, "apply").code == OK
    return stage.json("--run", run_id, *verb)


def test_account_playlists_land_as_their_own_inbox_playlists(stage, native_library, silence):
    cfg, _root = native_library
    swept(
        cfg,
        {
            "pl-a": ("Sunset Warmup", ("One", "Shared")),
            "pl-b": ("Deep Cuts", ("Shared", "Three")),
        },
    )
    for title in ("One", "Shared", "Three", "Unclaimed"):
        _stage(cfg, silence, title)

    acted = _two_acts(stage, _land())
    assert acted.code == OK, acted.stdout
    assert acted.envelope["data"]["totals"]["memberships"] == 5


def test_hearts_downloaded_and_owned_join_all_favorites_and_their_months(
    stage, native_library, silence
):
    cfg, _root = native_library
    _home(cfg)
    _owned(cfg, silence, "Owned")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    hearts_swept(cfg, {"Owned": SEP, "Fresh": NOV})
    for title in ("One", "Fresh"):
        _stage(cfg, silence, title)

    acted = _two_acts(stage, _land())
    assert acted.code == OK, acted.stdout
    assert acted.envelope["data"]["totals"]["hearts placed"] == 4


def test_an_emptied_account_playlist_is_refilled_from_its_pass(
    stage, native_library, silence, offline
):
    cfg, _root = native_library
    for title in ("Held1", "Held2", "Held3"):
        _stage(cfg, silence, title)
    older = _two_acts(stage, ["intake", "land", "--name", "older batch"])
    assert older.code == OK, older.stdout
    swept(cfg, {"pl-a": (ACCOUNT, ("Held1", "New1", "Held2", "New2", "Held3"))})
    for title in ("New1", "New2"):
        _stage(cfg, silence, title)
    landed = _two_acts(stage, _land())
    assert landed.code == OK, landed.stdout
    _emptied(cfg)

    refilled = _two_acts(stage, _refill(), refill_cli.APPROVE_GATE)
    assert refilled.code == OK, refilled.stdout
    assert refilled.envelope["data"]["totals"]["added"] == 5
    again = _two_acts(stage, _refill(), refill_cli.APPROVE_GATE)
    assert again.code == OK, again.stdout


def test_the_analysed_rows_are_cleared_from_analyze(stage, native_library, silence):
    cfg, _root = native_library
    for name in ("Alpha", "Bravo", "Charlie"):
        _stage_named(cfg, silence, f"{name}.flac")
    landed = _two_acts(stage, ["intake", "land", "--name", "2026-10-28_three"])
    assert landed.code == OK, landed.stdout
    _analysed(cfg, "Alpha", "Charlie")

    cleared = _two_acts(stage, ["inbox", "analyzed"], analyzed_cli.APPROVE_GATE)
    assert cleared.code == OK, cleared.stdout
    assert cleared.envelope["data"]["totals"]["removed"] == 2
    again = _two_acts(stage, ["inbox", "analyzed"], analyzed_cli.APPROVE_GATE)
    assert again.code == OK, again.stdout
