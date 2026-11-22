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
import hashlib
import json
import math
import os
import re
import sys
import tempfile
import tomllib
from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field, fields, is_dataclass, replace
from datetime import date
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any

import platformdirs
import tomli_w

from cratekit.core import profiles

try:
    import fcntl as _fcntl_module
except ImportError:  # pragma: no cover - Windows has no fcntl
    _fcntl_module = None  # type: ignore[assignment]

# Schema version and the file name.

#: The schema this build writes. Bumped only with a ``MIGRATIONS`` entry;
#: ``test_config_migration.py`` fails on a gap.
CURRENT_SCHEMA_VERSION = 1

#: The on-disk shape of the library state directory, separate from
#: ``CURRENT_SCHEMA_VERSION`` because ``MIGRATIONS`` is dict to dict and cannot
#: move a file. Nothing migrates a library state directory yet, as no build ever
#: wrote another shape. The unit that bumps this owns a one-time reconciliation
#: under the migration lock, idempotent and refusing rather than half-moving;
#: ``tests/test_config.py`` fails a bump without one.
LIBRARY_STATE_LAYOUT_VERSION = 1

CONFIG_FILENAME = "config.toml"

#: The key U31's destructive-operation assertion reads (R38), named here so a
#: guard never hardcodes the name of what it guards.
VOLUME_IDENTITY_KEY = "library.volume_id"

#: The key naming which shipped taxonomy template a library adopted (S6).
#: Only its shape is validated here; membership belongs to the taxonomy module
#: a layer above, so the wizard and doctor enforce it. A path-shaped value is
#: refused because the reader composes it into a packaged resource name.
TAXONOMY_TEMPLATE_KEY = "taxonomy.template"

#: A shipped template's short name: a bare token, never a path fragment.
_TEMPLATE_NAME_SHAPE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def template_name_is_usable(value: object) -> bool:
    """Whether ``value`` is a shape this configuration can carry as a template name.

    Public so the packaged template walker applies the same rule and never
    offers a name configuration would reject.
    """
    return isinstance(value, str) and bool(_TEMPLATE_NAME_SHAPE.match(value))

# Environment overrides. Each relocates a configured value and none supplies
# one, so a machine with no setup can never resolve a library root from the
# environment and write to the wrong volume (R38). They are applied in one
# place, ``_apply_env_overrides``, before any rule is decided, so validation and
# the builder see the same root. Relocating the root also re-bases a db_path
# under it, which is what keeps tests off the real rekordbox database.
ENV_CONFIG_DIR = "CRATEKIT_CONFIG_DIR"
ENV_STATE_DIR = "CRATEKIT_STATE_DIR"
ENV_LIBRARY_ROOT = "CRATEKIT_LIBRARY_ROOT"

#: The directory the ISRC cache and its lock live in, when set (U206). A copy
#: run points it at the live state directory so catalogue answers are not paid
#: for twice; ``core.rehearsal`` does that for every rehearsal.
ENV_ISRC_CACHE_DIR = "CRATEKIT_ISRC_CACHE_DIR"

#: The directory the provider gate's state file and its lock live in, when set
#: (U278). Unset, they live under the platform's installation state directory,
#: never under ``CRATEKIT_STATE_DIR``, so a copy run spends from the one
#: allowance the live run reads. The suite sets this to each test's own state.
ENV_PROVIDER_GATE_DIR = "CRATEKIT_PROVIDER_GATE_DIR"
ENV_DOWNLOAD_STAGING = "CRATEKIT_DOWNLOAD_STAGING"

_APP_NAME = "cratekit"


# Failure vocabulary: one type per remediation, so no caller parses a message
# (KTD25).


class Remedy(StrEnum):
    """What to do about a configuration failure, as a token rather than a command.

    D2: no foundation module holds the text a user types; only the CLI renders
    a token into a command. Part of the vocabulary U5 owns (S4).
    """

    RUN_SETUP = "run-setup"
    REPAIR_CONFIG_FILE = "repair-config-file"
    UPGRADE_CRATEKIT = "upgrade-cratekit"
    FIX_CONFIG_VALUES = "fix-config-values"
    RETRY_WHEN_UNLOCKED = "retry-when-unlocked"
    RECORD_REKORDBOX_PIN = "record-rekordbox-pin"


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


def config_dir() -> Path:
    """The installation-scoped configuration directory (KTD6, R1). Creates nothing."""
    override = os.environ.get(ENV_CONFIG_DIR)
    if override:
        return Path(override)
    return Path(platformdirs.user_config_dir(_APP_NAME))


def config_path() -> Path:
    """The path of the config file itself. Does not check that it exists.

    Resolved through ``state_path`` so the inventory and every loader and saver
    agree on one directory.
    """
    return state_path("config")


def installation_state_dir() -> Path:
    """The installation-scoped state directory, distinct from the config directory.

    Kept apart so syncing a config directory between machines never syncs one
    machine's job queue and caches.
    """
    override = os.environ.get(ENV_STATE_DIR)
    if override:
        return Path(override)
    return Path(platformdirs.user_state_dir(_APP_NAME))


def provider_gate_dir() -> Path:
    """Where the provider gate's two files live: ``CRATEKIT_PROVIDER_GATE_DIR``
    when set, else the platform's installation state directory (U278).

    Not :func:`installation_state_dir`, which follows ``CRATEKIT_STATE_DIR`` into
    a copy run's scratch; the account has one allowance, so there is one gate.
    """
    override = os.environ.get(ENV_PROVIDER_GATE_DIR)
    if override:
        return Path(override)
    return Path(platformdirs.user_state_dir(_APP_NAME))


#: The state entries resolved under :func:`provider_gate_dir` rather than under
#: their root's directory (U278). Resolved here, inside :func:`state_path`, so
#: the gate, a report, doctor and a rehearsal's copy all get one answer.
_PROVIDER_GATE_KEYS = frozenset({"provider_gate", "provider_gate_lock", "night_budget"})


def library_state_dir(config: Config) -> Path:
    """The library-scoped state root: a dot-directory beside the library.

    Beside it so the state travels and is snapshotted with the library (KTD21b)
    and is reachable from a second installation and the old system.
    """
    return config.library.root / config.library.state_dirname


def library_coupled_dir(config: Config) -> Path:
    """The one directory a KTD21b snapshot copies and a restore replaces.

    Holds exactly the ``COUPLED`` entries; ``tests/test_config.py`` asserts both
    halves.
    """
    return library_state_dir(config) / _LIBRARY_SUBDIR_BY_ROLE[SnapshotRole.COUPLED]


def library_history_dir(config: Config) -> Path:
    """Where the record of what is restorable lives: the session log and snapshots.

    Outside the coupled directory, so a snapshot never nests earlier snapshots
    and a restore never destroys the log of restorable sessions.
    """
    return library_state_dir(config) / _LIBRARY_SUBDIR_BY_ROLE[SnapshotRole.SURVIVES_ROLLBACK]


def library_local_dir(config: Config) -> Path:
    """Library state a restore must never touch: locks, undo logs, caches, calibration.

    Rolling an undo log back loses the only copy of an overwritten value, and
    replacing a directory holding a lock swaps the inode the live lock is on.
    """
    return library_state_dir(config) / _LIBRARY_SUBDIR_BY_ROLE[SnapshotRole.NEVER_RESTORED]


# The state-file inventory.


class StateRoot(StrEnum):
    """Which of the two roots an entry lives under. There are only two."""

    INSTALLATION = "installation"
    LIBRARY = "library"


class InstallationArea(StrEnum):
    """Which physical directory an installation entry lives in.

    Not a third KTD21 root: the installation root spans the platform's config
    and state directories, which coincide on macOS and differ elsewhere. Read
    only for installation entries; library entries keep the default, and
    ``tests/test_config.py`` asserts it.
    """

    CONFIG = "config"
    STATE = "state"


class SnapshotRole(StrEnum):
    """What a KTD21b restore does to this entry. Declared, never inferred.

    Each value maps to its own subdirectory, so the boundary is a directory
    rather than a maintained list.
    """

    #: Captured with the database and replaced on restore; a restore is
    #: self-consistent only if this set is exact.
    COUPLED = "coupled"

    #: The record of what is restorable, plus the snapshots. Rolling it back
    #: destroys that record; capturing it nests every prior snapshot.
    SURVIVES_ROLLBACK = "survives-rollback"

    #: Never captured, never replaced: its rollback loses data (an undo log),
    #: its identity is live (a lock, a heartbeat), or it is installation state.
    NEVER_RESTORED = "never-restored"


class RollbackEffect(StrEnum):
    """What a COUPLED entry's records caused outside the set a restore replaces.

    A restore discards records whose effect a rollback cannot undo (a playlist
    renamed at the provider, a file written or trashed), so the two disagree
    after it lands. Declared on the entry, never listed in the reconciler, since
    a companion list drifts and an undeclared effect is silently never
    reconciled (P4). ``NONE`` is spelled so "nobody decided" and "nothing
    happens" differ; ``tests/test_restore.py`` parses the literal and requires
    every COUPLED entry to name its answer.
    """

    #: Nothing outside the coupled set. The records describe database rows.
    NONE = "none"
    #: A playlist or folder was renamed at the provider, so the marker that says
    #: "already taken" lives on somebody else's server and does not roll back.
    REMOTE_PLAYLIST_PREFIX = "remote-playlist-prefix"
    #: Audio landed on the music volume. The rows go; the bytes stay, and the
    #: next pass reads them as owned.
    DOWNLOADED_FILE = "downloaded-file"
    #: A file was moved to the Trash. Rolling the record back does not move it
    #: out, and the library then holds a row for a file nobody can open.
    TRASHED_FILE = "trashed-file"
    #: A tag was written into a file on the music volume (U23). Rolling the
    #: ledger back does not un-write the tag; the original values survive in the
    #: adoption tag revert log, which is NEVER_RESTORED for that reason.
    WRITTEN_FILE_TAG = "written-file-tag"


#: One subdirectory per role, so an entry's location derives from its declared
#: role and cannot disagree with it.
_LIBRARY_SUBDIR_BY_ROLE: Mapping[SnapshotRole, str] = MappingProxyType(
    {
        SnapshotRole.COUPLED: "coupled",
        SnapshotRole.SURVIVES_ROLLBACK: "history",
        SnapshotRole.NEVER_RESTORED: "local",
    }
)


class Medium(StrEnum):
    """What the entry physically is.

    ``KEYCHAIN`` gives a disposition to state that stopped being a file (the
    refresh token), so the table stays complete.
    """

    FILE = "file"
    DIRECTORY = "directory"
    KEYCHAIN = "keychain"


@dataclass(frozen=True, slots=True)
class Sidecar:
    """A file the storage engine keeps beside an entry, named by a suffix.

    Declared on the schema rather than in the snapshot unit, since a companion
    list drifts. SQLite in WAL mode keeps committed transactions in ``<db>-wal``
    and an index in ``<db>-shm``; copying only the declared path yields a
    database that opens cleanly and is silently behind.
    """

    suffix: str
    #: True when a restore writes this sidecar back out of the snapshot. A
    #: restore removes the live ``-wal`` and ``-shm`` first, then restores only
    #: ``-wal``: the index derives from the log, and a stale one beside a fresh
    #: log gives SQLite two views of one database.
    restored: bool


#: The sidecars a SQLite database file travels with. Suffixes, not paths: they
#: are composed onto whatever path the user's rekordbox install chose.
SQLITE_SIDECARS: tuple[Sidecar, ...] = (
    Sidecar(suffix="-wal", restored=True),
    Sidecar(suffix="-shm", restored=False),
)


@dataclass(frozen=True, slots=True)
class StateFile:
    """One state entry, its root, what a restore does to it, and why.

    ``why`` is phrased as a failure (second install, reinstall, migration
    overlap) so it is checkable. ``snapshot`` has no default, so no entry is
    added without deciding whether a restore rolls it back.
    """

    key: str
    root: StateRoot
    medium: Medium
    relative: str
    why: str
    #: What a KTD21b restore does to this entry. Required.
    snapshot: SnapshotRole
    #: Which physical installation directory this lives in. Read only when
    #: ``root is StateRoot.INSTALLATION``.
    installation_area: InstallationArea = InstallationArea.STATE
    #: True when the ported shape keys records on a display name, which R19 and
    #: D5 forbid; the owning unit runs ``rekey_records`` before first use.
    rekey_from_display_name: bool = False
    #: True when the entry sits at the library root, for things another system
    #: must find without knowing Cratekit's layout.
    at_library_root: bool = False
    #: Files sharing this entry's path with a suffix, captured with it as one
    #: matched set. Any may be absent (a checkpointed or non-WAL database), and a
    #: consumer must treat absence as normal.
    sidecars: tuple[Sidecar, ...] = ()
    #: True when this entry is an R35 and R36 decision store, a revocable set of
    #: suppressions ``core.review`` reads as one document. Declared here so the
    #: review module never keeps its own list (P3).
    decision_store: bool = False
    #: What this entry's records caused outside the set a restore replaces (see
    #: :class:`RollbackEffect`); empty unless COUPLED. A tuple, because one record
    #: can reach out in several directions that are repaired separately.
    rollback_effects: tuple[RollbackEffect, ...] = ()


def _installation(
    key: str,
    relative: str,
    why: str,
    *,
    medium: Medium = Medium.FILE,
    area: InstallationArea = InstallationArea.STATE,
    **extra: Any,
) -> StateFile:
    """An installation entry. Never restored: a library snapshot covers a library."""
    return StateFile(
        key=key,
        root=StateRoot.INSTALLATION,
        medium=medium,
        relative=relative,
        why=why,
        snapshot=SnapshotRole.NEVER_RESTORED,
        installation_area=area,
        **extra,
    )


def _library(
    key: str,
    relative: str,
    snapshot: SnapshotRole,
    why: str,
    *,
    medium: Medium = Medium.FILE,
    **extra: Any,
) -> StateFile:
    """A library entry, with what a restore does to it."""
    return StateFile(
        key=key,
        root=StateRoot.LIBRARY,
        medium=medium,
        relative=relative,
        why=why,
        snapshot=snapshot,
        **extra,
    )


