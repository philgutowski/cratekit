"""U118: Soul and Hip-Hop are folders of their own, and their tracks move in.

Soul was filed in R&B's energy bands as one folder, and those bands stay
R&B's, so Soul declares them as SPLIT PLACES: a track whose genre names Soul
leaves the R&B band for the Soul band its reading names, and a track whose
genre names R&B is never touched. Hip-Hop was a style sub of the non
electronic folder and is promoted the way R&B was, through a former place.

Held here: where the words route and tag, what the shipped template declares,
what competes, what the placement reader finds, what adoption withholds, what
the move plans and lists, what the worker checks, and then the verb through
the real dispatcher against a disposable library with real tags.

Every expected identifier is derived from the shipped taxonomy's declarations,
except the genre words, which are the author's decision and are named.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import shutil
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import apply_cli, artifacts, collection, move_cli
from cratekit.adopt import move as adopt_move
from cratekit.adopt import placements as adopt_placements
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.core import rb_writer, routing, taxonomy, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild
from cratekit.write.routing_pass import destination
from tests import adopt_fixtures
from tests.test_adopt_move import (  # noqa: F401
    GATE,
    VERB,
    _approve_and_run,
    _live,
    _removed,
    _rows,
    _shown,
)
from tests.test_adopt_workers import (  # noqa: F401
    _platform_seams,
    _reader_cache,
    _release_process_locks,
    library,
    machine,
    silence,
)

DECLARED = taxonomy.default_taxonomy()
TREE_ID = DECLARED.tree.id

#: The bucket split out of another, found by what makes it one.
(SOUL,) = [bucket for bucket in DECLARED.buckets if bucket.split_from]
RNB = DECLARED.bucket(SOUL.split_from[0].bucket)
SPLIT = {place.sub: place for place in SOUL.split_from}
#: R&B's own former place, the old "Soul / R&B" playlist, which Soul splits too.
(RNB_FORMER,) = RNB.formerly
OLD_SOUL_RNB = (DECLARED.bucket(RNB_FORMER.bucket).display, RNB_FORMER.display)
#: The promoted bucket whose former place is NonElectronic's Hip-Hop playlist.
HIPHOP = next(bucket for bucket in DECLARED.buckets if bucket.formerly and bucket.id != RNB.id)
(HH_FORMER,) = HIPHOP.formerly
NONELEC = DECLARED.bucket(HH_FORMER.bucket)
OLD_HIPHOP = (NONELEC.display, HH_FORMER.display)

VOX = next(entry for entry in DECLARED.sub_classes if entry.id == "with_vox")


def _band(level: int) -> str:
    return next(band.id for band in DECLARED.energy.bands if level <= band.max)


LOW, MED, HIGH = _band(1), _band(5), _band(9)
SINK = DECLARED.energy.no_energy_sub.id


def _scanned(
    content_id: str,
    *,
    energy: int | None,
    genre: str,
    disposition: adopt_scan.Disposition = adopt_scan.Disposition.ROUTE,
) -> adopt_scan.ScannedTrack:
    verdict, bucket, _match = adopt_scan.classify_genre(DECLARED, genre)
    routed = disposition is adopt_scan.Disposition.ROUTE
    return adopt_scan.ScannedTrack(
        content_id=content_id,
        recorded=f"/library/Music/{content_id}.flac",
        path=f"/library/Music/{content_id}.flac" if routed else None,
        readability=(
            adopt_scan.Readability.READABLE if routed else adopt_scan.Readability.MISSING
        ),
        disposition=verdict if routed else disposition,
        genre=genre,
        bucket=bucket if routed else "",
        energy=energy,
    )


def _in_rnb(content_id: str, *bands: str, soul: tuple[str, ...] = ()) -> dict:
    """What the placement reader answers for a track in R&B's bands.

    Under R&B as its own bands, and under Soul as the split places they are,
    whatever the track's genre. ``soul`` is the Soul bands it holds as well.
    """
    return {
        RNB.id: {content_id: tuple(bands)},
        SOUL.id: {content_id: (*(SPLIT[band].id for band in bands), *soul)},
    }


def _adoption(tracks, held: dict, *, unnamed: dict | None = None) -> adopt_plan.AdoptionPlan:
    placements = adopt_plan.Placements(read=True, held=held, unnamed=unnamed or {})
    return adopt_plan.build_adoption_plan(tracks, DECLARED, tree=TREE_ID, placements=placements)


def _moves(tracks, held: dict, *, unnamed: dict | None = None) -> adopt_move.MovePlan:
    return adopt_move.build_move_plan(_adoption(tracks, held, unnamed=unnamed), DECLARED)


# ── where the words go, as the author decided ──────────────────────────────


@pytest.mark.parametrize(
    ("word", "folder"),
    [
        ("Soul", "Soul"),
        ("Soul / R&B", "Soul"),
        ("R&B", "R&B"),
        ("MPB", "R&B"),
        ("Hip-Hop", "Hip-Hop"),
        ("Hip-Hop / R&B", "Hip-Hop"),
        ("Hip-hop & Rap", "Hip-Hop"),
    ],
)
def test_each_word_routes_to_the_folder_the_author_gave_it(word, folder):
    resolution = routing.resolve_bucket(DECLARED, word)
    assert DECLARED.bucket(resolution.bucket_id).display == folder
    assert resolution.match is routing.Match.EXACT


@pytest.mark.parametrize(
    ("word", "folder"),
    [
        ("soul & funk", "Soul"),
        ("Soul / R&B", "Soul"),
        ("rnb", "R&B"),
        ("MPB", "R&B"),
        ("trap", "Hip-Hop"),
        ("rap", "Hip-Hop"),
        ("hip-hop / r&b", "Hip-Hop"),
        ("Trap / Wave", "Hip-Hop"),
    ],
)
def test_each_word_tags_as_the_folder_the_author_gave_it_and_the_tag_routes_there(word, folder):
    """A tag the tagger writes is a folder's name, and routing resolves it to
    that folder, so a tagged track lands where its word was meant to."""
    suggestion = routing.suggest_tag(DECLARED, word)
    assert (suggestion.tag, suggestion.sub_id) == (folder, None)
    assert DECLARED.bucket(suggestion.bucket_id).display == folder
    assert routing.resolve_bucket(DECLARED, suggestion.tag).bucket_id == suggestion.bucket_id


# ── the shipped declaration ────────────────────────────────────────────────


@pytest.mark.parametrize("bucket", [SOUL, HIPHOP], ids=["soul", "hip-hop"])
def test_both_new_folders_are_shaped_as_r_and_b_is(bucket):
    """Bands, the no reading sub and the vocal sub; no star rating; R&B's
    family and tempo window; no subs of their own, so no Candy."""
    assert bucket.sub_by_source is None and bucket.single_sub is None and bucket.subs == ()
    assert bucket.energy.enabled and not bucket.energy.band_display
    assert (bucket.family, bucket.bpm, bucket.rates) == (RNB.family, RNB.bpm, RNB.rates)
    assert routing.rates(DECLARED, bucket.id) is False
    kind, subs = routing.competing_subs(DECLARED, bucket.id)
    assert kind is routing.Competing.BAND
    assert {band.id for band in DECLARED.energy.bands} | {SINK} <= subs
    assert VOX.id not in subs
    assert destination(DECLARED, bucket.id, VOX.id) == (bucket.display, VOX.display)
    assert routing.energy_sub(DECLARED, bucket.id, None).id == SINK


def test_the_new_folders_sit_beside_r_and_b_at_the_top_of_the_tree():
    order = [bucket.id for bucket in DECLARED.buckets]
    assert order.index(RNB.id) + 1 == order.index(SOUL.id)
    assert order.index(SOUL.id) + 1 == order.index(HIPHOP.id)


def test_hip_hop_left_the_non_electronic_folder_and_declares_the_playlist_it_left():
    assert NONELEC.sub_by_source is not None
    assert HH_FORMER.sub not in {sub.id for sub in NONELEC.subs}
    assert HH_FORMER.sub not in set(NONELEC.sub_by_source.map.values())
    assert not set(HIPHOP.aliases) & set(NONELEC.aliases)
    assert OLD_HIPHOP == ("NonElectronic", "Hip-Hop")
    # Funk stays a style of the non electronic folder.
    assert routing.energy_sub(DECLARED, NONELEC.id, None, source_genre="Funk").display == "Funk"


def test_soul_is_split_out_of_every_r_and_b_band_and_r_and_bs_old_playlist():
    bands = {band.id for band in DECLARED.energy.bands} | {SINK}
    assert set(SPLIT) == bands | {RNB_FORMER.id}
    assert SOUL.formerly == ()
    for sub in bands:
        assert destination(DECLARED, RNB.id, sub) == (RNB.display, SPLIT[sub].display)
    assert (SPLIT[RNB_FORMER.id].display, OLD_SOUL_RNB) == (
        RNB_FORMER.display, ("NonElectronic", "Soul / R&B")
    )


def test_a_split_place_competes_in_soul_and_nowhere_else():
    split_ids = {place.id for place in SPLIT.values()}
    _kind, soul = routing.competing_subs(DECLARED, SOUL.id)
    assert split_ids <= soul
    for bucket in DECLARED.buckets:
        if bucket.id != SOUL.id:
            assert not split_ids & routing.competing_subs(DECLARED, bucket.id)[1], bucket.id
    # R&B competes on its bands and on its own former place, as before U118.
    _kind, rnb = routing.competing_subs(DECLARED, RNB.id)
    assert rnb == set(SPLIT) | {place.id for place in RNB.formerly}
    for place in SPLIT.values():
        assert routing.split_place(DECLARED, SOUL.id, place.id) is place
        assert routing.split_place(DECLARED, RNB.id, place.id) is None
        assert routing.split_place(DECLARED, RNB.id, place.sub) is None
        assert routing.former_place(DECLARED, SOUL.id, place.id) is None


def test_no_resolver_answers_with_a_split_place_and_no_writer_can_be_handed_one():
    split_ids = {place.id for place in SPLIT.values()}
    for level in (None, *range(1, 11)):
        assert routing.energy_sub(DECLARED, SOUL.id, level).id not in split_ids
    for place in SPLIT.values():
        with pytest.raises(KeyError):
            destination(DECLARED, SOUL.id, place.id)


def test_a_split_place_is_found_as_the_r_and_b_place_it_is():
    for sub, place in SPLIT.items():
        assert adopt_placements.named_place(DECLARED, SOUL.id, place.id) == (
            adopt_placements.named_place(DECLARED, RNB.id, sub)
        )
        assert adopt_placements.recorded_under(DECLARED, SOUL.id, place.id) == (
            adopt_placements.recorded_under(DECLARED, RNB.id, sub)
        )
    assert adopt_placements.named_place(DECLARED, SOUL.id, SPLIT[MED].id) == (RNB.display, "Med")
    assert adopt_placements.named_place(
        DECLARED, SOUL.id, SPLIT[RNB_FORMER.id].id
    ) == OLD_SOUL_RNB
    assert adopt_placements.recorded_under(DECLARED, SOUL.id, SPLIT[RNB_FORMER.id].id) == (
        RNB_FORMER.bucket, RNB_FORMER.sub
    )
    assert adopt_placements.named_place(DECLARED, SOUL.id, MED) == (SOUL.display, "Med")


# ── the placement reader ───────────────────────────────────────────────────


def _node(folder: str, playlist: str, *content_ids: str) -> rebuild.TreeNode:
    return rebuild.TreeNode(
        folder_id=f"f-{folder}",
        folder_display=folder,
        playlist_id=f"p-{folder}-{playlist}",
        playlist_display=playlist,
        content_ids=frozenset(content_ids),
    )


def test_a_track_in_an_r_and_b_band_holds_it_in_r_and_b_and_the_split_place_in_soul():
    nodes = [_node(*destination(DECLARED, RNB.id, MED), "t")]
    found = adopt_placements.placements_from(DECLARED, nodes, None)
    assert found.held == _in_rnb("t", MED)


def test_a_track_in_the_old_hip_hop_playlist_holds_its_former_place_in_both_buckets():
    found = adopt_placements.placements_from(DECLARED, [_node(*OLD_HIPHOP, "t")], None)
    assert found.holds(HIPHOP.id, "t") == (HH_FORMER.id,)
    assert found.holds(NONELEC.id, "t") == (HH_FORMER.id,)


# ── adoption ───────────────────────────────────────────────────────────────


def test_adoption_withholds_a_soul_track_still_in_an_r_and_b_band():
    (entry,) = _adoption([_scanned("t", energy=5, genre="Soul")], _in_rnb("t", MED)).entries
    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.bucket, entry.sub, entry.holds) == (SOUL.id, MED, (SPLIT[MED].id,))
    assert entry.held_elsewhere and not entry.applicable


@pytest.mark.parametrize("genre", ["R&B", "MPB"])
def test_adoption_leaves_an_r_and_b_track_in_its_band_as_it_was(genre):
    (entry,) = _adoption([_scanned("t", energy=5, genre=genre)], _in_rnb("t", MED)).entries
    assert (entry.bucket, entry.sub) == (RNB.id, MED)
    assert entry.applicable and not entry.held_elsewhere


# ── the move plan ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("genre", "level", "band"),
    [("Soul / R&B", 5, MED), ("Soul", 9, HIGH), ("Soul", 2, LOW)],
    ids=["same-band", "another-band", "low"],
)
def test_a_soul_track_in_r_and_b_med_moves_to_the_soul_band_its_reading_names(genre, level, band):
    plan = _moves([_scanned("t", energy=level, genre=genre)], _in_rnb("t", MED))
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add, move.remove) == (
        SOUL.id, band, band, (SPLIT[MED].id,)
    )
    assert (move.kind, move.decided_by) == ("band", adopt_move.DECIDED_BY_ENERGY)
    assert plan.left == ()
    assert plan.counts()["memberships_added"] == plan.counts()["memberships_removed"] == 1


def test_a_soul_track_with_no_reading_leaves_r_and_b_for_soul_unsorted():
    """Its genre sent it out of R&B, so no reading is needed to leave, and the
    no reading sub says nothing false about it."""
    plan = _moves([_scanned("t", energy=None, genre="Soul")], _in_rnb("t", MED))
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add, move.remove, move.energy) == (
        SOUL.id, SINK, SINK, (SPLIT[MED].id,), None
    )
    assert move.decided_by == adopt_move.DECIDED_BY_GENRE
    assert plan.left == ()


def test_a_soul_track_already_in_its_soul_band_only_leaves_r_and_b():
    plan = _moves([_scanned("t", energy=5, genre="Soul")], _in_rnb("t", MED, soul=(MED,)))
    (move,) = plan.moves
    assert (move.target, move.add, move.remove) == (MED, "", (SPLIT[MED].id,))


def test_a_soul_track_in_two_r_and_b_bands_leaves_both_in_one_move_and_r_and_b_plans_none():
    """R&B's own tree path would move a track held in two of its bands to the
    one its reading names. That band is Soul's to settle here, or the two
    buckets would plan competing moves and the read back would report one of
    them unfinished."""
    plan = _moves([_scanned("t", energy=9, genre="Soul")], _in_rnb("t", MED, HIGH))
    (move,) = plan.moves
    assert (move.bucket, move.add, set(move.remove)) == (
        SOUL.id, HIGH, {SPLIT[MED].id, SPLIT[HIGH].id}
    )
    assert plan.left == ()


@pytest.mark.parametrize("genre", ["R&B", "MPB"])
def test_an_r_and_b_track_in_r_and_b_med_is_never_asked_about_in_soul(genre):
    plan = _moves([_scanned("t", energy=5, genre=genre)], _in_rnb("t", MED))
    assert plan.moves == () and plan.left == ()


def test_an_r_and_b_track_in_two_r_and_b_bands_is_still_r_and_bs_to_settle():
    """R-780's rule in R&B, unchanged: Soul does not list or move it."""
    plan = _moves([_scanned("t", energy=9, genre="R&B")], _in_rnb("t", MED, HIGH))
    (move,) = plan.moves
    assert (move.bucket, move.target, move.remove) == (RNB.id, HIGH, (MED,))
    assert plan.left == ()


