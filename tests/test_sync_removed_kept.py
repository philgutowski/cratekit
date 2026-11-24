"""R-1716: ``crate sync removed`` keeps each synced playlist it read whole, so a stopped run continues.

A run that finds a removal reads every synced playlist, about two calls each,
and on Phillip's account stopped at the call ceiling and again at the hour's
read line with nothing offered, every run reading again what the last had
read. These drive the verb on ``tests/test_sync_removed.py``'s landed pass
with the account's calls counted the way the gate counts them, the ceiling and
the hour raised as the gate's own park. D1 applies.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from datetime import datetime, timedelta, timezone

import pytest

from cratekit.core import config, jobs, provider_gate
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.label import tidal_catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.sync import playlists, removed, removed_cli, removed_kept, unavailable
from tests._sync_builders import exited
from tests.cli_drive import drive
from tests.label_fakes import FakePagedPlaylist
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_sync_removed import SUNSET, VERB, Account, Listed, _by_title, _run, track
from tests.test_sync_removed import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_sync_removed import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_sync_removed import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_sync_removed import five_landed as five_landed  # noqa: PLC0414
from tests.test_sync_removed import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_sync_removed import library as library  # noqa: PLC0414
from tests.test_sync_removed import machine as machine  # noqa: PLC0414
from tests.test_sync_removed import native_library as native_library  # noqa: PLC0414
from tests.test_sync_removed import offline as offline  # noqa: PLC0414
from tests.test_sync_removed import pinned_day as pinned_day  # noqa: PLC0414
from tests.test_sync_removed import silence as silence  # noqa: PLC0414

NOW = datetime(2026, 11, 23, 20, 0, tzinfo=timezone.utc)
STAMP = "2026-11-20T09:15:00+00:00"
#: A write an hour before the run, long settled.
SETTLED_WRITE = "2026-11-23T19:00:00+00:00"
#: A write ten minutes before the run, which the provider may not serve yet.
FRESH_WRITE = "2026-11-23T19:50:00+00:00"
#: The calls one read of a playlist makes live: the open and one page (R-1716).
PER_PLAYLIST = 2
#: The account listing's page, as the adapter walks it.
LISTING_PAGE = 50
#: The pass's downloaded playlist, as ``_five`` lands it.
DOWNLOADED = "pl-a"


class Clock:
    """The moment ``unavailable.now`` answers, which both stores read."""

    def __init__(self, monkeypatch, moment: datetime = NOW) -> None:
        self.moment = moment
        monkeypatch.setattr(unavailable, "now", lambda: self.moment)


class Counted(Account):
    """The account with every call counted, one command's ceiling and the hour's line raising
    the gate's own park, as ``provider_gate`` raises it."""

    def __init__(self, monkeypatch) -> None:
        super().__init__(monkeypatch)
        self.ceiling: int | None = None
        self.hour_line: int | None = None
        self.command = 0
        self.hour = 0
        self.asked: list[str] = []
        self.per_playlist = PER_PLAYLIST
        fake = self.fake
        reader, lister, hearts = fake.playlist_for, fake.account_playlists, fake.favourite_tracks

        def playlist_for(reference: str):
            self.tick(self.per_playlist)
            self.asked.append(reference)
            return reader(reference)

        def account_playlists():
            self.tick(max(1, math.ceil(len(fake.account) / LISTING_PAGE)))
            return lister()

        def favourite_tracks():
            self.tick(1)
            return hearts()

        monkeypatch.setattr(fake, "playlist_for", playlist_for)
        monkeypatch.setattr(fake, "account_playlists", account_playlists)
        monkeypatch.setattr(fake, "favourite_tracks", favourite_tracks)

    def tick(self, calls: int) -> None:
        for _one in range(calls):
            if self.ceiling is not None and self.command >= self.ceiling:
                said = f"this command made {self.command} provider calls, its ceiling"
                parked = refuse(provider_gate.CEILING, said, detail={"ceiling": self.ceiling})
                raise jobs.Parked(parked.cause)
            if self.hour_line is not None and self.hour >= self.hour_line:
                said = f"the hour's {self.hour_line} calls are spent"
                raise jobs.Parked(refuse(provider_gate.BUDGET, said).cause)
            self.command += 1
            self.hour += 1

    def stamped(self, playlist_id: str, name: str, tracks: list[Listed], *,
                updated: str | None = STAMP) -> None:
        """Listed with ``tracks``, its count and a last updated stamp."""
        self.fake.playlists[playlist_id] = FakePagedPlaylist(tracks, declared=len(tracks))
        self.fake.account.append(AccountPlaylist(
            playlist_id=playlist_id, name=name, tracks=len(tracks), updated=updated
        ))

    def written(self, playlist_id: str, tracks: list[Listed], *,
                updated: str = SETTLED_WRITE) -> None:
        """A write to the account: the playlist holds ``tracks`` and the listing says so."""
        self.fake.playlists[playlist_id] = FakePagedPlaylist(tracks, declared=len(tracks))
        self.listed_as(playlist_id, len(tracks), updated)

    def listed_as(self, playlist_id: str, tracks: int, updated: str) -> None:
        """The account's listing names ``playlist_id`` with ``tracks`` and ``updated``."""
        self.fake.account[:] = [
            AccountPlaylist(one.playlist_id, one.name, tracks, updated)
            if one.playlist_id == playlist_id
            else one
            for one in self.fake.account
        ]

    def command_run(self) -> tuple[int, dict]:
        """One command, its own ceiling counted from nothing."""
        self.command = 0
        return drive(VERB)


