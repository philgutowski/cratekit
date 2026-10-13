"""U133: Jazz is a genre folder of its own, and its tracks move in.

Jazz was a style sub of the non electronic folder with no energy split, and
is promoted the way Hip-Hop was (U118), through a former place: a folder under
the tree with the dance bands, Unsorted, "with vox" and Favorites, declaring
the old NonElectronic / Jazz playlist as the place its tracks leave. Unlike
R&B and Hip-Hop, its keyword rule moved with it, by the author's naming.

Held here: where the words route and tag, what the shipped template declares,
what competes, what adoption withholds, what the move plans, and then the
verb through the real dispatcher against a disposable library with real tags.

Every expected identifier is derived from the shipped taxonomy's declarations,
except the genre words and the folder names, which are the author's decision
and are named.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import apply_cli, artifacts, collection
from cratekit.adopt import move as adopt_move
from cratekit.adopt import placements as adopt_placements
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.core import rb_writer, routing, taxonomy, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild
from cratekit.write.routing_pass import destination
from tests import adopt_fixtures
from tests import legacy_taxonomy as legacy
from tests.test_adopt_move import (  # noqa: F401
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

(JAZZ,) = [bucket for bucket in DECLARED.buckets if bucket.display == "Jazz"]
(HIPHOP,) = [bucket for bucket in DECLARED.buckets if bucket.display == "Hip-Hop"]
(FORMER,) = JAZZ.formerly
NONELEC = DECLARED.bucket(FORMER.bucket)
OLD_JAZZ = (NONELEC.display, FORMER.display)

VOX = next(entry for entry in DECLARED.sub_classes if entry.id == "with_vox")


def _band(level: int) -> str:
    return next(band.id for band in DECLARED.energy.bands if level <= band.max)


LOW, MED, HIGH = _band(1), _band(5), _band(9)
SINK = DECLARED.energy.no_energy_sub.id


def _scanned(content_id: str, *, energy: int | None, genre: str) -> adopt_scan.ScannedTrack:
    verdict, bucket, _match = adopt_scan.classify_genre(DECLARED, genre)
    return adopt_scan.ScannedTrack(
        content_id=content_id,
        recorded=f"/library/Music/{content_id}.flac",
        path=f"/library/Music/{content_id}.flac",
        readability=adopt_scan.Readability.READABLE,
        disposition=verdict,
        genre=genre,
        bucket=bucket,
        energy=energy,
    )


def _in_old(content_id: str) -> dict:
    """What the placement reader answers for a track in the old Jazz playlist."""
    return {JAZZ.id: {content_id: (FORMER.id,)}, NONELEC.id: {content_id: (FORMER.id,)}}


def _adoption(tracks, held: dict) -> adopt_plan.AdoptionPlan:
    placements = adopt_plan.Placements(read=True, held=held, unnamed={})
    return adopt_plan.build_adoption_plan(tracks, DECLARED, tree=TREE_ID, placements=placements)


def _moves(tracks, held: dict) -> adopt_move.MovePlan:
    return adopt_move.build_move_plan(_adoption(tracks, held), DECLARED)


# ── where the words go, as the author decided ──────────────────────────────


def test_a_track_tagged_jazz_routes_to_the_jazz_folder_by_its_alias():
    resolution = routing.resolve_bucket(DECLARED, "Jazz")
    assert resolution.bucket_id == JAZZ.id
    assert resolution.match is routing.Match.EXACT


@pytest.mark.parametrize("word", ["Jazz", "jazz", "JAZZ"])
def test_each_jazz_word_tags_as_the_folder_and_the_tag_routes_there(word):
    suggestion = routing.suggest_tag(DECLARED, word)
    assert (suggestion.tag, suggestion.bucket_id, suggestion.sub_id) == ("Jazz", JAZZ.id, None)
    assert routing.resolve_bucket(DECLARED, suggestion.tag).bucket_id == JAZZ.id


@pytest.mark.parametrize("genre", ["Acid Jazz", "jazz", "Jazz Funk"])
def test_a_partial_jazz_match_routes_to_jazz_by_the_keyword_rule_the_author_moved(genre):
    """The old code filed these in NonElectronic's default sub by the same
    keyword. R-804 and R-941 kept R&B's and Hip-Hop's rules where they were;
    the author named Jazz's with the bucket."""
    resolution = routing.resolve_bucket(DECLARED, genre)
    assert (resolution.bucket_id, resolution.match) == (JAZZ.id, routing.Match.FUZZY)
    assert resolution.matched_on == "jazz"
    assert legacy.resolve_genre(genre)[0] == NONELEC.display


