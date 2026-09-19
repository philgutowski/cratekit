"""Suite-wide isolation. Every test runs against redirected state, always.

Three autouse fixtures, ported in spirit from the source system's three, redirect
every root a test could reach into a temporary directory. They are autouse rather
than opt-in for one reason: opt-in isolation protects the tests that remembered,
and the tests that forget are exactly the ones that corrupt real state. The
source system learned this twice. Its identification ledger and its sync manifest
both got written to the real installation by tests that were never meant to touch
them, because isolation was something a test had to ask for.

What each fixture covers:

1. ``_isolate_state_roots`` moves the platform's own notion of "the user" into a
   temp directory. Config resolution goes through platformdirs (KTD6), and
   platformdirs derives every path it returns from HOME and the XDG variables. So
   redirecting those redirects installation-scoped config, state, cache, and data
   at once, on every platform, without this file needing to know what the config
   module will eventually call its own environment variables. That matters here:
   the config module lands in U2, after this file.

2. ``_isolate_keychain`` replaces the OS keychain with an in-memory dictionary.
   Secrets live in the keychain by design (R4), which means a test that reads or
   writes a credential would otherwise prompt for a real login, or worse, succeed
   and mutate it. The stub is installed whether or not any test asks for it.

3. ``_block_real_library_paths`` points the library root at a temp directory and
   neutralizes the mount precondition. The library root is the one path that
   names real music files and a real rekordbox database, so it gets its own
   fixture rather than riding along with the state roots.

A test that reaches real config, a real library, a real keychain, or a real
rekordbox database is a bug, not a slow test.
"""

from __future__ import annotations

import importlib
import importlib.util

import pytest


def _module_if_present(dotted: str):
    """Import ``dotted`` only if it exists, else return None.

    U6 lands before nearly everything it isolates. Rather than guess at module
    names that do not exist yet and fail on import, each redirection below is
    conditional: it is a no-op until the module lands, and it starts biting the
    moment it does, with no edit to this file required.
    """
    try:
        if importlib.util.find_spec(dotted) is None:
            return None
    except ModuleNotFoundError:
        return None
    return importlib.import_module(dotted)


@pytest.fixture(autouse=True)
def _isolate_state_roots(tmp_path_factory, monkeypatch):
    """Redirect installation-scoped state to a temp tree for every test.

    HOME and the XDG variables are the inputs platformdirs uses on every platform
    it supports, so setting them here covers the config directory, the state
    directory, the cache directory, and anything else resolved the same way,
    including code that has not been written yet.

    The CRATEKIT_* overrides are set alongside them belt-and-braces, so an
    explicit override path is exercised as well as the derived one.
    """
    root = tmp_path_factory.mktemp("state_roots")

    home = root / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))  # Windows equivalent
    for var, sub in (
        ("XDG_CONFIG_HOME", "config"),
        ("XDG_STATE_HOME", "state"),
        ("XDG_DATA_HOME", "data"),
        ("XDG_CACHE_HOME", "cache"),
    ):
        path = root / sub
        path.mkdir()
        monkeypatch.setenv(var, str(path))

    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(root / "config" / "cratekit"))
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(root / "state" / "cratekit"))

    # Once config lands (U2) it may cache its resolved directories at import time.
    # Re-point the module attributes too, so a cached value cannot outlive the
    # environment redirection above.
    config = _module_if_present("cratekit.core.config")
    if config is not None:
        for attr, path in (
            ("CONFIG_DIR", root / "config" / "cratekit"),
            ("STATE_DIR", root / "state" / "cratekit"),
        ):
            if hasattr(config, attr):
                monkeypatch.setattr(config, attr, path)

    return root


@pytest.fixture(autouse=True)
def _isolate_keychain(monkeypatch):
    """Swap the OS keychain for an in-memory dictionary.

    keyring resolves a platform backend at import time. Replacing the two
    module-level functions the rest of the codebase calls is enough, and is far
    less fragile than installing a backend object, because it does not depend on
    keyring's internal backend protocol staying still across versions.

    Without this a credential test on macOS pops a real authorization dialog,
    which in a headless run means the suite hangs rather than fails.
    """
    try:
        import keyring
    except ImportError:  # pragma: no cover - keyring is a core dependency
        return {}

    store: dict[tuple[str, str], str] = {}

    def _set(service: str, username: str, password: str) -> None:
        store[(service, username)] = password

    def _get(service: str, username: str):
        return store.get((service, username))

    def _delete(service: str, username: str) -> None:
        store.pop((service, username), None)

    monkeypatch.setattr(keyring, "set_password", _set)
    monkeypatch.setattr(keyring, "get_password", _get)
    monkeypatch.setattr(keyring, "delete_password", _delete)
    return store


