"""U100: an accepted harvested label is added to the registry.

R-419 is the reason this file exists. Harvest offered labels into review and
nothing read the verdict, so every approved label was typed again into
``label registry add``.

THE ITEMS ARE OFFERED BY THE REAL PRODUCER. ``harvest.from_tracks`` writes them
with a verifier that confirms every name, which is the provider seam and nothing
else, and they are answered through ``review resolve`` on the real dispatcher.
The registry is read back through ``label registry list``, so a test cannot pass
over an adopt that wrote a file ``list`` does not show.
"""

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
from tests.test_config import valid_data


@pytest.fixture
def installed(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    return resolved


def offer(cfg: config.Config, *names: str) -> dict[str, str]:
    """Harvest ``names`` into the review queue; the item identifier per name."""
    tracks = [SimpleNamespace(copyright=f"(P) 2024 {name}") for name in names]
    with review.open_store(cfg) as store:
        report = harvest.from_tracks(
            tracks, store=store, verify=lambda name: {"verdict": "confirmed"}
        )
    return {str(item.payload["name"]): item.item_id for item in report.offered}


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
    # Nothing added, nothing written: the file is the one the first run left.
    assert intent_bytes() == written


def test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry(installed):
    """A rewrite of equal entries is not harmless: ``recognize`` drops what it cannot read.

    The second run in the test above leaves equal bytes whether or not it
    wrote, so it cannot tell the two apart. A record the loader skips can: a
    save of what was loaded discards it.
    """
    path = config.state_path("label_intent")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"version": 1, "labels": {'
        '"kompakt": {"label_id": "kompakt", "name": "Kompakt"}, '
        '"unread": "a record this build cannot read"}}\n',
        encoding="utf-8",
    )
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
    "offered",
    [
        pytest.param("KOMPAKT", id="case"),
        pytest.param("  Kompakt", id="padding"),
    ],
)
def test_a_label_held_under_a_folded_name_is_reported_not_duplicated(installed, offered):
    code, _ = drive(["label", "registry", "add", "Kompakt"])
    assert code == int(ExitCode.OK)
    before = intent_bytes()
    with review.open_store(installed) as store:
        item = review.offer(
            store,
            queue=review.Queue.LABEL_RELEASE,
            kind=harvest.KIND,
            identity={"name": offered},
            payload={"name": offered, "source": "harvest"},
            handler_key=harvest.HANDLER_KEY,
        )
    answer(item.item_id)

    envelope = adopt()

    assert envelope["data"]["summary"]["added"] == []
    assert envelope["data"]["summary"]["present"] == ["kompakt"]
    assert listed() == {"kompakt": "Kompakt"}
    assert intent_bytes() == before


def test_a_carried_over_accented_label_is_not_filed_twice(installed):
    """R-381: ``Sueño`` held under the source system's ``sueno`` slugs to ``sue-o``.

    A presence check on the slug alone files a second entry, which is the
    hazard the brief names. Offered decomposed, so the name also has to fold
    through NFC to be recognised.
    """
    store = labels.RegistryStore()
    store.update(
        lambda current: current.update(
            {"sueno": labels.LabelEntry(label_id="sueno", name="Sueño")}
        )
    )
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
    with review.open_store(installed) as store:
        loud = review.offer(
            store,
            queue=review.Queue.LABEL_RELEASE,
            kind=harvest.KIND,
            identity={"name": "DRUMCODE"},
            payload={"name": "DRUMCODE", "source": "harvest"},
            handler_key=harvest.HANDLER_KEY,
        )
    answer(ids["Drumcode"])
    answer(loud.item_id)

    summary = adopt()["data"]["summary"]

    assert summary["added"] == ["drumcode"]
    assert summary["present"] == ["drumcode"]
    assert listed() == {"drumcode": "Drumcode"}


def test_a_name_with_no_identifier_fails_alone_and_the_rest_land(installed):
    ids = offer(installed, "Innervisions")
    with review.open_store(installed) as store:
        bare = review.offer(
            store,
            queue=review.Queue.LABEL_RELEASE,
            kind=harvest.KIND,
            identity={"name": "---"},
            payload={"name": "---", "source": "harvest"},
            handler_key=harvest.HANDLER_KEY,
        )
    answer(ids["Innervisions"])
    answer(bare.item_id)

    envelope = adopt()

    assert envelope["data"]["summary"]["added"] == ["innervisions"]
    assert envelope["data"]["summary"]["refused"] == ["---"]
    failing = [check for check in envelope["data"]["checks"] if check["status"] == "fail"]
    assert [check["key"] for check in failing] == [f"adopt.{bare.item_id}"]
    assert listed() == {"innervisions": "Innervisions"}


def test_an_accepted_item_naming_no_label_is_reported_not_skipped(installed):
    """``review import`` can land an item with no identity and an empty payload."""
    with review.open_store(installed) as store:
        item = review.offer(
            store,
            queue=review.Queue.LABEL_RELEASE,
            kind=harvest.KIND,
            identity={"name": " "},
            payload={"source": "harvest"},
            handler_key=harvest.HANDLER_KEY,
        )
    answer(item.item_id)

    envelope = adopt()

    assert envelope["data"]["summary"]["nameless"] == [item.item_id]
    (check,) = envelope["data"]["checks"]
    assert check["status"] == "fail"
    assert intent_bytes() is None


def test_a_label_release_on_the_same_queue_is_not_adopted(installed):
    """The queue is shared with the sweep's releases. Only harvested labels count."""
    with review.open_store(installed) as store:
        release = review.offer(
            store,
            queue=review.Queue.LABEL_RELEASE,
            kind="label-release",
            identity={"release_id": "1", "name": "A Release Title"},
            payload={"name": "A Release Title", "title": "A Release Title"},
            handler_key="sync.labels",
        )
    answer(release.item_id)

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
    assert any(
        line.strip().endswith("Hotflush Recordings: added as hotflush-recordings")
        for line in lines
    ), out.getvalue()
