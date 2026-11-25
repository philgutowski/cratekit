"""The menu bar app's envelope fixtures, written from the real verbs (U965).

The Swift decoders under ``app/`` are tested on a macOS runner against JSON in
``app/Tests/CrateEngineTests/Fixtures``, and this file is what keeps that JSON
true. Each fixture is driven here through the real dispatcher, its envelope
validated, the values that differ per run put in fixed form, and the text
compared with the committed file, so a verb that changes what it emits fails
the battery until the fixture is regenerated and the app workflow reads the
new one, so the engine and the app cannot drift apart silently over these
envelopes. A shape no fixture carries, a pending human action, is not held
here; the card that first reads one adds its fixture.

The status fixtures (U966) are ``crate status`` once per ``attention`` word,
each state built the way ``tests/test_status_glance.py`` builds it (backup
records, runs at a gate, a running job, a night record, the process table),
read at a held clock so every age and wait is the same on every run.

Regenerate an intended change with ``REGEN=1``, the convention
``tests/golden/`` uses, then read the diff before committing it. Never edit a
fixture by hand: the verb is the source of truth.
"""

from __future__ import annotations

import functools
import io
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pytest

from cratekit import cli
from cratekit.cli import gates, output, registry, status_glance, sync_night
from cratekit.core import backup_facts, config, jobs, processes
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.taxonomy import default_taxonomy
from tests import doctor_machines
from tests.test_doctor import document_for, seed_taxonomy
from tests.test_reports_cli import _one_folder_export

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "app" / "Tests" / "CrateEngineTests" / "Fixtures"

#: What a fixture holds in place of each value that differs from run to run.
RUN_ID = "run-fixture"
INSTANT = "2026-01-01T00:00:00+00:00"
ROOT = "/fixture"
STATE = "/fixture-state"

REGENERATE_HINT = (
    "regenerate it with REGEN=1 .venv/bin/python -m pytest tests/test_app_fixtures.py, "
    "read the diff, and let the app workflow read the new fixture on the pull request"
)


@pytest.fixture
def machine(tmp_path, monkeypatch):
    """A set up machine with no database, its taxonomy seeded and its rekordbox pinned,
    so doctor on the green machine passes; every fixture's verb needs only this."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    # Read by doctor's provider budget line, and exported by the provider gate
    # to a detached child, so a shell that holds it would change doctor.json.
    monkeypatch.delenv("CRATEKIT_PROVIDER_CALLS_PER_HOUR", raising=False)
    made = config.from_dict(document_for(library))
    config.save(made)
    config.reset_cache()
    seed_taxonomy(config.load())
    # A person is present (U49), so the gate is reached however pytest was launched.
    from cratekit.core import session

    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)
    from cratekit.cli import doctor

    monkeypatch.setattr(doctor, "Probes", lambda: doctor_machines.green())
    return library


def emitted(argv: list[str]) -> dict[str, Any]:
    """What ``crate --output json`` prints for ``argv``, validated as an envelope."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    assert document["exit_code"] == code, (code, document)
    return document


@pytest.fixture
def places(tmp_path, _isolate_state_roots) -> dict[Path, str]:
    """The test's temporary roots and the fixed names a fixture gives them."""
    return {tmp_path: ROOT, _isolate_state_roots: STATE}


def fixed(document: dict[str, Any], places: dict[Path, str]) -> dict[str, Any]:
    """The envelope with its run id, its times and its temporary roots in fixed form."""
    run_id = document["run_id"]
    named = {str(path): name for path, name in places.items()}
    named |= {str(path.resolve()): name for path, name in places.items()}
    prefixes = sorted(named, key=len, reverse=True)

    def value(item: Any) -> Any:
        if isinstance(item, dict):
            return {key: value(member) for key, member in item.items()}
        if isinstance(item, list):
            return [value(member) for member in item]
        if isinstance(item, str):
            for prefix in prefixes:
                item = item.replace(prefix, named[prefix])
            return item.replace(run_id, RUN_ID)
        return item

    made = value(document)
    made["started"] = made["ended"] = INSTANT
    return made


def text_of(document: dict[str, Any]) -> str:
    return json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


# The scenarios. Each returns the envelope and asserts the one thing it is
# there to show, so broken setup fails here instead of recording a refusal
# nobody meant as the fixture.


def doctor_on_a_green_machine(library: Path) -> dict[str, Any]:
    document = emitted(["doctor"])
    assert document["outcome"] == "ok", document
    assert document["data"]["checks"], document
    return document


def gate_refusal_with_its_screen(library: Path) -> dict[str, Any]:
    document = emitted(["profile", "set", "slim"])
    assert document["exit_code"] == int(ExitCode.DECISION_REQUIRED), document
    assert document["cause"]["reason"] == "decision-required", document
    assert document["cause"]["detail"]["shown"]["items"], document
    return document


