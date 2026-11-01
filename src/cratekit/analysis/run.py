"""Folder-level two-pass: wide head, then capped vocal finalize.

Resume is the Camelot-prefixed filename. A kill after a file is renamed
leaves that name on disk, and the next run skips it. Files that have
not been prefixed are the unfinished tail. That is the source system's
marker, and it does not need a sidecar to be true.

Finalize talks to the filesystem in bytes. A path is a Path, a write is
os.replace of bytes already on disk, never a decoded XML copy held as
one giant str.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from cratekit.analysis import light, vocals
from cratekit.core.naming import NameTemplate, has_head

_RESUME_TEMPLATE = NameTemplate()


@dataclass(frozen=True)
class Result:
    path: Path
    status: str
    camelot: str | None = None
    bpm: int | None = None
    energy: int | None = None
    #: Why ``energy`` is what it is: calibrated, uncalibrated, or unmeasurable.
    #: None only on a terminal result that never reached the energy step.
    energy_status: str | None = None
    vocal_active: bool = False
    #: Why the vocal pass did not score this track, None when it did.
    vocal_reason: str | None = None
    voxlevel: int | None = None
    voxgender: str | None = None
    voxgenderconf: int | None = None
    #: How far the tempo moves, a percent, and its verdict (U157). None and
    #: None from a detector that measures no drift, a test's fake above all.
    drift: float | None = None
    drift_verdict: str | None = None


def already_analyzed(path: Path) -> bool:
    """True when the filename already carries a complete key-tempo head."""
    return has_head(path.name, template=_RESUME_TEMPLATE)


def _as_result(payload: dict[str, Any]) -> Result:
    path = Path(payload["path"])
    terminal = payload.get("terminal")
    status = terminal or "analyzed"
    return Result(
        path=path,
        status=status,
        camelot=payload.get("camelot"),
        bpm=payload.get("bpm", payload.get("rate")),
        energy=payload.get("energy"),
        energy_status=payload.get("energy_status"),
        vocal_active=bool(payload.get("vocal_active")),
        vocal_reason=payload.get("vocal_reason"),
        voxlevel=payload.get("voxlevel"),
        voxgender=payload.get("voxgender"),
        voxgenderconf=payload.get("voxgenderconf"),
        drift=payload.get("drift"),
        drift_verdict=payload.get("drift_verdict"),
    )


def run_batch(
    paths: Iterable[Path],
    *,
    detect: Callable[[Path], dict[str, Any] | None] | None = None,
    vocal_loader: Callable[[], Any] | None = None,
    vocal: bool = True,
    decode: Callable[[Any], Any] | None = None,
) -> list[Result]:
    """Analyse paths in two pools. Prefixed names are the resume skip.

    ``decode`` is the vocal pass's decoder seam, what turns a path into the
    samples the model scores. None binds the shipped decoder, which reads the
    file at the model's own rate behind the extra (U58).
    """
    ordered = [Path(path) for path in paths]
    skipped = [path for path in ordered if already_analyzed(path)]
    pending = [path for path in ordered if not already_analyzed(path)]
    results = [
        Result(path=path, status="skipped-prefixed") for path in skipped
    ]
    if not pending:
        return results

    light.bind_detect(detect)
    vocals.bind_loader(vocal_loader if vocal else None)
    vocals.bind_decoder(decode)
    partials = light.run([str(path) for path in pending])
    finished = vocals.run(partials)
    results.extend(_as_result(item) for item in finished)
    results.sort(key=lambda item: item.path.name)
    return results
