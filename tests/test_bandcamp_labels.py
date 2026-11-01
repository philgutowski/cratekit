"""U177: a Bandcamp seller maps to a registered label, so a purchase stages tagged with it.

Sitting 46 found the label of every release it fetched empty, the files with
no label tag, and the label itself named only in the address the releases
were sold from. These drive the two Bandcamp verbs with a label registered for
that address, through the real dispatcher, over the account U176's suite
serves: the plan names each row's label and every seller no label names, the
fetch writes the label's display name into the label tag of every file it
stages, and ``--seller`` takes the label's name as its account.

EVERYTHING BUT THE TRANSPORT IS REAL, as in ``tests/test_bandcamp_cli.py``,
whose fixtures these are. The registry is written through its own store, the
one ``crate label registry`` writes through.

D1 applies. No real person, seller or release is named; ``pulsromania`` and
``otherlabel`` are the fake account's sellers.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.acquire import bandcamp_cli
from cratekit.core import config, jobs, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.label import registry as labels
from tests.test_bandcamp_cli import (
    account as account,  # noqa: PLC0414
)
from tests.test_bandcamp_cli import (
    cfg as cfg,  # noqa: PLC0414
)
from tests.test_bandcamp_cli import (
    dispositions,
    fetch,
    plan,
    rows,
    staged,
)
from tests.test_bandcamp_cli import (
    library as library,  # noqa: PLC0414
)
from tests.test_bandcamp_cli import (
    signed_in as signed_in,  # noqa: PLC0414
)
from tests.test_bandcamp_cli import (
    silence as silence,  # noqa: PLC0414
)

BATCH = "Batch One"

#: The files the fake account's ``pulsromania`` purchases stage, the library's
#: own track of the compilation held back.
PULS_FILES = (
    "Aurora Bloom - Sun Path - 01 Sun Path.flac",
    "Aurora Bloom - Sun Path - 02 Tide.flac",
    "Various Artists - Compiled - 01 Coral Arc - Glass.flac",
)
OTHER_FILES = ("Coral Arc - Drift - 01 Drift.flac",)


@pytest.fixture
def puls(signed_in) -> labels.LabelEntry:
    """PULS registered as the label ``pulsromania`` sells, by its address."""
    store = labels.RegistryStore()
    label_id = store.add("PULS", bandcamp="https://pulsromania.bandcamp.com/music")
    entry = store.load().by_id(label_id)
    assert entry is not None and entry.bandcamp == "pulsromania"
    return entry


def label_tags(cfg_: config.Config, batch: str = BATCH) -> dict[str, str | None]:
    folder = Path(cfg_.paths.download_staging) / batch
    return {name: tags.read_tag(folder / name, "label") for name in staged(cfg_, batch)}


def warned(envelope: dict, code: str) -> list[str]:
    return [one["message"] for one in envelope["warnings"] if one["code"] == code]


# ═══════════════════════════════════════════════════════════════════════════
# The plan
# ═══════════════════════════════════════════════════════════════════════════


def test_the_plan_names_each_rows_label_and_none_for_a_seller_no_label_names(
    signed_in, account, puls
):
    code, envelope = plan()

    assert code == int(ExitCode.OK), envelope
    by_row = rows(envelope)
    assert {key: row["label"] for key, row in by_row.items()} == {
        "1": "PULS",
        "2": "PULS",
        "3": "PULS",
        "4": None,
        "5": "PULS",
    }
    assert by_row["1"]["label_id"] == puls.label_id
    summary = envelope["data"]["summary"]
    assert summary["labels"] == {"pulsromania": "PULS"}
    assert summary["sellers_unregistered"] == ["otherlabel"]


def test_an_unregistered_seller_is_named_with_the_command_that_registers_it(signed_in, account, puls):
    _code, envelope = plan()

    (message,) = warned(envelope, bandcamp_cli.SELLER_UNREGISTERED)
    assert "otherlabel" in message
    assert bandcamp_cli.register_command("otherlabel") in message
    assert "--bandcamp otherlabel" in message
    (check,) = [c for c in envelope["data"]["checks"] if c["key"] == "acquire.bandcamp.labels"]
    assert check["status"] == "warn"
    assert "pulsromania as PULS" in check["detail"] and "otherlabel" in check["detail"]


def test_with_no_label_registered_every_seller_to_fetch_is_named(signed_in, account):
    _code, envelope = plan()

    summary = envelope["data"]["summary"]
    assert summary["labels"] == {}
    assert summary["sellers_unregistered"] == ["otherlabel", "pulsromania"]
    assert len(warned(envelope, bandcamp_cli.SELLER_UNREGISTERED)) == 2


def test_a_seller_with_nothing_to_fetch_is_not_asked_to_register(signed_in, account, puls):
    """Only a seller something would be fetched from is named: a filtered one is not."""
    _code, envelope = plan("PULS")

    assert envelope["data"]["summary"]["sellers_unregistered"] == []
    assert warned(envelope, bandcamp_cli.SELLER_UNREGISTERED) == []


def test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does(
    signed_in, account, puls
):
    _code, by_account = plan("pulsromania")
    _code, by_label = plan("PULS")
    _code, by_id = plan(puls.label_id)

    assert dispositions(by_label) == dispositions(by_account) == dispositions(by_id)
    assert dispositions(by_label)["4"] == "filtered"
    assert dispositions(by_label)["1"] == "new"
    assert by_label["data"]["summary"]["sellers"] == ["pulsromania"]
    assert by_label["data"]["summary"]["fetch_next"] == (
        "crate acquire bandcamp-fetch --seller pulsromania"
    )
    assert by_label["warnings"] == []


def test_a_followed_label_with_no_account_is_said_so_when_named_as_a_seller(signed_in, account):
    labels.RegistryStore().add("Kompakt")

    _code, envelope = plan("Kompakt")

    (message,) = warned(envelope, "bandcamp-seller-unmatched")
    assert "Kompakt names none" in message
    assert "--bandcamp" in message


def test_two_labels_naming_one_account_by_hand_stage_it_under_neither(signed_in, account):
    """The verbs refuse a second claimant, so two is a hand edit: neither label is guessed."""
    store = labels.RegistryStore()
    store.add("PULS", bandcamp="pulsromania")
    store.add("Puls Romania")
    path = config.state_path("label_intent")
    document = json.loads(path.read_text(encoding="utf-8"))
    document["labels"]["puls-romania"]["bandcamp"] = "pulsromania"
    path.write_text(json.dumps(document), encoding="utf-8")

    _code, envelope = plan()

    assert rows(envelope)["1"]["label"] is None
    messages = warned(envelope, bandcamp_cli.SELLER_UNREGISTERED)
    (tied,) = [one for one in messages if "pulsromania" in one]
    assert "2 labels" in tied and "PULS" in tied and "Puls Romania" in tied


@pytest.mark.parametrize("text", ["{not json", '{"version": 99, "labels": {}}'])
def test_an_unreadable_registry_refuses_the_plan_rather_than_staging_untagged(
    signed_in, account, text
):
    path = config.state_path("label_intent")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

    for drive in (plan, fetch):
        code, envelope = drive()
        assert code != int(ExitCode.OK), envelope
        assert envelope["cause"]["reason"] == "label-intent-unusable"
    assert account.downloaded == []
    assert account.requests == [], "refused before the account was asked"


# ═══════════════════════════════════════════════════════════════════════════
# The fetch
# ═══════════════════════════════════════════════════════════════════════════


def test_a_registered_sellers_files_stage_with_the_label_on_every_one(signed_in, account, puls):
    code, envelope = fetch("--batch", BATCH)

    assert code == int(ExitCode.OK), envelope
    found = label_tags(signed_in)
    assert {name: found[name] for name in PULS_FILES} == dict.fromkeys(PULS_FILES, "PULS")


def test_an_unregistered_sellers_files_stage_with_no_label_tag(signed_in, account, puls):
    fetch("--batch", BATCH)

    found = label_tags(signed_in)
    assert {name: found[name] for name in OTHER_FILES} == dict.fromkeys(OTHER_FILES)


def test_the_label_written_is_the_display_name_and_the_record_names_it(signed_in, account):
    labels.RegistryStore().add("Puls Romania Records", bandcamp="PulsRomania")

    fetch("--batch", BATCH)

    assert set(label_tags(signed_in).values()) == {"Puls Romania Records", None}
    record = bandcamp_cli.fetched(signed_in)
    assert record["1"]["label"] == "Puls Romania Records"
    assert record["4"]["label"] is None
    assert record["1"]["untagged"] == []


def test_the_job_freezes_each_releases_label(signed_in, account, puls):
    _code, envelope = fetch("--batch", BATCH)

    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    releases = job.payload[bandcamp_cli.RELEASES]
    assert releases["1"]["label"] == "PULS" and releases["1"]["label_id"] == puls.label_id
    assert releases["4"]["label"] is None


def test_the_fetch_names_the_landing_that_files_the_batch_by_label(signed_in, account, puls):
    _code, envelope = fetch("--batch", BATCH)

    (message,) = warned(envelope, bandcamp_cli.LAND_BY_LABEL)
    folder = Path(signed_in.paths.download_staging) / BATCH
    assert "PULS" in message
    assert f"crate intake land '{folder}' {bandcamp_cli.LAND_FLAG}" in message
    assert (
        warned(envelope, bandcamp_cli.SELLER_UNREGISTERED)
        and "otherlabel" in warned(envelope, bandcamp_cli.SELLER_UNREGISTERED)[0]
    )


def test_a_fetch_of_no_labels_release_names_no_label_landing(signed_in, account, puls):
    _code, envelope = fetch("--batch", BATCH, "--seller", "otherlabel")

    assert envelope["data"]["state"] == "succeeded"
    assert warned(envelope, bandcamp_cli.LAND_BY_LABEL) == []


def test_seller_by_label_name_fetches_only_that_labels_releases(signed_in, account, puls):
    code, envelope = fetch("--batch", BATCH, "--seller", "PULS")

    assert code == int(ExitCode.OK), envelope
    assert staged(signed_in, BATCH) == sorted(PULS_FILES)


def test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job(
    signed_in, account, puls, monkeypatch
):
    """KTD9: a resume tags by what was registered when the fetch was asked for."""
    real = bandcamp_cli.handle_fetch

    def renamed_first(job, item, cfg_):
        labels.RegistryStore().rename(puls.label_id, "PULS Records")
        return real(job, item, cfg_)

    # The worker is looked up by name when each item runs, so this one is the one run.
    monkeypatch.setattr(bandcamp_cli, "handle_fetch", renamed_first)

    code, envelope = fetch("--batch", BATCH, "--seller", "PULS")

    assert code == int(ExitCode.OK), envelope
    assert labels.RegistryStore().load().by_id(puls.label_id).name == "PULS Records"
    assert set(label_tags(signed_in).values()) == {"PULS"}


def test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item(
    signed_in, account, puls, monkeypatch
):
    real = tags.write_tags
    refused = "Aurora Bloom - Sun Path - 02 Tide.flac"

    def locked(path, fields):
        if "label" in fields and Path(path).name == refused:
            return False
        return real(path, fields)

    monkeypatch.setattr(bandcamp_cli.tags, "write_tags", locked)

    code, envelope = fetch("--batch", BATCH, "--seller", "PULS")

    assert code != int(ExitCode.OK), envelope
    assert staged(signed_in, BATCH) == sorted(PULS_FILES), "the untagged file is staged all the same"
    assert label_tags(signed_in)[refused] is None
    record = bandcamp_cli.fetched(signed_in)
    assert record["1"]["untagged"] == [refused]
    assert record["3"]["untagged"] == []
    with jobs.open_store() as store:
        (job,) = jobs.list_jobs(store)
        failed = [one for one in jobs.items(store, job.job_id) if one.cause is not None]
    (item,) = failed
    assert item.item_id == "1"
    assert item.cause.reason == bandcamp_cli.LABEL_UNWRITTEN
    assert refused in item.cause.message and "PULS" in item.cause.message
