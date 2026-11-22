"""R-797: a bucket promoted to its own folder leaves the playlist its tracks sat in.

R&B became a top level folder split by energy, and its old playlist in the non
electronic folder is its FORMER PLACE. Held here: what competes, what the reader
finds, what adoption withholds, what the move plans and lists, the writer's
refusal to file into a former place, and the verb against a disposable library
with real tags. Identifiers are derived from the shipped declarations, the old
shape rebuilt from the shipped text and checked to be the shape it claims.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date

import pytest

from cratekit.adopt import apply_cli, artifacts, collection, move_cli
from cratekit.adopt import move as adopt_move
from cratekit.adopt import placements as adopt_placements
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.core import config, convergence, jobs, routing, taxonomy
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild
from cratekit.write.routing_pass import destination
from tests.test_adopt_move import (  # noqa: F401
    DECLARED,
    HIGH,
    LOW,
    MED,
    SINK,
    TREE_ID,
    VERB,
    _adoption,
    _approve_and_run,
    _decided,
    _left_counts,
    _live,
    _moves,
    _refused_over,
    _removed,
    _rows,
    _shown,
    classified,
    seed_library,
)
from tests.test_adopt_workers import (  # noqa: F401
    _platform_seams,
    _reader_cache,
    _release_process_locks,
    library,
    machine,
    silence,
)

#: The bucket the shipped template promoted, found by what makes it one. The
#: first of them in declared order: since U118 Hip-Hop declares one too, held
#: by the same folder, and its own file is `test_adopt_split_place.py`.
PROMOTED = next(bucket for bucket in DECLARED.buckets if bucket.formerly)
(FORMER,) = PROMOTED.formerly
HOLDER = DECLARED.bucket(FORMER.bucket)
OLD_PLACE = (HOLDER.display, FORMER.display)
#: Every former place the holding folder competes on, this one and the others.
HELD_FORMERLY = {place.id for _declarer, place in routing.former_places(DECLARED, HOLDER.id)}
#: The bucket split out of the promoted one since (U118), whose words were the
#: promoted bucket's when it was promoted.
SPLIT = next(
    bucket
    for bucket in DECLARED.buckets
    if any(place.bucket == PROMOTED.id for place in bucket.split_from)
)
#: The split place it declares on the promoted bucket's former place.
(OLD_SPLIT,) = [place for place in SPLIT.split_from if place.sub == FORMER.id]

#: A genre the promoted bucket claims and one the old folder still claims.
PROMOTED_GENRE = PROMOTED.aliases[0]
STAYING_GENRE, STAYING_SUB = next(iter(HOLDER.sub_by_source.map.items()))
#: A word a keyword rule sends to the old folder with no row of its map, so it
#: lands in that folder's default sub.
DEFAULTED_GENRE = next(
    f"New {rule.keyword.title()}" for rule in DECLARED.fuzzy if rule.bucket == HOLDER.id
)
#: A bucket that is neither the promoted one nor the one holding its old place.
ELSEWHERE = next(
    bucket
    for bucket in DECLARED.buckets
    if bucket.id not in (PROMOTED.id, HOLDER.id)
    and bucket.sub_by_source is None
    and bucket.energy.enabled
    and adopt_scan.classify_genre(DECLARED, bucket.display)[1] == bucket.id
)


def _scanned(content_id: str, *, energy: int | None, genre: str = PROMOTED_GENRE, **excluded):
    return classified(content_id, energy=energy, genre=genre, **excluded)


def _in_old(content_id: str, *also: str) -> dict:
    """What the placement reader answers for a track in the old playlist.

    Under BOTH buckets the playlist competes in, as the reader reports it,
    and under the bucket split out of the promoted one since U118, which
    declares the playlist as one of its split places. ``also`` is the bands
    of the promoted bucket the track holds as well.
    """
    return {
        PROMOTED.id: {content_id: (FORMER.id, *also)},
        HOLDER.id: {content_id: (FORMER.id,)},
        SPLIT.id: {content_id: (OLD_SPLIT.id,)},
    }


# ── the shipped declaration ────────────────────────────────────────────────


def test_the_promoted_bucket_splits_by_energy_and_declares_the_place_it_left():
    assert PROMOTED.sub_by_source is None and PROMOTED.energy.enabled
    assert HOLDER.id != PROMOTED.id
    assert FORMER.sub not in {sub.id for sub in HOLDER.subs}
    assert FORMER.display not in {sub.display for sub in HOLDER.subs}
    assert FORMER.sub not in HOLDER.sub_by_source.map.values()


def test_the_promoted_bucket_writes_no_rating_as_the_folder_it_left_wrote_none():
    """Found by the review. The author decided bands and not ratings, and a
    bucket that omits the flag gets a star rating derived from energy."""
    assert routing.rates(DECLARED, HOLDER.id) is False
    assert routing.rates(DECLARED, PROMOTED.id) is False


def test_a_former_place_competes_where_it_is_declared_and_where_it_sits_and_nowhere_else():
    kind, subs = routing.competing_subs(DECLARED, PROMOTED.id)
    assert kind is routing.Competing.BAND
    assert subs == {band.id for band in DECLARED.energy.bands} | {SINK, FORMER.id}
    # IN THE FOLDER THAT HOLDS IT TOO, as it did before the promotion, and the
    # kind there is still that folder's own.
    kind, subs = routing.competing_subs(DECLARED, HOLDER.id)
    assert kind is routing.Competing.STYLE
    assert FORMER.id in HELD_FORMERLY
    assert subs == {sub.id for sub in HOLDER.subs} | HELD_FORMERLY
    for bucket in DECLARED.buckets:
        if bucket.id not in (PROMOTED.id, HOLDER.id):
            assert FORMER.id not in routing.competing_subs(DECLARED, bucket.id)[1], bucket.id
            assert (PROMOTED.id, FORMER) not in routing.former_places(DECLARED, bucket.id)
            if not bucket.formerly:
                # A BUCKET NO FORMER PLACE INVOLVES HAS NONE, strictly, so an
                # index that leaks one into an unrelated bucket fails here.
                assert routing.former_places(DECLARED, bucket.id) == (), bucket.id
    for bucket_id in (PROMOTED.id, HOLDER.id):
        assert routing.former_place(DECLARED, bucket_id, FORMER.id) is FORMER
    assert routing.former_places(DECLARED, PROMOTED.id) == ((PROMOTED.id, FORMER),)
    assert (PROMOTED.id, FORMER) in routing.former_places(DECLARED, HOLDER.id)
    assert routing.former_place(DECLARED, PROMOTED.id, MED) is None
    assert routing.former_place(DECLARED, ELSEWHERE.id, FORMER.id) is None


def test_no_resolver_answers_with_a_former_place_and_no_writer_can_name_one():
    for level in (None, *range(1, 11)):
        assert routing.energy_sub(DECLARED, PROMOTED.id, level).id != FORMER.id
    assert FORMER.id not in set(HOLDER.sub_by_source.map.values()) | {HOLDER.sub_by_source.default}
    for bucket_id in (PROMOTED.id, HOLDER.id):
        with pytest.raises(KeyError):
            destination(DECLARED, bucket_id, FORMER.id)


def test_a_former_place_is_found_in_the_folder_of_the_bucket_that_held_it():
    assert adopt_placements.named_place(DECLARED, PROMOTED.id, FORMER.id) == OLD_PLACE
    assert adopt_placements.named_place(DECLARED, HOLDER.id, FORMER.id) == OLD_PLACE
    assert adopt_placements.recorded_under(DECLARED, HOLDER.id, FORMER.id) == (
        HOLDER.id,
        FORMER.sub,
    )
    assert adopt_placements.named_place(DECLARED, PROMOTED.id, MED) == destination(
        DECLARED, PROMOTED.id, MED
    )
    assert adopt_placements.recorded_under(DECLARED, PROMOTED.id, FORMER.id) == (
        HOLDER.id,
        FORMER.sub,
    )
    assert adopt_placements.recorded_under(DECLARED, PROMOTED.id, MED) == (PROMOTED.id, MED)


# ── the placement reader ───────────────────────────────────────────────────


def _old_node(*content_ids: str, names=OLD_PLACE, ids=("f-old", "p-old")) -> rebuild.TreeNode:
    return rebuild.TreeNode(
        folder_id=ids[0],
        folder_display=names[0],
        playlist_id=ids[1],
        playlist_display=names[1],
        content_ids=frozenset(content_ids),
    )


def test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets():
    found = adopt_placements.placements_from(DECLARED, [_old_node("t")], None)
    assert found.held == _in_old("t")
    assert found.holds_unnamed(PROMOTED.id, "t") == ()
    assert found.holds(ELSEWHERE.id, "t") == ()


def test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub():
    record = convergence.TreeConvergence(
        tree_id=TREE_ID,
        nodes=(
            convergence.DestinationNode(
                bucket=HOLDER.id, sub=FORMER.sub, folder_id="f-old", playlist_id="p-old"
            ),
        ),
    )
    renamed = _old_node("t", names=(HOLDER.display, "Renamed by hand"))
    assert adopt_placements.placements_from(DECLARED, [renamed], None).held == {}
    found = adopt_placements.placements_from(DECLARED, [renamed], record)
    for bucket_id in (PROMOTED.id, HOLDER.id):
        assert found.holds(bucket_id, "t") == (FORMER.id,), bucket_id
        assert found.holds_unnamed(bucket_id, "t") == (FORMER.id,), bucket_id


# ── adoption ───────────────────────────────────────────────────────────────


def test_adoption_withholds_a_track_still_in_the_old_playlist():
    (entry,) = _adoption([_scanned("t", energy=8)], _in_old("t")).entries
    assert entry.disposition is adopt_scan.Disposition.WITHHELD
    assert (entry.bucket, entry.sub, entry.holds) == (PROMOTED.id, HIGH, (FORMER.id,))
    assert entry.held_elsewhere and not entry.applicable


def test_adoption_places_a_track_the_old_playlist_does_not_hold():
    (entry,) = _adoption([_scanned("t", energy=8)], {PROMOTED.id: {}}).entries
    assert entry.applicable and (entry.bucket, entry.sub) == (PROMOTED.id, HIGH)


# ── the move plan ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("energy", "also", "target", "add", "remove"),
    [
        (8, (), HIGH, HIGH, (FORMER.id,)),
        (8, (HIGH,), HIGH, "", (FORMER.id,)),
        (8, (LOW,), HIGH, HIGH, tuple(sorted((FORMER.id, LOW)))),
        # Nothing has to be read to know a playlist the taxonomy stopped
        # declaring is not the track's place, and the no reading sub says
        # nothing false about it.
        (None, (), SINK, SINK, (FORMER.id,)),
        # Filed in the no reading sub by an additive writer while it sat in the
        # old playlist: listing it as left for want of a reading kept it in both.
        (None, (SINK,), SINK, "", (FORMER.id,)),
    ],
    ids=["its-band", "already-in-it", "and-a-stale-band", "no-reading", "no-reading-in-the-sink"],
)
def test_a_track_in_the_old_playlist_leaves_it_for_the_band_its_reading_names(
    energy, also, target, add, remove
):
    plan = _moves([_scanned("t", energy=energy)], _in_old("t", *also))
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add, move.remove, move.energy) == (
        PROMOTED.id,
        target,
        add,
        remove,
        energy,
    )
    # With no reading, its genre sent it here and energy decided nothing.
    decided = adopt_move.DECIDED_BY_ENERGY if energy else adopt_move.DECIDED_BY_GENRE
    assert (move.kind, move.decided_by) == ("band", decided)
    assert plan.left == ()
    assert plan.counts()["memberships_added"] == (1 if add else 0)
    assert plan.counts()["memberships_removed"] == len(remove)


def _unread(genre: str = PROMOTED_GENRE) -> adopt_scan.ScannedTrack:
    return _scanned("t", energy=8, genre=genre, disposition=adopt_scan.Disposition.EXCLUDED)


#: Tracks in the old playlist left and listed, with nothing moved: the track,
#: what it holds, what it holds under another name, and the one row left.
_LEFT_IN_OLD = {
    # A band needs a reading, so a stale band beside the old playlist stays.
    "no-reading-and-a-band": (
        _scanned("t", energy=None), _in_old("t", LOW), {},
        {"bucket": PROMOTED.id, "reason": adopt_move.LEFT_NO_READING,
         "holds": tuple(sorted((FORMER.id, LOW)))},
    ),
    # R-758's rule, unchanged where no former place is held.
    "no-reading-no-former-place": (
        _scanned("t", energy=None), {PROMOTED.id: {"t": (LOW,)}}, {},
        {"reason": adopt_move.LEFT_NO_READING},
    ),
    "renamed-old-playlist": (
        _scanned("t", energy=8), _in_old("t"), _in_old("t"),
        {"reason": adopt_move.LEFT_UNNAMED, "holds_unnamed": (FORMER.id,)},
    ),
    # Claimed by neither bucket: listed once, under the one that took it over.
    "another-folder": (
        _scanned("t", energy=8, genre=ELSEWHERE.display), _in_old("t"), {},
        {"bucket": PROMOTED.id, "reason": adopt_move.LEFT_FORMER, "target": "",
         "holds": (FORMER.id,)},
    ),
    "no-genre": (
        _scanned("t", energy=8, genre=""), _in_old("t"), {},
        {"bucket": PROMOTED.id, "reason": adopt_move.LEFT_FORMER, "target": "",
         "holds": (FORMER.id,)},
    ),
    # A word with no row of its own has no style to move to.
    "defaulted-genre": (
        _scanned("t", energy=8, genre=DEFAULTED_GENRE), _in_old("t"), {},
        {"bucket": HOLDER.id, "reason": adopt_move.LEFT_NO_STYLE},
    ),
    "unread-genre-names-the-old-folder": (
        _unread(STAYING_GENRE), _in_old("t"), {},
        {"bucket": PROMOTED.id, "reason": adopt_move.LEFT_NO_READING},
    ),
    "unread": (
        _unread(), _in_old("t"), {},
        {"reason": adopt_move.LEFT_NO_READING, "holds": (FORMER.id,)},
    ),
}  # fmt: skip


@pytest.mark.parametrize("case", sorted(_LEFT_IN_OLD))
def test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason(case):
    track, held, unnamed, expected = _LEFT_IN_OLD[case]
    plan = _moves([track], held, unnamed=unnamed)
    assert plan.moves == ()
    (left,) = plan.left
    assert {name: getattr(left, name) for name in expected} == expected
    assert plan.counts()["left"] == _left_counts(**{expected["reason"]: 1})


def test_a_track_in_the_old_playlist_whose_genre_names_another_style_moves_to_that_style():
    """Found by the review. The old playlist competed in its folder until the
    promotion, and a track there with another style's genre was moved to that
    style. Competing in the promoted bucket alone, adoption added the style
    and nothing ever took the track out of the old playlist."""
    tracks = [_scanned("t", energy=8, genre=STAYING_GENRE)]
    (entry,) = _adoption(tracks, _in_old("t")).entries
    assert entry.held_elsewhere and not entry.applicable
    assert (entry.bucket, entry.sub) == (HOLDER.id, STAYING_SUB)

    plan = _moves(tracks, _in_old("t"))
    (move,) = plan.moves
    assert (move.bucket, move.target, move.add, move.remove) == (
        HOLDER.id,
        STAYING_SUB,
        STAYING_SUB,
        (FORMER.id,),
    )
    assert (move.kind, move.decided_by) == ("style", "genre")
    # ONCE. It is not listed as left under the bucket that declares the place.
    assert plan.left == ()


@pytest.mark.parametrize("band", [HIGH, LOW], ids=["its-reading", "another-band"])
def test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one(band):
    """Found by the second review. The track's genre names a style of the old
    folder and it sits in the old playlist and in a band of the promoted
    bucket. Both buckets planned leaving the one membership, or one moved the
    track while the other listed it as left beside that move."""
    held = {PROMOTED.id: {"t": (FORMER.id, band)}, HOLDER.id: {"t": (FORMER.id,)}}
    plan = _moves([_scanned("t", energy=8, genre=STAYING_GENRE)], held)
    (move,) = plan.moves
    assert (move.bucket, move.add, move.remove) == (HOLDER.id, STAYING_SUB, (FORMER.id,))
    assert plan.left == ()
    assert plan.counts()["memberships_removed"] == 1


def test_a_former_place_held_twice_is_not_listed_beside_the_move_that_leaves_it():
    held = _in_old("t")
    current = _adoption([_scanned("t", energy=8, genre=STAYING_GENRE)], held)
    doubled = replace(
        current,
        placements=adopt_plan.Placements(read=True, held=held, doubled=held),
    )
    plan = adopt_move.build_move_plan(doubled, DECLARED)
    assert [move.bucket for move in plan.moves] == [HOLDER.id]
    assert plan.left == ()


@pytest.mark.parametrize("genre", [STAYING_GENRE, PROMOTED_GENRE], ids=["holder", "promoted"])
def test_a_verdict_on_the_bucket_the_genre_names_is_the_reason_a_track_there_is_left(genre):
    refused = _refused_over([_scanned("t", energy=8, genre=genre)], _in_old("t"))
    plan = adopt_move.build_move_plan(refused, DECLARED)
    assert plan.moves == ()
    (left,) = plan.left
    assert (left.bucket, left.reason) == (PROMOTED.id, adopt_move.LEFT_VERDICT)


def test_a_genre_only_the_fallback_tier_lands_is_not_read_as_naming_the_bucket():
    """A taxonomy whose fallback bucket is the promoted one. A word nothing
    claims lands there, and that is not the genre naming it."""
    import tomllib

    data = tomllib.loads(taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME))
    data["fallback"]["bucket"] = PROMOTED.id
    data["fallback"]["too_coarse_as_source"] = [""]
    declared = taxonomy.build_taxonomy(data)
    word = "Zydeco"
    assert routing.resolve_bucket(declared, word).match is routing.Match.FALLBACK
    assert routing.resolve_bucket(declared, word).bucket_id == PROMOTED.id
    track = adopt_scan.ScannedTrack(
        content_id="t",
        recorded="/library/Music/t.flac",
        path="/library/Music/t.flac",
        readability=adopt_scan.Readability.READABLE,
        disposition=adopt_scan.Disposition.NEEDS_GENRE,
        genre=word,
        energy=8,
    )
    current = adopt_plan.build_adoption_plan(
        [track],
        declared,
        tree=TREE_ID,
        placements=adopt_plan.Placements(read=True, held=_in_old("t")),
    )
    (left,) = adopt_move.build_move_plan(current, declared).left
    assert left.reason == adopt_move.LEFT_FORMER


def test_a_track_whose_genre_lands_in_the_old_folders_default_is_withheld():
    """Not added to the default sub beside the old playlist; listed above."""
    assert DEFAULTED_GENRE not in HOLDER.sub_by_source.map
    (entry,) = _adoption([_scanned("t", energy=8, genre=DEFAULTED_GENRE)], _in_old("t")).entries
    assert entry.held_elsewhere and not entry.applicable


def test_a_track_in_one_live_sub_of_a_bucket_its_genre_does_not_name_is_still_not_asked():
    """The former place is the one exception to R-780's rule, and only it."""
    plan = _moves([_scanned("t", energy=8, genre=STAYING_GENRE)], {PROMOTED.id: {"t": (HIGH,)}})
    assert plan.moves == () and plan.left == ()


