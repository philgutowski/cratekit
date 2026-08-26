"""The contract a queued verb owes its own resume, derived rather than listed.

WHAT THIS FILE EXISTS FOR. A verb that declares an ``explicit`` gate and queues a
job is re-invoked by :mod:`cratekit.core.jobs` as a SUBPROCESS. That child is a
fresh process, and ``cli.run`` mints a NEW run whenever ``--run`` is absent, so a
resume argv naming only the job meets the gate with nothing recorded against it
and exits DECISION_REQUIRED. Every respawn does the same. The queue then holds
work that nothing in the product can advance, and the person who confirmed it is
told nothing.

THREE SHIPPED VERBS HAD THAT SHAPE AND TWO WERE LIVE, measured 2026-08-23:
``adopt.apply`` (fixed in the unit that found it), ``export.playlist``, and
``sync.favorites``. ``delete.review`` has the shape and is latent because nothing
enqueues it.

WHY THE FIRST GUARD IS DERIVED FROM THE REGISTRY AND NOT A LIST OF THREE NAMES.
The defect is a property of a COMBINATION any future verb can arrive at:
``long_running``, an ``argv_builder``, and a non exempt ``explicit`` gate. A test
naming today's three would pass for ever while the fourth verb shipped broken,
which is the same shape as a guard that forbids an implementation instead of a
feature. P3: walk the registry, and the day somebody adds the fourth it is
covered without this file being edited.

AND WHY THE TOKEN IS MATCHED WHOLE. The predicate that first surveyed this asked
whether the builder's source contained the substring ``--run``, and reported
``sync.favorites`` CLEAN, because ``--run-id`` contains it. ``--run-id`` is that
verb's own argument for the INTAKE run and restores no gate state at all. A
substring is not a flag.
"""

from __future__ import annotations

import importlib
import io
import json
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import config, jobs, rb_writer
from cratekit.core.exit_codes import ExitCode
from tests.test_cli_contract import UNREACHABLE_GATES
from tests.test_config import valid_data


def _explicitly_gated_queued_verbs() -> list[registry.Entry]:
    """Every landed verb that queues work behind a gate only a person can answer.

    DERIVED, and the exemption is taken from the conformance suite's own map
    rather than spelled again here, so a gate that stops being unreachable is
    covered by this guard on the same day it stops.
    """
    found = []
    for entry in registry.ENTRIES:
        if not (entry.landed and entry.long_running and entry.argv_builder):
            continue
        if any(
            spec.explicit and spec.name not in UNREACHABLE_GATES for spec in entry.gates
        ):
            found.append(entry)
    return found


QUEUED_GATED = _explicitly_gated_queued_verbs()


def test_the_population_this_file_guards_is_not_empty():
    """A derived parametrisation that derives nothing passes silently for ever."""
    assert QUEUED_GATED, (
        "no landed verb both queues and declares a non exempt explicit gate, so "
        "every parametrised guard below is vacuous; if that is genuinely true "
        "now, this file is what should fail rather than nothing"
    )


@pytest.mark.parametrize("entry", QUEUED_GATED, ids=lambda e: e.name)
def test_a_queued_gated_verb_emits_the_run_its_decision_was_recorded_against(entry):
    """The resume argv must carry the gate run as the root ``--run`` flag.

    Matched as a WHOLE TOKEN in the returned list rather than as a substring of
    the source, because ``--run-id`` contains ``--run`` and is a different flag
    answering a different question. The list is the contract; the source is not.
    """
    module = importlib.import_module(entry.module)
    builder = getattr(module, entry.argv_builder)

    class _Job:
        job_id = "job-1"
        payload = {jobs.GATE_RUN_KEY: "gate-run-1", "playlist": "pl-1", "run_id": "intake-1"}

    argv = list(builder(_Job()))
    assert "--run" in argv, (
        f"{entry.name} declares an explicit gate and queues a job, and its "
        f"resume argv {argv} does not carry the root --run flag. The child the "
        f"job driver spawns will mint a fresh run, meet the gate with nothing "
        f"recorded, and exit DECISION_REQUIRED on every respawn"
    )
    assert argv[argv.index("--run") + 1] == "gate-run-1", (
        f"{entry.name} emits --run with something other than the frozen gate run"
    )


@pytest.mark.parametrize("entry", QUEUED_GATED, ids=lambda e: e.name)
def test_a_payload_from_an_older_build_still_builds_a_valid_command_line(entry):
    """No gate run frozen means no flag, never a crash in a detached subprocess.

    A job queued before this contract landed carries no gate run. The builder
    must return the argv it always returned, so that job resumes to the refusal
    it was already in, rather than raising a KeyError inside a child whose only
    output is a log file nobody is watching.
    """
    module = importlib.import_module(entry.module)
    builder = getattr(module, entry.argv_builder)

    class _Older:
        job_id = "job-1"
        payload = {"playlist": "pl-1"}

    argv = list(builder(_Older()))
    assert "--run" not in argv, (
        f"{entry.name} emitted --run with no gate run frozen, so the child would "
        f"be handed an empty or literal run identifier"
    )
    assert argv, f"{entry.name} returned an empty command line"
    assert all(isinstance(part, str) for part in argv)
    # NOT "--job in argv". delete.review's resume is the same command and
    # declares no --job argument, which is that verb's shape rather than a gap.
    assert argv[0] != "--run"


