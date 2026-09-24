"""The vendored downloader, behind the interface. Nothing else may import it.

This is the boundary the whole unit exists to draw. ``cratekit._vendor`` is a
source tree whose upstream was deleted, which means every one of its APIs is
frozen at whatever the last extract happened to expose and none of them will ever
be fixed. Confining knowledge of that tree to one file is what makes the eventual
replacement a configuration change instead of a search across the codebase.

FOUR THINGS THIS FILE OWNS, and each is a failure the source system had:

1. **Settings live in memory, per invocation (KTD20).** The source system drives
   the wrapped tool by mutating its global settings file through subprocess calls
   before each run. Two racing pacing writes, or a process kill landing mid-write,
   reset that file to factory defaults, which are lossy audio into the tool's own
   download directory. Both happened. Here the settings object is built, applied
   to the tool's in-memory configuration, verified, and never saved, so there is
   no shared file left for another process to revert.
2. **The credential is materialised and erased (R4).** The wrapped tool persists
   its own plaintext session beside its settings and refreshes it silently. It is
   pointed at a private short-lived file instead, and the refreshed session goes
   back to the keychain.
3. **Failures are translated into the contract.** The tool raises whatever its
   client raises. An authentication rejection becomes an invocation-level
   AUTH_FAILED naming the replacement path (AE9), not a pile of missing tracks.
4. **The landed FILE is checked, not just the request (R-196).** The lossless
   rule used to be enforced at the setting alone, so the product asked for
   LOSSLESS, the provider sent AAC, and nothing between them ever looked. Every
   layer was green while the central promise failed. ``codec_of`` reads what
   actually arrived and ``landed_file`` refuses it under a strict policy.

WHAT IS DELIBERATELY NOT PROVEN BY THE TEST SUITE. That a real download works.
That needs an account, an authorised session, and the network, and it is the
attended smoke test U13 recorded. What IS proven here is everything between the
contract and the tool: the settings translation, the verification, the credential
lifetime, and the error translation, all of which are pure or injectable.
"""

from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractContextManager
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
    Offer,
    Remedy,
    TrackRequest,
    TrackSource,
    verify_applied,
)
from cratekit.core import binaries, provider_gate

#: Cratekit's quality vocabulary to the wrapped tool's. The tool takes the
#: streaming client's own enum VALUE as a string, and its factory default is the
#: lossy one, which is precisely why the value is pushed explicitly on every
#: invocation rather than left to whatever the tool last wrote down.
QUALITY_BY_POLICY: dict[str, str] = {
    "lossless": "LOSSLESS",
    "hi_res": "HI_RES_LOSSLESS",
    "lossy": "HIGH",
}

#: The file name the wrapped tool expects its session in.
TOKEN_FILENAME = "token.json"

#: Every keyword ``fetch`` hands the wrapped tool's downloader. Named here rather
#: than only spelled at the call so a test can assert the SET, which is the shape
#: R-197 needed: the tool declares all four of the missing ones with ``None``
#: defaults, so dropping one is accepted at construction and only dies later.
#:
#: Seven of the constructor's nine. ``skip_existing`` stays at its ``False``
#: default because this product always downloads, and ``progress_gui`` belongs to
#: the half of the tool that was not vendored.
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

#: What the wrapped tool names the file it lands, expressed in ITS template
#: language. Deliberately just the provider's track identifier: naming is U4's
#: engine working from the declared template, and letting the downloader choose a
#: library name would put a second naming authority in the pipeline. A staging
#: file named for the identifier that was requested is also unambiguous to match
#: back, which a name built from metadata is not.
STAGING_TEMPLATE = "{track_id}"


