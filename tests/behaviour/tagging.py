"""Tagging's scenarios: a tag written to an audio file (U297).

`crate tag remap` rewrites an older mapping's genre behind its gate, on the
remap suite's two synthesized FLAC containers and their tagging records.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_tag_remap import (
    GATE,
    NEW_ALTERNATIVE,
    NEW_POP,
    OLD_ALTERNATIVE,
    OLD_POP,
    VERB,
    genre_of,
    tagged,
)
from tests.test_tag_remap import machine as machine  # noqa: PLC0414
from tests.test_tag_remap import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_tag_write_to_an_audio_file(stage, machine, silence):
    pop = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    alternative = tagged(machine, silence, "an alternative record", OLD_ALTERNATIVE, "Alternative")

    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    written = stage.json("--run", run_id, *VERB)
    assert written.code == OK, written.stdout
    assert (genre_of(pop), genre_of(alternative)) == (NEW_POP, NEW_ALTERNATIVE)
    # Run again: nothing is left to write, and the verb says so.
    stage.crate(*VERB)
