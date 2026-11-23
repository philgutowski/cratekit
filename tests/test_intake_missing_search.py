"""U79: a row nothing names exactly gets provider candidates, and never a pick.

Everything but the catalogue is real. D1 applies.
"""

# ruff: noqa: F811 - the fixtures are imported from the ISRC suite by name
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from cratekit.acquire import listdoc, match
from cratekit.cli import registry
from cratekit.core import config, review
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import candidates, missing_cli
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, UnreadableCatalogue, catalogue_factory
from tests.test_intake_missing_isrc import cfg, fresh_cache, library  # noqa: F401 - fixtures

SUN = ("Aurora Bloom", "Sun Path")
TIDE = ("Nova Reef", "Tide")
GLASS = ("Mira Vale", "Glass Hour")


class Hit:
    """A provider search hit in the shape the provider reader reads."""

    def __init__(
        self, track_id: str, artist: str, name: str, *, version: str = "", album: str = ""
    ) -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = ""
        if version:
            self.version = version
        if album:
            self.album = {"name": album}


def bind(monkeypatch, fake: FakeCatalogue) -> FakeCatalogue:
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def searching(monkeypatch, searches: dict) -> FakeCatalogue:
    """A catalogue answering ``searches`` bound as the provider."""
    return bind(monkeypatch, FakeCatalogue(searches=searches))


def tracklist(tmp_path: Path, *lines: str, name: str = "typed.txt") -> Path:
    path = tmp_path / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def found(path: Path, *extra: str) -> tuple[int, dict]:
    return drive(["intake", "missing", "--list", str(path), *extra])


def ok(path: Path, *extra: str) -> tuple[dict, dict]:
    code, envelope = found(path, *extra)
    assert code == int(ExitCode.OK), envelope
    return envelope, envelope["data"]["summary"]


def refused(path: Path, *extra: str) -> dict:
    code, envelope = found(path, *extra)
    assert code == int(ExitCode.PRECONDITION), envelope
    return envelope


def ids(summary: dict) -> list[str]:
    return [t["id"] for t in json.loads(Path(summary["list"]).read_text())["tracks"]]


def lists_dir(library: Path) -> Path:
    return library.parent / "staging" / missing_cli.LISTS_DIR


def owned(library: Path, name: str) -> None:
    (library / "Music" / name).write_bytes(b"")


def checks(envelope: dict) -> dict[str, dict]:
    return {c["key"].removeprefix("intake.missing."): c for c in envelope["data"]["checks"]}


def items_of(cfg: config.Config) -> list[review.Item]:
    with review.open_store(cfg) as store:
        return list(review.list_items(store, queue=candidates.QUEUE, include_resolved=True).items)


def the_item(cfg: config.Config) -> review.Item:
    held = [one for one in items_of(cfg) if one.kind == candidates.KIND]
    assert len(held) == 1, held
    return held[0]


def resolve(item_id: str, verdict: str, *extra: str) -> None:
    code, envelope = drive(["review", "resolve", item_id, "--verdict", verdict, *extra])
    assert code == int(ExitCode.OK), envelope


# One exact candidate is listed without review


