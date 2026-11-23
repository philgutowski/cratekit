"""U340: a track sits in a second genre folder beside the one its genre names.

The one rule (:func:`cratekit.core.routing.second_bucket`) first, then each path
that files a track by it: the rebuild derivation and the converge check over a
disposable database, adoption's census and plan, ``adopt move``'s plan and its
worker's check, and mirror edits' reading of an edit on the account. A track
with one genre is filed exactly as before in every one. Every expected bucket
and band is asked of the shipped taxonomy, never spelled. D1 applies.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.adopt import move as adopt_move
from cratekit.adopt import move_cli
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.cli import converge as converge_cli
from cratekit.core import convergence, rb_writer, routing, tags, taxonomy, tree_registry
from cratekit.organize import mirror_edits
from cratekit.write import genre_favorites, rebuild, routing_pass, trees
from tests import test_rebuild as _rebuild_suite
from tests.test_adopt_move import _scanned

DECLARED = taxonomy.default_taxonomy()
TREE_ID = DECLARED.tree.id

DEEP, TECH, MELODIC = "Deep House", "Tech House", "Melodic House"
ONE, TWO, THIRD = (DECLARED.bucket_for_display(word) for word in (DEEP, TECH, MELODIC))


def _band(level: int) -> str:
    return next(band.id for band in DECLARED.energy.bands if level <= band.max)


LOW, MED, HIGH = _band(1), _band(5), _band(9)


def _display(bucket: str, sub: str) -> str:
    return routing.energy_sub(DECLARED, bucket, None, source_genre="").display if not sub else next(
        found.display
        for level in range(1, int(DECLARED.energy.scale_max) + 1)
        if (found := routing.energy_sub(DECLARED, bucket, level, source_genre="")) is not None
        and found.id == sub
    )


def test_the_shipped_buckets_this_suite_names_are_three_energy_buckets():
    assert len({ONE, TWO, THIRD}) == 3 and None not in {ONE, TWO, THIRD}
    for bucket in (ONE, TWO, THIRD):
        assert routing.competing_subs(DECLARED, bucket)[0] is routing.Competing.BAND
        assert DECLARED.bucket(bucket).sub_by_source is None
    assert len({LOW, MED, HIGH}) == 3


# 1. The rule


@pytest.mark.parametrize(
    ("genre", "second", "expected"),
    [
        (DEEP, TECH, TWO),
        (DEEP, f"  {TECH}  ", TWO),
        (DEEP, DEEP, None),
        (DEEP, "", None),
        (DEEP, None, None),
        (DEEP, "Polka", None),
        (DEEP, next(iter(DECLARED.fallback.too_coarse_as_source)), None),
        ("", TECH, None),
        ("Polka", TECH, None),
    ],
    ids=[
        "names-another", "padded", "same-folder", "blank", "absent", "fallback", "too-coarse",
        "first-blank", "first-fallback",
    ],
)
def test_a_second_genre_names_a_second_folder_only_beside_a_genre_that_names_one(
    genre, second, expected
):
    assert routing.second_bucket(DECLARED, genre, second) == expected


# 2. The derivation, and the converge check it feeds


def _truth(location: str, *, energy: int, second: str | None, voxlevel: int | None = None):
    return rebuild.Truth(
        location=location, genre=DEEP, energy=energy, voxlevel=voxlevel, second_genre=second
    )


def test_the_derivation_places_a_track_in_both_folders_in_the_same_band():
    placements, _gaps = rebuild.derive_from_taxonomy(
        DECLARED, [_truth("/m/t.flac", energy=8, second=TECH)], vocal_threshold=None
    )
    assert {(one.bucket, one.sub) for one in placements} == {(ONE, HIGH), (TWO, HIGH)}


def test_a_one_genre_track_derives_exactly_as_before():
    with_none, _ = rebuild.derive_from_taxonomy(
        DECLARED, [_truth("/m/t.flac", energy=8, second=None)], vocal_threshold=None
    )
    same_folder, _ = rebuild.derive_from_taxonomy(
        DECLARED, [_truth("/m/t.flac", energy=8, second=DEEP)], vocal_threshold=None
    )
    assert [(one.bucket, one.sub) for one in with_none] == [(ONE, HIGH)]
    assert same_folder == with_none


def test_an_energy_change_moves_the_band_in_both_folders():
    placements, _ = rebuild.derive_from_taxonomy(
        DECLARED, [_truth("/m/t.flac", energy=1, second=TECH)], vocal_threshold=None
    )
    assert {(one.bucket, one.sub) for one in placements} == {(ONE, LOW), (TWO, LOW)}


def test_a_vocal_track_takes_with_vox_in_both_folders():
    placements, _ = rebuild.derive_from_taxonomy(
        DECLARED, [_truth("/m/t.flac", energy=8, second=TECH, voxlevel=99)], vocal_threshold=10.0
    )
    vox = {one.bucket for one in placements if one.sub == trees.VOX_SUB_CLASS}
    assert vox == {ONE, TWO}


def test_the_truth_reads_the_second_genre_in_the_same_open(tmp_path):
    from tests._containers import synth_container

    path = synth_container(tmp_path, ".flac")
    assert tags.write_tags(path, {"genre": DEEP, "energylevel": 8, "secondgenre": TECH})
    read = rebuild.read_truth(path)
    assert (read.genre, read.energy, read.second_genre) == (DEEP, 8, TECH)


# The converge check over a disposable database: the shared rebuild fixtures.
cfg = _rebuild_suite.cfg
library = _rebuild_suite.library
db = _rebuild_suite.db
adopted_root = _rebuild_suite.adopted_root
gates_pass = _rebuild_suite.gates_pass
_platform_seams = _rebuild_suite._platform_seams
_release_process_locks = _rebuild_suite._release_process_locks


def test_rebuild_files_both_and_a_cleared_second_genre_reads_as_that_folder_alone(
    cfg, gates_pass, db, adopted_root
):
    """One genre removed takes it out of that folder only, as converge reads it."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=TECH)
    other = replace(track, location=music(cfg, _rebuild_suite.PLAIN), second_genre=None)
    _rebuild_suite._rebuild(
        cfg, db, adopted_root, DECLARED, [], truth=[track, other]
    )
    both, _ = rebuild.derive_from_taxonomy(DECLARED, [track, other], vocal_threshold=None)
    assert _rebuild_suite._check(cfg, db, adopted_root, DECLARED, both).converged

    cleared, _ = rebuild.derive_from_taxonomy(
        DECLARED, [replace(track, second_genre=None), other], vocal_threshold=None
    )
    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, cleared)
    assert report.missing == ()
    assert [(one.content_id, one.bucket, one.sub) for one in report.unexpected] == [
        ("1", TWO, HIGH)
    ]