def _others(count: int) -> list[str]:
    return [f"acc-other-{n:03d}" for n in range(count)]


def _synced(account: Counted, count: int) -> list[str]:
    """The landed pass's downloaded playlist with New1 taken off, and ``count`` other synced
    playlists, each held as taken by the legacy prefix, none holding a new track."""
    account.stamped(DOWNLOADED, SUNSET, [track("Held1"), track("New2"), track("Held2"), track("Held3")])
    names = _others(count)
    for n, playlist_id in enumerate(names):
        account.stamped(
            playlist_id,
            f"{playlists.SWEPT_PREFIX}Other {n}",
            [track(f"Other {n}"), track(f"Other {n} B")],
        )
    return names


def _counted(monkeypatch, count: int, clock=Clock) -> tuple[Clock, Counted, list[str]]:
    """The clock, the counted account and the ``count`` other synced playlists it lists."""
    pinned = clock(monkeypatch)
    account = Counted(monkeypatch)
    return pinned, account, _synced(account, count)


def _parked(account: Counted) -> dict:
    """One command parked by the gate, as policy refuses it."""
    return exited(account.command_run(), ExitCode.REFUSED_BY_POLICY)


def _asked(account: Counted) -> dict:
    """One command that read the account and asks its gate."""
    return exited(account.command_run(), ExitCode.DECISION_REQUIRED)


def _stopped(out: dict) -> None:
    """A run stopped by a park: blocked, nothing offered, no plan."""
    assert out["outcome"] == "blocked", out
    assert "items" not in (out.get("data") or {}), out


def _kept_document(cfg: config.Config) -> dict:
    return json.loads(config.state_path(removed_kept.STATE_KEY, cfg).read_text())


def _other(n: int, *more: str) -> list[Listed]:
    """The tracks the ``n``th other synced playlist holds, ``more`` added after them."""
    return [track(f"Other {n}"), track(f"Other {n} B"), *(track(one) for one in more)]


# The scenarios the brief names


