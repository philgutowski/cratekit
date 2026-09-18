"""The remote mutations this product is allowed to make.

A streaming account is mutated by adding a heart, by adding a track to a
playlist, and by retitling a playlist. There is no remove, no un-heart, no
un-color, and no playlist delete on this protocol. Deletion never propagates
to a streaming service (R36). The type is the rule: a caller that wants a
remove has nowhere to call it.

**RETITLING IS NOT A REMOVAL, AND IT IS THE ONE WRITE THAT TOUCHES SOMETHING
THE PRODUCT DID NOT MAKE.** It exists because a title is how the source system
records what it has already taken: ``sync.playlists.SWEPT_PREFIX`` is a
convention the live account already carries, and a playlist Cratekit swept is
new to that system's next pass until the prefix is on it (R-358). Nothing is
lost by a retitle, no membership changes, and the name a playlist had is
recoverable from the name it now has. It is still irreversible enough that
``sync.marks`` makes it wait for the importable file and a recheck rather than
applying it when the run merely started.
"""

from __future__ import annotations

from typing import Protocol


class RemoteAccount(Protocol):
    """Add-only writes against one streaming account, plus a playlist retitle."""

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

    def rename_playlist(self, playlist_id: str, name: str) -> None:
        """Retitle one playlist the account owns, keyed by its identifier.

        The playlist is named by identifier and never by title, so a retitle
        applied twice lands on the same playlist rather than on whatever now
        carries the old name. It changes no membership and deletes nothing.

        An empty ``name`` is a refusal and never a no-op. An implementation
        whose client reads a blank title as "keep the current one" would
        otherwise report a rename over a playlist that never changed, which is
        the one wrong answer this member exists to make impossible.
        """
