"""The write layer's row repair scenarios: rekordbox's defaults filled behind a gate (U302).

`crate repair rows` plans every live row that lacks one of rekordbox's own
defaults or carries a file id the binding numbered at random, stops at its
explicit gate, and once the gate is answered fills the defaults and gives each
such row its file's inode inside one guarded database session. On the repair
suite's own library: its disposable database with two rows a landing left bare
beside the rows the repair must leave alone, and the volume's inode bound
pinned under the binding's range.

THE TWO LANDED ROWS CARRY A FILE ID OF ZERO HERE, which the repair leaves
alone, so the plan fills defaults and renumbers nothing. A renumber's target is
the file's inode and the plan's digest covers it; `compare` pairs one
capture's inode with the other's where the number stands whole, but no pin
reaches a hash of it, so two captures of one tree would differ in every digest
and run record. The row naming no file keeps its random id either way, and the
plan still says so.

A file of its own beside ``write.py``, because the repair suite and the
routing suite that file borrows from each call their acknowledged machine
``acknowledged``, and one file can hold one fixture of a name.
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
