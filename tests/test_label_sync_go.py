"""U108: the guided label sync's go, one summary, one gate, one unattended download.

Every scenario the brief names is driven through the real dispatcher: answers
saved through U107's structured path, the gate refused and then decided by a
separate recorded act as R34 requires, and the download run by
``acquire download``'s own worker against the fake adapter, with the provider's
catalogue faked as U107's suite fakes it.

NOTHING HERE REACHES A NETWORK. The root fixtures fail any test that does.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from cratekit import acquire
from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import listdoc, match_cli
from cratekit.cli import gates, registry
from cratekit.cli import tail as tail_chain
from cratekit.core import config, jobs, provider_gate, review, session
from cratekit.core.cause import Cause, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.jobs import Parked
from cratekit.intake import land_cli, native
from cratekit.intake.land_cli import default_name
from cratekit.label import approved_cli, go, sync_cli
from tests.acquire_fakes import (
    FAKE_ADAPTER,
    FAKE_DECLARATION,
    FakeAdapter,
    Landing,
    Script,
    tidal_list,
)
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_label_sync import Track, answer, bind, next_question, offered, record, register
from tests.test_label_sync import script as scripted_terminal
from tests.test_sync_land import Tail, _ok, _refused

GATE = "label.sync.confirm"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def installed(tmp_path, monkeypatch) -> config.Config:
    """A configured library naming the fake adapter with pacing off."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    resolved = config.from_dict(
        valid_data(
            root,
            profile={"name": "full"},
            acquisition={"adapter": FAKE_ADAPTER, "pacing_delay_s": 0.0},
        )
    )
    config.save(resolved)
    config.reset_cache()
    return resolved


@pytest.fixture(autouse=True)
def tail(monkeypatch) -> Tail:
    """The tail and the landing standing in at the chain's one seam (U190).

    A go that downloaded runs ``tag folder`` through ``intake land`` next, and
    those need audio analysis, a rekordbox collection and an adopted intake
    tree, none of which this fixture holds. ``sync land``'s own stand in queues
    and drives a REAL job per step in the real queue, and its landing stops at
    its gate, so a go that downloaded ends PENDING there.
    """
    stand_in = Tail()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    return stand_in


@pytest.fixture(autouse=True)
def no_vocal_model(monkeypatch) -> None:
    """The vocal model unable to score, so the tail skips its rescore every time.

    PINNED, NOT INHERITED. ``vocals.unavailable`` reads a loader bound in this
    process as able, and an analysis worker driven by an earlier test in the
    same xdist worker leaves one bound. The tail then queues ``analyze vocals
    --unscored`` and every exact list of the tail's verbs here fails, on some
    distributions of the suite and not others: measured at R-1115, where the
    mutation driver's null control killed one such test twice.
    """
    from cratekit.analysis import vocals

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    monkeypatch.setattr(vocals, "missing_requirement", lambda: "the vocal model is not installed here")


@pytest.fixture
def script(monkeypatch) -> Script:
    fresh = Script()
    monkeypatch.setitem(acquire.ADAPTERS, FAKE_ADAPTER, FAKE_DECLARATION)
    monkeypatch.setattr(FakeAdapter, "script", fresh)
    monkeypatch.setattr(acquire_cli, "_SLEEP", lambda _seconds: None)
    return fresh


def land_every(script: Script, *releases: tuple[str, int]) -> None:
    """The fake lands every track of each ``(release, tracks)`` as lossless."""
    for release_id, count in releases:
        for n in range(1, count + 1):
            script.landings[f"t-{release_id}-{n}"] = Landing()


def asked() -> dict:
    """``label sync --go`` with nothing decided: the gate refuses with the summary."""
    code, envelope = drive(["label", "sync", "--go"])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["detail"]["gate"] == GATE
    return envelope


def decided(run_id: str, option: str) -> None:
    code, envelope = drive(["run", "decide", run_id, GATE, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), envelope


def gone(run_id: str) -> tuple[int, dict]:
    return drive(["--run", run_id, "label", "sync", "--go"])


def approved_go() -> tuple[str, int, dict]:
    """R34's two acts and then the go. Returns the run, the code and the envelope."""
    run_id = asked()["run_id"]
    decided(run_id, "apply")
    code, envelope = gone(run_id)
    return run_id, code, envelope


def our_jobs() -> list[jobs.Job]:
    with jobs.open_store() as store:
        return [
            job
            for job in jobs.list_jobs(store)
            if job.handler_key == go.DOWNLOAD and go.ORIGIN_KEY in (job.payload or {})
        ]


def item_states(job_id: str) -> dict[str, jobs.ItemState]:
    with jobs.open_store() as store:
        return {item.item_id: item.state for item in jobs.items(store, job_id)}


def fetched(script: Script) -> list[str]:
    return [request.key for request in script.fetched]


def check(envelope: dict, key: str) -> dict:
    found = [one for one in envelope["data"]["checks"] if one["key"] == f"label.sync.go.{key}"]
    assert len(found) == 1, (key, envelope["data"]["checks"])
    return found[0]


def three_labels(monkeypatch):
    for name in ("Alpha Works", "Beta Works", "Gamma Works", "Delta Works"):
        register(name)
    return bind(
        monkeypatch,
        {
            "alpha-works": [("a2", "2026", 2), ("a1", "2025", 1)],
            "beta-works": [("b1", "2026", 3)],
            "gamma-works": [("g2", "2026", 2), ("g1", "2025", 4)],
            "delta-works": [("d1", "2026", 1)],
        },
    )


def answer_every_label() -> None:
    for label_id, word, *picks in (
        ("alpha-works", "all"),
        ("beta-works", "all"),
        ("gamma-works", "pick", "g1"),
        ("delta-works", "not-now"),
    ):
        assert next_question()["label_id"] == label_id
        answer(label_id, word, *picks)


# ═══════════════════════════════════════════════════════════════════════════
# 1. The brief's scenarios
# ═══════════════════════════════════════════════════════════════════════════


def test_two_labels_answered_all_and_one_picked_produce_one_summary_and_one_gate(
    installed, monkeypatch, script
):
    three_labels(monkeypatch)
    answer_every_label()

    envelope = asked()

    shown = envelope["cause"]["detail"]["shown"]
    assert shown["labels_taking_releases"] == 3
    assert shown["releases"] == 4
    assert shown["tracks"] == 2 + 1 + 3 + 4
    assert shown["estimated_size"] == sync_cli.size_text(10 * 360 * sync_cli.BYTES_PER_SECOND)
    assert shown["labels_answered_not_now"] == 1
    assert shown["labels_answered_stop_following"] == 0
    assert shown["count"] == 4
    assert sorted(item["release"] for item in shown["items"]) == ["a1", "a2", "b1", "g1"]
    assert envelope["cause"]["detail"]["explicit"] is True
    assert fetched(script) == [] and our_jobs() == []

    land_every(script, ("a2", 2), ("a1", 1), ("b1", 3), ("g1", 4))
    run_id = envelope["run_id"]
    decided(run_id, "apply")
    code, done = gone(run_id)

    assert code == int(ExitCode.PENDING_HUMAN), done
    (job,) = our_jobs()
    assert job.state is jobs.JobState.SUCCEEDED
    assert len(item_states(job.job_id)) == 10
    assert sorted(fetched(script)) == sorted(script.landings)
    assert done["data"]["summary"]["go"]["job"] == job.job_id


def test_aborting_at_the_gate_downloads_nothing_and_keeps_the_answers(
    installed, monkeypatch, script
):
    three_labels(monkeypatch)
    answer_every_label()
    land_every(script, ("a2", 2), ("a1", 1), ("b1", 3), ("g1", 4))
    first = asked()
    decided(first["run_id"], "abort")

    code, envelope = gone(first["run_id"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert "nothing was downloaded" in check(envelope, "declined")["detail"]
    assert fetched(script) == [] and our_jobs() == []
    assert all(sync_cli.SETTLED not in one for one in record(installed)["answers"])
    later = asked()
    assert later["cause"]["detail"]["shown"]["digest"] == first["cause"]["detail"]["shown"]["digest"]


def test_a_job_stopped_halfway_resumes_and_downloads_only_the_rest(
    installed, monkeypatch, script
):
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 4)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 4))
    script.landings["t-r1-3"] = Landing(fetch_raises=cooldown(), fetch_raises_times=1)

    _run, code, envelope = approved_go()

    assert code != int(ExitCode.OK), envelope
    (job,) = our_jobs()
    assert item_states(job.job_id) == {
        "t-r1-1": jobs.ItemState.DONE,
        "t-r1-2": jobs.ItemState.DONE,
        "t-r1-3": jobs.ItemState.PENDING,
        "t-r1-4": jobs.ItemState.PENDING,
    }
    script.fetched.clear()

    resumed = asked()
    shown = resumed["cause"]["detail"]["shown"]
    assert shown["releases"] == 0 and shown["earlier_downloads_to_resume"] == 1
    decided(resumed["run_id"], "apply")
    code, envelope = gone(resumed["run_id"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r1-3", "t-r1-4"]
    assert our_jobs()[0].job_id == job.job_id and len(our_jobs()) == 1
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert check(envelope, f"resumed.{job.job_id}")["status"] == "ok"


def test_a_track_already_held_in_another_version_goes_to_the_match_queue_and_is_not_downloaded(
    installed, monkeypatch, script
):
    music = Path(installed.library.root) / "Music"
    (music / "Label Act - Harbour Lights (Someone Remix).flac").write_bytes(b"")
    register()
    fake = bind(monkeypatch, {"tide-works": [("r1", "2026", 2)]})
    fake.releases["r1"] = (
        [Track("t-r1-1", "Label Act", "Harbour Lights"), Track("t-r1-2", "Label Act", "Sun Path")],
        2026,
    )
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 2))

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r1-2"]
    (job,) = our_jobs()
    assert list(item_states(job.job_id)) == ["t-r1-2"]
    assert "1 held in another version" in check(envelope, "list.offered")["detail"]
    with review.open_store(installed) as store:
        offered_here = review.list_items(store, handler_key="label.sync").items
    assert [one.queue for one in offered_here] == [match_cli.QUEUE]


def cooldown() -> Parked:
    return Parked(
        Cause(
            reason="provider-cooldown",
            message="the streaming provider rate limited this account",
            remediation=Remediation(remedy=Remedy.RETRY_LATER),
            origin=("provider_gate",),
        )
    )


def test_a_rate_limit_refusal_parks_the_job(installed, monkeypatch, script):
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 3)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 3))
    script.landings["t-r1-2"] = Landing(fetch_raises=cooldown())

    _run, code, envelope = approved_go()

    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "blocked"
    assert envelope["cause"]["reason"] == "provider-cooldown"
    (job,) = our_jobs()
    assert job.state is jobs.JobState.BLOCKED
    assert fetched(script) == ["t-r1-1", "t-r1-2"], "a request followed the refusal"


def test_an_empty_set_of_answers_still_shows_the_summary_and_asks(installed, script):
    envelope = asked()

    shown = envelope["cause"]["detail"]["shown"]
    assert (shown["releases"], shown["tracks"], shown["count"]) == (0, 0, 0)
    assert shown["labels_taking_releases"] == 0
    assert shown["items"] == []

    decided(envelope["run_id"], "apply")
    code, done = gone(envelope["run_id"])

    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert our_jobs() == [] and fetched(script) == []


# ═══════════════════════════════════════════════════════════════════════════
# 2. What the go downloads, and what it never does
# ═══════════════════════════════════════════════════════════════════════════


