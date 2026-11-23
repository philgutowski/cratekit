"""The write layer's row repair scenarios: rekordbox's defaults filled behind a gate (U302).

`crate repair rows` fills rekordbox's defaults behind its gate in one guarded
session. The two landed rows carry a file id of zero, so nothing is renumbered:
an inode reaches the plan's digest, which no pin covers. Its own file because
both suites name ``acknowledged``.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_repair_rows import FILE_ID, GATE, VERB, _sql, build
from tests.test_repair_rows import _bound as _bound  # noqa: PLC0414
from tests.test_repair_rows import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_repair_rows import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_repair_rows import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_repair_rows import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_repair_rows import machine as machine  # noqa: PLC0414

OK = int(ExitCode.OK)


def _built_with_no_inode_to_write(cfg) -> None:
    """The suite's library, its two landed rows' file ids set to zero (see above)."""
    build(cfg)
    _sql(cfg, f"UPDATE djmdContent SET {FILE_ID} = 0 WHERE ID IN ('101', '102')")


def test_bare_rows_given_their_defaults_behind_the_gate(stage, acknowledged):
    _built_with_no_inode_to_write(acknowledged)

    # The plan as a person reads it, then as the envelope the two acts answer.
    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    assert refused.envelope["cause"]["detail"]["shown"]["count"] == 2
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    written = stage.json("--run", run_id, *VERB)
    assert written.code == OK, written.stdout
    assert written.envelope["data"]["totals"]["written"] == 2
    assert written.envelope["data"]["totals"]["renumbered"] == 0
    # Ask again: every live row is whole, so the gate offers nothing to fill.
    stage.crate(*VERB)


def test_an_inline_answer_is_refused_and_nothing_is_filled(stage, acknowledged):
    """The gate is explicit, so an answer typed on the command still stops at it."""
    _built_with_no_inode_to_write(acknowledged)
    refused = stage.crate("-d", f"{GATE}=apply", *VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout


def test_without_the_acknowledgment_the_repair_refuses_before_its_gate(stage, machine):
    build(machine)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.ACK_REQUIRED), refused.stdout
