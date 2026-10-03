"""The remote mutations this product is allowed to make.

A streaming account is mutated by adding a heart, by adding a track to a
playlist, by retitling a playlist, by making a folder and by putting a playlist
in one. There is no remove, no un-heart, no un-color, and no playlist or folder
delete on this protocol. Deletion never propagates
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

    def match_track(
        self,
        *,
        identity: str,
        isrc: str = "",
        title: str = "",
        artist: str = "",
        agree: bool = False,
    ) -> str | None:
        """The remote track id for this library identity, or None if unmatched.

        ``title`` and ``artist`` are the row's own, the title with the library's
        naming head already off. They CHOOSE among tracks an exact key already
        named, several releases sharing one ISRC, and are never a search: an
        implementation that matched on them alone would heart a cover version
        (R-356).

        ``agree`` ASKS THE ONE TRACK TO AGREE TOO. By default a code the
        provider files one track under names that track, since the code came
        from the provider. A code read off a library file's own tag did not, and
        a file tagged with another recording's code would name the wrong track,
        so with ``agree`` even a single track must agree with the row (R-879).
        """

    def unmatched_reason(self, identity: str) -> str:
        """Why the last ``match_track`` of this identity answered None, or ``""``.

        Words for a person, carried on the unmatched row. Empty when the account
        has nothing more to say than "unmatched", and empty after a match. It
        reads and writes nothing on the account.
        """

    def add_heart(self, remote_id: str) -> None:
        """Heart one remote track. Idempotent if already hearted."""

    def has_heart(self, remote_id: str) -> bool:
        """Whether the account already hearts this remote track."""

    def create_playlist(self, name: str) -> str:
        """Create one remote playlist, private, and return its stable remote identifier.

        Private because the source system makes every playlist it creates
        private (R-834). The identifier is returned even when the provider
        refuses the private step after the create, because a create that raised
        would go unrecorded and the next item would make a second playlist.
        """

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

    # ── folders (R-835) ──────────────────────────────────────────────────────
    #
    # FIVE MEMBERS, AND NONE OF THEM TAKES ANYTHING AWAY. A label's shape on the
    # account is one folder holding one playlist per release year, so the
    # protocol can list a folder, make one, put a playlist in one, and add a
    # chunk of tracks at once. A move changes where a playlist sits and nothing
    # it holds; it deletes nothing and removes no track.

    def add_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Add tracks to a playlist in chunks the provider accepts, skipping members.

        Returns every asked identifier the playlist holds once the adds are
        done, already a member or added now. One the provider would not add is
        left out of the answer rather than raised, because one withdrawn track
        on a year of a label's catalogue is not a reason to add none of it.
        """

    def folders(self) -> dict[str, str]:
        """Every folder at the root of the account's playlists, identifier to name."""

    def folder_playlists(self, folder_id: str) -> dict[str, str]:
        """Every playlist one folder holds, identifier to name."""

    def create_folder(self, name: str) -> str:
        """Create one folder at the root of the account's playlists, and return its id.

        Never retried, on ``create_playlist``'s argument: a create that reached
        the provider and then timed out would be retried into a second folder.
        """

    def move_to_folder(self, playlist_id: str, folder_id: str) -> None:
        """Put one playlist the account holds into one folder. Idempotent."""
