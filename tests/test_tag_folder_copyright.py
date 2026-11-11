"""U240: tag folder tags each file by the registered label its copyright line names.

The attended label pass of 2026-11-10 measured the cost this unit removes.
``tag folder`` over 106 staged files of five registered labels failed every
item ``catalogue-unreachable``: Beatport answered 403, Traxsource 403 and
Bandcamp a client challenge, so no catalogue was left. Every label carried a
genre in the registry, and ``tag folder --label`` would have tagged a folder of
one label with no catalogue asked, but the batch was five labels in one folder,
so a person split it by hand. The label go's tail queues ``tag folder`` with no
``--label`` at all.

So a file with no label tag, swept with no ``--label``, is matched to the
registry by its copyright line, the line the downloader writes on every file
it delivers. Exactly one registered label named, and it carries a genre: the
file takes that genre and no catalogue is asked. Anything else is asked of the
catalogues as before.

Four sections: the copyright line read off each container, the engine's tier,
the sweep through the real dispatcher, and the label go's tail step.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.cli import tail
from cratekit.core import config, jobs, tags
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.tagging import artifacts, searchers, tag
from cratekit.tagging import cli as tag_cli
from cratekit.tagging.tag import LabelAnswer, SearchHit
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_tag_workers import bound, item_causes, item_states, resume_argv, tag_job
from tests.test_tagging_engine import SPECIFIC, _jpeg, answering, plant

RAWAX = "Rawax"
ATIPIC = "Atipic"
CRONOS = "Cronos Barac"
MINIMAL = "Rominimal"
PROGRESSIVE = "Progressive House"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """A configured machine on the full profile, which turns the label verbs on."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    data = valid_data(library)
    data["profile"] = {"name": "full"}
    built = config.from_dict(data)
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def folder(tmp_path) -> Path:
    out = tmp_path / "staging"
    out.mkdir()
    return out


def downloaded(
    folder: Path,
    silence: Path,
    name: str,
    copyright: str | None,
    *,
    label: str | None = None,
    genre: str | None = None,
) -> Path:
    """One FLAC file as the vendored downloader leaves it, with a picture.

    THE COPYRIGHT LINE IS WRITTEN UNDER THE DOWNLOADER'S OWN KEY, upper case
    ``COPYRIGHT`` through mutagen, never through Cratekit's writer, so what is
    read is what a real download carries rather than what this unit's own
    table writes.
    """
    from mutagen.flac import FLAC

    path = folder / f"{name}.flac"
    shutil.copy2(silence, path)
    handle = FLAC(path)
    if copyright is not None:
        handle["COPYRIGHT"] = copyright
    if label is not None:
        handle["label"] = label
    if genre is not None:
        handle["genre"] = genre
    handle.save()
    plant(path, _jpeg(320, 200), dims=(320, 200, 24))
    return path


def registered(name: str, *argv: str) -> None:
    code, envelope = drive(["label", "registry", "add", name, *argv])
    assert code == int(ExitCode.OK), envelope


def blocked(artist: str, title: str):
    """Every catalogue refusing, the way the shipped searcher refuses a block."""
    raise refuse(
        searchers.UNREACHABLE_REASON,
        f"no catalogue could be read, so nothing is known about {title!r}",
        remedy=Remedy.RETRY_LATER,
        retryable=True,
        origin=("tagging", "searchers"),
    )


def blocking():
    asked: list[tuple[str, str]] = []

    def searcher(artist: str, title: str):
        asked.append((artist, title))
        blocked(artist, title)

    searcher.asked = asked  # type: ignore[attr-defined]
    return searcher


def never_searched(artist: str, title: str):
    raise AssertionError(f"a catalogue was searched for {title!r}")


def genre_seam(table: dict[str, str]):
    def answer(name: str) -> LabelAnswer | None:
        genre = table.get(name)
        return LabelAnswer(label=name, genre=genre) if genre else None

    return answer


