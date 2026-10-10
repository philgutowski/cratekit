"""The template is data, and a template that cannot be trusted is refused at load.

Two halves:

* the LOADER's validation rules, each proved to bite against a synthetic template
  built by mutating a good one, so a rule cannot pass by describing itself;
* the PARAMETERISATION claim, proved with a second taxonomy that shares nothing
  with the shipped default. That second template is the only honest way to show
  the engine reads its taxonomy rather than remembering one.

Parity against the pre-consolidation resolvers lives next door in
tests/test_routing_parity.py.
"""

from __future__ import annotations

import copy
import tomllib
from pathlib import Path

import pytest

from cratekit.core import routing
from cratekit.core.taxonomy import (
    SubPolicy,
    TaxonomyError,
    build_taxonomy,
    default_taxonomy,
    load_taxonomy,
)

HERE = Path(__file__).resolve().parent
SECOND_TEMPLATE = HERE / "taxonomies" / "second.toml"


@pytest.fixture(scope="module")
def default():
    return default_taxonomy()


@pytest.fixture(scope="module")
def default_raw() -> dict:
    """The shipped template as plain data, for mutation in the loader tests."""
    from importlib import resources

    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    return tomllib.loads(source.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def second():
    return load_taxonomy(SECOND_TEMPLATE.read_text(encoding="utf-8"))


def mutated(raw: dict, mutate) -> dict:
    data = copy.deepcopy(raw)
    mutate(data)
    return data


def problems_from(raw: dict, mutate) -> tuple[str, ...]:
    with pytest.raises(TaxonomyError) as caught:
        build_taxonomy(mutated(raw, mutate))
    return caught.value.problems


# ═══════════════════════════════════════════════════════════════════════════
# The shipped default is loadable and internally consistent
# ═══════════════════════════════════════════════════════════════════════════


def test_the_shipped_default_loads(default):
    # 2 since R-797: the shipped template declares a former place, and a
    # template has to state the version that knows one. 3 since U118, for a
    # split place, the same way. 4 since U119, for a sub class derived from a
    # playlist, the same way again.
    assert default.schema_version == 4
    assert default.buckets
    assert default.fallback.bucket in default.bucket_ids()


def test_every_bucket_declares_a_tempo_window(default):
    """A bucket with no window makes detection fall back to a generic one.

    That failure is silent and total: a window spanning a full octave folds
    nothing, so the octave-error defence the windows exist for is simply off, for
    every track, with no warning. Refusing beats defaulting.
    """
    assert default.buckets_without_bpm_prior() == ()


def test_the_tree_root_and_intake_are_declared_not_hardcoded(default):
    """R19's actual test: the two most-copied names in the old system are data.

    The tree root appeared as a literal in fifteen places and the intake folder
    in five, none of them sharing a constant.
    """
    assert default.tree.id and default.tree.display
    assert default.intake.id and default.intake.display


def test_the_reserved_and_derived_subs_carry_different_policies(default):
    """Two flags, not one 'excluded' flag, and the difference is the bug it stops."""
    policies = {entry.id: entry.policy for entry in default.sub_classes}
    assert SubPolicy.MANUAL in policies.values()
    assert SubPolicy.DERIVED in policies.values()
    derived = [entry for entry in default.sub_classes if entry.policy is SubPolicy.DERIVED]
    # TWO since U119, the vocal class and the genre Favorites, each additive and
    # each on its own signal.
    assert len(derived) == 2 and all(entry.additive for entry in derived)


# ═══════════════════════════════════════════════════════════════════════════
# Loader validation. Each rule bites.
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unsupported_schema_version_is_refused(default_raw):
    problems = problems_from(default_raw, lambda d: d.__setitem__("schema_version", 99))
    assert any("schema_version" in p for p in problems)


def test_a_display_name_used_as_an_id_is_refused(default_raw):
    """R19 in one assertion: an id is persisted, so it may never be a display name."""

    def mutate(d):
        d["bucket"][0]["id"] = d["bucket"][0]["display"]

    problems = problems_from(default_raw, mutate)
    assert any("must match" in p for p in problems)


def test_the_catalog_tree_is_declared_in_the_shipped_default(default):
    """The optional third tree, and the shipped template does declare one.

    Optional in the schema, present in the default. A user who never imports a
    catalog can delete the section; one who does gets a tree without editing
    anything, which is the point of shipping a template at all.
    """
    assert default.catalog is not None
    assert default.catalog.id and default.catalog.display


def test_a_template_declaring_no_catalog_tree_loads_clean(default_raw):
    """Absent is a complete declaration, not a deficient one.

    Every other tree in this file is mandatory, so the loader's default answer to
    a missing section is a problem. This one has to load, or a user who deletes a
    section they do not use finds their whole taxonomy refused.
    """
    data = mutated(default_raw, lambda d: d.pop("catalog"))
    assert build_taxonomy(data).catalog is None


def test_a_half_declared_catalog_tree_is_refused_as_strictly_as_a_mandatory_one(
    default_raw,
):
    """Optional to WRITE is not optional to get right.

    A section carrying one half of the pair reaches a writer as a tree named the
    empty string, or as one whose id cannot be a state key. Skipping validation
    because the section is optional is how an optional section becomes the one
    nobody checks.
    """

    def no_display(d):
        d["catalog"]["display"] = ""

    def bad_id(d):
        d["catalog"]["id"] = d["catalog"]["display"]

    def wrote_the_header_and_nothing_else(d):
        d["catalog"] = {}

    assert any("[catalog] display" in p for p in problems_from(default_raw, no_display))
    assert any("[catalog] id" in p for p in problems_from(default_raw, bad_id))
    # The empty table is the case a truthiness test gets wrong: it is falsy, so
    # "the user wrote the section header and stopped" reads as "the user wrote no
    # section" and every rule above is skipped for exactly the template most
    # likely to be half finished.
    empty = problems_from(default_raw, wrote_the_header_and_nothing_else)
    assert any("[catalog] id" in p for p in empty)
    assert any("[catalog] display" in p for p in empty)


def test_the_long_track_playlist_is_declared_in_the_shipped_default(default):
    """U88: the source system's separation of sets from tracks, as data."""
    assert default.long_tracks is not None
    assert default.long_tracks.id and default.long_tracks.display
    assert default.long_tracks.over_seconds == 1200


def test_a_template_declaring_no_long_track_playlist_loads_clean(default_raw):
    data = mutated(default_raw, lambda d: d.pop("long_tracks"))
    assert build_taxonomy(data).long_tracks is None


def test_a_long_track_playlist_with_no_bound_takes_the_source_systems(default_raw):
    data = mutated(default_raw, lambda d: d["long_tracks"].pop("over_seconds"))
    assert build_taxonomy(data).long_tracks.over_seconds == 1200


def test_a_half_declared_long_track_playlist_is_refused(default_raw):
    def no_display(d):
        d["long_tracks"]["display"] = ""

    def bad_id(d):
        d["long_tracks"]["id"] = d["long_tracks"]["display"]

    def not_a_table(d):
        d["long_tracks"] = "Sets"

    assert any("[long_tracks] display" in p for p in problems_from(default_raw, no_display))
    assert any("[long_tracks] id" in p for p in problems_from(default_raw, bad_id))
    assert any("[long_tracks] must be a table" in p for p in problems_from(default_raw, not_a_table))
    empty = problems_from(default_raw, lambda d: d.__setitem__("long_tracks", {}))
    assert any("[long_tracks] id" in p for p in empty)
    assert any("[long_tracks] display" in p for p in empty)


@pytest.mark.parametrize("bound", [True, 0, -5, "1200", 1200.5])
def test_a_long_track_bound_that_is_not_whole_positive_seconds_is_refused(default_raw, bound):
    """A boolean, zero or a negative bound would put every track in the playlist."""

    def mutate(d):
        d["long_tracks"]["over_seconds"] = bound

    assert any("[long_tracks] over_seconds" in p for p in problems_from(default_raw, mutate))


def test_a_duplicate_bucket_id_is_refused(default_raw):
    def mutate(d):
        d["bucket"][1]["id"] = d["bucket"][0]["id"]

    assert any("duplicate bucket id" in p for p in problems_from(default_raw, mutate))


def test_a_duplicate_display_name_is_refused(default_raw):
    """Two folders with one name means the XML bridge writes into whichever it
    finds first, which is not a decision anybody made."""

    def mutate(d):
        d["bucket"][1]["display"] = d["bucket"][0]["display"]

    assert any("duplicate display name" in p for p in problems_from(default_raw, mutate))


def test_a_fallback_naming_no_declared_bucket_is_refused(default_raw):
    def mutate(d):
        d["fallback"]["bucket"] = "nowhere"

    problems = problems_from(default_raw, mutate)
    assert any("routing must always land" in p for p in problems)


def test_a_template_letting_tagging_fall_back_is_refused(default_raw):
    """The blanket-genre rule, enforced at load rather than by convention.

    A guessed genre written onto a file outlives the run that guessed it, and the
    old system had to DELETE tags to undo exactly this.
    """

    def mutate(d):
        d["fallback"]["tagging_uses_fallback"] = True

    problems = problems_from(default_raw, mutate)
    assert any("allowed to decline" in p for p in problems)


def test_non_increasing_energy_bands_are_refused(default_raw):
    """Overlapping bounds put one level in two bands, and the winner is
    whichever happens to be first in the file."""

    def mutate(d):
        d["energy"]["bands"][1]["max"] = d["energy"]["bands"][0]["max"]

    assert any("does not increase" in p for p in problems_from(default_raw, mutate))


def test_bands_not_reaching_the_top_of_the_scale_are_refused(default_raw):
    def mutate(d):
        d["energy"]["bands"][-1]["max"] = 8

    problems = problems_from(default_raw, mutate)
    assert any("scale_max" in p for p in problems)


def test_rating_cuts_are_not_required_to_align_with_band_cuts(default):
    """The decoupling is deliberate and must stay expressible.

    Energy is decile-calibrated, so an even five-way star spread and a three-way
    tree split are both right. A loader that forced them to agree would re-rate a
    whole library the first time either moved.
    """
    band_cuts = {band.max for band in default.energy.bands}
    rating_cuts = {cut.max for cut in default.energy.rating_cuts}
    assert band_cuts != rating_cuts


def test_a_band_display_override_naming_an_undeclared_band_is_refused(default_raw):
    def mutate(d):
        for bucket in d["bucket"]:
            if "band_display" in bucket.get("energy", {}):
                bucket["energy"]["band_display"]["nosuchband"] = "Whatever"
                return
        raise AssertionError("the default no longer overrides any band label")

    problems = problems_from(default_raw, mutate)
    assert any("not a declared band" in p for p in problems)


def test_a_source_routed_sub_pointing_outside_its_bucket_is_refused(default_raw):
    def mutate(d):
        for bucket in d["bucket"]:
            if "sub_by_source" in bucket:
                bucket["sub_by_source"]["default"] = "not_a_sub"
                return
        raise AssertionError("the default no longer routes any bucket by source genre")

    problems = problems_from(default_raw, mutate)
    assert any("not a declared sub" in p for p in problems)


def test_one_source_string_routing_two_ways_is_refused(default_raw):
    def mutate(d):
        d["bucket"][1]["aliases"] = list(d["bucket"][1]["aliases"]) + [
            d["bucket"][0]["aliases"][0]
        ]

    problems = problems_from(default_raw, mutate)
    assert any("cannot route two ways" in p for p in problems)


def test_a_fuzzy_rule_naming_no_declared_bucket_is_refused(default_raw):
    def mutate(d):
        d["fuzzy"][0]["bucket"] = "nowhere"

    assert any("is not declared" in p for p in problems_from(default_raw, mutate))


def test_an_uppercase_keyword_is_refused(default_raw):
    """It could never match, and a rule that can never fire reads as one that does."""

    def mutate(d):
        d["fuzzy"][0]["keyword"] = d["fuzzy"][0]["keyword"].upper()

    assert any("can never match" in p for p in problems_from(default_raw, mutate))


def test_a_suggest_rule_that_both_answers_and_declines_is_refused(default_raw):
    def mutate(d):
        rule = next(r for r in d["suggest"] if "bucket" in r)
        rule["decline"] = "ask"

    problems = problems_from(default_raw, mutate)
    assert any("exactly one of bucket, tag, decline" in p for p in problems)


def test_a_tree_depth_other_than_three_is_refused_by_name(default_raw):
    """KTD14: the XML bridge's indentation encodes exactly three levels.

    Refusing by name beats emitting bytes rekordbox reads as a different tree.
    """

    def mutate(d):
        d["tree"]["depth"] = 4

    problems = problems_from(default_raw, mutate)
    assert any("KTD14" in p for p in problems)


def test_a_bad_tempo_window_is_refused(default_raw):
    def mutate(d):
        d["bucket"][0]["bpm"] = {"start": 100, "floor": 120, "ceil": 140}

    problems = problems_from(default_raw, mutate)
    assert any("floor < start < ceil" in p for p in problems)


def test_every_problem_is_reported_not_just_the_first(default_raw):
    """A friend fixing one error per run is a friend who stops after three."""

    def mutate(d):
        d["bucket"][0]["id"] = "Not An Id"
        d["fallback"]["bucket"] = "nowhere"
        d["fuzzy"][0]["bucket"] = "also_nowhere"

    assert len(problems_from(default_raw, mutate)) >= 3


def test_invalid_toml_is_refused_as_a_template_problem():
    with pytest.raises(TaxonomyError) as caught:
        load_taxonomy("this is not = = toml")
    assert "not valid TOML" in caught.value.problems[0]


# ═══════════════════════════════════════════════════════════════════════════
# Parameterisation: a second taxonomy, sharing nothing
# ═══════════════════════════════════════════════════════════════════════════


def test_the_second_template_shares_no_name_with_the_default(default, second):
    """If this ever fails, the second template stopped being a real second one."""
    assert not {b.display for b in default.buckets} & {b.display for b in second.buckets}
    assert not {b.id for b in default.buckets} & {b.id for b in second.buckets}
    assert not (
        {band.display for band in default.energy.bands}
        & {band.display for band in second.energy.bands}
    )
    assert len(default.energy.bands) != len(second.energy.bands)
    assert default.tree.display != second.tree.display


def test_a_custom_taxonomy_routes_with_no_code_change(second):
    """The whole parameterisation claim, in one assertion per tier."""
    assert routing.resolve_bucket(second, "Banger").bucket_id == "floor_filler"
    assert routing.resolve_bucket(second, "Slow Burn").bucket_id == "slow_burn"
    assert routing.resolve_bucket(second, "a proper banger").bucket_id == "floor_filler"
    assert routing.resolve_bucket(second, "no idea").bucket_id == "unfiled"


def test_a_custom_taxonomy_uses_its_own_band_count(second):
    """Four bands, four different cuts, and none of the default's names."""
    seen = {
        level: routing.energy_sub(second, "floor_filler", level).display
        for level in range(1, 11)
    }
    assert seen[1] == "Warm Up"
    assert seen[3] == "Groove"
    assert seen[6] == "Peak"
    assert seen[9] == "Afters"


def test_a_custom_taxonomy_applies_its_own_band_label_override(second):
    """Same cuts, different labels, and only the overridden ones move."""
    assert routing.energy_sub(second, "slow_burn", 1).display == "Barely Moving"
    assert routing.energy_sub(second, "slow_burn", 4).display == "Groove"
    assert routing.energy_sub(second, "slow_burn", 10).display == "Last Call"


def test_a_custom_taxonomy_honours_a_bucket_with_no_energy_split(second):
    for level in (None, 1, 5, 10):
        assert routing.energy_sub(second, "spoken", level).display == "Spoken Word"
    assert routing.no_energy_sub(second, "spoken") is None
    assert routing.rates(second, "spoken") is False


def test_a_custom_taxonomy_honours_a_bucket_routing_by_source(second):
    assert routing.energy_sub(second, "field_recordings", 5, source_genre="Wildlife").id == "birds"
    assert routing.energy_sub(second, "field_recordings", None, source_genre="Weather").id == "water"
    # Unmapped falls to the DECLARED default rather than to whichever sub is first.
    assert routing.energy_sub(second, "field_recordings", 5, source_genre="Ghosts").id == "engines"


def test_a_custom_taxonomy_uses_its_own_rating_curve(second):
    assert routing.energy_rating(second, 3) == 51
    assert routing.energy_rating(second, 6) == 153
    assert routing.energy_rating(second, 10) == 255
    assert routing.energy_rating(second, None) is None


def test_a_custom_taxonomy_uses_its_own_tempo_windows(second):
    prior = routing.bpm_prior(second, "Banger")
    assert (prior.start, prior.floor, prior.ceil) == (128, 120, 140)


def test_a_custom_taxonomy_uses_its_own_decline_vocabulary(second):
    assert routing.suggest_tag(second, "Misc").declined
    assert routing.suggest_tag(second, "").decline is routing.Decline.NOT_FOUND
    assert routing.suggest_tag(second, "Banger").tag == "Floor Filler"


def test_a_custom_taxonomy_splits_on_tempo_where_it_declares_one(second):
    assert routing.suggest_tag(second, "slow one", bpm=80.0).bucket_id == "spoken"
    assert routing.suggest_tag(second, "slow one", bpm=110.0).bucket_id == "slow_burn"
    unknown = routing.suggest_tag(second, "slow one")
    assert unknown.bucket_id == "slow_burn" and unknown.needs_review is True


def test_a_buckets_own_display_name_is_never_reported_off_taxonomy(default, second):
    """R-650. The library's own folder names are not a gap in the library.

    ``suggest_tag`` has NO tier that recognises a display name, deliberately:
    recognising one is routing's job, and tagging must not invent a bucket. So a
    catalogue answering with a bucket's own name, which happens constantly
    because this tagger writes bucket names back onto files, reaches the last
    tier and passes through as itself. The TAG is right, routing places it by
    its own second tier, and reporting it would put the person's own template in
    front of them as something to go and fix.

    BOTH TEMPLATES, because the shipped one has two such buckets and the second
    has three, measured 2026-09-21. A template whose every bucket display also
    has an alias would make this vacuous, which is what the second loop rules
    out.
    """
    for declared in (default, second):
        displays = [bucket.display for bucket in declared.buckets]
        assert displays
        assert [d for d in displays if routing.suggest_tag(declared, d).off_taxonomy] == []

    # NOT VACUOUS, which is the half a passing assertion above cannot show. Each
    # of these is claimed by no alias and comes back out of the resolver as
    # itself with no bucket, which is the last tier's own shape.
    for declared, display in ((default, "NonElectronic"), (second, "Floor Filler")):
        assert declared.bucket_for_display(display) is not None
        assert declared.tagging_alias(display.lower()) is None
        answer = routing.suggest_tag(declared, display)
        assert (answer.tag, answer.bucket_id, answer.declined) == (display, None, False)


def test_a_sub_display_and_a_changed_case_are_both_reported(default, second):
    """The two ways a declared-looking word still does not land where it says.

    The suppression above is the ROUTING tier, not the vocabulary, and this is
    the measurement that decided it. A sub's display is a word the template
    declares and ``resolve_bucket`` does not recognise, so the file wears it and
    lands in the fallback. A bucket display in another case is the same story,
    and it is not hypothetical: the Bandcamp picker only ever selects a tag
    equal to its own lowercase, so that is the case this product produces.

    Both are exactly the cost R-650 names, so both are reported rather than
    suppressed for looking familiar.
    """
    for display in ("Birds", "Water", "Engines"):
        assert routing.suggest_tag(second, display).off_taxonomy is True
        assert routing.resolve_bucket(second, display).bucket_id == second.fallback.bucket

    lowered = "nonelectronic"
    assert default.bucket_for_display("NonElectronic") is not None
    assert routing.suggest_tag(default, lowered).off_taxonomy is True
    assert routing.resolve_bucket(default, lowered).bucket_id == default.fallback.bucket


def test_an_off_taxonomy_word_can_still_route_to_a_real_bucket(default):
    """The flag is about the WORD, and reading it as a place is wrong both ways.

    ``suggest_tag``'s last tier and ``resolve_bucket``'s keyword tier read two
    different rule lists, so a string nothing tags can still be routed by a
    fuzzy rule. Driven 2026-09-21 on two ordinary Beatport genre strings. This
    is why the sweep's warning says what was written and not where it went.
    """
    for value in ("Psy-Trance", "Hardcore / Hard Techno"):
        assert routing.suggest_tag(default, value).off_taxonomy is True
        landing = routing.resolve_bucket(default, value)
        assert landing.bucket_id != default.fallback.bucket, value
        assert landing.match is routing.Match.FUZZY


def test_two_taxonomies_coexist_in_one_process(default, second):
    """The reason nothing here reads configuration (seam decision S3).

    A resolver that reached for global config could not be asked this question at
    all, and the question is the unit's verification.
    """
    assert routing.resolve_bucket(default, "Banger").bucket_id == default.fallback.bucket
    assert routing.resolve_bucket(second, "Banger").bucket_id == "floor_filler"


def test_a_template_with_no_energy_dimension_routes_and_does_not_error():
    """R19's least glamorous requirement: a taxonomy may simply not use energy.

    The engine must place the track in its bucket and report that there is no sub
    below it, rather than raising or inventing one.
    """
    template = """
schema_version = 1
[tree]
id = "flat"
display = "FLAT"
depth = 3
[intake]
id = "new"
display = "NEW"
[fallback]
bucket = "everything"
[energy]
enabled = false
[[bucket]]
id = "everything"
display = "Everything"
"""
    taxonomy = load_taxonomy(template)
    resolution = routing.resolve_bucket(taxonomy, "whatever this is")
    assert resolution.bucket_id == "everything"
    assert routing.energy_sub(taxonomy, "everything", 7) is None
    assert routing.energy_sub(taxonomy, "everything", None) is None
    assert routing.energy_rating(taxonomy, 7) is None


# ═══════════════════════════════════════════════════════════════════════════
# R19: a rename must not orphan state
# ═══════════════════════════════════════════════════════════════════════════


def test_renaming_a_display_name_preserves_state_keyed_to_its_identifier(default_raw):
    """The entire reason ids exist, asserted end to end.

    In the old system a folder name was simultaneously code, config, a state key,
    XML bytes, and a folder in the user's rekordbox. Renaming it orphaned every
    record keyed on the old name, silently, because nothing connected them.
    """
    before = build_taxonomy(default_raw)
    target = before.buckets[0]

    # State written under the OLD taxonomy, keyed on the identifier.
    state = {bucket.id: {"swept": index} for index, bucket in enumerate(before.buckets)}

    after = build_taxonomy(
        mutated(default_raw, lambda d: d["bucket"][0].__setitem__("display", "Renamed By Hand"))
    )
    renamed = after.bucket(target.id)

    assert renamed.display == "Renamed By Hand"
    assert renamed.display != target.display
    assert renamed.id == target.id
    assert state[renamed.id] == {"swept": 0}
    # And routing follows the new name, because the passthrough tier reads the
    # display off the declaration rather than off a hardcoded list.
    assert routing.resolve_bucket(after, "Renamed By Hand").bucket_id == target.id


def test_a_renamed_bucket_keeps_its_aliases_and_its_tempo_window(default_raw):
    """A rename is cosmetic. Anything it changes besides the name is a bug."""
    before = build_taxonomy(default_raw)
    after = build_taxonomy(
        mutated(default_raw, lambda d: d["bucket"][0].__setitem__("display", "Renamed By Hand"))
    )
    original, renamed = before.buckets[0], after.buckets[0]
    assert renamed.aliases == original.aliases
    assert renamed.bpm == original.bpm
    assert renamed.family == original.family


# ═══════════════════════════════════════════════════════════════════════════
# A former place (R-797): the loader refuses one that is still a place
# ═══════════════════════════════════════════════════════════════════════════


def _promoted(data: dict) -> dict:
    """The bucket of the shipped template that declares a former place."""
    return next(bucket for bucket in data["bucket"] if bucket.get("formerly"))


def _holder(data: dict) -> dict:
    """The bucket whose folder holds that former place."""
    former = _promoted(data)["formerly"][0]
    return next(bucket for bucket in data["bucket"] if bucket["id"] == former["bucket"])


def test_the_shipped_template_declares_two_former_places_and_they_load(default, default_raw):
    """R&B's since R-797 and Hip-Hop's since U118, each read as written."""
    declared = [
        (bucket.id, place) for bucket in default.buckets for place in bucket.formerly
    ]
    raw = [
        (bucket["id"], row) for bucket in default_raw["bucket"] for row in bucket.get("formerly", [])
    ]
    assert len(declared) == len(raw) == 2
    for (bucket_id, former), (raw_id, row) in zip(declared, raw):
        assert (bucket_id, former.id, former.bucket, former.sub, former.display) == (
            raw_id, row["id"], row["bucket"], row["sub"], row["display"]
        )


def test_a_former_place_in_a_bucket_nobody_declares_is_refused(default_raw):
    def mutate(data):
        _promoted(data)["formerly"][0]["bucket"] = "no_such_bucket"

    assert any("is not declared" in p for p in problems_from(default_raw, mutate))


def test_a_former_place_naming_a_sub_its_bucket_still_declares_is_refused(default_raw):
    """The guard that stops a mistyped line planning removals from a live sub."""

    def mutate(data):
        live = _holder(data)["sub"][0]
        _promoted(data)["formerly"][0]["sub"] = live["id"]

    assert any("still declares the sub" in p for p in problems_from(default_raw, mutate))


def test_a_former_place_carrying_the_name_of_a_live_sub_is_refused(default_raw):
    def mutate(data):
        live = _holder(data)["sub"][0]
        _promoted(data)["formerly"][0]["display"] = live["display"]

    assert any("still holds a sub named" in p for p in problems_from(default_raw, mutate))


def test_a_former_place_named_for_a_band_of_an_energy_bucket_is_refused(default_raw):
    """A band is a live place of a bucket that splits by energy, under the
    bucket's own label for it."""

    def mutate(data):
        holder = next(
            bucket
            for bucket in data["bucket"]
            if (bucket.get("energy") or {}).get("band_display")
        )
        former = _promoted(data)["formerly"][0]
        former["bucket"] = holder["id"]
        former["display"] = next(iter(holder["energy"]["band_display"].values()))

    assert any("still holds a sub named" in p for p in problems_from(default_raw, mutate))


def test_a_band_name_is_no_live_place_in_a_bucket_that_does_not_split_by_energy(default_raw):
    """The other side of the rule above: the check asks what THAT bucket holds."""

    def mutate(data):
        former = _promoted(data)["formerly"][0]
        former["display"] = data["energy"]["bands"][0]["display"]
        # The split place naming it carries the name it is given (U118).
        for row in _splitter(data)["split_from"]:
            if row["sub"] == former["id"]:
                row["display"] = former["display"]

    assert build_taxonomy(mutated(default_raw, mutate)).buckets


def test_a_former_place_named_for_a_sub_class_is_refused(default_raw):
    def mutate(data):
        _promoted(data)["formerly"][0]["display"] = data["sub_class"][0]["display"]

    assert any("still holds a sub named" in p for p in problems_from(default_raw, mutate))


def test_a_former_place_whose_own_id_is_a_band_is_refused(default_raw):
    def mutate(data):
        _promoted(data)["formerly"][0]["id"] = data["energy"]["bands"][0]["id"]

    assert any("already a sub of this bucket" in p for p in problems_from(default_raw, mutate))


def test_a_former_place_declared_twice_in_one_bucket_is_refused(default_raw):
    def mutate(data):
        promoted = _promoted(data)
        promoted["formerly"].append(dict(promoted["formerly"][0]))

    found = problems_from(default_raw, mutate)
    assert any("duplicate former place id" in p for p in found)
    assert any("already the former place of" in p for p in found)


def _another_bucket(data: dict) -> dict:
    return next(
        bucket
        for bucket in data["bucket"]
        if not bucket.get("formerly") and bucket["id"] != _holder(data)["id"]
    )


def test_one_playlist_cannot_be_the_former_place_of_two_buckets(default_raw):
    def mutate(data):
        _another_bucket(data)["formerly"] = [
            dict(_promoted(data)["formerly"][0], id="another_id")
        ]

    found = problems_from(default_raw, mutate)
    assert any("already the former place of" in p for p in found)
    assert not any("duplicate former place id" in p for p in found)


def test_two_buckets_cannot_declare_one_former_place_id(default_raw):
    """Both compete in the folder that holds them, under their identifiers."""

    def mutate(data):
        first = _promoted(data)["formerly"][0]
        _another_bucket(data)["formerly"] = [
            dict(first, sub="another_sub", display="Another playlist")
        ]

    found = problems_from(default_raw, mutate)
    assert any("duplicate former place id" in p for p in found)
    assert not any("already the former place of" in p for p in found)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("id", "Not An Id", "must match"),
        ("sub", "", "must match"),
        ("display", "", "display must be a non-empty string"),
    ],
)
def test_a_former_place_short_of_a_field_is_refused(default_raw, field, value, message):
    def mutate(data):
        _promoted(data)["formerly"][0][field] = value

    assert any("formerly" in p and message in p for p in problems_from(default_raw, mutate))


