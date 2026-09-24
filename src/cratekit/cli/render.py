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

import shlex
from collections.abc import Mapping, Sequence
from pathlib import PurePath
from types import MappingProxyType
from typing import Any

from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import cause as cause_module
from cratekit.core.cause import Cause
from cratekit.core.exit_codes import ExitCode, Remedy, meaning_of
from cratekit.modules import extras

#: The provider session procedure, worded once. TWO tokens need it, a session
#: that was never minted and a session the provider rejected, and they differ
#: only in why the person is reading it. Written as one string because two
#: copies of a three act procedure is how they come to name two different second
#: steps, which is the failure this whole file exists to make impossible.
#:
#: IT NAMES THE ERASE, which a reader drops and which the product's promise
#: needs: no provider token sits on disk between invocations, and the hop
#: through a file is the one moment that is briefly false.
#:
#: The document is named as the project's rather than as a local file. ``docs/``
#: is in no wheel, measured by building one, so an installed person told to open
#: a path would find nothing.
_PROVIDER_SESSION_PROCEDURE = (
    "mint it with the vendored downloader's own login command, record it with "
    "crate login provider-session --from-file, then erase the plaintext file, which "
    "docs/adapters.md in the project's repository sets out step by step"
)

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
    # Not "crate login", which this table offered until U97. That verb records a
    # value somebody already holds and refuses without one, so a first run person
    # who typed it reached a second refusal. Minting is an attended act at a
    # browser that the vendored downloader owns, which makes this three acts and
    # not a command; see the advice below.
    Remedy.AUTHENTICATE_PROVIDER: None,
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
    # THREE ACTS, IN ORDER, BECAUSE THERE IS NO COMMAND THAT DOES IT. R-411
    # measured the cost of the single verb the first of these used to be, and
    # the second said "log in again", which is the same dead end reached from
    # the other direction and is the likelier one: every session minted before
    # 2026-09-01 is a device flow session the adapter now refuses.
    Remedy.AUTHENTICATE_PROVIDER: (
        "no provider session is stored and crate login cannot mint one, it only records "
        "one; " + _PROVIDER_SESSION_PROCEDURE
    ),
    Remedy.REAUTHENTICATE_PROVIDER: (
        "the provider rejected the stored session and crate login cannot mint another, it "
        "only records one; " + _PROVIDER_SESSION_PROCEDURE
    ),
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

    Generated from the entry, never written per module, so renaming an extras
    group cannot leave a stale instruction behind in twelve places. The command
    itself is ``modules.extras``, the one source the analysis workers' refusals
    read too, and it depends on whether this process runs under pipx (R-395).
    """
    if entry.extras is None:
        raise ValueError(f"{entry.name} declares no extras group")
    return extras.install_command(entry.extras)


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


def render_review_set(envelope: Envelope) -> list[str]:
    """The review set a person reads, or nothing at all.

    Harvest already puts the offered names and the unresolved count on the
    envelope. Without a case here, the default output is the verb, the outcome,
    and a run id, and a person has to ask for json to see what was found.

    Gated on the schema rather than on the presence of an ``items`` key, so a
    later surface that happens to carry one is not rendered in a shape that was
    never designed for it. An item that already has a name is that name, because
    that is the field harvest projected for a person. An item that does not
    keeps its own fields rather than growing a harvest shaped line.
    """
    if not envelope.schema.startswith("review_set/"):
        return []
    data = envelope.data
    queue = data.get("queue")
    items = data.get("items")
    unresolved = data.get("unresolved")
    lines = [""]
    if queue not in (None, ""):
        lines.append(f"  queue: {_shown_value(queue)}")
    if isinstance(items, (list, tuple)):
        for item in items:
            lines.append(f"  {_review_item_line(item)}")
    if unresolved is not None:
        lines.append(f"  unresolved: {_shown_value(unresolved)}")
    return lines if len(lines) > 1 else []


#: The verbs whose ``job_state`` progress carries a resolution counted in the
#: intake words, and the command that lists what a finished one left missing.
#: Spelled as registry names rather than imported, because this layer renders
#: payloads and must not load a feature module to do it.
_RESOLVING_VERBS: frozenset[str] = frozenset({"intake.playlist", "intake.set"})

#: The intake resolution's four words, each with a sentence worded after the
#: ones ``intake missing`` puts beside the same counts. Not the same strings:
#: that verb says what it left out of a list, and this says where a row stands.
_RESOLUTION_WORDS: tuple[tuple[str, str], ...] = (
    ("owned", "already in the library"),
    ("offered", "held in another version, offered for review; see: crate review list"),
    ("missing", "not in the library"),
    ("suppressed", "deleted on purpose"),
)


def render_job_state(envelope: Envelope, *, drive: Sequence[str] | None = None) -> list[str]:
    """The job a verb queued or drove, or nothing at all.

    A queueing verb answers with ``job_state`` and, without a case here, the
    default output was the verb, the outcome and a run id: the identifier the
    person needs to drive the job was only in the json. Gated on the schema, the
    rule every case in this file follows, and on a job identifier, because a
    queue that correctly held nothing and a listing both carry an empty one.

    ``drive`` IS THE ONE THING NOT READ FROM THE ENVELOPE. A job is driven by its
    own verb's command line rebuilt from the frozen payload, and the payload is
    in the queue rather than the envelope, so the dispatcher looks it up and
    hands it here. It is None for every envelope but the one from the verb that
    queued the job, because ``job resume`` answers with a queued job too, after
    spawning the child that drives it, and a second drive command there would
    invite two drivers onto one job.
    """
    if not envelope.schema.startswith("job_state/"):
        return []
    data = envelope.data
    job_id = data.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        return []
    state = str(data.get("state", "?"))
    lines = ["", f"  job: {job_id}, {state}"]
    if state == "queued" and drive:
        lines.append(f"  drive it with: {shlex.join(['crate', *drive])}")
    progress = data.get("progress")
    if not isinstance(progress, Mapping):
        return lines
    total, settled = progress.get("total"), progress.get("settled")
    if isinstance(total, int) and isinstance(settled, int):
        lines.append(f"  items: {settled} of {total} settled")
    if envelope.verb in _RESOLVING_VERBS and state != "queued":
        lines += _resolution_lines(job_id, state, progress)
    return lines


def _resolution_lines(job_id: str, state: str, progress: Mapping[str, Any]) -> list[str]:
    """An intake job's resolution, counted by state, then what to run next.

    Only the words the progress actually carries. A resolution from a build that
    did not count one of them says nothing about it, rather than a zero that
    reads as counted.
    """
    lines = [
        f"  {word}: {progress[word]} {said}"
        for word, said in _RESOLUTION_WORDS
        if isinstance(progress.get(word), int)
    ]
    if state == "succeeded" and isinstance(progress.get("missing"), int) and progress["missing"]:
        # ONLY A SUCCEEDED JOB, because ``intake missing`` refuses every other.
        lines.append(f"  next: crate intake missing --job {job_id}")
    return lines


def _proof_line(item: Mapping[str, Any]) -> str:
    """One run of an import proof, worded by the action ``intake imported`` marked it.

    The action slugs are spelled here rather than imported from the verb, for
    the reason :data:`_RESOLVING_VERBS` gives. An action this table does not
    know keeps its own fields rather than being dropped.
    """
    run = f"run {item.get('session_id', '?')}"
    action = item.get("action")
    retired = item.get("retired_to")
    filed = f"intake file retired to {PurePath(str(retired)).name}" if retired else None
    closed = "run closed" if item.get("closed") is True else None
    if action == "imported":
        said = [f"proven imported, {_shown_value(item.get('count'))} track(s)"]
        said.append(filed or "no intake file to retire")
    elif action == "not-imported":
        said = [
            f"not imported, {_shown_value(item.get('missing'))} of "
            f"{_shown_value(item.get('count'))} landed track(s) not in the export"
        ]
    elif action == "unverifiable":
        said = [f"not verifiable, {_shown_value(item.get('why'))}"]
    elif action == "retired":
        said = ["proven earlier"] + ([filed] if filed else [])
    else:
        return ", ".join(f"{k}={_shown_value(v)}" for k, v in item.items())
    if closed:
        said.append(closed)
    return f"{run}: " + "; ".join(said)


def render_import_proof(envelope: Envelope) -> list[str]:
    """What ``intake imported`` proved and retired, or nothing at all.

    The ``plan`` surface's items are shaped by the verb that plans, so this case
    is gated on the verb as well as the schema: another planning verb's items
    carry no ``action`` and would be rendered in a shape never designed for them.
    """
    if not envelope.schema.startswith("plan/") or envelope.verb != "intake.imported":
        return []
    items = envelope.data.get("items")
    if not isinstance(items, (list, tuple)) or not items:
        return []
    lines = [""]
    for item in items:
        lines.append(f"  {_proof_line(item) if isinstance(item, Mapping) else _shown_value(item)}")
    # THE RUN COUNT IS THE VERB'S OWN TOTAL, so the summary a person reads and
    # the one a consumer reads cannot disagree. The track and file counts are
    # not totals the verb keeps, so they are summed from the same items.
    proven = [
        item for item in items if isinstance(item, Mapping) and item.get("action") == "imported"
    ]
    totals = envelope.data.get("totals")
    runs = totals.get("imported") if isinstance(totals, Mapping) else None
    runs = runs if isinstance(runs, int) else len(proven)
    tracks = sum(item["count"] for item in proven if isinstance(item.get("count"), int))
    retired = sum(1 for item in items if isinstance(item, Mapping) and item.get("retired_to"))
    lines.append(f"  proven: {runs} run(s), {tracks} track(s); retired: {retired} intake file(s)")
    return lines


def _review_item_line(item: Any) -> str:
    """One review item as a person should read it."""
    if not isinstance(item, Mapping):
        return _shown_value(item)
    name = item.get("name")
    if isinstance(name, str) and name:
        return name
    return ", ".join(f"{k}={_shown_value(v)}" for k, v in item.items())


def render(envelope: Envelope, *, drive: Sequence[str] | None = None) -> str:
    """The default human output for any verb's result.

    Deliberately terse and deliberately ordered: what happened, what a person
    still has to do, then the failure detail. A user reading a refusal wants the
    remedy before the diagnosis.

    ``drive`` is the command line that continues a job this invocation queued,
    looked up by the dispatcher because the envelope does not carry it; see
    :func:`render_job_state`.
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
    review_set = render_review_set(envelope)
    if envelope.cause is not None:
        lines.append("")
        lines += render_cause(envelope.cause, summary_only=bool(checks))
    lines += checks
    lines += review_set
    lines += render_job_state(envelope, drive=drive)
    lines += render_import_proof(envelope)

    for warning in envelope.warnings:
        lines.append(f"warning [{warning.get('code', '?')}]: {warning.get('message', '')}")

    lines.append(f"run: {envelope.run_id}")
    return "\n".join(lines) + "\n"


