"""U140: a set's account playlist follows the library's rename, ledger and frozen name with it.

The account is faked, the INSPIRATION row stood in for (``tests/test_set_inspiration_playlist.py``).
"""

from __future__ import annotations

import pytest

from cratekit.acquire import match
from cratekit.cli import registry
from cratekit.core import jobs, session
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.export import set_cli
from cratekit.intake import cli as intake_cli
from cratekit.intake import set_playlist
from cratekit.modules.outbound import ledger
from cratekit.sync import mark_record
from tests.cli_drive import drive
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_u129_set_account_playlist import BUILD, ROWS, _succeeded_set_job, _tracklist
from tests.test_u129_set_account_playlist import account as account  # noqa: PLC0414
from tests.test_u129_set_account_playlist import cfg as cfg  # noqa: PLC0414
from tests.test_u129_set_account_playlist import installed as installed  # noqa: PLC0414
from tests.test_u129_set_account_playlist import recognised as recognised  # noqa: PLC0414

try:
    from cratekit.export import set_rename
except ImportError:
    # Before U309 the rename lived in ``set_cli``, which the behaviour comparison runs.
    set_rename = set_cli


RENAME = set_cli.RENAME_GATE
#: The name the set was landed and exported under, the queued day's form.
OLD = "10_10_26 Public Service NYC Live at Probe 2-26"
#: The name a person gave the INSPIRATION playlist since, the posted day's form.
NEW = "3_25_26 Public Service NYC Live at Probe 2-26"
INSPIRATION_ID = "insp-1"


def _acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict, dict]:
    """The first act refused at ``gate``, the decide, and the run that carries it out."""
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    code, done = drive(["--run", run_id, *argv])
    return code, done, refused


def _rename_acts(job_id: str, option: str = "apply") -> tuple[int, dict, dict]:
    code, done, refused = _acts(["export", "set", "--rename", job_id], RENAME, option)
    assert refused["cause"]["detail"]["gate"] == RENAME
    assert refused["cause"]["detail"]["explicit"] is True
    return code, done, refused


def _renamed(job_id: str, option: str = "apply") -> tuple[dict, dict]:
    code, done, refused = _rename_acts(job_id, option)
    assert code == int(ExitCode.OK), done
    return done, refused


def _unresolved(job_id: str) -> dict:
    code, done = drive(["export", "set", "--rename", job_id])
    assert code == int(ExitCode.PRECONDITION), done
    assert done["cause"]["reason"] == set_cli.RENAME_UNRESOLVED
    return done


def _inspiration_named(monkeypatch, name: str) -> None:
    """The INSPIRATION playlist's live row, stood in for, carrying ``name``."""
    monkeypatch.setattr(set_rename, "_inspiration_of", lambda _cfg, _job_id: (INSPIRATION_ID, name))


def _recorded(cfg, held, name: str) -> str:
    made = ledger.reserve_set_playlist(cfg, name, "2026", lambda: held.create_playlist(name))
    remote_id = made[0]
    ledger.record_set_tracks(cfg, name, added=["tid-1"])
    return remote_id


def _landed(cfg, job_id: str, name: str, *, state=session.SessionState.CLOSED,
            source=session.SourceState.COMMITTED, stamp: str | None = None) -> None:
    """A landing's session record naming the set's INSPIRATION playlist ``name``."""
    record = session.open_session(cfg, workflow="intake", sources=("library",), session_id=stamp)
    record.sources["library"] = str(source)
    recorded = {"id": "insp-row", "name": name, "job": job_id, "folder": "insp-folder"}
    record.detail[set_playlist.RECORD_KEY] = recorded
    record.state = state
    record.ended = "2026-10-10T16:09:29+00:00"
    session.write_record(record, cfg)


def _backfill_shown() -> dict:
    """What the bare backfill's gate shows, before anything is decided."""
    code, asked = drive(["export", "set"])
    assert code == int(ExitCode.DECISION_REQUIRED), asked
    return asked["cause"]["detail"]["shown"]