def tool_settings(
    settings: AdapterSettings, *, resolve: Callable[[str], str] = binaries.resolve
) -> dict[str, Any]:
    """The wrapped tool's setting names and the values this run requires.

    The single source of what gets pushed AND what gets verified. Splitting those
    into a push list and a separate check list is how the source system's guard
    ended up watching two keys while the tool had more; one mapping means a
    setting added here is verified by existing (P4).

    ``resolve`` is a PARAMETER rather than a call into the binaries module,
    which is what keeps the rest of this function pure. Every existing caller
    gets the real lookup, and a test can drive both answers without depending on
    what happens to be installed on the machine running it.

    Each entry's drift has a different cost. A reverted quality silently violates
    the lossless rule. A reverted download path sends files somewhere no later
    stage looks. A reverted name template hands naming back to the downloader. A
    reverted ffmpeg path is the quietest of the four: the tool turns FLAC
    extraction off, logs one warning through a logger this adapter discards, and
    lands a lossy file that every later stage treats as the track (R-195).
    """
    try:
        ffmpeg = resolve("ffmpeg")
    except binaries.BinaryNotFound as exc:
        # An override the user set and got wrong is a different instruction from
        # an encoder they never installed. Installing ffmpeg does not fix a
        # CRATEKIT_BIN_FFMPEG pointing at nothing, and the binaries module
        # already made that distinction; collapsing both onto one token here
        # would throw it away at the last hop.
        broken_override = exc.remedy is binaries.Remedy.FIX_BINARY_OVERRIDE
        # Refused rather than pushed empty. Empty is the tool's factory default
        # and it is exactly what it reads as "do not extract FLAC", so an absent
        # encoder would otherwise arrive as a successful lossy download. Doctor
        # asks whether ffmpeg exists on this machine; the tool asks whether it
        # was told the path, and the two agreed only where somebody had already
        # run the wrapped tool's own config by hand.
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
        # Pushed for the same reason as the quality above, and it is the same
        # argument: the tool's factory default for this is True, but the value
        # this run gets is whatever the tool last wrote to its own settings file,
        # and a run that finds it False lands an m4a while reporting success.
        # KTD20's whole point is that a setting this product depends on is stated
        # every invocation rather than inherited.
        "extract_flac": True,
    }


