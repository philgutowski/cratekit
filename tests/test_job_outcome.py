"""R-290 and R-225: how a job ended decides how its verb exits, in every queued verb.

A queued verb's resume drives the job and then reports it. Two endings used to
leave through a normal envelope the dispatcher exits 0 over. A PARKED job, because
``jobs.drive`` returns normally with the job ``blocked`` and a blocked job is open,
so the "closed and carrying a cause" predicate every shell copied never saw it
(R-290). And a job that closed FAILED, in the three shells that never copied that
predicate at all (R-225). Anything wrapping the verb read a clean success while
the provider had just walled the account.

THE POPULATION IS ``handlers.HANDLERS`` AND NOT A LIST TYPED HERE. Every key bound
to a worker is driven through the command line its own verb declares for a resume,
with the worker swapped for one that parks or fails. A verb bound tomorrow is in
the population the moment it is bound, so it cannot forget the mapping and stay
green.

EVERY DRIVEN CASE ASSERTS THE STATE THE JOB REACHED, before it asserts the exit.
A verb that refused on a precondition also exits non zero, and without the state
check that refusal would pass as the property under test.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.cli import handlers
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError, JobBlocked, Outcome, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from tests.cli_drive import drive
from tests.test_config import valid_data

SRC = Path(__file__).resolve().parents[1] / "src" / "cratekit"

#: ``job.resume`` is the supervisor's own key: it spawns a child and drives nothing.
SUPERVISOR = "job.resume"

#: Driven in its own suite, and why. ``adopt apply`` opens a destructive session
#: before it looks at the job, which needs a rekordbox database, a recorded
#: acknowledgment and a pinned application version. That machine lives in
#: ``tests/test_adopt_workers.py`` and so does this key's parked test. The guard
#: below keeps this table from outliving the reason for it.
DRIVEN_ELSEWHERE = {
    "adopt.apply": "tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero",
}

#: What each verb's argv builder reads off the frozen payload before it can name
#: the verb at all. Only what the BUILDER or the shell's argument check needs:
#: nothing here is a file that exists, because no worker in this suite is real.
PAYLOADS: dict[str, dict[str, object]] = {
    "master": {"source": "set.wav"},
    "rebuild": {"actor": "a-person"},
    "tag.retag": {"folder": "Music"},
}

QUEUED_KEYS = sorted(
    key for key in handlers.HANDLERS if key != SUPERVISOR and key not in DRIVEN_ELSEWHERE
)


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(valid_data(root, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


def _block() -> CratekitError:
    return refuse(
        "provider-blocked",
        "the provider refused this client",
        remedy=Remedy.RETRY_LATER,
        origin=("test",),
    )


def parks(job, item, cfg):
    """The worker's answer that the RUN must stop."""
    raise jobs.Parked(_block().cause)


def fails_the_second(job, item, cfg):
    """One item completes and one does not, which is the shape ``drive`` returns
    normally over with the job recorded failed."""
    if item.item_id == "two":
        raise refuse("source-missing", "the second item is not there", origin=("test",))
    return None


def queued(cfg: config.Config, key: str, items: tuple[str, ...]) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.enqueue(
            store,
            handler_key=key,
            payload=dict(PAYLOADS.get(key, {})),
            cfg=cfg,
            item_ids=items,
        )


def job_of(job_id: str) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.get(store, job_id)


