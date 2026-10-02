"""R-799: the genres an older mapping wrote from the general catalogue's words, corrected.

On the author's library the general catalogue's Pop was written as the dance
bucket's name on 10 tracks and its Alternative as a bucket's bare name on 6,
before the taxonomy gave that catalogue a table of its own. ``crate tag remap``
finds those files from what the tagging jobs recorded and plans their rewrite
behind an explicit gate. These tests drive the engine over real containers and
committed records, and the verb through the real dispatcher.

EVERY EXPECTED GENRE IS A LITERAL. The words are the general catalogue's and
the genres are the shipped template's, typed, so a row of the template that
drifts fails here and is not followed.

NOTHING HERE REACHES A NETWORK OR A DATABASE. The verb asks nobody and opens
no library. D1 applies: no real artist or track is named.
"""

from __future__ import annotations

import json
import shutil
import tomllib
from dataclasses import replace
from importlib import resources
from pathlib import Path

import pytest

from cratekit.cli import registry
from cratekit.core import config, jobs, preflight, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import artifacts, remap, remap_cli
from tests._containers import synth_container
from tests.cli_drive import drive, drive_human
from tests.test_config import valid_data

DECLARED = taxonomy.default_taxonomy()
VERB = ["tag", "remap"]
GATE = "tag.remap.confirm"

#: The general catalogue and one record shop, as a tagging record names them.
CATALOGUE = "deezer"
SHOP = "beatport"

#: What the older mapping wrote for the catalogue's Pop and Alternative, and
#: what the shipped table writes for them now.
OLD_POP = "Dance / Pop"
NEW_POP = "NonElectronic / Pop"
OLD_ALTERNATIVE = "NonElectronic"
NEW_ALTERNATIVE = "Rock"


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One synthesized container, copied per track. The encoder runs once."""
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A set up machine with every module on and no active taxonomy copy."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(valid_data(root, profile={"name": "full"}))
    config.save(cfg)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return cfg


def music(cfg: config.Config) -> Path:
    return cfg.library.root / "Music"


def a_file(cfg: config.Config, silence: Path, name: str, genre: str | None) -> Path:
    """One real container under the library, carrying this genre or none."""
    path = music(cfg) / f"{name}.flac"
    shutil.copy2(silence, path)
    if genre is not None:
        assert tags.write_genre(path, genre)
    return path


def record(
    cfg: config.Config,
    path: Path | str,
    written: str | None,
    *,
    source: str = CATALOGUE,
    word: str = "",
    job: str = "job-a",
    ordinal: int | None = None,
) -> None:
    """Commit one tagging record, in the shape the tagging worker commits."""
    directory = jobs.store_dir(cfg) / artifacts.ARTIFACTS_DIRNAME / job
    taken = len(list(directory.glob("*.json"))) if directory.is_dir() else 0
    artifacts.write(
        artifacts.final_path(cfg, job, taken if ordinal is None else ordinal),
        {
            "item": Path(path).name,
            "path": str(path),
            "genre_written": written,
            "skipped": None if written else "unmapped-genre",
            "source": source,
            "source_genre": word,
            "off_taxonomy": False,
            "answers": [],
        },
    )


def tagged(cfg, silence, name, written, word, *, source=CATALOGUE, now=None, job="job-a") -> Path:
    """A file a tagging job wrote ``written`` onto, carrying ``now`` today."""
    path = a_file(cfg, silence, name, written if now is None else now)
    record(cfg, path, written, source=source, word=word, job=job)
    return path


def counts(plan: remap.RemapPlan, **expected: int) -> None:
    """Every outcome's count, the unnamed ones held to zero."""
    wanted = dict.fromkeys(
        ("agree", "write", "changed-since", "word-declined", "ambiguous-record",
         "file-missing", "file-unreadable", "outside-library"),
        0,
    )  # fmt: skip
    wanted.update({name.replace("_", "-"): count for name, count in expected.items()})
    assert dict(plan.counts) == wanted


def planned(cfg: config.Config, declared=DECLARED) -> remap.RemapPlan:
    return remap.plan(cfg, declared)


def genre_of(path: Path) -> str | None:
    return tags.read_genre_from_file(path)


def did(written: remap.Written) -> remap.Written:
    """An apply's counts and named paths, with the list of rewritten items set
    aside. That list is asserted where it is the point."""
    return replace(written, rewritten=())


# ═══════════════════════════════════════════════════════════════════════════
# 1. The plan: one outcome per file
# ═══════════════════════════════════════════════════════════════════════════


def test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    plan = planned(machine)
    counts(plan, write=1)
    assert plan.items == (
        remap.Item(str(path), "Pop", OLD_POP, OLD_POP, NEW_POP, "write"),
    )
    assert plan.writes == plan.items
    assert genre_of(path) == OLD_POP


def test_a_file_tagged_the_same_genre_by_a_record_shop_is_not_planned(machine, silence):
    """The card's second half. Beatport's Pop is a dance genre and stays one."""
    path = tagged(machine, silence, "a dance record", OLD_POP, "Pop", source=SHOP)
    plan = planned(machine)
    counts(plan)
    assert plan.items == () and plan.files == 0
    assert genre_of(path) == OLD_POP


def test_the_catalogues_alternative_written_as_the_bare_name_is_planned_as_rock(machine, silence):
    path = tagged(machine, silence, "an alternative record", OLD_ALTERNATIVE, "Alternative")
    (item,) = planned(machine).items
    assert (item.path, item.current, item.wanted, item.action) == (
        str(path), OLD_ALTERNATIVE, NEW_ALTERNATIVE, "write",
    )  # fmt: skip


