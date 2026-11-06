"""U227: a track queued for download by an account edit is filed where the edit put it.

Sitting 85 put a track the library lacked in a mirrored genre playlist on the
account. The mirror queued its download, the landing filed it by its own tags
into another band, and the next plan read that filing as a change made in
rekordbox later than the account's, so rekordbox's place stood and the mirror
would have taken the track off the playlist the person put it in. The landing's
own filing is not a person's change: the rule here reads it as the landing's,
by the places the landing filed the row into, and carries the account's edit
once. A change made in rekordbox after the landing still goes by the later
change rule.

Pure: the rule reads nothing, so every reading is driven here without a
database, an account or a queue.
"""

from __future__ import annotations

from cratekit.modules.outbound import mirror_edits as edits

AHH = edits.Place("Afro House High", "Afro House", "High", True)
AHM = edits.Place("Afro House Med", "Afro House", "Med", True)
JZM = edits.Place("Jazz Med", "Jazz", "Med", True)
JZV = edits.Place("Jazz with vox", "Jazz", "with vox", False)

OWNED = {"t9": ["c9"]}
#: When the account put it in Jazz Med, and when rekordbox placed it since.
ACCOUNT_AT = "2026-11-06T14:56:32.535000+00:00"
LANDED_AT = "2026-11-06 15:11:15.593 +00:00"
MOVED_AT = "2026-11-06 16:00:00.000 +00:00"
#: Where the landing filed the row, by the adoption ledger.
FILED = {"t9": frozenset({("Afro House", "High")})}


def _read(*, rekordbox_in=AHH, at=LANDED_AT, also=(), known=()):
    """Jazz Med edited on the account, the row placed in ``rekordbox_in`` at ``at``."""
    playlists = [
        edits.Mirrored(
            place=JZM,
            account=frozenset({"t9"}),
            rekordbox=frozenset({"t9"}) if rekordbox_in == JZM else frozenset(),
            agreed=frozenset(),
            account_added={"t9": ACCOUNT_AT},
            rekordbox_added={"t9": at} if rekordbox_in == JZM else {},
        ),
    ]
    for place in (AHH, AHM):
        playlists.append(
            edits.Mirrored(
                place=place,
                account=frozenset(known) if place == AHH else frozenset(),
                rekordbox=frozenset({"t9"}) if place in (rekordbox_in, *also) else frozenset(),
                agreed=frozenset(known) if place == AHH else frozenset(),
                rekordbox_added={"t9": at} if place in (rekordbox_in, *also) else {},
            )
        )
    return playlists


def _only(decided: edits.Decided) -> edits.Decision:
    (one,) = decided.decisions
    return one


def test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it():
    one = _only(edits.decide(_read(), OWNED, FILED))
    assert (one.outcome, one.to, one.content_id) == (edits.MOVE, JZM, "c9")
    assert "landed for the account's edit" in one.why
    assert "Afro House High" in one.why
    assert one.landed and one.item()["landed"] is True


def test_without_the_landings_record_the_later_change_rule_stands_as_before():
    one = _only(edits.decide(_read(), OWNED))
    assert one.outcome == edits.REKORDBOX
    assert "rekordbox's place stands" in one.why
    assert not one.landed and "landed" not in one.item()


def test_a_move_made_in_rekordbox_after_the_landing_stands():
    one = _only(edits.decide(_read(rekordbox_in=AHM, at=MOVED_AT), OWNED, FILED))
    assert one.outcome == edits.REKORDBOX
    assert "Afro House Med" in one.why and "rekordbox's place stands" in one.why
    assert not one.landed


def test_a_second_band_added_in_rekordbox_after_the_landing_stands():
    one = _only(edits.decide(_read(also=(AHM,)), OWNED, FILED))
    assert one.outcome == edits.REKORDBOX
    assert not one.landed


def test_a_track_a_snapshot_held_is_read_by_the_later_change_rule_alone():
    """ONCE: after the edit is carried the snapshot holds the track, and the
    landing's record never decides it again."""
    playlists = [
        edits.Mirrored(
            place=JZM,
            account=frozenset({"t9"}),
            agreed=frozenset({"t9"}),
            rekordbox=frozenset(),
        ),
        edits.Mirrored(
            place=AHH,
            account=frozenset(),
            agreed=frozenset(),
            rekordbox=frozenset({"t9"}),
            rekordbox_added={"t9": LANDED_AT},
        ),
    ]
    decided = edits.decide(playlists, OWNED, FILED)
    # The account side did not change since the snapshot, so rekordbox's move
    # is no account edit at all, and the landing's record is not read.
    assert decided.decisions == ()


def test_a_landing_filed_into_the_place_the_account_asked_agrees():
    one = _only(edits.decide(_read(rekordbox_in=JZM), OWNED, {"t9": frozenset({("Jazz", "Med")})}))
    assert one.outcome == edits.AGREED


def test_a_track_whose_landing_filed_it_nowhere_is_carried_as_before():
    one = _only(edits.decide(_read(rekordbox_in=None), OWNED, FILED))
    assert (one.outcome, one.to) == (edits.MOVE, JZM)
    assert not one.landed


def test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band():
    playlists = [
        edits.Mirrored(place=JZV, account=frozenset({"t9"}), agreed=frozenset()),
        edits.Mirrored(
            place=AHH,
            rekordbox=frozenset({"t9"}),
            agreed=frozenset(),
            rekordbox_added={"t9": LANDED_AT},
        ),
    ]
    one = _only(edits.decide(playlists, OWNED, FILED))
    assert (one.outcome, one.to) == (edits.FOLDER, JZV)
    assert one.landed


def test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands():
    """ONCE, pinned (the review of U227, K1): once the snapshot holds the track,
    a person's move back into the band its landing first filed is rekordbox's
    change, even though the ledger still names that band."""
    jzh = edits.Place("Jazz High", "Jazz", "High", True)
    playlists = [
        edits.Mirrored(place=JZM, account=frozenset(), agreed=frozenset({"t9"})),
        edits.Mirrored(
            place=jzh,
            account=frozenset({"t9"}),
            agreed=frozenset(),
            account_added={"t9": "2026-11-07T17:00:00+00:00"},
        ),
        edits.Mirrored(
            place=AHH,
            agreed=frozenset(),
            rekordbox=frozenset({"t9"}),
            rekordbox_added={"t9": "2026-11-07 18:00:00.000 +00:00"},
        ),
    ]
    one = _only(edits.decide(playlists, OWNED, FILED))
    assert one.outcome == edits.REKORDBOX
    assert not one.landed and "rekordbox's place stands" in one.why
