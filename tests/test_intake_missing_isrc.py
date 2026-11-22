"""U78: a set's missing tracks are named by exact ISRC, and the rest handed on.

The set jobs are real, recognised through the fakes ``tests/intake/test_workers.py``
uses; only the catalogue is a fake. D1 applies, and every ISRC is in a registrant
range nobody holds.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.acquire import match_cli
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import acrcloud, missing_cli
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from tests.cli_drive import drive
from tests.intake import test_workers
from tests.intake.test_recognition import FakeCarver, hit
from tests.label_fakes import FakeCatalogue, FakeTrack, UnreadableCatalogue, catalogue_factory
from tests.test_config import valid_data

ONE = "QZAAA2600001"
TWO = "QZAAA2600002"
NONE_FILED = "QZAAA2600003"

# Fixtures

recognised = test_workers.recognised  # the shared fixture, under its own name


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


def lists_dir(library: Path) -> Path:
    return library.parent / "staging" / missing_cli.LISTS_DIR


def finished_set(library: Path, transport, monkeypatch, *answers: dict) -> str:
    """A set of ``len(answers)`` chunks, identified, queued and driven to the end."""
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: FakeCarver(30.0 * len(answers) - 5))
    transport.answers[:] = list(answers)
    path = library / "set.mp3"
    path.write_bytes(b"ID3")
    code, envelope = drive(["intake", "set", str(path)])
    assert code == int(ExitCode.OK), envelope
    job_id = envelope["data"]["job_id"]
    with jobs.open_store() as store:
        argv = cli_jobs.argv_for(jobs.get(store, job_id))
    code, envelope = drive(argv)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    return job_id


def bind(monkeypatch, fake: FakeCatalogue) -> FakeCatalogue:
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def missing(job_id: str) -> tuple[int, dict]:
    return drive(["intake", "missing", "--job", job_id])


def three() -> tuple[dict, ...]:
    return (
        hit("Aurora Bloom", "Sun Path", isrc=ONE),
        hit("Nova Reef", "Tide", isrc=TWO),
        hit("Mira Vale", "Glass Hour"),
    )


# One id is listed, anything else is handed on


def test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on(
    cfg, library, recognised, monkeypatch
):
    """One set read every way: nothing written until every answer is in hand, then the one id
    listed, the rest handed on to a text list that reads back, and a second run the same."""
    from cratekit.core.cause import refuse
    from cratekit.core.exit_codes import Remedy
    class Expired(FakeCatalogue):
        def tracks_for_isrc(self, isrc):
            raise refuse(
                "credential-missing",
                "the stored session expired mid lookup",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
                origin=("test",),
            )
    job_id = finished_set(library, recognised, monkeypatch, *three())
    # NO STORED SESSION: the real ``resolve``, over an isolated keychain holding none.
    code, envelope = missing(job_id)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "credential-missing"
    # A PROVIDER OUTAGE refuses whole.
    fake = bind(monkeypatch, UnreadableCatalogue())
    code, envelope = missing(job_id)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "unavailable-transient"
    assert ONE in envelope["cause"]["message"]
    assert "nothing was written" in envelope["cause"]["message"]
    assert fake.isrcs_asked_for == [ONE]
    # A PRODUCT REFUSAL from the catalogue passes through unrelabelled.
    bind(monkeypatch, Expired())
    code, envelope = missing(job_id)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "credential-missing"
    assert not lists_dir(library).exists() or list(lists_dir(library).iterdir()) == []
    answers = {ONE: [FakeTrack("9001")], TWO: [FakeTrack("9002"), FakeTrack("9003")]}
    # A DIFFERENT FILE AT THE UNLISTED PATH refuses before the list is written.
    handed = lists_dir(library) / f"intake-{job_id}.unlisted.json"
    handed.parent.mkdir(parents=True, exist_ok=True)
    handed.write_text("somebody else's list\n")
    bind(monkeypatch, FakeCatalogue(isrcs=answers))
    code, envelope = missing(job_id)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert handed.read_text() == "somebody else's list\n"
    assert sorted(p.name for p in handed.parent.iterdir()) == [handed.name]
    handed.unlink()
    fake = bind(monkeypatch, FakeCatalogue(isrcs=answers))
    code, envelope = missing(job_id)
    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["by_isrc"], summary["unlisted"]) == (1, 1, 2)
    assert fake.isrcs_asked_for == [ONE, TWO], "a row with no ISRC was asked about"
    body = json.loads(Path(summary["list"]).read_text())
    assert [(t["id"], t["artist"], t["title"]) for t in body["tracks"]] == [
        ("9001", "Aurora Bloom", "Sun Path")
    ]
    manifest = json.loads(Path(summary["manifest"]).read_text())
    assert manifest["rows"]["9001"]["source"] == "set"
    assert [(t["artist"], t["title"], t["why"]) for t in summary["unlisted_tracks"]] == [
        ("Nova Reef", "Tide", missing_cli.SEVERAL),
        ("Mira Vale", "Glass Hour", missing_cli.NO_ISRC),
    ]
    assert "9002, 9003" in summary["unlisted_tracks"][0]["reason"]
    assert summary["unlisted_tracks"][0]["isrc"] == TWO
    # THE UNLISTED FILE round trips through read_list with its reasons.
    assert summary["unlisted_list"] == str(handed)
    read = match_cli.read_list(handed)
    assert [(one.artist, one.title) for one in read] == [
        ("Nova Reef", "Tide"), ("Mira Vale", "Glass Hour"),
    ]
    raw = json.loads(handed.read_text())
    assert (raw["list"], raw["origin"]) == (1, "text")
    assert raw["tracks"][1] == "Nova Reef - Tide"
    assert raw["tracks"][0].startswith("# the provider files 2 tracks under ISRC " + TWO)
    assert raw["tracks"][2].startswith("# it carries no ISRC")
    check = {c["key"]: c for c in envelope["data"]["checks"]}["intake.missing.unlisted"]
    assert check["status"] == "fail"
    assert f"crate intake missing --list {handed}" in check["detail"]
    # A SECOND RUN over the same answers is not refused.
    again = missing(job_id)
    assert again[0] == int(ExitCode.OK), again[1]
    assert again[1]["data"]["summary"] == summary
    # U206: the SHIPPED catalogue keeps an ISRC answer, so a later run asks nothing.
    from cratekit.cli import ISRC_LOOKUPS
    from cratekit.label import tidal_catalogue
    client = _CountingClient(
        {ONE: [_ProviderTrack("9001")], TWO: [_ProviderTrack("9002"), _ProviderTrack("9003")]}
    )
    monkeypatch.setattr(catalogue, "resolve", lambda cfg: tidal_catalogue.TidalCatalogue(client))
    first = missing(job_id)
    assert first[0] == int(ExitCode.OK), first[1]
    assert sorted(client.asked) == [ONE, TWO]
    again = missing(job_id)
    assert again[0] == int(ExitCode.OK), again[1]
    assert sorted(client.asked) == [ONE, TWO], "the second run asked the provider again"
    assert again[1]["data"]["summary"] == first[1]["data"]["summary"]
    said = [w["message"] for w in again[1]["warnings"] if w["code"] == ISRC_LOOKUPS]
    assert said == ["2 ISRC lookups answered from the cache, 0 asked of the streaming provider"]


def test_an_isrc_the_provider_files_nothing_under_is_handed_on_as_unknown(cfg, library, recognised, monkeypatch):
    job_id = finished_set(library, recognised, monkeypatch, hit("Lumen Drift", "Salt Road", isrc=NONE_FILED))
    fake = bind(monkeypatch, FakeCatalogue())
    code, envelope = missing(job_id)
    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert fake.isrcs_asked_for == [NONE_FILED]
    assert (summary["list"], summary["written"]) == (None, 0)
    assert [t["why"] for t in summary["unlisted_tracks"]] == [missing_cli.UNKNOWN]
    assert summary["unlisted_next"] == f"crate intake missing --list {summary['unlisted_list']}"


def test_an_isrc_is_folded_before_it_is_asked_and_a_malformed_one_is_never_asked(cfg, library, recognised, monkeypatch):
    job_id = finished_set(
        library,
        recognised,
        monkeypatch,
        hit("Aurora Bloom", "Sun Path", isrc="qz-aaa-26-00001"),
        hit("Nova Reef", "Tide", isrc="CAT-0042"),
    )
    fake = bind(monkeypatch, FakeCatalogue(isrcs={ONE: [FakeTrack("9001")]}))
    _code, envelope = missing(job_id)
    summary = envelope["data"]["summary"]
    assert fake.isrcs_asked_for == [ONE]
    assert summary["written"] == 1
    assert [t["why"] for t in summary["unlisted_tracks"]] == [missing_cli.MALFORMED]


def test_the_same_id_twice_in_one_answer_is_one_id_and_is_listed(cfg, library, recognised, monkeypatch):
    job_id = finished_set(library, recognised, monkeypatch, hit("Aurora Bloom", "Sun Path", isrc=ONE))
    bind(monkeypatch, FakeCatalogue(isrcs={ONE: [FakeTrack("9001"), FakeTrack("9001")]}))
    _code, envelope = missing(job_id)
    assert envelope["data"]["summary"]["written"] == 1
    # AN ANSWER HOLDING A TRACK WITH NO IDENTIFIER is handed on, not read as one.
    bind(monkeypatch, FakeCatalogue(isrcs={ONE: [FakeTrack("9001"), FakeTrack("")]}))
    _code, envelope = missing(job_id)
    summary = envelope["data"]["summary"]
    assert summary["written"] == 0
    assert [t["why"] for t in summary["unlisted_tracks"]] == [missing_cli.UNREADABLE]


# Nothing is written unless every answer is in hand


def test_a_set_with_no_isrc_resolves_no_catalogue_and_spends_no_login(cfg, library, recognised, monkeypatch):
    job_id = finished_set(
        library, recognised, monkeypatch, hit("Aurora Bloom", "Sun Path"), hit("Nova Reef", "Tide")
    )
    def never(cfg):
        raise AssertionError("the catalogue was resolved with nothing to ask it")
    monkeypatch.setattr(catalogue, "resolve", never)
    code, envelope = missing(job_id)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["unlisted"] == 2


def test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written(cfg, library, recognised, monkeypatch):
    """One row no text line can hold is named on its own check; the rest are still written."""
    job_id = finished_set(
        library,
        recognised,
        monkeypatch,
        hit("Aurora Bloom", "Sun Path", isrc=ONE),
        hit("Kite - Harbor", "Low Tide Signal"),
        hit("Mira Vale", "Glass Hour"),
    )
    bind(monkeypatch, FakeCatalogue(isrcs={ONE: [FakeTrack("9001")]}))
    code, envelope = missing(job_id)
    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert summary["written"] == 1
    assert [(t["artist"], t["why"]) for t in summary["unlisted_tracks"]] == [
        ("Kite - Harbor", missing_cli.NO_ISRC), ("Mira Vale", missing_cli.NO_ISRC),
    ]
    assert [t["in_file"] for t in summary["unlisted_tracks"]] == [False, True]
    read = match_cli.read_list(Path(summary["unlisted_list"]))
    assert [(one.artist, one.title) for one in read] == [("Mira Vale", "Glass Hour")]
    check = {c["key"]: c for c in envelope["data"]["checks"]}["intake.missing.unwritable"]
    assert check["status"] == "fail"
    assert "Kite - Harbor - Low Tide Signal" in check["detail"]


def test_the_order_the_provider_answers_in_does_not_change_the_files(cfg, library, recognised, monkeypatch):
    """Sorted ids, so a reshuffled answer never turns a repeat run into a refusal."""
    job_id = finished_set(library, recognised, monkeypatch, hit("Nova Reef", "Tide", isrc=TWO))
    bind(monkeypatch, FakeCatalogue(isrcs={TWO: [FakeTrack("9003"), FakeTrack("9002")]}))
    first = missing(job_id)
    bind(monkeypatch, FakeCatalogue(isrcs={TWO: [FakeTrack("9002"), FakeTrack("9003")]}))
    again = missing(job_id)
    assert again[0] == int(ExitCode.OK), again[1]
    assert "(9002, 9003)" in first[1]["data"]["summary"]["unlisted_tracks"][0]["reason"]


def test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op(cfg, library, recognised, monkeypatch):
    """Nothing listed or handed on is not a no-op, which would read as a set already held."""
    job_id = finished_set(library, recognised, monkeypatch, hit("Kite - Harbor", "Low Tide Signal"))
    code, envelope = missing(job_id)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert envelope["cause"]["detail"]["unlisted_tracks"][0]["artist"] == "Kite - Harbor"
    assert not lists_dir(library).exists()


# U206: the shipped catalogue keeps an ISRC answer, so a second run asks nothing


class _ProviderTrack:
    """A provider track the matcher can read: an identifier, an artist, a title."""

    def __init__(self, track_id: str) -> None:
        self.id = track_id
        self.name = f"Track {track_id}"
        self.artist = "Aurora Bloom"


class _CountingClient:
    """A provider client the SHIPPED catalogue adapter asks, counting every ISRC."""

    country_code = "GB"

    def __init__(self, answers: dict[str, list[_ProviderTrack]]) -> None:
        self.answers = answers
        self.asked: list[str] = []

    def get_tracks_by_isrc(self, code: str) -> list[_ProviderTrack]:
        from tidalapi.exceptions import ObjectNotFound
        self.asked.append(code)
        if code not in self.answers:
            raise ObjectNotFound()
        return list(self.answers[code])


