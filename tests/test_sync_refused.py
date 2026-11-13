"""U284: a sync pass lands when every catalogue but Discogs refuses, and stops plainly when Discogs cannot help.

Sitting 94's pass downloaded 25 tracks and failed 23 at its tag step as
``catalogue-unreachable``: Beatport answered 403 on every lookup, as it had
since sitting 93, and Discogs was not asked because no token was recorded. The
staged batch then held every later pass and label go beside it. Phillip's
answer of 2026-11-13, option 3: carry on only when a Discogs token is recorded.

With a token, a file Discogs searched and could not tag while every other
catalogue refused settles ``sources-unread``, never ``no-hit``, and the pass
goes on to the guess, analysis, naming and the landing, naming each such file
and the refusing catalogues with the date each began refusing. With no token
the pass stops at its tag step, as before, and its refusal says which
catalogues refused and since when, and that recording a Discogs token lets it
carry on, rather than sending the person to their network. A timeout, a failed
name lookup or a 5xx still stops it with the network step first.

Five sections: the record of when a catalogue began refusing, the run count
that writes it, the searcher's refusal, the sweep's report, and the chain every
landing verb runs. Every catalogue answer is a fake or a recorded shape.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.cli import label_sync, sync_land
from cratekit.cli import tail as tail_chain
from cratekit.core import config, jobs, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import artifacts, refused, searchers, tag
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_discogs_searcher import SENT, results, routed
from tests.test_sync_land import Tail
from tests.test_tag_folder_copyright import MINIMAL, RAWAX, downloaded, five_labels
from tests.test_tag_workers import general, item_causes, item_states, resume_argv, tag_job
from tests.test_tagging_engine import TAXONOMY, place

#: Beatport's refusal as the shipped fetch hands it on (U281).
CHALLENGE = searchers.Fetched(note="Cloudflare challenge, HTTP 403", status=403)
#: An outage, the shipped fetch's shape for a timeout and for a 5xx.
TIMED_OUT = searchers.Fetched(note="transport failure: timed out")
SERVER_ERROR = searchers.Fetched(note="HTTP 503", status=503)
#: Discogs refusing this client with a valid token, a 403.
DISCOGS_403 = searchers.Fetched(note="HTTP 403", status=403)

#: The moment sitting 93 first met Beatport's 403, and the record's clock after it.
BEGAN = datetime(2026, 11, 10, 3, 49, tzinfo=timezone.utc)
BEGAN_STAMP = "2026-11-10T03:49:00Z"


@pytest.fixture
def clock(monkeypatch):
    """The record's clock, fixed at :data:`BEGAN` and moved by the test."""
    now = [BEGAN]
    monkeypatch.setattr(refused, "_now", lambda: now[0])
    return now


@pytest.fixture(autouse=True)
def fresh_runs():
    searchers.reset_runs()
    yield
    searchers.reset_runs()


def _record_path() -> Path:
    return config.state_path(refused.KEY)


def _searcher(fetch, *, token: str | None = SENT, run: searchers.Refusals | None = None):
    asker = searchers.discogs_asker(token=token, fetch=fetch, sleep=lambda _s: None)
    return searchers.catalogue_searcher(
        TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=run
    )


# ═══════════════════════════════════════════════════════════════════════════
# 1. The record of when each catalogue began refusing
# ═══════════════════════════════════════════════════════════════════════════


def test_a_first_refusal_sets_since_and_a_later_one_keeps_it(clock):
    refused.refused(searchers.BEATPORT)
    clock[0] = BEGAN + timedelta(days=3)
    refused.refused(searchers.BEATPORT)

    held = refused.read()
    assert held[searchers.BEATPORT] == refused.Standing(
        since=BEGAN_STAMP, last="2026-11-13T03:49:00Z", count=2
    )
    assert refused.since((searchers.BEATPORT, searchers.DISCOGS)) == {
        searchers.BEATPORT: BEGAN_STAMP,
        searchers.DISCOGS: "",
    }


