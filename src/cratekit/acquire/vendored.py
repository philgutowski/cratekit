"""The vendored downloader, behind the interface. Nothing else may import it.

Its upstream is gone, so confining it to this file keeps a replacement a
configuration change. This file owns four rules: settings are pushed into the
tool's memory per invocation, verified, and never saved (KTD20); the credential
is a private short lived file written back to the keychain, one per job drive
(R4, U274, :func:`drive`); tool failures become contract outcomes, a rejected
session an AUTH_FAILED naming the replacement (AE9); and the landed FILE is
checked for its codec, not just the request (R-196). A real download needs an
account and is the attended smoke test, so the suite proves everything between.
"""

from __future__ import annotations

import functools
import inspect
import sys
from collections.abc import Callable, Iterator, Mapping
from contextlib import AbstractContextManager, ExitStack, contextmanager, nullcontext
from contextvars import ContextVar
from pathlib import Path
from threading import Event
from typing import Any

from cratekit.acquire import provider_session
from cratekit.acquire.adapter import (
    AdapterAuthFailed,
    AdapterBroken,
    AdapterSettings,
    BaseAdapter,
    LosslessPolicy,
    LosslessRefused,
    NoFileLanded,
    Offer,
    Remedy,
    TrackRequest,
    TrackSource,
    verify_applied,
)
from cratekit.core import binaries, config, provider_gate

#: Cratekit's quality vocabulary to the client's enum VALUE. Pushed every run,
#: because the tool's factory default is lossy.
QUALITY_BY_POLICY: dict[str, str] = {
    "lossless": "LOSSLESS", "hi_res": "HI_RES_LOSSLESS", "lossy": "HIGH",
}

#: The file name the wrapped tool expects its session in.
TOKEN_FILENAME = "token.json"

#: Every keyword ``fetch`` hands the downloader, so a test asserts the SET: each
#: defaults to ``None``, so a dropped one dies only later (R-197).
DOWNLOADER_ARGUMENTS: frozenset[str] = frozenset(
    {
        "tidal_obj",
        "path_base",
        "fn_logger",
        "event_abort",
        "event_run",
        "progress",
        "progress_overall",
    }
)

#: The staging file name in the tool's template language: the track identifier
#: only, since naming is U4's engine and an identifier matches back unambiguously.
STAGING_TEMPLATE = "{track_id}"


def tool_settings(
    settings: AdapterSettings, *, resolve: Callable[[str], str] = binaries.resolve
) -> dict[str, Any]:
    """The wrapped tool's setting names and the values this run requires.

    The single source of what is pushed AND verified, so a new setting is checked
    by existing (P4). ``resolve`` is a parameter to keep this pure. A missing
    ffmpeg path silently lands lossy files, so it is refused (R-195).
    """
    try:
        ffmpeg = resolve("ffmpeg")
    except binaries.BinaryNotFound as exc:
        # A broken override and an absent encoder need different fixes.
        broken_override = exc.remedy is binaries.Remedy.FIX_BINARY_OVERRIDE
        # Refused rather than pushed empty, which the tool reads as "no FLAC".
        raise AdapterBroken(
            f"the downloader needs ffmpeg to extract lossless audio and it could "
            f"not be resolved ({exc}); without it this run would land lossy files "
            f"and report success",
            remedy=(
                Remedy.REPAIR_ADAPTER_SETTINGS if broken_override else Remedy.INSTALL_ADAPTER
            ),
        ) from exc

    return {
        "quality_audio": QUALITY_BY_POLICY.get(settings.quality, settings.quality.upper()),
        "download_base_path": str(settings.download_staging),
        "format_track": STAGING_TEMPLATE,
        "path_binary_ffmpeg": ffmpeg,
        # Stated every run, never inherited, or a stale False lands an m4a (KTD20).
        "extract_flac": True,
    }


def apply_settings(
    target: Any, settings: AdapterSettings, *, resolve: Callable[[str], str] = binaries.resolve,
) -> None:
    """Push this run's settings onto the tool's in-memory configuration, then check.

    Read back off the same object, so a coerced or ignored field is caught. Nothing
    is saved (KTD20).
    """
    expected = tool_settings(settings, resolve=resolve)
    for key, value in expected.items():
        setattr(target, key, value)

    applied = {key: getattr(target, key, _ABSENT) for key in expected}
    problems = verify_applied(applied, expected)
    if problems:
        raise AdapterBroken(
            "the downloader did not accept this run's settings: " + "; ".join(problems),
            remedy=Remedy.REPAIR_ADAPTER_SETTINGS,
        )


