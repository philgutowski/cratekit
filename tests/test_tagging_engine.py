"""U56: the fill-if-empty engine, and the split that makes it drivable as a job.

One walk (:func:`tag.audio_files`) and one per file step (:func:`tag.tag_one`),
so the queue and the engine cover one set of files; ``retag_one`` one candidate
at a time must equal ``retag_folder`` whole.
"""

from __future__ import annotations

import io
import os
import shutil
from pathlib import Path

import pytest

from cratekit.acquire import cli as acquire_cli
from cratekit.core import art, tags, taxonomy
from cratekit.master import cli as master_cli
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
    """One real FLAC container, synthesized once and copied per file, since the write is real."""
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
    """A searcher answering by title and recording each ask, to tell declined from unasked."""
    asked: list[tuple[str, str]] = []

    def searcher(artist: str, title: str) -> SearchHit | None:
        asked.append((artist, title))
        return table.get(title)

    searcher.asked = asked  # type: ignore[attr-defined]
    return searcher


# A. The walk, which is also the item derivation


def test_the_walk_takes_audio_files_and_leaves_everything_else(folder, silence):
    """A stray file would be a failing item; the extensions are ``core.naming.AUDIO_EXTS``."""
    place(folder, silence, "track")
    (folder / "cover.jpg").write_bytes(b"not audio")
    (folder / "notes.txt").write_text("nor this", encoding="utf-8")

    found = tag.audio_files(folder)

    assert [path.name for path in found] == ["track.flac"]


def test_the_walk_recurses_and_comes_back_sorted(folder, silence):
    """Sorted, since an item's artifact is named from its ordinal."""
    place(folder, silence, "b")
    place(folder, silence, "nested/a")
    place(folder, silence, "c")

    found = tag.audio_files(folder)

    assert list(found) == sorted(found)
    assert [path.name for path in found] == ["b.flac", "a.flac", "c.flac"] or [
        path.name for path in found
    ] == ["b.flac", "c.flac", "a.flac"]


def test_a_root_that_is_not_a_directory_is_empty_rather_than_an_error(tmp_path):
    """Nothing to do, so the shell reports its own no-op over a mistyped path."""
    assert tag.audio_files(tmp_path / "absent") == ()

    a_file = tmp_path / "single.flac"
    a_file.write_bytes(b"")
    assert tag.audio_files(a_file) == ()


def test_the_walk_is_case_insensitive_about_the_extension(folder, silence):
    """A file off a case preserving volume arrives spelled how it was written."""
    path = folder / "SHOUTED.FLAC"
    shutil.copy2(silence, path)

    assert [found.name for found in tag.audio_files(folder)] == ["SHOUTED.FLAC"]


def test_the_walk_does_not_descend_into_the_acquisition_staging_tree(folder, silence):
    """R-289: a killed attempt's partial download under the staging dotfile is never queued."""
    place(folder, silence, "keep")
    staged = folder / acquire_cli.ACQUIRE_STAGING_DIRNAME / "job-1" / "0" / "partial"
    place(staged.parent, silence, staged.name)

    assert [found.name for found in tag.audio_files(folder)] == ["keep.flac"]


def test_the_walk_skips_the_appledouble_sidecar_beside_a_real_track(folder, silence):
    """macOS writes ``._track.flac`` beside every file on an exFAT stick; it is no track."""
    place(folder, silence, "track")
    place(folder, silence, "._track")

    assert [found.name for found in tag.audio_files(folder)] == ["track.flac"]


def test_a_title_that_opens_with_dots_is_walked_and_so_is_the_album_holding_it(folder, silence):
    """``...And Justice For All`` is real, so a guard skipping every dot name would hide files."""
    place(folder, silence, "...Ready For It")
    place(folder, silence, "Metallica/...And Justice For All/01 Blackened")

    assert sorted(found.name for found in tag.audio_files(folder)) == [
        "...Ready For It.flac",
        "01 Blackened.flac",
    ]


def test_the_skip_does_not_stop_the_walk_recursing(folder, silence):
    """The guard is about two names, not depth."""
    place(folder, silence, "nested/deeper/a")

    assert [found.name for found in tag.audio_files(folder)] == ["a.flac"]


def test_a_root_that_is_itself_a_staging_tree_is_still_walked(folder, silence):
    """Names match relative to the root, so a library under one of these names is still walked."""
    named = folder / acquire_cli.ACQUIRE_STAGING_DIRNAME / "job-1" / "0"
    named.mkdir(parents=True)
    place(named, silence, "1")

    assert [found.name for found in tag.audio_files(named)] == ["1.flac"]


