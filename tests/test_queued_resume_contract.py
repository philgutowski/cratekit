"""The contract a queued verb owes its own resume, derived rather than listed.

A queued verb behind an ``explicit`` gate is respawned as a subprocess, and with
no ``--run`` it meets the gate with nothing recorded on every respawn (2026-08-23).
Derived from the registry, since any future verb can arrive at the combination,
and the token matched whole, since ``--run-id`` contains ``--run``.
"""

from __future__ import annotations

import importlib
import shutil
from pathlib import Path

import pytest

from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import config, jobs, rb_writer, tags, taxonomy
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import source as outbound_source
from cratekit.tagging import searchers
from cratekit.tagging.tag import SearchHit
from tests import outbound_fakes
from tests._containers import synth_container
from tests.cli_drive import approve_and_queue as _approve_and_queue
from tests.cli_drive import drive as _drive
from tests.test_cli_contract import UNREACHABLE_GATES
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414 - fixture

#: Every landed verb that queues work behind a gate only a person can answer,
#: the exemption taken from the conformance suite's own map.
QUEUED_GATED = [
    entry
    for entry in registry.ENTRIES
    if entry.landed and entry.long_running and entry.argv_builder
    and any(spec.explicit and spec.name not in UNREACHABLE_GATES for spec in entry.gates)
]


def _argv(entry: registry.Entry, payload: dict) -> list[str]:
    """What the verb's resume builder returns for a job carrying ``payload``."""
    job = type("_Job", (), {"job_id": "job-1", "payload": payload})
    return list(getattr(importlib.import_module(entry.module), entry.argv_builder)(job()))


def test_the_population_this_file_guards_is_not_empty():
    """A derived parametrisation that derives nothing passes silently for ever."""
    assert QUEUED_GATED, "no landed verb queues behind an explicit gate, so every guard is vacuous"


@pytest.mark.parametrize("entry", QUEUED_GATED, ids=lambda e: e.name)
def test_a_queued_gated_verb_emits_the_run_its_decision_was_recorded_against(entry):
    """The resume argv carries the gate run as the root ``--run`` flag, a whole token."""
    argv = _argv(entry, {jobs.GATE_RUN_KEY: "gate-run-1", "playlist": "pl-1", "run_id": "intake-1"})
    assert "--run" in argv, (
        f"{entry.name} queues behind an explicit gate and its resume argv {argv} does not "
        f"carry --run, so every respawn meets the gate with nothing recorded"
    )
    assert argv[argv.index("--run") + 1] == "gate-run-1", (
        f"{entry.name} emits --run with something other than the frozen gate run"
    )


@pytest.mark.parametrize("entry", QUEUED_GATED, ids=lambda e: e.name)
def test_a_payload_from_an_older_build_still_builds_a_valid_command_line(entry):
    """No gate run frozen means no flag, never a crash in a detached subprocess."""
    argv = _argv(entry, {"playlist": "pl-1"})
    assert "--run" not in argv, f"{entry.name} emitted --run with no gate run frozen"
    assert argv, f"{entry.name} returned an empty command line"
    assert all(isinstance(part, str) for part in argv)
    assert argv[0] != "--run"


def test_the_gate_run_key_is_one_name_and_every_shell_uses_it():
    """The gate run has a name of its own, since ``sync.favorites`` froze the intake run's."""
    assert jobs.GATE_RUN_KEY == "gate_run_id"
    for entry in QUEUED_GATED:
        source = Path("src", *entry.module.split(".")).with_suffix(".py").read_text()
        assert '"run_id": ctx.run.run_id' not in source, (
            f"{entry.module} freezes the gate run under the intake run's name"
        )


# ── Driven: the static guards cannot see a flag the dispatcher rejects ──────


@pytest.fixture
def no_rekordbox(monkeypatch):
    """Neither rekordbox nor its agent is running."""
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)