_ABSENT = object()

#: How to mint a usable session. Only a PKCE session gets lossless audio (R-196).
REAUTHORISE_HINT = (
    "mint a new one with the vendored downloader's own login command, then record "
    "it with `crate login provider-session --from-file`"
)


def login_mode(stored: object, *, had_stored_session: bool) -> str | None:
    """Why this stored session cannot be used, or None to proceed with PKCE.

    Pure so the offline suite reaches it. A session with no PKCE marker is refused,
    naming the cause rather than letting the codec guard catch the symptom.
    """
    if not had_stored_session:
        return "there is no stored provider session to authenticate with"
    if not bool(getattr(stored, "is_pkce", False)):
        return (
            "the stored provider session was minted by the device-linking client, "
            "which the provider serves lossy audio; this product authenticates "
            "through PKCE only"
        )
    return None


def is_authentication_failure(exc: BaseException) -> bool:
    """Whether an exception from the wrapped tool means the session was rejected.

    The tool's own broad text check, so never asked alone; see
    ``raise_if_session_dead``.
    """
    text = str(exc)
    return "401" in text or "OAuth" in text or "token" in text.lower()


def raise_if_session_dead(exc: BaseException) -> None:
    """Escalate a per-track failure to an invocation failure when the session died.

    Permanence is asked FIRST, since the heuristic matches "token" anywhere and a
    stream token not found is about the track. Ordering is ours; narrowing the
    vendored heuristic would be a patch to reapply forever.
    """
    from cratekit.acquire.adapter import (  # noqa: PLC0415
        TrackOutcome,
        classify_unavailable,
        raise_if_defect,
    )

    # A defect first, since ``... has no attribute 'token'`` is a bug (R-348).
    raise_if_defect(exc)
    if classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT:
        return
    if is_authentication_failure(exc):
        raise AdapterAuthFailed(
            f"the provider rejected the session mid-run ({exc})",
            remedy=Remedy.REAUTHENTICATE_PROVIDER,
        ) from exc