STATE_FILES: tuple[StateFile, ...] = (
    # Installation-scoped. All NEVER_RESTORED: a library snapshot never rolls
    # back the machine's own state.
    _installation(
        "config", CONFIG_FILENAME,
        "Config records decisions about THIS machine: which library is "
        "mounted where, which adapter, which modules. Two machines "
        "legitimately answer those differently for one library, so a shared "
        "config would force one machine's mount path onto the other.",
        # The config directory, which differs from the state directory off macOS.
        area=InstallationArea.CONFIG,
    ),
    _installation(
        "credentials", "",
        "Was a plaintext env file whose 0600 came from the author's umask "
        "rather than from any code, so on a machine with a laxer umask it "
        "landed world readable. A credential is an account fact, not a "
        "library fact: the same account serves every library, and no library "
        "should carry a credential a second user of that library can read.",
        medium=Medium.KEYCHAIN,
    ),
    _installation(
        "provider_session", "",
        "A long-lived refresh token written by a third-party library that "
        "does no chmod at all. Stored as ONE blob under one key so the token, "
        "its refresh token, and the session fields cannot be updated apart "
        "and leave a half-refreshed session that authenticates once and then "
        "fails in a way that looks like a service outage.",
        medium=Medium.KEYCHAIN,
    ),
    _installation(
        "provider_folder_cache", "provider_folder_cache.json",
        "Remote folder identifiers keyed by year. It describes the remote "
        "ACCOUNT, not the library, and a second install that loses it "
        "re-derives it on the next run at the cost of one API call.",
    ),
    _installation(
        "identify_usage", "identify_usage.json",
        "The monthly call counter for the identification service. It is "
        "bound to the CREDENTIAL's quota, not to a library: two libraries "
        "identified on one account share one quota, so one counter beside "
        "the credential is the only placement that can tell the truth.",
    ),
    _installation(
        "identify_usage_lock", "identify_usage.lock",
        "A sibling lock serializing the read-modify-write of the counter "
        "beside it. It follows its file to the same root by necessity: a lock "
        "under a different root than the thing it protects is a lock two "
        "processes can each hold while both edit the same file.",
    ),
    _installation(
        "provider_gate", "provider_gate.json",
        "The streaming provider's pacing state (R-705): when the last call "
        "went out, how many rate limit answers came back in a row, when the "
        "breaker tripped and when its cooldown lifts, and the running call "
        "totals, and each identity's calls in the last hour (U278). It "
        "describes the ACCOUNT's allowance, not a library: two libraries "
        "swept on one account share one limit, so one file beside the "
        "credential is the only placement that can tell the truth. Resolved "
        "under provider_gate_dir, never under a redirected state directory, "
        "so a copy run spends from the same allowance as the live run.",
    ),
    _installation(
        "provider_gate_lock", "provider_gate.lock",
        "The one call at a time lock over the streaming provider, held for "
        "the whole of each call so two drivers never have a request in "
        "flight together. It follows its file to the same root by necessity: "
        "a lock under a different root than the state it protects is a lock "
        "two processes can each hold while both pace off the same account.",
    ),
    _installation(
        "night_budget", "night_budget.json",
        "What the night pass has spent of its night's budget (U293): the "
        "night, the calls its finished firings made, and the gate's running "
        "total when a firing began, written before its first call so a run "
        "that died is still charged. A fact about the ACCOUNT's allowance, "
        "so it sits beside the gate under provider_gate_dir and a copy run "
        "reads the same night.",
    ),
    _installation(
        "night_status", "night_status.json",
        "The last night pass's one line of status and what it stopped on "
        "(U293), which crate doctor shows and crate sync night --last "
        "prints. It describes this installation's last unattended run, "
        "not a library, and losing it loses only the line.",
    ),
    _installation(
        "schedule_log", "schedule/sync-night.log",
        "What the scheduled night pass printed (U295): launchd appends the "
        "agent's output and errors here, the one place a night that never "
        "reached its own record says why. It describes this installation's "
        "schedule, not a library, and losing it loses only the output.",
    ),
    _installation(
        "staging_lock", "staging.lock",
        "One pass stages at a time (U293): crate sync land, crate label "
        "sync --go and crate sync night hold it for the whole of a run, so "
        "the night pass and a pass by hand never download into the one "
        "staging folder together; crate schedule install and remove hold "
        "it around their bootout (U295), so they never end a night pass. The kernel releases it when its holder "
        "dies; the holder written inside is for the refusal's words.",
    ),
    _installation(
        "isrc_cache", "isrc_cache.json",
        "What the streaming provider answered for an ISRC, by ISRC and "
        "country, and when it was asked (U206). A fact about the provider's "
        "CATALOGUE, not about a library, so it sits beside the pacing state "
        "and a copy run that redirects the library's state shares it with "
        "the live run. Losing it costs calls and no data: the next lookup "
        "asks again.",
    ),
    _installation(
        "isrc_cache_lock", "isrc_cache.lock",
        "A sibling lock serializing the read, merge and replace of the ISRC "
        "cache beside it, so two processes never lose each other's answers. "
        "It follows its file to the same root by necessity: a lock under a "
        "different root than the thing it protects is a lock two processes "
        "can each hold while both edit the same file.",
    ),
    _installation(
        "catalogue_refusals", "catalogue_refusals.json",
        "When each record shop began refusing this client, and its latest "
        "refusal (U284), so a sweep's report and the refusal a sync pass "
        "stops on can say how long a catalogue has refused. A fact about "
        "this machine's client, not about a library. Losing it costs the "
        "date and nothing else: the next refusal starts it again.",
    ),
    _installation(
        "catalogue_refusals_lock", "catalogue_refusals.lock",
        "A sibling lock serializing the read, merge and replace of the "
        "catalogue refusal record beside it, so two sweeps never lose each "
        "other's dates. It follows its file to the same root by necessity, "
        "for the ISRC cache lock's reason.",
    ),
    _installation(
        "identify_cache", "identify_cache",
        "What the identification service answered about one recording, one "
        "document per recording, named by a digest of the recording's bytes "
        "and its chunk plan. An answer is a fact about the AUDIO and was paid "
        "for on the credential's quota, so it sits beside the counter and "
        "serves every library. Losing it costs money and no data: the next "
        "pass over that recording pays for every chunk again.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "mix_scratch", "mix_scratch",
        "Where a mix fetched from a web address sits while it is identified, "
        "one folder per address, removed when the pass ends. A mix is INPUT "
        "and never library material, so this is under the installation root "
        "and never under the library: a file left beside the music is one "
        "rekordbox can be pointed at and one a library walk would index. "
        "Losing it costs a download and no data.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "genre_lookup_cache", "genre_lookup_cache.json",
        "A cache of third-party catalog lookups keyed by track. Every entry "
        "is replayable from the network, so losing it costs time and no data. "
        "It also has nothing to do with which library asked.",
    ),
    _installation(
        "label_crawl_cache", "label_crawl",
        "Half of a source directory that straddled both roots (D4). The crawl "
        "half is what a catalog lookup returned: replayable, library-agnostic, "
        "and 53 directories of it live in the source install. What actually "
        "LANDED in a library is the other half, and it is library-scoped. "
        "Since R-1091 each label's directory also holds the release reads a "
        "full label playlists build keeps, so a build stopped part way "
        "resumes; losing them costs provider calls and no data.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "label_intent", "label_intent.json",
        "Half of a file that straddled both roots (D4). This half is curated "
        "intent: the labels a user chose to follow and how deep to sweep them. "
        "In the source system the whole file is COMMITTED TO GIT, so cloning "
        "the repository hands every friend one person's label list AND their "
        "watermarks. Splitting it makes the intent half exportable on purpose "
        "and leaves the watermarks where they belong.",
    ),
    _installation(
        "label_intent_lock", "label_intent.lock",
        "The sibling lock for the curated label list. Two processes adding "
        "one label each would both read the same document, both write, and "
        "the second rename would discard the first add while reporting that "
        "it saved. NEVER_RESTORED for the inode reason every lock here "
        "shares: a restore that replaced the lock file would leave a live "
        "holder believing it still owns a file whose inode is gone.",
    ),
    _installation(
        "landing_locks", "landing_locks",
        "One lock per batch name, held by ``intake land`` across its moves "
        "(R-432). The landing engine asks whether a target is free and then "
        "renames over it, so two landings under one batch name could take "
        "each other's files and intake file with neither told. Installation "
        "scoped ON PURPOSE, against the rule that a lock follows what it "
        "protects: the library volume is commonly exFAT, where an advisory "
        "lock was never verified to hold, and a lock that silently does not "
        "exclude is worse than one a second machine cannot see. Two machines "
        "landing into one library at once is the case this gives up. "
        "NEVER_RESTORED for the inode reason every lock here shares.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "credential_index", "credential_index.json",
        "The NAMES of the credentials this installation has recorded, never "
        "their values. It exists so doctor can answer 'is a credential set' "
        "without retrieving one, which on macOS would raise the keychain's "
        "authorization prompt during a health check that is supposed to be "
        "unattended.",
    ),
    _installation(
        "credential_index_lock", "credential_index.lock",
        "A sibling lock serializing the read-modify-write of the presence "
        "index beside it, for the reason the identification counter's lock "
        "gives: a lock under a different root than the file it protects is a "
        "lock two processes can each hold while both edit that file. Measured "
        "before it existed: two processes recording one credential each left "
        "the keychain holding both and the index naming one, in 23 of 25 "
        "trials, and a lost name reads as 'not recorded', which sends a user "
        "to re-record a credential the keychain already holds.",
    ),
    _installation(
        "job_queue", "jobs",
        "KTD21 names the job queue installation-scoped, and it is: a detached "
        "job belongs to the machine running it. One consequence follows and "
        "the unit that builds the queue owns it: because the queue is per "
        "install and a library is per config, a job record must NAME the "
        "library it targets, or a queue drained after the user reconfigures "
        "runs against the wrong volume.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "backup_outcomes", "backup_outcomes",
        "What each queued backup item actually ran, one JSON file per job "
        "and item: every rclone argv and its return code (R-349). Without it "
        "a failed transfer could not be diagnosed from the job record, "
        "because the job keeps counts and a cause and the per command report "
        "left the claimed item with nowhere to go. A FAILED item writes here "
        "directly rather than through the engine's artifact commit, since a "
        "commit completes the item and a completed item is never re-armed. "
        "Installation-scoped beside the job queue it is keyed by, so job "
        "show finds it from the job identifier alone. NEVER_RESTORED for the "
        "job queue's reason: it describes one machine's work, not the library.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "backup_manifest", "backup_manifest.json.gz",
        "What the last completed file mirror left on the remote, path by "
        "path, so a backup that changed little sends only the change and one "
        "that changed nothing is skipped (U317). INSTALLATION and never "
        "library state: the library's state folder is inside the mirrored "
        "tree, so a record kept there would change the tree each time it was "
        "written and no run could skip. It names the library, the mirror and "
        "the exclude set it was kept for, and carries a token the library's "
        "files fact is published with, so a record for any other library or "
        "remote, or one a second installation or an older build has since "
        "backed up past, is not trusted: either costs one full run and never "
        "a wrong skip. NEVER_RESTORED: it describes the remote, which a "
        "restore does not roll back.",
    ),
    _installation(
        "backup_database_fingerprint", "backup_database_fingerprint.json",
        "The content fingerprint of the database set the last completed "
        "snapshot copied, so a database that has not changed since is not "
        "copied again (U317). Installation state for the manifest's reason, "
        "and keyed by the database path, the snapshot root and the library "
        "identity, so a fingerprint taken for another is not compared. "
        "NEVER_RESTORED: it describes a snapshot on the remote.",
    ),
    _installation(
        "backup_census", "backup_census.json",
        "How many files outside the library's own state folder the last "
        "completed file mirror walked, for this library root and mirror "
        "(R-1761). It is what lets a backup refuse an empty folder left "
        "where an unmounted volume was, which a full sync would otherwise "
        "empty the mirror to match. INSTALLATION for the manifest's reason, "
        "and also because the library's own state goes with the volume it "
        "would be guarding. Unlike the manifest it is NEVER removed before a "
        "transfer, so a failed run still leaves it saying what the library "
        "held. NEVER_RESTORED: it describes the remote.",
    ),
    _installation(
        "run_state", "runs",
        "One record per run, holding the gates it reached, the decisions "
        "recorded against them, and any human action still outstanding. It "
        "is what makes R33 real: a gate is answerable from a DIFFERENT "
        "process in a LATER session, which is impossible if the only place "
        "an answer can live is the invocation that hit the gate."
        " Installation-scoped alongside the job queue and for the same "
        "reason: a detached run belongs to the machine executing it, and its "
        "records name the library they target rather than assuming one."
        " NEVER_RESTORED: a run is not library content. Rolling one back "
        "would resurrect decisions a person made about work that no longer "
        "exists.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "held_plans", "runs-held",
        "One plan per run, held by a verb whose gates are answered in later "
        "commands (U209), so the gate a person answers and the write that "
        "follows use the plan the first command showed rather than planning "
        "again, which for crate sync pair over a hundred playlists cost "
        "thousands of provider calls a gate. A sibling of the run records "
        "and not inside them, because every reader of a run record would "
        "otherwise read the whole plan, and because that directory's files "
        "are each read as a run. NEVER_RESTORED for the run records' reason: "
        "a plan is about one run's work, and a rolled back one would answer "
        "for a library that moved. Losing it costs a plan, never a write: a "
        "run whose plan is not held plans again, digest bound.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "app_token", "app_token",
        "A random token minted per server start for the local control plane. "
        "It is not a service credential and must NOT survive a restart, which "
        "is exactly why it stays a file with explicit 0600 rather than "
        "joining the keychain.",
    ),
    _installation(
        "dashboard_snapshot", "dashboard_snapshot.json",
        "Last-good render numbers so a dashboard still draws when the volume "
        "is unmounted. Pure presentation cache: if it were library-scoped it "
        "would be unreadable in exactly the situation it exists to serve.",
    ),
    # Library-scoped.
    _library(
        # Composed from library.db_path, since rekordbox decides where it sits.
        "rekordbox_db", "", SnapshotRole.COUPLED,
        "The single most important piece of library-scoped state in the "
        "product, and it had no row at all: an inventory that omits it looks "
        "complete while the thing every other entry describes goes "
        "undispositioned. It is library-scoped because a database is a "
        "library, so a second installation that adopted a per-installation "
        "database would adopt a DIFFERENT library under the same name. It is "
        "COUPLED because KTD21b exists to roll it back together with the "
        "registry, watermarks, tombstones and declines that describe it; that "
        "coupling is the whole answer to the plan's top-ranked risk. Its "
        "location is constrained rather than free: see the containment rule on "
        "LibraryConfig.db_outside_root_acknowledged_on, which makes a database "
        "on another filesystem an explicit decision at setup instead of a "
        "surprise at the first snapshot.",
        # The centre of the coupled set; what reaches outside is declared by the
        # entries below.
        rollback_effects=(RollbackEffect.NONE,),
        # The only SQLite database here, so the only entry with sidecars; this
        # keeps the KTD21b capture set derived.
        sidecars=SQLITE_SIDECARS,
    ),
    _library(
        "write_lock", "write.lock", SnapshotRole.NEVER_RESTORED,
        "KTD17 and R31, non-negotiable. In the source system this is a flock "
        "on a path under the installation root while the database it protects "
        "travels with the library, so a second install holds a lock the first "
        "install cannot see and both open the database at once. During the "
        "migration overlap the old system must be able to open this exact "
        "file, which only a path beside the library can provide."
        " NEVER_RESTORED for a second reason: a restore that replaced the "
        "directory holding this file would swap the inode a live flock is "
        "held on, and every process holding the old one would keep believing "
        "it had exclusive access, with nothing raised.",
    ),
    _library(
        "session_lock", "session.lock", SnapshotRole.NEVER_RESTORED,
        "The whole-run lock, held for a destructive session end to end (R31). "
        "Same failure as the write lock: per-installation placement makes two "
        "machines mutually invisible."
        " Same inode argument as the write lock: a restore must never "
        "replace the file a live lock is held on.",
    ),
    _library(
        "session_log", "sessions", SnapshotRole.SURVIVES_ROLLBACK,
        "The per-run state machine, the frozen plans, and the created-playlist "
        "ledger. Library-scoped for two reasons: KTD21b requires a snapshot to "
        "cover the database and this log ATOMICALLY, and during the overlap a "
        "Cratekit run that cannot read the old system's log treats its crash "
        "debris as fresh intake."
        " It SURVIVES a rollback rather than being part of one: rolling the "
        "log back would erase the record of which sessions are restorable, "
        "which is the one thing a user needs in order to restore again.",
        medium=Medium.DIRECTORY,
    ),
    _library(
        "snapshots", "snapshots", SnapshotRole.SURVIVES_ROLLBACK,
        "The headline case in KTD21. Restore lives per installation in the "
        "source system while the database it restores lives per library, so a "
        "second machine simply cannot roll back the first machine's write. "
        "Beside the library, any installation can restore any session."
        " It SURVIVES a rollback for a structural reason as well as a "
        "practical one: a snapshot that captured the snapshot store would "
        "nest every previous snapshot inside the new one, and each capture "
        "would then cost the sum of every capture before it.",
        medium=Medium.DIRECTORY,
    ),
    _library(
        "favorites_state", "favorites_state.json", SnapshotRole.COUPLED,
        "It records rekordbox row identifiers that have already been colored "
        "and tagged. A second install starts from an empty list and re-applies "
        "every one of them, turning what should be a no-op run into a full "
        "guarded write session against the live database, which is the highest "
        "risk operation in the product."
        " COUPLED: the rows it names are database rows, so a restore that "
        "rolled the database back without it would leave this file claiming "
        "work that no longer exists, and the next run would skip it.",
        # The reverse half of the favorites sweep hearts a track at the
        # provider. Rolling this file back forgets that it did, and the heart
        # stays on somebody else's server.
        rollback_effects=(RollbackEffect.REMOTE_PLAYLIST_PREFIX,),
    ),
    _library(
        "favorites_state_lock", "favorites_state.lock", SnapshotRole.NEVER_RESTORED,
        "A sibling lock serializing the read-modify-write of the state file "
        "beside it. Library-scoped for the same reason its file is: a lock in "
        "a per-installation directory is invisible to a second machine, so "
        "both would edit one library's record at once."
        " NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    _library(
        "energy_calibration", "energy_calibration.json", SnapshotRole.NEVER_RESTORED,
        "Cut points fitted against THIS library's own values. KTD21 names "
        "analysis calibration library-scoped, and the reason is that losing "
        "it does not just cost a re-fit: it silently changes where the same "
        "input track routes."
        " NEVER_RESTORED: the restamp these cut points drove wrote values "
        "into files on disk, and a database restore does not roll a file "
        "write back. Rolling the cut points back alone would describe a "
        "state the files are no longer in.",
    ),
    _library(
        "energy_feature_cache", "energy_features.json", SnapshotRole.NEVER_RESTORED,
        "Per-file signal features keyed on this library's files. Losing it to "
        "a reinstall costs a full re-analysis pass over thousands of files."
        " NEVER_RESTORED: it is keyed on files, which do not roll back, and "
        "it is re-derivable, so a rollback costs a re-analysis and buys "
        "nothing.",
    ),
    _library(
        "energy_undo_log", "energy_undo.json", SnapshotRole.NEVER_RESTORED,
        "The ONLY surviving copy of each file's pre-restamp energy value, "
        "which the restamp overwrote on disk. A reinstall that loses this is "
        "unrecoverable data loss against the user's own music files, and the "
        "source system's re-rate path refuses outright when it is absent."
        " Which is exactly why a restore must never roll it back: the values "
        "it protects were written to files, a database restore does not undo "
        "a file write, and discarding the log makes those writes permanent. "
        "Rolling this back is not a stale record, it is data loss.",
    ),
    _library(
        "vocal_calibration", "vocal_calibration.json", SnapshotRole.NEVER_RESTORED,
        "The hand-set vocal cut, fitted against this library. Same failure as "
        "energy calibration: losing it changes routing outcomes for unchanged "
        "input, silently."
        " NEVER_RESTORED for the same reason as energy calibration: its "
        "effects already landed on files that do not roll back.",
    ),
    _library(
        "genre_gaps", "genre_gaps.json", SnapshotRole.NEVER_RESTORED,
        "Counts of incoming genre strings that resolved to no folder in THIS "
        "library's taxonomy. The same string is a gap in one library and a "
        "match in another, so the count is meaningless anywhere else. Note "
        "the keys are external vendor strings, not taxonomy display names, "
        "which is why R19's re-key does not apply: the whole point of the "
        "record is that the string matched nothing we own."
        " NEVER_RESTORED: a gap observed is a fact about what arrived, not "
        "about what the database holds, and re-deriving it costs a pass.",
    ),
    _library(
        "genre_tag_undo_log", "genre_tag_undo.json", SnapshotRole.NEVER_RESTORED,
        "The replay source for reverting tag writes made to files on disk, "
        "carrying each file's original value. Second undo log, same argument: "
        "a reinstall that loses it makes hundreds of on-disk tag writes "
        "permanent."
        " And the same argument against rolling it back: the writes it "
        "reverses are on disk, so a restore that discarded this log would "
        "make them permanent too.",
    ),
    _library(
        "playlist_parole_ledger", "playlist_parole.json", SnapshotRole.COUPLED,
        "First-seen dates for playlists sitting in the rotation's holding "
        "area. It describes this library's playlists and nothing else."
        " COUPLED: the playlists it dates are database rows. A restore that "
        "brought a playlist back while its first-seen date stayed at the "
        "rolled-forward value would put it straight past the rotation "
        "deadline and delete it early.",
        # First-seen dates for database rows, and nothing else leaves the
        # database.
        rollback_effects=(RollbackEffect.NONE,),
        rekey_from_display_name=True,
    ),
    _library(
        "track_provider_id_cache", "track_provider_ids.json", SnapshotRole.NEVER_RESTORED,
        "A map from file location to the provider's track identifier, keyed "
        "on THIS library's file paths. On another library every key misses, so "
        "an installation-scoped copy is a cache that can only ever be wrong "
        "or empty."
        " NEVER_RESTORED: keyed on file paths, which a database restore does "
        "not move, and re-derivable at the cost of lookups.",
    ),
    _library(
        "review_queue", "review", SnapshotRole.COUPLED,
        "KTD12's one shared adjudication surface. Its items describe "
        "candidates for THIS library, and an item adjudicated on one machine "
        "must not be re-asked on another."
        " COUPLED: an adjudicated item becomes a decline, and R30 rolls "
        "declines back. Leaving the queue behind while the declines roll "
        "back would leave an item simultaneously queued and already decided.",
        medium=Medium.DIRECTORY,
        # Items and verdicts about this library's own candidates. An item is
        # a question, and asking one changes nothing outside.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "label_outcomes", "label_outcomes", SnapshotRole.COUPLED,
        "The other half of the split directory (D4): what a label sweep "
        "actually landed in this library. Distinct from the crawl cache, which "
        "is only what a lookup returned."
        " COUPLED for the same reason the watermarks are: it is a per-source "
        "audit record of what this library took in, and R25 is meaningless "
        "if it survives a rollback of the intake it describes.",
        medium=Medium.DIRECTORY,
        # What a sweep actually landed: the audio is on the music volume and
        # the rows that named it are about to go, so the next pass reads those
        # files as owned by nobody.
        rollback_effects=(RollbackEffect.DOWNLOADED_FILE,),
    ),
    _library(
        "label_watermarks", "label_watermarks.json", SnapshotRole.COUPLED,
        "The other half of the split registry file (D4). A watermark is a "
        "per-source audit record of what this library has already taken in "
        "(R25). Committed to git in the source system, which ships one "
        "person's sweep history to everyone who clones."
        " COUPLED, named by R30: a watermark that survives a rollback of the "
        "intake it recorded makes the next sync skip exactly the tracks the "
        "restore removed.",
        # Both directions: audio landed on the volume and the provider playlist
        # was renamed with the taken marker. Neither rolls back with the rows.
        rollback_effects=(
            RollbackEffect.DOWNLOADED_FILE,
            RollbackEffect.REMOTE_PLAYLIST_PREFIX,
        ),
    ),
    _library(
        "label_watermarks_lock", "label_watermarks.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the per-label last-pulled document. Two "
        "sweeps finishing at once would both read the same years, both "
        "write, and the second rename would discard the first label's "
        "advance while reporting success. NEVER_RESTORED for the inode "
        "reason every lock here shares, and it lives under local rather "
        "than coupled so a restore cannot swap the inode a holder still "
        "has open.",
    ),
    _library(
        "label_sync", "label_sync.json", SnapshotRole.COUPLED,
        "The guided label sync's record (U107): per label, which releases a "
        "person has been asked about and when, the question waiting to be "
        "answered, and every answer given. LIBRARY scoped because what was "
        "asked depends on this library's holdings and its review queue, and "
        "a copy run redirects library state so a rehearsal cannot move the "
        "live marker. COUPLED because the record describes review rows: a "
        "restore that puts the review queue back must put the asked set "
        "back with it, or a release answered in a rolled back run is never "
        "asked again.",
        # The record describes review rows and itself. The download an answer
        # leads to is U108's, and lands as an intake whose own records declare
        # the downloaded file.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "tag_suggest_catalogue", "tag_suggest_catalogue.json", SnapshotRole.NEVER_RESTORED,
        "What the catalogues answered for each row tag suggest offered a "
        "genre for (U114), kept a week so the run that applies a plan "
        "rebuilds it from the same answers the gate showed. LIBRARY scoped "
        "because it is keyed by this library's content identifiers. NEVER "
        "RESTORED because every entry is replayable from the network: "
        "losing it costs paced lookups and no data.",
    ),
    _library(
        "label_sync_lock", "label_sync.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the guided label sync's record. An answer is "
        "a read, modify, write of one document, and a structured answer "
        "given beside an interactive run must not discard the other's. "
        "NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    _library(
        "tree_registry", "tree_registry.json", SnapshotRole.COUPLED,
        "KTD22. Cutover mode and the adopted root's identifier describe one "
        "person's library. Committing them would ship the author's flips to "
        "every friend, and would leave the old system, which cannot read the "
        "new repository, unable to consult them at all. New state: the source "
        "system has no equivalent."
        " COUPLED, and it is the entry the plan's top-ranked risk is named "
        "after: the registry rolling back while the database does not, or "
        "the reverse, is the failure KTD21b exists to make impossible.",
        # A cutover's effect is inside the database. Reconciling the tree after a
        # pre-cutover restore is a separate marker, see cratekit.core.reconcile.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "tree_registry_lock", "tree_registry.lock", SnapshotRole.NEVER_RESTORED,
        "Recording a cutover reads the registry, adds one tree's record, and "
        "writes the whole file back, because trees flip one at a time and a "
        "whole-file overwrite would erase every other tree's record. That "
        "cycle is not made atomic by the atomic rename at the end of it: two "
        "processes that both read, both add and both rename leave one flip "
        "on the floor while the call that lost it returns a registry "
        "reporting success, and a tree whose cutover was lost then takes its "
        "next write through the XML bridge, which under U9's A2 verdict "
        "replaces the database-native tree on import. Library-scoped because "
        "the registry is: a lock under the installation root is invisible to "
        "a second machine writing the same library."
        " NEVER_RESTORED for the inode reason every lock here shares, and it "
        "matters more than usual because the registry is COUPLED: a restore "
        "replaces the directory holding it, so a lock beside it would have "
        "its inode swapped under every process holding it.",
    ),
    _library(
        "routing_intents", "routing_intents.json", SnapshotRole.COUPLED,
        "Where each new track's intended placement is written down at the "
        "moment it is decided, which is long before the library holds a row "
        "for that track. It describes ONE library's files and one library's "
        "playlist rows, so a second installation inheriting it would try to "
        "place tracks that library has never seen, and a reinstall must find "
        "it beside the library rather than beside the installation that "
        "recorded it. New state: the source system decides placement and "
        "writes it in one pass and therefore has nothing to persist."
        " COUPLED, and this is the entry where the coupling is the entire "
        "point. A track is marked routed only after its membership row is "
        "committed, so a restore that rolled the membership back while the "
        "mark survived would leave a run reporting placed tracks that sit in "
        "no playlist at all, with nothing left on disk that knows to place "
        "them again.",
        # Intents and marks, both about database rows.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "routing_intents_lock", "routing_intents.lock", SnapshotRole.NEVER_RESTORED,
        "The ledger beside it accumulates several runs from several sources, "
        "and every writer of it reads, modifies and writes. Two of those "
        "interleaving erases a decision that was fully recorded, and the run "
        "that made it then closes clean over a track sitting in no playlist. "
        "Library-scoped for the same reason the write lock is: a "
        "per-installation lock is invisible to a second install and to the "
        "old system during the overlap, so neither can contend for a file "
        "that only ever had one copy."
        " NEVER_RESTORED for the inode reason the write lock records: a "
        "restore that replaced the directory holding this file would swap "
        "the inode a live lock is held on, and every process holding the old "
        "one would keep believing it had exclusive access.",
    ),
    # NONE on purpose (U32): every record describes rows inside the database a
    # restore replaces, so nothing survives a rollback to reconcile.
    _library(
        "tree_convergence", "tree_convergence.json", SnapshotRole.COUPLED,
        "R39. Three facts about THIS library's database-native trees: the "
        "fingerprint of the database as Cratekit last left it, which tree is "
        "unconverged and why, and the playlist row identifiers a previous "
        "rebuild wrote each declared destination into. All three name rows in "
        "one person's database, so a second installation inheriting them would "
        "compare its own library against another one's counts and rebuild into "
        "row identifiers it does not have. New state: the source system has no "
        "convergence concept at all, which is the gap R39 names."
        " COUPLED, and every one of the three fails differently if it is not. "
        "A fingerprint that survived a rollback would report the restore it "
        "was rolled back by as an out-of-band one, so Cratekit's own restore "
        "would mark every native tree unconverged. A node map that survived "
        "would point a rebuild at playlist rows the restore removed, and the "
        "rebuild would create them again beside the real ones. An unconverged "
        "flag that survived would outlive the damage it describes, exactly as "
        "the committed-unverified session record did before U8 gave it a way "
        "to be resolved.",
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "tree_convergence_lock", "tree_convergence.lock", SnapshotRole.NEVER_RESTORED,
        "The document beside it is read, modified and written by the rebuild, "
        "by the convergence check, and by every governed write that records a "
        "fingerprint at its close, which is several processes against one "
        "file. Two of those interleaving discards an unconverged flag that was "
        "fully recorded, and the next sync then runs over a tree nothing "
        "believes is damaged. Library-scoped because the document is: a lock "
        "under the installation root is invisible to a second machine writing "
        "the same library."
        " NEVER_RESTORED for the inode reason every lock here shares, and it "
        "matters more than usual because the document it guards is COUPLED: a "
        "restore replaces the directory holding it, so a lock beside it would "
        "have its inode swapped under every process holding it.",
    ),
    _library(
        "tombstones", "tombstones.json", SnapshotRole.COUPLED,
        "R36. A suppressed acquisition is a fact about what this library has "
        "deliberately declined to hold. New state; the source system has no "
        "equivalent, so there is nothing to port and the shape is chosen here."
        " COUPLED, named by R30.",
        # A tombstone is written when a file is removed, and removal here means
        # the Trash. The record rolls back; the file does not walk out of the
        # Trash on its own.
        rollback_effects=(RollbackEffect.TRASHED_FILE,),
        decision_store=True,
    ),
    _library(
        "declines", "declines.json", SnapshotRole.COUPLED,
        "R36's other half: candidates a human rejected. Library-scoped so the "
        "rejection is not re-asked from a second machine. New state."
        " COUPLED, named by R30, and paired with the review queue: the two "
        "roll back together or an item ends up both open and decided.",
        # A decline suppresses an acquisition that never happened, so there is
        # nothing outside to undo.
        rollback_effects=(RollbackEffect.NONE,),
        decision_store=True,
    ),
    _library(
        "decision_store_locks", "decision_locks", SnapshotRole.NEVER_RESTORED,
        "One sibling lock per decision store, serializing the read then write "
        "each of them performs on its document. Without it two processes both "
        "read the same set, both add their own record, and the second rename "
        "discards the first one's while the call that lost reports success: "
        "eight processes recording two hundred decisions left seventy one on "
        "disk. A lost record re-offers a declined file and re-acquires a "
        "tombstoned version, and a lost revocation leaves a suppression "
        "standing forever with nothing to notice it. Library-scoped for the "
        "reason the stores are: a lock in a per-installation directory is "
        "invisible to a second machine, so both would edit one library's "
        "record at once."
        " NEVER_RESTORED for the inode reason every lock here shares, and it "
        "is why this is a directory of its own rather than a file beside each "
        "store: the stores are COUPLED, so a restore replaces the directory "
        "holding them, and a lock inside it would have its inode swapped "
        "under every process holding it."
        " A DIRECTORY rather than one entry per store, so the lock a store "
        "uses is derived from the store's own key and a third decision store "
        "cannot arrive without one.",
        medium=Medium.DIRECTORY,
    ),
    _library(
        "deletion_watermark", "deletion_watermark.json", SnapshotRole.COUPLED,
        "R35. It marks how far the deletion pass has read THIS library's "
        "soft-delete markers, and the number each absent landed row was "
        "given when a pass first saw it gone (R-1037). New state."
        " COUPLED, named by R30: a deletion watermark that survives a "
        "rollback skips markers the restore put back.",
        # How far the deletion pass read. The deletions themselves are recorded
        # as tombstones above, which is where the Trash effect is declared; this
        # is a position, and a position has no effect of its own.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "deletion_watermark_lock", "deletion_watermark.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the watermark above, which is a read then a "
        "write over one document exactly as the decision stores are. "
        "``atomic_write_bytes`` makes the RENAME atomic and does nothing for "
        "the cycle around it, so two passes finishing at once both read the "
        "same watermark, both advance it from what they read, and the second "
        "rename discards the first one's advance while the call that lost "
        "reports success. What that loses is not a number: the watermark is "
        "what makes a removal HANDLED, so a dropped advance re-offers files "
        "somebody already answered for, and a dropped RE-BASELINE offers a "
        "whole library's historical removals at once. Library-scoped for the "
        "reason the watermark is: a lock in a per-installation directory is "
        "invisible to a second machine, so both would advance one library's "
        "watermark at once."
        " NEVER_RESTORED for the inode reason every lock here shares, and it "
        "is a sibling rather than a lock beside the document because the "
        "watermark is COUPLED: a restore replaces the directory holding it, "
        "and a lock inside that directory would have its inode swapped under "
        "every process holding it.",
    ),
    _library(
        "source_watermarks", "source_watermarks.json", SnapshotRole.COUPLED,
        "R25's per-source audit record of how far each increment got on THIS "
        "library. The cursor does not decide the next scope; owned-dedup "
        "does. A second install that kept the same file would report "
        "completions that never happened on this machine, and a watermark "
        "that survives a rollback of the intake it recorded would tell "
        "status a source was clean after the restore removed that intake. "
        "Distinct from label_watermarks.json, which is the per-label "
        "last-pulled document U26 owns; this file is one cursor per source id.",
        rollback_effects=(
            RollbackEffect.DOWNLOADED_FILE,
            RollbackEffect.REMOTE_PLAYLIST_PREFIX,
        ),
    ),
    _library(
        "source_watermarks_lock", "source_watermarks.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the source watermark document. Two increments "
        "finishing at once would both read the same cursors, both write, and "
        "the second rename would discard the first source's advance while "
        "reporting success. Library-scoped for the reason the document is: a "
        "lock in a per-installation directory is invisible to a second "
        "machine editing the same library. NEVER_RESTORED because the "
        "document is COUPLED and a lock inside that directory would have its "
        "inode swapped under every process holding it.",
    ),
    _library(
        "bandcamp_fetched", "bandcamp_fetched.json", SnapshotRole.NEVER_RESTORED,
        "U176. Every Bandcamp purchase this library has fetched into "
        "download staging, by purchase id, so a later run plans only what "
        "it has not taken. Kept by purchase and never as a checkpoint, "
        "because a checkpoint hides every purchase older than it, which is "
        "how a purchase filtered out once was never offered again. "
        "Library-scoped because the files it records were staged for this "
        "library. NEVER_RESTORED because what it records happened on disk "
        "and at the account, and a database restore takes back neither: "
        "rolled back, it would fetch a release again into staging beside "
        "the copy already there.",
    ),
    _library(
        "bandcamp_fetched_lock", "bandcamp_fetched.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the record above. Two fetches finishing at "
        "once would both read it, both add their purchase, and the second "
        "rename would drop the first one's, so that purchase is fetched "
        "again on the next run. NEVER_RESTORED for the inode reason every "
        "lock here shares.",
    ),
    _library(
        "sync_mark_record", "sync_marks.json", SnapshotRole.NEVER_RESTORED,
        "R-838. Which account playlists each sync pass renamed with the swept "
        "prefix, the title before and the title written, so ``sync unmark`` "
        "can put a mistaken mark back and refuse a prefix no pass of this "
        "product wrote. The title alone cannot say who wrote it."
        " NEVER_RESTORED for the undo logs' reason: the renames it records "
        "are on somebody else's server and a database restore does not undo "
        "them, so rolling the record back forgets a mark that is still there "
        "and leaves the one verb that can remove it refusing to.",
    ),
    _library(
        "sync_mark_record_lock", "sync_marks.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the mark record, which is a read then a write "
        "over one document. Two marks landing at once would both read the "
        "same record and the second rename would discard the first one's "
        "entries while reporting success. NEVER_RESTORED for the inode reason "
        "every lock here shares.",
    ),
    _library(
        "sync_unavailable_record", "sync_unavailable.json", SnapshotRole.NEVER_RESTORED,
        "U320. Which synced account playlists ``sync removed`` found absent "
        "from the account's list with their id answering not found, the first "
        "and latest time it did, and which are retired, so a playlist deleted "
        "on the account stops holding back every removal once it has answered "
        "not found a day apart or a person retired it at the gate."
        " NEVER_RESTORED for the mark record's reason: it records what "
        "somebody else's server answered, which a database restore does not "
        "undo, and rolled back it would read a deleted playlist as live again.",
    ),
    _library(
        "sync_unavailable_record_lock", "sync_unavailable.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the record above, a read then a write over one "
        "document: two runs recording at once would both read it and the "
        "second write would drop the first one's sightings. NEVER_RESTORED "
        "for the inode reason every lock here shares.",
    ),
    _library(
        "sync_artifacts", "sync_artifacts.json", SnapshotRole.COUPLED,
        "The register of every file a sync run created, written at creation "
        "time so crash debris in the staging directory cannot become the next "
        "run's intake. Library-scoped because the files describe what THIS "
        "library's run produced. COUPLED so a restore forgets registrations "
        "for intake that no longer exists, and those leftover files become "
        "debris again rather than being re-imported as if they were new.",
        rollback_effects=(RollbackEffect.DOWNLOADED_FILE,),
    ),
    _library(
        "sync_artifacts_lock", "sync_artifacts.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the artifact register. Two sources in one run "
        "register files concurrently, and an unlocked read-modify-write would "
        "drop one source's registrations, which is how crash debris becomes "
        "invisible and then looks like next-run intake. NEVER_RESTORED for "
        "the inode reason every lock here shares.",
    ),
    _library(
        "backup_ack", "backup_ack.json", SnapshotRole.NEVER_RESTORED,
        "KTD18's queue-time acknowledgment and the backup age shown when it "
        "was given. New state: the source system's backup script persists no "
        "timestamp at all, it stats the remote, so there is nothing to port. "
        "Library-scoped because the thing acknowledged is a backup of THIS "
        "library."
        " NEVER_RESTORED: the backup it acknowledges lives off this volume "
        "and a restore does not un-take it, so rolling the record back would "
        "demand the user re-acknowledge a backup that is still there.",
    ),
    _library(
        "backup_facts", "backup_facts.json", SnapshotRole.NEVER_RESTORED,
        "When each portion of THIS library was last backed up, recorded PER "
        "PORTION because the database portion refuses while rekordbox is "
        "running and the file mirror completes anyway; one aggregate "
        "timestamp would report a database that is weeks stale as fresh, "
        "which is precisely the fact R15's warning exists to carry. It is a "
        "FILE rather than a function call so R15's warning reads a fact "
        "instead of importing a toggleable module (KTD23). New state: the "
        "source system's script persists nothing and stats the remote "
        "instead, so a machine that cannot reach the remote cannot answer "
        "the question at all. Library-scoped because a second installation "
        "must see the same answer; an installation-scoped copy reports "
        "'never backed up' for a library that was backed up an hour ago "
        "from the other machine, and a warning that cries wolf is one users "
        "learn to click through."
        " NEVER_RESTORED: the backup it describes lives off this volume and "
        "a restore does not un-take it, so rolling the record back would "
        "demand a fresh backup of something that is still there.",
    ),
    _library(
        "setbuilder_index_cache", "setbuilder_index.json", SnapshotRole.NEVER_RESTORED,
        "Per-file ranking signals keyed on THIS library's file paths and "
        "modification times, so a repeat run re-reads only what changed. "
        "Every key misses against another library, which makes an "
        "installation-scoped copy a cache that can only be empty or wrong, "
        "and the whole-library tag scan it avoids costs minutes per run on a "
        "library of this size."
        " NEVER_RESTORED: it is keyed on files, which a database restore "
        "does not move, and every entry is re-derivable from the files "
        "themselves at the cost of that scan.",
    ),
    _library(
        "taxonomy_active", "taxonomy.toml", SnapshotRole.COUPLED,
        "S6. The SHIPPED default template is packaged read-only data in the "
        "wheel; the ACTIVE template is a copy made here at setup. That makes "
        "a library self-describing: a second installation or a reinstall "
        "resolves the same tree without re-answering the wizard, and a "
        "snapshot rolls the taxonomy back with the database it describes."
        " Which is to say COUPLED, explicitly: the tree in the database and "
        "the template that describes it are one decision in two files.",
        # A declaration of the tree this library means. Nothing outside the
        # database reads it.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "taxonomy_origin", "taxonomy.origin.toml", SnapshotRole.COUPLED,
        "R-689. Which shipped text the active taxonomy copy was made from: "
        "the template's short name and a digest of the packaged text setup "
        "copied. Without it a copy that fell behind the shipped template "
        "cannot be told from one a person edited, so doctor could not say "
        "why a section the shipped template gained after setup is absent "
        "from every verb. It lives beside the copy it describes and rolls "
        "back with it, because a restored older copy under a newer record "
        "would read as edited when it is not. Setup writes it once, with the "
        "copy, and never for a copy it left alone, since it cannot know "
        "where an existing copy came from.",
        # A record about the active copy. Nothing routes by it; doctor reads it.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "active_run_sentinel", ".cratekit_active_run.json", SnapshotRole.NEVER_RESTORED,
        "The one entry the source system already places beside the library, "
        "carried forward as-is rather than converted. It sits at the library "
        "ROOT rather than inside the state directory on purpose: it is an "
        "advisory cross-machine heartbeat, and a second system looking for it "
        "should not have to know this layout."
        " NEVER_RESTORED: it is a live heartbeat. Restoring one would "
        "advertise a run that ended, to a machine that would then wait for it.",
        at_library_root=True,
    ),
    _library(
        "set_workspaces", "", SnapshotRole.NEVER_RESTORED,
        "Per-set stage artifacts, already correct by accident of location in "
        "the source system: they live under the library's own sets directory "
        "beside the audio they describe. Resolved from the CONFIGURED "
        "directory names rather than from a literal, which is why its relative "
        "path is empty here and ``state_path`` composes it. It names a "
        "Cratekit-owned subdirectory INSIDE the sets directory, never the sets "
        "directory itself: that directory holds the user's own recordings, and "
        "an entry pointing at it puts the whole recordings tree into every "
        "generic pass over the inventory. A snapshot would try to copy "
        "hundreds of gigabytes of audio, a state report would list the user's "
        "music as Cratekit state, and a future 'clear this library's state' "
        "built off the inventory would target user content. NEVER_RESTORED "
        "because a stage artifact belongs to a run, not to the database.",
        medium=Medium.DIRECTORY,
    ),
    # U32's entries. New entries are appended, never inserted, so two units
    # adding entries conflict textually instead of auto-merging a duplicate key.
    _library(
        "restore_reconciliation", "restore_reconciliation.json", SnapshotRole.SURVIVES_ROLLBACK,
        "What a restore left behind that the restore itself could not undo, "
        "and whether a person has dispositioned each one. A restore rolls the "
        "database and its coupled state back together, which makes them agree "
        "with each other and says nothing about the world: the audio the "
        "discarded run downloaded is still on the volume, the playlist it "
        "renamed at the provider is still renamed, and the file it moved to "
        "the Trash is still in the Trash. Library-scoped because every one of "
        "those facts is about THIS library, and a second machine restoring "
        "the same session must see the same outstanding list rather than a "
        "clean sheet. New state: the source system has no restore that "
        "reconciles anything."
        " It SURVIVES a rollback, for the reason the session log does and "
        "one more. Rolling it back would erase the record of what is owed at "
        "exactly the moment it is owed, and a second restore run against an "
        "earlier point would wipe the first restore's outstanding list while "
        "adding its own. It also holds the unconverged trees a pre-cutover "
        "restore marks, and those must outlive every later rollback, because "
        "the rebuild that clears them has not run yet.",
    ),
    _library(
        "restore_reconciliation_lock", "restore_reconciliation.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the document above, which is read then written "
        "as one cycle by a restore recording markers and by whoever "
        "dispositions them. The rename at the end of that cycle is atomic and "
        "the cycle is not: two processes both read the same set, both add "
        "their own record, and the second rename discards the first one's "
        "while the losing call returns a record reporting success. Two units "
        "shipped exactly that bug before it was caught."
        " NEVER_RESTORED for the inode reason every lock in this inventory "
        "shares, and it matters here more than anywhere else in the file: the "
        "process that replaces directories during a restore is the process "
        "holding this lock. A lock inside a directory a restore replaces has "
        "its inode swapped underneath every holder, and both then believe "
        "they have exclusive access with nothing raised. The role-derived "
        "layout is what enforces the separation rather than a convention: "
        "NEVER_RESTORED resolves under the local directory and the document "
        "resolves under the history directory, so the two cannot end up "
        "beside each other by an edit to a relative path.",
    ),
    _installation(
        "recovery_lock", "recovery.lock",
        "The ONE gate a bare-metal recovery can still take. Every gate KTD21 "
        "publishes is library-scoped on purpose, so that a second machine "
        "contends with the first instead of holding an invisible lock of its "
        "own. The cost is that all of them are unreachable when the library "
        "volume is the thing that died, which is the one case a recovery "
        "exists for. This is the substitute, and it is installation-scoped "
        "because with the library gone the only contention that can exist is "
        "between processes on this machine: there is no shared volume left "
        "for two machines to contend over."
        " NEVER_RESTORED for the inode reason every lock here shares, and "
        "trivially so: it is installation-scoped, and a library snapshot has "
        "no business reaching outside the library at all.",
    ),
    # Appended, for the reason above.
    _library(
        "adoption_ledger", "adoption_ledger.json", SnapshotRole.COUPLED,
        "Which entries of an approved adoption plan have already been applied "
        "to this library. R26 says a plan applies incrementally and resumably, "
        "and resumably across SESSIONS, so the record has to outlive the "
        "process that made it. Losing it to a reinstall re-applies a plan from "
        "its first item against a library that already holds most of it."
        " COUPLED: every record it holds names a playlist membership row a "
        "restore rolls back. A ledger that survived a rollback would report "
        "those entries applied while the rows were gone, and the resume would "
        "then skip exactly the work the restore undid.",
        # Every COUPLED entry names its effect; tests/test_restore.py checks.
        rollback_effects=(RollbackEffect.WRITTEN_FILE_TAG,),
    ),
    _library(
        "adoption_tag_revert_log", "adoption_tag_revert.json", SnapshotRole.NEVER_RESTORED,
        "The only surviving copy of each file's tag value from before adoption "
        "overwrote it on disk. A tag write is the one thing an adoption run "
        "does that the XML re-import safety net never covered: re-importing an "
        "export does not put a genre string back into a file. A reinstall that "
        "loses this makes every on-disk write permanent."
        " NEVER_RESTORED, and this is the third entry to carry that argument "
        "for the same reason the two undo logs already here do: the writes it "
        "reverses landed on FILES, a database restore does not undo a file "
        "write, and discarding the log would make them permanent. Rolling this "
        "back is not a stale record, it is data loss."
        " ITS OWN ENTRY RATHER THAN THE ADOPTION LEDGER'S FIELD, because the "
        "two answer to opposite snapshot roles and one file cannot be both.",
    ),
    _library(
        "adoption_locks", "adoption_locks", SnapshotRole.NEVER_RESTORED,
        "One sibling lock per adoption document, serializing the read then "
        "write each of them performs. An atomic rename makes the WRITE atomic "
        "and does nothing for the cycle around it: two processes both read the "
        "same set, both add their record, and the second rename discards the "
        "first while the call that lost reports success. A dropped applied "
        "record re-applies work, and a dropped revert record loses the only "
        "copy of an overwritten tag. Library-scoped because the documents are: "
        "a lock in a per-installation directory is invisible to the second "
        "machine editing the same library."
        " NEVER_RESTORED for the inode reason every lock here shares, and it "
        "is why this is a directory of its own rather than a file beside each "
        "document: the ledger is COUPLED, so a restore replaces the directory "
        "holding it, and a lock inside that directory would have its inode "
        "swapped under every process holding it."
        " A DIRECTORY rather than one entry per document, so a third adoption "
        "document cannot arrive without a lock.",
        medium=Medium.DIRECTORY,
    ),
    # U33's entries, appended for the reason above.
    _library(
        "outbound_writes", "outbound_writes.json", SnapshotRole.SURVIVES_ROLLBACK,
        "The remote identifiers a playlist export or a heart-back already "
        "wrote on THIS library's streaming account. A second install that "
        "lost it would create a second remote playlist for a crate that "
        "already has one, and would re-heart tracks the account already "
        "hearts. Library-scoped because the records name this library's "
        "playlists and favourites, not the machine."
        " It SURVIVES a rollback: the remote account does not roll back, "
        "and forgetting a remote playlist id is how the next export "
        "duplicates one. Coupled would be the wrong role, because a "
        "restore of the database must not make the next export create.",
    ),
    _library(
        "outbound_writes_lock", "outbound_writes.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the outbound write ledger. Two exports "
        "finishing at once would both miss the same remote id, both "
        "create, and the second rename would discard the first playlist "
        "while reporting success. Library-scoped for the reason the "
        "document is: a lock in a per-installation directory is invisible "
        "to a second machine editing the same library. NEVER_RESTORED "
        "for the inode reason every lock here shares.",
    ),
    # U130's entries, appended.
    _library(
        "playlist_pairs", "playlist_pairs.json", SnapshotRole.SURVIVES_ROLLBACK,
        "U130. Every account playlist the author marked to stay the same "
        "list as one rekordbox playlist, by both identifiers, with what "
        "each side held when the last sync finished. The next sync merges "
        "each side against that snapshot, so a lost document makes every "
        "pair's next sync a first one, which adds and never removes."
        " It SURVIVES a rollback for the outbound ledger's reason: the "
        "account does not roll back, and a snapshot older than the account "
        "would read the account's current tracks as additions.",
    ),
    _library(
        "playlist_pairs_lock", "playlist_pairs.lock", SnapshotRole.NEVER_RESTORED,
        "The sibling lock for the playlist pairs, which are a read then a "
        "write over one document. Two syncs recording at once would both "
        "read the same document and the second would discard the first "
        "one's snapshot. NEVER_RESTORED for the inode reason every lock "
        "here shares.",
    ),
    _library(
        "mirror_plans", "mirror_plans", SnapshotRole.NEVER_RESTORED,
        "The account mirror's plan frozen on the organize run whose gate it "
        "was shown at, one JSON file per run: the library it read and every "
        "match it made (R-1031). The run that applies rebuilds the mirror "
        "from it, reading the account listing alone, so the digest approved "
        "is the digest applied and a library write between the two acts "
        "does not stale the decision. Library-scoped because it names this "
        "library's content rows. NEVER_RESTORED for the run record's "
        "reason: a frozen plan belongs to a run, and restoring one would "
        "apply a plan nobody was shown against the restored library.",
        medium=Medium.DIRECTORY,
    ),
    _library(
        "rehearsal_areas", "rehearsals", SnapshotRole.NEVER_RESTORED,
        "The volume half of each rehearsal's scratch area, one folder per "
        "run (U162): a copy of the database file set, a copy of the library "
        "state it reads, and clones of the files the verb moves. On the "
        "library volume so a clone stays a clone. Removed when the "
        "rehearsal ends and kept, named, only when it failed. "
        "NEVER_RESTORED: a scratch copy is nobody's state, and restoring one "
        "would put a rehearsal's files back beside a library that never "
        "had them.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "rehearsals", "rehearsals",
        "The local half of each rehearsal's scratch area, the redirected "
        "config and installation state a rehearsal runs under, and one "
        "record per finished rehearsal, its plan digest and plan lines, "
        "which the live run of the same verb over the same input compares "
        "its own plan against (U162). Installation-scoped beside the run "
        "records, since a rehearsal is a run on this machine.",
        medium=Medium.DIRECTORY,
    ),
)