def test_a_file_whose_word_the_table_writes_as_it_was_written_agrees(machine, silence):
    tagged(machine, silence, "a rock record", "Rock", "Rock")
    tagged(machine, silence, "a rap record", "Hip-Hop", "Rap/Hip Hop")
    plan = planned(machine)
    counts(plan, agree=2)
    assert plan.items == ()


def test_a_file_already_carrying_the_genre_wanted_agrees(machine, silence):
    """What a second run finds, and what a file a person corrected looks like."""
    tagged(machine, silence, "a pop record", OLD_POP, "Pop", now=NEW_POP)
    plan = planned(machine)
    counts(plan, agree=1)
    assert plan.items == ()


@pytest.mark.parametrize("now", ["Deep House", "dance / pop", "Pop"])
def test_a_genre_nobody_recorded_writing_is_left_alone_and_listed(machine, silence, now):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop", now=now)
    plan = planned(machine)
    counts(plan, changed_since=1)
    assert plan.items == (
        remap.Item(str(path), "Pop", OLD_POP, now, NEW_POP, "leave", "changed-since"),
    )
    assert plan.writes == ()


def test_a_file_whose_genre_was_cleared_is_left_alone_and_not_read_as_agreeing(machine, silence):
    path = a_file(machine, silence, "a pop record", None)
    record(machine, path, OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, changed_since=1)
    assert plan.items[0].current == ""


def test_a_blank_file_whose_word_is_now_declined_is_not_read_as_agreeing(machine, silence):
    """Blank and nothing wanted are both empty, and that is not agreement."""
    path = a_file(machine, silence, "a record", None)
    record(machine, path, OLD_ALTERNATIVE, word="Indie Rock")
    counts(planned(machine), changed_since=1)


def test_a_file_holding_a_second_genre_is_left_alone_and_both_are_shown(machine, silence):
    path = a_file(machine, silence, "a pop record", None)
    from mutagen.flac import FLAC

    handle = FLAC(path)
    handle["genre"] = [OLD_POP, "Deep House"]
    handle.save()
    record(machine, path, OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, changed_since=1)
    assert plan.items[0].current == f"{OLD_POP} | Deep House"


def test_a_word_the_taxonomy_now_has_no_folder_for_is_listed_and_left(machine, silence):
    """A word with no row that the aliases answer with a bare bucket name,
    which is no longer written. The genre stays on the file: declining a word
    is no reason to blank one, and a person reads which word to add a row for."""
    path = tagged(machine, silence, "an indie record", OLD_ALTERNATIVE, "Indie Rock")
    plan = planned(machine)
    counts(plan, word_declined=1)
    assert plan.items == (
        remap.Item(
            str(path), "Indie Rock", OLD_ALTERNATIVE, OLD_ALTERNATIVE, "", "leave",
            "word-declined",
        ),
    )  # fmt: skip


def test_a_word_with_no_row_that_the_aliases_still_file_agrees(machine, silence):
    """The one House / Funky House / Disco of sitting 26. Its word has no row
    and is filed as it was."""
    tagged(machine, silence, "a disco record", "House / Funky House / Disco", "Disco")
    plan = planned(machine)
    counts(plan, agree=1)
    assert plan.items == ()


def test_a_genre_two_records_explain_with_different_sources_is_left(machine, silence):
    """Which job wrote last is not recorded, so a genre a record shop may have
    supplied is not rewritten on the general catalogue's say."""
    path = tagged(machine, silence, "a record", OLD_POP, "Pop", job="job-a")
    record(machine, path, OLD_POP, source=SHOP, word="Pop", job="job-b")
    plan = planned(machine)
    counts(plan, ambiguous_record=1)
    assert (plan.items[0].action, plan.items[0].reason) == ("leave", "ambiguous-record")


def test_a_genre_two_records_explain_with_different_words_is_left(machine, silence):
    path = tagged(machine, silence, "a record", OLD_ALTERNATIVE, "Alternative", job="job-a")
    record(machine, path, OLD_ALTERNATIVE, word="Country", job="job-b")
    counts(planned(machine), ambiguous_record=1)


def test_two_records_of_one_word_from_one_source_are_one_explanation(machine, silence):
    path = tagged(machine, silence, "a record", OLD_POP, "Pop", job="job-a")
    record(machine, path, OLD_POP, word="Pop", job="job-b")
    plan = planned(machine)
    counts(plan, write=1)
    assert len(plan.items) == 1


def test_a_genre_a_record_shop_wrote_later_on_a_path_the_catalogue_once_wrote_agrees(
    machine, silence
):
    path = tagged(machine, silence, "a record", OLD_ALTERNATIVE, "Alternative", now="Deep House")
    record(machine, path, "Deep House", source=SHOP, word="Deep House", job="job-b")
    plan = planned(machine)
    counts(plan, agree=1)
    assert plan.items == ()


def test_one_file_recorded_under_two_spellings_is_one_file(machine, silence):
    """What the second review drove. Grouped by the string, the shop's record
    was never seen beside the general catalogue's and the genre a record shop
    supplied was planned for rewrite."""
    path = tagged(machine, silence, "a record", OLD_POP, "Pop", job="job-a")
    spelled = music(machine) / ".." / "Music" / "a record.flac"
    record(machine, spelled, OLD_POP, source=SHOP, word="Pop", job="job-b")
    plan = planned(machine)
    counts(plan, ambiguous_record=1)
    assert [item.path for item in plan.items] == [str(path)]


def test_one_file_the_catalogue_recorded_twice_under_two_spellings_is_planned_once(
    machine, silence
):
    path = tagged(machine, silence, "a record", OLD_POP, "Pop", job="job-a")
    record(machine, music(machine) / "." / "a record.flac", OLD_POP, word="Pop", job="job-b")
    plan = planned(machine)
    counts(plan, write=1)
    assert did(remap.apply(machine, plan)) == remap.Written(written=1, read_back=1)
    assert genre_of(path) == NEW_POP


