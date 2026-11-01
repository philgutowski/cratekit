"""U155: a sub chosen by genre inside a bucket that splits by energy.

Phillip tags every PULS release ``Rominimal`` and wants those tracks in a place
of their own under Minimal / Deep Tech, beside the bucket's energy bands and
not instead of them. A genre sub is that place. It is ADDITIVE: a Rominimal
track files into its band exactly as before and into the genre sub as well,
and a Minimal track never reaches the sub.

Every expected value here is spelled from the brief or read from a second
taxonomy built WITHOUT the genre sub, never from the code under test, so a
comparison cannot reduce to the derivation agreeing with itself.
"""

from __future__ import annotations

import copy
import tomllib
from importlib import resources

import pytest

from cratekit.adopt import plan as adopt_plan
from cratekit.core import routing
from cratekit.core.taxonomy import (
    GENRE_SUB_SCHEMA_VERSION,
    TaxonomyError,
    build_taxonomy,
    default_taxonomy,
    live_places,
)
from cratekit.write import rebuild, routing_pass

BUCKET = "minimal_deep_tech"
FOLDER = "Minimal / Deep Tech"
GENRE = "Rominimal"
SUB = "rominimal"


@pytest.fixture(scope="module")
def default():
    return default_taxonomy()


@pytest.fixture(scope="module")
def default_raw() -> dict:
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    return tomllib.loads(source.read_text(encoding="utf-8"))


def _bucket(data: dict, bucket_id: str) -> dict:
    (found,) = [entry for entry in data["bucket"] if entry["id"] == bucket_id]
    return found


def _mutated(raw: dict, mutate) -> dict:
    data = copy.deepcopy(raw)
    mutate(data)
    return data


def _problems(raw: dict, mutate) -> tuple[str, ...]:
    with pytest.raises(TaxonomyError) as caught:
        build_taxonomy(_mutated(raw, mutate))
    return caught.value.problems


@pytest.fixture(scope="module")
def without(default_raw):
    """The shipped template as it was before U155: no genre sub, no Rominimal alias."""

    def strip(data):
        bucket = _bucket(data, BUCKET)
        del bucket["genre_sub"]
        bucket["aliases"] = [alias for alias in bucket["aliases"] if alias != GENRE]
        data["schema_version"] = 4

    return build_taxonomy(_mutated(default_raw, strip))


def _truth(genre: str | None, energy: int | None, name: str = "a.flac") -> rebuild.Truth:
    return rebuild.Truth(location=f"/music/{name}", genre=genre, energy=energy, voxlevel=None)


def _derive(declared, truth):
    placements, gaps = rebuild.derive_from_taxonomy(declared, truth, vocal_threshold=None)
    return placements, gaps


# ---------------------------------------------------------------------------
# The brief's routing scenarios
# ---------------------------------------------------------------------------


def test_a_rominimal_track_at_energy_3_lands_in_its_band_and_in_rominimal(default):
    placements, gaps = _derive(default, [_truth(GENRE, 3)])
    assert sorted((p.bucket, p.sub) for p in placements) == [(BUCKET, "low"), (BUCKET, SUB)]
    # The vocal dimension is the only gap with no calibration; the genre sub
    # is read off the same genre as the bucket and is never one.
    assert gaps == (rebuild.VOCAL_DIMENSION,)
    assert routing.resolve_bucket(default, GENRE).match is routing.Match.EXACT
    assert routing_pass.destination(default, BUCKET, "low") == (FOLDER, "Low Energy")
    assert routing_pass.destination(default, BUCKET, SUB) == (FOLDER, "Rominimal")


def test_a_minimal_track_at_energy_3_lands_in_its_band_and_not_in_rominimal(default):
    placements, _gaps = _derive(default, [_truth("Minimal", 3)])
    assert [(p.bucket, p.sub) for p in placements] == [(BUCKET, "low")]
    assert routing.genre_sub(default, BUCKET, "Minimal") is None


@pytest.mark.parametrize("spelling", ["rominimal", "ROMINIMAL", "Rominimal ", "Rominimal Techno"])
def test_only_the_exact_source_reaches_the_genre_sub(default, spelling):
    """Case sensitive and whole, like a source map row: a near spelling still
    files into the bucket by the keyword rule and its band, never the sub."""
    assert routing.genre_sub(default, BUCKET, spelling) is None
    placements, _gaps = _derive(default, [_truth(spelling, 3)])
    assert SUB not in {p.sub for p in placements}


