"""R-758: a track is moved from the competing sub it holds to the one its file names.

``crate adopt move`` acts on the list adoption withholds, and is the first verb
that removes a membership. The pure plan is held first, then the verb through
the real dispatcher against a disposable library with real tags, then the
writer's own guards. Every expected identifier is derived from the shipped
taxonomy's declarations rather than spelled.

The shared library builder, :func:`seed_library`, and the plan helpers serve
the other move suites too (former place, split place, jazz folder).

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import shutil
import sqlite3
from dataclasses import replace
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
OK, STALE = int(ExitCode.OK), int(ExitCode.DECISION_STALE)


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


HERE, THERE = _pure_energy_bucket().id, _other_energy_bucket().id


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


def classified(
    content_id: str,
    *,
    energy: int | None,
    genre: str,
    disposition: adopt_scan.Disposition = adopt_scan.Disposition.ROUTE,
) -> adopt_scan.ScannedTrack:
    """A track routed by what the census makes of its genre, or one it excluded."""
    verdict, bucket, _match = adopt_scan.classify_genre(DECLARED, genre)
    routed = disposition is adopt_scan.Disposition.ROUTE
    return adopt_scan.ScannedTrack(
        content_id=content_id,
        recorded=f"/library/Music/{content_id}.flac",
        path=f"/library/Music/{content_id}.flac" if routed else None,
        readability=(adopt_scan.Readability.READABLE if routed else adopt_scan.Readability.MISSING),
        disposition=verdict if routed else disposition,
        genre=genre,
        bucket=bucket if routed else "",
        energy=energy,
    )


def _no_genre(content_id: str, *, energy: int | None) -> adopt_scan.ScannedTrack:
    """A track the census could not route: no genre, so no bucket of its own."""
    return replace(
        _scanned(content_id, HERE, energy=energy),
        disposition=adopt_scan.Disposition.NEEDS_GENRE,
        genre="",
        bucket="",
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


def _refused(call, reason: str = "decision-stale"):
    """The cause ``call`` raised, asserted to carry ``reason``."""
    with pytest.raises(Exception) as raised:
        call()
    assert raised.value.cause.reason == reason, raised.value.cause
    return raised.value.cause


@pytest.mark.parametrize(
    ("energy", "held", "add", "remove"),
    [
        (8, (MED,), HIGH, (MED,)),
        (8, (LOW, MED, HIGH), "", tuple(sorted((LOW, MED)))),
        (5, (SINK,), MED, (SINK,)),
        # R-758's rule in the entry's own bucket, untouched by R-780: a reading
        # naming a third band adds it, as adoption itself would file it there.
        (1, (MED, HIGH), LOW, tuple(sorted((MED, HIGH)))),
    ],
    ids=["leaves-med", "three-bands", "leaves-the-sink", "a-third-band"],
)
def test_a_track_in_a_band_its_reading_does_not_name_moves_to_the_one_it_does(
    energy, held, add, remove
):
    plan = _moves([_scanned("t", HERE, energy=energy)], {HERE: {"t": held}})
    (move,) = plan.moves
    assert (move.target, move.add, move.remove, move.holds) == (
        _band(energy),
        add,
        remove,
        tuple(sorted(held)),
    )
    assert (move.kind, move.decided_by, move.energy) == ("band", "energy", energy)
    assert plan.left == ()
    assert plan.counts()["memberships_added"] == (1 if add else 0)
    assert plan.counts()["memberships_removed"] == len(remove)


def test_a_track_in_both_has_only_the_stale_one_removed():
    test_a_track_in_a_band_its_reading_does_not_name_moves_to_the_one_it_does(
        8, (MED, HIGH), "", (MED,)
    )


@pytest.mark.parametrize("sub_class", sorted(CLASSES))
def test_a_sub_class_is_never_a_source_and_never_removed_from(sub_class):
    alone = _moves([_scanned("t", HERE, energy=8)], {HERE: {"t": (sub_class,)}})
    assert alone.moves == () and alone.left == ()

    beside = _moves([_scanned("t", HERE, energy=8)], {HERE: {"t": (sub_class, MED)}})
    (move,) = beside.moves
    assert move.remove == (MED,)
    assert sub_class not in move.holds


def test_both_policies_are_declared_so_the_test_above_means_something():
    assert {entry.policy for entry in DECLARED.sub_classes} == set(taxonomy.SubPolicy)


def _excluded(content_id: str) -> adopt_scan.ScannedTrack:
    """A file the census could not read: it has no reading, whatever its row says."""
    return adopt_scan.ScannedTrack(
        content_id=content_id,
        recorded=f"/library/Music/{content_id}.flac",
        path=None,
        readability=adopt_scan.Readability.MISSING,
        disposition=adopt_scan.Disposition.EXCLUDED,
        genre=DECLARED.bucket(HERE).display,
        energy=8,
    )


#: Tracks left where they are and listed, with nothing moved: the track, what
#: it holds, the rows held under another name and twice, and the one row left.
_LEFT_ALONE = {
    "no-reading": (
        _scanned("t", HERE, energy=None), {HERE: {"t": (HIGH,)}}, {}, {},
        {"reason": adopt_move.LEFT_NO_READING, "holds": (HIGH,), "target": SINK},
    ),
    "under-another-name": (
        _scanned("t", HERE, energy=8), {HERE: {"t": (MED,)}}, {HERE: {"t": (MED,)}}, {},
        {"reason": adopt_move.LEFT_UNNAMED, "holds_unnamed": (MED,)},
    ),
    # R-780: nothing is ADDED in a bucket the genre does not name, so a
    # reading that picks none of the subs held there leaves the track listed.
    "names-neither-elsewhere": (
        _scanned("t", THERE, energy=1), {HERE: {"t": (MED, HIGH)}}, {}, {},
        {"bucket": HERE, "reason": adopt_move.LEFT_NAMES_NEITHER, "target": LOW,
         "holds": tuple(sorted((MED, HIGH))), "energy": 1},
    ),
    "no-reading-elsewhere": (
        _scanned("t", THERE, energy=None), {HERE: {"t": (MED, HIGH)}}, {}, {},
        {"bucket": HERE, "reason": adopt_move.LEFT_NO_READING, "target": SINK},
    ),
    "under-another-name-elsewhere": (
        _scanned("t", THERE, energy=8), {HERE: {"t": (MED, HIGH)}}, {HERE: {"t": (MED,)}}, {},
        {"reason": adopt_move.LEFT_UNNAMED, "holds_unnamed": (MED,)},
    ),
    "excluded-in-two-bands": (
        _excluded("t"), {HERE: {"t": (MED, HIGH)}}, {}, {},
        {"bucket": HERE, "reason": adopt_move.LEFT_NO_READING,
         "holds": tuple(sorted((MED, HIGH)))},
    ),
    # R-781: one sub held by two rows is listed and not moved, wherever the genre routes.
    "two-rows-genre-names-it": (
        _scanned("t", HERE, energy=2), {HERE: {"t": (LOW,)}}, {}, {HERE: {"t": (LOW,)}},
        {"bucket": HERE, "reason": adopt_move.LEFT_DOUBLED_ROWS, "holds": (LOW,), "target": LOW},
    ),
    "two-rows-genre-elsewhere": (
        _scanned("t", THERE, energy=2), {HERE: {"t": (LOW,)}}, {}, {HERE: {"t": (LOW,)}},
        {"bucket": HERE, "reason": adopt_move.LEFT_DOUBLED_ROWS, "holds": (LOW,), "target": LOW},
    ),
}  # fmt: skip


@pytest.mark.parametrize("case", sorted(_LEFT_ALONE))
def test_a_track_with_nothing_to_move_on_is_left_and_listed_under_its_reason(case):
    track, held, unnamed, doubled, expected = _LEFT_ALONE[case]
    plan = _moves([track], held, unnamed=unnamed, doubled=doubled)
    assert plan.moves == ()
    (left,) = plan.left
    assert {name: getattr(left, name) for name in expected} == expected
    assert plan.counts()["left"] == _left_counts(**{expected["reason"]: 1})


def test_a_track_already_where_its_reading_names_is_not_planned():
    plan = _moves([_scanned("t", HERE, energy=5)], {HERE: {"t": (MED,)}})
    assert plan.moves == () and plan.left == ()
    nowhere = _moves([_scanned("t", HERE, energy=5)], {})
    assert nowhere.moves == () and nowhere.left == ()
    single = _moves([_excluded("t")], {HERE: {"t": (MED,)}})
    assert single.moves == () and single.left == ()


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
    bucket = next(b for b in DECLARED.buckets if b.sub_by_source is None and not b.energy.enabled)
    kind, competing = routing.competing_subs(DECLARED, bucket.id)
    assert kind is routing.Competing.STYLE and competing == {bucket.single_sub.id}
    plan = _moves([_scanned("t", bucket.id, energy=8)], {bucket.id: {"t": tuple(competing)}})
    assert plan.moves == () and plan.left == ()


def test_a_bucket_that_reads_neither_energy_nor_genre_has_no_reading_to_move_on():
    """Nothing in the shipped template declares one, so the template is given
    one: several subs, no energy, no map from genre."""
    plain = next(b for b in DECLARED.buckets if b.sub_by_source is None and not b.energy.enabled)
    extra = taxonomy.Sub("another_place", "Another place")
    buckets = tuple(
        replace(b, subs=(*b.subs, extra)) if b.id == plain.id else b for b in DECLARED.buckets
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


def test_a_tree_nobody_read_plans_nothing_and_says_unread():
    unread = adopt_plan.build_adoption_plan(
        [_scanned("t", HERE, energy=8)],
        DECLARED,
        tree=TREE_ID,
        placements=adopt_plan.Placements(read=False, held={HERE: {"t": (MED,)}}),
    )
    plan = adopt_move.build_move_plan(unread, DECLARED)
    assert (plan.moves, plan.left, plan.placements) == ((), (), "unread")
    read = _moves([_scanned("t", HERE, energy=5)], {HERE: {"t": (MED,)}})
    assert read.moves == () and read.digest() != plan.digest()


def test_the_counts_split_by_kind_and_total():
    style = _style_bucket()
    named = next(g for g, sub in style.sub_by_source.map.items() if sub == style.subs[1].id)
    plan = _moves(
        [
            _scanned("a", HERE, energy=8),
            _scanned("b", HERE, energy=2),
            _scanned("c", style.id, energy=None, genre=named),
        ],
        {HERE: {"a": (MED,), "b": (MED, LOW)}, style.id: {"c": (style.subs[0].id,)}},
    )
    assert plan.counts() == {
        "moves": 3,
        "band": 2,
        "style": 1,
        "memberships_added": 2,
        "memberships_removed": 3,
        "left": _left_counts(),
    }


def _one_move(**changed) -> adopt_move.MovePlan:
    plan = _moves([_scanned("t", HERE, energy=8)], {HERE: {"t": (MED,)}})
    (move,) = plan.moves
    return adopt_move.MovePlan(
        tree=plan.tree, placements=plan.placements, moves=(replace(move, **changed),)
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
    left = adopt_move.Left(
        content_id="l", location="/l", bucket=HERE, kind="band",
        reason=adopt_move.LEFT_NO_READING, target=SINK, holds=(HIGH,),
        holds_unnamed=(), energy=None, genre="g",
    )  # fmt: skip
    with_left = replace(base, left=(left,))
    other_tree = adopt_move.MovePlan(tree="another", placements="read", moves=base.moves)
    assert len({base.digest(), with_left.digest(), other_tree.digest()}) == 3


def test_the_frozen_rows_read_back_to_the_moves_and_to_the_digest():
    plan = _moves(
        [_scanned("a", HERE, energy=8), _scanned("b", HERE, energy=None)],
        {HERE: {"a": (MED,), "b": (HIGH,)}},
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


def test_a_double_in_a_bucket_the_genre_does_not_name_moves_on_the_reading():
    """The shape read back off the author's library: the genre routes the
    track to one bucket and it sits in two bands of another."""
    held = {HERE: {"t": (MED, HIGH)}, THERE: {"t": (HIGH,)}}
    adoption = _adoption([_scanned("t", THERE, energy=8)], held)
    # NOT ON ADOPTION'S LIST, which is the whole of R-780.
    assert adoption.held_elsewhere() == ()
    assert [entry.bucket for entry in adoption.entries] == [THERE]

    plan = adopt_move.build_move_plan(adoption, DECLARED)
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add) == (HERE, HIGH, "")
    assert (move.remove, move.holds) == ((MED,), tuple(sorted((MED, HIGH))))
    assert (move.kind, move.decided_by, move.energy) == ("band", "energy", 8)
    assert plan.left == ()
    assert plan.counts()["memberships_added"] == 0


def test_a_track_with_no_genre_is_asked_in_every_bucket_it_doubles_in():
    """The other shape read back: a blank genre, so no entry bucket at all."""
    plan = _moves([_no_genre("t", energy=2)], {HERE: {"t": (LOW, MED)}, THERE: {"t": (MED, HIGH)}})
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add, move.remove) == (HERE, LOW, "", (MED,))
    (left,) = plan.left
    assert (left.bucket, left.reason, left.target) == (THERE, adopt_move.LEFT_NAMES_NEITHER, LOW)


def test_what_the_tree_path_never_asks_about():
    """One sub in a bucket the genre does not name is adoption's question, and
    a style double there is out of scope, as is a doubled row in a sub class."""
    for track in (_scanned("t", THERE, energy=8), _no_genre("t", energy=8)):
        plan = _moves([track], {HERE: {"t": (MED,)}})
        assert plan.moves == () and plan.left == ()
    style = _style_bucket()
    plan = _moves(
        [_scanned("t", HERE, energy=8)],
        {HERE: {"t": (HIGH,)}, style.id: {"t": (style.subs[0].id, style.subs[1].id)}},
    )
    assert plan.moves == () and plan.left == ()
    plan = _moves(
        [_scanned("t", HERE, energy=5)],
        {HERE: {"t": (MED, DERIVED)}},
        doubled={HERE: {"t": (DERIVED,)}},
    )
    assert plan.moves == () and plan.left == ()


def _with_verdict_on(current: adopt_plan.AdoptionPlan, bucket: str) -> adopt_plan.AdoptionPlan:
    """The plan with a keep-separate verdict folded in for one bucket, the way
    ``with_collision_verdicts`` folds it: every routed entry of that bucket
    withheld under the verdict's reason."""
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