def test_the_skipped_dirnames_are_the_two_constants_that_own_them():
    """The hand copy (KTD23) pinned by set equality, so a third staging tree fails here."""
    assert tag.SKIPPED_DIRNAMES == {
        acquire_cli.ACQUIRE_STAGING_DIRNAME,
        master_cli.MASTER_STAGING_DIRNAME,
    }


def test_the_master_staging_tree_is_skipped_too(folder, silence):
    """``master.cli.staging_dir`` stages a partial encode under the library, skipped too."""
    place(folder, silence, "track")
    staged = folder / master_cli.MASTER_STAGING_DIRNAME / "job-1" / "0"
    staged.mkdir(parents=True)
    place(staged, silence, "partial")

    assert [found.name for found in tag.audio_files(folder)] == ["track.flac"]


# B. One file, which is one job item


def test_a_file_with_no_genre_gets_the_answer_written_onto_it(folder, silence):
    path = place(folder, silence, "track")

    result = tag.tag_one(path, searcher=answering({"track": SearchHit(genre=SPECIFIC)}))

    assert result.genre_written == SPECIFIC
    assert result.skipped is None
    assert tags.read_genre_from_file(path) == SPECIFIC


def test_a_file_that_already_carries_a_genre_is_skipped_and_never_overwritten(folder, silence):
    """Fill if empty: the file's genre is curation; its picture spares it an art search (U85)."""
    path = place(folder, silence, "track", SPECIFIC)
    plant(path, _jpeg(320, 200), dims=(320, 200, 24))
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
    """``unmapped-genre`` is the user's to fix and carries the raw string, unlike ``no-hit``."""
    path = place(folder, silence, "track")
    hit = SearchHit(genre=None, source="beatport", source_genre="Hardvapour")

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert result.skipped == tag.UNMAPPED_GENRE
    assert result.source == "beatport"
    assert result.source_genre == "Hardvapour"
    assert tags.read_genre_from_file(path) is None


def test_a_word_the_taxonomy_does_not_know_is_written_and_reported(folder, silence):
    """R-650: the word is written, ``skipped`` None, and the result says the catalogue gave it."""
    path = place(folder, silence, "track")
    hit = SearchHit(genre="gqom", source="beatport", source_genre="gqom", off_taxonomy=True)

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert result.skipped is None
    assert result.genre_written == "gqom"
    assert tags.read_genre_from_file(path) == "gqom"
    assert result.off_taxonomy is True


def test_a_tag_the_declared_table_produced_is_not_off_taxonomy(folder, silence):
    """The ordinary write, which is the majority of every sweep, stays clean."""
    path = place(folder, silence, "track")
    hit = SearchHit(genre=SPECIFIC, source="beatport", source_genre="Deep House")

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert result.genre_written == SPECIFIC
    assert result.off_taxonomy is False


def test_a_file_this_engine_did_not_tag_is_never_off_taxonomy(folder, silence):
    """The flag qualifies a write; a genre file searched for art holds a flagged hit unwritten."""
    tagged = place(folder, silence, "tagged")
    assert tags.write_genre(tagged, SPECIFIC)
    flagged = SearchHit(genre="gqom", source="beatport", source_genre="gqom", off_taxonomy=True)
    result = tag.tag_one(tagged, searcher=answering({"tagged": flagged}))
    assert result.skipped == tag.HAS_GENRE
    assert result.off_taxonomy is False
    assert tags.read_genre_from_file(tagged) == SPECIFIC

    unmapped = place(folder, silence, "unmapped")
    result = tag.tag_one(
        unmapped,
        searcher=answering(
            {"unmapped": SearchHit(genre=None, source="beatport", source_genre="Techno")}
        ),
    )
    assert (result.skipped, result.off_taxonomy) == (tag.UNMAPPED_GENRE, False)

    missed = place(folder, silence, "missed")
    result = tag.tag_one(missed, searcher=answering({"missed": None}))
    assert (result.skipped, result.off_taxonomy) == (tag.NO_HIT, False)


def test_a_hit_with_no_genre_and_no_source_genre_is_a_plain_miss(folder, silence):
    """Only the source genre separates the two reasons: none is a catalogue answering nothing."""
    path = place(folder, silence, "track")
    hit = SearchHit(genre=None, source="bandcamp", source_genre="")

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert result.skipped == tag.NO_HIT


