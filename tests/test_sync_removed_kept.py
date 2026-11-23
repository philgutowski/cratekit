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
from tests.cli_drive import drive
from tests.label_fakes import FakePagedPlaylist
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_sync_removed import (
    SUNSET,
    VERB,
    Account,
    Listed,
    _by_title,
    _run,
    track,
)
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
        fake = self.fake
        reader, lister, hearts = fake.playlist_for, fake.account_playlists, fake.favourite_tracks

        def playlist_for(reference: str):
            self.tick(PER_PLAYLIST)
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
                raise jobs.Parked(
                    refuse(
                        provider_gate.CEILING,
                        f"this command made {self.command} provider calls, its ceiling",
                        detail={"ceiling": self.ceiling},
                    ).cause
                )
            if self.hour_line is not None and self.hour >= self.hour_line:
                raise jobs.Parked(
                    refuse(
                        provider_gate.BUDGET,
                        f"the hour's {self.hour_line} calls are spent",
                    ).cause
                )
            self.command += 1
            self.hour += 1

    def stamped(
        self, playlist_id: str, name: str, tracks: list[Listed], *, updated: str | None = STAMP
    ) -> None:
        """Listed with ``tracks``, its count and a last updated stamp."""
        self.fake.playlists[playlist_id] = FakePagedPlaylist(tracks, declared=len(tracks))
        self.fake.account.append(
            AccountPlaylist(
                playlist_id=playlist_id, name=name, tracks=len(tracks), updated=updated
            )
        )

    def written(
        self, playlist_id: str, tracks: list[Listed], *, updated: str = "2026-11-23T20:30:00+00:00"
    ) -> None:
        """A write to the account: the playlist holds ``tracks`` and the listing says so."""
        self.fake.playlists[playlist_id] = FakePagedPlaylist(tracks, declared=len(tracks))
        self.fake.account[:] = [
            AccountPlaylist(one.playlist_id, one.name, len(tracks), updated)
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


def _stopped(out: dict) -> None:
    """A run stopped by a park: blocked, nothing offered, no plan."""
    assert out["outcome"] == "blocked", out
    assert "items" not in (out.get("data") or {}), out


def _kept_document(cfg: config.Config) -> dict:
    return json.loads(config.state_path(removed_kept.STATE_KEY, cfg).read_text())


# The scenarios the brief names


def test_a_run_stopped_at_its_ceiling_and_continued_reads_no_playlist_twice(
    five_landed, monkeypatch
):
    Clock(monkeypatch)
    account = Counted(monkeypatch)
    others = _synced(account, 20)
    # The listing's page, the downloaded playlist, then eight others: a stop part way.
    account.ceiling = 1 + PER_PLAYLIST + 8 * PER_PLAYLIST

    code, first = account.command_run()
    assert code == int(ExitCode.REFUSED_BY_POLICY), first
    _stopped(first)
    assert first["cause"]["reason"] == provider_gate.CEILING
    assert "9 synced playlist(s) read whole on this run are kept" in first["cause"]["message"]
    assert first["cause"]["detail"]["kept"] == 9
    code, second = account.command_run()
    assert code == int(ExitCode.REFUSED_BY_POLICY), second
    _stopped(second)
    account.ceiling = None

    answers = _by_title(_run())

    read = Counter(account.asked)
    assert set(read) == {DOWNLOADED, *others}
    assert max(read.values()) == 1, read
    assert answers["New1"]["action"] == removed.OFFERED


def test_a_continuation_after_a_write_reads_the_changed_playlist_again_and_only_it(
    five_landed, monkeypatch
):
    Clock(monkeypatch)
    account = Counted(monkeypatch)
    others = _synced(account, 6)
    account.ceiling = 1 + PER_PLAYLIST + 4 * PER_PLAYLIST
    assert account.command_run()[0] == int(ExitCode.REFUSED_BY_POLICY)
    account.ceiling = None
    # New1, taken off the downloaded playlist, is put on a playlist read and kept.
    account.written(others[1], [track("Other 1"), track("Other 1 B"), track("New1")])

    answers = _by_title(_run())

    read = Counter(account.asked)
    assert read[others[1]] == 2
    assert all(read[one] == 1 for one in [DOWNLOADED, *others] if one != others[1]), read
    assert answers["New1"]["action"] == removed.KEPT
    assert answers["New1"]["why"] == removed.ON_ANOTHER


@pytest.mark.parametrize("moved", ["stamp", "count"])
def test_a_playlist_whose_stamp_or_count_moved_is_read_again(five_landed, monkeypatch, moved):
    Clock(monkeypatch)
    account = Counted(monkeypatch)
    others = _synced(account, 2)
    _run()
    first = Counter(account.asked)
    listed = {one.playlist_id: one for one in account.fake.account}
    shown = listed[others[0]]
    account.fake.account[:] = [
        (
            AccountPlaylist(
                shown.playlist_id,
                shown.name,
                shown.tracks if moved == "stamp" else 3,
                "2026-11-23T20:05:00+00:00" if moved == "stamp" else shown.updated,
            )
            if one.playlist_id == others[0]
            else one
        )
        for one in account.fake.account
    ]

    _run()

    again = Counter(account.asked) - first
    assert dict(again) == {others[0]: 1}


def test_a_stopped_run_offers_nothing_and_a_continuation_with_a_short_playlist_offers_nothing(
    five_landed, monkeypatch
):
    Clock(monkeypatch)
    account = Counted(monkeypatch)
    others = _synced(account, 4)
    account.fake.playlists[others[3]] = FakePagedPlaylist([track("Other 3")], declared=2)
    account.ceiling = 1 + PER_PLAYLIST + 2 * PER_PLAYLIST
    code, stopped = account.command_run()
    assert code == int(ExitCode.REFUSED_BY_POLICY)
    _stopped(stopped)
    account.ceiling = None

    out = _run()

    assert out["data"]["totals"]["partial"] is True
    assert out["data"]["totals"][removed.OFFERED] == 0
    assert any(one["code"] == removed_cli.PARTIAL for one in out["warnings"])
    # NEVER KEPT, so the next run asks it again.
    assert others[3] not in _kept_document(config.load())["reads"]
    _run()
    assert Counter(account.asked)[others[3]] == 2


def test_six_hundred_synced_playlists_finish_in_the_next_hour_reading_each_once(
    five_landed, monkeypatch
):
    """Each command under the default ceiling, the hour under its read line, and the run
    that finishes it in the next hour; no playlist is read twice."""
    Clock(monkeypatch)
    account = Counted(monkeypatch)
    others = _synced(account, 599)
    settings = provider_gate.GateSettings()
    account.ceiling = provider_gate.ceiling(settings)
    account.hour_line = provider_gate.line_for(settings, reserve=False)
    assert (account.ceiling, account.hour_line) == (500, 1125)

    hours, runs = 1, 0
    while True:
        runs += 1
        assert runs <= 10, "the step never finished"
        code, out = account.command_run()
        if code == int(ExitCode.DECISION_REQUIRED):
            break
        _stopped(out)
        assert out["cause"]["reason"] in (provider_gate.CEILING, provider_gate.BUDGET), out
        if out["cause"]["reason"] == provider_gate.BUDGET:
            # The hour's calls leave the window: the next hour begins.
            hours += 1
            account.hour = 0

    read = Counter(account.asked)
    assert set(read) == {DOWNLOADED, *others}
    assert max(read.values()) == 1
    assert hours == 2, (hours, runs)
    # THE STEP FINISHED: New1 is offered at the gate.
    assert out["cause"]["detail"]["gate"] == removed_cli.CONFIRM_GATE


def test_a_plan_from_kept_reads_is_the_plan_from_fresh_reads(five_landed, monkeypatch):
    clock = Clock(monkeypatch)
    account = Counted(monkeypatch)
    _synced(account, 5)
    code, asked = account.command_run()
    assert code == int(ExitCode.DECISION_REQUIRED), asked
    decided, _envelope = drive(
        ["run", "decide", asked["run_id"], removed_cli.CONFIRM_GATE, "abort", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK)
    # Past the hours a read is kept, so this command reads every playlist again.
    clock.moment = NOW + removed_kept.KEPT_FOR
    code, fresh = drive(["--run", asked["run_id"], *VERB])
    assert code == int(ExitCode.OK), fresh
    assert not any(one["code"] == removed_kept.FROM_KEPT for one in fresh["warnings"])
    read = len(account.asked)

    code, kept = drive(["--run", asked["run_id"], *VERB])

    assert code == int(ExitCode.OK), kept
    assert len(account.asked) == read
    assert any(one["code"] == removed_kept.FROM_KEPT for one in kept["warnings"])
    assert kept["data"] == fresh["data"]


def test_a_read_past_its_hours_or_of_a_playlist_with_no_stamp_is_read_again(
    five_landed, monkeypatch
):
    clock = Clock(monkeypatch)
    account = Counted(monkeypatch)
    others = _synced(account, 2)
    account.stamped("acc-unstamped", f"{playlists.SWEPT_PREFIX}Unstamped", [track("U")], updated=None)
    assert account.command_run()[0] == int(ExitCode.DECISION_REQUIRED)
    first = Counter(account.asked)
    assert first["acc-unstamped"] == 1

    account.command_run()
    assert (Counter(account.asked) - first) == Counter({"acc-unstamped": 1})

    clock.moment = NOW + removed_kept.KEPT_FOR
    before = Counter(account.asked)
    account.command_run()
    assert set(Counter(account.asked) - before) == {DOWNLOADED, *others, "acc-unstamped"}


def test_retire_reads_through_the_same_store(five_landed, monkeypatch):
    Clock(monkeypatch)
    account = Counted(monkeypatch)
    others = _synced(account, 3)
    _run()
    asked = len(account.asked)

    code, out = drive([*VERB, "--retire"])

    assert code == int(ExitCode.OK), out
    assert out["outcome"] == "no_op"
    assert len(account.asked) == asked
    assert out["data"]["totals"]["playlists read"] == len(others) + 1


# The store itself


def _listing(account: str = "acc-x") -> removed.Listing:
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


@pytest.mark.parametrize(
    ("tracks", "updated"),
    [(None, STAMP), (2, None), (2, ""), (2, "  "), (True, STAMP), (-1, STAMP)],
)
def test_a_listing_with_no_count_or_no_stamp_marks_nothing(tracks, updated):
    assert removed_kept.mark_of(_shown(tracks=tracks, updated=updated)) is None
    assert removed_kept.mark_of(None) is None


def test_a_kept_read_comes_back_whole_and_only_while_the_listing_says_it_stands(native_library):
    cfg, _root = native_library
    store = removed_kept.KeptReads(cfg, NOW)
    store.keep("acc-x", _shown(), _listing())
    store.flush()
    later = removed_kept.KeptReads(cfg, NOW + removed_kept.KEPT_FOR - timedelta(seconds=1))

    assert later.get("acc-x", _shown()) == _listing()
    assert later.get("acc-x", None) is None
    assert later.get("acc-x", _shown(tracks=3)) is None
    assert later.get("acc-x", _shown(updated="2026-11-21T00:00:00+00:00")) is None
    assert later.get("acc-y", _shown("acc-y")) is None
    assert removed_kept.KeptReads(cfg, NOW + removed_kept.KEPT_FOR).get("acc-x", _shown()) is None
    assert removed_kept.KeptReads(cfg, NOW - timedelta(seconds=1)).get("acc-x", _shown()) is None


@pytest.mark.parametrize(
    "state", [removed.SHORT, removed.EMPTY, removed.UNREADABLE, removed.GONE, removed.RETIRED]
)
def test_only_a_read_whole_is_kept_and_a_read_not_whole_now_drops_the_kept_one(native_library, state):
    cfg, _root = native_library
    store = removed_kept.KeptReads(cfg, NOW)
    store.keep("acc-x", _shown(), _listing())
    store.keep("acc-x", _shown(), removed.Listing(account="acc-x", name="X", state=state))
    store.flush()

    assert removed_kept.KeptReads(cfg, NOW).get("acc-x", _shown()) is None
    assert _kept_document(cfg)["reads"] == {}


def test_a_read_made_by_another_reader_is_not_trusted(native_library):
    cfg, _root = native_library
    store = removed_kept.KeptReads(cfg, NOW)
    store.keep("acc-x", _shown(), _listing())
    store.flush()
    document = _kept_document(cfg)
    document["reads"]["acc-x"]["reader"] = removed_kept.READER + 1
    config.state_path(removed_kept.STATE_KEY, cfg).write_text(json.dumps(document))

    assert removed_kept.KeptReads(cfg, NOW).get("acc-x", _shown()) is None


@pytest.mark.parametrize(
    "text", ["not json", "[]", '{"version": 2, "reads": {}}', '{"version": 1, "reads": []}']
)
def test_a_document_that_cannot_be_used_reads_as_nothing_kept_and_says_so(native_library, text):
    cfg, _root = native_library
    config.state_path(removed_kept.STATE_KEY, cfg).write_text(text)

    store = removed_kept.KeptReads(cfg, NOW)

    assert store.entries == {}
    assert store.get("acc-x", _shown()) is None
    assert [one["code"] for one in store.warnings()] == [removed_kept.UNREAD]


def test_a_refused_write_is_said_and_never_raised(native_library, monkeypatch):
    cfg, _root = native_library

    def refused(*_args, **_kwargs):
        raise OSError("read-only file system")

    monkeypatch.setattr(config, "atomic_write_bytes", refused)
    store = removed_kept.KeptReads(cfg, NOW)
    store.keep("acc-x", _shown(), _listing())
    store.flush()

    assert [one["code"] for one in store.warnings()] == [removed_kept.UNKEPT]
    assert "read-only file system" in store.unkept


def test_the_store_is_written_every_fifty_new_reads_and_drops_reads_past_their_hours(native_library):
    cfg, _root = native_library
    old = removed_kept.KeptReads(cfg, NOW - removed_kept.KEPT_FOR)
    old.keep("acc-old", _shown("acc-old"), _listing("acc-old"))
    old.flush()
    store = removed_kept.KeptReads(cfg, NOW)
    for n in range(removed_kept.FLUSH_EVERY - 1):
        store.keep(f"acc-{n}", _shown(f"acc-{n}"), _listing(f"acc-{n}"))
    assert set(_kept_document(cfg)["reads"]) == {"acc-old"}

    store.keep("acc-last", _shown("acc-last"), _listing("acc-last"))

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
