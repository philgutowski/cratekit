"""U209: answering a gate does not plan the whole sync again.

Driven through ``crate sync pair`` on the disposable database
``tests/test_sync_pair.py`` builds, with the fake account and catalogue
counting what each command asks: every listing of an account playlist and
every ISRC lookup. The command that plans holds its plan under its run, the
later commands read it back, and the check before the write reads only the
lists the plan read.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import json

import pytest

from cratekit.core import held_plan
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.sync import pair_cli, pair_merge
from cratekit.write import playlist_pair
from tests.cli_drive import drive
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair import ACCOUNT, NAME, VERB, sync
from tests.test_sync_pair import db as db  # noqa: PLC0414
from tests.test_sync_pair import world as world  # noqa: PLC0414

APPLY = ["apply", "--actor", "a-person"]


class Counted:
    """What the provider was asked, by kind, counted across every command of a test."""

    def __init__(self, w, monkeypatch) -> None:
        self.w = w
        self.asked = len(w.account.matches)
        self.writes = w.account._writes
        self.listings = 0
        self.reads = 0
        real = intake_cli.list_playlist_readable

        def listing(found, reference, **kwargs):
            self.listings += 1
            return real(found, reference, **kwargs)

        monkeypatch.setattr(pair_cli.intake_cli, "list_playlist_readable", listing)
        tracks = w.account.playlist_tracks

        def read(playlist_id):
            self.reads += 1
            return tracks(playlist_id)

        w.account.playlist_tracks = read
        # The provider gate's own count, as the fakes reach no gate: every
        # listing, every lookup and every account write is one call.
        monkeypatch.setattr(pair_cli, "_spent", self.total)

    @property
    def lookups(self) -> int:
        return len(self.w.account.matches) - self.asked

    def total(self) -> int:
        return self.listings + self.reads + self.lookups + self.w.account._writes - self.writes


@pytest.fixture
def counted(monkeypatch):
    def made(w) -> Counted:
        return Counted(w, monkeypatch)

    return made


def _gate(envelope) -> str:
    return envelope["cause"]["detail"]["gate"]


def _to_the_write(w) -> str:
    """Answer both gates apply, one command each, and stop before the write. The run id."""
    code, first = drive(w.args())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, _gate(first), *APPLY])[0] == int(ExitCode.OK)
    code, second = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert drive(["run", "decide", run_id, _gate(second), *APPLY])[0] == int(ExitCode.OK)
    return run_id


# ═══════════════════════════════════════════════════════════════════════════
# One plan per run
# ═══════════════════════════════════════════════════════════════════════════


def test_a_two_gate_sync_makes_one_plans_lookups(world, counted):
    w = world(account=("1", "2"), rekordbox=("2", "3", "4"))
    seen = counted(w)
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "2", "3", "4"]
    assert w.on_account() == ["t1", "t2", "t3", "t4"]
    # Rows three and four are asked once each, by the one plan; the account
    # playlist is listed by that plan and by the check before the write.
    assert seen.lookups == 2
    assert seen.listings == 2


def test_answers_continued_in_later_commands_ask_nothing_when_nothing_moved(world, counted):
    w = world(account=("1",), rekordbox=("1", "2"))
    seen = counted(w)
    code, first = drive(w.args())
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = first["run_id"]
    planned = (seen.lookups, seen.listings)
    assert planned == (1, 1)
    code, second = drive(["run", "decide", run_id, _gate(first), *APPLY, "--continue"])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert (seen.lookups, seen.listings) == planned, "the second gate planned again"
    code, done = drive(["run", "decide", run_id, _gate(second), *APPLY, "--continue"])
    assert code == int(ExitCode.OK), done
    assert seen.lookups == 1, "the write asked about a track"
    assert seen.listings == 2, "the write listed more than the check"
    assert w.on_account() == ["t1", "t2"]


def test_the_held_plan_is_released_once_the_run_writes(world, cfg):
    w = world(account=("1",), rekordbox=("1", "2"))
    code, first = drive(w.args())
    run_id = first["run_id"]
    assert held_plan.path(run_id).is_file()
    drive(["run", "decide", run_id, _gate(first), *APPLY])
    drive(["--run", run_id, *w.args()])
    drive(["run", "decide", run_id, pair_cli.ACCOUNT_GATE, *APPLY])
    code, done = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.OK), done
    assert not held_plan.path(run_id).exists()


def test_both_sides_skipped_releases_the_held_plan(world):
    w = world(account=("1",), rekordbox=("2",))
    code, first = drive(w.args())
    run_id = first["run_id"]
    drive(["run", "decide", run_id, _gate(first), "skip", "--actor", "a-person"])
    drive(["--run", run_id, *w.args()])
    drive(["run", "decide", run_id, pair_cli.ACCOUNT_GATE, "skip", "--actor", "a-person"])
    code, done = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.OK), done
    assert not held_plan.path(run_id).exists()


# ═══════════════════════════════════════════════════════════════════════════
# The check before the write
# ═══════════════════════════════════════════════════════════════════════════


def test_an_account_list_changed_before_the_write_refuses_stale_and_names_it(world):
    w = world(account=("1",), rekordbox=("1", "2"))
    run_id = _to_the_write(w)
    w.account.playlists[ACCOUNT].append("t5")
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert refused["cause"]["reason"] == "decision-stale"
    moved = refused["cause"]["detail"]["moved"]
    assert moved == [
        {
            "side": "account",
            "playlist_id": ACCOUNT,
            "name": NAME,
            "why": "has gained 1 track(s) since the plan",
        }
    ]
    assert NAME in refused["cause"]["message"]
    assert w.on_account() == ["t1", "t5"], "the account was written over its moved list"
    assert w.held() == ["1", "2"]
    # The plan stays held, so the run says stale again rather than writing.
    assert held_plan.path(run_id).is_file()
    assert drive(["--run", run_id, *w.args()])[0] == int(ExitCode.DECISION_STALE)


def test_an_account_list_reordered_before_the_write_refuses_stale(world):
    w = world(account=("1", "3"), rekordbox=("1", "3", "2"))
    run_id = _to_the_write(w)
    w.account.playlists[ACCOUNT] = ["t3", "t1"]
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert refused["cause"]["detail"]["moved"][0]["why"] == "was reordered since the plan"


def test_a_rekordbox_membership_changed_before_the_write_refuses_stale_and_names_it(world):
    w = world(account=("1",), rekordbox=("1", "2"))
    run_id = _to_the_write(w)
    w.rekordbox_remove("2")
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    moved = refused["cause"]["detail"]["moved"]
    assert [(one["side"], one["playlist_id"]) for one in moved] == [
        ("rekordbox", w.rekordbox_id)
    ]
    assert moved[0]["why"] == "has lost 1 track(s) since the plan"
    assert w.on_account() == ["t1"], "the account was written over a moved rekordbox list"


def test_both_sides_moved_are_both_named(world):
    w = world(account=("1",), rekordbox=("1", "2"))
    run_id = _to_the_write(w)
    w.rekordbox_add("3")
    w.account.playlists[ACCOUNT].remove("t1")
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert sorted(one["side"] for one in refused["cause"]["detail"]["moved"]) == [
        "account",
        "rekordbox",
    ]


def test_a_moved_list_is_checked_whichever_side_was_skipped(world):
    w = world(account=("1",), rekordbox=("1", "2"))
    code, first = drive(w.args())
    run_id = first["run_id"]
    drive(["run", "decide", run_id, _gate(first), "skip", "--actor", "a-person"])
    drive(["--run", run_id, *w.args()])
    drive(["run", "decide", run_id, pair_cli.ACCOUNT_GATE, *APPLY])
    w.rekordbox_add("3")
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert w.on_account() == ["t1"]


def test_a_withheld_count_changed_before_the_write_refuses_stale(world):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_add("3")
    run_id = _to_the_write(w)
    w.declared = 5
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert "withholds" in refused["cause"]["detail"]["moved"][0]["why"]


def test_a_pair_with_nothing_to_write_on_the_account_is_not_listed_again(world, counted):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_order("2", "1")
    w.account.playlists[ACCOUNT] = ["t2", "t1"]
    seen = counted(w)
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert seen.reads == 0, "the account playlist was listed again for its snapshot"
    assert seen.listings == 2


# ═══════════════════════════════════════════════════════════════════════════
# A no change sync, and what each phase cost
# ═══════════════════════════════════════════════════════════════════════════


def test_a_no_change_sync_of_a_linked_pair_makes_no_isrc_lookup(world, counted, cfg):
    w = world(account=("1",), rekordbox=("1", "2", "3"))
    # Row three is a track the account has none of: asked once, remembered.
    del w.account.catalog["3"]
    assert sync(w.args())[0] == int(ExitCode.OK)
    assert w.on_account() == ["t1", "t2"]
    seen = counted(w)
    for args in (w.args(), VERB):
        code, envelope = sync(args)
        assert code == int(ExitCode.OK), envelope
        assert envelope["outcome"] == "no_op"
    assert seen.lookups == 0, w.account.matches


def test_each_phase_is_counted_on_the_answer(world, counted):
    w = world(account=("1",), rekordbox=("1", "2", "3"))
    counted(w)
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    # Plan: one listing and two lookups. Check: one listing. Write: the add
    # and the listing after it.
    assert envelope["data"]["totals"]["calls"] == {"plan": 3, "check": 1, "write": 2}
    written = next(one for one in envelope["warnings"] if one["code"] == pair_cli.WRITTEN)
    assert (
        "provider calls: 3 to plan (in the command that planned), 1 to check the lists "
        "before writing, 2 to write" in written["message"]
    )


def test_the_calls_are_on_a_no_op_answer_too(world, counted):
    w = world(account=("1",), rekordbox=("2",))
    counted(w)
    code, envelope = sync(w.args(), rekordbox="skip", account="skip")
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["calls"] == {"plan": 2, "check": 0, "write": 0}


# ═══════════════════════════════════════════════════════════════════════════
# A held plan that cannot be used is planned again, and says so
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unreadable_held_plan_is_planned_again_and_says_why(world, counted):
    w = world(account=("1",), rekordbox=("1", "2"))
    seen = counted(w)
    code, first = drive(w.args())
    run_id = first["run_id"]
    held_plan.path(run_id).write_text("not json")
    drive(["run", "decide", run_id, _gate(first), *APPLY])
    code, second = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert "could not be read" in second["cause"]["detail"]["shown"]["planned again"]
    drive(["run", "decide", run_id, pair_cli.ACCOUNT_GATE, *APPLY])
    code, done = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.OK), done
    assert pair_cli.REPLANNED not in {one["code"] for one in done["warnings"]}
    assert w.on_account() == ["t1", "t2"]
    # The first plan and the plan made again each ask once; the plan made
    # again is held, so the write asks nothing.
    assert seen.lookups == 2


def test_a_held_plan_other_than_the_offer_is_planned_again(world, cfg):
    w = world(account=("1",), rekordbox=("1", "2"))
    code, first = drive(w.args())
    run_id = first["run_id"]
    drive(["run", "decide", run_id, _gate(first), *APPLY])
    drive(["--run", run_id, *w.args()])
    drive(["run", "decide", run_id, pair_cli.ACCOUNT_GATE, *APPLY])
    other = pair_cli.Plan()
    asked = pair_cli._asked((pair_cli.Target(ACCOUNT, w.rekordbox_id, False),), False)
    assert pair_cli._hold(run_id, other, 0, asked) == ""
    code, done = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.OK), done
    said = next(one for one in done["warnings"] if one["code"] == pair_cli.REPLANNED)
    assert "is not the plan" in said["message"]
    assert w.on_account() == ["t1", "t2"]


def test_a_held_plan_made_for_other_pairs_is_planned_again(world, cfg):
    w = world(account=("1",), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_add("3")
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    run_id = first["run_id"]
    drive(["run", "decide", run_id, _gate(first), *APPLY])
    # The same run asked again for one pair by name, not for every pair.
    code, second = drive(["--run", run_id, *VERB, ACCOUNT])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    said = second["cause"]["detail"]["shown"]["planned again"]
    assert "other pairs" in said


def test_a_replanned_run_whose_list_moved_is_refused_by_the_gate(world):
    w = world(account=("1",), rekordbox=("1", "2"))
    run_id = _to_the_write(w)
    held_plan.release(run_id)
    w.rekordbox_add("3")
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert w.on_account() == ["t1"]


# ═══════════════════════════════════════════════════════════════════════════
# The codec
# ═══════════════════════════════════════════════════════════════════════════


def _a_plan(w) -> pair_cli.Plan:
    from cratekit.core import jobs

    with jobs.open_store() as store:
        return pair_cli.plan(w.cfg, pair_cli.targets(_store(w), ACCOUNT, w.rekordbox_id), store=store)


def _store(w):
    from cratekit.modules.outbound import pairs

    return pairs.PairStore(w.cfg)


def test_a_real_plan_reads_back_equal_with_its_digest(world):
    w = world(account=("1", "3"), rekordbox=("1", "2"))
    planned = _a_plan(w)
    registry = pair_cli._held_classes()
    back = held_plan.decode(json.loads(json.dumps(held_plan.encode(planned, registry))), registry)
    assert back == planned
    assert back.digest == planned.digest
    assert isinstance(back.pairs[0].account_now, tuple)


def test_a_merge_call_with_its_moments_reads_back_equal():
    from datetime import datetime, timezone

    registry = pair_cli._held_classes()
    merged = pair_merge.Merged(
        order=("r:1",),
        leader=pair_merge.ACCOUNT,
        first=False,
        calls=(
            pair_merge.Call("r:1", pair_merge.ACCOUNT, datetime(2026, 1, 1, tzinfo=timezone.utc), None),
        ),
    )
    change = playlist_pair.Change("9", (("1", "a"),), adds=("2",), order=("1", "2"))
    value = {"merged": merged, "change": change, "seen": frozenset({"b", "a"}), "set": {1}}
    assert held_plan.decode(held_plan.encode(value, registry), registry) == value


def test_a_class_the_registry_does_not_name_is_refused_both_ways():
    registry = pair_cli._held_classes()
    stranger = pair_cli.Done(account_id="x")
    with pytest.raises(held_plan.Unheld, match="not a class this plan may hold"):
        held_plan.encode(stranger, registry)
    forged = {"$": "dataclass", "n": "Done", "v": {"account_id": "x"}}
    with pytest.raises(held_plan.Unheld, match="not a class this plan may hold"):
        held_plan.decode(forged, registry)
    with pytest.raises(held_plan.Unheld, match="not a tag"):
        held_plan.decode({"$": "module", "v": "os"}, registry)
    with pytest.raises(held_plan.Unheld):
        held_plan.decode({"plain": "dict"}, registry)


def test_a_value_the_codec_cannot_carry_is_not_held(cfg):
    reason = held_plan.hold("run-x", "sync.pair", object(), registry={}, digest="d")
    assert "could not be held" in reason
    assert not held_plan.path("run-x").exists()


def test_a_held_plan_of_another_kind_or_run_is_no_plan(cfg):
    registry = pair_cli._held_classes()
    plan = pair_cli.Plan()
    assert held_plan.hold("run-a", "sync.pair", plan, registry=registry, digest=plan.digest) == ""
    found, digest, _extra, why = held_plan.load(
        "run-a", "other.verb", registry=registry, digest_of=lambda one: one.digest
    )
    assert found is None and "kind" in why
    found, digest, _extra, why = held_plan.load(
        "run-a", "sync.pair", registry=registry, digest_of=lambda one: one.digest
    )
    assert found == plan and digest == plan.digest and why == ""
    document = json.loads(held_plan.path("run-a").read_text())
    document["digest"] = "forged"
    held_plan.path("run-a").write_text(json.dumps(document))
    found, _digest, _extra, why = held_plan.load(
        "run-a", "sync.pair", registry=registry, digest_of=lambda one: one.digest
    )
    assert found is None and "does not digest" in why


def test_old_held_plans_are_pruned_and_the_new_one_kept(cfg):
    import os
    import time

    registry = pair_cli._held_classes()
    plan = pair_cli.Plan()
    assert held_plan.hold("run-old", "sync.pair", plan, registry=registry, digest=plan.digest) == ""
    assert held_plan.hold("run-young", "sync.pair", plan, registry=registry, digest=plan.digest) == ""
    long_ago = time.time() - held_plan.KEEP.total_seconds() - 60
    os.utime(held_plan.path("run-old"), (long_ago, long_ago))
    assert held_plan.hold("run-new", "sync.pair", plan, registry=registry, digest=plan.digest) == ""
    assert not held_plan.path("run-old").exists()
    assert held_plan.path("run-young").exists()
    assert held_plan.path("run-new").exists()


def test_a_rekordbox_playlist_deleted_before_the_write_refuses_stale(world):
    w = world(account=("1",), rekordbox=("1", "2"))
    run_id = _to_the_write(w)
    import sqlite3

    conn = sqlite3.connect(w.cfg.library.db_path)
    conn.execute("UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", (w.rekordbox_id,))
    conn.commit()
    conn.close()
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert refused["cause"]["detail"]["moved"][0]["why"] == "is no longer a live plain playlist"
    assert w.on_account() == ["t1"]


def test_a_held_plan_older_than_it_is_kept_is_planned_again(world):
    import os
    import time

    w = world(account=("1",), rekordbox=("1", "2"))
    code, first = drive(w.args())
    run_id = first["run_id"]
    long_ago = time.time() - held_plan.KEEP.total_seconds() - 60
    os.utime(held_plan.path(run_id), (long_ago, long_ago))
    drive(["run", "decide", run_id, _gate(first), *APPLY])
    code, second = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert "older than 30 days" in second["cause"]["detail"]["shown"]["planned again"]


def test_tracks_another_sync_queued_before_the_write_refuse_stale_not_twice(world):
    from cratekit.core import jobs

    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT].append("t77")
    first = _to_the_write(w)
    second = _to_the_write(w)
    code, done = drive(["--run", first, *w.args()])
    assert code == int(ExitCode.OK), done
    assert len(done["data"]["totals"]["queued_jobs"]) == 1
    code, refused = drive(["--run", second, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    moved = refused["cause"]["detail"]["moved"]
    assert [(one["side"], one["playlist_id"]) for one in moved] == [("library", ACCOUNT)]
    with jobs.open_store() as store:
        assert len(pair_cli.pair_jobs(w.cfg, store)) == 1