@pytest.mark.parametrize("genre", ["Blues", "blues", "Rhythm & Blues"])
def test_blues_still_routes_as_the_old_code_routed_it(genre):
    """No rule of the routing table names blues, before U133 or after it."""
    assert routing.resolve_bucket(DECLARED, genre).bucket_id != JAZZ.id
    assert DECLARED.bucket(routing.resolve_bucket(DECLARED, genre).bucket_id).display == (
        legacy.resolve_genre(genre)[0]
    )


def test_the_catalogues_blues_kind_rule_still_runs_after_r_and_b():
    """A label kind, not a folder: "blues" says jazz, and the long spelling of
    R&B, which contains it, is still claimed by the R&B rule first."""
    assert routing.published_kind(DECLARED, "Blues") == "jazz"
    assert routing.published_kind(DECLARED, "Jazz") == "jazz"
    assert routing.published_kind(DECLARED, "Rhythm & Blues") == "rnb"
    kinds = [rule.kind for rule in DECLARED.label_gate.published]
    assert kinds.index("rnb") < kinds.index("jazz")


# ── the shipped declaration ────────────────────────────────────────────────


def test_jazz_is_shaped_as_hip_hop_is():
    """Bands, the no reading sub and the vocal sub; no star rating; the non
    electronic tempo window and family; no subs of its own, so no Candy."""
    assert JAZZ.sub_by_source is None and JAZZ.single_sub is None and JAZZ.subs == ()
    assert JAZZ.energy.enabled and not JAZZ.energy.band_display
    assert (JAZZ.family, JAZZ.bpm, JAZZ.rates) == (HIPHOP.family, HIPHOP.bpm, HIPHOP.rates)
    assert (JAZZ.family, JAZZ.bpm) == (NONELEC.family, NONELEC.bpm)
    assert routing.rates(DECLARED, JAZZ.id) is False
    kind, subs = routing.competing_subs(DECLARED, JAZZ.id)
    assert kind is routing.Competing.BAND
    assert {band.id for band in DECLARED.energy.bands} | {SINK, FORMER.id} == subs
    assert VOX.id not in subs
    assert destination(DECLARED, JAZZ.id, VOX.id) == ("Jazz", VOX.display)
    for level, band in ((2, LOW), (5, MED), (9, HIGH)):
        assert routing.energy_sub(DECLARED, JAZZ.id, level).id == band
    assert routing.energy_sub(DECLARED, JAZZ.id, None).id == SINK
    assert JAZZ.split_from == ()


def test_jazz_sits_after_hip_hop_and_before_the_folder_it_left():
    order = [bucket.id for bucket in DECLARED.buckets]
    assert order.index(HIPHOP.id) + 1 == order.index(JAZZ.id)
    assert order.index(JAZZ.id) + 1 == order.index(NONELEC.id)


def test_jazz_left_the_non_electronic_folder_and_declares_the_playlist_it_left():
    assert OLD_JAZZ == ("NonElectronic", "Jazz")
    assert NONELEC.sub_by_source is not None
    assert FORMER.sub not in {sub.id for sub in NONELEC.subs}
    assert FORMER.sub not in set(NONELEC.sub_by_source.map.values())
    assert "Jazz" not in NONELEC.sub_by_source.map
    assert not {a.casefold() for a in (*JAZZ.aliases, *JAZZ.tag_aliases)} & {
        a.casefold() for a in (*NONELEC.aliases, *NONELEC.tag_aliases)
    }
    for sub in NONELEC.subs:
        assert "jazz" not in {word.casefold() for word in sub.tag_aliases}, sub.id
    # Classical stays a style of the non electronic folder.
    assert routing.energy_sub(DECLARED, NONELEC.id, None, source_genre="Classical").display == (
        "Classical"
    )


