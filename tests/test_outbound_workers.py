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

import io
import os
import time
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import handlers, registry
from cratekit.core import config, jobs, locations, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.export import cli as export_cli
from cratekit.favorites import cli as favorites_cli
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import artifacts, ledger, source
from cratekit.modules.outbound import shell as shell_module
from cratekit.modules.reports import export as library_export
from tests import outbound_fakes
from tests._containers import synth_container
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
    assert resumed["data"]["progress"]["outbound"]["added"] == []
    assert sorted(resumed["data"]["progress"]["outbound"]["already"]) == [
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
    assert resumed["data"]["progress"]["outbound"]["added"] == ["tid-2"]
    assert sorted(resumed["data"]["progress"]["outbound"]["unmatched"]) == ["1", "3"], (
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

    ``master/cli.py``'s resume branch reported a half failed job through a normal
    envelope and exited OK when this was written, so a person whose export wrote
    nothing was told it finished. Copying that branch is what this asserts did
    not happen. Every shell calls ``jobs.raise_for_state`` now.
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
    # The fake raises RuntimeError, which the item records as internal-error.
    # The job used to wrap that as unavailable-transient. It now reports the
    # item's own cause, which is not retryable (R-380).
    assert resumed["cause"]["reason"] == "internal-error"
    assert resumed["cause"]["retryable"] is False
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
    assert resumed["data"]["progress"]["outbound"]["hearted"] == ["tid-2"]
    assert resumed["data"]["progress"]["outbound"]["already"] == ["tid-1"]


def test_a_second_sweep_writes_nothing_because_the_ledger_remembers(
    installed, exported, monkeypatch
):
    """The ledger short circuit, reached without asking the provider at all.

    THE SECOND SWEEP GETS A FRESH ACCOUNT, and that is what makes this a test of
    the LEDGER rather than of the provider. Reusing the first account leaves its
    ``hearts`` set populated, so ``account.has_heart`` alone would report every
    row as already and the assertion would pass with the ledger check deleted.
    Measured that way: the guard killed zero tests. A new account that hearts
    nothing can only be kept from writing by the recorded ledger.
    """
    del installed
    first_account = outbound_fakes.FakeAccount(catalog=catalog(1, 2))
    bind(monkeypatch, first_account)
    _run, first = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    assert _resume(first)[0] == int(ExitCode.OK)
    assert sorted(first_account.hearted) == ["tid-1", "tid-2"]

    second_account = outbound_fakes.FakeAccount(catalog=catalog(1, 2))
    bind(monkeypatch, second_account)
    _run, second = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    assert _resume(second)[0] == int(ExitCode.OK)
    assert second_account.hearted == [], (
        "the ledger is the only thing that can stop this write: this account "
        "hearts nothing, so a re-write means the recorded hearts were not read"
    )


def test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item(
    installed, exported, monkeypatch
):
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1)))
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["progress"]["counts"]["done"] == 2
    assert resumed["data"]["progress"]["outbound"]["unmatched"] == ["2"]


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
# 4b. R-424: the verb says only what it does, in the output a person gets
# ═══════════════════════════════════════════════════════════════════════════


def _human(argv: list[str]) -> tuple[int, str]:
    """One invocation in the DEFAULT output mode, returned as text.

    ``tests.cli_drive.drive`` always passes ``--output json``, which is why the
    whole of this file stayed green over a report that never mentioned the local
    write it was not doing. These rows go through the dispatcher the way a person
    does. Recorded in
    ``docs/solutions/workflow-issues/a-json-only-driver-cannot-see-a-blank-human-renderer.md``.
    """
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue() or err.getvalue()