# R-1949: a cleared second genre leaves its track in that folder, and the
# check names the membership whatever else the playlist holds. The tree is
# made by hand, as adoption makes it, so no rebuild has recorded a node.


def _by_hand(db, adopted_root, members) -> dict:
    """Each ``(bucket, sub)`` playlist under the root holding ``members``' rows, its node id kept."""
    made = {}
    for (bucket, sub), ids in members.items():
        folder_name, playlist_name = routing_pass.destination(DECLARED, bucket, sub)
        folder = rb_writer.ensure_folder(db, folder_name, parent=adopted_root)
        playlist = rb_writer.ensure_playlist(db, playlist_name, folder)
        for content_id in ids:
            rb_writer.add_membership(db, playlist, content_id)
        made[(bucket, sub)] = str(playlist.ID)
    db.session.commit()
    return made


def _derived(*truths):
    placements, _gaps = rebuild.derive_from_taxonomy(DECLARED, list(truths), vocal_threshold=None)
    return placements


def _left(report) -> list[tuple[str | None, str, str]]:
    return [(one.content_id, one.bucket, one.sub) for one in report.unexpected]


def test_a_cleared_second_genre_alone_in_its_folder_is_named_by_the_check(
    cfg, gates_pass, db, adopted_root
):
    """THE RESIDUAL: alone in Tech House / High, the track read as a person's own playlist."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=TECH)
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    check = _rebuild_suite._check
    # THE CONTROL: before the clear the tree matches, both folders declared.
    assert check(cfg, db, adopted_root, DECLARED, _derived(track)).converged

    report = check(
        cfg, db, adopted_root, DECLARED, _derived(replace(track, second_genre=None))
    )
    assert not report.converged
    assert report.missing == ()
    assert _left(report) == [("1", TWO, HIGH)]
    (leftover,) = report.unexpected
    assert leftover.location is not None and leftover.location.endswith(_rebuild_suite.COMPOSED)
    assert (leftover.folder, leftover.playlist) == routing_pass.destination(DECLARED, TWO, HIGH)
    assert report.foreign == ()
    # What route resort names as left behind, the way a person is told to take it out.
    assert rebuild.left_behind(report, DECLARED) == (leftover,)


def test_a_cleared_second_genre_beside_another_track_of_that_folder_is_named_as_before(
    cfg, gates_pass, db, adopted_root
):
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    other = replace(
        track, location=music(cfg, _rebuild_suite.PLAIN), genre=TECH, second_genre=None
    )
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1", "2")})
    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, _derived(track, other))
    assert _left(report) == [("1", TWO, HIGH)]
    assert report.missing == ()


def test_a_one_genre_tree_still_matches_and_a_playlist_named_by_nothing_stays_foreign(
    cfg, gates_pass, db, adopted_root
):
    """P7 still holds: only a playlist bearing a declared destination's names is compared."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",)})
    folder_name, _playlist = routing_pass.destination(DECLARED, TWO, HIGH)
    folder = rb_writer.ensure_folder(db, folder_name, parent=adopted_root)
    own = rb_writer.ensure_playlist(db, _rebuild_suite.CURATED_PLAYLIST, folder)
    rb_writer.add_membership(db, own, "1")
    db.session.commit()

    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, _derived(track))
    assert report.converged
    assert report.unexpected == ()
    assert report.foreign == (f"{folder_name}/{_rebuild_suite.CURATED_PLAYLIST}",)


