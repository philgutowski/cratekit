"""The account mirror's plan, frozen on the run whose gate showed it (R-1031).

WHY. The account gate is explicit, so the mirror is always planned twice: once
by the run that shows the gate and once by the run that applies after a person
records the answer. Planned from scratch the second time, a first build paid
its matching twice, about two hours of provider requests, and any library write
between the two acts, a landing, a refresh or a split, moved the digest and
refused the approved plan ``decision-stale``.

WHAT IS FROZEN is what the plan read that is not the account: the library, every
folder, playlist and row ``read_library`` returned with each name it refused,
and every match the plan made, ``(account track, ISRC, reason)`` per row. The
run that applies rebuilds the mirror from them and reads the account listing
afresh, so the digest it compares is the plan the person approved as long as
the account did not move, and the provider is asked only about a row the frozen
plan does not carry.

ONE FILE PER RUN, under the library scoped ``mirror_plans`` directory, named
by the run's identifier, which is generated and checked against a plain
pattern before it names a file. A frozen plan older than :data:`KEPT_DAYS` is
pruned when another is written.

ABSENT IS NOT A REFUSAL. A record that is missing, unreadable or of another
version is no plan to rebuild from, and the caller plans afresh and says so; a
fresh plan's digest is still compared with the decision, so the worst it costs
is the second pass this module exists to save.

Layer: modules.
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.core import config
from cratekit.core.cause import Cause
from cratekit.modules.outbound import mirror

#: The frozen record's own schema version.
VERSION = 1

#: How long a frozen plan is kept once another is written.
KEPT_DAYS = 7

_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")


@dataclass(frozen=True, slots=True)
class Frozen:
    """What a gate's plan read, the library and the matches, to rebuild it from."""

    #: The library, as ``account_mirror.read_library`` returned it.
    library: Any
    matches: Mapping[str, tuple[str, str, str]]


def _path(cfg: config.Config, run_id: str) -> Path | None:
    if not _RUN_ID.match(run_id):
        return None
    return config.state_path("mirror_plans", cfg) / f"{run_id}.json"


def _library_json(library: Any) -> dict[str, Any]:
    return {
        "folders": [
            {
                "name": folder.name,
                "playlists": [
                    {
                        "name": source.name,
                        "rows": [
                            [row.content_id, row.title, row.artist, row.isrc, row.path]
                            for row in source.rows
                        ],
                    }
                    for source in folder.playlists
                ],
            }
            for folder in library.folders
        ],
        "refused": {name: cause.to_json() for name, cause in sorted(library.refused.items())},
        "favorites": library.favorites,
    }


def _library_of(data: Mapping[str, Any]) -> Any:
    from cratekit.organize import account_mirror

    return account_mirror.Library(
        folders=tuple(
            mirror.Folder(
                name=str(folder["name"]),
                playlists=tuple(
                    mirror.Source(
                        name=str(source["name"]),
                        rows=tuple(
                            mirror.Row(
                                content_id=str(cid),
                                title=str(title),
                                artist=str(artist),
                                isrc=str(isrc),
                                path=str(path),
                            )
                            for cid, title, artist, isrc, path in source["rows"]
                        ),
                    )
                    for source in folder["playlists"]
                ),
            )
            for folder in data["folders"]
        ),
        refused={str(name): Cause.from_json(cause) for name, cause in data["refused"].items()},
        favorites=str(data["favorites"]),
    )


def freeze(
    cfg: config.Config,
    run_id: str,
    library: Any,
    matches: Mapping[str, tuple[str, str, str]],
) -> str:
    """Write this run's frozen plan and prune the old ones. Returns what the gate says of it.

    Raises ``OSError`` when the directory cannot be written, which the caller
    shows as a fact rather than a refusal: the plan stands, and the run that
    applies plans afresh.
    """
    path = _path(cfg, run_id)
    if path is None:
        return f"not frozen: the run identifier {run_id!r} cannot name a file, so the apply plans again"
    document = {
        "version": VERSION,
        "run_id": run_id,
        "library": _library_json(library),
        "matches": {cid: list(held) for cid, held in sorted(matches.items())},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    config.atomic_write_bytes(json.dumps(document, sort_keys=True).encode("utf-8") + b"\n", path)
    _prune(path)
    return f"frozen on run {run_id}, so the apply rebuilds it without asking the provider again"


def _prune(kept: Path) -> None:
    cutoff = time.time() - KEPT_DAYS * 86400
    for one in kept.parent.glob("*.json"):
        if one == kept:
            continue
        try:
            if one.stat().st_mtime < cutoff:
                one.unlink()
        except OSError:
            continue


def load(cfg: config.Config, run_id: str) -> tuple[Frozen | None, str]:
    """This run's frozen plan, or ``None`` and why there is none to rebuild from."""
    path = _path(cfg, run_id)
    if path is None:
        return None, f"the run identifier {run_id!r} names no frozen plan"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"run {run_id} holds no frozen mirror plan"
    except (OSError, ValueError) as exc:
        return None, f"the frozen mirror plan of run {run_id} could not be read ({exc})"
    try:
        if data.get("version") != VERSION or data.get("run_id") != run_id:
            raise ValueError(f"it says version {data.get('version')!r} of run {data.get('run_id')!r}")
        library = _library_of(data["library"])
        matches = {
            str(cid): (str(remote), str(isrc), str(reason))
            for cid, (remote, isrc, reason) in data["matches"].items()
        }
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        return None, f"the frozen mirror plan of run {run_id} is not one this build reads ({exc})"
    return Frozen(library=library, matches=matches), ""


__all__ = ["KEPT_DAYS", "VERSION", "Frozen", "freeze", "load"]
