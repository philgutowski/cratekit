"""Label's scenarios: the registry document, written, read back and refused (U298).

An unparseable document is refused rather than read empty, which U298's move
of the read and the lock must keep. The second scenario drives every other
action and its refusals (U308).
"""

from __future__ import annotations

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from tests.test_label_registry_adopt import offer
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


def test_every_registry_action_and_its_refusals(stage, installed):
    assert stage.crate(*VERB, "add", "Tide Works", "--offer", "4", "--kind", "rnb").code == OK
    assert stage.crate(*VERB, "add", "Puls", "--bandcamp", "https://Puls.bandcamp.com/music").code == OK
    assert stage.crate(*VERB, "set", "Puls", "--genre", "Rominimal", "--seed", "id:77").code == OK
    assert stage.crate(*VERB, "set", "Puls", "--genre", "Polka").code != OK
    assert stage.crate(*VERB, "set", "Puls", "--genre", "Polka", "--accept-fallback").code == OK
    assert stage.crate(*VERB, "set", "tide-works", "--kind", "default", "--genre", "default").code == OK
    assert stage.crate(*VERB, "add", "Other Shore", "--bandcamp", "puls.bandcamp.com").code != OK
    assert stage.crate(*VERB, "add", "Tide Works").code == OK  # an add of a held label
    assert stage.crate(*VERB, "add", "Bad Seed", "--seed", "id:x").code != OK
    assert stage.crate(*VERB, "set", "Puls").code != OK
    assert stage.crate(*VERB, "rename", "Tide Works", "--to", "Tide Works Recordings").code == OK
    assert stage.crate(*VERB, "rename", "No Such Label", "--to", "Elsewhere").code != OK
    assert stage.crate(*VERB, "rename", "Puls").code != OK
    assert stage.crate(*VERB, "remove", "Puls", "--genre", "Rominimal").code != OK
    assert stage.crate(*VERB, "remove", "Puls").code == OK
    assert stage.crate(*VERB, "remove", "Puls").code == OK  # a remove of an absent label
    stage.crate(*VERB, "list")

    # Adopt: one harvested label accepted in review, one rejected, then a second run.
    ids = offer(installed, "Northern Harbour", "Second Tide")
    for item_id, verdict in ((ids["Northern Harbour"], "accepted"), (ids["Second Tide"], "rejected")):
        assert stage.crate("review", "resolve", item_id, "--verdict", verdict).code == OK
    assert stage.crate(*VERB, "adopt", "Northern Harbour").code != OK
    assert stage.crate(*VERB, "adopt").code == OK
    assert stage.json(*VERB, "adopt").code == OK
    assert stage.json(*VERB).code == OK
