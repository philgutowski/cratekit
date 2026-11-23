"""R-290 and R-225: how a job ended decides how its verb exits, in every queued verb.

A parked or failed job must not leave through a normal envelope that exits 0.
The population is ``handlers.HANDLERS``, so a verb bound later is covered, and
every driven case asserts the job's state, since a precondition refusal also
exits non zero.
"""

from __future__ import annotations

import ast
import dataclasses
import functools
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

#: Keys whose parked test lives in another suite, whose verb needs a machine this
#: file does not build; the guard below keeps the table from outliving the reason.
DRIVEN_ELSEWHERE = {
    "adopt.apply": "tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero",
    # R-758: it answers its gate from the job's frozen plan.
    "adopt.move": "tests/test_adopt_move.py::test_a_parked_move_leaves_blocked_and_non_zero",
}

#: What each verb's argv builder reads off the frozen payload; no file named exists.
PAYLOADS: dict[str, dict[str, object]] = {
    "master": {"source": "set.wav"},
    "rebuild": {"actor": "a-person"},
    # U219: a resort refuses a job that froze no adds, so an empty plan is frozen.
    "route.resort": {"adds": []},
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
    """The worker's answer that the run must stop."""
    raise jobs.Parked(_block().cause)


def fails_the_second(job, item, cfg):
    """One item completes and one does not, so ``drive`` returns with the job failed."""
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
    """Drive the verb's own resume command line, answering its gate if it has one (R34)."""
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
    """A blocked row with no cause, which only another writer makes, is no success."""
    job = dataclasses.replace(
        _job_in(machine, jobs.JobState.BLOCKED, cause=_block().cause), cause=None
    )

    with pytest.raises(JobBlocked) as caught:
        jobs.raise_for_state(job)

    # The type too, since a plain refusal would read ``failed`` over a blocked row.
    assert caught.value.cause.reason == "internal-error"
    assert job.job_id in caught.value.cause.message


def test_a_failed_job_raises_its_own_cause_as_neither_carried_type(machine):
    """A failed job is not reported as blocked, which would send a person to their account."""
    cause = refuse("source-missing", "it is gone", origin=("test",)).cause
    job = _job_in(machine, jobs.JobState.FAILED, cause=cause)

    with pytest.raises(CratekitError) as caught:
        jobs.raise_for_state(job)

    assert type(caught.value) is CratekitError
    assert caught.value.cause == job.cause


def test_a_cancelled_job_raises_the_cancelled_type_carrying_its_own_cause(machine):
    """A person who stopped a run is told it was cancelled, not that it broke."""
    with jobs.open_store() as store:
        job = jobs.cancel(store, queued(machine, "master", ("one",)).job_id)

    with pytest.raises(JobCancelled) as caught:
        jobs.raise_for_state(job)

    assert caught.value.cause == job.cause


@pytest.mark.parametrize("state", [jobs.JobState.QUEUED, jobs.JobState.SUCCEEDED])
def test_a_job_that_is_waiting_or_done_is_reported_and_not_refused(machine, state):
    """A merely queued job is reported through this same envelope."""
    jobs.raise_for_state(_job_in(machine, state))


def test_the_dispatcher_reads_the_blocked_type_as_the_blocked_outcome(machine, monkeypatch):
    """``resumable`` stays false: a parked job continues through its verb, not ``crate run``."""
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
    """``resumable`` stays false even when the park's cause carries a gate code."""
    from cratekit.cli import gates

    monkeypatch.setattr(handlers, "resolve", lambda _key: _gate_coded_park)
    job = queued(machine, "master", ("one",))

    # Not ``resumed``, which would answer this code as a gate; ``master`` has none.
    code, envelope = drive(cli_jobs.argv_for(job))

    assert job_of(job.job_id).state is jobs.JobState.BLOCKED, envelope
    assert ExitCode(code) in gates.GATE_CODES, envelope
    assert envelope["outcome"] == str(Outcome.BLOCKED), envelope
    assert envelope["resumable"] is False, envelope


@pytest.mark.parametrize("key", QUEUED_KEYS)
def test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero(machine, key):
    """A cancelled job is closed, so no worker runs and none is swapped in."""
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
    """A blocked job is open, so a second ask drives it again and reads blocked again."""
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
    """R-225 over the whole population; ``drive`` raises only when every item failed."""
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
    """A job failed on entry skips the drive, and any check inside that branch."""
    monkeypatch.setattr(handlers, "resolve", lambda _key: fails_the_second)
    job = queued(machine, key, ("one", "two"))
    resumed(job)

    code, envelope = resumed(job_of(job.job_id))

    assert envelope["outcome"] == str(Outcome.FAILED), envelope
    assert code != int(ExitCode.OK), envelope


def test_the_tables_name_only_keys_that_are_bound():
    """An exemption naming no bound key reads as coverage, so none may outlive its key."""
    assert set(DRIVEN_ELSEWHERE) <= set(handlers.HANDLERS)
    assert set(PAYLOADS) <= set(handlers.HANDLERS)
    for where in DRIVEN_ELSEWHERE.values():
        path, _, name = where.partition("::")
        source = (SRC.parents[1] / path).read_text()
        assert f"def {name}(" in source, f"{where} is named here and does not exist"


# ═══════════════════════════════════════════════════════════════════════════
# The population, read
# ═══════════════════════════════════════════════════════════════════════════


@functools.cache
def _parsed() -> tuple[tuple[Path, ast.Module], ...]:
    """Every source module parsed once, read only by the walks below."""
    return tuple((path, ast.parse(path.read_text())) for path in sorted(SRC.rglob("*.py")))


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
    """Every function outside the driver's two modules that runs a job, with the
    names its module declares as never returning."""
    own = {SRC / "cli" / "__init__.py", SRC / "cli" / "handlers.py"}
    found = []
    for path, module in _parsed():
        if path in own:
            continue
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
    """A statement that is the mapping call alone, by attribute or bare name (U298)."""
    if not (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)):
        return False
    callee = statement.value.func
    name = callee.attr if isinstance(callee, ast.Attribute) else getattr(callee, "id", "")
    return name == "raise_for_state"


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
    """The mapping as a plain statement, or ``backup``'s ``try`` holding only the call
    whose every handler raises, since one that falls through makes a normal envelope.
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

    Judged by control flow, not line number: walking out from the drive, no
    enclosing block may return before the mapping.
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
                # Inside the ``is_open`` branch is not enough: a failed job skips it.
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
    """The static half, reaching a verb the driven tests cannot, such as ``adopt apply``."""
    shells = _shells()
    # Eleven since U298, ``jobs.resumed`` among them by name.
    assert len(shells) >= 11, "the walk stopped finding the shells it exists to read"
    assert ("core/jobs.py", "resumed") in {
        (path.relative_to(SRC).as_posix(), function.name) for path, function, _ in shells
    }, "the shared tail of every resume is no longer one of the shells this guard reads"
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
    """A mapping after a return or in a skipped branch is refused, and a wrapped one
    accepted only while no handler can swallow what it raised."""
    reason = unmapped_reason(_shell(source), frozenset({"_raise_refusal"}))
    if expected is None:
        assert reason is None
    else:
        assert reason is not None and expected in reason, reason


def test_no_shell_keeps_a_hand_rolled_copy_of_the_mapping():
    """No shell keeps its own copy of the mapping (R-290), matched as a condition
    reading both ``is_open()`` and ``cause`` whatever the job is named."""
    offenders = []
    for path, module in _parsed():
        if path == SRC / "core" / "jobs.py":
            continue
        for node in ast.walk(module):
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

#: Refusals built from a cause with no exception in hand, so no type to keep.
#: ``sync`` raises the first queue refusal over the whole pass and drives no job.
NO_ERROR_IN_HAND = {
    "sync/cli.py": "compose",
    # U293: the night pass rebuilds its cause from the pass's JSON envelope.
    "cli/sync_night.py": "_ended",
}


def _is_a_replace(node: ast.expr) -> bool:
    return (
        isinstance(node, ast.Call)
        and ast.unparse(node.func) in {"replace", "dataclasses.replace"}
    )


def test_a_reworded_refusal_is_rebuilt_in_one_place_only():
    """``cause.rebuilt`` is the only rebuild: no ``CratekitError(replace(...))`` by
    hand, and no carried type constructed outside the mapping."""
    by_hand, constructed = [], []
    for path, module in _parsed():
        where = str(path.relative_to(SRC))
        if where == "core/cause.py":
            continue
        for function in _functions(module):
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
    """``Parked`` is not carried: only the two types the dispatcher reads are."""
    assert type(rebuilt(jobs.Parked(_block().cause), _block().cause)) is CratekitError