def test_a_release_accepted_by_hand_and_answered_for_by_nobody_is_not_downloaded(
    installed, monkeypatch, script
):
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 1), ("r-hand", "2020", 2)]})
    hand = offered(installed, "r-hand")
    with review.open_store(installed) as store:
        review.resolve(store, hand, review.Verdict.ACCEPTED, actor="a-person")
    question = next_question()
    answer("tide-works", "pick", "r1")
    land_every(script, ("r1", 1), ("r-hand", 2))
    assert {one["identity"] for one in question["releases"]} >= {"r1"}

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r1-1"]


def test_a_release_cleared_after_answering_is_named_and_not_downloaded(
    installed, monkeypatch, script
):
    register()
    bind(monkeypatch, {"tide-works": [("r2", "2026", 1), ("r1", "2025", 1)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r2", 1), ("r1", 1))
    with review.open_store(installed) as store:
        review.clear(store, go.genre_gate.release_item_id("r1"), actor="a-person")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r2-1"]
    assert "Tide Works r1" in check(envelope, "withdrawn")["detail"]
    assert envelope["data"]["summary"]["go"]["withdrawn"] == ["r1"]


def test_an_answer_saved_after_the_decision_makes_the_decision_stale(
    installed, monkeypatch, script
):
    three_labels(monkeypatch)
    next_question()
    answer("alpha-works", "all")
    run_id = asked()["run_id"]
    decided(run_id, "apply")
    next_question()
    answer("beta-works", "all")

    code, envelope = gone(run_id)

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "decision-stale"
    assert our_jobs() == [] and fetched(script) == []


def test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice(
    installed, monkeypatch, script
):
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 2)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 2))

    def killed(*_args, **_kwargs):
        raise KeyboardInterrupt

    with monkeypatch.context() as patched:
        patched.setattr(sync_cli, "settle_in", killed)
        with pytest.raises(KeyboardInterrupt):
            approved_go()
    (job,) = our_jobs()
    assert fetched(script) == []
    assert all(sync_cli.SETTLED not in one for one in record(installed)["answers"])

    again = asked()
    shown = again["cause"]["detail"]["shown"]
    assert shown["releases"] == 1 and shown["earlier_downloads_to_resume"] == 1
    decided(again["run_id"], "apply")
    code, envelope = gone(again["run_id"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert sorted(fetched(script)) == ["t-r1-1", "t-r1-2"]
    assert "1 answer(s) wait for the next go" in check(envelope, "waiting")["detail"]
    landed_by_hand(installed, job.payload[go.ORIGIN_KEY]["run"])

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.OK), envelope
    assert sorted(fetched(script)) == ["t-r1-1", "t-r1-2"], "a track was asked for twice"
    assert [one.job_id for one in our_jobs()] == [job.job_id]
    assert "2 track(s) an earlier go already holds" in check(envelope, "held-by-a-go")["detail"]
    assert all(one[sync_cli.SETTLED] for one in record(installed)["answers"])


def test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new(
    installed, monkeypatch, script
):
    """One job per go, so one manifest and one landing per go (the review's second finding)."""
    register("Alpha Works")
    register("Beta Works")
    bind(monkeypatch, {"alpha-works": [("a1", "2026", 2)], "beta-works": [("b1", "2026", 1)]})
    next_question()
    answer("alpha-works", "all")
    land_every(script, ("a1", 2), ("b1", 1))
    script.landings["t-a1-2"] = Landing(fetch_raises=cooldown(), fetch_raises_times=1)
    approved_go()
    (first,) = our_jobs()
    next_question()
    answer("beta-works", "all")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert [one.job_id for one in our_jobs()] == [first.job_id]
    assert "t-b1-1" not in fetched(script)
    (landing,) = [one for one in envelope["data"]["summary"]["go"]["next"] if "intake land" in one]
    assert first.payload[go.ORIGIN_KEY]["manifest"] in landing
    landed_by_hand(installed, first.payload[go.ORIGIN_KEY]["run"])

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script)[-1] == "t-b1-1"
    assert len(our_jobs()) == 2


def test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures(
    installed, monkeypatch, script
):
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 3)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 3))
    script.landings["t-r1-2"] = Landing(
        fetch_raises=RuntimeError("connection reset by peer"), fetch_raises_times=99
    )

    _run, code, envelope = approved_go()

    assert code != int(ExitCode.OK), envelope
    (job,) = our_jobs()
    assert job.state is jobs.JobState.FAILED
    assert item_states(job.job_id)["t-r1-2"] is jobs.ItemState.FAILED
    script.landings["t-r1-2"] = Landing()
    script.fetched.clear()

    resumed = asked()
    assert resumed["cause"]["detail"]["shown"]["earlier_downloads_to_resume"] == 1
    decided(resumed["run_id"], "apply")
    code, envelope = gone(resumed["run_id"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r1-2"]
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}


def test_a_release_gone_from_the_provider_does_not_refuse_every_go_after_it(
    installed, monkeypatch, script
):
    """The review's fourth finding: nothing listed beside a gone release was a refusal."""
    register()
    fake = bind(monkeypatch, {"tide-works": [("r2", "2026", 1), ("r1", "2025", 1)]})
    next_question()
    answer("tide-works", "all")
    del fake.releases["r1"]
    (Path(installed.library.root) / "Music" / "Label Act - Cut 1 of r2.flac").write_bytes(b"")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.OK), envelope
    assert fetched(script) == [] and our_jobs() == []
    (gone_line,) = [
        one for one in envelope["data"]["checks"] if one["key"] == "label.sync.go.list.release.r1"
    ]
    assert gone_line["status"] == "fail" and "crate review clear" in gone_line["detail"]
    assert all(one[sync_cli.SETTLED] for one in record(installed)["answers"])


def test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again(
    installed, monkeypatch, script
):
    """The review's fifth finding, the race, driven by letting the summary miss
    the job another go queued while this one waited for the record's lock."""
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 1)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 1))
    with monkeypatch.context() as patched:
        patched.setattr(sync_cli, "settle_in", lambda *_a, **_k: (_ for _ in ()).throw(KeyboardInterrupt))
        with pytest.raises(KeyboardInterrupt):
            approved_go()
    real = go.held_by_goes
    calls = []

    def first_blind(store):
        # BLIND FOR BOTH SUMMARIES, the one the gate is asked over and the one
        # the go rebuilds, so the gate's own digest agrees and the refusal
        # measured is the one under the lock (mutation row G11).
        calls.append(1)
        return go.Held(resume=(), tracks=frozenset()) if len(calls) <= 2 else real(store)

    monkeypatch.setattr(go, "held_by_goes", first_blind)

    _run, code, envelope = approved_go()

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "decision-stale"
    assert len(our_jobs()) == 1 and fetched(script) == []


def test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go(
    installed, monkeypatch, script
):
    register()
    fake = bind(monkeypatch, {"tide-works": [("r2", "2026", 1), ("r1", "2025", 1)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r2", 1), ("r1", 1))
    reader = fake.release_tracks

    def flaky(release_id):
        if release_id == "r1":
            raise RuntimeError("the provider did not answer")
        return reader(release_id)

    monkeypatch.setattr(fake, "release_tracks", flaky)

    first_run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r2-1"]
    assert check(envelope, "carried")["status"] == "fail"
    assert all(sync_cli.SETTLED not in one for one in record(installed)["answers"])
    landed_by_hand(installed, first_run)

    monkeypatch.setattr(fake, "release_tracks", reader)
    script.fetched.clear()
    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r1-1"]
    assert all(one[sync_cli.SETTLED] for one in record(installed)["answers"])


def test_a_settled_answer_is_not_summarised_again(installed, monkeypatch, script):
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 1)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 1))
    run_id, _code, _envelope = approved_go()
    landed_by_hand(installed, run_id)

    shown = asked()["cause"]["detail"]["shown"]

    assert (shown["releases"], shown["labels_taking_releases"]) == (0, 0)


# ═══════════════════════════════════════════════════════════════════════════
# 3. How it lands, and how the walk reaches it
# ═══════════════════════════════════════════════════════════════════════════


def test_the_download_lands_as_an_intake_under_the_runs_one_batch(installed, monkeypatch, script):
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 2)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 2))

    run_id, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    report = envelope["data"]["summary"]["go"]
    rows = listdoc.read_manifest(Path(report["manifest"]))
    assert sorted(row.ref for row in rows) == ["t-r1-1", "t-r1-2"]
    assert {row.provenance.source for row in rows} == {approved_cli.LABEL_SOURCE}
    assert {row.provenance.label_id for row in rows} == {"tide-works"}
    assert {row.provenance.year for row in rows} == {2026}
    (job,) = our_jobs()
    assert job.payload[go.RUN_KEY] == run_id
    assert job.payload[go.ORIGIN_KEY]["manifest"] == report["manifest"]
    staging = str(installed.paths.download_staging)
    assert report["next"][-1] == (
        f"crate intake land {staging} --manifest {report['manifest']} "
        f"--pass {default_name(run_id)}"
    )
    assert report["next"][0] == f"crate tag folder {staging}"
    for track in ("t-r1-1", "t-r1-2"):
        assert (Path(staging) / f"{track}.wav").is_file()


def test_the_walk_ends_at_the_gate_and_a_yes_downloads_what_it_answered(
    installed, monkeypatch, script
):
    from tests.test_label_sync import script as scripted

    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 1)]})
    scripted(monkeypatch, "all")
    land_every(script, ("r1", 1))

    code, envelope = drive(["label", "sync"])

    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    shown = envelope["cause"]["detail"]["shown"]
    assert shown["answered_this_run"][0].startswith("Tide Works: all")
    assert shown["releases"] == 1
    assert fetched(script) == []
    decided(envelope["run_id"], "apply")

    code, done = gone(envelope["run_id"])

    assert code == int(ExitCode.PENDING_HUMAN), done
    assert fetched(script) == ["t-r1-1"]


def test_the_estimated_time_is_the_pacing_and_the_transfer_of_the_size():
    summary = go.Summary(
        answers=(),
        taken=(
            go.Taken("l", "L", "r", "i", "", "", "", tracks=10, size=25_000_000),
        ),
        taking=("L",),
        not_now=(),
        stopped=(),
        open_jobs=(),
        pace_s=6.0,
    )

    assert summary.seconds == 10 * 6 + 25_000_000 // go.TRANSFER_BYTES_PER_SECOND
    assert go.duration_text(summary.seconds) == "about 1 min"
    assert go.duration_text(3 * 3600 + 25 * 60) == "about 3 h 25 min"


def test_a_go_job_whose_track_was_refused_for_good_is_not_resumed(
    installed, monkeypatch, script
):
    """A delisted track is settled, not failed, since U169, so the job that
    holds it succeeded and a later go has nothing of it to resume."""
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 2)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 2))
    script.landings["t-r1-2"] = Landing(offer_raises=LookupError("404 not found"))

    run_id, _code, _envelope = approved_go()
    landed_by_hand(installed, run_id)

    (job,) = our_jobs()
    assert job.state is jobs.JobState.SUCCEEDED, job
    with jobs.open_store() as store:
        skipped = [i for i in jobs.items(store, job.job_id) if i.state is jobs.ItemState.SKIPPED]
    assert [i.cause.reason for i in skipped if i.cause] == ["unavailable-permanent"]
    script.fetched.clear()

    shown = asked()["cause"]["detail"]["shown"]

    assert "earlier_downloads_to_resume" not in shown
    assert shown["releases"] == 0


