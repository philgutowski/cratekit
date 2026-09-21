"""R-395: the printed install command installs where ``crate`` actually runs.

The command used to be a bare ``pip install 'cratekit[analysis]'``. Under pipx,
which is how the README installs Cratekit, a bare pip runs against whichever
Python the shell finds first, so the extra landed where ``crate`` never reads it
and the same refusal came back. These pin the two environment shapes and the
one source every surface reads.
"""

from __future__ import annotations

import json
import shlex
import sys

import pytest

from cratekit.cli import registry, render
from cratekit.modules import extras


def _pipx_prefix(tmp_path, package_or_url):
    prefix = tmp_path / "venvs" / "cratekit"
    prefix.mkdir(parents=True)
    body = {"main_package": {"package_or_url": package_or_url}}
    (prefix / "pipx_metadata.json").write_text(json.dumps(body), encoding="utf-8")
    return prefix


def test_a_plain_virtual_environment_gets_pip_run_by_its_own_interpreter(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    monkeypatch.setattr(sys, "executable", "/opt/venv/bin/python")
    assert extras.install_command("analysis") == (
        "/opt/venv/bin/python -m pip install 'cratekit[analysis]'"
    )


def test_a_pipx_environment_gets_pipx_against_the_recorded_clone(tmp_path, monkeypatch):
    clone = tmp_path / "cratekit"
    clone.mkdir()
    monkeypatch.setattr(sys, "prefix", str(_pipx_prefix(tmp_path, str(clone))))
    assert extras.install_command("analysis") == shlex.join(
        ["pipx", "install", "--force", f"{clone}[analysis]"]
    )


def test_a_pipx_force_install_keeps_the_extras_already_chosen(tmp_path, monkeypatch):
    """``--force`` reinstalls from exactly the spec given.

    A command naming only the missing extra would drop the one already there,
    and the next verb would refuse for that one instead.
    """
    clone = tmp_path / "cratekit"
    clone.mkdir()
    prefix = _pipx_prefix(tmp_path, f"{clone}[analysis]")
    monkeypatch.setattr(sys, "prefix", str(prefix))
    assert extras.install_command("vocals") == shlex.join(
        ["pipx", "install", "--force", f"{clone}[analysis,vocals]"]
    )
    assert extras.install_command("analysis") == shlex.join(
        ["pipx", "install", "--force", f"{clone}[analysis]"]
    )


@pytest.mark.parametrize(
    "metadata",
    [
        "{not json",
        json.dumps({"main_package": {}}),
        json.dumps({"main_package": {"package_or_url": "/no/such/clone[vocals]"}}),
        json.dumps({"main_package": {"package_or_url": "git+https://example.invalid/c.git"}}),
    ],
)
def test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form(
    tmp_path, monkeypatch, metadata
):
    """Still pipx, never pip: the file's presence decides the environment."""
    prefix = tmp_path / "venv"
    prefix.mkdir()
    (prefix / "pipx_metadata.json").write_text(metadata, encoding="utf-8")
    monkeypatch.setattr(sys, "prefix", str(prefix))
    assert extras.install_command("analysis").startswith(
        "pipx install --force '.[analysis"
    )


def test_the_parser_stub_and_the_workers_read_one_source(tmp_path, monkeypatch):
    clone = tmp_path / "cratekit"
    clone.mkdir()
    monkeypatch.setattr(sys, "prefix", str(_pipx_prefix(tmp_path, str(clone))))
    for verb, slug in (("analyze.run", "analysis"), ("analyze.vocals", "vocals")):
        assert render.install_command(registry.entry(verb)) == extras.install_command(slug)
        assert render.install_command(registry.entry(verb)).startswith("pipx install")
