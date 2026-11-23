"""U339: after ``tag set``, ``adopt move`` files the track under its new genre's folder.

A filed track's genre is moved, through the verb, to a genre another top level
folder files by; then ``adopt move`` takes it out of its old genre folder's
energy band, ``with vox`` and Favorites (R-1965) and into the new folder's, the
one move it makes across folders.
A track a person put in a second genre folder by hand is left there, and a
genre moved back asks nothing. The library is ``tests/test_adopt_move.py``'s.
D1 applies.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import collection, genre_moves
from cratekit.adopt import move as adopt_move
from cratekit.core import rb_writer, routing, session, tags, taxonomy
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import genre_set_cli
from cratekit.write import genre_favorites, trees
from cratekit.write.routing_pass import destination
from tests.cli_drive import approve_and_queue, drive
from tests.test_adopt_move import DECLARED, HIGH, LOW, _live, _removed, seed_library
from tests.test_adopt_workers import _calibrate, _resume, _tag_vox
from tests.test_adopt_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_adopt_workers import _reader_cache as _reader_cache  # noqa: PLC0414
from tests.test_adopt_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_adopt_workers import library as library  # noqa: PLC0414
from tests.test_adopt_workers import machine as machine  # noqa: PLC0414
from tests.test_adopt_workers import silence as silence  # noqa: PLC0414

#: The bucket the track is filed in, and the one its new genre names.
OLD_BUCKET, OLD_GENRE = "house_funky_disco", "Funky House"
NEW_BUCKET, NEW_GENRE = "deep_house", "Deep House"


def _place(bucket: str, band: str) -> tuple[str, str]:
    return destination(DECLARED, bucket, band)


@pytest.fixture
def filed(machine, silence):
    """``mover`` and ``stays`` in the old folder's high band, ``second`` in the new
    folder's low band and, put there by hand, in the old folder's high band too."""
    tracks = [
        ("mover", OLD_GENRE, "8"),
        ("stays", OLD_GENRE, "8"),
        ("second", NEW_GENRE, "2"),
    ]
    places = [
        (*_place(OLD_BUCKET, HIGH), "mover"),
        (*_place(OLD_BUCKET, HIGH), "stays"),
        (*_place(NEW_BUCKET, LOW), "second"),
        (*_place(OLD_BUCKET, HIGH), "second"),
    ]
    seed_library(machine, silence, tracks, places, on=date(2026, 10, 1))
    music = Path(machine.library.root) / "Music"
    for stray in ("one.flac", "two.flac"):
        (music / stray).unlink(missing_ok=True)
    for content_id, genre, _energy in tracks:
        assert tags.write_tags(music / f"{content_id}.flac", {"genre": genre})
    session.record_acknowledgment(machine, terminal=lambda: True)
    collection.reset_cache()
    return machine


def _held(cfg, content_id: str) -> set[tuple[str, str]]:
    collection.reset_cache()
    return set(_live(cfg).get(content_id, ()))


def _tag_set(*argv: str) -> dict:
    verb = ["tag", "set", NEW_GENRE, *argv]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), acted
    collection.reset_cache()
    return acted


def _shown() -> dict:
    code, refused = drive(["adopt", "move"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused["cause"]["detail"]["shown"]


def _move() -> dict:
    _run_id, job_id = approve_and_queue(["adopt", "move"], "adopt.move.approve")
    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed
    collection.reset_cache()
    return resumed


def test_the_moved_track_leaves_its_old_genre_folder_for_the_new_ones_band(filed):
    old, new = _place(OLD_BUCKET, HIGH), _place(NEW_BUCKET, HIGH)
    assert _held(filed, "mover") == {old}
    acted = _tag_set("--row", "mover")
    assert "crate adopt move" in acted["warnings"][-1]["message"]
    assert dict(genre_moves.read(filed)) == {"mover": frozenset({OLD_BUCKET})}

    shown = _shown()
    (move,) = shown["items"]
    assert (move["content_id"], move["bucket"], move["target_bucket"]) == (
        "mover", OLD_BUCKET, NEW_BUCKET
    )
    assert (move["target"], move["add"], move["remove"]) == (HIGH, HIGH, [HIGH])
    assert move["decided_by"] == adopt_move.DECIDED_BY_GENRE

    _move()

    assert _held(filed, "mover") == {new}
    assert old in set(_removed(filed).get("mover", ()))
    # THE ENTRY IS SPENT, and the others stay where they were.
    assert dict(genre_moves.read(filed)) == {}
    assert _held(filed, "stays") == {old}
    assert _held(filed, "second") == {old, _place(NEW_BUCKET, LOW)}


def test_rows_never_filed_are_filed_by_the_step_the_run_names(filed, silence):
    """A row with no genre given one, filed nowhere: the run names `adopt apply`
    first, and the two steps file every row (review round one)."""
    import shutil

    from tests.test_adopt_move import _sql

    music = Path(filed.library.root) / "Music"
    shutil.copyfile(music / "stays.flac", music / "fresh.flac")
    assert tags.clear_tags(music / "fresh.flac", ["genre"])
    _sql(
        filed,
        "INSERT INTO djmdContent (ID, FolderPath, Title, GenreID, rb_local_deleted, "
        "created_at, updated_at) SELECT 'fresh', REPLACE(FolderPath, 'stays', 'fresh'), "
        "'fresh', NULL, 0, created_at, updated_at FROM djmdContent WHERE ID = 'stays'",
    )
    collection.reset_cache()
    acted = _tag_set("--row", "fresh", "--row", "mover")
    said = acted["warnings"][1]["message"]
    assert "run `crate adopt apply`" in said and "then `crate adopt move`, which takes the 1" in said
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, applied = drive(_resume(job_id))
    assert code == int(ExitCode.OK), applied
    _move()
    assert _held(filed, "fresh") == {_place(NEW_BUCKET, HIGH)}
    assert _held(filed, "mover") == {_place(NEW_BUCKET, HIGH)}
    assert dict(genre_moves.read(filed)) == {}


def test_a_genre_given_again_after_the_approval_refuses_the_move_stale(filed):
    """The folder a move files into is part of what was approved (review round one)."""
    from tests.test_adopt_move import _sql

    _sql(
        filed,
        "INSERT INTO djmdGenre (ID, Name, UUID, rb_local_deleted, created_at, updated_at) "
        "VALUES ('9990', 'Tech House', 'u', 0, '2026-10-01', '2026-10-01')",
    )
    _tag_set("--row", "mover")
    _run_id, job_id = approve_and_queue(["adopt", "move"], "adopt.move.approve")
    verb = ["tag", "set", "Tech House", "--row", "mover"]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK) and acted["data"]["totals"]["written"] == 1, acted
    collection.reset_cache()

    code, resumed = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    inner = resumed["cause"]["inner"]
    assert inner["reason"] == "decision-stale"
    assert inner["detail"]["moved_under"] == {"mover": "its genre names another folder now"}
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH)}


def test_a_track_leaving_two_folders_in_one_job_spends_both(filed):
    """Two moves of one track in one job each spend their folder (review round two)."""
    from tests.test_adopt_move import _sql

    _sql(
        filed,
        "INSERT INTO djmdGenre (ID, Name, UUID, rb_local_deleted, created_at, updated_at) "
        "VALUES ('9990', 'Tech House', 'u', 0, '2026-10-01', '2026-10-01')",
    )
    _tag_set("--row", "mover")
    for _ in range(2):
        _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
        assert drive(_resume(job_id))[0] == int(ExitCode.OK)
        collection.reset_cache()
        if _ == 0:
            verb = ["tag", "set", "Tech House", "--row", "mover"]
            _code, refused = drive(verb)
            run_id = refused["run_id"]
            drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply",
                   "--actor", "a-person"])
            assert drive(["--run", run_id, *verb])[0] == int(ExitCode.OK)
            collection.reset_cache()
    assert dict(genre_moves.read(filed)) == {"mover": frozenset({OLD_BUCKET, NEW_BUCKET})}
    _move()
    assert _held(filed, "mover") == {_place("tech_house", HIGH)}
    assert dict(genre_moves.read(filed)) == {}


def test_a_hand_placed_second_folder_is_never_asked_without_a_genre_move(filed):
    assert _shown()["items"] == []
    assert _held(filed, "second") == {_place(OLD_BUCKET, HIGH), _place(NEW_BUCKET, LOW)}


def test_a_move_already_half_made_by_adoption_only_removes(filed):
    _tag_set("--row", "mover")
    # ADOPTION FILES IT IN THE NEW FOLDER FIRST, and leaves the old one.
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, applied = drive(_resume(job_id))
    assert code == int(ExitCode.OK), applied
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH), _place(NEW_BUCKET, HIGH)}
    (move,) = _shown()["items"]
    assert (move["add"], move["remove"]) == ("", [HIGH])
    _move()
    assert _held(filed, "mover") == {_place(NEW_BUCKET, HIGH)}


def test_a_genre_moved_back_asks_nothing_of_the_old_folder(filed):
    _tag_set("--row", "mover")
    verb = ["tag", "set", OLD_GENRE, "--row", "mover"]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), acted
    collection.reset_cache()
    # THE OLD BUCKET IS THE ONE THE GENRE NAMES AGAIN, and the new one was never
    # filed, so the entry is spent and nothing waits on it.
    assert dict(genre_moves.read(filed)) == {}
    assert _shown()["items"] == []
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH)}


def _entry(bucket: str, genre: str) -> "adopt_move.PlanEntry":
    from cratekit.adopt.plan import PlanEntry
    from cratekit.adopt.scan import Disposition, Readability

    return PlanEntry(
        entry_id=f"e-{bucket}", content_id="mover", recorded="/m.flac",
        disposition=Disposition.ROUTE, category=Readability.READABLE, genre=genre,
        tree=DECLARED.tree.id, bucket=bucket, sub=HIGH, energy=8,
    )


def test_a_bucket_any_entry_of_the_track_claims_is_never_left():
    """Per content identifier, never per entry, so a second genre folder an
    entry of the same track files it in (U340) is kept."""
    moved = {"mover": frozenset({OLD_BUCKET})}
    alone = [_entry(NEW_BUCKET, NEW_GENRE)]
    assert adopt_move.still_moved(alone, DECLARED, moved) == moved
    both = [*alone, _entry(OLD_BUCKET, NEW_GENRE)]
    assert adopt_move.still_moved(both, DECLARED, moved) == {}
    named = [_entry(NEW_BUCKET, OLD_GENRE)]
    assert adopt_move.still_moved(named, DECLARED, moved) == {}


def test_a_move_stopped_before_its_removal_keeps_its_entry_and_a_resume_finishes(
    filed, monkeypatch
):
    """The entry is spent only once the track reads back moved (mutation table, M24)."""
    from cratekit.core import jobs, rb_writer
    from tests.test_adopt_move import _fails

    _tag_set("--row", "mover")
    _run_id, job_id = approve_and_queue(["adopt", "move"], "adopt.move.approve")
    with monkeypatch.context() as patched:
        patched.setattr(rb_writer, "remove_memberships", _fails)
        code, failed = drive(_resume(job_id))
    assert code != int(ExitCode.OK), failed
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH), _place(NEW_BUCKET, HIGH)}
    assert dict(genre_moves.read(filed)) == {"mover": frozenset({OLD_BUCKET})}

    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    collection.reset_cache()
    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed
    assert _held(filed, "mover") == {_place(NEW_BUCKET, HIGH)}
    assert dict(genre_moves.read(filed)) == {}


def test_a_track_with_a_second_genre_leaves_only_its_old_folder(filed):
    """One move, by the first genre's entry; the second genre's folder stays (U340)."""
    from cratekit.tagging import second_cli

    verb = ["tag", "second", "Tech House", "--row", "mover"]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, second_cli.CONFIRM_GATE, "apply", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), acted
    collection.reset_cache()
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    assert drive(_resume(job_id))[0] == int(ExitCode.OK)
    collection.reset_cache()
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH), _place("tech_house", HIGH)}

    _tag_set("--row", "mover")
    (move,) = _shown()["items"]
    assert (move["bucket"], move["target_bucket"]) == (OLD_BUCKET, NEW_BUCKET)
    _move()

    assert _held(filed, "mover") == {_place(NEW_BUCKET, HIGH), _place("tech_house", HIGH)}
    assert dict(genre_moves.read(filed)) == {}


# ── R-1965: the derived memberships of the old folder leave with the band ───

#: The derived sub classes adoption files beside a band, and the manual one.
VOX = trees.VOX_SUB_CLASS
FAVORITES = genre_favorites.favorites_class(DECLARED).id
CANDY = next(e.id for e in DECLARED.sub_classes if e.policy is taxonomy.SubPolicy.MANUAL)
#: The bucket with a genre sub in the shipped template, the sub and its genre.
GENRE_SUB_BUCKET = next(b.id for b in DECLARED.buckets if b.genre_subs)
GENRE_SUB, GENRE_SUB_GENRE = (
    DECLARED.bucket(GENRE_SUB_BUCKET).genre_subs[0].id,
    DECLARED.bucket(GENRE_SUB_BUCKET).genre_subs[0].sources[0],
)
#: The source the genre Favorites mirror, in a folder outside the tree.
SOURCE = ("Favorites", genre_favorites.favorites_class(DECLARED).signal_playlist)


def _in_tree(cfg, content_id: str) -> set[tuple[str, str]]:
    """What ``_held`` reads, the source playlist outside the tree left out."""
    return _held(cfg, content_id) - {SOURCE}


def _apply() -> dict:
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, applied = drive(_resume(job_id))
    assert code == int(ExitCode.OK), applied
    collection.reset_cache()
    return applied


@pytest.fixture
def sung(machine, silence):
    """``mover`` vox tagged and a favourite, ``plain`` a favourite only, and
    ``kept`` a favourite in the old folder's Candy too, each filed by
    ``adopt apply`` in the old folder's high band, ``with vox`` and Favorites as
    its tags and the source say; ``deep`` in the new folder gives the library
    its genre row. The cut and the tag rows are the ones the vocals verb
    leaves (``tests/test_adopt_workers.py``)."""
    movers = ("mover", "plain", "kept")
    tracks = [*((content_id, OLD_GENRE, "8") for content_id in movers), ("deep", NEW_GENRE, "2")]
    places = [
        *((*_place(OLD_BUCKET, HIGH), content_id) for content_id in movers),
        *((*SOURCE, content_id) for content_id in movers),
        (*_place(OLD_BUCKET, CANDY), "kept"),
        (*_place(NEW_BUCKET, LOW), "deep"),
    ]
    seed_library(machine, silence, tracks, places, on=date(2026, 10, 1), outside=(SOURCE[0],))
    music = Path(machine.library.root) / "Music"
    for stray in ("one.flac", "two.flac"):
        (music / stray).unlink(missing_ok=True)
    for content_id, genre, _energy in tracks:
        assert tags.write_tags(music / f"{content_id}.flac", {"genre": genre})
    session.record_acknowledgment(machine, terminal=lambda: True)
    _calibrate(machine)
    _tag_vox(machine, "mover")
    collection.reset_cache()
    _apply()
    return machine


def test_a_vocal_favourite_leaves_the_old_folders_with_vox_and_favorites_too(sung):
    """The brief's drive: filed, given another genre, applied, moved; it ends in
    the new folder's band, ``with vox`` and Favorites and nowhere in the old."""
    olds = {_place(OLD_BUCKET, sub) for sub in (HIGH, VOX, FAVORITES)}
    news = {_place(NEW_BUCKET, sub) for sub in (HIGH, VOX, FAVORITES)}
    assert _in_tree(sung, "mover") == olds

    acted = _tag_set("--row", "mover")
    said = acted["warnings"][-1]["message"]
    assert "crate adopt move" in said and "in rekordbox" not in said
    _apply()
    assert _in_tree(sung, "mover") == olds | news

    (move,) = _shown()["items"]
    assert (move["bucket"], move["target_bucket"], move["add"]) == (OLD_BUCKET, NEW_BUCKET, "")
    assert move["remove"] == sorted([HIGH, VOX, FAVORITES]) == move["holds"]

    _move()

    assert _in_tree(sung, "mover") == news
    assert olds <= set(_removed(sung).get("mover", ()))
    assert dict(genre_moves.read(sung)) == {}
    # NOTHING ELSE MOVED: the others stay as adoption filed them.
    assert _in_tree(sung, "plain") == {_place(OLD_BUCKET, s) for s in (HIGH, FAVORITES)}


