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

A missing helper binary (ffmpeg, used to carve the 12 second chunks, and
ffprobe, which measures the recording so the spend is known before the
first call) is the same class of refusal: report it before any spend, not
after the first failed carve.

The implementation behind the seam is :mod:`cratekit.intake.acrcloud`. It
landed in U57; until then ``identify`` refused on every real call.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire.match import Wanted
from cratekit.core import binaries, secrets
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy


@dataclass(frozen=True, slots=True)
class Identified:
    """What one identification found, and what it cost to find it.

    ``rows`` is the tracklist. The four counts are what a bare tuple of rows
    cannot say: how many paid calls were made, how many chunks the grid asked
    for, how many the service answered with nothing, and how many got NO
    answer at all. The last one is the one a report has to carry, because a
    set where most chunks were never answered is not a set nobody recognised,
    and the two look identical as a tuple of rows.

    ``calls`` is what THIS pass paid for. ``cached`` is how many of the chunks
    were answered from the recognition cache instead, so a second pass over an
    unchanged recording reads ``calls`` of zero and ``cached`` equal to
    ``chunks``. ``cache_unwritten`` is empty unless the answers this pass paid
    for could not be kept, and then it says why: the pass still succeeded, and
    the next one over the same recording will pay again, which a person is
    owed the chance to know before it happens.
    """

    rows: tuple[Wanted, ...]
    calls: int = 0
    chunks: int = 0
    misses: int = 0
    unreached: int = 0
    cached: int = 0
    cache_unwritten: str = ""


#: An identifier answers with an :class:`Identified`, or with the bare rows
#: when it has nothing to say about cost, which is what a fake in the suite
#: does. ``identify`` normalises the two.
Identifier = Callable[[Path], "Identified | tuple[Wanted, ...]"]

#: The binaries recognition needs, in the order a person would install them.
#: Both are checked by presence here and resolved again by the carver at call
#: time, so an override that points at nothing refuses there by name.
BINARIES = ("ffmpeg", "ffprobe")


def recognition_ready() -> tuple[str, ...]:
    """Names of the things that are missing, empty when spend may start."""
    missing: list[str] = []
    if not secrets.exists(str(secrets.Credential.IDENTIFY_KEY)):
        missing.append(str(secrets.Credential.IDENTIFY_KEY))
    if not secrets.exists(str(secrets.Credential.IDENTIFY_SIGNING_KEY)):
        missing.append(str(secrets.Credential.IDENTIFY_SIGNING_KEY))
    for name in BINARIES:
        if binaries.find(name) is None:
            missing.append(name)
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
) -> Identified:
    """Identify the tracks in ``source``: the Wanted rows, and what it cost.

    Downloads nothing. Writes nothing. The caller decides whether to persist
    a tracklist. ``identifier`` is injected so the suite can prove the gate
    and the shape without spending; left unset, the bound ACRCloud
    identifier runs, and that is the paid path.

    THE GATE RUNS BEFORE THE IDENTIFIER IS BUILT. Building the bound one
    touches nothing, but the order is the contract rather than a nicety: a
    missing key refuses here, by name, and the keychain is never asked.
    """
    assert_recognition_ready()
    if identifier is None:
        from cratekit.intake import acrcloud  # noqa: PLC0415 - bound only on the paid path

        identifier = acrcloud.bound_identifier()
    found = identifier(source)
    if isinstance(found, Identified):
        return found
    return Identified(rows=tuple(found))


def tracklist_text(rows: tuple[Wanted, ...] | list[Wanted] | Any) -> str:
    """A plain tracklist, one 'Artist - Title' line per row. No downloads."""
    lines = []
    for row in rows:
        version = f" ({row.version})" if getattr(row, "version", "") else ""
        lines.append(f"{row.artist} - {row.title}{version}")
    return "\n".join(lines) + ("\n" if lines else "")
