"""Parity: the declared taxonomy answers exactly as the eight resolvers it replaced.

WHAT IS COMPARED, AND WHY IT IS NOT THE MAP KEYS. The obvious parity suite walks
the old lookup tables and checks each key still resolves the same. It proves
almost nothing. Every table key hits the exact-match tier by construction, so
such a suite exercises the exact tier and nothing else, while all the drift lives
in the keyword and fallback tiers, which by definition fire only on strings the
tables do NOT contain.

So the population here is the LIBRARY's own genre tag values plus the acquisition
sweeps' source strings: 105 distinct values, of which 25 appear in no table at
all. Those 25 cover 14 percent of a real library. They are the test.

The reference is tests/legacy_taxonomy.py, the original code frozen. Comparing
against code rather than against a typed table of expectations is what makes this
parity rather than a restatement.

WHERE THE NEW ENGINE DELIBERATELY DIFFERS. Consolidation resolves disagreements;
it cannot preserve both sides of one. Every difference is named below, in its own
test, with the reason. Nothing diverges silently, and a new divergence fails a
test rather than passing unnoticed.

The populations below are split at COLLECTION time rather than skipped at run
time. A skipped case is a case nobody reads; a case that is not collected is one
that another test owns, by name.
"""

from __future__ import annotations

import pytest

from cratekit.core import routing
from cratekit.core.taxonomy import default_taxonomy
from tests import legacy_taxonomy as legacy

# Reading the packaged default at import is safe: it is read-only data inside the
# wheel, and building a Taxonomy touches no state, no config, and no filesystem
# the isolation fixtures redirect.
TAXONOMY = default_taxonomy()
DISPLAY = {bucket.id: bucket.display for bucket in TAXONOMY.buckets}

# Every source string either system has an opinion about: the live library's
# values, the sweeps' values, and both old tables' keys.
POPULATION = sorted(set(legacy.CORPUS) | set(legacy.GENRE_MAP) | set(legacy.GENRE_NORMALIZE))

# The strings the template declares an outright refusal for. They have their own
# test, because they are the one place the consolidation had to choose a side.
REFUSED = {
    needle.lower()
    for rule in TAXONOMY.suggest
    if rule.equals and rule.decline
    for needle in rule.equals
}

# The strings the template declares an alias for. The acquisition sweep never had
# an alias table, so every one of these is a deliberate change to it, covered by
# its own test rather than by the sweep-parity sweep below.
ALIASED = {v for v in POPULATION if TAXONOMY.tagging_alias(v.lower().strip()) is not None}

SWEEP_PARITY_POPULATION = [
    v for v in POPULATION if v.lower().strip() not in REFUSED and v not in ALIASED
]

# THE BUCKETS THE OLD CODE NEVER HAD (R-797, U118, U133). The author moved R&B
# out of the source routed folder to a folder of its own on 2026-10-01, on
# 2026-10-09 split Soul out of R&B and moved Hip-Hop out the same way, and on
# 2026-10-12 moved Jazz out the same way, with its keyword rule. So the
# strings that filed in the two playlists they left now route to the new
# buckets, and the tagger writes R&B's or Soul's name where it wrote the old
# "Soul / R&B" playlist's. Every set is derived, from the engine or from the
# frozen code, and their own tests below hold them equal to what the old code
# filed there.
PROMOTED_BUCKETS = tuple(
    bucket for bucket in TAXONOMY.buckets if bucket.formerly or bucket.split_from
)


def _old_playlist(bucket):
    """The former place a promoted bucket's words were filed in by the old code.

    Its own, or for a bucket split out of a promoted one, that bucket's.
    """
    if bucket.formerly:
        return bucket.formerly[0]
    (holder,) = {place.bucket for place in bucket.split_from}
    return TAXONOMY.bucket(holder).formerly[0]


