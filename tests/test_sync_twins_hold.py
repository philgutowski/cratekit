"""U221: a twin's missing tracks are held for Phillip's choice per playlist.

``sync twins`` records the hold, ``sync pair`` names it and queues none, and
``sync release`` lets one or every twin's go at its own explicit gate, on the
world tests/test_sync_twins.py builds.
"""

from __future__ import annotations

import json
from types import MappingProxyType

import pytest

from cratekit.core import jobs
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli, release_cli, twins, twins_cli
from tests._sync_builders import exited, failed
from tests.cli_drive import drive
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_twins import PHIL, PHIL_NAME, World, backfill, sync_pair
from tests.test_sync_twins import db as db  # noqa: PLC0414

OTHER = "acc-other"
OTHER_NAME = "DOWNLOADED Other 10-01-26"
RELEASE = ["sync", "release"]
#: Account tracks the library lacks, beyond the two the world already codes.
LACKING = {"t22": "USZZZ2600022", "t23": "USZZZ2600023", "t24": "USZZZ2600024"}
#: The three tracks of Phil's twin the library lacks.
THREE = ["t20", "t21", "t22"]


@pytest.fixture
def world(cfg, gates_pass, db, monkeypatch) -> World:
    made = World(cfg, monkeypatch)
    made.codes.update(LACKING)
    return made


def _codes(envelope) -> set[str]:
    return {warning["code"] for warning in envelope.get("warnings") or ()}


def _warning(envelope, code: str) -> str:
    (said,) = [one["message"] for one in envelope.get("warnings") or () if one["code"] == code]
    return said


def _on_hold(envelope) -> list[tuple[str, str]]:
    return [
        (item["pair"], item["remote_id"])
        for item in envelope["data"]["items"]
        if item["side"] == "library" and item["action"] == pair_cli.ON_HOLD_ACTION
    ]


def _held_ids(envelope) -> list[str]:
    return sorted(remote for _pair, remote in _on_hold(envelope))


def _queued(envelope) -> list[str]:
    found: list[str] = []
    with jobs.open_store() as store:
        for job_id in envelope["data"]["totals"]["queued_jobs"]:
            found.extend(sorted((jobs.get(store, job_id).payload or {}).get("tracks") or {}))
    return sorted(found)


def _holding(cfg, account_id: str = PHIL) -> list[str]:
    """What the pairs document holds for the twin's choice, by id."""
    return sorted(pairs.PairStore(cfg).get(account_id).on_hold or {})


def release(*args: str, answer: str = "approve"):
    """Drive ``sync release`` through its explicit gate, answering as asked."""
    code, envelope = drive([*RELEASE, *args])
    if code != int(ExitCode.DECISION_REQUIRED):
        return code, envelope
    run_id = envelope["run_id"]
    gate = envelope["cause"]["detail"]["gate"]
    assert gate == release_cli.APPROVE_GATE, envelope
    exited(drive(["run", "decide", run_id, gate, answer, "--actor", "a-person"]))
    return drive(["--run", run_id, *RELEASE, *args])


def _three_missing(w: World) -> None:
    """``DOWNLOADED Phil 9-30-26``: two owned tracks and three the library lacks."""
    w.playlist(PHIL, PHIL_NAME, ["t3", "t20", "t1", "t21", "t22"])


def _backfilled(w: World) -> None:
    """Phil's twin with its three missing, backfilled."""
    _three_missing(w)
    exited(backfill())


def _two_twins(w: World) -> None:
    _three_missing(w)
    w.playlist(OTHER, OTHER_NAME, ["t4", "t23", "t5"])
    exited(backfill())


# The brief's scenarios


