"""U214: every INBOX node the mirror leaves off the account is named, with its reason.

The rotation's classifier and plan, the organize step over the fake account, and
the frozen plan carrying the lines to the run that applies. D1 applies.
"""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from dataclasses import replace
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from cratekit.core import active_taxonomy, config, rb_writer, session, tree_registry
from cratekit.intake import native, rotate, rotate_cli
from cratekit.modules.outbound import mirror
from cratekit.organize import account_mirror, mirror_frozen
from cratekit.organize import rekordbox as rekordbox_area
from cratekit.organize.steps import NOTHING, PLANNED, Area
from tests.test_inbox_rotate import OLD, TODAY, _node, _open, _record_landing
from tests.test_inbox_rotate import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_inbox_rotate import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_inbox_rotate import acknowledged as acknowledged  # noqa: PLC0414 - fixture
from tests.test_inbox_rotate import machine as machine  # noqa: PLC0414 - fixture
from tests.test_inbox_rotate import native_library as native_library  # noqa: PLC0414 - fixture
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_organize_mirror import World, row
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414 - fixture

BATCH = "2026-09-23 Tidal playlists"
LABELS = "2026-10-08 Labels"
FOLDER = "Lisa picks"
SMART = "Fresh this week"

#: Each node the brief's INBOX leaves off, by name, to its kind.
KINDS = {
    OLD: rotate.LEFT_OLD, native.ANALYZE: rotate.LEFT_ANALYZE, FOLDER: rotate.LEFT_FOLDER,
    LABELS: rotate.LEFT_UNRECOGNISED, SMART: rotate.LEFT_SMART,
}


@pytest.fixture
def brief(native_library):
    """The brief's INBOX in one open: a batch, Old, Analyze, a folder, a label and a smart one."""
    cfg, root_id = native_library
    ids: dict[str, str] = {}
    with _opened(cfg) as handle:
        def make(key, name, under, age=None, tracks=(), *, folder=False, smart=False):
            create = handle.create_playlist_folder if folder else handle.create_playlist
            made = create(name, parent=handle.get_playlist(ID=under))
            if age is not None:
                made.created_at = datetime.combine(TODAY - timedelta(days=age), datetime.min.time())
            for content_id in tracks:
                handle.add_to_playlist(made, content_id)
            if smart:
                made.Attribute = 4
            handle.session.commit()
            ids[key] = str(made.ID)

        make("old", OLD, root_id, folder=True)
        make("batch", BATCH, root_id, 10, ("t1", "t2"))
        make("old batch", "2026-05-01 Tidal playlists", ids.pop("old"), 150, ("t6",))
        make("analyze", native.ANALYZE, root_id, tracks=("t3",))
        make("folder", FOLDER, root_id, folder=True)
        # Dated, three rows, and no batch folder or record: no rule recognises it.
        make("labels", LABELS, root_id, 5, ("t3", "t4", "t5"))
        make("smart", SMART, root_id, smart=True)
    for batch in (BATCH, "2026-05-01 Tidal playlists"):
        (Path(cfg.library.root) / cfg.library.music_dir / batch).mkdir(parents=True)
    return cfg, root_id, ids


@contextmanager
def _opened(cfg):
    handle = _open(cfg)
    try:
        yield handle
    finally:
        rb_writer.close_db(handle)


def _live(cfg, declared=None) -> rotate.Live:
    declared = declared or active_taxonomy.load(cfg)
    with _opened(cfg) as handle:
        registry = tree_registry.read(cfg)
        return rotate.live_batches(cfg, handle, declared=declared, registry=registry, today=TODAY)


def _rotation(cfg) -> rotate.RotationPlan:
    with _opened(cfg) as handle:
        return rotate.plan_rotation(
            cfg, handle, declared=active_taxonomy.load(cfg), registry=tree_registry.read(cfg), today=TODAY
        )


def _organized_rotation(cfg) -> tuple[Area, object]:
    """The organize step's rotation over ``cfg``: its area, and the step it answers."""
    area = Area(name="rekordbox")
    return area, rekordbox_area._rotation(cfg, active_taxonomy.load(cfg), TODAY, area)


