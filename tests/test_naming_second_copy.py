"""U212: a rename held back by a second copy of one recording says so.

Sitting 55 (A70) downloaded two tracks an unlanded pass had already staged and
named. The new copies, named for their provider ids, rendered to the names the
earlier copies held, and ``name apply`` refused ``rename-incomplete`` with "is
already taken in the folder by a file nothing here is renaming", which sent the
session to compare audio by hand. When the file in the way carries the same
ISRC as the file held back, the plan and the refusal now say it is the same
recording twice, and carry the ISRC for the verb that ran the step.
"""

# ruff: noqa: F811, the fixtures below are imported from the naming apply suite by name
from __future__ import annotations

from cratekit.core import tags
from cratekit.core.exit_codes import ExitCode
from tests.test_naming_apply_cli import (  # noqa: F401 - fixtures by name
    _actions,
    _answer,
    _folder,
    _plan,
    _track,
    configured,
    library,
)

ISRC = "GBAAA2601101"


def _copies(folder, *, earlier: str | None, newer: str | None):
    """The copy an earlier pass named, and the one a later pass staged under its id."""
    named = _track(folder, "Artist 101 - Title 101.flac")
    fresh = _track(folder, "101.flac")
    for path, isrc in ((named, earlier), (fresh, newer)):
        fields = {"artist": "Artist 101", "title": "Title 101"}
        if isrc is not None:
            fields["isrc"] = isrc
        assert tags.write_tags(path, fields)
    return named, fresh


def test_a_target_held_by_the_same_recording_is_said_as_a_second_copy(configured):
    folder = _folder(configured)
    named, fresh = _copies(folder, earlier=ISRC, newer="gb-aaa-26-01101")

    plan = _plan(folder)

    assert _actions(plan) == {fresh.name: "collides"}
    (item,) = plan["items"]
    assert item["isrc"] == ISRC
    assert item["why"] == (
        f"{named.name} is already taken in the folder by a file carrying the same "
        f"ISRC {ISRC}, a second copy of one recording, so this one is not renamed"
    )
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "rename-incomplete"
    assert f"the same ISRC {ISRC}" in cause["message"]
    (owed,) = cause["detail"]["incomplete"]
    assert (owed["from"], owed["isrc"]) == (fresh.name, ISRC)
    assert any(
        step.startswith("a file held back as a second copy carries the same ISRC")
        for step in cause["remediation"]["steps"]
    ), cause["remediation"]["steps"]
    assert fresh.is_file() and named.is_file()


def test_a_target_held_by_another_recording_keeps_the_plain_collision(configured):
    folder = _folder(configured)
    named, fresh = _copies(folder, earlier="GBAAA2601999", newer=ISRC)

    (item,) = _plan(folder)["items"]

    assert "isrc" not in item
    assert item["why"] == (
        f"{named.name} is already taken in the folder by a file nothing here is renaming"
    )


def test_a_copy_with_no_isrc_on_either_side_is_never_called_the_same_recording(configured):
    """Absence of a read is not a match: no ISRC on the file in the way, then
    none on the file held back."""
    folder = _folder(configured)
    _copies(folder, earlier=None, newer=ISRC)
    (item,) = _plan(folder)["items"]
    assert "isrc" not in item and "ISRC" not in item["why"]


def test_a_held_back_copy_with_no_isrc_is_never_called_the_same_recording(configured):
    folder = _folder(configured)
    _copies(folder, earlier=ISRC, newer=None)
    (item,) = _plan(folder)["items"]
    assert "isrc" not in item and "ISRC" not in item["why"]


def test_two_movers_sharing_a_target_a_copy_holds_carry_no_isrc(configured):
    """Review round one, F3: the reason is the two movers', so the item carries
    no ISRC that would describe the file on disk instead."""
    folder = _folder(configured)
    _copies(folder, earlier=ISRC, newer=ISRC)
    third = _track(folder, "102.flac")
    assert tags.write_tags(third, {"artist": "Artist 101", "title": "Title 101", "isrc": ISRC})

    plan = _plan(folder)

    held = [item for item in plan["items"] if item["action"] == "collides"]
    assert {item["from"] for item in held} == {"101.flac", "102.flac"}
    for item in held:
        assert "render to the same name" in item["why"] or "renders to the same name" in item["why"]
        assert "isrc" not in item


def test_a_copy_that_takes_the_name_after_the_plan_is_said_a_second_copy(configured):
    """Review round one, F8, the claim after the gate. ``lead`` renders onto the
    name ``marked`` holds while ``marked`` is itself moving, so the plan leaves
    it promised (R-172) and the claim finds the name taken by a file carrying
    the same ISRC."""
    folder = _folder(configured)
    marker = configured.naming.lossy_marker
    lead = _track(
        folder, "01A - 120 - Alpha - Artist - Alpha.flac", title="01A - 120 - Alpha", key="01A"
    )
    marked = _track(
        folder, "01A - 120 - Alpha - Artist.flac", title=f"01A - 120 - Alpha {marker}", key="01A"
    )
    for path in (lead, marked):
        assert tags.write_tags(path, {"isrc": ISRC})
    assert _actions(_plan(folder)) == {lead.name: "rename", marked.name: "rename"}

    code, envelope = _answer(folder)

    assert code == int(ExitCode.PRECONDITION), envelope
    (owed,) = envelope["cause"]["detail"]["incomplete"]
    assert (owed["from"], owed["isrc"]) == (lead.name, ISRC)
    assert f"the same ISRC {ISRC}, a second copy of one recording" in owed["why"]
