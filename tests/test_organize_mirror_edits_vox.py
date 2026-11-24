"""R-2062: the account's mirror edits file the vocal sub by the vox My Tag, as the resort does.

U127 gave the vocal sub to the ``vox`` My Tag and R-2056 moved the check, the
rebuild and the resort onto it. A genre edit taken from the account derives
the track's new places by the same rule, so a membership the mirror writes is
never one the next resort takes back or adds again.
"""

from __future__ import annotations

import pytest

from cratekit.core import rb_writer, tags, taxonomy
from cratekit.core.cause import refuse
from cratekit.organize import mirror_edits
from cratekit.organize.steps import PLANNED, REFUSED
from cratekit.write import rebuild, vox_tag
from tests.test_organize_mirror_edits import Machine, without_fsync
from tests.test_organize_mirror_edits import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_routing_workers import CUT, _calibrated, _tag_vox
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import _release_process_locks as _release_process_locks
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414

#: Either side of the calibrated cut, as the routing workers read it.
UNDER, OVER = int(CUT) - 1, int(CUT) + 1

VOX = "with vox"


def _vocal(machine: Machine, content_id: str, level: int) -> None:
    assert tags.write_tags(machine.files[content_id], {"voxlevel": level})


def _hold_in(machine: Machine, place: tuple[str, str], content_id: str) -> None:
    """A membership the library already holds, as adoption or a resort wrote it."""
    handle = rb_writer.open_db(machine.db, unlock=False, cfg=machine.cfg)
    try:
        rb_writer.add_memberships(handle, handle.get_playlist(ID=machine.playlists[place]), [content_id])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)


def _resort_adds(machine: Machine) -> list[dict[str, str]]:
    """Every add the resort's gate would show now, through its own read (U219)."""
    reports, _opened = rebuild.preview_governed_trees(
        machine.cfg, tree_ids=(taxonomy.default_taxonomy().tree.id,), vocal_threshold=CUT
    )
    return [row for report in reports for row in rebuild.additions(report)]


def _vox_adds(machine: Machine, content_id: str) -> list[dict[str, str]]:
    """The resort's adds of one track to a vocal sub."""
    path = str(machine.files[content_id])
    return [row for row in _resort_adds(machine) if row["playlist"] == VOX and row["path"] == path]


def _settled(machine: Machine) -> None:
    """The mirror carries the library's new vocal sub onto the account, then nothing is left."""
    machine.run()
    machine.plans_nothing()


@pytest.fixture
def calibrated(acknowledged, tmp_path, monkeypatch) -> Machine:
    """The organize harness on a calibrated library, its first run not yet made."""
    without_fsync(monkeypatch)
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    built = Machine(acknowledged, scratch)
    _calibrated(acknowledged)
    return built


def _moved(machine: Machine, to: str) -> list[str]:
    """Track 1 moved on the account from Deep House Low into ``to``; the change's joins."""
    machine.take_off("Deep House Low", "r1")
    machine.put_in(to, "r1")
    _area, step = machine.run()
    assert step.state == PLANNED, step
    (change,) = [one for one in step.items if one.get("edit")]
    return change


@pytest.mark.parametrize(
    "to, kept",
    [
        ("Tech House Med", {("Tech House", "Med"), ("Tech House", VOX)}),
        ("Deep House High", {("Deep House", "High"), ("Deep House", VOX)}),
    ],
    ids=["to-another-genre", "within-its-genre"],
)
def test_a_tagged_track_under_the_cut_keeps_or_joins_its_new_folders_with_vox(calibrated, to, kept):
    machine = calibrated
    _vocal(machine, "1", UNDER)
    _tag_vox(machine.cfg, "1")
    _hold_in(machine, ("Deep House", VOX), "1")
    machine.run()
    assert machine.places("1") == {("Deep House", "Low"), ("Deep House", VOX)}

    change = _moved(machine, to)
    assert machine.places("1") == kept, change
    assert _vox_adds(machine, "1") == [], "the resort would add back what the mirror left"
    _settled(machine)


def test_an_untagged_track_over_the_cut_leaves_with_vox_and_joins_none(calibrated):
    machine = calibrated
    _vocal(machine, "1", OVER)
    # THE LIBRARY HAS THE TAG, on another row, so this is not the no tag library.
    _tag_vox(machine.cfg, "2")
    _hold_in(machine, ("Deep House", VOX), "1")
    machine.run()

    change = _moved(machine, "Tech House Med")
    assert set(change["leaves"]) == {"Deep House / Low", f"Deep House / {VOX}"}, change
    assert change["joins"] == ["Tech House / Med"], change
    assert machine.places("1") == {("Tech House", "Med")}
    assert _vox_adds(machine, "1") == []
    _settled(machine)


def test_a_library_with_no_vox_tag_files_no_with_vox_by_the_mirror(calibrated):
    machine = calibrated
    _vocal(machine, "1", OVER)
    machine.run()
    handle = rb_writer.open_db(machine.db, unlock=False, cfg=machine.cfg)
    try:
        assert vox_tag.vox_tagged(handle) is None, "the library carries a vox tag"
    finally:
        rb_writer.close_db(handle)

    change = _moved(machine, "Tech House Med")
    assert change["joins"] == ["Tech House / Med"], change
    assert machine.places("1") == {("Tech House", "Med")}


def test_an_uncalibrated_library_reads_no_tag(acknowledged, tmp_path, monkeypatch):
    """The tag is read only where it could file something, as the rebuild reads it."""
    without_fsync(monkeypatch)
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    machine = Machine(acknowledged, scratch)
    _tag_vox(machine.cfg, "1")
    machine.run()

    def unread(_db):
        raise AssertionError("the tag was read on an uncalibrated library")

    monkeypatch.setattr(vox_tag, "vox_tagged", unread)
    change = _moved(machine, "Tech House Med")
    assert change["joins"] == ["Tech House / Med"], change


def test_a_tag_that_cannot_be_read_refuses_the_step_alone(calibrated, monkeypatch):
    """A My Tag row that cannot say whether it was removed refuses, never files by a guess."""
    machine = calibrated
    _vocal(machine, "1", UNDER)
    _tag_vox(machine.cfg, "1")
    machine.run()
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")

    def unreadable(_db):
        raise refuse("soft-delete-marker-unreadable", "the marker cannot be read", origin=("test",))

    monkeypatch.setattr(vox_tag, "vox_tagged", unreadable)
    _area, step, _shared = machine.plan()
    assert step.state == REFUSED and step.cause.reason == "soft-delete-marker-unreadable", step
    assert machine.places("1") == {("Deep House", "Low")}


def test_the_plan_reads_the_tag_once(calibrated, monkeypatch):
    machine = calibrated
    _vocal(machine, "1", UNDER)
    _vocal(machine, "2", UNDER)
    _tag_vox(machine.cfg, "1")
    machine.run()
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")
    machine.take_off("Deep House Med", "r2")
    machine.put_in("Tech House Low", "r2")
    reads: list[object] = []
    real = vox_tag.vox_tagged

    def counted(db):
        reads.append(db)
        return real(db)

    monkeypatch.setattr(vox_tag, "vox_tagged", counted)
    _area, step, _shared = machine.plan()
    assert step.state == PLANNED
    assert len(reads) == 1, reads
    joins = {one["content_id"]: set(one["joins"]) for one in step.items if one.get("edit")}
    assert joins == {
        "1": {"Tech House / Med", f"Tech House / {VOX}"},
        "2": {"Tech House / Low"},
    }, joins
    assert step.key == mirror_edits.KIND
