"""``crate sync land`` takes a sync pass to its landing gate in one verb (U152).

It runs the verbs in order, drives each job to a settled state, skips a
download refused for good, stops on anything else and ends at the landing's
gate. All is real but the tail and the landing, which stand in through
``cratekit.cli.tail.dispatch`` and still queue and drive real jobs.
"""

from __future__ import annotations

import json
import shlex
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pytest

from cratekit import acquire
from cratekit.acquire import cli as acquire_cli
from cratekit.cli import gates, registry, sync_land
from cratekit.cli import tail as tail_chain
from cratekit.core import config, jobs, rb_writer
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from tests._sync_builders import exited, failed
from tests.acquire_fakes import FAKE_ADAPTER, FAKE_DECLARATION, FakeAdapter, Landing, Script
from tests.cli_drive import drive
from tests.intake.test_workers import owned
from tests.test_config import valid_data
from tests.test_sync_all import (
    ShortHearts,
    _hearts,
    _playlist,
    _tracks,
    _warmup_and_peak,
    bind_hearts,
    bind_playlists,
)

ENTRY = registry.entry("sync.land")


# The machine, the account and the stand ins


def _machine(tmp_path, monkeypatch, profile: str) -> tuple[config.Config, Script]:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    acquisition = {"adapter": FAKE_ADAPTER, "pacing_delay_s": 0.0}
    built = config.from_dict(valid_data(root, profile={"name": profile}, acquisition=acquisition))
    config.save(built)
    config.reset_cache()
    script = Script()
    monkeypatch.setitem(acquire.ADAPTERS, FAKE_ADAPTER, FAKE_DECLARATION)
    monkeypatch.setattr(FakeAdapter, "script", script)
    monkeypatch.setattr(acquire_cli, "_SLEEP", lambda _seconds: None)
    return built, script


@pytest.fixture(autouse=True)
def vocal_model(monkeypatch):
    """A stand in vocal model able to score, so the pass's preflight goes on (U181)."""
    from cratekit.analysis import vocals

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", lambda: object())
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)


@pytest.fixture
def machine(tmp_path, monkeypatch):
    """The slim profile, which composes the account playlists alone."""
    return _machine(tmp_path, monkeypatch, "slim")


def _account(monkeypatch, script: Script, *ids: str, lossy: tuple[str, ...] = ()) -> None:
    """One new account playlist holding ``ids``, each downloadable, ``lossy`` landing MP3."""
    for track_id in ids:
        script.landings[track_id] = Landing(kind="lossy" if track_id in lossy else "lossless")
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks(*ids)))


def _ready(machine, monkeypatch, *ids: str, lossy: tuple[str, ...] = ()):
    """``machine`` with one new account playlist holding ``ids``, as ``_account`` binds it."""
    cfg, script = machine
    _account(monkeypatch, script, *ids, lossy=lossy)
    return cfg, script


def _enqueue(cfg: config.Config, verb: str, payload: dict, *item_ids: str, **kwargs) -> jobs.Job:
    """One job queued under ``verb``'s handler key, as that verb queues it."""
    key = registry.entry(verb).handler_key
    with jobs.open_store() as store:
        return jobs.enqueue(
            store, handler_key=key, payload=payload, cfg=cfg, item_ids=item_ids, **kwargs
        )


def _state(job_id: str) -> jobs.JobState:
    with jobs.open_store() as store:
        return jobs.get(store, job_id).state


def _cancel(job_id: str) -> None:
    with jobs.open_store() as store:
        jobs.cancel(store, job_id)


def _ok(data: dict[str, Any], outcome: str = "ok") -> tuple[int, dict[str, Any]]:
    return int(ExitCode.OK), {"outcome": outcome, "data": data, "warnings": []}


def _refused(cause: Cause, outcome: str = "failed") -> tuple[int, dict[str, Any]]:
    return int(cause.code), {"outcome": outcome, "cause": cause.to_json(), "warnings": []}


def _gate(run_id: str, gate: str = sync_land.LAND_GATE, **shown) -> Cause:
    """A step's gate refusal; ``shown`` adds what its screen shows."""
    return Cause(
        reason="decision-required",
        message=f"{gate} needs a recorded decision",
        remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
        retryable=True,
        origin=("test",),
        detail={"gate": gate, "options": ["apply", "abort"], "run_id": run_id, **shown},
    )


def _broken(_job, item) -> None:
    """Analysis work whose extra is missing, refusing each item."""
    raise refuse(
        "module-extras-missing",
        f"the analysis extra is not importable for {item.item_id}",
        scope=Scope.ITEM,
        origin=("test",),
    )


def _step_answers(monkeypatch, tail: "Tail", step: str, answer: tuple, *, driven: bool = False):
    """The tail's ``step`` answers ``answer`` at its queue command, or at its job command when
    ``driven``; returns the job method it stood in for."""
    real = tail._job

    def answering(step_: str, verb: str, argv: list[str]) -> tuple[int, dict[str, Any]]:
        if step_ == step and ("--job" in argv) == driven:
            return answer
        return real(step_, verb, argv)

    monkeypatch.setattr(tail, "_job", answering)
    return real


def _backup_missing(_argv) -> tuple[int, dict[str, Any]]:
    """A landing that refuses for want of a backup acknowledgment."""
    return _refused(
        refuse(
            "backup-acknowledgment-missing",
            "no backup acknowledgment is recorded",
            remedy=Remedy.ACKNOWLEDGE_BACKUP,
            origin=("test",),
        ).cause
    )


def _failed_intake(job_id: str, message: str, remedy: Remedy, retryable: bool = False) -> None:
    """The intake job ended failed on an ``adapter-broken`` cause."""
    cause = Cause(
        reason="adapter-broken",
        message=message,
        remediation=Remediation(remedy=remedy),
        retryable=retryable,
        origin=("test",),
    )
    with jobs.open_store() as store:
        jobs.transition(store, job_id, jobs.JobState.FAILED, cause=cause)


class Tail:
    """The tail and the landing, standing in: each queues and drives a real job, item per file.

    ``work`` decides each item; the landing answers with ``landing``, its gate by default.
    """

    def __init__(self) -> None:
        self.real = tail_chain.dispatch
        self.calls: list[list[str]] = []
        self.work: dict[str, Callable[[jobs.Job, jobs.Item], None]] = {}
        self.landing: Callable[[list[str]], tuple[int, dict[str, Any]]] = (
            lambda _argv: _refused(_gate("land-run"), outcome="blocked")
        )
        self.named: list[list[str]] = []

    def __call__(self, argv: list[str]) -> tuple[int, dict[str, Any]]:
        self.calls.append(list(argv))
        for step, verb, words in sync_land.TAIL:
            if tuple(argv[: len(words)]) == words:
                return self._job(step, verb, argv)
        if "name" in argv and "apply" in argv:
            self.named.append(list(argv))
            return _ok({"digest": "d", "items": [], "totals": {"renamed": 0}})
        if argv[:2] == ["intake", "land"]:
            return self.landing(argv)
        return self.real(argv)

    def _job(self, step: str, verb: str, argv: list[str]) -> tuple[int, dict[str, Any]]:
        if "--job" not in argv:
            folder = Path(argv[-1])
            files = tuple(sorted(p.name for p in folder.iterdir() if p.is_file()))
            if not files:
                return _ok({"job_id": None, "state": "no-tracks"}, outcome="no_op")
            job = _enqueue(config.load(), verb, {"folder": str(folder)}, *files)
            return _ok({"job_id": job.job_id, "state": "queued"})
        job_id = argv[argv.index("--job") + 1]
        work = self.work.get(step, lambda _job, _item: None)
        with jobs.open_store() as store:
            try:
                jobs.drive(store, job_id, work)
            except Exception:  # noqa: BLE001 - the queue records it, as the shell's does
                pass
            job = jobs.get(store, job_id)
        if job.state is jobs.JobState.SUCCEEDED:
            return _ok({"job_id": job_id, "state": str(job.state)})
        return _refused(job.cause)

    def verbs(self) -> list[tuple[str, ...]]:
        """Each command's verb words, in the order the pass ran them."""
        named = []
        for argv in self.calls:
            words = [a for a in argv if not a.startswith("-") and "/" not in a][:2]
            if argv[:1] == ["-d"]:
                words = ["name", "apply"]
            named.append(tuple(words))
        return named


