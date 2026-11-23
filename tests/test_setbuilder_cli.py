"""U43: ``crate setbuild``, the shell over the set building engine.

The pure half drives ``plan_for`` over a frozen index, the disk half a small
tagged library. Fixture tempos live in the title tag, never a tempo tag (R17).
"""

from __future__ import annotations

import dataclasses
import io
import json
import shutil
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output, registry
from cratekit.core import config, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import setbuilder
from cratekit.setbuilder import cli as setbuild_cli
from tests._containers import synth_container
from tests._sync_builders import exited

TAXONOMY = taxonomy.default_taxonomy()

#: The genre every fixture track carries, so genre affinity is constant and the
#: harmonic and tempo signals are what move the ordering.
GENRE = "Deep House"


# ── the pure half: plan_for over a frozen index ──────────────────────────────


def track(artist, title, key, bpm=124.0, energy=5, vox=None, path=""):
    return setbuilder.Track(
        artist=artist, title=title, key=setbuilder.canonical_key(key), bpm=bpm, genre=GENRE,
        energy=energy, vox=vox, voxgender=None, match=setbuilder.match_key(artist, title),
        path=path or f"/library/{artist}-{title}.flac",
    )


def plan_of(anchor, index, **kwargs):
    return setbuild_cli.plan_for(anchor, index, declared=TAXONOMY, **kwargs)


@pytest.fixture
def index():
    """A frozen index. Every track is owned by construction, which is the point."""
    return (
        track("Alder", "Anchor Work", "8A", 124.0, energy=6),
        track("Birch", "Same Key Lower", "8A", 124.0, energy=4),
        track("Cedar", "Neighbour Up", "9A", 125.0, energy=8),
        track("Deodar", "Relative Major", "8B", 123.0, energy=6),
        track("Elm", "Energy Boost", "10A", 124.0, energy=9),
        track("Fir", "Diagonal", "9B", 124.0, energy=3),
        track("Gum", "Wrong Key", "3B", 124.0, energy=5),
        track("Hazel", "Right Key Wrong Tempo", "8A", 100.0, energy=5),
    )


def anchor_of(index):
    return index[0]


def test_plan_for_composes_the_engine_exactly_as_build_set_does(index):
    """THE DRIFT PIN, and the reason this shell may reimplement four lines."""
    anchor = anchor_of(index)
    mine = plan_of(anchor, index)
    theirs = setbuilder.build_set(anchor.display, index, taxonomy=TAXONOMY)

    assert theirs.anchor.owned and theirs.anchor.track is anchor, "the anchor moved"
    assert [item["path"] for item in mine["items"] if item["position"] is not None] == [
        scored.track.path for scored in theirs.sequence
    ]
    assert {item["path"] for item in mine["items"]} == {
        scored.track.path for scored in theirs.pool
    } | {scored.track.path for scored in theirs.sequence}
    assert mine["totals"]["sequence"] == len(theirs.sequence)


def test_the_sequence_leads_the_items_and_carries_its_own_order(index):
    plan = plan_of(anchor_of(index), index)
    positions = [item["position"] for item in plan["items"]]
    placed = [p for p in positions if p is not None]

    assert placed, "the fixture produced no sequence, so ordering is untested"
    assert placed == list(range(1, len(placed) + 1)), "the sequence must lead, in order"
    assert positions[: len(placed)] == placed, "a pool-only item interrupts the sequence"
    assert all(p is None for p in positions[len(placed):])
    assert plan["totals"]["sequence"] == len(placed)


def test_every_recommendation_came_out_of_the_index(index):
    """The grounding rule, asserted at the shell's own output boundary."""
    plan = plan_of(anchor_of(index), index)
    owned = {t.path for t in index}
    assert plan["items"], "no items, so this guard measured nothing"
    for item in plan["items"]:
        assert item["path"] in owned
    assert all(item["path"] != anchor_of(index).path for item in plan["items"])


def test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical(index):
    """Two plans over the same companions and different anchors are two plans."""
    original = anchor_of(index)
    renamed = track("Alder", "Anchor Work (Alternate Master)", "8A", energy=original.energy)
    first = plan_of(original, index)
    second = plan_of(renamed, (renamed, *index[1:]))

    assert first["items"] == second["items"], "the rename moved a ranking signal"
    assert first["digest"] != second["digest"]


def test_two_plans_over_the_same_anchor_and_different_companions_digest_apart(index):
    """The other half of the digest, and it was a zero row."""
    anchor = anchor_of(index)
    full = plan_of(anchor, index)
    narrowed = plan_of(anchor, index[:3])

    assert full["items"] != narrowed["items"], "the two indexes gave the same items"
    assert full["totals"]["anchor"] == narrowed["totals"]["anchor"], "the anchor moved too"
    assert full["digest"] != narrowed["digest"]
    # And the same anchor over the same index, in any order, always digests the same.
    assert plan_of(anchor, tuple(reversed(index)))["digest"] == full["digest"]


