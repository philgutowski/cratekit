"""U78: a set's missing tracks are named by exact ISRC, and the rest handed on.

``crate intake set`` identifies a recording and resolves every track, and a
recognised track carries no provider identifier, so before U78 ``intake missing``
had nothing it could list for a set (R-401). It now asks the catalogue for each
such row's ISRC. Exactly one distinct identifier lists the row. Anything else,
no ISRC, a malformed one, none filed or several filed (R-356), writes the row to
``<name>.unlisted.json``, a text list ``match run`` reads, with the reason above
it. A provider that cannot answer refuses before any file is written.

THE SET JOBS HERE ARE REAL. Recognition runs through the carver and transport
fakes ``tests/intake/test_workers.py`` uses, the job is queued and driven through
the dispatcher, and the reports this verb reads are the ones the worker wrote.
Only the catalogue is a fake, and it is substituted where the verb looks it up.

D1 applies. Nothing here names a real volume, a real person, or a real track,
and every ISRC is in a registrant range nobody holds.
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
from tests.intake.test_recognition import FakeCarver, hit
from tests.intake.test_workers import recognised  # noqa: F401 - a fixture
from tests.label_fakes import FakeCatalogue, FakeTrack, UnreadableCatalogue, catalogue_factory
from tests.test_config import valid_data

ONE = "QZAAA2600001"
TWO = "QZAAA2600002"
NONE_FILED = "QZAAA2600003"

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


# ═══════════════════════════════════════════════════════════════════════════
# One id is listed, anything else is handed on
# ═══════════════════════════════════════════════════════════════════════════


def test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on(
    cfg, library, recognised, monkeypatch  # noqa: F811 - the imported fixture
):
    job_id = finished_set(library, recognised, monkeypatch, *three())
    fake = bind(
        monkeypatch,
        FakeCatalogue(isrcs={ONE: [FakeTrack("9001")], TWO: [FakeTrack("9002"), FakeTrack("9003")]}),
    )

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


def test_the_unlisted_file_round_trips_through_read_list_with_its_reasons(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    job_id = finished_set(library, recognised, monkeypatch, *three())
    bind(
        monkeypatch,
        FakeCatalogue(isrcs={ONE: [FakeTrack("9001")], TWO: [FakeTrack("9002"), FakeTrack("9003")]}),
    )

    _code, envelope = missing(job_id)

    handed = lists_dir(library) / f"intake-{job_id}.unlisted.json"
    assert envelope["data"]["summary"]["unlisted_list"] == str(handed)
    read = match_cli.read_list(handed)
    assert [(one.artist, one.title) for one in read] == [
        ("Nova Reef", "Tide"),
        ("Mira Vale", "Glass Hour"),
    ]
    raw = json.loads(handed.read_text())
    assert (raw["list"], raw["origin"]) == (1, "text")
    assert raw["tracks"][1] == "Nova Reef - Tide"
    assert raw["tracks"][0].startswith("# the provider files 2 tracks under ISRC " + TWO)
    assert raw["tracks"][2].startswith("# it carries no ISRC")
    check = {c["key"]: c for c in envelope["data"]["checks"]}["intake.missing.unlisted"]
    assert check["status"] == "fail"
    assert f"crate match run {handed}" in check["detail"]


def test_an_isrc_the_provider_files_nothing_under_is_handed_on_as_unknown(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    job_id = finished_set(library, recognised, monkeypatch, hit("Lumen Drift", "Salt Road", isrc=NONE_FILED))
    fake = bind(monkeypatch, FakeCatalogue())

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert fake.isrcs_asked_for == [NONE_FILED]
    assert (summary["list"], summary["written"]) == (None, 0)
    assert [t["why"] for t in summary["unlisted_tracks"]] == [missing_cli.UNKNOWN]
    assert summary["unlisted_next"] == f"crate match run {summary['unlisted_list']}"


def test_an_isrc_is_folded_before_it_is_asked_and_a_malformed_one_is_never_asked(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
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


def test_the_same_id_twice_in_one_answer_is_one_id_and_is_listed(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    job_id = finished_set(library, recognised, monkeypatch, hit("Aurora Bloom", "Sun Path", isrc=ONE))
    bind(monkeypatch, FakeCatalogue(isrcs={ONE: [FakeTrack("9001"), FakeTrack("9001")]}))

    _code, envelope = missing(job_id)

    assert envelope["data"]["summary"]["written"] == 1


def test_an_answer_holding_a_track_with_no_identifier_is_handed_on_not_read_as_one(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    job_id = finished_set(library, recognised, monkeypatch, hit("Aurora Bloom", "Sun Path", isrc=ONE))
    bind(monkeypatch, FakeCatalogue(isrcs={ONE: [FakeTrack("9001"), FakeTrack("")]}))

    _code, envelope = missing(job_id)

    summary = envelope["data"]["summary"]
    assert summary["written"] == 0
    assert [t["why"] for t in summary["unlisted_tracks"]] == [missing_cli.UNREADABLE]


# ═══════════════════════════════════════════════════════════════════════════
# Nothing is written unless every answer is in hand
# ═══════════════════════════════════════════════════════════════════════════


def test_a_provider_outage_refuses_and_writes_nothing(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    job_id = finished_set(library, recognised, monkeypatch, *three())
    fake = bind(monkeypatch, UnreadableCatalogue())

    code, envelope = missing(job_id)

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "unavailable-transient"
    assert ONE in envelope["cause"]["message"]
    assert "nothing was written" in envelope["cause"]["message"]
    assert fake.isrcs_asked_for == [ONE]
    assert not lists_dir(library).exists() or list(lists_dir(library).iterdir()) == []


def test_no_stored_session_refuses_before_anything_is_written(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    """The real ``resolve``, over an isolated keychain holding no provider session."""
    job_id = finished_set(library, recognised, monkeypatch, *three())

    code, envelope = missing(job_id)

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "credential-missing"
    assert not lists_dir(library).exists() or list(lists_dir(library).iterdir()) == []


def test_a_set_with_no_isrc_resolves_no_catalogue_and_spends_no_login(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    job_id = finished_set(
        library, recognised, monkeypatch, hit("Aurora Bloom", "Sun Path"), hit("Nova Reef", "Tide")
    )

    def never(cfg):
        raise AssertionError("the catalogue was resolved with nothing to ask it")

    monkeypatch.setattr(catalogue, "resolve", never)

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["unlisted"] == 2


def test_a_different_file_at_the_unlisted_path_refuses_before_the_list_is_written(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    job_id = finished_set(library, recognised, monkeypatch, *three())
    bind(
        monkeypatch,
        FakeCatalogue(isrcs={ONE: [FakeTrack("9001")], TWO: [FakeTrack("9002"), FakeTrack("9003")]}),
    )
    handed = lists_dir(library) / f"intake-{job_id}.unlisted.json"
    handed.parent.mkdir(parents=True)
    handed.write_text("somebody else's list\n")

    code, envelope = missing(job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert handed.read_text() == "somebody else's list\n"
    assert sorted(p.name for p in handed.parent.iterdir()) == [handed.name]


def test_a_second_run_over_the_same_answers_is_not_refused(
    cfg, library, recognised, monkeypatch  # noqa: F811
):
    job_id = finished_set(library, recognised, monkeypatch, *three())
    bind(
        monkeypatch,
        FakeCatalogue(isrcs={ONE: [FakeTrack("9001")], TWO: [FakeTrack("9002"), FakeTrack("9003")]}),
    )
    first = missing(job_id)

    again = missing(job_id)

    assert again[0] == int(ExitCode.OK), again[1]
    assert again[1]["data"]["summary"] == first[1]["data"]["summary"]
