"""U51: the two outbound verbs run for real, driven end to end through the queue.

The binding the engine's own suite cannot see: a confirmed export queues its
tracks, a driver claims them, the report survives as a committed artifact, a
person is told what the provider could not match, and no path reaches a
remove. The provider is always a stand in on ``account.resolve``; the
dispatcher, gate, queue, driver and engines are real.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import handlers, registry
from cratekit.core import config, jobs, locations, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.export import cli as export_cli
from cratekit.favorites import cli as favorites_cli
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import artifacts, ledger, source
from cratekit.modules.outbound import shell as shell_module
from cratekit.modules.reports import export as library_export
from tests import outbound_fakes
from tests._containers import synth_container
from tests.cli_drive import approve_and_queue, drive, drive_human
from tests.test_config import valid_data

EXPORT_KEY = "export.playlist"
FAVORITES_KEY = "sync.favorites"
EXPORT_GATE = "export.playlist.confirm"
SWEEP_GATE = "sync.favorites.confirm"


# Fixtures


@pytest.fixture
def installed(tmp_path, monkeypatch):
    """A machine the real dispatcher can load, with every module switched on."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    source.forget_libraries()
    yield resolved
    source.forget_libraries()


@pytest.fixture
def exported(installed) -> Path:
    """One collection export under the configured library. Never a literal path (R1)."""
    return _export(installed)


#: The command tree each membership builds, the same for every drive here.
_PARSERS: dict = {}


@pytest.fixture(autouse=True)
def _less_work(monkeypatch):
    """Neither durability nor the command tree's construction is under test here:
    a temporary directory need not reach the disk, and one membership's tree is
    built once rather than on every drive."""
    monkeypatch.setattr(os, "fsync", lambda _fd: None)
    build = cli.build_parser

    def built(*args, **kwargs):
        if args or kwargs:
            return build(*args, **kwargs)
        membership = cli._membership()
        if membership not in _PARSERS:
            _PARSERS[membership] = build()
        return _PARSERS[membership]

    monkeypatch.setattr(cli, "build_parser", built)


def bind(monkeypatch, account) -> None:
    """Put ``account`` in front of the provider seam for this test."""
    monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(account))


def catalog(*indexes: int) -> dict[str, str]:
    return {str(index): f"tid-{index}" for index in indexes}


def fake(*indexes: int, **kwargs) -> outbound_fakes.FakeAccount:
    return outbound_fakes.FakeAccount(catalog=catalog(*indexes), **kwargs)


@pytest.fixture
def queue(exported, monkeypatch):
    """``queue(account, verb, gate)``: bind ``account``, then confirm and queue; the job id."""

    def queued(account=None, verb=None, gate=EXPORT_GATE) -> str:
        if account is not None:
            bind(monkeypatch, account)
        return approve_and_queue(verb or export_verb(exported), gate)[1]

    return queued


@pytest.fixture
def sweep(queue, exported):
    """``sweep(account)``: the favourites sweep confirmed and queued; the job id."""
    return lambda account=None: queue(account, favorites_verb(exported), SWEEP_GATE)


def _export(installed, **kwargs) -> Path:
    """The collection export under the library, written as ``kwargs`` say."""
    return outbound_fakes.write_export(installed.library.root / "outbound", **kwargs)


def export_verb(exported: Path, playlist: str = outbound_fakes.CRATE) -> list[str]:
    return ["export", "playlist", playlist, "--export", str(exported)]


def favorites_verb(exported: Path, playlist: str | None = None) -> list[str]:
    verb = ["sync", "favorites", "--export", str(exported)]
    if playlist is not None:
        verb += ["--favorites-playlist", playlist]
    return verb


# 1. The binding itself


def test_both_verbs_report_a_bound_worker_rather_than_a_reason_they_have_none():
    """``crate job show``'s worker field, at the source it is derived from."""
    for key in (EXPORT_KEY, FAVORITES_KEY):
        assert handlers.is_known(key), key
        assert handlers.unbound_reason(key) is None, key
        assert callable(handlers.resolve(key)), key


def test_the_two_bound_keys_are_the_ones_the_registry_declares():
    """Derived, so a renamed handler key fails here rather than at a queue."""
    declared = {
        entry.handler_key
        for entry in registry.ENTRIES
        if entry.landed and entry.long_running
    }
    assert {EXPORT_KEY, FAVORITES_KEY} <= declared


def test_job_show_reports_the_bound_worker_for_a_queued_export(queue):
    code, shown = drive(["job", "show", queue(fake(1, 2, 3))])
    assert code == int(ExitCode.OK), shown
    assert shown["data"]["progress"]["worker"] == "bound"
    assert shown["data"]["progress"]["worker_reason"] is None


# 2. The zero item rule: neither verb can queue empty work


def _queue_is_empty() -> bool:
    with jobs.open_store() as store:
        return not jobs.list_jobs(store)


def _precondition(verb: list[str], reason: str) -> dict:
    """The refusal ``verb`` meets before anything is queued, for ``reason``."""
    code, refused = drive(verb)
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == reason
    return refused


@pytest.mark.parametrize(
    "verb, reason",
    [
        (["export", "playlist", outbound_fakes.CRATE], "outbound-export-required"),
        (["sync", "favorites"], "outbound-export-required"),
    ],
    ids=["export.playlist", "sync.favorites"],
)
def test_neither_verb_queues_anything_without_an_export(installed, verb, reason):
    """No document, no items, no job. Not a usage error either."""
    del installed
    code, refused = drive(verb)
    assert code == int(ExitCode.PRECONDITION), refused
    assert code != int(ExitCode.USAGE)
    assert refused["cause"]["reason"] == reason
    assert _queue_is_empty()


def test_an_export_naming_a_playlist_the_document_lacks_queues_nothing(exported):
    _precondition(export_verb(exported, "no-such-crate"), "export-playlist-unknown")
    assert _queue_is_empty()


def test_a_name_that_is_a_folder_refuses_rather_than_resolving(installed):
    """The live library's ``Favorites`` shape, which is why the default is its child."""
    path = _export(installed, extra_children=outbound_fakes.folder_only("Favorites"))
    _precondition(favorites_verb(path, "Favorites"), "export-playlist-unknown")
    assert _queue_is_empty()


def test_an_empty_playlist_refuses_distinguishably_from_an_absent_one(installed):
    path = _export(installed, favorites=())
    refused = _precondition(favorites_verb(path), "export-playlist-empty")
    assert refused["cause"]["reason"] != "export-playlist-unknown"
    assert _queue_is_empty()


def _two_playlists_called(name: str) -> list[str]:
    """The same display name in two folders, which is a real per-year tree shape."""
    return [
        *outbound_fakes.nested_playlist("Crates", name, [1]),
        *outbound_fakes.nested_playlist("Archive", name, [2]),
    ]


def test_a_name_two_playlists_carry_refuses_and_names_both_paths(installed):
    path = _export(installed, extra_children=_two_playlists_called("2026"))
    refused = _precondition(export_verb(path, "2026"), "export-playlist-ambiguous")
    assert sorted(refused["cause"]["detail"]["paths"]) == ["Archive/2026", "Crates/2026"]
    assert _queue_is_empty()


def test_the_full_path_disambiguates_what_the_bare_name_could_not(installed):
    path = _export(installed, extra_children=_two_playlists_called("2026"))
    resolved = source.resolve(source.read_library(path), "Crates/2026")
    assert resolved.key == "Crates/2026"
    assert resolved.track_ids == ("1",)


def test_a_top_level_playlist_wins_over_a_nested_one_of_the_same_name(installed):
    """The exact-path rule, driven, so it is a decision rather than an accident."""
    path = _export(installed, extra_children=outbound_fakes.nested_playlist(
            "Crates", outbound_fakes.CRATE, [1]
        ),
    )
    resolved = source.resolve(source.read_library(path), outbound_fakes.CRATE)
    assert resolved.key == outbound_fakes.CRATE
    assert resolved.track_ids == ("1", "2", "3")


def test_a_dangling_track_id_is_reported_and_not_queued(installed):
    """R-146 input, driven. The reader accepts it, so this is reachable."""
    path = _export(installed, crate=(1, 2, 99), tracks=2)
    resolved = source.resolve(source.read_library(path), outbound_fakes.CRATE)
    assert resolved.track_ids == ("1", "2")
    assert resolved.dangling == ("99",)


def test_a_repeated_track_id_becomes_one_item(installed):
    """A repeat would break ``job_items``' key and reach a person as ``internal-error``."""
    path = _export(installed, crate=(1, 2, 1))
    resolved = source.resolve(source.read_library(path), outbound_fakes.CRATE)
    assert resolved.track_ids == ("1", "2")
    assert resolved.repeated == ("1",)


def test_a_queued_export_holds_one_item_per_track(queue):
    assert [item.item_id for item in _items(queue(fake(1, 2, 3)))] == ["1", "2", "3"]


# 3. The export worker runs


def _items(job_id: str) -> list:
    with jobs.open_store() as store:
        return list(jobs.items(store, job_id))


def _job(job_id: str):
    with jobs.open_store() as store:
        return jobs.get(store, job_id)


def _resume(job_id: str, run=drive) -> tuple[int, dict]:
    """Drive the resume the job engine would spawn, in THIS process."""
    from cratekit.cli import jobs as cli_jobs

    return run(cli_jobs.argv_for(_job(job_id)))


def _done(job_id: str) -> dict:
    """The resume, driven to a clean finish."""
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    return resumed


def _retried(job_id: str) -> tuple[int, dict]:
    """Re-armed in process, as ``crate job resume`` does before its child, then driven."""
    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    return _resume(job_id)


