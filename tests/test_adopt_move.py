"""R-758: a track is moved from the competing sub it holds to the one its file names.

Adoption withholds a track that already holds a competing sub and lists it.
``crate adopt move`` is the verb that acts on that list, and it is the first
verb in this product that removes a membership. The pure plan is held first,
then the verb through the real dispatcher against a disposable library with
real tags, then the writer's own guards.

Every expected identifier is derived from the shipped taxonomy's declarations
rather than spelled.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import shutil
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import apply_cli, artifacts, collection, move_cli
from cratekit.adopt import move as adopt_move
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.cli import handlers, registry
from cratekit.core import jobs, rb_writer, routing, session, taxonomy, tree_registry
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import trees
from cratekit.write.routing_pass import destination
from tests import adopt_fixtures
from tests.cli_drive import approve_and_queue, drive, drive_human
from tests.test_adopt_workers import (  # noqa: F401
    _energy_bucket,
    _platform_seams,
    _reader_cache,
    _release_process_locks,
    _resume,
    _style_bucket,
    library,
    machine,
    silence,
)

DECLARED = taxonomy.default_taxonomy()
TREE_ID = DECLARED.tree.id
GATE = "adopt.move.approve"
VERB = ["adopt", "move"]


def _band(level: int) -> str:
    return next(band.id for band in DECLARED.energy.bands if level <= band.max)


LOW, MED, HIGH = _band(1), _band(5), _band(9)
SINK = DECLARED.energy.no_energy_sub.id
CLASSES = {entry.id: entry for entry in DECLARED.sub_classes}
MANUAL = next(e.id for e in DECLARED.sub_classes if e.policy is taxonomy.SubPolicy.MANUAL)
DERIVED = next(e.id for e in DECLARED.sub_classes if e.policy is taxonomy.SubPolicy.DERIVED)


# ---------------------------------------------------------------------------
# The plan, with no database
# ---------------------------------------------------------------------------


def _pure_energy_bucket() -> taxonomy.Bucket:
    return next(
        bucket
        for bucket in DECLARED.buckets
        if bucket.sub_by_source is None and bucket.energy.enabled
    )


def _scanned(
    content_id: str, bucket: str, *, energy: int | None, genre: str = ""
) -> adopt_scan.ScannedTrack:
    return adopt_scan.ScannedTrack(
        content_id=content_id,
        recorded=f"/library/Music/{content_id}.flac",
        path=f"/library/Music/{content_id}.flac",
        readability=adopt_scan.Readability.READABLE,
        disposition=adopt_scan.Disposition.ROUTE,
        genre=genre or DECLARED.bucket(bucket).display,
        bucket=bucket,
        energy=energy,
    )


def _adoption(
    tracks, held: dict, *, unnamed: dict | None = None, doubled: dict | None = None
) -> adopt_plan.AdoptionPlan:
    placements = adopt_plan.Placements(
        read=True, held=held, unnamed=unnamed or {}, doubled=doubled or {}
    )
    return adopt_plan.build_adoption_plan(tracks, DECLARED, tree=TREE_ID, placements=placements)


def _moves(
    tracks, held: dict, *, unnamed: dict | None = None, doubled: dict | None = None
) -> adopt_move.MovePlan:
    return adopt_move.build_move_plan(
        _adoption(tracks, held, unnamed=unnamed, doubled=doubled), DECLARED
    )


def _left_counts(**nonzero: int) -> dict:
    """The left counts as the plan reports them, every reason present."""
    return {"total": sum(nonzero.values()), **{r: 0 for r in adopt_move.LEFT_REASONS}, **nonzero}


def test_a_track_in_med_whose_file_reads_eight_is_added_to_high_and_leaves_med():
    bucket = _pure_energy_bucket().id
    plan = _moves([_scanned("t", bucket, energy=8)], {bucket: {"t": (MED,)}})
    (move,) = plan.moves
    assert (move.target, move.add, move.remove, move.holds) == (HIGH, HIGH, (MED,), (MED,))
    assert (move.kind, move.decided_by, move.energy) == ("band", "energy", 8)
    assert plan.left == ()


def test_a_track_in_both_has_only_the_stale_one_removed():
    bucket = _pure_energy_bucket().id
    plan = _moves([_scanned("t", bucket, energy=8)], {bucket: {"t": (MED, HIGH)}})
    (move,) = plan.moves
    assert (move.target, move.add, move.remove) == (HIGH, "", (MED,))
    assert plan.counts()["memberships_added"] == 0
    assert plan.counts()["memberships_removed"] == 1


def test_a_track_in_three_bands_leaves_the_two_its_reading_does_not_name():
    bucket = _pure_energy_bucket().id
    plan = _moves([_scanned("t", bucket, energy=8)], {bucket: {"t": (LOW, MED, HIGH)}})
    (move,) = plan.moves
    assert (move.add, set(move.remove)) == ("", {LOW, MED})


@pytest.mark.parametrize("sub_class", sorted(CLASSES))
def test_a_sub_class_is_never_a_source_and_never_removed_from(sub_class):
    bucket = _pure_energy_bucket().id
    alone = _moves([_scanned("t", bucket, energy=8)], {bucket: {"t": (sub_class,)}})
    assert alone.moves == () and alone.left == ()

    beside = _moves([_scanned("t", bucket, energy=8)], {bucket: {"t": (sub_class, MED)}})
    (move,) = beside.moves
    assert move.remove == (MED,)
    assert sub_class not in move.holds


def test_both_policies_are_declared_so_the_test_above_means_something():
    assert {entry.policy for entry in DECLARED.sub_classes} == set(taxonomy.SubPolicy)


def test_a_track_whose_file_has_no_reading_is_left_and_listed():
    bucket = _pure_energy_bucket().id
    plan = _moves([_scanned("t", bucket, energy=None)], {bucket: {"t": (HIGH,)}})
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.reason, left.holds, left.target) == (adopt_move.LEFT_NO_READING, (HIGH,), SINK)
    assert plan.counts()["left"] == _left_counts(**{adopt_move.LEFT_NO_READING: 1})


def test_a_track_in_the_no_reading_sub_whose_file_now_reads_is_moved_out_of_it():
    bucket = _pure_energy_bucket().id
    plan = _moves([_scanned("t", bucket, energy=5)], {bucket: {"t": (SINK,)}})
    (move,) = plan.moves
    assert (move.add, move.remove) == (MED, (SINK,))


def test_a_track_already_where_its_reading_names_is_not_planned():
    bucket = _pure_energy_bucket().id
    plan = _moves([_scanned("t", bucket, energy=5)], {bucket: {"t": (MED,)}})
    assert plan.moves == () and plan.left == ()
    nowhere = _moves([_scanned("t", bucket, energy=5)], {})
    assert nowhere.moves == () and nowhere.left == ()


def test_the_genre_decides_a_style_move_and_a_genre_naming_no_style_is_left():
    bucket = _style_bucket()
    first, second = bucket.subs[0], bucket.subs[1]
    named = next(g for g, sub in bucket.sub_by_source.map.items() if sub == second.id)
    plan = _moves(
        [_scanned("t", bucket.id, energy=8, genre=named)], {bucket.id: {"t": (first.id,)}}
    )
    (move,) = plan.moves
    assert (move.kind, move.decided_by) == ("style", "genre")
    assert (move.add, move.remove, move.genre) == (second.id, (first.id,), named)

    unnamed_genre = "A genre no style is declared for"
    assert unnamed_genre not in bucket.sub_by_source.map
    held = next(sub.id for sub in bucket.subs if sub.id != bucket.sub_by_source.default)
    plan = _moves(
        [_scanned("t", bucket.id, energy=8, genre=unnamed_genre)],
        {bucket.id: {"t": (held,)}},
    )
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.reason, left.holds) == (adopt_move.LEFT_NO_STYLE, (held,))


def test_a_bucket_with_one_sub_and_no_energy_names_no_style():
    bucket = next(
        b for b in DECLARED.buckets if b.sub_by_source is None and not b.energy.enabled
    )
    kind, competing = routing.competing_subs(DECLARED, bucket.id)
    assert kind is routing.Competing.STYLE and competing == {bucket.single_sub.id}
    plan = _moves([_scanned("t", bucket.id, energy=8)], {bucket.id: {"t": tuple(competing)}})
    assert plan.moves == () and plan.left == ()


def test_a_bucket_that_reads_neither_energy_nor_genre_has_no_reading_to_move_on():
    """Found by the review. Nothing in the shipped template declares one, so
    the template is given one: several subs, no energy, no map from genre."""
    from dataclasses import replace

    plain = next(
        b for b in DECLARED.buckets if b.sub_by_source is None and not b.energy.enabled
    )
    extra = taxonomy.Sub("another_place", "Another place")
    buckets = tuple(
        replace(b, subs=(*b.subs, extra)) if b.id == plain.id else b
        for b in DECLARED.buckets
    )
    # The index is a field the loader fills, so it is rebuilt with the buckets.
    declared = replace(DECLARED, buckets=buckets, _by_id={b.id: b for b in buckets})
    kind, competing = routing.competing_subs(declared, plain.id)
    assert kind is routing.Competing.STYLE
    assert competing == {plain.single_sub.id, extra.id}

    plan = adopt_plan.build_adoption_plan(
        [_scanned("t", plain.id, energy=8)],
        declared,
        tree=TREE_ID,
        placements=adopt_plan.Placements(read=True, held={plain.id: {"t": (extra.id,)}}),
    )
    found = adopt_move.build_move_plan(plan, declared)
    assert found.moves == ()
    (left,) = found.left
    assert left.reason == adopt_move.LEFT_NO_READING


def test_a_sub_held_under_another_name_only_is_left_and_listed():
    bucket = _pure_energy_bucket().id
    plan = _moves(
        [_scanned("t", bucket, energy=8)],
        {bucket: {"t": (MED,)}},
        unnamed={bucket: {"t": (MED,)}},
    )
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.reason, left.holds_unnamed) == (adopt_move.LEFT_UNNAMED, (MED,))


def test_a_tree_nobody_read_plans_nothing_and_says_unread():
    bucket = _pure_energy_bucket().id
    unread = adopt_plan.build_adoption_plan(
        [_scanned("t", bucket, energy=8)],
        DECLARED,
        tree=TREE_ID,
        placements=adopt_plan.Placements(read=False, held={bucket: {"t": (MED,)}}),
    )
    plan = adopt_move.build_move_plan(unread, DECLARED)
    assert (plan.moves, plan.left, plan.placements) == ((), (), "unread")
    read = _moves([_scanned("t", bucket, energy=5)], {bucket: {"t": (MED,)}})
    assert read.moves == () and read.digest() != plan.digest()


def test_the_counts_split_by_kind_and_total():
    energy, style = _pure_energy_bucket().id, _style_bucket()
    named = next(g for g, sub in style.sub_by_source.map.items() if sub == style.subs[1].id)
    plan = _moves(
        [
            _scanned("a", energy, energy=8),
            _scanned("b", energy, energy=2),
            _scanned("c", style.id, energy=None, genre=named),
        ],
        {
            energy: {"a": (MED,), "b": (MED, LOW)},
            style.id: {"c": (style.subs[0].id,)},
        },
    )
    assert plan.counts() == {
        "moves": 3,
        "band": 2,
        "style": 1,
        "memberships_added": 2,
        "memberships_removed": 3,
        "left": {"total": 0, **{reason: 0 for reason in adopt_move.LEFT_REASONS}},
    }


def _one_move(**changed) -> adopt_move.MovePlan:
    bucket = _pure_energy_bucket().id
    plan = _moves([_scanned("t", bucket, energy=8)], {bucket: {"t": (MED,)}})
    (move,) = plan.moves
    fields = {name: getattr(move, name) for name in move.__slots__}
    fields.update(changed)
    return adopt_move.MovePlan(
        tree=plan.tree, placements=plan.placements, moves=(adopt_move.Move(**fields),)
    )


@pytest.mark.parametrize(
    "changed",
    [
        {"move_id": "mv_other"},
        {"content_id": "u"},
        {"location": "/library/Music/elsewhere.flac"},
        {"bucket": "another"},
        {"kind": "style"},
        {"target": LOW},
        {"add": ""},
        {"remove": (MED, LOW)},
        {"holds": (MED, LOW)},
        {"energy": 9},
        {"genre": "Another"},
    ],
    ids=lambda changed: next(iter(changed)),
)
def test_the_digest_covers_every_field_a_move_shows(changed):
    assert set(adopt_move.move_row(_one_move().moves[0])) - {"decided_by", "id"} == {
        name for name in adopt_move.Move.__slots__ if name != "move_id"
    }
    assert _one_move(**changed).digest() != _one_move().digest()


def test_the_digest_covers_the_tracks_left_and_the_tree():
    base = _one_move()
    bucket = _pure_energy_bucket().id
    left = adopt_move.Left(
        content_id="l", location="/l", bucket=bucket, kind="band",
        reason=adopt_move.LEFT_NO_READING, target=SINK, holds=(HIGH,),
        holds_unnamed=(), energy=None, genre="g",
    )
    with_left = adopt_move.MovePlan(
        tree=base.tree, placements=base.placements, moves=base.moves, left=(left,)
    )
    other_tree = adopt_move.MovePlan(tree="another", placements="read", moves=base.moves)
    assert len({base.digest(), with_left.digest(), other_tree.digest()}) == 3


def test_the_frozen_rows_read_back_to_the_moves_and_to_the_digest():
    bucket = _pure_energy_bucket().id
    plan = _moves(
        [_scanned("a", bucket, energy=8), _scanned("b", bucket, energy=None)],
        {bucket: {"a": (MED,), "b": (HIGH,)}},
    )
    document = adopt_move.to_json(plan)
    assert adopt_move.from_rows(document["moves"]) == plan.moves
    assert adopt_move.document_digest(document) == plan.digest() == document["digest"]
    tampered = {**document, "moves": [{**document["moves"][0], "remove": [LOW]}]}
    assert adopt_move.document_digest(tampered) != plan.digest()


def test_a_frozen_row_short_of_a_field_raises_rather_than_defaulting():
    row = adopt_move.move_row(_one_move().moves[0])
    for name in ("id", "content_id", "bucket", "target", "add", "remove", "holds", "energy"):
        short = {key: value for key, value in row.items() if key != name}
        with pytest.raises(KeyError):
            adopt_move.from_rows([short])


# ---------------------------------------------------------------------------
# R-780: the tree as it stands, in buckets adoption's entry does not claim
# ---------------------------------------------------------------------------


def _other_energy_bucket() -> taxonomy.Bucket:
    """A second bucket split by energy, whose display routes to itself."""
    first = _pure_energy_bucket().id
    return next(
        bucket
        for bucket in DECLARED.buckets
        if bucket.sub_by_source is None
        and bucket.energy.enabled
        and bucket.id != first
        and adopt_scan.classify_genre(DECLARED, bucket.display)[1] == bucket.id
    )


def _no_genre(content_id: str, *, energy: int | None) -> adopt_scan.ScannedTrack:
    """A track the census could not route: no genre, so no bucket of its own."""
    return adopt_scan.ScannedTrack(
        content_id=content_id,
        recorded=f"/library/Music/{content_id}.flac",
        path=f"/library/Music/{content_id}.flac",
        readability=adopt_scan.Readability.READABLE,
        disposition=adopt_scan.Disposition.NEEDS_GENRE,
        genre="",
        bucket="",
        energy=energy,
    )


def test_a_double_in_a_bucket_the_genre_does_not_name_moves_on_the_reading():
    """The shape read back off the author's library: the genre routes the
    track to one bucket and it sits in two bands of another."""
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    held = {here: {"t": (MED, HIGH)}, there: {"t": (HIGH,)}}
    adoption = _adoption([_scanned("t", there, energy=8)], held)
    # NOT ON ADOPTION'S LIST, which is the whole of R-780.
    assert adoption.held_elsewhere() == ()
    assert [entry.bucket for entry in adoption.entries] == [there]

    plan = adopt_move.build_move_plan(adoption, DECLARED)
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add) == (here, HIGH, "")
    assert (move.remove, move.holds) == ((MED,), tuple(sorted((MED, HIGH))))
    assert (move.kind, move.decided_by, move.energy) == ("band", "energy", 8)
    assert plan.left == ()
    assert plan.counts()["memberships_added"] == 0


def test_a_double_whose_reading_names_neither_is_left_where_the_genre_does_not_name_it():
    """Nothing is ADDED in a bucket the genre does not name. Which bucket a
    track belongs in is adoption's question, so the reading either picks one
    of the subs held or the track is left and listed."""
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    plan = _moves([_scanned("t", there, energy=1)], {here: {"t": (MED, HIGH)}})
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.bucket, left.reason, left.target) == (here, adopt_move.LEFT_NAMES_NEITHER, LOW)
    assert (left.holds, left.energy) == (tuple(sorted((MED, HIGH))), 1)
    assert plan.counts()["left"] == _left_counts(**{adopt_move.LEFT_NAMES_NEITHER: 1})


def test_a_track_with_no_genre_is_asked_in_every_bucket_it_doubles_in():
    """The other shape read back: a blank genre, so no entry bucket at all."""
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    plan = _moves([_no_genre("t", energy=2)], {here: {"t": (LOW, MED)}, there: {"t": (MED, HIGH)}})
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add, move.remove) == (here, LOW, "", (MED,))
    (left,) = plan.left
    assert (left.bucket, left.reason, left.target) == (there, adopt_move.LEFT_NAMES_NEITHER, LOW)


def test_in_the_same_bucket_the_genre_names_the_reading_still_adds():
    """R-758's rule in the entry's own bucket is untouched: a track in two
    bands whose reading names a third is moved to the third, because adoption
    itself would file it there."""
    bucket = _pure_energy_bucket().id
    plan = _moves([_scanned("t", bucket, energy=1)], {bucket: {"t": (MED, HIGH)}})
    (move,) = plan.moves
    assert (move.add, set(move.remove)) == (LOW, {MED, HIGH})
    assert plan.left == ()


def test_one_sub_in_a_bucket_the_genre_does_not_name_is_not_this_verbs():
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    plan = _moves([_scanned("t", there, energy=8)], {here: {"t": (MED,)}})
    assert plan.moves == () and plan.left == ()
    without_genre = _moves([_no_genre("t", energy=8)], {here: {"t": (MED,)}})
    assert without_genre.moves == () and without_genre.left == ()


def test_a_style_double_in_a_bucket_the_genre_does_not_name_is_out_of_scope():
    here, style = _pure_energy_bucket().id, _style_bucket()
    plan = _moves(
        [_scanned("t", here, energy=8)],
        {here: {"t": (HIGH,)}, style.id: {"t": (style.subs[0].id, style.subs[1].id)}},
    )
    assert plan.moves == () and plan.left == ()


def test_a_double_with_no_reading_in_a_bucket_the_genre_does_not_name_is_left():
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    plan = _moves([_scanned("t", there, energy=None)], {here: {"t": (MED, HIGH)}})
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.bucket, left.reason, left.target) == (here, adopt_move.LEFT_NO_READING, SINK)


def test_a_double_held_under_another_name_in_a_bucket_the_genre_does_not_name_is_left():
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    plan = _moves(
        [_scanned("t", there, energy=8)],
        {here: {"t": (MED, HIGH)}},
        unnamed={here: {"t": (MED,)}},
    )
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.reason, left.holds_unnamed) == (adopt_move.LEFT_UNNAMED, (MED,))


def _with_verdict_on(current: adopt_plan.AdoptionPlan, bucket: str) -> adopt_plan.AdoptionPlan:
    """The plan with a keep-separate verdict folded in for one bucket, the way
    ``with_collision_verdicts`` folds it: every routed entry of that bucket
    withheld under the verdict's reason."""
    from dataclasses import replace

    return replace(
        current,
        entries=tuple(
            replace(
                entry,
                disposition=adopt_scan.Disposition.WITHHELD,
                withheld_by=adopt_plan.WITHHELD_BY_VERDICT,
            )
            if entry.applicable and entry.bucket == bucket
            else entry
            for entry in current.entries
        ),
    )


