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

THE ANALYSIS SHARE travels with whichever half reaches it (R-338). Under the
library root it is in the mirror. Beside a database that sits outside the root,
which is rekordbox's own default, the mirror never sees it, so the database
portion mirrors it to its own stable destination, behind the same gate, because
rekordbox writes the share while it analyses. This module READS analysis files
and hands them to rclone. It never opens, authors or edits one.

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

import re
import sys
from collections.abc import Callable, Mapping, Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path

from cratekit.core import analysis_store, backup_facts, binaries, config, preflight, session
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
SNAPSHOT_IDENTITY = "snapshot-identity"
SNAPSHOT_SHARE = "snapshot-share"
RESTORE_MIRROR = "restore-mirror"
RESTORE_DATABASE = "restore-database"
RESTORE_SHARE = "restore-share"
LIST_SNAPSHOTS = "list-snapshots"
LIST_SNAPSHOT_CONTENTS = "list-snapshot-contents"
LIST_SNAPSHOT_IDENTITY = "list-snapshot-identity"
LIST_SHARE = "list-share"

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

#: The warning code for an outside layout whose analysis share is not a
#: directory, so the database portion has nothing to carry (R-338). Not a refusal
#: for the same reason as the two above: the database portion still runs and
#: still protects the database. It is said because "there was no share to copy"
#: and "the share was copied" are different facts, and only one of them means the
#: grids are in a backup.
ANALYSIS_SHARE_ABSENT = "analysis-share-absent"

#: Where an outside share is mirrored, under the configured snapshot root. NOT
#: STAMP SHAPED, so :func:`_snapshot_names` never offers it as a snapshot.
#:
#: A STABLE MIRROR AND NOT A COPY INSIDE EACH DATED SNAPSHOT (R-338). Dated
#: snapshots are never rotated and copy whole, so a share of a few gigabytes
#: inside each one fills a consumer quota within a handful of runs, after which
#: the backup itself fails. A mirror costs the share once, and its dated archive
#: keeps one run undoable, which is what the library mirror already gives a share
#: that sits under the root.
SHARE_DEST_DIRNAME = "analysis-share"

#: The mirror's folder for a library with no identity a path can carry. The
#: leading underscore is what no real identity can start with
#: (``_MARKER_IDENTITY``), so it cannot collide with one.
SHARE_UNRECORDED = "_unrecorded"

#: rclone's documented exit for a directory that does not exist. Measured on
#: 2026-09-20 with ``rclone lsf`` over a missing local directory: exit 3, and
#: ONLY ON THE LOCAL BACKEND. No remote was driven, which is an attended act.
RCLONE_DIRECTORY_NOT_FOUND = 3

#: Labels whose command TRANSFERS data, so a dry run must neutralize them.
#: Derived membership, checked by a test, so a transferring command added later
#: cannot quietly become one the preview would really execute.
TRANSFERRING_LABELS: frozenset[str] = frozenset(
    {
        MIRROR,
        SNAPSHOT_DATABASE,
        SNAPSHOT_SETTINGS,
        SNAPSHOT_IDENTITY,
        SNAPSHOT_SHARE,
        RESTORE_MIRROR,
        RESTORE_DATABASE,
        RESTORE_SHARE,
    }
)

#: The capture could not say which library a snapshot belongs to, so it wrote no
#: marker. A warning rather than a refusal: the database copy is still worth
#: having, and what is lost is that the newest-by-default restore will ask for
#: this snapshot to be named.
SNAPSHOT_IDENTITY_NOT_WRITTEN = "snapshot-identity-not-written"

#: What a snapshot's identity marker is called, up to the identity itself. The
#: marker is an EMPTY file whose name carries the value, beside ``db/`` in the
#: dated folder and never inside it, so the database set a restore copies from
#: holds the database set and nothing else.
IDENTITY_MARKER_PREFIX = "library-volume."