@pytest.mark.parametrize("genre", ["", "Deep House"], ids=["no-genre", "another-folder"])
def test_a_track_in_two_r_and_b_bands_whose_genre_names_neither_is_not_listed_under_soul(genre):
    plan = _moves([_scanned("t", energy=9, genre=genre)], _in_rnb("t", MED, HIGH))
    assert SOUL.id not in {row.bucket for row in (*plan.moves, *plan.left)}


def test_a_soul_track_in_a_renamed_r_and_b_band_is_left_since_the_writer_cannot_see_it():
    held = _in_rnb("t", MED)
    plan = _moves([_scanned("t", energy=5, genre="Soul")], held, unnamed=held)
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.bucket, left.reason, left.holds_unnamed) == (
        SOUL.id, adopt_move.LEFT_UNNAMED, (SPLIT[MED].id,)
    )


def test_an_unreadable_soul_file_in_r_and_b_is_listed_under_soul_and_not_moved():
    """Found by the review: it was in no row, so the split could not be seen to
    be unfinished before its declaration was deleted."""
    excluded = _scanned(
        "t", energy=5, genre="Soul", disposition=adopt_scan.Disposition.EXCLUDED
    )
    plan = _moves([excluded], _in_rnb("t", MED))
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.bucket, left.reason, left.target, left.holds) == (
        SOUL.id, adopt_move.LEFT_NO_READING, "", (SPLIT[MED].id,)
    )


