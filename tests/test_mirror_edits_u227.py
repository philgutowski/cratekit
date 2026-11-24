"""U227: a track queued by an account edit is filed where the edit put it; the landing's own
filing is the landing's and the edit is carried once. Pure."""

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


def _m(place, *, account=False, rekordbox=False, agreed=False, **added) -> edits.Mirrored:
    """``place`` read three ways, each side holding t9 or not, the snapshot never ``None``."""
    def t9(on: bool) -> frozenset[str]:
        return frozenset({"t9"}) if on else frozenset()
    return edits.Mirrored(place, t9(account), t9(rekordbox), t9(agreed), **added)


def _read(*, rekordbox_in=AHH, at=LANDED_AT, also=(), known=False):
    """Jazz Med edited on the account, the row placed in ``rekordbox_in`` at ``at``."""
    placed = (rekordbox_in, *also)
    return [
        _m(
            place,
            account=place == JZM or (known and place == AHH),
            agreed=known and place == AHH,
            rekordbox=place in placed,
            account_added={"t9": ACCOUNT_AT} if place == JZM else {},
            rekordbox_added={"t9": at} if place in placed else {},
        )
        for place in (JZM, AHH, AHM)
    ]


def _one(playlists, filed=FILED) -> edits.Decision:
    (one,) = edits.decide(playlists, OWNED, filed).decisions
    return one


def test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it():
    one = _one(_read())
    assert (one.outcome, one.to, one.content_id) == (edits.MOVE, JZM, "c9")
    assert "landed for the account's edit" in one.why and "Afro House High" in one.why
    assert one.landed and one.item()["landed"] is True
    # Without the landing's record the later change rule stands as before.
    one = _one(_read(), None)
    assert one.outcome == edits.REKORDBOX and "rekordbox's place stands" in one.why
    assert not one.landed and "landed" not in one.item()
    # A track whose landing filed it nowhere is carried as before.
    one = _one(_read(rekordbox_in=None))
    assert (one.outcome, one.to) == (edits.MOVE, JZM) and not one.landed


def test_a_move_made_in_rekordbox_after_the_landing_stands():
    one = _one(_read(rekordbox_in=AHM, at=MOVED_AT))
    assert one.outcome == edits.REKORDBOX
    assert "Afro House Med" in one.why and "rekordbox's place stands" in one.why
    assert not one.landed


def test_a_second_band_added_in_rekordbox_after_the_landing_stands():
    one = _one(_read(also=(AHM,)))
    assert one.outcome == edits.REKORDBOX and not one.landed


def test_another_genres_band_of_the_landings_name_is_not_the_landings():
    """A landing filed into Afro House High; Jazz High is rekordbox's place, not the landing's."""
    jzh = edits.Place("Jazz High", "Jazz", "High", True)
    jazz_med = _m(JZM, account=True, account_added={"t9": ACCOUNT_AT})
    one = _one([jazz_med, _m(jzh, rekordbox=True, rekordbox_added={"t9": LANDED_AT})])
    assert one.outcome == edits.REKORDBOX and not one.landed


def test_a_track_a_snapshot_held_is_read_by_the_later_change_rule_alone():
    """ONCE: the snapshot holds the carried track and the account is unchanged, so no landing is read."""
    playlists = [_m(JZM, account=True, agreed=True), _m(AHH, rekordbox=True, rekordbox_added={"t9": LANDED_AT})]
    assert edits.decide(playlists, OWNED, FILED).decisions == ()


def test_a_landing_filed_into_the_place_the_account_asked_agrees():
    one = _one(_read(rekordbox_in=JZM), {"t9": frozenset({("Jazz", "Med")})})
    assert one.outcome == edits.AGREED


def test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band():
    one = _one([_m(JZV, account=True), _m(AHH, rekordbox=True, rekordbox_added={"t9": LANDED_AT})])
    assert (one.outcome, one.to) == (edits.FOLDER, JZV)
    assert one.landed


def test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands():
    """K1: once the snapshot holds the track, a move back into the landing's band is rekordbox's."""
    jzh = edits.Place("Jazz High", "Jazz", "High", True)
    one = _one(
        [
            _m(JZM, agreed=True),
            _m(jzh, account=True, account_added={"t9": "2026-11-07T17:00:00+00:00"}),
            _m(AHH, rekordbox=True, rekordbox_added={"t9": "2026-11-07 18:00:00.000 +00:00"}),
        ]
    )
    assert one.outcome == edits.REKORDBOX
    assert not one.landed and "rekordbox's place stands" in one.why
