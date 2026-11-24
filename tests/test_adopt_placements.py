"""R-731: adoption withholds a track that already holds a competing place.

The pure halves: what competes, what the plan does with a track holding one,
and how a tree already read becomes the plan's value; the database read and the
apply are in ``tests/test_adopt_workers.py``. Identifiers are derived from the
shipped taxonomy. D1 applies.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from cratekit.adopt import placements as adopt_placements
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.core import convergence, routing, taxonomy
from cratekit.write import rebuild
from cratekit.write.routing_pass import destination
from tests.test_adopt_move import HIGH, LOW, MED, SINK, _scanned
from tests.test_adopt_move import _no_genre as _needs_genre
from tests.test_adopt_move import _pure_energy_bucket as _energy_bucket
from tests.test_adopt_workers import _style_bucket

TREE_ID = "shelf_stack"
DECLARED = taxonomy.default_taxonomy()


def _held(bucket: str, **tracks: tuple[str, ...]) -> adopt_plan.Placements:
    return adopt_plan.Placements(read=True, held={bucket: dict(tracks)})


def _plan(tracks, placements=adopt_plan.UNREAD) -> adopt_plan.AdoptionPlan:
    return adopt_plan.build_adoption_plan(tracks, DECLARED, tree=TREE_ID, placements=placements)


def _only(plan: adopt_plan.AdoptionPlan) -> adopt_plan.PlanEntry:
    (entry,) = plan.entries
    return entry


def _recorded(bucket: str) -> convergence.TreeConvergence:
    """A record naming node ``f1``, ``p1`` as where ``bucket``'s Med was written."""
    node = convergence.DestinationNode(bucket=bucket, sub=MED, folder_id="f1", playlist_id="p1")
    return convergence.TreeConvergence(tree_id=TREE_ID, nodes=(node,))


# ── what the taxonomy says competes ────────────────────────────────────────


def test_the_bands_and_the_no_reading_sub_compete_in_an_energy_bucket():
    kind, subs = routing.competing_subs(DECLARED, _energy_bucket().id)
    assert kind is routing.Competing.BAND
    assert subs == {band.id for band in DECLARED.energy.bands} | {SINK}


def test_the_style_subs_compete_where_a_bucket_has_no_energy_dimension():
    bucket = _style_bucket()
    kind, subs = routing.competing_subs(DECLARED, bucket.id)
    assert kind is routing.Competing.STYLE
    # R-797: a former place still held for a bucket that left competes too
    # (test_adopt_former_place.py), read off the declarations.
    former = {
        place.id
        for declarer in DECLARED.buckets
        for place in declarer.formerly
        if bucket.id in (declarer.id, place.bucket)
    }
    assert subs == {sub.id for sub in bucket.subs} | former
    assert not subs & {band.id for band in DECLARED.energy.bands}


def test_a_manual_or_derived_sub_never_competes():
    classes = {entry.id for entry in DECLARED.sub_classes}
    assert {entry.policy for entry in DECLARED.sub_classes} == set(taxonomy.SubPolicy), (
        "the shipped template must declare a sub of each policy for this to mean anything"
    )
    for bucket in DECLARED.buckets:
        _kind, subs = routing.competing_subs(DECLARED, bucket.id)
        assert not subs & classes, bucket.id


def test_every_sub_routing_can_name_is_one_of_its_buckets_competing_subs():
    """A sub routing can return that the set misses would be filed twice unsaid."""
    for bucket in DECLARED.buckets:
        _kind, subs = routing.competing_subs(DECLARED, bucket.id)
        for level in (None, *range(1, DECLARED.energy.scale_max + 1)):
            for genre in ("", bucket.display, *(sub.display for sub in bucket.subs)):
                named = routing.energy_sub(DECLARED, bucket.id, level, source_genre=genre)
                if named is not None:
                    assert named.id in subs, (bucket.id, level, genre)


# ── what the plan does with a track that holds a place ─────────────────────


