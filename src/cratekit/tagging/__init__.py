"""Genre and album-art tagging. Core, no extra.

Search is injectable so the suite can prove the write path without a
network. The live searchers (Beatport, then Discogs; Traxsource and Bandcamp
off the default walk) live in
``searchers`` and a worker binds one through ``for_taxonomy`` at call
time, and its picture fetch through ``for_images``, so a test can
substitute a fake in process. A general catalogue asked by ISRC lives in
``published`` and is bound the same way, through its own ``for_taxonomy``.
"""

from __future__ import annotations

from cratekit.tagging.retag import retag_folder
from cratekit.tagging.searchers import catalogue_searcher, for_taxonomy
from cratekit.tagging.tag import Searcher, SearchHit, tag_folder

__all__ = [
    "SearchHit",
    "Searcher",
    "catalogue_searcher",
    "for_taxonomy",
    "retag_folder",
    "tag_folder",
]