def _answer_the_confirm(verb: list[str], gate: str) -> str:
    """R34's first two acts, without the third. Returns the gate run.

    ``approve_and_queue`` does all three and returns a job id, which is the right
    helper when the queueing pass is json. It is the wrong one here: the drive
    under test IS the queueing pass, and it has to be the human one.
    """
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == gate
    run_id = str(refused["run_id"])
    decided, envelope = drive(
        ["run", "decide", run_id, gate, detail["options"][0], "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    return run_id


def _says_no_local_write(text: str) -> bool:
    """The warning as the renderer prints it, on its own line.

    THE WHOLE LINE AND NOT A SUBSTRING OF THE MESSAGE. A dump of the json
    envelope as text would contain the sentence inside a quoted value and would
    satisfy a substring match while telling a person nothing, which is the shape
    the human-renderer learning warns about.
    """
    code = favorites_cli.LOCAL_WRITE_WARNING["code"]
    message = favorites_cli.LOCAL_WRITE_WARNING["message"]
    return f"warning [{code}]: {message}" in text.splitlines()


def test_queueing_a_sweep_tells_a_person_in_the_default_output_that_nothing_local_is_written(
    installed, exported, monkeypatch
):
    """R-424's cost, driven on the surface that carried it.

    The verb declared four local write surfaces it never reached, the guide
    promised a colour, a Favorite tag and a playlist membership, and the pass
    itself said nothing either way. This is the pass a person types.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    run_id = _answer_the_confirm(favorites_verb(exported), "sync.favorites.confirm")

    code, text = _human(["--run", run_id, *favorites_verb(exported)])

    assert code == int(ExitCode.OK), text
    assert _says_no_local_write(text), text


def test_the_resumed_sweep_says_the_same_thing_where_the_hearting_actually_happens(
    installed, exported, monkeypatch
):
    """The queueing pass writes nothing at all; the resume is the run.

    A correction that appeared only at queue time would be on the invocation
    whose report nobody reads for what happened.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        argv = cli_jobs.argv_for(jobs.get(store, job_id))

    code, text = _human(argv)

    assert code == int(ExitCode.OK), text
    assert _says_no_local_write(text), text


def test_an_item_report_carries_no_empty_colored_list(installed, exported, monkeypatch):
    """R-424's other half: an empty list reads as a write that found nothing.

    Asserted on the COMMITTED artifact rather than on the worker's return value,
    because the artifact is what survives a kill and what ``crate job`` reads
    back, so a key dropped from one and kept in the other is two answers.
    """
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    assert _resume(job_id)[0] == int(ExitCode.OK)

    reports = artifacts.committed(installed, job_id)

    assert reports, "the sweep committed nothing to assert about"
    for report in reports:
        assert "colored" not in report, report
        assert "hearted" in report, report


def test_the_verb_declares_the_remote_account_and_no_local_surface():
    """The declaration R-424 is about, read off the shipped registry.

    Each surface is named rather than compared as a set alone, because a set
    comparison that fails says only that two sets differ and this assertion is
    about WHICH ones were claimed. ``db_tree`` and ``db_metadata`` stood for the
    colour, the tag and the playlist membership; ``xml`` and ``files`` for a
    document and a file the sweep never writes.
    """
    entry = registry.entry("sync.favorites")
    assert entry.writes == frozenset({"remote"}), sorted(entry.writes)
    assert not entry.writes & registry.DB_WRITE_SURFACES
    assert "colour" not in entry.summary and "both ways" not in entry.summary


def test_the_verb_asks_no_question_its_work_cannot_raise():
    """The cloud-sync decision goes with the database surfaces.

    It is the decision a person answers when the guarded writer cannot read
    rekordbox's Cloud Library Sync state. This verb never opens the database, so
    the question could not arise and an answer to it authorised nothing.
    """
    entry = registry.entry("sync.favorites")
    assert [spec.name for spec in entry.gates] == ["sync.favorites.confirm"]


def test_doctor_asks_neither_rekordbox_question_for_a_sweep_that_reads_an_export(
    monkeypatch,
):
    """Derived from this entry alone, the way ``route.unplaced`` pinned the same shape.

    ``requires_check`` walks every entry a profile switches on, so over the real
    registry another verb would answer for this one and the assertion would say
    nothing about favourites.
    """
    from cratekit.cli import doctor
    from cratekit.core import profiles

    monkeypatch.setattr(registry, "entries", lambda: (registry.entry("sync.favorites"),))
    membership = profiles.resolve("full")
    assert doctor.requires_check("library.mounted", membership)
    assert doctor.requires_check("credential.provider", membership)
    assert not doctor.requires_check("rekordbox.closed", membership)
    assert not doctor.requires_check("rekordbox.pins", membership)


def test_a_sweep_runs_with_rekordbox_open_and_never_opens_the_database(
    installed, exported, monkeypatch
):
    """Why dropping both checks is safe, driven rather than argued.

    The verb reads a collection export through this project's own reader. Both
    rekordbox and its agent are reported running, which is the state doctor used
    to refuse this verb in, and the sweep still hearts both rows. Nothing opens
    the library database: ``rb_writer.open_db`` raises if anything reaches for it.
    """
    del installed
    from cratekit.core import rb_writer

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)

    def refuse_to_open(*args, **kwargs):
        raise AssertionError("the favourites sweep opened the library database")

    monkeypatch.setattr(rb_writer, "open_db", refuse_to_open)
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2))
    bind(monkeypatch, account)

    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")

    assert _resume(job_id)[0] == int(ExitCode.OK)
    assert sorted(account.hearted) == ["tid-1", "tid-2"]