def _inbox(cfg) -> mirror.Folder:
    with _opened(cfg) as handle:
        declared, registry = active_taxonomy.load(cfg), tree_registry.read(cfg)
        _name, read = account_mirror._inbox(cfg, handle, declared, registry, TODAY)
    assert isinstance(read, mirror.Folder), read
    return read


# 1. The classifier names every node it does not take as a batch


def test_the_live_batches_name_every_other_node_under_inbox_with_its_kind(brief):
    cfg, _root, ids = brief
    live = _live(cfg)
    assert live.batches == ((ids["batch"], BATCH),)
    assert {node.name: node.kind for node in live.left} == KINDS
    # The label playlist is named as unrecognised with its row count.
    (labels,) = [node for node in live.left if node.name == LABELS]
    assert labels.tracks == 3
    assert labels.playlist_id == ids["labels"]
    assert "no landing record names it" in labels.reason
    assert labels.label() == f"{LABELS} (3 row(s)), not recognised as a batch"
    # A plain playlist is counted, a folder or a smart playlist is not.
    counted = {node.name: node.tracks for node in live.left}
    assert counted[native.ANALYZE] == 1
    assert counted[OLD] is None and counted[FOLDER] is None and counted[SMART] is None
    # Nothing inside Old is a direct child of INBOX, so nothing of it is named.
    assert "2026-05-01 Tidal playlists" not in counted


def test_an_undeclared_old_is_named_as_a_folder(brief):
    cfg, _root, _ids = brief
    declared = replace(active_taxonomy.load(cfg), intake_old=None)
    live = _live(cfg, declared)
    assert {node.name: node.kind for node in live.left}[OLD] == rotate.LEFT_FOLDER


def test_an_undated_batch_is_mirrored_and_not_named_left(native_library):
    """A batch with no age is still live: it is a mirrored batch, not a node left off."""
    cfg, root_id = native_library
    later = _node(cfg, "2026-10-09 Favorites", under=root_id, tracks=("t1",), batch_folder=True)
    # Its record dates it after the day read for, so its age is unknown.
    _record_landing(cfg, later, "2026-10-09 Favorites", TODAY + timedelta(days=6))
    assert _rotation(cfg).left[0].kind == rotate.LEFT_UNDATED
    live = _live(cfg)
    assert [name for _id, name in live.batches] == ["2026-10-09 Favorites"]
    assert live.left == ()


def test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none(native_library):
    """Unread is not none: the record a later build wrote may be the one naming it."""
    cfg, root_id = native_library
    batch = _node(cfg, "2026-09-20 Defected", under=root_id, age=13, tracks=("t1", "t2"))
    _record_landing(cfg, batch, "2026-09-20 Defected", TODAY - timedelta(days=13))
    (entry,) = sorted(session.log_dir(cfg).glob("*.json"))
    data = json.loads(entry.read_text(encoding="utf-8"))
    data["schema_version"] = 2
    entry.write_text(json.dumps(data), encoding="utf-8")
    (node,) = _live(cfg).left
    planned = _rotation(cfg)
    assert node.kind == rotate.LEFT_UNRECOGNISED
    assert node.reason.startswith(
        "no readable landing record names it (1 session record(s) could not be read, "
        "and one of them may)"
    )
    assert "no landing record names it" not in node.reason
    assert planned.unreadable_records == 1
    assert [(one.name, one.reason) for one in planned.left] == [(node.name, node.reason)]
    assert dict(_inbox(cfg).unmirrored)[node.label()] == node.reason


def _refuse_under(monkeypatch, call: str, under: Path) -> None:
    """Refuse one os call at or under ``under``, since no mode bars the container's root."""
    real = getattr(os, call)

    def refused(path, *args, **kwargs):
        if Path(path) == under or under in Path(path).parents:
            raise PermissionError(13, "Permission denied", str(path))
        return real(path, *args, **kwargs)

    monkeypatch.setattr(os, call, refused)