def test_a_soul_tracks_cleared_rnb_alone_in_the_rnb_band_is_named_too(
    cfg, gates_pass, db, adopted_root
):
    """The band is Soul's split place again, which ``adopt move`` takes it out of
    (``test_a_one_genre_soul_track_still_leaves_the_rnb_band``); until it does,
    the check names it."""
    soul, rnb = (DECLARED.bucket_for_display(word) for word in (SOUL, RNB))
    music = _rebuild_suite._music
    track = rebuild.Truth(
        location=music(cfg, _rebuild_suite.COMPOSED), genre=SOUL, energy=5, voxlevel=None,
        second_genre=RNB,
    )
    _by_hand(db, adopted_root, {(soul, MED): ("1",), (rnb, MED): ("1",)})
    check = _rebuild_suite._check
    assert check(cfg, db, adopted_root, DECLARED, _derived(track)).converged

    report = check(cfg, db, adopted_root, DECLARED, _derived(replace(track, second_genre=None)))
    assert _left(report) == [("1", rnb, MED)]


def test_a_vocal_playlist_the_run_did_not_compare_is_not_named_through_its_names(
    cfg, gates_pass, db, adopted_root
):
    """With no vocal calibration nothing was derived into ``with vox``, which is not evidence."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    _by_hand(
        db,
        adopted_root,
        {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",), (TWO, trees.VOX_SUB_CLASS): ("1",)},
    )
    check = _rebuild_suite._check
    placements = _derived(track)
    unjudged = check(
        cfg, db, adopted_root, DECLARED, placements, not_compared=(rebuild.VOCAL_DIMENSION,)
    )
    assert _left(unjudged) == [("1", TWO, HIGH)]
    vox_display = routing_pass.destination(DECLARED, TWO, trees.VOX_SUB_CLASS)
    assert unjudged.foreign == ("/".join(vox_display),)

    # Compared, the vocal playlist is a leftover too.
    judged = check(cfg, db, adopted_root, DECLARED, placements)
    assert sorted(_left(judged)) == sorted([("1", TWO, HIGH), ("1", TWO, trees.VOX_SUB_CLASS)])


def test_a_namesake_of_a_destination_already_resolved_elsewhere_is_left_as_it_was(
    cfg, gates_pass, db, adopted_root
):
    """A renamed folder keeps its destination; a fresh folder bearing the old names stays foreign."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    _rebuild_suite._rebuild(cfg, db, adopted_root, DECLARED, [], truth=[track])
    (built,) = rebuild.read_tree(db, str(adopted_root.ID))
    renamed = db.get_playlist(ID=built.folder_id)
    renamed.Name = _rebuild_suite.RENAMED_FOLDER
    db.session.commit()
    _by_hand(db, adopted_root, {(ONE, HIGH): ("2",)})

    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, _derived(track))
    assert report.unexpected == ()
    assert report.foreign == ("/".join(routing_pass.destination(DECLARED, ONE, HIGH)),)


def test_the_converge_verb_says_differing_over_a_cleared_second_genre(
    cfg, db, adopted_root, monkeypatch
):
    """The verb a DJ runs, driven: matching before the clear, differing after, naming the track."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=TECH)
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    tree_registry.write(cfg, _rebuild_suite._registry(str(adopted_root.ID)))
    readings = [track]
    monkeypatch.setattr(rebuild, "library_truth", lambda *_args, **_kwargs: list(readings))

    (before,) = _rebuild_suite._converge()["data"]["checks"]
    assert before["status"] == converge_cli.MATCHING, before
    # The word a person reads for the dimension an uncalibrated run left out.
    assert before["detail"].endswith("; not compared: vocal"), before

    readings[:] = [replace(track, second_genre=None)]
    (after,) = _rebuild_suite._converge()["data"]["checks"]
    assert after["status"] == converge_cli.DIFFERING, after
    assert f"unexpected:{TWO}/{HIGH}:1" in after["detail"]
    assert after["remedy"] is not None


def test_a_hand_filled_candy_playlist_alone_in_its_folder_stays_a_persons_own(
    cfg, gates_pass, db, adopted_root
):
    """Candy is a manual class: nothing derives into it, so its names are no evidence."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, "candy"): ("1", "2")})
    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, _derived(track))
    assert report.converged, report.summaries()
    assert report.foreign == ("/".join(routing_pass.destination(DECLARED, TWO, "candy")),)