def _refused_over(tracks, held: dict) -> adopt_plan.AdoptionPlan:
    """Adoption over an empty tree with every entry then withheld by a
    verdict, handed ``held`` as the tree the move reads."""
    current = _adoption(tracks, {})
    entries = tuple(
        replace(
            entry,
            disposition=adopt_scan.Disposition.WITHHELD,
            withheld_by=adopt_plan.WITHHELD_BY_VERDICT,
        )
        for entry in current.entries
    )
    placements = adopt_plan.Placements(read=True, held=held)
    return replace(current, entries=entries, placements=placements)


def test_a_verdict_withheld_double_is_left_and_listed_under_its_own_reason():
    current = _adoption([_scanned("t", HERE, energy=8)], {HERE: {"t": (MED, HIGH)}})
    (move,) = adopt_move.build_move_plan(current, DECLARED).moves
    assert move.remove == (MED,)
    plan = adopt_move.build_move_plan(_with_verdict_on(current, HERE), DECLARED)
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.reason, left.bucket, left.holds) == (
        adopt_move.LEFT_VERDICT,
        HERE,
        tuple(sorted((MED, HIGH))),
    )


def test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder():
    """A verdict honoured only on the entry's own bucket would remove a
    membership inside a folder the person refused, where the track sat under
    another genre."""
    tracks = [_scanned("t", THERE, energy=8), _scanned("u", HERE, energy=5)]
    held = {HERE: {"t": (MED, HIGH), "u": (MED,)}, THERE: {"t": (HIGH,)}}
    current = _adoption(tracks, held)
    assert [move.content_id for move in adopt_move.build_move_plan(current, DECLARED).moves] == [
        "t"
    ]

    refused = _with_verdict_on(current, HERE)
    assert adopt_move.refused_buckets(refused.entries) == {HERE}
    plan = adopt_move.build_move_plan(refused, DECLARED)
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.content_id, left.bucket, left.reason) == ("t", HERE, adopt_move.LEFT_VERDICT)

    # And the worker refuses a move approved before the verdict landed.
    (approved,) = adopt_move.build_move_plan(current, DECLARED).moves
    cause = _refused(lambda: move_cli.remaining([approved], refused, DECLARED))
    assert adopt_move.LEFT_VERDICT in cause.detail["moved_under"]["t"]