def test_an_unowned_anchor_in_8a_ranks_the_library_against_it(index):
    """U98's scenario: companions for a track the index does not hold."""
    anchor = setbuild_cli.unowned_anchor("Oak - Not Bought Yet", "8A", None)
    plan = plan_of(anchor, index)

    rendered = plan["totals"]["anchor"]
    assert (rendered["owned"], rendered["key_needs_confirming"]) == (False, True)
    assert (rendered["key"], rendered["display"]) == ("8A", "Oak - Not Bought Yet")
    assert plan["items"], "an unowned 8A anchor found no companions in the fixture"
    tiers = setbuilder.compatible_keys("8A")
    assert all(item["key"] in tiers for item in plan["items"])
    assert "Wrong Key" not in {item["title"] for item in plan["items"]}


def test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it(index):
    """The empty index is the guarantee, so drive a label that WOULD fuzzy match."""
    extended = track("Alder", "Anchor Work (Extended Mix)", "9A", 124.0)
    library = (extended, *index[1:])
    label = "Alder - Anchor Work"
    assert setbuilder.resolve_anchor(label, library, key="9A").track is extended
    anchor = setbuild_cli.unowned_anchor(label, "9A", None)
    plan = plan_of(anchor, library)

    assert anchor.owned is False and anchor.track is None
    assert plan["totals"]["anchor"]["key"] == "9A"
    assert extended.path in {item["path"] for item in plan["items"]}
    assert plan["totals"]["held"] == []


def test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked(index):
    """The review's finding, driven: the library's copy as its own companion."""
    owned = anchor_of(index)
    plan = plan_of(setbuild_cli.unowned_anchor(owned.display, "8A", 124.0), index)

    assert owned.path not in {item["path"] for item in plan["items"]}
    assert plan["totals"]["held"] == [owned.path]
    assert plan["items"], "nothing else was ranked, so the exclusion measured nothing"


def test_an_unowned_sequence_places_each_companion_once(index):
    """An unowned anchor's companions are mostly ``either``, once picked for BOTH sides."""
    same_number = tuple(t for t in index if t.key in ("8A", "8B"))
    plan = plan_of(setbuild_cli.unowned_anchor("Oak", "8A", 124.0), same_number)
    assert {item["role"] for item in plan["items"]} == {"either"}
    assert len(plan["items"]) > setbuilder.DEFAULT_SIDE, "too few companions for both sides"
    placed = [item["position"] for item in plan["items"] if item["position"] is not None]
    paths = [item["path"] for item in plan["items"]]

    assert placed == list(range(1, len(placed) + 1))
    assert len(paths) == len(set(paths)), "a companion appears twice in the items"
    assert plan["totals"]["sequence"] == len(placed)


def test_an_unowned_anchor_with_no_key_or_no_label_refuses():
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.unowned_anchor("Oak - Not Bought Yet", None, None)
    assert caught.value.cause.reason == "setbuild-unowned-key-missing"
    assert caught.value.cause.remediation.steps
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.unowned_anchor("", "8A", None)
    assert caught.value.cause.reason == "setbuild-anchor-unknown"


@pytest.mark.parametrize(
    ("parse", "text"),
    [(setbuild_cli.camelot_key, t) for t in ("13C", "13A", "0A", "8C", "", "eight")]
    + [(setbuild_cli.positive_tempo, t) for t in ("0", "-124", "nan", "inf", "-inf")]
    + [(setbuild_cli.positive_count, t) for t in ("0", "-1", "-8")],
)
def test_a_value_the_flag_cannot_take_is_refused_at_the_parser(parse, text):
    """A key off the wheel, a tempo that would empty the pool, a count below one."""
    with pytest.raises(ValueError):
        parse(text)


def test_the_parsers_canonicalize_and_accept_the_smallest_values():
    assert setbuild_cli.camelot_key("08A") == "8A"
    assert setbuild_cli.camelot_key("12b") == "12B"
    assert setbuild_cli.positive_count("1") == 1


def test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band(index):
    """``--bpm`` is a ranking input: with it, the tempo band applies."""
    keyless = plan_of(setbuild_cli.unowned_anchor("Oak", "8A", None), index)
    banded = plan_of(setbuild_cli.unowned_anchor("Oak", "8A", 124.0), index)
    assert "Right Key Wrong Tempo" in {item["title"] for item in keyless["items"]}
    assert "Right Key Wrong Tempo" not in {item["title"] for item in banded["items"]}
    assert banded["totals"]["anchor"]["tempo"] == 124.0


def test_one_either_companion_of_an_owned_anchor_is_placed_once():
    """The same defect on main, through the owned form and through ``build_set``."""
    anchor = track("Alder", "Anchor Work", "8A", 124.0, energy=5)
    other = track("Birch", "Other", "8A", 124.0, energy=5)
    plan = plan_of(anchor, (anchor, other))
    engine = setbuilder.build_set(anchor.display, (anchor, other), taxonomy=TAXONOMY)

    assert [item["position"] for item in plan["items"]] == [1]
    assert [scored.track.path for scored in engine.sequence] == [other.path]