def test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold(world, cfg):
    _backfilled(world)
    held = pairs.PairStore(cfg).get(PHIL)
    assert held is not None and held.twin
    assert sorted(held.on_hold or {}) == THREE
    envelope = exited(sync_pair())
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert envelope["data"]["totals"]["acquire"] == 0
    assert sorted(_on_hold(envelope)) == [(PHIL, "t20"), (PHIL, "t21"), (PHIL, "t22")]
    assert envelope["data"]["totals"]["on_hold"] == 3
    said = _warning(envelope, pair_cli.ON_HOLD)
    assert f"{PHIL_NAME}: 3" in said and f"crate sync release {PHIL}" in said
    # A SECOND SYNC STILL HOLDS THEM: the snapshot moved and the hold did not.
    again = exited(sync_pair())
    assert again["data"]["totals"]["queued_jobs"] == []
    assert len(_on_hold(again)) == 3
    assert _holding(cfg) == THREE


def test_releasing_the_twin_queues_its_three_at_the_next_sync(world, cfg):
    _backfilled(world)
    envelope = exited(release(PHIL))
    assert envelope["data"]["totals"]["released"] == 1
    assert envelope["data"]["totals"]["tracks"] == 3
    assert release_cli.RELEASED in _codes(envelope)
    assert dict(pairs.PairStore(cfg).get(PHIL).on_hold) == {}
    synced = exited(sync_pair())
    assert _queued(synced) == THREE
    assert _on_hold(synced) == []


def test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held(world, cfg):
    _backfilled(world)
    world.account.playlists[PHIL].append("t24")
    envelope = exited(sync_pair())
    assert _queued(envelope) == ["t24"]
    assert _held_ids(envelope) == THREE


def test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held(
    world, cfg, tmp_path
):
    """U229: a held track the library now holds is that row, one it lacks stays held."""
    from tests.test_sync_pair import _landed_for, _untagged_row

    _backfilled(world)
    # Another playlist's landing brought t22 in as row nine, its code in its
    # file only.
    _untagged_row(cfg, "9", tmp_path, file_isrc=LACKING["t22"])
    _landed_for(world, cfg, "acc-daily", ("9",), session_id="s-daily", name="Daily")
    envelope = exited(sync_pair())
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert sorted(_on_hold(envelope)) == [(PHIL, "t20"), (PHIL, "t21")]
    assert world.held(world.twin("Phil 9-30-26")) == ["3", "1", "9"]


#: Sorts before the twin, so a sync of every pair plans it first.
WARM = "acc-amber"
WARM_NAME = "Warmup"


def _warmup(world, *, sync: bool) -> str:
    """A plain pair, ``Warmup``, listing row one and t22, a track the twin holds."""
    world.playlist(WARM, WARM_NAME, ["t1", "t22"], folder="")
    made = world.make(WARM_NAME)
    world.rekordbox_add(made, "1")
    if sync:
        assert _queued(exited(sync_pair(WARM, "--rekordbox", made))) == ["t22"]
    else:
        pairs.PairStore(world.cfg).mark(WARM, made, name=WARM_NAME)
    return made


def test_a_twins_held_track_another_pairs_job_holds_is_still_held(world, cfg):
    """R-1385: another pair's job holding a twin's held track leaves it held, never awaiting."""
    _backfilled(world)
    _warmup(world, sync=True)
    envelope = exited(sync_pair())
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert sorted(_on_hold(envelope)) == [(PHIL, "t20"), (PHIL, "t21"), (PHIL, "t22")]
    awaiting = [
        (item["pair"], item["remote_id"])
        for item in envelope["data"]["items"]
        if item["action"] == "awaiting"
    ]
    assert awaiting == [(WARM, "t22")]


def test_a_twins_held_track_a_plain_pair_lists_is_queued_once_and_still_held(world, cfg):
    """R-1385: in one plan the plain pair queues t22 once and the twin still holds it."""
    _warmup(world, sync=False)
    _backfilled(world)
    envelope = exited(sync_pair())
    assert _queued(envelope) == ["t22"]
    assert sorted(_on_hold(envelope)) == [(PHIL, "t20"), (PHIL, "t21"), (PHIL, "t22")]
    planned = [item["pair"] for item in envelope["data"]["items"] if item["side"] == "library"]
    assert planned.index(WARM) < planned.index(PHIL), planned


