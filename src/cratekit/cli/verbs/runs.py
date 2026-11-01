"""``crate run show`` and ``crate run decide``: a gate answered from elsewhere.

These two verbs are what make R33 more than a flag. A decision supplied on the
command line only helps somebody who is sitting in front of the run that hit the
gate. The cases that actually matter are the other ones: a detached job parked
at a gate, a run that exited hours ago, a second person on the same library. All
of those need the decision to be state on the run rather than an argument to a
process that has already gone.

``run show`` is also where a pending human action surfaces. The source system
prints an instruction to import an XML in eleven different places and forgets it
immediately afterwards; the only run that records the state machine-readably is
the one orchestrator, and it is the only one that can tell whether the import
ever happened.
"""

from __future__ import annotations

import argparse
import dataclasses
import re
import sys
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

from cratekit.cli import gates, registry
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context


def build_show(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("run_id", help="the run to describe")
    parser.set_defaults(_handler=show)


def show(ctx: "Context") -> Envelope:
    state = gates.load(ctx.args.run_id)
    checks = [
        {
            "key": f"gate.{name}",
            "title": name,
            "status": "answered",
            "detail": f"{decision.option} (recorded by {decision.actor})",
            "remedy": None,
        }
        for name, decision in sorted(state.decisions.items())
    ]
    if state.open_gate:
        entry = registry.entry(state.verb)
        spec = next((g for g in entry.gates if g.name == state.open_gate), None)
        checks.append(
            {
                "key": f"gate.{state.open_gate}",
                "title": state.open_gate,
                "status": "open",
                "detail": ", ".join(spec.options) if spec else "",
                "remedy": str(Remedy.ANSWER_DECISION),
            }
        )

    data = {
        "checks": checks,
        "summary": {
            "run_id": state.run_id,
            "verb": state.verb,
            "created": state.created,
            "open_gate": state.open_gate,
        },
    }
    if state.pending is not None:
        # The envelope's own invariant, asserted in both directions by
        # ``output.envelope_problems``: a pending action means outcome pending
        # and status PENDING_HUMAN, so a caller reading either half of the result
        # reaches the same conclusion.
        return ctx.envelope(
            data=data,
            outcome=Outcome.PENDING,
            code=ExitCode.PENDING_HUMAN,
            pending=state.pending,
            resumable=True,
        )
    return ctx.envelope(data=data)


def build_decide(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("run_id", help="the run holding the gate")
    parser.add_argument("gate", help="the gate's stable name, as shown by run show")
    parser.add_argument("option", help="one of the gate's declared options")
    parser.add_argument(
        "--actor",
        default=None,
        help=(
            "who is making this decision; recorded with it (R34). Defaults to "
            "'cli' at a terminal and 'session' with none"
        ),
    )
    parser.add_argument(
        "--continue",
        dest="continue_run",
        action="store_true",
        help="then continue the verb that owns the run, with its own arguments and --run",
    )
    parser.set_defaults(_handler=decide)


#: Who answered when ``--actor`` is not given (U168): a person at a terminal,
#: or a session with none, which is how the 2026-10-09 rule tells them apart.
TERMINAL_ACTOR = "cli"
SESSION_ACTOR = "session"

#: The warning a continued run carries, naming the answer it continued on.
DECISION_RECORDED = "decision-recorded"


def _actor(given: str | None) -> tuple[str, str]:
    """Who the decision is recorded as, and why, in words."""
    if given is not None:
        return given, "given with --actor"
    if session.has_controlling_terminal():
        return TERMINAL_ACTOR, "a terminal, and no --actor"
    return SESSION_ACTOR, "no controlling terminal, and no --actor"


def decide(ctx: "Context") -> Envelope:
    state = gates.load(ctx.args.run_id)
    owner = registry.entry(state.verb)
    spec = next((g for g in owner.gates if g.name == ctx.args.gate), None)
    if spec is None:
        raise CratekitError(
            Cause(
                reason="decision-unknown-gate",
                message=(
                    f"{ctx.args.gate!r} is not a gate on {state.verb}; "
                    f"it declares {', '.join(g.name for g in owner.gates) or 'none'}"
                ),
                remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
                origin=("cli.verbs.runs",),
                detail={"run_id": state.run_id, "verb": state.verb},
            )
        )

    actor, why = _actor(ctx.args.actor)
    gates.record(state, spec, ctx.args.option, actor=actor)
    gates.save(state)
    if ctx.args.continue_run:
        return _continued(ctx, state, spec.name, actor=actor)
    return ctx.envelope(
        data={
            "checks": [
                {
                    "key": f"gate.{spec.name}",
                    "title": spec.name,
                    "status": "answered",
                    "detail": ctx.args.option,
                    "remedy": None,
                }
            ],
            "summary": {
                "run_id": state.run_id,
                "verb": state.verb,
                "gate": spec.name,
                "option": ctx.args.option,
                "actor": actor,
                "actor_because": why,
            },
        }
    )


def _continued(ctx: "Context", state: gates.RunState, gate: str, *, actor: str) -> Envelope:
    """Continue the verb that owns ``state`` with its recorded arguments, and answer as it did (U168).

    THE ANSWER IS RECORDED AND SAVED FIRST, so a continuation that refuses
    leaves the answer standing and the run continuable by hand. The verb runs
    in this process through the dispatcher's own path, and its envelope, exit
    code included, is the one this call answers, with a warning naming the
    answer it continued on. An explicit gate is untouched: its answer is still
    this second call, never a flag on the verb's own.
    """
    if state.argv is None:
        raise CratekitError(
            Cause(
                reason="run-not-continuable",
                message=(
                    f"the answer to {gate} was recorded, and run {state.run_id} keeps no "
                    f"command line to continue it with, since it was recorded before "
                    f"run decide could continue one; run the verb again yourself"
                ),
                remediation=Remediation(
                    steps=(f"crate --run {state.run_id} {state.verb.replace('.', ' ')} ...",),
                ),
                origin=("cli.verbs.runs",),
                detail={"run_id": state.run_id, "verb": state.verb, "gate": gate},
            )
        )
    from cratekit import cli

    envelope = cli.dispatch(["--run", state.run_id, *state.argv], stderr=sys.stderr)
    note = {
        "code": DECISION_RECORDED,
        "message": (
            f"{gate} answered {ctx.args.option} as {actor} on run {state.run_id}, "
            f"then {' '.join(state.argv)} continued"
        ),
    }
    return dataclasses.replace(envelope, warnings=(note, *envelope.warnings))


# ---------------------------------------------------------------------------
# crate run retire (U170)
# ---------------------------------------------------------------------------

#: ``--older-than``'s form, a whole number of days. Its ceiling is the one the
#: configured day count has, ``config.MAX_OPEN_GATE_STALE_DAYS``.
_AGE = re.compile(r"^([1-9][0-9]*)d$")


def older_than(text: str) -> timedelta:
    """``--older-than``: a positive whole number of days, written ``7d``.

    Days only, since the threshold it overrides is a day count and an hour
    would retire a gate a person opened this morning. A malformed value is
    the argument parser's refusal, which is what the usage code is for.
    """
    match = _AGE.match(text.strip())
    days = int(match.group(1)) if match else 0
    if not match or days > config.MAX_OPEN_GATE_STALE_DAYS:
        raise argparse.ArgumentTypeError(
            f"{text!r} is not an age; give a whole number of days from 1 to "
            f"{config.MAX_OPEN_GATE_STALE_DAYS}, such as 7d"
        )
    return timedelta(days=days)


def build_retire(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument(
        "--older-than",
        dest="older_than",
        type=older_than,
        default=None,
        metavar="DAYS",
        help=(
            "retire open gates idle for longer than this many days, such as 7d; "
            "defaults to reports.open_gate_stale_days"
        ),
    )
    parser.set_defaults(_handler=retire)


def old_gates(
    *, older_than: timedelta, now: datetime, skip: str | None = None
) -> tuple[list[gates.OldGate], list[str]]:
    """Every open gate idle past ``older_than``, and the records that could not be read.

    The records that could not be read are said rather than dropped, so a
    retirement that found nothing it could read is never reported as a
    library with nothing old in it. ``skip`` is the run asking.
    """
    found: list[gates.OldGate] = []
    unreadable: list[str] = []
    for path in sorted(gates.run_dir().glob("*.json")):
        if path.stem == skip:
            continue
        try:
            state = gates.load(path.stem)
        except CratekitError:
            unreadable.append(path.stem)
            continue
        old = gates.old_gate(state, path, older_than=older_than, now=now)
        if old is not None:
            found.append(old)
    return found, unreadable


def _days(age: timedelta) -> str:
    return f"{age.days}d"


def retire(ctx: "Context") -> Envelope:
    """Answer ``abort`` on every open gate idle past the threshold, after one confirm.

    THE ANSWER IS ALWAYS ``abort``, recorded as ``session``, whatever the gate,
    explicit ones included: a retirement says no on a person's behalf and
    never yes. The plan is every retirable gate but this run's own, shown by
    run, verb, gate and the date it went idle, and the confirm's digest is
    taken over it, so a gate that ages in or is resumed between the question
    and the answer makes the answer stale rather than wider. Nothing old is
    nothing to confirm, and the verb ends with no change and asks nothing.

    Each run is written as it is retired, so a retirement stopped part way
    keeps what it did, and ``crate run retire`` again plans what is left.
    """
    age = ctx.args.older_than
    if age is None:
        age = timedelta(days=config.load().reports.open_gate_stale_days)
    found, unreadable = old_gates(
        older_than=age, now=datetime.now(timezone.utc), skip=ctx.run.run_id
    )
    planned = [one for one in found if one.retirable]
    kept = [one for one in found if not one.retirable]
    checks = [_kept_check(one) for one in kept] + [
        {
            "key": f"run.{stem}",
            "title": "run record",
            "status": "unreadable",
            "detail": "this run's record could not be read, so its gate was not judged",
            "remedy": str(Remedy.REPORT_DEFECT),
        }
        for stem in unreadable
    ]
    summary: dict[str, Any] = {
        "older_than": _days(age),
        "retired": 0,
        "kept": len(kept),
        "unreadable": len(unreadable),
    }
    if not planned:
        return ctx.envelope(data={"checks": checks, "summary": summary}, outcome=Outcome.NO_OP)

    items = [one.item() for one in planned]
    plan = {"digest": digest_of(items), "count": len(items), "items": items}
    option = ctx.gate.require(
        ctx.entry.gates[0],
        plan=plan,
        context={"older_than": _days(age), "answer": gates.RETIRE_OPTION, "actor": SESSION_ACTOR},
    )
    if option != "apply":
        summary["declined"] = len(planned)
        return ctx.envelope(data={"checks": checks, "summary": summary}, outcome=Outcome.NO_OP)

    retired: list[dict[str, Any]] = []
    for one in planned:
        if _retire_one(one):
            retired.append(_retired_check(one))
        else:
            checks.append(_moved_check(one))
    summary["retired"] = len(retired)
    return ctx.envelope(
        data={"checks": retired + checks, "summary": summary},
        outcome=Outcome.OK if retired else Outcome.NO_OP,
    )


def _retire_one(one: gates.OldGate) -> bool:
    """Record ``abort`` on one planned gate, if it is still the run's open gate."""
    state = gates.load(one.run_id)
    if state.open_gate != one.gate:
        return False
    spec = next(g for g in registry.entry(state.verb).gates if g.name == one.gate)
    gates.record(state, spec, gates.RETIRE_OPTION, actor=SESSION_ACTOR)
    gates.save(state)
    return True


def _retired_check(one: gates.OldGate) -> dict[str, Any]:
    return {
        "key": f"gate.{one.run_id}.{one.gate}",
        "title": f"{one.verb} {one.gate}",
        "status": "retired",
        "detail": (
            f"answered {gates.RETIRE_OPTION} as {SESSION_ACTOR} on run {one.run_id}, "
            f"idle since {one.idle_since}"
        ),
        "remedy": None,
    }


def _kept_check(one: gates.OldGate) -> dict[str, Any]:
    return {
        "key": f"gate.{one.run_id}.{one.gate}",
        "title": f"{one.verb} {one.gate}",
        "status": "kept",
        "detail": f"left open on run {one.run_id}, because {one.kept}",
        "remedy": str(Remedy.ANSWER_DECISION),
    }


def _moved_check(one: gates.OldGate) -> dict[str, Any]:
    return {
        "key": f"gate.{one.run_id}.{one.gate}",
        "title": f"{one.verb} {one.gate}",
        "status": "moved",
        "detail": (
            f"run {one.run_id} no longer waits at {one.gate}, so nothing was "
            f"recorded on it; it was answered or resumed while this ran"
        ),
        "remedy": None,
    }
