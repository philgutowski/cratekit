"""The guarded rekordbox database writer: the chain of refusals that stands
between automation and an irreplaceable music library.

pyrekordbox supplies no version gating, no write-ahead-log handling and no
locking, so every property in this module is load-bearing and none of it can be
delegated upstream. The chain, in the order it fires, and what each link refuses:

1. **Three version pins.** The installed binding, the database's own schema
   version, and the installed rekordbox application. Any drift is a
   stop-and-revalidate event rather than a silent write, because a rekordbox
   update can rotate the database key or migrate the schema underneath a writer
   that was validated against neither.
2. **The two-process refusal**, covering the application AND its background
   agent, at open and again at commit. The agent is the one that gets missed: it
   holds the database handle and mutates the library through cloud sync with the
   application closed, which is exactly the window a long write runs in.
3. **The cloud-sync canary.** A concurrent writer we cannot see is a concurrent
   writer we cannot serialise against, so an active library sync refuses.
4. **A write-ahead-log-aware snapshot** with a symmetric restore, taken before
   any write and verified before anything commits behind it.
5. **The additive whitelist.** A session may CREATE rows only in named playlist
   and tag tables, may MODIFY only columns an enabled operation has REGISTERED,
   and may DELETE nothing at all, ever. That is R17 stated as a property of the
   database rather than as a code-review note: grid and analysis data is
   structurally unwritable, not merely untested.
6. **A cross-process write-session lock**, held from snapshot through smoke test.

WHAT CHANGED IN THE PORT, AND WHY EACH CHANGE IS A FIX RATHER THAN A DRIFT.

* **No import-time path constants.** The source froze four paths at import, so a
  configuration loaded afterwards changed the config module and nothing else.
  Every path here is a late-bound accessor reading resolved configuration.
* **The application pin is configuration, and an unset pin REFUSES** (S2). A pin
  the software copies from whatever happens to be installed refuses nothing,
  forever, which is the entire property the pin exists to provide.
* **The cloud canary has a real predicate.** The source's was an unconditional
  "not active" whose docstring is a falsification record; see
  :func:`cloud_sync_state` for the marker that was found, the three traps around
  it, and the incident that produced them.
* **The snapshot-protection scan works.** The source globbed a filename its own
  run-state store never writes, read a status key that does not exist, and
  compared against a terminal set missing one of the two real values, so nothing
  was ever protected. See :func:`default_protected_snapshot_paths`.
* **Pruning is not called from inside the snapshot.** The source pruned inside
  the write session, before the commit the snapshot protects. Pruning is now a
  separate step the caller places after its commit (R30).
* **The writable column set is registered, not maximal.** The source shipped a
  static union of every column any operation might ever want, so a slim install
  with no metadata operations still had four extra columns structurally
  writable. R14's "widened only as far as each feature requires" is implemented
  here rather than described.

LAYER: infrastructure. It may read configuration directly and may do input and
output. It carries remediation TOKENS and never the text a user types (D2).
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import sys
import tempfile
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass
from enum import StrEnum
from functools import partial
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.core import config, processes
from cratekit.core.cause import Cause, CratekitError, Scope, name_the_database, refuse
from cratekit.core.exit_codes import Remedy

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Refusals
#
# Two types, not one, because callers discriminate on them: a snapshot integrity
# probe swallows an unavailable database and must NOT swallow "the application is
# running", which is a different fact with a different fix.
#
# Both carry a structured cause (KTD25). A bare RuntimeError, which is what the
# source raised, forces every catcher to parse a message string, and a typed
# failure that collapses at any hop cannot be recovered downstream.
# ---------------------------------------------------------------------------


class RekordboxUnavailable(CratekitError):
    """The database cannot be opened, fails a canary or a guard, or a precondition refuses."""


class RekordboxRunning(CratekitError):
    """The rekordbox application or its background agent is running and a write was requested."""


def _cause(
    reason: str,
    message: str,
    *,
    remedy: Remedy | None = None,
    steps: Sequence[str] = (),
    scope: Scope = Scope.SESSION,
    detail: Mapping[str, Any] | None = None,
    inner: Cause | None = None,
) -> Cause:
    """Build one cause through the shared constructor, then hand back the cause.

    Routed through ``cause.refuse`` rather than constructing a ``Cause`` here so
    that the closed reason registry and the default-remediation lookup are
    applied in exactly one place. A raise site that builds its own cause is a
    raise site that can invent an undeclared slug.
    """
    return refuse(
        reason,
        message,
        remedy=remedy,
        steps=steps,
        scope=scope,
        detail=detail,
        inner=inner,
    ).cause


def _unavailable(reason: str, message: str, **kwargs: Any) -> RekordboxUnavailable:
    return RekordboxUnavailable(_cause(reason, message, **kwargs))


def _running(message: str, **kwargs: Any) -> RekordboxRunning:
    return RekordboxRunning(_cause("rekordbox-running", message, **kwargs))


# ---------------------------------------------------------------------------
# Configuration accessors, all late-bound
#
# Rule 1 of the configuration module is that nothing resolves at import. The
# source system bound its database path, its state root, its snapshot root and
# its lock path at import time in seventeen modules, so reloading configuration
# afterwards changed the configuration module and nothing else. There is no
# module-level path constant here to bind.
# ---------------------------------------------------------------------------

#: The environment variable pointing at a disposable database for the integration
#: suite. Named here so the accessor and the tests cannot disagree about it.
TEST_DB_ENV = "CRATEKIT_TEST_DB"

#: rekordbox's own legacy playlist file, which lives beside the database. It is
#: deliberately NOT a declared Cratekit state entry: it belongs to rekordbox, not
#: to us. It travels with the database through snapshot and restore because
#: pyrekordbox reconciles playlists against it on commit, and a restored database
#: sitting beside a newer copy of this file describes two different libraries.
MASTER_PLAYLIST_XML = "masterPlaylists6.xml"

def db_sidecar_suffixes() -> tuple[str, ...]:
    """Every suffix a SQLite database file travels with, DERIVED from the state schema.

    Derived rather than listed (P4): a companion list kept here would be the
    hand-maintained set the schema exists to abolish, and the cost of that drift
    is a captured database silently missing every transaction still in its log.

    A function rather than a constant because a module-level read of a
    configuration attribute is a snapshot, and this repository fails the build on
    those regardless of whether the particular value can move.
    """
    return tuple(sidecar.suffix for sidecar in config.SQLITE_SIDECARS)


def restored_sidecar_suffixes() -> tuple[str, ...]:
    """The subset a RESTORE writes back out of a snapshot.

    The asymmetry is declared in the schema and is the fix for a real regression:
    the shared-memory index is derived from the log, so restoring a stale one
    beside a fresh log hands SQLite two disagreeing views of one database.
    """
    return tuple(sidecar.suffix for sidecar in config.SQLITE_SIDECARS if sidecar.restored)


def _loaded_config(cfg: config.Config | None) -> config.Config | None:
    """The effective configuration, or None when this machine has none usable.

    None is not a pass. Every caller below treats an absent configuration as a
    machine that has recorded no decisions, which for the application pin means
    a refusal rather than a default (S2). Configuration failures are absorbed
    here rather than propagated because a writer refusal has to arrive in the
    writer's own vocabulary; the underlying configuration error is carried into
    the refusal's message so the result is still self-diagnosing.
    """
    if cfg is not None:
        return cfg
    try:
        return config.load()
    except config.ConfigError as exc:
        logger.debug("no usable configuration for the guarded writer: %s", exc)
        return None


def _pins(cfg: config.Config | None = None) -> config.RekordboxConfig:
    """The three pins as configured, falling back to the schema's own defaults.

    Pins 1 and 2 have defaults because they are facts about the SHIPPED build:
    the binding version is fixed by the lockfile and the schema version is fixed
    by what this build was validated against. Pin 3 has no default because it is
    a fact about the USER's machine, and inventing one would be the tautology S2
    forbids.
    """
    loaded = _loaded_config(cfg)
    return config.RekordboxConfig() if loaded is None else loaded.rekordbox


def pinned_pyrekordbox(cfg: config.Config | None = None) -> str:
    """The binding version this build is validated against."""
    return _pins(cfg).pinned_pyrekordbox


def pinned_db_version(cfg: config.Config | None = None) -> str:
    """The database schema version this build is validated against."""
    return _pins(cfg).pinned_db_version


def pinned_app_version(cfg: config.Config | None = None) -> str | None:
    """The recorded rekordbox application pin, or None when none was recorded.

    None is the state that refuses. The health check reads this accessor rather
    than a module constant, so there is exactly one answer to "what is pinned"
    and it cannot drift from what the writer enforces.
    """
    return _pins(cfg).pinned_app_version


def pin_validated_on(cfg: config.Config | None = None) -> str | None:
    """The date the recorded pin was confirmed against a real write.

    A pin without this is a number somebody typed. With it, a stale pin is
    visible as stale, which is what turns a recorded decision into a reviewable
    one.
    """
    return _pins(cfg).validated_on


def live_db_path(cfg: config.Config | None = None) -> Path:
    """The configured rekordbox database.

    No default, deliberately. A default library root is one person's disk baked
    into shipped code (R1), and an unconfigured library is a named refusal
    (AE10) that the configuration layer already owns with its own remedy token.
    """
    resolved = cfg if cfg is not None else config.load()
    return config.state_path("rekordbox_db", resolved)


def snapshot_root(cfg: config.Config | None = None) -> Path:
    """Where snapshots live: library-scoped, and outside the coupled set.

    Beside the library rather than per installation, so a second machine can
    restore the first machine's write. Outside the coupled set because a capture
    that included the snapshot store would nest every previous snapshot inside
    the new one.
    """
    resolved = cfg if cfg is not None else config.load()
    return config.state_path("snapshots", resolved)


def write_lock_path(cfg: config.Config | None = None) -> Path:
    """The cross-process write-session lock, beside the library.

    The source system put this under the installation root while the database it
    protects travelled with the library, so two installations held two different
    locks and both opened one database. It is also the file the old system has to
    be able to open during the migration overlap (R31), which only a path beside
    the library can provide.
    """
    resolved = cfg if cfg is not None else config.load()
    return config.state_path("write_lock", resolved)


#: The first bytes of an UNencrypted SQLite file. A rekordbox 6 database on a
#: real machine is encrypted and does not start with it, while every disposable
#: database this suite builds does.
SQLITE_HEADER = b"SQLite format 3"


def unlock_needed(path: Path | str) -> bool:
    """True when the file at ``path`` is encrypted, so the binding needs the key.

    ASKED OF THE BYTES RATHER THAN ASSUMED EITHER WAY, and both constant answers
    are wrong somewhere. ``unlock=True`` against a plain file fails on a database
    a test just built; ``unlock=False`` against a real library fails on every
    machine. ``open_db`` and ``integrity_ok`` ask it whenever their caller names
    no answer, and no caller in ``src`` names one (R-239): five verb sites used
    to pass ``unlock=False`` and failed at the open on every real library, which
    ``tests/test_rb_writer_db.py`` now refuses by walking the source.

    A file that cannot be read at all answers True, which is the conservative
    direction: the open below then fails with the database's own refusal rather
    than with a guess made here.

    THE HEADER IS THE ONLY THING READ, and its length comes from the constant
    rather than from a number typed beside it. A copy that read the whole file
    through ``read_bytes`` to look at fifteen characters lived in
    ``cratekit.deletion.cli`` until R-239 removed it.
    """
    try:
        with Path(path).open("rb") as handle:
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
    except OSError:
        return True


def close_db(db: Any) -> None:
    """Release a database handle COMPLETELY: the session AND the connection pool.

    THE BINDING'S OWN CLOSE IS NOT ENOUGH, and the gap is invisible until the one
    moment it is not. It closes the session and leaves the engine's pooled
    connection open, so the process still holds the database file, its
    write-ahead log, and its shared-memory index. Everything keeps working, which
    is why nobody notices.

    Then a restore replaces those three files underneath that live connection,
    and the next reader gets an input-output error against a database that is in
    fact perfectly intact. Observed directly against a disposable database while
    building this unit: the log stayed open and non-empty after the documented
    close, and the restored copy would not open afterwards.

    Tolerant of a handle that is already half closed, because the recovery path
    is exactly where a caller is unwinding from a failure and cannot be sure.
    """
    try:
        if getattr(db, "session", None) is not None:
            db.close()
    finally:
        engine = getattr(db, "engine", None)
        if engine is not None:
            engine.dispose()


def integration_db_path() -> Path | None:
    """A disposable database for the integration suite, or None when unset.

    Never falls back to the configured library. A test that can silently reach
    the live database is a test that eventually does.
    """
    raw = os.environ.get(TEST_DB_ENV)
    return Path(raw) if raw else None


# ---------------------------------------------------------------------------
# Pin 1: the installed binding
# ---------------------------------------------------------------------------


def assert_binding_version(cfg: config.Config | None = None) -> None:
    """Refuse unless the installed binding is exactly the validated version.

    Refuses: any version string that is not an exact match, including the
    placeholder used when the attribute is missing entirely.
    When: on every open, read or write.

    The strictest pin in the module and the only one with no escape. The binding
    is schema-coupled: it maps table shapes this build was validated against, and
    a mismatch is not a smaller risk on a read than on a write, because a read
    that mis-maps a column feeds a write that follows it.
    """
    import pyrekordbox

    pin = pinned_pyrekordbox(cfg)
    found = getattr(pyrekordbox, "__version__", "unknown")
    if found != pin:
        raise _unavailable(
            "pyrekordbox-pin-drift",
            f"the installed rekordbox binding is {found!r} and this build is "
            f"validated only against {pin!r}; re-validate against a snapshot "
            f"copy before moving the pin",
            detail={"installed": found, "pinned": pin},
        )


# ---------------------------------------------------------------------------
# Pin 2: the database's own schema version
# ---------------------------------------------------------------------------


def db_schema_version(db: Any) -> str | None:
    """The schema version the database stores, or None when it holds no property row.

    ONE READER, because there are now two callers. The pin below refuses on drift
    from it and the convergence fingerprint records it, and two spellings of
    "read the property table" is two chances to reach for a different column when
    the schema moves.

    IT DOES NOT CATCH, AND THAT IS THE DECISION IT MAKES. The raise on a table
    that cannot be read comes from the binding, not from here; what this function
    decides is to LET IT THROUGH rather than absorbing it into None. The two
    outcomes mean different things and only one of them is ordinary: no property
    row at all is a database this build has never seen written, while a table
    that will not answer is evidence of a migration. Both callers wrap it and
    both attach their own remedy, so wrapping here would replace two accurate
    answers with one generic one.
    """
    from pyrekordbox.db6 import tables

    row = db.session.query(tables.DjmdProperty).first()
    return None if row is None else str(row.DBVersion)


def assert_schema_version(
    db: Any, *, force: bool = False, cfg: config.Config | None = None
) -> None:
    """Refuse when the database's stored schema version drifts from the pin.

    Refuses: a stored version that is not an exact match, AND a property table
    that cannot be read at all, because an unreadable property table is itself
    evidence of a migrated schema.
    When: inside :func:`open_db`, on every open.

    FOLDED INTO THE OPEN CHAIN, WHICH THE SOURCE DID NOT DO. There it was a
    caller responsibility, and its three call sites disagreed: two threaded a
    force flag and the third called it only on a real run, so a rehearsal never
    saw a schema drift at all. A guard a caller can forget is a guard that is
    eventually forgotten.

    ``force`` is the deliberate re-validation path: it warns and continues. The
    flag that reaches it belongs to the command-line layer, which is why nothing
    here names one (D2).
    """
    pin = pinned_db_version(cfg)
    try:
        found = db_schema_version(db)
    except Exception as exc:  # noqa: BLE001 - an unreadable property table IS drift
        raise _unavailable(
            "db-schema-pin-drift",
            f"the database schema version could not be read, which is itself "
            f"evidence of a migrated schema: {exc}",
            detail={"pinned": pin},
        ) from exc
    if found == pin:
        return
    message = (
        f"the database schema version is {found!r} and this build is validated "
        f"against {pin!r}; a rekordbox upgrade has most likely migrated the "
        f"schema, so re-run the validation checklist against a snapshot copy "
        f"before moving the pin"
    )
    if force:
        logger.warning("proceeding past a schema pin refusal by explicit request: %s", message)
        return
    raise _unavailable("db-schema-pin-drift", message, detail={"found": found, "pinned": pin})


# ---------------------------------------------------------------------------
# Pin 3: the installed application
#
# Two platform probes behind one accessor. The source read a macOS bundle layout
# directly, which is an ImportError-free but silently macOS-only assumption (R1).
# ---------------------------------------------------------------------------

#: Test-only relocation of the application bundle. It RELOCATES an already
#: configured value and cannot supply one, which is the same rule the
#: configuration module applies to its own three overrides.
ENV_APP_PATH = "CRATEKIT_REKORDBOX_APP"


def _macos_app_version(app_path: Path) -> str | None:
    """The short version string from a macOS application bundle, or None."""
    import plistlib

    info = Path(app_path) / "Contents" / "Info.plist"
    try:
        with info.open("rb") as handle:
            data = plistlib.load(handle)
    except (OSError, ValueError):
        return None
    value = data.get("CFBundleShortVersionString")
    return str(value) if value else None


def _windows_app_version(app_path: Path) -> str | None:  # pragma: no cover - needs Windows
    """Placeholder probe for a Windows install.

    Returns None, which the caller already handles by warning and continuing, so
    a Windows install degrades exactly as an uninstalled application does today
    rather than crashing. That is the cheapest correct seam: adding Windows is
    filling in this function, not changing the decision above it.
    """
    return None


def _default_app_probe() -> Callable[[Path], str | None]:
    if sys.platform == "darwin":
        return _macos_app_version
    if sys.platform.startswith("win"):
        return _windows_app_version
    return lambda _path: None


def _candidate_app_paths(cfg: config.Config | None) -> list[Path]:
    """Where to look for the installed application, most specific first.

    Configuration is asked first so a user whose application lives outside the
    platform's usual place stops falling through to the degraded state described
    on :func:`assert_app_version`. The environment override exists for tests and
    is deliberately narrower than the source's, which was named for one person.
    """
    override = os.environ.get(ENV_APP_PATH)
    if override:
        return [Path(override)]
    configured = _pins(cfg).app_path
    if configured is not None:
        return [Path(configured)]
    if sys.platform == "darwin":
        import glob

        # Newest first: several major versions can be installed side by side, and
        # the one that opened the database most recently is the newest.
        return [
            Path(found)
            for found in sorted(glob.glob("/Applications/rekordbox*/rekordbox.app"), reverse=True)
        ]
    return []


def read_installed_app_version(*, cfg: config.Config | None = None) -> str | None:
    """The installed rekordbox application version, or None when it cannot be found.

    None on every failure path, never an exception. The caller treats "cannot
    find it" as its own outcome, and a probe that raised would make that
    indistinguishable from a drift, which has the opposite remediation.

    ``cfg`` is KEYWORD-ONLY so that a caller cannot pass an application path here
    by mistaking the first parameter for one, and so that the effective
    configuration is always threaded by name rather than by position. Passing it
    is what makes the pin comparison and this probe read ONE set of effective
    values (P2); see :func:`assert_app_version`.
    """
    probe = _default_app_probe()
    for candidate in _candidate_app_paths(cfg):
        version = probe(candidate)
        if version:
            return version
    return None


def assert_app_version(*, force: bool = False, cfg: config.Config | None = None) -> None:
    """Refuse when the installed application drifts from the recorded pin.

    Refuses: a located version that is not an EXACT match for the recorded pin,
    and a located version when no pin was ever recorded.
    Warns and continues: when the application cannot be located at all.
    When: inside :func:`open_db` on a write-intent open.

    WHY THE COMPARISON STAYS EXACT. The schema pin cannot see a point release: it
    held its value across a whole major version of rekordbox, and key extraction
    has broken across a point release before. Adding semantic-version tolerance,
    or comparing only major and minor, deletes the property this pin exists for.

    WHY AN UNRECORDED PIN REFUSES (S2). A pin the software copies from whatever
    is installed refuses nothing, forever. Setup may READ the installed version
    and PROPOSE it; recording it takes an explicit decision from the user, and
    the recorded decision carries the date it was validated on.

    WHY A MISSING APPLICATION ONLY WARNS. Refusing there would break every
    headless run for no safety gain: an application that is not installed cannot
    be holding the database open. Note what it costs, though, and note it out
    loud: on such a machine pin 3 is absent entirely and only the schema pin
    guards, which is a weaker guarantee than a machine where the probe resolves.
    The health check reports that as a named condition rather than leaving it as
    a line of transient log output, and the configured application path is the
    mechanism that makes the probe stop failing.

    WHY AN UNRECORDED PIN REFUSES IN THIS MODULE'S OWN VOCABULARY. The refusal
    itself belongs to the configuration layer, which owns the remedy token, but
    the TYPE it raises there is a plain configuration error carrying no reason
    slug and no exit code. Letting that escape gave one condition two identities:
    an unrecorded pin exited as a configuration precondition on a machine with a
    config file and as a version-pin refusal on a machine without one, which is
    exactly the collapse the cause type exists to prevent. It also escaped every
    ``except RekordboxUnavailable`` a caller writes, breaking the discrimination
    contract this module's header states. It is re-raised below with the
    configuration error carried underneath, so nothing is lost.

    WHY THE CONFIGURATION IS RESOLVED ONCE (P2). The pin is judged against a
    configuration and the probe searches the application path recorded in a
    configuration, so those had better be the same one. The probe used to be
    called with no argument and re-entered ``config.load()`` on its own, which
    under KTD9 is a different snapshot from the one a queued job was frozen
    against: a check and its consumer disagreeing about the same input.
    """
    loaded = _loaded_config(cfg)

    # Threaded, not re-derived. ``read_installed_app_version`` stays a SEAM a
    # test replaces with a one-line stand-in; what changed is that the value it
    # searches with now comes from the caller rather than from a second load.
    found = read_installed_app_version(cfg=loaded)
    if found is None:
        logger.warning(
            "the rekordbox application could not be located, so its version pin cannot "
            "be checked; only the database schema pin guards this session"
        )
        return

    if loaded is not None:
        # The refusal on an unset pin lives in the configuration layer, which
        # owns the remedy token for it, and is inert until a writer calls it.
        # This is that call.
        try:
            loaded.assert_rekordbox_pin_recorded()
        except config.ConfigError as exc:
            raise _unavailable(
                "app-version-pin-unrecorded",
                f"the installed rekordbox application is version {found!r} and no "
                f"pin has ever been recorded for this machine, so there is nothing "
                f"to validate the write against: {exc}",
                remedy=Remedy.RECORD_REKORDBOX_PIN,
                detail={
                    "installed": found,
                    "pinned": None,
                    "validated_on": pin_validated_on(loaded),
                    "config_error": type(exc).__name__,
                },
            ) from exc

    pin = pinned_app_version(loaded)
    if found == pin:
        return

    message = (
        f"the installed rekordbox application is version {found!r} and the "
        f"recorded pin is {pin!r}; a rekordbox update can rotate the database "
        f"key or migrate the schema, so re-validate against a snapshot copy and "
        f"record the new pin with the date it was confirmed"
    )
    if force:
        logger.warning(
            "proceeding past an application pin refusal by explicit request: %s", message
        )
        return

    detail = {"installed": found, "pinned": pin, "validated_on": pin_validated_on(loaded)}
    if not pin:
        # The other half of ONE identity. This branch is the machine with no
        # usable configuration at all; the branch above is the machine that has a
        # configuration and never recorded a pin. Same slug, same remedy token,
        # therefore the same exit code either way, which is the whole point:
        # "you never pinned one" must not become a different failure depending on
        # whether a config file happens to exist. Raised as its own reason rather
        # than folded into drift because "you pinned the wrong version" and "you
        # never pinned one" have the same class of code and different things to
        # do about them.
        raise _unavailable(
            "app-version-pin-unrecorded",
            message,
            remedy=Remedy.RECORD_REKORDBOX_PIN,
            detail=detail,
        )
    raise _unavailable("app-version-pin-drift", message, detail=detail)


# ---------------------------------------------------------------------------
# The two-process refusal
#
# Three sites, not two: open, commit, and restore. The plan names the first two.
# The third matters because restore replaces the database file underneath
# whatever has it open, and the unit that owns restore must not drop it.
# ---------------------------------------------------------------------------


def rekordbox_running() -> bool:
    """True when the rekordbox application itself is running."""
    from pyrekordbox.utils import get_rekordbox_pid

    return bool(get_rekordbox_pid())


def rekordbox_agent_running() -> bool:
    """True when the background agent is running.

    The agent holds the database handle and mutates the library through cloud
    sync even with the application closed, so a guard that checks only the
    application declares the coast clear during exactly the window a long write
    occupies.
    """
    from pyrekordbox.utils import get_rekordbox_agent_pid

    return bool(get_rekordbox_agent_pid())


#: The probe that answers for each name in the shared process list.
#:
#: Keyed by name rather than written as a sequence of ``if`` statements, so the
#: list itself lives in ``core.processes`` and this module holds only the
#: MECHANISM for asking. The writer asks pyrekordbox, which is the upstream
#: authority on finding rekordbox; the backup module asks the platform directly,
#: because it must work on a slim install with the rekordbox extra absent. Two
#: mechanisms, deliberately. One list, mandatorily.
#:
#: The value is the probe's ATTRIBUTE NAME, not the function object, and it is
#: resolved through the module at call time. Capturing the function here instead
#: would freeze it at import and silently defeat every test that fakes a running
#: rekordbox by patching these two seams, which is how the whole refuse-while-open
#: path is exercised without a real application on the machine.
_PROCESS_PROBES: Mapping[str, str] = MappingProxyType(
    {
        "rekordbox": "rekordbox_running",
        "rekordboxAgent": "rekordbox_agent_running",
    }
)


def rekordbox_processes_running() -> str:
    """The names of the rekordbox processes holding the database, comma joined.

    The empty string means both are clear. One predicate rather than three call
    sites each asking two questions, so a site cannot accidentally check half.

    Iterates the SHARED name list rather than a local copy. A name added there
    with no probe here raises instead of being skipped, because a process this
    guard cannot ask about is one it cannot declare clear. Refusing is the safe
    direction; silently not checking is how a guard passes a write it should
    have stopped.
    """
    running = []
    for name in processes.REKORDBOX_PROCESSES:
        probe_name = _PROCESS_PROBES.get(name)
        if probe_name is None:
            raise _running(
                f"{name!r} is listed as a process holding the database but this "
                f"module has no way to ask whether it is running, so no write "
                f"can be declared safe",
                detail={"process": name},
            )
        if globals()[probe_name]():
            running.append(name)
    return ", ".join(running)


def assert_rekordbox_closed(what: str) -> None:
    """Refuse while either rekordbox process is up.

    ``what`` names the operation being refused, so the message says which write
    was stopped rather than only that something was.
    """
    running = rekordbox_processes_running()
    if running:
        raise _running(
            f"{running} is running, so {what} is refused; quit the application "
            f"and let the background agent settle before retrying",
            detail={"processes": running},
        )


# ---------------------------------------------------------------------------
# The cloud-sync canary
# ---------------------------------------------------------------------------


class CloudSyncState(StrEnum):
    """What is known about rekordbox's Cloud Library Sync, as three answers.

    Three rather than a boolean because "cannot tell" has a different fix from
    "it is on", and collapsing them is how the previous predicate came to refuse
    every open while blaming the wrong thing.
    """

    OFF = "off"
    ON = "on"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class CloudSyncVerdict:
    """One reading of the cloud-sync state, with the evidence that produced it.

    ``reason`` quotes the actual key or row that decided the answer. The source's
    two refusal messages both named a marker that its own docstring recorded as
    false, which is how a three-day outage hid: the refusal was loud and pointed
    at the wrong thing.
    """

    state: CloudSyncState
    reason: str


#: The setting rekordbox writes when the user toggles Cloud Library Sync. Found
#: 2026-08-01 against a disposable copy of a real library, after every database
#: marker had been falsified.
LIBRARY_SYNC_SETTING = "EnableLibrarySync"

#: The application-data subdirectory holding that settings file. It is named for
#: major version SIX even under rekordbox 7, and there is no version-7 directory
#: at all, so deriving this name from the installed application version finds
#: nothing. Verified on a machine running rekordbox 7.
SETTINGS_APP_DIRNAME = "rekordbox6"

#: A real rekordbox application-data directory supplied to the canary's battery,
#: the settings-file sibling of :data:`TEST_DB_ENV`. Named here for the same
#: reason that one is: the reader and the tests cannot disagree about it.
#:
#: It is a SUBSTITUTION, not a skip. With it unset the battery parses a settings
#: file the test wrote itself, so every assertion runs on every machine; with it
#: set the SAME assertions run against a real file and the battery gets stronger.
#: A gate expressed as a skip would let the untested case look tested.
TEST_SETTINGS_ENV = "CRATEKIT_TEST_REKORDBOX_SETTINGS"


def _no_autoflush(session: Any):
    """Suspend the session's automatic flush, degrading to a no-op without one.

    THE FAILURE THIS PREVENTS, WHICH IS THE SHARPEST ONE IN THIS MODULE. Every
    guard downstream reads the session's PENDING collections to decide what a
    commit would do. An object-mapper session flushes pending changes before a
    query so the query can see them, and a flush empties exactly those
    collections. So any probe that queries through the caller's session hands the
    whitelist an empty session and a forbidden write sails through a guard that
    can no longer see it.

    That is not hypothetical: the cloud canary in the source system read nothing
    at all, so ordering it before the whitelist was safe by accident. Giving the
    canary a real predicate made it a query, and the guard went blind. The fix
    travels with every probe rather than with the one that exposed it.

    THE PROBE THAT EXPOSED THIS IS GONE AND THIS STAYS. The canary's database
    cross-check was deleted on evidence, so at the time of writing no pre-commit
    check queries at all and this guard has nothing to suspend. Do not delete it
    on that basis. The containment belongs to the guard PATH, not to whichever
    probe currently occupies it, and removing it because its occupant left is how
    the next probe added there inherits the hazard with the fix already gone.

    Degrades to a no-op rather than raising, because the probes are driven with
    stand-in objects in tests, and a helper that demanded a real session would
    make the guard untestable without a database.
    """
    guard = getattr(session, "no_autoflush", None)
    if guard is None:
        return nullcontext()
    return guard


def read_rekordbox_settings(app_dir: Path | str | None = None) -> Mapping[str, Any]:
    """Parse rekordbox's settings file through the binding's own reader.

    A seam as well as a reader: patching this function is how the tests drive
    every branch of :func:`cloud_sync_state` without a rekordbox install. Patch
    it HERE, in this module, because that is where the canary resolves the name.
    """
    from pyrekordbox.config import get_pioneer_app_dir
    from pyrekordbox.config import read_rekordbox_settings as _read

    base = Path(app_dir) if app_dir is not None else get_pioneer_app_dir()
    return _read(base / SETTINGS_APP_DIRNAME)


def cloud_sync_state(db: Any = None) -> CloudSyncVerdict:
    """Read whether Cloud Library Sync is on, off, or unreadable.

    ONE SOURCE, AND THAT IS A DECISION RATHER THAN A GAP. The declared setting is
    authoritative, cheap, and readable while everything is closed. A database
    cross-check for a settings file that had gone stale used to sit below; it was
    deleted on evidence, and the comment where it stood records both the evidence
    and the limit of that evidence.

    ``db`` is accepted and DELIBERATELY NOT READ. It stays in the signature
    because :func:`cloud_sync_active` is the seam every refusal site drives
    through and a handle is what any future corroborator would need. Nothing here
    queries it, which is the property that keeps this function off the hazard
    described on :func:`_no_autoflush`; adding a query means reading that first.

    WHAT WAS OBSERVED, AND WHAT WAS NOT. Read on 2026-08-01 from a disposable
    copy of a real library: the OFF encoding is ``val="0"``. The ON encoding was
    never observed. Producing it means switching library sync on against a
    library carrying 2,938,336 local updates against the 103,480 the cloud has
    ever acknowledged, dormant since 2024-08-27, which sets the cloud agent
    reconciling that backlog against a live library and is not quickly
    reversible. The comparison below is written as "not zero" precisely so that
    whatever the positive encoding turns out to be is caught by it.

    **The ON encoding is an untested inference.** It does not belong in the list
    that follows and must not be read as if it did. Every marker in that list was
    checked against a real library and found FALSE; this one was not checked at
    all. A reader who cannot tell those two apart will trust the wrong half.

    EVERY DATABASE MARKER THAT LOOKS LIKE THE ANSWER IS FALSE, and each was
    checked against a real library rather than reasoned about:

    * the cloud agent registry's row count. A real library has carried one such
      row since 2023 with sync switched off. Keying on it refused every open for
      three days, undetected, because nothing opened the database in between.
      That incident is the reason this function has three states instead of two.
    * the cloud property table's service name, which reads as a configured
      service with sync off;
    * the equipment authorisation temporary file, which tracks device auth and is
      independent of library sync;
    * the cloud credential row's timestamp, which refreshes routinely while every
      library-sync row is years stale. Authentication activity is not library
      activity, and that confusion is what produced the false positive above;
    * per-row sync columns on the content table, which are historical bookkeeping.

    TWO SETTINGS KEYS ARE TRAPS. Both the sync METHOD and the overwrite-list flag
    read as enabled while library sync is off, so anything matching a substring
    of the word "sync" produces an immediate false positive.
    """
    try:
        settings = read_rekordbox_settings()
    except Exception as exc:  # noqa: BLE001 - any failure to read is "cannot tell"
        return CloudSyncVerdict(
            CloudSyncState.UNKNOWN,
            f"the rekordbox settings file could not be read, so {LIBRARY_SYNC_SETTING} "
            f"is unknown: {exc}",
        )

    if LIBRARY_SYNC_SETTING not in settings:
        return CloudSyncVerdict(
            CloudSyncState.UNKNOWN,
            f"the rekordbox settings file carries no {LIBRARY_SYNC_SETTING} value",
        )

    declared = settings[LIBRARY_SYNC_SETTING]
    if str(declared) not in ("0", "False"):
        return CloudSyncVerdict(
            CloudSyncState.ON,
            f"{LIBRARY_SYNC_SETTING}={declared!r} in the rekordbox settings file",
        )

    # A DATABASE STALENESS CROSS-CHECK STOOD HERE AND WAS DELETED ON EVIDENCE.
    #
    # It read two cloud rows to catch a settings file that claimed off while sync
    # had in fact been running. The question it answered was "does rekordbox
    # write this file when the user flips the toggle, or only when it quits". A1
    # answered that at no cost: Auto Analysis was toggled in the interface and,
    # with rekordbox STILL RUNNING, the settings file already carried the new
    # value 23 seconds later; separately, two keys edited on disk with rekordbox
    # closed were honoured at the next startup. The file flips at toggle time, so
    # there is no staleness window for a cross-check to close (A3).
    #
    # HONEST LIMIT. That was observed on Auto Analysis and on the master database
    # directory, not on the library-sync key itself. It is strong evidence about
    # rekordbox's write discipline generally and it is a judgement, not a
    # certainty. If the settings file is ever found lagging a live toggle, this
    # is the paragraph that was wrong.
    #
    # AND A REASON NOT TO PUT IT BACK CASUALLY. That cross-check was the only
    # code in this canary that touched the caller's session. Touching the session
    # is what re-arms the hazard on ``_no_autoflush``: the query flushed a
    # caller's pending write out of the collections the additive whitelist reads,
    # so the guard approved a commit it could no longer see. The guard would have
    # passed a forbidden write BECAUSE the canary started working. Reading
    # nothing removes that at the root; anything added back here must be read
    # against ``_no_autoflush`` first.
    return CloudSyncVerdict(CloudSyncState.OFF, f"{LIBRARY_SYNC_SETTING}={declared!r}")


def cloud_sync_active(db: Any) -> bool:
    """True only when the evidence says library sync is ON.

    An unreadable state answers False here and is refused separately by
    :func:`assert_cloud_sync_readable`. Keeping the two apart is what lets this
    predicate stay the seam every refusal site drives through while the
    cannot-tell case keeps its own distinct message and its own escape.
    """
    return cloud_sync_state(db).state is CloudSyncState.ON


def assert_cloud_sync_readable(db: Any = None, *, force: bool = False) -> None:
    """Refuse a WRITE when the cloud-sync state cannot be determined.

    THE UNCERTAIN CASE, DECIDED EXPLICITLY. A state we cannot read is a
    concurrent writer we cannot rule out, and the whole module fails closed on
    the write path, so unknown refuses. The 2026 incident is not an argument
    against refusing; it is an argument against refusing silently on a false
    signal with a misattributed message. This refusal names the file it could not
    read and the error it got, which is self-diagnosing in one line.

    It binds to WRITE intent only. A read-only open must keep working on a
    machine with no rekordbox settings at all, or the snapshot integrity check
    would refuse on exactly the machine trying to verify a snapshot, and a user
    could not reach the step that fixes their setup.

    ITS OWN SLUG, NOT THE ACTIVE ONE. This refusal and the two genuinely-ACTIVE
    ones used to share a reason, so two conditions with opposite remedies arrived
    at the caller as one exit code, which is the collision the cause type exists
    to prevent. "Cloud Library Sync is on" is answered by switching it off.
    "We cannot tell whether it is on" is answered by a PERSON deciding, which is
    what the decision code already means and what its remedy token already says.
    No new code was invented for it, per S4.

    ``force`` is the boolean that decision resolves to. It is a boolean and
    nothing else: the core never learns the name of the gate that produced it,
    nor any text a user types, because remediation crosses this layer as a token
    and the rendering belongs to the command-line layer (D2).
    """
    if force:
        return
    verdict = cloud_sync_state(db)
    if verdict.state is not CloudSyncState.UNKNOWN:
        return
    raise _unavailable(
        "cloud-sync-unreadable",
        f"Cloud Library Sync could not be read, so a concurrent writer cannot be "
        f"ruled out and this write is refused: {verdict.reason}",
        # The token AND the sentence. The token says a person must answer; the
        # sentence says what to look at before answering, and it is a sentence
        # rather than a command because switching a preference in another
        # application is not something this product can run for them.
        remedy=Remedy.ANSWER_DECISION,
        steps=(
            "confirm Cloud Library Sync is switched off in rekordbox, which "
            "writes the setting this check reads",
        ),
        detail={"state": str(verdict.state), "evidence": verdict.reason},
    )


# ---------------------------------------------------------------------------
# Opening, and the generic canary
# ---------------------------------------------------------------------------


def handle_path(db: Any) -> str | None:
    """The database file an OPEN HANDLE is actually reading, or None.

    The binding keeps no public attribute for it, and the object mapper it is
    built on does: the engine carries the URL it was constructed from. Read off
    the handle rather than remembered by the caller so that a read failure names
    the file even where the caller did not open it, which is every reader that
    was handed a handle.

    None rather than a guess when the handle is not one of these, because a wrong
    path is worse here than no path: the classification would probe a file the
    failure was never about.
    """
    database = getattr(getattr(db, "engine", None), "url", None)
    spelled = getattr(database, "database", None)
    return str(spelled) if spelled else None


def canary(
    db: Any,
    *,
    write_intent: bool = False,
    force_cloud_canary: bool = False,
    path: Path | str | None = None,
) -> None:
    """Cheap reads that fail fast on key or schema drift, plus the cloud refusal.

    The two reads are chosen because they exercise the whole path: the local
    update counter proves the registry is readable and the first content row
    proves the main table maps. A failure of either means the database is
    incompatible or unopenable, whatever the file's existence suggests.

    THE FILE IS NAMED ON THE FAILURE, and this is the site the whole guarantee
    below rests on. ``canary-read-failed`` sits on the library-unreadable band,
    whose declared remedy is ``restore-from-snapshot``, which tells a user to
    overwrite the library state they still have. Over a ``chmod 000`` that advice
    destroys data, and a ``chmod 000`` is exactly what produces this failure: the
    binding opens lazily, so the file is not touched until these two reads, and
    what comes back is a driver level "unable to open database file" carrying no
    errno, no filename and nothing else to classify.

    The path is what makes it classifiable, and this is the only place that knows
    it, so this is where it is recorded. ``path`` when the caller opened the file
    and knows which one it meant, and the handle's own engine URL otherwise.
    """
    try:
        db.get_local_usn()
        db.get_content().first()
    except Exception as exc:  # noqa: BLE001 - any read failure means incompatible
        named = path if path is not None else handle_path(db)
        if named is not None:
            name_the_database(exc, named)
        where = f" at {named}" if named is not None else ""
        raise _unavailable(
            "canary-read-failed",
            f"the rekordbox database{where} opened but could not be read as "
            f"expected: {exc}",
            detail={"path": str(named)} if named is not None else None,
        ) from exc

    if cloud_sync_active(db):
        raise _unavailable(
            "cloud-sync-active",
            f"Cloud Library Sync appears active, so a cloud agent may be mutating "
            f"the database concurrently: {cloud_sync_state(db).reason}",
        )
    if write_intent:
        assert_cloud_sync_readable(db, force=force_cloud_canary)


def open_db(
    path: Path | str | None = None,
    *,
    require_closed: bool = False,
    check_app_version: bool = True,
    force_schema: bool = False,
    force_cloud_canary: bool = False,
    unlock: bool | None = None,
    cfg: config.Config | None = None,
) -> Any:
    """Open the rekordbox database behind the full open-side gate.

    THE ORDER OF THE CHECKS IS LOAD-BEARING and is preserved from the source:

    1. the parent directory, so an unmounted volume is named as an unmounted
       volume rather than as a missing file;
    2. the file itself;
    3. only on a write-intent open: the two-process refusal, then the
       application pin. Both before anything is opened, so the run aborts up
       front instead of discovering the guard at commit;
    4. the binding pin, unconditionally, so even a read-only open enforces it;
    5. the open itself, with any failure wrapped;
    6. the canary, then the schema pin.

    ``require_closed`` is the write-intent flag. A caller that forgets it gets no
    open-time refusal, which is why the commit-side check is unconditional and is
    the real backstop.

    ``unlock`` is ASKED OF THE FILE when a caller names no answer, which is
    every caller in ``src``: :func:`unlock_needed` reads the header, so a real
    library opens with the key and a disposable plain database opens without
    it. An explicit bool exists for the integration suite. It is not a safety
    escape, because the live database is encrypted and reading it with the key
    off simply fails.
    """
    target = Path(path) if path is not None else live_db_path(cfg)

    if not target.parent.exists():
        raise _unavailable(
            "library-directory-missing",
            f"the directory holding the rekordbox database does not exist: "
            f"{target.parent}; the library volume is most likely not mounted",
            detail={"directory": str(target.parent)},
        )
    if not target.exists():
        raise _unavailable(
            "library-database-missing",
            f"there is no rekordbox database at {target}",
            detail={"path": str(target)},
        )

    if require_closed:
        assert_rekordbox_closed("opening the database for writing")
        if check_app_version:
            assert_app_version(cfg=cfg)

    assert_binding_version(cfg)

    from pyrekordbox import Rekordbox6Database

    if unlock is None:
        unlock = unlock_needed(target)

    try:
        db = Rekordbox6Database(path=str(target), unlock=unlock)
    except Exception as exc:  # noqa: BLE001 - every open failure is one refusal
        # The same hand-off the canary makes, at the other half of the same
        # connection, and MEASURED TO KILL NOTHING TODAY, which is recorded in
        # the mutation table rather than left for a reader to discover. This
        # binding never connects while it constructs, so every failure it raises
        # here is a Python level error or an ``OSError`` carrying its own
        # filename, both of which the classification already answers; the case
        # that needs a recorded path is a driver level ``sqlite3.Error``, which
        # only an eagerly connecting binding produces. It stays because this slug
        # shares the canary's band and therefore its ``restore-from-snapshot``
        # default, so the day the binding connects earlier is the day a chmod
        # here starts telling a user to overwrite their library.
        name_the_database(exc, target)
        raise _unavailable(
            "database-open-failed",
            f"the rekordbox database at {target} could not be opened: {exc}",
            detail={"path": str(target)},
        ) from exc

    clear_registry_buffer()

    canary(
        db,
        write_intent=require_closed,
        force_cloud_canary=force_cloud_canary,
        path=target,
    )
    assert_schema_version(db, force=force_schema, cfg=cfg)
    return db


# ---------------------------------------------------------------------------
# Snapshot, integrity, restore, prune
# ---------------------------------------------------------------------------


def snapshot_db(
    db_path: Path | str | None = None,
    *,
    stamp: str,
    root: Path | str | None = None,
    db: Any = None,
    cfg: config.Config | None = None,
) -> Path:
    """Copy the database and everything it is incomplete without. Returns the copy.

    WRITE-AHEAD-LOG AWARE, IN TWO LAYERS. When the caller passes its open handle
    a checkpoint runs first so the database file is self-contained; that is the
    belt. The full file-set copy is the braces, and it is what actually holds the
    guarantee: a checkpoint can fail for reasons a snapshot must survive, and the
    committed transactions still sitting in the log are captured by copying the
    log itself.

    IT DOES NOT PRUNE. The source pruned from inside this function, which put
    retention inside the write session, before the commit the snapshot exists to
    protect. Pruning is a separate step the caller places after its commit (R30).
    """
    source = Path(db_path) if db_path is not None else live_db_path(cfg)
    destination_root = Path(root) if root is not None else snapshot_root(cfg)

    if db is not None:
        try:
            from sqlalchemy import text

            db.session.execute(text("PRAGMA wal_checkpoint(TRUNCATE)"))
        except Exception as exc:  # noqa: BLE001 - the checkpoint is the belt, not the braces
            logger.debug("snapshot checkpoint did not run, relying on the sidecar copy: %s", exc)

    destination = destination_root / stamp
    # An explicit mode on the directory as well as on the files: a private file
    # inside a world-writable directory can be unlinked and replaced by any local
    # account whatever its own mode says (P1).
    config._mkdir_private(destination)

    copied = destination / source.name
    shutil.copy2(source, copied)
    for suffix in db_sidecar_suffixes():
        sidecar = source.with_name(source.name + suffix)
        if sidecar.exists():
            shutil.copy2(sidecar, destination / sidecar.name)
    playlist_xml = source.parent / MASTER_PLAYLIST_XML
    if playlist_xml.exists():
        shutil.copy2(playlist_xml, destination / MASTER_PLAYLIST_XML)
    return copied


@contextmanager
def disposable_copy(source: Path | str) -> Iterator[Path]:
    """A throwaway copy of a database in a private temporary directory, then gone.

    THE ONE WAY A READ ONLY DIAGNOSTIC MAY REACH THE DATABASE (R-372). The live
    file is protected by standing constraint, so doctor and the wizard, which
    only want to count rows and read two registry entries, copy the file first
    and open the copy. Nothing here opens ``source``: it is read as bytes by the
    copy and never handed to the binding. The sidecars travel with it for the
    reason ``snapshot_db`` copies them, a database in write ahead mode is
    incomplete without its log, and a copy missing the log opens cleanly and is
    silently behind.

    ``mkdtemp`` creates the directory at 0700 (P1). The directory is removed on
    the way out whether the body raised or returned, so a diagnostic that ran a
    hundred times leaves nothing behind.
    """
    origin = Path(source)
    directory = Path(tempfile.mkdtemp(prefix="cratekit-copy-"))
    try:
        copied = directory / origin.name
        shutil.copy2(origin, copied)
        for suffix in db_sidecar_suffixes():
            sidecar = origin.with_name(origin.name + suffix)
            if sidecar.exists():
                shutil.copy2(sidecar, directory / sidecar.name)
        yield copied
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def recorded_db_drives(db: Any) -> tuple[str | None, str | None]:
    """rekordbox's own record of where this database was made and where it is now.

    ``BaseDBDrive`` and ``CurrentDBDrive`` are two COLUMNS of the one row in
    ``djmdProperty``, and they are rekordbox's renamed drive mechanism: nearly
    every collection row keeps the path it was imported under, and the
    application remaps the base drive to the current one at runtime. The source
    system verified that on 2026-08-01 and carried the old name as a constant;
    this product's answer is a ``library.location_prefix_map`` rule, and these
    two names are what setup offers it from (R-372).

    Blank and None come back as None so a caller has one absence to test. The
    trailing separator rekordbox stores is stripped, because a prefix rule is
    matched on a whole path component and ``/Volumes/NAME/`` would never match
    ``/Volumes/NAME/Music/a.flac`` under that rule.
    """
    from sqlalchemy import text

    row = db.session.execute(
        text("SELECT BaseDBDrive, CurrentDBDrive FROM djmdProperty LIMIT 1")
    ).first()
    if row is None:
        return None, None

    def _clean(value: Any) -> str | None:
        if not isinstance(value, str) or not value.strip():
            return None
        stripped = value.strip().rstrip("/\\")
        return stripped or value.strip()

    return _clean(row[0]), _clean(row[1])


def integrity_ok(snapshot_database: Path | str, *, unlock: bool | None = None) -> bool:
    """True when a snapshot passes SQLite's own consistency check.

    Run through the same open path the writers use rather than through a bare
    connection, so a snapshot that cannot be opened the way it will be USED fails
    here rather than at the moment somebody needs it. The application pin is
    skipped: a snapshot is a file, and whether an application is installed says
    nothing about whether the copy is intact. ``unlock`` is passed through
    unanswered, so the copy is asked for its key the way the open asks the
    original.
    """
    from sqlalchemy import text

    try:
        db = open_db(snapshot_database, check_app_version=False, unlock=unlock)
    except RekordboxUnavailable:
        return False
    try:
        result = db.session.execute(text("PRAGMA quick_check")).scalar()
        return str(result).lower() == "ok"
    except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
        return False
    finally:
        # The full release, not the binding's session close: this function is
        # called immediately before a session that may go on to restore the very
        # file it just verified.
        close_db(db)


def restore_from_snapshot(
    snapshot_database: Path | str,
    db_path: Path | str | None = None,
    *,
    cfg: config.Config | None = None,
) -> None:
    """Put a snapshot back, write-ahead-log symmetrically.

    THE ASYMMETRY IS THE WHOLE POINT AND IT IS NOT A TYPO. Both LIVE sidecars are
    removed first so the engine cannot replay a log belonging to the database
    that was just replaced. The snapshot's log is copied back, because the
    transactions it holds are part of the state being restored. The snapshot's
    shared-memory index is NOT copied back, because it is derived from the log,
    and a stale one beside a fresh log describes a database that no longer exists.

    The regression this encodes: a restore that copied back only the database
    file while deleting the live sidecars silently reverted a snapshot taken with
    uncheckpointed frames to a pre-log state. Nothing failed. The library was
    simply older than the snapshot said it was.

    THE CALLER MUST HAVE RELEASED EVERY HANDLE FIRST, through :func:`close_db`
    rather than through the binding's own close, which leaves a pooled connection
    open. Replacing these three files underneath a live connection produces an
    input-output error against a database that is actually intact, which reads as
    a corrupted restore and is not one.
    """
    target = Path(db_path) if db_path is not None else live_db_path(cfg)
    source = Path(snapshot_database)

    assert_rekordbox_closed("restoring the database")

    for suffix in db_sidecar_suffixes():
        live_sidecar = target.with_name(target.name + suffix)
        if live_sidecar.exists():
            live_sidecar.unlink()

    shutil.copy2(source, target)
    for suffix in restored_sidecar_suffixes():
        snapshot_sidecar = source.with_name(source.name + suffix)
        if snapshot_sidecar.exists():
            shutil.copy2(snapshot_sidecar, target.with_name(target.name + suffix))

    playlist_xml = source.parent / MASTER_PLAYLIST_XML
    if playlist_xml.exists():
        shutil.copy2(playlist_xml, target.parent / MASTER_PLAYLIST_XML)


# --- the protected-snapshot provider seam ----------------------------------


@dataclass(frozen=True, slots=True)
class RunStateVocabulary:
    """What the run-state store calls the fields this scan reads.

    A PARAMETER RATHER THAN A LITERAL because the source's equivalent was three
    literals typed into this module about a file another module writes, and all
    three were wrong: the filename, the field name, and one of the two terminal
    values. Nothing failed, because a scan that matches nothing returns nothing,
    and the result was that no snapshot was ever protected while a comment said
    they were.

    The unit that owns the session log (U8) supplies its own instance. These
    defaults were provisional and are no longer: ``core.session`` has landed and
    publishes ``RUN_STATE_VOCABULARY``, derived from its own state enumeration
    rather than restated, and it matches these values exactly.

    Two guards hold that. One compares the two vocabularies, which is the weak
    half, because the version of this that failed agreed with itself perfectly.
    The other builds a REAL session record through the session module, writes it
    to the directory the session module chooses, reads it with the scan below,
    and asserts the capture comes back protected. Changing a default here without
    changing it there fails the second one.
    """

    state_key: str = "state"
    terminal_states: frozenset[str] = frozenset({"closed", "abandoned"})
    snapshot_key: str = "snapshot_path"


def read_run_state_records(run_state_dir: Path) -> list[Mapping[str, Any]]:
    """Every run-state record in one directory, skipping anything unreadable.

    BOUNDED TO ONE DIRECTORY, one level deep. The source walked the entire
    runtime-state tree recursively on every snapshot, which on a real
    installation meant descending dozens of unrelated cache directories to find
    a file that was never there.

    Any name ending in ``.json`` counts, so this module never encodes another
    module's filename convention. That convention is exactly what the source got
    wrong.
    """
    records: list[Mapping[str, Any]] = []
    try:
        entries = sorted(run_state_dir.glob("*.json"))
    except OSError:
        return records
    for entry in entries:
        try:
            parsed = json.loads(entry.read_text())
        except (OSError, ValueError):
            continue
        if isinstance(parsed, Mapping):
            records.append(parsed)
    return records


def default_protected_snapshot_paths(
    cfg: config.Config | None = None,
    *,
    vocabulary: RunStateVocabulary | None = None,
    records: Iterable[Mapping[str, Any]] | None = None,
) -> set[Path]:
    """Snapshot paths an OPEN run still references, which pruning must never delete.

    R30 in one sentence: a snapshot an unfinished run may restore from is not
    old, whatever its position in the retention order.

    Every parameter is optional, so this remains the zero-argument callable the
    pruning seam expects while staying fully drivable from a test. Resolution
    goes through the state inventory's own path builder, never through a glob
    pattern typed in this module.
    """
    vocab = vocabulary or RunStateVocabulary()
    if records is None:
        resolved = _loaded_config(cfg)
        if resolved is None:
            return set()
        records = read_run_state_records(config.state_path("session_log", resolved))

    protected: set[Path] = set()
    for record in records:
        state = str(record.get(vocab.state_key, "")).lower()
        if state in vocab.terminal_states:
            continue  # a finished run releases its snapshot
        recorded = record.get(vocab.snapshot_key)
        if not recorded:
            continue
        try:
            protected.add(Path(str(recorded)).resolve())
        except (OSError, ValueError):
            continue
    return protected


def snapshot_database_in(directory: Path) -> Path | None:
    """The database file inside a snapshot directory, or None if it holds none.

    Derived from the file's SHAPE rather than from a fixed name, because the
    database's filename belongs to the user's rekordbox install and not to us.
    A directory holding no database is not a snapshot and is never touched.
    """
    for candidate in sorted(directory.glob("*.db")):
        if candidate.is_file():
            return candidate
    return None


def prune_snapshots(
    root: Path | str | None = None,
    *,
    keep: int = 5,
    protected_provider: Callable[[], set[Path]] | None = default_protected_snapshot_paths,
    cfg: config.Config | None = None,
) -> list[Path]:
    """Delete all but the newest ``keep`` snapshots, sparing any an open run holds.

    ``protected_provider`` is a zero-argument callable returning a set of paths.
    Passing None means no protection at all, which is only ever correct in a test
    that is asserting retention itself.

    A PROVIDER THAT RAISES DELETES NOTHING. Failing open here would mean a
    transient error in an unrelated module costs a user their recovery point, and
    a snapshot kept unnecessarily costs disk.

    A provider may return either the snapshot directory or the database file
    inside it, and both are honoured, because the snapshot function returns the
    file path and that is what a session log records.
    """
    destination_root = Path(root) if root is not None else snapshot_root(cfg)
    if not destination_root.is_dir() or keep < 1:
        return []

    provider = protected_provider
    if provider is default_protected_snapshot_paths:
        # Thread the CALLER's configuration into the default provider instead of
        # letting it resolve its own. A prune judged against one configuration
        # while the snapshot root came from another would spare the wrong
        # snapshots, and would do it silently.
        provider = partial(default_protected_snapshot_paths, cfg)

    try:
        protected = provider() if provider else set()
    except Exception as exc:  # noqa: BLE001 - a provider failure must not delete a recovery point
        logger.warning(
            "the protected-snapshot provider failed, so every snapshot is kept this run: %s",
            exc,
        )
        return []

    snapshots = sorted(
        (
            directory
            for directory in destination_root.iterdir()
            if directory.is_dir() and snapshot_database_in(directory) is not None
        ),
        key=lambda directory: directory.stat().st_mtime,
        reverse=True,
    )

    pruned: list[Path] = []
    for directory in snapshots[keep:]:
        database = snapshot_database_in(directory)
        if directory.resolve() in protected or (
            database is not None and database.resolve() in protected
        ):
            logger.info("keeping snapshot %s: an open run still references it", directory.name)
            continue
        shutil.rmtree(directory)
        pruned.append(directory)
        logger.info("pruned snapshot %s, keeping the newest %d", directory.name, keep)
    return pruned


# ---------------------------------------------------------------------------
# Playlist and tag primitives
# ---------------------------------------------------------------------------

#: Parent identifiers that mean "this tag row is a top-level category". Four
#: spellings because the value has been written all four ways over the life of
#: the schema, and a reader that knows only one silently treats a category as a
#: value.
ROOT_PARENT_SENTINELS = ("", "0", "root", "None")


def _is_folder(playlist: Any) -> bool:
    return int(getattr(playlist, "Attribute", -1)) == 1


def ensure_folder(db: Any, name: str, parent: Any = None) -> Any:
    """Find or create a playlist FOLDER by name, optionally under a parent.

    ``name`` has no default. The source defaulted it to one feature's folder,
    which put a taxonomy display name into the one module that must not carry
    one (R19).

    ``parent`` scopes the match exactly as :func:`ensure_playlist` scopes its
    own, and for the same reason: two trees may legitimately hold folders of one
    name, and a global match returns whichever the query happens to yield first.
    The asymmetry this closes was live: a caller that had gone to the trouble of
    asserting which root its tree adopted then resolved the folder globally, so
    the assertion held while the write landed somewhere else entirely.

    Unscoped stays available and stays the default, because a caller writing a
    top-level folder has no parent to name and requiring one would be a
    ceremony that answers nothing.
    """
    if parent is None:
        for playlist in db.get_playlist(Name=name):
            if _is_folder(playlist):
                return playlist
        return db.create_playlist_folder(name)

    parent_id = str(parent.ID)
    for playlist in db.get_playlist(Name=name):
        if _is_folder(playlist) and str(getattr(playlist, "ParentID", "")) == parent_id:
            return playlist
    return db.create_playlist_folder(name, parent=parent)


def ensure_playlist(db: Any, name: str, parent: Any) -> Any:
    """Find or create a playlist under a specific parent.

    Scoped to the parent, not global by name: two folders may legitimately hold
    playlists of the same name, and a global match would return somebody else's.
    """
    parent_id = str(parent.ID)
    for playlist in db.get_playlist(Name=name):
        if not _is_folder(playlist) and str(getattr(playlist, "ParentID", "")) == parent_id:
            return playlist
    return db.create_playlist(name, parent=parent)


def add_memberships(db: Any, playlist: Any, content_ids: Iterable[str]) -> list[str]:
    """Add each track to a playlist when absent. Returns the ids it inserted, in order.

    THIS IS WHERE THE "ONLY WHEN ABSENT" RULE LIVES, and :func:`add_membership`
    is a one-id call into it rather than a second spelling. A caller that wants
    to batch must come here instead of asking the database what a playlist
    holds and deciding for itself, because two implementations of one rule is
    how a track comes to be silently inserted twice or silently skipped (R-10).

    ONE presence query per call, not one per track. The playlist's current
    content ids are read once, and each insert joins that set, so an id named
    twice in one call lands once and its second mention reads as present, which
    is what the per-track read answered when the first insert was still pending.

    Read-then-insert, which is race-free ONLY under the write-session lock. That
    is not a caveat, it is a requirement: the same lock is what makes the update
    counter's autoincrement safe, so a caller outside the lock is already unsafe
    for a second reason.
    """
    present = {
        str(song.ContentID) for song in db.get_playlist_songs(PlaylistID=str(playlist.ID))
    }
    inserted: list[str] = []
    for content_id in content_ids:
        key = str(content_id)
        if key in present:
            continue
        db.add_to_playlist(playlist, key)
        present.add(key)
        inserted.append(key)
    return inserted


def add_membership(db: Any, playlist: Any, content_id: str) -> bool:
    """Add a track to a playlist when absent. True when it inserted.

    One id through :func:`add_memberships`, which owns the rule.
    """
    return bool(add_memberships(db, playlist, [content_id]))


def _mytag_templates(db: Any) -> tuple[Any, Any, Any]:
    """Mirror the shape of existing tag rows: (root parent, category, value).

    The binding defines no constants for these, so the alternative to mirroring
    is fabricating them. A fabricated attribute value produces rows rekordbox
    reads as a different kind of object, which is a corruption that looks like a
    working write.
    """
    root_parent = None
    category_attr = None
    value_attr = None
    for tag in db.get_my_tag():
        parent_id = str(getattr(tag, "ParentID", "") or "")
        if parent_id in ROOT_PARENT_SENTINELS:
            if category_attr is None:
                root_parent, category_attr = parent_id, getattr(tag, "Attribute", 0)
        elif value_attr is None:
            value_attr = getattr(tag, "Attribute", 0)
    if category_attr is None:
        raise _unavailable(
            "mytag-category-template-missing",
            "the library has no tag category to mirror, so there is nothing to "
            "copy the row shape from and this writer refuses to invent one",
        )
    if value_attr is None:
        value_attr = category_attr
    return root_parent, category_attr, value_attr


def ensure_my_tag_value(db: Any, category_name: str, value_name: str) -> Any:
    """Find or create a tag category and one value inside it. Returns the value row."""
    from uuid import uuid4

    from pyrekordbox.db6 import tables

    root_parent, category_attr, value_attr = _mytag_templates(db)

    category = next((tag for tag in db.get_my_tag(Name=category_name)), None)
    if category is None:
        category = tables.DjmdMyTag.create(
            ID=db.generate_unused_id(tables.DjmdMyTag, is_28_bit=True),
            UUID=str(uuid4()),
            Name=category_name,
            Attribute=category_attr,
            ParentID=root_parent,
            Seq=0,
        )
        db.add(category)

    value = next(
        (
            tag
            for tag in db.get_my_tag(Name=value_name)
            if str(getattr(tag, "ParentID", "")) == str(category.ID)
        ),
        None,
    )
    if value is None:
        value = tables.DjmdMyTag.create(
            ID=db.generate_unused_id(tables.DjmdMyTag, is_28_bit=True),
            UUID=str(uuid4()),
            Name=value_name,
            Attribute=value_attr,
            ParentID=str(category.ID),
            Seq=0,
        )
        db.add(value)
    return value


def add_my_tag(db: Any, value_row: Any, content_id: str) -> bool:
    """Associate a track with a tag value when absent. True when it inserted."""
    from uuid import uuid4

    from pyrekordbox.db6 import tables

    existing = db.get_my_tag_songs(
        MyTagID=str(value_row.ID), ContentID=str(content_id)
    ).first()
    if existing is not None:
        return False
    db.add(
        tables.DjmdSongMyTag.create(
            ID=db.generate_unused_id(tables.DjmdSongMyTag),
            UUID=str(uuid4()),
            MyTagID=str(value_row.ID),
            ContentID=str(content_id),
            TrackNo=0,
        )
    )
    return True


# ---------------------------------------------------------------------------
# The additive whitelist
# ---------------------------------------------------------------------------

#: The content table, named once so the judge and the registry cannot disagree.
CONTENT_TABLE = "djmdContent"

#: Tables a writer may CREATE rows in. A new content row is forbidden because
#: new-track intake stays in the XML bridge, where the user performs, reviews and
#: can undo the import. A beat-grid row cannot even be modelled, since the
#: binding has no class for it, but that is not what makes it unwritable: ANY
#: unlisted table is refused, so grid and analysis rows are structurally
#: impossible rather than merely untested (R17).
#:
#: Static, and deliberately not feature-derived. This is the set that makes the
#: structural guarantee, so no registration may widen it.
PERMITTED_ROW_TABLES = frozenset(
    {"djmdPlaylist", "djmdSongPlaylist", "djmdMyTag", "djmdSongMyTag", "djmdKey"}
)

#: ``djmdKey`` joins the whitelist on the A4 verdict, TOLERATED, settled against
#: rekordbox 7.2.17 on 2026-08-01. An externally authored key row rendered
#: correctly while referenced and was left completely untouched across a full
#: launch and quit cycle: rekordbox did not renumber ``Seq``, did not set ``usn``,
#: did not flip ``rb_data_status`` and did not soft-delete. There is no column
#: ownership to document because rekordbox took ownership of nothing.
#:
#: TWO RULES TRAVEL WITH THE PERMISSION, and both are preventable only in code.
#:
#: 1. Create and link in the SAME write session. Never speculatively. rekordbox
#:    garbage collects a lookup row nothing references, which it was observed
#:    doing (43 rows to 42), and it would do the same to one of its own.
#: 2. A duplicate ``ScaleName`` is the one real hazard. There is no unique
#:    constraint and no trigger, so it is invisible to the schema. Resolve before
#:    creating, under the write lock this module already holds.
#:
#: THE PERMISSION IS A CEILING, NOT A LICENCE. Phillip's decision, taken at the
#: desk while A4 ran, is that the writer may never author a key value at all:
#: padded Camelot belongs in the track title as a sorting artifact, and the key
#: metadata field stays blank so rekordbox's answer and this product's answer
#: remain independently comparable. That is the grid rule's own argument one
#: layer up. Nothing in this module can write a key today and nothing should
#: acquire the ability without that decision being revisited.

#: Analysis columns a row THIS PRODUCT CREATES may never declare. Checked on
#: creation, which until W3 had no column policy at all.
#:
#: AN HONEST LIST RATHER THAN A DERIVATION, and the honesty is the point (P4). A
#: rule such as "every column whose name contains Analysis" reads plausibly and
#: misses ``BPM`` and ``CueUpdated``, and a derivation that is nearly complete
#: invites trust it has not earned. A test asserts every name here is a real
#: column on the content table, so a binding rename fails loudly rather than
#: silently disarming the check.
GRIDLESS_ON_CREATE_COLUMNS = frozenset(
    {
        "BPM",
        "Analysed",
        "AnalysisDataPath",
        "AnalysisUpdated",
        "CueUpdated",
    }
)

#: rekordbox's soft-delete marker, named once so a reader can be BOUND to it
#: rather than to a string that looks like it.
#:
#: The column belongs to this module because the vocabulary of the binding does,
#: and it is spelled out here rather than left as a literal inside
#: :data:`BOOKKEEPING_COLUMNS` because a guard that can only recognize the literal
#: is one indirection away from being switched off. A reader that says
#: ``rb_writer.SOFT_DELETE_COLUMN`` is resolvable through the import graph; a
#: reader that says ``"rb_local_deleted"`` is a string somebody typed.
#:
#: Naming it does NOT make it readable permissively. It is a bookkeeping column,
#: so a binding that stops exposing it produces a row that cannot say whether it
#: is a tombstone, and every default a reader could supply for that is the answer
#: "active", which is the permissive one. See
#: ``tests/_source_guards.py:permissive_soft_delete_reads``.
SOFT_DELETE_COLUMN = "rb_local_deleted"

#: Columns the binding and the object mapper bump on their own during a commit.
#: TEN of them. Without every one, an otherwise legitimate write trips the guard,
#: and a guard that fires on correct code gets disabled, which is the failure mode
#: that actually loses data (P7).
BOOKKEEPING_COLUMNS = frozenset(
    {
        "ID",
        "UUID",
        "usn",
        "rb_local_usn",
        "rb_data_status",
        "rb_local_data_status",
        SOFT_DELETE_COLUMN,
        "rb_local_synced",
        "created_at",
        "updated_at",
    }
)


class Ownership(StrEnum):
    """How strongly an operation owns a field it declares.

    ``OWNED`` means the operation may overwrite, because it owns that field's
    formatting or assignment outright. ``FILL_IF_EMPTY`` means it writes only
    into an unset field, which is what keeps a value a person set by hand from
    being replaced by automation.
    """

    OWNED = "owned"
    FILL_IF_EMPTY = "fill_if_empty"


@dataclass(frozen=True, slots=True)
class FieldPolicy:
    """One operation's declared fields, and how strongly it owns each.

    THIS IS THE SEAM THAT INVERTS THE DIRECTION. The source kept a single static
    table here, keyed on feature operation names, so the writer enumerated
    features and the writable column set was the maximal union of every operation
    that might ever exist. On a slim install with no metadata operations enabled,
    four columns were still structurally writable for no reason.

    Operations now register themselves, the writable set becomes the union of
    what is actually enabled, and R14's "widened only as far as each feature
    requires" is implemented rather than described.
    """

    owner: str
    fields: Mapping[str, Ownership]


#: The one operation that exists at this unit's time: the track colour write. It
#: is registered here rather than left to a later unit because the whitelist must
#: be meaningful the moment it ships, and an empty writable set would make the
#: guard vacuous instead of strict.
TRACK_COLOR_POLICY = FieldPolicy(
    owner="track-color",
    fields=MappingProxyType({"ColorID": Ownership.OWNED}),
)

_REGISTERED: dict[str, FieldPolicy] = {}


def register_field_policy(policy: FieldPolicy) -> None:
    """Declare one operation's fields, widening the writable column set by exactly them.

    Registration happens when the operation is enabled. An operation that is not
    registered can write nothing at all, which is the property that makes the set
    closed by construction rather than by review.
    """
    _REGISTERED[policy.owner] = policy


def reset_field_policies() -> None:
    """Return the registry to its baseline. For tests, and for a re-enabled profile."""
    _REGISTERED.clear()
    register_field_policy(TRACK_COLOR_POLICY)


def registered_field_policies() -> Mapping[str, FieldPolicy]:
    """Every operation currently permitted to write a content column."""
    return MappingProxyType(dict(_REGISTERED))


def content_writable_columns() -> frozenset[str]:
    """The union of every registered operation's declared fields.

    Derived by walking the registry rather than by listing, so an operation added
    later cannot be missed and an operation disabled later cannot leave its
    column writable (P3).
    """
    columns: set[str] = set()
    for policy in _REGISTERED.values():
        columns.update(policy.fields)
    return frozenset(columns)


reset_field_policies()


def guard_violations(
    new: Iterable[tuple[str, Iterable[str]]],
    dirty: Iterable[tuple[str, Iterable[str]]],
    deleted: Iterable[str],
    *,
    content_columns: Iterable[str] | None = None,
) -> list[str]:
    """Judge a pending session against the whitelist. Empty means allowed.

    PURE, and that is what makes it the part of the safety chain that is actually
    tested. It takes table names and column names, so every branch is reachable
    with literal inputs and no database at all.

    It returns EVERY violation rather than the first. A guard that stops at the
    first finding turns one review into as many round trips as there are
    problems, which is how a guard becomes something people work around.
    """
    writable = (
        frozenset(content_columns)
        if content_columns is not None
        else content_writable_columns()
    )
    violations: list[str] = []

    for table, columns in new:
        if table == CONTENT_TABLE:
            violations.append(
                f"creates a {CONTENT_TABLE} row; new-track intake stays in the XML "
                f"bridge, where an import is something a person performs and can undo"
            )
            continue
        if table not in PERMITTED_ROW_TABLES:
            violations.append(f"creates a row in the non-whitelisted table {table!r}")
            continue
        # W3. A CREATION used to be judged on its table name alone, so a row in a
        # permitted table could declare any column at all, analysis columns
        # included. The column set was bound and then discarded.
        declared = {column for column in columns if column in GRIDLESS_ON_CREATE_COLUMNS}
        if declared:
            violations.append(
                f"creates a row in {table!r} declaring analysis column(s): "
                f"{sorted(declared)}; a row this product creates is gridless and "
                f"rekordbox derives the grid from the audio"
            )

    for table, columns in dirty:
        modified = {column for column in columns if column not in BOOKKEEPING_COLUMNS}
        if not modified:
            continue
        if table == CONTENT_TABLE:
            forbidden = modified - writable
            if forbidden:
                violations.append(
                    f"modifies non-whitelisted {CONTENT_TABLE} column(s): {sorted(forbidden)}"
                )
        elif table not in PERMITTED_ROW_TABLES:
            violations.append(
                f"modifies the non-whitelisted table {table!r}: {sorted(modified)}"
            )

    for table in deleted:
        # Unconditional. No table exemption, no flag, no configuration. Additive
        # only is what makes the snapshot a real safety net: if nothing is ever
        # removed, the worst outcome of a bad run is extra rows, which a person
        # can see and remove. Deletion is the one operation whose damage is
        # invisible. Do not soften this to make a later unit easier.
        violations.append(f"deletes a row in {table!r}; writers are additive-only")

    return violations


#: Reported instead of a column name when an object cannot be introspected.
#: Guaranteed to be outside every writable set, so it refuses.
UNINSPECTABLE = "<uninspectable>"

#: Reported for a re-parented row, whose changed column the binding's buffer does
#: not carry. A named sentinel rather than an empty set, because an empty set is
#: indistinguishable from a bookkeeping-only touch and would skip the table check
#: entirely. On a whitelisted table it passes, on any other it refuses, which is
#: exactly the judgement a move deserves.
MOVED = "<moved>"


def clear_registry_buffer() -> None:
    """Empty the binding's process-wide update buffer.

    Called when a write session opens. The binding already does this inside its
    own open, so this is belt and braces, and it is cheap. It is here because the
    guard's correctness now DEPENDS on the buffer describing this session and no
    other, and a dependency that important should be asserted by this module
    rather than inherited from a library's implementation detail. A test pins it.
    """
    try:
        from pyrekordbox.db6.registry import RekordboxAgentRegistry
    except Exception:  # noqa: BLE001 - binding absent means no buffer to clear
        return
    RekordboxAgentRegistry.clear_buffer()


def _table_of(obj: Any) -> str | None:
    table = getattr(obj, "__table__", None)
    return getattr(table, "name", None)


def _columns_of(obj: Any) -> set[str]:
    """The columns an EXISTING object reports as changed. Fails closed."""
    from sqlalchemy import inspect as sa_inspect

    try:
        return {
            attribute.key
            for attribute in sa_inspect(obj).attrs
            if attribute.history.has_changes()
        }
    except Exception:  # noqa: BLE001 - un-inspectable means treat as all-changed
        return {UNINSPECTABLE}


def _declared_columns(obj: Any) -> set[str]:
    """The columns a NOT YET FLUSHED object carries a value for.

    Deliberately does NOT go through the object mapper. Inspecting a transient
    instance forces mapper configuration, and if that configuration fails the
    failure is CACHED process-wide: every later mapper use then raises, including
    in code that had nothing to do with the guard. Swallowing the exception here
    does not undo it, because the damage is recorded inside the mapper registry
    rather than raised past us. Reading the instance dictionary asks the same
    question and touches none of that machinery.

    Fails closed, like its sibling: an object with no table reports the sentinel.
    """
    table = getattr(obj, "__table__", None)
    if table is None:
        return {UNINSPECTABLE}
    names = {column.name for column in table.columns}
    try:
        state = vars(obj)
    except TypeError:  # no instance dictionary to read
        return {UNINSPECTABLE}
    return {key for key, value in state.items() if key in names and value is not None}


def _session_changes(
    session: Any,
) -> tuple[dict[int, tuple[str, set[str]]], dict[int, tuple[str, set[str]]], dict[int, str]]:
    """Adapt an object-mapper session into the judge's inputs, keyed by instance.

    FAILS CLOSED. An object whose state cannot be introspected reports a
    placeholder column name, which is guaranteed to be outside any writable set
    and therefore refuses. The alternative, reporting no changed columns, would
    let exactly the objects we cannot see through unexamined.

    NOT SUFFICIENT ON ITS OWN, which is the whole of W2. ``session.new`` and
    ``session.dirty`` are emptied by any flush, and SQLAlchemy flushes pending
    work before a query so the query can see it. A flushed INSERT is still
    uncommitted and still rollback-able, but it has left these collections, so a
    guard reading only them judges an empty session and approves. Every one of
    this module's own primitives does an add followed by a lookup, in a loop, so
    the blindness is the normal case rather than the exotic one.

    Keyed by ``id(instance)`` so the union with the registry buffer merges rather
    than double-reports.
    """
    created = {
        id(obj): (_table_of(obj) or UNINSPECTABLE, _declared_columns(obj)) for obj in session.new
    }
    modified = {
        id(obj): (_table_of(obj) or UNINSPECTABLE, _columns_of(obj)) for obj in session.dirty
    }
    removed = {id(obj): (_table_of(obj) or UNINSPECTABLE) for obj in session.deleted}
    return created, modified, removed


def _registry_changes(
    db: Any,
) -> tuple[dict[int, tuple[str, set[str]]], dict[int, tuple[str, set[str]]], dict[int, str]]:
    """The same judgement inputs, read from the binding's own update buffer.

    ``RekordboxAgentRegistry.__update_sequence__`` is a process-wide list the
    binding appends to on every tracked write. Crucially it is NOT emptied by a
    flush: it is cleared only on open, close, commit and rollback. So it still
    holds a creation that autoflush has already carried out of ``session.new``,
    which is exactly what makes it the fix for W2.

    It is not sufficient on its own either. The binding disables its own tracking
    around a dozen of its internal operations, and a raw ``session.add`` never
    reaches it at all. Neither source is complete, so the guard reads the UNION.
    Stating that plainly matters: a derivation that is nearly complete invites
    trust it has not earned (P4).

    Reads a list. Runs no query, so it cannot flush anything itself.

    SCOPED TO A HANDLE, DELIBERATELY. The buffer is a CLASS attribute, shared
    process wide, and the binding clears it on open, close, commit and rollback
    rather than per session. So without an open handle there is no session whose
    buffer this could be, and reading it anyway attributes another caller's
    writes to this one. That is not hypothetical: it fired the first time this
    ran, when a guard called with no handle inherited rows created by earlier
    work in the same process and refused a write that was perfectly legitimate.
    A guard that refuses correct code is one people route around (P7).
    """
    if db is None:
        return {}, {}, {}
    try:
        from pyrekordbox.db6.registry import RekordboxAgentRegistry
    except Exception:  # noqa: BLE001 - binding absent means no buffer to read
        return {}, {}, {}

    created: dict[int, tuple[str, set[str]]] = {}
    modified: dict[int, tuple[str, set[str]]] = {}
    removed: dict[int, str] = {}

    for entry in list(getattr(RekordboxAgentRegistry, "__update_sequence__", [])):
        try:
            target, op, key, _value = entry
        except (TypeError, ValueError):  # a shape this code does not understand
            modified[id(entry)] = (UNINSPECTABLE, {UNINSPECTABLE})
            continue
        # "move" carries a LIST of instances; the other three carry one.
        instances = target if isinstance(target, (list, tuple)) else [target]
        for obj in instances:
            table = _table_of(obj)
            if table is None:
                modified[id(obj)] = (UNINSPECTABLE, {UNINSPECTABLE})
            elif op == "create":
                created[id(obj)] = (table, _declared_columns(obj))
            elif op == "update":
                seen = modified.get(id(obj))
                columns = set(seen[1]) if seen else set()
                columns.add(key if key else UNINSPECTABLE)
                modified[id(obj)] = (table, columns)
            elif op == "delete":
                removed[id(obj)] = table
            elif op == "move":
                modified[id(obj)] = (table, {MOVED})
            else:
                # An operation this code has never heard of. Refuse rather than
                # ignore: a future binding adding a fifth op must fail loudly
                # here, not pass silently.
                modified[id(obj)] = (table, {UNINSPECTABLE})
    return created, modified, removed


def pending_changes(
    session: Any, db: Any = None
) -> tuple[list[tuple[str, set[str]]], list[tuple[str, set[str]]], list[str]]:
    """Everything this session will write, from BOTH sources, unioned.

    Creation wins over modification for the same instance: a row created and then
    updated in one session is a creation, and reporting it as both would produce
    two findings for one act.
    """
    s_created, s_modified, s_removed = _session_changes(session)
    r_created, r_modified, r_removed = _registry_changes(db)

    created = {**r_created, **s_created}

    modified: dict[int, tuple[str, set[str]]] = {}
    for source in (r_modified, s_modified):
        for key, (table, columns) in source.items():
            seen = modified.get(key)
            modified[key] = (table, (set(seen[1]) if seen else set()) | set(columns))

    # Creation wins.
    for key in created:
        modified.pop(key, None)

    removed = {**r_removed, **s_removed}

    return list(created.values()), list(modified.values()), list(removed.values())


def assert_created_rows_are_gridless(db: Any) -> None:
    """Verify from SQL that no row this session creates carries analysis data.

    WHY NOT READ THE OBJECT. The mapped object is our own construction, so
    reading an attribute off it reports what the writer INTENDED rather than what
    the database will store, and between that read and the INSERT the binding's
    own machinery still runs: it stamps a local update sequence onto every
    buffered instance, and column defaults are applied by the database rather
    than by the attribute. Second, after a flush the object may be expired, so
    reading an attribute can trigger a fresh load and the answer then depends on
    session cache state rather than on the row. The in-memory check in
    ``guard_violations`` is a backstop; this is the check.

    ORDERING IS LOAD BEARING. The flush here is DELIBERATE and happens after the
    guard has already captured what it is judging, so it cannot be the flush that
    blinds the guard. It runs before the commit, so a violation still rolls back.
    A check that only ran after the commit would find a violation it could no
    longer undo, leaving a snapshot restore as the sole remedy.
    """
    session = getattr(db, "session", None)
    if session is None:
        return

    from sqlalchemy import inspect as sa_inspect
    from sqlalchemy import text

    created, _modified, _removed = _session_changes(session)
    r_created, _, _ = _registry_changes(db)
    instances = {**r_created, **created}
    if not instances:
        return

    # Resolve the objects again by identity so the primary keys are populated.
    pending = [obj for obj in session.new]
    try:
        session.flush()
    except Exception:  # noqa: BLE001 - a flush failure is the caller's to report
        return

    violations: list[str] = []
    for obj in pending:
        table = _table_of(obj)
        if table is None:
            continue
        columns = {c.name for c in obj.__table__.columns} & GRIDLESS_ON_CREATE_COLUMNS
        if not columns:
            continue
        identity = sa_inspect(obj).identity
        if not identity:
            continue
        keys = [c.name for c in obj.__table__.primary_key.columns]
        where = " AND ".join(f"{k} = :{k}" for k in keys)
        selected = ", ".join(sorted(columns))
        row = session.execute(
            text(f"SELECT {selected} FROM {table} WHERE {where}"),
            dict(zip(keys, identity)),
        ).first()
        if row is None:
            continue
        for name, value in zip(sorted(columns), row):
            if value not in (None, 0, 0.0, "", "0"):
                violations.append(f"{table}.{name} = {value!r}")

    if violations:
        raise _unavailable(
            "whitelist-violation",
            "a row this session creates carries analysis data, which this product "
            "never writes; rekordbox derives the grid from the audio:\n  - "
            + "\n  - ".join(violations),
            detail={"violations": violations},
        )


def assert_session_whitelisted(session: Any, db: Any = None) -> None:
    """Raise unless the pending session touches only whitelisted tables and columns."""
    created, modified, removed = pending_changes(session, db)
    violations = guard_violations(created, modified, removed)
    if violations:
        raise _unavailable(
            "whitelist-violation",
            "the pending write session touches tables or columns outside the "
            "additive whitelist:\n  - " + "\n  - ".join(violations),
            detail={"violations": list(violations)},
        )


# ---------------------------------------------------------------------------
# Per-field metadata policy: the semantic gate above the structural one
# ---------------------------------------------------------------------------


class Decision(StrEnum):
    """What the per-field policy says about one proposed write."""

    WRITE = "write"
    SKIP_SAME = "skip_same"
    SKIP_PRESENT = "skip_present"
    SKIP_UNOWNED = "skip_unowned"


#: What "unset" means per column, because fill-if-empty has to know when a value
#: is absent and the database spells absence three ways.
#:
#: AN HONEST LIST RATHER THAN A DERIVATION. A rule such as "identifier columns
#: also count zero as empty" covers four of these five and quietly misses the
#: rating, and a derivation that is nearly complete is worse than a list, because
#: it invites trust (P4). Anything not named here falls back to the two spellings
#: every column shares.
FIELD_EMPTIES: Mapping[str, tuple[Any, ...]] = MappingProxyType(
    {
        "Title": (None, ""),
        "Rating": (None, "", 0, "0"),
        "GenreID": (None, "", 0, "0"),
        "KeyID": (None, "", 0, "0"),
        "ColorID": (None, "", 0, "0"),
    }
)

_DEFAULT_EMPTIES: tuple[Any, ...] = (None, "")


def metadata_decision(
    owner: str,
    field_name: str,
    current: Any,
    new: Any,
    *,
    policies: Mapping[str, FieldPolicy] | None = None,
) -> Decision:
    """Decide one field write. Pure, so every operation is testable without a database.

    CLOSED BY CONSTRUCTION. An operation that has not registered, or a field it
    did not declare, is unowned and writes nothing. That is what makes ratings a
    person set, colours a person chose, and comments a person typed unwritable by
    automation: they simply have no policy entry.
    """
    table = policies if policies is not None else _REGISTERED
    policy = table.get(owner)
    mode = None if policy is None else policy.fields.get(field_name)
    if mode is None:
        return Decision.SKIP_UNOWNED
    if str(current) == str(new):
        return Decision.SKIP_SAME  # idempotent: re-running a run is a no-op
    if mode is Ownership.OWNED:
        return Decision.WRITE
    empties = FIELD_EMPTIES.get(field_name, _DEFAULT_EMPTIES)
    return Decision.WRITE if current in empties else Decision.SKIP_PRESENT


def write_metadata_field(
    row: Any,
    owner: str,
    field_name: str,
    new_value: Any,
    *,
    policies: Mapping[str, FieldPolicy] | None = None,
) -> Decision:
    """Apply the per-field policy to one existing row and report what happened.

    Does not commit. The caller batches and calls :func:`commit_guarded`, whose
    whitelist is the structural backstop underneath this semantic one.
    """
    current = getattr(row, field_name, None)
    decision = metadata_decision(owner, field_name, current, new_value, policies=policies)
    if decision is Decision.WRITE:
        setattr(row, field_name, new_value)
    return decision


# ---------------------------------------------------------------------------
# The cross-process write-session lock
# ---------------------------------------------------------------------------


def _acquire_exclusive(handle: Any) -> None:
    """Take a non-blocking exclusive lock on an open file. Raises OSError on contention.

    Two backends, selected at call time rather than at import so the module stays
    importable on a platform with neither. Both give the property that matters:
    the kernel releases the lock when the holder dies, which IS the stale-lock
    recovery story. A lock file carrying a process identifier is deliberately not
    used, because reclaiming one means unlinking and recreating, and that races a
    live holder.
    """
    if sys.platform.startswith("win"):  # pragma: no cover - needs Windows
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        return
    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def _release_exclusive(handle: Any) -> None:
    if sys.platform.startswith("win"):  # pragma: no cover - needs Windows
        import msvcrt

        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        return
    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def write_session_lock(path: Path | str | None = None, *, cfg: config.Config | None = None):
    """Hold the write-session lock for a whole session: snapshot through smoke test.

    Two writers must not interleave. The membership helper's read-then-insert and
    the update counter's autoincrement are race-free only under this lock, and a
    failing writer's snapshot restore would otherwise erase a concurrent writer's
    committed work.

    THE FILE IS NEVER UNLINKED. Unlinking it to "clean up" races a live holder
    that is holding a lock on the inode, and the second process then creates a
    fresh file and locks that instead, so both believe they hold it.

    NOT THE SAME LOCK AS THE SESSION LOCK, and the difference is scope rather
    than mechanism. This one is narrow: it is held from capture through smoke
    test so two writers cannot interleave. ``core.session`` holds a wider one on
    its own file for a whole destructive session, so a second process refuses at
    the door instead of part way through. Both call the same two acquisition
    helpers below, deliberately: a second implementation of one primitive is a
    second chance for the two to differ on a platform nobody tests.
    """
    target = Path(path) if path is not None else write_lock_path(cfg)
    # The directory mode is part of the file mode: a private lock file inside a
    # world-writable directory can be unlinked and replaced by any local account,
    # which takes mutual exclusion with it (P1).
    config._mkdir_private(target.parent)

    handle = open(target, "a+")
    try:
        if hasattr(os, "chmod"):  # guarded: a POSIX mode is meaningless on some platforms
            try:
                os.chmod(target, config.PRIVATE_FILE_MODE)
            except OSError as exc:
                # Best effort, and deliberately not fatal. The mode matters, but
                # not as much as the lock: a second person on a shared machine
                # cannot chmod a file the first one created, and refusing there
                # would turn a cosmetic problem into no mutual exclusion at all.
                logger.debug("could not set the mode on the write lock at %s: %s", target, exc)
        try:
            _acquire_exclusive(handle)
        except OSError as exc:
            raise _unavailable(
                "write-lock-held",
                f"another writer holds the write-session lock at {target}; it is "
                f"not reclaimable by force, so wait for that run to finish",
                detail={"lock": str(target)},
            ) from exc
        yield target
    finally:
        try:
            _release_exclusive(handle)
        finally:
            handle.close()


# ---------------------------------------------------------------------------
# The guarded commit
# ---------------------------------------------------------------------------


class CommitWitness:
    """Whether the SQL commit on one handle has landed. See :func:`commit_witness`."""

    __slots__ = ("landed",)

    def __init__(self) -> None:
        self.landed = False

    def _mark(self, _session: Any) -> None:
        self.landed = True


@contextmanager
def commit_witness(db: Any) -> Iterator[CommitWitness]:
    """Tell a commit that LANDED and then raised from one that never landed.

    AN EXCEPTION OUT OF A COMMIT DOES NOT MEAN NOTHING WAS COMMITTED. The
    binding's ``commit`` lands the SQL transaction FIRST and only then reconciles
    and saves rekordbox's legacy playlist file, so a failure in that second half
    arrives as an exception over rows that are already durable. A caller that
    reads the exception as "nothing landed" rolls back, which by then does
    nothing, and records a session that committed no work, and the next restore
    reaches back past those rows without asking.

    Asked of the engine rather than inferred from where the exception came from:
    the listener is SQLAlchemy's own ``after_commit``, which fires when the
    transaction has landed and at no other time. Removed on the way out, so a
    handle that outlives this block is left as it was found.
    """
    from sqlalchemy import event

    witness = CommitWitness()
    target = getattr(db, "session", None)
    if target is None:
        yield witness
        return
    event.listen(target, "after_commit", witness._mark)
    try:
        yield witness
    finally:
        event.remove(target, "after_commit", witness._mark)


def commit_guarded(db: Any, *, force_cloud_canary: bool = False) -> None:
    """Commit only when it is still safe to, and roll back rather than leak.

    RE-CHECKED AT COMMIT, NOT ONLY AT OPEN, AND UNCONDITIONALLY. A run takes
    minutes, and the user can launch rekordbox during it. The open-time process
    refusal is behind a flag a caller can forget; this one is not, which is what
    makes it the real backstop.

    A GUARD FAILURE ROLLS THE SESSION BACK. Leaving the rejected objects pending
    would carry them into whatever commits next, so a refused write would land
    later under a different operation's name.

    The binding's post-commit reconciliation logs one warning per playlist absent
    from rekordbox's legacy playlist file, which under rekordbox 7 is a near-empty
    artifact. That logger is quietened for the duration of the commit only, and
    restored in a finally, so a failure cannot leave the process permanently
    quieter than it was.
    """
    assert_rekordbox_closed("committing")

    # EVERY PRE-COMMIT CHECK RUNS WITH THE AUTOMATIC FLUSH SUSPENDED. The checks
    # below read the database, and a query would otherwise flush the caller's
    # pending work before the whitelist has judged it, which empties the
    # collections the whitelist inspects. See ``_no_autoflush``: this is the one
    # ordering in the module where a read can defeat a guard.
    with _no_autoflush(getattr(db, "session", None)):
        if cloud_sync_active(db):
            raise _unavailable(
                "cloud-sync-active",
                f"Cloud Library Sync appears active, so this commit would race a "
                f"concurrent writer: {cloud_sync_state(db).reason}",
            )
        assert_cloud_sync_readable(db, force=force_cloud_canary)

        try:
            # Reads the binding's update buffer as well as the session, so a
            # write autoflush has already carried out of ``session.new`` is
            # still judged (W2).
            assert_session_whitelisted(db.session, db)
            assert_created_rows_are_gridless(db)
        except RekordboxUnavailable:
            # Rolled back rather than left pending: carrying rejected objects
            # forward would land a refused write later, under whatever operation
            # commits next and in that operation's name.
            db.rollback()
            raise

    reconciliation_logger = logging.getLogger("pyrekordbox.db6.database")
    previous = reconciliation_logger.level
    reconciliation_logger.setLevel(logging.ERROR)
    try:
        db.commit()
    finally:
        reconciliation_logger.setLevel(previous)


__all__ = [
    "BOOKKEEPING_COLUMNS",
    "CONTENT_TABLE",
    "CommitWitness",
    "ENV_APP_PATH",
    "FIELD_EMPTIES",
    "GRIDLESS_ON_CREATE_COLUMNS",
    "LIBRARY_SYNC_SETTING",
    "MASTER_PLAYLIST_XML",
    "PERMITTED_ROW_TABLES",
    "ROOT_PARENT_SENTINELS",
    "SETTINGS_APP_DIRNAME",
    "SOFT_DELETE_COLUMN",
    "TEST_DB_ENV",
    "TEST_SETTINGS_ENV",
    "TRACK_COLOR_POLICY",
    "CloudSyncState",
    "CloudSyncVerdict",
    "Decision",
    "FieldPolicy",
    "Ownership",
    "RekordboxRunning",
    "RekordboxUnavailable",
    "RunStateVocabulary",
    "SQLITE_HEADER",
    "add_membership",
    "add_memberships",
    "add_my_tag",
    "assert_app_version",
    "assert_binding_version",
    "assert_cloud_sync_readable",
    "assert_rekordbox_closed",
    "assert_schema_version",
    "assert_created_rows_are_gridless",
    "assert_session_whitelisted",
    "canary",
    "cloud_sync_active",
    "cloud_sync_state",
    "close_db",
    "clear_registry_buffer",
    "commit_guarded",
    "commit_witness",
    "content_writable_columns",
    "db_schema_version",
    "db_sidecar_suffixes",
    "default_protected_snapshot_paths",
    "ensure_folder",
    "ensure_my_tag_value",
    "ensure_playlist",
    "MOVED",
    "UNINSPECTABLE",
    "guard_violations",
    "pending_changes",
    "integration_db_path",
    "integrity_ok",
    "live_db_path",
    "metadata_decision",
    "open_db",
    "pin_validated_on",
    "pinned_app_version",
    "pinned_db_version",
    "pinned_pyrekordbox",
    "prune_snapshots",
    "read_installed_app_version",
    "read_rekordbox_settings",
    "read_run_state_records",
    "register_field_policy",
    "registered_field_policies",
    "rekordbox_agent_running",
    "rekordbox_processes_running",
    "rekordbox_running",
    "reset_field_policies",
    "restore_from_snapshot",
    "restored_sidecar_suffixes",
    "snapshot_database_in",
    "snapshot_db",
    "snapshot_root",
    "unlock_needed",
    "write_lock_path",
    "write_metadata_field",
    "write_session_lock",
]
