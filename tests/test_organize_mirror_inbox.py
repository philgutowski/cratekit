"""U150: INBOX mirrored onto the account, live batches only, a retired batch's playlist removed.

Three surfaces. The organize step itself, :func:`account_mirror.add_steps`,
over the recording fake account the U147 suite drives, with the library handed
in as values, so each scenario reads what the account holds after the apply.
The library side on a disposable database whose intake tree is cut over, as
the rotation suite builds it, so what a live batch is comes off a real schema
and the rotation's own classifier. And the label landing's record, which names
each landed row's provider track for the mirror to fill a label batch from.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

import pytest

from cratekit.core import active_taxonomy, config, rb_writer, session, tree_registry
from cratekit.core.cause import Cause, CratekitError, Scope, refuse
from cratekit.intake import label_filing, native, rotate
from cratekit.modules.outbound import ledger, mirror
from cratekit.organize import account_mirror, mirror_frozen
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, Area
from cratekit.sync import playlists
from tests.test_inbox_rotate import (
    INTAKE,
    OLD,
    TODAY,
    _node,
    _open,
    _record_landing,
)
from tests.test_inbox_rotate import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_inbox_rotate import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_inbox_rotate import acknowledged as acknowledged  # noqa: PLC0414 - fixture
from tests.test_inbox_rotate import machine as machine  # noqa: PLC0414 - fixture
from tests.test_inbox_rotate import native_library as native_library  # noqa: PLC0414 - fixture
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_organize_mirror import World, folder, row

BATCHES = ("2026-10-20 Tidal playlists", "2026-10-25 Favorites", "2026-10-31 Defected")


def inbox(*batches: tuple[str, tuple[int, ...]], present: tuple[str, ...] = ()) -> mirror.Folder:
    """INBOX as the library reads it: each live batch with its rows, and every title there."""
    sources = tuple(
        mirror.Source(name=mirror.title("INBOX", name), rows=tuple(row(n) for n in numbers))
        for name, numbers in batches
    )
    return mirror.Folder(
        name="INBOX",
        playlists=sources,
        retire=True,
        present=frozenset(
            {source.name for source in sources} | {mirror.title("INBOX", one) for one in present}
        ),
    )


def _world(installed, monkeypatch, *folders: mirror.Folder) -> World:
    world = World(installed, monkeypatch)
    world.library = account_mirror.Library(folders=folders)
    return world


def _step(area: Area, name: str = "INBOX"):
    (found,) = [step for step in area.steps if step.key == f"mirror:{name}"]
    return found


def _three() -> mirror.Folder:
    return inbox((BATCHES[0], (1, 2)), (BATCHES[1], (3,)), (BATCHES[2], (4, 5, 6)))


# ═══════════════════════════════════════════════════════════════════════════
# 1. Live batches become playlists
# ═══════════════════════════════════════════════════════════════════════════


def test_three_live_batches_plan_three_inbox_playlists_with_their_account_tracks(
    installed, monkeypatch
):
    world = _world(installed, monkeypatch, _three())

    area = world.plan()
    step = _step(area)
    assert step.state == PLANNED
    assert step.counts["create folder"] == 1 and step.counts["create playlist"] == 3
    world.apply(area)

    inbox_id = world.folder_id("INBOX")
    assert sorted(world.account.folder_playlists(inbox_id).values()) == [
        f"INBOX {name}" for name in BATCHES
    ]
    assert world.held(f"INBOX {BATCHES[0]}") == ["r1", "r2"]
    assert world.held(f"INBOX {BATCHES[1]}") == ["r3"]
    assert world.held(f"INBOX {BATCHES[2]}") == ["r4", "r5", "r6"]
    assert world.account.deleted == []


def test_a_second_refresh_with_nothing_changed_plans_nothing(installed, monkeypatch):
    world = _world(installed, monkeypatch, _three())
    world.run()
    created, deleted = list(world.account.created), list(world.account.deleted)

    area = world.plan()

    assert [step.state for step in area.steps] == [NOTHING] and not area.writes
    assert area.deletes == []
    assert world.account.created == created and world.account.deleted == deleted


def test_a_persons_playlist_titled_inbox_batch_in_the_folder_is_left_and_named(
    installed, monkeypatch
):
    world = _world(installed, monkeypatch, _three())
    world.account.folder_names["hand-1"] = "INBOX"
    world.account.titles["mine-1"] = f"INBOX {BATCHES[1]}"
    world.account.playlists["mine-1"] = ["r99"]
    world.account.placed["mine-1"] = "hand-1"

    area = world.run()
    items = {item["playlist"]: item for item in _step(area).items[1:]}

    assert items[f"INBOX {BATCHES[1]}"]["action"] == mirror.LEFT
    assert "did not make" in items[f"INBOX {BATCHES[1]}"]["why"]
    assert sorted(world.account.created) == [f"INBOX {BATCHES[0]}", f"INBOX {BATCHES[2]}"]
    assert world.account.playlists["mine-1"] == ["r99"]
    # Never removed later either: the ledger records nothing of it.
    world.library = account_mirror.Library(folders=(inbox((BATCHES[0], (1, 2))),))
    area = world.run()
    assert "mine-1" not in [pid for pid, _held in world.account.deleted]
    assert world.account.playlists["mine-1"] == ["r99"]


# ═══════════════════════════════════════════════════════════════════════════
# 2. A batch that leaves INBOX
# ═══════════════════════════════════════════════════════════════════════════


def test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else(
    installed, monkeypatch
):
    world = _world(installed, monkeypatch, _three())
    world.run()
    gone = world.playlist_id(f"INBOX {BATCHES[0]}")
    others = {name: world.held(f"INBOX {name}") for name in BATCHES[1:]}
    chunks, moves, taken = list(world.account.chunks), list(world.account.moves), list(world.account.taken)

    # Moved into Old: no longer a live batch, and its title is not directly under INBOX.
    world.library = account_mirror.Library(
        folders=(inbox((BATCHES[1], (3,)), (BATCHES[2], (4, 5, 6)), present=(OLD,)),)
    )
    area = world.plan()
    step = _step(area)

    assert step.state == PLANNED and step.counts["remove playlist"] == 1
    assert {k: step.counts[k] for k in ("create playlist", "add", "remove")} == {
        "create playlist": 0,
        "add": 0,
        "remove": 0,
    }
    (removal,) = [item for item in step.items if item.get("action") == mirror.RETIRE]
    assert removal["playlist"] == f"INBOX {BATCHES[0]}" and removal["remote_id"] == gone
    assert area.deletes == [
        f"the mirrored playlist 'INBOX {BATCHES[0]}' ({gone}) off the account, since what "
        f"it mirrors left INBOX"
    ]

    (applied,) = world.apply(area)

    assert applied["retired"] == [f"INBOX {BATCHES[0]}"]
    assert world.account.deleted == [(gone, ("r1", "r2"))]
    assert {name: world.held(f"INBOX {name}") for name in BATCHES[1:]} == others
    assert (world.account.chunks, world.account.moves, world.account.taken) == (chunks, moves, taken)
    assert f"INBOX {BATCHES[0]}" not in ledger.mirror_folders(installed)["INBOX"].playlists
    assert gone not in ledger.mirror_playlist_ids(installed)
    # And the refresh after it plans nothing.
    assert [one.state for one in world.plan().steps] == [NOTHING]


def test_a_batch_still_under_inbox_that_no_longer_reads_as_one_is_left_not_removed(
    installed, monkeypatch
):
    """An unreadable landing record unrecognises a batch that never left."""
    world = _world(installed, monkeypatch, _three())
    world.run()
    kept = world.playlist_id(f"INBOX {BATCHES[2]}")

    world.library = account_mirror.Library(
        folders=(inbox((BATCHES[0], (1, 2)), (BATCHES[1], (3,)), present=(BATCHES[2],)),)
    )
    area = world.run()
    step = _step(area)

    assert step.state == NOTHING and step.counts["remove playlist"] == 0
    assert step.counts["left"] == 1 and "still in INBOX" in step.items[-1]["playlist"]
    assert world.account.deleted == [] and area.deletes == []
    assert world.held(f"INBOX {BATCHES[2]}") == ["r4", "r5", "r6"]
    assert kept in ledger.mirror_playlist_ids(installed)


def test_a_genre_folder_never_removes_a_playlist_it_no_longer_declares(installed, monkeypatch):
    """The removal is the retiring folder's alone; every other folder still leaves and names."""
    world = _world(installed, monkeypatch, folder("Techno", Low=(1,), High=(2,)))
    world.run()

    world.library = account_mirror.Library(folders=(folder("Techno", High=(2,)),))
    area = world.run()

    assert world.account.deleted == [] and area.deletes == []
    assert _step(area, "Techno").counts["left"] == 1


