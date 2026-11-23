"""A rehearsal of a gated database write, on a scratch area of its own (U162).

Each :class:`Area` is per run and never shared, its moved files CLONED and never
linked, so no live ledger or file is reached; the ISRC cache (U206) and provider
gate (U278) stay live. :func:`assert_untouched` proves the live library unmoved.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from cratekit.core import config, rb_writer
from cratekit.core.cause import refuse

_ORIGIN = ("core", "rehearsal")

#: Never copied: the database (its own file set), locks (held on an inode), the
#: active run sentinel, and histories such as the snapshots and rehearsal areas.
_NOT_COPIED = frozenset(
    {
        "rekordbox_db",
        "active_run_sentinel",
        "session_log",
        "snapshots",
        "decision_store_locks",
        "adoption_locks",
        "mirror_plans",
        "set_workspaces",
        "rehearsal_areas",
    }
)


@dataclasses.dataclass(frozen=True, slots=True)
class Area:
    """One rehearsal's scratch area, its two halves, and the config that points at them."""

    #: The run the rehearsal belongs to, as the run record names it.
    run_id: str
    #: The library volume half, beside the library so a clone stays a clone.
    volume: Path
    #: The local state disk half, where locks and run records belong.
    local: Path
    #: The database copy the rehearsal opens.
    database: Path
    #: The config the rehearsal runs under, every library path redirected.
    cfg: config.Config

    @property
    def staging(self) -> Path:
        """Where the files a verb moves are cloned to."""
        return self.volume / "staging"

    @property
    def paths(self) -> tuple[Path, ...]:
        """Both halves, the way a refusal names an area it kept."""
        return (self.volume, self.local)


def slug(run_id: str) -> str:
    """A run id as a folder name every volume accepts (exFAT refuses a colon)."""
    return re.sub(r"[^A-Za-z0-9-]+", "-", run_id).strip("-") or "run"


def volume_root(cfg: config.Config) -> Path:
    """Where every rehearsal's volume half lives, under the library state directory."""
    return config.state_path("rehearsal_areas", cfg)


def local_root() -> Path:
    """Where every rehearsal's local half and record lives."""
    return config.state_path("rehearsals")