def test_a_favourite_with_no_vocal_sub_leaves_the_old_favorites(sung):
    """The Favorites membership alone, with no ``with vox``, moved before
    ``adopt apply`` files the new folder, so the move adds the band itself."""
    _tag_set("--row", "plain")
    (move,) = _shown()["items"]
    assert (move["add"], move["remove"]) == (HIGH, sorted([HIGH, FAVORITES]))
    _move()
    assert _in_tree(sung, "plain") == {_place(NEW_BUCKET, HIGH)}
    assert _place(OLD_BUCKET, FAVORITES) in set(_removed(sung).get("plain", ()))


def test_a_manual_sub_is_never_removed_and_keeps_the_old_folders_favorites(sung):
    """Candy keeps the track in the old folder, so its Favorites there is still
    what the mirror files; removing it would be undone by the next refresh."""
    _tag_set("--row", "kept")
    (move,) = _shown()["items"]
    assert move["remove"] == [HIGH]
    _move()
    assert _in_tree(sung, "kept") == {
        _place(OLD_BUCKET, CANDY), _place(OLD_BUCKET, FAVORITES), _place(NEW_BUCKET, HIGH)
    }
    assert dict(genre_moves.read(sung)) == {}


def test_a_derived_membership_added_after_the_approval_refuses_the_move_stale(sung):
    """The worker asks the plan's own rule again: a sub nobody was shown leaving."""
    _tag_set("--row", "plain")
    _run_id, job_id = approve_and_queue(["adopt", "move"], "adopt.move.approve")
    handle = rb_writer.open_db(rb_writer.live_db_path(sung), unlock=False, cfg=sung)
    try:
        tree = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        folder = rb_writer.ensure_folder(handle, _place(OLD_BUCKET, VOX)[0], parent=tree)
        vocal = rb_writer.ensure_playlist(handle, _place(OLD_BUCKET, VOX)[1], folder)
        rb_writer.add_memberships(handle, vocal, ["plain"])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    collection.reset_cache()

    code, resumed = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    inner = resumed["cause"]["inner"]
    assert inner["reason"] == "decision-stale"
    assert inner["detail"]["moved_under"] == {"plain": "it holds a sub nobody was shown"}
    assert _place(OLD_BUCKET, HIGH) in _in_tree(sung, "plain")


