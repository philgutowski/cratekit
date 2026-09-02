"""U51: the two outbound verbs run for real, driven end to end through the queue.

WHAT THIS FILE GUARDS THAT THE ENGINE'S OWN SUITE CANNOT. ``tests/modules/test_outbound.py``
proves ``export.apply`` and ``hearts.heart_back`` keep their promises when called
directly, and it has always passed, because until this unit NOTHING IN ``src``
called either one. A green run of that file said nothing about whether the
product ever wrote a playlist or a heart. This file is about the binding: that a
confirmed export queues its tracks, that a driver claims them, that the engine's
report survives a kill as a committed artifact, that a person is told about the
tracks the provider could not match, and that no path through either shell can
reach a remove.

THE PROVIDER IS ALWAYS A STAND IN. A live streaming account is attended work and
is R-144's remaining half; every drive here goes through
``modules.outbound.account.resolve``, substituted on the module attribute. The
one thing that is NOT substituted is the path under test: the real dispatcher,
the real gate flow, the real queue, the real driver, and the real engines.

THE POPULATION IS DERIVED WHERE IT CAN BE. The two verbs' handler keys are read
off the registry rather than spelled, so a rename fails here rather than leaving
a guard pointed at a key nothing uses.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.cli import handlers, registry
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.export import cli as export_cli
from cratekit.favorites import cli as favorites_cli
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import artifacts, source
from tests import outbound_fakes
from tests.cli_drive import approve_and_queue, drive
from tests.test_config import valid_data

EXPORT_KEY = "export.playlist"
FAVORITES_KEY = "sync.favorites"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


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
    return outbound_fakes.write_export(installed.library.root / "outbound")


def bind(monkeypatch, account) -> None:
    """Put ``account`` in front of the provider seam for this test."""
    monkeypatch.setattr(
        account_module, "resolve", outbound_fakes.account_factory(account)
    )


def catalog(*indexes: int) -> dict[str, str]:
    return {str(index): f"tid-{index}" for index in indexes}


def export_verb(exported: Path, playlist: str = outbound_fakes.CRATE) -> list[str]:
    return ["export", "playlist", playlist, "--export", str(exported)]


def favorites_verb(exported: Path, playlist: str | None = None) -> list[str]:
    verb = ["sync", "favorites", "--export", str(exported)]
    if playlist is not None:
        verb += ["--favorites-playlist", playlist]
    return verb


# ═══════════════════════════════════════════════════════════════════════════
# 1. The binding itself
# ═══════════════════════════════════════════════════════════════════════════


def test_both_verbs_report_a_bound_worker_rather_than_a_reason_they_have_none():
    """``crate job show``'s worker field, at the source it is derived from.

    Asked through ``handlers`` rather than through the verb, because the field is
    answered WITHOUT importing the feature module (KTD26) and driving the verb
    would import it and prove nothing about that property.
    """
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


def test_job_show_reports_the_bound_worker_for_a_queued_export(
    installed, exported, monkeypatch
):
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    code, shown = drive(["job", "show", job_id])
    assert code == int(ExitCode.OK), shown
    assert shown["data"]["progress"]["worker"] == "bound"
    assert shown["data"]["progress"]["worker_reason"] is None


# ═══════════════════════════════════════════════════════════════════════════
# 2. The zero item rule: neither verb can queue empty work
# ═══════════════════════════════════════════════════════════════════════════


def _queue_is_empty() -> bool:
    with jobs.open_store() as store:
        return not jobs.list_jobs(store)


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


def test_an_export_naming_a_playlist_the_document_lacks_queues_nothing(
    installed, exported
):
    del installed
    code, refused = drive(export_verb(exported, "no-such-crate"))
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "export-playlist-unknown"
    assert _queue_is_empty()


def test_a_name_that_is_a_folder_refuses_rather_than_resolving(installed):
    """The live library's ``Favorites`` shape, which is why the default is its child.

    A folder holds nodes rather than tracks, so it never reaches
    ``LibraryView.playlists``. Driven because a default naming a folder would
    have refused on every real run while every fixture stayed green.
    """
    path = outbound_fakes.write_export(
        installed.library.root / "outbound",
        extra_children=outbound_fakes.folder_only("Favorites"),
    )
    code, refused = drive(favorites_verb(path, "Favorites"))
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "export-playlist-unknown"
    assert _queue_is_empty()


def test_an_empty_playlist_refuses_distinguishably_from_an_absent_one(installed):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=()
    )
    code, refused = drive(favorites_verb(path))
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "export-playlist-empty"
    assert refused["cause"]["reason"] != "export-playlist-unknown"
    assert _queue_is_empty()


def _two_playlists_called(name: str) -> list[str]:
    """The same display name in two folders, which is a real per-year tree shape.

    A top-level playlist of that name would NOT be ambiguous: the resolver
    matches a full display path first, and a top-level playlist's path IS its
    name. The ambiguity only exists between two nested nodes, which is why the
    fixture nests both.
    """
    return [
        *outbound_fakes.nested_playlist("Crates", name, [1]),
        *outbound_fakes.nested_playlist("Archive", name, [2]),
    ]


def test_a_name_two_playlists_carry_refuses_and_names_both_paths(installed):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", extra_children=_two_playlists_called("2026")
    )
    code, refused = drive(export_verb(path, "2026"))
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "export-playlist-ambiguous"
    assert sorted(refused["cause"]["detail"]["paths"]) == ["Archive/2026", "Crates/2026"]
    assert _queue_is_empty()


def test_the_full_path_disambiguates_what_the_bare_name_could_not(installed):
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", extra_children=_two_playlists_called("2026")
    )
    resolved = source.resolve(source.read_library(path), "Crates/2026")
    assert resolved.key == "Crates/2026"
    assert resolved.track_ids == ("1",)


def test_a_top_level_playlist_wins_over_a_nested_one_of_the_same_name(installed):
    """The exact-path rule, driven, so it is a decision rather than an accident."""
    path = outbound_fakes.write_export(
        installed.library.root / "outbound",
        extra_children=outbound_fakes.nested_playlist(
            "Crates", outbound_fakes.CRATE, [1]
        ),
    )
    resolved = source.resolve(source.read_library(path), outbound_fakes.CRATE)
    assert resolved.key == outbound_fakes.CRATE
    assert resolved.track_ids == ("1", "2", "3")


def test_a_dangling_track_id_is_reported_and_not_queued(installed):
    """R-146 input, driven. The reader accepts it, so this is reachable."""
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", crate=(1, 2, 99), tracks=2
    )
    resolved = source.resolve(source.read_library(path), outbound_fakes.CRATE)
    assert resolved.track_ids == ("1", "2")
    assert resolved.dangling == ("99",)


def test_a_repeated_track_id_becomes_one_item(installed):
    """``job_items`` is keyed on (job_id, item_id), so a repeat would be an
    IntegrityError reaching a person as ``internal-error`` over a document the
    reader accepted."""
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", crate=(1, 2, 1)
    )
    resolved = source.resolve(source.read_library(path), outbound_fakes.CRATE)
    assert resolved.track_ids == ("1", "2")
    assert resolved.repeated == ("1",)


def test_a_queued_export_holds_one_item_per_track(installed, exported, monkeypatch):
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, job_id)] == ["1", "2", "3"]


# ═══════════════════════════════════════════════════════════════════════════
# 3. The export worker runs
# ═══════════════════════════════════════════════════════════════════════════


def _resume(job_id: str) -> tuple[int, dict]:
    """Drive the resume the job engine would spawn, in THIS process.

    ``argv_for`` is the real builder and the argv is the real one, which is what
    makes this a drive of the shipped resume rather than of a list. The only
    thing not reproduced is the detachment, and it cannot be: a spawned child is
    a fresh process and inherits no substituted provider.
    """
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    return drive(cli_jobs.argv_for(job))


def _drive_job(job_id: str, exported: Path) -> tuple[int, dict]:
    """The same resume, for a job that was just re-armed by ``jobs.retry``."""
    del exported
    return _resume(job_id)


def test_an_export_runs_pending_to_done_and_its_artifact_reads_back(
    installed, exported, monkeypatch
):
    """The whole point of the unit, driven through the real resume path.

    The artifact is READ BACK AND CHECKED FOR SHAPE rather than for existence: a
    file that exists and says nothing is exactly what a handler that reported
    success over work it never did would leave behind.
    """
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3))
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")

    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
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


def test_a_second_export_of_the_same_playlist_adds_nothing_and_creates_nothing(
    installed, exported, monkeypatch
):
    del installed
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3))
    bind(monkeypatch, account)
    _run, first = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    assert _resume(first)[0] == int(ExitCode.OK)

    _run, second = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    code, resumed = _resume(second)
    assert code == int(ExitCode.OK), resumed
    assert account.created == [outbound_fakes.CRATE]
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-2", "tid-3")
    assert resumed["data"]["outbound"]["added"] == []
    assert sorted(resumed["data"]["outbound"]["already"]) == [
        "tid-1",
        "tid-2",
        "tid-3",
    ]


def test_the_envelope_names_the_tracks_the_provider_could_not_match(
    installed, exported, monkeypatch
):
    """Without this a person sees three of three items done and is told nothing.

    ``export.apply``'s docstring promises unmatched tracks are reported and never
    dropped silently, and until the envelope carried them that promise held only
    for whoever opened the JSON under the queue root.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(2)))
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["outbound"]["added"] == ["tid-2"]
    assert sorted(resumed["data"]["outbound"]["unmatched"]) == ["1", "3"], (
        "the envelope must name the library identity of each unmatched row, not "
        "a stringified mapping nothing downstream can key on"
    )