def clone(source: Path, destination: Path) -> None:
    """A clone of ``source`` where the volume clones, else its bytes, NEVER A HARD LINK."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if sys.platform == "darwin":
        done = subprocess.run(
            ["/bin/cp", "-c", "-p", str(source), str(destination)],
            capture_output=True,
            check=False,
        )
        if done.returncode == 0:
            return
        destination.unlink(missing_ok=True)
    shutil.copy2(source, destination)


def open_area(
    cfg: config.Config,
    run_id: str,
    *,
    files: Iterable[Path] = (),
    staging: Path | None = None,
) -> Area:
    """Make the run's scratch area and copy into it what a rehearsal reads.

    REFUSES WHILE REKORDBOX OR ITS AGENT IS RUNNING, as the copy would be torn,
    and REFUSES AN AREA THAT EXISTS, since an area is never shared.
    """
    rb_writer.assert_rekordbox_closed("copying the database for a rehearsal")
    live = rb_writer.live_db_path(cfg)
    rb_writer.require_present(live)
    name = slug(run_id)
    volume = volume_root(cfg) / name
    local = local_root() / name
    for path in (volume, local):
        if path.exists():
            raise refuse(
                "output-exists",
                f"a rehearsal area for run {run_id} already exists at {path}; an area "
                f"belongs to one rehearsal, so nothing was copied",
                origin=_ORIGIN,
                detail={"area": str(path), "run_id": run_id},
            )
    made: list[Path] = []
    try:
        for path in (volume, local):
            path.mkdir(parents=True)
            made.append(path)
        (volume / "db").mkdir()
        database = rb_writer.copy_file_set(live, volume / "db")
        relative = volume.relative_to(cfg.library.root)
        library = dataclasses.replace(
            cfg.library,
            db_path=database,
            state_dirname=str(relative / "state"),
            music_dir=str(relative / cfg.library.music_dir),
        )
        paths = (
            dataclasses.replace(cfg.paths, download_staging=volume / "staging")
            if staging is not None
            else cfg.paths
        )
        redirected_cfg = dataclasses.replace(cfg, library=library, paths=paths)
        _copy_library_state(cfg, redirected_cfg)
        (volume / "staging").mkdir()
        for one in files:
            clone(one, volume / "staging" / one.name)
        (local / "config").mkdir()
        (local / "state").mkdir()
        # A NEW DOCUMENT IN A NEW FOLDER, so the locked cycle has nothing to erase.
        config.update(
            lambda _absent: redirected_cfg.to_toml_dict(),
            local / "config" / config.CONFIG_FILENAME,
        )
    except BaseException:
        for path in made:
            shutil.rmtree(path, ignore_errors=True)
        raise
    return Area(run_id=run_id, volume=volume, local=local, database=database, cfg=redirected_cfg)


def _copy_library_state(cfg: config.Config, redirected: config.Config) -> None:
    """Copy the library state a rehearsal reads, and none of what it must not share."""
    live_root = config.library_state_dir(cfg)
    for entry in config.STATE_FILES:
        if entry.root is not config.StateRoot.LIBRARY or not entry.relative:
            continue
        if entry.key in _NOT_COPIED or entry.key.endswith("_lock"):
            continue
        found = config.state_path(entry.key, cfg)
        if not found.is_relative_to(live_root):
            continue
        target = config.state_path(entry.key, redirected)
        if entry.medium is config.Medium.DIRECTORY:
            if found.is_dir():
                shutil.copytree(found, target)
        elif found.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(found, target)


@contextmanager
def redirected(area: Area) -> Iterator[config.Config]:
    """Run the body with config and installation state pointed into the area.

    Restored on the way out; the ISRC cache and provider gate stay live (U206, U278).
    """
    keys = (config.ENV_CONFIG_DIR, config.ENV_STATE_DIR, config.ENV_ISRC_CACHE_DIR)
    saved = {key: os.environ.get(key) for key in keys}
    # THE ISRC ANSWERS STAY LIVE (U206), resolved before the state moves; they mark nothing done.
    os.environ[config.ENV_ISRC_CACHE_DIR] = saved[config.ENV_ISRC_CACHE_DIR] or str(
        config.state_path("isrc_cache").parent
    )
    os.environ[config.ENV_CONFIG_DIR] = str(area.local / "config")
    os.environ[config.ENV_STATE_DIR] = str(area.local / "state")
    config.reset_cache()
    try:
        yield area.cfg
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        config.reset_cache()


def remove(area: Area) -> None:
    """Take the area away, both halves."""
    for path in area.paths:
        shutil.rmtree(path, ignore_errors=True)


# The live library, before and after


@dataclasses.dataclass(frozen=True, slots=True)
class Witness:
    """What the live library looked like before a rehearsal, to be asked again after."""

    database: Path
    hashes: tuple[tuple[str, str], ...]
    folders: tuple[tuple[str, tuple[tuple[str, int, int, int], ...] | None], ...]


def _hashes(database: Path) -> tuple[tuple[str, str], ...]:
    found = []
    for path in (
        database,
        *(database.with_name(database.name + s) for s in rb_writer.db_sidecar_suffixes()),
    ):
        if path.is_file():
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for block in iter(lambda: handle.read(1 << 20), b""):
                    digest.update(block)
            found.append((path.name, digest.hexdigest()))
    return tuple(found)


def _listed(folder: Path) -> tuple[tuple[str, int, int, int], ...] | None:
    if not folder.is_dir():
        return None
    rows = []
    for entry in sorted(folder.iterdir(), key=lambda p: p.name):
        stat = entry.lstat()
        rows.append((entry.name, stat.st_size, stat.st_mtime_ns, stat.st_ino))
    return tuple(rows)


def witness(cfg: config.Config, folders: Iterable[Path]) -> Witness:
    """The live database file set's hashes and each live folder's listing, now."""
    database = rb_writer.live_db_path(cfg)
    return Witness(
        database=database,
        hashes=_hashes(database),
        folders=tuple((str(folder), _listed(folder)) for folder in folders),
    )


def assert_untouched(before: Witness, *, kept: Iterable[Path] = ()) -> None:
    """Refuse, as the defect it would be, when the live library moved under a rehearsal."""
    moved = []
    if _hashes(before.database) != before.hashes:
        moved.append(f"the live database {before.database}")
    for folder, listing in before.folders:
        if _listed(Path(folder)) != listing:
            moved.append(f"the live folder {folder}")
    if moved:
        raise refuse(
            "internal-error",
            f"a rehearsal changed {', '.join(moved)}, which rehearsal code must never "
            f"touch; this is a defect, report it"
            + (f"; the rehearsal area is kept at {', '.join(map(str, kept))}" if kept else ""),
            origin=_ORIGIN,
            detail={"changed": moved, "kept": [str(path) for path in kept]},
        )


# The record a live run compares against


def lines(identity: Any, prefix: str = "") -> list[str]:
    """Every leaf of a plan's identity as one ``path = value`` line, so a difference is named."""
    if isinstance(identity, Mapping):
        out: list[str] = []
        for key in sorted(identity):
            out.extend(lines(identity[key], f"{prefix}.{key}" if prefix else str(key)))
        return out or [f"{prefix} = {{}}"]
    if isinstance(identity, (list, tuple)):
        out = []
        for index, one in enumerate(identity):
            out.extend(lines(one, f"{prefix}[{index}]"))
        return out or [f"{prefix} = []"]
    return [f"{prefix} = {json.dumps(identity, sort_keys=True, default=str)}"]