def test_a_run_stopped_at_its_ceiling_and_continued_reads_no_playlist_twice(
    five_landed, monkeypatch
):
    _clock, account, others = _counted(monkeypatch, 20)
    # The listing's page, the downloaded playlist, then eight others: a stop part way.
    account.ceiling = 1 + PER_PLAYLIST + 8 * PER_PLAYLIST

    first = _parked(account)
    _stopped(first)
    assert first["cause"]["reason"] == provider_gate.CEILING
    assert "9 synced playlist(s) read whole are held, 9 of them read on this run" in first[
        "cause"
    ]["message"]
    assert first["cause"]["detail"]["kept"] == 9
    second = _parked(account)
    _stopped(second)
    assert second["cause"]["detail"]["kept"] == 18
    account.ceiling = None

    answers = _by_title(_run())

    read = Counter(account.asked)
    assert set(read) == {DOWNLOADED, *others}
    assert max(read.values()) == 1, read
    assert answers["New1"]["action"] == removed.OFFERED


def test_a_continuation_after_a_write_reads_the_changed_playlist_again_and_only_it(
    five_landed, monkeypatch
):
    _clock, account, others = _counted(monkeypatch, 6)
    account.ceiling = 1 + PER_PLAYLIST + 4 * PER_PLAYLIST
    _parked(account)
    account.ceiling = None
    # New1, taken off the downloaded playlist, is put on a playlist read and kept.
    account.written(others[1], _other(1, "New1"))

    answers = _by_title(_run())

    read = Counter(account.asked)
    assert read[others[1]] == 2
    assert all(read[one] == 1 for one in [DOWNLOADED, *others] if one != others[1]), read
    assert answers["New1"]["action"] == removed.KEPT
    assert answers["New1"]["why"] == removed.ON_ANOTHER


@pytest.mark.parametrize("moved", ["stamp", "count"])
def test_a_playlist_whose_stamp_or_count_moved_is_read_again(five_landed, monkeypatch, moved):
    _clock, account, others = _counted(monkeypatch, 2)
    _run()
    first = Counter(account.asked)
    if moved == "stamp":
        account.written(others[0], _other(0))
    else:
        account.written(others[0], _other(0, "Added"), updated=STAMP)

    _run()

    # READ ONCE, then held again under its new mark for the second command.
    again = Counter(account.asked) - first
    assert dict(again) == {others[0]: 1}


def test_a_playlist_written_lately_is_read_on_every_run_until_its_stamp_settles(
    five_landed, monkeypatch
):
    """The provider serves old rows for minutes after a write, so a read under a fresh stamp
    is never held (round one's finding 2)."""
    clock, account, others = _counted(monkeypatch, 2)
    account.written(others[0], _other(0), updated=FRESH_WRITE)

    account.command_run()
    account.command_run()
    assert Counter(account.asked)[others[0]] == 2
    clock.moment = NOW + removed_kept.SETTLED
    account.command_run()
    account.command_run()

    assert Counter(account.asked)[others[0]] == 3
    assert Counter(account.asked)[others[1]] == 1


def test_a_read_that_lags_its_listing_is_never_held_and_never_answers_a_later_run(
    five_landed, monkeypatch
):
    """The listing counts New1 added to another synced playlist while the read still serves
    the old rows: the run reads it as it is served, holds nothing, and the next run, once the
    provider serves the add, keeps New1 (round one's finding 2)."""
    _clock, account, others = _counted(monkeypatch, 2)
    account.listed_as(others[0], 3, SETTLED_WRITE)
    _asked(account)
    assert others[0] not in _kept_document(config.load())["reads"]
    account.fake.playlists[others[0]] = FakePagedPlaylist(_other(0, "New1"), declared=3)

    answers = _by_title(_run())

    assert answers["New1"]["action"] == removed.KEPT
    assert answers["New1"]["why"] == removed.ON_ANOTHER


def test_a_stop_before_any_read_still_names_what_the_store_holds(five_landed, monkeypatch):
    """Round one's finding 1: the hour still spent, the next run parks at the listing and says
    how many reads are held, not none."""
    _clock, account, _others = _counted(monkeypatch, 6)
    account.ceiling = 1 + PER_PLAYLIST + 3 * PER_PLAYLIST
    _parked(account)
    account.ceiling = 0

    again = _parked(account)

    assert again["cause"]["detail"]["kept"] == 4
    assert "4 synced playlist(s) read whole are held, 0 of them read on this run" in again[
        "cause"
    ]["message"]