def test_the_old_jazz_playlist_competes_in_both_buckets_and_is_never_a_destination():
    assert routing.former_place(DECLARED, JAZZ.id, FORMER.id) is FORMER
    assert FORMER.id in routing.competing_subs(DECLARED, NONELEC.id)[1]
    for level in (None, *range(1, 11)):
        assert routing.energy_sub(DECLARED, JAZZ.id, level).id != FORMER.id
    with pytest.raises(KeyError):
        destination(DECLARED, JAZZ.id, FORMER.id)


# ── the placement reader ───────────────────────────────────────────────────


def _node(folder: str, playlist: str, *content_ids: str) -> rebuild.TreeNode:
    return rebuild.TreeNode(
        folder_id=f"f-{folder}",
        folder_display=folder,
        playlist_id=f"p-{folder}-{playlist}",
        playlist_display=playlist,
        content_ids=frozenset(content_ids),
    )


def test_a_track_in_the_old_jazz_playlist_holds_its_former_place_in_both_buckets():
    found = adopt_placements.placements_from(DECLARED, [_node(*OLD_JAZZ, "t")], None)
    assert found.holds(JAZZ.id, "t") == (FORMER.id,)
    assert found.holds(NONELEC.id, "t") == (FORMER.id,)


#: The identifier the old Jazz playlist had as a sub of NonElectronic, before
#: U133, from the template's history. A write before U133 recorded the
#: playlist's node under it, so a renamed old playlist is found by it.
OLD_SUB_ID = "jazz"


def test_the_old_playlist_is_found_under_the_identifier_it_was_recorded_by():
    assert FORMER.sub == OLD_SUB_ID
    assert adopt_placements.recorded_under(DECLARED, JAZZ.id, FORMER.id) == (NONELEC.id, OLD_SUB_ID)
    assert adopt_placements.recorded_under(DECLARED, NONELEC.id, FORMER.id) == (
        NONELEC.id, OLD_SUB_ID
    )
    assert adopt_placements.named_place(DECLARED, JAZZ.id, FORMER.id) == OLD_JAZZ


# ── adoption and the move ──────────────────────────────────────────────────


def test_adoption_withholds_a_jazz_track_still_in_the_old_playlist():
    (entry,) = _adoption([_scanned("t", energy=5, genre="Jazz")], _in_old("t")).entries
    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.bucket, entry.sub, entry.holds) == (JAZZ.id, MED, (FORMER.id,))
    assert entry.held_elsewhere and not entry.applicable


@pytest.mark.parametrize(("level", "band"), [(2, LOW), (5, MED), (9, HIGH), (None, SINK)])
def test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it(level, band):
    plan = _moves([_scanned("t", energy=level, genre="Jazz")], _in_old("t"))
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add, move.remove) == (
        JAZZ.id, band, band, (FORMER.id,)
    )
    assert plan.left == ()


def test_a_partial_jazz_match_already_in_rock_is_filed_in_jazz_and_stays_in_rock():
    """THE COST OF THE MOVED KEYWORD RULE, pinned so a fix shows up here.

    The old code filed "Acid Jazz" in NonElectronic's default sub, Rock. It
    routes to Jazz now, and Rock is not a place Jazz competes on, so adoption
    files it into a Jazz band and the move plans nothing: it sits in both
    folders, which no verb settles. R-804 named this cost for R&B and chose
    not to pay it; the author named the rule for Jazz, and the residual U133
    filed carries it.
    """
    rock = NONELEC.sub_by_source.default
    held = {NONELEC.id: {"t": (rock,)}}
    tracks = [_scanned("t", energy=5, genre="Acid Jazz")]
    (entry,) = _adoption(tracks, held).entries
    assert (entry.bucket, entry.sub) == (JAZZ.id, MED)
    assert entry.applicable and not entry.held_elsewhere
    plan = _moves(tracks, held)
    assert plan.moves == () and plan.left == ()


def test_a_classical_track_in_its_style_playlist_is_never_asked_about():
    held = {NONELEC.id: {"t": ("classical",)}}
    plan = _moves([_scanned("t", energy=5, genre="Classical")], held)
    assert plan.moves == () and plan.left == ()


# ---------------------------------------------------------------------------
# The verb, against a disposable library filed under the shape before U133
# ---------------------------------------------------------------------------

