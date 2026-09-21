"""R-381: a label slug transliterates before it folds, and the loader migrates.

The producer is the carried-over registry of the fourth attended sitting, which
stored ``Sueño`` as ``sue-o`` and ``Voll Schön`` as ``voll-sch-n`` while the
source system keyed both as ``sueno`` and ``voll-schoen``. The stored documents
here are written as raw JSON, the way that sitting left them, rather than
through :meth:`RegistryStore.add`, which now produces the new identifier.
"""

from __future__ import annotations

import json
import unicodedata

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.label import marks
from cratekit.label import registry as labels
from tests.test_config import valid_data


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    resolved = config.from_dict(valid_data(root))
    config.save(resolved)
    config.reset_cache()
    return resolved


def store_registry(entries: dict[str, str]) -> None:
    """Write the intent document as a pre-R-381 build left it, id to name."""
    path = config.state_path("label_intent")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": labels.REGISTRY_VERSION,
        "labels": {
            label_id: {
                "label_id": label_id,
                "name": name,
                "match": None,
                "seed_artists": [],
                "track_limit": None,
            }
            for label_id, name in entries.items()
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def store_marks(cfg, years: dict[str, str]) -> None:
    path = config.state_path("label_watermarks", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": marks.MARKS_VERSION,
        "labels": {key: {"last_pulled": year} for key, year in years.items()},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def stored_registry() -> dict:
    return json.loads(config.state_path("label_intent").read_text(encoding="utf-8"))


def stored_marks(cfg) -> dict[str, str]:
    raw = json.loads(config.state_path("label_watermarks", cfg).read_text(encoding="utf-8"))
    return {key: value["last_pulled"] for key, value in raw["labels"].items()}


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Sueño", "sueno"),
        ("Voll Schön", "voll-schoen"),
        ("Harbour Lights", "harbour-lights"),
        (unicodedata.normalize("NFD", "Sueño"), "sueno"),
        (unicodedata.normalize("NFD", "Voll Schön"), "voll-schoen"),
        ("Straße", "strasse"),
        ("ÄÖÜ Records", "aeoeue-records"),
        ("Café del Mar", "cafe-del-mar"),
        ("Life and Death", "life-and-death"),
        ("Kompakt", "kompakt"),
    ],
)
def test_a_slug_transliterates_before_it_folds(name, expected):
    assert labels.slug(name) == expected


@pytest.mark.parametrize("name", ["", "   ", "!!!", "--", "́̃"])
def test_a_name_empty_after_transliteration_still_refuses(name):
    with pytest.raises(CratekitError) as caught:
        labels.slug(name)
    assert caught.value.cause.reason == "label-name-invalid"


def test_a_stored_fold_only_identifier_migrates_on_load(cfg):
    del cfg
    store_registry(
        {"sue-o": "Sueño", "voll-sch-n": "Voll Schön", "harbour-lights": "Harbour Lights"}
    )

    held = labels.RegistryStore().load()

    assert list(held.labels) == ["sueno", "voll-schoen", "harbour-lights"]
    assert held.by_id("sueno").name == "Sueño"
    assert held.by_id("sueno").label_id == "sueno"
    written = stored_registry()
    assert list(written["labels"]) == ["sueno", "voll-schoen", "harbour-lights"]
    assert written["labels"]["voll-schoen"]["label_id"] == "voll-schoen"
    assert written["renamed"] == {"sue-o": "sueno", "voll-sch-n": "voll-schoen"}
    assert written["version"] == 1
    before = config.state_path("label_intent").read_bytes()
    labels.RegistryStore().load()
    assert config.state_path("label_intent").read_bytes() == before


def test_a_migrated_label_keeps_its_watermark(cfg):
    store_registry({"sue-o": "Sueño", "harbour-lights": "Harbour Lights"})
    store_marks(cfg, {"sue-o": "2024", "harbour-lights": "2023"})

    labels.RegistryStore().load()

    assert marks.read(cfg, "sueno") == "2024"
    assert marks.read(cfg, "sue-o") is None
    assert stored_marks(cfg) == {"sueno": "2024", "harbour-lights": "2023"}


def test_an_advance_of_another_label_carries_the_migrated_year_along(cfg):
    store_registry({"voll-sch-n": "Voll Schön", "harbour-lights": "Harbour Lights"})
    store_marks(cfg, {"voll-sch-n": "2022"})

    marks.advance(cfg, "harbour-lights", year="2026")

    assert stored_marks(cfg) == {"voll-schoen": "2022", "harbour-lights": "2026"}


def test_a_year_already_held_under_the_new_identifier_is_not_overwritten(cfg):
    store_registry({"sue-o": "Sueño"})
    store_marks(cfg, {"sue-o": "2021", "sueno": "2025"})

    assert marks.read(cfg, "sueno") == "2025"
    assert stored_marks(cfg) == {"sue-o": "2021", "sueno": "2025"}


def test_a_collision_leaves_the_old_identifier(cfg):
    store_registry({"sue-o": "Sueño", "sueno": "Sueno"})
    store_marks(cfg, {"sue-o": "2024", "sueno": "2020"})
    before = config.state_path("label_intent").read_bytes()

    held = labels.RegistryStore().load()

    assert {key: entry.name for key, entry in held.labels.items()} == {
        "sue-o": "Sueño",
        "sueno": "Sueno",
    }
    assert config.state_path("label_intent").read_bytes() == before
    assert marks.read(cfg, "sue-o") == "2024"
    assert marks.read(cfg, "sueno") == "2020"


def test_re_adding_a_collided_label_updates_it_and_not_its_neighbour(cfg):
    del cfg
    store_registry({"sue-o": "Sueño", "sueno": "Sueno"})

    label_id = labels.RegistryStore().add("Sueño", track_limit=25)

    assert label_id == "sue-o"
    held = labels.RegistryStore().load()
    assert held.by_id("sue-o").track_limit == 25
    assert held.by_id("sueno").name == "Sueno"
    assert held.by_id("sueno").track_limit is None


@pytest.mark.parametrize(
    "entries",
    [
        # Renamed since it was created, so the identifier is not the fold of
        # the name it carries now.
        {"sue-o": "Sueño Recordings"},
        # Carried over under an identifier the source system chose.
        {"sueno-music": "Sueño"},
    ],
)
def test_an_identifier_the_old_fold_did_not_produce_is_left_alone(cfg, entries):
    del cfg
    store_registry(entries)
    before = config.state_path("label_intent").read_bytes()

    held = labels.RegistryStore().load()

    assert list(held.labels) == list(entries)
    assert config.state_path("label_intent").read_bytes() == before


def test_re_adding_a_migrated_label_does_not_file_it_twice(cfg):
    del cfg
    store_registry({"sue-o": "Sueño"})

    label_id = labels.RegistryStore().add("Sueño", track_limit=10)

    assert label_id == "sueno"
    held = labels.RegistryStore().load()
    assert list(held.labels) == ["sueno"]
    assert held.by_id("sueno").track_limit == 10