def needles(table: dict[str, str], genres: dict[str, str] | None = None):
    """A copyright seam over ``{name: needle}``, the shell's own matcher over them,
    each label carrying its genre from ``genres`` (the module's GENRES by default)."""
    held = GENRES if genres is None else genres
    return tag_cli.copyright_matcher((name, needle, held.get(name)) for name, needle in table.items())


def names(matcher, line: str) -> tuple[str, ...]:
    return tuple(found.label for found in matcher(line))


# ═══════════════════════════════════════════════════════════════════════════
# 1. The copyright line, read off every container the downloader writes
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("suffix", [".flac", ".m4a", ".mp3"])
def test_the_copyright_line_is_read_from_the_key_the_downloader_writes(tmp_path, suffix):
    """``_vendor/downloader/metadata.py`` writes Vorbis ``COPYRIGHT``, ID3
    ``TCOP`` and MP4 ``cprt``; each is written here by mutagen directly."""
    path = synth_container(tmp_path, suffix)
    line = "℗ 2023 Rawax"
    if suffix == ".flac":
        from mutagen.flac import FLAC

        handle = FLAC(path)
        handle["COPYRIGHT"] = line
        handle.save()
    elif suffix == ".m4a":
        from mutagen.mp4 import MP4

        handle = MP4(path)
        handle["cprt"] = [line]
        handle.save()
    else:
        from mutagen.id3 import ID3, TCOP

        handle = ID3()
        handle.add(TCOP(encoding=3, text=line))
        handle.save(path)
    assert tags.read_tag(path, "copyright") == line


# ═══════════════════════════════════════════════════════════════════════════
# 2. The engine: the copyright line names a file's label when nothing else does
# ═══════════════════════════════════════════════════════════════════════════


GENRES = {RAWAX: MINIMAL, ATIPIC: PROGRESSIVE, CRONOS: SPECIFIC}
NEEDLES = {RAWAX: RAWAX, ATIPIC: ATIPIC, CRONOS: CRONOS, "Gettraum": "Gettraum"}


def test_a_mixed_folder_with_every_catalogue_blocked_tags_each_file_by_its_line(folder, silence):
    """The brief's scenario at the engine: three labels' files, no catalogue asked."""
    downloaded(folder, silence, "a", "℗ 2023 Rawax")
    downloaded(folder, silence, "b", "(P) 2024 Atipic")
    downloaded(folder, silence, "c", "2022 Cronos Barac")
    results = tag.tag_folder(
        folder,
        searcher=never_searched,
        label_genre=genre_seam(GENRES),
        copyright_labels=needles(NEEDLES),
    )
    assert [tags.read_genre_from_file(result.path) for result in results] == [
        MINIMAL,
        PROGRESSIVE,
        SPECIFIC,
    ]
    assert [(r.source, r.label, r.label_from) for r in results] == [
        (tag.LABEL_GENRE, RAWAX, tag.NAMED_BY_COPYRIGHT),
        (tag.LABEL_GENRE, ATIPIC, tag.NAMED_BY_COPYRIGHT),
        (tag.LABEL_GENRE, CRONOS, tag.NAMED_BY_COPYRIGHT),
    ]
    assert all(result.copyright_labels == () for result in results)


def test_a_file_whose_line_names_no_registered_label_is_asked_of_the_catalogues(folder, silence):
    path = downloaded(folder, silence, "a", "℗ 2023 Other Label")
    searcher = blocking()
    with pytest.raises(Exception) as raised:
        tag.tag_one(
            path,
            searcher=searcher,
            label_genre=genre_seam(GENRES),
            copyright_labels=needles(NEEDLES),
        )
    assert raised.value.cause.reason == searchers.UNREACHABLE_REASON
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(path) in (None, "")


