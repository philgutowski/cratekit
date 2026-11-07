"""U230: a download an account edit queued is filed there even when that playlist already lists it.

Sitting 86 read U227 live: a track a person put on a mirrored genre playlist
on the account, which the library lacked and the mirror queued, landed and
was filed by its own tags into another band. U227 carries the account's edit
over that filing only for a track no snapshot ever held. The brief reads the
playlist the person edited as holding the track in its own base, its
snapshot or, for a playlist never agreed, its account side, so the rule never
fired and rekordbox's place stood.

The rule here: the base of the playlist whose mirror job queued the track is
read without it, as it stood when the download was queued, while the
landing's filing stands and the account still lists the track there. Every
other playlist's base counts as before, so a row another playlist held is
never read as landed, and once the library holds the track where the account
put it the edit is read no more.

Pure: the rule reads nothing, so every reading is driven without a database,
an account or a queue.
"""

from __future__ import annotations

from cratekit.modules.outbound import mirror_edits as edits

AHH = edits.Place("Afro House High", "Afro House", "High", True)
AHM = edits.Place("Afro House Med", "Afro House", "Med", True)
JZM = edits.Place("Jazz Med", "Jazz", "Med", True)
JZV = edits.Place("Jazz with vox", "Jazz", "with vox", False)

OWNED = {"t9": ["c9"]}
ACCOUNT_AT = "2026-11-06T14:56:32.535000+00:00"
LANDED_AT = "2026-11-06 15:11:15.593 +00:00"
MOVED_AT = "2026-11-06 16:00:00.000 +00:00"
#: Where the landing filed the row, by the adoption ledger.
FILED = {"t9": frozenset({("Afro House", "High")})}
#: Which mirrored playlist's job queued the download.
QUEUED = {"t9": frozenset({"Jazz Med"})}


def _read(
    *,
    agreed=None,
    rekordbox_in=(AHH,),
    at=LANDED_AT,
    edited=JZM,
    on_account=True,
    others=None,
):
    """The edited playlist holding the track on the account, the row placed in ``rekordbox_in``.

    ``agreed`` is the edited playlist's snapshot, ``None`` for one never
    agreed, whose account side is then its base. ``others`` maps a band to its
    snapshot and account side, for another playlist that held the track.
    """
    others = others or {}
    playlists = [
        edits.Mirrored(
            place=edited,
            account=frozenset({"t9"}) if on_account else frozenset(),
            rekordbox=frozenset({"t9"}) if edited in rekordbox_in else frozenset(),
            agreed=agreed,
            account_added={"t9": ACCOUNT_AT} if on_account else {},
            rekordbox_added={"t9": at} if edited in rekordbox_in else {},
        )
    ]
    for place in (AHH, AHM):
        snapshot, account = others.get(place, (frozenset(), frozenset()))
        playlists.append(
            edits.Mirrored(
                place=place,
                account=account,
                rekordbox=frozenset({"t9"}) if place in rekordbox_in else frozenset(),
                agreed=snapshot,
                rekordbox_added={"t9": at} if place in rekordbox_in else {},
            )
        )
    return playlists


def _only(decided: edits.Decided) -> edits.Decision:
    (one,) = decided.decisions
    return one


# ═══════════════════════════════════════════════════════════════════════════
# The brief's shapes: the edited playlist's base holds the track
# ═══════════════════════════════════════════════════════════════════════════


def test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it():
    """Sitting 86's shape: the account side is the base, and it holds the track."""
    one = _only(edits.decide(_read(agreed=None), OWNED, FILED, QUEUED))
    assert (one.outcome, one.to, one.content_id) == (edits.MOVE, JZM, "c9")
    assert one.landed and one.item()["landed"] is True
    assert "landed for the account's edit" in one.why and "Afro House High" in one.why


def test_an_agreed_snapshot_that_holds_the_track_is_the_librarys_word():
    """The brief asked for this carried; the review of U230, round one, drove
    the producers and found an agreed snapshot of the queuing playlist takes
    a queued track only once the library took the edit, so lifting it carried
    a person's later move back. It is read as U227 reads it."""
    assert edits.decide(_read(agreed=frozenset({"t9"})), OWNED, FILED, QUEUED).decisions == ()


def test_the_same_reading_without_the_queue_is_no_edit_at_all_as_before():
    """Nothing changes for a track the queue does not name: the base holds it on
    the account's side, so the account changed nothing and rekordbox's side is
    mirrored, U227's reading."""
    assert edits.decide(_read(agreed=frozenset({"t9"})), OWNED, FILED).decisions == ()
    assert edits.decide(_read(agreed=None), OWNED, FILED, {}).decisions == ()


def test_a_queued_track_with_no_landing_places_is_read_as_before():
    """Nothing changes for a track with no filed places (U227 round two kept):
    a landing that filed nothing, or one a person's adopt apply replaced."""
    assert edits.decide(_read(agreed=frozenset({"t9"})), OWNED, {}, QUEUED).decisions == ()
    assert edits.decide(_read(agreed=None), OWNED, None, QUEUED).decisions == ()


