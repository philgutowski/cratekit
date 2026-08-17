"""Set identification, gated before any paid call.

Recognition here is ACRCloud, reached through the operator's own key. This
module does not use a watermark, does not take a date floor, and does not
ask sync how far a previous run got (KTD11). Scope of a set is the audio
the caller handed over, plus owned-dedup later in matching.

The spend gate is presence, not retrieval. Doctor's recognition check
records that both keys exist. Retrieving them here would prompt the
keychain on macOS, which is how an unattended run hangs. The first paid
call is the first retrieval, and it happens only after this gate has
passed.

A missing helper binary (ffmpeg, used to carve the 12 second chunks) is
the same class of refusal: report it before any spend, not after the
first failed carve.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from cratekit.acquire.match import Wanted
from cratekit.core import binaries, secrets
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy

Identifier = Callable[[Path], tuple[Wanted, ...]]


def recognition_ready() -> tuple[str, ...]:
    """Names of the things that are missing, empty when spend may start."""
    missing: list[str] = []
    if not secrets.exists(str(secrets.Credential.IDENTIFY_KEY)):
        missing.append(str(secrets.Credential.IDENTIFY_KEY))
    if not secrets.exists(str(secrets.Credential.IDENTIFY_SIGNING_KEY)):
        missing.append(str(secrets.Credential.IDENTIFY_SIGNING_KEY))
    if binaries.find("ffmpeg") is None:
        missing.append("ffmpeg")
    return tuple(missing)


def assert_recognition_ready() -> None:
    """Refuse before any paid call if a key or the carve binary is missing."""
    missing = recognition_ready()
    if not missing:
        return
    raise refuse(
        "intake-recognition-unready",
        "recognition cannot start because "
        + ", ".join(missing)
        + " is not recorded on this machine; reporting that now is the "
        "difference between a refusal and a paid call that cannot finish",
        remedy=Remedy.SET_CREDENTIAL,
        origin=("intake.recognize",),
        detail={"missing": list(missing)},
    )


def identify(
    source: Path,
    *,
    identifier: Identifier | None = None,
) -> tuple[Wanted, ...]:
    """Identify the tracks in ``source`` and return them as Wanted rows.

    Downloads nothing. Writes nothing. The caller decides whether to persist
    a tracklist. ``identifier`` is injected so the suite can prove the gate
    and the shape without spending.
    """
    assert_recognition_ready()
    if identifier is None:
        raise refuse(
            "intake-recognition-unready",
            "no identifier is bound in this build, so a paid recognition "
            "call cannot be made; bind one or stay in identification tests",
            remedy=Remedy.SET_CREDENTIAL,
            origin=("intake.recognize",),
        )
    return identifier(source)


def tracklist_text(rows: tuple[Wanted, ...] | list[Wanted] | Any) -> str:
    """A plain tracklist, one 'Artist - Title' line per row. No downloads."""
    lines = []
    for row in rows:
        version = f" ({row.version})" if getattr(row, "version", "") else ""
        lines.append(f"{row.artist} - {row.title}{version}")
    return "\n".join(lines) + ("\n" if lines else "")
