"""Parity: the declared taxonomy answers exactly as the eight resolvers it replaced.

The population is the library's own genre values plus the sweeps' source
strings, not the old tables' keys: every key hits the exact tier, while drift
lives in the keyword and fallback tiers that fire only on strings no table holds.
The reference is tests/legacy_taxonomy.py, the original code frozen. Every
deliberate difference has its own test; populations are split at collection
time, so each excluded case is owned by a named test rather than skipped.
"""

from __future__ import annotations

import inspect

import pytest

from cratekit.core import routing
from cratekit.core.taxonomy import default_taxonomy
from tests import legacy_taxonomy as legacy

TAXONOMY = default_taxonomy()
DISPLAY = {bucket.id: bucket.display for bucket in TAXONOMY.buckets}

# The live library's values, the sweeps' values, and both old tables' keys.
POPULATION = sorted(set(legacy.CORPUS) | set(legacy.GENRE_MAP) | set(legacy.GENRE_NORMALIZE))

# The strings the template declares an outright refusal for (own test).
REFUSED = {
    needle.lower()
    for rule in TAXONOMY.suggest
    if rule.equals and rule.decline
    for needle in rule.equals
}

# The strings the template declares an alias for; the sweep never had one (own test).
ALIASED = {v for v in POPULATION if TAXONOMY.tagging_alias(v.lower().strip()) is not None}

SWEEP_PARITY_POPULATION = [
    v for v in POPULATION if v.lower().strip() not in REFUSED and v not in ALIASED
]

# The buckets the old code never had (R-797, U118, U133): R&B, Soul, Hip-Hop
# and Jazz moved out of the playlists the old code filed them in. Every set is
# derived, and its own test holds it equal to what the old code filed there.
PROMOTED_BUCKETS = tuple(
    bucket for bucket in TAXONOMY.buckets if bucket.formerly or bucket.split_from
)


def _old_playlist(bucket):
    """The place the old code filed a promoted bucket's words: its own, or its holder's."""
    if bucket.formerly:
        return bucket.formerly[0]
    (holder,) = {place.bucket for place in bucket.split_from}
    return TAXONOMY.bucket(holder).formerly[0]


OLD_PLAYLIST = {bucket.id: _old_playlist(bucket) for bucket in PROMOTED_BUCKETS}
_IN_PROMOTED = {
    v: resolution
    for v in POPULATION
    if (resolution := routing.resolve_bucket(TAXONOMY, v)).bucket_id in OLD_PLAYLIST
}
PROMOTED = {v for v, r in _IN_PROMOTED.items() if r.match is not routing.Match.FUZZY}
#: The keyword rules moved with a promoted bucket: only Jazz's (U133; R-804, R-941).
KEYWORDS_MOVED = {"jazz"}
#: The words such a rule sends to a promoted bucket.
MOVED_BY_KEYWORD = {v for v, r in _IN_PROMOTED.items() if r.match is routing.Match.FUZZY}
#: The one word in a promoted bucket the old code filed elsewhere (U118).
NAMED_BY_THE_AUTHOR = {"Hip-hop & Rap"}
#: The old tagger's answers naming the old "Soul / R&B" playlist, now R&B's or Soul's.
RETAGGED = {
    k
    for k in legacy.GENRE_NORMALIZE
    if any(
        legacy.normalize_genre(k) == place.display != TAXONOMY.bucket(bucket_id).display
        for bucket_id, place in OLD_PLAYLIST.items()
    )
}
#: The first of them, as R-797 declared it.
PROMOTED_BUCKET = next(bucket for bucket in TAXONOMY.buckets if bucket.formerly)
(FORMER_PLACE,) = PROMOTED_BUCKET.formerly