def test_a_go_job_whose_failures_cannot_succeed_on_a_retry_is_not_resumed(installed):
    """Mutation row G14: a cause that says no retry can succeed is not retried.

    Driven at ``resumable`` since U169, because the delisted track the driven
    form used is now declined and its job succeeds; a failed job with a
    permanent cause is still a state an earlier build recorded, and a refusal
    outside the policy class (``output-exists``) still produces one.
    """
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key=go.DOWNLOAD, payload={}, cfg=config.load(), item_ids=("a",)
        )
    permanent = refuse("output-exists", "a file is already there").cause
    transient = refuse("unavailable-transient", "later", retryable=True).cause

    stopped = dataclasses.replace(job, state=jobs.JobState.FAILED, cause=permanent)
    retryable = dataclasses.replace(job, state=jobs.JobState.FAILED, cause=transient)
    unexplained = dataclasses.replace(job, state=jobs.JobState.FAILED, cause=None)
    finished = dataclasses.replace(job, state=jobs.JobState.SUCCEEDED, cause=None)

    assert go.resumable(stopped, 1) is False
    assert go.resumable(retryable, 1) is True
    assert go.resumable(unexplained, 1) is True
    assert go.resumable(finished, 1) is False
    assert go.resumable(job, 1) is True, "an open job is always resumed"


def test_a_download_queued_by_hand_is_not_resumed_or_held_by_a_go(
    installed, monkeypatch, script, tmp_path
):
    """Mutation row G16: only a job a go queued is a go's to resume."""
    listed = tmp_path / "by-hand.json"
    listed.write_text(tidal_list([("x1", "Other Act", "Elsewhere")]))
    code, queued = drive(["acquire", "download", str(listed)])
    assert code == int(ExitCode.OK), queued
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 1)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 1))

    shown = asked()["cause"]["detail"]["shown"]
    assert "earlier_downloads_to_resume" not in shown

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r1-1"]
    with jobs.open_store() as store:
        assert jobs.get(store, queued["data"]["job_id"]).state is jobs.JobState.QUEUED


def test_settling_leaves_an_answer_whose_place_now_holds_a_different_one():
    """Mutation row G18: a record rewritten while a go waited is not settled blind."""
    document = {
        "answers": [
            {"label_id": "tide-works", "answered_at": "2026-10-03T01:00:00Z", "answer": "all"},
            {"label_id": "beta-works", "answered_at": "2026-10-03T02:00:00Z", "answer": "all"},
        ]
    }

    settled = sync_cli.settle_in(
        document,
        [(0, "tide-works", "2026-10-03T01:00:00Z"), (1, "alpha-works", "2026-10-03T02:00:00Z")],
        marker={"run": "r", "job": None},
    )

    assert settled == 1
    assert sync_cli.SETTLED in document["answers"][0]
    assert sync_cli.SETTLED not in document["answers"][1]


def test_settling_an_answer_already_settled_keeps_its_first_marker():
    """Mutation row G20: the job an answer went with is not overwritten by a later go."""
    first = {"run": "first", "job": "job-1", "at": "2026-10-03T01:00:00Z"}
    document = {
        "answers": [
            {
                "label_id": "tide-works",
                "answered_at": "2026-10-03T01:00:00Z",
                "answer": "all",
                sync_cli.SETTLED: first,
            }
        ]
    }

    settled = sync_cli.settle_in(
        document, [(0, "tide-works", "2026-10-03T01:00:00Z")], marker={"run": "second", "job": None}
    )

    assert settled == 0
    assert document["answers"][0][sync_cli.SETTLED] == first


# ═══════════════════════════════════════════════════════════════════════════
# 4. U190: the go runs the tail and stops at the landing's gate
# ═══════════════════════════════════════════════════════════════════════════


def two_releases_answered(monkeypatch, script) -> None:
    """Two labels answered ``all``, one release each, every track downloadable."""
    register("Alpha Works")
    register("Beta Works")
    bind(monkeypatch, {"alpha-works": [("a1", "2026", 2)], "beta-works": [("b1", "2026", 1)]})
    next_question()
    answer("alpha-works", "all")
    next_question()
    answer("beta-works", "all")
    land_every(script, ("a1", 2), ("b1", 1))


def staged(cfg: config.Config) -> str:
    return str(Path(cfg.paths.download_staging).expanduser().absolute())


def chain_check(envelope: dict, step: str) -> dict:
    """One of the chain's checks, from the envelope or from a refusal's detail."""
    cause = envelope.get("cause") or {}
    data = (cause.get("detail") or {}).get("label_sync") or envelope["data"]
    (found,) = [one for one in data["checks"] if one["key"] == f"label.sync.go.{step}"]
    return found


def test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate(
    installed, monkeypatch, script, tail
):
    two_releases_answered(monkeypatch, script)

    run_id, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == "pending"
    assert sorted(fetched(script)) == ["t-a1-1", "t-a1-2", "t-b1-1"]
    folder = staged(installed)
    manifest = envelope["data"]["summary"]["go"]["manifest"]
    assert tail.verbs() == [
        ("tag", "folder"),
        ("tag", "folder"),
        ("tag", "guess"),
        ("analyze", "run"),
        ("analyze", "run"),
        ("analyze", "restamp"),
        ("analyze", "restamp"),
        ("name", "apply"),
        ("intake", "land"),
    ]
    # U172: the genre guess runs over the same folder, with no pass: the go's
    # pass names its landing, and no account playlist asked for a label's tracks.
    (guessed,) = [argv for argv in tail.calls if argv[:2] == ["tag", "guess"]]
    assert guessed == ["tag", "guess", folder]
    queued = [
        argv for argv in tail.calls if "--job" not in argv and argv[:2] != ["tag", "guess"]
    ]
    assert [argv[-1] for argv in queued[:3]] == [folder] * 3, "the tail ran on another folder"
    assert tail.calls[-1] == [
        "intake", "land", folder, "--manifest", manifest, "--pass", default_name(run_id),
    ]
    for step in (tail_chain.TAG, tail_chain.ANALYZE, tail_chain.RESTAMP, tail_chain.NAME):
        assert chain_check(envelope, step)["status"] == "ok", step
    assert "next" not in {one["title"] for one in envelope["data"]["checks"]}, (
        "the go still told a person to type the tail it ran"
    )


def test_the_landing_gates_run_is_named_in_the_envelope_with_the_commands_that_answer_it(
    installed, monkeypatch, script, tail
):
    two_releases_answered(monkeypatch, script)

    run_id, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    pending = envelope["pending_human_action"]
    assert pending["kind"] == "external_step"
    assert pending["verify_verb"] == tail_chain.LAND_VERB
    assert pending["id"] == f"label-sync-{run_id}"
    steps = pending["steps"]
    assert steps[0].endswith(
        f"crate run decide land-run {tail_chain.LAND_GATE} {tail_chain.LAND_OPTION} "
        f"--actor {tail_chain.SESSION_ACTOR}"
    )
    manifest = envelope["data"]["summary"]["go"]["manifest"]
    assert steps[1] == (
        f"apply it: crate --run land-run intake land {staged(installed)} --manifest "
        f"{manifest} --pass {default_name(run_id)}"
    )
    assert tuple(steps[2:]) == tail_chain.REKORDBOX_STEPS
    assert envelope["data"]["summary"]["tail"]["gate_run"] == "land-run"
    assert envelope["data"]["summary"]["tail"]["stopped_at"] == tail_chain.LAND_GATE
    assert "land-run" in pending["summary"]


def test_name_apply_has_its_confirm_answered_inline_over_the_absolute_staging_folder(
    installed, monkeypatch, script, tail
):
    """The literal rule, which ``tests/test_sync_land.py`` pins for sync land's call too."""
    two_releases_answered(monkeypatch, script)

    approved_go()

    (named,) = tail.named
    assert named == [
        "-d", "name.apply.confirm=apply", "name", "apply", "--root", staged(installed),
    ]


def test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail(
    installed, monkeypatch, script, tail
):
    two_releases_answered(monkeypatch, script)
    real = tail._job

    def gated(step, verb, argv):
        if step == tail_chain.RESTAMP and "--job" not in argv:
            return _refused(
                Cause(
                    reason="decision-required",
                    message="analyze.restamp.confirm needs a recorded decision",
                    remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
                    retryable=True,
                    origin=("test",),
                    detail={"gate": "analyze.restamp.confirm", "options": ["apply"],
                            "run_id": "restamp-run"},
                ),
                outcome="blocked",
            )
        return real(step, verb, argv)

    monkeypatch.setattr(tail, "_job", gated)

    run_id, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    pending = envelope["pending_human_action"]
    assert pending["verify_verb"] == "label.sync", "the go's own verb continues, not the landing"
    folder = staged(installed)
    manifest = envelope["data"]["summary"]["go"]["manifest"]
    assert "crate run decide restamp-run analyze.restamp.confirm" in pending["steps"][0]
    assert pending["steps"][2:] == [
        f"then: crate name apply --root {folder}",
        f"then: crate intake land {folder} --manifest {manifest} --pass {default_name(run_id)}",
    ]
    assert not tail.named and ("intake", "land") not in tail.verbs()


def test_a_landing_that_planned_nothing_ends_the_go_with_its_own_outcome(
    installed, monkeypatch, script, tail
):
    two_releases_answered(monkeypatch, script)
    tail.landing = lambda _argv: _ok({"items": []}, outcome="no_op")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok" and envelope["pending_human_action"] is None
    assert envelope["data"]["summary"]["tail"]["stopped_at"] == tail_chain.LAND
    assert chain_check(envelope, tail_chain.LAND)["detail"] == "intake land planned nothing to land"


def test_the_chain_runs_on_the_absolute_folder_whatever_it_is_handed(
    installed, monkeypatch, tail
):
    monkeypatch.chdir(Path(installed.library.root))
    chain = tail_chain.Chain(
        progress=None, namespace="t", title="t", steps=tail_chain.STEPS,
        origin=("test",), again="again",
    )
    relative = Path("staged-here")
    relative.mkdir()

    with pytest.raises(tail_chain.Stop):
        tail_chain.run(chain, relative, installed, ["--pass", "p"])

    absolute = str(Path(installed.library.root) / "staged-here")
    assert chain.summary["staging"] == absolute
    assert tail.calls[0] == ["tag", "folder", "--queue-only", absolute]