def test_a_cleared_second_genre_leaves_its_genre_sub_named_as_well(
    cfg, gates_pass, db, adopted_root
):
    """A second genre that names a genre sub files the track there too, so the clear leaves both."""
    second = next(
        source
        for bucket in DECLARED.buckets
        for genre in bucket.genre_subs
        for source in genre.sources
        if routing.second_bucket(DECLARED, DEEP, source) == bucket.id
    )
    folder = routing.second_bucket(DECLARED, DEEP, second)
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=second)
    filed = {(one.bucket, one.sub) for one in _derived(track)}
    (genre_sub,) = [sub for bucket, sub in filed if bucket == folder and sub != HIGH]
    _by_hand(db, adopted_root, {place: ("1",) for place in filed})
    check = _rebuild_suite._check
    assert check(cfg, db, adopted_root, DECLARED, _derived(track)).converged

    report = check(cfg, db, adopted_root, DECLARED, _derived(replace(track, second_genre=None)))
    assert sorted(_left(report)) == sorted([("1", folder, HIGH), ("1", folder, genre_sub)])


def test_a_recorded_playlist_renamed_to_another_bands_names_keeps_its_own_destination(
    cfg, gates_pass, db, adopted_root
):
    """A node a record resolves is never compared again under the names it now bears."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    _rebuild_suite._rebuild(cfg, db, adopted_root, DECLARED, [], truth=[track])
    (built,) = rebuild.read_tree(db, str(adopted_root.ID))
    playlist = db.get_playlist(ID=built.playlist_id)
    playlist.Name = routing_pass.destination(DECLARED, ONE, MED)[1]
    db.session.commit()

    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, _derived(track))
    assert report.converged, report.summaries()
    assert report.renamed == (f"{ONE}/{HIGH}",)


def test_a_playlist_rekordbox_removed_is_not_compared_through_its_names(
    cfg, gates_pass, db, adopted_root
):
    """A removed playlist is one nobody sees; its names are no evidence."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    made = _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    check = _rebuild_suite._check
    assert _left(check(cfg, db, adopted_root, DECLARED, _derived(track))) == [("1", TWO, HIGH)]

    row = db.get_playlist(ID=made[(TWO, HIGH)])
    setattr(row, rb_writer.SOFT_DELETE_COLUMN, 1)
    db.session.commit()
    report = check(cfg, db, adopted_root, DECLARED, _derived(track))
    assert report.converged, report.summaries()


def test_a_cleared_second_genre_under_a_folder_renamed_in_rekordbox_is_named(
    cfg, gates_pass, db, adopted_root
):
    """The folder a rebuild recorded is read by its bucket's name, as a write resolves it."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=TECH)
    other = _truth(music(cfg, _rebuild_suite.PLAIN), energy=1, second=None)
    _rebuild_suite._rebuild(cfg, db, adopted_root, DECLARED, [], truth=[track, other])
    folder_id = next(
        node.folder_id
        for node in rebuild.read_tree(db, str(adopted_root.ID))
        if node.folder_display == DECLARED.bucket(TWO).display
    )
    folder = db.get_playlist(ID=folder_id)
    folder.Name = _rebuild_suite.RENAMED_FOLDER
    low = rb_writer.ensure_playlist(db, routing_pass.destination(DECLARED, TWO, LOW)[1], folder)
    rb_writer.add_membership(db, low, "2")
    db.session.commit()

    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, _derived(track, other))
    assert _left(report) == [("2", TWO, LOW)]
    assert report.foreign == ()


def test_a_favorites_playlist_the_run_did_not_compare_stays_foreign(
    cfg, gates_pass, db, adopted_root
):
    """With the favourites source unread, a Favorites playlist is left as it stands (U119)."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, "favorites"): ("1",)})
    report = _rebuild_suite._check(
        cfg, db, adopted_root, DECLARED, _derived(track),
        not_compared=(genre_favorites.FAVORITES_DIMENSION,),
    )
    assert report.converged, report.summaries()
    assert report.foreign == ("/".join(routing_pass.destination(DECLARED, TWO, "favorites")),)