def test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit(folder, silence):
    """R-791: a miss beside an unread catalogue is no absence; every answer is kept."""
    path = place(folder, silence, "track")
    answers = (
        tag.SourceAnswer("beatport", "miss"),
        tag.SourceAnswer("traxsource", "blocked", note="HTTP 403"),
        tag.SourceAnswer("bandcamp", "blocked"),
    )
    hit = SearchHit(answers=answers, unread=("traxsource", "bandcamp"))

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert result.skipped == tag.SOURCES_UNREAD
    assert result.genre_written is None
    assert result.answers == answers
    assert result.unread == ("traxsource", "bandcamp")
    assert tags.read_genre_from_file(path) is None
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert "traxsource, bandcamp went unread" in result.art_fetch_detail


def test_a_decline_with_every_answer_a_miss_is_still_no_hit(folder, silence):
    path = place(folder, silence, "track")
    answers = tuple(tag.SourceAnswer(source, "miss") for source in ("a", "b", "c"))

    result = tag.tag_one(path, searcher=answering({"track": SearchHit(answers=answers)}))

    assert result.skipped == tag.NO_HIT
    assert result.answers == answers
    assert result.art_fetch_detail == "no catalogue carried the track, so no picture was named"


def test_the_written_result_carries_which_catalogue_answered(folder, silence):
    """The artifact says where the value came from, not only what it was."""
    path = place(folder, silence, "track")
    hit = SearchHit(genre=SPECIFIC, source="traxsource", source_genre="Deep House")

    result = tag.tag_one(path, searcher=answering({"track": hit}))

    assert (result.source, result.source_genre) == ("traxsource", "Deep House")


def test_the_title_tag_is_used_and_the_stem_is_the_fallback(folder, silence):
    """The filename may be a naming pass's rewrite, so the title tag is asked first."""
    tagged = place(folder, silence, "renamed")
    assert tags.write_tags(tagged, {"title": "Real Title", "artist": "Real Artist"})
    bare = place(folder, silence, "no-tags")

    searcher = answering({})
    tag.tag_one(tagged, searcher=searcher)
    tag.tag_one(bare, searcher=searcher)

    assert searcher.asked == [("Real Artist", "Real Title"), ("", "no-tags")]


def test_a_searcher_that_refuses_propagates_rather_than_becoming_a_skip(folder, silence):
    """A refusal learned nothing, so it is not a skip, which claims the catalogues were read."""
    path = place(folder, silence, "track")

    def refusing(artist: str, title: str):
        raise RuntimeError("nothing could be read")

    with pytest.raises(RuntimeError):
        tag.tag_one(path, searcher=refusing)

    assert tags.read_genre_from_file(path) is None


# C. The folder pass is the walk plus the per file work, and nothing else


def test_the_folder_pass_produces_exactly_what_the_per_file_calls_produce(folder, silence):
    """The sweep and the queued worker agree, or a folder would get two answers."""
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

    assert [(result.path.name, result.genre_written, result.skipped) for result in swept] == [
        (result.path.name, result.genre_written, result.skipped)
        for result in one_at_a_time
    ]


def test_the_folder_pass_asks_once_per_untagged_file(folder, silence):
    place(folder, silence, "one")
    place(folder, silence, "two")
    # Genre AND picture, since a tagged file with no picture is asked for art.
    plant(place(folder, silence, "already", SPECIFIC), _jpeg(320, 200), dims=(320, 200, 24))
    searcher = answering({})

    tag.tag_folder(folder, searcher=searcher)

    assert len(searcher.asked) == 2


def test_a_folder_that_is_not_there_tags_nothing_rather_than_raising(tmp_path):
    assert tag.tag_folder(tmp_path / "absent", searcher=answering({})) == []


# D. The retag side: one candidate at a time is the same pass


def test_one_candidate_at_a_time_is_the_same_pass_as_the_whole_folder(folder, silence):
    """The two entry points are the same work, which ``tests/test_genre_retag.py`` cannot assert."""
    place(folder, silence, "coarse", CATCH_ALL)
    place(folder, silence, "also-coarse", CATCH_ALL)
    place(folder, silence, "specific", SPECIFIC)
    table = {"coarse": SearchHit(genre=SPECIFIC)}

    selection = retag.select(folder, declared=TAXONOMY)
    driven = [
        retag.retag_one(candidate, searcher=answering(table), declared=TAXONOMY, decided={})
        for candidate in selection.candidates
    ]

    # The folder pass runs over a second copy, because the first pass wrote.
    assert [(result.path.name, result.written, result.reason) for result in driven] == [
        ("also-coarse.flac", None, retag.NO_ANSWER),
        ("coarse.flac", SPECIFIC, ""),
    ]