class _VendoredSource:
    """The I/O half: the only object in the product that touches the vendored tree.

    The tool is imported at call time so a broken install can still be named and
    replaced (KTD7). ``session``, ``tool`` and ``downloader`` are injectable so the
    translation is provable without an account.
    """

    def __init__(
        self, settings: AdapterSettings, token_path: Path, *, session: Any = None, tool: Any = None,
        downloader: Any = None,
    ) -> None:
        self._settings = settings
        self._token_path = token_path
        self._session: Any = session
        self._tool: Any = tool
        self._tidal: Any = None
        #: The provider gate over the tool's own session (R-705).
        self._gate = provider_gate.Gate(settings.gate)
        #: The downloader CLASS, injectable so its construction is tested (R-197).
        self._downloader: Any = downloader
        #: The refusal this source met (U274). Once refused it is never asked again,
        #: since a second login into a refused session risks a lockout.
        self._refused: AdapterAuthFailed | None = None

    @property
    def settings(self) -> AdapterSettings:
        return self._settings

    def rebind(self, settings: AdapterSettings) -> None:
        """Serve the next track under its own settings (U274); the gate is kept."""
        self._settings = settings

    def capture(self, scope: provider_session.SessionScope) -> None:
        """Write the logged in session into the scope's token file (U274).

        The tool refreshes in memory only, so this is how a refresh reaches the
        keychain. Nothing is written for a source that never logged in.
        """
        if self._tidal is None:
            return
        # A session left in the tool's Dolby Atmos client is not the PKCE one.
        if getattr(self._tidal, "is_atmos_session", False):
            return
        refreshed = provider_session.captured(self._session, scope.stored)
        if refreshed is None:
            return
        config.atomic_write_bytes(
            provider_session.JSON.dumps(refreshed), scope.path, mode=config.PRIVATE_FILE_MODE
        )

    def _refuse_if_refused(self) -> None:
        """Raise the refusal this source met again, making no call (U274)."""
        if self._refused is not None:
            raise AdapterAuthFailed(str(self._refused), remedy=self._refused.remedy)

    def authenticate(self) -> None:
        # A refused session is never asked again (U274).
        self._refuse_if_refused()
        try:
            self._authenticate()
        except AdapterAuthFailed as refused:
            self._refused = refused
            raise

    def _authenticate(self) -> None:
        # The gate is asked before anything is built (R-705), so a cooldown parks.
        self._gate.assert_open()
        if self._session is not None:
            # An injected session is authorised; settings are still verified.
            if self._tool is not None:
                apply_settings(self._tool.data, self._settings)
            self._gate.attach(self._session)
            return

        try:
            from cratekit._vendor.downloader.config import Settings, Tidal  # noqa: PLC0415
        except ImportError as exc:  # pragma: no cover - needs the core deps absent
            raise AdapterBroken(
                f"the vendored downloader could not be imported ({exc}); its "
                f"dependencies ship with the core install and one of them is missing",
                remedy=Remedy.SWITCH_ADAPTER,
            ) from exc

        self._tool = Settings()
        apply_settings(self._tool.data, self._settings)

        tidal = Tidal(self._tool)
        # Attached before the login, so the tool's own retries are paced too.
        self._gate.attach(tidal.session)
        # The private session file, both where the tool reads and where it saves.
        tidal.file_path = str(self._token_path)
        tidal.path_base = str(self._token_path.parent)
        tidal.token_from_storage = tidal.read(str(self._token_path))

        refusal = login_mode(tidal.data, had_stored_session=tidal.token_from_storage)
        if refusal is not None:
            raise AdapterAuthFailed(
                f"{refusal}. To fix it, {REAUTHORISE_HINT}.", remedy=Remedy.REAUTHENTICATE_PROVIDER,
            )

        try:
            authorised = tidal.login_token(do_pkce=True)
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            raise AdapterAuthFailed(
                f"the provider rejected the stored session ({exc})",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            ) from exc
        # Asked again after the login (R-705): the tool swallows a trip as False,
        # which must park rather than read as a rejected session.
        self._gate.raise_if_parked()
        if not authorised:
            raise AdapterAuthFailed(
                "the stored provider session is no longer valid",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            )
        self._tidal = tidal
        self._session = tidal.session

    def offer(self, request: TrackRequest) -> Offer:
        """What the provider has for this track; any lossless tier counts."""
        self._refuse_if_refused()
        try:
            track = self._session.track(request.key)
        except Exception as exc:
            try:
                raise_if_session_dead(exc)
            except AdapterAuthFailed as dead:
                self._refused = dead
                raise
            raise
        quality = str(getattr(track, "audio_quality", "") or "")
        return Offer(lossless="LOSSLESS" in quality.upper(), detail=quality)

    def fetch(self, request: TrackRequest, destination: Path) -> Path:
        self._refuse_if_refused()
        try:
            return self._fetch(request, destination)
        except AdapterAuthFailed as dead:
            self._refused = dead
            raise

    def _fetch(self, request: TrackRequest, destination: Path) -> Path:
        from cratekit._vendor.downloader.constants import MediaType  # noqa: PLC0415

        event_abort, event_run = download_events()
        progress, progress_overall = disabled_progress()
        downloader_class = self._downloader or _vendored_downloader()
        # One log per fetch, since fetches run side by side (R-703).
        tool_log = _ToolLogging()
        downloader = downloader_class(
            tidal_obj=self._tidal,
            path_base=str(destination),
            fn_logger=tool_log,
            event_abort=event_abort,
            event_run=event_run,
            progress=progress,
            progress_overall=progress_overall,
        )
        # What the constructor logged is never this track's cause.
        tool_log.forget()
        observe_session(downloader, tool_log)
        try:
            ok, landed = downloader.item(
                file_template=STAGING_TEMPLATE, media_id=str(request.key),
                media_type=MediaType.TRACK,
            )
        except Exception as exc:
            raise_if_session_dead(exc)
            raise
        # Asked again after the tool returns, so a swallowed trip parks (R-705).
        self._gate.raise_if_parked()
        # THE SWALLOWED ERROR is judged as if it escaped, on a failed item, for
        # the dead session and defect escalations only (R-703).
        cause = tool_log.cause
        if not ok and isinstance(cause, BaseException):
            raise_if_session_dead(cause)
        return landed_file(
            ok,
            landed,
            request.key,
            policy=self._settings.lossless_policy,
            cause=cause,
        )


def _vendored_downloader() -> Any:  # pragma: no cover - needs the vendored tree's deps
    """The wrapped tool's downloader class, imported at CALL time (KTD7)."""
    from cratekit._vendor.downloader.download import Download  # noqa: PLC0415

    return Download


