"""Intake's set scenarios: a recording identified, queued and resolved, and its refusals (U307).

`crate intake identify` asks the recognition seam about each chunk of a
recording and writes its tracklist; `crate intake set` over the same
recording reads the answers identify kept and queues one item per track, and
the resume through the driver reports each track owned, offered or missing.
A mix address is fetched through the fetch seam, identified and removed. A
set named for its account playlist stops at the account gate and, answered,
makes the playlist on the faked account. Then the spend refusals, which
queue nothing: a month over its configured bound, a provider quota answered
mid run, and a machine holding no recognition key. Every outside touch is
the worker suite's own fake: the carver, the transport, the ledger, the
fetcher, the catalogue and the account.

A file of its own, because the worker suite calls its configuration ``cfg``
and its library ``library`` as other intake suites call theirs.
"""

from __future__ import annotations

from datetime import date

from cratekit.core.exit_codes import ExitCode
from cratekit.intake import acrcloud, fetch, recognize, set_playlist
from tests.intake.test_recognition import FakeTransport, hit
from tests.intake.test_set_fetch import URL
from tests.intake.test_set_fetch import fetcher as fetcher  # noqa: PLC0414
from tests.intake.test_workers import (
    _recognition,
    owned,
    recording,
    resume_argv,
    three_tracks,
)
from tests.intake.test_workers import cfg as cfg  # noqa: PLC0414
from tests.intake.test_workers import library as library  # noqa: PLC0414
from tests.intake.test_workers import recognised as recognised  # noqa: PLC0414
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_u129_set_account_playlist import ACCOUNT_GATE, PageWritingFetcher, _page
from tests.test_u129_set_account_playlist import account as account  # noqa: PLC0414

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)
REFUSED = int(ExitCode.REFUSED_BY_POLICY)


def test_identify_then_set_then_the_resume_that_resolves_each_track(
    stage, cfg, library, recognised
):
    three_tracks(recognised)
    owned(library, "Aurora Bloom - Sun Path.flac")
    owned(library, "Nova Reef - Tide (Someone Remix).flac")
    path = recording(library)

    assert stage.crate("intake", "identify", str(path)).code in (OK, int(ExitCode.PENDING_HUMAN))
    queued = stage.json("intake", "set", str(path))
    assert queued.code == OK, queued.stdout
    assert queued.envelope["data"]["progress"]["calls"] == 0
    job_id = queued.envelope["data"]["job_id"]

    resumed = stage.json(*resume_argv(job_id))
    assert resumed.code == OK, resumed.stdout
    assert resumed.envelope["data"]["state"] == "succeeded"
    assert stage.crate("job", "show", job_id).code == OK


def test_a_mix_address_is_fetched_identified_and_removed(stage, cfg, library, recognised, fetcher):
    three_tracks(recognised)
    queued = stage.json("intake", "set", URL)
    assert queued.code == OK, queued.stdout
    assert [url for url, _ in fetcher.asked] == [URL]


def test_a_set_stops_at_the_account_gate_and_makes_the_account_playlist(
    stage, account, recognised, monkeypatch
):
    three_tracks(recognised)
    monkeypatch.setattr(fetch, "fetcher", lambda: PageWritingFetcher(_page()))
    monkeypatch.setattr(set_playlist, "today", lambda: date(2026, 10, 10))
    verb = ["intake", "set", URL]

    assert stage.crate(*verb).code == ASKED
    refused = stage.json(*verb)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, ACCOUNT_GATE, "apply").code == OK
    done = stage.json("--run", run_id, *verb)
    assert done.code == OK, done.stdout
    _cfg, _fake, held = account
    assert len(held.added) == 3


def test_a_month_over_its_bound_refuses_identify_and_set_and_queues_nothing(
    stage, library, recognised
):
    _recognition(library, monthly_calls=2)
    three_tracks(recognised)
    path = recording(library)
    for verb in ("identify", "set"):
        refused = stage.json("intake", verb, str(path))
        assert refused.code == REFUSED, refused.stdout
        assert refused.envelope["cause"]["detail"]["kind"] == "monthly"
    assert stage.crate("intake", "set", str(path)).code == REFUSED
    assert recognised.requests == []


def test_a_provider_quota_mid_run_refuses_and_queues_nothing(stage, cfg, library, recognised):
    recognised.answers[:] = [
        hit("Aurora Bloom", "Sun Path"),
        {"status": {"code": 3003, "msg": "limit"}},
    ]
    refused = stage.json("intake", "set", str(recording(library)))
    assert refused.code == REFUSED, refused.stdout
    assert refused.envelope["cause"]["detail"]["kind"] == "provider-quota"


def test_a_set_with_no_recognition_key_is_refused_before_any_seam(stage, cfg, library, monkeypatch):
    monkeypatch.setattr(recognize.binaries, "find", lambda name: f"/usr/bin/{name}")
    transport = FakeTransport()
    monkeypatch.setattr(acrcloud, "http_transport", transport)
    refused = stage.json("intake", "set", str(recording(library)))
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    assert refused.envelope["cause"]["reason"] == "intake-recognition-unready"
    assert transport.requests == []