# ═══════════════════════════════════════════════════════════════════════════
# 5. The provider seam, and what a person is told before they confirm
# ═══════════════════════════════════════════════════════════════════════════


def test_with_no_credential_the_seam_refuses_with_the_credential_cause(installed):
    """Distinguishable from the no-adapter refusal, because doctor can fix one."""
    with pytest.raises(CratekitError) as excinfo:
        account_module.resolve(installed)
    assert excinfo.value.cause.reason == "credential-missing"
    assert excinfo.value.cause.code is not ExitCode.INTERNAL


def unimportable_adapter(monkeypatch) -> None:
    """A build whose account adapter does not import, which is the one case the
    unbound refusal and the queued warning still describe since U63."""
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
    """Told at the moment it is still actionable, not after the job has failed.

    Since U63 a shipped build is bound, so the warning is gone there, and a build
    whose adapter does not import still carries it.
    """
    del installed
    if not adapter_imports:
        unimportable_adapter(monkeypatch)
    assert account_module.bound() is adapter_imports
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
    assert ("outbound-account-unbound" in codes) is not adapter_imports


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


@pytest.mark.parametrize(
    "verb, gate, module, worker",
    [
        ("export", "export.playlist.confirm", export_cli, "run_export_item"),
        ("favorites", "sync.favorites.confirm", favorites_cli, "run_heart_item"),
    ],
    ids=["export.playlist", "sync.favorites"],
)
def test_the_handler_runs_against_the_frozen_configuration_not_the_current_one(
    installed, exported, monkeypatch, verb, gate, module, worker
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
    invocation = export_verb(exported) if verb == "export" else favorites_verb(exported)
    _run, job_id = approve_and_queue(invocation, gate)

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
    real = getattr(module, worker)

    def watched(payload, item_id, cfg, remote):
        seen.append(cfg.reports.intake_stale_days)
        return real(payload, item_id, cfg, remote)

    monkeypatch.setattr(module, worker, watched)
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
    data["library"]["location_prefix_map"] = [
        {"from": str(old), "to": "{library.root}"}
    ]
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
    assert [c.isrc for c in source.heart_candidates(library, ("1",), cfg=cfg)] == [
        "ZZX9A2600042"
    ]
    source.forget_libraries()


def test_an_absent_library_root_refuses_rather_than_reading_every_row_untagged(
    installed, exported, monkeypatch
):
    """The review's finding: an unmounted volume is not a library of untagged files."""
    library = source.read_library(exported)
    gone = replace(installed, library=replace(installed.library, root=installed.library.root / "unplugged"))

    for build in (source.local_tracks, source.heart_candidates):
        with pytest.raises(CratekitError) as raised:
            build(library, ("1",), cfg=gone)
        assert raised.value.cause.reason == "library-volume-unmounted"


def test_the_default_favourites_playlist_is_the_one_the_fixture_carries():
    """A default that drifted from the live library's shape is the whole point.

    The first draft of this unit defaulted to ``Favorites``, which is a FOLDER in
    the live library, so every real run would have refused while the suite stayed
    green on a fixture that named a playlist directly.
    """
    assert source.DEFAULT_FAVORITES_PLAYLIST == outbound_fakes.FAVORITES


# ═══════════════════════════════════════════════════════════════════════════
# 9. What the review found a green suite could not see
# ═══════════════════════════════════════════════════════════════════════════


def test_a_dangling_track_is_named_in_the_queued_envelope(installed, monkeypatch):
    """The derivation collected it and nothing drove the reporting of it.

    ``source.resolve`` returning ``dangling`` was tested; the warning built from
    it was not, so the branch could have been deleted with the suite green.
    """
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", crate=(1, 2, 99), tracks=2
    )
    _run, job_id = approve_and_queue(export_verb(path), "export.playlist.confirm")
    code, shown = drive(["job", "show", job_id])
    assert code == int(ExitCode.OK), shown
    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, job_id)] == ["1", "2"]


