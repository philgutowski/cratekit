"""U236: the month the library placed a favourite in is never read as rekordbox's addition.

Pure, over :func:`mirror_edits.decide`, :func:`mirror_edits.placed_after` and
the ledger's record of a placement. D1 applies: nothing here names a real
account, a real person or a real track.
"""

from __future__ import annotations

import json

from cratekit.core import config
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound import mirror_edits as edits
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_mirror_edits import AF, NOV, OCT, OWNED, only

SEP = edits.Place("Favorites 2026-09", "Favorites", "2026-09", False, edits.FAVORITES)


#: The time of the membership a write made, as rekordbox writes it.
AT = "2026-11-07 16:40:00.000 +00:00"


def held(place, *, account=(), rekordbox=(), agreed=(), never=False, placed=(), **times):
    """A playlist read three ways, with the placements the reader found still standing."""
    return edits.Mirrored(
        place=place,
        account=frozenset(account),
        rekordbox=frozenset(rekordbox),
        agreed=None if never else frozenset(agreed),
        placed=frozenset(placed),
        account_added=times.get("account_added", {}),
        rekordbox_added=times.get("rekordbox_added", {}),
    )


# ═══════════════════════════════════════════════════════════════════════════
# 1. An unfavourite over the library's own month placement
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unfavourite_over_the_month_the_library_placed_is_carried():
    """Sitting 88's second round, read pure."""
    one = only(
        edits.decide(
            [
                held(AF, rekordbox=("t1",), agreed=("t1",)),
                held(NOV, rekordbox=("t1",), placed=("t1",)),
            ],
            OWNED,
        )
    )
    assert (one.outcome, one.content_id) == (edits.UNFAVOURITE, "c1")
    assert set(one.settle) == {
        ("Favorites", "All Favorites", False),
        ("Favorites", "Favorites 2026-11", False),
    }


