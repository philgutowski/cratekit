"""Where rekordbox keeps its analysis files, and the one join that finds them (R-14).

The store is ``share`` beside ``master.db``, never the volume root's
``PIONEER/USBANLZ`` export cache, and ``AnalysisDataPath`` is share relative,
so joining it to the library root resolves zero rows. A database outside the
library root leaves no grid under the root at all.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath

from cratekit.core import config

#: The directory beside the database that holds the analysis store.
SHARE_DIRNAME = "share"


def share_root(cfg: config.Config) -> Path:
    """The directory every ``AnalysisDataPath`` is relative to, beside the CONFIGURED database."""
    return config.state_path("rekordbox_db", cfg).parent / SHARE_DIRNAME


def analysis_file(cfg: config.Config, stored: str) -> Path | None:
    """Where one row's stored ``AnalysisDataPath`` is on disk, None for no analysis recorded.

    A stored ``..`` is refused, since it is a corrupt or hostile row and the store is the share.
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

    The share joins the root when outside it, or the watch is barren and reports
    a clean session whatever happened to the grids.
    """
    root = Path(cfg.library.root)
    share = share_root(cfg)
    if config.is_inside(share, root):
        return (root,)
    return (root, share)


def is_watched(cfg: config.Config, path: Path) -> bool:
    """Whether ``path`` is under a watched root, where new analysis files fail a session (R-338)."""
    return any(config.is_inside(Path(path), root) for root in watch_roots(cfg))