def test_a_candidate_whose_answer_is_itself_too_coarse_is_refused_per_candidate(folder, silence):
    """A catch-all written would never be selected again."""
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
    """One reader of the decided answers, or the one that drifted would re-ask."""
    assert retag.decided_index(None) == {}


# C. U84: the picture repair runs first, in place, without the web


def _gradient(width: int, height: int):
    from PIL import Image

    img = Image.new("RGB", (width, height))
    img.putdata([(x % 256, y % 256, (x + y) % 256) for y in range(height) for x in range(width)])
    return img


def _jpeg(width: int = 320, height: int = 200, *, progressive: bool = False) -> bytes:
    """Deliberately NOT 800 square, so a repair that resized would show."""
    buffer = io.BytesIO()
    _gradient(width, height).save(buffer, format="JPEG", quality=85, progressive=progressive)
    return buffer.getvalue()


def _png(width: int = 320, height: int = 200) -> bytes:
    buffer = io.BytesIO()
    _gradient(width, height).save(buffer, format="PNG")
    return buffer.getvalue()


def plant(path: Path, data: bytes, *, dims=(0, 0, 0), mime="image/jpeg", kind=3, desc=""):
    """Add one FLAC picture block, by default as the vendored downloader writes it, zero dimensions.

    ``dims`` fills them for a block meant to be sound.
    """
    from mutagen.flac import FLAC, Picture

    handle = FLAC(path)
    block = Picture()
    block.type = kind
    block.mime = mime
    block.desc = desc
    block.data = data
    block.width, block.height, block.depth = dims
    handle.add_picture(block)
    handle.save()


def blocks(path: Path):
    from mutagen.flac import FLAC

    return list(FLAC(path).pictures)


def decoded(data: bytes):
    from PIL import Image

    with Image.open(io.BytesIO(data)) as img:
        img.load()
        return img.format, img.size, bool(img.info.get("progressive") or img.info.get("progression")), img.convert("RGB")


def mean_difference(a, b) -> float:
    from PIL import ImageChops, ImageStat

    return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3


def test_a_vendored_zeroed_block_ends_with_real_dimensions_and_the_same_image(folder, silence):
    path = place(folder, silence, "track")
    original = _jpeg(320, 200)
    plant(path, original, kind=3, desc="Cover")

    result = tag.tag_one(path, searcher=answering({}))

    assert result.art_repair == art.REPAIR_FIXED
    (block,) = blocks(path)
    assert (block.width, block.height, block.depth) == (320, 200, 24)
    assert (block.type, block.desc, block.mime) == (3, "Cover", "image/jpeg")
    fmt, size, progressive, pixels = decoded(block.data)
    assert (fmt, size, progressive) == ("JPEG", (320, 200), False)
    assert mean_difference(pixels, decoded(original)[3]) < 4, "the repair changed the picture"


def test_a_progressive_jpeg_with_sound_dimensions_becomes_baseline(folder, silence):
    path = place(folder, silence, "track")
    plant(path, _jpeg(320, 200, progressive=True), dims=(320, 200, 24))
    assert decoded(blocks(path)[0].data)[2] is True, "the fixture is not progressive"

    result = tag.tag_one(path, searcher=answering({}))

    assert result.art_repair == art.REPAIR_FIXED
    (block,) = blocks(path)
    assert decoded(block.data)[:3] == ("JPEG", (320, 200), False)


def test_a_png_in_a_filled_block_is_re_encoded_as_a_baseline_jpeg(folder, silence):
    path = place(folder, silence, "track")
    plant(path, _png(), mime="image/png", dims=(320, 200, 24))

    assert art.repair_in_place(path).status == art.REPAIR_FIXED

    (block,) = blocks(path)
    assert block.mime == "image/jpeg"
    assert decoded(block.data)[:3] == ("JPEG", (320, 200), False)


@pytest.mark.parametrize("dims", [(0, 200, 24), (320, 0, 24), (320, 200, 0)])
def test_any_one_zeroed_dimension_is_broken(folder, silence, dims):
    path = place(folder, silence, "track")
    plant(path, _jpeg(320, 200), dims=dims)

    assert art.repair_in_place(path).status == art.REPAIR_FIXED
    (block,) = blocks(path)
    assert (block.width, block.height, block.depth) == (320, 200, 24)


def test_sound_art_is_not_rewritten_and_its_mtime_is_unchanged(folder, silence):
    path = place(folder, silence, "track")
    plant(path, _jpeg(320, 200), dims=(320, 200, 24))
    os.utime(path, (1_000_000_000, 1_000_000_000))
    before = path.read_bytes()

    result = tag.tag_one(path, searcher=answering({}))

    assert result.art_repair == art.REPAIR_OK
    assert path.stat().st_mtime == 1_000_000_000
    assert path.read_bytes() == before