def test_a_file_reached_through_a_link_is_the_file(machine, silence, tmp_path):
    path = tagged(machine, silence, "a record", OLD_POP, "Pop", job="job-a")
    link = music(machine) / "linked.flac"
    link.symlink_to(path)
    record(machine, link, OLD_POP, source=SHOP, word="Pop", job="job-b")
    counts(planned(machine), ambiguous_record=1)


def test_a_folder_named_in_another_case_on_a_volume_that_folds_case_is_inside(
    machine, silence
):
    """A tag job keeps the folder as it was typed. Where the volume folds case
    that is the same directory, and its files are this library's."""
    path = tagged(machine, silence, "a record", OLD_POP, "Pop")
    typed = Path(str(machine.library.root).upper()) / "Music" / "a record.flac"
    if not typed.exists():
        pytest.skip("this volume keeps two cases apart, so the other case is another folder")
    directory = jobs.store_dir(machine) / artifacts.ARTIFACTS_DIRNAME / "job-a"
    for report in directory.glob("*.json"):
        report.unlink()
    record(machine, typed, OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, write=1)
    assert genre_of(path) == OLD_POP


def test_two_files_that_are_gone_are_two_files(machine):
    record(machine, music(machine) / "gone one.flac", OLD_POP, word="Pop")
    record(machine, music(machine) / "gone two.flac", OLD_POP, word="Pop")
    counts(planned(machine), file_missing=2)


def test_a_file_that_is_gone_is_counted_missing_and_listed(machine, silence):
    gone = music(machine) / "moved since.flac"
    record(machine, gone, OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, file_missing=1)
    assert plan.items == (
        remap.Item(str(gone), "Pop", OLD_POP, "", "", "leave", "file-missing"),
    )


def test_a_file_no_tag_library_opens_is_unreadable_and_not_changed_since(machine, silence):
    broken = music(machine) / "broken.flac"
    broken.write_bytes(b"not a container at all")
    record(machine, broken, OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, file_unreadable=1)
    assert plan.items[0].reason == "file-unreadable"


def test_a_file_outside_this_librarys_root_is_counted_and_never_opened(
    machine, silence, tmp_path, monkeypatch
):
    """The queue is the installation's. A folder tagged before it was landed,
    and another library's files, are not this library's taxonomy's to resolve."""
    staging = tmp_path / "staging"
    staging.mkdir()
    outside = staging / "a pop record.flac"
    shutil.copy2(silence, outside)
    assert tags.write_genre(outside, OLD_POP)
    record(machine, outside, OLD_POP, word="Pop")
    record(machine, tmp_path / "another library" / "gone.flac", OLD_POP, word="Pop")
    opened: list[Path] = []
    real = tags.read_tag_values_checked
    monkeypatch.setattr(
        tags, "read_tag_values_checked", lambda path, field: opened.append(path) or real(path, field)
    )

    plan = planned(machine)

    counts(plan, outside_library=2)
    assert plan.items == () and plan.files == 2 and opened == []
    assert did(remap.apply(machine, plan)) == remap.Written(written=0, read_back=0)
    assert genre_of(outside) == OLD_POP


def test_a_path_that_climbs_out_of_the_library_is_outside_it(machine, silence, tmp_path):
    escaped = tmp_path / "escaped.flac"
    shutil.copy2(silence, escaped)
    assert tags.write_genre(escaped, OLD_POP)
    record(machine, music(machine) / ".." / ".." / "escaped.flac", OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, outside_library=1)
    assert genre_of(escaped) == OLD_POP


def test_every_file_is_counted_once_and_the_items_are_in_path_order(machine, silence):
    tagged(machine, silence, "d pop", OLD_POP, "Pop")
    tagged(machine, silence, "a rock", "Rock", "Rock")
    tagged(machine, silence, "c alternative", OLD_ALTERNATIVE, "Alternative")
    tagged(machine, silence, "b by hand", OLD_POP, "Pop", now="Deep House")
    tagged(machine, silence, "e a shop's", OLD_POP, "Pop", source=SHOP)
    record(machine, music(machine) / "f gone.flac", OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, agree=1, write=2, changed_since=1, file_missing=1)
    assert plan.files == 5
    assert [Path(item.path).stem for item in plan.items] == [
        "b by hand", "c alternative", "d pop", "f gone",
    ]  # fmt: skip
    assert plan.pairs() == [
        {"from": OLD_POP, "to": NEW_POP, "files": 1},
        {"from": OLD_ALTERNATIVE, "to": NEW_ALTERNATIVE, "files": 1},
    ]


