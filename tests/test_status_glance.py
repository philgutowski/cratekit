"""U960: ``crate status`` carries one machine readable glance an app can show.

Each test guards a way the glance could be green and wrong: a source it could
not read shown as empty, none or closed; a word that disagrees with the verbs
whose facts it projects; a shape the app was not built for; a read that writes.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest

from cratekit import cli
from cratekit.cli import gates, output, registry, render, status_glance, sync_night
from cratekit.core import backup_facts, config, jobs, processes
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import Remedy
from tests.test_doctor import document_for, fresh_root
from tests.test_session_log_unlisted import _refuse_listing

SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "status_glance.v1.json"
SCHEMA: dict[str, Any] = json.loads(SCHEMA_PATH.read_text())

NOW = datetime(2026, 11, 25, 12, 0, tzinfo=timezone.utc)
DAY = timedelta(days=1)


# ═══ A small validator for the subset of JSON Schema the file uses ═══════════


_TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool, "null": type(None),
}


def _type_holds(value: Any, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    return isinstance(value, _TYPES[name])


def problems(value: Any, schema: dict[str, Any] | None = None, where: str = "glance") -> list[str]:
    """Every way ``value`` breaks ``schema``; empty when it conforms."""
    schema = SCHEMA if schema is None else schema
    if "$ref" in schema:
        name = schema["$ref"].removeprefix("#/$defs/")
        return problems(value, SCHEMA["$defs"][name], where)
    if "anyOf" in schema:
        found = [problems(value, one, where) for one in schema["anyOf"]]
        if any(not one for one in found):
            return []
        return [f"{where}: matches none of {len(found)} shapes ({found})"]
    out: list[str] = []
    if "enum" in schema and value not in schema["enum"]:
        out.append(f"{where}: {value!r} is not one of {schema['enum']}")
    if "type" in schema:
        names = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_holds(value, name) for name in names):
            return out + [f"{where}: {type(value).__name__} is not {names}"]
    if isinstance(value, dict):
        for key in schema.get("required", ()):
            if key not in value:
                out.append(f"{where}: missing {key!r}")
        declared = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            out += [f"{where}: undeclared {key!r}" for key in value if key not in declared]
        for key, sub in declared.items():
            if key in value:
                out += problems(value[key], sub, f"{where}.{key}")
    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            out += problems(item, schema["items"], f"{where}[{index}]")
    return out


# ═══ Fixtures ═══════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    root = fresh_root(tmp_path, monkeypatch, "library")
    built = config.from_dict(document_for(root))
    config.save(built)
    config.reset_cache()
    return config.load()


def drive(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def backed_up(cfg: config.Config, *, files: timedelta = DAY, database: timedelta = DAY) -> None:
    """Both portions completed ``files`` and ``database`` before :data:`NOW`."""
    for portion, age in ((backup_facts.Portion.FILES, files), (backup_facts.Portion.DATABASE, database)):
        backup_facts.record(cfg, portion, completed_at=NOW - age, destination="/backups/x")


def glance_of(cfg: config.Config, **kwargs: Any) -> dict[str, Any]:
    found = status_glance.glance(cfg, now=kwargs.pop("now", NOW), **kwargs)
    assert problems(found) == [], found
    return found


def status_glance_via_cli() -> dict[str, Any]:
    code, out, err = drive(["--output", "json", "status"])
    assert code == 0, err
    found = json.loads(out)["data"]["summary"]["glance"]
    assert problems(found) == [], found
    return found


def at_gate(verb: str, gate: str, *, idle: timedelta | None = None) -> gates.RunState:
    try:
        state = gates.new_run(registry.entry(verb))
    except KeyError:
        state = gates.RunState(run_id=f"run-{verb.replace('.', '-')}", verb=verb, created=NOW.isoformat())
    state.open_gate = gate
    if idle is not None:
        state.created = (NOW - idle).isoformat()
    path = gates.save(state)
    if idle is not None:
        stamp = (NOW - idle).timestamp()
        os.utime(path, (stamp, stamp))
    return state


def running_job(cfg: config.Config, handler: str = "intake.tidal") -> str:
    with jobs.open_store(jobs.queue_path(cfg)) as store:
        job = jobs.enqueue(store, handler_key=handler, payload={}, cfg=cfg)
        jobs.transition(store, job.job_id, jobs.JobState.RUNNING)
    return job.job_id


def night_record(**fields: Any) -> None:
    record = {
        "schema": sync_night.STATUS_SCHEMA, "night": "2026-11-24",
        "line": "night of 2026-11-24: nothing new to land", "outcome": sync_night.NOTHING,
        **fields,
    }
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record))


def rekordbox_lists(monkeypatch, answer) -> None:
    """The process table doctor and the glance both read, answering ``answer``."""

    def listed():
        if isinstance(answer, BaseException):
            raise answer
        return answer

    monkeypatch.setattr(processes, "running_process_names", listed)


# ═══ The brief's scenarios ═══════════════════════════════════════════════════


def test_a_quiet_library_reads_ok(cfg):
    backed_up(cfg)
    found = glance_of(cfg)
    assert found["attention"] == status_glance.OK
    assert found["rekordbox"] == status_glance.CLOSED
    assert found["jobs_running"] == [] and found["gates"] == [] and found["night"] is None
    assert found["backup"]["files"]["state"] == "known"
    assert found["backup"]["files"]["age_seconds"] == int(DAY.total_seconds())
    assert found["backup"]["database"]["completed_at"] == (NOW - DAY).isoformat()
    assert found["version"] == status_glance.VERSION


def test_a_run_at_the_native_landing_gate_reads_gate_and_writes_the_database(cfg):
    backed_up(cfg)
    state = at_gate("intake.land", "intake.land.native")
    found = glance_of(cfg)
    assert found["attention"] == status_glance.GATE
    (item,) = found["gates"]
    assert item["run_id"] == state.run_id and item["verb"] == "intake.land"
    assert item["gate"] == "intake.land.native"
    assert item["writes_database"] is True and item["explicit"] is True
    assert item["options"] == ["apply", "abort"]
    assert item["old"] is False


def test_a_gate_on_a_verb_that_writes_no_database_says_so(cfg):
    backed_up(cfg)
    at_gate("profile.set", "profile.set.apply")
    (item,) = glance_of(cfg)["gates"]
    assert item["writes_database"] is gates.writes_the_database("profile.set") is False


def test_a_run_past_the_retire_threshold_is_listed_old_not_folded(cfg):
    backed_up(cfg)
    days = cfg.reports.open_gate_stale_days
    state = at_gate("intake.land", "intake.land.native", idle=timedelta(days=days + 1))
    found = glance_of(cfg)
    (item,) = found["gates"]
    assert item["run_id"] == state.run_id and item["old"] is True
    assert item["since"] == (NOW - timedelta(days=days + 1)).replace(microsecond=0).isoformat()
    assert found["attention"] == status_glance.GATE


def test_a_gate_just_inside_the_threshold_is_not_old(cfg):
    backed_up(cfg)
    days = cfg.reports.open_gate_stale_days
    at_gate("intake.land", "intake.land.native", idle=timedelta(days=days) - timedelta(hours=1))
    (item,) = glance_of(cfg)["gates"]
    assert item["old"] is False


def test_an_old_gate_retire_would_keep_is_not_old_and_its_unknowns_are_said(cfg):
    """A verb this build does not declare: retire keeps it, so ``old`` is false."""
    backed_up(cfg)
    at_gate("no.such.verb", "no.such.gate", idle=timedelta(days=400))
    (item,) = glance_of(cfg)["gates"]
    assert item["old"] is False
    assert item["options"] == [] and item["explicit"] is None
    assert item["writes_database"] is False


def test_a_run_waiting_on_a_person_without_a_gate_is_not_a_gate(cfg):
    backed_up(cfg)
    state = gates.new_run(registry.entry("profile.set"))
    gates.save(state)
    assert glance_of(cfg)["gates"] == []


def test_a_running_job_reads_running(cfg):
    backed_up(cfg)
    job_id = running_job(cfg)
    found = glance_of(cfg)
    assert found["jobs_running"] == [{"job_id": job_id, "verb": "intake.tidal", "state": "running"}]
    assert found["attention"] == status_glance.RUNNING


def test_a_queued_job_is_not_running(cfg):
    backed_up(cfg)
    with jobs.open_store(jobs.queue_path(cfg)) as store:
        jobs.enqueue(store, handler_key="intake.tidal", payload={}, cfg=cfg)
    found = glance_of(cfg)
    assert found["jobs_running"] == [] and found["attention"] == status_glance.OK


def test_a_gate_outranks_a_running_job(cfg):
    backed_up(cfg)
    running_job(cfg)
    at_gate("intake.land", "intake.land.native")
    assert glance_of(cfg)["attention"] == status_glance.GATE


@pytest.mark.parametrize("portion", ["files", "database"])
def test_a_backup_five_days_old_reads_backup_due(cfg, portion):
    backed_up(cfg, **{portion: timedelta(days=5)})
    assert glance_of(cfg)["attention"] == status_glance.BACKUP_DUE


def test_a_backup_just_under_five_days_reads_ok(cfg):
    backed_up(cfg, files=timedelta(days=5) - timedelta(minutes=1))
    assert glance_of(cfg)["attention"] == status_glance.OK


@pytest.mark.parametrize("missing", list(backup_facts.Portion))
def test_an_unknown_backup_age_reads_backup_due(cfg, missing):
    for portion in backup_facts.Portion:
        if portion is not missing:
            backup_facts.record(cfg, portion, completed_at=NOW - DAY, destination="/backups/x")
    found = glance_of(cfg)
    assert found["backup"][str(missing)] == {
        "state": "never-recorded", "age_seconds": None, "completed_at": None,
    }
    assert found["attention"] == status_glance.BACKUP_DUE


def test_a_backup_recorded_ahead_of_now_reads_fail(cfg):
    backed_up(cfg, database=-timedelta(days=2))
    found = glance_of(cfg)
    assert found["backup"]["database"]["state"] == "recorded-in-the-future"
    assert found["attention"] == status_glance.FAIL


def test_a_running_job_outranks_a_backup_that_is_due(cfg):
    running_job(cfg)
    assert glance_of(cfg)["attention"] == status_glance.RUNNING


# ── Unreadable is said, never empty, none or closed ─────────────────────────


def test_an_unreadable_run_record_is_an_item_and_reads_fail(cfg):
    backed_up(cfg)
    state = at_gate("intake.land", "intake.land.native")
    gates.run_path("damaged").write_text("{not json")
    found = glance_of(cfg)
    by_run = {item["run_id"]: item for item in found["gates"]}
    assert status_glance.is_unreadable(by_run["damaged"])
    assert "not readable JSON" in by_run["damaged"]["unreadable"]
    assert by_run[state.run_id]["gate"] == "intake.land.native"
    assert found["attention"] == status_glance.FAIL


def test_a_run_record_missing_its_fields_is_unreadable_not_a_crash(cfg):
    backed_up(cfg)
    gates.run_path("hollow").parent.mkdir(parents=True, exist_ok=True)
    gates.run_path("hollow").write_text(json.dumps({"version": gates.RUN_SCHEMA_VERSION}))
    found = glance_of(cfg)
    assert found["gates"][0]["run_id"] == "hollow"
    assert status_glance.is_unreadable(found["gates"][0])
    assert found["attention"] == status_glance.FAIL


def test_a_run_directory_that_cannot_be_listed_is_unreadable_not_empty(cfg, monkeypatch):
    backed_up(cfg)
    at_gate("intake.land", "intake.land.native")
    _refuse_listing(monkeypatch, gates.run_dir())
    found = glance_of(cfg)
    assert status_glance.is_unreadable(found["gates"])
    assert "Permission denied" in found["gates"]["unreadable"]
    assert found["attention"] == status_glance.FAIL


def test_no_run_directory_is_no_gate(cfg):
    backed_up(cfg)
    assert not gates.run_dir().exists()
    assert glance_of(cfg)["gates"] == []


def test_an_unreadable_night_record_reads_fail_not_null(cfg):
    backed_up(cfg)
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[]")
    found = glance_of(cfg)
    assert status_glance.is_unreadable(found["night"])
    assert "is not a night pass record" in found["night"]["unreadable"]
    assert found["attention"] == status_glance.FAIL


def test_a_night_record_without_a_gate_run_keeps_its_nulls(cfg):
    backed_up(cfg)
    night_record()
    night = glance_of(cfg)["night"]
    assert night["gate_run"] is None and night["pass_run"] is None and night["staging"] is None
    assert night["outcome"] == sync_night.NOTHING


def test_no_night_record_reads_null(cfg):
    backed_up(cfg)
    assert not sync_night.status_path().exists()
    found = glance_of(cfg)
    assert found["night"] is None and found["attention"] == status_glance.OK


def test_a_night_record_carries_the_fields_a_landing_needs(cfg):
    backed_up(cfg)
    night_record(outcome=sync_night.STOPPED, gate_run="G", pass_run="P", staging="/s")
    night = glance_of(cfg)["night"]
    assert night == {
        "outcome": sync_night.STOPPED, "line": "night of 2026-11-24: nothing new to land",
        "gate_run": "G", "pass_run": "P", "staging": "/s",
    }


def test_a_rekordbox_probe_that_raises_reads_unreadable_and_fail(cfg, monkeypatch):
    backed_up(cfg)
    rekordbox_lists(monkeypatch, RuntimeError("the table broke"))
    found = glance_of(cfg)
    assert found["rekordbox"] == {"unreadable": "RuntimeError: the table broke"}
    assert found["attention"] == status_glance.FAIL


def test_a_scan_that_could_not_confirm_absence_is_unknown_never_closed(cfg, monkeypatch):
    backed_up(cfg)
    unconfirmed = processes.AbsenceUnconfirmed(
        Cause(reason=processes.UNCONFIRMED, message="pid 7 could not be read",
              remediation=Remediation(remedy=Remedy.QUIT_REKORDBOX))
    )
    rekordbox_lists(monkeypatch, unconfirmed)
    found = glance_of(cfg)
    assert found["rekordbox"] == status_glance.UNKNOWN
    assert found["attention"] == status_glance.OK


def test_rekordbox_or_its_agent_running_reads_open(cfg, monkeypatch):
    backed_up(cfg)
    for name in processes.REKORDBOX_PROCESSES:
        rekordbox_lists(monkeypatch, ("launchd", name))
        assert glance_of(cfg)["rekordbox"] == status_glance.OPEN


def test_an_unreadable_job_queue_reads_fail_not_empty(cfg):
    backed_up(cfg)
    path = jobs.queue_path(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"this is not a database at all, and is long enough to say so" * 4)
    found = glance_of(cfg)
    assert status_glance.is_unreadable(found["jobs_running"])
    assert found["attention"] == status_glance.FAIL


def test_unreadable_backup_facts_read_fail_not_due(cfg):
    path = backup_facts.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json")
    found = glance_of(cfg)
    assert status_glance.is_unreadable(found["backup"])
    assert found["attention"] == status_glance.FAIL


def test_backup_ages_off_an_absent_library_volume_are_unreadable_not_never_recorded(cfg):
    """Review round one: the record is on the volume, so an absent root is not "never"."""
    backed_up(cfg)
    assert glance_of(cfg)["attention"] == status_glance.OK
    root = cfg.library.root
    root.rename(root.with_name("ejected"))
    found = glance_of(cfg)
    assert status_glance.is_unreadable(found["backup"])
    assert "could not establish that the volume is there" in found["backup"]["unreadable"]
    assert found["attention"] == status_glance.FAIL


def test_a_queue_that_cannot_be_looked_at_is_unreadable_not_empty(cfg):
    """Only an absent queue is no job; a path that cannot be stat'd says so."""
    backed_up(cfg)
    parent = jobs.queue_path(cfg).parent
    parent.parent.mkdir(parents=True, exist_ok=True)
    parent.write_text("a file where the queue's folder should be")
    found = glance_of(cfg)
    assert status_glance.is_unreadable(found["jobs_running"])
    assert "NotADirectoryError" in found["jobs_running"]["unreadable"]
    assert found["attention"] == status_glance.FAIL


