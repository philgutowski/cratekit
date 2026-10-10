"""U57: the two queued intake verbs, driven through the real dispatcher.

``intake.set`` and ``intake.playlist`` queued a job with nothing to claim and
nothing ran it (R-203). This file is the proof that both are over: a set is
identified at the queue and queues one item per identified track, a playlist
is listed through the catalogue seam and queues one item per provider row,
and the shared worker resolves each frozen track against the frozen library
and commits a report that says owned, offered or missing and never acquired.

EVERY OUTSIDE TOUCH GOES THROUGH A FAKE. Recognition is driven through the
carver and transport seams in ``intake.acrcloud`` with credentials recorded in
the isolated keychain; the playlist is driven through the label fakes'
catalogue. What remains unproven without a live key is stated in the unit's
record.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cratekit.acquire import listing, match
from cratekit.cli import handlers
from cratekit.cli import jobs as cli_jobs
from cratekit.core import artifacts, config, jobs, review, secrets
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import acrcloud, recognize
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from tests._containers import tagged_container
from tests.cli_drive import drive, drive_human
from tests.intake.test_recognition import FakeCarver, FakeTransport, hit, miss
from tests.label_fakes import (
    PROTOCOL_METHODS,
    FakeCatalogue,
    FakePagedPlaylist,
    StrictCatalogue,
    UnreadableCatalogue,
    catalogue_factory,
)
from tests.test_config import valid_data

SET_KEY = "intake.set"
PLAYLIST_KEY = "intake.playlist"

# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


def _configure(library: Path) -> config.Config:
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library) -> config.Config:
    """A configured machine. This is the configuration a job freezes."""
    return _configure(library)


@pytest.fixture
def recognised(monkeypatch, tmp_path):
    """Recognition READY and driven through fakes: keys in the isolated
    keychain, both binaries found, the carver and transport substituted on the
    module, and a ledger of this test's own. Returns the transport so a test
    can script it and read what was asked."""
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-1")
    secrets.set(str(secrets.Credential.IDENTIFY_SIGNING_KEY), "s-1")
    monkeypatch.setattr(recognize.binaries, "find", lambda name: f"/usr/bin/{name}")
    transport = FakeTransport()
    monkeypatch.setattr(acrcloud, "http_transport", transport)
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: FakeCarver(85.0))
    ledger = acrcloud.Ledger(path=tmp_path / "usage.json", lock_path=tmp_path / "usage.lock")
    monkeypatch.setattr(acrcloud, "Ledger", lambda: ledger)
    transport.ledger = ledger
    return transport


def recording(library: Path, name: str = "set.mp3") -> Path:
    path = library / name
    path.write_bytes(b"ID3")
    return path


def owned(library: Path, name: str) -> Path:
    """One file the library holds, named the way the index reads a name."""
    path = library / "Music" / name
    path.write_bytes(b"")
    return path


def three_tracks(transport: FakeTransport) -> None:
    """An 85 second recording is three chunks; script three different tracks."""
    transport.answers[:] = [
        hit("Aurora Bloom", "Sun Path", isrc="X1"),
        hit("Nova Reef", "Tide", isrc="X2"),
        hit("Mira Vale", "Glass Hour", isrc="X3"),
    ]


def queued_set(path: Path) -> tuple[str, dict]:
    code, envelope = drive(["intake", "set", str(path)])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"], envelope


def resume_argv(job_id: str) -> list[str]:
    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def items_of(job_id: str) -> tuple[jobs.Item, ...]:
    with jobs.open_store() as store:
        return jobs.items(store, job_id)


def states(job_id: str) -> dict[str, jobs.ItemState]:
    return {item.item_id: item.state for item in items_of(job_id)}


def job_of(job_id: str) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.get(store, job_id)


def reports(cfg: config.Config, job_id: str) -> tuple[dict, ...]:
    return artifacts.committed(intake_cli.ARTIFACTS, cfg, job_id)


def by_title(cfg: config.Config, job_id: str) -> dict[str, dict]:
    return {report["track"]["title"]: report for report in reports(cfg, job_id)}


class Track:
    """A provider playlist row in the shape the Tidal reader reads."""

    def __init__(self, track_id: str, artist: str, name: str, *, isrc: str = "") -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = isrc


def bind_playlist(monkeypatch, reference: str, tracks: list[Track]) -> FakeCatalogue:
    fake = FakeCatalogue(playlists={reference: FakePagedPlaylist(tracks)})
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


# ═══════════════════════════════════════════════════════════════════════════
# The binding
# ═══════════════════════════════════════════════════════════════════════════


def test_both_intake_keys_resolve_to_the_one_worker():
    assert handlers.resolve(SET_KEY) is intake_cli.handle
    assert handlers.resolve(PLAYLIST_KEY) is intake_cli.handle
    assert SET_KEY not in handlers.HANDLERS_NOT_YET_BOUND
    assert PLAYLIST_KEY not in handlers.HANDLERS_NOT_YET_BOUND


# ═══════════════════════════════════════════════════════════════════════════
# The set: identify at the queue
# ═══════════════════════════════════════════════════════════════════════════


def test_queueing_a_set_identifies_it_and_gives_the_driver_one_item_per_track(
    cfg, library, recognised
):
    three_tracks(recognised)
    path = recording(library)

    job_id, envelope = queued_set(path)

    assert envelope["data"]["state"] == "queued"
    assert envelope["data"]["progress"]["calls"] == 3
    assert len(recognised.requests) == 3
    items = items_of(job_id)
    assert len(items) == 3
    assert all(item.item_id.startswith("rc_") for item in items), "an item is a digest, not a name"
    job = job_of(job_id)
    assert job.payload[intake_cli.SOURCE] == str(path.absolute())
    assert job.payload[intake_cli.CALLS] == 3
    assert job.payload[intake_cli.UNREACHED] == 0
    assert [w["code"] for w in envelope["warnings"]] == [intake_cli.TRACKLIST_WRITTEN]
    frozen = job.payload[intake_cli.TRACKS]
    assert {said["title"] for said in frozen.values()} == {"Sun Path", "Tide", "Glass Hour"}
    assert all(said["ref"] == "" for said in frozen.values())
    assert list(frozen) == [item.item_id for item in items], "item order is the set order"


def test_a_set_nobody_recognised_is_an_honest_zero_that_says_what_it_cost(
    cfg, library, recognised
):
    recognised.answers[:] = [miss(), miss(), miss()]
    path = recording(library)

    code, envelope = drive(["intake", "set", str(path)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["state"] == "nothing-identified"
    assert envelope["data"]["job_id"] == ""
    assert envelope["data"]["progress"]["calls"] == 3
    assert envelope["data"]["progress"]["chunks"] == 3
    assert envelope["data"]["progress"]["source"] == str(path.absolute())
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == (), "a set with nothing identified must queue nothing"


def test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero(
    cfg, library, recognised
):
    """Absence read as evidence of absence, refused. Two chunks unanswered and
    one miss is not a set nobody recognised."""
    recognised.answers[:] = [ConnectionError("down"), miss(), ConnectionError("down")]
    code, envelope = drive(["intake", "set", str(recording(library))])
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "intake-recognition-failed"
    assert envelope["cause"]["detail"]["unreached"] == 2
    assert envelope["cause"]["detail"]["calls"] == 3
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap(
    cfg, library, recognised
):
    recognised.answers[:] = [hit("Aurora Bloom", "Sun Path", isrc="X1"), ConnectionError("down"), miss()]
    job_id, envelope = queued_set(recording(library))
    assert [w["code"] for w in envelope["warnings"]] == [
        intake_cli.TRACKLIST_WRITTEN,
        "recognition-incomplete",
    ]
    assert "1 of 3" in envelope["warnings"][1]["message"]
    assert envelope["data"]["progress"]["unreached"] == 1
    assert job_of(job_id).payload[intake_cli.UNREACHED] == 1
    code, resumed = drive(resume_argv(job_id))
    assert resumed["data"]["progress"]["unreached"] == 1, "the gap was forgotten on resume"
    assert resumed["data"]["progress"]["calls"] == 3


def test_identify_only_reports_the_same_coverage_rule(cfg, library, recognised):
    recognised.answers[:] = [hit("Aurora Bloom", "Sun Path"), ConnectionError("down"), miss()]
    code, envelope = drive(["intake", "identify", str(recording(library))])
    assert code == int(ExitCode.OK), envelope
    assert [w["code"] for w in envelope["warnings"]] == [
        intake_cli.TRACKLIST_WRITTEN,
        "recognition-incomplete",
    ]
    assert [row["title"] for row in envelope["data"]["missing"]] == ["Sun Path"]


# ═══════════════════════════════════════════════════════════════════════════
# U103: identification asks the library, writes its tracklist, and is paid once
# ═══════════════════════════════════════════════════════════════════════════


def tracklist_note(envelope: dict) -> dict:
    notes = [w for w in envelope["warnings"] if w["code"] == intake_cli.TRACKLIST_WRITTEN]
    assert len(notes) == 1, envelope["warnings"]
    return notes[0]


def test_identify_reports_an_owned_track_owned_an_offered_one_offered_and_the_rest_missing(
    cfg, library, recognised
):
    """R-422. The library is asked, under this verb's own key."""
    three_tracks(recognised)
    held = owned(library, "Aurora Bloom - Sun Path.flac")
    owned(library, "Nova Reef - Tide (Someone Remix).flac")

    code, envelope = drive(["intake", "identify", str(recording(library))])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == str(Outcome.PENDING)
    data = envelope["data"]
    assert [row["title"] for row in data["matched"]] == ["Sun Path"]
    assert data["matched"][0]["paths"] == [str(held)]
    assert [row["title"] for row in data["needs_review"]] == ["Tide"]
    assert [row["title"] for row in data["missing"]] == ["Glass Hour"]
    with review.open_store(cfg) as items:
        page = review.list_items(items, handler_key="intake.identify")
    assert [item.item_id for item in page.items] == [data["needs_review"][0]["review_item"]]
    assert envelope["pending_human_action"]["kind"] == "review"