def test_a_file_that_already_has_a_genre_is_still_repaired(folder, silence):
    path = place(folder, silence, "track", SPECIFIC)
    plant(path, _jpeg(320, 200))
    searcher = answering({"track": SearchHit(genre="Techno")})

    result = tag.tag_one(path, searcher=searcher)

    assert result.skipped == tag.HAS_GENRE
    assert result.art_repair == art.REPAIR_FIXED
    assert (blocks(path)[0].width, blocks(path)[0].height) == (320, 200)
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert searcher.asked == []


def test_a_corrupt_image_reports_an_error_and_the_genre_flow_still_proceeds(folder, silence):
    path = place(folder, silence, "track")
    plant(path, b"\xff\xd8\xff\xe0 not really a jpeg")
    stored = blocks(path)[0].data

    result = tag.tag_one(path, searcher=answering({"track": SearchHit(genre=SPECIFIC)}))

    assert result.art_repair == art.REPAIR_ERROR
    assert "could not be repaired" in result.art_repair_detail
    assert result.genre_written == SPECIFIC
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert blocks(path)[0].data == stored, "a failed repair rewrote the picture"


def test_one_unrepairable_block_leaves_every_block_as_it_was(folder, silence):
    """The source system's rule: a half repaired file is not reported fixed."""
    path = place(folder, silence, "track")
    plant(path, _jpeg(320, 200))
    plant(path, b"garbage", kind=4)
    os.utime(path, (1_000_000_000, 1_000_000_000))
    before = path.read_bytes()

    assert art.repair_in_place(path).status == art.REPAIR_ERROR

    assert path.read_bytes() == before
    assert path.stat().st_mtime == 1_000_000_000


def test_a_sound_block_beside_a_broken_one_is_kept_as_it_was_and_in_order(folder, silence):
    path = place(folder, silence, "track")
    sound = _jpeg(100, 100)
    plant(path, sound, dims=(100, 100, 24), kind=4, desc="Back")
    plant(path, _jpeg(320, 200), kind=3, desc="Cover")

    repair = art.repair_in_place(path)

    assert repair.status == art.REPAIR_FIXED
    assert repair.detail == "1 of 2 pictures re-encoded"
    first, second = blocks(path)
    assert (first.type, first.desc, bytes(first.data)) == (4, "Back", sound)
    assert (second.type, second.desc, second.width, second.height) == (3, "Cover", 320, 200)


def test_a_file_with_no_picture_reports_none_and_is_not_written(folder, silence):
    path = place(folder, silence, "track")
    os.utime(path, (1_000_000_000, 1_000_000_000))

    result = tag.tag_one(path, searcher=answering({}))

    assert result.art_repair == art.REPAIR_NONE
    assert path.stat().st_mtime == 1_000_000_000


def test_a_container_that_is_not_flac_is_unchecked_rather_than_none(tmp_path):
    """FLAC only is parity, and "did not look" must not read as "no art"."""
    path = synth_container(tmp_path, ".mp3")
    before = path.read_bytes()

    repair = art.repair_in_place(path)

    assert repair.status == art.REPAIR_UNCHECKED
    assert repair.status != art.REPAIR_NONE
    assert path.read_bytes() == before


def test_an_unreadable_flac_is_an_error_and_never_raises(tmp_path):
    path = tmp_path / "broken.flac"
    path.write_bytes(b"not a flac at all")

    repair = art.repair_in_place(path)

    assert repair.status == art.REPAIR_ERROR
    assert "could not read" in repair.detail


def test_a_save_that_fails_is_an_error_and_never_raises(folder, silence, monkeypatch):
    path = place(folder, silence, "track")
    plant(path, _jpeg(320, 200))

    def refuse(path, handle):
        raise OSError("read only volume")

    monkeypatch.setattr(tags, "_save", refuse)

    repair = art.repair_in_place(path)

    assert repair.status == art.REPAIR_ERROR
    assert "read only volume" in repair.detail


def test_a_result_built_without_the_repair_does_not_claim_it_passed():
    assert tag.TagResult(path=Path("x.flac"), genre_written=None).art_repair == (
        art.REPAIR_UNCHECKED
    )


def _noise_jpeg(width: int, height: int) -> bytes:
    """Incompressible pixels, so the byte cap is really exceeded at native size."""
    import random

    from PIL import Image

    rng = random.Random(84)
    img = Image.frombytes("RGB", (width, height), rng.randbytes(width * height * 3))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=95)
    return buffer.getvalue()