def test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again(
    installed, monkeypatch
):
    world = _world(installed, monkeypatch, _three())
    world.run()
    gone = world.playlist_id(f"INBOX {BATCHES[0]}")

    def refused(_pid):
        raise refuse(
            "outbound-remove-refused", "not vouched for", scope=Scope.SOURCE, origin=("test",)
        )

    monkeypatch.setattr(world.account, "remove_playlist", refused)
    world.library = account_mirror.Library(folders=(inbox((BATCHES[1], (3,)), (BATCHES[2], (4, 5, 6))),))
    area = world.plan()
    (applied,) = world.apply(area)

    assert applied["kept"] == [f"INBOX {BATCHES[0]}: not vouched for"]
    assert applied["retired"] == []
    assert [w["code"] for w in _step(area).warnings] == ["organize-mirror-kept"]
    # The record stays, so the next refresh plans the removal again.
    assert gone in ledger.mirror_playlist_ids(installed)
    assert _step(world.plan()).counts["remove playlist"] == 1


def test_a_playlist_removal_refused_for_any_other_reason_is_raised(installed, monkeypatch):
    world = _world(installed, monkeypatch, _three())
    world.run()

    def differs(_pid):
        raise refuse(
            "outbound-remove-refused", "still served", scope=Scope.RUN, origin=("test",)
        )

    monkeypatch.setattr(world.account, "remove_playlist", differs)
    world.library = account_mirror.Library(folders=(inbox((BATCHES[1], (3,)), (BATCHES[2], (4, 5, 6))),))
    area = world.plan()

    with pytest.raises(CratekitError) as caught:
        world.apply(area)
    assert caught.value.cause.message == "still served"
    assert world.playlist_id(f"INBOX {BATCHES[0]}") in ledger.mirror_playlist_ids(installed)


