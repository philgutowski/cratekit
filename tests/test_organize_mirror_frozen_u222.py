"""U222: the mirror's apply after a library write between its acts holds the gate's plan.

Sitting 66 drove ``crate organize --only mirror`` to its account gate, took an
edit made on the account into the library with a ``mirror-edits`` pass, then
answered the gate: the run that applied rebuilt the frozen plan, read the
ledger's snapshot live, found the snapshot settled by the pass, read the edit
as rekordbox's own change, planned the track off the account and refused
``decision-stale``. Driven here on U204's disposable library, with each act a
run of its own as ``crate organize`` makes them: the gate's run records and
freezes, a run of the rekordbox area's ``mirror-edits`` step writes the
library between the acts, and the gate's run again, decided, rebuilds.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import json

from cratekit.core import active_taxonomy, config, rb_writer, tree_registry
from cratekit.modules.outbound import ledger
from cratekit.organize import account_mirror, mirror_edits, mirror_frozen
from cratekit.organize.steps import NOTHING, Area
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_organize_mirror import World as Plain
from tests.test_organize_mirror import folder
from tests.test_organize_mirror_edits import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import BATCH_A
from tests.test_organize_mirror_edits_u204 import world as world  # noqa: PLC0414
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414

GATE = "2026-11-05T20:23:49Z-5868"
INBOX_A = f"INBOX {BATCH_A}"


def _mirror(world, run: account_mirror.Run) -> Area:
    """The account area's mirror on ``run``, off a reading of its own, as ``--only mirror``."""
    shared = account_mirror.Shared(world.cfg, lambda: world.account, run)
    area = Area(name="account")
    account_mirror.add_steps(world.cfg, area, shared.account, run, shared=shared)
    return area


def _gate(world) -> Area:
    """The run that shows the gate: it records and freezes."""
    return _mirror(world, account_mirror.Run(run_id=GATE, record=True))


def _answered(world) -> Area:
    """The gate's run again, its account gate answered: it rebuilds from the frozen plan."""
    return _mirror(world, account_mirror.Run(run_id=GATE, record=True, decided=True))


def _edits_pass(world) -> None:
    """A ``mirror-edits`` run of its own between the acts, planned and applied."""
    world.runs += 1
    run = account_mirror.Run(run_id=f"edits-{world.runs}", record=True)
    shared = account_mirror.Shared(world.cfg, lambda: world.account, run)
    step = mirror_edits.add_step(
        world.cfg, active_taxonomy.load(world.cfg), tree_registry.read(world.cfg), shared
    )
    assert step.apply is not None, step.detail
    step.applied = step.apply()


def _apply(area: Area) -> None:
    for step in area.steps:
        if step.apply is not None:
            step.applied = step.apply()


def _asked(world) -> int:
    return len(world.account.matches)


# ═══════════════════════════════════════════════════════════════════════════
# 1. An account edit the library took between the acts (sitting 66)
# ═══════════════════════════════════════════════════════════════════════════


def test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan(world):
    """Sitting 66, A41: the apply lands with no stale and the track stays on the account."""
    world.put_in(INBOX_A, "r2")
    shown = _gate(world)
    assert world.members(world.batch_a) == {"1"}
    _edits_pass(world)
    assert world.members(world.batch_a) == {"1", "2"}
    asked = _asked(world)

    applied = _answered(world)

    assert applied.digest() == shown.digest()
    assert _asked(world) == asked
    assert applied.facts[account_mirror.FROZEN_FACT] == f"rebuilt from the plan frozen on run {GATE}"
    (inbox,) = [step for step in applied.steps if step.key == "mirror:INBOX"]
    assert inbox.state == NOTHING, inbox.items
    _apply(applied)
    assert world.held(INBOX_A) == ["r1", "r2"]
    # And the next run reads the edit as agreed, with nothing to write anywhere.
    _area, step, _shared = world.plan()
    after = _gate_of_next(world)
    assert step.state == NOTHING
    assert all(one.state != "planned" for one in after.steps), [one.key for one in after.steps]


def _gate_of_next(world) -> Area:
    world.runs += 1
    return _mirror(world, account_mirror.Run(run_id=f"next-{world.runs}", record=True))


def test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan(world):
    """The other way: a track taken off on the account is never put back by the apply."""
    world.take_off(INBOX_A, "r1")
    shown = _gate(world)
    _edits_pass(world)
    assert world.members(world.batch_a) == set()

    applied = _answered(world)

    assert applied.digest() == shown.digest()
    _apply(applied)
    assert world.held(INBOX_A) == []


