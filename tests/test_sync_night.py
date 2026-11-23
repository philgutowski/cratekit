"""U293: ``crate sync night`` runs the sync pass unattended, up to its landing gate.

WHAT THIS FILE GUARDS. The brief's limits, each a merge blocker if broken: the
night pass never approves a gate, never writes the database, never opens
rekordbox, never runs beside rekordbox, a live job or another pass, never
spends past its night's budget, and never stages over a pass by hand; and
whatever it meets, it stops and leaves one line saying so.

WHAT IS REAL AND WHAT STANDS IN. The pass driven to its gate is the real
``crate sync land`` through the real dispatcher, with the tail and the landing
standing in through ``cratekit.cli.tail.dispatch`` exactly as
``tests/test_sync_land.py`` stands them in. The rest stand in the whole of
``sync land`` at that one seam, so what the night does around the pass is
read without a pass.
"""

from __future__ import annotations

import ast
import fcntl
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from cratekit.cli import doctor, label_sync, registry, sync_night
from cratekit.cli import tail as tail_chain
from cratekit.core import config, jobs, night_budget, provider_gate, rb_writer, staging_lock
from cratekit.core.cause import Cause, Remediation, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from tests import test_sync_land as land
from tests._sync_builders import exited
from tests.cli_drive import drive
from tests.test_sync_land import Tail, _account, _model_cannot_score, _ok, _refused

#: The sync land suite's own machine and stand ins, bound here by name so
#: pytest finds them as this module's fixtures.
machine = land.machine
full = land.full
tail = land.tail
vocal_model = land.vocal_model

ENTRY = registry.entry("sync.night")
SOURCE = Path(sync_night.__file__)

#: 03:00 UTC on 2026-11-22 is a firing of the night of 2026-11-21 in any zone
#: within nine hours of UTC either side, the zones a test runner sits in.
NIGHT_AT = datetime(2026, 11, 22, 3, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def at_night(monkeypatch):
    monkeypatch.setattr(sync_night, "_clock", lambda: NIGHT_AT)


def _night() -> str:
    return night_budget.night_of(NIGHT_AT)


def _status() -> dict[str, Any]:
    record = sync_night.read_status()
    assert record is not None, "the night pass left no record"
    return record


class Pass:
    """``crate sync land`` standing in whole, at the night's one seam.

    Records every command the night ran, the night's line and hour as each
    command saw them, and answers with ``answer``.
    """

    def __init__(self, answer: tuple[int, dict[str, Any]] | None = None) -> None:
        self.calls: list[list[str]] = []
        self.lines: list[provider_gate.Night | None] = []
        self.hours: list[int] = []
        self.env: list[str | None] = []
        self.answer = answer or _ok({"checks": [], "summary": {"stopped_at": "sync"}}, "no_op")

    def __call__(self, argv: list[str]) -> tuple[int, dict[str, Any]]:
        self.calls.append(list(argv))
        scope = provider_gate._COMMAND
        self.lines.append(scope.night if scope is not None else None)
        self.hours.append(provider_gate.hourly(provider_gate.GateSettings()))
        self.env.append(os.environ.get(provider_gate.NIGHT_ENV))
        return self.answer


@pytest.fixture
def one_pass(monkeypatch) -> Pass:
    stand_in = Pass()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    return stand_in


@pytest.fixture
def plain(tmp_path, monkeypatch) -> config.Config:
    """A configured library, for the tests that stand ``sync land`` in whole."""
    from tests.test_config import valid_data

    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(valid_data(root, profile={"name": "slim"}))
    config.save(built)
    config.reset_cache()
    return built


def _staging(cfg: config.Config) -> Path:
    return cfg.paths.download_staging.expanduser().absolute()


def _gate_total(calls: int) -> None:
    """The provider gate's running total set to ``calls``, as other processes leave it."""
    path = config.state_path(provider_gate.STATE_KEY)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        data = {}
    data["calls"] = calls
    path.write_text(json.dumps(data))


def _write_status(**fields: Any) -> None:
    record = {
        "schema": sync_night.STATUS_SCHEMA,
        "night": "2026-11-20",
        "line": "an earlier night's line",
        "outcome": sync_night.NOTHING,
        **fields,
    }
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record))


