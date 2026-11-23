"""Adoption's scenarios: the scan, apply and move jobs, the genre report and the revert (U298, U310).

`crate adopt scan` queues and drives one item per live row; `crate adopt apply`
stops at its gate, then its worker writes the memberships inside one guarded
session; every job's printing and report file is held (U298). U310 adds
`crate adopt move` behind its gate, `crate report genres`, and the revert
ledger, which no verb reaches, driven after an apply handed a tag to write.
"""

from __future__ import annotations

import json
from pathlib import Path

from cratekit.adopt import apply_cli, revert_tags
from cratekit.adopt import revert as adopt_revert
from cratekit.core import tags
from cratekit.core.exit_codes import ExitCode
from tests.test_adopt_move import GATE as MOVE_GATE
from tests.test_adopt_move import VERB as MOVE
from tests.test_adopt_move import moved as moved  # noqa: PLC0414
from tests.test_adopt_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_adopt_workers import _reader_cache as _reader_cache  # noqa: PLC0414
from tests.test_adopt_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_adopt_workers import cut_over as cut_over  # noqa: PLC0414
from tests.test_adopt_workers import library as library  # noqa: PLC0414
from tests.test_adopt_workers import machine as machine  # noqa: PLC0414
from tests.test_adopt_workers import placed as placed  # noqa: PLC0414
from tests.test_adopt_workers import silence as silence  # noqa: PLC0414
from tests.test_report_genres import VERB as GENRES
from tests.test_report_genres import counted as counted  # noqa: PLC0414

OK = int(ExitCode.OK)
APPROVE = "adopt.apply.approve"


def test_scan_and_apply_jobs_queued_driven_and_reported(stage, cut_over):
    queued = stage.json("adopt", "scan")
    assert queued.code == OK, queued.stdout
    scan = queued.envelope["data"]["job_id"]
    driven = stage.json("adopt", "scan", "--job", scan)
    assert driven.code == OK, driven.stdout
    # The finished job as a person reads it: a second ask drives nothing.
    assert stage.crate("adopt", "scan", "--job", scan).code == OK

    assert stage.crate("adopt", "apply").code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json("adopt", "apply")
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    option = refused.envelope["cause"]["detail"]["options"][0]
    assert stage.decide(run_id, APPROVE, option).code == OK

    approved = stage.json("--run", run_id, "adopt", "apply")
    assert approved.code == OK, approved.stdout
    apply = approved.envelope["data"]["job_id"]
    applied = stage.json("--run", run_id, "adopt", "apply", "--job", apply)
    assert applied.code == OK, applied.stdout
    assert applied.envelope["data"]["state"] == "succeeded", applied.stdout
    stage.crate("--run", run_id, "adopt", "apply", "--job", apply)


def _approved(stage, *verb: str, gate: str) -> str:
    """Meet the gate twice, as a person reads it and as the envelope, then answer it."""
    assert stage.crate(*verb).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*verb)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    assert refused.envelope["cause"]["detail"]["gate"] == gate, refused.stdout
    run_id = refused.envelope["run_id"]
    option = refused.envelope["cause"]["detail"]["options"][0]
    assert stage.decide(run_id, gate, option).code == OK
    return run_id


def test_move_job_queued_driven_and_reported(stage, moved):
    run_id = _approved(stage, *MOVE, gate=MOVE_GATE)
    queued = stage.json("--run", run_id, *MOVE)
    assert queued.code == OK, queued.stdout
    job = queued.envelope["data"]["job_id"]
    driven = stage.json("--run", run_id, *MOVE, "--job", job)
    assert driven.code == OK, driven.stdout
    assert driven.envelope["data"]["state"] == "succeeded", driven.stdout
    stage.crate("--run", run_id, *MOVE, "--job", job)

    # A second plan over the moved tree has nothing left to move.
    again = stage.json(*MOVE)
    assert again.code == int(ExitCode.DECISION_REQUIRED), again.stdout
    assert stage.decide(again.envelope["run_id"], MOVE_GATE, "abort").code == OK
    stage.crate("--run", again.envelope["run_id"], *MOVE)


def test_genre_report(stage, counted):
    assert stage.crate(*GENRES).code == OK
    assert stage.json(*GENRES).code == OK


def _written(report) -> dict:
    """A revert report as sorted, stable data: every pair restored, every refusal."""
    return {
        "restored": sorted([path, field] for path, field in report.restored),
        "failed": sorted([path, field, why] for (path, field), why in report.failed.items()),
        "files": sorted(report.files()),
    }


def test_revert_after_an_apply_that_wrote_tags(stage, placed, monkeypatch):
    # The shipped apply writes no tag, so no verb reaches the revert ledger: the
    # worker is handed each entry's bucket name as a tag, and the rest is the verb
    # as it ships, each tag written with its revert record ahead of it.
    real = apply_cli.apply_outstanding

    def writing(*args, **kwargs):
        kwargs["tag_value"] = lambda entry, declared: declared.bucket(entry.bucket).display
        return real(*args, **kwargs)

    monkeypatch.setattr(apply_cli, "apply_outstanding", writing)

    queued = stage.json("adopt", "scan")
    assert queued.code == OK, queued.stdout
    assert stage.json("adopt", "scan", "--job", queued.envelope["data"]["job_id"]).code == OK
    run_id = _approved(stage, "adopt", "apply", gate=APPROVE)
    approved = stage.json("--run", run_id, "adopt", "apply")
    assert approved.code == OK, approved.stdout
    job = approved.envelope["data"]["job_id"]
    applied = stage.json("--run", run_id, "adopt", "apply", "--job", job)
    assert applied.code == OK, applied.stdout
    assert applied.envelope["data"]["state"] == "succeeded", applied.stdout

    snapshots = sorted(adopt_revert.read(placed).snapshots, key=lambda one: one.path)
    assert len(snapshots) >= 3, snapshots
    first, changed = snapshots[0], snapshots[1]
    written = {
        "recorded": [[one.path, one.field, one.entry_id, list(one.entries)] for one in snapshots]
    }

    # One entry reverted on its own, through the records its write went through.
    targeted = revert_tags(placed, entry_id=first.entry_id)
    assert targeted.restored and not targeted.failed, targeted
    written["targeted"] = _written(targeted)

    # Another tool rewrites a second file, so its bytes are not the ones its
    # record was stamped from: the revert refuses that one and restores the rest.
    assert tags.write_tags(Path(changed.path), {"energylevel": "1"}) is True
    refused = revert_tags(placed)
    assert list(refused.failed) == [(changed.path, changed.field)], refused
    written["refused"] = _written(refused)

    # The override names that one record, and the ledger is then empty.
    forced = revert_tags(placed, force=list(refused.failed))
    assert list(forced.restored) == [(changed.path, changed.field)], forced
    written["forced"] = _written(forced)
    assert adopt_revert.read(placed).snapshots == ()

    (stage.root / "reverts.json").write_text(json.dumps(written, indent=2, sort_keys=True) + "\n")