def test_a_failing_analyze_run_stops_the_go_and_plans_no_landing(
    installed, monkeypatch, script, tail
):
    two_releases_answered(monkeypatch, script)

    def broken(_job, item):
        raise refuse(
            "module-extras-missing",
            f"the analysis extra is not importable for {item.item_id}",
            scope=Scope.ITEM,
            origin=("test",),
        )

    tail.work[tail_chain.ANALYZE] = broken

    run_id, code, envelope = approved_go()

    assert code == int(ExitCode.MODULE_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "module-extras-missing"
    assert "label.sync.go" in envelope["cause"]["origin"]
    assert ("analyze", "restamp") not in tail.verbs()
    assert not tail.named, "name apply ran after a failed analysis"
    assert ("intake", "land") not in tail.verbs(), "a landing was planned over an unfinished tail"
    assert chain_check(envelope, tail_chain.TAG)["status"] == "ok"
    assert chain_check(envelope, tail_chain.ANALYZE)["status"] == "fail"
    folder = staged(installed)
    (way_on,) = [
        step for step in envelope["cause"]["remediation"]["steps"] if "rest of the tail" in step
    ]
    assert way_on.endswith(
        f"crate analyze run {folder}; then crate analyze restamp {folder}; then crate name "
        f"apply --root {folder}; then crate intake land {folder} --manifest "
        f"{envelope['cause']['detail']['label_sync']['summary']['go']['manifest']} --pass "
        f"{default_name(run_id)}"
    )
    assert sorted(fetched(script)) == ["t-a1-1", "t-a1-2", "t-b1-1"], "the download was lost"


def test_a_stale_tag_job_over_the_staging_folder_is_replaced_not_resumed(
    installed, monkeypatch, script, tail
):
    two_releases_answered(monkeypatch, script)
    folder = Path(staged(installed))
    folder.mkdir(parents=True, exist_ok=True)
    key = registry.entry("tag.folder").handler_key
    with jobs.open_store() as store:
        stale = jobs.enqueue(
            store,
            handler_key=key,
            payload={"folder": str(folder)},
            cfg=installed,
            item_ids=("old.wav",),
        )

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    with jobs.open_store() as store:
        assert jobs.get(store, stale.job_id).state is jobs.JobState.CANCELLED
        fresh = [
            job
            for job in jobs.list_jobs(store)
            if job.handler_key == key and job.job_id != stale.job_id
        ]
    assert {"step": "tag", "job_id": stale.job_id} in envelope["data"]["summary"]["tail"][
        "replaced"
    ]
    assert not any(stale.job_id in argv for argv in tail.calls), "the stale job was resumed"
    assert len(fresh) == 1 and fresh[0].state is jobs.JobState.SUCCEEDED


def test_a_go_with_every_track_already_owned_runs_no_tail(installed, monkeypatch, script, tail):
    """Both tracks reach the library between the answer and the go, so none is listed."""
    register()
    fake = bind(monkeypatch, {"tide-works": [("r1", "2026", 2)]})
    fake.releases["r1"] = (
        [Track("t-r1-1", "Label Act", "Harbour Lights"), Track("t-r1-2", "Label Act", "Sun Path")],
        2026,
    )
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 2))
    music = Path(installed.library.root) / "Music"
    (music / "Label Act - Harbour Lights.flac").write_bytes(b"")
    (music / "Label Act - Sun Path.flac").write_bytes(b"")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.OK), envelope
    assert fetched(script) == [] and our_jobs() == []
    assert tail.calls == [], "the tail ran over a go that downloaded nothing"
    assert envelope["data"]["summary"]["go"][go.LAND_KEY] is None
    assert "tail" not in envelope["data"]["summary"]


def test_a_declined_go_runs_no_tail(installed, monkeypatch, script, tail):
    two_releases_answered(monkeypatch, script)
    run_id = asked()["run_id"]
    decided(run_id, "abort")

    code, envelope = gone(run_id)

    assert code == int(ExitCode.OK), envelope
    assert fetched(script) == [] and tail.calls == []


def test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass(
    installed, monkeypatch, script, tail
):
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 2)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", 2))
    script.landings["t-r1-2"] = Landing(fetch_raises=cooldown(), fetch_raises_times=1)
    first_run, code, _parked = approved_go()
    assert code != int(ExitCode.PENDING_HUMAN) and tail.calls == []
    (first,) = our_jobs()

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert tail.calls[-1] == [
        "intake", "land", staged(installed),
        "--manifest", first.payload[go.ORIGIN_KEY]["manifest"],
        "--pass", default_name(first_run),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 5. R-1115: a track refused for good is named and skipped, and the rest lands
# ═══════════════════════════════════════════════════════════════════════════


def one_release_answered(monkeypatch, script, tracks: int = 2) -> None:
    """One label answered ``all``, one release of ``tracks`` tracks, each downloadable."""
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", tracks)]})
    next_question()
    answer("tide-works", "all")
    land_every(script, ("r1", tracks))


def already_staged(monkeypatch, cfg: config.Config, *track_ids: str) -> None:
    """A file at each track's staging name while the go downloads, refused ``output-exists``.

    THE FILE IS MOVED OUT AGAIN ONCE THE DRIVE RETURNS. R-1115 left it in the
    folder for good; since R-1467 a file there that no download of the go's
    put there refuses the go, before its gate and before its tail, since the
    landing would take it with the go's own. What these tests read is how a
    download failed only by such a refusal settles, so the file is there for
    the drive and gone when the go reads the folder.
    """
    folder = Path(staged(cfg))
    real = go._drive

    def kept(ctx, store, job_id):
        folder.mkdir(parents=True, exist_ok=True)
        for track_id in track_ids:
            (folder / f"{track_id}.wav").write_bytes(b"kept on purpose")
        try:
            return real(ctx, store, job_id)
        finally:
            for track_id in track_ids:
                (folder / f"{track_id}.wav").unlink(missing_ok=True)

    monkeypatch.setattr(go, "_drive", kept)


def refused_ids(envelope: dict) -> list[str]:
    cause = envelope.get("cause") or {}
    data = (cause.get("detail") or {}).get("label_sync") or envelope["data"]
    return [row["item_id"] for row in data["summary"]["go"]["refused"]]


def test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it(
    installed, monkeypatch, script, tail
):
    one_release_answered(monkeypatch, script)
    script.landings["t-r1-2"] = Landing(kind="lossy")

    run_id, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == "pending"
    assert tail.calls[-1] == [
        "intake", "land", staged(installed),
        "--manifest", envelope["data"]["summary"]["go"]["manifest"],
        "--pass", default_name(run_id),
    ], "the tail did not run on to the landing"
    downloaded = check(envelope, "downloaded")
    assert downloaded["status"] == "ok"
    assert "1 of 2 track(s) downloaded" in downloaded["detail"]
    assert "1 refused for good and skipped" in downloaded["detail"]
    assert "t-r1-2 (lossy-refused)" in downloaded["detail"]
    assert refused_ids(envelope) == ["t-r1-2"]
    assert any(
        "t-r1-2" in warning["message"] and "lossy-refused" in warning["message"]
        for warning in envelope["warnings"]
    ), envelope["warnings"]
    assert "next" not in {one["title"] for one in envelope["data"]["checks"]}


def test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so(
    installed, monkeypatch, script, tail
):
    one_release_answered(monkeypatch, script)
    script.landings["t-r1-1"] = Landing(kind="lossy")
    script.landings["t-r1-2"] = Landing(kind="lossy")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.OK), envelope
    assert tail.calls == [], "the tail ran over a download that landed nothing"
    downloaded = check(envelope, "downloaded")
    assert downloaded["status"] == "fail"
    assert "0 of 2 track(s) downloaded" in downloaded["detail"]
    assert "every track was refused for good, so no tail was run" in downloaded["detail"]
    assert sorted(refused_ids(envelope)) == ["t-r1-1", "t-r1-2"]
    go_report = envelope["data"]["summary"]["go"]
    assert go_report[go.LAND_KEY] is None and go_report["next"] == []
    assert "next" not in {one["title"] for one in envelope["data"]["checks"]}, (
        "the go named a tail to type over a folder nothing landed in"
    )


def test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest(
    installed, monkeypatch, script, tail
):
    """The FAILED half of the rule ``sync land`` reads: ``output-exists`` is not
    the policy's class, so the item fails rather than being declined, and the
    job ends FAILED with one track done."""
    one_release_answered(monkeypatch, script)
    already_staged(monkeypatch, installed, "t-r1-2")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    (job,) = our_jobs()
    assert job.state is jobs.JobState.FAILED, job
    assert item_states(job.job_id) == {
        "t-r1-1": jobs.ItemState.DONE, "t-r1-2": jobs.ItemState.FAILED,
    }
    assert ("intake", "land") in tail.verbs()
    assert refused_ids(envelope) == ["t-r1-2"]
    assert "t-r1-2 (output-exists)" in check(envelope, "downloaded")["detail"]
    (warning,) = [w for w in envelope["warnings"] if w["code"] == go.REFUSED_WARNING]
    assert "t-r1-2" in warning["message"] and "output-exists" in warning["message"]


def test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so(
    installed, monkeypatch, script, tail
):
    """The engine raises inside the drive when every attempted item failed, so
    the go reads the job back off the queue rather than the refusal."""
    one_release_answered(monkeypatch, script, tracks=1)
    already_staged(monkeypatch, installed, "t-r1-1")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.OK), envelope
    (job,) = our_jobs()
    assert job.state is jobs.JobState.FAILED, job
    assert tail.calls == []
    assert check(envelope, "downloaded")["status"] == "fail"
    assert refused_ids(envelope) == ["t-r1-1"]


def test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail(
    installed, monkeypatch, script, tail
):
    one_release_answered(monkeypatch, script)
    script.landings["t-r1-2"] = Landing(
        fetch_raises=RuntimeError("connection reset by peer"), fetch_raises_times=99
    )

    _run, code, envelope = approved_go()

    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "failed"
    assert envelope["cause"]["retryable"] is True
    (job,) = our_jobs()
    assert job.state is jobs.JobState.FAILED
    assert tail.calls == [], "a retryable failure was read as refused for good"


def test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest(
    installed, monkeypatch, script, tail
):
    one_release_answered(monkeypatch, script)
    script.landings["t-r1-2"] = Landing(fetch_raises=cooldown(), fetch_raises_times=1)
    first_run, code, _parked = approved_go()
    assert code != int(ExitCode.PENDING_HUMAN) and tail.calls == []
    (first,) = our_jobs()
    already_staged(monkeypatch, installed, "t-r1-2")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert jobs.JobState.FAILED is our_jobs()[0].state
    assert tail.calls[-1] == [
        "intake", "land", staged(installed),
        "--manifest", first.payload[go.ORIGIN_KEY]["manifest"],
        "--pass", default_name(first_run),
    ]
    assert any(
        w["code"] == go.REFUSED_WARNING and "t-r1-2" in w["message"]
        for w in envelope["warnings"]
    ), envelope["warnings"]


@pytest.mark.parametrize(
    "state, items, settled",
    [
        pytest.param(
            jobs.JobState.FAILED,
            ((jobs.ItemState.DONE, None), (jobs.ItemState.FAILED, "permanent")),
            True,
            id="failed-only-by-a-refusal",
        ),
        pytest.param(
            jobs.JobState.FAILED,
            ((jobs.ItemState.DONE, None), (jobs.ItemState.FAILED, "transient")),
            False,
            id="a-failure-a-retry-could-clear",
        ),
        pytest.param(
            jobs.JobState.FAILED,
            ((jobs.ItemState.DONE, None), (jobs.ItemState.FAILED, None)),
            False,
            id="a-failure-recording-no-cause",
        ),
        pytest.param(
            jobs.JobState.FAILED,
            ((jobs.ItemState.DONE, None), (jobs.ItemState.SKIPPED, "permanent")),
            False,
            id="failed-with-no-failed-track",
        ),
        pytest.param(
            jobs.JobState.FAILED,
            ((jobs.ItemState.FAILED, "permanent"), (jobs.ItemState.PENDING, None)),
            False,
            id="a-track-never-attempted",
        ),
        pytest.param(
            jobs.JobState.SUCCEEDED,
            ((jobs.ItemState.DONE, None), (jobs.ItemState.SKIPPED, "permanent")),
            True,
            id="succeeded-with-a-declined-track",
        ),
        pytest.param(
            jobs.JobState.CANCELLED,
            ((jobs.ItemState.DONE, None), (jobs.ItemState.FAILED, "permanent")),
            False,
            id="cancelled",
        ),
    ],
)
def test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry(
    installed, monkeypatch, state, items, settled
):
    """R-1115's one reading, read at the function: a FAILED job settles only when
    every track it did not land carries a cause no retry can clear."""
    causes = {
        "permanent": refuse("output-exists", "a file is already there").cause,
        "transient": refuse("unavailable-transient", "later", retryable=True).cause,
        None: None,
    }
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key=go.DOWNLOAD, payload={}, cfg=config.load(), item_ids=("a",)
        )
        job = dataclasses.replace(job, state=state)
        held = [
            jobs.Item(job_id=job.job_id, item_id=f"i{n}", ordinal=n, state=item_state,
                      cause=causes[cause])
            for n, (item_state, cause) in enumerate(items, start=1)
        ]
        monkeypatch.setattr(jobs, "items", lambda _store, _job_id: held)
        read = acquire_cli.read_download(store, job)

    assert read.settled is settled
    assert read.done == sum(1 for one, _cause in items if one is jobs.ItemState.DONE)
    assert read.landed is (settled and read.done > 0)
    if settled:
        assert [row["item_id"] for row in read.refused] == [
            f"i{n}" for n, (_s, cause) in enumerate(items, start=1) if cause == "permanent"
        ]


