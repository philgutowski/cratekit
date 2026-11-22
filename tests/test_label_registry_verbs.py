"""U99: the label registry verbs set a track limit and seed artists (R-418)."""

from __future__ import annotations

import unicodedata

import pytest

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from tests.cli_drive import drive
from tests.test_config import valid_data


def install(tmp_path, monkeypatch) -> config.Config:
    """A configured library on the full profile, which turns the label verbs on."""
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


@pytest.fixture
def installed(tmp_path, monkeypatch):
    return install(tmp_path, monkeypatch)


@pytest.fixture(autouse=True)
def _library(installed):
    """Every test here runs on a configured library."""


def ok(argv: list[str]) -> dict:
    code, envelope = drive(["label", "registry", *argv])
    assert code == int(ExitCode.OK), envelope
    return envelope


def refused(argv: list[str]) -> dict:
    code, envelope = drive(["label", "registry", *argv])
    assert code != int(ExitCode.OK), envelope
    assert envelope.get("cause"), envelope
    return envelope["cause"]


def listed() -> dict[str, dict]:
    """The registry as ``list`` reports it, keyed by identifier."""
    envelope = ok([])
    return {entry["label_id"]: entry for entry in envelope["data"]["summary"]["labels"]}


def intent_bytes() -> bytes | None:
    path = config.state_path("label_intent")
    return path.read_bytes() if path.exists() else None


def test_an_add_with_a_limit_and_two_seeds_round_trips_through_list():
    ok(["add", "Hotflush Recordings", "--track-limit", "50", "--seed", "Scuba", "--seed", "id:4012"])
    entry = listed()["hotflush-recordings"]
    assert entry["track_limit"] == 50
    assert entry["seed_artists"] == ["Scuba", "id:4012"]
    assert entry["name"] == "Hotflush Recordings"


def test_list_shows_the_limit_and_the_seeds_to_a_person():
    """The human rendering reads the check detail, so the fields ride there too."""
    ok(["add", "Kompakt", "--track-limit", "20", "--seed", "id:77"])
    envelope = ok([])
    (check,) = envelope["data"]["checks"]
    assert check["detail"] == "kompakt, track limit 20, seeds id:77"


def test_set_changes_one_field_and_keeps_the_rest():
    ok(["add", "Ostgut Ton", "--match", "Ostgut", "--track-limit", "30",
        "--seed", "Ben Klock", "--seed", "Marcel Dettmann"])
    envelope = ok(["set", "ostgut-ton", "--track-limit", "120"])
    assert envelope["data"]["summary"]["updated"] == "ostgut-ton"
    entry = listed()["ostgut-ton"]
    assert entry["track_limit"] == 120
    assert entry["seed_artists"] == ["Ben Klock", "Marcel Dettmann"]
    assert entry["match"] == "Ostgut"
    assert entry["name"] == "Ostgut Ton"


def test_set_seeds_replaces_the_list_and_keeps_the_limit():
    ok(["add", "Ostgut Ton", "--track-limit", "30", "--seed", "Ben Klock"])
    ok(["set", "Ostgut Ton", "--seed", "id:9", "--seed", "Answer Code Request"])
    entry = listed()["ostgut-ton"]
    assert entry["seed_artists"] == ["id:9", "Answer Code Request"]
    assert entry["track_limit"] == 30


def test_set_on_an_unknown_label_refuses_by_name_and_creates_nothing():
    ok(["add", "Kompakt"])
    before = intent_bytes()
    cause = refused(["set", "Innervisions", "--track-limit", "10"])
    assert cause["reason"] == "label-unknown"
    assert "Innervisions" in cause["message"]
    assert intent_bytes() == before
    assert set(listed()) == {"kompakt"}