def _unwritable(monkeypatch) -> None:
    def refused(*_args, **_kwargs):
        raise OSError("read-only file system")

    monkeypatch.setattr(config, "atomic_write_bytes", refused)


def test_a_stop_whose_reads_could_not_be_held_says_so_and_counts_none(five_landed, monkeypatch):
    _clock, account, _others = _counted(monkeypatch, 4)
    account.ceiling = 1 + PER_PLAYLIST + 2 * PER_PLAYLIST
    _unwritable(monkeypatch)

    stopped = _parked(account)

    assert stopped["cause"]["detail"]["kept"] == 0
    assert "could not be held (OSError: read-only file system)" in stopped["cause"]["message"]


def test_the_gate_says_the_plan_took_playlists_from_held_reads(five_landed, monkeypatch):
    """Round one's finding 3: the person answering the gate is told."""
    _clock, account, _others = _counted(monkeypatch, 3)
    fresh = _asked(account)
    assert "held reads" not in json.dumps(fresh["cause"]["detail"])

    held = _asked(account)

    assert "4 of the 4 synced playlist(s) were taken from a read made whole" in json.dumps(
        held["cause"]["detail"]
    )


def test_a_stopped_run_offers_nothing_and_a_continuation_with_a_short_playlist_offers_nothing(
    five_landed, monkeypatch
):
    _clock, account, others = _counted(monkeypatch, 4)
    account.fake.playlists[others[3]] = FakePagedPlaylist([track("Other 3")], declared=2)
    account.ceiling = 1 + PER_PLAYLIST + 2 * PER_PLAYLIST
    _stopped(_parked(account))
    account.ceiling = None

    out = _run()

    assert out["data"]["totals"]["partial"] is True
    assert out["data"]["totals"][removed.OFFERED] == 0
    assert any(one["code"] == removed_cli.PARTIAL for one in out["warnings"])
    # NEVER KEPT, so the next run asks it again.
    assert others[3] not in _kept_document(config.load())["reads"]
    _run()
    assert Counter(account.asked)[others[3]] == 2


@pytest.mark.parametrize(
    ("synced", "per_playlist", "hours"),
    [
        # The card's own fixture: about 600 synced playlists at two calls each.
        (600, 2, 2),
        # The measured account: 717 playlists at about 3.25 calls each (cutover, sitting 101).
        (717, 3, 3),
    ],
)
def test_a_large_account_finishes_in_the_hours_its_calls_need_reading_each_playlist_once(
    five_landed, monkeypatch, synced, per_playlist, hours
):
    """Each command under the default ceiling and each hour under its read line, the clock
    moved an hour at each hour stop; no playlist is read twice."""
    clock = Clock(monkeypatch)
    account = Counted(monkeypatch)
    account.per_playlist = per_playlist
    others = _synced(account, synced - 1)
    settings = provider_gate.GateSettings()
    account.ceiling = provider_gate.ceiling(settings)
    account.hour_line = provider_gate.line_for(settings, reserve=False)
    assert (account.ceiling, account.hour_line) == (500, 1125)

    spent, runs = 1, 0
    while True:
        runs += 1
        assert runs <= 12, "the step never finished"
        code, out = account.command_run()
        if code == int(ExitCode.DECISION_REQUIRED):
            break
        _stopped(out)
        assert out["cause"]["reason"] in (provider_gate.CEILING, provider_gate.BUDGET), out
        if out["cause"]["reason"] == provider_gate.BUDGET:
            # The hour's calls leave the window: the next hour begins.
            spent += 1
            account.hour = 0
            clock.moment += timedelta(hours=1)

    read = Counter(account.asked)
    assert set(read) == {DOWNLOADED, *others}
    assert max(read.values()) == 1
    assert spent == hours, (spent, runs)
    assert spent * timedelta(hours=1) < removed_kept.HELD_FOR
    # THE STEP FINISHED: New1 is offered at the gate.
    assert out["cause"]["detail"]["gate"] == removed_cli.CONFIRM_GATE