def test_an_entry_naming_a_former_place_as_its_sub_is_never_a_move():
    """No resolver builds one. Somebody did, and nothing is filed into it."""
    current = _adoption([_scanned("t", energy=8)], {PROMOTED.id: {"t": (HIGH,)}})
    forged = replace(
        current, entries=tuple(replace(entry, sub=FORMER.id) for entry in current.entries)
    )
    plan = adopt_move.build_move_plan(forged, DECLARED)
    assert plan.moves == ()


def test_the_digest_moves_when_a_track_turns_up_in_the_old_playlist():
    tracks = [_scanned("t", energy=8, genre=ELSEWHERE.display)]
    without = _moves(tracks, {PROMOTED.id: {}})
    with_one = _moves(tracks, _in_old("t"))
    assert without.digest() != with_one.digest()


# ── the writer's list ──────────────────────────────────────────────────────


def _approved() -> adopt_move.Move:
    (move,) = _moves([_scanned("t", energy=8)], _in_old("t")).moves
    return move


def test_the_writer_is_told_to_leave_the_old_playlist_by_its_own_names():
    (written,) = move_cli.membership_moves([_approved()], DECLARED)
    assert written.target == destination(DECLARED, PROMOTED.id, HIGH)
    assert written.remove == (OLD_PLACE,)

    (style,) = _moves([_scanned("t", energy=8, genre=STAYING_GENRE)], _in_old("t")).moves
    (written,) = move_cli.membership_moves([style], DECLARED)
    assert written.target == destination(DECLARED, HOLDER.id, STAYING_SUB)
    assert written.remove == (OLD_PLACE,)