def test_an_export_runs_pending_to_done_and_its_artifact_reads_back(installed, queue):
    """The whole point of the unit, driven through the real resume path."""
    account = fake(1, 2, 3)
    job_id = queue(account)
    resumed = _done(job_id)
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert resumed["data"]["progress"]["counts"]["done"] == 3
    reports = artifacts.committed(installed, job_id)
    assert len(reports) == 3
    assert [report["track"] for report in reports] == ["1", "2", "3"]
    for report in reports:
        assert report["playlist_key"] == outbound_fakes.CRATE
        assert report["remote_id"] == "pl-1"
        assert report["unmatched"] == []
    assert [report["created"] for report in reports] == [True, False, False]
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-2", "tid-3")
    assert account.created == [outbound_fakes.CRATE]


def test_a_second_export_of_the_same_playlist_adds_nothing_and_creates_nothing(queue):
    account = fake(1, 2, 3)
    _done(queue(account))
    resumed = _done(queue())
    assert account.created == [outbound_fakes.CRATE]
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-2", "tid-3")
    assert resumed["data"]["progress"]["outbound"]["added"] == []
    assert sorted(resumed["data"]["progress"]["outbound"]["already"]) == ["tid-1", "tid-2", "tid-3"]


def test_the_envelope_names_the_tracks_the_provider_could_not_match(queue):
    """Without this a person sees three of three items done and is told nothing."""
    resumed = _done(queue(fake(2)))
    assert resumed["data"]["progress"]["outbound"]["added"] == ["tid-2"]
    assert sorted(resumed["data"]["progress"]["outbound"]["unmatched"]) == ["1", "3"], (
        "the envelope must name the library identity of each unmatched row, not "
        "a stringified mapping nothing downstream can key on"
    )


def _codes(envelope: dict) -> list[str]:
    return [warning["code"] for warning in envelope["warnings"]]


def test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers(queue):
    """R-850, driven. A live export of eight answered ``ok`` and ``8 of 8 settled``."""
    account = fake(1, 3)
    job_id = queue(account)
    resumed = _done(job_id)
    assert resumed["outcome"] == "ok"
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["counts"] == {"written": 2, "already": 0, "unmatched": 1}
    assert outbound["unmatched_tracks"] == [
        {
            "identity": "2",
            "artist": "Artist 2",
            "title": "08A - 124 - Track 2",
            "reason": export_cli.NO_MATCH,
        }
    ]
    assert _codes(resumed) == [export_cli.UNMATCHED_WARNING]
    (warning,) = resumed["warnings"]
    assert "1 of the 3 track(s)" in warning["message"]
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-3")
    code, said = _resume(job_id, drive_human)
    assert code == int(ExitCode.OK), said
    assert "  tracks: 2 written, 0 already there or written before, 1 unmatched" in said
    assert (f"    unmatched: Artist 2 - 08A - 124 - Track 2: {export_cli.NO_MATCH}" in said), said
    assert f"warning [{export_cli.UNMATCHED_WARNING}]" in said


def test_an_export_where_every_track_matches_answers_with_no_unmatched_line(queue):
    job_id = queue(fake(1, 2, 3))
    resumed = _done(job_id)
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["counts"] == {"written": 3, "already": 0, "unmatched": 0}
    assert outbound["unmatched_tracks"] == []
    assert export_cli.UNMATCHED_WARNING not in _codes(resumed)
    code, said = _resume(job_id, drive_human)
    assert "  tracks: 3 written, 0 already there or written before, 0 unmatched" in said, said
    assert "unmatched:" not in said
    assert export_cli.UNMATCHED_WARNING not in said


def test_a_second_export_counts_what_the_playlist_already_held(queue):
    _done(queue(fake(1, 2, 3)))
    resumed = _done(queue())
    assert resumed["data"]["progress"]["outbound"]["counts"] == {
        "written": 0,
        "already": 3,
        "unmatched": 0,
    }


def test_a_resumed_export_counts_across_both_runs_and_each_item_once(queue):
    """U270: a refused request adds none, so the resume settles all three, each once."""
    account = fake(1, 3, fail_on={"tid-3"}, transient=True)
    job_id = queue(account)
    assert _resume(job_id)[0] != int(ExitCode.OK)
    account.fail_on = frozenset()
    code, resumed = _retried(job_id)
    assert code == int(ExitCode.OK), resumed
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["counts"] == {"written": 2, "already": 0, "unmatched": 1}
    assert sorted(outbound["added"]) == ["tid-1", "tid-3"]
    assert [row["identity"] for row in outbound["unmatched_tracks"]] == ["2"]
    assert account.added.count(("pl-1", "tid-1")) == 1


def _match_fails_for(account, identity: str, *, transient: bool = True) -> None:
    """Make ONE track's match fail, which fails that item alone (U270)."""
    real = account.match_track

    def broken(**asked):
        if asked["identity"] == identity and account.fail_on:
            if transient:
                raise refuse(
                    "unavailable-transient",
                    f"interrupted outbound match for {identity}",
                    remedy=Remedy.RETRY_LATER,
                    retryable=True,
                    origin=("test",),
                )
            raise RuntimeError(f"interrupted outbound match for {identity}")
        return real(**asked)

    account.match_track = broken


def test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it(queue):
    """The engine's resume guarantee, through the binding rather than beside it."""
    account = fake(1, 2, 3, fail_on={"armed"})
    _match_fails_for(account, "2")
    job_id = queue(account)
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    states = {item.item_id: str(item.state) for item in _items(job_id)}
    assert states["1"] == str(jobs.ItemState.DONE)
    assert states["2"] == str(jobs.ItemState.FAILED)
    assert states["3"] == str(jobs.ItemState.DONE)
    account.fail_on = frozenset()
    assert _retried(job_id)[0] == int(ExitCode.OK)
    after = {item.item_id: str(item.state) for item in _items(job_id)}
    assert after["2"] == str(jobs.ItemState.DONE)
    # The two that already succeeded were not written a second time.
    assert account.added.count(("pl-1", "tid-1")) == 1
    assert account.added.count(("pl-1", "tid-2")) == 1
    assert account.added.count(("pl-1", "tid-3")) == 1
    assert account.chunks == [("pl-1", ("tid-1", "tid-3")), ("pl-1", ("tid-2",))]


def test_a_track_the_provider_would_not_add_fails_its_item_alone_and_is_never_recorded(
    installed, queue
):
    """U270: the track the answer leaves out fails alone and is never recorded."""
    account = fake(1, 2, 3)
    account.unaddable.add("tid-2")
    job_id = queue(account)
    assert _resume(job_id)[0] != int(ExitCode.OK)
    held = _items(job_id)
    states = {item.item_id: str(item.state) for item in held}
    cause = {item.item_id: item.cause for item in held}["2"]
    assert states == {
        "1": str(jobs.ItemState.DONE),
        "2": str(jobs.ItemState.FAILED),
        "3": str(jobs.ItemState.DONE),
    }
    assert cause is not None and cause.reason == "unavailable-transient"
    assert "the provider added nothing for the track 'tid-2'" in cause.message
    written = json.loads(config.state_path("outbound_writes", installed).read_text())
    assert [record["added"] for record in written["playlists"].values()] == [["tid-1", "tid-3"]]
    assert "sending" not in next(iter(written["playlists"].values()))
    assert account.playlists["pl-1"] == ["tid-1", "tid-3"]


def test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once(queue):
    """U270: one request carries the batch, so a refused one fails each of its items."""
    account = fake(1, 2, 3, fail_on={"tid-2"}, transient=True)
    job_id = queue(account)
    assert _resume(job_id)[0] != int(ExitCode.OK)
    states = {item.item_id: str(item.state) for item in _items(job_id)}
    assert set(states.values()) == {str(jobs.ItemState.FAILED)}
    assert account.added == []
    account.fail_on = frozenset()
    assert _retried(job_id)[0] == int(ExitCode.OK)
    assert account.playlists["pl-1"] == ["tid-1", "tid-2", "tid-3"]
    assert [one for _pl, one in account.added] == ["tid-1", "tid-2", "tid-3"]


def test_the_resume_of_a_half_failed_export_does_not_exit_ok(queue):
    """R-225, pinned where the branch was written rather than inherited."""
    account = fake(1, 2, 3, fail_on={"armed"})
    # One track's own defect, met while its batch is planned (U270).
    _match_fails_for(account, "2", transient=False)
    code, resumed = _resume(queue(account))
    assert code != int(ExitCode.OK)
    assert sorted(one for _pl, one in account.added) == ["tid-1", "tid-3"]
    assert resumed["cause"] is not None
    # The item's own cause, a RuntimeError, not retryable (R-380).
    assert resumed["cause"]["reason"] == "internal-error"
    assert resumed["cause"]["retryable"] is False
    assert resumed["data"] is None or resumed["data"].get("state") != str(jobs.JobState.SUCCEEDED)


# 4. The favourites sweep runs, add only


def test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row(installed, sweep):
    account = fake(1, 2)
    job_id = sweep(account)
    resumed = _done(job_id)
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert sorted(account.hearted) == ["tid-1", "tid-2"]
    reports = artifacts.committed(installed, job_id)
    assert [report["row"] for report in reports] == ["1", "2"]


def test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written(sweep):
    """The add-only property under the condition that would expose a re-write."""
    account = fake(1, 2, hearts={"tid-1"})
    resumed = _done(sweep(account))
    assert account.hearted == ["tid-2"]
    assert resumed["data"]["progress"]["outbound"]["hearted"] == ["tid-2"]
    assert resumed["data"]["progress"]["outbound"]["already"] == ["tid-1"]


