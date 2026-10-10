"""R-926: under pytest, a state writer refuses a path outside the test root.

On 2026-10-08 a probe test run from a folder outside ``tests/`` wrote a pytest
library into the real ``config.toml``. The conftest that redirects HOME, the
XDG variables and ``CRATEKIT_CONFIG_DIR`` never loaded for it, so the
environment said "the real machine" and the writer believed it. The guard these
tests pin reads no environment variable: it asks whether pytest is loaded and
whether the resolved target sits under the root the isolation registered.

Removing the isolation is simulated by clearing ``config._TEST_WRITE_ROOT``,
which is the one thing the conftest's absence leaves behind that the guard
reads. The redirected environment stays in place, so a refusal here can only
come from the guard and never from a write that happened to land somewhere
harmless.

The configuration document is held to the test root alone. The two primitives
every other state writer uses, ``atomic_write_bytes`` and ``_exclusive_lock``,
also accept the system temporary directory, where shipped code keeps scratch
files of its own, and nothing else.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import tomli_w

from cratekit.core import config
from tests.test_config_update import document_for

#: A path no machine running this suite has, outside every temporary root.
OUTSIDE = Path(os.sep, "cratekit-r926-outside-every-test-root")


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def unisolated(monkeypatch):
    """The state a probe outside ``tests/`` runs in: pytest loaded, no root."""
    monkeypatch.setattr(config, "_TEST_WRITE_ROOT", None)


def test_with_the_isolation_removed_a_save_is_refused_and_names_the_path(
    library, unisolated
):
    target = config.config_path()
    with pytest.raises(config.WriteOutsideTestRoot) as refused:
        config.save(config.from_dict(document_for(library)))
    assert str(target) in str(refused.value)
    assert "no test root is registered" in str(refused.value)
    # Refused before the directory, the lock file or the document existed.
    assert not target.parent.exists()


def test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing(
    library, unisolated
):
    target = config.config_path()
    revised = []
    with pytest.raises(config.WriteOutsideTestRoot) as refused:
        config.update(lambda document: revised.append(document) or document_for(library))
    assert str(target) in str(refused.value)
    assert revised == []
    assert not target.parent.exists()


def test_with_the_isolation_removed_a_migration_write_back_is_refused(
    library, tmp_path, unisolated
):
    path = tmp_path / "config.toml"
    before = tomli_w.dumps(document_for(library)).encode("utf-8")
    path.write_bytes(before)

    def to_two(data: dict) -> dict:
        return {**data, "schema_version": 2}

    with pytest.raises(config.WriteOutsideTestRoot) as refused:
        config.load_from_path(path, current=2, migrations={1: to_two})
    assert str(path) in str(refused.value)
    assert path.read_bytes() == before
    assert not path.with_name(path.name + ".v1.bak").exists()


def test_with_the_isolation_a_save_lands_in_the_temporary_root(
    library, tmp_path_factory
):
    target = config.save(config.from_dict(document_for(library)))
    assert target == config.config_path()
    assert target.is_file()
    root = tmp_path_factory.getbasetemp().resolve()
    assert target.resolve().is_relative_to(root)
    assert config._TEST_WRITE_ROOT == tmp_path_factory.getbasetemp()


def test_a_write_to_a_tmp_path_lands_as_it_always_has(library, tmp_path):
    target = tmp_path / "elsewhere" / "config.toml"
    assert config.save(config.from_dict(document_for(library)), target) == target
    assert target.is_file()


def test_a_path_outside_the_root_is_refused_with_the_isolation_in_place(library):
    target = OUTSIDE / "config.toml"
    with pytest.raises(config.WriteOutsideTestRoot) as refused:
        config.save(config.from_dict(document_for(library)), target)
    assert str(target) in str(refused.value)
    assert "outside the test root" in str(refused.value)
    assert not OUTSIDE.exists()


def test_a_link_inside_the_root_aimed_outside_it_is_refused(library, tmp_path):
    link = tmp_path / "looks-local"
    link.symlink_to(OUTSIDE, target_is_directory=True)
    with pytest.raises(config.WriteOutsideTestRoot):
        config.save(config.from_dict(document_for(library)), link / "config.toml")
    assert not OUTSIDE.exists()


def test_a_path_resolution_that_leaves_the_root_is_refused(library, monkeypatch):
    """What a mutant of ``config_path`` or a missed redirect looks like to a save."""
    monkeypatch.setattr(config, "config_path", lambda: OUTSIDE / "config.toml")
    with pytest.raises(config.WriteOutsideTestRoot):
        config.save(config.from_dict(document_for(library)))
    assert not OUTSIDE.exists()


def test_a_state_write_outside_every_temporary_folder_is_refused(unisolated):
    target = OUTSIDE / "ledger.json"
    with pytest.raises(config.WriteOutsideTestRoot) as refused:
        config.atomic_write_bytes(b"{}", target)
    assert str(target) in str(refused.value)
    assert "no test root is registered" in str(refused.value)
    assert not OUTSIDE.exists()


def test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place():
    target = OUTSIDE / "ledger.json"
    with pytest.raises(config.WriteOutsideTestRoot) as refused:
        config.atomic_write_bytes(b"{}", target)
    assert "outside the test root" in str(refused.value)
    assert not OUTSIDE.exists()


def test_a_lock_outside_every_temporary_folder_is_refused(unisolated):
    lock = config._exclusive_lock(OUTSIDE / "session.lock")
    with pytest.raises(config.WriteOutsideTestRoot), lock:
        pass
    assert not OUTSIDE.exists()


def test_a_scratch_write_in_the_system_temporary_folder_lands_without_a_root(unisolated):
    """Shipped code's own mkdtemp folders, and a test child's locks, still work."""
    scratch = Path(tempfile.mkdtemp(prefix="cratekit-r926-"))
    target = scratch / "token.json"
    config.atomic_write_bytes(b"{}", target)
    with config._exclusive_lock(scratch / "token.lock"):
        pass
    assert target.read_bytes() == b"{}"
    for each in (target, scratch / "token.lock"):
        each.unlink()
    scratch.rmdir()


def test_the_configuration_is_not_allowed_the_system_temporary_folder(library):
    scratch = Path(tempfile.mkdtemp(prefix="cratekit-r926-"))
    try:
        with pytest.raises(config.WriteOutsideTestRoot):
            config.save(config.from_dict(document_for(library)), scratch / "config.toml")
        assert list(scratch.iterdir()) == []
    finally:
        scratch.rmdir()


def test_a_process_without_pytest_loaded_is_never_checked(library, tmp_path):
    """The guard is inert for the shipped tool, which never imports pytest.

    The child saves a real configuration with no root registered, so a check
    that ran anyway, in the guard or anywhere on the write path, fails it.
    """
    target = tmp_path / "shipped" / "config.toml"
    probe = (
        "import sys\n"
        "from pathlib import Path\n"
        "from cratekit.core import config\n"
        "assert 'pytest' not in sys.modules, sorted(m for m in sys.modules if 'pytest' in m)\n"
        "assert config._TEST_WRITE_ROOT is None\n"
        f"config._refuse_write_outside_test_root(Path({str(OUTSIDE / 'config.toml')!r}))\n"
        f"document = {document_for(library)!r}\n"
        f"config.save(config.from_dict(document), Path({str(target)!r}))\n"
        "print('unchecked')\n"
    )
    done = subprocess.run(
        [sys.executable, "-I", "-c", probe], capture_output=True, text=True, check=False
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "unchecked"
    assert target.is_file()