OLD_PLAYLIST = {bucket.id: _old_playlist(bucket) for bucket in PROMOTED_BUCKETS}
PROMOTED = {
    v
    for v in POPULATION
    if routing.resolve_bucket(TAXONOMY, v).bucket_id in OLD_PLAYLIST
    and routing.resolve_bucket(TAXONOMY, v).match is not routing.Match.FUZZY
}
#: The keyword rules the author moved with a promoted bucket, by keyword. Only
#: Jazz's moved (U133); R&B's and Hip-Hop's stayed (R-804, R-941).
KEYWORDS_MOVED = {"jazz"}
#: The words such a rule sends to a promoted bucket. The old code filed them in
#: the source routed folder by the same keyword, in its default sub.
MOVED_BY_KEYWORD = {
    v
    for v in POPULATION
    if routing.resolve_bucket(TAXONOMY, v).bucket_id in OLD_PLAYLIST
    and routing.resolve_bucket(TAXONOMY, v).match is routing.Match.FUZZY
}
#: The one word filed in a promoted bucket that the old code filed elsewhere.
#: The author named it a Hip-Hop word on 2026-10-09 (U118); a keyword rule sent
#: it to the source routed folder's default sub.
NAMED_BY_THE_AUTHOR = {"Hip-hop & Rap"}
#: The old tagger's answers that were a playlist name the new tagger does not
#: write: the old "Soul / R&B" playlist, whose words are R&B's or Soul's now.
#: The old Hip-Hop playlist's name is the new bucket's, so its answers stand.
RETAGGED = {
    k
    for k in legacy.GENRE_NORMALIZE
    if any(
        legacy.normalize_genre(k) == place.display != TAXONOMY.bucket(bucket_id).display
        for bucket_id, place in OLD_PLAYLIST.items()
    )
}
#: The first of them, as R-797 declared it, for the tests that ask of one.
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


def resolved_display(value: str) -> str:
    return DISPLAY[routing.resolve_bucket(TAXONOMY, value).bucket_id]


# ═══════════════════════════════════════════════════════════════════════════
# Routing
# ═══════════════════════════════════════════════════════════════════════════


def test_the_corpus_actually_exercises_the_tiers_that_drift():
    """Guard the guard: if the corpus stops reaching the keyword and fallback
    tiers, every assertion below becomes a test of the exact-match tier only."""
    matches = [routing.resolve_bucket(TAXONOMY, value).match for value in legacy.CORPUS]
    assert matches.count(routing.Match.FUZZY) >= 10
    assert matches.count(routing.Match.FALLBACK) >= 10
    assert matches.count(routing.Match.PASSTHROUGH) >= 1


@pytest.mark.parametrize("value", ROUTING_PARITY_POPULATION)
def test_routing_resolves_every_source_string_identically(value):
    assert resolved_display(value) == legacy.resolve_genre(value)[0]


def test_the_promoted_buckets_take_exactly_what_the_old_code_filed_in_the_playlists_they_left():
    """R-797 and U118, and the only routing differences from the old code.

    The old code filed these strings in two playlists of the source routed
    folder. The author gave their genres folders of their own, so they route
    there now. Each set is asked of the FROZEN code, by the playlist name it
    answers with, so a string added to a new bucket that the old code filed
    anywhere else fails here, and so does one the old code filed there that the
    new buckets forgot. The one exception is named by the author.
    """
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
    """U118: a combined name files under its first word, so "Soul / R&B" is
    Soul's, and R&B keeps R&B and MPB. Asked by name, since this is the
    author's decision and not something the frozen code knew."""
    resolved = {v: routing.resolve_bucket(TAXONOMY, v).bucket_id for v in PROMOTED}
    soul = next(b.id for b in PROMOTED_BUCKETS if b.display == "Soul")
    assert {v for v, b in resolved.items() if b == soul} == {"Soul", "Soul / R&B"}
    assert {v for v, b in resolved.items() if b == PROMOTED_BUCKET.id} == {"R&B", "MPB"}


def test_the_one_keyword_rule_the_author_moved_takes_only_what_the_old_code_filed_by_it():
    """U133: the "jazz" rule moved with the Jazz bucket, so a partial match
    files in Jazz now. Every word it sends there, the old code filed in the
    source routed folder by that same keyword, and no other rule moved."""
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
    """A partial match on the promoted genre's words lands where it always did.

    Decided with the promotion and recorded as a residual: repointing the two
    keyword rules would route such a track to the new bucket while it sits in
    the old folder's default sub, which no verb settles. These are in the
    parity population above, so this names what that population is holding.
    """
    partial = [v for v in ROUTING_PARITY_POPULATION if v.lower() in {"soul", "r&b", "soul / r&b"}]
    assert partial, "the corpus no longer carries a partial match to hold this"
    for value in partial:
        assert routing.resolve_bucket(TAXONOMY, value).bucket_id == FORMER_PLACE.bucket


