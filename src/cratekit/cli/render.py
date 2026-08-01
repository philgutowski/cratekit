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

from typing import Mapping

from cratekit.cli import registry
from cratekit.cli.output import Envelope
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


def remediation_line(cause: Cause) -> str:
    """One line telling the user what to do, built from the token."""
    remedy = cause.remediation.remedy
    if remedy is not None:
        command = _COMMANDS.get(remedy)
        if command:
            return f"  fix: {command}"
        advice = _ADVICE.get(remedy)
        if advice:
            return f"  fix: {advice}"
    if cause.remediation.steps:
        return "  fix: " + cause.remediation.steps[0]
    return f"  fix: {meaning_of(cause.code).summary}"


def render_cause(cause: Cause) -> list[str]:
    """The human form of a failure: what happened, what to do, what caused it."""
    lines = [f"{cause.reason}: {cause.message}", remediation_line(cause)]
    for step in cause.remediation.steps:
        lines.append(f"    - {step}")
    if cause.remediation.doc:
        lines.append(f"  see: {cause.remediation.doc}")
    inner = cause.inner
    depth = 1
    while inner is not None:
        lines.append(f"  {'  ' * depth}caused by {inner.reason}: {inner.message}")
        inner = inner.inner
        depth += 1
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

    if envelope.cause is not None:
        lines.append("")
        lines += render_cause(envelope.cause)

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


__all__ = ["install_command", "remediation_line", "render", "render_cause", "render_gate"]
