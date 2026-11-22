"""Acquisition: the adapter boundary that makes the downloader replaceable (R9).

The vendored downloader's upstream is gone, so recovery means pointing the
product at a different tool through one declared contract. This initializer is
the registry and imports no adapter: an adapter's import pulls in the tool it
wraps, which may be missing or broken, and a broken adapter must still be
nameable (KTD7, AE9). Entries are strings resolved on demand.
"""

from __future__ import annotations

import importlib
from collections.abc import Mapping

from cratekit.acquire.adapter import AdapterSettings, Remedy, UnknownAdapter
from cratekit.core.config import current_adapter_name

#: Adapter name to ``"module:attribute"``. The name is the stable identifier
#: configuration records, never a display string (R19, D5). The conformance
#: suite derives its parameters from this mapping (P3). A retired name reads
#: through ``core.config.RETIRED_ADAPTER_NAMES`` (U197).
ADAPTERS: Mapping[str, str] = {
    "vendored": "cratekit.acquire.vendored:VendoredAdapter",
    "streamrip": "cratekit.acquire.streamrip:StreamripAdapter",
}


def alternatives_to(name: str) -> tuple[str, ...]:
    """The replacement paths when ``name`` broke (AE9), derived from the registry
    so they never go stale."""
    current = current_adapter_name(name)
    return tuple(other for other in ADAPTERS if other != current)


def load(name: str) -> type:
    """Resolve an adapter name to its class, importing it only now.

    An unknown name raises, so a configuration typo never silently switches tool.
    """
    try:
        target = ADAPTERS[current_adapter_name(name)]
    except KeyError:
        raise UnknownAdapter(
            f"no acquisition adapter is registered under {name!r}; "
            f"registered names are {', '.join(ADAPTERS)}",
            remedy=Remedy.CHOOSE_KNOWN_ADAPTER,
        ) from None
    module_name, _, attribute = target.partition(":")
    module = importlib.import_module(module_name)
    return getattr(module, attribute)


def build(name: str, settings: AdapterSettings, **kwargs: object):
    """Construct the named adapter with the settings it will own for this run."""
    return load(name)(settings, **kwargs)


__all__ = ["ADAPTERS", "alternatives_to", "build", "load"]