def test_identify_with_nothing_to_ask_a_person_is_an_ok_exit(cfg, library, recognised):
    three_tracks(recognised)
    owned(library, "Aurora Bloom - Sun Path.flac")
    code, envelope = drive(["intake", "identify", str(recording(library))])
    assert code == int(ExitCode.OK), envelope
    assert envelope["pending_human_action"] is None
    assert len(envelope["data"]["matched"]) == 1
    assert len(envelope["data"]["missing"]) == 2


def test_identify_is_declared_adjudicating_because_it_offers_under_its_own_key():
    from cratekit.cli import registry

    assert registry.entry("intake.identify").adjudicates


def test_identify_writes_the_tracklist_naming_every_identified_row_in_order(
    cfg, library, recognised
):
    three_tracks(recognised)
    path = recording(library, "friday night.mp3")

    code, envelope = drive(["intake", "identify", str(path)])

    assert code == int(ExitCode.OK), envelope
    # The expected name is spelled out here, not asked of the code under test.
    token = hashlib.sha256(b"ID3").hexdigest()[:12]
    written = (
        cfg.paths.download_staging
        / intake_cli.TRACKLISTS_DIR
        / f"friday night-{token}.tracklist.txt"
    )
    assert written.read_text(encoding="utf-8") == (
        "Aurora Bloom - Sun Path\nNova Reef - Tide\nMira Vale - Glass Hour\n"
    )
    note = tracklist_note(envelope)
    assert str(written) in note["message"]
    assert "3 identified" in note["message"]


def test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row(cfg, library, recognised):
    """The file is a door, not a souvenir: what identify wrote, match reads."""
    from cratekit.acquire import match_cli

    recognised.answers[:] = [
        hit("Aurora Bloom", "Sun Path (Dub Mix)", isrc="X1"),
        hit("Nova Reef", "Tide", isrc="X2"),
        miss(),
    ]
    out = library / "lists"
    code, envelope = drive(["intake", "identify", str(recording(library)), "--out", str(out)])
    assert code == int(ExitCode.OK), envelope
    (written,) = list(out.iterdir())
    rows = match_cli.read_list(written)
    assert [(row.artist, row.title, row.version) for row in rows] == [
        ("Aurora Bloom", "Sun Path", "Dub Mix"),
        ("Nova Reef", "Tide", ""),
    ]


def test_a_tracklist_folder_that_is_a_file_is_refused_before_any_spend(cfg, library, recognised):
    three_tracks(recognised)
    blocker = library / "not-a-folder"
    blocker.write_text("x")
    code, envelope = drive(
        ["intake", "identify", str(recording(library)), "--out", str(blocker)]
    )
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert recognised.requests == [], "the refusal was paid for"
    assert recognised.ledger.used() == 0


