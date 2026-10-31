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
import sys
from typing import TYPE_CHECKING

from cratekit.cli import gates, registry
from cratekit.cli.output import Envelope
from cratekit.core import session
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
                reason="decision-required",
                message=(
                    f"the answer to {gate} was recorded, and run {state.run_id} keeps no "
                    f"command line to continue it with, since it was recorded before "
                    f"run decide could continue one; run the verb again yourself"
                ),
                remediation=Remediation(
                    remedy=Remedy.ANSWER_DECISION,
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
