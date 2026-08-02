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

**Two tables that cannot disagree.** ``core.cause.REASONS`` is the other mapping
in this repository that gives a slug a code, and a second opinion that drifts is
worse than no opinion at all. So the overlap is not avoided, it is ASSERTED:
where a slug appears in both, ``tests/test_reserved_causes.py`` requires the same
code from both, and the same suite forbids any third file in the package from
mapping a reserved cause to a code at all. Today the overlap is one slug,
``rekordbox-running``, and one is enough to prove the check works.

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
executable, 127 means not found, 128 plus a signal number covers 129 to 165, and
255 is what a status above a byte truncates to. A caller reading a status can
therefore always tell a Cratekit refusal from the shell reporting on Cratekit.
``_index`` enforces every clause of that at import, so a reservation outside the
range cannot even load.

**One key space, with one recorded asymmetry.** Most reserved keys are refusal
CAUSES. Two of them, ``repair-backup-facts`` and ``upgrade-cratekit``, are
remediation TOKENS, because ``core.backup_facts`` models its unreadable fact file
as a choice of remedy rather than a choice of cause: one file, one diagnosis, two
fixes. Folding them into one key space risks the worst defect a registry can
have, one symbol meaning two things, since ``upgrade-cratekit`` is also what
``core.config`` says about a file from a newer build. The guard is that any key
which is also a canonical ``Remedy`` value must reserve THAT token, so the symbol
keeps one meaning wherever it is read. The modules whose structured cause is
their exception TYPE rather than an enum member, ``core.config`` and
``core.secrets``, are deliberately outside this table: their conversion is
already declared, they already reach the command line carrying their own token,
and duplicating them here is how a second opinion starts.
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
        value = int(reservation.code)
        if not low <= value < high:
            raise ValueError(
                f"{reservation.cause!r} reserves {reservation.code.name}={value}, "
                f"outside the reserved range {low} to {high - 1}. Below it is the "
                f"process band, where 0 is success, 1 is a defect and 2 belongs "
                f"to the argument parser; at or above {MAX_CODE} is the shell's "
                f"own territory."
            )
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