def _node(bucket: str, sub: str, *content_ids: str, playlist_id: str, names=None):
    from cratekit.write import rebuild

    folder, playlist = names or _place(bucket, sub)
    return rebuild.TreeNode(
        folder_id=f"f-{bucket}", folder_display=folder, playlist_id=playlist_id,
        playlist_display=playlist, content_ids=frozenset(content_ids),
    )


def test_the_shipped_places_beside_a_band_are_the_two_derived_classes_and_the_genre_subs():
    from cratekit.adopt.plan import alongside_places

    assert alongside_places(DECLARED, OLD_BUCKET) == (VOX, FAVORITES)
    assert alongside_places(DECLARED, GENRE_SUB_BUCKET) == (VOX, FAVORITES, GENRE_SUB)


def test_the_reader_files_each_place_beside_the_band_and_the_folders_other_playlists_apart():
    from cratekit.adopt import placements as adopt_placements
    from cratekit.adopt.plan import alongside_places

    beside = alongside_places(DECLARED, OLD_BUCKET)
    nodes = [
        _node(OLD_BUCKET, HIGH, "t", playlist_id="p1"),
        *(_node(OLD_BUCKET, sub, "t", playlist_id=f"p-{sub}") for sub in beside),
        _node(OLD_BUCKET, FAVORITES, "u", playlist_id="p3"),
        _node(OLD_BUCKET, CANDY, "t", playlist_id="p4"),
        _node(OLD_BUCKET, HIGH, "u", playlist_id="p5", names=(_place(OLD_BUCKET, HIGH)[0], "Mine")),
        _node(NEW_BUCKET, CANDY, "u", playlist_id="p6"),
    ]
    found = adopt_placements.placements_from(DECLARED, nodes, None)
    assert found.holds(OLD_BUCKET, "t") == (HIGH,)
    assert found.holds_alongside(OLD_BUCKET, "t") == tuple(sorted(beside))
    assert found.holds_alongside(OLD_BUCKET, "u") == (FAVORITES,)
    assert found.holds_alongside_unnamed(OLD_BUCKET, "t") == ()
    # THE OTHER PLAYLISTS OF THE FOLDER ITS OWN PLACES ANSWER FROM, by name, and
    # a playlist of another folder is that folder's.
    assert found.holds_others(OLD_BUCKET, "t") == (_place(OLD_BUCKET, CANDY)[1],)
    assert found.holds_others(OLD_BUCKET, "u") == ("Mine",)
    assert found.holds_others(NEW_BUCKET, "u") == ()


