"""Configuration, the two state roots, and the frozen identity a queued job runs against.

Rule 1: nothing here touches the filesystem at import, so ``crate --help`` and
the health check run on a machine never set up. Config is lazy, so
``config_dir()``, ``config_path()`` and ``load()`` are functions, and there is
no module-level path constant for another module to snapshot, because a bound
copy keeps the old value after a reload. ``tests/test_config.py`` fails the
build if a module grows one.

Rule 2: a value that can change without the user deciding it is state, not
config. Watermarks, tombstones, declines, locks, calibration, session logs,
cached tokens and the active taxonomy template live in a state root.

The two state roots (KTD21):

* Installation-scoped, under the platform's per-user config and state
  directories: config, credentials, the job queue, and caches that describe a
  remote account or a replayable lookup.
* Library-scoped, in a dot-directory beside the library: the write lock, the
  session log and its snapshots, watermarks, tombstones, declines, the deletion
  watermark, calibration, the tree registry and the active taxonomy template.

Each ``STATE_FILES`` entry names the failure its root prevents: a second
install against one library, a reinstall losing the undo logs, or the
migration overlap. Every entry belongs to exactly one root, and installation
entries also name their ``installation_area`` (config or state directory).

The snapshot boundary (KTD21b): each library-scoped entry declares what a
restore does to it, one subdirectory per answer, so the coupled set is a
directory boundary rather than a list to keep in sync:

* ``COUPLED`` -> ``<state>/coupled/``: captured with the database and replaced
  on restore (registry, watermarks, tombstones, declines, active taxonomy,
  favorites; R30).
* ``SURVIVES_ROLLBACK`` -> ``<state>/history/``: the record of what is
  restorable; rolling it back destroys the log of restorable sessions.
* ``NEVER_RESTORED`` -> ``<state>/local/``: rolling it back loses data (the
  undo logs) or swaps the inode a live lock is held on.

U8 and U32 derive the snapshot set from this field (``coupled_state_files`` and
``snapshot_sources``), never from a hand-kept list.
"""

from __future__ import annotations

import copy
import errno
import json
import os
import sys
import tempfile
import tomllib
from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from types import MappingProxyType
from typing import Any

import tomli_w