def test_an_unreadable_soul_file_in_a_renamed_r_and_b_band_is_listed_under_the_name():
    excluded = _scanned(
        "t", energy=5, genre="Soul", disposition=adopt_scan.Disposition.EXCLUDED
    )
    held = _in_rnb("t", MED)
    (left,) = _moves([excluded], held, unnamed=held).left
    assert (left.bucket, left.reason, left.holds_unnamed) == (
        SOUL.id, adopt_move.LEFT_UNNAMED, (SPLIT[MED].id,)
    )


def test_a_soul_track_whose_folder_a_verdict_refused_is_listed_and_r_and_b_moves_nothing():
    """Found by the review: R&B's own tree path moved it between R&B's bands,
    a folder its genre does not name, because no entry claimed Soul."""
    current = _adoption([_scanned("t", energy=9, genre="Soul")], {})
    refused = replace(
        current,
        entries=tuple(
            replace(
                entry,
                disposition=adopt_scan.Disposition.WITHHELD,
                withheld_by=adopt_plan.WITHHELD_BY_VERDICT,
            )
            for entry in current.entries
        ),
        placements=adopt_plan.Placements(read=True, held=_in_rnb("t", LOW, HIGH)),
    )
    plan = adopt_move.build_move_plan(refused, DECLARED)
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.bucket, left.reason, set(left.holds)) == (
        SOUL.id, adopt_move.LEFT_VERDICT, {SPLIT[LOW].id, SPLIT[HIGH].id}
    )


