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

import json
import os
import re
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path

from cratekit.core import analysis_store, backup_facts, binaries, config, preflight, session
from cratekit.core.cause import CratekitError
from cratekit.core.processes import (
    REKORDBOX_PROCESSES,
    AbsenceUnconfirmed,
    ProcessLister,
    rekordbox_processes_running,
    running_process_names,
)
from cratekit.modules.tools import backup_record

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
#: The three commands of a QUICK run (U317), each reading its paths from
#: standard input and none listing the remote. The first sends what was added
#: or changed, the second what was rewritten in place with its size and time
#: kept, and the third moves what was removed into this run's dated archive,
#: which is where the full sync's ``--backup-dir`` puts a deletion.
QUICK_SEND = "quick-send"
QUICK_RESEND = "quick-resend"
QUICK_ARCHIVE = "quick-archive"
QUICK_LABELS: frozenset[str] = frozenset({QUICK_SEND, QUICK_RESEND, QUICK_ARCHIVE})

#: What a completed portion's run was (U317), the word its fact records under
#: ``kind``. The files portion is ``full``, ``quick`` or ``skipped``; the
#: database portion is ``snapshot`` or ``unchanged``. ``backup_facts.KINDS``
#: holds the same words, which it accepts and doctor reads, and a test holds
#: the two equal.
KINDS = ("full", "quick", "skipped", "snapshot", "unchanged")
KIND_FULL, KIND_QUICK, KIND_SKIPPED, KIND_SNAPSHOT, KIND_UNCHANGED = KINDS

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
#: the backup itself fails. A mirror costs the share once plus what changes, and
#: its dated archive keeps every run undoable. THAT ARCHIVE IS NEVER ROTATED,
#: unlike the library mirror's, so it grows by whatever rekordbox rewrote between
#: runs. Recorded as a residual rather than pruned here, because a prune is a
#: delete on the remote and this unit's brief is a read and a copy.
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
        QUICK_SEND,
        QUICK_RESEND,
        QUICK_ARCHIVE,
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

#: A portion completed and the record a quick run reads next time could not be
#: kept (U317). A warning and not a failure: the backup exists and its age is
#: true, and what is lost is speed, since the next run is a full check.
BACKUP_RECORD_NOT_KEPT = "backup-record-not-kept"

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

#: The flag that is the only way past the content proof (R-1761), named once
#: so every refusal and failure that names it names the one the verb declares.
EMPTIED_FLAG = "--library-emptied"

#: R-1761. What a new library's first backup is given, so rclone itself
#: deletes no file from the mirror: one it would delete fails the run instead.
#: A new library has nothing to remove, and a lost volume's mount point on an
#: installation that remembers nothing would otherwise archive the whole
#: mirror. ``--max-delete`` counts a move into ``--backup-dir`` as a delete. It
#: stops deletions and not overwrites: a file the library sends over an older
#: copy still moves that copy into the archive, as every mirror does.
MOVE_NOTHING = ("--max-delete", "0")

#: The option that makes rclone list the remote in one recursive pass, where it
#: otherwise asks once per folder (R-757). It changes HOW THE REMOTE IS LISTED
#: and nothing about what is compared: every file on both sides is still
#: compared by size and modification time, so a file that changed is sent in
#: either mode.
#:
#: MEASURED ON THE AUTHOR'S LIBRARY, 2026-09-29, 91,265 files in 22,433 folders.
#: The local walk took 1.5 seconds. The mirror without this option had compared
#: 18,774 files after 220 seconds and was killed at 540, a rate the remote's
#: request pacing sets and 64 checkers did not move. The same command with this
#: option compared all 91,235 in 190 seconds.
FAST_LIST = "--fast-list"

#: The two ways the mirror lists the remote, as the words a report carries.
COMPARISON_FAST = "fast"
COMPARISON_FULL = "full"
#: A quick run's report (U317), which compared the library with the record and
#: listed nothing on the remote.
COMPARISON_QUICK = "quick"

#: What makes rclone say what the mirror did, in a shape that can be read
#: rather than scraped. Without ``--stats-log-level`` the final totals are
#: logged below the level rclone prints at, and with a ``--stats`` of zero they
#: are not logged at all, both measured. The interval is an hour so an ordinary
#: run carries the final totals and no others.
MIRROR_STATS_ARGS: tuple[str, ...] = (
    "--use-json-log",
    "--stats", "1h",
    "--stats-log-level", "NOTICE",
)


class Refusal(StrEnum):
    """Why a portion will not run, as a structured cause (KTD25, D2).

    Each member names one diagnosis with one fix, and none of them carries the
    text a user types. U5 reserves an exit code and a remediation per member.
    """

    RCLONE_MISSING = "rclone-missing"
    REMOTE_NOT_CONFIGURED = "remote-not-configured"
    DESTINATION_NOT_CONFIGURED = "destination-not-configured"
    LIBRARY_ROOT_ABSENT = "library-root-absent"
    # R-1761. The root is a directory and not provably this library: a volume
    # that is not the one recorded for it, or a folder that holds none of its
    # files, the empty mount point an unmounted drive leaves. Two members for
    # two acts: the first is fixed only by mounting the right volume, and the
    # second also by saying the library was emptied on purpose.
    LIBRARY_ROOT_FOREIGN = "library-root-foreign"
    LIBRARY_ROOT_UNPROVEN = "library-root-unproven"
    REKORDBOX_RUNNING = "rekordbox-running"
    # U211. The process scan met a live process it could not read, so whether
    # rekordbox is closed was not established. Its own member because "quit
    # rekordbox" would be false, and the database portion refuses alone so the
    # file mirror still runs.
    REKORDBOX_ABSENCE_UNCONFIRMED = "rekordbox-absence-unconfirmed"
    DATABASE_ABSENT = "database-absent"
    RESTORE_NOT_CONFIRMED = "restore-not-confirmed"
    RESTORE_TARGET_ABSENT = "restore-target-absent"
    NO_SNAPSHOT_AVAILABLE = "no-snapshot-available"
    # R-388. A listing on the remote that exited non zero. Its own member rather
    # than the one above, because the acts differ: no snapshot is fixed by taking
    # a backup, and a listing that failed is fixed by checking the remote, its
    # credential and the configured root. A person told to take a backup here
    # takes one they already have and leaves the real fault where it was.
    SNAPSHOT_LISTING_FAILED = "snapshot-listing-failed"
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
    #: What the runner pipes to the program, or None for nothing. A quick run's
    #: paths travel here and rclone reads them with ``--files-from-raw -``, so
    #: the plan stays data and no list file is left behind. Nothing in this
    #: module reads its own standard input.
    feed: str | None = None


