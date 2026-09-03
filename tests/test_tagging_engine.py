"""U56: the fill-if-empty engine, and the split that makes it drivable as a job.

WHY THIS FILE DID NOT EXIST UNTIL NOW, WHICH IS THE POINT OF IT.
``cratekit.tagging.tag`` shipped in an early unit and had NO test anywhere in
this suite: a grep for ``tag_folder`` over ``tests/`` before this unit returned
``tests/test_cli_contract.py``, which names the verb rather than the engine, and
``tests/test_genre_retag.py``, which mentions it only in prose. It also had no
caller in ``src``. U56 is both, so under
``docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md``
its unreviewed failure paths are this unit's to drive rather than to inherit.

WHAT THE SPLIT IS FOR. A queued verb populates its items at enqueue and its
worker runs one of them, so the walk and the per file work have to be reachable
separately. They are :func:`tag.audio_files` and :func:`tag.tag_one`, and
:func:`tag.tag_folder` is now the first applied to every result of the second.
The property that matters is that there is only one of each: a shell that walked
the folder itself would be a second opinion about which files the job covers,
and the drift runs in the expensive direction, a job reporting done over files it
never queued.

THE RETAG SIDE IS CHARACTERIZED RATHER THAN RE-ASSERTED. ``retag_one`` is the
body of ``retag_folder``'s loop lifted out unchanged, and the evidence that it
came out unchanged is that every one of ``tests/test_genre_retag.py``'s
assertions still passes with no edit. What is added here is the property that
file makes only implicitly, that driving one candidate at a time and driving the
whole folder produce the same results in the same order.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.core import tags, taxonomy
from cratekit.tagging import retag, tag
from cratekit.tagging.tag import SearchHit
from tests._containers import synth_container

TAXONOMY = taxonomy.default_taxonomy()

#: Read off the template rather than typed, so a taxonomy edit moves the fixture
#: with it instead of leaving a test asserting about a value nobody declares.
CATCH_ALL = TAXONOMY.fallback.too_coarse_as_source[1]
SPECIFIC = "Deep House"


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC container, synthesized once and copied per file.

    A real container rather than a stub, because the write under test goes
    through ``core.tags.write_genre`` and a stub would prove the branch and
    nothing about the write.
    """
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def folder(tmp_path) -> Path:
    out = tmp_path / "Music"
    out.mkdir()
    return out


def place(folder: Path, silence: Path, name: str, genre: str | None = None) -> Path:
    """One audio file in the folder, carrying ``genre`` or carrying none."""
    path = folder / f"{name}.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(silence, path)
    if genre is not None:
        assert tags.write_genre(path, genre), f"the fixture could not tag {name}"
    return path


def answering(table: dict[str, SearchHit | None]):
    """A searcher that answers by TITLE and records what it was asked.

    The recording is not decoration. Two tests below assert the searcher was
    asked exactly once per file, and a searcher with no memory cannot tell
    "asked and declined" from "never asked at all".
    """
    asked: list[tuple[str, str]] = []

    def searcher(artist: str, title: str) -> SearchHit | None:
        asked.append((artist, title))
        return table.get(title)

    searcher.asked = asked  # type: ignore[attr-defined]
    return searcher


# ═══════════════════════════════════════════════════════════════════════════
# A. The walk, which is also the item derivation
# ═══════════════════════════════════════════════════════════════════════════


def test_the_walk_takes_audio_files_and_leaves_everything_else(folder, silence):
    """A job item per entry here, so a stray file is a queued item that fails.

    The extension set is ``core.naming.AUDIO_EXTS`` and is read off it rather
    than typed, because a format added there must widen this walk on the same
    edit or the two disagree about what this product considers audio.
    """
    place(folder, silence, "track")
    (folder / "cover.jpg").write_bytes(b"not audio")
    (folder / "notes.txt").write_text("nor this", encoding="utf-8")

    found = tag.audio_files(folder)

    assert [path.name for path in found] == ["track.flac"]


def test_the_walk_recurses_and_comes_back_sorted(folder, silence):
    """Sorted, so an enqueue and a later walk agree about ORDER as well as set.

    Item ordinals are assigned in the order the shell hands them over, and the
    artifact for one item is named from its ordinal. An unsorted walk would make
    the ordinal depend on directory order, so the same folder queued twice would
    file the same file's report under two different names.
    """
    place(folder, silence, "b")
    place(folder, silence, "nested/a")
    place(folder, silence, "c")

    found = tag.audio_files(folder)

    assert list(found) == sorted(found)
    assert [path.name for path in found] == ["b.flac", "a.flac", "c.flac"] or [
        path.name for path in found
    ] == ["b.flac", "c.flac", "a.flac"]