def test_a_move_whose_target_is_a_former_place_is_refused_and_nothing_is_written():
    approved = _approved()
    fields = {name: getattr(approved, name) for name in approved.__slots__}
    fields.update(target=FORMER.id, add=FORMER.id, remove=(HIGH,))
    with pytest.raises(Exception) as raised:
        move_cli.membership_moves([adopt_move.Move(**fields)], DECLARED)
    assert raised.value.cause.reason == "decision-stale"


def test_the_worker_narrows_a_move_whose_band_landed_to_the_removal_alone():
    current = _adoption([_scanned("t", energy=8)], _in_old("t", HIGH))
    todo, gone = move_cli.remaining([_approved()], current, DECLARED)
    assert ([(move.add, move.remove) for move in todo], gone) == ([("", (FORMER.id,))], ())


def test_the_worker_finds_a_finished_move_done():
    current = _adoption([_scanned("t", energy=8)], {PROMOTED.id: {"t": (HIGH,)}})
    assert move_cli.remaining([_approved()], current, DECLARED) == ((), ())


@pytest.mark.parametrize("genre", [STAYING_GENRE, ELSEWHERE.display, ""])
def test_a_genre_that_left_the_promoted_bucket_since_the_approval_is_a_stale_decision(genre):
    current = _adoption([_scanned("t", energy=8, genre=genre)], _in_old("t"))
    with pytest.raises(Exception) as raised:
        move_cli.remaining([_approved()], current, DECLARED)
    assert raised.value.cause.reason == "decision-stale"


