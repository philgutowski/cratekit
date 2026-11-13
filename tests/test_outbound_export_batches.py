"""U270. Exporting a crate to the account adds its tracks a hundred to a request.

Phillip's answer of 2026-11-13: an export keeps one job item per track, and
the driver hands the export worker a batch of them, whose tracks go to the
account in one add request. Each track is recorded only after the provider's
answer names it, and an answer that names part of the batch is settled by one
read of the playlist. The card's four scenarios are here, each on the fake
account and the riskiest on the real provider client over the counting
transport U255 built: a full batch, a batch answered in part, a stop between
the request and the ledger write followed by a resume, and a playlist a person
edited between two batches. The request count is the assertion, never a clock.

What each write test holds is what the brief asks of it: the ledger never
records a track the playlist does not hold, a resume adds nothing twice and
loses nothing, and a person's edit is never overwritten.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import artifacts, export, ledger, source
from tests import outbound_fakes
from tests.cli_drive import approve_and_queue, drive
from tests.test_config import valid_data
from tests.test_outbound_add_requests import Account, _adapter, _ids

KEY = "crate-one"


@pytest.fixture
def cfg(tmp_path, monkeypatch):
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


def _recorded(cfg) -> dict:
    path = config.state_path("outbound_writes", cfg)
    return json.loads(path.read_text())["playlists"] if path.exists() else {}


def _plan(*pairs: tuple[str, str]) -> export.ExportPlan:
    return export.ExportPlan(playlist_key=KEY, name="Crate One", matched=pairs, unmatched=())


def _rows(*tracks: str) -> tuple[tuple[str, str], ...]:
    return tuple((f"row-{one}", one) for one in tracks)


class LandsThenFails(outbound_fakes.FakeAccount):
    """The add lands on the playlist and the call then raises, as a refused
    read after the provider's POST does (R-1543), before anything is recorded."""

    def __init__(self, *args, raising: Exception, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.raising: Exception | None = raising

    def add_tracks(self, playlist_id, remote_ids):
        held = super().add_tracks(playlist_id, remote_ids)
        if self.raising is not None:
            raising, self.raising = self.raising, None
            raise raising
        return held


def _transient() -> CratekitError:
    return refuse(
        "unavailable-transient",
        "the read after the add was refused",
        remedy=Remedy.RETRY_LATER,
        retryable=True,
        origin=("test",),
    )


# ═══════════════════════════════════════════════════════════════════════════
# The writer, on the fake account
# ═══════════════════════════════════════════════════════════════════════════


def test_a_full_batch_is_one_add_and_one_record_of_every_track(cfg):
    account = outbound_fakes.FakeAccount()
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))

    report = export.apply(cfg, account, _plan(*_rows("t1", "t2", "t3")))

    assert account.chunks == [("pl-1", ("t1", "t2", "t3"))]
    assert report.added == ("t1", "t2", "t3")
    assert report.outcomes == tuple(
        (f"row-{one}", one, export.ADDED) for one in ("t1", "t2", "t3")
    )
    record = _recorded(cfg)[KEY]
    assert record["added"] == ["t1", "t2", "t3"]
    assert record["rows"] == {"row-t1": "t1", "row-t2": "t2", "row-t3": "t3"}
    assert "sending" not in record


def test_a_batch_answered_in_part_records_only_what_the_answer_names(cfg):
    account = outbound_fakes.FakeAccount()
    account.unaddable.add("t2")
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))

    report = export.apply(cfg, account, _plan(*_rows("t1", "t2", "t3")))

    assert report.added == ("t1", "t3")
    assert report.refused == ("t2",)
    assert dict((row, said) for row, _track, said in report.outcomes) == {
        "row-t1": export.ADDED,
        "row-t2": export.REFUSED,
        "row-t3": export.ADDED,
    }
    record = _recorded(cfg)[KEY]
    assert record["added"] == ["t1", "t3"]
    assert "row-t2" not in record["rows"]
    assert "sending" not in record


