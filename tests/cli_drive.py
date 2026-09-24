"""Driving a verb through the REAL dispatcher, and answering R34's two acts.

Three suites want the same two helpers, and before this module they were typed
out three times. That matters more than the line count: ``approve_and_queue``
encodes a CONTRACT, that an explicit gate is answered by a separate recorded act
and never inline, and a copy of a contract is a copy that can quietly drift into
answering it the easy way.

``cli.run`` in process rather than a subprocess, deliberately. A verb driven out
of process cannot have its provider seam substituted, which every outbound test
needs, and the property under test in all three suites is the dispatcher's rather
than the operating system's.

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

    THE VALIDATION IS THE POINT OF PUTTING THIS IN ONE PLACE. Every verb declares
    an ``output_schema`` and ``cli.output`` closes each declared surface with
    ``additionalProperties: false``, but nothing in the dispatcher validates what
    a verb actually emitted. U51 shipped an undeclared ``outbound`` key on two
    verbs' ``job_state/1`` payload and the whole suite stayed green, because the
    schema fingerprint hashes the DECLARED fields and the golden envelope is a
    hand written literal. ``tests/test_master_cli.py`` had this assertion inside
    its own private driver, where it guarded one verb.

    Here it guards every verb any of these suites drives, so the next undeclared
    field fails in the suite rather than in somebody's consumer.
    """
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    document = json.loads(out.getvalue() or "{}")
    if document:
        assert output.envelope_problems(document) == [], document
    return code, document


def approve_and_queue(verb: list[str], gate: str) -> tuple[str, str]:
    """R34's two acts, then the queueing drive. Returns (gate run, job id).

    THREE INVOCATIONS AND NOT ONE. The first meets the gate with nothing
    recorded and must refuse. The second records the decision with an actor,
    which is the separate deliberate act R34 requires. Only the third, naming
    that run, queues. A helper that answered the gate inline with ``-d`` would
    be asserting that the contract can be met by typing one more flag on the
    command that discovered it, which is the thing the contract forbids.
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

    ``drive`` always requests json, which is why a verb can keep a green suite
    over a human answer that says only ``ok`` and a run id (R-378, R-678). A
    success is written to standard output and a refusal to standard error, so
    whichever one holds text is the answer.
    """
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(list(argv), stdout=out, stderr=err)
    return code, out.getvalue() or err.getvalue()


__all__ = ["approve_and_queue", "drive", "drive_human"]
