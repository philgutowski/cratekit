"""U152: ``crate sync land`` takes a sync pass to its landing gate in one verb.

WHAT THIS FILE GUARDS. Sitting 47 ran ten commands by hand, each with an
identifier copied from the last, and planned a landing over files the tail had
never run on. The properties here are the ones that make the one verb real: it
runs the existing verbs in their one order, it drives every job it meets to a
settled state, it reads each job's answer off the queue, it skips a download
refused for good and stops on anything else, and it ends at the landing's own
gate naming what the session does next.

WHAT IS REAL AND WHAT STANDS IN. The pass, its intake jobs, the missing list and
the download run through the real dispatcher and the real workers, with the
catalogue and the acquisition adapter in front of their seams exactly as their
own suites put them. The tail and the landing need audio analysis, a rekordbox
collection and an adopted intake tree, none of which a fixture here can hold, so
those steps stand in through the verb's one seam, ``sync_land.dispatch``: each
stand in queues and drives a real job in the real queue, so the driver's every
read of a job is a read of the queue.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import pytest

from cratekit import acquire
from cratekit.acquire import cli as acquire_cli
from cratekit.cli import registry, sync_land
from cratekit.core import config, jobs, rb_writer
from cratekit.core.cause import Cause, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from tests.acquire_fakes import FAKE_ADAPTER, FAKE_DECLARATION, FakeAdapter, Landing, Script
from tests.cli_drive import drive
from tests.intake.test_workers import owned
from tests.test_config import valid_data
from tests.test_sync_all import (
    ShortHearts,
    _hearts,
    _playlist,
    _tracks,
    bind_hearts,
    bind_playlists,
)

ENTRY = registry.entry("sync.land")


# ═══════════════════════════════════════════════════════════════════════════
# The machine, the account and the stand ins
# ═══════════════════════════════════════════════════════════════════════════


def _machine(tmp_path, monkeypatch, profile: str) -> tuple[config.Config, Script]:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(
        valid_data(
            root,
            profile={"name": profile},
            acquisition={"adapter": FAKE_ADAPTER, "pacing_delay_s": 0.0},
        )
    )
    config.save(built)
    config.reset_cache()
    script = Script()
    monkeypatch.setitem(acquire.ADAPTERS, FAKE_ADAPTER, FAKE_DECLARATION)
    monkeypatch.setattr(FakeAdapter, "script", script)
    monkeypatch.setattr(acquire_cli, "_SLEEP", lambda _seconds: None)
    return built, script


@pytest.fixture
def machine(tmp_path, monkeypatch):
    """The slim profile, which composes the account playlists alone."""
    return _machine(tmp_path, monkeypatch, "slim")


def _account(monkeypatch, script: Script, *ids: str, lossy: tuple[str, ...] = ()) -> None:
    """One new account playlist holding ``ids``, each downloadable, ``lossy`` landing MP3."""
    for track_id in ids:
        script.landings[track_id] = Landing(kind="lossy" if track_id in lossy else "lossless")
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks(*ids)))


def _ok(data: dict[str, Any], outcome: str = "ok") -> tuple[int, dict[str, Any]]:
    return int(ExitCode.OK), {"outcome": outcome, "data": data, "warnings": []}


def _refused(cause: Cause, outcome: str = "failed") -> tuple[int, dict[str, Any]]:
    return int(cause.code), {"outcome": outcome, "cause": cause.to_json(), "warnings": []}


def _gate(run_id: str, gate: str = sync_land.LAND_GATE) -> Cause:
    return Cause(
        reason="decision-required",
        message=f"{gate} needs a recorded decision",
        remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
        retryable=True,
        origin=("test",),
        detail={"gate": gate, "options": ["apply", "abort"], "run_id": run_id},
    )


class Tail:
    """The tail and the landing, standing in, every other step real.

    Each queueing command enqueues a REAL job under its verb's own key over the
    folder it names, one item per file there, and each ``--job`` command drives
    that job through the engine with ``work`` deciding each item. The landing
    answers with ``landing``, its gate by default.
    """

    def __init__(self) -> None:
        self.real = sync_land.dispatch
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
        key = registry.entry(verb).handler_key
        if "--job" not in argv:
            folder = Path(argv[-1])
            files = tuple(sorted(p.name for p in folder.iterdir() if p.is_file()))
            if not files:
                return _ok({"job_id": None, "state": "no-tracks"}, outcome="no_op")
            with jobs.open_store() as store:
                job = jobs.enqueue(
                    store,
                    handler_key=key,
                    payload={"folder": str(folder)},
                    cfg=config.load(),
                    item_ids=files,
                )
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
    monkeypatch.setattr(sync_land, "dispatch", stand_in)
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


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declaration
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_queues_nothing_of_its_own_and_declares_no_gate():
    """Every job it drives is queued by its own verb; every gate is a step's own."""
    assert ENTRY.landed and not ENTRY.long_running and ENTRY.argv_builder is None
    assert ENTRY.gates == ()
    assert ENTRY.writes == frozenset({"files"}) and ENTRY.destructive
    assert ENTRY.module == "cratekit.cli.sync_land"


