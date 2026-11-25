"""A ``crate sync land`` run under ``--progress json``, for a parent test to read over a pipe.

Not collected: ``tests/test_progress_json.py`` runs it in a child pytest, so
the root conftest's guards stand around it as around every test, and reads
its standard error through a real pipe (U963, R-932). The child writes what
the run answered to the file named by ``RESULT``, and, when ``GO`` names a
file, holds the tag step's job running until that file exists.
"""

from __future__ import annotations

import io
import json
import os
import sys
import time
from pathlib import Path

from cratekit import cli
from cratekit.cli import gates, progress
from cratekit.cli import tail as tail_chain
from cratekit.core import jobs
from tests.test_sync_land import Tail, _account, _machine

#: The environment variables the parent names its files by.
RESULT = "CRATEKIT_PROGRESS_CHILD_RESULT"
GO = "CRATEKIT_PROGRESS_CHILD_GO"

#: How long the held job waits for the parent before it gives up, in seconds.
HOLD_SECONDS = 60.0


def _held(go: Path, waited: list[bool]):
    """A tag step's work that waits for ``go``, so the parent reads the job running."""

    def work(_job: jobs.Job, _item: jobs.Item) -> None:
        deadline = time.monotonic() + HOLD_SECONDS
        while not go.exists():
            if time.monotonic() > deadline:
                return
            time.sleep(0.02)
        waited.append(True)

    return work


def test_child(tmp_path, monkeypatch):
    from cratekit.analysis import vocals

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", lambda: object())
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(progress, "WATCH_SECONDS", 0.02)
    _cfg, script = _machine(tmp_path, monkeypatch, "slim")
    _account(monkeypatch, script, "101")
    stand_in = Tail()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    waited: list[bool] = []
    go = os.environ.get(GO)
    if go:
        stand_in.work[tail_chain.TAG] = _held(Path(go), waited)

    out = io.StringIO()
    code = cli.run(
        ["--output", "json", "--progress", "json", "sync", "land"], stdout=out, stderr=sys.stderr
    )
    envelope = json.loads(out.getvalue())
    try:
        gates.load(envelope["run_id"])
        saved = True
    except Exception:  # noqa: BLE001 - the parent reads the answer, not a traceback
        saved = False
    Path(os.environ[RESULT]).write_text(
        json.dumps(
            {"code": code, "run_id": envelope["run_id"], "saved": saved, "waited": bool(waited)}
        )
    )