def test_reading_the_queue_cannot_write_it(cfg, monkeypatch):
    """The connection ``read_jobs`` opens is read only: a write through it is refused."""
    import sqlite3

    running_job(cfg)
    asked: list[tuple[tuple, dict]] = []
    real = sqlite3.connect

    def recorded(*args, **kwargs):
        asked.append((args, kwargs))
        return real(*args, **kwargs)

    monkeypatch.setattr(sqlite3, "connect", recorded)
    assert len(jobs.read_jobs(jobs.queue_path(cfg))) == 1
    ((args, kwargs),) = asked
    monkeypatch.setattr(sqlite3, "connect", real)
    same = real(*args, **kwargs)
    try:
        with pytest.raises(sqlite3.OperationalError, match="readonly"):
            same.execute("DELETE FROM jobs")
    finally:
        same.close()
    with jobs.open_store(jobs.queue_path(cfg)) as store:
        assert len(jobs.list_jobs(store)) == 1


def test_unreadable_outranks_every_other_word(cfg, monkeypatch):
    running_job(cfg)
    at_gate("intake.land", "intake.land.native")
    rekordbox_lists(monkeypatch, RuntimeError("the table broke"))
    assert glance_of(cfg)["attention"] == status_glance.FAIL


# ── The schema ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize("key", status_glance.KEYS)
def test_the_schema_rejects_a_glance_missing_any_key(cfg, key):
    backed_up(cfg)
    found = glance_of(cfg)
    del found[key]
    assert problems(found) == [f"glance: missing {key!r}"]