def test_a_playlist_already_gone_from_the_account_is_still_forgotten(installed, monkeypatch):
    world = _world(installed, monkeypatch, _three())
    world.run()
    gone = world.playlist_id(f"INBOX {BATCHES[0]}")
    world.account.playlists.pop(gone)
    world.account.titles.pop(gone)
    world.account.placed.pop(gone)

    world.library = account_mirror.Library(folders=(inbox((BATCHES[1], (3,)), (BATCHES[2], (4, 5, 6))),))
    world.run()

    assert gone not in ledger.mirror_playlist_ids(installed)


def test_forgetting_a_mirrored_playlist_drops_only_the_record_of_that_identifier(installed):
    ledger.reserve_mirror_playlist(installed, "INBOX", "INBOX a", lambda: "pl-a")
    ledger.reserve_mirror_playlist(installed, "INBOX", "INBOX b", lambda: "pl-b")

    ledger.forget_mirror_playlist(installed, "INBOX", "INBOX a", "pl-other")
    assert ledger.mirror_playlist_ids(installed) == {"pl-a", "pl-b"}

    ledger.forget_mirror_playlist(installed, "INBOX", "INBOX a", "pl-a")
    ledger.forget_mirror_playlist(installed, "INBOX", "INBOX a", "pl-a")
    ledger.forget_mirror_playlist(installed, "Elsewhere", "INBOX b", "pl-b")
    assert ledger.mirror_playlist_ids(installed) == {"pl-b"}
    assert not ledger.product_made(installed, "pl-a")


