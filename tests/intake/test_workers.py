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

import json
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import handlers
from cratekit.cli import jobs as cli_jobs
from cratekit.core import artifacts, config, jobs, review, secrets
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import acrcloud, recognize
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from tests.cli_drive import drive
from tests.intake.test_recognition import FakeCarver, FakeTransport, hit, miss
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist, catalogue_factory
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
    assert "Aurora Bloom - Sun Path" in job.payload[intake_cli.TRACKLIST]
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
    assert envelope["data"]["progress"]["source"] == str(path.absolute())
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == (), "a set with nothing identified must queue nothing"


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


def test_a_mix_url_is_refused_at_the_queue_before_the_gate_or_any_spend(cfg, recognised):
    three_tracks(recognised)
    code, envelope = drive(["intake", "set", "https://example.invalid/mix"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "download the mix" in " ".join(envelope["cause"]["remediation"]["steps"])
    assert recognised.requests == []


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

    assert envelope["data"]["state"] == "failed", envelope
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
    intake_cli._RESOLVED.clear()

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
        "origin": match.TIDAL, "ref": "102", "spelled": "Tide",
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


def test_an_unbound_catalogue_refuses_honestly_and_queues_nothing(cfg):
    assert catalogue.bound() is False
    code, envelope = drive(["intake", "playlist", "pl-1"])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] in {"credential-missing", "label-catalogue-unbound"}
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