# ---------------------------------------------------------------------------
# The verb, against a disposable library filed under the old shape
# ---------------------------------------------------------------------------

#: Content identifier, genre, energy tag, and the places seeded: ``old`` is the
#: playlist the promotion left, anything else a band of the promoted bucket.
_SEEDED = (
    ("r-reads-high", PROMOTED.aliases[0], "8", ("old",)),
    ("r-reads-low", PROMOTED.aliases[-1], "2", ("old",)),
    ("r-reads-med", PROMOTED.aliases[0], "5", ("old",)),
    ("r-already-in-band", PROMOTED.aliases[-1], "5", ("old", MED)),
    ("r-no-reading", PROMOTED_GENRE, None, ("old",)),
    ("r-by-hand", STAYING_GENRE, "5", ("old",)),
    ("r-no-genre", "", "5", ("old",)),
)
_MOVED = {
    "r-reads-high", "r-reads-low", "r-reads-med", "r-already-in-band", "r-no-reading", "r-by-hand"
}  # fmt: skip
_LEFT = {"r-no-genre"}
#: Where each track of the promoted genre ends: its band, or the no reading sub.
_BAND = {
    "r-reads-high": HIGH,
    "r-reads-low": LOW,
    "r-reads-med": MED,
    "r-already-in-band": MED,
    "r-no-reading": SINK,
}


