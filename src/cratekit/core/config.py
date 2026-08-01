"""Configuration, the two state roots, and the frozen identity a queued job runs against.

TWO RULES GOVERN THIS MODULE. Both are here because the source system's
equivalent survived four years without drifting, and the reason it did is that
its docstring stated its rule and the rule was checkable.

**Rule 1: nothing here touches the filesystem at import.** No mkdir, no write,
no existence check, no read. This is what lets ``crate --help``, and the health
check beside it, run on a machine that has never been set up, which is the only
way a first-run wizard can ever be reached. The source module got this for free
because it read environment variables only. Cratekit's config is a FILE, so it
cannot resolve at import without breaking the rule. The resolution is that
config is LAZY: ``config_dir()``, ``config_path()``, and ``load()`` are
functions, none of them run at import, and there is no module-level path
constant for anything else to snapshot.

That last clause is load-bearing. In the source system seventeen modules bound a
state-directory path at their OWN import time. Reloading config after that point
changed the config module and changed nothing else, so half the package tracked
the new value and half kept the old one, silently, forever. There is no such
constant here to bind, and ``tests/test_config.py`` fails the build if a module
grows one.

**Rule 2: if a value can change without the user deciding it changed, it is
state, not config.** Config carries decisions. Watermarks, tombstones, declines,
lock state, calibration data, session logs, cached tokens, and the active
taxonomy template are all things the software changes on its own, so none of
them live in the config file. They live in one of the two state roots below.

---

THE TWO STATE ROOTS (KTD21). This is the heart of the module.

* **Installation-scoped**, under the platform's per-user config and state
  directories: config, credentials, the job queue, and caches that describe a
  remote account or a replayable lookup rather than a library.
* **Library-scoped**, in a dot-directory beside the library itself: the write
  lock, the session log and its snapshots, per-source watermarks, tombstones and
  declines, the deletion watermark, analysis calibration, the tree registry, and
  the active taxonomy template.

The source system stores essentially all of its state per installation. Carrying
that forward breaks three concrete scenarios, and ``STATE_FILES`` below records,
per entry, which one it breaks:

1. **A second install against one library.** Two installation roots means two
   write-lock files, which means zero mutual exclusion against a database that
   only ever had one copy.
2. **A reinstall or a fresh clone.** Two of the ported files are undo logs: the
   only surviving record of a value that was overwritten on disk. Losing them to
   a reinstall is unrecoverable data loss against the user's own music files.
3. **The migration overlap**, where the old system and Cratekit both run against
   one library. Locks that live per installation can never contend. A lock beside
   the library is the only shape that both systems can open.

``STATE_FILES`` assigns every entry to exactly ONE root. None straddles. Two
source entries that did straddle are split into two named files each, one per
root, which is the only way "exactly one" can be true of them.

The installation root spans two PHYSICAL directories, the platform's config
directory and its state directory, so each installation entry also names which of
the two it lives in (``installation_area``). That is not a third KTD21 root; it is
the resolver being able to say where an entry actually is. Leaving it implicit is
how the config file itself came to be declared under the state directory while
every loader and saver read the config directory: on macOS platformdirs returns
one directory for both, so the two agreed by accident here and diverged on Linux.

---

THE SNAPSHOT BOUNDARY (KTD21b). The second thing every library-scoped entry
declares is what a RESTORE does to it, because the plan's top-ranked risk is the
registry rolling back while the database does not. Three answers, one
subdirectory each, so the coupled set is a directory boundary rather than a list
somebody has to keep in sync:

* ``COUPLED`` -> ``<state>/coupled/``. Captured with the database and replaced on
  restore. The registry, the watermarks, the tombstones, the declines, the active
  taxonomy, and the favorites state (R30 names most of these by name).
* ``SURVIVES_ROLLBACK`` -> ``<state>/history/``. The record of what is
  restorable. Rolling the session log back destroys the log of the sessions a
  user might restore, and capturing the snapshot store nests every prior snapshot
  inside the new one.
* ``NEVER_RESTORED`` -> ``<state>/local/``. Rolling it back is either active data
  loss or a broken invariant: the undo logs hold the ONLY surviving copy of values
  already overwritten on the user's files, and a restore that replaces a directory
  holding a lock swaps the inode a live advisory lock is held on, so mutual
  exclusion disappears mid-session with nothing raised.

U8 and U32 derive the snapshot set from this field (``coupled_state_files`` and
``snapshot_sources``). A hand-maintained exclusion list is the drift this
repository already refuses for its CI dependency list and its extras table.
"""

from __future__ import annotations

import copy
import hashlib
import os
import re
import tempfile
import tomllib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import date
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType

import platformdirs
import tomli_w

from cratekit.core import profiles

# ---------------------------------------------------------------------------
# Schema version and the file name
# ---------------------------------------------------------------------------

#: The schema this build writes and validates. Bumped only alongside a migration
#: entry in ``MIGRATIONS``; ``test_config_migration.py`` fails on a gap, so the
#: version number can never get ahead of the code that upgrades to it.
CURRENT_SCHEMA_VERSION = 1

#: The on-disk SHAPE of the library state directory: which subdirectory each
#: entry's snapshot role resolves into. Deliberately a second number, separate
#: from ``CURRENT_SCHEMA_VERSION``, because the two need different mechanisms and
#: only one of those mechanisms exists in this module.
#:
#: NOTHING MIGRATES AN EXISTING LIBRARY STATE DIRECTORY, AND THAT IS A RECORDED
#: DEFERRAL RATHER THAN AN OVERSIGHT. ``MIGRATIONS`` is dict-to-dict by
#: construction, which is exactly what makes "a failed migration leaves the
#: original untouched" true by construction rather than by a cleanup path that
#: can itself fail. The same purity makes it structurally incapable of moving a
#: file, so it can never be the thing that reconciles a LAYOUT change.
#:
#: At version 1 there is nothing to reconcile. The role subdirectories
#: (``coupled/``, ``history/``, ``local/``) were introduced before this package
#: had any write path at all, so no build has ever written a library state
#: directory in another shape and there is no installation on disk to move.
#:
#: The day this number moves, the unit that moves it owns a one-time on-disk
#: reconciliation with its OWN mechanism: a directory walk under the same
#: exclusive lock a config migration takes, idempotent, and refusing rather than
#: half-moving. ``tests/test_config.py`` fails on a bump that arrives without
#: one, so the deferral expires rather than persisting.
LIBRARY_STATE_LAYOUT_VERSION = 1

CONFIG_FILENAME = "config.toml"

#: The key U31's destructive-operation assertion reads (R38). Named here so the
#: unit that implements the assertion does not spell the key itself: a guard that
#: hardcodes the name of the thing it guards stops guarding it the day it is
#: renamed, and nothing fails.
VOLUME_IDENTITY_KEY = "library.volume_id"

# Environment overrides. Exactly three, mirroring the source system's three,
# and each one RELOCATES a configured value. None of them SUPPLIES one.
#
# That distinction is the whole design. An override that can supply a value lets
# a machine with no setup at all resolve a library root from the environment and
# start writing to it, which is precisely the "runs against the wrong volume"
# failure R38 exists to prevent. An override that can only relocate an
# already-configured value is useful for tests, for a remounted drive, and for
# nothing else.
#
# THEY ARE APPLIED IN EXACTLY ONE PLACE, ``_apply_env_overrides``, BEFORE ANY
# RULE IS DECIDED. That placement is the fix for a defect with two faces and one
# cause. Validation used to dig ``library.root`` out of the raw file mapping
# while the BUILDER applied the override, so the containment rule was decided
# against the file's root and then lived against a different one. Both faces were
# reproduced: a config that violates containment at runtime validated clean, and
# a single save under a relocation wrote a root that the file's own db_path was
# no longer under, producing a file that refused to load and that the user had
# never edited.
#
# Relocating the root also RE-BASES a db_path that sat under it. That is what
# "relocate" has to mean here: what the file records is where the database sits
# RELATIVE to the library, so moving the library without moving the database
# leaves a path aimed into a tree that is no longer the library. It is also a
# safety property the test suite has been relying on without stating it, since
# redirecting the library root is the whole mechanism keeping tests off the real
# rekordbox database.
ENV_CONFIG_DIR = "CRATEKIT_CONFIG_DIR"
ENV_STATE_DIR = "CRATEKIT_STATE_DIR"
ENV_LIBRARY_ROOT = "CRATEKIT_LIBRARY_ROOT"
ENV_DOWNLOAD_STAGING = "CRATEKIT_DOWNLOAD_STAGING"

_APP_NAME = "cratekit"


# ---------------------------------------------------------------------------
# Failure vocabulary
#
# Five types, not one. Each has a DIFFERENT remediation, and collapsing them
# into a single ConfigError would force every caller to parse a message string
# to find out what to tell the user (KTD25).
# ---------------------------------------------------------------------------


class Remedy(StrEnum):
    """What to do about a configuration failure, as a TOKEN rather than a command.

    D2: no foundation module contains the text a user types. The CLI layer, and
    only the CLI layer, renders one of these into a command line, because the
    command depends on the interface the user is actually sitting in front of and
    this layer does not know which one that is.

    The alternative, which this module shipped first, is remediation as prose
    inside the message string. A caller that wants to tell a user what to do
    about a missing config versus a too-new one then has to string-match the
    message, which is exactly the KTD25 failure this module's own docstring
    cites. ``secrets.py`` in the same unit already models it correctly; these
    tokens are this module's contribution to the vocabulary U5 owns (S4), not a
    competing scheme.
    """

    RUN_SETUP = "run-setup"
    REPAIR_CONFIG_FILE = "repair-config-file"
    UPGRADE_CRATEKIT = "upgrade-cratekit"
    FIX_CONFIG_VALUES = "fix-config-values"
    RETRY_WHEN_UNLOCKED = "retry-when-unlocked"
    RECORD_REKORDBOX_PIN = "record-rekordbox-pin"