class _Foreign:
    """The staging lock held on a descriptor of its own, as another process holds it."""

    def __init__(self, verb: str = "crate sync land", run_id: str = "manual-run") -> None:
        path = staging_lock.lock_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = open(path, "a+")  # noqa: SIM115 - held across the test
        fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.handle.seek(0)
        self.handle.truncate()
        json.dump({"pid": 424242, "verb": verb, "run_id": run_id, "started": "then"}, self.handle)
        self.handle.flush()

    def release(self) -> None:
        self.handle.close()


@pytest.fixture
def foreign():
    held: list[_Foreign] = []

    def hold(**kwargs: Any) -> _Foreign:
        lock = _Foreign(**kwargs)
        held.append(lock)
        return lock

    yield hold
    for lock in held:
        lock.release()


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declaration
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_declares_no_gate_and_writes_only_files():
    """No gate of its own to answer, no database surface, and never a job of its own."""
    assert ENTRY.gates == ()
    assert ENTRY.writes == frozenset({"files"}) and ENTRY.destructive
    assert not ENTRY.long_running and ENTRY.argv_builder is None
    assert ENTRY.module == "cratekit.cli.sync_night"
    assert "rekordbox.closed" in ENTRY.doctor_checks


def _imports(source: Path) -> set[str]:
    tree = ast.parse(source.read_text())
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
            found.update(f"{node.module}.{alias.name}" for alias in node.names)
    return found


def test_the_night_module_reaches_no_launcher_no_decide_and_no_acknowledgment():
    """Read off the module's own imports and words, so a later edit that reaches
    any of them fails here by name. The library session is banned with its
    parts (R-1890), since ``cratekit.core.session_holders`` takes the same lock
    and does not match ``cratekit.core.session`` followed by a dot."""
    from tests._split_modules import names_of

    imported = _imports(SOURCE)
    for banned in ("subprocess", "os.system", *names_of("cratekit.core.session"),
                   "cratekit.session", "cratekit.session.cli", "cratekit.cli.verbs.runs",
                   "cratekit.cli.prompt"):
        assert not any(name == banned or name.startswith(banned + ".") for name in imported), banned
    text = SOURCE.read_text()
    for word in ("Popen", "os.system", "execv", "record_acknowledgment", "launchctl",
                 '"decide"', '"-d"', "--decision", "--actor"):
        assert word not in text, word
    # THE ONE COMMAND IT RUNS is the pass, and its one optional argument.
    assert sync_night.LAND_ARGV == ("sync", "land")


# ═══════════════════════════════════════════════════════════════════════════
# 2. The pass, driven to its gate
# ═══════════════════════════════════════════════════════════════════════════