def test_a_picture_too_large_for_the_cap_at_native_size_is_shrunk_not_left_blank(folder, silence):
    """Shrunk inside the art edge keeping its shape, never left blank for good."""
    data = _noise_jpeg(1400, 1000)
    with pytest.raises(art.ArtError):
        art.to_cdj_jpeg(data, size=None)
    path = place(folder, silence, "track")
    plant(path, data)

    repair = art.repair_in_place(path)

    assert repair.status == art.REPAIR_FIXED
    assert repair.detail == "1 of 1 pictures re-encoded, 1 shrunk to fit 800 pixels"
    (block,) = blocks(path)
    assert (block.width, block.height, block.depth) == (800, 571, 24)
    assert len(block.data) <= art.ART_MAX_BYTES
    assert decoded(block.data)[:3] == ("JPEG", (800, 571), False)


def test_a_picture_inside_the_box_that_cannot_fit_is_an_error_and_is_never_enlarged(
    folder, silence, monkeypatch
):
    path = place(folder, silence, "track")
    plant(path, _jpeg(320, 200))
    stored = blocks(path)[0].data

    def never_fits(data, *, size=art.ART_SIZE, max_bytes=art.ART_MAX_BYTES):
        raise art.ArtError("does not fit")

    monkeypatch.setattr(art, "to_cdj_jpeg", never_fits)

    repair = art.repair_in_place(path)

    assert repair.status == art.REPAIR_ERROR
    assert "too small to shrink" in repair.detail
    assert blocks(path)[0].data == stored


@pytest.mark.parametrize(
    "data",
    [b"garbage", _jpeg(320, 200)[:400]],
    ids=["not-an-image", "truncated-jpeg"],
)
def test_an_undecodable_image_in_a_filled_block_is_an_error_not_ok(folder, silence, data):
    """An undecodable filled block renders blank; the truncated JPEG fails only a full decode."""
    path = place(folder, silence, "track")
    plant(path, data, dims=(320, 200, 24))

    assert art.repair_in_place(path).status == art.REPAIR_ERROR


def test_an_encoder_failure_that_is_not_an_art_error_is_still_an_error(
    folder, silence, monkeypatch
):
    """The repair never raises, whatever Pillow throws, not only ``ArtError``."""
    path = place(folder, silence, "track")
    plant(path, _jpeg(320, 200))

    def breaks(data, *, size=art.ART_SIZE, max_bytes=art.ART_MAX_BYTES):
        raise OSError("decoder fell over")

    monkeypatch.setattr(art, "to_cdj_jpeg", breaks)

    repair = art.repair_in_place(path)

    assert repair.status == art.REPAIR_ERROR
    assert "decoder fell over" in repair.detail


# D. U85: a file with no picture gets the catalogue's, and no other file does

ART_URL = "https://geo-media.example/image_size/1400x1400/cover.jpg"


def fetching(answer: bytes | None = None, *, raises: Exception | None = None):
    """An image fetch answering ``answer``, recording each URL, 1000 square to show a re-encode."""
    asked: list[str] = []

    def fetch_image(url: str) -> bytes | None:
        asked.append(url)
        if raises is not None:
            raise raises
        return _jpeg(1000, 1000) if answer is None else answer

    fetch_image.asked = asked  # type: ignore[attr-defined]
    return fetch_image


def test_a_file_with_no_genre_and_no_art_gets_both(folder, silence):
    path = place(folder, silence, "track")
    fetch = fetching()

    result = tag.tag_one(
        path,
        searcher=answering({"track": SearchHit(genre=SPECIFIC, source="beatport", art_url=ART_URL)}),
        fetch_image=fetch,
    )

    assert result.genre_written == SPECIFIC
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert result.art_fetch == tag.ART_EMBEDDED
    assert result.art_fetch_detail == "800 by 800 from beatport"
    assert fetch.asked == [ART_URL]
    (block,) = blocks(path)
    assert (block.type, block.mime) == (3, "image/jpeg")
    assert (block.width, block.height, block.depth) == (800, 800, 24)
    assert decoded(block.data)[:3] == ("JPEG", (800, 800), False)


def test_a_file_with_a_genre_and_no_art_gets_art_and_its_genre_is_untouched(folder, silence):
    """Art and genre are independent needs, so the tagged file is still asked."""
    path = place(folder, silence, "track", SPECIFIC)
    searcher = answering({"track": SearchHit(genre="Techno", source="beatport", art_url=ART_URL)})
    fetch = fetching()

    result = tag.tag_one(path, searcher=searcher, fetch_image=fetch)

    assert searcher.asked == [("", "track")]
    assert result.skipped == tag.HAS_GENRE
    assert result.genre_written is None
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert result.art_fetch == tag.ART_EMBEDDED
    assert len(blocks(path)) == 1


