"""The staged intake pipeline. One internal shape, then match, then place.

Every input door lands here as ``Wanted`` rows (R13). Identification-only
stops after recognition and writes a tracklist. A file already on disk
never touches the network. Recognition spend is gated before any paid
call. Lossy policy is U15's: this pipeline applies the marker through
naming, it does not invent a third policy.

Watermarks are not an input. Scope is the list in hand plus owned-dedup
at match time (KTD11).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from cratekit.acquire.adapter import LosslessPolicy, decide_lossless
from cratekit.acquire.match import MatchResult, Wanted
from cratekit.core import config
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import ingest, normalize, recognize
from cratekit.intake.ingest import PlacedTrack
from cratekit.intake.recognize import Identifier


@dataclass(frozen=True, slots=True)
class IdentifyResult:
    """Identification-only output: a tracklist, and the Wanted rows behind it."""

    rows: tuple[Wanted, ...]
    tracklist: str


@dataclass(frozen=True, slots=True)
class FileIngestResult:
    """One on-disk file that reached a Fresh Export."""

    placed: tuple[PlacedTrack, ...]
    destination: Path
    networked: bool = False


def identify_only(
    source: Path,
    *,
    identifier: Identifier | None = None,
) -> IdentifyResult:
    """Identify the tracks in ``source`` and stop. Download nothing."""
    rows = recognize.identify(source, identifier=identifier)
    return IdentifyResult(rows=rows, tracklist=recognize.tracklist_text(rows))


def ingest_file(
    path: Path,
    *,
    cfg: config.Config,
    export: Path,
    destination: Path,
    lossy: bool = False,
) -> FileIngestResult:
    """Ingest one audio file already on disk. No network call."""
    normalize.from_audio_file(path)
    placed = ingest.place_files(
        [path],
        cfg=cfg,
        export=export,
        destination=destination,
        lossy=lossy,
    )
    return FileIngestResult(
        placed=tuple(placed),
        destination=destination,
        networked=False,
    )


def acquire_lossy_or_refuse(
    *,
    policy: LosslessPolicy | str,
    source_is_lossless: bool,
) -> bool:
    """True when a lossy source may proceed and must be marked.

    Strict policy raises. Allowed-and-marked returns True. A lossless
    source returns False (no marker).
    """
    resolved = (
        policy
        if isinstance(policy, LosslessPolicy)
        else LosslessPolicy(policy)
    )
    decision = decide_lossless(resolved, source_is_lossless=source_is_lossless)
    if not decision.permitted:
        raise refuse(
            "lossy-refused",
            "strict lossless policy refuses a track that only exists lossy; "
            "it is reported unacquired rather than downloaded unmarked",
            remedy=Remedy.RELAX_LOSSLESS_POLICY,
            origin=("intake.pipeline",),
        )
    return bool(decision.marker_required)


def ingest_tracklist(
    text: str,
    *,
    match_against: Callable[[tuple[Wanted, ...]], MatchResult] | None = None,
) -> tuple[Wanted, ...]:
    """Normalize pasted (or transcribed) text to Wanted rows, then optionally match."""
    rows = normalize.from_tracklist(text)
    if match_against is not None:
        match_against(rows)
    return rows
