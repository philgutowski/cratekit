"""The reservation table: every module refusal cause, its exit code, its remedy.

``core.cause`` cannot see what a feature module raises, so an unreserved refusal
would reach the boundary as a bare status with its remediation lost (KTD25). This
module sits at foundation rank under ``cli``, names and imports no module, and
keys every reservation by cause STRING, because the slug is what a stored cause
persists. Where a slug is also in ``core.cause.REASONS`` the two must agree, and
``tests/test_reserved_causes.py`` asserts it. Several causes may share a code,
since the slug carries the sentence. Codes are drawn only from 10 through 59, so a
refusal is never confused with success, a defect, the parser's 2, the growth band
or the shell's own statuses, and ``_index`` enforces that at import. Nothing in
``src/`` reads this table yet: it records what a refusal is owed.

Two readers see these statuses. A shell owns 126 and above (not executable, not
found, 128 plus a signal, and 255 for a status above a byte); the job engine
reads ``subprocess.returncode``, which is the NEGATIVE signal number for a child
killed by a signal. Both are safe because nothing reserved here is negative and
nothing is at or above 126.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from cratekit.core.cause import Remediation
from cratekit.core.exit_codes import MAX_CODE, ExitCode, Remedy, band_of, meaning_of

#: The half-open range a reserved cause may draw its code from.
RESERVED_RANGE: tuple[int, int] = (10, 60)

#: The bands that range spans, by name, so a failure names the classification.
RESERVED_BANDS: frozenset[str] = frozenset(
    {"gate", "library", "installation", "upstream", "lifecycle"}
)


class UnreservedCause(KeyError):
    """A structured refusal cause reached the boundary with no reserved code.

    Raised by name so the refusal never collapses into a bare status; the fix is
    one entry in ``RESERVATIONS``.
    """


@dataclass(frozen=True, slots=True)
class Reservation:
    """One refusal cause, the status it exits with, and what to do about it.

    ``remedy`` is a token and ``steps`` are sentences, as ``Remediation`` splits
    them, and at least one must be set. Prefer a token, since it survives a
    process boundary; use steps where no token fits rather than a wrong one.
    ``note`` says why this code and not its neighbour.
    """

    cause: str
    code: ExitCode
    note: str
    remedy: Remedy | None = None
    steps: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.remedy is None and not self.steps:
            raise ValueError(
                f"{self.cause!r} reserves a code and no remediation. A refusal "
                f"with nothing to do about it is the bare status this table "
                f"exists to replace."
            )

    def remediation(self) -> Remediation:
        """The remediation a cause built from this reservation carries."""
        return Remediation(remedy=self.remedy, steps=self.steps)


RESERVATIONS: tuple[Reservation, ...] = (
    # ── The external programs this installation depends on ──────────────────
    #
    # ``core.binaries.BinaryNotFound`` carries one of these four. All are 3x,
    # this machine lacks a program, and none is 31, which means an uninstalled
    # optional dependency group.
    Reservation(
        cause="install-binary",
        code=ExitCode.PRECONDITION,
        remedy=Remedy.INSTALL_BINARY,
        note="a program a verb declares as a prerequisite is not on this machine",
    ),
    Reservation(
        cause="install-binary-source-unknown",
        code=ExitCode.PRECONDITION,
        remedy=Remedy.INSTALL_BINARY_SOURCE_UNKNOWN,
        note=(
            "same condition as the entry above, and a separate slug because the "
            "instruction differs: this platform has no packaged source, so the "
            "person installs it themselves and points at it"
        ),
    ),
    Reservation(
        cause="fix-binary-override",
        code=ExitCode.PRECONDITION,
        remedy=Remedy.FIX_BINARY_OVERRIDE,
        note=(
            "the configured override names something that is not a usable "
            "program; installing again would fix nothing, which is why this is "
            "not the install slug"
        ),
    ),
    Reservation(
        cause="unsupported-platform",
        code=ExitCode.PRECONDITION,
        remedy=Remedy.UNSUPPORTED_PLATFORM,
        note=(
            "the operation has no implementation for this operating system; "
            "still 3x because it is this installation refusing, not the library"
        ),
    ),
    # ── The recorded backup facts ───────────────────────────────────────────
    #
    # ``BackupFactsUnreadable`` carries a REMEDY, since one diagnosis has
    # several fixes. All reserve 32, agreeing with ``core.cause`` and
    # ``core.session``.
    Reservation(
        cause="repair-backup-facts",
        code=ExitCode.ACK_REQUIRED,
        remedy=Remedy.REPAIR_BACKUP_FACTS,
        note=(
            "the fact file is present and unintelligible, so the gate that has "
            "to show a backup age cannot be satisfied until the file is repaired"
        ),
    ),
    Reservation(
        cause="upgrade-cratekit",
        code=ExitCode.ACK_REQUIRED,
        remedy=Remedy.UPGRADE_CRATEKIT,
        note=(
            "same file and same gate, written by a newer build. Repairing it by "
            "hand would discard a record this build cannot read but the newer "
            "one can, so the fix is the newer build and not the repair"
        ),
    ),
    # 32, measured from its siblings rather than chosen (U27, U48).
    Reservation(
        cause="grant-path-access",
        code=ExitCode.ACK_REQUIRED,
        remedy=Remedy.GRANT_PATH_ACCESS,
        note=(
            "the fact file may be perfectly intact and unreachable, so the gate "
            "that has to show a backup age cannot be satisfied until the account "
            "can open the path. Repairing or resetting the record is the wrong "
            "act and destroys library state to answer a question nobody asked"
        ),
    ),
    # ── The backup module's refusals ────────────────────────────────────────
    Reservation(
        cause="rclone-missing",
        code=ExitCode.PRECONDITION,
        remedy=Remedy.INSTALL_BINARY,
        note=(
            "the same condition as install-binary, re-raised in the backup "
            "module's own vocabulary so a caller has one failure type to read "
            "rather than two. Deliberately the SAME code and the SAME token: a "
            "second answer for one situation is the drift this table prevents"
        ),
    ),
    Reservation(
        cause="remote-not-configured",
        code=ExitCode.PRECONDITION,
        remedy=Remedy.RUN_SETUP,
        note=(
            "no destination account is recorded, and none is ever defaulted "
            "because the account belongs to the user; setup is where it is given"
        ),
    ),
    Reservation(
        cause="destination-not-configured",
        code=ExitCode.PRECONDITION,
        remedy=Remedy.RUN_SETUP,
        note=(
            "the remote is named and one of the three places under it is not; "
            "same class and same fix as the entry above, and a separate slug "
            "because the sentence names which of the three is unset"
        ),
    ),
    Reservation(
        cause="library-root-absent",
        code=ExitCode.LIBRARY_UNAVAILABLE,
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
        note=(
            "the configured library root is not a directory, which on a library "
            "that lives on an external volume almost always means unmounted"
        ),
    ),
    Reservation(
        cause="library-root-foreign",
        code=ExitCode.LIBRARY_UNAVAILABLE,
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
        note=(
            "The root is a directory on a volume other than the one "
            "recorded for this library, so mirroring it would empty the remote "
            "into the archive to match. The same class and fix as the absent "
            "root above, and its own slug because the root is there"
        ),
    ),
    Reservation(
        cause="library-root-unproven",
        code=ExitCode.LIBRARY_UNAVAILABLE,
        steps=(
            "mount the library's volume and run the backup again: the folder at "
            "the library root holds none of the library's files, or under a "
            "tenth of what the last backup held, which is what an unmounted "
            "volume leaves",
            "if the library was emptied on purpose, back it up with "
            "crate backup run --library-emptied",
        ),
        note=(
            "Steps rather than the mount token, because a library its "
            "owner emptied has a second way out the token cannot say, and "
            "nothing in the vocabulary says it"
        ),
    ),
    Reservation(
        cause="rekordbox-running",
        code=ExitCode.REKORDBOX_OPEN,
        remedy=Remedy.QUIT_REKORDBOX,
        note=(
            "a slug this table shares with the closed reason registry, "
            "and it reserves the identical code there. A copy taken under a "
            "live application opens cleanly and is silently missing whatever "
            "was mid-write, which is worse than no copy"
        ),
    ),
    Reservation(
        cause="rekordbox-absence-unconfirmed",
        code=ExitCode.REKORDBOX_OPEN,
        remedy=Remedy.RETRY_LATER,
        note=(
            "U211. A live process the scan could not read, so whether rekordbox "
            "is closed was not established; shared with the closed reason "
            "registry at the identical code. The database portion refuses "
            "alone and the files still mirror, as with rekordbox running, and "
            "the remedy is waiting for the process to finish exiting"
        ),
    ),
    Reservation(
        cause="database-absent",
        code=ExitCode.LIBRARY_UNAVAILABLE,
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
        note=(
            "nothing is at the configured database path. Same code as the root "
            "being absent because the class of answer is the same, and its own "
            "slug because the file portion of a backup can still run"
        ),
    ),
    Reservation(
        cause="restore-not-confirmed",
        code=ExitCode.DECISION_REQUIRED,
        remedy=Remedy.ANSWER_DECISION,
        note=(
            "a restore replaces a live database, so it is a gate rather than a "
            "failure: the state is resumable and the run continues once the "
            "decision naming this library and this snapshot is supplied"
        ),
    ),
    Reservation(
        cause="restore-target-absent",
        code=ExitCode.LIBRARY_UNAVAILABLE,
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
        note=(
            "the directory the restore would write into does not exist; the "
            "same volume-shaped fix as the two entries above, and never 2, "
            "because the argument parser owns 2 and the path parsed fine"
        ),
    ),
    Reservation(
        cause="no-snapshot-available",
        code=ExitCode.PRECONDITION,
        steps=(
            "when --snapshot named a stamp, that snapshot or its database "
            "folder is not on the remote; check the stamp, or leave the flag "
            "off to take the newest",
            "otherwise no dated database snapshot exists for this library yet; "
            "take a backup before a restore can be planned",
        ),
        note=(
            "steps rather than a token, because no token in the vocabulary says "
            "this and the nearest one would send a person to list snapshots "
            "that are not there. A sentence beats a plausible wrong command"
        ),
    ),
    Reservation(
        cause="snapshot-listing-failed",
        code=ExitCode.PRECONDITION,
        steps=(
            "check the backup remote is reachable from this machine; the snapshot "
            "is not known to be missing, a listing of it failed",
            "check the remote's credential has not expired or been revoked, and "
            "reconnect it in rclone if it has",
            "check backup.db_dest_root names the folder the backups were written "
            "to, then retry the restore; nothing was pulled or cleared",
        ),
        note=(
            "its own slug rather than no-snapshot-available, whose step is "
            "to take a backup: a person who followed that here would take a new "
            "snapshot beside the one they already have and leave the remote, the "
            "credential or the path that actually failed untouched"
        ),
    ),
    # ── Snapshot provenance: a pulled snapshot is a stamp, and this library's ─
    Reservation(
        cause="snapshot-name-invalid",
        code=ExitCode.PRECONDITION,
        steps=(
            "give --snapshot the dated folder name a backup wrote, and nothing "
            "else; leave the flag off to take the newest snapshot",
        ),
        note=(
            "NOT 2. The parser accepted the value, because any string is a valid "
            "argument to a flag that takes one. Steps rather than a token, since "
            "no token says retype a stamp"
        ),
    ),
    Reservation(
        cause="snapshot-library-mismatch",
        code=ExitCode.PRECONDITION,
        steps=(
            "name a snapshot that was taken from this library with --snapshot",
            "when the snapshot IS this library's, taken before its drive was "
            "replaced, say so by passing the volume the refusal names as "
            "--snapshot-volume; it is checked, used once and never recorded",
        ),
        note=(
            "the second step hands a value over, and it is safe to for a reason "
            "worth keeping: the value is read from the snapshot's own marker "
            "rather than from whatever disk is mounted, following the step "
            "changes no configuration, and the flag enters the confirmation "
            "digest, so the person approves the volume they named"
        ),
    ),
    Reservation(
        cause="snapshot-identity-unrecorded",
        code=ExitCode.PRECONDITION,
        steps=(
            "when the snapshot the refusal names is this library's, pull it by "
            "naming it with --snapshot",
            "otherwise take a backup, after checking library.volume_id is the "
            "volume's own identity, a plain UUID or serial; a snapshot says which "
            "library it was taken from only when that identity can be a filename",
        ),
        note=(
            "every snapshot taken before the identity marker existed lands here "
            "when it is the newest, so the first step has to work with no new "
            "backup: a person whose drive just died cannot take one"
        ),
    ),
    # ── The mastering module's refusals ─────────────────────────────────────
    #
    # Most are 30: each is a precondition this verb declares, undone by a
    # different act, and the slug keeps them apart.
    Reservation(
        cause="source-missing",
        code=ExitCode.PRECONDITION,
        steps=("name a recording that exists; nothing was read and nothing was written",),
        note=(
            "the recording named does not exist. NOT 2: the command line parsed "
            "perfectly and the parser owns that integer, which is the whole "
            "durability of the KTD25 fix"
        ),
    ),
    Reservation(
        cause="source-unsupported",
        code=ExitCode.PRECONDITION,
        steps=("convert the recording to a container this reads, or name a different file",),
        note=(
            "the file is there and is not a container this reads. Its own slug "
            "rather than the missing one, because a person told the file is "
            "absent will go looking for a file that is sitting in front of them"
        ),
    ),
    Reservation(
        cause="output-exists",
        code=ExitCode.PRECONDITION,
        steps=(
            "move or rename the existing master, or ask for the overwrite explicitly",
        ),
        note=(
            "refusing to replace a master that may already have been kept, and "
            "whose settings are recorded nowhere. A refusal to destroy, so it "
            "is a precondition rather than a policy violation"
        ),
    ),
    Reservation(
        cause="archive-holds-a-different-recording",
        code=ExitCode.PRECONDITION,
        steps=(
            "the archive slot for this name already holds different audio; "
            "rename the source or clear the slot by hand",
        ),
        note=(
            "the source archive is the only untouched copy, so a name collision "
            "is never resolved by guessing which recording is wanted"
        ),
    ),
    Reservation(
        cause="archive-verify-failed",
        code=ExitCode.PRECONDITION,
        steps=(
            "the archived copy does not match the source; check the destination "
            "disk before retrying, because the source has not been touched",
        ),
        note=(
            "NOT 1. A verify failure is usually a disk, not a defect in this "
            "program, and telling a person to report a bug for a failing drive "
            "sends them to the one place that cannot help"
        ),
    ),
    Reservation(
        cause="restore-transfer-failed",
        code=ExitCode.PRECONDITION,
        steps=(
            "the restore's transfer failed part way; check the remote is "
            "reachable and run the restore again before opening the library, "
            "because the live companion files were cleared and not put back",
        ),
        note=(
            "NOT 1, for the reason archive-verify-failed is not 1: an "
            "unreachable remote or an expired token is a condition of the world "
            "rather than a defect in this program, and report-defect sends a "
            "person to the one place that cannot help. STEPS rather than a "
            "token, because no token in the vocabulary says the thing that "
            "actually matters here, which is that the library is mid restore and "
            "must not be opened until one succeeds"
        ),
    ),
    Reservation(
        cause="encoder-missing",
        code=ExitCode.PRECONDITION,
        remedy=Remedy.INSTALL_BINARY,
        note=(
            "the same condition as install-binary, re-raised in the mastering "
            "module's vocabulary, exactly as rclone-missing is in the backup "
            "module's. One situation, one code, one token, three spellings"
        ),
    ),
    Reservation(
        cause="encoder-failed",
        code=ExitCode.PRECONDITION,
        steps=(
            "the encoder rejected this recording; its own message is on the "
            "cause, and the source file is unchanged",
        ),
        note=(
            "the program is installed and returned a failure. Its own slug "
            "rather than the missing one because installing it again fixes "
            "nothing, and not an upstream code because nothing here is remote"
        ),
    ),
)


def _index(reservations: tuple[Reservation, ...]) -> Mapping[str, Reservation]:
    """Index the reservations by cause, refusing anything the range forbids.

    Enforced at import so a duplicate never ships without the suite; it is
    countable only because ``RESERVATIONS`` is a tuple.
    """
    index: dict[str, Reservation] = {}
    low, high = RESERVED_RANGE
    for reservation in reservations:
        if reservation.cause in index:
            raise ValueError(
                f"{reservation.cause!r} is reserved twice. Two reservations for "
                f"one cause means the later one silently wins, and which one is "
                f"later is a property of line order rather than of intent."
            )
        if not isinstance(reservation.code, ExitCode):
            raise ValueError(
                f"{reservation.cause!r} reserves {reservation.code!r}, which is "
                f"not a member of the one status vocabulary. A bare integer here "
                f"is the same second opinion the guards forbid elsewhere, and it "
                f"is refused by name rather than by an attribute error while this "
                f"module was trying to describe it."
            )
        value = int(reservation.code)
        if not low <= value < high:
            raise ValueError(
                f"{reservation.cause!r} reserves {reservation.code.name}={value}, "
                f"outside the reserved range {low} to {high - 1}. Below it is the "
                f"process band, where 0 is success, 1 is a defect and 2 belongs "
                f"to the argument parser; at or above {MAX_CODE} is the shell's "
                f"own territory."
            )
        # Unreachable today, kept as defence in depth: these state what the
        # range means, so a renumbered band fails by name. See the residual
        # "One check in this unit is unreachable".
        band = band_of(reservation.code)
        if band.name not in RESERVED_BANDS:
            raise ValueError(
                f"{reservation.cause!r} reserves a code in the {band.name!r} "
                f"band, which is not one a refusal cause may draw from."
            )
        if not meaning_of(reservation.code).verb_producible:
            raise ValueError(
                f"{reservation.cause!r} reserves {reservation.code.name}, which "
                f"no verb may ever return."
            )
        index[reservation.cause] = reservation
    return MappingProxyType(index)


#: cause slug -> its reservation. The mapping every consumer reads.
RESERVED_CAUSES: Mapping[str, Reservation] = _index(RESERVATIONS)


def reserved(cause: str) -> Reservation:
    """The reservation for a cause, or a refusal that NAMES the missing cause.

    A default code would pass an unreserved cause off as a reserved one.
    """
    try:
        return RESERVED_CAUSES[str(cause)]
    except KeyError:
        raise UnreservedCause(
            f"{str(cause)!r} has no reserved exit code. A module is raising a "
            f"structured refusal that nothing downstream can classify, so it "
            f"would arrive as a bare status with its remediation discarded. "
            f"Add it to cratekit.cli.exit_codes.RESERVATIONS."
        ) from None


def code_for(cause: str) -> ExitCode:
    """The status a refusal carrying this cause exits with."""
    return reserved(cause).code


def remediation_for(cause: str) -> Remediation:
    """The remediation a refusal carrying this cause travels with."""
    return reserved(cause).remediation()


__all__ = [
    "RESERVATIONS",
    "RESERVED_BANDS",
    "RESERVED_CAUSES",
    "RESERVED_RANGE",
    "Reservation",
    "UnreservedCause",
    "code_for",
    "remediation_for",
    "reserved",
]
