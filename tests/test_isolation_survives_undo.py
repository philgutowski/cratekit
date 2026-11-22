"""The suite's isolation outlives a test body's ``monkeypatch.undo()`` (R-658).

``monkeypatch`` is one instance shared by the test body and every fixture that
requests it, and ``undo()`` reverts all of it, so isolation recorded on it was
once undone and a test overwrote the live configuration. The isolation holds
its own instance; these tests undo the body's patches and then reach for
everything it redirects.

EVERY CHECK RESOLVES BEFORE IT WRITES, so a regression fails here without
doing the damage it describes. The last test bans a body ``undo()`` on the
shared instance everywhere in ``tests/`` but here, since modules keep guards
of their own on it.
"""

from __future__ import annotations

import ast
import os
from pathlib import Path

import keyring
import platformdirs

from cratekit.acquire import provider_session
from cratekit.core import config, preflight
from cratekit.intake import acrcloud, fetch


def _starting_roots() -> tuple[Path, ...]:
    """Where installation state resolves with the environment the process has."""
    roots = [
        Path(platformdirs.user_config_dir("cratekit")),
        Path(platformdirs.user_state_dir("cratekit")),
    ]
    roots += [
        Path(os.environ[name])
        for name in (config.ENV_CONFIG_DIR, config.ENV_STATE_DIR)
        if os.environ.get(name)
    ]
    return tuple(roots)


# Read at import, before any fixture ran: what the PROCESS started with, which
# an ``undo()`` used to restore.
_STARTING_ROOTS = _starting_roots()
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
    """The exact 2026-09-20 shape: undo, resolve the config location, write.
    The state directory rides along: the secrets presence index lives there."""
    _undo_the_body(monkeypatch)

    targets = (
        Path(platformdirs.user_config_dir("cratekit")) / "config.toml",
        config.config_path(),
        Path(platformdirs.user_state_dir("cratekit")) / "r658-probe",
        config.installation_state_dir() / "r658-probe",
    )
    for path in targets:
        assert _inside(path, _isolate_state_roots), (
            f"{path} resolves outside this test's temp root after an undo"
        )
        reached = [root for root in _STARTING_ROOTS if _inside(path, root)]
        assert not reached, f"{path} resolves under {reached}, where the process started"

    for path in targets:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("a fixture configuration", encoding="utf-8")
    assert all(path.is_file() for path in targets)


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
    """The body's instance is set up after the isolation's, so the HOME it
    records as original, and an undo puts back, is the redirected one."""
    redirected = {name: os.environ[name] for name in ("HOME", config.ENV_CONFIG_DIR)}
    for value in redirected.values():
        assert _inside(Path(value), _isolate_state_roots)

    monkeypatch.setenv("HOME", str(_isolate_state_roots / "elsewhere"))
    monkeypatch.delenv(config.ENV_CONFIG_DIR)
    monkeypatch.undo()

    assert {name: os.environ.get(name) for name in redirected} == redirected


def _body_undoes(tree: ast.AST) -> list[int]:
    """Line numbers of every ``monkeypatch.undo()`` in ``tree``."""
    return [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "undo"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "monkeypatch"
    ]


def test_no_test_undoes_the_shared_monkeypatch():
    """Reverse one patch with a ``pytest.MonkeyPatch.context()`` around it.

    Exempt by exact path, this file only. A scoped instance's own ``undo()``
    reverts only what it recorded, so the ban is on the shared fixture's name.
    Only a file whose text holds ``undo`` is parsed, since no call without it
    is one.
    """
    tests = Path(__file__).parent
    here = Path(__file__).resolve()
    texts = {path: path.read_text(encoding="utf-8") for path in sorted(tests.rglob("*.py"))}
    found = [
        f"{path.relative_to(tests)}:{line}"
        for path, text in texts.items()
        if path.resolve() != here and "undo" in text
        for line in _body_undoes(ast.parse(text))
    ]
    assert found == [], (
        "monkeypatch.undo() reverts every patch on the shared instance, the "
        f"module's own guards with it; scope the one patch instead: {found}"
    )


def test_the_ban_sees_an_undo():
    """The walk answers an empty list for a clean tree, so it is shown one."""
    assert _body_undoes(ast.parse("def t(monkeypatch):\n    monkeypatch.undo()\n")) == [2]
    assert _body_undoes(ast.parse("zone.undo()\n")) == []