def test_the_tail_is_the_four_verbs_in_their_order():
    """Sitting 47's order, pinned: tag, analyse, restamp, then name."""
    assert [verb for _step, verb, _words in sync_land.TAIL] == [
        "tag.folder",
        "analyze.run",
        "analyze.restamp",
    ]
    for _step, verb, words in sync_land.TAIL:
        assert registry.entry(verb).path == words
    assert sync_land.STEPS.index(sync_land.NAME) > sync_land.STEPS.index(sync_land.RESTAMP)
    assert sync_land.STEPS.index(sync_land.LAND) == len(sync_land.STEPS) - 1


# ═══════════════════════════════════════════════════════════════════════════
# 2. The brief's four scenarios
# ═══════════════════════════════════════════════════════════════════════════


def test_a_pass_with_only_owned_tracks_ends_without_a_download_or_a_landing(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")
    for track_id in ("101", "102"):
        owned(cfg.library.root, f"Artist {track_id} - Title {track_id}.flac")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.OK), envelope
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

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    (download,) = _by_key("acquire.download")
    assert download.state is jobs.JobState.FAILED
    assert download.cause.reason == "lossy-refused"
    summary = _summary(envelope)
    assert [row["item_id"] for row in summary["download_refused"]] == ["107"]
    assert summary["download_refused"][0]["reason"] == "lossy-refused"
    assert "landed 7 track(s); 1 refused and skipped" in _check(envelope, "download")["detail"]
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "sync-land-download-refused"]
    assert "107" in warning["message"] and "lossy-refused" in warning["message"]
    staged = sorted(p.name for p in _staged(cfg).iterdir() if p.is_file())
    assert staged == sorted(f"{track_id}.wav" for track_id in ids[:7])
    # THE REFUSAL DID NOT END THE PASS: the tail ran and the landing was planned.
    assert ("intake", "land") in tail.verbs()
    assert summary["stopped_at"] == sync_land.LAND_GATE


def test_a_stale_queued_analyze_job_is_replaced_not_resumed(machine, monkeypatch, tail):
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")
    staging = _staged(cfg)
    staging.mkdir(parents=True, exist_ok=True)
    (staging / "old.wav").write_bytes(b"")
    with jobs.open_store() as store:
        stale = jobs.enqueue(
            store,
            handler_key=registry.entry("analyze.run").handler_key,
            payload={"folder": str(staging)},
            cfg=cfg,
            item_ids=("old.wav",),
        )

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    with jobs.open_store() as store:
        assert jobs.get(store, stale.job_id).state is jobs.JobState.CANCELLED
    assert {"step": "analyze", "job_id": stale.job_id} in _summary(envelope)["replaced"]
    assert not any(stale.job_id in argv for argv in tail.calls), "the stale job was resumed"
    fresh = [job for job in _by_key("analyze.run") if job.job_id != stale.job_id]
    assert len(fresh) == 1 and fresh[0].state is jobs.JobState.SUCCEEDED


def test_rekordbox_running_refuses_before_any_write(machine, monkeypatch, tail):
    cfg, script = machine
    _account(monkeypatch, script, "101")
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.REKORDBOX_OPEN), envelope
    assert envelope["cause"]["reason"] == "rekordbox-running"
    assert tail.calls == [], "a step ran while rekordbox was up"
    assert _all_jobs() == []


def test_a_running_backup_refuses_before_any_write(machine, monkeypatch, tail):
    cfg, script = machine
    _account(monkeypatch, script, "101")
    with jobs.open_store() as store:
        backup = jobs.enqueue(
            store,
            handler_key=registry.entry("backup.run").handler_key,
            payload={},
            cfg=cfg,
            item_ids=("mirror",),
        )

    with jobs.driver_lock(backup.job_id):
        code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    assert envelope["cause"]["reason"] == "job-driver-held"
    assert backup.job_id in envelope["cause"]["message"]
    assert tail.calls == []
    assert [job.job_id for job in _all_jobs()] == [backup.job_id]


def test_a_backup_job_whose_driver_died_does_not_hold_the_pass(machine, monkeypatch, tail):
    """The lock is the liveness test, so an open row with no live driver is not running."""
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")
    for track_id in ("101", "102"):
        owned(cfg.library.root, f"Artist {track_id} - Title {track_id}.flac")
    with jobs.open_store() as store:
        jobs.enqueue(
            store,
            handler_key=registry.entry("backup.run").handler_key,
            payload={},
            cfg=cfg,
            item_ids=("mirror",),
        )

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.OK), envelope
    assert _check(envelope, sync_land.PREFLIGHT)["status"] == "ok"