def test_the_schema_names_exactly_the_keys_the_glance_carries():
    assert set(SCHEMA["required"]) == set(SCHEMA["properties"]) == set(status_glance.KEYS)
    assert SCHEMA["properties"]["attention"]["enum"] == list(status_glance.ATTENTION)
    assert SCHEMA["properties"]["version"]["enum"] == [status_glance.VERSION]
    portion = SCHEMA["$defs"]["portion"]
    assert portion["properties"]["state"]["enum"] == [str(s) for s in backup_facts.AgeState]
    backup = SCHEMA["properties"]["backup"]["anyOf"][1]
    assert backup["required"] == [str(p) for p in backup_facts.Portion]
    night = SCHEMA["$defs"]["night"]
    assert night["required"] == list(status_glance.NIGHT_FIELDS)


def test_the_schema_rejects_a_word_it_does_not_name_and_an_extra_key(cfg):
    backed_up(cfg)
    found = glance_of(cfg)
    assert problems({**found, "attention": "fine"})
    assert problems({**found, "extra": 1})
    assert problems({**found, "rekordbox": None})


def test_every_unreadable_shape_validates(cfg, monkeypatch):
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[]")
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_text("{not json")
    gates.run_dir().mkdir(parents=True, exist_ok=True)
    gates.run_path("damaged").write_text("{not json")
    rekordbox_lists(monkeypatch, RuntimeError("broke"))
    found = glance_of(cfg)
    for key in ("backup", "rekordbox", "night"):
        assert status_glance.is_unreadable(found[key]), key
    assert status_glance.is_unreadable(found["gates"][0])