def test_a_night_pass_reaches_the_landing_gate_and_answers_nothing_but_the_name_confirm(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")

    envelope = exited(drive(["sync", "night"]), ExitCode.PENDING_HUMAN)
    assert envelope["outcome"] == "pending"
    record = _status()
    assert record["outcome"] == sync_night.WAITING_GATE
    assert record["gate"] == tail_chain.LAND_GATE
    assert record["gate_run"] == "land-run"
    assert record["staging"] == str(_staging(cfg))
    assert record["land_name"] and record["pass_run"]
    assert record["night"] == _night()
    assert "waits at the landing gate under run land-run" in record["line"]
    assert envelope["data"]["summary"]["night"] == record
    # EVERY ANSWER IN THE CHAIN, read off the commands it ran: the tail's
    # name confirm, and nothing else.
    answered = [argv for argv in tail.calls if "-d" in argv or "--decision" in argv]
    assert answered and all(
        argv[:2] == ["-d", f"{tail_chain.NAME_GATE}={tail_chain.NAME_OPTION}"] for argv in answered
    ), answered
    words = [" ".join(argv) for argv in tail.calls]
    assert not any("run decide" in w or "session ack" in w or "--actor" in w for w in words)
    # THE LANDING WAS PLANNED AND LEFT AT ITS GATE, never applied.
    assert [argv for argv in tail.calls if argv[:2] == ["intake", "land"]]
    assert not any("--run" in argv for argv in tail.calls if argv[:2] == ["intake", "land"])
    # THE NIGHT WAS CHARGED, before and after.
    ledger = night_budget.read()
    assert ledger.night == _night() and ledger.open_start is None
    assert record["budget"] == cfg.provider.night_calls


def test_a_night_pass_that_needs_the_acknowledgment_stops_there_and_mints_none(
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

    exited(drive(["sync", "night"]), ExitCode.PENDING_HUMAN)
    record = _status()
    assert record["outcome"] == sync_night.WAITING_ACK
    assert "crate session ack --as session" in record["line"]
    assert f"crate sync land --pass-run {record['pass_run']}" in record["next"]
    assert not (cfg.library.root / "ack").exists()
    from cratekit.core import session

    assert session.read_acknowledgment(cfg) is None, "the night minted an acknowledgment"


def test_a_night_pass_the_vocal_model_cannot_score_waits_at_that_gate_and_queues_nothing(
    full, monkeypatch, tail
):
    cfg, script = full
    _account(monkeypatch, script, "101")
    _model_cannot_score(monkeypatch)

    code, envelope = drive(["sync", "night"])

    record = _status()
    assert record["outcome"] == sync_night.WAITING, (code, envelope)
    assert record["gate"] == "sync.land.without-vocals"
    assert code == int(ExitCode.PENDING_HUMAN)
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == (), "the pass queued work behind an unanswered gate"


# ═══════════════════════════════════════════════════════════════════════════
# 3. The refusals before any call
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "argv",
    [
        ["-d", "intake.land.native=apply", "sync", "night"],
        ["-d", "sync.land.without-vocals=go", "sync", "night"],
        ["--calls", "50", "sync", "night"],
        ["--calls-per-hour", "5000", "sync", "night"],
    ],
)
def test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything(
    plain, one_pass, argv
):
    envelope = exited(drive(argv), ExitCode.REFUSED_BY_POLICY)
    cause = envelope["cause"]
    assert cause["reason"] == "refused-by-policy"
    assert cause["detail"][sync_night.REFUSAL_KEY] == sync_night.NO_ANSWER
    assert one_pass.calls == []
    assert _status()["outcome"] == sync_night.REFUSED


@pytest.mark.parametrize("running", [("rekordbox",), ("rekordboxAgent",)])
def test_rekordbox_or_its_agent_up_refuses_before_any_call(plain, one_pass, monkeypatch, running):
    monkeypatch.setattr(rb_writer, "rekordbox_processes_running", lambda: running)

    envelope = exited(drive(["sync", "night"]), ExitCode.REKORDBOX_OPEN)
    assert envelope["cause"]["reason"] == "rekordbox-running"
    assert running[0] in envelope["cause"]["message"]
    assert one_pass.calls == []
    assert not night_budget.ledger_path().exists(), "the night was charged over a refusal"
    assert _status()["reason"] == "rekordbox-running"


def test_a_job_with_a_live_driver_refuses_before_any_call(plain, one_pass):
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=registry.entry("tag.folder").handler_key,
            payload={"folder": "x"},
            cfg=plain,
            item_ids=("a",),
        )

    with jobs.driver_lock(job.job_id):
        code, envelope = drive(["sync", "night"])

    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    assert envelope["cause"]["reason"] == "job-driver-held"
    assert job.job_id in envelope["cause"]["message"]
    assert one_pass.calls == []


def test_a_job_whose_driver_died_does_not_hold_the_night(plain, one_pass):
    with jobs.open_store() as store:
        jobs.enqueue(
            store,
            handler_key=registry.entry("tag.folder").handler_key,
            payload={"folder": "x"},
            cfg=plain,
            item_ids=("a",),
        )

    exited(drive(["sync", "night"]))
    assert one_pass.calls == [["sync", "land"]]


def test_another_pass_holding_the_staging_lock_refuses_the_night_naming_it(
    plain, one_pass, foreign
):
    foreign(verb="crate label sync --go", run_id="go-run")

    envelope = exited(drive(["sync", "night"]), ExitCode.LIBRARY_BUSY)
    cause = envelope["cause"]
    assert cause["reason"] == staging_lock.HELD
    assert "crate label sync --go" in cause["message"] and "go-run" in cause["message"]
    assert one_pass.calls == []
    assert _status()["outcome"] == sync_night.REFUSED
    assert "another pass is staging" in _status()["line"]


