"""U959: rekordbox's WIP folder mirrored onto the recording fake account, and its frozen plan. D1 applies."""

from __future__ import annotations

import json

from cratekit.core import config
from cratekit.modules.outbound import ledger, mirror
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize import account_mirror, mirror_frozen
from cratekit.organize.steps import NOTHING, PLANNED, Area
from tests import outbound_fakes
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_organize_mirror import row, soul
from tests.test_organize_mirror import world as world  # noqa: PLC0414 - fixture

SET = "deep and soulful"


# 1. The step over the recording fake account


def wip_folder(*playlists: tuple[str, tuple[int, ...]], unmirrored=()) -> mirror.Folder:
    """WIP as the library reads it, each ``(title, rows by number)``."""
    return mirror.Folder(
        name="WIP",
        playlists=tuple(mirror.Source(name=title, rows=tuple(row(n) for n in numbers)) for title, numbers in playlists),
        edits=edits.WIP,
        unmirrored=tuple(unmirrored),
    )


THREE = ((f"Phil {SET}", (1, 2)), ("Lisa lisa_sandbox", (3,)), ("WIP warmup", (4, 5)))


def _step(area: Area, name: str = "WIP"):
    (found,) = [step for step in area.steps if step.key == f"mirror:{name}"]
    return found


def test_wip_plans_one_account_folder_holding_each_title(world):
    world.mirror(wip_folder(*THREE), soul())
    area = world.plan()
    step = _step(area)
    assert step.state == PLANNED
    assert step.counts["create folder"] == 1 and step.counts["create playlist"] == 3
    assert _step(area, "Soul").state == PLANNED
    world.apply(area)
    wip_id = world.folder_id("WIP")
    assert sorted(world.account.folder_playlists(wip_id).values()) == sorted(title for title, _rows in THREE)
    assert world.held(f"Phil {SET}") == ["r1", "r2"]
    assert world.held("WIP warmup") == ["r4", "r5"]
    assert world.account.deleted == [] and area.deletes == []
    # And the refresh after it plans nothing.
    assert [one.state for one in world.plan().steps] == [NOTHING, NOTHING]


def test_a_playlist_removed_from_wip_leaves_its_account_playlist_where_it_is(world):
    world.mirror(wip_folder(*THREE))
    world.run()
    gone = world.playlist_id("Lisa lisa_sandbox")
    before = list(world.account.playlists[gone])
    world.mirror(wip_folder(THREE[0], THREE[2]))
    area = world.plan()
    step = _step(area)
    assert step.state == NOTHING and area.deletes == []
    (left,) = [item for item in step.items if item.get("action") == mirror.LEFT]
    assert left["playlist"].startswith(f"Lisa lisa_sandbox ({gone}): the folder no longer declares it")
    world.apply(area)
    assert world.account.deleted == [] and world.account.taken == []
    assert world.account.playlists[gone] == before


def test_every_node_wip_leaves_off_is_named_on_its_step(world):
    unmirrored = (
        ("Phil / Fresh this week, a smart playlist", "a smart playlist holds no membership"),
        ("Phil / paired set, paired by sync pair", "the mirror does not copy it a second time"),
    )
    world.mirror(wip_folder(THREE[0], unmirrored=unmirrored))
    step = _step(world.plan())
    assert step.detail.endswith(
        "; 2 node(s) in WIP not mirrored: Phil / Fresh this week, a smart playlist; "
        "Phil / paired set, paired by sync pair"
    )
    left = [item["playlist"] for item in step.items if item.get("action") == mirror.LEFT]
    assert left == [f"{label}: not mirrored, {reason}" for label, reason in unmirrored]


def test_no_wip_folder_is_one_fact_and_no_step(world):
    world.library = account_mirror.Library(folders=(soul(),), wip="the library holds no top level folder named 'WIP', so nothing is mirrored for it")
    area = world.plan()
    assert [step.key for step in area.steps] == ["mirror:Soul"]
    assert area.facts[account_mirror.WIP_FACT] == world.library.wip
    world.mirror(soul())
    assert account_mirror.WIP_FACT not in world.plan().facts