ROUTING_PARITY_POPULATION = [
    v for v in POPULATION if v not in PROMOTED and v not in MOVED_BY_KEYWORD
]
TAGGER_PARITY_POPULATION = [
    k
    for k in sorted(legacy.GENRE_NORMALIZE)
    if k.lower().strip() not in REFUSED and k not in RETAGGED
]
SOUL = next(b for b in PROMOTED_BUCKETS if b.display == "Soul")
LEVELS = [None, *range(1, 11)]
PLAIN = next(b for b in TAXONOMY.buckets if b.energy.enabled and not b.energy.band_display)


def resolved_display(value: str) -> str:
    return DISPLAY[routing.resolve_bucket(TAXONOMY, value).bucket_id]


# Routing


def test_the_corpus_actually_exercises_the_tiers_that_drift():
    """Guard the guard: without keyword and fallback hits, parity tests only the exact tier."""
    matches = [routing.resolve_bucket(TAXONOMY, value).match for value in legacy.CORPUS]
    assert matches.count(routing.Match.FUZZY) >= 10
    assert matches.count(routing.Match.FALLBACK) >= 10
    assert matches.count(routing.Match.PASSTHROUGH) >= 1


@pytest.mark.parametrize("value", ROUTING_PARITY_POPULATION)
def test_routing_resolves_every_source_string_identically(value):
    assert resolved_display(value) == legacy.resolve_genre(value)[0]


def test_the_promoted_buckets_take_exactly_what_the_old_code_filed_in_the_playlists_they_left():
    """R-797 and U118: each set is asked of the frozen code by the playlist it
    answers with, so a word gained or forgotten fails; one exception is named."""
    for place in {place.id: place for place in OLD_PLAYLIST.values()}.values():
        holder = TAXONOMY.bucket(place.bucket)
        filed_there_by_the_old_code = {
            value
            for value in POPULATION
            if legacy.resolve_genre(value)[0] == holder.display
            and legacy.energy_to_sub(5, holder.display, value) == place.display
        }
        assert filed_there_by_the_old_code, f"the frozen code no longer files in {place.display}"
        sharing = {bucket_id for bucket_id, old in OLD_PLAYLIST.items() if old == place}
        routed_there = {
            v for v in PROMOTED if routing.resolve_bucket(TAXONOMY, v).bucket_id in sharing
        }
        assert routed_there - NAMED_BY_THE_AUTHOR == filed_there_by_the_old_code, place.id
    assert NAMED_BY_THE_AUTHOR <= PROMOTED
    for value in NAMED_BY_THE_AUTHOR:
        assert legacy.resolve_genre(value)[0] == TAXONOMY.bucket(FORMER_PLACE.bucket).display
    assert PROMOTED == {alias for bucket in PROMOTED_BUCKETS for alias in bucket.aliases}
    for value in PROMOTED:
        assert routing.resolve_bucket(TAXONOMY, value).match is routing.Match.EXACT


def test_soul_and_r_and_b_divide_the_old_playlist_as_the_author_decided():
    """U118: a combined name files under its first word; R&B keeps R&B and MPB."""
    resolved = {v: routing.resolve_bucket(TAXONOMY, v).bucket_id for v in PROMOTED}
    assert {v for v, b in resolved.items() if b == SOUL.id} == {"Soul", "Soul / R&B"}
    assert {v for v, b in resolved.items() if b == PROMOTED_BUCKET.id} == {"R&B", "MPB"}


def test_the_one_keyword_rule_the_author_moved_takes_only_what_the_old_code_filed_by_it():
    """U133: the "jazz" rule moved with Jazz; the old code filed each word it
    sends there by that same keyword, and no other rule moved."""
    assert MOVED_BY_KEYWORD, "the corpus no longer carries a partial match to hold this"
    for value in MOVED_BY_KEYWORD:
        resolution = routing.resolve_bucket(TAXONOMY, value)
        assert resolution.matched_on in KEYWORDS_MOVED, value
        old = OLD_PLAYLIST[resolution.bucket_id]
        assert legacy.resolve_genre(value) == (
            TAXONOMY.bucket(old.bucket).display, f"fuzzy {resolution.matched_on}"
        ), value
    assert {rule.keyword for rule in TAXONOMY.fuzzy if rule.bucket in OLD_PLAYLIST} == KEYWORDS_MOVED


