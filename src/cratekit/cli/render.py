"""Human rendering, and the ONE place a remediation token becomes a command.

D2 in practice. Every layer below this one carries remediation as a ``Remedy``
token, because the text a user types depends on the platform, the package
manager they actually have, and the interface they are sitting in front of, and
none of those is knowable from a foundation module. This file knows all three,
so this is where a token turns into words.

The other half of R32 lives here too: human output is a FUNCTION OF the
envelope, never a field inside it. The source system stores its rendered gate
text inside the plan JSON, which makes every wording change a schema change and
gives machine consumers a blob of prose they must ignore. Keeping the renderer
separate means the wording can be improved on any afternoon without versioning
anything.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import cause as cause_module
from cratekit.core.cause import Cause
from cratekit.core.exit_codes import ExitCode, Remedy, meaning_of

#: One command line per remediation token, or None when the fix is not a command
#: at all. A token whose answer is "quit an application" or "plug the drive in"
#: has no command, and inventing one would be worse than saying so.
_COMMANDS: Mapping[Remedy, str | None] = {
    Remedy.RUN_SETUP: "crate setup",
    Remedy.REPAIR_CONFIG_FILE: "crate doctor",
    Remedy.UPGRADE_CRATEKIT: None,
    Remedy.FIX_CONFIG_VALUES: "crate doctor",
    Remedy.RETRY_WHEN_UNLOCKED: None,
    Remedy.RECORD_REKORDBOX_PIN: "crate setup",
    Remedy.REPORT_DEFECT: None,
    Remedy.FIX_COMMAND_LINE: None,
    Remedy.ANSWER_DECISION: "crate run decide <run> <gate> <option>",
    Remedy.REPLAN_THEN_DECIDE: "crate run show <run>",
    Remedy.COMPLETE_PENDING_ACTION: None,
    Remedy.WAIT_FOR_HOLDER: None,
    Remedy.RELEASE_STALE_LOCK: "crate session release",
    Remedy.QUIT_REKORDBOX: None,
    Remedy.MOUNT_LIBRARY_VOLUME: None,
    Remedy.REVALIDATE_PINS: "crate doctor",
    Remedy.REBUILD_TREE: "crate rebuild <tree>",
    Remedy.RESTORE_FROM_SNAPSHOT: "crate restore list",
    Remedy.DISABLE_CLOUD_SYNC: None,
    Remedy.PREPARE_LIBRARY_IN_REKORDBOX: None,
    Remedy.RUN_DOCTOR: "crate doctor",
    Remedy.INSTALL_MODULE_EXTRA: None,  # generated per entry, see install_command
    Remedy.ACKNOWLEDGE_BACKUP: "crate session ack",
    Remedy.AUTHENTICATE_PROVIDER: "crate login",
    Remedy.RETRY_LATER: None,
    Remedy.CHANGE_POLICY_OR_INPUT: "crate doctor",
    Remedy.RESUME_JOB: "crate job resume <id>",
}

#: What to do when there is no command. One sentence, imperative, no path.
_ADVICE: Mapping[Remedy, str] = {
    Remedy.UPGRADE_CRATEKIT: "install a newer Cratekit; migrations only move forward",
    Remedy.RETRY_WHEN_UNLOCKED: "another process holds the file; try again shortly",
    Remedy.REPORT_DEFECT: "this is a defect; report it with the cause identifier below",
    Remedy.FIX_COMMAND_LINE: "check the command line against --help",
    Remedy.COMPLETE_PENDING_ACTION: "complete the outstanding action, then verify it",
    Remedy.WAIT_FOR_HOLDER: "wait for the holder named below to finish",
    Remedy.QUIT_REKORDBOX: "quit rekordbox and let its background agent settle",
    Remedy.MOUNT_LIBRARY_VOLUME: "mount the configured library volume",
    # "REACH OR WRITE" rather than only reach, because the token serves both and
    # the detail beside it is where the specific act is named. Written as only
    # the first, it asserted "cannot open a directory on the way to" over a
    # library volume mounted read only, which this account CAN open, and a
    # one-line remedy that states the wrong fact is the collapse this vocabulary
    # exists to prevent.
    Remedy.GRANT_PATH_ACCESS: (
        "this account cannot reach or write the path named below; grant this interpreter "
        "access to it, on macOS through Full Disk Access, or choose a path it can already "
        "use"
    ),
    # Neither of these says Full Disk Access, and that is the point. Both used to.
    Remedy.REMOUNT_WRITABLE: (
        "the volume holding the path named below is mounted read only, so it refuses every "
        "writer on this machine; remount it read write, release the medium's write "
        "protection, or choose a path on a writable volume"
    ),
    Remedy.UNLOCK_PATH: (
        "the path named below carries a lock flag, which is what Finder's Locked checkbox "
        "sets; clear it in Get Info or with chflags nouchg, then retry"
    ),
    Remedy.DISABLE_CLOUD_SYNC: "turn off the streaming service's library sync",
    Remedy.PREPARE_LIBRARY_IN_REKORDBOX: (
        "create the missing structure in rekordbox once; it is mirrored, never fabricated"
    ),
    Remedy.INSTALL_MODULE_EXTRA: "install the extra named below",
    Remedy.RETRY_LATER: "the provider is unavailable; retry later",
    # External binaries.
    Remedy.INSTALL_BINARY: "install the binary named below, then run crate doctor",
    Remedy.INSTALL_BINARY_SOURCE_UNKNOWN: (
        "install the binary named below; this platform has no packaged source, so install it "
        "yourself and point at it with a configured override"
    ),
    Remedy.FIX_BINARY_OVERRIDE: "the configured override does not point at a usable binary",
    Remedy.UNSUPPORTED_PLATFORM: "this platform is not supported for the operation named below",
    # Credentials.
    Remedy.SET_CREDENTIAL: "store the credential named below, then retry",
    Remedy.INSTALL_KEYCHAIN_BACKEND: "install a keychain backend so credentials can be stored",
    Remedy.REPAIR_CREDENTIAL_STORE: "the credential store is unreadable; repair or recreate it",
    Remedy.REAUTHENTICATE: "the stored credential was rejected; authenticate again",
    Remedy.REAUTHENTICATE_PROVIDER: "the provider rejected the stored credential; log in again",
    Remedy.PAUSE_AND_CHECK_ACCOUNT: (
        "the provider is refusing this account; stop and check it before retrying, because "
        "retrying into a block is how an account gets suspended"
    ),
    # The acquisition adapter.
    Remedy.SWITCH_ADAPTER: "switch to another configured acquisition adapter",
    Remedy.INSTALL_ADAPTER: "install the acquisition adapter named below",
    Remedy.CHOOSE_KNOWN_ADAPTER: "name one of the adapters listed below",
    Remedy.REPAIR_ADAPTER_SETTINGS: "the adapter's own settings are unusable; repair them",
    Remedy.RELAX_LOSSLESS_POLICY: (
        "no lossless source exists; change the lossless policy if a marked lossy copy is acceptable"
    ),
    # This installation.
    Remedy.REPAIR_BACKUP_FACTS: "the recorded backup facts are unreadable; repair or reset them",
}


def install_command(entry: registry.Entry) -> str:
    """The exact command that installs a verb's missing extras group.

    Generated from the entry and the distribution name, never written per
    module, so renaming an extras group cannot leave a stale instruction behind
    in twelve places.
    """
    if entry.extras is None:
        raise ValueError(f"{entry.name} declares no extras group")
    # Single-quoted because several shells treat square brackets as a glob.
    # The extras name is validated against the declared modules, so it can
    # only ever be an identifier; no general-purpose quoting is warranted, and
    # reaching for one here would put a second caller of the URL-quoting family
    # in the tree, which the one-decoder guard exists to keep at zero.
    return f"pip install '{registry.DISTRIBUTION}[{entry.extras}]'"


def remedy_text(remedy: Remedy) -> str | None:
    """The words for one token: a command when there is one, else the advice.

    Extracted from :func:`remediation_line` so a caller holding a bare token can
    reach the same rendering rather than growing a second table. The doctor is
    that caller: it reports many findings at once, each with its own token, and a
    private copy of this mapping in that module would be the second place a token
    becomes words, which is exactly what D2 exists to prevent.

    None when the token has neither, which is a defect this module's own
    completeness test already fails on rather than a state a caller must handle.
    """
    return _COMMANDS.get(remedy) or _ADVICE.get(remedy)


#: One sentence per kind of refusal, each ending before the path, which is
#: appended by :func:`access_note`. THREE SENTENCES BECAUSE THERE ARE THREE ACTS.
#: One sentence for all three told a user with a read only volume and a user with
#: a locked file to open Full Disk Access, which changes neither.
_ACCESS_SENTENCE: Mapping[cause_module.AccessKind, str] = MappingProxyType(
    {
        cause_module.AccessKind.PERMISSION: (
            "The operating system refused this account, which is a permission to grant "
            "rather than a defect in this program. On macOS an interpreter without Full "
            "Disk Access is refused exactly this way under Documents, Desktop, Downloads "
            "and external volumes. Grant this interpreter access to the path, or choose "
            "one it can already reach"
        ),
        cause_module.AccessKind.READ_ONLY: (
            "The volume holding it is mounted read only, so it refuses every writer on "
            "this machine and no permission grant can change that. Remount it read write, "
            "release the medium's write protection, or write somewhere else"
        ),
        cause_module.AccessKind.LOCKED: (
            "It carries a lock flag, which is what Finder's Locked checkbox sets and what "
            "chflags uchg writes. It refuses the file's own owner, so this is not a "
            "permission to grant; clear the flag in Get Info or with chflags nouchg"
        ),
    }
)


def access_note(exc: BaseException | None) -> str | None:
    """One sentence for a failure the operating system refused, or None.

    The words for ``cause.access_refusal``, kept here because this is the layer
    allowed to have words (D2) and because three callers need the SAME ones: the
    dispatcher's blanket, doctor's check runner, and the wizard. Three wordings
    for one condition is how one report ends up telling a user their permission
    is a defect on one line and not a defect three lines below.

    IT ALWAYS NAMES THE PATH, because the classification will not report a
    refusal without one. The path is the entire actionable content: "permission
    denied" with nothing to grant access TO is a sentence a user can do nothing
    with, and the sentence that used to be produced for a pathless kernel refusal
    said "the path named below" with nothing below it.
    """
    refusal = cause_module.access_refusal(exc)
    if refusal is None:
        return None
    return f"The path is {refusal.path}. {_ACCESS_SENTENCE[refusal.kind]}"


def remediation_line(cause: Cause) -> str:
    """One line telling the user what to do, built from the token."""
    remedy = cause.remediation.remedy
    if remedy is not None:
        words = remedy_text(remedy)
        if words:
            return f"  fix: {words}"
    if cause.remediation.steps:
        return "  fix: " + cause.remediation.steps[0]
    return f"  fix: {meaning_of(cause.code).summary}"


def render_cause(cause: Cause, *, summary_only: bool = False) -> list[str]:
    """The human form of a failure: what happened, what to do, what caused it.

    ``summary_only`` drops the remediation line and the steps, for the one caller
    that is about to print the same information in a better shape immediately
    below. A diagnostic verb whose payload carries checks lists every failure with
    its own fix in the check table, so the remediation line above it, which falls
    back to the FIRST step when the cause carries no token, prints one of those
    failures a second time and reads as though it were the only one.
    """
    lines = [f"{cause.reason}: {cause.message}"]
    if summary_only:
        return lines + _inner_chain(cause)
    lines.append(remediation_line(cause))
    for step in cause.remediation.steps:
        lines.append(f"    - {step}")
    if cause.remediation.doc:
        lines.append(f"  see: {cause.remediation.doc}")
    return lines + _inner_chain(cause)


def _inner_chain(cause: Cause) -> list[str]:
    """The wrapped causes beneath this one, deepest last.

    Always rendered, even in the summary form: a cause arriving at the boundary
    with things under it means some layer added context, and dropping that is
    dropping the only record of where the failure actually started.
    """
    lines: list[str] = []
    inner = cause.inner
    depth = 1
    while inner is not None:
        lines.append(f"  {'  ' * depth}caused by {inner.reason}: {inner.message}")
        inner = inner.inner
        depth += 1
    return lines


#: How a check's status is coloured in words. Statuses come from the payload, so
#: an unrecognised one renders as itself rather than being dropped: a consumer
#: that invented a fourth status is a defect to see, not a row to hide.
_CHECK_MARK: Mapping[str, str] = {"ok": "ok  ", "fail": "FAIL", "info": "note"}


def render_checks(envelope: Envelope) -> list[str]:
    """The check table for a diagnostic verb, or nothing at all.

    The five structured surfaces are rendered by this module rather than carried
    as prose inside the envelope (R32), and the diagnostic surface is the one a
    person reads directly: a doctor whose human output says only "failed" sends
    the reader to parse JSON to find out what failed.

    Gated on the schema rather than on the presence of a ``checks`` key, so a
    later surface that happens to have one is not rendered in a shape that was
    never designed for it.
    """
    if not envelope.schema.startswith("diagnostic/"):
        return []
    checks = envelope.data.get("checks")
    if not isinstance(checks, (list, tuple)) or not checks:
        return []
    lines = [""]
    for check in checks:
        if not isinstance(check, Mapping):  # pragma: no cover - a malformed payload
            continue
        status = str(check.get("status", "?"))
        lines.append(
            f"  [{_CHECK_MARK.get(status, status)}] {check.get('key', '?')}: "
            f"{check.get('detail', '')}"
        )
        token = check.get("remedy")
        if not token:
            continue
        try:
            words = remedy_text(Remedy(str(token)))
        except ValueError:  # pragma: no cover - a token outside the vocabulary
            words = None
        if words:
            lines.append(f"         fix: {words}")
    return lines


def render(envelope: Envelope) -> str:
    """The default human output for any verb's result.

    Deliberately terse and deliberately ordered: what happened, what a person
    still has to do, then the failure detail. A user reading a refusal wants the
    remedy before the diagnosis.
    """
    lines: list[str] = []
    if envelope.exit_code is ExitCode.OK:
        lines.append(f"{envelope.verb}: {envelope.outcome}")
    else:
        lines.append(f"{envelope.verb}: {envelope.outcome} ({envelope.exit_code.name})")

    pending = envelope.pending_human_action
    if pending is not None:
        lines.append("")
        lines.append(f"Outstanding: {pending.summary}")
        if pending.artifact:
            lines.append(f"  file: {pending.artifact}")
        for index, step in enumerate(pending.steps, start=1):
            lines.append(f"  {index}. {step}")
        lines.append(f"  verify: {pending.verify_verb}")
        if pending.blocks:
            lines.append(f"  blocks: {', '.join(pending.blocks)}")

    checks = render_checks(envelope)
    if envelope.cause is not None:
        lines.append("")
        lines += render_cause(envelope.cause, summary_only=bool(checks))
    lines += checks

    for warning in envelope.warnings:
        lines.append(f"warning [{warning.get('code', '?')}]: {warning.get('message', '')}")

    lines.append(f"run: {envelope.run_id}")
    return "\n".join(lines) + "\n"


def render_gate(cause: Cause) -> str:
    """The decision screen: the question, the options, and how to answer it.

    The options come from the gate declaration rather than from prose, so a new
    option appears here the moment it is declared and cannot be forgotten in the
    wording.
    """
    detail = cause.detail
    gate = detail.get("gate", "?")
    options = detail.get("options") or []
    run_id = detail.get("run_id", "<run>")
    lines = [
        detail.get("prompt", "A decision is required."),
        "",
        f"  gate:    {gate}",
        f"  options: {', '.join(options)}",
        "",
        f"  answer:  crate run decide {run_id} {gate} <option>",
    ]
    if not detail.get("explicit"):
        lines.append(f"  or:      rerun with -d {gate}=<option>")
    else:
        lines.append(
            "  this gate takes no inline answer: it must be asserted on its own, "
            "and the assertion records who made it"
        )
    return "\n".join(lines) + "\n"


__all__ = [
    "access_note",
    "install_command",
    "remediation_line",
    "remedy_text",
    "render",
    "render_cause",
    "render_checks",
    "render_gate",
]