def test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart(index):
    """Ownership is part of the question, so it is part of the identity."""
    owned = dataclasses.replace(track("Oak", "Not Bought Yet", "8A"), genre=None, energy=None)
    first = plan_of(owned, index)
    second = plan_of(setbuild_cli.unowned_anchor(owned.display, "8A", 124.0), index)

    assert first["items"] == second["items"], "the two anchors ranked differently"
    assert first["items"], "no companions, so the comparison is between two empty plans"
    assert first["digest"] != second["digest"]


def test_a_role_narrows_the_answer_to_one_side(index):
    plan = plan_of(anchor_of(index), index, role="before")
    assert plan["items"], "the fixture produced nothing for one side"
    assert all(item["role"] in ("before", "either") for item in plan["items"])


@pytest.fixture
def wide_index():
    """An index with more compatible companions than any default returns."""
    keys = ("8A", "8B", "7A", "9A")
    companions = (
        track(f"Tree{n:02d}", f"Companion {n:02d}", keys[n % len(keys)], energy=n)
        for n in range(1, 11)
    )
    return (track("Alder", "Anchor Work", "8A", energy=6), *companions)


def test_a_count_caps_the_companions(wide_index):
    """The cap reaches the engine, and its effect is reported rather than implied."""
    capped = plan_of(anchor_of(wide_index), wide_index, count=2)
    uncapped = plan_of(anchor_of(wide_index), wide_index)

    assert uncapped["totals"]["pool"] > capped["totals"]["pool"], "the cap is not observable"
    assert capped["totals"]["pool"] == 2
    assert uncapped["totals"]["pool"] == setbuilder.DEFAULT_POOL
    assert len(capped["items"]) < len(uncapped["items"])
    assert capped["totals"]["count"] == len(capped["items"])


def test_the_payload_validates_against_the_declared_plan_surface(index):
    """``plan/1`` is closed, so a fifth key here is a defect rather than an extra."""
    plan = plan_of(anchor_of(index), index)
    assert output.payload_problems("plan", plan) == []
    assert plan["totals"]["anchor"]["display"] == anchor_of(index).display


def test_the_vocal_signal_is_reachable_only_because_a_threshold_can_be_supplied():
    """The fifth ranking signal, which is dead weight without the flag."""
    anchor = track("Alder", "Anchor Work", "8A", 124.0, energy=5, vox=90)
    loud = track("Birch", "Also Vocal", "8A", 124.0, energy=5, vox=90)
    quiet = track("Cedar", "Instrumental", "8A", 124.0, energy=5, vox=5)
    index = (anchor, loud, quiet)

    neutral = plan_of(anchor, index)
    thresholded = plan_of(anchor, index, vox_threshold=50.0)

    def paths(plan):
        return [item["path"] for item in plan["items"]]

    assert paths(neutral) != paths(thresholded), "the threshold changed no ordering"
    assert paths(thresholded)[0] == quiet.path, "two lead vocals were stacked"


# ── the anchor lookup, which is the whole reason the positional is a path ─────


def test_an_exact_name_is_never_lost_to_a_longer_title_whichever_came_first():
    """R-187, DRIVEN ON THE SHAPE ITS ENTRY DROVE."""
    extended = track("Alder", "Anchor Work (Extended Mix)", "8A", path="/library/ext.flac")
    original = track("Alder", "Anchor Work", "8A", path="/library/orig.flac")

    for index in ((extended, original), (original, extended)):
        assert setbuilder.find_in_index("Alder - Anchor Work", index) is original
        assert setbuild_cli.named_anchor("Alder - Anchor Work", index) is original
        assert setbuild_cli.named_anchor("Alder - Anchor Work (Extended Mix)", index) is extended
    assert setbuild_cli.anchor_in_index(Path("/library/orig.flac"), (extended, original)) is original


def test_a_name_that_reaches_two_versions_lists_both_and_picks_neither():
    """The refusal IS the feature, so its contents are asserted and not its slug alone."""
    extended = track("Alder", "Anchor Work (Extended Mix)", "8A", path="/library/ext.flac")
    original = track("Alder", "Anchor Work", "8A", path="/library/orig.flac")
    other = track("Gum", "Wrong Key", "3B", path="/library/gum.flac")

    listings = []
    for index in ((extended, original, other), (other, original, extended)):
        with pytest.raises(CratekitError) as caught:
            setbuild_cli.named_anchor("Anchor Work", index)
        cause = caught.value.cause
        assert cause.reason == "setbuild-anchor-ambiguous"
        assert cause.detail["reached"] == 2
        listings.append(cause.detail["candidates"])
        steps = " ".join(cause.remediation.steps)
        assert "/library/orig.flac" in steps and "/library/ext.flac" in steps
        assert "/library/gum.flac" not in steps

    assert listings[0] == listings[1], "the listing follows the walk order"
    assert listings[0] == [
        {"display": "Alder - Anchor Work", "path": "/library/orig.flac"},
        {"display": "Alder - Anchor Work (Extended Mix)", "path": "/library/ext.flac"},
    ]


