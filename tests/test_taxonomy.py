"""The template is data, and a template that cannot be trusted is refused at load.

Each rule is proved to bite on a mutated template, and a second taxonomy sharing
nothing with the default proves the engine reads its taxonomy. Parity against
the old resolvers is in tests/test_routing_parity.py.
"""

from __future__ import annotations

import copy
import enum
import tomllib
from pathlib import Path

import pytest

from cratekit.core import routing
from cratekit.core.taxonomy import (
    DEFAULT_TEMPLATE_NAME,
    SubPolicy,
    TaxonomyError,
    build_taxonomy,
    default_taxonomy,
    load_taxonomy,
    shipped_template_text,
)
from tests._taxonomy_parses import counted, renamed_in_place, unique

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


# The shipped default is loadable and internally consistent.


def test_the_shipped_default_loads(default):
    # 2 for a former place (R-797), 3 a split place (U118), 4 a playlist sub
    # class (U119), 5 a genre sub (U155): a template states the version it needs.
    assert default.schema_version == 5
    assert default.buckets
    assert default.fallback.bucket in default.bucket_ids()


def test_every_bucket_declares_a_tempo_window(default):
    """With no window an octave wide one folds nothing, silently ending the octave defence."""
    assert default.buckets_without_bpm_prior() == ()


@pytest.mark.parametrize("node", ["tree", "intake", "catalog", "long_tracks", "inspiration"])
def test_each_root_node_is_declared_by_id_and_display(default, node):
    """R19: root literals are data; catalog, long track (U88) and inspiration (U121) declared."""
    declared = getattr(default, node)
    assert declared is not None and declared.id and declared.display


def test_the_long_track_bound_and_the_inspiration_folder_ship_as_the_source_system_had_them(default):
    assert default.long_tracks.over_seconds == 1200
    assert default.inspiration.id == "inspiration"
    assert default.inspiration.display == "INSPIRATION"


def test_the_reserved_and_derived_subs_carry_different_policies(default):
    """Two flags, not one 'excluded' flag, and the difference is the bug it stops."""
    policies = {entry.id: entry.policy for entry in default.sub_classes}
    assert SubPolicy.MANUAL in policies.values()
    assert SubPolicy.DERIVED in policies.values()
    derived = [entry for entry in default.sub_classes if entry.policy is SubPolicy.DERIVED]
    # Two since U119, the vocal class and the genre Favorites, each additive.
    assert len(derived) == 2 and all(entry.additive for entry in derived)


@pytest.mark.parametrize("section", ["catalog", "long_tracks", "inspiration"])
def test_a_template_declaring_no_optional_section_loads_clean(default_raw, section):
    """Absent is a complete declaration, or deleting an unused section refuses all."""
    data = mutated(default_raw, lambda d: d.pop(section))
    assert getattr(build_taxonomy(data), section) is None


def test_a_long_track_playlist_with_no_bound_takes_the_source_systems(default_raw):
    data = mutated(default_raw, lambda d: d["long_tracks"].pop("over_seconds"))
    assert build_taxonomy(data).long_tracks.over_seconds == 1200


def test_rating_cuts_are_not_required_to_align_with_band_cuts(default):
    """Deliberate: forcing them to agree would re-rate a library when either moved."""
    band_cuts = {band.max for band in default.energy.bands}
    rating_cuts = {cut.max for cut in default.energy.rating_cuts}
    assert band_cuts != rating_cuts


# Loader validation: each rule bites, on one mutation of the shipped template.


def _walk(d, path):
    for step in path:
        d = step(d) if callable(step) else d[step]
    return d


def _get(*path):
    return lambda d: _walk(d, path)


def _set(path: tuple, value):
    """A mutation setting ``path``'s key; a callable step applies, a callable value reads."""

    def mutate(d):
        _walk(d, path[:-1])[path[-1]] = value(d) if callable(value) else value

    return mutate


def _all(*mutations):
    def mutate(d):
        for each in mutations:
            each(d)

    return mutate


def _promoted(data: dict) -> dict:
    """The bucket of the shipped template that declares a former place."""
    return next(bucket for bucket in data["bucket"] if bucket.get("formerly"))