def test_a_verdict_withheld_double_is_left_and_listed_under_its_own_reason():
    bucket = _pure_energy_bucket().id
    current = _adoption([_scanned("t", bucket, energy=8)], {bucket: {"t": (MED, HIGH)}})
    (move,) = adopt_move.build_move_plan(current, DECLARED).moves
    assert move.remove == (MED,)
    plan = adopt_move.build_move_plan(_with_verdict_on(current, bucket), DECLARED)
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.reason, left.bucket, left.holds) == (
        adopt_move.LEFT_VERDICT, bucket, tuple(sorted((MED, HIGH)))
    )


def test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder():
    """Found by the review. The first version honoured a verdict only on the
    entry's own bucket, and would have removed a membership inside a folder
    the person refused when the track sat there under another genre."""
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    tracks = [_scanned("t", there, energy=8), _scanned("u", here, energy=5)]
    held = {here: {"t": (MED, HIGH), "u": (MED,)}, there: {"t": (HIGH,)}}
    current = _adoption(tracks, held)
    assert [move.content_id for move in adopt_move.build_move_plan(current, DECLARED).moves] == ["t"]

    refused = _with_verdict_on(current, here)
    assert adopt_move.refused_buckets(refused.entries) == {here}
    plan = adopt_move.build_move_plan(refused, DECLARED)
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.content_id, left.bucket, left.reason) == ("t", here, adopt_move.LEFT_VERDICT)

    # And the worker refuses a move approved before the verdict landed.
    (approved,) = adopt_move.build_move_plan(current, DECLARED).moves
    with pytest.raises(Exception) as raised:
        move_cli.remaining([approved], refused, DECLARED)
    assert adopt_move.LEFT_VERDICT in raised.value.cause.detail["moved_under"]["t"]