def test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)
    real = config.atomic_write_bytes

    def failing(payload, path, **kwargs):
        if str(path).endswith(intake_cli.TRACKLIST_SUFFIX):
            raise PermissionError(13, "Permission denied", str(path))
        return real(payload, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", failing)
    path = recording(library)
    code, envelope = drive(["intake", "identify", str(path)])
    assert code == int(ExitCode.PRECONDITION), envelope
    # The constructor reclassifies a refusal chained from a permission error,
    # and keeps the site's own slug beside it.
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert envelope["cause"]["detail"]["declared_reason"] == "intake-list-unusable"
    assert "spends nothing" in envelope["cause"]["message"]
    monkeypatch.setattr(config, "atomic_write_bytes", real)
    code, envelope = drive(["intake", "identify", str(path)])
    assert code == int(ExitCode.OK), envelope
    assert len(recognised.requests) == 3, "the promise in the refusal was false"


def test_nothing_identified_writes_no_tracklist_and_reports_three_empty_arrays(
    cfg, library, recognised
):
    recognised.answers[:] = [miss(), miss(), miss()]
    code, envelope = drive(["intake", "identify", str(recording(library))])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"] == {"matched": [], "needs_review": [], "missing": []}
    assert not (cfg.paths.download_staging / intake_cli.TRACKLISTS_DIR).exists()
    assert [w["code"] for w in envelope["warnings"]] == []


def test_a_second_identify_over_the_same_recording_makes_zero_transport_calls(
    cfg, library, recognised
):
    """The brief's scenario, asserted on the fake transport, the ledger and
    the tracklist, which the second pass still writes from kept answers."""
    three_tracks(recognised)
    path = recording(library)
    first_code, first = drive(["intake", "identify", str(path)])
    assert len(recognised.requests) == 3

    second_code, second = drive(["intake", "identify", str(path)])

    assert (first_code, second_code) == (int(ExitCode.OK), int(ExitCode.OK))
    assert len(recognised.requests) == 3, "the second pass reached the transport"
    assert recognised.ledger.used() == 3, "the second pass was counted as spend"
    assert second["data"] == first["data"]
    assert intake_cli.CACHE_SERVED not in [w["code"] for w in first["warnings"]]
    served = [w for w in second["warnings"] if w["code"] == intake_cli.CACHE_SERVED]
    assert len(served) == 1 and "3 of 3" in served[0]["message"]
    assert "--refresh" in served[0]["message"]


def test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing(
    cfg, library, recognised
):
    """The ordinary two step use. ``intake set`` reads the cache identify wrote."""
    three_tracks(recognised)
    path = recording(library)
    drive(["intake", "identify", str(path)])

    job_id, envelope = queued_set(path)

    assert len(recognised.requests) == 3, "intake set paid for the recording again"
    assert recognised.ledger.used() == 3
    assert envelope["data"]["progress"]["calls"] == 0
    frozen = job_of(job_id).payload[intake_cli.TRACKS]
    assert [said["title"] for said in frozen.values()] == ["Sun Path", "Tide", "Glass Hour"]


# ═══════════════════════════════════════════════════════════════════════════
# R-925: a queued set's tracks can be read, in a file and through job show
# ═══════════════════════════════════════════════════════════════════════════


def test_a_set_writes_the_tracklist_identify_writes_for_the_same_rows(cfg, library, recognised):
    three_tracks(recognised)
    path = recording(library, "friday night.mp3")

    job_id, envelope = queued_set(path)

    # The expected name and text are spelled out here, not asked of the code.
    token = hashlib.sha256(b"ID3").hexdigest()[:12]
    written = (
        cfg.paths.download_staging
        / intake_cli.TRACKLISTS_DIR
        / f"friday night-{token}.tracklist.txt"
    )
    from_set = written.read_bytes()
    assert from_set == b"Aurora Bloom - Sun Path\nNova Reef - Tide\nMira Vale - Glass Hour\n"
    assert envelope["data"]["progress"][intake_cli.TRACKLIST] == str(written)
    note = tracklist_note(envelope)
    assert str(written) in note["message"] and "3 identified" in note["message"]

    written.unlink()
    code, identified = drive(["intake", "identify", str(path)])
    assert code == int(ExitCode.OK), identified
    assert written.read_bytes() == from_set, "set and identify wrote different tracklists"
    assert len(recognised.requests) == 3


def test_a_set_whose_tracklist_folder_is_a_file_is_refused_before_any_spend(
    cfg, library, recognised
):
    three_tracks(recognised)
    blocker = cfg.paths.download_staging / intake_cli.TRACKLISTS_DIR
    blocker.parent.mkdir(parents=True, exist_ok=True)
    blocker.write_text("x")

    code, envelope = drive(["intake", "set", str(recording(library))])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert any("--out" in step for step in envelope["cause"]["remediation"]["steps"])
    assert recognised.requests == [], "the refusal was paid for"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it(
    cfg, library, recognised, monkeypatch
):
    """The job is what the spend bought; a convenience file does not withhold it."""
    three_tracks(recognised)
    real = config.atomic_write_bytes

    def failing(payload, path, **kwargs):
        if str(path).endswith(intake_cli.TRACKLIST_SUFFIX):
            raise PermissionError(13, "Permission denied", str(path))
        return real(payload, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", failing)
    job_id, envelope = queued_set(recording(library))
    assert len(items_of(job_id)) == 3
    assert envelope["data"]["progress"][intake_cli.TRACKLIST] is None
    assert [w["code"] for w in envelope["warnings"]] == [intake_cli.TRACKLIST_UNWRITTEN]
    note = envelope["warnings"][0]["message"]
    assert f"crate job show {job_id}" in note and "PermissionError" in note
    assert not list(cfg.paths.download_staging.rglob("*" + intake_cli.TRACKLIST_SUFFIX))


def test_a_set_writes_its_tracklist_where_out_says(cfg, library, recognised):
    """The remedy the folder refusal names is a flag this verb takes."""
    three_tracks(recognised)
    out = library / "lists"
    code, envelope = drive(["intake", "set", str(recording(library)), "--out", str(out)])
    assert code == int(ExitCode.OK), envelope
    (written,) = list(out.iterdir())
    assert envelope["data"]["progress"][intake_cli.TRACKLIST] == str(written)
    assert not (cfg.paths.download_staging / intake_cli.TRACKLISTS_DIR).exists()


def test_a_resumed_set_writes_no_tracklist(cfg, library, recognised):
    three_tracks(recognised)
    job_id, envelope = queued_set(recording(library))
    written = Path(envelope["data"]["progress"][intake_cli.TRACKLIST])
    written.unlink()
    code, resumed = drive(resume_argv(job_id))
    assert code == int(ExitCode.OK), resumed
    assert not written.exists()
    assert intake_cli.TRACKLIST_WRITTEN not in [w["code"] for w in resumed["warnings"]]


def test_job_show_lists_every_track_an_intake_set_froze_in_set_order(cfg, library, recognised):
    recognised.answers[:] = [
        hit("Aurora Bloom", "Sun Path (Dub Mix)", isrc="X1"),
        hit("Nova Reef", "Tide"),
        hit("Mira Vale", "Glass Hour", isrc="X3"),
    ]
    job_id, _ = queued_set(recording(library))
    items = [item.item_id for item in items_of(job_id)]

    code, envelope = drive(["job", "show", job_id])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["progress"][cli_jobs.TRACKS_FIELD] == [
        {"item": items[0], "artist": "Aurora Bloom", "title": "Sun Path", "version": "Dub Mix", "isrc": "X1"},
        {"item": items[1], "artist": "Nova Reef", "title": "Tide", "version": "", "isrc": None},
        {"item": items[2], "artist": "Mira Vale", "title": "Glass Hour", "version": "", "isrc": "X3"},
    ]
    code, text = drive_human(["job", "show", job_id])
    assert code == int(ExitCode.OK), text
    assert "  tracks: 3\n" in text
    assert "    1. Aurora Bloom - Sun Path (Dub Mix), isrc X1\n" in text
    assert "    2. Nova Reef - Tide, no isrc\n" in text
    assert "    3. Mira Vale - Glass Hour, isrc X3\n" in text


def test_job_show_lists_a_playlist_jobs_tracks_too(cfg, library, monkeypatch):
    bind_playlist(
        monkeypatch,
        "pl-1",
        [Track("101", "Aurora Bloom", "Sun Path", isrc="X1"), Track("102", "Nova Reef", "Tide")],
    )
    code, queued = drive(["intake", "playlist", "pl-1"])
    assert code == int(ExitCode.OK), queued
    code, envelope = drive(["job", "show", queued["data"]["job_id"]])
    assert [(row["item"], row["title"], row["isrc"]) for row in envelope["data"]["progress"][cli_jobs.TRACKS_FIELD]] == [
        ("101", "Sun Path", "X1"),
        ("102", "Tide", None),
    ]


def test_job_show_on_a_job_of_another_handler_lists_no_tracks(cfg, library):
    """The payload carries a ``tracks`` key on purpose, so only the handler
    gate stands between it and the listing."""
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="master",
            payload={"source": "x", "tracks": {"x": {"artist": "Aurora Bloom", "title": "Sun Path"}}},
            cfg=cfg,
            item_ids=("x",),
        )
    code, envelope = drive(["job", "show", job.job_id])
    assert code == int(ExitCode.OK), envelope
    assert cli_jobs.TRACKS_FIELD not in envelope["data"]["progress"]
    code, text = drive_human(["job", "show", job.job_id])
    assert "tracks:" not in text and "Sun Path" not in text


def test_the_job_verbs_spell_the_intake_keys_the_intake_module_spells():
    """``cli.jobs`` spells these rather than importing the feature module."""
    assert cli_jobs.INTAKE_HANDLERS == intake_cli.INTAKE_KEYS
    assert cli_jobs.INTAKE_TRACKS_KEY == intake_cli.TRACKS


def test_a_changed_recording_misses_the_cache_and_is_paid_for(cfg, library, recognised):
    three_tracks(recognised)
    path = recording(library)
    drive(["intake", "identify", str(path)])
    path.write_bytes(b"ID3 and then a different set entirely")
    recognised.answers[:] = [hit("Other Act", "Other Record"), miss(), miss()]

    code, envelope = drive(["intake", "identify", str(path)])

    assert code == int(ExitCode.OK), envelope
    assert len(recognised.requests) == 6, "a changed file was served the old answers"
    assert [row["title"] for row in envelope["data"]["missing"]] == ["Other Record"]


def test_a_gap_is_paid_for_again_and_nothing_else_is(cfg, library, recognised):
    """A chunk that got no answer is never kept, so the second pass fills it."""
    recognised.answers[:] = [
        hit("Aurora Bloom", "Sun Path", isrc="X1"),
        ConnectionError("down"),
        miss(),
    ]
    path = recording(library)
    _, first = drive(["intake", "identify", str(path)])
    assert "recognition-incomplete" in [w["code"] for w in first["warnings"]]
    recognised.answers[:] = [hit("Nova Reef", "Tide", isrc="X2")]

    code, second = drive(["intake", "identify", str(path)])

    assert code == int(ExitCode.OK), second
    assert len(recognised.requests) == 4
    assert recognised.requests[-1].sample == b"chunk@25", "the wrong chunk was paid for"
    assert "recognition-incomplete" not in [w["code"] for w in second["warnings"]]
    assert [row["title"] for row in second["data"]["missing"]] == ["Sun Path", "Tide"]


def test_answers_that_could_not_be_kept_are_said_on_both_verbs(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)

    def failing(self, plan, answers):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(acrcloud.RecognitionCache, "write", failing)
    path = recording(library)
    code, envelope = drive(["intake", "identify", str(path)])
    assert code == int(ExitCode.OK), envelope
    assert intake_cli.CACHE_UNWRITTEN in [w["code"] for w in envelope["warnings"]]
    three_tracks(recognised)
    _, queued = queued_set(path)
    assert intake_cli.CACHE_UNWRITTEN in [w["code"] for w in queued["warnings"]]


def test_refresh_pays_for_every_chunk_again_and_the_new_answers_replace_the_kept_ones(
    cfg, library, recognised
):
    """A kept miss is served until somebody asks again. This is the asking."""
    recognised.answers[:] = [hit("Aurora Bloom", "Sun Path", isrc="X1"), miss(), miss()]
    path = recording(library)
    drive(["intake", "identify", str(path)])
    recognised.answers[:] = [
        hit("Aurora Bloom", "Sun Path", isrc="X1"),
        hit("Nova Reef", "Tide", isrc="X2"),
        miss(),
    ]

    code, refreshed = drive(["intake", "identify", str(path), "--refresh"])

    assert code == int(ExitCode.OK), refreshed
    assert len(recognised.requests) == 6, "--refresh read the kept answers"
    assert [row["title"] for row in refreshed["data"]["missing"]] == ["Sun Path", "Tide"]
    assert intake_cli.CACHE_SERVED not in [w["code"] for w in refreshed["warnings"]]
    job_id, queued = queued_set(path)
    assert len(recognised.requests) == 6, "the refreshed answers were not kept"
    assert len(items_of(job_id)) == 2
    recognised.answers[:] = [miss(), miss(), miss()]
    code, again = drive(["intake", "set", str(path), "--refresh"])
    assert len(recognised.requests) == 9, "intake set --refresh read the kept answers"
    assert again["data"]["state"] == "nothing-identified"


def test_two_recordings_sharing_a_stem_keep_a_tracklist_each(cfg, library, recognised):
    """A recorder names every set the same. The name carries the audio's digest."""
    (library / "aug").mkdir()
    (library / "sep").mkdir()
    first = library / "aug" / "REC001.WAV"
    second = library / "sep" / "REC001.WAV"
    first.write_bytes(b"august")
    second.write_bytes(b"september")
    three_tracks(recognised)
    drive(["intake", "identify", str(first)])
    recognised.answers[:] = [hit("Other Act", "Other Record"), miss(), miss()]
    drive(["intake", "identify", str(second)])

    folder = cfg.paths.download_staging / intake_cli.TRACKLISTS_DIR
    texts = sorted(path.read_text() for path in folder.iterdir())
    assert texts == [
        "Aurora Bloom - Sun Path\nNova Reef - Tide\nMira Vale - Glass Hour\n",
        "Other Act - Other Record\n",
    ]


def test_a_recording_with_no_digest_is_named_by_its_path_so_two_folders_still_differ(tmp_path):
    one = intake_cli.tracklist_name(intake_cli.SetRecording.local(tmp_path / "a" / "REC001.WAV"), "")
    other = intake_cli.tracklist_name(intake_cli.SetRecording.local(tmp_path / "b" / "REC001.WAV"), "")
    assert one != other
    assert one.startswith("REC001-") and one.endswith(intake_cli.TRACKLIST_SUFFIX)
    assert intake_cli.tracklist_name(intake_cli.SetRecording.local(tmp_path / "REC001.WAV"), "ab" * 32) == (
        "REC001-abababababab.tracklist.txt"
    )


def test_an_absent_library_is_refused_before_the_spend_and_never_read_as_an_empty_one(
    cfg, library, recognised, tmp_path
):
    """Absence read as evidence of absence, refused: an unplugged drive would
    otherwise report every owned track missing with a clean exit."""
    three_tracks(recognised)
    path = tmp_path / "set.mp3"
    path.write_bytes(b"ID3")
    (library / "Music").rmdir()

    code, envelope = drive(["intake", "identify", str(path)])

    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "library-volume-unmounted"
    assert recognised.requests == [], "the refusal was paid for"


def test_doctor_is_told_identify_needs_the_library():
    from cratekit.cli import registry

    assert "library.mounted" in registry.entry("intake.identify").doctor_checks


def test_a_set_nothing_was_identified_in_still_says_its_answers_could_not_be_kept(
    cfg, library, recognised, monkeypatch
):
    recognised.answers[:] = [miss(), miss(), miss()]

    def failing(self, plan, answers):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(acrcloud.RecognitionCache, "write", failing)
    code, envelope = drive(["intake", "set", str(recording(library))])
    assert envelope["data"]["state"] == "nothing-identified"
    assert [w["code"] for w in envelope["warnings"]] == [intake_cli.CACHE_UNWRITTEN]


def test_the_unwritable_tracklist_refusal_does_not_promise_a_free_rerun_over_a_gap(
    cfg, library, recognised, monkeypatch
):
    recognised.answers[:] = [hit("Aurora Bloom", "Sun Path"), ConnectionError("down"), miss()]
    real = config.atomic_write_bytes

    def failing(payload, path, **kwargs):
        if str(path).endswith(intake_cli.TRACKLIST_SUFFIX):
            raise PermissionError(13, "Permission denied", str(path))
        return real(payload, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", failing)
    code, envelope = drive(["intake", "identify", str(recording(library))])
    message = envelope["cause"]["message"]
    assert "spends nothing" not in message
    assert "pays only for the 1 chunk(s)" in message


def test_a_repeated_recording_in_one_set_is_one_item_per_play_and_one_per_fold(
    cfg, library, recognised
):
    recognised.answers[:] = [
        hit("Aurora Bloom", "Sun Path", isrc="X1"),
        hit("Aurora Bloom", "Sun Path", isrc="X1"),
        hit("Nova Reef", "Tide", isrc="X2"),
    ]
    job_id, _ = queued_set(recording(library))
    assert len(items_of(job_id)) == 2


def test_the_help_text_and_the_registry_summary_say_what_the_verb_takes():
    """SEAM P6, both ways. A verb that refuses a URL cannot advertise one, and
    since U104 these two take one, so the help and the summary have to say so.
    The URL's own behaviour is ``tests/intake/test_set_fetch.py``."""
    import argparse

    from cratekit.cli import registry

    for name, build in (("intake.set", intake_cli.build_set), ("intake.identify", intake_cli.build_identify)):
        parser = argparse.ArgumentParser()
        build(parser, None)
        source = next(a for a in parser._actions if a.dest == "source")
        assert "on this machine" in source.help
        assert "mix URL" in source.help
        assert "yt-dlp" in source.help
        entry = next(e for e in registry.ENTRIES if e.name == name)
        assert "mix URL" in entry.summary
        assert "binary.ffprobe" in entry.doctor_checks
        assert "credential.recognition" in entry.doctor_checks
        assert "credential.provider" not in entry.doctor_checks
        # Only an address needs the downloader, so doctor does not demand it.
        assert "binary.yt-dlp" not in entry.doctor_checks


def test_a_tilde_is_expanded_before_the_file_is_looked_for(cfg, library, recognised, monkeypatch):
    three_tracks(recognised)
    monkeypatch.setenv("HOME", str(library))
    recording(library, "friday.mp3")
    job_id, _ = queued_set(Path("~/friday.mp3"))
    assert job_of(job_id).payload[intake_cli.SOURCE] == str(library / "friday.mp3")


def test_a_missing_recording_is_refused_by_name(cfg, library, recognised):
    code, envelope = drive(["intake", "set", str(library / "no-such-set.mp3")])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert recognised.requests == []


def test_the_gate_refuses_a_set_with_no_credentials_and_touches_no_seam(
    cfg, library, monkeypatch
):
    monkeypatch.setattr(recognize.binaries, "find", lambda name: f"/usr/bin/{name}")
    transport = FakeTransport()
    monkeypatch.setattr(acrcloud, "http_transport", transport)
    code, envelope = drive(["intake", "set", str(recording(library))])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-recognition-unready"
    assert transport.requests == []
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_spend_refusal_at_the_queue_is_reported_as_policy_and_queues_nothing(
    cfg, library, recognised
):
    recognised.answers[:] = [hit("Aurora Bloom", "Sun Path"), {"status": {"code": 3003, "msg": "limit"}}]
    code, envelope = drive(["intake", "set", str(recording(library))])
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["reason"] == "intake-recognition-spend-bound"
    assert envelope["cause"]["detail"]["kind"] == "provider-quota"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_the_resume_argv_carries_the_frozen_source_and_the_job(cfg, library, recognised):
    three_tracks(recognised)
    path = recording(library)
    job_id, _ = queued_set(path)
    assert resume_argv(job_id) == ["intake", "set", str(path.absolute()), "--job", job_id]


# ═══════════════════════════════════════════════════════════════════════════
# The worker, through the real resume path
# ═══════════════════════════════════════════════════════════════════════════


def test_a_set_job_runs_pending_to_done_and_reports_owned_offered_and_missing(
    cfg, library, recognised
):
    """The whole point of the unit. Read from the store, not the exit code."""
    three_tracks(recognised)
    owned(library, "Aurora Bloom - Sun Path.flac")
    owned(library, "Nova Reef - Tide (Someone Remix).flac")
    job_id, _ = queued_set(recording(library))

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    assert set(states(job_id).values()) == {jobs.ItemState.DONE}
    assert job_of(job_id).state is jobs.JobState.SUCCEEDED
    found = by_title(cfg, job_id)
    assert found["Sun Path"]["state"] == "owned"
    assert found["Sun Path"]["paths"] == [str(library / "Music" / "Aurora Bloom - Sun Path.flac")]
    assert found["Tide"]["state"] == "offered"
    assert found["Tide"]["review_item"]
    assert found["Glass Hour"]["state"] == "missing"
    assert found["Glass Hour"]["acquisitions"], "a missing track carries its acquisition options"
    assert all(report["acquired"] is False for report in found.values())
    progress = envelope["data"]["progress"]
    assert progress["reported"] == 3
    assert (progress["owned"], progress["offered"], progress["missing"]) == (1, 1, 1)
    assert progress["acquired"] == 0
    assert progress["by_reason"] == {
        "owned": {"exact": 1},
        "offered": {"version-differs": 1},
        "missing": {"not-in-library": 1},
        "suppressed": {},
    }
    for item in items_of(job_id):
        assert item.artifact and Path(item.artifact).is_file()
        assert json.loads(Path(item.artifact).read_text())["item_id"] == item.item_id


def test_an_offered_track_is_a_review_item_and_no_intake_file_is_written(
    cfg, library, recognised
):
    """R-140, one layer down: an offer is a question, not an acquisition."""
    recognised.answers[:] = [hit("Nova Reef", "Tide", isrc="X2"), miss(), miss()]
    owned(library, "Nova Reef - Tide (Someone Remix).flac")
    job_id, _ = queued_set(recording(library))

    drive(resume_argv(job_id))

    report = by_title(cfg, job_id)["Tide"]
    with review.open_store(cfg) as items:
        page = review.list_items(items, queue=str(review.Queue.VERSION_MATCH))
    assert [item.item_id for item in page.items] == [report["review_item"]]
    assert page.items[0].verdict is None
    assert not list(library.rglob("*_inboxed.xml")), "an offer wrote an intake file"
    assert not list(library.rglob("*_synced.xml"))


def test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it(
    cfg, library, recognised, monkeypatch
):
    """The brief's scenario. The item's cause is asserted, not the exit code."""
    three_tracks(recognised)
    job_id, _ = queued_set(recording(library))
    real = intake_cli.resolve_track
    resolved: list[str] = []

    def failing(wanted, job, frozen):
        resolved.append(wanted.title)
        if wanted.title == "Tide":
            raise refuse(
                "unavailable-transient",
                "the review store could not be opened mid set",
                remedy=Remedy.RETRY_LATER,
                retryable=True,
                origin=("test",),
            )
        return real(wanted, job, frozen)

    monkeypatch.setattr(intake_cli, "resolve_track", failing)

    code, envelope = drive(resume_argv(job_id))

    # A JOB THAT ENDED BADLY IS NOT AN OK EXIT. The engine records the job
    # failed and returns; the verb re-raises the cause, so the exit code says
    # so and the envelope carries the partial failure with the item's own
    # cause nested inside it.
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "unavailable-transient"
    assert envelope["cause"]["detail"]["failed"] == 1
    tide = next(item for item in items_of(job_id) if item.state is jobs.ItemState.FAILED)
    assert job_of(job_id).payload[intake_cli.TRACKS][tide.item_id]["title"] == "Tide"
    assert tide.cause.reason == "unavailable-transient"
    assert "mid set" in tide.cause.message
    assert sorted(states(job_id).values(), key=str) == sorted(
        [jobs.ItemState.DONE, jobs.ItemState.FAILED, jobs.ItemState.DONE], key=str
    )
    assert job_of(job_id).state is jobs.JobState.FAILED
    assert len(reports(cfg, job_id)) == 2

    monkeypatch.setattr(intake_cli, "resolve_track", real)
    monkeypatch.setattr(intake_cli, "resolve_track", lambda w, j, c: (resolved.append(w.title), real(w, j, c))[1])
    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    before = len(resolved)
    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert set(states(job_id).values()) == {jobs.ItemState.DONE}
    assert resolved[before:] == ["Tide"], "the resume redid more than the failed item"
    assert len(reports(cfg, job_id)) == 3


def test_the_frozen_library_reaches_the_worker_not_the_live_one(
    cfg, library, recognised, tmp_path, monkeypatch
):
    """KTD9. The library root moves after the queue; the worker resolves
    against the one the job froze.

    THE DIVERGENCE HAS TO COME FROM THE FILE. ``config.from_dict`` applies
    environment overrides unconditionally and ``jobs.frozen_config`` rebuilds
    through it, so with the root variable still set both readings relocate
    onto it and agree whatever the saved file says. Recorded in
    ``docs/solutions/workflow-issues/a-frozen-config-is-frozen-against-the-file-not-against-an-env-override.md``.
    """
    three_tracks(recognised)
    owned(library, "Aurora Bloom - Sun Path.flac")
    job_id, _ = queued_set(recording(library))

    elsewhere = tmp_path / "elsewhere"
    (elsewhere / "Music").mkdir(parents=True)
    (elsewhere / "db").mkdir()
    (elsewhere / "Music" / "Nova Reef - Tide.flac").write_bytes(b"")
    monkeypatch.delenv(config.ENV_LIBRARY_ROOT)
    _configure(elsewhere)
    assert config.load().library.root == elsewhere, (
        "the live configuration still names the queued library, so the two "
        "readings cannot differ and this test would pass either way"
    )

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert any(w["code"] == "config-drift" for w in envelope["warnings"]), envelope
    found = by_title(cfg, job_id)
    assert found["Sun Path"]["state"] == "owned", "the live library was consulted"
    assert found["Tide"]["state"] == "missing", "the live library was consulted"


def test_the_library_is_indexed_once_per_drive_not_once_per_item(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)
    job_id, _ = queued_set(recording(library))
    walks: list[Path] = []
    real = match.index_library

    def counting(root, **kwargs):
        walks.append(root)
        return real(root, **kwargs)

    monkeypatch.setattr(match, "index_library", counting)
    intake_cli.reset_cache()

    drive(resume_argv(job_id))

    assert walks == [library / "Music"]


def test_an_open_job_with_no_items_refuses_rather_than_reporting_success(cfg, library):
    """A job queued by a build before this unit. The zero item rule."""
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key=SET_KEY, payload={intake_cli.SOURCE: str(library / "old.mp3")}, cfg=cfg
        )
    code, envelope = drive(["intake", "set", str(library / "old.mp3"), "--job", job.job_id])
    assert envelope["cause"]["reason"] == "internal-error", envelope
    assert "did not record what its items were" in envelope["cause"]["message"]
    assert job_of(job.job_id).state is jobs.JobState.QUEUED


def test_a_job_of_another_verb_is_refused_rather_than_driven_under_this_envelope(cfg, library):
    with jobs.open_store() as store:
        job = jobs.enqueue(store, handler_key="master", payload={"source": "x"}, cfg=cfg, item_ids=("x",))
    code, envelope = drive(["intake", "set", "x", "--job", job.job_id])
    assert envelope["cause"]["reason"] == "job-unknown", envelope
    assert "not an intake job" in envelope["cause"]["message"]
    assert states(job.job_id) == {"x": jobs.ItemState.PENDING}


def test_a_stray_file_beside_the_reports_does_not_take_the_summary_down(cfg, library, recognised):
    three_tracks(recognised)
    job_id, _ = queued_set(recording(library))
    drive(resume_argv(job_id))
    first = Path(items_of(job_id)[0].artifact)
    (first.parent / "notes.json").write_text("{}")
    (first.parent / "0001 (copy).json").write_text("{}")
    code, envelope = drive(resume_argv(job_id))
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["progress"]["reported"] == 3


def test_an_item_the_payload_does_not_carry_fails_by_name_rather_than_resolving_nothing(cfg, library):
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=SET_KEY,
            payload={intake_cli.SOURCE: "x", intake_cli.TRACKS: {}},
            cfg=cfg,
            item_ids=("rc_orphan",),
        )
        item = jobs.items(store, job.job_id)[0]
    with pytest.raises(CratekitError) as excinfo:
        intake_cli.handle(job, item, cfg)
    assert excinfo.value.cause.reason == "internal-error"
    assert excinfo.value.cause.detail["item_id"] == "rc_orphan"


