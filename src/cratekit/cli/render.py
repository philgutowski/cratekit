"""Human rendering, and the one place a remediation token becomes words (D2).

Lower layers carry a ``Remedy`` token, since the command a user types depends
on platform, package manager and interface, which only this layer knows. Human
output is a function of the envelope, never a field inside it (R32), so wording
can change without a schema change.
"""

from __future__ import annotations

import json
import shlex
from collections.abc import Mapping, Sequence
from pathlib import PurePath
from types import MappingProxyType
from typing import Any

from cratekit.cli import gates, registry
from cratekit.cli.output import Envelope
from cratekit.core import cause as cause_module
from cratekit.core.cause import Cause
from cratekit.core.exit_codes import ExitCode, Remedy, meaning_of
from cratekit.modules import extras

#: The provider session procedure, worded once because two tokens share it. It
#: names the erase, since no provider token may sit on disk between invocations,
#: and names the doc as the project's because ``docs/`` is in no wheel.
_PROVIDER_SESSION_PROCEDURE = (
    "mint it with the vendored downloader's own login command, record it with "
    "crate login provider-session --from-file, then erase the plaintext file, which "
    "docs/adapters.md in the project's repository sets out step by step"
)

#: One command line per remediation token, or None when the fix is not a
#: command; inventing one would be worse than saying so.
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
    Remedy.RUN_BACKUP: "crate backup run",
    # Not "crate login", which only records a session (U97); minting is three
    # attended acts, worded in the advice below.
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
    # "Reach or write", because the token serves both and the detail names which.
    Remedy.GRANT_PATH_ACCESS: (
        "this account cannot reach or write the path named below; grant this interpreter "
        "access to it, on macOS through Full Disk Access, or choose a path it can already "
        "use"
    ),
    # Neither says Full Disk Access, since no permission grant fixes either.
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
    # Three acts in order, because no command does it (R-411).
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

    Generated from the entry via ``modules.extras``, the one source shared with
    the analysis workers, so a renamed group leaves no stale instruction (R-395).
    """
    if entry.extras is None:
        raise ValueError(f"{entry.name} declares no extras group")
    return extras.install_command(entry.extras)


def remedy_text(remedy: Remedy) -> str | None:
    """The words for one token: a command when there is one, else the advice.

    Public so a caller holding a bare token, such as doctor, needs no second
    table (D2). None only for a token with neither, which a test forbids.
    """
    return _COMMANDS.get(remedy) or _ADVICE.get(remedy)


#: One sentence per kind of refusal, ending before the path. Three, because
#: each kind needs a different act.
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

    The words for ``cause.access_refusal``, shared by the dispatcher, doctor and
    the wizard so one condition has one wording (D2). It always names the path,
    the only actionable part.
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

    ``summary_only`` drops the remediation line and steps, for a diagnostic verb
    whose check table already lists every failure with its own fix.
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
    """The wrapped causes beneath this one, deepest last, always rendered.

    They are the only record of where the failure started.
    """
    lines: list[str] = []
    inner = cause.inner
    depth = 1
    while inner is not None:
        lines.append(f"  {'  ' * depth}caused by {inner.reason}: {inner.message}")
        inner = inner.inner
        depth += 1
    return lines


#: How a check's status reads. An unrecognised status renders as itself, so a
#: defect is seen rather than hidden.
_CHECK_MARK: Mapping[str, str] = {"ok": "ok  ", "fail": "FAIL", "info": "note"}


def render_checks(envelope: Envelope) -> list[str]:
    """The check table for a diagnostic verb, or nothing at all (R32).

    Gated on the schema rather than a ``checks`` key, so another surface with
    one is not rendered in a shape not designed for it.
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

    Gated on the schema rather than an ``items`` key. An item with a name prints
    that name, the field harvest projected for a person; one without keeps its
    own fields.
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


#: The verbs whose ``job_state`` progress carries an intake resolution. Spelled
#: as registry names, since this layer must not load a feature module.
_RESOLVING_VERBS: frozenset[str] = frozenset({"intake.playlist", "intake.set"})

#: The intake resolution's four words, each with the sentence that says where
#: a row stands.
_RESOLUTION_WORDS: tuple[tuple[str, str], ...] = (
    ("owned", "already in the library"),
    ("offered", "held in another version, offered for review; see: crate review list"),
    ("missing", "not in the library"),
    ("suppressed", "deleted on purpose"),
)