def download_events() -> tuple[Event, Event]:
    """The abort and run events, in the STATES the wrapped tool requires.

    ``event_run`` is SET and ``event_abort`` is CLEAR. Nothing in the vendored tree
    sets ``event_run``, so an unset one hangs every segment worker.
    """
    event_run = Event()
    event_run.set()
    return Event(), event_run


def disabled_progress() -> tuple[Any, Any]:
    """The tool's two progress bars, rendering nothing.

    The tool never checks for None (R-197). Real ``rich`` objects, not stubs,
    disabled so nothing reaches a parsed stream (R32).
    """
    from rich.progress import Progress  # noqa: PLC0415 - same deferral as the tree above

    return Progress(disable=True), Progress(disable=True)


#: Whether a container is lossless, when the container alone decides it. Keyed by
#: mutagen's CLASS name, since a ``.m4a`` suffix holds AAC or ALAC. MP4 is absent;
#: see ``MP4_LOSSLESS_CODECS``.
LOSSLESS_BY_CONTAINER: dict[str, bool] = {
    "FLAC": True,
    "WAVE": True,
    "AIFF": True,
    "OggFLAC": True,
    "MP3": False,
    "OggVorbis": False,
    "OggOpus": False,
    "AAC": False,
}

#: The MP4 codec strings that are lossless. Only MP4 exposes ``info.codec``, so a
#: None codec means the container decides, not that the file is unreadable.
MP4_LOSSLESS_CODECS: frozenset[str] = frozenset({"alac"})


def codec_of(path: Path) -> tuple[str, bool | None]:
    """What landed, as ``(name, lossless)``. ``lossless`` is None when unreadable.

    Mutagen is imported inside, as ``core/tags.py`` does, to keep this importable.
    """
    import mutagen  # noqa: PLC0415 - see the docstring

    try:
        handle = mutagen.File(str(path))
    except Exception:  # noqa: BLE001 - every container fails differently; none may escape
        handle = None
    if handle is None:
        return "unreadable", None

    container = type(handle).__name__
    codec = str(getattr(handle.info, "codec", "") or "")
    if codec:
        return codec, codec.lower() in MP4_LOSSLESS_CODECS
    known = LOSSLESS_BY_CONTAINER.get(container)
    if known is None:
        return container, None
    return container, known


def landed_file(
    ok: bool, landed: object, key: str, *, policy: LosslessPolicy = LosslessPolicy.STRICT,
    probe: Callable[[Path], tuple[str, bool | None]] = codec_of,
    cause: BaseException | str | None = None,
) -> Path:
    """Turn the tool's ``(succeeded, path)`` pair into a file or an exception.

    No file raises ``NoFileLanded``, transient, naming the swallowed ``cause``
    (R-703). Under strict policy the landed FILE's codec is checked (R-196), and a
    lossy one is a per track ``LosslessRefused``, left in place as evidence. Not
    ``AdapterBroken``: an adapter level failure raised inside the per track loop
    builds a failed ``InvocationResult`` from the tracks already landed, which
    raises ``ValueError`` once an earlier track was permanently unavailable.
    """
    if not ok:
        message = f"the downloader reported no file for {key}"
        if cause is not None:
            message = f"{message}; {describe_cause(cause)}"
        raise NoFileLanded(message, cause=cause) from (
            cause if isinstance(cause, BaseException) else None
        )
    path = Path(str(landed))
    if policy is not LosslessPolicy.STRICT:
        return path

    name, lossless = probe(path)
    if lossless is None:
        # A plain transient error, NOT a policy refusal: an unreadable file is
        # usually truncated, and relaxing the policy would accept it.
        raise RuntimeError(
            f"the file that landed for {key} could not be read as audio ({name}), "
            f"so this run cannot confirm it is lossless; it is at {path}"
        )
    if not lossless:
        raise LosslessRefused(
            f"the provider was asked for lossless audio and the file that landed "
            f"for {key} is {name}; it is at {path}"
        )
    return path


def _provider_errors() -> tuple[type[BaseException], ...]:
    """The classes a provider answer arrives as, imported late (KTD7)."""
    try:
        from requests import RequestException  # noqa: PLC0415
        from tidalapi.exceptions import TidalAPIError  # noqa: PLC0415
    except ImportError:  # pragma: no cover - needs the core deps absent
        return ()
    return (TidalAPIError, RequestException)