def test_the_keyword_rules_were_not_repointed_by_the_promotion():
    """A partial match on R&B's and Soul's words lands where it always did."""
    partial = [v for v in ROUTING_PARITY_POPULATION if v.lower() in {"soul", "r&b", "soul / r&b"}]
    assert partial, "the corpus no longer carries a partial match to hold this"
    for value in partial:
        assert routing.resolve_bucket(TAXONOMY, value).bucket_id == FORMER_PLACE.bucket


def test_routing_never_raises_and_always_lands():
    """A missing answer would leave a track with no place in the tree."""
    for value in [*POPULATION, "", "   ", "¡nunca visto!", "🎧"]:
        assert routing.resolve_bucket(TAXONOMY, value).bucket_id in TAXONOMY.bucket_ids()
    assert routing.resolve_bucket(TAXONOMY, None).bucket_id == TAXONOMY.fallback.bucket


def test_an_unmapped_genre_lands_in_the_declared_fallback():
    resolution = routing.resolve_bucket(TAXONOMY, "gouranga")
    assert resolution.bucket_id == TAXONOMY.fallback.bucket
    assert resolution.match is routing.Match.FALLBACK


def test_the_fallback_is_visible_rather_than_indistinguishable():
    """A structured match value says which tier answered."""
    assert routing.resolve_bucket(TAXONOMY, "Deep House").match is routing.Match.EXACT
    assert routing.resolve_bucket(TAXONOMY, "Psy-Trance").match is routing.Match.FUZZY
    assert routing.resolve_bucket(TAXONOMY, "Psy-Trance").matched_on == "trance"


# Energy: every bucket crossed with every level


def test_every_bucket_and_level_lands_in_the_same_sub():
    """198 cases, pinning the per-bucket exceptions and the band-label override."""
    for bucket in TAXONOMY.buckets:
        for level in LEVELS:
            sub = routing.energy_sub(TAXONOMY, bucket.id, level)
            assert sub is not None
            assert sub.display == legacy.energy_to_sub(level, bucket.display), (
                bucket.display,
                level,
            )


def test_the_source_routed_bucket_matches_for_every_source_string():
    """The one bucket that routes by the source genre, unmapped strings included."""
    bucket = next(b for b in TAXONOMY.buckets if b.sub_by_source is not None)
    for value in ROUTING_PARITY_POPULATION:
        sub = routing.energy_sub(TAXONOMY, bucket.id, 5, source_genre=value)
        assert sub is not None
        assert sub.display == legacy.energy_to_sub(5, bucket.display, value), value


def test_a_bucket_with_no_energy_split_ignores_the_level_entirely():
    """Checked before the missing level, since this bucket has no no-energy sink."""
    bucket = next(
        b for b in TAXONOMY.buckets if not b.energy.enabled and b.single_sub is not None
    )
    subs = {routing.energy_sub(TAXONOMY, bucket.id, level).id for level in LEVELS}
    assert subs == {bucket.single_sub.id}
    assert routing.no_energy_sub(TAXONOMY, bucket.id) is None


def test_the_renamed_band_bucket_keeps_the_shared_cuts():
    """Only the labels differ, so the two copies cannot drift apart."""
    renamed = next(b for b in TAXONOMY.buckets if b.energy.band_display)
    for level in range(1, 11):
        here = routing.energy_sub(TAXONOMY, renamed.id, level)
        there = routing.energy_sub(TAXONOMY, PLAIN.id, level)
        assert here.id == there.id
        assert here.display != there.display


@pytest.mark.parametrize("level", LEVELS)
def test_the_star_curve_is_unchanged(level):
    assert routing.energy_rating(TAXONOMY, level) == legacy.energy_to_rating(level)


