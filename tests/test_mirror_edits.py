"""U201: an account edit to a mirrored genre playlist, told apart and decided.

The pure rule, :func:`mirror_edits.decide`, over each playlist read three ways. D1 applies.
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
#: t1 in rekordbox and the snapshot, not on the account: taken off there.
OFF = dict(rekordbox=("t1",), agreed=("t1",))
#: t1 on every side, the snapshot included.
ALL = dict(account=("t1",), **OFF)


def held(place, *, account=(), rekordbox=(), agreed=(), never=False, short=False, placed=(), **times):
    """A playlist read three ways, with the placements the reader found still standing (U236)."""
    return edits.Mirrored(
        place=place, account=frozenset(account), rekordbox=frozenset(rekordbox),
        agreed=None if never else frozenset(agreed), short=short, placed=frozenset(placed),
        account_added=times.get("account_added", {}), rekordbox_added=times.get("rekordbox_added", {}),
    )


def decide(*playlists, owner=OWNED) -> edits.Decided:
    return edits.decide(list(playlists), owner)


def only(decided: edits.Decided) -> edits.Decision:
    (one,) = decided.decisions
    return one


def one(*playlists, owner=OWNED) -> edits.Decision:
    return only(decide(*playlists, owner=owner))


# 1. One side changed


def test_a_move_on_the_account_is_carried_and_the_mirror_holds_it():
    decided = decide(held(DHL, **OFF), held(THM, account=("t1",)))
    got = only(decided)
    assert (got.outcome, got.to, got.content_id) == (edits.MOVE, THM, "c1")
    assert decided.hold("Deep House Low") == edits.Hold(skip=frozenset({"t1"}))
    assert decided.hold("Tech House Mid") == edits.Hold(keep=frozenset({"t1"}))
    assert [got.track for got in decided.carried] == ["t1"]


def test_a_track_taken_off_its_band_and_added_nowhere_is_unfiled():
    got = one(held(DHL, **OFF), held(THM))
    assert (got.outcome, got.to, got.content_id) == (edits.UNFILE, None, "c1")


def test_a_playlist_never_agreed_reads_every_difference_as_rekordboxs():
    decided = decide(held(DHL, rekordbox=("t1",), never=True), held(THM, account=("t1",), never=True))
    assert decided.decisions == () and decided.holds == {}
    # A change made in rekordbox alone is no edit either, and holds nothing.
    decided = decide(held(DHL, account=("t1",), agreed=("t1",)), held(THM, rekordbox=("t1",)))
    assert decided.decisions == () and decided.holds == {}


def test_a_track_added_to_another_genres_with_vox_takes_that_genre():
    got = one(held(DHL, **ALL), held(THV, account=("t1",)))
    assert (got.outcome, got.to) == (edits.FOLDER, THV)


def test_a_track_added_to_its_own_genres_with_vox_is_no_edit():
    assert decide(held(DHL, **ALL), held(DHV, account=("t1",))).decisions == ()
    # Nor is one taken off a with vox playlist alone, which holds nothing.
    decided = decide(held(DHL, **ALL), held(DHV, **OFF))
    assert decided.decisions == () and decided.holds == {}


def test_a_track_left_in_one_of_two_bands_is_moved_to_the_one_left():
    got = one(held(DHL, **OFF), held(DHM, **ALL))
    assert (got.outcome, got.to) == (edits.MOVE, DHM)


# 2. What is held, never carried and never undone


def test_a_track_added_to_two_bands_at_once_is_held_on_both_sides():
    decided = decide(held(DHL, **OFF), held(THM, account=("t1",)), held(THL, account=("t1",)))
    got = only(decided)
    assert got.outcome == edits.HELD and "2 band playlists" in got.why
    assert decided.carried == ()
    assert decided.hold("Deep House Low").skip == {"t1"}
    assert decided.hold("Tech House Mid").keep == {"t1"}
    assert decided.hold("Tech House Low").keep == {"t1"}


def test_a_track_the_library_does_not_own_is_held_and_queued_for_download():
    decided = decide(held(THM, account=("t9",)))
    got = only(decided)
    assert got.outcome == edits.HELD and got.acquire and "queued for download" in got.why
    assert got.to == THM
    assert decided.wanted == (got,)
    assert decided.hold("Tech House Mid").keep == {"t9"}


def test_a_track_two_library_rows_match_is_held():
    got = one(held(THM, account=("t1",)), owner={"t1": ["c1", "c9"]})
    assert got.outcome == edits.HELD and "2 library rows" in got.why


def test_a_track_taken_off_its_band_and_left_in_a_derived_playlist_is_held():
    got = one(held(DHL, **OFF), held(DHV, **ALL))
    assert got.outcome == edits.HELD and "derived" in got.why


def test_a_short_listing_carries_no_edit_and_holds_what_it_read_differently():
    decided = decide(held(DHL, short=True, **OFF), held(THM, account=("t1",)))
    got = only(decided)
    assert got.outcome == edits.HELD and "short" in got.why
    assert decided.carried == ()
    assert decided.hold("Deep House Low").skip == {"t1"}
    # One never agreed is read as its account side.
    assert decide(held(DHL, rekordbox=("t1",), never=True, short=True)).decisions == ()


# 3. Both sides changed: the most recent change wins


def test_both_sides_moving_a_track_to_one_place_agree():
    got = one(held(DHL, agreed=("t1",)), held(THM, account=("t1",), rekordbox=("t1",)))
    assert got.outcome == edits.AGREED


def test_an_unfile_on_the_account_against_a_move_in_rekordbox_keeps_rekordboxs():
    decided = decide(held(DHL, agreed=("t1",)), held(THM, rekordbox=("t1",)))
    got = only(decided)
    assert got.outcome == edits.REKORDBOX and "an addition beats a removal" in got.why
    # Rekordbox winning holds nothing, so the mirror writes its place.
    assert decided.holds == {}


def test_a_move_on_the_account_against_rekordbox_unfiling_it_is_carried():
    got = one(held(DHL, agreed=("t1",)), held(THM, account=("t1",)))
    assert got.outcome == edits.MOVE and "an addition beats a removal" in got.why


def _both_moved(account_at: str, rekordbox_at: str) -> edits.Decision:
    return one(
        held(DHL, agreed=("t1",)),
        held(THM, account=("t1",), account_added={"t1": account_at}),
        held(THL, rekordbox=("t1",), rekordbox_added={"t1": rekordbox_at}),
    )


def test_two_moves_follow_the_account_when_its_is_the_later():
    got = _both_moved("2026-11-04T12:00:00+00:00", "2026-11-04 10:00:00.000 +00:00")
    assert (got.outcome, got.to) == (edits.MOVE, THM)
    assert "later than rekordbox" in got.why


def test_two_moves_at_one_moment_keep_rekordboxs():
    got = _both_moved("2026-11-04T10:00:00+00:00", "2026-11-04 10:00:00.000 +00:00")
    assert got.outcome == edits.REKORDBOX
    # And so do two moves where rekordbox's is the later.
    got = _both_moved("2026-11-04T09:00:00+00:00", "2026-11-04 10:00:00.000 +00:00")
    assert got.outcome == edits.REKORDBOX and "rekordbox's place stands" in got.why


@pytest.mark.parametrize(
    "account_at, rekordbox_at",
    [("", "2026-11-04 10:00:00.000 +00:00"), ("2026-11-04T12:00:00+00:00", ""),
     ("2026-11-04T12:00:00", "2026-11-04 10:00:00.000 +00:00")],
)
def test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so(account_at, rekordbox_at):
    got = _both_moved(account_at, rekordbox_at)
    assert got.outcome == edits.REKORDBOX and "unknown" in got.why


# 4. The snapshot and the times


def test_the_snapshot_after_keeps_its_word_on_a_held_track():
    hold = edits.Hold(keep=frozenset({"t1"}), skip=frozenset({"t2"}))
    after = edits.agreed_after(frozenset({"t2", "t3"}), {"t1", "t3", "t4"}, hold.tracks)
    assert after == {"t2", "t3", "t4"}
    # A playlist never agreed takes what the account holds after.
    assert edits.agreed_after(None, {"t1", "t2"}, ()) == {"t1", "t2"}
    assert edits.agreed_after(None, {"t1"}, {"t1"}) == {"t1"}


def test_a_time_is_read_with_its_zone_or_not_at_all():
    ten = datetime(2026, 11, 4, 10, tzinfo=timezone.utc)
    assert edits.moment("2026-11-04 10:00:00.000 +00:00") == ten
    assert edits.moment("2026-11-04T10:00:00+00:00") == ten
    for unknown in ("2026-11-04T10:00:00", "", "not a time"):
        assert edits.moment(unknown) is None


def test_a_decision_shows_its_places_on_the_gate():
    shown = one(held(DHL, **OFF), held(THM, account=("t1",))).item()
    assert shown == {
        "track": "t1", "outcome": edits.MOVE, "was": ["Deep House Low"],
        "account": ["Tech House Mid"], "rekordbox": ["Deep House Low"],
        "why": "put in Tech House Mid on the account", "to": "Tech House Mid", "content_id": "c1",
    }


def test_a_track_taken_off_its_band_and_put_in_its_own_genres_with_vox_is_held():
    """Round one, finding 3: the genre is unchanged and the band is gone."""
    decided = decide(held(DHL, **OFF), held(DHV, account=("t1",)))
    got = only(decided)
    assert got.outcome == edits.HELD and "of its own genre" in got.why
    assert decided.carried == ()


def test_a_short_listing_reads_a_track_it_lists_and_holds_only_one_it_leaves_out():
    """Round one, finding 1: a listed track is on the account whatever the count says."""
    got = one(held(DHL, **OFF), held(THM, account=("t1",), short=True))
    assert (got.outcome, got.to) == (edits.MOVE, THM)


# U204. The Favorites folder and INBOX, each by its own rule

AF = edits.Place("All Favorites", "Favorites", "All Favorites", True, edits.FAVORITES)
OCT = edits.Place("Favorites 2026-10", "Favorites", "2026-10", False, edits.FAVORITES)
NOV = edits.Place("Favorites 2026-11", "Favorites", "2026-11", False, edits.FAVORITES)
BA = edits.Place("INBOX A", "INBOX", "A", True, edits.INBOX)
BB = edits.Place("INBOX B", "INBOX", "B", True, edits.INBOX)


def test_a_track_put_in_all_favorites_is_favourited_with_its_added_time():
    at = "2026-09-14T10:00:00+00:00"
    decided = decide(held(AF, account=("t1",), account_added={"t1": at}), held(OCT))
    got = only(decided)
    assert (got.outcome, got.to, got.content_id) == (edits.FAVOURITE, AF, "c1")
    assert got.tree == edits.FAVORITES
    assert (got.when, got.filed) == (at, False)
    assert decided.hold("All Favorites").keep == {"t1"}
    # Settled where both sides will agree: All Favorites, and the month it is not in.
    assert set(got.settle) == {("Favorites", AF.title, True), ("Favorites", OCT.title, False)}


def test_a_track_put_in_all_favorites_that_sits_in_a_month_takes_no_month():
    got = one(held(AF, account=("t1",)), held(OCT, **ALL))
    assert got.outcome == edits.FAVOURITE and got.filed is True


def test_a_track_put_in_a_month_is_favourited_there():
    got = one(held(AF), held(OCT, account=("t1",)))
    assert (got.outcome, got.to) == (edits.FAVOURITE, OCT)


def test_a_track_taken_off_all_favorites_is_unfavourited_and_settled_out_of_the_folder():
    got = one(held(AF, **OFF), held(OCT, **ALL))
    assert (got.outcome, got.to, got.content_id) == (edits.UNFAVOURITE, None, "c1")
    # The month the account still holds it in keeps the snapshot's word, so it comes off.
    assert got.settle == (("Favorites", "All Favorites", False),)


@pytest.mark.parametrize(
    ("af", "oct_", "nov", "why"),
    [
        (ALL, OFF, {}, "listed and not carried"),
        (ALL, dict(account=("t1",)), dict(account=("t1",)), "2 month playlists"),
        (OFF, {}, dict(account=("t1",)), "at once"),
    ],
)
def test_a_favorites_edit_the_account_does_not_decide_is_held(af, oct_, nov, why):
    decided = decide(held(AF, **af), held(OCT, **oct_), held(NOV, **nov))
    got = only(decided)
    assert got.outcome == edits.HELD and why in got.why
    assert got.tree == edits.FAVORITES and decided.carried == ()


def test_an_unfavourite_against_a_month_rekordbox_added_since_keeps_rekordboxs():
    got = one(held(AF, **OFF), held(NOV, rekordbox=("t1",)))
    assert got.outcome == edits.REKORDBOX and "addition beats a removal" in got.why


def test_a_favourite_or_an_unfavourite_rekordbox_made_too_is_agreed():
    assert one(held(AF, agreed=("t1",)), held(OCT, agreed=("t1",))).outcome == edits.AGREED
    assert one(held(AF, account=("t1",), rekordbox=("t1",))).outcome == edits.AGREED


def test_two_months_follow_the_later_addition():
    def moved(account_at: str) -> edits.Decision:
        return one(
            held(AF, **ALL),
            held(OCT, account=("t1",), account_added={"t1": account_at}),
            held(NOV, rekordbox=("t1",), rekordbox_added={"t1": "2026-11-03 10:00:00.000 +00:00"}),
        )

    assert moved("2026-11-04T10:00:00+00:00").outcome == edits.FAVOURITE
    assert moved("2026-11-02T10:00:00+00:00").outcome == edits.REKORDBOX


def test_a_short_favorites_listing_holds_what_it_left_out():
    got = one(held(AF, short=True, **OFF))
    assert got.outcome == edits.HELD and "short" in got.why


def test_an_inbox_track_put_in_joins_and_one_taken_off_leaves():
    decided = decide(
        held(BA, account=("t1", "t2"), rekordbox=("t1",), agreed=("t1",)),
        held(BB, rekordbox=("t2",), agreed=("t2",)),
    )
    found = {(got.outcome, got.to.title) for got in decided.decisions}
    assert found == {(edits.JOIN, "INBOX A"), (edits.LEAVE, "INBOX B")}
    join = next(got for got in decided.decisions if got.outcome == edits.JOIN)
    assert join.settle == (("INBOX", "INBOX A", True),)
    assert decided.hold("INBOX A").keep == {"t2"}
    assert decided.hold("INBOX B").skip == {"t2"}


def test_an_inbox_change_both_sides_made_is_agreed():
    decided = decide(held(BA, account=("t2",), rekordbox=("t2",)), held(BB, agreed=("t1",)))
    assert {got.outcome for got in decided.decisions} == {edits.AGREED}
    assert decided.holds == {}


def test_a_hold_in_one_tree_is_never_a_hold_in_another():
    decided = decide(held(DHL, **OFF), held(THM, account=("t1",)), held(AF, rekordbox=("t1",)))
    assert only(decided).tree == edits.GENRE
    # All Favorites differs, but the Favorites tree's own rule holds nothing.
    assert decided.hold("All Favorites") == edits.Hold()


def test_an_addition_the_library_lacks_is_queued_in_favorites_and_inbox_and_a_known_one_never():
    decided = decide(
        held(AF, account=("t9",)),
        held(BA, account=("t9",)),
        held(BB, account=("t8",)),
        held(DHL, account=("t8",), agreed=("t8",)),
    )
    wanted = {(got.tree, got.acquire) for got in decided.decisions if got.track == "t9"}
    assert wanted == {(edits.FAVORITES, True), (edits.INBOX, True)}
    assert [got.track for got in decided.wanted] == ["t9", "t9"]
    # t8 sits in a genre snapshot, so it left the collection: held, never fetched.
    gone = next(got for got in decided.decisions if got.track == "t8")
    assert gone.outcome == edits.HELD and not gone.acquire


def test_an_inbox_edit_holds_its_own_batch_and_no_other():
    """Review round one, finding 6: a join on A no longer holds rekordbox's addition to B."""
    decided = decide(held(BA, account=("t1",)), held(BB, rekordbox=("t1",)))
    assert only(decided).outcome == edits.JOIN
    assert decided.hold("INBOX A").keep == {"t1"}
    assert decided.hold("INBOX B") == edits.Hold()


def test_a_month_move_leaves_the_month_it_was_taken_off():
    """Review round one, finding 1."""
    got = one(held(AF, **ALL), held(OCT, **OFF), held(NOV, account=("t1",)))
    assert (got.outcome, got.to, got.away) == (edits.FAVOURITE, NOV, (OCT,))
    assert set(got.settle) == {
        ("Favorites", "All Favorites", True),
        ("Favorites", "Favorites 2026-10", False),
        ("Favorites", "Favorites 2026-11", True),
    }


def test_an_unfavourite_rekordbox_made_in_all_favorites_alone_is_still_carried():
    """Mutation row P7: rekordbox took it off All Favorites and kept its month, so not agreed."""
    assert one(held(AF, agreed=("t1",)), held(OCT, **ALL)).outcome == edits.UNFAVOURITE
