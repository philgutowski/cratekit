"""U28: the verb that installs the shipped operator skills.

WHY THIS FILE EXISTS SEPARATELY FROM THE LINT SUITE. ``tests/test_skills_lint.py``
answers whether the skills are CORRECT, which is a property of their text. This
answers whether a person can get them, which is a property of the verb, and the
two rot in different directions: a skill can be perfectly written and reachable
by nobody, and the conformance suite drives this verb only far enough to prove it
emits a well formed envelope.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real machine.
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from cratekit import __version__, cli
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.skills import cli as skills_cli


def _drive(argv: list[str]) -> tuple[int, dict]:
    """Run the REAL dispatcher and return the status with the parsed envelope."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def test_a_clean_directory_gets_every_shipped_skill_with_a_stamp(tmp_path):
    """The headline scenario, and the count is DERIVED rather than pinned.

    A literal here would be a second register of which skills ship, and it would
    be right on the day it was written and wrong the day one was added beside the
    others (P3).
    """
    into = tmp_path / "agent"

    code, envelope = _drive(["skills", "install", "--into", str(into)])

    assert code == int(ExitCode.OK), envelope
    shipped = skills_cli.shipped_names()
    assert shipped, "the package ships no skills, so this proves nothing"
    assert envelope["data"]["summary"]["installed"] == len(shipped)
    for name in shipped:
        assert (into / name / "SKILL.md").is_file()
        assert skills_cli.installed_version(into / name) == __version__


def test_the_copies_are_copies_and_not_symlinks(tmp_path):
    """The whole reason the verb exists rather than a line of shell.

    A symlink points into the installed package, which is this machine's virtual
    environment or somebody's checkout. The moment that path moves the agent gets
    nothing, and the failure reads as a missing skill rather than a broken link.
    """
    into = tmp_path / "agent"
    _drive(["skills", "install", "--into", str(into)])

    for name in skills_cli.shipped_names():
        skill = into / name / "SKILL.md"
        assert not skill.is_symlink(), f"{name} was linked rather than copied"
        assert not (into / name).is_symlink()
        assert skill.read_bytes(), "the copy is empty"


def test_running_it_twice_reports_current_and_not_installed(tmp_path):
    """Idempotent, and it says which of the three things happened.

    "It was already right" and "it was wrong and now is right" are the two facts
    a person runs this to learn, so collapsing them into one success would answer
    a question nobody asked.
    """
    into = tmp_path / "agent"
    _drive(["skills", "install", "--into", str(into)])

    code, envelope = _drive(["skills", "install", "--into", str(into)])

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert summary["current"] == len(skills_cli.shipped_names())
    assert summary["installed"] == 0
    assert summary["refreshed"] == 0
    assert all(check["status"] == "ok" for check in envelope["data"]["checks"])