def test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it(
    installed, exported, monkeypatch
):
    """The engine's resume guarantee, through the binding rather than beside it."""
    del installed
    account = outbound_fakes.FakeAccount(
        catalog=catalog(1, 2, 3), fail_on={"tid-2"}
    )
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")

    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    with jobs.open_store() as store:
        states = {item.item_id: str(item.state) for item in jobs.items(store, job_id)}
    assert states["1"] == str(jobs.ItemState.DONE)
    assert states["2"] == str(jobs.ItemState.FAILED)
    assert states["3"] == str(jobs.ItemState.DONE)

    # RE-ARMED IN PROCESS RATHER THAN THROUGH ``crate job resume``, which spawns
    # a DETACHED child. That child is a fresh process and inherits no
    # monkeypatch, so it would meet the real provider seam and fail every item.
    # ``jobs.retry`` is the same re-arming that verb performs, and the claim
    # under test is the driver's, not the spawner's.
    account.fail_on = frozenset()
    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    assert _drive_job(job_id, exported)[0] == int(ExitCode.OK)
    with jobs.open_store() as store:
        after = {item.item_id: str(item.state) for item in jobs.items(store, job_id)}
    assert after["2"] == str(jobs.ItemState.DONE)
    # The two that already succeeded were not written a second time.
    assert account.added.count(("pl-1", "tid-1")) == 1
    assert account.added.count(("pl-1", "tid-3")) == 1


