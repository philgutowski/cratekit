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
from tests.cli_drive import drive
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
    assert envelope["warnings"] == []
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
    assert [w["code"] for w in envelope["warnings"]] == ["recognition-incomplete"]
    assert "1 of 3" in envelope["warnings"][0]["message"]
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
    one = intake_cli.tracklist_name(tmp_path / "a" / "REC001.WAV", "")
    other = intake_cli.tracklist_name(tmp_path / "b" / "REC001.WAV", "")
    assert one != other
    assert one.startswith("REC001-") and one.endswith(intake_cli.TRACKLIST_SUFFIX)
    assert intake_cli.tracklist_name(tmp_path / "REC001.WAV", "ab" * 32) == (
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
