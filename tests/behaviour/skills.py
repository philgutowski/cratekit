"""The skills package's scenario: what `crate skills install` copies (U311).

Every copy, into each kind of directory, is held by its bytes.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.core.exit_codes import ExitCode
from cratekit.skills import cli as skills_cli

OK = int(ExitCode.OK)


def test_the_shipped_skills_are_installed_and_refreshed(stage, tmp_path):
    into = tmp_path / "agent"

    fresh = stage.json("skills", "install", "--into", into)
    assert fresh.code == OK, fresh.stdout
    assert fresh.envelope["data"]["summary"]["installed"] == len(skills_cli.shipped_names())
    current = stage.crate("skills", "install", "--into", into)
    assert current.code == OK, current.stderr

    name = skills_cli.shipped_names()[0]
    (into / name / "WITHDRAWN.md").write_text("shipped by an older build\n")
    (into / name / "MY-NOTES.md").write_text("notes I keep beside the skill\n")
    (into / name / skills_cli.STAMP_NAME).write_text(
        'version = "0.0.0"\nskill = "x"\nfiles = ["SKILL.md", "WITHDRAWN.md"]\n'
    )
    (into / name / "SKILL.md").write_text("what the older build said\n")
    refreshed = stage.json("skills", "install", "--into", into)
    assert refreshed.code == OK, refreshed.stdout
    assert refreshed.envelope["data"]["summary"]["refreshed"] == 1
    assert stage.crate("skills", "install", "--into", into).code == OK


def test_the_default_directory_is_under_home(stage, tmp_path):
    assert Path.home().is_relative_to(tmp_path), "home is outside the scenario's directory"
    assert stage.crate("skills", "install").code == OK
    assert stage.json("skills", "install").code == OK