def test_the_worker_reads_each_items_own_track_and_never_the_first(cfg, library, recognised):
    three_tracks(recognised)
    job_id, _ = queued_set(recording(library))
    drive(resume_argv(job_id))
    assert [r["track"]["title"] for r in reports(cfg, job_id)] == ["Sun Path", "Tide", "Glass Hour"]
    assert [r["item_id"] for r in reports(cfg, job_id)] == [i.item_id for i in items_of(job_id)]


def test_a_resume_that_redoes_an_offered_item_asks_nothing_twice(cfg, library, recognised):
    recognised.answers[:] = [hit("Nova Reef", "Tide", isrc="X2"), miss(), miss()]
    owned(library, "Nova Reef - Tide (Someone Remix).flac")
    job_id, _ = queued_set(recording(library))
    job = job_of(job_id)
    offered = next(item for item in items_of(job_id) if job.payload[intake_cli.TRACKS][item.item_id]["title"] == "Tide")
    # What a resume does to an item a killed driver had claimed: the worker
    # runs it again, whole. The offer underneath is content addressed.
    first = intake_cli.handle(job, offered, cfg)
    second = intake_cli.handle(job, offered, cfg)
    assert first.final == second.final
    with review.open_store(cfg) as items:
        page = review.list_items(items, queue=str(review.Queue.VERSION_MATCH))
    assert len(page.items) == 1