def refusal_with_steps(library: Path) -> dict[str, Any]:
    export = _one_folder_export(library / "no-tree.xml", default_taxonomy().intake.display)
    document = emitted(["audit", "coverage", str(export)])
    assert document["cause"]["reason"] == "governed-tree-absent", document
    assert len(document["cause"]["remediation"]["steps"]) == 2, document
    return document


# The status fixtures, one per attention word (U966).

#: The instant every status fixture is read at.
STATUS_NOW = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
DAY = timedelta(days=1)
LANDING_RUN = "run-fixture-landing"
PROFILE_RUN = "run-fixture-profile"
DAMAGED_RUN = "run-fixture-damaged"
RUNNING_JOB = "job-fixture-running"


def _held_clock(patch: pytest.MonkeyPatch) -> None:
    """``crate status`` reads its clock in two places; both read :data:`STATUS_NOW`."""
    from cratekit.cli import doctor

    patch.setattr(doctor, "_run_report", functools.partial(doctor._run_report, now=STATUS_NOW))
    real = status_glance.glance
    patch.setattr(status_glance, "glance", lambda cfg, **kw: real(cfg, now=STATUS_NOW, **kw))


def _backed_up(files: timedelta | None = DAY, database: timedelta | None = 2 * DAY) -> None:
    """Each portion completed that long before the held clock; None records nothing."""
    cfg = config.load()
    for portion, age in (
        (backup_facts.Portion.FILES, files), (backup_facts.Portion.DATABASE, database),
    ):
        if age is not None:
            backup_facts.record(
                cfg, portion, completed_at=STATUS_NOW - age, destination="/backups/fixture")


def _at_gate(run_id: str, verb: str, gate: str, *, idle: timedelta) -> None:
    state = gates.new_run(registry.entry(verb), run_id=run_id)
    state.open_gate = gate
    state.created = (STATUS_NOW - idle).isoformat()
    path = gates.save(state)
    stamp = (STATUS_NOW - idle).timestamp()
    os.utime(path, (stamp, stamp))


def _night(text: str | None = None, **fields: Any) -> None:
    """The night pass record, ``text`` written as it is when given."""
    record = {
        "schema": sync_night.STATUS_SCHEMA, "night": "2025-12-31",
        "line": "night of 2025-12-31: nothing new to land", "outcome": sync_night.NOTHING,
        **fields,
    }
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record) if text is None else text, encoding="utf-8")


def _rekordbox_lists(patch: pytest.MonkeyPatch, answer: Any) -> None:
    """The process table doctor and the glance both read, answering ``answer``."""

    def listed():
        if isinstance(answer, BaseException):
            raise answer
        return answer

    patch.setattr(processes, "running_process_names", listed)


def status_of(prepare: Callable[[pytest.MonkeyPatch], None], word: str) -> dict[str, Any]:
    """``crate status`` after ``prepare``, at the held clock, reading ``word``."""
    with pytest.MonkeyPatch.context() as patch:
        _held_clock(patch)
        prepare(patch)
        document = emitted(["status"])
    assert document["exit_code"] == 0, document
    glance = document["data"]["summary"]["glance"]
    assert glance["attention"] == word, glance
    return document


def status_ok(library: Path) -> dict[str, Any]:
    return status_of(lambda patch: _backed_up(), status_glance.OK)


def status_gate(library: Path) -> dict[str, Any]:
    def prepare(patch: pytest.MonkeyPatch) -> None:
        _backed_up()
        _at_gate(LANDING_RUN, "intake.land", "intake.land.native", idle=timedelta(hours=3))
        past = timedelta(days=config.load().reports.open_gate_stale_days + 10)
        _at_gate(PROFILE_RUN, "profile.set", "profile.set.apply", idle=past)
        _night(
            outcome=sync_night.WAITING_GATE, gate_run=LANDING_RUN, pass_run="pass-fixture",
            staging="/fixture-staging", land_name="pass-fixture",
            line="night of 2025-12-31: the landing waits at its gate",
        )

    document = status_of(prepare, status_glance.GATE)
    old = {item["run_id"]: item["old"] for item in document["data"]["summary"]["glance"]["gates"]}
    assert old == {LANDING_RUN: False, PROFILE_RUN: True}, old
    return document


def status_running(library: Path) -> dict[str, Any]:
    def prepare(patch: pytest.MonkeyPatch) -> None:
        _backed_up()
        cfg = config.load()
        if not jobs.read_jobs(jobs.queue_path(cfg), states=(jobs.JobState.RUNNING,)):
            with jobs.open_store(jobs.queue_path(cfg)) as store:
                jobs.enqueue(store, handler_key="intake.tidal", payload={}, cfg=cfg,
                             job_id=RUNNING_JOB)
                jobs.transition(store, RUNNING_JOB, jobs.JobState.RUNNING)
        _rekordbox_lists(patch, ("launchd", processes.REKORDBOX_PROCESSES[0]))

    return status_of(prepare, status_glance.RUNNING)