@pytest.fixture
def tail(monkeypatch) -> Tail:
    stand_in = Tail()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    return stand_in


def _all_jobs() -> list[jobs.Job]:
    with jobs.open_store() as store:
        return list(jobs.list_jobs(store))


def _by_key(verb: str) -> list[jobs.Job]:
    key = registry.entry(verb).handler_key
    return [job for job in _all_jobs() if job.handler_key == key]


def _check(envelope: dict, step: str) -> dict:
    cause = envelope.get("cause") or {}
    data = (cause.get("detail") or {}).get("sync_land") or envelope["data"]
    (found,) = [c for c in data["checks"] if c["key"] == f"sync.land.{step}"]
    return found


def _summary(envelope: dict) -> dict:
    if envelope.get("cause") and "sync_land" in (envelope["cause"].get("detail") or {}):
        return envelope["cause"]["detail"]["sync_land"]["summary"]
    return envelope["data"]["summary"]


def _staged(cfg: config.Config) -> Path:
    return cfg.paths.download_staging.expanduser().absolute()


# 1. The declaration


def test_the_verb_queues_nothing_of_its_own_and_declares_one_gate_of_its_own():
    """Every job is queued by its own verb, every gate is its step's, the pass's own is inline."""
    assert ENTRY.landed and not ENTRY.long_running and ENTRY.argv_builder is None
    (gate,) = ENTRY.gates
    assert gate.name == sync_land.WITHOUT_VOCALS
    assert set(gate.options) == {sync_land.WITHOUT_VOCALS_GO, "stop"}
    assert not gate.explicit and gate.digest_source is None
    assert ENTRY.writes == frozenset({"files"}) and ENTRY.destructive
    assert ENTRY.module == "cratekit.cli.sync_land"


def test_the_tail_is_the_four_verbs_in_their_order():
    """The order is pinned: tag, analyse, restamp, then name."""
    assert [verb for _step, verb, _words in sync_land.TAIL] == [
        "tag.folder",
        "analyze.run",
        "analyze.restamp",
    ]
    for _step, verb, words in sync_land.TAIL:
        assert registry.entry(verb).path == words
    assert sync_land.STEPS.index(sync_land.NAME) > sync_land.STEPS.index(sync_land.RESTAMP)
    assert sync_land.STEPS.index(sync_land.LAND) == len(sync_land.STEPS) - 1


# 2. The brief's four scenarios


def test_a_pass_with_only_owned_tracks_ends_without_a_download_or_a_landing(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    for track_id in ("101", "102"):
        owned(cfg.library.root, f"Artist {track_id} - Title {track_id}.flac")

    envelope = exited(drive(["sync", "land"]))
    assert envelope["outcome"] == "no_op"
    assert _summary(envelope)["stopped_at"] == sync_land.MISSING
    assert "nothing is downloaded or landed" in _check(envelope, sync_land.MISSING)["detail"]
    assert _by_key("acquire.download") == []
    assert script.fetched == []
    assert ("intake", "land") not in tail.verbs()
    assert ("tag", "folder") not in tail.verbs()
    (intake,) = _by_key("intake.playlist")
    assert intake.state is jobs.JobState.SUCCEEDED, "the pass's intake job was not driven"


def test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one(
    machine, monkeypatch, tail
):
    cfg, script = machine
    ids = [str(100 + n) for n in range(8)]
    _account(monkeypatch, script, *ids, lossy=("107",))

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    (download,) = _by_key("acquire.download")
    # U169: the refusal is settled, so the job succeeded and the item carries it.
    assert download.state is jobs.JobState.SUCCEEDED
    with jobs.open_store() as store:
        (skipped,) = [
            i for i in jobs.items(store, download.job_id) if i.state is jobs.ItemState.SKIPPED
        ]
    assert skipped.item_id == "107" and skipped.cause.reason == "lossy-refused"
    summary = _summary(envelope)
    assert [row["item_id"] for row in summary["download_refused"]] == ["107"]
    assert summary["download_refused"][0]["reason"] == "lossy-refused"
    assert "landed 7 track(s); 1 refused and skipped" in _check(envelope, "download")["detail"]
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "sync-land-download-refused"]
    assert "107" in warning["message"] and "lossy-refused" in warning["message"]
    staged = sorted(p.name for p in _staged(cfg).iterdir() if p.is_file())
    assert staged == sorted(f"{track_id}.wav" for track_id in ids[:7])
    # The refusal did not end the pass: the tail ran and the landing was planned.
    assert ("intake", "land") in tail.verbs()
    assert summary["stopped_at"] == sync_land.LAND_GATE