def test_a_staging_folder_holding_what_a_landing_takes_refuses_a_new_pass(plain, one_pass):
    staging = _staging(plain)
    staging.mkdir(parents=True, exist_ok=True)
    (staging / "Waiting - Track.flac").write_bytes(b"x")
    _write_status(
        outcome=sync_night.WAITING_GATE, night="2026-11-20",
        line="night of 2026-11-20: waiting at the landing gate under run G",
    )

    envelope = exited(drive(["sync", "night"]), ExitCode.REFUSED_BY_POLICY)
    cause = envelope["cause"]
    assert cause["detail"][sync_night.REFUSAL_KEY] == sync_night.OCCUPIED
    assert cause["detail"]["files"] == ["Waiting - Track.flac"]
    steps = cause["remediation"]["steps"]
    assert any("night pass of 2026-11-20 waits" in step for step in steps), steps
    assert one_pass.calls == []
    assert not night_budget.ledger_path().exists()


def test_a_staging_folder_with_nothing_a_landing_takes_lets_the_night_run(plain, one_pass):
    staging = _staging(plain)
    staging.mkdir(parents=True, exist_ok=True)
    (staging / ".DS_Store").write_bytes(b"x")

    exited(drive(["sync", "night"]))
    assert one_pass.calls == [["sync", "land"]]


# ═══════════════════════════════════════════════════════════════════════════
# 4. The night's budget around the pass
# ═══════════════════════════════════════════════════════════════════════════


def test_the_pass_runs_under_the_nights_line_and_hour(plain, one_pass):
    _gate_total(40)

    drive(["sync", "night"])

    (line,) = one_pass.lines
    assert line is not None
    # THE LOWER OF THE NIGHT'S BUDGET AND ONE COMMAND'S CEILING (review round one).
    assert line.start == 40
    assert line.budget == min(plain.provider.night_calls, plain.provider.calls_per_command)
    assert line.night == _night()
    assert one_pass.hours == [min(plain.provider.night_calls_per_hour, plain.provider.calls_per_hour)]
    assert one_pass.env == [line.to_env()]
    assert os.environ.get(provider_gate.NIGHT_ENV) is None, "the line outlived the pass"


def test_a_night_already_spent_refuses_before_any_call(plain, one_pass):
    _gate_total(0)
    night_budget._write(
        night_budget.Ledger(night=_night(), spent=plain.provider.night_calls),
        night_budget.ledger_path(),
    )

    envelope = exited(drive(["sync", "night"]), ExitCode.REFUSED_BY_POLICY)
    assert envelope["cause"]["reason"] == provider_gate.NIGHT
    assert str(plain.provider.night_calls) in envelope["cause"]["message"]
    assert one_pass.calls == []
    assert "the night's provider budget" in _status()["line"]


def test_a_firing_that_died_is_charged_to_the_next_of_the_same_night(plain, one_pass):
    _gate_total(500)
    night_budget._write(
        night_budget.Ledger(night=_night(), spent=100, open_start=300),
        night_budget.ledger_path(),
    )

    drive(["sync", "night"])

    (line,) = one_pass.lines
    # 100 finished, and 200 the dead firing moved the total by since its mark.
    assert line.budget == min(plain.provider.night_calls - 300, plain.provider.calls_per_command)
    assert night_budget.read().spent >= 300
    assert line.start == 500


def test_what_the_pass_spent_is_added_to_the_night(plain, monkeypatch):
    _gate_total(10)

    def spending(argv):
        _gate_total(10 + 37)
        return _ok({"checks": [], "summary": {"stopped_at": "sync"}}, "no_op")

    monkeypatch.setattr(tail_chain, "dispatch", spending)

    drive(["sync", "night"])

    ledger = night_budget.read()
    assert ledger.spent == 37 and ledger.open_start is None
    record = _status()
    assert record["calls"] == 37 and record["spent_tonight"] == 37
    assert "37 provider call(s), 37 of the night's" in record["line"]


# ═══════════════════════════════════════════════════════════════════════════
# 5. How the pass ended, and the next firing
# ═══════════════════════════════════════════════════════════════════════════


