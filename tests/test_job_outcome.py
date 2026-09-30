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
import dataclasses
from pathlib import Path

import pytest

from cratekit.cli import handlers
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs
from cratekit.core.cause import (
    CratekitError,
    JobBlocked,
    JobCancelled,
    Outcome,
    rebuilt,
    refuse,
)
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
    # R-758. It reads the backup acknowledgment before it looks at the job, and
    # its resume answers the gate from the plan the job froze, so it needs that
    # file's machine and a job its own verb queued.
    "adopt.move": "tests/test_adopt_move.py::test_a_parked_move_leaves_blocked_and_non_zero",
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


def test_a_blocked_job_recording_no_reason_is_still_not_a_success(machine):
    """``transition`` refuses to park without a cause, so this row was written by
    something other than the engine. The mapping must not read a missing reason
    as a missing problem, which is the first defect pattern METHOD lists."""
    job = dataclasses.replace(
        _job_in(machine, jobs.JobState.BLOCKED, cause=_block().cause), cause=None
    )

    with pytest.raises(JobBlocked) as caught:
        jobs.raise_for_state(job)

    # THE TYPE AS WELL AS THE REASON, which the first version of this test did not
    # pin. A plain refusal here reads ``failed`` in the envelope over a row whose
    # state reads ``blocked``, the disagreement the type exists to remove.
    assert caught.value.cause.reason == "internal-error"
    assert job.job_id in caught.value.cause.message


def test_a_failed_job_raises_its_own_cause_as_neither_carried_type(machine):
    """The answers differ. ``failed`` sends a person to look at what broke,
    ``blocked`` sends them to their account, and a closed job reported as blocked
    would send them to the wrong place."""
    cause = refuse("source-missing", "it is gone", origin=("test",)).cause
    job = _job_in(machine, jobs.JobState.FAILED, cause=cause)

    with pytest.raises(CratekitError) as caught:
        jobs.raise_for_state(job)

    assert type(caught.value) is CratekitError
    assert caught.value.cause == job.cause


def test_a_cancelled_job_raises_the_cancelled_type_carrying_its_own_cause(machine):
    """``Outcome.CANCELLED`` was declared and nothing produced it, which is the
    state ``Outcome.BLOCKED`` was in when R-290 was filed. A person who stopped a
    run is not told it broke."""
    with jobs.open_store() as store:
        job = jobs.cancel(store, queued(machine, "master", ("one",)).job_id)

    with pytest.raises(JobCancelled) as caught:
        jobs.raise_for_state(job)

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


def _gate_coded_park(job, item, cfg):
    """A worker parking on a cause whose code is one of the gate codes."""
    raise jobs.Parked(
        refuse(
            "decision-required",
            "an acknowledgment this run needs was never recorded",
            origin=("test",),
        ).cause
    )


def test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run(
    machine, monkeypatch
):
    """``resumable`` was derived from the cause's code alone, so the claim above
    held only while no worker parked on a gate coded cause, and ``transition``'s
    own text names a missing acknowledgment as a reason to park. The code must be
    a gate code here or this drives nothing: asserted, not assumed."""
    from cratekit.cli import gates

    monkeypatch.setattr(handlers, "resolve", lambda _key: _gate_coded_park)
    job = queued(machine, "master", ("one",))

    # NOT ``resumed``, which reads this very exit code as a gate to answer.
    # ``master`` has no gate, so the code can only have come from the park.
    code, envelope = drive(cli_jobs.argv_for(job))

    assert job_of(job.job_id).state is jobs.JobState.BLOCKED, envelope
    assert ExitCode(code) in gates.GATE_CODES, envelope
    assert envelope["outcome"] == str(Outcome.BLOCKED), envelope
    assert envelope["resumable"] is False, envelope


@pytest.mark.parametrize("key", QUEUED_KEYS)
def test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero(machine, key):
    """The third ending, over the whole population. A cancelled job is closed, so
    no worker runs and none is swapped in."""
    with jobs.open_store() as store:
        job = jobs.cancel(store, queued(machine, key, ("one",)).job_id)

    code, envelope = resumed(job)

    assert job_of(job.job_id).state is jobs.JobState.CANCELLED, envelope
    assert envelope["outcome"] == str(Outcome.CANCELLED), envelope
    assert code == int(ExitCode.INTERRUPTED), envelope
    assert envelope["cause"]["reason"] == "cancelled", envelope


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