# ═══════════════════════════════════════════════════════════════════════════
# 3. A label batch, the sweep, the digest
# ═══════════════════════════════════════════════════════════════════════════


def test_a_live_batch_made_by_a_label_landing_plans_its_playlist_with_the_batchs_tracks(
    installed, monkeypatch
):
    """No account playlist holds a label batch; its rows' own provider tracks fill it."""
    world = _world(installed, monkeypatch, inbox((BATCHES[2], (4, 5, 6))))
    # The provider would match none of these rows by ISRC, a tie or no code.
    world.account.catalog.clear()
    monkeypatch.setattr(
        account_mirror, "landed_tracks", lambda _cfg: {"c4": "t-4", "c5": "t-5", "c6": "t-6"}
    )

    area = world.run()

    assert world.held(f"INBOX {BATCHES[2]}") == ["t-4", "t-5", "t-6"]
    assert world.account.matches == []
    assert area.facts[account_mirror.KNOWN_FACT].startswith("3 row(s) were matched")
    assert ledger.mirror_links(installed)["c4"] == ("t-4", "ISRC00004")


def test_a_row_the_ledger_already_links_keeps_its_link_over_a_landing_track(installed, monkeypatch):
    world = _world(installed, monkeypatch, inbox((BATCHES[2], (4,))))
    world.run()
    monkeypatch.setattr(account_mirror, "landed_tracks", lambda _cfg: {"c4": "t-4"})

    area = world.plan()

    assert [one.state for one in area.steps] == [NOTHING]
    assert account_mirror.KNOWN_FACT not in area.facts


def test_the_sweep_still_excludes_every_mirrored_inbox_playlist(installed, monkeypatch):
    world = _world(installed, monkeypatch, _three())
    world.run()
    ids = {world.playlist_id(f"INBOX {name}") for name in BATCHES}

    assert ids <= ledger.mirror_playlist_ids(installed)
    for playlist_id in ids:
        listed = playlists.AccountPlaylist(playlist_id, "INBOX x", 1)
        assert (
            playlists.exclusion(
                listed, recorded=set(), in_flight=set(), mirrored=ledger.mirror_playlist_ids(installed)
            )
            == playlists.Excluded.MIRROR
        )


def test_the_digest_covers_the_removal(installed, monkeypatch):
    world = _world(installed, monkeypatch, _three())
    world.run()
    world.library = account_mirror.Library(folders=(inbox((BATCHES[1], (3,)), (BATCHES[2], (4, 5, 6))),))
    retiring = _step(world.plan()).digest

    world.library = account_mirror.Library(
        folders=(inbox((BATCHES[1], (3,)), (BATCHES[2], (4, 5, 6)), present=(BATCHES[0],)),)
    )

    assert _step(world.plan()).digest != retiring


def test_an_inbox_with_no_live_batch_makes_no_empty_folder(installed, monkeypatch):
    world = _world(installed, monkeypatch, inbox(present=(OLD, "Analyze")))

    area = world.run()

    assert [one.state for one in area.steps] == [NOTHING]
    assert world.account.folders_created == []


def test_a_genre_folder_with_no_playlist_still_makes_its_folder(installed, monkeypatch):
    """Only the retiring folder waits for something to hold, U147's shape stands."""
    world = _world(installed, monkeypatch, mirror.Folder(name="Techno"))

    world.run()

    assert world.account.folders_created == ["Techno"]