def test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so(
    installed, monkeypatch, script, tail
):
    """The resume twin of the every track refused scenario, the review's row 1."""
    one_release_answered(monkeypatch, script, tracks=1)
    script.landings["t-r1-1"] = Landing(fetch_raises=cooldown(), fetch_raises_times=1)
    _first, code, _parked = approved_go()
    assert code != int(ExitCode.PENDING_HUMAN) and tail.calls == []
    (first,) = our_jobs()
    already_staged(monkeypatch, installed, "t-r1-1")

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.OK), envelope
    assert tail.calls == [], "the tail ran over a resumed download that landed nothing"
    resumed = check(envelope, f"resumed.{first.job_id}")
    assert resumed["status"] == "fail"
    assert "every track was refused for good, so no tail was run" in resumed["detail"]
    go_report = envelope["data"]["summary"]["go"]
    assert go_report[go.LAND_KEY] is None and go_report["next"] == []
    assert refused_ids(envelope) == ["t-r1-1"]
    assert "next" not in {one["title"] for one in envelope["data"]["checks"]}


@pytest.mark.parametrize(
    "state",
    [state for state in jobs.JobState if state not in (jobs.JobState.SUCCEEDED, jobs.JobState.FAILED)],
)
def test_no_state_but_succeeded_or_failed_settles_a_download(installed, monkeypatch, state):
    """Derived from the enum, so a state added later is read here the day it is added."""
    permanent = refuse("output-exists", "a file is already there").cause
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key=go.DOWNLOAD, payload={}, cfg=config.load(), item_ids=("a",)
        )
        held = [
            jobs.Item(job_id=job.job_id, item_id="i1", ordinal=1, state=jobs.ItemState.DONE),
            jobs.Item(job_id=job.job_id, item_id="i2", ordinal=2, state=jobs.ItemState.FAILED,
                      cause=permanent),
        ]
        monkeypatch.setattr(jobs, "items", lambda _store, _job_id: held)
        read = acquire_cli.read_download(store, dataclasses.replace(job, state=state))

    assert read.settled is False and read.landed is False


# ═══════════════════════════════════════════════════════════════════════════
# 6. U239: a go stopped at the call ceiling finishes its tail on the next go
# ═══════════════════════════════════════════════════════════════════════════


def ceiling() -> Parked:
    """The provider gate's own park at the call ceiling, met by a fetch part way."""
    return Parked(
        Cause(
            reason=provider_gate.CEILING,
            message="this command made 500 calls to the streaming provider, so it stopped",
            remediation=Remediation(
                remedy=Remedy.FIX_COMMAND_LINE,
                steps=(
                    "continue with a higher ceiling for one run",
                    "or raise [provider] calls_per_command in the configuration for every run",
                ),
            ),
            retryable=False,
            origin=("provider_gate",),
            detail={"calls": 500, "ceiling": 500, "raised": False, "higher": 1000},
        )
    )


def stopped_at_the_ceiling(monkeypatch, script, *, label: str = "tide-works") -> tuple[str, dict]:
    """One release of three tracks answered, its go stopped by the ceiling at the second."""
    if label == "tide-works":
        one_release_answered(monkeypatch, script, tracks=3)
        key = "t-r1-2"
    else:
        key = "t-a1-2"
    script.landings[key] = Landing(fetch_raises=ceiling(), fetch_raises_times=1)
    run_id, code, envelope = approved_go()
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["reason"] == provider_gate.CEILING
    return run_id, envelope


def finished_by_hand(job_id: str) -> None:
    """The job driven to the end the way ``job resume``'s detached worker drives it."""
    code, envelope = drive(["acquire", "download", "--job", job_id])
    assert code == int(ExitCode.OK), envelope
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.SUCCEEDED


def landing_argv(cfg: config.Config, job: jobs.Job, run_id: str) -> list[str]:
    return [
        "intake", "land", staged(cfg),
        "--manifest", job.payload[go.ORIGIN_KEY]["manifest"],
        "--pass", default_name(run_id),
    ]


def test_a_go_stopped_at_the_ceiling_names_its_own_go_to_continue_not_the_job(
    installed, monkeypatch, script, tail
):
    run_id, envelope = stopped_at_the_ceiling(monkeypatch, script)

    # The test driver's own global option is kept, as the dispatcher keeps it.
    command = f"crate --output json --run {run_id} --calls 1000 label sync --go"
    cause = envelope["cause"]
    assert cause["detail"]["continue"] == command
    assert cause["remediation"]["steps"][0] == f"continue with a higher ceiling for one run: {command}"
    (job,) = our_jobs()
    assert job.state is jobs.JobState.BLOCKED and cause["detail"]["job"] == job.job_id
    assert "job resume" not in " ".join(cause["remediation"]["steps"])
    assert tail.calls == []


def test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run(
    installed, monkeypatch, script, tail
):
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    script.fetched.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r1-2", "t-r1-3"]
    assert [one.job_id for one in our_jobs()] == [job.job_id]
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert check(envelope, "continued")["status"] == "ok"
    assert "3 of 3 track(s) downloaded" in check(envelope, "continued")["detail"]
    assert tail.calls[-1] == landing_argv(installed, job, run_id)


def test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision(
    installed, monkeypatch, script, tail
):
    """The sequence the attended pass of 2026-11-10 measured: refused stale before U239."""
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    finished_by_hand(job.job_id)
    script.fetched.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == [], "a finished download was fetched again"
    assert tail.calls[-1] == landing_argv(installed, job, run_id)
    assert envelope["data"]["summary"]["go"]["continued"] == job.job_id
    pending = envelope["pending_human_action"]
    assert pending["verify_verb"] == tail_chain.LAND_VERB


def test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing(
    installed, monkeypatch, script, tail
):
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    with jobs.open_store() as store:
        jobs.cancel(store, job.job_id)
    script.fetched.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.DECISION_STALE), envelope
    assert fetched(script) == [] and tail.calls == []
    assert item_states(job.job_id)["t-r1-3"] is not jobs.ItemState.DONE


def test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it(
    installed, monkeypatch, script, tail
):
    register("Alpha Works")
    register("Beta Works")
    bind(monkeypatch, {"alpha-works": [("a1", "2026", 3)], "beta-works": [("b1", "2026", 1)]})
    next_question()
    answer("alpha-works", "all")
    land_every(script, ("a1", 3), ("b1", 1))
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script, label="alpha-works")
    (job,) = our_jobs()
    next_question()
    answer("beta-works", "all")
    finished_by_hand(job.job_id)

    code, envelope = gone(run_id)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert "t-b1-1" not in fetched(script)
    assert [one.job_id for one in our_jobs()] == [job.job_id]
    assert tail.calls[-1] == landing_argv(installed, job, run_id)
    assert check(envelope, "waiting")["detail"].startswith("1 answer(s) wait for the next go")
    landed_by_hand(installed, run_id)

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script)[-1] == "t-b1-1" and len(our_jobs()) == 2


def test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands(
    installed, monkeypatch, script, tail
):
    register("Alpha Works")
    register("Beta Works")
    bind(monkeypatch, {"alpha-works": [("a1", "2026", 3)], "beta-works": [("b1", "2026", 1)]})
    next_question()
    answer("alpha-works", "all")
    land_every(script, ("a1", 3), ("b1", 1))
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script, label="alpha-works")
    (first,) = our_jobs()
    finished_by_hand(first.job_id)
    next_question()
    answer("beta-works", "all")
    _later, code, _envelope = before_r1467(monkeypatch, approved_go)
    assert code == int(ExitCode.PENDING_HUMAN)
    (second,) = [one for one in our_jobs() if one.job_id != first.job_id]
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == [], "the tail ran over two batches"
    cause = envelope["cause"]
    assert cause["reason"] == "refused-by-policy"
    assert cause["detail"]["beside"] == [second.job_id]
    folder = staged(installed)
    manifest = first.payload[go.ORIGIN_KEY]["manifest"]
    typed = cause["remediation"]["steps"][-1]
    assert typed.startswith("the tail by hand, in this order: crate tag folder ")
    assert f"crate tag guess {folder}" in typed
    assert typed.endswith(
        f"crate intake land {folder} --manifest {manifest} --pass {default_name(run_id)}"
    )


def test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again(
    installed, monkeypatch, script, tail
):
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    code, _landed = gone(run_id)
    assert code == int(ExitCode.PENDING_HUMAN)
    tail.calls.clear()
    script.fetched.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert tail.calls == [] and fetched(script) == []
    assert "under run land-run already" in check(envelope, "landing")["detail"]
    assert "crate run show land-run" in check(envelope, "landing")["detail"]


def test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again(
    installed, monkeypatch, script, tail
):
    """Before U239 the same run asked again refused stale over an empty plan."""
    one_release_answered(monkeypatch, script)
    run_id, code, _envelope = approved_go()
    assert code == int(ExitCode.PENDING_HUMAN)
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.OK), envelope
    assert tail.calls == []
    assert "land-run" in check(envelope, "landing")["detail"]


def test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park(
    installed, monkeypatch, script
):
    one_release_answered(monkeypatch, script, tracks=3)
    script.landings["t-r1-2"] = Landing(fetch_raises=cooldown())

    run_id, code, envelope = approved_go()

    assert envelope["outcome"] == "blocked", envelope
    assert envelope["cause"]["remediation"]["steps"][-1].endswith(
        f"crate --run {run_id} label sync --go"
    )


# ── U239's review, round one: each guard the suite left unpinned ────────────


def two_labels(monkeypatch, script, tracks: int = 3) -> None:
    """Alpha and Beta, ``tracks`` tracks each, only Alpha answered so far."""
    register("Alpha Works")
    register("Beta Works")
    bind(
        monkeypatch,
        {"alpha-works": [("a1", "2026", tracks)], "beta-works": [("b1", "2026", tracks)]},
    )
    next_question()
    answer("alpha-works", "all")
    land_every(script, ("a1", tracks), ("b1", tracks))


def other_than(job: jobs.Job) -> jobs.Job:
    (found,) = [one for one in our_jobs() if one.job_id != job.job_id]
    return found


