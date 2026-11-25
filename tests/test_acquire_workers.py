"""U54: the acquisition worker, driven through the queue against a fake adapter.

The shell reads the list and queues its tracks as items, the worker constructs the adapter
through the registry's ``build`` and drives ``download.acquire_paced``, and every answer
lands on the item's row under its own slug (R-203, R-204). Every network touch goes through
``tests.acquire_fakes``; the vendored tool is never exercised here. The sleep is recorded,
never taken: an autouse fixture sits in front of the paced pool's delay, and the KTD9 test
reads the recorder.
"""

from __future__ import annotations

import json
import shlex
from pathlib import Path

import pytest

from cratekit import acquire
from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import download
from cratekit.acquire.adapter import (
    AdapterAuthFailed,
    AdapterBroken,
    AdapterSettings,
    InvocationOutcome,
    InvocationResult,
    LosslessPolicy,
    TrackOutcome,
    TrackResult,
)
from cratekit.cli import handlers, registry
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from tests.acquire_fakes import (
    FAKE_ADAPTER,
    FAKE_DECLARATION,
    FakeAdapter,
    Landing,
    Script,
    text_list,
    tidal_list,
)
from tests.cli_drive import drive, drive_human
from tests.test_config import valid_data


def _configure(library: Path, **acquisition) -> config.Config:
    settings = {"adapter": FAKE_ADAPTER, "pacing_delay_s": 0.0}
    settings.update(acquisition)
    built = config.from_dict(valid_data(library, profile={"name": "full"}, acquisition=settings))
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
    """A configured machine naming the fake adapter, pacing off: what a job freezes."""
    return _configure(library)


@pytest.fixture
def script(monkeypatch) -> Script:
    """The fake, registered for this test only, with a fresh script."""
    fresh = Script()
    monkeypatch.setitem(acquire.ADAPTERS, FAKE_ADAPTER, FAKE_DECLARATION)
    monkeypatch.setattr(FakeAdapter, "script", fresh)
    return fresh


@pytest.fixture(autouse=True)
def slept(monkeypatch) -> list[float]:
    """Every delay the worker's pool asked to sleep, recorded and not taken."""
    seen: list[float] = []
    monkeypatch.setattr(acquire_cli, "_SLEEP", seen.append)
    return seen


def listed(library: Path, rows: list[tuple[str, str, str]], name: str = "list.json") -> Path:
    path = library / name
    path.write_text(tidal_list(rows))
    return path


def queued(path: Path) -> str:
    code, envelope = drive(["acquire", "download", str(path)])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"]


def resume_argv(job_id: str) -> list[str]:
    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def items_of(job_id: str) -> tuple[jobs.Item, ...]:
    with jobs.open_store() as store:
        return jobs.items(store, job_id)


def states(job_id: str) -> dict[str, jobs.ItemState]:
    return {item.item_id: item.state for item in items_of(job_id)}


def causes(job_id: str) -> dict[str, str]:
    return {item.item_id: item.cause.reason for item in items_of(job_id) if item.cause}


def job_of(job_id: str) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.get(store, job_id)


def landings(*keys: str, **fields) -> dict[str, Landing]:
    return {key: Landing(**fields) for key in keys}


#: Five rows of a provider list, sliced to the length a test needs.
ROWS = [("1", "A", "T"), ("2", "B", "U"), ("3", "C", "V"), ("4", "D", "W"), ("5", "E", "X")]


def driven(library: Path, rows=ROWS[:1]) -> tuple[str, int, dict]:
    """Queue ``rows`` as a list and drive its job once through the resume path."""
    job_id = queued(listed(library, list(rows)))
    code, envelope = drive(resume_argv(job_id))
    return job_id, code, envelope


def refused_as_unusable(code: int, envelope: dict) -> None:
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"


def drives_with(job_id: str, *named: str) -> None:
    """``--job`` beside the list spelled ``named`` drives the job's one track to done."""
    code, envelope = drive(["acquire", "download", *named, "--job", job_id])
    assert code == int(ExitCode.OK), envelope
    assert states(job_id) == {"1": jobs.ItemState.DONE}


def nothing_queued() -> None:
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()



def test_the_download_key_resolves_to_this_worker():
    assert handlers.resolve("acquire.download") is acquire_cli.handle
    assert "acquire.download" not in handlers.HANDLERS_NOT_YET_BOUND


def test_the_worker_constructs_the_adapter_through_the_registry(cfg, script, library):
    """R-204's obligation, discharged: ``build`` has a caller, and it is here."""
    script.landings = landings("1")
    driven(library)

    assert len(script.constructed) == 1
    built = script.constructed[0]
    assert isinstance(built, AdapterSettings)
    assert built.lossless_policy is LosslessPolicy.STRICT



def test_queueing_a_list_gives_the_driver_one_item_per_track(cfg, library):
    job_id = queued(listed(library, [("10", "A", "T1"), ("20", "B", "T2")]))
    assert [item.item_id for item in items_of(job_id)] == ["10", "20"]
    assert set(states(job_id).values()) == {jobs.ItemState.PENDING}