_STATE_BY_KEY: Mapping[str, StateFile] = MappingProxyType({s.key: s for s in STATE_FILES})

#: The Cratekit-owned directory inside the user's sets directory.
SET_WORKSPACE_DIRNAME = ".cratekit_workspaces"

#: The entries whose location is composed from configured values rather than a
#: fixed relative path, each with the function that composes it.
_COMPOSED_PATHS: Mapping[str, Callable[["Config"], Path]] = MappingProxyType(
    {
        "rekordbox_db": lambda config: config.library.db_path,
        "set_workspaces": lambda config: (
            config.library.root
            / config.library.music_dir
            / config.library.sets_dir
            / SET_WORKSPACE_DIRNAME
        ),
    }
)


def state_file(key: str) -> StateFile:
    """Look up one inventory entry, or raise naming the closest thing to a menu."""
    try:
        return _STATE_BY_KEY[key]
    except KeyError:
        raise KeyError(
            f"{key!r} is not a declared state entry. Every state file is declared "
            f"in config.STATE_FILES with a root and the failure that root prevents; "
            f"an undeclared one is a file nobody decided the root for. "
            f"Declared: {', '.join(sorted(_STATE_BY_KEY))}"
        ) from None


def state_path(key: str, config: Config | None = None) -> Path:
    """Resolve one state entry to a path. Creates nothing (Rule 1).

    A library-scoped entry needs a ``Config``; without one it raises rather than
    fall back to the installation root (KTD21).
    """
    entry = state_file(key)
    if entry.medium is Medium.KEYCHAIN:
        raise ValueError(
            f"{key!r} is stored in the OS keychain and has no path. Read it "
            f"through cratekit.core.secrets, which is the one place that knows "
            f"how to fail when no keychain backend is reachable."
        )
    if entry.root is StateRoot.INSTALLATION:
        if key in _PROVIDER_GATE_KEYS:
            return provider_gate_dir() / entry.relative
        # The entry names which of the two installation directories it means.
        base = (
            config_dir()
            if entry.installation_area is InstallationArea.CONFIG
            else installation_state_dir()
        )
        return base / entry.relative
    if config is None:
        raise ValueError(
            f"{key!r} is library-scoped, so resolving it needs the config that "
            f"names the library. Passing no config would resolve it under the "
            f"installation root, which is the exact placement KTD21 exists to end."
        )
    composed = _COMPOSED_PATHS.get(key)
    if composed is not None:
        return composed(config)
    if entry.at_library_root:
        return config.library.root / entry.relative
    # The subdirectory derives from the declared role (KTD21b).
    return library_state_dir(config) / _LIBRARY_SUBDIR_BY_ROLE[entry.snapshot] / entry.relative