def test_a_second_sweep_writes_nothing_because_the_ledger_remembers(sweep):
    """The ledger short circuit, reached without asking the provider at all."""
    first_account = fake(1, 2)
    _done(sweep(first_account))
    assert sorted(first_account.hearted) == ["tid-1", "tid-2"]
    second_account = fake(1, 2)
    _done(sweep(second_account))
    assert second_account.hearted == [], (
        "the ledger is the only thing that can stop this write: this account "
        "hearts nothing, so a re-write means the recorded hearts were not read"
    )


def test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item(sweep):
    resumed = _done(sweep(fake(1)))
    assert resumed["data"]["progress"]["counts"]["done"] == 2
    assert resumed["data"]["progress"]["outbound"]["unmatched"] == ["2"]


def _three_favourites(installed, queue, account) -> str:
    """A sweep queued over an export whose favourites playlist holds all three rows."""
    three = outbound_fakes.write_export(installed.library.root / "outbound-three", favorites=(1, 2, 3))
    return queue(account, favorites_verb(three), SWEEP_GATE)


def test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers(
    installed, queue
):
    """R-856, driven. The sweep answered ``ok`` and ``3 of 3 settled`` and nothing else."""
    account = fake(1, 3)
    job_id = _three_favourites(installed, queue, account)
    resumed = _done(job_id)
    assert resumed["outcome"] == "ok"
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["counts"] == {"hearted": 2, "already_hearted": 0, "unmatched": 1}
    assert outbound["unmatched_tracks"] == [
        {
            "identity": "2",
            "artist": "Artist 2",
            "title": "Track 2",
            "reason": favorites_cli.NO_MATCH,
        }
    ]
    assert _codes(resumed) == [
        favorites_cli.LOCAL_WRITE_WARNING["code"],
        favorites_cli.UNMATCHED_WARNING,
    ]
    assert "1 of the 3 favourite(s)" in resumed["warnings"][1]["message"]
    assert sorted(account.hearted) == ["tid-1", "tid-3"]
    code, said = _resume(job_id, drive_human)
    assert code == int(ExitCode.OK), said
    assert "  tracks: 2 hearted, 0 already hearted or hearted before, 1 unmatched" in said
    assert f"    unmatched: Artist 2 - Track 2: {favorites_cli.NO_MATCH}" in said, said
    assert f"warning [{favorites_cli.UNMATCHED_WARNING}]" in said
    assert _says_no_local_write(said), said


def test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line(installed, queue):
    job_id = _three_favourites(installed, queue, fake(1, 2, 3, hearts={"tid-3"}))
    resumed = _done(job_id)
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["counts"] == {"hearted": 2, "already_hearted": 1, "unmatched": 0}
    assert outbound["unmatched_tracks"] == []
    assert _codes(resumed) == [favorites_cli.LOCAL_WRITE_WARNING["code"]]
    code, said = _resume(job_id, drive_human)
    assert "  tracks: 2 hearted, 1 already hearted or hearted before, 0 unmatched" in said, said
    assert "unmatched:" not in said
    assert favorites_cli.UNMATCHED_WARNING not in said


def test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason(installed, queue):
    account = fake(1, 2)
    several = (
        "the ISRC GBXXX names 2 provider tracks, 2 of them agree with this row's "
        "artist, title and version and the account hearts 0 of those, so none was chosen"
    )
    account.reasons["3"] = several
    job_id = _three_favourites(installed, queue, account)
    resumed = _done(job_id)
    (row,) = resumed["data"]["progress"]["outbound"]["unmatched_tracks"]
    assert row == {"identity": "3", "artist": "Artist 3", "title": "Track 3", "reason": several}
    code, said = _resume(job_id, drive_human)
    assert f"    unmatched: Artist 3 - Track 3: {several}" in said, said


def test_a_report_written_before_the_listing_still_names_its_unmatched_rows():
    """An artifact from an earlier build carries ``reasons`` and no listing."""
    report = {
        "unmatched": ["4", "5"],
        "reasons": [{"row": "4", "artist": "A", "title": "T", "reason": "names 2"}],
    }
    said = list(report["reasons"])
    assert favorites_cli._left_out(report, said) == [
        {"identity": "4", "artist": "A", "title": "T", "reason": "names 2"},
        {"identity": "5", "artist": "", "title": "", "reason": favorites_cli.NO_MATCH},
    ]


def test_the_sweep_warning_counts_only_whole_numbers():
    assert favorites_cli.concluded({}) == ()
    assert favorites_cli.concluded({"counts": {"hearted": 3, "unmatched": 0}}) == ()
    assert favorites_cli.concluded({"counts": {"hearted": 3, "unmatched": True}}) == ()
    (warning,) = favorites_cli.concluded(
        {"counts": {"hearted": 2, "already_hearted": True, "unmatched": 1}}
    )
    assert warning["code"] == favorites_cli.UNMATCHED_WARNING
    assert warning["message"].startswith("1 of the 3 favourite(s)")


def test_the_sweep_reaches_nothing_outside_the_add_only_protocol(monkeypatch, sweep):
    """An absence proves nothing; this raises on any attribute outside the protocol."""
    bind(monkeypatch, outbound_fakes.StrictAccount(catalog=catalog(1, 2)))
    _done(sweep())


def test_no_colour_writer_reaches_the_engine_from_a_queued_sweep(monkeypatch, sweep):
    """``colors=None``, asserted at the engine boundary rather than in prose."""
    seen: list[object] = []
    real = favorites_cli.hearts.heart_back

    def watched(cfg, remote, candidates, *, colors=None, flags=None):
        seen.append((colors, flags))
        return real(cfg, remote, candidates, colors=colors, flags=flags)

    monkeypatch.setattr(favorites_cli.hearts, "heart_back", watched)
    _done(sweep(fake(1, 2)))
    assert seen and all(colors is None for colors, _flags in seen)


def test_the_resume_of_a_half_failed_sweep_does_not_exit_ok(sweep):
    code, resumed = _resume(sweep(fake(1, 2, fail_on={"tid-2"})))
    assert code != int(ExitCode.OK)
    assert resumed["cause"] is not None


# 4b. R-424: the verb says only what it does, in the output a person gets


def _asked(verb: list[str]) -> dict:
    """The refusal a verb's gate answers first, with the decision it needs."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused


def _decided(refused: dict, option: str | None = None) -> str:
    """A person's answer to the gate ``refused`` names, its first option unless given."""
    detail = refused["cause"]["detail"]
    run_id = str(refused["run_id"])
    answer = option or detail["options"][0]
    decided, envelope = drive(["run", "decide", run_id, detail["gate"], answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    return run_id


def _answer_the_confirm(verb: list[str], gate: str) -> str:
    """R34's first two acts, without the third. Returns the gate run."""
    refused = _asked(verb)
    assert refused["cause"]["detail"]["gate"] == gate
    return _decided(refused)


def _says_no_local_write(text: str) -> bool:
    """The warning as the renderer prints it, on its own line."""
    code = favorites_cli.LOCAL_WRITE_WARNING["code"]
    message = favorites_cli.LOCAL_WRITE_WARNING["message"]
    return f"warning [{code}]: {message}" in text.splitlines()


def test_queueing_a_sweep_tells_a_person_in_the_default_output_that_nothing_local_is_written(
    installed, exported, monkeypatch
):
    """R-424's cost, driven on the surface that carried it."""
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    run_id = _answer_the_confirm(favorites_verb(exported), "sync.favorites.confirm")
    code, text = drive_human(["--run", run_id, *favorites_verb(exported)])
    assert code == int(ExitCode.OK), text
    assert _says_no_local_write(text), text


def test_the_resumed_sweep_says_the_same_thing_where_the_hearting_actually_happens(sweep):
    """The queueing pass writes nothing at all; the resume is the run."""
    job_id = sweep(fake(1, 2))
    from cratekit.cli import jobs as cli_jobs
    argv = cli_jobs.argv_for(_job(job_id))
    code, text = drive_human(argv)
    assert code == int(ExitCode.OK), text
    assert _says_no_local_write(text), text


def test_an_item_report_carries_no_empty_colored_list(installed, sweep):
    """R-424's other half: an empty list reads as a write that found nothing."""
    job_id = sweep(fake(1, 2))
    _done(job_id)
    reports = artifacts.committed(installed, job_id)
    assert reports, "the sweep committed nothing to assert about"
    for report in reports:
        assert "colored" not in report, report
        assert "hearted" in report, report


def test_the_verb_declares_the_remote_account_and_no_local_surface():
    """The declaration R-424 is about, read off the shipped registry."""
    entry = registry.entry("sync.favorites")
    assert entry.writes == frozenset({"remote"}), sorted(entry.writes)
    assert not entry.writes & registry.DB_WRITE_SURFACES
    assert "colour" not in entry.summary and "both ways" not in entry.summary


def test_the_verb_asks_no_question_its_work_cannot_raise():
    """The cloud-sync decision goes with the database surfaces."""
    entry = registry.entry("sync.favorites")
    assert [spec.name for spec in entry.gates] == ["sync.favorites.confirm"]


def test_doctor_asks_neither_rekordbox_question_for_a_sweep_that_reads_an_export(
    monkeypatch,
):
    """Derived from this entry alone, the way ``route.unplaced`` pinned the same shape."""
    from cratekit.cli import doctor
    from cratekit.core import profiles
    monkeypatch.setattr(registry, "entries", lambda: (registry.entry("sync.favorites"),))
    membership = profiles.resolve("full")
    assert doctor.requires_check("library.mounted", membership)
    assert doctor.requires_check("credential.provider", membership)
    assert not doctor.requires_check("rekordbox.closed", membership)
    assert not doctor.requires_check("rekordbox.pins", membership)


def test_a_sweep_runs_with_rekordbox_open_and_never_opens_the_database(monkeypatch, sweep):
    """Why dropping both checks is safe, driven rather than argued."""
    from cratekit.core import rb_writer
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)

    def refuse_to_open(*args, **kwargs):
        raise AssertionError("the favourites sweep opened the library database")

    monkeypatch.setattr(rb_writer, "open_db", refuse_to_open)
    account = fake(1, 2)
    _done(sweep(account))
    assert sorted(account.hearted) == ["tid-1", "tid-2"]


# 5. The provider seam, and what a person is told before they confirm


def test_with_no_credential_the_seam_refuses_with_the_credential_cause(installed):
    """Distinguishable from the no-adapter refusal, because doctor can fix one."""
    with pytest.raises(CratekitError) as excinfo:
        account_module.resolve(installed)
    assert excinfo.value.cause.reason == "credential-missing"
    assert excinfo.value.cause.code is not ExitCode.INTERNAL


def unimportable_adapter(monkeypatch) -> None:
    """A build whose account adapter does not import, the unbound case since U63."""
    monkeypatch.setattr(
        account_module, "ADAPTER_MODULE", "cratekit.modules.outbound.no_such_adapter"
    )


def test_with_a_credential_stored_and_no_adapter_the_seam_refuses_unbound(
    installed, monkeypatch
):
    from cratekit.core import secrets
    monkeypatch.setattr(secrets, "exists", lambda name: True)
    unimportable_adapter(monkeypatch)
    with pytest.raises(CratekitError) as excinfo:
        account_module.resolve(installed)
    assert excinfo.value.cause.reason == "outbound-account-unbound"
    assert excinfo.value.cause.code is not ExitCode.INTERNAL
    assert excinfo.value.cause.remediation is not None


@pytest.mark.parametrize("adapter_imports", [True, False], ids=["bound", "unbound"])
def test_the_queued_envelope_warns_only_when_no_provider_adapter_is_bound(
    installed, exported, monkeypatch, adapter_imports
):
    """Told at the moment it is still actionable, not after the job has failed."""
    del installed
    if not adapter_imports:
        unimportable_adapter(monkeypatch)
    assert account_module.bound() is adapter_imports
    refused = _asked(export_verb(exported))
    _decided(refused)
    code, queued = drive(["--run", refused["run_id"], *export_verb(exported)])
    assert code == int(ExitCode.OK), queued
    codes = {warning["code"] for warning in queued.get("warnings") or ()}
    assert ("outbound-account-unbound" in codes) is not adapter_imports


def test_a_job_driven_with_no_adapter_fails_rather_than_reporting_success(queue):
    """What this build actually delivers on a machine with nothing bound."""
    job_id = queue()
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK)
    # The job's verdict for a person, the seam's cause on the items for a maintainer.
    assert resumed["cause"]["reason"] == "no-evidence"
    assert _job(job_id).state is jobs.JobState.FAILED
    reasons = {item.cause.reason for item in _items(job_id) if item.cause is not None}
    assert reasons <= {"credential-missing", "outbound-account-unbound"}
    assert reasons