def old_shape_text() -> str:
    """The shipped template with the promotion undone, as a library's own copy.

    A library set up before R-797 holds this shape until a person edits it.
    Rebuilt from the shipped text so that everything else in it stays the
    shipped template, and checked below to be the shape it claims.

    THE BUCKET SPLIT OUT OF THE PROMOTED ONE GOES TOO (U118). Its words were
    the old sub's, and its split places name a bucket this shape has not got.
    Hip-Hop's promotion stays, which is a shape no library held, and is kept
    because only R&B's is being undone here.
    """
    text = taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)
    start = text.index("# R&B AT THE TOP LEVEL")
    end = text.index("# HIP-HOP AT THE TOP LEVEL")
    assert f'id = "{SPLIT.id}"' in text[start:end]
    text = text[:start] + text[end:]
    words = (*PROMOTED.aliases, *SPLIT.aliases)
    aliases = "".join(f'  "{alias}",\n' for alias in words)
    anchor = f'[[bucket]]\nid = "{HOLDER.id}"\n'
    head, tail = text.split(anchor)
    opening, rest = tail.split("aliases = [\n", 1)
    tail = f"{opening}aliases = [\n{aliases}{rest}"
    sub = (
        f'[[bucket.sub]]\nid = "{FORMER.sub}"\ndisplay = "{FORMER.display}"\n\n'
        "[bucket.sub_by_source]\n"
    )
    assert tail.count("[bucket.sub_by_source]\n") == 1
    tail = tail.replace("[bucket.sub_by_source]\n", sub)
    rows = "".join(f'  {{ source = "{alias}", sub = "{FORMER.sub}" }},\n' for alias in words)
    assert tail.count("map = [\n") == 1
    tail = tail.replace("map = [\n", f"map = [\n{rows}")
    return head + anchor + tail


