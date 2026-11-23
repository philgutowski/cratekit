"""The one reserved exit-code vocabulary, and the remediation tokens beside it.

KTD25: one integer once meant different things to different producers, so no
consumer could tell them apart. Three rules, each enforced by a test:

1. One vocabulary in the foundation layer, so producers and consumers name the
   same constant instead of bare integers.
2. 2 belongs to argparse and no verb may ever return it, because argparse will
   keep producing it.
3. Every code carries a remediation token, never the text a user types; the CLI
   renders it (D2), since the command depends on platform and interface.

Foundation layer: names no verb, module or taxonomy term, imports nothing from
Cratekit.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from types import MappingProxyType
from typing import Mapping

#: Nothing at or above this value is used, so a status never collides with the
#: shell's 126, 127 and 128 plus a signal, or truncates past one byte.
MAX_CODE = 64


class ExitCode(IntEnum):
    """Every status ``crate`` can exit with, banded by tens, gapped for growth.

    The tens digit classifies a code without a lookup. New codes join a band and
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
    """What to do about a failure, as a token the CLI renders (D2).

    Values are stable slugs persisted inside a cause across processes (KTD26),
    so a rename is a breaking change and follows the exit-code retirement rule.
    Foundation modules that declare their own remedy subset must stay a subset;
    ``tests/test_cli_contract.py`` finds them by walking the package (P3, KTD13).
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
    # A path this account cannot reach, such as macOS without Full Disk Access;
    # a different act from mounting a volume.
    GRANT_PATH_ACCESS = "grant-path-access"
    # A read only volume refuses every writer, so access grants cannot fix it.
    REMOUNT_WRITABLE = "remount-writable"
    # A per-file immutable flag (Finder's "Locked", ``chflags uchg``), which
    # refuses even the owner, so it is not a permission.
    UNLOCK_PATH = "unlock-path"
    REVALIDATE_PINS = "revalidate-pins"
    REBUILD_TREE = "rebuild-tree"
    RESTORE_FROM_SNAPSHOT = "restore-from-snapshot"
    DISABLE_CLOUD_SYNC = "disable-cloud-sync"
    PREPARE_LIBRARY_IN_REKORDBOX = "prepare-library-in-rekordbox"

    # This installation.
    RUN_DOCTOR = "run-doctor"
    INSTALL_MODULE_EXTRA = "install-module-extra"
    ACKNOWLEDGE_BACKUP = "acknowledge-backup"
    # U138: over a backup too old to acknowledge, the answer is a backup.
    RUN_BACKUP = "run-backup"
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

    # Re-authentication. ``reauthenticate`` is a stored credential the keychain
    # rejected, ``reauthenticate-provider`` one the provider rejected. They sit
    # close to ``authenticate-provider``, but each is a persisted slug, so
    # merging them needs a migration.
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
    # Growth room for a new class; MAX_CODE and above stay free.
    Band(60, MAX_CODE, "unclaimed", "reserved for a class that has not appeared yet"),
)


@dataclass(frozen=True, slots=True)
class Meaning:
    """What one code means, and what the user does about it.

    ``verb_producible`` is False for a code a verb must never return, today
    ``USAGE``, which argparse owns (KTD25).
    """

    summary: str
    remedy: Remedy
    verb_producible: bool = True


#: One entry per member, declared because a remediation is a decision, not a
#: function of the number. A test iterates ``ExitCode`` to keep it complete.
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

#: Values withdrawn from service, mapped to their old name. A retired value is
#: never assigned again, since stored causes and scripts outlive a release.
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
