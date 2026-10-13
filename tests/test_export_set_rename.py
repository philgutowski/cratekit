"""U140: a set's account playlist follows the library's rename, ledger and frozen name with it.

Driven through the real dispatcher with the account faked and the INSPIRATION
playlist's live row stood in for, since that read is driven against the
disposable database in tests/test_set_inspiration_playlist.py. No live account
write is claimed here; the Signal set's rename is owed to a sitting.
"""

from __future__ import annotations

import pytest

from cratekit.acquire import match
from cratekit.cli import registry
from cratekit.core import jobs
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.export import set_cli
from cratekit.intake import cli as intake_cli
from cratekit.intake import set_playlist
from cratekit.modules.outbound import ledger
from cratekit.sync import mark_record
from tests.cli_drive import drive
from tests.test_u129_set_account_playlist import (
    BUILD,
    ROWS,
    _succeeded_set_job,
    _tracklist,
)
from tests.test_u129_set_account_playlist import account as account  # noqa: PLC0414
from tests.test_u129_set_account_playlist import cfg as cfg  # noqa: PLC0414
from tests.test_u129_set_account_playlist import installed as installed  # noqa: PLC0414
from tests.test_u129_set_account_playlist import recognised as recognised  # noqa: PLC0414

RENAME = set_cli.RENAME_GATE
#: The name the set was landed and exported under, the queued day's form.
OLD = "10_10_26 Public Service NYC Live at Probe 2-26"
#: The name a person gave the INSPIRATION playlist since, the posted day's form.
NEW = "3_25_26 Public Service NYC Live at Probe 2-26"
INSPIRATION_ID = "insp-1"


def _rename_acts(job_id: str, option: str = "apply") -> tuple[int, dict, dict]:
    argv = ["export", "set", "--rename", job_id]
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == RENAME
    assert refused["cause"]["detail"]["explicit"] is True
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, RENAME, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    code, done = drive(["--run", run_id, *argv])
    return code, done, refused


def _recorded(cfg, held, name: str) -> str:
    remote_id, _made = ledger.reserve_set_playlist(
        cfg, name, "2026", lambda: held.create_playlist(name)
    )
    ledger.record_set_tracks(cfg, name, added=["tid-1"])
    return remote_id


def _frozen(job_id: str) -> str:
    with jobs.open_store() as store:
        return set_playlist.frozen_name(jobs.get(store, job_id))


@pytest.fixture
def renamed(account, monkeypatch):
    """A succeeded set job frozen under OLD, its account playlist recorded under OLD,
    and its INSPIRATION playlist renamed by a person to NEW."""
    cfg, _fake, held = account
    job = _succeeded_set_job(cfg, OLD)
    remote_id = _recorded(cfg, held, OLD)
    live = {"name": NEW}
    monkeypatch.setattr(
        set_cli, "_inspiration_of", lambda _cfg, _job_id: (INSPIRATION_ID, live["name"])
    )
    return cfg, held, job.job_id, remote_id, live


def test_export_set_declares_the_rename_gate_explicit():
    entry = registry.entry("export.set")
    spec = next(one for one in entry.gates if one.name == RENAME)
    assert (spec.options, spec.explicit, spec.digest_source) == (("apply", "abort"), True, "plan")
    assert "remote" in entry.writes
    assert "library.mounted" in entry.doctor_checks


def test_a_renamed_inspiration_playlist_renames_the_account_playlist_ledger_and_job(renamed):
    cfg, held, job_id, remote_id, _live = renamed

    code, done, refused = _rename_acts(job_id)

    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "ok"
    assert held.renamed == [(remote_id, NEW)]
    assert held.titles[remote_id] == NEW
    assert ledger.set_playlist(cfg, OLD) is None
    moved = ledger.set_playlist(cfg, NEW)
    assert moved is not None and moved.remote_id == remote_id
    # The record moves whole: the tracks written under the old key stay written.
    assert moved.added == frozenset({"tid-1"}) and moved.year == "2026"
    assert _frozen(job_id) == NEW
    assert done["data"]["totals"]["applied"] == {
        "renamed": True,
        "rekeyed": True,
        "refrozen": True,
    }
    shown = refused["cause"]["detail"]["shown"]
    assert shown["account playlist"] == f"{remote_id}: {OLD!r} -> {NEW!r}"
    assert shown["ledger entry"] == f"{OLD!r} -> {NEW!r}"
    assert shown["frozen name"] == f"{OLD!r} -> {NEW!r}"
    assert INSPIRATION_ID in shown["follows"]
    actions = {item["kind"]: item["action"] for item in done["data"]["items"]}
    assert actions == {"playlist": set_cli.RENAME, "job": set_cli.REFREEZE}


