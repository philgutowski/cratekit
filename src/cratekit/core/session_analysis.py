"""rekordbox's analysis files under a root, fingerprinted so a session can tell they did not move.

Part of :mod:`cratekit.core.session`, which re-exports every name its callers read; read them there. A
name of the session outside this file, and every seam a test patches, is read through
``session`` at call time so a patch on the session bites here too (U300).
"""

from __future__ import annotations

import os
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator, Mapping

from cratekit.core.cause import (
    CratekitError,
    Scope,
    refuse,
)
from cratekit.core.exit_codes import Remedy

#: The names rekordbox gives the per-track analysis files, WIDER than the
#: binding's three on purpose, since R17's fifth surface names a fourth (P4).
ANLZ_NAME_PATTERN = re.compile(r"^ANLZ[0-9]{4}\.(?:DAT|EXT|2EX|3EX)$", re.IGNORECASE)


def is_analysis_file(path: Path | str) -> bool:
    """Whether a path names one of rekordbox's per-track analysis files."""
    return bool(ANLZ_NAME_PATTERN.match(Path(path).name))


def analysis_files_under(roots: Iterable[Path | str]) -> tuple[Path, ...]:
    """Every analysis file beneath the given directories, sorted.

    DERIVED BY WALKING (P3), since the write to catch is the unintended one a
    hand-list omits.
    """
    found: list[Path] = []
    for root in roots:
        base = Path(root)
        if base.is_file():
            if is_analysis_file(base):
                found.append(base)
            continue
        if not base.is_dir():
            continue
        for current, _directories, files in os.walk(base):
            for name in files:
                if is_analysis_file(name):
                    found.append(Path(current) / name)
    return tuple(sorted(set(found)))


def fingerprint_analysis_files(paths: Iterable[Path | str]) -> dict[str, tuple[int, int]]:
    """Modification time and size per analysis file, as a comparable mapping.

    Size too, since a rewrite inside one clock tick leaves the time alone.
    """
    out: dict[str, tuple[int, int]] = {}
    for path in paths:
        target = Path(path)
        try:
            stat = target.stat()
        except OSError:
            continue
        out[str(target)] = (stat.st_mtime_ns, stat.st_size)
    return out


def analysis_drift(
    before: Mapping[str, tuple[int, int]], after: Mapping[str, tuple[int, int]]
) -> tuple[str, ...]:
    """Every analysis file that changed, vanished, or appeared between two reads.

    An appearing file means rekordbox analysed during the session, worth surfacing.
    """
    problems: list[str] = []
    for path, signature in sorted(before.items()):
        found = after.get(path)
        if found is None:
            problems.append(f"{path} was removed")
        elif found != signature:
            problems.append(f"{path} was modified")
    for path in sorted(set(after) - set(before)):
        problems.append(f"{path} appeared")
    return tuple(problems)


@contextmanager
def analysis_files_unmoved(roots: Iterable[Path | str]) -> Iterator[dict[str, tuple[int, int]]]:
    """Refuse if any analysis file under ``roots`` moved while the body ran.

    THIS IS THE HALF THE SOURCE SCAN CANNOT DO, a grid rewritten through a
    handle the binding returned. The remedy is the capture. THE COMPARISON RUNS
    ON BOTH PATHS, since a body that raised is retried; its error is carried
    beneath the refusal.
    """

    watched = list(analysis_files_under(roots))
    before = fingerprint_analysis_files(watched)
    raised: BaseException | None = None
    try:
        yield before
    except BaseException as exc:
        raised = exc
        raise
    finally:
        drift = analysis_drift(
            before, fingerprint_analysis_files(analysis_files_under(roots))
        )
        if drift:
            refusal = refuse(
                "anlz-modified",
                "rekordbox analysis files moved during this session, and the beat "
                "grid lives in those files:\n  - " + "\n  - ".join(drift),
                remedy=Remedy.RESTORE_FROM_SNAPSHOT,
                scope=Scope.SESSION,
                detail={"changed": list(drift), "watched": len(watched)},
                inner=raised.cause if isinstance(raised, CratekitError) else None,
            )
            if raised is not None:
                raise refusal from raised
            raise refusal