def test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record(native_library, monkeypatch):
    """The scan's glob answers an unlistable log with nothing; nothing is not none."""
    cfg, root_id = native_library
    batch = _node(cfg, "2026-09-20 Defected", under=root_id, age=13, tracks=("t1", "t2"))
    _record_landing(cfg, batch, "2026-09-20 Defected", TODAY - timedelta(days=13))
    assert [name for _id, name in _live(cfg).batches] == ["2026-09-20 Defected"]
    log = Path(session.log_dir(cfg))
    # The scan asks the listing itself since R-1255, so refusing it is enough;
    # the glob it used to read is refused too, as an unprivileged account is.
    _refuse_under(monkeypatch, "listdir", log)
    _refuse_under(monkeypatch, "scandir", log)
    (node,) = _live(cfg).left
    assert rotate.landings(cfg).unlisted is True
    assert node.kind == rotate.LEFT_UNRECOGNISED
    assert node.reason.startswith(
        "no readable landing record names it (the session log could not be listed, "
        "and a record in it may)"
    )
    assert [(one.name, one.reason) for one in _rotation(cfg).left] == [(node.name, node.reason)]
    # The plan carries the listing to every warning: unlisted, never a count of one.
    plan = _rotation(cfg)
    assert plan.log_unlisted is True
    listed = (
        "the session log could not be listed, so a batch a record in it names was "
        "aged from its playlist's creation date"
    )
    assert [one["message"] for one in rotate_cli.records_warnings(plan)] == [listed]
    _area, step = _organized_rotation(cfg)
    assert [one["message"] for one in step.warnings] == [listed]


def test_an_absent_session_log_is_no_record_at_all(native_library):
    """A library nothing ever landed in has no log, and that is read as none."""
    cfg, _root = native_library
    log = Path(session.log_dir(cfg))
    if log.exists():
        for entry in log.iterdir():
            entry.unlink()
        log.rmdir()
    assert rotate.landings(cfg).unlisted is False
    assert rotate.landings(cfg).unread() == ""


def test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder(native_library, monkeypatch):
    cfg, root_id = native_library
    _node(cfg, BATCH, under=root_id, age=10, tracks=("t1",), batch_folder=True)
    assert [name for _id, name in _live(cfg).batches] == [BATCH]
    _refuse_under(monkeypatch, "stat", Path(cfg.library.root) / cfg.library.music_dir)
    (node,) = _live(cfg).left
    assert node.kind == rotate.LEFT_UNRECOGNISED
    assert node.reason.endswith(
        "and the music folder could not be read to look for a batch folder of its "
        "name, which may be there"
    )
    assert "no batch folder under the music folder carries its name" not in node.reason


def test_a_dated_playlist_with_no_batch_folder_still_says_so(native_library):
    """The readable case keeps its plain wording."""
    cfg, root_id = native_library
    _node(cfg, LABELS, under=root_id, age=5, tracks=("t3",))
    (node,) = _live(cfg).left
    assert node.reason == (
        "no landing record names it, its name does not end _inboxed, and no batch "
        "folder under the music folder carries its name"
    )


def test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours(brief):
    """Only the Old directly under INBOX is the rotation's own folder."""
    cfg, _root, _ids = brief
    planned = _rotation(cfg)
    (nested,) = [_node(cfg, OLD, under=planned.old_id, folder=True)]
    again = _rotation(cfg)
    (inside,) = [node for node in again.left if node.playlist_id == nested]
    assert (inside.kind, inside.place) == (rotate.LEFT_FOLDER, again.old_place)
    area, _step = _organized_rotation(cfg)
    assert [one["kind"] for one in area.yours if one["name"] == OLD] == [rotate.LEFT_FOLDER]


# 2. The mirror's INBOX folder and the rotation's plan name the same nodes


def test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes(brief):
    cfg, _root, _ids = brief
    read = _inbox(cfg)
    assert [source.name for source in read.playlists] == [f"{read.name} {BATCH}"]
    assert [label for label, _reason in read.unmirrored] == [
        f"{LABELS} (3 row(s)), not recognised as a batch",
        f"{native.ANALYZE} (1 row(s)), the Analyze playlist",
        f"{SMART}, a smart playlist",
        f"{FOLDER}, a folder",
        f"{OLD}, the Old folder",
    ]
    reasons = dict(read.unmirrored)
    assert reasons[f"{OLD}, the Old folder"].startswith("the folder a stale batch moves into")
    assert reasons[f"{SMART}, a smart playlist"] == "a smart playlist is never a batch"