def test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked(
    cfg, library, tmp_path
):
    """THE PATH THAT FILED THE LIVE ITEMS. The 85 stale version questions the
    residual titled "A review item outlives its question" measured were asked
    by intake jobs, and the job that later owned their rows by ISRC was an
    intake job too. The per item worker used to open the review store only for
    a question, so the owning job would have retired none of them."""
    owned(library, "04A - 126 - Malive - Burning (Radio Edit).flac")
    line = match.read_row(
        {"id": "301", "artist": {"name": "Malive"}, "title": "Burning (Extended Mix)",
         "isrc": "USNRS2644532"},
        origin=match.TIDAL, position=1,
    )
    with jobs.open_store() as store:
        earlier = jobs.enqueue(
            store, handler_key=PLAYLIST_KEY, payload={intake_cli.SOURCE: "x"}, cfg=cfg
        )
        later = jobs.enqueue(
            store, handler_key=PLAYLIST_KEY, payload={intake_cli.SOURCE: "y"}, cfg=cfg
        )

    asked = intake_cli.resolve_track(line, earlier, cfg)
    assert (asked.state, asked.why) == (match.MatchState.NEEDS_REVIEW, match.Why.VERSION_DIFFERS)
    with review.open_store(cfg) as items:
        assert [one.item_id for one in review.list_items(items)] == [asked.item_id]

    tagged_container(
        tmp_path, library / "Music" / "04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac",
        artist="Malive, Tito Azevedo, MRQZ", title="04A - 126 - Burning (Extended Mix)",
        isrc="USNRS2644532",
    )
    intake_cli.reset_cache()
    settled = intake_cli.resolve_track(line, later, cfg)
    assert (settled.state, settled.why) == (match.MatchState.MATCHED, match.Why.ISRC_EXACT)
    with review.open_store(cfg) as items:
        assert [one.item_id for one in review.list_items(items)] == []
        retired = review.get(items, asked.item_id)
    assert retired.verdict is review.Verdict.SUPERSEDED
    assert retired.actor == "isrc-exact"


# ═══════════════════════════════════════════════════════════════════════════
# The playlist: list at the queue
# ═══════════════════════════════════════════════════════════════════════════


def test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id(
    cfg, library, monkeypatch
):
    fake = bind_playlist(
        monkeypatch,
        "pl-1",
        [Track("101", "Aurora Bloom", "Sun Path"), Track("102", "Nova Reef", "Tide", isrc="X2"),
         Track("101", "Aurora Bloom", "Sun Path")],
    )

    code, envelope = drive(["intake", "playlist", "pl-1"])

    assert code == int(ExitCode.OK), envelope
    job_id = envelope["data"]["job_id"]
    assert fake.playlists_asked_for == ["pl-1"]
    assert [item.item_id for item in items_of(job_id)] == ["101", "102"]
    frozen = job_of(job_id).payload[intake_cli.TRACKS]
    assert frozen["102"] == {
        "artist": "Nova Reef", "title": "Tide", "version": "", "key": None, "isrc": "X2",
        "origin": match.TIDAL, "ref": "102", "spelled": "Tide", "other_reading": None,
        "several_artists": False,
    }
    assert resume_argv(job_id) == ["intake", "playlist", "pl-1", "--job", job_id]