def test_a_verdict_no_entry_routes_to_is_not_known_and_is_recorded_as_such():
    """The plan carries a verdict only as the entries it withheld, so a bucket
    no entry routes to reads as unrefused. Pinned so the gap is visible."""
    current = _adoption([_scanned("t", THERE, energy=8)], {HERE: {"t": (MED, HIGH)}})
    assert adopt_move.refused_buckets(_with_verdict_on(current, HERE).entries) == frozenset()


def test_a_double_beside_a_track_left_for_another_reason_is_still_listed():
    plan = _moves(
        [_scanned("t", THERE, energy=1)],
        {HERE: {"t": (MED, HIGH)}},
        doubled={HERE: {"t": (HIGH,)}},
    )
    assert plan.moves == ()
    assert [left.reason for left in plan.left] == [
        adopt_move.LEFT_NAMES_NEITHER,
        adopt_move.LEFT_DOUBLED_ROWS,
    ]
    assert plan.counts()["left"]["total"] == 2


def test_one_track_carries_a_move_in_each_bucket_it_doubles_in():
    current = _adoption(
        [_scanned("t", THERE, energy=5)], {HERE: {"t": (MED, HIGH)}, THERE: {"t": (LOW, MED)}}
    )
    moves = adopt_move.build_move_plan(current, DECLARED).moves
    assert [(m.bucket, m.remove) for m in moves] == [(HERE, (HIGH,)), (THERE, (LOW,))]
    assert len({m.move_id for m in moves}) == 2
    # Gone once, though it carried two moves.
    assert move_cli.remaining(moves, _adoption([], {}), DECLARED) == ((), ("t",))


def test_a_target_held_only_under_another_name_is_not_done():
    """A track whose one place is a renamed playlist is refused on purpose,
    not read as finished."""
    tracks = [_scanned("t", HERE, energy=8)]
    approved = adopt_move.build_move_plan(_adoption(tracks, {HERE: {"t": (MED,)}}), DECLARED).moves
    renamed = _adoption(tracks, {HERE: {"t": (HIGH,)}}, unnamed={HERE: {"t": (HIGH,)}})
    cause = _refused(lambda: move_cli.remaining(approved, renamed, DECLARED))
    assert "another name" in cause.detail["moved_under"]["t"]
    done = _adoption(tracks, {HERE: {"t": (HIGH,)}})
    assert move_cli.remaining(approved, done, DECLARED) == ((), ())


def test_a_doubled_target_beside_a_stale_sub_is_a_move_and_the_double_is_listed_after():
    track = _scanned("t", HERE, energy=2)
    plan = _moves([track], {HERE: {"t": (LOW, MED)}}, doubled={HERE: {"t": (LOW,)}})
    (move,) = plan.moves
    assert (move.add, move.remove) == ("", (MED,))
    assert plan.left == ()
    after = _moves([track], {HERE: {"t": (LOW,)}}, doubled={HERE: {"t": (LOW,)}})
    assert after.moves == ()
    assert [left.reason for left in after.left] == [adopt_move.LEFT_DOUBLED_ROWS]


def test_the_digest_moves_when_a_double_appears_in_a_bucket_the_genre_does_not_name():
    tracks = [_scanned("t", THERE, energy=8)]
    alone = _moves(tracks, {THERE: {"t": (HIGH,)}})
    doubled = _moves(tracks, {THERE: {"t": (HIGH,)}, HERE: {"t": (MED, HIGH)}})
    left = _moves(
        [_scanned("t", THERE, energy=1)], {THERE: {"t": (LOW,)}, HERE: {"t": (MED, HIGH)}}
    )
    assert len({alone.digest(), doubled.digest(), left.digest()}) == 3


def test_the_reading_is_asked_of_the_one_resolver_in_either_bucket():
    """No second rule for what a level means: in the bucket the genre names
    the target is adoption's sub, elsewhere it is the same resolver's answer."""
    (entry,) = _adoption([_scanned("t", THERE, energy=8)], {}).entries
    assert adopt_move.reading_target(entry, THERE, DECLARED) == entry.sub == HIGH
    assert (
        adopt_move.reading_target(entry, HERE, DECLARED) == routing.energy_sub(DECLARED, HERE, 8).id
    )
    assert adopt_move.reading_target(entry, "no-such-bucket", DECLARED) == ""
    (blank,) = _adoption([_no_genre("t", energy=None)], {}).entries
    assert adopt_move.reading_target(blank, HERE, DECLARED) == SINK


def test_a_tree_path_move_is_checked_by_the_worker_in_the_bucket_it_names():
    """Asking adoption's bucket and sub of every approved row would refuse a
    move in a bucket the genre does not name as naming another place."""
    tracks = [_scanned("t", THERE, energy=8)]
    start = _adoption(tracks, {HERE: {"t": (MED, HIGH)}, THERE: {"t": (HIGH,)}})
    approved = adopt_move.build_move_plan(start, DECLARED).moves
    assert [move.bucket for move in approved] == [HERE]
    assert move_cli.remaining(approved, start, DECLARED) == (approved, ())
    done = _adoption(tracks, {HERE: {"t": (HIGH,)}, THERE: {"t": (HIGH,)}})
    assert move_cli.remaining(approved, done, DECLARED) == ((), ())

    stale = {
        "another place": _adoption([_scanned("t", THERE, energy=2)], {HERE: {"t": (MED, HIGH)}}),
        "": _adoption([_scanned("t", HERE, energy=1)], {HERE: {"t": (MED, HIGH)}}),
        "holds no sub": _adoption(tracks, {THERE: {"t": (HIGH,)}}),
    }
    for said, current in stale.items():
        cause = _refused(lambda current=current: move_cli.remaining(approved, current, DECLARED))
        assert said in cause.detail["moved_under"]["t"], said