def state_files_for(root: StateRoot) -> tuple[StateFile, ...]:
    """Every declared entry under one root, in declaration order."""
    return tuple(s for s in STATE_FILES if s.root is root)


def coupled_state_files() -> tuple[StateFile, ...]:
    """Every entry a KTD21b snapshot must capture and a restore must replace.

    Derived from the schema so U8 and U32 never keep a second copy.
    """
    return tuple(s for s in STATE_FILES if s.snapshot is SnapshotRole.COUPLED)


def out_of_band_effects() -> tuple[tuple[StateFile, RollbackEffect], ...]:
    """Every coupled entry that reaches outside the set a restore replaces, paired
    with each effect it declares.

    Uses the same predicate as ``coupled_state_files``, so the set a restore
    reconciles is the set it replaces. ``NONE`` is dropped here, since there is
    nothing to disposition.
    """
    return tuple(
        (entry, effect)
        for entry in coupled_state_files()
        for effect in entry.rollback_effects
        if effect is not RollbackEffect.NONE
    )


def sidecar_paths(key: str, config: Config, *, restored_only: bool = False) -> tuple[Path, ...]:
    """The sidecar paths that travel with one entry. Composed, never listed.

    A capture wants every sidecar; a restore passes ``restored_only`` because a
    stale index beside a fresh log describes a database that no longer exists.
    Any path may be absent, which is normal. Touches no disk (Rule 1).
    """
    entry = state_file(key)
    base = state_path(key, config)
    return tuple(
        base.with_name(base.name + sidecar.suffix)
        for sidecar in entry.sidecars
        if sidecar.restored or not restored_only
    )


