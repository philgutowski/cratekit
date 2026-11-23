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
from cratekit.core import routing, tags, taxonomy
from cratekit.organize import mirror_edits
from cratekit.write import rebuild, trees
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