def _in_old_soul_rnb(content_id: str) -> dict:
    """A track in the old "Soul / R&B" playlist, as the reader reports it."""
    return {
        RNB.id: {content_id: (RNB_FORMER.id,)},
        RNB_FORMER.bucket: {content_id: (RNB_FORMER.id,)},
        SOUL.id: {content_id: (SPLIT[RNB_FORMER.id].id,)},
    }


def test_a_soul_track_in_the_old_soul_r_and_b_playlist_moves_to_soul_and_is_withheld_until():
    """Found by the review: it was filed in Soul by adoption while it sat in
    the old playlist, and nothing took it out."""
    tracks = [_scanned("t", energy=5, genre="Soul / R&B")]
    (entry,) = _adoption(tracks, _in_old_soul_rnb("t")).entries
    assert entry.held_elsewhere and not entry.applicable
    plan = _moves(tracks, _in_old_soul_rnb("t"))
    (move,) = plan.moves
    assert (move.bucket, move.add, move.remove) == (SOUL.id, MED, (SPLIT[RNB_FORMER.id].id,))
    assert plan.left == ()
    (written,) = move_cli.membership_moves([move], DECLARED)
    assert written.remove == (OLD_SOUL_RNB,)


def test_an_r_and_b_track_in_the_old_soul_r_and_b_playlist_still_moves_to_r_and_b():
    plan = _moves([_scanned("t", energy=5, genre="R&B")], _in_old_soul_rnb("t"))
    (move,) = plan.moves
    assert (move.bucket, move.add, move.remove) == (RNB.id, MED, (RNB_FORMER.id,))
    assert plan.left == ()