@pytest.fixture(scope="module")
def _silence(tmp_path_factory) -> Path:
    """One real audio container, synthesized once for the whole module."""
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def coarse_folder(installed, _silence):
    """One file whose genre the taxonomy would correct, since ``tag.retag`` queues no empty plan."""
    catch_all = taxonomy.default_taxonomy().fallback.too_coarse_as_source[1]
    path = installed.library.root / "Music" / "too-coarse.flac"
    shutil.copy2(_silence, path)
    assert tags.write_genre(path, catch_all), "the fixture could not tag the file"
    return path


@pytest.fixture
def catalogue(monkeypatch):
    """A genre answer the tagging worker reads at call time instead of a live catalogue."""
    hit = SearchHit(genre="Deep House", source="beatport", source_genre="Deep House")
    monkeypatch.setattr(
        searchers, "for_taxonomy", lambda declared=None, refusals=None: lambda artist, title: hit
    )


@pytest.fixture
def remote(monkeypatch):
    """A fake account matching every track of the shared export, so a job reaches done."""
    account = outbound_fakes.FakeAccount(catalog={str(index): f"tid-{index}" for index in range(1, 6)})
    monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(account))
    # The parsed export is memoized per process by absolute path, so cleared at both ends.
    outbound_source.forget_libraries()
    yield account
    outbound_source.forget_libraries()


#: Stand for a folder and an export under the CONFIGURED library, substituted
#: once a fixture has built one; the parametrisation is read before any does.
LIBRARY_FOLDER = "<library>"
LIBRARY_EXPORT = "<export>"


def _resolved(verb: list[str]) -> list[str]:
    root = config.load().library.root
    substitutions = {
        LIBRARY_FOLDER: str(root / "Music"),
        LIBRARY_EXPORT: str(outbound_fakes.write_export(root / "outbound")),
    }
    return [substitutions.get(part, part) for part in verb]


@pytest.mark.parametrize(
    "verb, gate",
    [
        (["export", "playlist", outbound_fakes.CRATE, "--export", LIBRARY_EXPORT],
         "export.playlist.confirm"),
        (["sync", "favorites", "--export", LIBRARY_EXPORT], "sync.favorites.confirm"),
        (["tag", "retag", LIBRARY_FOLDER], "tag.retag.confirm"),
    ],
    ids=["export.playlist", "sync.favorites", "tag.retag"],
)
def test_the_resume_the_job_driver_spawns_can_actually_proceed(
    installed, no_rekordbox, remote, catalogue, request, verb, gate
):
    """The real ``argv_for`` through the real dispatcher: OK means answerable and the work ran."""
    if gate == "tag.retag.confirm":
        request.getfixturevalue("coarse_folder")
    _run_id, job_id = _approve_and_queue(_resolved(verb), gate)
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    argv = cli_jobs.argv_for(job)
    assert "--run" in argv, argv
    code, resumed = _drive(argv)
    assert code == int(ExitCode.OK), (
        f"the resume the driver spawns refuses: {resumed.get('cause')}, so nothing can "
        f"advance the job"
    )
    assert resumed["data"]["job_id"] == job_id


def test_the_favorites_intake_run_and_its_gate_run_are_separate_fields(installed, no_rekordbox, remote):
    """``--run-id`` is the intake run and ``--run`` the gate's, shown apart by a different one."""
    exported = str(outbound_fakes.write_export(config.load().library.root / "outbound"))
    verb = ["sync", "favorites", "--run-id", "an-intake-run", "--export", exported]
    code, refused = _drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED)
    gate_run = refused["run_id"]
    assert gate_run != "an-intake-run"
    decided, _ = _drive(
        ["run", "decide", gate_run, "sync.favorites.confirm", "sync", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK)
    code, queued = _drive(["--run", gate_run, *verb])
    assert code == int(ExitCode.OK), queued
    with jobs.open_store() as store:
        job = jobs.get(store, queued["data"]["job_id"])
    assert job.payload["run_id"] == "an-intake-run"
    assert job.payload[jobs.GATE_RUN_KEY] == gate_run
    argv = cli_jobs.argv_for(job)
    assert argv[argv.index("--run") + 1] == gate_run
    assert argv[argv.index("--run-id") + 1] == "an-intake-run"
    assert _drive(argv)[0] == int(ExitCode.OK)