def test_two_rows_matched_to_one_track_send_it_once_and_record_both_rows(cfg):
    account = outbound_fakes.FakeAccount()
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))

    report = export.apply(cfg, account, _plan(("a", "t1"), ("b", "t1"), ("c", "t2")))

    assert account.chunks == [("pl-1", ("t1", "t2"))]
    assert report.outcomes == (
        ("a", "t1", export.ADDED),
        ("b", "t1", export.ALREADY),
        ("c", "t2", export.ADDED),
    )
    assert _recorded(cfg)[KEY]["rows"] == {"a": "t1", "b": "t1", "c": "t2"}


def test_two_rows_matched_to_one_refused_track_are_both_refused(cfg):
    account = outbound_fakes.FakeAccount()
    account.unaddable.add("t1")
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))

    report = export.apply(cfg, account, _plan(("a", "t1"), ("b", "t1")))

    assert [said for _row, _track, said in report.outcomes] == [export.REFUSED] * 2
    assert _recorded(cfg)[KEY]["added"] == []


def test_a_track_on_the_playlist_or_recorded_is_not_sent(cfg):
    account = outbound_fakes.FakeAccount()
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))
    account.playlists["pl-1"].append("theirs")
    export.apply(cfg, account, _plan(*_rows("t1")))

    report = export.apply(cfg, account, _plan(*_rows("theirs", "t1", "t2")))

    assert account.chunks == [("pl-1", ("t1",)), ("pl-1", ("t2",))]
    assert report.already == ("theirs", "t1")
    # A TRACK A PERSON PUT THERE IS NEVER CLAIMED by being matched again.
    assert _recorded(cfg)[KEY]["added"] == ["t1", "t2"]
    assert "row-theirs" not in _recorded(cfg)[KEY]["rows"]


@pytest.mark.parametrize(
    "raising",
    [RuntimeError("the read after the add died"), jobs.Parked(_transient().cause)],
    ids=["refused-read", "ceiling-park"],
)
def test_a_stop_between_the_request_and_the_record_adds_nothing_twice_and_records_nothing_unanswered(
    cfg, raising
):
    """The card's third scenario, at the writer: the batch landed and its
    answer never came back, so nothing is recorded, and the next apply finds
    every track on the playlist, sends nothing and claims none of them, as one
    track was left before U270 (R-1543). The review drove why the read is not
    taken as the answer: it cannot tell our add from a person's."""
    account = LandsThenFails(raising=raising)
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))

    with pytest.raises(type(raising)):
        export.apply(cfg, account, _plan(*_rows("t1", "t2", "t3")))
    assert account.playlists["pl-1"] == ["t1", "t2", "t3"]
    assert _recorded(cfg)[KEY]["added"] == []

    report = export.apply(cfg, account, _plan(*_rows("t1", "t2", "t3")))

    assert account.chunks == [("pl-1", ("t1", "t2", "t3"))]
    assert account.playlists["pl-1"] == ["t1", "t2", "t3"]
    assert report.added == ()
    assert report.already == ("t1", "t2", "t3")
    assert _recorded(cfg)[KEY]["added"] == []


def test_a_stop_before_the_request_landed_sends_the_batch_again_and_records_it_once(cfg):
    """The request never reached the provider: nothing is on the playlist,
    nothing is recorded, and the next apply sends it."""
    account = outbound_fakes.FakeAccount(fail_on={"t2"}, transient=True)
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))

    with pytest.raises(CratekitError):
        export.apply(cfg, account, _plan(*_rows("t1", "t2")))
    assert _recorded(cfg)[KEY]["added"] == []
    assert account.playlists["pl-1"] == []

    account.fail_on = frozenset()
    report = export.apply(cfg, account, _plan(*_rows("t1", "t2")))

    assert report.added == ("t1", "t2")
    assert account.playlists["pl-1"] == ["t1", "t2"]
    assert [one for _pl, one in account.added] == ["t1", "t2"]
    assert _recorded(cfg)[KEY]["added"] == ["t1", "t2"]