def test_the_gate_run_key_is_one_name_and_every_shell_uses_it():
    """One symbol, not four spellings, and the reason is the defect it prevents.

    ``sync.favorites`` already froze a ``run_id`` and it is the INTAKE run, a
    different thing that happened to default to the same value. Its builder
    emitted that one and looked correct while restoring nothing. Two concepts
    under one name is how that read as a fix, so the gate run has a name of its
    own and this asserts nobody re-spells it locally.
    """
    assert jobs.GATE_RUN_KEY == "gate_run_id"
    for entry in QUEUED_GATED:
        source = Path("src", *entry.module.split(".")).with_suffix(".py").read_text()
        assert '"run_id": ctx.run.run_id' not in source, (
            f"{entry.module} freezes the gate run under the intake run's name, "
            f"which is the confusion jobs.GATE_RUN_KEY exists to end"
        )


# ═══════════════════════════════════════════════════════════════════════════
# Driven. The static guards above cannot see a flag the dispatcher rejects.
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def installed(tmp_path, monkeypatch):
    """A machine the real dispatcher can load, with every module switched on."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    return resolved


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue() or "{}")


def _approve_and_queue(verb: list[str], gate: str) -> tuple[str, str]:
    """R34's two acts, then the queueing drive. Returns (run_id, job_id)."""
    code, refused = _drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == gate
    run_id = refused["run_id"]
    decided, envelope = _drive(
        ["run", "decide", run_id, gate, detail["options"][0], "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, queued = _drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), queued
    return run_id, queued["data"]["job_id"]


#: Stands in for a path under the CONFIGURED library, substituted once the
#: fixture has built one. A literal here would be a real path on somebody's
#: machine (R1), and the parametrisation is read before any fixture runs.
LIBRARY_FOLDER = "<library>"


def _resolved(verb: list[str]) -> list[str]:
    root = config.load().library.root
    return [str(root / "Music") if part == LIBRARY_FOLDER else part for part in verb]


@pytest.mark.parametrize(
    "verb, gate",
    [
        (["export", "playlist", "crate-export"], "export.playlist.confirm"),
        (["sync", "favorites"], "sync.favorites.confirm"),
        (["tag", "retag", LIBRARY_FOLDER], "tag.retag.confirm"),
    ],
    ids=["export.playlist", "sync.favorites", "tag.retag"],
)
def test_the_resume_the_job_driver_spawns_can_actually_proceed(installed, verb, gate):
    """The one check the static guards cannot make: does the dispatcher accept it.

    Two of these verbs shipped broken and both were driven to a permanent exit
    10 on 2026-08-23. Asserting the argv equals a list is a unit test of a list.
    Running the real ``argv_for`` output through the real dispatcher is the only
    thing that can tell a resume that works from one refused for ever.

    ``tag.retag`` joined on 2026-08-26, in the unit that landed it rather than in
    a later sweep, because a verb arriving with this combination is exactly the
    fourth verb the file's own docstring says a hardcoded list of three would miss.
    """
    del installed
    verb = _resolved(verb)
    _run_id, job_id = _approve_and_queue(verb, gate)

    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    argv = cli_jobs.argv_for(job)
    assert "--run" in argv, argv

    code, resumed = _drive(argv)
    assert code == int(ExitCode.OK), (
        f"the resume the driver spawns refuses: {resumed.get('cause')}. A job "
        f"whose own resume cannot answer its gate is a job nothing can advance"
    )
    assert resumed["data"]["job_id"] == job_id


def test_the_favorites_intake_run_and_its_gate_run_are_separate_fields(installed):
    """The near miss, pinned. Two runs travel on this verb and they are not one.

    ``--run-id`` carries the intake run shared across a sync's sources.
    ``--run`` carries the run the confirm decision was recorded against. They
    default to the same value, which is precisely why emitting only the first
    looked like carrying the run. Driving with an explicit, DIFFERENT intake run
    is what makes the two visible as separate fields rather than one value seen
    twice.
    """
    del installed
    code, refused = _drive(["sync", "favorites", "--run-id", "an-intake-run"])
    assert code == int(ExitCode.DECISION_REQUIRED)
    gate_run = refused["run_id"]
    assert gate_run != "an-intake-run"
    decided, _ = _drive(
        ["run", "decide", gate_run, "sync.favorites.confirm", "sync", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK)
    code, queued = _drive(
        ["--run", gate_run, "sync", "favorites", "--run-id", "an-intake-run"]
    )
    assert code == int(ExitCode.OK), queued

    with jobs.open_store() as store:
        job = jobs.get(store, queued["data"]["job_id"])
    assert job.payload["run_id"] == "an-intake-run"
    assert job.payload[jobs.GATE_RUN_KEY] == gate_run

    argv = cli_jobs.argv_for(job)
    assert argv[argv.index("--run") + 1] == gate_run
    assert argv[argv.index("--run-id") + 1] == "an-intake-run"
    assert _drive(argv)[0] == int(ExitCode.OK)