def test_the_resume_of_a_half_failed_export_does_not_exit_ok(
    installed, exported, monkeypatch
):
    """R-225, pinned where the branch was written rather than inherited.

    ``master/cli.py``'s resume branch reports a half failed job through a normal
    envelope and exits OK, so a person whose export wrote nothing is told it
    finished. Copying that branch is what this asserts did not happen.
    """
    del installed
    bind(
        monkeypatch,
        outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3), fail_on={"tid-2"}),
    )
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK)
    assert resumed["cause"] is not None
    assert resumed["cause"]["reason"] != "internal-error"
    assert resumed["data"] is None or resumed["data"].get("state") != str(
        jobs.JobState.SUCCEEDED
    )


# ═══════════════════════════════════════════════════════════════════════════
# 4. The favourites sweep runs, add only
# ═══════════════════════════════════════════════════════════════════════════


def test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row(
    installed, exported, monkeypatch
):
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2))
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert sorted(account.hearted) == ["tid-1", "tid-2"]
    reports = artifacts.committed(installed, job_id)
    assert [report["row"] for report in reports] == ["1", "2"]


def test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written(
    installed, exported, monkeypatch
):
    """The add-only property under the condition that would expose a re-write."""
    del installed
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2), hearts={"tid-1"})
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    assert account.hearted == ["tid-2"]
    assert resumed["data"]["outbound"]["hearted"] == ["tid-2"]
    assert resumed["data"]["outbound"]["already"] == ["tid-1"]