def test_another_act_sharing_a_labels_first_letters_is_never_that_label(folder, silence):
    """U237's whole word rule decides it: ``Rawax`` never names ``RAWAXXX``."""
    path = downloaded(folder, silence, "a", "℗ 2023 RAWAXXX")
    searcher = answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)})
    result = tag.tag_one(
        path, searcher=searcher, label_genre=genre_seam(GENRES), copyright_labels=needles(NEEDLES)
    )
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(path) == "Techno"
    assert (result.label, result.label_from, result.copyright_labels) == ("", "", ())


def test_a_line_naming_two_registered_labels_is_refused_for_that_file(folder, silence):
    path = downloaded(folder, silence, "a", "2023 Cronos Barac under exclusive licence to Atipic")
    searcher = answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)})
    result = tag.tag_one(
        path, searcher=searcher, label_genre=genre_seam(GENRES), copyright_labels=needles(NEEDLES)
    )
    assert searcher.asked == [("", "a")], "the file was asked of the catalogues, as before"
    assert tags.read_genre_from_file(path) == "Techno"
    assert result.label == ""
    assert set(result.copyright_labels) == {ATIPIC, CRONOS}


def test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues(folder, silence):
    path = downloaded(folder, silence, "a", "℗ 2021 Gettraum")
    searcher = answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)})
    result = tag.tag_one(
        path, searcher=searcher, label_genre=genre_seam(GENRES), copyright_labels=needles(NEEDLES)
    )
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(path) == "Techno"
    assert (result.label, result.copyright_labels) == ("", ("Gettraum",))


def test_a_file_with_a_label_tag_keeps_it_whatever_its_line_names(folder, silence):
    """The tag outranks the line: a tag naming a label with no genre is searched."""
    path = downloaded(folder, silence, "a", "℗ 2023 Rawax", label="Other Label")
    searcher = answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)})
    result = tag.tag_one(
        path, searcher=searcher, label_genre=genre_seam(GENRES), copyright_labels=needles(NEEDLES)
    )
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(path) == "Techno"
    assert (result.label, result.label_tag, result.label_from) == ("", "Other Label", "")


def test_a_label_tag_naming_a_label_with_a_genre_is_named_by_the_tag(folder, silence):
    path = downloaded(folder, silence, "a", "℗ 2023 Atipic", label=RAWAX)
    result = tag.tag_one(
        path, searcher=never_searched, label_genre=genre_seam(GENRES), copyright_labels=needles(NEEDLES)
    )
    assert tags.read_genre_from_file(path) == MINIMAL
    assert (result.label, result.label_from) == (RAWAX, tag.NAMED_BY_TAG)


def test_the_verbs_label_outranks_the_copyright_line(folder, silence):
    """Every sweep given ``--label`` behaves exactly as it did before U240."""
    path = downloaded(folder, silence, "a", "℗ 2023 Atipic")
    result = tag.tag_one(
        path,
        searcher=never_searched,
        label_genre=genre_seam(GENRES),
        label=RAWAX,
        copyright_labels=needles(NEEDLES),
    )
    assert tags.read_genre_from_file(path) == MINIMAL
    assert (result.label, result.label_from) == (RAWAX, tag.NAMED_BY_FOLDER)


def test_a_file_already_carrying_a_genre_keeps_it_and_its_line_is_never_matched(folder, silence):
    path = downloaded(folder, silence, "a", "℗ 2023 Rawax", genre="Techno")
    asked: list[str] = []

    def matcher(line: str) -> tuple[tag.CopyrightLabel, ...]:
        asked.append(line)
        return (tag.CopyrightLabel(RAWAX, MINIMAL),)

    result = tag.tag_one(
        path, searcher=never_searched, label_genre=genre_seam(GENRES), copyright_labels=matcher
    )
    assert tags.read_genre_from_file(path) == "Techno"
    assert result.skipped == tag.HAS_GENRE
    assert asked == []