#: How many dated archive folders survive a prune. One is a single run's
#: rollback, which is what the source keeps and what a consumer cloud quota
#: tolerates. It is a parameter everywhere below so a user with room can keep
#: more; what is NOT negotiable is that pruning happens only after the mirror
#: succeeds, so a failed run never touches the safety net.
#:
#: THE NEWEST SLOT IS A RUN, NOT AN ATTEMPT. Every attempt at the mirror stamps
#: its own dated folder, so a mirror that failed partway and was retried to
#: success leaves two, and the first holds the only copies of what that attempt
#: overwrote. :func:`_prune_archive` holds every folder written since the last
#: COMPLETED mirror as one slot of this number. Only that newest slot is grouped:
#: once a run is settled its folders are counted one by one again, which costs
#: nothing at the one value any verb passes and is recorded as a residual for a
#: wider keep.
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
    # R-154. Three diagnoses with three different acts behind them: retype the
    # stamp, pick a snapshot that is this library's or say which volume it was
    # taken from, and name a snapshot that predates the identity marker.
    SNAPSHOT_NAME_INVALID = "snapshot-name-invalid"
    SNAPSHOT_LIBRARY_MISMATCH = "snapshot-library-mismatch"
    SNAPSHOT_IDENTITY_UNRECORDED = "snapshot-identity-unrecorded"


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
    """What one run of a plan did, INCLUDING which kind of run it was.

    ``dry_run`` is on the outcome and not left to whoever called
    :func:`run_backup` to remember, because a rehearsal and a real run are
    otherwise indistinguishable here: both list the same portions with ``ran``
    true, and only one of them copied anything or published an age. Every
    renderer of an outcome would then need the flag handed to it separately, and
    R-221 is what happens when one of them is not: the queued backup's envelope
    reported a rehearsal's ages, which are the PREVIOUS real run's and therefore
    true, with nothing saying this run copied nothing.

    It records the run rather than the request. :func:`run_backup` sets it from
    the value it actually executed under, which is the same value that decided
    whether anything was published, so the outcome cannot say one thing while the
    fact file says the other.
    """

    stamp: str
    portions: tuple[PortionOutcome, ...]
    dry_run: bool = False

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
    return now.astimezone(timezone.utc).strftime(_STAMP_FORMAT)


_STAMP_FORMAT = "%Y-%m-%dT%H%M%SZ"
_STAMP_SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{6}Z")
#: What a refusal shows a person who typed something else. A literal rather than
#: a computed value, and a test holds it to :func:`is_stamp`, so it cannot drift
#: from the format while staying out of the way of the format's own callers.
STAMP_EXAMPLE = "2026-01-31T235959Z"


def is_stamp(value: str) -> bool:
    """Whether ``value`` is a folder name :func:`stamp_for` could have written.

    THE SHAPE AND THE CALENDAR, both. The pattern alone admits a thirteenth
    month, and the parse alone admits whatever padding the platform's parser is
    lenient about, so neither is trusted by itself. What this buys is that a
    value reaching a remote path is a name and never a path: no separator, no
    dot segment and no whitespace survives it (R-154).
    """
    if not _STAMP_SHAPE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, _STAMP_FORMAT)
    except ValueError:
        return False
    return True


#: The source system's dated folder, local time with an underscore. It writes
#: the same ``<root>/<name>/db/`` layout this product reads, commonly into the
#: same remote directory, so on the day of a cutover every snapshot a person
#: owns is spelled this way and a restore that refused the spelling would have
#: nothing to pull (found by the built in review of the shape check).
_LEGACY_FORMAT = "%Y-%m-%d_%H%M%S"
_LEGACY_SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}")


def is_snapshot_name(value: str) -> bool:
    """Whether ``value`` names a dated snapshot folder, this product's or the source's.

    WIDER THAN :func:`is_stamp` AND EXACTLY AS SAFE. What the check is for is
    that a value reaching a remote path is a NAME, and both spellings are digits
    and one separator character with a real date behind them. ``is_stamp`` stays
    the narrow statement of what a backup WRITES, which is what the test holding
    the two ends together compares against.

    The two spellings sort together as text, and across them the order is only
    roughly by time: one is UTC and one is local, and on a shared date the
    underscore sorts after the letter. That is tolerable because a source system
    snapshot never carries a marker, so the newest-by-default walk steps over
    it and it is pulled only by name.
    """
    if is_stamp(value):
        return True
    if not _LEGACY_SHAPE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, _LEGACY_FORMAT)
    except ValueError:
        return False
    return True


_MARKER_IDENTITY = re.compile(r"[0-9a-z][0-9a-z_-]*(?:\.[0-9a-z_-]+)*")


def identity_marker(identity: str | None) -> str | None:
    """The marker filename for one volume identity, or None when it has none.

    NORMALIZED BEFORE IT IS WRITTEN, which is the opposite of what setup does
    with the configured value and for a different reason. The configured
    identity is matched exactly elsewhere, so it is recorded as typed (R-344).
    A marker is only ever compared through ``preflight.normalize_identity``, so
    one spelling on the remote is strictly simpler than two.

    None FOR ANYTHING THAT IS NOT PLAINLY A NAME. Both shipped adapters report
    hex and hyphens. A value carrying a separator, a space or a leading dot did
    not come from one of them, and interpolating it would write the marker
    somewhere other than the dated folder.
    """
    if identity is None:
        return None
    folded = preflight.normalize_identity(identity)
    if not _MARKER_IDENTITY.fullmatch(folded):
        return None
    return IDENTITY_MARKER_PREFIX + folded


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
        detail=_rotation_detail(archive_keep),
    )