def snapshot_sources(config: Config) -> tuple[Path, ...]:
    """Every path a KTD21b capture copies: the coupled directory, the database,
    and the database's SQLite sidecars.

    Everything coupled but the database lives in one directory, so capture is a
    directory copy and restore a directory replace; the database sits where the
    user chose, which is why ``validate`` constrains it to one filesystem. The
    sidecars are included because the log holds committed transactions the
    database file lacks. Some returned paths may not exist; copy what is there.
    """
    coupled_dir = library_coupled_dir(config)
    sources = [coupled_dir]
    for entry in coupled_state_files():
        if entry.medium is Medium.KEYCHAIN:
            continue
        path = state_path(entry.key, config)
        if path == coupled_dir or coupled_dir in path.parents:
            # Already covered by the directory copy, sidecars included.
            continue
        sources.append(path)
        sources.extend(sidecar_paths(entry.key, config))
    return tuple(sources)


def rekey_records(
    records: Mapping[str, object],
    resolve_identifier: Callable[[str], str | None],
) -> tuple[dict[str, object], tuple[str, ...]]:
    """The one-time re-key D5 requires, as a pure function.

    ``resolve_identifier`` maps a display-name key to its stable identifier, or
    None. Returns the re-keyed records and the keys that did not resolve, which
    are returned rather than dropped so the orphans surface.
    """
    migrated: dict[str, object] = {}
    unresolved: list[str] = []
    for old_key, value in records.items():
        identifier = resolve_identifier(old_key)
        if identifier is None:
            unresolved.append(old_key)
            continue
        migrated[identifier] = value
    return migrated, tuple(unresolved)


# The typed schema: frozen dataclasses, so a typo is an AttributeError at the
# call site rather than a None that travels.


@dataclass(frozen=True, slots=True)
class PrefixMapping:
    """One entry of the ordered location prefix map (S1).

    The TOML keys are ``from`` and ``to``, mapped to suffixed fields once in
    ``_PREFIX_TOML_KEYS``. Order must survive a round trip: one prefix can be
    another's prefix, and the first match wins.
    """

    from_prefix: str
    to_prefix: str
    #: R38, per rule: the recorded identity of the volume ``to`` sits on, since a
    #: mount path does not say which disk is there. Unset is correct for a target
    #: inside the library root; a target elsewhere with nothing recorded refuses a
    #: destructive pass.
    volume_id: str | None = None


_PREFIX_TOML_KEYS = (("from", "from_prefix"), ("to", "to_prefix"))

#: The one optional key of a prefix mapping, written only when set so a rule
#: without one keeps its bytes and its fingerprint (KTD9).
PREFIX_VOLUME_IDENTITY_KEY = "volume_id"

#: The one interpolation token a prefix mapping's ``to`` may contain, so the map
#: survives remounting the library.
LIBRARY_ROOT_TOKEN = "{library.root}"

#: The processed tree's default name (U154), shared by the wizard and the
#: dataclass.
DEFAULT_PROCESSED_DIR = "Processed_Tracks"


@dataclass(frozen=True, slots=True)
class LibraryConfig:
    """Where the library is, what proves it is the right one, and how it is laid out."""

    root: Path
    #: R38. The recorded identity of the volume, asserted before any destructive
    #: operation. A UUID or serial, never a mount path.
    volume_id: str
    #: The rekordbox database (``rekordbox_db``, COUPLED), expected under ``root``.
    db_path: Path
    #: The date the user accepted that their database sits outside the library
    #: root. Unset, a database elsewhere refuses at load. KTD21b needs one atomic
    #: rename across the database and its coupled state, which works only on one
    #: filesystem; rekordbox's default location breaks that, so the case is
    #: allowed as a decision made visibly at setup rather than refused.
    db_outside_root_acknowledged_on: str | None = None
    music_dir: str = "Music"
    #: The directory under ``music_dir`` where ``intake shelve`` files a landed
    #: batch, ``<processed_dir>/<year>/<MM_DD_YY subject>`` (U154). A setup answer.
    processed_dir: str = DEFAULT_PROCESSED_DIR
    sets_dir: str = "Set_Recordings"
    #: The library-scoped state root's directory name, relative to ``root``.
    state_dirname: str = ".cratekit"
    #: Ordered, first match wins, since one prefix can be another's prefix.
    #: Populated at setup from what the database contains.
    location_prefix_map: tuple[PrefixMapping, ...] = ()


@dataclass(frozen=True, slots=True)
class PathsConfig:
    """Paths that are not inside the library."""

    #: Where fresh downloads land before moving into the library. One value that
    #: round-trips into the acquisition adapter's setting (KTD20).
    download_staging: Path


@dataclass(frozen=True, slots=True)
class ProfileConfig:
    """Which named preset of module membership is in force."""

    name: str


@dataclass(frozen=True, slots=True)
class ModulesConfig:
    """Per-module toggles the user set explicitly.

    Only what the file contains: a module it omits takes the profile's answer
    (D6), so "chose off" and "profile says off" stay distinguishable.
    """

    explicit: Mapping[str, bool] = field(default_factory=lambda: MappingProxyType({}))


@dataclass(frozen=True, slots=True)
class TaxonomyConfig:
    """The taxonomy selection only (S6).

    The active template is library-scoped state; config records the setup
    choice so a re-run of setup seeds the same one.
    """

    template: str = "default"


@dataclass(frozen=True, slots=True)
class NamingConfig:
    """Naming policy values (S3).

    The naming engine takes these as parameters and never reads config, so it
    can run against two taxonomies in one process.
    """

    lossy_marker: str = "[MP3]"
    #: Both budgets are UTF-8 bytes, not characters. The margin below the
    #: filesystem ceiling reserves room for a later zero-padding pass.
    path_budget_bytes: int = 250
    filename_max_bytes: int = 255


#: Retired adapter names a config file may hold, each mapped to its current
#: name (U197), so an old file selects the same adapter rather than refuse.
#: Folded where the file is read; here because a foundation module may not
#: import ``cratekit.acquire``.
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({"tidal_dl_ng": "vendored"})


def current_adapter_name(name: str) -> str:
    """The name an adapter goes by now, given any name configuration recorded."""
    return RETIRED_ADAPTER_NAMES.get(name, name)


@dataclass(frozen=True, slots=True)
class AcquisitionConfig:
    """What acquires, at what quality, under which lossless policy."""

    adapter: str = "vendored"
    quality: str = "lossless"
    #: None means "the adapter's own default". The adapter owns pacing (KTD20).
    pacing_delay_s: float | None = None
    #: How many acquisitions run at once (R10). One declared value the adapter
    #: carries in memory per invocation; the bounded pool reads it rather than
    #: declaring a second cap.
    concurrency: int = 1
    #: R21 and S3. Two values only: marking is mandatory wherever lossy is
    #: permitted, so an unmarked lossy file cannot be expressed.
    lossless_policy: str = "strict"


#: The tempo window the head's estimate is chosen inside, in BPM, both ends
#: included. It decides which metrical level a head names (83 or 166, R-744); a
#: drum and bass library raises both bounds in the config file.
DEFAULT_TEMPO_FLOOR = 80
DEFAULT_TEMPO_CEILING = 160

#: The drift at or above which a track reads as variable and its landed row is
#: marked ``dyn`` for rekordbox's Dynamic analysis (U157), as a percent tempo
#: spread (``core.drift``). Set above every synthetic steady reading (0.0 to 0.3)
#: and leaning toward Normal, since a steady track sent to Dynamic gets a
#: wobbling grid. Not yet calibrated on a real library; the card owes that.
DEFAULT_DRIFT_CUT = 1.5


