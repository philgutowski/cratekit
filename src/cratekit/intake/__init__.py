"""Intake: every input shape becomes one internal list, then one library row.

This package owns the path from a set URL, a pasted tracklist, a playlist, or
one file on disk to a routed library entry. Matching, downloading, naming, and
tree writes already live elsewhere. What lives here is the orchestration and
the one COLLECTION TRACK emitter no other unit ports.

The initializer imports nothing heavy. Recognition talks to a paid service and
tagging talks to the network. Listing what this package can do must not spend
either.
"""

from __future__ import annotations

__all__ = [
    "collection_xml",
    "ingest",
    "normalize",
    "pipeline",
    "recognize",
    "repair",
]