def test_a_rominimal_track_with_no_reading_lands_in_unsorted_and_in_rominimal(default):
    placements, _gaps = _derive(default, [_truth(GENRE, None)])
    assert sorted(p.sub for p in placements) == [SUB, "unsorted"]


def test_the_genre_sub_is_additive_so_it_never_competes(default, without):
    """Additive, pinned: the band a track files into is the same with the sub
    declared or not, and the sub is never one of the bucket's competing subs."""
    for level in (None, *range(1, default.energy.scale_max + 1)):
        assert routing.energy_sub(
            default, BUCKET, level, source_genre=GENRE
        ) == routing.energy_sub(without, BUCKET, level, source_genre="Minimal")
    assert routing.competing_subs(default, BUCKET) == routing.competing_subs(without, BUCKET)
    assert SUB not in routing.competing_subs(default, BUCKET)[1]


def test_every_other_bucket_routes_exactly_as_before(default, without):
    """A bucket that routes by source genre keeps today's behaviour exactly,
    and so does every bucket that declares no genre sub."""
    by_source = [b for b in default.buckets if b.sub_by_source is not None]
    assert by_source, "the shipped template has a bucket that routes by source genre"
    for bucket in default.buckets:
        if bucket.id == BUCKET:
            continue
        assert bucket.genre_subs == ()
        assert bucket == without.bucket(bucket.id)
        assert routing.competing_subs(default, bucket.id) == routing.competing_subs(
            without, bucket.id
        )
        sources = list(bucket.aliases)
        if bucket.sub_by_source is not None:
            sources += list(bucket.sub_by_source.map)
        for source in sources:
            assert routing.genre_sub(default, bucket.id, source) is None
            for level in (None, 1, 5, 10):
                assert routing.energy_sub(
                    default, bucket.id, level, source_genre=source
                ) == routing.energy_sub(without, bucket.id, level, source_genre=source)


def test_route_resort_moves_the_96_puls_tracks_additively(default, without):
    """The 96 PULS tracks landed on 2026-10-27, across every energy and none.

    Measured against the same readings derived without the genre sub: every
    placement that derivation makes is still made, and the only addition is
    each Rominimal track in the genre sub, once.
    """
    levels = [None, *range(1, default.energy.scale_max + 1)]
    puls = [_truth(GENRE, levels[i % len(levels)], f"puls-{i:03d}.flac") for i in range(96)]
    others = [_truth("Minimal", 4, "minimal.flac"), _truth("Deep House", 8, "deep.flac")]
    after, _ = _derive(default, puls + others)
    as_minimal = [_truth("Minimal", t.energy, t.location.rsplit("/", 1)[1]) for t in puls]
    before, _ = _derive(without, as_minimal + others)

    added = set(after) - set(before)
    assert set(before) <= set(after)
    assert len(added) == 96
    assert {(p.bucket, p.sub) for p in added} == {(BUCKET, SUB)}
    assert {p.location for p in added} == {t.location for t in puls}


# ---------------------------------------------------------------------------
# The tagger keeps the word that names the sub
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("seen", ["Rominimal", "rominimal", "ROMINIMAL"])
def test_the_tagger_writes_rominimal_rather_than_the_buckets_name(default, seen):
    """The "minimal" substring rule would rewrite the file to the bucket's
    name and take the track out of the very sub its genre names."""
    suggestion = routing.suggest_tag(default, seen)
    assert suggestion.tag == GENRE
    assert (suggestion.bucket_id, suggestion.sub_id) == (BUCKET, SUB)
    assert not suggestion.declined and not suggestion.off_taxonomy


def test_the_tagger_still_writes_the_buckets_name_for_minimal(default):
    assert routing.suggest_tag(default, "minimal").tag == FOLDER