def resumed(job: jobs.Job) -> tuple[int, dict]:
    """Drive the verb's own resume command line, answering its gate if it has one.

    R34'S TWO ACTS, NOT A FLAG. A verb with an explicit gate refuses the first
    drive with ``decision-required`` and names the run. The decision is recorded
    against that run as a separate act, and the resume is driven again naming it,
    which is what a person does and what ``cli_drive.approve_and_queue`` does for
    the queueing side.
    """
    argv = cli_jobs.argv_for(job)
    code, envelope = drive(argv)
    if code != int(ExitCode.DECISION_REQUIRED):
        return code, envelope
    detail = envelope["cause"]["detail"]
    run_id = envelope["run_id"]
    decided, answer = drive(
        ["run", "decide", run_id, detail["gate"], detail["options"][0], "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), answer
    return drive(["--run", run_id, *argv])


# ═══════════════════════════════════════════════════════════════════════════
# The mapping itself
# ═══════════════════════════════════════════════════════════════════════════


def _job_in(machine, state: jobs.JobState, *, cause=None) -> jobs.Job:
    job = queued(machine, "master", ("one",))
    with jobs.open_store() as store:
        if state is jobs.JobState.QUEUED:
            return job
        if state is jobs.JobState.BLOCKED:
            return jobs.block(store, job.job_id, cause)
        jobs.transition(store, job.job_id, jobs.JobState.RUNNING)
        return jobs.transition(store, job.job_id, state, cause=cause)


def test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause(machine):
    job = _job_in(machine, jobs.JobState.BLOCKED, cause=_block().cause)

    with pytest.raises(JobBlocked) as caught:
        jobs.raise_for_state(job)

    assert caught.value.cause == job.cause


@pytest.mark.parametrize("state", [jobs.JobState.FAILED, jobs.JobState.CANCELLED])
def test_a_job_closed_with_a_cause_raises_that_cause_and_is_not_called_blocked(
    machine, state
):
    """The two are different answers. ``failed`` sends a person to look at what
    broke, ``blocked`` sends them to their account, and a closed job reported as
    blocked would send them to the wrong place."""
    cause = refuse("source-missing", "it is gone", origin=("test",)).cause
    job = _job_in(machine, state, cause=cause)

    with pytest.raises(CratekitError) as caught:
        jobs.raise_for_state(job)

    assert not isinstance(caught.value, JobBlocked)
    assert caught.value.cause == job.cause


@pytest.mark.parametrize("state", [jobs.JobState.QUEUED, jobs.JobState.SUCCEEDED])
def test_a_job_that_is_waiting_or_done_is_reported_and_not_refused(machine, state):
    """The queueing side of every verb reports a job that is merely queued through
    this same envelope, so the mapping must leave it alone."""
    jobs.raise_for_state(_job_in(machine, state))


def test_the_dispatcher_reads_the_blocked_type_as_the_blocked_outcome(machine, monkeypatch):
    """The other half of the mapping, asserted apart from any shell.

    ``resumable`` STAYS FALSE. That field names the gate run, which ``crate run``
    can continue, and a parked job continues through its verb with the job id.
    """
    monkeypatch.setattr(handlers, "resolve", lambda _key: parks)
    job = queued(machine, "master", ("one",))

    code, envelope = resumed(job)

    assert envelope["outcome"] == str(Outcome.BLOCKED), envelope
    assert code == int(_block().cause.code), envelope
    assert envelope["resumable"] is False, envelope


# ═══════════════════════════════════════════════════════════════════════════
# The population, driven
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("key", QUEUED_KEYS)
def test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero(
    machine, monkeypatch, key
):
    """R-290 over the whole population, through each verb's own argv."""
    monkeypatch.setattr(handlers, "resolve", lambda _key: parks)
    job = queued(machine, key, ("one",))

    code, envelope = resumed(job)

    assert job_of(job.job_id).state is jobs.JobState.BLOCKED, envelope
    assert envelope["outcome"] == str(Outcome.BLOCKED), envelope
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "provider-blocked", envelope


@pytest.mark.parametrize("key", QUEUED_KEYS)
def test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked(
    machine, monkeypatch, key
):
    """A blocked job is open, so the second ask drives it again, and a provider
    still refusing must read as blocked again rather than as a report."""
    monkeypatch.setattr(handlers, "resolve", lambda _key: parks)
    job = queued(machine, key, ("one",))
    resumed(job)

    code, envelope = resumed(job_of(job.job_id))

    assert envelope["outcome"] == str(Outcome.BLOCKED), envelope
    assert code != int(ExitCode.OK), envelope


@pytest.mark.parametrize("key", QUEUED_KEYS)
def test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero(
    machine, monkeypatch, key
):
    """R-225 over the whole population. ``drive`` raises only when EVERY item
    failed, so this is the ending only the shell can refuse."""
    monkeypatch.setattr(handlers, "resolve", lambda _key: fails_the_second)
    job = queued(machine, key, ("one", "two"))

    code, envelope = resumed(job)

    assert job_of(job.job_id).state is jobs.JobState.FAILED, envelope
    assert envelope["outcome"] == str(Outcome.FAILED), envelope
    assert code != int(ExitCode.OK), envelope


@pytest.mark.parametrize("key", QUEUED_KEYS)
def test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked(
    machine, monkeypatch, key
):
    """The placement ``backup`` paid for. A job failed on entry is not open, so
    the drive is skipped, and a check inside that branch is skipped with it."""
    monkeypatch.setattr(handlers, "resolve", lambda _key: fails_the_second)
    job = queued(machine, key, ("one", "two"))
    resumed(job)

    code, envelope = resumed(job_of(job.job_id))

    assert envelope["outcome"] == str(Outcome.FAILED), envelope
    assert code != int(ExitCode.OK), envelope


def test_the_tables_name_only_keys_that_are_bound():
    """A key unbound or renamed leaves its exemption behind otherwise, and an
    exemption nothing matches reads as coverage."""
    assert set(DRIVEN_ELSEWHERE) <= set(handlers.HANDLERS)
    assert set(PAYLOADS) <= set(handlers.HANDLERS)
    for where in DRIVEN_ELSEWHERE.values():
        path, _, name = where.partition("::")
        source = (SRC.parents[1] / path).read_text()
        assert f"def {name}(" in source, f"{where} is named here and does not exist"


# ═══════════════════════════════════════════════════════════════════════════
# The population, read
# ═══════════════════════════════════════════════════════════════════════════


def _functions(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def _calls(function: ast.AST, attribute: str) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == attribute
    ]


def _shells() -> list[tuple[Path, ast.FunctionDef]]:
    """Every function outside the driver's own two modules that runs a job."""
    own = {SRC / "cli" / "__init__.py", SRC / "cli" / "handlers.py"}
    found = []
    for path in sorted(SRC.rglob("*.py")):
        if path in own:
            continue
        for function in _functions(ast.parse(path.read_text())):
            if _calls(function, "run_job"):
                found.append((path, function))
    return found


def test_every_function_that_drives_a_job_maps_its_ending_afterwards():
    """The static half, for the verb the driven half cannot reach.

    A shell whose resume refuses on a precondition this file does not build, as
    ``adopt apply`` does, is invisible to the driven tests. It is not invisible
    here. AFTER, by line, because a check placed before the drive reads the state
    the job had on entry.
    """
    shells = _shells()
    assert len(shells) >= 13, "the walk stopped finding the shells it exists to read"
    for path, function in shells:
        drives = max(call.lineno for call in _calls(function, "run_job"))
        mapped = [call.lineno for call in _calls(function, "raise_for_state")]
        assert mapped and max(mapped) > drives, (
            f"{path.relative_to(SRC)}:{function.lineno} {function.name} drives a job "
            f"and never calls jobs.raise_for_state after it, so a parked or half "
            f"failed job leaves through a normal envelope and exits 0"
        )


def test_the_mapping_sits_outside_the_branch_that_drives():
    """``if job.is_open(): drive; check`` answers a failed job once and exits 0 for
    ever after. The call must not share the drive's enclosing ``if``."""
    for path, function in _shells():
        for branch in ast.walk(function):
            if not isinstance(branch, ast.If) or not _calls(branch, "run_job"):
                continue
            if "is_open" not in ast.unparse(branch.test):
                continue
            inside = {call.lineno for call in _calls(branch, "raise_for_state")}
            outside = {call.lineno for call in _calls(function, "raise_for_state")} - inside
            assert outside, (
                f"{path.relative_to(SRC)}:{function.lineno} {function.name} maps the "
                f"ending only inside its is_open branch"
            )


def test_no_shell_keeps_a_hand_rolled_copy_of_the_mapping():
    """The copy is what R-290 was. It could not know about a state added after it
    was written, and ten of them were wrong at once."""
    offenders = []
    for path in sorted(SRC.rglob("*.py")):
        if path == SRC / "core" / "jobs.py":
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, ast.Raise) or node.exc is None:
                continue
            if ast.unparse(node.exc).replace(" ", "") == "CratekitError(job.cause)":
                offenders.append(f"{path.relative_to(SRC)}:{node.lineno}")
    assert offenders == []