def test_a_list_with_no_tracks_queues_nothing_and_says_so(cfg, library):
    """Zero items is impossible: an explicitly empty document is a no-op."""
    empty = library / "empty.json"
    empty.write_text(json.dumps({"list": 1, "origin": "tidal", "tracks": []}))
    code, envelope = drive(["acquire", "download", str(empty)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"] == {"job_id": "", "state": "no-tracks", "cause": None, "progress": {}}
    nothing_queued()


def test_every_queued_download_job_has_as_many_items_as_the_list_has_tracks(cfg, library):
    """Stated as a property over what was queued, not over one example."""
    for rows in ([("1", "A", "T")], ROWS[:3]):
        job_id = queued(listed(library, rows, name=f"l{len(rows)}.json"))
        assert len(items_of(job_id)) == len(rows)


def test_a_pasted_tracklist_is_refused_at_the_queue_rather_than_queued_unacquirable(cfg, library):
    """No provider identifier, no request the adapter contract can make."""
    pasted = library / "pasted.txt"
    pasted.write_text(text_list(["Artist - Title", "Other - Song"]))
    code, envelope = drive(["acquire", "download", str(pasted)])
    refused_as_unusable(code, envelope)
    assert "text list" in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["origin"] == "text"
    nothing_queued()


def test_a_provider_row_without_an_identifier_is_refused_by_position(cfg, library):
    rows = [("1", "A", "T"), ("", "B", "U"), ("3", "C", "V"), ("", "D", "W")]
    code, envelope = drive(["acquire", "download", str(listed(library, rows))])
    refused_as_unusable(code, envelope)
    assert envelope["cause"]["detail"]["positions"] == [2, 4]
    nothing_queued()


def test_a_repeated_identifier_is_one_item(cfg, library):
    """A playlist holding one track twice asks for one file; the queue keys items by
    identifier, so the repeat is folded."""
    job_id = queued(listed(library, [("7", "A", "T"), ("8", "B", "U"), ("7", "A", "T")]))
    assert [item.item_id for item in items_of(job_id)] == ["7", "8"]


def test_the_list_path_is_frozen_absolute(cfg, library, monkeypatch):
    monkeypatch.chdir(library)
    listed(library, [("1", "A", "T")])
    job_id = queued(Path("list.json"))
    assert job_of(job_id).payload[acquire_cli.LIST] == str(library / "list.json")


def test_what_the_list_said_is_frozen_with_the_job(cfg, script, library):
    """KTD9 for the list: a list edited after queueing does not change a queued item,
    since the worker builds its request from the payload."""
    script.landings = landings("1")
    path = listed(library, [("1", "Frozen Artist", "Frozen Title")])
    job_id = queued(path)
    path.write_text(tidal_list([("1", "Edited", "Edited")]))

    drive(resume_argv(job_id))

    assert [(r.artist, r.title) for r in script.fetched] == [("Frozen Artist", "Frozen Title")]



def test_a_download_job_runs_pending_to_done_through_the_resume_path(cfg, script, library):
    """The whole point of the unit. Read from the store, not from the exit code."""
    script.landings = landings("1", "2")
    job_id, code, envelope = driven(library, ROWS[:2])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    assert states(job_id) == {"1": jobs.ItemState.DONE, "2": jobs.ItemState.DONE}
    staging = Path(cfg.paths.download_staging)
    for item in items_of(job_id):
        assert item.artifact == str(staging / f"{item.item_id}.wav")
        assert Path(item.artifact).is_file()
    assert job_of(job_id).state is jobs.JobState.SUCCEEDED


def test_the_landing_is_staged_per_item_and_committed_rather_than_written_in_place(
    cfg, script, library
):
    script.landings = landings("1")
    job_id = queued(listed(library, [("1", "A", "T")]))
    staging = Path(cfg.paths.download_staging)

    drive(resume_argv(job_id))

    per_item = staging / acquire_cli.ACQUIRE_STAGING_DIRNAME / job_id / "0"
    assert per_item.is_dir(), "the adapter was not pointed at a per item staging directory"
    assert not (per_item / "1.wav").exists(), "the landing was copied rather than moved"
    assert (staging / "1.wav").is_file()
    # The adapter was handed the STAGING directory, not the configured root.
    assert script.constructed[0].download_staging == per_item


def test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt(cfg, script, library):
    """The tool skips rather than overwrites, reporting the path already there as a
    success, so a half download would pass as the track; the clear is a guard."""
    script.landings = landings("1", skips_when_present=True)
    job_id = queued(listed(library, [("1", "A", "T")]))
    stale = Path(cfg.paths.download_staging) / acquire_cli.ACQUIRE_STAGING_DIRNAME / job_id / "0"
    stale.mkdir(parents=True)
    (stale / "1.wav").write_bytes(b"half a download")

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert states(job_id) == {"1": jobs.ItemState.DONE}
    assert (Path(cfg.paths.download_staging) / "1.wav").read_bytes() != b"half a download"


# The staging sweep, R-291


def staging_tree(cfg: config.Config) -> Path:
    return Path(cfg.paths.download_staging) / acquire_cli.ACQUIRE_STAGING_DIRNAME


def test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run(cfg, script, library):
    """R-291's cost: one directory per item of every job, kept for good. The sweep is at
    the HEAD of the verb, so the first job's tree is still there when that job returns."""
    script.landings = landings("1", "2")
    first = queued(listed(library, ROWS[:2]))
    drive(resume_argv(first))
    assert job_of(first).state is jobs.JobState.SUCCEEDED
    assert sorted(path.name for path in (staging_tree(cfg) / first).iterdir()) == ["0", "1"]

    queued(listed(library, [("3", "C", "V")], name="second.json"))

    assert not (staging_tree(cfg) / first).exists(), (
        "the finished job's emptied staging directories were never reclaimed"
    )


def test_an_open_jobs_staging_survives_the_sweep(cfg, script, library):
    """Nothing moves out of a terminal job; everything may still move out of this one,
    whose item is PENDING and may be being worked right now."""
    script.landings = landings("1")
    open_job = queued(listed(library, [("1", "A", "T")]))
    held = staging_tree(cfg) / open_job / "0"
    held.mkdir(parents=True)

    queued(listed(library, [("2", "B", "U")], name="second.json"))

    assert job_of(open_job).state is jobs.JobState.QUEUED
    assert held.is_dir(), "an open job's staging was swept"


def test_the_refused_landing_left_as_evidence_survives_the_sweep(cfg, script, library):
    """A landing ``checked_landing`` refused stays as evidence for diagnosing the next
    demotion, so the sweep removes only empties: keyed on the filesystem refusing a
    non empty directory, not on the terminal job state (U169)."""
    script.landings = landings("1", kind="lossy", offer_lossless=True)
    failed = queued(listed(library, [("1", "A", "T")]))
    drive(resume_argv(failed))
    evidence = staging_tree(cfg) / failed / "0" / "1.mp3"
    assert evidence.is_file(), "the fixture did not leave a refused landing"
    assert job_of(failed).state in jobs.TERMINAL_STATES

    queued(listed(library, [("2", "B", "U")], name="second.json"))

    assert evidence.is_file(), "the refused landing kept as evidence was swept"
    assert (staging_tree(cfg) / failed).is_dir()


def test_a_directory_naming_a_job_this_queue_does_not_hold_is_left_alone(cfg, script, library):
    """No code path deletes a job row, so an unresolvable name is another store's: removing
    it as "the job is gone" is the one mistake here that would cost somebody a file."""
    stranger = staging_tree(cfg) / "job-from-somewhere-else" / "0"
    stranger.mkdir(parents=True)

    queued(listed(library, [("1", "A", "T")]))

    assert stranger.is_dir(), "a staging directory of an unknown job was swept"


def test_the_sweep_reports_what_it_removed_deepest_first(cfg, script, library):
    """The return value is asserted where it is made: removing the job directory before
    its items would leave the items behind on every run."""
    script.landings = landings("1")
    done = queued(listed(library, [("1", "A", "T")]))
    drive(resume_argv(done))

    with jobs.open_store() as store:
        removed = acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store)

    assert removed == (staging_tree(cfg) / done / "0", staging_tree(cfg) / done)


def test_a_staging_root_that_was_never_created_sweeps_to_nothing(cfg):
    """The verb runs on a machine that has never acquired anything."""
    with jobs.open_store() as store:
        assert acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store) == ()


