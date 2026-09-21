"""U43: ``crate setbuild``, the shell over the set-building engine U35 landed.

TWO HALVES, AND THE SPLIT IS DELIBERATE. The pure half drives
:func:`cratekit.setbuilder.cli.plan_for` over a frozen index, which is where every
property about ordering, positions and the digest lives; none of it needs a disk.
The disk half builds a small real library, tags it through the product's own
writer and drives the actual dispatcher, which is the only thing that can prove
the index, the anchor lookup and the envelope agree.

WHY THE FIXTURE LIBRARY CARRIES ITS TEMPO IN THE TITLE TAG rather than in a tempo
tag: nothing in this product writes a tempo tag, ever (R17), and the engine reads
the tempo out of the declared name head for exactly that reason. A fixture that
wrote one would be testing a shape the product refuses to produce.
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

TAXONOMY = taxonomy.default_taxonomy()

#: The genre every fixture track carries. One value, so genre affinity is a
#: constant across the pool and the harmonic and tempo signals are what move the
#: ordering. A mixed-genre fixture would make the ranking assertions depend on
#: the shipped taxonomy's family table, which is a different unit's subject.
GENRE = "Deep House"


# ── the pure half: plan_for over a frozen index ──────────────────────────────


def track(artist, title, key, bpm=124.0, energy=5, vox=None, path=""):
    return setbuilder.Track(
        artist=artist,
        title=title,
        key=setbuilder.canonical_key(key),
        bpm=bpm,
        genre=GENRE,
        energy=energy,
        vox=vox,
        voxgender=None,
        match=setbuilder.match_key(artist, title),
        path=path or f"/library/{artist}-{title}.flac",
    )


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
    """THE DRIFT PIN, and the reason this shell may reimplement four lines.

    ``plan_for`` cannot call ``build_set``, because ``build_set`` opens with the
    fuzzy anchor resolution this verb replaces with a path lookup. Everything
    after that resolution is ``build_set``'s own composition, and a copy of four
    lines is a copy that drifts. So the two are compared here over an anchor
    whose display resolves unambiguously, which makes the fuzzy path and the path
    path produce the same anchor and leaves the composition as the only
    difference. The day either side changes, this fails rather than the two
    quietly disagreeing.
    """
    anchor = anchor_of(index)
    mine = setbuild_cli.plan_for(anchor, index, declared=TAXONOMY)
    theirs = setbuilder.build_set(anchor.display, index, taxonomy=TAXONOMY)

    assert theirs.anchor.owned and theirs.anchor.track is anchor, (
        "the fixture's anchor no longer resolves to itself by display, so this "
        "comparison is between two different anchors and proves nothing"
    )
    assert [item["path"] for item in mine["items"] if item["position"] is not None] == [
        scored.track.path for scored in theirs.sequence
    ]
    assert {item["path"] for item in mine["items"]} == {
        scored.track.path for scored in theirs.pool
    } | {scored.track.path for scored in theirs.sequence}
    assert mine["totals"]["sequence"] == len(theirs.sequence)


def test_the_sequence_leads_the_items_and_carries_its_own_order(index):
    plan = setbuild_cli.plan_for(anchor_of(index), index, declared=TAXONOMY)
    positions = [item["position"] for item in plan["items"]]
    placed = [p for p in positions if p is not None]

    assert placed, "the fixture produced no sequence, so ordering is untested"
    assert placed == list(range(1, len(placed) + 1)), (
        "the sequence must lead the items in its own order, so a consumer can "
        "read the recommendation off the top of the array"
    )
    assert positions[: len(placed)] == placed, "a pool-only item interrupts the sequence"
    assert all(p is None for p in positions[len(placed):])
    assert plan["totals"]["sequence"] == len(placed)


def test_every_recommendation_came_out_of_the_index(index):
    """The grounding rule, asserted at the shell's own output boundary.

    The engine asserts it too. It is asserted again here because this is the
    surface a person reads, and a shell that reshaped the payload is a shell that
    could have introduced an item the index never held.
    """
    plan = setbuild_cli.plan_for(anchor_of(index), index, declared=TAXONOMY)
    owned = {t.path for t in index}
    assert plan["items"], "no items, so this guard measured nothing"
    for item in plan["items"]:
        assert item["path"] in owned
    assert all(item["path"] != anchor_of(index).path for item in plan["items"]), (
        "the anchor came back as its own companion"
    )


def test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical(index):
    """Two plans over the same companions and different anchors are two plans.

    Built by RENAMING the anchor rather than by choosing a second one, because a
    second anchor changes the pool and the item lists stop being comparable. A
    rename moves the anchor's identity and touches none of its ranking signals,
    so the items come out byte for byte identical and the digest is the only
    thing that can tell the two apart.
    """
    original = anchor_of(index)
    renamed = track(
        "Alder", "Anchor Work (Alternate Master)", "8A", original.bpm, energy=original.energy
    )
    first = setbuild_cli.plan_for(original, index, declared=TAXONOMY)
    second = setbuild_cli.plan_for(renamed, (renamed, *index[1:]), declared=TAXONOMY)

    assert first["items"] == second["items"], (
        "the rename moved a ranking signal, so this is no longer a test about "
        "the anchor's presence in the digest"
    )
    assert first["digest"] != second["digest"]


def test_two_plans_over_the_same_anchor_and_different_companions_digest_apart(index):
    """The other half of the digest, and it was a zero row.

    The test above pins that the anchor is IN the digest. Nothing pinned that the
    items are, so a digest computed over the anchor alone passed the whole suite:
    two entirely different sets of recommendations for one anchor would have
    carried one identity. Found by mutation.
    """
    anchor = anchor_of(index)
    full = setbuild_cli.plan_for(anchor, index, declared=TAXONOMY)
    narrowed = setbuild_cli.plan_for(anchor, index[:3], declared=TAXONOMY)

    assert full["items"] != narrowed["items"], (
        "the two indexes produced the same items, so this measures nothing"
    )
    assert full["totals"]["anchor"] == narrowed["totals"]["anchor"], (
        "the anchor moved as well, so the digest could be telling the two apart "
        "on the anchor and this would not notice"
    )
    assert full["digest"] != narrowed["digest"]


def test_the_same_anchor_and_index_always_digest_the_same(index):
    first = setbuild_cli.plan_for(anchor_of(index), index, declared=TAXONOMY)
    second = setbuild_cli.plan_for(anchor_of(index), tuple(reversed(index)), declared=TAXONOMY)
    assert first["digest"] == second["digest"]


def test_an_unowned_anchor_in_8a_ranks_the_library_against_it(index):
    """U98's scenario: companions for a track the index does not hold."""
    anchor = setbuild_cli.unowned_anchor("Oak - Not Bought Yet", "8A", None)
    plan = setbuild_cli.plan_for(anchor, index, declared=TAXONOMY)

    assert plan["totals"]["anchor"]["owned"] is False
    assert plan["totals"]["anchor"]["key_needs_confirming"] is True
    assert plan["totals"]["anchor"]["key"] == "8A"
    assert plan["totals"]["anchor"]["display"] == "Oak - Not Bought Yet"
    assert plan["items"], "an unowned 8A anchor found no companions in the fixture"
    tiers = setbuilder.compatible_keys("8A")
    assert all(item["key"] in tiers for item in plan["items"])
    assert "Wrong Key" not in {item["title"] for item in plan["items"]}


