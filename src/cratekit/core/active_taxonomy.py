"""The library's active taxonomy, the copy beside the database that doctor checks (R-685, S6).

Every verb routes by this copy, never by the shipped template, so a person's
edit to it takes effect. It is not in ``core/taxonomy`` because that module
reads no configuration value (KTD23, S3).

The shipped template stands in only when the library root is there and holds
no copy, a setup never finished that doctor already reports. Every other
failure to read refuses, because "could not look" is not "not present": an
absent library root is an unmounted volume, and falling back there would route
a person's tracks by a declaration that is not theirs.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.core import config, taxonomy
from cratekit.core.cause import access_remedy, refuse
from cratekit.core.exit_codes import Remedy

_ORIGIN = ("core", "active_taxonomy")


def read_text(cfg: config.Config) -> tuple[Path, str | None]:
    """The active copy's path and text, or None for the text when the library holds none.

    The one read for the loader and the upgrade (U132), so both refuse alike.
    None means the library root is a directory with no copy under it; every
    other failure refuses.
    """
    path = config.state_path("taxonomy_active", cfg)
    try:
        return path, path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError) as exc:
        if not cfg.library.root.is_dir():
            raise refuse(
                "library-volume-unmounted",
                f"the library root {cfg.library.root} is not there, so this "
                f"library's taxonomy at {path} could not be read and the shipped "
                f"template was not used in its place",
                remedy=Remedy.MOUNT_LIBRARY_VOLUME,
                origin=_ORIGIN,
                detail={"path": str(path)},
            ) from exc
        return path, None
    except (OSError, UnicodeDecodeError) as exc:
        raise refuse(
            "config-unusable",
            f"the active taxonomy template at {path} could not be read ({exc}), "
            f"so this library's declared tree is unknown and the shipped template "
            f"was not used in its place",
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
            origin=_ORIGIN,
            detail={"path": str(path)},
        ) from exc


def load(cfg: config.Config) -> taxonomy.Taxonomy:
    """The taxonomy this library declares, from its active copy on the volume.

    Falls back to the shipped template ``taxonomy.template`` names only when the
    library root holds no copy. Refuses an unmounted library and a copy that
    cannot be read or parsed, with doctor's remedy for each.
    """
    path, text = read_text(cfg)
    if text is None:
        return _shipped(cfg.taxonomy.template)
    try:
        return taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        raise refuse(
            "config-unusable",
            f"the active taxonomy template at {path} is not usable: {exc}",
            remedy=Remedy.RUN_SETUP,
            origin=_ORIGIN,
            detail={"path": str(path)},
        ) from exc


def _shipped(name: str) -> taxonomy.Taxonomy:
    """The shipped template the configuration names, which is not always ``default``."""
    try:
        text = taxonomy.shipped_template_text(name)
    except (OSError, ValueError) as exc:
        # An unknown name or an unreadable package: no declaration to route by,
        # and guessing one repairs nothing.
        raise refuse(
            "config-unusable",
            f"this library has no active taxonomy template and the shipped "
            f"template {name!r} could not be read ({exc})",
            remedy=Remedy.RUN_SETUP,
            origin=_ORIGIN,
        ) from exc
    return taxonomy.load_taxonomy(text)


__all__ = ["load", "read_text"]