def test_the_old_shape_is_the_shape_before_the_promotion():
    old = taxonomy.load_taxonomy(old_shape_text())
    assert PROMOTED.id not in old.bucket_ids() and SPLIT.id not in old.bucket_ids()
    assert FORMER.id not in {place.id for bucket in old.buckets for place in bucket.formerly}
    assert all(not bucket.split_from for bucket in old.buckets)
    for alias in (*PROMOTED.aliases, *SPLIT.aliases):
        assert routing.resolve_bucket(old, alias).bucket_id == HOLDER.id
        assert routing.energy_sub(old, HOLDER.id, 5, source_genre=alias).id == FORMER.sub
    assert destination(old, HOLDER.id, FORMER.sub) == OLD_PLACE


def _band_place(sub_id: str) -> tuple[str, str]:
    return destination(DECLARED, PROMOTED.id, sub_id)


@pytest.fixture
def promoted(machine, silence):  # noqa: F811
    """A cut over library whose R&B tracks still sit in the old playlist."""
    tracks = [(content_id, genre, tag) for content_id, genre, tag, _held in _SEEDED]
    places = [
        (*(OLD_PLACE if place == "old" else _band_place(place)), content_id)
        for content_id, _genre, _tag, held in _SEEDED
        for place in held
    ]
    tracks.append(("r-staying", STAYING_GENRE, None))
    places.append((*destination(DECLARED, HOLDER.id, STAYING_SUB), "r-staying"))
    seed_library(machine, silence, tracks, places, on=date(2026, 10, 1))
    return machine