def test_the_pairs_are_the_writes_counted_largest_first(machine, silence):
    tagged(machine, silence, "one", OLD_ALTERNATIVE, "Alternative")
    tagged(machine, silence, "two", OLD_POP, "Pop")
    tagged(machine, silence, "three", OLD_POP, "Pop")
    assert planned(machine).pairs() == [
        {"from": OLD_POP, "to": NEW_POP, "files": 2},
        {"from": OLD_ALTERNATIVE, "to": NEW_ALTERNATIVE, "files": 1},
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 2. The records
# ═══════════════════════════════════════════════════════════════════════════


def test_a_record_that_wrote_no_genre_names_no_file_to_look_at(machine, silence):
    path = a_file(machine, silence, "declined then", None)
    record(machine, path, None, word="Christian")
    record(machine, path, "   ", word="Christian", job="job-b")
    plan = planned(machine)
    counts(plan)
    assert plan.files == 0


def test_the_correction_verbs_of_another_shape_are_passed_over(machine, silence):
    """``tag retag`` commits beside the tagging records, with no genre_written."""
    path = a_file(machine, silence, "retagged", "Deep House")
    artifacts.write(
        artifacts.final_path(machine, "job-retag", 0),
        {"item": str(path), "path": str(path), "current": "Electronica", "written": "Deep House"},
    )
    assert remap.recorded(artifacts.every_committed(machine)[0]) == ()


def test_a_record_that_cannot_be_parsed_is_counted_and_carried_by_the_plan(machine, silence):
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    directory = jobs.store_dir(machine) / artifacts.ARTIFACTS_DIRNAME / "job-a"
    (directory / "0007.json").write_text("{ not json", encoding="utf-8")
    (directory / "0008.json").write_text('["a list"]', encoding="utf-8")
    reports, unread = artifacts.every_committed(machine)
    assert (len(reports), unread) == (1, 2)
    plan = planned(machine)
    assert plan.records_unread == 2
    counts(plan, write=1)


def test_every_jobs_records_are_read_in_job_then_item_order(machine):
    record(machine, "/b", "Rock", word="Rock", job="job-b")
    record(machine, "/a2", "Rock", word="Rock", job="job-a", ordinal=2)
    record(machine, "/a10", "Rock", word="Rock", job="job-a", ordinal=10)
    reports, unread = artifacts.every_committed(machine)
    assert [(job, report["path"]) for job, report in reports] == [
        ("job-a", "/a2"), ("job-a", "/a10"), ("job-b", "/b"),
    ]  # fmt: skip
    assert unread == 0


def test_the_ten_thousandth_item_is_read_after_the_nine_thousand_nine_hundred_ninety_ninth(
    machine,
):
    """As a number. As text ``10000`` sorts before ``9999``."""
    record(machine, "/late", "Rock", word="Rock", ordinal=10000)
    record(machine, "/early", "Rock", word="Rock", ordinal=9999)
    directory = jobs.store_dir(machine) / artifacts.ARTIFACTS_DIRNAME / "job-a"
    (directory / "notes.json").write_text('{"path": "/stray"}', encoding="utf-8")
    reports, unread = artifacts.every_committed(machine)
    assert [report["path"] for _job, report in reports] == ["/early", "/late", "/stray"]
    assert unread == 0


def test_a_queue_that_has_never_tagged_reads_as_no_records(machine):
    assert artifacts.every_committed(machine) == ((), 0)
    plan = planned(machine)
    counts(plan)
    assert plan.items == ()


def test_a_record_is_read_whether_or_not_the_queue_still_lists_its_job(machine, silence):
    """Off the directory. No job row exists for any record these tests commit."""
    tagged(machine, silence, "a pop record", OLD_POP, "Pop", job="a-job-the-queue-never-held")
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()
    counts(planned(machine), write=1)


# ═══════════════════════════════════════════════════════════════════════════
# 2b. The exact reader that keeps a failed read apart
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture(scope="module")
def id3_silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("id3"), ".aiff")


def test_the_checked_exact_reader_answers_every_value_as_its_sibling_does(
    tmp_path, silence, id3_silence
):
    from mutagen.aiff import AIFF
    from mutagen.flac import FLAC
    from mutagen.id3 import TCON

    listed = tmp_path / "listed.flac"
    shutil.copy2(silence, listed)
    handle = FLAC(listed)
    handle["genre"] = [OLD_POP, "Deep House"]
    handle.save()
    framed = tmp_path / "framed.aiff"
    shutil.copy2(id3_silence, framed)
    frame = AIFF(framed)
    if frame.tags is None:
        frame.add_tags()
    frame.tags.add(TCON(encoding=3, text=[OLD_POP, "Deep House"]))
    frame.save()

    for path in (listed, framed):
        assert tags.read_tag_values_checked(path, "genre") == (OLD_POP, "Deep House")
        assert tags.read_tag_values(path, "genre") == (OLD_POP, "Deep House")


def test_the_checked_exact_reader_reads_an_absent_field_as_absent(tmp_path, silence):
    bare = tmp_path / "bare.flac"
    shutil.copy2(silence, bare)
    assert tags.read_tag_values_checked(bare, "genre") is None
    assert tags.read_tag_values(bare, "genre") is None


def test_a_read_that_failed_is_raised_by_the_checked_reader_and_absent_to_its_sibling(tmp_path):
    broken = tmp_path / "broken.flac"
    broken.write_bytes(b"not a container at all")
    unknown = tmp_path / "notes.txt"
    unknown.write_text("no container", encoding="utf-8")
    gone = tmp_path / "gone.flac"
    for path in (broken, unknown, gone):
        with pytest.raises(tags.TagReadFailed):
            tags.read_tag_values_checked(path, "genre")
        assert tags.read_tag_values(path, "genre") is None


def test_both_exact_readers_refuse_a_field_the_table_does_not_name(tmp_path, silence):
    for reader in (tags.read_tag_values, tags.read_tag_values_checked):
        with pytest.raises(ValueError, match="unknown tag field"):
            reader(tmp_path / "any.flac", "bpm")


def test_a_genre_frame_holding_two_values_is_two_values_on_an_id3_container(
    machine, id3_silence
):
    """The plan reads every value on every container, so a second genre in a
    frame is seen as one and the file is left."""
    from mutagen.aiff import AIFF
    from mutagen.id3 import TCON

    path = music(machine) / "a pop record.aiff"
    shutil.copy2(id3_silence, path)
    frame = AIFF(path)
    if frame.tags is None:
        frame.add_tags()
    frame.tags.add(TCON(encoding=3, text=[OLD_POP, "Deep House"]))
    frame.save()
    record(machine, path, OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, changed_since=1)
    assert plan.items[0].current == f"{OLD_POP} | Deep House"


