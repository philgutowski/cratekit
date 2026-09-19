"""A missing ``yt-dlp`` as the calling verb's refusal, the install hint and all.

ONE SPELLING, TWO VERB FAMILIES. ``acquire fallback`` searches and downloads
through ``yt-dlp`` (U80) and ``intake set`` fetches a mix through it (U104). The
refusal lived in the first one's command line module, and the second could only
reach it by importing that module from inside a function, because that module
imports ``intake.missing_cli`` and that imports ``intake.cli``. It uses nothing
but :mod:`core.binaries`, :mod:`core.cause` and the remedy vocabulary, so it
belongs here, below both.

``said`` AND ``origin`` ARE REQUIRED. They are the caller's, and a default
would report one verb's sentence under another verb's name.
"""

from __future__ import annotations

from typing import Any

from cratekit.core import binaries
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy


def yt_dlp_missing(
    exc: binaries.BinaryNotFound,
    subject: dict[str, Any],
    *,
    said: str,
    origin: tuple[str, ...],
) -> CratekitError:
    """The ``yt-dlp-missing`` refusal for one :class:`binaries.BinaryNotFound`.

    The binaries module already decided which of its situations this is, so
    the remedy IS its token: install, install from source, or fix the override.
    The hint travels as data for the command line layer to render (D2).
    """
    hint = exc.hint
    return refuse(
        "yt-dlp-missing",
        f"{exc} {said}",
        remedy=Remedy(exc.remedy.value),
        steps=(
            (f"install {', '.join(hint.packages)} with {hint.manager}, then run it again",)
            if hint is not None
            else ()
        ),
        scope=Scope.RUN,
        origin=origin,
        detail={
            "binary": exc.binary,
            "override": binaries.env_var(exc.binary),
            "manager": str(hint.manager) if hint is not None else None,
            "packages": list(hint.packages) if hint is not None else [],
            **subject,
        },
    )


__all__ = ["yt_dlp_missing"]
