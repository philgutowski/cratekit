"""The one reserved exit-code vocabulary, and the remediation tokens beside it.

KTD25 asks for this BEFORE any verb ships, and the reason is in the source
system. It has three unrelated exit-code schemes, and the same integer means
different things in each:

* ``2`` from either master.db writer means "rekordbox is open", and its
  remediation is for the user to quit the application and retry.
* ``2`` from the sync orchestrator means "another run holds the lock", and its
  remediation is the opposite: quitting anything is wrong, and there is no
  command to run because that lock is deliberately not reclaimable.
* ``2`` from argparse means the command line was mistyped.

All three are reachable in one process today, because an argparse failure inside
a writer raises ``SystemExit``, which is a ``BaseException`` and escapes the
orchestrator's ``except Exception``. So the collision is not theoretical, and no
consumer can tell the three apart.

Three properties fix that here, and each is enforced by a test:

1. **One vocabulary, defined in the foundation layer**, so producers and
   consumers name the same constant. In the source, the only named exit constant
   lives in a CONSUMER; every producer writes a bare integer literal, which is
   why nothing detects a producer changing its code.
2. **2 belongs to argparse and no verb may ever return it.** That is the durable
   half of the fix: argparse will keep producing 2 whatever anyone decides, so
   the only way the collision cannot come back is for that integer to have
   exactly one owner and for the owner not to be us.
3. **Every code carries a remediation TOKEN, never the text a user types.**
   Rendering a token into a command is the CLI layer's job (D2), because the
   command depends on the platform, the package manager the user actually has,
   and the interface they are sitting in front of. A string baked in down here
   has already decided all three.

Layer note: this module is FOUNDATION. It names no verb, no module, and no
taxonomy term, and it imports nothing from Cratekit at all.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from types import MappingProxyType
from typing import Mapping

#: Nothing at or above this value is ever used. The shell reserves 126
#: (not executable), 127 (not found), and 128 plus the signal number, and a
#: process status is a single unsigned byte, so a code above 255 silently
#: truncates. Staying under 64 leaves both conventions untouched, which means a
#: caller reading a status can always tell a Cratekit refusal from the shell
#: reporting on Cratekit itself.
MAX_CODE = 64


class ExitCode(IntEnum):
    """Every status ``crate`` can exit with. Banded by tens, gapped for growth.

    A reader who meets an unfamiliar code can classify it from its tens digit
    without a lookup: 1x is a gate, 2x is the library's state, 3x is this
    installation's environment, 4x is something upstream, 5x is the run's
    lifecycle. That is the whole reason for the bands. New codes join a band and
    never reuse a retired value (see ``RETIRED``).
    """

    # ── 0 to 9: the process-level classes ────────────────────────────────────
    OK = 0
    INTERNAL = 1
    USAGE = 2

    # ── 1x: a gate was reached and could not be passed here ─────────────────
    DECISION_REQUIRED = 10
    DECISION_STALE = 11
    PENDING_HUMAN = 12

    # ── 2x: the LIBRARY's state refuses ─────────────────────────────────────
    LIBRARY_BUSY = 20
    REKORDBOX_OPEN = 21
    LIBRARY_UNAVAILABLE = 22
    VERSION_PIN = 23
    UNCONVERGED = 24
    LIBRARY_UNREADABLE = 25
    EXTERNAL_WRITER = 26
    LIBRARY_PREREQUISITE = 27

    # ── 3x: THIS INSTALLATION's environment refuses ─────────────────────────
    PRECONDITION = 30
    MODULE_UNAVAILABLE = 31
    ACK_REQUIRED = 32

    # ── 4x: something UPSTREAM of us refuses ────────────────────────────────
    UPSTREAM_AUTH = 40
    UPSTREAM_UNAVAILABLE = 41
    REFUSED_BY_POLICY = 42

    # ── 5x: the run's own lifecycle ─────────────────────────────────────────
    INTERRUPTED = 50


class Remedy(StrEnum):
    """What to do about a failure, as a token rather than as a command line.

    D2 in one sentence: the foundation names no verb, so remediation below the
    CLI is a token and only the CLI renders it into text a user types.

    The values are stable machine slugs and are persisted inside a cause, which
    crosses a process boundary when the job engine re-invokes the CLI (KTD26).
    Renaming one is a breaking change to anything holding a stored cause, so
    renames go through the same retirement discipline as an exit code.

    Several foundation modules declare their own subset of these for their own
    failures, because they landed before or beside this enum:
    ``cratekit.core.config``, ``cratekit.core.binaries``,
    ``cratekit.core.secrets``, ``cratekit.core.backup_facts`` and
    ``cratekit.acquire.adapter``. ``tests/test_cli_contract.py`` asserts every
    one of those stays a subset, so they cannot drift into several vocabularies
    for one idea, which is the drift KTD13 records in the taxonomy resolvers.

    That test used to name ``config`` alone, because config was the only such
    module on the day it was written. Four more landed and none of them was a
    subset: sixteen tokens existed that this enum had never heard of, so
    ``render`` matched none of them and fell through to the exit code's generic
    summary. A user told to set a credential read "an unexpected failure"
    instead. The test now DERIVES the module set by walking the package, per
    seam decision P3, because a test that enumerates is a test that misses the
    next addition, and this one already had.
    """

    # Configuration (the six ``config.Remedy`` already declares).
    RUN_SETUP = "run-setup"
    REPAIR_CONFIG_FILE = "repair-config-file"
    UPGRADE_CRATEKIT = "upgrade-cratekit"
    FIX_CONFIG_VALUES = "fix-config-values"
    RETRY_WHEN_UNLOCKED = "retry-when-unlocked"
    RECORD_REKORDBOX_PIN = "record-rekordbox-pin"

    # Process and command line.
    REPORT_DEFECT = "report-defect"
    FIX_COMMAND_LINE = "fix-command-line"

    # Gates.
    ANSWER_DECISION = "answer-decision"
    REPLAN_THEN_DECIDE = "replan-then-decide"
    COMPLETE_PENDING_ACTION = "complete-pending-action"

    # Library state.
    WAIT_FOR_HOLDER = "wait-for-holder"
    RELEASE_STALE_LOCK = "release-stale-lock"
    QUIT_REKORDBOX = "quit-rekordbox"
    MOUNT_LIBRARY_VOLUME = "mount-library-volume"
    # A path this account cannot reach, which is a DIFFERENT act from attaching a
    # drive: nothing is missing and nothing needs plugging in. On macOS an
    # interpreter without Full Disk Access is refused by the kernel for anything
    # under Documents, Desktop, Downloads or an external volume, and telling that
    # user to mount a volume that is already mounted is the collapse this
    # vocabulary exists to prevent.
    GRANT_PATH_ACCESS = "grant-path-access"
    REVALIDATE_PINS = "revalidate-pins"
    REBUILD_TREE = "rebuild-tree"
    RESTORE_FROM_SNAPSHOT = "restore-from-snapshot"
    DISABLE_CLOUD_SYNC = "disable-cloud-sync"
    PREPARE_LIBRARY_IN_REKORDBOX = "prepare-library-in-rekordbox"

    # This installation.
    RUN_DOCTOR = "run-doctor"
    INSTALL_MODULE_EXTRA = "install-module-extra"
    ACKNOWLEDGE_BACKUP = "acknowledge-backup"
    REPAIR_BACKUP_FACTS = "repair-backup-facts"

    # External binaries this installation depends on.
    INSTALL_BINARY = "install-binary"
    INSTALL_BINARY_SOURCE_UNKNOWN = "install-binary-source-unknown"
    FIX_BINARY_OVERRIDE = "fix-binary-override"
    UNSUPPORTED_PLATFORM = "unsupported-platform"

    # Credentials.
    SET_CREDENTIAL = "set-credential"
    INSTALL_KEYCHAIN_BACKEND = "install-keychain-backend"
    REPAIR_CREDENTIAL_STORE = "repair-credential-store"

    # Upstream.
    AUTHENTICATE_PROVIDER = "authenticate-provider"
    RETRY_LATER = "retry-later"
    CHANGE_POLICY_OR_INPUT = "change-policy-or-input"
    PAUSE_AND_CHECK_ACCOUNT = "pause-and-check-account"

    # The acquisition adapter (R9, KTD5).
    SWITCH_ADAPTER = "switch-adapter"
    INSTALL_ADAPTER = "install-adapter"
    CHOOSE_KNOWN_ADAPTER = "choose-known-adapter"
    REPAIR_ADAPTER_SETTINGS = "repair-adapter-settings"
    RELAX_LOSSLESS_POLICY = "relax-lossless-policy"

    # Re-authentication. THREE tokens sit close together here and that is
    # recorded rather than resolved: ``authenticate-provider`` (no credential
    # yet), ``reauthenticate`` (a stored credential the keychain rejected), and
    # ``reauthenticate-provider`` (a stored credential the PROVIDER rejected).
    # They may well be one idea, but each is already a persisted slug, and this
    # docstring says renaming one is a breaking change to anything holding a
    # stored cause. Collapsing them is a deliberate decision with a migration,
    # not a tidy-up.
    REAUTHENTICATE = "reauthenticate"
    REAUTHENTICATE_PROVIDER = "reauthenticate-provider"

    # Lifecycle.
    RESUME_JOB = "resume-job"


@dataclass(frozen=True, slots=True)
class Band:
    """One decade of the vocabulary, and the question its members answer."""

    start: int
    stop: int  # exclusive
    name: str
    question: str


BANDS: tuple[Band, ...] = (
    Band(0, 10, "process", "did the process itself work"),
    Band(10, 20, "gate", "was a decision or a human action outstanding"),
    Band(20, 30, "library", "does the state of the LIBRARY allow this"),
    Band(30, 40, "installation", "does the state of THIS INSTALL allow this"),
    Band(40, 50, "upstream", "did something outside us refuse"),
    Band(50, 60, "lifecycle", "how did this run end"),
    # 60 to 63 are deliberately unassigned: the growth room a new class claims
    # when no existing band fits. Everything at or above MAX_CODE stays free.
    Band(60, MAX_CODE, "unclaimed", "reserved for a class that has not appeared yet"),
)


@dataclass(frozen=True, slots=True)
class Meaning:
    """What one code means, and what the user does about it.

    ``verb_producible`` is False only for codes a verb must never return.
    Currently that is ``USAGE``, whose owner is argparse: the entire durability
    of the KTD25 fix rests on nothing of ours competing for that integer.
    """

    summary: str
    remedy: Remedy
    verb_producible: bool = True


#: One entry per member, looked up rather than derived, because the remediation
#: is a decision and not a function of the number. The test that asserts
#: completeness ITERATES ``ExitCode`` rather than listing members, so a code
#: added without a meaning fails the build instead of silently having none.
MEANINGS: Mapping[ExitCode, Meaning] = MappingProxyType(
    {
        ExitCode.OK: Meaning(
            "the verb completed; the envelope says whether work actually happened",
            Remedy.COMPLETE_PENDING_ACTION,
        ),
        ExitCode.INTERNAL: Meaning(
            "an unexpected failure; the envelope carries the cause chain",
            Remedy.REPORT_DEFECT,
        ),
        ExitCode.USAGE: Meaning(
            "the command line could not be parsed; owned by the argument parser",
            Remedy.FIX_COMMAND_LINE,
            verb_producible=False,
        ),
        ExitCode.DECISION_REQUIRED: Meaning(
            "a named gate was reached with no matching decision; state is resumable",
            Remedy.ANSWER_DECISION,
        ),
        ExitCode.DECISION_STALE: Meaning(
            "a decision was supplied but the artifact it was made against moved",
            Remedy.REPLAN_THEN_DECIDE,
        ),
        ExitCode.PENDING_HUMAN: Meaning(
            "the tool finished its half; a person has to complete an action off-tool",
            Remedy.COMPLETE_PENDING_ACTION,
        ),
        ExitCode.LIBRARY_BUSY: Meaning(
            "another destructive session holds the library lock",
            Remedy.WAIT_FOR_HOLDER,
        ),
        ExitCode.REKORDBOX_OPEN: Meaning(
            "the rekordbox application or its background agent is running",
            Remedy.QUIT_REKORDBOX,
        ),
        ExitCode.LIBRARY_UNAVAILABLE: Meaning(
            "the library volume is unmounted, is a different volume, or the "
            "database is not where the configuration says",
            Remedy.MOUNT_LIBRARY_VOLUME,
        ),
        ExitCode.VERSION_PIN: Meaning(
            "a recorded version pin does not match what is installed, or was "
            "never recorded at all",
            Remedy.REVALIDATE_PINS,
        ),
        ExitCode.UNCONVERGED: Meaning(
            "a governed tree's declared membership does not match the database",
            Remedy.REBUILD_TREE,
        ),
        ExitCode.LIBRARY_UNREADABLE: Meaning(
            "the database is present but could not be opened or read as expected",
            Remedy.RESTORE_FROM_SNAPSHOT,
        ),
        ExitCode.EXTERNAL_WRITER: Meaning(
            "another writer may be mutating the library concurrently",
            Remedy.DISABLE_CLOUD_SYNC,
        ),
        ExitCode.LIBRARY_PREREQUISITE: Meaning(
            "the library lacks a structure this operation mirrors rather than "
            "fabricates, so there is nothing to copy the schema from",
            Remedy.PREPARE_LIBRARY_IN_REKORDBOX,
        ),
        ExitCode.PRECONDITION: Meaning(
            "a health check this verb declares is failing",
            Remedy.RUN_DOCTOR,
        ),
        ExitCode.MODULE_UNAVAILABLE: Meaning(
            "the module is enabled but the dependencies it needs are not installed",
            Remedy.INSTALL_MODULE_EXTRA,
        ),
        ExitCode.ACK_REQUIRED: Meaning(
            "this destructive session has no recorded backup acknowledgment",
            Remedy.ACKNOWLEDGE_BACKUP,
        ),
        ExitCode.UPSTREAM_AUTH: Meaning(
            "the provider rejected our credentials; no watermark advances",
            Remedy.AUTHENTICATE_PROVIDER,
        ),
        ExitCode.UPSTREAM_UNAVAILABLE: Meaning(
            "the provider or the adapter failed in a way that may pass on retry",
            Remedy.RETRY_LATER,
        ),
        ExitCode.REFUSED_BY_POLICY: Meaning(
            "the operation would violate a policy this installation declares",
            Remedy.CHANGE_POLICY_OR_INPUT,
        ),
        ExitCode.INTERRUPTED: Meaning(
            "cancelled by a signal; distinct from failed, and resumable",
            Remedy.RESUME_JOB,
        ),
    }
)

#: Values withdrawn from service, mapped to the name they used to carry.
#:
#: Empty today, and the discipline is the point rather than the contents. A
#: stored cause and a shell script both outlive the release that wrote them, so
#: re-using a number is how a caller ends up acting on last year's meaning. A
#: retired value stays here forever and is never assigned again.
RETIRED: Mapping[int, str] = MappingProxyType({})


def band_of(code: ExitCode | int) -> Band:
    """The band a code belongs to, or raise if it is outside the vocabulary."""
    value = int(code)
    for band in BANDS:
        if band.start <= value < band.stop:
            return band
    raise ValueError(
        f"exit code {value} is outside the reserved range 0 to {MAX_CODE - 1}. "
        f"Codes at or above {MAX_CODE} collide with the shell's own conventions."
    )


def meaning_of(code: ExitCode) -> Meaning:
    """What a code means and which remediation token answers it."""
    try:
        return MEANINGS[code]
    except KeyError:  # pragma: no cover - the conformance suite makes this unreachable
        raise KeyError(
            f"{code!r} has no declared meaning. Every member of ExitCode carries "
            f"a summary and a remediation token, or a consumer has a number and "
            f"nothing to tell the user about it."
        ) from None


__all__ = [
    "BANDS",
    "MAX_CODE",
    "MEANINGS",
    "RETIRED",
    "Band",
    "ExitCode",
    "Meaning",
    "Remedy",
    "band_of",
    "meaning_of",
]