def apply_settings(
    target: Any,
    settings: AdapterSettings,
    *,
    resolve: Callable[[str], str] = binaries.resolve,
) -> None:
    """Push this run's settings onto the tool's in-memory configuration, then check.

    ``target`` is the tool's settings data object. It is written through
    ``setattr`` and read back through ``getattr`` on the same object, which is
    what makes the verification meaningful: a tool that coerces, ignores, or
    renames a field is caught here rather than by the wrong files turning up
    later.

    Nothing is saved. That is the entire KTD20 change, and it is one absent call.
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

#: What the wrapped tool's stored session must be for this product to use it.
#: The provider gates lossless audio behind the PKCE client, so a device-flow
#: session is not a lesser credential, it is one that silently downgrades every
#: download (R-196).
REAUTHORISE_HINT = (
    "mint a new one with the vendored downloader's own login command, then record "
    "it with `crate login provider-session --from-file`"
)


def login_mode(stored: object, *, had_stored_session: bool) -> str | None:
    """Why this stored session cannot be used, or None to proceed with PKCE.

    Pure, and a function rather than an ``if`` inside ``authenticate`` for one
    reason: ``authenticate`` returns early on an injected session and imports the
    wrapped tool's classes inside itself, so nothing in the offline suite can
    reach a decision written there. This is the checking path, and it is the half
    that can be proven.

    A session with no PKCE marker is refused rather than used. The alternative is
    to load it and let the post-landing codec guard catch the lossy file, which
    works and is slower, noisier, and names the symptom instead of the cause. The
    refusal is also what makes the marker load-bearing: a flag nothing reads is a
    flag that stops being written.
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

    Ported from the wrapped tool's own check, which tests for "401", "OAuth", or
    "token" anywhere in the message. That is broad enough to catch an unrelated
    error whose text happens to mention a token, which is why it is never asked
    on its own; see ``raise_if_session_dead``.
    """
    text = str(exc)
    return "401" in text or "OAuth" in text or "token" in text.lower()


def raise_if_session_dead(exc: BaseException) -> None:
    """Escalate a per-track failure to an invocation failure when the session died.

    The permanence question is asked FIRST, and the order is the whole point. The
    wrapped tool's authentication heuristic matches the word "token" anywhere in
    a message, so a provider error that says a track's stream token is not found
    would be read as a dead session and would abort a run that had nothing wrong
    with it. An explicit not-found is a fact about the track and is never re-read
    as a fact about the session.

    Narrowing the heuristic instead was the alternative. It is worse: the
    heuristic belongs to code whose upstream is gone, so a local narrowing is a
    patch to re-apply forever, while an ordering is a property of our own call.
    """
    from cratekit.acquire.adapter import (  # noqa: PLC0415
        TrackOutcome,
        classify_unavailable,
        raise_if_defect,
    )

    # A defect first, because the authentication heuristic below matches the
    # word "token" anywhere, and ``'NoneType' object has no attribute 'token'``
    # is a bug in code, not a dead session (R-348).
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

    The import is inside ``authenticate`` rather than at module scope so that
    importing this adapter, listing it in the registry, and naming it as the
    thing that broke all stay possible on a machine where the tool's own
    dependencies are missing (KTD7). An adapter that cannot be named while it is
    broken cannot be replaced.

    ``session`` and ``tool`` are injectable so the translation layer, which is
    where the defects actually live, is provable without an account. What cannot
    be injected away is the download itself, and that method is kept to the
    fewest possible decisions for exactly that reason.
    """

    def __init__(
        self,
        settings: AdapterSettings,
        token_path: Path,
        *,
        session: Any = None,
        tool: Any = None,
        downloader: Any = None,
    ) -> None:
        self._settings = settings
        self._token_path = token_path
        self._session: Any = session
        self._tool: Any = tool
        self._tidal: Any = None
        #: The provider gate over the tool's own session (R-705), on the same
        #: interval and cooldown the catalogue and the account pace with, read
        #: off the frozen configuration the settings came from.
        self._gate = provider_gate.Gate(settings.gate)
        #: The downloader CLASS, injectable so the construction R-197 got wrong is
        #: provable without an account. Only the deferred import below is left
        #: unreachable offline, instead of the whole of ``fetch``.
        self._downloader: Any = downloader

    def authenticate(self) -> None:
        # THE GATE IS ASKED BEFORE ANYTHING IS BUILT OR LOGGED IN (R-705). A
        # download started inside the cooldown a rate limited sweep left behind
        # refuses here, naming the time it lifts, and makes no call; the worker
        # above turns that into a park, so the item stays queued.
        self._gate.assert_open()
        if self._session is not None:
            # An injected session is already authorised. The settings still get
            # pushed and verified when a tool object came with it, so the KTD20
            # half of authenticate is exercised rather than skipped.
            if self._tool is not None:
                apply_settings(self._tool.data, self._settings)
            self._gate.attach(self._session)
            return

        try:
            from cratekit._vendor.tidal_dl_ng.config import Settings, Tidal  # noqa: PLC0415
        except ImportError as exc:  # pragma: no cover - needs the core deps absent
            raise AdapterBroken(
                f"the vendored downloader could not be imported ({exc}); its "
                f"dependencies ship with the core install and one of them is missing",
                remedy=Remedy.SWITCH_ADAPTER,
            ) from exc

        self._tool = Settings()
        apply_settings(self._tool.data, self._settings)

        tidal = Tidal(self._tool)
        # THE GATE IS ATTACHED BEFORE THE LOGIN, so the login is the first paced
        # call of the run and the tool's own retries on a rate limit, which it
        # would otherwise make as fast as it can, wait their turn. The tool is
        # a singleton, so on a second build in one process this wraps the same
        # session again, which ``attach`` makes a no-op.
        self._gate.attach(tidal.session)
        # Point the tool at the private, short-lived session file instead of the
        # plaintext one it would otherwise write into the user's config directory.
        # Both attributes are set: one is where it READS, the other is the base
        # directory it would create under on a save.
        tidal.file_path = str(self._token_path)
        tidal.path_base = str(self._token_path.parent)
        tidal.token_from_storage = tidal.read(str(self._token_path))

        refusal = login_mode(tidal.data, had_stored_session=tidal.token_from_storage)
        if refusal is not None:
            raise AdapterAuthFailed(
                f"{refusal}. To fix it, {REAUTHORISE_HINT}.",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            )

        try:
            authorised = tidal.login_token(do_pkce=True)
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            raise AdapterAuthFailed(
                f"the provider rejected the stored session ({exc})",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            ) from exc
        if not authorised:
            raise AdapterAuthFailed(
                "the stored provider session is no longer valid",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            )
        self._tidal = tidal
        self._session = tidal.session

    def offer(self, request: TrackRequest) -> Offer:
        """What the provider has for this track, as a lossless yes or no.

        The quality string is matched rather than compared for equality because
        the client publishes several lossless tiers and adding one upstream must
        not silently start refusing tracks under strict policy.
        """
        try:
            track = self._session.track(request.key)
        except Exception as exc:
            raise_if_session_dead(exc)
            raise
        quality = str(getattr(track, "audio_quality", "") or "")
        return Offer(lossless="LOSSLESS" in quality.upper(), detail=quality)

    def fetch(self, request: TrackRequest, destination: Path) -> Path:
        from cratekit._vendor.tidal_dl_ng.constants import MediaType  # noqa: PLC0415

        event_abort, event_run = download_events()
        progress, progress_overall = disabled_progress()
        downloader_class = self._downloader or _vendored_downloader()
        downloader = downloader_class(
            tidal_obj=self._tidal,
            path_base=str(destination),
            fn_logger=_discard_tool_logging,
            event_abort=event_abort,
            event_run=event_run,
            progress=progress,
            progress_overall=progress_overall,
        )
        try:
            ok, landed = downloader.item(
                file_template=STAGING_TEMPLATE,
                media_id=str(request.key),
                media_type=MediaType.TRACK,
            )
        except Exception as exc:
            raise_if_session_dead(exc)
            raise
        # ASKED AGAIN AFTER THE TOOL RETURNS (R-705). The wrapped tool catches
        # every exception inside its download and answers "no file", so a trip
        # the gate raised mid download would otherwise read as one unavailable
        # track and the worker would claim the next one. The gate remembers the
        # trip, and asking it here turns that answer back into the park.
        self._gate.assert_open()
        return landed_file(ok, landed, request.key, policy=self._settings.lossless_policy)