def test_a_track_in_one_band_whose_file_reads_another_is_withheld_and_listed():
    bucket = _energy_bucket().id
    plan = _plan([_scanned("t", bucket, energy=8)], _held(bucket, t=(MED,)))
    entry = _only(plan)

    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert not entry.applicable
    assert (entry.bucket, entry.sub, entry.holds, entry.withheld_by) == (
        bucket,
        HIGH,
        (MED,),
        "band",
    )
    assert plan.applicable() == ()
    assert plan.withheld_by_placement() == {"total": 1, "band": 1, "style": 0}
    assert adopt_plan.to_json(plan)["held_elsewhere"] == [
        {
            "content_id": "t",
            "location": "/library/Music/t.flac",
            "bucket": bucket,
            "kind": "band",
            "holds": [MED],
            "holds_under_another_name": [],
            "planned": HIGH,
            "energy": 8,
            "energy_unreadable": False,
        }
    ]


_B = _energy_bucket().id
_WITHHELD, _ROUTE = adopt_scan.Disposition.WITHHELD, adopt_scan.Disposition.ROUTE

#: One track in the energy bucket: its reading, the places it holds, the
#: disposition the plan gives it and the entry's fields that follow.
_ONE_TRACK = {
    "withheld-keeps-its-identifier": (
        8, _held(_B, t=(MED,)), _WITHHELD,
        {"entry_id": adopt_plan.entry_id_for(TREE_ID, "t", _B, HIGH)},
    ),
    "sink-whose-file-now-reads": (
        5, _held(_B, t=(SINK,)), _WITHHELD, {"sub": MED, "holds": (SINK,)},
    ),
    "band-whose-file-has-no-reading": (
        None, _held(_B, t=(HIGH,)), _WITHHELD, {"sub": SINK, "holds": (HIGH,), "energy": None},
    ),
    # The live library holds 37 of these; the writer reports the row present.
    "two-bands-one-the-plan-names": (8, _held(_B, t=(HIGH, MED)), _ROUTE, {}),
    "two-bands-and-a-third-named": (
        1, _held(_B, t=(HIGH, MED)), _WITHHELD, {"holds": tuple(sorted((HIGH, MED)))},
    ),
    "unread-tree-carrying-held-subs": (
        8, adopt_plan.Placements(read=False, held={_B: {"t": (MED,)}}), _ROUTE, {},
    ),
    "the-planned-sub-under-another-name-only": (
        8,
        adopt_plan.Placements(read=True, held={_B: {"t": (HIGH,)}}, unnamed={_B: {"t": (HIGH,)}}),
        _WITHHELD, {"sub": HIGH, "holds": (HIGH,), "holds_unnamed": (HIGH,)},
    ),
    # ``unnamed`` is a part of ``held``, so one without the other shows nothing.
    "an-unnamed-sub-it-does-not-hold": (
        8, adopt_plan.Placements(read=True, unnamed={_B: {"t": (HIGH,)}}), _ROUTE, {},
    ),
    # The plan asks the taxonomy itself, even when handed a held sub class.
    **{
        f"only-in-sub-class-{entry.id}": (8, _held(_B, t=(entry.id,)), _ROUTE, {"sub": HIGH})
        for entry in DECLARED.sub_classes
    },
}  # fmt: skip


@pytest.mark.parametrize("case", sorted(_ONE_TRACK))
def test_a_track_holding_a_place_is_withheld_only_where_it_competes(case):
    energy, placements, disposition, expected = _ONE_TRACK[case]
    entry = _only(_plan([_scanned("t", _B, energy=energy)], placements))
    assert entry.disposition is disposition
    assert {name: getattr(entry, name) for name in expected} == expected


def test_a_track_in_no_sub_of_the_bucket_is_added_as_before():
    bucket = _energy_bucket().id
    other = next(b.id for b in DECLARED.buckets if b.id != bucket)
    plan = _plan(
        [_scanned("t", bucket, energy=8)],
        adopt_plan.Placements(read=True, held={other: {"t": (MED,)}, bucket: {"u": (MED,)}}),
    )
    entry = _only(plan)
    assert entry.disposition is adopt_scan.Disposition.ROUTE
    assert (entry.sub, entry.holds, entry.withheld_by) == (HIGH, (), "")
    assert plan.withheld_by_placement()["total"] == 0


def test_a_track_in_one_style_sub_is_withheld_from_another():
    bucket = _style_bucket()
    first, second = bucket.subs[0], bucket.subs[1]
    genre = next(source for source, sub in bucket.sub_by_source.map.items() if sub == second.id)
    plan = _plan([_scanned("t", bucket.id, energy=8, genre=genre)], _held(bucket.id, t=(first.id,)))
    entry = _only(plan)
    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.sub, entry.holds, entry.withheld_by) == (second.id, (first.id,), "style")
    assert plan.withheld_by_placement() == {"total": 1, "band": 0, "style": 1}