def test_the_ledger_never_notes_a_row_for_a_track_it_does_not_hold_as_added(cfg):
    """The ledger's own guard, driven alone (round two's fourth finding): a row
    named for a track the record does not hold as added, a person's, is not
    written, whatever the caller passes."""
    account = outbound_fakes.FakeAccount()
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))
    ledger.record_playlist_tracks(cfg, KEY, landed={"row-t1": "t1"})

    ledger.record_playlist_tracks(cfg, KEY, landed={}, rows={"row-x": "theirs", "row-y": "t1"})

    record = _recorded(cfg)[KEY]
    assert record["added"] == ["t1"]
    assert record["rows"] == {"row-t1": "t1", "row-y": "t1"}


def test_a_re_export_names_the_rows_of_tracks_recorded_before_rows_were_kept(cfg):
    """Round two's third finding: a record written before R-836 holds its
    tracks and no rows, and an export that writes nothing new still names
    each recorded track's row, in one write."""
    account = outbound_fakes.FakeAccount()
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))
    ledger.record_playlist_track(cfg, KEY, "t1")
    ledger.record_playlist_track(cfg, KEY, "t2")
    account.playlists["pl-1"].extend(["t1", "t2"])

    report = export.apply(cfg, account, _plan(*_rows("t1", "t2")))

    assert report.already == ("t1", "t2")
    assert account.chunks == []
    assert _recorded(cfg)[KEY]["rows"] == {"row-t1": "t1", "row-t2": "t2"}


def test_a_person_who_took_a_track_off_between_batches_is_not_overwritten(cfg):
    """The card's fourth scenario on the fake: the first batch's track a person
    took off stays off when its row is exported again, and their own track
    stays where they put it, ahead of the second batch."""
    account = outbound_fakes.FakeAccount()
    ledger.reserve_playlist(cfg, KEY, lambda: account.create_playlist("Crate One"))
    export.apply(cfg, account, _plan(*_rows("t1", "t2")))
    account.playlists["pl-1"].remove("t1")
    account.playlists["pl-1"].append("theirs")

    report = export.apply(cfg, account, _plan(*_rows("t1", "t2", "t3", "t4")))

    assert account.playlists["pl-1"] == ["t2", "theirs", "t3", "t4"]
    assert report.added == ("t3", "t4")
    assert report.already == ("t1", "t2")


# ═══════════════════════════════════════════════════════════════════════════
# The writer, on the real provider client over the counting transport
# ═══════════════════════════════════════════════════════════════════════════


class FailsTheReadAfterAdding(Account):
    """The provider takes the add and then refuses every playlist read for a
    while: the client's own read after its POST, and the retry's."""

    def __init__(self, *uuids: str, refusals: int) -> None:
        super().__init__(*uuids)
        self.after_add = refusals

    def request(self, method, url, params=None, data=None, headers=None, **rest):
        answer = super().request(method, url, params=params, data=data, headers=headers, **rest)
        if method == "POST" and url.endswith("/items") and answer.ok and self.after_add:
            self.open_fail.extend([503] * self.after_add)
            self.after_add = 0
        return answer


def test_a_hundred_and_fifty_tracks_through_one_apply_are_two_requests_on_one_open(cfg):
    """More than the provider takes in one request: ``add_tracks`` chunks,
    each chunk one POST and the client's read after it, on the one open."""
    provider = Account("pl0")
    remote = _adapter(provider)
    ledger.reserve_playlist(cfg, KEY, lambda: "pl0")
    wanted = _ids(150)

    report = export.apply(cfg, remote, _plan(*_rows(*wanted)))

    assert report.added == tuple(wanted)
    assert provider.items["pl0"] == wanted
    assert provider.posts("pl0") == 2
    assert provider.gets("pl0") == 6
    assert provider.track_reads("pl0") == 1


