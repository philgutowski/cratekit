"""U340: an edit on the account to one of a track's two genre folders leaves the other.

Track 1 sits in Deep House Low by its genre and in Tech House Low by its second
genre. The disposable library and the faked account are U201's. D1 applies.
"""

from __future__ import annotations

import pytest

from cratekit.core import rb_writer, tags
from tests import test_organize_mirror_edits as _suite
from tests.test_organize_mirror_edits import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import _release_process_locks as _release_process_locks
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414

DEEP, TECH = "Deep House", "Tech House"


class TwoFolders(_suite.Machine):
    """U201's library, track 1 given Tech House as its second genre and filed there too."""

    def build(self, scratch):
        names = super().build(scratch)
        assert tags.write_tags(self.files["1"], {"secondgenre": TECH})
        handle = rb_writer.open_db(self.db, unlock=False, cfg=self.cfg)
        try:
            playlist = handle.get_playlist(ID=names["playlists"][(TECH, "Low")])
            rb_writer.add_memberships(handle, playlist, ["1"])
            handle.session.commit()
        finally:
            rb_writer.close_db(handle)
        return names


@pytest.fixture
def machine(acknowledged, tmp_path, monkeypatch) -> TwoFolders:
    _suite.without_fsync(monkeypatch)
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    built = TwoFolders(acknowledged, scratch)
    built.run()
    return built


def test_the_mirror_shows_the_track_in_both_genre_folders(machine):
    assert machine.places("1") == {(DEEP, "Low"), (TECH, "Low")}
    assert machine.held(f"{DEEP} Low") == ["r1"]
    assert machine.held(f"{TECH} Low") == ["r1"]


def test_a_band_move_in_one_folder_moves_the_energy_in_both_and_keeps_the_second_genre(machine):
    machine.take_off(f"{DEEP} Low", "r1")
    machine.put_in(f"{DEEP} High", "r1")
    _area, step = machine.run()
    (change,) = [one for one in step.items if one.get("edit")]
    assert change["genre"] == [DEEP, DEEP]
    assert sorted(change["leaves"]) == [f"{DEEP} / Low", f"{TECH} / Low"]
    assert sorted(change["joins"]) == [f"{DEEP} / High", f"{TECH} / High"]
    assert machine.places("1") == {(DEEP, "High"), (TECH, "High")}
    assert tags.read_tag(machine.files["1"], "secondgenre") == TECH
    assert tags.read_genre_from_file(machine.files["1"]) == DEEP


def test_taking_it_off_one_folder_alone_is_listed_and_not_taken(machine):
    machine.take_off(f"{TECH} Low", "r1")
    _area, step = machine.run()
    assert [one for one in step.items if one.get("edit")] == []
    (named,) = [one for one in step.items if one.get("track") == "r1"]
    assert "crate tag second" in named["why"]
    assert machine.places("1") == {(DEEP, "Low"), (TECH, "Low")}
    assert tags.read_tag(machine.files["1"], "secondgenre") == TECH


def test_a_one_genre_track_beside_it_moves_as_before(machine):
    machine.take_off(f"{DEEP} Med", "r2")
    machine.put_in(f"{TECH} Med", "r2")
    machine.run()
    assert machine.places("2") == {(TECH, "Med")}
    assert tags.read_tag(machine.files["2"], "secondgenre") is None
