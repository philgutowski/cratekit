"""Adoption files each track into the energy sub its own file's tag names.

The residual titled "Adoption files every track as if it had no energy reading,
and the library's files carry one" is what this module holds shut. Adoption
passed a level of None for every track, so a library where 7,726 of 7,773
files carried an energy tag was planned with 7,401 of them in Unsorted. The
reading now comes off the file at the census, through the tag module's one
reader, and rides on the scanned track into the plan.

Every file here is a real container with a real tag, written by the product's
own writer, because the defect was a reading nobody took and a fixture that
hands the census a number would not have seen it.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.adopt import apply_cli as adopt_apply_cli
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.core import config, routing, tags, taxonomy
from tests._containers import synth_container
from tests.test_config import valid_data

TREE_ID = "shelf_stack"


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library):
    return config.from_dict(valid_data(library))


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC, encoded once and copied per track, because ffmpeg is slow."""
    return synth_container(tmp_path_factory.mktemp("synth"), ".flac")


def _track(library: Path, silence: Path, name: str, *, energy: str | None) -> Path:
    path = library / "Music" / name
    shutil.copyfile(silence, path)
    if energy is not None:
        assert tags.write_tags(path, {"energylevel": energy}) is True
    return path


def _row(path: Path, genre: str, content_id: str) -> adopt_scan.CollectionRow:
    return adopt_scan.CollectionRow(
        content_id=content_id, recorded=str(path), genre=genre, deleted=False
    )


def _plan(cfg, declared, rows) -> adopt_plan.AdoptionPlan:
    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root))
    return adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)


def _by_id(plan: adopt_plan.AdoptionPlan) -> dict[str, adopt_plan.PlanEntry]:
    return {entry.content_id: entry for entry in plan.entries}


def _band_for(declared, level: int) -> str:
    """The band id the taxonomy declares for a level, derived rather than named."""
    return next(band.id for band in declared.energy.bands if level <= band.max)


# ── a tagged file lands in its energy band ─────────────────────────────────


def test_a_tagged_file_lands_in_the_band_its_energy_falls_in(cfg, declared, library, silence):
    levels = {"low": 2, "mid": 5, "top": 9}
    rows = [
        _row(_track(library, silence, f"{name}.flac", energy=str(level)), "Tech House", name)
        for name, level in levels.items()
    ]
    entries = _by_id(_plan(cfg, declared, rows))

    subs = {name: entries[name].sub for name in levels}
    assert subs == {name: _band_for(declared, level) for name, level in levels.items()}
    assert len(set(subs.values())) == 3, "three levels in three bands landed together"
    assert declared.energy.no_energy_sub.id not in subs.values()
    assert {entries[name].energy for name in levels} == set(levels.values())


def test_adoption_lands_a_track_where_the_routing_pass_would(cfg, declared, library, silence):
    """The same reading through the same resolver, compared over every bucket."""
    path = _track(library, silence, "t.flac", energy="8")
    for bucket in declared.buckets:
        entry = _by_id(_plan(cfg, declared, [_row(path, bucket.display, "t")]))["t"]
        if entry.disposition is not adopt_scan.Disposition.ROUTE:
            continue
        expected = routing.energy_sub(
            declared, entry.bucket, tags.read_energy_from_file(path), source_genre=bucket.display
        )
        assert entry.sub == expected.id, bucket.id


# ── an untagged file lands where it always did ─────────────────────────────


def test_an_untagged_file_lands_in_unsorted_as_before(cfg, declared, library, silence):
    path = _track(library, silence, "bare.flac", energy=None)
    plan = _plan(cfg, declared, [_row(path, "Tech House", "bare")])
    entry = _by_id(plan)["bare"]

    assert entry.sub == declared.energy.no_energy_sub.id
    assert (entry.energy, entry.energy_unreadable) == (None, False)
    assert plan.energy_readings() == {"read": 0, "absent": 1, "unreadable": 0}


# ── the per bucket exceptions hold for both ────────────────────────────────


@pytest.mark.parametrize("energy", ["9", None], ids=["tagged", "untagged"])
@pytest.mark.parametrize("genre", ["Chill / Ambient", "Hip-Hop"])
def test_a_bucket_with_an_exception_keeps_it_tagged_or_not(
    cfg, declared, library, silence, genre, energy
):
    path = _track(library, silence, "x.flac", energy=energy)
    entry = _by_id(_plan(cfg, declared, [_row(path, genre, "x")]))["x"]
    bucket = declared.bucket(entry.bucket)
    assert bucket.sub_by_source is not None or bucket.single_sub is not None, (
        f"{genre} no longer reaches an exception bucket, so this proves nothing"
    )

    expected = routing.energy_sub(declared, entry.bucket, None, source_genre=genre)
    assert entry.sub == expected.id
    assert entry.sub not in {band.id for band in declared.energy.bands}