def test_an_answer_clears_the_catalogue_and_leaves_the_others(clock):
    refused.refused(searchers.BEATPORT)
    refused.refused(searchers.TRAXSOURCE)
    refused.answered(searchers.BEATPORT)

    assert set(refused.read()) == {searchers.TRAXSOURCE}


def test_an_answer_from_a_catalogue_not_refusing_writes_nothing(clock):
    refused.answered(searchers.BEATPORT)

    assert not _record_path().exists()


def test_a_record_that_does_not_parse_reads_as_none_and_is_written_over(clock):
    path = _record_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json", encoding="utf-8")
    assert refused.read() == {}

    refused.refused(searchers.BEATPORT)

    assert refused.read()[searchers.BEATPORT].since == BEGAN_STAMP
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["version"] == refused.VERSION


def test_an_entry_of_the_wrong_shape_is_skipped_and_the_rest_read(clock):
    path = _record_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "catalogues": {
                    "beatport": {"since": BEGAN_STAMP, "last": BEGAN_STAMP, "count": 4},
                    "traxsource": {"since": "", "last": BEGAN_STAMP, "count": 1},
                    "bandcamp": "refusing",
                }
            }
        ),
        encoding="utf-8",
    )
    assert set(refused.read()) == {searchers.BEATPORT}


def test_a_record_that_cannot_be_written_never_raises(tmp_path, clock):
    blocker = tmp_path / "a-file"
    blocker.write_text("x", encoding="utf-8")

    refused.refused(
        searchers.BEATPORT, path=blocker / "record.json", lock=blocker / "record.lock"
    )

    assert refused.read(blocker / "record.json") == {}


def test_a_lock_another_process_holds_skips_the_write_rather_than_waiting(tmp_path, clock):
    fcntl = pytest.importorskip("fcntl")
    import os

    lock = tmp_path / "held.lock"
    fd = os.open(lock, os.O_CREAT | os.O_RDWR)
    naps: list[float] = []
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        refused.refused(
            searchers.BEATPORT, path=tmp_path / "record.json", lock=lock, sleep=naps.append
        )
    finally:
        os.close(fd)

    assert refused.read(tmp_path / "record.json") == {}
    assert sum(naps) >= refused.LOCK_WAIT_S - refused.LOCK_POLL_S


# ═══════════════════════════════════════════════════════════════════════════
# 2. The run count of a sweep writes it, and nothing else does
# ═══════════════════════════════════════════════════════════════════════════


def test_a_sweeps_run_count_records_a_refusal_sent_and_not_one_unsent(clock):
    fetch = routed(search=results(), beatport=CHALLENGE)
    run = searchers.for_run("job@1")
    assert run.record

    for title in ("a", "b", "c", "d", "e"):
        hit = _searcher(fetch, run=run)("", title)
        assert hit.unread == (searchers.BEATPORT,)

    standing = refused.read()[searchers.BEATPORT]
    assert standing.since == BEGAN_STAMP
    assert standing.count == searchers.REFUSALS_BEFORE_STOP, "an unsent answer is not a refusal"


def test_a_miss_from_the_refusing_catalogue_clears_it_and_an_outage_does_not(clock):
    run = searchers.for_run("job@1")
    _searcher(routed(search=results(), beatport=CHALLENGE), run=run)("", "a")
    _searcher(routed(search=results(), beatport=TIMED_OUT), run=run)("", "b")
    assert searchers.BEATPORT in refused.read(), "an outage says nothing about a refusal"

    _searcher(routed(search=results()), run=run)("", "c")
    assert refused.read() == {}


def test_a_searcher_built_with_no_run_count_keeps_no_record(clock):
    _searcher(routed(search=results(), beatport=CHALLENGE))("", "a")
    _searcher(routed(search=results(), beatport=CHALLENGE), run=searchers.Refusals())("", "b")

    assert not _record_path().exists()