def _vendored_downloader() -> Any:  # pragma: no cover - needs the vendored tree's deps
    """The wrapped tool's downloader class, imported at CALL time (KTD7)."""
    from cratekit._vendor.tidal_dl_ng.download import Download  # noqa: PLC0415

    return Download


def download_events() -> tuple[Event, Event]:
    """The abort and run events, in the STATES the wrapped tool requires.

    Returned as a pair rather than built at the call because their states are the
    requirement and are invisible from the keyword names alone. ``event_run`` is
    SET and ``event_abort`` is CLEAR.

    ``Download._download_segment`` runs ``if not self.event_run.is_set():
    self.event_run.wait()`` inside its worker pool, and the vendored
    ``HandlingApp.__init__`` is the only thing in that tree that ever sets it. A
    fresh unset ``Event`` therefore blocks every segment worker on something
    nothing will wake, so the failure is a HANG rather than an error and no
    message names its cause. Passing the keyword is not enough.
    """
    event_run = Event()
    event_run.set()
    return Event(), event_run


def disabled_progress() -> tuple[Any, Any]:
    """The tool's two progress bars, rendering nothing.

    The wrapped tool touches these inside the download and does not check for
    None first, which is the half of R-197 that returned ``(False, path)`` and
    logged nothing. They are real ``rich`` objects rather than stubs, because a
    stub would be a second model of an interface the vendored tree can change
    under us; ``disable=True`` keeps ``add_task`` and ``update`` working while
    writing nothing to a stream a caller may be parsing (R32).
    """
    from rich.progress import Progress  # noqa: PLC0415 - same deferral as the tree above

    return Progress(disable=True), Progress(disable=True)


#: Whether a container is lossless, when the container alone decides it.
#:
#: Keyed by mutagen's CLASS name rather than by file suffix, and the difference
#: is the whole point: a ``.m4a`` holds AAC or ALAC and the suffix cannot say
#: which, so a suffix test gives the wrong answer for the exact container this
#: defect produced. MP4 is deliberately absent from this table; see
#: ``MP4_LOSSLESS_CODECS``.
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

#: The MP4 codec strings that are lossless. Measured, not assumed: mutagen
#: exposes ``info.codec`` on MP4 alone. FLAC, WAV, AIFF and MP3 all report None,
#: which is why a None codec means "the container decided" rather than "this file
#: could not be read". Reading None as unreadable would refuse every real FLAC,
#: which is the opposite of what this guard is for.
MP4_LOSSLESS_CODECS: frozenset[str] = frozenset({"alac"})