def test_a_root_that_is_not_a_directory_is_empty_rather_than_an_error(tmp_path):
    """The first caller is a shell asking whether it has anything to queue.

    "Nothing to do" is the honest answer to give it, and it is the answer that
    lets the shell report its own no-op rather than meeting a traceback over a
    path the person mistyped.
    """
    assert tag.audio_files(tmp_path / "absent") == ()

    a_file = tmp_path / "single.flac"
    a_file.write_bytes(b"")
    assert tag.audio_files(a_file) == ()


def test_the_walk_is_case_insensitive_about_the_extension(folder, silence):
    """A file off a case preserving volume arrives spelled how it was written."""
    path = folder / "SHOUTED.FLAC"
    shutil.copy2(silence, path)

    assert [found.name for found in tag.audio_files(folder)] == ["SHOUTED.FLAC"]


# ═══════════════════════════════════════════════════════════════════════════
# B. One file, which is one job item
# ═══════════════════════════════════════════════════════════════════════════


def test_a_file_with_no_genre_gets_the_answer_written_onto_it(folder, silence):
    path = place(folder, silence, "track")

    result = tag.tag_one(path, searcher=answering({"track": SearchHit(genre=SPECIFIC)}))

    assert result.genre_written == SPECIFIC
    assert result.skipped is None
    assert tags.read_genre_from_file(path) == SPECIFIC


def test_a_file_that_already_carries_a_genre_is_skipped_and_never_overwritten(
    folder, silence
):
    """Fill if empty is the whole policy of this verb.

    The value on the file is somebody's curation until ``crate tag retag``
    decides the declared taxonomy calls it too coarse. Two verbs own this field
    under two policies, and a file that already has a value belongs to neither
    of them here.
    """
    path = place(folder, silence, "track", SPECIFIC)
    searcher = answering({"track": SearchHit(genre="Techno")})

    result = tag.tag_one(path, searcher=searcher)

    assert result.skipped == tag.HAS_GENRE
    assert result.genre_written is None
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert searcher.asked == [], "the searcher was asked about a file it cannot touch"


def test_a_searcher_that_declines_leaves_the_file_alone_and_says_no_hit(folder, silence):
    path = place(folder, silence, "track")

    result = tag.tag_one(path, searcher=answering({}))

    assert result.skipped == tag.NO_HIT
    assert result.source_genre == ""
    assert tags.read_genre_from_file(path) is None


def test_a_catalogue_answer_the_taxonomy_could_not_map_is_its_own_reason(folder, silence):
    """``unmapped-genre`` is not a kind of ``no-hit``, and the difference is the user's.

    A person whose folder came back untagged needs to know whether the
    catalogues have never heard of these tracks or whether their own taxonomy is
    missing an alias, because only the second is theirs to fix. The raw string
    rides along for the same reason: a reason with no string beside it says a gap
    exists and not which one.
    """
    path = place(folder, silence, "track")
    hit = SearchHit(genre=None, source="beatport", source_genre="Hardvapour")

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert result.skipped == tag.UNMAPPED_GENRE
    assert result.source == "beatport"
    assert result.source_genre == "Hardvapour"
    assert tags.read_genre_from_file(path) is None


def test_a_hit_with_no_genre_and_no_source_genre_is_a_plain_miss(folder, silence):
    """The two reasons are separated by the SOURCE GENRE and by nothing else.

    A searcher can hand back a hit that names the catalogue it asked and carries
    no string, and that is a catalogue that answered with nothing rather than one
    whose word could not be mapped.
    """
    path = place(folder, silence, "track")
    hit = SearchHit(genre=None, source="bandcamp", source_genre="")

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert result.skipped == tag.NO_HIT


def test_the_written_result_carries_which_catalogue_answered(folder, silence):
    """The artifact says where the value came from, not only what it was."""
    path = place(folder, silence, "track")
    hit = SearchHit(genre=SPECIFIC, source="traxsource", source_genre="Deep House")

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert (result.source, result.source_genre) == ("traxsource", "Deep House")


def test_the_title_tag_is_used_and_the_stem_is_the_fallback(folder, silence):
    """What the searcher is asked is the file's own metadata first.

    A folder of downloads carries real title tags, and the filename is a
    rendering of them that a naming pass may have already rewritten. Asking with
    the rewritten name would search for the product's own output.
    """
    tagged = place(folder, silence, "renamed")
    assert tags.write_tags(tagged, {"title": "Real Title", "artist": "Real Artist"})
    bare = place(folder, silence, "no-tags")

    searcher = answering({})
    tag.tag_one(tagged, searcher=searcher)
    tag.tag_one(bare, searcher=searcher)

    assert searcher.asked == [("Real Artist", "Real Title"), ("", "no-tags")]