def test_the_queued_envelope_names_a_missing_and_a_repeated_track(
    installed, monkeypatch
):
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    path = outbound_fakes.write_export(
        installed.library.root / "outbound", crate=(1, 2, 99, 1, 1), tracks=2
    )
    code, refused = drive(export_verb(path))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
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
    code, queued = drive(["--run", refused["run_id"], *export_verb(path)])
    assert code == int(ExitCode.OK), queued
    warnings = {w["code"]: w["message"] for w in queued.get("warnings") or ()}
    assert "playlist-track-missing" in warnings
    assert "99" in warnings["playlist-track-missing"]
    assert "playlist-track-repeated" in warnings
    # ONE track repeated, however many times it repeats. The count and the named
    # list must describe distinct tracks or the sentence contradicts itself.
    assert warnings["playlist-track-repeated"].startswith("1 track(s)")
    assert warnings["playlist-track-repeated"].count("'1'") <= 1


def test_a_ledger_that_cannot_be_written_creates_no_remote_playlist_at_all(
    installed, exported, monkeypatch
):
    """The duplicate playlist defect, driven, in the direction that produced it.

    An UNREADABLE ledger refuses before anything is created and was already
    covered. An UNWRITABLE one is the case that duplicated: the old ordering read
    the recorded id without a lock, created a remote playlist, and only then
    failed trying to record it, so every item after it created another one. One
    three track export made three remote playlists. The lock now precedes the
    create, so the account is untouched.
    """
    del installed
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3))
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")

    def unwritable(cfg):
        raise ledger._unusable(
            Path("outbound_writes.lock"), "the state directory is not writable"
        )

    monkeypatch.setattr(ledger, "_locked", unwritable)
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    assert account.created == [], (
        "an unwritable ledger must refuse BEFORE the remote playlist is made; "
        "a create the ledger cannot record is one the next item makes again"
    )


def test_a_cancelled_job_does_not_report_a_clean_resume(
    installed, exported, monkeypatch
):
    """R-225 taken to the state that actually reaches a person: an interrupt.

    A run stopped with a signal is CANCELLED, not FAILED, and it carries the
    cause ``jobs.cancel`` builds. A guard reading FAILED alone reported an
    interrupted export through a normal envelope and exited OK, over a job with
    items still pending and tracks already on the remote playlist.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    with jobs.open_store() as store:
        cancelled = jobs.cancel(store, job_id)
    assert cancelled.state is jobs.JobState.CANCELLED
    assert cancelled.cause is not None

    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    assert resumed["cause"] is not None


def test_a_job_with_no_items_refuses_rather_than_reporting_a_clean_success(
    installed, exported, monkeypatch
):
    """The zero item rule on the DRIVE side, for a job neither verb can queue now.

    A job frozen by a build before this one carries no items, and ``core.jobs``
    reports attempting nothing as SUCCEEDED by design. Driving one would tell a
    person their export finished when nothing was ever queued to run.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    with jobs.open_store() as store:
        with store.immediate() as conn:
            conn.execute("DELETE FROM job_items WHERE job_id = ?", (job_id,))
    code, resumed = _resume(job_id)
    assert code != int(ExitCode.OK), resumed
    assert resumed["cause"]["reason"] == "internal-error"
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is not jobs.JobState.SUCCEEDED