def test_a_job_directory_that_cannot_be_LISTED_does_not_fail_the_verb(cfg, script, library):
    """``_children`` swallows ``OSError``, so an unreadable staging directory (mode
    ``0o111``) is no ``PermissionError``, and is left as not shown empty."""
    script.landings = landings("1")
    done = queued(listed(library, [("1", "A", "T")]))
    drive(resume_argv(done))
    blind = staging_tree(cfg) / done
    blind.chmod(0o111)
    try:
        with pytest.raises(OSError):
            list(blind.iterdir())

        second = listed(library, [("2", "B", "U")], name="second.json")
        code, envelope = drive(["acquire", "download", str(second)])
    finally:
        blind.chmod(0o700)

    assert code == int(ExitCode.OK), envelope
    assert blind.is_dir(), "an unlistable directory was removed on a guess"


def test_the_sweep_does_not_report_a_directory_it_could_not_remove(cfg, script, library):
    """The return value records removals, so a failure must not enter it; the refused
    landing holds evidence on purpose and is never removed."""
    script.landings = landings("1", kind="lossy", offer_lossless=True)
    failed = queued(listed(library, [("1", "A", "T")]))
    drive(resume_argv(failed))
    kept = staging_tree(cfg) / failed / "0"
    assert (kept / "1.mp3").is_file(), "the fixture did not leave a refused landing"

    with jobs.open_store() as store:
        removed = acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store)

    assert removed == ()
    assert kept.is_dir()



def test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing(
    cfg, script, library
):
    """The item's cause is asserted, not the exit code. A defect is permanent (R-348) and
    no longer re-armed (R-390), so the second half measures what the refusal leaves alone."""
    script.landings = landings("1", "2", "3")
    script.landings["2"].fetch_raises = AdapterBroken(
        "the tool crashed mid transfer", remedy=acquire.Remedy.SWITCH_ADAPTER
    )
    job_id, code, envelope = driven(library, ROWS[:3])

    # A partial failure is REFUSED, not reported (R-225): the successes are durable, the
    # job is recorded failed, and the verb leaves through the job's cause, non zero.
    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "failed", envelope
    assert states(job_id) == {
        "1": jobs.ItemState.DONE, "2": jobs.ItemState.FAILED, "3": jobs.ItemState.DONE,
    }
    assert causes(job_id) == {"2": "adapter-broken"}
    failed = next(i for i in items_of(job_id) if i.item_id == "2")
    assert "crashed mid transfer" in failed.cause.message
    assert "streamrip" in failed.cause.message, "the replacement path was not named"
    assert failed.cause.remediation.remedy == Remedy.SWITCH_ADAPTER
    assert job_of(job_id).state is jobs.JobState.FAILED

    # The resume is refused (R-390): ``adapter-broken`` is permanent (R-348), so
    # nothing is re-armed or fetched again; a switched adapter needs a fresh job.
    script.landings["2"].fetch_raises = None
    fetched_before = len(script.fetched)
    with jobs.open_store() as store:
        with pytest.raises(CratekitError) as excinfo:
            jobs.retry(store, job_id)
    assert excinfo.value.cause.reason == "job-not-retryable"
    assert excinfo.value.cause.inner is not None
    assert excinfo.value.cause.inner.reason == "adapter-broken"
    code, envelope = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "adapter-broken"
    assert states(job_id) == {
        "1": jobs.ItemState.DONE, "2": jobs.ItemState.FAILED, "3": jobs.ItemState.DONE,
    }
    assert script.fetched[fetched_before:] == []