def test_a_template_with_no_former_place_loads_as_it_always_did(default_raw):
    def mutate(data):
        formerly = {row["id"] for bucket in data["bucket"] for row in bucket.get("formerly", [])}
        for bucket in data["bucket"]:
            bucket.pop("formerly", None)
        # A split place naming a former place goes with it (U118).
        splitter = _splitter(data)
        splitter["split_from"] = [
            row for row in splitter["split_from"] if row["sub"] not in formerly
        ]

    loaded = build_taxonomy(mutated(default_raw, mutate))
    assert all(bucket.formerly == () for bucket in loaded.buckets)


def test_a_former_place_under_schema_version_1_is_refused(default_raw):
    """An older build reads version 1, ignores the declaration, and files a
    track into its new place while it sits in the old one. Version 2 is what
    such a build refuses by name, so the declaration has to state it."""

    def mutate(data):
        data["schema_version"] = 1

    assert any(
        "declares a former place under schema_version 1" in p
        for p in problems_from(default_raw, mutate)
    )


def test_a_version_1_template_with_no_former_place_still_loads(default_raw, second):
    def mutate(data):
        data["schema_version"] = 1
        for bucket in data["bucket"]:
            bucket.pop("formerly", None)
            bucket.pop("split_from", None)
        data["sub_class"] = [c for c in data["sub_class"] if c.get("signal") != "playlist"]

    assert build_taxonomy(mutated(default_raw, mutate)).schema_version == 1
    assert second.schema_version == 1