@pytest.mark.parametrize("policy", ["manual", "derived"], ids=["reserved", "derived"])
def test_the_reserved_and_derived_subs_are_never_returned_by_routing(policy):
    """The reserved sub is asserted, not merely absent; the derived one is
    additive, so returning it would make it a replacement."""
    held = {e.display for e in TAXONOMY.sub_classes if e.policy.value == policy}
    assert held
    produced = {
        routing.energy_sub(TAXONOMY, bucket.id, level).display
        for bucket in TAXONOMY.buckets
        for level in LEVELS
    }
    assert not produced & held


# The divergent decile (seam decision D3)


def test_energy_level_four_follows_the_tree_rule_not_the_dashboard_rule():
    """Level 4 alone is the middle band in the tree and the low one on the
    dashboard. The tree wins: the dashboard reads a rating not always derived
    from energy. Asserted so nobody "fixes" it and re-files a tenth of a library."""
    tree_band = routing.energy_sub(TAXONOMY, PLAIN.id, 4)
    dashboard_band = legacy.stars_to_energy_band(
        legacy.RATING_TO_STARS[routing.energy_rating(TAXONOMY, 4)]
    )

    assert tree_band.display != dashboard_band
    assert tree_band.display == legacy.energy_to_sub(4, PLAIN.display)
    assert tree_band.id == TAXONOMY.energy.bands[1].id

    disagreeing = [
        level
        for level in range(1, 11)
        if routing.energy_sub(TAXONOMY, PLAIN.id, level).display
        != legacy.stars_to_energy_band(
            legacy.RATING_TO_STARS[routing.energy_rating(TAXONOMY, level)]
        )
    ]
    assert disagreeing == [4]


# Tempo priors


@pytest.mark.parametrize("value", [v for v in POPULATION if v.strip()])
def test_the_tempo_window_is_unchanged_for_every_source_string(value):
    prior = routing.bpm_prior(TAXONOMY, value)
    assert prior is not None
    assert (prior.start, prior.floor, prior.ceil) == legacy.prior_for_genre(value)


def test_an_untagged_track_now_uses_the_fallback_window_not_a_generic_one():
    """The one deliberate change: an empty genre takes the fallback bucket's
    declared window, not a hardcoded two-octave one the fold never fired on."""
    prior = routing.bpm_prior(TAXONOMY, "")
    assert prior == TAXONOMY.bucket(TAXONOMY.fallback.bucket).bpm
    assert (prior.start, prior.floor, prior.ceil) != legacy.prior_for_genre("")


# The family projection (a projection, never a merge)


@pytest.mark.parametrize("value", POPULATION)
def test_the_family_projection_matches_the_old_rules_applied_to_the_folder(value):
    """Exact against the old rules run on the folder, not the raw tag, which
    let a track score as a family its folder is not in."""
    assert routing.family_of(TAXONOMY, value) == legacy.family_of(
        legacy.resolve_genre(value)[0]
    )


def test_running_the_family_rules_on_the_raw_tag_was_the_bug_not_the_contract():
    """Two library strings the old raw-tag rules scored against their folder."""
    assert legacy.family_of("Afrobeat") != legacy.family_of(legacy.resolve_genre("Afrobeat")[0])
    assert routing.family_of(TAXONOMY, "Afrobeat") == legacy.family_of("NonElectronic")
    assert legacy.family_of("Amapiano") == "other"
    assert routing.family_of(TAXONOMY, "Amapiano") == legacy.family_of("Afro House")


def test_the_catch_all_family_awards_no_bonus():
    """Sharing the least informative family must not be the strongest signal."""
    catch_all = [b for b in TAXONOMY.buckets if b.family == TAXONOMY.family.catch_all]
    assert len(catch_all) >= 2
    assert routing.genre_affinity(
        TAXONOMY, catch_all[0].display, catch_all[1].display
    ) == TAXONOMY.family.unrelated


