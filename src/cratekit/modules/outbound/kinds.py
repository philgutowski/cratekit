"""The root folder each kind of playlist is filed in, by a rule a person can read (U131).

THE SCHEME KEEPS THE ACCOUNT'S ROOT SHAPES. A followed label's playlists sit in
a root folder named as the label (R-835); an archived set and a marked custom
playlist sit in a root folder named as the year (R-837, U116). This module adds
the two kinds those leave at the root:

* ``Exports``, every playlist ``export playlist`` made, by the ledger's record;
* ``Mine``, every playlist at the root that no ledger claims, which is the
  author's own, except a set still waiting for its archive.

A kind's folder is found the way a year's is: the folder recorded for the kind
and still listed at the root, else the one root folder named as the kind, else
a new one made on apply. Two root folders under the kind's name leave the
kind's playlists where they are, since a name does not decide which is meant.

ADD ONLY. A folder is created and a playlist is put in one. Nothing is renamed
or removed.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from cratekit.core import config
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound.service import RemoteAccount

MINE = "Mine"
EXPORTS = "Exports"
KINDS = (EXPORTS, MINE)

#: What happens to a kind's folder, the set archive's words.
CREATE = "create"
REUSE = "reuse"
ADOPT = "adopt"
LEFT = "left"


@dataclass(frozen=True, slots=True)
class KindFolder:
    """One kind's folder as a plan found it."""

    kind: str
    action: str
    folder_id: str = ""
    #: A recorded folder the account no longer lists, so its record is replaced.
    stale: str = ""
    #: Set when the kind cannot be placed, and then nothing of the kind moves.
    why: str = ""
    #: Whether this product made the folder, by the ledger, so a playlist may
    #: be moved out of it again. A folder adopted by its name never is.
    made: bool = False


def decide(cfg: config.Config, kind: str, root: Mapping[str, str]) -> KindFolder:
    """The kind's folder against the ledger and the root folders. Reads only."""
    recorded = ledger.kind_folder(cfg, kind)
    if recorded.folder_id and recorded.folder_id in root:
        return KindFolder(kind, REUSE, recorded.folder_id, made=recorded.created)
    named = sorted(folder_id for folder_id, title in root.items() if title == kind)
    if len(named) > 1:
        return KindFolder(
            kind,
            LEFT,
            stale=recorded.folder_id,
            why=(
                f"the account holds {len(named)} root folders named {kind!r}, so which "
                f"one is the kind's is not something its name decides"
            ),
        )
    if named:
        return KindFolder(kind, ADOPT, named[0], stale=recorded.folder_id)
    return KindFolder(kind, CREATE, stale=recorded.folder_id)


def reserve(
    cfg: config.Config, account: RemoteAccount, folder: KindFolder, made: list[str] | None = None
) -> str:
    """The kind's folder identifier, made once if the plan found none.

    ``made`` is the caller's, and has the kind appended as soon as the provider
    answers a create, so a ledger write that then raises still names it.
    """

    def create() -> str:
        folder_id = account.create_folder(folder.kind)
        if made is not None:
            made.append(folder.kind)
        return folder_id

    folder_id, _created = ledger.reserve_kind_folder(
        cfg,
        folder.kind,
        create,
        adopt=folder.folder_id if folder.action == ADOPT else "",
        stale=folder.stale,
    )
    return folder_id


def file_new(cfg: config.Config, account: RemoteAccount, playlist_id: str, kind: str) -> str:
    """Put a playlist the product just made into its kind's folder; answer why not.

    Answers ``""`` once filed. A kind whose folder a name cannot decide is
    left with that reason, and the playlist stays at the root for ``crate
    organize`` to list. A provider refusal is raised to the caller.
    """
    folder = decide(cfg, kind, account.folders())
    if folder.why:
        return folder.why
    account.move_to_folder(playlist_id, reserve(cfg, account, folder))
    return ""


__all__ = [
    "ADOPT",
    "CREATE",
    "EXPORTS",
    "KINDS",
    "KindFolder",
    "LEFT",
    "MINE",
    "REUSE",
    "decide",
    "file_new",
    "reserve",
]