def test_an_authentication_failure_parks_the_run_and_names_the_replacement_path(
    cfg, script, library
):
    """AE9 through the queue: the session is dead, and the row says where to go. The job
    is PARKED, not failed per item, since failing the item lets the driver claim the next
    one and log in again; the remaining tracks stay pending."""
    script.landings = landings("1", "2", "3")
    script.authenticate_raises = AdapterAuthFailed("the provider rejected the stored session")
    job_id, code, envelope = driven(library, ROWS[:3])

    # BLOCKED, not an OK exit (R-290): the block is not legible only inside ``data.cause``.
    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "blocked", envelope
    assert job_of(job_id).state is jobs.JobState.BLOCKED
    cause = envelope["cause"]
    assert cause["reason"] == "auth-failed"
    assert cause["remediation"]["remedy"] == Remedy.REAUTHENTICATE_PROVIDER
    assert "streamrip" in cause["message"]
    assert states(job_id) == {
        "1": jobs.ItemState.PENDING, "2": jobs.ItemState.PENDING, "3": jobs.ItemState.PENDING,
    }
    assert script.fetched == [], "a fetch was attempted with a dead session"


def test_a_dead_session_logs_in_once_and_not_once_per_track(cfg, script, library):
    """The measured cost of failing the item instead: a login per remaining track."""
    script.landings = landings("1", "2", "3", "4", "5")
    script.authenticate_raises = AdapterAuthFailed("the provider rejected the stored session")
    driven(library, ROWS)

    assert len(script.constructed) == 1, "the adapter was rebuilt for a track after the refusal"


def test_a_broken_adapter_fails_the_item_and_does_not_park_the_run(cfg, script, library):
    """A dead CREDENTIAL stops the run; a broken TOOL fails only the track it broke on."""
    script.landings = landings("1", "2")
    script.authenticate_raises = AdapterBroken("the vendored tool is not installed")
    job_id = driven(library, ROWS[:2])[0]

    assert job_of(job_id).state is not jobs.JobState.BLOCKED
    assert causes(job_id)["1"] == "adapter-broken"
    assert states(job_id) == {"1": jobs.ItemState.FAILED, "2": jobs.ItemState.FAILED}


def test_a_provider_block_parks_the_job_and_makes_no_further_request(cfg, script, library):
    """A forbidden response is about the CLIENT: the pool stops, the engine parks the job
    with the item released, and the third track is never asked for."""
    script.landings = landings("1", "2", "3")
    script.landings["2"].fetch_raises = RuntimeError("403 Forbidden: access denied")
    job_id, code, envelope = driven(library, ROWS[:3])

    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "blocked", envelope
    assert job_of(job_id).state is jobs.JobState.BLOCKED
    assert envelope["cause"]["reason"] == "provider-blocked"
    assert envelope["cause"]["retryable"] is False
    assert states(job_id) == {
        "1": jobs.ItemState.DONE, "2": jobs.ItemState.PENDING, "3": jobs.ItemState.PENDING,
    }
    assert [r.key for r in script.offered] == ["1", "2"], "a request followed the block"
    assert [r.key for r in script.fetched] == ["1", "2"]


def test_a_rate_limit_is_retried_under_backoff_and_then_lands(cfg, script, library):
    """A throttle is "slower", not "stop": the pool backs off, shaped by the frozen pacing."""
    script.landings = landings("1")
    script.landings["1"].fetch_raises = RuntimeError("429 too many requests")
    script.landings["1"].fetch_raises_times = 2
    job_id, code, envelope = driven(library)

    assert code == int(ExitCode.OK), envelope
    assert states(job_id) == {"1": jobs.ItemState.DONE}
    assert [r.key for r in script.fetched] == ["1", "1", "1"]


def test_a_rate_limit_that_never_clears_fails_the_item_as_transient(cfg, script, library, slept):
    script.landings = landings("1")
    script.landings["1"].fetch_raises = RuntimeError("429 too many requests")
    job_id, code, envelope = driven(library)

    assert code != int(ExitCode.OK)
    item = items_of(job_id)[0]
    assert item.cause is not None
    assert item.cause.reason == "unavailable-transient"
    assert item.cause.retryable is True
    assert len(script.fetched) == download.Pacing().max_attempts
    assert len(slept) >= download.Pacing().max_attempts - 1, "no backoff was waited"


def test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy(
    cfg, script, library
):
    script.landings = landings("1")
    script.landings["1"].offer_raises = LookupError("404 not found")
    job_id = driven(library)[0]

    item = items_of(job_id)[0]
    assert item.cause is not None
    assert item.cause.reason == "unavailable-permanent"
    assert item.cause.retryable is False
    # A track the provider no longer has is not the person's to fix, so the refusal must
    # never tell them to weaken the lossless policy.
    assert item.cause.remediation.remedy != Remedy.RELAX_LOSSLESS_POLICY
    assert item.cause.remediation.remedy is Remedy.CHANGE_POLICY_OR_INPUT
    assert script.fetched == []


def test_a_run_reporting_nothing_for_the_key_is_refused_rather_than_read_as_success(
    cfg, script, monkeypatch, tmp_path
):
    """Absence is not evidence. Driven at the handler with a run shaped by hand, since the
    pool fills every slot it does not stop on."""
    script.landings = landings("1")
    monkeypatch.setattr(
        download,
        "acquire_paced",
        lambda adapter, requests, **options: download.DownloadRun(
            invocation=InvocationResult(
                adapter=FAKE_ADAPTER, outcome=InvocationOutcome.OK, requested=("1",)
            )
        ),
    )
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key="acquire.download", payload={}, cfg=cfg, item_ids=("1",)
        )
        item = jobs.items(store, job.job_id)[0]

    with pytest.raises(CratekitError) as caught:
        acquire_cli.handle(job, item, cfg)
    assert caught.value.cause.reason == "unavailable-transient"
    assert "without reporting" in caught.value.cause.message