def test_a_verdict_no_entry_routes_to_is_not_known_and_is_recorded_as_such():
    """The plan carries a verdict only as the entries it withheld, so a bucket
    no entry routes to reads as unrefused. Pinned so the gap is visible."""
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    current = _adoption([_scanned("t", there, energy=8)], {here: {"t": (MED, HIGH)}})
    assert adopt_move.refused_buckets(_with_verdict_on(current, here).entries) == frozenset()


def test_an_excluded_track_in_two_bands_is_listed_and_never_moved():
    """A file the census could not read has no reading, whatever its row says."""
    here = _pure_energy_bucket().id
    excluded = adopt_scan.ScannedTrack(
        content_id="t",
        recorded="/library/Music/t.flac",
        path=None,
        readability=adopt_scan.Readability.MISSING,
        disposition=adopt_scan.Disposition.EXCLUDED,
        genre=DECLARED.bucket(here).display,
        energy=8,
    )
    plan = _moves([excluded], {here: {"t": (MED, HIGH)}})
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.bucket, left.reason, left.holds) == (
        here, adopt_move.LEFT_NO_READING, tuple(sorted((MED, HIGH)))
    )
    single = _moves([excluded], {here: {"t": (MED,)}})
    assert single.moves == () and single.left == ()


def test_a_double_beside_a_track_left_for_another_reason_is_still_listed():
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    plan = _moves(
        [_scanned("t", there, energy=1)],
        {here: {"t": (MED, HIGH)}},
        doubled={here: {"t": (HIGH,)}},
    )
    assert plan.moves == ()
    assert [left.reason for left in plan.left] == [
        adopt_move.LEFT_NAMES_NEITHER, adopt_move.LEFT_DOUBLED_ROWS
    ]
    assert plan.counts()["left"]["total"] == 2


def test_one_track_carries_a_move_in_each_bucket_it_doubles_in():
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    tracks = [_scanned("t", there, energy=5)]
    current = _adoption(tracks, {here: {"t": (MED, HIGH)}, there: {"t": (LOW, MED)}})
    moves = adopt_move.build_move_plan(current, DECLARED).moves
    assert [(m.bucket, m.remove) for m in moves] == [(here, (HIGH,)), (there, (LOW,))]
    assert len({m.move_id for m in moves}) == 2

    # Gone once, though it carried two moves.
    without = _adoption([], {})
    todo, gone = move_cli.remaining(moves, without, DECLARED)
    assert (todo, gone) == ((), ("t",))


def test_a_target_held_only_under_another_name_is_not_done():
    """Found by the review. Dropping the routed check made a track whose one
    place is a renamed playlist read as finished; the refusal is restored on
    purpose rather than by accident."""
    bucket = _pure_energy_bucket().id
    tracks = [_scanned("t", bucket, energy=8)]
    start = _adoption(tracks, {bucket: {"t": (MED,)}})
    approved = adopt_move.build_move_plan(start, DECLARED).moves
    renamed = _adoption(tracks, {bucket: {"t": (HIGH,)}}, unnamed={bucket: {"t": (HIGH,)}})
    with pytest.raises(Exception) as raised:
        move_cli.remaining(approved, renamed, DECLARED)
    assert "another name" in raised.value.cause.detail["moved_under"]["t"]
    done = _adoption(tracks, {bucket: {"t": (HIGH,)}})
    assert move_cli.remaining(approved, done, DECLARED) == ((), ())


@pytest.mark.parametrize("routes_here", [True, False], ids=["genre-names-it", "genre-elsewhere"])
def test_a_sub_held_by_two_rows_is_listed_and_not_moved(routes_here):
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    genre_bucket = here if routes_here else there
    plan = _moves(
        [_scanned("t", genre_bucket, energy=2)],
        {here: {"t": (LOW,)}},
        doubled={here: {"t": (LOW,)}},
    )
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.bucket, left.reason, left.holds, left.target) == (
        here, adopt_move.LEFT_DOUBLED_ROWS, (LOW,), LOW
    )
    assert plan.counts()["left"] == _left_counts(**{adopt_move.LEFT_DOUBLED_ROWS: 1})


def test_a_doubled_target_beside_a_stale_sub_is_a_move_and_the_double_is_listed_after():
    bucket = _pure_energy_bucket().id
    plan = _moves(
        [_scanned("t", bucket, energy=2)],
        {bucket: {"t": (LOW, MED)}},
        doubled={bucket: {"t": (LOW,)}},
    )
    (move,) = plan.moves
    assert (move.add, move.remove) == ("", (MED,))
    assert plan.left == ()
    after = _moves(
        [_scanned("t", bucket, energy=2)], {bucket: {"t": (LOW,)}}, doubled={bucket: {"t": (LOW,)}}
    )
    assert after.moves == () and [left.reason for left in after.left] == [
        adopt_move.LEFT_DOUBLED_ROWS
    ]


def test_a_doubled_row_in_a_sub_class_is_not_listed():
    bucket = _pure_energy_bucket().id
    plan = _moves(
        [_scanned("t", bucket, energy=5)],
        {bucket: {"t": (MED, DERIVED)}},
        doubled={bucket: {"t": (DERIVED,)}},
    )
    assert plan.moves == () and plan.left == ()


def test_the_digest_moves_when_a_double_appears_in_a_bucket_the_genre_does_not_name():
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    tracks = [_scanned("t", there, energy=8)]
    alone = _moves(tracks, {there: {"t": (HIGH,)}})
    doubled = _moves(tracks, {there: {"t": (HIGH,)}, here: {"t": (MED, HIGH)}})
    left = _moves([_scanned("t", there, energy=1)], {there: {"t": (LOW,)}, here: {"t": (MED, HIGH)}})
    assert len({alone.digest(), doubled.digest(), left.digest()}) == 3


def test_the_reading_is_asked_of_the_one_resolver_in_either_bucket():
    """No second rule for what a level means: in the bucket the genre names
    the target is adoption's sub, elsewhere it is the same resolver's answer."""
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    (entry,) = _adoption([_scanned("t", there, energy=8)], {}).entries
    assert adopt_move.reading_target(entry, there, DECLARED) == entry.sub == HIGH
    assert adopt_move.reading_target(entry, here, DECLARED) == routing.energy_sub(
        DECLARED, here, 8
    ).id
    assert adopt_move.reading_target(entry, "no-such-bucket", DECLARED) == ""
    (blank,) = _adoption([_no_genre("t", energy=None)], {}).entries
    assert adopt_move.reading_target(blank, here, DECLARED) == SINK


def test_a_tree_path_move_is_checked_by_the_worker_in_the_bucket_it_names():
    """The worker asked adoption's bucket and sub of every approved row, so a
    move in a bucket the genre does not name would have been refused as
    naming another place."""
    here, there = _pure_energy_bucket().id, _other_energy_bucket().id
    tracks = [_scanned("t", there, energy=8)]
    start = _adoption(tracks, {here: {"t": (MED, HIGH)}, there: {"t": (HIGH,)}})
    approved = adopt_move.build_move_plan(start, DECLARED).moves
    assert [move.bucket for move in approved] == [here]

    todo, gone = move_cli.remaining(approved, start, DECLARED)
    assert (todo, gone) == (approved, ())

    done = _adoption(tracks, {here: {"t": (HIGH,)}, there: {"t": (HIGH,)}})
    assert move_cli.remaining(approved, done, DECLARED) == ((), ())

    reading_moved = _adoption([_scanned("t", there, energy=2)], {here: {"t": (MED, HIGH)}})
    with pytest.raises(Exception) as raised:
        move_cli.remaining(approved, reading_moved, DECLARED)
    assert raised.value.cause.reason == "decision-stale"
    assert "another place" in raised.value.cause.detail["moved_under"]["t"]

    genre_now_here = _adoption([_scanned("t", here, energy=1)], {here: {"t": (MED, HIGH)}})
    with pytest.raises(Exception) as raised:
        move_cli.remaining(approved, genre_now_here, DECLARED)
    assert raised.value.cause.reason == "decision-stale"

    left_bucket = _adoption(tracks, {there: {"t": (HIGH,)}})
    with pytest.raises(Exception) as raised:
        move_cli.remaining(approved, left_bucket, DECLARED)
    assert "holds no sub" in raised.value.cause.detail["moved_under"]["t"]


# ---------------------------------------------------------------------------
# A placed library with real tags
# ---------------------------------------------------------------------------

#: One library, as data: a track, the energy its file carries, the subs it sits in.
_SEEDED = (
    ("m-med-reads-high", "8", (MED,)),
    ("m-both-reads-high", "8", (MED, HIGH)),
    ("m-vox-and-med", "8", (DERIVED, MED)),
    ("m-candy-only", "2", (MANUAL,)),
    ("m-no-reading", None, (HIGH,)),
    ("m-same", "5", (MED,)),
    ("m-sink-now-reads", "5", (SINK,)),
)

#: R-780's shapes, none of them on adoption's list: a track whose genre routes
#: to ANOTHER energy bucket, or to none, sitting in two bands of the first.
#: Row: track, energy tag, where its genre routes ("other", "none"), the subs
#: it holds in the first bucket, the subs it holds in the other bucket.
_SEEDED_ELSEWHERE = (
    ("m-genre-elsewhere-reads-high", "8", "other", (MED, HIGH), (HIGH,)),
    ("m-genre-elsewhere-reads-low", "1", "other", (MED, HIGH), ()),
    ("m-no-genre", "2", "none", (LOW, MED), ()),
    # Two moves for one track: a double in each bucket, the reading naming Med.
    ("m-two-buckets", "5", "other", (MED, HIGH), (LOW, MED)),
)

#: One pair held by two active rows (R-781), reading naming that very sub.
_TWICE = "m-twice"

_MOVED = {
    "m-med-reads-high",
    "m-both-reads-high",
    "m-vox-and-med",
    "m-sink-now-reads",
    "m-style",
    "m-genre-elsewhere-reads-high",
    "m-no-genre",
    "m-two-buckets",
}
_LEFT = {"m-no-reading", "m-genre-elsewhere-reads-low", _TWICE}
#: The moves the plan holds: one per track, and two for the track that doubles
#: in both buckets.
_MOVE_ROWS = len(_MOVED) + 1
#: Of the moves, the ones adoption's own plan withholds over a held place.
_WITHHELD_BY_ADOPTION = {"m-med-reads-high", "m-vox-and-med", "m-sink-now-reads", "m-style"}


def _other_bucket() -> taxonomy.Bucket:
    """A second energy bucket the fixture's other genre routes to."""
    first = _energy_bucket().id
    return next(
        bucket
        for bucket in DECLARED.buckets
        if bucket.sub_by_source is None
        and bucket.energy.enabled
        and bucket.id != first
        and adopt_scan.classify_genre(DECLARED, bucket.display)[1] == bucket.id
    )


