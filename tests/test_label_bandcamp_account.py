"""U177: a label in the registry names the Bandcamp seller account it sells from.

One more registry field beside ``match`` and ``kind``, set and cleared with the
registry's own verbs and read by ``crate acquire bandcamp``. Every drive goes
through the real dispatcher and every read back through ``list``, for the
reason ``tests/test_label_registry_verbs.py`` gives: a person must be able to
set the field AND see it set with the verbs they have. A refusal is proven by
the file not moving as well as by its reason.

D1 applies. ``pulsromania`` is the fake account's seller in the Bandcamp suites.
"""

from __future__ import annotations

import json

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.label import registry as labels
from tests.test_label_registry_verbs import (
    installed as installed,  # noqa: PLC0414
)
from tests.test_label_registry_verbs import intent_bytes, listed, ok, refused


def test_add_with_an_account_round_trips_through_list(installed):
    del installed
    envelope = ok(["add", "PULS", "--bandcamp", "pulsromania"])

    assert listed()["puls"]["bandcamp"] == "pulsromania"
    (check,) = [c for c in envelope["data"]["checks"] if c["key"] == "labels.puls"]
    assert "Bandcamp pulsromania" in check["detail"]


@pytest.mark.parametrize(
    "given",
    [
        "PulsRomania",
        "pulsromania.bandcamp.com",
        "https://pulsromania.bandcamp.com",
        "https://PulsRomania.bandcamp.com/music",
        "pulsromania.bandcamp.com/album/sun-path",
        "  pulsromania  ",
    ],
)
def test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as(installed, given):
    del installed
    ok(["add", "PULS", "--bandcamp", given])

    assert listed()["puls"]["bandcamp"] == "pulsromania"


def test_a_seller_on_its_own_domain_keeps_the_whole_host(installed):
    """``acquire.bandcamp.seller_of`` keeps the host of a seller off bandcamp.com."""
    del installed
    ok(["add", "PULS", "--bandcamp", "https://music.example.org/album/x"])

    assert listed()["puls"]["bandcamp"] == "music.example.org"


@pytest.mark.parametrize("given", ["", "   ", "puls romania", "https://", "puls_romania", "-puls"])
def test_an_account_that_could_match_no_purchase_is_refused_and_writes_nothing(installed, given):
    del installed
    ok(["add", "PULS"])
    before = intent_bytes()

    cause = refused(["set", "PULS", f"--bandcamp={given}"])

    assert cause["reason"] == "label-name-invalid"
    assert intent_bytes() == before


def test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name(installed):
    del installed
    ok(["add", "PULS", "--bandcamp", "pulsromania"])
    ok(["add", "Kompakt"])
    before = intent_bytes()

    for argv in (
        ["set", "Kompakt", "--bandcamp", "pulsromania.bandcamp.com"],
        ["add", "Puls Romania", "--bandcamp", "PULSROMANIA"],
    ):
        cause = refused(argv)
        assert cause["reason"] == "label-name-invalid"
        assert "PULS" in cause["message"] and "pulsromania" in cause["message"]
        assert cause["detail"]["held_by"] == "puls"
        assert intent_bytes() == before
    assert "puls-romania" not in listed()


def test_a_label_setting_its_own_account_again_is_no_conflict(installed):
    del installed
    ok(["add", "PULS", "--bandcamp", "pulsromania"])

    ok(["set", "PULS", "--bandcamp", "pulsromania"])
    ok(["add", "PULS", "--bandcamp", "pulsromania", "--track-limit", "9"])

    assert listed()["puls"]["bandcamp"] == "pulsromania"
    assert listed()["puls"]["track_limit"] == 9


def test_default_clears_the_account_and_frees_it_for_another_label(installed):
    del installed
    ok(["add", "PULS", "--bandcamp", "pulsromania"])
    ok(["add", "Kompakt"])

    ok(["set", "PULS", "--bandcamp", "Default"])
    ok(["set", "Kompakt", "--bandcamp", "pulsromania"])

    assert listed()["puls"]["bandcamp"] is None
    assert listed()["kompakt"]["bandcamp"] == "pulsromania"