def test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened():
    """The subset score is 100 in BOTH directions, and this is the other one."""
    original = track("Alder", "Anchor Work", "8A", path="/library/orig.flac")
    index = (original, track("Gum", "Wrong Key", "3B"))

    assert setbuilder.match_in_index("Alder - Anchor Work (Extended Mix)", index) == (
        setbuilder.AnchorMatch(candidates=(original,), partial=True)
    )
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.named_anchor("Alder - Anchor Work (Extended Mix)", index)
    cause = caught.value.cause
    assert cause.reason == "setbuild-anchor-ambiguous"
    assert cause.detail["reached"] == 1 and cause.detail["partial"] is True
    assert cause.detail["candidates"] == [
        {"display": "Alder - Anchor Work", "path": "/library/orig.flac"}
    ]
    assert "different version" in cause.message
    assert "--unowned" in cause.remediation.steps[-1]


def test_one_differing_word_in_a_long_title_is_a_different_version():
    """Found by the built in review, and the set score CANNOT see it."""
    owned = track("Some Long Artist Name", "A Very Long Track Title Indeed (Original Mix)", "8A")
    named = "Some Long Artist Name - A Very Long Track Title Indeed (Extended Mix)"
    from rapidfuzz import fuzz

    assert fuzz.token_set_ratio(
        setbuilder.match_key("", named), owned.match
    ) >= setbuilder.MATCH_THRESHOLD, "the pair no longer scores as a match"
    assert setbuilder.match_in_index(named, (owned,)) == setbuilder.AnchorMatch(
        candidates=(owned,), partial=True
    )
    dub = track("Alder", "A Rather Long Anchor Work Title (Dub Mix)", "8A")
    matched = setbuilder.match_in_index("Alder - A Rather Long Anchor Work Title (Club Mix)", (dub,))
    assert matched.track is None


def test_the_one_title_holding_every_typed_word_wins_over_titles_holding_fewer():
    """Both titles score 100 on "anchor work", and only one holds "extended"."""
    extended = track("Alder", "Anchor Work (Extended Mix)", "8A", path="/library/ext.flac")
    original = track("Alder", "Anchor Work", "8A", path="/library/orig.flac")
    for index in ((extended, original), (original, extended)):
        assert setbuild_cli.named_anchor("anchor work extended", index) is extended


def test_a_file_with_no_artist_tag_is_reachable_by_the_name_the_refusal_lists():
    """Found by the built in review: the remedy has to be one that works."""
    bare = track("", "Anchor Work", "8A", path="/library/bare.flac")
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.named_anchor("Alder - Anchor Work", (bare,))
    listed = caught.value.cause.detail["candidates"][0]["display"]
    assert listed in caught.value.cause.remediation.steps[1]
    assert setbuild_cli.named_anchor(listed, (bare,)) is bare


def test_a_name_typed_short_resolves_when_only_one_track_answers_to_it(index):
    """What fuzzy is FOR: a person types what they remember, which is less."""
    extended = track("Alder", "Anchor Work (Extended Mix)", "8A", path="/library/ext.flac")
    library = (extended, *index[1:])
    assert setbuild_cli.named_anchor("anchor work", library) is extended
    assert setbuild_cli.named_anchor("Alder - Anchr Work Extended Mix", library) is extended


def test_a_name_nothing_answers_to_is_not_indexed_and_not_ambiguous(index):
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.named_anchor("Nobody - Absent", index)
    assert caught.value.cause.reason == "setbuild-anchor-not-indexed"
    assert caught.value.cause.detail == {"named": "Nobody - Absent", "indexed": len(index)}


@pytest.mark.parametrize("text", ["", "   ", " - "])
def test_a_name_with_nothing_in_it_is_an_unknown_anchor(text, index):
    """" - " is punctuation only, so its comparison key is empty too."""
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.named_anchor(text, index)
    assert caught.value.cause.reason == "setbuild-anchor-unknown"


def test_two_indexed_tracks_under_one_comparison_key_are_listed_and_not_chosen():
    """``build_index`` collapses these, and a hand built index need not have."""
    flac = track("Alder", "Anchor Work", "8A", path="/library/b.flac")
    mp3 = track("Alder", "Anchor Work", "8A", path="/library/a.mp3")
    matched = setbuilder.match_in_index("Alder - Anchor Work", (flac, mp3))
    assert matched == setbuilder.AnchorMatch(candidates=(mp3, flac))


def test_the_listing_is_capped_and_says_how_many_it_reached():
    many = tuple(
        track("Alder", f"Work Part {n:02d}", "8A", path=f"/library/{n:02d}.flac")
        for n in range(setbuilder.CANDIDATE_LIMIT + 3)
    )
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.named_anchor("Alder Work Part", many)
    detail = caught.value.cause.detail
    assert detail["reached"] == setbuilder.CANDIDATE_LIMIT + 3
    assert len(detail["candidates"]) == setbuilder.CANDIDATE_LIMIT