def _holder(data: dict) -> dict:
    """The bucket whose folder holds that former place."""
    former = _promoted(data)["formerly"][0]
    return next(bucket for bucket in data["bucket"] if bucket["id"] == former["bucket"])


def _another_bucket(data: dict) -> dict:
    return next(
        bucket
        for bucket in data["bucket"]
        if not bucket.get("formerly") and bucket["id"] != _holder(data)["id"]
    )


def _splitter(data: dict) -> dict:
    """The bucket of the shipped template that declares split places."""
    return next(bucket for bucket in data["bucket"] if bucket.get("split_from"))


def _split_holder(data: dict) -> dict:
    """The bucket whose bands those split places are."""
    place = _splitter(data)["split_from"][0]
    return next(bucket for bucket in data["bucket"] if bucket["id"] == place["bucket"])


def _band_ids(data: dict) -> set:
    return {band["id"] for band in data["energy"]["bands"]} | {"unsorted"}


def _band_label_holder(data: dict) -> dict:
    return next(b for b in data["bucket"] if (b.get("energy") or {}).get("band_display"))


def _override_an_undeclared_band(d):
    for bucket in d["bucket"]:
        if "band_display" in bucket.get("energy", {}):
            bucket["energy"]["band_display"]["nosuchband"] = "Whatever"
            return
    raise AssertionError("the default no longer overrides any band label")


def _route_by_source_outside_the_bucket(d):
    for bucket in d["bucket"]:
        if "sub_by_source" in bucket:
            bucket["sub_by_source"]["default"] = "not_a_sub"
            return
    raise AssertionError("the default no longer routes any bucket by source genre")


def _former_place_named_for_a_band(data):
    holder = _band_label_holder(data)
    former = _promoted(data)["formerly"][0]
    former["bucket"] = holder["id"]
    former["display"] = next(iter(holder["energy"]["band_display"].values()))


def _one_band_split_by_two_buckets(data):
    other = next(
        bucket
        for bucket in data["bucket"]
        if bucket["id"] not in (_splitter(data)["id"], _split_holder(data)["id"])
        and not bucket.get("sub_by_source")
        and (bucket.get("energy") or {}).get("enabled", True)
    )
    other["split_from"] = [dict(_splitter(data)["split_from"][0], id="another_id")]


def _split_another_buckets_former_place(data):
    hip_hop = next(b for b in data["bucket"] if b["id"] == "hip_hop")
    _splitter(data)["split_from"][0].update(
        sub=hip_hop["formerly"][0]["id"], display=hip_hop["formerly"][0]["display"]
    )


def _tagging_word_in_two_buckets(data):
    first = _splitter(data)
    other = next(b for b in data["bucket"] if b.get("tag_aliases") and b is not first)
    first.setdefault("tag_aliases", []).append(other["tag_aliases"][0])


def case(id_: str, mutate, *needles, absent: tuple = ()):
    """A refused mutation: needles a problem carries, alone or together; ``absent`` none carries."""
    return pytest.param(mutate, needles, absent, id=id_)


_FORMER = (_promoted, "formerly", 0)
_former = _get(*_FORMER)


def _former_copy(**changed):
    return lambda d: [dict(_former(d), **changed)]


_SPLIT = (_splitter, "split_from", 0)
_ONE_TABLE = {"id": "x", "bucket": "y", "sub": "z", "display": "One table"}