def test_affinity_is_unchanged_wherever_the_two_systems_agree_on_family():
    checked = 0
    for anchor in POPULATION[:120]:
        if legacy.family_of(anchor) != routing.family_of(TAXONOMY, anchor):
            continue
        for candidate in POPULATION[:40]:
            if legacy.family_of(candidate) != routing.family_of(TAXONOMY, candidate):
                continue
            checked += 1
            assert routing.genre_affinity(TAXONOMY, anchor, candidate) == pytest.approx(
                legacy.genre_affinity(anchor, candidate)
            )
    assert checked > 1000


def test_an_unknown_anchor_scores_neutral():
    assert routing.genre_affinity(TAXONOMY, "", "Deep House") == legacy.genre_affinity(
        "", "Deep House"
    )


# The acquisition gate


@pytest.mark.parametrize("value", POPULATION)
def test_the_gate_classifies_every_source_string_the_same_way(value):
    """The family names became identifiers, so droppability is what is compared."""
    assert (routing.gate_family(TAXONOMY, value) is None) == (legacy.gate_family(value) is None)


def test_the_whole_catalogue_gate_decision_is_unchanged():
    verdicts = [v.value for v in routing.gate_decisions(TAXONOMY, POPULATION)]
    assert verdicts == legacy.gate_decisions(POPULATION)


def test_a_catalogue_the_source_never_classified_keeps_everything():
    """Unclassified rows in the share would turn a timid gate aggressive."""
    assert routing.gate_decisions(TAXONOMY, ["", "", ""]) == [routing.GateVerdict.KEEP] * 3


def test_the_gate_keys_on_the_source_vocabulary_not_on_the_resolved_bucket():
    """A bucket refusal means the folder is uncertain; the family is still known."""
    assert routing.suggest_tag(TAXONOMY, "Techno").declined
    assert routing.gate_family(TAXONOMY, "Techno") is not None


# Tagging: allowed to decline


@pytest.mark.parametrize("value", SWEEP_PARITY_POPULATION)
def test_tagging_matches_the_old_sweep_resolver_wherever_no_alias_applies(value):
    """Outside a declared refusal and alias, identical decline for decline."""
    suggestion = routing.suggest_tag(TAXONOMY, value)
    tag, _flag = legacy.suggest_genre(value)
    assert (None if suggestion.declined else suggestion.tag) == (tag or None)


@pytest.mark.parametrize("value", TAGGER_PARITY_POPULATION)
def test_tagging_matches_the_old_tagger_except_on_a_declared_refusal(value):
    assert routing.suggest_tag(TAXONOMY, value).tag == legacy.normalize_genre(value)


def test_the_tagger_writes_the_promoted_buckets_name_where_it_wrote_the_old_playlists():
    """R-797 and U118: R&B's or Soul's name by the first word, no sub, and it
    routes there; the old playlist's name routes to Soul by the same rule."""
    assert RETAGGED, "the frozen tagger no longer answers with the old playlist's name"
    for value in sorted(RETAGGED):
        suggestion = routing.suggest_tag(TAXONOMY, value)
        expected = SOUL if value.startswith("soul") else PROMOTED_BUCKET
        assert (suggestion.bucket_id, suggestion.sub_id, suggestion.tag) == (
            expected.id, None, expected.display
        ), value
        assert routing.resolve_bucket(TAXONOMY, suggestion.tag).bucket_id == expected.id
    assert routing.resolve_bucket(TAXONOMY, FORMER_PLACE.display).bucket_id == SOUL.id
    assert routing.resolve_bucket(TAXONOMY, PROMOTED_BUCKET.display).bucket_id == PROMOTED_BUCKET.id


