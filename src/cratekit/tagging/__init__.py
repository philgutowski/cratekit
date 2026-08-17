"""Genre and album-art tagging. Core, no extra.

Search is injectable so the suite can prove the write path without a
network. The live searchers (Beatport, Traxsource, Bandcamp) bind at the
CLI when a later worker runs the queued job.
"""

from __future__ import annotations

from cratekit.tagging.tag import Searcher, SearchHit, tag_folder

__all__ = ["SearchHit", "Searcher", "tag_folder"]
