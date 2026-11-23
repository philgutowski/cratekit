"""A session's own snapshot restored, the plan first and then the database (U300).

`crate restore run SESSION` stops at its gate, walks the plan with `--dry-run`,
then puts the captured database back, on the restore suite's library.
"""

from __future__ import annotations

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from tests.test_restore import acknowledge, completed_session
from tests.test_restore import cfg as cfg  # noqa: PLC0414
from tests.test_restore_cli import CONFIRM
from tests.test_restore_cli import _nothing_is_running as _nothing_is_running  # noqa: PLC0414
from tests.test_restore_cli import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_restore_cli import installed as installed  # noqa: PLC0414

OK = int(ExitCode.OK)
DECISION = int(ExitCode.DECISION_REQUIRED)


def test_a_session_snapshot_restored(stage, installed):
    acknowledge(installed)
    record, _captured = completed_session(installed)
    config.state_path("rekordbox_db", installed).write_bytes(b"database, generation two")
    verb = ("restore", "run", record.session_id)

    assert stage.crate(*verb, "--dry-run").code == DECISION
    dry = stage.json(*verb, "--dry-run")
    assert dry.code == DECISION, dry.stdout
    assert stage.decide(dry.envelope["run_id"], CONFIRM, "restore").code == OK
    walked = stage.json("--run", dry.envelope["run_id"], *verb, "--dry-run")
    assert walked.code == OK, walked.stdout

    refused = stage.json(*verb)
    assert refused.code == DECISION, refused.stdout
    assert stage.decide(refused.envelope["run_id"], CONFIRM, "restore").code == OK
    restored = stage.json("--run", refused.envelope["run_id"], *verb)
    assert restored.code == OK, restored.stdout
    stage.crate("restore", "list")