def test_a_plan_from_kept_reads_is_the_plan_from_fresh_reads(five_landed, monkeypatch):
    clock, account, _others = _counted(monkeypatch, 5)
    asked = _asked(account)
    decide = ["run", "decide", asked["run_id"], removed_cli.CONFIRM_GATE, "abort"]
    exited(drive([*decide, "--actor", "a-person"]))
    # Past the hours a read is kept, so this command reads every playlist again.
    clock.moment = NOW + removed_kept.HELD_FOR
    fresh = exited(drive(["--run", asked["run_id"], *VERB]))
    assert not any(one["code"] == removed_kept.FROM_KEPT for one in fresh["warnings"])
    read = len(account.asked)

    kept = exited(drive(["--run", asked["run_id"], *VERB]))

    assert len(account.asked) == read
    assert any(one["code"] == removed_kept.FROM_KEPT for one in kept["warnings"])
    assert kept["data"] == fresh["data"]


def test_a_read_past_its_hours_or_of_a_playlist_with_no_stamp_is_read_again(
    five_landed, monkeypatch
):
    clock, account, others = _counted(monkeypatch, 2)
    account.stamped("acc-unstamped", f"{playlists.SWEPT_PREFIX}Unstamped", [track("U")], updated=None)
    _asked(account)
    first = Counter(account.asked)
    assert first["acc-unstamped"] == 1

    account.command_run()
    assert (Counter(account.asked) - first) == Counter({"acc-unstamped": 1})

    clock.moment = NOW + removed_kept.HELD_FOR
    before = Counter(account.asked)
    account.command_run()
    assert set(Counter(account.asked) - before) == {DOWNLOADED, *others, "acc-unstamped"}


def test_retire_reads_through_the_same_store(five_landed, monkeypatch):
    _clock, account, others = _counted(monkeypatch, 3)
    _run()
    asked = len(account.asked)

    out = exited(drive([*VERB, "--retire"]))

    assert out["outcome"] == "no_op"
    assert len(account.asked) == asked
    assert out["data"]["totals"]["playlists read"] == len(others) + 1


# The store itself


@pytest.fixture
def pinned(monkeypatch) -> Clock:
    """The clock every store test reads, a read made at NOW unless moved."""
    return Clock(monkeypatch)


@pytest.fixture
def library_cfg(native_library, pinned) -> config.Config:
    """The landing suite's configuration, the clock pinned at NOW."""
    cfg, _root = native_library
    return cfg


def _listing(account: str = "acc-x", state: str = removed.READ) -> removed.Listing:
    if state != removed.READ:
        return removed.Listing(account=account, name="X", state=state)
    return removed.Listing(
        account=account,
        name="X",
        state=removed.READ,
        refs=frozenset({"tid-1", "tid-2"}),
        isrcs=frozenset({"USX"}),
        recordings=frozenset({"probe one"}),
    )


def _shown(account: str = "acc-x", *, tracks: int | None = 2, updated: str | None = STAMP):
    return AccountPlaylist(account, "X", tracks, updated)


def _keep(store: removed_kept.SyncedReads, *accounts: str) -> None:
    """A whole read of each of ``accounts``, kept under the listing's mark."""
    for account in accounts:
        store.keep(account, _shown(account), _listing(account))


def _flushed(cfg: config.Config, moment: datetime, *accounts: str) -> removed_kept.SyncedReads:
    """A store at ``moment`` that kept a whole read of each of ``accounts``, written out."""
    store = removed_kept.SyncedReads(cfg, moment)
    _keep(store, *accounts)
    store.flush()
    return store


@pytest.mark.parametrize(
    ("tracks", "updated"),
    [
        (None, STAMP),
        (2, None),
        (2, ""),
        (2, "  "),
        (2, "not a time"),
        (2, "2026-11-20T09:15:00"),
        (True, STAMP),
        (-1, STAMP),
    ],
)
def test_a_listing_with_no_count_or_no_stamp_marks_nothing(tracks, updated):
    assert removed_kept.mark_of(_shown(tracks=tracks, updated=updated)) is None
    assert removed_kept.mark_of(None) is None