def is_rate_limit(exc: BaseException) -> bool:
    """Whether the provider refused a call for spending its allowance too fast.

    The status is read by the paced pool's own ``status_of``, so they agree.
    """
    from cratekit.acquire.download import RATE_LIMIT_STATUSES, status_of  # noqa: PLC0415

    try:
        from tidalapi.exceptions import TooManyRequests  # noqa: PLC0415
    except ImportError:  # pragma: no cover - needs the core deps absent
        TooManyRequests = ()  # noqa: N806 - an empty isinstance tuple matches nothing
    return isinstance(exc, TooManyRequests) or status_of(exc) in RATE_LIMIT_STATUSES


def describe_cause(cause: BaseException | str) -> str:
    """The swallowed cause in words: a rate limit said as one, the error named.

    "The provider answered" only for a provider class, not the tool's own flow.
    """
    if isinstance(cause, str):
        return f"the downloader logged {cause!r}"
    named = f"{type(cause).__name__}: {cause}" if str(cause) else type(cause).__name__
    if is_rate_limit(cause):
        return f"the provider rate limited the lookup ({named}), retry after the limit lifts"
    if isinstance(cause, _provider_errors()):
        return f"the provider answered {named}"
    return f"the downloader failed on {named}"


class _ObservedSession:
    """The tool's session, noting every exception a call on it raises, then raising it.

    The tool's media lookup swallows errors without logging (R-703). Only method
    calls are observed; other attributes are the real ones, and writes go to the
    real session.
    """

    def __init__(self, session: Any, log: _ToolLogging) -> None:
        object.__setattr__(self, "_session", session)
        object.__setattr__(self, "_log", log)

    def __getattr__(self, name: str) -> Any:
        value = getattr(self._session, name)
        if not inspect.ismethod(value):
            return value
        log = self._log

        @functools.wraps(value)
        def observed(*args: object, **kwargs: object) -> Any:
            try:
                return value(*args, **kwargs)
            except Exception as exc:
                log.note(exc)
                raise

        return observed

    def __setattr__(self, name: str, value: object) -> None:
        setattr(self._session, name, value)


def observe_session(downloader: Any, log: _ToolLogging) -> None:
    """Stand an observed session in the downloader's ``session`` attribute, if any."""
    session = getattr(downloader, "session", None)
    if session is not None and not isinstance(session, _ObservedSession):
        downloader.session = _ObservedSession(session, log)


class _ToolLogging:
    """Absorb the wrapped tool's logging, writing nothing and keeping its first failure.

    THE CAUSE IS KEPT, NOT WRITTEN (R-703). ``error``, ``exception`` and
    ``critical`` note the exception being handled, else the message; the FIRST of
    each is kept and an exception outranks a message. The tool annotates
    ``fn_logger`` as ``Callable`` but calls logger methods on it (R-210), so both
    shapes are served; the method set is pinned by a test.
    """

    def __init__(self) -> None:
        self._exception: BaseException | None = None
        self._message: str | None = None

    @property
    def cause(self) -> BaseException | str | None:
        """The first exception noted, else the first failure message, else None."""
        return self._exception if self._exception is not None else self._message

    def note(self, exc: BaseException) -> None:
        if self._exception is None:
            self._exception = exc

    def forget(self) -> None:
        self._exception = None
        self._message = None

    def _failure(self, args: tuple[object, ...]) -> None:
        # The tool logs inside its except clauses without passing ``exc_info``.
        active = sys.exc_info()[1]
        if active is not None:
            self.note(active)
        elif self._message is None and args:
            self._message = _render(args)

    def __call__(self, *_args: object, **_kwargs: object) -> None:
        return None

    def debug(self, *_args: object, **_kwargs: object) -> None:
        return None

    def info(self, *_args: object, **_kwargs: object) -> None:
        return None

    def warning(self, *_args: object, **_kwargs: object) -> None:
        return None

    def error(self, *args: object, **_kwargs: object) -> None:
        self._failure(args)

    def exception(self, *args: object, **_kwargs: object) -> None:
        self._failure(args)

    def critical(self, *args: object, **_kwargs: object) -> None:
        self._failure(args)