# 6. The confirm digest, and the frozen configuration


def test_a_confirm_recorded_against_one_document_does_not_authorise_another(
    installed, monkeypatch
):
    """The reason the digest grew to cover the export path."""
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    first = outbound_fakes.write_export(installed.library.root / "one")
    second = outbound_fakes.write_export(installed.library.root / "two", crate=(1,))
    refused = _asked(export_verb(first))
    _decided(refused)
    code, other = drive(["--run", refused["run_id"], *export_verb(second)])
    assert code != int(ExitCode.OK), other
    assert other["cause"]["reason"] == "decision-stale"
    assert _queue_is_empty()


def test_a_relative_export_argument_still_resumes(exported, monkeypatch, tmp_path, queue):
    """The other half of the digest decision, and the one that would strand a job."""
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    monkeypatch.chdir(exported.parent)
    relative = ["export", "playlist", outbound_fakes.CRATE, "--export", exported.name]
    job_id = queue(verb=relative)
    assert Path(_job(job_id).payload["export"]).is_absolute()
    _done(job_id)


@pytest.mark.parametrize(
    "verb, gate, module, worker",
    [
        ("export", "export.playlist.confirm", export_cli, "run_export_items"),
        ("favorites", "sync.favorites.confirm", favorites_cli, "run_heart_item"),
    ],
    ids=["export.playlist", "sync.favorites"],
)
def test_the_handler_runs_against_the_frozen_configuration_not_the_current_one(
    installed, exported, monkeypatch, verb, gate, module, worker
):
    """KTD9, asserted on a key NO environment variable overrides."""
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    invocation = export_verb(exported) if verb == "export" else favorites_verb(exported)
    _run, job_id = approve_and_queue(invocation, gate)
    current = config.load()
    # BOTH BANDS MOVE, since validation refuses a stale count above the expired one.
    moved = replace(
        current,
        reports=replace(
            current.reports, intake_stale_days=99, intake_expired_days=180
        ),
    )
    config.save(moved)
    config.reset_cache()
    assert config.load().reports.intake_stale_days == 99
    seen: list[int] = []
    real = getattr(module, worker)

    def watched(payload, item_id, cfg, remote, *rest):
        seen.append(cfg.reports.intake_stale_days)
        return real(payload, item_id, cfg, remote, *rest)

    monkeypatch.setattr(module, worker, watched)
    _done(job_id)
    assert seen and all(days != 99 for days in seen), (
        "the handler saw the CURRENT configuration, not the one its job froze"
    )


# 7. First-caller failure paths through the engines


def test_an_item_whose_track_left_the_export_refuses_rather_than_writing_nothing(exported, queue):
    """A regenerated document under a queued job, driven."""
    job_id = queue(fake(1, 2, 3))
    exported.write_bytes(outbound_fakes.export_document(crate=(1,), tracks=1))
    source.forget_libraries()
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    failed = [item for item in _items(job_id) if item.state is jobs.ItemState.FAILED]
    assert {item.item_id for item in failed} == {"2", "3"}
    assert all(
        item.cause is not None and item.cause.reason == "outbound-item-absent"
        for item in failed
    )


def test_a_ledger_that_cannot_be_read_stops_the_write_rather_than_duplicating(installed, queue):
    """The engine's own refusal, reached through the binding for the first time."""
    account = fake(1, 2, 3)
    job_id = queue(account)
    ledger_path = config.state_path("outbound_writes", installed)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text("{not json", encoding="utf-8")
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    assert account.created == []
    causes = {item.cause.reason for item in _items(job_id) if item.cause is not None}
    assert causes == {"outbound-ledger-unusable"}


# 8. The derivation's own properties


def test_the_export_document_is_parsed_once_per_process(installed, monkeypatch):
    """The N times M shape ``coverage.py`` records this repository removing once."""
    path = _export(installed)
    reads: list[str] = []
    real = source.library_export.read_export_file

    def counted(target):
        reads.append(str(target))
        return real(target)

    monkeypatch.setattr(source.library_export, "read_export_file", counted)
    source.forget_libraries()
    for _ in range(4):
        source.read_library(path)
    assert len(reads) == 1


def test_the_two_engines_receive_the_same_rows_for_one_playlist(installed, exported):
    library = source.read_library(exported)
    resolved = source.resolve(library, outbound_fakes.CRATE)
    tracks = source.local_tracks(library, resolved.track_ids, cfg=installed)
    candidates = source.heart_candidates(library, resolved.track_ids, cfg=installed)
    assert [track.identity for track in tracks] == [c.row_id for c in candidates]
    assert [track.isrc for track in tracks] == [c.isrc for c in candidates]
    assert all(track.isrc == "" for track in tracks), (
        "these rows name no audio file, so there is no ISRC to read, and "
        "inventing one would hand the provider seam a fabricated identity"
    )
    assert all(track.title and track.artist for track in tracks)


def _entry(location: str) -> library_export.CollectionEntry:
    return library_export.CollectionEntry(
        track_id="1", name="08A - 124 - Track 1", artist="Artist 1", location=location
    )


def _tagged(tmp_path: Path, where: Path, isrc: str) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    made = synth_container(tmp_path, ".flac")
    where.parent.mkdir(parents=True, exist_ok=True)
    made.replace(where)
    assert tags.write_tags(where, {"isrc": isrc}) is True
    return where


def test_the_isrc_is_read_through_the_prefix_map_and_folded(installed, tmp_path):
    """R-355 and R-372 together: a renamed drive's row still reaches its file."""
    root = Path(installed.library.root)
    _tagged(tmp_path / "synth", root / "Music" / "a.flac", " zz-x9a-26-00042 ")
    old = tmp_path / "renamed-drive"
    recorded = locations.location_url(old / "Music" / "a.flac")
    rules = [locations.PrefixRule(str(old), str(root))]
    found = source.isrc_for(_entry(recorded), root=root, prefix_map=rules)
    assert found == "ZZX9A2600042"
    assert source.isrc_for(_entry(recorded), root=root, prefix_map=[]) == "", (
        "an unmapped prefix is not guessed onto the current root"
    )


@pytest.mark.parametrize(
    "location",
    [
        "",
        "file://elsewhere/Music/a.flac",
        "tidal:tracks:123",
        "file://localhost/nowhere/a.flac",
    ],
    ids=["no-location", "remote-host", "streaming", "unmapped"],
)
def test_a_location_with_no_local_file_reads_as_no_isrc(installed, location):
    root = Path(installed.library.root)
    assert source.isrc_for(_entry(location), root=root, prefix_map=[]) == ""


