"""The write layer's probe scenarios: chosen values written into chosen rows (U302).

`crate repair link` plans ``--set row:column=value`` triples on the two probe
columns with how many rows share each value, then writes and reads them back
behind its gate. Its own file because ``write_rows.py`` names ``VERB`` and
``GATE`` for another verb.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_repair_link import GATE, HOUSE, ISRC, LINK, VERB, _sets, seed
from tests.test_repair_rows import _bound as _bound  # noqa: PLC0414
from tests.test_repair_rows import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_repair_rows import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_repair_rows import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_repair_rows import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_repair_rows import machine as machine  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_three_probe_values_written_behind_the_gate(stage, acknowledged):
    seed(acknowledged)
    argv = [*VERB, *_sets(f"101:{LINK}={HOUSE}", f"101:{ISRC}=", f"102:{ISRC}=")]

    assert stage.crate(*argv).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*argv)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    assert refused.envelope["cause"]["detail"]["shown"]["values to write"] == 3
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    written = stage.json("--run", run_id, *argv)
    assert written.code == OK, written.stdout
    assert written.envelope["data"]["totals"]["written"] == 3
    # Ask again: every row already holds its value, so the plan writes nothing.
    stage.crate(*argv)


def test_an_unknown_row_refuses_before_any_gate(stage, acknowledged):
    seed(acknowledged)
    refused = stage.json(*VERB, *_sets(f"999:{LINK}={HOUSE}"))
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout


def test_without_the_acknowledgment_the_probe_refuses_before_its_gate(stage, machine):
    seed(machine)
    refused = stage.json(*VERB, *_sets(f"101:{LINK}={HOUSE}"))
    assert refused.code == int(ExitCode.ACK_REQUIRED), refused.stdout