def test_the_same_over_a_placed_month_never_agreed():
    """A month the write made has no record yet, so its base is its account side."""
    one = only(
        edits.decide(
            [
                held(AF, rekordbox=("t1",), agreed=("t1",)),
                held(NOV, rekordbox=("t1",), never=True, placed=("t1",)),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.UNFAVOURITE


def test_without_the_placement_the_month_is_rekordboxs_addition_as_before():
    one = only(
        edits.decide(
            [
                held(AF, rekordbox=("t1",), agreed=("t1",)),
                held(NOV, rekordbox=("t1",)),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.REKORDBOX and "addition beats a removal" in one.why


def test_a_month_added_beside_the_placed_one_still_beats_the_removal():
    one = only(
        edits.decide(
            [
                held(AF, rekordbox=("t1",), agreed=("t1",)),
                held(OCT, rekordbox=("t1",)),
                held(NOV, rekordbox=("t1",), placed=("t1",)),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.REKORDBOX and "addition beats a removal" in one.why


def test_a_placement_on_another_track_or_in_all_favorites_alone_excuses_nothing():
    one = only(
        edits.decide(
            [
                held(AF, rekordbox=("t1",), agreed=("t1",), placed=("t1",)),
                held(NOV, rekordbox=("t1",), placed=("t2",)),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.REKORDBOX


# ═══════════════════════════════════════════════════════════════════════════
# 2. A favourite over the library's own month placement
# ═══════════════════════════════════════════════════════════════════════════


def test_a_favourite_put_in_another_month_leaves_the_placed_one():
    one = only(
        edits.decide(
            [
                held(AF, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
                held(SEP, account=("t1",)),
                held(NOV, rekordbox=("t1",), placed=("t1",)),
            ],
            OWNED,
        )
    )
    assert (one.outcome, one.to, one.away) == (edits.FAVOURITE, SEP, (NOV,))
    assert "the month the library placed it in" in one.why
    assert ("Favorites", "Favorites 2026-11", False) in one.settle


def test_without_the_placement_the_other_month_goes_by_the_later_change_rule():
    one = only(
        edits.decide(
            [
                held(AF, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
                held(SEP, account=("t1",)),
                held(NOV, rekordbox=("t1",)),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.REKORDBOX


def test_a_favourite_put_in_the_placed_month_on_the_account_is_agreed():
    one = only(
        edits.decide(
            [
                held(AF, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
                held(NOV, account=("t1",), rekordbox=("t1",), placed=("t1",)),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.AGREED


# ═══════════════════════════════════════════════════════════════════════════
# 3. What a placement becomes once the mirror finished its playlist
# ═══════════════════════════════════════════════════════════════════════════


def test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one():
    """Review round one, finding 5: never the later change rule against its own month."""
    one = only(
        edits.decide(
            [
                held(AF, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
                held(SEP, account=("t1",), rekordbox=("t1",)),
                held(NOV, rekordbox=("t1",), placed=("t1",)),
            ],
            OWNED,
        )
    )
    assert (one.outcome, one.to, one.away) == (edits.FAVOURITE, SEP, (NOV,))


def test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold():
    placed = {"t1": AT, "t2": AT, "t3": AT}
    # t1 on the account and no hold: dropped. t2 held: kept. t3 refused or
    # taken off in rekordbox, not on the account: kept, read only by its time.
    assert edits.placed_after(placed, after={"t1", "t2"}, held={"t2"}) == {"t2": AT, "t3": AT}
    assert edits.placed_after({}, after={"t1"}, held={"t1"}) == {}


def test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist(installed):
    ledger.reserve_mirror_folder(installed, "Favorites", lambda: "f1")
    ledger.reserve_mirror_playlist(installed, "Favorites", "All Favorites", lambda: "p1")
    ledger.reserve_mirror_playlist(installed, "Favorites", "Favorites 2026-10", lambda: "p2")
    ledger.record_mirror_agreed(
        installed,
        "Favorites",
        {"All Favorites": ("p1", set(), set()), "Favorites 2026-10": ("p2", set(), set())},
    )

    # A PLACEMENT IS RECORDED BY TITLE, mirrored or not, beside the settle.
    ledger.settle_mirror_tracks(
        installed,
        [("Favorites", "All Favorites", "r1", True), ("Favorites", "Favorites 2026-10", "r1", False)],
        placed=[
            ("Favorites", "Favorites 2026-10", "r1", AT),
            ("Favorites", "Favorites 2026-09", "r1", AT),
            ("Favorites", "Favorites 2026-08", "r1", ""),
            ("Nowhere", "Nowhere 2026-10", "r1", AT),
        ],
    )
    folder = ledger.mirror_folders(installed)["Favorites"]
    assert folder.placed == {"Favorites 2026-10": {"r1": AT}, "Favorites 2026-09": {"r1": AT}}
    assert folder.playlists["Favorites 2026-10"].agreed == frozenset()
    assert "Nowhere" not in ledger.mirror_folders(installed)

    # Kept while a hold covers the track, and while the account lacks it.
    ledger.record_mirror_agreed(installed, "Favorites", {"Favorites 2026-10": ("p2", {"r1"}, {"r1"})})
    assert ledger.mirror_folders(installed)["Favorites"].placed["Favorites 2026-10"] == {"r1": AT}
    ledger.record_mirror_agreed(installed, "Favorites", {"Favorites 2026-10": ("p2", set(), set())})
    assert ledger.mirror_folders(installed)["Favorites"].placed["Favorites 2026-10"] == {"r1": AT}
    # A track settled on the playlist since takes the settle's word instead.
    ledger.settle_mirror_tracks(installed, [("Favorites", "Favorites 2026-09", "r1", False)])
    assert "Favorites 2026-09" not in ledger.mirror_folders(installed)["Favorites"].placed
    # Dropped once the account holds it there with no hold on it.
    ledger.record_mirror_agreed(installed, "Favorites", {"Favorites 2026-10": ("p2", {"r1"}, set())})
    folder = ledger.mirror_folders(installed)["Favorites"]
    assert folder.placed == {}
    assert folder.playlists["Favorites 2026-10"].agreed == {"r1"}


def test_a_placement_survives_the_ledgers_own_read_and_write(installed):
    ledger.reserve_mirror_folder(installed, "Favorites", lambda: "f1")
    ledger.settle_mirror_tracks(installed, [], placed=[("Favorites", "Favorites 2026-10", "r1", AT)])
    # Another write of the ledger keeps it.
    ledger.record_mirror_links(installed, {"9": ("r9", "")})
    assert ledger.mirror_folders(installed)["Favorites"].placed == {"Favorites 2026-10": {"r1": AT}}
    document = json.loads(config.state_path("outbound_writes", installed).read_text(encoding="utf-8"))
    assert document["mirrors"]["Favorites"]["placed"] == {"Favorites 2026-10": {"r1": AT}}
    # A placement the ledger cannot read is dropped, never refused.
    document["mirrors"]["Favorites"]["placed"] = {"Favorites 2026-10": ["r1"], "x": {"r2": 7}}
    config.state_path("outbound_writes", installed).write_text(json.dumps(document), encoding="utf-8")
    assert ledger.mirror_folders(installed)["Favorites"].placed == {}