def _asked(placements) -> tuple:
    entry = _entry(NEW_BUCKET, NEW_GENRE)
    moved = {"mover": frozenset({OLD_BUCKET})}
    competing = {b.id: routing.competing_subs(DECLARED, b.id) for b in DECLARED.buckets}
    asked = adopt_move.buckets_asked(entry, placements, DECLARED, competing, moved)
    found = adopt_move.standing_in(
        entry, OLD_BUCKET, placements, DECLARED, tree=DECLARED.tree.id, moved=moved
    )
    return asked, found


def _placed(**fields):
    from cratekit.adopt.plan import Placements

    return Placements(read=True, **{
        name: {OLD_BUCKET: {"mover": tuple(subs)}} for name, subs in fields.items()
    })


def test_a_derived_class_held_under_another_name_only_is_listed_never_moved():
    asked, found = _asked(_placed(held=(HIGH,), alongside=(VOX,), alongside_unnamed=(VOX,)))
    assert OLD_BUCKET in asked
    assert isinstance(found, adopt_move.Left)
    assert (found.reason, found.holds, found.holds_unnamed) == (
        adopt_move.LEFT_UNNAMED, tuple(sorted((HIGH, VOX))), (VOX,)
    )


def test_a_derived_class_alone_in_the_old_folder_is_asked_and_left():
    asked, found = _asked(_placed(alongside=(VOX,)))
    assert OLD_BUCKET in asked
    assert isinstance(found, adopt_move.Move)
    assert (found.add, found.remove, found.target_bucket) == (HIGH, (VOX,), NEW_BUCKET)