def test_a_stale_queued_analyze_job_is_replaced_not_resumed(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    staging = _staged(cfg)
    staging.mkdir(parents=True, exist_ok=True)
    # No file of its own in the folder (R-1499), which would refuse the pass first.
    stale = _enqueue(cfg, "analyze.run", {"folder": str(staging)}, "old.wav")
    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert _state(stale.job_id) is jobs.JobState.CANCELLED
    assert {"step": "analyze", "job_id": stale.job_id} in _summary(envelope)["replaced"]
    assert not any(stale.job_id in argv for argv in tail.calls), "the stale job was resumed"
    fresh = [job for job in _by_key("analyze.run") if job.job_id != stale.job_id]
    assert len(fresh) == 1 and fresh[0].state is jobs.JobState.SUCCEEDED


def test_rekordbox_running_refuses_before_any_write(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)

    envelope = exited(drive(["sync", "land"]), ExitCode.REKORDBOX_OPEN)
    assert envelope["cause"]["reason"] == "rekordbox-running"
    assert tail.calls == [], "a step ran while rekordbox was up"
    assert _all_jobs() == []


def test_a_running_backup_refuses_before_any_write(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    backup = _enqueue(cfg, "backup.run", {}, "mirror")
    with jobs.driver_lock(backup.job_id):
        code, envelope = drive(["sync", "land"])
    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    assert envelope["cause"]["reason"] == "job-driver-held"
    assert backup.job_id in envelope["cause"]["message"]
    assert tail.calls == []
    assert [job.job_id for job in _all_jobs()] == [backup.job_id]


def test_a_backup_job_whose_driver_died_does_not_hold_the_pass(machine, monkeypatch, tail):
    """The lock is the liveness test, so an open row with no live driver is not running."""
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    for track_id in ("101", "102"):
        owned(cfg.library.root, f"Artist {track_id} - Title {track_id}.flac")
    _enqueue(cfg, "backup.run", {}, "mirror")
    envelope = exited(drive(["sync", "land"]))
    assert _check(envelope, sync_land.PREFLIGHT)["status"] == "ok"


# 3. The order, the tail and the stop


def test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    monkeypatch.chdir(cfg.library.root)

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    queued = [words for words in tail.verbs() if words != ("intake", "playlist")]
    assert queued == [
        ("sync", "all"), ("intake", "missing"), ("acquire", "download"), ("acquire", "download"),
        ("tag", "folder"), ("tag", "folder"), ("tag", "guess"), ("analyze", "run"),
        ("analyze", "run"), ("analyze", "restamp"), ("analyze", "restamp"), ("name", "apply"),
        ("intake", "land"),
    ]
    staging = str(_staged(cfg))
    assert Path(staging).is_absolute()
    # U172: the genre guess runs over the same absolute folder, with the land name as its pass.
    (guessed,) = [argv for argv in tail.calls if argv[:2] == ["tag", "guess"]]
    assert guessed[2] == staging
    assert guessed[guessed.index("--pass") + 1] == _summary(envelope)["land_name"]
    assert _check(envelope, sync_land.GUESS)["status"] == "ok"
    (named,) = tail.named
    assert named[named.index("--root") + 1] == staging
    assert named[:2] == ["-d", f"{sync_land.NAME_GATE}={sync_land.NAME_OPTION}"]
    land = tail.calls[-1]
    assert land[2] == staging
    assert land[land.index("--pass") + 1] == _summary(envelope)["land_name"]
    assert _summary(envelope)["land_name"].endswith("_synced")
    for step in (sync_land.TAG, sync_land.ANALYZE, sync_land.RESTAMP):
        assert _check(envelope, step)["status"] == "ok"
    for verb in ("tag.folder", "analyze.run", "analyze.restamp"):
        (job,) = _by_key(verb)
        assert job.state is jobs.JobState.SUCCEEDED, verb
        assert job.payload["folder"] == staging


def test_each_tail_step_queues_only_and_drives_its_job_through_one_job_command(
    machine, monkeypatch, tail
):
    """By hand the tail verbs drive what they queue, so the pass queues, then drives once (U192)."""
    from cratekit.modules import foreground

    cfg, script = _ready(machine, monkeypatch, "101")

    exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    for _step, verb, words in sync_land.TAIL:
        calls = [argv for argv in tail.calls if tuple(argv[: len(words)]) == words]
        queued = [argv for argv in calls if "--job" not in argv]
        driven = [argv for argv in calls if "--job" in argv]
        assert len(queued) == 1 and foreground.QUEUE_ONLY in queued[0], (verb, calls)
        (job,) = _by_key(verb)
        assert driven == [[*words, job.payload["folder"], "--job", job.job_id]], (verb, calls)


def test_the_stop_at_the_landing_gate_names_the_session_commands_and_the_visit(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert envelope["outcome"] == "pending"
    pending = envelope["pending_human_action"]
    assert pending["kind"] == "external_step" and pending["verify_verb"] == "intake.land"
    steps = pending["steps"]
    decide = f"crate run decide land-run {sync_land.LAND_GATE} apply --actor session"
    assert steps[0].endswith(decide)
    land = " ".join(tail.calls[-1])
    assert steps[1] == f"apply it: crate --run land-run {land}"
    # U166: the visit fills the one playlist every landing fills, and its clear closes the visit.
    assert steps[-1].endswith("crate inbox analyzed")
    analyse = [step for step in steps if "Analyze Tracks" in step]
    assert analyse and "KEY on" in analyse[0] and "Normal" in analyse[0]
    assert "INBOX / Analyze" in analyse[0]
    # U163: the row carries its tags from the landing, so the visit never asks Reload Tags.
    assert not any("Reload Tags" in step for step in steps)
    assert envelope["cause"]["reason"] == "awaiting-human-action"
    assert _summary(envelope)["gate_run"] == "land-run"


def test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    tail.landing = _backup_missing
    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    pending = envelope["pending_human_action"]
    assert pending["kind"] == "backup_ack"
    land = " ".join(tail.calls[-1])
    assert f"then plan the landing again: crate {land}" in pending["steps"]
    assert _summary(envelope)["stopped_at"] == "backup-acknowledgment-missing"
    assert not (cfg.library.root / "ack").exists()


def test_a_failed_tail_step_plans_no_landing_and_names_the_continuation(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    tail.work[sync_land.ANALYZE] = _broken
    envelope = exited(drive(["sync", "land"]), ExitCode.MODULE_UNAVAILABLE)
    assert envelope["cause"]["reason"] == "module-extras-missing"
    assert ("intake", "land") not in tail.verbs()
    assert ("analyze", "restamp") not in tail.verbs()
    assert not tail.named, "name apply ran after a failed analysis"
    assert _check(envelope, sync_land.ANALYZE)["status"] == "fail"
    assert _check(envelope, sync_land.ANALYZE)["remedy"] != "None"
    run_id = _summary(envelope)["pass_run"]
    assert any(
        f"crate sync land --pass-run {run_id}" in step
        for step in envelope["cause"]["remediation"]["steps"]
    )
    assert "sync.land" in envelope["cause"]["origin"]


def test_a_tail_step_with_nothing_to_queue_plans_no_landing(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    nothing = _ok({"job_id": None, "state": "no-tracks"}, outcome="no_op")
    _step_answers(monkeypatch, tail, sync_land.TAG, nothing)
    envelope = failed(drive(["sync", "land"]))
    assert envelope["cause"]["reason"] == "source-missing"
    assert ("analyze", "run") not in tail.verbs()
    assert ("intake", "land") not in tail.verbs()


def test_a_parked_download_ends_the_pass_blocked_before_the_tail(machine, monkeypatch, tail):
    """A provider that refused the client is a block, never a refusal to skip."""
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    real = tail.real

    def parked(argv):
        if argv[:2] == ["acquire", "download"] and "--job" in argv:
            job_id = argv[argv.index("--job") + 1]
            cause = Cause(
                reason="provider-blocked",
                message="the provider refused the client",
                remediation=Remediation(remedy=Remedy.RESUME_JOB),
                retryable=True,
                origin=("test",),
            )
            with jobs.open_store() as store:
                jobs.block(store, job_id, cause)
            return _refused(jobs.get(jobs.open_store(), job_id).cause, outcome="blocked")
        return real(argv)

    tail.real = parked

    code, envelope = drive(["sync", "land"])

    assert envelope["outcome"] == "blocked", envelope
    assert envelope["cause"]["reason"] == "provider-blocked"
    assert ("tag", "folder") not in tail.verbs()


# 4. Continuing a pass


def test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    first = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    run_id = _summary(first)["pass_run"]
    fetched = len(script.fetched)
    tail.calls.clear()

    again = exited(drive(["sync", "land", "--pass-run", run_id]), ExitCode.PENDING_HUMAN)
    assert ("sync", "all") not in tail.verbs()
    assert len(_by_key("acquire.download")) == 1
    assert len(script.fetched) == fetched, "a settled download was fetched again"
    assert _summary(again)["download_job"] == _summary(first)["download_job"]


def test_a_continued_pass_over_an_open_intake_job_drives_it_first(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    passed = exited(drive(["sync", "all"]))
    run_id = passed["run_id"]
    (intake,) = _by_key("intake.playlist")
    assert intake.state is jobs.JobState.QUEUED

    exited(drive(["sync", "land", "--pass-run", run_id]), ExitCode.PENDING_HUMAN)
    assert tail.verbs()[0] == ("intake", "playlist")
    (intake,) = _by_key("intake.playlist")
    assert intake.state is jobs.JobState.SUCCEEDED


def test_a_continued_pass_naming_no_intake_job_is_refused_in_the_preflight(machine, tail):
    envelope = failed(drive(["sync", "land", "--pass-run", "no-such-run"]))
    assert envelope["cause"]["reason"] == "job-unknown"
    assert tail.calls == [], "a step ran before the unknown id was refused (U183)"


# 5. What the pass carries through


def test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried(tmp_path, monkeypatch):
    cfg, _script = _machine(tmp_path, monkeypatch, "full")
    fake = bind_hearts(monkeypatch, ShortHearts(_hearts("301", "302", "303"), declared=5))
    for track_id in ("301", "302", "303"):
        owned(cfg.library.root, f"Heart Artist {track_id} - Heart {track_id}.flac")

    envelope = exited(drive(["sync", "land"]))
    failing = [c for c in envelope["data"]["checks"] if c["status"] == "fail"]
    assert len(failing) == 1 and "2 withheld by the provider" in failing[0]["detail"]
    assert fake.heart_listings == 1, "the shortfall was retried"


def test_the_outbound_hearts_write_stays_behind_its_own_gate(tmp_path, monkeypatch):
    """No export is handed to the pass, so the favourites write half queues nothing."""
    cfg, _script = _machine(tmp_path, monkeypatch, "full")
    bind_hearts(monkeypatch)
    for track_id in ("301", "302", "303"):
        owned(cfg.library.root, f"Heart Artist {track_id} - Heart {track_id}.flac")

    envelope = exited(drive(["sync", "land"]))
    assert _by_key("sync.favorites") == []
    assert any(w["code"] == "sync-source-not-queued" for w in envelope["warnings"])
    checks = envelope["data"]["checks"]
    assert not [c for c in checks if c["key"] == "sync.favorites"], "the unasked write is a FAIL row"
    assert any(
        c["key"] == "sync.land.sync" and "outbound hearts write is not this verb's" in c["detail"]
        for c in checks
    )


def test_a_step_with_no_readable_envelope_is_a_defect_not_a_success(machine, monkeypatch):
    monkeypatch.setattr(tail_chain, "dispatch", lambda argv: (int(ExitCode.OK), {}))

    envelope = failed(drive(["sync", "land"]))
    assert envelope["cause"]["reason"] == "internal-error"
    assert "sync all" in envelope["cause"]["message"]


def test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes(
    machine, monkeypatch, tail
):
    """A step's gate is answered on that step's own run, never on this verb's."""
    cfg, script = _ready(machine, monkeypatch, "101")
    gate = _refused(_gate("restamp-run", "write.cloudsync.unreadable"), outcome="blocked")
    _step_answers(monkeypatch, tail, sync_land.RESTAMP, gate)
    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert envelope["resumable"] is False
    steps = envelope["pending_human_action"]["steps"]
    assert "crate run decide restamp-run write.cloudsync.unreadable" in steps[0]
    assert steps[-1].endswith(f"crate sync land --pass-run {_summary(envelope)['pass_run']}")
    assert ("intake", "land") not in tail.verbs()


def test_the_default_output_prints_each_step_and_what_the_session_does_next(
    machine, monkeypatch, tail
):
    """A person reads the human output; the json is not where the next step lives."""
    from tests.cli_drive import drive_human

    cfg, script = _ready(machine, monkeypatch, "101")

    text = exited(drive_human(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert "sync.land.download" in text
    assert "--actor session" in text
    assert "Analyze Tracks" in text


def test_a_job_another_driver_holds_ends_the_pass_with_that_drivers_refusal(
    machine, monkeypatch, tail
):
    """A job still running elsewhere was never driven here, and the pass says whose it is."""
    cfg, script = _ready(machine, monkeypatch, "101")
    passed = exited(drive(["sync", "all"]))
    (intake,) = _by_key("intake.playlist")

    with jobs.driver_lock(intake.job_id):
        code, envelope = drive(["sync", "land", "--pass-run", passed["run_id"]])

    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    assert envelope["cause"]["reason"] == "job-driver-held"
    assert intake.job_id in envelope["cause"]["message"]
    assert ("intake", "missing") not in tail.verbs()


# 6. Passes queued by hand, transient failures and foreign jobs


def test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes(
    machine, monkeypatch, tail
):
    """A sync all typed by hand, its jobs queued and idle, is the pass this verb takes."""
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    passed = exited(drive(["sync", "all"]))
    (intake,) = _by_key("intake.playlist")
    assert intake.state is jobs.JobState.QUEUED

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert _summary(envelope)["pass_run"] == passed["run_id"]
    (intake,) = _by_key("intake.playlist")
    assert intake.state is jobs.JobState.SUCCEEDED
    assert ("intake", "land") in tail.verbs()
    notes = [c["detail"] for c in envelope["data"]["checks"] if c["key"] == "sync.land.sync"]
    assert any(passed["run_id"] in note and intake.job_id in note for note in notes)


def test_two_earlier_passes_holding_open_jobs_are_a_choice_named_not_made(
    machine, monkeypatch, tail
):
    cfg, script = machine
    runs = ["run-one", "run-two"]
    for run_id in runs:
        _enqueue(cfg, "intake.playlist", {"source": f"pl-{run_id}", "run_id": run_id}, "101")
    bind_playlists(monkeypatch)

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    steps = envelope["pending_human_action"]["steps"]
    assert steps == [f"continue one pass: crate sync land --pass-run {run}" for run in runs]
    assert not any(argv[:2] == ["intake", "playlist"] for argv in tail.calls), "a pass was chosen"


def test_a_listing_with_nothing_nameable_says_so_and_carries_its_failing_row(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    real = tail.real
    unlisted = {
        "key": "intake.missing.unlisted",
        "title": "unlisted",
        "status": "fail",
        "detail": "1 missing track(s) the provider cannot name exactly are NOT in the list",
        "remedy": None,
    }

    def listing(argv):
        if argv[:2] == ["intake", "missing"]:
            return _ok(
                {
                    "checks": [unlisted],
                    "summary": {"list": None, "unlisted": 1, "owned": 0, "offered": 0},
                },
                outcome="no_op",
            )
        return real(argv)

    tail.real = listing

    envelope = exited(drive(["sync", "land"]))
    assert unlisted in envelope["data"]["checks"]
    detail = _check(envelope, sync_land.MISSING)["detail"]
    assert "missing and not nameable 1" in detail and "found nothing missing" not in detail


def test_an_intake_job_that_ended_failed_names_its_retry_not_a_continuation(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    code, passed = drive(["sync", "all"])
    (intake,) = _by_key("intake.playlist")
    _failed_intake(intake.job_id, "the catalogue broke", Remedy.REPORT_DEFECT)
    code, envelope = drive(["sync", "land", "--pass-run", passed["run_id"]])

    assert envelope["cause"]["reason"] == "adapter-broken", envelope
    steps = envelope["cause"]["remediation"]["steps"]
    assert not any("--pass-run" in step for step in steps), "a continuation that cannot advance"
    assert any("start a new pass with: crate sync land" in step for step in steps)


def test_a_transient_download_failure_ends_the_pass_and_lands_nothing(machine, monkeypatch, tail):
    """Only a refusal for good is skipped; a failure that waiting mends is not landed."""
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    script.landings["102"] = Landing(fetch_raises=TimeoutError("the provider timed out"))

    failed(drive(["sync", "land"]))
    (download,) = _by_key("acquire.download")
    assert download.state is jobs.JobState.FAILED and download.cause.retryable
    assert ("tag", "folder") not in tail.verbs()
    assert ("intake", "land") not in tail.verbs()


def test_a_continued_pass_retries_a_download_that_failed_transiently(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    script.landings["102"] = Landing(
        fetch_raises=TimeoutError("the provider timed out"), fetch_raises_times=1
    )
    first = failed(drive(["sync", "land"]))
    run_id = _summary(first)["pass_run"]

    exited(drive(["sync", "land", "--pass-run", run_id]), ExitCode.PENDING_HUMAN)
    (download,) = _by_key("acquire.download")
    assert download.state is jobs.JobState.SUCCEEDED
    assert [request.key for request in script.fetched].count("101") == 1


def test_a_cancelled_download_over_the_same_list_is_not_reused(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    real = tail.real

    def undriven(argv):
        # The download's command answers without driving it, so the first pass stops there.
        if argv[:2] == ["acquire", "download"] and "--job" in argv:
            return _refused(refuse("job-driver-held", "held elsewhere", origin=("test",)).cause)
        return real(argv)

    tail.real = undriven
    first = failed(drive(["sync", "land"]))
    (download,) = _by_key("acquire.download")
    _cancel(download.job_id)
    tail.real = real

    code, again = drive(["sync", "land", "--pass-run", _summary(first)["pass_run"]])

    assert code == int(ExitCode.PENDING_HUMAN), again
    assert _summary(again)["download_job"] != download.job_id
    assert len(_by_key("acquire.download")) == 2


def test_a_fresh_pass_never_reuses_another_lists_download_job(machine, monkeypatch, tail):
    cfg, script = machine
    other = cfg.library.root / "other.list.json"
    from tests.acquire_fakes import tidal_list

    other.write_text(tidal_list([("901", "Other", "Track")]))
    with jobs.open_store() as store:
        queued = acquire_cli.queue_list(
            store, cfg, other, handler_key=registry.entry("acquire.download").handler_key
        )
    _account(monkeypatch, script, "101")

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert _summary(envelope)["download_job"] != queued.job_id
    assert _state(queued.job_id) is jobs.JobState.QUEUED


def test_a_name_apply_refusal_ends_the_pass_before_the_landing(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    original = tail.__call__

    def refusing(argv):
        if "name" in argv and "apply" in argv:
            tail.calls.append(list(argv))
            return _refused(
                refuse("rename-incomplete", "two renames did not land", origin=("test",)).cause
            )
        return original(argv)

    monkeypatch.setattr(tail_chain, "dispatch", refusing)

    code, envelope = drive(["sync", "land"])

    assert envelope["cause"]["reason"] == "rename-incomplete", envelope
    assert not any(argv[:2] == ["intake", "land"] for argv in tail.calls)


def test_a_stale_job_over_another_folder_or_library_is_left_alone(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    elsewhere = cfg.library.root / "elsewhere"
    elsewhere.mkdir()
    other_folder = _enqueue(cfg, "analyze.run", {"folder": str(elsewhere)}, "a")
    other_library = _enqueue(
        dataclasses_replace_library(cfg), "analyze.run", {"folder": str(_staged(cfg))}, "b"
    )
    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert _state(other_folder.job_id) is jobs.JobState.QUEUED
    assert _state(other_library.job_id) is jobs.JobState.QUEUED
    assert _summary(envelope)["replaced"] == []


def dataclasses_replace_library(cfg: config.Config) -> config.Config:
    """The same machine naming another library, so a job queued under it is not ours."""
    import dataclasses

    return dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, volume_id="another-volume")
    )


def test_a_stale_job_a_live_driver_holds_is_not_cancelled(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    staging = _staged(cfg)
    staging.mkdir(parents=True, exist_ok=True)
    held = _enqueue(cfg, "tag.folder", {"folder": str(staging)}, "x.wav")
    with jobs.driver_lock(held.job_id):
        code, envelope = drive(["sync", "land"])
    assert envelope["cause"]["reason"] == "job-driver-held", envelope
    assert _state(held.job_id) is jobs.JobState.QUEUED
    assert not any(argv[:2] == ["tag", "folder"] for argv in tail.calls)


def test_the_acknowledgment_stop_names_the_gate_the_replanned_landing_will_ask(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    tail.landing = _backup_missing
    code, envelope = drive(["sync", "land"])
    steps = envelope["pending_human_action"]["steps"]
    replan = next(i for i, step in enumerate(steps) if step.startswith("then plan the landing"))
    assert "answer it as the session" in steps[replan + 1]
    assert "Analyze Tracks" in steps[replan + 2]


# 7. Earlier passes and repeated downloads


def test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on(
    machine, monkeypatch, tail
):
    """A new pass drives only its own run; an earlier hand typed one is named with its command."""
    cfg, script = _ready(machine, monkeypatch, "101")
    earlier = exited(drive(["sync", "all"]))
    (held,) = _by_key("intake.playlist")
    script.landings["201"] = Landing()
    bind_playlists(monkeypatch, *_warmup_and_peak())

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert _summary(envelope)["pass_run"] != earlier["run_id"]
    row = _check(envelope, "left-open")
    assert row["status"] == "fail"
    assert held.job_id in row["detail"]
    assert f"crate sync land --pass-run {earlier['run_id']}" in row["detail"]
    assert _summary(envelope)["left_open"] == [held.job_id]
    assert any(w["code"] == "sync-land-intake-left-open" for w in envelope["warnings"])


def test_an_intake_job_queued_by_hand_with_no_pass_is_named_not_passed_over(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    queued = exited(drive(["intake", "playlist", "pl-a"]))
    job_id = queued["data"]["job_id"]

    envelope = exited(drive(["sync", "land"]))
    assert envelope["outcome"] == "no_op"
    row = _check(envelope, "left-open")
    assert row["status"] == "fail"
    assert f"crate intake playlist pl-a --job {job_id}" in row["detail"]


def test_the_newest_download_over_the_list_is_the_one_the_pass_reads(machine, monkeypatch, tail):
    """A first download refused both tracks; a second, typed by hand, landed both."""
    cfg, script = _ready(machine, monkeypatch, "101", "102", lossy=("101", "102"))
    code, first = drive(["sync", "land"])
    assert code == int(ExitCode.OK) and first["outcome"] == "no_op", first
    listed = _summary(first)["list"]
    script.landings["101"] = Landing()
    script.landings["102"] = Landing()
    queued = exited(drive(["acquire", "download", listed]))
    exited(drive(["acquire", "download", "--job", queued["data"]["job_id"]]))

    code, again = drive(["sync", "land", "--pass-run", _summary(first)["pass_run"]])

    assert code == int(ExitCode.PENDING_HUMAN), again
    assert _summary(again)["download_job"] == queued["data"]["job_id"]
    assert _summary(again)["download_refused"] == []
    assert ("intake", "land") in tail.verbs()


def test_every_download_refused_lands_nothing_on_a_failing_row(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101", "102", lossy=("101", "102"))

    code, envelope = drive(["sync", "land"])

    assert envelope["outcome"] == "no_op", envelope
    row = _check(envelope, sync_land.DOWNLOAD)
    assert row["status"] == "fail" and "landed no track; 2 refused" in row["detail"]
    assert ("tag", "folder") not in tail.verbs()


def test_a_stale_answer_from_a_step_is_the_steps_own_and_never_resumes_this_run(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    tail.landing = lambda _argv: _refused(
        Cause(
            reason="decision-stale",
            message="the plan moved since the answer",
            remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
            retryable=True,
            origin=("test",),
            detail={"gate": sync_land.LAND_GATE, "run_id": "land-run"},
        ),
        outcome="blocked",
    )

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert envelope["resumable"] is False
    land = " ".join(tail.calls[-1])
    assert f"then run the step again: crate {land}" in envelope["pending_human_action"]["steps"]


def test_a_job_command_that_stops_at_a_gate_is_that_commands_gate(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    gate = _refused(_gate("tag-run", "write.cloudsync.unreadable"), outcome="blocked")
    _step_answers(monkeypatch, tail, sync_land.TAG, gate, driven=True)
    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert envelope["resumable"] is False
    assert "crate run decide tag-run write.cloudsync.unreadable" in (
        envelope["pending_human_action"]["steps"][0]
    )


def test_an_earlier_pass_that_ended_or_belongs_to_another_library_is_not_continued(
    machine, monkeypatch, tail
):
    cfg, script = machine
    foreign_payload = {"source": "pl-x", "run_id": "foreign-run"}
    foreign = _enqueue(dataclasses_replace_library(cfg), "intake.playlist", foreign_payload, "1")
    ended = _enqueue(cfg, "intake.playlist", {"source": "pl-y", "run_id": "ended-run"}, "2")
    _cancel(ended.job_id)
    bind_playlists(monkeypatch)

    envelope = exited(drive(["sync", "land"]))
    assert envelope["outcome"] == "no_op"
    assert _summary(envelope)["pass_run"] not in ("foreign-run", "ended-run")
    assert not any(argv[:2] == ["intake", "playlist"] for argv in tail.calls)
    assert _state(foreign.job_id) is jobs.JobState.QUEUED


# U182: stale intake jobs, named by playlist, let go by a cancel


def _age(job_id: str, days: float) -> None:
    stamp = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    with jobs.open_store() as store, store.immediate() as conn:
        conn.execute("UPDATE jobs SET created = ? WHERE job_id = ?", (stamp, job_id))


def _cancelled_pass(cfg: config.Config, run_id: str) -> None:
    """A pass ``--pass-run`` resolves (U183) whose one intake job was cancelled."""
    _cancel(_enqueue(cfg, "intake.playlist", {"source": "pl-gone", "run_id": run_id}, "901").job_id)


def test_the_left_open_row_names_each_playlist_its_age_size_and_copies(machine, monkeypatch, tail):
    """Each playlist on the left open row carries its age, size and copies, not ids alone."""
    cfg, script = machine
    for job_id, source, name in (("copy-a", "pl-a", "Warmup"), ("copy-b", "pl-b", "Warmup Two")):
        payload = {"source": source, "playlist_name": name, "run_id": "old-run"}
        _enqueue(cfg, "intake.playlist", payload, "101", "102", job_id=job_id)
    _age("copy-a", 44)
    _age("copy-b", 43)
    bind_playlists(monkeypatch)
    _cancelled_pass(cfg, "other-run")

    code, envelope = drive(["sync", "land", "--pass-run", "other-run"])
    row = _check(envelope, "left-open")
    assert row["status"] == "fail"
    detail = row["detail"]
    assert "for 2 playlist(s)" in detail
    assert "playlist 'Warmup' (pl-a): copy-a (queued, 44 day(s) old, 2 track(s), the same tracks as copy-b)" in detail
    assert "playlist 'Warmup Two' (pl-b): copy-b (queued, 43 day(s) old" in detail
    assert "Cancelling a job lets its playlist's increment queue again on the next pass" in detail
    assert "crate job cancel --stale-days DAYS --dry-run" in detail
    grouped = _summary(envelope)["left_open_playlists"]
    # Newest first, the order every open job is read in.
    assert [group["playlist"] for group in grouped] == [
        "playlist 'Warmup Two' (pl-b)",
        "playlist 'Warmup' (pl-a)",
    ]
    by_job = {job["job_id"]: job for group in grouped for job in group["jobs"]}
    assert by_job["copy-a"]["age_days"] == 44 and by_job["copy-a"]["tracks"] == 2
    assert by_job["copy-a"]["same_tracks"] == ["copy-b"]


def test_a_pass_after_the_stale_cancel_queues_the_freed_playlist(machine, monkeypatch, tail):
    """The cancel is what lets the playlist queue again."""
    cfg, script = _ready(machine, monkeypatch, "101")
    exited(drive(["sync", "all"]))
    (stale,) = _by_key("intake.playlist")
    _age(stale.job_id, 40)
    code, again = drive(["sync", "all"])
    assert again["outcome"] == "no_op", "an open job did not hold its playlist out"

    cancelled = exited(drive(["job", "cancel", "--stale-days", "30"]))
    (row,) = cancelled["data"]["progress"]["cancel"]
    assert row["job_id"] == stale.job_id
    assert row["frees"] == "frees playlist 'Warmup' (pl-a), so the next pass queues it again"

    exited(drive(["sync", "all"]))
    queued = [job for job in _by_key("intake.playlist") if job.job_id != stale.job_id]
    assert len(queued) == 1 and queued[0].state is jobs.JobState.QUEUED
    assert queued[0].payload["playlist_name"] == "Warmup"


def test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest(
    machine, monkeypatch, tail
):
    """A cancel's copy in the same run is reported cancelled, and the kept job goes on."""
    cfg, script = machine
    script.landings["101"] = Landing()
    script.landings["201"] = Landing()
    bind_playlists(monkeypatch, *_warmup_and_peak())
    passed = exited(drive(["sync", "all"]))
    first, second = _by_key("intake.playlist")
    _cancel(first.job_id)
    code, envelope = drive(["sync", "land", "--pass-run", passed["run_id"]])
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert _state(first.job_id) is jobs.JobState.CANCELLED
    assert _state(second.job_id) is jobs.JobState.SUCCEEDED
    assert not any(first.job_id in argv for argv in tail.calls), "a cancelled job was driven"
    notes = [c["detail"] for c in envelope["data"]["checks"] if c["key"] == "sync.land.intake"]
    assert any(f"{first.job_id}" in note and "cancelled" in note for note in notes)
    assert _summary(envelope)["cancelled_jobs"] == [first.job_id]
    assert ["intake", "missing", "--run", passed["run_id"], "--skip-failed"] in tail.calls


def test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    code, passed = drive(["sync", "all"])
    (intake,) = _by_key("intake.playlist")
    _cancel(intake.job_id)
    envelope = exited(drive(["sync", "land", "--pass-run", passed["run_id"]]))
    assert envelope["outcome"] == "no_op"
    detail = _check(envelope, sync_land.INTAKE)["detail"]
    assert "cancelled" in detail and "crate sync land" in detail
    assert "job resume" not in detail and "--pass-run" not in detail
    assert _summary(envelope)["stopped_at"] == sync_land.INTAKE
    assert not any(argv[:2] == ["intake", "missing"] for argv in tail.calls)
    assert _state(intake.job_id) is jobs.JobState.CANCELLED


def test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row(
    machine, monkeypatch, tail
):
    """Grouped as the pass holds them, not as typed."""
    cfg, script = machine
    uuid = "0f6e2c3a-1b2d-4e5f-8a9b-0c1d2e3f4a5b"
    swept = dict(source=uuid, source_id="playlists", playlist_name="Warmup", run_id="old-run")
    _enqueue(cfg, "intake.playlist", swept, "101", job_id="swept")
    typed = {"source": f"https://tidal.com/playlist/{uuid}"}
    _enqueue(cfg, "intake.playlist", typed, "102", job_id="typed")
    bind_playlists(monkeypatch)
    _cancelled_pass(cfg, "other-run")
    code, envelope = drive(["sync", "land", "--pass-run", "other-run"])
    assert "for 1 playlist(s)" in _check(envelope, "left-open")["detail"]
    (group,) = _summary(envelope)["left_open_playlists"]
    # Headed by the account's name, though the typed job is the newer.
    assert group["playlist"] == f"playlist 'Warmup' ({uuid})"
    assert sorted(job["job_id"] for job in group["jobs"]) == ["swept", "typed"]


# U181. A pass refuses to land rows with no vocal score, unless told to go on

_NO_EXTRA = (
    "the 'vocals' extra is not installed here; "
    "pipx install --force 'cratekit[analysis,vocals] @ git+https://example.invalid/c@v0.3.0'"
)
#: The pass told up front to go on without vocal scores.
_GO_ON = ["-d", f"{sync_land.WITHOUT_VOCALS}={sync_land.WITHOUT_VOCALS_GO}", "sync", "land"]


@pytest.fixture
def full(tmp_path, monkeypatch):
    """The full profile, which switches on the vocals module."""
    return _machine(tmp_path, monkeypatch, "full")


def _model_cannot_score(monkeypatch) -> None:
    """No loader bound, and the extra missing."""
    from cratekit.analysis import vocals

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    monkeypatch.setattr(vocals, "missing_requirement", lambda: _NO_EXTRA)


def test_a_pass_whose_vocal_model_cannot_score_stops_at_its_gate_before_queueing_anything(
    full, monkeypatch, tail
):
    cfg, script = _ready(full, monkeypatch, "101")
    _model_cannot_score(monkeypatch)

    envelope = exited(drive(["sync", "land"]), ExitCode.DECISION_REQUIRED)
    assert envelope["resumable"] is True
    detail = envelope["cause"]["detail"]
    assert detail["gate"] == sync_land.WITHOUT_VOCALS
    shown = detail["shown"]
    assert "pipx install --force 'cratekit[analysis,vocals]" in shown["vocal model"]
    assert "no voxlevel" in shown["without it"]
    assert shown["to go on without vocal scores"] == (
        f"crate -d {sync_land.WITHOUT_VOCALS}={sync_land.WITHOUT_VOCALS_GO} sync land"
    )
    assert _all_jobs() == [], "the pass queued something before it stopped"
    assert tail.calls == [], "a step ran before the stop"


def test_a_continued_pass_is_told_the_answer_that_continues_it(full, monkeypatch, tail):
    _model_cannot_score(monkeypatch)
    _cancelled_pass(full[0], "run-earlier")
    code, envelope = drive(["sync", "land", "--pass-run", "run-earlier"])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    shown = envelope["cause"]["detail"]["shown"]
    assert shown["to go on without vocal scores"].endswith("sync land --pass-run run-earlier")


def test_answering_stop_refuses_with_the_command_that_mends_it(full, monkeypatch, tail):
    _model_cannot_score(monkeypatch)
    code, envelope = drive(["-d", f"{sync_land.WITHOUT_VOCALS}=stop", "sync", "land"])
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == sync_land.VOCALS_UNAVAILABLE
    assert "pipx install --force 'cratekit[analysis,vocals]" in cause["message"]
    assert _all_jobs() == []
    assert tail.calls == []


def test_the_gate_recorded_by_a_separate_act_continues_the_same_run(full, monkeypatch, tail):
    """The second way any gate is answered: run decide, then --run."""
    cfg, script = _ready(full, monkeypatch, "101")
    _model_cannot_score(monkeypatch)
    refused = exited(drive(["sync", "land"]), ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    answer = ["run", "decide", run_id, sync_land.WITHOUT_VOCALS, sync_land.WITHOUT_VOCALS_GO]
    decided, answer = drive(answer)
    assert decided == int(ExitCode.OK), answer
    envelope = exited(drive(["--run", run_id, "sync", "land"]), ExitCode.PENDING_HUMAN)
    assert _summary(envelope)["vocal_scoring"] == "skipped"


def test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped(
    full, monkeypatch, tail
):
    cfg, script = _ready(full, monkeypatch, "101")
    _model_cannot_score(monkeypatch)
    code, envelope = drive(_GO_ON)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    summary = _summary(envelope)
    assert summary["vocal_scoring"] == "skipped"
    assert summary["vocal_rescore"] == "skipped", "the tail did not ask a model it was told is absent"
    (row,) = [c for c in envelope["data"]["checks"] if c["key"] == "sync.land.vocal-model"]
    assert row["status"] == "info" and _NO_EXTRA in row["detail"]
    assert sync_land.WITHOUT_VOCALS_WARNING in [w["code"] for w in envelope["warnings"]]
    assert ("tag", "folder") in tail.verbs(), "the pass ran on"


def test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing(full, monkeypatch, tail):
    cfg, script = _ready(full, monkeypatch, "101")

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert _summary(envelope)["vocal_scoring"] == "available"
    (row,) = [c for c in envelope["data"]["checks"] if c["key"] == "sync.land.vocal-model"]
    assert row["status"] == "ok"


def test_a_profile_with_the_vocals_module_off_is_not_asked(machine, monkeypatch, tail):
    """Slim switches the module off: the person chose not to score vocals."""
    cfg, script = _ready(machine, monkeypatch, "101")
    _model_cannot_score(monkeypatch)

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    assert _summary(envelope)["vocal_scoring"] == "off"
    assert _summary(envelope)["vocal_rescore"] == "off"


def test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp(
    full, monkeypatch, tail
):
    """The vocals restamp over the staging folder, between the run and the restamp."""
    cfg, script = _ready(full, monkeypatch, "101")

    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    verbs = tail.verbs()
    vocals_at = verbs.index(("analyze", "vocals"))
    assert verbs.index(("analyze", "run")) < vocals_at < verbs.index(("analyze", "restamp"))
    (call,) = [argv for argv in tail.calls if argv[:2] == ["analyze", "vocals"]]
    assert call == ["analyze", "vocals", tail_chain.VOCALS_UNSCORED, str(_staged(cfg))]
    (row,) = [c for c in envelope["data"]["checks"] if c["key"] == "sync.land.rescore"]
    assert row["status"] == "ok", "a staging folder whose files carry no head owes no score"


def test_a_warning_the_landing_plan_carries_rides_the_passes_own_warnings(
    machine, monkeypatch, tail
):
    """A stop at the gate is a refusal with no warnings channel, so the plan's
    warning reaches the pass's envelope only by being lifted off the screen."""
    cfg, script = _ready(machine, monkeypatch, "101")
    shown = {"warnings": [{"code": "vox-mostly-unscored", "message": "19 of the 19 row(s)"}]}
    gate = _gate("land-run", shown=shown)
    tail.landing = lambda _argv: _refused(gate, outcome="blocked")
    envelope = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    lifted = [w for w in envelope["warnings"] if w["code"] == "vox-mostly-unscored"]
    assert lifted == [{"code": "vox-mostly-unscored", "message": "land: 19 of the 19 row(s)"}]


def test_the_tail_asks_the_vocal_model_before_analyze_run_binds_its_loader(full, monkeypatch, tail):
    """The question is asked before ``analyze run`` binds the loader, which reads as able."""
    from cratekit.analysis import vocals

    cfg, script = _ready(full, monkeypatch, "101")
    _model_cannot_score(monkeypatch)

    def binds_the_loader(_job, _item):
        monkeypatch.setattr(vocals, "_VOCAL_LOADER", lambda: object())

    tail.work[sync_land.ANALYZE] = binds_the_loader
    code, envelope = drive(_GO_ON)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert vocals.loader_bound(), "the stand in never ran, so the order was not tested"
    assert _summary(envelope)["vocal_rescore"] == "skipped"
    assert ("analyze", "vocals") not in tail.verbs()


# U183. Either run id continues the pass


def _record(run_id: str) -> dict[str, Any]:
    return json.loads(gates.run_path(run_id).read_text())


def _land_runs() -> list[str]:
    """Every sync land run the record directory holds, oldest first."""
    return sorted(
        path.stem
        for path in gates.run_dir().glob("*.json")
        if json.loads(path.read_text()).get("verb") == "sync.land"
    )


def test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id(
    machine, monkeypatch, tail
):
    """Continuing by the land run's own id reaches the same jobs as by the pass id."""
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    first = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    land_run, pass_run = first["run_id"], _summary(first)["pass_run"]
    assert land_run != pass_run
    assert _record(land_run)["related_runs"] == {"pass_run": pass_run}
    fetched = len(script.fetched)
    tail.calls.clear()

    by_land = exited(drive(["sync", "land", "--pass-run", land_run]), ExitCode.PENDING_HUMAN)
    assert _summary(by_land)["pass_run"] == pass_run
    assert _summary(by_land)["download_job"] == _summary(first)["download_job"]
    assert ("sync", "all") not in tail.verbs()
    assert len(script.fetched) == fetched, "a settled download was fetched again"
    checks = by_land["data"]["checks"]
    (resolved,) = [c for c in checks if c["key"] == "sync.land.preflight" and c["status"] == "info"]
    assert f"continuing the pass it recorded, run {pass_run}" in resolved["detail"]

    by_pass = exited(drive(["sync", "land", "--pass-run", pass_run]), ExitCode.PENDING_HUMAN)
    assert _summary(by_pass)["pass_run"] == pass_run
    assert _summary(by_pass)["download_job"] == _summary(first)["download_job"]
    assert len(_by_key("acquire.download")) == 1
    assert _record(by_land["run_id"])["related_runs"] == {"pass_run": pass_run}


def test_an_unknown_id_refuses_before_any_step_and_names_the_recent_passes(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    passed = exited(drive(["sync", "all"]))
    tail.calls.clear()
    jobs_before = [(job.job_id, job.state) for job in _all_jobs()]

    code, envelope = drive(["sync", "land", "--pass-run", "2026-10-30T00:00:00Z-beef"])

    assert envelope["cause"]["reason"] == "job-unknown", envelope
    assert tail.calls == [], "a step ran for an id that names no pass"
    assert script.fetched == []
    assert [(job.job_id, job.state) for job in _all_jobs()] == jobs_before
    assert passed["run_id"] in envelope["cause"]["message"]
    steps = envelope["cause"]["remediation"]["steps"]
    assert f"crate sync land --pass-run {passed['run_id']}" in steps[0]
    assert steps[-1].endswith("crate sync land")
    assert envelope["cause"]["detail"]["recent_passes"] == [passed["run_id"]]


def test_a_refused_id_names_the_land_run_recorded_beside_each_pass(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    first = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)

    code, envelope = drive(["sync", "land", "--pass-run", "../../etc/passwd"])

    assert envelope["cause"]["reason"] == "job-unknown", envelope
    pass_run = _summary(first)["pass_run"]
    assert envelope["cause"]["detail"]["land_runs"] == {pass_run: first["run_id"]}
    assert f"(crate sync land run {first['run_id']})" in envelope["cause"]["remediation"]["steps"][0]


@pytest.mark.parametrize(
    ("related", "said"),
    [(None, "recorded no pass"),
     ("2026-10-30T00:00:00Z-gone", "2026-10-30T00:00:00Z-gone, no intake job")],
    ids=["recorded-no-pass", "no-intake-job"],
)
def test_a_land_run_naming_no_pass_an_intake_job_carries_is_refused(machine, tail, related, said):
    """A land run that recorded no pass, or one a later step would refuse, is refused up front."""
    land_run = gates.new_run(ENTRY)
    if related is not None:
        land_run.related_runs["pass_run"] = related
    gates.save(land_run)
    recorded = None if related is None else {"pass_run": related}
    assert _record(land_run.run_id).get("related_runs") == recorded

    code, envelope = drive(["sync", "land", "--pass-run", land_run.run_id])

    assert envelope["cause"]["reason"] == "job-unknown", envelope
    assert said in envelope["cause"]["message"]
    assert tail.calls == []


def test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    first = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    (gates.run_dir() / "2026-01-01T00:00:02Z-dead.json").write_text("[]\n")
    misshapen = {**_record(first["run_id"]), "run_id": "2026-01-01T00:00:03Z-dead"}
    misshapen["pins"] = {"gate": [1]}
    (gates.run_dir() / "2026-01-01T00:00:03Z-dead.json").write_text(json.dumps(misshapen))

    for given in ("2026-01-01T00:00:02Z-dead", "2026-01-01T00:00:03Z-dead"):
        code, envelope = drive(["sync", "land", "--pass-run", given])

        assert envelope["cause"]["reason"] == "job-unknown", envelope
        lands = envelope["cause"]["detail"]["land_runs"]
        assert lands == {_summary(first)["pass_run"]: first["run_id"]}


def test_a_record_with_no_related_runs_is_the_record_it_was_and_one_with_them_round_trips():
    state = gates.new_run(ENTRY)
    assert "related_runs" not in state.to_json()
    state.related_runs["pass_run"] = "2026-10-30T00:00:00Z-beef"
    read = gates.RunState.from_json(json.loads(json.dumps(state.to_json())))
    assert read.related_runs == {"pass_run": "2026-10-30T00:00:00Z-beef"}
    assert read.to_json() == state.to_json()


def test_a_run_record_that_is_not_an_object_is_the_gates_own_refusal(machine):
    """Every reader catches the gates refusal; an AttributeError reached none of them."""
    gates.run_dir().mkdir(parents=True, exist_ok=True)
    gates.run_path("2026-01-01T00:00:02Z-dead").write_text("[]\n")

    with pytest.raises(CratekitError) as refused:
        gates.load("2026-01-01T00:00:02Z-dead")

    assert refused.value.cause.reason == "internal-error"
    assert "is not a JSON object" in refused.value.cause.message


def test_a_run_interrupted_after_sync_all_continues_by_its_own_id(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    real = sync_land._intake

    def interrupted(*_args, **_kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(sync_land, "_intake", interrupted)
    with pytest.raises(KeyboardInterrupt):
        drive(["sync", "land"])
    (land_run,) = _land_runs()
    pass_run = _record(land_run)["related_runs"]["pass_run"]
    (intake,) = _by_key("intake.playlist")
    assert intake.payload["run_id"] == pass_run
    assert intake.state is jobs.JobState.QUEUED
    monkeypatch.setattr(sync_land, "_intake", real)
    tail.calls.clear()

    envelope = exited(drive(["sync", "land", "--pass-run", land_run]), ExitCode.PENDING_HUMAN)
    assert ("sync", "all") not in tail.verbs()
    assert _summary(envelope)["pass_run"] == pass_run
    (intake,) = _by_key("intake.playlist")
    assert intake.state is jobs.JobState.SUCCEEDED


def _pasted(step: str) -> list[str]:
    """The command a way on ends with, as a person pastes it, without ``crate``."""
    command = step.rsplit(": ", 1)[1]
    words = shlex.split(command)
    assert words[0] == "crate", step
    return words[1:]


def test_the_continue_command_a_failed_step_prints_works_when_pasted(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101", "102")
    tail.work[sync_land.ANALYZE] = _broken
    failed = exited(drive(["sync", "land"]), ExitCode.MODULE_UNAVAILABLE)
    last = failed["cause"]["remediation"]["steps"][-1]
    assert last.endswith(f"crate sync land --pass-run {_summary(failed)['pass_run']}")
    del tail.work[sync_land.ANALYZE]
    tail.calls.clear()

    again = exited(drive(_pasted(last)), ExitCode.PENDING_HUMAN)
    assert ("sync", "all") not in tail.verbs()
    assert _summary(again)["pass_run"] == _summary(failed)["pass_run"]
    assert _summary(again)["stopped_at"] == sync_land.LAND_GATE


def test_the_continue_command_a_pending_stop_prints_works_when_pasted(machine, monkeypatch, tail):
    cfg, script = _ready(machine, monkeypatch, "101")
    gate = _refused(_gate("analyze-run", gate="analyze-confirm"), outcome="blocked")
    gated = _step_answers(monkeypatch, tail, sync_land.ANALYZE, gate)
    pending = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    last = pending["pending_human_action"]["steps"][-1]
    assert last.endswith(f"crate sync land --pass-run {_summary(pending)['pass_run']}")
    monkeypatch.setattr(tail, "_job", gated)

    again = exited(drive(_pasted(last)), ExitCode.PENDING_HUMAN)
    assert _summary(again)["pass_run"] == _summary(pending)["pass_run"]
    assert _summary(again)["stopped_at"] == sync_land.LAND_GATE


def test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    code, passed = drive(["sync", "all"])
    (intake,) = _by_key("intake.playlist")
    _failed_intake(intake.job_id, "the catalogue timed out", Remedy.RETRY_LATER, retryable=True)
    code, envelope = drive(["sync", "land", "--pass-run", passed["run_id"]])

    assert envelope["cause"]["reason"] == "adapter-broken", envelope
    steps = envelope["cause"]["remediation"]["steps"]
    assert f"crate job resume {intake.job_id}" in steps[-2]
    assert steps[-1].endswith(f"crate sync land --pass-run {passed['run_id']}")


def test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back(
    machine, monkeypatch, tail
):
    cfg, script = _ready(machine, monkeypatch, "101")
    first = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    tail.calls.clear()

    code, envelope = drive(["sync", "land", "--pass-run", first["run_id"]])

    assert code == int(ExitCode.REKORDBOX_OPEN), envelope
    assert tail.calls == []
    steps = envelope["cause"]["remediation"]["steps"]
    assert steps[-1].endswith(f"crate sync land --pass-run {_summary(first)['pass_run']}")