def test_a_kept_read_comes_back_whole_and_only_while_the_listing_says_it_stands(library_cfg):
    cfg = library_cfg
    _flushed(cfg, NOW, "acc-x")
    later = removed_kept.SyncedReads(cfg, NOW + removed_kept.HELD_FOR - timedelta(seconds=1))

    assert later.get("acc-x", _shown()) == _listing()
    assert later.get("acc-x", None) is None
    assert later.get("acc-x", _shown(tracks=3)) is None
    assert later.get("acc-x", _shown(updated="2026-11-21T00:00:00+00:00")) is None
    assert later.get("acc-y", _shown("acc-y")) is None
    assert removed_kept.SyncedReads(cfg, NOW + removed_kept.HELD_FOR).get("acc-x", _shown()) is None
    assert removed_kept.SyncedReads(cfg, NOW - timedelta(seconds=1)).get("acc-x", _shown()) is None


def test_a_read_whose_count_differs_from_the_listing_or_under_a_fresh_stamp_is_not_held(
    library_cfg
):
    cfg = library_cfg
    store = removed_kept.SyncedReads(cfg, NOW)
    store.keep("acc-more", _shown("acc-more", tracks=3), _listing("acc-more"))
    store.keep("acc-fewer", _shown("acc-fewer", tracks=1), _listing("acc-fewer"))
    store.keep("acc-fresh", _shown("acc-fresh", updated=FRESH_WRITE), _listing("acc-fresh"))
    at_line = (NOW - removed_kept.SETTLED).isoformat()
    store.keep("acc-settled", _shown("acc-settled", updated=at_line), _listing("acc-settled"))
    store.flush()

    assert set(_kept_document(cfg)["reads"]) == {"acc-settled"}


#: Every state a listing can be in, read off the module, so a new one joins.
STATES = sorted(removed.NOT_WHOLE | removed.HOLDING | {removed.RETIRED})


def test_the_states_are_every_one_the_reader_answers():
    assert set(STATES) == {"read", "gone", "unreadable", "short", "empty", "withheld", "retired"}


@pytest.mark.parametrize("state", [one for one in STATES if one != removed.READ])
def test_only_a_read_whole_is_kept_and_a_read_not_whole_now_drops_the_kept_one(
    library_cfg, state
):
    cfg = library_cfg
    store = removed_kept.SyncedReads(cfg, NOW)
    _keep(store, "acc-x")
    # COUNTED NONE, so the count guard alone cannot refuse an empty listing not read whole.
    store.keep("acc-x", _shown(tracks=0), _listing(state=state))
    store.flush()

    assert removed_kept.SyncedReads(cfg, NOW).get("acc-x", _shown()) is None
    assert _kept_document(cfg)["reads"] == {}


def _rewritten(cfg: config.Config, document: dict) -> None:
    config.state_path(removed_kept.STATE_KEY, cfg).write_text(json.dumps(document))


def test_a_read_made_by_another_reader_is_not_trusted(library_cfg):
    cfg = library_cfg
    _flushed(cfg, NOW, "acc-x")
    document = _kept_document(cfg)
    document["reads"]["acc-x"]["reader"] = removed_kept.READER + 1
    _rewritten(cfg, document)

    assert removed_kept.SyncedReads(cfg, NOW).get("acc-x", _shown()) is None


@pytest.mark.parametrize(
    "text", ["not json", "[]", '{"version": 2, "reads": {}}', '{"version": 1, "reads": []}']
)
def test_a_document_that_cannot_be_used_reads_as_nothing_kept_and_says_so(native_library, text):
    cfg, _root = native_library
    config.state_path(removed_kept.STATE_KEY, cfg).write_text(text)

    store = removed_kept.SyncedReads(cfg, NOW)

    assert store.entries == {}
    assert store.get("acc-x", _shown()) is None
    assert [one["code"] for one in store.warnings()] == [removed_kept.UNREAD]


