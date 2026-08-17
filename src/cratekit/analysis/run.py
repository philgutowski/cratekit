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
    vocal_active: bool = False
    voxlevel: int | None = None
    voxgender: str | None = None


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
        vocal_active=bool(payload.get("vocal_active")),
        voxlevel=payload.get("voxlevel"),
        voxgender=payload.get("voxgender"),
    )


def run_batch(
    paths: Iterable[Path],
    *,
    detect: Callable[[Path], dict[str, Any] | None] | None = None,
    vocal_loader: Callable[[], Any] | None = None,
    vocal: bool = True,
) -> list[Result]:
    """Analyse paths in two pools. Prefixed names are the resume skip."""
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
    partials = light.run([str(path) for path in pending])
    finished = vocals.run(partials)
    results.extend(_as_result(item) for item in finished)
    results.sort(key=lambda item: item.path.name)
    return results