def test_a_favorites_another_playlist_keeps_is_not_asked_alone_and_not_left_beside_a_band():
    asked, found = _asked(_placed(alongside=(FAVORITES,), others=("Candy",)))
    assert OLD_BUCKET not in asked and found is None
    _asked_too, beside = _asked(_placed(held=(HIGH,), alongside=(FAVORITES, VOX), others=("Mine",)))
    assert beside.remove == tuple(sorted((HIGH, VOX)))
    # WITH NOTHING ELSE THERE, IT LEAVES WITH THE BAND.
    _asked_alone, alone = _asked(_placed(held=(HIGH,), alongside=(FAVORITES,)))
    assert alone.remove == tuple(sorted((FAVORITES, HIGH)))


def test_a_place_another_bucket_declares_names_no_folder_of_the_declarer():
    """A former place sits in the holder's folder and a split place is the
    holder's band, so neither makes the declarer read the holder's other
    playlists as its own (review round one)."""
    from cratekit.adopt import placements as adopt_placements
    from cratekit.adopt.plan import in_own_folder

    assert in_own_folder(DECLARED, "rnb", HIGH)
    assert not in_own_folder(DECLARED, "soul", "rnb_high")
    assert not in_own_folder(DECLARED, "hip_hop", "non_electronic_hip_hop")
    assert in_own_folder(DECLARED, "non_electronic", "non_electronic_hip_hop")
    nodes = [
        _node("rnb", HIGH, "t", playlist_id="p1"),
        _node("rnb", VOX, "t", playlist_id="p2"),
        _node(
            "non_electronic", "", "u", playlist_id="p3",
            names=adopt_placements.named_place(DECLARED, "hip_hop", "non_electronic_hip_hop"),
        ),
        _node("non_electronic", CANDY, "u", playlist_id="p4"),
    ]
    found = adopt_placements.placements_from(DECLARED, nodes, None)
    assert found.holds("soul", "t") == ("rnb_high",)
    assert found.holds_others("soul", "t") == ()
    assert found.holds_others("rnb", "t") == ()
    assert found.holds("hip_hop", "u") == ("non_electronic_hip_hop",)
    assert found.holds_others("hip_hop", "u") == ()
    assert found.holds_others("non_electronic", "u") == (_place("non_electronic", CANDY)[1],)