def test_a_missing_file_or_a_value_that_is_not_an_isrc_reads_as_none(
    installed, tmp_path
):
    """Empty is the honest route: the account reports the row unmatched."""
    root = Path(installed.library.root)
    gone = locations.location_url(root / "Music" / "gone.flac")
    assert source.isrc_for(_entry(gone), root=root, prefix_map=[]) == ""
    for index, value in enumerate(("CAT-0042", "ZZX9A260004", "ZZX9A26000421", "1ZX9A2600042")):
        path = _tagged(tmp_path / str(index), root / "Music" / f"bad{index}.flac", value)
        assert source.isrc_for(
            _entry(locations.location_url(path)), root=root, prefix_map=[]
        ) == "", value


def test_the_row_builders_use_the_configured_prefix_map(tmp_path, monkeypatch):
    """The builders must hand the resolver the config's map, not an empty one."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    old = tmp_path / "renamed-drive"
    data["library"]["location_prefix_map"] = [{"from": str(old), "to": "{library.root}"}]
    cfg = config.from_dict(data)
    _tagged(tmp_path / "synth", root / "Music" / "1.flac", "ZZX9A2600042")
    exported = outbound_fakes.write_export(
        root / "outbound",
        locations={1: locations.location_url(old / "Music" / "1.flac")},
    )
    source.forget_libraries()
    library = source.read_library(exported)
    assert [t.isrc for t in source.local_tracks(library, ("1", "2"), cfg=cfg)] == [
        "ZZX9A2600042",
        "",
    ]
    assert [c.isrc for c in source.heart_candidates(library, ("1",), cfg=cfg)] == ["ZZX9A2600042"]
    source.forget_libraries()


def test_an_absent_library_root_refuses_rather_than_reading_every_row_untagged(installed, exported):
    """The review's finding: an unmounted volume is not a library of untagged files."""
    library = source.read_library(exported)
    gone = replace(installed, library=replace(installed.library, root=installed.library.root / "unplugged"))
    for build in (source.local_tracks, source.heart_candidates):
        with pytest.raises(CratekitError) as raised:
            build(library, ("1",), cfg=gone)
        assert raised.value.cause.reason == "library-volume-unmounted"


def test_the_default_favourites_playlist_is_the_one_the_fixture_carries():
    """A default that drifted from the live library's shape is the whole point."""
    assert source.DEFAULT_FAVORITES_PLAYLIST == outbound_fakes.FAVORITES


# 9. What the review found a green suite could not see


def test_a_dangling_track_is_named_in_the_queued_envelope(installed, monkeypatch, queue):
    """The derivation collected it and nothing drove the reporting of it."""
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    path = _export(installed, crate=(1, 2, 99), tracks=2)
    job_id = queue(verb=export_verb(path))
    code, shown = drive(["job", "show", job_id])
    assert code == int(ExitCode.OK), shown
    assert [item.item_id for item in _items(job_id)] == ["1", "2"]


def test_the_queued_envelope_names_a_missing_and_a_repeated_track(
    installed, monkeypatch
):
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    path = _export(installed, crate=(1, 2, 99, 1, 1), tracks=2)
    refused = _asked(export_verb(path))
    _decided(refused)
    code, queued = drive(["--run", refused["run_id"], *export_verb(path)])
    assert code == int(ExitCode.OK), queued
    warnings = {w["code"]: w["message"] for w in queued.get("warnings") or ()}
    assert "playlist-track-missing" in warnings
    assert "99" in warnings["playlist-track-missing"]
    assert "playlist-track-repeated" in warnings
    # ONE track repeated, however many times: the count and the list name distinct tracks.
    assert warnings["playlist-track-repeated"].startswith("1 track(s)")
    assert warnings["playlist-track-repeated"].count("'1'") <= 1


def test_a_ledger_that_cannot_be_written_creates_no_remote_playlist_at_all(monkeypatch, queue):
    """The duplicate playlist defect, driven, in the direction that produced it."""
    account = fake(1, 2, 3)
    job_id = queue(account)

    def unwritable(cfg):
        raise ledger._unusable(Path("outbound_writes.lock"), "the state directory is not writable")

    monkeypatch.setattr(ledger, "_locked", unwritable)
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    assert account.created == [], (
        "an unwritable ledger must refuse BEFORE the remote playlist is made; "
        "a create the ledger cannot record is one the next item makes again"
    )


def test_a_cancelled_job_does_not_report_a_clean_resume(queue):
    """R-225 taken to the state that actually reaches a person: an interrupt."""
    job_id = queue(fake(1, 2, 3))
    with jobs.open_store() as store:
        cancelled = jobs.cancel(store, job_id)
    assert cancelled.state is jobs.JobState.CANCELLED
    assert cancelled.cause is not None
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    assert resumed["cause"] is not None


def test_a_job_with_no_items_refuses_rather_than_reporting_a_clean_success(queue):
    """The zero item rule on the DRIVE side, for a job neither verb can queue now."""
    job_id = queue(fake(1, 2, 3))
    with jobs.open_store() as store:
        with store.immediate() as conn:
            conn.execute("DELETE FROM job_items WHERE job_id = ?", (job_id,))
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    assert resumed["cause"]["reason"] == "internal-error"
    assert _job(job_id).state is not jobs.JobState.SUCCEEDED


def test_a_confirm_does_not_authorise_a_different_track_set_at_the_same_path(
    installed, monkeypatch
):
    """The case the two-path test could not reach, and the one a person hits."""
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    path = _export(installed, crate=(1,))
    refused = _asked(export_verb(path))
    _decided(refused)
    path.write_bytes(outbound_fakes.export_document(crate=(1, 2, 3)))
    source.forget_libraries()
    code, other = drive(["--run", refused["run_id"], *export_verb(path)])
    assert code != int(ExitCode.OK), other
    assert other["cause"]["reason"] == "decision-stale"
    assert _queue_is_empty()


def test_job_show_reports_the_bound_worker_for_a_queued_sweep(sweep):
    """The plan named this for both verbs and only the export verb had it."""
    code, shown = drive(["job", "show", sweep(fake(1, 2))])
    assert code == int(ExitCode.OK), shown
    assert shown["data"]["progress"]["worker"] == "bound"


def test_a_failed_favourite_leaves_the_sweep_resumable(sweep):
    """The plan named it for both verbs and only the export verb had it."""
    account = fake(1, 2, fail_on={"tid-2"}, transient=True)
    job_id = sweep(account)
    assert _resume(job_id)[0] != int(ExitCode.OK)
    account.fail_on = frozenset()
    assert _retried(job_id)[0] == int(ExitCode.OK)
    assert sorted(account.hearted) == ["tid-1", "tid-2"]
    assert account.hearted.count("tid-1") == 1


def test_both_provider_refusals_carry_a_remediation_a_person_can_act_on(
    installed, monkeypatch
):
    """Not merely non-None: a remedy token or a step, or the refusal says nothing."""
    from cratekit.core import secrets
    with pytest.raises(CratekitError) as missing:
        account_module.resolve(installed)
    assert missing.value.cause.remediation is not None
    assert str(missing.value.cause.remediation.remedy)
    monkeypatch.setattr(secrets, "exists", lambda name: True)
    unimportable_adapter(monkeypatch)
    with pytest.raises(CratekitError) as unbound:
        account_module.resolve(installed)
    assert unbound.value.cause.reason == "outbound-account-unbound"
    remediation = unbound.value.cause.remediation
    assert remediation is not None
    assert remediation.steps or str(remediation.remedy)


def test_an_export_the_provider_matches_nothing_of_says_so_in_the_envelope(monkeypatch, queue):
    """The plan's success criterion, at its worst case rather than its easy one."""
    account = outbound_fakes.FakeAccount(catalog={})
    bind(monkeypatch, account)
    resumed = _done(queue())
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["added"] == []
    assert sorted(outbound["unmatched"]) == ["1", "2", "3"]


def test_a_bare_name_resolves_a_uniquely_named_nested_playlist(installed):
    """The bare-name fallback, reached into a resolution rather than a refusal."""
    path = _export(installed, extra_children=outbound_fakes.nested_playlist("Crates", "Deep Cuts", [2, 3]),
    )
    resolved = source.resolve(source.read_library(path), "Deep Cuts")
    assert resolved.key == "Crates/Deep Cuts"
    assert resolved.name == "Deep Cuts"
    assert resolved.track_ids == ("2", "3")


def test_aborting_the_confirmation_queues_nothing(exported):
    """The other option on the gate, which no test had ever chosen."""
    refused = _asked(export_verb(exported))
    detail = refused["cause"]["detail"]
    assert detail["options"][-1] == "abort"
    _decided(refused, "abort")
    code, aborted = drive(["--run", refused["run_id"], *export_verb(exported)])
    assert code == int(ExitCode.OK), aborted
    assert aborted["outcome"] == "no_op"
    assert aborted["data"]["state"] == "declined"
    assert _queue_is_empty()


# R-227. The export is a file somebody made by hand, and it can be old

#: A fixed instant, so an age is a subtraction rather than a race with the clock.
_WRITTEN = datetime(2026, 8, 1, 12, 0, 0, tzinfo=timezone.utc)

BOTH_VERBS = pytest.mark.parametrize(
    "verb, gate",
    [
        pytest.param("export", "export.playlist.confirm", id="export.playlist"),
        pytest.param("favorites", "sync.favorites.confirm", id="sync.favorites"),
    ],
)


@pytest.fixture
def document(tmp_path) -> Path:
    """A collection document written at ``_WRITTEN``."""
    path = tmp_path / "collection.xml"
    path.write_text("<x/>")
    os.utime(path, (_WRITTEN.timestamp(), _WRITTEN.timestamp()))
    return path


def _invocation(verb: str, exported: Path) -> list[str]:
    return export_verb(exported) if verb == "export" else favorites_verb(exported)