def _rotation_detail(archive_keep: int) -> str:
    """What the plan says the rotation will keep, in the three cases it has.

    Three sentences because :func:`_prune_archive` has three behaviours, and a
    preview that described the held run at a keep of zero would promise a
    retention the run does not apply.
    """
    if archive_keep < 0:
        return "keeping every dated archive folder"
    if archive_keep == 0:
        return "keeping no dated archive folder"
    return (
        f"keeping the newest {archive_keep} dated archive folder(s), and "
        f"counting every folder written since the last completed mirror as "
        f"one of them"
    )


def _plan_database(
    cfg: config.Config,
    *,
    rclone: str,
    stamp: str,
    process_lister: ProcessLister | None,
    settings_dirs: Sequence[Path] | None,
) -> PortionPlan:
    uncovered = absent_analysis_share(cfg)
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
    # THE MARKER FOLLOWS THE WHOLE DATABASE SET AND PRECEDES THE SETTINGS. It
    # says "the database in this folder is this library's", so it must not exist
    # beside a copy that failed, and the executor stops at the first failing
    # command. It does not wait for the settings, because a snapshot whose
    # settings copy failed still holds a database a restore can use (R-154).
    warnings = [*uncovered, *snapshot_identity_warning(cfg)]
    marker = identity_marker(cfg.library.volume_id)
    if marker is not None:
        commands.append(
            Command(
                label=SNAPSHOT_IDENTITY,
                argv=(rclone, "touch", f"{destination}/{marker}"),
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
    # THE SHARE GOES LAST, AND IN THIS PORTION (R-338). In this portion because
    # rekordbox writes the share while it analyses, so it needs the gate that was
    # passed above and the mirror does not have. Last because it is gigabytes and
    # the executor stops at the first failing command: a share that fails after
    # the settings costs the settings nothing. It still FAILS the portion, so no
    # database age is published over a library whose grids did not copy.
    share = _outside_share(cfg)
    if share is not None and share.is_dir():
        kept = share_destination(cfg, identity=cfg.library.volume_id)
        commands.append(
            Command(
                label=SNAPSHOT_SHARE,
                argv=(
                    rclone, "sync", str(share), f"{kept}/current",
                    *_exclude_args(VOLUME_EXCLUDES),
                    # The mirror's own rule: what this sync would overwrite or
                    # delete moves to a dated folder first, so a share emptied by
                    # a reinstall does not empty its only copy.
                    "--backup-dir", f"{kept}/archive/{stamp}",
                    "--transfers", "8", "--checkers", "16",
                ),
            )
        )
    return PortionPlan(
        portion=backup_facts.Portion.DATABASE,
        commands=tuple(commands),
        warnings=tuple(warnings),
    )


def snapshot_identity_warning(cfg: config.Config) -> tuple[Mapping[str, str], ...]:
    """A warning when this configuration's snapshots cannot say whose they are.

    PUBLIC, AND ASKED OF THE CONFIGURATION, for the reason
    :func:`absent_analysis_share` is: the backup verb runs through the job
    queue, a claimed item's report does not reach the person, and a warning that
    rides only on the plan therefore reaches nobody. Every backup would write an
    unmarked snapshot in silence, and the first word of it would be a restore
    refusing on the day it was needed.
    """
    if identity_marker(cfg.library.volume_id) is not None:
        return ()
    why = "not recorded" if cfg.library.volume_id is None else "not a plain name"
    return (
        {
            "code": SNAPSHOT_IDENTITY_NOT_WRITTEN,
            "message": (
                f"this snapshot will not say which library it was taken from, "
                f"because {config.VOLUME_IDENTITY_KEY} is {why}. A restore will "
                f"pull it only when its stamp is named"
            ),
        },
    )


def _outside_share(cfg: config.Config) -> Path | None:
    """The analysis share when the mirror does NOT reach it, else None.

    Asked through ``analysis_store.watch_roots`` rather than re-derived, so the
    backup and the analysis watch cannot disagree about which layout this is.
    """
    if analysis_store.watch_roots(cfg) == (Path(cfg.library.root),):
        return None
    return analysis_store.share_root(cfg)


def share_destination(cfg: config.Config, *, identity: str | None) -> str:
    """Where one library's outside share is mirrored on the remote.

    KEYED BY THE VOLUME IDENTITY, for the reason the snapshot marker exists
    (R-154): two libraries can share one snapshot root, and a sync makes its
    destination match its source, so under one unkeyed folder each library's
    backup would archive the other's grids and a restore would pull whichever
    ran last. The key passes through :func:`identity_marker`, so a value that is
    not plainly a name is never interpolated into a path.
    """
    marker = identity_marker(identity)
    key = SHARE_UNRECORDED if marker is None else marker[len(IDENTITY_MARKER_PREFIX):]
    return f"{cfg.backup.db_dest_root}/{SHARE_DEST_DIRNAME}/{key}"


def absent_analysis_share(cfg: config.Config) -> tuple[Mapping[str, str], ...]:
    """A warning when an outside analysis share is not there to be carried.

    R-338. The share beside the database holds every beat grid. Under the library
    root the mirror carries it. Outside the root, which is an acknowledged
    configuration and rekordbox's own default, the database portion mirrors it
    (see ``SHARE_DEST_DIRNAME``). What is left to say is the one case where that
    command is not planned: no directory at the path the database implies. That
    is normal for a library nothing has analysed, and it is also what a wrong
    ``db_path`` looks like, so it is said rather than folded into "carried".

    PUBLIC, AND ASKED OF THE CONFIGURATION, because the backup verb runs through
    the job queue, a claimed item's report does not reach the person, and a
    warning that rides only on the plan therefore reaches nobody.
    """
    share = _outside_share(cfg)
    if share is None or share.is_dir():
        return ()
    return (
        {
            "code": ANALYSIS_SHARE_ABSENT,
            "message": (
                f"the analysis share {share} sits outside the library root "
                f"{cfg.library.root} and is not a directory, so this backup "
                f"carries no beat grids or analysis. That is expected only for a "
                f"library rekordbox has not analysed yet"
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
            if result.returncode != 0 and command.label == SNAPSHOT_IDENTITY:
                # THE SECOND CLASS THIS LOOP DOES NOT FAIL ON. By the time the
                # marker is attempted the whole database set has copied, and
                # that copy is what the portion is for. Failing here would skip
                # the settings, publish no age, and report a failed backup over
                # a remote holding a good one, on every run, for a remote that
                # cannot hold an empty file. What is lost is said instead: the
                # snapshot is unmarked, and a restore pulls it only by name.
                warnings.append(
                    {
                        "code": SNAPSHOT_IDENTITY_NOT_WRITTEN,
                        "message": (
                            f"the database was copied and the marker saying which "
                            f"library it was taken from could not be written "
                            f"(exit {result.returncode}). A restore will pull this "
                            f"snapshot only when its stamp is named"
                        ),
                    }
                )
                continue
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

    # ``dry_run`` RATHER THAN ``not publish``, and the two are not the same
    # question. A caller can ask a real run to publish nothing, and that run
    # still copied the library; a rehearsal is the one that did not. The flag
    # recorded is the one this body branched its neutralisation on.
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=dry_run)


def _destination_for(cfg: config.Config, portion: backup_facts.Portion) -> str:
    if portion is backup_facts.Portion.DATABASE:
        return str(cfg.backup.db_dest_root or "")
    return str(cfg.backup.dest or "")


def _rotation_floor(cfg: config.Config) -> str | None:
    """The stamp of the last COMPLETED mirror to this destination, or None.

    A dated folder named after this belongs to the run now finishing, whichever
    attempt wrote it, and one at or before it belongs to a run that is over.
    That is what lets the rotation count runs rather than attempts (R-222)
    without a record of attempts: the age fact is already published only on
    success and only after the prune, so at prune time it names the previous
    completed run and nothing later.

    NONE IS NOT "NOTHING TO HOLD". It is "no completed mirror to THIS destination
    is on record", which is a first backup onto a remote something else already
    mirrored to, a first attempt that failed, or a reconfigured destination. No
    folder can be called settled then, and the caller purges none.

    A FILE THAT CANNOT BE READ RAISES, and is neither of the answers above. The
    publish a few lines after the prune reads the same file through the same
    reader and would raise the same exception, so nothing reachable changes
    except that the purge, the one command here that deletes, does not run on a
    record nobody could read.

    AS A STAMP AND NOT AS A TIME, because the folders are compared by name, which
    is how the rotation has always ordered them and the only ordering a folder
    the source system wrote can join. A record from a clock running ahead sorts
    after every folder, so nothing is held and the rotation is exactly what it
    was before this rule: the kept set is never smaller than it used to be.
    """
    fact = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return None
    return stamp_for(fact.completed_at)


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

    THE FLOOR IS WHAT MAKES A SLOT A RUN (R-222), and :func:`_rotation_floor` is
    where it comes from. Every folder named after it was written by an attempt at
    the run now finishing, so they are HELD together as one slot, and the rest of
    ``keep`` is spent on the settled folders, newest first. No floor holds
    everything. The held names are the top of the sort order, so whatever this
    keeps includes what counting attempts kept. A ``keep`` of zero is the one
    case nothing is held: it asks for no archive at all, and holding a run
    against it would overrule that.

    IT IS READ HERE, AFTER THE MIRROR, BEFORE THE PUBLISH, AND ONLY TO DELETE.
    The position is the mechanism: this portion's own age is published by the
    caller once every command has returned, so the record still names the run
    BEFORE this one. And it sits below the rehearsal's return, so a preview
    never opens a file it has no use for, and ``purge`` stays the one thing
    standing between a rehearsal and a deletion rather than one of two.
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
    floor = _rotation_floor(cfg)
    names = sorted(line.strip().rstrip("/") for line in result.stdout.splitlines() if line.strip())
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
    settled = names[: len(names) - len(held)]
    slots = keep - 1 if held else keep
    unremoved = 0
    for stale in settled[: max(0, len(settled) - slots)]:
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
    """What a restore will do, including the sidecars it clears first.

    ``absent_sidecars`` are the suffixes the inventory says to write back that
    this snapshot does not hold. A checkpointed database has no write ahead log,
    and the snapshot verb copies a sidecar only when it is present, so a restore
    that always copies the log is a restore that always fails against the only
    kind of snapshot this product takes (R-367). They are named rather than
    transferred, so a person is told the sidecar was absent, not that it arrived.
    """

    target: Path
    database_target: Path
    snapshot: str | None
    clears: tuple[Path, ...]
    commands: tuple[Command, ...] = field(default_factory=tuple)
    absent_sidecars: tuple[str, ...] = field(default_factory=tuple)
    #: The identity the snapshot's own marker records, normalized, or None for a
    #: snapshot that carries no marker and was pulled because it was named.
    recorded_volume: str | None = None
    #: True when the analysis share sits outside the library root and the remote
    #: holds no mirror of it, so this restore brings back rows without their
    #: grids. Named rather than transferred, as ``absent_sidecars`` is. Always
    #: False for a share under the root, which the mirror half carries.
    share_absent: bool = False


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
    names = _snapshot_names(cfg, runner=runner)
    return names[-1] if names else None


def _snapshot_names(cfg: config.Config, *, runner: Runner) -> tuple[str, ...] | None:
    """Every dated snapshot folder on the remote, oldest first, or None if unlisted.

    ONLY NAMES A BACKUP COULD HAVE WRITTEN. A folder somebody made by hand under
    the snapshot root sorts after every stamp when it starts with a letter, and
    would be offered as the newest snapshot of a database it does not hold
    (R-154, the shape check's other caller).

    None AND EMPTY ARE DIFFERENT ANSWERS and the caller that refuses says which:
    a remote that did not answer is not a remote with nothing on it.
    """
    result = runner(
        Command(
            label=LIST_SNAPSHOTS,
            argv=(_rclone(), "lsf", f"{cfg.backup.db_dest_root}/", "--dirs-only"),
        )
    )
    if result.returncode != 0:
        return None
    return tuple(
        sorted(
            name
            for name in (line.strip().rstrip("/") for line in result.stdout.splitlines())
            if is_snapshot_name(name)
        )
    )


#: How many of the newest snapshots the newest-by-default walk reads a marker
#: from before it gives up. A judgement and NOT MEASURED: enough to step over a
#: week of another library's nightly backups under a shared root, and few enough
#: that a remote holding only unmarked snapshots refuses in seconds.
NEWEST_WALK = 8


@dataclass(frozen=True, slots=True)
class ResolvedSnapshot:
    """Which snapshot a restore will pull, and whose its marker says it is.

    ``named`` is whether a PERSON chose the stamp. It is carried rather than
    re-derived from "a stamp was passed", because the verb resolves the newest
    stamp for its offer and hands that same stamp down, and a stamp that came
    off a listing must not arrive looking typed.
    """

    stamp: str
    recorded_volume: str | None
    named: bool


def snapshot_identities(
    cfg: config.Config, snapshot: str, *, runner: Runner
) -> tuple[str, ...]:
    """Every identity a dated snapshot's markers record, normalized and sorted.

    Empty means the folder was LISTED and holds no marker. A listing that fails
    raises, for the reason :func:`snapshot_filenames` gives one function down: a
    named snapshot with no marker is accepted, so a remote that did not answer
    must never arrive looking like one.

    A marker with nothing after its prefix is reported as the empty identity
    rather than dropped, so it fails the comparison instead of passing as absent.
    """
    result = runner(
        Command(
            label=LIST_SNAPSHOT_IDENTITY,
            argv=(_rclone(), "lsf", f"{cfg.backup.db_dest_root}/{snapshot}/", "--files-only"),
        )
    )
    if result.returncode != 0:
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed, so which library it was taken from is unknown; a restore "
            f"is not planned against a snapshot this account cannot see",
        )
    found = {
        preflight.normalize_identity(name[len(IDENTITY_MARKER_PREFIX):])
        for name in (line.strip() for line in result.stdout.splitlines())
        if name.startswith(IDENTITY_MARKER_PREFIX)
    }
    return tuple(sorted(found))


def resolve_snapshot(
    cfg: config.Config,
    *,
    snapshot: str | None = None,
    snapshot_volume: str | None = None,
    accept_unrecorded: bool | None = None,
    runner: Runner = subprocess_runner,
) -> ResolvedSnapshot:
    """Decide which snapshot is pulled, and refuse one that is not this library's.

    ONE FUNCTION, CALLED TWICE, and both calls matter. The verb calls it before
    its confirmation gate so the offer can show, and digest, the stamp it is
    really offering (R-153). :func:`plan_restore` calls it again under the
    gates, because that is the path every restore takes whoever the caller is,
    and a check that lived only in the verb would be a fix on the performing
    path with the checking path open.

    THE SHAPE IS CHECKED BEFORE THE REMOTE IS ASKED ANYTHING. The value is about
    to become part of a remote path, so a value that is not a stamp never
    reaches an argument list at all, including a listing's.

    THE IDENTITY COMPARED IS A VOLUME'S, because that is the identity a library
    has here, and it has one consequence worth stating. The ordinary reason to
    pull a mirror is a dead drive, and its replacement is a different volume, so
    every snapshot of the old drive names an identity the configuration no
    longer holds. ``snapshot_volume`` is how a person says so: it REPLACES the
    expected identity for this one call, it is never recorded, and it excuses
    nothing else, so a snapshot marked for any third volume is still refused.

    AN UNMARKED SNAPSHOT IS PULLED ONLY WHEN IT WAS NAMED. Every snapshot taken
    before the marker existed is unmarked, and refusing them all would strand
    exactly the person a restore is for. ``accept_unrecorded`` defaults to
    whether a stamp was passed, and a caller handing down a stamp it resolved
    itself says ``False``.

    WITH NO STAMP NAMED, OWNERSHIP SELECTS RATHER THAN VETOES. The newest
    ``NEWEST_WALK`` folders are read newest first and the first one marked for
    the expected identity is the answer. The first cut took the newest folder
    and then refused it, which the built in review drove to two failures: under
    a shared root the default refused whenever the other library had backed up
    last, and a backup cut off before its marker left an unmarked folder in
    front of a good one, which the refusal then told the person to name.
    """
    _require_destinations(cfg)
    root = cfg.backup.db_dest_root
    wanted = snapshot_volume if snapshot_volume is not None else cfg.library.volume_id
    # AN EMPTY IDENTITY IS NO IDENTITY. A marker with nothing after its prefix
    # reads back as the empty string, and an expected value of whitespace folds
    # to the same, so without this the two would match each other and a
    # snapshot that names nobody would be pulled as verified.
    expected = (preflight.normalize_identity(wanted) or None) if wanted is not None else None
    whose = (
        f"the volume this restore was told to expect is {expected or 'empty'}"
        if snapshot_volume is not None
        else f"this library is recorded as volume {expected}"
        if expected is not None
        else f"this library records no {config.VOLUME_IDENTITY_KEY} to compare it with"
    )

    if snapshot is not None:
        if not is_snapshot_name(snapshot):
            raise BackupRefused(
                Refusal.SNAPSHOT_NAME_INVALID,
                f"{snapshot!r} is not a snapshot stamp. A stamp is the dated folder "
                f"name a backup wrote, like {STAMP_EXAMPLE}, "
                f"and nothing else is put into a path on the remote.",
            )
        recorded = snapshot_identities(cfg, snapshot, runner=runner)
        if recorded == (expected,):
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
        accepted = True if accept_unrecorded is None else accept_unrecorded
        if not recorded and snapshot_volume is None and accepted:
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=None, named=True)
        raise _not_this_librarys(
            cfg, snapshot, recorded, whose=whose, stated=snapshot_volume is not None
        )

    names = _snapshot_names(cfg, runner=runner)
    if names is None:
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the dated database snapshots under {root} could not be listed, so "
            f"whether one exists is unknown; a restore is not planned against a "
            f"remote that did not answer",
        )
    if not names:
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"no dated database snapshot was found under {root}",
        )
    # THE NEWEST THAT IS THIS LIBRARY'S, not the newest and then a veto. Under a
    # shared root the newest folder is whichever library backed up last, and a
    # backup cut off between two files leaves a folder with no marker in front
    # of a good one. Refusing on either would make the default unusable exactly
    # where the marker was supposed to help, so ownership selects.
    newest = names[::-1][:NEWEST_WALK]
    seen: dict[str, tuple[str, ...]] = {}
    for name in newest:
        seen[name] = snapshot_identities(cfg, name, runner=runner)
        if seen[name] == (expected,):
            return ResolvedSnapshot(stamp=name, recorded_volume=expected, named=False)
    raise _not_this_librarys(
        cfg,
        newest[0],
        seen[newest[0]],
        whose=whose,
        stated=snapshot_volume is not None,
        walked=len(newest),
    )