def test_a_file_with_no_copyright_line_is_asked_of_the_catalogues(folder, silence):
    path = downloaded(folder, silence, "a", None)
    searcher = answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)})
    result = tag.tag_one(
        path, searcher=searcher, label_genre=genre_seam(GENRES), copyright_labels=needles(NEEDLES)
    )
    assert searcher.asked == [("", "a")]
    assert (result.label, result.copyright_labels) == ("", ())


def test_no_copyright_seam_reads_no_line_and_tags_exactly_as_before(folder, silence):
    """A job queued before U240 froze no needles, and hands the engine no seam."""
    path = downloaded(folder, silence, "a", "℗ 2023 Rawax")
    searcher = answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)})
    result = tag.tag_one(path, searcher=searcher, label_genre=genre_seam(GENRES))
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(path) == "Techno"
    assert result.label == ""


# ═══════════════════════════════════════════════════════════════════════════
# 3. The matcher: whole words, through the needle each label is registered with
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    ("line", "named"),
    [
        ("℗ 2023 Rawax", (RAWAX,)),
        ("© 2023 RAWAX", (RAWAX,)),
        ("(P) 2023 Rawax Records", (RAWAX,)),
        ("2023 Rawax under exclusive licence to Some Distributor", (RAWAX,)),
        ("℗ 2023 RAWAXXX", ()),
        ("℗ 2023", ()),
        ("", ()),
        ("   ", ()),
    ],
)
def test_the_matcher_names_a_label_by_its_needle_in_whole_words(line, named):
    assert names(needles({RAWAX: RAWAX, ATIPIC: ATIPIC}), line) == named


def test_the_matcher_reads_a_labels_match_needle_and_not_its_name():
    """A label registered as ``Some Label`` with ``--match "SL Recordings"``: a
    line carrying the needle and not the name names it, and the name alone does not."""
    matcher = needles({"Some Label": "SL Recordings"})
    assert names(matcher, "℗ 2024 SL Recordings") == ("Some Label",)
    assert names(matcher, "℗ 2024 Some Label") == ()


@pytest.mark.parametrize(
    "line",
    ["℗ 2023 Barac", "(P) 2024 Cronos", "℗ 2024 Music", "℗ 2023 Records"],
)
def test_a_line_carrying_only_part_of_a_needle_names_no_label(line):
    """One way only: a short line inside a long needle writes no genre (review round one)."""
    matcher = needles({CRONOS: CRONOS, "Aus Music": "Aus Music", "Some Label": "Some Label Records"})
    assert names(matcher, line) == ()


def test_a_sublabels_own_line_names_the_sublabel_and_the_parents_names_the_parent():
    """The needle carrying every other needle named wins; review round one found
    the parent's own line answered both and settled neither."""
    matcher = needles({RAWAX: RAWAX, "Rawax Motor City Edition": "Rawax Motor City Edition"})
    assert names(matcher, "℗ 2023 Rawax") == (RAWAX,)
    assert names(matcher, "℗ 2023 Rawax Motor City Edition") == ("Rawax Motor City Edition",)


def test_two_labels_registered_with_one_needle_settle_neither():
    matcher = needles({RAWAX: RAWAX, "Rawax Again": RAWAX})
    assert set(names(matcher, "℗ 2023 Rawax")) == {RAWAX, "Rawax Again"}


def test_each_named_label_carries_its_own_genre():
    matcher = needles({RAWAX: RAWAX, "Gettraum": "Gettraum"})
    assert matcher("℗ 2023 Rawax") == (tag.CopyrightLabel(RAWAX, MINIMAL),)
    assert matcher("℗ 2023 Gettraum") == (tag.CopyrightLabel("Gettraum", None),)


@pytest.mark.parametrize(
    ("needle", "line"),
    [
        ("2020 Vision", "\u2117 2020 Vision Quest"),
        ("1985 Music", "(P) 1985 Music For Nations"),
    ],
)
def test_a_lines_year_never_completes_a_needle(needle, line):
    """Review round two: matched on the raw line, the year completed the needle."""
    assert names(needles({needle: needle}), line) == ()