REFUSED = [
    case("unsupported-schema-version", _set(("schema_version",), 99), "schema_version"),
    # R19: an id is persisted, so it may never be a display name.
    case("display-name-as-id", _set(("bucket", 0, "id"), _get("bucket", 0, "display")), "must match"),
    # An optional section is checked as strictly as a mandatory one; the empty
    # table is falsy, so a truthiness test would skip it.
    *[
        row
        for section in ("catalog", "long_tracks", "inspiration")
        for row in (
            case(f"{section}-without-display", _set((section, "display"), ""), f"[{section}] display"),
            case(f"{section}-bad-id", _set((section, "id"), _get(section, "display")), f"[{section}] id"),
            case(f"{section}-header-only", _set((section,), {}), f"[{section}] id", f"[{section}] display"),
        )
    ],
    case("long-tracks-not-a-table", _set(("long_tracks",), "Sets"), "[long_tracks] must be a table"),
    case("inspiration-not-a-table", _set(("inspiration",), "INSPIRATION"), "[inspiration] must be a table"),
    # A boolean, zero or a negative bound would put every track in the playlist.
    *[
        case(f"long-track-bound-{bound!r}", _set(("long_tracks", "over_seconds"), bound), "[long_tracks] over_seconds")
        for bound in (True, 0, -5, "1200", 1200.5)
    ],
    case("duplicate-bucket-id", _set(("bucket", 1, "id"), _get("bucket", 0, "id")), "duplicate bucket id"),
    # Two folders of one name and the XML bridge writes into whichever is first.
    case("duplicate-display", _set(("bucket", 1, "display"), _get("bucket", 0, "display")), "duplicate display name"),
    case("fallback-to-no-bucket", _set(("fallback", "bucket"), "nowhere"), "routing must always land"),
    # The blanket genre rule: a guessed genre on a file outlives the run.
    case("tagging-uses-fallback", _set(("fallback", "tagging_uses_fallback"), True), "allowed to decline"),
    # Overlapping bounds put one level in two bands.
    case("bands-not-increasing", _set(("energy", "bands", 1, "max"), _get("energy", "bands", 0, "max")), "does not increase"),
    case("bands-short-of-scale", _set(("energy", "bands", -1, "max"), 8), "scale_max"),
    case("band-label-for-undeclared-band", _override_an_undeclared_band, "not a declared band"),
    case("source-sub-outside-bucket", _route_by_source_outside_the_bucket, "not a declared sub"),
    case("source-string-routing-two-ways", _set(("bucket", 1, "aliases"), lambda d: [
        *d["bucket"][1]["aliases"], d["bucket"][0]["aliases"][0]]), "cannot route two ways"),
    case("fuzzy-rule-to-no-bucket", _set(("fuzzy", 0, "bucket"), "nowhere"), "is not declared"),
    # An uppercase keyword could never match, and reads as a rule that fires.
    case("uppercase-keyword", _set(("fuzzy", 0, "keyword"), lambda d: d["fuzzy"][0]["keyword"].upper()), "can never match"),
    case("suggest-rule-answers-and-declines", _set((lambda d: next(r for r in d["suggest"] if "bucket" in r), "decline"),
         "ask"), "exactly one of bucket, tag, decline"),
    # KTD14: the XML bridge's indentation encodes exactly three levels.
    case("tree-depth-not-three", _set(("tree", "depth"), 4), "KTD14"),
    case("bad-tempo-window", _set(("bucket", 0, "bpm"), {"start": 100, "floor": 120, "ceil": 140}), "floor < start < ceil"),
    # A former place (R-797) that is still a place.
    case("former-in-undeclared-bucket", _set((*_FORMER, "bucket"), "no_such_bucket"), "is not declared"),
    # Stops a mistyped line planning removals from a live sub.
    case("former-is-a-live-sub", _set((*_FORMER, "sub"), _get(_holder, "sub", 0, "id")), "still declares the sub"),
    case("former-named-for-live-sub", _set((*_FORMER, "display"), _get(_holder, "sub", 0, "display")),
         "still holds a sub named"),
    # A band is a live place of an energy bucket, under the bucket's label for it.
    case("former-named-for-a-band", _former_place_named_for_a_band, "still holds a sub named"),
    case("former-named-for-sub-class", _set((*_FORMER, "display"), _get("sub_class", 0, "display")), "still holds a sub named"),
    case("former-id-is-a-band", _set((*_FORMER, "id"), _get("energy", "bands", 0, "id")), "already a sub of this bucket"),
    case("former-twice-in-one-bucket", _set((_promoted, "formerly"), lambda d: [*_promoted(d)["formerly"], dict(_former(d))]),
         "duplicate former place id", "already the former place of"),
    case("one-playlist-former-place-of-two-buckets", _set((_another_bucket, "formerly"), _former_copy(id="another_id")),
         "already the former place of", absent=("duplicate former place id",)),
    # Both compete in the folder that holds them, under their identifiers.
    case("two-buckets-one-former-place-id",
         _set((_another_bucket, "formerly"), _former_copy(sub="another_sub", display="Another playlist")),
         "duplicate former place id", absent=("already the former place of",)),
    case("former-short-of-id", _set((*_FORMER, "id"), "Not An Id"), ("formerly", "must match")),
    case("former-short-of-sub", _set((*_FORMER, "sub"), ""), ("formerly", "must match")),
    case("former-short-of-display", _set((*_FORMER, "display"), ""), ("formerly", "display must be a non-empty string")),
    # An older build reads version 1, ignores the declaration and files a track
    # into its new place while it sits in the old one.
    case("former-under-schema-1", _set(("schema_version",), 1), "declares a former place under schema_version 1"),
    # One pair of brackets is valid TOML, and raised out of the loader as a defect.
    *[
        case(f"former-as-{name}", _set((_promoted, "formerly"), shape), "formerly must be an array of tables")
        for name, shape in (("one-table", _ONE_TABLE), ("list-of-strings", ["a bare name"]), ("string", "a bare name"))
    ],
    # It competes in the holder too, so the identifier has to be free there.
    case("former-id-is-holder-sub", _set((*_FORMER, "id"), _get(_holder, "sub", 0, "id")),
         "where a former place competes as well"),
    # A split place (U118) that is not a live band; stops a former place being
    # written as a split place.
    case("split-of-undeclared-band", _set((*_SPLIT, "sub"), "no_such_band"), "is not a band"),
    case("split-out-of-bucket-with-no-bands",
         _set((*_SPLIT, "bucket"), lambda d: next(b for b in d["bucket"] if b.get("sub_by_source"))["id"]), "is not a band"),
    case("split-renamed", _set((*_SPLIT, "display"), "Renamed by hand"), ("the name", "gives")),
    case("split-out-of-undeclared-bucket", _set((*_SPLIT, "bucket"), "no_such_bucket"), "not another declared bucket"),
    case("split-out-of-itself", _set((*_SPLIT, "bucket"), _get(_splitter, "id")), "not another declared bucket"),
    case("one-band-split-by-two-buckets", _one_band_split_by_two_buckets, "already split out by"),
    case("split-id-of-a-former-place", _set((*_SPLIT, "id"), _get(*_FORMER, "id")), "already a former or split place"),
    case("split-of-holders-former-place-renamed", _set((lambda d: next(
        r for r in _splitter(d)["split_from"] if r["sub"] not in _band_ids(d)), "display"), "Renamed by hand"), "gives"),
    # Only the holder's own former place is one the holder competes on.
    case("split-of-another-buckets-former", _split_another_buckets_former_place, "is not a band or a former place"),
    case("split-id-is-a-band", _set((*_SPLIT, "id"), _get("energy", "bands", 0, "id")), "already a sub of this bucket"),
    case("split-in-bucket-without-energy", _all(_set((_splitter, "energy"), {"enabled": False}),
         _set((_splitter, "single_sub"), {"id": "everything", "display": "Everything"})), "does not split by energy"),
    # An older build ignores the key and files the split genre into its new
    # folder while it sits in the old band.
    *[
        case(f"split-under-schema-{v}", _set(("schema_version",), v), f"declares a split place under schema_version {v}")
        for v in (1, 2)
    ],
    *[
        case(f"split-as-{name}", _set((_splitter, "split_from"), shape), "split_from must be an array of tables")
        for name, shape in (("one-table", _ONE_TABLE), ("string", "a bare name"))
    ],
    case("tagging-word-claimed-by-two-buckets", _tagging_word_in_two_buckets, "is claimed by both"),
    # A sub class derived from a playlist (U119).
    case("two-additive-classes-on-one-signal", _set(("sub_class",), lambda d: [*d["sub_class"], {
        "id": "second_vox", "display": "Second", "policy": "derived", "additive": True}]),
         ("'vox' signal", "only one is supported per signal")),
    case("playlist-signal-without-playlist", _set(("sub_class", 2, "signal_playlist"), ""), "signal_playlist"),
    case("playlist-signal-manual", _all(_set(("sub_class", 2, "policy"), "manual"), _set(("sub_class", 2, "additive"), False)),
         "derived and additive"),
    case("playlist-name-on-vocal-class", _set(("sub_class", 1, "signal_playlist"), "All Favorites"),
         "only meaningful for a playlist signal"),
    case("unknown-signal", _set(("sub_class", 2, "signal"), "colour"), "signal 'colour'"),
    case("playlist-signal-under-schema-3", _set(("schema_version",), 3), "schema_version = 4"),
]