def test_routing_never_raises_and_always_lands():
    """Nine call sites build a plan keyed by bucket. A missing answer means a
    track enters the collection with no place in the tree and vanishes from it."""
    for value in [*POPULATION, "", "   ", "¡nunca visto!", "🎧"]:
        assert routing.resolve_bucket(TAXONOMY, value).bucket_id in TAXONOMY.bucket_ids()
    assert routing.resolve_bucket(TAXONOMY, None).bucket_id == TAXONOMY.fallback.bucket


def test_an_unmapped_genre_lands_in_the_declared_fallback():
    resolution = routing.resolve_bucket(TAXONOMY, "gouranga")
    assert resolution.bucket_id == TAXONOMY.fallback.bucket
    assert resolution.match is routing.Match.FALLBACK


def test_the_fallback_is_visible_rather_than_indistinguishable():
    """The old resolver returned a human note for exactly this, and two sweeps
    printed it. A structured match value renders the same line without a domain
    module writing prose."""
    assert routing.resolve_bucket(TAXONOMY, "Deep House").match is routing.Match.EXACT
    assert routing.resolve_bucket(TAXONOMY, "Psy-Trance").match is routing.Match.FUZZY
    assert routing.resolve_bucket(TAXONOMY, "Psy-Trance").matched_on == "trance"


# ═══════════════════════════════════════════════════════════════════════════
# Energy: every bucket crossed with every level
# ═══════════════════════════════════════════════════════════════════════════

LEVELS = [None, *range(1, 11)]


def test_every_bucket_and_level_lands_in_the_same_sub():
    """198 cases. This is the assertion that pins all three per-bucket
    exceptions and the band-label override at once."""
    for bucket in TAXONOMY.buckets:
        for level in LEVELS:
            sub = routing.energy_sub(TAXONOMY, bucket.id, level)
            assert sub is not None
            assert sub.display == legacy.energy_to_sub(level, bucket.display), (
                bucket.display,
                level,
            )


def test_the_source_routed_bucket_matches_for_every_source_string():
    """The one bucket that ignores energy and routes by the source genre,
    including the landing place for anything unmapped."""
    bucket = next(b for b in TAXONOMY.buckets if b.sub_by_source is not None)
    # The strings R-797 moved to a bucket of their own never reach this one.
    for value in ROUTING_PARITY_POPULATION:
        sub = routing.energy_sub(TAXONOMY, bucket.id, 5, source_genre=value)
        assert sub is not None
        assert sub.display == legacy.energy_to_sub(5, bucket.display, value), value


def test_a_bucket_with_no_energy_split_ignores_the_level_entirely():
    """Its check runs BEFORE the missing-level check, and the order is load
    bearing: this bucket has no sink in the real library, so a track with no
    energy reading would otherwise be routed to a sub that does not exist."""
    bucket = next(
        b for b in TAXONOMY.buckets if not b.energy.enabled and b.single_sub is not None
    )
    subs = {routing.energy_sub(TAXONOMY, bucket.id, level).id for level in LEVELS}
    assert subs == {bucket.single_sub.id}
    assert routing.no_energy_sub(TAXONOMY, bucket.id) is None


def test_the_renamed_band_bucket_keeps_the_shared_cuts():
    """Only the labels differ. If the CUTS had been overridden instead, the two
    copies could drift apart the moment either moved."""
    renamed = next(b for b in TAXONOMY.buckets if b.energy.band_display)
    plain = next(b for b in TAXONOMY.buckets if b.energy.enabled and not b.energy.band_display)
    for level in range(1, 11):
        here = routing.energy_sub(TAXONOMY, renamed.id, level)
        there = routing.energy_sub(TAXONOMY, plain.id, level)
        assert here.id == there.id
        assert here.display != there.display


