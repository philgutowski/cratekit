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

import io
import json
import shutil
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output, registry
from cratekit.core import config, tags, taxonomy
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


def test_the_same_anchor_and_index_always_digest_the_same(index):
    first = setbuild_cli.plan_for(anchor_of(index), index, declared=TAXONOMY)
    second = setbuild_cli.plan_for(anchor_of(index), tuple(reversed(index)), declared=TAXONOMY)
    assert first["digest"] == second["digest"]


def test_a_role_narrows_the_answer_to_one_side(index):
    plan = setbuild_cli.plan_for(anchor_of(index), index, declared=TAXONOMY, role="before")
    assert plan["items"], "the fixture produced nothing for one side"
    assert all(item["role"] in ("before", "either") for item in plan["items"])


def test_a_count_caps_the_companions(index):
    plan = setbuild_cli.plan_for(anchor_of(index), index, declared=TAXONOMY, count=2)
    assert plan["totals"]["count"] == len(plan["items"])
    # The sequence is drawn from the whole ranked list rather than from the
    # capped pool, so the item count is the cap plus whatever the sequence
    # contributed that the cap excluded. Asserting the cap holds on the pool half
    # is what this measures; asserting on the total would be asserting on a sum.
    pool_only = [item for item in plan["items"] if item["position"] is None]
    assert len(pool_only) <= 2


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


def test_an_anchor_the_index_does_not_hold_is_absent_rather_than_approximated():
    index = (track("Alder", "Anchor Work", "8A", path="/library/orig.flac"),)
    assert setbuild_cli.anchor_in_index(Path("/library/elsewhere.flac"), index) is None


def test_a_relative_anchor_is_taken_against_the_library_and_not_the_process(tmp_path):
    root = tmp_path / "library"
    root.mkdir()
    assert setbuild_cli.anchor_path("Music/x.flac", root) == root / "Music" / "x.flac"


def test_an_anchor_that_walks_out_of_the_library_is_refused(tmp_path):
    from cratekit.core.cause import CratekitError

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

    def put(artist, title, key, bpm, *, energy=None, vox=None, name=None) -> Path:
        head = f"{key} - {bpm:g} - {title}"
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
        "sequence": 0,
        "payload_version": setbuilder.PAYLOAD_VERSION,
        "anchor": document["data"]["totals"]["anchor"],
    }
    assert document["data"]["digest"], "an empty plan still has an identity"


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
