"""The staged intake pipeline. One internal shape, then match, then place.

Every input door lands here as ``Wanted`` rows (R13). Identification-only
stops after recognition and writes a tracklist. A file already on disk never
touches the network. Recognition spend is gated before any paid call. Lossy
policy is U15's, applied through naming. Watermarks are not an input: scope
is the list in hand plus owned-dedup at match time (KTD11).
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Callable

from cratekit.acquire.adapter import LosslessPolicy, decide_lossless
from cratekit.acquire.match import MatchResult, Wanted
from cratekit.core import config, taxonomy, tree_registry
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import ingest, normalize, recognize
from cratekit.intake.ingest import PlacedTrack
from cratekit.intake.recognize import Identifier


@dataclass(frozen=True, slots=True)
class IdentifyResult(recognize.Identified):
    """Identification-only output: the identifier's rows and counts, carried
    through so a verb can say whether coverage was complete, how much the
    recognition cache answered and whether what was paid for could be kept,
    plus the tracklist those rows make."""

    tracklist: str = ""


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
    refresh: bool = False,
    recognition: config.RecognitionConfig | None = None,
    progress: recognize.Progress | None = None,
) -> IdentifyResult:
    """Identify the tracks in ``source`` and stop. Download nothing."""
    found = recognize.identify(
        source,
        identifier=identifier,
        refresh=refresh,
        recognition=recognition,
        progress=progress,
    )
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified)}
    return IdentifyResult(**copied, tracklist=recognize.tracklist_text(found.rows))


def ingest_file(
    path: Path,
    *,
    cfg: config.Config,
    export: Path,
    destination: Path,
    lossy: bool = False,
    declared: taxonomy.Taxonomy | None = None,
    registry: tree_registry.Registry | None = None,
) -> FileIngestResult:
    """Ingest one audio file already on disk. No network call.

    ``declared`` and ``registry`` are what the caller read to choose the intake
    tree's medium, handed on so the splice is asked of the same read (R-770).
    With none, ``place_files`` reads them itself.
    """
    normalize.from_audio_file(path)
    placed = ingest.place_files(
        [path],
        cfg=cfg,
        export=export,
        destination=destination,
        lossy=lossy,
        declared=declared,
        registry=registry,
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
    decision = decide_lossless(LosslessPolicy(policy), source_is_lossless=source_is_lossless)
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