def test_a_refused_write_is_said_and_never_raised(library_cfg, monkeypatch):
    _unwritable(monkeypatch)
    store = _flushed(library_cfg, NOW, "acc-x")

    assert [one["code"] for one in store.warnings()] == [removed_kept.UNKEPT]
    assert "read-only file system" in store.unkept


def test_the_store_is_written_every_fifty_new_reads_and_drops_reads_past_their_hours(
    library_cfg, pinned
):
    cfg = library_cfg
    pinned.moment = NOW - removed_kept.HELD_FOR
    _flushed(cfg, pinned.moment, "acc-old")
    pinned.moment = NOW
    store = removed_kept.SyncedReads(cfg, NOW)
    _keep(store, *(f"acc-{n}" for n in range(removed_kept.FLUSH_EVERY - 1)))
    assert set(_kept_document(cfg)["reads"]) == {"acc-old"}

    _keep(store, "acc-last")

    reads = _kept_document(cfg)["reads"]
    assert len(reads) == removed_kept.FLUSH_EVERY
    assert "acc-old" not in reads


def test_the_store_is_declared_library_scoped_and_never_restored():
    (entry,) = [one for one in config.STATE_FILES if one.key == removed_kept.STATE_KEY]
    assert entry.root.name == "LIBRARY"
    assert entry.snapshot.name == "NEVER_RESTORED"


def test_the_adapter_lists_the_providers_last_updated_stamp_and_none_when_it_gave_none():
    from tests.test_label_tidal_catalogue import AccountEntry, AccountUser, FakeClient

    stamped = AccountEntry("pl-stamped", "Warmup", 42, num_tracks=12)
    stamped.last_updated = datetime(2026, 11, 20, 9, 15, tzinfo=timezone.utc)
    spelled = AccountEntry("pl-spelled", "Spelled", 42, num_tracks=3)
    spelled.last_updated = STAMP
    blank = AccountEntry("pl-blank", "Blank", 42, num_tracks=3)
    blank.last_updated = " "
    client = FakeClient()
    client.user = AccountUser(42, [stamped, spelled, blank, AccountEntry("pl-none", "None", 42, 1)])

    listed = {
        one.playlist_id: one.updated
        for one in tidal_catalogue.TidalCatalogue(client).account_playlists()
    }

    assert listed == {
        "pl-stamped": "2026-11-20T09:15:00+00:00",
        "pl-spelled": STAMP,
        "pl-blank": None,
        "pl-none": None,
    }


def test_two_overlapping_runs_each_keep_what_they_read(library_cfg, pinned):
    """Round one's finding 6: the later write merges the earlier, the later read winning."""
    cfg = library_cfg
    first = removed_kept.SyncedReads(cfg, NOW)
    second = removed_kept.SyncedReads(cfg, NOW)
    _keep(first, "acc-1", "acc-2", "acc-3")
    first.flush()
    pinned.moment = NOW + timedelta(minutes=5)
    _keep(second, "acc-3", "acc-4")
    second.flush()

    reads = _kept_document(cfg)["reads"]
    assert set(reads) == {"acc-1", "acc-2", "acc-3", "acc-4"}
    assert reads["acc-3"]["read_at"] == (NOW + timedelta(minutes=5)).isoformat()


def test_a_playlist_one_run_dropped_stays_dropped_over_an_older_write(library_cfg, pinned):
    cfg = library_cfg
    _flushed(cfg, NOW, "acc-x")
    pinned.moment = NOW + timedelta(minutes=5)
    dropping = removed_kept.SyncedReads(cfg, pinned.moment)
    dropping.keep("acc-x", _shown(), _listing(state=removed.SHORT))
    dropping.flush()

    assert _kept_document(cfg)["reads"] == {}