def test_one_exact_candidate_is_listed_without_review(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    fake = searching(monkeypatch, {SUN: [
        Hit("7001", "Aurora Bloom", "Sun Path"),
        Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix"),
        Hit("7003", "Someone Else", "Sun Path"),
    ]})
    envelope, summary = ok(path)
    assert fake.searched_for == [SUN]
    assert (summary["written"], summary["by_search"], summary["candidates_offered"]) == (1, 1, 0)
    assert Path(summary["list"]).parent == lists_dir(library)
    assert re.fullmatch(r"typed-found-[0-9a-f]{12}\.list\.json", Path(summary["list"]).name)
    body = json.loads(Path(summary["list"]).read_text())
    assert [(t["id"], t["artist"], t["title"]) for t in body["tracks"]] == [
        ("7001", "Aurora Bloom", "Sun Path")
    ]
    assert summary["next"] == f"crate acquire download {summary['list']}"
    manifest = json.loads(Path(summary["manifest"]).read_text())
    assert manifest["rows"]["7001"]["source"] == missing_cli.LIST_SOURCE
    assert manifest["rows"]["7001"]["source_ref"] == str(path)
    assert [one for one in items_of(cfg) if one.kind == candidates.KIND] == []


def test_an_original_mix_row_and_a_bare_candidate_are_one_version(
    cfg, library, tmp_path, monkeypatch
):
    """The exact test is ``match``'s fold, so the null qualifier folds away."""
    path = tracklist(tmp_path, "AURORA BLOOM - Sun Path (Original Mix)")
    asked = ("AURORA BLOOM", "Sun Path")
    fake = searching(monkeypatch, {asked: [Hit("7001", "Aurora Bloom", "Sun Path")]})
    envelope = ok(path)[0]
    assert fake.searched_for == [asked], "the null version went into the query"
    assert envelope["data"]["summary"]["by_search"] == 1


def test_a_version_the_row_names_goes_into_the_query_and_into_the_exact_test(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)")
    fake = searching(monkeypatch, {("Aurora Bloom", "Sun Path Extended Mix"): [
        Hit("7001", "Aurora Bloom", "Sun Path"),
        Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix"),
    ]})
    envelope = ok(path)[0]
    assert fake.searched_for == [("Aurora Bloom", "Sun Path Extended Mix")]
    assert ids(envelope["data"]["summary"]) == ["7002"], "the plain cut was listed for a remix"


def test_the_same_exact_track_served_twice_is_one_candidate(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    searching(monkeypatch, {SUN: [Hit("7001", *SUN), Hit("7001", *SUN)]})
    envelope = ok(path)[0]
    assert envelope["data"]["summary"]["by_search"] == 1


# Two exact candidates are offered, not picked


def two_exact() -> FakeCatalogue:
    return FakeCatalogue(
        searches={
            SUN: [
                Hit("7001", "Aurora Bloom", "Sun Path", album="Sun Path"),
                Hit("7009", "Aurora Bloom", "Sun Path", album="Harbour Lights"),
            ]
        }
    )


def test_two_exact_candidates_are_offered_and_neither_is_picked(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    bind(monkeypatch, two_exact())
    envelope, summary = ok(path)
    assert (summary["list"], summary["written"], summary["candidates_offered"]) == (None, 0, 1)
    assert envelope["outcome"] == "ok", "a question put to a person read as nothing to do"
    assert not list(lists_dir(library).glob("*")), "a list was written over an open question"
    item = the_item(cfg)
    assert item.verdict is None
    assert item.handler_key == "intake.missing"
    assert [o.option_id for o in item.options] == ["7001", "7009"]
    assert [o.detail["exact"] for o in item.options] == [True, True]
    assert "Harbour Lights" in item.options[1].summary
    assert "2 tracks that match it exactly" in item.payload["why"]
    row = summary["rows"][0]
    assert (row["state"], row["item_id"], row["candidates"]) == (candidates.OFFERED, item.item_id, 2)
    check = checks(envelope)["candidates"]
    assert check["status"] == "fail"
    assert item.item_id in check["detail"]
    assert f"--queue {candidates.QUEUE} --kind {candidates.KIND}" in check["detail"]
    # AN ACCEPTANCE NAMING NEITHER of the two candidates lists nothing and says how to clear it.
    resolve(item.item_id, "accepted")
    envelope = refused(path)
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "without naming which of its 2 candidates" in envelope["cause"]["message"]
    assert "crate review clear" in " ".join(envelope["cause"]["remediation"]["steps"])
    assert not list(lists_dir(library).glob("*"))


def test_an_exact_candidate_beside_a_row_that_cannot_be_read_is_offered(
    cfg, library, tmp_path, monkeypatch
):
    """The unreadable row could be the second exact candidate, so nothing is picked."""
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    nameless = Hit("7004", "", "Sun Path")
    searching(monkeypatch, {SUN: [Hit("7001", "Aurora Bloom", "Sun Path"), nameless]})
    envelope = ok(path)[0]
    assert envelope["data"]["summary"]["written"] == 0
    item = the_item(cfg)
    assert [o.option_id for o in item.options] == ["7001"]
    assert item.payload["unreadable"] == 1
    assert "could not be read" in item.payload["why"]


def test_an_exact_candidate_beside_an_exact_one_with_no_identifier_is_offered(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    searching(monkeypatch, {SUN: [Hit("7001", *SUN), Hit("", *SUN)]})
    envelope = ok(path)[0]
    assert envelope["data"]["summary"]["written"] == 0
    item = the_item(cfg)
    assert [o.option_id for o in item.options] == ["7001"], "a track with no id was an option"
    assert "carries no identifier" in item.payload["why"]


def test_a_title_with_two_readings_is_offered_when_each_reading_has_a_candidate(
    cfg, library, tmp_path, monkeypatch
):
    """``Sun Path - Dub`` may be a dub version or a title ending in Dub."""
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path - Dub")
    wanted = match.read_text_lines("Aurora Bloom - Sun Path - Dub")[0]
    assert wanted.other_reading is not None, "the fixture title is not ambiguous"
    searching(monkeypatch, {(wanted.artist, candidates.query_title(wanted)): [
        Hit("7001", "Aurora Bloom", "Sun Path", version="Dub"),
        Hit("7002", "Aurora Bloom", "Sun Path Dub"),
    ]})
    envelope = ok(path)[0]
    assert envelope["data"]["summary"]["written"] == 0
    assert sorted(o.option_id for o in the_item(cfg).options) == ["7001", "7002"]


# A near miss is offered with its score and never listed until accepted


def near_miss() -> FakeCatalogue:
    return FakeCatalogue(
        searches={
            SUN: [
                Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix"),
                Hit("7005", "Aurora Bloome", "Sun Path"),
                Hit("7006", "Quite Another Act", "Wholly Different"),
            ]
        }
    )


def test_a_near_miss_is_offered_with_its_score_and_is_not_listed(
    cfg, library, tmp_path, monkeypatch
):
    """A near miss is offered, asked once however often it is listed, and listed as accepted."""
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    fake = bind(monkeypatch, near_miss())
    envelope, summary = ok(path)
    assert (summary["written"], summary["by_search"], summary["candidates_offered"]) == (0, 0, 1)
    item = the_item(cfg)
    # A perfect score is still not a pick: the extended mix is another version.
    shown = {o.option_id: o.detail for o in item.options}
    assert shown["7002"]["score"] == 100.0 and shown["7002"]["exact"] is False
    assert candidates.CANDIDATE_FLOOR <= shown["7005"]["score"] < 100.0
    assert "7006" not in shown, "a hit resembling nothing was put on the screen"
    assert [o.option_id for o in item.options] == ["7002", "7005"], "best score first"
    assert "score 100" in item.options[0].summary
    assert "never picked from a score" in item.payload["why"]
    # A SECOND RUN offers nothing new and spends no search.
    envelope = ok(path)[0]
    assert fake.searched_for == [SUN], "an open question was searched for again"
    again = the_item(cfg)
    assert (again.item_id, again.updated) == (item.item_id, item.updated)
    assert envelope["data"]["summary"]["rows"][0]["state"] == candidates.WAITING
    # THE SAME ROW IN ANOTHER LIST is the same question.
    found(tracklist(tmp_path, "1. aurora bloom - SUN PATH", name="two.txt"))
    the_item(cfg)
    # AN ACCEPTED CANDIDATE is listed by the next run, as the candidate's row.
    resolve(item.item_id, "accepted", "--option", "7005")
    envelope, summary = ok(path)
    assert fake.searched_for == [SUN], "an answered row was searched for again"
    assert (summary["written"], summary["by_review"], summary["by_search"]) == (1, 1, 0)
    body = json.loads(Path(summary["list"]).read_text())
    assert [(t["id"], t["artist"], t["title"]) for t in body["tracks"]] == [
        ("7005", "Aurora Bloome", "Sun Path")
    ]
    assert checks(envelope)["candidates"]["status"] == "ok"


# An accepted candidate is listed by the next run


def test_an_acceptance_of_the_only_candidate_needs_no_option(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    searching(monkeypatch, {SUN: [Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix")]})
    found(path)
    resolve(the_item(cfg).item_id, "accepted")
    envelope = ok(path)[0]
    assert ids(envelope["data"]["summary"]) == ["7002"]


def test_an_accepted_candidate_the_library_now_holds_is_not_listed_again(
    cfg, library, tmp_path, monkeypatch
):
    """The row stays missing for ever when the candidate is another spelling."""
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    searching(monkeypatch, {
        SUN: [Hit("7005", "Aurora Bloom and the Reef Players", "Sun Path")],
        TIDE: [Hit("7010", "Nova Reef", "Tide")],
    })
    found(path)
    resolve(the_item(cfg).item_id, "accepted", "--option", "7005")
    owned(library, "Aurora Bloom and the Reef Players - Sun Path.flac")
    intake_cli.reset_cache()
    envelope, summary = ok(path)
    assert ids(summary) == ["7010"], "a held track was listed for download"
    assert (summary["by_review"], summary["in_library"]) == (0, 1)
    assert [r["state"] for r in summary["rows"]] == [candidates.HELD, candidates.LISTED]
    assert "already in the library" in checks(envelope)["accepted"]["detail"]


def test_a_rejected_row_is_reported_and_never_searched_again(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    fake = searching(monkeypatch, {
        SUN: [Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix")],
        TIDE: [Hit("7010", "Nova Reef", "Tide")],
    })
    found(path)
    resolve(the_item(cfg).item_id, "rejected")
    fake.searched_for.clear()
    envelope = ok(path)[0]
    assert fake.searched_for == [TIDE]
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["unfound"]) == (1, 1)
    check = checks(envelope)["unfound"]
    assert check["status"] == "fail"
    assert "rejected in review" in check["detail"]


# No candidates is reported, not silent


def test_no_candidate_beside_a_listed_row_is_a_failing_check(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Mira Vale - Glass Hour")
    bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", "Aurora Bloom", "Sun Path")]}))
    envelope, summary = ok(path)
    assert (summary["written"], summary["unfound"]) == (1, 1)
    check = checks(envelope)["unfound"]
    assert check["status"] == "fail"
    assert "Mira Vale - Glass Hour" in check["detail"]
    assert "returned nothing" in check["detail"]
    assert [r["state"] for r in summary["rows"]] == [candidates.LISTED, candidates.NO_CANDIDATES]


def test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Mira Vale - Glass Hour")
    searching(monkeypatch, {GLASS: [Hit("7006", "Quite Another Act", "Wholly Different")]})
    envelope = refused(path)
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "1 hit(s) and none that can be downloaded resembles it" in envelope["cause"]["message"]
    assert [one for one in items_of(cfg) if one.kind == candidates.KIND] == []


def test_a_provider_that_cannot_search_refuses_with_nothing_offered_or_written(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    bind(monkeypatch, UnreadableCatalogue())
    code, envelope = found(path)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "unavailable-transient"
    assert items_of(cfg) == []
    assert not lists_dir(library).exists() or not list(lists_dir(library).glob("*"))


def test_a_failure_on_the_second_row_leaves_the_first_row_unoffered(
    cfg, library, tmp_path, monkeypatch
):
    """Every answer is in hand before any offer, so a partial pass offers nothing."""
    class SecondFails(FakeCatalogue):
        def search_tracks(self, artist: str, title: str):
            if (artist, title) == TIDE:
                raise RuntimeError("the provider stopped answering")
            return super().search_tracks(artist, title)
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    bind(monkeypatch, SecondFails(searches=near_miss().searches))
    code, envelope = found(path)
    assert envelope["cause"]["reason"] == "unavailable-transient", (code, envelope)
    assert items_of(cfg) == []


# The library is asked first


def test_an_owned_row_is_never_searched_for(cfg, library, tmp_path, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    fake = searching(monkeypatch, {SUN: [Hit("7001", *SUN)], TIDE: [Hit("7010", *TIDE)]})
    envelope = ok(path)[0]
    assert fake.searched_for == [TIDE], "a track the library holds was searched for"
    summary = envelope["data"]["summary"]
    assert (summary["owned"], summary["missing"], summary["written"]) == (1, 1, 1)


def test_a_list_the_library_holds_entirely_is_a_no_op_that_spends_no_login(
    cfg, library, tmp_path, monkeypatch
):
    owned(library, "Aurora Bloom - Sun Path.flac")
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    def unreachable(_cfg):
        raise AssertionError("the catalogue was resolved with nothing to search for")
    monkeypatch.setattr(catalogue, "resolve", unreachable)
    envelope = ok(path)[0]
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["written"] == 0


def test_a_music_folder_that_is_not_there_refuses_rather_than_listing_everything(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    fake = bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", *SUN)]}))
    (library / "Music").rmdir()
    code, envelope = found(path)
    assert envelope["cause"]["reason"] == "library-volume-unmounted", (code, envelope)
    assert fake.searched_for == []


def test_the_same_line_twice_is_searched_once_and_listed_once(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Aurora Bloom - Sun Path")
    fake = bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", *SUN)]}))
    envelope = ok(path)[0]
    assert fake.searched_for == [SUN]
    assert envelope["data"]["summary"]["written"] == 1


# The unlisted list of an earlier run is the input, and the names do not collide


def test_the_unlisted_list_is_read_and_its_found_list_sits_beside_the_jobs(
    cfg, library, tmp_path, monkeypatch
):
    out = lists_dir(library)
    wanted = match.read_text_lines("Aurora Bloom - Sun Path")
    written = listdoc.write(
        out,
        "intake-j1",
        (),
        {},
        handed_on=[listdoc.HandedOn(listdoc.rows_of(wanted)[0], "it carries no ISRC")],
    )
    assert written.unlisted_path is not None
    bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", *SUN)]}))
    envelope = ok(written.unlisted_path)[0]
    listed = Path(envelope["data"]["summary"]["list"])
    assert listed.parent == out
    assert re.fullmatch(r"intake-j1-found-[0-9a-f]{12}\.list\.json", listed.name)


@pytest.mark.parametrize(
    ("given", "named"),
    [
        ("intake-j1.unlisted.json", "intake-j1-found"),
        ("warmup.list.json", "warmup-found"),
        ("friday set (2026).txt", "friday-set-2026-found"),
        ("notes", "notes-found"),
        (".txt", "txt-found"),
        ("§§§.txt", "tracklist-found"),
    ],
)
def test_the_found_list_is_named_for_its_input(given, named):
    name = missing_cli.found_name(Path("/somewhere") / given)
    assert re.fullmatch(re.escape(named) + r"-[0-9a-f]{12}", name), name


def test_a_folder_that_cannot_be_written_is_a_refusal_and_not_an_internal_error(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Nova Reef - Tide")
    bind(monkeypatch, FakeCatalogue(searches={TIDE: [Hit("7010", *TIDE)]}))
    out = tmp_path / "sealed"
    out.mkdir()
    out.chmod(0o500)
    try:
        code, envelope = found(path, "--out", str(out))
    finally:
        out.chmod(0o700)
    # A PERMISSION FAILURE KEEPS ITS OWN SLUG, as it does under label approved.
    assert code != int(ExitCode.INTERNAL), envelope
    assert envelope["cause"]["reason"] == "path-permission-denied"


def test_a_disk_that_refuses_the_write_is_this_verbs_refusal(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Nova Reef - Tide")
    bind(monkeypatch, FakeCatalogue(searches={TIDE: [Hit("7010", *TIDE)]}))
    def full(*_args, **_kwargs):
        raise OSError(28, "No space left on device", str(tmp_path / "x.list.json"))
    monkeypatch.setattr(listdoc, "write", full)
    envelope = refused(path)
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "could not be written" in envelope["cause"]["message"]


def test_skip_failed_means_nothing_for_a_list_and_is_refused(cfg, library, tmp_path):
    envelope = refused(tracklist(tmp_path, "Aurora Bloom - Sun Path"), "--skip-failed")
    assert envelope["cause"]["reason"] == "intake-list-unusable"


def test_the_verb_declares_that_it_adjudicates():
    assert registry.entry("intake.missing").adjudicates


# What the unit's review drove


def test_the_run_after_an_answer_lists_more_than_the_first_and_is_not_refused(
    cfg, library, tmp_path, monkeypatch
):
    """The run after an answer lists more under a new name rather than being refused."""
    path = tracklist(tmp_path, "Nova Reef - Tide", "Aurora Bloom - Sun Path")
    bind(
        monkeypatch,
        FakeCatalogue(
            searches={
                TIDE: [Hit("7010", *TIDE)],
                SUN: [Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix")],
            }
        ),
    )
    _code, first = found(path)
    # THE SAME WORK TWICE rewrites the same list.
    again = ok(path)[0]
    assert again["data"]["summary"]["list"] == first["data"]["summary"]["list"]
    assert len(list(lists_dir(library).glob("*.list.json"))) == 1
    resolve(the_item(cfg).item_id, "accepted", "--option", "7002")
    second = ok(path)[0]
    assert ids(second["data"]["summary"]) == ["7010", "7002"]
    assert second["data"]["summary"]["list"] != first["data"]["summary"]["list"]


def test_two_tracklists_of_one_file_name_in_two_folders_do_not_collide(
    cfg, library, tmp_path, monkeypatch
):
    (tmp_path / "friday").mkdir()
    (tmp_path / "saturday").mkdir()
    one = tracklist(tmp_path / "friday", "Nova Reef - Tide", name="tracklist.txt")
    two = tracklist(tmp_path / "saturday", "Aurora Bloom - Sun Path", name="tracklist.txt")
    bind(monkeypatch, FakeCatalogue(searches={TIDE: [Hit("7010", *TIDE)], SUN: [Hit("7001", *SUN)]}))
    found(one)
    ok(two)
    assert len(list(lists_dir(library).glob("tracklist-found-*.list.json"))) == 2


def test_a_missing_row_of_another_services_list_is_searched_for_and_not_dropped(
    cfg, library, tmp_path, monkeypatch
):
    """Its ref is that service's id, which the emitter writes as none, so it is searched."""
    path = tmp_path / "other.json"
    path.write_text(
        json.dumps(
            {
                "list": 1,
                "origin": "spotify",
                "tracks": [
                    {"track": {"id": "sp1", "name": "Sun Path", "artists": [{"name": "Aurora Bloom"}]}}
                ],
            }
        ),
        encoding="utf-8",
    )
    fake = bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", *SUN)]}))
    envelope = ok(path)[0]
    assert fake.searched_for == [SUN]
    assert ids(envelope["data"]["summary"]) == ["7001"], "another service's id was listed"


def test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    filler = [
        Hit(str(8000 + n), "Quite Another Act", f"Wholly Different {n}")
        for n in range(catalogue.TRACK_SEARCH_PAGE - 1)
    ]
    bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", *SUN), *filler]}))
    envelope = ok(path)[0]
    assert envelope["data"]["summary"]["written"] == 0
    item = the_item(cfg)
    assert [o.option_id for o in item.options] == ["7001"]
    assert "filled its page" in item.payload["why"]


def test_one_hit_short_of_a_full_page_is_a_whole_answer(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    filler = [
        Hit(str(8000 + n), "Quite Another Act", f"Wholly Different {n}")
        for n in range(catalogue.TRACK_SEARCH_PAGE - 2)
    ]
    bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", *SUN), *filler]}))
    envelope = ok(path)[0]
    assert envelope["data"]["summary"]["by_search"] == 1


@pytest.mark.parametrize(
    "hit",
    [
        Hit("7001", "Aurora Bloom", "Sun Path", version="Dub"),
        Hit("7002", "Aurora Bloom", "Sun Path - Dub"),
    ],
    ids=["the-version-reading", "the-title-reading"],
)
def test_a_title_with_two_readings_is_never_listed_on_one_candidate(
    hit, cfg, library, tmp_path, monkeypatch
):
    """The string cannot say which reading was meant, so no candidate is THE one."""
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path - Dub")
    wanted = match.read_text_lines("Aurora Bloom - Sun Path - Dub")[0]
    bind(
        monkeypatch,
        FakeCatalogue(searches={(wanted.artist, candidates.query_title(wanted)): [hit]}),
    )
    envelope = ok(path)[0]
    assert envelope["data"]["summary"]["written"] == 0
    item = the_item(cfg)
    assert [o.option_id for o in item.options] == [hit.id]
    assert item.options[0].detail["exact"] is True
    assert "reads two ways" in item.payload["why"]


def test_a_failed_search_says_which_offers_it_did_not_make(cfg, library, tmp_path, monkeypatch):
    """A version question the library raised is queued first, so the refusal may not say none."""
    owned(library, "Nova Reef - Tide (Extended Mix).flac")
    path = tracklist(tmp_path, "Nova Reef - Tide", "Aurora Bloom - Sun Path")
    bind(monkeypatch, UnreadableCatalogue())
    code, envelope = found(path)
    message = envelope["cause"]["message"]
    assert "no provider candidate was offered and no list was written" in message
    assert "nothing was offered" not in message
    assert [one.kind for one in items_of(cfg)] == [match.QUESTION_KIND]
    assert "take the row out of the list" in " ".join(envelope["cause"]["remediation"]["steps"])


def test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue(
    cfg, library, tmp_path, monkeypatch
):
    path = tmp_path / "mixed.json"
    path.write_text(
        json.dumps(
            {
                "list": 1,
                "origin": "spotify",
                "tracks": [
                    {
                        "track": {
                            "id": "sp1",
                            "name": "Tide",
                            "artists": [{"name": "Nova Reef"}],
                            "external_ids": {"isrc": "QZAAA2600001"},
                        }
                    },
                    {"track": {"id": "sp2", "name": "Sun Path", "artists": [{"name": "Aurora Bloom"}]}},
                ],
            }
        ),
        encoding="utf-8",
    )
    fake = FakeCatalogue(
        isrcs={"QZAAA2600001": [Hit("7010", *TIDE)]}, searches={SUN: [Hit("7001", *SUN)]}
    )
    resolved: list[object] = []
    def resolve_once(cfg_):
        resolved.append(cfg_)
        return fake
    monkeypatch.setattr(catalogue, "resolve", resolve_once)
    envelope = ok(path)[0]
    assert len(resolved) == 1, "one run restored the provider session twice"
    summary = envelope["data"]["summary"]
    assert (summary["by_isrc"], summary["by_search"], summary["written"]) == (1, 1, 2)
    assert ids(summary) == ["7010", "7001"]


# The proposal, below the verb


def answer_of(line: str, *hits: Hit) -> tuple[match.Wanted, candidates.Answer]:
    wanted = match.read_text_lines(line)[0]
    return wanted, candidates.read_answer(wanted, tuple(hits))


def test_more_candidates_than_the_screen_holds_are_truncated_and_counted(cfg):
    hits = [Hit(str(8000 + n), "Aurora Bloom", "Sun Path", album=f"Release {n}") for n in range(13)]
    wanted, answer = answer_of("Aurora Bloom - Sun Path", *hits)
    with review.open_store(cfg) as items:
        said = candidates.propose(items, wanted, answer, handler_key="intake.missing")
        held = review.get(items, said.item_id)
    assert said.state == candidates.OFFERED
    assert len(held.options) == candidates.OFFER_LIMIT == said.offered
    assert held.payload["withheld"] == 3
    assert held.payload["hits"] == 13


def test_an_exact_candidate_under_the_floor_of_nothing_is_still_first():
    """Exact outranks score, so a near miss scoring 100 never leads an exact one."""
    wanted, answer = answer_of(
        "Aurora Bloom - Sun Path",
        Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix"),
        Hit("7001", "Aurora Bloom", "Sun Path"),
        Hit("7009", "Aurora Bloom", "Sun Path"),
    )
    assert [one.track.ref for one in candidates.shown(answer)] == ["7001", "7009", "7002"]
    assert candidates.sole_exact(answer) is None


def test_the_only_exact_candidate_carrying_no_identifier_is_not_listed():
    """Two exact hits with no id share ONE id, the empty one, and must still not be listed."""
    wanted, answer = answer_of(
        "Aurora Bloom - Sun Path",
        Hit("", "Aurora Bloom", "Sun Path"),
        Hit("", "Aurora Bloom", "Sun Path"),
    )
    assert candidates.sole_exact(answer) is None


def test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance(cfg):
    wanted, answer = answer_of("Aurora Bloom - Sun Path", Hit("", "Aurora Bloom", "Sun Path"))
    with review.open_store(cfg) as items:
        said = candidates.propose(items, wanted, answer, handler_key="intake.missing")
    assert said.state == candidates.NO_CANDIDATES
    assert "1 that do resemble it carry no identifier" in said.reason


def test_an_accepted_option_that_does_not_carry_its_own_track_lists_nothing(cfg):
    """An option whose detail names another track is a download nobody accepted."""
    wanted = match.read_text_lines("Aurora Bloom - Sun Path")[0]
    other = match.read_row(Hit("9999", "Nova Reef", "Tide"), origin=match.TIDAL, position=1)
    with review.open_store(cfg) as items:
        held = review.offer(
            items,
            queue=candidates.QUEUE,
            kind=candidates.KIND,
            identity=candidates.identity(wanted),
            payload={},
            options=[
                review.Option(
                    option_id="7001", summary="one", detail={"track": intake_cli.frozen(other)}
                )
            ],
            handler_key="intake.missing",
        )
        review.resolve(items, held.item_id, review.Verdict.ACCEPTED, option="7001", actor="suite")
        said = candidates.settled(items, wanted)
    assert said is not None and said.state == candidates.STALLED
    assert said.track is None


def test_the_identity_is_the_folded_row_and_not_its_spelling():
    """Keyed on the folded row, and on a title's own identity, so an accepted ``💧`` is never
    listed for a later ``🌊`` row (review round one's fourth finding)."""
    one = match.read_text_lines("Aurora Bloom - Sun Path (Original Mix)")[0]
    two = match.read_text_lines("AURORA  BLOOM - sun path")[0]
    other = match.read_text_lines("Aurora Bloom - Sun Path (Extended Mix)")[0]
    assert candidates.item_id(one) == candidates.item_id(two)
    assert candidates.item_id(one) != candidates.item_id(other)
    drop = match.read_text_lines("Aurora Bloom - \U0001f4a7")[0]
    wave = match.read_text_lines("Aurora Bloom - \U0001f30a")[0]
    assert candidates.item_id(drop) != candidates.item_id(wave)
    assert candidates.identity(other) == {
        "artist": "aurora bloom", "title": "sun path", "version": "extended mix"
    }


def test_a_store_that_cannot_be_read_is_not_read_as_nobody_was_asked(cfg, monkeypatch):
    wanted = match.read_text_lines("Aurora Bloom - Sun Path")[0]
    def broken(_store, _item_id):
        raise refuse("unavailable-transient", "the queue could not be read", origin=("review",))
    monkeypatch.setattr(review, "get", broken)
    with review.open_store(cfg) as items, pytest.raises(CratekitError) as caught:
        candidates.settled(items, wanted)
    assert caught.value.cause.reason == "unavailable-transient"


@pytest.mark.parametrize(
    ("line", "title", "exact"),
    [("Aurora Bloom - \U0001f4a7", "\U0001f525", False), ("Aurora Bloom - ❤", "❤️", True)],
    ids=["another-emoji", "the-same-emoji"],
)
def test_a_search_answered_by_another_emoji_title_is_not_exact(line, title, exact):
    """Two emoji titles by one artist fold to one recording token, so the exact flag compares the
    recording's identity: ``🔥`` answering ``💧`` is never listed without a person."""
    _wanted, answer = answer_of(line, Hit("7001", "Aurora Bloom", title))
    assert [one.exact for one in answer.candidates] == [exact]
    assert (candidates.sole_exact(answer) is not None) is exact


def test_two_emoji_rows_are_each_searched_and_listed(cfg, library, tmp_path, monkeypatch):
    """Two emoji titles by one artist share a match id, and each is still searched and listed."""
    drop, wave = "\U0001f4a7", "\U0001f30a"
    path = tracklist(tmp_path, f"Aurora Bloom - {drop}", f"Aurora Bloom - {wave}")
    fake = bind(
        monkeypatch,
        FakeCatalogue(
            searches={
                ("Aurora Bloom", drop): [Hit("7001", "Aurora Bloom", drop)],
                ("Aurora Bloom", wave): [Hit("7002", "Aurora Bloom", wave)],
            }
        ),
    )
    envelope = ok(path)[0]
    assert sorted(fake.searched_for) == sorted([("Aurora Bloom", drop), ("Aurora Bloom", wave)])
    body = json.loads(Path(envelope["data"]["summary"]["list"]).read_text())
    assert sorted(t["id"] for t in body["tracks"]) == ["7001", "7002"]