# ---------------------------------------------------------------------------
# The worker's check of each approved row, with no database
# ---------------------------------------------------------------------------


def test_a_sub_class_in_an_approved_row_is_refused_by_what_competes_now():
    current = _adoption([_scanned("t", HERE, energy=8)], {HERE: {"t": (MED,)}})
    (approved,) = adopt_move.build_move_plan(current, DECLARED).moves
    forged = replace(approved, remove=(MED, DERIVED))
    _refused(lambda: move_cli.remaining([forged], current, DECLARED))
    todo, gone = move_cli.remaining([approved], current, DECLARED)
    assert ([move.remove for move in todo], gone) == ([(MED,)], ())


def _approved_over(tracks, held) -> tuple[adopt_plan.AdoptionPlan, tuple[adopt_move.Move, ...]]:
    plan = _adoption(tracks, held)
    return plan, adopt_move.build_move_plan(plan, DECLARED).moves


def test_a_track_a_verdict_withheld_since_the_approval_is_a_stale_decision():
    """The bucket and the sub are unchanged by a verdict, so comparing those
    two alone would perform the move."""
    current, approved = _approved_over([_scanned("t", HERE, energy=8)], {HERE: {"t": (MED,)}})
    (entry,) = current.entries
    withheld = replace(
        entry,
        disposition=adopt_scan.Disposition.WITHHELD,
        holds=(),
        holds_unnamed=(),
        withheld_by=adopt_plan.WITHHELD_BY_VERDICT,
    )
    refused = replace(current, entries=(withheld,))
    assert (refused.entries[0].bucket, refused.entries[0].sub) == (HERE, HIGH)
    cause = _refused(lambda: move_cli.remaining(approved, refused, DECLARED))
    assert "does not move it" in cause.detail["moved_under"]["t"]


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
    cause = _refused(lambda: move_cli.remaining(approved, now, DECLARED))
    assert adopt_move.LEFT_NO_STYLE in cause.detail["moved_under"]["t"]


def test_a_reading_lost_since_the_approval_is_a_stale_decision():
    _plan, approved = _approved_over(
        [_scanned("t", HERE, energy=None)], {HERE: {"t": (SINK, HIGH)}}
    )
    assert approved == ()
    _plan, approved = _approved_over([_scanned("t", HERE, energy=8)], {HERE: {"t": (SINK,)}})
    # The file loses its tag, and the sink is where an untagged track goes.
    now, _none = _approved_over([_scanned("t", HERE, energy=None)], {HERE: {"t": (SINK,)}})
    _refused(lambda: move_cli.remaining(approved, now, DECLARED))


def test_what_is_left_of_a_move_is_narrowed_and_a_finished_one_is_dropped():
    tracks = [_scanned("a", HERE, energy=8), _scanned("b", HERE, energy=8)]
    _start, approved = _approved_over(tracks, {HERE: {"a": (MED,), "b": (MED,)}})
    halfway = _adoption(tracks, {HERE: {"a": (MED, HIGH), "b": (HIGH,)}})
    todo, gone = move_cli.remaining(approved, halfway, DECLARED)
    assert [(m.content_id, m.add, m.remove) for m in todo] == [("a", "", (MED,))]
    assert gone == ()

    without_b = _adoption(tracks[:1], {HERE: {"a": (MED,)}})
    todo, gone = move_cli.remaining(approved, without_b, DECLARED)
    assert ([m.content_id for m in todo], gone) == (["a"], ("b",))

    unread = adopt_plan.build_adoption_plan(tracks, DECLARED, tree=TREE_ID)
    _refused(lambda: move_cli.remaining(approved, unread, DECLARED))


# ---------------------------------------------------------------------------
# A placed library with real tags
# ---------------------------------------------------------------------------

#: Every library :func:`seed_library` built, by what it was built from: the
#: directory holding its database and files, and the tree's root identifier.
_SEEDED_LIBRARIES: dict[tuple, tuple[Path, str]] = {}


def seed_library(cfg, silence: Path, tracks, places, *, on: date, outside=()) -> None:  # noqa: F811
    """A cut over library holding ``tracks`` with real tags, filed in ``places``.

    ``tracks`` is (content id, genre, energy tag or None) per track and
    ``places`` (folder, playlist, content id) per membership, the folder under
    the tree's root unless it is named in ``outside``. REAL CONTAINERS WITH
    REAL TAGS, since a move is a disagreement between a file's tag and its
    sub, and the tree is seeded through the writer's own find or create under
    the declared names, which is what a cutover adopts.

    BUILT ONCE PER MODULE AND COPIED, since the build is most of a test's
    setup: the database and the files are copied into this machine's library
    and each recorded location is rewritten to it, which is all a build leaves
    that depends on where the library is. The cutover is recorded each time.
    """
    from cratekit.core import tags

    tracks, places = tuple(tracks), tuple(places)
    root, db = Path(cfg.library.root), Path(cfg.library.db_path)
    files = [(root / "Music" / f"{content_id}.flac", content_id) for content_id, *_ in tracks]
    key = (silence, tracks, places, tuple(outside))
    if key in _SEEDED_LIBRARIES:
        template, root_id = _SEEDED_LIBRARIES[key]
        shutil.copyfile(template / db.name, db)
        for path, _content_id in files:
            shutil.copyfile(template / path.name, path)
        _sql(
            cfg,
            "UPDATE djmdContent SET FolderPath = ? WHERE ID = ?",
            many=[(adopt_fixtures.recorded_location(root, path.name), cid) for path, cid in files],
        )
    else:
        adopt_fixtures.build(
            cfg, tuple(adopt_fixtures.Track(cid, f"{cid}.flac", genre) for cid, genre, _ in tracks)
        )
        for (path, _content_id), (_cid, _genre, tag) in zip(files, tracks, strict=True):
            shutil.copyfile(silence, path)
            if tag is not None:
                assert tags.write_tags(path, {"energylevel": tag}) is True
        handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
        try:
            tree = rb_writer.ensure_folder(handle, DECLARED.tree.display)
            for folder_display, sub_display, content_id in places:
                parent = None if folder_display in outside else tree
                folder = rb_writer.ensure_folder(handle, folder_display, parent=parent)
                playlist = rb_writer.ensure_playlist(handle, sub_display, folder)
                rb_writer.add_memberships(handle, playlist, [content_id])
            handle.session.commit()
            root_id = str(tree.ID)
        finally:
            rb_writer.close_db(handle)
        template = silence.parent / f"seeded-{len(_SEEDED_LIBRARIES)}"
        template.mkdir()
        for path in (db, *(path for path, _content_id in files)):
            shutil.copyfile(path, template / path.name)
        _SEEDED_LIBRARIES[key] = (template, root_id)
    collection.reset_cache()
    tree_registry.record_cutover(
        cfg, TREE_ID, root_id=root_id, on=on, source=tree_registry.DerivationSource.TAXONOMY
    )


def _sql(cfg, statement: str, *params, many: list | None = None) -> list[tuple]:
    """One statement on the database file in plain SQL, committed: its rows.

    Plain SQL, so what is asserted is what the file holds, the removal marker
    included, whatever a reader in the product does with it.
    """
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        if many is not None:
            conn.executemany(statement, many)
            rows = []
        else:
            rows = conn.execute(statement, params).fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()


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


