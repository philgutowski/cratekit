"""What ``export.set``, ``export.archive`` and the set rename share: names, origins, failures.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

_SET = ("export.set",)
_ARCHIVE = ("export.archive",)

#: What every set gate says it takes away.
REMOVES_NOTHING = "nothing, ever: no track or playlist is taken away"
NOTHING_WRITTEN = "nothing was written before this failed"


def set_name(given: str) -> str:
    """A set playlist's name as made, recorded and looked up: ONE SPELLING FOR EVERY VERB.

    A slash becomes a dash, since a downloader reads one as a folder.
    """
    return str(given).replace("/", "-").strip()


def _unnamed(given: str) -> CratekitError:
    return refuse(
        "intake-list-unusable",
        f"the set playlist would be named {given!r}, which is no name, so nothing was planned",
        steps=("pass --name with the name the playlist should carry",),
        origin=_SET,
        detail={"name": given},
    )


def warning(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def plan_payload(identity: Any, items: list[dict[str, Any]], totals: dict[str, Any]) -> dict:
    """A gate's plan: the digest of ``identity``, its items and its totals."""
    return {"digest": digest_of(identity), "items": items, "totals": totals, "chunk": None}


def before_failing(parts: list[str], joined: str) -> str:
    """What was written before a failure, from its ``parts``, in words."""
    return f"before this failed {joined.join(parts)}" if parts else NOTHING_WRITTEN


def with_applied(payload: dict[str, Any], applied: dict[str, Any]) -> dict[str, Any]:
    """``payload`` as applied: its totals with what the apply did."""
    return {**payload, "totals": {**payload["totals"], "applied": applied}}


def failed(
    exc: Exception,
    said: str,
    again: str,
    *,
    origin: tuple[str, ...],
    detail: dict[str, Any],
    scope: Scope = Scope.RUN,
    credential: bool = False,
) -> CratekitError | None:
    """``exc`` refused again after ``said``, keeping its cause, or None for a defect.

    With ``credential`` a lost sign in, not a ``CratekitError``, is said as one.
    """
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{said}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=scope,
            retryable=cause.retryable,
            origin=origin,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    if credential and isinstance(exc, secrets.CredentialError):
        return refuse(
            "credential-missing",
            f"{said}. {exc}",
            remedy=Remedy(str(exc.remedy)),
            steps=(again,),
            origin=origin,
            detail={**detail, "kind": type(exc).__name__},
        )
    return None


class _Deferred:
    """The account, resolved the first time one of its members is asked for.

    A set needing none before its gate spends no login until its approved write.
    """

    def __init__(self, cfg: config.Config) -> None:
        self._cfg = cfg
        self._held = None

    def __getattr__(self, name: str) -> Any:
        if self._held is None:
            from cratekit.modules.outbound import account

            self._held = account.resolve(self._cfg)
        return getattr(self._held, name)


@contextmanager
def _inspiration_folder(
    cfg, *, read_only: bool = False, declared=None, one_read=None
) -> Iterator[tuple[Any, str]]:
    """The live database, opened to read, and the INSPIRATION folder's id, empty when absent.

    ONE OPENER FOR THE BACKFILL AND THE RENAME, with rekordbox closed unless
    ``read_only`` (U142). ``one_read`` is ``organize --report``'s one handle
    (U267), and ONLY A READ TAKES IT, never a write without the closed check.
    """
    from cratekit.core import active_taxonomy, rb_writer
    from cratekit.intake import set_playlist

    if one_read is not None and not read_only:
        raise refuse(
            "internal-error",
            "the INSPIRATION folder was asked for to write through a shared read handle",
            remedy=Remedy.REPORT_DEFECT,
            origin=("export", "set_cli"),
        )
    if declared is None:
        declared = active_taxonomy.load(cfg)
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
            rb_writer.live_db_path(cfg),
            require_closed=not read_only,
            check_app_version=not read_only,
            cfg=cfg,
        )
    )
    try:
        folder_id, _node = set_playlist.folder_for(db, declared)
        yield db, folder_id
    finally:
        rb_writer.done_reading(db, one_read)


def _names_for_job(job) -> tuple[str, ...]:
    """Every name a set job's playlists may carry, most deliberate first.

    Its frozen name, then the source system's form on the posted day, then on
    the queued day (U136); never today, which a later backfill would miss (R-949).
    """
    from cratekit.intake import set_playlist

    frozen = set_playlist.frozen_name(job)
    found = [set_name(frozen)] if frozen else []
    try:
        words = set_playlist.words_for(job)
    except Exception:
        return tuple(dict.fromkeys(found))
    try:
        landing = datetime.fromisoformat(str(getattr(job, "created", "") or "")).astimezone().date()
    except ValueError:
        landing = None
    posted, _warn = set_playlist.naming_day_for(job, landing=landing)
    found.append(set_name(set_playlist.playlist_name(words, on=posted)))
    if landing is not None and landing != posted:
        found.append(set_name(set_playlist.playlist_name(words, on=landing)))
    return tuple(dict.fromkeys(name for name in found if name))