def test_a_track_already_in_the_sub_the_plan_names_is_not_withheld():
    bucket = _energy_bucket().id
    plan = _plan([_scanned("t", bucket, energy=8)], _held(bucket, t=(HIGH,)))
    entry = _only(plan)
    assert entry.disposition is adopt_scan.Disposition.ROUTE
    assert adopt_plan.to_json(plan)["held_elsewhere"] == []


# ── the digest and the unread tree ─────────────────────────────────────────


def test_the_digest_differs_between_a_plan_with_a_withheld_entry_and_one_without():
    bucket = _energy_bucket().id
    tracks = [_scanned("t", bucket, energy=8), _scanned("u", bucket, energy=8)]
    nothing_held = adopt_plan.Placements(read=True)
    assert _plan(tracks, _held(bucket, t=(MED,))).digest() != _plan(tracks, nothing_held).digest()


def test_the_digest_moves_when_a_withheld_track_is_moved_to_another_band():
    bucket = _energy_bucket().id
    tracks = [_scanned("t", bucket, energy=8)]
    assert (
        _plan(tracks, _held(bucket, t=(MED,))).digest()
        != _plan(tracks, _held(bucket, t=(LOW,))).digest()
    )


def test_a_tree_nobody_read_is_a_different_plan_from_a_tree_holding_nothing():
    bucket = _energy_bucket().id
    tracks = [_scanned("t", bucket, energy=8)]
    unread, empty = _plan(tracks), _plan(tracks, adopt_plan.Placements(read=True))

    assert [entry.disposition for entry in unread.entries] == [adopt_scan.Disposition.ROUTE]
    assert adopt_plan.to_json(unread)["placements"] == "unread"
    assert adopt_plan.to_json(empty)["placements"] == "read"
    assert unread.digest() != empty.digest()


# ── the verdict paths keep what the plan read ──────────────────────────────


def test_a_genre_answered_later_is_withheld_over_the_place_the_track_holds():
    bucket = _energy_bucket().id
    plan = _plan([_needs_genre("t", energy=8)], _held(bucket, t=(MED,)))
    answered = adopt_plan.with_verdicts(plan, {"t": bucket}, DECLARED)
    entry = _only(answered)

    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.bucket, entry.sub, entry.holds, entry.withheld_by) == (
        bucket,
        HIGH,
        (MED,),
        "band",
    )
    assert answered.placements == plan.placements


def test_a_genre_answered_later_routes_a_track_that_holds_nothing():
    bucket = _energy_bucket().id
    plan = _plan([_needs_genre("t", energy=8)], adopt_plan.Placements(read=True))
    entry = _only(adopt_plan.with_verdicts(plan, {"t": bucket}, DECLARED))
    assert entry.disposition is adopt_scan.Disposition.ROUTE
    assert entry.sub == HIGH


def test_a_collision_verdict_withholds_under_its_own_reason_and_own_count():
    bucket = _energy_bucket()
    folder = adopt_plan.ExistingFolder(
        node_id="n1", display=bucket.display, content_ids=("stranger",)
    )
    plan = adopt_plan.build_adoption_plan(
        [_scanned("t", bucket.id, energy=8), _scanned("u", bucket.id, energy=8)],
        DECLARED,
        tree=TREE_ID,
        existing=[folder],
        placements=_held(bucket.id, t=(MED,)),
    )
    assert [item.strangers for item in plan.collisions] == [1]

    refused = adopt_plan.with_collision_verdicts(plan, {"n1": adopt_plan.COLLISION_SEPARATE})
    by_id = {entry.content_id: entry for entry in refused.entries}
    assert by_id["t"].withheld_by == "band"
    assert by_id["u"].withheld_by == adopt_plan.WITHHELD_BY_VERDICT
    assert refused.counts()["withheld"] == 2
    assert refused.withheld_by_placement() == {"total": 1, "band": 1, "style": 0}
    assert [row["content_id"] for row in adopt_plan.to_json(refused)["held_elsewhere"]] == ["t"]
    assert refused.placements == plan.placements