@pytest.fixture
def moved(machine, silence):  # noqa: F811
    """A cut over library whose tree files tracks where their files do not read."""
    from cratekit.core import tags

    energy, style, other = _energy_bucket(), _style_bucket(), _other_bucket()
    first, second = style.subs[0], style.subs[1]
    style_genre = next(g for g, sub in style.sub_by_source.map.items() if sub == second.id)
    tracks = [
        adopt_fixtures.Track(content_id, f"{content_id}.flac", energy.display)
        for content_id, _tag, _held in _SEEDED
    ]
    tracks.append(adopt_fixtures.Track("m-style", "m-style.flac", style_genre))
    for content_id, _tag, routes, _held, _elsewhere in _SEEDED_ELSEWHERE:
        genre = other.display if routes == "other" else ""
        tracks.append(adopt_fixtures.Track(content_id, f"{content_id}.flac", genre))
    tracks.append(adopt_fixtures.Track(_TWICE, f"{_TWICE}.flac", energy.display))
    adopt_fixtures.build(machine, tuple(tracks))
    collection.reset_cache()

    music = Path(machine.library.root) / "Music"
    readings = {content_id: tag for content_id, tag, _held in _SEEDED}
    readings["m-style"] = "8"
    readings.update({row[0]: row[1] for row in _SEEDED_ELSEWHERE})
    readings[_TWICE] = "5"
    for content_id, tag in readings.items():
        path = music / f"{content_id}.flac"
        shutil.copyfile(silence, path)
        if tag is not None:
            assert tags.write_tags(path, {"energylevel": tag}) is True

    seeded = [
        (energy.id, sub, content_id) for content_id, _tag, held in _SEEDED for sub in held
    ]
    seeded.append((style.id, first.id, "m-style"))
    for content_id, _tag, _routes, held, elsewhere in _SEEDED_ELSEWHERE:
        seeded.extend((energy.id, sub, content_id) for sub in held)
        seeded.extend((other.id, sub, content_id) for sub in elsewhere)
    seeded.append((energy.id, MED, _TWICE))
    handle = rb_writer.open_db(rb_writer.live_db_path(machine), unlock=False, cfg=machine)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        for bucket_id, sub_id, content_id in seeded:
            folder_display, sub_display = destination(DECLARED, bucket_id, sub_id)
            folder = rb_writer.ensure_folder(handle, folder_display, parent=root)
            playlist = rb_writer.ensure_playlist(handle, sub_display, folder)
            rb_writer.add_memberships(handle, playlist, [content_id])
        handle.session.commit()
        root_id = str(root.ID)
    finally:
        rb_writer.close_db(handle)
    # THE SECOND ROW OF ONE PAIR, as rekordbox made them (R-781). The additive
    # writer will not write a pair twice, so it is inserted as a row.
    conn = sqlite3.connect(Path(machine.library.db_path))
    try:
        conn.execute(
            "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, "
            "rb_local_deleted, created_at, updated_at) "
            "SELECT 'twice', PlaylistID, ContentID, 99, 0, created_at, updated_at "
            "FROM djmdSongPlaylist WHERE ContentID = ?",
            (_TWICE,),
        )
        conn.commit()
    finally:
        conn.close()
    tree_registry.record_cutover(
        machine,
        TREE_ID,
        root_id=root_id,
        on=date(2026, 9, 29),
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    return machine


def _rows(cfg) -> list[tuple[str, str, str, int]]:
    """Every membership row: track, folder name, playlist name, removal marker.

    Read with plain SQL off the file, so what is asserted is what the database
    holds and the marker is read whatever a reader in the product does with it.
    """
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        return [
            (str(a), str(b), str(c), int(d))
            for a, b, c, d in conn.execute(
                "SELECT sp.ContentID, f.Name, p.Name, sp.rb_local_deleted "
                "FROM djmdSongPlaylist sp "
                "JOIN djmdPlaylist p ON p.ID = sp.PlaylistID "
                "JOIN djmdPlaylist f ON f.ID = p.ParentID "
                "ORDER BY sp.ContentID, f.Name, p.Name, sp.rb_local_deleted"
            )
        ]
    finally:
        conn.close()


def _live(cfg) -> dict[str, set[tuple[str, str]]]:
    found: dict[str, set[tuple[str, str]]] = {}
    for content_id, folder, playlist, marker in _rows(cfg):
        if not marker:
            found.setdefault(content_id, set()).add((folder, playlist))
    return found


def _removed(cfg) -> dict[str, set[tuple[str, str]]]:
    found: dict[str, set[tuple[str, str]]] = {}
    for content_id, folder, playlist, marker in _rows(cfg):
        if marker:
            found.setdefault(content_id, set()).add((folder, playlist))
    return found


def _place(sub_id: str, bucket: taxonomy.Bucket | None = None) -> tuple[str, str]:
    return destination(DECLARED, (bucket or _energy_bucket()).id, sub_id)


def _shown(verb: list[str]) -> dict:
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    return refused["cause"]["detail"]["shown"]


def _approve_and_run() -> tuple[str, int, dict]:
    _run_id, job_id = approve_and_queue(VERB, GATE)
    code, resumed = drive(_resume(job_id))
    return job_id, code, resumed


# ── the gate ────────────────────────────────────────────────────────────────


def test_the_gate_shows_every_move_with_what_it_adds_removes_and_reads(moved):
    shown = _shown(VERB)
    style = _style_bucket()

    items = {item["content_id"]: item for item in shown["items"]}
    assert set(items) == _MOVED
    assert len(shown["items"]) == _MOVE_ROWS == 9
    assert shown["counts"] == {
        "moves": 9,
        "band": 8,
        "style": 1,
        "memberships_added": 4,
        "memberships_removed": 9,
        "left": _left_counts(
            **{
                adopt_move.LEFT_NO_READING: 1,
                adopt_move.LEFT_NAMES_NEITHER: 1,
                adopt_move.LEFT_DOUBLED_ROWS: 1,
            }
        ),
    }
    assert shown["placements"] == "read"

    row = items["m-med-reads-high"]
    assert (row["add"], row["remove"], row["holds"]) == (HIGH, [MED], [MED])
    assert (row["decided_by"], row["energy"], row["bucket"]) == ("energy", 8, _energy_bucket().id)
    assert row["location"].endswith("m-med-reads-high.flac")
    assert (items["m-both-reads-high"]["add"], items["m-both-reads-high"]["remove"]) == ("", [MED])
    assert (items["m-vox-and-med"]["holds"], items["m-vox-and-med"]["remove"]) == ([MED], [MED])
    assert (items["m-sink-now-reads"]["add"], items["m-sink-now-reads"]["remove"]) == (MED, [SINK])
    assert (items["m-style"]["decided_by"], items["m-style"]["kind"]) == ("genre", "style")
    assert items["m-style"]["remove"] == [style.subs[0].id]
    assert items["m-style"]["add"] == style.subs[1].id
    # R-780: the two shapes off the author's library, shown like every other row.
    elsewhere = items["m-genre-elsewhere-reads-high"]
    assert (elsewhere["bucket"], elsewhere["add"], elsewhere["remove"]) == (
        _energy_bucket().id, "", [MED]
    )
    assert (elsewhere["holds"], elsewhere["energy"], elsewhere["genre"]) == (
        sorted((MED, HIGH)), 8, _other_bucket().display
    )
    no_genre = items["m-no-genre"]
    assert (no_genre["bucket"], no_genre["add"], no_genre["remove"], no_genre["genre"]) == (
        _energy_bucket().id, "", [MED], ""
    )
    two = sorted(
        (row["bucket"], row["remove"]) for row in shown["items"] if row["content_id"] == "m-two-buckets"
    )
    assert two == sorted([(_energy_bucket().id, [HIGH]), (_other_bucket().id, [LOW])])

    left = {row["content_id"]: row for row in shown["left"]}
    assert set(left) == _LEFT
    assert left["m-no-reading"]["reason"] == adopt_move.LEFT_NO_READING
    neither = left["m-genre-elsewhere-reads-low"]
    assert (neither["reason"], neither["bucket"], neither["target"], neither["holds"]) == (
        adopt_move.LEFT_NAMES_NEITHER, _energy_bucket().id, LOW, sorted((MED, HIGH))
    )
    assert (left[_TWICE]["reason"], left[_TWICE]["holds"], left[_TWICE]["target"]) == (
        adopt_move.LEFT_DOUBLED_ROWS, [MED], MED
    )
    assert shown["digest"] == move_cli.current_plan(moved, DECLARED).digest()


def test_a_person_reading_the_gate_is_shown_every_move_and_every_track_left(moved):
    _code, text = drive_human(VERB)
    for content_id in _MOVED | _LEFT:
        assert f"content_id={content_id}" in text, content_id


def test_the_gate_takes_no_inline_answer(moved):
    before = _rows(moved)
    code, refused = drive(["-d", f"{GATE}=approve", *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()
    assert _rows(moved) == before


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(moved):
    session.ack_path(moved).unlink()
    before = _rows(moved)

    code, refused = drive(VERB)

    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert refused["cause"]["reason"] == "backup-acknowledgment-missing"
    assert "shown" not in refused["cause"].get("detail", {})
    assert refused["cause"]["remediation"]["remedy"] == str(Remedy.ACKNOWLEDGE_BACKUP)
    assert _rows(moved) == before


def test_an_acknowledgment_out_of_its_window_refuses_before_the_gate(moved, monkeypatch):
    monkeypatch.setattr(session.Acknowledgment, "valid_at", lambda self, moment: False)
    code, refused = drive(VERB)
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert refused["cause"]["detail"]["expired"] is True


def test_a_resume_with_no_acknowledgment_refuses_before_anything_is_driven(moved):
    _run_id, job_id = approve_and_queue(VERB, GATE)
    session.ack_path(moved).unlink()
    before = _rows(moved)
    code, refused = drive(_resume(job_id))
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert _rows(moved) == before


# ── the move ────────────────────────────────────────────────────────────────


def test_an_approved_move_adds_the_new_sub_and_removes_the_old(moved):
    before = _live(moved)
    job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    after, removed = _live(moved), _removed(moved)
    style = _style_bucket()

    # In High and not in Med.
    assert after["m-med-reads-high"] == {_place(HIGH)}
    # In Med and High: Med removed, nothing added.
    assert after["m-both-reads-high"] == {_place(HIGH)}
    # The vocal sub is untouched.
    assert after["m-vox-and-med"] == {_place(DERIVED), _place(HIGH)}
    assert after["m-sink-now-reads"] == {_place(MED)}
    assert after["m-style"] == {_place(style.subs[1].id, style)}
    # R-780: the stale band goes in the bucket the genre does not name, and
    # the place the genre does name is not touched.
    assert after["m-genre-elsewhere-reads-high"] == {_place(HIGH), _place(HIGH, _other_bucket())}
    assert after["m-no-genre"] == {_place(LOW)}
    # Two moves on one track, one in each bucket.
    assert after["m-two-buckets"] == {_place(MED), _place(MED, _other_bucket())}
    # Not planned, and left where they are.
    for content_id in (
        "m-candy-only", "m-no-reading", "m-same", "m-genre-elsewhere-reads-low", _TWICE
    ):
        assert after[content_id] == before[content_id], content_id
        assert content_id not in removed, content_id
    # Both rows of the doubled pair are still live.
    assert len([row for row in _rows(moved) if row[0] == _TWICE and not row[3]]) == 2

    report = artifacts.committed(moved, job_id)[-1]
    assert (report["added"], report["already_present"]) == (4, 5)
    assert (report["removed"], report["already_absent"]) == (9, 0)
    # ONCE PER TRACK, though one of them carried two moves.
    assert sorted(report["moved"]) == sorted(_MOVED)
    assert report["in_both"] == report["untouched"] == report["neither"] == []
    assert report["interrupted"] is False
    assert resumed["data"]["progress"]["move"]["moved"] == sorted(_MOVED)


def test_the_removal_is_a_soft_delete_and_the_row_is_still_there(moved):
    rows_before = len(_rows(moved))
    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed

    assert _removed(moved) == {
        "m-med-reads-high": {_place(MED)},
        "m-both-reads-high": {_place(MED)},
        "m-vox-and-med": {_place(MED)},
        "m-sink-now-reads": {_place(SINK)},
        "m-style": {_place(_style_bucket().subs[0].id, _style_bucket())},
        "m-genre-elsewhere-reads-high": {_place(MED)},
        "m-no-genre": {_place(MED)},
        "m-two-buckets": {_place(HIGH), _place(LOW, _other_bucket())},
    }
    # Nine rows marked, four rows added, none deleted.
    assert len(_rows(moved)) == rows_before + 4


def test_a_removed_row_changes_its_marker_and_its_stamp_and_nothing_else(moved):
    """As rekordbox's own removed rows read: the marker set, ``updated_at``
    moved past ``created_at``, the local update sequence stamped, and the
    track number where it was."""
    columns = "ID, PlaylistID, ContentID, TrackNo, UUID, rb_data_status, created_at"

    def rows(extra: str):
        conn = sqlite3.connect(Path(moved.library.db_path))
        try:
            return conn.execute(
                f"SELECT {columns}, {extra} FROM djmdSongPlaylist "
                "WHERE ContentID = 'm-med-reads-high' ORDER BY created_at, ID"
            ).fetchall()
        finally:
            conn.close()

    (before,) = rows("rb_local_deleted, updated_at, rb_local_usn")
    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    after = [row for row in rows("rb_local_deleted, updated_at, rb_local_usn") if row[0] == before[0]]
    (after,) = after

    assert after[:7] == before[:7]
    assert (before[7], after[7]) == (0, 1)
    assert after[8] != before[8] and str(after[8]) > str(before[6])
    assert after[9] is not None and after[9] != before[9]


def test_no_content_row_and_no_grid_column_is_written(moved):
    def content():
        conn = sqlite3.connect(Path(moved.library.db_path))
        try:
            return conn.execute("SELECT * FROM djmdContent ORDER BY ID").fetchall()
        finally:
            conn.close()

    before = content()
    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    assert content() == before


#: The columns and tables a move must never touch, named one by one so a
#: difference is reported against the column and not against a whole row.
_GUARDED_CONTENT_COLUMNS = (
    "BPM", "Rating", "KeyID", "Analysed", "AnalysisDataPath", "AnalysisUpdated", "CueUpdated"
)
_GUARDED_TABLES = ("djmdCue", "contentCue", "hotCueBanklistCue")


def test_no_tempo_grid_cue_or_rating_value_differs_column_by_column(moved):
    """R-780's brief asks for it by column. A whole row comparison would say
    only that something differed; this says which column, on which track."""

    def read(sql: str):
        conn = sqlite3.connect(Path(moved.library.db_path))
        try:
            return conn.execute(sql).fetchall()
        finally:
            conn.close()

    tables = {row[0] for row in read("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert set(_GUARDED_TABLES) <= tables, sorted(tables)
    columns = {
        name: read(f"SELECT ID, {name} FROM djmdContent ORDER BY ID")
        for name in _GUARDED_CONTENT_COLUMNS
    }
    cues = {name: read(f"SELECT * FROM {name} ORDER BY ID") for name in _GUARDED_TABLES}
    assert all(columns.values()), "the fixture holds rows to compare"

    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed

    for name, before in columns.items():
        assert read(f"SELECT ID, {name} FROM djmdContent ORDER BY ID") == before, name
    for name, before in cues.items():
        assert read(f"SELECT * FROM {name} ORDER BY ID") == before, name


def test_after_the_move_adoption_withholds_none_of_the_moved_tracks(moved):
    withheld = {e.content_id for e in apply_cli.current_plan(moved, DECLARED).held_elsewhere()}
    assert withheld == _WITHHELD_BY_ADOPTION | {"m-no-reading"}
    # R-780: the ones the tree path moves were never on adoption's list.
    assert {"m-genre-elsewhere-reads-high", "m-no-genre", "m-two-buckets"}.isdisjoint(withheld)

    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    collection.reset_cache()

    plan = apply_cli.current_plan(moved, DECLARED)
    assert {e.content_id for e in plan.held_elsewhere()} == {"m-no-reading"}
    applicable = {entry.content_id for entry in plan.applicable()}
    assert _MOVED - {"m-no-genre"} <= applicable
    # A track with no genre is adoption's open question, not a placed track.
    assert "m-no-genre" not in applicable


def test_a_second_approved_run_plans_nothing_and_writes_nothing(moved):
    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    rows = _rows(moved)
    collection.reset_cache()

    shown = _shown(VERB)
    assert shown["items"] == []
    assert shown["counts"]["moves"] == 0
    assert {row["content_id"] for row in shown["left"]} == _LEFT

    code, refused = drive(VERB)
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, GATE, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    code, envelope = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "no-op"
    assert [w["code"] for w in envelope["warnings"]] == [move_cli.NOTHING_TO_MOVE]
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 1
    assert _rows(moved) == rows


def test_a_declined_gate_queues_nothing(moved):
    before = _rows(moved)
    code, refused = drive(VERB)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, envelope = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "declined"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()
    assert _rows(moved) == before


def test_a_moved_track_can_be_moved_back_and_gets_a_live_row(moved):
    """A removed membership is not counted as present, so the track returns."""
    from cratekit.core import tags

    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    music = Path(moved.library.root) / "Music"
    assert tags.write_tags(music / "m-med-reads-high.flac", {"energylevel": "5"}) is True
    collection.reset_cache()

    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    assert _live(moved)["m-med-reads-high"] == {_place(MED)}
    assert _removed(moved)["m-med-reads-high"] == {_place(MED), _place(HIGH)}


# ── a failure between the add and the remove ───────────────────────────────


def test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes(
    moved, monkeypatch
):
    before = _live(moved)
    _run_id, job_id = approve_and_queue(VERB, GATE)

    def fails(*_args, **_kwargs):
        raise RuntimeError("the disk went away")

    with monkeypatch.context() as patched:
        patched.setattr(rb_writer, "remove_memberships", fails)
        code, failed = drive(_resume(job_id))

    assert code != int(ExitCode.OK), failed
    after = _live(moved)
    # IN BOTH, and never in neither.
    assert after["m-med-reads-high"] == {_place(MED), _place(HIGH)}
    assert after["m-sink-now-reads"] == {_place(SINK), _place(MED)}
    for content_id, places in before.items():
        assert places <= after[content_id], content_id
    assert _removed(moved) == {}

    # THE JOB SAYS SO, once per track.
    report = artifacts.committed(moved, job_id)[-1]
    assert sorted(report["in_both"]) == sorted(_MOVED)
    assert report["moved"] == [] and report["neither"] == []
    assert (report["interrupted"], report["added"], report["removed"]) == (True, 4, 0)
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    assert job.state is jobs.JobState.FAILED
    assert job.cause is not None and job.cause.retryable is True
    assert "adopt-entries-failed" in str(job.cause.to_json())
    assert "m-med-reads-high" in str(job.cause.to_json())

    # AND A RESUME FINISHES IT.
    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    collection.reset_cache()
    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed
    finished = _live(moved)
    assert finished["m-med-reads-high"] == {_place(HIGH)}
    assert finished["m-both-reads-high"] == {_place(HIGH)}
    assert finished["m-vox-and-med"] == {_place(DERIVED), _place(HIGH)}
    assert finished["m-sink-now-reads"] == {_place(MED)}
    assert finished["m-genre-elsewhere-reads-high"] == {_place(HIGH), _place(HIGH, _other_bucket())}
    assert finished["m-no-genre"] == {_place(LOW)}
    assert finished["m-two-buckets"] == {_place(MED), _place(MED, _other_bucket())}
    report = artifacts.committed(moved, job_id)[-1]
    assert set(report["moved"]) == _MOVED and report["in_both"] == []
    assert (report["added"], report["already_present"], report["removed"]) == (0, 9, 9)
    assert resumed["data"]["progress"]["move"]["moved"] == sorted(_MOVED)


def test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised(
    moved, monkeypatch
):
    """The read back is the verdict. A writer that reports no failure over
    tracks still in both subs must not drive the job to succeeded."""
    _run_id, job_id = approve_and_queue(VERB, GATE)
    monkeypatch.setattr(rb_writer, "remove_memberships", lambda *_args, **_kwargs: [])

    code, failed = drive(_resume(job_id))

    assert code != int(ExitCode.OK), failed
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        (item,) = jobs.items(store, job_id)
    assert job.state is jobs.JobState.FAILED
    assert item.cause.reason == "adopt-entries-failed" and item.cause.retryable is True
    assert set(item.cause.detail["in_both"]) == _MOVED
    report = artifacts.committed(moved, job_id)[-1]
    assert (report["interrupted"], report["removed"], report["already_absent"]) == (False, 0, 9)


def test_a_failure_in_the_additions_writes_nothing_at_all(moved, monkeypatch):
    before = _rows(moved)
    _run_id, job_id = approve_and_queue(VERB, GATE)

    def fails(*_args, **_kwargs):
        raise RuntimeError("the disk went away")

    monkeypatch.setattr(rb_writer, "add_memberships", fails)
    code, failed = drive(_resume(job_id))
    assert code != int(ExitCode.OK), failed
    assert _rows(moved) == before


# ── what the review found, driven ──────────────────────────────────────────


def _mark_playlist_removed(cfg, sub_id: str) -> None:
    """Mark the first energy bucket's playlist for ``sub_id`` removed.

    BY FOLDER AS WELL AS BY NAME, since the other bucket's band of the same
    name is a different playlist and is left live."""
    folder, playlist = _place(sub_id)
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        changed = conn.execute(
            "UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE Name = ? AND Attribute = 0 "
            "AND ParentID IN (SELECT ID FROM djmdPlaylist WHERE Name = ?)",
            (playlist, folder),
        ).rowcount
        conn.commit()
    finally:
        conn.close()
    assert changed == 1


def test_an_addition_never_lands_in_a_playlist_rekordbox_removed(moved):
    """The additive find or create reads no marker and hands back a removed
    namesake. The move resolves among live nodes and makes a live one."""
    _mark_playlist_removed(moved, HIGH)
    shown = _shown(VERB)
    items = {item["content_id"]: item for item in shown["items"]}
    # Held only through the removed playlist, so High is not a place it holds.
    assert (items["m-both-reads-high"]["holds"], items["m-both-reads-high"]["add"]) == (
        [MED],
        HIGH,
    )
    assert "m-no-reading" not in {row["content_id"] for row in shown["left"]}

    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed

    conn = sqlite3.connect(Path(moved.library.db_path))
    try:
        found = conn.execute(
            "SELECT p.rb_local_deleted, COUNT(*) FROM djmdSongPlaylist sp "
            "JOIN djmdPlaylist p ON p.ID = sp.PlaylistID "
            "WHERE p.Name = ? AND sp.rb_local_deleted = 0 AND sp.ContentID IN (?, ?, ?) "
            "GROUP BY p.rb_local_deleted ORDER BY p.rb_local_deleted",
            (_place(HIGH)[1], "m-med-reads-high", "m-both-reads-high", "m-vox-and-med"),
        ).fetchall()
    finally:
        conn.close()
    # Three additions in the live playlist. The one row in the removed playlist
    # is the row the fixture seeded there, which nothing here touches.
    assert found == [(0, 3), (1, 1)]


def test_a_sub_held_only_through_a_removed_playlist_is_not_planned_for_removal(moved):
    _mark_playlist_removed(moved, MED)
    shown = _shown(VERB)
    # The first bucket's Med is not a place, so every double through it is
    # gone. The other bucket's Med is live, so m-two-buckets keeps its move there.
    assert {item["content_id"] for item in shown["items"]} == {
        "m-sink-now-reads", "m-style", "m-two-buckets"
    }
    assert [row["bucket"] for row in shown["items"] if row["content_id"] == "m-two-buckets"] == [
        _other_bucket().id
    ]
    before = [row for row in _rows(moved) if row[2] == _place(MED)[1]]
    _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    assert all(not row[3] for row in before)
    unmarked = [row for row in _rows(moved) if row[2] == _place(MED)[1] and not row[3]]
    assert set(before) <= set(unmarked)


def test_a_person_stopping_the_removals_is_an_interrupt_and_not_a_failure(
    moved, monkeypatch
):
    def stopped(*_args, **_kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(rb_writer, "remove_memberships", stopped)
    with pytest.raises(KeyboardInterrupt):
        _write(moved, [trees.MembershipMove("m-med-reads-high", _place(HIGH), (_place(MED),))])
    assert _live(moved)["m-med-reads-high"] == {_place(MED), _place(HIGH)}
    assert _removed(moved) == {}


def test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both(
    moved, monkeypatch
):
    _run_id, job_id = approve_and_queue(VERB, GATE)

    def opened(_what):
        raise rb_writer._running("rekordbox was opened while this ran")

    with monkeypatch.context() as patched:
        # The guarded commit asks whether rekordbox is closed. The additions'
        # commit is let through and the removals' is refused.
        patched.setattr(rb_writer, "assert_rekordbox_closed", _after_first(opened))
        code, failed = drive(_resume(job_id))

    assert code != int(ExitCode.OK), failed
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        (item,) = jobs.items(store, job_id)
    # THE ITEM FAILED ON THE REFUSAL ITSELF, with its own slug and remedy, and
    # not on this verb's account of an unfinished move.
    assert item.cause.reason == "rekordbox-running", item.cause
    assert "adopt-entries-failed" not in str(job.cause.to_json())
    assert "rekordbox-running" in str(job.cause.to_json())
    assert _live(moved)["m-med-reads-high"] == {_place(MED), _place(HIGH)}
    assert _removed(moved) == {}
    report = artifacts.committed(moved, job_id)[-1]
    assert set(report["in_both"]) == _MOVED and report["interrupted"] is True


def _after_first(refusal):
    """A stand in for the closed check that passes until a commit has landed."""
    seen = {"commits": 0}

    def check(what):
        if what != "committing":
            return None
        seen["commits"] += 1
        if seen["commits"] > 1:
            refusal(what)
        return None

    return check


def test_the_fingerprint_is_taken_after_each_commit_that_landed(moved, monkeypatch):
    from cratekit.core import convergence

    taken: list[int] = []
    real = convergence.record_fingerprint

    def counting(cfg, db, **kwargs):
        taken.append(1)
        return real(cfg, db, **kwargs)

    monkeypatch.setattr(convergence, "record_fingerprint", counting)

    def fails(*_args, **_kwargs):
        raise RuntimeError("the disk went away")

    with monkeypatch.context() as patched:
        patched.setattr(rb_writer, "remove_memberships", fails)
        with pytest.raises(trees.MoveInterrupted) as raised:
            _write(
                moved,
                [trees.MembershipMove("m-med-reads-high", _place(HIGH), (_place(MED),))],
            )
    assert (raised.value.report.added, raised.value.report.adds_committed) == (1, True)
    assert isinstance(raised.value.__cause__, RuntimeError)
    assert len(taken) == 1, "the additions landed and the reading was not moved"

    _write(moved, [trees.MembershipMove("m-med-reads-high", _place(HIGH), (_place(MED),))])
    # Nothing to add the second time, so one more reading, for the removal.
    assert len(taken) == 2


def test_a_membership_that_cannot_say_is_unproven_and_is_refused_by_a_reader(moved):
    from cratekit.write import rebuild, routing_pass

    class Song:
        ID = "s"
        ContentID = "c"
        PlaylistID = "p"
        rb_local_deleted = None

    class Node:
        def __init__(self, name, parent):
            self.ID, self.Name, self.ParentID = name, name, parent
            self.rb_local_deleted = 0

    class Db:
        def get_playlist_songs(self, **_kwargs):
            return [Song()]

        def get_playlist(self, **kwargs):
            if "ParentID" in kwargs:
                return [Node("child", kwargs["ParentID"])]
            return {"p": Node("Sub", "f"), "f": Node("Folder", "root")}.get(kwargs["ID"])

    placed = routing_pass.Placed.__new__(routing_pass.Placed)
    for name, value in (("content_id", "c"), ("sub", "Sub"), ("folder", "Folder")):
        object.__setattr__(placed, name, value)
    assert routing_pass.membership_proven(Db(), placed, root_id="root") is False
    with pytest.raises(Exception) as raised:
        rebuild.read_tree(Db(), "root")
    assert raised.value.cause.reason == "soft-delete-marker-unreadable"


def test_a_job_another_verb_queued_is_never_driven_through_this_gate(moved):
    _run_id, job_id = approve_and_queue(VERB, GATE)
    with jobs.open_store() as store:
        mine = jobs.get(store, job_id)
        other = jobs.enqueue(
            store,
            handler_key="adopt.apply",
            payload=dict(mine.payload),
            item_ids=("one",),
            cfg=moved,
        )
    before = _rows(moved)
    code, envelope = drive(["adopt", "move", "--job", other.job_id])
    assert code != int(ExitCode.DECISION_REQUIRED), "it was shown the gate"
    assert envelope["cause"]["reason"] == "internal-error"
    assert "adopt.apply" in envelope["cause"]["message"]
    assert _rows(moved) == before


def test_rows_under_a_digest_that_does_not_describe_them_are_never_shown(moved):
    _run_id, job_id = approve_and_queue(VERB, GATE)
    with jobs.open_store() as store:
        document = dict(jobs.get(store, job_id).payload[move_cli.PLAN_KEY])
    document["moves"] = document["moves"][:1]
    _requeued(job_id, **{move_cli.PLAN_KEY: document})
    before = _rows(moved)
    code, envelope = drive(["adopt", "move", "--job", job_id])
    assert code == int(ExitCode.DECISION_STALE), envelope
    assert "shown" not in envelope["cause"].get("detail", {})
    assert _rows(moved) == before


def test_the_summary_a_person_reads_names_every_ending(moved):
    job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    summary = resumed["data"]["progress"]["move"]
    assert {"moved", "in_both", "untouched", "neither", "gone", "skipped", "held_back"} <= set(
        summary
    )
    report = artifacts.committed(moved, job_id)[-1]
    for name in ("neither", "skipped"):
        assert summary[name] == report[name] == []


# ── the endings a queued verb owes ─────────────────────────────────────────


def test_a_parked_move_leaves_blocked_and_non_zero(moved, monkeypatch):
    """R-290 for a key ``tests/test_job_outcome.py`` cannot drive, which names
    this function as the place the key is covered."""
    from cratekit.core.cause import refuse

    def parks(job, item, cfg):
        raise jobs.Parked(
            refuse("provider-blocked", "the run must stop", origin=("test",)).cause
        )

    before = _rows(moved)
    _run_id, job_id = approve_and_queue(VERB, GATE)
    monkeypatch.setattr(handlers, "resolve", lambda _key: parks)

    code, envelope = drive(_resume(job_id))

    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.BLOCKED, envelope
    assert envelope["outcome"] == "blocked", envelope
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "provider-blocked"
    assert _rows(moved) == before


def test_a_cancelled_move_exits_with_its_own_cause_and_not_ok(moved):
    before = _rows(moved)
    _run_id, job_id = approve_and_queue(VERB, GATE)
    with jobs.open_store() as store:
        jobs.cancel(store, job_id, stage="interrupted")

    code, envelope = drive(_resume(job_id))

    assert code == int(ExitCode.INTERRUPTED), envelope
    assert envelope["cause"]["reason"] == "cancelled"
    assert _rows(moved) == before


def test_a_job_carrying_no_plan_is_refused_rather_than_driven(moved):
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="adopt.move",
            payload={"tree": TREE_ID, "digest": "d"},
            item_ids=("d",),
            cfg=moved,
        )
    code, envelope = drive(["adopt", "move", "--job", job.job_id])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "internal-error"
    assert job.job_id in envelope["cause"]["message"]


# ── the worker's own checks ────────────────────────────────────────────────


def _worker(job_id: str):
    handler = handlers.resolve(registry.entry("adopt.move").handler_key)
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[0]
    return handler, job, item


def _file_in(cfg, content_id: str, sub_id: str) -> None:
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        folder_display, sub_display = _place(sub_id)
        folder = rb_writer.ensure_folder(handle, folder_display, parent=root)
        playlist = rb_writer.ensure_playlist(handle, sub_display, folder)
        rb_writer.add_memberships(handle, playlist, [content_id])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)


def test_a_track_filed_somewhere_nobody_was_shown_is_a_stale_decision(moved):
    _run_id, job_id = approve_and_queue(VERB, GATE)
    _file_in(moved, "m-med-reads-high", LOW)
    before = _rows(moved)

    handler, job, item = _worker(job_id)
    with pytest.raises(Exception) as raised:
        handler(job, item, jobs.frozen_config(job))
    assert raised.value.cause.reason == "decision-stale"
    assert set(raised.value.cause.detail["moved_under"]) == {"m-med-reads-high"}
    assert _rows(moved) == before


def test_a_reading_that_changed_after_the_approval_is_a_stale_decision(moved):
    from cratekit.core import tags

    _run_id, job_id = approve_and_queue(VERB, GATE)
    music = Path(moved.library.root) / "Music"
    assert tags.write_tags(music / "m-med-reads-high.flac", {"energylevel": "1"}) is True
    collection.reset_cache()
    before = _rows(moved)

    handler, job, item = _worker(job_id)
    with pytest.raises(Exception) as raised:
        handler(job, item, jobs.frozen_config(job))
    assert raised.value.cause.reason == "decision-stale"
    assert _rows(moved) == before


def test_a_track_approved_as_in_its_target_that_left_it_is_a_stale_decision(moved):
    _run_id, job_id = approve_and_queue(VERB, GATE)
    conn = sqlite3.connect(Path(moved.library.db_path))
    try:
        conn.execute(
            "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE ContentID = ? "
            "AND PlaylistID IN (SELECT ID FROM djmdPlaylist WHERE Name = ?)",
            ("m-both-reads-high", _place(HIGH)[1]),
        )
        conn.commit()
    finally:
        conn.close()
    before = _rows(moved)

    handler, job, item = _worker(job_id)
    with pytest.raises(Exception) as raised:
        handler(job, item, jobs.frozen_config(job))
    assert raised.value.cause.reason == "decision-stale"
    assert _rows(moved) == before, "its one live place would have been removed"


def _requeued(job_id: str, **changed):
    """The same job with its payload edited, which is what a tampered queue is."""
    import json

    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        payload = {**job.payload, **changed}
        with store.immediate() as conn:
            conn.execute(
                "UPDATE jobs SET payload = ? WHERE job_id = ?", (json.dumps(payload), job_id)
            )
    return _worker(job_id)


def test_rows_that_are_not_the_rows_approved_are_refused(moved):
    _run_id, job_id = approve_and_queue(VERB, GATE)
    with jobs.open_store() as store:
        document = dict(jobs.get(store, job_id).payload[move_cli.PLAN_KEY])
    document["moves"] = [
        {**row, "remove": [DERIVED]} if row["content_id"] == "m-vox-and-med" else row
        for row in document["moves"]
    ]
    before = _rows(moved)
    handler, job, item = _requeued(job_id, **{move_cli.PLAN_KEY: document})
    with pytest.raises(Exception) as raised:
        handler(job, item, jobs.frozen_config(job))
    assert raised.value.cause.reason == "decision-stale"
    assert _rows(moved) == before


def test_a_job_naming_nobody_writes_nothing(moved):
    _run_id, job_id = approve_and_queue(VERB, GATE)
    before = _rows(moved)
    handler, job, item = _requeued(job_id, **{move_cli.ACTOR_KEY: " "})
    with pytest.raises(Exception) as raised:
        handler(job, item, jobs.frozen_config(job))
    assert raised.value.cause.reason == "decision-required"
    assert _rows(moved) == before


def test_the_approving_actor_travels_in_the_payload(moved):
    _run_id, job_id = approve_and_queue(VERB, GATE)
    with jobs.open_store() as store:
        payload = jobs.get(store, job_id).payload
    assert payload[move_cli.ACTOR_KEY] == "a-person"
    assert payload["digest"] == payload[move_cli.PLAN_KEY]["digest"]


def test_a_sub_class_in_an_approved_row_is_refused_by_what_competes_now():
    bucket = _pure_energy_bucket().id
    tracks = [_scanned("t", bucket, energy=8)]
    held = {bucket: {"t": (MED,)}}
    current = adopt_plan.build_adoption_plan(
        tracks, DECLARED, tree=TREE_ID,
        placements=adopt_plan.Placements(read=True, held=held),
    )
    (approved,) = adopt_move.build_move_plan(current, DECLARED).moves
    fields = {name: getattr(approved, name) for name in approved.__slots__}
    fields["remove"] = (MED, DERIVED)
    with pytest.raises(Exception) as raised:
        move_cli.remaining([adopt_move.Move(**fields)], current, DECLARED)
    assert raised.value.cause.reason == "decision-stale"

    todo, gone = move_cli.remaining([approved], current, DECLARED)
    assert ([move.remove for move in todo], gone) == ([(MED,)], ())


def _approved_over(tracks, held) -> tuple[adopt_plan.AdoptionPlan, tuple[adopt_move.Move, ...]]:
    plan = adopt_plan.build_adoption_plan(
        tracks, DECLARED, tree=TREE_ID,
        placements=adopt_plan.Placements(read=True, held=held),
    )
    return plan, adopt_move.build_move_plan(plan, DECLARED).moves


def test_a_track_a_verdict_withheld_since_the_approval_is_a_stale_decision():
    """Found by the review. The bucket and the sub are unchanged by a verdict,
    and the first version of the check compared those two and nothing else."""
    from dataclasses import replace

    bucket = _pure_energy_bucket().id
    current, approved = _approved_over(
        [_scanned("t", bucket, energy=8)], {bucket: {"t": (MED,)}}
    )
    (entry,) = current.entries
    refused = replace(
        current,
        entries=(
            replace(
                entry,
                disposition=adopt_scan.Disposition.WITHHELD,
                holds=(),
                holds_unnamed=(),
                withheld_by=adopt_plan.WITHHELD_BY_VERDICT,
            ),
        ),
    )
    assert (refused.entries[0].bucket, refused.entries[0].sub) == (bucket, HIGH)
    with pytest.raises(Exception) as raised:
        move_cli.remaining(approved, refused, DECLARED)
    assert raised.value.cause.reason == "decision-stale"
    assert "does not move it" in raised.value.cause.detail["moved_under"]["t"]


def test_a_genre_that_stopped_naming_the_style_is_a_stale_decision():
    """The resolver's default can equal the approved target, so the sub alone
    does not say whether the file still names it."""
    style = _style_bucket()
    default = style.sub_by_source.default
    named = next(g for g, sub in style.sub_by_source.map.items() if sub == default)
    held = next(sub.id for sub in style.subs if sub.id != default)
    _plan, approved = _approved_over(
        [_scanned("t", style.id, energy=None, genre=named)], {style.id: {"t": (held,)}}
    )
    assert [move.target for move in approved] == [default]

    now, _none = _approved_over(
        [_scanned("t", style.id, energy=None, genre="A genre no style is declared for")],
        {style.id: {"t": (held,)}},
    )
    assert (now.entries[0].bucket, now.entries[0].sub) == (style.id, default)
    with pytest.raises(Exception) as raised:
        move_cli.remaining(approved, now, DECLARED)
    assert raised.value.cause.reason == "decision-stale"
    assert adopt_move.LEFT_NO_STYLE in raised.value.cause.detail["moved_under"]["t"]


def test_a_reading_lost_since_the_approval_is_a_stale_decision():
    bucket = _pure_energy_bucket().id
    _plan, approved = _approved_over(
        [_scanned("t", bucket, energy=None)], {bucket: {"t": (SINK, HIGH)}}
    )
    assert approved == ()
    _plan, approved = _approved_over(
        [_scanned("t", bucket, energy=8)], {bucket: {"t": (SINK,)}}
    )
    # The file loses its tag, and the sink is where an untagged track goes.
    now, _none = _approved_over([_scanned("t", bucket, energy=None)], {bucket: {"t": (SINK,)}})
    with pytest.raises(Exception) as raised:
        move_cli.remaining(approved, now, DECLARED)
    assert raised.value.cause.reason == "decision-stale"


def test_what_is_left_of_a_move_is_narrowed_and_a_finished_one_is_dropped():
    bucket = _pure_energy_bucket().id
    tracks = [_scanned("a", bucket, energy=8), _scanned("b", bucket, energy=8)]
    start = adopt_plan.build_adoption_plan(
        tracks, DECLARED, tree=TREE_ID,
        placements=adopt_plan.Placements(read=True, held={bucket: {"a": (MED,), "b": (MED,)}}),
    )
    approved = adopt_move.build_move_plan(start, DECLARED).moves
    halfway = adopt_plan.build_adoption_plan(
        tracks, DECLARED, tree=TREE_ID,
        placements=adopt_plan.Placements(
            read=True, held={bucket: {"a": (MED, HIGH), "b": (HIGH,)}}
        ),
    )
    todo, gone = move_cli.remaining(approved, halfway, DECLARED)
    assert [(m.content_id, m.add, m.remove) for m in todo] == [("a", "", (MED,))]
    assert gone == ()

    without_b = adopt_plan.build_adoption_plan(
        tracks[:1], DECLARED, tree=TREE_ID,
        placements=adopt_plan.Placements(read=True, held={bucket: {"a": (MED,)}}),
    )
    todo, gone = move_cli.remaining(approved, without_b, DECLARED)
    assert ([m.content_id for m in todo], gone) == (["a"], ("b",))

    unread = adopt_plan.build_adoption_plan(tracks, DECLARED, tree=TREE_ID)
    with pytest.raises(Exception) as raised:
        move_cli.remaining(approved, unread, DECLARED)
    assert raised.value.cause.reason == "decision-stale"


# ---------------------------------------------------------------------------
# The writer's own guards
# ---------------------------------------------------------------------------


def _write(cfg, moves, monkeypatch=None):
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        return trees.move_tree_membership(
            cfg,
            handle,
            tree_id=TREE_ID,
            registry=tree_registry.read(cfg),
            moves=moves,
            root_exists=lambda root_id: root_id in known,
            analysis_roots=[Path(cfg.library.root)],
        )
    finally:
        rb_writer.close_db(handle)


def test_a_track_not_in_its_target_has_nothing_removed(moved, monkeypatch):
    """Never in neither: the removal waits on the addition being in the database."""
    before = _rows(moved)
    monkeypatch.setattr(rb_writer, "add_memberships", lambda *_args, **_kwargs: [])
    report = _write(
        moved,
        [trees.MembershipMove("m-med-reads-high", _place(HIGH), (_place(MED),))],
    )
    assert report.held_back == ("m-med-reads-high",)
    assert (report.added, report.removed) == (0, 0)
    assert _live(moved)["m-med-reads-high"] == {_place(MED)}
    assert [row for row in _rows(moved) if row[3]] == [row for row in before if row[3]] == []


def test_a_track_with_no_live_collection_row_is_skipped_whole(moved):
    conn = sqlite3.connect(Path(moved.library.db_path))
    try:
        conn.execute("UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = 'm-med-reads-high'")
        conn.commit()
    finally:
        conn.close()
    before = _rows(moved)
    report = _write(
        moved,
        [
            trees.MembershipMove("m-med-reads-high", _place(HIGH), (_place(MED),)),
            trees.MembershipMove("nobody", _place(HIGH), (_place(MED),)),
        ],
    )
    assert report.skipped == ("m-med-reads-high", "nobody")
    assert (report.added, report.removed) == (0, 0)
    assert _rows(moved) == before


def test_a_removal_from_a_playlist_that_is_not_there_creates_none(moved):
    def playlists():
        conn = sqlite3.connect(Path(moved.library.db_path))
        try:
            return conn.execute("SELECT COUNT(*) FROM djmdPlaylist").fetchone()[0]
        finally:
            conn.close()

    before = playlists()
    report = _write(
        moved, [trees.MembershipMove("m-same", _place(MED), (_place(LOW),))]
    )
    assert (report.removed, report.already_absent, report.already_present) == (0, 1, 1)
    assert playlists() == before


def test_the_target_is_never_removed_from_even_when_a_move_names_it(moved):
    report = _write(
        moved, [trees.MembershipMove("m-same", _place(MED), (_place(MED),))]
    )
    assert report.removed == 0
    assert _live(moved)["m-same"] == {_place(MED)}


def test_a_doubled_membership_leaves_in_one_move(moved):
    conn = sqlite3.connect(Path(moved.library.db_path))
    try:
        conn.execute(
            "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, "
            "rb_local_deleted, created_at, updated_at) "
            "SELECT 'doubled', PlaylistID, ContentID, 99, 0, created_at, updated_at "
            "FROM djmdSongPlaylist WHERE ContentID = 'm-med-reads-high'"
        )
        conn.commit()
    finally:
        conn.close()
    report = _write(
        moved, [trees.MembershipMove("m-med-reads-high", _place(HIGH), (_place(MED),))]
    )
    assert report.removed == 2
    assert _live(moved)["m-med-reads-high"] == {_place(HIGH)}


def test_the_move_takes_one_capture_and_records_both_commits(moved):
    from cratekit.core import snapshot

    taken = []
    real = snapshot.capture

    def counting(*args, **kwargs):
        taken.append(1)
        return real(*args, **kwargs)

    import unittest.mock

    with unittest.mock.patch.object(snapshot, "capture", counting):
        _job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    assert len(taken) == 1

    (record,) = [r for r in session.records(moved) if r.workflow == trees.MOVE_WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert record.snapshot_path
    assert (record.change.created, record.change.updated) == (4, 9)
    assert record.sources == {TREE_ID: str(session.SourceState.COMMITTED)}


def test_an_empty_watch_is_refused(moved):
    handle = rb_writer.open_db(rb_writer.live_db_path(moved), unlock=False, cfg=moved)
    try:
        with pytest.raises(ValueError, match="analysis_roots is empty"):
            trees.move_tree_membership(
                moved, handle, tree_id=TREE_ID, registry=tree_registry.read(moved),
                moves=[], root_exists=lambda _root: True, analysis_roots=[],
            )
    finally:
        rb_writer.close_db(handle)


def test_a_tree_still_on_the_bridge_is_refused(machine):  # noqa: F811
    handle = rb_writer.open_db(rb_writer.live_db_path(machine), unlock=False, cfg=machine)
    try:
        with pytest.raises(tree_registry.TreeModeRefused):
            trees.move_tree_membership(
                machine, handle, tree_id=TREE_ID, registry=tree_registry.read(machine),
                moves=[], root_exists=lambda _root: True,
                analysis_roots=[Path(machine.library.root)],
            )
    finally:
        rb_writer.close_db(handle)


# ── every other writer still cannot remove ─────────────────────────────────


def _mark_one_removed(handle) -> None:
    (song,) = [
        row
        for row in handle.get_playlist_songs(ContentID="m-med-reads-high")
        if not rb_writer.membership_removed(row)
    ]
    playlist = handle.get_playlist(ID=str(song.PlaylistID))
    assert rb_writer.remove_memberships(handle, playlist, ["m-med-reads-high"]) == [
        "m-med-reads-high"
    ]


def test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back(moved):
    before = _rows(moved)
    handle = rb_writer.open_db(rb_writer.live_db_path(moved), unlock=False, cfg=moved)
    try:
        _mark_one_removed(handle)
        with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
            rb_writer.commit_guarded(handle)
        assert raised.value.cause.reason == "whitelist-violation"
        assert "soft delete marker" in raised.value.cause.message
    finally:
        rb_writer.close_db(handle)
    assert _rows(moved) == before


def test_a_commit_that_admits_the_removal_lands_it(moved):
    handle = rb_writer.open_db(rb_writer.live_db_path(moved), unlock=False, cfg=moved)
    try:
        _mark_one_removed(handle)
        rb_writer.commit_guarded(handle, removals=rb_writer.REMOVABLE_TABLES)
    finally:
        rb_writer.close_db(handle)
    assert _removed(moved) == {"m-med-reads-high": {_place(MED)}}


def test_an_admitted_commit_refuses_a_removed_collection_row(moved):
    before = _rows(moved)
    handle = rb_writer.open_db(rb_writer.live_db_path(moved), unlock=False, cfg=moved)
    try:
        row = handle.get_content(ID="m-med-reads-high")
        setattr(row, rb_writer.SOFT_DELETE_COLUMN, 1)
        with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
            rb_writer.commit_guarded(handle, removals=rb_writer.REMOVABLE_TABLES)
        assert raised.value.cause.reason == "whitelist-violation"
        assert "djmdContent" in raised.value.cause.message
    finally:
        rb_writer.close_db(handle)
    assert _rows(moved) == before
    conn = sqlite3.connect(Path(moved.library.db_path))
    try:
        assert conn.execute(
            "SELECT rb_local_deleted FROM djmdContent WHERE ID = 'm-med-reads-high'"
        ).fetchone() == (0,)
    finally:
        conn.close()


def test_an_admitted_commit_refuses_a_hard_delete_of_a_membership(moved):
    before = _rows(moved)
    handle = rb_writer.open_db(rb_writer.live_db_path(moved), unlock=False, cfg=moved)
    try:
        (song,) = list(handle.get_playlist_songs(ContentID="m-med-reads-high"))
        handle.delete(song)
        with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
            rb_writer.commit_guarded(handle, removals=rb_writer.REMOVABLE_TABLES)
        assert "additive-only" in raised.value.cause.message
    finally:
        rb_writer.close_db(handle)
    assert _rows(moved) == before


def test_the_additive_membership_writer_refuses_a_removal_in_its_session(moved, monkeypatch):
    """The other writer's own session, with a removal slipped into it."""
    before = _rows(moved)
    real = rb_writer.add_memberships

    def adds_and_removes(db, playlist, content_ids):
        _mark_one_removed(db)
        return real(db, playlist, content_ids)

    monkeypatch.setattr(rb_writer, "add_memberships", adds_and_removes)
    handle = rb_writer.open_db(rb_writer.live_db_path(moved), unlock=False, cfg=moved)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
            trees.write_tree_membership(
                moved,
                handle,
                tree_id=TREE_ID,
                registry=tree_registry.read(moved),
                plan={_place(LOW): [adopt_fixtures.recorded_location(
                    Path(moved.library.root), "m-same.flac"
                )]},
                rows=collection.read_collection(moved),
                root_exists=lambda root_id: root_id in known,
                analysis_roots=[Path(moved.library.root)],
            )
        assert raised.value.cause.reason == "whitelist-violation"
    finally:
        rb_writer.close_db(handle)
    assert _rows(moved) == before


def test_the_moves_own_first_commit_refuses_a_removal(moved, monkeypatch):
    """Only the second commit admits one, so a removal in the additions is refused."""
    before = _rows(moved)
    real = rb_writer.add_memberships

    def adds_and_removes(db, playlist, content_ids):
        _mark_one_removed(db)
        return real(db, playlist, content_ids)

    monkeypatch.setattr(rb_writer, "add_memberships", adds_and_removes)
    with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
        _write(moved, [trees.MembershipMove("m-same", _place(LOW), (_place(MED),))])
    assert raised.value.cause.reason == "whitelist-violation"
    assert _rows(moved) == before


# ── the readers ─────────────────────────────────────────────────────────────


def test_a_removed_membership_is_not_held_and_not_present(moved):
    from cratekit.adopt import placements

    bucket = _energy_bucket().id
    assert placements.read_placements(moved, DECLARED).holds(bucket, "m-med-reads-high") == (MED,)
    handle = rb_writer.open_db(rb_writer.live_db_path(moved), unlock=False, cfg=moved)
    try:
        _mark_one_removed(handle)
        handle.session.commit()
        playlist = next(
            row for row in handle.get_playlist(Name=_place(MED)[1])
        )
        # Absent to the writer, so an add inserts a live row beside the removed one.
        assert rb_writer.add_memberships(handle, playlist, ["m-med-reads-high"]) == [
            "m-med-reads-high"
        ]
        # And a second removal finds the one live row and not the removed one.
        assert rb_writer.remove_memberships(handle, playlist, ["m-med-reads-high"]) == [
            "m-med-reads-high"
        ]
        assert rb_writer.remove_memberships(handle, playlist, ["m-med-reads-high"]) == []
        handle.session.rollback()
    finally:
        rb_writer.close_db(handle)
    assert placements.read_placements(moved, DECLARED).holds(bucket, "m-med-reads-high") == ()


def test_a_membership_row_that_cannot_say_refuses():
    class Row:
        ID = "r"

    class Unset(Row):
        rb_local_deleted = None

    for row in (Row(), Unset()):
        with pytest.raises(Exception) as raised:
            rb_writer.membership_removed(row)
        assert raised.value.cause.reason == "soft-delete-marker-unreadable"


# ── the registry ────────────────────────────────────────────────────────────


def test_the_verb_is_its_own_and_resort_is_still_additive():
    entry = registry.entry("adopt.move")
    assert entry.landed and entry.destructive and entry.long_running
    assert entry.writes == frozenset({"db_tree"})
    assert entry.module_id == registry.entry("adopt.apply").module_id
    (approve,) = [spec for spec in entry.gates if spec.digest_source == "plan"]
    assert (approve.name, approve.explicit, approve.options) == (GATE, True, ("approve", "abort"))
    resort = registry.entry("route.resort")
    assert "additive" in resort.summary
    assert all(spec.digest_source is None for spec in resort.gates)


def test_the_resume_carries_the_run_that_holds_the_approval(moved):
    run_id, job_id = approve_and_queue(VERB, GATE)
    assert _resume(job_id) == ["--run", run_id, "adopt", "move", "--job", job_id]