@pytest.mark.parametrize(("mutate", "needles", "absent"), REFUSED)
def test_a_template_breaking_a_rule_is_refused_by_name(default_raw, mutate, needles, absent):
    problems = problems_from(default_raw, mutate)
    for needle in needles:
        parts = (needle,) if isinstance(needle, str) else needle
        assert any(all(part in p for part in parts) for p in problems), (needle, problems)
    for text in absent:
        assert not any(text in p for p in problems), (text, problems)


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


# Parameterisation: a second taxonomy, sharing nothing.


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


def _band(bucket, level):
    return lambda t: routing.energy_sub(t, bucket, level).display


def _by_source(level, genre):
    return lambda t: routing.energy_sub(t, "field_recordings", level, source_genre=genre).id


def _prior(t):
    prior = routing.bpm_prior(t, "Banger")
    return (prior.start, prior.floor, prior.ceil)


def _unknown_tempo(t):
    unknown = routing.suggest_tag(t, "slow one")
    return (unknown.bucket_id, unknown.needs_review is True)


# The whole parameterisation claim: the second template answers by its own
# declaration, one case per tier, band, curve and vocabulary it declares.
CUSTOM = [
    ("routes-exactly", lambda t: routing.resolve_bucket(t, "Banger").bucket_id, "floor_filler"),
    ("routes-by-display", lambda t: routing.resolve_bucket(t, "Slow Burn").bucket_id, "slow_burn"),
    ("routes-by-keyword", lambda t: routing.resolve_bucket(t, "a proper banger").bucket_id, "floor_filler"),
    ("routes-to-its-fallback", lambda t: routing.resolve_bucket(t, "no idea").bucket_id, "unfiled"),
    # Four bands, four different cuts, and none of the default's names.
    *[(f"band-{lv}-{name}", _band("floor_filler", lv), name) for lv, name in
      ((1, "Warm Up"), (3, "Groove"), (6, "Peak"), (9, "Afters"))],
    # Same cuts, different labels, and only the overridden ones move.
    *[(f"label-override-{lv}", _band("slow_burn", lv), name) for lv, name in
      ((1, "Barely Moving"), (4, "Groove"), (10, "Last Call"))],
    *[(f"no-energy-split-{lv}", _band("spoken", lv), "Spoken Word") for lv in (None, 1, 5, 10)],
    ("no-energy-split-has-no-no-energy-sub", lambda t: routing.no_energy_sub(t, "spoken"), None),
    ("no-energy-split-does-not-rate", lambda t: routing.rates(t, "spoken"), False),
    ("by-source-wildlife", _by_source(5, "Wildlife"), "birds"),
    ("by-source-without-energy", _by_source(None, "Weather"), "water"),
    # Unmapped falls to the DECLARED default rather than to whichever sub is first.
    ("by-source-unmapped-to-declared-default", _by_source(5, "Ghosts"), "engines"),
    *[(f"rating-{lv}", lambda t, lv=lv: routing.energy_rating(t, lv), r) for lv, r in
      ((3, 51), (6, 153), (10, 255), (None, None))],
    ("tempo-window", _prior, (128, 120, 140)),
    ("declines-its-own-word", lambda t: routing.suggest_tag(t, "Misc").declined, True),
    ("declines-empty-as-not-found", lambda t: routing.suggest_tag(t, "").decline, routing.Decline.NOT_FOUND),
    ("tags-by-its-vocabulary", lambda t: routing.suggest_tag(t, "Banger").tag, "Floor Filler"),
    ("tempo-split-slow", lambda t: routing.suggest_tag(t, "slow one", bpm=80.0).bucket_id, "spoken"),
    ("tempo-split-fast", lambda t: routing.suggest_tag(t, "slow one", bpm=110.0).bucket_id, "slow_burn"),
    ("tempo-split-unknown-needs-review", _unknown_tempo, ("slow_burn", True)),
]