@pytest.mark.parametrize(
    "shape",
    [
        {"id": "x", "bucket": "y", "sub": "z", "display": "One table, single brackets"},
        ["a bare name"],
        "a bare name",
    ],
    ids=["one-table", "list-of-strings", "string"],
)
def test_a_former_place_in_the_wrong_shape_is_a_problem_and_not_a_crash(default_raw, shape):
    """A person edits a library's copy by hand, and one pair of brackets is
    valid TOML. It raised an attribute error out of the loader, which every
    verb reported as a defect in this product."""

    def mutate(data):
        _promoted(data)["formerly"] = shape

    assert any(
        "formerly must be an array of tables" in p for p in problems_from(default_raw, mutate)
    )


def test_a_former_place_whose_id_is_a_sub_of_the_bucket_that_holds_it_is_refused(default_raw):
    """It competes in that bucket too, so the identifier has to be free there."""

    def mutate(data):
        _promoted(data)["formerly"][0]["id"] = _holder(data)["sub"][0]["id"]

    assert any("where a former place competes as well" in p for p in problems_from(default_raw, mutate))


# ═══════════════════════════════════════════════════════════════════════════
# A split place (U118): the loader refuses one that is not a live band
# ═══════════════════════════════════════════════════════════════════════════


def _splitter(data: dict) -> dict:
    """The bucket of the shipped template that declares split places."""
    return next(bucket for bucket in data["bucket"] if bucket.get("split_from"))


