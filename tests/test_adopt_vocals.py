"""R-788: adoption files a vox tagged track under its bucket's vocal sub.

Only the routing pass filed a vocal sub, per batch, so a track that reached its
bucket through adoption sat there without the bucket's vocal sub. This module
holds the pure halves of the fix: which buckets declare the sub, what the plan
does with a track that carries the tag, what the digest covers, how a tree
already read becomes the value the plan takes, and how the tag is read off a
database. The read off a real database and the approved apply are driven in
``tests/test_adopt_workers.py``.

Every expected identifier is derived from the shipped taxonomy's own
declarations rather than spelled, for the reason ``test_adopt_placements``
gives.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from cratekit.adopt import apply_cli
from cratekit.adopt import placements as adopt_placements
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.core import convergence, rb_writer, routing, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.write import metadata_cli, rebuild, trees
from cratekit.write.routing_pass import destination

TREE_ID = "shelf_stack"
DECLARED = taxonomy.default_taxonomy()
VOX = trees.VOX_SUB_CLASS


def _energy_bucket() -> taxonomy.Bucket:
    return next(
        bucket
        for bucket in DECLARED.buckets
        if bucket.sub_by_source is None and bucket.energy.enabled
    )


def _style_bucket() -> taxonomy.Bucket:
    return next(
        bucket
        for bucket in DECLARED.buckets
        if not bucket.energy.enabled and len(bucket.subs) > 1
    )


def _band(level: int) -> str:
    return next(band.id for band in DECLARED.energy.bands if level <= band.max)


MED, HIGH = _band(5), _band(9)
BUCKET = _energy_bucket().id


def _with_vocal_class(**changes) -> taxonomy.Taxonomy:
    """The shipped template with its vocal sub class changed."""
    return replace(
        DECLARED,
        sub_classes=tuple(
            replace(entry, **changes) if entry.id == VOX else entry
            for entry in DECLARED.sub_classes
        ),
    )


def _scanned(content_id: str, bucket: str = BUCKET, *, energy: int | None = 5):
    return adopt_scan.ScannedTrack(
        content_id=content_id,
        recorded=f"/library/Music/{content_id}.flac",
        path=f"/library/Music/{content_id}.flac",
        readability=adopt_scan.Readability.READABLE,
        disposition=adopt_scan.Disposition.ROUTE,
        genre=DECLARED.bucket(bucket).display,
        bucket=bucket,
        energy=energy,
    )


def _vocals(*tagged: str, filed=(), unnamed=(), bucket: str = BUCKET) -> adopt_plan.Vocals:
    return adopt_plan.Vocals(
        read=True,
        tag_found=True,
        tagged=frozenset(tagged),
        filed={bucket: frozenset({*filed, *unnamed})} if (filed or unnamed) else {},
        unnamed={bucket: frozenset(unnamed)} if unnamed else {},
    )


def _plan(tracks, vocals=adopt_plan.NO_VOCALS, *, placements=adopt_plan.UNREAD, declared=DECLARED):
    return adopt_plan.build_adoption_plan(
        tracks, declared, tree=TREE_ID, placements=placements, vocals=vocals
    )


def _only(plan: adopt_plan.AdoptionPlan) -> adopt_plan.PlanEntry:
    (entry,) = plan.entries
    return entry


# ── which buckets declare the vocal sub ────────────────────────────────────


def test_the_shipped_template_declares_the_vocal_sub_in_every_bucket():
    assert DECLARED.sub_class(VOX).additive is True
    for bucket in DECLARED.buckets:
        assert adopt_plan.vocal_sub(DECLARED, bucket.id) == VOX, bucket.id


def test_a_class_declared_for_the_energy_buckets_is_in_those_and_in_no_other():
    declared = _with_vocal_class(present_in=adopt_plan.PRESENT_IN_ENERGY)
    for bucket in declared.buckets:
        kind, _subs = routing.competing_subs(declared, bucket.id)
        expected = VOX if kind is routing.Competing.BAND else None
        assert adopt_plan.vocal_sub(declared, bucket.id) == expected, bucket.id
    assert adopt_plan.vocal_sub(declared, _energy_bucket().id) == VOX
    assert adopt_plan.vocal_sub(declared, _style_bucket().id) is None


def test_a_present_in_nobody_defined_is_no_bucket():
    declared = _with_vocal_class(present_in="some_buckets")
    assert {adopt_plan.vocal_sub(declared, bucket.id) for bucket in declared.buckets} == {None}


def test_a_taxonomy_with_no_additive_class_declares_no_vocal_sub():
    declared = replace(
        DECLARED, sub_classes=tuple(e for e in DECLARED.sub_classes if not e.additive)
    )
    assert adopt_plan.vocal_sub(declared, BUCKET) is None


def test_a_class_of_that_identifier_that_is_not_additive_is_not_the_vocal_sub():
    assert adopt_plan.vocal_sub(_with_vocal_class(additive=False), BUCKET) is None


def test_an_additive_class_of_another_identifier_is_not_the_vocal_sub():
    """The derivation knows the signal for one additive class. Filing the tag
    under any other would be answering for a dimension nobody defined."""
    assert adopt_plan.vocal_sub(_with_vocal_class(id="instrumental"), BUCKET) is None


# ── what the plan does with a track that carries the tag ───────────────────


def test_a_tagged_track_gains_the_vocal_sub_and_its_band_entry_is_unchanged():
    plain = _only(_plan([_scanned("t")]))
    entry = _only(_plan([_scanned("t")], _vocals("t")))

    assert (entry.vocal, entry.vocal_sub) == (adopt_plan.VOCAL_ADD, VOX)
    assert entry.vocal_planned is True
    assert (entry.entry_id, entry.bucket, entry.sub) == (plain.entry_id, BUCKET, MED)
    assert entry.disposition is adopt_scan.Disposition.ROUTE
    assert replace(entry, vocal="", vocal_sub="") == plain


def test_a_track_already_in_the_sub_is_counted_present_and_not_added():
    plan = _plan([_scanned("t"), _scanned("u")], _vocals("t", "u", filed=("t",)))
    states = {entry.content_id: entry.vocal for entry in plan.entries}

    assert states == {"t": adopt_plan.VOCAL_PRESENT, "u": adopt_plan.VOCAL_ADD}
    assert [entry.content_id for entry in plan.vocal_additions()] == ["u"]
    assert plan.vocal_counts() == {
        adopt_plan.VOCAL_ADD: 1,
        adopt_plan.VOCAL_PRESENT: 1,
        adopt_plan.VOCAL_RENAMED: 0,
        adopt_plan.VOCAL_NO_SUB: 0,
        adopt_plan.VOCAL_WITHHELD: 0,
    }


def test_a_bucket_with_no_vocal_sub_plans_nothing_for_its_tagged_tracks():
    declared = _with_vocal_class(present_in=adopt_plan.PRESENT_IN_ENERGY)
    style = _style_bucket()
    track = replace(
        _scanned("s", style.id), genre=next(iter(style.sub_by_source.map))
    )
    banded = _scanned("t")
    plan = _plan([track, banded], _vocals("s", "t"), declared=declared)
    states = {entry.content_id: (entry.vocal, entry.vocal_sub) for entry in plan.entries}

    assert states["s"] == (adopt_plan.VOCAL_NO_SUB, "")
    assert states["t"] == (adopt_plan.VOCAL_ADD, VOX)
    assert [entry.content_id for entry in plan.vocal_additions()] == ["t"]
    assert plan.vocal_counts()[adopt_plan.VOCAL_NO_SUB] == 1


def test_a_track_without_the_tag_is_never_added():
    plan = _plan([_scanned("t"), _scanned("u")], _vocals("u"))
    untagged = next(entry for entry in plan.entries if entry.content_id == "t")

    assert (untagged.vocal, untagged.vocal_sub) == adopt_plan.NO_VOCAL_PLACE
    assert untagged.vocal_planned is False
    assert [entry.content_id for entry in plan.vocal_additions()] == ["u"]


def test_an_untagged_track_sitting_in_a_vocal_sub_is_left_out_of_the_plan_entirely():
    """Nothing here removes. A membership whose tag is absent is not a state
    the plan has, so no writer is ever handed it."""
    vocals = adopt_plan.Vocals(
        read=True, tag_found=True, tagged=frozenset(), filed={BUCKET: frozenset({"t"})}
    )
    plan = _plan([_scanned("t")], vocals)

    assert _only(plan).vocal == ""
    assert plan.vocal_additions() == ()
    assert sum(plan.vocal_counts().values()) == 0
    assert plan.digest() == _plan([_scanned("t")], _vocals()).digest()


def test_a_track_in_the_sub_under_another_name_only_is_not_added():
    plan = _plan([_scanned("t")], _vocals("t", unnamed=("t",)))

    assert _only(plan).vocal == adopt_plan.VOCAL_RENAMED
    assert _only(plan).vocal_planned is False
    assert plan.vocal_additions() == ()


def test_a_track_whose_bucket_has_its_vocal_sub_under_another_name_only_is_not_added():
    """The track is not in the sub. Adding it would not put it in the renamed
    playlist, it would make a second one of the declared name beside it."""
    vocals = replace(_vocals("t", "u", unnamed=("u",)), renamed=frozenset({BUCKET}))
    plan = _plan([_scanned("t"), _scanned("u")], vocals)

    assert {entry.vocal for entry in plan.entries} == {adopt_plan.VOCAL_RENAMED}
    assert plan.vocal_additions() == ()
    assert plan.vocal_counts()[adopt_plan.VOCAL_RENAMED] == 2


def test_a_tree_nobody_read_plans_no_vocal_membership():
    blind = adopt_plan.Vocals(read=False, tag_found=True, tagged=frozenset({"t"}))
    plan = _plan([_scanned("t")], blind)

    assert _only(plan).vocal == ""
    assert plan.vocals.state == adopt_plan.VOCALS_UNREAD


def test_an_entry_with_no_bucket_has_no_vocal_question():
    needs_genre = replace(
        _scanned("t"), disposition=adopt_scan.Disposition.NEEDS_GENRE, bucket=""
    )
    excluded = replace(
        _scanned("u"),
        disposition=adopt_scan.Disposition.EXCLUDED,
        readability=adopt_scan.Readability.UNREADABLE,
    )
    plan = _plan([needs_genre, excluded], _vocals("t", "u"))

    assert {entry.vocal for entry in plan.entries} == {""}


# ── a withheld track gains nothing ─────────────────────────────────────────


def _held(**tracks: tuple[str, ...]) -> adopt_plan.Placements:
    return adopt_plan.Placements(read=True, held={BUCKET: dict(tracks)})


def test_a_track_withheld_over_another_band_stays_withheld_and_gains_no_vocal_sub():
    plan = _plan([_scanned("t", energy=9)], _vocals("t"), placements=_held(t=(MED,)))
    entry = _only(plan)

    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.vocal, entry.vocal_sub) == (adopt_plan.VOCAL_WITHHELD, VOX)
    assert entry.vocal_planned is False
    assert plan.vocal_additions() == ()
    assert plan.vocal_counts()[adopt_plan.VOCAL_WITHHELD] == 1


def test_a_withheld_track_already_in_its_vocal_sub_reads_present_and_is_not_digested():
    placements = _held(t=(MED,))
    there = _plan([_scanned("t", energy=9)], _vocals("t", filed=("t",)), placements=placements)
    owed = _plan([_scanned("t", energy=9)], _vocals("t"), placements=placements)

    assert _only(there).vocal == adopt_plan.VOCAL_PRESENT
    assert _only(there).vocal_planned is False
    # Neither is a membership an apply may write, so neither is in the digest.
    assert there.digest() == owed.digest()


def test_a_keep_separate_verdict_withholds_the_vocal_addition_with_the_entry():
    existing = adopt_plan.ExistingFolder(
        node_id="n1", display=DECLARED.bucket(BUCKET).display, content_ids=("stranger",)
    )
    plan = adopt_plan.build_adoption_plan(
        [_scanned("t"), _scanned("u")],
        DECLARED,
        tree=TREE_ID,
        existing=[existing],
        vocals=_vocals("t", "u", filed=("u",)),
    )
    assert [entry.content_id for entry in plan.vocal_additions()] == ["t"]

    refused = adopt_plan.with_collision_verdicts(plan, {"n1": adopt_plan.COLLISION_SEPARATE})
    states = {entry.content_id: entry.vocal for entry in refused.entries}

    assert states == {"t": adopt_plan.VOCAL_WITHHELD, "u": adopt_plan.VOCAL_PRESENT}
    assert refused.vocal_additions() == ()
    assert refused.digest() != plan.digest()

    kept = adopt_plan.with_collision_verdicts(plan, {"n1": adopt_plan.COLLISION_ADOPT})
    assert kept.vocal_additions() == plan.vocal_additions()


def test_an_answered_genre_is_filed_under_the_vocal_sub_of_the_bucket_it_was_given():
    asked = replace(
        _scanned("t"), disposition=adopt_scan.Disposition.NEEDS_GENRE, bucket="", genre=""
    )
    plan = _plan([asked], _vocals("t"))
    assert _only(plan).vocal == ""

    answered = _only(adopt_plan.with_verdicts(plan, {"t": BUCKET}, DECLARED))
    assert answered.disposition is adopt_scan.Disposition.ROUTE
    assert (answered.bucket, answered.vocal, answered.vocal_sub) == (
        BUCKET,
        adopt_plan.VOCAL_ADD,
        VOX,
    )


# ── what the digest covers ─────────────────────────────────────────────────


def test_the_digest_changes_when_a_vocal_membership_is_added_to_the_plan():
    tracks = [_scanned("t"), _scanned("u")]
    none = _plan(tracks, _vocals())
    one = _plan(tracks, _vocals("t"))
    two = _plan(tracks, _vocals("t", "u"))

    assert len({none.digest(), one.digest(), two.digest()}) == 3


def test_the_digest_does_not_move_when_the_membership_it_approved_lands():
    """The apply's own write turns an addition into a presence. A digest that
    told them apart would refuse a stopped run's own half finished work."""
    tracks = [_scanned("t"), _scanned("u")]
    before = _plan(tracks, _vocals("t", "u"))
    after = _plan(tracks, _vocals("t", "u", filed=("t", "u")))

    assert len(before.vocal_additions()) == 2
    assert after.vocal_additions() == ()
    assert before.digest() == after.digest()