def test_an_entry_naming_a_split_place_as_its_sub_is_never_a_move():
    current = _adoption([_scanned("t", energy=5, genre="Soul")], _in_rnb("t", MED))
    forged = replace(
        current, entries=tuple(replace(e, sub=SPLIT[MED].id) for e in current.entries)
    )
    assert adopt_move.build_move_plan(forged, DECLARED).moves == ()


@pytest.mark.parametrize("genre", ["Hip-Hop", "Hip-Hop / R&B", "Hip-hop & Rap"])
def test_a_hip_hop_track_in_the_old_playlist_moves_into_its_band_and_leaves_it(genre):
    held = {HIPHOP.id: {"t": (HH_FORMER.id,)}, NONELEC.id: {"t": (HH_FORMER.id,)}}
    plan = _moves([_scanned("t", energy=5, genre=genre)], held)
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add, move.remove) == (
        HIPHOP.id, MED, MED, (HH_FORMER.id,)
    )
    assert plan.left == ()


# ── the writer's list and the worker's check ───────────────────────────────


def _approved() -> adopt_move.Move:
    (move,) = _moves([_scanned("t", energy=5, genre="Soul")], _in_rnb("t", MED)).moves
    return move


def test_the_writer_is_told_to_add_the_soul_band_and_leave_the_r_and_b_band_by_name():
    (written,) = move_cli.membership_moves([_approved()], DECLARED)
    assert written.target == (SOUL.display, "Med")
    assert written.remove == (destination(DECLARED, RNB.id, MED),)