def _split_holder(data: dict) -> dict:
    """The bucket whose bands those split places are."""
    place = _splitter(data)["split_from"][0]
    return next(bucket for bucket in data["bucket"] if bucket["id"] == place["bucket"])


def test_the_shipped_template_splits_one_bucket_out_of_every_place_of_another(default, default_raw):
    """Soul out of R&B: every band, the no reading sub and R&B's own former
    place, each read as written."""
    (splitter,) = [bucket for bucket in default.buckets if bucket.split_from]
    holder = default.bucket(splitter.split_from[0].bucket)
    raw = _splitter(default_raw)["split_from"]
    assert [(p.id, p.bucket, p.sub, p.display) for p in splitter.split_from] == [
        (row["id"], row["bucket"], row["sub"], row["display"]) for row in raw
    ]
    assert {place.bucket for place in splitter.split_from} == {holder.id}
    assert {place.sub for place in splitter.split_from} == {
        *(band.id for band in default.energy.bands),
        default.energy.no_energy_sub.id,
        *(former.id for former in holder.formerly),
    }


def test_a_split_place_naming_a_band_the_holder_does_not_file_into_is_refused(default_raw):
    """The guard that stops a former place being written as a split place."""

    def mutate(data):
        _splitter(data)["split_from"][0]["sub"] = "no_such_band"

    assert any("is not a band" in p for p in problems_from(default_raw, mutate))