def _requests(world, *folders) -> int:
    world.account = outbound_fakes.StrictAccount(catalog={f"c{n}": f"r{n}" for n in range(1, 400)})
    world.mirror(*folders)
    return int(world.plan().facts[account_mirror.PLAN_FACT].split(" ")[0])


def test_wip_adds_only_its_own_rows_requests_to_the_plan(world):
    """The WIP folder is one more step of the same area: its rows' matches, the root read shared."""
    soul_alone = _requests(world, soul())
    wip_alone = _requests(world, wip_folder(*THREE))
    beside = _requests(world, soul(), wip_folder(*THREE))
    # One root folder read, then one match per row: five WIP rows.
    assert wip_alone == 1 + 5
    assert beside == soul_alone + wip_alone - 1


def test_the_mirrored_wip_titles_are_what_sync_pair_reads(world, installed):
    from cratekit.sync import pair_discover

    world.mirror(wip_folder(*THREE))
    world.run()
    assert pair_discover.mirrored_wip(installed) == frozenset(title for title, _rows in THREE)


# 2. The frozen plan


def test_the_frozen_plan_carries_wip_its_rule_its_unmirrored_and_why_not(installed):
    library = account_mirror.Library(
        folders=(wip_folder(THREE[0], unmirrored=(("Phil / smart, a smart playlist", "no membership"),)),),
    )
    mirror_frozen.freeze(installed, "2026-11-24T00:00:00Z-ab12", library, {})
    frozen, said = mirror_frozen.load(installed, "2026-11-24T00:00:00Z-ab12")
    assert said == "" and frozen is not None and frozen.library == library
    listed = account_mirror.Library(wip="the library holds no top level folder named 'WIP', so nothing is mirrored for it")
    mirror_frozen.freeze(installed, "2026-11-24T00:00:01Z-ab12", listed, {})
    assert mirror_frozen.load(installed, "2026-11-24T00:00:01Z-ab12")[0].library == listed


def test_a_plan_frozen_before_wip_reads_as_no_reason_given(installed):
    mirror_frozen.freeze(installed, "2026-11-24T00:00:02Z-ab12", account_mirror.Library(), {})
    path = config.state_path("mirror_plans", installed) / "2026-11-24T00:00:02Z-ab12.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["library"].pop("wip")
    path.write_text(json.dumps(document), encoding="utf-8")
    frozen, said = mirror_frozen.load(installed, "2026-11-24T00:00:02Z-ab12")
    assert said == "" and frozen is not None and frozen.library.wip == ""


def test_the_answering_run_applies_the_wip_plan_its_gate_showed(world, installed):
    world.mirror(wip_folder(*THREE))
    run = "2026-11-24T00:00:00Z-ef56"
    gate = Area(name="account")
    account_mirror.add_steps(installed, gate, lambda: world.account, account_mirror.Run(run_id=run, record=True))
    shown = _step(gate).digest
    # rekordbox moved after the gate: a playlist left WIP and another came in.
    world.mirror(wip_folder(THREE[0], ("Phil later", (6,))))
    area = Area(name="account")
    account_mirror.add_steps(installed, area, lambda: world.account, account_mirror.Run(run_id=run, decided=True))
    assert _step(area).digest == shown
    assert area.facts[account_mirror.FROZEN_FACT].startswith(f"rebuilt from the plan frozen on run {run}")
    world.apply(area)
    assert sorted(world.account.folder_playlists(world.folder_id("WIP")).values()) == sorted(t for t, _r in THREE)
    assert "Phil later" not in world.account.titles.values()
    assert sorted(ledger.mirror_folders(installed)["WIP"].playlists) == sorted(t for t, _r in THREE)