# ═══════════════════════════════════════════════════════════════════════════
# 3. The searcher's refusal when every catalogue asked refused
# ═══════════════════════════════════════════════════════════════════════════


def _raised(searcher, title: str = "a") -> CratekitError:
    with pytest.raises(CratekitError) as raised:
        searcher("", title)
    return raised.value


def test_with_no_token_a_refusing_beatport_names_itself_its_date_and_the_token(clock):
    refused.refused(searchers.BEATPORT)
    clock[0] = BEGAN + timedelta(days=3)

    error = _raised(_searcher(routed(search=results(), beatport=CHALLENGE), token=None))

    cause = error.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.retryable
    assert "every catalogue asked refused this client" in cause.message
    assert f"beatport, refusing since {BEGAN_STAMP}" in cause.message
    first = cause.remediation.steps[0]
    assert "crate login discogs-token" in first
    assert "carries on" in first
    assert not any("network" in step for step in cause.remediation.steps)
    assert cause.detail["refused"] == {searchers.BEATPORT: BEGAN_STAMP}
    assert cause.detail["discogs"] == searchers.DISCOGS_NO_TOKEN


def test_a_refusal_with_no_date_recorded_still_names_the_catalogue(clock):
    error = _raised(_searcher(routed(search=results(), beatport=CHALLENGE), token=None))

    assert "refused this client: beatport, so nothing" in error.cause.message
    assert error.cause.detail["refused"] == {searchers.BEATPORT: ""}


@pytest.mark.parametrize("outage", [TIMED_OUT, SERVER_ERROR], ids=["timeout", "5xx"])
def test_an_outage_is_not_a_refusal_and_sends_the_person_to_their_network_first(clock, outage):
    error = _raised(_searcher(routed(search=results(), beatport=outage), token=None))

    cause = error.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.remediation.steps[0].startswith("check this machine's network connection")
    assert "refused" not in cause.detail
    assert "none of beatport could be read" in cause.message


def test_with_a_token_discogs_refusing_too_stops_and_names_both(clock):
    error = _raised(_searcher(routed(search=DISCOGS_403, beatport=CHALLENGE)))

    cause = error.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert "refused this client: discogs, beatport" in cause.message
    assert set(cause.detail["refused"]) == {searchers.DISCOGS, searchers.BEATPORT}
    assert cause.detail["discogs"] == ""
    assert not any("crate login" in step for step in cause.remediation.steps)


def test_a_refusal_beside_an_outage_is_an_outage_first(clock):
    error = _raised(_searcher(routed(search=SERVER_ERROR, beatport=CHALLENGE)))

    assert error.cause.remediation.steps[0].startswith("check this machine's network")
    assert "refused" not in error.cause.detail


def test_a_token_discogs_rejects_beside_a_refusing_beatport_names_beatport_too(clock):
    refused.refused(searchers.BEATPORT)

    error = _raised(
        _searcher(routed(search=searchers.Fetched(note="HTTP 401", status=401), beatport=CHALLENGE))
    )

    cause = error.cause
    assert cause.reason == "credential-missing"
    assert "crate login discogs-token" in " ".join(cause.remediation.steps)
    assert any(
        f"beatport, refusing since {BEGAN_STAMP}" in step for step in cause.remediation.steps
    )
    assert cause.detail["refused"] == {searchers.BEATPORT: BEGAN_STAMP}
    assert SENT not in json.dumps(cause.detail)