def test_a_second_sweep_writes_nothing_because_the_ledger_remembers(
    installed, exported, monkeypatch
):
    """The ledger short circuit, reached without asking the provider at all."""
    del installed
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2))
    bind(monkeypatch, account)
    _run, first = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    assert _resume(first)[0] == int(ExitCode.OK)
    assert sorted(account.hearted) == ["tid-1", "tid-2"]

    _run, second = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    assert _resume(second)[0] == int(ExitCode.OK)
    assert sorted(account.hearted) == ["tid-1", "tid-2"]


def test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item(
    installed, exported, monkeypatch
):
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1)))
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["progress"]["counts"]["done"] == 2
    assert resumed["data"]["outbound"]["unmatched"] == ["2"]


def test_the_sweep_reaches_nothing_outside_the_add_only_protocol(
    installed, exported, monkeypatch
):
    """An absence proves nothing; this raises on any attribute outside the protocol.

    The add-only promise (R36) rests on ``RemoteAccount`` declaring no remove, so
    the assertion worth making is that no code path in the shell or the engine
    can even NAME one, rather than that a particular run did not.
    """
    del installed
    bind(monkeypatch, outbound_fakes.StrictAccount(catalog=catalog(1, 2)))
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    assert _resume(job_id)[0] == int(ExitCode.OK)


def test_no_colour_writer_reaches_the_engine_from_a_queued_sweep(
    installed, exported, monkeypatch
):
    """``colors=None``, asserted at the engine boundary rather than in prose.

    Colouring a library row is a write to the live rekordbox database and belongs
    behind the guarded write session, so a queued sweep must not carry one.
    """
    del installed
    seen: list[object] = []
    real = favorites_cli.hearts.heart_back

    def watched(cfg, remote, candidates, *, colors=None, flags=None):
        seen.append((colors, flags))
        return real(cfg, remote, candidates, colors=colors, flags=flags)

    monkeypatch.setattr(favorites_cli.hearts, "heart_back", watched)
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    assert _resume(job_id)[0] == int(ExitCode.OK)
    assert seen and all(colors is None for colors, _flags in seen)


def test_the_resume_of_a_half_failed_sweep_does_not_exit_ok(
    installed, exported, monkeypatch
):
    del installed
    bind(
        monkeypatch,
        outbound_fakes.FakeAccount(catalog=catalog(1, 2), fail_on={"tid-2"}),
    )
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK)
    assert resumed["cause"] is not None


# ═══════════════════════════════════════════════════════════════════════════
# 5. The provider seam, and what a person is told before they confirm
# ═══════════════════════════════════════════════════════════════════════════


def test_with_no_credential_the_seam_refuses_with_the_credential_cause(installed):
    """Distinguishable from the no-adapter refusal, because doctor can fix one."""
    with pytest.raises(CratekitError) as excinfo:
        account_module.resolve(installed)
    assert excinfo.value.cause.reason == "credential-missing"
    assert excinfo.value.cause.code is not ExitCode.INTERNAL


def test_with_a_credential_stored_the_seam_refuses_that_no_adapter_is_bound(
    installed, monkeypatch
):
    from cratekit.core import secrets

    monkeypatch.setattr(secrets, "exists", lambda name: True)
    with pytest.raises(CratekitError) as excinfo:
        account_module.resolve(installed)
    assert excinfo.value.cause.reason == "outbound-account-unbound"
    assert excinfo.value.cause.code is not ExitCode.INTERNAL
    assert excinfo.value.cause.remediation is not None