def _place(sub_id: str, bucket: taxonomy.Bucket | None = None) -> tuple[str, str]:
    return destination(DECLARED, (bucket or _energy_bucket()).id, sub_id)


@pytest.fixture
def moved(machine, silence):  # noqa: F811
    """A cut over library whose tree files tracks where their files do not read."""
    energy, style, other = _energy_bucket(), _style_bucket(), _other_bucket()
    style_genre = next(g for g, sub in style.sub_by_source.map.items() if sub == style.subs[1].id)
    tracks = [(content_id, energy.display, tag) for content_id, tag, _held in _SEEDED]
    places = [(*_place(sub), content_id) for content_id, _tag, held in _SEEDED for sub in held]
    tracks.append(("m-style", style_genre, "8"))
    places.append((*_place(style.subs[0].id, style), "m-style"))
    for content_id, tag, routes, held, elsewhere in _SEEDED_ELSEWHERE:
        tracks.append((content_id, other.display if routes == "other" else "", tag))
        places.extend((*_place(sub), content_id) for sub in held)
        places.extend((*_place(sub, other), content_id) for sub in elsewhere)
    tracks.append((_TWICE, energy.display, "5"))
    places.append((*_place(MED), _TWICE))
    seed_library(machine, silence, tracks, places, on=date(2026, 9, 29))
    # THE SECOND ROW OF ONE PAIR, as rekordbox made them (R-781). The additive
    # writer will not write a pair twice, so it is inserted as a row.
    _sql(
        machine,
        "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, "
        "rb_local_deleted, created_at, updated_at) "
        "SELECT 'twice', PlaylistID, ContentID, 99, 0, created_at, updated_at "
        "FROM djmdSongPlaylist WHERE ContentID = ?",
        _TWICE,
    )
    return machine


def _rows(cfg) -> list[tuple[str, str, str, int]]:
    """Every membership row: track, folder name, playlist name, removal marker."""
    return [
        (str(a), str(b), str(c), int(d))
        for a, b, c, d in _sql(
            cfg,
            "SELECT sp.ContentID, f.Name, p.Name, sp.rb_local_deleted "
            "FROM djmdSongPlaylist sp "
            "JOIN djmdPlaylist p ON p.ID = sp.PlaylistID "
            "JOIN djmdPlaylist f ON f.ID = p.ParentID "
            "ORDER BY sp.ContentID, f.Name, p.Name, sp.rb_local_deleted",
        )
    ]


def _by_marker(cfg, removed: bool) -> dict[str, set[tuple[str, str]]]:
    found: dict[str, set[tuple[str, str]]] = {}
    for content_id, folder, playlist, marker in _rows(cfg):
        if bool(marker) is removed:
            found.setdefault(content_id, set()).add((folder, playlist))
    return found


def _live(cfg) -> dict[str, set[tuple[str, str]]]:
    return _by_marker(cfg, False)


def _removed(cfg) -> dict[str, set[tuple[str, str]]]:
    return _by_marker(cfg, True)


def _shown(verb: list[str]) -> dict:
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    return refused["cause"]["detail"]["shown"]


def _approve_and_run() -> tuple[str, int, dict]:
    _run_id, job_id = approve_and_queue(VERB, GATE)
    code, resumed = drive(_resume(job_id))
    return job_id, code, resumed


def _decided(answer: str) -> tuple[int, dict]:
    """Meet the gate, answer it as a person, and run the verb again on that run."""
    _code, refused = drive(VERB)
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, GATE, answer, "--actor", "a-person"])
    assert decided == OK
    return drive(["--run", run_id, *VERB])