def test_a_second_rename_is_a_no_op(renamed):
    cfg, held, job_id, _remote_id, _live = renamed
    assert _rename_acts(job_id)[0] == int(ExitCode.OK)

    code, done, refused = _rename_acts(job_id)

    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert len(held.renamed) == 1
    assert "nothing to write" in refused["cause"]["detail"]["shown"]
    assert done["data"]["totals"]["writes"] is False


def test_an_aborted_rename_writes_nothing(renamed):
    cfg, held, job_id, _remote_id, _live = renamed

    code, done, _refused = _rename_acts(job_id, option="abort")

    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert held.renamed == []
    assert ledger.set_playlist_names(cfg) == (OLD,)
    assert _frozen(job_id) == OLD


def test_a_backfill_after_the_rename_plans_no_twin_and_a_named_export_adds_to_it(
    account, monkeypatch
):
    """The twin R-1004 names: a job with no frozen name, exported under the
    queued day's form, whose INSPIRATION playlist now carries the posted day's."""
    cfg, _fake, held = account
    job = _succeeded_set_job(cfg, "", created="2026-10-09T12:00:00+00:00")
    posted, queued = set_cli._names_for_job(job)
    remote_id = _recorded(cfg, held, queued)
    monkeypatch.setattr(set_cli, "_inspiration_of", lambda _cfg, _job_id: (INSPIRATION_ID, posted))
    monkeypatch.setattr(set_cli, "_inspiration_playlists", lambda _cfg: [(posted, INSPIRATION_ID)])
    wanted = tuple(match.Wanted(artist=a, title=t, origin=match.TEXT) for a, t in ROWS)
    monkeypatch.setattr(set_cli, "_wanted_from_job", lambda _cfg, _job: wanted)
    # Before the rename the backfill reads the set as having no account playlist.
    code, before = drive(["export", "set"])
    assert code == int(ExitCode.DECISION_REQUIRED), before
    assert before["cause"]["detail"]["shown"]["inspiration without account playlist"] == [posted]

    assert _rename_acts(job.job_id)[0] == int(ExitCode.OK)

    code, after = drive(["export", "set"])
    assert code == int(ExitCode.DECISION_REQUIRED), after
    assert after["cause"]["detail"]["shown"]["inspiration without account playlist"] == ["none"]
    assert held.created == [queued]

    # A set exported again under its new name adds to the renamed playlist.
    path = _tracklist(cfg)
    code, refused = drive(["export", "set", str(path), "--name", posted])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    assert drive(["run", "decide", run_id, BUILD, "apply", "--actor", "a-person"])[0] == int(
        ExitCode.OK
    )
    code, done = drive(["--run", run_id, "export", "set", str(path), "--name", posted])
    assert code == int(ExitCode.OK), done
    (playlist,) = [i for i in done["data"]["items"] if i["kind"] == "playlist"]
    assert (playlist["id"], playlist["action"]) == (remote_id, "reuse")
    assert held.created == [queued]
    assert done["data"]["totals"]["applied"]["added"] == len(ROWS) - 1


def test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen(account, monkeypatch):
    """The Signal set's own shape: queued before the freeze, exported under the
    queued day's form, its INSPIRATION playlist renamed to the posted day's."""
    cfg, _fake, held = account
    job = _succeeded_set_job(cfg, "", created="2026-10-09T12:00:00+00:00")
    names = set_cli._names_for_job(job)
    assert names[0] == "5_03_26 Probe Friday Night Mix 5-26"
    queued = names[1]
    assert queued.startswith("10_09_26 ")
    remote_id = _recorded(cfg, held, queued)
    monkeypatch.setattr(
        set_cli, "_inspiration_of", lambda _cfg, _job_id: (INSPIRATION_ID, names[0])
    )

    code, done, refused = _rename_acts(job.job_id)

    assert code == int(ExitCode.OK), done
    assert refused["cause"]["detail"]["shown"]["frozen name"] == f"none -> {names[0]!r}"
    assert held.renamed == [(remote_id, names[0])]
    assert ledger.set_playlist_names(cfg) == (names[0],)
    assert _frozen(job.job_id) == names[0]