# ═══════════════════════════════════════════════════════════════════════════
# 3. The order, the tail and the stop
# ═══════════════════════════════════════════════════════════════════════════


def test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")
    monkeypatch.chdir(cfg.library.root)

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    queued = [words for words in tail.verbs() if words != ("intake", "playlist")]
    assert queued == [
        ("sync", "all"),
        ("intake", "missing"),
        ("acquire", "download"),
        ("acquire", "download"),
        ("tag", "folder"),
        ("tag", "folder"),
        ("analyze", "run"),
        ("analyze", "run"),
        ("analyze", "restamp"),
        ("analyze", "restamp"),
        ("name", "apply"),
        ("intake", "land"),
    ]
    staging = str(_staged(cfg))
    assert Path(staging).is_absolute()
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


def test_the_stop_at_the_landing_gate_names_the_session_commands_and_the_visit(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == "pending"
    pending = envelope["pending_human_action"]
    assert pending["kind"] == "external_step" and pending["verify_verb"] == "intake.land"
    steps = pending["steps"]
    assert steps[0].endswith(
        f"crate run decide land-run {sync_land.LAND_GATE} apply --actor session"
    )
    land = " ".join(tail.calls[-1])
    assert steps[1] == f"apply it: crate --run land-run {land}"
    assert any("Reload Tags" in step and "batch playlist" in step for step in steps)
    analyse = [step for step in steps if "Analyze Tracks" in step]
    assert analyse and "KEY on" in analyse[0] and "Normal" in analyse[0]
    assert steps.index([s for s in steps if "Reload Tags" in s][0]) < steps.index(analyse[0])
    assert envelope["cause"]["reason"] == "awaiting-human-action"
    assert _summary(envelope)["gate_run"] == "land-run"


def test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _account(monkeypatch, script, "101")
    tail.landing = lambda _argv: _refused(
        refuse(
            "backup-acknowledgment-missing",
            "no backup acknowledgment is recorded",
            remedy=Remedy.ACKNOWLEDGE_BACKUP,
            origin=("test",),
        ).cause
    )

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    pending = envelope["pending_human_action"]
    assert pending["kind"] == "backup_ack"
    land = " ".join(tail.calls[-1])
    assert f"then plan the landing again: crate {land}" in pending["steps"]
    assert _summary(envelope)["stopped_at"] == "backup-acknowledgment-missing"
    assert not (cfg.library.root / "ack").exists()


def test_a_failed_tail_step_plans_no_landing_and_names_the_continuation(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")

    def broken(_job, item):
        raise refuse(
            "module-extras-missing",
            f"the analysis extra is not importable for {item.item_id}",
            scope=Scope.ITEM,
            origin=("test",),
        )

    tail.work[sync_land.ANALYZE] = broken

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.MODULE_UNAVAILABLE), envelope
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
    cfg, script = machine
    _account(monkeypatch, script, "101")
    real = tail._job

    def emptied(step, verb, argv):
        if step == sync_land.TAG and "--job" not in argv:
            return _ok({"job_id": None, "state": "no-tracks"}, outcome="no_op")
        return real(step, verb, argv)

    monkeypatch.setattr(tail, "_job", emptied)

    code, envelope = drive(["sync", "land"])

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "source-missing"
    assert ("analyze", "run") not in tail.verbs()
    assert ("intake", "land") not in tail.verbs()


def test_a_parked_download_ends_the_pass_blocked_before_the_tail(machine, monkeypatch, tail):
    """A provider that refused the client is a block, never a refusal to skip."""
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")
    real = tail.real

    def parked(argv):
        if argv[:2] == ["acquire", "download"] and "--job" in argv:
            job_id = argv[argv.index("--job") + 1]
            with jobs.open_store() as store:
                jobs.block(
                    store,
                    job_id,
                    Cause(
                        reason="provider-blocked",
                        message="the provider refused the client",
                        remediation=Remediation(remedy=Remedy.RESUME_JOB),
                        retryable=True,
                        origin=("test",),
                    ),
                )
            return _refused(jobs.get(jobs.open_store(), job_id).cause, outcome="blocked")
        return real(argv)

    tail.real = parked

    code, envelope = drive(["sync", "land"])

    assert envelope["outcome"] == "blocked", envelope
    assert envelope["cause"]["reason"] == "provider-blocked"
    assert ("tag", "folder") not in tail.verbs()


# ═══════════════════════════════════════════════════════════════════════════
# 4. Continuing a pass
# ═══════════════════════════════════════════════════════════════════════════


def test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")
    code, first = drive(["sync", "land"])
    assert code == int(ExitCode.PENDING_HUMAN), first
    run_id = _summary(first)["pass_run"]
    fetched = len(script.fetched)
    tail.calls.clear()

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.PENDING_HUMAN), again
    assert ("sync", "all") not in tail.verbs()
    assert len(_by_key("acquire.download")) == 1
    assert len(script.fetched) == fetched, "a settled download was fetched again"
    assert _summary(again)["download_job"] == _summary(first)["download_job"]