def _shells() -> list[tuple[Path, ast.FunctionDef, frozenset[str]]]:
    """Every function outside the driver's own two modules that runs a job, with
    the names its module declares as never returning."""
    own = {SRC / "cli" / "__init__.py", SRC / "cli" / "handlers.py"}
    found = []
    for path in sorted(SRC.rglob("*.py")):
        if path in own:
            continue
        module = ast.parse(path.read_text())
        for function in _functions(module):
            if _calls(function, "run_job"):
                found.append((path, function, _never_returns(module)))
    return found


def _blocks(statement: ast.stmt) -> list[list[ast.stmt]]:
    """Every statement list one compound statement owns."""
    found = []
    for name in ("body", "orelse", "finalbody"):
        block = getattr(statement, name, None)
        if isinstance(block, list) and block and isinstance(block[0], ast.stmt):
            found.append(block)
    for handler in getattr(statement, "handlers", []):
        found.append(handler.body)
    for case in getattr(statement, "cases", []):
        found.append(case.body)
    return found


def _path_to(block: list[ast.stmt], target: ast.AST) -> list[tuple[list[ast.stmt], int]] | None:
    """The chain of (statement list, index) from ``block`` down to ``target``."""
    for index, statement in enumerate(block):
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        for inner in _blocks(statement):
            below = _path_to(inner, target)
            if below is not None:
                return [(block, index), *below]
        if any(node is target for node in ast.walk(statement)):
            return [(block, index)]
    return None


def _is_the_call(statement: ast.stmt) -> bool:
    return (
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Call)
        and isinstance(statement.value.func, ast.Attribute)
        and statement.value.func.attr == "raise_for_state"
    )


def _never_returns(module: ast.AST) -> frozenset[str]:
    """The module's own functions annotated ``-> NoReturn``, by name."""
    return frozenset(
        function.name
        for function in _functions(module)
        if function.returns is not None and ast.unparse(function.returns) == "NoReturn"
    )


def _leaves(handler: ast.ExceptHandler, never_returns: frozenset[str]) -> bool:
    """Whether a handler's last act is to raise, itself or through a helper."""
    last = handler.body[-1]
    if isinstance(last, ast.Raise):
        return True
    return (
        isinstance(last, ast.Expr)
        and isinstance(last.value, ast.Call)
        and isinstance(last.value.func, ast.Name)
        and last.value.func.id in never_returns
    )


def _is_the_mapping(statement: ast.stmt, never_returns: frozenset[str] = frozenset()) -> bool:
    """The mapping as a plain statement, or wrapped by a verb that words its exit.

    THE SECOND SHAPE IS ``backup``'s. Its refusals leave through a helper that
    adds the rehearsal sentence, so the mapping sits alone in a ``try`` whose
    handler re-raises what it caught, extended. That is still the mapping ONLY IF
    NO HANDLER CAN SWALLOW IT: a handler that falls through turns the refusal
    back into the normal envelope this file exists to forbid. So every handler
    must end in a ``raise`` or in a call to a function the same module annotates
    ``NoReturn``, and the ``try`` may carry nothing but the call.
    """
    if _is_the_call(statement):
        return True
    return (
        isinstance(statement, ast.Try)
        and len(statement.body) == 1
        and _is_the_call(statement.body[0])
        and bool(statement.handlers)
        and not statement.orelse
        and not statement.finalbody
        and all(_leaves(handler, never_returns) for handler in statement.handlers)
    )


