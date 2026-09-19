"""Irreversible remote marks wait until the local output exists.

Deferred prefixing: a provider playlist is renamed only after the importable
file is on disk, and only after a recheck shows the remote side is still the
thing the run planned to mark. Applying the mark first is how a crash leaves
the provider believing the run finished while the library has nothing to import.
"""

from __future__ import annotations

import os
import stat
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from cratekit.core.cause import CratekitError, Scope, refuse


@dataclass(frozen=True, slots=True)
class PendingMark:
    """One remote side effect, keyed by a stable target id, never a title."""

    target_id: str
    kind: str


def _blocked(local_output: Path, because: str) -> CratekitError:
    return refuse(
        "sync-marks-blocked",
        f"a remote mark was requested before {local_output.name} existed; "
        f"the local importable file is the proof the increment finished ({because})",
        steps=("write the importable file, then mark the remote side",),
        scope=Scope.SOURCE,
        origin=("sync.marks",),
        detail={"path": str(local_output)},
    )


def require_output(local_output: Path) -> os.stat_result:
    """The importable file's stat, or the refusal. THE PATH IS READ ONCE.

    One ``os.stat`` answers all three questions, is it there, is it a file, does
    it hold anything. The check used to be ``is_file()`` and then ``stat()``, and
    a file removed between the two raised ``FileNotFoundError`` out of the second
    as a bare ``OSError``, at the one step whose whole design is that it refuses
    (R-398). Every ``OSError`` is the refusal, a dead mount included, because a
    file this process cannot stat is not proof of anything. A permission error
    is chained as the cause, so ``core.cause`` reads it as the path refusal it
    is and the person is given the remedy for that and not for a missing file.

    The result is returned so a caller that wants to fingerprint the file it was
    shown uses THIS read and not a second one.
    """
    try:
        found = os.stat(local_output)
    except OSError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
    if not stat.S_ISREG(found.st_mode):
        raise _blocked(local_output, "it is not a file")
    if found.st_size == 0:
        raise _blocked(local_output, "it is empty")
    return found


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
    require_output(local_output)
    applied: list[str] = []
    for mark in pending:
        if not recheck(mark):
            continue
        apply(mark)
        applied.append(mark.target_id)
    return tuple(applied)