def test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one(
    installed, monkeypatch, script, tail
):
    """The review's BLOCKING finding: a run that resumed another go's download to
    its landing, then queued and stopped its own, was told its own had landed."""
    two_labels(monkeypatch, script)
    stopped_at_the_ceiling(monkeypatch, script, label="alpha-works")
    (first,) = our_jobs()
    resuming = asked()["run_id"]
    decided(resuming, "apply")
    code, _envelope = gone(resuming)
    assert code == int(ExitCode.PENDING_HUMAN)
    landed_by_hand(installed, first.payload[go.ORIGIN_KEY]["run"])
    next_question()
    answer("beta-works", "all")
    script.landings["t-b1-2"] = Landing(fetch_raises=ceiling(), fetch_raises_times=1)
    code, _envelope = gone(resuming)
    assert code == int(ExitCode.DECISION_STALE)
    decided(resuming, "apply")
    code, envelope = gone(resuming)
    assert envelope["cause"]["reason"] == provider_gate.CEILING
    second = other_than(first)
    script.fetched.clear()
    tail.calls.clear()

    code, envelope = gone(resuming)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-b1-2", "t-b1-3"]
    assert tail.calls[-1] == landing_argv(installed, second, resuming)


def test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run(
    installed, monkeypatch, script, tail
):
    first_run, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    resuming = asked()["run_id"]
    decided(resuming, "apply")
    code, _envelope = gone(resuming)
    assert code == int(ExitCode.PENDING_HUMAN)
    assert gates.load(first_run).related_runs == {go.landing_role(job.job_id): "land-run"}
    tail.calls.clear()

    code, envelope = gone(first_run)

    assert code == int(ExitCode.OK), envelope
    assert tail.calls == [], "the tail ran a second time for a download already at its landing"
    assert "land-run" in check(envelope, "landing")["detail"]


def test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue(
    installed, monkeypatch, script, tail
):
    first_run, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    script.landings["t-r1-3"] = Landing(fetch_raises=ceiling(), fetch_raises_times=1)
    resuming = asked()["run_id"]
    decided(resuming, "apply")

    code, envelope = gone(resuming)

    command = envelope["cause"]["detail"]["continue"]
    assert command == f"crate --output json --run {first_run} --calls 1000 label sync --go"
    assert resuming not in command


def test_an_abort_recorded_after_the_stop_is_not_taken_on(installed, monkeypatch, script, tail):
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    code, envelope = drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    assert code == int(ExitCode.OK), envelope
    script.fetched.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.DECISION_STALE), envelope
    assert fetched(script) == [] and tail.calls == []
    assert item_states(job.job_id)["t-r1-3"] is jobs.ItemState.PENDING


def test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run(
    installed, monkeypatch, script, tail
):
    one_release_answered(monkeypatch, script, tracks=3)
    script.landings["t-r1-2"] = Landing(
        fetch_raises=refuse("unavailable-transient", "later", retryable=True),
        fetch_raises_times=1,
    )
    run_id, code, envelope = approved_go()
    assert code != int(ExitCode.PENDING_HUMAN), envelope
    (job,) = our_jobs()
    assert job.state is jobs.JobState.FAILED
    assert envelope["cause"]["remediation"]["steps"][-1].endswith(
        f"crate --run {run_id} label sync --go"
    )

    code, envelope = gone(run_id)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert tail.calls[-1] == landing_argv(installed, job, run_id)


def test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail(
    installed, monkeypatch, script, tail
):
    two_labels(monkeypatch, script, tracks=1)
    script.landings["t-a1-1"] = Landing(fetch_raises=ceiling(), fetch_raises_times=1)
    run_id, code, _envelope = approved_go()
    (first,) = our_jobs()
    finished_by_hand(first.job_id)
    next_question()
    answer("beta-works", "all")
    script.landings["t-b1-1"] = Landing(fetch_raises=cooldown())
    before_r1467(monkeypatch, approved_go)
    second = other_than(first)
    assert second.state is jobs.JobState.BLOCKED
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["detail"]["beside"] == [second.job_id]
    assert tail.calls == []


def test_an_earlier_gos_landed_download_does_not_refuse_a_later_runs_tail(
    installed, monkeypatch, script, tail
):
    two_labels(monkeypatch, script)
    earlier, code, _envelope = approved_go()
    assert code == int(ExitCode.PENDING_HUMAN)
    landed_by_hand(installed, earlier)
    next_question()
    answer("beta-works", "all")
    script.landings["t-b1-2"] = Landing(fetch_raises=ceiling(), fetch_raises_times=1)
    later, _code, _envelope = approved_go()
    (job,) = [one for one in our_jobs() if one.payload[go.ORIGIN_KEY]["run"] == later]
    tail.calls.clear()

    code, envelope = gone(later)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert tail.calls[-1] == landing_argv(installed, job, later)


def test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail(
    installed, monkeypatch, script, tail
):
    one_release_answered(monkeypatch, script)
    real = tail._job
    gated = {"on": True}

    def restamp_gated(step, verb, argv):
        if gated["on"] and step == tail_chain.RESTAMP and "--job" not in argv:
            return _refused(
                Cause(
                    reason="decision-required",
                    message="analyze.restamp.confirm needs a recorded decision",
                    remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
                    retryable=True,
                    origin=("test",),
                    detail={"gate": "analyze.restamp.confirm", "options": ["apply"],
                            "run_id": "restamp-run"},
                ),
                outcome="blocked",
            )
        return real(step, verb, argv)

    monkeypatch.setattr(tail, "_job", restamp_gated)
    run_id, code, _envelope = approved_go()
    assert code == int(ExitCode.PENDING_HUMAN)
    assert gates.load(run_id).related_runs == {}
    gated["on"] = False
    (job,) = our_jobs()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert tail.calls[-1] == landing_argv(installed, job, run_id)
    assert gates.load(run_id).related_runs == {go.landing_role(job.job_id): "land-run"}


def test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op(
    installed, monkeypatch, script, tail
):
    register("Alpha Works")
    register("Beta Works")
    bind(monkeypatch, {"alpha-works": [("a1", "2026", 2)]})
    land_every(script, ("a1", 2), ("b1", 1))
    scripted_terminal(monkeypatch, "all")
    _code, envelope = drive(["label", "sync"])
    run_id = envelope["run_id"]
    code, envelope = drive(
        ["run", "decide", "--actor", "a-person", "--continue", run_id, GATE, "apply"]
    )
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    bind(monkeypatch, {"alpha-works": [("a1", "2026", 2)], "beta-works": [("b1", "2026", 1)]})
    scripted_terminal(monkeypatch, "all")

    code, envelope = drive(["--run", run_id, "label", "sync"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert "land-run" in check(envelope, "landing")["detail"]


def test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it(
    installed, monkeypatch, script, tail
):
    first_run, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    saved = gates.save

    def refusing(state):
        if state.run_id == first_run:
            raise PermissionError("the run record is not writable")
        return saved(state)

    monkeypatch.setattr(gates, "save", refusing)
    resuming = asked()["run_id"]
    decided(resuming, "apply")

    code, envelope = gone(resuming)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert tail.calls[-1] == landing_argv(installed, job, first_run)
    (warned,) = [one for one in envelope["warnings"] if one["code"] == "label-sync-landing-unrecorded"]
    assert first_run in warned["message"] and job.job_id in warned["message"]
    assert "PermissionError" in warned["message"]
    assert gates.load(first_run).related_runs == {}


def test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail(
    installed, monkeypatch, script, tail
):
    """M11 of U239's table: the run's own download read again lands nothing."""
    one_release_answered(monkeypatch, script)
    script.landings["t-r1-1"] = Landing(kind="lossy")
    script.landings["t-r1-2"] = Landing(kind="lossy")
    run_id, code, _envelope = approved_go()
    assert code == int(ExitCode.OK)

    code, envelope = gone(run_id)

    assert code == int(ExitCode.OK), envelope
    assert tail.calls == [], "the tail ran over a download that landed nothing"
    continued = check(envelope, "continued")
    assert continued["status"] == "fail"
    assert "every track was refused for good, so no tail was run" in continued["detail"]
    go_report = envelope["data"]["summary"]["go"]
    assert go_report[go.LAND_KEY] is None and go_report["next"] == []


# ═══════════════════════════════════════════════════════════════════════════
# 7. R-1467: a go never lands, as its own batch, a download that is not its own
# ═══════════════════════════════════════════════════════════════════════════


def renamed_by_its_tail(cfg: config.Config) -> None:
    """Every track in the folder renamed, as the tail's ``name apply`` renames them.

    The stand in tail answers ``name apply`` with nothing renamed, so a download
    whose tail stopped at the landing's gate would still sit at its download
    names; the real one renames each file before that gate, which is the state
    a go must not read as gone.
    """
    folder = Path(staged(cfg))
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix == ".wav":
            path.rename(folder / f"Artist - {path.stem}.wav")


def moved_out(cfg: config.Config) -> None:
    """Every track in the folder moved into the library, as a landing moves them."""
    folder = Path(staged(cfg))
    target = Path(cfg.library.root) / "Music" / "landed"
    target.mkdir(parents=True, exist_ok=True)
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix == ".wav":
            path.rename(target / path.name)


def proven(cfg: config.Config, run_id: str, *, medium: str = "bridge") -> None:
    """The landing proof of a go's pass, on one medium.

    ``bridge`` writes the intake file the landing writes at the library root;
    ``native`` records the closed landing that committed the pass on a database
    native intake tree, as ``native.landings_of_pass`` reads it.
    """
    name = default_name(run_id)
    if medium == "bridge":
        (Path(cfg.library.root) / f"{name}{land_cli.INTAKE_SUFFIX}").write_text("<xml/>")
        return
    session.write_record(
        session.SessionRecord(
            session_id=f"landing-{name}",
            workflow=native.WORKFLOW,
            started="2026-11-11T12:00:00+00:00",
            state=session.SessionState.CLOSED,
            sources={"intake": str(session.SourceState.COMMITTED)},
            ended="2026-11-11T12:05:00+00:00",
            detail={native.PASS_KEY: name},
        ),
        cfg,
    )


def landed_by_hand(cfg: config.Config, run_id: str, *, medium: str = "bridge") -> None:
    """The landing a go's tail stopped at, applied: its tracks moved out, its proof kept."""
    moved_out(cfg)
    proven(cfg, run_id, medium=medium)


def before_r1467(monkeypatch, act):
    """``act`` run as a build before R-1467 ran it, reading nothing as waiting.

    The state a go of such a build left, a later go's download queued into the
    folder beside an earlier one no landing took, is what a run's own go still
    refuses its tail beside, and no go of this build queues it.
    """
    with monkeypatch.context() as earlier:
        earlier.setattr(go, "beside", lambda _cfg, _store, staging, *_a, **_k: go.Beside(staging))
        return act()


def stray(cfg: config.Config, name: str = "Someone - Kept By Hand.wav") -> Path:
    """A track in the folder that no download put there."""
    folder = Path(staged(cfg))
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_bytes(b"put here by hand")
    return path


def downloaded_by_hand(script: Script, tmp_path: Path, ref: str = "x1") -> str:
    """A plain ``acquire download`` into the same folder, driven to the end."""
    listed = tmp_path / f"by-hand-{ref}.json"
    listed.write_text(tidal_list([(ref, "Other Act", f"Elsewhere {ref}")]))
    script.landings[ref] = Landing()
    code, queued = drive(["acquire", "download", str(listed)])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]
    code, envelope = drive(["acquire", "download", "--job", job_id])
    assert code == int(ExitCode.OK), envelope
    return job_id


def landed_first(monkeypatch, script) -> str:
    """Alpha's go run to its landing's gate, Beta answered after it. Returns Alpha's run."""
    two_labels(monkeypatch, script, tracks=2)
    run_id, code, envelope = approved_go()
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    next_question()
    answer("beta-works", "all")
    return run_id


def refused_before_the_gate(envelope: dict) -> dict:
    cause = envelope["cause"]
    assert cause["reason"] == "refused-by-policy", cause
    assert "gate" not in (cause.get("detail") or {}), "the gate was asked over a folder it cannot land"
    return cause


def test_an_earlier_gos_download_finished_by_hand_refuses_a_fresh_go_before_it_queues(
    installed, monkeypatch, script, tail
):
    """The brief's first scenario: before R-1467 the fresh go queued, and its tail
    landed both downloads as one batch under its own manifest and pass."""
    two_labels(monkeypatch, script)
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script, label="alpha-works")
    (first,) = our_jobs()
    finished_by_hand(first.job_id)
    next_question()
    answer("beta-works", "all")
    script.fetched.clear()
    tail.calls.clear()

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert [one["job"] for one in cause["detail"]["waiting"]] == [first.job_id]
    assert cause["detail"]["waiting"][0]["run"] == run_id
    assert first.job_id in cause["message"]
    assert f"crate --run {run_id} label sync --go" in " ".join(cause["remediation"]["steps"])
    assert [one.job_id for one in our_jobs()] == [first.job_id], "a second download was queued"
    assert fetched(script) == [] and tail.calls == []


