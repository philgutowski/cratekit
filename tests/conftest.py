"""Suite-wide isolation. Every test runs against redirected state, always.

Autouse fixtures, the first five of them listed here. Three, ported in spirit
from the source system's three, redirect every root a test could reach into a
temporary directory. They are autouse rather
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

4. ``_favourites_without_pink`` makes ``favorites.cli.read_pink_track_ids``
   return no pink rows. R-228's favourites sweep opens a read only copy of the
   configured database for colour; almost every outbound drive has no library
   to open, and would refuse with the colour read's own cause. Tests that care
   about pink override the attribute on the test's own ``monkeypatch``.

5. ``_no_host_process_table`` reads the host as a machine with no rekordbox
   running (U232). Both routes to the process table, the careful scan's
   ``core.processes._platform`` and pyrekordbox's ``utils.get_process_id``,
   answer no process, and psutil's own enumeration beneath them fails the test
   that reaches it. A test marked ``real_process_table`` keeps the real table.

A test that reaches real config, a real library, a real keychain, a real
rekordbox database or the host's real process table is a bug, not a slow test.

None of these fixtures takes the ``monkeypatch`` fixture. Each holds its own
``pytest.MonkeyPatch`` for the life of the test, because ``monkeypatch`` is one
instance shared by every fixture that requests it and by the test body, and
``monkeypatch.undo()`` in a body reverts everything recorded on it. When the
isolation shared that instance, one ``undo()`` put the test back on the real
machine, and what it restored was whatever the PROCESS started with (R-658, and
see ``docs/solutions/workflow-issues/``). On its own instance the isolation
outlives any body's ``undo()``.

The ordering is load bearing. These fixtures are autouse at the root, so they
are set up before the test's ``monkeypatch`` and torn down after it. A body that
patches an attribute these fixtures already redirected therefore records the
REDIRECTED value as its original, puts it back first, and then this file puts
the real one back. Requesting ``monkeypatch`` here would invert that: the body's
teardown would run last and leave the process pointing at a deleted temp tree.
"""

from __future__ import annotations

import importlib
import importlib.util
import traceback

import pytest

from tests import _host_processes

#: The one call every fixture below makes to get an instance of its own. A
#: context manager rather than ``pytest.MonkeyPatch()`` so that an exception
#: anywhere between the patch and the ``yield`` still undoes what was patched.
_own_patch = pytest.MonkeyPatch.context


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
def _isolate_state_roots(tmp_path_factory):
    """Redirect installation-scoped state to a temp tree for every test.

    HOME and the XDG variables are the inputs platformdirs uses on every platform
    it supports, so setting them here covers the config directory, the state
    directory, the cache directory, and anything else resolved the same way,
    including code that has not been written yet.

    The CRATEKIT_* overrides are set alongside them belt-and-braces, so an
    explicit override path is exercised as well as the derived one.
    """
    root = tmp_path_factory.mktemp("state_roots")
    with _own_patch() as monkeypatch:
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
        # U206: an override a shell left set would put every test's ISRC cache
        # outside this tree, so it is cleared and the cache follows the state.
        monkeypatch.delenv("CRATEKIT_ISRC_CACHE_DIR", raising=False)
        # U278: the provider gate never follows CRATEKIT_STATE_DIR, so it is
        # pointed into this test's own state root by its own variable, and no
        # test reads or spends the real gate's hour.
        monkeypatch.setenv("CRATEKIT_PROVIDER_GATE_DIR", str(root / "state" / "cratekit"))

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

            # R-926: the config writer refuses, under pytest, any path outside
            # this root, whatever the environment says. The base temp holds
            # both this fixture's roots and every test's own tmp_path.
            monkeypatch.setattr(
                config, "_TEST_WRITE_ROOT", tmp_path_factory.getbasetemp()
            )

        yield root


@pytest.fixture(autouse=True)
def _isolate_keychain():
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
        yield {}
        return

    store: dict[tuple[str, str], str] = {}

    def _set(service: str, username: str, password: str) -> None:
        store[(service, username)] = password

    def _get(service: str, username: str):
        return store.get((service, username))

    def _delete(service: str, username: str) -> None:
        store.pop((service, username), None)

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(keyring, "set_password", _set)
        monkeypatch.setattr(keyring, "get_password", _get)
        monkeypatch.setattr(keyring, "delete_password", _delete)
        yield store


@pytest.fixture(autouse=True)
def _no_live_provider_client():
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

    # U63: the outbound seam holds the account it opened for the life of the
    # process, so an adapter one test opened over its fake client would answer
    # the next test's resolve. Dropped on both sides of every test. U261: the
    # logged in session both openers share is held for the process too, and
    # ``account.forget`` drops it with the adapter.
    from cratekit.modules.outbound import account

    account.forget()
    def refused_transport():
        raise AssertionError(
            "a test reached the live catalogue transport; set "
            "provider_session.CATALOGUE_TRANSPORT_FACTORY to a fake"
        )

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(provider_session, "CLIENT_FACTORY", refused)
        # U205: the app credentials' catalogue client sends through its own
        # transport, so a test that records the app's two values and opens an
        # account would otherwise reach the live catalogue with the battery
        # green. Refused the same way.
        monkeypatch.setattr(provider_session, "CATALOGUE_TRANSPORT_FACTORY", refused_transport)
        yield
    account.forget()


