"""Irreversible remote marks wait until the local output exists.

Deferred prefixing: a provider playlist is renamed only after the importable
file is on disk, and only after a recheck shows the remote side is still the
thing the run planned to mark. Applying the mark first is how a crash leaves
the provider believing the run finished while the library has nothing to import.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from cratekit.core.cause import Scope, refuse


@dataclass(frozen=True, slots=True)
class PendingMark:
    """One remote side effect, keyed by a stable target id, never a title."""

    target_id: str
    kind: str


def apply_deferred(
    pending: Sequence[PendingMark],
    *,
    local_output: Path,
    recheck: Callable[[PendingMark], bool],
    apply: Callable[[PendingMark], None],
) -> tuple[str, ...]:
    """Apply marks whose recheck still holds, after the local file is real.

    Returns the target ids that were actually marked. A failed recheck skips
    that mark rather than forcing it: the remote item changed, and the next
    increment will see it again.
    """
    if not local_output.is_file() or local_output.stat().st_size == 0:
        raise refuse(
            "sync-marks-blocked",
            f"a remote mark was requested before {local_output.name} existed; "
            f"the local importable file is the proof the increment finished",
            steps=("write the importable file, then mark the remote side",),
            scope=Scope.SOURCE,
            origin=("sync.marks",),
            detail={"path": str(local_output)},
        )
    applied: list[str] = []
    for mark in pending:
        if not recheck(mark):
            continue
        apply(mark)
        applied.append(mark.target_id)
    return tuple(applied)