def codec_of(path: Path) -> tuple[str, bool | None]:
    """What landed, as ``(name, lossless)``. ``lossless`` is None when unreadable.

    Three answers, not two, because "this file is lossy" and "nothing here could
    be read" are different facts and lead to different sentences. Mutagen is
    imported inside the function, the convention ``core/tags.py`` sets, so this
    module stays importable on an install with no audio stack.
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
    ok: bool,
    landed: object,
    key: str,
    *,
    policy: LosslessPolicy = LosslessPolicy.STRICT,
    probe: Callable[[Path], tuple[str, bool | None]] = codec_of,
) -> Path:
    """Turn the tool's ``(succeeded, path)`` pair into a file or an exception.

    Pulled out of ``fetch`` because it is the only DECISION in a method that
    otherwise cannot be run without an account, and it is the decision that
    matters most. The tool reports a skip as a successful call carrying a false
    flag, which is precisely the shape that made "nothing was new" and "the
    download failed" the same observation in the source system.

    Raising sends it back through the classifier, where it becomes a transient
    result that stays re-queueable. Returning a path for a file that is not there
    would send a phantom into tagging.

    THE CODEC CHECK IS HERE, at the acceptance, and not at the request. The
    lossless rule was enforced at the SETTING and never at the FILE, which is how
    the product's central promise failed silently from July: the setting said
    LOSSLESS, the provider sent AAC, and nothing between them ever looked. This
    is the cheap half of that problem and it is what catches the next demotion.

    ``LosslessRefused`` rather than ``AdapterBroken``, and the reason is a defect
    rather than a preference. An adapter-level failure raised from inside the per
    track loop makes ``acquire_with_source`` build a failed ``InvocationResult``
    carrying whatever landed earlier in the same run, and that constructor
    refuses a failed invocation holding any permanently unavailable result. One
    delisted track earlier in the batch would turn this refusal into an uncaught
    ValueError. Per track also matches what the adapter already does with the
    identical condition seen at the OFFER, so one unreadable file does not end a
    fifty track sync.

    The refused file is left where it landed. Deleting a file on the strength of
    a probe is a destructive act, and that file is the evidence somebody
    diagnosing the next demotion will want.
    """
    if not ok:
        raise RuntimeError(f"the downloader reported no file for {key}")
    path = Path(str(landed))
    if policy is not LosslessPolicy.STRICT:
        return path

    name, lossless = probe(path)
    if lossless is None:
        # A plain error, NOT a policy refusal, and the difference is what the
        # user is told to do. A file nothing could parse is almost always a
        # truncated or interrupted download, so it goes back through the
        # classifier as transient and stays re-queueable. Raising
        # ``LosslessRefused`` here would carry RELAX_LOSSLESS_POLICY, which tells
        # somebody to loosen the rule that just caught an unreadable file, and
        # loosening it would make the product ACCEPT that file.
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


class _DiscardedToolLogging:
    """Absorb the wrapped tool's logging: every method it calls, writing nothing.

    THE TOOL SAYS CALLABLE AND USES A LOGGER. Its ``fn_logger`` parameter is
    annotated ``Callable`` and its body never calls the value; it calls
    ``.debug``, ``.info``, ``.error`` and ``.exception`` on it, at twenty two
    sites across the vendored tree. A plain function satisfied the annotation
    and every offline test, because every test injects a fake tool, and died on
    the first real download with ``'function' object has no attribute 'info'``,
    which the translation in ``_source`` then reported as a transient provider
    outage. Found 2026-09-16 on the first real track through this adapter, the
    observation R-210 asked for (#82).

    Structured output is U5's envelope, so tool chatter is dropped here rather
    than allowed onto a stream a caller may be parsing. ``__call__`` stays so the
    annotation's promise holds as well as the body's. The method set is pinned
    by ``tests/test_adapter_contract.py``, which reads it off the vendored tree
    rather than off a list here, so a revendor that starts calling ``.warning``
    fails the suite instead of the next real download.
    """

    def __call__(self, *_args: object, **_kwargs: object) -> None:
        return None

    def debug(self, *_args: object, **_kwargs: object) -> None:
        return None

    def info(self, *_args: object, **_kwargs: object) -> None:
        return None

    def warning(self, *_args: object, **_kwargs: object) -> None:
        return None

    def error(self, *_args: object, **_kwargs: object) -> None:
        return None

    def exception(self, *_args: object, **_kwargs: object) -> None:
        return None

    def critical(self, *_args: object, **_kwargs: object) -> None:
        return None


#: The one instance the adapter hands the tool. A name rather than a class so the
#: construction site reads as before and a test can ask the same object.
_discard_tool_logging = _DiscardedToolLogging()


class VendoredAdapter(BaseAdapter):
    """The default adapter: the vendored downloader behind the declared contract."""

    name = "tidal_dl_ng"

    def _session_scope(self) -> AbstractContextManager[object]:
        return provider_session.materialised_session(filename=TOKEN_FILENAME)

    def _source(self, scope: object) -> TrackSource:
        token_path = getattr(scope, "path", None)
        if token_path is None:  # pragma: no cover - only a misconfigured scope
            raise AdapterBroken(
                "no provider session was materialised for this run",
                remedy=Remedy.REPAIR_CREDENTIAL_STORE,
            )
        return _VendoredSource(self.settings, Path(token_path))


__all__ = [
    "DOWNLOADER_ARGUMENTS",
    "LOSSLESS_BY_CONTAINER",
    "MP4_LOSSLESS_CODECS",
    "QUALITY_BY_POLICY",
    "REAUTHORISE_HINT",
    "STAGING_TEMPLATE",
    "TOKEN_FILENAME",
    "VendoredAdapter",
    "apply_settings",
    "codec_of",
    "disabled_progress",
    "download_events",
    "is_authentication_failure",
    "landed_file",
    "login_mode",
    "raise_if_session_dead",
    "tool_settings",
]