@pytest.fixture(autouse=True)
def _no_paid_recognition():
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

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(acrcloud, "http_transport", refused)
        yield


@pytest.fixture(autouse=True)
def _no_real_mix_download():
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

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(fetch, "fetcher", refused)
        yield


@pytest.fixture(autouse=True)
def _no_live_bandcamp():
    """Refuse the shipped Bandcamp transport in every test, structurally.

    U176 bound ``acquire bandcamp`` to a transport looked up on the module at
    call time, so a test that records a session in the isolated keychain and
    forgets to bind a fake would reach the real account with the battery green.
    The process level caches of signed links and library views are dropped on
    both sides, so one test's listing cannot answer the next test's worker.
    """
    from cratekit.acquire import bandcamp_cli

    def refused():
        raise AssertionError(
            "a test reached the shipped Bandcamp transport; set "
            "bandcamp_cli.transport to a fake"
        )

    bandcamp_cli.forget()
    with _own_patch() as monkeypatch:
        monkeypatch.setattr(bandcamp_cli, "transport", refused)
        yield
    bandcamp_cli.forget()


@pytest.fixture(autouse=True)
def _no_live_general_catalogue():
    """Refuse the general catalogue's live lookup in every test, structurally.

    R-796 bound a second network source into the tagging worker. Its lookup is
    one per process, held on ``published._shared`` and read at call time, so a
    test that binds only the searcher and tags a file carrying an ISRC would
    otherwise ask the real catalogue, with real sleeps, with the battery
    green. The shared lookup is replaced with one whose fetch fails the test,
    and dropped again afterwards so a refusal one test's lookup remembered
    does not answer the next test. A file with no ISRC still gets its honest
    ``no-isrc``, because that answer makes no request. A test that wants an
    answer replaces ``published.for_lookup`` itself.
    """
    from cratekit.tagging import published

    def refused(url):
        raise AssertionError(
            f"a test reached the live general catalogue, {url}; set "
            f"published.for_lookup to a lookup over a fake fetch"
        )

    guarded = published.genre_lookup(fetch=refused, sleep=lambda _seconds: None)
    with _own_patch() as monkeypatch:
        monkeypatch.setattr(published, "_shared", [guarded])
        yield


@pytest.fixture(autouse=True)
def _forget_cover_memory():
    """Start and end every test with no remembered picture and no shared fetch.

    U260 made the worker's image fetch one per process, remembering each
    address's bytes, and the encoder remember each picture it made. A shared
    fetch built while one test had replaced the HTTP getter would carry that
    getter into every later test in the worker, and a picture one test's fake
    host answered would answer the next test's address without a request.
    The run whose refusals are counted (U281) is forgotten on the same rule.
    """
    from cratekit.core import art
    from cratekit.tagging import searchers

    searchers.reset_images()
    searchers.reset_runs()
    art.reset_cache()
    yield
    searchers.reset_images()
    searchers.reset_runs()
    art.reset_cache()


@pytest.fixture(autouse=True)
def _forget_library_reads():
    """Start and end every test with the library index reader remembering nothing.

    U249 made the reader keep what each file's tags said for the life of the
    process, keyed on the path and the file's stat. Test paths are unique, so
    one test's library cannot answer another's, but a memory that outlives its
    test is a memory a later test's assertion about opens or reads can trip
    on, and it grows with every library the worker indexes.
    """
    from cratekit.acquire import match

    match.reset_cache()
    yield
    match.reset_cache()


@pytest.fixture(autouse=True)
def _block_real_library_paths(request, tmp_path_factory):
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
    with _own_patch() as monkeypatch:
        monkeypatch.setenv("CRATEKIT_LIBRARY_ROOT", str(library))

        config = _module_if_present("cratekit.core.config")
        if config is not None and hasattr(config, "LIBRARY_ROOT"):
            monkeypatch.setattr(config, "LIBRARY_ROOT", library)

        preflight = _module_if_present("cratekit.core.preflight")
        if (
            request.node.path.name != "test_preflight.py"
            and preflight is not None
            and hasattr(preflight, "assert_library_mounted")
        ):
            monkeypatch.setattr(preflight, "assert_library_mounted", lambda *a, **k: None)

        yield library

