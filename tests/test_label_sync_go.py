"""U108: the guided label sync's go, one summary, one gate, one unattended download.

Every scenario the brief names is driven through the real dispatcher: answers
saved through U107's structured path, the gate refused and then decided by a
separate recorded act as R34 requires, and the download run by
``acquire download``'s own worker against the fake adapter, with the provider's
catalogue faked as U107's suite fakes it.

NOTHING HERE REACHES A NETWORK. The root fixtures fail any test that does.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit import acquire
from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import listdoc, match_cli
from cratekit.core import config, jobs, review
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.jobs import Parked
from cratekit.intake.land_cli import default_name
from cratekit.label import approved_cli, go, sync_cli
from tests.acquire_fakes import FAKE_ADAPTER, FAKE_DECLARATION, FakeAdapter, Landing, Script
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_label_sync import Track, answer, bind, next_question, offered, record, register

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

    assert code == int(ExitCode.OK), done
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

    assert code == int(ExitCode.OK), envelope
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

    assert code == int(ExitCode.OK), envelope
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

    assert code == int(ExitCode.OK), envelope
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

    assert code == int(ExitCode.OK), envelope
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
        patched.setattr(sync_cli, "settle_answers", killed)
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

    assert code == int(ExitCode.OK), envelope
    assert sorted(fetched(script)) == ["t-r1-1", "t-r1-2"]
    assert [one.job_id for one in our_jobs()] == [job.job_id]
    assert "2 track(s) an earlier go already holds" in check(envelope, "held-by-a-go")["detail"]
    assert all(one[sync_cli.SETTLED] for one in record(installed)["answers"])


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

    assert code == int(ExitCode.OK), envelope
    assert fetched(script) == ["t-r2-1"]
    assert check(envelope, "carried")["status"] == "fail"
    assert all(sync_cli.SETTLED not in one for one in record(installed)["answers"])

    monkeypatch.setattr(fake, "release_tracks", reader)
    script.fetched.clear()
    _run, code, envelope = approved_go()

    assert code == int(ExitCode.OK), envelope
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

    assert code == int(ExitCode.OK), envelope
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
        f"--name {default_name(run_id)}"
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

    assert code == int(ExitCode.OK), done
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