#: Content identifier, genre, energy tag, and the places seeded: ``old`` is the
#: Jazz playlist of the non electronic folder, ``vox`` that folder's vocal sub,
#: ``set`` a playlist outside the tree, and anything else a NonElectronic style.
_SEEDED = (
    ("j-med", "Jazz", "5", ("old", "vox")),
    ("j-high", "Jazz", "9", ("old", "set")),
    ("j-low", "Jazz", "2", ("old",)),
    ("j-no-reading", "Jazz", None, ("old",)),
    ("c-stays", "Classical", "5", ("Classical",)),
    ("r-stays", "Rock", "8", ("Rock", "vox")),
)
#: Where each moved track ends among Jazz's competing places.
_ENDS = {"j-med": MED, "j-high": HIGH, "j-low": LOW, "j-no-reading": SINK}
_STAYING = {"c-stays", "r-stays"}
NONELEC_VOX = (NONELEC.display, VOX.display)
A_SET = ("SETS", "Late Lounge")


def _seeded_place(place: str) -> tuple[str, str]:
    if place == "old":
        return OLD_JAZZ
    if place == "vox":
        return NONELEC_VOX
    if place == "set":
        return A_SET
    return (NONELEC.display, place)


@pytest.fixture
def before_u133(machine, silence):  # noqa: F811
    """A library whose Jazz tracks sit in NonElectronic's Jazz playlist, as on 2026-10-12."""
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
        sets = rb_writer.ensure_folder(handle, A_SET[0])
        for content_id, _genre, _tag, held in _SEEDED:
            for place in held:
                folder_display, sub_display = _seeded_place(place)
                folder = (
                    sets
                    if place == "set"
                    else rb_writer.ensure_folder(handle, folder_display, parent=root)
                )
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


def test_the_gate_shows_every_jazz_track_moving_and_no_other_track(before_u133):
    shown = _shown(VERB)
    rows = {row["content_id"]: row for row in shown["items"]}
    assert set(rows) == set(_ENDS) and len(shown["items"]) == len(_ENDS)
    for content_id, sub in _ENDS.items():
        row = rows[content_id]
        assert (row["bucket"], row["target"], row["add"]) == (JAZZ.id, sub, sub), content_id
        assert row["remove"] == [FORMER.id], content_id
    assert shown["left"] == []


def test_an_approved_move_files_jazz_in_its_bands_and_keeps_every_other_membership(
    before_u133,
):
    before = _live(before_u133)
    job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    after, removed = _live(before_u133), _removed(before_u133)

    for content_id, sub in _ENDS.items():
        seeded = next(held for cid, _g, _t, held in _SEEDED if cid == content_id)
        kept = {_seeded_place(place) for place in seeded if place != "old"}
        assert after[content_id] == {destination(DECLARED, JAZZ.id, sub), *kept}, content_id
        assert removed[content_id] == {OLD_JAZZ}, content_id
    # "WITH VOX" AND A SET ARE KEPT: a sub class and a playlist outside the
    # tree are never a place a move removes.
    assert NONELEC_VOX in after["j-med"]
    assert A_SET in after["j-high"]
    # A track with no reading lands in Unsorted.
    assert after["j-no-reading"] == {("Jazz", "Unsorted")}
    # The other styles are where they were, and nothing of theirs removed.
    for content_id in _STAYING:
        assert after[content_id] == before[content_id], content_id
        assert content_id not in removed, content_id
    # THE OLD JAZZ PLAYLIST IS EMPTY.
    assert not any(OLD_JAZZ in places for places in after.values())

    report = artifacts.committed(before_u133, job_id)[-1]
    assert (report["added"], report["removed"]) == (len(_ENDS), len(_ENDS))
    assert sorted(report["moved"]) == sorted(_ENDS)


def test_adoption_after_the_move_files_none_of_them_a_second_time(before_u133):
    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    collection.reset_cache()
    rows = _rows(before_u133)

    shown = _shown(VERB)
    assert shown["items"] == [] and shown["left"] == []
    plan = apply_cli.current_plan(before_u133, DECLARED)
    entries = {entry.content_id: entry for entry in plan.entries}
    for content_id, sub in _ENDS.items():
        entry = entries[content_id]
        assert (entry.bucket, entry.sub) == (JAZZ.id, sub), content_id
        assert not entry.held_elsewhere, content_id
    assert _rows(before_u133) == rows
