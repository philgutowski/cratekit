"""A missing ``yt-dlp`` as the calling verb's refusal, the install hint and all.

One spelling for ``acquire fallback`` (U80) and ``intake set`` (U104), kept
below both. ``said`` and ``origin`` are required: they are the caller's.
"""

from __future__ import annotations

from typing import Any

from cratekit.core import binaries
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy


def yt_dlp_missing(
    exc: binaries.BinaryNotFound, subject: dict[str, Any], *, said: str, origin: tuple[str, ...]
) -> CratekitError:
    """The ``yt-dlp-missing`` refusal for one :class:`binaries.BinaryNotFound`.

    The remedy is the exception's own token; the hint travels as data (D2).
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