def test_another_playlists_snapshot_holding_the_track_is_never_read_as_landed():
    """A row the library owned before the download: another playlist's snapshot
    held it, so the landing's filing is not the only word and the later change
    rule decides."""
    held = (frozenset({"t9"}), frozenset())
    one = _only(
        edits.decide(_read(agreed=frozenset({"t9"}), others={AHM: held}), OWNED, FILED, QUEUED)
    )
    assert one.outcome == edits.REKORDBOX
    assert not one.landed and "rekordbox's place stands" in one.why


def test_another_playlist_the_account_still_lists_it_on_counts_too():
    held = (frozenset({"t9"}), frozenset({"t9"}))
    one = _only(edits.decide(_read(agreed=None, others={AHM: held}), OWNED, FILED, QUEUED))
    assert one.outcome == edits.REKORDBOX and not one.landed


def test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too():
    one = _only(
        edits.decide(_read(agreed=None, edited=JZV), OWNED, FILED, {"t9": frozenset({JZV.title})})
    )
    assert (one.outcome, one.to) == (edits.FOLDER, JZV)
    assert one.landed


def test_a_queue_named_for_another_playlist_does_not_lift_this_ones_base():
    """Only the base of the playlist whose job queued the track is read as it
    stood at the queue."""
    decided = edits.decide(_read(agreed=frozenset({"t9"})), OWNED, FILED, {"t9": frozenset({"Jazz High"})})
    assert decided.decisions == ()


# ═══════════════════════════════════════════════════════════════════════════
# Once: the exclusion U227 meant still holds
# ═══════════════════════════════════════════════════════════════════════════


def test_once_the_library_holds_it_where_the_account_put_it_nothing_is_read():
    """After the carry rekordbox holds the track in Jazz Med, which the landing
    did not file, so the snapshot is the library's word and nothing is read."""
    decided = edits.decide(_read(agreed=frozenset({"t9"}), rekordbox_in=(JZM,)), OWNED, FILED, QUEUED)
    assert decided.decisions == ()


def test_a_move_in_rekordbox_after_the_carry_is_rekordboxs():
    decided = edits.decide(
        _read(agreed=frozenset({"t9"}), rekordbox_in=(AHM,), at=MOVED_AT), OWNED, FILED, QUEUED
    )
    assert decided.decisions == ()


def test_a_second_band_added_in_rekordbox_is_not_the_landings():
    decided = edits.decide(_read(agreed=frozenset({"t9"}), rekordbox_in=(AHH, AHM)), OWNED, FILED, QUEUED)
    assert decided.decisions == ()


def test_a_later_account_move_then_a_rekordbox_move_back_into_the_landings_band_stands():
    """U227's K1 with the queue named: the account no longer lists the track on
    the playlist whose job queued it, so that playlist's snapshot counts and
    the person's rekordbox move stands."""
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
    one = _only(edits.decide(playlists, OWNED, FILED, QUEUED))
    assert one.outcome == edits.REKORDBOX
    assert not one.landed and "rekordbox's place stands" in one.why


def test_a_landing_filed_where_the_account_asked_is_no_edit():
    """The library already holds it where the account put it, so the base is the
    library's word and nothing is read, run after run."""
    decided = edits.decide(
        _read(agreed=None, rekordbox_in=(JZM,)), OWNED, {"t9": frozenset({("Jazz", "Med")})}, QUEUED
    )
    assert decided.decisions == ()


def test_a_short_listing_of_the_queuing_playlist_lifts_nothing():
    """The review of U230, round one: a listing that could not be read is read
    as its snapshot and short, and carries no edit of its own."""
    for agreed in (None, frozenset({"t9"})):
        playlists = _read(agreed=agreed)
        playlists[0] = edits.Mirrored(
            place=JZM,
            account=frozenset({"t9"}),
            agreed=agreed,
            short=True,
            account_added={"t9": ACCOUNT_AT},
        )
        assert edits.decide(playlists, OWNED, FILED, QUEUED).decisions == (), agreed


def test_a_band_a_person_chose_before_any_carry_is_not_lifted_over():
    """The landing's filing must still stand for the lift: a never agreed
    playlist whose row a person moved, or gave a second band, in rekordbox
    before the edit was carried reads as before, no edit at all."""
    for rekordbox_in, at in (((AHM,), MOVED_AT), ((AHH, AHM), LANDED_AT)):
        decided = edits.decide(_read(agreed=None, rekordbox_in=rekordbox_in, at=at), OWNED, FILED, QUEUED)
        assert decided.decisions == (), rekordbox_in


def test_a_row_taken_out_of_the_tree_in_rekordbox_is_not_lifted_over():
    """A row rekordbox holds in no band has no landing's filing standing, so a
    person's removal is not beaten by the account's addition."""
    assert edits.decide(_read(agreed=None, rekordbox_in=()), OWNED, FILED, QUEUED).decisions == ()
