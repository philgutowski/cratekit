"""Intake's set scenarios: a set landed under INSPIRATION and the backfill verb (U307).

`crate intake land --set` writes the set's playlist in played order and adds a
second part to it (U135); `crate intake inspiration --job` backfills behind its
gate, adds nothing again, and refuses with no acknowledgment. Its own file
because the set suites name ``machine`` and pin the batch day.
"""

from __future__ import annotations

from datetime import date

from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name
from tests import cutover_fixtures
from tests.test_intake_land_native import GATE
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_set_inspiration_playlist import (
    APPROVE,
    FOLDER,
    WORDS,
    _cut_over_intake,
    _inspiration,
    _land,
    _owned,
    _stage,
    set_job,
)
from tests.test_set_inspiration_playlist import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_set_inspiration_playlist import machine as machine  # noqa: PLC0414
from tests.test_set_inspiration_playlist import pinned_day as pinned_day  # noqa: PLC0414

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)


def _two_acts(stage, verb: list[str], gate: str):
    """The gate as a person reads it and as the envelope, its answer, and the acting drive."""
    assert stage.crate(*verb).code == ASKED
    refused = stage.json(*verb)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, gate, "apply").code == OK
    return stage.json("--run", run_id, *verb)


def test_a_set_lands_under_inspiration_and_a_second_part_joins_its_inbox_playlist(
    stage, native_library, silence, monkeypatch
):
    cfg, _root = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("Zebra", "Three", "Apple"))
    _stage(cfg, silence, "Zebra")

    first = _two_acts(stage, _land("--set", job_id, *WORDS), GATE)
    assert first.code == OK, first.stdout
    assert first.envelope["data"]["totals"]["set playlist tracks"] == 2

    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 10))
    _stage(cfg, silence, "Apple")
    verb = ["intake", "land", "--name", "2026-10-10 Set", "--set", job_id, *WORDS]
    second = _two_acts(stage, verb, GATE)
    assert second.code == OK, second.stdout


def test_the_backfill_adds_the_set_playlist_once(stage, native_library, silence):
    cfg, _root = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    _owned(cfg, silence, "Three", content_id="held-3")
    job_id = set_job(cfg, ("One", "Three", "Two"))
    _stage(cfg, silence, "One")
    _stage(cfg, silence, "Two")
    landed = _two_acts(stage, _land(), GATE)
    assert landed.code == OK, landed.stdout

    backfilled = _two_acts(stage, _inspiration(job_id, *WORDS), APPROVE)
    assert backfilled.code == OK, backfilled.stdout
    assert backfilled.envelope["data"]["totals"]["added"] == 3
    again = _two_acts(stage, _inspiration(job_id, *WORDS), APPROVE)
    assert again.code == OK, again.stdout
    assert again.envelope["data"]["totals"]["added"] == 0


def test_the_backfill_with_no_acknowledgment_refuses_before_its_gate(stage, machine):
    _cut_over_intake(machine)
    job_id = set_job(machine, ("One",))
    refused = stage.json(*_inspiration(job_id, *WORDS))
    assert refused.code == int(ExitCode.ACK_REQUIRED), refused.stdout
    assert stage.crate(*_inspiration(job_id, *WORDS)).code == refused.code