def _frozen(job_id: str) -> str:
    with jobs.open_store() as store:
        return set_playlist.frozen_name(jobs.get(store, job_id))


@pytest.fixture
def renamed(account, monkeypatch):
    """A set job and its account playlist under OLD, its INSPIRATION playlist renamed NEW."""
    cfg, _fake, held = account
    job = _succeeded_set_job(cfg, OLD)
    remote_id = _recorded(cfg, held, OLD)
    live = {"name": NEW}
    monkeypatch.setattr(
        set_rename, "_inspiration_of", lambda _cfg, _job_id: (INSPIRATION_ID, live["name"])
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
    done, refused = _renamed(job_id)
    assert done["outcome"] == "ok"
    assert held.renamed == [(remote_id, NEW)]
    assert held.titles[remote_id] == NEW
    assert ledger.set_playlist(cfg, OLD) is None
    moved = ledger.set_playlist(cfg, NEW)
    assert moved is not None and moved.remote_id == remote_id
    # The record moves whole: the tracks written under the old key stay written.
    assert moved.added == frozenset({"tid-1"}) and moved.year == "2026"
    assert _frozen(job_id) == NEW
    assert done["data"]["totals"]["applied"] == {"renamed": True, "rekeyed": True, "refrozen": True}
    shown = refused["cause"]["detail"]["shown"]
    assert shown["account playlist"] == f"{remote_id}: {OLD!r} -> {NEW!r}"
    assert shown["ledger entry"] == f"{OLD!r} -> {NEW!r}"
    assert shown["frozen name"] == f"{OLD!r} -> {NEW!r}"
    assert INSPIRATION_ID in shown["follows"]
    actions = {item["kind"]: item["action"] for item in done["data"]["items"]}
    assert actions == {"playlist": set_rename.RENAME, "job": set_rename.REFREEZE}


def test_a_second_rename_is_a_no_op(renamed):
    cfg, held, job_id, _remote_id, _live = renamed
    _renamed(job_id)
    done, refused = _renamed(job_id)
    assert done["outcome"] == "no_op"
    assert len(held.renamed) == 1
    assert "nothing to write" in refused["cause"]["detail"]["shown"]
    assert done["data"]["totals"]["writes"] is False


def test_an_aborted_rename_writes_nothing(renamed):
    cfg, held, job_id, _remote_id, _live = renamed
    done, _refused = _renamed(job_id, option="abort")
    assert done["outcome"] == "no_op"
    assert held.renamed == []
    assert ledger.set_playlist_names(cfg) == (OLD,)
    assert _frozen(job_id) == OLD


def test_a_backfill_after_the_rename_plans_no_twin_and_a_named_export_adds_to_it(
    account, monkeypatch
):
    """R-1004's twin: no frozen name, exported as queued, INSPIRATION now as posted."""
    cfg, _fake, held = account
    job = _succeeded_set_job(cfg, "", created="2026-10-09T12:00:00+00:00")
    posted, queued = set_cli._names_for_job(job)
    remote_id = _recorded(cfg, held, queued)
    _inspiration_named(monkeypatch, posted)
    monkeypatch.setattr(set_cli, "_inspiration_playlists", lambda _cfg: [(posted, INSPIRATION_ID)])
    wanted = tuple(match.Wanted(artist=a, title=t, origin=match.TEXT) for a, t in ROWS)
    monkeypatch.setattr(set_cli, "_wanted_from_job", lambda _cfg, _job: wanted)
    # Before the rename the backfill reads the set as having no account playlist.
    assert _backfill_shown()["inspiration without account playlist"] == [posted]
    _renamed(job.job_id)
    assert _backfill_shown()["inspiration without account playlist"] == ["none"]
    assert held.created == [queued]
    # A set exported again under its new name adds to the renamed playlist.
    code, done, _refused = _acts(["export", "set", str(_tracklist(cfg)), "--name", posted], BUILD)
    assert code == int(ExitCode.OK), done
    (playlist,) = [i for i in done["data"]["items"] if i["kind"] == "playlist"]
    assert (playlist["id"], playlist["action"]) == (remote_id, "reuse")
    assert held.created == [queued]
    assert done["data"]["totals"]["applied"]["added"] == len(ROWS) - 1


def test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen(account, monkeypatch):
    """The Signal set: no frozen name, exported as queued, INSPIRATION renamed as posted."""
    cfg, _fake, held = account
    job = _succeeded_set_job(cfg, "", created="2026-10-09T12:00:00+00:00")
    names = set_cli._names_for_job(job)
    assert names[0] == "5_03_26 Probe Friday Night Mix 5-26"
    queued = names[1]
    assert queued.startswith("10_09_26 ")
    remote_id = _recorded(cfg, held, queued)
    _inspiration_named(monkeypatch, names[0])
    done, refused = _renamed(job.job_id)
    assert refused["cause"]["detail"]["shown"]["frozen name"] == f"none -> {names[0]!r}"
    assert held.renamed == [(remote_id, names[0])]
    assert ledger.set_playlist_names(cfg) == (names[0],)
    assert _frozen(job.job_id) == names[0]


def test_a_missing_account_record_refuses_by_name(renamed):
    cfg, held, _job_id, _remote_id, _live = renamed
    other = _succeeded_set_job(cfg, "1_01_26 Nobody Recorded 1-26")
    done = _unresolved(other.job_id)
    assert "no account playlist is recorded" in done["cause"]["message"]
    assert "1_01_26 Nobody Recorded 1-26" in done["cause"]["message"]
    assert held.renamed == []


def test_a_job_whose_inspiration_playlist_is_gone_refuses_by_name(renamed, monkeypatch):
    cfg, held, job_id, _remote_id, _live = renamed
    monkeypatch.setattr(set_rename, "_inspiration_of", lambda _cfg, _job_id: None)
    done = _unresolved(job_id)
    assert "no INSPIRATION playlist" in done["cause"]["message"]
    assert held.renamed == []
    assert ledger.set_playlist_names(cfg) == (OLD,)


def test_a_playlist_the_archive_marked_is_refused_rather_than_retitled(renamed):
    cfg, held, job_id, remote_id, _live = renamed
    mark_record.MarkRecord(cfg).record_marked("pass-1", {remote_id: (OLD, f"DOWNLOADED {OLD}")})
    done = _unresolved(job_id)
    steps = done["cause"]["remediation"]["steps"]
    assert any("crate sync unmark --pass 'pass-1'" in step for step in steps), done["cause"]
    assert held.renamed == []
    assert _frozen(job_id) == OLD


def test_a_mark_already_put_back_does_not_refuse(renamed):
    cfg, held, job_id, remote_id, _live = renamed
    record = mark_record.MarkRecord(cfg)
    record.record_marked("pass-1", {remote_id: (OLD, f"DOWNLOADED {OLD}")})
    record.record_unmarked("pass-1", remote_id)
    _renamed(job_id)
    assert held.renamed == [(remote_id, NEW)]


def test_a_rename_that_failed_after_the_account_finishes_on_the_next_run(renamed, monkeypatch):
    cfg, held, job_id, remote_id, _live = renamed
    real = jobs.refreeze
    def broken(*_args, **_kwargs):
        raise refuse("unavailable-transient", "the job store was busy",
                     remedy=Remedy.RETRY_LATER, origin=("test",))
    monkeypatch.setattr(jobs, "refreeze", broken)
    code, done, _refused = _rename_acts(job_id)
    assert code != int(ExitCode.OK), done
    message = done["cause"]["message"]
    assert "renamed to" in message and "ledger entry moved" in message
    assert done["cause"]["detail"]["refrozen"] is False
    assert ledger.set_playlist_names(cfg) == (NEW,)
    assert _frozen(job_id) == OLD
    monkeypatch.setattr(jobs, "refreeze", real)
    done, refused = _renamed(job_id)
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
    done, _refused = _renamed(job_id)
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
        payload = {intake_cli.SOURCE: "x"}
        other = jobs.enqueue(store, handler_key="intake.playlist", payload=payload, cfg=cfg)
    code, done = drive(["export", "set", "--rename", other.job_id])
    assert done["cause"]["reason"] == "job-unknown", done
    assert held.renamed == []


def test_refreeze_refuses_a_job_that_has_not_succeeded(account):
    cfg, _fake, _held = account
    with jobs.open_store() as store:
        payload = {"playlist_name": OLD}
        open_job = jobs.enqueue(store, handler_key=set_playlist.SET_KEY, payload=payload, cfg=cfg)
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
    done = _unresolved(job_id)
    assert remote_id in done["cause"]["message"] and twin in done["cause"]["message"]
    assert held.renamed == []
    assert set(ledger.set_playlist_names(cfg)) == {OLD, NEW}
    assert _frozen(job_id) == OLD


def test_a_name_with_a_slash_freezes_as_the_library_spells_it(account, monkeypatch):
    """The account and ledger spell a slash as a dash; the frozen name keeps it."""
    cfg, _fake, held = account
    live = "3_25_26 Live 3/25 at Probe 2-26"
    job = _succeeded_set_job(cfg, OLD)
    remote_id = _recorded(cfg, held, OLD)
    _inspiration_named(monkeypatch, live)
    done, refused = _renamed(job.job_id)
    spelled = set_cli.set_name(live)
    assert held.renamed == [(remote_id, spelled)]
    assert ledger.set_playlist_names(cfg) == (spelled,)
    assert _frozen(job.job_id) == live
    assert refused["cause"]["detail"]["shown"]["frozen name"] == f"{OLD!r} -> {live!r}"
    done, _refused = _renamed(job.job_id)
    assert done["outcome"] == "no_op"


def test_refreeze_refuses_a_job_that_is_not_in_the_queue(account):
    with jobs.open_store() as store:
        with pytest.raises(CratekitError) as caught:
            jobs.refreeze(store, "no-such-job", intake_cli.PLAYLIST_NAME, NEW)
    assert caught.value.cause.reason == "job-unknown"


# ── R-1017: the name the landing recorded ───────────────────────────────────

#: The names a landing and a backfill wrote the playlists under, no page word today.
LANDED = "10_10_26 Public Service NYC Live at Signal 2-26"


@pytest.fixture
def landed(account, monkeypatch):
    """No frozen name, the account playlist under the landing's name, INSPIRATION as NEW."""
    cfg, _fake, held = account
    job = _succeeded_set_job(cfg, "", created="2026-10-10T14:59:24+00:00")
    assert LANDED not in set_cli._names_for_job(job)
    assert NEW not in set_cli._names_for_job(job)
    remote_id = _recorded(cfg, held, LANDED)
    _inspiration_named(monkeypatch, NEW)
    return cfg, held, job.job_id, remote_id


def test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded(landed):
    cfg, held, job_id, remote_id = landed
    _landed(cfg, job_id, LANDED)
    done, refused = _renamed(job_id)
    assert held.renamed == [(remote_id, NEW)]
    assert ledger.set_playlist(cfg, LANDED) is None
    moved = ledger.set_playlist(cfg, NEW)
    assert moved is not None and moved.remote_id == remote_id
    assert moved.added == frozenset({"tid-1"})
    assert _frozen(job_id) == NEW
    shown = refused["cause"]["detail"]["shown"]
    assert shown["account playlist"] == f"{remote_id}: {LANDED!r} -> {NEW!r}"
    assert shown["frozen name"] == f"none -> {NEW!r}"
    # A second run is a no op: the record is under NEW and the job carries it.
    done, _refused = _renamed(job_id)
    assert done["outcome"] == "no_op"
    assert len(held.renamed) == 1


@pytest.mark.parametrize("recorded", ["none", "open", "uncommitted", "another job"])
def test_a_job_with_no_landing_record_and_no_matching_name_still_refuses(landed, recorded):
    """Only a closed landing of this job whose source committed names the playlist."""
    cfg, held, job_id, _remote_id = landed
    if recorded == "open":
        _landed(cfg, job_id, LANDED, state=session.SessionState.OPEN)
    elif recorded == "uncommitted":
        _landed(cfg, job_id, LANDED, source=session.SourceState.PENDING)
    elif recorded == "another job":
        _landed(cfg, "2026-10-10T00:00:00Z-0000", LANDED)
    done = _unresolved(job_id)
    assert "no account playlist is recorded" in done["cause"]["message"]
    assert LANDED not in done["cause"]["detail"]["names"]
    assert held.renamed == []
    assert ledger.set_playlist_names(cfg) == (LANDED,)


def test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old(landed):
    cfg, held, job_id, remote_id = landed
    _landed(cfg, job_id, LANDED)
    twin = _recorded(cfg, held, NEW)
    done = _unresolved(job_id)
    assert done["cause"]["detail"]["twin"] == remote_id
    assert done["cause"]["detail"]["remote_id"] == twin
    assert held.renamed == []
    assert set(ledger.set_playlist_names(cfg)) == {LANDED, NEW}
    assert _frozen(job_id) == ""


def test_the_backfill_plans_no_twin_after_a_rename_by_the_landing_record(landed, monkeypatch):
    cfg, held, job_id, _remote_id = landed
    _landed(cfg, job_id, LANDED)
    monkeypatch.setattr(set_cli, "_inspiration_playlists", lambda _cfg: [(NEW, INSPIRATION_ID)])
    # Before the rename the backfill reads the set as having no account playlist.
    left = _backfill_shown()["left for a later sitting"]
    assert any(message.startswith(f"{NEW}: ") for message in left), left
    _renamed(job_id)
    assert _backfill_shown()["inspiration without account playlist"] == ["none"]
    assert held.created == [LANDED]


def test_two_playlists_under_two_older_names_are_a_twin_not_a_choice(landed):
    """Renaming either of two older names' playlists would leave the other unrecorded."""
    cfg, held, job_id, remote_id = landed
    _landed(cfg, job_id, LANDED)
    with jobs.open_store() as store:
        queued = set_cli._names_for_job(jobs.get(store, job_id))[-1]
    twin = _recorded(cfg, held, queued)
    done = _unresolved(job_id)
    detail = done["cause"]["detail"]
    assert (detail["remote_id"], detail["twin"]) == (remote_id, twin)
    assert held.renamed == []
    assert set(ledger.set_playlist_names(cfg)) == {LANDED, queued}


def test_the_frozen_name_ranks_ahead_of_the_landing_record(account, monkeypatch):
    """With OLD frozen, a stale record under the landing's name is the twin."""
    cfg, _fake, held = account
    job = _succeeded_set_job(cfg, OLD)
    kept = _recorded(cfg, held, OLD)
    _landed(cfg, job.job_id, LANDED)
    stale = _recorded(cfg, held, LANDED)
    _inspiration_named(monkeypatch, NEW)
    code, done = drive(["export", "set", "--rename", job.job_id])
    assert code == int(ExitCode.PRECONDITION), done
    assert (done["cause"]["detail"]["remote_id"], done["cause"]["detail"]["twin"]) == (kept, stale)
    assert f"{kept} under {OLD!r}" in done["cause"]["message"]


def test_recorded_names_reads_every_landing_of_the_job_the_newest_first(account):
    cfg, _fake, _held = account
    _landed(cfg, "job-a", "10_10_26 First Part", stamp="2026-10-10T16:09:29Z-0001")
    _landed(cfg, "job-a", "10_11_26 Second Part", stamp="2026-10-11T16:09:29Z-0002")
    _landed(cfg, "job-a", "10_11_26 Second Part", stamp="2026-10-11T17:00:00Z-0003")
    _landed(cfg, "job-b", "10_12_26 Another Set", stamp="2026-10-12T16:09:29Z-0004")
    newest_first = ("10_11_26 Second Part", "10_10_26 First Part")
    assert set_playlist.recorded_names(cfg, "job-a") == newest_first
