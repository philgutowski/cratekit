"""The suite's isolation outlives a test body's ``monkeypatch.undo()`` (R-658).

``monkeypatch`` is one instance shared by the test body and every fixture that
requests it, and ``undo()`` reverts all of it. While the conftest's isolation
was recorded on that instance, one ``undo()`` put a test back on the real
machine, and on 2026-09-20 a test in that state overwrote the live
configuration. The isolation now holds its own instance, so these tests undo
the body's patches and then reach for everything the isolation redirects.

EVERY CHECK RESOLVES BEFORE IT WRITES. If the isolation is broken, the path a
write would take is the real one, so each test asserts where the path points
first and writes only once that has passed. A regression fails here without
doing the damage it is describing.
"""

from __future__ import annotations

import os
from pathlib import Path

import keyring
import platformdirs

from cratekit.acquire import provider_session
from cratekit.core import config, preflight
from cratekit.intake import acrcloud, fetch

# Read at import, before any fixture has run, so these are what the PROCESS
# started with, which is exactly what an ``undo()`` used to restore.
_STARTING_HOME = Path(os.environ.get("HOME", "/"))
_STARTING_CONFIG_OVERRIDE = os.environ.get(config.ENV_CONFIG_DIR)
_REAL_SET_PASSWORD = keyring.set_password
_REAL_CLIENT_FACTORY = provider_session.CLIENT_FACTORY
_REAL_TRANSPORT = acrcloud.http_transport
_REAL_FETCHER = fetch.fetcher
_REAL_MOUNT_CHECK = preflight.assert_library_mounted


def _undo_the_body(monkeypatch) -> None:
    """Patch something of the test's own and undo it, the shape R-658 names."""
    monkeypatch.setenv("CRATEKIT_R658_PROBE", "the body's own patch")
    monkeypatch.undo()
    assert "CRATEKIT_R658_PROBE" not in os.environ, "the undo did not run"


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def test_a_write_to_the_platformdirs_config_after_an_undo_lands_in_the_temp_root(
    _isolate_state_roots, monkeypatch
):
    """The exact 2026-09-20 shape: undo, resolve the config location, write."""
    _undo_the_body(monkeypatch)

    resolved = Path(platformdirs.user_config_dir("cratekit"))
    product = config.config_path()
    for path in (resolved, product):
        assert _inside(path, _isolate_state_roots), (
            f"{path} resolves outside this test's temp root after an undo"
        )
        assert not _inside(path, _STARTING_HOME), (
            f"{path} resolves under the home this process started with"
        )
        if _STARTING_CONFIG_OVERRIDE:
            assert not _inside(path, Path(_STARTING_CONFIG_OVERRIDE))

    resolved.mkdir(parents=True, exist_ok=True)
    (resolved / "config.toml").write_text("a fixture configuration", encoding="utf-8")
    product.parent.mkdir(parents=True, exist_ok=True)
    product.write_text("a fixture configuration", encoding="utf-8")
    assert (resolved / "config.toml").is_file() and product.is_file()


def test_the_keychain_is_still_the_stub_after_an_undo(_isolate_keychain, monkeypatch):
    _undo_the_body(monkeypatch)

    assert keyring.set_password is not _REAL_SET_PASSWORD, (
        "the real keychain is back after an undo"
    )
    keyring.set_password("cratekit-r658", "probe", "not a real secret")
    assert _isolate_keychain[("cratekit-r658", "probe")] == "not a real secret"


def test_the_library_root_and_the_refusals_survive_an_undo(
    _block_real_library_paths, monkeypatch
):
    _undo_the_body(monkeypatch)

    assert os.environ[config.ENV_LIBRARY_ROOT] == str(_block_real_library_paths)
    assert preflight.assert_library_mounted is not _REAL_MOUNT_CHECK
    assert provider_session.CLIENT_FACTORY is not _REAL_CLIENT_FACTORY
    assert acrcloud.http_transport is not _REAL_TRANSPORT
    assert fetch.fetcher is not _REAL_FETCHER


def test_a_body_patch_of_a_redirected_value_undoes_to_the_redirect(
    _isolate_state_roots, monkeypatch
):
    """The ordering the conftest's docstring calls load bearing.

    The body's instance is set up after the isolation's, so what it records as
    HOME's original is the redirected HOME, and that is what an undo puts back.
    """
    redirected = {name: os.environ[name] for name in ("HOME", config.ENV_CONFIG_DIR)}
    for value in redirected.values():
        assert _inside(Path(value), _isolate_state_roots)

    monkeypatch.setenv("HOME", str(_isolate_state_roots / "elsewhere"))
    monkeypatch.delenv(config.ENV_CONFIG_DIR)
    monkeypatch.undo()

    assert {name: os.environ.get(name) for name in redirected} == redirected