def render_job_state(envelope: Envelope, *, drive: Sequence[str] | None = None) -> list[str]:
    """The job a verb queued or drove, or nothing at all.

    Gated on the schema and on a job identifier, since an empty queue and a
    listing both carry an empty one. ``drive`` is the command line rebuilt from
    the queued payload, passed by the dispatcher only for the verb that queued
    the job, so ``job resume`` never invites a second driver.
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
    lines += _playlist_lines(progress)
    if progress.get(_DRY_RUN) is True:
        lines.append("  a dry run: nothing was cancelled")
    total, settled = progress.get("total"), progress.get("settled")
    if isinstance(total, int) and isinstance(settled, int):
        lines.append(f"  items: {settled} of {total} settled")
    if envelope.verb in _RESOLVING_VERBS and state != "queued":
        lines += _resolution_lines(job_id, state, progress)
    lines += _judging_lines(progress)
    if state != "queued":
        lines += _outbound_lines(progress)
    lines += _track_lines(progress)
    lines += _analysis_check_lines(progress)
    return lines


#: The verb whose ``job_state`` answer lists every job rather than one (U169).
_LISTING_VERB = "job.list"


def render_job_list(envelope: Envelope) -> list[str]:
    """``job list``'s jobs, one line each, under how many sit in each state (U169).

    Gated on the schema and the listing verb, since the listing carries no
    single job. ``no worker`` marks a job nothing is bound to run. An empty
    listing says so; an unreadable progress prints nothing rather than an
    unmeasured ``none``.
    """
    if not envelope.schema.startswith("job_state/") or envelope.verb != _LISTING_VERB:
        return []
    progress = envelope.data.get("progress")
    if not isinstance(progress, Mapping):
        return []
    rows = progress.get("jobs")
    if not isinstance(rows, list):
        return []
    listed = [row for row in rows if isinstance(row, Mapping)]
    if rows and not listed:
        return []
    if not listed:
        state = envelope.data.get("state")
        within = f" in {state}" if isinstance(state, str) and state and state != "all" else ""
        return ["", f"  jobs: none{within}"]
    counts = progress.get("counts")
    by_state = (
        ", ".join(
            f"{state} {count}" for state, count in counts.items() if _whole(count) and count
        )
        if isinstance(counts, Mapping)
        else ""
    )
    lines = ["", f"  jobs: {len(listed)}" + (f" ({by_state})" if by_state else "")]
    lines += [f"  {_job_line(row)}" for row in listed]
    lines.append("  each job in full: crate job show JOB_ID")
    return lines


def _job_line(row: Mapping[str, Any]) -> str:
    """One listed job: id, verb, state, then what is known of its progress."""
    parts = [_one_line(row.get(key) or "?") for key in ("job_id", "handler", "state")]
    if isinstance(row.get(_PLAYLIST), str) and row[_PLAYLIST]:
        parts.append(f"playlist {_one_line(row[_PLAYLIST])}")
    elif isinstance(row.get(_SOURCE), str) and row[_SOURCE]:
        parts.append(f"source {_one_line(row[_SOURCE])}")
    progress = row.get("progress")
    if isinstance(progress, Mapping):
        total, settled = progress.get("total"), progress.get("settled")
        if _whole(total) and _whole(settled):
            parts.append(f"{settled} of {total} settled")
        # A skipped item is settled but not done (U169), so say how many.
        counts = progress.get("counts")
        skipped = counts.get("skipped") if isinstance(counts, Mapping) else None
        if _whole(skipped) and skipped:
            parts.append(f"{skipped} skipped")
    cause = row.get("cause")
    if isinstance(cause, Mapping) and cause.get("reason"):
        parts.append(_one_line(cause["reason"]))
    if row.get("worker") == "none":
        parts.append("no worker")
    return ", ".join(parts)


#: The stale cancel verb and its fields (U182), spelled here for
#: :data:`_RESOLVING_VERBS`' reason; a test pins each to ``cli.jobs``.
_CANCEL_VERB = "job.cancel"
_STALE_DAYS = "stale_days"
_DRY_RUN = "dry_run"
_CANCEL_LISTS: tuple[tuple[str, str, str], ...] = (
    ("cancel", "cancelled", "would cancel"),
    ("kept", "kept", "would keep"),
    ("left", "left alone", "would leave alone"),
)


def render_stale_cancel(envelope: Envelope) -> list[str]:
    """What ``job cancel --stale-days`` cancelled, kept and left, one line a job (U182).

    Gated on the verb and on the payload naming its cutoff, so a single cancel
    renders as before.
    """
    if not envelope.schema.startswith("job_state/") or envelope.verb != _CANCEL_VERB:
        return []
    progress = envelope.data.get("progress")
    if not isinstance(progress, Mapping) or not _whole(progress.get(_STALE_DAYS)):
        return []
    dry = progress.get(_DRY_RUN) is True
    days = progress[_STALE_DAYS]
    lines = ["", f"  queued intake jobs older than {days} day(s)" + (", a dry run" if dry else "")]
    for field, done, would in _CANCEL_LISTS:
        rows = progress.get(field)
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, Mapping):
                lines.append(f"  {would if dry else done}: {_stale_line(row)}")
    if len(lines) == 2:
        lines.append("  none open")
    if not dry and progress.get("cancel"):
        lines.append("  a cancelled job reopens with: crate job resume JOB_ID")
    return lines


def _stale_line(row: Mapping[str, Any]) -> str:
    parts = [_one_line(row.get("job_id") or "?"), _one_line(row.get("label") or "?")]
    age = row.get("age_days")
    parts.append(f"{age} day(s) old" if _whole(age) else "age unknown")
    if _whole(row.get("tracks")):
        parts.append(f"{row['tracks']} track(s)")
    same = row.get("same_tracks")
    if isinstance(same, list) and same:
        parts.append("same tracks as " + ", ".join(_one_line(job) for job in same))
    line = ", ".join(parts)
    if row.get("reason"):
        line += f": {_one_line(row['reason'])}"
    if row.get("frees"):
        line += f"; {_one_line(row['frees'])}"
    return line

#: The fields naming an intake job's playlist (U182); a test pins them to
#: ``cli.jobs``.
_PLAYLIST = "playlist"
_SOURCE = "source"


def _playlist_lines(progress: Mapping[str, Any]) -> list[str]:
    """The playlist an intake job was made for, and its source when that differs."""
    named = progress.get(_PLAYLIST)
    source = progress.get(_SOURCE)
    if not isinstance(named, str) or not named:
        if isinstance(source, str) and source:
            return [f"  source: {_one_line(source)}"]
        return []
    if isinstance(source, str) and source and source != named:
        return [f"  playlist: {_one_line(named)} ({_one_line(source)})"]
    return [f"  playlist: {_one_line(named)}"]


#: The field holding an intake job's frozen tracks; a test pins it to
#: ``cli.jobs.TRACKS_FIELD``.
_INTAKE_TRACKS = "intake_tracks"


def _analysis_check_lines(progress: Mapping[str, Any]) -> list[str]:
    """The checks an analysis job reports about its own run, or nothing at all (U241).

    Gated on the payload, never the verb's name, and printed in the check
    table's form so a status reads as it does under ``crate doctor``.
    """
    analysis = progress.get("analysis")
    if not isinstance(analysis, Mapping):
        return []
    checks = analysis.get("checks")
    if not isinstance(checks, Sequence) or isinstance(checks, str):
        return []
    lines: list[str] = []
    for check in checks:
        if not isinstance(check, Mapping):
            continue
        status = str(check.get("status", "?"))
        lines.append(
            f"  [{_CHECK_MARK.get(status, status)}] {_one_line(check.get('key', '?'))}: "
            f"{_one_line(check.get('detail', ''))}"
        )
    return lines


def _track_lines(progress: Mapping[str, Any]) -> list[str]:
    """Every track an intake job froze, in its order, or nothing at all (R-925).

    Gated on the payload, never the verb's name. Every row prints, with its
    ISRC or its absence, since one song under several ISRCs is what it is read for.
    """
    rows = progress.get(_INTAKE_TRACKS)
    if not isinstance(rows, Sequence) or isinstance(rows, str):
        return []
    lines = [f"  tracks: {len(rows)}"]
    for number, row in enumerate(rows, start=1):
        if not isinstance(row, Mapping):
            lines.append(f"    {number}. {_one_line(row)}")
            continue
        named = " - ".join(_one_line(row[key]) for key in ("artist", "title") if row.get(key))
        named = named or f"item {_one_line(row.get('item') or '?')}"
        if row.get("version"):
            named += f" ({_one_line(row['version'])})"
        isrc = f"isrc {_one_line(row['isrc'])}" if row.get("isrc") else "no isrc"
        lines.append(f"    {number}. {named}, {isrc}")
    return lines


#: The counts an outbound job reports, in reading order, with their words
#: (R-850, R-856). Only keys a summary carries print. "Already there or written
#: before", since the engine counts off its ledger, not the account (R-855).
_OUTBOUND_WORDS: tuple[tuple[str, str], ...] = (
    ("written", "written"),
    ("hearted", "hearted"),
    ("already", "already there or written before"),
    ("already_hearted", "already hearted or hearted before"),
    ("unmatched", "unmatched"),
)


def _outbound_lines(progress: Mapping[str, Any]) -> list[str]:
    """What an outbound job wrote and every track it left out, or nothing at all.

    Gated on the payload, never the verb's name, so an uncounted summary prints
    no zero that reads as counted.
    """
    outbound = progress.get("outbound")
    if not isinstance(outbound, Mapping):
        return []
    counts = outbound.get("counts")
    if not isinstance(counts, Mapping):
        return []
    said = [f"{counts[word]} {words}" for word, words in _OUTBOUND_WORDS if _whole(counts.get(word))]
    lines = [f"  tracks: {', '.join(said)}"] if said else []
    left_out = outbound.get("unmatched_tracks")
    for row in left_out if isinstance(left_out, Sequence) and not isinstance(left_out, str) else ():
        if isinstance(row, Mapping):
            named = " - ".join(_one_line(row[key]) for key in ("artist", "title") if row.get(key))
            named = named or f"row {_one_line(row.get('identity') or '?')}"
            lines.append(f"    unmatched: {named}: {_one_line(row.get('reason') or 'no reason given')}")
    return lines


def _one_line(value: Any) -> str:
    """Free text on one line, quoted only when it holds a line break.

    Not :func:`_item_value`: commas are common in artists and titles here, and
    quoting them would quote nearly every row.
    """
    text = str(value)
    if "\n" in text or "\r" in text:
        return json.dumps(text, ensure_ascii=False)
    return text


#: The four counts ``label judge`` reports per label, in reading order (R-815).
_JUDGING_WORDS: tuple[str, ...] = ("judged", "held", "passed", "not-judged")


def _judging_lines(progress: Mapping[str, Any]) -> list[str]:
    """What a judging job did, in total and per label, or nothing at all.

    Gated on the payload, never the verb's name. An unreadable count is left
    out, not shown as zero.
    """
    judging = progress.get("judging")
    if not isinstance(judging, Mapping):
        return []

    def counted(row: Mapping[str, Any]) -> str:
        return ", ".join(
            f"{row[word]} {word.replace('-', ' ')}" for word in _JUDGING_WORDS if _whole(row.get(word))
        )

    lines = [f"  releases: {counted(judging)}"]
    labels = judging.get("labels")
    for row in labels if isinstance(labels, Sequence) and not isinstance(labels, str) else ():
        if isinstance(row, Mapping):
            name = row.get("label_name") or row.get("label_id") or "(no label)"
            lines.append(f"    {name}: {counted(row)}")
    if _whole(judging.get("held")) and judging["held"]:
        lines.append("  the held releases are listed by: crate label held")
    return lines


def _resolution_lines(job_id: str, state: str, progress: Mapping[str, Any]) -> list[str]:
    """An intake job's resolution, counted by state, then what to run next.

    Only the words the progress carries, each with its reasons when present
    (R-682), so nothing uncounted reads as zero.
    """
    lines = []
    for word, said in _RESOLUTION_WORDS:
        count = progress.get(word)
        if not _whole(count):
            continue
        lines.append(f"  {word}: {count} {said}")
        reasons = _reasons_for(progress, word, count)
        if reasons:
            lines.append(f"    by reason: {reasons}")
    if state == "succeeded" and _whole(progress.get("missing")) and progress["missing"]:
        # Only a succeeded job, since ``intake missing`` refuses every other.
        lines.append(f"  next: crate intake missing --job {job_id}")
    return lines


def _whole(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _reasons_for(progress: Mapping[str, Any], word: str, count: int) -> str:
    """One state's reasons as ``slug count`` pairs, most rows first, or empty.

    Slugs print as the report spells them, since a person greps for them. Rows
    no reason explains are said as ``unstated N`` last, so a partial breakdown
    never reads as complete.
    """
    by_reason = progress.get("by_reason")
    if not isinstance(by_reason, Mapping):
        return ""
    reasons = by_reason.get(word)
    if not isinstance(reasons, Mapping):
        return ""
    counted = [
        (str(why), n) for why, n in reasons.items() if _whole(n) and n > 0
    ]
    counted.sort(key=lambda pair: (-pair[1], pair[0]))
    unstated = count - sum(n for _, n in counted)
    if unstated > 0:
        counted.append(("unstated", unstated))
    return ", ".join(f"{why} {n}" for why, n in counted)


def _proof_line(item: Mapping[str, Any]) -> str:
    """One run of an import proof, worded by the action ``intake imported`` marked it.

    An unknown action keeps its own fields rather than being dropped.
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

    Gated on the verb as well as the schema, since plan items are shaped by
    the verb that plans.
    """
    if not envelope.schema.startswith("plan/") or envelope.verb != "intake.imported":
        return []
    items = envelope.data.get("items")
    if not isinstance(items, (list, tuple)) or not items:
        return []
    lines = [""]
    for item in items:
        lines.append(f"  {_proof_line(item) if isinstance(item, Mapping) else _shown_value(item)}")
    # The run count is the verb's own total, so human and machine summaries
    # agree; tracks and files are summed from the items.
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

    Ordered what happened, what a person still has to do, then the failure
    detail, since a reader wants the remedy first. ``drive`` is described at
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
    lines += render_job_list(envelope)
    lines += render_stale_cancel(envelope)
    lines += render_import_proof(envelope)
    lines += render_waiting_gate(envelope)

    for warning in envelope.warnings:
        lines.append(f"warning [{warning.get('code', '?')}]: {warning.get('message', '')}")

    lines.append(f"run: {envelope.run_id}")
    return "\n".join(lines) + "\n"


def _shown_lines(shown: Mapping[str, Any]) -> list[str]:
    """What the verb consulted, rendered under the gate's question.

    One line per fact, collections expanded rather than printed as a repr. The
    keys are the verb's, uninterpreted here.
    """
    lines: list[str] = []
    for name, value in shown.items():
        if isinstance(value, (Mapping, list, tuple)) and not value:
            # An empty collection says so, unlike a list that failed (R-686).
            lines.append(f"  {name}: none")
        elif isinstance(value, Mapping):
            lines.append(f"  {name}:")
            for key, entry in value.items():
                lines.append(f"    {key}: {_shown_value(entry)}")
        elif isinstance(value, (list, tuple)):
            lines.append(f"  {name}:")
            for item in value:
                if isinstance(item, Mapping):
                    lines.append(
                        "    " + ", ".join(f"{k}={_item_value(v)}" for k, v in item.items())
                    )
                else:
                    lines.append(f"    {_shown_value(item)}")
        else:
            lines.append(f"  {name}: {_shown_value(value)}")
    return lines


#: What makes a free text value read as more than one field on a ``k=v, k=v``
#: line, or as more than one line.
_FIELD_BREAKERS = (",", "=", "\n", "\r")


def _item_value(value: Any) -> str:
    """One value on an item's ``k=v, k=v`` line, quoted when it would break it.

    Free text holding a comma, equals sign or line break prints as a JSON string
    so it cannot read as another field (R-692).
    """
    if isinstance(value, str) and any(mark in value for mark in _FIELD_BREAKERS):
        return json.dumps(value, ensure_ascii=False)
    return _shown_value(value)


def _shown_value(value: Any) -> str:
    """One carried value as a person should read it, with words for None and bools."""
    if value is None:
        return "none"
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return str(value)


#: The line a stale answer's screen opens with (R-1334).
STALE_SCREEN = (
    "The plan moved since this gate was answered. This is the plan this run "
    "reads now, and an answer recorded on the run now is taken over it:"
)


def is_gate_screen(cause: Cause) -> bool:
    """Whether a refusal carries a gate's screen, which :func:`render_gate` prints.

    An open gate always does. A stale answer does when the gate itself raised
    it over the plan it now offers (R-1334), which its options mark; a stale a
    verb raised on its write handle binds no new offer and carries none.
    """
    if cause.reason == "decision-required":
        return True
    return cause.reason == "decision-stale" and "options" in (cause.detail or {})


def render_gate(cause: Cause) -> str:
    """The decision screen: the question, the options, and how to answer it.

    Options come from the gate declaration, so a new one cannot be forgotten.
    The refusal's ``shown`` context is rendered here or reaches no human
    (:class:`cratekit.cli.gates.DecisionRequired`); absent stays absent.
    """
    detail = cause.detail
    gate = detail.get("gate", "?")
    options = detail.get("options") or []
    run_id = detail.get("run_id", "<run>")
    stale = cause.reason == "decision-stale"
    # A stale answer's screen is the moved plan, and says so first (R-1334).
    lines = [STALE_SCREEN, ""] if stale else []
    lines += [
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
        # U168: the same answer, carried straight on into the verb's next step.
        "  then:    add --continue to answer and carry on the run in one command",
    ]
    if not detail.get("explicit"):
        # No inline answer on a stale screen, since it would refuse again.
        if not stale:
            lines.append(f"  or:      rerun with -d {gate}=<option>")
    else:
        lines.append(
            "  this gate takes no inline answer: it must be asserted on its own, "
            "and the assertion records who made it"
        )
    return "\n".join(lines) + "\n"


#: The verb whose summary carries a waiting gate's kept screen (U961).
_RUN_SHOW = "run.show"


def render_waiting_gate(envelope: Envelope) -> list[str]:
    """The gate ``crate run show`` names as waiting, on the screen its refusal printed (U961).

    A kept screen is rendered by :func:`render_gate` from the fields the
    refusal carried, so a person reads in another process what the refusal
    printed; a cut screen, and a gate whose screen cannot be shown, each name
    the command that shows the whole plan. Nothing for any other verb.
    """
    if envelope.verb != _RUN_SHOW:
        return []
    summary = envelope.data.get("summary")
    gate = summary.get("gate") if isinstance(summary, Mapping) else None
    if not isinstance(gate, Mapping):
        return []
    name = gate.get("name", "?")
    missing = gate.get("screen_missing")
    if isinstance(missing, Mapping):
        return [
            "",
            f"The run waits at {name}, with no screen to show: {missing.get('reason')}.",
            f"  show it: {missing.get('command')}",
            f"  answer:  {gate.get('answer')}",
        ]
    stale = gate.get("kind") == gates.SCREEN_STALE
    detail: dict[str, Any] = {
        "gate": name,
        "options": list(gate.get("options") or ()),
        "prompt": gate.get("prompt"),
        "explicit": gate.get("explicit"),
        "run_id": summary.get("run_id"),
    }
    if gate.get("shown") is not None:
        detail["shown"] = gate["shown"]
    screen = Cause(
        reason="decision-stale" if stale else "decision-required",
        message=f"run {summary.get('run_id')} waits at the gate {name!r}",
        remediation=cause_module.Remediation(
            remedy=Remedy.REPLAN_THEN_DECIDE if stale else Remedy.ANSWER_DECISION
        ),
        detail=detail,
    )
    # A cut is said before the screen, so it is read before the items are.
    cut = gate.get("cut")
    lines = [""] + (_cut_lines(cut, gate.get("continue")) if isinstance(cut, Mapping) else [])
    return lines + render_gate(screen).splitlines()


def _cut_lines(cut: Mapping[str, Any], command: Any) -> list[str]:
    """What a kept screen left out to stay small, and how to see it whole (U961)."""
    lists = cut.get("lists")
    if isinstance(lists, Mapping) and lists:
        said = "; ".join(
            f"{name}: the first {one.get('kept')}, and {one.get('left_out')} more not kept"
            for name, one in lists.items()
            if isinstance(one, Mapping)
        )
    else:
        dropped = ", ".join(str(one) for one in cut.get("dropped") or ())
        said = f"only the digest and the count, not {dropped or 'the facts'}"
    return [
        f"The run kept this screen short, {cut.get('limit')} characters at most: {said}.",
        f"  whole:   {command}",
        "",
    ]


__all__ = [
    "access_note",
    "install_command",
    "is_gate_screen",
    "remediation_line",
    "remedy_text",
    "render",
    "render_cause",
    "render_checks",
    "render_gate",
    "render_import_proof",
    "render_job_state",
    "render_stale_cancel",
    "render_review_set",
    "render_waiting_gate",
]