def test_an_account_named_default_is_set_by_its_address(installed):
    del installed
    ok(["add", "PULS", "--bandcamp", "default.bandcamp.com"])

    assert listed()["puls"]["bandcamp"] == "default"


def test_set_of_another_field_keeps_the_account(installed):
    del installed
    ok(["add", "PULS", "--bandcamp", "pulsromania"])

    ok(["set", "PULS", "--track-limit", "40"])
    ok(["add", "PULS", "--offer", "3"])

    assert listed()["puls"]["bandcamp"] == "pulsromania"


def test_a_rename_of_the_label_keeps_its_seller(installed):
    del installed
    ok(["add", "PULS", "--bandcamp", "pulsromania"])

    ok(["rename", "PULS", "--to", "PULS Records"])

    entry = listed()["puls"]
    assert entry["name"] == "PULS Records"
    assert entry["bandcamp"] == "pulsromania"
    assert labels.RegistryStore().load().by_bandcamp("pulsromania").name == "PULS Records"


@pytest.mark.parametrize("action", [["remove", "PULS"], ["rename", "PULS", "--to", "P"], []])
def test_bandcamp_on_an_action_that_does_not_set_it_refuses(installed, action):
    del installed
    ok(["add", "PULS"])
    before = intent_bytes()

    cause = refused([*action, "--bandcamp", "pulsromania"])

    assert cause["reason"] == "label-name-invalid"
    assert intent_bytes() == before


def test_set_with_only_bandcamp_is_a_field_to_change(installed):
    del installed
    ok(["add", "PULS"])

    ok(["set", "PULS", "--bandcamp", "pulsromania"])

    assert listed()["puls"]["bandcamp"] == "pulsromania"


# ---------------------------------------------------------------------------
# The store, for a file edited by hand
# ---------------------------------------------------------------------------


def _hand_written(labels_: dict) -> labels.Registry:
    path = config.state_path("label_intent")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 1, "labels": labels_}), encoding="utf-8")
    return labels.RegistryStore().load()


def test_two_labels_naming_one_account_by_hand_answer_no_label(installed):
    del installed
    held = _hand_written(
        {
            "puls": {"name": "PULS", "bandcamp": "pulsromania"},
            "puls-romania": {"name": "Puls Romania", "bandcamp": "PulsRomania.bandcamp.com"},
        }
    )

    assert [entry.label_id for entry in held.claimants("pulsromania")] == ["puls", "puls-romania"]
    assert held.by_bandcamp("pulsromania") is None


def test_a_malformed_stored_account_is_no_account_and_the_label_keeps_the_rest(installed):
    del installed
    held = _hand_written({"puls": {"name": "PULS", "bandcamp": "puls romania", "track_limit": 9}})

    entry = held.by_id("puls")
    assert entry.bandcamp is None and entry.track_limit == 9
    assert held.by_bandcamp("puls romania") is None


def test_an_account_is_looked_up_in_any_form_a_purchase_could_name_it(installed):
    del installed
    labels.RegistryStore().add("PULS", bandcamp="pulsromania")
    held = labels.RegistryStore().load()

    for form in ("pulsromania", "PULSROMANIA", "https://pulsromania.bandcamp.com/"):
        assert held.by_bandcamp(form).label_id == "puls"
    assert held.by_bandcamp("otherlabel") is None
    assert held.by_bandcamp("") is None


def test_the_store_refuses_a_second_claimant_from_a_python_caller(installed):
    del installed
    store = labels.RegistryStore()
    store.add("PULS", bandcamp="pulsromania")
    store.add("Kompakt")

    with pytest.raises(CratekitError) as caught:
        store.edit("Kompakt", bandcamp="pulsromania")

    assert caught.value.cause.reason == "label-name-invalid"
    assert store.load().by_id("kompakt").bandcamp is None
