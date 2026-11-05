"""The remote mutations this product is allowed to make.

A streaming account is mutated by adding a heart, by adding a track to a
playlist, by retitling a playlist, by making a folder, by putting a playlist
in one, and by taking tracks off, or removing, a playlist THE PRODUCT ITSELF
CREATED. There is no un-heart, no un-color, and no delete of a playlist or a
folder anybody else made on this protocol, save the account root's three
kinds below (U143). Deletion in the library never
propagates to a streaming service (R36). The type is the rule: a caller that
wants any other remove has nowhere to call it.

**ONE REMOVAL, THE NARROWEST THAT DOES THE JOB (R-836).** ``remove_tracks``
takes tracks out of one playlist and nothing else, and an implementation
refuses it, before any call to the provider, for a playlist the outbound
ledger does not record as one the product created
(``ledger.product_made``). A playlist the source system or a person made,
including a label year playlist adopted by its name, is never touched. The
suite's removal scans admit this member and ``remove_playlist`` by name and
nothing else.

**AND ONE PLAYLIST REMOVAL, ON THE SAME RULE (U123).** ``remove_playlist``
removes one playlist and nothing else, refused before any provider call for a
playlist the ledger does not vouch for. ``label heard`` is its one caller, and
only for a label's dated playlist once its tracks sit in the year playlist.

**AND THE AUTHOR'S OWN PAIRED PLAYLISTS (U130).** A playlist the author made
and marked, with ``crate sync pair``, to stay the same list as one rekordbox
playlist is the one other playlist ``remove_tracks`` and ``order_tracks`` may
change, because the author asked for a removal on either side to be applied on
both (decided 2026-10-10). The pairs record vouches for it beside the ledger,
and a playlist the author did not pair is refused exactly as before. A removal
there takes a track off that one playlist and nothing else: no track leaves the
account or the library.

**AND THE ACCOUNT ROOT'S THREE KINDS, NAMED BY A GATE (U143).** The one
removal no ledger vouches for, because what it removes is nothing the product
made: ``remove_root_playlist`` removes a playlist at the root that is the
source system's label debris or holds no track, and ``remove_legacy_folder``
removes a root folder named as a legacy year folder once it holds nothing.
Each checks its kind on the provider's own answer before it removes, refuses a
playlist any ledger claims, and reads the removal back. ``crate organize``'s
root step is the one caller, and only for a row its gate showed by name.

**ORDERING IS NOT A REMOVAL, AND IT IS HELD TO THE SAME RULE.**
``order_tracks`` moves tracks within one playlist the ledger or the pairs
vouch for. It changes no membership, so nothing is lost by it, and it is still
refused for any other playlist, since a person's order is theirs.

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

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

#: The words an unmatched reason carries when a candidate track could not be
#: read, formatted into the reason by the adapter and read by the mirror, which
#: never remembers such a miss since it is not an answer about the row (R-1031).
UNREADABLE_CANDIDATE = "could not be read"

#: The words an unmatched reason carries when several releases agree with the
#: row and nothing told them apart (R-572), formatted into the reason by the
#: adapter. The mirror and the pairs read it to ask such a miss again, since
#: under ``any_agreeing`` a tie no longer misses (R-1032, U208).
AGREEING_RELEASES = "of them agree with this row's artist, title and version"


@dataclass(frozen=True, slots=True)
class PlaylistListing:
    """One playlist's tracks as one read gives them, with when each was added (U201).

    ``names`` is every track identifier to ``(artist, title)``, in the order
    first listed. ``added`` is each track's added time on the playlist as ISO
    8601 UTC text, or absent when the provider gave none. ``listed`` is how
    many track items the read returned, a track held twice counted twice, and
    ``declared`` the count the provider declares for the playlist, ``None``
    when it declares none.
    """

    names: dict[str, tuple[str, str]] = field(default_factory=dict)
    added: dict[str, str] = field(default_factory=dict)
    listed: int = 0
    declared: int | None = None

    @property
    def short(self) -> bool:
        """Whether the read may have left a track out.

        THE PROVIDER LEAVES OUT A TRACK THIS ACCOUNT CANNOT PLAY AND STILL
        COUNTS IT, so a read shorter than the declared count is missing tracks
        it cannot name, and a playlist declaring no count cannot be checked at
        all. Either is short, since a track missing from it is no evidence that
        a person took it off.
        """
        return self.declared is None or self.listed < self.declared


class RemoteAccount(Protocol):
    """Writes against one streaming account: adds, a retitle, and one narrow remove."""

    def match_track(
        self,
        *,
        identity: str,
        isrc: str = "",
        title: str = "",
        artist: str = "",
        agree: bool = False,
        album: str = "",
        any_agreeing: bool = False,
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

        ``album`` is the album tag of the row's own file. Among several releases
        that agree with the row and that the account hearts none of, the one
        whose album name is the file's is the match (R-572). Never a search.

        ``any_agreeing`` TAKES ONE OF A TIE rather than refusing it (R-1032):
        the mirror passes it, whose playlist is a listening copy where releases
        spelled alike are the same thing to hear, and since U208 the pairs,
        decided by Phillip at Sitting 54, so a paired playlist carries the
        tracks rekordbox holds. It narrows by the account's hearts and the
        file's album first, as without it, and then takes the lowest provider
        identifier, so every run takes the same one. It changes nothing but a
        tie: a release that does not agree is never taken, and a tie beside a
        candidate that could not be read still refuses. A heart never passes
        it, since there the heart is the person's own choice of release and
        R-572's refusal stands.
        """

    def screen_isrcs(self, codes: Iterable[str]) -> int:
        """Ask, in as few requests as the provider allows, which codes it files nothing under.

        Called by a plan before its first ``match_track``, with every code the
        plan will ask (U207). A later ``match_track`` of a code the provider
        answered as filed under nothing is answered unmatched with no request;
        every other code is asked as before, since a batch answer names one
        release per code and never says which release a row is. It writes
        nothing, raises nothing for a batch the provider could not answer (the
        codes are then asked one at a time), and returns the requests it made,
        zero for an account that has no batch form.
        """

    def unmatched_reason(self, identity: str) -> str:
        """Why the last ``match_track`` of this identity answered None, or ``""``.

        Words for a person, carried on the unmatched row. Empty when the account
        has nothing more to say than "unmatched", and empty after a match. It
        reads and writes nothing on the account.
        """

    def tie_broken(self, identity: str) -> bool:
        """Whether the last ``match_track`` of this identity took one of a tie (U208).

        True only when ``any_agreeing`` chose among releases that all agree
        with the row and that nothing else told apart, a match that without it
        would have been refused; false after any other match and after a miss.
        The pairs count it for the gate. It reads and writes nothing on the
        account.
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

    def folder_playlists_dated(self, folder_id: str) -> dict[str, tuple[str, datetime | None]]:
        """Every playlist one folder holds, identifier to its name and when it was made.

        U216. The same walk as :meth:`folder_playlists`, read off the same
        pages; the time is None where the account gave none, never guessed.
        """

    def folder_folders(self, folder_id: str) -> dict[str, str]:
        """Every folder one folder holds, identifier to name."""

    def create_folder(self, name: str) -> str:
        """Create one folder at the root of the account's playlists, and return its id.

        Never retried, on ``create_playlist``'s argument: a create that reached
        the provider and then timed out would be retried into a second folder.
        """

    def move_to_folder(self, playlist_id: str, folder_id: str) -> None:
        """Put one playlist the account holds into one folder. Idempotent."""

    # ── the one removal (R-836) ──────────────────────────────────────────────
    #
    # TWO MEMBERS: a read that names what a playlist holds, for the gate a
    # person approves a removal at, and the removal itself.

    def track_names(self, playlist_id: str) -> dict[str, tuple[str, str]]:
        """Every track on the playlist, remote identifier to ``(artist, title)``.

        A read, for the prune's gate, which lists every track it would take
        off by artist and title. It writes nothing.
        """

    def playlist_listing(self, playlist_id: str) -> PlaylistListing:
        """Every track on the playlist with its added time and the declared count (U201).

        A read, for the account mirror, which tells an edit a person made on the
        account from a track the read could not see. It writes nothing.
        """

    def remove_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Take tracks off one playlist the product created or the author paired.

        REFUSED BEFORE ANY PROVIDER CALL for a playlist the outbound ledger
        does not record as one the product created and no playlist pair names
        (U130). Every occurrence of an asked track comes off; nothing else on
        the playlist moves.

        Returns every asked identifier the playlist no longer holds once the
        removal is done, taken off now or already absent, so a resume asking
        again for one that came off before records it and takes nothing.
        """

    def order_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Put one playlist's tracks in this order, and change nothing else (U130).

        REFUSED BEFORE ANY PROVIDER CALL on :meth:`remove_tracks`'s rule. A
        track the playlist does not hold is not added and one it holds that
        the order does not name stays on it. Returns the playlist's order once
        the moves are done, read back.
        """

    def remove_playlist(self, playlist_id: str) -> None:
        """Remove one playlist the product created, and nothing else (U123).

        REFUSED BEFORE ANY PROVIDER CALL for a playlist the outbound ledger
        does not record as one the product created. A playlist the provider no
        longer has is already removed, so a resume asking again succeeds and
        removes nothing. No track leaves any other playlist.
        """

    # ── the account root's removals (U143) ───────────────────────────────────
    #
    # TWO MEMBERS, EACH NARROWED TO A KIND THE PROVIDER'S OWN ANSWER CONFIRMS,
    # since the playlist or folder is one no ledger records.

    def remove_root_playlist(self, playlist_id: str, kind: str) -> None:
        """Remove one root playlist of a kind the gate named, and nothing else.

        ``kind`` is ``kinds.DEBRIS`` or ``kinds.EMPTY``. REFUSED BEFORE ANY
        REMOVAL for any other kind, for a playlist any ledger claims, and for
        one the provider serves as not of that kind: debris must carry the
        source system's suffix, and an empty playlist must declare no track
        and no video. A playlist the provider no longer has is already
        removed. Read back: one still served is refused.
        """

    def remove_legacy_folder(self, folder_id: str) -> None:
        """Remove one empty legacy year folder at the root, and nothing else.

        REFUSED BEFORE ANY REMOVAL for a folder that is not at the root, whose
        name is not a legacy year folder's, or that holds any playlist or
        folder. A folder the root no longer lists is already removed. Read
        back: one still listed is refused.
        """
