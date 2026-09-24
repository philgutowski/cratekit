"""U54: the acquisition worker, driven through the queue against a fake adapter.

``acquire.download`` queued and nothing ran it (R-203), and the adapter behind
it had never been constructed by anything in the product (R-204). This file is
the proof that both are over: the shell reads the list and queues its tracks as
items, the worker constructs the adapter through the registry's ``build`` and
drives ``download.acquire_paced``, and every answer that function can give lands
on the item's row under its own slug.

EVERY NETWORK TOUCH GOES THROUGH ``tests.acquire_fakes``. The fake is registered
under a name and the frozen configuration names it, so ``load`` and ``build``
run for real. The vendored tool is never exercised here; what remains unproven
without a live provider is stated in the unit's record.

THE SLEEP IS RECORDED, NEVER TAKEN. The paced pool waits before EVERY request,
including the first, through the delay the frozen configuration holds. An
autouse fixture puts a recorder in front of it so the suite does not spend six
jittered seconds per item, and the KTD9 test reads the recorder.
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

# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


def _configure(library: Path, **acquisition) -> config.Config:
    settings = {"adapter": FAKE_ADAPTER, "pacing_delay_s": 0.0}
    settings.update(acquisition)
    built = config.from_dict(
        valid_data(library, profile={"name": "full"}, acquisition=settings)
    )
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
    """A configured machine naming the fake adapter, pacing off. This is the
    configuration a job freezes."""
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


# ═══════════════════════════════════════════════════════════════════════════
# The binding
# ═══════════════════════════════════════════════════════════════════════════


def test_the_download_key_resolves_to_this_worker():
    assert handlers.resolve("acquire.download") is acquire_cli.handle
    assert "acquire.download" not in handlers.HANDLERS_NOT_YET_BOUND


def test_the_worker_constructs_the_adapter_through_the_registry(cfg, script, library):
    """R-204's obligation, discharged: ``build`` has a caller, and it is here."""
    script.landings = landings("1")
    job_id = queued(listed(library, [("1", "A", "T")]))

    drive(resume_argv(job_id))

    assert len(script.constructed) == 1
    built = script.constructed[0]
    assert isinstance(built, AdapterSettings)
    assert built.lossless_policy is LosslessPolicy.STRICT


# ═══════════════════════════════════════════════════════════════════════════
# Items: the tracks of the frozen list, and the zero item rule
# ═══════════════════════════════════════════════════════════════════════════


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
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_every_queued_download_job_has_as_many_items_as_the_list_has_tracks(cfg, library):
    """Stated as a property over what was queued, not over one example."""
    for rows in ([("1", "A", "T")], [("1", "A", "T"), ("2", "B", "U"), ("3", "C", "V")]):
        job_id = queued(listed(library, rows, name=f"l{len(rows)}.json"))
        assert len(items_of(job_id)) == len(rows)


def test_a_pasted_tracklist_is_refused_at_the_queue_rather_than_queued_unacquirable(
    cfg, library
):
    """No provider identifier, no request the adapter contract can make."""
    pasted = library / "pasted.txt"
    pasted.write_text(text_list(["Artist - Title", "Other - Song"]))
    code, envelope = drive(["acquire", "download", str(pasted)])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "text list" in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["origin"] == "text"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_provider_row_without_an_identifier_is_refused_by_position(cfg, library):
    rows = [("1", "A", "T"), ("", "B", "U"), ("3", "C", "V"), ("", "D", "W")]
    code, envelope = drive(["acquire", "download", str(listed(library, rows))])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert envelope["cause"]["detail"]["positions"] == [2, 4]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_repeated_identifier_is_one_item(cfg, library):
    """A playlist holding one track twice asks for one file, and the queue
    keys items by identifier, so the repeat is folded rather than inserted."""
    job_id = queued(listed(library, [("7", "A", "T"), ("8", "B", "U"), ("7", "A", "T")]))
    assert [item.item_id for item in items_of(job_id)] == ["7", "8"]


def test_the_list_path_is_frozen_absolute(cfg, library, monkeypatch):
    monkeypatch.chdir(library)
    listed(library, [("1", "A", "T")])
    job_id = queued(Path("list.json"))
    assert job_of(job_id).payload[acquire_cli.LIST] == str(library / "list.json")


