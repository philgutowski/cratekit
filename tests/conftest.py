"""Suite-wide isolation. Every test runs against redirected state, always.

The autouse fixtures below redirect every root a test could reach into a
temporary directory and refuse every live service, process table and launchd
the product could reach. They are autouse rather than opt-in because opt-in
isolation protects only the tests that remembered: the source system twice had
its identification ledger and sync manifest written to the real installation by
tests that never meant to touch them.

* ``_isolate_state_roots`` redirects HOME and the XDG variables, from which
  platformdirs derives every path (KTD6), plus the CRATEKIT_* overrides.
* ``_isolate_keychain`` replaces the OS keychain with a dictionary (R4).
* ``_block_real_library_paths`` points the library root at a temp directory
  and disarms the mount precondition.
* ``_favourites_without_pink`` answers no pink rows (R-228).
* ``_no_host_process_table`` reads the host as a machine with no rekordbox
  (U232); a test marked ``real_process_table`` keeps the real table.
* The ``_no_live_*`` fixtures refuse each live service a test could reach.

A test that reaches real config, a real library, a real keychain, a real
rekordbox database or the host's real process table is a bug, not a slow test.

No fixture here takes ``monkeypatch``. Each holds its own ``pytest.MonkeyPatch``,
because ``monkeypatch`` is shared by every fixture and the test body, and one
``undo()`` in a body once put the test back on the real machine (R-658, see
``docs/solutions/workflow-issues/``).

The ordering is load bearing. These fixtures are autouse at the root, so they
are set up before the test's ``monkeypatch`` and torn down after it: a body
that patches an attribute already redirected here records the REDIRECTED value,
puts it back first, and then this file puts the real one back. Requesting
``monkeypatch`` here would invert that and leave the process pointing at a
deleted temp tree.
"""

from __future__ import annotations

import gc
import importlib
import importlib.util
import traceback

import pytest

from tests import _host_processes

#: A context manager, so an exception before the ``yield`` still undoes the patch.
_own_patch = pytest.MonkeyPatch.context

#: Whether each dotted name exists, found once per process (U312).
_PRESENT: dict[str, bool] = {}


def _module_if_present(dotted: str):
    """Import ``dotted`` only if it exists, else None: a no-op until its module lands."""
    present = _PRESENT.get(dotted)
    if present is None:
        try:
            present = importlib.util.find_spec(dotted) is not None
        except ModuleNotFoundError:
            present = False
        _PRESENT[dotted] = present
    return importlib.import_module(dotted) if present else None


@pytest.fixture(autouse=True)
def _isolate_state_roots(tmp_path_factory):
    """Redirect installation-scoped state to a temp tree for every test.

    The CRATEKIT_* overrides are set too, so the explicit override path is
    exercised as well as the derived one.
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
        # U206: a stale override would put the ISRC cache outside this tree.
        monkeypatch.delenv("CRATEKIT_ISRC_CACHE_DIR", raising=False)
        # U278: the provider gate never follows CRATEKIT_STATE_DIR.
        monkeypatch.setenv("CRATEKIT_PROVIDER_GATE_DIR", str(root / "state" / "cratekit"))

        # The config module may cache its directories at import, so re-point them.
        config = _module_if_present("cratekit.core.config")
        if config is not None:
            for attr, path in (
                ("CONFIG_DIR", root / "config" / "cratekit"),
                ("STATE_DIR", root / "state" / "cratekit"),
            ):
                if hasattr(config, attr):
                    monkeypatch.setattr(config, attr, path)

            # R-926: under pytest the config writer refuses any path outside
            # the base temp, which holds these roots and every tmp_path.
            monkeypatch.setattr(
                config, "_TEST_WRITE_ROOT", tmp_path_factory.getbasetemp()
            )

        yield root


@pytest.fixture(autouse=True)
def _isolate_keychain():
    """Swap the OS keychain for an in-memory dictionary.

    Replacing keyring's three module functions does not depend on its backend
    protocol. Without it a credential test on macOS pops a real dialog, and a
    headless run hangs rather than fails.
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
    """Refuse the live provider client and catalogue transport (U62, U205).

    The outbound account and its logged in session are held for the process,
    so they are dropped on both sides of every test (U63, U261).
    """
    from cratekit.acquire import provider_session

    def refused():
        raise AssertionError(
            "a test reached the live provider client; set "
            "provider_session.CLIENT_FACTORY to a fake"
        )

    from cratekit.modules.outbound import account

    account.forget()
    def refused_transport():
        raise AssertionError(
            "a test reached the live catalogue transport; set "
            "provider_session.CATALOGUE_TRANSPORT_FACTORY to a fake"
        )

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(provider_session, "CLIENT_FACTORY", refused)
        monkeypatch.setattr(provider_session, "CATALOGUE_TRANSPORT_FACTORY", refused_transport)
        yield
    account.forget()


