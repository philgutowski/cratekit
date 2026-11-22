"""The state file inventory (KTD21, KTD21b): every entry, its root, what a
restore does to it and why, and the resolvers over it.

Split from :mod:`cratekit.core.config` (U299), which re-exports every name
here. Every entry is assigned to exactly one root, and every library entry
says whether a restore replaces it, survives it or never touches it.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

import platformdirs

from cratekit.core.config_base import (
    _APP_NAME,
    CONFIG_FILENAME,
    ENV_PROVIDER_GATE_DIR,
    config_dir,
    installation_state_dir,
)

if TYPE_CHECKING:
    from cratekit.core.config_schema import Config


def config_path() -> Path:
    """The path of the config file itself. Does not check that it exists.

    Resolved through ``state_path`` so the inventory and every loader and saver
    agree on one directory.
    """
    return state_path("config")


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
    # Installation-scoped, all NEVER_RESTORED.
    _installation(
        "config", CONFIG_FILENAME,
        "Records this machine's choices (mount path, adapter, modules); two machines legitimately "
        "answer those differently for one library, so a shared config forces one mount path onto "
        "the other.",
        # Off macOS the config directory differs from the state directory.
        area=InstallationArea.CONFIG,
    ),
    _installation(
        "credentials", "",
        "A credential is an account fact, not a library fact. In the keychain because the old "
        "plaintext env file took its 0600 from the umask, and no library should carry a secret "
        "another user of it can read.",
        medium=Medium.KEYCHAIN,
    ),
    _installation(
        "provider_session", "",
        "The provider session as ONE keychain blob under one key, so the token, its refresh token "
        "and the session fields cannot be updated apart into a half-refreshed session that fails "
        "like an outage.",
        medium=Medium.KEYCHAIN,
    ),
    _installation(
        "provider_folder_cache", "provider_folder_cache.json",
        "Remote folder identifiers keyed by year. They describe the remote ACCOUNT, not the "
        "library, and a second install that loses them re-derives them for one API call.",
    ),
    _installation(
        "identify_usage", "identify_usage.json",
        "The identification service's monthly call counter, bound to the CREDENTIAL's quota: two "
        "libraries on one account share one quota, so only a counter beside the credential tells "
        "the truth.",
    ),
    _installation(
        "identify_usage_lock", "identify_usage.lock",
        "Serializes the counter's read-modify-write, under the same root by necessity: a lock "
        "under another root than its file is one two processes can each hold while both edit it.",
    ),
    _installation(
        "provider_gate", "provider_gate.json",
        "The streaming provider's pacing state (R-705, U278): calls, rate limit answers, breaker "
        "and per identity counts. An ACCOUNT fact, resolved under provider_gate_dir and never a "
        "redirected state directory, so a copy run spends the live allowance.",
    ),
    _installation(
        "provider_gate_lock", "provider_gate.lock",
        "The one call at a time lock over the streaming provider, held for each whole call so two "
        "drivers never have a request in flight together; beside its file for the counter lock's "
        "reason.",
    ),
    _installation(
        "night_budget", "night_budget.json",
        "What the night pass has spent of its budget (U293), written before its first call so a "
        "run that died is still charged. An ACCOUNT fact, so it sits beside the gate under "
        "provider_gate_dir.",
    ),
    _installation(
        "night_status", "night_status.json",
        "The last night pass's status line and what it stopped on (U293), shown by doctor and "
        "sync night --last. It describes this installation's last unattended run; losing it loses "
        "only the line.",
    ),
    _installation(
        "schedule_log", "schedule/sync-night.log",
        "Where launchd appends the scheduled night pass's output (U295), the one place a night "
        "that never reached its own record says why. Installation state; losing it loses only "
        "output.",
    ),
    _installation(
        "staging_lock", "staging.lock",
        "One pass stages at a time (U293, U295): land, label sync --go, sync night and schedule "
        "install or remove hold it, so no two share a staging folder or end a night pass. The "
        "kernel frees it when its holder dies.",
    ),
    _installation(
        "isrc_cache", "isrc_cache.json",
        "The provider's answer per ISRC and country (U206), a CATALOGUE fact, so it sits beside "
        "the pacing state and a copy run shares it. Losing it costs calls and no data.",
    ),
    _installation(
        "isrc_cache_lock", "isrc_cache.lock",
        "Serializes the read, merge and replace of the ISRC cache so two processes never lose "
        "each other's answers; beside its file for the counter lock's reason.",
    ),
    _installation(
        "catalogue_refusals", "catalogue_refusals.json",
        "When each record shop began refusing this client and its latest refusal (U284), so a "
        "report can say for how long. A fact about this machine's client; losing it costs only "
        "the date.",
    ),
    _installation(
        "catalogue_refusals_lock", "catalogue_refusals.lock",
        "Serializes the read, merge and replace of the catalogue refusal record so two sweeps "
        "never lose each other's dates; beside its file for the counter lock's reason.",
    ),
    _installation(
        "identify_cache", "identify_cache",
        "Identification answers, one document per recording keyed by a digest of its bytes and "
        "chunk plan. A paid fact about the AUDIO, so it serves every library; losing it costs "
        "money, not data.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "mix_scratch", "mix_scratch",
        "A mix fetched from a web address, one folder per address, removed when the pass ends. "
        "INPUT and never library material: a file left beside the music is one rekordbox or a "
        "library walk could pick up.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "genre_lookup_cache", "genre_lookup_cache.json",
        "Third-party catalog lookups keyed by track, replayable from the network and unrelated to "
        "which library asked; losing it costs time and no data.",
    ),
    _installation(
        "label_crawl_cache", "label_crawl",
        "The crawl half of a directory that straddled both roots (D4): replayable lookups, plus "
        "since R-1091 the release reads that let a stopped label playlists build resume. Losing "
        "it costs calls.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "label_intent", "label_intent.json",
        "The curated half of a file that straddled both roots (D4): labels followed and how deep. "
        "The source committed it to git with the watermarks; the split makes intent exportable "
        "and leaves watermarks with the library.",
    ),
    _installation(
        "label_intent_lock", "label_intent.lock",
        "Without it two processes each adding a label both write, and the second rename discards "
        "the first add while reporting success. NEVER_RESTORED for the inode reason every lock "
        "here shares.",
    ),
    _installation(
        "landing_locks", "landing_locks",
        "One lock per batch name, held by ``intake land`` across its moves so two landings never "
        "take each other's files (R-432). Installation-scoped ON PURPOSE: exFAT advisory locks "
        "were never verified, so two machines landing at once is given up.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "credential_index", "credential_index.json",
        "The NAMES of recorded credentials, never values, so doctor can say whether one is set "
        "without a retrieval that would raise the macOS keychain prompt in an unattended check.",
    ),
    _installation(
        "credential_index_lock", "credential_index.lock",
        "Serializes the presence index's read-modify-write. Before it existed, two processes "
        "recording one credential each lost a name in 23 of 25 trials, sending a user to "
        "re-record a credential already held.",
    ),
    _installation(
        "job_queue", "jobs",
        "KTD21: a detached job belongs to the machine running it. The queue is per install and a "
        "library per config, so a job record must NAME the library it targets, or a queue drained "
        "after reconfiguring hits the wrong volume.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "backup_outcomes", "backup_outcomes",
        "Each queued backup item's rclone argv and return codes, one file per job and item "
        "(R-349), so a failed transfer is diagnosable. A failure writes directly, since a commit "
        "would complete the item; keyed by job, beside the queue.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "backup_manifest", "backup_manifest.json.gz",
        "What the last file mirror left on the remote, path by path, so a backup sends only "
        "change (U317). INSTALLATION because the library's state folder is mirrored; a record for "
        "another library, mirror or later backup is not trusted.",
    ),
    _installation(
        "backup_database_fingerprint", "backup_database_fingerprint.json",
        "The fingerprint of the database set the last snapshot copied, so an unchanged database "
        "is not copied again (U317). Installation state for the manifest's reason, keyed by "
        "database, snapshot root and library.",
    ),
    _installation(
        "backup_census", "backup_census.json",
        "How many files the last file mirror walked for this root and mirror (R-1761), so a "
        "backup refuses the empty folder an unmounted volume leaves. Never removed before a "
        "transfer, so a failed run keeps it.",
    ),
    _installation(
        "run_state", "runs",
        "One record per run, its gates, decisions and outstanding actions, so a gate is "
        "answerable from a later process (R33). Installation-scoped like the job queue, naming "
        "its library; rolling it back would resurrect stale decisions.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "held_plans", "runs-held",
        "The plan a verb answered over later commands holds (U209), so its gates and write use "
        "the plan first shown rather than replanning at provider cost. Beside the run records, "
        "not inside them; losing it costs a replan.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "app_token", "app_token",
        "A random token minted per server start for the local control plane. Not a service "
        "credential and must NOT survive a restart, so it stays a 0600 file outside the keychain.",
    ),
    _installation(
        "dashboard_snapshot", "dashboard_snapshot.json",
        "Last-good dashboard render numbers so it draws with the volume unmounted; "
        "library-scoped, it would be unreadable in exactly the case it serves.",
    ),
    # Library-scoped.
    _library(
        # Composed from library.db_path, since rekordbox decides where it sits.
        "rekordbox_db", "", SnapshotRole.COUPLED,
        "The database is the library, so a per-installation copy would be a DIFFERENT library "
        "under one name. COUPLED because KTD21b rolls it back with the state describing it; "
        "LibraryConfig.db_outside_root_acknowledged_on constrains where it sits.",
        # The centre of the coupled set; outside effects are declared below.
        rollback_effects=(RollbackEffect.NONE,),
        # The only SQLite database, so the only entry with sidecars (KTD21b).
        sidecars=SQLITE_SIDECARS,
    ),
    _library(
        "write_lock", "write.lock", SnapshotRole.NEVER_RESTORED,
        "KTD17 and R31: under the installation root, a second install holds a lock the first "
        "cannot see, and the old system needs it beside the library in the overlap. "
        "NEVER_RESTORED: replacing its directory swaps the inode a live flock holds.",
    ),
    _library(
        "session_lock", "session.lock", SnapshotRole.NEVER_RESTORED,
        "The whole-run lock for a destructive session (R31). Per-installation placement makes two "
        "machines invisible to each other, and like the write lock a restore never replaces it.",
    ),
    _library(
        "session_log", "sessions", SnapshotRole.SURVIVES_ROLLBACK,
        "Run state machines, frozen plans and the created-playlist ledger, snapshotted with the "
        "database (KTD21b) and read in the overlap. SURVIVES rollback, which would erase which "
        "sessions are restorable.",
        medium=Medium.DIRECTORY,
    ),
    _library(
        "snapshots", "snapshots", SnapshotRole.SURVIVES_ROLLBACK,
        "KTD21's headline case: beside the library, any installation can restore any session. "
        "SURVIVES rollback, since capturing the store would nest every earlier snapshot in each "
        "new one.",
        medium=Medium.DIRECTORY,
    ),
    _library(
        "favorites_state", "favorites_state.json", SnapshotRole.COUPLED,
        "rekordbox rows already colored and tagged, so a second install does not redo each as a "
        "guarded live write. COUPLED: kept over a restored database it claims work that no longer "
        "exists.",
        # The reverse sweep hearts tracks at the provider, which never rolls back.
        rollback_effects=(RollbackEffect.REMOTE_PLAYLIST_PREFIX,),
    ),
    _library(
        "favorites_state_lock", "favorites_state.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the favorites state's read-modify-write; library-scoped so a second machine "
        "sees it. NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    _library(
        "energy_calibration", "energy_calibration.json", SnapshotRole.NEVER_RESTORED,
        "Cut points fitted to THIS library's values (KTD21); losing them silently reroutes "
        "unchanged tracks. NEVER_RESTORED: the restamp they drove wrote files, which a database "
        "restore does not roll back.",
    ),
    _library(
        "energy_feature_cache", "energy_features.json", SnapshotRole.NEVER_RESTORED,
        "Per-file signal features keyed on this library's files; losing them costs a full "
        "re-analysis. NEVER_RESTORED: files do not roll back and the cache is re-derivable.",
    ),
    _library(
        "energy_undo_log", "energy_undo.json", SnapshotRole.NEVER_RESTORED,
        "The ONLY copy of each file's pre-restamp energy value. Never rolled back: the restamp "
        "wrote files a database restore does not undo, so losing the log is data loss.",
    ),
    _library(
        "vocal_calibration", "vocal_calibration.json", SnapshotRole.NEVER_RESTORED,
        "The hand-set vocal cut for this library; losing it silently changes routing. "
        "NEVER_RESTORED like energy calibration, since its effects landed on files.",
    ),
    _library(
        "genre_gaps", "genre_gaps.json", SnapshotRole.NEVER_RESTORED,
        "Incoming genre strings with no folder in THIS library's taxonomy, keyed by vendor string "
        "so R19's re-key does not apply. NEVER_RESTORED: a gap is a fact about what arrived.",
    ),
    _library(
        "genre_tag_undo_log", "genre_tag_undo.json", SnapshotRole.NEVER_RESTORED,
        "Each file's original value for reverting on-disk tag writes. Losing it or rolling it "
        "back makes hundreds of file writes permanent, as with the energy undo log.",
    ),
    _library(
        "playlist_parole_ledger", "playlist_parole.json", SnapshotRole.COUPLED,
        "First-seen dates for playlists in the rotation's holding area. COUPLED: a restored "
        "playlist keeping a rolled-forward date would pass the deadline and be deleted early.",
        # Dates for database rows only.
        rollback_effects=(RollbackEffect.NONE,),
        rekey_from_display_name=True,
    ),
    _library(
        "track_provider_id_cache", "track_provider_ids.json", SnapshotRole.NEVER_RESTORED,
        "File location to provider track id, keyed on THIS library's paths, so any other library "
        "only misses. NEVER_RESTORED: paths do not move on restore and it is re-derivable.",
    ),
    _library(
        "review_queue", "review", SnapshotRole.COUPLED,
        "KTD12's adjudication surface for THIS library's candidates, so a decided item is not "
        "re-asked elsewhere. COUPLED: a verdict becomes a decline R30 rolls back, or an item is "
        "queued and decided at once.",
        medium=Medium.DIRECTORY,
        # An item is a question, and asking one changes nothing outside.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "label_outcomes", "label_outcomes", SnapshotRole.COUPLED,
        "The landed half of the split directory (D4): what a label sweep took into this library. "
        "COUPLED like the watermarks, or R25's audit outlives the intake it records.",
        medium=Medium.DIRECTORY,
        # The landed audio stays on the volume after its rows roll back.
        rollback_effects=(RollbackEffect.DOWNLOADED_FILE,),
    ),
    _library(
        "label_watermarks", "label_watermarks.json", SnapshotRole.COUPLED,
        "The library half of the split registry (D4), per-source records of what was taken in "
        "(R25), once committed to git. COUPLED, named by R30, or the next sync skips the tracks a "
        "restore removed.",
        # Audio landed and the provider playlist was renamed; neither rolls back.
        rollback_effects=(
            RollbackEffect.DOWNLOADED_FILE,
            RollbackEffect.REMOTE_PLAYLIST_PREFIX,
        ),
    ),
    _library(
        "label_watermarks_lock", "label_watermarks.lock", SnapshotRole.NEVER_RESTORED,
        "Without it two sweeps both write and the second rename discards the first label's "
        "advance. NEVER_RESTORED, under local not coupled, for the inode reason every lock "
        "shares.",
    ),
    _library(
        "label_sync", "label_sync.json", SnapshotRole.COUPLED,
        "The guided label sync's record (U107): releases asked about, the pending question and "
        "answers. COUPLED because it describes review rows, or a release answered in a rolled "
        "back run is never asked again.",
        # A download an answer leads to is declared by U108's intake records.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "tag_suggest_catalogue", "tag_suggest_catalogue.json", SnapshotRole.NEVER_RESTORED,
        "Catalogue answers for each row tag suggest offered a genre for (U114), kept a week so "
        "applying rebuilds the plan the gate showed. NEVER_RESTORED: replayable from the network.",
    ),
    _library(
        "label_sync_lock", "label_sync.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes answers to the guided label sync's record, so a structured answer beside an "
        "interactive run never discards the other. NEVER_RESTORED for the inode reason.",
    ),
    _library(
        "tree_registry", "tree_registry.json", SnapshotRole.COUPLED,
        "KTD22 cutover modes and adopted root ids for one library; committed, they would ship one "
        "person's flips. COUPLED: registry and database rolling back apart is what KTD21b "
        "prevents.",
        # A cutover's effect is in the database; see cratekit.core.reconcile.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "tree_registry_lock", "tree_registry.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the registry's read, add, write cycle; a lost flip sends that tree's next "
        "write through the XML bridge, which replaces the native tree (U9's A2). NEVER_RESTORED, "
        "outside the COUPLED directory.",
    ),
    _library(
        "routing_intents", "routing_intents.json", SnapshotRole.COUPLED,
        "Each new track's intended placement, decided before its row exists, about ONE library's "
        "files and rows. COUPLED: a routed mark surviving a membership rollback reports tracks "
        "placed in no playlist.",
        # Intents and marks, both about database rows.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "routing_intents_lock", "routing_intents.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the multi-source ledger, whose lost update closes a run clean over an "
        "unplaced track; beside the library so a second install and the old system contend. "
        "NEVER_RESTORED for the write lock's inode reason.",
    ),
    # NONE on purpose (U32): every record names rows the restore replaces.
    _library(
        "tree_convergence", "tree_convergence.json", SnapshotRole.COUPLED,
        "R39: last fingerprint, unconverged trees and rebuild node maps for THIS library's native "
        "trees. COUPLED, or a surviving fingerprint flags our own restore, a node map duplicates "
        "rows, a flag outlives its damage.",
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "tree_convergence_lock", "tree_convergence.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the rebuild, check and governed writes on the convergence document, whose "
        "lost update drops an unconverged flag. NEVER_RESTORED, outside the COUPLED directory.",
    ),
    _library(
        "tombstones", "tombstones.json", SnapshotRole.COUPLED,
        "R36: acquisitions this library deliberately declined to hold, a new shape with nothing "
        "to port. COUPLED, named by R30.",
        # Removal means the Trash, and the file does not leave it on rollback.
        rollback_effects=(RollbackEffect.TRASHED_FILE,),
        decision_store=True,
    ),
    _library(
        "declines", "declines.json", SnapshotRole.COUPLED,
        "R36's other half: candidates a human rejected, library-scoped so no second machine "
        "re-asks. COUPLED, named by R30, rolling back with the review queue.",
        # A decline suppresses an acquisition that never happened.
        rollback_effects=(RollbackEffect.NONE,),
        decision_store=True,
    ),
    _library(
        "decision_store_locks", "decision_locks", SnapshotRole.NEVER_RESTORED,
        "One lock per decision store; unlocked, eight processes recording two hundred decisions "
        "kept seventy one. NEVER_RESTORED outside the COUPLED stores, and a directory so each "
        "lock derives from its store's key.",
        medium=Medium.DIRECTORY,
    ),
    _library(
        "deletion_watermark", "deletion_watermark.json", SnapshotRole.COUPLED,
        "R35: how far the deletion pass has read THIS library's soft-delete markers, and each "
        "absent row's number (R-1037). COUPLED, named by R30, or it skips markers a restore put "
        "back.",
        # A position; the Trash effect is declared on tombstones.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "deletion_watermark_lock", "deletion_watermark.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the deletion watermark's read and advance; a dropped advance re-offers "
        "answered removals, a dropped re-baseline a whole library's. NEVER_RESTORED, outside the "
        "COUPLED directory.",
    ),
    _library(
        "source_watermarks", "source_watermarks.json", SnapshotRole.COUPLED,
        "R25's per-source cursors for THIS library, distinct from the per-label label_watermarks "
        "(U26). COUPLED, or after a restore removes an intake, status still reports its source "
        "clean.",
        rollback_effects=(
            RollbackEffect.DOWNLOADED_FILE,
            RollbackEffect.REMOTE_PLAYLIST_PREFIX,
        ),
    ),
    _library(
        "source_watermarks_lock", "source_watermarks.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the source watermark document so two increments never discard each other's "
        "advance. NEVER_RESTORED, since a lock in the COUPLED directory has its inode swapped.",
    ),
    _library(
        "bandcamp_fetched", "bandcamp_fetched.json", SnapshotRole.NEVER_RESTORED,
        "U176: every Bandcamp purchase fetched into staging, by purchase id rather than a "
        "checkpoint that hid older purchases. NEVER_RESTORED: the fetch happened on disk and at "
        "the account, so a rollback fetches again.",
    ),
    _library(
        "bandcamp_fetched_lock", "bandcamp_fetched.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the fetch record so two fetches never drop each other's purchase and fetch it "
        "again next run. NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    _library(
        "sync_mark_record", "sync_marks.json", SnapshotRole.NEVER_RESTORED,
        "R-838: which account playlists a sync pass prefixed, with each title before and after, "
        "so ``sync unmark`` can undo a mark and refuse one it never wrote. NEVER_RESTORED: the "
        "renames live on the provider's server.",
    ),
    _library(
        "sync_mark_record_lock", "sync_marks.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the mark record so two marks landing at once never drop each other's entries. "
        "NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    _library(
        "sync_unavailable_record", "sync_unavailable.json", SnapshotRole.NEVER_RESTORED,
        "U320: synced playlists ``sync removed`` found gone with ids answering not found, and "
        "which are retired, so a deleted one stops holding back removals. NEVER_RESTORED: it "
        "records the provider's answers.",
    ),
    _library(
        "sync_unavailable_record_lock", "sync_unavailable.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the unavailable record so two runs never drop each other's sightings. "
        "NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    _library(
        "sync_artifacts", "sync_artifacts.json", SnapshotRole.COUPLED,
        "Every file a sync run created, registered at creation so staging crash debris never "
        "becomes intake. COUPLED, so a restore forgets registrations for removed intake and those "
        "files are debris again.",
        rollback_effects=(RollbackEffect.DOWNLOADED_FILE,),
    ),
    _library(
        "sync_artifacts_lock", "sync_artifacts.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes concurrent registrations, since a lost one hides crash debris that then looks "
        "like intake. NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    _library(
        "backup_ack", "backup_ack.json", SnapshotRole.NEVER_RESTORED,
        "KTD18's queue-time acknowledgment and the backup age it showed, for a backup of THIS "
        "library. NEVER_RESTORED: the backup is off this volume, so a rollback would demand a "
        "fresh acknowledgment.",
    ),
    _library(
        "backup_facts", "backup_facts.json", SnapshotRole.NEVER_RESTORED,
        "When each portion of THIS library was last backed up, per portion since the database can "
        "refuse while the mirror completes (R15, KTD23). Library-scoped so installs agree; "
        "NEVER_RESTORED, the backup is off this volume.",
    ),
    _library(
        "setbuilder_index_cache", "setbuilder_index.json", SnapshotRole.NEVER_RESTORED,
        "Per-file ranking signals keyed on THIS library's paths and mtimes, saving a minutes-long "
        "tag scan. NEVER_RESTORED: files do not roll back and entries re-derive from them.",
    ),
    _library(
        "taxonomy_active", "taxonomy.toml", SnapshotRole.COUPLED,
        "S6: the active taxonomy, copied from the shipped template at setup, so a library is "
        "self-describing to a second install. COUPLED: the database tree and this template are "
        "one decision in two files.",
        # Nothing outside the database reads it.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "taxonomy_origin", "taxonomy.origin.toml", SnapshotRole.COUPLED,
        "R-689: the shipped template and digest the active copy came from, so doctor tells a "
        "stale copy from an edited one. COUPLED with the copy, or a restored older copy reads as "
        "edited.",
        # A record about the active copy. Nothing routes by it; doctor reads it.
        rollback_effects=(RollbackEffect.NONE,),
    ),
    _library(
        "active_run_sentinel", ".cratekit_active_run.json", SnapshotRole.NEVER_RESTORED,
        "The advisory cross-machine run heartbeat, carried over from the source at the library "
        "ROOT so another system finds it without this layout. NEVER_RESTORED: restoring it "
        "advertises a run that ended.",
        at_library_root=True,
    ),
    _library(
        "set_workspaces", "", SnapshotRole.NEVER_RESTORED,
        "Per-set stage artifacts in a Cratekit subdirectory INSIDE the configured sets directory, "
        "composed by ``state_path``, never the sets directory, whose recordings every inventory "
        "pass would then sweep up.",
        medium=Medium.DIRECTORY,
    ),
    # U32's entries. Append, never insert, so a duplicate key conflicts textually.
    _library(
        "restore_reconciliation", "restore_reconciliation.json", SnapshotRole.SURVIVES_ROLLBACK,
        "What a restore could not undo (downloaded audio, provider renames, trashed files) and "
        "each disposition, plus trees a pre-cutover restore marks. SURVIVES rollback, or a later "
        "restore erases what is still owed.",
    ),
    _library(
        "restore_reconciliation_lock", "restore_reconciliation.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the reconciliation record's read and write, a lost update two units shipped. "
        "NEVER_RESTORED, under local apart from the history document, as the restoring process "
        "holds it.",
    ),
    _installation(
        "recovery_lock", "recovery.lock",
        "The ONE gate a bare-metal recovery can take once the library volume, home of every KTD21 "
        "lock, is gone; installation-scoped because only this machine's processes can contend "
        "then.",
    ),
    # Appended, for the reason above.
    _library(
        "adoption_ledger", "adoption_ledger.json", SnapshotRole.COUPLED,
        "Applied entries of an approved adoption plan, resumable across sessions (R26). COUPLED: "
        "they name membership rows a restore rolls back, or the resume skips work the restore "
        "undid.",
        # Every COUPLED entry names its effect; tests/test_restore.py checks.
        rollback_effects=(RollbackEffect.WRITTEN_FILE_TAG,),
    ),
    _library(
        "adoption_tag_revert_log", "adoption_tag_revert.json", SnapshotRole.NEVER_RESTORED,
        "The only copy of each file's tag value before adoption overwrote it. NEVER_RESTORED like "
        "the undo logs, and its own entry because the adoption ledger has the opposite role.",
    ),
    _library(
        "adoption_locks", "adoption_locks", SnapshotRole.NEVER_RESTORED,
        "One lock per adoption document; a lost applied record redoes work and a lost revert "
        "record loses a tag. NEVER_RESTORED outside the COUPLED ledger, and a directory so no "
        "document arrives lockless.",
        medium=Medium.DIRECTORY,
    ),
    # U33's entries, appended for the reason above.
    _library(
        "outbound_writes", "outbound_writes.json", SnapshotRole.SURVIVES_ROLLBACK,
        "Remote ids a playlist export or heart-back wrote on THIS library's account (U33). "
        "SURVIVES rollback: the account does not roll back, and a forgotten id makes the next "
        "export duplicate a playlist.",
    ),
    _library(
        "outbound_writes_lock", "outbound_writes.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the outbound ledger so two exports never both create a remote playlist and "
        "lose one. NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    # U130's entries, appended.
    _library(
        "playlist_pairs", "playlist_pairs.json", SnapshotRole.SURVIVES_ROLLBACK,
        "U130: account and rekordbox playlists kept as one list, with each side's last synced "
        "state; losing it makes the next sync add only. SURVIVES rollback for the outbound "
        "ledger's reason.",
    ),
    _library(
        "playlist_pairs_lock", "playlist_pairs.lock", SnapshotRole.NEVER_RESTORED,
        "Serializes the playlist pairs so two syncs never discard each other's snapshot. "
        "NEVER_RESTORED for the inode reason every lock here shares.",
    ),
    _library(
        "mirror_plans", "mirror_plans", SnapshotRole.NEVER_RESTORED,
        "The account mirror plan frozen at its organize gate (R-1031), so the applying run "
        "applies the approved digest. NEVER_RESTORED: a frozen plan belongs to a run, and a "
        "restored one applies what nobody saw.",
        medium=Medium.DIRECTORY,
    ),
    _library(
        "rehearsal_areas", "rehearsals", SnapshotRole.NEVER_RESTORED,
        "The volume half of each rehearsal's scratch (U162), on the library volume so clones stay "
        "clones, kept only on failure. NEVER_RESTORED: a scratch copy is nobody's state.",
        medium=Medium.DIRECTORY,
    ),
    _installation(
        "rehearsals", "rehearsals",
        "The local half of rehearsal scratch plus one record per finished rehearsal, its plan "
        "digest and lines, which the live run compares against (U162). Installation-scoped beside "
        "the run records.",
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