from cratekit.core.config_base import (
    CONFIG_FILENAME,
    CURRENT_SCHEMA_VERSION,
    LIBRARY_STATE_LAYOUT_VERSION,
    TAXONOMY_TEMPLATE_KEY,
    VOLUME_IDENTITY_KEY,
    config_dir,
    installation_state_dir,
    is_inside,
    template_name_is_usable,
)
from cratekit.core.config_base import (
    ENV_CONFIG_DIR as ENV_CONFIG_DIR,
)
from cratekit.core.config_base import (
    ENV_DOWNLOAD_STAGING as ENV_DOWNLOAD_STAGING,
)
from cratekit.core.config_base import (
    ENV_ISRC_CACHE_DIR as ENV_ISRC_CACHE_DIR,
)
from cratekit.core.config_base import (
    ENV_LIBRARY_ROOT as ENV_LIBRARY_ROOT,
)
from cratekit.core.config_base import (
    ENV_PROVIDER_GATE_DIR as ENV_PROVIDER_GATE_DIR,
)
from cratekit.core.config_base import (
    ENV_STATE_DIR as ENV_STATE_DIR,
)
from cratekit.core.config_schema import (
    BACKUP_DESTINATION_KEYS,
    LIBRARY_ROOT_TOKEN,
    PREFIX_VOLUME_IDENTITY_KEY,
    RETIRED_ADAPTER_NAMES,
    AcquisitionConfig,
    AnalysisConfig,
    BackupConfig,
    Config,
    LabelsConfig,
    LibraryConfig,
    ModulesConfig,
    NamingConfig,
    PathsConfig,
    PrefixMapping,
    ProfileConfig,
    ProviderConfig,
    RecognitionConfig,
    RekordboxConfig,
    ReportsConfig,
    TaxonomyConfig,
    backup_remote_disagreement,
    backup_remote_name,
    current_adapter_name,
)
from cratekit.core.config_schema import (
    DEFAULT_DRIFT_CUT as DEFAULT_DRIFT_CUT,
)
from cratekit.core.config_schema import (
    DEFAULT_EXPORT_STALE_DAYS as DEFAULT_EXPORT_STALE_DAYS,
)
from cratekit.core.config_schema import (
    DEFAULT_INTAKE_EXPIRED_DAYS as DEFAULT_INTAKE_EXPIRED_DAYS,
)
from cratekit.core.config_schema import (
    DEFAULT_INTAKE_STALE_DAYS as DEFAULT_INTAKE_STALE_DAYS,
)
from cratekit.core.config_schema import (
    DEFAULT_LABEL_OFFER as DEFAULT_LABEL_OFFER,
)
from cratekit.core.config_schema import (
    DEFAULT_NEW_PLAYLIST_AGE_DAYS as DEFAULT_NEW_PLAYLIST_AGE_DAYS,
)
from cratekit.core.config_schema import (
    DEFAULT_OPEN_GATE_STALE_DAYS as DEFAULT_OPEN_GATE_STALE_DAYS,
)
from cratekit.core.config_schema import (
    DEFAULT_PAIR_SKIP_FOLDERS as DEFAULT_PAIR_SKIP_FOLDERS,
)
from cratekit.core.config_schema import (
    DEFAULT_PROCESSED_DIR as DEFAULT_PROCESSED_DIR,
)
from cratekit.core.config_schema import (
    DEFAULT_PROVIDER_CALLS_PER_COMMAND as DEFAULT_PROVIDER_CALLS_PER_COMMAND,
)
from cratekit.core.config_schema import (
    DEFAULT_PROVIDER_CALLS_PER_HOUR as DEFAULT_PROVIDER_CALLS_PER_HOUR,
)
from cratekit.core.config_schema import (
    DEFAULT_PROVIDER_COOLDOWN_S as DEFAULT_PROVIDER_COOLDOWN_S,
)
from cratekit.core.config_schema import (
    DEFAULT_PROVIDER_ISRC_CACHE_DAYS as DEFAULT_PROVIDER_ISRC_CACHE_DAYS,
)
from cratekit.core.config_schema import (
    DEFAULT_PROVIDER_MIN_INTERVAL_S as DEFAULT_PROVIDER_MIN_INTERVAL_S,
)
from cratekit.core.config_schema import (
    DEFAULT_PROVIDER_NIGHT_CALLS as DEFAULT_PROVIDER_NIGHT_CALLS,
)
from cratekit.core.config_schema import (
    DEFAULT_PROVIDER_NIGHT_CALLS_PER_HOUR as DEFAULT_PROVIDER_NIGHT_CALLS_PER_HOUR,
)
from cratekit.core.config_schema import (
    DEFAULT_PROVIDER_RESERVE_SHARE as DEFAULT_PROVIDER_RESERVE_SHARE,
)
from cratekit.core.config_schema import (
    DEFAULT_RECOGNITION_HOST as DEFAULT_RECOGNITION_HOST,
)
from cratekit.core.config_schema import (
    DEFAULT_RECOGNITION_MONTHLY_CALLS as DEFAULT_RECOGNITION_MONTHLY_CALLS,
)
from cratekit.core.config_schema import (
    DEFAULT_TEMPO_CEILING as DEFAULT_TEMPO_CEILING,
)
from cratekit.core.config_schema import (
    DEFAULT_TEMPO_FLOOR as DEFAULT_TEMPO_FLOOR,
)
from cratekit.core.config_schema import (
    MAX_EXPORT_STALE_DAYS as MAX_EXPORT_STALE_DAYS,
)
from cratekit.core.config_schema import (
    MAX_OPEN_GATE_STALE_DAYS as MAX_OPEN_GATE_STALE_DAYS,
)
from cratekit.core.config_schema import (
    PAIR_ORDER_EVERY_PAIR_KEY as PAIR_ORDER_EVERY_PAIR_KEY,
)
from cratekit.core.config_schema import (
    PAIR_SKIP_FOLDERS_KEY as PAIR_SKIP_FOLDERS_KEY,
)
from cratekit.core.config_schema import (
    RECOGNITION_HOST_DOMAIN as RECOGNITION_HOST_DOMAIN,
)
from cratekit.core.config_schema import (
    OutboundConfig as OutboundConfig,
)
from cratekit.core.config_validate import (
    ACKNOWLEDGMENT_KEY,
    REQUIRED_KEYS,
    _acquisition,
    _apply_env_overrides,
    _build,
    _outbound,
    derived_backup_remote,
    validate,
)
from cratekit.core.config_validate import (
    _validate_labels as _validate_labels,
)
from cratekit.core.config_validate import (
    _validate_pair_order_every_pair as _validate_pair_order_every_pair,
)
from cratekit.core.config_validate import (
    recognition_host_problem as recognition_host_problem,
)
from cratekit.core.exit_codes import Remedy as Remedy
from cratekit.core.state_files import (
    _LIBRARY_SUBDIR_BY_ROLE as _LIBRARY_SUBDIR_BY_ROLE,
)
from cratekit.core.state_files import (
    SET_WORKSPACE_DIRNAME,
    SQLITE_SIDECARS,
    STATE_FILES,
    InstallationArea,
    Medium,
    RollbackEffect,
    Sidecar,
    SnapshotRole,
    StateFile,
    StateRoot,
    config_path,
    coupled_state_files,
    library_coupled_dir,
    library_history_dir,
    library_local_dir,
    library_state_dir,
    out_of_band_effects,
    provider_gate_dir,
    rekey_records,
    sidecar_paths,
    snapshot_sources,
    state_file,
    state_files_for,
    state_path,
)

try:
    import fcntl as _fcntl_module
except ImportError:  # pragma: no cover - Windows has no fcntl
    _fcntl_module = None  # type: ignore[assignment]

# Schema version and the file name.


# Failure vocabulary: one type per remediation, so no caller parses a message
# (KTD25).
#
# ``Remedy`` is the canonical ``exit_codes.Remedy``, imported above: the six
# tokens a configuration failure names are declared there once (U329). D2
# holds, since a token is never the command a user types; only the CLI renders it.