@pytest.mark.parametrize(
    ("needle", "line"),
    [
        ("\u00c2me", "\u2117 2021 Give Me Records"),
        ("\u6771\u4eac Records", "\u2117 2023 Completely Unrelated Records"),
    ],
)
def test_a_letter_outside_ascii_never_folds_away_from_a_needle(needle, line):
    """Review round two: the ASCII fold shrank \u00c2me to me and \u6771\u4eac Records to records."""
    assert names(needles({needle: needle}), line) == ()


def test_a_needle_outside_ascii_still_names_its_own_line():
    assert names(needles({"\u00c2me": "\u00c2me"}), "\u2117 2021 \u00c2me") == ("\u00c2me",)


def test_a_sublabel_beside_a_third_label_settles_nothing():
    """The longer needle wins only when it carries EVERY other one named."""
    matcher = needles(
        {RAWAX: RAWAX, "Rawax Motor City Edition": "Rawax Motor City Edition", ATIPIC: ATIPIC}
    )
    line = "\u2117 2023 Rawax Motor City Edition under exclusive licence to Atipic"
    assert set(names(matcher, line)) == {RAWAX, "Rawax Motor City Edition", ATIPIC}


def test_two_labels_sharing_a_display_name_are_two_in_the_ambiguous_count():
    counted: dict[str, int] = {}
    tag_cli._count_ambiguous(counted, ["Alpha", "Alpha"])
    tag_cli._count_ambiguous(counted, ["Gettraum"])
    assert counted == {"Alpha, Alpha": 1}


def test_a_searchers_park_reaches_the_job_as_a_park_on_a_file_its_line_could_not_settle(
    folder, silence
):
    path = downloaded(folder, silence, "a", "2023 Cronos Barac under exclusive licence to Atipic")

    def parking(artist: str, title: str):
        raise jobs.Parked(
            refuse(searchers.UNREACHABLE_REASON, "the catalogue refused the client", origin=("tests",)).cause
        )

    with pytest.raises(jobs.Parked):
        tag.tag_one(
            path, searcher=parking, label_genre=genre_seam(GENRES), copyright_labels=needles(NEEDLES)
        )


# ═══════════════════════════════════════════════════════════════════════════
# 4. The sweep, through the real dispatcher and a resume
# ═══════════════════════════════════════════════════════════════════════════


def sweep(*argv: str) -> tuple[int, jobs.Job, dict]:
    code, queued = drive(["tag", "folder", "--queue-only", *argv])
    assert code == int(ExitCode.OK), queued
    job = tag_job()
    code, resumed = drive(resume_argv(job.job_id))
    return code, job, resumed


def five_labels() -> None:
    registered(RAWAX, "--genre", MINIMAL)
    registered(ATIPIC, "--genre", PROGRESSIVE)
    registered(CRONOS, "--genre", SPECIFIC)
    registered("Gettraum")


def test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label(
    cfg, folder, silence, monkeypatch
):
    """The live failure of 2026-11-10, in one call and with no ``--label``."""
    five_labels()
    downloaded(folder, silence, "a", "℗ 2023 Rawax")
    downloaded(folder, silence, "b", "℗ 2024 Atipic")
    downloaded(folder, silence, "c", "℗ 2022 Cronos Barac")
    searcher = bound(monkeypatch, blocking())

    code, job, resumed = sweep(str(folder))

    assert code == int(ExitCode.OK), resumed
    assert searcher.asked == [], "no catalogue was asked about a file its line named"
    assert [tags.read_genre_from_file(folder / f"{n}.flac") for n in "abc"] == [
        MINIMAL,
        PROGRESSIVE,
        SPECIFIC,
    ]
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged_by"][tag.LABEL_GENRE] == 3
    assert tagging["label_genres"] == {RAWAX: 1, ATIPIC: 1, CRONOS: 1}
    assert tagging["ways"] == {"label": 3, "catalogue": 0, "none": 0}
    assert tagging["files"] == [
        {"item": "a.flac", "way": "label", "label": RAWAX, "named_by": "copyright", "failed": ""},
        {"item": "b.flac", "way": "label", "label": ATIPIC, "named_by": "copyright", "failed": ""},
        {"item": "c.flac", "way": "label", "label": CRONOS, "named_by": "copyright", "failed": ""},
    ]
    assert "label" not in job.payload, "no --label was frozen"
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert (reports["a.flac"]["label"], reports["a.flac"]["label_from"]) == (RAWAX, "copyright")
    assert reports["a.flac"]["copyright_labels"] == []