@pytest.mark.parametrize(("ask", "answer"), [pytest.param(a, b, id=i) for i, a, b in CUSTOM])
def test_a_custom_taxonomy_answers_by_its_own_declaration(second, ask, answer):
    got = ask(second)
    assert got is answer if answer is None or isinstance(answer, (bool, enum.Enum)) else got == answer


def test_a_buckets_own_display_name_is_never_reported_off_taxonomy(default, second):
    """R-650: a bucket's own name passes the last tier as itself and routing places it: unreported.

    Both templates; the second loop shows the check is not vacuous.
    """
    for declared in (default, second):
        displays = [bucket.display for bucket in declared.buckets]
        assert displays
        assert [d for d in displays if routing.suggest_tag(declared, d).off_taxonomy] == []

    # Claimed by no alias, and back out of the resolver as itself with no bucket.
    for declared, display in ((default, "NonElectronic"), (second, "Floor Filler")):
        assert declared.bucket_for_display(display) is not None
        assert declared.tagging_alias(display.lower()) is None
        answer = routing.suggest_tag(declared, display)
        assert (answer.tag, answer.bucket_id, answer.declined) == (display, None, False)


def test_a_sub_display_and_a_changed_case_are_both_reported(default, second):
    """The suppression is routing's: a sub's display and a recased bucket both report (R-650)."""
    for display in ("Birds", "Water", "Engines"):
        assert routing.suggest_tag(second, display).off_taxonomy is True
        assert routing.resolve_bucket(second, display).bucket_id == second.fallback.bucket

    lowered = "nonelectronic"
    assert default.bucket_for_display("NonElectronic") is not None
    assert routing.suggest_tag(default, lowered).off_taxonomy is True
    assert routing.resolve_bucket(default, lowered).bucket_id == default.fallback.bucket