def test_the_digest_says_whether_the_tag_and_the_tree_were_read():
    tracks = [_scanned("t")]
    unread = _plan(tracks)
    no_tag = _plan(tracks, adopt_plan.Vocals(read=True, tag_found=False))
    read = _plan(tracks, _vocals())

    assert [plan.vocals.state for plan in (unread, no_tag, read)] == [
        adopt_plan.VOCALS_UNREAD,
        adopt_plan.VOCALS_NO_TAG,
        adopt_plan.VOCALS_READ,
    ]
    assert len({unread.digest(), no_tag.digest(), read.digest()}) == 3


def test_a_vocal_membership_has_an_identifier_of_its_own():
    entry = _only(_plan([_scanned("t")], _vocals("t")))

    assert adopt_plan.vocal_id(entry) == adopt_plan.entry_id_for(TREE_ID, "t", BUCKET, VOX)
    assert adopt_plan.vocal_id(entry) != entry.entry_id


# ── the plan document ──────────────────────────────────────────────────────


def test_the_document_names_the_count_and_lists_every_addition():
    plan = _plan(
        [_scanned("t"), _scanned("u"), _scanned("v")], _vocals("t", "u", filed=("u",))
    )
    document = adopt_plan.to_json(plan)

    assert document["vocals"] == adopt_plan.VOCALS_READ
    assert tuple(document["vocal"]) == adopt_plan.VOCAL_STATES
    assert document["vocal"][adopt_plan.VOCAL_ADD] == 1
    assert document["vocal"][adopt_plan.VOCAL_PRESENT] == 1
    assert document["vocal_additions"] == [
        {
            "id": adopt_plan.entry_id_for(TREE_ID, "t", BUCKET, VOX),
            "content_id": "t",
            "location": "/library/Music/t.flac",
            "bucket": BUCKET,
            "sub": VOX,
        }
    ]
    assert {row["content_id"]: row["vocal"] for row in document["entries"]} == {
        "t": adopt_plan.VOCAL_ADD,
        "u": adopt_plan.VOCAL_PRESENT,
        "v": "",
    }