def test_the_queued_envelope_warns_that_no_provider_adapter_is_bound(
    installed, exported
):
    """Told at the moment it is still actionable, not after the job has failed."""
    del installed
    assert account_module.bound() is False
    code, refused = drive(export_verb(exported))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    decided, _ = drive(
        [
            "run",
            "decide",
            refused["run_id"],
            detail["gate"],
            detail["options"][0],
            "--actor",
            "a-person",
        ]
    )
    assert decided == int(ExitCode.OK)
    code, queued = drive(["--run", refused["run_id"], *export_verb(exported)])
    assert code == int(ExitCode.OK), queued
    codes = {warning["code"] for warning in queued.get("warnings") or ()}
    assert "outbound-account-unbound" in codes


def test_a_job_driven_with_no_adapter_fails_rather_than_reporting_success(
    installed, exported
):
    """What this build actually delivers on a machine with nothing bound.

    Before this unit the job stayed pending for ever and said nothing. It now
    ends with a named cause, which is a smaller thing than a working export and
    is the honest one.
    """
    del installed
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK)
    # ``no-evidence`` is the engine's verdict when every item failed, and the
    # provider seam's own cause rides on the ITEMS. Asserted at both altitudes,
    # because a person reads the first and a maintainer needs the second.
    assert resumed["cause"]["reason"] == "no-evidence"
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.FAILED
        reasons = {
            item.cause.reason
            for item in jobs.items(store, job_id)
            if item.cause is not None
        }
    assert reasons <= {"credential-missing", "outbound-account-unbound"}
    assert reasons


# ═══════════════════════════════════════════════════════════════════════════
# 6. The confirm digest, and the frozen configuration
# ═══════════════════════════════════════════════════════════════════════════


def test_a_confirm_recorded_against_one_document_does_not_authorise_another(
    installed, monkeypatch
):
    """The reason the digest grew to cover the export path.

    Before this, ``export.playlist``'s digest was built from the playlist name
    alone, so an approval of ``crate-export`` in one collection authorised a
    write built from a different collection with a different track set, to
    somebody's streaming account.
    """
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    first = outbound_fakes.write_export(installed.library.root / "one")
    second = outbound_fakes.write_export(installed.library.root / "two", crate=(1,))

    code, refused = drive(export_verb(first))
    assert code == int(ExitCode.DECISION_REQUIRED)
    detail = refused["cause"]["detail"]
    assert (
        drive(
            [
                "run",
                "decide",
                refused["run_id"],
                detail["gate"],
                detail["options"][0],
                "--actor",
                "a-person",
            ]
        )[0]
        == int(ExitCode.OK)
    )
    code, other = drive(["--run", refused["run_id"], *export_verb(second)])
    assert code != int(ExitCode.OK), other
    assert other["cause"]["reason"] == "decision-stale"
    assert _queue_is_empty()


def test_a_relative_export_argument_still_resumes(
    installed, exported, monkeypatch, tmp_path
):
    """The other half of the digest decision, and the one that would strand a job.

    The resumed child rebuilds ``--export`` from the frozen ABSOLUTE path. If the
    digest were taken over what the person typed, a relative argument would
    produce a different digest on every respawn and the confirmed job could never
    advance, which is the defect
    ``an-explicit-gate-makes-a-queued-job-undriveable-without-the-run-id``
    records in another shape.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    monkeypatch.chdir(exported.parent)
    relative = ["export", "playlist", outbound_fakes.CRATE, "--export", exported.name]
    _run, job_id = approve_and_queue(relative, "export.playlist.confirm")
    with jobs.open_store() as store:
        assert Path(jobs.get(store, job_id).payload["export"]).is_absolute()
    assert _resume(job_id)[0] == int(ExitCode.OK)


def test_the_handler_runs_against_the_frozen_configuration_not_the_current_one(
    installed, exported, monkeypatch
):
    """KTD9, asserted on a key NO environment variable overrides.

    ``tests/conftest.py`` sets ``CRATEKIT_LIBRARY_ROOT`` for the whole suite and
    ``jobs.frozen_config`` rebuilds through ``config.from_dict``, which reapplies
    environment overrides, so moving the library root between enqueue and drive
    proves nothing: the frozen copy and the live one would agree.
    ``reports.intake_stale_days`` has no override, which is what makes the two
    copies genuinely able to differ. Recorded in
    ``docs/solutions/workflow-issues/a-frozen-config-is-frozen-against-the-file-not-against-an-env-override.md``.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")

    current = config.load()
    # BOTH BANDS MOVE, because config validation refuses a stale day count above
    # the expired one: the bands would overlap and a grouping would be reported
    # as both. A test that edited one is a test that never reached the handler.
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
    real = export_cli.run_export_item

    def watched(payload, track_id, cfg, remote):
        seen.append(cfg.reports.intake_stale_days)
        return real(payload, track_id, cfg, remote)

    monkeypatch.setattr(export_cli, "run_export_item", watched)
    assert _resume(job_id)[0] == int(ExitCode.OK)
    assert seen and all(days != 99 for days in seen), (
        "the handler saw the CURRENT configuration, not the one its job froze"
    )