def test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it(index):
    """The empty index is the guarantee, so drive a label that WOULD fuzzy match.

    Given the index, ``resolve_anchor`` would resolve this label to the owned
    "Anchor Work (Extended Mix)" and take its key, because ``token_set_ratio``
    scores a subset at 100. Against the empty index it cannot, so the key is the
    supplied one and the owned extended mix is an ordinary companion, not the
    anchor and not held.
    """
    extended = track("Alder", "Anchor Work (Extended Mix)", "9A", 124.0)
    library = (extended, *index[1:])
    label = "Alder - Anchor Work"
    assert setbuilder.resolve_anchor(label, library, key="9A").track is extended, (
        "the label no longer fuzzy matches the owned track, so this measures nothing"
    )
    anchor = setbuild_cli.unowned_anchor(label, "9A", None)
    plan = setbuild_cli.plan_for(anchor, library, declared=TAXONOMY)

    assert anchor.owned is False and anchor.track is None
    assert plan["totals"]["anchor"]["key"] == "9A"
    assert extended.path in {item["path"] for item in plan["items"]}
    assert plan["totals"]["held"] == []


def test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked(index):
    """The review's finding, driven: the library's copy as its own companion.

    Before the exact match exclusion this plan's first sequence pick was the
    owned "Anchor Work", at the perfect key tier, recommended as the best mix
    for the track it is.
    """
    owned = anchor_of(index)
    plan = setbuild_cli.plan_for(
        setbuild_cli.unowned_anchor(owned.display, "8A", 124.0), index, declared=TAXONOMY
    )

    assert owned.path not in {item["path"] for item in plan["items"]}
    assert plan["totals"]["held"] == [owned.path]
    assert plan["items"], "nothing else was ranked, so the exclusion measured nothing"