def _written_days_ago(exported: Path, days: float) -> datetime:
    """Set the export's modification time, and return the instant it now carries."""
    moment = datetime.now(timezone.utc).timestamp() - days * 86_400
    os.utime(exported, (moment, moment))
    return datetime.fromtimestamp(exported.stat().st_mtime, tz=timezone.utc)


def _local(moment: datetime) -> str:
    """The instant as the product shows it: this machine's zone, to the second."""
    return moment.astimezone().replace(microsecond=0).isoformat()


def _configure_stale_days(days: int) -> None:
    current = config.load()
    config.save(replace(current, outbound=replace(current.outbound, export_stale_days=days)))
    config.reset_cache()


@BOTH_VERBS
def test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows(
    installed, exported, verb, gate
):
    """R-227's cost, reproduced. The person deciding is told the file's date."""
    del installed
    written = _written_days_ago(exported, 30)
    refused = _asked(_invocation(verb, exported))
    detail = refused["cause"]["detail"]
    assert detail["gate"] == gate
    shown = detail["shown"]["export"]
    assert shown["file"] == exported.name
    assert shown["written"] == _local(written)
    assert shown["age_days"] == 30
    assert shown["stale_after_days"] == 7
    assert shown["freshness"] == "stale"
    # THE SENTENCE IS AT THE GATE, before anybody has confirmed.
    assert "Export the collection again" in shown["warning"]
    assert written.astimezone().date().isoformat() in shown["warning"]


@BOTH_VERBS
def test_the_date_reaches_a_person_who_is_not_reading_json(exported, verb, gate):
    """``drive`` is json only, and the human renderer is a second reader."""
    del gate
    written = _written_days_ago(exported, 30)
    code, text = drive_human(_invocation(verb, exported))
    assert code == int(ExitCode.DECISION_REQUIRED), text
    assert written.astimezone().date().isoformat() in text
    assert "freshness: stale" in text
    assert "Export the collection again" in text


@BOTH_VERBS
def test_the_queueing_envelope_warns_that_the_export_is_old(
    installed, exported, monkeypatch, verb, gate
):
    """Refuse nothing, the person decides. And say it again where they queued."""
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    written = _written_days_ago(exported, 30)
    run_id = _answer_the_confirm(_invocation(verb, exported), gate)
    code, queued = drive(["--run", run_id, *_invocation(verb, exported)])
    assert code == int(ExitCode.OK), queued
    stale = [w for w in queued["warnings"] if w["code"] == "outbound-export-stale"]
    assert len(stale) == 1, queued["warnings"]
    assert written.astimezone().date().isoformat() in stale[0]["message"]
    assert "30 days" in stale[0]["message"]
    assert _items(queued["data"]["job_id"]), "a stale export refuses nothing"


@BOTH_VERBS
def test_a_fresh_export_shows_its_date_and_warns_of_nothing(
    installed, exported, monkeypatch, verb, gate
):
    """The date is shown EVERY time, the warning only past the limit."""
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    _written_days_ago(exported, 2)
    refused = _asked(_invocation(verb, exported))
    shown = refused["cause"]["detail"]["shown"]["export"]
    assert shown["freshness"] == "within-limit"
    assert shown["age_days"] == 2
    assert "warning" not in shown, "a recent export has nothing to be warned of"
    run_id = _answer_the_confirm(_invocation(verb, exported), gate)
    code, queued = drive(["--run", run_id, *_invocation(verb, exported)])
    assert code == int(ExitCode.OK), queued
    codes = {w["code"] for w in queued.get("warnings") or ()}
    assert not codes & {"outbound-export-stale", "outbound-export-age-unknown"}


@BOTH_VERBS
def test_the_limit_is_the_configured_one_in_both_directions(exported, verb, gate):
    """A longer limit quiets a month old file, a shorter one flags a two day old one."""
    del gate
    _written_days_ago(exported, 30)
    _configure_stale_days(60)
    _code, refused = drive(_invocation(verb, exported))
    shown = refused["cause"]["detail"]["shown"]["export"]
    assert (shown["freshness"], shown["stale_after_days"]) == ("within-limit", 60)
    _written_days_ago(exported, 2)
    _configure_stale_days(1)
    _code, refused = drive(_invocation(verb, exported))
    shown = refused["cause"]["detail"]["shown"]["export"]
    assert (shown["freshness"], shown["stale_after_days"]) == ("stale", 1)


def test_old_means_past_the_limit_and_not_at_it(document):
    """Seven days exactly is not past seven days, and one second more is."""
    at = source.export_age(document, limit_days=7, now=_WRITTEN + timedelta(days=7))
    past = source.export_age(document, limit_days=7, now=_WRITTEN + timedelta(days=7, seconds=1))
    late = source.export_age(document, limit_days=7, now=_WRITTEN + timedelta(days=7, hours=23))
    assert (at.stale, at.age_days) == (False, 7)
    assert (past.stale, past.age_days) == (True, 7)
    assert (late.stale, late.age_days) == (True, 7)
    assert at.written == _WRITTEN


def test_a_few_hours_ahead_is_a_clock_and_reads_as_written_just_now(document):
    """A volume whose clock runs ahead, or an exFAT zone skew, is not news."""
    age = source.export_age(document, limit_days=7, now=_WRITTEN - timedelta(hours=14))
    assert (age.stale, age.age_days, age.future_dated) == (False, 0, False)
    assert shell_module.freshness(age) == "within-limit"


def test_a_date_well_in_the_future_is_not_the_freshest_export_there_could_be(document):
    """A date that cannot be true cannot be judged, and says so (built in review)."""
    age = source.export_age(document, limit_days=7, now=_WRITTEN - timedelta(days=400))
    assert age.future_dated is True
    assert (age.stale, age.age_days) == (False, None)
    assert shell_module.freshness(age) == "future-dated"
    (warning,) = shell_module.age_warnings(age)
    assert warning["code"] == "outbound-export-age-unknown"
    assert _WRITTEN.astimezone().date().isoformat() in warning["message"]
    shown = shell_module.shown_export(age)["export"]
    assert shown["written"] == _local(_WRITTEN)
    assert shown["warning"] == warning["message"]


def test_the_date_is_the_persons_own_and_not_greenwichs(tmp_path):
    """Nine in the evening in New York is one in the morning, tomorrow, in UTC."""
    document = tmp_path / "collection.xml"
    document.write_text("<x/>")
    written = datetime(2026, 8, 2, 1, 0, 0, tzinfo=timezone.utc)
    os.utime(document, (written.timestamp(), written.timestamp()))
    try:
        with pytest.MonkeyPatch.context() as zone:
            zone.setenv("TZ", "America/New_York")
            time.tzset()
            age = source.export_age(document, limit_days=7, now=written + timedelta(days=30))
            (warning,) = shell_module.age_warnings(age)
            block = shell_module.shown_export(age)["export"]
    finally:
        time.tzset()
    assert "2026-08-01" in warning["message"]
    assert "2026-08-02" not in warning["message"]
    assert block["written"] == "2026-08-01T21:00:00-04:00"


def test_the_sentence_does_not_say_seven_is_past_seven(document):
    """Staleness is a duration, never floored days (built in review)."""
    age = source.export_age(document, limit_days=7, now=_WRITTEN + timedelta(days=7, hours=5))
    (warning,) = shell_module.age_warnings(age)
    assert "7 days 5 hours ago" in warning["message"]
    assert shell_module.shown_export(age)["export"]["age"] == "7 days 5 hours"


def test_a_limit_too_large_for_a_duration_does_not_crash_the_question(document):
    """The value object holds on its own against an OverflowError (built in review)."""
    age = source.export_age(document, limit_days=10_000_000_000, now=_WRITTEN + timedelta(days=30))
    assert age.stale is False


def test_an_age_is_built_whole_or_not_at_all(tmp_path):
    """A date with no instant to judge it at would fold unknown into recent."""
    with pytest.raises(ValueError):
        source.ExportAge(path=tmp_path / "x.xml", limit_days=7, written=_WRITTEN)
    with pytest.raises(ValueError):
        source.ExportAge(path=tmp_path / "x.xml", limit_days=7, judged_at=_WRITTEN)


def test_a_modification_time_no_date_can_hold_is_unknown_rather_than_a_crash(
    tmp_path, monkeypatch
):
    """``export_age`` says it never raises, and only the stat was guarded."""
    document = tmp_path / "collection.xml"
    document.write_text("<x/>")

    class _Stat:
        st_mtime = 1e20

    monkeypatch.setattr(Path, "stat", lambda self, **kwargs: _Stat())
    age = source.export_age(document, limit_days=7, now=_WRITTEN)
    assert age.known is False


def test_an_age_that_cannot_be_read_is_unknown_rather_than_fresh(tmp_path):
    """Absence of a date is not evidence of a recent one (METHOD, pattern one)."""
    age = source.export_age(tmp_path / "gone.xml", limit_days=7, now=_WRITTEN)
    assert age.written is None
    assert age.age_days is None
    assert age.stale is False
    assert age.known is False
    codes = [w["code"] for w in shell_module.age_warnings(age)]
    assert codes == ["outbound-export-age-unknown"]
    shown = shell_module.shown_export(age)["export"]
    assert shown["written"] is None
    assert shown["age_days"] is None
    assert shown["freshness"] == "unknown"


# R-229. A crate rekordbox shows under a new path keeps its remote playlist

_GATE = "export.playlist.confirm"
_FOLDER = "Sets"
_MOVED = f"{_FOLDER}/{outbound_fakes.CRATE}"


def _reorganised(installed, **kwargs) -> Path:
    """Write the export again as rekordbox would after a reorganisation."""
    path = _export(installed, **kwargs)
    source.forget_libraries()
    return path