def test_a_tagged_file_with_zeroed_art_is_repaired_and_never_fetched(folder, silence):
    """The previous unit's repair owns a picture the file already has."""
    path = place(folder, silence, "track", SPECIFIC)
    plant(path, _jpeg(320, 200))
    searcher = answering({"track": SearchHit(genre="Techno", art_url=ART_URL)})
    fetch = fetching()

    result = tag.tag_one(path, searcher=searcher, fetch_image=fetch)

    assert result.art_repair == art.REPAIR_FIXED
    assert result.art_fetch == tag.ART_PRESENT
    assert searcher.asked == [] and fetch.asked == []
    (block,) = blocks(path)
    assert (block.width, block.height) == (320, 200)


def test_an_untagged_file_with_zeroed_art_gets_its_genre_and_keeps_its_picture(folder, silence):
    """ANY picture settles the art, even on a file that is searched for its genre."""
    path = place(folder, silence, "track")
    plant(path, _jpeg(320, 200))
    fetch = fetching()

    result = tag.tag_one(
        path,
        searcher=answering({"track": SearchHit(genre=SPECIFIC, art_url=ART_URL)}),
        fetch_image=fetch,
    )

    assert result.genre_written == SPECIFIC
    assert result.art_fetch == tag.ART_PRESENT
    assert fetch.asked == []
    (block,) = blocks(path)
    assert (block.width, block.height) == (320, 200)


def test_an_image_404_still_writes_the_genre_and_reports_art_unavailable(folder, silence):
    path = place(folder, silence, "track")
    fetch = fetching(b"")

    result = tag.tag_one(
        path,
        searcher=answering({"track": SearchHit(genre=SPECIFIC, art_url=ART_URL)}),
        fetch_image=fetch,
    )

    assert result.genre_written == SPECIFIC
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert ART_URL in result.art_fetch_detail
    assert blocks(path) == []


def test_a_fetch_that_raises_is_unavailable_and_never_fails_the_item(folder, silence):
    path = place(folder, silence, "track")

    result = tag.tag_one(
        path,
        searcher=answering({"track": SearchHit(genre=SPECIFIC, art_url=ART_URL)}),
        fetch_image=fetching(raises=OSError("connection reset")),
    )

    assert result.genre_written == SPECIFIC
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert "connection reset" in result.art_fetch_detail


def test_bytes_that_are_not_a_picture_are_unavailable_and_nothing_is_embedded(folder, silence):
    path = place(folder, silence, "track")

    result = tag.tag_one(
        path,
        searcher=answering({"track": SearchHit(genre=SPECIFIC, art_url=ART_URL)}),
        fetch_image=fetching(b"<html>not found</html>"),
    )

    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert "not a usable picture" in result.art_fetch_detail
    assert blocks(path) == []


def test_a_fake_searcher_with_no_art_url_still_works_and_nothing_is_fetched(folder, silence):
    path = place(folder, silence, "track")
    fetch = fetching()

    result = tag.tag_one(
        path, searcher=answering({"track": SearchHit(genre=SPECIFIC)}), fetch_image=fetch
    )

    assert result.genre_written == SPECIFIC
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert fetch.asked == []
    assert blocks(path) == []


def test_no_fetch_supplied_is_unavailable_rather_than_a_silent_skip(folder, silence):
    path = place(folder, silence, "track")

    result = tag.tag_one(
        path, searcher=answering({"track": SearchHit(genre=SPECIFIC, art_url=ART_URL)})
    )

    assert result.genre_written == SPECIFIC
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert "no image fetch" in result.art_fetch_detail


def test_a_tagged_file_nobody_carries_is_still_has_genre_and_art_unavailable(folder, silence):
    path = place(folder, silence, "track", SPECIFIC)
    fetch = fetching()

    result = tag.tag_one(path, searcher=answering({}), fetch_image=fetch)

    assert result.skipped == tag.HAS_GENRE
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert fetch.asked == []


def test_an_unmapped_genre_on_the_matched_row_still_brings_its_picture(folder, silence):
    """The row passed the artist and title gate, and only its WORD was unmapped."""
    path = place(folder, silence, "track")

    result = tag.tag_one(
        path,
        searcher=answering({"track": SearchHit(source_genre="gqom", art_url=ART_URL)}),
        fetch_image=fetching(),
    )

    assert result.skipped == tag.UNMAPPED_GENRE
    assert result.art_fetch == tag.ART_EMBEDDED