def _no_jobs() -> bool:
    with jobs.open_store() as store:
        return jobs.list_jobs(store) == ()


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
        _energy_bucket().id,
        "",
        [MED],
    )
    assert (elsewhere["holds"], elsewhere["energy"], elsewhere["genre"]) == (
        sorted((MED, HIGH)),
        8,
        _other_bucket().display,
    )
    no_genre = items["m-no-genre"]
    assert (no_genre["bucket"], no_genre["add"], no_genre["remove"], no_genre["genre"]) == (
        _energy_bucket().id,
        "",
        [MED],
        "",
    )
    two = sorted(
        (row["bucket"], row["remove"])
        for row in shown["items"]
        if row["content_id"] == "m-two-buckets"
    )
    assert two == sorted([(_energy_bucket().id, [HIGH]), (_other_bucket().id, [LOW])])

    left = {row["content_id"]: row for row in shown["left"]}
    assert set(left) == _LEFT
    assert left["m-no-reading"]["reason"] == adopt_move.LEFT_NO_READING
    neither = left["m-genre-elsewhere-reads-low"]
    assert (neither["reason"], neither["bucket"], neither["target"], neither["holds"]) == (
        adopt_move.LEFT_NAMES_NEITHER,
        _energy_bucket().id,
        LOW,
        sorted((MED, HIGH)),
    )
    assert (left[_TWICE]["reason"], left[_TWICE]["holds"], left[_TWICE]["target"]) == (
        adopt_move.LEFT_DOUBLED_ROWS,
        [MED],
        MED,
    )
    assert shown["digest"] == move_cli.current_plan(moved, DECLARED).digest()

    # A person reading the gate is shown every move and every track left.
    _code, text = drive_human(VERB)
    for content_id in _MOVED | _LEFT:
        assert f"content_id={content_id}" in text, content_id

    # It takes no inline answer, and a declined gate queues nothing.
    before = _rows(moved)
    code, refused = drive(["-d", f"{GATE}=approve", *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _no_jobs()
    code, envelope = _decided("abort")
    assert code == OK, envelope
    assert envelope["data"]["state"] == "declined"
    assert _no_jobs()
    assert _rows(moved) == before


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(moved, monkeypatch):
    with monkeypatch.context() as patched:
        patched.setattr(session.Acknowledgment, "valid_at", lambda self, moment: False)
        code, refused = drive(VERB)
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert refused["cause"]["detail"]["expired"] is True

    _run_id, job_id = approve_and_queue(VERB, GATE)
    session.ack_path(moved).unlink()
    before = _rows(moved)

    code, refused = drive(VERB)
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert refused["cause"]["reason"] == "backup-acknowledgment-missing"
    assert "shown" not in refused["cause"].get("detail", {})
    assert refused["cause"]["remediation"]["remedy"] == str(Remedy.ACKNOWLEDGE_BACKUP)
    # A resume with none refuses before anything is driven.
    code, refused = drive(_resume(job_id))
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert _rows(moved) == before


# ── the move ────────────────────────────────────────────────────────────────

#: The columns and tables a move must never touch, named one by one so a
#: difference is reported against the column and not against a whole row.
_GUARDED_CONTENT_COLUMNS = (
    "BPM",
    "Rating",
    "KeyID",
    "Analysed",
    "AnalysisDataPath",
    "AnalysisUpdated",
    "CueUpdated",
)
_GUARDED_TABLES = ("djmdCue", "contentCue", "hotCueBanklistCue")
_STAMPED = "ID, PlaylistID, ContentID, TrackNo, UUID, rb_data_status, created_at, "
_STAMPED += "rb_local_deleted, updated_at, rb_local_usn"


def _untouched(cfg) -> dict:
    """Every content row, every guarded column by name and every cue table."""
    return {
        "content": _sql(cfg, "SELECT * FROM djmdContent ORDER BY ID"),
        **{
            name: _sql(cfg, f"SELECT ID, {name} FROM djmdContent ORDER BY ID")
            for name in _GUARDED_CONTENT_COLUMNS
        },
        **{name: _sql(cfg, f"SELECT * FROM {name} ORDER BY ID") for name in _GUARDED_TABLES},
    }


def test_an_approved_move_adds_the_new_sub_and_removes_the_old(moved, monkeypatch):
    """One approved run, read every way a person or rekordbox would read it."""
    from cratekit.adopt import placements as adopt_placements
    from cratekit.core import snapshot, tags
    from cratekit.write import metadata_cli

    before, rows_before, untouched = _live(moved), _rows(moved), _untouched(moved)
    tables = {row[0] for row in _sql(moved, "SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert set(_GUARDED_TABLES) <= tables, sorted(tables)
    assert all(untouched[name] for name in _GUARDED_CONTENT_COLUMNS), "rows to compare"
    stamped = f"SELECT {_STAMPED} FROM djmdSongPlaylist WHERE ContentID = 'm-med-reads-high' "
    (stamp_before,) = _sql(moved, stamped + "ORDER BY created_at, ID")
    withheld = {e.content_id for e in apply_cli.current_plan(moved, DECLARED).held_elsewhere()}
    assert withheld == _WITHHELD_BY_ADOPTION | {"m-no-reading"}
    # R-780: the ones the tree path moves were never on adoption's list.
    assert {"m-genre-elsewhere-reads-high", "m-no-genre", "m-two-buckets"}.isdisjoint(withheld)

    # A move asks nothing about vocals (R-788), so neither read may stop one,
    # and it takes one capture.
    def never(*_args, **_kwargs):
        raise AssertionError("the move verb read the vocals")

    captured = []
    real_capture = snapshot.capture
    with monkeypatch.context() as patched:
        patched.setattr(adopt_placements, "vox_tagged", never)
        patched.setattr(metadata_cli, "load_vocal_threshold", never)
        patched.setattr(
            snapshot, "capture", lambda *a, **k: captured.append(1) or real_capture(*a, **k)
        )
        job_id, code, resumed = _approve_and_run()
    assert code == OK, resumed
    assert len(captured) == 1
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
        "m-candy-only",
        "m-no-reading",
        "m-same",
        "m-genre-elsewhere-reads-low",
        _TWICE,
    ):
        assert after[content_id] == before[content_id], content_id
    # Both rows of the doubled pair are still live.
    assert len([row for row in _rows(moved) if row[0] == _TWICE and not row[3]]) == 2

    # A SOFT DELETE: nine rows marked, four added, none deleted.
    assert removed == {
        "m-med-reads-high": {_place(MED)},
        "m-both-reads-high": {_place(MED)},
        "m-vox-and-med": {_place(MED)},
        "m-sink-now-reads": {_place(SINK)},
        "m-style": {_place(style.subs[0].id, style)},
        "m-genre-elsewhere-reads-high": {_place(MED)},
        "m-no-genre": {_place(MED)},
        "m-two-buckets": {_place(HIGH), _place(LOW, _other_bucket())},
    }
    assert len(_rows(moved)) == len(rows_before) + 4
    # As rekordbox's own removed rows read: the marker set, ``updated_at`` past
    # ``created_at``, the update sequence stamped, the track number kept.
    (stamp_after,) = [r for r in _sql(moved, stamped) if r[0] == stamp_before[0]]
    assert stamp_after[:7] == stamp_before[:7]
    assert (stamp_before[7], stamp_after[7]) == (0, 1)
    assert stamp_after[8] != stamp_before[8] and str(stamp_after[8]) > str(stamp_before[6])
    assert stamp_after[9] is not None and stamp_after[9] != stamp_before[9]
    # No content row, and no tempo, grid, cue or rating value, column by column.
    for name, rows in _untouched(moved).items():
        assert rows == untouched[name], name

    report = artifacts.committed(moved, job_id)[-1]
    assert (report["added"], report["already_present"]) == (4, 5)
    assert (report["removed"], report["already_absent"]) == (9, 0)
    # ONCE PER TRACK, though one of them carried two moves.
    assert sorted(report["moved"]) == sorted(_MOVED)
    assert report["in_both"] == report["untouched"] == report["neither"] == []
    assert report["interrupted"] is False
    summary = resumed["data"]["progress"]["move"]
    assert summary["moved"] == sorted(_MOVED)
    # The summary a person reads names every ending.
    assert {"moved", "in_both", "untouched", "neither", "gone", "skipped", "held_back"} <= set(
        summary
    )
    for name in ("neither", "skipped"):
        assert summary[name] == report[name] == []
    (record,) = [r for r in session.records(moved) if r.workflow == trees.MOVE_WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert record.snapshot_path
    assert (record.change.created, record.change.updated) == (4, 9)
    assert record.sources == {TREE_ID: str(session.SourceState.COMMITTED)}

    # Adoption after the move withholds none of the moved tracks.
    collection.reset_cache()
    plan = apply_cli.current_plan(moved, DECLARED)
    assert {e.content_id for e in plan.held_elsewhere()} == {"m-no-reading"}
    applicable = {entry.content_id for entry in plan.applicable()}
    assert _MOVED - {"m-no-genre"} <= applicable
    # A track with no genre is adoption's open question, not a placed track.
    assert "m-no-genre" not in applicable

    # A second approved run plans nothing and writes nothing.
    rows = _rows(moved)
    shown = _shown(VERB)
    assert shown["items"] == []
    assert shown["counts"]["moves"] == 0
    assert {row["content_id"] for row in shown["left"]} == _LEFT
    code, envelope = _decided("approve")
    assert code == OK, envelope
    assert envelope["data"]["state"] == "no-op"
    assert [w["code"] for w in envelope["warnings"]] == [move_cli.NOTHING_TO_MOVE]
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 1
    assert _rows(moved) == rows

    # A moved track can be moved back: a removed membership is not counted as
    # present, so it gets a live row.
    music = Path(moved.library.root) / "Music"
    assert tags.write_tags(music / "m-med-reads-high.flac", {"energylevel": "5"}) is True
    collection.reset_cache()
    _job_id, code, resumed = _approve_and_run()
    assert code == OK, resumed
    assert _live(moved)["m-med-reads-high"] == {_place(MED)}
    assert _removed(moved)["m-med-reads-high"] == {_place(MED), _place(HIGH)}


# ── a failure between the add and the remove ───────────────────────────────


def _fails(*_args, **_kwargs):
    raise RuntimeError("the disk went away")


def test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes(moved, monkeypatch):
    before = _live(moved)
    _run_id, job_id = approve_and_queue(VERB, GATE)
    with monkeypatch.context() as patched:
        patched.setattr(rb_writer, "remove_memberships", _fails)
        code, failed = drive(_resume(job_id))

    assert code != OK, failed
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
    assert code == OK, resumed
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


def test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised(moved, monkeypatch):
    """The read back is the verdict. A writer that reports no failure over
    tracks still in both subs must not drive the job to succeeded."""
    _run_id, job_id = approve_and_queue(VERB, GATE)
    monkeypatch.setattr(rb_writer, "remove_memberships", lambda *_args, **_kwargs: [])

    code, failed = drive(_resume(job_id))

    assert code != OK, failed
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
    monkeypatch.setattr(rb_writer, "add_memberships", _fails)
    code, failed = drive(_resume(job_id))
    assert code != OK, failed
    assert _rows(moved) == before


# ── what the review found, driven ──────────────────────────────────────────


def _mark_playlist_removed(cfg, sub_id: str) -> None:
    """Mark the first energy bucket's playlist for ``sub_id`` removed, by
    folder as well as by name: the other bucket's namesake stays live."""
    folder, playlist = _place(sub_id)
    changed = _sql(
        cfg,
        "UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE Name = ? AND Attribute = 0 "
        "AND ParentID IN (SELECT ID FROM djmdPlaylist WHERE Name = ?) RETURNING ID",
        playlist,
        folder,
    )
    assert len(changed) == 1


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
    assert code == OK, resumed

    found = _sql(
        moved,
        "SELECT p.rb_local_deleted, COUNT(*) FROM djmdSongPlaylist sp "
        "JOIN djmdPlaylist p ON p.ID = sp.PlaylistID "
        "WHERE p.Name = ? AND sp.rb_local_deleted = 0 AND sp.ContentID IN (?, ?, ?) "
        "GROUP BY p.rb_local_deleted ORDER BY p.rb_local_deleted",
        _place(HIGH)[1],
        "m-med-reads-high",
        "m-both-reads-high",
        "m-vox-and-med",
    )
    # Three additions in the live playlist. The one row in the removed playlist
    # is the row the fixture seeded there, which nothing here touches.
    assert found == [(0, 3), (1, 1)]


def test_a_sub_held_only_through_a_removed_playlist_is_not_planned_for_removal(moved):
    _mark_playlist_removed(moved, MED)
    shown = _shown(VERB)
    # The first bucket's Med is not a place, so every double through it is
    # gone. The other bucket's Med is live, so m-two-buckets keeps its move there.
    assert {item["content_id"] for item in shown["items"]} == {
        "m-sink-now-reads",
        "m-style",
        "m-two-buckets",
    }
    assert [row["bucket"] for row in shown["items"] if row["content_id"] == "m-two-buckets"] == [
        _other_bucket().id
    ]
    before = [row for row in _rows(moved) if row[2] == _place(MED)[1]]
    _job_id, code, resumed = _approve_and_run()
    assert code == OK, resumed
    assert all(not row[3] for row in before)
    unmarked = [row for row in _rows(moved) if row[2] == _place(MED)[1] and not row[3]]
    assert set(before) <= set(unmarked)


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

    assert code != OK, failed
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


def test_a_membership_that_cannot_say_is_unproven_and_is_refused_by_a_reader():
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
    _refused(lambda: rebuild.read_tree(Db(), "root"), "soft-delete-marker-unreadable")


def _plan_of(job_id: str) -> dict:
    with jobs.open_store() as store:
        return dict(jobs.get(store, job_id).payload[move_cli.PLAN_KEY])


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

    # Nor are rows under a digest that does not describe them ever shown.
    document = _plan_of(job_id)
    document["moves"] = document["moves"][:1]
    _requeued(job_id, **{move_cli.PLAN_KEY: document})
    code, envelope = drive(["adopt", "move", "--job", job_id])
    assert code == STALE, envelope
    assert "shown" not in envelope["cause"].get("detail", {})
    assert _rows(moved) == before


# ── the endings a queued verb owes ─────────────────────────────────────────


def test_a_parked_move_leaves_blocked_and_non_zero(moved, monkeypatch):
    """R-290 for a key ``tests/test_job_outcome.py`` cannot drive, which names
    this function as the place the key is covered."""
    from cratekit.core.cause import refuse

    def parks(job, item, cfg):
        raise jobs.Parked(refuse("provider-blocked", "the run must stop", origin=("test",)).cause)

    before = _rows(moved)
    _run_id, job_id = approve_and_queue(VERB, GATE)
    monkeypatch.setattr(handlers, "resolve", lambda _key: parks)

    code, envelope = drive(_resume(job_id))

    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.BLOCKED, envelope
    assert envelope["outcome"] == "blocked", envelope
    assert code != OK, envelope
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
    assert code != OK
    assert envelope["cause"]["reason"] == "internal-error"
    assert job.job_id in envelope["cause"]["message"]


# ── the worker's own checks ────────────────────────────────────────────────


def _worker(job_id: str):
    handler = handlers.resolve(registry.entry("adopt.move").handler_key)
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[0]
    return handler, job, item


def _worker_refuses(cfg, job_id: str, reason: str = "decision-stale", **changed):
    """Run the worker over the job, its payload edited by ``changed``: it
    refuses with ``reason`` and writes nothing."""
    before = _rows(cfg)
    handler, job, item = _requeued(job_id, **changed) if changed else _worker(job_id)
    cause = _refused(lambda: handler(job, item, jobs.frozen_config(job)), reason)
    assert _rows(cfg) == before
    return cause


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
    cause = _worker_refuses(moved, job_id)
    assert set(cause.detail["moved_under"]) == {"m-med-reads-high"}


def test_a_reading_that_changed_after_the_approval_is_a_stale_decision(moved):
    from cratekit.core import tags

    _run_id, job_id = approve_and_queue(VERB, GATE)
    music = Path(moved.library.root) / "Music"
    assert tags.write_tags(music / "m-med-reads-high.flac", {"energylevel": "1"}) is True
    collection.reset_cache()
    _worker_refuses(moved, job_id)


def test_a_track_approved_as_in_its_target_that_left_it_is_a_stale_decision(moved):
    """Its one live place would otherwise be removed."""
    _run_id, job_id = approve_and_queue(VERB, GATE)
    _sql(
        moved,
        "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE ContentID = ? "
        "AND PlaylistID IN (SELECT ID FROM djmdPlaylist WHERE Name = ?)",
        "m-both-reads-high",
        _place(HIGH)[1],
    )
    _worker_refuses(moved, job_id)


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


def test_the_worker_refuses_rows_that_are_not_approved_and_a_job_naming_nobody(moved):
    run_id, job_id = approve_and_queue(VERB, GATE)
    with jobs.open_store() as store:
        payload = jobs.get(store, job_id).payload
    # The approving actor travels in the payload, and the resume carries the
    # run that holds the approval.
    assert payload[move_cli.ACTOR_KEY] == "a-person"
    assert payload["digest"] == payload[move_cli.PLAN_KEY]["digest"]
    assert _resume(job_id) == ["--run", run_id, "adopt", "move", "--job", job_id]

    _worker_refuses(moved, job_id, "decision-required", **{move_cli.ACTOR_KEY: " "})
    document = _plan_of(job_id)
    document["moves"] = [
        {**row, "remove": [DERIVED]} if row["content_id"] == "m-vox-and-med" else row
        for row in document["moves"]
    ]
    _worker_refuses(moved, job_id, **{move_cli.ACTOR_KEY: "a-person", move_cli.PLAN_KEY: document})


# ---------------------------------------------------------------------------
# The writer's own guards
# ---------------------------------------------------------------------------


def _write(cfg, moves):
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


def _to_high(content_id: str = "m-med-reads-high") -> list[trees.MembershipMove]:
    return [trees.MembershipMove(content_id, _place(HIGH), (_place(MED),))]


def test_a_person_stopping_the_removals_is_an_interrupt_and_not_a_failure(moved, monkeypatch):
    def stopped(*_args, **_kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(rb_writer, "remove_memberships", stopped)
    with pytest.raises(KeyboardInterrupt):
        _write(moved, _to_high())
    assert _live(moved)["m-med-reads-high"] == {_place(MED), _place(HIGH)}
    assert _removed(moved) == {}


def test_the_fingerprint_is_taken_after_each_commit_that_landed(moved, monkeypatch):
    from cratekit.core import convergence

    taken: list[int] = []
    real = convergence.record_fingerprint

    def counting(cfg, db, **kwargs):
        taken.append(1)
        return real(cfg, db, **kwargs)

    monkeypatch.setattr(convergence, "record_fingerprint", counting)
    with monkeypatch.context() as patched:
        patched.setattr(rb_writer, "remove_memberships", _fails)
        with pytest.raises(trees.MoveInterrupted) as raised:
            _write(moved, _to_high())
    assert (raised.value.report.added, raised.value.report.adds_committed) == (1, True)
    assert isinstance(raised.value.__cause__, RuntimeError)
    assert len(taken) == 1, "the additions landed and the reading was not moved"

    _write(moved, _to_high())
    # Nothing to add the second time, so one more reading, for the removal.
    assert len(taken) == 2


def test_a_track_not_in_its_target_has_nothing_removed(moved, monkeypatch):
    """Never in neither: the removal waits on the addition being in the database."""
    before = _rows(moved)
    monkeypatch.setattr(rb_writer, "add_memberships", lambda *_args, **_kwargs: [])
    report = _write(moved, _to_high())
    assert report.held_back == ("m-med-reads-high",)
    assert (report.added, report.removed) == (0, 0)
    assert _live(moved)["m-med-reads-high"] == {_place(MED)}
    assert [row for row in _rows(moved) if row[3]] == [row for row in before if row[3]] == []


def test_a_track_with_no_live_collection_row_is_skipped_whole(moved):
    _sql(moved, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = 'm-med-reads-high'")
    before = _rows(moved)
    report = _write(moved, [*_to_high(), *_to_high("nobody")])
    assert report.skipped == ("m-med-reads-high", "nobody")
    assert (report.added, report.removed) == (0, 0)
    assert _rows(moved) == before


def test_a_removal_from_a_playlist_that_is_not_there_creates_none(moved):
    count = "SELECT COUNT(*) FROM djmdPlaylist"
    before = _sql(moved, count)
    report = _write(moved, [trees.MembershipMove("m-same", _place(MED), (_place(LOW),))])
    assert (report.removed, report.already_absent, report.already_present) == (0, 1, 1)
    assert _sql(moved, count) == before
    # And the target is never removed from, even when a move names it.
    report = _write(moved, [trees.MembershipMove("m-same", _place(MED), (_place(MED),))])
    assert report.removed == 0
    assert _live(moved)["m-same"] == {_place(MED)}


def test_a_doubled_membership_leaves_in_one_move(moved):
    _sql(
        moved,
        "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, "
        "rb_local_deleted, created_at, updated_at) "
        "SELECT 'doubled', PlaylistID, ContentID, 99, 0, created_at, updated_at "
        "FROM djmdSongPlaylist WHERE ContentID = 'm-med-reads-high'",
    )
    report = _write(moved, _to_high())
    assert report.removed == 2
    assert _live(moved)["m-med-reads-high"] == {_place(HIGH)}


def _move_tree(cfg, **overrides):
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        trees.move_tree_membership(
            cfg, handle, tree_id=TREE_ID, registry=tree_registry.read(cfg), moves=[],
            root_exists=lambda _root: True, **overrides,
        )  # fmt: skip
    finally:
        rb_writer.close_db(handle)


def test_an_empty_watch_is_refused(moved):
    with pytest.raises(ValueError, match="analysis_roots is empty"):
        _move_tree(moved, analysis_roots=[])


def test_a_tree_still_on_the_bridge_is_refused(machine):  # noqa: F811
    with pytest.raises(tree_registry.TreeModeRefused):
        _move_tree(machine, analysis_roots=[Path(machine.library.root)])


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


def _guarded(cfg, change, **removals):
    """Make ``change`` on a handle and commit it guarded: the refusal's cause,
    or None when the commit landed."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        change(handle)
        rb_writer.commit_guarded(handle, **removals)
    except rb_writer.RekordboxUnavailable as exc:
        return exc.cause
    finally:
        rb_writer.close_db(handle)
    return None


_ADMITTED = {"removals": rb_writer.REMOVABLE_TABLES}


def test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back(moved):
    before = _rows(moved)
    refused = _guarded(moved, _mark_one_removed)
    assert refused.reason == "whitelist-violation" and "soft delete marker" in refused.message
    assert _rows(moved) == before
    # A commit that admits the removal lands it.
    assert _guarded(moved, _mark_one_removed, **_ADMITTED) is None
    assert _removed(moved) == {"m-med-reads-high": {_place(MED)}}


def test_an_admitted_commit_refuses_a_removed_collection_row_or_a_hard_delete(moved):
    def removes_the_track(handle):
        setattr(handle.get_content(ID="m-med-reads-high"), rb_writer.SOFT_DELETE_COLUMN, 1)

    def deletes_the_row(handle):
        (song,) = list(handle.get_playlist_songs(ContentID="m-med-reads-high"))
        handle.delete(song)

    before = _rows(moved)
    refused = _guarded(moved, removes_the_track, **_ADMITTED)
    assert refused.reason == "whitelist-violation" and "djmdContent" in refused.message
    assert _sql(
        moved, "SELECT rb_local_deleted FROM djmdContent WHERE ID = 'm-med-reads-high'"
    ) == [(0,)]
    assert "additive-only" in _guarded(moved, deletes_the_row, **_ADMITTED).message
    assert _rows(moved) == before


def test_the_additive_membership_writer_refuses_a_removal_in_its_session(moved, monkeypatch):
    """The other writer's own session, and the move's own first commit, with a
    removal slipped in: only the move's second commit admits one."""
    before = _rows(moved)
    real = rb_writer.add_memberships

    def adds_and_removes(db, playlist, content_ids):
        _mark_one_removed(db)
        return real(db, playlist, content_ids)

    monkeypatch.setattr(rb_writer, "add_memberships", adds_and_removes)
    handle = rb_writer.open_db(rb_writer.live_db_path(moved), unlock=False, cfg=moved)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        location = adopt_fixtures.recorded_location(Path(moved.library.root), "m-same.flac")
        with pytest.raises(rb_writer.RekordboxUnavailable) as raised:
            trees.write_tree_membership(
                moved,
                handle,
                tree_id=TREE_ID,
                registry=tree_registry.read(moved),
                plan={_place(LOW): [location]},
                rows=collection.read_collection(moved),
                root_exists=lambda root_id: root_id in known,
                analysis_roots=[Path(moved.library.root)],
            )
        assert raised.value.cause.reason == "whitelist-violation"
    finally:
        rb_writer.close_db(handle)
    assert _rows(moved) == before
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
        playlist = next(row for row in handle.get_playlist(Name=_place(MED)[1]))
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
        _refused(lambda row=row: rb_writer.membership_removed(row), "soft-delete-marker-unreadable")


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
    # U219 gave the resort a plan gate of its own, over the tracks it adds,
    # and it is still not this verb's: it approves adds, never a move.
    (plan,) = [spec for spec in resort.gates if spec.digest_source == "plan"]
    assert (plan.name, plan.options) == ("route.resort.apply", ("apply", "abort"))
