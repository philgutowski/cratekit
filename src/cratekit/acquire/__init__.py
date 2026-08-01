"""Acquisition: the adapter boundary that makes the downloader replaceable (R9).

The vendored downloader is a single point of failure whose upstream no longer
exists. Nothing can be installed from an index to replace it, so the only
recovery available to a user whose acquisition broke is to point the product at a
DIFFERENT tool. That is only possible if the tool is reachable through one
declared contract, and R9 requires at least one alternative proven against that
contract before launch rather than after the first outage.

This initializer is the REGISTRY, and it is deliberately import-free with respect
to the adapters themselves. Two reasons, and neither is style:

* An adapter's import pulls in the tool it wraps. The vendored one drags in a
  streaming client and a crypto extension; the alternative drags in a third-party
  package that may not be installed at all. Importing both to answer "which
  adapters exist" would make listing them cost more than using one, and would
  make the listing fail on exactly the machine that needs to read it (KTD7).
* AE9's replacement path has to be nameable while the current adapter is broken.
  A registry that imports what it names cannot name a broken adapter.

So entries are strings resolved on demand, and every adapter's identity, its
alternatives, and its selection by configuration are answerable without importing
any of them.
"""

from __future__ import annotations

import importlib
from collections.abc import Mapping

from cratekit.acquire.adapter import AdapterSettings, Remedy, UnknownAdapter

#: Adapter name to ``"module:attribute"``. The NAME is the stable identifier that
#: ``acquisition.adapter`` records in configuration, so it must never be a display
#: string that somebody might tidy up later (R19, D5).
#:
#: Adding an entry here is the whole cost of adding an adapter: the conformance
#: suite derives its parameter set from this mapping, so a new adapter is tested
#: against the full contract by arriving, not by somebody remembering (P3).
ADAPTERS: Mapping[str, str] = {
    "tidal_dl_ng": "cratekit.acquire.vendored:VendoredAdapter",
    "streamrip": "cratekit.acquire.streamrip:StreamripAdapter",
}


def adapter_names() -> tuple[str, ...]:
    """Every registered adapter name, in declaration order."""
    return tuple(ADAPTERS)


def alternatives_to(name: str) -> tuple[str, ...]:
    """The replacement paths available when ``name`` is the one that broke.

    AE9 requires an authentication failure to be reported as an adapter failure
    "naming the replacement path". Derived from the registry rather than written
    into each adapter, because an adapter that hand-lists its alternatives is one
    that goes stale the moment a third arrives, and going stale here means the
    user is told there is nowhere to go while somewhere to go exists.
    """
    return tuple(other for other in ADAPTERS if other != name)


def load(name: str) -> type:
    """Resolve an adapter name to its class, importing it only now.

    An unknown name raises rather than falling back to the default. A fallback
    here would turn a typo in configuration into a silent switch of the tool that
    touches the user's music, which is the class of surprise this whole unit
    exists to remove.
    """
    try:
        target = ADAPTERS[name]
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


__all__ = ["ADAPTERS", "adapter_names", "alternatives_to", "build", "load"]
