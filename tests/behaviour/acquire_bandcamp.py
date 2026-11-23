"""Acquire's Bandcamp scenarios: the plan, the fetch and its refusals (U305).

`crate acquire bandcamp` plans every purchase of the signed in account with
one disposition each, and `acquire bandcamp-fetch` stages what the plan named
into a batch folder and records it. Through the suite's fake account, which
serves real tagged FLAC inside real archives: a plan, a filtered plan, a
fetch, a second run that plans nothing, an expired session and none recorded.
Kept apart from ``acquire.py`` because the Bandcamp suite names its own
``cfg`` and ``library``.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.bandcamp_fakes import FakeAccount
from tests.test_bandcamp_cli import account as account  # noqa: PLC0414
from tests.test_bandcamp_cli import bind
from tests.test_bandcamp_cli import cfg as cfg  # noqa: PLC0414
from tests.test_bandcamp_cli import library as library  # noqa: PLC0414
from tests.test_bandcamp_cli import signed_in as signed_in  # noqa: PLC0414
from tests.test_bandcamp_cli import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_bandcamp_plan_and_fetch(stage, signed_in, account):
    assert stage.json("acquire", "bandcamp").code == OK
    stage.crate("acquire", "bandcamp")
    stage.json("acquire", "bandcamp", "--seller", "pulsromania")
    stage.crate("acquire", "bandcamp", "--seller", "nosuchlabel")
    assert stage.json("acquire", "bandcamp-fetch", "--batch", "Batch One").code == OK
    stage.crate("acquire", "bandcamp")
    stage.json("acquire", "bandcamp-fetch", "--batch", "two/folders")


def test_bandcamp_without_a_session(stage, cfg, monkeypatch):
    bind(monkeypatch, FakeAccount([], page_size=2, archives={}))
    assert stage.json("acquire", "bandcamp").code != OK
    stage.crate("acquire", "bandcamp")