def _render(args: tuple[object, ...]) -> str:
    """A logging call's message, formatted the way ``logging`` would, never raising."""
    message, *rest = args
    text = str(message)
    if rest:
        # One mapping argument formats by name, as ``logging`` does.
        values = rest[0] if len(rest) == 1 and isinstance(rest[0], Mapping) else tuple(rest)
        try:
            text = text % values
        except (TypeError, ValueError):
            text = " ".join([text, *map(str, rest)])
    return text


class _Drive:
    """One drive of one download job: one token file, one login, one write back.

    Nothing happens until a track asks (U274). Each track still asks the gate and
    verifies its own settings, and a refusal is remembered across the drive.
    """

    def __init__(self) -> None:
        self._stack = ExitStack()
        self._scope: provider_session.SessionScope | None = None
        self._source: _VendoredSource | None = None
        #: What the close could not do, as envelope warnings (see :func:`drive`).
        self.warnings: list[dict[str, str]] = []

    def source(self, settings: AdapterSettings) -> _VendoredSource:
        """The drive's source under this track's settings; the first call logs in."""
        if self._scope is None:
            self._scope = self._stack.enter_context(
                provider_session.materialised_session(filename=TOKEN_FILENAME)
            )
        held = self._source
        if held is not None and held.settings.gate == settings.gate:
            held.rebind(settings)
            return held
        fresh = _VendoredSource(settings, self._scope.path)
        # A refusal outlives the source it was met on.
        fresh._refused = held._refused if held is not None else None
        self._source = fresh
        return fresh

    def close(self) -> None:
        """Write back what the provider gave this drive, then always erase the file."""
        try:
            if self._scope is not None and self._source is not None:
                self._source.capture(self._scope)
        finally:
            self._stack.close()


#: The warning when a refreshed session could not be stored at the close (U274).
SESSION_NOT_STORED = provider_session.SESSION_NOT_STORED

#: The drive this thread of control is inside, if any (U274).
_DRIVE: ContextVar[_Drive | None] = ContextVar("cratekit_vendored_drive", default=None)


@contextmanager
def drive() -> Iterator[_Drive]:
    """Hold one session for every track a job's drive acquires (U274).

    Entered around a drive through the worker's ``per_drive``, so the write back
    and the erase run on every way out. A write back that fails never replaces the
    drive's own answer: it becomes :data:`SESSION_NOT_STORED` on a finished drive.
    Any other close failure after a finished drive is a defect and raises.
    """
    held = _Drive()
    entered = _DRIVE.set(held)
    finished = False
    try:
        yield held
        finished = True
    finally:
        _DRIVE.reset(entered)
        try:
            held.close()
        except provider_session.STORE_FAILURES as exc:
            # Judged by class, since a credential refusal's words are for setup.
            held.warnings.append(
                {
                    "code": SESSION_NOT_STORED,
                    "message": (
                        f"the provider session this download refreshed could not be "
                        f"stored ({type(exc).__name__}), so the next run logs in again "
                        f"from the stored session"
                    ),
                }
            )
        except Exception:
            if finished:
                raise


class VendoredAdapter(BaseAdapter):
    """The default adapter: the vendored downloader behind the declared contract."""

    name = "vendored"

    def _session_scope(self) -> AbstractContextManager[object]:
        # Inside a drive, the drive's scope (U274); else one per invocation.

        held = _DRIVE.get()
        if held is not None:
            return nullcontext(held)
        return provider_session.materialised_session(filename=TOKEN_FILENAME)

    def _source(self, scope: object) -> TrackSource:
        if isinstance(scope, _Drive):
            return scope.source(self.settings)
        token_path = getattr(scope, "path", None)
        if token_path is None:  # pragma: no cover - only a misconfigured scope
            raise AdapterBroken(
                "no provider session was materialised for this run",
                remedy=Remedy.REPAIR_CREDENTIAL_STORE,
            )
        return _VendoredSource(self.settings, Path(token_path))


__all__ = [
    "DOWNLOADER_ARGUMENTS", "LOSSLESS_BY_CONTAINER", "MP4_LOSSLESS_CODECS", "QUALITY_BY_POLICY",
    "REAUTHORISE_HINT", "SESSION_NOT_STORED", "STAGING_TEMPLATE", "TOKEN_FILENAME",
    "VendoredAdapter", "apply_settings", "codec_of", "describe_cause", "disabled_progress", "drive",
    "download_events", "is_authentication_failure", "is_rate_limit", "landed_file", "login_mode",
    "observe_session", "raise_if_session_dead", "tool_settings",
]