def test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left(promoted):
    shown = _shown(VERB)
    rows = {row["content_id"]: row for row in shown["items"]}
    assert set(rows) == _MOVED and len(shown["items"]) == len(_MOVED)
    for content_id, band in _BAND.items():
        row = rows[content_id]
        assert row["bucket"] == PROMOTED.id and row["remove"] == [FORMER.id], content_id
        assert row["target"] == band, content_id
    assert rows["r-already-in-band"]["add"] == ""
    assert rows["r-reads-high"]["add"] == HIGH
    # The track a person filed there under another style's genre goes to that
    # style, in the folder that holds the old playlist.
    by_hand = rows["r-by-hand"]
    assert (by_hand["bucket"], by_hand["add"], by_hand["remove"]) == (
        HOLDER.id,
        STAYING_SUB,
        [FORMER.id],
    )
    assert (rows["r-no-reading"]["add"], rows["r-no-reading"]["energy"]) == (SINK, None)
    left = [(row["content_id"], row["reason"]) for row in shown["left"]]
    assert left == [("r-no-genre", adopt_move.LEFT_FORMER)]

    # Adoption over the same library files none of them a second time.
    plan = apply_cli.current_plan(promoted, DECLARED)
    entries = {entry.content_id: entry for entry in plan.entries}
    for content_id in ("r-reads-high", "r-reads-low", "r-reads-med", "r-no-reading", "r-by-hand"):
        assert entries[content_id].held_elsewhere, content_id
        assert not entries[content_id].applicable, content_id