# ── Through the verb, and agreeing with the verbs it projects ───────────────


def test_crate_status_carries_the_glance_and_keeps_its_summary(cfg):
    backed_up(cfg, files=timedelta(days=9))
    at_gate("intake.land", "intake.land.native")
    code, out, err = drive(["--output", "json", "status"])
    assert code == 0, err
    envelope = json.loads(out)
    assert output.envelope_problems(envelope) == []
    summary = envelope["data"]["summary"]
    assert {"open_runs", "old_gates", "sources", "trees", "library"} <= set(summary)
    assert summary["open_runs"] == 1
    assert problems(summary["glance"]) == []
    assert summary["glance"]["attention"] == status_glance.GATE


def _checks(argv: list[str]) -> dict[str, dict[str, Any]]:
    _code, out, _err = drive(["--output", "json", *argv])
    return {check["key"]: check for check in json.loads(out)["data"]["checks"]}


@pytest.mark.parametrize(
    ("table", "word", "doctor_status"),
    [
        ((), status_glance.CLOSED, "ok"),
        (("rekordboxAgent",), status_glance.OPEN, "fail"),
    ],
)
def test_the_glance_agrees_with_doctor_and_sync_night_last(cfg, monkeypatch, table, word, doctor_status):
    """One fixture, three verbs: the glance projects what each already says."""
    backup_facts.record(
        cfg, backup_facts.Portion.FILES, completed_at=datetime.now(timezone.utc) - 3 * DAY,
        destination="/backups/x",
    )
    night_record(outcome=sync_night.WAITING_GATE, gate_run="G", pass_run="P", staging="/s",
                 land_name="L")
    rekordbox_lists(monkeypatch, table)
    found = status_glance_via_cli()
    doctor_checks = _checks(["doctor"])

    files = found["backup"]["files"]
    assert files["state"] == "known"
    days = files["age_seconds"] // 86400
    assert f"last completed {days} days ago" in doctor_checks["backup.age.files"]["detail"]
    assert found["backup"]["database"]["state"] == "never-recorded"
    assert "no completion has been recorded" in doctor_checks["backup.age.database"]["detail"]

    assert found["rekordbox"] == word
    assert doctor_checks["rekordbox.closed"]["status"] == doctor_status

    _code, out, _err = drive(["--output", "json", "sync", "night", "--last"])
    last = json.loads(out)["data"]["summary"]["night"]
    assert found["night"] == {name: last.get(name) for name in status_glance.NIGHT_FIELDS}


