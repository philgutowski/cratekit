"""R-731: adoption withholds a track that already holds a competing place.

The plan placed each track by genre and energy reading and never read the tree,
and the writer is add only, so 569 of 700 additions on a copy of a real library
were a second energy band beside the one the track held. This module holds the
three pure halves of the fix: what the taxonomy says competes, what the plan
does with a track that holds one, and how a tree already read becomes the value
the plan takes. The read off a real database and the approved apply are driven
in ``tests/test_adopt_workers.py``.

Every expected identifier is derived from the shipped taxonomy's own
declarations rather than spelled, so a template that moves does not leave a
test asserting a name nobody declares.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
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

TREE_ID = "shelf_stack"
DECLARED = taxonomy.default_taxonomy()


def _energy_bucket() -> taxonomy.Bucket:
    """A bucket the shipped template splits by energy."""
    return next(
        bucket
        for bucket in DECLARED.buckets
        if bucket.sub_by_source is None and bucket.energy.enabled
    )


def _style_bucket() -> taxonomy.Bucket:
    """A bucket with no energy dimension and more than one style sub."""
    return next(
        bucket
        for bucket in DECLARED.buckets
        if not bucket.energy.enabled and len(bucket.subs) > 1
    )


def _band(level: int) -> str:
    return next(band.id for band in DECLARED.energy.bands if level <= band.max)


LOW, MED, HIGH = _band(1), _band(5), _band(9)
SINK = DECLARED.energy.no_energy_sub.id


def _scanned(content_id: str, bucket: str, *, energy: int | None, genre: str = "") -> adopt_scan.ScannedTrack:
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


def _held(bucket: str, **tracks: tuple[str, ...]) -> adopt_plan.Placements:
    return adopt_plan.Placements(read=True, held={bucket: dict(tracks)})


def _plan(tracks, placements=adopt_plan.UNREAD) -> adopt_plan.AdoptionPlan:
    return adopt_plan.build_adoption_plan(
        tracks, DECLARED, tree=TREE_ID, placements=placements
    )


def _only(plan: adopt_plan.AdoptionPlan) -> adopt_plan.PlanEntry:
    (entry,) = plan.entries
    return entry


# ── what the taxonomy says competes ────────────────────────────────────────


def test_the_bands_and_the_no_reading_sub_compete_in_an_energy_bucket():
    kind, subs = routing.competing_subs(DECLARED, _energy_bucket().id)
    assert kind is routing.Competing.BAND
    assert subs == {band.id for band in DECLARED.energy.bands} | {SINK}


def test_the_style_subs_compete_where_a_bucket_has_no_energy_dimension():
    bucket = _style_bucket()
    kind, subs = routing.competing_subs(DECLARED, bucket.id)
    assert kind is routing.Competing.STYLE
    # R-797: a playlist this folder still holds for a bucket that left it
    # competes here too. Its own tests are in test_adopt_former_place.py.
    former = {place.id for _declarer, place in routing.former_places(DECLARED, bucket.id)}
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
    """The plan only withholds a sub in the set, so a sub routing can return
    that the set misses would be a track filed twice with nothing said."""
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
        bucket, HIGH, (MED,), "band",
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


def test_a_withheld_entry_keeps_the_identifier_of_the_work_it_was():
    bucket = _energy_bucket().id
    entry = _only(_plan([_scanned("t", bucket, energy=8)], _held(bucket, t=(MED,))))
    assert entry.entry_id == adopt_plan.entry_id_for(TREE_ID, "t", bucket, HIGH)


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


@pytest.mark.parametrize("sub_class", [entry.id for entry in DECLARED.sub_classes])
def test_a_track_sitting_only_in_a_sub_class_is_added_to_its_band(sub_class):
    """Even when a caller hands the plan a held sub class, which the reader
    never does. The plan asks the taxonomy for itself."""
    bucket = _energy_bucket().id
    entry = _only(_plan([_scanned("t", bucket, energy=8)], _held(bucket, t=(sub_class,))))
    assert entry.disposition is adopt_scan.Disposition.ROUTE
    assert entry.sub == HIGH


def test_a_track_in_the_no_reading_sub_whose_file_now_reads_is_withheld():
    bucket = _energy_bucket().id
    entry = _only(_plan([_scanned("t", bucket, energy=5)], _held(bucket, t=(SINK,))))
    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.sub, entry.holds) == (MED, (SINK,))


def test_a_track_in_a_band_whose_file_has_no_reading_is_withheld_from_the_sink():
    bucket = _energy_bucket().id
    entry = _only(_plan([_scanned("t", bucket, energy=None)], _held(bucket, t=(HIGH,))))
    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.sub, entry.holds, entry.energy) == (SINK, (HIGH,), None)


def test_a_track_in_one_style_sub_is_withheld_from_another():
    bucket = _style_bucket()
    first, second = bucket.subs[0], bucket.subs[1]
    genre = next(
        source for source, sub in bucket.sub_by_source.map.items() if sub == second.id
    )
    plan = _plan(
        [_scanned("t", bucket.id, energy=8, genre=genre)], _held(bucket.id, t=(first.id,))
    )
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


def test_a_track_in_two_bands_is_not_withheld_from_the_one_the_plan_names():
    """The shape the live library already holds 37 of. The writer reports the
    row already present, so there is nothing to withhold it from."""
    bucket = _energy_bucket().id
    entry = _only(_plan([_scanned("t", bucket, energy=8)], _held(bucket, t=(HIGH, MED))))
    assert entry.disposition is adopt_scan.Disposition.ROUTE


def test_a_track_in_two_bands_is_withheld_from_a_third_and_both_are_listed():
    bucket = _energy_bucket().id
    entry = _only(_plan([_scanned("t", bucket, energy=1)], _held(bucket, t=(HIGH, MED))))
    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert entry.holds == tuple(sorted((HIGH, MED)))


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


def test_an_unread_tree_withholds_nothing_even_when_it_carries_held_subs():
    bucket = _energy_bucket().id
    unread = adopt_plan.Placements(read=False, held={bucket: {"t": (MED,)}})
    entry = _only(_plan([_scanned("t", bucket, energy=8)], unread))
    assert entry.disposition is adopt_scan.Disposition.ROUTE


# ── the verdict paths keep what the plan read ──────────────────────────────


def _needs_genre(content_id: str, *, energy: int | None) -> adopt_scan.ScannedTrack:
    return adopt_scan.ScannedTrack(
        content_id=content_id,
        recorded=f"/library/Music/{content_id}.flac",
        path=f"/library/Music/{content_id}.flac",
        readability=adopt_scan.Readability.READABLE,
        disposition=adopt_scan.Disposition.NEEDS_GENRE,
        genre="",
        energy=energy,
    )


def test_a_genre_answered_later_is_withheld_over_the_place_the_track_holds():
    bucket = _energy_bucket().id
    plan = _plan([_needs_genre("t", energy=8)], _held(bucket, t=(MED,)))
    answered = adopt_plan.with_verdicts(plan, {"t": bucket}, DECLARED)
    entry = _only(answered)

    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.bucket, entry.sub, entry.holds, entry.withheld_by) == (
        bucket, HIGH, (MED,), "band",
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
    folder = adopt_plan.ExistingFolder(
        node_id="n1", display=bucket.display, content_ids=("t", "u")
    )
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


def test_a_node_carrying_the_declared_names_is_the_sub_it_names():
    bucket = _energy_bucket().id
    found = adopt_placements.placements_from(DECLARED, [_node(bucket, MED, "t", "u")], None)
    assert found.read is True
    assert found.holds(bucket, "t") == (MED,)
    assert found.holds(bucket, "absent") == ()


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
    record = convergence.TreeConvergence(
        tree_id=TREE_ID,
        nodes=(
            convergence.DestinationNode(
                bucket=bucket, sub=MED, folder_id="f1", playlist_id="p1"
            ),
        ),
    )
    renamed = _node(bucket, MED, "t", names=("Renamed folder", "Renamed list"))
    assert adopt_placements.placements_from(DECLARED, [renamed], None).held == {}
    found = adopt_placements.placements_from(DECLARED, [renamed], record)
    assert found.holds(bucket, "t") == (MED,)
    assert found.holds_unnamed(bucket, "t") == (MED,)


def test_a_sub_held_under_both_names_is_one_the_writer_can_see():
    bucket = _energy_bucket().id
    record = convergence.TreeConvergence(
        tree_id=TREE_ID,
        nodes=(
            convergence.DestinationNode(
                bucket=bucket, sub=MED, folder_id="f1", playlist_id="p1"
            ),
        ),
    )
    nodes = [
        _node(bucket, MED, "t", "u", names=("Renamed folder", "Renamed list")),
        _node(bucket, MED, "t", ids=("f2", "p2")),
    ]
    found = adopt_placements.placements_from(DECLARED, nodes, record)
    assert (found.holds(bucket, "t"), found.holds_unnamed(bucket, "t")) == ((MED,), ())
    assert (found.holds(bucket, "u"), found.holds_unnamed(bucket, "u")) == ((MED,), (MED,))


def test_a_recorded_node_that_carries_the_declared_names_is_not_unnamed():
    bucket = _energy_bucket().id
    record = convergence.TreeConvergence(
        tree_id=TREE_ID,
        nodes=(
            convergence.DestinationNode(
                bucket=bucket, sub=MED, folder_id="f1", playlist_id="p1"
            ),
        ),
    )
    found = adopt_placements.placements_from(DECLARED, [_node(bucket, MED, "t")], record)
    assert (found.holds(bucket, "t"), found.holds_unnamed(bucket, "t")) == ((MED,), ())


def test_two_nodes_answering_for_one_destination_both_count():
    bucket = _energy_bucket().id
    nodes = [
        _node(bucket, MED, "t", ids=("f1", "p1")),
        _node(bucket, MED, "u", ids=("f2", "p2")),
    ]
    found = adopt_placements.placements_from(DECLARED, nodes, None)
    assert (found.holds(bucket, "t"), found.holds(bucket, "u")) == ((MED,), (MED,))


def test_a_track_in_two_bands_holds_both():
    bucket = _energy_bucket().id
    nodes = [
        _node(bucket, MED, "t", ids=("f1", "p1")),
        _node(bucket, HIGH, "t", ids=("f1", "p2")),
    ]
    found = adopt_placements.placements_from(DECLARED, nodes, None)
    assert found.holds(bucket, "t") == tuple(sorted((MED, HIGH)))
    assert found.holds_doubled(bucket, "t") == ()


def test_a_pair_held_by_two_rows_is_held_once_and_doubled():
    """R-781's shape, carried rather than lost in the set (R-780 lists it)."""
    bucket = _energy_bucket().id
    found = adopt_placements.placements_from(
        DECLARED, [_node(bucket, MED, "t", "u", doubled=("t",))], None
    )
    assert (found.holds(bucket, "t"), found.holds_doubled(bucket, "t")) == ((MED,), (MED,))
    assert (found.holds(bucket, "u"), found.holds_doubled(bucket, "u")) == ((MED,), ())
    assert found.holds_doubled(bucket, "absent") == ()