def test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again(installed, monkeypatch):
    world = _world(installed, monkeypatch, _three())
    world.run()
    ids = {world.playlist_id(f"INBOX {name}") for name in BATCHES}
    del world.account.folder_names[world.folder_id("INBOX")]

    world.library = account_mirror.Library(folders=(inbox(present=(OLD,)),))
    area = world.run()

    assert _step(area).counts["create folder"] == 0
    assert world.account.folders_created == ["INBOX"]
    assert {pid for pid, _held in world.account.deleted} == ids
    assert not ids & ledger.mirror_playlist_ids(installed)


def test_an_inbox_that_cannot_be_read_is_listed_and_nothing_of_it_is_removed(
    installed, monkeypatch
):
    world = _world(installed, monkeypatch, _three())
    world.run()

    world.library = account_mirror.Library(inbox="INBOX is not mirrored: the intake tree is on the xml bridge")
    area = world.run()
    listed = {step.key: step for step in area.steps}

    assert listed["mirror:inbox"].state == LISTED and "xml bridge" in listed["mirror:inbox"].detail
    assert listed["mirror:INBOX"].state == LISTED
    assert world.account.deleted == [] and area.deletes == []


# ═══════════════════════════════════════════════════════════════════════════
# 4. The frozen plan carries the retirement
# ═══════════════════════════════════════════════════════════════════════════


def test_the_frozen_plan_carries_inbox_its_retirement_and_its_titles(installed):
    library = account_mirror.Library(
        folders=(inbox((BATCHES[1], (3,)), present=(OLD, "Analyze")), folder("Techno", Low=(1,))),
        inbox="",
    )

    mirror_frozen.freeze(installed, "2026-11-01T00:00:00Z-ab12", library, {})
    frozen, said = mirror_frozen.load(installed, "2026-11-01T00:00:00Z-ab12")

    assert said == "" and frozen is not None
    assert frozen.library == library
    listed = account_mirror.Library(inbox="INBOX is not mirrored: unadopted")
    mirror_frozen.freeze(installed, "2026-11-01T00:00:01Z-ab12", listed, {})
    assert mirror_frozen.load(installed, "2026-11-01T00:00:01Z-ab12")[0].library == listed


def test_a_frozen_folder_whose_retire_is_not_a_boolean_is_not_read(installed):
    library = account_mirror.Library(folders=(inbox((BATCHES[1], (3,))),))
    mirror_frozen.freeze(installed, "2026-11-01T00:00:00Z-cd34", library, {})
    path = config.state_path("mirror_plans", installed) / "2026-11-01T00:00:00Z-cd34.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["library"]["folders"][0]["retire"] = "yes"
    path.write_text(json.dumps(document), encoding="utf-8")

    frozen, said = mirror_frozen.load(installed, "2026-11-01T00:00:00Z-cd34")

    assert frozen is None and "is not one this build reads" in said


def test_frozen_titles_that_are_not_a_list_are_not_read(installed):
    """A string would read as a set of letters, and every batch still there as gone."""
    library = account_mirror.Library(folders=(inbox((BATCHES[1], (3,))),))
    mirror_frozen.freeze(installed, "2026-11-01T00:00:00Z-ef56", library, {})
    path = config.state_path("mirror_plans", installed) / "2026-11-01T00:00:00Z-ef56.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["library"]["folders"][0]["present"] = f"INBOX {BATCHES[1]}"
    path.write_text(json.dumps(document), encoding="utf-8")

    frozen, said = mirror_frozen.load(installed, "2026-11-01T00:00:00Z-ef56")

    assert frozen is None and "is not one this build reads" in said


def test_a_rebuild_from_a_frozen_plan_reads_no_landing_record(installed, monkeypatch):
    world = _world(installed, monkeypatch, inbox((BATCHES[2], (4,))))
    run = "2026-11-01T00:00:00Z-gh78"
    account_mirror.add_steps(installed, Area(name="account"), lambda: world.account,
                             account_mirror.Run(run_id=run, record=True))

    def unread(_cfg):
        raise AssertionError("a frozen rebuild read the landing records")

    monkeypatch.setattr(account_mirror, "landed_tracks", unread)
    area = Area(name="account")
    account_mirror.add_steps(installed, area, lambda: world.account,
                             account_mirror.Run(run_id=run, record=True, decided=True))

    assert _step(area).state == PLANNED


