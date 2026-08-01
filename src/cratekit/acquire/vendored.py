"""The vendored downloader, behind the interface. Nothing else may import it.

This is the boundary the whole unit exists to draw. ``cratekit._vendor`` is a
source tree whose upstream was deleted, which means every one of its APIs is
frozen at whatever the last extract happened to expose and none of them will ever
be fixed. Confining knowledge of that tree to one file is what makes the eventual
replacement a configuration change instead of a search across the codebase.

THREE THINGS THIS FILE OWNS, and each is a failure the source system had:

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

WHAT IS DELIBERATELY NOT PROVEN BY THE TEST SUITE. That a real download works.
That needs an account, an authorised session, and the network, and it is the
attended smoke test U13 recorded. What IS proven here is everything between the
contract and the tool: the settings translation, the verification, the credential
lifetime, and the error translation, all of which are pure or injectable.
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any

from cratekit.acquire import provider_session
from cratekit.acquire.adapter import (
    AdapterAuthFailed,
    AdapterBroken,
    AdapterSettings,
    BaseAdapter,
    Offer,
    Remedy,
    TrackRequest,
    TrackSource,
    verify_applied,
)

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

#: What the wrapped tool names the file it lands, expressed in ITS template
#: language. Deliberately just the provider's track identifier: naming is U4's
#: engine working from the declared template, and letting the downloader choose a
#: library name would put a second naming authority in the pipeline. A staging
#: file named for the identifier that was requested is also unambiguous to match
#: back, which a name built from metadata is not.
STAGING_TEMPLATE = "{track_id}"


def tool_settings(settings: AdapterSettings) -> dict[str, Any]:
    """The wrapped tool's setting names and the values this run requires.

    Pure, and the single source of what gets pushed AND what gets verified.
    Splitting those into a push list and a separate check list is how the source
    system's guard ended up watching two keys while the tool had more; one
    mapping means a setting added here is verified by existing (P4).

    Each entry's drift has a different cost. A reverted quality silently violates
    the lossless rule. A reverted download path sends files somewhere no later
    stage looks. A reverted name template hands naming back to the downloader.
    """
    return {
        "quality_audio": QUALITY_BY_POLICY.get(settings.quality, settings.quality.upper()),
        "download_base_path": str(settings.download_staging),
        "format_track": STAGING_TEMPLATE,
    }


def apply_settings(target: Any, settings: AdapterSettings) -> None:
    """Push this run's settings onto the tool's in-memory configuration, then check.

    ``target`` is the tool's settings data object. It is written through
    ``setattr`` and read back through ``getattr`` on the same object, which is
    what makes the verification meaningful: a tool that coerces, ignores, or
    renames a field is caught here rather than by the wrong files turning up
    later.

    Nothing is saved. That is the entire KTD20 change, and it is one absent call.
    """
    expected = tool_settings(settings)
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
    from cratekit.acquire.adapter import TrackOutcome, classify_unavailable  # noqa: PLC0415

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
    ) -> None:
        self._settings = settings
        self._token_path = token_path
        self._session: Any = session
        self._tool: Any = tool
        self._tidal: Any = None

    def authenticate(self) -> None:
        if self._session is not None:
            # An injected session is already authorised. The settings still get
            # pushed and verified when a tool object came with it, so the KTD20
            # half of authenticate is exercised rather than skipped.
            if self._tool is not None:
                apply_settings(self._tool.data, self._settings)
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
        # Point the tool at the private, short-lived session file instead of the
        # plaintext one it would otherwise write into the user's config directory.
        # Both attributes are set: one is where it READS, the other is the base
        # directory it would create under on a save.
        tidal.file_path = str(self._token_path)
        tidal.path_base = str(self._token_path.parent)
        tidal.token_from_storage = tidal.read(str(self._token_path))

        try:
            authorised = tidal.login_token()
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

    def fetch(self, request: TrackRequest, destination: Path) -> Path:  # pragma: no cover
        # Reaching the tool's downloader needs a live authorised session, so this
        # is the one method the offline suite cannot exercise. It is kept to the
        # fewest possible decisions for exactly that reason: everything decidable
        # was already decided above this line.
        from cratekit._vendor.tidal_dl_ng.constants import MediaType  # noqa: PLC0415
        from cratekit._vendor.tidal_dl_ng.download import Download  # noqa: PLC0415

        downloader = Download(
            tidal_obj=self._tidal,
            path_base=str(destination),
            fn_logger=_discard_tool_logging,
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
        return landed_file(ok, landed, request.key)


def landed_file(ok: bool, landed: object, key: str) -> Path:
    """Turn the tool's ``(succeeded, path)`` pair into a file or an exception.

    Pulled out of ``fetch`` because it is the only DECISION in a method that
    otherwise cannot be run without an account, and it is the decision that
    matters most. The tool reports a skip as a successful call carrying a false
    flag, which is precisely the shape that made "nothing was new" and "the
    download failed" the same observation in the source system.

    Raising sends it back through the classifier, where it becomes a transient
    result that stays re-queueable. Returning a path for a file that is not there
    would send a phantom into tagging.
    """
    if not ok:
        raise RuntimeError(f"the downloader reported no file for {key}")
    return Path(str(landed))


def _discard_tool_logging(*_args: object, **_kwargs: object) -> None:
    """Absorb the wrapped tool's progress logging.

    The tool requires a logging callable and writes free-form progress through
    it. Structured output is U5's envelope, so tool chatter is dropped here
    rather than allowed onto a stream a caller may be parsing.
    """


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
    "QUALITY_BY_POLICY",
    "STAGING_TEMPLATE",
    "TOKEN_FILENAME",
    "VendoredAdapter",
    "apply_settings",
    "is_authentication_failure",
    "landed_file",
    "raise_if_session_dead",
    "tool_settings",
]
