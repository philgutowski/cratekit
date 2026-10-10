"""Reverse heart-back: pink local favourites become remote hearts, add-only.

The source system's add-only union is load-bearing (R36): a heart marks a
favourite, not ownership, and un-hearting is a one-tap action that must not
cost a file. This module has no remove path. Flags and config keys that
sound like a remove are ignored so no combination can un-heart or un-color.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from cratekit.core import config
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound.service import RemoteAccount

# Names a caller might use to ask for a remove. Present so the engine can
# see them and still refuse to act on them. A new alias added here is
# ignored the same way; a new remove API would have to be written.
REMOVE_FLAGS = frozenset(
    {
        "remove",
        "unheart",
        "unlike",
        "uncolor",
        "clear",
        "delete",
        "mirror",
        "subtract",
        "sync_removals",
        "remove_missing",
        "drop_unhearted",
        "no_heartback",
    }
)


class LocalColors(Protocol):
    """Local pink colour. Add-only: there is no clear on this protocol."""

    def color_pink(self, row_id: str) -> None:
        """Mark one library row pink. Idempotent if already pink."""

    def is_pink(self, row_id: str) -> bool:
        """Whether this library row is already pink."""


@dataclass(frozen=True, slots=True)
class HeartCandidate:
    """One library favourite that may be hearted remotely.

    ``release_title`` is the row's title with the library's naming head off, and
    with ``artist`` it lets the account choose among several releases sharing
    the row's ISRC (R-356). Neither is ever searched on.
    """

    row_id: str
    remote_id: str = ""
    isrc: str = ""
    release_title: str = ""
    artist: str = ""
    #: The album tag of the row's own file, which chooses among releases
    #: spelled alike under one ISRC when none is hearted (R-572).
    album: str = ""


@dataclass(frozen=True, slots=True)
class HeartReport:
    """What one heart-back pass wrote, and what it left alone.

    ``reasons`` pairs an unmatched row with what the account said about it, and
    carries only the rows it said something about.
    """

    hearted: tuple[str, ...]
    already: tuple[str, ...]
    colored: tuple[str, ...]
    unmatched: tuple[str, ...]
    reasons: tuple[tuple[str, str], ...] = ()


def _remove_requested(flags: Mapping[str, Any] | None) -> bool:
    if not flags:
        return False
    for key, value in flags.items():
        folded = str(key).replace("-", "_").casefold()
        if folded in REMOVE_FLAGS or folded.replace("_", "") in {
            item.replace("-", "").replace("_", "") for item in REMOVE_FLAGS
        }:
            if value:
                return True
    return False


def heart_back(
    cfg: config.Config,
    account: RemoteAccount,
    candidates: Sequence[HeartCandidate],
    *,
    colors: LocalColors | None = None,
    flags: Mapping[str, Any] | None = None,
) -> HeartReport:
    """Heart each matched favourite. Never removes a heart or a colour.

    ``flags`` is accepted so a caller that still thinks in mirror mode cannot
    accidentally get a different function. Remove-shaped keys are ignored.
    """
    del flags  # add-only: a remove request does not change the write set
    hearted: list[str] = []
    already: list[str] = []
    colored: list[str] = []
    unmatched: list[str] = []
    reasons: list[tuple[str, str]] = []
    known = set(ledger.recorded_hearts(cfg))
    for item in candidates:
        remote = item.remote_id or account.match_track(
            identity=item.row_id,
            isrc=item.isrc,
            title=item.release_title,
            artist=item.artist,
            album=item.album,
        )
        if not remote:
            unmatched.append(item.row_id)
            reason = account.unmatched_reason(item.row_id)
            if reason:
                reasons.append((item.row_id, reason))
            continue
        if colors is not None and not colors.is_pink(item.row_id):
            colors.color_pink(item.row_id)
            colored.append(item.row_id)
        if remote in known or account.has_heart(remote):
            already.append(remote)
            continue
        account.add_heart(remote)
        ledger.record_heart(cfg, remote)
        known.add(remote)
        hearted.append(remote)
    return HeartReport(
        hearted=tuple(hearted),
        already=tuple(already),
        colored=tuple(colored),
        unmatched=tuple(unmatched),
        reasons=tuple(reasons),
    )


def remove_requested(flags: Mapping[str, Any] | None) -> bool:
    """Whether the caller asked for a remove. The engine still will not do it."""
    return _remove_requested(flags)