def _stopped_by(reason: str, pass_run: str = "pass-1") -> tuple[int, dict[str, Any]]:
    cause = Cause(
        reason=reason,
        message=f"stopped by {reason}",
        remediation=Remediation(remedy=Remedy.RETRY_LATER, steps=("wait",)),
        origin=("test",),
        detail={"sync_land": {"checks": [], "summary": {"pass_run": pass_run}}},
    )
    return _refused(cause)


def test_a_pass_the_nights_budget_stopped_is_continued_by_the_next_firing(plain, monkeypatch):
    first = Pass(_stopped_by(provider_gate.NIGHT))
    monkeypatch.setattr(tail_chain, "dispatch", first)

    exited(drive(["sync", "night"]), ExitCode.REFUSED_BY_POLICY)
    record = _status()
    assert record["outcome"] == sync_night.STOPPED
    assert record["continue_pass"] == "pass-1"
    assert "the next firing continues pass pass-1" in record["line"]
    # ITS OWN FILES ARE STAGED, which a new pass would refuse beside; the
    # continue does not ask the folder, and sync land's own reading guards it.
    staging = _staging(plain)
    staging.mkdir(parents=True, exist_ok=True)
    (staging / "101.wav").write_bytes(b"x")
    second = Pass()
    monkeypatch.setattr(tail_chain, "dispatch", second)

    exited(drive(["sync", "night"]))
    assert second.calls == [["sync", "land", "--pass-run", "pass-1"]]


@pytest.mark.parametrize("reason", ["unavailable-transient", "intake-list-unusable"])
def test_a_pass_stopped_for_any_other_reason_is_not_continued(plain, monkeypatch, reason):
    monkeypatch.setattr(tail_chain, "dispatch", Pass(_stopped_by(reason)))

    drive(["sync", "night"])

    record = _status()
    assert record["outcome"] == sync_night.STOPPED and record["continue_pass"] is None
    second = Pass()
    monkeypatch.setattr(tail_chain, "dispatch", second)
    drive(["sync", "night"])
    assert second.calls == [["sync", "land"]]


def test_a_pass_with_nothing_new_says_so(plain, one_pass):
    code, envelope = drive(["sync", "night"])

    assert code == int(ExitCode.OK) and envelope["outcome"] == "no_op", envelope
    record = _status()
    assert record["outcome"] == sync_night.NOTHING
    assert "nothing new to land" in record["line"]


def test_a_record_that_cannot_be_read_continues_nothing(plain, monkeypatch):
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json")
    stand_in = Pass()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)

    drive(["sync", "night"])

    assert stand_in.calls == [["sync", "land"]]


# ═══════════════════════════════════════════════════════════════════════════
# 6. The line: --last and doctor
# ═══════════════════════════════════════════════════════════════════════════


def test_last_prints_the_record_and_runs_nothing(plain, one_pass):
    _write_status(outcome=sync_night.WAITING_GATE, gate_run="G", land_name="P", staging="/s")

    envelope = exited(drive(["sync", "night", "--last"]))
    night = envelope["data"]["summary"]["night"]
    assert night["gate_run"] == "G" and night["land_name"] == "P"
    assert one_pass.calls == []
    assert not night_budget.ledger_path().exists()


def test_last_with_no_night_says_so(plain, one_pass):
    envelope = exited(drive(["sync", "night", "--last"]))
    assert envelope["data"]["summary"]["night"] is None
    assert "no night pass has run" in envelope["data"]["checks"][0]["detail"]


def _doctor_row(cfg) -> doctor.Finding:
    (check,) = [c for c in doctor.CHECKS if c.key == doctor.NIGHT_CHECK]
    return check.run(SimpleNamespace(cfg=cfg))


def test_doctor_shows_the_last_line_as_a_note(plain):
    _write_status(line="night of 2026-11-20: nothing new to land", ended="2026-11-21T03:10:00+00:00")

    row = _doctor_row(plain)

    assert row.status is doctor.Status.INFO
    assert row.detail.startswith("night of 2026-11-20: nothing new to land")