def test_a_store_whose_clock_is_behind_keeps_a_newer_read_another_run_wrote(library_cfg, pinned):
    cfg = library_cfg
    pinned.moment = NOW + timedelta(seconds=2)
    _flushed(cfg, pinned.moment, "acc-ahead")
    pinned.moment = NOW
    _flushed(cfg, NOW, "acc-behind")

    assert set(_kept_document(cfg)["reads"]) == {"acc-ahead", "acc-behind"}


class Ticking:
    """``unavailable.now`` moving a second at every reading, as the real clock does."""

    def __init__(self, monkeypatch, moment: datetime = NOW) -> None:
        self.moment = moment

        def now() -> datetime:
            self.moment += timedelta(seconds=1)
            return self.moment

        monkeypatch.setattr(unavailable, "now", now)


def test_a_stop_on_a_moving_clock_counts_the_reads_of_the_run_that_stopped(
    five_landed, monkeypatch
):
    """Round two's finding 1: each read is stamped when made, after the run began, and the stop
    still counts it."""
    _clock, account, _others = _counted(monkeypatch, 20, Ticking)
    account.ceiling = 1 + PER_PLAYLIST + 8 * PER_PLAYLIST

    first = _parked(account)
    assert first["cause"]["detail"]["kept"] == 9
    second = _parked(account)

    assert second["cause"]["detail"]["kept"] == 18
    assert len(_kept_document(config.load())["reads"]) == 18


def test_standing_counts_only_reads_under_their_hours_at_now(library_cfg, pinned):
    cfg = library_cfg
    pinned.moment = NOW - removed_kept.HELD_FOR
    _flushed(cfg, pinned.moment, "acc-old")
    pinned.moment = NOW
    later = removed_kept.SyncedReads(cfg, NOW)
    _keep(later, "acc-new")

    assert later.standing() == 1


def test_a_drop_holds_against_a_read_made_before_it_and_yields_to_one_after(library_cfg, pinned):
    """Round two's finding 4: compared with when this run dropped it, not when it began."""
    cfg = library_cfg
    dropping = removed_kept.SyncedReads(cfg, NOW)
    pinned.moment = NOW + timedelta(minutes=1)
    _flushed(cfg, pinned.moment, "acc-x")
    pinned.moment = NOW + timedelta(minutes=5)
    dropping.entries["acc-x"] = dict(_kept_document(cfg)["reads"]["acc-x"])
    dropping.keep("acc-x", _shown(), _listing(state=removed.SHORT))
    dropping.flush()
    assert _kept_document(cfg)["reads"] == {}

    again = removed_kept.SyncedReads(cfg, pinned.moment)
    pinned.moment = NOW + timedelta(minutes=6)
    _keep(again, "acc-y")
    pinned.moment = NOW + timedelta(minutes=7)
    _flushed(cfg, pinned.moment, "acc-x")
    again.dropped["acc-x"] = NOW + timedelta(minutes=5)
    again.flush()

    assert set(_kept_document(cfg)["reads"]) == {"acc-x", "acc-y"}


def test_the_gate_line_counts_the_synced_playlists_and_the_held_ones_apart(five_landed, monkeypatch):
    clock, account, others = _counted(monkeypatch, 3)
    account.command_run()
    account.written(others[0], _other(0), updated=FRESH_WRITE)
    clock.moment = NOW + timedelta(minutes=1)

    held = _asked(account)

    assert "3 of the 4 synced playlist(s) were taken from a read made whole" in json.dumps(
        held["cause"]["detail"]
    )


@pytest.mark.parametrize("key", ["refs", "isrcs", "recordings"])
@pytest.mark.parametrize("damaged", ["tid-1", ["tid-1", 2], None])
def test_a_held_read_whose_sets_do_not_hold_together_is_read_again(library_cfg, key, damaged):
    """The mutation table's K17: a damaged set is never read as empty, which would claim the
    playlist holds nothing and offer its tracks."""
    cfg = library_cfg
    _flushed(cfg, NOW, "acc-x")
    document = _kept_document(cfg)
    document["reads"]["acc-x"][key] = damaged
    _rewritten(cfg, document)

    assert removed_kept.SyncedReads(cfg, NOW).get("acc-x", _shown()) is None