def _vocal_favourite(machine, silence, genre: str, places) -> None:
    """``mover`` vox tagged, a favourite, filed by ``adopt apply`` from ``places``;
    ``other`` carries ``genre`` so the library has its row."""
    tracks = [("mover", places[0][2], "8"), ("other", genre, "2")]
    seed_library(
        machine, silence, tracks, [*places[1:], (*SOURCE, "mover")],
        on=date(2026, 10, 1), outside=(SOURCE[0],),
    )
    music = Path(machine.library.root) / "Music"
    for stray in ("one.flac", "two.flac"):
        (music / stray).unlink(missing_ok=True)
    for content_id, track_genre, _energy in tracks:
        assert tags.write_tags(music / f"{content_id}.flac", {"genre": track_genre})
    session.record_acknowledgment(machine, terminal=lambda: True)
    _calibrate(machine)
    _tag_vox(machine, "mover")
    collection.reset_cache()
    _apply()


def test_a_row_moved_into_the_genre_split_out_of_its_folder_leaves_every_place_there(
    machine, silence
):
    """R&B to Soul, Soul's split place: R&B's band is Soul's own move to take
    out, so R&B's Favorites leaves with ``with vox`` in the same job, the job
    finishes and the entry is spent (review round one, BLOCKING)."""
    _vocal_favourite(
        machine, silence, "Soul",
        [("", "", "R&B"), (*_place("rnb", HIGH), "mover"), (*_place("soul", LOW), "other")],
    )
    rnb = {_place("rnb", sub) for sub in (HIGH, VOX, FAVORITES)}
    assert _in_tree(machine, "mover") == rnb
    _tag_set_genre("Soul", "mover")
    _apply()
    items = {item["bucket"]: item for item in _shown()["items"]}
    assert items["rnb"]["remove"] == sorted([VOX, FAVORITES])
    assert items["rnb"]["target_bucket"] == "soul"
    assert items["soul"]["remove"] == ["rnb_high"]

    _move()

    # ADOPTION WITHHELD THE SOUL ENTRY over the split place, so the move filed
    # the band, and the next apply files Soul's ``with vox`` and Favorites.
    assert _in_tree(machine, "mover") == {_place("soul", HIGH)}
    assert dict(genre_moves.read(machine)) == {}
    _apply()
    assert _in_tree(machine, "mover") == {_place("soul", sub) for sub in (HIGH, VOX, FAVORITES)}


