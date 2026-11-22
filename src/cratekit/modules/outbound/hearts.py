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

# Names a caller might use to ask for a remove, so the engine can see them and
# still refuse to act on them. A new remove API would have to be written.
REMOVE_FLAGS = frozenset(
    {
        "remove", "unheart", "unlike", "uncolor", "clear", "delete", "mirror", "subtract",
        "sync_removals", "remove_missing", "drop_unhearted", "no_heartback",
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

    ``release_title`` (the title with the naming head off) and ``artist`` let the
    account choose among releases sharing the row's ISRC (R-356), never searched on.
    """

    row_id: str
    remote_id: str = ""
    isrc: str = ""
    release_title: str = ""
    artist: str = ""
    #: The file's album tag, choosing among releases spelled alike (R-572).
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


def heart_back(
    cfg: config.Config,
    account: RemoteAccount,
    candidates: Sequence[HeartCandidate],
    *,
    colors: LocalColors | None = None,
    flags: Mapping[str, Any] | None = None,
) -> HeartReport:
    """Heart each matched favourite. Never removes a heart or a colour.

    ``flags`` is accepted, and ignored, so a caller still thinking in mirror
    mode cannot get a different function.
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
        tuple(hearted), tuple(already), tuple(colored), tuple(unmatched), tuple(reasons)
    )


def remove_requested(flags: Mapping[str, Any] | None) -> bool:
    """Whether the caller asked for a remove, in any spelling. The engine still will not do it."""
    folded = {item.replace("_", "") for item in REMOVE_FLAGS}
    return any(
        value and str(key).replace("-", "_").casefold().replace("_", "") in folded
        for key, value in (flags or {}).items()
    )