def test_the_worker_finds_a_finished_soul_move_done():
    current = _adoption([_scanned("t", energy=5, genre="Soul")], {SOUL.id: {"t": (MED,)}})
    assert move_cli.remaining([_approved()], current, DECLARED) == ((), ())


def test_the_worker_narrows_a_soul_move_whose_band_landed_to_the_removal_alone():
    current = _adoption(
        [_scanned("t", energy=5, genre="Soul")], _in_rnb("t", MED, soul=(MED,))
    )
    todo, gone = move_cli.remaining([_approved()], current, DECLARED)
    assert ([(move.add, move.remove) for move in todo], gone) == ([("", (SPLIT[MED].id,))], ())


@pytest.mark.parametrize("genre", ["R&B", "", "Deep House"])
def test_a_track_retagged_out_of_soul_since_the_approval_is_a_stale_decision(genre):
    current = _adoption([_scanned("t", energy=5, genre=genre)], _in_rnb("t", MED))
    with pytest.raises(Exception) as raised:
        move_cli.remaining([_approved()], current, DECLARED)
    assert raised.value.cause.reason == "decision-stale"


# ---------------------------------------------------------------------------
# The verb, against a disposable library filed under the shape before U118
# ---------------------------------------------------------------------------

#: Content identifier, genre, energy tag, and the places seeded: ``old`` is the
#: Hip-Hop playlist of the non electronic folder, ``vox`` R&B's vocal sub, and
#: anything else an R&B band.
_SEEDED = (
    ("s-med", "Soul", "5", (MED, "vox")),
    ("s-combined", "Soul / R&B", "9", (MED,)),
    ("s-no-reading", "Soul", None, (MED,)),
    ("r-stays", "R&B", "5", (MED, "vox")),
    ("m-stays", "MPB", "2", (LOW,)),
    ("h-plain", "Hip-Hop", "8", ("old",)),
    ("h-combined", "Hip-Hop / R&B", "2", ("old",)),
    ("h-named", "Hip-hop & Rap", None, ("old",)),
    ("s-old", "Soul", "5", ("soul-rnb",)),
    ("r-old", "R&B", "2", ("soul-rnb",)),
)
#: Where each moved track ends among the competing places: Soul's or
#: Hip-Hop's band, or the no reading sub.
_ENDS = {
    "s-med": (SOUL, MED),
    "s-combined": (SOUL, HIGH),
    "s-no-reading": (SOUL, SINK),
    "h-plain": (HIPHOP, HIGH),
    "h-combined": (HIPHOP, LOW),
    "h-named": (HIPHOP, SINK),
    "s-old": (SOUL, MED),
    "r-old": (RNB, LOW),
}
_STAYING = {"r-stays", "m-stays"}
RNB_VOX = (RNB.display, VOX.display)


def _seeded_place(place: str) -> tuple[str, str]:
    if place == "old":
        return OLD_HIPHOP
    if place == "vox":
        return RNB_VOX
    if place == "soul-rnb":
        return OLD_SOUL_RNB
    return destination(DECLARED, RNB.id, place)