def test_the_gate_shows_what_the_document_says_about_vocals():
    plan = _plan([_scanned("t"), _scanned("u")], _vocals("t"))
    digested, facts = apply_cli._digested(plan)
    document = adopt_plan.to_json(plan)

    assert digested["digest"] == plan.digest()
    for key in ("vocals", "vocal", "vocal_additions"):
        assert facts[key] == document[key], key
    assert [row["content_id"] for row in facts["vocal_additions"]] == ["t"]


# ── the mapping the tree writer is handed ──────────────────────────────────


def test_only_the_additions_reach_the_writer_under_the_declared_names():
    plan = _plan(
        [_scanned("t"), _scanned("u"), _scanned("v")],
        _vocals("t", "u", "v", filed=("u",), unnamed=("v",)),
    )
    assert apply_cli.vocal_locations(plan, DECLARED) == {
        destination(DECLARED, BUCKET, VOX): ["/library/Music/t.flac"]
    }


def test_one_apply_writes_the_entries_and_the_vocal_subs_in_one_mapping():
    plan = _plan([_scanned("t"), _scanned("u", energy=9)], _vocals("t"))
    wanted = apply_cli.planned_memberships(plan, DECLARED)

    assert wanted == {
        destination(DECLARED, BUCKET, MED): ["/library/Music/t.flac"],
        destination(DECLARED, BUCKET, HIGH): ["/library/Music/u.flac"],
        destination(DECLARED, BUCKET, VOX): ["/library/Music/t.flac"],
    }
    assert apply_cli.membership_locations(plan.applicable(), DECLARED) == {
        key: rows for key, rows in wanted.items() if key[1] != DECLARED.sub_class(VOX).display
    }