def test_the_rotation_plan_names_the_same_nodes_the_same_way(brief):
    cfg, _root, _ids = brief
    planned = _rotation(cfg)
    live = _live(cfg)
    under_inbox = [node for node in planned.left if node.place == planned.tree_id]
    assert {node.name: node.kind for node in under_inbox} == KINDS
    assert sorted(under_inbox, key=lambda node: (node.name, node.playlist_id)) == list(live.left)
    # The batch is the rotation's too, and the batch in Old is its, never left.
    assert [batch.name for batch in planned.kept] == [BATCH]
    assert [batch.name for batch in planned.removals] == ["2026-05-01 Tidal playlists"]
    assert [node.name for node in planned.left if node.place != planned.tree_id] == []


def test_the_rotation_payload_shows_each_left_node_with_its_row_count(brief):
    cfg, _root, _ids = brief
    planned = _rotation(cfg)
    shown = rotate_cli.plan_payload(planned)
    left = {item["playlist"]: item for item in shown["items"] if item["action"] == rotate_cli.LEAVE}
    assert set(left) == set(KINDS)
    assert left[LABELS]["tracks"] == 3 and left[LABELS]["kind"] == rotate.LEFT_UNRECOGNISED
    assert "tracks" not in left[FOLDER] and "tracks" not in left[OLD]
    assert shown["totals"]["left alone"] == len(KINDS)


def test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest(brief):
    """Nothing writes a left playlist, so a person adding to it does not stale the gate."""
    cfg, _root, ids = brief
    before = _rotation(cfg)
    with _opened(cfg) as handle:
        handle.add_to_playlist(handle.get_playlist(ID=ids["labels"]), "t6")
        handle.session.commit()
    after = _rotation(cfg)
    assert {node.name: node.tracks for node in after.left}[LABELS] == 4
    assert after.digest == before.digest


def test_a_renamed_left_playlist_still_moves_the_rotations_digest(brief):
    """The row count is the only fact left out; the node itself is still covered."""
    cfg, _root, ids = brief
    before = _rotation(cfg)
    with _opened(cfg) as handle:
        handle.get_playlist(ID=ids["labels"]).Name = "2026-10-08 Label picks"
        handle.session.commit()
    assert _rotation(cfg).digest != before.digest


def test_the_organize_rotation_step_does_not_list_old_as_yours(brief):
    cfg, _root, _ids = brief
    area, _step = _organized_rotation(cfg)
    yours = {one["name"] for one in area.yours}
    assert OLD not in yours
    assert {FOLDER, LABELS, SMART, native.ANALYZE} <= yours


# 3. The organize step names them on its plan and its line

UNMIRRORED = (
    (f"{LABELS} (36 row(s)), not recognised as a batch", "no landing record names it"),
    (f"{OLD}, the Old folder", "the folder a stale batch moves into is never a batch"),
)


def _with_unmirrored(*batches: tuple[str, tuple[int, ...]]) -> mirror.Folder:
    sources = tuple(
        mirror.Source(name=mirror.title("INBOX", name), rows=tuple(row(n) for n in numbers))
        for name, numbers in batches
    )
    present = frozenset(source.name for source in sources)
    return mirror.Folder(
        name="INBOX", playlists=sources, retire=True, present=present, unmirrored=UNMIRRORED
    )


def _inbox_step(area: Area):
    (found,) = [step for step in area.steps if step.key == "mirror:INBOX"]
    return found


def _named(step) -> list[str]:
    return [item["playlist"] for item in step.items if item["action"] == mirror.LEFT]