@pytest.fixture
def split(machine, silence):  # noqa: F811
    """A library whose Soul tracks sit in R&B's bands and whose Hip-Hop tracks
    sit in the non electronic folder's Hip-Hop playlist, as on 2026-10-08."""
    from cratekit.core import tags

    adopt_fixtures.build(
        machine,
        tuple(
            adopt_fixtures.Track(content_id, f"{content_id}.flac", genre)
            for content_id, genre, _tag, _held in _SEEDED
        ),
    )
    collection.reset_cache()

    music = Path(machine.library.root) / "Music"
    for content_id, _genre, tag, _held in _SEEDED:
        path = music / f"{content_id}.flac"
        shutil.copyfile(silence, path)
        if tag is not None:
            assert tags.write_tags(path, {"energylevel": tag}) is True

    handle = rb_writer.open_db(rb_writer.live_db_path(machine), unlock=False, cfg=machine)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        for content_id, _genre, _tag, held in _SEEDED:
            for place in held:
                folder_display, sub_display = _seeded_place(place)
                folder = rb_writer.ensure_folder(handle, folder_display, parent=root)
                playlist = rb_writer.ensure_playlist(handle, sub_display, folder)
                rb_writer.add_memberships(handle, playlist, [content_id])
        handle.session.commit()
        root_id = str(root.ID)
    finally:
        rb_writer.close_db(handle)
    tree_registry.record_cutover(
        machine,
        TREE_ID,
        root_id=root_id,
        on=date(2026, 10, 1),
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    return machine


def test_the_gate_shows_every_soul_and_hip_hop_track_moving_and_no_r_and_b_track(split):
    shown = _shown(VERB)
    rows = {row["content_id"]: row for row in shown["items"]}
    assert set(rows) == set(_ENDS) and len(shown["items"]) == len(_ENDS)
    for content_id, (bucket, sub) in _ENDS.items():
        row = rows[content_id]
        assert (row["bucket"], row["target"], row["add"]) == (bucket.id, sub, sub), content_id
    for content_id in ("s-med", "s-combined", "s-no-reading"):
        assert rows[content_id]["remove"] == [SPLIT[MED].id], content_id
    for content_id in ("h-plain", "h-combined", "h-named"):
        assert rows[content_id]["remove"] == [HH_FORMER.id], content_id
    assert rows["s-old"]["remove"] == [SPLIT[RNB_FORMER.id].id]
    assert rows["r-old"]["remove"] == [RNB_FORMER.id]
    assert shown["left"] == []


def test_an_approved_move_files_soul_and_hip_hop_in_their_folders_and_keeps_r_and_b(split):
    before = _live(split)
    job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    after, removed = _live(split), _removed(split)

    for content_id, (bucket, sub) in _ENDS.items():
        seeded = next(held for cid, _g, _t, held in _SEEDED if cid == content_id)
        left = {_seeded_place(place) for place in seeded if place != "vox"}
        kept = {_seeded_place(place) for place in seeded if place == "vox"}
        assert after[content_id] == {destination(DECLARED, bucket.id, sub), *kept}, content_id
        assert removed[content_id] == left, content_id
    # THE VOCAL SUB IS KEPT: a Soul track leaves R&B / Med and stays in R&B's
    # "with vox", which is a sub class and never a place a move removes.
    assert RNB_VOX in after["s-med"]
    # R&B and MPB tracks are where they were, and nothing of theirs removed.
    for content_id in _STAYING:
        assert after[content_id] == before[content_id], content_id
        assert content_id not in removed, content_id
    # R&B KEEPS ONLY R&B AND MPB, and the old Hip-Hop playlist is empty.
    in_rnb_bands = {
        content_id
        for content_id, places in after.items()
        for sub in SPLIT
        if sub != RNB_FORMER.id and destination(DECLARED, RNB.id, sub) in places
    }
    assert in_rnb_bands == _STAYING | {"r-old"}
    assert not any(OLD_HIPHOP in places for places in after.values())
    assert not any(OLD_SOUL_RNB in places for places in after.values())

    report = artifacts.committed(split, job_id)[-1]
    assert (report["added"], report["removed"]) == (len(_ENDS), len(_ENDS))
    assert sorted(report["moved"]) == sorted(_ENDS)
    assert report["in_both"] == report["untouched"] == report["neither"] == []


def test_adoption_after_the_move_files_none_of_them_a_second_time(split):
    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    collection.reset_cache()
    rows = _rows(split)

    shown = _shown(VERB)
    assert shown["items"] == [] and shown["left"] == []
    plan = apply_cli.current_plan(split, DECLARED)
    entries = {entry.content_id: entry for entry in plan.entries}
    for content_id, (bucket, sub) in _ENDS.items():
        entry = entries[content_id]
        assert (entry.bucket, entry.sub) == (bucket.id, sub), content_id
        assert not entry.held_elsewhere, content_id
    assert _rows(split) == rows