def test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named(
    cfg, script, library
):
    """The offer says lossless and the file is not: the check is at the FILE, and the
    refused file is left where it landed."""
    script.landings = landings("1", kind="lossy", offer_lossless=True)
    job_id, code, envelope = driven(library)

    # U169: refused for good by the policy is SETTLED, skipped with the cause it was refused under.
    assert code == int(ExitCode.OK), envelope
    item = items_of(job_id)[0]
    assert item.state is jobs.ItemState.SKIPPED
    assert item.cause is not None
    assert item.cause.reason == "lossy-refused"
    assert "MP3" in item.cause.message
    assert item.cause.remediation.remedy == Remedy.RELAX_LOSSLESS_POLICY
    staging = Path(cfg.paths.download_staging)
    assert not (staging / "1.mp3").exists(), "a refused landing was committed"
    evidence = staging / acquire_cli.ACQUIRE_STAGING_DIRNAME / job_id / "0" / "1.mp3"
    assert evidence.is_file(), "the refused file was not left as evidence"


# U169: a list whose only failures are policy refusals ends ok


FOUR = [("1", "Aurora Bloom", "Sun Path"), ("2", "B", "U"), ("3", "C", "V"), ("4", "D", "W")]


def test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it(
    cfg, script, library
):
    """Sitting 47: 116 of 117 landed, the last was lossy only, and the verb said failed."""
    script.landings = landings("2", "3", "4")
    script.landings["1"] = Landing(kind="lossy", offer_lossless=False)
    job_id, code, envelope = driven(library, FOUR)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert job_of(job_id).state is jobs.JobState.SUCCEEDED
    assert states(job_id) == {
        "1": jobs.ItemState.SKIPPED, "2": jobs.ItemState.DONE, "3": jobs.ItemState.DONE,
        "4": jobs.ItemState.DONE,
    }
    (warning,) = [w for w in envelope["warnings"] if w["code"] == acquire_cli.DECLINED_WARNING]
    assert warning["message"].startswith("Sun Path by Aurora Bloom (1) was not acquired")
    assert "lossy-refused" in warning["message"]


def test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again(cfg, script, library):
    script.landings = landings("2", "3", "4")
    script.landings["1"] = Landing(kind="lossy", offer_lossless=False)
    job_id = queued(listed(library, FOUR))
    _code, first = drive(resume_argv(job_id))

    code, again = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), again
    named = [w for w in again["warnings"] if w["code"] == acquire_cli.DECLINED_WARNING]
    assert named == [w for w in first["warnings"] if w["code"] == acquire_cli.DECLINED_WARNING]
    assert len(named) == 1


def test_the_human_output_says_ok_and_names_the_refused_track(cfg, script, library):
    script.landings = landings("2", "3", "4")
    script.landings["1"] = Landing(kind="lossy", offer_lossless=False)
    job_id = queued(listed(library, FOUR))

    code, text = drive_human(resume_argv(job_id))

    assert code == int(ExitCode.OK), text
    assert text.splitlines()[0] == "acquire.download: ok", text
    assert f"  job: {job_id}, succeeded" in text.splitlines(), text
    assert any(
        line.startswith("warning [acquire-refused]: Sun Path by Aurora Bloom") for line in text.splitlines()
    ), text


def test_three_landed_and_one_network_failure_still_fails(cfg, script, library):
    script.landings = landings("1", "2", "3", "4")
    script.landings["1"].fetch_raises = RuntimeError("connection reset by peer")
    job_id, code, envelope = driven(library, FOUR)

    assert code != int(ExitCode.OK), envelope
    assert job_of(job_id).state is jobs.JobState.FAILED
    assert states(job_id)["1"] is jobs.ItemState.FAILED
    assert not [w for w in envelope["warnings"] if w["code"] == acquire_cli.DECLINED_WARNING]


def test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped(
    cfg, script, library
):
    script.landings = landings("2", "3", "4")
    script.landings["1"] = Landing(kind="lossy", offer_lossless=False)
    script.landings["2"].fetch_raises = RuntimeError("connection reset by peer")
    job_id, code, envelope = driven(library, FOUR)

    assert code != int(ExitCode.OK), envelope
    assert job_of(job_id).state is jobs.JobState.FAILED
    assert states(job_id)["1"] is jobs.ItemState.SKIPPED
    assert states(job_id)["2"] is jobs.ItemState.FAILED


def test_a_track_the_provider_no_longer_has_is_declined_as_well(cfg, script, library):
    """``unavailable-permanent`` is filed in the policy refusal's exit class; no resume
    brings a delisted track back."""
    script.landings = landings("1", "2")
    script.landings["1"].offer_raises = LookupError("404 not found")
    job_id, code, envelope = driven(library, ROWS[:2])

    assert code == int(ExitCode.OK), envelope
    assert causes(job_id) == {"1": "unavailable-permanent"}
    assert states(job_id)["1"] is jobs.ItemState.SKIPPED


def test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one(cfg, script, library):
    """Read at the function, because a job holding a failed item refuses before the verb
    returns its warnings, so no envelope can show the difference."""
    script.landings = landings("2", "3", "4")
    script.landings["1"] = Landing(kind="lossy", offer_lossless=False)
    script.landings["2"].fetch_raises = RuntimeError("connection reset by peer")
    job_id = queued(listed(library, FOUR))
    drive(resume_argv(job_id))

    with jobs.open_store() as store:
        found = acquire_cli.declined_warnings(store, jobs.get(store, job_id))

    assert [w["message"].split(" (")[0] for w in found] == ["Sun Path by Aurora Bloom"], found
    assert states(job_id)["2"] is jobs.ItemState.FAILED