# ═══════════════════════════════════════════════════════════════════════════
# 5. What a live batch is, on a real schema
# ═══════════════════════════════════════════════════════════════════════════


def _live(cfg) -> rotate.Live:
    declared = active_taxonomy.load(cfg)
    handle = _open(cfg)
    try:
        return rotate.live_batches(
            cfg, handle, declared=declared, registry=tree_registry.read(cfg), today=TODAY
        )
    finally:
        rb_writer.close_db(handle)


def _inbox_folder(cfg) -> tuple[str, object]:
    declared = active_taxonomy.load(cfg)
    handle = _open(cfg)
    try:
        return account_mirror._inbox(cfg, handle, declared, tree_registry.read(cfg), TODAY)
    finally:
        rb_writer.close_db(handle)


@pytest.fixture
def batches(native_library):
    """Three live batches, one in Old, Analyze, a person's playlist and a folder."""
    cfg, root_id = native_library
    old_id = _node(cfg, OLD, under=root_id, folder=True)
    ids = {
        "dated": _node(
            cfg, "2026-09-23 Tidal playlists", under=root_id, age=10, tracks=("t1", "t2"),
            batch_folder=True,
        ),
        "suffix": _node(cfg, "2026-09-13T101010Z-1_inboxed", under=root_id, age=20, tracks=("t5",)),
        "label": _node(cfg, "2026-10-01 Defected", under=root_id, age=2, tracks=("t3", "t4")),
        "old": _node(cfg, "2026-05-01 Tidal playlists", under=old_id, age=150, tracks=("t6",)),
        "analyze": _node(cfg, native.ANALYZE, under=root_id, tracks=("t3",)),
        "mine": _node(cfg, "listen later", under=root_id, age=200, tracks=("t8",)),
        "folder": _node(cfg, "Lisa picks", under=root_id, folder=True),
    }
    # A label landing names its batch on its record by identifier.
    _record_landing(cfg, ids["label"], "2026-10-01 Defected", TODAY - timedelta(days=2))
    return cfg, root_id, ids


def test_the_live_batches_are_the_rotations_batches_directly_under_inbox(batches):
    cfg, _root, ids = batches

    live = _live(cfg)

    assert live.batches == (
        (ids["suffix"], "2026-09-13T101010Z-1_inboxed"),
        (ids["dated"], "2026-09-23 Tidal playlists"),
        (ids["label"], "2026-10-01 Defected"),
    )
    assert live.present == {
        "2026-09-23 Tidal playlists",
        "2026-09-13T101010Z-1_inboxed",
        "2026-10-01 Defected",
        OLD,
        native.ANALYZE,
        "listen later",
        "Lisa picks",
    }


def test_the_inbox_folder_reads_each_batch_under_its_account_title_with_its_rows(batches):
    cfg, _root, _ids = batches

    name, read = _inbox_folder(cfg)

    assert isinstance(read, mirror.Folder) and read.retire
    assert name == read.name
    assert {source.name: [one.content_id for one in source.rows] for source in read.playlists} == {
        f"{name} 2026-10-01 Defected": ["t3", "t4"],
        f"{name} 2026-09-13T101010Z-1_inboxed": ["t5"],
        f"{name} 2026-09-23 Tidal playlists": ["t1", "t2"],
    }
    assert f"{name} listen later" in read.present and f"{name} {OLD}" in read.present
    assert f"{name} 2026-05-01 Tidal playlists" not in read.present


def test_a_batch_with_no_date_is_still_live(native_library):
    """Its age decides the rotation, never whether it is in INBOX."""
    cfg, root_id = native_library
    later = _node(cfg, "2026-10-09 Favorites", under=root_id, tracks=("t1",), batch_folder=True)
    _record_landing(cfg, later, "2026-10-09 Favorites", TODAY + timedelta(days=6))

    assert [name for _id, name in _live(cfg).batches] == ["2026-10-09 Favorites"]