def test_a_recorded_folder_renamed_to_another_genres_name_is_read_by_that_name(
    cfg, gates_pass, db, adopted_root
):
    """A folder bearing a declared bucket's name is that bucket's, whatever a record says."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=TECH)
    other = _truth(music(cfg, _rebuild_suite.PLAIN), energy=1, second=None)
    _rebuild_suite._rebuild(cfg, db, adopted_root, DECLARED, [], truth=[track, other])
    folder_id = next(
        node.folder_id
        for node in rebuild.read_tree(db, str(adopted_root.ID))
        if node.folder_display == DECLARED.bucket(TWO).display
    )
    folder = db.get_playlist(ID=folder_id)
    folder.Name = DECLARED.bucket(THIRD).display
    med = rb_writer.ensure_playlist(db, routing_pass.destination(DECLARED, THIRD, MED)[1], folder)
    rb_writer.add_membership(db, med, "2")
    db.session.commit()

    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, _derived(track, other))
    assert _left(report) == [("2", THIRD, MED)]


def test_a_record_naming_a_bucket_the_taxonomy_dropped_is_reported_not_raised(
    cfg, gates_pass, db, adopted_root
):
    """The record outlives a template edit; the check reads past it and says so."""
    music = _rebuild_suite._music
    track = _truth(music(cfg, _rebuild_suite.COMPOSED), energy=8, second=None)
    made = _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    (node,) = [
        one for one in rebuild.read_tree(db, str(adopted_root.ID))
        if one.playlist_id == made[(TWO, HIGH)]
    ]
    retired = convergence.DestinationNode(
        bucket="retired_genre", sub=HIGH, folder_id=node.folder_id, playlist_id="gone-1"
    )
    convergence.record_nodes(cfg, _rebuild_suite.TREE_ID, [retired])

    report = _rebuild_suite._check(cfg, db, adopted_root, DECLARED, _derived(track))
    assert _left(report) == [("1", TWO, HIGH)]
    assert report.undeclared == (f"retired_genre/{HIGH}",)


# 3. Adoption's census and plan


def _two(content_id: str, *, energy: int | None, second: str = TECH) -> adopt_scan.ScannedTrack:
    """A track whose genre routes to ONE and whose file names a second genre."""
    return replace(
        _scanned(content_id, ONE, energy=energy, genre=DEEP),
        second_genre=second,
        second_bucket=routing.second_bucket(DECLARED, DEEP, second) or "",
    )


def _plan(tracks, held: dict) -> adopt_plan.AdoptionPlan:
    placements = adopt_plan.Placements(read=True, held=held, unnamed={}, doubled={})
    return adopt_plan.build_adoption_plan(tracks, DECLARED, tree=TREE_ID, placements=placements)


def test_the_census_reads_the_second_genre_of_a_routed_track(tmp_path):
    rows = [
        adopt_scan.CollectionRow("1", str(tmp_path / "a.flac"), DEEP, False),
        adopt_scan.CollectionRow("2", str(tmp_path / "b.flac"), "", False),
        adopt_scan.CollectionRow("3", str(tmp_path / "c.flac"), DEEP, False),
    ]
    readers = {"a.flac": TECH, "b.flac": TECH}

    def reader(path: Path) -> str | None:
        if path.name not in readers:
            raise tags.TagReadFailed("unreadable")
        return readers[path.name]

    found = {
        track.content_id: track
        for track in adopt_scan.scan_rows(
            rows, DECLARED, root=tmp_path,
            probe=lambda _path: adopt_scan.Readability.READABLE,
            energy_reader=lambda _path: 8,
            second_reader=reader,
        )
    }
    assert (found["1"].second_genre, found["1"].second_bucket) == (TECH, TWO)
    # NO GENRE OF ITS OWN, so no second; AN UNREAD ONE, so no second.
    assert (found["2"].second_genre, found["2"].second_bucket) == ("", "")
    assert (found["3"].second_genre, found["3"].second_bucket) == ("", "")
    none = list(
        adopt_scan.scan_rows(
            rows[:1], DECLARED, root=tmp_path,
            probe=lambda _path: adopt_scan.Readability.READABLE,
            energy_reader=lambda _path: 8,
            second_reader=adopt_scan.NO_SECOND_GENRE,
        )
    )
    assert none[0].second_bucket == ""


def test_the_plan_gives_a_second_entry_and_counts_the_track_once():
    plan = _plan([_two("t", energy=8), _scanned("u", ONE, energy=8, genre=DEEP)], {})
    assert [(e.content_id, e.bucket, e.sub, e.second) for e in plan.entries] == [
        ("t", ONE, HIGH, False),
        ("t", TWO, HIGH, True),
        ("u", ONE, HIGH, False),
    ]
    assert len({entry.entry_id for entry in plan.entries}) == 3
    assert plan.counts()[str(adopt_scan.Disposition.ROUTE)] == 2
    assert plan.energy_readings()["read"] == 2
    assert [entry.content_id for entry in plan.seconds()] == ["t"]
    (shown,) = [row for row in adopt_plan.to_json(plan)["entries"] if row.get("second_genre")]
    assert (shown["content_id"], shown["bucket"]) == ("t", TWO)


def test_a_track_in_its_second_folder_is_no_stranger_there():
    existing = adopt_plan.ExistingFolder(
        display=DECLARED.bucket(TWO).display, node_id="n2", content_ids=("t", "u")
    )
    u = _scanned("u", TWO, energy=8, genre=TECH)
    plan = adopt_plan.build_adoption_plan(
        [_two("t", energy=8), u], DECLARED, tree=TREE_ID, existing=(existing,)
    )
    assert plan.collisions == ()
    # THE CONTROL: the same track with one genre is a stranger in that folder.
    alone = adopt_plan.build_adoption_plan(
        [_scanned("t", ONE, energy=8, genre=DEEP), u], DECLARED, tree=TREE_ID,
        existing=(existing,),
    )
    assert [(one.bucket, one.strangers) for one in alone.collisions] == [(TWO, 1)]


# 4. adopt move: each entry speaks for its own folder


def test_an_energy_change_moves_the_track_in_both_folders():
    plan = adopt_move.build_move_plan(_plan([_two("t", energy=8)], {ONE: {"t": (MED,)}, TWO: {"t": (MED,)}}), DECLARED)
    assert sorted((m.bucket, m.target, m.remove) for m in plan.moves) == sorted(
        [(ONE, HIGH, (MED,)), (TWO, HIGH, (MED,))]
    )
    assert plan.left == ()


def test_a_double_in_the_second_folder_is_moved_once_by_its_own_entry():
    """Without the claim, the first entry's tree path asks the same bucket too."""
    plan = adopt_move.build_move_plan(
        _plan([_two("t", energy=8)], {ONE: {"t": (HIGH,)}, TWO: {"t": (MED, HIGH)}}), DECLARED
    )
    (move,) = plan.moves
    assert (move.bucket, move.target, move.remove) == (TWO, HIGH, (MED,))
    assert plan.left == ()