def test_a_batch_answered_in_part_on_the_real_client_is_settled_by_one_read_back(cfg):
    """The card's second scenario: the provider cannot find one track, so its
    answer names the rest, and the adapter reads the playlist back once."""
    provider = Account("pl0")
    provider.missing.add("101")
    remote = _adapter(provider)
    ledger.reserve_playlist(cfg, KEY, lambda: "pl0")

    report = export.apply(cfg, remote, _plan(*_rows("100", "101", "102")))

    assert report.added == ("100", "102")
    assert report.refused == ("101",)
    assert provider.items["pl0"] == ["100", "102"]
    assert provider.posts("pl0") == 1
    # The membership's open and tracks read, the add's open and the client's
    # read after its POST, then the one read back: an open and a tracks read.
    assert provider.gets("pl0") == 7
    assert provider.track_reads("pl0") == 2
    assert _recorded(cfg)[KEY]["added"] == ["100", "102"]


def test_one_refused_read_after_a_landed_add_is_retried_on_a_fresh_open_and_recorded(cfg):
    """Round one's first finding. The POST landed and the client's read after
    it was refused once: the retry opens the playlist afresh, its add is
    skipped as duplicates, and the read back records all three. Before the
    fix the retry sent the stale tag, was refused 412, and failed the batch
    with every track on the playlist and none recorded."""
    provider = FailsTheReadAfterAdding("pl0", refusals=1)
    ledger.reserve_playlist(cfg, KEY, lambda: "pl0")
    wanted = ("100", "101", "102")

    report = export.apply(cfg, _adapter(provider), _plan(*_rows(*wanted)))

    assert report.added == wanted
    assert provider.items["pl0"] == list(wanted)
    assert provider.posts("pl0") == 2
    assert [tag for _uuid, _form, tag in provider.adds] == ['"1"', '"2"']
    assert _recorded(cfg)[KEY]["added"] == list(wanted)


def test_reads_refused_past_the_retry_fail_the_batch_and_the_resume_adds_nothing_twice(cfg):
    """The read after the add refused past every retry: the add raises with
    the batch on the playlist and nothing recorded, and the resume, a fresh
    adapter as a fresh process has, sends nothing and claims nothing."""
    provider = FailsTheReadAfterAdding("pl0", refusals=12)
    ledger.reserve_playlist(cfg, KEY, lambda: "pl0")
    wanted = ("100", "101", "102")

    with pytest.raises(CratekitError):
        export.apply(cfg, _adapter(provider), _plan(*_rows(*wanted)))
    assert provider.items["pl0"] == list(wanted)
    assert _recorded(cfg)[KEY]["added"] == []
    sent = provider.posts("pl0")

    provider.open_fail.clear()
    report = export.apply(cfg, _adapter(provider), _plan(*_rows(*wanted)))

    assert provider.posts("pl0") == sent
    assert provider.items["pl0"] == list(wanted)
    assert report.already == wanted
    assert _recorded(cfg)[KEY]["added"] == []


def test_a_track_a_person_adds_after_a_refused_add_is_never_claimed(cfg):
    """Round one's second finding. The add's open is refused, so nothing is
    sent; a person then adds one of the batch's tracks by hand. The next apply
    reads it as theirs: it is not recorded as added, so a prune never takes
    it off, and only the other track is sent."""
    provider = Account("pl0")
    remote = _adapter(provider)
    ledger.reserve_playlist(cfg, KEY, lambda: "pl0")
    remote.playlist_tracks("pl0")
    provider.open_fail.extend([503] * 6)

    with pytest.raises(CratekitError):
        export.apply(cfg, remote, _plan(("row-a", "100"), ("row-b", "101")))
    assert provider.posts("pl0") == 0
    provider.open_fail.clear()
    provider.outside_add("pl0", "101")

    report = export.apply(cfg, _adapter(provider), _plan(("row-a", "100"), ("row-b", "101")))

    assert report.added == ("100",)
    assert report.already == ("101",)
    assert provider.items["pl0"] == ["101", "100"]
    record = _recorded(cfg)[KEY]
    assert record["added"] == ["100"]
    assert record["rows"] == {"row-a": "100"}