def test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record(world, cfg):
    """R-1383: the twin's hold names its own remedy, never the landing's."""
    from cratekit.core import session

    _backfilled(world)
    torn = session.log_path("s-torn", cfg)
    torn.parent.mkdir(parents=True, exist_ok=True)
    torn.write_text('{"session_id": "s-to')
    envelope = exited(sync_pair())
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert sorted(_on_hold(envelope)) == [(PHIL, "t20"), (PHIL, "t21"), (PHIL, "t22")]
    assert envelope["data"]["totals"]["landing_unread"] == 0


def test_a_second_twin_stays_held_when_the_first_is_released(world, cfg):
    _two_twins(world)
    assert _holding(cfg, OTHER) == ["t23"]
    exited(release(PHIL))
    assert _holding(cfg, OTHER) == ["t23"]
    synced = exited(sync_pair())
    assert _queued(synced) == THREE
    assert _on_hold(synced) == [(OTHER, "t23")]


def test_release_all_lets_every_twin_go(world, cfg):
    _two_twins(world)
    envelope = exited(release("--all"))
    assert envelope["data"]["totals"]["released"] == 2
    assert _queued(exited(sync_pair())) == ["t20", "t21", "t22", "t23"]


# A twin paired before U221, read by time


def _as_before_u221(cfg) -> str:
    """Drop every recorded hold, as a pairs document from before U221 reads, and return the mark."""
    store = pairs.PairStore(cfg)
    raw = json.loads(store.path.read_text(encoding="utf-8"))
    for record in raw["pairs"].values():
        record.pop("on_hold", None)
    store.path.write_text(json.dumps(raw), encoding="utf-8")
    held = store.get(PHIL)
    assert held is not None and held.on_hold is None
    return held.marked


def test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark(world, cfg):
    _backfilled(world)
    marked = _as_before_u221(cfg)
    # t20 undated, t21 before the mark, t22 after it, so only t22 reads as
    # added by hand since the twin was made.
    world.dates = {"t21": "2026-01-01T00:00:00+00:00", "t22": "2099-01-01T00:00:00+00:00"}
    assert marked < world.dates["t22"]
    envelope = exited(sync_pair())
    assert _queued(envelope) == ["t22"]
    assert _held_ids(envelope) == ["t20", "t21"]


def _shown_twins() -> str:
    """The twins line the release's gate shows for Phil's twin, nothing yet let go."""
    refused = exited(drive([*RELEASE, PHIL]), ExitCode.DECISION_REQUIRED)
    return refused["cause"]["detail"]["shown"]["twins"]


def test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time(world, cfg):
    _backfilled(world)
    _as_before_u221(cfg)
    shown = _shown_twins()
    assert shown.startswith(f"{PHIL_NAME}: every track the library lacks that its account")
    assert "listed before the twin was made" in shown
    envelope = exited(release(PHIL))
    assert envelope["data"]["totals"]["by_time"] == 1
    assert _queued(exited(sync_pair())) == THREE


# The release verb's refusals and its plan of nothing


def test_an_abort_lets_nothing_go(world, cfg):
    _backfilled(world)
    envelope = exited(release(PHIL, answer="abort"))
    assert envelope["outcome"] == "no_op"
    assert _holding(cfg) == THREE


def test_a_released_twin_asks_nothing_the_second_time(world, cfg):
    _backfilled(world)
    exited(release(PHIL))
    envelope = exited(drive([*RELEASE, PHIL]))
    assert envelope["outcome"] == "no_op"
    assert release_cli.NOTHING in _codes(envelope)
    assert [one["action"] for one in envelope["data"]["items"]] == [release_cli.NOTHING_HELD]