def test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing(promoted):
    before = _live(promoted)
    job_id, code, resumed = _approve_and_run()
    assert code == int(ExitCode.OK), resumed
    after, removed = _live(promoted), _removed(promoted)

    for content_id, band in _BAND.items():
        assert after[content_id] == {_band_place(band)}, content_id
        assert removed[content_id] == {OLD_PLACE}, content_id
    assert after["r-by-hand"] == {destination(DECLARED, HOLDER.id, STAYING_SUB)}
    assert removed["r-by-hand"] == {OLD_PLACE}
    # NO TRACK IS IN BOTH, which is R8, asked of every track in the library:
    # whatever still sits in the old playlist sits nowhere else.
    for content_id, places in after.items():
        assert not (OLD_PLACE in places and len(places) > 1), content_id
    # Left where they were, and nothing of theirs removed.
    for content_id in (*_LEFT, "r-staying"):
        assert after[content_id] == before[content_id], content_id
        assert content_id not in removed, content_id

    report = artifacts.committed(promoted, job_id)[-1]
    assert (report["added"], report["already_present"]) == (5, 1)
    assert (report["removed"], report["already_absent"]) == (6, 0)
    assert sorted(report["moved"]) == sorted(_MOVED)
    assert report["in_both"] == report["untouched"] == report["neither"] == []

    # A second run after the move plans nothing and writes nothing.
    rows = _rows(promoted)
    collection.reset_cache()
    shown = _shown(VERB)
    assert shown["items"] == [] and shown["counts"]["moves"] == 0
    assert {row["content_id"] for row in shown["left"]} == _LEFT
    code, envelope = _decided("approve")
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "no-op"
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 1
    assert _rows(promoted) == rows


def test_a_library_whose_own_taxonomy_still_has_the_sub_moves_no_track_of_that_sub(promoted):
    """Until a person edits the library's copy, the old shape holds and nothing
    is filed twice: the tracks are where that taxonomy says they belong.

    THE ONE MOVE IT DOES PLAN IS THE OLD SHAPE'S OWN. The track a person filed
    there by hand carries another style's genre, and under the old taxonomy
    the playlist is a live style sub, so R-758's rule moves it to its style.
    """
    target = config.state_path("taxonomy_active", promoted)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(old_shape_text(), encoding="utf-8")
    rows = _rows(promoted)

    shown = _shown(VERB)
    assert [(row["content_id"], row["bucket"]) for row in shown["items"]] == [
        ("r-by-hand", HOLDER.id)
    ]
    assert PROMOTED.id not in {row["bucket"] for row in (*shown["items"], *shown["left"])}

    from cratekit.core import active_taxonomy

    old = active_taxonomy.load(promoted)
    assert PROMOTED.id not in old.bucket_ids()
    plan = apply_cli.current_plan(promoted, old)
    entries = {entry.content_id: entry for entry in plan.entries}
    for content_id in ("r-reads-high", "r-reads-low", "r-reads-med", "r-already-in-band"):
        assert (entries[content_id].bucket, entries[content_id].sub) == (HOLDER.id, FORMER.sub), (
            content_id
        )
    assert _rows(promoted) == rows
