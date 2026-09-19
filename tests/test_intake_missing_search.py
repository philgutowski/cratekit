"""U79: a row nothing names exactly gets provider candidates, and never a pick.

``crate intake missing --list PATH`` reads a text list, the unlisted list of an
earlier run or any tracklist, resolves every row against the library, and asks
the catalogue's text search about each row that is still missing. Exactly one
candidate matching under the product's own fold is listed. Anything else is
offered into the review queue with its candidates and its scores, and the next
run lists what a person accepted. No candidate is reported, never silent.

EVERYTHING BUT THE CATALOGUE IS REAL. The list is read by ``match_cli.read_list``,
the library is a folder of files the real index walks, the review store is the
real store, and an answer is recorded through ``crate review resolve`` on the
real dispatcher. Only the provider is a fake, substituted where the verb looks
it up.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

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
from tests.test_config import valid_data

SUN = ("Aurora Bloom", "Sun Path")
TIDE = ("Nova Reef", "Tide")
GLASS = ("Mira Vale", "Glass Hour")

# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library) -> config.Config:
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


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


def tracklist(tmp_path: Path, *lines: str, name: str = "typed.txt") -> Path:
    path = tmp_path / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def found(path: Path, *extra: str) -> tuple[int, dict]:
    return drive(["intake", "missing", "--list", str(path), *extra])


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


# ═══════════════════════════════════════════════════════════════════════════
# One exact candidate is listed without review
# ═══════════════════════════════════════════════════════════════════════════


def test_one_exact_candidate_is_listed_without_review(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    fake = bind(
        monkeypatch,
        FakeCatalogue(
            searches={
                SUN: [
                    Hit("7001", "Aurora Bloom", "Sun Path"),
                    Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix"),
                    Hit("7003", "Someone Else", "Sun Path"),
                ]
            }
        ),
    )

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
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
    fake = bind(monkeypatch, FakeCatalogue(searches={asked: [Hit("7001", "Aurora Bloom", "Sun Path")]}))

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert fake.searched_for == [asked], "the null version went into the query"
    assert envelope["data"]["summary"]["by_search"] == 1


def test_a_version_the_row_names_goes_into_the_query_and_into_the_exact_test(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)")
    fake = bind(
        monkeypatch,
        FakeCatalogue(
            searches={
                ("Aurora Bloom", "Sun Path Extended Mix"): [
                    Hit("7001", "Aurora Bloom", "Sun Path"),
                    Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix"),
                ]
            }
        ),
    )

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert fake.searched_for == [("Aurora Bloom", "Sun Path Extended Mix")]
    body = json.loads(Path(envelope["data"]["summary"]["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["7002"], "the plain cut was listed for a remix"


def test_the_same_exact_track_served_twice_is_one_candidate(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    bind(
        monkeypatch,
        FakeCatalogue(
            searches={SUN: [Hit("7001", "Aurora Bloom", "Sun Path"), Hit("7001", "Aurora Bloom", "Sun Path")]}
        ),
    )

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["by_search"] == 1


# ═══════════════════════════════════════════════════════════════════════════
# Two exact candidates are offered, not picked
# ═══════════════════════════════════════════════════════════════════════════


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

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["list"], summary["written"], summary["candidates_offered"]) == (None, 0, 1)
    assert not list(lists_dir(library).glob("*")), "a list was written over an open question"
    item = the_item(cfg)
    assert item.verdict is None
    assert item.handler_key == "intake.missing"
    assert [o.option_id for o in item.options] == ["7001", "7009"]
    assert [o.detail["exact"] for o in item.options] == [True, True]
    assert "Harbour Lights" in item.options[1].summary
    assert "2 tracks that match it exactly" in item.payload["why"]
    row = summary["rows"][0]
    assert (row["state"], row["item_id"], row["candidates"]) == (
        candidates.OFFERED,
        item.item_id,
        2,
    )
    check = checks(envelope)["candidates"]
    assert check["status"] == "fail"
    assert item.item_id in check["detail"]
    assert f"--queue {candidates.QUEUE} --kind {candidates.KIND}" in check["detail"]


def test_an_exact_candidate_beside_a_row_that_cannot_be_read_is_offered(
    cfg, library, tmp_path, monkeypatch
):
    """The unreadable row could be the second exact candidate, so nothing is picked."""
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    nameless = Hit("7004", "", "Sun Path")
    bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", "Aurora Bloom", "Sun Path"), nameless]}))

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["written"] == 0
    item = the_item(cfg)
    assert [o.option_id for o in item.options] == ["7001"]
    assert item.payload["unreadable"] == 1
    assert "could not be read" in item.payload["why"]


def test_an_exact_candidate_beside_an_exact_one_with_no_identifier_is_offered(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    bind(
        monkeypatch,
        FakeCatalogue(
            searches={SUN: [Hit("7001", "Aurora Bloom", "Sun Path"), Hit("", "Aurora Bloom", "Sun Path")]}
        ),
    )

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
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
    bind(
        monkeypatch,
        FakeCatalogue(
            searches={
                (wanted.artist, candidates.query_title(wanted)): [
                    Hit("7001", "Aurora Bloom", "Sun Path", version="Dub"),
                    Hit("7002", "Aurora Bloom", "Sun Path Dub"),
                ]
            }
        ),
    )

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["written"] == 0
    assert sorted(o.option_id for o in the_item(cfg).options) == ["7001", "7002"]


# ═══════════════════════════════════════════════════════════════════════════
# A near miss is offered with its score and never listed until accepted
# ═══════════════════════════════════════════════════════════════════════════


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
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    bind(monkeypatch, near_miss())

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["by_search"], summary["candidates_offered"]) == (0, 0, 1)
    item = the_item(cfg)
    # A PERFECT SCORE IS STILL NOT A PICK. The extended mix is the same
    # recording, so it scores 100 on the recording, and it is another version.
    shown = {o.option_id: o.detail for o in item.options}
    assert shown["7002"]["score"] == 100.0 and shown["7002"]["exact"] is False
    assert candidates.CANDIDATE_FLOOR <= shown["7005"]["score"] < 100.0
    assert "7006" not in shown, "a hit resembling nothing was put on the screen"
    assert [o.option_id for o in item.options] == ["7002", "7005"], "best score first"
    assert "score 100" in item.options[0].summary
    assert "never picked from a score" in item.payload["why"]


def test_a_second_run_offers_nothing_new_and_spends_no_search(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    fake = bind(monkeypatch, near_miss())
    found(path)
    first = the_item(cfg)

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert fake.searched_for == [SUN], "an open question was searched for again"
    again = the_item(cfg)
    assert (again.item_id, again.updated) == (first.item_id, first.updated)
    assert envelope["data"]["summary"]["rows"][0]["state"] == candidates.WAITING


def test_the_same_row_in_two_lists_is_one_question(cfg, library, tmp_path, monkeypatch):
    bind(monkeypatch, near_miss())
    found(tracklist(tmp_path, "Aurora Bloom - Sun Path", name="one.txt"))

    found(tracklist(tmp_path, "1. aurora bloom - SUN PATH", name="two.txt"))

    the_item(cfg)


# ═══════════════════════════════════════════════════════════════════════════
# An accepted candidate is listed by the next run
# ═══════════════════════════════════════════════════════════════════════════


def test_an_accepted_candidate_is_listed_by_the_next_run(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    fake = bind(monkeypatch, near_miss())
    found(path)
    resolve(the_item(cfg).item_id, "accepted", "--option", "7005")

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert fake.searched_for == [SUN], "an answered row was searched for again"
    assert (summary["written"], summary["by_review"], summary["by_search"]) == (1, 1, 0)
    body = json.loads(Path(summary["list"]).read_text())
    # THE ROW IS THE CANDIDATE'S, since that is the track the download fetches.
    assert [(t["id"], t["artist"], t["title"]) for t in body["tracks"]] == [
        ("7005", "Aurora Bloome", "Sun Path")
    ]
    assert checks(envelope)["candidates"]["status"] == "ok"


def test_an_acceptance_of_the_only_candidate_needs_no_option(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    bind(
        monkeypatch,
        FakeCatalogue(searches={SUN: [Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix")]}),
    )
    found(path)
    resolve(the_item(cfg).item_id, "accepted")

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    body = json.loads(Path(envelope["data"]["summary"]["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["7002"]


def test_an_acceptance_naming_none_of_several_candidates_lists_nothing(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    bind(monkeypatch, two_exact())
    found(path)
    item_id = the_item(cfg).item_id
    resolve(item_id, "accepted")

    code, envelope = found(path)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "without naming which of its 2 candidates" in envelope["cause"]["message"]
    assert "crate review clear" in " ".join(envelope["cause"]["remediation"]["steps"])
    assert not list(lists_dir(library).glob("*"))


def test_an_accepted_candidate_the_library_now_holds_is_not_listed_again(
    cfg, library, tmp_path, monkeypatch
):
    """The row stays missing for ever when the candidate is another spelling.

    Another VERSION held, and a spelling close enough to score over the
    library's own floor, are questions the library raises itself, so the row
    stops being missing. A spelling further off than that is another recording
    to the fold and no question to the library, and nothing but this guard
    stands between it and a download on every later run.
    """
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    bind(
        monkeypatch,
        FakeCatalogue(
            searches={
                SUN: [Hit("7005", "Aurora Bloom and the Reef Players", "Sun Path")],
                TIDE: [Hit("7010", "Nova Reef", "Tide")],
            }
        ),
    )
    found(path)
    resolve(the_item(cfg).item_id, "accepted", "--option", "7005")
    owned(library, "Aurora Bloom and the Reef Players - Sun Path.flac")
    intake_cli.reset_cache()

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["7010"], "a held track was listed for download"
    assert (summary["by_review"], summary["in_library"]) == (0, 1)
    assert [r["state"] for r in summary["rows"]] == [candidates.HELD, candidates.LISTED]
    assert "already in the library" in checks(envelope)["accepted"]["detail"]


def test_a_rejected_row_is_reported_and_never_searched_again(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    fake = bind(
        monkeypatch,
        FakeCatalogue(
            searches={
                SUN: [Hit("7002", "Aurora Bloom", "Sun Path", version="Extended Mix")],
                TIDE: [Hit("7010", "Nova Reef", "Tide")],
            }
        ),
    )
    found(path)
    resolve(the_item(cfg).item_id, "rejected")
    fake.searched_for.clear()

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert fake.searched_for == [TIDE]
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["unfound"]) == (1, 1)
    check = checks(envelope)["unfound"]
    assert check["status"] == "fail"
    assert "rejected in review" in check["detail"]


# ═══════════════════════════════════════════════════════════════════════════
# No candidates is reported, not silent
# ═══════════════════════════════════════════════════════════════════════════


def test_no_candidate_beside_a_listed_row_is_a_failing_check(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Mira Vale - Glass Hour")
    bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", "Aurora Bloom", "Sun Path")]}))

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
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
    bind(
        monkeypatch,
        FakeCatalogue(searches={GLASS: [Hit("7006", "Quite Another Act", "Wholly Different")]}),
    )

    code, envelope = found(path)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "1 hit(s) and none resembles it" in envelope["cause"]["message"]
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


# ═══════════════════════════════════════════════════════════════════════════
# The library is asked first
# ═══════════════════════════════════════════════════════════════════════════


def test_an_owned_row_is_never_searched_for(cfg, library, tmp_path, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    fake = bind(
        monkeypatch,
        FakeCatalogue(searches={SUN: [Hit("7001", *SUN)], TIDE: [Hit("7010", *TIDE)]}),
    )

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
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

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
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

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert fake.searched_for == [SUN]
    assert envelope["data"]["summary"]["written"] == 1


# ═══════════════════════════════════════════════════════════════════════════
# The unlisted list of an earlier run is the input, and the names do not collide
# ═══════════════════════════════════════════════════════════════════════════


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

    code, envelope = found(written.unlisted_path)

    assert code == int(ExitCode.OK), envelope
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


def test_skip_failed_means_nothing_for_a_list_and_is_refused(cfg, library, tmp_path):
    code, envelope = found(tracklist(tmp_path, "Aurora Bloom - Sun Path"), "--skip-failed")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"


def test_the_verb_declares_that_it_adjudicates():
    assert registry.entry("intake.missing").adjudicates


# ═══════════════════════════════════════════════════════════════════════════
# What the unit's review drove
# ═══════════════════════════════════════════════════════════════════════════


def test_the_run_after_an_answer_lists_more_than_the_first_and_is_not_refused(
    cfg, library, tmp_path, monkeypatch
):
    """The documented second run. Under one fixed name it was refused, because
    the first run had already written a list and this one holds other bytes."""
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
    code, first = found(path)
    assert code == int(ExitCode.OK), first
    resolve(the_item(cfg).item_id, "accepted", "--option", "7002")

    code, second = found(path)

    assert code == int(ExitCode.OK), second
    body = json.loads(Path(second["data"]["summary"]["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["7010", "7002"]
    assert second["data"]["summary"]["list"] != first["data"]["summary"]["list"]


def test_the_same_work_twice_rewrites_the_same_list(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, "Nova Reef - Tide")
    bind(monkeypatch, FakeCatalogue(searches={TIDE: [Hit("7010", *TIDE)]}))
    _code, first = found(path)

    code, second = found(path)

    assert code == int(ExitCode.OK), second
    assert second["data"]["summary"]["list"] == first["data"]["summary"]["list"]
    assert len(list(lists_dir(library).glob("*.list.json"))) == 1


def test_two_tracklists_of_one_file_name_in_two_folders_do_not_collide(
    cfg, library, tmp_path, monkeypatch
):
    (tmp_path / "friday").mkdir()
    (tmp_path / "saturday").mkdir()
    one = tracklist(tmp_path / "friday", "Nova Reef - Tide", name="tracklist.txt")
    two = tracklist(tmp_path / "saturday", "Aurora Bloom - Sun Path", name="tracklist.txt")
    bind(monkeypatch, FakeCatalogue(searches={TIDE: [Hit("7010", *TIDE)], SUN: [Hit("7001", *SUN)]}))
    found(one)

    code, envelope = found(two)

    assert code == int(ExitCode.OK), envelope
    assert len(list(lists_dir(library).glob("tracklist-found-*.list.json"))) == 2


def test_a_missing_row_of_another_services_list_is_searched_for_and_not_dropped(
    cfg, library, tmp_path, monkeypatch
):
    """Its ref is that service's id, which the emitter writes as none. Sorted by
    the ref alone it was in no file and on no check, at exit zero."""
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

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert fake.searched_for == [SUN]
    body = json.loads(Path(envelope["data"]["summary"]["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["7001"], "another service's id was listed"


def test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    filler = [
        Hit(str(8000 + n), "Quite Another Act", f"Wholly Different {n}")
        for n in range(catalogue.TRACK_SEARCH_PAGE - 1)
    ]
    bind(monkeypatch, FakeCatalogue(searches={SUN: [Hit("7001", *SUN), *filler]}))

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
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

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
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

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["written"] == 0
    item = the_item(cfg)
    assert [o.option_id for o in item.options] == [hit.id]
    assert item.options[0].detail["exact"] is True
    assert "reads two ways" in item.payload["why"]


def test_a_failed_search_says_which_offers_it_did_not_make(cfg, library, tmp_path, monkeypatch):
    """A version question the library raised is in the queue before the provider
    is asked, so the refusal may not say nothing was offered."""
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

    code, envelope = found(path)

    assert code == int(ExitCode.OK), envelope
    assert len(resolved) == 1, "one run restored the provider session twice"
    summary = envelope["data"]["summary"]
    assert (summary["by_isrc"], summary["by_search"], summary["written"]) == (1, 1, 2)
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["7010", "7001"]


# ═══════════════════════════════════════════════════════════════════════════
# The proposal, below the verb
# ═══════════════════════════════════════════════════════════════════════════


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


def test_the_identity_is_the_folded_row_and_not_its_spelling():
    one = match.read_text_lines("Aurora Bloom - Sun Path (Original Mix)")[0]
    two = match.read_text_lines("AURORA  BLOOM - sun path")[0]
    other = match.read_text_lines("Aurora Bloom - Sun Path (Extended Mix)")[0]

    assert candidates.item_id(one) == candidates.item_id(two)
    assert candidates.item_id(one) != candidates.item_id(other)


def test_a_store_that_cannot_be_read_is_not_read_as_nobody_was_asked(cfg, monkeypatch):
    wanted = match.read_text_lines("Aurora Bloom - Sun Path")[0]

    def broken(_store, _item_id):
        raise refuse("unavailable-transient", "the queue could not be read", origin=("review",))

    monkeypatch.setattr(review, "get", broken)

    with review.open_store(cfg) as items, pytest.raises(CratekitError) as caught:
        candidates.settled(items, wanted)
    assert caught.value.cause.reason == "unavailable-transient"