def test_an_off_taxonomy_word_can_still_route_to_a_real_bucket(default):
    """The flag is about the word: a word nothing tags can still route by a fuzzy rule."""
    for value in ("Psy-Trance", "Hardcore / Hard Techno"):
        assert routing.suggest_tag(default, value).off_taxonomy is True
        landing = routing.resolve_bucket(default, value)
        assert landing.bucket_id != default.fallback.bucket, value
        assert landing.match is routing.Match.FUZZY


def test_two_taxonomies_coexist_in_one_process(default, second):
    """Why nothing here reads configuration (seam decision S3)."""
    assert routing.resolve_bucket(default, "Banger").bucket_id == default.fallback.bucket
    assert routing.resolve_bucket(second, "Banger").bucket_id == "floor_filler"


def test_a_template_with_no_energy_dimension_routes_and_does_not_error():
    """R19: a taxonomy may not use energy; the track lands with no sub below it."""
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


# R19: a rename must not orphan state.


def _renamed(default_raw):
    before = build_taxonomy(default_raw)
    after = build_taxonomy(
        mutated(default_raw, lambda d: d["bucket"][0].__setitem__("display", "Renamed By Hand"))
    )
    return before, after


def test_renaming_a_display_name_preserves_state_keyed_to_its_identifier(default_raw):
    """The reason ids exist: a renamed folder once orphaned every record keyed on it."""
    before, after = _renamed(default_raw)
    target = before.buckets[0]
    state = {bucket.id: {"swept": index} for index, bucket in enumerate(before.buckets)}
    renamed = after.bucket(target.id)

    assert renamed.display == "Renamed By Hand"
    assert renamed.display != target.display
    assert renamed.id == target.id
    assert state[renamed.id] == {"swept": 0}
    # Routing follows the new name, read off the declaration.
    assert routing.resolve_bucket(after, "Renamed By Hand").bucket_id == target.id


def test_a_renamed_bucket_keeps_its_aliases_and_its_tempo_window(default_raw):
    """A rename is cosmetic. Anything it changes besides the name is a bug."""
    before, after = _renamed(default_raw)
    original, renamed = before.buckets[0], after.buckets[0]
    assert renamed.aliases == original.aliases
    assert renamed.bpm == original.bpm
    assert renamed.family == original.family


# Former places (R-797) and split places (U118) that load.