def status_backup_due(library: Path) -> dict[str, Any]:
    def prepare(patch: pytest.MonkeyPatch) -> None:
        _backed_up(files=9 * DAY, database=None)
        _night()
        _rekordbox_lists(patch, processes.AbsenceUnconfirmed(
            Cause(reason=processes.UNCONFIRMED, message="pid 7 could not be read",
                  remediation=Remediation(remedy=Remedy.QUIT_REKORDBOX))))

    return status_of(prepare, status_glance.BACKUP_DUE)


def status_fail(library: Path) -> dict[str, Any]:
    def prepare(patch: pytest.MonkeyPatch) -> None:
        _backed_up(database=-2 * DAY)
        _at_gate(LANDING_RUN, "intake.land", "intake.land.native", idle=timedelta(hours=3))
        gates.run_path(DAMAGED_RUN).write_text("{not json", encoding="utf-8")
        _night(text="[]")
        _rekordbox_lists(patch, RuntimeError("the process table could not be read"))

    document = status_of(prepare, status_glance.FAIL)
    glance = document["data"]["summary"]["glance"]
    assert status_glance.is_unreadable(glance["rekordbox"]), glance
    assert status_glance.is_unreadable(glance["night"]), glance
    assert any(status_glance.is_unreadable(item) for item in glance["gates"]), glance
    return document


SCENARIOS: dict[str, Callable[[Path], dict[str, Any]]] = {
    "doctor": doctor_on_a_green_machine,
    "gate_refusal": gate_refusal_with_its_screen,
    "refusal_with_steps": refusal_with_steps,
    "status_ok": status_ok,
    "status_gate": status_gate,
    "status_running": status_running,
    "status_backup_due": status_backup_due,
    "status_fail": status_fail,
}


def check(name: str, text: str, directory: Path) -> None:
    """Fail unless the fixture ``name`` in ``directory`` holds exactly ``text``."""
    path = directory / f"{name}.json"
    assert path.is_file(), f"{path.name} is missing; {REGENERATE_HINT}"
    committed = path.read_text(encoding="utf-8")
    assert committed == text, (
        f"{path.name} no longer matches what its verb emits; {REGENERATE_HINT}"
    )


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_each_fixture_is_what_its_verb_emits(name, machine, places):
    text = text_of(fixed(SCENARIOS[name](machine), places))
    if os.environ.get("REGEN") == "1":
        FIXTURES.mkdir(parents=True, exist_ok=True)
        (FIXTURES / f"{name}.json").write_text(text, encoding="utf-8")
    check(name, text, FIXTURES)


def test_the_fixtures_are_the_scenarios_and_nothing_else():
    """A fixture no scenario writes is never checked, so it may not be there.

    A hidden file, the .DS_Store Finder leaves, is no fixture and is passed over.
    """
    listed = [path for path in FIXTURES.iterdir() if not path.name.startswith(".")]
    assert sorted(path.stem for path in listed) == sorted(SCENARIOS), listed
    assert all(path.suffix == ".json" for path in listed), listed


def test_there_is_a_status_fixture_for_every_attention_word():
    """A word the glance gains needs its fixture, so the app is tested on it (U966)."""
    words = {
        name.removeprefix("status_").replace("_", "-")
        for name in SCENARIOS if name.startswith("status_")
    }
    assert words == set(status_glance.ATTENTION)


def test_a_fixture_edited_away_from_its_verb_fails(machine, places, tmp_path):
    """The comparison is what fails the battery, so it must see a one value edit."""
    text = text_of(fixed(SCENARIOS["gate_refusal"](machine), places))
    edited = tmp_path / "edited"
    edited.mkdir()
    (edited / "gate_refusal.json").write_text(
        text.replace('"decision-required"', '"decision-stale"', 1), encoding="utf-8")
    with pytest.raises(AssertionError, match="no longer matches"):
        check("gate_refusal", text, edited)
    with pytest.raises(AssertionError, match="is missing"):
        check("doctor", text, edited)


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_a_fixture_holds_no_value_that_differs_per_run(name, machine, places):
    """Two runs give one text, and it names no run and no temporary root."""
    first = fixed(SCENARIOS[name](machine), places)
    second = fixed(SCENARIOS[name](machine), places)
    assert first["run_id"] == RUN_ID, first
    assert text_of(first) == text_of(second)
    text = text_of(first)
    for path in places:
        for real in (str(path), str(path.resolve())):
            assert real not in text, real
    assert (first["started"], first["ended"]) == (INSTANT, INSTANT)