@pytest.mark.parametrize("level", LEVELS)
def test_the_star_curve_is_unchanged(level):
    assert routing.energy_rating(TAXONOMY, level) == legacy.energy_to_rating(level)


def _every_sub_routing_can_produce() -> set[str]:
    return {
        routing.energy_sub(TAXONOMY, bucket.id, level).display
        for bucket in TAXONOMY.buckets
        for level in LEVELS
    }


def test_the_reserved_sub_is_never_returned_by_routing():
    """Asserted, not merely absent from the code. The old rule lived in a
    docstring and was enforced only by that string not appearing in the body."""
    manual = {e.display for e in TAXONOMY.sub_classes if e.policy.value == "manual"}
    assert manual
    assert not _every_sub_routing_can_produce() & manual


def test_the_derived_sub_is_never_returned_by_routing():
    """It is additive: a track keeps its energy sub AND gains this one. Returning
    it here would make it a REPLACEMENT, which is the opposite of the rule."""
    derived = {e.display for e in TAXONOMY.sub_classes if e.policy.value == "derived"}
    assert derived
    assert not _every_sub_routing_can_produce() & derived


# ═══════════════════════════════════════════════════════════════════════════
# The divergent decile (seam decision D3)
# ═══════════════════════════════════════════════════════════════════════════


def test_energy_level_four_follows_the_tree_rule_not_the_dashboard_rule():
    """ONE energy level reads differently in the tree and on the dashboard, and
    it is level 4. The tree calls it the middle band; the dashboard, which folds
    five stars back into three bands, calls it the low one.

    THE TREE RULE WINS. Two reasons, and the second is stronger than the first:

    1. the dashboard is the divergent consumer and stays on the old system;
    2. the dashboard's band is not a function of energy at all in the general
       case. It reads a rating field that automation only writes when that field
       is still unset, so every hand-rated or legacy-rated track feeds it a
       number never derived from its current energy.

    Asserted by name so nobody later "fixes" the dashboard into agreeing and
    quietly re-files a tenth of a library.
    """
    plain = next(b for b in TAXONOMY.buckets if b.energy.enabled and not b.energy.band_display)
    tree_band = routing.energy_sub(TAXONOMY, plain.id, 4)
    dashboard_band = legacy.stars_to_energy_band(
        legacy.RATING_TO_STARS[routing.energy_rating(TAXONOMY, 4)]
    )

    assert tree_band.display != dashboard_band
    assert tree_band.display == legacy.energy_to_sub(4, plain.display)
    assert tree_band.id == TAXONOMY.energy.bands[1].id

    disagreeing = [
        level
        for level in range(1, 11)
        if routing.energy_sub(TAXONOMY, plain.id, level).display
        != legacy.stars_to_energy_band(
            legacy.RATING_TO_STARS[routing.energy_rating(TAXONOMY, level)]
        )
    ]
    assert disagreeing == [4]


# ═══════════════════════════════════════════════════════════════════════════
# Tempo priors
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("value", [v for v in POPULATION if v.strip()])
def test_the_tempo_window_is_unchanged_for_every_source_string(value):
    prior = routing.bpm_prior(TAXONOMY, value)
    assert prior is not None
    assert (prior.start, prior.floor, prior.ceil) == legacy.prior_for_genre(value)


def test_an_untagged_track_now_uses_the_fallback_window_not_a_generic_one():
    """The one deliberate change, and it removes the last hardcoded default.

    The old code short-circuited on an empty genre to a window spanning most of
    two octaves, so the fold that catches half-time and double-time errors never
    fired for an untagged track. Resolving through the fallback bucket gives that
    track the window the library's own catch-all declares, which is narrower and
    is a value the user can change.
    """
    prior = routing.bpm_prior(TAXONOMY, "")
    assert prior == TAXONOMY.bucket(TAXONOMY.fallback.bucket).bpm
    assert (prior.start, prior.floor, prior.ceil) != legacy.prior_for_genre("")