def test_a_playlist_job_runs_pending_to_done_through_the_resume_path(cfg, library, monkeypatch):
    bind_playlist(
        monkeypatch, "pl-1", [Track("101", "Aurora Bloom", "Sun Path"), Track("102", "Nova Reef", "Tide")]
    )
    owned(library, "Aurora Bloom - Sun Path.flac")
    code, envelope = drive(["intake", "playlist", "pl-1"])
    job_id = envelope["data"]["job_id"]

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    assert states(job_id) == {"101": jobs.ItemState.DONE, "102": jobs.ItemState.DONE}
    found = by_title(cfg, job_id)
    assert found["Sun Path"]["state"] == "owned"
    assert found["Tide"]["state"] == "missing"
    assert envelope["data"]["progress"]["acquired"] == 0


def test_no_provider_session_refuses_honestly_and_queues_nothing(cfg):
    assert catalogue.bound() is True
    code, envelope = drive(["intake", "playlist", "pl-1"])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "credential-missing"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_playlist_the_catalogue_cannot_list_is_unreadable_not_empty(cfg, monkeypatch):
    bind_playlist(monkeypatch, "pl-1", [])
    code, envelope = drive(["intake", "playlist", "pl-other"])
    assert envelope["cause"]["reason"] == "label-playlist-unreadable", envelope
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_empty_playlist_queues_nothing_and_says_so(cfg, monkeypatch):
    bind_playlist(monkeypatch, "pl-1", [])
    code, envelope = drive(["intake", "playlist", "pl-1"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["state"] == "no-tracks"
    assert envelope["data"]["job_id"] == ""


def test_a_provider_row_without_an_identifier_is_refused_by_position(cfg, monkeypatch):
    bind_playlist(
        monkeypatch, "pl-1", [Track("101", "Aurora Bloom", "Sun Path"), Track("", "Nova Reef", "Tide")]
    )
    code, envelope = drive(["intake", "playlist", "pl-1"])
    assert envelope["cause"]["reason"] == "intake-list-unusable", envelope
    assert envelope["cause"]["detail"]["positions"] == [2]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_row_naming_no_artist_is_the_readers_own_refusal(cfg, monkeypatch):
    bind_playlist(monkeypatch, "pl-1", [Track("101", "", "Sun Path")])
    code, envelope = drive(["intake", "playlist", "pl-1"])
    assert envelope["cause"]["reason"] == "intake-list-unusable", envelope
    assert "names no artist" in envelope["cause"]["message"]


# ═══════════════════════════════════════════════════════════════════════════
# U70: the reserved reference ``favorites`` lists the account's hearts
# ═══════════════════════════════════════════════════════════════════════════


def bind_hearts(monkeypatch, hearts: list[Track]) -> StrictCatalogue:
    """The account's hearts on a catalogue that refuses anything undeclared."""
    fake = StrictCatalogue(hearts=hearts)
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def five_hearts() -> list[Track]:
    return [
        Track("201", "Aurora Bloom", "Sun Path"),
        Track("202", "Nova Reef", "Tide"),
        Track("203", "Mira Vale", "Glass Hour"),
        Track("204", "Lumen Drift", "Salt Road"),
        Track("205", "Kite Harbor", "Low Tide Signal"),
    ]


def queued_hearts(cfg, library, monkeypatch, spelled: str = "favorites") -> tuple[str, StrictCatalogue]:
    fake = bind_hearts(monkeypatch, five_hearts())
    owned(library, "Aurora Bloom - Sun Path.flac")
    owned(library, "Mira Vale - Glass Hour.flac")
    owned(library, "Nova Reef - Tide (Someone Remix).flac")
    code, envelope = drive(["intake", "playlist", spelled])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"], fake


def test_favorites_lists_the_hearts_and_never_asks_for_a_playlist(cfg, library, monkeypatch):
    job_id, fake = queued_hearts(cfg, library, monkeypatch)

    assert fake.heart_listings == 1
    assert fake.playlists_asked_for == [], "the reserved reference reached playlist_for"
    assert [item.item_id for item in items_of(job_id)] == ["201", "202", "203", "204", "205"]
    job = job_of(job_id)
    assert job.handler_key == PLAYLIST_KEY
    assert job.payload[intake_cli.SOURCE] == "favorites"
    assert job.payload["source_id"] == "favorites"
    assert resume_argv(job_id) == ["intake", "playlist", "favorites", "--job", job_id]


def test_favorites_resolves_each_heart_owned_offered_or_missing(cfg, library, monkeypatch):
    job_id, _ = queued_hearts(cfg, library, monkeypatch)

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    progress = envelope["data"]["progress"]
    assert (progress["owned"], progress["offered"], progress["missing"]) == (2, 1, 2)
    assert progress["acquired"] == 0
    found = by_title(cfg, job_id)
    assert {title for title, report in found.items() if report["state"] == "owned"} == {
        "Sun Path", "Glass Hour",
    }
    assert found["Tide"]["state"] == "offered"


def test_the_missing_hearts_carry_the_provider_id_acquisition_reads(cfg, library, monkeypatch):
    """What ``intake missing --job`` lists: the missing reports, by provider id.

    U69 landed that verb, and the drive through it, down to a download against
    the fake adapter, is in ``tests/test_intake_missing.py``. This pins the half
    U70 owns, that a finished hearts job holds
    exactly two missing reports and each names the provider identifier a
    download is asked for.
    """
    job_id, _ = queued_hearts(cfg, library, monkeypatch)
    drive(resume_argv(job_id))

    missing = [report for report in reports(cfg, job_id) if report["state"] == "missing"]
    assert sorted(report["track"]["ref"] for report in missing) == ["204", "205"]
    assert all(report["item_id"] == report["track"]["ref"] for report in missing)


def test_a_rerun_after_acquiring_reports_the_heart_owned_with_no_cursor(cfg, library, monkeypatch):
    first, _ = queued_hearts(cfg, library, monkeypatch)
    drive(resume_argv(first))
    owned(library, "Lumen Drift - Salt Road.flac")

    code, envelope = drive(["intake", "playlist", "favorites"])
    second = envelope["data"]["job_id"]
    drive(resume_argv(second))

    assert second != first
    assert by_title(cfg, second)["Salt Road"]["state"] == "owned"
    assert by_title(cfg, second)["Low Tide Signal"]["state"] == "missing"


@pytest.mark.parametrize("spelled", ["Favorites", " FAVORITES "])
def test_the_reserved_reference_is_read_however_it_is_cased(cfg, library, monkeypatch, spelled):
    job_id, fake = queued_hearts(cfg, library, monkeypatch, spelled)
    assert fake.playlists_asked_for == []
    assert job_of(job_id).payload[intake_cli.SOURCE] == "favorites"


def test_a_truncated_hearts_listing_refuses_whole_and_queues_nothing(cfg, monkeypatch):
    class Truncated(StrictCatalogue):
        def favourite_tracks(self):
            raise listing.ListingTruncated("favorite_tracks spent its whole budget")

    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(Truncated(hearts=five_hearts())))
    code, envelope = drive(["intake", "playlist", "favorites"])

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "label-playlist-unreadable", envelope
    assert envelope["cause"]["detail"]["kind"] == "ListingTruncated"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_unreadable_hearts_listing_is_unreadable_not_empty(cfg, monkeypatch):
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(UnreadableCatalogue()))
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert envelope["cause"]["reason"] == "label-playlist-unreadable", envelope
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_adapter_refusal_under_the_hearts_listing_passes_through(cfg, monkeypatch):
    class Expired(StrictCatalogue):
        def favourite_tracks(self):
            raise refuse(
                "credential-missing",
                "the stored session expired mid listing",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
                origin=("test",),
            )

    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(Expired()))
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert envelope["cause"]["reason"] == "credential-missing", envelope


def test_a_heart_without_an_identifier_is_refused_by_position(cfg, monkeypatch):
    hearts = five_hearts()
    hearts[2] = Track("", "Mira Vale", "Glass Hour")
    bind_hearts(monkeypatch, hearts)
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert envelope["cause"]["reason"] == "intake-list-unusable", envelope
    assert envelope["cause"]["detail"]["positions"] == [3]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_account_with_no_hearts_queues_nothing_and_says_so(cfg, monkeypatch):
    bind_hearts(monkeypatch, [])
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["state"] == "no-tracks"
    assert envelope["data"]["progress"]["source"] == "favorites"