def test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned(world, cfg):
    _backfilled(world)
    pairs.PairStore(cfg).mark("acc-hand", "999", name="By hand")
    for named in ("acc-nobody", "acc-hand"):
        envelope = failed(drive([*RELEASE, PHIL, named]))
        assert envelope["cause"]["reason"] == release_cli.NOT_A_TWIN
        assert envelope["cause"]["detail"]["account_ids"] == [named]
    assert _holding(cfg) == THREE


@pytest.mark.parametrize("args", [[], ["--all", PHIL]])
def test_release_needs_names_or_all_and_not_both(world, cfg, args):
    _backfilled(world)
    envelope = failed(drive([*RELEASE, *args]))
    assert envelope["cause"]["reason"] == release_cli.UNNAMED
    assert _holding(cfg) == THREE


def test_a_twin_paired_again_since_the_plan_is_left_held(world, cfg):
    _backfilled(world)
    store = pairs.PairStore(cfg)
    held = store.get(PHIL)
    assert store.release_hold({PHIL: "not-" + held.rekordbox_id}) == {}
    assert _holding(cfg) == THREE
    assert sorted(store.release_hold({PHIL: held.rekordbox_id})) == [PHIL]


# The other makers, the note and the record


def test_the_backfills_note_says_the_missing_are_held_not_queued(world):
    _three_missing(world)
    said = _warning(exited(backfill()), twins_cli.MISSING)
    assert "held for your choice" in said and "crate sync release" in said
    assert "queues each one the library lacks" not in said


def test_a_landing_twin_records_an_empty_hold(cfg):
    landed = twins.LandedTwin(
        account_id="acc-land", account_name="DOWNLOADED Land", name="Land",
        folder="Custom Playlists 2026", playlist_id="77", tracks=2,
    )
    twins.pair_landed(cfg, [landed])
    held = pairs.PairStore(cfg).get("acc-land")
    assert held is not None and held.twin and held.on_hold is not None
    assert dict(held.on_hold) == {}


def test_the_hold_survives_a_recorded_snapshot_and_a_mark_of_the_same_pair(cfg):
    store = pairs.PairStore(cfg)
    store.mark("a", "1", name="x", twin=True, on_hold={"t9": "Artist - Title"})
    store.record("a", account=["t9"], rekordbox=[], links={"t8": "8"})
    store.mark("a", "1", name="x", twin=True, on_hold={})
    assert dict(store.get("a").on_hold) == {"t9": "Artist - Title"}
    raw = json.loads(store.path.read_text(encoding="utf-8"))
    assert raw["pairs"]["a"]["on_hold"] == {"t9": "Artist - Title"}
    assert raw["version"] == pairs.PAIRS_VERSION


def test_a_pair_with_no_hold_writes_none_and_reads_back_none(cfg):
    store = pairs.PairStore(cfg)
    store.mark("a", "1", name="x")
    assert '"on_hold"' not in store.path.read_text(encoding="utf-8")
    assert store.get("a").on_hold is None


@pytest.mark.parametrize("bad", [["t1"], {"t1": 3}, {"": "x"}, "t1"])
def test_a_hold_that_is_not_ids_to_words_refuses_the_document(cfg, bad):
    store = pairs.PairStore(cfg)
    store.mark("a", "1", name="x", twin=True)
    raw = json.loads(store.path.read_text(encoding="utf-8"))
    raw["pairs"]["a"]["on_hold"] = bad
    store.path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(Exception) as caught:
        store.all()
    assert "sync-pair-store-unusable" in str(getattr(caught.value, "cause", caught.value).reason)


def _twin(marked: str, **held) -> pairs.Pair:
    return pairs.Pair(account_id="a", rekordbox_id="1", name="x", marked=marked, twin=True, **held)


