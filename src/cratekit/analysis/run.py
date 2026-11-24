"""Folder-level two-pass: wide measure, then capped vocal finalize.

RESUME IS A TAG ON THE FILE (U343): ``analyze run`` writes :data:`MARK_FIELD`
in the same write as the values it measured, so a kill leaves a file either
marked and finished or unmarked and owed, with no sidecar. A file carrying a
head on its NAME was measured by a run before U343, which named it, and reads
as measured too.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from cratekit.analysis import light, vocals
from cratekit.core import tags
from cratekit.core.naming import NameTemplate, has_head

_RESUME_TEMPLATE = NameTemplate()

#: The tag ``analyze run`` writes on every file it measured, and its value.
#: Any value but an empty one reads as marked, so a later build may write another.
MARK_FIELD = "analyzed"
MARK_VALUE = "1"


@dataclass(frozen=True)
class Result:
    path: Path
    status: str
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


def marked(path: Path) -> bool:
    """Whether ``path`` carries the mark ``analyze run`` writes on a file it measured.

    A file whose tags cannot be read reads as unmarked, so it is measured
    again: the safe direction, since the run then refuses its write by name.
    ``tags.read_tag`` already reads a blank value as absent (review round one).
    """
    return tags.read_tag(path, MARK_FIELD) is not None


def already_analyzed(path: Path, *, template: NameTemplate = _RESUME_TEMPLATE) -> bool:
    """True when ``path`` is marked, or its name carries a complete key and tempo head.

    The name is the marker a run before U343 left, so a file it measured is
    never measured again; asked first, since it reads no file.
    """
    return has_head(path.name, template=template) or marked(path)


def _as_result(payload: dict[str, Any]) -> Result:
    path = Path(payload["path"])
    terminal = payload.get("terminal")
    status = terminal or "analyzed"
    return Result(
        path=path,
        status=status,
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
    """Analyse paths in two pools. A file already analysed is the resume skip.

    ``decode`` is the vocal pass's decoder seam; None binds the shipped one (U58).
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