class ConfigError(Exception):
    """Base for every configuration failure. Always carries a structured remedy."""

    remedy: Remedy = Remedy.FIX_CONFIG_VALUES

    def __init__(self, message: str, *, remedy: Remedy | None = None) -> None:
        super().__init__(message)
        if remedy is not None:
            # Per-raise override, for the case where one type covers two
            # remediations. An unrecorded rekordbox pin is a ConfigInvalid whose
            # answer is one specific decision, not "go read your config file".
            self.remedy = remedy


class ConfigMissing(ConfigError):
    """No config file exists. Remedy token: ``RUN_SETUP``."""

    remedy = Remedy.RUN_SETUP


class ConfigCorrupt(ConfigError):
    """The file exists but cannot be read as a versioned config.

    Covers unparseable TOML and an absent or non-integer ``schema_version``.
    An absent version is corruption rather than age: Cratekit has written the
    field since its first release, so a file without one was hand-edited.
    """

    remedy = Remedy.REPAIR_CONFIG_FILE


class ConfigTooNew(ConfigError):
    """The file was written by a newer Cratekit. Migrations are forward-only.

    Downgrading is never attempted. A newer build may have written keys this
    build would silently drop on the next save, and a silent drop of a key the
    user set is worse than a refusal that names the two versions.
    """

    remedy = Remedy.UPGRADE_CRATEKIT


class ConfigInvalid(ConfigError):
    """The config parsed but failed validation.

    Carries EVERY problem, not the first. Validation that stops at the first
    missing key turns one setup session into one round trip per missing key,
    and the plan's first test scenario for this unit requires each missing key
    to be named.
    """

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
    """A config migration could not take the exclusive lock, so it refused.

    Advisory ledgers in the source system tolerate a failed ``flock`` and carry
    on. A config MIGRATION must not: the job engine re-invokes the CLI as
    subprocesses (KTD26), so two processes can reach an unmigrated file in the
    same second, and two unsynchronized migrations of one file is how a config
    ends up half-upgraded.
    """

    remedy = Remedy.RETRY_WHEN_UNLOCKED


# ---------------------------------------------------------------------------
# Directory resolution. Functions, never constants (Rule 1).
# ---------------------------------------------------------------------------


def config_dir() -> Path:
    """The installation-scoped configuration directory.

    Resolved through platformdirs rather than a hardcoded path so the deferred
    Windows adapter costs nothing here (KTD6, R1). The override exists for tests
    and for a user who keeps their dotfiles somewhere unusual.

    Creates nothing. A caller that is about to write creates it at that moment.
    """
    override = os.environ.get(ENV_CONFIG_DIR)
    if override:
        return Path(override)
    return Path(platformdirs.user_config_dir(_APP_NAME))


def config_path() -> Path:
    """The path of the config file itself. Does not check that it exists.

    Resolved THROUGH the inventory rather than beside it. Composing
    ``config_dir() / CONFIG_FILENAME`` here is what let the inventory declare the
    config file under the installation STATE directory while every loader and
    saver used the installation CONFIG directory: two roots for one file, invisible
    on macOS where platformdirs returns the same directory for both. Going through
    ``state_path`` makes the two answers the same answer by construction.
    """
    return state_path("config")


def installation_state_dir() -> Path:
    """The installation-scoped STATE directory, distinct from the config directory.

    Kept separate rather than folded into the config directory because the two
    have different backup semantics on every platform Cratekit targets: a user
    who syncs their config directory between machines would otherwise sync a job
    queue and a set of caches that describe one machine's work in progress.
    """
    override = os.environ.get(ENV_STATE_DIR)
    if override:
        return Path(override)
    return Path(platformdirs.user_state_dir(_APP_NAME))


def library_state_dir(config: Config) -> Path:
    """The library-scoped state root: a dot-directory beside the library.

    Beside the library and not inside the platform state directory, because
    everything in here describes THIS library and must travel with it, be
    snapshotted with it (KTD21b), and be reachable from a second installation
    and from the old system during the migration overlap.
    """
    return config.library.root / config.library.state_dirname


def library_coupled_dir(config: Config) -> Path:
    """The one directory a KTD21b snapshot copies and a restore replaces.

    Named as a function so U8 and U32 can say "snapshot this directory" instead of
    keeping a list of files in sync with ``STATE_FILES``. Everything inside it is
    declared ``COUPLED``; nothing that is not is allowed in, and
    ``tests/test_config.py`` asserts both halves.
    """
    return library_state_dir(config) / _LIBRARY_SUBDIR_BY_ROLE[SnapshotRole.COUPLED]


def library_history_dir(config: Config) -> Path:
    """Where the record of what is restorable lives: the session log and snapshots.

    Outside the coupled directory on purpose. A snapshot that captured this would
    nest every previous snapshot inside itself, and a restore that replaced it
    would destroy the log of the sessions the user might still want to restore.
    """
    return library_state_dir(config) / _LIBRARY_SUBDIR_BY_ROLE[SnapshotRole.SURVIVES_ROLLBACK]


def library_local_dir(config: Config) -> Path:
    """Library state a restore must never touch: locks, undo logs, caches, calibration.

    Two different failures share this directory. Rolling an undo log back discards
    the only surviving copy of a value already overwritten on the user's files.
    Replacing a directory that holds a lock file swaps the inode a live advisory
    lock is held on, so two processes both believe they hold it and neither is
    told otherwise.
    """
    return library_state_dir(config) / _LIBRARY_SUBDIR_BY_ROLE[SnapshotRole.NEVER_RESTORED]


# ---------------------------------------------------------------------------
# The state-file inventory
# ---------------------------------------------------------------------------


class StateRoot(StrEnum):
    """Which of the two roots an entry lives under. There are only two."""

    INSTALLATION = "installation"
    LIBRARY = "library"


class InstallationArea(StrEnum):
    """Which physical directory an INSTALLATION entry lives in.

    Not a third KTD21 root. The installation root has always spanned two
    directories, the platform's config directory and its state directory, and
    those have different backup and sync semantics on every platform Cratekit
    targets. What was missing was any way for an ENTRY to say which one it meant,
    so the resolver guessed one and the loader used the other. On macOS
    platformdirs returns the same path for both, so the disagreement was invisible
    on the machine this was written on.

    Read only when ``root is StateRoot.INSTALLATION``. Library entries leave it at
    the default, and ``tests/test_config.py`` asserts they do, so it can never
    look meaningful where nothing reads it.
    """

    CONFIG = "config"
    STATE = "state"


class SnapshotRole(StrEnum):
    """What a KTD21b restore does to this entry. Declared, never inferred.

    The plan's top-ranked risk is the registry rolling back while the database
    does not, so this is the field that risk turns on. Its three values are the
    three incompatible categories that a single flat state directory mixed
    together, and each one maps to its own subdirectory so the boundary between
    them is a directory rather than a list a later unit has to maintain.
    """

    #: Captured with the database and replaced on restore. Restoring returns the
    #: library to a self-consistent pre-session state only if this set is exact.
    COUPLED = "coupled"

    #: The record of WHAT is restorable, plus the snapshots themselves. Rolling it
    #: back destroys that record; capturing it nests every prior snapshot inside
    #: the new one.
    SURVIVES_ROLLBACK = "survives-rollback"

    #: Never captured, never replaced. Either its rollback is active data loss (an
    #: undo log holds the only copy of a value already written to the user's files,
    #: and a file write is not something a database restore undoes), or its
    #: identity is live (a lock's inode, a heartbeat, a run in progress), or it
    #: simply is not library state at all (everything installation-scoped: a
    #: library snapshot has no business reaching outside the library).
    NEVER_RESTORED = "never-restored"


#: One subdirectory per role, so an entry's physical location is DERIVED from the
#: answer it already gave rather than typed a second time. A relative path spelled
#: per entry could disagree with the entry's own declared role; this cannot.
_LIBRARY_SUBDIR_BY_ROLE: Mapping[SnapshotRole, str] = MappingProxyType(
    {
        SnapshotRole.COUPLED: "coupled",
        SnapshotRole.SURVIVES_ROLLBACK: "history",
        SnapshotRole.NEVER_RESTORED: "local",
    }
)


class Medium(StrEnum):
    """What the entry physically is.

    ``KEYCHAIN`` is in this enum rather than being left out of the table because
    the Definition of Done requires every state file to be dispositioned, and
    "this one stopped being a file" is a disposition. Leaving it out would make
    the table look complete while the sharpest credential exposure in the source
    system, a long-lived refresh token in a default-permission file, quietly had
    no row.
    """

    FILE = "file"
    DIRECTORY = "directory"
    KEYCHAIN = "keychain"