def test_doctor_with_no_night_and_with_a_record_it_cannot_read(plain):
    assert "no night pass has run" in _doctor_row(plain).detail
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[]")
    row = _doctor_row(plain)
    assert row.status is doctor.Status.INFO
    assert "could not be read" in row.detail


def test_doctor_runs_the_night_check_beside_the_hours_budget():
    keys = list(doctor.CHECK_KEYS)
    assert keys.index(doctor.NIGHT_CHECK) == keys.index(doctor.BUDGET_CHECK) + 1


# ═══════════════════════════════════════════════════════════════════════════
# 7. The staging lock on a pass by hand and a label go
# ═══════════════════════════════════════════════════════════════════════════


def test_a_pass_by_hand_refuses_while_the_night_holds_the_lock(machine, monkeypatch, tail, foreign):
    cfg, script = machine
    _account(monkeypatch, script, "101")
    foreign(verb="crate sync night", run_id="night-run")

    envelope = exited(drive(["sync", "land"]), ExitCode.LIBRARY_BUSY)
    assert envelope["cause"]["reason"] == staging_lock.HELD
    assert "crate sync night" in envelope["cause"]["message"]
    assert tail.calls == []
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def _go_ctx(go: bool) -> SimpleNamespace:
    return SimpleNamespace(args=SimpleNamespace(go=go), run=SimpleNamespace(run_id="go-run"))


def test_a_label_go_refuses_while_another_pass_holds_the_lock(monkeypatch, foreign):
    ran: list[bool] = []
    monkeypatch.setattr(label_sync, "_label_sync", lambda ctx: ran.append(True))
    foreign(verb="crate sync night", run_id="night-run")

    with pytest.raises(Exception) as caught:
        label_sync.label_sync(_go_ctx(True))

    assert caught.value.cause.reason == staging_lock.HELD
    assert ran == []


def test_a_label_go_holds_the_lock_and_a_walk_does_not(monkeypatch):
    seen: list[bool] = []
    monkeypatch.setattr(
        label_sync, "_label_sync", lambda ctx: seen.append(staging_lock._HANDLE is not None)
    )

    label_sync.label_sync(_go_ctx(True))
    label_sync.label_sync(_go_ctx(False))

    assert seen == [True, False]
    assert staging_lock._HANDLE is None


def test_the_night_holds_the_lock_for_the_whole_of_its_pass(plain, monkeypatch):
    seen: list[dict[str, Any] | None] = []

    def during(argv):
        seen.append(dict(staging_lock._HOLDER or {}))
        return _ok({"checks": [], "summary": {"stopped_at": "sync"}}, "no_op")

    monkeypatch.setattr(tail_chain, "dispatch", during)

    drive(["sync", "night"])

    (holder,) = seen
    assert holder["verb"] == "crate sync night" and holder["pid"] == os.getpid()
    assert staging_lock._HANDLE is None, "the lock outlived the night"


def test_a_refused_night_writes_its_record_even_when_its_line_cannot_be_kept(
    plain, one_pass, monkeypatch
):
    monkeypatch.setattr(rb_writer, "rekordbox_processes_running", lambda: ("rekordbox",))
    monkeypatch.setattr(sync_night, "_write_status", lambda record: "no room")

    code, envelope = drive(["sync", "night"])

    assert envelope["cause"]["detail"]["status_unwritten"] == "no room"
    assert envelope["cause"]["detail"]["sync_night"]["outcome"] == sync_night.REFUSED


def test_the_night_never_reaches_tail_names_it_does_not_own():
    """Every name the night module reads off the chain is the chain's own."""
    for name in ("LAND_GATE", "ACK_STOP", "NAME_GATE", "NAME_OPTION", "dispatch", "load_config"):
        assert hasattr(tail_chain, name), name
    assert Tail  # the stand in this file shares with the sync land suite


# ═══════════════════════════════════════════════════════════════════════════
# 8. Review round one: the record is what is owed, not the last snapshot
# ═══════════════════════════════════════════════════════════════════════════