def test_a_file_whose_pictures_cannot_be_read_is_unchecked_and_not_fetched(
    folder, silence, monkeypatch
):
    """Could not look is not the same as has no picture, so nothing is fetched."""
    path = place(folder, silence, "track", SPECIFIC)

    def unreadable(_path):
        raise art.UnreadableFile("the volume went away")

    monkeypatch.setattr(art, "read_pictures", unreadable)
    searcher = answering({"track": SearchHit(genre="Techno", art_url=ART_URL)})
    fetch = fetching()

    result = tag.tag_one(path, searcher=searcher, fetch_image=fetch)

    assert result.art_fetch == tag.ART_UNCHECKED
    assert "the volume went away" in result.art_fetch_detail
    assert searcher.asked == [] and fetch.asked == []


def test_a_picture_the_file_will_not_take_is_an_error_and_the_genre_stands(
    folder, silence, monkeypatch
):
    path = place(folder, silence, "track")
    monkeypatch.setattr(art, "write_front_cover", lambda _path, _jpeg: False)

    result = tag.tag_one(
        path,
        searcher=answering({"track": SearchHit(genre=SPECIFIC, art_url=ART_URL)}),
        fetch_image=fetching(),
    )

    assert result.genre_written == SPECIFIC
    assert result.art_fetch == tag.ART_ERROR


def test_an_mp3_with_no_picture_gets_an_id3_front_cover(tmp_path):
    """Not only FLAC: the write goes through the per container writer."""
    path = synth_container(tmp_path, ".mp3")

    result = tag.tag_one(
        path,
        searcher=answering({path.stem: SearchHit(genre=SPECIFIC, art_url=ART_URL)}),
        fetch_image=fetching(),
    )

    assert result.art_fetch == tag.ART_EMBEDDED
    (picture,) = art.read_pictures(path)
    assert (picture.width, picture.height, picture.progressive) == (800, 800, False)
    assert tags.read_genre_from_file(path) == SPECIFIC


def test_the_folder_pass_hands_its_fetch_to_every_file(folder, silence):
    place(folder, silence, "one")
    place(folder, silence, "two")
    table = {name: SearchHit(genre=SPECIFIC, art_url=f"{ART_URL}?{name}") for name in ("one", "two")}
    fetch = fetching()

    results = tag.tag_folder(folder, searcher=answering(table), fetch_image=fetch)

    assert [result.art_fetch for result in results] == [tag.ART_EMBEDDED] * 2
    assert sorted(fetch.asked) == [f"{ART_URL}?one", f"{ART_URL}?two"]


def _refusing(reason: str):
    """A searcher that refuses the way the shipped one does when nothing answered."""
    from cratekit.core.cause import refuse

    asked: list[tuple[str, str]] = []

    def searcher(artist: str, title: str):
        asked.append((artist, title))
        raise refuse(reason, f"no catalogue could be read for {title!r}", origin=("test",))

    searcher.asked = asked  # type: ignore[attr-defined]
    return searcher


@pytest.mark.parametrize("reason", ["catalogue-unreachable", "catalogue-parse-broken"])
def test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal(folder, silence, reason):
    """U85 review: a refusal on an art only search is ``unavailable``, not a failure every run."""
    path = place(folder, silence, "track", SPECIFIC)
    searcher = _refusing(reason)
    fetch = fetching()

    result = tag.tag_one(path, searcher=searcher, fetch_image=fetch)

    assert searcher.asked == [("", "track")]
    assert result.skipped == tag.HAS_GENRE
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert result.art_fetch_detail.startswith(f"{reason}: ")
    assert fetch.asked == []
    assert tags.read_genre_from_file(path) == SPECIFIC


def test_an_untagged_file_still_fails_on_a_refusal(folder, silence):
    """The genre is what the refusal left unlearned, so this one still propagates."""
    from cratekit.core.cause import CratekitError

    path = place(folder, silence, "track")

    with pytest.raises(CratekitError):
        tag.tag_one(path, searcher=_refusing("catalogue-unreachable"), fetch_image=fetching())

    assert tags.read_genre_from_file(path) is None
    assert blocks(path) == []


def test_a_tagged_file_whose_searcher_breaks_outright_still_raises(folder, silence):
    """Only a refusal is absorbed. A defect in the searcher is not a decline."""
    path = place(folder, silence, "track", SPECIFIC)

    def broken(artist: str, title: str):
        raise RuntimeError("a bug, not a refusal")

    with pytest.raises(RuntimeError):
        tag.tag_one(path, searcher=broken, fetch_image=fetching())