def test_an_unowned_sequence_places_each_companion_once(index):
    """Every companion of an unowned anchor has no energy relation to it, so most
    are ``either``, and ``either`` filler used to be picked for BOTH sides. The
    positions then skipped 1 and a companion was in the set twice.
    """
    plan = setbuild_cli.plan_for(
        setbuild_cli.unowned_anchor("Oak", "8A", 124.0), index, declared=TAXONOMY
    )
    placed = [item["position"] for item in plan["items"] if item["position"] is not None]
    paths = [item["path"] for item in plan["items"]]

    assert placed == list(range(1, len(placed) + 1))
    assert len(paths) == len(set(paths)), "a companion appears twice in the items"
    assert plan["totals"]["sequence"] == len(placed)


def test_an_unowned_anchor_with_no_key_refuses():
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.unowned_anchor("Oak - Not Bought Yet", None, None)
    assert caught.value.cause.reason == "setbuild-unowned-key-missing"
    assert caught.value.cause.remediation.steps


def test_an_empty_unowned_label_refuses_as_an_unknown_anchor():
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.unowned_anchor("", "8A", None)
    assert caught.value.cause.reason == "setbuild-anchor-unknown"


@pytest.mark.parametrize("text", ["13C", "13A", "0A", "8C", "", "eight"])
def test_a_key_off_the_wheel_is_refused_at_the_parser(text):
    with pytest.raises(ValueError):
        setbuild_cli.camelot_key(text)


def test_a_key_is_canonicalized_at_the_parser():
    assert setbuild_cli.camelot_key("08A") == "8A"
    assert setbuild_cli.camelot_key("12b") == "12B"


@pytest.mark.parametrize("text", ["0", "-124", "nan", "inf", "-inf"])
def test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser(text):
    with pytest.raises(ValueError):
        setbuild_cli.positive_tempo(text)


def test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band(index):
    """``--bpm`` is a ranking input: with it, the tempo band applies."""
    keyless = setbuild_cli.plan_for(
        setbuild_cli.unowned_anchor("Oak", "8A", None), index, declared=TAXONOMY
    )
    banded = setbuild_cli.plan_for(
        setbuild_cli.unowned_anchor("Oak", "8A", 124.0), index, declared=TAXONOMY
    )
    assert "Right Key Wrong Tempo" in {item["title"] for item in keyless["items"]}
    assert "Right Key Wrong Tempo" not in {item["title"] for item in banded["items"]}
    assert banded["totals"]["anchor"]["tempo"] == 124.0


def test_one_either_companion_of_an_owned_anchor_is_placed_once():
    """The same defect on main, through the owned form and through ``build_set``.

    One same-key companion of equal energy is ``either``. It was the before
    side's filler and the after side's filler, so the sequence was that one
    track twice and its only position was 2.
    """
    anchor = track("Alder", "Anchor Work", "8A", 124.0, energy=5)
    other = track("Birch", "Other", "8A", 124.0, energy=5)
    plan = setbuild_cli.plan_for(anchor, (anchor, other), declared=TAXONOMY)
    engine = setbuilder.build_set(anchor.display, (anchor, other), taxonomy=TAXONOMY)

    assert [item["position"] for item in plan["items"]] == [1]
    assert [scored.track.path for scored in engine.sequence] == [other.path]


