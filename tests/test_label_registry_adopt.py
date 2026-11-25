"""U100: an accepted harvested label is added to the registry (R-419)."""

from __future__ import annotations

import io
import unicodedata
from types import SimpleNamespace

import pytest

from cratekit import cli
from cratekit.core import config, review
from cratekit.core.exit_codes import ExitCode
from cratekit.label import harvest
from cratekit.label import registry as labels
from tests.cli_drive import drive
from tests.test_label_registry_verbs import installed as installed  # noqa: PLC0414
from tests.test_label_workers import one_parser as one_parser  # noqa: PLC0414 - fixture


def offer(cfg: config.Config, *names: str) -> dict[str, str]:
    """Harvest ``names`` into the review queue; the item identifier per name."""
    tracks = [SimpleNamespace(copyright=f"(P) 2024 {name}") for name in names]
    def confirmed(name: str) -> dict:
        return {"verdict": "confirmed"}
    with review.open_store(cfg) as store:
        report = harvest.from_tracks(tracks, store=store, verify=confirmed)
    return {str(item.payload["name"]): item.item_id for item in report.offered}


def harvested(cfg: config.Config, name: str, **fields) -> str:
    """Offer one harvested-label item for ``name`` straight to the queue; its identifier."""
    item = dict(queue=review.Queue.LABEL_RELEASE, kind=harvest.KIND, identity={"name": name},
                payload={"name": name, "source": "harvest"}, handler_key=harvest.HANDLER_KEY)
    item.update(fields)
    with review.open_store(cfg) as store:
        return review.offer(store, **item).item_id


def answer(item_id: str, verdict: str = "accepted") -> None:
    code, envelope = drive(["review", "resolve", item_id, "--verdict", verdict])
    assert code == int(ExitCode.OK), envelope


def adopt(*extra: str) -> dict:
    code, envelope = drive(["label", "registry", "adopt", *extra])
    assert code == int(ExitCode.OK), envelope
    return envelope


def listed() -> dict[str, str]:
    """The registry as ``list`` reports it, identifier to display name."""
    code, envelope = drive(["label", "registry"])
    assert code == int(ExitCode.OK), envelope
    return {entry["label_id"]: entry["name"] for entry in envelope["data"]["summary"]["labels"]}


def intent_bytes() -> bytes | None:
    path = config.state_path("label_intent")
    return path.read_bytes() if path.exists() else None


def test_an_accepted_label_is_added_once_and_a_second_run_adds_none(installed):
    ids = offer(installed, "Hotflush Recordings")
    answer(ids["Hotflush Recordings"])
    first = adopt()
    assert first["outcome"] == "ok"
    assert first["data"]["summary"]["added"] == ["hotflush-recordings"]
    assert listed() == {"hotflush-recordings": "Hotflush Recordings"}
    written = intent_bytes()
    second = adopt()
    assert second["outcome"] == "no_op"
    assert second["data"]["summary"]["added"] == []
    assert second["data"]["summary"]["present"] == ["hotflush-recordings"]
    assert listed() == {"hotflush-recordings": "Hotflush Recordings"}
    assert intent_bytes() == written


def test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry(installed):
    """A rewrite of equal entries is not harmless: ``recognize`` drops what it cannot read."""
    path = config.state_path("label_intent")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"version": 1, "labels": {'
                    '"kompakt": {"label_id": "kompakt", "name": "Kompakt"}, '
                    '"unread": "a record this build cannot read"}}\n', encoding="utf-8")
    before = intent_bytes()
    ids = offer(installed, "Kompakt")
    answer(ids["Kompakt"])
    envelope = adopt()
    assert envelope["data"]["summary"]["present"] == ["kompakt"]
    assert intent_bytes() == before


def test_a_rejected_or_open_label_is_not_added(installed):
    ids = offer(installed, "Kept", "Turned Down", "Undecided")
    answer(ids["Kept"])
    answer(ids["Turned Down"], "rejected")
    summary = adopt()["data"]["summary"]
    assert summary["added"] == ["kept"]
    assert summary["rejected"] == 1
    assert summary["open"] == 1
    assert listed() == {"kept": "Kept"}


def test_nothing_accepted_writes_nothing_and_says_what_is_waiting(installed):
    ids = offer(installed, "Undecided", "Turned Down")
    answer(ids["Turned Down"], "rejected")
    envelope = adopt()
    assert envelope["outcome"] == "no_op"
    (check,) = envelope["data"]["checks"]
    assert check["detail"] == "no harvested label is accepted in review; 1 open, 1 rejected"
    assert intent_bytes() is None


@pytest.mark.parametrize(
    "offered", [pytest.param("KOMPAKT", id="case"), pytest.param("  Kompakt", id="padding")]
)
def test_a_label_held_under_a_folded_name_is_reported_not_duplicated(installed, offered):
    code, _ = drive(["label", "registry", "add", "Kompakt"])
    assert code == int(ExitCode.OK)
    before = intent_bytes()
    item_id = harvested(installed, offered)
    answer(item_id)
    envelope = adopt()
    assert envelope["data"]["summary"]["added"] == []
    assert envelope["data"]["summary"]["present"] == ["kompakt"]
    assert listed() == {"kompakt": "Kompakt"}
    assert intent_bytes() == before