# ── a tag that cannot be read is reported, not silently unsorted ──────────


def test_a_file_whose_tags_cannot_be_read_is_reported(cfg, declared, library):
    path = library / "Music" / "damaged.flac"
    path.write_bytes(b"\x00" * 64)
    plan = _plan(cfg, declared, [_row(path, "Tech House", "damaged")])
    entry = _by_id(plan)["damaged"]

    assert entry.category is adopt_scan.Readability.READABLE
    assert entry.sub == declared.energy.no_energy_sub.id
    assert entry.energy_unreadable is True
    assert plan.energy_readings() == {"read": 0, "absent": 0, "unreadable": 1}
    document = adopt_plan.to_json(plan)
    assert document["energy"]["unreadable"] == 1
    assert document["entries"][0]["energy_unreadable"] is True


def test_a_value_that_is_not_a_number_is_reported_as_unreadable(cfg, declared, library, silence):
    path = _track(library, silence, "word.flac", energy="high")
    entry = _by_id(_plan(cfg, declared, [_row(path, "Tech House", "word")]))["word"]

    assert entry.energy_unreadable is True
    assert entry.sub == declared.energy.no_energy_sub.id


def test_the_approval_gate_shows_the_reading_tally(cfg, declared, library, silence):
    rows = [
        _row(_track(library, silence, "a.flac", energy="7"), "Tech House", "a"),
        _row(_track(library, silence, "b.flac", energy=None), "Tech House", "b"),
    ]
    _screen, facts = adopt_apply_cli._digested(_plan(cfg, declared, rows))

    assert facts["energy"] == {"read": 1, "absent": 1, "unreadable": 0}


def test_an_excluded_file_is_never_opened_for_its_reading(cfg, declared, library):
    opened: list[Path] = []

    def reader(path: Path) -> int | None:
        opened.append(path)
        return 5

    rows = [_row(library / "Music" / "gone.flac", "Tech House", "gone")]
    scanned = list(
        adopt_scan.scan_rows(rows, declared, root=cfg.library.root, energy_reader=reader)
    )

    assert scanned[0].readability is adopt_scan.Readability.MISSING
    assert opened == [], "the census opened a file it had just classified as absent"
    plan = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)
    assert plan.energy_readings() == {"read": 0, "absent": 0, "unreadable": 0}


# ── the digest covers the chosen sub ───────────────────────────────────────


def test_a_changed_reading_moves_the_digest(cfg, declared, library, silence):
    path = _track(library, silence, "d.flac", energy="2")
    rows = [_row(path, "Tech House", "d")]
    before = _plan(cfg, declared, rows).digest()

    assert tags.write_tags(path, {"energylevel": "9"}) is True
    assert _plan(cfg, declared, rows).digest() != before


def test_an_unreadable_file_and_an_untagged_one_are_different_plans(cfg, declared, library, silence):
    path = _track(library, silence, "u.flac", energy=None)
    rows = [_row(path, "Tech House", "u")]
    untagged = _plan(cfg, declared, rows)
    path.write_bytes(b"\x00" * 64)
    damaged = _plan(cfg, declared, rows)

    assert [e.entry_id for e in untagged.entries] == [e.entry_id for e in damaged.entries]
    assert untagged.digest() != damaged.digest()


# ── a genre answered later keeps the census's reading ─────────────────────


def test_a_genre_verdict_lands_in_the_band_the_census_read(cfg, declared, library, silence):
    path = _track(library, silence, "n.flac", energy="9")
    plan = _plan(cfg, declared, [_row(path, "", "n")])
    assert _by_id(plan)["n"].disposition is adopt_scan.Disposition.NEEDS_GENRE

    answered = adopt_plan.with_verdicts(plan, {"n": "tech_house"}, declared)
    entry = _by_id(answered)["n"]

    assert entry.disposition is adopt_scan.Disposition.ROUTE
    assert entry.sub == _band_for(declared, 9)


# ── the checked reader beneath it ──────────────────────────────────────────


def test_the_checked_reader_tells_absent_from_unreadable(library, silence):
    tagged = _track(library, silence, "r1.flac", energy="6")
    bare = _track(library, silence, "r2.flac", energy=None)
    word = _track(library, silence, "r3.flac", energy="loud")
    damaged = library / "Music" / "r4.flac"
    damaged.write_bytes(b"\x00" * 64)

    assert tags.read_energy_checked(tagged) == 6
    assert tags.read_energy_checked(bare) is None
    for path in (word, damaged):
        with pytest.raises(tags.TagReadFailed):
            tags.read_energy_checked(path)
        assert tags.read_energy_from_file(path) is None, "the lenient reader moved"
