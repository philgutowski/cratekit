"""The verb that installs the shipped operator skills.

The lint suite asks whether the skills are correct; this asks whether a person
can get them. Nothing below names a real volume, person or machine (D1).
"""

from __future__ import annotations

import pytest

from cratekit import __version__
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.skills import cli as skills_cli
from tests._sync_builders import exited
from tests.cli_drive import drive


def _install(into) -> tuple[int, dict]:
    """The REAL dispatcher installing into ``into``: the status and the validated envelope."""
    return drive(["skills", "install", "--into", str(into)])


@pytest.fixture
def installed(tmp_path):
    """One clean install: its status, its envelope and its target."""
    into = tmp_path / "agent"
    code, envelope = _install(into)
    return code, envelope, into


@pytest.fixture
def reinstalled(tmp_path):
    """A clean install of the tests' own, and the first shipped skill's name."""
    into = tmp_path / "agent"
    _install(into)
    return into, skills_cli.shipped_names()[0]


def test_a_clean_directory_gets_every_shipped_skill_with_a_stamp(installed):
    """The count is DERIVED, never pinned (P3)."""
    code, envelope, into = installed
    assert code == int(ExitCode.OK), envelope
    shipped = skills_cli.shipped_names()
    assert shipped, "the package ships no skills, so this proves nothing"
    assert envelope["data"]["summary"]["installed"] == len(shipped)
    for name in shipped:
        assert (into / name / "SKILL.md").is_file()
        assert skills_cli.installed_version(into / name) == __version__


def test_the_copies_are_copies_and_not_symlinks(installed):
    """A link into the installed package breaks when the package moves."""
    into = installed[2]
    for name in skills_cli.shipped_names():
        skill = into / name / "SKILL.md"
        assert not skill.is_symlink(), f"{name} was linked rather than copied"
        assert not (into / name).is_symlink()
        assert skill.read_bytes(), "the copy is empty"


def test_every_shipped_skill_is_installed_and_the_set_is_walked_not_listed(installed):
    """Compared against the packaged directory, so a skipped skill fails."""
    into = installed[2]
    packaged = {entry.name for entry in skills_cli.packaged_root().iterdir() if entry.is_dir()}
    written = {d.name for d in into.iterdir() if d.is_dir()}
    assert written == packaged


def test_running_it_twice_reports_current_and_not_installed(reinstalled):
    """Idempotent, and it says which of the three things happened."""
    into, _ = reinstalled
    envelope = exited(_install(into))
    summary = envelope["data"]["summary"]
    assert summary["current"] == len(skills_cli.shipped_names())
    assert summary["installed"] == 0
    assert summary["refreshed"] == 0
    assert all(check["status"] == "ok" for check in envelope["data"]["checks"])


def test_a_stale_stamp_warns_and_is_repaired_in_the_same_run(reinstalled):
    """Drift warns, as the one check that is not ``ok``, and is repaired."""
    into, name = reinstalled
    (into / name / skills_cli.STAMP_NAME).write_text('version = "0.0.0-from-an-older-build"\n')
    (into / name / "SKILL.md").write_text("what the older build said\n")

    envelope = exited(_install(into))
    assert envelope["data"]["summary"]["refreshed"] == 1
    drifted = [c for c in envelope["data"]["checks"] if c["key"] == f"skill.{name}"]
    assert drifted and drifted[0]["status"] == "info", drifted
    assert "different build" in drifted[0]["detail"]
    assert skills_cli.installed_version(into / name) == __version__
    assert (into / name / "SKILL.md").read_text() != "what the older build said\n"


def test_an_unstamped_copy_is_drift_rather_than_damage(tmp_path):
    """A hand made copy has no stamp, and overwriting it is what was asked."""
    into = tmp_path / "agent"
    name = skills_cli.shipped_names()[0]
    (into / name).mkdir(parents=True)
    (into / name / "SKILL.md").write_text("hand written\n")

    envelope = exited(_install(into))
    assert envelope["data"]["summary"]["refreshed"] == 1
    assert skills_cli.installed_version(into / name) == __version__


def test_a_file_a_previous_install_wrote_and_this_build_withdrew_disappears(reinstalled):
    """A file the PREVIOUS STAMP names, and this build no longer ships, goes."""
    into, name = reinstalled
    withdrawn = into / name / "WITHDRAWN.md"
    withdrawn.write_text("shipped by an older build\n")
    stamp = 'version = "0.0.0"\nskill = "x"\nfiles = ["SKILL.md", "WITHDRAWN.md"]\n'
    (into / name / skills_cli.STAMP_NAME).write_text(stamp)

    _install(into)

    assert not withdrawn.exists(), "a withdrawn file survived a refresh"
    assert (into / name / "SKILL.md").is_file()