def test_the_inbox_step_names_each_unmirrored_node_on_its_plan_and_its_line(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(_with_unmirrored((BATCH, (1, 2))))
    step = _inbox_step(world.plan())
    assert step.state == PLANNED
    assert _named(step) == [
        f"{LABELS} (36 row(s)), not recognised as a batch: not mirrored, no landing record names it",
        f"{OLD}, the Old folder: not mirrored, the folder a stale batch moves into is never a batch",
    ]
    assert step.counts["left"] == 2
    assert step.detail.endswith(
        f"; 2 node(s) in INBOX not mirrored: {LABELS} (36 row(s)), not recognised as a "
        f"batch; {OLD}, the Old folder"
    )


def test_an_inbox_with_nothing_to_write_still_names_them(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(_with_unmirrored((BATCH, (1,))))
    world.run()
    step = _inbox_step(world.plan())
    assert step.state == NOTHING
    assert len(_named(step)) == 2 and step.counts["left"] == 2
    assert "2 left as they are" in step.detail
    assert f"2 node(s) in INBOX not mirrored: {LABELS}" in step.detail


def test_an_inbox_with_no_batch_at_all_still_names_them(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(_with_unmirrored())
    step = _inbox_step(world.plan())
    assert step.state == NOTHING
    assert len(_named(step)) == 2
    assert "2 node(s) in INBOX not mirrored" in step.detail


def test_the_unmirrored_lines_take_no_part_in_the_digest(installed, monkeypatch):
    """Naming a node writes nothing, so it moves no gate."""
    world = World(installed, monkeypatch)
    world.mirror(_with_unmirrored((BATCH, (1,))))
    named = _inbox_step(world.plan()).digest
    world.mirror(replace(_with_unmirrored((BATCH, (1,))), unmirrored=()))
    assert _inbox_step(world.plan()).digest == named


def test_a_genre_folder_names_no_unmirrored_node(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(mirror.Folder(name="Techno", playlists=(mirror.Source("Techno Low", (row(1),)),)))
    (step,) = world.plan().steps
    assert "not mirrored" not in step.detail and _named(step) == []


# 4. The frozen plan carries them to the run that applies


def test_the_frozen_plan_carries_the_unmirrored_nodes(installed):
    library = account_mirror.Library(folders=(_with_unmirrored((BATCH, (1,))),))
    mirror_frozen.freeze(installed, "2026-11-05T00:00:00Z-u214", library, {})
    frozen, said = mirror_frozen.load(installed, "2026-11-05T00:00:00Z-u214")
    assert said == "" and frozen is not None
    assert frozen.library == library
    assert frozen.library.folders[0].unmirrored == UNMIRRORED


def test_a_rebuild_from_the_frozen_plan_still_names_them(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(_with_unmirrored((BATCH, (1,))))
    run = "2026-11-05T00:00:00Z-u215"
    recorded = account_mirror.Run(run_id=run, record=True)
    account_mirror.add_steps(installed, Area(name="account"), lambda: world.account, recorded)
    # The library now reads empty: a rebuild that named the nodes took the frozen one.
    world.mirror()
    area = Area(name="account")
    decided = account_mirror.Run(run_id=run, record=True, decided=True)
    account_mirror.add_steps(installed, area, lambda: world.account, decided)
    step = _inbox_step(area)
    assert len(_named(step)) == 2
    assert "2 node(s) in INBOX not mirrored" in step.detail


def _frozen_as(cfg, run: str, edit) -> tuple:
    """A frozen plan written, its document changed by ``edit``, and read back."""
    library = account_mirror.Library(folders=(_with_unmirrored((BATCH, (1,))),))
    mirror_frozen.freeze(cfg, run, library, {})
    path = config.state_path("mirror_plans", cfg) / f"{run}.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    edit(document)
    path.write_text(json.dumps(document), encoding="utf-8")
    return mirror_frozen.load(cfg, run)


@pytest.mark.parametrize(
    "held",
    ["INBOX Old", [["a label only"]], [["a label", 3]], [("a", "b", "c")]],
    ids=["text", "one part", "not text", "three parts"],
)
def test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read(installed, held):
    def edit(document):
        document["library"]["folders"][0]["unmirrored"] = held

    frozen, said = _frozen_as(installed, "2026-11-05T00:00:00Z-ab12", edit)
    assert frozen is None and "is not one this build reads" in said


def test_a_version_four_frozen_plan_is_planned_afresh(installed):
    """Version 4 carried no unmirrored nodes, so a rebuild from it would lose every line."""

    def edit(document):
        document["version"] = 4
        del document["library"]["folders"][0]["unmirrored"]

    frozen, said = _frozen_as(installed, "2026-11-05T00:00:00Z-cd34", edit)
    # 7 since U236, which froze the placements beside the snapshots U222 froze;
    # a version 4 record is still refused.
    assert mirror_frozen.VERSION == 7
    assert frozen is None and "version 4" in said
