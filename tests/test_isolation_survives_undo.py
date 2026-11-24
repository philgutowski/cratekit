"""The suite's isolation outlives a test body's ``monkeypatch.undo()`` (R-658), which once
reverted it so a test overwrote the live configuration; a body ``undo()`` of the shared
instance is banned anywhere else in ``tests/``.
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path

import keyring
import platformdirs

from cratekit.acquire import provider_session
from cratekit.core import config, preflight
from cratekit.intake import acrcloud, fetch

# Read at import, before any fixture: what the PROCESS started with, which ``undo()`` restored.
_STARTING_ROOTS = (
    Path(platformdirs.user_config_dir("cratekit")),
    Path(platformdirs.user_state_dir("cratekit")),
    *(Path(os.environ[name]) for name in (config.ENV_CONFIG_DIR, config.ENV_STATE_DIR)
      if os.environ.get(name)),
)
_REAL_SET_PASSWORD = keyring.set_password
_REAL_CLIENT_FACTORY = provider_session.CLIENT_FACTORY
_REAL_TRANSPORT = acrcloud.http_transport
_REAL_FETCHER = fetch.fetcher
_REAL_MOUNT_CHECK = preflight.assert_library_mounted
# ``monkeypatch.undo`` in source, only blanks, brackets, continuations and comments between.
_CALL = re.compile(r"\bmonkeypatch(?:[\s)\\]|#[^\n]*)*\.(?:[\s\\]|#[^\n]*)*undo\b")


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def test_every_redirect_survives_an_undo_of_the_body_s_own_patch(
        _isolate_state_roots, _isolate_keychain, _block_real_library_paths, monkeypatch):
    """The 2026-09-20 shape: undo, resolve the config location, write."""
    monkeypatch.setenv("CRATEKIT_R658_PROBE", "the body's own patch")
    monkeypatch.undo()
    assert "CRATEKIT_R658_PROBE" not in os.environ, "the undo did not run"
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
    assert keyring.set_password is not _REAL_SET_PASSWORD, "the real keychain is back after an undo"
    assert os.environ[config.ENV_LIBRARY_ROOT] == str(_block_real_library_paths)
    assert preflight.assert_library_mounted is not _REAL_MOUNT_CHECK
    assert provider_session.CLIENT_FACTORY is not _REAL_CLIENT_FACTORY
    assert acrcloud.http_transport is not _REAL_TRANSPORT
    assert fetch.fetcher is not _REAL_FETCHER
    for path in targets:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("a fixture configuration", encoding="utf-8")
    assert all(path.is_file() for path in targets)
    keyring.set_password("cratekit-r658", "probe", "not a real secret")
    assert _isolate_keychain[("cratekit-r658", "probe")] == "not a real secret"


def test_a_body_patch_of_a_redirected_value_undoes_to_the_redirect(
        _isolate_state_roots, monkeypatch):
    """The body's instance is set up after the isolation's, so an undo restores the redirect."""
    redirected = {name: os.environ[name] for name in ("HOME", config.ENV_CONFIG_DIR)}
    for value in redirected.values():
        assert _inside(Path(value), _isolate_state_roots)
    monkeypatch.setenv("HOME", str(_isolate_state_roots / "elsewhere"))
    monkeypatch.delenv(config.ENV_CONFIG_DIR)
    monkeypatch.undo()
    assert {name: os.environ.get(name) for name in redirected} == redirected


def _body_undoes(tree: ast.AST) -> list[int]:
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    undo = [node for node in calls if getattr(node.func, "attr", None) == "undo"]
    owners = [(node.lineno, node.func.value) for node in undo]
    return [line for line, who in owners if isinstance(who, ast.Name) and who.id == "monkeypatch"]


def test_no_test_undoes_the_shared_monkeypatch():
    """A scoped ``MonkeyPatch.context()`` may undo; this file alone may undo the shared one."""
    assert _body_undoes(ast.parse("def t(monkeypatch):\n    monkeypatch.undo()\n")) == [2]
    assert _body_undoes(ast.parse("zone.undo()\n")) == []
    tests = Path(__file__).parent
    here = Path(__file__).resolve()
    texts = {path: path.read_text(encoding="utf-8") for path in sorted(tests.rglob("*.py"))}
    found = [
        f"{path.relative_to(tests)}:{line}"
        for path, text in texts.items()
        if path.resolve() != here and "undo" in text and _CALL.search(text)
        for line in _body_undoes(ast.parse(text))
    ]
    assert found == [], (
        "monkeypatch.undo() reverts every patch on the shared instance, the "
        f"module's own guards with it; scope the one patch instead: {found}"
    )
