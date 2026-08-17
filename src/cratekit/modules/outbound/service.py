"""The two remote mutations this product is allowed to make.

A streaming account is mutated only by adding a heart or adding a track to a
playlist. There is no remove, no un-heart, no un-color, and no playlist
delete on this protocol. Deletion never propagates to a streaming service
(R36). The type is the rule: a caller that wants a remove has nowhere to
call it.
"""

from __future__ import annotations

from typing import Protocol


class RemoteAccount(Protocol):
    """Add-only writes against one streaming account."""

    def match_track(self, *, identity: str, isrc: str = "") -> str | None:
        """The remote track id for this library identity, or None if unmatched."""

    def add_heart(self, remote_id: str) -> None:
        """Heart one remote track. Idempotent if already hearted."""

    def has_heart(self, remote_id: str) -> bool:
        """Whether the account already hearts this remote track."""

    def create_playlist(self, name: str) -> str:
        """Create one remote playlist and return its stable remote identifier."""

    def add_to_playlist(self, playlist_id: str, remote_id: str) -> None:
        """Add one remote track to a playlist. Idempotent if already a member."""

    def playlist_tracks(self, playlist_id: str) -> tuple[str, ...]:
        """Remote track identifiers currently on the playlist, in order."""
