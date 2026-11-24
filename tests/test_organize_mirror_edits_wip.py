"""U959: an edit made on the account to a mirrored WIP playlist is held, never undone and never carried. D1 applies.

The rule alone, then a whole organize run on a disposable library: the
rekordbox area's ``mirror-edits`` step and the account mirror over one reading.
"""

from __future__ import annotations

import pytest

from cratekit.core import rb_writer
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize.steps import NOTHING
from tests.test_organize_mirror_edits import Machine, without_fsync
from tests.test_organize_mirror_edits import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import _release_process_locks as _release_process_locks
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414

SET = "deep and soulful"
TITLE = f"Phil {SET}"


# 1. The rule alone


def _place(title: str = TITLE) -> edits.Place:
    return edits.Place(title, "WIP", title, True, edits.WIP)


def test_every_account_change_to_a_wip_playlist_is_held_both_ways_and_never_carried():
    """A row the library holds for each track: an INBOX batch would carry both, WIP carries neither."""
    one = edits.Mirrored(
        place=_place(),
        account=frozenset({"r1", "r9"}),
        rekordbox=frozenset({"r1", "r2"}),
        agreed=frozenset({"r1", "r2"}),
    )
    decided = edits.decide([one], {"r1": ["1"], "r2": ["2"], "r9": ["9"]})
    assert {d.track: d.outcome for d in decided.decisions} == {"r2": edits.HELD, "r9": edits.HELD}
    assert {d.tree for d in decided.decisions} == {edits.WIP}
    assert decided.carried == () and decided.wanted == ()
    assert decided.holds == {TITLE: edits.Hold(keep=frozenset({"r9"}), skip=frozenset({"r2"}))}
    (taken,) = [d for d in decided.decisions if d.track == "r2"]
    assert taken.why == (
        f"taken off {TITLE} on the account, and a WIP playlist takes no edit into the "
        f"library, so it stays as the account has it"
    )


def test_a_track_the_library_lacks_added_to_a_wip_playlist_is_held_and_never_queued():
    one = edits.Mirrored(place=_place(), account=frozenset({"r1", "r9"}), rekordbox=frozenset({"r1"}), agreed=frozenset({"r1"}))
    decided = edits.decide([one], {"r1": ["1"]})
    (added,) = decided.decisions
    assert added.outcome == edits.HELD and added.acquire is False
    assert decided.wanted == ()


def test_a_change_rekordbox_made_too_is_agreed_and_a_short_listing_holds_what_it_left_out():
    agreed = edits.Mirrored(
        place=_place(), account=frozenset({"r1"}), rekordbox=frozenset({"r1"}), agreed=frozenset({"r1", "r2"})
    )
    short = edits.Mirrored(
        place=_place("WIP warmup"), account=frozenset({"r4"}), rekordbox=frozenset({"r4", "r5"}),
        agreed=frozenset({"r4", "r5"}), short=True,
    )
    decided = edits.decide([agreed, short], {"r1": ["1"], "r2": ["2"], "r4": ["4"], "r5": ["5"]})
    outcomes = {(d.to.title, d.track): d.outcome for d in decided.decisions}
    assert outcomes == {(TITLE, "r2"): edits.AGREED, ("WIP warmup", "r5"): edits.HELD}
    # EACH WIP PLAYLIST HOLDS ALONE: the short one's hold is not the other's.
    assert TITLE not in decided.holds
    assert decided.holds["WIP warmup"] == edits.Hold(skip=frozenset({"r5"}))


def test_a_wip_hold_is_its_own_playlists_and_no_other_trees():
    wip = edits.Mirrored(place=_place(), account=frozenset({"r9"}), rekordbox=frozenset(), agreed=frozenset())
    batch = edits.Mirrored(
        place=edits.Place("INBOX b", "INBOX", "b", True, edits.INBOX),
        account=frozenset(), rekordbox=frozenset({"r9"}), agreed=frozenset(),
    )
    decided = edits.decide([wip, batch], {})
    assert decided.holds == {TITLE: edits.Hold(keep=frozenset({"r9"}))}


# 2. A whole organize run


class WipMachine(Machine):
    """U201's library grown a top level ``WIP `` folder holding ``Phil / deep and soulful``."""

    def build(self, scratch):
        names = super().build(scratch)
        handle = rb_writer.open_db(self.db, unlock=False, cfg=self.cfg)
        try:
            wip = handle.create_playlist_folder("WIP ")
            phil = handle.create_playlist_folder("Phil", parent=wip)
            made = handle.create_playlist(SET, parent=phil)
            rb_writer.add_memberships(handle, made, ["1", "2"])
            handle.session.commit()
            names["wip_set"] = str(made.ID)
        finally:
            rb_writer.close_db(handle)
        return names

    def in_set(self) -> list[str]:
        found = self.sql(
            "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? AND COALESCE(rb_local_deleted, 0) = 0",
            self.wip_set,
        )
        return sorted(str(one[0]) for one in found)


@pytest.fixture
def machine(acknowledged, tmp_path, monkeypatch) -> WipMachine:
    without_fsync(monkeypatch)
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    built = WipMachine(acknowledged, scratch)
    built.run()
    return built


def test_the_first_run_mirrors_the_wip_set_and_the_next_plans_nothing(machine):
    assert machine.held(TITLE) == ["r1", "r2"]
    machine.plans_nothing()


def test_an_account_edit_to_a_wip_set_is_held_and_never_undone_nor_carried(machine):
    machine.take_off(TITLE, "r2")
    machine.put_in(TITLE, "r9")
    area, step, shared = machine.plan()
    decided = shared.reading().decided
    assert {(d.track, d.outcome, d.tree) for d in decided.decisions} == {
        ("r2", edits.HELD, edits.WIP), ("r9", edits.HELD, edits.WIP),
    }
    # The library takes nothing, and the mirror writes nothing back.
    assert step.state == NOTHING and step.counts["named"] == 2
    (wip,) = [one for one in area.steps if one.key == "mirror:WIP"]
    assert wip.state == NOTHING
    for _ in range(2):
        machine.run()
        assert machine.held(TITLE) == ["r1", "r9"]
        assert machine.in_set() == ["1", "2"]
    assert shared.reading().decided.wanted == ()


def test_an_account_removal_rekordbox_made_too_is_agreed_and_settles(machine):
    machine.take_off(TITLE, "r2")
    machine.sql(
        "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE PlaylistID = ? AND ContentID = '2'", machine.wip_set
    )
    _area, _step, shared = machine.plan()
    assert [(d.track, d.outcome) for d in shared.reading().decided.decisions] == [("r2", edits.AGREED)]
    machine.run()
    assert machine.held(TITLE) == ["r1"]
    machine.plans_nothing()
