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
from cratekit.cli import registry
from cratekit.cli import tail as tail_chain
from cratekit.core import config, jobs, review
from cratekit.core.cause import Cause, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.jobs import Parked
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

    _run, code, envelope = approved_go()

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert fetched(script) == ["t-r2-1"]
    assert check(envelope, "carried")["status"] == "fail"
    assert all(sync_cli.SETTLED not in one for one in record(installed)["answers"])

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
    approved_go()

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

    approved_go()

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
    (folder / "old.wav").write_bytes(b"")
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


def already_staged(cfg: config.Config, *track_ids: str) -> None:
    """A file at each track's staging name, so its download is refused ``output-exists``."""
    folder = Path(staged(cfg))
    folder.mkdir(parents=True, exist_ok=True)
    for track_id in track_ids:
        (folder / f"{track_id}.wav").write_bytes(b"kept on purpose")


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
    already_staged(installed, "t-r1-2")

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
    already_staged(installed, "t-r1-1")

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
    already_staged(installed, "t-r1-2")

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
    already_staged(installed, "t-r1-1")

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