def test_an_id3_container_carrying_one_genre_is_planned_and_rewritten(machine, id3_silence):
    path = music(machine) / "a pop record.aiff"
    shutil.copy2(id3_silence, path)
    assert tags.write_genre(path, OLD_POP)
    record(machine, path, OLD_POP, word="Pop")
    plan = planned(machine)
    counts(plan, write=1)
    assert did(remap.apply(machine, plan)) == remap.Written(written=1, read_back=1)
    assert genre_of(path) == NEW_POP


# ═══════════════════════════════════════════════════════════════════════════
# 3. A taxonomy with no table
# ═══════════════════════════════════════════════════════════════════════════


def shipped_text_with_no_vocabulary() -> str:
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    text = source.read_text(encoding="utf-8")
    head, marker, _table = text.partition("\n[vocabulary.deezer]\n")
    assert marker, "the shipped template no longer declares the table where this test cuts"
    return head + "\n"


def test_a_taxonomy_with_no_table_plans_nothing_and_says_it_declares_none(machine, silence):
    before = taxonomy.load_taxonomy(shipped_text_with_no_vocabulary())
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    tagged(machine, silence, "an alternative record", OLD_ALTERNATIVE, "Alternative")
    plan = planned(machine, before)
    counts(plan, agree=2)
    assert plan.declared is False
    assert planned(machine).declared is True


# ═══════════════════════════════════════════════════════════════════════════
# 4. The digest
# ═══════════════════════════════════════════════════════════════════════════


def test_two_plans_over_one_unchanged_queue_digest_equal(machine, silence):
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    tagged(machine, silence, "a rock record", "Rock", "Rock")
    assert planned(machine).digest == planned(machine).digest


