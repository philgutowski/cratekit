"""U236: a favourite put in on the account and taken off again before the next organize.

Sitting 88 (A90): a track put in ``All Favorites`` on the account was carried by
an organize run into All Favorites and its month in rekordbox. The account area
had been planned before that write, so the account's month never got it, and
the month's snapshot was settled without it. The account then took it off All
Favorites, and the next organize read the library's own month placement as a
change made in rekordbox since: "an addition beats a removal", and the
favourite was kept.

Driven end to end on U204's disposable library, each pass a new organize run
written in organize's order. What is asserted is what the account, the
database and the ledger hold afterwards. D1 applies: nothing here names a real
account, a real person or a real track.
"""

from __future__ import annotations

from cratekit.core import rb_writer
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize.steps import LISTED, NOTHING
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_organize_mirror_edits import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import MONTH, SOURCE, _items, _named, _second_month
from tests.test_organize_mirror_edits_u204 import world as world  # noqa: PLC0414
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414

#: The month the world holds already, and the account's title for it.
SHOWN = f"Favorites {MONTH}"
#: An account time inside the month the world holds, and one in a month it lacks.
IN_MONTH = f"{MONTH}-14T10:00:00+00:00"
NEW_MONTH = "2026-09"
IN_NEW_MONTH = f"{NEW_MONTH}-14T10:00:00+00:00"


def _placed(world) -> dict[str, frozenset[str]]:
    return dict(ledger.mirror_folders(world.cfg)["Favorites"].placed)


def _by_hand(world, name: str, content_id: str) -> str:
    """A person puts a row in a Favorites playlist in rekordbox, making it if absent."""
    handle = rb_writer.open_db(world.db, unlock=False, cfg=world.cfg)
    try:
        folder = handle.get_playlist(ID=world.favorites)
        found = [
            one
            for one in handle.get_playlist(ParentID=world.favorites)
            if str(one.Name) == name and not rb_writer.node_removed(one)
        ]
        playlist = found[0] if found else handle.create_playlist(name, parent=folder)
        handle.session.flush()
        rb_writer.add_memberships(handle, playlist, [content_id])
        handle.session.commit()
        return str(playlist.ID)
    finally:
        rb_writer.close_db(handle)


def _favourited(world, *, at: str) -> None:
    """Round one of the sitting: put in All Favorites on the account, then organize."""
    world.put_in(SOURCE, "r2", at=at)
    _area, step, _queue = world.run_all()
    (change,) = _items(step)
    assert change["edit"] == edits.FAVOURITE
    assert world.members(world.source) == {"1", "2"}


# ═══════════════════════════════════════════════════════════════════════════
# 1. The sitting's two rounds
# ═══════════════════════════════════════════════════════════════════════════


def test_a_favourite_taken_off_again_before_another_organize_is_unfavourited(world):
    """Sitting 88: the month the library placed it in is never read as rekordbox's addition."""
    _favourited(world, at=IN_MONTH)
    assert world.members(world.month) == {"1", "2"}
    # The account area was planned before that write, so its month lacks it.
    assert world.held(SHOWN) == ["r1"]
    assert _placed(world) == {SHOWN: frozenset({"r2"})}

    world.take_off(SOURCE, "r2")
    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.UNFAVOURITE, step.items
    assert sorted(change["leaves"]) == [f"Favorites / {MONTH}", f"Favorites / {SOURCE}"]
    assert world.members(world.source) == {"1"}
    assert world.members(world.month) == {"1"}
    assert world.held(SOURCE) == ["r1"]
    assert _placed(world) == {}
    # And the organize after it plans nothing anywhere.
    area, step, queue, shared = world.plan_all()
    assert step.state == NOTHING and queue.state == NOTHING
    assert {one.state for one in area.steps} <= {NOTHING, LISTED}
    assert shared.reading().decided.decisions == ()


def test_the_same_when_the_write_made_the_month(world):
    """A month the write made is mirrored by no record yet, and its placement is kept all the same."""
    _favourited(world, at=IN_NEW_MONTH)
    made = world.under_favorites(NEW_MONTH)
    assert world.members(made) == {"2"}
    assert _placed(world) == {f"Favorites {NEW_MONTH}": frozenset({"r2"})}

    world.take_off(SOURCE, "r2")
    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.UNFAVOURITE, step.items
    assert world.members(world.source) == {"1"}
    assert world.members(made) == set()


def test_a_month_added_by_hand_in_rekordbox_between_still_beats_the_removal(world):
    """A real addition in rekordbox after the run keeps the favourite, as before."""
    _favourited(world, at=IN_MONTH)
    other = _by_hand(world, "2026-08", "2")

    world.take_off(SOURCE, "r2")
    _area, step, _queue = world.run_all()

    assert step.state == NOTHING
    (named,) = [one for one in _named(step) if one.get("outcome") == edits.REKORDBOX]
    assert "an addition beats a removal" in named["why"]
    assert world.members(world.source) == {"1", "2"}
    assert world.members(other) == {"2"}


# ═══════════════════════════════════════════════════════════════════════════
# 2. The organize after the favourite
# ═══════════════════════════════════════════════════════════════════════════


def test_the_organize_after_the_favourite_puts_it_in_the_accounts_month(world):
    _favourited(world, at=IN_MONTH)

    _area, step, _queue = world.run_all()

    assert step.state == NOTHING
    assert world.held(SHOWN) == ["r1", "r2"]
    assert _placed(world) == {}
    assert "r2" in ledger.mirror_folders(world.cfg)["Favorites"].playlists[SHOWN].agreed
    area, step, queue, _shared = world.plan_all()
    assert step.state == NOTHING and queue.state == NOTHING
    assert {one.state for one in area.steps} <= {NOTHING, LISTED}


def test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one(world):
    """Once the mirror finished the month, a month a person adds in rekordbox is theirs."""
    _favourited(world, at=IN_MONTH)
    world.run_all()
    assert _placed(world) == {}
    other = _by_hand(world, "2026-08", "2")

    world.take_off(SOURCE, "r2")
    _area, step, _queue = world.run_all()

    assert step.state == NOTHING
    assert world.members(world.source) == {"1", "2"}
    assert world.members(other) == {"2"}


def test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month(world):
    """The library chose the placed month for the person, so their own choice replaces it."""
    september = _second_month(world)
    _favourited(world, at=IN_MONTH)
    assert _placed(world) == {SHOWN: frozenset({"r2"})}

    world.put_in(f"Favorites {NEW_MONTH}", "r2")
    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.FAVOURITE, step.items
    assert change["joins"] == [f"Favorites / {NEW_MONTH}"]
    assert change["leaves"] == [f"Favorites / {MONTH}"]
    assert world.members(september) == {"2"}
    assert world.members(world.month) == {"1"}
    assert world.members(world.source) == {"1", "2"}
    assert _placed(world) == {}
    _area, step, queue, shared = world.plan_all()
    assert step.state == NOTHING and queue.state == NOTHING
    assert shared.reading().decided.decisions == ()