def test_with_a_token_a_discogs_miss_beside_a_refusing_beatport_is_askable_and_never_no_hit(
    clock,
):
    hit = _searcher(routed(search=results(), beatport=CHALLENGE))("", "a")

    assert hit.genre is None
    assert hit.unread == (searchers.BEATPORT,)
    assert [(said.source, said.answer) for said in hit.answers] == [
        (searchers.DISCOGS, "miss"),
        (searchers.BEATPORT, "blocked"),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 4. The sweep names the files the catalogues refused
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """A configured machine on the full profile, so the label verbs are on."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    data = valid_data(library)
    data["profile"] = {"name": "full"}
    built = config.from_dict(data)
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def staging(tmp_path) -> Path:
    out = tmp_path / "staging"
    out.mkdir()
    return out


def bind(monkeypatch, *, token: str | None, beatport=CHALLENGE, search=None, by_title=None):
    """Bind the worker's searcher to the shipped one over recorded answers.

    A searcher per call carrying the run count the worker hands in, as the
    shipped binder builds one. ``by_title`` answers Beatport per title.
    """

    def fetch(url: str) -> searchers.Fetched:
        if url.startswith(searchers.BEATPORT_SEARCH):
            for title, page in (by_title or {}).items():
                if f"={title}" in url or f"+{title}" in url:
                    return page
            return beatport
        if url.startswith(searchers.DISCOGS_SEARCH):
            return search or searchers.Fetched(text=results(), status=200)
        return searchers.Fetched(note=f"no route for {url}")

    def for_taxonomy(declared=None, refusals=None):
        asker = searchers.discogs_asker(token=token, fetch=fetch, sleep=lambda _s: None)
        return searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        )

    monkeypatch.setattr(searchers, "for_taxonomy", for_taxonomy)
    general(monkeypatch, None)


def _sweep(staging: Path) -> tuple[int, jobs.Job, dict]:
    code, queued = drive(["tag", "folder", "--queue-only", str(staging)])
    assert code == int(ExitCode.OK), queued
    job = tag_job()
    code, resumed = drive(resume_argv(job.job_id))
    return code, job, resumed


def test_a_sweep_with_a_token_names_each_file_beatport_refused_and_writes_no_genre(
    cfg, staging, silence, monkeypatch, clock
):
    for name in ("a", "b", "c"):
        place(staging, silence, name)
    bind(monkeypatch, token=SENT)

    code, job, resumed = _sweep(staging)

    assert code == int(ExitCode.OK), resumed
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["refused"]["files"] == ["a.flac", "b.flac", "c.flac"]
    assert tagging["refused"]["catalogues"] == {searchers.BEATPORT: BEGAN_STAMP}
    assert "a.flac, b.flac, c.flac" in tagging["refused"]["said"]
    assert f"beatport, refusing since {BEGAN_STAMP}" in tagging["refused"]["said"]
    assert tagging["skipped"][tag.SOURCES_UNREAD] == 3
    assert tagging["skipped"][tag.NO_HIT] == 0
    assert tagging["refusal_stop"] is None
    for report in artifacts.committed(cfg, job.job_id):
        assert report["skipped"] == tag.SOURCES_UNREAD
        assert report["unread"] == {searchers.BEATPORT: "blocked"}
    assert all(tags.read_genre_from_file(staging / f"{n}.flac") is None for n in "abc")


def test_a_file_beatport_answered_is_tagged_through_it_and_not_named(
    cfg, staging, silence, monkeypatch, clock
):
    from tests.test_catalogue_searcher import (
        ARTIST,
        BUCKET_GENRE,
        TITLE,
        _beatport_page,
        _beatport_track,
    )

    answered = place(staging, silence, "a")
    assert tags.write_tags(answered, {"artist": ARTIST, "title": TITLE})
    place(staging, silence, "b")
    page = searchers.Fetched(
        text=_beatport_page([_beatport_track(ARTIST, TITLE, BUCKET_GENRE)]), status=200
    )
    bind(monkeypatch, token=SENT, by_title={"Sunrise": page})

    code, _job, resumed = _sweep(staging)

    assert code == int(ExitCode.OK), resumed
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged"] == 1
    assert tagging["refused"]["files"] == ["b.flac"]


def test_a_sweep_beatport_never_refused_names_nothing(cfg, staging, silence, monkeypatch, clock):
    place(staging, silence, "a")
    bind(monkeypatch, token=SENT, beatport=SERVER_ERROR)

    code, _job, resumed = _sweep(staging)

    assert code == int(ExitCode.OK), resumed
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.SOURCES_UNREAD] == 1
    assert tagging["refused"] is None, "an outage beside a miss is not a refusal"


def test_a_file_its_copyright_line_settles_is_tagged_by_its_label_and_not_named(
    cfg, staging, silence, monkeypatch, clock
):
    """U240 unchanged: a label's file takes its genre with every catalogue refusing."""
    five_labels()
    downloaded(staging, silence, "a", "℗ 2023 Rawax")
    place(staging, silence, "b")
    bind(monkeypatch, token=SENT)

    code, _job, resumed = _sweep(staging)

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(staging / "a.flac") == MINIMAL
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["label_genres"] == {RAWAX: 1}
    assert tagging["refused"]["files"] == ["b.flac"]


def test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token(
    cfg, staging, silence, monkeypatch, clock
):
    refused.refused(searchers.BEATPORT)
    clock[0] = BEGAN + timedelta(days=3)
    for name in ("a", "b"):
        place(staging, silence, name)
    bind(monkeypatch, token=None)

    code, job, resumed = _sweep(staging)

    assert code != int(ExitCode.OK)
    assert item_causes(job.job_id) == {
        "a.flac": searchers.UNREACHABLE_REASON,
        "b.flac": searchers.UNREACHABLE_REASON,
    }
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.FAILED}
    stop = resumed["cause"]["detail"]["tagging"]["refusal_stop"]
    assert stop["files"] == ["a.flac", "b.flac"]
    assert stop["catalogues"] == {searchers.BEATPORT: BEGAN_STAMP}
    assert stop["discogs"] == searchers.DISCOGS_NO_TOKEN
    assert "crate login discogs-token" in stop["said"]
    assert stop["said"] in resumed["cause"]["message"]
    assert any("crate login discogs-token" in step for step in stop["steps"])


