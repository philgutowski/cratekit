"""Marks wait until the local output exists.

A playlist is marked (a taken entry in Cratekit's own record, U242) only after
the importable file is on disk and a recheck shows the remote side unchanged.
Marking first lets a crash leave a playlist taken with nothing to import.
"""

from __future__ import annotations

import os
import stat
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.core.cause import CratekitError, Scope, refuse


@dataclass(frozen=True, slots=True)
class PendingMark:
    """One remote side effect, keyed by a stable target id, never a title."""

    target_id: str
    kind: str


def blocked(origin: Sequence[str], message: str, /, *steps: str, **detail: Any) -> CratekitError:
    """The refusal a verb over the account's marks ends on, with the verb's own origin."""
    return refuse(
        "sync-marks-blocked",
        message,
        steps=steps,
        scope=Scope.SOURCE,
        origin=origin,
        detail=detail,
    )


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

    One ``os.stat`` answers exists, is a file and is non empty, so a file
    removed between two reads cannot escape as a bare ``OSError`` (R-398).
    Every ``OSError`` is the refusal, chained as the cause so a permission
    error gets its own remedy. A caller fingerprints the returned stat rather
    than reading again.
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

    A native landing writes no importable file, so this stands in for it: the
    caller read the medium as native and resolved every unfound track against
    the library before planning a mark. ``sync mark --pass`` is the one maker.

    A TYPE AND NOT A MISSING ARGUMENT, so a ``None`` is still refused.
    """

    tree_id: str
    pass_name: str
    #: The closed native landings that committed the pass, which a mark waits for.
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
    """Apply marks whose recheck still holds, after the local proof is real.

    Returns the ids actually marked. A failed recheck skips the mark, since the
    remote item changed and the next increment sees it again.
    """
    require_proof(local_output)
    applied: list[str] = []
    for mark in pending:
        if not recheck(mark):
            continue
        apply(mark)
        applied.append(mark.target_id)
    return tuple(applied)