def _shown_lines(shown: Mapping[str, Any]) -> list[str]:
    """What the verb consulted, rendered under the question it was asked over.

    ONE LINE PER FACT, and a collection is expanded rather than printed as a
    Python repr, because a person reading "shown: [{'portion': 'database', ...}]"
    has been handed the serializer's output rather than an answer. The keys come
    from whatever the verb passed, so nothing here names a backup portion or a
    lock holder: this function's whole job is to be the display half of a value
    it does not interpret.
    """
    lines: list[str] = []
    for name, value in shown.items():
        if isinstance(value, Mapping):
            lines.append(f"  {name}:")
            for key, entry in value.items():
                lines.append(f"    {key}: {_shown_value(entry)}")
        elif isinstance(value, (list, tuple)):
            lines.append(f"  {name}:")
            for item in value:
                if isinstance(item, Mapping):
                    lines.append(
                        "    " + ", ".join(f"{k}={_shown_value(v)}" for k, v in item.items())
                    )
                else:
                    lines.append(f"    {_shown_value(item)}")
        else:
            lines.append(f"  {name}: {_shown_value(value)}")
    return lines


def _shown_value(value: Any) -> str:
    """One carried value as a person should read it.

    ``None`` becomes a word rather than the interpreter's spelling of it. A
    refusal that prints "acknowledgment: None" has told a Python programmer
    something and told everybody else nothing, and this is the surface a person
    reads without asking for JSON.
    """
    if value is None:
        return "none"
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return str(value)


def render_gate(cause: Cause) -> str:
    """The decision screen: the question, the options, and how to answer it.

    The options come from the gate declaration rather than from prose, so a new
    option appears here the moment it is declared and cannot be forgotten in the
    wording.

    WHAT THE VERB SHOWED IS RENDERED HERE OR IT IS NOT SHOWN AT ALL. A gate's
    prompt is fixed at declaration, so a verb that has to put a fact in front of
    the person carries it on the refusal instead
    (:class:`cratekit.cli.gates.DecisionRequired`). This function is the only
    place that reaches a person who is not reading JSON, so a carried context
    that stopped at the envelope would satisfy a machine and leave a human
    answering a bare question. Absent stays absent: a refusal with no context
    prints exactly what it printed before this existed.
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
    ]
    shown = detail.get("shown")
    if isinstance(shown, Mapping) and shown:
        lines.append("")
        lines += _shown_lines(shown)
    lines += [
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
    "render_import_proof",
    "render_job_state",
    "render_review_set",
]
