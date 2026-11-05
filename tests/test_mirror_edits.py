"""U201: an edit made on the account to a mirrored genre playlist, told apart and decided.

The pure rule, :func:`mirror_edits.decide`, driven with each playlist read three
ways as values: the snapshot, the account and rekordbox, by account track. The
organize step that reads them and the one that writes the library are driven in
``tests/test_organize_mirror_edits.py``.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from cratekit.modules.outbound import mirror_edits as edits

DHL = edits.Place("Deep House Low", "Deep House", "Low", True)
DHM = edits.Place("Deep House Med", "Deep House", "Med", True)
THM = edits.Place("Tech House Mid", "Tech House", "Mid", True)
THL = edits.Place("Tech House Low", "Tech House", "Low", True)
DHV = edits.Place("Deep House with vox", "Deep House", "with vox", False)
THV = edits.Place("Tech House with vox", "Tech House", "with vox", False)

OWNED = {"t1": ["c1"], "t2": ["c2"], "t3": ["c3"]}


def held(place, *, account=(), rekordbox=(), agreed=(), never=False, short=False, **times):
    return edits.Mirrored(
        place=place,
        account=frozenset(account),
        rekordbox=frozenset(rekordbox),
        agreed=None if never else frozenset(agreed),
        short=short,
        account_added=times.get("account_added", {}),
        rekordbox_added=times.get("rekordbox_added", {}),
    )


def only(decided: edits.Decided) -> edits.Decision:
    (one,) = decided.decisions
    return one


# ═══════════════════════════════════════════════════════════════════════════
# 1. One side changed
# ═══════════════════════════════════════════════════════════════════════════


def test_a_move_on_the_account_is_carried_and_the_mirror_holds_it():
    decided = edits.decide(
        [
            held(DHL, account=(), rekordbox=("t1",), agreed=("t1",)),
            held(THM, account=("t1",), rekordbox=(), agreed=()),
        ],
        OWNED,
    )
    one = only(decided)
    assert (one.outcome, one.to, one.content_id) == (edits.MOVE, THM, "c1")
    assert decided.hold("Deep House Low") == edits.Hold(skip=frozenset({"t1"}))
    assert decided.hold("Tech House Mid") == edits.Hold(keep=frozenset({"t1"}))
    assert [one.track for one in decided.carried] == ["t1"]


def test_a_track_taken_off_its_band_and_added_nowhere_is_unfiled():
    one = only(
        edits.decide(
            [
                held(DHL, account=(), rekordbox=("t1",), agreed=("t1",)),
                held(THM, account=(), rekordbox=(), agreed=()),
            ],
            OWNED,
        )
    )
    assert (one.outcome, one.to, one.content_id) == (edits.UNFILE, None, "c1")


def test_a_change_made_in_rekordbox_alone_is_no_edit_and_holds_nothing():
    decided = edits.decide(
        [
            held(DHL, account=("t1",), rekordbox=(), agreed=("t1",)),
            held(THM, account=(), rekordbox=("t1",), agreed=()),
        ],
        OWNED,
    )
    assert decided.decisions == () and decided.holds == {}


def test_a_playlist_never_agreed_reads_every_difference_as_rekordboxs():
    decided = edits.decide(
        [
            held(DHL, account=(), rekordbox=("t1",), never=True),
            held(THM, account=("t1",), rekordbox=(), never=True),
        ],
        OWNED,
    )
    assert decided.decisions == () and decided.holds == {}


def test_a_track_added_to_another_genres_with_vox_takes_that_genre():
    one = only(
        edits.decide(
            [
                held(DHL, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
                held(THV, account=("t1",), rekordbox=(), agreed=()),
            ],
            OWNED,
        )
    )
    assert (one.outcome, one.to) == (edits.FOLDER, THV)


def test_a_track_added_to_its_own_genres_with_vox_is_no_edit():
    decided = edits.decide(
        [
            held(DHL, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
            held(DHV, account=("t1",), rekordbox=(), agreed=()),
        ],
        OWNED,
    )
    assert decided.decisions == ()


def test_a_track_taken_off_a_with_vox_playlist_alone_is_no_edit():
    decided = edits.decide(
        [
            held(DHL, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
            held(DHV, account=(), rekordbox=("t1",), agreed=("t1",)),
        ],
        OWNED,
    )
    assert decided.decisions == () and decided.holds == {}


def test_a_track_left_in_one_of_two_bands_is_moved_to_the_one_left():
    one = only(
        edits.decide(
            [
                held(DHL, account=(), rekordbox=("t1",), agreed=("t1",)),
                held(DHM, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
            ],
            OWNED,
        )
    )
    assert (one.outcome, one.to) == (edits.MOVE, DHM)


# ═══════════════════════════════════════════════════════════════════════════
# 2. What is held, never carried and never undone
# ═══════════════════════════════════════════════════════════════════════════


def test_a_track_added_to_two_bands_at_once_is_held_on_both_sides():
    decided = edits.decide(
        [
            held(DHL, account=(), rekordbox=("t1",), agreed=("t1",)),
            held(THM, account=("t1",), agreed=()),
            held(THL, account=("t1",), agreed=()),
        ],
        OWNED,
    )
    one = only(decided)
    assert one.outcome == edits.HELD and "2 band playlists" in one.why
    assert decided.carried == ()
    assert decided.hold("Deep House Low").skip == {"t1"}
    assert decided.hold("Tech House Mid").keep == {"t1"}
    assert decided.hold("Tech House Low").keep == {"t1"}


def test_a_track_the_library_does_not_own_is_held_and_queued_for_download():
    decided = edits.decide([held(THM, account=("t9",), agreed=())], OWNED)
    one = only(decided)
    assert one.outcome == edits.HELD and one.acquire and "queued for download" in one.why
    assert one.to == THM
    assert decided.wanted == (one,)
    assert decided.hold("Tech House Mid").keep == {"t9"}


def test_a_track_two_library_rows_match_is_held():
    one = only(
        edits.decide([held(THM, account=("t1",), agreed=())], {"t1": ["c1", "c9"]})
    )
    assert one.outcome == edits.HELD and "2 library rows" in one.why


def test_a_track_taken_off_its_band_and_left_in_a_derived_playlist_is_held():
    one = only(
        edits.decide(
            [
                held(DHL, account=(), rekordbox=("t1",), agreed=("t1",)),
                held(DHV, account=("t1",), rekordbox=("t1",), agreed=("t1",)),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.HELD and "derived" in one.why


def test_a_short_listing_carries_no_edit_and_holds_what_it_read_differently():
    decided = edits.decide(
        [
            held(DHL, account=(), rekordbox=("t1",), agreed=("t1",), short=True),
            held(THM, account=("t1",), rekordbox=(), agreed=()),
        ],
        OWNED,
    )
    one = only(decided)
    assert one.outcome == edits.HELD and "short" in one.why
    assert decided.carried == ()
    assert decided.hold("Deep House Low").skip == {"t1"}


def test_a_short_listing_never_agreed_is_read_as_its_account_side():
    decided = edits.decide(
        [held(DHL, account=(), rekordbox=("t1",), never=True, short=True)], OWNED
    )
    assert decided.decisions == ()


# ═══════════════════════════════════════════════════════════════════════════
# 3. Both sides changed: the most recent change wins
# ═══════════════════════════════════════════════════════════════════════════


def test_both_sides_moving_a_track_to_one_place_agree():
    one = only(
        edits.decide(
            [
                held(DHL, account=(), rekordbox=(), agreed=("t1",)),
                held(THM, account=("t1",), rekordbox=("t1",), agreed=()),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.AGREED


def test_an_unfile_on_the_account_against_a_move_in_rekordbox_keeps_rekordboxs():
    one = only(
        edits.decide(
            [
                held(DHL, account=(), rekordbox=(), agreed=("t1",)),
                held(THM, account=(), rekordbox=("t1",), agreed=()),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.REKORDBOX and "an addition beats a removal" in one.why


def test_a_move_on_the_account_against_rekordbox_unfiling_it_is_carried():
    one = only(
        edits.decide(
            [
                held(DHL, account=(), rekordbox=(), agreed=("t1",)),
                held(THM, account=("t1",), rekordbox=(), agreed=()),
            ],
            OWNED,
        )
    )
    assert one.outcome == edits.MOVE and "an addition beats a removal" in one.why


def _both_moved(account_at: str, rekordbox_at: str) -> edits.Decision:
    return only(
        edits.decide(
            [
                held(DHL, account=(), rekordbox=(), agreed=("t1",)),
                held(THM, account=("t1",), rekordbox=(), agreed=(), account_added={"t1": account_at}),
                held(THL, account=(), rekordbox=("t1",), agreed=(), rekordbox_added={"t1": rekordbox_at}),
            ],
            OWNED,
        )
    )


def test_two_moves_follow_the_account_when_its_is_the_later():
    one = _both_moved("2026-11-04T12:00:00+00:00", "2026-11-04 10:00:00.000 +00:00")
    assert (one.outcome, one.to) == (edits.MOVE, THM)
    assert "later than rekordbox" in one.why


def test_two_moves_follow_rekordbox_when_its_is_the_later():
    one = _both_moved("2026-11-04T09:00:00+00:00", "2026-11-04 10:00:00.000 +00:00")
    assert one.outcome == edits.REKORDBOX and "rekordbox's place stands" in one.why


def test_two_moves_at_one_moment_keep_rekordboxs():
    one = _both_moved("2026-11-04T10:00:00+00:00", "2026-11-04 10:00:00.000 +00:00")
    assert one.outcome == edits.REKORDBOX


@pytest.mark.parametrize(
    "account_at, rekordbox_at",
    [("", "2026-11-04 10:00:00.000 +00:00"), ("2026-11-04T12:00:00+00:00", ""),
     ("2026-11-04T12:00:00", "2026-11-04 10:00:00.000 +00:00")],
)
def test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so(account_at, rekordbox_at):
    one = _both_moved(account_at, rekordbox_at)
    assert one.outcome == edits.REKORDBOX and "unknown" in one.why


def test_rekordbox_winning_holds_nothing_so_the_mirror_writes_its_place():
    decided = edits.decide(
        [
            held(DHL, account=(), rekordbox=(), agreed=("t1",)),
            held(THM, account=(), rekordbox=("t1",), agreed=()),
        ],
        OWNED,
    )
    assert decided.holds == {}


# ═══════════════════════════════════════════════════════════════════════════
# 4. The snapshot and the times
# ═══════════════════════════════════════════════════════════════════════════


def test_the_snapshot_after_keeps_its_word_on_a_held_track():
    hold = edits.Hold(keep=frozenset({"t1"}), skip=frozenset({"t2"}))
    after = edits.agreed_after(frozenset({"t2", "t3"}), {"t1", "t3", "t4"}, hold.tracks)
    assert after == {"t2", "t3", "t4"}


def test_a_playlist_never_agreed_takes_what_the_account_holds_after():
    assert edits.agreed_after(None, {"t1", "t2"}, ()) == {"t1", "t2"}
    assert edits.agreed_after(None, {"t1"}, {"t1"}) == {"t1"}


def test_a_time_is_read_with_its_zone_or_not_at_all():
    assert edits.moment("2026-11-04 10:00:00.000 +00:00") == datetime(
        2026, 11, 4, 10, tzinfo=timezone.utc
    )
    assert edits.moment("2026-11-04T10:00:00+00:00") == datetime(2026, 11, 4, 10, tzinfo=timezone.utc)
    assert edits.moment("2026-11-04T10:00:00") is None
    assert edits.moment("") is None
    assert edits.moment("not a time") is None


def test_a_decision_shows_its_places_on_the_gate():
    one = only(
        edits.decide(
            [
                held(DHL, account=(), rekordbox=("t1",), agreed=("t1",)),
                held(THM, account=("t1",), agreed=()),
            ],
            OWNED,
        )
    )
    assert one.item() == {
        "track": "t1",
        "outcome": edits.MOVE,
        "was": ["Deep House Low"],
        "account": ["Tech House Mid"],
        "rekordbox": ["Deep House Low"],
        "why": "put in Tech House Mid on the account",
        "to": "Tech House Mid",
        "content_id": "c1",
    }


def test_a_track_taken_off_its_band_and_put_in_its_own_genres_with_vox_is_held():
    """Round one, finding 3: the genre is unchanged and the band is gone."""
    decided = edits.decide(
        [
            held(DHL, account=(), rekordbox=("t1",), agreed=("t1",)),
            held(DHV, account=("t1",), rekordbox=(), agreed=()),
        ],
        OWNED,
    )
    one = only(decided)
    assert one.outcome == edits.HELD and "of its own genre" in one.why
    assert decided.carried == ()


def test_a_short_listing_reads_a_track_it_lists_and_holds_only_one_it_leaves_out():
    """Round one, finding 1: a listed track is on the account whatever the count says."""
    decided = edits.decide(
        [
            held(DHL, account=(), rekordbox=("t1",), agreed=("t1",)),
            held(THM, account=("t1",), rekordbox=(), agreed=(), short=True),
        ],
        OWNED,
    )
    one = only(decided)
    assert (one.outcome, one.to) == (edits.MOVE, THM)