def test_an_unregistered_file_in_the_batch_is_left_untagged_and_its_item_fails(
    cfg, folder, silence, monkeypatch
):
    five_labels()
    downloaded(folder, silence, "a", "℗ 2023 Rawax")
    downloaded(folder, silence, "b", "℗ 2024 Atipic")
    downloaded(folder, silence, "c", "℗ 2022 Cronos Barac")
    downloaded(folder, silence, "d", "℗ 2022 Other Label")
    searcher = bound(monkeypatch, blocking())

    code, job, _resumed = sweep(str(folder))

    assert code != int(ExitCode.OK)
    assert searcher.asked == [("", "d")]
    assert item_states(job.job_id) == {
        "a.flac": jobs.ItemState.DONE,
        "b.flac": jobs.ItemState.DONE,
        "c.flac": jobs.ItemState.DONE,
        "d.flac": jobs.ItemState.FAILED,
    }
    assert item_causes(job.job_id) == {"d.flac": searchers.UNREACHABLE_REASON}
    assert tags.read_genre_from_file(folder / "d.flac") in (None, "")
    assert tags.read_genre_from_file(folder / "a.flac") == MINIMAL


def test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all(
    cfg, folder, silence, monkeypatch
):
    five_labels()
    downloaded(folder, silence, "a", "℗ 2023 Rawax")
    downloaded(folder, silence, "b", "℗ 2022 Other Label")
    downloaded(folder, silence, "c", "℗ 2022 Nobody")
    downloaded(folder, silence, "d", "℗ 2022 Rawax", genre="Techno")
    bound(monkeypatch, answering({"b": SearchHit(genre="Techno", source=searchers.BEATPORT)}))

    code, job, resumed = sweep(str(folder))

    assert code == int(ExitCode.OK), resumed
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["ways"] == {"label": 1, "catalogue": 1, "none": 2}
    assert tagging["files"] == [
        {"item": "a.flac", "way": "label", "label": RAWAX, "named_by": "copyright", "failed": ""},
        {"item": "b.flac", "way": "catalogue", "label": "", "named_by": "", "failed": ""},
        {"item": "c.flac", "way": "none", "label": "", "named_by": "", "failed": ""},
        {"item": "d.flac", "way": "none", "label": "", "named_by": "", "failed": ""},
    ]


def test_files_whose_line_named_two_labels_are_counted_and_warned(
    cfg, folder, silence, monkeypatch
):
    five_labels()
    downloaded(folder, silence, "a", "2023 Cronos Barac under exclusive licence to Atipic")
    downloaded(folder, silence, "b", "2023 Cronos Barac under exclusive licence to Atipic")
    downloaded(folder, silence, "c", "\u2117 2021 Gettraum")
    bound(monkeypatch, answering({}))

    code, job, resumed = sweep(str(folder))

    assert code == int(ExitCode.OK), resumed
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert sorted(reports["a.flac"]["copyright_labels"]) == [ATIPIC, CRONOS]
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["copyright_ambiguous"] == {f"{ATIPIC}, {CRONOS}": 2}
    warned = {w["code"]: w["message"] for w in resumed["warnings"]}
    assert tag_cli.COPYRIGHT_AMBIGUOUS == "tag-folder-copyright-ambiguous"
    assert f"{ATIPIC}, {CRONOS} on 2" in warned[tag_cli.COPYRIGHT_AMBIGUOUS]