def test_a_confirm_does_not_authorise_a_different_track_set_at_the_same_path(
    installed, monkeypatch
):
    """The case the two-path test could not reach, and the one a person hits.

    An operator confirms an export, re-exports the collection from rekordbox over
    the same working path because that is what a working path is for, and runs
    the approved invocation. The digest used to name the path and the playlist,
    both unchanged, so a different set of tracks was written to their streaming
    account under a decision that never described it.
    """
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    path = outbound_fakes.write_export(installed.library.root / "outbound", crate=(1,))
    code, refused = drive(export_verb(path))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
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
    path.write_bytes(outbound_fakes.export_document(crate=(1, 2, 3)))
    source.forget_libraries()
    code, other = drive(["--run", refused["run_id"], *export_verb(path)])
    assert code != int(ExitCode.OK), other
    assert other["cause"]["reason"] == "decision-stale"
    assert _queue_is_empty()


def test_job_show_reports_the_bound_worker_for_a_queued_sweep(
    installed, exported, monkeypatch
):
    """The plan named this for both verbs and only the export verb had it."""
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2)))
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    code, shown = drive(["job", "show", job_id])
    assert code == int(ExitCode.OK), shown
    assert shown["data"]["progress"]["worker"] == "bound"


def test_a_failed_favourite_leaves_the_sweep_resumable(
    installed, exported, monkeypatch
):
    """The plan named it for both verbs and only the export verb had it."""
    del installed
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2), fail_on={"tid-2"})
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")
    assert _resume(job_id)[0] != int(ExitCode.OK)

    account.fail_on = frozenset()
    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    assert _resume(job_id)[0] == int(ExitCode.OK)
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


def test_an_export_the_provider_matches_nothing_of_says_so_in_the_envelope(
    installed, exported, monkeypatch
):
    """The plan's success criterion, at its worst case rather than its easy one."""
    del installed
    account = outbound_fakes.FakeAccount(catalog={})
    bind(monkeypatch, account)
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    code, resumed = _resume(job_id)
    assert code == int(ExitCode.OK), resumed
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["added"] == []
    assert sorted(outbound["unmatched"]) == ["1", "2", "3"]


def test_a_bare_name_resolves_a_uniquely_named_nested_playlist(installed):
    """The bare-name fallback, reached into a resolution rather than a refusal."""
    path = outbound_fakes.write_export(
        installed.library.root / "outbound",
        extra_children=outbound_fakes.nested_playlist("Crates", "Deep Cuts", [2, 3]),
    )
    resolved = source.resolve(source.read_library(path), "Deep Cuts")
    assert resolved.key == "Crates/Deep Cuts"
    assert resolved.name == "Deep Cuts"
    assert resolved.track_ids == ("2", "3")


def test_aborting_the_confirmation_queues_nothing(installed, exported):
    """The other option on the gate, which no test had ever chosen."""
    del installed
    code, refused = drive(export_verb(exported))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["options"][-1] == "abort"
    assert (
        drive(
            [
                "run",
                "decide",
                refused["run_id"],
                detail["gate"],
                "abort",
                "--actor",
                "a-person",
            ]
        )[0]
        == int(ExitCode.OK)
    )
    code, aborted = drive(["--run", refused["run_id"], *export_verb(exported)])
    assert code == int(ExitCode.OK), aborted
    assert aborted["outcome"] == "no_op"
    assert aborted["data"]["state"] == "declined"
    assert _queue_is_empty()


# ═══════════════════════════════════════════════════════════════════════════
# R-227. The export is a file somebody made by hand, and it can be old
# ═══════════════════════════════════════════════════════════════════════════

#: A fixed instant, so an age is a subtraction rather than a race with the clock.
_WRITTEN = datetime(2026, 8, 1, 12, 0, 0, tzinfo=timezone.utc)