@dataclass(frozen=True, slots=True)
class AnalysisConfig:
    """Analysis sizing, calibration selection, and the tempo window."""

    #: None means "probe" (KTD10): worker count comes from a probe worker's
    #: resident size against available memory, never from a CPU count.
    jobs: int | None = None
    energy_calibration: str = "auto"
    #: The head names a tempo from the floor to the ceiling, both included.
    tempo_floor: int = DEFAULT_TEMPO_FLOOR
    tempo_ceiling: int = DEFAULT_TEMPO_CEILING
    #: A drift at or above this reads as variable and is marked ``dyn`` (U157).
    drift_cut: float = DEFAULT_DRIFT_CUT


@dataclass(frozen=True, slots=True)
class RekordboxConfig:
    """The version pins the guarded writer refuses on.

    ``pinned_app_version`` defaults to None, and None refuses (S2). It is never
    auto-recorded from the installed app, since a copied pin refuses nothing;
    setup may propose it, and the user records it.
    """

    pinned_pyrekordbox: str = "0.4.4"
    pinned_db_version: str = "6000"
    pinned_app_version: str | None = None
    #: The date the user confirmed this pin against a real write, so a stale pin
    #: shows as stale.
    validated_on: str | None = None
    app_path: Path | None = None


@dataclass(frozen=True, slots=True)
class BackupConfig:
    """Remote backup destinations. All None by default, all wizard supplied.

    Each destination must name an rclone remote, ``remote:path``, and
    ``validate`` refuses one that does not (R-345): rclone reads a value with no
    colon as a local path relative to its working directory, and would back the
    library up beside the worker. ``remote`` is derived from the destinations
    when unset and checked against them when set, so doctor looks up the remote
    the transfers use.
    """

    remote: str | None = None
    dest: str | None = None
    archive_root: str | None = None
    db_dest_root: str | None = None


#: The three keys rclone is handed as targets, in wizard order, shared by the
#: validator, the wizard and the backup verb.
BACKUP_DESTINATION_KEYS: tuple[str, ...] = (
    "backup.dest",
    "backup.archive_root",
    "backup.db_dest_root",
)

#: An rclone remote name by rclone's own rule since 1.61: letters and digits in
#: any script, underscore, dot, plus, at sign, hyphen and space, not starting
#: with a hyphen or space nor ending with a space. ``\w`` is Unicode aware.
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*(?<! )$")


def backup_remote_name(value: object) -> str | None:
    """The rclone remote a destination names, or None when it names none.

    The remote is the part before the first colon. None for no colon (a local
    path), an empty name (an on the fly backend), a single character (a Windows
    drive letter), or a name rclone's configuration cannot hold. Public so the
    wizard and doctor split by the same rule.
    """
    if not isinstance(value, str):
        return None
    name, colon, _rest = value.partition(":")
    if not colon or len(name) < 2:
        return None
    if not _RCLONE_REMOTE_NAME.match(name):
        return None
    return name


def _validate_backup_destinations(data: Mapping) -> list[str]:
    """Every backup destination names one rclone remote, and ``remote`` agrees.

    Judged on the effective mapping, overrides applied (P2). An unset
    destination is not a problem here, since doctor and the backup verb report
    it; a set value that is not a configured remote is.
    """
    problems: list[str] = []
    named: dict[str, str] = {}
    for key in BACKUP_DESTINATION_KEYS:
        value = _dig(data, key)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        name = backup_remote_name(value)
        if name is None:
            problems.append(
                f"{key} must name a configured rclone remote as remote:path, "
                f"found {value!r}. rclone reads a value with no remote before "
                f"the colon as a local path relative to the working directory "
                f"of the process running the backup, so a real run would copy "
                f"the library beside that process and report a backup age for "
                f"the copy (R-345)."
            )
            continue
        named[key] = name
    if len(set(named.values())) > 1:
        spelled = ", ".join(f"{key} names {name!r}" for key, name in named.items())
        problems.append(
            f"the backup destinations must name one rclone remote and they "
            f"name several: {spelled}. The mirror, the dated archive and the "
            f"database snapshots are read back together, so they live under "
            f"one remote."
        )
    disagreement = backup_remote_disagreement(data)
    if disagreement is not None:
        remote, expected = disagreement
        problems.append(
            f"backup.remote names {remote!r} and the backup destinations "
            f"name {expected!r}. Doctor checks the remote it is told against "
            f"rclone's configuration, and the transfers use the one in the "
            f"destinations, so the two must agree or the check reports on a "
            f"remote nothing writes to. Setup's --backup-remote replaces the "
            f"spelled one (R-662)."
        )
    return problems


def backup_remote_disagreement(data: Mapping) -> tuple[str, str] | None:
    """The spelled ``backup.remote`` and the one remote the destinations name,
    when the two differ; None otherwise.

    None when no remote is spelled or the destinations do not name exactly one.
    Compares names, so ``gdrive``, ``gdrive:`` and ``gdrive:path`` agree. Public
    so the wizard's repair and its refusal ask the same question (R-662).
    """
    remote = _dig(data, "backup.remote")
    if not isinstance(remote, str) or not remote.strip():
        return None
    named = {
        name
        for name in (backup_remote_name(_dig(data, key)) for key in BACKUP_DESTINATION_KEYS)
        if name is not None
    }
    if len(named) != 1:
        return None
    expected = next(iter(named))
    if remote.split(":", 1)[0] == expected:
        return None
    return remote, expected


#: The default intake ages, named as constants because ``slots=True`` hides a
#: field default from the validator, which would otherwise keep a second copy.
DEFAULT_INTAKE_STALE_DAYS = 30
DEFAULT_INTAKE_EXPIRED_DAYS = 90

#: How long an open gate may sit idle before ``crate status`` folds it into one
#: line and ``crate run retire`` offers to answer it (U170).
DEFAULT_OPEN_GATE_STALE_DAYS = 7

#: Ten years, a ceiling so the day count never overflows a duration.
MAX_OPEN_GATE_STALE_DAYS = 3650


@dataclass(frozen=True, slots=True)
class ReportsConfig:
    """Policy the read-only reports age against (R5, feature row 20).

    Day counts the user owns (S3); the report module owns the mechanism. The
    defaults, thirty and ninety days, reproduce the source convention.
    """

    intake_stale_days: int = DEFAULT_INTAKE_STALE_DAYS
    intake_expired_days: int = DEFAULT_INTAKE_EXPIRED_DAYS
    #: Open gates idle for longer than this many days are one line in
    #: ``crate status`` and what ``crate run retire`` answers by default (U170).
    open_gate_stale_days: int = DEFAULT_OPEN_GATE_STALE_DAYS


#: How old a hand made collection export may be before the outbound verbs say
#: so. A constant for the reason the intake ages give.
DEFAULT_EXPORT_STALE_DAYS = 7

#: Ten years, a ceiling rather than a policy: a larger count overflows a
#: duration and crashed the outbound verbs at the gate.
MAX_EXPORT_STALE_DAYS = 3650


#: The rekordbox top folders a sync of every pair skips unless the file says
#: otherwise (U198).
DEFAULT_PAIR_SKIP_FOLDERS: tuple[str, ...] = ("ARCHIVE",)

PAIR_SKIP_FOLDERS_KEY = "outbound.pair_skip_folders"

#: U231. Whether ``crate sync pair`` keeps the account's order for every pair
#: rather than only those whose rekordbox playlist is under GIG READY.
PAIR_ORDER_EVERY_PAIR_KEY = "outbound.pair_order_every_pair"


@dataclass(frozen=True, slots=True)
class OutboundConfig:
    """Policy for the verbs that write to a streaming account (R-227).

    ``export_stale_days`` is a warning threshold, never a refusal: past it the
    plan names the hand made export's date and says it is old, and the person
    still decides. A user value, on the rule ``ReportsConfig`` states.
    """

    export_stale_days: int = DEFAULT_EXPORT_STALE_DAYS
    #: The rekordbox top folders ``crate sync pair`` lists and never pairs
    #: (U198), by exact name; an empty list pairs every folder.
    pair_skip_folders: tuple[str, ...] = DEFAULT_PAIR_SKIP_FOLDERS
    #: U231. ``crate sync pair`` orders an account playlist only when its
    #: rekordbox playlist is under GIG READY, since every move is a provider
    #: call. True orders every pair; tracks still sync both ways regardless.
    pair_order_every_pair: bool = False


#: The recognition service's identify endpoint for the region most accounts are
#: made in. A constant for the reason the intake ages give.
DEFAULT_RECOGNITION_HOST = "identify-us-west-2.acrcloud.com"

#: Paid recognition calls this machine may make in one calendar month before it
#: refuses, about three two hour sets. A default bound rather than none, so a
#: spent quota cannot be overrun unnoticed; the refusal names the line to raise.
DEFAULT_RECOGNITION_MONTHLY_CALLS = 1000

#: The only domain a recognition host may sit under, since the access key and
#: its signature go to that host with every paid call.
RECOGNITION_HOST_DOMAIN = "acrcloud.com"

_HOST_LABEL = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


@dataclass(frozen=True, slots=True)
class RecognitionConfig:
    """Where paid recognition is sent and how much of it a month may cost (R-301).

    ``host`` is the account's regional endpoint; another region's host answers
    with errors the identifier reads as transient. ``monthly_calls`` is a
    refusal, never a warning, checked against this machine's ledger before the
    first chunk is carved. Both are user values frozen with a queued job.
    """

    host: str = DEFAULT_RECOGNITION_HOST
    monthly_calls: int = DEFAULT_RECOGNITION_MONTHLY_CALLS


#: The least time between two consecutive calls to the streaming provider from
#: any process on this machine, well under any published allowance. Each
#: provider default is a constant for the reason the intake ages give.
DEFAULT_PROVIDER_MIN_INTERVAL_S = 1.0

#: How long every provider call is refused after the breaker trips, longer than
#: the observed clearing time so the cooldown is not a second trip.
DEFAULT_PROVIDER_COOLDOWN_S = 900

#: The most calls to the streaming provider one command may make before it
#: stops, keeping what it did, and names the command that continues (U193).
#: Raised for one run with ``--calls`` or for every run here.
DEFAULT_PROVIDER_CALLS_PER_COMMAND = 500

#: How many days a provider answer for an ISRC is reused before it is asked
#: again (U206). A not found is kept a week at most, in ``acquire.isrc_cache``.
#: Zero turns the cache off.
DEFAULT_PROVIDER_ISRC_CACHE_DAYS = 30

#: How many calls each identity (the account session, Cratekit's app
#: credentials) may make in any sixty minutes across every process reading the
#: one gate (U278), below the default pacing so a day of reads cannot use up
#: what a label go needs. Raised for one run with ``--calls-per-hour``.
DEFAULT_PROVIDER_CALLS_PER_HOUR = 1500

#: How many calls the night pass may make in one night, across every firing and
#: every process reading the one gate (U293). A night runs noon to noon, local
#: time.
DEFAULT_PROVIDER_NIGHT_CALLS = 1200

#: The hour's budget the night pass holds the account to (U293). The lower of
#: this and ``calls_per_hour`` holds.
DEFAULT_PROVIDER_NIGHT_CALLS_PER_HOUR = 600

#: The share of the hour's budget a read-only command may never spend, kept for
#: the verbs that write the account or download (U278).
DEFAULT_PROVIDER_RESERVE_SHARE = 0.25


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    """How the streaming provider's account is protected from this machine (R-705).

    Every field is a refusal, never a warning, none can be switched off, and
    all are frozen with a queued job. ``min_interval_s`` paces from the last
    call any process made; ``cooldown_s`` holds the breaker after a rate limit
    survives the retry ladder; ``calls_per_command`` is per command, never per
    day (U193); ``isrc_cache_days`` reuses an ISRC answer, zero asking every
    time (U206); ``calls_per_hour`` is each identity's budget in the one gate,
    of which ``reserve_share`` is barred to read-only commands (U278);
    ``night_calls`` and ``night_calls_per_hour`` only lower these for the night
    pass (U293).
    """

    min_interval_s: float = DEFAULT_PROVIDER_MIN_INTERVAL_S
    cooldown_s: int = DEFAULT_PROVIDER_COOLDOWN_S
    calls_per_command: int = DEFAULT_PROVIDER_CALLS_PER_COMMAND
    isrc_cache_days: int = DEFAULT_PROVIDER_ISRC_CACHE_DAYS
    calls_per_hour: int = DEFAULT_PROVIDER_CALLS_PER_HOUR
    reserve_share: float = DEFAULT_PROVIDER_RESERVE_SHARE
    night_calls: int = DEFAULT_PROVIDER_NIGHT_CALLS
    night_calls_per_hour: int = DEFAULT_PROVIDER_NIGHT_CALLS_PER_HOUR


#: How many releases one sweep of one favourite label may offer for review,
#: counting those already queued (R-790), small enough to answer in a sitting.
#: A constant for the reason the intake ages give.
DEFAULT_LABEL_OFFER = 10

#: How many days a dated new releases playlist beside a label's year may sit
#: before ``crate organize`` reports it (U117). Reported only, never merged.
DEFAULT_NEW_PLAYLIST_AGE_DAYS = 30


@dataclass(frozen=True, slots=True)
class LabelsConfig:
    """How much of a favourite label's catalogue one sweep offers (R-790).

    ``offer_per_sweep`` is a window over the newest releases, never a date: a
    sweep walks newest first and fills this many places with queued and newly
    filed releases. The whole catalogue is still read, so an owned release is
    skipped without taking a place (R-137), and what the window misses is
    counted, less releases whose copyright names another label (U238). A
    label's registry entry may override it. No value switches it off.
    """

    offer_per_sweep: int = DEFAULT_LABEL_OFFER
    #: The age in days past which ``crate organize`` reports a dated
    #: ``<label> <year> new <date>`` playlist on the account (U117).
    new_playlist_age_days: int = DEFAULT_NEW_PLAYLIST_AGE_DAYS