def test_a_sweep_stopped_by_an_outage_carries_no_refusal_stop(
    cfg, staging, silence, monkeypatch, clock
):
    place(staging, silence, "a")
    bind(monkeypatch, token=None, beatport=TIMED_OUT)

    code, _job, resumed = _sweep(staging)

    assert code != int(ExitCode.OK)
    assert resumed["cause"]["detail"]["tagging"]["refusal_stop"] is None


# ═══════════════════════════════════════════════════════════════════════════
# 5. The chain every landing verb runs: on to the landing, or a plain stop
# ═══════════════════════════════════════════════════════════════════════════


class Rest(Tail):
    """The tail with its tag step REAL and every later step standing in.

    ``tag folder`` runs through the real dispatcher, its worker and the shipped
    searcher over recorded answers. The guess answers as its verb would, and
    the analysis, naming and landing stand in as :class:`tests.test_sync_land.Tail`
    has them: real jobs in the real queue, and the landing's gate.
    """

    def __call__(self, argv: list[str]):
        if argv[:2] == ["tag", "folder"]:
            self.calls.append(list(argv))
            return self.real(argv)
        if argv[:2] == ["tag", "guess"]:
            self.calls.append(list(argv))
            totals = {"count": 3, "before": 0, "after": 0, "written": 0, "unread": 0}
            return 0, {"outcome": "ok", "data": {"totals": totals}, "warnings": []}
        return super().__call__(argv)


@pytest.fixture
def rest(monkeypatch) -> Rest:
    stand_in = Rest()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    monkeypatch.setattr(tail_chain, "vocals_unavailable", lambda: None)
    monkeypatch.setattr(tail_chain, "vocals_on", lambda _cfg: False)
    return stand_in


def _chain() -> tail_chain.Chain:
    return tail_chain.Chain(
        progress=None,
        namespace="sync.land",
        title="sync land",
        steps=tail_chain.STEPS,
        origin=("test",),
        again="run crate sync land again",
    )