def test_a_playlist_reference_still_reaches_the_playlist_and_not_the_hearts(cfg, monkeypatch):
    fake = StrictCatalogue(
        playlists={"pl-1": FakePagedPlaylist([Track("101", "Aurora Bloom", "Sun Path")])},
        hearts=five_hearts(),
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    code, envelope = drive(["intake", "playlist", "pl-1"])
    assert code == int(ExitCode.OK), envelope
    assert fake.heart_listings == 0
    assert "source_id" not in job_of(envelope["data"]["job_id"]).payload


def test_the_strict_catalogue_answers_the_hearts_and_still_refuses_the_undeclared():
    strict = StrictCatalogue(hearts=five_hearts())
    assert "favourite_tracks" in PROTOCOL_METHODS
    assert [track.id for track in strict.favourite_tracks()] == ["201", "202", "203", "204", "205"]
    with pytest.raises(AssertionError):
        strict.add_heart


def test_the_fake_declares_exactly_the_protocol_the_seam_declares():
    declared = {
        name
        for name, value in vars(catalogue.Catalogue).items()
        if callable(value) and not name.startswith("_")
    }
    assert declared == PROTOCOL_METHODS


# ═══════════════════════════════════════════════════════════════════════════
# The item key
# ═══════════════════════════════════════════════════════════════════════════


def test_a_recognised_track_is_keyed_by_recording_version_and_isrc_and_a_provider_row_by_its_id():
    plain = match.Wanted(artist="Aurora Bloom", title="Sun Path")
    same = match.Wanted(artist="aurora bloom", title="SUN PATH")
    remix = match.Wanted(artist="Aurora Bloom", title="Sun Path", version="Someone Remix")
    coded = match.Wanted(artist="Aurora Bloom", title="Sun Path", isrc="X1")
    provider = match.Wanted(artist="Aurora Bloom", title="Sun Path", origin=match.TIDAL, ref="101")
    assert intake_cli.item_key(plain) == intake_cli.item_key(same)
    assert intake_cli.item_key(plain) != intake_cli.item_key(remix)
    assert intake_cli.item_key(plain) != intake_cli.item_key(coded)
    assert intake_cli.item_key(provider) == "101"
    assert intake_cli.item_key(plain).startswith("rc_")
    assert "Sun" not in intake_cli.item_key(plain), "an item identifier is never a display name"


def test_a_frozen_row_thaws_to_the_row_the_engine_reads():
    row = match.Wanted(
        artist="Aurora Bloom", title="Sun Path", version="Someone Remix", key="8A",
        isrc="X1", origin=match.TEXT, spelled="Sun Path (Someone Remix)",
    )
    frozen = intake_cli.frozen_rows((row,))
    thawed = intake_cli.thawed(next(iter(frozen.values())))
    assert (thawed.artist, thawed.title, thawed.version, thawed.key, thawed.isrc) == (
        "Aurora Bloom", "Sun Path", "Someone Remix", "8A", "X1"
    )
    assert thawed.recording == row.recording
    assert thawed.listed == row.listed
    assert thawed.identity == row.identity


def test_a_titles_other_reading_survives_the_freeze():
    """``resolve_one`` asks the library about the second reading of an
    ambiguous title, so a freeze that dropped it would narrow the question."""
    row = match.read_text_lines("Aurora Bloom - Sun Path - Live\n")[0]
    assert row.other_reading is not None, "the fixture title is not ambiguous"
    frozen = intake_cli.frozen_rows((row,))
    said = next(iter(frozen.values()))
    assert said["other_reading"] == list(row.other_reading)
    thawed = intake_cli.thawed(said)
    assert thawed.other_reading == row.other_reading
    assert [(r.title, r.version) for r in thawed.readings] == [
        (r.title, r.version) for r in row.readings
    ]
    plain = intake_cli.thawed({"artist": "A", "title": "T", "other_reading": ["only-one"]})
    assert plain.other_reading is None, "a malformed reading is dropped, not guessed"


# ═══════════════════════════════════════════════════════════════════════════
# R-301: the recognition section is what the paid path reads
# ═══════════════════════════════════════════════════════════════════════════


def _recognition(library: Path, **section) -> config.Config:
    """A configured machine whose ``[recognition]`` section says ``section``."""
    built = config.from_dict(
        valid_data(library, profile={"name": "full"}, recognition=section)
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.mark.parametrize("verb", ["identify", "set"])
def test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call(
    cfg, library, recognised, verb
):
    """THE COST R-301 NAMED. With nothing configured the per run cap was the
    only bound, so a month that had already spent its plan kept paying. The
    default section bounds the month, and the refusal names the key to raise."""
    recognised.ledger.record(config.DEFAULT_RECOGNITION_MONTHLY_CALLS - 1)
    three_tracks(recognised)

    code, envelope = drive(["intake", verb, str(recording(library))])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["reason"] == "intake-recognition-spend-bound"
    detail = envelope["cause"]["detail"]
    assert detail["kind"] == "monthly"
    assert detail["bound"] == config.DEFAULT_RECOGNITION_MONTHLY_CALLS
    assert detail["key"] == "recognition.monthly_calls"
    assert "recognition.monthly_calls" in envelope["cause"]["message"]
    assert recognised.requests == [], "the month's bound was paid past"
    assert recognised.ledger.used() == config.DEFAULT_RECOGNITION_MONTHLY_CALLS - 1


@pytest.mark.parametrize("verb", ["identify", "set"])
def test_the_configured_monthly_bound_is_the_one_the_verb_meets(library, recognised, verb):
    _recognition(library, monthly_calls=2)
    three_tracks(recognised)

    code, envelope = drive(["intake", verb, str(recording(library))])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["detail"]["bound"] == 2
    assert recognised.requests == []
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == (), "a refused set queued a job"


def test_a_month_within_the_configured_bound_is_paid_for(library, recognised):
    _recognition(library, monthly_calls=3)
    three_tracks(recognised)
    code, envelope = drive(["intake", "identify", str(recording(library))])
    assert code in (int(ExitCode.OK), int(ExitCode.PENDING_HUMAN)), envelope
    assert len(recognised.requests) == 3
    assert recognised.ledger.used() == 3


@pytest.mark.parametrize("verb", ["identify", "set"])
def test_the_configured_host_is_the_one_every_paid_call_is_sent_to(library, recognised, verb):
    _recognition(library, host="identify-eu-west-1.acrcloud.com")
    three_tracks(recognised)

    code, envelope = drive(["intake", verb, str(recording(library))])

    assert code in (int(ExitCode.OK), int(ExitCode.PENDING_HUMAN)), envelope
    assert [request.url for request in recognised.requests] == [
        f"https://identify-eu-west-1.acrcloud.com{acrcloud.ENDPOINT}"
    ] * 3


def test_a_queued_set_freezes_the_recognition_section_it_was_identified_under(
    library, recognised
):
    _recognition(library, host="identify-eu-west-1.acrcloud.com", monthly_calls=50)
    three_tracks(recognised)
    job_id, _ = queued_set(recording(library))
    frozen = jobs.frozen_config(job_of(job_id)).recognition
    assert frozen == config.RecognitionConfig(
        host="identify-eu-west-1.acrcloud.com", monthly_calls=50
    )


# ═══════════════════════════════════════════════════════════════════════════
# R-678: what a person reads without asking for json
# ═══════════════════════════════════════════════════════════════════════════


def test_queueing_favorites_names_the_job_and_the_command_that_drives_it(
    cfg, library, monkeypatch
):
    """The sittings read the identifier out of ``job list --output json`` every time."""
    bind_hearts(monkeypatch, five_hearts())

    code, text = drive_human(["intake", "playlist", "favorites"])

    assert code == int(ExitCode.OK), text
    with jobs.open_store() as store:
        (job,) = jobs.list_jobs(store)
    lines = text.splitlines()
    assert f"  job: {job.job_id}, queued" in lines, text
    assert f"  drive it with: crate intake playlist favorites --job {job.job_id}" in lines, text
    assert "  items: 0 of 5 settled" in lines, text


def test_the_resolution_names_owned_offered_and_missing_and_the_next_command(
    cfg, library, monkeypatch
):
    """206 settled rows printed ``intake.playlist: ok`` and the counts were read from artifacts."""
    job_id, _ = queued_hearts(cfg, library, monkeypatch)

    code, text = drive_human(resume_argv(job_id))

    assert code == int(ExitCode.OK), text
    lines = text.splitlines()
    assert f"  job: {job_id}, succeeded" in lines, text
    assert "  owned: 2 already in the library" in lines, text
    assert (
        "  offered: 1 held in another version, offered for review; see: crate review list"
        in lines
    ), text
    assert "  missing: 2 not in the library" in lines, text
    assert "  suppressed: 0 deleted on purpose" in lines, text
    assert f"  next: crate intake missing --job {job_id}" in lines, text
    assert not any(line.startswith("  drive it with:") for line in lines), text


def test_each_resolution_count_is_followed_by_its_reasons(cfg, library, monkeypatch):
    """R-682: sittings 8 and 10 read the reasons off the artifacts because nothing
    printed them. Each count's reasons sit on the line under it, and a state no
    row reached prints none."""
    job_id, _ = queued_hearts(cfg, library, monkeypatch)

    code, text = drive_human(resume_argv(job_id))

    assert code == int(ExitCode.OK), text
    lines = text.splitlines()
    owned_at = lines.index("  owned: 2 already in the library")
    assert lines[owned_at + 1] == "    by reason: exact 2", text
    offered_at = lines.index(
        "  offered: 1 held in another version, offered for review; see: crate review list"
    )
    assert lines[offered_at + 1] == "    by reason: version-differs 1", text
    missing_at = lines.index("  missing: 2 not in the library")
    assert lines[missing_at + 1] == "    by reason: not-in-library 2", text
    suppressed_at = lines.index("  suppressed: 0 deleted on purpose")
    assert lines[suppressed_at + 1] == f"  next: crate intake missing --job {job_id}", text
    assert sum(line.startswith("    by reason:") for line in lines) == 3, text


def test_the_reasons_are_read_back_from_the_reports_on_every_resume(cfg, library, monkeypatch):
    """A second resume over a finished job counts the same reasons, because they are
    read from the committed artifacts rather than kept by the process that ran them."""
    job_id, _ = queued_hearts(cfg, library, monkeypatch)
    code, first = drive(resume_argv(job_id))
    assert code == int(ExitCode.OK), first

    code, again = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), again
    reasons = again["data"]["progress"]["by_reason"]
    assert reasons == first["data"]["progress"]["by_reason"]
    assert reasons == {
        "owned": {"exact": 2},
        "offered": {"version-differs": 1},
        "missing": {"not-in-library": 2},
        "suppressed": {},
    }


def test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason(cfg, monkeypatch):
    """Reports no worker writes today, read the way ``_summary`` reads any: a missing
    ``why`` is not given one, and a state word the counts do not know is not counted
    under any state, reason or no reason."""
    reports = [
        {"state": "owned", "why": "exact"},
        {"state": "owned", "why": "isrc-exact"},
        {"state": "owned"},
        {"state": "owned", "why": ""},
        {"state": "owned", "why": 3},
        {"state": "misplaced", "why": "exact"},
    ]
    monkeypatch.setattr(intake_cli.artifacts, "committed", lambda *args: reports)

    class Job:
        job_id = "j-1"
        payload: dict = {}

    summary = intake_cli._summary(cfg, Job())

    assert summary["owned"] == 5
    assert summary["reported"] == 6
    assert summary["by_reason"] == {
        "owned": {"exact": 1, "isrc-exact": 1},
        "offered": {},
        "missing": {},
        "suppressed": {},
    }


def test_a_resolution_with_nothing_missing_names_no_next_command(cfg, library, monkeypatch):
    bind_playlist(monkeypatch, "pl-1", [Track("101", "Aurora Bloom", "Sun Path")])
    owned(library, "Aurora Bloom - Sun Path.flac")
    code, envelope = drive(["intake", "playlist", "pl-1"])
    job_id = envelope["data"]["job_id"]

    code, text = drive_human(resume_argv(job_id))

    assert code == int(ExitCode.OK), text
    lines = text.splitlines()
    assert "  owned: 1 already in the library" in lines, text
    assert "  missing: 0 not in the library" in lines, text
    assert not any(line.startswith("  next:") for line in lines), text


def test_an_empty_playlist_names_no_job_because_none_was_queued(cfg, monkeypatch):
    bind_playlist(monkeypatch, "pl-1", [])

    code, text = drive_human(["intake", "playlist", "pl-1"])

    assert code == int(ExitCode.OK), text
    assert text.splitlines()[0] == "intake.playlist: no_op", text
    assert "  job:" not in text, text
    assert "drive it with" not in text, text


def test_json_mode_never_reaches_the_human_cases(cfg, library, monkeypatch):
    """Scenario 5: the json a consumer reads cannot have moved.

    Every new case is reached only from the human path. Each is replaced with a
    tripwire and the verb is driven in json mode, queue and resolution both; a
    json answer that consulted any of them fails here rather than differing.
    """
    from cratekit import cli
    from cratekit.cli import render

    def tripwire(*args, **kwargs):
        raise AssertionError("json mode reached a human renderer")

    monkeypatch.setattr(cli, "_drive_argv", tripwire)
    monkeypatch.setattr(render, "render_job_state", tripwire)
    monkeypatch.setattr(render, "render_import_proof", tripwire)
    job_id, _ = queued_hearts(cfg, library, monkeypatch)
    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert set(envelope["data"]) == {"job_id", "state", "cause", "progress"}


# ═══════════════════════════════════════════════════════════════════════════
# R-706: a set longer than one run is identified in parts and lands as one
# ═══════════════════════════════════════════════════════════════════════════


def test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said(
    cfg, library, recognised, monkeypatch
):
    """Three chunks under a run bound of two is two parts. One job, one item
    per track in set order, and the note says the split was the spend's and
    not the set's."""
    monkeypatch.setattr(acrcloud, "MAX_CALLS_PER_RUN", 2)
    three_tracks(recognised)
    path = recording(library)

    job_id, envelope = queued_set(path)

    assert envelope["data"]["progress"]["parts"] == 2
    assert envelope["data"]["progress"]["calls"] == 3
    assert len(recognised.requests) == 3
    assert [w["code"] for w in envelope["warnings"]] == [
        intake_cli.TRACKLIST_WRITTEN,
        intake_cli.IN_PARTS,
    ]
    note = envelope["warnings"][1]["message"]
    assert "2 even parts" in note and "3 chunk(s)" in note and "one batch" in note
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 1, "a split set queued more than one job"
    job = job_of(job_id)
    assert job.payload[intake_cli.PARTS] == 2
    frozen = job.payload[intake_cli.TRACKS]
    assert [said["title"] for said in frozen.values()] == ["Sun Path", "Tide", "Glass Hour"]
    assert [item.item_id for item in items_of(job_id)] == list(frozen), "item order is the set order"
    code, resumed = drive(resume_argv(job_id))
    assert resumed["data"]["progress"]["parts"] == 2, "the split was forgotten on resume"


def test_identify_only_says_the_same_parts_note(cfg, library, recognised, monkeypatch):
    monkeypatch.setattr(acrcloud, "MAX_CALLS_PER_RUN", 2)
    three_tracks(recognised)
    code, envelope = drive(["intake", "identify", str(recording(library))])
    assert code in (int(ExitCode.OK), int(ExitCode.PENDING_HUMAN)), envelope
    assert [w["code"] for w in envelope["warnings"]] == [
        intake_cli.TRACKLIST_WRITTEN,
        intake_cli.IN_PARTS,
    ]
    note = envelope["warnings"][1]["message"]
    assert "one list" in note and "batch" not in note, "identify lands nothing"
    assert [row["title"] for row in envelope["data"]["missing"]] == ["Sun Path", "Tide", "Glass Hour"]


def test_a_set_that_fits_one_run_carries_no_parts_note(cfg, library, recognised):
    three_tracks(recognised)
    job_id, envelope = queued_set(recording(library))
    assert [w["code"] for w in envelope["warnings"]] == [intake_cli.TRACKLIST_WRITTEN]
    assert envelope["data"]["progress"]["parts"] == 1
    assert job_of(job_id).payload[intake_cli.PARTS] == 1


def test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing(
    cfg, library, recognised, monkeypatch
):
    """Four chunks under a run bound of one is four parts, one over the
    ceiling of three, so it is refused as not one set before any call."""
    monkeypatch.setattr(acrcloud, "MAX_CALLS_PER_RUN", 1)
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: FakeCarver(100.0))
    three_tracks(recognised)

    code, envelope = drive(["intake", "set", str(recording(library))])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["reason"] == "intake-recognition-spend-bound"
    detail = envelope["cause"]["detail"]
    assert (detail["kind"], detail["parts"], detail["ceiling"], detail["planned"]) == (
        "per-run", acrcloud.MAX_PARTS, 3, 4
    )
    assert recognised.requests == []
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