def test_a_stale_stamp_warns_and_is_repaired_in_the_same_run(tmp_path):
    """"Drift warns", driven, and the repair is asserted rather than assumed.

    Warning without repairing would make a person act twice on one condition.
    Repairing without warning would hide that their agent had been reading an
    older build's instructions. Both happen, and the check that reports the
    refresh is the one that is not ``ok``.
    """
    into = tmp_path / "agent"
    _drive(["skills", "install", "--into", str(into)])
    name = skills_cli.shipped_names()[0]
    stamp = into / name / skills_cli.STAMP_NAME
    stamp.write_text('version = "0.0.0-from-an-older-build"\n')
    (into / name / "SKILL.md").write_text("what the older build said\n")

    code, envelope = _drive(["skills", "install", "--into", str(into)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["refreshed"] == 1
    drifted = [c for c in envelope["data"]["checks"] if c["key"] == f"skill.{name}"]
    assert drifted and drifted[0]["status"] == "info", drifted
    assert "different build" in drifted[0]["detail"]
    assert skills_cli.installed_version(into / name) == __version__
    assert (into / name / "SKILL.md").read_text() != "what the older build said\n"


def test_an_unstamped_copy_is_drift_rather_than_damage(tmp_path):
    """A copy somebody made by hand has no stamp, and overwriting it is the ask.

    Refusing here would make the verb unusable on exactly the directory a person
    is trying to bring under management.
    """
    into = tmp_path / "agent"
    name = skills_cli.shipped_names()[0]
    (into / name).mkdir(parents=True)
    (into / name / "SKILL.md").write_text("hand written\n")

    code, envelope = _drive(["skills", "install", "--into", str(into)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["refreshed"] == 1
    assert skills_cli.installed_version(into / name) == __version__


def test_a_file_this_build_no_longer_ships_disappears(tmp_path):
    """The reason the destination is replaced whole rather than copied over.

    A leftover file looks current to anything reading the directory, and an agent
    reading a skill this build withdrew is the failure the version stamp exists
    to make visible everywhere else.
    """
    into = tmp_path / "agent"
    _drive(["skills", "install", "--into", str(into)])
    name = skills_cli.shipped_names()[0]
    stale = into / name / "WITHDRAWN.md"
    stale.write_text("shipped by an older build and withdrawn since\n")

    _drive(["skills", "install", "--into", str(into)])

    assert not stale.exists(), "a withdrawn file survived a reinstall"


def test_the_default_target_is_composed_from_home_and_is_not_a_literal(monkeypatch, tmp_path):
    """R1 in the one place a home directory would legitimately be reached for.

    Asserted by MOVING home and watching the answer move with it, which is the
    only way to tell a composed path from a literal that happens to be right on
    the machine running the suite.
    """
    monkeypatch.setenv("HOME", str(tmp_path / "elsewhere"))
    assert skills_cli.default_target() == tmp_path / "elsewhere" / ".claude" / "skills"


def test_a_target_that_cannot_be_created_refuses_with_a_typed_cause(tmp_path):
    """A permission the account does not have is not a defect in this program.

    It carries its own reason and a remedy a person can act on, rather than an
    OSError arriving at the boundary with neither.
    """
    blocked = tmp_path / "not-a-directory"
    blocked.write_text("this is a file, so nothing can be created inside it\n")

    code, envelope = _drive(["skills", "install", "--into", str(blocked / "agent")])

    assert code != int(ExitCode.OK)
    assert code != int(ExitCode.USAGE)
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert envelope["cause"]["remediation"]["remedy"]


def test_every_shipped_skill_is_installed_and_the_set_is_walked_not_listed(tmp_path):
    """The install set is exactly what ships, derived on both sides.

    Compared against the packaged directory rather than against a name list, so a
    skill added beside the others is covered on the day it appears and a skill
    the verb silently skipped is a failure rather than a shorter report.
    """
    into = tmp_path / "agent"
    _drive(["skills", "install", "--into", str(into)])

    packaged = {entry.name for entry in skills_cli.packaged_root().iterdir() if entry.is_dir()}
    written = {d.name for d in into.iterdir() if d.is_dir()}
    assert written == packaged


def test_install_one_reports_which_of_the_three_things_happened(tmp_path):
    """The engine underneath, driven directly for the three answers in sequence."""
    into = tmp_path / "agent"
    name = skills_cli.shipped_names()[0]

    assert skills_cli.install_one(name, into) == "installed"
    assert skills_cli.install_one(name, into) == "current"
    (into / name / skills_cli.STAMP_NAME).write_text('version = "0.0.0"\n')
    assert skills_cli.install_one(name, into) == "refreshed"


def test_the_packaged_root_resolves_through_the_package(tmp_path):
    """Through importlib.resources, so a wheel install finds them too.

    Path arithmetic from ``__file__`` is a claim about the package being unpacked
    on a filesystem, which is true of every install this product currently sees
    and is not a property of installing a wheel.
    """
    del tmp_path
    root = skills_cli.packaged_root()
    assert root.is_dir()
    assert (root / skills_cli.shipped_names()[0] / "SKILL.md").is_file()


def test_a_skill_directory_with_no_stamp_reads_as_no_version(tmp_path):
    """The absent case answers None rather than raising or inventing a version."""
    assert skills_cli.installed_version(tmp_path / "nothing-here") is None
    (tmp_path / "empty").mkdir()
    assert skills_cli.installed_version(tmp_path / "empty") is None


@pytest.mark.parametrize("flag", ["--into"])
def test_the_declared_flag_is_the_one_the_tests_drive(flag):
    """The verb's surface, pinned, so a rename shows up here rather than in a skill."""
    import sys  # noqa: PLC0415

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from tests.test_skills_lint import verb_table  # noqa: PLC0415

    assert flag in verb_table()[("skills", "install")]


def test_a_refusal_leaves_no_half_written_target(tmp_path):
    """Nothing is written before the target is known to be usable.

    A verb that created part of a tree and then refused would leave a directory
    an agent reads as a partial install.
    """
    blocked = tmp_path / "not-a-directory"
    blocked.write_text("a file\n")
    with pytest.raises(CratekitError):
        skills_cli.install_skills(
            type("Ctx", (), {"args": type("A", (), {"into": str(blocked / "agent")})()})()
        )
    assert blocked.is_file(), "the blocking file was replaced"