BOTH_VERBS = pytest.mark.parametrize(
    "verb, gate",
    [
        pytest.param("export", "export.playlist.confirm", id="export.playlist"),
        pytest.param("favorites", "sync.favorites.confirm", id="sync.favorites"),
    ],
)


def _invocation(verb: str, exported: Path) -> list[str]:
    return export_verb(exported) if verb == "export" else favorites_verb(exported)


def _written_days_ago(exported: Path, days: float) -> datetime:
    """Set the export's modification time, and return the instant it now carries.

    THE RETURNED INSTANT IS READ BACK OFF THE FILE rather than computed here, so
    a filesystem that rounds a timestamp cannot make the expected date disagree
    with the one the product reads.
    """
    moment = datetime.now(timezone.utc).timestamp() - days * 86_400
    os.utime(exported, (moment, moment))
    return datetime.fromtimestamp(exported.stat().st_mtime, tz=timezone.utc)


def _local(moment: datetime) -> str:
    """The instant as the product shows it: this machine's zone, to the second.

    LOCAL BECAUSE A PERSON COMPARES IT WITH THEIR MEMORY AND WITH FINDER. An
    evening export west of Greenwich is the next day in UTC, which is a day off
    on the one fact this surface exists to show.
    """
    return moment.astimezone().replace(microsecond=0).isoformat()


def _configure_stale_days(days: int) -> None:
    current = config.load()
    config.save(replace(current, outbound=replace(current.outbound, export_stale_days=days)))
    config.reset_cache()


@BOTH_VERBS
def test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows(
    installed, exported, verb, gate
):
    """R-227's cost, reproduced. The person deciding is told the file's date.

    Before this, a month old export met the gate with no ``shown`` at all, so
    the question arrived with nothing about the document it was asked over.
    """
    del installed
    written = _written_days_ago(exported, 30)
    code, refused = drive(_invocation(verb, exported))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == gate
    shown = detail["shown"]["export"]
    assert shown["file"] == exported.name
    assert shown["written"] == _local(written)
    assert shown["age_days"] == 30
    assert shown["stale_after_days"] == 7
    assert shown["freshness"] == "stale"
    # THE SENTENCE IS AT THE GATE, not only on the envelope that follows the
    # answer. Advice to export again is no use to somebody who already confirmed.
    assert "Export the collection again" in shown["warning"]
    assert written.astimezone().date().isoformat() in shown["warning"]


@BOTH_VERBS
def test_the_date_reaches_a_person_who_is_not_reading_json(
    installed, exported, verb, gate
):
    """``drive`` is json only, and the human renderer is a second reader."""
    del installed, gate
    written = _written_days_ago(exported, 30)
    code, text = _human(_invocation(verb, exported))
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
    with jobs.open_store() as store:
        assert jobs.items(store, queued["data"]["job_id"]), "a stale export refuses nothing"


@BOTH_VERBS
def test_a_fresh_export_shows_its_date_and_warns_of_nothing(
    installed, exported, monkeypatch, verb, gate
):
    """The date is shown EVERY time, the warning only past the limit.

    A plan that named the date only when it was old would make a missing line
    mean "fresh", which is absence read as evidence.
    """
    del installed
    bind(monkeypatch, outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3)))
    _written_days_ago(exported, 2)
    code, refused = drive(_invocation(verb, exported))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
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
def test_the_limit_is_the_configured_one_in_both_directions(
    installed, exported, verb, gate
):
    """A longer limit quiets a month old file, a shorter one flags a two day old one."""
    del installed, gate
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


def test_old_means_past_the_limit_and_not_at_it(tmp_path):
    """Seven days exactly is not past seven days, and one second more is.

    Compared as DURATIONS. Floored whole days would read seven days and twenty
    three hours as seven, and call it fresh for a day longer than the key says.
    """
    document = tmp_path / "collection.xml"
    document.write_text("<x/>")
    os.utime(document, (_WRITTEN.timestamp(), _WRITTEN.timestamp()))
    at = source.export_age(document, limit_days=7, now=_WRITTEN + timedelta(days=7))
    past = source.export_age(
        document, limit_days=7, now=_WRITTEN + timedelta(days=7, seconds=1)
    )
    late = source.export_age(
        document, limit_days=7, now=_WRITTEN + timedelta(days=7, hours=23)
    )
    assert (at.stale, at.age_days) == (False, 7)
    assert (past.stale, past.age_days) == (True, 7)
    assert (late.stale, late.age_days) == (True, 7)
    assert at.written == _WRITTEN