# ---------------------------------------------------------------------------
# U120: the date a heart was made rides on the job's frozen row
# ---------------------------------------------------------------------------


def test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not(
    cfg, library, monkeypatch
):
    """The quarter a landed heart goes to is read from the job, never from the
    account again (U113's rule), so the listing records the account's date."""
    from datetime import datetime, timedelta, timezone

    hearts = five_hearts()
    hearts[0].user_date_added = datetime(2026, 10, 1, 3, 0, tzinfo=timezone.utc)
    # An older client spells it ``date_added``; a local moment is kept as UTC.
    hearts[1].date_added = datetime(2026, 9, 30, 22, 0, tzinfo=timezone(timedelta(hours=-5)))
    hearts[2].user_date_added = "not a date"
    bind_hearts(monkeypatch, hearts)
    owned(library, "Aurora Bloom - Sun Path.flac")
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert code == int(ExitCode.OK), envelope
    job_id = envelope["data"]["job_id"]

    frozen = job_of(job_id).payload[intake_cli.TRACKS]
    assert frozen["201"][intake_cli.HEARTED] == "2026-10-01T03:00:00+00:00"
    assert frozen["202"][intake_cli.HEARTED] == "2026-10-01T03:00:00+00:00"
    # THE KEY IS ON EVERY ROW, None for a heart the account dates nowhere, so
    # a row with no key at all is one an older build froze.
    assert frozen["203"][intake_cli.HEARTED] is None
    assert frozen["204"][intake_cli.HEARTED] is None
    # The worker thaws the row as before and its report carries the date along.
    drive(resume_argv(job_id))
    found = by_title(cfg, job_id)
    assert found["Sun Path"]["track"][intake_cli.HEARTED] == "2026-10-01T03:00:00+00:00"
    assert found["Salt Road"]["track"][intake_cli.HEARTED] is None
    assert intake_cli.thawed(frozen["201"]).ref == "201"


def test_a_playlist_job_freezes_no_date_even_when_the_rows_carry_one(cfg, library, monkeypatch):
    from datetime import datetime, timezone

    rows = [Track("301", "Someone", "Something")]
    rows[0].user_date_added = datetime(2026, 10, 1, tzinfo=timezone.utc)
    bind_playlist(monkeypatch, "pl-1", rows)
    code, envelope = drive(["intake", "playlist", "pl-1"])
    assert code == int(ExitCode.OK), envelope
    frozen = job_of(envelope["data"]["job_id"]).payload[intake_cli.TRACKS]
    assert intake_cli.HEARTED not in frozen["301"]
