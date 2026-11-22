"""One source increment: scope, process, one shared intake file, then audit.

The watermark advances only when every scoped item completed without error; a
source whose every lookup failed raises. Sources in one run share one
``{run_id}_synced.xml`` so the hand import never multiplies (R29).
"""

from __future__ import annotations

from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Container, ContextManager, Protocol, Sequence

from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.sync import artifacts, scope
from cratekit.sync.watermarks import WatermarkStore

#: Newest-N default, above 10 to 59 so the reserved-cause walk never reads it as a status.
DEFAULT_LIMIT = 100


class LookupFailure(Exception):
    """Every listing call for this source failed. Distinct from a verified empty.

    ``rate_limited`` makes the refusal retryable, since a rate limit clears on
    its own (R-704); every other failure stays permanent.
    """

    def __init__(self, message: str = "", *, rate_limited: bool = False) -> None:
        super().__init__(message)
        self.rate_limited = rate_limited


@dataclass(frozen=True, slots=True)
class Candidate:
    """One item a source listed. ``identity`` is stable; ``recency`` only orders."""

    identity: str
    recency: str
    payload: dict[str, Any] | None = None


class Source(Protocol):
    """What an increment needs from a source."""

    id: str

    #: Whether a completed :meth:`process` means the item LANDED, or was only
    #: OFFERED for a decision; only the first may be recorded (R-140). It is a
    #: property of the source since both complete without raising.
    #: :func:`increment` defaults it to ``True``.
    acquires: bool

    def list_recent(self, n: int) -> Sequence[Candidate]: ...

    def process(
        self,
        candidate: Candidate,
        registry: artifacts.ArtifactRegistry,
        run_id: str,
    ) -> None: ...


@dataclass(frozen=True, slots=True)
class IncrementResult:
    """What one source did, including a shortfall that blocked the watermark.

    **A CALLER OBLIGATION.** A non-empty ``processed`` with no ``shortfall``
    does not imply an intake row or a moved watermark, since an offering source
    completes the same way. A caller that needs the distinction reads
    ``source.acquires``; widening this type is a contract change (R-136).
    """

    source_id: str
    processed: tuple[str, ...]
    errors: tuple[str, ...]
    shortfall: str | None


def intake_path(staging: Path, run_id: str) -> Path:
    """The one importable file every source in this run appends to."""
    return Path(staging) / f"{run_id}_synced.xml"


def _xml_name(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _append_intake(path: Path, identities: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\r\n'
            "<DJ_PLAYLISTS>\r\n"
            "  <COLLECTION>\r\n"
            "</COLLECTION>\r\n"
            "</DJ_PLAYLISTS>\r\n",
            encoding="utf-8",
        )
    text = path.read_text(encoding="utf-8")
    rows = "".join(
        f'    <TRACK Name="{_xml_name(identity)}"/>\r\n' for identity in identities
    )
    path.write_text(text.replace("</COLLECTION>", rows + "</COLLECTION>"), encoding="utf-8")


def increment(
    source: Source,
    *,
    owned: Container[str],
    limit: int,
    watermarks: WatermarkStore,
    artifacts: artifacts.ArtifactRegistry,
    run_id: str,
    staging: Path,
    boundary: Callable[[str], ContextManager[Any]] | None = None,
) -> IncrementResult:
    """Run one source. The watermark moves only if ``shortfall`` is None.

    And only if the source ACQUIRES; an offering source records no intake row,
    no artifact and no cursor.
    """
    ctx = boundary(source.id) if boundary is not None else nullcontext()
    with ctx:
        try:
            listed = list(source.list_recent(limit))
        except LookupFailure as exc:
            if exc.rate_limited:
                # R-704. A rate limit clears on its own, so the item cause is
                # retryable and the job's verdict and ``jobs.retry`` follow it.
                raise refuse(
                    "sync-source-lookups-failed",
                    f"the provider rate limited a lookup {source.id} needed "
                    f"({exc}); the source was not read in full, which is not a "
                    f"verified empty catalogue, and the limit clears on its own",
                    remedy=Remedy.RESUME_JOB,
                    retryable=True,
                    origin=("sync.run",),
                    detail={"source_id": source.id, "rate_limited": True},
                ) from exc
            raise refuse(
                "sync-source-lookups-failed",
                f"every listing call for {source.id} failed ({exc}); "
                f"an empty result is not a verified empty catalogue",
                steps=("retry this source when the provider is reachable",),
                origin=("sync.run",),
                detail={"source_id": source.id},
            ) from exc

        chosen = scope.scoped(listed, owned=owned, limit=limit)
        processed: list[Candidate] = []
        errors: list[str] = []
        for item in chosen:
            try:
                source.process(item, artifacts, run_id)
            except Exception as exc:
                errors.append(f"{item.identity}: {exc}")
                continue
            processed.append(item)

        if not processed and not errors:
            return IncrementResult(
                source_id=source.id,
                processed=(),
                errors=(),
                shortfall="empty",
            )
        if errors:
            return IncrementResult(
                source_id=source.id,
                processed=tuple(item.identity for item in processed),
                errors=tuple(errors),
                shortfall="; ".join(errors),
            )

        if not getattr(source, "acquires", True):
            # Offered, not acquired. One return rather than a guard per write, so
            # any later writer below it is never reached by an offering source.
            return IncrementResult(
                source_id=source.id,
                processed=tuple(item.identity for item in processed),
                errors=(),
                shortfall=None,
            )

        target = intake_path(staging, run_id)
        _append_intake(target, [item.identity for item in processed])
        artifacts.register(target, run_id=run_id, source_id=source.id, complete=True)

        newest = max(processed, key=lambda item: item.recency)
        watermarks.advance(
            source.id,
            cursor=newest.identity,
            items=len(processed),
            library_id=watermarks.cfg.library.volume_id,
        )
        return IncrementResult(
            source_id=source.id,
            processed=tuple(item.identity for item in processed),
            errors=(),
            shortfall=None,
        )


def run_independent(
    source_list: Sequence[Source],
    *,
    owned: Container[str],
    limit: int,
    watermarks: WatermarkStore,
    artifacts: artifacts.ArtifactRegistry,
    run_id: str,
    staging: Path,
    boundary: Callable[[str], ContextManager[Any]] | None = None,
) -> dict[str, IncrementResult | CratekitError]:
    """Run each source even if a neighbour refuses. One failure is not a halt."""
    results: dict[str, IncrementResult | CratekitError] = {}
    for source in source_list:
        try:
            results[source.id] = increment(
                source,
                owned=owned,
                limit=limit,
                watermarks=watermarks,
                artifacts=artifacts,
                run_id=run_id,
                staging=staging,
                boundary=boundary,
            )
        except CratekitError as exc:
            results[source.id] = exc
        except Exception as exc:
            results[source.id] = refuse(
                "sync-source-lookups-failed",
                f"{source.id} failed before it could list ({type(exc).__name__}: "
                f"{exc}); the other sources still run",
                steps=("retry this source; the neighbour jobs were not cancelled",),
                origin=("sync.run",),
                detail={"source_id": source.id, "exc_type": type(exc).__name__},
            )
    return results