def test_a_split_place_out_of_a_bucket_with_no_bands_is_refused(default_raw):
    def mutate(data):
        holder = next(bucket for bucket in data["bucket"] if bucket.get("sub_by_source"))
        _splitter(data)["split_from"][0]["bucket"] = holder["id"]

    assert any("is not a band" in p for p in problems_from(default_raw, mutate))


def test_a_split_place_under_another_name_than_the_holders_is_refused(default_raw):
    def mutate(data):
        _splitter(data)["split_from"][0]["display"] = "Renamed by hand"

    assert any("the name" in p and "gives" in p for p in problems_from(default_raw, mutate))


def test_a_split_place_of_a_band_under_its_own_label_is_checked_against_that_label(default_raw):
    """A holder that labels its bands differently is asked for its label."""

    def mutate(data):
        holder = next(
            bucket for bucket in data["bucket"] if (bucket.get("energy") or {}).get("band_display")
        )
        band, label = next(iter(holder["energy"]["band_display"].items()))
        bands = {row["id"] for row in data["energy"]["bands"]} | {"unsorted"}
        splitter = _splitter(data)
        splitter["split_from"] = [row for row in splitter["split_from"] if row["sub"] in bands]
        place = splitter["split_from"][0]
        place.update(bucket=holder["id"], sub=band, display=label)
        for other in splitter["split_from"][1:]:
            other["bucket"] = holder["id"]
            other["display"] = holder["energy"]["band_display"].get(other["sub"], other["display"])

    assert build_taxonomy(mutated(default_raw, mutate)).buckets

    def plain_name(data):
        mutate(data)
        place = _splitter(data)["split_from"][0]
        place["display"] = next(
            band["display"] for band in data["energy"]["bands"] if band["id"] == place["sub"]
        )

    assert any("gives" in p for p in problems_from(default_raw, plain_name))


