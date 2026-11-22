"""What a backup run reports: the comparison rclone made, and the plan and outcome as data.

Split out of :mod:`cratekit.modules.tools.backup`, which re-exports every name
here and is the module to import; this one reads the backup module's labels and
types, so it is loaded through it. Renderers only: nothing here decides a run.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence

from cratekit.modules.tools import backup_record
from cratekit.modules.tools.backup import (
    COMPARISON_FAST,
    COMPARISON_FULL,
    COMPARISON_QUICK,
    FAST_LIST,
    QUICK_LABELS,
    QUICK_RESEND,
    QUICK_SEND,
    RECORD_TOKEN,
    BackupOutcome,
    BackupPlan,
    Command,
    CommandResult,
    PortionPlan,
)


def comparison_mode(command: Command) -> str:
    """Which listing one mirror command used, read off the command as run."""
    return COMPARISON_FAST if FAST_LIST in command.argv else COMPARISON_FULL


def _parsed(line: str) -> object:
    try:
        return json.loads(line)
    except ValueError:
        return None


def _logged(stderr: str) -> list[dict]:
    """The JSON objects one command logged, skipping every line that is not one."""
    return [entry for entry in map(_parsed, stderr.splitlines()) if isinstance(entry, dict)]


def _count(stats: Mapping[str, object], key: str) -> int | float | None:
    """One total, or None when rclone gave no number; a bool is refused, being
    an ``int`` to ``isinstance``."""
    value = stats.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def comparison_report(command: Command, result: CommandResult) -> dict[str, object]:
    """What one mirror's comparison did: the mode, the time, and the counts.

    A count that could not be read is None, never zero. ``checked`` is rclone's
    count of files found on both sides; ``seconds`` is the whole command, and
    ``transfer_seconds`` rclone's own total. The last totals logged are read.
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
        # rclone's own names and counting; how many files went to the archive
        # is not derived from them.
        "renames": _count(stats, "renames"),
        "deletes": _count(stats, "deletes"),
    }


def _said(stderr: str) -> str:
    """What a failed command said, line by line: a logged object as its message,
    the totals dropped, and a plain line kept as written."""
    lines: list[str] = []
    for line in stderr.splitlines():
        entry = _parsed(line)
        if not isinstance(entry, dict):
            lines.append(line)
        elif "stats" not in entry:
            lines.append(str(entry.get("msg", "")))
    said = "\n".join(piece.strip() for piece in lines if piece.strip())
    return said or stderr.strip()


def _summary(
    entry: PortionPlan, comparison: Mapping[str, object] | None, seconds: float, *,
    token: str = "",
) -> dict[str, object]:
    """What a fact records about the run that completed it; ``record`` is the
    token a later quick run or skip trusts the record by."""
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
    """What a quick run's commands did, summed from each command's totals:
    ``sent`` by the copies, ``archived`` by the move and the copies' archive,
    ``checked`` the paths a copy found current. A total any command did not
    give makes its sum None, never zero."""

    def total(labels: frozenset[str], key: str) -> int | float | None:
        found = [comparison_report(c, r)[key] for c, r in ran if c.label in labels]
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
        # rclone counts each move into the archive as a rename.
        "archived": total(QUICK_LABELS, "renames"),
    }


PAYLOAD_VERSION = 1


def _listed(command: Command) -> dict[str, int]:
    """How many paths a command read on standard input, never the paths."""
    if command.feed is None:
        return {}
    return {"paths": len(backup_record.paths_from(command.feed))}


def _kind_fields(kind: str, why: str, changes: Mapping[str, int] | None) -> dict:
    return {
        "kind": kind or None, "why": why or None,
        "changes": dict(changes) if changes is not None else None,
    }


def plan_payload(plan: BackupPlan) -> dict:
    """A plan as plain data. Human rendering stays with the CLI."""
    return {
        "payload_version": PAYLOAD_VERSION, "stamp": plan.stamp,
        "portions": [
            {
                "portion": entry.portion.value, "will_run": entry.will_run,
                "refusal": entry.refusal.value if entry.refusal else None, "detail": entry.detail,
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
    """Render the outcome; nothing here interprets a return code. Fields that
    join leave ``PAYLOAD_VERSION`` as it is: it is bumped only when a field is
    removed or changes meaning."""
    return {
        "payload_version": PAYLOAD_VERSION, "stamp": outcome.stamp, "ok": outcome.ok,
        "dry_run": outcome.dry_run,
        "portions": [
            {
                "portion": entry.portion.value, "ran": entry.ran,
                "refusal": entry.refusal.value if entry.refusal else None, "detail": entry.detail,
                "warnings": [dict(warning) for warning in entry.warnings],
                "comparison": dict(entry.comparison) if entry.comparison is not None else None,
                # STRICT: both come from the same runner calls, and a mismatch
                # would pair a return code with the wrong argv.
                "commands": [
                    {
                        "label": command.label,
                        "argv": list(command.argv),
                        "returncode": result.returncode, **_listed(command),
                    }
                    for command, result in zip(entry.commands, entry.results, strict=True)
                ],
                **_kind_fields(entry.kind, entry.why, entry.changes),
                "seconds": entry.seconds,
            }
            for entry in outcome.portions
        ],
    }
