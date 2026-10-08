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


@dataclass(frozen=True, slots=True)
class NativeLanding:
    """The proof a pass landed on a database native intake tree (R-777).

    A native landing takes its files into the collection through the guarded
    writer and writes NO importable file, so the file this module waits for
    cannot exist. What stands in for it is what the file was evidence of: the
    caller read the intake tree's medium as native and resolved every track
    the pass did not find against the library, by ``acquire match``'s view,
    before planning a single mark. ``sync mark --pass`` is the one maker, and
    it reads the medium again before the first rename.

    A TYPE AND NOT A MISSING ARGUMENT. A ``None`` where the file belongs is
    still refused, so a caller that has neither proof is as wrong about the
    run as it was before this existed.
    """

    tree_id: str
    pass_name: str
    #: The closed native landings that committed the pass, which a mark waits
    #: for the way it waits for a file (R-777).
    landings: tuple[str, ...] = ()


def require_proof(local_output: Path | NativeLanding) -> os.stat_result | None:
    """The importable file's stat, the native proof as given, or the refusal."""
    if isinstance(local_output, NativeLanding):
        if not local_output.tree_id or not local_output.pass_name or not local_output.landings:
            raise refuse(
                "sync-marks-blocked",
                "a remote mark was requested on a database native intake tree with no "
                "pass, no tree or no landing named, so nothing proves the increment finished",
                steps=("name the pass with crate sync mark --pass",),
                scope=Scope.SOURCE,
                origin=("sync.marks",),
                detail={"tree_id": local_output.tree_id, "pass": local_output.pass_name},
            )
        return None
    if not isinstance(local_output, Path):
        raise refuse(
            "sync-marks-blocked",
            "a remote mark was requested with neither an importable file nor a native "
            "landing to prove the increment finished",
            steps=("write the importable file, then mark the remote side",),
            scope=Scope.SOURCE,
            origin=("sync.marks",),
            detail={"given": type(local_output).__name__},
        )
    return require_output(local_output)


def apply_deferred(
    pending: Sequence[PendingMark],
    *,
    local_output: Path | NativeLanding,
    recheck: Callable[[PendingMark], bool],
    apply: Callable[[PendingMark], None],
) -> tuple[str, ...]:
    """Apply marks whose recheck still holds, after the local file is real.

    Returns the target ids that were actually marked. A failed recheck skips
    that mark rather than forcing it: the remote item changed, and the next
    increment will see it again. On a database native intake tree the file is
    a :class:`NativeLanding` instead, see there.
    """
    require_proof(local_output)
    applied: list[str] = []
    for mark in pending:
        if not recheck(mark):
            continue
        apply(mark)
        applied.append(mark.target_id)
    return tuple(applied)
