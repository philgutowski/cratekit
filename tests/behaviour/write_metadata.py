"""The write layer's My Tag scenarios: vocal tags written from a file's vocal reading (U302).

`crate metadata mytags-vocals` reads each collection row's file for its vocal
level and gender, plans the My Tags those earn above the calibrated cut, and
with ``--apply`` writes them inside one guarded database session, never a
content column. On the metadata suite's own library: a disposable database
with a tag category and one row naming a file the encoder synthesized, tagged
as a voiced male track. Its refusal is a vocal calibration that cannot be read,
which stops the apply with no My Tag written.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_metadata_cli import _vocal_calibration
from tests.test_metadata_cli import ready as ready  # noqa: PLC0414
from tests.test_metadata_cli import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)
VERB = ("metadata", "mytags-vocals")


def test_vocal_tags_planned_then_written_then_already_there(stage, ready):
    planned = stage.json(*VERB)
    assert planned.code == OK, planned.stdout
    assert [row["content_id"] for row in planned.envelope["data"]["items"]] == ["3"]
    stage.crate(*VERB)

    written = stage.json(*VERB, "--apply")
    assert written.code == OK, written.stdout
    assert written.envelope["data"]["totals"]["written"] == 2
    # Apply again: both tags are on the row, so nothing more is written.
    stage.crate(*VERB, "--apply")


def test_an_unreadable_calibration_refuses_and_writes_nothing(stage, ready):
    cfg, _audio, _db_path = ready
    _vocal_calibration(cfg, '{"threshold": 37.')
    refused = stage.json(*VERB, "--apply")
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    assert refused.envelope["cause"]["reason"] == "vocal-calibration-unreadable"