def test_a_refused_firing_keeps_the_pass_waiting_at_its_gate(machine, monkeypatch, tail):
    """Finding 1: the firing after a waiting pass refuses on the occupied folder,
    and once erased every field the landing needs."""
    cfg, script = machine
    _account(monkeypatch, script, "101", "102")
    drive(["sync", "night"])
    waiting = _status()
    assert waiting["outcome"] == sync_night.WAITING_GATE

    exited(drive(["sync", "night"]), ExitCode.REFUSED_BY_POLICY)
    exited(drive(["-d", "x=y", "sync", "night"]), ExitCode.REFUSED_BY_POLICY)

    kept = _status()
    for name in ("outcome", "gate_run", "pass_run", "staging", "land_name", "gate"):
        assert kept[name] == waiting[name], name
    assert kept["firing"]["outcome"] == sync_night.REFUSED
    assert kept["firing"]["reason"] == "refused-by-policy"
    assert kept["pass_line"] == waiting["line"]
    assert kept["line"].endswith(f"still owed: {waiting['line']}")
    code, envelope = drive(["sync", "night", "--last"])
    assert envelope["data"]["summary"]["night"]["gate_run"] == "land-run"
    assert envelope["data"]["summary"]["night"]["outcome"] == sync_night.WAITING_GATE