def test_a_missing_account_record_refuses_by_name(renamed):
    cfg, held, _job_id, _remote_id, _live = renamed
    other = _succeeded_set_job(cfg, "1_01_26 Nobody Recorded 1-26")

    code, done = drive(["export", "set", "--rename", other.job_id])

    assert code == int(ExitCode.PRECONDITION), done
    assert done["cause"]["reason"] == set_cli.RENAME_UNRESOLVED
    assert "no account playlist is recorded" in done["cause"]["message"]
    assert "1_01_26 Nobody Recorded 1-26" in done["cause"]["message"]
    assert held.renamed == []


def test_a_job_whose_inspiration_playlist_is_gone_refuses_by_name(renamed, monkeypatch):
    cfg, held, job_id, _remote_id, _live = renamed
    monkeypatch.setattr(set_cli, "_inspiration_of", lambda _cfg, _job_id: None)

    code, done = drive(["export", "set", "--rename", job_id])

    assert code == int(ExitCode.PRECONDITION), done
    assert done["cause"]["reason"] == set_cli.RENAME_UNRESOLVED
    assert "no INSPIRATION playlist" in done["cause"]["message"]
    assert held.renamed == []
    assert ledger.set_playlist_names(cfg) == (OLD,)


def test_a_playlist_the_archive_marked_is_refused_rather_than_retitled(renamed):
    cfg, held, job_id, remote_id, _live = renamed
    mark_record.MarkRecord(cfg).record_marked("pass-1", {remote_id: (OLD, f"DOWNLOADED {OLD}")})

    code, done = drive(["export", "set", "--rename", job_id])

    assert code == int(ExitCode.PRECONDITION), done
    assert done["cause"]["reason"] == set_cli.RENAME_UNRESOLVED
    assert any(
        "crate sync unmark --pass 'pass-1'" in step
        for step in done["cause"]["remediation"]["steps"]
    ), done["cause"]
    assert held.renamed == []
    assert _frozen(job_id) == OLD


def test_a_mark_already_put_back_does_not_refuse(renamed):
    cfg, held, job_id, remote_id, _live = renamed
    record = mark_record.MarkRecord(cfg)
    record.record_marked("pass-1", {remote_id: (OLD, f"DOWNLOADED {OLD}")})
    record.record_unmarked("pass-1", remote_id)

    assert _rename_acts(job_id)[0] == int(ExitCode.OK)
    assert held.renamed == [(remote_id, NEW)]


def test_a_rename_that_failed_after_the_account_finishes_on_the_next_run(renamed, monkeypatch):
    cfg, held, job_id, remote_id, _live = renamed
    real = jobs.refreeze

    def broken(*_args, **_kwargs):
        raise refuse(
            "unavailable-transient",
            "the job store was busy",
            remedy=Remedy.RETRY_LATER,
            origin=("test",),
        )

    monkeypatch.setattr(jobs, "refreeze", broken)
    code, done, _refused = _rename_acts(job_id)
    assert code != int(ExitCode.OK), done
    message = done["cause"]["message"]
    assert "renamed to" in message and "ledger entry moved" in message
    assert done["cause"]["detail"]["refrozen"] is False
    assert ledger.set_playlist_names(cfg) == (NEW,)
    assert _frozen(job_id) == OLD

    monkeypatch.setattr(jobs, "refreeze", real)
    code, done, refused = _rename_acts(job_id)

    assert code == int(ExitCode.OK), done
    assert refused["cause"]["detail"]["shown"]["account playlist"] == f"{remote_id}: already {NEW!r}"
    assert len(held.renamed) == 1
    assert _frozen(job_id) == NEW


def test_a_ledger_left_under_the_old_key_is_moved_on_the_next_run(renamed, monkeypatch):
    cfg, held, job_id, remote_id, _live = renamed
    real = ledger.rename_set_playlist

    def broken(*_args, **_kwargs):
        raise OSError("the ledger's directory went read only")

    monkeypatch.setattr(ledger, "rename_set_playlist", broken)
    code, done, _refused = _rename_acts(job_id)
    assert code != int(ExitCode.OK), done
    assert done["cause"]["reason"] == "internal-error"
    assert "renamed to" in done["cause"]["message"]
    assert ledger.set_playlist_names(cfg) == (OLD,)
    assert _frozen(job_id) == OLD
    monkeypatch.setattr(ledger, "rename_set_playlist", real)

    code, done, _refused = _rename_acts(job_id)

    assert code == int(ExitCode.OK), done
    assert held.renamed == [(remote_id, NEW), (remote_id, NEW)]
    assert ledger.set_playlist_names(cfg) == (NEW,)
    assert _frozen(job_id) == NEW