def test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart(index):
    """Ownership is part of the question, so it is part of the identity.

    Built so that EVERY OTHER INPUT IS EQUAL. The owned anchor sits outside the
    index and carries no genre, energy or vocal reading, which is exactly what an
    unowned anchor contributes, and the label is its display. The items therefore
    come out identical and the rendered anchor differs only in ``owned`` and
    ``key_needs_confirming``, so the digest is the only thing left to tell them
    apart.
    """
    owned = dataclasses.replace(
        track("Oak", "Not Bought Yet", "8A", 124.0), genre=None, energy=None
    )
    first = setbuild_cli.plan_for(owned, index, declared=TAXONOMY)
    second = setbuild_cli.plan_for(
        setbuild_cli.unowned_anchor(owned.display, "8A", 124.0), index, declared=TAXONOMY
    )

    assert first["items"] == second["items"], (
        "the two anchors ranked differently, so the digest is not the only difference"
    )
    assert first["items"], "no companions, so the comparison is between two empty plans"
    assert first["digest"] != second["digest"]


def test_a_role_narrows_the_answer_to_one_side(index):
    plan = setbuild_cli.plan_for(anchor_of(index), index, declared=TAXONOMY, role="before")
    assert plan["items"], "the fixture produced nothing for one side"
    assert all(item["role"] in ("before", "either") for item in plan["items"])


@pytest.fixture
def wide_index():
    """An index with more compatible companions than any default returns.

    THE EIGHT-TRACK FIXTURE ABOVE CANNOT MEASURE A CAP, and that is why this one
    exists. It yields five compatible companions, which is fewer than
    ``DEFAULT_POOL``, so ``pool[:2]`` and ``pool[:8]`` union with the same
    four-entry sequence to the same five items and a cap assertion over it holds
    whether the cap is applied or not. Found by mutation: dropping ``count`` on
    the way to the engine killed nothing.
    """
    keys = ("8A", "8B", "7A", "9A")
    return (
        track("Alder", "Anchor Work", "8A", 124.0, energy=6),
        *(
            track(f"Tree{n:02d}", f"Companion {n:02d}", keys[n % len(keys)], 124.0, energy=n)
            for n in range(1, 11)
        ),
    )


def test_a_count_caps_the_companions(wide_index):
    """The cap reaches the engine, and its effect is reported rather than implied.

    ``pool`` is the number the cap governs. ``count`` is the size of the union
    with the sequence and can exceed the cap, because the sequence is drawn from
    the full ranked list and ships whole. Both are asserted, so a change to
    either the cap or the union rule is reported.
    """
    capped = setbuild_cli.plan_for(anchor_of(wide_index), wide_index, declared=TAXONOMY, count=2)
    uncapped = setbuild_cli.plan_for(anchor_of(wide_index), wide_index, declared=TAXONOMY)

    assert uncapped["totals"]["pool"] > capped["totals"]["pool"], (
        "the fixture yields too few companions for a cap to be observable, so "
        "this measures nothing"
    )
    assert capped["totals"]["pool"] == 2
    assert uncapped["totals"]["pool"] == setbuilder.DEFAULT_POOL
    assert len(capped["items"]) < len(uncapped["items"])
    assert capped["totals"]["count"] == len(capped["items"])


def test_the_payload_validates_against_the_declared_plan_surface(index):
    """``plan/1`` is closed, so a fifth key here is a defect rather than an extra.

    This is the guard that catches the shell putting the anchor at the top level
    instead of inside ``totals``, which is where the closed surface forces it.
    """
    plan = setbuild_cli.plan_for(anchor_of(index), index, declared=TAXONOMY)
    assert output.payload_problems("plan", plan) == []
    assert plan["totals"]["anchor"]["display"] == anchor_of(index).display


def test_the_vocal_signal_is_reachable_only_because_a_threshold_can_be_supplied():
    """The fifth ranking signal, which is dead weight without the flag.

    Nothing below the modules layer publishes a vocal threshold and importing the
    vocals module would couple a read-only recommender to a toggleable one, so an
    unsupplied threshold scores every candidate neutral and the signal's whole
    weight does nothing. The flag is what makes it reachable at all, and this
    drives that rather than asserting it.
    """
    anchor = track("Alder", "Anchor Work", "8A", 124.0, energy=5, vox=90)
    loud = track("Birch", "Also Vocal", "8A", 124.0, energy=5, vox=90)
    quiet = track("Cedar", "Instrumental", "8A", 124.0, energy=5, vox=5)
    index = (anchor, loud, quiet)

    neutral = setbuild_cli.plan_for(anchor, index, declared=TAXONOMY)
    thresholded = setbuild_cli.plan_for(anchor, index, declared=TAXONOMY, vox_threshold=50.0)

    assert [item["path"] for item in neutral["items"]] != [
        item["path"] for item in thresholded["items"]
    ], "the threshold changed no ordering, so the signal is not reachable"
    assert thresholded["items"][0]["path"] == quiet.path, (
        "two lead vocals were stacked despite a threshold that declares both "
        "vocal-forward"
    )


