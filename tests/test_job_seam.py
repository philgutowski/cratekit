"""U46: the resume guarantee, measured through the SHIPPED binding: a real ``run_job`` over
the ``master`` handler killed mid job must redo the unfinished item and no other.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.cli import handlers
from cratekit.core import config, jobs
from cratekit.master import cli as master_cli
from cratekit.modules.tools import mastering
from tests import job_worker
from tests.test_jobs import _attempts, _config_document, _spawn_worker, _wait_for


def fake_binaries(tmp_path: Path) -> tuple[Path, Path]:
    """Two executables NAMED ffmpeg and ffprobe, so the stand-in can tell them apart."""
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
    ffmpeg, ffprobe = fake_binaries(tmp_path)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(tmp_path / "library"))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    monkeypatch.setenv("CRATEKIT_BIN_FFMPEG", str(ffmpeg))
    monkeypatch.setenv("CRATEKIT_BIN_FFPROBE", str(ffprobe))
    built = config.from_dict(_config_document(tmp_path))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def queued(cfg, tmp_path):
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
        payload = master_cli.frozen_payload(str(sources[0]), None, False)
        items = tuple(str(p) for p in sources)
        job = jobs.enqueue(store, handler_key="master", payload=payload, cfg=cfg, item_ids=items)
    return job, db, root, sources


def _kill_at(stall: str, db: Path, job, root: Path, ledger: Path) -> None:
    worker = _spawn_worker("seam", str(db), job.job_id, str(root), str(ledger), stall)
    try:
        _wait_for(root / f"stalled-{stall}", seconds=30.0)
    finally:
        worker.kill()
        worker.wait(timeout=30)


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

    _kill_at(stall, db, job, root, first)

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
    again = sorted(set(redone) & set(finished))
    assert not again, f"the resume redid work that was already done: {again}"
    assert result.failed == 0
    assert all(state == jobs.ItemState.DONE for state in _states(db, job.job_id).values())


def test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination(queued):
    """The reason the handler stages at all."""
    job, db, root, sources = queued
    stall = "three"
    stalled_source = next(p for p in sources if p.stem == stall)
    ledger = root / "kill.log"
    ledger.write_text("")

    _kill_at(stall, db, job, root, ledger)

    final = mastering.output_path(stalled_source)
    assert not final.exists(), "a killed encode left a partial file at the destination"
    staging = final.parent / master_cli.MASTER_STAGING_DIRNAME / job.job_id
    partial = list(staging.rglob(final.name))
    assert partial, f"nothing was staged under {staging}"
    assert partial[0].read_bytes() == b"half an encode"
