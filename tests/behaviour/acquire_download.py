"""Acquire's download scenarios: the vendored drive through its fake provider (U305).

`crate acquire download` queues a list's tracks and a resume drives them
through the vendored downloader, which the suite stands a fake provider and
tool in for. A drive that lands every track, one whose login is refused, one
whose session is withdrawn part way and then resumed, and one with no session
stored, each with the files it leaves and the job's state as `crate` prints
them. Kept apart from ``acquire.py`` because the drive suite names its own
``cfg`` and ``library``.
"""

from __future__ import annotations

import pytest

from cratekit.core import secrets
from cratekit.core.exit_codes import ExitCode
from tests.test_vendored_drive import STORED, keys, resume_argv, tidal_list
from tests.test_vendored_drive import cfg as cfg  # noqa: PLC0414
from tests.test_vendored_drive import keychain as keychain  # noqa: PLC0414
from tests.test_vendored_drive import library as library  # noqa: PLC0414
from tests.test_vendored_drive import provider as provider  # noqa: PLC0414
from tests.test_vendored_drive import slept as slept  # noqa: PLC0414
from tests.test_vendored_drive import stored as stored  # noqa: PLC0414
from tests.test_vendored_drive import tool as tool  # noqa: PLC0414

OK = int(ExitCode.OK)


@pytest.fixture
def temporary(tmp_path):
    """The drive suite's own, less its move of the temporary directory.

    The suite points ``tempfile`` at a folder of the test's so it can count
    token directories; a capture refuses any configuration outside the
    temporary directory, so here the scenario's own directory stands for it.
    """
    return tmp_path


def _queue(stage, library, tracks: list[str], name: str) -> list[str]:
    path = library / name
    path.write_text(tidal_list([(key, f"Artist {key}", f"Title {key}") for key in tracks]))
    queued = stage.json("acquire", "download", str(path))
    assert queued.code == OK, queued.stdout
    return resume_argv(queued.envelope["data"]["job_id"])


def test_a_drive_lands_every_track(stage, cfg, library, tool, provider, keychain):
    resume = _queue(stage, library, keys(3), "three.json")
    assert stage.json(*resume).code == OK
    stage.crate("jobs", "list")


def test_a_refused_login_and_a_withdrawn_session_park(stage, cfg, library, tool, provider, keychain):
    provider.reject_login = True
    stage.json(*_queue(stage, library, keys(2), "refused.json"))
    provider.reject_login = False

    resume = _queue(stage, library, keys(4), "withdrawn.json")
    provider.withdraw_at = 2 + 4 * 2
    stage.json(*resume)
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, {**STORED, "access_token": "FAKE-value-4"})
    provider.withdraw_at = None
    assert stage.json(*resume).code == OK
    stage.crate("jobs", "list")


def test_a_missing_session_parks(stage, cfg, library, tool, provider, temporary):
    resume = _queue(stage, library, keys(2), "unstored.json")
    assert stage.json(*resume).code != OK
    stage.crate(*resume)