@pytest.fixture(autouse=True)
def _no_live_provider_client(monkeypatch):
    """Refuse the live provider client in every test, structurally.

    U62 bound the label catalogue, so a test that records a provider session in
    the isolated keychain and asks ``catalogue.resolve`` for a catalogue would
    otherwise log a real client in against the real provider with the battery
    green. A test that wants a client replaces ``CLIENT_FACTORY`` itself.
    """
    from cratekit.acquire import provider_session

    def refused():
        raise AssertionError(
            "a test reached the live provider client; set "
            "provider_session.CLIENT_FACTORY to a fake"
        )

    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", refused)

    # U63: the outbound seam holds the account it opened for the life of the
    # process, so an adapter one test opened over its fake client would answer
    # the next test's resolve. Dropped on both sides of every test.
    from cratekit.modules.outbound import account

    account.forget()
    yield
    account.forget()


@pytest.fixture(autouse=True)
def _no_paid_recognition(monkeypatch):
    """Refuse the live recognition transport in every test, structurally.

    Until U57 the suite could not spend by construction: ``recognize.identify``
    refused whenever no identifier was injected. Now the seam binds the
    ACRCloud identifier, whose transport is looked up on the module at call
    time, so a test that records both recognition keys in the isolated
    keychain and has ffmpeg on PATH would post real chunks to a real host with
    the battery green. This puts the guarantee back where it was: the shipped
    transport is replaced with one that fails the test, and a test that wants
    a transport injects its own, which every one of them already does.
    """
    from cratekit.intake import acrcloud

    def refused(request):
        raise AssertionError(
            "a test reached the live recognition transport; inject a fake one"
        )

    monkeypatch.setattr(acrcloud, "http_transport", refused)


@pytest.fixture(autouse=True)
def _no_real_mix_download(monkeypatch):
    """Refuse the shipped mix fetcher in every test, structurally.

    U104 taught ``intake set`` and ``intake identify`` to fetch a mix URL, and
    the seam is looked up on the module at call time. A machine with ``yt-dlp``
    installed would otherwise download a real upload from a test that passed
    an address and forgot to inject a fetcher, with the battery green. A test
    that wants a download replaces ``fetch.fetcher`` itself.
    """
    from cratekit.intake import fetch

    def refused():
        raise AssertionError(
            "a test reached the shipped mix fetcher; set fetch.fetcher to a fake"
        )

    monkeypatch.setattr(fetch, "fetcher", refused)


@pytest.fixture(autouse=True)
def _block_real_library_paths(request, tmp_path_factory, monkeypatch):
    """Point the library root at a temp directory and disarm the mount check.

    Two separate concerns, one fixture, because they are the same risk:

    * The library root names real audio files and the real rekordbox database.
      Any test that resolves it must resolve it into a temp tree.
    * The mount precondition samples real on-disk paths, so tests built on
      synthetic locations would fail on the precondition rather than on the thing
      they are testing. The precondition's OWN behaviour is covered directly by
      the preflight tests, which is why they are excluded here by exact module
      name rather than by a substring: a substring exclusion silently exempts any
      future file whose name happens to contain it, and that class of over-broad
      exclusion is precisely what the portability guard was widened to remove.

    The redirected root gets its OWN temp directory rather than a subdirectory of
    the test's ``tmp_path``. That is not tidiness. A test that builds a synthetic
    tree in ``tmp_path`` and then walks it would otherwise find this fixture's
    directory sitting in its input, and the resulting failure points at the test
    rather than at the fixture that caused it.
    """
    library = tmp_path_factory.mktemp("library")
    monkeypatch.setenv("CRATEKIT_LIBRARY_ROOT", str(library))

    config = _module_if_present("cratekit.core.config")
    if config is not None and hasattr(config, "LIBRARY_ROOT"):
        monkeypatch.setattr(config, "LIBRARY_ROOT", library)

    if request.node.path.name == "test_preflight.py":
        return library

    preflight = _module_if_present("cratekit.core.preflight")
    if preflight is not None and hasattr(preflight, "assert_library_mounted"):
        monkeypatch.setattr(preflight, "assert_library_mounted", lambda *a, **k: None)

    return library