def _not_this_librarys(
    cfg: config.Config,
    stamp: str,
    recorded: tuple[str, ...],
    *,
    whose: str,
    stated: bool,
    walked: int = 0,
) -> BackupRefused:
    """The refusal for a snapshot that cannot be shown to be this library's.

    THREE SENTENCES FOR THREE STATES OF ONE FOLDER, because each sends a person
    somewhere different and two of them used to share words that were false for
    one of the two.

    * No marker. Either the snapshot predates the marker or its backup was cut
      off before the marker was written, and the message says BOTH, because
      telling a person to name a snapshot that is really half a database set
      sends them to pull it over the live one.
    * Two markers. Two libraries wrote one dated folder in one second, the
      database beside them is whichever landed last, and NO stated identity can
      vouch for it, so the message does not offer one.
    * One marker, another volume. The ordinary mismatch.
    """
    root = cfg.backup.db_dest_root
    looked = (
        f"none of the {walked} newest snapshots under {root} says it was taken "
        f"from this library. The newest, {stamp},"
        if walked
        else f"the snapshot {stamp} under {root}"
    )
    if not recorded:
        if stated:
            return BackupRefused(
                Refusal.SNAPSHOT_LIBRARY_MISMATCH,
                f"{looked} does not say which library it was taken from, and "
                f"{whose}. An expected identity cannot be confirmed against a "
                f"snapshot that records none.",
            )
        return BackupRefused(
            Refusal.SNAPSHOT_IDENTITY_UNRECORDED,
            f"{looked} does not say which library it was taken from. That is true "
            f"of every snapshot taken before identities were recorded, and also of "
            f"one whose backup did not finish, so check it holds a whole database "
            f"before pulling it. It is pulled only when it is named: "
            f"--snapshot {stamp}",
        )
    if len(recorded) > 1:
        return BackupRefused(
            Refusal.SNAPSHOT_LIBRARY_MISMATCH,
            f"{looked} carries {len(recorded)} identities, "
            f"{' and '.join(r or '(empty)' for r in recorded)}, so two libraries "
            f"wrote into it and the database it holds is whichever copy landed "
            f"last. No expected volume can vouch for it; name another snapshot.",
        )
    return BackupRefused(
        Refusal.SNAPSHOT_LIBRARY_MISMATCH,
        f"{looked} says it was taken from the library on volume "
        f"{recorded[0] or '(empty)'}, and {whose}. Restoring it would put another "
        f"library's database here.",
    )