def test_the_engine_says_ambiguous_and_never_not_in_your_library():
    """The same shape one file over: ``resolve_anchor`` and ``build_set``."""
    extended = track("Alder", "Anchor Work (Extended Mix)", "8A", path="/library/ext.flac")
    original = track("Alder", "Anchor Work", "8A", path="/library/orig.flac")
    index = (extended, original)

    for supplied in (None, "8A"):
        anchor = setbuilder.resolve_anchor("Anchor Work", index, key=supplied)
        assert anchor.key is None and anchor.owned is False and anchor.track is None
        assert "names 2 owned tracks" in anchor.unresolved
        assert "Alder - Anchor Work (Extended Mix)" in anchor.unresolved
        assert "not in your library" not in anchor.unresolved
    plan = setbuilder.build_set("Anchor Work", index, taxonomy=TAXONOMY, key="8A")
    assert plan.pool == () and plan.sequence == ()


def test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied():
    """Found by the built in review."""
    original = track("Alder", "Anchor Work", "8A", path="/library/orig.flac")
    index = (original, track("Birch", "Same Key Lower", "8A"))
    remix = "Alder - Anchor Work (Someone Remix)"

    bare = setbuilder.resolve_anchor(remix, index)
    assert bare.key is None and "may be a version you do not own" in bare.unresolved
    assert "owned tracks" not in bare.unresolved

    keyed = setbuilder.resolve_anchor(remix, index, key="8A")
    assert (keyed.key, keyed.owned, keyed.track, keyed.display) == ("8A", False, None, remix)
    assert keyed.key_needs_confirming is True and keyed.unresolved == ""
    plan = setbuilder.build_set(remix, index, taxonomy=TAXONOMY, key="8A")
    assert original in [scored.track for scored in plan.pool]


def test_an_anchor_spelled_through_a_symlink_still_resolves(tmp_path):
    """The second pass in anchor_in_index, which was a zero row."""
    real = tmp_path / "real"
    (real / "Music").mkdir(parents=True)
    audio = real / "Music" / "anchor.flac"
    audio.touch()
    link = tmp_path / "linked"
    link.symlink_to(real, target_is_directory=True)

    indexed = track("Alder", "Anchor Work", "8A", path=str(audio))
    through_link = link / "Music" / "anchor.flac"

    assert through_link != audio, "the two spellings are identical, so this proves nothing"
    assert setbuild_cli.anchor_in_index(through_link, (indexed,)) is indexed
    # An anchor the index does not hold is absent rather than approximated.
    index = (track("Alder", "Anchor Work", "8A", path="/library/orig.flac"),)
    assert setbuild_cli.anchor_in_index(Path("/library/elsewhere.flac"), index) is None


def test_an_anchor_path_is_taken_against_the_library_and_never_walks_out_or_defaults(tmp_path):
    """Relative to the library and not the process; outside it or empty is refused."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    assert setbuild_cli.anchor_path("Music/x.flac", root) == root / "Music" / "x.flac"
    for typed, reason in (
        ("../elsewhere/x.flac", "setbuild-anchor-outside-library"),
        ("", "setbuild-anchor-unknown"),
    ):
        with pytest.raises(CratekitError) as caught:
            setbuild_cli.anchor_path(typed, root)
        assert caught.value.cause.reason == reason


# ── the disk half: a real library, tagged through the product's own writer ────


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One second of real FLAC, copied per fixture track."""
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def configured(library):
    """A set-up machine with NO DATABASE, which is all this verb may have."""
    cfg = config.from_dict({
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(library), "volume_id": "F1E2-D3C4",
            "db_path": str(library / "db" / "master.db"),
        },
        "paths": {"download_staging": str(library.parent / "staging")},
        "profile": {"name": "full"},
    })
    config.save(cfg)
    config.reset_cache()
    return cfg


@pytest.fixture
def place(library, silence):
    """One tagged FLAC in the library, and the path it landed at."""

    def put(artist, title, key, bpm, *, energy=None, vox=None, name=None, marker="") -> Path:
        # The marker goes right AFTER the head, where the renamer writes it.
        head = f"{key} - {bpm:g} - {marker + ' ' if marker else ''}{title}"
        path = library / "Music" / f"{name or f'{artist} - {head}'}.flac"
        shutil.copy2(silence, path)
        written = {"title": head, "artist": artist, "initialkey": key, "genre": GENRE,
                   "energylevel": energy, "voxlevel": vox}
        assert tags.write_tags(path, written), f"the fixture could not tag {path.name}"
        return path

    return put