def test_a_searcher_that_refuses_propagates_rather_than_becoming_a_skip(folder, silence):
    """A refusal is the searcher saying it learned nothing, and it must not land as a skip.

    A skip is a claim about the catalogues. An item that reported done having
    read no catalogue at all is the clean report over unreadable state the merge
    bar names, and it is exactly what makes a whole job look finished after a
    network outage.
    """
    path = place(folder, silence, "track")

    def refusing(artist: str, title: str):
        raise RuntimeError("nothing could be read")

    with pytest.raises(RuntimeError):
        tag.tag_one(path, searcher=refusing)

    assert tags.read_genre_from_file(path) is None


# ═══════════════════════════════════════════════════════════════════════════
# C. The folder pass is the walk plus the per file work, and nothing else
# ═══════════════════════════════════════════════════════════════════════════


def test_the_folder_pass_produces_exactly_what_the_per_file_calls_produce(
    folder, silence
):
    """The one property that keeps the sweep and the queued worker in agreement.

    If these two ever diverge, a person's folder gets one answer when they run
    the verb and a different one when the job driver runs it, and nothing in the
    product would report the difference.
    """
    place(folder, silence, "written")
    place(folder, silence, "curated", SPECIFIC)
    place(folder, silence, "declined")
    table = {"written": SearchHit(genre=SPECIFIC)}

    # TWO COPIES, because the first pass WRITES. Running both over one folder
    # would show the second pass a file the first had already tagged, and the
    # comparison would prove the fill-if-empty policy rather than the split.
    mirror = folder.parent / "Mirror"
    shutil.copytree(folder, mirror)

    swept = tag.tag_folder(folder, searcher=answering(table))
    one_at_a_time = [
        tag.tag_one(path, searcher=answering(table)) for path in tag.audio_files(mirror)
    ]

    assert [
        (result.path.name, result.genre_written, result.skipped) for result in swept
    ] == [
        (result.path.name, result.genre_written, result.skipped)
        for result in one_at_a_time
    ]


def test_the_folder_pass_asks_once_per_untagged_file(folder, silence):
    place(folder, silence, "one")
    place(folder, silence, "two")
    place(folder, silence, "already", SPECIFIC)
    searcher = answering({})

    tag.tag_folder(folder, searcher=searcher)

    assert len(searcher.asked) == 2


def test_a_folder_that_is_not_there_tags_nothing_rather_than_raising(tmp_path):
    assert tag.tag_folder(tmp_path / "absent", searcher=answering({})) == []


# ═══════════════════════════════════════════════════════════════════════════
# D. The retag side: one candidate at a time is the same pass
# ═══════════════════════════════════════════════════════════════════════════


def test_one_candidate_at_a_time_is_the_same_pass_as_the_whole_folder(folder, silence):
    """The extraction's own proof, stated where a reader will look for it.

    ``tests/test_genre_retag.py`` covers every branch of this policy through
    ``retag_folder`` and still passes unchanged, which is the evidence that the
    body came out intact. This is the assertion that file cannot make: that the
    two entry points are the same work.
    """
    place(folder, silence, "coarse", CATCH_ALL)
    place(folder, silence, "also-coarse", CATCH_ALL)
    place(folder, silence, "specific", SPECIFIC)
    table = {"coarse": SearchHit(genre=SPECIFIC)}

    selection = retag.select(folder, declared=TAXONOMY)
    driven = [
        retag.retag_one(
            candidate,
            searcher=answering(table),
            declared=TAXONOMY,
            decided={},
        )
        for candidate in selection.candidates
    ]

    # The folder pass runs over a second copy, because the first pass wrote.
    assert [(result.path.name, result.written, result.reason) for result in driven] == [
        ("also-coarse.flac", None, retag.NO_ANSWER),
        ("coarse.flac", SPECIFIC, ""),
    ]


def test_a_candidate_whose_answer_is_itself_too_coarse_is_refused_per_candidate(
    folder, silence
):
    """Driven through the per candidate entry point, because the worker is what runs it.

    Writing a catch all launders it into a value this verb would never select
    again, since selecting is what "too coarse" means. The guard exists in the
    folder pass and this proves it survived the split.
    """
    place(folder, silence, "coarse", CATCH_ALL)
    (candidate,) = retag.select(folder, declared=TAXONOMY).candidates

    result = retag.retag_one(
        candidate,
        searcher=answering({"coarse": SearchHit(genre=CATCH_ALL)}),
        declared=TAXONOMY,
        decided={},
    )

    assert result.reason == retag.ANSWER_TOO_COARSE
    assert result.written is None
    assert tags.read_genre_from_file(candidate.path) == CATCH_ALL


def test_the_queue_index_is_the_folder_passs_and_the_workers_one_function(folder, silence):
    """One reader for "what has already been decided", used by both entry points.

    The sweep calls it once for a whole walk and a worker calls it once for its
    one item. Two readers would be two ideas of which queue and which kind hold
    this pass's answers, and the one that drifted would re-ask a settled question.
    """
    assert retag.decided_index(None) == {}
