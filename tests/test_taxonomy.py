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
    assert default.schema_version == 1
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
    assert len(derived) == 1 and derived[0].additive is True


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
