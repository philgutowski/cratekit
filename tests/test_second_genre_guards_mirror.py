"""R-1950: each guard on mirror edits' second genre paths (U340) killed by a test.

An unfile clears the second genre, a change's identity and its gate item carry
it, the write reads it back, a non move edit into one of the two folders is
not taken, and a band move whose band only another word files into is not
taken. Expected values are literals or shipped taxonomy words. D1 applies.
"""

from __future__ import annotations

import pytest

from cratekit.core import tags
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize import mirror_edits
from cratekit.write import rebuild
from tests._containers import synth_container
from tests.test_organize_mirror_edits_u340 import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_organize_mirror_edits_u340 import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_organize_mirror_edits_u340 import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_organize_mirror_edits_u340 import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_organize_mirror_edits_u340 import configured as configured  # noqa: PLC0414
from tests.test_organize_mirror_edits_u340 import library as library  # noqa: PLC0414
from tests.test_organize_mirror_edits_u340 import machine as machine  # noqa: PLC0414
from tests.test_second_genre import (
    DECLARED,
    DEEP,
    MED,
    MELODIC,
    ONE,
    TECH,
    TRUTH,
    TWO,
    _at,
    _decision,
)

RNB = DECLARED.bucket_for_display("R&B")


def _two_genre(second: str | None = MELODIC, path: str = "/m/t.flac") -> mirror_edits.Change:
    return mirror_edits.Change(
        "1", "t", edits.MOVE, "t", path, DEEP, DEEP, 5, 9, second_was=TECH, second=second
    )


def _one_genre() -> mirror_edits.Change:
    return mirror_edits.Change("1", "t", edits.MOVE, "t", "/m/t.flac", DEEP, DEEP, 5, 9)


# M01: an unfile clears the second genre with the genre and the energy.


def test_an_unfile_of_a_two_genre_track_clears_its_second_genre(machine):
    machine.take_off(f"{DEEP} Low", "r1")
    machine.take_off(f"{TECH} Low", "r1")
    _area, step = machine.run()
    (change,) = [one for one in step.items if one.get("edit")]
    assert change["edit"] == edits.UNFILE
    assert change["second genre"] == [TECH, None]
    assert tags.read_tag(machine.files["1"], "secondgenre") is None
    assert tags.read_genre_from_file(machine.files["1"]) is None
    assert machine.places("1") == set()


# M02: the second genre is in a change's identity, so in the step's digest.


def test_two_changes_differing_only_in_the_second_genre_have_different_identities():
    assert _two_genre().identity() == [
        "1", "t", "move", "/m/t.flac", DEEP, 9, [], [], ["", "", False], [TECH, MELODIC],
    ]
    assert _two_genre(None).identity()[-1] == [TECH, None]
    assert _two_genre().identity() != _two_genre(None).identity()
    first = mirror_edits.Planned(changes=(_two_genre(),)).identity()
    assert first != mirror_edits.Planned(changes=(_two_genre(None),)).identity()


def test_a_one_genre_change_keeps_its_old_identity():
    assert _one_genre().identity() == ["1", "t", "move", "/m/t.flac", DEEP, 9, [], [], ["", "", False]]


# M03: the write reads the second genre back, so one that did not take fails.


@pytest.fixture
def two_genre_file(tmp_path):
    path = synth_container(tmp_path, ".flac")
    assert tags.write_tags(path, {"genre": DEEP, "energylevel": 5, "secondgenre": TECH})
    return path


def test_a_second_genre_the_writer_drops_fails_the_read_back(two_genre_file, monkeypatch):
    real = tags.write_tags

    def dropping(path, fields):
        return real(path, {name: value for name, value in fields.items() if name != "secondgenre"})

    monkeypatch.setattr(tags, "write_tags", dropping)
    assert mirror_edits._write_tags(_two_genre(path=str(two_genre_file))) is False
    assert tags.read_tag(two_genre_file, "secondgenre") == TECH


def test_a_second_genre_the_clearer_skips_fails_the_read_back(two_genre_file, monkeypatch):
    real = tags.clear_tags

    def skipping(path, names):
        kept = [name for name in names if name != "secondgenre"]
        return real(path, kept) if kept else True

    monkeypatch.setattr(tags, "clear_tags", skipping)
    assert mirror_edits._write_tags(_two_genre(None, path=str(two_genre_file))) is False
    assert tags.read_tag(two_genre_file, "secondgenre") == TECH


# M04: the gate item shows the second genre where one is in play, and only there.


def test_the_item_of_a_two_genre_change_shows_both_second_genres():
    assert _two_genre().item()["second genre"] == [TECH, MELODIC]
    assert _two_genre(None).item()["second genre"] == [TECH, None]
    assert "second genre" not in _one_genre().item()


# M05: a non move edit into one of the two folders says nothing of which genre.


@pytest.mark.parametrize(
    ("folder", "shown"), [(DEEP, (TECH, "Med")), (TECH, (DEEP, "Med"))], ids=["first", "second"]
)
def test_a_folder_edit_into_one_of_the_two_folders_is_not_taken(folder, shown):
    """The account showed it in one folder's band alone, then put it in the other's with vox."""
    edit = _decision(edits.FOLDER, (folder, "with vox"), [shown], [shown])
    why = mirror_edits._second_genre_tags(DECLARED, edit, TRUTH, TWO)
    assert isinstance(why, str)
    assert f"the account put it in a playlist of {folder}, which holds it" in why


# M06: a band move inside one of the two folders keeps the word naming it.


def test_a_move_to_a_playlist_no_energy_files_into_is_not_taken():
    """Built by hand, as the decider emits no such move today: a move naming no band is
    refused rather than raised, since no energy files the track there by the folder's genre."""
    edit = _decision(edits.MOVE, (DEEP, "with vox"), [_at(ONE, MED)], [(DEEP, "with vox")])
    why = mirror_edits._second_genre_tags(DECLARED, edit, TRUTH, TWO)
    assert isinstance(why, str)
    assert f"no energy files it into {DEEP} with vox by the genre that names {DEEP}" in why


def test_a_style_sub_only_another_source_word_files_into_is_not_taken():
    """NonElectronic files Folk by the word Folk, so a Rock track moved there is not given Rock."""
    truth = rebuild.Truth(location="/m/t.flac", genre="Rock", energy=5, second_genre=TECH)
    assert mirror_edits.target_tags(DECLARED, "NonElectronic", "Folk", "Rock", 5) == ("Folk", 5)
    edit = _decision(
        edits.MOVE,
        ("NonElectronic", "Folk"),
        [("NonElectronic", "Rock"), _at(TWO, MED)],
        [("NonElectronic", "Folk"), _at(TWO, MED)],
    )
    why = mirror_edits._second_genre_tags(DECLARED, edit, truth, TWO)
    assert isinstance(why, str)
    assert "no energy files it into NonElectronic Folk by the genre that names NonElectronic" in why