def test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan(world):
    world.put_in("Deep House Low", "r2")
    shown = _gate(world)
    _edits_pass(world)
    assert "2" in world.members(world.playlists[("Deep House", "Low")])

    applied = _answered(world)

    assert applied.digest() == shown.digest()
    _apply(applied)
    assert "r2" in world.held("Deep House Low")


# ═══════════════════════════════════════════════════════════════════════════
# 2. The brief's other scenarios
# ═══════════════════════════════════════════════════════════════════════════


def test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale(world):
    shown = _gate(world)
    handle = rb_writer.open_db(world.db, unlock=False, cfg=world.cfg)
    try:
        made = handle.create_playlist("Somewhere Else")
        handle.session.flush()
        rb_writer.add_memberships(handle, made, ["2"])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    applied = _answered(world)

    assert applied.digest() == shown.digest()
    assert applied.stale[0] == "every step plans as the gate showed it"


def test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan(world):
    """As at sitting 58: rebuilt, equal, and the stale lines say so and how."""
    shown = _gate(world)
    asked = _asked(world)

    applied = _answered(world)

    assert applied.digest() == shown.digest()
    assert _asked(world) == asked
    assert applied.stale == [
        "every step plans as the gate showed it",
        f"{account_mirror.FROZEN_FACT}: rebuilt from the plan frozen on run {GATE}",
        f"{account_mirror.PLAN_FACT}: {applied.facts[account_mirror.PLAN_FACT]}",
    ]
    assert "read the account and rebuild" in applied.stale[2]


def test_the_gate_run_and_a_report_say_nothing_stale(world):
    """Only a decided run carries stale lines: a gate's answer is not yet given."""
    assert _gate(world).stale == []
    assert _mirror(world, account_mirror.Run(run_id="report", record=False)).stale == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. What a stale answer names
# ═══════════════════════════════════════════════════════════════════════════


def test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist(
    installed, monkeypatch
):
    """The one change the frozen plan does not hold, named, and no row asked to say it."""
    world = Plain(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1, 2), Med=(3,)), folder("Soul", High=(4,)))
    world.run()
    shown = Area(name="account")
    account_mirror.add_steps(world.cfg, shown, lambda: world.account, account_mirror.Run(run_id=GATE, record=True))
    world.account.playlists[world.playlist_id("Techno Low")].append("r99")
    world.account.names["r99"] = ("Someone", "By Hand")
    asked = len(world.account.matches)

    applied = Area(name="account")
    account_mirror.add_steps(
        world.cfg, applied, lambda: world.account, account_mirror.Run(run_id=GATE, record=True, decided=True)
    )

    assert applied.digest() != shown.digest()
    assert len(world.account.matches) == asked
    assert applied.stale[0] == (
        "moved since the gate showed it: mirror Techno onto the account, in 'Techno Low'"
    )
    assert applied.stale[1].startswith(f"{account_mirror.FROZEN_FACT}: rebuilt from the plan frozen")


def test_a_decided_run_with_no_frozen_plan_says_it_planned_afresh(world, monkeypatch):
    _gate(world)
    monkeypatch.setattr(mirror_frozen, "load", lambda _cfg, _run: (None, "none, by the test"))

    applied = _answered(world)

    assert not any(line.startswith("moved since") for line in applied.stale)
    assert applied.stale[0] == (
        f"{account_mirror.FROZEN_FACT}: none, by the test, so it was planned afresh; "
        f"frozen on run {GATE}, so the apply rebuilds it without asking the provider again"
    )


