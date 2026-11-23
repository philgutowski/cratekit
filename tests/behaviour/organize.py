"""Organize's scenarios: both areas, the filing, the root and the mirror (U309).

`crate organize` plans the rekordbox and account areas behind a gate each, and
the fake's record of every account call is written beside the ledger. The
refusals: two root folders named for a genre, and no provider session; with
export off the verb still plans and names the steps it left out.
"""

from __future__ import annotations

import dataclasses
from types import MappingProxyType

from cratekit.adopt import collection
from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import account as outbound_account
from cratekit.organize import account as account_area
from cratekit.organize import account_mirror, rekordbox
from tests.behaviour.outbound import account_calls
from tests.test_organize import (
    ACCOUNT_GATE,
    DB_GATE,
    MARKED_ID,
    MARKED_YEAR,
    ONLY_FILE,
    ONLY_ROOT,
    VERB,
    _filed,
    _listing_without_removed,
    _marked,
    _root_world,
    _steps,
)
from tests.test_organize import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_organize import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_organize import machine as machine  # noqa: PLC0414
from tests.test_organize import seams as seams  # noqa: PLC0414
from tests.test_organize import world as world  # noqa: PLC0414

OK = int(ExitCode.OK)
DECISION = int(ExitCode.DECISION_REQUIRED)
ONLY_MIRROR = (*VERB, "--only", account_area.MIRROR)
#: The real seam to the account, held before any fixture puts the fake there.
STORED_ACCOUNT = outbound_account.resolve


def _crate(stage, *argv):
    collection.reset_cache()
    return stage.crate(*argv)


def _json(stage, *argv):
    collection.reset_cache()
    return stage.json(*argv)


def _gated(stage, argv, *answers: tuple[str, str]) -> None:
    """The first gate as a person reads it, each gate's two acts, and the acting run printed."""
    assert _crate(stage, *argv).code == DECISION
    refused = _json(stage, *argv)
    run_id = refused.envelope["run_id"]
    for gate, option in answers:
        assert refused.code == DECISION, refused.stdout
        assert refused.envelope["cause"]["detail"]["gate"] == gate, refused.stdout
        assert stage.decide(run_id, gate, option).code == OK
        if (gate, option) != answers[-1]:
            refused = _json(stage, "--run", run_id, *argv)
    done = _crate(stage, "--run", run_id, *argv)
    assert done.code == OK, done.stdout + done.stderr


def test_the_rekordbox_side_files_the_tracks_and_rotates_the_batch(stage, world):
    cfg, _fake, held, inbox, ids = world
    assert _crate(stage, *VERB, "--report").code == OK

    _gated(stage, VERB, (DB_GATE, "approve"), (ACCOUNT_GATE, "abort"))

    assert _filed(cfg) == ["r-one", "r-two"]
    assert held.folders_created == [] and held.moves == []
    account_calls(stage, held)


def test_the_account_side_makes_the_label_folder_and_archives_the_set(stage, world):
    cfg, _fake, held, _inbox, _ids = world

    _gated(stage, VERB, (DB_GATE, "abort"), (ACCOUNT_GATE, "apply"))

    assert _filed(cfg) == []
    assert "Kompakt" in held.folders_created
    account_calls(stage, held)


def test_the_filing_step_alone_files_a_marked_playlist_in_its_year(stage, world):
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)
    assert _crate(stage, *ONLY_FILE, "--report").code == OK

    _gated(stage, ONLY_FILE, (ACCOUNT_GATE, "apply"))

    assert held.folder_names[held.placed[MARKED_ID]] == MARKED_YEAR
    account_calls(stage, held)


def test_the_root_step_alone_removes_debris_and_then_the_emptied_legacy_folder(stage, world):
    _cfg, fake, held = _root_world(world)

    _gated(stage, ONLY_ROOT, (ACCOUNT_GATE, "apply"))
    assert [kind for _id, kind in held.root_removed] == ["debris", "debris", "empty"]
    _listing_without_removed(fake, held)
    _gated(stage, ONLY_ROOT, (ACCOUNT_GATE, "apply"))

    assert held.folders_removed == ["hand-legacy"]
    account_calls(stage, held)


def test_a_mirror_pass_after_a_full_apply_and_a_rerun_that_plans_nothing(stage, world):
    _cfg, _fake, held, _inbox, _ids = world
    _gated(stage, VERB, (DB_GATE, "approve"), (ACCOUNT_GATE, "apply"))
    folders = list(held.folders_created)

    _gated(stage, ONLY_MIRROR, (ACCOUNT_GATE, "apply"))

    assert len(held.folders_created) > len(folders)
    again = _json(stage, *ONLY_MIRROR, "--report")
    assert again.code == OK, again.stdout
    states = {step["state"] for step in _steps(again.envelope, account_area.AREA).values()}
    assert not states & {"planned", "refused"}, states
    account_calls(stage, held)


def test_a_genre_two_root_folders_on_the_account_carry_is_refused_by_the_mirror(stage, world):
    cfg, _fake, held, _inbox, _ids = world
    _gated(stage, VERB, (DB_GATE, "approve"), (ACCOUNT_GATE, "apply"))
    name = account_mirror.read_library(cfg).folders[0].name
    held.folder_names.update({"hand-1": name, "hand-2": name})

    assert _crate(stage, *ONLY_MIRROR, "--report").code == OK
    report = _json(stage, *ONLY_MIRROR, "--report")

    step = _steps(report.envelope, account_area.AREA)[f"mirror:{name}"]
    assert (step["state"], step["reason"]) == ("refused", "account-mirror-ambiguous"), step
    account_calls(stage, held)


def test_an_account_with_no_stored_session_refuses_the_account_steps(stage, world, monkeypatch):
    _cfg, _fake, held, _inbox, _ids = world
    monkeypatch.setattr(outbound_account, "resolve", STORED_ACCOUNT)

    assert _crate(stage, *ONLY_FILE, "--report").code == OK
    report = _json(stage, *ONLY_FILE, "--report")

    step = _steps(report.envelope, account_area.AREA)[account_area.FILE]
    assert (step["state"], step["reason"]) == ("refused", "credential-missing"), step
    account_calls(stage, held)


def test_with_the_export_module_off_organize_plans_and_says_what_it_left_out(stage, world):
    cfg, _fake, held, _inbox, _ids = world
    off = config.ModulesConfig(explicit=MappingProxyType({"export": False}))
    config.save(dataclasses.replace(cfg, modules=off))
    config.reset_cache()

    shown = _crate(stage, *VERB, "--report")
    assert shown.code == OK, shown.stderr
    report = _json(stage, *VERB, "--report")

    assert _steps(report.envelope, account_area.AREA)[account_area.SETS]["state"] == "listed"
    assert _steps(report.envelope, rekordbox.AREA)[rekordbox.INSPIRATION]["state"] == "listed"
    account_calls(stage, held)