def snapshot_filenames(
    cfg: config.Config, snapshot: str, *, runner: Runner
) -> frozenset[str]:
    """The filenames a dated database snapshot actually holds.

    A listing that fails is a snapshot this account cannot see, not an empty
    folder. Treating a failed listing as no sidecars would skip the log and
    report a complete restore against a remote that never answered.
    """
    result = runner(
        Command(
            label=LIST_SNAPSHOT_CONTENTS,
            argv=(
                _rclone(),
                "lsf",
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
                "--files-only",
            ),
        )
    )
    if result.returncode != 0:
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed; a restore cannot be planned against a snapshot this "
            f"account cannot see",
        )
    return frozenset(
        line.strip().rstrip("/")
        for line in result.stdout.splitlines()
        if line.strip()
    )


def share_is_held(cfg: config.Config, *, identity: str | None, runner: Runner) -> bool:
    """Whether the remote holds a mirror of this library's outside share.

    THREE ANSWERS, AND ONLY TWO OF THEM ARE ABOUT THE SHARE. A listing that names
    something is a mirror. A listing that names nothing, or a directory rclone
    says does not exist, is a backup taken before the share was carried, which is
    every backup older than R-338's fix and is normal. Anything else is a remote
    that did not answer, and reading that as "no share" would plan a restore
    that reports complete over grids it never looked for.
    """
    result = runner(
        Command(
            label=LIST_SHARE,
            argv=(_rclone(), "lsf", f"{share_destination(cfg, identity=identity)}/current/"),
        )
    )
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        return False
    if result.returncode != 0:
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the analysis share mirror under {cfg.backup.db_dest_root} could not "
            f"be listed (exit {result.returncode}), so whether this library's beat "
            f"grids are in the backup is unknown; a restore is not planned against "
            f"a remote that did not answer",
        )
    return bool(result.stdout.strip())


