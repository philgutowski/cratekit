"""Register every file a run creates, at creation time.

A path is intake only when this register says a run created it and marked it
complete, so crash debris in staging is never taken in by a later run.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

ARTIFACTS_VERSION = 1


@dataclass(frozen=True, slots=True)
class Artifact:
    """One registered path, complete only after the writer finished it."""

    path: str
    run_id: str
    source_id: str
    complete: bool
    recorded: str


class ArtifactRegistry:
    """The locked document of files this library's sync runs created."""

    def __init__(self, cfg: config.Config) -> None:
        self.path: Path = config.state_path("sync_artifacts", cfg)
        self.lock_path: Path = config.state_path("sync_artifacts_lock", cfg)

    def _unusable(self, what: str) -> CratekitError:
        return refuse(
            "sync-artifacts-unusable",
            f"the sync artifact register at {self.path.name} could not be read "
            f"({what}), so crash debris cannot be told from finished intake",
            steps=("repair or restore the artifact register before running sync",),
            scope=Scope.RUN,
            origin=("sync.artifacts",),
            detail={"problem": what, "path": str(self.path)},
        )

    def _locked(self):
        return config.held(
            self.lock_path,
            lambda exc: refuse(
                "sync-artifacts-unusable",
                f"the artifact register could not be locked ({exc})",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN,
                origin=("sync.artifacts",),
                detail={"lock": str(self.lock_path)},
            ),
        )

    def _load(self) -> dict[str, Artifact]:
        found, raw = config.read_json(self.path, self._unusable)
        if not found:
            return {}
        if not isinstance(raw, Mapping) or raw.get("version") != ARTIFACTS_VERSION:
            raise self._unusable("it is not this document")
        records = raw.get("artifacts")
        if not isinstance(records, Mapping):
            raise self._unusable("it has no artifacts map")
        found: dict[str, Artifact] = {}
        for key, value in records.items():
            if not isinstance(value, Mapping):
                raise self._unusable(f"entry {key!r} is not an object")
            found[str(key)] = Artifact(
                path=str(value.get("path") or key),
                run_id=str(value.get("run_id") or ""),
                source_id=str(value.get("source_id") or ""),
                complete=bool(value.get("complete")),
                recorded=str(value.get("recorded") or ""),
            )
        return found

    def _write(self, records: Mapping[str, Artifact]) -> None:
        payload = {
            "version": ARTIFACTS_VERSION,
            "artifacts": {
                key: {
                    "path": item.path,
                    "run_id": item.run_id,
                    "source_id": item.source_id,
                    "complete": item.complete,
                    "recorded": item.recorded,
                }
                for key, item in sorted(records.items())
            },
        }
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            self.path,
        )

    def _key(self, path: Path) -> str:
        return str(path.resolve()) if path.exists() else str(path)

    def register(
        self,
        path: Path,
        *,
        run_id: str,
        source_id: str,
        complete: bool = False,
    ) -> Artifact:
        """Record ``path`` the moment it is created. Complete is a later flip."""
        item = Artifact(
            path=str(path),
            run_id=run_id,
            source_id=source_id,
            complete=complete,
            recorded=timestamp(),
        )
        with self._locked():
            records = self._load()
            records[self._key(path)] = item
            # Also index the unresolved string, so a later walk finds it either way.
            records[str(path)] = item
            self._write(records)
        return item

    def intake_eligible(self, paths: Iterable[Path]) -> list[Path]:
        """Files a later run may take in: registered and marked complete."""
        records = self._load()
        eligible: list[Path] = []
        for path in paths:
            if not path.is_file():
                continue
            item = records.get(self._key(path)) or records.get(str(path))
            if item is not None and item.complete:
                eligible.append(path)
        return eligible

    def debris(self, paths: Iterable[Path]) -> list[Path]:
        """Files that exist and are not complete registered intake."""
        found = list(paths)
        allowed = {self._key(path) for path in self.intake_eligible(found)}
        leftover: list[Path] = []
        for path in found:
            if not path.is_file():
                continue
            if self._key(path) in allowed or str(path) in allowed:
                continue
            leftover.append(path)
        return leftover
