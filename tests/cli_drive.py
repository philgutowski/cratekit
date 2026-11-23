"""Driving a verb through the REAL dispatcher, and answering R34's two acts.

Shared by three suites, since ``approve_and_queue`` encodes a contract: an
explicit gate is answered by a separate recorded act, never inline. ``cli.run``
in process, so a provider seam can be substituted.

Not a test module: pytest does not collect it.
"""

from __future__ import annotations

import io
import json

from cratekit import cli
from cratekit.cli import output
from cratekit.core.exit_codes import ExitCode


def drive(argv: list[str]) -> tuple[int, dict]:
    """Run one invocation, VALIDATE its envelope, and return the code and payload.

    Nothing in the dispatcher validates what a verb emitted: U51 shipped an
    undeclared ``outbound`` key in ``job_state/1`` with the suite green. So every
    verb these suites drive is checked against its ``output_schema`` here.
    """
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    document = json.loads(out.getvalue() or "{}")
    if document:
        assert output.envelope_problems(document) == [], document
    return code, document


def approve_and_queue(verb: list[str], gate: str) -> tuple[str, str]:
    """R34's two acts, then the queueing drive. Returns (gate run, job id).

    The gate refuses with nothing recorded, a second invocation records the
    decision with an actor, and only the third, naming that run, queues; never
    ``-d`` inline, which the contract forbids.
    """
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == gate
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, gate, detail["options"][0], "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, queued = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), queued
    return run_id, queued["data"]["job_id"]


def drive_human(argv: list[str]) -> tuple[int, str]:
    """Run one invocation in the DEFAULT output mode and return what a person reads.

    ``drive`` requests json, so a verb could keep a green suite over a human
    answer saying only ``ok`` (R-378, R-678). Success goes to stdout, a refusal
    to stderr; whichever holds text is the answer.
    """
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(list(argv), stdout=out, stderr=err)
    return code, out.getvalue() or err.getvalue()


__all__ = ["approve_and_queue", "drive", "drive_human"]