def test_a_person_who_edited_the_playlist_between_two_batches_keeps_their_edit(cfg):
    """The card's fourth scenario on the real client. Each batch opens the
    playlist afresh, so the second carries the tag the person's write left and
    goes at the end, after their track: nothing refused, nothing moved."""
    provider = Account("pl0")
    remote = _adapter(provider)
    ledger.reserve_playlist(cfg, KEY, lambda: "pl0")
    export.apply(cfg, remote, _plan(*_rows("100", "101")))
    provider.outside_add("pl0", "7")

    report = export.apply(cfg, remote, _plan(*_rows("100", "101", "102", "103")))

    assert provider.items["pl0"] == ["100", "101", "7", "102", "103"]
    assert report.added == ("102", "103")
    assert [status for _form in provider.adds for status in [_form[2]]] == ['"1"', '"3"']
    assert provider.posts("pl0") == 2
    assert "7" not in _recorded(cfg)[KEY]["added"]


# ═══════════════════════════════════════════════════════════════════════════
# Through the driver
# ═══════════════════════════════════════════════════════════════════════════


def _crate(cfg, tracks: int) -> Path:
    return outbound_fakes.write_export(
        cfg.library.root / "outbound", crate=range(1, tracks + 1), tracks=tracks
    )


def _queue(exported: Path) -> str:
    _run, job_id = approve_and_queue(
        ["export", "playlist", outbound_fakes.CRATE, "--export", str(exported)],
        "export.playlist.confirm",
    )
    return job_id


def _resume(job_id: str) -> tuple[int, dict]:
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    return drive(cli_jobs.argv_for(job))


def _bind(monkeypatch, remote) -> None:
    monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(remote))


def test_a_job_of_two_hundred_and_fifty_tracks_makes_fifteen_requests(cfg, monkeypatch):
    """The brief's goal, through the shipped resume and the real client: three
    batches, a hundred, a hundred and fifty, each one add request. U255 left
    this at 503 requests, over the gate's ceiling of 500 for one command."""
    provider = Account("pl0")
    remote = _adapter(provider)
    monkeypatch.setattr(
        remote, "match_track", lambda **asked: str(1000 + int(asked["identity"]))
    )
    _bind(monkeypatch, remote)
    ledger.reserve_playlist(cfg, outbound_fakes.CRATE, lambda: "pl0")
    job_id = _queue(_crate(cfg, 250))

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    wanted = [str(1000 + n) for n in range(1, 251)]
    assert provider.items["pl0"] == wanted
    assert provider.posts("pl0") == 3
    # The membership's open (two GETs) and its one tracks read, then each
    # batch's open (two GETs) and the client's read after its POST.
    assert provider.gets("pl0") == 2 + 3 * 3
    assert provider.track_reads("pl0") == 1
    assert sum(provider.requests.values()) == 15
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["counts"] == {"written": 250, "already": 0, "unmatched": 0}
    assert _recorded(cfg)[outbound_fakes.CRATE]["added"] == wanted
    with jobs.open_store() as store:
        assert {str(item.state) for item in jobs.items(store, job_id)} == {"done"}
    reports = artifacts.committed(cfg, job_id)
    assert len(reports) == 250
    assert all(len(report["added"]) == 1 for report in reports)