def drive(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def envelope_of(argv: list[str]) -> tuple[int, dict]:
    code, out, err = drive(["--output", "json", *argv])
    assert out.strip(), f"the verb printed nothing to standard output: {err}"
    document = json.loads(out)
    assert output.envelope_problems(document) == [], document
    return code, document


def test_the_verb_produces_a_compatible_sequence_over_a_real_library(configured, place):
    """The end-to-end scenario, asserted against the ENGINE'S declared windows."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    place("Cedar", "Neighbour Up", "09A", 125, energy=8)
    place("Deodar", "Relative Major", "08B", 123, energy=6)
    place("Gum", "Wrong Key", "03B", 124, energy=5)
    place("Hazel", "Right Key Wrong Tempo", "08A", 100, energy=5)

    document = exited(envelope_of(["setbuild", str(anchor)]))
    assert document["outcome"] == "ok"
    data = document["data"]
    assert data["totals"]["anchor"]["owned"] is True
    assert data["totals"]["anchor"]["key"] == "8A"
    assert data["totals"]["sequence"], "no sequence was produced for an owned anchor"

    tiers = setbuilder.compatible_keys(data["totals"]["anchor"]["key"])
    for item in data["items"]:
        assert item["key"] in tiers, f"{item['title']} is not on a compatible key"
        tempo = data["totals"]["anchor"]["tempo"]
        assert setbuilder.in_band(item["tempo"], tempo), f"{item['title']} is off the band"

    titles = {item["title"] for item in data["items"]}
    assert "Wrong Key" not in titles
    assert "Right Key Wrong Tempo" not in titles
    assert "Anchor Work" not in titles


def test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure(configured, place):
    """Empty is an answer. The verb must not read "nothing mixes" as a fault."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    document = exited(envelope_of(["setbuild", str(anchor)]))
    data = document["data"]
    assert data["items"] == []
    assert data["totals"] == {
        "count": 0, "pool": 0, "sequence": 0, "payload_version": setbuilder.PAYLOAD_VERSION,
        "anchor": data["totals"]["anchor"],
    }
    assert data["digest"], "an empty plan still has an identity"
    # The outcome, not only the status: NO_OP also exits zero.
    assert document["outcome"] == "ok"


def material(cfg) -> dict[Path, int]:
    """Everything under the library that is the LIBRARY'S, with when it changed."""
    library = Path(cfg.library.root)
    state = config.library_state_dir(cfg)
    return {
        p: p.stat().st_mtime_ns
        for p in sorted(library.rglob("*"))
        if p != state and state not in p.parents
    }


def test_the_verb_writes_its_declared_cache_and_nothing_of_the_librarys(configured, place):
    """"No write to the library" as a structural assertion rather than a promise."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    cache = config.state_path("setbuilder_index_cache", configured)
    before = material(configured)
    assert not cache.exists()

    exited(envelope_of(["setbuild", str(anchor)]))
    assert material(configured) == before, "the verb touched the library"
    state = config.library_state_dir(configured)
    assert [p for p in state.rglob("*") if p.is_file()] == [cache]
    assert str(anchor) in json.loads(cache.read_text(encoding="utf-8"))["entries"]


def test_a_second_run_reads_no_tag_it_already_holds(configured, place, monkeypatch):
    """The cost R-188 names, measured as READS rather than as seconds."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    other = place("Birch", "Same Key Lower", "08A", 124, energy=4)
    reads: list[Path] = []
    real = setbuilder.read_index_tags

    def counting(path):
        reads.append(path)
        return real(path)

    # ``build_index`` binds its reader as a default argument, so replace the default.
    monkeypatch.setattr(setbuilder.build_index, "__kwdefaults__", {
        **setbuilder.build_index.__kwdefaults__, "reader": counting,
    })

    first = envelope_of(["setbuild", str(anchor)])[1]["data"]
    assert sorted(reads) == sorted([anchor, other])
    reads.clear()
    second = envelope_of(["setbuild", str(anchor)])[1]["data"]
    assert reads == [], "the cache was written and not read back"
    assert second == first, "a cached index answered differently from a scanned one"

    assert tags.write_tags(other, {"energylevel": 9})
    envelope_of(["setbuild", str(anchor)])
    assert reads == [other]


def test_the_first_run_opens_each_file_once_and_the_second_none(configured, place, monkeypatch):
    """U266: the cost the card names, counted as container OPENS through the verb."""
    import mutagen

    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    other = place("Birch", "Same Key Lower", "08A", 124, energy=4)
    third = place("Cedar", "Next Key Up", "09A", 124, energy=5, vox=30)
    opens: list[Path] = []
    real = mutagen.File

    def counting(target, *args, **kwargs):
        opens.append(Path(target))
        return real(target, *args, **kwargs)

    monkeypatch.setattr(mutagen, "File", counting)

    first = exited(envelope_of(["setbuild", str(anchor)]))
    assert first["data"], "the cold run built no set to compare"
    assert sorted(opens) == sorted([anchor, other, third]), "a cold run opens each file once"
    opens.clear()
    warm_code, warm = envelope_of(["setbuild", str(anchor)])
    assert warm_code == int(ExitCode.OK)
    assert warm["data"] == first["data"], "a cached index answered differently"
    assert opens == [], "a warm run opened a file the cache holds"


def test_a_cache_that_cannot_be_written_does_not_cost_the_set(configured, place):
    """A performance feature must not become an outage."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    blocker = config.library_state_dir(configured)
    blocker.write_text("not a directory", encoding="utf-8")

    document = exited(envelope_of(["setbuild", str(anchor)]))
    assert [item["title"] for item in document["data"]["items"]] == ["Same Key Lower"]
    assert blocker.read_text(encoding="utf-8") == "not a directory"


def test_an_anchor_with_no_camelot_key_is_not_indexed(configured, library, silence):
    """A file that is present, audio, and unusable."""
    path = library / "Music" / "Alder - Unanalyzed.flac"
    shutil.copy2(silence, path)
    assert tags.write_tags(path, {"title": "Unanalyzed", "artist": "Alder", "genre": GENRE})

    document = exited(envelope_of(["setbuild", str(path)]), ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-anchor-not-indexed"


def test_an_anchor_outside_the_library_refuses_before_any_scan(configured, tmp_path):
    outside = tmp_path / "elsewhere" / "Alder - 08A - 124 - Anchor Work.flac"
    outside.parent.mkdir(parents=True)
    outside.touch()

    document = exited(envelope_of(["setbuild", str(outside)]), ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-anchor-outside-library"


def test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor(
    configured, place
):
    """A library that is not there is not a library holding nothing."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    shutil.rmtree(configured.library.root)

    document = exited(envelope_of(["setbuild", str(anchor)]), ExitCode.LIBRARY_UNAVAILABLE)
    assert document["cause"]["reason"] == "library-root-absent"


def test_a_lossy_marked_companion_comes_back_with_a_clean_title(configured, place):
    """The template's marker declaration, which was a zero row."""
    marker = configured.naming.lossy_marker
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Lossy Companion", "08A", 124, energy=4, marker=marker)

    _, document = envelope_of(["setbuild", str(anchor)])

    titles = {item["title"] for item in document["data"]["items"]}
    assert "Lossy Companion" in titles, f"the marker survived into the title: {titles}"


def test_an_unowned_anchor_is_ranked_through_the_dispatcher(configured, place):
    """``crate setbuild --unowned LABEL --key 8A`` over a real library."""
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    place("Cedar", "Neighbour Up", "09A", 125, energy=8)
    place("Gum", "Wrong Key", "03B", 124, energy=5)
    before = material(configured)

    code, document = envelope_of(
        ["setbuild", "--unowned", "Oak - Not Bought Yet", "--key", "08A", "--bpm", "124"]
    )

    assert code == int(ExitCode.OK)
    assert document["outcome"] == "ok"
    assert document["data"]["totals"]["anchor"] == {
        "display": "Oak - Not Bought Yet", "key": "8A", "tempo": 124.0, "owned": False,
        "key_needs_confirming": True, "unresolved": "",
    }
    titles = {item["title"] for item in document["data"]["items"]}
    assert titles == {"Same Key Lower", "Neighbour Up"}
    assert document["data"]["totals"]["held"] == []
    assert material(configured) == before, "the unowned form touched the library"


#: A refusal through the dispatcher: argv, with ANCHOR standing for a placed
#: track's path, and the reason the envelope must carry.
REFUSALS = {
    "path-not-indexed": (["Music/no-such.flac"], "setbuild-anchor-not-indexed"),
    "empty-anchor": ([""], "setbuild-anchor-unknown"),
    "unowned-no-key": (["--unowned", "Oak - Not Bought Yet"], "setbuild-unowned-key-missing"),
    "key-beside-path": (["ANCHOR", "--key", "9A"], "setbuild-supplied-needs-unowned"),
    "tempo-beside-path": (["ANCHOR", "--bpm", "126"], "setbuild-supplied-needs-unowned"),
    "named-not-indexed": (["--named", "Nobody - Absent"], "setbuild-anchor-not-indexed"),
    "key-beside-name": (
        ["--named", "Alder - Anchor Work", "--key", "9A"], "setbuild-supplied-needs-unowned"
    ),
}


@pytest.mark.parametrize("case", list(REFUSALS))
def test_a_refused_invocation_is_a_precondition_with_its_own_reason(configured, place, case):
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    argv, reason = REFUSALS[case]
    library = Path(configured.library.root)
    argv = [str(anchor) if a == "ANCHOR" else str(library / a) if a.startswith("Music/") else a
            for a in argv]

    document = exited(envelope_of(["setbuild", *argv]), ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == reason
    assert document["cause"]["remediation"]["steps"], "a refusal with no next step"
    if case == "named-not-indexed":
        assert "Nobody - Absent" in document["cause"]["message"]


#: An invocation the parser refuses: argv, ANCHOR as above, and its stderr words.
USAGE = {
    "count-below-one": (["ANCHOR", "--count", "0"], "invalid positive_count value: '0'"),
    "key-off-the-wheel": (["--unowned", "Oak", "--key", "13C"], "invalid camelot_key value: '13C'"),
    "path-and-unowned": (
        ["ANCHOR", "--unowned", "Oak", "--key", "8A"], "not allowed with argument"
    ),
    "name-and-unowned": (
        ["--named", "Alder", "--unowned", "Oak", "--key", "8A"], "not allowed with argument"
    ),
    "name-and-path": (["--named", "Alder", "Music/x.flac"], "not allowed with argument"),
}


@pytest.mark.parametrize("case", list(USAGE))
def test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict(
    configured, place, capsys, case
):
    """Status 2, from the parser, with no envelope at all."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    argv, words = USAGE[case]
    argv = [str(anchor) if a == "ANCHOR" else a for a in argv]
    code, out, err = drive(["--output", "json", "setbuild", *argv])
    assert code == int(ExitCode.USAGE)
    assert not out.strip() and not err.strip(), "a usage failure emitted an envelope"
    assert words in capsys.readouterr().err


def test_a_path_anchor_is_unchanged_by_the_unowned_form(configured, place):
    """The path form still reads owned, with the library's own key."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)

    document = exited(envelope_of(["setbuild", str(anchor)]))
    assert document["data"]["totals"]["anchor"]["owned"] is True
    assert document["data"]["totals"]["anchor"]["key_needs_confirming"] is False
    assert {item["title"] for item in document["data"]["items"]} == {"Same Key Lower"}


def test_what_plays_after_a_track_is_asked_by_name(configured, place):
    """THE COST IN THE BRIEF, as the workflow a person runs."""
    original = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Alder", "Anchor Work (Extended Mix)", "08A", 124, energy=6)
    place("Cedar", "Neighbour Up", "09A", 125, energy=8)

    code, document = envelope_of(["setbuild", "--named", "Alder - Anchor Work", "--role", "after"])

    assert code == int(ExitCode.OK)
    assert document["data"]["totals"]["anchor"]["display"] == "Alder - Anchor Work"
    assert document["data"]["totals"]["anchor"]["owned"] is True
    assert "held" not in document["data"]["totals"]
    by_path = envelope_of(["setbuild", str(original), "--role", "after"])[1]
    assert document["data"] == by_path["data"]


def test_an_ambiguous_name_refuses_through_the_dispatcher_and_lists_the_paths(configured, place):
    original = place("Alder", "Anchor Work", "08A", 124, energy=6)
    extended = place("Alder", "Anchor Work (Extended Mix)", "08A", 124, energy=6)

    document = exited(envelope_of(["setbuild", "--named", "Anchor Work"]), ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-anchor-ambiguous"
    candidates = document["cause"]["detail"]["candidates"]
    assert {c["path"] for c in candidates} == {str(original), str(extended)}
    steps = " ".join(document["cause"]["remediation"]["steps"])
    assert str(original) in steps and str(extended) in steps


def test_an_empty_name_refuses_before_any_scan(configured, place):
    """Measured by the cache, which every scan writes and this run must not."""
    place("Alder", "Anchor Work", "08A", 124, energy=6)
    document = exited(envelope_of(["setbuild", "--named", " - "]), ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-anchor-unknown"
    assert not config.state_path("setbuilder_index_cache", configured).exists()


def test_the_role_flag_reaches_the_engine(configured, place):
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    place("Cedar", "Neighbour Up", "09A", 125, energy=8)

    _, document = envelope_of(["setbuild", str(anchor), "--role", "before"])
    assert document["data"]["items"], "the fixture produced nothing for one side"
    assert all(item["role"] in ("before", "either") for item in document["data"]["items"])


# ── the registry, and the profile that switches this verb off ────────────────


def test_the_entry_has_lost_its_planned_marker_and_declares_no_write():
    entry = next(e for e in registry.entries() if e.name == "setbuild")
    assert entry.landed, "the module shipped, so the countdown marker must be gone"
    assert entry.module == "cratekit.setbuilder.cli"
    assert entry.writes == frozenset(), "a write surface would make the verb destructive"
    assert (entry.destructive, entry.long_running, entry.gates) == (False, False, ())


def test_the_verb_appears_in_help_under_the_full_profile(configured, capsys):
    """Read through ``capsys``: argparse prints help to the process's own stdout."""
    assert drive(["--help"])[0] == int(ExitCode.OK)
    assert "setbuild" in capsys.readouterr().out


def test_a_profile_without_the_setbuilder_module_withdraws_the_verb():
    """Asserted on the parser rather than on a help screen."""
    from cratekit.core import profiles

    entry = next(e for e in registry.entries() if e.name == "setbuild")
    full = cli.build_parser([entry], membership=profiles.resolve("full"))
    assert full.parse_args(["setbuild", "x.flac"])._entry is entry

    slim = cli.build_parser([entry], membership=profiles.resolve("slim"))
    with pytest.raises(SystemExit):
        slim.parse_args(["setbuild", "x.flac"])