# ── the anchor lookup, which is the whole reason the positional is a path ─────


def test_the_anchor_is_found_by_path_and_never_by_title():
    """THE DESIGN DECISION, DRIVEN RATHER THAN ARGUED.

    ``token_set_ratio`` scores a subset at 100, so the engine's fuzzy lookup
    cannot distinguish a title from that title plus a version suffix, and
    ``extractOne`` returns whichever it met first. Driven here on both paths in
    one test: the fuzzy lookup returns the WRONG file for an exact query naming
    the original, and the path lookup returns the right one. Building a set
    around the wrong anchor is this verb's worst answer, because every pick after
    it is internally consistent and therefore looks right.
    """
    extended = track("Alder", "Anchor Work (Extended Mix)", "8A", path="/library/ext.flac")
    original = track("Alder", "Anchor Work", "8A", path="/library/orig.flac")
    index = (extended, original)

    assert setbuilder.find_in_index("Alder - Anchor Work", index) is extended, (
        "the fuzzy lookup no longer mis-resolves, so the argument for a path "
        "positional has changed and this file should say the new one"
    )
    assert setbuild_cli.anchor_in_index(Path("/library/orig.flac"), index) is original


def test_an_anchor_spelled_through_a_symlink_still_resolves(tmp_path):
    """The second pass in anchor_in_index, which was a zero row.

    The index records the path the walk produced, which is the configured root
    joined with a relative path and is not resolved. A person can reasonably hand
    the verb the same file spelled through a symlinked mount, and on macOS the
    two spellings of a temporary directory differ by a ``/private`` prefix all on
    their own. Nothing exercised that, so deleting the whole fallback killed
    nothing and a real user's paste would have been told their track is not in
    their library.
    """
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


def test_an_anchor_the_index_does_not_hold_is_absent_rather_than_approximated():
    index = (track("Alder", "Anchor Work", "8A", path="/library/orig.flac"),)
    assert setbuild_cli.anchor_in_index(Path("/library/elsewhere.flac"), index) is None


def test_a_relative_anchor_is_taken_against_the_library_and_not_the_process(tmp_path):
    root = tmp_path / "library"
    root.mkdir()
    assert setbuild_cli.anchor_path("Music/x.flac", root) == root / "Music" / "x.flac"


def test_an_anchor_that_walks_out_of_the_library_is_refused(tmp_path):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    with pytest.raises(CratekitError) as caught:
        setbuild_cli.anchor_path("../elsewhere/x.flac", root)
    assert caught.value.cause.reason == "setbuild-anchor-outside-library"


def test_an_empty_anchor_is_refused_rather_than_defaulted(tmp_path):
    from cratekit.core.cause import CratekitError

    with pytest.raises(CratekitError) as caught:
        setbuild_cli.anchor_path("", tmp_path)
    assert caught.value.cause.reason == "setbuild-anchor-unknown"


@pytest.mark.parametrize("text", ["0", "-1", "-8"])
def test_a_count_below_one_is_refused_at_the_parser(text):
    """The engine's own slice is why this guard exists.

    ``build_plan`` slices ``pool[: count or DEFAULT_POOL]``: zero is falsy and
    silently becomes eight, and a negative silently drops the last-ranked
    companion. Both answer a question nobody asked. Refused at the parser because
    status 2 belongs to the argument parser and this is the same kind of
    statement ``type=int`` already makes.
    """
    with pytest.raises(ValueError):
        setbuild_cli.positive_count(text)