# ═══════════════════════════════════════════════════════════════════════════
# The family projection (a projection, never a merge)
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("value", POPULATION)
def test_the_family_projection_matches_the_old_rules_applied_to_the_folder(value):
    """The projection is exact against the old rules run on the FOLDER.

    That is the correct comparison. The old code ran them on the RAW TAG, which
    is a different question and gave a different answer for 461 pairs in a 24000
    pair sample: a track could sit in one folder and score as a family that
    folder is not in. Reading the family off the resolved bucket ends that by
    construction.
    """
    assert routing.family_of(TAXONOMY, value) == legacy.family_of(
        legacy.resolve_genre(value)[0]
    )


def test_running_the_family_rules_on_the_raw_tag_was_the_bug_not_the_contract():
    """Two named cases where the old raw-tag rules contradicted the tree.

    Both are strings the library actually contains. One is filed as
    non-electronic yet scored as house; the other is filed under a house folder
    yet scored as unrelated. Neither can happen now.
    """
    assert legacy.family_of("Afrobeat") != legacy.family_of(legacy.resolve_genre("Afrobeat")[0])
    assert routing.family_of(TAXONOMY, "Afrobeat") == legacy.family_of("NonElectronic")

    assert legacy.family_of("Amapiano") == "other"
    assert routing.family_of(TAXONOMY, "Amapiano") == legacy.family_of("Afro House")


def test_the_catch_all_family_awards_no_bonus():
    """Two buckets share it without being alike. Rewarding them for sharing the
    least informative answer would make it the strongest signal in the ranker."""
    catch_all = [b for b in TAXONOMY.buckets if b.family == TAXONOMY.family.catch_all]
    assert len(catch_all) >= 2
    assert routing.genre_affinity(
        TAXONOMY, catch_all[0].display, catch_all[1].display
    ) == TAXONOMY.family.unrelated


