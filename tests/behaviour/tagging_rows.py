"""Tagging's row scenarios: a row's genre written from its file (U298).

`crate tag rows` plans a genre for every row whose file says another word,
stops at its explicit gate, and once the gate is answered writes the rows
inside one guarded database session and reads every one back. On the rows
suite's own library: its disposable database and the FLAC containers the
encoder synthesized, one row per outcome. The verb asks its gate through the
shell's one lookup, takes its capture through the write layer and records its
commit through the row writer, three of the things U298 gave one home each.

A file of its own beside ``tagging.py``, because the two suites these
scenarios borrow from each call their machine ``machine``, and one file can
hold one fixture of a name.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_tag_rows import (
    COARSE,
    DEEP,
    GATE,
    MELODIC,
    OLD,
    PROGRESSIVE,
    VERB,
    Track,
    _genre_of,
    build,
)
from tests.test_tag_rows import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_tag_rows import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_tag_rows import _reader_cache as _reader_cache  # noqa: PLC0414
from tests.test_tag_rows import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_tag_rows import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_tag_rows import machine as machine  # noqa: PLC0414
from tests.test_tag_rows import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_row_genres_written_from_their_files(stage, acknowledged, silence):
    cfg = acknowledged
    build(
        cfg,
        silence,
        Track("30", OLD, MELODIC),
        Track("31", OLD, MELODIC),
        Track("32", "", PROGRESSIVE),
        Track("33", DEEP, COARSE),
        Track("34", DEEP, DEEP),
    )

    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    written = stage.json("--run", run_id, *VERB)
    assert written.code == OK, written.stdout
    assert (_genre_of(cfg, "30"), _genre_of(cfg, "32")) == (MELODIC, PROGRESSIVE)
    # Run again: every row carries its file's word, and the verb says so.
    stage.crate(*VERB)