def test_an_earlier_go_whose_tail_renamed_its_tracks_at_the_landings_gate_still_refuses(
    installed, monkeypatch, script, tail
):
    """The usual state after a go: its tail stopped at the landing's gate, its
    tracks renamed by ``name apply`` and no landing applied yet."""
    run_id = landed_first(monkeypatch, script)
    renamed_by_its_tail(installed)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    (waiting,) = cause["detail"]["waiting"]
    assert waiting["run"] == run_id and waiting["tracks"] == 0
    assert len(our_jobs()) == 1


def test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly(
    installed, monkeypatch, script, tail
):
    """Row 9 of U239's review: the fresh go ended ``no_op`` naming nothing."""
    one_release_answered(monkeypatch, script)
    run_id, code, _envelope = approved_go()
    assert code == int(ExitCode.PENDING_HUMAN)
    renamed_by_its_tail(installed)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert [one["run"] for one in cause["detail"]["waiting"]] == [run_id]


@pytest.mark.parametrize("medium", ["bridge", "native"])
def test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download(
    installed, monkeypatch, script, tail, medium
):
    run_id = landed_first(monkeypatch, script)
    landed_by_hand(installed, run_id, medium=medium)

    new = asked()["run_id"]
    decided(new, "apply")
    code, envelope = gone(new)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert len(our_jobs()) == 2
    assert fetched(script)[-2:] == ["t-b1-1", "t-b1-2"]


@pytest.mark.parametrize("medium", ["bridge", "native"])
def test_a_track_no_download_names_refuses_the_fresh_go_and_only_an_unproven_go_is_named(
    installed, monkeypatch, script, tail, medium
):
    """A file no download names is beside the go whoever put it there; the
    landing proof says only which go's tail may have renamed it."""
    run_id = landed_first(monkeypatch, script)
    moved_out(installed)
    kept = stray(installed)
    code, envelope = drive(["label", "sync", "--go"])
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert [one["run"] for one in cause["detail"]["waiting"]] == [run_id]
    assert cause["detail"]["unnamed"] == [kept.name]

    proven(installed, run_id, medium=medium)

    code, envelope = drive(["label", "sync", "--go"])
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert cause["detail"]["waiting"] == [] and cause["detail"]["unnamed"] == [kept.name]
    assert kept.name in cause["message"]
    kept.unlink()

    assert asked()["cause"]["detail"]["gate"] == GATE


def test_a_retired_intake_file_proves_the_pass(installed, monkeypatch, script, tail):
    run_id = landed_first(monkeypatch, script)
    moved_out(installed)
    stray(installed)
    name = f"{default_name(run_id)}{land_cli.INTAKE_SUFFIX}{land_cli.RETIRED_SUFFIX}-2"
    (Path(installed.library.root) / name).write_text("<xml/>")

    code, envelope = drive(["label", "sync", "--go"])

    assert envelope["cause"]["detail"]["waiting"] == [], envelope


def test_a_landing_proof_of_another_pass_proves_nothing(installed, monkeypatch, script, tail):
    run_id = landed_first(monkeypatch, script)
    moved_out(installed)
    stray(installed)
    proven(installed, "another-run")
    (Path(installed.library.root) / f"{default_name(run_id)}_other.xml").write_text("<xml/>")
    (Path(installed.library.root) / f"{default_name(run_id)}{land_cli.INTAKE_SUFFIX}").mkdir()

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert [one["run"] for one in envelope["cause"]["detail"]["waiting"]] == [run_id]


def test_a_proven_pass_whose_tracks_are_still_at_their_download_names_is_still_waiting(
    installed, monkeypatch, script, tail
):
    """A pass landed part way, then finished: its proof is there, and so are its
    later tracks, at the names they were downloaded under."""
    run_id = landed_first(monkeypatch, script)
    proven(installed, run_id)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    (waiting,) = envelope["cause"]["detail"]["waiting"]
    assert waiting["run"] == run_id and waiting["tracks"] == 2


def test_an_unreadable_library_root_refuses_rather_than_read_the_pass_as_landed(
    installed, monkeypatch, script, tail
):
    run_id = landed_first(monkeypatch, script)
    landed_by_hand(installed, run_id)
    stray(installed)
    real = Path.iterdir
    root = Path(installed.library.root)

    def unreadable(self):
        if self == root:
            raise PermissionError(13, "Permission denied", str(self))
        return real(self)

    monkeypatch.setattr(Path, "iterdir", unreadable)

    code, envelope = drive(["label", "sync", "--go"])

    assert code != int(ExitCode.OK), envelope
    cause = envelope["cause"]
    assert cause["detail"].get("declared_reason", cause["reason"]) == "library-root-unreachable"
    assert "whether the pass" in cause["message"], cause
    assert "gate" not in (envelope["cause"].get("detail") or {})
    assert len(our_jobs()) == 1


def test_a_plain_download_into_the_folder_refuses_the_runs_own_tail(
    installed, monkeypatch, script, tail, tmp_path
):
    """The brief's third scenario: ``_beside`` saw later go jobs only."""
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    plain = downloaded_by_hand(script, tmp_path)
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == [], "the tail ran over a download no go queued"
    cause = envelope["cause"]
    assert cause["detail"]["beside"] == [plain]
    assert [one["job"] for one in cause["detail"]["waiting"]] == [plain]
    assert cause["detail"]["waiting"][0]["run"] is None
    assert cause["remediation"]["steps"][-1].startswith("the tail by hand, in this order: ")
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}


def test_a_plain_download_in_the_folder_refuses_a_fresh_go_before_the_gate(
    installed, monkeypatch, script, tail, tmp_path
):
    plain = downloaded_by_hand(script, tmp_path)
    one_release_answered(monkeypatch, script)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert cause["detail"]["waiting"] == [
        {"job": plain, "run": None, "verb": go.DOWNLOAD, "tracks": 1}
    ]
    assert cause["detail"]["unnamed"] == []
    assert "move" in " ".join(cause["remediation"]["steps"])


def test_a_plain_download_already_landed_refuses_nothing(
    installed, monkeypatch, script, tail, tmp_path
):
    downloaded_by_hand(script, tmp_path)
    moved_out(installed)
    one_release_answered(monkeypatch, script)

    run_id, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    (job,) = our_jobs()
    assert tail.calls[-1] == landing_argv(installed, job, run_id)


def test_an_earlier_download_the_fresh_go_resumes_is_its_own_and_a_plain_one_is_not(
    installed, monkeypatch, script, tail, tmp_path
):
    """A fresh go with an earlier go's job to resume lands that job's batch: a
    plain download beside it would land under that go's pass."""
    stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    plain = downloaded_by_hand(script, tmp_path)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert [one["job"] for one in cause["detail"]["waiting"]] == [plain]
    assert job.job_id not in [one["job"] for one in cause["detail"]["waiting"]]


def test_an_earlier_download_the_fresh_go_resumes_alone_is_asked_about(
    installed, monkeypatch, script, tail
):
    stopped_at_the_ceiling(monkeypatch, script)

    shown = asked()["cause"]["detail"]["shown"]

    assert shown["earlier_downloads_to_resume"] == 1


def test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail(
    installed, monkeypatch, script, tail, tmp_path
):
    """A plain download that finished while the go's own drove, after the gate."""
    one_release_answered(monkeypatch, script)
    real = go._drive
    beside: list[str] = []

    def and_another(ctx, store, job_id):
        driven = real(ctx, store, job_id)
        beside.append(downloaded_by_hand(script, tmp_path))
        return driven

    monkeypatch.setattr(go, "_drive", and_another)

    run_id, code, envelope = approved_go()

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == []
    assert envelope["cause"]["detail"]["beside"] == beside
    (job,) = our_jobs()
    assert envelope["cause"]["remediation"]["steps"][-1].endswith(
        f"--manifest {job.payload[go.ORIGIN_KEY]['manifest']} --pass {default_name(run_id)}"
    )


def test_a_staging_folder_not_there_holds_nothing_waiting(installed, monkeypatch, script, tail):
    one_release_answered(monkeypatch, script)
    assert not Path(staged(installed)).exists() or not any(Path(staged(installed)).iterdir())

    assert asked()["cause"]["detail"]["gate"] == GATE


def test_a_staging_folder_that_cannot_be_listed_refuses_rather_than_hold_nothing(
    installed, monkeypatch, script, tail
):
    one_release_answered(monkeypatch, script)
    Path(staged(installed)).mkdir(parents=True, exist_ok=True)

    def unlistable(folder):
        raise PermissionError(13, "Permission denied", str(folder))

    monkeypatch.setattr(go, "folder_listing", unlistable)

    code, envelope = drive(["label", "sync", "--go"])

    assert code != int(ExitCode.OK), envelope
    cause = envelope["cause"]
    assert cause["detail"].get("declared_reason", cause["reason"]) == "intake-list-unusable"
    assert "could not be listed" in cause["message"]
    assert "gate" not in cause["detail"] and our_jobs() == []


# ── Review round one of R-1467: tracks a tail renamed, and other handlers ──


def landing_refused(tail, cfg: config.Config | None = None) -> None:
    """The landing refuses, as a bridge tree the export cannot be read for does.

    With ``cfg``, the folder's tracks are renamed first, as the real ``name
    apply`` renames them before the landing; the stand in renames nothing.
    """

    def refused(_argv):
        if cfg is not None:
            renamed_by_its_tail(cfg)
        return _refused(
            Cause(
                reason="library-export-unusable",
                message="the rekordbox export could not be read",
                remediation=Remediation(remedy=Remedy.PREPARE_LIBRARY_IN_REKORDBOX),
                origin=("test",),
            )
        )

    tail.landing = refused


