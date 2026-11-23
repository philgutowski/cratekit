"""R-926: under pytest, a state writer refuses a path outside the test root.

On 2026-10-08 a probe run from outside ``tests/`` wrote a pytest library into
the real ``config.toml``: the redirecting conftest never loaded. The guard reads
no environment variable; it asks whether pytest is loaded and whether the
resolved target sits under the root the isolation registered.

Removing the isolation is simulated by clearing ``config._TEST_WRITE_ROOT`` with
the redirected environment left in place, so a refusal can only come from the
guard. The configuration is held to the test root alone; ``atomic_write_bytes``
and ``exclusive_lock`` also accept the system temporary directory.
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
from tests.test_config_update import library as library  # noqa: PLC0414

#: A path no machine running this suite has, outside every temporary root.
OUTSIDE = Path(os.sep, "cratekit-r926-outside-every-test-root")


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


#: The state writers besides the configuration. U254's synced append never
#: creates a file, so a refusal from ``os.open`` would be a FileNotFoundError
#: and say nothing about the guard.
STATE_WRITERS = pytest.mark.parametrize(
    "write",
    [lambda target: config.atomic_write_bytes(b"{}", target),
     lambda target: config.append_durable_bytes(b"{}\n", target)],
    ids=["atomic-write", "durable-append"],
)


@STATE_WRITERS
def test_a_state_write_outside_every_temporary_folder_is_refused(unisolated, write):
    target = OUTSIDE / "ledger.json"
    with pytest.raises(config.WriteOutsideTestRoot) as refused:
        write(target)
    assert str(target) in str(refused.value)
    assert "no test root is registered" in str(refused.value)
    assert not OUTSIDE.exists()


@STATE_WRITERS
def test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place(write):
    with pytest.raises(config.WriteOutsideTestRoot) as refused:
        write(OUTSIDE / "ledger.json")
    assert "outside the test root" in str(refused.value)
    assert not OUTSIDE.exists()


def test_an_append_inside_the_root_adds_to_the_file_and_never_creates_one(tmp_path):
    target = tmp_path / "ledger.json"
    with pytest.raises(FileNotFoundError):
        config.append_durable_bytes(b"one\n", target)
    assert not target.exists()
    config.atomic_write_bytes(b"zero\n", target)
    config.append_durable_bytes(b"one\n", target)
    config.append_durable_bytes(b"", target)
    config.append_durable_bytes(b"two\n", target)
    assert target.read_bytes() == b"zero\none\ntwo\n"


def test_a_lock_outside_every_temporary_folder_is_refused(unisolated):
    lock = config.exclusive_lock(OUTSIDE / "session.lock")
    with pytest.raises(config.WriteOutsideTestRoot), lock:
        pass
    assert not OUTSIDE.exists()


def test_a_scratch_write_in_the_system_temporary_folder_lands_without_a_root(unisolated):
    """Shipped code's own mkdtemp folders, and a test child's locks, still work."""
    scratch = Path(tempfile.mkdtemp(prefix="cratekit-r926-"))
    target = scratch / "token.json"
    config.atomic_write_bytes(b"{}", target)
    with config.exclusive_lock(scratch / "token.lock"):
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
    """The guard is inert for the shipped tool, which never imports pytest: the
    child saves with no root registered, so a check that ran anyway fails it."""
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