@pytest.mark.parametrize("value", ["House", "Disco", "Ambient", "Jackin House", "Trap / Future Bass"])
def test_the_sweep_gains_the_alias_table_it_never_had(value):
    """The old sweep wrote the source's word verbatim; the alias table writes
    this library's name for it, which still routes to the same bucket."""
    assert legacy.suggest_genre(value)[0] == value
    suggestion = routing.suggest_tag(TAXONOMY, value)
    assert suggestion.bucket_id is not None
    assert suggestion.tag == DISPLAY[suggestion.bucket_id]
    assert suggestion.tag != value
    assert routing.resolve_bucket(TAXONOMY, suggestion.tag).bucket_id == suggestion.bucket_id
    assert legacy.resolve_genre(value)[0] == suggestion.tag


def test_tagging_refuses_the_catch_all_buckets_both_old_taggers_disagreed_about():
    """The old tagger mapped these, the old sweep asked; the refusal wins as the
    reversible choice. A specific sub-genre of the family still resolves, which
    is why refusals are exact strings, not substrings."""
    for value in ("Techno", "Electronica", "Electronic", "Electronica / Other"):
        suggestion = routing.suggest_tag(TAXONOMY, value)
        assert suggestion.declined, value
        assert suggestion.decline is routing.Decline.ASK
        assert suggestion.tag is None
    assert routing.suggest_tag(TAXONOMY, "Techno (Peak Time / Driving)").tag == "Techno"
    assert legacy.suggest_genre("Techno (Peak Time / Driving)") == ("", "ASK")


def test_tagging_declines_on_nothing_at_all():
    for value in (None, "", "   "):
        assert routing.suggest_tag(TAXONOMY, value).decline is routing.Decline.NOT_FOUND


def test_tagging_never_falls_back_to_a_bucket():
    """A string nothing claims passes through as itself, flagged (R-650)."""
    suggestion = routing.suggest_tag(TAXONOMY, "Hyperpop Gabber Waltz")
    assert suggestion.bucket_id is None
    assert suggestion.tag == "Hyperpop Gabber Waltz"
    assert not suggestion.declined
    assert suggestion.off_taxonomy is True


def test_a_declared_tag_with_no_bucket_is_not_off_taxonomy():
    """``off_taxonomy`` is not ``bucket_id is None``: a declared bucketless rule
    is the template's deliberate gap, an undeclared word is the one to report."""
    declared = routing.suggest_tag(TAXONOMY, "melodic techno")
    assert declared.tag == "Melodic Techno"
    assert declared.bucket_id is None
    assert declared.declined is False
    assert declared.off_taxonomy is False
    undeclared = routing.suggest_tag(TAXONOMY, "gqom")
    assert undeclared.bucket_id is None
    assert undeclared.off_taxonomy is True


def test_only_the_last_tier_is_off_taxonomy():
    """One string per other tier: refusal, alias, bucket rule, the tempo split
    each way and with no tempo, the literal tag rule, and nothing at all."""
    for value, bpm in (
        ("Techno", None),
        ("Electronic", None),
        ("Deep House", None),
        ("Downtempo", None),
        ("Organic House / Downtempo", None),
        ("Organic House / Downtempo", 100.0),
        ("Organic House / Downtempo", 130.0),
        ("melodic techno", None),
        ("", None),
        (None, None),
    ):
        assert routing.suggest_tag(TAXONOMY, value, bpm=bpm).off_taxonomy is False, value


def test_the_tempo_split_is_unchanged_for_the_combined_source_bucket():
    """The only tagging rule reading tempo; with none it asks rather than guess."""
    for value in ("Organic House / Downtempo", "organic house / downtempo"):
        for bpm in (None, 100.0, 130.0):
            suggestion = routing.suggest_tag(TAXONOMY, value, bpm=bpm)
            tag, flag = legacy.suggest_genre(value, bpm)
            assert suggestion.tag == tag, (value, bpm)
            assert suggestion.needs_review == (flag == "REVIEW"), (value, bpm)


