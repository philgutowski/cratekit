"""Set identification, gated before any paid call.

Recognition is ACRCloud, reached through the operator's own key. No
watermark, no date floor, no asking sync how far a previous run got (KTD11):
scope is the audio the caller handed over, plus owned-dedup in matching.

The spend gate is presence, not retrieval. Retrieving the keys here would
prompt the keychain on macOS, which is how an unattended run hangs, so the
first paid call is the first retrieval. A missing ffmpeg (carves the chunks)
or ffprobe (measures the recording, so the spend is known first) is refused
here too, before any spend rather than after the first failed carve.

The implementation behind the seam is :mod:`cratekit.intake.acrcloud`.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire.match import Wanted
from cratekit.core import binaries, config, secrets
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy


@dataclass(frozen=True, slots=True)
class Identified:
    """What one identification found, and what it cost to find it.

    ``rows`` is the tracklist. ``unreached`` counts chunks that got NO answer,
    apart from ``misses``, because a set where most chunks were never answered
    is not a set nobody recognised, and the two look identical as rows.
    ``calls`` is what THIS pass paid for and ``cached`` what the recognition
    cache answered instead. ``cache_unwritten`` says why paid answers could
    not be kept, so a person knows the next pass pays again. ``digest`` is the
    sha256 of the recording's bytes, the one name two recordings sharing a
    file name do not share. ``parts`` is how many runs the set took (R-706);
    the rows are still one set's, folded once across the parts.
    """

    rows: tuple[Wanted, ...]
    calls: int = 0
    chunks: int = 0
    misses: int = 0
    unreached: int = 0
    cached: int = 0
    cache_unwritten: str = ""
    digest: str = ""
    parts: int = 1


#: An identifier answers with an :class:`Identified`, or with bare rows (a
#: fake in the suite); ``identify`` normalises the two.
Identifier = Callable[[Path], "Identified | tuple[Wanted, ...]"]

#: What a progress line is handed (R-924). None says nothing.
Progress = Callable[[str], None]

#: The binaries recognition needs, in the order a person would install them.
#: Checked by presence here and resolved again by the carver at call time.
BINARIES = ("ffmpeg", "ffprobe")


def recognition_ready() -> tuple[str, ...]:
    """Names of the things that are missing, empty when spend may start."""
    keys = (secrets.Credential.IDENTIFY_KEY, secrets.Credential.IDENTIFY_SIGNING_KEY)
    missing = [str(key) for key in keys if not secrets.exists(str(key))]
    missing += [name for name in BINARIES if binaries.find(name) is None]
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
    refresh: bool = False,
    recognition: config.RecognitionConfig | None = None,
    progress: Progress | None = None,
) -> Identified:
    """Identify the tracks in ``source``: the Wanted rows, and what it cost.

    Downloads nothing, writes nothing. ``identifier`` is injected so the suite
    proves the gate without spending; unset, the bound ACRCloud identifier
    runs, which is the paid path.

    THE GATE RUNS BEFORE THE IDENTIFIER IS BUILT, so a missing key refuses by
    name and the keychain is never asked. ``refresh`` and ``progress`` reach
    the bound identifier only. THE PAID PATH WILL NOT RUN WITHOUT
    ``recognition`` (R-301): the host and the month's bound come from nowhere
    else, so a forgotten section is a defect, not a run against a region and
    a month nobody chose.
    """
    assert_recognition_ready()
    if identifier is None:
        if recognition is None:
            raise TypeError(
                "the bound identifier needs the configuration's recognition "
                "section, which names the host and the month's bound"
            )
        from cratekit.intake import acrcloud  # noqa: PLC0415 - bound only on the paid path

        identifier = acrcloud.bound_identifier(
            recognition, refresh=refresh, progress=progress
        )
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