def test_a_plan_with_no_vocal_addition_hands_the_writer_what_it_always_did():
    plan = _plan([_scanned("t")], _vocals())
    assert apply_cli.planned_memberships(plan, DECLARED) == apply_cli.membership_locations(
        plan.applicable(), DECLARED
    )


# ── how a tree already read becomes the value ──────────────────────────────


def _node(bucket_id: str, sub_id: str, *content_ids: str, **changes) -> rebuild.TreeNode:
    folder, playlist = destination(DECLARED, bucket_id, sub_id)
    values = {
        "folder_id": f"f-{bucket_id}",
        "folder_display": folder,
        "playlist_id": f"p-{bucket_id}-{sub_id}",
        "playlist_display": playlist,
        "content_ids": frozenset(content_ids),
    }
    return rebuild.TreeNode(**{**values, **changes})


def _record(bucket_id: str, node: rebuild.TreeNode) -> convergence.TreeConvergence:
    return convergence.TreeConvergence(tree_id=DECLARED.tree.id).with_nodes(
        [
            convergence.DestinationNode(
                bucket=bucket_id,
                sub=VOX,
                folder_id=node.folder_id,
                playlist_id=node.playlist_id,
            )
        ]
    )


def test_a_vocal_playlist_under_the_declared_names_files_its_tracks():
    nodes = [_node(BUCKET, VOX, "t", "u"), _node(BUCKET, MED, "t", "w")]
    found = adopt_placements.vocals_from(DECLARED, nodes, None, frozenset({"t"}))

    assert (found.read, found.tag_found) == (True, True)
    assert found.tagged == {"t"}
    assert found.filed == {BUCKET: {"t", "u"}}
    assert found.unnamed == {}
    assert found.renamed == frozenset()
    assert found.sits(BUCKET, "u") and not found.sits(BUCKET, "w")