def unmapped_reason(
    function: ast.FunctionDef, never_returns: frozenset[str] = frozenset()
) -> str | None:
    """Why this function's drive can reach a report unmapped, or None.

    BY CONTROL FLOW AND NOT BY LINE NUMBER, which is what the first version of
    this guard compared and what the review drove a hole through: a mapping call
    in a later ``else``, or after a ``return`` inside the driving branch, sits on
    a greater line and is never reached. The rule here is the shape every shell
    actually has. Walking OUT from the drive, no enclosing block may return
    before the mapping is met, and the mapping must be a plain statement of one
    of those enclosing blocks, after the drive.
    """
    for call in _calls(function, "run_job"):
        path = _path_to(function.body, call)
        assert path is not None
        mapped = False
        for depth, (block, index) in enumerate(reversed(path)):
            for later in block[index + 1 :]:
                if _is_the_mapping(later, never_returns):
                    mapped = True
                    break
                if any(isinstance(node, ast.Return) for node in ast.walk(later)):
                    return f"returns at line {later.lineno} before the mapping is reached"
            if mapped:
                # INSIDE THE DRIVING BRANCH IS NOT ENOUGH. ``depth`` zero is the
                # block the drive itself sits in, and when that block is the
                # ``is_open`` branch a job already failed on entry skips it whole.
                owner = path[-depth - 2] if depth + 2 <= len(path) else None
                if depth == 0 and owner is not None:
                    holder = owner[0][owner[1]]
                    if isinstance(holder, ast.If) and "is_open" in ast.unparse(holder.test):
                        return "maps the ending only inside its is_open branch"
                break
        if not mapped:
            return "never calls jobs.raise_for_state on the path out of the drive"
    return None


def test_every_function_that_drives_a_job_maps_its_ending_afterwards():
    """The static half, for the verb the driven half cannot reach.

    A shell whose resume refuses on a precondition this file does not build, as
    ``adopt apply`` does, is invisible to the driven tests. It is not invisible
    here.
    """
    shells = _shells()
    assert len(shells) >= 13, "the walk stopped finding the shells it exists to read"
    for path, function, never_returns in shells:
        reason = unmapped_reason(function, never_returns)
        assert reason is None, (
            f"{path.relative_to(SRC)}:{function.lineno} {function.name} {reason}, so a "
            f"parked or half failed job leaves through a normal envelope and exits 0"
        )


def _shell(source: str) -> ast.FunctionDef:
    return next(_functions(ast.parse(source)))


_WORDED = (
    "def resume(ctx, store, job):\n"
    "    if job.is_open():\n"
    "        ctx.run_job(store, job)\n"
    "    try:\n"
    "        jobs.raise_for_state(job)\n"
    "    except CratekitError as exc:\n"
    "        {handler}\n"
    "    return ctx.envelope(data={{}})\n"
)


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            "def resume(ctx, store, job):\n"
            "    if job.is_open():\n"
            "        ctx.run_job(store, job)\n"
            "    jobs.raise_for_state(job)\n"
            "    return ctx.envelope(data={})\n",
            None,
        ),
        (
            "def resume(ctx, store, job):\n"
            "    if job.is_open():\n"
            "        ctx.run_job(store, job)\n"
            "    return ctx.envelope(data={})\n",
            "returns at line 4",
        ),
        (
            "def resume(ctx, store, job):\n"
            "    if job.is_open():\n"
            "        ctx.run_job(store, job)\n"
            "        jobs.raise_for_state(job)\n"
            "    return ctx.envelope(data={})\n",
            "only inside its is_open branch",
        ),
        (
            "def resume(ctx, store, job):\n"
            "    if job.is_open():\n"
            "        ctx.run_job(store, job)\n"
            "        return ctx.envelope(data={})\n"
            "    jobs.raise_for_state(job)\n"
            "    return ctx.envelope(data={})\n",
            "returns at line 4",
        ),
        (
            "def resume(ctx, store, job):\n"
            "    if job.is_open():\n"
            "        ctx.run_job(store, job)\n"
            "    else:\n"
            "        jobs.raise_for_state(job)\n"
            "    return ctx.envelope(data={})\n",
            "returns at line 6",
        ),
        (_WORDED.format(handler="raise extended(exc) from exc"), None),
        (_WORDED.format(handler="_raise_refusal(exc, job)"), None),
        (_WORDED.format(handler="_log_and_carry_on(exc, job)"), "returns at line 8"),
        (_WORDED.format(handler="pass"), "returns at line 8"),
    ],
)
def test_the_static_guard_refuses_the_shapes_it_exists_for(source, expected):
    """The guard's own teeth, because a guard that reads source is only as good as
    the shapes it has been shown. The fourth and fifth are the review's: a later
    line is not a later point in the run. The last four are ``backup``'s exit, a
    mapping wrapped so the verb can word its refusal, which holds only while no
    handler can swallow what the mapping raised."""
    reason = unmapped_reason(_shell(source), frozenset({"_raise_refusal"}))
    if expected is None:
        assert reason is None
    else:
        assert reason is not None and expected in reason, reason