@pytest.fixture(autouse=True)
def _no_paid_recognition():
    """Refuse the live ACRCloud transport (U57); a test injects its own."""
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
    """Refuse the shipped mix fetcher (U104); a test sets ``fetch.fetcher``."""
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
    """Refuse the shipped Bandcamp transport (U176).

    The process caches of signed links and library views are dropped on both
    sides, so one test's listing cannot answer the next test's worker.
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
    """Refuse the general catalogue's live lookup (R-796).

    The shared lookup is one per process, so it is replaced for each test and
    a refusal one test's lookup remembered never answers the next. A file with
    no ISRC still gets ``no-isrc``, which makes no request. A test that wants
    an answer replaces ``published.for_lookup``.
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
def _no_live_discogs():
    """Fail any test that reaches the live Discogs API through the shipped getter (U283).

    The shipped fetch folds a transport failure into an unreachable answer
    that setup stores, so a raised refusal alone would pass. The address is
    recorded and the test failed at teardown; other hosts pass through.
    """
    from cratekit.tagging import searchers

    reached: list[str] = []
    shipped = searchers._requests_get

    def guarded(url, *, headers, timeout):
        if url.startswith(searchers.DISCOGS_API):
            reached.append(url.split("?", 1)[0])
            raise ConnectionError("a test reached the live Discogs API")
        return shipped(url, headers=headers, timeout=timeout)

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(searchers, "_requests_get", guarded)
        yield
    if reached:
        pytest.fail(
            f"a test reached the live Discogs API, {reached}; hand the step or the "
            f"asker a fake fetch"
        )


@pytest.fixture(autouse=True)
def _no_live_cyanite():
    """Refuse the Cyanite trial's shipped send, a paid upload (U245)."""
    from cratekit.tagging import cyanite

    def refused(request):
        raise AssertionError(
            f"a test reached the shipped Cyanite send, {request.method} "
            f"{request.url}; hand the run a recorded send"
        )

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(cyanite, "_requests_send", refused)
        yield


@pytest.fixture(autouse=True)
def _forget_cover_memory():
    """Start and end every test with no remembered picture, fetch or run (U260, U281).

    A shared fetch built while one test replaced the HTTP getter would carry
    that getter into every later test in the worker.
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
    """Start and end every test with the library index reader remembering nothing (U249)."""
    from cratekit.acquire import match

    match.reset_cache()
    yield
    match.reset_cache()


@pytest.fixture(autouse=True)
def _block_real_library_paths(request, tmp_path_factory):
    """Point the library root at a temp directory and disarm the mount check.

    The root gets its own temp directory, never inside ``tmp_path``, so a test
    that walks its own tree never finds it; moving it beside the state roots
    moves where the filesystem places every test's directory (the U326 entry in
    ``docs/solutions/`` says what that cost). The preflight tests are excluded
    by exact module name, since a substring would exempt any future file
    containing it.
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

        # The backup's identity proof (#893) reads the real volume through the
        # same gate, so it answers "proven" here; its own tests take it back.
        backup = _module_if_present("cratekit.modules.tools.backup")
        if backup is not None and hasattr(backup, "_not_the_recorded_volume"):
            monkeypatch.setattr(backup, "_not_the_recorded_volume", lambda *a, **k: "")

        yield library

@pytest.fixture(autouse=True)
def _favourites_without_pink(request):
    """Default the favourites colour read to no pink rows (R-228) unless ``real_pink_read``."""
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


#: The cyclic collector's thresholds while the suite runs (U326), against the
#: interpreter's ``(700, 10, 10)``. A worker's heap grows to about 760,000
#: tracked objects, and at the defaults the collector took 50 of 270 seconds
#: over an eighth of the suite; at these it took 18 to 20. Nothing reads the
#: collector and reference counting is untouched. ``pytest_unconfigure`` puts
#: the interpreter's own back, for a run made in process by a test.
COLLECTOR_THRESHOLDS = (50_000, 20, 20)

#: The thresholds this process had before ``pytest_configure`` set the ones above.
_thresholds_before: list[tuple[int, int, int]] = []


def pytest_configure(config):
    _thresholds_before.append(gc.get_threshold())
    gc.set_threshold(*COLLECTOR_THRESHOLDS)
    config.addinivalue_line(
        "markers",
        f"{REAL_PROCESS_TABLE}: keep the host's real process table, which every "
        "other test reads as a machine with no rekordbox (U232)",
    )


def pytest_unconfigure(config):
    if _thresholds_before:
        gc.set_threshold(*_thresholds_before.pop())


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

    The v0.13.0 cut was refused because two tests read a Mac's real table with
    rekordbox open. ``core.processes._platform`` answers an empty table and
    pyrekordbox's ``utils.get_process_id`` answers no process. psutil's own
    ``process_iter`` and ``pids`` are a tripwire: refused AND recorded, and
    failed at teardown, since the careful scan turns any exception into a
    refusal of its own. A test faking rekordbox patches either seam on its own
    ``monkeypatch``, which is set up after this and wins.
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
    """rekordbox and rekordboxAgent on the host at psutil, beneath the tripwire (U232)."""
    with _own_patch() as monkeypatch:
        _host_processes.install(monkeypatch)
        yield _host_processes.OPEN


@pytest.fixture(autouse=True)
def _no_live_launchd():
    """Refuse launchctl in every test, and read the platform as one without it (U295).

    The refusal fails the test even when a verb's own path swallowed it, and
    the platform reads as Linux, so every verb refuses before launchd unless a
    test names the Mac and stands launchd in itself.
    """
    from cratekit.cli import schedule

    reached: list[str] = []

    def refused(*args):
        reached.append(" ".join(args))
        raise AssertionError(
            f"a test reached launchctl {' '.join(args)}; set schedule.launchctl to a fake"
        )

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(schedule, "launchctl", refused)
        monkeypatch.setattr(schedule, "platform", lambda: "linux")
        yield reached
    if reached:
        pytest.fail(
            f"a test reached launchctl: {reached}; set schedule.launchctl to a fake",
            pytrace=False,
        )