def test_a_renamed_vocal_playlist_is_found_through_its_recorded_node_and_says_so():
    renamed = _node(BUCKET, VOX, "t", playlist_display="Singers")
    assert adopt_placements.vocals_from(DECLARED, [renamed], None, frozenset()).filed == {}

    found = adopt_placements.vocals_from(
        DECLARED, [renamed], _record(BUCKET, renamed), frozenset()
    )
    assert found.filed == {BUCKET: {"t"}}
    assert found.unnamed == {BUCKET: {"t"}}
    assert found.sits_unnamed(BUCKET, "t")
    assert found.renamed == {BUCKET}


def test_a_track_held_under_both_names_is_not_held_under_another_name_only():
    renamed = _node(BUCKET, VOX, "t", "u", playlist_display="Singers", playlist_id="p-old")
    named = _node(BUCKET, VOX, "t")
    found = adopt_placements.vocals_from(
        DECLARED, [renamed, named], _record(BUCKET, renamed), frozenset()
    )

    assert found.filed == {BUCKET: {"t", "u"}}
    assert found.unnamed == {BUCKET: {"u"}}
    # A playlist of the declared name is there, so an addition has somewhere
    # the writer can find and the bucket is not one it would double.
    assert found.renamed == frozenset()


def test_a_removed_vocal_playlist_is_not_a_place():
    gone = _node(BUCKET, VOX, "t", removed=True)
    found = adopt_placements.vocals_from(DECLARED, [gone], _record(BUCKET, gone), frozenset())
    assert found.filed == {}
    assert found.renamed == frozenset()


def test_an_empty_renamed_vocal_playlist_still_names_its_bucket():
    """Nobody sits in it, so nothing is filed, and the next tagged track must
    still not be handed to a writer that would make a second playlist."""
    empty = _node(BUCKET, VOX, playlist_display="Singers")
    found = adopt_placements.vocals_from(DECLARED, [empty], _record(BUCKET, empty), frozenset())

    assert found.filed == {}
    assert found.renamed == {BUCKET}