def test_a_split_place_out_of_itself_or_a_bucket_nobody_declares_is_refused(default_raw):
    for name in ("no_such_bucket", None):

        def mutate(data, name=name):
            _splitter(data)["split_from"][0]["bucket"] = name or _splitter(data)["id"]

        assert any("not another declared bucket" in p for p in problems_from(default_raw, mutate))


def test_one_band_split_out_by_two_buckets_is_refused(default_raw):
    def mutate(data):
        other = next(
            bucket
            for bucket in data["bucket"]
            if bucket["id"] not in (_splitter(data)["id"], _split_holder(data)["id"])
            and not bucket.get("sub_by_source")
            and (bucket.get("energy") or {}).get("enabled", True)
        )
        other["split_from"] = [dict(_splitter(data)["split_from"][0], id="another_id")]

    assert any("already split out by" in p for p in problems_from(default_raw, mutate))


def test_a_split_place_id_shared_with_a_former_place_is_refused(default_raw):
    def mutate(data):
        _splitter(data)["split_from"][0]["id"] = _promoted(data)["formerly"][0]["id"]

    assert any("already a former or split place" in p for p in problems_from(default_raw, mutate))


def test_a_split_place_of_the_holders_former_place_under_another_name_is_refused(default_raw):
    def mutate(data):
        former = next(row for row in _splitter(data)["split_from"] if row["sub"] not in (
            {band["id"] for band in data["energy"]["bands"]} | {"unsorted"}
        ))
        former["display"] = "Renamed by hand"

    assert any("gives" in p for p in problems_from(default_raw, mutate))