def test_a_count_of_one_is_accepted():
    assert setbuild_cli.positive_count("1") == 1


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
    """A set-up machine with NO DATABASE, which is all this verb may have.

    Deliberately not the conformance suite's fixture. That one builds a
    disposable rekordbox database because the destructive verbs it drives will
    not admit a machine without one; copying it here would imply this verb needs
    something it is structurally forbidden from touching.
    """
    cfg = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(library / "db" / "master.db"),
            },
            "paths": {"download_staging": str(library.parent / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(cfg)
    config.reset_cache()
    return cfg


@pytest.fixture
def place(library, silence):
    """One tagged FLAC in the library, and the path it landed at.

    The head goes in the TITLE TAG because that is where the engine reads the
    tempo from, and it reads it there because nothing in this product writes a
    tempo tag (R17). ``initialkey`` is written as well as being spelled in the
    head, which is the state a real analyzed file is in.
    """

    def put(artist, title, key, bpm, *, energy=None, vox=None, name=None, marker="") -> Path:
        # The marker goes immediately AFTER the head, which is where the renamer
        # writes it and the only position where the declared template's marker
        # rule has any effect. See the lossy-companion test.
        head = f"{key} - {bpm:g} - {marker + ' ' if marker else ''}{title}"
        path = library / "Music" / f"{name or f'{artist} - {head}'}.flac"
        shutil.copy2(silence, path)
        assert tags.write_tags(
            path,
            {
                "title": head,
                "artist": artist,
                "initialkey": key,
                "genre": GENRE,
                "energylevel": energy,
                "voxlevel": vox,
            },
        ), f"the fixture could not tag {path.name}"
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
    """The end-to-end scenario, asserted against the ENGINE'S declared windows.

    No tempo or key number is typed into the assertions. The harmonic window
    comes from ``compatible_keys`` and the tempo window from ``in_band`` at the
    engine's own default half-width, so a change to either window moves this test
    with it rather than leaving it asserting about a rule nobody holds any more.
    """
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    place("Cedar", "Neighbour Up", "09A", 125, energy=8)
    place("Deodar", "Relative Major", "08B", 123, energy=6)
    place("Gum", "Wrong Key", "03B", 124, energy=5)
    place("Hazel", "Right Key Wrong Tempo", "08A", 100, energy=5)

    code, document = envelope_of(["setbuild", str(anchor)])

    assert code == int(ExitCode.OK)
    assert document["outcome"] == "ok"
    data = document["data"]
    assert data["totals"]["anchor"]["owned"] is True
    assert data["totals"]["anchor"]["key"] == "8A"
    assert data["totals"]["sequence"], "no sequence was produced for an owned anchor"

    tiers = setbuilder.compatible_keys(data["totals"]["anchor"]["key"])
    for item in data["items"]:
        assert item["key"] in tiers, f"{item['title']} is not on a compatible key"
        assert setbuilder.in_band(
            item["tempo"], data["totals"]["anchor"]["tempo"]
        ), f"{item['title']} is outside the tempo band"

    titles = {item["title"] for item in data["items"]}
    assert "Wrong Key" not in titles
    assert "Right Key Wrong Tempo" not in titles
    assert "Anchor Work" not in titles


def test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure(
    configured, place
):
    """Empty is an answer. The verb must not read "nothing mixes" as a fault."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    code, document = envelope_of(["setbuild", str(anchor)])

    assert code == int(ExitCode.OK)
    assert document["data"]["items"] == []
    assert document["data"]["totals"] == {
        "count": 0,
        "pool": 0,
        "sequence": 0,
        "payload_version": setbuilder.PAYLOAD_VERSION,
        "anchor": document["data"]["totals"]["anchor"],
    }
    assert document["data"]["digest"], "an empty plan still has an identity"
    # THE OUTCOME AND NOT ONLY THE STATUS, because NO_OP also exits zero and the
    # status alone could not tell the two apart. Found by mutation: making an
    # empty plan report NO_OP killed nothing, and the difference is what a
    # consumer reads to decide whether the question was answered or skipped. It
    # was answered; "nothing here mixes with it" is a result.
    assert document["outcome"] == "ok"


def test_the_verb_writes_nothing_at_all(configured, place):
    """"No write" as a structural assertion rather than a promise.

    It covers the cache decision specifically: ``build_index`` is called with no
    cache path, so the declared ``setbuilder_index_cache`` state file must not
    appear. A cache would be a ``files`` write, and the registry entry declares
    none.
    """
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    library = Path(configured.library.root)
    before = {p: p.stat().st_mtime_ns for p in sorted(library.rglob("*"))}

    code, _ = envelope_of(["setbuild", str(anchor)])

    assert code == int(ExitCode.OK)
    after = {p: p.stat().st_mtime_ns for p in sorted(library.rglob("*"))}
    assert after == before, "the verb touched the library"
    assert not (library / "setbuilder_index.json").exists()


def test_an_anchor_that_is_not_in_the_library_refuses_with_a_vocabulary_code(
    configured, place
):
    place("Alder", "Anchor Work", "08A", 124, energy=6)
    library = Path(configured.library.root)
    code, document = envelope_of(["setbuild", str(library / "Music" / "no-such.flac")])

    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-anchor-not-indexed"
    assert document["cause"]["remediation"]["steps"], "a refusal with no next step"


def test_an_anchor_with_no_camelot_key_is_not_indexed(configured, library, silence):
    """A file that is present, audio, and unusable. The third of the three.

    One slug covers absent, not-audio and keyless because the index is what
    decides ownership and a track it does not hold cannot be ranked against,
    whichever of the three put it outside. This drives the least obvious of them:
    the file is right there and the answer is still no.
    """
    path = library / "Music" / "Alder - Unanalyzed.flac"
    shutil.copy2(silence, path)
    assert tags.write_tags(path, {"title": "Unanalyzed", "artist": "Alder", "genre": GENRE})

    code, document = envelope_of(["setbuild", str(path)])

    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-anchor-not-indexed"


def test_an_anchor_outside_the_library_refuses_before_any_scan(configured, tmp_path):
    outside = tmp_path / "elsewhere" / "Alder - 08A - 124 - Anchor Work.flac"
    outside.parent.mkdir(parents=True)
    outside.touch()

    code, document = envelope_of(["setbuild", str(outside)])

    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-anchor-outside-library"


def test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor(
    configured, place
):
    """A library that is not there is not a library holding nothing.

    Without the root check the scan walks a directory that does not exist, finds
    no files, and every anchor comes back "not in the library index", which tells
    a person with an unmounted volume that their track is missing. That is
    METHOD's named cost of a clean report over state the tool could not read, and
    it was a zero row: nothing drove a missing root.
    """
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    shutil.rmtree(configured.library.root)

    code, document = envelope_of(["setbuild", str(anchor)])

    assert code == int(ExitCode.LIBRARY_UNAVAILABLE)
    assert document["cause"]["reason"] == "library-root-absent"


def test_a_lossy_marked_companion_comes_back_with_a_clean_title(configured, place):
    """The template's marker declaration, which was a zero row.

    The renamer writes the marker immediately after the head, so a marked file's
    title tag reads "08A - 124 - [MP3] Anchor Work". With the marker declared the
    head parser strips it and the clean title is "Anchor Work"; without it the
    title keeps the marker and the match key gains a token, which is the exact
    defect the engine's own docstring says the declared template was adopted to
    close. Nothing in the suite carried a marked fixture, so dropping the marker
    from this shell's template killed nothing.

    THE MARKER'S POSITION IS THE WHOLE TEST. The first attempt at this fixture put
    it at the END of the title, where it changes nothing either way, and would
    have been a guard that passes under the mutation it was written to catch.
    """
    marker = configured.naming.lossy_marker
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Lossy Companion", "08A", 124, energy=4, marker=marker)

    _, document = envelope_of(["setbuild", str(anchor)])

    titles = {item["title"] for item in document["data"]["items"]}
    assert "Lossy Companion" in titles, f"the marker survived into the title: {titles}"


def test_an_empty_anchor_refuses_through_the_dispatcher(configured):
    code, document = envelope_of(["setbuild", ""])
    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-anchor-unknown"


def test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal(
    configured, place, capsys
):
    """Status 2, from the parser, with no envelope at all. That is the contract.

    Read through ``capsys`` rather than through the injected streams on purpose:
    argparse writes its own usage failure to the process's standard error before
    the dispatcher exists, which is precisely what "status 2 belongs to the
    argument parser and to nothing else" means. A message found on the injected
    stream would mean the refusal had come from somewhere else.
    """
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    code, out, err = drive(["--output", "json", "setbuild", str(anchor), "--count", "0"])
    assert code == int(ExitCode.USAGE)
    assert not out.strip() and not err.strip(), "a usage failure emitted an envelope"
    assert "invalid positive_count value: '0'" in capsys.readouterr().err


def test_an_unowned_anchor_is_ranked_through_the_dispatcher(configured, place):
    """``crate setbuild --unowned LABEL --key 8A`` over a real library."""
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    place("Cedar", "Neighbour Up", "09A", 125, energy=8)
    place("Gum", "Wrong Key", "03B", 124, energy=5)
    library = Path(configured.library.root)
    before = {p: p.stat().st_mtime_ns for p in sorted(library.rglob("*"))}

    code, document = envelope_of(
        ["setbuild", "--unowned", "Oak - Not Bought Yet", "--key", "08A", "--bpm", "124"]
    )

    assert code == int(ExitCode.OK)
    assert document["outcome"] == "ok"
    anchor = document["data"]["totals"]["anchor"]
    assert anchor == {
        "display": "Oak - Not Bought Yet",
        "key": "8A",
        "tempo": 124.0,
        "owned": False,
        "key_needs_confirming": True,
        "unresolved": "",
    }
    titles = {item["title"] for item in document["data"]["items"]}
    assert titles == {"Same Key Lower", "Neighbour Up"}
    assert document["data"]["totals"]["held"] == []
    after = {p: p.stat().st_mtime_ns for p in sorted(library.rglob("*"))}
    assert after == before, "the unowned form touched the library"


def test_an_unowned_anchor_with_no_key_refuses_through_the_dispatcher(configured, place):
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    code, document = envelope_of(["setbuild", "--unowned", "Oak - Not Bought Yet"])

    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-unowned-key-missing"
    assert document["cause"]["remediation"]["steps"]


def test_a_key_off_the_wheel_is_the_parsers_verdict(configured, capsys):
    code, out, err = drive(
        ["--output", "json", "setbuild", "--unowned", "Oak", "--key", "13C"]
    )
    assert code == int(ExitCode.USAGE)
    assert not out.strip() and not err.strip(), "a usage failure emitted an envelope"
    assert "invalid camelot_key value: '13C'" in capsys.readouterr().err


def test_a_path_and_an_unowned_label_together_are_the_parsers_verdict(
    configured, place, capsys
):
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    code, _, _ = drive(
        ["--output", "json", "setbuild", str(anchor), "--unowned", "Oak", "--key", "8A"]
    )
    assert code == int(ExitCode.USAGE)
    assert "not allowed with argument" in capsys.readouterr().err


@pytest.mark.parametrize(
    "flags", [["--key", "9A"], ["--bpm", "126"]], ids=["key", "tempo"]
)
def test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored(
    configured, place, flags
):
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)

    code, document = envelope_of(["setbuild", str(anchor), *flags])

    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "setbuild-supplied-needs-unowned"


def test_a_path_anchor_is_unchanged_by_the_unowned_form(configured, place):
    """The path form still reads owned, with the library's own key."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)

    code, document = envelope_of(["setbuild", str(anchor)])

    assert code == int(ExitCode.OK)
    assert document["data"]["totals"]["anchor"]["owned"] is True
    assert document["data"]["totals"]["anchor"]["key_needs_confirming"] is False
    assert {item["title"] for item in document["data"]["items"]} == {"Same Key Lower"}


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
    assert entry.writes == frozenset(), (
        "a write surface here would make the verb destructive by the registry's "
        "own invariant, and a read-only recommender does not bind the library "
        "lock, the backup acknowledgment and the volume identity assertion"
    )
    assert entry.destructive is False
    assert entry.long_running is False
    assert entry.gates == ()


def test_the_verb_appears_in_help_under_the_full_profile(configured, capsys):
    """Read through ``capsys``: argparse prints help to the process's own stdout."""
    assert drive(["--help"])[0] == int(ExitCode.OK)
    assert "setbuild" in capsys.readouterr().out


def test_a_profile_without_the_setbuilder_module_withdraws_the_verb():
    """Asserted on the parser rather than on a help screen.

    A help screen is a rendering, and a verb can be missing from one while still
    being reachable by typing it. This asks the parser the question a person's
    keystrokes ask.
    """
    from cratekit.core import profiles

    entry = next(e for e in registry.entries() if e.name == "setbuild")
    full = cli.build_parser([entry], membership=profiles.resolve("full"))
    assert full.parse_args(["setbuild", "x.flac"])._entry is entry

    slim = cli.build_parser([entry], membership=profiles.resolve("slim"))
    with pytest.raises(SystemExit):
        slim.parse_args(["setbuild", "x.flac"])
