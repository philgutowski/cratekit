"""U230: a download an account edit queued is filed there even when that playlist already lists it.

The base of the playlist whose job queued the track is read without it while the landing's
filing stands; every other base counts as before. Pure.
"""

from __future__ import annotations

from cratekit.modules.outbound import mirror_edits as edits
from tests.test_mirror_edits_u227 import ACCOUNT_AT, AHH, AHM, FILED, JZM, JZV, LANDED_AT, MOVED_AT

OWNED = {"t9": ["c9"]}

T9 = frozenset({"t9"})
NONE = frozenset()
#: Which mirrored playlist's job queued the download.
QUEUED = {"t9": frozenset({"Jazz Med"})}


def _read(*, agreed=None, rekordbox_in=(AHH,), at=LANDED_AT, edited=JZM, others=None):
    """The edited playlist listing t9, snapshot ``agreed``; ``others`` maps a band to its two sides."""
    others = others or {}
    def side(place) -> dict:
        return {"rekordbox": T9, "rekordbox_added": {"t9": at}} if place in rekordbox_in else {}
    playlists = [edits.Mirrored(edited, T9, agreed=agreed, account_added={"t9": ACCOUNT_AT}, **side(edited))]
    for place in (AHH, AHM):
        snapshot, account = others.get(place, (NONE, NONE))
        playlists.append(edits.Mirrored(place, account, agreed=snapshot, **side(place)))
    return playlists


def _decided(playlists, filed=FILED, queued=QUEUED) -> tuple[edits.Decision, ...]:
    return edits.decide(playlists, OWNED, filed, queued).decisions


def _one(playlists, filed=FILED, queued=QUEUED) -> edits.Decision:
    (one,) = _decided(playlists, filed, queued)
    return one


# The brief's shapes: the edited playlist's base holds the track


def test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it():
    """Sitting 86's shape: the account side is the base, and it holds the track."""
    one = _one(_read())
    assert (one.outcome, one.to, one.content_id) == (edits.MOVE, JZM, "c9")
    assert one.landed and one.item()["landed"] is True
    assert "landed for the account's edit" in one.why and "Afro House High" in one.why


def test_an_agreed_snapshot_that_holds_the_track_is_the_librarys_word():
    """An agreed snapshot takes a queued track only once the library took the edit: never lifted."""
    assert _decided(_read(agreed=T9)) == ()
    # Only the base of the playlist whose job queued the track is lifted.
    assert _decided(_read(agreed=T9), queued={"t9": frozenset({"Jazz High"})}) == ()


def test_the_same_reading_without_the_queue_is_no_edit_at_all_as_before():
    """A track the queue does not name reads as U227 reads it: no account change."""
    assert _decided(_read(agreed=T9), queued=None) == ()
    assert _decided(_read(), queued={}) == ()
    # Nor for a queued track with no landing places: a landing that filed
    # nothing, or one an adopt apply replaced (U227 round two).
    assert _decided(_read(agreed=T9), filed={}) == ()
    assert _decided(_read(), filed=None) == ()


def test_another_playlists_snapshot_holding_the_track_is_never_read_as_landed():
    """A row owned before the download: the later change rule decides."""
    one = _one(_read(agreed=T9, others={AHM: (T9, NONE)}))
    assert one.outcome == edits.REKORDBOX
    assert not one.landed and "rekordbox's place stands" in one.why


def test_another_playlist_the_account_still_lists_it_on_counts_too():
    one = _one(_read(others={AHM: (T9, T9)}))
    assert one.outcome == edits.REKORDBOX and not one.landed


def test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too():
    one = _one(_read(edited=JZV), queued={"t9": frozenset({JZV.title})})
    assert (one.outcome, one.to) == (edits.FOLDER, JZV)
    assert one.landed


# Once: the exclusion U227 meant still holds


def test_once_the_library_holds_it_where_the_account_put_it_nothing_is_read():
    """Rekordbox holds it in Jazz Med, which the landing did not file."""
    assert _decided(_read(agreed=T9, rekordbox_in=(JZM,))) == ()
    # A move in rekordbox after the carry is rekordbox's, and so is a second band.
    assert _decided(_read(agreed=T9, rekordbox_in=(AHM,), at=MOVED_AT)) == ()
    assert _decided(_read(agreed=T9, rekordbox_in=(AHH, AHM))) == ()


def test_a_later_account_move_then_a_rekordbox_move_back_into_the_landings_band_stands():
    """U227's K1 with the queue named: off the queuing playlist, its snapshot counts."""
    jzh = edits.Place("Jazz High", "Jazz", "High", True)
    one = _one(
        [
            edits.Mirrored(JZM, NONE, agreed=T9),
            edits.Mirrored(jzh, T9, agreed=NONE, account_added={"t9": "2026-11-07T17:00:00+00:00"}),
            edits.Mirrored(AHH, NONE, T9, NONE, rekordbox_added={"t9": "2026-11-07 18:00:00.000 +00:00"}),
        ]
    )
    assert one.outcome == edits.REKORDBOX
    assert not one.landed and "rekordbox's place stands" in one.why


def test_a_landing_filed_where_the_account_asked_is_no_edit():
    """The library already holds it where the account put it, run after run."""
    filed = {"t9": frozenset({("Jazz", "Med")})}
    assert _decided(_read(rekordbox_in=(JZM,)), filed=filed) == ()


def test_a_short_listing_of_the_queuing_playlist_lifts_nothing():
    """The review of U230, round one: a short listing carries no edit of its own."""
    for agreed in (None, T9):
        playlists = _read(agreed=agreed)
        playlists[0] = edits.Mirrored(JZM, T9, agreed=agreed, short=True, account_added={"t9": ACCOUNT_AT})
        assert _decided(playlists) == (), agreed


def test_a_band_a_person_chose_before_any_carry_is_not_lifted_over():
    """A row a person moved, or gave a second band, in rekordbox before the carry is no edit."""
    for rekordbox_in, at in (((AHM,), MOVED_AT), ((AHH, AHM), LANDED_AT)):
        assert _decided(_read(rekordbox_in=rekordbox_in, at=at)) == (), rekordbox_in


def test_a_row_taken_out_of_the_tree_in_rekordbox_is_not_lifted_over():
    """A row in no band has no landing's filing standing to beat a person's removal."""
    assert _decided(_read(rekordbox_in=())) == ()