def test_only_a_permanent_cause_in_the_policy_class_is_refused_for_good():
    from cratekit.core.cause import refuse

    assert acquire_cli.refused_for_good(refuse("lossy-refused", "x").cause)
    assert acquire_cli.refused_for_good(refuse("unavailable-permanent", "x").cause)
    assert not acquire_cli.refused_for_good(
        refuse("lossy-refused", "x", retryable=True).cause
    ), "a retryable refusal must stay a failure a resume can reach"
    assert not acquire_cli.refused_for_good(refuse("unavailable-transient", "x").cause)
    assert not acquire_cli.refused_for_good(refuse("output-exists", "x").cause)


def test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched(
    cfg, script, library
):
    script.landings = landings("1", kind="lossy", offer_lossless=False)
    job_id = driven(library)[0]

    assert causes(job_id) == {"1": "lossy-refused"}
    assert script.fetched == [], "a lossy offer was fetched under strict policy"


@pytest.mark.parametrize("offer_lossless", [False, True], ids=["lossy-offer", "lying-offer"])
def test_a_lossy_landing_under_the_permissive_policy_is_committed_marked(
    library, script, offer_lossless
):
    """R21: lossy is permitted only WITH the marker, and config owns its text. The lying
    offer is R21's forbidden state reached through the offer: ``requires_lossy_marker`` is
    derived from the OFFER and the landing's codec check is strict policy's only, so the
    marker is decided by the file instead."""
    cfg = _configure(library, lossless_policy="allow_lossy_marked")
    script.landings = landings("1", kind="lossy", offer_lossless=offer_lossless)
    job_id, code, envelope = driven(library)

    assert code == int(ExitCode.OK), envelope
    item = items_of(job_id)[0]
    assert item.state is jobs.ItemState.DONE
    marker = cfg.naming.lossy_marker
    assert item.artifact == str(Path(cfg.paths.download_staging) / f"1 {marker}.mp3")
    assert Path(item.artifact).name == f"1 {marker}.mp3"
    assert Path(item.artifact).is_file()


def test_a_lossless_landing_under_the_permissive_policy_is_not_marked(library, script):
    _configure(library, lossless_policy="allow_lossy_marked")
    script.landings = landings("1")
    job_id = driven(library)[0]

    item = items_of(job_id)[0]
    assert item.state is jobs.ItemState.DONE
    assert Path(item.artifact).name == "1.wav"


def test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked(tmp_path):
    """An unmarked lossy file is the single state the audit exists to find."""
    landed = tmp_path / "1.mp3"
    with pytest.raises(CratekitError) as caught:
        acquire_cli.marked_name(landed, "   ", required=True)
    assert caught.value.cause.reason == "lossy-refused"
    assert acquire_cli.marked_name(landed, "   ", required=False) == "1.mp3"
    assert acquire_cli.marked_name(landed, "[MP3]", required=True) == "1 [MP3].mp3"


def test_an_unreadable_landing_is_transient_and_not_a_policy_refusal(cfg, script, library):
    """A file nothing could parse is a truncated download; advising a relaxed policy
    would make the product accept it."""
    script.landings = landings("1", kind="unreadable")
    job_id = driven(library)[0]

    item = items_of(job_id)[0]
    assert item.cause is not None
    assert item.cause.reason == "unavailable-transient"
    assert item.cause.retryable is True
    assert item.cause.remediation.remedy == Remedy.RETRY_LATER


def test_the_permissive_policy_skips_the_codec_probe(tmp_path):
    """Under the permissive policy the marker is the rule, and the probe is strict's."""
    junk = tmp_path / "1.flac"
    junk.write_bytes(b"junk")
    assert (
        acquire_cli.checked_landing(junk, "1", policy=LosslessPolicy.ALLOW_LOSSY_MARKED) == junk
    )



def test_the_pacing_delay_comes_from_the_frozen_configuration_not_a_fresh_load(
    library, script, slept
):
    """KTD9 through the pool: a delay edited after queueing is not the delay waited. Every
    request waits once, jittered around the frozen nominal, and the drift reaches the person."""
    _configure(library, pacing_delay_s=2.0)
    script.landings = landings("1", "2")
    job_id = queued(listed(library, ROWS[:2]))
    _configure(library, pacing_delay_s=0.0)

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert len(slept) == 2, slept
    assert all(1.0 <= s <= 3.0 for s in slept), slept
    assert any(w["code"] == "config-drift" for w in envelope["warnings"]), envelope["warnings"]
    assert any("pacing_delay_s" in w["message"] for w in envelope["warnings"])


def test_a_delay_frozen_at_zero_waits_nothing_whatever_the_live_configuration_says(
    library, script, slept
):
    _configure(library, pacing_delay_s=0.0)
    script.landings = landings("1")
    job_id = queued(listed(library, [("1", "A", "T")]))
    _configure(library, pacing_delay_s=4.0)

    drive(resume_argv(job_id))

    assert slept == []


def test_the_frozen_policy_reaches_the_worker_not_the_live_one(library, script):
    """Frozen strict, then relaxed live: the lossy landing is still refused."""
    _configure(library, lossless_policy="strict")
    script.landings = landings("1", kind="lossy", offer_lossless=True)
    job_id = queued(listed(library, [("1", "A", "T")]))
    _configure(library, lossless_policy="allow_lossy_marked")

    drive(resume_argv(job_id))

    assert causes(job_id) == {"1": "lossy-refused"}