def test_a_track_the_plan_withheld_is_not_a_stranger_in_its_own_folder():
    bucket = _energy_bucket()
    folder = adopt_plan.ExistingFolder(node_id="n1", display=bucket.display, content_ids=("t", "u"))
    plan = adopt_plan.build_adoption_plan(
        [_scanned("t", bucket.id, energy=8), _scanned("u", bucket.id, energy=8)],
        DECLARED,
        tree=TREE_ID,
        existing=[folder],
        placements=_held(bucket.id, t=(MED,)),
    )
    assert plan.collisions == ()


# ── a tree already read becomes the value the plan takes ───────────────────


def _node(
    bucket: str, sub: str, *content_ids: str, ids=("f1", "p1"), names=None, doubled=()
) -> rebuild.TreeNode:
    folder, playlist = names or destination(DECLARED, bucket, sub)
    return rebuild.TreeNode(
        folder_id=ids[0],
        folder_display=folder,
        playlist_id=ids[1],
        playlist_display=playlist,
        content_ids=frozenset(content_ids),
        doubled=frozenset(doubled),
    )


_RENAMED = ("Renamed folder", "Renamed list")

#: Nodes read off the energy bucket, the convergence record beside them, and
#: what the placements answer: (method, track) to its value.
_READ_BACK = {
    "declared-names": (
        [_node(_B, MED, "t", "u")], None,
        {("holds", "t"): (MED,), ("holds", "absent"): ()},
    ),
    "recorded-node-under-the-declared-names": (
        [_node(_B, MED, "t")], _recorded(_B),
        {("holds", "t"): (MED,), ("holds_unnamed", "t"): ()},
    ),
    "one-sub-under-both-names": (
        [_node(_B, MED, "t", "u", names=_RENAMED), _node(_B, MED, "t", ids=("f2", "p2"))],
        _recorded(_B),
        {("holds", "t"): (MED,), ("holds_unnamed", "t"): (),
         ("holds", "u"): (MED,), ("holds_unnamed", "u"): (MED,)},
    ),
    "two-nodes-for-one-destination": (
        [_node(_B, MED, "t", ids=("f1", "p1")), _node(_B, MED, "u", ids=("f2", "p2"))], None,
        {("holds", "t"): (MED,), ("holds", "u"): (MED,)},
    ),
    "two-bands": (
        [_node(_B, MED, "t", ids=("f1", "p1")), _node(_B, HIGH, "t", ids=("f1", "p2"))], None,
        {("holds", "t"): tuple(sorted((MED, HIGH))), ("holds_doubled", "t"): ()},
    ),
    # R-781's shape, carried rather than lost in the set (R-780 lists it).
    "a-pair-held-by-two-rows": (
        [_node(_B, MED, "t", "u", doubled=("t",))], None,
        {("holds", "t"): (MED,), ("holds_doubled", "t"): (MED,), ("holds", "u"): (MED,),
         ("holds_doubled", "u"): (), ("holds_doubled", "absent"): ()},
    ),
    "two-playlists-for-one-sub-are-not-a-double": (
        [_node(_B, MED, "t", ids=("f1", "p1")), _node(_B, MED, "t", ids=("f2", "p2"))], None,
        {("holds", "t"): (MED,), ("holds_doubled", "t"): ()},
    ),
    "a-double-in-a-renamed-recorded-node": (
        [_node(_B, MED, "t", names=_RENAMED, doubled=("t",))], _recorded(_B),
        {("holds_doubled", "t"): (MED,)},
    ),
}  # fmt: skip


@pytest.mark.parametrize("case", sorted(_READ_BACK))
def test_a_tree_read_back_holds_what_its_nodes_name(case):
    nodes, record, expected = _READ_BACK[case]
    found = adopt_placements.placements_from(DECLARED, nodes, record)
    assert found.read is True
    assert {key: getattr(found, key[0])(_B, key[1]) for key in expected} == expected


def test_a_band_label_a_bucket_overrides_still_resolves_to_the_band():
    bucket = next(b for b in DECLARED.buckets if b.energy.band_display)
    names = destination(DECLARED, bucket.id, MED)
    assert names[1] != next(b.display for b in DECLARED.energy.bands if b.id == MED)
    found = adopt_placements.placements_from(DECLARED, [_node(bucket.id, MED, "t")], None)
    assert found.holds(bucket.id, "t") == (MED,)