def test_no_shell_keeps_a_hand_rolled_copy_of_the_mapping():
    """The copy is what R-290 was. It could not know about a state added after it
    was written, and ten of them were wrong at once.

    THE PREDICATE IS MATCHED, NOT ONE SPELLING OF THE RAISE. Shells name their job
    ``job``, ``queued`` and ``current``, so a guard matching the text of one raise
    passes every other name. What all copies share is a condition reading both
    ``is_open()`` and ``cause``.
    """
    offenders = []
    for path in sorted(SRC.rglob("*.py")):
        if path == SRC / "core" / "jobs.py":
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, (ast.If, ast.IfExp, ast.While)):
                continue
            names = {
                inner.attr for inner in ast.walk(node.test) if isinstance(inner, ast.Attribute)
            }
            if {"is_open", "cause"} <= names:
                offenders.append(f"{path.relative_to(SRC)}:{node.lineno}")
    assert offenders == []


# ═══════════════════════════════════════════════════════════════════════════
# The hop between a shell and the dispatcher
# ═══════════════════════════════════════════════════════════════════════════

#: A refusal built from a cause where NO EXCEPTION IS IN HAND, so there is no type
#: to keep. ``sync`` collects the causes of sources that refused at the queue and
#: raises the first one over the whole pass. It drives no job.
NO_ERROR_IN_HAND = {"sync/cli.py": "compose"}


def _is_a_replace(node: ast.expr) -> bool:
    return (
        isinstance(node, ast.Call)
        and ast.unparse(node.func) in {"replace", "dataclasses.replace"}
    )


def test_a_reworded_refusal_is_rebuilt_in_one_place_only():
    """The blocked and cancelled bits ride the exception's TYPE, so every hop that
    rewords a refusal on its way out has to keep it, and two shells in a row got
    that wrong by building ``CratekitError(replace(...))``. ``cause.rebuilt`` owns
    the choice now. This refuses the two ways of going round it: the rebuild
    spelled by hand, and either carried type constructed outside the mapping."""
    by_hand, constructed = [], []
    for path in sorted(SRC.rglob("*.py")):
        where = str(path.relative_to(SRC))
        if where == "core/cause.py":
            continue
        for function in _functions(ast.parse(path.read_text())):
            for node in ast.walk(function):
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
                    continue
                if (
                    node.func.id == "CratekitError"
                    and node.args
                    and _is_a_replace(node.args[0])
                    and NO_ERROR_IN_HAND.get(where) != function.name
                ):
                    by_hand.append(f"{where}:{node.lineno}")
                if node.func.id in {"JobBlocked", "JobCancelled"} and where != "core/jobs.py":
                    constructed.append(f"{where}:{node.lineno}")
    assert by_hand == []
    assert constructed == []


def test_the_exemption_from_the_rebuild_rule_still_names_a_real_function():
    for where, name in NO_ERROR_IN_HAND.items():
        assert f"def {name}(" in (SRC / where).read_text(), f"{where} has no {name}"


@pytest.mark.parametrize("kind", [JobBlocked, JobCancelled, CratekitError])
def test_a_rebuilt_refusal_keeps_a_carried_type_and_takes_the_new_cause(kind):
    before, after = _block().cause, refuse("source-missing", "gone", origin=("test",)).cause

    again = rebuilt(kind(before), after)

    assert type(again) is kind
    assert again.cause == after


def test_a_rebuilt_refusal_of_any_other_type_is_the_plain_one():
    """``Parked`` takes a cause like the base type, and it is still not carried:
    only the two types the dispatcher reads are, and the docstring says why."""
    assert type(rebuilt(jobs.Parked(_block().cause), _block().cause)) is CratekitError