def test_what_the_list_said_is_frozen_with_the_job(cfg, script, library):
    """KTD9 for the list: a list edited after queueing does not change what a
    queued item means. The worker builds its request from the payload."""
    script.landings = landings("1")
    path = listed(library, [("1", "Frozen Artist", "Frozen Title")])
    job_id = queued(path)
    path.write_text(tidal_list([("1", "Edited", "Edited")]))

    drive(resume_argv(job_id))

    assert [(r.artist, r.title) for r in script.fetched] == [("Frozen Artist", "Frozen Title")]


# ═══════════════════════════════════════════════════════════════════════════
# The happy path, through the real resume argv
# ═══════════════════════════════════════════════════════════════════════════


def test_a_download_job_runs_pending_to_done_through_the_resume_path(cfg, script, library):
    """The whole point of the unit. Read from the store, not from the exit code."""
    script.landings = landings("1", "2")
    job_id = queued(listed(library, [("1", "A", "T"), ("2", "B", "U")]))

    code, envelope = drive(resume_argv(job_id))

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


def test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt(
    cfg, script, library
):
    """THE TOOL SKIPS RATHER THAN OVERWRITES, which is what makes the clear a
    guard rather than a tidy up.

    Measured 2026-09-09: with a fake that always writes its landing, reverting
    the clear killed nothing in a suite of 6991, because the fresh write
    replaced the stale bytes on its own. The wrapped tool reports a skip as a
    successful call carrying the path already there, so the half download is
    what gets handed on as the track. The fake skips here for the same reason.
    """
    script.landings = landings("1", skips_when_present=True)
    job_id = queued(listed(library, [("1", "A", "T")]))
    stale = Path(cfg.paths.download_staging) / acquire_cli.ACQUIRE_STAGING_DIRNAME / job_id / "0"
    stale.mkdir(parents=True)
    (stale / "1.wav").write_bytes(b"half a download")

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert states(job_id) == {"1": jobs.ItemState.DONE}
    assert (Path(cfg.paths.download_staging) / "1.wav").read_bytes() != b"half a download"


# ═══════════════════════════════════════════════════════════════════════════
# The staging sweep, R-291
# ═══════════════════════════════════════════════════════════════════════════


def staging_tree(cfg: config.Config) -> Path:
    return Path(cfg.paths.download_staging) / acquire_cli.ACQUIRE_STAGING_DIRNAME


def test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run(
    cfg, script, library
):
    """R-291's cost. One directory per item of every job ever run, kept for good.

    The sweep is at the HEAD of the verb, so the tree the first job left is
    still there when that job returns and goes on the second invocation. That
    ordering is asserted on purpose rather than worked around: it is what lets
    a person look at the staging of the run that just finished.
    """
    script.landings = landings("1", "2")
    first = queued(listed(library, [("1", "A", "T"), ("2", "B", "U")]))
    drive(resume_argv(first))
    assert job_of(first).state is jobs.JobState.SUCCEEDED
    assert sorted(path.name for path in (staging_tree(cfg) / first).iterdir()) == ["0", "1"]

    queued(listed(library, [("3", "C", "V")], name="second.json"))

    assert not (staging_tree(cfg) / first).exists(), (
        "the finished job's emptied staging directories were never reclaimed"
    )


def test_an_open_jobs_staging_survives_the_sweep(cfg, script, library):
    """Nothing moves out of a terminal job. Everything may still move out of this one.

    The item is still PENDING, so a resume is entitled to redo it and a driver
    working it right now is writing into exactly this directory.
    """
    script.landings = landings("1")
    open_job = queued(listed(library, [("1", "A", "T")]))
    held = staging_tree(cfg) / open_job / "0"
    held.mkdir(parents=True)

    queued(listed(library, [("2", "B", "U")], name="second.json"))

    assert job_of(open_job).state is jobs.JobState.QUEUED
    assert held.is_dir(), "an open job's staging was swept"


