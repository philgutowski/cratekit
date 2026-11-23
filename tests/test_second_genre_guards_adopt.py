"""R-1950: the guards on adoption's second genre paths, each pinned by a test.

U340 gave a track a second entry for its second genre folder. These pin the
guards round one of its review removed with nothing red: the second entry is
built only for a track that routes, only where the second folder declares a
place for the reading, under the second genre's own word, shown as such on the
review list; a split place is kept only beside an entry that files the track;
and an entry that does not claim its bucket never hides that bucket from the
track's other entry in ``adopt move``.

Where no shipped bucket lacks a place for a reading, the shipped template is
given one, R&B with no place below it, so the guard has an input to answer.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from cratekit.adopt import move as adopt_move
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.core import routing, taxonomy
from tests.test_adopt_move import _with_verdict_on
from tests.test_adopt_vocals import _with_bucket
from tests.test_second_genre import (
    DECLARED,
    DEEP,
    MED,
    ONE,
    RNB,
    SOUL,
    TECH,
    TREE_ID,
    TWO,
    _plan,
    _split_pair,
    _two,
)

ROUTE, WITHHELD = adopt_scan.Disposition.ROUTE, adopt_scan.Disposition.WITHHELD
SOUL_ID, RNB_ID = (DECLARED.bucket_for_display(word) for word in (SOUL, RNB))
#: Soul's split place over R&B's middle band: the track sits in R&B's band.
SPLIT_MED = next(place.id for place in DECLARED.bucket(SOUL_ID).split_from if place.sub == MED)
#: The shipped template with R&B declaring no place below it for any reading.
NO_RNB_PLACE = _with_bucket(
    replace(DECLARED.bucket(RNB_ID), energy=taxonomy.BucketEnergy(enabled=False), single_sub=None)
)


def _rows(plan: adopt_plan.AdoptionPlan) -> list[tuple]:
    return [(e.bucket, e.sub, e.disposition, e.withheld_by, e.second) for e in plan.entries]


def test_the_template_given_here_has_rnb_with_no_place_and_soul_as_shipped():
    assert routing.energy_sub(NO_RNB_PLACE, RNB_ID, 5, source_genre=RNB) is None
    assert routing.energy_sub(NO_RNB_PLACE, SOUL_ID, 5, source_genre=SOUL).id == MED
    assert routing.second_bucket(NO_RNB_PLACE, SOUL, RNB) == RNB_ID
    assert routing.second_bucket(NO_RNB_PLACE, RNB, SOUL) == SOUL_ID


# A01: only a track that routes by its first genre gets a second entry.


@pytest.mark.parametrize(
    "disposition",
    [
        WITHHELD,
        adopt_scan.Disposition.NEEDS_GENRE,
        adopt_scan.Disposition.EXCLUDED,
        adopt_scan.Disposition.UNDECLARED,
    ],
)
def test_a_track_that_does_not_route_gets_no_second_entry_whatever_its_census_says(disposition):
    """The census reads a second genre only for a routed track, so this row is
    built by hand: a second bucket on a track that does not route."""
    track = replace(_two("t", energy=8), disposition=disposition)
    assert track.second_bucket == TWO
    plan = _plan([track], {})
    assert [(e.content_id, e.second) for e in plan.entries] == [("t", False)]
    assert plan.seconds() == ()


# A02: no second entry where the second folder declares no place for the reading.


def test_a_second_folder_with_no_place_for_the_reading_files_nothing_and_keeps_nothing():
    """Soul first, R&B second, and R&B declares no place: one entry, Soul's,
    and R&B's band held in Soul is a competing place, as for one genre."""
    plan = adopt_plan.build_adoption_plan(
        [_split_pair("t", SOUL, RNB, energy=5)],
        NO_RNB_PLACE,
        tree=TREE_ID,
        placements=adopt_plan.Placements(read=True, held={SOUL_ID: {"t": (SPLIT_MED,)}}),
    )
    assert _rows(plan) == [(SOUL_ID, MED, WITHHELD, "band", False)]
    (entry,) = plan.entries
    assert entry.holds == (SPLIT_MED,)


# A03 and A04: the second entry carries the second genre's word, and shows it.


def test_the_second_entry_carries_the_second_genres_word():
    plan = _plan([_two("t", energy=8)], {})
    first, second = plan.entries
    assert (first.genre, second.genre) == (DEEP, TECH)
    rows = adopt_plan.to_json(plan)["entries"]
    assert [row.get("second_genre") for row in rows] == [None, TECH]


def test_the_second_entrys_band_is_chosen_by_the_second_genres_word():
    """NonElectronic files by the source word: a Deep House track whose second
    genre is Folk is planned into Folk there, never into the band its first
    genre's word would name."""
    plan = _plan([_two("t", energy=8, second="Folk")], {})
    assert [(e.bucket, e.sub, e.second) for e in plan.entries] == [
        (ONE, "high", False),
        ("non_electronic", "folk", True),
    ]


def test_the_review_row_names_the_second_genre_on_a_second_entry_only():
    plan = _plan([_two("t", energy=8)], {ONE: {"t": (MED,)}, TWO: {"t": (MED,)}})
    first, second = plan.entries
    assert (first.held_elsewhere, second.held_elsewhere) == (True, True)
    assert adopt_plan.review_row(second)["second_genre"] == TECH
    assert "second_genre" not in adopt_plan.review_row(first)
    shown = adopt_plan.to_json(plan)["held_elsewhere"]
    assert [(row["bucket"], row.get("second_genre")) for row in shown] == [(ONE, None), (TWO, TECH)]


# A05: the second entry keeps a split place only beside a first entry that files.


def test_a_second_entry_keeps_no_split_place_beside_a_first_folder_with_no_place():
    """R&B first and declaring no place, Soul second: nothing files the track
    into R&B, so R&B's band held in Soul is a competing place for Soul."""
    plan = adopt_plan.build_adoption_plan(
        [_split_pair("t", RNB, SOUL, energy=5)],
        NO_RNB_PLACE,
        tree=TREE_ID,
        placements=adopt_plan.Placements(read=True, held={SOUL_ID: {"t": (SPLIT_MED,)}}),
    )
    assert _rows(plan) == [
        ("", "", adopt_scan.Disposition.UNDECLARED, "", False),
        (SOUL_ID, MED, WITHHELD, "band", True),
    ]
    assert plan.entries[1].holds == (SPLIT_MED,)


# A06: an entry that does not claim its bucket hides it from no other entry.


def test_a_second_entry_a_verdict_withheld_claims_no_bucket():
    plan = _with_verdict_on(_plan([_two("t", energy=8)], {}), TWO)
    first, second = plan.entries
    assert (second.bucket, second.disposition, second.withheld_by) == (TWO, WITHHELD, "verdict")
    claimed = adopt_move.claimed_buckets(plan.entries)
    assert claimed == {"t": frozenset({ONE})}
    assert adopt_move.elsewhere_of(claimed, first) == frozenset()
    assert adopt_move.elsewhere_of(claimed, second) == frozenset({ONE})