def test_a_split_place_of_another_buckets_former_place_is_refused(default_raw):
    """Only the holder's own former place, which is a place the holder competes on."""

    def mutate(data):
        hip_hop = next(b for b in data["bucket"] if b["id"] == "hip_hop")
        _splitter(data)["split_from"][0].update(
            sub=hip_hop["formerly"][0]["id"], display=hip_hop["formerly"][0]["display"]
        )

    assert any("is not a band or a former place" in p for p in problems_from(default_raw, mutate))


def test_a_split_place_whose_id_is_a_band_is_refused(default_raw):
    def mutate(data):
        _splitter(data)["split_from"][0]["id"] = data["energy"]["bands"][0]["id"]

    assert any("already a sub of this bucket" in p for p in problems_from(default_raw, mutate))


def test_a_bucket_that_does_not_split_by_energy_cannot_declare_a_split_place(default_raw):
    def mutate(data):
        _splitter(data)["energy"] = {"enabled": False}
        _splitter(data)["single_sub"] = {"id": "everything", "display": "Everything"}

    assert any("does not split by energy" in p for p in problems_from(default_raw, mutate))


@pytest.mark.parametrize("version", [1, 2])
def test_a_split_place_under_an_older_schema_version_is_refused(default_raw, version):
    """A build that reads version 2 ignores the key and files every track of
    the split genre into its new folder while it sits in the old band."""

    def mutate(data):
        data["schema_version"] = version

    assert any(
        f"declares a split place under schema_version {version}" in p
        for p in problems_from(default_raw, mutate)
    )


def test_a_version_2_template_with_no_split_place_still_loads(default_raw):
    def mutate(data):
        data["schema_version"] = 2
        del _splitter(data)["split_from"]
        data["sub_class"] = [c for c in data["sub_class"] if c.get("signal") != "playlist"]

    assert build_taxonomy(mutated(default_raw, mutate)).schema_version == 2