def test_the_refused_landing_left_as_evidence_survives_the_sweep(cfg, script, library):
    """The deliberate half of R-291, and the reason the sweep removes only empties.

    A landing ``checked_landing`` refused stays where it fell because it is the
    evidence for diagnosing the next demotion. The job FAILS, which is terminal,
    so a sweep keyed on the job state alone would delete it. Keyed on the
    filesystem refusing to remove a directory with something in it, it cannot.
    """
    script.landings = landings("1", kind="lossy", offer_lossless=True)
    failed = queued(listed(library, [("1", "A", "T")]))
    drive(resume_argv(failed))
    evidence = staging_tree(cfg) / failed / "0" / "1.mp3"
    assert evidence.is_file(), "the fixture did not leave a refused landing"
    assert job_of(failed).state is jobs.JobState.FAILED

    queued(listed(library, [("2", "B", "U")], name="second.json"))

    assert evidence.is_file(), "the refused landing kept as evidence was swept"
    assert (staging_tree(cfg) / failed).is_dir()


def test_a_directory_naming_a_job_this_queue_does_not_hold_is_left_alone(
    cfg, script, library
):
    """No code path deletes a job row, so an unresolvable name is another store's.

    Removing it on the reading "the job is gone, so the work is over" is the one
    mistake in this sweep that would cost somebody a file, and an unresolvable
    identifier does not distinguish that reading from "this tree and this queue
    are not from the same installation".
    """
    stranger = staging_tree(cfg) / "job-from-somewhere-else" / "0"
    stranger.mkdir(parents=True)

    queued(listed(library, [("1", "A", "T")]))

    assert stranger.is_dir(), "a staging directory of an unknown job was swept"


def test_the_sweep_reports_what_it_removed_deepest_first(cfg, script, library):
    """The return value, which no caller reads today, asserted where it is made.

    A sweep that removed the job directory before its items would leave the
    items behind on every run, and the order is the only place that shows.
    """
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
    """``_children`` swallows ``OSError`` and nothing drove the swallow.

    Found by mutation: deleting the ``try``/``except`` and letting the error
    escape killed NOTHING across the whole suite, while the sweep runs at the
    head of a verb that has not started its real work yet. An unreadable
    directory under the staging tree must not turn ``acquire download`` into an
    unhandled ``PermissionError`` over housekeeping nobody asked for.

    Mode ``0o111`` is the shape that reaches it: the account may traverse the
    directory and may not list it, so ``is_dir`` still answers and ``iterdir``
    raises. The directory is left where it is, which is the honest outcome,
    because a sweep that could not see inside has not established that it is
    empty.
    """
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
    """The return value is a record of removals, so a failure must not enter it.

    Found by mutation: turning ``_reclaim``'s ``return`` into ``pass``, so every
    directory it touched was appended whether or not it went, killed nothing.
    The refused landing case is the reachable one: that directory holds evidence
    on purpose and will never be removed, and a caller reading this tuple as
    what is gone would be reading the opposite of the truth.
    """
    script.landings = landings("1", kind="lossy", offer_lossless=True)
    failed = queued(listed(library, [("1", "A", "T")]))
    drive(resume_argv(failed))
    kept = staging_tree(cfg) / failed / "0"
    assert (kept / "1.mp3").is_file(), "the fixture did not leave a refused landing"

    with jobs.open_store() as store:
        removed = acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store)

    assert removed == ()
    assert kept.is_dir()


# ═══════════════════════════════════════════════════════════════════════════
# Failure paths of the engine this unit is the first to call
# ═══════════════════════════════════════════════════════════════════════════


def test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing(
    cfg, script, library
):
    """The brief's scenario. The item's cause is asserted, not the exit code.

    Named for a resumable job until R-390: a defect is permanent (R-348) and a
    permanent failure is no longer re-armed, so the second half now measures
    what the refusal leaves alone.
    """
    script.landings = landings("1", "2", "3")
    script.landings["2"].fetch_raises = AdapterBroken(
        "the tool crashed mid transfer", remedy=acquire.Remedy.SWITCH_ADAPTER
    )
    job_id = queued(listed(library, [("1", "A", "T"), ("2", "B", "U"), ("3", "C", "V")]))

    code, envelope = drive(resume_argv(job_id))

    # A partial failure is REFUSED, not reported (R-225). The successes are
    # durable, the job is recorded failed, and the verb leaves through the job's
    # own cause with a non zero exit. Until R-225 closed here this asserted a
    # normal envelope whose ``data.state`` said failed beside an exit of 0.
    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "failed", envelope
    assert states(job_id) == {
        "1": jobs.ItemState.DONE,
        "2": jobs.ItemState.FAILED,
        "3": jobs.ItemState.DONE,
    }
    assert causes(job_id) == {"2": "adapter-broken"}
    failed = next(i for i in items_of(job_id) if i.item_id == "2")
    assert "crashed mid transfer" in failed.cause.message
    assert "streamrip" in failed.cause.message, "the replacement path was not named"
    assert failed.cause.remediation.remedy == Remedy.SWITCH_ADAPTER
    assert job_of(job_id).state is jobs.JobState.FAILED

    # THE RESUME IS REFUSED (R-390). ``adapter-broken`` is a defect in the
    # acquisition code and is recorded as permanent on purpose, R-348: a job
    # retrying it would have retried it for ever. ``jobs.retry`` reads that flag
    # before it re-arms anything, so the two landed tracks stay done, the broken
    # one stays failed, and a second ask fetches nothing. The person's path
    # after switching adapters is a fresh job, which the refusal's steps say.
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
        "1": jobs.ItemState.DONE,
        "2": jobs.ItemState.FAILED,
        "3": jobs.ItemState.DONE,
    }
    assert script.fetched[fetched_before:] == []