def test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it(cfg, script, library):
    script.landings = landings("1")
    kept = Path(cfg.paths.download_staging) / "1.wav"
    kept.parent.mkdir(parents=True, exist_ok=True)
    kept.write_bytes(b"a file somebody kept")
    job_id, code, envelope = driven(library)

    assert code != int(ExitCode.OK)
    assert causes(job_id) == {"1": "output-exists"}
    assert kept.read_bytes() == b"a file somebody kept"



def test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy(
    library, script
):
    """The vendored adapter, built by the worker with no provider session in the keychain:
    the session scope refuses before there is a source, and the item's row says to
    re-authorise. The fake is registered only so the registry has its per test shape."""
    _configure(library, adapter="vendored")
    job_id = driven(library)[0]

    # Asserts the pair: a dead credential parks the JOB with the track released, a broken
    # tool fails the ITEM, and an offline machine produces either by its keychain.
    job = job_of(job_id)
    item = items_of(job_id)[0]
    parked = job.state is jobs.JobState.BLOCKED
    cause = job.cause if parked else item.cause
    assert cause is not None
    assert cause.reason in {"auth-failed", "adapter-broken"}
    assert cause.remediation.remedy in {
        Remedy.REAUTHENTICATE_PROVIDER, Remedy.REPAIR_CREDENTIAL_STORE,
    }
    assert "streamrip" in cause.message
    assert (cause.reason == "auth-failed") is parked
    assert item.state is (jobs.ItemState.PENDING if parked else jobs.ItemState.FAILED)
    assert script.constructed == [], "the fake was constructed instead of the real adapter"


def test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name(library, script):
    """``load`` refuses an unknown name rather than defaulting; through the queue the
    refusal is the item's, not a traceback."""
    _configure(library, adapter="no-such-adapter")
    job_id, code, envelope = driven(library)

    assert code != int(ExitCode.OK)
    item = items_of(job_id)[0]
    assert item.cause is not None
    assert "no-such-adapter" in item.cause.message


def test_a_pasted_web_address_gets_the_readers_own_refusal(cfg, library):
    """``read_list`` refuses a URL by its leading scheme; absolutising the path first would
    mangle ``https://host/x`` into a relative path and give a file-not-found."""
    code, envelope = drive(["--output", "json", "acquire", "download", "https://tidal.com/p/1"])

    assert code != int(ExitCode.OK)
    assert "web address" in envelope["cause"]["message"]
    nothing_queued()


def test_an_open_job_with_no_items_refuses_rather_than_reporting_success(cfg, library):
    """A job queued before this unit has a frozen list path and no items; driving it would
    report every track acquired over a list nothing read (R-198). ``master`` needs no
    guard, as it always queues one item."""
    path = listed(library, [("1", "A", "T")])
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key="acquire.download", payload={acquire_cli.LIST: str(path)}, cfg=cfg,
        )

    code, envelope = drive(resume_argv(job.job_id))

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "internal-error"
    assert job_of(job.job_id).state is not jobs.JobState.SUCCEEDED


def test_the_registry_entry_still_declares_the_argv_builder_the_resume_uses(cfg, library):
    entry = registry.entry("acquire.download")
    job_id = queued(listed(library, [("1", "A", "T")]))
    argv = resume_argv(job_id)
    assert argv[:2] == ["acquire", "download"]
    assert argv[-2:] == ["--job", job_id]
    assert entry.argv_builder == "download_argv"


def test_a_track_result_that_is_acquired_is_the_only_one_committed():
    """The mapping is total over the outcome vocabulary, so a new outcome fails here, not
    as a KeyError on a row."""
    for outcome in TrackOutcome:
        if outcome is TrackOutcome.ACQUIRED:
            continue
        assert outcome in acquire_cli._ITEM_REASONS, outcome
    for outcome in InvocationOutcome:
        if outcome is InvocationOutcome.OK:
            continue
        assert outcome in acquire_cli._INVOCATION_REASONS, outcome
    assert TrackResult(key="k", outcome=TrackOutcome.UNAVAILABLE_TRANSIENT).outcome in (
        acquire_cli._ITEM_REASONS
    )


# R-678: the queueing half names the job it queued


def test_queueing_a_download_names_the_job_and_the_command_that_drives_it(cfg, library):
    """Sitting 9: ``ok`` in under a second, and the identifier nowhere a person reads."""
    path = listed(library, [("10", "A", "T1"), ("20", "B", "T2")])

    code, text = drive_human(["acquire", "download", str(path)])

    assert code == int(ExitCode.OK), text
    with jobs.open_store() as store:
        (job,) = jobs.list_jobs(store)
    lines = text.splitlines()
    assert f"  job: {job.job_id}, queued" in lines, text
    drives = shlex.join(["crate", "acquire", "download", "--job", job.job_id])
    assert f"  drive it with: {drives}" in lines, text
    assert "  items: 0 of 2 settled" in lines, text


# R-668: the resume needs the job and not the list


def test_the_job_alone_drives_the_queued_acquisition(cfg, script, library):
    """Sitting 7: ``--job`` alone was a usage error demanding the list. Typed out, not taken
    from ``resume_argv``, so it holds if the builder carries the list again."""
    script.landings = landings("1", "2")
    job_id = queued(listed(library, ROWS[:2]))

    code, envelope = drive(["acquire", "download", "--job", job_id])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    assert states(job_id) == {"1": jobs.ItemState.DONE, "2": jobs.ItemState.DONE}