def test_the_tagger_writes_the_source_it_matched_when_a_sub_has_two(default_raw):
    def two(data):
        bucket = _bucket(data, BUCKET)
        bucket["aliases"].append("Romanian Minimal")
        bucket["genre_sub"][0]["sources"] = [GENRE, "Romanian Minimal"]

    declared = build_taxonomy(_mutated(default_raw, two))
    assert routing.suggest_tag(declared, "romanian minimal").tag == "Romanian Minimal"
    assert routing.suggest_tag(declared, "rominimal").tag == GENRE
    assert routing.genre_sub(declared, BUCKET, "Romanian Minimal").id == SUB


# ---------------------------------------------------------------------------
# One list of what a folder can hold
# ---------------------------------------------------------------------------


def test_live_places_names_the_genre_sub(default):
    ids, displays = live_places(default.bucket(BUCKET), default.energy, default.sub_classes)
    assert SUB in ids and "Rominimal" in displays


def test_a_former_place_naming_the_genre_sub_is_refused_through_that_list(default_raw):
    def former(data):
        data["schema_version"] = GENRE_SUB_SCHEMA_VERSION
        _bucket(data, "techno").setdefault("formerly", []).append(
            {"id": "old_rominimal", "bucket": BUCKET, "sub": SUB, "display": "Rominimal"}
        )

    problems = _problems(default_raw, former)
    assert any("still declares the sub 'rominimal'" in p for p in problems)
    assert any("still holds a sub named 'Rominimal'" in p for p in problems)


def test_the_adoption_plans_vocal_sub_is_unchanged(default, without):
    for bucket in default.buckets:
        assert adopt_plan.vocal_sub(default, bucket.id) == adopt_plan.vocal_sub(without, bucket.id)


# ---------------------------------------------------------------------------
# The loader refuses a genre sub that is not a place of its own, by name
# ---------------------------------------------------------------------------


def _genre(data: dict) -> dict:
    return _bucket(data, BUCKET)["genre_sub"][0]


@pytest.mark.parametrize(
    "field,value,said",
    [
        ("display", "Low Energy", "display 'Low Energy' is already the name of a band"),
        ("display", "Unsorted", "display 'Unsorted' is already the name of a band"),
        ("display", "with vox", "display 'with vox' is already the name of a band"),
        ("display", "Favorites", "display 'Favorites' is already the name of a band"),
        ("id", "low", "id 'low' is already a band"),
        ("id", "unsorted", "id 'unsorted' is already a band"),
        ("id", "with_vox", "id 'with_vox' is already a band"),
        ("id", "candy", "id 'candy' is already a band"),
    ],
)
def test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name(
    default_raw, field, value, said
):
    def collide(data):
        _genre(data)[field] = value

    problems = _problems(default_raw, collide)
    assert any(f"[[bucket]] {BUCKET} genre_sub" in p and said in p for p in problems), problems


def test_a_band_display_that_is_not_this_buckets_label_is_free(default_raw):
    """The bucket labels its bands Low Energy and so on, so the global label
    Low names no playlist in its folder and is not a collision."""
    declared = build_taxonomy(_mutated(default_raw, lambda d: _genre(d).update(display="Low")))
    assert routing.genre_sub(declared, BUCKET, GENRE).display == "Low"


def test_two_genre_subs_of_one_name_are_refused(default_raw):
    def twice(data):
        bucket = _bucket(data, BUCKET)
        bucket["aliases"].append("Romanian Minimal")
        bucket["genre_sub"].append(
            {"id": "romanian", "display": "Rominimal", "sources": ["Romanian Minimal"]}
        )

    assert any("display 'Rominimal' is already the name" in p for p in _problems(default_raw, twice))


def test_two_genre_subs_of_one_identifier_are_refused_by_that_name(default_raw):
    """Loaded, the second would resolve to the first's playlist and its
    source's tracks would file there."""

    def twice(data):
        bucket = _bucket(data, BUCKET)
        bucket["aliases"].append("Romanian Minimal")
        bucket["genre_sub"].append(
            {"id": SUB, "display": "Romanian", "sources": ["Romanian Minimal"]}
        )

    assert any(
        "id 'rominimal' is already another genre sub of this bucket" in p
        for p in _problems(default_raw, twice)
    )