def test_a_stale_batch_is_live_until_it_actually_leaves_inbox(native_library):
    """Whether this run's rotation moves it is not known when the mirror is planned:
    its gate may be declined, or ``--only mirror`` asks for no rotation at all."""
    cfg, root_id = native_library
    stale = cfg.reports.intake_stale_days
    moving = _node(cfg, "a batch named by hand", under=root_id, age=0, tracks=("t1",))
    _record_landing(cfg, moving, "a batch named by hand", TODAY - timedelta(days=stale + 10))
    staying = _node(cfg, "another named by hand", under=root_id, age=0, tracks=("t2",))
    _record_landing(cfg, staying, "another named by hand", TODAY - timedelta(days=stale - 1))

    live = _live(cfg)

    assert live.batches == ((moving, "a batch named by hand"), (staying, "another named by hand"))


def test_two_batches_of_one_name_refuse_the_inbox_folder_by_name(native_library):
    cfg, root_id = native_library
    for _ in range(2):
        _node(cfg, "2026-09-23 Tidal playlists", under=root_id, age=10, tracks=("t1",))
    (Path(cfg.library.root) / cfg.library.music_dir / "2026-09-23 Tidal playlists").mkdir()

    name, read = _inbox_folder(cfg)

    assert name and isinstance(read, Cause) and read.reason == mirror.AMBIGUOUS_REASON


def test_an_intake_tree_still_on_the_bridge_lists_inbox_and_mirrors_none_of_it(acknowledged):
    name, why = _inbox_folder(acknowledged)

    assert name == "" and isinstance(why, str) and why.startswith("INBOX is not mirrored: ")


# ═══════════════════════════════════════════════════════════════════════════
# 6. The landing records each row's provider track
# ═══════════════════════════════════════════════════════════════════════════


def _landing_record(cfg, provider: object, *, workflow: str = native.WORKFLOW, n: int = 1) -> None:
    record = session.SessionRecord(
        session_id=f"20261031T12000{n}-landing",
        workflow=workflow,
        started="2026-10-31T12:00:00+00:00",
        state=session.SessionState.CLOSED,
        sources={INTAKE: "committed"},
        ended="2026-10-31T12:00:00+00:00",
        detail={label_filing.PROVIDER_KEY: provider},
    )
    session.write_record(record, cfg)


def test_landed_tracks_reads_every_native_landings_provider_tracks(native_library):
    cfg, _root = native_library
    _landing_record(cfg, {"t1": "111", "t2": "222", "t3": "333"}, n=1)
    _landing_record(cfg, {"t2": "222", "t3": "999", "t4": " "}, n=2)
    _landing_record(cfg, {"t5": "555"}, workflow="inbox-rotate", n=3)
    _landing_record(cfg, ["not", "a", "map"], n=4)

    # t3 is named two tracks, so neither decides it; t4 names nothing.
    assert account_mirror.landed_tracks(cfg) == {"t1": "111", "t2": "222"}


def test_the_label_plans_refs_leave_out_a_target_two_rows_name_two_tracks():
    one = type("Row", (), {"ref": "111"})()
    two = type("Row", (), {"ref": "222"})()
    blank = type("Row", (), {"ref": ""})()
    matched = {
        "Kompakt": {
            2024: [(one, ["/a.flac", "/shared.flac"])],
            2025: [(two, ["/b.flac", "/shared.flac"]), (blank, ["/c.flac"])],
        }
    }

    assert label_filing._refs(matched) == (("/a.flac", "111"), ("/b.flac", "222"))


def test_a_row_with_no_id_makes_no_claim_on_a_file_another_row_names():
    one = type("Row", (), {"ref": "101"})()
    blank = type("Row", (), {"ref": " "})()

    assert label_filing._refs({"Kompakt": {2025: [(one, ["/a.flac"]), (blank, ["/a.flac"])]}}) == (
        ("/a.flac", "101"),
    )