def test_the_digest_moves_when_one_files_genre_moves(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    before = planned(machine).digest
    assert tags.write_genre(path, "Deep House")
    assert planned(machine).digest != before


def test_the_digest_moves_when_only_a_count_moves(machine, silence):
    """A file that agrees is in no item, so only the counts carry it."""
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    before = planned(machine)
    tagged(machine, silence, "a rock record", "Rock", "Rock")
    after = planned(machine)
    assert after.items == before.items
    assert after.digest != before.digest


def test_the_digest_moves_when_a_record_becomes_unreadable(machine, silence):
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    before = planned(machine).digest
    directory = jobs.store_dir(machine) / artifacts.ARTIFACTS_DIRNAME / "job-a"
    (directory / "0009.json").write_text("{", encoding="utf-8")
    assert planned(machine).digest != before


def test_the_digest_covers_whether_the_taxonomy_declares_a_table():
    held = dict.fromkeys(remap.OUTCOMES, 0)
    assert (
        remap.RemapPlan((), held, declared=True).digest
        != remap.RemapPlan((), held, declared=False).digest
    )


# ═══════════════════════════════════════════════════════════════════════════
# 5. The write
# ═══════════════════════════════════════════════════════════════════════════


def test_the_apply_writes_the_planned_genre_and_no_other_file(machine, silence):
    pop = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    alternative = tagged(machine, silence, "an alternative record", OLD_ALTERNATIVE, "Alternative")
    by_hand = tagged(machine, silence, "by hand", OLD_POP, "Pop", now="Deep House")
    shop = tagged(machine, silence, "a shop's", OLD_POP, "Pop", source=SHOP)
    rock = tagged(machine, silence, "a rock record", "Rock", "Rock")

    written = remap.apply(machine, planned(machine))

    assert did(written) == remap.Written(written=2, read_back=2)
    assert written.clean
    assert {p.stem: genre_of(p) for p in (pop, alternative, by_hand, shop, rock)} == {
        "a pop record": NEW_POP,
        "an alternative record": NEW_ALTERNATIVE,
        "by hand": "Deep House",
        "a shop's": OLD_POP,
        "a rock record": "Rock",
    }


def test_the_apply_changes_the_genre_and_no_other_tag(machine, silence):
    path = a_file(machine, silence, "a pop record", OLD_POP)
    assert tags.write_tags(path, {"artist": "an artist", "title": "a title", "isrc": "USRC17607839"})
    record(machine, path, OLD_POP, word="Pop")
    remap.apply(machine, planned(machine))
    assert tags.read_tags(path, ("genre", "artist", "title", "isrc")) == {
        "genre": NEW_POP, "artist": "an artist", "title": "a title", "isrc": "USRC17607839",
    }  # fmt: skip


def test_a_second_plan_after_the_apply_agrees_and_writes_nothing(machine, silence):
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    remap.apply(machine, planned(machine))
    again = planned(machine)
    counts(again, agree=1)
    assert did(remap.apply(machine, again)) == remap.Written(written=0, read_back=0)


def test_a_rewrite_is_recorded_as_a_tagging_record_of_its_own(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    plan = planned(machine)
    remap.apply(machine, plan)
    reports, _unread = artifacts.every_committed(machine)
    (mine,) = [report for job, report in reports if job == f"remap-{plan.digest}"]
    assert mine == {
        "item": str(path),
        "path": str(path),
        "genre_written": NEW_POP,
        "skipped": None,
        "source": CATALOGUE,
        "source_genre": "Pop",
        "remapped_from": OLD_POP,
        "generation": 1,
    }
    staging = jobs.store_dir(machine) / artifacts.STAGING_DIRNAME / f"remap-{plan.digest}"
    assert not list(staging.rglob("*.json")), "the record was staged and never put in place"


def with_pop_written_as(tag: str) -> taxonomy.Taxonomy:
    """The shipped template with the general catalogue's Pop given another genre."""
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    raw = tomllib.loads(source.read_text(encoding="utf-8"))
    for row in raw["vocabulary"][CATALOGUE]["words"]:
        if row["word"] == "Pop":
            row["tag"] = tag
    return taxonomy.build_taxonomy(raw)


def test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again(
    machine, silence
):
    """What the review found. With no record of its own write, a rewritten file
    read as edited by hand, and a second change of the word left it for good."""
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    remap.apply(machine, planned(machine))
    assert genre_of(path) == NEW_POP

    moved = with_pop_written_as("Folk")
    plan = planned(machine, moved)

    counts(plan, write=1)
    assert plan.items == (
        remap.Item(str(path), "Pop", NEW_POP, NEW_POP, "Folk", "write", generation=1),
    )
    assert did(remap.apply(machine, plan)) == remap.Written(written=1, read_back=1)
    assert genre_of(path) == "Folk"
    counts(planned(machine, moved), agree=1)
    generations = sorted(
        report.get("generation", 0) for _job, report in artifacts.every_committed(machine)[0]
    )
    assert generations == [0, 1, 2]


def test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone(machine, silence):
    """What the second review drove. The record the rewrite replaced still
    matched the file, so the undo a person made was planned for rewrite again
    on every run."""
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    remap.apply(machine, planned(machine))
    assert tags.write_genre(path, OLD_POP)

    plan = planned(machine)

    counts(plan, changed_since=1)
    assert plan.items == (
        remap.Item(str(path), "Pop", NEW_POP, OLD_POP, NEW_POP, "leave", "changed-since"),
    )
    assert did(remap.apply(machine, plan)) == remap.Written(written=0, read_back=0)
    assert genre_of(path) == OLD_POP


def test_a_word_given_its_first_genre_back_is_still_followed(machine, silence):
    """A rewrite's record is in force however its genre compares with an older
    record's. The genre goes there and back, and then moves a third time."""
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    remap.apply(machine, planned(machine))
    back = with_pop_written_as(OLD_POP)
    remap.apply(machine, planned(machine, back))
    assert genre_of(path) == OLD_POP
    counts(planned(machine, back), agree=1)

    third = planned(machine)

    counts(third, write=1)
    assert third.items[0].generation == 2
    remap.apply(machine, third)
    assert genre_of(path) == NEW_POP


@pytest.mark.parametrize("generation", [True, -1, "2", 1.5, None])
def test_a_generation_that_is_not_a_positive_whole_number_is_a_tagging_jobs(generation):
    (read,) = remap.recorded(
        [("job-a", {"path": "/a", "genre_written": "Rock", "generation": generation})]
    )
    assert read.generation == 0


def test_the_rewritten_items_are_carried_for_the_undo(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    written = remap.apply(machine, planned(machine))
    assert [(item.path, item.current, item.wanted) for item in written.rewritten] == [
        (str(path), OLD_POP, NEW_POP)
    ]


def test_a_file_that_was_not_rewritten_gets_no_record(machine, silence, monkeypatch):
    stuck = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    monkeypatch.setattr(tags, "write_genre", lambda path, genre: False)
    plan = planned(machine)
    remap.apply(machine, plan)
    reports, _unread = artifacts.every_committed(machine)
    assert [job for job, _report in reports] == ["job-a"]
    assert genre_of(stuck) == OLD_POP


def test_a_record_that_cannot_be_committed_is_named_and_the_file_stays_rewritten(
    machine, silence, monkeypatch
):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    plan = planned(machine)

    def refuse_to_write(_cfg, _name, _ordinal, _report):
        raise OSError("the queue's volume is full")

    monkeypatch.setattr(artifacts, "commit", refuse_to_write)
    written = remap.apply(machine, plan)
    assert did(written) == remap.Written(written=1, read_back=1, unrecorded=(str(path),))
    assert not written.clean
    assert genre_of(path) == NEW_POP


def test_a_file_that_moved_since_the_plan_is_named_and_not_written(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    other = tagged(machine, silence, "another pop record", OLD_POP, "Pop")
    plan = planned(machine)
    assert tags.write_genre(path, "Deep House")
    written = remap.apply(machine, plan)
    assert did(written) == remap.Written(written=1, read_back=1, moved=(str(path),))
    assert genre_of(path) == "Deep House"
    assert genre_of(other) == NEW_POP


def test_a_file_the_writer_could_not_write_is_named_as_untouched_and_the_rest_are_written(
    machine, silence, monkeypatch
):
    """The writer's own answer is kept. A file it did not write is not counted
    as written and is not reported as one that failed to read back."""
    stuck = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    fine = tagged(machine, silence, "another pop record", OLD_POP, "Pop")
    real = tags.write_genre
    monkeypatch.setattr(
        tags, "write_genre", lambda path, genre: path != stuck and real(path, genre)
    )
    written = remap.apply(machine, planned(machine))
    assert did(written) == remap.Written(written=1, read_back=1, failed=(str(stuck),))
    assert genre_of(stuck) == OLD_POP
    assert genre_of(fine) == NEW_POP


def test_a_file_written_that_does_not_read_back_is_named_as_wrong(machine, silence, monkeypatch):
    """The writer said yes and the file does not carry the genre."""
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    monkeypatch.setattr(tags, "write_genre", lambda _path, _genre: True)
    written = remap.apply(machine, planned(machine))
    assert did(written) == remap.Written(written=1, read_back=0, wrong=(str(path),))
    reports, _unread = artifacts.every_committed(machine)
    assert [job for job, _report in reports] == ["job-a"]


def test_only_a_planned_write_is_written(machine, silence):
    """A left item carries a wanted genre for a person to read, and no write."""
    path = tagged(machine, silence, "by hand", OLD_POP, "Pop", now="Deep House")
    plan = planned(machine)
    assert plan.items[0].wanted == NEW_POP
    assert did(remap.apply(machine, plan)) == remap.Written(written=0, read_back=0)
    assert genre_of(path) == "Deep House"


# ═══════════════════════════════════════════════════════════════════════════
# 6. The verb, through the dispatcher
# ═══════════════════════════════════════════════════════════════════════════


def two_acts(option: str = "apply") -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, option, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *VERB])
    return code, acted, refused


def codes(envelope: dict) -> list[str]:
    return [warning["code"] for warning in envelope.get("warnings") or ()]


def message(envelope: dict, code: str) -> str:
    (found,) = [w["message"] for w in envelope["warnings"] if w["code"] == code]
    return found


def test_the_registry_declares_the_verb_as_a_file_write_behind_an_explicit_gate():
    entry = registry.entry("tag.remap")
    assert entry.writes == frozenset({"files"})
    assert entry.destructive is True
    (gate,) = entry.gates
    assert (gate.name, gate.explicit, gate.digest_source) == (GATE, True, "plan")
    assert remap_cli.CONFIRM_GATE == GATE


def test_the_verb_asks_before_it_writes_and_the_gate_shows_the_plan(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert genre_of(path) == OLD_POP
    shown = refused["cause"]["detail"]["shown"]
    assert shown["digest"] == planned(machine).digest
    assert shown["outcomes"]["write"] == 1
    assert shown["pairs"] == [{"from": OLD_POP, "to": NEW_POP, "files": 1}]
    assert shown["source"] == CATALOGUE


def test_the_gate_takes_no_inline_answer(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    code, _refused = drive(["-d", f"{GATE}=apply", *VERB])
    assert code != int(ExitCode.OK)
    assert genre_of(path) == OLD_POP


def test_an_approved_plan_is_written_and_the_run_names_the_verb_the_rows_follow_by(
    machine, silence
):
    pop = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    alternative = tagged(machine, silence, "an alternative record", OLD_ALTERNATIVE, "Alternative")
    shop = tagged(machine, silence, "a shop's", OLD_POP, "Pop", source=SHOP)

    code, acted, refused = two_acts()

    assert code == int(ExitCode.OK), acted
    # The plan the person approved is the plan that was applied.
    shown = refused["cause"]["detail"]["shown"]
    assert shown["digest"] == acted["data"]["digest"]
    assert shown["items"] == acted["data"]["items"]
    assert (genre_of(pop), genre_of(alternative), genre_of(shop)) == (
        NEW_POP, NEW_ALTERNATIVE, OLD_POP,
    )  # fmt: skip
    totals = acted["data"]["totals"]
    assert (totals["written"], totals["read_back"], totals["files"]) == (2, 2, 2)
    assert totals["outcomes"]["write"] == 2
    said = message(acted, "remap-genre-written")
    assert "2 file(s)" in said and "crate tag rows" in said and "2 read back" in said
    assert [item["path"] for item in acted["data"]["items"]] == [str(pop), str(alternative)]
    assert {item["current"] for item in acted["data"]["items"]} == {OLD_POP, OLD_ALTERNATIVE}


def test_an_empty_plan_still_asks_and_then_writes_nothing(machine):
    code, acted, _refused = two_acts()
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert codes(acted) == ["remap-nothing-to-write"]
    assert "0 of 0 file(s)" in message(acted, "remap-nothing-to-write")


def test_an_abort_writes_nothing(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    code, acted, _refused = two_acts("abort")
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert genre_of(path) == OLD_POP
    assert "remap-genre-written" not in codes(acted)


def test_a_file_changed_after_the_answer_makes_the_decision_stale(machine, silence):
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    other = tagged(machine, silence, "another pop record", OLD_POP, "Pop")
    code, refused = drive(VERB)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert tags.write_genre(path, "Deep House")

    code, stale = drive(["--run", run_id, *VERB])

    assert code == int(ExitCode.DECISION_STALE), stale
    assert (genre_of(path), genre_of(other)) == ("Deep House", OLD_POP)


def test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path(machine, silence):
    tagged(machine, silence, "by hand", OLD_POP, "Pop", now="Deep House")
    tagged(machine, silence, "an indie record", OLD_ALTERNATIVE, "Indie Rock")
    record(machine, music(machine) / "gone.flac", OLD_POP, word="Pop")

    code, acted, _refused = two_acts()

    assert code == int(ExitCode.OK), acted
    assert codes(acted) == ["remap-nothing-to-write", "remap-left-alone", "remap-file-not-read"]
    left = message(acted, "remap-left-alone")
    assert "2 file(s)" in left and "1 changed-since, 1 word-declined" in left
    unread = message(acted, "remap-file-not-read")
    assert "1 of 3 file(s)" in unread and "1 file-missing" in unread
    assert [item["reason"] for item in acted["data"]["items"]] == [
        "word-declined", "changed-since", "file-missing",
    ]  # fmt: skip


def test_a_run_that_wrote_still_says_what_it_left(machine, silence):
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    tagged(machine, silence, "by hand", OLD_POP, "Pop", now="Deep House")
    code, acted, _refused = two_acts()
    assert code == int(ExitCode.OK), acted
    assert codes(acted) == ["remap-genre-written", "remap-left-alone"]


def test_a_record_that_could_not_be_parsed_is_said(machine, silence):
    tagged(machine, silence, "a rock record", "Rock", "Rock")
    directory = jobs.store_dir(machine) / artifacts.ARTIFACTS_DIRNAME / "job-a"
    (directory / "0005.json").write_text("{", encoding="utf-8")
    code, acted, _refused = two_acts()
    assert code == int(ExitCode.OK), acted
    assert "remap-records-unread" in codes(acted)
    assert acted["data"]["totals"]["records_unread"] == 1


def test_an_active_taxonomy_with_no_table_says_so_and_plans_nothing(machine, silence):
    """The library's copy before the attended edit. A clean answer there would
    read as a library already corrected."""
    active = config.state_path("taxonomy_active", machine)
    active.parent.mkdir(parents=True, exist_ok=True)
    active.write_text(shipped_text_with_no_vocabulary(), encoding="utf-8")
    path = tagged(machine, silence, "a pop record", OLD_POP, "Pop")

    code, acted, _refused = two_acts()

    assert code == int(ExitCode.OK), acted
    assert codes(acted) == ["remap-nothing-to-write", "remap-no-vocabulary"]
    said = message(acted, "remap-no-vocabulary")
    assert "[vocabulary.deezer]" in said
    # The table alone would not load: its Pop row's tag needs an alias and a
    # map row the copy does not have yet, and the message has to say so.
    assert "routing alias" in said and "sub_by_source map row" in said
    assert genre_of(path) == OLD_POP


def test_the_shipped_table_alone_does_not_load_on_a_copy_from_before_it(machine):
    """Why the message above names the alias and the map row."""
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    shipped = tomllib.loads(source.read_text(encoding="utf-8"))
    before = tomllib.loads(shipped_text_with_no_vocabulary())
    bucket = next(b for b in before["bucket"] if b["id"] == "non_electronic")
    bucket["aliases"].remove("NonElectronic / Pop")
    bucket["sub_by_source"]["map"] = [
        row for row in bucket["sub_by_source"]["map"] if row["source"] != "NonElectronic / Pop"
    ]
    taxonomy.build_taxonomy(before)
    before["vocabulary"] = shipped["vocabulary"]
    with pytest.raises(taxonomy.TaxonomyError) as caught:
        taxonomy.build_taxonomy(before)
    assert any("is filed by no exact declaration" in p for p in caught.value.problems)


def test_the_shipped_template_declares_the_table_so_the_warning_is_not_given(machine, silence):
    tagged(machine, silence, "a rock record", "Rock", "Rock")
    _code, acted, _refused = two_acts()
    assert "remap-no-vocabulary" not in codes(acted)


def test_a_write_that_does_not_take_refuses_after_the_rest_were_written(
    machine, silence, monkeypatch
):
    stuck = tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    fine = tagged(machine, silence, "another pop record", OLD_POP, "Pop")
    real = tags.write_genre
    monkeypatch.setattr(
        tags, "write_genre", lambda path, genre: path != stuck and real(path, genre)
    )

    code, acted, _refused = two_acts()

    assert code == int(ExitCode.PRECONDITION), acted
    cause = acted["cause"]
    assert cause["reason"] == "tag-remap-unwritten"
    assert cause["detail"] == {
        "wrong": [], "moved": [], "failed": [str(stuck)], "unrecorded": [],
        "written": 1, "read_back": 1,
        # The undo for the file that did take, which no later run lists.
        "rewritten": [{"path": str(fine), "from": OLD_POP, "to": NEW_POP}],
    }  # fmt: skip
    assert "1 file(s) were rewritten and read back" in cause["message"]
    assert "1 could not be written and are untouched" in cause["message"]
    assert genre_of(fine) == NEW_POP
    # The file that WAS rewritten has a stale row, and this run is the only
    # one that will ever say so: the next one finds it agreeing.
    assert any("crate tag rows" in step for step in cause["remediation"]["steps"])


def test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb(
    machine, silence, monkeypatch
):
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    monkeypatch.setattr(tags, "write_genre", lambda _path, _genre: False)
    code, acted, _refused = two_acts()
    assert code == int(ExitCode.PRECONDITION), acted
    assert not any("crate tag rows" in step for step in acted["cause"]["remediation"]["steps"])


def test_a_file_outside_the_library_is_said_and_not_listed(machine, silence, tmp_path):
    tagged(machine, silence, "a rock record", "Rock", "Rock")
    record(machine, tmp_path / "staging" / "a pop record.flac", OLD_POP, word="Pop")
    code, acted, _refused = two_acts()
    assert code == int(ExitCode.OK), acted
    assert codes(acted) == ["remap-nothing-to-write", "remap-outside-library"]
    assert "1 of 2 file(s)" in message(acted, "remap-outside-library")
    assert acted["data"]["items"] == []
    assert acted["data"]["totals"]["outcomes"]["outside-library"] == 1


def test_the_refusal_names_a_few_files_and_carries_them_all():
    moved = tuple(f"/music/{n}.flac" for n in range(8))
    with pytest.raises(CratekitError) as caught:
        remap_cli.assert_written(remap.Written(written=3, read_back=3, moved=moved))
    cause = caught.value.cause
    assert cause.reason == "tag-remap-unwritten"
    assert "/music/4.flac and 3 more" in cause.message and "/music/5.flac" not in cause.message
    assert cause.detail["moved"] == list(moved)


@pytest.mark.parametrize(
    ("field", "said"),
    [
        ("moved", "carried something else"),
        ("failed", "could not be written and are untouched"),
        ("wrong", "do not read back"),
        ("unrecorded", "no record of the rewrite could be committed"),
    ],
)
def test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which(field, said):
    written = remap.Written(written=1, read_back=1, **{field: ("/music/one.flac",)})
    with pytest.raises(CratekitError) as caught:
        remap_cli.assert_written(written)
    cause = caught.value.cause
    assert said in cause.message
    assert cause.detail[field] == ["/music/one.flac"]
    assert sum(bool(cause.detail[name]) for name in ("moved", "failed", "wrong", "unrecorded")) == 1


def test_a_clean_write_is_not_refused():
    remap_cli.assert_written(remap.Written(written=3, read_back=3))


def test_a_person_reads_the_counts_and_the_pairs_at_the_gate(machine, silence):
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    code, text = drive_human(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert NEW_POP in text and OLD_POP in text


def test_the_plan_payload_is_json_and_round_trips(machine, silence):
    tagged(machine, silence, "a pop record", OLD_POP, "Pop")
    _code, refused = drive(VERB)
    assert json.loads(json.dumps(refused)) == refused
