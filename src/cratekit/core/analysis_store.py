"""Where rekordbox keeps its analysis files, and the one join that finds them.

R-14. A rekordbox library on an external volume has TWO directory trees ending
in ``PIONEER/USBANLZ``, and only one of them is the analysis store:

* ``PIONEER/Master/share/PIONEER/USBANLZ/`` is keyed by UUID, holds the beat
  grids, and is where every local row's analysis resolves. Measured on the
  source library on 2026-08-02: 10,066 of 10,070 rows.
* ``PIONEER/USBANLZ/`` at the volume root is the USB export cache, written when
  rekordbox exports to a device. A different key shape, regenerable, and ZERO
  rows resolve into it.

``djmdContent.AnalysisDataPath`` is stored SHARE RELATIVE
(``/PIONEER/USBANLZ/8d2/...``). Joined to the library root it resolves zero
rows, which reads as "the analysis files are missing" and is a measurement
artifact rather than a defect. The source repository paid for that twice: once
as a false open item, and once as a grid rollback step that named the export
cache and would have protected regenerable device output while leaving every
grid it existed for uncovered.

THE SHARE IS THE DATABASE'S SIBLING, NOT A FIXED PLACE UNDER THE LIBRARY. It is
``share`` beside ``master.db``, which is ``PIONEER/Master/share`` on an external
volume and ``~/Library/Pioneer/rekordbox/share`` at the platform default. A
database outside the library root is an acknowledged configuration (see
``LibraryConfig.db_outside_root_acknowledged_on``), and in that layout the
library root holds no grid at all, so anything that looks for analysis under the
root alone looks at nothing.

Layer note: INFRASTRUCTURE, by the ``core`` default. It resolves paths from the
configuration and touches no file.
"""

from __future__ import annotations

import os
from pathlib import Path, PurePosixPath

from cratekit.core import config

#: The directory beside the database that holds the analysis store.
SHARE_DIRNAME = "share"


def share_root(cfg: config.Config) -> Path:
    """The directory every ``AnalysisDataPath`` is relative to.

    Derived from the CONFIGURED database path, never from an assumed vendor
    layout under the library root, for the reason
    :func:`cratekit.modules.tools.backup.database_target_for` gives: the
    database's location is the user's decision, made in rekordbox, not ours.
    """
    return config.state_path("rekordbox_db", cfg).parent / SHARE_DIRNAME


def analysis_file(cfg: config.Config, stored: str) -> Path | None:
    """Where one row's stored ``AnalysisDataPath`` actually is on disk.

    ``None`` for an empty value, which is a track with no analysis recorded and
    is a different fact from an analysis file that is missing. Whether the
    returned path exists is the caller's question to ask, and asking it of the
    join below is the only way the answer means anything.

    A value that would climb out of the share is refused rather than joined. The
    store is the share and nothing else, so a stored ``..`` is either a corrupt
    row or a hostile one, and resolving it would read a file this function was
    never asked about.
    """
    parts = tuple(
        part for part in PurePosixPath(stored.replace("\\", "/")).parts if part != "/"
    )
    if not parts:
        return None
    if ".." in parts:
        raise ValueError(
            f"the stored analysis path {stored!r} climbs out of the analysis share, "
            f"and every analysis file this library holds is inside it"
        )
    return share_root(cfg).joinpath(*parts)


def watch_roots(cfg: config.Config) -> tuple[Path, ...]:
    """The roots a destructive session arms its analysis watch over.

    The library root always, because a write can touch any file under it. The
    share as well when it sits outside the root, because in that layout the root
    holds no grid and a watch over it alone fingerprints nothing, which reports a
    clean session whatever happened to the grids. That is the barren watch
    ``docs/solutions/integration-issues/a-guard-that-refuses-an-empty-list-cannot-see-a-barren-one.md``
    describes, reached through the configuration rather than through a caller.

    The share is left out when the root already contains it, only so the common
    layout is walked once rather than twice. The watch matches by file name and
    deduplicates what it finds, so including it would change nothing but the
    time.
    """
    root = Path(cfg.library.root)
    share = share_root(cfg)
    if _is_within(share, root):
        return (root,)
    return (root, share)


def is_watched(cfg: config.Config, path: Path) -> bool:
    """Whether ``path`` sits under a root the analysis watch covers.

    Asked by anything that is about to PUT analysis files somewhere, because a
    session armed over :func:`watch_roots` refuses at its close when an analysis
    file under them appeared or changed, whoever moved it and however good the
    reason (R-338).
    """
    return any(_is_within(Path(path), root) for root in watch_roots(cfg))


def _is_within(child: Path, parent: Path) -> bool:
    """True when ``child`` is ``parent`` or sits under it, compared textually.

    ``normpath`` rather than ``resolve``, so the answer does not depend on the
    volume being mounted when the question is asked.
    """
    child_parts = Path(os.path.normpath(str(child))).parts
    parent_parts = Path(os.path.normpath(str(parent))).parts
    return child_parts[: len(parent_parts)] == parent_parts


__all__ = ["SHARE_DIRNAME", "analysis_file", "is_watched", "share_root", "watch_roots"]