def test_a_step_new_since_the_gate_and_one_gone_are_named():
    class One:
        def __init__(self, key, title, digest="d", items=()):
            self.key, self.title, self.items = key, title, list(items)
            self._digest = digest

        def identity(self):
            return [self.key, "planned", self._digest]

    then = [One("mirror:A", "mirror A onto the account", items=[{"playlist": "A Low"}])]
    gone = One("sets", "the sets step")
    frozen = mirror_frozen.Frozen(
        library=None,
        matches={},
        steps={
            step.key: mirror_frozen.Shown(
                title=step.title,
                digest=mirror_frozen._shown_json(step)["digest"],
                lines=mirror_frozen._lines(step),
            )
            for step in (*then, gone)
        },
    )
    now = [
        One("mirror:A", "mirror A onto the account", digest="e", items=[{"playlist": "A Low", "add": 1}]),
        One("mirror:B", "mirror B onto the account"),
    ]

    assert mirror_frozen.moved(now, frozen) == [
        "mirror A onto the account, in 'A Low'",
        "mirror B onto the account, which the gate did not show",
        "the sets step, which the gate showed and this run did not plan",
    ]
    assert mirror_frozen.moved(then, frozen) == [
        "the sets step, which the gate showed and this run did not plan"
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 4. The frozen snapshot itself
# ═══════════════════════════════════════════════════════════════════════════


def test_the_frozen_snapshot_is_the_one_the_gates_plan_read_not_the_one_it_recorded(world):
    """The gate's own plan records a snapshot; the frozen one is what it read before."""
    before = ledger.mirror_folders(world.cfg)["INBOX"].playlists[INBOX_A].agreed
    world.put_in(INBOX_A, "r2")
    _gate(world)
    frozen, _said = mirror_frozen.load(world.cfg, GATE)

    assert frozen.agreed["INBOX"][INBOX_A] == (world.remote(INBOX_A), before)


def test_a_playlist_made_again_between_the_acts_reads_its_snapshot_now():
    recorded = {
        "INBOX": ledger.MirrorFolder(
            name="INBOX",
            playlists={
                "kept": ledger.MirrorPlaylist(name="kept", remote_id="p1", agreed=frozenset({"now"})),
                "made again": ledger.MirrorPlaylist(
                    name="made again", remote_id="p3", agreed=frozenset({"now"})
                ),
                "new": ledger.MirrorPlaylist(name="new", remote_id="p4", agreed=None),
            },
        ),
        "Techno": ledger.MirrorFolder(
            name="Techno",
            playlists={"low": ledger.MirrorPlaylist(name="low", remote_id="p5", agreed=None)},
        ),
    }
    frozen = mirror_frozen.Frozen(
        library=None,
        matches={},
        agreed={
            "INBOX": {"kept": ("p1", frozenset({"then"})), "made again": ("p2", frozenset({"then"}))},
            "Techno": {"low": ("p5", frozenset({"then"}))},
        },
    )

    read = mirror_frozen.overlay(recorded, frozen)

    assert read["INBOX"].playlists["kept"].agreed == frozenset({"then"})
    assert read["INBOX"].playlists["made again"].agreed == frozenset({"now"})
    assert read["INBOX"].playlists["new"].agreed is None
    assert read["Techno"].playlists["low"].agreed == frozenset({"then"})
    # A never agreed snapshot at the gate stays never agreed at the apply.
    frozen = mirror_frozen.Frozen(library=None, matches={}, agreed={"INBOX": {"kept": ("p1", None)}})
    assert mirror_frozen.overlay(recorded, frozen)["INBOX"].playlists["kept"].agreed is None
    # Every other field is the ledger's now.
    assert read["INBOX"].playlists["kept"].remote_id == "p1"


def test_a_version_5_record_or_an_unreadable_snapshot_or_step_is_planned_afresh(world):
    _gate(world)
    path = config.state_path("mirror_plans", world.cfg) / f"{GATE}.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["version"] == mirror_frozen.VERSION == 6
    for changed in (
        {"version": 5},
        {"agreed": {"INBOX": {INBOX_A: ["p1", "not a list"]}}},
        {"agreed": {"INBOX": {INBOX_A: [7, None]}}},
        {"steps": {"mirror:INBOX": {"title": "t", "digest": 7, "lines": {}}}},
        {"steps": {"mirror:INBOX": {"title": "t", "digest": "d", "lines": {"x": None}}}},
        {"steps": {"mirror:INBOX": {"title": "t", "digest": "d"}}},
    ):
        path.write_text(json.dumps({**document, **changed}), encoding="utf-8")
        frozen, said = mirror_frozen.load(world.cfg, GATE)
        assert frozen is None, changed
        assert "is not one this build reads" in said, said
    path.write_text(json.dumps(document), encoding="utf-8")
    frozen, _said = mirror_frozen.load(world.cfg, GATE)
    assert frozen is not None and set(frozen.steps) == {
        "mirror:Deep House",
        "mirror:Tech House",
        "mirror:Favorites",
        "mirror:INBOX",
    }