def test_a_file_the_product_never_wrote_survives_a_refresh(reinstalled):
    """A person's own file beside a skill is not this verb's to delete."""
    into, name = reinstalled
    mine = into / name / "MY-NOTES.md"
    mine.write_text("notes I keep beside the skill\n")
    stamp = 'version = "0.0.0"\nskill = "x"\nfiles = ["SKILL.md"]\n'
    (into / name / skills_cli.STAMP_NAME).write_text(stamp)

    code, envelope = _install(into)

    assert envelope["data"]["summary"]["refreshed"] == 1, envelope
    assert mine.read_text() == "notes I keep beside the skill\n"


def test_an_up_to_date_install_writes_nothing_at_all(reinstalled):
    """Measured by modification time, since rewriting the same bytes is a write."""
    into, name = reinstalled
    mine = into / name / "MY-NOTES.md"
    mine.write_text("untouched\n")
    before = {path.name: path.stat().st_mtime_ns for path in (into / name).iterdir()}

    code, envelope = _install(into)

    assert envelope["data"]["summary"]["current"] == len(skills_cli.shipped_names())
    after = {path.name: path.stat().st_mtime_ns for path in (into / name).iterdir()}
    assert after == before, "an up to date install rewrote files it had no reason to"
    assert mine.exists()


def test_the_default_target_is_composed_from_home_and_is_not_a_literal(monkeypatch, tmp_path):
    """R1: moving home moves the answer, which a literal would not."""
    monkeypatch.setenv("HOME", str(tmp_path / "elsewhere"))
    assert skills_cli.default_target() == tmp_path / "elsewhere" / ".claude" / "skills"


def test_a_target_that_cannot_be_created_refuses_with_a_typed_cause(tmp_path):
    """A missing permission carries its own reason and a remedy."""
    blocked = tmp_path / "not-a-directory"
    blocked.write_text("this is a file, so nothing can be created inside it\n")

    code, envelope = _install(blocked / "agent")

    assert code != int(ExitCode.OK)
    assert code != int(ExitCode.USAGE)
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert envelope["cause"]["remediation"]["remedy"]


def test_install_one_reports_which_of_the_three_things_happened(tmp_path):
    """The engine underneath, driven directly for the three answers in sequence."""
    into = tmp_path / "agent"
    name = skills_cli.shipped_names()[0]

    assert skills_cli.install_one(name, into) == "installed"
    assert skills_cli.install_one(name, into) == "current"
    (into / name / skills_cli.STAMP_NAME).write_text('version = "0.0.0"\n')
    assert skills_cli.install_one(name, into) == "refreshed"


def test_the_packaged_root_resolves_through_the_package():
    """Through importlib.resources, so a wheel install finds them too."""
    root = skills_cli.packaged_root()
    assert root.is_dir()
    assert (root / skills_cli.shipped_names()[0] / "SKILL.md").is_file()


def test_a_skill_directory_with_no_stamp_reads_as_no_version(tmp_path):
    """The absent case answers None rather than raising or inventing a version."""
    assert skills_cli.installed_version(tmp_path / "nothing-here") is None
    (tmp_path / "empty").mkdir()
    assert skills_cli.installed_version(tmp_path / "empty") is None


def test_the_declared_flag_is_the_one_the_tests_drive():
    """``--into`` on the REAL assembled parser, so a rename shows up here."""
    from cratekit.cli import build_parser  # noqa: PLC0415

    with pytest.raises(SystemExit) as exit_code:
        build_parser().parse_args(["skills", "install", "--into", "/tmp/somewhere", "--help"])
    assert exit_code.value.code in (0, None), "--into is not accepted by crate skills install"


def test_a_refusal_leaves_no_half_written_target(tmp_path):
    """Nothing is written before the target is known to be usable."""
    blocked = tmp_path / "not-a-directory"
    blocked.write_text("a file\n")
    with pytest.raises(CratekitError):
        skills_cli.install_skills(
            type("Ctx", (), {"args": type("A", (), {"into": str(blocked / "agent")})()})()
        )
    assert blocked.is_file(), "the blocking file was replaced"