def _moved_into_a_folder(installed, tracks=(1, 2, 3)) -> Path:
    return _reorganised(
        installed,
        crate_name=None,
        extra_children=outbound_fakes.nested_playlist(
            _FOLDER, outbound_fakes.CRATE, list(tracks)
        ),
    )


def _exported_once(queue, *indexes: int):
    account = fake(*(indexes or (1, 2, 3)))
    assert _resume(queue(account))[0] == int(ExitCode.OK)
    assert account.created == [outbound_fakes.CRATE]
    return account


def _shown_playlist(verb: list[str]) -> dict:
    refused = _asked(verb)
    return refused["cause"]["detail"]["shown"]["remote_playlist"]


def _ledger_playlists(installed) -> dict:
    import json
    path = config.state_path("outbound_writes", installed)
    return json.loads(path.read_text(encoding="utf-8"))["playlists"]


def test_a_crate_dragged_into_a_folder_updates_its_remote_playlist(installed, queue):
    """R-229's measured cost, driven through the verb: one crate, two playlists."""
    account = _exported_once(queue)
    account.catalog.update(catalog(4))
    moved = _reorganised(
        installed,
        crate_name=None,
        tracks=4,
        extra_children=outbound_fakes.nested_playlist(
            _FOLDER, outbound_fakes.CRATE, [1, 2, 3, 4]
        ),
    )
    job_id = queue(verb=export_verb(moved, _MOVED))
    resumed = _done(job_id)
    assert account.created == [outbound_fakes.CRATE]
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-2", "tid-3", "tid-4")
    assert resumed["data"]["progress"]["outbound"]["added"] == ["tid-4"]
    reports = artifacts.committed(installed, job_id)
    # ONE MOVE PER JOB, reported by the item that made it and by no other.
    assert [report["adopted_from"] for report in reports] == [outbound_fakes.CRATE, "", "", ""]
    assert {report["remote_id"] for report in reports} == {"pl-1"}
    recorded = _ledger_playlists(installed)
    assert list(recorded) == [_MOVED]
    assert recorded[_MOVED]["formerly"] == [outbound_fakes.CRATE]
    assert recorded[_MOVED]["tracks"] == ["1", "2", "3", "4"]


def test_a_renamed_crate_updates_its_remote_playlist(installed, queue):
    """A rename changes the display name too, so only the tracks can say it."""
    account = _exported_once(queue)
    renamed = _reorganised(installed, crate_name="Peak Time")
    _done(queue(verb=export_verb(renamed, "Peak Time")))
    assert account.created == [outbound_fakes.CRATE]
    assert list(_ledger_playlists(installed)) == ["Peak Time"]


def test_the_gate_and_the_envelope_both_say_which_playlist_is_adopted(installed, queue):
    """A refusal carries no warnings, so the gate has to say it as well."""
    _exported_once(queue)
    moved = _moved_into_a_folder(installed)
    shown = _shown_playlist(export_verb(moved, _MOVED))
    assert shown["action"] == export_cli.ACTION_ADOPT
    assert shown["remote_id"] == "pl-1"
    assert shown["recorded_as"] == outbound_fakes.CRATE
    assert "--new-playlist" in shown["warning"]
    # THE EVIDENCE NAMES BOTH SIDES, the record's size and the crate's.
    assert "from 3 track(s), 3 of them among the 3 this playlist holds" in shown["warning"]
    run_id, _job = approve_and_queue(export_verb(moved, _MOVED), _GATE)
    # THE SAME RUN AGAIN, which the recorded decision still answers.
    code, queued = drive(["--run", run_id, *export_verb(moved, _MOVED)])
    assert code == int(ExitCode.OK), queued
    codes = [warning["code"] for warning in queued["warnings"]]
    assert "outbound-playlist-adopted" in codes


def test_the_gate_says_create_and_update_when_nothing_is_adopted(exported, queue):
    """The block is shown every time, so its absence never means create."""
    first = _shown_playlist(export_verb(exported))
    assert first == {"action": export_cli.ACTION_CREATE, "remote_id": None}
    _exported_once(queue)
    again = _shown_playlist(export_verb(exported))
    assert again == {"action": export_cli.ACTION_UPDATE, "remote_id": "pl-1"}


def test_a_crate_the_export_still_carries_is_never_adopted_from(installed, queue):
    """Two crates sharing every track is an ordinary library, not a rename."""
    account = _exported_once(queue)
    both = _reorganised(
        installed,
        extra_children=outbound_fakes.nested_playlist(
            _FOLDER, outbound_fakes.CRATE, [1, 2, 3]
        ),
    )
    assert _shown_playlist(export_verb(both, _MOVED))["action"] == export_cli.ACTION_CREATE
    _done(queue(verb=export_verb(both, _MOVED)))
    assert account.created == [outbound_fakes.CRATE, outbound_fakes.CRATE]
    assert sorted(_ledger_playlists(installed)) == sorted([outbound_fakes.CRATE, _MOVED])


def test_new_playlist_declines_the_adoption_and_creates(installed, queue):
    """Without a way to decline, a wrong offer leaves the crate unexportable."""
    account = _exported_once(queue)
    moved = _moved_into_a_folder(installed)
    verb = [*export_verb(moved, _MOVED), "--new-playlist"]
    assert _shown_playlist(verb) == {"action": export_cli.ACTION_CREATE, "remote_id": None}
    _done(queue(verb=verb))
    assert account.created == [outbound_fakes.CRATE, outbound_fakes.CRATE]
    recorded = _ledger_playlists(installed)
    assert recorded[outbound_fakes.CRATE]["remote_id"] == "pl-1"
    assert recorded[_MOVED]["remote_id"] == "pl-2"


def test_a_confirmed_adoption_does_not_authorise_a_create(installed, queue):
    """The decision and the queue are two invocations, and the offer is digested."""
    _exported_once(queue)
    moved = _moved_into_a_folder(installed)
    verb = export_verb(moved, _MOVED)
    refused = _asked(verb)
    run_id = refused["run_id"]
    option = refused["cause"]["detail"]["options"][0]
    assert drive(["run", "decide", run_id, _GATE, option, "--actor", "a-person"])[0] == 0
    with jobs.open_store() as store:
        before = len(jobs.list_jobs(store))
    code, stale = drive(["--run", run_id, *verb, "--new-playlist"])
    assert code != int(ExitCode.OK), stale
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == before


def test_an_export_that_adopts_nothing_digests_as_it_always_did():
    """A job frozen before the key existed must still resume (``DecisionStale``)."""
    plain = export_cli.confirm_digest("crate", "/x/collection.xml", ["1", "2"])
    assert export_cli.confirm_digest("crate", "/x/collection.xml", ["1", "2"], adopts="") == plain
    assert export_cli.confirm_digest(
        "crate", "/x/collection.xml", ["1", "2"], adopts="old"
    ) != plain
    assert export_cli._frozen_adoption({}) == {"adopts": ""}
    assert export_cli._frozen_adoption({export_cli.ADOPTS: "old"}) == {"adopts": "old"}


def test_two_orphaned_records_that_could_each_be_it_adopt_neither(installed, queue):
    """Two candidates is reported as two, never settled by a rule nobody chose."""
    account = _exported_once(queue)
    second = _reorganised(installed, crate_name="Second")
    job_id = queue(verb=[*export_verb(second, "Second"), "--new-playlist"])
    _done(job_id)
    assert account.created == [outbound_fakes.CRATE, "Second"]
    third = _reorganised(installed, crate_name="Third")
    shown = _shown_playlist(export_verb(third, "Third"))
    assert shown["action"] == export_cli.ACTION_CREATE
    assert outbound_fakes.CRATE in shown["warning"]
    assert "Second" in shown["warning"]
    job_id = queue(verb=export_verb(third, "Third"))
    code, _resumed = _resume(job_id)
    assert code == int(ExitCode.OK)
    assert account.created == [outbound_fakes.CRATE, "Second", "Third"]
    assert sorted(_ledger_playlists(installed)) == ["Second", "Third", outbound_fakes.CRATE]


def test_two_crates_offered_one_orphan_do_not_both_get_it(installed, queue):
    """Both gates said update. The second to run must not create instead."""
    account = _exported_once(queue)
    split = _reorganised(
        installed,
        crate_name=None,
        extra_children=[
            *outbound_fakes.nested_playlist("P", "One", [1, 2, 3]),
            *outbound_fakes.nested_playlist("Q", "Two", [1, 2, 3]),
        ],
    )
    first = queue(verb=export_verb(split, "P/One"))
    second = queue(verb=export_verb(split, "Q/Two"))
    _done(first)
    code, refused = _resume(second)
    assert code != int(ExitCode.OK), refused
    assert "outbound-record-moved" in str(refused)
    assert account.created == [outbound_fakes.CRATE]
    assert list(_ledger_playlists(installed)) == ["P/One"]


def test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing(installed, queue):
    """The old job froze the remote id it was confirmed to update, and finds it."""
    account = _exported_once(queue, 1, 2)
    account.catalog.update(catalog(3))
    old_job = queue()
    assert _job(old_job).payload[export_cli.REMOTE] == "pl-1"
    moved = _moved_into_a_folder(installed)
    new_job = queue(verb=export_verb(moved, _MOVED))
    account.catalog.pop("3")
    _done(new_job)
    assert list(_ledger_playlists(installed)) == [_MOVED]
    account.catalog.update(catalog(3))
    # The old job reads its frozen document path, so its document goes back first.
    _reorganised(installed)
    _done(old_job)
    assert account.created == [outbound_fakes.CRATE]
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-2", "tid-3")
    assert list(_ledger_playlists(installed)) == [_MOVED]


