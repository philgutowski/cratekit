"""Label's scenarios: the registry document, written, read back and refused (U298).

`crate label registry` keeps one state document. `add` and `set` write it
under the registry's lock and `list` reads it back; a document that exists and
cannot be parsed is refused in the registry's own words and never read as an
empty registry. The read and the lock are two of the things U298 gave one
home each, so this is the scenario that holds a state store's words and bytes
across that move. On the registry verbs suite's own machine, with labels that
name no real one.
"""

from __future__ import annotations

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from tests.test_label_registry_verbs import installed as installed  # noqa: PLC0414

OK = int(ExitCode.OK)
VERB = ("label", "registry")


def test_registry_document_written_read_back_and_refused(stage, installed):
    added = stage.json(
        *VERB, "add", "Northern Harbour Recordings", "--track-limit", "50",
        "--seed", "A Harbour Artist", "--seed", "id:4012",
    )  # fmt: skip
    assert added.code == OK, added.stdout
    assert stage.json(*VERB, "add", "Second Tide", "--match", "Tide").code == OK
    assert stage.json(*VERB, "set", "second-tide", "--track-limit", "120").code == OK
    listed = stage.json(*VERB)
    assert listed.code == OK, listed.stdout
    labels = {one["label_id"]: one for one in listed.envelope["data"]["summary"]["labels"]}
    assert labels["second-tide"]["track_limit"] == 120
    stage.crate(*VERB)

    # A label the registry does not hold, as a person reads the refusal.
    assert stage.crate(*VERB, "set", "No Such Label", "--track-limit", "3").code != OK

    # A document that is not JSON is refused by every read, and no write replaces it.
    document = config.state_path("label_intent")
    assert document.is_file()
    document.write_bytes(b"{not json")
    assert stage.crate(*VERB).code != OK
    unreadable = stage.json(*VERB, "add", "Third Shore")
    assert unreadable.code != OK, unreadable.stdout
    assert document.read_bytes() == b"{not json"