@pytest.fixture(autouse=True)
def _favourites_without_pink(request):
    """Default the favourites colour read to no pink rows (R-228).

    A test that wants pink rows, or a colour refusal, patches
    ``favorites.cli.read_pink_track_ids`` on its own ``monkeypatch``. This
    fixture uses its own MonkeyPatch instance for the reason the module
    docstring gives. A test marked ``real_pink_read`` keeps the real read, so
    the one function that opens the library is exercised somewhere.
    """
    favorites_cli = _module_if_present("cratekit.favorites.cli")
    if request.node.get_closest_marker("real_pink_read") is not None:
        yield
        return
    if favorites_cli is None or not hasattr(favorites_cli, "read_pink_track_ids"):
        yield
        return
    with _own_patch() as monkeypatch:
        monkeypatch.setattr(favorites_cli, "read_pink_track_ids", lambda cfg: ())
        yield


#: The marker a test carries to keep the host's real process table (U232).
REAL_PROCESS_TABLE = "real_process_table"


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        f"{REAL_PROCESS_TABLE}: keep the host's real process table, which every "
        "other test reads as a machine with no rekordbox (U232)",
    )


class _NoProcesses:
    """A process table with nothing on it, in the shape the scan reads psutil."""

    def __init__(self, psutil):
        self.NoSuchProcess = psutil.NoSuchProcess
        self.ZombieProcess = psutil.ZombieProcess
        self.AccessDenied = psutil.AccessDenied
        self.STATUS_ZOMBIE = psutil.STATUS_ZOMBIE

    def pids(self):
        return []

    def Process(self, pid):  # noqa: N802 - psutil's own name
        raise self.NoSuchProcess(pid)


@pytest.fixture(autouse=True)
def _no_host_process_table(request):
    """Read the host as a machine with no rekordbox on it, in every test (U232).

    The v0.13.0 cut was refused on a red Mac battery because rekordbox was open
    on the machine and two tests read the host's real process table: one
    exited 21 for a rekordbox it should never have seen, and the other exited 1
    at a commit pyrekordbox refused. Both routes to the table are answered here:

    * ``core.processes._platform``, the seam every careful scan reads
      (``running_processes``, ``running_process_names``, a lister left as
      ``None``), answers an empty table;
    * pyrekordbox's ``utils.get_process_id``, the walk behind
      ``get_rekordbox_pid``, ``get_rekordbox_agent_pid`` and the binding's own
      ``db6.database.get_rekordbox_pid`` at construction and commit, answers no
      process, exactly as pyrekordbox does on a clean machine.

    Under both, psutil's own enumeration, ``process_iter`` and ``pids``, is a
    tripwire: a call is refused AND recorded, and the test fails at teardown
    over anything recorded, since the careful scan turns every exception into
    a refusal of its own and a refusal alone would be swallowed. A test that
    fakes rekordbox running keeps faking it at either seam, on its own
    ``monkeypatch``, which is set up after this and so wins. A test marked
    ``real_process_table`` keeps the real table, so the real scan is driven
    somewhere.
    """
    if request.node.get_closest_marker(REAL_PROCESS_TABLE) is not None:
        yield
        return
    import psutil

    from cratekit.core import processes

    reached: list[str] = []

    def tripwire(name):
        def refused(*_args, **_kwargs):
            where = "".join(traceback.format_stack(limit=6)[:-1])
            reached.append(f"psutil.{name} was called from:\n{where}")
            raise AssertionError(
                f"a test reached the host's real process table through psutil.{name}; "
                f"fake it at core.processes._platform or pyrekordbox.utils.get_process_id, "
                f"or mark the test {REAL_PROCESS_TABLE}"
            )

        return refused

    def no_process(name, raise_exec=False):
        if raise_exec:
            # pyrekordbox's own words, which name rekordbox whatever was asked.
            raise RuntimeError("No process with name 'rekordbox' found!")
        return 0

    empty = _NoProcesses(psutil)
    with _own_patch() as monkeypatch:
        monkeypatch.setattr(psutil, "process_iter", tripwire("process_iter"))
        monkeypatch.setattr(psutil, "pids", tripwire("pids"))
        monkeypatch.setattr(processes, "_platform", lambda: empty)
        utils = _module_if_present("pyrekordbox.utils")
        if utils is not None:
            monkeypatch.setattr(utils, "get_process_id", no_process)
        yield
    if reached:
        pytest.fail(
            f"the test reached the host's real process table without the "
            f"{REAL_PROCESS_TABLE} marker:\n" + "\n".join(reached),
            pytrace=False,
        )


@pytest.fixture
def rekordbox_on_the_host():
    """rekordbox and rekordboxAgent running on the host, at psutil itself (U232).

    Beneath the stubs above, so a test under it proves the suite reads a Mac
    with rekordbox open the way it reads one without. Installed after the
    tripwire, so for this test psutil's enumeration answers the fake host.
    """
    with _own_patch() as monkeypatch:
        _host_processes.install(monkeypatch)
        yield _host_processes.OPEN