def test_a_path_reused_for_a_different_crate_is_said_at_the_gate(installed, queue):
    """The rename chain. The crate now at the old path is told whose playlist it is."""
    _exported_once(queue)
    chained = _reorganised(
        installed,
        tracks=6,
        crate=(4, 5, 6),
        extra_children=outbound_fakes.nested_playlist(_FOLDER, "Archive", [1, 2, 3]),
    )
    reused = _shown_playlist(export_verb(chained))
    assert reused["action"] == export_cli.ACTION_UPDATE
    assert reused["remote_id"] == "pl-1"
    assert f"{_FOLDER}/Archive" in reused["warning"]
    assert "exporting that one first" in reused["warning"]
    renamed_away = _shown_playlist(export_verb(chained, f"{_FOLDER}/Archive"))
    assert renamed_away["action"] == export_cli.ACTION_ADOPT
    assert renamed_away["recorded_as"] == outbound_fakes.CRATE


def test_new_playlist_does_not_hide_a_record_the_crate_already_has(exported, queue):
    """The flag declines an offer. It does not make the gate say create falsely."""
    _exported_once(queue)
    shown = _shown_playlist([*export_verb(exported), "--new-playlist"])
    assert shown == {"action": export_cli.ACTION_UPDATE, "remote_id": "pl-1"}


# R-693: the queued resume's gate shows the frozen plan it asks about


def test_the_resume_gate_shows_the_frozen_tracks_the_digest_covers(exported, queue):
    """R-693: the resume's gate shows every frozen track, off the payload only."""
    job_id = queue(fake(1, 2, 3))
    payload = _job(job_id).payload
    refused = _asked([*export_verb(exported), "--job", job_id])
    detail = refused["cause"]["detail"]
    assert detail["gate"] == "export.playlist.confirm"
    shown = detail["shown"]
    tracks = [str(track) for track in payload[shell_module.TRACKS]]
    assert shown["items"] == tracks == ["1", "2", "3"]
    assert shown["count"] == 3
    assert shown[shell_module.PLAYLIST] == payload[shell_module.PLAYLIST] == outbound_fakes.CRATE
    assert shown[shell_module.EXPORT_PATH] == payload[shell_module.EXPORT] == str(exported)
    assert shown["adopts"] == str(payload.get(export_cli.ADOPTS) or "")
    # THE EXPORTS FOLDER DECISION IS FROZEN, SHOWN AND DIGESTED (U131).
    assert shown[export_cli.FILING] == payload[export_cli.FILING] == "Exports:create:"
    assert shown["digest"] == export_cli.confirm_digest(
        shown[shell_module.PLAYLIST],
        shown[shell_module.EXPORT_PATH],
        tracks,
        adopts=shown["adopts"],
        filing=shown[export_cli.FILING],
    )
    assert shell_module.EXPORT not in shown, "the resume reads nothing off the export document"
    assert _job(job_id).state is jobs.JobState.QUEUED


def test_the_export_gate_shows_the_tracks_the_digest_covers_beside_the_age(
    installed, exported, monkeypatch
):
    """R-693: the first ask lists every track the digest covers beside the age."""
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    refused = _asked(export_verb(exported))
    shown = refused["cause"]["detail"]["shown"]
    assert shown["items"] == ["1", "2", "3"]
    assert shown["count"] == 3
    assert shown[shell_module.PLAYLIST] == outbound_fakes.CRATE
    assert shown[shell_module.EXPORT_PATH] == str(exported)
    assert shown[export_cli.ADOPTS] == ""
    assert shown[export_cli.FILING] == "Exports:create:"
    assert shown["digest"] == export_cli.confirm_digest(
        outbound_fakes.CRATE, str(exported), ["1", "2", "3"], adopts="", filing="Exports:create:"
    )
    assert shown["export"]["file"] == exported.name
    assert shown["export"]["freshness"] == "within-limit"
    assert shown["remote_playlist"]["action"] == export_cli.ACTION_CREATE


def test_the_favorites_gate_shows_the_tracks_the_digest_covers_beside_the_age(exported):
    refused = _asked(favorites_verb(exported))
    shown = refused["cause"]["detail"]["shown"]
    _exported, resolved = favorites_cli.resolve_sweep(str(exported), None)
    assert shown["items"] == list(resolved.track_ids)
    assert shown["items"], "a sweep over no favourites proves nothing about the screen"
    assert shown["count"] == len(resolved.track_ids)
    assert shown[shell_module.PLAYLIST] == resolved.key
    assert shown[shell_module.EXPORT_PATH] == str(exported)
    assert shown["digest"] == favorites_cli.sweep_digest(exported, resolved)
    assert shown["export"]["file"] == exported.name


@pytest.mark.parametrize(
    "counts, said",
    [
        ({"written": 2, "already": 1, "unmatched": 1}, "1 of the 4 track(s)"),
        ({"written": 2, "already": True, "unmatched": 1}, "1 of the 3 track(s)"),
        ({"written": 2, "already": 0, "unmatched": True}, None),
        ({"written": 2, "already": 0, "unmatched": 0}, None),
        ({"written": 2}, None),
        ({}, None),
    ],
    ids=["one-left-out", "bool-is-no-count", "bool-unmatched", "none-left-out", "no-key", "empty"],
)
def test_the_unmatched_warning_reads_only_whole_counts(counts, said):
    warned = export_cli.concluded({"counts": counts})
    if said is None:
        assert warned == ()
    else:
        (warning,) = warned
        assert warning["code"] == export_cli.UNMATCHED_WARNING
        assert said in warning["message"]


def test_the_files_album_is_read_beside_its_isrc_in_one_read(installed, tmp_path):
    """R-572: the album tag rides with the ISRC, stripped, and is empty when absent."""
    root = Path(installed.library.root)
    tagged = _tagged(tmp_path / "a", root / "Music" / "a.flac", "ZZX9A2600042")
    assert tags.write_tags(tagged, {"album": "  Tidal Lines "}) is True
    bare = _tagged(tmp_path / "b", root / "Music" / "b.flac", "ZZX9A2600043")
    found = source.file_identity(_entry(locations.location_url(tagged)), root=root, prefix_map=[])
    assert found == source.FileIdentity(isrc="ZZX9A2600042", album="Tidal Lines")
    assert source.file_identity(
        _entry(locations.location_url(bare)), root=root, prefix_map=[]
    ) == source.FileIdentity(isrc="ZZX9A2600043", album="")
    gone = locations.location_url(root / "Music" / "gone.flac")
    assert source.file_identity(_entry(gone), root=root, prefix_map=[]) == source.FileIdentity()

def test_local_tracks_carries_the_files_album_to_the_export_plan(installed, tmp_path):
    """R-572. local_tracks hands the album through so export.plan can pass it on."""
    root = Path(installed.library.root)
    one = _tagged(tmp_path / "one", root / "Music" / "1.flac", "ZZX9A2600042")
    assert tags.write_tags(one, {"album": "  Tidal Lines "}) is True
    two = _tagged(tmp_path / "two", root / "Music" / "2.flac", "ZZX9A2600043")
    exported = outbound_fakes.write_export(
        root / "outbound-album",
        locations={
            1: locations.location_url(one),
            2: locations.location_url(two),
        },
    )
    source.forget_libraries()
    library = source.read_library(exported)
    tracks = source.local_tracks(library, ("1", "2"), cfg=installed)
    assert [(t.identity, t.isrc, t.album) for t in tracks] == [
        ("1", "ZZX9A2600042", "Tidal Lines"),
        ("2", "ZZX9A2600043", ""),
    ]
    source.forget_libraries()



# U131: a playlist export playlist creates is filed in Exports, on its gate


def test_a_created_playlist_is_filed_in_exports_as_its_gate_showed(queue):
    account = fake(1, 2, 3)
    resumed = _done(queue(account))
    assert _codes(resumed) == []
    assert account.folders_created == ["Exports"]
    assert account.moves == [("pl-1", "folder-1")]
    assert resumed["data"]["progress"]["outbound"]["unfiled"] == []


def test_a_changed_exports_folder_makes_the_old_answer_stale(exported, monkeypatch):
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3))
    bind(monkeypatch, account)
    refused = _asked(export_verb(exported))
    detail = refused["cause"]["detail"]
    assert detail["shown"][export_cli.FILING] == "Exports:create:"
    _decided(refused)
    # A person makes an Exports folder on the account between the ask and the answer.
    account.create_folder("Exports")
    code, other = drive(["--run", refused["run_id"], *export_verb(exported)])
    assert code != int(ExitCode.OK), other
    assert other["cause"]["reason"] == "decision-stale"
    assert _queue_is_empty()


def test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning(queue):
    account = fake(1, 2, 3)
    job_id = queue(account)
    account.create_folder("Exports")
    resumed = _done(job_id)
    assert resumed["outcome"] == "ok"
    assert _codes(resumed) == [export_cli.UNFILED_WARNING]
    (warning,) = resumed["warnings"]
    assert "Exports:create: then, Exports:adopt:folder-1 now" in warning["message"]
    assert account.moves == []
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-2", "tid-3")


def test_a_filing_failure_is_a_warning_on_a_finished_export(monkeypatch, queue):
    from cratekit.modules.outbound import kinds
    account = fake(1, 2, 3)
    job_id = queue(account)

    def broken(*_args, **_kwargs):
        raise OSError("ledger write failed")

    monkeypatch.setattr(kinds, "reserve", broken)
    resumed = _done(job_id)
    assert resumed["outcome"] == "ok"
    assert _codes(resumed) == [export_cli.UNFILED_WARNING]
    (warning,) = resumed["warnings"]
    assert "OSError: ledger write failed" in warning["message"]
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-2", "tid-3")
    assert account.moves == []