@dataclass(frozen=True, slots=True)
class Sidecar:
    """A file the storage engine keeps BESIDE an entry, named by a suffix.

    Declared here rather than kept as a companion list in the unit that captures
    snapshots, for the reason every other field in this schema is declared: a
    list maintained beside the schema is the drift this whole design exists to
    remove, and here the cost of that drift is a torn database.

    THE CONCRETE FAILURE. SQLite in WAL mode holds committed-but-uncheckpointed
    transactions in ``<db>-wal`` and a shared index over them in ``<db>-shm``.
    The database row declares ONE path, so a consumer that copies exactly what
    ``snapshot_sources`` names, and no more, captures a database missing every
    transaction still in the log. That copy opens cleanly and is silently behind,
    which is the worst shape a backup can take. The source system captures the
    database and both sidecars as one matched set; this is that set, declared.
    """

    suffix: str
    #: True when a restore writes this sidecar back OUT of the snapshot.
    #:
    #: The source system's restore is deliberately asymmetric: it removes the
    #: LIVE ``-wal`` and ``-shm`` first, so the engine cannot replay a log
    #: belonging to the database that was just replaced, then copies the
    #: snapshot's ``-wal`` and never its ``-shm``. The shared-memory index is
    #: derived from the log, so restoring a stale one beside a fresh log hands
    #: SQLite two disagreeing views of one database.
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

    ``why`` is not documentation for its own sake. Every future unit that adds
    state has to answer the same question, and the answer is only checkable if
    it is phrased as a failure: what breaks under a second install, under a
    reinstall, or during the migration overlap.

    ``snapshot`` carries no default, so the same is true of the KTD21b question.
    A new entry cannot be added without deciding whether a restore rolls it back,
    which is the decision that the plan's top-ranked risk turns on.
    """

    key: str
    root: StateRoot
    medium: Medium
    relative: str
    why: str
    #: What a KTD21b restore does to this entry. Required: see the class docstring.
    snapshot: SnapshotRole
    #: Which physical installation directory this lives in. Read only when
    #: ``root is StateRoot.INSTALLATION``.
    installation_area: InstallationArea = InstallationArea.STATE
    #: True when the ported shape keys its records on a playlist or folder
    #: DISPLAY name. R19 and D5 forbid that, so the unit that owns the entry runs
    #: the one-time re-key in ``rekey_records`` before first use.
    rekey_from_display_name: bool = False
    #: True when the entry sits at the library ROOT rather than inside the
    #: library state directory. Only things another system has to find without
    #: knowing Cratekit's layout belong here.
    at_library_root: bool = False
    #: Files that share this entry's path with a suffix and must be captured with
    #: it as ONE matched set. Empty for everything that really is a single file.
    #:
    #: EVERY ONE OF THEM MAY LEGITIMATELY BE ABSENT, and a consumer must treat
    #: absence as normal rather than as an error: a database that has just been
    #: checkpointed, or that was never opened in WAL mode, has no sidecars on
    #: disk at all. The source system copies each one only if it exists, and so
    #: must anything reading this field.
    sidecars: tuple[Sidecar, ...] = ()


STATE_FILES: tuple[StateFile, ...] = (
    # ── Installation-scoped ────────────────────────────────────────────────
    #
    # Every entry here is NEVER_RESTORED for one shared reason: a library snapshot
    # covers a library. Reaching outside it to roll back a job queue or a
    # credential index would roll back work that belongs to the MACHINE, and on a
    # second install it would roll back state the restoring machine has never seen.
    StateFile(
        key="config",
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative=CONFIG_FILENAME,
        why=(
            "Config records decisions about THIS machine: which library is "
            "mounted where, which adapter, which modules. Two machines "
            "legitimately answer those differently for one library, so a shared "
            "config would force one machine's mount path onto the other."
        ),
        snapshot=SnapshotRole.NEVER_RESTORED,
        # The CONFIG directory, not the state directory. This is the entry whose
        # area was implicit and therefore wrong: the loader and saver read
        # config_dir() while the inventory resolved installation_state_dir(),
        # which are the same path on macOS and different everywhere else.
        installation_area=InstallationArea.CONFIG,
    ),
    StateFile(
        key="credentials",
        root=StateRoot.INSTALLATION,
        medium=Medium.KEYCHAIN,
        relative="",
        snapshot=SnapshotRole.NEVER_RESTORED,
        why=(
            "Was a plaintext env file whose 0600 came from the author's umask "
            "rather than from any code, so on a machine with a laxer umask it "
            "landed world readable. A credential is an account fact, not a "
            "library fact: the same account serves every library, and no library "
            "should carry a credential a second user of that library can read."
        ),
    ),
    StateFile(
        key="provider_session",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.KEYCHAIN,
        relative="",
        why=(
            "A long-lived refresh token written by a third-party library that "
            "does no chmod at all. Stored as ONE blob under one key so the token, "
            "its refresh token, and the session fields cannot be updated apart "
            "and leave a half-refreshed session that authenticates once and then "
            "fails in a way that looks like a service outage."
        ),
    ),
    StateFile(
        key="provider_folder_cache",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative="provider_folder_cache.json",
        why=(
            "Remote folder identifiers keyed by year. It describes the remote "
            "ACCOUNT, not the library, and a second install that loses it "
            "re-derives it on the next run at the cost of one API call."
        ),
    ),
    StateFile(
        key="identify_usage",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative="identify_usage.json",
        why=(
            "The monthly call counter for the identification service. It is "
            "bound to the CREDENTIAL's quota, not to a library: two libraries "
            "identified on one account share one quota, so one counter beside "
            "the credential is the only placement that can tell the truth."
        ),
    ),
    StateFile(
        key="identify_usage_lock",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative="identify_usage.lock",
        why=(
            "A sibling lock serializing the read-modify-write of the counter "
            "beside it. It follows its file to the same root by necessity: a lock "
            "under a different root than the thing it protects is a lock two "
            "processes can each hold while both edit the same file."
        ),
    ),
    StateFile(
        key="genre_lookup_cache",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative="genre_lookup_cache.json",
        why=(
            "A cache of third-party catalog lookups keyed by track. Every entry "
            "is replayable from the network, so losing it costs time and no data. "
            "It also has nothing to do with which library asked."
        ),
    ),
    StateFile(
        key="label_crawl_cache",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.DIRECTORY,
        relative="label_crawl",
        why=(
            "Half of a source directory that straddled both roots (D4). The crawl "
            "half is what a catalog lookup returned: replayable, library-agnostic, "
            "and 53 directories of it live in the source install. What actually "
            "LANDED in a library is the other half, and it is library-scoped."
        ),
    ),
    StateFile(
        key="label_intent",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative="label_intent.json",
        why=(
            "Half of a file that straddled both roots (D4). This half is curated "
            "intent: the labels a user chose to follow and how deep to sweep them. "
            "In the source system the whole file is COMMITTED TO GIT, so cloning "
            "the repository hands every friend one person's label list AND their "
            "watermarks. Splitting it makes the intent half exportable on purpose "
            "and leaves the watermarks where they belong."
        ),
    ),
    StateFile(
        key="credential_index",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative="credential_index.json",
        why=(
            "The NAMES of the credentials this installation has recorded, never "
            "their values. It exists so doctor can answer 'is a credential set' "
            "without retrieving one, which on macOS would raise the keychain's "
            "authorization prompt during a health check that is supposed to be "
            "unattended."
        ),
    ),
    StateFile(
        key="job_queue",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.DIRECTORY,
        relative="jobs",
        why=(
            "KTD21 names the job queue installation-scoped, and it is: a detached "
            "job belongs to the machine running it. One consequence follows and "
            "the unit that builds the queue owns it: because the queue is per "
            "install and a library is per config, a job record must NAME the "
            "library it targets, or a queue drained after the user reconfigures "
            "runs against the wrong volume."
        ),
    ),
    StateFile(
        key="run_state",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.DIRECTORY,
        relative="runs",
        why=(
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
            "exists."
        ),
    ),
    StateFile(
        key="app_token",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative="app_token",
        why=(
            "A random token minted per server start for the local control plane. "
            "It is not a service credential and must NOT survive a restart, which "
            "is exactly why it stays a file with explicit 0600 rather than "
            "joining the keychain."
        ),
    ),
    StateFile(
        key="dashboard_snapshot",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
        relative="dashboard_snapshot.json",
        why=(
            "Last-good render numbers so a dashboard still draws when the volume "
            "is unmounted. Pure presentation cache: if it were library-scoped it "
            "would be unreadable in exactly the situation it exists to serve."
        ),
    ),
    # ── Library-scoped ─────────────────────────────────────────────────────
    StateFile(
        key="rekordbox_db",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        # Composed from library.db_path rather than from a relative literal: the
        # database's location is the user's decision, made in rekordbox, not ours.
        relative="",
        why=(
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
            "surprise at the first snapshot."
        ),
        # The only entry with sidecars, and the only one that needs them: it is
        # the only SQLite database in the inventory. Declaring them here is what
        # keeps the KTD21b capture set derived rather than hand-listed by U8.
        sidecars=SQLITE_SIDECARS,
    ),
    StateFile(
        key="write_lock",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="write.lock",
        why=(
            "KTD17 and R31, non-negotiable. In the source system this is a flock "
            "on a path under the installation root while the database it protects "
            "travels with the library, so a second install holds a lock the first "
            "install cannot see and both open the database at once. During the "
            "migration overlap the old system must be able to open this exact "
            "file, which only a path beside the library can provide."
            " NEVER_RESTORED for a second reason: a restore that replaced the "
            "directory holding this file would swap the inode a live flock is "
            "held on, and every process holding the old one would keep believing "
            "it had exclusive access, with nothing raised."
        ),
    ),
    StateFile(
        key="session_lock",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="session.lock",
        why=(
            "The whole-run lock, held for a destructive session end to end (R31). "
            "Same failure as the write lock: per-installation placement makes two "
            "machines mutually invisible."
            " Same inode argument as the write lock: a restore must never "
            "replace the file a live lock is held on."
        ),
    ),
    StateFile(
        key="session_log",
        snapshot=SnapshotRole.SURVIVES_ROLLBACK,
        root=StateRoot.LIBRARY,
        medium=Medium.DIRECTORY,
        relative="sessions",
        why=(
            "The per-run state machine, the frozen plans, and the created-playlist "
            "ledger. Library-scoped for two reasons: KTD21b requires a snapshot to "
            "cover the database and this log ATOMICALLY, and during the overlap a "
            "Cratekit run that cannot read the old system's log treats its crash "
            "debris as fresh intake."
            " It SURVIVES a rollback rather than being part of one: rolling the "
            "log back would erase the record of which sessions are restorable, "
            "which is the one thing a user needs in order to restore again."
        ),
    ),
    StateFile(
        key="snapshots",
        snapshot=SnapshotRole.SURVIVES_ROLLBACK,
        root=StateRoot.LIBRARY,
        medium=Medium.DIRECTORY,
        relative="snapshots",
        why=(
            "The headline case in KTD21. Restore lives per installation in the "
            "source system while the database it restores lives per library, so a "
            "second machine simply cannot roll back the first machine's write. "
            "Beside the library, any installation can restore any session."
            " It SURVIVES a rollback for a structural reason as well as a "
            "practical one: a snapshot that captured the snapshot store would "
            "nest every previous snapshot inside the new one, and each capture "
            "would then cost the sum of every capture before it."
        ),
    ),
    StateFile(
        key="favorites_state",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="favorites_state.json",
        why=(
            "It records rekordbox row identifiers that have already been colored "
            "and tagged. A second install starts from an empty list and re-applies "
            "every one of them, turning what should be a no-op run into a full "
            "guarded write session against the live database, which is the highest "
            "risk operation in the product."
            " COUPLED: the rows it names are database rows, so a restore that "
            "rolled the database back without it would leave this file claiming "
            "work that no longer exists, and the next run would skip it."
        ),
    ),
    StateFile(
        key="favorites_state_lock",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="favorites_state.lock",
        why=(
            "A sibling lock serializing the read-modify-write of the state file "
            "beside it. Library-scoped for the same reason its file is: a lock in "
            "a per-installation directory is invisible to a second machine, so "
            "both would edit one library's record at once."
            " NEVER_RESTORED for the inode reason every lock here shares."
        ),
    ),
    StateFile(
        key="energy_calibration",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="energy_calibration.json",
        why=(
            "Cut points fitted against THIS library's own values. KTD21 names "
            "analysis calibration library-scoped, and the reason is that losing "
            "it does not just cost a re-fit: it silently changes where the same "
            "input track routes."
            " NEVER_RESTORED: the restamp these cut points drove wrote values "
            "into files on disk, and a database restore does not roll a file "
            "write back. Rolling the cut points back alone would describe a "
            "state the files are no longer in."
        ),
    ),
    StateFile(
        key="energy_feature_cache",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="energy_features.json",
        why=(
            "Per-file signal features keyed on this library's files. Losing it to "
            "a reinstall costs a full re-analysis pass over thousands of files."
            " NEVER_RESTORED: it is keyed on files, which do not roll back, and "
            "it is re-derivable, so a rollback costs a re-analysis and buys "
            "nothing."
        ),
    ),
    StateFile(
        key="energy_undo_log",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="energy_undo.json",
        why=(
            "The ONLY surviving copy of each file's pre-restamp energy value, "
            "which the restamp overwrote on disk. A reinstall that loses this is "
            "unrecoverable data loss against the user's own music files, and the "
            "source system's re-rate path refuses outright when it is absent."
            " Which is exactly why a restore must never roll it back: the values "
            "it protects were written to files, a database restore does not undo "
            "a file write, and discarding the log makes those writes permanent. "
            "Rolling this back is not a stale record, it is data loss."
        ),
    ),
    StateFile(
        key="vocal_calibration",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="vocal_calibration.json",
        why=(
            "The hand-set vocal cut, fitted against this library. Same failure as "
            "energy calibration: losing it changes routing outcomes for unchanged "
            "input, silently."
            " NEVER_RESTORED for the same reason as energy calibration: its "
            "effects already landed on files that do not roll back."
        ),
    ),
    StateFile(
        key="genre_gaps",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="genre_gaps.json",
        why=(
            "Counts of incoming genre strings that resolved to no folder in THIS "
            "library's taxonomy. The same string is a gap in one library and a "
            "match in another, so the count is meaningless anywhere else. Note "
            "the keys are external vendor strings, not taxonomy display names, "
            "which is why R19's re-key does not apply: the whole point of the "
            "record is that the string matched nothing we own."
            " NEVER_RESTORED: a gap observed is a fact about what arrived, not "
            "about what the database holds, and re-deriving it costs a pass."
        ),
    ),
    StateFile(
        key="genre_tag_undo_log",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="genre_tag_undo.json",
        why=(
            "The replay source for reverting tag writes made to files on disk, "
            "carrying each file's original value. Second undo log, same argument: "
            "a reinstall that loses it makes hundreds of on-disk tag writes "
            "permanent."
            " And the same argument against rolling it back: the writes it "
            "reverses are on disk, so a restore that discarded this log would "
            "make them permanent too."
        ),
    ),
    StateFile(
        key="playlist_parole_ledger",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="playlist_parole.json",
        why=(
            "First-seen dates for playlists sitting in the rotation's holding "
            "area. It describes this library's playlists and nothing else."
            " COUPLED: the playlists it dates are database rows. A restore that "
            "brought a playlist back while its first-seen date stayed at the "
            "rolled-forward value would put it straight past the rotation "
            "deadline and delete it early."
        ),
        rekey_from_display_name=True,
    ),
    StateFile(
        key="track_provider_id_cache",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="track_provider_ids.json",
        why=(
            "A map from file location to the provider's track identifier, keyed "
            "on THIS library's file paths. On another library every key misses, so "
            "an installation-scoped copy is a cache that can only ever be wrong "
            "or empty."
            " NEVER_RESTORED: keyed on file paths, which a database restore does "
            "not move, and re-derivable at the cost of lookups."
        ),
    ),
    StateFile(
        key="review_queue",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.DIRECTORY,
        relative="review",
        why=(
            "KTD12's one shared adjudication surface. Its items describe "
            "candidates for THIS library, and an item adjudicated on one machine "
            "must not be re-asked on another."
            " COUPLED: an adjudicated item becomes a decline, and R30 rolls "
            "declines back. Leaving the queue behind while the declines roll "
            "back would leave an item simultaneously queued and already decided."
        ),
    ),
    StateFile(
        key="label_outcomes",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.DIRECTORY,
        relative="label_outcomes",
        why=(
            "The other half of the split directory (D4): what a label sweep "
            "actually landed in this library. Distinct from the crawl cache, which "
            "is only what a lookup returned."
            " COUPLED for the same reason the watermarks are: it is a per-source "
            "audit record of what this library took in, and R25 is meaningless "
            "if it survives a rollback of the intake it describes."
        ),
    ),
    StateFile(
        key="label_watermarks",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="label_watermarks.json",
        why=(
            "The other half of the split registry file (D4). A watermark is a "
            "per-source audit record of what this library has already taken in "
            "(R25). Committed to git in the source system, which ships one "
            "person's sweep history to everyone who clones."
            " COUPLED, named by R30: a watermark that survives a rollback of the "
            "intake it recorded makes the next sync skip exactly the tracks the "
            "restore removed."
        ),
    ),
    StateFile(
        key="tree_registry",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="tree_registry.json",
        why=(
            "KTD22. Cutover mode and the adopted root's identifier describe one "
            "person's library. Committing them would ship the author's flips to "
            "every friend, and would leave the old system, which cannot read the "
            "new repository, unable to consult them at all. New state: the source "
            "system has no equivalent."
            " COUPLED, and it is the entry the plan's top-ranked risk is named "
            "after: the registry rolling back while the database does not, or "
            "the reverse, is the failure KTD21b exists to make impossible."
        ),
    ),
    StateFile(
        key="tombstones",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="tombstones.json",
        why=(
            "R36. A suppressed acquisition is a fact about what this library has "
            "deliberately declined to hold. New state; the source system has no "
            "equivalent, so there is nothing to port and the shape is chosen here."
            " COUPLED, named by R30."
        ),
    ),
    StateFile(
        key="declines",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="declines.json",
        why=(
            "R36's other half: candidates a human rejected. Library-scoped so the "
            "rejection is not re-asked from a second machine. New state."
            " COUPLED, named by R30, and paired with the review queue: the two "
            "roll back together or an item ends up both open and decided."
        ),
    ),
    StateFile(
        key="deletion_watermark",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="deletion_watermark.json",
        why=(
            "R35. It marks how far the deletion pass has read THIS library's "
            "soft-delete markers. New state."
            " COUPLED, named by R30: a deletion watermark that survives a "
            "rollback skips markers the restore put back."
        ),
    ),
    StateFile(
        key="backup_ack",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="backup_ack.json",
        why=(
            "KTD18's queue-time acknowledgment and the backup age shown when it "
            "was given. New state: the source system's backup script persists no "
            "timestamp at all, it stats the remote, so there is nothing to port. "
            "Library-scoped because the thing acknowledged is a backup of THIS "
            "library."
            " NEVER_RESTORED: the backup it acknowledges lives off this volume "
            "and a restore does not un-take it, so rolling the record back would "
            "demand the user re-acknowledge a backup that is still there."
        ),
    ),
    StateFile(
        key="taxonomy_active",
        snapshot=SnapshotRole.COUPLED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative="taxonomy.toml",
        why=(
            "S6. The SHIPPED default template is packaged read-only data in the "
            "wheel; the ACTIVE template is a copy made here at setup. That makes "
            "a library self-describing: a second installation or a reinstall "
            "resolves the same tree without re-answering the wizard, and a "
            "snapshot rolls the taxonomy back with the database it describes."
            " Which is to say COUPLED, explicitly: the tree in the database and "
            "the template that describes it are one decision in two files."
        ),
    ),
    StateFile(
        key="active_run_sentinel",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.FILE,
        relative=".cratekit_active_run.json",
        why=(
            "The one entry the source system already places beside the library, "
            "carried forward as-is rather than converted. It sits at the library "
            "ROOT rather than inside the state directory on purpose: it is an "
            "advisory cross-machine heartbeat, and a second system looking for it "
            "should not have to know this layout."
            " NEVER_RESTORED: it is a live heartbeat. Restoring one would "
            "advertise a run that ended, to a machine that would then wait for it."
        ),
        at_library_root=True,
    ),
    StateFile(
        key="set_workspaces",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
        medium=Medium.DIRECTORY,
        relative="",
        why=(
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
            "because a stage artifact belongs to a run, not to the database."
        ),
    ),
)

_STATE_BY_KEY: Mapping[str, StateFile] = MappingProxyType({s.key: s for s in STATE_FILES})

#: The Cratekit-owned directory inside the user's sets directory. Named here so
#: the entry above and the resolver below cannot disagree about it.
SET_WORKSPACE_DIRNAME = ".cratekit_workspaces"

#: The two entries whose location is COMPOSED from configured values rather than
#: from a fixed relative path, each with the function that composes it.
#:
#: A table rather than a chain of branches inside ``state_path``, because there
#: are now two of them and a branch per row stops being readable at the third.
#: They stay out of ``relative`` because neither is a constant: the database's
#: location is the user's decision made in rekordbox, and the sets directory's
#: name is a config value the user can change.
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

    A library-scoped entry needs a ``Config`` because its root is the configured
    library. Asking for one without a config raises rather than falling back to
    the installation root, since a silent fallback is how the write lock ends up
    per installation again.
    """
    entry = state_file(key)
    if entry.medium is Medium.KEYCHAIN:
        raise ValueError(
            f"{key!r} is stored in the OS keychain and has no path. Read it "
            f"through cratekit.core.secrets, which is the one place that knows "
            f"how to fail when no keychain backend is reachable."
        )
    if entry.root is StateRoot.INSTALLATION:
        # The installation root spans two physical directories with different
        # backup and sync semantics, and the entry says which one it means. It
        # used to be implicit, which is how the config file came to be declared
        # under the state directory while every loader read the config directory.
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
    # One subdirectory per snapshot role, DERIVED from the role the entry already
    # declared. That is what makes the KTD21b coupled set a directory boundary
    # instead of a list U8 and U32 have to keep in sync with this table.
    return library_state_dir(config) / _LIBRARY_SUBDIR_BY_ROLE[entry.snapshot] / entry.relative


