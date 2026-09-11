"""Feature Inventory row 31: library backup, and the age fact R15 reads.

A library backup has two halves with different rules, and treating them as one
job is the defect this module is shaped around.

THE FILE MIRROR can run at any time. It copies the volume to the configured
remote and moves anything it is about to overwrite or delete into a dated archive
first, so one run is always undoable.

THE DATABASE cannot. rekordbox keeps the database open, and its background agent
keeps writing through Cloud Library Sync even when the window is closed, which is
vendor-confirmed and is the fact the source system's original check missed: it
watched only the visible application. A copy taken while either process is live
captures a torn database, and a torn SQLite database opens cleanly and is
silently wrong, which is the worst shape a backup can take. So the database
fileset is EXCLUDED from the mirror outright and comes only from a gated, dated
snapshot taken with both processes confirmed gone.

Because those two complete independently, what gets published is a fact PER
PORTION (see ``core.backup_facts``). A single timestamp would report a library
whose database has not been captured in three weeks as fully backed up, which is
precisely the thing R15's warning exists to say.

WHAT THIS PORT CHANGES, beyond translating the shell.

* **Nothing is hardcoded.** The source names one person's volume, one person's
  remote, and two of their bucket names, with no override for any of them. All
  four are configuration (``[backup]``), the volume is the configured library
  root, and the database path is the configured one rather than an assumed
  layout under the volume.
* **The process probe is an injected seam, not an environment variable.** The
  source lets ``DJ_BACKUP_FAKE_RUNNING`` override its safety check so its tests
  can drive it. That variable is readable in production too, which makes the one
  guard standing between a live database and a torn copy switchable by anything
  that can set an environment variable.
* **The plan is separated from the run.** Deciding what will happen and doing it
  are different functions over the same data, so the dry run reports exactly what
  the real run would do rather than approximating it with a second code path.
* **Restore is a named decision, not a prompt.** The source waits on standard
  input before overwriting a library. R33 says a gated decision is answerable by
  name and that an unanswerable gate exits with a documented code leaving state
  resumable, which a blocking read cannot do inside a detached job.
* **No provider-specific flag is baked in.** The source passes a Google Drive
  option to its prune. The remote is configuration now, so a flag that is correct
  for one provider and meaningless or wrong for another does not belong in the
  command; rclone carries per-remote options in its own configuration, which is
  where a provider-specific choice belongs.
* **Sidecar suffixes are derived** from the state inventory rather than typed
  here, so the set of files that travel with the database cannot drift from the
  set the snapshot unit captures.
* **The restore passes the destructive-session gates** (the residual finding "The
  backup restore is not yet bound to the destructive-session gates", KTD24). A restore
  replaces a live database and the files beside it while writing no database
  row, so a rule that bound the library lock, the backup acknowledgment and the
  volume identity assertion to database WRITES would leave the single most
  destructive thing this product does outside the safety spine. The gates bind
  to destruction. Both halves of a restore pass them, and both take the guard as
  an injected seam so this module's own battery stays hermetic.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping, Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path

from cratekit.core import analysis_store, backup_facts, binaries, config, session
from cratekit.core.processes import (
    REKORDBOX_PROCESSES,
    ProcessLister,
    rekordbox_processes_running,
    running_process_names,
)

#: Volume clutter no backup should carry. Platform metadata directories and
#: resource-fork stubs: large in aggregate, meaningless off the machine that made
#: them, and regenerated on demand.
VOLUME_EXCLUDES: tuple[str, ...] = (
    ".DS_Store",
    ".Spotlight-V100/**",
    ".fseventsd/**",
    ".Trashes/**",
    ".DocumentRevisions-V100/**",
    ".TemporaryItems/**",
    "._*",
    "$RECYCLE.BIN/**",
    "System Volume Information/**",
)

#: Where rekordbox keeps its own application settings, per platform. Not a config
#: key: it is a fact about where the application puts its files, and a user who
#: could change it would only be able to change it to the wrong answer. Absent
#: platforms simply contribute nothing, which is reported rather than assumed.
_SETTINGS_DIRS_BY_PLATFORM: dict[str, tuple[str, ...]] = {
    "darwin": ("Library/Application Support/Pioneer/rekordbox6",),
    "win32": ("AppData/Roaming/Pioneer/rekordbox6",),
}

#: Command labels. Named constants rather than literals at each site, because
#: the executor and the dry-run translator both branch on them: two spellings of
#: one label makes the preview and the run disagree about which command they are
#: looking at, which is the exact class of divergence this module's plan/run
#: split exists to remove.
MIRROR = "mirror"
PRUNE_ARCHIVE = "prune-archive"
PRUNE_ARCHIVE_FOLDER = "prune-archive-folder"
SNAPSHOT_DATABASE = "snapshot-database"
SNAPSHOT_SETTINGS = "snapshot-settings"
RESTORE_MIRROR = "restore-mirror"
RESTORE_DATABASE = "restore-database"
LIST_SNAPSHOTS = "list-snapshots"

#: What a portion says about a rotation that did not happen, as codes rather
#: than as sentences, for the same reason the labels above are constants: a
#: producer and a reader that spell one condition differently disagree about
#: which condition they are looking at.
#:
#: TWO CODES, BECAUSE THESE ARE TWO CONDITIONS WITH DIFFERENT FIXES. A listing
#: this account cannot get is a remote or a credential problem and nothing was
#: removed. A purge that failed on a folder the listing named is that folder,
#: and the rest of the rotation happened. One code over both would leave the
#: difference in the message, which is the only part nothing can branch on.
#:
#: NEITHER IS A REFUSAL CAUSE. Every member of :class:`Refusal` is a reason one
#: portion will NOT run, decided before anything is attempted. These two are
#: reports about a rotation that failed AFTER the backup in the same portion
#: succeeded, so they belong to neither ``REFUSALS`` nor the reserved cause
#: table.
ARCHIVE_LISTING_FAILED = "archive-listing-failed"
ARCHIVE_PURGE_FAILED = "archive-purge-failed"

#: The warning code for an analysis share neither portion reaches (R-14). Not a
#: refusal for the same reason as the two above: the database portion still runs
#: and still protects the database, and what it cannot say on its own is that
#: the grids beside it are in no copy at all.
ANALYSIS_SHARE_NOT_CARRIED = "analysis-share-not-carried"

#: Labels whose command TRANSFERS data, so a dry run must neutralize them.
#: Derived membership, checked by a test, so a transferring command added later
#: cannot quietly become one the preview would really execute.
TRANSFERRING_LABELS: frozenset[str] = frozenset(
    {MIRROR, SNAPSHOT_DATABASE, SNAPSHOT_SETTINGS, RESTORE_MIRROR, RESTORE_DATABASE}
)

#: How many dated archive folders survive a prune. One is a single run's
#: rollback, which is what the source keeps and what a consumer cloud quota
#: tolerates. It is a parameter everywhere below so a user with room can keep
#: more; what is NOT negotiable is that pruning happens only after the mirror
#: succeeds, so a failed run never touches the safety net.
DEFAULT_ARCHIVE_KEEP = 1


class Refusal(StrEnum):
    """Why a portion will not run, as a structured cause (KTD25, D2).

    Each member names one diagnosis with one fix, and none of them carries the
    text a user types. U5 reserves an exit code and a remediation per member.
    """

    RCLONE_MISSING = "rclone-missing"
    REMOTE_NOT_CONFIGURED = "remote-not-configured"
    DESTINATION_NOT_CONFIGURED = "destination-not-configured"
    LIBRARY_ROOT_ABSENT = "library-root-absent"
    REKORDBOX_RUNNING = "rekordbox-running"
    DATABASE_ABSENT = "database-absent"
    RESTORE_NOT_CONFIRMED = "restore-not-confirmed"
    RESTORE_TARGET_ABSENT = "restore-target-absent"
    NO_SNAPSHOT_AVAILABLE = "no-snapshot-available"
    # U27. A transfer this module ran came back non zero. Its own member rather
    # than one of the conditions above, because every one of those is decided
    # BEFORE anything is attempted and this one is the attempt failing: the
    # remote was reachable enough to plan against and then was not.
    RESTORE_TRANSFER_FAILED = "restore-transfer-failed"


#: Every refusal this module can raise, derived from the enum so U5's reservation
#: check cannot fall behind a member added later (P3, P5).
REFUSALS: tuple[Refusal, ...] = tuple(Refusal)


class BackupRefused(Exception):
    """A whole-run refusal. Per-portion refusals are reported, not raised."""

    def __init__(self, refusal: Refusal, detail: str) -> None:
        super().__init__(detail)
        self.refusal = refusal
        self.detail = detail


@dataclass(frozen=True, slots=True)
class Command:
    """One external invocation, as data, so a plan can be shown before it runs."""

    label: str
    argv: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


Runner = Callable[[Command], CommandResult]
# ``ProcessLister`` is imported from ``core.processes`` above, so the injection
# point both guards accept is one type rather than two identical ones.

#: The destructive-session gates, as an injectable seam. A zero-argument callable
#: returning a context manager, so a caller can supply the real gates, a
#: pass-through for a battery that is testing something else, or its own already
#: open guard.
GateGuard = Callable[[], AbstractContextManager[object]]

#: What the session log calls a restore. A workflow LABEL rather than a verb
#: name: this module does not decide what the command-line layer calls itself,
#: and the log records what happened rather than what was typed.
RESTORE_WORKFLOW = "backup-restore"


def _restore_gates(cfg: config.Config, gates: GateGuard | None) -> AbstractContextManager[object]:
    """The gates a restore runs behind, real unless the caller injected otherwise.

    KTD24 in one function. The library lock stops a second process restoring over
    this one, the backup acknowledgment stops a restore nobody has confirmed they
    can afford, and the volume identity assertion stops a restore landing on a
    disk that is not the library it was recorded for. None of those is a database
    write, which is exactly why binding them to writes would have missed this.

    IT DECLARES ITSELF A RECOVERY, and that declaration buys exactly one thing:
    a library latched by a session that ended ``committed-unverified`` does not
    refuse this. It cannot, because a restore is what that latch's own refusal
    names as the remedy, and a latch that condemned its remedy would leave a
    library with no exit but a hand-edited file. All three gates above still
    apply here, unchanged.
    """
    if gates is not None:
        return gates()
    return session.assert_gates(
        cfg, workflow=RESTORE_WORKFLOW, intent=session.Intent.RECOVERY
    )


@dataclass(frozen=True, slots=True)
class PortionPlan:
    """What one portion will do, or why it will not.

    ``refusal`` and ``commands`` are mutually exclusive by construction: a
    refused portion carries no commands, so a caller cannot execute a plan it was
    told would not run.

    ``warnings`` is what the plan already knows the run will NOT cover, in the
    same ``code`` and ``message`` pair :class:`PortionOutcome` carries. It rides
    through to the outcome whether or not the portion runs, because it is a fact
    about what the backup reaches rather than about how this run went.
    """

    portion: backup_facts.Portion
    refusal: Refusal | None = None
    detail: str = ""
    commands: tuple[Command, ...] = field(default_factory=tuple)
    warnings: tuple[Mapping[str, str], ...] = field(default_factory=tuple)

    @property
    def will_run(self) -> bool:
        return self.refusal is None and bool(self.commands)


@dataclass(frozen=True, slots=True)
class BackupPlan:
    """The whole run: one entry per portion, always, in declaration order.

    ``archive_keep`` rides on the PLAN rather than being passed again at
    execution. Taking it twice is two places for one decision, and the two can
    disagree: a plan built to keep three and executed with a keep of one deletes
    two archives the preview said it would leave alone.
    """

    stamp: str
    portions: tuple[PortionPlan, ...]
    archive_keep: int = DEFAULT_ARCHIVE_KEEP

    def portion(self, which: backup_facts.Portion) -> PortionPlan:
        for entry in self.portions:
            if entry.portion is which:
                return entry
        raise KeyError(f"no plan for portion {which!r}")

    @property
    def refusals(self) -> tuple[PortionPlan, ...]:
        return tuple(p for p in self.portions if p.refusal is not None)


@dataclass(frozen=True, slots=True)
class PortionOutcome:
    """What one portion did, including what it could not finish but survived.

    ``warnings`` carries conditions that are REAL and are not failures, in the
    ``code`` and ``message`` pair ``cli.output.Envelope`` uses for its own
    warnings, so one vocabulary describes a non-fatal condition everywhere in
    this program. Today its only producer is the archive rotation: a prune the
    portion deliberately does not fail on, and therefore the one thing that
    happened here that ``ran`` cannot express.

    A mapping rather than a dataclass makes an instance unhashable, which is
    safe only because nothing hashes a ``PortionOutcome``. Keep it that way.
    """

    portion: backup_facts.Portion
    ran: bool
    refusal: Refusal | None = None
    detail: str = ""
    results: tuple[CommandResult, ...] = field(default_factory=tuple)
    warnings: tuple[Mapping[str, str], ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class BackupOutcome:
    stamp: str
    portions: tuple[PortionOutcome, ...]

    @property
    def ok(self) -> bool:
        """True when every portion that was planned to run actually completed.

        A refused portion does not make the run a failure: a mirror that
        completed while the database was skipped is a successful mirror, and the
        published fact says so per portion.
        """
        return all(p.refusal is not None or p.ran for p in self.portions)


# ---------------------------------------------------------------------------
# Probes
# ---------------------------------------------------------------------------


# ``running_process_names`` and ``rekordbox_processes_running`` are imported from
# ``core.processes`` and re-exported here, so this module's public surface is
# unchanged while the name list and the matching rule have exactly one home. The
# local copies were removed when the U7 merge put them beside the database
# guard's copy and the two turned out to disagree about Windows.


def settings_directories(
    *, home: Path | None = None, platform: str | None = None
) -> tuple[Path, ...]:
    """rekordbox's own settings directories on this platform, those that exist.

    They ride the DATABASE portion rather than the mirror, and rather than being
    a portion of their own. Two reasons, and the first is the one that matters:
    the settings hold the pointer to where the database lives, so a database
    snapshot without them can be restored to a rekordbox that then looks
    somewhere else. The second is that a running application is writing them, so
    they inherit the same gate the database has.
    """
    base = home or Path.home()
    relatives = _SETTINGS_DIRS_BY_PLATFORM.get(
        sys.platform if platform is None else platform, ()
    )
    return tuple(p for p in (base / rel for rel in relatives) if p.is_dir())


# ---------------------------------------------------------------------------
# Planning
# ---------------------------------------------------------------------------


def _require_destinations(cfg: config.Config) -> None:
    """Refuse before doing anything when the wizard's answers are missing.

    A whole-run refusal rather than a per-portion one: with no remote there is no
    portion that could run, and reporting two identical refusals says the same
    thing twice.
    """
    if not (cfg.backup.remote or "").strip():
        raise BackupRefused(
            Refusal.REMOTE_NOT_CONFIGURED,
            "no backup remote is configured. Cratekit ships no destination: the "
            "remote names an account that belongs to the user, so it is captured "
            "at setup and never defaulted.",
        )
    missing = [
        name
        for name, value in (
            ("backup.dest", cfg.backup.dest),
            ("backup.archive_root", cfg.backup.archive_root),
            ("backup.db_dest_root", cfg.backup.db_dest_root),
        )
        if not (value or "").strip()
    ]
    if missing:
        raise BackupRefused(
            Refusal.DESTINATION_NOT_CONFIGURED,
            f"these backup destinations are not configured: {', '.join(missing)}. "
            f"The mirror, the dated archive, and the database snapshots are three "
            f"distinct places on purpose, so one of them being unset is not "
            f"something to guess at.",
        )


def _rclone() -> str:
    """The rclone path, or a refusal carrying this module's own cause.

    ``binaries.resolve`` raises its own exception type with its own remedy token.
    Letting that escape from here would give a caller two unrelated failure
    vocabularies for one situation, which is the KTD25 defect: the caller would
    have to know about both to report either.
    """
    try:
        return binaries.resolve("rclone")
    except binaries.BinaryNotFound as exc:
        raise BackupRefused(
            Refusal.RCLONE_MISSING,
            f"{exc} It is the one program that talks to the remote, so nothing "
            f"here can proceed without it.",
        ) from exc


def stamp_for(now: datetime) -> str:
    """The dated folder name one run writes into.

    UTC, and sortable as text, because the prune below picks the newest folder by
    string order. A local-time stamp reverses order for an hour every year when
    the clock goes back, and the prune would then delete the newest archive.
    """
    return now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


def _exclude_args(patterns: Sequence[str]) -> tuple[str, ...]:
    out: list[str] = []
    for pattern in patterns:
        out += ["--exclude", pattern]
    return tuple(out)


def database_fileset(cfg: config.Config) -> tuple[Path, ...]:
    """The database and its SQLite sidecars, as ONE matched set.

    Derived from the state inventory (``sidecar_paths``) rather than listed here.
    A hand-kept list is how a capture ends up copying a database file without the
    write-ahead log beside it, which produces a copy that opens cleanly and is
    silently missing every uncheckpointed transaction.
    """
    return (config.state_path("rekordbox_db", cfg), *config.sidecar_paths("rekordbox_db", cfg))


def _mirror_excludes(cfg: config.Config) -> tuple[str, ...]:
    """Volume clutter, plus the database fileset the mirror must never carry.

    Anchored at the volume root (a leading slash in rclone's pattern language) so
    the exclusion cannot accidentally match a similarly named file deeper in the
    tree.
    """
    root = cfg.library.root
    patterns = list(VOLUME_EXCLUDES)
    for path in database_fileset(cfg):
        try:
            patterns.append("/" + path.relative_to(root).as_posix())
        except ValueError:
            # A database outside the library root is an acknowledged
            # configuration (see LibraryConfig.db_outside_root_acknowledged_on).
            # It is not in the mirror's tree at all, so there is nothing to
            # exclude, and inventing a pattern for it would exclude nothing while
            # looking like protection.
            continue
    return tuple(patterns)


def plan_backup(
    cfg: config.Config,
    *,
    now: datetime | None = None,
    process_lister: ProcessLister | None = None,
    archive_keep: int = DEFAULT_ARCHIVE_KEEP,
    settings_dirs: Sequence[Path] | None = None,
) -> BackupPlan:
    """Decide what a run would do. Touches no remote and copies nothing.

    The same function serves the dry run and the real run, so "what it says it
    will do" and "what it does" are one decision rather than two that can
    disagree. That is not a refactor for elegance: the source system's dry run
    and its real run build their argument lists separately, so a change to one
    can silently make the preview wrong.

    Three inputs are seams rather than lookups, and each one is a seam because a
    test that could not control it would be a test of this machine rather than of
    the decision. ``process_lister`` answers which rekordbox processes are alive,
    ``settings_dirs`` names rekordbox's own settings directories, and ``now``
    fixes the dated folder. None of them is an environment variable: the process
    probe in particular is the one guard standing between a live database and a
    torn copy, and the source system made it switchable by anything that could
    set a variable.
    """
    _require_destinations(cfg)
    stamp = stamp_for(now or datetime.now(timezone.utc))
    rclone = binaries.find("rclone")
    portions: list[PortionPlan] = []

    if rclone is None:
        detail = (
            "rclone was not found. Every portion needs it: it is the one program "
            "that talks to the remote."
        )
        return BackupPlan(
            stamp=stamp,
            archive_keep=archive_keep,
            portions=tuple(
                PortionPlan(portion=p, refusal=Refusal.RCLONE_MISSING, detail=detail)
                for p in backup_facts.Portion
            ),
        )

    portions.append(_plan_files(cfg, rclone=rclone, stamp=stamp, archive_keep=archive_keep))
    portions.append(
        _plan_database(
            cfg,
            rclone=rclone,
            stamp=stamp,
            process_lister=process_lister,
            settings_dirs=settings_dirs,
        )
    )
    return BackupPlan(stamp=stamp, archive_keep=archive_keep, portions=tuple(portions))


def _plan_files(
    cfg: config.Config, *, rclone: str, stamp: str, archive_keep: int
) -> PortionPlan:
    root = cfg.library.root
    if not root.is_dir():
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_ABSENT,
            detail=f"the library root {root} is not a directory; mount the volume first",
        )
    archive = f"{cfg.backup.archive_root}/{stamp}"
    commands = [
        Command(
            label=MIRROR,
            argv=(
                rclone, "sync", str(root), str(cfg.backup.dest),
                *_exclude_args(_mirror_excludes(cfg)),
                # Everything the sync is about to overwrite or delete moves here
                # FIRST, so one run is always undoable. Without it, a sync is a
                # one-way propagation of local deletions to the only copy.
                "--backup-dir", archive,
                "--transfers", "8", "--checkers", "16",
            ),
        )
    ]
    if archive_keep >= 0:
        # A separate command on purpose: it runs only after the mirror above
        # succeeds, so a failed backup never removes the rollback it might need.
        # A negative keep disables pruning entirely, for a user whose remote has
        # room and who would rather keep every run's archive.
        commands.append(
            Command(
                label=PRUNE_ARCHIVE,
                argv=(rclone, "lsf", f"{cfg.backup.archive_root}/", "--dirs-only"),
            )
        )
    return PortionPlan(
        portion=backup_facts.Portion.FILES,
        commands=tuple(commands),
        detail=(
            f"keeping the newest {archive_keep} dated archive folder(s)"
            if archive_keep >= 0
            else "keeping every dated archive folder"
        ),
    )


def _plan_database(
    cfg: config.Config,
    *,
    rclone: str,
    stamp: str,
    process_lister: ProcessLister | None,
    settings_dirs: Sequence[Path] | None,
) -> PortionPlan:
    uncovered = _uncovered_analysis_share(cfg)
    running = rekordbox_processes_running(lister=process_lister)
    if running:
        return PortionPlan(
            portion=backup_facts.Portion.DATABASE,
            refusal=Refusal.REKORDBOX_RUNNING,
            detail=(
                f"{', '.join(running)} is running, so the database may be "
                f"mid-write. A copy taken now opens cleanly and is silently "
                f"missing whatever the agent was writing, which is worse than no "
                f"copy at all. Previous dated snapshots remain the backstop."
            ),
            warnings=uncovered,
        )
    database = config.state_path("rekordbox_db", cfg)
    if not database.is_file():
        return PortionPlan(
            portion=backup_facts.Portion.DATABASE,
            refusal=Refusal.DATABASE_ABSENT,
            detail=f"no rekordbox database at the configured path {database}",
            warnings=uncovered,
        )

    destination = f"{cfg.backup.db_dest_root}/{stamp}"
    commands = [
        Command(
            label=SNAPSHOT_DATABASE,
            argv=(
                rclone, "copy", str(database), f"{destination}/db/", "--transfers", "4"
            ),
        )
    ]
    # The sidecars go into the SAME dated folder, one command each, and only when
    # present: a checkpointed database legitimately has none, so absence is
    # normal rather than an error. They share the database's LABEL rather than
    # taking a derived one, because the label is what the dry-run translator and
    # the executor both branch on, and a label built by string arithmetic is a
    # label that silently falls outside the set they check against.
    for sidecar in config.sidecar_paths("rekordbox_db", cfg):
        if sidecar.is_file():
            commands.append(
                Command(
                    label=SNAPSHOT_DATABASE,
                    argv=(rclone, "copy", str(sidecar), f"{destination}/db/"),
                )
            )
    resolved_settings = (
        settings_directories() if settings_dirs is None else tuple(settings_dirs)
    )
    for directory in resolved_settings:
        commands.append(
            Command(
                label=SNAPSHOT_SETTINGS,
                argv=(
                    rclone, "copy", str(directory), f"{destination}/{directory.name}",
                    "--transfers", "8", "--checkers", "16",
                ),
            )
        )
    return PortionPlan(
        portion=backup_facts.Portion.DATABASE, commands=tuple(commands), warnings=uncovered
    )


def _uncovered_analysis_share(cfg: config.Config) -> tuple[Mapping[str, str], ...]:
    """A warning when the analysis share sits where neither portion reaches.

    R-14. The share beside the database holds every beat grid, and the mirror
    carries it only because it normally sits under the library root: the mirror
    excludes the database fileset by name and nothing else. A database outside the
    root is an acknowledged configuration, and in that layout the share is outside
    it too, so the mirror never sees it and the snapshot copies the database file
    alone. A restore from that backup brings back rows without their grids, and
    the rows look fine.

    SAID RATHER THAN CARRIED. Carrying it is a choice with a real cost, the share
    is gigabytes and a dated snapshot copies whole, and it is recorded as a
    residual with its options rather than made here. What is not acceptable is a
    backup that reports complete over the one tree it exists to protect.
    """
    share = analysis_store.share_root(cfg)
    if analysis_store.watch_roots(cfg) == (Path(cfg.library.root),):
        return ()
    return (
        {
            "code": ANALYSIS_SHARE_NOT_CARRIED,
            "message": (
                f"the analysis share {share} sits outside the library root "
                f"{cfg.library.root}, so neither the mirror nor the database "
                f"snapshot carries it. It holds this library's beat grids, and a "
                f"database restored without it brings back every row without its "
                f"analysis"
            ),
        },
    )


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------


def subprocess_runner(command: Command) -> CommandResult:
    """Run one command with the fallback directories on PATH and no credentials."""
    import subprocess

    completed = subprocess.run(
        list(command.argv),
        capture_output=True,
        text=True,
        env=binaries.subprocess_env(),
        check=False,
    )
    return CommandResult(
        returncode=completed.returncode,
        stdout=completed.stdout or "",
        stderr=completed.stderr or "",
    )


def dry_run_argv(command: Command) -> tuple[str, ...]:
    """The same command, made to report instead of transfer.

    Derived from the real command rather than assembled separately, which is the
    whole reason the plan is data: a preview built by a second code path is a
    preview that can be wrong about the run it previews.
    """
    if command.label in TRANSFERRING_LABELS:
        return (*command.argv, "--dry-run")
    return command.argv


def run_backup(
    cfg: config.Config,
    plan: BackupPlan,
    *,
    runner: Runner = subprocess_runner,
    now: datetime | None = None,
    dry_run: bool = False,
    publish: bool = True,
) -> BackupOutcome:
    """Execute a plan and publish the age fact for each portion that completed.

    The fact is published PER PORTION and only on success. A portion that refused
    leaves its previous fact untouched, so the age of the last real database
    snapshot survives every run that skipped it, which is exactly the number R15
    needs to show.

    ``dry_run`` runs THE SAME plan with every transferring command neutralized,
    and publishes nothing: a preview that recorded a backup age would report the
    library as protected by a run that copied not one byte. It reuses the plan
    rather than building a second one, so the preview cannot describe a run
    different from the one that follows it.
    """
    moment = now or datetime.now(timezone.utc)
    outcomes: list[PortionOutcome] = []
    if dry_run:
        publish = False

    for entry in plan.portions:
        if entry.refusal is not None:
            outcomes.append(
                PortionOutcome(
                    portion=entry.portion,
                    ran=False,
                    refusal=entry.refusal,
                    detail=entry.detail,
                    warnings=entry.warnings,
                )
            )
            continue

        results: list[CommandResult] = []
        warnings: list[Mapping[str, str]] = list(entry.warnings)
        failed: CommandResult | None = None
        for command in entry.commands:
            if command.label == PRUNE_ARCHIVE:
                # THE ONE CLASS THIS LOOP DOES NOT FAIL ON, AND NO LONGER STAYS
                # SILENT ABOUT. ``_prune_archive`` argues at length why a failed
                # rotation must not fail a portion whose mirror completed. That
                # argument is about the VERDICT and says nothing about the
                # report, and for as long as nothing reported it a person whose
                # remote refused ``lsf`` accumulated dated folders with no
                # signal. The classification comes back from the function that
                # already reads the listing's return code, rather than being
                # re-derived here from a position in a returned list.
                #
                # Listing is safe; purging is not, so a preview is the same call
                # with the purge suppressed rather than a second path through
                # the same command. A rehearsal therefore reports a failed
                # listing exactly as a real run does, which the branch this
                # replaced could not: it ran the listing and read nothing.
                pruned, warning = _prune_archive(
                    cfg,
                    command,
                    runner=runner,
                    keep=plan.archive_keep,
                    purge=not dry_run,
                )
                results += pruned
                if warning is not None:
                    warnings.append(warning)
                continue
            if dry_run:
                command = Command(label=command.label, argv=dry_run_argv(command))
            result = runner(command)
            results.append(result)
            if result.returncode != 0:
                failed = result
                break

        if failed is not None:
            outcomes.append(
                PortionOutcome(
                    portion=entry.portion,
                    ran=False,
                    detail=f"{entry.portion.value} portion failed: {failed.stderr.strip()[-400:]}",
                    results=tuple(results),
                    warnings=tuple(warnings),
                )
            )
            continue

        if publish:
            backup_facts.record(
                cfg,
                entry.portion,
                completed_at=moment,
                destination=_destination_for(cfg, entry.portion),
            )
        outcomes.append(
            PortionOutcome(
                portion=entry.portion,
                ran=True,
                results=tuple(results),
                warnings=tuple(warnings),
            )
        )

    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes))


def _destination_for(cfg: config.Config, portion: backup_facts.Portion) -> str:
    if portion is backup_facts.Portion.DATABASE:
        return str(cfg.backup.db_dest_root or "")
    return str(cfg.backup.dest or "")


def _prune_archive(
    cfg: config.Config,
    listing: Command,
    *,
    runner: Runner,
    keep: int,
    purge: bool = True,
) -> tuple[list[CommandResult], Mapping[str, str] | None]:
    """Remove all but the newest ``keep`` dated archive folders, and say so.

    Runs only after the mirror in the same portion succeeded, because each dated
    folder holds the pre-overwrite versions from one run: pruning before the new
    folder exists would leave a window with no rollback at all.

    A failed listing prunes nothing. Deleting on a partial listing is how a
    prune removes the only archive there is.

    A failed PURGE does not fail the portion either. By the time it runs the
    mirror has already completed, so the backup the user asked for exists; what
    is left over is a stale folder using space, which is a smaller problem than
    reporting a completed backup as failed and having the user run the whole
    transfer again.

    NEITHER FAILURE IS SILENT, and this function is where that is decided
    because it is the only place that knows which result is the listing and
    which are purges. It returns its results AND at most one warning, so a
    caller reports the condition without re-reading a return code this function
    already read or identifying the listing by its position in the list. The
    warning is at most one because the two conditions cannot co-occur: a listing
    that failed purged nothing.

    ``purge`` is the rehearsal seam. False lists and deletes nothing, which is
    what a preview owes a user; it defaults to True so a caller that says
    nothing gets the real rotation rather than a silent no-op.
    """
    out: list[CommandResult] = []
    result = runner(listing)
    out.append(result)
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
            "message": (
                f"the archive rotation did not run: listing "
                f"{cfg.backup.archive_root}/ exited {result.returncode}, so "
                f"nothing was removed and dated archive folders will accumulate "
                f"until it succeeds. The backup itself completed"
            ),
        }
    if keep < 0 or not purge:
        return out, None
    names = sorted(line.strip().rstrip("/") for line in result.stdout.splitlines() if line.strip())
    unremoved = 0
    for stale in names[: max(0, len(names) - keep)]:
        purged = runner(
            Command(
                label=PRUNE_ARCHIVE_FOLDER,
                # The SAME rclone the listing used, taken from its own argv
                # rather than resolved a second time: two resolutions inside
                # one run can disagree if PATH changes underneath, and the
                # one that deletes is not the one to leave to chance.
                argv=(listing.argv[0], "purge", f"{cfg.backup.archive_root}/{stale}"),
            )
        )
        out.append(purged)
        if purged.returncode != 0:
            unremoved += 1
    if unremoved:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
            "message": (
                f"the archive rotation did not finish: {unremoved} dated folder(s) "
                f"under {cfg.backup.archive_root}/ could not be removed and will "
                f"use remote space until a later run removes them. The backup "
                f"itself completed"
            ),
        }
    return out, None


# ---------------------------------------------------------------------------
# Restore
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RestorePlan:
    """What a restore will do, including the sidecars it clears first."""

    target: Path
    database_target: Path
    snapshot: str | None
    clears: tuple[Path, ...]
    commands: tuple[Command, ...] = field(default_factory=tuple)


def database_target_for(cfg: config.Config, target: Path) -> Path:
    """Where the database lands under an arbitrary restore target.

    Re-based from the CONFIGURED database path relative to the library root,
    never from an assumed vendor layout. The source system composes
    ``<target>/PIONEER/Master/master.db``, which is right for one installation and
    silently wrong for a user who moved their database, restoring it to a path
    rekordbox does not read.
    """
    database = config.state_path("rekordbox_db", cfg)
    try:
        return target / database.relative_to(cfg.library.root)
    except ValueError:
        # An acknowledged database outside the library root has no position
        # relative to it, so the only honest answer is its own name at the top of
        # the target.
        return target / database.name


def latest_snapshot(cfg: config.Config, *, runner: Runner) -> str | None:
    """The newest dated database snapshot on the remote, or None.

    Newest by NAME, which is sound only because ``stamp_for`` writes a sortable
    UTC stamp. That coupling is stated here because it is the kind that breaks
    quietly: a local-time stamp would sort wrongly for one hour a year and this
    would restore the second-newest snapshot without saying so.
    """
    result = runner(
        Command(
            label=LIST_SNAPSHOTS,
            argv=(_rclone(), "lsf", f"{cfg.backup.db_dest_root}/", "--dirs-only"),
        )
    )
    if result.returncode != 0:
        return None
    names = sorted(line.strip().rstrip("/") for line in result.stdout.splitlines() if line.strip())
    return names[-1] if names else None


def plan_restore(
    cfg: config.Config,
    *,
    target: Path | str,
    confirmed: bool,
    snapshot: str | None = None,
    include_mirror: bool = False,
    runner: Runner = subprocess_runner,
    process_lister: ProcessLister | None = None,
    gates: GateGuard | None = None,
) -> RestorePlan:
    """Decide a restore. Refuses rather than prompting (R33), and behind the gates.

    ``confirmed`` is a NAMED DECISION the caller passes, not a question this asks.
    A restore overwrites a live database, and the source system gates it on a
    blocking read from standard input, which cannot be answered by a detached job
    and cannot be recorded as having been answered by anyone.

    ``include_mirror`` adds the file half: the music and everything else the
    mirror carried. It is off by default because the two halves have very
    different costs and are wanted at different times. Recovering from a bad
    write means the database alone; recovering from a dead drive means both, and
    the second is hundreds of gigabytes.

    THE MIRROR IS PULLED WITH A COPY, NEVER A SYNC. A sync would make the target
    match the remote by DELETING anything the remote does not have, and the
    target of a restore is frequently a partially-recovered volume holding files
    the user salvaged by other means. Copy adds and overwrites; it never removes.

    THE GATES COME BEFORE EVERY CHECK BUT ONE, and the exception is deliberate.
    ``_require_destinations`` reads configuration, resolves no path and touches
    no volume, so running it first costs nothing and gives a user with an
    unconfigured remote the message that actually applies to them. Everything
    after that point resolves paths on the library volume, and a destructive
    session must refuse before it resolves a single path: resolving against the
    wrong volume is already the damage.

    THE EXISTING REFUSALS STAY. The gates are added to them rather than replacing
    them; an unconfirmed decision and a live rekordbox process are still refused
    here and are still refused in this module's own vocabulary.
    """
    _require_destinations(cfg)
    with _restore_gates(cfg, gates):
        return _plan_restore_inside_the_gates(
            cfg,
            target=Path(target),
            confirmed=confirmed,
            snapshot=snapshot,
            include_mirror=include_mirror,
            runner=runner,
            process_lister=process_lister,
        )


def _plan_restore_inside_the_gates(
    cfg: config.Config,
    *,
    target: Path,
    confirmed: bool,
    snapshot: str | None,
    include_mirror: bool,
    runner: Runner,
    process_lister: ProcessLister | None,
) -> RestorePlan:
    """The planning body, split out so the gate wraps it as one block.

    A separate function rather than an indented body, because the alternative is
    re-indenting a hundred lines every time the guard changes shape, and a diff
    that moves every line is a diff nobody reads.
    """
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
            "a restore replaces the live database and is not performed without an "
            "explicit decision naming this library and this snapshot.",
        )
    if not target.is_dir():
        raise BackupRefused(
            Refusal.RESTORE_TARGET_ABSENT,
            f"the restore target {target} does not exist; create or mount it first",
        )
    running = rekordbox_processes_running(lister=process_lister)
    if running:
        raise BackupRefused(
            Refusal.REKORDBOX_RUNNING,
            f"{', '.join(running)} is running. Restoring underneath a live "
            f"rekordbox replaces the file it holds open, which leaves the "
            f"application and the disk describing two different libraries.",
        )

    chosen = snapshot or latest_snapshot(cfg, runner=runner)
    if not chosen:
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"no dated database snapshot was found under {cfg.backup.db_dest_root}",
        )

    database_target = database_target_for(cfg, target)
    # THE SIDECARS ARE CLEARED BEFORE ANYTHING IS COPIED. A stale write-ahead log
    # beside a freshly restored database belongs to the database that was just
    # replaced, and SQLite will happily replay it onto the new file, corrupting
    # it in a way that opens without complaint. Suffixes come from the state
    # inventory so this cannot drift from the capture side.
    clears = tuple(
        database_target.with_name(database_target.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    rclone = _rclone()
    base = f"{cfg.backup.db_dest_root}/{chosen}/db"
    commands = []
    if include_mirror:
        commands.append(
            Command(
                label=RESTORE_MIRROR,
                argv=(
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(VOLUME_EXCLUDES),
                    "--transfers", "8", "--checkers", "16",
                ),
            )
        )
    commands.append(
        Command(
            label=RESTORE_DATABASE,
            argv=(rclone, "copy", f"{base}/{database_target.name}", f"{database_target.parent}/"),
        )
    )
    # Only the sidecars a restore writes BACK. The shared-memory index is derived
    # from the log, so putting a stale one back beside a fresh log hands SQLite
    # two disagreeing views of one database; the declaration says which.
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if sidecar.restored:
            commands.append(
                Command(
                    label=RESTORE_DATABASE,
                    argv=(
                        rclone,
                        "copy",
                        f"{base}/{database_target.name}{sidecar.suffix}",
                        f"{database_target.parent}/",
                    ),
                )
            )
    return RestorePlan(
        target=target,
        database_target=database_target,
        snapshot=chosen,
        clears=clears,
        commands=tuple(commands),
    )


def run_restore(
    plan: RestorePlan,
    cfg: config.Config,
    *,
    runner: Runner = subprocess_runner,
    dry_run: bool = False,
    gates: GateGuard | None = None,
) -> tuple[CommandResult, ...]:
    """Clear the stale sidecars, then copy. In that order, always.

    The order is the entire safety property, so it is one function rather than
    two the caller sequences: a caller that copied first and cleared afterwards
    would have already handed SQLite a database and a log that disagree.

    The sidecars are cleared before ANY command, including the file mirror. The
    mirror never carried them, so clearing first costs nothing and keeps the
    invariant at its strongest: at no point during a restore does a stale log sit
    beside a database that has started to change.

    ``dry_run`` neutralizes the transfer AND skips the clearing, which is the
    part worth stating. Deleting the live sidecars is itself destructive, so a
    rehearsal that cleared them and then transferred nothing would leave the
    user's database without the log it needs: a "preview" that did the damage
    and skipped the repair.

    A DRY RUN IS NOT EXEMPT FROM THE GATES, and that is a decision rather than an
    oversight. Three reasons, in order of weight. The lock is the one that
    matters: a rehearsal that runs while another destructive session is writing
    describes a library that is changing underneath it, so its preview is a
    report about a world that no longer exists, which is worse than no preview.
    Second, the whole reason the plan and the run are one pair of functions is
    that a preview built by a second code path can be wrong about the run it
    previews, and a preview that skipped a guard the run does not skip is exactly
    that divergence wearing a different hat. Third, a rehearsal that passes is
    then evidence the real run will reach its work, which is most of what a
    person rehearses for. The cost is one acknowledgment, which they need
    anyway.

    ``cfg`` is required rather than optional, so there is no call shape that
    reaches the destructive half with nothing to resolve the gates against.
    """
    with _restore_gates(cfg, gates):
        if dry_run:
            # THE REHEARSAL'S RESULTS ARE READ TOO, and this branch had the same
            # defect the real one did. It is not a lesser case: the whole reason
            # a rehearsal is worth running is the claim above, that one which
            # passes is evidence the real run will reach its work, and that claim
            # is false the moment a failing preview reports as a passing one.
            return _ran(
                tuple(
                    runner(Command(label=c.label, argv=dry_run_argv(c)))
                    for c in plan.commands
                ),
                plan,
            )
        plan.database_target.parent.mkdir(parents=True, exist_ok=True)
        for stale in plan.clears:
            stale.unlink(missing_ok=True)
        return _ran(tuple(runner(command) for command in plan.commands), plan)


def _ran(results: tuple[CommandResult, ...], plan: RestorePlan) -> tuple[CommandResult, ...]:
    """Every transfer's return code, READ. Raises on the first one that failed.

    THIS FUNCTION IS A BLOCKING DEFECT'S FIX AND THE DEFECT WAS SILENCE. The
    results were returned unread, so a restore whose every copy failed came back
    as an ordinary tuple and the caller reported a success. That is not a
    cosmetic misreport, because the sidecars are cleared BEFORE the first
    command: measured on 2026-08-23 by driving a runner that answers the listing
    and fails the copy, the live write-ahead log was deleted, the database was
    unchanged, and the verb exited OK saying two transfers had happened. The log
    holds transactions committed since the last checkpoint, which are in no
    capture by construction, so the one report a person acts on said their
    library was restored at the moment it had silently lost work.

    RAISES RATHER THAN REPORTING A PARTIAL RUN, which is the difference between
    this function and :func:`run_backup`'s per portion accounting one file over.
    A backup that copied three of four portions has still improved the world and
    the outcome says which. A restore that copied some of a database and its
    companions has produced a set that matches nothing, and there is no shape of
    "partly restored" a caller can do anything useful with.

    THE SIDECARS ARE NOT PUT BACK, and the refusal says so rather than pretending
    otherwise. Clearing them first is the safety property the ordering exists for
    (a stale log replayed onto a replaced database corrupts it in a way that
    opens without complaint), so the honest answer to a failed transfer is a loud
    refusal naming what was cleared, not a silent repair this module cannot make.
    """
    # STRICT, because both callers build the results by walking ``plan.commands``
    # exactly once, so a length that differs is a driver defect rather than a
    # short list to be tolerated, and tolerating it would skip the tail unread.
    for command, result in zip(plan.commands, results, strict=True):
        if result.returncode != 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
                f"the transfer {command.label!r} exited {result.returncode} and the "
                f"restore did not complete. The live companion files beside "
                f"{plan.database_target.name} were cleared before it began and have "
                f"not been put back, so run the restore again once the remote is "
                f"reachable rather than opening the library first.",
            )
    return results


# ---------------------------------------------------------------------------
# Structured output (R32)
# ---------------------------------------------------------------------------

PAYLOAD_VERSION = 1


def plan_payload(plan: BackupPlan) -> dict:
    """A plan as plain data. Human rendering stays with the CLI."""
    return {
        "payload_version": PAYLOAD_VERSION,
        "stamp": plan.stamp,
        "portions": [
            {
                "portion": entry.portion.value,
                "will_run": entry.will_run,
                "refusal": entry.refusal.value if entry.refusal else None,
                "detail": entry.detail,
                "commands": [
                    {"label": c.label, "argv": list(c.argv)} for c in entry.commands
                ],
                "warnings": [dict(warning) for warning in entry.warnings],
            }
            for entry in plan.portions
        ],
    }


def outcome_payload(outcome: BackupOutcome) -> dict:
    """Render the outcome. A RENDERER: nothing here interprets a return code.

    ``warnings`` is rendered rather than derived. The condition it reports is
    read once, in ``_prune_archive``, and carried out on the portion; deriving
    it here instead would put the reading in a function whose whole contract is
    serialization, where a caller reporting the outcome any other way would
    lose it.

    ``PAYLOAD_VERSION`` is NOT bumped for this key. The rule is stated at
    ``modules.tools.setbuilder.PAYLOAD_VERSION``: bumped when a field is removed
    or its meaning changes, so a consumer can refuse rather than silently read a
    field that now means something else. A field that joins takes nothing away
    from a consumer that does not read it.
    """
    return {
        "payload_version": PAYLOAD_VERSION,
        "stamp": outcome.stamp,
        "ok": outcome.ok,
        "portions": [
            {
                "portion": entry.portion.value,
                "ran": entry.ran,
                "refusal": entry.refusal.value if entry.refusal else None,
                "detail": entry.detail,
                "warnings": [dict(warning) for warning in entry.warnings],
            }
            for entry in outcome.portions
        ],
    }


__all__ = [
    "DEFAULT_ARCHIVE_KEEP",
    "PAYLOAD_VERSION",
    "REFUSALS",
    "REKORDBOX_PROCESSES",
    "RESTORE_WORKFLOW",
    "VOLUME_EXCLUDES",
    "BackupOutcome",
    "GateGuard",
    "BackupPlan",
    "BackupRefused",
    "Command",
    "CommandResult",
    "PortionOutcome",
    "PortionPlan",
    "Refusal",
    "RESTORE_MIRROR",
    "RestorePlan",
    "database_fileset",
    "database_target_for",
    "dry_run_argv",
    "latest_snapshot",
    "plan_backup",
    "plan_payload",
    "plan_restore",
    "outcome_payload",
    "rekordbox_processes_running",
    "run_backup",
    "run_restore",
    "running_process_names",
    "settings_directories",
    "stamp_for",
    "subprocess_runner",
]