def test_a_one_genre_track_in_another_folder_is_asked_as_before():
    plan = adopt_move.build_move_plan(
        _plan([_scanned("t", ONE, energy=8, genre=DEEP)], {ONE: {"t": (HIGH,)}, TWO: {"t": (MED, HIGH)}}),
        DECLARED,
    )
    (move,) = plan.moves
    assert (move.bucket, move.target, move.remove) == (TWO, HIGH, (MED,))


def test_the_worker_checks_a_move_against_the_entry_that_planned_it():
    held = {ONE: {"t": (MED,)}, TWO: {"t": (MED,)}}
    current = _plan([_two("t", energy=8)], held)
    approved = adopt_move.build_move_plan(current, DECLARED).moves
    todo, gone = move_cli.remaining(approved, current, DECLARED)
    assert sorted((m.bucket, m.target) for m in todo) == sorted([(ONE, HIGH), (TWO, HIGH)])
    assert gone == ()
    found = adopt_move.entries_by_track(current.entries)
    assert adopt_move.entry_for(found, "t", TWO).second
    assert not adopt_move.entry_for(found, "t", ONE).second
    assert not adopt_move.entry_for(found, "t", THIRD).second
    assert adopt_move.entry_for(found, "x", ONE) is None


SOUL, RNB = "Soul", "R&B"


def _split_pair(content_id: str, first: str, second: str, *, energy: int):
    """A track whose two genres are a split place's declarer and its holder."""
    return replace(
        _scanned(content_id, DECLARED.bucket_for_display(first), energy=energy, genre=first),
        second_genre=second,
        second_bucket=routing.second_bucket(DECLARED, first, second) or "",
    )


def _in_both(content_id: str, band: str) -> dict:
    """The track in Soul's band and R&B's, as placements read it: R&B's band
    is Soul's split place there too."""
    soul, rnb = (DECLARED.bucket_for_display(word) for word in (SOUL, RNB))
    (place,) = [one for one in DECLARED.bucket(soul).split_from if one.sub == band]
    return {soul: {content_id: (band, place.id)}, rnb: {content_id: (band,)}}


def test_the_shipped_soul_folder_declares_rnb_bands_as_split_places():
    soul, rnb = (DECLARED.bucket_for_display(word) for word in (SOUL, RNB))
    assert {place.bucket for place in DECLARED.bucket(soul).split_from} == {rnb}
    assert routing.second_bucket(DECLARED, SOUL, RNB) == rnb


@pytest.mark.parametrize(("first", "second"), [(SOUL, RNB), (RNB, SOUL)], ids=["soul-rnb", "rnb-soul"])
def test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either(first, second):
    """B1 of round one: the split place of the one is the other's own band."""
    held = _in_both("t", MED)
    plan = _plan([_split_pair("t", first, second, energy=5)], held)
    assert [(e.disposition, e.withheld_by) for e in plan.entries] == [
        (adopt_scan.Disposition.ROUTE, ""),
        (adopt_scan.Disposition.ROUTE, ""),
    ]
    moves = adopt_move.build_move_plan(plan, DECLARED)
    assert (moves.moves, moves.left) == ((), ())
    # NOT YET IN THE SECOND: adoption files it there, nothing withheld.
    soul = DECLARED.bucket_for_display(SOUL)
    only_first = {bucket: rows for bucket, rows in held.items() if bucket != soul}
    only_first[soul] = {"t": tuple(sub for sub in held[soul]["t"] if sub != MED)}
    fresh = _plan([_split_pair("t", first, second, energy=5)], only_first)
    assert [(e.bucket, e.disposition, e.holds) for e in fresh.entries if e.bucket == soul] == [
        (soul, adopt_scan.Disposition.ROUTE, ())
    ]
    assert adopt_move.build_move_plan(fresh, DECLARED).moves == ()