def test_a_continued_pass_over_an_open_intake_job_drives_it_first(machine, monkeypatch, tail):
    cfg, script = machine
    _account(monkeypatch, script, "101")
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    run_id = passed["run_id"]
    (intake,) = _by_key("intake.playlist")
    assert intake.state is jobs.JobState.QUEUED

    code, envelope = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert tail.verbs()[0] == ("intake", "playlist")
    (intake,) = _by_key("intake.playlist")
    assert intake.state is jobs.JobState.SUCCEEDED


def test_a_continued_pass_naming_no_intake_job_is_the_listings_own_refusal(machine, tail):
    code, envelope = drive(["sync", "land", "--pass-run", "no-such-run"])

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "job-unknown"
    assert ("acquire", "download") not in tail.verbs()


# ═══════════════════════════════════════════════════════════════════════════
# 5. What the pass carries through
# ═══════════════════════════════════════════════════════════════════════════


def test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried(
    tmp_path, monkeypatch
):
    cfg, _script = _machine(tmp_path, monkeypatch, "full")
    fake = bind_hearts(monkeypatch, ShortHearts(_hearts("301", "302", "303"), declared=5))
    for track_id in ("301", "302", "303"):
        owned(cfg.library.root, f"Heart Artist {track_id} - Heart {track_id}.flac")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.OK), envelope
    failing = [c for c in envelope["data"]["checks"] if c["status"] == "fail"]
    assert len(failing) == 1 and "2 withheld by the provider" in failing[0]["detail"]
    assert fake.heart_listings == 1, "the shortfall was retried"


def test_the_outbound_hearts_write_stays_behind_its_own_gate(tmp_path, monkeypatch):
    """No export is handed to the pass, so the favourites write half queues nothing."""
    cfg, _script = _machine(tmp_path, monkeypatch, "full")
    bind_hearts(monkeypatch)
    for track_id in ("301", "302", "303"):
        owned(cfg.library.root, f"Heart Artist {track_id} - Heart {track_id}.flac")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.OK), envelope
    assert _by_key("sync.favorites") == []
    assert any(w["code"] == "sync-source-not-queued" for w in envelope["warnings"])
    checks = envelope["data"]["checks"]
    assert not [c for c in checks if c["key"] == "sync.favorites"], "the unasked write is a FAIL row"
    assert any(
        c["key"] == "sync.land.sync" and "outbound hearts write is not this verb's" in c["detail"]
        for c in checks
    )


def test_a_step_with_no_readable_envelope_is_a_defect_not_a_success(machine, monkeypatch):
    monkeypatch.setattr(sync_land, "dispatch", lambda argv: (int(ExitCode.OK), {}))

    code, envelope = drive(["sync", "land"])

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "internal-error"
    assert "sync all" in envelope["cause"]["message"]


def test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes(
    machine, monkeypatch, tail
):
    """A step's gate is answered on that step's own run, never on this verb's."""
    cfg, script = machine
    _account(monkeypatch, script, "101")
    real = tail._job

    def gated(step, verb, argv):
        if step == sync_land.RESTAMP and "--job" not in argv:
            return _refused(_gate("restamp-run", "write.cloudsync.unreadable"), outcome="blocked")
        return real(step, verb, argv)

    monkeypatch.setattr(tail, "_job", gated)

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
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

    cfg, script = machine
    _account(monkeypatch, script, "101")

    code, text = drive_human(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), text
    assert "sync.land.download" in text
    assert "--actor session" in text
    assert "Analyze Tracks" in text


def test_a_job_another_driver_holds_ends_the_pass_with_that_drivers_refusal(
    machine, monkeypatch, tail
):
    """A job still running elsewhere was never driven here, and the pass says whose it is."""
    cfg, script = machine
    _account(monkeypatch, script, "101")
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    (intake,) = _by_key("intake.playlist")

    with jobs.driver_lock(intake.job_id):
        code, envelope = drive(["sync", "land", "--pass-run", passed["run_id"]])

    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    assert envelope["cause"]["reason"] == "job-driver-held"
    assert intake.job_id in envelope["cause"]["message"]
    assert ("intake", "missing") not in tail.verbs()