def test_a_sweep_one_file_of_which_fails_still_reports_every_file(
    cfg, folder, silence, monkeypatch
):
    """Review round one: with the catalogues blocked, one unsettled file made the
    sweep a refusal that said nothing of the files the labels had tagged."""
    five_labels()
    downloaded(folder, silence, "a", "\u2117 2023 Rawax")
    downloaded(folder, silence, "b", "\u2117 2024 Atipic")
    downloaded(folder, silence, "d", "\u2117 2022 Some Other Label")
    downloaded(folder, silence, "e", "2023 Cronos Barac under exclusive licence to Atipic")
    bound(monkeypatch, blocking())

    code, job, resumed = sweep(str(folder))

    assert code != int(ExitCode.OK), resumed
    assert item_causes(job.job_id) == {
        "d.flac": searchers.UNREACHABLE_REASON,
        "e.flac": searchers.UNREACHABLE_REASON,
    }
    cause = resumed["cause"]
    tagging = cause["detail"]["tagging"]
    assert tagging["ways"] == {"label": 2, "catalogue": 0, "none": 2}
    assert [(row["item"], row["way"], row["label"], row["failed"]) for row in tagging["files"]] == [
        ("a.flac", "label", RAWAX, ""),
        ("b.flac", "label", ATIPIC, ""),
        ("d.flac", "none", "", searchers.UNREACHABLE_REASON),
        ("e.flac", "none", "", searchers.UNREACHABLE_REASON),
    ]
    assert tagging["copyright_ambiguous"] == {f"{ATIPIC}, {CRONOS}": 1}
    assert (
        "Of 4 file(s), 2 took their registered label's genre, 0 a catalogue's and 2 none; "
        "the item failed for d.flac, e.flac." in cause["message"]
    )
    assert f"({ATIPIC}, {CRONOS} on 1)" in cause["message"]


def test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre(
    cfg, folder, silence, monkeypatch
):
    """Review round one: the seam keyed the needles by display name, so a rename
    onto a taken name gave one label's files the other's genre."""
    registered("Alpha", "--genre", SPECIFIC)
    registered("Omega")
    code, envelope = drive(["label", "registry", "rename", "omega", "--to", "Alpha"])
    assert code == int(ExitCode.OK), envelope
    code, envelope = drive(["label", "registry", "set", "omega", "--match", "Omega Trax"])
    assert code == int(ExitCode.OK), envelope
    downloaded(folder, silence, "f", "\u2117 2024 Omega Trax")
    downloaded(folder, silence, "g", "\u2117 2024 Alpha")
    searcher = bound(monkeypatch, answering({"f": SearchHit(genre="Techno", source=searchers.BEATPORT)}))

    code, _job, resumed = sweep(str(folder))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "f.flac") == "Techno", "the genre-less label's file"
    assert tags.read_genre_from_file(folder / "g.flac") == SPECIFIC
    assert searcher.asked == [("", "f")]


def test_a_refusal_names_ten_failed_files_and_counts_the_rest(cfg, folder, silence, monkeypatch):
    five_labels()
    for index in range(12):
        downloaded(folder, silence, f"x{index:02d}", "\u2117 2022 Some Other Label")
    bound(monkeypatch, blocking())

    code, _job, resumed = sweep(str(folder))

    assert code != int(ExitCode.OK)
    message = resumed["cause"]["message"]
    shown = ", ".join(f"x{index:02d}.flac" for index in range(10))
    assert f"the item failed for {shown} and 2 more." in message