def plan_restore(
    cfg: config.Config,
    *,
    target: Path | str,
    confirmed: bool,
    snapshot: str | None = None,
    snapshot_volume: str | None = None,
    accept_unrecorded: bool | None = None,
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
            snapshot_volume=snapshot_volume,
            accept_unrecorded=accept_unrecorded,
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
    snapshot_volume: str | None,
    accept_unrecorded: bool | None,
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

    # A STAMP, AND THIS LIBRARY'S, before it is put into a single path (R-154).
    resolved = resolve_snapshot(
        cfg,
        snapshot=snapshot,
        snapshot_volume=snapshot_volume,
        accept_unrecorded=accept_unrecorded,
        runner=runner,
    )
    chosen = resolved.stamp

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
    # Only the sidecars a restore writes BACK, and only when the snapshot holds
    # them. The shared-memory index is derived from the log, so putting a stale
    # one back beside a fresh log hands SQLite two disagreeing views of one
    # database; the declaration says which. Absence is normal: a checkpointed
    # database has no write ahead log, and the snapshot verb copies a sidecar
    # only when it is present, so a restore that always copies the log is a
    # restore that always fails against the only kind of snapshot this product
    # takes (R-367).
    held = snapshot_filenames(cfg, chosen, runner=runner)
    absent: list[str] = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if not sidecar.restored:
            continue
        name = f"{database_target.name}{sidecar.suffix}"
        if name not in held:
            absent.append(sidecar.suffix)
            continue
        commands.append(
            Command(
                label=RESTORE_DATABASE,
                argv=(
                    rclone,
                    "copy",
                    f"{base}/{name}",
                    f"{database_target.parent}/",
                ),
            )
        )
    # THE SHARE COMES BACK BESIDE THE DATABASE, LAST, AND ONLY FROM A LISTING
    # (R-338). Planned from a listing because the sidecars are cleared before the
    # first transfer, so a copy from a mirror that is not there would fail after
    # the clearing, which is the refusal ``_ran`` describes. A COPY, NEVER A
    # SYNC, for the reason the mirror half gives: the share beside a database
    # being restored may hold analysis the mirror never saw.
    #
    # WHOSE SHARE: the library the snapshot's marker names. An unmarked snapshot
    # falls back to this configuration's identity, because a marker that failed
    # to write is a warning and the same run still mirrored the share under it.
    share_absent = False
    if _outside_share(cfg) is not None:
        whose = resolved.recorded_volume or cfg.library.volume_id
        if share_is_held(cfg, identity=whose, runner=runner):
            commands.append(
                Command(
                    label=RESTORE_SHARE,
                    argv=(
                        rclone, "copy",
                        f"{share_destination(cfg, identity=whose)}/current",
                        str(database_target.parent / analysis_store.SHARE_DIRNAME),
                        "--transfers", "8", "--checkers", "16",
                    ),
                )
            )
        else:
            share_absent = True
    return RestorePlan(
        target=target,
        database_target=database_target,
        snapshot=chosen,
        clears=clears,
        commands=tuple(commands),
        absent_sidecars=tuple(absent),
        recorded_volume=resolved.recorded_volume,
        share_absent=share_absent,
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
        # RENDERED FROM THE OUTCOME, so every reader of a rendered run learns
        # which kind it was from the run itself. It used to be written onto the
        # report by the one caller that thought of it, which is a field that is
        # correct where somebody remembered and absent everywhere else.
        "dry_run": outcome.dry_run,
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
    "ANALYSIS_SHARE_ABSENT",
    "LIST_SHARE",
    "LIST_SNAPSHOT_CONTENTS",
    "RESTORE_MIRROR",
    "RESTORE_SHARE",
    "SNAPSHOT_SHARE",
    "RestorePlan",
    "absent_analysis_share",
    "database_fileset",
    "database_target_for",
    "dry_run_argv",
    "latest_snapshot",
    "plan_backup",
    "snapshot_filenames",
    "plan_payload",
    "plan_restore",
    "outcome_payload",
    "rekordbox_processes_running",
    "run_backup",
    "run_restore",
    "running_process_names",
    "share_destination",
    "share_is_held",
    "settings_directories",
    "stamp_for",
    "subprocess_runner",
]