def test_a_row_filed_in_a_genre_sub_leaves_it_with_the_band(machine, silence):
    """A Rominimal row ``route resort`` filed in the old folder's genre sub,
    given Deep House: the genre sub was filed by the genre it no longer
    carries, so it leaves with the band, and Favorites with it (review round
    one, BLOCKING)."""
    _vocal_favourite(
        machine, silence, NEW_GENRE,
        [
            ("", "", GENRE_SUB_GENRE),
            (*_place(GENRE_SUB_BUCKET, HIGH), "mover"),
            (*_place(NEW_BUCKET, LOW), "other"),
        ],
    )
    _run_id, job_id = approve_and_queue(["route", "resort"], "route.resort.apply")
    assert drive(_resume(job_id))[0] == int(ExitCode.OK)
    collection.reset_cache()
    old = {_place(GENRE_SUB_BUCKET, sub) for sub in (HIGH, VOX, FAVORITES, GENRE_SUB)}
    assert _in_tree(machine, "mover") == old
    _tag_set_genre(NEW_GENRE, "mover")
    _apply()
    (move,) = _shown()["items"]
    assert move["remove"] == sorted([HIGH, VOX, FAVORITES, GENRE_SUB])

    _move()

    assert _in_tree(machine, "mover") == {_place(NEW_BUCKET, s) for s in (HIGH, VOX, FAVORITES)}
    assert dict(genre_moves.read(machine)) == {}
    code, converged = drive(["converge"])
    assert code == int(ExitCode.OK), converged


def _tag_set_genre(genre: str, *rows: str) -> dict:
    verb = ["tag", "set", genre, *(arg for row in rows for arg in ("--row", row))]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), acted
    collection.reset_cache()
    return acted