def test_a_cancelled_sweep_carries_its_report_too(cfg, folder, silence, monkeypatch):
    five_labels()
    downloaded(folder, silence, "a", "\u2117 2023 Rawax")
    downloaded(folder, silence, "b", "\u2117 2023 Atipic")
    bound(monkeypatch, never_searched)
    code, queued = drive(["tag", "folder", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = tag_job()
    code, cancelled = drive(["job", "cancel", job.job_id])
    assert code == int(ExitCode.OK), cancelled

    code, resumed = drive(resume_argv(job.job_id))

    assert code != int(ExitCode.OK), resumed
    assert resumed["outcome"] == "cancelled", resumed
    tagging = resumed["cause"]["detail"]["tagging"]
    assert tagging["ways"] == {"label": 0, "catalogue": 0, "none": 2}
    assert "Of 2 file(s), 0 took their registered label's genre" in resumed["cause"]["message"]


def test_the_needles_are_frozen_with_the_genres_when_the_sweep_is_queued(
    cfg, folder, silence, monkeypatch
):
    from cratekit.label import registry as labels

    five_labels()
    labels.RegistryStore().edit(RAWAX, match="Rawax Records")
    downloaded(folder, silence, "a", "℗ 2023 Rawax Records")
    bound(monkeypatch, never_searched)
    code, queued = drive(["tag", "folder", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    labels.RegistryStore().edit(RAWAX, match="Nothing Like It")
    job = tag_job()
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "a.flac") == MINIMAL
    assert job.payload["label_needles"]["rawax"] == {"name": RAWAX, "needle": "Rawax Records"}
    assert job.payload["label_needles"]["gettraum"] == {"name": "Gettraum", "needle": "Gettraum"}


def test_a_sweep_with_no_label_genres_freezes_no_needles(cfg, folder, silence, monkeypatch):
    registered("Gettraum")
    downloaded(folder, silence, "a", "℗ 2023 Gettraum")
    bound(monkeypatch, answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)}))
    _code, job, _resumed = sweep(str(folder))
    assert job.payload == {"folder": str(folder)}


def test_a_job_queued_before_needles_were_frozen_is_tagged_as_it_always_was(
    cfg, folder, silence, monkeypatch
):
    five_labels()
    downloaded(folder, silence, "a", "℗ 2023 Rawax")
    searcher = bound(monkeypatch, answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)}))
    shipped = tag_cli._label_payload

    def older_build(label):
        frozen, warnings = shipped(label)
        frozen.pop("label_needles", None)
        return frozen, warnings

    monkeypatch.setattr(tag_cli, "_label_payload", older_build)
    code, queued = drive(["tag", "folder", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = tag_job()
    assert "label_genres" in job.payload and "label_needles" not in job.payload
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(folder / "a.flac") == "Techno"


# ═══════════════════════════════════════════════════════════════════════════
# 5. The label go's tail: its tag step passes the copyright tier through
# ═══════════════════════════════════════════════════════════════════════════


def test_the_tails_tag_step_lands_a_label_batch_with_every_catalogue_blocked(
    cfg, folder, silence, monkeypatch
):
    """``label sync --go`` queues ``tag folder`` with no ``--label`` (U190)."""
    five_labels()
    downloaded(folder, silence, "a", "℗ 2023 Rawax")
    downloaded(folder, silence, "b", "℗ 2024 Atipic")
    bound(monkeypatch, blocking())
    chain = tail.Chain(
        progress=None, namespace="t", title="t", steps=tail.STEPS, origin=("test",), again="again"
    )

    tail.tail_step(chain, tail.TAG, "tag.folder", ("tag", "folder"), folder, cfg)

    assert chain.summary["commands"][0] == ["crate", "tag", "folder", "--queue-only", str(folder)]
    assert tag_job().state is jobs.JobState.SUCCEEDED
    assert tags.read_genre_from_file(folder / "a.flac") == MINIMAL
    assert tags.read_genre_from_file(folder / "b.flac") == PROGRESSIVE