def test_a_sub_class_playlist_and_a_hand_made_one_are_not_places():
    bucket = _energy_bucket()
    nodes = [
        _node(bucket.id, entry.id, "t", ids=("f1", f"p-{entry.id}"))
        for entry in DECLARED.sub_classes
    ]
    nodes.append(_node(bucket.id, MED, "t", ids=("f1", "p9"), names=(bucket.display, "My picks")))
    nodes.append(_node(bucket.id, MED, "t", ids=("f9", "p8"), names=("Not a bucket", "Med")))
    assert adopt_placements.placements_from(DECLARED, nodes, None).held == {}


def test_a_renamed_node_is_resolved_through_its_recorded_identifier():
    bucket = _energy_bucket().id
    record = _recorded(bucket)
    renamed = _node(bucket, MED, "t", names=("Renamed folder", "Renamed list"))
    assert adopt_placements.placements_from(DECLARED, [renamed], None).held == {}
    found = adopt_placements.placements_from(DECLARED, [renamed], record)
    assert found.holds(bucket, "t") == (MED,)
    assert found.holds_unnamed(bucket, "t") == (MED,)


def test_a_double_in_a_playlist_that_is_not_a_place_is_not_carried():
    bucket = _energy_bucket()
    hand_made = _node(
        bucket.id, MED, "t", ids=("f1", "p9"), names=(bucket.display, "My picks"), doubled=("t",)
    )
    sub_class = [
        _node(bucket.id, entry.id, "t", ids=("f1", f"p-{entry.id}"), doubled=("t",))
        for entry in DECLARED.sub_classes
    ]
    found = adopt_placements.placements_from(DECLARED, [hand_made, *sub_class], None)
    assert found.held == {} and found.doubled == {}


# ── a place the writer cannot see, and a screen the digest covers ──────────


def test_the_digest_covers_every_field_the_review_list_shows():
    """One changed field at a time, over a closed list a new screen field must join."""
    bucket = _energy_bucket().id
    held = _held(bucket, t=(MED,))
    shown = _scanned("t", bucket, energy=8)
    base = _plan([shown], held)
    renamed = adopt_plan.Placements(
        read=True, held={bucket: {"t": (MED,)}}, unnamed={bucket: {"t": (MED,)}}
    )
    changed = {
        "location": _plan([replace(shown, recorded="/library/Music/moved.flac")], held),
        "energy": _plan([replace(shown, energy=9)], held),
        "energy_unreadable": _plan([replace(shown, energy_unreadable=True)], held),
        "holds": _plan([shown], _held(bucket, t=(LOW,))),
        "holds_under_another_name": _plan([shown], renamed),
    }
    (row,) = adopt_plan.to_json(base)["held_elsewhere"]
    for name, plan in changed.items():
        (other,) = adopt_plan.to_json(plan)["held_elsewhere"]
        assert {key for key in row if row[key] != other[key]} == {name}, name
        assert plan.digest() != base.digest(), name
    # THE REST ARE THE ENTRY'S IDENTITY, which the digest has always covered.
    assert set(row) == set(changed) | {"content_id", "bucket", "kind", "planned"}


# ── a template whose sub class shares a band's identifier ──────────────────


def _clashing() -> taxonomy.Taxonomy:
    """The shipped taxonomy with a sub class under a band's identifier, as a person's can be."""
    clash = taxonomy.SubClass(id=HIGH, display="Peak", policy=taxonomy.SubPolicy.MANUAL)
    return replace(DECLARED, sub_classes=(*DECLARED.sub_classes, clash))


def test_a_sub_class_is_removed_from_the_bands_by_identifier():
    _kind, subs = routing.competing_subs(_clashing(), _energy_bucket().id)
    assert HIGH not in subs
    assert {LOW, MED, SINK} <= subs


def test_a_planned_sub_outside_the_competing_set_is_never_withheld():
    bucket = _energy_bucket().id
    plan = adopt_plan.build_adoption_plan(
        [_scanned("t", bucket, energy=8)],
        _clashing(),
        tree=TREE_ID,
        placements=_held(bucket, t=(MED,)),
    )
    entry = _only(plan)
    assert (entry.sub, entry.disposition) == (HIGH, adopt_scan.Disposition.ROUTE)