@dataclass(frozen=True, slots=True)
class Config:
    """The whole validated configuration, frozen.

    Frozen so a job runs against the configuration as it was queued (KTD9),
    which a mutable object could not guarantee.
    """

    schema_version: int
    library: LibraryConfig
    paths: PathsConfig
    profile: ProfileConfig
    modules: ModulesConfig = field(default_factory=ModulesConfig)
    taxonomy: TaxonomyConfig = field(default_factory=TaxonomyConfig)
    naming: NamingConfig = field(default_factory=NamingConfig)
    acquisition: AcquisitionConfig = field(default_factory=AcquisitionConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    rekordbox: RekordboxConfig = field(default_factory=RekordboxConfig)
    backup: BackupConfig = field(default_factory=BackupConfig)
    # Later sections are appended, never inserted, so concurrent units conflict.
    reports: ReportsConfig = field(default_factory=ReportsConfig)
    outbound: OutboundConfig = field(default_factory=OutboundConfig)
    recognition: RecognitionConfig = field(default_factory=RecognitionConfig)
    provider: ProviderConfig = field(default_factory=ProviderConfig)
    labels: LabelsConfig = field(default_factory=LabelsConfig)

    # Derived views.

    def enabled_modules(self) -> frozenset[str]:
        """Effective module membership: the profile's preset, then explicit overrides."""
        return profiles.resolve(self.profile.name, self.modules.explicit).modules

    def available_capabilities(self) -> frozenset[str]:
        """Everything the install can do, including what no profile may switch off."""
        return profiles.resolve(self.profile.name, self.modules.explicit).available

    def resolved_prefix_map(self) -> tuple[tuple[str, str], ...]:
        """The prefix map with ``{library.root}`` interpolated, in declared order.

    Plain pairs for a resolver that takes the first match; never sorted or
    deduped.
    """
        root = str(self.library.root)
        return tuple(
            (m.from_prefix, m.to_prefix.replace(LIBRARY_ROOT_TOKEN, root))
            for m in self.library.location_prefix_map
        )

    def resolved_prefix_rules(self) -> tuple[tuple[str, str, str | None], ...]:
        """The resolved prefix map with each rule's recorded volume identity.

    A second shape so readers of ``resolved_prefix_map`` keep their pairs; built
    from those pairs so the interpolation is written once.
    """
        return tuple(
            (source, target, mapping.volume_id)
            for (source, target), mapping in zip(
                self.resolved_prefix_map(), self.library.location_prefix_map, strict=True
            )
        )

    # Serialization and identity.

    def to_toml_dict(self) -> dict:
        """A TOML-safe, deterministically ordered plain dict.

    Determinism is required because ``fingerprint`` hashes these bytes. None
    values are omitted, since TOML has no null.
    """
        return _to_toml_value(self)

    def to_toml_bytes(self) -> bytes:
        """The exact bytes ``save`` writes and ``fingerprint`` hashes."""
        return tomli_w.dumps(self.to_toml_dict()).encode("utf-8")

    def fingerprint(self) -> str:
        """A stable identity for this configuration (KTD9).

    Recorded at queue time and compared at run time, so a job reports drift
    rather than silently picking a version.
    """
        return hashlib.sha256(self.to_toml_bytes()).hexdigest()

    def db_is_inside_library_root(self) -> bool:
        """True when the database and its coupled state share a filesystem (KTD21b).

        A bare fact: validation refuses on it at load, and doctor reports it on
        every run as a reminder that snapshots are copies, not atomic commits.
        """
        return is_inside(self.library.db_path, self.library.root)

    # Preconditions.

    def assert_rekordbox_pin_recorded(self) -> None:
        """Refuse when the application pin has never been explicitly recorded (S2).

        Called by the guarded writer before it opens the database. Unset refuses
        a write, not a load, so read-only verbs still reach the setup step.
        """
        if not self.rekordbox.pinned_app_version:
            # The message states the problem; the remedy token says what to do (D2).
            raise ConfigInvalid(
                [
                    "rekordbox.pinned_app_version is not set, and an unset pin "
                    "refuses every database write. A pin copied from whatever "
                    "happens to be installed would refuse nothing, forever, which "
                    "is the entire property the pin exists to provide. The pin is "
                    "meaningful only together with rekordbox.validated_on, the "
                    "date it was confirmed against a real write."
                ],
                remedy=Remedy.RECORD_REKORDBOX_PIN,
            )


# Validation collects every problem before raising.

#: Dotted paths that have no default and must appear in the file, kept short so
#: the first-run wizard is short.
REQUIRED_KEYS: tuple[str, ...] = (
    "schema_version",
    "library.root",
    "library.volume_id",
    "library.db_path",
    "paths.download_staging",
    "profile.name",
)

_LOSSLESS_POLICIES = ("strict", "allow_lossy_marked")


def _dig(data: Mapping, dotted: str):
    """Fetch a dotted key from nested mappings, or return None when absent."""
    node: object = data
    for part in dotted.split("."):
        if not isinstance(node, Mapping) or part not in node:
            return None
        node = node[part]
    return node


def _env_path(variable: str) -> Path | None:
    """An override path from the environment, or None. Relocates, never supplies."""
    value = os.environ.get(variable)
    return Path(value) if value else None


def _apply_env_overrides(data: Mapping) -> dict:
    """Return a copy of ``data`` with the relocation overrides applied.

    The one place the environment enters. It relocates and never supplies, so a
    machine with no setup cannot resolve a library root (R38). A relocated root
    carries a db_path that was under it; one outside stays put and still needs
    its acknowledgment. Idempotent, since ``from_dict`` and ``validate`` both
    apply it.
    """
    working = {key: (dict(value) if isinstance(value, Mapping) else value)
               for key, value in data.items()}

    library = working.get("library")
    if isinstance(library, dict):
        root_override = _env_path(ENV_LIBRARY_ROOT)
        configured_root = library.get("root")
        if (
            root_override is not None
            and isinstance(configured_root, str)
            and configured_root.strip()
        ):
            db_path = library.get("db_path")
            if (
                isinstance(db_path, str)
                and db_path.strip()
                and is_inside(Path(db_path), Path(configured_root))
            ):
                relative = os.path.relpath(
                    os.path.normpath(db_path), os.path.normpath(configured_root)
                )
                library["db_path"] = os.path.normpath(
                    os.path.join(str(root_override), relative)
                )
            library["root"] = str(root_override)

    paths = working.get("paths")
    if isinstance(paths, dict):
        staging_override = _env_path(ENV_DOWNLOAD_STAGING)
        if staging_override is not None:
            staged = paths.get("download_staging")
            if isinstance(staged, str) and staged.strip():
                paths["download_staging"] = str(staging_override)

    return working


def validate(data: Mapping) -> list[str]:
    """Return every problem with the effective configuration, as readable lines.

    Side-effect free, so the wizard shows all remaining work and the loader
    raises the same content. The environment overrides are applied first, so
    every rule is decided against the values the process will use.
    """
    data = _apply_env_overrides(data)
    problems: list[str] = []

    for key in REQUIRED_KEYS:
        value = _dig(data, key)
        if value is None or (isinstance(value, str) and not value.strip()):
            problems.append(f"missing required key: {key}")

    version = data.get("schema_version")
    if version is not None and not isinstance(version, int):
        problems.append(
            f"schema_version must be an integer, found {type(version).__name__}"
        )

    volume_id = _dig(data, "library.volume_id")
    if isinstance(volume_id, str) and volume_id.strip():
        problems += _mount_path_problem(VOLUME_IDENTITY_KEY, volume_id)

    template = _dig(data, TAXONOMY_TEMPLATE_KEY)
    if template is not None and not template_name_is_usable(template):
        problems.append(
            f"{TAXONOMY_TEMPLATE_KEY} must be the short name of a shipped "
            f"template, letters, digits, underscores and dashes only, found "
            f"{template!r}. The name is composed into a packaged resource path, "
            f"so a value carrying a separator would read some other file."
        )

    profile_name = _dig(data, "profile.name")
    if profile_name is not None and profile_name not in profiles.PROFILE_NAMES:
        problems.append(
            f"profile.name must be one of {', '.join(profiles.PROFILE_NAMES)}, "
            f"found {profile_name!r}"
        )

    modules = data.get("modules") or {}
    if isinstance(modules, Mapping):
        for name, value in modules.items():
            if name not in profiles.MODULES:
                problems.append(
                    f"modules.{name} is not a known module. Known: "
                    f"{', '.join(profiles.MODULES)}"
                )
            elif not isinstance(value, bool):
                problems.append(f"modules.{name} must be true or false, found {value!r}")

    policy = _dig(data, "acquisition.lossless_policy")
    if policy is not None and policy not in _LOSSLESS_POLICIES:
        problems.append(
            f"acquisition.lossless_policy must be one of "
            f"{', '.join(_LOSSLESS_POLICIES)}, found {policy!r}. There is no "
            f"value that permits lossy without marking it (R21)."
        )

    concurrency = _dig(data, "acquisition.concurrency")
    if concurrency is not None and (
        not isinstance(concurrency, int)
        or isinstance(concurrency, bool)
        or concurrency < 1
    ):
        problems.append(
            f"acquisition.concurrency must be a positive integer number of "
            f"simultaneous acquisitions, found {concurrency!r}. Zero or a "
            f"negative value would not be a slower run, it would be a run that "
            f"acquires nothing while reporting success."
        )

    problems += _validate_db_containment(data)
    problems += _validate_prefix_map(_dig(data, "library.location_prefix_map"))
    problems += _validate_backup_destinations(data)

    for key in ("naming.path_budget_bytes", "naming.filename_max_bytes"):
        budget = _dig(data, key)
        if budget is not None and (not isinstance(budget, int) or isinstance(budget, bool)):
            problems.append(
                f"{key} must be an integer number of UTF-8 bytes, found "
                f"{budget!r}. S3 hands these to a pure naming engine as "
                f"parameters, so a wrong type surfaces as a TypeError in the "
                f"middle of a rename instead of as a named problem at load."
            )

    jobs = _dig(data, "analysis.jobs")
    if jobs is not None and (not isinstance(jobs, int) or jobs < 1):
        problems.append(
            f"analysis.jobs must be a positive integer, or absent to probe "
            f"available memory (KTD10). Found {jobs!r}."
        )

    problems += _validate_tempo_window(data)
    problems += _validate_drift_cut(data)

    problems += _validate_aging_thresholds(data)
    problems += _validate_export_staleness(data)
    problems += _validate_pair_skip_folders(data)
    problems += _validate_pair_order_every_pair(data)
    problems += _validate_open_gate_staleness(data)
    problems += _validate_recognition(data)
    problems += _validate_provider(data)
    problems += _validate_labels(data)

    return problems


def _validate_labels(data: Mapping) -> list[str]:
    """The per sweep offer of a favourite label (R-790).

    Zero is refused, since a sweep that offers nothing on purpose looks like a
    label with nothing new.
    """
    key = "labels.offer_per_sweep"
    offer = _dig(data, key)
    if offer is not None and (
        not isinstance(offer, int) or isinstance(offer, bool) or offer < 1
    ):
        return [
            f"{key} must be a positive whole number of releases one sweep of a "
            f"label may offer for review, found {offer!r}. A label's own "
            f"registry entry can raise it for that label alone."
        ]
    key = "labels.new_playlist_age_days"
    age = _dig(data, key)
    if age is not None and (not isinstance(age, int) or isinstance(age, bool) or age < 1):
        return [
            f"{key} must be a positive whole number of days a dated new releases "
            f"playlist may sit before organize reports it, found {age!r}."
        ]
    return []


def _validate_provider(data: Mapping) -> list[str]:
    """The pacing interval, the breaker's cooldown (R-705), the call ceiling (U193)
    and how long an ISRC answer is kept (U206).

    A wrong value is reported with its key rather than reaching the gate.
    """
    problems: list[str] = []
    key = "provider.min_interval_s"
    interval = _dig(data, key)
    if interval is not None and (
        isinstance(interval, bool)
        or not isinstance(interval, (int, float))
        or not math.isfinite(interval)
        or interval <= 0
    ):
        problems.append(
            f"{key} must be a positive number of seconds between two calls to the "
            f"streaming provider, found {interval!r}. There is no value that "
            f"switches pacing off; a person who wants it faster writes a smaller "
            f"number."
        )
    key = "provider.cooldown_s"
    cooldown = _dig(data, key)
    if cooldown is not None and (
        not isinstance(cooldown, int) or isinstance(cooldown, bool) or cooldown < 1
    ):
        problems.append(
            f"{key} must be a positive whole number of seconds the breaker holds "
            f"after the provider rate limits a run, found {cooldown!r}. There is "
            f"no value that switches the cooldown off."
        )
    key = "provider.calls_per_command"
    ceiling = _dig(data, key)
    if ceiling is not None and (
        not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 1
    ):
        problems.append(
            f"{key} must be a positive whole number of calls one command may make to "
            f"the streaming provider before it stops, found {ceiling!r}. There is no "
            f"value that switches the ceiling off; raise it for one run with --calls."
        )
    key = "provider.isrc_cache_days"
    days = _dig(data, key)
    if days is not None and (not isinstance(days, int) or isinstance(days, bool) or days < 0):
        problems.append(
            f"{key} must be a whole number of days an answer the streaming provider "
            f"gave for an ISRC is reused, found {days!r}. Zero turns the cache off."
        )
    key = "provider.calls_per_hour"
    hour = _dig(data, key)
    if hour is not None and (not isinstance(hour, int) or isinstance(hour, bool) or hour < 1):
        problems.append(
            f"{key} must be a positive whole number of calls each identity may make "
            f"to the streaming provider in an hour, found {hour!r}. There is no value "
            f"that switches the budget off; raise it for one run with --calls-per-hour."
        )
    key = "provider.reserve_share"
    share = _dig(data, key)
    if share is not None and (
        isinstance(share, bool)
        or not isinstance(share, (int, float))
        or not math.isfinite(share)
        or share < 0
        or share >= 1
    ):
        problems.append(
            f"{key} must be a number from 0 up to but not including 1, the share of "
            f"the hour's budget kept for writes and downloads, found {share!r}."
        )
    # U293. The night pass's own lines; zero would schedule a pass that does nothing.
    for key, what in (
        ("provider.night_calls", "the night pass may make in one night"),
        ("provider.night_calls_per_hour", "the night pass may make in an hour"),
    ):
        value = _dig(data, key)
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value < 1
        ):
            problems.append(
                f"{key} must be a positive whole number of calls {what} to the "
                f"streaming provider, found {value!r}. There is no value that "
                f"switches it off."
            )
    return problems


def _validate_aging_thresholds(data: Mapping) -> list[str]:
    """The two day counts the intake aging report bands against (feature row 20).

    Both positive, and expiry no earlier than staleness, as the report's own
    value object also requires. The pair check is skipped when either value was
    set and rejected, so the user is never told a default they did not write
    conflicts with one they did; an omitted value takes its default and is
    still compared.
    """
    problems: list[str] = []
    read: dict[str, int] = {}
    rejected: set[str] = set()
    for field_name in ("intake_stale_days", "intake_expired_days"):
        key = f"reports.{field_name}"
        value = _dig(data, key)
        if value is None:
            continue
        problem = _day_count_problem(
            key,
            value,
            consequence=(
                "Zero or a negative threshold does not report less, it reports "
                "every intake grouping as overdue on the day it is created."
            ),
        )
        if problem is not None:
            problems.append(problem)
            rejected.add(field_name)
            continue
        read[field_name] = value

    if read and not rejected:
        stale = read.get("intake_stale_days", DEFAULT_INTAKE_STALE_DAYS)
        expired = read.get("intake_expired_days", DEFAULT_INTAKE_EXPIRED_DAYS)
        if expired < stale:
            problems.append(
                f"reports.intake_expired_days ({expired}) is earlier than "
                f"reports.intake_stale_days ({stale}). The bands would overlap, "
                f"so a grouping would be reported as both stale and expired. Note "
                f"that a value left out takes its default, which is what makes "
                f"changing only one of the two able to produce this."
            )
    return problems


def _day_count_problem(
    key: str, value: object, *, consequence: str, maximum: int | None = None
) -> str | None:
    """What is wrong with one configured day count, or none. The rule, once.

    A ``bool`` is refused by name because it is an ``int`` to ``isinstance``.
    ``maximum`` applies only to a count that becomes a duration.
    """
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        return (
            f"{key} must be a positive whole number of days, found {value!r}. "
            f"{consequence}"
        )
    if maximum is not None and value > maximum:
        return (
            f"{key} must be a positive whole number of days no greater than "
            f"{maximum}, found {value!r}. There is no value that switches the "
            f"warning off, and a larger one cannot be held as a duration."
        )
    return None


def _validate_export_staleness(data: Mapping) -> list[str]:
    """The age past which an outbound verb calls its export old (R-227)."""
    key = "outbound.export_stale_days"
    value = _dig(data, key)
    if value is None:
        return []
    problem = _day_count_problem(
        key,
        value,
        consequence=(
            "Zero or a negative threshold does not switch the warning off, it "
            "calls every export old on the day it is made."
        ),
        maximum=MAX_EXPORT_STALE_DAYS,
    )
    return [] if problem is None else [problem]


def _validate_pair_skip_folders(data: Mapping) -> list[str]:
    """The rekordbox folders a sync of every pair leaves out (U198): a list of names."""
    value = _dig(data, PAIR_SKIP_FOLDERS_KEY)
    if value is None:
        return []
    if not isinstance(value, list | tuple) or not all(
        isinstance(one, str) and one.strip() for one in value
    ):
        return [
            f"{PAIR_SKIP_FOLDERS_KEY} must be a list of rekordbox folder names, found "
            f"{value!r}. A folder that cannot be named would skip nothing, and the "
            f"playlists under it would be paired with the account."
        ]
    return []


def _validate_pair_order_every_pair(data: Mapping) -> list[str]:
    """Whether every pair keeps the account's order (U231): true or false."""
    value = _dig(data, PAIR_ORDER_EVERY_PAIR_KEY)
    if value is None or isinstance(value, bool):
        return []
    return [
        f"{PAIR_ORDER_EVERY_PAIR_KEY} must be true or false, found {value!r}. A value "
        f"read as true would write the account's order for every pair, a provider call "
        f"per track moved."
    ]


