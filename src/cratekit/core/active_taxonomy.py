"""The library's ACTIVE taxonomy, read from the file doctor checks (R-685).

WHY THIS MODULE EXISTS. Setup copies the chosen template beside the database
(S6), doctor reads that copy for ``taxonomy.active``, and a person is told the
copy is theirs to edit. Until R-685 no verb read it: every verb called
``taxonomy.default_taxonomy()``, which returns the SHIPPED template, so an edit
to the active copy changed nothing any verb did, and a section the shipped
template gained after setup, ``[long_tracks]`` on the tenth sitting's library,
built a playlist the active declaration never asked for.

It lives HERE rather than in ``core/taxonomy`` because that module reads no
configuration value (KTD23, S3) and is tested against two taxonomies in one
process on the strength of it. Resolving a library path needs a ``Config``, so
the one read that does is a module of its own, and every verb reads through it.

THE FALLBACK IS NARROW ON PURPOSE. The shipped template stands in only when the
library is there to look at and holds no active copy, which is a library setup
never finished, and doctor already reports that as a failure with its remedy.
Every other way of not reading the copy refuses, because each of them is "could
not look" rather than "not present": a library root that is absent is an
unmounted volume, and falling back there would route a person's tracks by a
declaration that is not theirs while their own sits on a disk nobody read.
"""

from __future__ import annotations

from cratekit.core import config, taxonomy
from cratekit.core.cause import access_remedy, refuse
from cratekit.core.exit_codes import Remedy

_ORIGIN = ("core", "active_taxonomy")


def load(cfg: config.Config) -> taxonomy.Taxonomy:
    """The taxonomy this library declares, from its active copy on the volume.

    The shipped template ``taxonomy.template`` names is the answer only when the
    library root is a directory and no active copy exists under it. Raises a
    refusal for an unmounted library, an active copy that could not be read,
    and one that does not parse, with the remedy doctor gives for each.
    """
    path = config.state_path("taxonomy_active", cfg)
    try:
        text = path.read_text(encoding="utf-8")
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
        return _shipped(cfg.taxonomy.template)
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
        # A name configuration accepted and nothing ships under, or a packaged
        # directory that could not be read. Doctor tells the two apart; here
        # both mean there is no declaration to route by, and neither is repaired
        # by guessing one.
        raise refuse(
            "config-unusable",
            f"this library has no active taxonomy template and the shipped "
            f"template {name!r} could not be read ({exc})",
            remedy=Remedy.RUN_SETUP,
            origin=_ORIGIN,
        ) from exc
    return taxonomy.load_taxonomy(text)


__all__ = ["load"]