def test_rename_with_a_tracklist_or_name_is_refused_before_anything(renamed):
    cfg, held, job_id, _remote_id, _live = renamed
    path = _tracklist(cfg)
    for extra in ([str(path)], ["--name", NEW]):
        code, done = drive(["export", "set", *extra, "--rename", job_id])
        assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), done
        assert done["cause"]["reason"] == "intake-list-unusable"
    assert held.renamed == []


def test_a_job_that_is_not_a_set_is_refused(renamed):
    cfg, held, _job_id, _remote_id, _live = renamed
    with jobs.open_store() as store:
        other = jobs.enqueue(
            store, handler_key="intake.playlist", payload={intake_cli.SOURCE: "x"}, cfg=cfg
        )
    code, done = drive(["export", "set", "--rename", other.job_id])
    assert done["cause"]["reason"] == "job-unknown", done
    assert held.renamed == []


def test_refreeze_refuses_a_job_that_has_not_succeeded(account):
    cfg, _fake, _held = account
    with jobs.open_store() as store:
        open_job = jobs.enqueue(
            store, handler_key=set_playlist.SET_KEY, payload={"playlist_name": OLD}, cfg=cfg
        )
        with pytest.raises(CratekitError) as caught:
            jobs.refreeze(store, open_job.job_id, intake_cli.PLAYLIST_NAME, NEW)
        assert "only a succeeded job" in caught.value.cause.message
        assert set_playlist.frozen_name(jobs.get(store, open_job.job_id)) == OLD


def test_the_ledger_refuses_to_fold_a_rename_into_another_playlist(account):
    cfg, _fake, held = account
    first = _recorded(cfg, held, OLD)
    _recorded(cfg, held, NEW)
    with pytest.raises(CratekitError) as caught:
        ledger.rename_set_playlist(cfg, OLD, NEW, first)
    assert caught.value.cause.reason == "outbound-ledger-unusable"
    assert ledger.set_playlist(cfg, OLD).remote_id == first
    with pytest.raises(CratekitError):
        ledger.rename_set_playlist(cfg, OLD, "elsewhere", "not-" + first)
    assert set(ledger.set_playlist_names(cfg)) == {OLD, NEW}


def test_a_twin_under_the_new_name_is_refused_rather_than_adopted(renamed):
    """A backfill that already made a twin under NEW: the rename chooses neither."""
    cfg, held, job_id, remote_id, _live = renamed
    twin = _recorded(cfg, held, NEW)

    code, done = drive(["export", "set", "--rename", job_id])

    assert code == int(ExitCode.PRECONDITION), done
    assert done["cause"]["reason"] == set_cli.RENAME_UNRESOLVED
    assert remote_id in done["cause"]["message"] and twin in done["cause"]["message"]
    assert held.renamed == []
    assert set(ledger.set_playlist_names(cfg)) == {OLD, NEW}
    assert _frozen(job_id) == OLD


def test_a_name_with_a_slash_freezes_as_the_library_spells_it(account, monkeypatch):
    """The account and the ledger spell a slash as a dash; the job keeps the slash,
    since its frozen name names the INSPIRATION playlist too."""
    cfg, _fake, held = account
    live = "3_25_26 Live 3/25 at Probe 2-26"
    job = _succeeded_set_job(cfg, OLD)
    remote_id = _recorded(cfg, held, OLD)
    monkeypatch.setattr(set_cli, "_inspiration_of", lambda _cfg, _job_id: (INSPIRATION_ID, live))

    code, done, refused = _rename_acts(job.job_id)

    assert code == int(ExitCode.OK), done
    spelled = set_cli.set_name(live)
    assert held.renamed == [(remote_id, spelled)]
    assert ledger.set_playlist_names(cfg) == (spelled,)
    assert _frozen(job.job_id) == live
    assert refused["cause"]["detail"]["shown"]["frozen name"] == f"{OLD!r} -> {live!r}"

    code, done, _refused = _rename_acts(job.job_id)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"


def test_refreeze_refuses_a_job_that_is_not_in_the_queue(account):
    with jobs.open_store() as store:
        with pytest.raises(CratekitError) as caught:
            jobs.refreeze(store, "no-such-job", intake_cli.PLAYLIST_NAME, NEW)
    assert caught.value.cause.reason == "job-unknown"