class RemediedError(Exception):
    """An exception that always carries a structured remedy token.

    Its class's own, or one a raise names when one type covers two remediations
    (an unrecorded rekordbox pin is a ConfigInvalid with its own answer).
    """

    def __init__(self, message: str, *, remedy=None) -> None:
        super().__init__(message)
        if remedy is not None:
            self.remedy = remedy


class ConfigError(RemediedError):
    """Base for every configuration failure. Always carries a structured remedy."""

    remedy: Remedy = Remedy.FIX_CONFIG_VALUES


class ConfigMissing(ConfigError):
    """No config file exists. Remedy token: ``RUN_SETUP``."""

    remedy = Remedy.RUN_SETUP


class ConfigCorrupt(ConfigError):
    """The file exists but cannot be read as a versioned config.

    Covers unparseable TOML and an absent or non-integer ``schema_version``;
    every release writes the field, so its absence means a hand edit.
    """

    remedy = Remedy.REPAIR_CONFIG_FILE


class ConfigTooNew(ConfigError):
    """The file was written by a newer Cratekit. Migrations are forward only.

    Never downgraded, because a save could drop keys this build does not know.
    """

    remedy = Remedy.UPGRADE_CRATEKIT


class ConfigInvalid(ConfigError):
    """The config parsed but failed validation. Carries every problem, not the first."""

    remedy = Remedy.FIX_CONFIG_VALUES

    def __init__(
        self,
        problems: Sequence[str],
        *,
        path: Path | None = None,
        remedy: Remedy | None = None,
    ) -> None:
        self.problems = tuple(problems)
        self.path = path
        where = f" in {path}" if path is not None else ""
        joined = "\n".join(f"  - {p}" for p in self.problems)
        super().__init__(f"configuration is not valid{where}:\n{joined}", remedy=remedy)


class ConfigLockUnavailable(ConfigError):
    """A config write could not take the exclusive lock, so it refused.

    The job engine runs the CLI as subprocesses (KTD26), so two unsynchronized
    migrations or saves of one file would half-upgrade it or lose answers while
    reporting success (R-116).
    """

    remedy = Remedy.RETRY_WHEN_UNLOCKED


class ConfigConflict(ConfigError):
    """Two writers changed the same value while one of them was deciding.

    Raised by ``merge_changes`` only when nothing was written. Changes to
    different values are both kept; the same value changed two ways has no
    honest merge, so it refuses and names the keys. ``RUN_SETUP`` reruns the
    wizard against the document on disk now.
    """

    remedy = Remedy.RUN_SETUP

    def __init__(self, keys: Sequence[str]) -> None:
        self.keys = tuple(keys)
        super().__init__(
            f"the configuration was changed by another command while this "
            f"one was deciding, and both changed {', '.join(self.keys)}. Nothing "
            f"was written, so neither set of answers was lost."
        )


# Directory resolution: functions, never constants (Rule 1).


# The state-file inventory.


# The typed schema: frozen dataclasses, so a typo is an AttributeError at the
# call site rather than a None that travels.


# Validation collects every problem before raising.


# Dict to typed and back.


def from_dict(data: Mapping, *, path: Path | None = None) -> Config:
    """Build a validated, frozen ``Config``, or raise ``ConfigInvalid`` with all problems.

    Optional keys are merged over defaults, so a missing or unknown one
    degrades; required keys fail loudly, on a separate code path so the
    tolerant half never swallows the strict half's failures. The overrides are
    applied once, up front, so this returns the values ``validate`` judged.
    """
    data = _apply_env_overrides(data)
    problems = validate(data)  # re-applies the overrides; the operation is idempotent
    if problems:
        raise ConfigInvalid(problems, path=path)

    library_raw = dict(data.get("library") or {})
    prefix_raw = library_raw.pop("location_prefix_map", []) or []
    library = _build(
        LibraryConfig,
        library_raw,
        overrides={
            "location_prefix_map": tuple(
                PrefixMapping(
                    from_prefix=entry["from"],
                    to_prefix=entry["to"],
                    volume_id=entry.get(PREFIX_VOLUME_IDENTITY_KEY),
                )
                for entry in prefix_raw
            ),
        },
    )

    modules_raw = data.get("modules") or {}
    modules = ModulesConfig(
        explicit=MappingProxyType({k: bool(v) for k, v in sorted(modules_raw.items())})
    )

    return Config(
        schema_version=int(data["schema_version"]),
        library=library,
        paths=_build(PathsConfig, data.get("paths") or {}),
        profile=_build(ProfileConfig, data.get("profile") or {}),
        modules=modules,
        taxonomy=_build(TaxonomyConfig, data.get("taxonomy") or {}),
        naming=_build(NamingConfig, data.get("naming") or {}),
        acquisition=_acquisition(data.get("acquisition") or {}),
        analysis=_build(AnalysisConfig, data.get("analysis") or {}),
        rekordbox=_build(RekordboxConfig, data.get("rekordbox") or {}),
        # ``remote`` is derived from the destinations when the file omits it;
        # validation has checked that they name one remote.
        backup=_build(
            BackupConfig,
            data.get("backup") or {},
            overrides={"remote": derived_backup_remote(data)},
        ),
        reports=_build(ReportsConfig, data.get("reports") or {}),
        outbound=_outbound(data.get("outbound") or {}),
        recognition=_build(RecognitionConfig, data.get("recognition") or {}),
        provider=_build(ProviderConfig, data.get("provider") or {}),
        labels=_build(LabelsConfig, data.get("labels") or {}),
    )