def test_one_source_in_two_genre_subs_is_refused(default_raw):
    def twice(data):
        _bucket(data, BUCKET)["genre_sub"].append(
            {"id": "again", "display": "Again", "sources": [GENRE]}
        )

    assert any(
        "source 'Rominimal' already names the genre sub 'rominimal'" in p
        for p in _problems(default_raw, twice)
    )


def test_a_source_that_is_not_an_exact_alias_of_the_bucket_is_refused(default_raw):
    def unaliased(data):
        bucket = _bucket(data, BUCKET)
        bucket["aliases"] = [alias for alias in bucket["aliases"] if alias != GENRE]

    problems = _problems(default_raw, unaliased)
    assert any("source 'Rominimal' is not an exact alias of this bucket" in p for p in problems)


def test_a_source_another_bucket_routes_is_refused(default_raw):
    def elsewhere(data):
        _genre(data)["sources"] = ["Deep House"]

    problems = _problems(default_raw, elsewhere)
    assert any("source 'Deep House' is not an exact alias of this bucket" in p for p in problems)


@pytest.mark.parametrize("sources", [[], "Rominimal", [1], None])
def test_sources_must_be_a_non_empty_list_of_words(default_raw, sources):
    def bad(data):
        if sources is None:
            del _genre(data)["sources"]
        else:
            _genre(data)["sources"] = sources

    assert any("sources must be a non-empty list" in p for p in _problems(default_raw, bad))


def test_an_identifier_that_is_not_one_is_refused(default_raw):
    problems = _problems(default_raw, lambda d: _genre(d).update(id="Rominimal"))
    assert any("id 'Rominimal' must match" in p for p in problems)


def test_an_empty_display_is_refused(default_raw):
    problems = _problems(default_raw, lambda d: _genre(d).update(display=""))
    assert any("genre_sub" in p and "display must be a non-empty string" in p for p in problems)


@pytest.mark.parametrize("version", [1, 2, 3, 4])
def test_a_genre_sub_under_an_older_schema_version_is_refused_by_name(default_raw, version):
    """An older build reads the version and ignores the key, so it would file
    the genre's tracks into their band alone and call the sub nobody's."""

    def older(data):
        data["schema_version"] = version
        if version < 4:
            data["sub_class"] = [c for c in data["sub_class"] if c.get("signal") != "playlist"]
        if version < 3:
            for bucket in data["bucket"]:
                bucket.pop("split_from", None)
        if version < 2:
            for bucket in data["bucket"]:
                bucket.pop("formerly", None)

    problems = _problems(default_raw, older)
    assert any(
        f"declares a genre sub under schema_version {version}; write schema_version = 5" in p
        for p in problems
    ), problems


def test_a_genre_sub_on_a_bucket_that_routes_by_source_genre_is_refused(default_raw):
    def on_source(data):
        bucket = _bucket(data, "non_electronic")
        bucket["aliases"].append("Romanian Folk")
        bucket["genre_sub"] = [{"id": "folk", "display": "Folk", "sources": ["Romanian Folk"]}]

    problems = _problems(default_raw, on_source)
    assert any(
        "non_electronic: declares a genre sub and does not split by energy" in p for p in problems
    )


def test_a_genre_sub_on_a_bucket_with_one_sub_is_refused(default_raw):
    def on_single(data):
        bucket = _bucket(data, "chill_ambient")
        bucket.setdefault("aliases", []).append("Ambient Dub")
        bucket["genre_sub"] = [{"id": "dub", "display": "Dub", "sources": ["Ambient Dub"]}]

    problems = _problems(default_raw, on_single)
    assert any(
        "chill_ambient: declares a genre sub and does not split by energy" in p for p in problems
    )


@pytest.mark.parametrize(
    "shape",
    [{"id": "x", "display": "One table", "sources": ["X"]}, "a bare name", ["a bare name"]],
    ids=["one-table", "string", "list-of-strings"],
)
def test_a_genre_sub_in_the_wrong_shape_is_a_problem_and_not_a_crash(default_raw, shape):
    def mutate(data):
        _bucket(data, BUCKET)["genre_sub"] = shape

    assert any("genre_sub must be an array of tables" in p for p in _problems(default_raw, mutate))


def test_a_template_with_no_genre_sub_still_loads_at_version_4(without):
    assert without.schema_version == 4
    assert routing.genre_sub(without, BUCKET, GENRE) is None