def differing(rehearsed: Iterable[str], live: Iterable[str]) -> list[str]:
    """The lines only the rehearsal has, marked ``-``, then those only the live plan has, ``+``."""
    before, after = list(rehearsed), list(live)
    seen_before, seen_after = set(before), set(after)
    return [f"- {one}" for one in before if one not in seen_after] + [
        f"+ {one}" for one in after if one not in seen_before
    ]


def record(
    run_id: str,
    *,
    verb: str,
    key: Mapping[str, str],
    digest: str,
    plan: list[str],
    facts: Mapping[str, Any],
) -> Path:
    """Keep what a live run of the same verb over the same input compares against."""
    root = local_root()
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{slug(run_id)}.json"
    body = {
        "run_id": run_id,
        "at": datetime.now(UTC).isoformat(timespec="seconds"),
        "verb": verb,
        "key": dict(key),
        "digest": digest,
        "plan": plan,
        "facts": dict(facts),
    }
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(body, sort_keys=True, indent=1, default=str))
    os.replace(temporary, path)
    return path


def latest(*, verb: str, key: Mapping[str, str]) -> dict[str, Any] | None:
    """The newest readable rehearsal of ``verb`` over ``key``, or None when none was kept."""
    root = local_root()
    if not root.is_dir():
        return None
    found: list[dict[str, Any]] = []
    for path in root.glob("*.json"):
        try:
            body = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if (
            isinstance(body, dict)
            and body.get("verb") == verb
            and body.get("key") == dict(key)
            and isinstance(body.get("plan"), list)
        ):
            found.append(body)
    if not found:
        return None
    return max(found, key=lambda body: str(body.get("at") or ""))


def mapped(value: Any, replacements: Iterable[tuple[str, str]]) -> Any:
    """``value`` with every string's scratch spelling replaced by its live one.

    THE LONGEST SCRATCH SPELLING FIRST, so one holding another is not half mapped (U188).
    """
    pairs = tuple(
        sorted(
            ((scratch, live) for scratch, live in replacements if scratch),
            key=lambda pair: len(pair[0]),
            reverse=True,
        )
    )
    if isinstance(value, str):
        for scratch, live in pairs:
            value = value.replace(scratch, live)
        return value
    if isinstance(value, Mapping):
        return {mapped(key, pairs): mapped(one, pairs) for key, one in value.items()}
    if isinstance(value, (list, tuple)):
        return [mapped(one, pairs) for one in value]
    return value
