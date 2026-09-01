"""U46: the resume guarantee, measured through the SHIPPED binding.

``tests/test_jobs.py`` already kills a driver mid item and proves the engine
redoes exactly one. That file calls ``jobs.drive`` with a handler written beside
it, so it measures the engine and says nothing about the seam that reaches the
engine from a verb. This file kills a process running ``cli.handlers.run_job``
against the real ``master`` handler instead.

It also measures the property a one-item job structurally cannot: that a resume
redoes the unfinished item AND NO OTHER. "No other" needs something to range over,
so every job here has several.

THE PROCESS GENUINELY DIES. A thread cannot be killed this way and an in-process
fake never leaves the driver lock behind for the kernel to release, which is the
state the next process has to read correctly.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from cratekit.cli import handlers
from cratekit.core import config, jobs
from cratekit.master import cli as master_cli
from cratekit.modules.tools import mastering
from tests import job_worker

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
WORKER = Path(__file__).resolve().parent / "job_worker.py"


def fake_binaries(tmp_path: Path) -> tuple[Path, Path]:
    """Two executables NAMED ffmpeg and ffprobe, so the stand-in can tell them apart.

    ``core.binaries`` checks only that an override points at an executable file, so
    a link to ``/bin/echo`` satisfies resolution and nothing here ever runs a real
    encoder. The NAMES matter: the stand-in runner dispatches on ``argv[0]``, and
    two overrides pointing at one path make every stage look like the same stage,
    which is a harness failure that reads exactly like a broken handler.
    """
    directory = tmp_path / "bin"
    directory.mkdir(exist_ok=True)
    made = []
    for name in ("ffmpeg", "ffprobe"):
        link = directory / name
        if not link.exists():
            link.symlink_to("/bin/echo")
        made.append(link)
    return made[0], made[1]


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    ffmpeg, ffprobe = fake_binaries(tmp_path)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    monkeypatch.setenv("CRATEKIT_BIN_FFMPEG", str(ffmpeg))
    monkeypatch.setenv("CRATEKIT_BIN_FFPROBE", str(ffprobe))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def queued(cfg, tmp_path):
    """Four recordings, one job, one item each, in a queue of its own."""
    sets = tmp_path / "library" / "Sets"
    sets.mkdir(parents=True)
    sources = []
    for name in ("one", "two", "three", "four"):
        path = sets / f"{name}.wav"
        path.write_bytes(b"not really audio, and nothing here ever reads it")
        sources.append(path)

    root = tmp_path / "jobs"
    root.mkdir()
    db = root / jobs.QUEUE_FILENAME
    with jobs.open_store(db) as store:
        job = jobs.enqueue(
            store,
            handler_key="master",
            payload=master_cli.frozen_payload(str(sources[0]), None, False),
            cfg=cfg,
            item_ids=tuple(str(p) for p in sources),
        )
    return job, db, root, sources


def _spawn(*args: str) -> subprocess.Popen:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    return subprocess.Popen(
        [sys.executable, str(WORKER), *args],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _wait_for(path: Path, *, seconds: float = 30.0) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if path.exists():
            return
        time.sleep(0.02)
    raise AssertionError(f"{path.name} never appeared within {seconds}s")


def _attempts(ledger: Path) -> list[str]:
    return [line for line in ledger.read_text().splitlines() if line]


def _states(db: Path, job_id: str) -> dict[str, jobs.ItemState]:
    with jobs.open_store(db) as store:
        return {Path(i.item_id).stem: i.state for i in jobs.items(store, job_id)}


def test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item(
    queued, monkeypatch
):
    job, db, root, sources = queued
    first = root / "first.log"
    first.write_text("")
    stall = "three"

    worker = _spawn("seam", str(db), job.job_id, str(root), str(first), stall)
    try:
        _wait_for(root / f"stalled-{stall}")
    finally:
        worker.kill()
        worker.wait(timeout=30)

    before = _attempts(first)
    assert before[-1] == stall, before
    assert before.count(stall) == 1
    finished = [name for name in before if name != stall]
    assert finished, "nothing completed before the kill, so 'and no other' ranges over nothing"

    states = _states(db, job.job_id)
    assert states[stall] == jobs.ItemState.CLAIMED, states
    for name in finished:
        assert states[name] == jobs.ItemState.DONE, states

    # The second pass runs here, in this process, through the same seam.
    second = root / "second.log"
    second.write_text("")
    monkeypatch.setattr(mastering, "subprocess_runner", job_worker.seam_encoder(second))
    with jobs.open_store(db) as store:
        result = handlers.run_job(store, jobs.get(store, job.job_id), root=root)

    redone = _attempts(second)
    assert stall in redone, redone
    assert not (set(redone) & set(finished)), (
        f"the resume redid work that was already done: {sorted(set(redone) & set(finished))}"
    )
    assert result.failed == 0
    assert all(state == jobs.ItemState.DONE for state in _states(db, job.job_id).values())


def test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination(
    queued
):
    """The reason the handler stages at all.

    A killed encode leaves a partial file. At the destination that file is
    permanent damage: every later resume meets ``output-exists`` and is told it
    would discard a master somebody kept, when the file is this queue's own corpse.
    """
    job, db, root, sources = queued
    stall = "three"
    stalled_source = next(p for p in sources if p.stem == stall)
    ledger = root / "kill.log"
    ledger.write_text("")

    worker = _spawn("seam", str(db), job.job_id, str(root), str(ledger), stall)
    try:
        _wait_for(root / f"stalled-{stall}")
    finally:
        worker.kill()
        worker.wait(timeout=30)

    final = mastering.output_path(stalled_source)
    assert not final.exists(), "a killed encode left a partial file at the destination"
    staging = final.parent / master_cli.MASTER_STAGING_DIRNAME / job.job_id
    partial = list(staging.rglob(final.name))
    assert partial, f"nothing was staged under {staging}"
    assert partial[0].read_bytes() == b"half an encode"