def test_the_old_flag_agrees_with_what_run_retire_would_retire(cfg):
    from cratekit.cli.verbs import runs

    backed_up(cfg)
    days = cfg.reports.open_gate_stale_days
    old = at_gate("intake.land", "intake.land.native", idle=timedelta(days=days + 3))
    at_gate("profile.set", "profile.set.apply")
    retired, _unreadable = runs.old_gates(older_than=timedelta(days=days), now=NOW)
    would = {one.run_id for one in retired if one.retirable}
    found = glance_of(cfg)
    assert {item["run_id"] for item in found["gates"] if item["old"]} == would == {old.run_id}


# ── Reads only ──────────────────────────────────────────────────────────────


def _tree(*roots: Path) -> dict[str, str]:
    """Every file under ``roots`` and its digest; SQLite's own sidecars aside."""
    found: dict[str, str] = {}
    for root in roots:
        for folder, _dirs, files in os.walk(root):
            for name in files:
                if name.endswith(("-wal", "-shm")):
                    continue
                path = Path(folder) / name
                found[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return found


def test_the_glance_writes_nothing_and_creates_no_queue(cfg):
    backed_up(cfg)
    at_gate("intake.land", "intake.land.native")
    night_record()
    roots = (Path(os.environ["HOME"]), cfg.library.root)
    before = _tree(*roots)
    queue = jobs.queue_path(cfg)
    assert not queue.exists()
    glance_of(cfg)
    assert not queue.exists() and not queue.parent.exists()
    assert _tree(*roots) == before


def test_reading_the_queue_changes_no_byte_of_it(cfg):
    running_job(cfg)
    queue = jobs.queue_path(cfg)
    before = queue.read_bytes()
    stat = queue.stat()
    glance_of(cfg)
    assert queue.read_bytes() == before
    assert queue.stat().st_mtime_ns == stat.st_mtime_ns


# ── The human line ──────────────────────────────────────────────────────────


def _diagnostic(data: dict[str, Any]) -> output.Envelope:
    return output.build(
        verb="status", run_id="r", schema=output.current_schema("diagnostic"),
        started="2026-01-01T00:00:00+00:00", data=data,
    )


def test_the_human_rendering_keeps_its_lines_and_gains_one_naming_attention(cfg):
    backed_up(cfg)
    at_gate("intake.land", "intake.land.native")
    _code, out, _err = drive(["--output", "json", "status"])
    data = json.loads(out)["data"]
    bare = dict(data, summary={k: v for k, v in data["summary"].items() if k != "glance"})
    shown = render.render(_diagnostic(data)).splitlines()
    plain = render.render(_diagnostic(bare)).splitlines()
    assert [line for line in shown if line not in plain] == ["attention: gate"]
    assert [line for line in shown if line != "attention: gate"] == plain
    _code, out, err = drive(["status"])
    assert "attention: gate" in out.splitlines(), err


def test_the_attention_line_names_what_could_not_be_read(cfg):
    backed_up(cfg)
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[]")
    gates.run_dir().mkdir(parents=True, exist_ok=True)
    gates.run_path("damaged").write_text("{not json")
    _code, out, err = drive(["status"])
    assert "attention: fail (gates, night unreadable)" in out.splitlines(), (out, err)


def test_the_attention_line_is_gated_on_the_payload_not_the_verb():
    assert "attention" not in render.render(_diagnostic({"checks": [], "summary": {}}))
    named = {"checks": [], "summary": {"glance": {"attention": 7}}}
    assert "attention" not in render.render(_diagnostic(named))


def test_doctor_and_the_glance_agree_that_an_absent_volume_hides_the_backup_ages(cfg):
    """R-2082: one fixture, the root ejected, and neither verb reads the ages as never."""
    backup_facts.record(
        cfg, backup_facts.Portion.FILES, completed_at=datetime.now(timezone.utc) - 3 * DAY,
        destination="/backups/x",
    )
    backup_facts.record(
        cfg, backup_facts.Portion.DATABASE, completed_at=datetime.now(timezone.utc) - DAY,
        destination="/backups/x",
    )
    root = cfg.library.root
    root.rename(root.with_name("ejected"))
    found = status_glance_via_cli()
    doctor_checks = _checks(["doctor"])

    assert status_glance.is_unreadable(found["backup"])
    for portion in backup_facts.PORTIONS:
        check = doctor_checks[f"backup.age.{portion}"]
        assert check["status"] == "info", check
        assert "could not establish that the volume is there" in check["detail"], check
        assert "could not establish that the volume is there" in found["backup"]["unreadable"]
        assert "no completion has been recorded" not in check["detail"], check