def test_with_a_token_the_pass_reaches_its_landing_and_names_the_refused_files(
    cfg, staging, silence, monkeypatch, clock, rest
):
    for name in ("a", "b", "c"):
        place(staging, silence, name)
    bind(monkeypatch, token=SENT)
    chain = _chain()

    with pytest.raises(tail_chain.Attend) as attended:
        tail_chain.run(chain, staging, cfg, ["--pass", "p1"], "p1")

    assert attended.value.step == tail_chain.LAND
    assert chain.summary["refused"] == {
        "files": ["a.flac", "b.flac", "c.flac"],
        "catalogues": {searchers.BEATPORT: BEGAN_STAMP},
    }
    (row,) = [check for check in chain.checks if check["key"] == "sync.land.refused"]
    assert row["status"] == "warn"
    for named in ("a.flac", "b.flac", "c.flac", f"beatport, refusing since {BEGAN_STAMP}"):
        assert named in row["detail"]
    assert "needs genre" in row["detail"]
    assert "tag retag" in row["detail"]
    assert [step for step in chain.summary["steps"]] == [
        tail_chain.TAG,
        tail_chain.GUESS,
        tail_chain.ANALYZE,
        tail_chain.RESTAMP,
        tail_chain.NAME,
    ]
    assert all(tags.read_genre_from_file(staging / f"{n}.flac") is None for n in "abc")


def test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token(
    cfg, staging, silence, monkeypatch, clock, rest
):
    refused.refused(searchers.BEATPORT)
    clock[0] = BEGAN + timedelta(days=3)
    place(staging, silence, "a")
    bind(monkeypatch, token=None)

    with pytest.raises(tail_chain.Stop) as stopped:
        tail_chain.run(_chain(), staging, cfg, ["--pass", "p1"], "p1")

    stop = stopped.value
    assert stop.step == tail_chain.TAG
    cause = stop.error.cause
    assert f"beatport, refusing since {BEGAN_STAMP}" in cause.message
    assert "crate login discogs-token" in cause.message
    assert any("crate login discogs-token" in step for step in cause.remediation.steps)
    assert not any(argv[:2] == ["intake", "land"] for argv in rest.calls)
    assert not any(argv[:2] == ["tag", "guess"] for argv in rest.calls)


def test_a_timeout_still_stops_the_pass_at_its_tag_step_with_no_refusal_said(
    cfg, staging, silence, monkeypatch, clock, rest
):
    place(staging, silence, "a")
    bind(monkeypatch, token=None, beatport=TIMED_OUT)
    chain = _chain()

    with pytest.raises(tail_chain.Stop) as stopped:
        tail_chain.run(chain, staging, cfg, ["--pass", "p1"], "p1")

    assert stopped.value.step == tail_chain.TAG
    assert "refusing since" not in stopped.value.error.cause.message
    assert "refused" not in chain.summary
    assert not any(argv[:2] == ["intake", "land"] for argv in rest.calls)


def test_a_pass_whose_catalogues_answered_says_nothing_of_refusals(
    cfg, staging, silence, monkeypatch, clock, rest
):
    place(staging, silence, "a")
    bind(monkeypatch, token=SENT, beatport=SERVER_ERROR)
    chain = _chain()

    with pytest.raises(tail_chain.Attend):
        tail_chain.run(chain, staging, cfg, ["--pass", "p1"], "p1")

    assert "refused" not in chain.summary
    assert not [check for check in chain.checks if check["key"] == "sync.land.refused"]


def test_every_landing_verb_runs_the_one_chain_whose_tag_step_this_is():
    """``sync land``, ``label sync --go`` and ``sync bandcamp`` reach the tag step
    through :func:`tail.through_name`, so a label go's tag step behaves as the
    sync pass's by construction."""
    import inspect

    from cratekit.cli import sync_bandcamp

    for module in (sync_land, label_sync, sync_bandcamp):
        assert "tail.through_name(" in inspect.getsource(module)