def test_a_bucket_that_declares_no_vocal_sub_is_not_read_for_one():
    declared = _with_vocal_class(present_in=adopt_plan.PRESENT_IN_ENERGY)
    style = _style_bucket().id
    nodes = [_node(style, VOX, "s"), _node(BUCKET, VOX, "t")]
    found = adopt_placements.vocals_from(declared, nodes, None, frozenset())

    assert found.filed == {BUCKET: {"t"}}


def test_a_library_with_no_such_tag_is_not_a_library_with_nobody_tagged():
    absent = adopt_placements.vocals_from(DECLARED, [], None, None)
    empty = adopt_placements.vocals_from(DECLARED, [], None, frozenset())

    assert (absent.tag_found, absent.state) == (False, adopt_plan.VOCALS_NO_TAG)
    assert (empty.tag_found, empty.state) == (True, adopt_plan.VOCALS_READ)
    assert absent.tagged == empty.tagged == frozenset()


# ── how the tag is read off a database ─────────────────────────────────────


class _TagTables:
    """The two lookups the tag reader makes, over rows a test spells."""

    def __init__(self, tags, songs):
        self._tags, self._songs = list(tags), list(songs)

    def get_my_tag(self, **where):
        return [tag for tag in self._tags if tag.Name == where["Name"]]

    def get_my_tag_songs(self, **where):
        return [song for song in self._songs if song.MyTagID == where["MyTagID"]]


def _tag(tag_id: str, name: str, parent: str, deleted: int = 0) -> SimpleNamespace:
    row = SimpleNamespace(ID=tag_id, Name=name, ParentID=parent)
    setattr(row, rb_writer.SOFT_DELETE_COLUMN, deleted)
    return row


def _song(tag_id: str, content_id: str, deleted: int = 0) -> SimpleNamespace:
    row = SimpleNamespace(ID=f"s-{tag_id}-{content_id}", MyTagID=tag_id, ContentID=content_id)
    setattr(row, rb_writer.SOFT_DELETE_COLUMN, deleted)
    return row


CATEGORY = _tag("10", metadata_cli.CATEGORY, "0")
VALUE = _tag("11", metadata_cli.VALUE_VOX, "10")


def test_the_tag_is_the_vox_value_inside_the_vocals_category():
    db = _TagTables(
        [CATEGORY, VALUE, _tag("12", metadata_cli.VALUE_MALE, "10")],
        [_song("11", "t"), _song("11", "u"), _song("12", "m")],
    )
    assert adopt_placements.vox_tagged(db) == {"t", "u"}


def test_a_value_of_that_name_under_another_category_is_another_tag():
    db = _TagTables(
        [CATEGORY, _tag("20", "Moods", "0"), _tag("21", metadata_cli.VALUE_VOX, "20")],
        [_song("21", "t")],
    )
    assert adopt_placements.vox_tagged(db) is None


def test_a_library_with_the_tag_and_nobody_carrying_it_answers_the_empty_set():
    assert adopt_placements.vox_tagged(_TagTables([CATEGORY, VALUE], [])) == frozenset()
    assert adopt_placements.vox_tagged(_TagTables([CATEGORY], [])) is None
    assert adopt_placements.vox_tagged(_TagTables([], [])) is None


def test_a_tag_a_person_took_off_is_not_a_tag():
    db = _TagTables([CATEGORY, VALUE], [_song("11", "t"), _song("11", "u", deleted=1)])
    assert adopt_placements.vox_tagged(db) == {"t"}


def test_a_removed_value_or_category_is_no_tag_at_all():
    songs = [_song("11", "t")]
    gone_value = _TagTables([CATEGORY, _tag("11", metadata_cli.VALUE_VOX, "10", 1)], songs)
    gone_category = _TagTables([_tag("10", metadata_cli.CATEGORY, "0", 1), VALUE], songs)

    assert adopt_placements.vox_tagged(gone_value) is None
    assert adopt_placements.vox_tagged(gone_category) is None


def test_an_association_that_cannot_say_whether_it_was_removed_refuses():
    silent = SimpleNamespace(ID="s", MyTagID="11", ContentID="t")
    with pytest.raises(CratekitError) as refused:
        adopt_placements.vox_tagged(_TagTables([CATEGORY, VALUE], [silent]))
    assert refused.value.cause.reason == "soft-delete-marker-unreadable"