def test_a_plain_download_a_tail_renamed_refuses_a_fresh_go_before_its_gate(
    installed, monkeypatch, script, tail, tmp_path
):
    """Round one's B1: a sync pass's tracks, renamed at its landing's gate, were
    read as landed and planned into the label go's landing."""
    downloaded_by_hand(script, tmp_path, "x1")
    downloaded_by_hand(script, tmp_path, "x2")
    renamed_by_its_tail(installed)
    one_release_answered(monkeypatch, script)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert cause["detail"]["unnamed"] == ["Artist - x1.wav", "Artist - x2.wav"]
    assert cause["detail"]["waiting"] == []
    assert our_jobs() == []


def test_a_plain_download_a_tail_renamed_refuses_the_runs_own_tail(
    installed, monkeypatch, script, tail, tmp_path
):
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    downloaded_by_hand(script, tmp_path)
    folder = Path(staged(installed))
    (folder / "x1.wav").rename(folder / "Other Act - Elsewhere x1.wav")
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == []
    assert envelope["cause"]["detail"]["unnamed"] == ["Other Act - Elsewhere x1.wav"]


def test_a_download_of_another_verb_with_its_track_in_the_folder_refuses_the_go(
    installed, monkeypatch, script, tail
):
    """Round one's B2: a fallback fetch commits into the same folder under its
    own handler, and only ``acquire.download`` jobs were read."""
    folder = Path(staged(installed))
    folder.mkdir(parents=True, exist_ok=True)
    fetched_file = folder / "Aurora Bloom - Sun Path [LOSSY].mp3"
    fetched_file.write_bytes(b"a second source")
    key = registry.entry("acquire.fallback-fetch").handler_key
    with jobs.open_store() as store:
        fetch = jobs.enqueue(store, handler_key=key, payload={}, cfg=installed, item_ids=("f1",))
        jobs.complete_item(store, fetch.job_id, "f1", artifact=fetched_file)
    one_release_answered(monkeypatch, script)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert cause["detail"]["waiting"] == [
        {"job": fetch.job_id, "run": None, "verb": key, "tracks": 1}
    ]
    assert f"job {fetch.job_id} of {key}" in cause["message"]


def test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run(
    installed, monkeypatch, script, tail
):
    """Round one's B3: a run's own tracks, renamed by its own tail, were read
    as another go's and its own ``--go`` was refused."""
    one_release_answered(monkeypatch, script)
    landing_refused(tail, installed)
    run_id, code, envelope = approved_go()
    assert code != int(ExitCode.PENDING_HUMAN), envelope
    (job,) = our_jobs()
    tail.landing = Tail().landing
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert tail.calls[-1] == landing_argv(installed, job, run_id)


def test_a_go_whose_tail_ran_still_refuses_a_file_more_than_its_own_renamed(
    installed, monkeypatch, script, tail
):
    one_release_answered(monkeypatch, script)
    landing_refused(tail, installed)
    run_id, _code, _envelope = approved_go()
    kept = stray(installed)
    tail.landing = Tail().landing
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == []
    assert kept.name in envelope["cause"]["detail"]["unnamed"]


def test_a_go_whose_tracks_another_tail_renamed_does_not_read_them_as_its_own(
    installed, monkeypatch, script, tail
):
    """No tail of this run ran, so files no download names are not its tracks."""
    run_id, _envelope = stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    finished_by_hand(job.job_id)
    renamed_by_its_tail(installed)
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == []
    assert len(envelope["cause"]["detail"]["unnamed"]) == 3


def test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail(
    installed, monkeypatch, script, tail, tmp_path
):
    """Round one's R2: the beside check after a resume's drive killed no test."""
    stopped_at_the_ceiling(monkeypatch, script)
    (job,) = our_jobs()
    real = go._drive
    beside: list[str] = []

    def and_another(ctx, store, job_id):
        driven = real(ctx, store, job_id)
        beside.append(downloaded_by_hand(script, tmp_path))
        return driven

    monkeypatch.setattr(go, "_drive", and_another)
    resuming = asked()["run_id"]
    decided(resuming, "apply")
    tail.calls.clear()

    code, envelope = gone(resuming)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == []
    assert envelope["cause"]["detail"]["beside"] == beside
    assert envelope["cause"]["detail"]["job"] == job.job_id


def test_the_walk_refused_beside_a_download_keeps_what_it_answered(
    installed, monkeypatch, script, tail, tmp_path
):
    """Round one's R5: the walk's answers are saved and named in the refusal."""
    downloaded_by_hand(script, tmp_path)
    register()
    bind(monkeypatch, {"tide-works": [("r1", "2026", 1)]})
    scripted_terminal(monkeypatch, "all")

    code, envelope = drive(["label", "sync"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = envelope["cause"]
    assert cause["detail"]["answered_this_run"][0].startswith("Tide Works: all")
    assert len(record(installed)["answers"]) == 1
    assert cause["remediation"]["steps"][-1].endswith("the answers given are saved")
    assert "it did not ask its gate or queue a download" in cause["message"]


def test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good(
    installed, monkeypatch, script, tail, tmp_path
):
    """Round one's R4: the go's report, which names them, is not returned."""
    one_release_answered(monkeypatch, script)
    script.landings["t-r1-2"] = Landing(kind="lossy")
    real = go._drive

    def and_another(ctx, store, job_id):
        driven = real(ctx, store, job_id)
        downloaded_by_hand(script, tmp_path)
        return driven

    monkeypatch.setattr(go, "_drive", and_another)

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert [row["item_id"] for row in envelope["cause"]["detail"]["refused"]] == ["t-r1-2"]


# ── Review round two of R-1467: what the tail left, kept by identity ──


def stopped_short_of_its_landing(monkeypatch, script, tail, installed) -> tuple[str, jobs.Job]:
    """A go whose tail renamed its tracks and stopped before the landing's gate."""
    one_release_answered(monkeypatch, script)
    landing_refused(tail, installed)
    run_id, code, envelope = approved_go()
    assert code != int(ExitCode.PENDING_HUMAN), envelope
    (job,) = our_jobs()
    tail.landing = Tail().landing
    tail.calls.clear()
    return run_id, job


def test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own(
    installed, monkeypatch, script, tail, tmp_path
):
    """Round two's BLOCKING finding: once its tracks left the folder, a go whose
    tail had started read as many foreign files as its own and landed them."""
    run_id, _job = stopped_short_of_its_landing(monkeypatch, script, tail, installed)
    moved_out(installed)
    downloaded_by_hand(script, tmp_path, "x1")
    downloaded_by_hand(script, tmp_path, "x2")
    renamed_by_its_tail(installed)

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == [], "the go landed another download's tracks as its own"
    assert envelope["cause"]["detail"]["unnamed"] == ["Artist - x1.wav", "Artist - x2.wav"]


def test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos(
    installed, monkeypatch, script, tail
):
    run_id, _job = stopped_short_of_its_landing(monkeypatch, script, tail, installed)
    folder = Path(staged(installed))
    (taken,) = [path for path in folder.iterdir() if path.name == "Artist - t-r1-1.wav"]
    taken.write_bytes(b"another recording under the same name")

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["detail"]["unnamed"] == ["Artist - t-r1-1.wav"]


def test_a_go_whose_pass_landed_reads_nothing_by_its_tails_record(
    installed, monkeypatch, script, tail
):
    run_id, _job = stopped_short_of_its_landing(monkeypatch, script, tail, installed)
    proven(installed, run_id)

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == []
    assert len(envelope["cause"]["detail"]["unnamed"]) == 2


def test_a_tails_record_that_cannot_be_read_reads_nothing_as_the_gos_own(
    installed, monkeypatch, script, tail
):
    run_id, job = stopped_short_of_its_landing(monkeypatch, script, tail, installed)
    (jobs.store_dir(installed) / go.TAILS_DIRNAME / f"{job.job_id}.json").write_text("{")

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == []


def test_the_tail_keeps_what_it_left_whichever_way_it_ends(installed, monkeypatch, script, tail):
    one_release_answered(monkeypatch, script)
    landing_refused(tail)
    _run, code, envelope = approved_go()
    assert code != int(ExitCode.PENDING_HUMAN), envelope
    (job,) = our_jobs()

    kept = go.kept_tail(installed, job.job_id)

    assert sorted(name for name, _size, _mtime in kept) == ["t-r1-1.wav", "t-r1-2.wav"]
    folder = Path(staged(installed))
    assert kept == {
        (path.name, path.stat().st_size, path.stat().st_mtime_ns)
        for path in folder.iterdir()
        if path.is_file()
    }


def test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos(
    installed, monkeypatch, script, tail, tmp_path
):
    """Round two's R5: a download committed while the tail ran is that download's."""
    one_release_answered(monkeypatch, script)
    plain: list[str] = []

    def downloaded_then_refused(_argv):
        plain.append(downloaded_by_hand(script, tmp_path))
        return _refused(
            Cause(
                reason="library-export-unusable",
                message="the rekordbox export could not be read",
                remediation=Remediation(remedy=Remedy.PREPARE_LIBRARY_IN_REKORDBOX),
                origin=("test",),
            )
        )

    tail.landing = downloaded_then_refused
    run_id, code, envelope = approved_go()
    assert code != int(ExitCode.PENDING_HUMAN), envelope
    (job,) = our_jobs()
    assert "x1.wav" not in {name for name, _s, _m in go.kept_tail(installed, job.job_id)}
    tail.landing = Tail().landing
    tail.calls.clear()

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert tail.calls == []
    assert envelope["cause"]["detail"]["beside"] == plain


def test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good(
    installed, monkeypatch, script, tail, tmp_path
):
    """Round two's zero row: the refused tracks were carried on this tail untested."""
    one_release_answered(monkeypatch, script, tracks=3)
    script.landings["t-r1-1"] = Landing(kind="lossy")
    script.landings["t-r1-2"] = Landing(fetch_raises=ceiling(), fetch_raises_times=1)
    run_id, code, envelope = approved_go()
    assert envelope["cause"]["reason"] == provider_gate.CEILING, envelope
    downloaded_by_hand(script, tmp_path)

    code, envelope = gone(run_id)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert [row["item_id"] for row in envelope["cause"]["detail"]["refused"]] == ["t-r1-1"]


def test_a_go_with_tracks_in_the_folder_is_named_once_beside_files_no_download_names(
    installed, monkeypatch, script, tail
):
    """Mutation row M13: a go already named by its tracks is not named again
    as one whose tail may have renamed the files no download names."""
    run_id = landed_first(monkeypatch, script)
    stray(installed)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    (waiting,) = envelope["cause"]["detail"]["waiting"]
    assert (waiting["run"], waiting["tracks"]) == (run_id, 2)


def test_a_go_whose_tracks_were_recorded_in_another_folder_is_not_named_for_this_one(
    installed, monkeypatch, script, tail, tmp_path
):
    """Mutation row M08: a download into another staging folder, say before the
    configured one moved, has nothing in this one to be put down to."""
    elsewhere = tmp_path / "old-staging"
    elsewhere.mkdir()
    (elsewhere / "t-old-1.wav").write_bytes(b"downloaded elsewhere")
    with jobs.open_store() as store:
        old = jobs.enqueue(
            store,
            handler_key=go.DOWNLOAD,
            payload={go.ORIGIN_KEY: {"run": "an-old-run", "manifest": "m"}, go.RUN_KEY: "an-old-run"},
            cfg=installed,
            item_ids=("t-old-1",),
        )
        jobs.complete_item(store, old.job_id, "t-old-1", artifact=elsewhere / "t-old-1.wav")
    one_release_answered(monkeypatch, script)
    kept = stray(installed)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = refused_before_the_gate(envelope)
    assert cause["detail"]["waiting"] == [] and cause["detail"]["unnamed"] == [kept.name]