@pytest.mark.parametrize(("first", "second"), [(SOUL, RNB), (RNB, SOUL)], ids=["soul-rnb", "rnb-soul"])
def test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees(first, second):
    current = _plan([_split_pair("t", first, second, energy=9)], _in_both("t", MED))
    approved = adopt_move.build_move_plan(current, DECLARED).moves
    soul, rnb = (DECLARED.bucket_for_display(word) for word in (SOUL, RNB))
    assert sorted((m.bucket, m.target, m.remove) for m in approved) == sorted(
        [(soul, HIGH, (MED,)), (rnb, HIGH, (MED,))]
    )
    todo, gone = move_cli.remaining(approved, current, DECLARED)
    assert sorted((m.bucket, m.target) for m in todo) == sorted([(soul, HIGH), (rnb, HIGH)])
    assert gone == ()


def test_only_a_split_place_whose_holder_the_other_genre_names_is_kept():
    soul, rnb = (DECLARED.bucket_for_display(word) for word in (SOUL, RNB))
    every = {place.id for place in DECLARED.bucket(soul).split_from}
    assert adopt_plan.kept_beside(DECLARED, soul, frozenset({rnb})) == every
    assert adopt_plan.kept_beside(DECLARED, soul, frozenset({ONE})) == frozenset()
    assert adopt_plan.kept_beside(DECLARED, soul, frozenset()) == frozenset()


def test_a_soul_track_whose_second_genre_is_another_folder_still_leaves_the_rnb_band():
    """The other genre names Deep House, not R&B, so R&B's band is Soul's split place."""
    soul = DECLARED.bucket_for_display(SOUL)
    plan = _plan([_split_pair("t", SOUL, DEEP, energy=5)], _in_both("t", MED))
    (move,) = [one for one in adopt_move.build_move_plan(plan, DECLARED).moves if one.bucket == soul]
    (place,) = [one for one in DECLARED.bucket(soul).split_from if one.sub == MED]
    assert (move.target, move.remove) == (MED, (place.id,))


def test_a_one_genre_soul_track_still_leaves_the_rnb_band():
    """THE CONTROL: with no second genre, R&B's band is Soul's split place."""
    soul = DECLARED.bucket_for_display(SOUL)
    held = _in_both("t", MED)
    plan = _plan([_scanned("t", soul, energy=5, genre=SOUL)], held)
    (move,) = adopt_move.build_move_plan(plan, DECLARED).moves
    (place,) = [one for one in DECLARED.bucket(soul).split_from if one.sub == MED]
    assert (move.bucket, move.target, move.remove) == (soul, MED, (place.id,))


# 5. Mirror edits: an edit on the account in one folder leaves the other


def _decision(outcome: str, to: tuple[str, str], was: list[tuple[str, str]], account: list[tuple[str, str]]):
    """An edit the rule decided, in the shape the step reads: places by title."""

    def title(place: tuple[str, str]) -> str:
        return f"{place[0]} {place[1]}"

    every = {*was, *account, to}
    return SimpleNamespace(
        outcome=outcome,
        to=SimpleNamespace(folder=to[0], playlist=to[1], title=title(to)),
        was=tuple(sorted(title(one) for one in was)),
        account=tuple(sorted(title(one) for one in account)),
        settle=tuple((folder, title((folder, playlist)), True) for folder, playlist in every),
    )


def _at(bucket: str, sub: str) -> tuple[str, str]:
    return DECLARED.bucket(bucket).display, _display(bucket, sub)


TRUTH = rebuild.Truth(location="/m/t.flac", genre=DEEP, energy=5, second_genre=TECH)


def test_a_band_move_inside_the_second_folder_changes_the_energy_alone():
    from cratekit.modules.outbound import mirror_edits as edits

    edit = _decision(edits.MOVE, _at(TWO, HIGH), [_at(ONE, MED), _at(TWO, MED)], [_at(ONE, MED), _at(TWO, HIGH)])
    genre, energy, second = mirror_edits._second_genre_tags(DECLARED, edit, TRUTH, TWO)
    assert (genre, second) == (DEEP, TECH) and _band(energy) == HIGH


