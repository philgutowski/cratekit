"""The alternative adapter that proves R9 (KTD5), written against the same contract.

It proves the interface can express a second tool, tested with the tool absent: a
numeric quality vocabulary, quality passed per call (KTD20 by another route), a
configuration file as its credential, and an uninstalled package as its failure mode.
The acquisition loop stays shared because its order is the contract itself.
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
)

#: The distribution that provides this adapter, a name and never an install command (D2).
DISTRIBUTION = "streamrip"

#: Cratekit's quality vocabulary to this tool's numeric tiers, pushed on every call
#: because the tool's own default is lossy (KTD20).
QUALITY_TIERS: dict[str, int] = {
    "lossy": 1,
    "lossless": 2,
    "hi_res": 3,
}

#: Tiers at or above this are lossless; a threshold so newer higher tiers still pass.
LOSSLESS_TIER_FLOOR = 2

#: The file name this tool expects its credentials in.
CREDENTIAL_FILENAME = "config.toml"


def quality_tier(settings: AdapterSettings) -> int:
    """The numeric tier this run requires; an unknown name refuses rather than fall back
    to the tool's lossy default (KTD20).
    """
    try:
        return QUALITY_TIERS[settings.quality]
    except KeyError:
        raise AdapterBroken(
            f"{settings.quality!r} is not a quality this adapter can express; "
            f"it grades quality as one of {sorted(QUALITY_TIERS)}",
            remedy=Remedy.REPAIR_ADAPTER_SETTINGS,
        ) from None


def offer_from_tier(tier: int) -> Offer:
    """Read the tool's per-track tier as the contract's lossless question."""
    return Offer(lossless=tier >= LOSSLESS_TIER_FLOOR, detail=f"tier {tier}")


class _StreamripSource:
    """The I/O half, importing the tool only when a run starts.

    A missing install is its own case, since it is the likeliest failure and the user
    can act on it at once.
    """

    def __init__(self, settings: AdapterSettings, credential_path: Path) -> None:
        self._settings = settings
        self._credential_path = credential_path
        self._client: Any = None
        self._tier: int | None = None

    def _load(self) -> Any:
        try:
            import streamrip  # noqa: PLC0415 - see the class docstring
        except ImportError as exc:
            raise AdapterBroken(
                f"the {DISTRIBUTION} distribution is not installed on this machine, "
                f"so this adapter cannot run",
                remedy=Remedy.INSTALL_ADAPTER,
            ) from exc
        return streamrip

    def authenticate(self) -> None:
        # Resolved before any download, so an inexpressible quality stops at track zero.
        self._tier = quality_tier(self._settings)
        module = self._load()
        # The client entry point moves between releases, so it is resolved by name and
        # a missing one reported as breakage.
        factory = getattr(module, "Client", None) or getattr(module, "client", None)
        if factory is None:
            raise AdapterBroken(
                f"the installed {DISTRIBUTION} release exposes no client entry point "
                f"this adapter recognises",
                remedy=Remedy.SWITCH_ADAPTER,
            )
        try:
            self._client = factory(config_path=str(self._credential_path))
            self._client.login()
        except (AdapterAuthFailed, AdapterBroken):
            # Already contract vocabulary; re-wrapping would point at the wrong fix.
            raise
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            raise AdapterAuthFailed(
                f"{DISTRIBUTION} could not authorise the stored session ({exc})",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            ) from exc

    def offer(self, request: TrackRequest) -> Offer:
        """Ask the tool for its tier and answer in the contract's vocabulary.

        A missing quality reads as tier zero, refused under strict policy, so a tool
        that stops reporting quality cannot fill the library with lossy files.
        """
        metadata = self._client.get(request.key, media_type="track")
        return offer_from_tier(int(metadata.get("quality", 0)))

    def fetch(self, request: TrackRequest, destination: Path) -> Path:
        landed = self._client.download(
            request.key, quality=self._tier, folder=str(destination)
        )
        return Path(landed)


class StreamripAdapter(BaseAdapter):
    """The replacement path AE9 names when the vendored adapter stops working."""

    name = "streamrip"

    def _session_scope(self) -> AbstractContextManager[object]:
        return provider_session.materialised_session(
            filename=CREDENTIAL_FILENAME, codec=provider_session.TOML
        )

    def _source(self, scope: object) -> TrackSource:
        credential_path = getattr(scope, "path", None)
        if credential_path is None:  # pragma: no cover - only a misconfigured scope
            raise AdapterBroken(
                "no provider session was materialised for this run",
                remedy=Remedy.REPAIR_CREDENTIAL_STORE,
            )
        return _StreamripSource(self.settings, Path(credential_path))


__all__ = [
    "CREDENTIAL_FILENAME", "DISTRIBUTION", "LOSSLESS_TIER_FLOOR", "QUALITY_TIERS",
    "StreamripAdapter", "offer_from_tier", "quality_tier",
]