@pytest.mark.parametrize("seed", ["id:", "id:12a", "ID:12", "id: 12", "id:-4", "   "])
def test_a_malformed_seed_on_add_refuses_and_writes_nothing(seed):
    ok(["add", "Kompakt", "--seed", "Michael Mayer"])
    before = intent_bytes()
    cause = refused(["add", "Kompakt", "--seed", "Wolfgang Voigt", "--seed", seed])
    assert cause["reason"] == "label-name-invalid"
    assert intent_bytes() == before
    assert listed()["kompakt"]["seed_artists"] == ["Michael Mayer"]


def test_a_malformed_id_seed_on_set_refuses_and_writes_nothing():
    ok(["add", "Kompakt", "--track-limit", "40", "--seed", "id:1"])
    before = intent_bytes()
    cause = refused(["set", "kompakt", "--track-limit", "80", "--seed", "id:1x"])
    assert cause["reason"] == "label-name-invalid"
    assert "id:1x" in cause["message"]
    assert intent_bytes() == before


def test_a_malformed_id_seed_on_a_new_label_creates_no_entry():
    cause = refused(["add", "Kompakt", "--seed", "id:abc"])
    assert cause["reason"] == "label-name-invalid"
    assert intent_bytes() is None


def test_a_name_seed_that_merely_contains_id_is_stored():
    """Only a seed that STARTS like an identifier is held to the digits rule."""
    ok(["add", "Kompakt", "--seed", "Kid:Nap"])
    assert listed()["kompakt"]["seed_artists"] == ["Kid:Nap"]


@pytest.mark.parametrize("limit", ["0", "-5", "ten"])
def test_a_track_limit_below_one_refuses_at_the_parser(limit):
    code, _ = drive(["label", "registry", "add", "Kompakt", "--track-limit", limit])
    assert code == int(ExitCode.USAGE)
    assert intent_bytes() is None


@pytest.mark.parametrize("limit", [0, -1, True])
def test_the_store_refuses_a_limit_below_one_from_a_python_caller(limit):
    """The parser guards the verb; this guards the store, which Python callers reach directly."""
    from cratekit.core.cause import CratekitError
    from cratekit.label import registry as labels
    store = labels.RegistryStore()
    with pytest.raises(CratekitError) as added:
        store.add("Kompakt", track_limit=limit)
    assert added.value.cause.reason == "label-name-invalid"
    store.add("Kompakt")
    with pytest.raises(CratekitError) as edited:
        store.edit("kompakt", track_limit=limit)
    assert edited.value.cause.reason == "label-name-invalid"
    assert store.load().by_id("kompakt").track_limit is None


def test_set_with_no_field_refuses_rather_than_reporting_an_edit():
    ok(["add", "Kompakt", "--track-limit", "40"])
    before = intent_bytes()
    cause = refused(["set", "kompakt"])
    assert cause["reason"] == "label-name-invalid"
    assert intent_bytes() == before


@pytest.mark.parametrize("action", [["remove", "kompakt"], ["rename", "kompakt", "--to", "K"], []])
@pytest.mark.parametrize(
    "field", [["--seed", "Michael Mayer"], ["--track-limit", "9"], ["--match", "Kompakt Rec"]]
)
def test_a_field_flag_on_an_action_that_does_not_set_it_refuses(action, field):
    ok(["add", "Kompakt"])
    before = intent_bytes()
    cause = refused([*action, *field])
    assert cause["reason"] == "label-name-invalid"
    assert intent_bytes() == before


def test_set_finds_an_accented_name_typed_in_decomposed_form():
    """Hazard R-381: the name must resolve however the terminal composed it."""
    composed = unicodedata.normalize("NFC", "Sueño")
    decomposed = unicodedata.normalize("NFD", "Sueño")
    assert composed != decomposed
    ok(["add", composed])
    (label_id,) = listed()
    envelope = ok(["set", decomposed, "--track-limit", "25"])
    assert envelope["data"]["summary"]["updated"] == label_id
    held = listed()
    assert set(held) == {label_id}
    assert held[label_id]["track_limit"] == 25