def test_a_carried_over_accented_label_is_not_filed_twice(installed):
    """R-381: ``Sueño`` carried over under the source system's ``sueno``."""
    store = labels.RegistryStore()
    store.update(lambda current: current.update(
        {"sueno": labels.LabelEntry(label_id="sueno", name="Sueño")}
    ))
    before = intent_bytes()
    decomposed = unicodedata.normalize("NFD", "Sueño")
    ids = offer(installed, decomposed)
    answer(ids[decomposed])
    envelope = adopt()
    assert envelope["data"]["summary"]["added"] == []
    assert envelope["data"]["summary"]["present"] == ["sueno"]
    assert listed() == {"sueno": "Sueño"}
    assert intent_bytes() == before
    (check,) = envelope["data"]["checks"]
    assert check["status"] == "info"
    assert check["detail"].endswith("already held as sueno, under the name Sueño")


def test_two_spellings_accepted_in_one_run_add_the_label_once(installed):
    ids = offer(installed, "Drumcode")
    loud_id = harvested(installed, "DRUMCODE")
    answer(ids["Drumcode"])
    answer(loud_id)
    summary = adopt()["data"]["summary"]
    assert summary["added"] == ["drumcode"]
    assert summary["present"] == ["drumcode"]
    assert listed() == {"drumcode": "Drumcode"}


def test_a_name_with_no_identifier_fails_alone_and_the_rest_land(installed):
    ids = offer(installed, "Innervisions")
    bare_id = harvested(installed, "---")
    answer(ids["Innervisions"])
    answer(bare_id)
    envelope = adopt()
    assert envelope["data"]["summary"]["added"] == ["innervisions"]
    assert envelope["data"]["summary"]["refused"] == ["---"]
    # Not present: a script reading the summary must not be told the registry holds it.
    assert envelope["data"]["summary"]["present"] == []
    failing = [check for check in envelope["data"]["checks"] if check["status"] == "fail"]
    assert [check["key"] for check in failing] == [f"adopt.{bare_id}"]
    assert listed() == {"innervisions": "Innervisions"}


def test_an_accepted_item_naming_no_label_is_reported_not_skipped(installed):
    """``review import`` can land an item with no identity and an empty payload."""
    item_id = harvested(installed, " ", payload={"source": "harvest"})
    answer(item_id)
    envelope = adopt()
    assert envelope["data"]["summary"]["nameless"] == [item_id]
    (check,) = envelope["data"]["checks"]
    assert check["status"] == "fail"
    assert intent_bytes() is None


def test_a_label_release_on_the_same_queue_is_not_adopted(installed):
    """The queue is shared with the sweep's releases. Only harvested labels count."""
    answer(harvested(installed, "A Release Title", kind="label-release",
                     identity={"release_id": "1", "name": "A Release Title"},
                     payload={"name": "A Release Title", "title": "A Release Title"},
                     handler_key="sync.labels"))
    envelope = adopt()
    assert envelope["data"]["summary"]["added"] == []
    assert intent_bytes() is None


@pytest.mark.parametrize(
    "extra",
    [["Some Label"], ["--to", "Other"], ["--track-limit", "5"], ["--seed", "Scuba"]],
    ids=["name", "to", "track-limit", "seed"],
)
def test_adopt_with_a_name_or_a_field_refuses_and_writes_nothing(installed, extra):
    ids = offer(installed, "Hotflush Recordings")
    answer(ids["Hotflush Recordings"])
    code, envelope = drive(["label", "registry", "adopt", *extra])
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "label-name-invalid"
    assert intent_bytes() is None


def test_a_person_reading_the_default_output_sees_what_was_added(installed):
    """``drive`` requests json; this is the output a person actually gets."""
    ids = offer(installed, "Hotflush Recordings")
    answer(ids["Hotflush Recordings"])
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["label", "registry", "adopt"], stdout=out, stderr=err)
    assert code == int(ExitCode.OK), err.getvalue()
    lines = out.getvalue().splitlines()
    added = "Hotflush Recordings: added as hotflush-recordings"
    assert any(line.strip().endswith(added) for line in lines), out.getvalue()


def test_a_renamed_label_is_held_by_its_name_and_not_filed_again(installed):
    """A rename keeps the identifier, so presence is the name as verbs resolve it."""
    for argv in (["add", "Kompakt"], ["rename", "kompakt", "--to", "Sueño"]):
        code, envelope = drive(["label", "registry", *argv])
        assert code == int(ExitCode.OK), envelope
    ids = offer(installed, "Sueño")
    answer(ids["Sueño"])
    summary = adopt()["data"]["summary"]
    assert summary["added"] == []
    assert summary["present"] == ["kompakt"]
    assert listed() == {"kompakt": "Sueño"}