def test_two_nodes_answering_for_one_sub_are_two_playlists_and_not_a_double():
    bucket = _energy_bucket().id
    nodes = [
        _node(bucket, MED, "t", ids=("f1", "p1")),
        _node(bucket, MED, "t", ids=("f2", "p2")),
    ]
    found = adopt_placements.placements_from(DECLARED, nodes, None)
    assert (found.holds(bucket, "t"), found.holds_doubled(bucket, "t")) == ((MED,), ())


def test_a_double_in_a_renamed_recorded_node_is_still_a_double():
    bucket = _energy_bucket().id
    record = convergence.TreeConvergence(
        tree_id=TREE_ID,
        nodes=(
            convergence.DestinationNode(
                bucket=bucket, sub=MED, folder_id="f1", playlist_id="p1"
            ),
        ),
    )
    renamed = _node(bucket, MED, "t", names=("Renamed folder", "Renamed list"), doubled=("t",))
    found = adopt_placements.placements_from(DECLARED, [renamed], record)
    assert found.holds_doubled(bucket, "t") == (MED,)


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


def test_a_track_in_the_planned_sub_under_another_name_only_is_withheld():
    bucket = _energy_bucket().id
    renamed = adopt_plan.Placements(
        read=True, held={bucket: {"t": (HIGH,)}}, unnamed={bucket: {"t": (HIGH,)}}
    )
    entry = _only(_plan([_scanned("t", bucket, energy=8)], renamed))
    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.sub, entry.holds, entry.holds_unnamed) == (HIGH, (HIGH,), (HIGH,))


def test_an_unnamed_sub_the_track_does_not_hold_changes_nothing():
    """``unnamed`` is a part of ``held``. A caller that hands over one without
    the other has not shown that the track sits anywhere."""
    bucket = _energy_bucket().id
    odd = adopt_plan.Placements(read=True, unnamed={bucket: {"t": (HIGH,)}})
    entry = _only(_plan([_scanned("t", bucket, energy=8)], odd))
    assert entry.disposition is adopt_scan.Disposition.ROUTE


def test_the_digest_covers_every_field_the_review_list_shows():
    """One changed field at a time, and the list of fields is closed below so
    a field added to the screen has to be added here."""
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
    """The shipped taxonomy with a sub class added under a band's identifier.

    Nothing in the shipped template does this, which is why the two guards
    below measured zero against it. A person's own template can.
    """
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