def test_the_shipped_template_declares_three_former_places_and_they_load(default, default_raw):
    """R&B's since R-797, Hip-Hop's since U118 and Jazz's since U133, each read as written."""
    declared = [(bucket.id, place) for bucket in default.buckets for place in bucket.formerly]
    raw = [
        (bucket["id"], row) for bucket in default_raw["bucket"] for row in bucket.get("formerly", [])
    ]
    assert len(declared) == len(raw) == 3
    for (bucket_id, former), (raw_id, row) in zip(declared, raw):
        assert (bucket_id, former.id, former.bucket, former.sub, former.display) == (
            raw_id, row["id"], row["bucket"], row["sub"], row["display"]
        )


def test_a_band_name_is_no_live_place_in_a_bucket_that_does_not_split_by_energy(default_raw):
    """The check asks what THAT bucket holds."""

    def mutate(data):
        former = _promoted(data)["formerly"][0]
        former["display"] = data["energy"]["bands"][0]["display"]
        # The split place naming it carries the name it is given (U118).
        for row in _splitter(data)["split_from"]:
            if row["sub"] == former["id"]:
                row["display"] = former["display"]

    assert build_taxonomy(mutated(default_raw, mutate)).buckets


def test_a_template_with_no_former_place_loads_as_it_always_did(default_raw):
    def mutate(data):
        formerly = {row["id"] for bucket in data["bucket"] for row in bucket.get("formerly", [])}
        for bucket in data["bucket"]:
            bucket.pop("formerly", None)
        # A split place naming a former place goes with it (U118).
        splitter = _splitter(data)
        splitter["split_from"] = [row for row in splitter["split_from"] if row["sub"] not in formerly]

    loaded = build_taxonomy(mutated(default_raw, mutate))
    assert all(bucket.formerly == () for bucket in loaded.buckets)


def test_a_version_1_template_with_no_former_place_still_loads(default_raw, second):
    def mutate(data):
        data["schema_version"] = 1
        for bucket in data["bucket"]:
            bucket.pop("formerly", None)
            bucket.pop("split_from", None)
            # And the genre sub, which needs version 5 (U155).
            bucket.pop("genre_sub", None)
        data["sub_class"] = [c for c in data["sub_class"] if c.get("signal") != "playlist"]

    assert build_taxonomy(mutated(default_raw, mutate)).schema_version == 1
    assert second.schema_version == 1


def test_the_shipped_template_splits_one_bucket_out_of_every_place_of_another(default, default_raw):
    """Soul out of R&B: every band, the no reading sub and R&B's former place."""
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


def test_a_split_place_of_a_band_under_its_own_label_is_checked_against_that_label(default_raw):
    """A holder that labels its bands differently is asked for its label."""

    def mutate(data):
        holder = _band_label_holder(data)
        band, label = next(iter(holder["energy"]["band_display"].items()))
        splitter = _splitter(data)
        splitter["split_from"] = [row for row in splitter["split_from"] if row["sub"] in _band_ids(data)]
        splitter["split_from"][0].update(bucket=holder["id"], sub=band, display=label)
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


def test_a_version_2_template_with_no_split_place_still_loads(default_raw):
    def mutate(data):
        data["schema_version"] = 2
        del _splitter(data)["split_from"]
        data["sub_class"] = [c for c in data["sub_class"] if c.get("signal") != "playlist"]
        for bucket in data["bucket"]:
            bucket.pop("genre_sub", None)

    assert build_taxonomy(mutated(default_raw, mutate)).schema_version == 2


def test_a_tagging_only_word_wins_over_another_buckets_routing_alias(default):
    """"Trap / Wave" tags as Hip-Hop: a tagging-only word is the more specific statement."""
    routed = default.routing_alias("Trap / Wave")
    tagged = default.tagging_alias("trap / wave")
    assert routed is not None and tagged is not None
    assert tagged == (next(b.id for b in default.buckets if b.display == "Hip-Hop"), None)
    assert routed != tagged[0]


# U119: a sub class derived from a playlist, beside the vocal one.


def test_the_shipped_default_declares_the_genre_favorites_as_a_playlist_signal(default):
    """U119: one Favorites playlist in every genre folder, mirroring All Favorites."""
    favorites = default.sub_class("favorites")
    assert favorites.policy is SubPolicy.DERIVED and favorites.additive is True
    assert favorites.present_in == "all_buckets"
    assert favorites.signal == "playlist"
    assert favorites.signal_playlist == "All Favorites"
    assert default.schema_version >= 4
    vox = default.sub_class("with_vox")
    assert vox.signal == "vox" and vox.signal_playlist == ""