def test_the_tempo_split_no_longer_swallows_a_source_that_named_one_side():
    """The trigger narrowed from either term to both: a source naming one side
    outright is not moved to the other and flagged."""
    suggestion = routing.suggest_tag(TAXONOMY, "Downtempo")
    assert suggestion.tag == "Downtempo"
    assert suggestion.needs_review is False
    assert legacy.suggest_genre("Downtempo") == ("Organic House", "REVIEW")
    assert legacy.normalize_genre("Downtempo") == "Downtempo"
    assert legacy.resolve_genre("Downtempo")[0] == "Downtempo"


def test_an_exact_alias_beats_a_plain_substring_rule():
    """A declaration beats a substring guess; the tempo rule outranks the alias
    on the combined bucket, deciding on evidence the alias lacks."""
    declared, guessed = "Downtempo", "sunrise downtempo thing"
    assert TAXONOMY.tagging_alias(declared.lower()) is not None
    assert TAXONOMY.tagging_alias(guessed) is None
    assert routing.suggest_tag(TAXONOMY, declared).tag == declared
    assert routing.suggest_tag(TAXONOMY, guessed).tag != guessed
    assert routing.suggest_tag(TAXONOMY, guessed).bucket_id is not None
    assert routing.suggest_tag(TAXONOMY, "Organic House / Downtempo", bpm=100.0).tag == "Downtempo"


def test_a_source_string_naming_something_with_no_bucket_keeps_its_own_word():
    """A rule answering a tag and no bucket is a visible gap, not collapsed."""
    suggestion = routing.suggest_tag(TAXONOMY, "Melodic Techno")
    assert suggestion.bucket_id is None
    assert suggestion.tag == legacy.suggest_genre("Melodic Techno")[0]


@pytest.mark.parametrize(
    ("value", "tagged_as"),
    [
        ("Bass / Club", "UK Garage / Bassline"),
        ("Reggae", "Caribbean"),
        ("Trap / Wave", "Hip-Hop"),
    ],
)
def test_the_three_strings_the_two_old_tables_flatly_contradicted(value, tagged_as):
    """Tagging and routing disagree here, chained not parallel: the tagged file
    lands where its new tag says, an untouched one where the raw string says."""
    suggestion = routing.suggest_tag(TAXONOMY, value)
    assert suggestion.tag == tagged_as, value
    assert suggestion.tag == legacy.normalize_genre(value), value
    assert legacy.resolve_genre(value)[0] != tagged_as


def test_a_sub_playlist_name_can_be_the_tag_a_bucket_alias_is_not():
    """A tag may be a sub's name and still round trip to its bucket."""
    suggestion = routing.suggest_tag(TAXONOMY, "Classical")
    assert suggestion.sub_id is not None
    assert suggestion.tag == legacy.normalize_genre("Classical")
    assert routing.resolve_bucket(TAXONOMY, "Classical").bucket_id == suggestion.bucket_id


def test_the_two_coarse_source_strings_are_declared_unusable_as_a_final_tag():
    """One declaration replaces a reject set and a fallback name that never matched."""
    assert TAXONOMY.is_too_coarse_as_source("")
    assert TAXONOMY.is_too_coarse_as_source("Electronica")
    assert TAXONOMY.is_too_coarse_as_source(DISPLAY[TAXONOMY.fallback.bucket])
    assert not TAXONOMY.is_too_coarse_as_source("Deep House")


# The vocal cut: a value the caller supplies (seam decision D7)


def test_an_absent_vocal_threshold_routes_nothing_and_raises_nothing():
    """No lazy default reached up into an optional analysis module."""
    assert routing.routes_with_vox(90, None) is False
    assert routing.routes_with_vox(None, 5.0) is False
    assert routing.routes_with_vox(None, None) is False


def test_the_vocal_cut_is_inclusive_at_the_threshold():
    assert routing.routes_with_vox(5, 5.0) is True
    assert routing.routes_with_vox(4, 5.0) is False


def test_the_taxonomy_does_not_decide_the_vocal_cut():
    """A calibration the caller supplies, not a taxonomy fact."""
    assert list(inspect.signature(routing.routes_with_vox).parameters) == [
        "voxlevel",
        "threshold",
    ]