@dataclass(frozen=True, slots=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""
    #: Wall clock seconds the command took, or None when the runner did not
    #: time it. None and never zero: a stand-in runner that measured nothing
    #: must not report a comparison that took no time.
    elapsed: float | None = None


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
    #: Which kind of run this portion is (U317), one of :data:`KINDS`,
    #: or empty for a refused portion. A ``skipped`` or ``unchanged`` portion
    #: carries no command and still runs: it publishes its age, because the
    #: plan proved the remote already holds what it would have sent.
    kind: str = ""
    #: Why the files portion is a full run, or empty when it is not.
    why: str = ""
    #: What the walk found changed since the record, by kind of change, or
    #: None where no comparison with a record was made.
    changes: Mapping[str, int] | None = None
    #: What a completed run settles its record from: the walk before the
    #: transfer, or the fingerprint before the snapshot. None keeps no record.
    basis: object = field(default=None, compare=False, repr=False)
    #: The token of the record a skip was proved against, carried onto the
    #: fact it publishes.
    record_token: str = ""
    #: R-1761. The device the library root was on when the plan read it, which
    #: the full mirror is held to just before it runs, and -1 where it could
    #: not be read, which holds it to nothing and fails it.
    root_dev: int = -1
    #: R-1761. How many files outside the library's own state folder the plan
    #: found, by the walk or, where it refused, by the probe: the census a
    #: completed portion keeps.
    held: int = 0

    @property
    def will_run(self) -> bool:
        if self.refusal is not None:
            return False
        return bool(self.commands) or self.kind in _NOTHING_TO_SEND


#: The kinds that complete with no command, because nothing changed.
_NOTHING_TO_SEND = frozenset({KIND_SKIPPED, KIND_UNCHANGED})


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
    #: The commands handed to the runner, index for index with ``results``
    #: (R-349). A return code with no argv beside it cannot say which rclone
    #: invocation failed, and that is the question a failed backup is asked. It
    #: is the command AS RUN, so a rehearsal records its neutralized argv and
    #: the rotation records its listing and every purge it attempted.
    commands: tuple[Command, ...] = field(default_factory=tuple)
    #: What the mirror's comparison did (R-757), or None for a portion that ran
    #: no mirror. Built by :func:`comparison_report` from the command AS RUN and
    #: from rclone's own totals.
    comparison: Mapping[str, object] | None = None
    #: The plan's kind, reason and changes, carried so a report says which kind
    #: of run this was without the plan beside it (U317).
    kind: str = ""
    why: str = ""
    changes: Mapping[str, int] | None = None
    #: Wall clock seconds the portion took, its walk included.
    seconds: float | None = None


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
    full: bool = False,
    check: bool = False,
    only: backup_facts.Portion | None = None,
    emptied: bool = False,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> BackupPlan:
    """Decide what a run would do. Touches no remote and copies nothing.

    ``full`` lists the remote folder by folder, the way every mirror did before
    R-757, instead of in one recursive pass. Both modes compare every file, so
    it selects the slower listing that does not depend on the recursive one
    being complete, and nothing else.

    ``check`` asks for a FULL CHECK (U317), the backup as it always was: the
    mirror lists the remote and compares every file, and the database is
    snapshotted whether or not it changed. Without it the files portion runs
    one only when :func:`_full_reason` names a reason, and otherwise compares
    the library with the record of the last completed backup and plans a quick
    run of the difference, or a skip; the database is snapshotted only when it
    changed. ``full`` is a full check too.

    THE WEEKLY FULL CHECK IS THE FILES PORTION'S ALONE. It exists to read the
    remote again, which only the mirror lists. A queued backup plans each
    portion in its own item, after the one before it published, so a due date
    read by the database item would already have moved, and only the frozen
    flags force a snapshot the same way in both items.

    ``only`` plans one portion, so the item that backs up the database does not
    walk the library and the item that mirrors it does not read the database.

    THE FILES PORTION PROVES THE ROOT IS THE LIBRARY FIRST (R-1761), or refuses
    with no command: the recorded volume identity where the platform reads
    one, and a walk holding the library's files measured against the census
    the last completed backup kept. ``emptied`` is the one way past the second,
    for a library its owner emptied on purpose, and ``identity_provider`` and
    ``mount_enumerator`` are the identity's seams, as ``preflight`` takes them.
    ``check`` and ``full`` are no way past either: an attended sitting asks for
    a full check, and the volume may be the thing missing.

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
    moment = now or datetime.now(timezone.utc)
    stamp = stamp_for(moment)
    rclone = binaries.find("rclone")
    portions: list[PortionPlan] = []
    wanted = tuple(p for p in backup_facts.Portion if only is None or p is only)

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
                for p in wanted
            ),
        )

    if backup_facts.Portion.FILES in wanted:
        asked = (
            "a full check was asked for"
            if check or full
            else _full_reason(cfg, now=moment)
        )
        portions.append(
            _plan_files(
                cfg,
                rclone=rclone,
                stamp=stamp,
                archive_keep=archive_keep,
                full=full,
                asked=asked,
                emptied=emptied,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
            )
        )
    if backup_facts.Portion.DATABASE in wanted:
        portions.append(
            _plan_database(
                cfg,
                rclone=rclone,
                stamp=stamp,
                process_lister=process_lister,
                settings_dirs=settings_dirs,
                snapshot_anyway=check or full,
            )
        )
    return BackupPlan(stamp=stamp, archive_keep=archive_keep, portions=tuple(portions))


def _full_reason(cfg: config.Config, *, now: datetime) -> str:
    """Why the next run must be a full check by the calendar, or an empty string.

    Read off the files portion's age, which carries the full check's schedule,
    so the planner and the session gate answer from one reading of the fact
    file. A fact file that cannot be read is a reason too. A record that is
    missing or damaged is the files portion's own reason, read where the
    record is.
    """
    try:
        reported = backup_facts.ages(cfg, now=now)
    except backup_facts.BackupFactsUnreadable as exc:
        return f"the record of the last full check could not be read: {exc}"
    files = next(entry for entry in reported if entry.portion is backup_facts.Portion.FILES)
    return files.full_check_overdue


#: The summary key under which a files fact carries its record's token (U317).
RECORD_TOKEN = "record"


def _strike_token(cfg: config.Config) -> None:
    """Strike the record's token from the library's files fact, leaving its age.

    Through the fact file's own reader and writer, so the age, its destination,
    its kind and the held full check and full comparison travel through as they
    were. A fact with no token is left as it is and the file not rewritten.
    """
    fact = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
    if fact is None or fact.summary is None or RECORD_TOKEN not in fact.summary:
        return
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=fact.completed_at,
        destination=fact.destination,
        kind=fact.kind,
        summary={name: value for name, value in fact.summary.items() if name != RECORD_TOKEN},
    )


def _record_unpublished(cfg: config.Config, manifest: backup_record.Manifest) -> str:
    """Why the library's files fact says another writer reached the mirror.

    THE RECORD IS THIS INSTALLATION'S AND THE MIRROR IS NOT. A second
    installation of this library, or a build before U317 on this state, mirrors
    without reading or removing this record, so a run of either that sent or
    archived files would leave it describing a remote it no longer matches.
    Each of them publishes a files fact without this record's token, so the
    fact the library carries is asked: unless it is the one this record was
    published with, the run is full.
    """
    try:
        fact = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
    except backup_facts.BackupFactsUnreadable as exc:
        return f"the record of the last backup's age could not be read: {exc}"
    held = (fact.summary or {}).get(RECORD_TOKEN) if fact is not None else None
    if fact is None or not manifest.token or held != manifest.token:
        return (
            "the library's backup age was published by a run that did not keep "
            "this record, another installation or an older build, so the mirror "
            "may have changed since it was kept"
        )
    return ""


def _self_written(cfg: config.Config) -> frozenset[str]:
    """The files under the library root the backup itself rewrites after a run.

    The fact file is library state inside the mirrored tree, and every run
    publishes it after its transfer, so the remote's copy is a run behind under
    every kind of run. Counting it would make every run after a backup a
    change, and no run could ever be skipped.
    """
    try:
        # The fact file's inventory key, which ``backup_facts`` resolves by.
        rel = config.state_path("backup_facts", cfg).relative_to(cfg.library.root)
    except ValueError:
        return frozenset()
    return frozenset({rel.as_posix()})


def _plan_files(
    cfg: config.Config,
    *,
    rclone: str,
    stamp: str,
    archive_keep: int,
    full: bool = False,
    asked: str = "a full check was asked for",
    emptied: bool = False,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> PortionPlan:
    """The files portion: a full check, a quick run of the difference, or a skip.

    ``asked`` is why a full check is due before the record is read, or empty.
    The library is walked whichever kind follows, because the walk before the
    transfer is what a completed full check settles the next record from.

    NOTHING IS PLANNED OVER A ROOT THAT IS NOT PROVEN TO BE THE LIBRARY
    (R-1761). An empty folder at the root, the mount point an unmounted drive
    leaves, walks as a library with no files, and both a full sync and a quick
    run of that difference empty the mirror into the archive. So the root is
    proved by the identity and then by what the walk holds, and a refusal
    carries no command: no record removed, no token struck, no age published.
    """
    root = cfg.library.root
    if not root.is_dir():
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_ABSENT,
            detail=f"the library root {root} is not a directory; mount the volume first",
        )
    foreign = _not_the_recorded_volume(
        cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    if foreign:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_FOREIGN,
            detail=foreign,
        )
    excludes = _mirror_excludes(cfg)
    state_dirname = cfg.library.state_dirname
    why = asked
    manifest: backup_record.Manifest | None = None
    if not why:
        manifest, why = backup_record.read_manifest()
    if manifest is not None and not why:
        why = backup_record.manifest_mismatch(manifest, cfg, excludes)
    if manifest is not None and not why:
        why = _record_unpublished(cfg, manifest)
    trusted = manifest.entries if manifest is not None and not why else {}
    try:
        root_dev = os.stat(root).st_dev
    except OSError:
        root_dev = -1
    try:
        before = backup_record.walk(
            root,
            excludes,
            hash_paths=[rel for rel, entry in trusted.items() if entry.sha256 is not None],
        )
    except backup_record.WalkRefused as exc:
        before = None
        why = why or f"the library could not be walked: {exc}"
    if before is not None:
        root_dev = before.root_dev
        anything = bool(before.entries)
        held = backup_record.count_held(before.entries, state_dirname)
    else:
        # The walk refused, so it is counted another way: the floor below
        # needs a number, and the census this run keeps needs one too.
        anything, held = backup_record.probe(root, excludes, state_dirname)
    unproven, new_library = _unproven(cfg, anything=anything, held=held, emptied=emptied)
    if unproven:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_UNPROVEN,
            detail=unproven,
        )
    proof = {"root_dev": root_dev, "held": held}
    # A ROOT HOLDING NONE OF THE LIBRARY'S FILES IS MIRRORED DELETING NOTHING,
    # whatever is on record, unless the flag says it was emptied on purpose. A
    # new library's first backup has nothing to delete, and a census of none
    # only says the last completed backup held nothing: a later run that failed
    # part way can have sent files the census never counted, and a full sync
    # over a lost volume's mount point would archive them. A skip runs no
    # command and a quick run archives only paths the record held, so both are
    # planned as any other.
    move_nothing = held == 0 and not emptied
    if new_library:
        why = (
            "the library holds no file outside its state folder and no "
            "backup of it is on record, so it runs as a new library's "
            "first backup, which deletes nothing from the mirror"
        )
    if not why and before is not None:
        found = backup_record.difference(
            trusted, before.entries, self_written=_self_written(cfg)
        )
        if not found.anything:
            return PortionPlan(
                portion=backup_facts.Portion.FILES,
                kind=KIND_SKIPPED,
                detail="nothing changed since the last completed backup",
                changes=found.counts(),
                basis=before,
                record_token=manifest.token if manifest is not None else "",
                **proof,
            )
        uncomposed = backup_record.first_uncomposed(found.paths)
        if len(found.paths) > backup_record.QUICK_LIMIT:
            why = (
                f"{len(found.paths)} paths changed, more than the "
                f"{backup_record.QUICK_LIMIT} a quick run is for"
            )
        elif uncomposed is not None:
            why = (
                f"the changed name {uncomposed!r} is not in composed Unicode form, "
                f"and a quick run looks each name up on the remote, where a remote "
                f"that composes names would not find it"
            )
        else:
            return PortionPlan(
                portion=backup_facts.Portion.FILES,
                kind=KIND_QUICK,
                commands=_quick_commands(
                    cfg, rclone=rclone, stamp=stamp, archive_keep=archive_keep, found=found
                ),
                detail=_rotation_detail(archive_keep),
                changes=found.counts(),
                basis=before,
                **proof,
            )
    return PortionPlan(
        portion=backup_facts.Portion.FILES,
        kind=KIND_FULL,
        why=why,
        commands=_full_commands(
            cfg,
            rclone=rclone,
            stamp=stamp,
            archive_keep=archive_keep,
            full=full,
            move_nothing=move_nothing,
        ),
        detail=_rotation_detail(archive_keep),
        basis=before,
        **proof,
    )


def _not_the_recorded_volume(
    cfg: config.Config,
    *,
    identity_provider: preflight.IdentityProvider | None,
    mount_enumerator: preflight.MountEnumerator | None,
) -> str:
    """Why the root is on a volume other than the library's, or an empty string.

    The first proof (R-1761), through the volume gate destructive sessions
    pass, read for what it found: a recorded identity read and found elsewhere,
    or not at all, refuses whatever else the root holds. An identity the
    platform cannot read, or one never recorded, is no answer and is left to
    the census, which holds on every platform: every Linux volume reads as the
    first, and refusing it would stop every backup there.

    An identity read that raises is the same unread identity, left to the
    census, and never a refusal: a flaky probe of the volume should not stop
    every backup when the second proof stands on its own.
    """
    try:
        session.assert_volume_identity(
            cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
        )
    except CratekitError as exc:
        found = exc.cause.detail or {}
        recorded, observed = found.get("recorded_identity"), found.get("observed_identity")
        if recorded is None or observed is None:
            return ""
        return (
            f"the volume at the library root {cfg.library.root} is not the one "
            f"recorded for this library (recorded {recorded}, observed {observed}), "
            f"so the folder there is not proven to be this library and nothing "
            f"was sent or archived; mount the library's own volume and back up again"
        )
    except Exception:  # noqa: BLE001 - an unread identity is left to the census
        return ""
    return ""


def _history(cfg: config.Config) -> tuple[int | None, str] | None:
    """How many of the library's files the last completed backup held, and
    which record says so, or None when no record says a backup was kept.

    THE CENSUS ANSWERS FIRST AND ALONE when there is one for this root and
    mirror, since it is the one record no run removes: a count of none says the
    last backup held nothing and there is nothing to guard. Without it, a
    record kept for this root and mirror (one an older build kept), and then
    the library's own files fact, which goes with its volume. A count of None
    is a backup that happened with a count nobody can read.
    """
    census = backup_record.read_census(cfg)
    if census is not None:
        return census.files, "the last completed backup"
    manifest, _ = backup_record.read_manifest()
    if (
        manifest is not None
        and manifest.library_root == str(cfg.library.root)
        and manifest.dest == str(cfg.backup.dest)
    ):
        return (
            backup_record.count_held(manifest.entries, cfg.library.state_dirname),
            "the record of the last completed backup",
        )
    try:
        fact = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
    except backup_facts.BackupFactsUnreadable:
        return None, "the library's own record of its backups"
    if fact is not None:
        return None, "the library's own record of its backups"
    return None


def _unproven(
    cfg: config.Config, *, anything: bool, held: int, emptied: bool
) -> tuple[str, bool]:
    """Why what the root holds does not prove it is the library, or an empty
    string, and whether it is a new library's first backup.

    The second proof (R-1761), and the one that holds where no identity is
    read. ``anything`` is whether the root holds any file the mirror carries,
    and ``held`` how many outside the library's own state folder.

    ``emptied`` passes the census and nothing else: the root must still carry
    the library's own fact of a completed FILES backup, which every completed
    files run leaves in its state folder. A library its owner emptied keeps
    it; the mount point a lost volume leaves does not, so a queued job frozen
    with the flag and driven after the volume went refuses as a plain ask does.
    The fact file alone proves nothing: the database item of the same job
    writes one wherever the root is when the database lives outside it, with
    a database fact and no files fact.
    """
    root = cfg.library.root
    remedy = (
        f"Mount the library's volume and back up again; if the library was "
        f"emptied on purpose, back it up with {EMPTIED_FLAG}"
    )
    if emptied:
        try:
            carried = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
        except backup_facts.BackupFactsUnreadable:
            carried = None
        if carried is not None:
            return "", False
        return (
            f"the backup was asked with {EMPTIED_FLAG} and the library root "
            f"{root} does not carry the library's own record of a completed "
            f"files backup, which a library emptied by its owner keeps in its "
            f"state folder and the folder an unmounted volume leaves does not, "
            f"so nothing was sent or archived. Mount the library's volume and "
            f"back up again; a library emptied before its first completed "
            f"backup needs no flag"
        ), False
    history = _history(cfg)
    if not anything:
        held_before = ""
        if history is not None and history[0]:
            held_before = f", where {history[1]} held {history[0]} files"
        return (
            f"the library root {root} holds no file at all, not even the "
            f"library's own state folder{held_before}, which is what an "
            f"unmounted volume leaves, so nothing was sent or archived. {remedy}"
        ), False
    if history is None:
        return "", held == 0
    had, said = history
    if held == 0 and had != 0:
        counted = "files" if had is None else f"{had} files"
        return (
            f"the library root {root} holds no file outside the library's own "
            f"state folder, and {said} held {counted}, so nothing was sent or "
            f"archived. {remedy}"
        ), False
    if had and held * backup_record.LIBRARY_FLOOR < had:
        return (
            f"the library root {root} holds {held} files outside the library's "
            f"own state folder, under a tenth of the {had} {said} held, so it is "
            f"not proven to be the library and nothing was sent or archived. "
            f"{remedy}"
        ), False
    return "", False


def _quick_commands(
    cfg: config.Config,
    *,
    rclone: str,
    stamp: str,
    archive_keep: int,
    found: backup_record.Difference,
) -> tuple[Command, ...]:
    """A quick run's commands: the difference sent, rewritten and archived.

    NONE LISTS THE REMOTE. ``--no-traverse`` makes rclone look each listed path
    up on its own, and each still compares size and time before it sends, so a
    path already current costs a lookup and no transfer.

    The archive is this run's dated folder, the one the full sync's
    ``--backup-dir`` names, so whatever a quick run overwrites or removes is
    undoable exactly as a full run's is, and the rotation counts it the same.
    """
    root, dest = str(cfg.library.root), str(cfg.backup.dest)
    archive = f"{cfg.backup.archive_root}/{stamp}"
    listed = ("--files-from-raw", "-", "--no-traverse")
    commands: list[Command] = []
    send = (*found.added, *found.changed)
    if send:
        commands.append(
            Command(
                label=QUICK_SEND,
                argv=(
                    rclone, "copy", root, dest, *listed, "--backup-dir", archive,
                    "--transfers", "8", "--checkers", "16", *MIRROR_STATS_ARGS,
                ),
                feed=backup_record.paths_list(send),
            )
        )
    resend = tuple(sorted((*found.rewritten, *found.doubted)))
    if resend:
        # THE ONE PLACE A TIME IS IGNORED, and only for files whose size and
        # time held while their content hash moved, or whose record was a
        # doubt. rclone compares size and time, so without this it would find
        # each one current and send none.
        commands.append(
            Command(
                label=QUICK_RESEND,
                argv=(
                    rclone, "copy", root, dest, *listed, "--ignore-times",
                    "--backup-dir", archive, "--transfers", "8", "--checkers", "16",
                    *MIRROR_STATS_ARGS,
                ),
                feed=backup_record.paths_list(resend),
            )
        )
    if found.removed:
        # A path already gone from the remote is no error to rclone, so a
        # retried run archives what is left and nothing else.
        commands.append(
            Command(
                label=QUICK_ARCHIVE,
                argv=(rclone, "move", dest, archive, *listed, *MIRROR_STATS_ARGS),
                feed=backup_record.paths_list(found.removed),
            )
        )
    if archive_keep >= 0:
        commands.append(_prune_listing(cfg, rclone))
    return tuple(commands)


def _prune_listing(cfg: config.Config, rclone: str) -> Command:
    return Command(
        label=PRUNE_ARCHIVE,
        argv=(rclone, "lsf", f"{cfg.backup.archive_root}/", "--dirs-only"),
    )


def _full_commands(
    cfg: config.Config,
    *,
    rclone: str,
    stamp: str,
    archive_keep: int,
    full: bool,
    move_nothing: bool = False,
) -> tuple[Command, ...]:
    """The full check: the mirror as it was before U317, and its rotation.

    ``move_nothing`` adds :data:`MOVE_NOTHING`, for a root holding none of the
    library's files (R-1761).
    """
    root = cfg.library.root
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
                # THE FULL MODE IS THE ABSENCE OF ONE OPTION, so the two modes
                # cannot drift apart in anything else: the excludes, the
                # archive and the comparison itself are the same arguments.
                *(() if full else (FAST_LIST,)),
                *(MOVE_NOTHING if move_nothing else ()),
                *MIRROR_STATS_ARGS,
            ),
        )
    ]
    if archive_keep >= 0:
        # A separate command on purpose: it runs only after the mirror above
        # succeeds, so a failed backup never removes the rollback it might need.
        # A negative keep disables pruning entirely, for a user whose remote has
        # room and who would rather keep every run's archive.
        commands.append(_prune_listing(cfg, rclone))
    return tuple(commands)


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
    snapshot_anyway: bool = True,
) -> PortionPlan:
    """The database portion: a dated snapshot, or none when nothing changed.

    THE FINGERPRINT IS TAKEN ONLY BELOW THE PROCESS CHECK (U317), because it
    reads the live database, and CLAUDE.md allows the backup that read only
    with both rekordbox processes confirmed gone. A refused or unconfirmed scan
    returns above it, so nothing here opens the database file.

    ``snapshot_anyway`` is a full check's: the database is snapshotted whether
    or not it changed, so a full check is the backup as it always was.
    """
    uncovered = absent_analysis_share(cfg)
    try:
        running = rekordbox_processes_running(lister=process_lister)
    except AbsenceUnconfirmed as exc:
        return PortionPlan(
            portion=backup_facts.Portion.DATABASE,
            refusal=Refusal.REKORDBOX_ABSENCE_UNCONFIRMED,
            detail=(
                f"{exc.cause.message}, so no snapshot of the database was taken. "
                f"Previous dated snapshots remain the backstop."
            ),
            warnings=uncovered,
        )
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
    share = _outside_share(cfg)
    carried_share = share if share is not None and share.is_dir() else None
    fileset = database_fileset(cfg)
    folders = (*resolved_settings, *((carried_share,) if carried_share is not None else ()))
    key = backup_record.fingerprint_key(cfg, marker)
    fingerprint = backup_record.database_fingerprint(fileset, folders)
    if not snapshot_anyway and fingerprint is not None:
        held = backup_record.read_fingerprint()
        if (
            held is not None
            and held.get("fingerprint") == fingerprint
            and all(held.get(name) == value for name, value in key.items())
        ):
            return PortionPlan(
                portion=backup_facts.Portion.DATABASE,
                kind=KIND_UNCHANGED,
                detail=(
                    "the database, its settings and its analysis share are what "
                    "the last completed snapshot copied, so no new one is taken"
                ),
                warnings=tuple(warnings),
            )
    basis = (
        None if fingerprint is None else (key, fingerprint, fileset, folders, process_lister)
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
    if carried_share is not None:
        share = carried_share
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
        kind=KIND_SNAPSHOT,
        commands=tuple(commands),
        warnings=tuple(warnings),
        basis=basis,
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

    started = time.monotonic()
    completed = subprocess.run(
        list(command.argv),
        capture_output=True,
        text=True,
        env=binaries.subprocess_env(),
        check=False,
        # A quick run's paths (U317). None leaves standard input as it was for
        # every command that reads none.
        **({"input": command.feed} if command.feed is not None else {}),
    )
    return CommandResult(
        returncode=completed.returncode,
        stdout=completed.stdout or "",
        stderr=completed.stderr or "",
        elapsed=time.monotonic() - started,
    )


def comparison_mode(command: Command) -> str:
    """Which listing one mirror command used, read off the command AS RUN.

    From the argv and from nothing else, so the report, the published fact and
    the command rclone was handed cannot disagree about which mode a run was. A
    flag carried beside the plan would be a second statement of it.
    """
    return COMPARISON_FAST if FAST_LIST in command.argv else COMPARISON_FULL


def _logged(stderr: str) -> list[dict]:
    """The JSON objects one command logged, skipping every line that is not one."""
    out: list[dict] = []
    for line in stderr.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict):
            out.append(entry)
    return out


def _count(stats: Mapping[str, object], key: str) -> int | float | None:
    """One total, or None when rclone did not give a number under that name.

    ``bool`` is refused by name because it is an ``int`` to ``isinstance``, and
    rclone's totals carry two booleans beside the counts.
    """
    value = stats.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def comparison_report(command: Command, result: CommandResult) -> dict[str, object]:
    """What one mirror's comparison did: the mode, the time, and the counts.

    EVERY COUNT IS NONE WHEN IT COULD NOT BE READ, AND NEVER ZERO. A run whose
    totals were not found would otherwise answer "sent 0 files", which is the
    sentence a person reads as nothing having changed.

    ``checked`` IS rclone's OWN COUNT AND ITS OWN MEANING: the files it found
    on both sides and compared. A file that is only in the library is sent
    without being counted there, so a first backup checks none and sends all,
    and the two numbers together are what the run looked at.

    ``seconds`` IS THE WHOLE MIRROR COMMAND, measured around it. rclone compares
    and transfers at once, so the comparison has no separate clock; on a run
    that sent nothing, and on a rehearsal, the two are the same number.
    ``transfer_seconds`` is rclone's own total beside it.

    THE LAST TOTALS LOGGED ARE THE ONES READ, because a run longer than the
    stats interval logs more than one and only the last describes the whole run.
    """
    stats: Mapping[str, object] = {}
    for entry in _logged(result.stderr):
        found = entry.get("stats")
        if isinstance(found, dict):
            stats = found
    return {
        "mode": comparison_mode(command),
        "seconds": result.elapsed,
        "checked": _count(stats, "checks"),
        "sent": _count(stats, "transfers"),
        "sent_bytes": _count(stats, "bytes"),
        "transfer_seconds": _count(stats, "transferTime"),
        # rclone's own names and its own counting. How many files went to the
        # dated archive is not derived from them: between two local folders a
        # replaced file counted as a rename and a removed one as a rename and a
        # delete, and what the remote counts was not measured.
        "renames": _count(stats, "renames"),
        "deletes": _count(stats, "deletes"),
    }


def _said(stderr: str) -> str:
    """What a failed command said, as sentences when it logged JSON.

    The mirror logs JSON so its totals can be read, and the tail of a JSON log
    is the totals object rather than the reason. LINE BY LINE: a logged object
    is rendered as its message, the totals are dropped, and a line that is not
    an object is kept as it was written, because a program that dies outside
    its own logger says why in plain text after a page of JSON.
    """
    lines: list[str] = []
    for line in stderr.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            entry = None
        if not isinstance(entry, dict):
            lines.append(line)
        elif "stats" not in entry:
            lines.append(str(entry.get("msg", "")))
    said = "\n".join(piece.strip() for piece in lines if piece.strip())
    return said or stderr.strip()


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

        started = time.monotonic()
        planned = {"kind": entry.kind, "why": entry.why, "changes": entry.changes}
        if not dry_run and entry.commands:
            # THE RECORD GOES BEFORE THE FIRST TRANSFER IT DESCRIBES (U317), and
            # a record that cannot be removed stops the portion before anything
            # is sent. A record that outlived a failed run could be compared
            # with a tree a person then put back, and would answer "nothing
            # changed" over a remote the failed run half rewrote. Removed, the
            # next run is full whatever happens below.
            try:
                backup_record.invalidate(_record_path(entry.portion))
                if entry.portion is backup_facts.Portion.FILES:
                    # AND THE TOKEN GOES FROM THE LIBRARY'S FACT WITH IT, so a
                    # run that fails after sending leaves every installation's
                    # record untrusted, this one's and any other's: a record is
                    # trusted only while the fact carries its token, and a
                    # failed run publishes no fact to replace it.
                    _strike_token(cfg)
            # A fact file that cannot be read raises out of here, before
            # anything is sent, and the shell refuses with the file it names,
            # as it does when the publish after a transfer meets the same file.
            except OSError as exc:
                outcomes.append(
                    PortionOutcome(
                        portion=entry.portion,
                        ran=False,
                        detail=(
                            f"{entry.portion.value} portion failed before sending "
                            f"anything: the record of the last backup could not be "
                            f"removed ahead of the transfer: {exc}"
                        ),
                        warnings=entry.warnings,
                        **planned,
                    )
                )
                continue

        results: list[CommandResult] = []
        warnings: list[Mapping[str, str]] = list(entry.warnings)
        failed: CommandResult | None = None
        # EVERY RUNNER CALL IN THIS PORTION GOES THROUGH ``recorded``, including
        # the ones ``_prune_archive`` makes, so ``executed`` and ``results`` are
        # built by the same calls and cannot fall out of step. Pairing them
        # afterwards by position would be a second reading of which result
        # belongs to which command, and the prune returns a variable number.
        executed: list[Command] = []
        comparison: Mapping[str, object] | None = None
        quick: list[tuple[Command, CommandResult]] = []
        marker_failed = False

        def recorded(command: Command, _executed: list[Command] = executed) -> CommandResult:
            _executed.append(command)
            return runner(command)

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
                    runner=recorded,
                    keep=plan.archive_keep,
                    purge=not dry_run,
                )
                results += pruned
                if warning is not None:
                    warnings.append(warning)
                continue
            if dry_run:
                command = Command(
                    label=command.label, argv=dry_run_argv(command), feed=command.feed
                )
            elif command.label in QUICK_LABELS and isinstance(entry.basis, backup_record.Walk):
                # THE PLAN'S WALK CAN BE MINUTES OLD BY NOW. Every quick command
                # runs only while the root is still the volume it walked, and
                # what it found removed is archived off the mirror only while
                # every path is still absent, so a volume unmounted after the
                # plan fails the portion here rather than emptying the mirror or
                # sending nothing and calling that a backup.
                stale = backup_record.still_removed(
                    cfg.library.root,
                    entry.basis.root_dev,
                    backup_record.paths_from(command.feed)
                    if command.label == QUICK_ARCHIVE
                    else (),
                )
                if stale:
                    failed = CommandResult(
                        returncode=1, stderr=f"nothing was archived: {stale}"
                    )
                    break
            elif command.label == MIRROR:
                # R-1761, THE SAME QUESTION ASKED OF THE FULL SYNC, which would
                # empty the mirror into the archive to match a folder a volume
                # unmounted after the plan left behind. The root must still be
                # the device the plan read and, where the plan found the
                # library's files, still hold one.
                lost = backup_record.root_still_holds(
                    cfg.library.root,
                    entry.root_dev,
                    _mirror_excludes(cfg),
                    cfg.library.state_dirname,
                    files=entry.held != 0,
                )
                if lost:
                    failed = CommandResult(
                        returncode=1, stderr=f"nothing was sent or archived: {lost}"
                    )
                    break
            result = recorded(command)
            results.append(result)
            if command.label == MIRROR:
                # READ WHETHER OR NOT THE MIRROR SUCCEEDED, so a run that failed
                # after sending half of what changed still says how far it got.
                comparison = comparison_report(command, result)
            if command.label in QUICK_LABELS:
                quick.append((command, result))
                comparison = quick_report(quick)
            if result.returncode != 0 and command.label == SNAPSHOT_IDENTITY:
                marker_failed = True
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
            said = _said(failed.stderr)[-400:]
            if (
                executed
                and executed[-1].label == MIRROR
                and _moves_nothing(executed[-1])
                # rclone names the option it stopped on, "max-delete
                # threshold reached", read off the option itself.
                and MOVE_NOTHING[0].lstrip("-") in failed.stderr
            ):
                said += (
                    f". The library holds none of its files outside its state "
                    f"folder, so this mirror was told to delete nothing from "
                    f"the remote, and the remote holds files it would have "
                    f"moved into the archive. "
                    f"Mount the library's volume and back up again; if the "
                    f"library was emptied on purpose, back it up with {EMPTIED_FLAG}"
                )
            outcomes.append(
                PortionOutcome(
                    portion=entry.portion,
                    ran=False,
                    detail=f"{entry.portion.value} portion failed: {said}",
                    results=tuple(results),
                    warnings=tuple(warnings),
                    commands=tuple(executed),
                    comparison=comparison,
                    seconds=time.monotonic() - started,
                    **planned,
                )
            )
            continue

        if publish and entry.commands:
            # ONLY AFTER EVERY COMMAND RETURNED ZERO, and only where a record
            # was removed above, so a skip keeps the record it was proved
            # against and a rehearsal touches neither.
            kept, token = _settle_record(
                cfg, entry, at=moment, marker_failed=marker_failed
            )
            if kept is not None:
                warnings.append(kept)
        else:
            # A skip keeps the record it was proved against, and its fact
            # carries that record's token on, so the next run trusts it still.
            token = entry.record_token
        if publish and entry.portion is backup_facts.Portion.FILES:
            # R-1761. The census every completed files portion leaves, a skip
            # included, and the one record no run removes before it sends.
            try:
                backup_record.write_census(cfg, entry.held, at=moment)
            except OSError as exc:
                warnings.append(
                    {
                        "code": BACKUP_RECORD_NOT_KEPT,
                        "message": (
                            f"the files portion completed and the count of the "
                            f"library's files the next backup is checked against "
                            f"was not kept: {exc}. The next backup proves the "
                            f"library against the older count, or the record"
                        ),
                    }
                )
        seconds = time.monotonic() - started + _walk_seconds(entry)
        if publish:
            backup_facts.record(
                cfg,
                entry.portion,
                completed_at=moment,
                destination=_destination_for(cfg, entry.portion),
                # READ FROM THE REPORT OF THE COMMAND THAT RAN. A portion with
                # no mirror carries no comparison and records none, so the
                # database portion can never move this fact.
                full_comparison=(
                    comparison is not None
                    and comparison["mode"] == COMPARISON_FULL
                ),
                # A FULL CHECK IS THE MIRROR THAT RAN, in either listing mode,
                # read off the command as run like the fact above.
                full_check=(
                    comparison is not None
                    and comparison["mode"] in (COMPARISON_FAST, COMPARISON_FULL)
                ),
                kind=entry.kind or None,
                summary=_summary(entry, comparison, seconds, token=token),
            )
        outcomes.append(
            PortionOutcome(
                portion=entry.portion,
                ran=True,
                results=tuple(results),
                warnings=tuple(warnings),
                commands=tuple(executed),
                comparison=comparison,
                seconds=seconds,
                **planned,
            )
        )

    # ``dry_run`` RATHER THAN ``not publish``, and the two are not the same
    # question. A caller can ask a real run to publish nothing, and that run
    # still copied the library; a rehearsal is the one that did not. The flag
    # recorded is the one this body branched its neutralisation on.
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=dry_run)


def _moves_nothing(command: Command) -> bool:
    """Whether a mirror command was told to delete nothing from the remote."""
    argv = command.argv
    return any(
        argv[i : i + len(MOVE_NOTHING)] == MOVE_NOTHING for i in range(len(argv))
    )


def _record_path(portion: backup_facts.Portion) -> Path:
    """The record a portion's transfer would make untrue."""
    if portion is backup_facts.Portion.DATABASE:
        return backup_record.fingerprint_path()
    return backup_record.manifest_path()


def _walk_seconds(entry: PortionPlan) -> float:
    """The seconds the plan spent walking the library for this portion."""
    return entry.basis.seconds if isinstance(entry.basis, backup_record.Walk) else 0.0


def _settle_record(
    cfg: config.Config, entry: PortionPlan, *, at: datetime, marker_failed: bool = False
) -> tuple[Mapping[str, str] | None, str]:
    """Keep the record a completed portion leaves, or say why it was not kept.

    THE FILES RECORD IS SETTLED FROM TWO WALKS. The one before the transfer is
    the plan's; the one after is taken here, hashing the same files against the
    same instant, and :func:`backup_record.settled` trusts only the entries the
    two agree on. THE DATABASE FINGERPRINT is taken again the same way and kept
    only when it equals the one taken before the copy, since a database that
    moved while it copied may be in the snapshot in either version.

    Nothing kept is not a failure: the backup exists and its age is true, and
    the next run is full. Each reason is said, so a person whose runs stay slow
    is told why.

    THE SECOND READING OF THE DATABASE IS HELD TO THE RULE THE FIRST WAS: the
    processes are scanned again first, and with either running or unconfirmed
    the database is not read and no fingerprint is kept. A snapshot whose
    identity marker failed keeps none either, so the next run takes a fresh,
    marked one rather than calling the unmarked one current.

    Returns the warning, or None, and the token the files record was kept
    under, or an empty string.
    """
    basis = entry.basis
    try:
        if isinstance(basis, backup_record.Walk):
            excludes = _mirror_excludes(cfg)
            after = backup_record.walk(
                cfg.library.root,
                excludes,
                hash_paths=[rel for rel, e in basis.entries.items() if e.sha256 is not None],
                racy_after_ns=basis.racy_after_ns,
            )
            token = backup_record.new_token()
            backup_record.write_manifest(
                cfg, excludes, backup_record.settled(basis, after), at=at, token=token
            )
            return None, token
        if isinstance(basis, tuple):
            key, fingerprint, fileset, folders, lister = basis
            if marker_failed:
                why = "the snapshot's identity marker could not be written"
            elif _not_confirmed_gone(lister):
                why = "rekordbox was not confirmed gone after the copy"
            elif backup_record.database_fingerprint(fileset, folders) == fingerprint:
                backup_record.write_fingerprint(key, fingerprint, at=at)
                return None, ""
            else:
                why = "the database or a folder beside it changed while it was copied"
        else:
            why = "what it held before the transfer could not be read"
    except (backup_record.WalkRefused, OSError) as exc:
        why = str(exc)
    return {
        "code": BACKUP_RECORD_NOT_KEPT,
        "message": (
            f"the {entry.portion.value} portion completed and the record the next "
            f"run compares against was not kept: {why}. The next backup of it "
            f"is a full one"
        ),
    }, ""


def _not_confirmed_gone(lister: ProcessLister | None) -> bool:
    try:
        return bool(rekordbox_processes_running(lister=lister))
    except AbsenceUnconfirmed:
        return True


def _summary(
    entry: PortionPlan,
    comparison: Mapping[str, object] | None,
    seconds: float,
    *,
    token: str = "",
) -> dict[str, object]:
    """What a fact records about the run that completed it (U317).

    ``record`` is the token of the files record this run left, the one thing
    here a run decides on: a quick run or a skip trusts the record only while
    the library's files fact still carries it.
    """
    out: dict[str, object] = {"seconds": round(seconds, 1)}
    if token:
        out[RECORD_TOKEN] = token
    if entry.why:
        out["why"] = entry.why
    if entry.changes is not None:
        out.update(entry.changes)
    if comparison is not None:
        for name in ("sent", "archived", "checked"):
            if comparison.get(name) is not None:
                out[name] = comparison[name]
    return out


def quick_report(ran: Sequence[tuple[Command, CommandResult]]) -> dict[str, object]:
    """What a quick run's commands did, in the comparison's own words (U317).

    rclone's totals per command, read the way :func:`comparison_report` reads
    the mirror's and summed: ``sent`` is what the two copies transferred,
    ``archived`` what the move put in the dated archive, and ``checked`` the
    listed paths a copy found already current. A total any command did not give
    makes its sum unread, None and never zero, for the reason given there.
    """

    def total(labels: frozenset[str], key: str) -> int | float | None:
        found = [
            comparison_report(command, result)[key]
            for command, result in ran
            if command.label in labels
        ]
        if not found:
            return 0
        if any(value is None for value in found):
            return None
        return sum(found)  # type: ignore[arg-type]

    sending = frozenset({QUICK_SEND, QUICK_RESEND})
    elapsed = [result.elapsed for _, result in ran]
    return {
        "mode": COMPARISON_QUICK,
        "seconds": None if any(e is None for e in elapsed) else sum(elapsed),  # type: ignore[arg-type]
        "sent": total(sending, "sent"),
        "sent_bytes": total(sending, "sent_bytes"),
        "checked": total(sending, "checked"),
        # A copy's --backup-dir moves what it overwrites into the archive, and
        # rclone counts each such move as a rename, as it does the archive's.
        "archived": total(QUICK_LABELS, "renames"),
    }


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


class ShareRestore(StrEnum):
    """What a restore does about the analysis share, in one word (R-338).

    Four answers because there are four facts, and a boolean over them would
    fold two of them into "nothing was pulled", which is the silence this
    finding was about. Single words on purpose: a hyphenated value would join
    the population the reserved cause guard reads as cause shaped.
    """

    #: The share sits under the library root, so the mirror half carries it and
    #: the database half has nothing to do.
    MIRRORED = "mirrored"
    #: Outside the root, held on the remote, and a transfer is planned.
    PULLED = "pulled"
    #: Outside the root, and the remote holds no mirror of it, which is every
    #: backup taken before the share was carried. Rows come back without grids.
    ABSENT = "absent"
    #: Outside the root, and the place it would land is under the analysis
    #: watch, so it is NOT pulled and the remote is not asked. See
    #: :func:`_plan_restore_inside_the_gates`.
    WITHHELD = "withheld"


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
    #: What this restore does about the analysis share. Named on the plan, as
    #: ``absent_sidecars`` is, so a restore that pulled nothing for the share
    #: cannot read as one that pulled it.
    share: ShareRestore = ShareRestore.MIRRORED


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
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A root no backup has written yet is an empty root, not a remote that
        # did not answer, and its answer is to take a backup.
        return ()
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
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A mistyped or pruned stamp. The folder is absent, so the remote and
        # its credential are not what a person should go and check.
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} was not found under {cfg.backup.db_dest_root}",
        )
    if result.returncode != 0:
        raise BackupRefused(
            Refusal.SNAPSHOT_LISTING_FAILED,
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
            Refusal.SNAPSHOT_LISTING_FAILED,
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
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A backup cut off before its database folder was written. Nothing is
        # there to restore, which is an absence and not a remote fault.
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} holds no "
            f"database folder, so there is nothing in it to restore",
        )
    if result.returncode != 0:
        raise BackupRefused(
            Refusal.SNAPSHOT_LISTING_FAILED,
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
            Refusal.SNAPSHOT_LISTING_FAILED,
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
    pull_share: bool = True,
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

    ``pull_share`` is for the one caller that already knows it will not spend the
    database half, the bare metal recovery of a library whose database was never
    on the lost volume. An outside share rides that half, so with this off it is
    WITHHELD and the remote is not asked about it: a listing that fails refuses
    the plan, and refusing a recovery of the music over a share nobody was going
    to pull is a refusal with no reason behind it.

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
            pull_share=pull_share,
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
    pull_share: bool,
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
                # THE BACKUP MIRROR'S OWN EXCLUDES, the database fileset
                # included. A mirror taken before that exclusion existed can
                # still hold the database, and landing it here puts a file where
                # the database half writes, which a bare-metal rerun refuses as
                # an occupied target (R-592). The database comes from the
                # snapshot and nowhere else.
                argv=(
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(_mirror_excludes(cfg)),
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
    # NOT UNDER THE ANALYSIS WATCH. A restore onto the live library runs inside a
    # session that fingerprints every analysis file under the library root and
    # the live share, and refuses at its close when one appeared or changed.
    # Driven on 2026-09-20: a share pulled there ended the restore refused as
    # moved analysis files, after the database had already been replaced. So a
    # landing place the watch covers is WITHHELD, said on the plan, and the
    # remote is not asked a question whose answer could change nothing. The
    # share comes back through a restore that names a target, which is also the
    # one restore that lands this layout's database where the person chose.
    #
    # WHOSE SHARE: the library the snapshot's marker names. An unmarked snapshot
    # falls back to this configuration's identity, because a marker that failed
    # to write is a warning and the same run still mirrored the share under it.
    share = ShareRestore.MIRRORED
    if _outside_share(cfg) is not None:
        landing = database_target.parent / analysis_store.SHARE_DIRNAME
        whose = resolved.recorded_volume or cfg.library.volume_id
        if not pull_share or analysis_store.is_watched(cfg, landing):
            share = ShareRestore.WITHHELD
        elif share_is_held(cfg, identity=whose, runner=runner):
            share = ShareRestore.PULLED
            commands.append(
                Command(
                    label=RESTORE_SHARE,
                    argv=(
                        rclone, "copy",
                        f"{share_destination(cfg, identity=whose)}/current",
                        str(landing),
                        "--transfers", "8", "--checkers", "16",
                    ),
                )
            )
        else:
            share = ShareRestore.ABSENT
    return RestorePlan(
        target=target,
        database_target=database_target,
        snapshot=chosen,
        clears=clears,
        commands=tuple(commands),
        absent_sidecars=tuple(absent),
        recorded_volume=resolved.recorded_volume,
        share=share,
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


def _listed(command: Command) -> dict[str, int]:
    """How many paths a command read on standard input, never the paths.

    A quick run can list thousands, and the report names the count and leaves
    the paths to the record.
    """
    if command.feed is None:
        return {}
    return {"paths": len(backup_record.paths_from(command.feed))}


def _kind_fields(kind: str, why: str, changes: Mapping[str, int] | None) -> dict:
    return {
        "kind": kind or None,
        "why": why or None,
        "changes": dict(changes) if changes is not None else None,
    }


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
                    {"label": c.label, "argv": list(c.argv), **_listed(c)}
                    for c in entry.commands
                ],
                "warnings": [dict(warning) for warning in entry.warnings],
                **_kind_fields(entry.kind, entry.why, entry.changes),
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
                # R-757. None for a portion that ran no mirror. A field that
                # joins, so ``PAYLOAD_VERSION`` stays for the reason above.
                "comparison": (
                    dict(entry.comparison) if entry.comparison is not None else None
                ),
                # R-349. STRICT, because ``run_backup`` builds both from the same
                # runner calls, and a mismatch would pair a return code with the
                # wrong argv, which is worse than printing neither.
                "commands": [
                    {
                        "label": command.label,
                        "argv": list(command.argv),
                        "returncode": result.returncode,
                        **_listed(command),
                    }
                    for command, result in zip(entry.commands, entry.results, strict=True)
                ],
                # U317. Fields that join, so ``PAYLOAD_VERSION`` stays.
                **_kind_fields(entry.kind, entry.why, entry.changes),
                "seconds": entry.seconds,
            }
            for entry in outcome.portions
        ],
    }


__all__ = [
    "BACKUP_RECORD_NOT_KEPT",
    "COMPARISON_FAST",
    "COMPARISON_FULL",
    "COMPARISON_QUICK",
    "DEFAULT_ARCHIVE_KEEP",
    "FAST_LIST",
    "MIRROR",
    "MIRROR_STATS_ARGS",
    "PAYLOAD_VERSION",
    "QUICK_ARCHIVE",
    "QUICK_LABELS",
    "QUICK_RESEND",
    "QUICK_SEND",
    "KINDS",
    "KIND_FULL",
    "KIND_QUICK",
    "KIND_SKIPPED",
    "KIND_SNAPSHOT",
    "KIND_UNCHANGED",
    "RECORD_TOKEN",
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
    "ShareRestore",
    "absent_analysis_share",
    "comparison_mode",
    "comparison_report",
    "database_fileset",
    "database_target_for",
    "dry_run_argv",
    "latest_snapshot",
    "plan_backup",
    "snapshot_filenames",
    "plan_payload",
    "plan_restore",
    "outcome_payload",
    "quick_report",
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