# Forward-only migrations, applied in memory over a deep copy, validated in
# full, and only then written.

#: Every migration is ``dict -> dict`` with no I/O, which makes "a failed
#: migration leaves the original untouched" true by construction.
Migration = Callable[[dict], dict]

#: Keyed by the version the step upgrades from. Empty at schema 1; tests supply
#: their own ladder, and ``test_config_migration.py`` checks this one for gaps.
MIGRATIONS: Mapping[int, Migration] = MappingProxyType({})


def migrate(
    data: Mapping,
    *,
    current: int = CURRENT_SCHEMA_VERSION,
    migrations: Mapping[int, Migration] = MIGRATIONS,
) -> dict:
    """Upgrade a raw config dict to ``current``. Pure, forward only.

    Steps run in ascending order over a deep copy, so a step that raises leaves
    the caller's data untouched and nothing on disk, with no cleanup to fail.
    """
    found = data.get("schema_version")
    if found is None:
        raise ConfigCorrupt(
            "schema_version is missing. Cratekit has written this field since its "
            "first release, so a config without one was hand-edited rather than "
            "written by an older build, and guessing its version could migrate it "
            "with the wrong steps."
        )
    if not isinstance(found, int) or isinstance(found, bool):
        raise ConfigCorrupt(f"schema_version must be an integer, found {found!r}")
    if found > current:
        raise ConfigTooNew(
            f"this config is schema version {found}, but this build understands "
            f"up to {current}. Migrations are forward-only, and this build would "
            f"silently drop keys it does not know on the next save."
        )

    working = copy.deepcopy(dict(data))
    for version in range(found, current):
        step = migrations.get(version)
        if step is None:
            raise ConfigCorrupt(
                f"no migration is registered from schema version {version} to "
                f"{version + 1}, so a config at version {found} cannot reach "
                f"{current}. The ladder has a gap."
            )
        working = step(working)
        working["schema_version"] = version + 1
    return working


# Reading and writing.


def _read_raw(path: Path) -> dict:
    """Parse the file as TOML, or raise ``ConfigCorrupt`` naming the file and line."""
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        # No instruction in the message; the remedy token carries it (D2).
        raise ConfigMissing(f"no configuration file at {path}") from None
    except OSError as exc:
        raise ConfigCorrupt(f"{path} could not be read: {exc}") from exc
    try:
        return tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ConfigCorrupt(f"{path} is not valid TOML: {exc}") from exc


def load_from_path(
    path: Path,
    *,
    current: int = CURRENT_SCHEMA_VERSION,
    migrations: Mapping[int, Migration] = MIGRATIONS,
    write_back: bool = True,
) -> Config:
    """Read, migrate, validate, and only then write. Not memoized.

    1. parse, 2. migrate in memory over a deep copy, 3. validate the fully
    migrated data, 4. back up the original, 5. atomically replace it. No byte
    reaches disk before step 3 passes.

    The decision is made twice, the second time under the lock: the write
    re-reads and re-decides, so two processes migrating at once cannot copy
    already-migrated bytes into a backup named for an older version.
    """
    raw = _read_raw(path)
    found = raw.get("schema_version")
    migrated = migrate(raw, current=current, migrations=migrations)
    config = from_dict(migrated, path=path)

    if not write_back or found == current:
        return config

    with _write_lock(path):
        # Re-read: another process may have migrated while this one waited.
        current_raw = _read_raw(path)
        found_now = current_raw.get("schema_version")
        if found_now == current:
            # Another process did the work; rebuild from what is on disk.
            return from_dict(current_raw, path=path)

        migrated = migrate(current_raw, current=current, migrations=migrations)
        config = from_dict(migrated, path=path)
        # The backup holds the bytes about to be replaced, re-read under the
        # lock, so its name always matches its version.
        _back_up_version(path, found_now)
        atomic_write_bytes(tomli_w.dumps(migrated).encode("utf-8"), path)
    return config


def _write_lock(path: Path) -> exclusive_lock:
    """The one lock every writer of the configuration document takes, the
    migration included, so no write lands inside another's cycle (R-116).

    Never call ``load`` or ``load_from_path`` while holding it: ``flock`` locks
    belong to the open file description, so a second open from the same process
    blocks for ever. Code under the lock reads through ``_document_on_disk``.
    Also checks a write under pytest against the test root (R-926).
    """
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))


#: Where a state write may land while this process runs under pytest, set by
#: the suite's isolation fixture. None under pytest refuses every write.
_TEST_WRITE_ROOT: Path | None = None


class WriteOutsideTestRoot(RuntimeError):
    """A state write under pytest aimed outside the test's temporary root."""


