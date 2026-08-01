"""The alternative adapter that proves R9 (KTD5). Written against the same contract.

WHY THIS ONE. R9 requires at least one alternative proven against the interface
BEFORE launch, not after the outage that needs it, and the alternative was chosen
on evidence rather than popularity: this tool broke on the same provider
authentication change in March 2026 that killed the vendored downloader, and it
shipped a confirmed fix. That is the resilience the boundary exists to exploit.
It also locates the boundary correctly. What both the provider and the competing
forks contest is credentials and authentication, so that is the layer the adapter
must isolate, and it is the layer these two implementations differ most in.

WHAT "PROVEN" MEANS HERE, PRECISELY. Not that a download runs. This adapter is
implemented against the declared contract and tested with the third-party tool
ABSENT, which is the state of the machine that runs the suite and of any friend's
clone that never needed a replacement. What is proven is that the interface can
EXPRESS a second tool: its quality vocabulary, its credential shape, its error
translation, and its absence all have a place in the contract without the
contract bending. An interface that could only describe the tool it was extracted
from would look identical to this one right up until it was needed.

WHAT MAKES IT A REAL SECOND IMPLEMENTATION AND NOT A COPY:

* Its quality vocabulary is numeric tiers, not the streaming client's enum names,
  so the settings translation is genuinely a translation.
* It takes quality per call rather than from a settings object it keeps, so there
  is no persistent file here to revert and nothing to verify after a write. KTD20
  is satisfied by a different route, which is worth noticing: the decision moved
  the setting into the adapter, and how each tool then receives it is the tool's
  business.
* Its credential is a configuration file it reads, not a token file the client
  library manages, so the session materialisation writes a different shape.
* It is absent by design. The vendored adapter's failure mode is a broken import
  of code that is present; this one's is a package that was never installed, and
  the two need different remedies.

WHAT IS SHARED, AND WHY THAT IS CORRECT. The acquisition loop. The order of
operations, authenticate then per track offer, policy, fetch, pace, is the
contract itself, not an implementation detail. Letting each adapter write its own
order is how the source system ended up with two call sites that classify the
same provider failure differently.
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

#: The distribution that provides this adapter. A NAME, never an install command:
#: what the user types depends on their platform and package manager, and only
#: the CLI layer knows either (D2).
DISTRIBUTION = "streamrip"

#: Cratekit's quality vocabulary to this tool's numeric tiers. The tool grades
#: quality as an integer rather than a name, and its own default is the lossy
#: tier, so the value is pushed on every invocation for the same reason it is
#: pushed for the vendored one (KTD20).
QUALITY_TIERS: dict[str, int] = {
    "lossy": 1,
    "lossless": 2,
    "hi_res": 3,
}

#: Tiers at or above this are lossless. Expressed as a threshold rather than a
#: set because the tool adds higher tiers over time and a set would start
#: refusing new ones under strict policy.
LOSSLESS_TIER_FLOOR = 2

#: The file name this tool expects its credentials in.
CREDENTIAL_FILENAME = "config.toml"


def quality_tier(settings: AdapterSettings) -> int:
    """The numeric tier this run requires.

    An unrecognised quality name is a refusal rather than a fallback. Falling
    back would silently pick a tier, and the only sensible fallback value is the
    tool's default, which is the lossy one; that is the precise shape of the
    failure KTD20 exists to remove.
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
    """The I/O half. Imports the third-party tool only when a run actually starts.

    The import failure is handled as a distinct case rather than folded into a
    generic breakage, because "you chose an adapter whose tool is not installed"
    is the single most likely way this adapter fails and it has a remedy the user
    can act on immediately. A generic "adapter broken" would send them looking
    for a defect.
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
        # Resolved BEFORE anything is downloaded, for the same reason the other
        # adapter verifies its settings before its first fetch: a quality this
        # adapter cannot express must stop the run at track zero, not at track
        # forty, and certainly not by quietly taking the tool's lossy default.
        self._tier = quality_tier(self._settings)
        module = self._load()
        # The tool authenticates from a configuration file it is given the path
        # to, which is why the session materialisation writes one and erases it
        # afterwards. Its client surface has moved between releases, so the entry
        # point is resolved by name and a missing one is reported as breakage
        # rather than raising an attribute error from inside a library.
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
            # Already in the contract's vocabulary. Re-wrapping would relabel a
            # broken install as a stale session and send the user to the wrong fix.
            raise
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            raise AdapterAuthFailed(
                f"{DISTRIBUTION} could not authorise the stored session ({exc})",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
            ) from exc

    def offer(self, request: TrackRequest) -> Offer:
        """Ask the tool what it has, in ITS vocabulary, and answer in the contract's.

        A missing quality field reads as tier zero, which is below the lossless
        floor and therefore refused under strict policy. Defaulting the other way
        would let a tool that stopped reporting quality quietly fill the library
        with lossy files, which is the same failure KTD20 removes from settings.
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
    "CREDENTIAL_FILENAME",
    "DISTRIBUTION",
    "LOSSLESS_TIER_FLOOR",
    "QUALITY_TIERS",
    "StreamripAdapter",
    "offer_from_tier",
    "quality_tier",
]