def test_two_additive_classes_load_when_their_signals_differ(default):
    additive = [entry for entry in default.sub_classes if entry.additive]
    assert sorted(entry.signal for entry in additive) == ["playlist", "vox"]


def test_a_template_without_the_favorites_class_loads_clean(default_raw):
    data = mutated(default_raw, lambda d: d["sub_class"].pop(2))
    built = build_taxonomy(data)
    assert [entry.id for entry in built.sub_classes if entry.additive] == ["with_vox"]


# One parse per text in a process (U247). Every count is of a text the test made
# unique, since the memo outlives the test.


def _shipped_text() -> str:
    return shipped_template_text(DEFAULT_TEMPLATE_NAME)


def test_the_same_text_is_parsed_once_and_answers_what_a_fresh_parse_builds(monkeypatch):
    text = unique(_shipped_text())
    parses = counted(monkeypatch)

    answers = [load_taxonomy(text) for _ in range(3)]

    assert parses.of(text) == 1, "the same text was parsed again"
    fresh = build_taxonomy(tomllib.loads(text))
    assert all(answer == fresh for answer in answers)
    assert answers[0] is answers[1] is answers[2]


def test_two_texts_are_each_parsed_once_and_each_answers_its_own(monkeypatch):
    """The two templates of one process, interleaved, as doctor and the upgrade ask."""
    first = unique(_shipped_text())
    second = unique(SECOND_TEMPLATE.read_text(encoding="utf-8"))
    parses = counted(monkeypatch)

    answers = [load_taxonomy(text) for text in (first, second, first, second)]

    assert (parses.of(first), parses.of(second)) == (1, 1)
    assert answers[0] == answers[2] == build_taxonomy(tomllib.loads(first))
    assert answers[1] == answers[3] == build_taxonomy(tomllib.loads(second))
    assert answers[0] != answers[1]
    assert routing.resolve_bucket(answers[3], "Banger").bucket_id == "floor_filler"


def test_an_edit_that_keeps_the_length_is_a_different_text_and_is_parsed_again(monkeypatch):
    """The key is the whole text: an edit a size could not see still counts."""
    before = unique(_shipped_text())
    display = load_taxonomy(_shipped_text()).buckets[0].display
    after, renamed = renamed_in_place(before, display)
    parses = counted(monkeypatch)

    assert load_taxonomy(before).buckets[0].display == display
    assert load_taxonomy(after).buckets[0].display == renamed
    assert load_taxonomy(before).buckets[0].display == display
    assert (parses.of(before), parses.of(after)) == (1, 1)


@pytest.mark.parametrize(
    "text, problem",
    [("this is not = = toml", "not valid TOML"), ("schema_version = 1\n", None)],
    ids=["not-toml", "not-a-taxonomy"],
)
def test_a_text_that_does_not_load_raises_on_every_call(monkeypatch, text, problem):
    """A refusal is never remembered as an answer, and is never remembered at all."""
    text = unique(text)
    parses = counted(monkeypatch)

    for _ in range(3):
        with pytest.raises(TaxonomyError) as caught:
            load_taxonomy(text)
        if problem is not None:
            assert problem in caught.value.problems[0]

    assert parses.of(text) == 3


def test_the_three_texts_an_upgrade_reads_are_each_parsed_once(monkeypatch):
    """The active copy, the template and the upgrade each parse once across rounds."""
    texts = [unique(_shipped_text()) for _ in range(3)]
    parses = counted(monkeypatch)

    for _ in range(3):
        for text in texts:
            load_taxonomy(text)

    assert [parses.of(text) for text in texts] == [1, 1, 1]


def test_the_memo_holds_eight_texts_and_parses_the_first_again_after_a_ninth(monkeypatch):
    """Bounded to a handful; the nine is written here, so a bound raised to all texts fails."""
    texts = [unique(_shipped_text()) for _ in range(9)]
    parses = counted(monkeypatch)

    for text in texts:
        load_taxonomy(text)
    load_taxonomy(texts[-1])
    load_taxonomy(texts[0])

    assert parses.of(texts[-1]) == 1, "the text asked last was not kept"
    assert parses.of(texts[0]) == 2, "the memo kept more texts than its bound"