def _refuse_write_outside_test_root(path: Path, *, system_temporary: bool = False) -> None:
    """Under pytest, refuse a state write that would land outside the test root.

    R-926. Reads no environment variable: it asks whether pytest is loaded and
    whether the resolved target (resolved on both sides, for macOS symlinks)
    sits under the registered root. Called from ``_write_lock``,
    ``atomic_write_bytes``, ``append_durable_bytes`` (U254) and
    ``exclusive_lock``, so every state writer is covered. ``system_temporary``,
    passed by the last three, also allows the system temporary directory for
    shipped scratch files, even with no root registered; never for the
    configuration document.
    """
    if "pytest" not in sys.modules:
        return
    root = _TEST_WRITE_ROOT
    allowed = [] if root is None else [root.resolve()]
    if system_temporary:
        allowed.append(Path(tempfile.gettempdir()).resolve())
    target = path.resolve()
    if any(is_inside(target, each) for each in allowed):
        return
    if root is None:
        raise WriteOutsideTestRoot(
            f"refused to write {path}: this process is "
            f"running under pytest and no test root is registered, so the "
            f"isolation in tests/conftest.py did not run for this test"
        )
    raise WriteOutsideTestRoot(
        f"refused to write {path}: this process is "
        f"running under pytest and the path is outside the test root {root}"
    )


def _back_up_version(path: Path, found: int) -> None:
    """Copy the bytes about to be replaced to the backup named for their version."""
    atomic_write_bytes(path.read_bytes(), path.with_name(f"{path.name}.v{found}.bak"))


_MEMO: dict[tuple, Config] = {}


def load(path: Path | None = None) -> Config:
    """The ordinary entry point: the validated config, memoized on file identity.

    Memoized on ``(path, inode, mtime, size)``; every write is an atomic replace
    that mints a new inode, so a rewritten file is never served stale. Memoized
    so callers call ``load()`` where they need a value instead of binding one at
    import.
    """
    target = config_path() if path is None else path
    try:
        st = target.stat()
        key = (str(target), st.st_ino, st.st_mtime_ns, st.st_size)
    except FileNotFoundError:
        raise ConfigMissing(f"no configuration file at {target}") from None
    if key not in _MEMO:
        _MEMO[key] = load_from_path(target)
    return _MEMO[key]


def reset_cache() -> None:
    """Drop the memo. For tests and for a process that just wrote a new config."""
    _MEMO.clear()


def save(config: Config, path: Path | None = None) -> Path:
    """Write the config atomically and return where it went.

    Refuses to write a file this module would refuse to load, so a save never
    locks a user out. Creates its directory through ``mkdir_private`` just
    before the write, never at import.

    A whole-document write for a caller with no prior read; a caller that read
    and writes back uses ``update`` (R-116). Nothing under ``src/`` outside this
    module calls ``save``, which ``tests/test_config_update.py`` guards.
    """
    target = config_path() if path is None else path
    problems = validate(config.to_toml_dict())
    if problems:
        raise ConfigInvalid(problems, path=target)
    # Created under the lock, so a refused write leaves no directory behind.
    with _write_lock(target):
        mkdir_private(target.parent)
        atomic_write_bytes(config.to_toml_bytes(), target)
    reset_cache()
    return target


def _document_on_disk(path: Path) -> tuple[dict, int | None]:
    """The document as it is now, and the schema version its bytes carry.

    For code holding the write lock: migrates in memory and never writes. The
    same three shapes the setup wizard reads, so first and second reads compare
    like with like:

    * no file: an empty document and no version;
    * a file that loads: its effective form, as ``load().to_toml_dict()``;
    * a file that parses but is incomplete: the migrated raw document.

    A corrupt or newer file raises, so nothing is written over it.
    """
    try:
        raw = _read_raw(path)
    except ConfigMissing:
        return {}, None
    migrated = migrate(raw)
    try:
        return from_dict(migrated, path=path).to_toml_dict(), raw["schema_version"]
    except ConfigInvalid:
        return migrated, raw["schema_version"]


def update(
    revise: Callable[[dict], Mapping], path: Path | None = None
) -> tuple[Config, Path]:
    """The configuration read-modify-write, as one locked cycle every writer uses.

    Take the lock, read the document on disk, hand it to ``revise``, validate,
    write, release. Returns the written configuration and its path.

    The caller decides outside the lock as slowly as it likes; ``revise`` is the
    re-decision under the lock against what is actually there, which may hold
    another command's answers (R-116). ``revise`` must not prompt, since it
    holds the lock; it computes or raises, and a raise writes nothing.

    An unmigrated document gets the same version backup a migration writes.
    """
    target = config_path() if path is None else path
    with _write_lock(target):
        current, found = _document_on_disk(target)
        config = from_dict(revise(current), path=target)
        # Judge the serialized form, which is what the next load reads.
        problems = validate(config.to_toml_dict())
        if problems:
            raise ConfigInvalid(problems, path=target)
        if found is not None and found != CURRENT_SCHEMA_VERSION:
            _back_up_version(target, found)
        atomic_write_bytes(config.to_toml_bytes(), target)
    reset_cache()
    return config, target


#: What a leaf holds when the key is absent, since TOML has no null.
_ABSENT = object()


def _leaves(document: Mapping, prefix: tuple[str, ...] = ()) -> dict[tuple[str, ...], object]:
    """Every value in a document that is not itself a table, by its full path.

    A list is a leaf, including a list of tables: ``library.location_prefix_map``
    is ordered and its entries have no identity to merge by, so it is one answer.
    """
    found: dict[tuple[str, ...], object] = {}
    for key, value in document.items():
        if isinstance(value, Mapping):
            found.update(_leaves(value, (*prefix, key)))
        else:
            found[(*prefix, key)] = value
    return found


