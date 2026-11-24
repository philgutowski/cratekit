"""Acquire's fallback fetch scenarios: an accepted upload landed marked (U305).

Landed marked lossy, or refused under a strict policy. Apart from ``acquire.py``
because the fetch suite names its own ``library``.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_acquire_fallback_fetch import BOOT, FakeFetcher, accepted, bind, tracklist
from tests.test_acquire_fallback_fetch import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_acquire_fallback_fetch import library as library  # noqa: PLC0414
from tests.test_acquire_fallback_fetch import no_real_subprocess as no_real_subprocess  # noqa: PLC0414
from tests.test_acquire_fallback_fetch import permissive as permissive  # noqa: PLC0414
from tests.test_acquire_fallback_fetch import strict as strict  # noqa: PLC0414

OK = int(ExitCode.OK)


def _drive(stage, path) -> None:
    queued = stage.json("acquire", "fallback-fetch", str(path))
    assert queued.code == OK, queued.stdout
    from cratekit.cli import jobs as cli_jobs
    from cratekit.core import jobs

    with jobs.open_store() as store:
        argv = cli_jobs.argv_for(jobs.get(store, queued.envelope["data"]["job_id"]))
    stage.json(*argv)


def test_fallback_fetch_lands_marked(stage, permissive, tmp_path, monkeypatch):
    accepted(permissive)
    bind(monkeypatch, FakeFetcher())
    _drive(stage, tracklist(tmp_path, BOOT))
    stage.crate("acquire", "fallback-fetch", str(tracklist(tmp_path, BOOT)))


def test_fallback_fetch_refused_when_strict(stage, strict, tmp_path, monkeypatch):
    accepted(strict)
    bind(monkeypatch, FakeFetcher())
    _drive(stage, tracklist(tmp_path, BOOT))