def test_an_authentication_failure_parks_the_run_and_names_the_replacement_path(
    cfg, script, library
):
    """AE9 through the queue: the session is dead, and the row says where to go.

    PARKED RATHER THAN FAILED PER ITEM. The worker builds an adapter and
    authenticates inside every item, so failing the item lets the driver claim
    the next one and log in again. The job stops on the first refusal with the
    cause the adapter gave, and every remaining track stays pending.
    """
    script.landings = landings("1", "2", "3")
    script.authenticate_raises = AdapterAuthFailed("the provider rejected the stored session")
    job_id = queued(listed(library, [("1", "A", "T"), ("2", "B", "U"), ("3", "C", "V")]))

    code, envelope = drive(resume_argv(job_id))

    # BLOCKED, and not an OK exit (R-290). This asserted ``ExitCode.OK`` with the
    # block legible only inside ``data.cause``, which is the entry's measured cost.
    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "blocked", envelope
    assert job_of(job_id).state is jobs.JobState.BLOCKED
    cause = envelope["cause"]
    assert cause["reason"] == "auth-failed"
    assert cause["remediation"]["remedy"] == Remedy.REAUTHENTICATE_PROVIDER
    assert "streamrip" in cause["message"]
    assert states(job_id) == {
        "1": jobs.ItemState.PENDING,
        "2": jobs.ItemState.PENDING,
        "3": jobs.ItemState.PENDING,
    }
    assert script.fetched == [], "a fetch was attempted with a dead session"


def test_a_dead_session_logs_in_once_and_not_once_per_track(cfg, script, library):
    """The measured cost of failing the item instead: one login per remaining
    track, into the account the lockout applies to."""
    script.landings = landings("1", "2", "3", "4", "5")
    script.authenticate_raises = AdapterAuthFailed("the provider rejected the stored session")
    job_id = queued(
        listed(
            library,
            [("1", "A", "T"), ("2", "B", "U"), ("3", "C", "V"), ("4", "D", "W"), ("5", "E", "X")],
        )
    )

    drive(resume_argv(job_id))

    assert len(script.constructed) == 1, "the adapter was rebuilt for a track after the refusal"


def test_a_broken_adapter_fails_the_item_and_does_not_park_the_run(cfg, script, library):
    """The asymmetry, asserted so it cannot be flattened by accident. A dead
    CREDENTIAL stops the run; a broken TOOL fails the track it broke on, because
    the crash may be about that track and a fifty track sync should not end on
    one bad file."""
    script.landings = landings("1", "2")
    script.authenticate_raises = AdapterBroken("the vendored tool is not installed")
    job_id = queued(listed(library, [("1", "A", "T"), ("2", "B", "U")]))

    drive(resume_argv(job_id))

    assert job_of(job_id).state is not jobs.JobState.BLOCKED
    assert causes(job_id)["1"] == "adapter-broken"
    assert states(job_id) == {"1": jobs.ItemState.FAILED, "2": jobs.ItemState.FAILED}