def test_neither_a_list_nor_a_job_is_refused_by_the_verb_and_queues_nothing(cfg, library):
    """The verb now says this, naming both forms, not as a usage error it cannot produce."""
    code, envelope = drive(["acquire", "download"])

    refused_as_unusable(code, envelope)
    steps = " ".join(envelope["cause"]["remediation"]["steps"])
    assert "--job" in steps
    assert "list" in steps
    nothing_queued()


def test_the_frozen_list_named_beside_the_job_still_drives(cfg, script, library):
    """The form every build before R-668 required, so a saved command still works."""
    script.landings = landings("1")
    path = listed(library, [("1", "A", "T")])
    job_id = queued(path)

    drives_with(job_id, str(path))


def test_the_frozen_list_named_relative_from_where_it_was_queued_still_drives(
    cfg, script, library, monkeypatch
):
    """Compared after the freeze's own absolutising, so the same words agree."""
    monkeypatch.chdir(library)
    script.landings = landings("1")
    listed(library, [("1", "A", "T")])
    job_id = queued(Path("list.json"))

    drives_with(job_id, "list.json")


def test_a_different_list_named_beside_the_job_is_refused_and_nothing_is_fetched(
    cfg, script, library
):
    """Driving the job would report the named list acquired when another one was."""
    script.landings = landings("1")
    job_id = queued(listed(library, [("1", "A", "T")]))
    other = listed(library, [("9", "Z", "Q")], name="other.json")

    code, envelope = drive(["acquire", "download", str(other), "--job", job_id])

    refused_as_unusable(code, envelope)
    assert envelope["cause"]["detail"]["named"] == str(other)
    assert envelope["cause"]["detail"]["frozen"] == str(library / "list.json")
    assert f"--job {job_id} alone" in " ".join(envelope["cause"]["remediation"]["steps"])
    assert script.fetched == []
    assert states(job_id) == {"1": jobs.ItemState.PENDING}
    assert job_of(job_id).state is jobs.JobState.QUEUED


def test_the_frozen_list_spelled_through_a_symlink_still_drives(cfg, script, library, tmp_path):
    """Two spellings of one file are one list, as the filesystem answers (``/tmp`` against
    ``/private/tmp``)."""
    script.landings = landings("1")
    path = listed(library, [("1", "A", "T")])
    job_id = queued(path)
    alias = tmp_path / "alias"
    alias.symlink_to(library, target_is_directory=True)

    drives_with(job_id, str(alias / "list.json"))


def test_an_empty_job_identifier_is_refused_rather_than_queueing_the_list_again(cfg, library):
    """``--job ""`` read by truthiness fell through to the queueing path."""
    path = listed(library, [("1", "A", "T")])

    code, envelope = drive(["acquire", "download", str(path), "--job", ""])

    refused_as_unusable(code, envelope)
    assert "empty identifier" in envelope["cause"]["message"]
    nothing_queued()


def test_a_command_naming_nothing_is_refused_before_the_configuration_is_read(
    cfg, library, monkeypatch
):
    """Argparse refused it before anything ran, and so does the verb."""

    def boom(origin):
        raise AssertionError("the configuration was read for a command naming nothing")

    monkeypatch.setattr(acquire_cli, "load_config", boom)

    code, envelope = drive(["acquire", "download"])

    refused_as_unusable(code, envelope)


def test_a_refused_list_leaves_a_dead_drivers_claim_for_the_resume_to_reconcile(
    cfg, script, library, monkeypatch
):
    """Review round: the list is checked before ``reconcile`` touches the queue."""
    job_id = queued(listed(library, [("1", "A", "T")]))
    other = listed(library, [("9", "Z", "Q")], name="other.json")
    reconciled: list[str] = []
    monkeypatch.setattr(jobs, "reconcile", lambda store, jid: reconciled.append(jid))

    code, envelope = drive(["acquire", "download", str(other), "--job", job_id])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert reconciled == []


def test_another_verbs_job_is_not_read_as_a_frozen_download_list(tmp_path):
    """A payload under another handler may use the same key for another thing."""

    class Job:
        job_id = "j"
        handler_key = "some.other.verb"
        payload = {acquire_cli.LIST: str(tmp_path / "theirs.json")}

    acquire_cli._same_list_or_refuse(str(tmp_path / "mine.json"), Job(), "acquire.download")
    with pytest.raises(CratekitError) as refused:
        acquire_cli._same_list_or_refuse(str(tmp_path / "mine.json"), Job(), Job.handler_key)
    assert refused.value.cause.reason == "intake-list-unusable"


def test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives(
    cfg, script, library, monkeypatch
):
    """The job froze every track, so a list deleted since still resumes; the freeze's own
    absolutising makes the two spellings agree."""
    monkeypatch.chdir(library)
    script.landings = landings("1")
    path = listed(library, [("1", "A", "T")])
    job_id = queued(Path("list.json"))
    path.unlink()

    drives_with(job_id, "list.json")


def test_a_list_under_a_home_that_cannot_be_expanded_is_refused_by_name(cfg, library):
    """``expanduser`` raises for an unknown user; the resume answers with the list refusal."""
    job_id = queued(listed(library, [("1", "A", "T")]))

    code, envelope = drive(["acquire", "download", "~no-such-user-r668/list.json", "--job", job_id])

    refused_as_unusable(code, envelope)
    assert states(job_id) == {"1": jobs.ItemState.PENDING}


def test_a_download_job_whose_payload_froze_no_list_is_not_compared_with_one_named(tmp_path):
    """R-2071: no frozen list is nothing to disagree with, never the working directory."""

    class Job:
        job_id = "j"
        handler_key = "acquire.download"
        payload: dict = {}

    acquire_cli._same_list_or_refuse(str(tmp_path / "mine.json"), Job(), Job.handler_key)