def test_a_refused_firing_keeps_the_pass_the_next_night_continues(plain, monkeypatch):
    """Finding 2: a budget stop, a refusal the same night, then the next night."""
    monkeypatch.setattr(tail_chain, "dispatch", Pass(_stopped_by(provider_gate.NIGHT)))
    drive(["sync", "night"])
    staging = _staging(plain)
    staging.mkdir(parents=True, exist_ok=True)
    (staging / "101.wav").write_bytes(b"x")
    monkeypatch.setattr(rb_writer, "rekordbox_processes_running", lambda: ("rekordbox",))
    drive(["sync", "night"])
    monkeypatch.setattr(rb_writer, "rekordbox_processes_running", lambda: ())
    night_budget._write(
        night_budget.Ledger(night=_night(), spent=plain.provider.night_calls),
        night_budget.ledger_path(),
    )
    drive(["sync", "night"])
    assert _status()["continue_pass"] == "pass-1"

    later = datetime(2026, 11, 23, 3, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(sync_night, "_clock", lambda: later)
    nxt = Pass()
    monkeypatch.setattr(tail_chain, "dispatch", nxt)
    exited(drive(["sync", "night"]))
    assert nxt.calls == [["sync", "land", "--pass-run", "pass-1"]]


def _run_with_gate(run_id: str, *, open_: bool) -> None:
    from cratekit.cli import gates

    state = gates.RunState(run_id=run_id, verb="intake.land", created="then")
    state.open_gate = tail_chain.LAND_GATE if open_ else None
    gates.save(state)


def _landed_passes(monkeypatch, *names: str) -> None:
    from cratekit.intake import native

    monkeypatch.setattr(
        native, "landings_of_pass", lambda cfg, name: ("session-1",) if name in names else ()
    )


def _waiting_at(staging: Path, gate_run: str = "2026-11-22T030000Z-land") -> None:
    _write_status(
        outcome=sync_night.WAITING_GATE, gate_run=gate_run, staging=str(staging),
        land_name="P", pass_run="R", next="land it",
        line=f"night of 2026-11-21: waits at the landing gate under run {gate_run}",
    )


def test_an_answered_gate_over_tracks_still_staged_stays_owed(plain, one_pass, monkeypatch):
    """Round two, finding 1: an apply refused beside rekordbox, or an abort,
    answers the gate and leaves every track staged."""
    staging = _staging(plain)
    staging.mkdir(parents=True, exist_ok=True)
    (staging / "101.wav").write_bytes(b"x")
    _waiting_at(staging)
    _landed_passes(monkeypatch)
    _run_with_gate("2026-11-22T030000Z-land", open_=False)

    view = sync_night.settle(sync_night.read_status(), plain)

    assert view["outcome"] == sync_night.WAITING_GATE
    assert "has been answered and no landing of pass P is recorded" in view["line"]
    drive(["sync", "night"])
    kept = _status()
    assert kept["outcome"] == sync_night.WAITING_GATE and kept["gate_run"]
    assert "still owed" in kept["line"]


def test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since(
    plain, one_pass, monkeypatch
):
    """Round one, finding 3, and round two, finding 2: the landing's own proof
    ends the wait, and another pass's tracks staged later do not revive it."""
    staging = _staging(plain)
    staging.mkdir(parents=True, exist_ok=True)
    _waiting_at(staging)
    _landed_passes(monkeypatch, "P")
    (staging / "103.wav").write_bytes(b"x")  # another pass's, staged since

    settled = sync_night.settle(sync_night.read_status(), plain)
    assert settled["outcome"] == sync_night.SETTLED and settled["was"] == sync_night.WAITING_GATE
    assert "since then pass P has landed" in settled["line"]
    assert settled["next"] is None
    code, envelope = drive(["sync", "night", "--last"])
    assert envelope["data"]["summary"]["night"]["outcome"] == sync_night.SETTLED
    assert "nothing waits" in _doctor_row(plain).detail
    # THE NEXT FIRING READS IT SETTLED TOO, so its refusal beside 103.wav is a
    # fresh record and keeps no pass that has landed.
    exited(drive(["sync", "night"]), ExitCode.REFUSED_BY_POLICY)
    fresh = _status()
    assert fresh["outcome"] == sync_night.REFUSED and fresh["gate_run"] is None


def test_an_emptied_staging_folder_alone_never_settles_a_wait(plain, one_pass, monkeypatch):
    staging = _staging(plain)
    staging.mkdir(parents=True, exist_ok=True)
    _waiting_at(staging)
    _landed_passes(monkeypatch)

    assert sync_night.settle(sync_night.read_status(), plain)["outcome"] == sync_night.WAITING_GATE
    # AND THE NIGHT STILL RUNS over an empty folder.
    exited(drive(["sync", "night"]))
    assert one_pass.calls == [["sync", "land"]]


def test_a_landing_that_cannot_be_read_settles_nothing(plain, monkeypatch):
    from cratekit.intake import native

    def unreadable(cfg, name):
        raise refuse("refused-by-policy", "the log cannot be listed", origin=("test",))

    _waiting_at(_staging(plain))
    monkeypatch.setattr(native, "landings_of_pass", unreadable)

    assert sync_night.settle(sync_night.read_status(), plain)["outcome"] == sync_night.WAITING_GATE


def test_a_wait_whose_gate_and_folder_cannot_be_read_stays_as_written(plain):
    _write_status(outcome=sync_night.WAITING_GATE, gate_run="no-such-run", staging=None,
                  line="waits")
    assert sync_night.settle(sync_night.read_status())["outcome"] == sync_night.WAITING_GATE


@pytest.mark.parametrize("reason", sorted(sync_night.CONTINUES))
def test_every_stop_waiting_mends_is_continued(plain, monkeypatch, reason):
    """Review round one's zero row: each reason in the set, not only the night's."""
    monkeypatch.setattr(tail_chain, "dispatch", Pass(_stopped_by(reason)))
    drive(["sync", "night"])
    assert _status()["continue_pass"] == "pass-1"


def test_a_track_the_download_refused_is_named_in_the_record(machine, monkeypatch, tail):
    """Finding 7: a pass that waits at its gate is landed without its own run."""
    cfg, script = machine
    _account(monkeypatch, script, "101", "107", lossy=("107",))

    drive(["sync", "night"])

    record = _status()
    assert record["download_refused"] == [{"item_id": "107", "reason": "lossy-refused"}]
    assert "107 (lossy-refused)" in record["line"]
    code, envelope = drive(["sync", "night", "--last"])
    rows = {row["key"]: row["detail"] for row in envelope["data"]["checks"]}
    assert rows["sync.night.download_refused"] == "107 (lossy-refused)"
    assert rows["sync.night.gate_run"] == "land-run"


def test_a_gate_unreadable_at_the_close_is_said_not_read_as_nothing(plain, monkeypatch):
    _gate_total(5)

    def breaking(argv):
        config.state_path(provider_gate.STATE_KEY).write_text("{")
        return _ok({"checks": [], "summary": {"stopped_at": "sync"}}, "no_op")

    monkeypatch.setattr(tail_chain, "dispatch", breaking)

    drive(["sync", "night"])

    record = _status()
    assert record["calls"] is None and record["spent_tonight"] is None
    assert "provider calls not read at the close" in record["line"]