# ═══════════════════════════════════════════════════════════════════════════
# 7. First-caller failure paths through the engines
# ═══════════════════════════════════════════════════════════════════════════


def test_an_item_whose_track_left_the_export_refuses_rather_than_writing_nothing(
    installed, exported, monkeypatch
):
    """A regenerated document under a queued job, driven.

    Reported as a refusal rather than skipped, because an item that reports done
    having written nothing is the clean-report-over-unreadable-state cost METHOD
    names, and the person's remedy is a fresh export rather than another resume.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    exported.write_bytes(outbound_fakes.export_document(crate=(1,), tracks=1))
    source.forget_libraries()

    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    with jobs.open_store() as store:
        failed = [
            item
            for item in jobs.items(store, job_id)
            if item.state is jobs.ItemState.FAILED
        ]
    assert {item.item_id for item in failed} == {"2", "3"}
    assert all(
        item.cause is not None and item.cause.reason == "outbound-item-absent"
        for item in failed
    )


def test_a_ledger_that_cannot_be_read_stops_the_write_rather_than_duplicating(
    installed, exported, monkeypatch
):
    """The engine's own refusal, reached through the binding for the first time.

    ``ledger._load`` refuses rather than treating an unreadable ledger as empty,
    because an empty reading would create a second remote playlist for a crate
    the account already has. Nothing in ``src`` had ever driven that path.
    """
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3))
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    ledger_path = config.state_path("outbound_writes", installed)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text("{not json", encoding="utf-8")

    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    assert account.created == []
    with jobs.open_store() as store:
        causes = {
            item.cause.reason
            for item in jobs.items(store, job_id)
            if item.cause is not None
        }
    assert causes == {"outbound-ledger-unusable"}


# ═══════════════════════════════════════════════════════════════════════════
# 8. The derivation's own properties
# ═══════════════════════════════════════════════════════════════════════════


def test_the_export_document_is_parsed_once_per_process(installed, monkeypatch):
    """The N times M shape ``coverage.py`` records this repository removing once."""
    path = outbound_fakes.write_export(installed.library.root / "outbound")
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
    del installed
    library = source.read_library(exported)
    resolved = source.resolve(library, outbound_fakes.CRATE)
    tracks = source.local_tracks(library, resolved.track_ids)
    candidates = source.heart_candidates(library, resolved.track_ids)
    assert [track.identity for track in tracks] == [c.row_id for c in candidates]
    assert all(track.isrc == "" for track in tracks), (
        "a collection export carries no ISRC; inventing one would hand the "
        "provider seam a fabricated identity"
    )
    assert all(track.title and track.artist for track in tracks)


def test_the_default_favourites_playlist_is_the_one_the_fixture_carries():
    """A default that drifted from the live library's shape is the whole point.

    The first draft of this unit defaulted to ``Favorites``, which is a FOLDER in
    the live library, so every real run would have refused while the suite stayed
    green on a fixture that named a playlist directly.
    """
    assert source.DEFAULT_FAVORITES_PLAYLIST == outbound_fakes.FAVORITES
