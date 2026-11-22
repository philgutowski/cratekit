"""Sync's scenario: the collection removal behind its gate (U298).

`crate sync removed` over a landed pass whose account playlist lost a track:
the plan as a person reads it, the gate as the envelope the two acts answer,
the decision, and the acting drive that takes the offered row out of the
collection through the guarded writer's shared capture. On the removal
suite's own library, with the account a fake catalogue and no socket open.
"""

from __future__ import annotations

import os

from cratekit.core.exit_codes import ExitCode
from cratekit.sync import removed_cli
from tests import test_intake_land_account_playlists_native as account_landing
from tests import test_sync_removed
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
#: The modification time every staged file is given. A landing's digest covers
#: each file's size and time, and the clock the capture pins is not the one a
#: file is stamped with, so an unpinned time moves the digest between runs.
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