def test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice(
    cfg, monkeypatch
):
    """The card's third scenario through the driver: a park after the batch
    landed releases the batch whole and blocks the job, and the resume adds
    nothing twice and settles every item, reading the tracks as already there
    and recording none it has no answer for (R-1543)."""
    account = LandsThenFails(catalog=dict(_catalog(3)), raising=jobs.Parked(_transient().cause))
    _bind(monkeypatch, account)
    job_id = _queue(_crate(cfg, 3))

    code, _blocked = _resume(job_id)
    assert code != int(ExitCode.OK)
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.BLOCKED
        assert {str(item.state) for item in jobs.items(store, job_id)} == {"pending"}
    assert _recorded(cfg)[outbound_fakes.CRATE]["added"] == []

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    assert account.playlists["pl-1"] == ["tid-1", "tid-2", "tid-3"]
    assert [one for _pl, one in account.added] == ["tid-1", "tid-2", "tid-3"]
    assert _recorded(cfg)[outbound_fakes.CRATE]["added"] == []
    assert resumed["data"]["progress"]["outbound"]["counts"] == {
        "written": 0,
        "already": 3,
        "unmatched": 0,
    }
    with jobs.open_store() as store:
        assert {str(item.state) for item in jobs.items(store, job_id)} == {"done"}


def test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job(
    cfg, monkeypatch
):
    """Round one's first finding as it was driven: a hundred tracks, the read
    after the add refused once, and the job succeeds with every track recorded
    once and nothing told failed."""
    provider = FailsTheReadAfterAdding("pl0", refusals=1)
    remote = _adapter(provider)
    monkeypatch.setattr(
        remote, "match_track", lambda **asked: str(1000 + int(asked["identity"]))
    )
    _bind(monkeypatch, remote)
    ledger.reserve_playlist(cfg, outbound_fakes.CRATE, lambda: "pl0")
    job_id = _queue(_crate(cfg, 100))

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    wanted = [str(1000 + n) for n in range(1, 101)]
    assert provider.items["pl0"] == wanted
    assert provider.posts("pl0") == 2
    assert _recorded(cfg)[outbound_fakes.CRATE]["added"] == wanted
    assert resumed["data"]["progress"]["outbound"]["counts"]["written"] == 100


def test_a_stop_asked_while_a_batch_is_planned_writes_none_of_it(cfg, monkeypatch):
    """Round one's third finding, the guard no test reached: a signal while a
    batch is matched ends the planning, nothing is sent, and the worker
    answers that it stopped, so the driver releases the batch whole."""
    from cratekit.export import cli as export_cli

    account = outbound_fakes.FakeAccount(catalog=dict(_catalog(3)))
    exported = _crate(cfg, 3)
    payload = {
        export_cli.PLAYLIST: outbound_fakes.CRATE,
        export_cli.NAME: outbound_fakes.CRATE,
        export_cli.EXPORT: str(exported),
    }
    asked: list[int] = []

    def stop() -> bool:
        asked.append(len(account.matches))
        return len(account.matches) == 2

    answered = export_cli.run_export_items(payload, ["1", "2", "3"], cfg, account, stop)

    assert answered is None
    assert asked == [0, 1, 2]
    assert account.chunks == [] and account.created == []
    assert _recorded(cfg) == {}


def test_a_created_playlist_is_said_once_for_the_batch(cfg, monkeypatch):
    """The create and its filing are the batch's, so the first item's report
    says them and the rest do not: one filing warning, not one per track."""
    account = outbound_fakes.FakeAccount(catalog=dict(_catalog(3)))
    _bind(monkeypatch, account)
    job_id = _queue(_crate(cfg, 3))

    code, _resumed = _resume(job_id)

    assert code == int(ExitCode.OK)
    reports = artifacts.committed(cfg, job_id)
    assert [report["created"] for report in reports] == [True, False, False]
    assert account.created == [outbound_fakes.CRATE]


def _catalog(count: int) -> list[tuple[str, str]]:
    return [(str(n), f"tid-{n}") for n in range(1, count + 1)]