def test_a_pair_that_is_no_twin_never_holds(cfg):
    plain = pairs.Pair(account_id="a", rekordbox_id="1", name="x", marked="", twin=False)
    assert not pair_cli.held_for_choice(plain, "t1", {})
    held = _twin("2026-11-05T00:00:00+00:00", on_hold=MappingProxyType({"t1": "A - B"}))
    assert pair_cli.held_for_choice(held, "t1", {})
    assert not pair_cli.held_for_choice(held, "t2", {})
    assert not pair_cli.held_for_choice(None, "t1", {})


# Late served tracks and stale links


def test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later(world, cfg):
    """A track the account withheld from the backfill is held by time once it is served."""
    world.playlist(PHIL, PHIL_NAME, ["t3", "t20", "t1"])
    world.short.add(PHIL)
    exited(backfill())
    assert pairs.PairStore(cfg).get(PHIL).on_hold is None
    world.short.clear()
    world.account.playlists[PHIL].append("t22")
    envelope = exited(sync_pair())
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert _held_ids(envelope) == ["t20", "t22"]


def test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released(
    world, cfg
):
    """A link the pairs document keeps to a row since removed never hides a held track."""
    world.playlist(PHIL, PHIL_NAME, ["t3", "t20", "t1"])
    exited(backfill())
    # The link names a row the collection no longer holds.
    pairs.PairStore(cfg).record(PHIL, links={"t20": "777"})
    assert world.sql("SELECT ID FROM djmdContent WHERE ID = '777'") == []
    assert _shown_twins() == f"{PHIL_NAME}: 1 track(s)"
    envelope = exited(release(PHIL))
    assert envelope["data"]["totals"]["released"] == 1
    assert [one["remote_id"] for one in envelope["data"]["items"] if one["action"] == "held"] == [
        "t20"
    ]


def test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold(world, cfg):
    """A twin read by time again, its hold dropped by a copy, names its queued track awaiting."""
    _backfilled(world)
    exited(release(PHIL))
    assert _queued(exited(sync_pair())) == THREE
    _as_before_u221(cfg)
    again = exited(sync_pair())
    assert _on_hold(again) == []
    assert again["data"]["totals"]["awaiting"] == 3


def test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing(cfg):
    store = pairs.PairStore(cfg)
    store.mark("plain", "1", name="x")
    store.mark("empty", "2", name="y", twin=True, on_hold={})
    before = store.path.read_bytes()
    assert store.release_hold({"plain": "1", "empty": "2", "gone": "3"}) == {}
    assert store.path.read_bytes() == before
    assert store.get("plain").on_hold is None


def test_the_plans_digest_moves_with_the_hold():
    from cratekit.sync import pair_merge
    from cratekit.write import playlist_pair

    target = pair_cli.Target(account_id="a", rekordbox_id="1", marked=True)
    named = pair_cli.Named(key="r:t1", artist="A", title="B", remote_id="t1")

    def plan(on_hold):
        return pair_cli.PairPlan(
            target=target,
            name="x",
            rekordbox_name="x",
            first=False,
            merged=pair_merge.merge(None, pair_merge.Side(()), pair_merge.Side(())),
            account_now=(),
            rekordbox_before=(),
            change=playlist_pair.Change(playlist_id="1", before=(), adds=(), removes=(), order=()),
            on_hold=on_hold,
        )

    assert "on_hold" not in plan(()).identity()
    assert plan((named,)).identity()["on_hold"] == ["t1"]
    assert plan((named,)).identity() != plan(()).identity()


def test_a_track_dated_at_the_very_mark_is_held():
    held = _twin("2026-11-05T10:00:00+00:00")
    assert pair_cli.held_for_choice(held, "t1", {"t1": "2026-11-05T12:00:00+02:00"})
    assert not pair_cli.held_for_choice(held, "t1", {"t1": "2026-11-05T10:00:01+00:00"})
    assert pair_cli.held_for_choice(held, "t1", {"t1": "2026-11-05T09:59:59+00:00"})