def state_files_for(root: StateRoot) -> tuple[StateFile, ...]:
    """Every declared entry under one root, in declaration order."""
    return tuple(s for s in STATE_FILES if s.root is root)


def coupled_state_files() -> tuple[StateFile, ...]:
    """Every entry a KTD21b snapshot must capture and a restore must replace.

    Derived from the schema so U8 and U32 never maintain a second copy of it. A
    hand-mirrored list is the drift this repository already refuses for its CI
    dependency list and its extras table, and here the cost of that drift is the
    plan's top-ranked risk: the registry rolling back while the database does not.
    """
    return tuple(s for s in STATE_FILES if s.snapshot is SnapshotRole.COUPLED)


def sidecar_paths(key: str, config: Config, *, restored_only: bool = False) -> tuple[Path, ...]:
    """The sidecar paths that travel with one entry. Composed, never listed.

    ``restored_only`` is the difference between the two consumers. A CAPTURE
    wants every sidecar, because the log holds transactions the database file
    does not. A RESTORE wants only the ones it writes back, because the
    shared-memory index is derived from the log and a stale one put back beside
    a fresh log describes a database that no longer exists. Both answers come
    from the same declaration, so they cannot disagree.

    These are paths, not files: any of them may be absent, which is normal (see
    ``StateFile.sidecars``). Resolving a path never touches the disk (Rule 1).
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

    Few entries, not many, and that is the point of the layout. Everything
    coupled except the database lives inside one directory, so capture is a
    directory copy and restore is a directory replace. The database is the one
    exception because its location is the user's decision, which is exactly why
    ``validate`` constrains it: on one filesystem these two rename atomically, on
    two they do not.

    THE SIDECARS ARE PART OF THE ANSWER, NOT A DETAIL FOR THE CALLER. An entry
    declares one path, and for a SQLite database that path is not the whole file
    set: the write-ahead log beside it holds committed transactions the database
    file does not yet contain. A consumer that copied exactly the paths this
    function used to return would produce a database silently missing them. They
    are expanded from ``StateFile.sidecars`` rather than appended by U8, because
    a companion list in the capture unit is the hand-maintained set this schema
    exists to abolish.

    Some of the returned paths will not exist, and that is expected rather than
    exceptional: see ``StateFile.sidecars`` for when a database legitimately has
    no log beside it. Copy what is there.
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

    A record keyed by a display name is orphaned the instant the user renames
    the thing it describes, and the orphan is invisible: the code simply finds no
    entry and starts over. ``resolve_identifier`` maps an old display-name key to
    the stable identifier, returning None when it no longer resolves.

    Returns the re-keyed records and the keys that did not resolve. Unresolved
    keys are RETURNED rather than dropped, because a record that cannot be
    re-keyed is exactly the orphan the rule exists to surface, and dropping it
    silently would make the migration look clean.
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


# ---------------------------------------------------------------------------
# The typed schema
#
# Frozen dataclasses, not a dict. Every access is attribute access, so a typo is
# an AttributeError at the call site rather than a None that travels three
# functions before it fails as something else.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PrefixMapping:
    """One entry of the ordered location prefix map (S1).

    The TOML keys are ``from`` and ``to``. ``from`` is a Python keyword, so the
    fields carry a suffix and the serializer maps them back. That mapping is
    declared once, in ``_PREFIX_TOML_KEYS``, rather than spelled at each end.

    On disk this is an ordered array of tables. The writer emits it as an inline
    array of inline tables rather than repeated ``[[library.location_prefix_map]]``
    headers, which is the same TOML value by every parser and only differs in how
    it reads by hand. What matters, and what is asserted, is that ORDER survives:
    one prefix can be another's prefix, first match wins, and an unordered map
    resolves those two differently on different runs.
    """

    from_prefix: str
    to_prefix: str


_PREFIX_TOML_KEYS = (("from", "from_prefix"), ("to", "to_prefix"))

#: The one interpolation token a prefix mapping's ``to`` may contain. Keeping the
#: map interpolated rather than absolute is what lets it survive the user
#: remounting the library somewhere else without a rewrite.
LIBRARY_ROOT_TOKEN = "{library.root}"


@dataclass(frozen=True, slots=True)
class LibraryConfig:
    """Where the library is, what proves it is the right one, and how it is laid out."""

    root: Path
    #: R38. The recorded identity of the volume, asserted before any destructive
    #: operation. A UUID or serial, NEVER a mount path: a mount path is exactly
    #: what R38 says not to identify a volume by, because two different drives
    #: mount at the same path on different days.
    volume_id: str
    #: The rekordbox database. Declared in ``STATE_FILES`` as ``rekordbox_db``,
    #: library-scoped and COUPLED, and CONSTRAINED: it is expected under ``root``.
    db_path: Path
    #: The date the user accepted that their database sits outside the library
    #: root. Unset means the containment rule applies and a database elsewhere
    #: refuses at load.
    #:
    #: WHY THE RULE EXISTS, AND WHY IT IS NOT AN OUTRIGHT REFUSAL. KTD21b requires
    #: the database and its coupled state to be captured in ONE atomic commit, and
    #: the only atomic commit available is a rename, which is atomic only within
    #: one filesystem. A friend who leaves rekordbox at its default location puts
    #: the database in their home directory while the coupled state sits on the
    #: music volume, and the plan's stated premise for the decision, "the coupled
    #: state is a handful of small files beside the database", is then false for
    #: that install. Refusing outright would lock out the platform default, so the
    #: non-contained case stays supported and becomes a recorded decision with its
    #: consequence attached. What is not acceptable is the silent default: the
    #: failure has to be visible at setup, while the user can still move the
    #: database, rather than at the first snapshot, when they cannot.
    db_outside_root_acknowledged_on: str | None = None
    music_dir: str = "Music"
    processed_dir: str = "Processed_Tracks"
    sets_dir: str = "Set_Recordings"
    #: The library-scoped state root's directory name, relative to ``root``.
    state_dirname: str = ".cratekit"
    #: Ordered; FIRST MATCH WINS. Order is load-bearing because one prefix can be
    #: another's prefix, and an unordered map resolves those two differently on
    #: different runs. Populated at setup from what the database actually
    #: contains, never from a constant.
    location_prefix_map: tuple[PrefixMapping, ...] = ()


@dataclass(frozen=True, slots=True)
class PathsConfig:
    """Paths that are not inside the library."""

    #: Where fresh downloads land before they are moved into the library. It must
    #: round-trip into the acquisition adapter's own setting (KTD20), which is why
    #: it is one configured value rather than two that can disagree.
    download_staging: Path


@dataclass(frozen=True, slots=True)
class ProfileConfig:
    """Which named preset of module membership is in force."""

    name: str


@dataclass(frozen=True, slots=True)
class ModulesConfig:
    """Per-module toggles the user set EXPLICITLY.

    Only what the file actually contains. Absence matters: a module the file does
    not mention takes the profile's answer, and a module the file does mention
    overrides it (D6). If this stored a fully defaulted mapping there would be no
    way left to tell "the user chose off" from "the profile says off", and the
    precedence rule would become unexpressible.
    """

    explicit: Mapping[str, bool] = field(default_factory=lambda: MappingProxyType({}))


@dataclass(frozen=True, slots=True)
class TaxonomyConfig:
    """The taxonomy SELECTION only (S6).

    The active template itself is library-scoped state. Config records which
    template was chosen at setup, so a re-run of setup can seed the same one.
    """

    template: str = "default"


@dataclass(frozen=True, slots=True)
class NamingConfig:
    """Naming POLICY values (S3).

    U2 owns these values; the naming engine owns the mechanism and takes them as
    parameters. The engine must not read config: a function that reaches for
    global configuration cannot be exercised against two taxonomies in one
    process, and proving a second template works needs exactly that.
    """

    lossy_marker: str = "[MP3]"
    #: Both budgets are UTF-8 BYTES, not characters. The margin below the
    #: filesystem's own ceiling is deliberate: a later zero-padding pass grows the
    #: key field, and measuring against the padded form pre-reserves that growth.
    path_budget_bytes: int = 250
    filename_max_bytes: int = 255


@dataclass(frozen=True, slots=True)
class AcquisitionConfig:
    """What acquires, at what quality, under which lossless policy."""

    adapter: str = "tidal_dl_ng"
    quality: str = "lossless"
    #: None means "the adapter's own default". The adapter owns pacing (KTD20).
    pacing_delay_s: float | None = None
    #: R21 and S3. Two values only. There is deliberately no third value in which
    #: a lossy file goes UNMARKED: marking is mandatory wherever lossy is
    #: permitted at all, so a "lossy allowed, marking off" combination cannot be
    #: expressed, which is stronger than validating it away.
    lossless_policy: str = "strict"


@dataclass(frozen=True, slots=True)
class AnalysisConfig:
    """Analysis sizing and calibration selection."""

    #: None means "probe" (KTD10): worker count comes from a probe worker's
    #: resident size against available memory, never from a CPU count.
    jobs: int | None = None
    energy_calibration: str = "auto"


@dataclass(frozen=True, slots=True)
class RekordboxConfig:
    """The version pins the guarded writer refuses on.

    ``pinned_app_version`` is None by default and None REFUSES (S2). It is never
    auto-recorded from whatever is installed: a pin the software copies from the
    running install is a tautology that refuses nothing, forever, which is the
    entire property the pin exists to provide. Setup may READ the installed
    version and PROPOSE it; recording it takes an explicit decision from the user.
    """

    pinned_pyrekordbox: str = "0.4.4"
    pinned_db_version: str = "6000"
    pinned_app_version: str | None = None
    #: The date the user confirmed this pin against a real write. Without it, a
    #: pin is a number somebody typed; with it, a stale pin is visible as stale.
    validated_on: str | None = None
    app_path: Path | None = None


@dataclass(frozen=True, slots=True)
class BackupConfig:
    """Remote backup destinations. All None by default, all wizard-supplied.

    Every one of these is a hardcoded literal in the source system's backup
    script, naming one person's remote and one person's bucket names.
    """

    remote: str | None = None
    dest: str | None = None
    archive_root: str | None = None
    db_dest_root: str | None = None


@dataclass(frozen=True, slots=True)
class Config:
    """The whole validated configuration, frozen.

    Frozen matters beyond hygiene. KTD9 says a job runs against the configuration
    frozen when it was QUEUED and reports drift rather than silently choosing a
    version. A mutable config makes "the configuration it was queued against"
    unanswerable, because the object the job holds could have been edited by
    whatever queued it.
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

    # -- derived views -----------------------------------------------------

    def enabled_modules(self) -> frozenset[str]:
        """Effective module membership: the profile's preset, then explicit overrides."""
        return profiles.resolve(self.profile.name, self.modules.explicit).modules

    def available_capabilities(self) -> frozenset[str]:
        """Everything the install can do, including what no profile may switch off."""
        return profiles.resolve(self.profile.name, self.modules.explicit).available

    def resolved_prefix_map(self) -> tuple[tuple[str, str], ...]:
        """The prefix map with ``{library.root}`` interpolated, in declared order.

        Returned as plain pairs because the consumer is a resolver that walks
        them in order and takes the first match. Order is preserved end to end;
        nothing here sorts or dedupes.
        """
        root = str(self.library.root)
        return tuple(
            (m.from_prefix, m.to_prefix.replace(LIBRARY_ROOT_TOKEN, root))
            for m in self.library.location_prefix_map
        )

    # -- serialization and identity ---------------------------------------

    def to_toml_dict(self) -> dict:
        """A TOML-safe, deterministically ordered plain dict.

        Deterministic is a hard requirement, not a nicety: ``fingerprint`` hashes
        exactly these bytes, and a fingerprint that depends on dict ordering
        would report drift on a config nobody edited.

        None values are OMITTED. TOML has no null, so an omitted key and a null
        key are the same state, and writing one requires inventing a sentinel
        that would then have to be un-invented on read.
        """
        return _to_toml_value(self)

    def to_toml_bytes(self) -> bytes:
        """The exact bytes ``save`` writes and ``fingerprint`` hashes."""
        return tomli_w.dumps(self.to_toml_dict()).encode("utf-8")

    def fingerprint(self) -> str:
        """A stable identity for this configuration (KTD9).

        The job engine records this at queue time alongside the specific values a
        job needs, and compares at run time. Equal fingerprint means nothing
        drifted; different means something did, and the job reports which rather
        than silently picking a version.
        """
        return hashlib.sha256(self.to_toml_bytes()).hexdigest()

    def db_is_inside_library_root(self) -> bool:
        """True when the database and its coupled state share a filesystem (KTD21b).

        A FACT, with no prose and no verb attached, because the two callers want
        different things from it: validation refuses on it at load, and doctor
        reports it on every run so a user who acknowledged the consequence months
        ago is reminded that their snapshots are copies rather than atomic
        commits.
        """
        return _is_inside(self.library.db_path, self.library.root)

    # -- preconditions -----------------------------------------------------

    def assert_rekordbox_pin_recorded(self) -> None:
        """Refuse when the application pin has never been explicitly recorded (S2).

        Called by the guarded writer before it opens the database. Unset is a
        refusal to WRITE, not a refusal to load: doctor, help, and every read-only
        verb must still run on a config whose pin was never set, or a user could
        not reach the setup step that sets it.
        """
        if not self.rekordbox.pinned_app_version:
            # The message STATES what is wrong; the remedy token says what to do
            # about it, and the CLI renders that token (D2). The two are separate
            # because a caller choosing between "record this pin" and "fix these
            # values" by string-matching a sentence is the KTD25 failure again.
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