def test_affinity_is_unchanged_wherever_the_two_systems_agree_on_family():
    """Where the projection and the raw-tag rules agree, the score must too."""
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
    """An unowned anchor with no genre must let genre neither help nor hurt."""
    assert routing.genre_affinity(TAXONOMY, "", "Deep House") == legacy.genre_affinity(
        "", "Deep House"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The acquisition gate
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("value", POPULATION)
def test_the_gate_classifies_every_source_string_the_same_way(value):
    """The gate's family names were renamed to identifiers, so what is compared
    is whether a string is droppable at all, not the label put on it."""
    assert (routing.gate_family(TAXONOMY, value) is None) == (legacy.gate_family(value) is None)


def test_the_whole_catalogue_gate_decision_is_unchanged():
    verdicts = [v.value for v in routing.gate_decisions(TAXONOMY, POPULATION)]
    assert verdicts == legacy.gate_decisions(POPULATION)


def test_a_catalogue_the_source_never_classified_keeps_everything():
    """Counting unclassified rows in the share would dilute every share toward
    zero and turn a timid gate into an aggressive one."""
    assert routing.gate_decisions(TAXONOMY, ["", "", ""]) == [routing.GateVerdict.KEEP] * 3


def test_the_gate_keys_on_the_source_vocabulary_not_on_the_resolved_bucket():
    """Deliberate, and the reason is precise: a bucket-level refusal means the
    FOLDER is uncertain, while a confident source sub-genre is still a confident
    FAMILY signal. Merging them undid a softening that had been dropping most of
    a legitimate catalogue."""
    assert routing.suggest_tag(TAXONOMY, "Techno").declined
    assert routing.gate_family(TAXONOMY, "Techno") is not None


# ═══════════════════════════════════════════════════════════════════════════
# Tagging: allowed to decline
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("value", SWEEP_PARITY_POPULATION)
def test_tagging_matches_the_old_sweep_resolver_wherever_no_alias_applies(value):
    """Outside a declared refusal and a declared alias, the answers are
    identical, decline for decline."""
    suggestion = routing.suggest_tag(TAXONOMY, value)
    tag, _flag = legacy.suggest_genre(value)
    assert (None if suggestion.declined else suggestion.tag) == (tag or None)


@pytest.mark.parametrize("value", TAGGER_PARITY_POPULATION)
def test_tagging_matches_the_old_tagger_except_on_a_declared_refusal(value):
    assert routing.suggest_tag(TAXONOMY, value).tag == legacy.normalize_genre(value)


def test_the_tagger_writes_the_promoted_buckets_name_where_it_wrote_the_old_playlists():
    """R-797 and U118. The old tagger answered these with the name of the
    playlist R&B left. The answer is a new folder's name now, R&B's or Soul's
    by the first word, a bucket and no sub, and a file carrying it routes
    there. A file still carrying the old playlist's name routes to Soul, by
    the same first word rule."""
    assert RETAGGED, "the frozen tagger no longer answers with the old playlist's name"
    soul = next(b for b in PROMOTED_BUCKETS if b.display == "Soul")
    for value in sorted(RETAGGED):
        suggestion = routing.suggest_tag(TAXONOMY, value)
        expected = soul if value.startswith("soul") else PROMOTED_BUCKET
        assert (suggestion.bucket_id, suggestion.sub_id, suggestion.tag) == (
            expected.id, None, expected.display
        ), value
        assert routing.resolve_bucket(TAXONOMY, suggestion.tag).bucket_id == expected.id
    assert routing.resolve_bucket(TAXONOMY, FORMER_PLACE.display).bucket_id == soul.id
    assert routing.resolve_bucket(TAXONOMY, PROMOTED_BUCKET.display).bucket_id == PROMOTED_BUCKET.id


def test_the_sweep_gains_the_alias_table_it_never_had():
    """The single largest deliberate change, and the reason the sweep-parity
    population above excludes anything with an alias.

    The old sweep had no exact table at all: a source string no ordered rule
    claimed was written onto the file verbatim. The tagger, on the same string,
    wrote this library's own name for it. So the SAME track acquired two ways
    ended up with two different genre tags, and both routed to the same folder
    only because the routing table happened to accept either.

    The alias table wins. It is the shared declaration; keeping the sweep's
    verbatim behaviour would mean keeping a second vocabulary with no table.
    Nothing is lost: the source string is still what the sweep records for
    review, and routing still resolves it if it is left on the file.
    """
    for value in ("House", "Disco", "Ambient", "Jackin House", "Trap / Future Bass"):
        # The old sweep wrote the source's own word onto the file.
        assert legacy.suggest_genre(value)[0] == value
        suggestion = routing.suggest_tag(TAXONOMY, value)
        # The new engine writes this library's name for it, from the one table.
        assert suggestion.bucket_id is not None
        assert suggestion.tag == DISPLAY[suggestion.bucket_id]
        assert suggestion.tag != value
        # And the tag it writes still routes to the same bucket, so nothing moves.
        assert routing.resolve_bucket(TAXONOMY, suggestion.tag).bucket_id == suggestion.bucket_id
        assert legacy.resolve_genre(value)[0] == suggestion.tag


def test_tagging_refuses_the_catch_all_buckets_both_old_taggers_disagreed_about():
    """The one place the consolidation had to choose, so it is asserted by name.

    The old tagger MAPPED a source taxonomy's catch-all bucket onto this
    library's catch-all folder and wrote it to the file, while the old sweep
    refused the same string and asked. They cannot both be kept.

    The refusal wins, and the old tagger's own table says why: its comment
    forbids writing the bare catch-all as a final tag, three lines above the
    entry that writes it. The refusal is also the reversible choice, since a
    refused string is surfaced for a human while a written one becomes the file's
    genre until somebody notices.

    Each of these is one line in the template. A user who disagrees deletes it.
    """
    for value in ("Techno", "Electronica", "Electronic", "Electronica / Other"):
        suggestion = routing.suggest_tag(TAXONOMY, value)
        assert suggestion.declined, value
        assert suggestion.decline is routing.Decline.ASK
        assert suggestion.tag is None

    # A SPECIFIC sub-genre of the same family still resolves, which is exactly
    # why the refusals are exact strings and not substrings. The old sweep
    # refused these too, on a substring, and the library holds 60 tracks that
    # disagree with it.
    assert routing.suggest_tag(TAXONOMY, "Techno (Peak Time / Driving)").tag == "Techno"
    assert legacy.suggest_genre("Techno (Peak Time / Driving)") == ("", "ASK")


def test_tagging_declines_on_nothing_at_all():
    for value in (None, "", "   "):
        assert routing.suggest_tag(TAXONOMY, value).decline is routing.Decline.NOT_FOUND


def test_tagging_never_falls_back_to_a_bucket():
    """Routing always lands; tagging must never invent. A string nothing claims
    passes through as itself, which is how a genuinely new genre survives long
    enough for somebody to notice it."""
    suggestion = routing.suggest_tag(TAXONOMY, "Hyperpop Gabber Waltz")
    assert suggestion.bucket_id is None
    assert suggestion.tag == "Hyperpop Gabber Waltz"
    assert not suggestion.declined
    # The noticing, which until R-650 was a hope in a docstring.
    assert suggestion.off_taxonomy is True


def test_a_declared_tag_with_no_bucket_is_not_off_taxonomy():
    """The pair that proves ``off_taxonomy`` is not ``bucket_id is None``.

    Both of these answer with a tag and no bucket, and they are not the same
    thing. ``Melodic Techno`` is a rule in the shipped template with a comment
    saying why it has no folder, so the author already knows. The other is a word
    nobody has declared anywhere, and the report exists to name it. Reading the
    first as the second would report the template's own deliberate gap on every
    sweep that meets it, which is how a warning becomes noise nobody reads.
    """
    declared = routing.suggest_tag(TAXONOMY, "melodic techno")
    assert declared.tag == "Melodic Techno"
    assert declared.bucket_id is None
    assert declared.declined is False
    assert declared.off_taxonomy is False

    undeclared = routing.suggest_tag(TAXONOMY, "gqom")
    assert undeclared.bucket_id is None
    assert undeclared.off_taxonomy is True


def test_only_the_last_tier_is_off_taxonomy():
    """Every other tier of the shipped table leaves the flag alone.

    One string per tier, driven rather than argued: an exact refusal, an alias,
    a bucket rule, the tempo split on both sides and with no tempo, the literal
    tag rule, and nothing at all.
    """
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
    """The only tagging rule that reads tempo, including the no-tempo path that
    takes the safe side and asks rather than guessing."""
    for value in ("Organic House / Downtempo", "organic house / downtempo"):
        for bpm in (None, 100.0, 130.0):
            suggestion = routing.suggest_tag(TAXONOMY, value, bpm=bpm)
            tag, flag = legacy.suggest_genre(value, bpm)
            assert suggestion.tag == tag, (value, bpm)
            assert suggestion.needs_review == (flag == "REVIEW"), (value, bpm)


def test_the_tempo_split_no_longer_swallows_a_source_that_named_one_side():
    """The split's trigger was narrowed from either term to both, deliberately.

    The old rule fired on either, so a source string that names one of these two
    buckets OUTRIGHT was moved to the other one and flagged for review. Routing
    and the tagger both disagreed with it, and the library holds 87 tracks tagged
    with the string it moved. A source that already named a side does not need
    splitting; the combined bucket does.
    """
    suggestion = routing.suggest_tag(TAXONOMY, "Downtempo")
    assert suggestion.tag == "Downtempo"
    assert suggestion.needs_review is False
    assert legacy.suggest_genre("Downtempo") == ("Organic House", "REVIEW")
    assert legacy.normalize_genre("Downtempo") == "Downtempo"
    assert legacy.resolve_genre("Downtempo")[0] == "Downtempo"


def test_an_exact_alias_beats_a_plain_substring_rule():
    """Precedence, stated and asserted, on one source string and one that is not.

    A declaration is a statement; a substring is a guess. The two exceptions are
    a refusal and the tempo rule, both of which decide on more than a name.
    """
    declared, guessed = "Downtempo", "sunrise downtempo thing"
    assert TAXONOMY.tagging_alias(declared.lower()) is not None
    assert TAXONOMY.tagging_alias(guessed) is None

    # Declared: the alias answers, and the substring rule never runs.
    assert routing.suggest_tag(TAXONOMY, declared).tag == declared
    # Undeclared: the same substring rule is what answers.
    assert routing.suggest_tag(TAXONOMY, guessed).tag != guessed
    assert routing.suggest_tag(TAXONOMY, guessed).bucket_id is not None

    # The tempo rule is the exception, and outranks the alias on the combined
    # source bucket because it is deciding on evidence the alias does not have.
    assert routing.suggest_tag(TAXONOMY, "Organic House / Downtempo", bpm=100.0).tag == "Downtempo"


def test_a_source_string_naming_something_with_no_bucket_keeps_its_own_word():
    """A declared rule may answer with a tag and no bucket. That is a gap in the
    taxonomy made visible, not a bug: collapsing it into a neighbouring bucket is
    the one thing the rule above it exists to prevent."""
    suggestion = routing.suggest_tag(TAXONOMY, "Melodic Techno")
    assert suggestion.bucket_id is None
    assert suggestion.tag == legacy.suggest_genre("Melodic Techno")[0]


def test_the_three_strings_the_two_old_tables_flatly_contradicted():
    """Routing and tagging genuinely disagree on three source strings, and the
    disagreement is now VISIBLE in one file instead of split across two tables
    that never referenced each other.

    It is also coherent rather than accidental: tagging rewrites the file's genre
    to this library's own name, and routing then resolves THAT. The two are
    chained, not parallel, so a track acquired through tagging lands where its
    new tag says, and an untouched file carrying the raw string lands where the
    raw string says.
    """
    for value, tagged_as in (
        ("Bass / Club", "UK Garage / Bassline"),
        ("Reggae", "Caribbean"),
        ("Trap / Wave", "Hip-Hop"),
    ):
        suggestion = routing.suggest_tag(TAXONOMY, value)
        assert suggestion.tag == tagged_as, value
        assert suggestion.tag == legacy.normalize_genre(value), value
        assert legacy.resolve_genre(value)[0] != tagged_as


def test_a_sub_playlist_name_can_be_the_tag_a_bucket_alias_is_not():
    """Nine of the old tagger's answers were sub-playlist names rather than
    folder names, and the round trip only worked because the routing table
    happened to contain all nine as keys. Declared explicitly now. Six are
    left since R-797, U118 and U133 gave three of the nine folders of their
    own, so the example is one that is still a sub."""
    suggestion = routing.suggest_tag(TAXONOMY, "Classical")
    assert suggestion.sub_id is not None
    assert suggestion.tag == legacy.normalize_genre("Classical")
    assert routing.resolve_bucket(TAXONOMY, "Classical").bucket_id == suggestion.bucket_id


def test_the_two_coarse_source_strings_are_declared_unusable_as_a_final_tag():
    """Replaces two separate constants that always meant the same thing: a reject
    set used to decide whether a lookup improved on an existing tag, and a
    fallback folder name used to decide whether a track counted as a taxonomy
    gap. They were never the same string."""
    assert TAXONOMY.is_too_coarse_as_source("")
    assert TAXONOMY.is_too_coarse_as_source("Electronica")
    assert TAXONOMY.is_too_coarse_as_source(DISPLAY[TAXONOMY.fallback.bucket])
    assert not TAXONOMY.is_too_coarse_as_source("Deep House")


# ═══════════════════════════════════════════════════════════════════════════
# The vocal cut: a value the caller supplies (seam decision D7)
# ═══════════════════════════════════════════════════════════════════════════


def test_an_absent_vocal_threshold_routes_nothing_and_raises_nothing():
    """The first of the two live layering violations this port fixes.

    The old router reached UPWARD into an analysis module, lazily, to default
    this. That module is an optional extra, so a slim install raised ImportError
    on the first vocal track and the traceback named an import inside a function
    rather than the packaging decision behind it.
    """
    assert routing.routes_with_vox(90, None) is False
    assert routing.routes_with_vox(None, 5.0) is False
    assert routing.routes_with_vox(None, None) is False


def test_the_vocal_cut_is_inclusive_at_the_threshold():
    assert routing.routes_with_vox(5, 5.0) is True
    assert routing.routes_with_vox(4, 5.0) is False


def test_the_taxonomy_does_not_decide_the_vocal_cut():
    """It is a calibration, not a taxonomy fact. Two libraries with the same tree
    can have different cuts, and one with no vocal analysis has none."""
    import inspect

    assert list(inspect.signature(routing.routes_with_vox).parameters) == [
        "voxlevel",
        "threshold",
    ]