def merge_changes(base: Mapping, desired: Mapping, current: Mapping) -> dict:
    """``current`` with the changes between ``base`` and ``desired`` laid over it.

    ``base`` is the caller's first read, ``desired`` what it would write, and
    ``current`` what ``update`` found under the lock. Only leaves the caller
    changed are applied, so a value merely carried through cannot overwrite
    another writer's. A leaf both changed to different values raises
    ``ConfigConflict`` naming every such key; the same value is agreement.
    """
    if current == base:
        return copy.deepcopy(dict(desired))
    before, after, now = _leaves(base), _leaves(desired), _leaves(current)
    merged = copy.deepcopy(dict(current))
    conflicts: list[str] = []
    for key in sorted({*before, *after}):
        was, wanted = before.get(key, _ABSENT), after.get(key, _ABSENT)
        if wanted == was:
            continue
        theirs = now.get(key, _ABSENT)
        if theirs != was and theirs != wanted:
            conflicts.append(".".join(key))
            continue
        node = merged
        for part in key[:-1]:
            child = node.get(part)
            if not isinstance(child, dict):
                child = node[part] = {}
            node = child
        if wanted is _ABSENT:
            node.pop(key[-1], None)
        else:
            node[key[-1]] = copy.deepcopy(wanted)
    if conflicts:
        raise ConfigConflict(conflicts)
    return merged


#: The mode every state file this package writes lands at, on every machine.
PRIVATE_FILE_MODE = 0o600

#: The mode every directory this package creates lands at. Directory write
#: permission governs unlink and rename, so a 0600 file in a 0777 directory can
#: be replaced by any local account.
PRIVATE_DIR_MODE = 0o700

#: True when this platform has POSIX modes, probed once for every call site.
_CAN_SET_MODE = hasattr(os, "chmod")


def mkdir_private(path: Path) -> None:
    """Create ``path`` and any missing parent, owner-only, on any umask.

    Not ``Path.mkdir(mode=...)``: the umask applies to that mode, and with
    ``parents=True`` intermediate levels get 0o777. Each missing level is
    created then chmodded; levels that already existed belong to the user and
    are never touched. Degrades to a plain mkdir without POSIX modes (R1, KTD6).
    """
    if path.is_dir():
        return
    for level in [*reversed(path.parents), path]:
        if level.is_dir():
            continue
        try:
            level.mkdir()
        except FileExistsError:
            # Another process created it, so it is not ours to re-mode.
            continue
        if _CAN_SET_MODE:
            os.chmod(level, PRIVATE_DIR_MODE)