@pytest.mark.parametrize(
    "shape",
    [{"id": "x", "bucket": "y", "sub": "z", "display": "One table"}, "a bare name"],
    ids=["one-table", "string"],
)
def test_a_split_place_in_the_wrong_shape_is_a_problem_and_not_a_crash(default_raw, shape):
    def mutate(data):
        _splitter(data)["split_from"] = shape

    assert any(
        "split_from must be an array of tables" in p for p in problems_from(default_raw, mutate)
    )


def test_a_tagging_only_word_wins_over_another_buckets_routing_alias(default):
    """"Trap / Wave" routes to one bucket and tags as Hip-Hop, as it did while
    Hip-Hop was a sub. A tagging-only word is the more specific statement."""
    routed = default.routing_alias("Trap / Wave")
    tagged = default.tagging_alias("trap / wave")
    assert routed is not None and tagged is not None
    assert tagged == (next(b.id for b in default.buckets if b.display == "Hip-Hop"), None)
    assert routed != tagged[0]


def test_two_buckets_listing_one_tagging_only_word_is_refused(default_raw):
    def mutate(data):
        first = _splitter(data)
        other = next(bucket for bucket in data["bucket"] if bucket.get("tag_aliases") and bucket is not first)
        first.setdefault("tag_aliases", []).append(other["tag_aliases"][0])

    assert any("is claimed by both" in p for p in problems_from(default_raw, mutate))


# ---------------------------------------------------------------------------
# U121: the INSPIRATION folder, an optional root node like the catalog tree
# ---------------------------------------------------------------------------


def test_the_inspiration_folder_is_declared_in_the_shipped_default(default):
    """U121: the folder a set's permanent playlist is kept in, as data. A
    library whose author keeps no such playlists can delete the section; one
    who does gets the folder the source system already used."""
    assert default.inspiration is not None
    assert default.inspiration.id == "inspiration"
    assert default.inspiration.display == "INSPIRATION"


def test_a_template_declaring_no_inspiration_folder_loads_clean(default_raw):
    data = mutated(default_raw, lambda d: d.pop("inspiration"))
    assert build_taxonomy(data).inspiration is None


def test_a_half_declared_inspiration_folder_is_refused_as_strictly_as_a_mandatory_one(
    default_raw,
):
    def no_display(d):
        d["inspiration"]["display"] = ""

    def bad_id(d):
        d["inspiration"]["id"] = d["inspiration"]["display"]

    def empty(d):
        d["inspiration"] = {}

    def not_a_table(d):
        d["inspiration"] = "INSPIRATION"

    assert any("[inspiration] display" in p for p in problems_from(default_raw, no_display))
    assert any("[inspiration] id" in p for p in problems_from(default_raw, bad_id))
    emptied = problems_from(default_raw, empty)
    assert any("[inspiration] id" in p for p in emptied)
    assert any("[inspiration] display" in p for p in emptied)
    assert any("[inspiration] must be a table" in p for p in problems_from(default_raw, not_a_table))
# U119: a sub class derived from a playlist, beside the vocal one
# ---------------------------------------------------------------------------


def test_the_shipped_default_declares_the_genre_favorites_as_a_playlist_signal(default):
    """U119: one Favorites playlist in every genre folder, mirroring All Favorites."""
    favorites = default.sub_class("favorites")
    assert favorites.policy is SubPolicy.DERIVED and favorites.additive is True
    assert favorites.present_in == "all_buckets"
    assert favorites.signal == "playlist"
    assert favorites.signal_playlist == "All Favorites"
    assert default.schema_version == 4
    vox = default.sub_class("with_vox")
    assert vox.signal == "vox" and vox.signal_playlist == ""


def test_two_additive_classes_load_when_their_signals_differ(default):
    additive = [entry for entry in default.sub_classes if entry.additive]
    assert sorted(entry.signal for entry in additive) == ["playlist", "vox"]


def test_two_additive_classes_on_one_signal_are_refused(default_raw):
    def second_vocal(d):
        d["sub_class"].append(
            {"id": "second_vox", "display": "Second", "policy": "derived", "additive": True}
        )

    problems = problems_from(default_raw, second_vocal)
    assert any("'vox' signal" in p and "only one is supported per signal" in p for p in problems)


def test_a_playlist_signal_names_its_playlist_and_is_derived_and_additive(default_raw):
    def no_playlist(d):
        d["sub_class"][2]["signal_playlist"] = ""

    def manual(d):
        d["sub_class"][2]["policy"] = "manual"
        d["sub_class"][2]["additive"] = False

    assert any("signal_playlist" in p for p in problems_from(default_raw, no_playlist))
    assert any("derived and additive" in p for p in problems_from(default_raw, manual))


def test_a_playlist_name_on_a_vocal_class_and_an_unknown_signal_are_refused(default_raw):
    def misplaced(d):
        d["sub_class"][1]["signal_playlist"] = "All Favorites"

    def unknown(d):
        d["sub_class"][2]["signal"] = "colour"

    assert any("only meaningful for a playlist signal" in p for p in problems_from(default_raw, misplaced))
    assert any("signal 'colour'" in p for p in problems_from(default_raw, unknown))


def test_a_playlist_signal_under_schema_version_three_is_refused_by_name(default_raw):
    def older(d):
        d["schema_version"] = 3

    problems = problems_from(default_raw, older)
    assert any("schema_version = 4" in p for p in problems)


def test_a_template_without_the_favorites_class_loads_clean(default_raw):
    data = mutated(default_raw, lambda d: d["sub_class"].pop(2))
    built = build_taxonomy(data)
    assert [entry.id for entry in built.sub_classes if entry.additive] == ["with_vox"]
