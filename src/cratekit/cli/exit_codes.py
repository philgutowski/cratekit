"""The reservation table: every module refusal cause, its exit code, its remedy.

S4 applied to the standalone utilities. ``core.exit_codes`` names the statuses and
``core.cause`` closes the registry of reasons a CORE failure may carry. Neither
can see the causes a toggleable feature module raises, because a core module may
never import one, and a refusal nobody reserved a code for reaches the process
boundary as a bare non-zero integer with its remediation discarded. That is the
collapse KTD25 exists to prevent, one layer further out.

**Why this table lives under ``cli`` and is ranked FOUNDATION.** It has to see
what the feature modules raise, so it cannot live in ``core``. It must be
readable by everything, so it cannot rank above the layers that consume it.
``tests/test_layering.py`` already places this module, alongside the output
envelope, at foundation rank for exactly that reason. The consequence is a hard
one and it is the point: this file NAMES no module, IMPORTS no module, and knows
its subjects only as strings.

**Reserved by cause STRING, never by enum identity.** A cause slug is persisted
inside a stored cause and crosses a process boundary when the job engine
re-invokes the command line, so the slug is the stable key and the enum is one
module's spelling of it. Keying on the enum would also mean importing the module,
which the paragraph above forbids.

**Two tables that agree wherever they are SPELLED the same.**
``core.cause.REASONS`` is the other mapping in this repository that gives a slug
a code, and a second opinion that drifts is worse than no opinion at all. So the
overlap is not avoided, it is ASSERTED: where a slug appears in both,
``tests/test_reserved_causes.py`` requires the same code from both, and the same
suite forbids any third file in the package from mapping a reserved cause to a
code at all.

That check compares SPELLING and not meaning, which is a real limit and is
written down rather than implied. Today the identical spelling is one slug,
``rekordbox-running``. Two more conditions are spelled twice: this table's
``library-root-absent`` is the registry's ``library-directory-missing``, and this
table's ``database-absent`` is its ``library-database-missing``. Both pairs
happen to agree on 22 and a test asserts that pair by pair, but the overlap check
cannot see them, because a slug is persisted inside a stored cause and renaming
one is a breaking change to anything holding it. So the duplication stays and is
recorded, rather than being tidied away at the cost of a stored cause that no
longer resolves.

**Several causes share a code, and that is correct.** ``REASONS`` makes this
argument at length and it holds here: what a person needs kept apart is the
SENTENCE, which the slug carries, not the integer, which only has to classify.
So the table's length is asserted against its distinct CAUSES and never against
its distinct codes. The reservations are declared as a TUPLE and indexed at
import for the same reason ``cli.registry`` declares its entries as one: a
duplicate key in a dict literal is resolved silently by whichever line comes
last, and a tuple keeps both so the count can see it.

**The reserved range is 10 through 59, and nothing else.** That is the five
non-process bands: gate, library, installation, upstream, lifecycle. 0 is
success, 1 is a defect, and 2 belongs to the argument parser and to nothing else,
so the process band is closed to a refusal cause. 60 through 63 is the growth
room a class nobody has met yet will claim, so it is closed too. Everything at or
above ``MAX_CODE`` is closed because the shell already owns it: 126 means not
executable, 127 means not found, 128 plus a signal number covers 129 to 192 on a
platform whose real-time signals run to a ``SIGRTMAX`` of 64, and 255 is what a
status above a byte truncates to. A caller reading a status can therefore always
tell a Cratekit refusal from the shell reporting on Cratekit. ``_index`` enforces
every clause of that at import, so a reservation outside the range cannot even
load.

That last property is about a SHELL, and the other reader of these statuses is
not one. The job engine re-invokes the command line through ``subprocess`` and
reads ``returncode``, which on POSIX is the NEGATIVE signal number when a child
is killed by a signal, never 128 plus it. Both readings are safe against this
range, and neither is safe by accident: nothing reserved here is negative and
nothing reserved here is at or above 126.

**One key space, and six of its keys are remediation tokens.** Most reserved keys
are refusal CAUSES. Six are also canonical ``Remedy`` values.
``repair-backup-facts`` and ``upgrade-cratekit`` are, because
``core.backup_facts`` models its unreadable fact file as a choice of remedy
rather than a choice of cause: one file, one diagnosis, two fixes.
``install-binary``, ``install-binary-source-unknown``, ``fix-binary-override``
and ``unsupported-platform`` are, because ``core.binaries`` does the same for a
program that is missing, unusable, or unpackaged on this platform. The guard is
that any key which is also a canonical ``Remedy`` value must reserve THAT token.

**``upgrade-cratekit`` is one symbol with two meanings and this table holds one.**
Three enums declare it: ``backup_facts.Remedy``, ``config.Remedy`` and the
canonical ``exit_codes.Remedy``. A FACT FILE written by a newer build is an
acknowledgment gate that cannot be satisfied, which is 32 and is what the entry
below reserves. A CONFIGURATION file written by a newer build is
``config-unusable``, which ``core.cause`` reserves at 30 and which the
command-line boundary already converts to. A flat key space keyed on a slug
cannot hold both, so this is a limit of the shape rather than evidence that the
second meaning is not real, and ``tests/test_reserved_causes.py`` pins both
readings so neither can quietly become the other. Resolving it means keying on
more than a slug, or retiring one spelling, and both are a migration rather than
a tidy-up because a slug is persisted inside a stored cause.

**``core.config`` and ``acquire.adapter`` are excluded BY NAME.** Both declare a
per-raise ``Remedy | None`` override on their base exception, so both have the
shape the completeness walk hunts for, and both are listed in
``CONVERTED_ELSEWHERE`` in the suite together with the conversion that already
gives them a code and a token: config at the command-line boundary, the adapter
inside the acquisition layer that folds its failures into a run outcome. The
suite proves each claim against the tree rather than accepting it. Neither is
excluded any longer by the accident of an annotation the walk could not read,
which is how both were excluded before and which meant one unrelated tightening
would have flipped the result.

``core.secrets`` is a different case and is deliberately not in that list. It
carries its remedy as a CLASS attribute and subclasses per meaning, so its
structured cause really is the exception TYPE and no constructor parameter names
one. Its conversion is also narrower than the earlier argument here claimed:
exactly one caller converts it, and every other path reaches ``except Exception``
and becomes ``internal-error``. That is recorded in
``docs/residual-findings.md`` rather than assumed away.

**Nothing in ``src/`` reads this table yet.** It is a RESERVATION and not a
wiring. Every cause below still reaches ``except Exception`` in ``cratekit.cli``
today and exits 1 carrying ``report-defect``. Read this file as what a refusal is
OWED, not as what it currently does.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from cratekit.core.cause import Remediation
from cratekit.core.exit_codes import MAX_CODE, ExitCode, Remedy, band_of, meaning_of

#: The half-open range a reserved cause may draw its code from. See the module
#: docstring: the process band below and the growth band above are both closed,
#: and everything the shell owns sits at or above ``MAX_CODE``.
RESERVED_RANGE: tuple[int, int] = (10, 60)

#: The bands that range spans, by name, so a failure says which classification
#: was violated rather than only which integer.
RESERVED_BANDS: frozenset[str] = frozenset(
    {"gate", "library", "installation", "upstream", "lifecycle"}
)


class UnreservedCause(KeyError):
    """A structured refusal cause reached the boundary with no reserved code.

    Raised by name rather than collapsed into a generic failure, because the
    whole defect this table prevents is a refusal arriving as a bare status with
    nothing left to say. A caller that meets this has found a module raising a
    cause nobody reserved, and the fix is one entry here.
    """


@dataclass(frozen=True, slots=True)
class Reservation:
    """One refusal cause, the status it exits with, and what to do about it.

    ``remedy`` is a token and ``steps`` are sentences, exactly as
    ``core.cause.Remediation`` splits them, and at least one of the two must say
    something. A token is preferred whenever one fits, because the token is what
    survives a process boundary and what the renderer turns into a command. A
    sentence is used where no token fits, which is better than reaching for the
    nearest token and telling a person to do something that will not help.

    ``note`` says why THIS code and not its neighbour. It is the field a reviewer
    reads when two causes share a code and one of them looks wrong.
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
    # ``core.binaries.BinaryNotFound`` carries one of these four as its
    # structured cause. All four are 3x: the library is fine and nothing
    # upstream refused, this machine is missing a program or points at the wrong
    # one. None of them is 31, because that code means an optional dependency
    # GROUP is uninstalled, which is a packaging fact and a different fix.
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
    # ``core.backup_facts.BackupFactsUnreadable`` carries a REMEDY as its
    # structured cause rather than a refusal slug, because one diagnosis, an
    # unreadable fact file, has two fixes. Both reserve 32, which is the code
    # ``core.cause`` already gives ``backup-facts-unreadable`` and the code
    # ``core.session`` already exits with when the ages an acknowledgment must
    # show cannot be read. Agreeing with the landed conversion is the whole
    # point of reserving these at all.
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
    # THE THIRD MEMBER OF THE SAME FAMILY, reserved at the U27 merge on
    # 2026-08-15. U27 added GRANT_PATH_ACCESS to backup_facts.Remedy so that a
    # directory this account cannot open stops being reported as a damaged fact
    # file, which is the correction the raise site's own comment explains at
    # length. U27's branch was cut before U38 landed this registry, so its new
    # remedy never had to be reserved on either side and only the merged tree can
    # see the obligation.
    #
    # 32 IS MEASURED RATHER THAN CHOSEN, which is what this table's rule asks:
    # agree with the landed conversion. Both siblings above answer 32, and the
    # code has not moved since.
    #
    # WHAT MOVED IS THE REASON, and it is worth saying because the number stayed
    # the same while the argument under it was replaced. This note used to
    # measure 32 from a defect: core.session caught every BackupFactsUnreadable
    # at one site and re-raised it naming REPAIR_BACKUP_FACTS without reading the
    # exception's own remedy at all, so grant-path-access never reached a
    # refusal from that path and the only landed answer was its siblings'. U48
    # closed that on 2026-09-02: the session now carries the exception's remedy
    # the way cli.doctor and the backup shell already did, so this token is
    # reachable from three consumers rather than two. It still answers 32,
    # because the siblings that decided the number are unchanged.
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
        cause="rekordbox-running",
        code=ExitCode.REKORDBOX_OPEN,
        remedy=Remedy.QUIT_REKORDBOX,
        note=(
            "the one slug this table shares with the closed reason registry, "
            "and it reserves the identical code there. A copy taken under a "
            "live application opens cleanly and is silently missing whatever "
            "was mid-write, which is worse than no copy"
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
            "no dated database snapshot exists for this library yet; take a "
            "backup before a restore can be planned",
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
    # Six of the seven are 30. That is not laziness: a set recording named on
    # the command line, the container it is in, and the archive slot beside it
    # are all preconditions THIS verb declares, and each is undone by a
    # different act. The slug is what keeps them apart where it is read, which
    # is the envelope, and the integer only has to classify.
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

    Enforced at IMPORT rather than only in a test, for the reason
    ``cli.registry`` gives for the same choice: a duplicate that only a test
    catches is a duplicate that ships to anyone who runs the code without the
    suite. The duplicate check works because ``RESERVATIONS`` is a tuple; the
    same entries written as a dict literal would have collapsed at parse time
    and there would be nothing left to count.
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
        # THE NEXT TWO ARE UNREACHABLE TODAY and are kept deliberately. The range
        # check above already excludes every code outside a reserved band and
        # every code no verb may return, so deleting either of these kills no
        # test and changes no behaviour. They stay because each states a
        # DIFFERENT rule from the range: the range is a span of integers and
        # these two are about what the span means, so a band renumbered or a
        # meaning changed to non-producible fails by name here rather than
        # passing because the arithmetic still happens to hold. A reader should
        # take them as defence in depth, not as live paths. See the residual
        # "One check in this unit is unreachable" in
        # ``docs/residual-findings.md``.
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

    The naming is the requirement. A lookup that returned a default code would
    turn an unreserved cause into a plausible status, which is indistinguishable
    from a reserved one and is precisely the collapse this table exists to stop.
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