def test_a_move_out_of_one_folder_into_a_third_replaces_that_folders_genre_only():
    from cratekit.modules.outbound import mirror_edits as edits

    out_of_second = _decision(
        edits.MOVE, _at(THIRD, MED), [_at(ONE, MED), _at(TWO, MED)], [_at(ONE, MED), _at(THIRD, MED)]
    )
    genre, _energy, second = mirror_edits._second_genre_tags(DECLARED, out_of_second, TRUTH, TWO)
    assert genre == DEEP and routing.files_by_genre(DECLARED, second) == THIRD

    out_of_first = _decision(
        edits.MOVE, _at(THIRD, MED), [_at(ONE, MED), _at(TWO, MED)], [_at(TWO, MED), _at(THIRD, MED)]
    )
    genre, _energy, second = mirror_edits._second_genre_tags(DECLARED, out_of_first, TRUTH, TWO)
    assert second == TECH and routing.files_by_genre(DECLARED, genre) == THIRD


@pytest.mark.parametrize(
    ("to", "was", "account"),
    [
        # Taken out of the second folder only, left in the first.
        (lambda: _at(ONE, MED), lambda: [_at(ONE, MED), _at(TWO, MED)], lambda: [_at(ONE, MED)]),
        # Taken out of the first folder only, left in the second.
        (lambda: _at(TWO, MED), lambda: [_at(ONE, MED), _at(TWO, MED)], lambda: [_at(TWO, MED)]),
        # Added to a third folder and taken out of neither.
        (
            lambda: _at(THIRD, MED),
            lambda: [_at(ONE, MED), _at(TWO, MED)],
            lambda: [_at(ONE, MED), _at(TWO, MED), _at(THIRD, MED)],
        ),
    ],
    ids=["off-second", "off-first", "third-beside-both"],
)
def test_an_edit_that_does_not_say_which_genre_changed_is_not_taken(to, was, account):
    from cratekit.modules.outbound import mirror_edits as edits

    edit = _decision(edits.MOVE, to(), was(), account())
    why = mirror_edits._second_genre_tags(DECLARED, edit, TRUTH, TWO)
    assert isinstance(why, str) and "crate tag second" in why


@pytest.mark.parametrize("out_of", ["first", "second"])
def test_a_move_into_the_fallback_folder_is_not_taken(out_of):
    """B2 of round one: a word filing by the fallback alone files no second
    genre beside it, nor as one, so either move would lose a folder."""
    from cratekit.modules.outbound import mirror_edits as edits

    fallback = DECLARED.fallback.bucket
    assert routing.files_by_genre(DECLARED, DECLARED.bucket(fallback).display) is None
    kept = _at(TWO, MED) if out_of == "first" else _at(ONE, MED)
    edit = _decision(
        edits.MOVE, _at(fallback, MED), [_at(ONE, MED), _at(TWO, MED)], [kept, _at(fallback, MED)]
    )
    why = mirror_edits._second_genre_tags(DECLARED, edit, TRUTH, TWO)
    assert isinstance(why, str) and "crate tag second" in why
    # WHERE IT WOULD END: the fallback by the first genre, which rebuild
    # derives; the first folder alone when the second genre is the fallback's.
    ends = DECLARED.bucket(fallback if out_of == "first" else ONE).display
    assert f"file it into {ends} where" in why


def test_left_folders_reads_the_folders_a_band_left():
    from cratekit.modules.outbound import mirror_edits as edits

    edit = _decision(edits.MOVE, _at(THIRD, MED), [_at(ONE, MED), _at(TWO, MED)], [_at(ONE, MED), _at(THIRD, MED)])
    assert mirror_edits.left_folders(edit) == {DECLARED.bucket(TWO).display}


def test_the_write_reads_back_the_second_genre_and_leaves_a_one_genre_file_as_before(tmp_path):
    from tests._containers import synth_container

    path = synth_container(tmp_path, ".flac")
    assert tags.write_tags(path, {"genre": DEEP, "energylevel": 5, "secondgenre": TECH})
    change = mirror_edits.Change(
        "1", "t", "move", "t", str(path), DEEP, DEEP, 5, 9, second_was=TECH, second=MELODIC
    )
    assert mirror_edits._write_tags(change)
    assert tags.read_tag(path, "secondgenre") == MELODIC
    assert mirror_edits._write_tags(replace(change, second_was=MELODIC, second=None))
    assert tags.read_tag(path, "secondgenre") is None
    one = mirror_edits.Change("1", "t", "move", "t", str(path), DEEP, DEEP, 9, 5)
    assert mirror_edits._write_tags(one) and tags.read_energy_from_file(path) == 5
    assert "second genre" not in one.item() and len(one.identity()) == 9


def test_a_route_gate_column_names_both_folders_rather_than_the_last():
    from cratekit.write import routing_export

    named: dict[str, str] = {}
    for place in ("Deep House/High", "Tech House/High", "Tech House/High"):
        routing_export._shown(named, "k", place)
    assert named == {"k": "Deep House/High; Tech House/High"}