def atomic_write_bytes(payload: bytes, path: Path, *, mode: int = PRIVATE_FILE_MODE) -> None:
    """Write ``payload`` to ``path`` atomically at an explicit mode, or not at all.

    Atomic: the temp file is in the target's directory so ``os.replace`` is a
    same-filesystem rename, and it is fsynced first so a crash cannot leave a
    correctly named file with unwritten contents.

    0600 regardless of umask, by an explicit chmod. This is the shared writer
    for every state file, with :func:`append_durable_bytes` for appends, so no
    state file inherits the umask. Its directory goes through ``mkdir_private``,
    since a world-writable directory makes the file's mode meaningless.
    """
    _refuse_write_outside_test_root(path, system_temporary=True)
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if _CAN_SET_MODE:  # guarded: a POSIX mode is meaningless on some platforms
            os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def append_durable_bytes(payload: bytes, path: Path) -> None:
    """Append ``payload`` to the existing file at ``path`` and sync it, or raise.

    The second shared state writer, for a ledger that grows a record at a time
    (U254), so N records cost N bytes rather than N squared.

    Not atomic: a kill can leave a torn last line, so a caller appends whole
    lines under its own lock and reads a torn last line as a record that did
    not land. Never creates the file; the first write goes through
    :func:`atomic_write_bytes` for its mode. Synced before it returns, and
    refused outside the test root like every state writer.
    """
    _refuse_write_outside_test_root(path, system_temporary=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
    try:
        view = memoryview(payload)
        while view:
            view = view[os.write(fd, view) :]
        os.fsync(fd)
    finally:
        os.close(fd)


#: The request that empties the drive's own write cache as well as the
#: operating system's, or None where a plain sync is the strongest flush. On
#: macOS ``fsync`` returns with the bytes possibly still in the drive cache;
#: ``F_FULLFSYNC`` does not. A capture asks for it (U272), since the restore
#: point usually lives on an external drive.
_FULL_FLUSH: int | None = getattr(_fcntl_module, "F_FULLFSYNC", None)

#: What a filesystem answers when it has no full flush to give. Every other
#: error is a flush that failed, and raises.
_FULL_FLUSH_UNSUPPORTED = frozenset({errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.ENOTTY})


def _full_flush(fd: int, operation: int) -> None:
    """Ask for the full flush on one descriptor. A seam, so the suite drives both answers."""
    _fcntl_module.fcntl(fd, operation)


def flush_to_disk(path: Path) -> None:
    """Flush one file's or one directory's contents and entries to the device, or raise.

    The third durability primitive, for bytes another writer put on disk, such
    as a ``shutil`` copy (U272). A directory is flushed too, since an unflushed
    directory loses a new file's entry.

    Uses the full flush where the platform has one (``_FULL_FLUSH``), falling
    back to the plain sync where the filesystem does not support it, as SQLite
    does. Nothing else is swallowed, because the caller records a verdict on
    this returning; unlike the directory flush in ``core/jobs.py``.
    """
    if os.name == "nt" and Path(path).is_dir():  # pragma: no cover - needs Windows
        # A directory cannot be opened for a flush on Windows, and NTFS
        # journals the entries a flush of one would make durable.
        return
    fd = os.open(path, os.O_RDONLY)
    try:
        _flush_descriptor(fd)
    except OSError as exc:
        # A descriptor's error names no file, so name it for the person.
        if exc.filename is not None:
            raise
        raise OSError(exc.errno, exc.strerror or str(exc), str(path)) from exc
    finally:
        os.close(fd)


def _flush_descriptor(fd: int) -> None:
    """The full flush where there is one, the plain sync where it is unsupported."""
    if _FULL_FLUSH is not None:
        try:
            _full_flush(fd, _FULL_FLUSH)
            return
        except OSError as exc:
            if exc.errno not in _FULL_FLUSH_UNSUPPORTED:
                raise
    os.fsync(fd)


class exclusive_lock:
    """An exclusive advisory lock that refuses rather than proceeding unlocked.

    Two ``crate`` subprocesses (KTD26) migrating one file at once would leave it
    half-upgraded.

    The lock file persists after release on purpose: unlinking the name lets a
    second process lock a fresh inode while the first still holds the old one,
    and both believe they hold the only lock. It is created 0600 inside a 0700
    directory, so no other account can hold or truncate it.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.handle = None

    def __enter__(self):
        _refuse_write_outside_test_root(self.path, system_temporary=True)
        mkdir_private(self.path.parent)
        try:
            import fcntl

            # os.open at 0600 rather than the builtin open(), which creates at
            # 0666 masked by the umask.
            fd = os.open(self.path, os.O_CREAT | os.O_RDWR, PRIVATE_FILE_MODE)
            self.handle = os.fdopen(fd, "r+b")
            if _CAN_SET_MODE:
                # O_CREAT sets the mode only on creation; an older lock file
                # may still be 0666.
                os.chmod(self.path, PRIVATE_FILE_MODE)
            fcntl.flock(self.handle, fcntl.LOCK_EX)
        except (ImportError, OSError) as exc:
            if self.handle is not None:
                self.handle.close()
                self.handle = None
            raise ConfigLockUnavailable(
                f"could not take an exclusive lock on {self.path} ({exc}). A "
                f"config write refuses rather than running unsynchronized, "
                f"because two processes writing one file leaves it half-upgraded "
                f"or erases one set of answers while reporting success."
            ) from exc
        return self

    def __exit__(self, *exc_info) -> None:
        if self.handle is not None:
            self.handle.close()
            self.handle = None


# What every state document's store did for itself, once (U298).


@contextmanager
def held(lock_path: Path, refused: Callable[[ConfigLockUnavailable], BaseException]) -> Iterator[None]:
    """Hold the exclusive lock at ``lock_path`` across one read then write cycle.

    Only the acquisition is translated, by ``refused``, into the store's own
    refusal. A failure raised by the body keeps its own identity.
    """
    lock = exclusive_lock(lock_path)
    try:
        lock.__enter__()
    except ConfigLockUnavailable as exc:
        raise refused(exc) from exc
    try:
        yield
    finally:
        lock.__exit__(None, None, None)


@contextmanager
def lock_within(
    lock_path: Path, *, wait_s: float, poll_s: float, sleep: Callable[[float], None]
) -> Iterator[bool]:
    """Hold the lock at ``lock_path`` and yield True, or yield False when it was not had in time.

    For a writer that would rather skip one write than wait, a cache or a
    tally. The lock file is never unlinked, for :class:`exclusive_lock`'s reason.
    """
    try:
        mkdir_private(lock_path.parent)
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, PRIVATE_FILE_MODE)
    except OSError:
        yield False
        return
    try:
        try:
            import fcntl  # noqa: PLC0415 - POSIX only, see the except
        except ImportError:  # pragma: no cover - no advisory locks here
            fcntl = None
        had = fcntl is None
        polls = 0
        while not had and polls * poll_s < wait_s:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                had = True
            except BlockingIOError:
                polls += 1
                sleep(poll_s)
        yield had
    finally:
        os.close(fd)  # closing the descriptor releases the lock; the file stays


def lock_now(path: Path) -> tuple[Any, bool]:
    """Open the lock file at ``path`` and take its lock without waiting.

    Returns the open handle, whose close releases the lock, and whether the lock
    was had. A lock held elsewhere is ``False`` with the handle open, so the
    caller can quote the holder's words from the file. Opened at 0600 through
    ``os.open``. A platform with no advisory locks reads as had. On any other
    failure the handle is closed and the failure leaves as itself.
    """
    mkdir_private(path.parent)
    handle = os.fdopen(os.open(path, os.O_CREAT | os.O_RDWR, PRIVATE_FILE_MODE), "r+")
    try:
        try:
            import fcntl  # noqa: PLC0415 - POSIX only, see the except
        except ImportError:  # pragma: no cover - POSIX only in practice
            return handle, True
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return handle, False
    except BaseException:
        handle.close()
        raise
    return handle, True


def flock_exclusive(target: Path, harden: Callable[[Path], None]):
    """Open ``target`` owner only, harden it, and take its exclusive lock.

    Returns the open handle, whose close releases the lock. On any failure,
    an interrupt included, the handle is closed and the failure leaves as
    itself. Opened at 0600 through ``os.open`` (P1). ``harden`` is the caller's,
    since ``O_CREAT`` sets the mode only on creation.
    """
    handle = None
    try:
        import fcntl  # noqa: PLC0415 - POSIX only; the caller turns its absence into a refusal

        descriptor = os.open(target, os.O_CREAT | os.O_RDWR, PRIVATE_FILE_MODE)
        handle = os.fdopen(descriptor, "r+b")
        harden(target)
        fcntl.flock(handle, fcntl.LOCK_EX)
    except BaseException:
        if handle is not None:
            handle.close()
        raise
    return handle


def read_bytes_if_present(path: Path) -> bytes | None:
    """A state file's bytes, or None when there is no file.

    Any other read failure leaves as its ``OSError`` for the caller to refuse.
    """
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def read_json(path: Path, unusable: Callable[[str], BaseException]) -> tuple[bool, Any]:
    """Whether a state document exists at ``path``, and what it parses to.

    A document that exists and cannot be read is refused, never read as empty,
    or the next write would persist the emptiness. ``unusable`` builds the
    store's refusal from a clause. An absent file is ``(False, None)``.
    """
    if not path.exists():
        return False, None
    try:
        return True, json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise unusable("it could not be opened") from exc
    except ValueError as exc:
        raise unusable("it is not JSON") from exc


def read_json_map(path: Path, unusable: Callable[[str], BaseException]) -> Mapping[str, Any] | None:
    """:func:`read_json` for a document that must be a map, None when the file is absent.

    Any other top level is refused, since read as empty it would be deleted by
    the next write.
    """
    found, raw = read_json(path, unusable)
    if not found:
        return None
    if not isinstance(raw, Mapping):
        raise unusable(f"the document is a {type(raw).__name__}, not a map")
    return raw


def read_json_as_text(path: Path, unusable: Callable[[str], BaseException]) -> tuple[bool, Any]:
    """:func:`read_json`, for the two stores that read the file in the platform's encoding.

    Kept apart because a file that is not text in that encoding leaves here as
    a ``UnicodeDecodeError`` rather than being refused as not JSON.
    """
    if not path.exists():
        return False, None
    try:
        text = path.read_text()
    except OSError as exc:
        raise unusable("it could not be opened") from exc
    try:
        return True, json.loads(text)
    except ValueError as exc:
        raise unusable("it is not JSON") from exc


__all__ = [
    "ACKNOWLEDGMENT_KEY", "BACKUP_DESTINATION_KEYS", "CONFIG_FILENAME", "CURRENT_SCHEMA_VERSION",
    "LIBRARY_ROOT_TOKEN", "LIBRARY_STATE_LAYOUT_VERSION", "MIGRATIONS", "PRIVATE_DIR_MODE",
    "PRIVATE_FILE_MODE", "REQUIRED_KEYS", "RETIRED_ADAPTER_NAMES", "SET_WORKSPACE_DIRNAME",
    "SQLITE_SIDECARS", "STATE_FILES", "TAXONOMY_TEMPLATE_KEY", "VOLUME_IDENTITY_KEY",
    "AcquisitionConfig", "AnalysisConfig", "BackupConfig", "Config", "ConfigConflict",
    "ConfigCorrupt", "ConfigError", "ConfigInvalid", "ConfigLockUnavailable", "ConfigMissing",
    "ConfigTooNew", "InstallationArea", "LibraryConfig", "Medium", "Migration", "ModulesConfig",
    "NamingConfig", "PathsConfig", "PrefixMapping", "ProfileConfig", "RekordboxConfig",
    "RemediedError", "Remedy", "RollbackEffect", "Sidecar", "SnapshotRole", "StateFile",
    "StateRoot", "TaxonomyConfig", "append_durable_bytes", "atomic_write_bytes",
    "backup_remote_disagreement", "backup_remote_name", "derived_backup_remote", "config_dir",
    "config_path", "coupled_state_files", "current_adapter_name", "flush_to_disk", "from_dict",
    "installation_state_dir", "library_coupled_dir", "library_history_dir", "library_local_dir",
    "library_state_dir", "load", "load_from_path", "merge_changes", "migrate", "exclusive_lock",
    "flock_exclusive", "held", "is_inside", "lock_now", "lock_within", "mkdir_private",
    "out_of_band_effects", "provider_gate_dir", "read_bytes_if_present", "read_json",
    "read_json_as_text", "read_json_map", "rekey_records", "reset_cache", "save", "sidecar_paths",
    "snapshot_sources", "state_file", "state_files_for", "state_path", "template_name_is_usable",
    "update", "validate",
]