def test_a_provider_block_parks_the_job_and_makes_no_further_request(
    cfg, script, library
):
    """A forbidden response is about the CLIENT. The pacing layer stops the run
    and returns the cause; the worker hands it to the engine, which parks the
    job with the item released. The third track is never asked for."""
    script.landings = landings("1", "2", "3")
    script.landings["2"].fetch_raises = RuntimeError("403 Forbidden: access denied")
    job_id = queued(listed(library, [("1", "A", "T"), ("2", "B", "U"), ("3", "C", "V")]))

    code, envelope = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "blocked", envelope
    assert job_of(job_id).state is jobs.JobState.BLOCKED
    assert envelope["cause"]["reason"] == "provider-blocked"
    assert envelope["cause"]["retryable"] is False
    assert states(job_id) == {
        "1": jobs.ItemState.DONE,
        "2": jobs.ItemState.PENDING,
        "3": jobs.ItemState.PENDING,
    }
    assert [r.key for r in script.offered] == ["1", "2"], "a request followed the block"
    assert [r.key for r in script.fetched] == ["1", "2"]


def test_a_rate_limit_is_retried_under_backoff_and_then_lands(cfg, script, library):
    """A throttle is "slower", not "stop": the pool backs off and asks again,
    and the frozen pacing is what shapes the wait."""
    script.landings = landings("1")
    script.landings["1"].fetch_raises = RuntimeError("429 too many requests")
    script.landings["1"].fetch_raises_times = 2
    job_id = queued(listed(library, [("1", "A", "T")]))

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert states(job_id) == {"1": jobs.ItemState.DONE}
    assert [r.key for r in script.fetched] == ["1", "1", "1"]


def test_a_rate_limit_that_never_clears_fails_the_item_as_transient(
    cfg, script, library, slept
):
    script.landings = landings("1")
    script.landings["1"].fetch_raises = RuntimeError("429 too many requests")
    job_id = queued(listed(library, [("1", "A", "T")]))

    code, envelope = drive(resume_argv(job_id))

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
    job_id = queued(listed(library, [("1", "A", "T")]))

    drive(resume_argv(job_id))

    item = items_of(job_id)[0]
    assert item.cause is not None
    assert item.cause.reason == "unavailable-permanent"
    assert item.cause.retryable is False
    # THE POINT OF THE NAME. There is nothing to do about a track the provider no
    # longer has, and the remedy this refusal must never carry is the one that
    # tells somebody to weaken the lossless policy over it.
    assert item.cause.remediation.remedy != Remedy.RELAX_LOSSLESS_POLICY
    assert item.cause.remediation.remedy is Remedy.CHANGE_POLICY_OR_INPUT
    assert script.fetched == []


def test_a_run_reporting_nothing_for_the_key_is_refused_rather_than_read_as_success(
    cfg, script, monkeypatch, tmp_path
):
    """Absence is not evidence. Driven at the handler with a run shaped by hand,
    because the pool fills every slot it does not stop on."""
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


# ═══════════════════════════════════════════════════════════════════════════
# The lossless policy, at the file
# ═══════════════════════════════════════════════════════════════════════════


def test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named(
    cfg, script, library
):
    """The offer says lossless and the file is not. The check is at the FILE,
    so the lie is caught, and the refused file is left where it landed."""
    script.landings = landings("1", kind="lossy", offer_lossless=True)
    job_id = queued(listed(library, [("1", "A", "T")]))

    code, envelope = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK)
    item = items_of(job_id)[0]
    assert item.state is jobs.ItemState.FAILED
    assert item.cause is not None
    assert item.cause.reason == "lossy-refused"
    assert "MP3" in item.cause.message
    assert item.cause.remediation.remedy == Remedy.RELAX_LOSSLESS_POLICY
    staging = Path(cfg.paths.download_staging)
    assert not (staging / "1.mp3").exists(), "a refused landing was committed"
    evidence = staging / acquire_cli.ACQUIRE_STAGING_DIRNAME / job_id / "0" / "1.mp3"
    assert evidence.is_file(), "the refused file was not left as evidence"


def test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched(
    cfg, script, library
):
    script.landings = landings("1", kind="lossy", offer_lossless=False)
    job_id = queued(listed(library, [("1", "A", "T")]))

    drive(resume_argv(job_id))

    assert causes(job_id) == {"1": "lossy-refused"}
    assert script.fetched == [], "a lossy offer was fetched under strict policy"


