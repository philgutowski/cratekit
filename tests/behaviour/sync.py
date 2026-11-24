"""Sync's scenario: the collection removal behind its gate (U298).

``borrowed`` routes a suite's own drivers through the stage, so its tests run
as written as scenarios (U304).
"""

from __future__ import annotations

import json
import os
import sys

from cratekit.cli import output
from cratekit.core.exit_codes import ExitCode
from cratekit.sync import removed_cli
from tests import cli_drive, test_sync_removed
from tests import test_intake_land_account_playlists_native as account_landing
from tests.test_sync_removed import VERB, _one_offered
from tests.test_sync_removed import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_sync_removed import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_sync_removed import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_sync_removed import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_sync_removed import library as library  # noqa: PLC0414
from tests.test_sync_removed import machine as machine  # noqa: PLC0414
from tests.test_sync_removed import native_library as native_library  # noqa: PLC0414
from tests.test_sync_removed import offline as offline  # noqa: PLC0414
from tests.test_sync_removed import pinned_day as pinned_day  # noqa: PLC0414
from tests.test_sync_removed import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)
#: The modification time every staged file is given, since a landing's digest
#: covers each file's time and the capture's clock pin does not reach it.
STAGED_NS = 1_790_000_000_000_000_000


def test_collection_removal(stage, native_library, silence, monkeypatch, offline):
    cfg, _root = native_library
    stage_file = account_landing._stage

    def pinned(*args, **kwargs):
        path = stage_file(*args, **kwargs)
        os.utime(path, ns=(STAGED_NS, STAGED_NS))
        return path

    # Both helpers that stage a file: the owned tracks' and the new ones'.
    monkeypatch.setattr(account_landing, "_stage", pinned)
    monkeypatch.setattr(test_sync_removed, "_stage", pinned)
    _one_offered(cfg, silence, monkeypatch)

    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, removed_cli.CONFIRM_GATE, "apply").code == OK

    acted = stage.json("--run", run_id, *VERB)
    assert acted.code == OK, acted.stdout
    assert acted.envelope["data"]["totals"]["removed"] == 1
    # The record the write left, as restore reads it back.
    assert stage.crate("restore", "list").code == OK


def borrowed(stage, monkeypatch) -> None:
    """Route the suites' two drivers through ``stage``, so a suite's own test is a scenario (U304).

    Every binding of ``tests.cli_drive``'s ``drive`` and ``drive_human`` in a
    loaded test module answers through the stage: the same dispatcher and
    envelope check, each command kept.
    """

    def drive(argv):
        ran = stage.json(*argv)
        document = json.loads(ran.stdout or "{}")
        if document:
            assert output.envelope_problems(document) == [], document
        return ran.code, document

    def drive_human(argv):
        ran = stage.crate(*argv)
        return ran.code, ran.stdout or ran.stderr

    for name, module in list(sys.modules.items()):
        if module is None or not (name == "tests" or name.startswith("tests.")):
            continue
        for attr, value in list(vars(module).items()):
            if value is cli_drive.drive:
                monkeypatch.setattr(module, attr, drive)
            elif value is cli_drive.drive_human:
                monkeypatch.setattr(module, attr, drive_human)