def _validate_open_gate_staleness(data: Mapping) -> list[str]:
    """The age past which an open gate is folded away and offered for retirement (U170)."""
    key = "reports.open_gate_stale_days"
    value = _dig(data, key)
    if value is None:
        return []
    problem = _day_count_problem(
        key,
        value,
        consequence=(
            "Zero or a negative threshold does not keep every gate in view, it "
            "folds away and offers to retire a gate opened a minute ago."
        ),
        maximum=MAX_OPEN_GATE_STALE_DAYS,
    )
    return [] if problem is None else [problem]


def recognition_host_problem(value: object) -> str | None:
    """What is wrong with a recognition host, or none. The rule, once.

    A bare lowercase hostname under ``RECOGNITION_HOST_DOMAIN``: the identifier
    composes the URL around it, and the credential travels to that domain.
    """
    key = "recognition.host"
    if not isinstance(value, str):
        return f"{key} must be a hostname, found {value!r}"
    labels = value.split(".")
    if not all(_HOST_LABEL.match(label) for label in labels) or not value.endswith(
        f".{RECOGNITION_HOST_DOMAIN}"
    ):
        return (
            f"{key} must be a bare lowercase hostname under "
            f"{RECOGNITION_HOST_DOMAIN}, such as {DEFAULT_RECOGNITION_HOST}, found "
            f"{value!r}. No scheme and no path: the access key and its signature "
            f"are sent to this host with every paid call."
        )
    return None


def _validate_tempo_window(data: Mapping) -> list[str]:
    """The tempo window is two whole numbers, floor below ceiling (R-744).

    An empty window leaves the estimator no bin, so every head would silently
    carry no tempo.
    """
    problems: list[str] = []
    bounds: dict[str, object] = {}
    for key in ("tempo_floor", "tempo_ceiling"):
        value = _dig(data, f"analysis.{key}")
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            problems.append(
                f"analysis.{key} must be a whole number of beats per minute above "
                f"zero, found {value!r}."
            )
            continue
        bounds[key] = value
    floor = bounds.get("tempo_floor", DEFAULT_TEMPO_FLOOR)
    ceiling = bounds.get("tempo_ceiling", DEFAULT_TEMPO_CEILING)
    if isinstance(floor, int) and isinstance(ceiling, int) and floor >= ceiling:
        problems.append(
            f"analysis.tempo_floor must be below analysis.tempo_ceiling, found "
            f"{floor} and {ceiling}. The head names a tempo inside that window, "
            f"and an empty window names none."
        )
    return problems


def _validate_drift_cut(data: Mapping) -> list[str]:
    """The drift cut is a finite percent above zero (U157).

    Zero or below would mark every track ``dyn``, and a NaN would mark none
    while every row read as checked.
    """
    key = "analysis.drift_cut"
    value = _dig(data, key)
    if value is None:
        return []
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
        or value > 100
    ):
        return [
            f"{key} must be a percent above zero and at most 100, the drift at or "
            f"above which a track is marked dyn, found {value!r}."
        ]
    return []


def _validate_recognition(data: Mapping) -> list[str]:
    """The recognition host and the monthly call bound (R-301)."""
    problems: list[str] = []
    host = _dig(data, "recognition.host")
    if host is not None:
        problem = recognition_host_problem(host)
        if problem is not None:
            problems.append(problem)
    key = "recognition.monthly_calls"
    bound = _dig(data, key)
    if bound is not None and (
        not isinstance(bound, int) or isinstance(bound, bool) or bound < 1
    ):
        problems.append(
            f"{key} must be a positive whole number of paid recognition calls, "
            f"found {bound!r}. There is no value that switches the bound off; a "
            f"person on a larger plan writes a larger number."
        )
    return problems


def is_inside(child: Path, parent: Path) -> bool:
    """True when ``child`` is ``parent`` or sits under it. Purely textual.

    No ``resolve()`` or ``exists()`` (Rule 1); ``normpath`` collapses ``..`` so
    a typed path cannot escape by spelling.
    """
    child_parts = Path(os.path.normpath(str(child))).parts
    parent_parts = Path(os.path.normpath(str(parent))).parts
    return child_parts[: len(parent_parts)] == parent_parts


#: The shape ``library.db_outside_root_acknowledged_on`` must take, anchored at
#: both ends.
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ACKNOWLEDGMENT_KEY = "library.db_outside_root_acknowledged_on"


def _validate_acknowledgment_date(value: object) -> list[str]:
    """Shape-check the containment acknowledgment. It is a date, never a flag.

    A merely truthy value such as ``no`` would switch the refusal off. It must
    be a real calendar date so a later run can compare it to today; the pattern
    runs before ``fromisoformat`` to refuse the compact ``20260801`` form.
    """
    if not isinstance(value, str) or not _ISO_DATE.match(value.strip()):
        return [
            f"{ACKNOWLEDGMENT_KEY} must be an ISO calendar date (YYYY-MM-DD), "
            f"found {value!r}. It records WHEN the non-atomic-snapshot "
            f"consequence was accepted, so it is a date rather than a flag: a "
            f"value that is merely non-empty would switch the containment "
            f"refusal off while saying nothing a later run could check."
        ]
    try:
        date.fromisoformat(value.strip())
    except ValueError:
        return [
            f"{ACKNOWLEDGMENT_KEY} is date-shaped but is not a real calendar "
            f"date: {value!r}. An unparseable acknowledgment is not an "
            f"acknowledgment, so the containment rule still applies."
        ]
    return []


def _validate_db_containment(data: Mapping) -> list[str]:
    """The containment rule for the rekordbox database (KTD21b).

    See ``LibraryConfig.db_outside_root_acknowledged_on`` for why. Decided
    against the effective root, overrides applied.
    """
    root = _dig(data, "library.root")
    db_path = _dig(data, "library.db_path")
    acknowledged = _dig(data, "library.db_outside_root_acknowledged_on")

    problems: list[str] = []
    accepted = False
    if acknowledged is not None:
        # Shape-checked even when the database is inside the root.
        shape_problems = _validate_acknowledgment_date(acknowledged)
        problems += shape_problems
        accepted = not shape_problems

    if not isinstance(root, str) or not isinstance(db_path, str):
        return problems  # a missing required key is already reported by the caller
    if not root.strip() or not db_path.strip():
        return problems
    if is_inside(Path(db_path), Path(root)):
        return problems
    if accepted:
        return problems
    return problems + [
        f"library.db_path ({db_path!r}) is not under library.root ({root!r}). "
        f"KTD21b captures the database and its coupled state in one atomic "
        f"commit, and the only atomic commit available is a rename, which is "
        f"atomic within one filesystem and not across two. A database on another "
        f"volume makes every snapshot a non-atomic copy, so it is permitted only "
        f"as a recorded decision: library.db_outside_root_acknowledged_on carries "
        f"the date that consequence was accepted."
    ]


def _mount_path_problem(key: str, volume_id: str) -> list[str]:
    """Refuse a volume identity that is shaped like a path. One rule, two keys.

    R38 identifies a volume by recorded identity, never by mount path, or the
    next drive mounted there would pass. Shared by ``library.volume_id`` and
    each prefix rule's ``volume_id``.
    """
    if volume_id.startswith(("/", "\\")) or ":\\" in volume_id:
        return [
            f"{key} looks like a mount path ({volume_id!r}). "
            f"Record the volume's own identity, a UUID or serial, so a "
            f"different drive mounted at the same path fails the assertion "
            f"instead of passing it (R38)."
        ]
    return []


def _validate_prefix_map(raw: object) -> list[str]:
    """Validate the ordered array-of-tables prefix map (S1)."""
    if raw is None:
        return []
    if not isinstance(raw, list):
        return [
            "library.location_prefix_map must be an ordered array of tables, each "
            "with 'from' and 'to'. Order is load-bearing: one prefix can be "
            "another's prefix, and first match wins."
        ]
    problems: list[str] = []
    for index, entry in enumerate(raw):
        where = f"library.location_prefix_map[{index}]"
        if not isinstance(entry, Mapping):
            problems.append(f"{where} must be a table with 'from' and 'to'")
            continue
        for toml_key, _ in _PREFIX_TOML_KEYS:
            value = entry.get(toml_key)
            if not isinstance(value, str) or not value:
                problems.append(f"{where}.{toml_key} must be a non-empty string")
        to_value = entry.get("to")
        if isinstance(to_value, str):
            unknown = _unknown_tokens(to_value)
            if unknown:
                problems.append(
                    f"{where}.to contains unsupported interpolation "
                    f"{', '.join(sorted(unknown))}; only {LIBRARY_ROOT_TOKEN} is "
                    f"interpolated"
                )
        if PREFIX_VOLUME_IDENTITY_KEY in entry:
            # Present and unusable is a problem, never read as "none recorded",
            # which would let the check pass on a mistyped value.
            identity = entry[PREFIX_VOLUME_IDENTITY_KEY]
            key = f"{where}.{PREFIX_VOLUME_IDENTITY_KEY}"
            if not isinstance(identity, str) or not identity.strip():
                problems.append(
                    f"{key} must be a non-empty string when it is given; leave "
                    f"the key out for a target inside the library root"
                )
            else:
                problems += _mount_path_problem(key, identity)
    return problems


def _unknown_tokens(text: str) -> set[str]:
    """Every ``{...}`` token in ``text`` that is not the one supported token."""
    found: set[str] = set()
    rest = text
    while "{" in rest:
        start = rest.index("{")
        if "}" not in rest[start:]:
            break
        end = rest.index("}", start)
        token = rest[start : end + 1]
        if token != LIBRARY_ROOT_TOKEN:
            found.add(token)
        rest = rest[end + 1 :]
    return found


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


def derived_backup_remote(data: Mapping) -> str | None:
    """The remote name the destinations carry, when the file spells none.

    None when ``backup.remote`` is set, so the file's value wins, or when no
    destination is set, so the backup verb's refusal still names it. Public so
    the wizard writes the same derivation into the file.
    """
    remote = _dig(data, "backup.remote")
    if isinstance(remote, str) and remote.strip():
        return None
    for key in BACKUP_DESTINATION_KEYS:
        name = backup_remote_name(_dig(data, key))
        if name is not None:
            return name
    return None


def _build(cls, raw: Mapping, *, overrides: Mapping[str, object] | None = None):
    """Construct one schema dataclass from a raw mapping.

    Unknown keys are ignored: a newer build's file is refused by version, so a
    stray key is a hand edit and should not lock the user out.
    """
    kwargs: dict[str, object] = {}
    for f in fields(cls):
        if overrides and f.name in overrides and overrides[f.name] is not None:
            kwargs[f.name] = overrides[f.name]
            continue
        if f.name not in raw:
            continue
        kwargs[f.name] = _coerce(f.type, raw[f.name])
    return cls(**kwargs)


def _outbound(raw: Mapping) -> OutboundConfig:
    """The outbound section, the skip list held as a tuple so the frozen config stays hashable."""
    built = _build(OutboundConfig, raw)
    return replace(built, pair_skip_folders=tuple(str(one) for one in built.pair_skip_folders))


def _acquisition(raw: Mapping) -> AcquisitionConfig:
    """The acquisition section, with a retired adapter name read as its current one."""
    built = _build(AcquisitionConfig, raw)
    current = current_adapter_name(built.adapter)
    if current == built.adapter:
        return built
    return replace(built, adapter=current)


def _coerce(annotation, value):
    """Turn a TOML scalar into the field's declared type. Paths and floats only."""
    text = annotation if isinstance(annotation, str) else getattr(annotation, "__name__", "")
    if "Path" in text and isinstance(value, str):
        return Path(value)
    if "float" in text and isinstance(value, int) and not isinstance(value, bool):
        return float(value)
    return value


def _to_toml_value(value):
    """Recursively convert a schema object into TOML-safe, sorted plain data."""
    if is_dataclass(value) and not isinstance(value, type):
        out: dict[str, object] = {}
        for f in sorted(fields(value), key=lambda f: f.name):
            item = getattr(value, f.name)
            if item is None:
                continue  # TOML has no null; absent and null are the same state
            converted = _to_toml_value(item)
            # An empty table means what its absence means; emitting one would
            # change the fingerprint of an unchanged meaning (KTD9).
            if isinstance(converted, dict) and not converted:
                continue
            out[f.name] = converted
        return _apply_toml_key_aliases(value, out)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {k: _to_toml_value(value[k]) for k in sorted(value)}
    if isinstance(value, tuple | list):
        return [_to_toml_value(v) for v in value]
    return value


def _apply_toml_key_aliases(source, out: dict) -> dict:
    """Reshape the two dataclasses whose TOML form differs from their field names.

    ``PrefixMapping`` uses ``from`` and ``to`` on disk, since ``from`` cannot be
    a Python field name. ``ModulesConfig`` flattens to one key per module under
    ``[modules]``; the ``explicit`` wrapper is a code concern only.
    """
    if isinstance(source, PrefixMapping):
        aliased = {toml_key: out[field_name] for toml_key, field_name in _PREFIX_TOML_KEYS}
        if PREFIX_VOLUME_IDENTITY_KEY in out:
            aliased[PREFIX_VOLUME_IDENTITY_KEY] = out[PREFIX_VOLUME_IDENTITY_KEY]
        return aliased
    if isinstance(source, ModulesConfig):
        return out.get("explicit", {})
    return out


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
    "ACKNOWLEDGMENT_KEY",
    "BACKUP_DESTINATION_KEYS",
    "CONFIG_FILENAME",
    "CURRENT_SCHEMA_VERSION",
    "LIBRARY_ROOT_TOKEN",
    "LIBRARY_STATE_LAYOUT_VERSION",
    "MIGRATIONS",
    "PRIVATE_DIR_MODE",
    "PRIVATE_FILE_MODE",
    "REQUIRED_KEYS",
    "RETIRED_ADAPTER_NAMES",
    "SET_WORKSPACE_DIRNAME",
    "SQLITE_SIDECARS",
    "STATE_FILES",
    "TAXONOMY_TEMPLATE_KEY",
    "VOLUME_IDENTITY_KEY",
    "AcquisitionConfig",
    "AnalysisConfig",
    "BackupConfig",
    "Config",
    "ConfigConflict",
    "ConfigCorrupt",
    "ConfigError",
    "ConfigInvalid",
    "ConfigLockUnavailable",
    "ConfigMissing",
    "ConfigTooNew",
    "InstallationArea",
    "LibraryConfig",
    "Medium",
    "Migration",
    "ModulesConfig",
    "NamingConfig",
    "PathsConfig",
    "PrefixMapping",
    "ProfileConfig",
    "RekordboxConfig",
    "RemediedError",
    "Remedy",
    "RollbackEffect",
    "Sidecar",
    "SnapshotRole",
    "StateFile",
    "StateRoot",
    "TaxonomyConfig",
    "append_durable_bytes",
    "atomic_write_bytes",
    "backup_remote_disagreement",
    "backup_remote_name",
    "derived_backup_remote",
    "config_dir",
    "config_path",
    "coupled_state_files",
    "current_adapter_name",
    "flush_to_disk",
    "from_dict",
    "installation_state_dir",
    "library_coupled_dir",
    "library_history_dir",
    "library_local_dir",
    "library_state_dir",
    "load",
    "load_from_path",
    "merge_changes",
    "migrate",
    "exclusive_lock",
    "flock_exclusive",
    "held",
    "is_inside",
    "lock_now",
    "lock_within",
    "mkdir_private",
    "out_of_band_effects",
    "provider_gate_dir",
    "read_bytes_if_present",
    "read_json",
    "read_json_as_text",
    "read_json_map",
    "rekey_records",
    "reset_cache",
    "save",
    "sidecar_paths",
    "snapshot_sources",
    "state_file",
    "state_files_for",
    "state_path",
    "template_name_is_usable",
    "update",
    "validate",
]