def test_a_lossy_landing_under_the_permissive_policy_is_committed_marked(
    library, script
):
    """R21: lossy is permitted only WITH the marker, and config owns its text."""
    cfg = _configure(library, lossless_policy="allow_lossy_marked")
    script.landings = landings("1", kind="lossy", offer_lossless=False)
    job_id = queued(listed(library, [("1", "A", "T")]))

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    item = items_of(job_id)[0]
    assert item.state is jobs.ItemState.DONE
    marker = cfg.naming.lossy_marker
    assert item.artifact == str(Path(cfg.paths.download_staging) / f"1 {marker}.mp3")
    assert Path(item.artifact).is_file()


def test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked(
    library, script
):
    """R21's forbidden state, reached through the offer rather than the file.

    The provider says lossless and lands lossy. ``requires_lossy_marker`` is
    derived from the OFFER, and the codec check inside the landing is strict
    policy's only, so trusting the claim commits an unmarked lossy file, which
    is the single state the audit verb exists to find. The marker is decided by
    the file instead.
    """
    cfg = _configure(library, lossless_policy="allow_lossy_marked")
    script.landings = landings("1", kind="lossy", offer_lossless=True)
    job_id = queued(listed(library, [("1", "A", "T")]))

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    item = items_of(job_id)[0]
    assert item.state is jobs.ItemState.DONE
    marker = cfg.naming.lossy_marker
    assert Path(item.artifact).name == f"1 {marker}.mp3"


def test_a_lossless_landing_under_the_permissive_policy_is_not_marked(library, script):
    _configure(library, lossless_policy="allow_lossy_marked")
    script.landings = landings("1")
    job_id = queued(listed(library, [("1", "A", "T")]))

    drive(resume_argv(job_id))

    item = items_of(job_id)[0]
    assert item.state is jobs.ItemState.DONE
    assert Path(item.artifact).name == "1.wav"


def test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked(
    tmp_path,
):
    """An unmarked lossy file is the single state the audit exists to find."""
    landed = tmp_path / "1.mp3"
    with pytest.raises(CratekitError) as caught:
        acquire_cli.marked_name(landed, "   ", required=True)
    assert caught.value.cause.reason == "lossy-refused"
    assert acquire_cli.marked_name(landed, "   ", required=False) == "1.mp3"
    assert acquire_cli.marked_name(landed, "[MP3]", required=True) == "1 [MP3].mp3"


def test_an_unreadable_landing_is_transient_and_not_a_policy_refusal(
    cfg, script, library
):
    """A file nothing could parse is a truncated download, and telling the
    person to relax the policy would make the product accept it."""
    script.landings = landings("1", kind="unreadable")
    job_id = queued(listed(library, [("1", "A", "T")]))

    drive(resume_argv(job_id))

    item = items_of(job_id)[0]
    assert item.cause is not None
    assert item.cause.reason == "unavailable-transient"
    assert item.cause.retryable is True
    assert item.cause.remediation.remedy == Remedy.RETRY_LATER


def test_the_permissive_policy_skips_the_codec_probe(tmp_path):
    """Under the permissive policy the file is what it is; the marker is the
    rule, and the probe is strict policy's."""
    junk = tmp_path / "1.flac"
    junk.write_bytes(b"junk")
    assert (
        acquire_cli.checked_landing(junk, "1", policy=LosslessPolicy.ALLOW_LOSSY_MARKED) == junk
    )


# ═══════════════════════════════════════════════════════════════════════════
# The frozen configuration, and where the pacing comes from
# ═══════════════════════════════════════════════════════════════════════════


def test_the_pacing_delay_comes_from_the_frozen_configuration_not_a_fresh_load(
    library, script, slept
):
    """KTD9 through the pool: the delay edited after queueing is not the delay
    this run waits. Every request waits once, jittered around the frozen
    nominal, and the configuration that moved reaches the person as drift."""
    _configure(library, pacing_delay_s=2.0)
    script.landings = landings("1", "2")
    job_id = queued(listed(library, [("1", "A", "T"), ("2", "B", "U")]))
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


# ═══════════════════════════════════════════════════════════════════════════
# The destination
# ═══════════════════════════════════════════════════════════════════════════


def test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it(
    cfg, script, library
):
    script.landings = landings("1")
    kept = Path(cfg.paths.download_staging) / "1.wav"
    kept.parent.mkdir(parents=True, exist_ok=True)
    kept.write_bytes(b"a file somebody kept")
    job_id = queued(listed(library, [("1", "A", "T")]))

    code, envelope = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK)
    assert causes(job_id) == {"1": "output-exists"}
    assert kept.read_bytes() == b"a file somebody kept"