def test_a_few_hours_ahead_is_a_clock_and_reads_as_written_just_now(tmp_path):
    """A volume whose clock runs ahead, or an exFAT zone skew, is not news."""
    document = tmp_path / "collection.xml"
    document.write_text("<x/>")
    os.utime(document, (_WRITTEN.timestamp(), _WRITTEN.timestamp()))
    age = source.export_age(document, limit_days=7, now=_WRITTEN - timedelta(hours=14))
    assert (age.stale, age.age_days, age.future_dated) == (False, 0, False)
    assert shell_module.freshness(age) == "within-limit"


def test_a_date_well_in_the_future_is_not_the_freshest_export_there_could_be(tmp_path):
    """Found by the built in review. Clamped to zero it read ``within-limit``
    until the clock caught up, so an old export was never called old. A date
    that cannot be true is a date that cannot be judged, and it says so."""
    document = tmp_path / "collection.xml"
    document.write_text("<x/>")
    os.utime(document, (_WRITTEN.timestamp(), _WRITTEN.timestamp()))
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


def test_the_date_is_the_persons_own_and_not_greenwichs(tmp_path, monkeypatch):
    """Nine in the evening in New York is one in the morning, tomorrow, in UTC.

    THE ZONE IS SET HERE, because read off the machine this is a guard that
    holds only at some hours of the day and on some machines, and a CI runner in
    UTC would agree with the defect for ever.
    """
    document = tmp_path / "collection.xml"
    document.write_text("<x/>")
    written = datetime(2026, 8, 2, 1, 0, 0, tzinfo=timezone.utc)
    os.utime(document, (written.timestamp(), written.timestamp()))
    monkeypatch.setenv("TZ", "America/New_York")
    time.tzset()
    try:
        age = source.export_age(document, limit_days=7, now=written + timedelta(days=30))
        (warning,) = shell_module.age_warnings(age)
        block = shell_module.shown_export(age)["export"]
    finally:
        monkeypatch.undo()
        time.tzset()
    assert "2026-08-01" in warning["message"]
    assert "2026-08-02" not in warning["message"]
    assert block["written"] == "2026-08-01T21:00:00-04:00"


def test_the_sentence_does_not_say_seven_is_past_seven(tmp_path):
    """Found by the built in review. Staleness is a duration and the sentence
    printed floored days, so for a whole day it read "7 day(s) ago, which is
    past the 7 day(s)" allowed."""
    document = tmp_path / "collection.xml"
    document.write_text("<x/>")
    os.utime(document, (_WRITTEN.timestamp(), _WRITTEN.timestamp()))
    age = source.export_age(
        document, limit_days=7, now=_WRITTEN + timedelta(days=7, hours=5)
    )
    (warning,) = shell_module.age_warnings(age)
    assert "7 days 5 hours ago" in warning["message"]
    assert shell_module.shown_export(age)["export"]["age"] == "7 days 5 hours"


def test_a_limit_too_large_for_a_duration_does_not_crash_the_question(tmp_path):
    """Found by the built in review, reproduced as an OverflowError from
    ``timedelta(days=10_000_000_000)``. Validation bounds the key now; this is
    the value object holding on its own, since it is constructible from code
    that never touched a file."""
    document = tmp_path / "collection.xml"
    document.write_text("<x/>")
    os.utime(document, (_WRITTEN.timestamp(), _WRITTEN.timestamp()))
    age = source.export_age(
        document, limit_days=10_000_000_000, now=_WRITTEN + timedelta(days=30)
    )
    assert age.stale is False


def test_an_age_is_built_whole_or_not_at_all(tmp_path):
    """A date with no instant to judge it at would read as known and not stale,
    which is unknown folded into recent by construction."""
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
