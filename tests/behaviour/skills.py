"""The skills package's scenario: what `crate skills install` copies (U311).

The verb copies the operator skills the package ships into an agent's skills
directory, with a stamp naming the build. It is driven into a clean directory,
again over the copies it left, over a copy whose stamp an older build wrote
and which names a file this build withdrew, beside a file of a person's own,
and once into its default directory, which is composed from the home
directory the scenario's own isolation moved into its directory. The capture
holds every copy by its bytes.
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