# ═══════════════════════════════════════════════════════════════════════════
# The real default adapter, constructed for the first time, offline
# ═══════════════════════════════════════════════════════════════════════════


def test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy(
    library, script
):
    """The vendored adapter, built by the worker from a frozen configuration
    naming it, with no provider session in the keychain. No network is reached:
    the session scope refuses before there is a source, and the item's row says
    to re-authorise and where else to go. The fake is registered only so the
    registry is in its per test shape; the configuration names the real one."""
    _configure(library, adapter="tidal_dl_ng")
    job_id = queued(listed(library, [("1", "A", "T")]))

    drive(resume_argv(job_id))

    # THE CAUSE LANDS WHERE THE REFUSAL BELONGS, and this test asserts the pair
    # rather than picking one: a dead credential parks the JOB with the track
    # released, and a broken tool fails the ITEM. Which of the two an offline
    # machine produces depends on what is in its keychain, so both are read.
    job = job_of(job_id)
    item = items_of(job_id)[0]
    parked = job.state is jobs.JobState.BLOCKED
    cause = job.cause if parked else item.cause
    assert cause is not None
    assert cause.reason in {"auth-failed", "adapter-broken"}
    assert cause.remediation.remedy in {
        Remedy.REAUTHENTICATE_PROVIDER,
        Remedy.REPAIR_CREDENTIAL_STORE,
    }
    assert "streamrip" in cause.message
    assert (cause.reason == "auth-failed") is parked
    assert item.state is (jobs.ItemState.PENDING if parked else jobs.ItemState.FAILED)
    assert script.constructed == [], "the fake was constructed instead of the real adapter"


def test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name(library, script):
    """``load`` refuses an unknown name rather than falling back to the
    default; through the queue that refusal is the item's, not a traceback."""
    _configure(library, adapter="no-such-adapter")
    job_id = queued(listed(library, [("1", "A", "T")]))

    code, envelope = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK)
    item = items_of(job_id)[0]
    assert item.cause is not None
    assert "no-such-adapter" in item.cause.message


def test_a_pasted_web_address_gets_the_readers_own_refusal(cfg, library):
    """The most likely wrong input, and the sentence that tells them what to do.

    ``read_list`` refuses a URL by matching a scheme at the front of the string.
    Absolutising the path before the read turns ``https://host/x`` into a
    relative path under the working directory, which that guard cannot match,
    and the person gets a file-not-found over a mangled path instead.
    """
    code, envelope = drive(["--output", "json", "acquire", "download", "https://tidal.com/p/1"])

    assert code != int(ExitCode.OK)
    assert "web address" in envelope["cause"]["message"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_open_job_with_no_items_refuses_rather_than_reporting_success(cfg, library):
    """A job queued before this unit carries a frozen list path and no items.

    Driving it settles nothing and the engine's success transition then reports
    every track acquired over a list nothing read, which is R-198's empty queue
    wearing a full one's clothes. ``adopt`` and ``tagging`` both guard this;
    ``master`` does not need to, because it always queues exactly one item.
    """
    path = listed(library, [("1", "A", "T")])
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="acquire.download",
            payload={acquire_cli.LIST: str(path)},
            cfg=cfg,
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
    """The mapping the worker reads is total over the outcome vocabulary, so a
    fifth outcome added upstream fails here rather than as a KeyError on a row."""
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


# ═══════════════════════════════════════════════════════════════════════════
# R-678: the queueing half names the job it queued
# ═══════════════════════════════════════════════════════════════════════════


def test_queueing_a_download_names_the_job_and_the_command_that_drives_it(cfg, library):
    """Sitting 9: ``ok`` in under a second, and the identifier nowhere a person reads."""
    path = listed(library, [("10", "A", "T1"), ("20", "B", "T2")])

    code, text = drive_human(["acquire", "download", str(path)])

    assert code == int(ExitCode.OK), text
    with jobs.open_store() as store:
        (job,) = jobs.list_jobs(store)
    lines = text.splitlines()
    assert f"  job: {job.job_id}, queued" in lines, text
    drives = shlex.join(["crate", "acquire", "download", str(path.absolute()), "--job", job.job_id])
    assert f"  drive it with: {drives}" in lines, text
    assert "  items: 0 of 2 settled" in lines, text