# ---------------------------------------------------------------------------
# Validation
#
# Collects EVERY problem before raising. The plan's first test scenario for this
# unit is that a config missing required keys names each missing key.
# ---------------------------------------------------------------------------

#: Dotted paths that have no default and must appear in the file. Six of them,
#: deliberately: a short required list is a short first-run wizard, and every
#: other key is a decision the product can make on the user's behalf.
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
    """An override path from the environment, or None.

    Returns None for an unset variable so the caller can tell "relocate this"
    from "leave it alone". Never used to SUPPLY a value that the file omitted;
    see the note on the ENV_ constants above.
    """
    value = os.environ.get(variable)
    return Path(value) if value else None


def _apply_env_overrides(data: Mapping) -> dict:
    """Return a copy of ``data`` with the relocation overrides applied.

    THE ONE PLACE THE ENVIRONMENT ENTERS. Everything downstream, validation and
    construction alike, reads the mapping this returns, so there is no longer a
    "raw" answer and an "effective" answer for any rule to disagree about. The
    defect this closes is recorded on the ENV_ constants: the containment rule
    was decided against the file's root while every runtime consumer read the
    overridden one.

    Two properties, and both are load-bearing:

    RELOCATE, NEVER SUPPLY. A key the file does not carry stays absent, so a
    machine with no setup at all cannot resolve a library root out of the
    environment and start writing to it (R38). Validation then reports the key
    as missing, which is the correct outcome.

    A RELOCATED ROOT CARRIES ITS DATABASE. What the file records is where the
    database sits RELATIVE to the library, so a db_path that was under the old
    root is re-based onto the new one. Leaving it behind would aim it into a
    tree that is no longer the library, and would make a relocation violate the
    containment rule for no reason the user could act on. A db_path that was
    NOT under the old root is left exactly where it is: it was never expressed
    relative to the library, so it still needs its own acknowledgment.

    Idempotent, which matters because ``from_dict`` applies it and then calls
    ``validate``, which applies it again: re-basing a path already under the
    effective root maps it onto itself.
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
                and _is_inside(Path(db_path), Path(configured_root))
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
    """Return EVERY problem with the EFFECTIVE configuration, as readable lines.

    Side-effect free and list-returning rather than raising, so the setup wizard
    can show a user all of their remaining work at once and the loader can raise
    with the same content. One implementation, two consumers, no drift.

    NOT A FUNCTION OF ``data`` ALONE, DELIBERATELY. The environment overrides are
    applied here first, so every rule below is decided against the values the
    running process will actually use. Validating the raw file mapping instead is
    what let a config violate the containment rule at runtime and still validate
    clean: the rule was checked against a root that nothing downstream read.
    Callers do not have to remember to pre-apply anything, because there is no
    way to reach these rules without going through this line.
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
        # R38 identifies a volume by RECORDED IDENTITY, not by mount path. A
        # value shaped like a path means somebody recorded where the drive
        # happened to be mounted, which is the failure the requirement names:
        # the next drive to mount there would pass the assertion.
        if volume_id.startswith(("/", "\\")) or ":\\" in volume_id:
            problems.append(
                f"{VOLUME_IDENTITY_KEY} looks like a mount path ({volume_id!r}). "
                f"Record the volume's own identity, a UUID or serial, so a "
                f"different drive mounted at the same path fails the assertion "
                f"instead of passing it (R38)."
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

    problems += _validate_db_containment(data)
    problems += _validate_prefix_map(_dig(data, "library.location_prefix_map"))

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

    return problems


def _is_inside(child: Path, parent: Path) -> bool:
    """True when ``child`` is ``parent`` or sits under it. PURELY TEXTUAL.

    No ``resolve()`` and no ``exists()``: Rule 1 forbids this module from touching
    the filesystem, and validation runs before anything is mounted. ``normpath``
    collapses ``..`` so a path cannot escape by spelling, which is the only
    evasion that matters for a value the user typed.
    """
    child_parts = Path(os.path.normpath(str(child))).parts
    parent_parts = Path(os.path.normpath(str(parent))).parts
    return child_parts[: len(parent_parts)] == parent_parts


#: The shape ``library.db_outside_root_acknowledged_on`` must take. Anchored at
#: both ends: a substring match would accept a date buried in a sentence.
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ACKNOWLEDGMENT_KEY = "library.db_outside_root_acknowledged_on"


def _validate_acknowledgment_date(value: object) -> list[str]:
    """Shape-check the containment acknowledgment. It is a DATE, never a flag.

    Accepting any non-empty string made ``no``, ``true``, and ``2026-13-99`` all
    switch the containment refusal off, and two of those read to a human as the
    opposite of what they did. Its sibling in this same validator,
    ``library.volume_id``, is shape-checked for exactly this reason: a value that
    is merely truthy passes a truthiness test while meaning nothing.

    A real calendar date, not just a date-shaped string, because the point of
    recording WHEN the consequence was accepted is that something can later
    compare it to today. ``fromisoformat`` alone would accept the compact
    ``20260801`` form, so the pattern runs first and pins the layout.
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

    See ``LibraryConfig.db_outside_root_acknowledged_on`` for why the rule exists
    and why it is a recorded acknowledgment rather than a flat refusal.

    Decided against the EFFECTIVE root: ``validate`` applies the environment
    overrides before this runs, so the root judged here is the root every runtime
    consumer reads. It used to be the file's raw value, which meant the rule was
    decided against one root and enforced against another.
    """
    root = _dig(data, "library.root")
    db_path = _dig(data, "library.db_path")
    acknowledged = _dig(data, "library.db_outside_root_acknowledged_on")

    problems: list[str] = []
    accepted = False
    if acknowledged is not None:
        # Shape-checked whether or not the database is actually outside the root,
        # because a malformed date is a defect in the file either way, and the
        # user should learn about it while they are still looking at the file.
        shape_problems = _validate_acknowledgment_date(acknowledged)
        problems += shape_problems
        accepted = not shape_problems

    if not isinstance(root, str) or not isinstance(db_path, str):
        return problems  # a missing required key is already reported by the caller
    if not root.strip() or not db_path.strip():
        return problems
    if _is_inside(Path(db_path), Path(root)):
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


# ---------------------------------------------------------------------------
# dict -> typed, typed -> dict
# ---------------------------------------------------------------------------


def from_dict(data: Mapping, *, path: Path | None = None) -> Config:
    """Build a validated, frozen ``Config``, or raise ``ConfigInvalid`` with all problems.

    Optional keys are merged OVER freshly constructed defaults, so a missing or
    unknown optional key degrades instead of crashing. Required keys do the
    opposite and fail loudly. Those two policies are written as two separate code
    paths on purpose: in the source system they were one function, and the
    tolerant half quietly swallowed the intolerant half's failures.

    The environment overrides are applied ONCE, up front, and everything below
    reads the result. Applying them here rather than field by field inside
    ``_build`` is what makes the values this returns the same values ``validate``
    just judged; the two used to disagree about the library root.
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
        acquisition=_build(AcquisitionConfig, data.get("acquisition") or {}),
        analysis=_build(AnalysisConfig, data.get("analysis") or {}),
        rekordbox=_build(RekordboxConfig, data.get("rekordbox") or {}),
        backup=_build(BackupConfig, data.get("backup") or {}),
    )


def _build(cls, raw: Mapping, *, overrides: Mapping[str, object] | None = None):
    """Construct one schema dataclass from a raw mapping.

    Unknown keys are ignored rather than rejected. That is deliberate for a
    FORWARD-only migration model: a file written by a newer build is refused
    outright by version, so an unknown key here can only come from a hand edit,
    and crashing on a stray key would lock a user out of their own config over a
    typo they can still see.
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
            # An all-default section serializes to an empty table, and an empty
            # table means exactly what its absence means. Emitting one would make
            # two configurations with identical meaning produce different bytes,
            # and therefore different fingerprints, which is the one thing the
            # fingerprint must never do (KTD9).
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

    ``PrefixMapping`` uses ``from`` and ``to`` on disk, because those read as
    English in a file a user edits by hand, and ``from`` cannot be a Python
    field name.

    ``ModulesConfig`` FLATTENS: the file has ``[modules]`` with one key per
    module, not ``[modules.explicit]``. The wrapper exists in code so that
    "explicitly set" stays distinguishable from "defaulted" (see the class), and
    that distinction is a code concern the user should never have to type.
    """
    if isinstance(source, PrefixMapping):
        return {toml_key: out[field_name] for toml_key, field_name in _PREFIX_TOML_KEYS}
    if isinstance(source, ModulesConfig):
        return out.get("explicit", {})
    return out


# ---------------------------------------------------------------------------
# Forward-only migrations
#
# Applied IN MEMORY over a deep copy, validated in full, and only then written.
# ---------------------------------------------------------------------------

#: Every migration is ``dict -> dict``. No I/O, no Path, no network. That is what
#: makes each one a two-line unit test, and it is also what makes the "a failed
#: migration leaves the original untouched" property true BY CONSTRUCTION rather
#: than by a cleanup path that can itself fail.
Migration = Callable[[dict], dict]

#: Keyed by the version the step upgrades FROM. Empty at schema 1 because there
#: is nothing before schema 1. Inventing historical versions to exercise the
#: machinery would make the version number a lie, so the machinery is exercised
#: with a ladder supplied by the test instead, and the shipped table is checked
#: for gaps by ``test_config_migration.py``.
MIGRATIONS: Mapping[int, Migration] = MappingProxyType({})


def migrate(
    data: Mapping,
    *,
    current: int = CURRENT_SCHEMA_VERSION,
    migrations: Mapping[int, Migration] = MIGRATIONS,
) -> dict:
    """Upgrade a raw config dict to ``current``. Pure, forward-only.

    Steps run in ascending version order over a deep copy of the input, so a step
    that raises halfway leaves the caller's data untouched and leaves nothing at
    all on disk. The plan phrases this as "applied to a temporary file that
    replaces the original only after all steps succeed"; in memory is strictly
    stronger, because a temp file still has to be cleaned up when step two of
    three raises, and the cleanup is one more thing that can fail.
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


# ---------------------------------------------------------------------------
# Reading and writing
# ---------------------------------------------------------------------------


def _read_raw(path: Path) -> dict:
    """Parse the file as TOML, or raise ``ConfigCorrupt`` naming the file and line."""
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        # No instruction in the message: the remedy is the RUN_SETUP token on the
        # class, and only the CLI knows what running setup looks like from
        # wherever the user is (D2).
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

    Order is the whole design:

    1. parse, 2. migrate in memory over a deep copy, 3. validate the FULLY
    migrated data, 4. back up the original, 5. atomically replace it.

    No byte reaches the disk before step 3 passes. So a migration that raises at
    step two of three leaves the original file byte-identical and leaves no
    orphan behind, because there was never a partial artifact to orphan.

    THE DECISION IS MADE TWICE, AND THE SECOND TIME IS UNDER THE LOCK. The first
    pass answers the caller: parse, migrate, validate, return a Config even when
    nothing is written. The write then re-reads the file with the lock held and
    re-decides from what is actually there. Deciding once, outside the lock, is
    the shape that lets two processes reach an unmigrated config in the same
    second, both decide to migrate, and the second one copy ALREADY-MIGRATED bytes
    into a backup named for the version it came from. A file called
    ``config.toml.v1.bak`` holding version 3 is the half-safe outcome the lock's
    own docstring says it exists to prevent.
    """
    raw = _read_raw(path)
    found = raw.get("schema_version")
    migrated = migrate(raw, current=current, migrations=migrations)
    config = from_dict(migrated, path=path)

    if not write_back or found == current:
        return config

    with _exclusive_lock(path.with_name(path.name + ".migrate.lock")):
        # Re-read and re-decide. Everything above ran without the lock, so the
        # file may have been migrated by another process while this one waited.
        current_raw = _read_raw(path)
        found_now = current_raw.get("schema_version")
        if found_now == current:
            # Another process did the work, including its own backup. Rebuild from
            # what is on disk rather than returning the value derived from the
            # bytes that are no longer there.
            return from_dict(current_raw, path=path)

        migrated = migrate(current_raw, current=current, migrations=migrations)
        config = from_dict(migrated, path=path)
        # The backup holds the bytes this call is about to replace, re-read under
        # the lock, so it can no longer hold a version other than the one its name
        # claims. Overwriting an older backup of the same version is correct for
        # the same reason: what a user needs back is what was just replaced.
        backup = path.with_name(f"{path.name}.v{found_now}.bak")
        atomic_write_bytes(path.read_bytes(), backup)
        atomic_write_bytes(tomli_w.dumps(migrated).encode("utf-8"), path)
    return config


_MEMO: dict[tuple, Config] = {}


def load(path: Path | None = None) -> Config:
    """The ordinary entry point: the validated config, memoized on file identity.

    Memoized on ``(path, inode, mtime, size)``. The inode is in the key because
    every write here goes through an atomic replace, which mints a NEW inode, so
    a rewritten file can never be served from the cache even on a filesystem
    whose timestamp resolution is coarse.

    Memoization is what makes it safe for callers to call ``load()`` wherever they
    need a value instead of binding one at their own import time. Removing the
    reason to snapshot is the only thing that actually stops the snapshotting.
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

    IT REFUSES TO WRITE A FILE THIS MODULE WOULD REFUSE TO LOAD. That is not
    belt-and-braces; it is the property that stops a save from locking a user out
    of their own configuration. The concrete case it was added for: an
    environment override relocated the library root, ``save`` serialized the
    relocated root beside a db_path the override had not touched, and the
    resulting file failed the containment rule at the next load. The user had
    never edited it and had no way to know what to change.

    That specific inconsistency is now impossible upstream, because a relocated
    root carries its database with it (see ``_apply_env_overrides``). The check
    stays because the CLASS of failure is not specific to those two fields: any
    future pair of values that a validation rule relates can drift apart in
    memory, and a write is the moment that turns a runtime inconsistency into a
    permanent one. Validating the exact bytes about to be written closes all of
    them at once, and costs one pure function call on a path that runs at setup.

    DIRECTORY CREATION. This is one of three places in the module that creates a
    directory (the others are ``atomic_write_bytes`` and ``_exclusive_lock``),
    and all three go through ``_mkdir_private`` so no state directory's
    permissions depend on the user's umask. Each creates immediately before a
    write, never at import (Rule 1).
    """
    target = config_path() if path is None else path
    problems = validate(config.to_toml_dict())
    if problems:
        raise ConfigInvalid(problems, path=target)
    _mkdir_private(target.parent)
    atomic_write_bytes(config.to_toml_bytes(), target)
    reset_cache()
    return target


#: The mode every state file this package writes lands at, on every machine.
PRIVATE_FILE_MODE = 0o600

#: The mode every directory this package CREATES lands at, on every machine.
#:
#: A 0600 file inside a 0777 directory is not a private file. Directory write
#: permission is what governs unlink and rename, so any local account can delete
#: the file and put its own in place, whatever the file's own mode says. The
#: credential presence index is the sharp case: it carries no credential values,
#: but replacing it lets any local account decide what doctor reports about which
#: credentials are set.
PRIVATE_DIR_MODE = 0o700

#: True when this platform has POSIX modes at all. Probed once, so every
#: mode-setting call site degrades the same way instead of each guessing.
_CAN_SET_MODE = hasattr(os, "chmod")


def _mkdir_private(path: Path) -> None:
    """Create ``path`` and any missing parent, owner-only, on any umask.

    NOT ``Path.mkdir(mode=...)``, and the difference is the whole reason this
    function exists. ``mkdir`` applies the process umask to the mode it is given,
    and with ``parents=True`` it creates the intermediate levels at the DEFAULT
    0o777 rather than at the mode the caller asked for. Under a permissive umask
    that leaves a world-writable directory one level above a 0600 file, which
    negates the file's mode entirely: the observed result was a 0o777 config
    directory and a 0o777 installation state directory holding correctly-moded
    0600 files.

    So each missing level is created and then chmodded explicitly. Only levels
    this call actually created are touched: a directory that already existed
    belongs to the user, and tightening their home directory because a state root
    happened to be under it would be a far worse bug than the one being fixed.

    Guarded on ``_CAN_SET_MODE`` so a platform with no POSIX modes degrades to an
    ordinary mkdir rather than crashing (R1, KTD6).
    """
    if path.is_dir():
        return
    for level in [*reversed(path.parents), path]:
        if level.is_dir():
            continue
        try:
            level.mkdir()
        except FileExistsError:
            # Another process won the race. Not ours to create, so not ours to
            # re-mode either.
            continue
        if _CAN_SET_MODE:
            os.chmod(level, PRIVATE_DIR_MODE)


def atomic_write_bytes(payload: bytes, path: Path, *, mode: int = PRIVATE_FILE_MODE) -> None:
    """Write ``payload`` to ``path`` atomically at an EXPLICIT mode, or not at all.

    Two properties, and both were learned from a defect.

    ATOMIC. The temp file is created in the TARGET's directory so ``os.replace``
    is a same-filesystem rename and therefore atomic; a temp file in the system
    temp directory would make it a copy, which can be interrupted halfway. The
    fsync before the replace is the source system's one omission: without it a
    crash can leave a correctly named file whose contents never reached the
    platter.

    0600 REGARDLESS OF UMASK. ``mkstemp`` already creates at 0600, so the mode was
    previously an undocumented side effect that nothing would have caught if the
    writer changed. The explicit chmod makes it a stated property, and it is the
    reason this function is the shared writer for every state file rather than one
    of two: the sibling that wrote the credential presence index with
    ``write_text`` inherited the user's umask and landed 0666 under umask 000,
    which is the exact defect class ``secrets.py`` was chartered to end. That file
    carries no credential VALUES, but world-writable means any local account can
    forge or erase the answer doctor gives about which credentials are set.

    THE DIRECTORY MODE IS PART OF THE FILE MODE. A 0600 file inside a
    world-writable directory is not private: unlink and rename are governed by
    the DIRECTORY's permissions, so anyone who can write the directory can
    replace the file whatever its own mode says. The mkdir here therefore goes
    through ``_mkdir_private`` rather than through ``Path.mkdir``, which would
    take its mode from the umask (see that function for why the obvious
    ``mode=`` argument does not fix it).
    """
    _mkdir_private(path.parent)
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



class _exclusive_lock:
    """An exclusive advisory lock that REFUSES rather than proceeding unlocked.

    The source system's equivalent tolerates a failed ``flock`` and carries on,
    which is defensible for an advisory ledger and wrong here. Two ``crate``
    subprocesses (KTD26) can reach an unmigrated config in the same second, and
    two concurrent migrations of one file is how it ends up half-upgraded.

    THE LOCK FILE PERSISTS AFTER A SUCCESSFUL MIGRATION, DELIBERATELY. Unlinking
    a lock file on release is the classic way to lose the exclusion it provides:
    process A holds the lock on inode X and unlinks the NAME, process B creates a
    fresh file at that name and takes the lock on inode Y, and both then believe
    they hold the only lock with nothing raised. That failure is silent and
    survives review, which is exactly the failure the lock exists to prevent, so
    the file stays. The source system's own write-session lock is never unlinked
    for the same reason.

    What made a persistent lock file a real exposure was its MODE, not its
    lifetime. Opened through the builtin ``open(path, "w")`` it landed 0666 under
    a permissive umask, in a directory that was itself 0777, so any local account
    could hold it, making every future migration refuse, or truncate it out from
    under the process holding it. It is created 0600 now, inside a 0700
    directory, which makes persisting cost one empty file and nothing else.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.handle = None

    def __enter__(self):
        _mkdir_private(self.path.parent)
        try:
            import fcntl

            # os.open with an explicit mode rather than the builtin open(): the
            # builtin creates at 0666 masked by the umask, so a permissive umask
            # yields a world-writable lock. The mode here is masked too, but 0600
            # carries no group or other bits for a mask to add, so masking can
            # only ever leave it at or below 0600.
            fd = os.open(self.path, os.O_CREAT | os.O_RDWR, PRIVATE_FILE_MODE)
            self.handle = os.fdopen(fd, "r+b")
            if _CAN_SET_MODE:
                # O_CREAT sets the mode only when it CREATES the file. A lock
                # left behind by a build from before this fix is already there,
                # already 0666, and would keep that mode forever without this.
                os.chmod(self.path, PRIVATE_FILE_MODE)
            fcntl.flock(self.handle, fcntl.LOCK_EX)
        except (ImportError, OSError) as exc:
            if self.handle is not None:
                self.handle.close()
                self.handle = None
            raise ConfigLockUnavailable(
                f"could not take an exclusive lock on {self.path} ({exc}). A "
                f"config migration refuses rather than running unsynchronized, "
                f"because two processes migrating one file leaves it "
                f"half-upgraded."
            ) from exc
        return self

    def __exit__(self, *exc_info) -> None:
        if self.handle is not None:
            self.handle.close()
            self.handle = None


__all__ = [
    "ACKNOWLEDGMENT_KEY",
    "CONFIG_FILENAME",
    "CURRENT_SCHEMA_VERSION",
    "LIBRARY_ROOT_TOKEN",
    "LIBRARY_STATE_LAYOUT_VERSION",
    "MIGRATIONS",
    "PRIVATE_DIR_MODE",
    "PRIVATE_FILE_MODE",
    "REQUIRED_KEYS",
    "SET_WORKSPACE_DIRNAME",
    "SQLITE_SIDECARS",
    "STATE_FILES",
    "VOLUME_IDENTITY_KEY",
    "AcquisitionConfig",
    "AnalysisConfig",
    "BackupConfig",
    "Config",
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
    "Remedy",
    "Sidecar",
    "SnapshotRole",
    "StateFile",
    "StateRoot",
    "TaxonomyConfig",
    "atomic_write_bytes",
    "config_dir",
    "config_path",
    "coupled_state_files",
    "from_dict",
    "installation_state_dir",
    "library_coupled_dir",
    "library_history_dir",
    "library_local_dir",
    "library_state_dir",
    "load",
    "load_from_path",
    "migrate",
    "rekey_records",
    "reset_cache",
    "save",
    "sidecar_paths",
    "snapshot_sources",
    "state_file",
    "state_files_for",
    "state_path",
    "validate",
]
