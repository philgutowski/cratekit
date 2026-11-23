"""The remote mutations this product is allowed to make.

A streaming account is mutated by adding a heart, adding a track to a playlist,
retitling a playlist, making a folder, putting a playlist in one, and by taking
tracks off, or removing, a playlist THE PRODUCT ITSELF CREATED. There is no
un-heart, no un-color, and no delete of anything anybody else made, save the
account root's kinds below (U143); deletion in the library never propagates to a
streaming service (R36). The type is the rule: a caller that wants any other
remove has nowhere to call it, and the suite's removal scans admit the four
removal members by name and nothing else.

**THE REMOVALS, EACH THE NARROWEST THAT DOES THE JOB.**

* ``remove_tracks`` (R-836) takes tracks out of one playlist, refused before any
  provider call unless the outbound ledger records it as the product's
  (``ledger.product_made``) or the author paired it with a rekordbox playlist
  (U130, decided 2026-10-10: a removal on either side is applied on both). A
  playlist the source system or a person made, a label year playlist adopted by
  its name included, is never touched.
* ``remove_playlist`` (U123) removes one playlist on the ledger's rule;
  ``label heard`` is its one caller, for a label's dated playlist once its
  tracks sit in the year playlist.
* ``remove_root_playlist`` and ``remove_legacy_folder`` (U143) remove what no
  ledger records, a root playlist that is label debris or holds no track and an
  empty legacy year folder, each checked on the provider's own answer, refused
  for anything a ledger claims, and read back. ``crate organize``'s root step,
  for a row its gate showed by name, is the one caller.

**ORDERING IS NOT A REMOVAL, AND IT IS HELD TO THE SAME RULE.**
``order_tracks`` changes no membership, and is still refused for a playlist the
ledger or the pairs do not vouch for, since a person's order is theirs.

**RETITLING IS THE ONE WRITE THAT TOUCHES SOMETHING THE PRODUCT DID NOT MAKE.**
Since U242 no mark retitles anything; the callers left are ``sync strip``, which
takes the retired ``DOWNLOADED `` prefix off (R-358), ``sync unmark``, which puts
a title back, and ``export set --rename``, which follows a rename in the library
(U140). Each records the title before it writes, and nothing is lost by it.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol

#: The words an unmatched reason carries when a candidate track could not be
#: read. The mirror reads it and never remembers such a miss, which is not an
#: answer about the row (R-1031).
UNREADABLE_CANDIDATE = "could not be read"

#: The words an unmatched reason carries when several releases agree with the
#: row and nothing told them apart (R-572). The mirror and the pairs read it to
#: ask such a miss again, since under ``any_agreeing`` a tie no longer misses
#: (R-1032, U208).
AGREEING_RELEASES = "of them agree with this row's artist, title and version"


@dataclass(frozen=True, slots=True)
class PlaylistListing:
    """One playlist's tracks as one read gives them, with when each was added (U201).

    ``names`` is every track identifier to ``(artist, title)``, in the order
    first listed; ``added`` each track's added time as ISO 8601 UTC text, absent
    when the provider gave none; ``listed`` how many track items the read
    returned, a repeat counted twice; ``declared`` the count the provider
    declares, ``None`` when it declares none.
    """

    names: dict[str, tuple[str, str]] = field(default_factory=dict)
    added: dict[str, str] = field(default_factory=dict)
    listed: int = 0
    declared: int | None = None

    @property
    def short(self) -> bool:
        """Whether the read may have left a track out.

        THE PROVIDER LEAVES OUT A TRACK THIS ACCOUNT CANNOT PLAY AND STILL COUNTS
        IT, so a read short of the declared count, or of no count, is short: a
        track missing from it is no evidence a person took it off.
        """
        return self.declared is None or self.listed < self.declared


class RemoteAccount(Protocol):
    """Writes against one streaming account: adds, a retitle, and the narrow removals."""

    def read_backs(self) -> tuple[dict[str, Any], ...]:
        """Every reading this account judged a write or an order by, in order (U226).

        Asks the provider nothing: each read back the writes recorded, with its
        readings and wait, for a run to carry as its facts.
        """
        ...

    def match_track(
        self, *, identity: str, isrc: str = "", title: str = "", artist: str = "",
        agree: bool = False, album: str = "", any_agreeing: bool = False,
    ) -> str | None:
        """The remote track id for this library identity, or None if unmatched.

        ``title`` and ``artist`` CHOOSE among tracks an exact key already named
        and are never a search, which would heart a cover version (R-356).
        ``agree`` asks even a lone track to agree with the row, for a code read
        off a file's own tag rather than from the provider (R-879). ``album``,
        the file's album tag, picks among agreeing releases the account hearts
        none of (R-572).

        ``any_agreeing`` TAKES ONE OF A TIE rather than refusing it (R-1032),
        after the hearts and the album narrow it, the lowest provider identifier
        so every run takes the same one: the mirror's listening copy passes it,
        and since U208 the pairs (Phillip, Sitting 54). A release that does not
        agree is never taken, a tie beside an unreadable candidate still
        refuses, and a heart never passes it, since there the person chose.
        """

    def screen_isrcs(self, codes: Iterable[str]) -> int:
        """Ask, in as few requests as the provider allows, which codes it files nothing under.

        Called by a plan before its first ``match_track`` with every code it will
        ask (U207); a later match of such a code is unmatched with no request.
        Writes nothing, raises nothing for a batch the provider could not answer,
        and returns the requests made, zero for an account with no batch form.
        """

    def unmatched_reason(self, identity: str) -> str:
        """Why the last ``match_track`` of this identity answered None, or ``""``.

        Words for a person, carried on the unmatched row; empty when there is
        nothing more to say than "unmatched", and after a match.
        """

    def tie_broken(self, identity: str) -> bool:
        """Whether the last ``match_track`` of this identity took one of a tie (U208).

        True only when ``any_agreeing`` chose a match that without it would have
        been refused. The pairs count it for the gate.
        """

    def add_heart(self, remote_id: str) -> None:
        """Heart one remote track. Idempotent if already hearted."""

    def has_heart(self, remote_id: str) -> bool:
        """Whether the account already hearts this remote track."""

    def create_playlist(self, name: str) -> str:
        """Create one remote playlist, private, and return its stable remote identifier.

        Private because the source system makes every playlist private (R-834).
        Returned even when the private step is refused, since a create that
        raised would go unrecorded and the next item would make a second one.
        """

    def add_to_playlist(self, playlist_id: str, remote_id: str) -> None:
        """Add one remote track to a playlist. Idempotent if already a member."""

    def playlist_tracks(self, playlist_id: str) -> tuple[str, ...]:
        """Remote track identifiers currently on the playlist, in order."""

    def rename_playlist(self, playlist_id: str, name: str) -> None:
        """Retitle one playlist the account owns, keyed by its identifier.

        By identifier, never by title, so a retitle applied twice lands on the
        same playlist. An empty ``name`` is a refusal and never a no-op: a client
        that reads a blank title as "keep the current one" would report a rename
        that never happened.
        """

    # ── folders (R-835) ──────────────────────────────────────────────────────
    #
    # A label's shape on the account is one folder holding one playlist per
    # release year. None of these takes anything away: a move changes where a
    # playlist sits and nothing it holds.

    def add_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Add tracks to a playlist in chunks the provider accepts, skipping members.

        Returns every asked identifier the playlist holds once done. One the
        provider would not add is left out rather than raised: one withdrawn
        track is no reason to add none of a label's year.
        """

    def folders(self) -> dict[str, str]:
        """Every folder at the root of the account's playlists, identifier to name."""

    def folder_playlists(self, folder_id: str) -> dict[str, str]:
        """Every playlist one folder holds, identifier to name."""

    def folder_playlists_dated(self, folder_id: str) -> dict[str, tuple[str, datetime | None]]:
        """Every playlist one folder holds, identifier to its name and when it was made (U216).

        The walk :meth:`folder_playlists` makes; the time is None where the
        account gave none, never guessed.
        """

    def folder_folders(self, folder_id: str) -> dict[str, str]:
        """Every folder one folder holds, identifier to name."""

    def create_folder(self, name: str) -> str:
        """Create one folder at the root of the account's playlists, and return its id.

        Never retried: a create that reached the provider and then timed out
        would be retried into a second folder.
        """

    def move_to_folder(self, playlist_id: str, folder_id: str) -> None:
        """Put one playlist the account holds into one folder. Idempotent."""

    # ── the removals (R-836, U123) ───────────────────────────────────────────

    def track_names(self, playlist_id: str) -> dict[str, tuple[str, str]]:
        """Every track on the playlist, remote identifier to ``(artist, title)``.

        A read, for the gate a person approves a removal at. It writes nothing.
        """

    def playlist_listing(self, playlist_id: str) -> PlaylistListing:
        """Every track on the playlist with its added time and the declared count (U201).

        A read, for the account mirror, which tells a person's edit on the
        account from a track the read could not see. It writes nothing.
        """

    def remove_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Take tracks off one playlist the product created or the author paired.

        REFUSED BEFORE ANY PROVIDER CALL for any other playlist (U130). Every
        occurrence of an asked track comes off; nothing else moves. Returns every
        asked identifier the playlist no longer holds, so a resume asking again
        records one that came off before and takes nothing.
        """

    def order_tracks(
        self,
        playlist_id: str,
        remote_ids: tuple[str, ...],
        *,
        expect: tuple[str, ...] | None = None,
        begun: Callable[[tuple[str, ...], tuple[str, ...]], Callable[[int, int], None] | None]
        | None = None,
        agreed: tuple[str, ...] | None = None,
    ) -> tuple[str, ...]:
        """Put one playlist's tracks in this order, and change nothing else (U130).

        REFUSED BEFORE ANY PROVIDER CALL on :meth:`remove_tracks`'s rule. A track
        the playlist does not hold is not added, one the order does not name
        stays. Returns the order the moves leave, as sent: since U231 they are
        sent with no read back between, and :meth:`settled_order` reads whether
        they landed.

        No track moves until the account's reading agrees with ``expect``, a
        reading the caller took (U220), and holds every track of ``agreed``, an
        order agreed before this command's own writes, in that order (R-1411);
        a reading that never does refuses with nothing moved. ``begun`` is
        called with the reading planned from and the order the moves leave,
        before the first move and not when nothing moves; whatever it raises
        sends nothing. It may answer a recorder, told before each move how many
        may have reached the provider and how many it accepted, and told again
        with the first brought down after a 412 that changed nothing (R-1394);
        whatever the recorder raises sends no further move.
        """

    def settled_order(self, playlist_id: str, *, wait: float = 0.0) -> tuple[str, ...] | None:
        """One judged reading of a playlist an order was sent to, after ``wait`` seconds (U231).

        Reads only. The playlist's tracks in order, or None when the provider's
        reads of it disagree so that no reading can be trusted.
        """

    def remove_playlist(self, playlist_id: str) -> None:
        """Remove one playlist the product created, and nothing else (U123).

        REFUSED BEFORE ANY PROVIDER CALL for a playlist the ledger does not
        record as the product's. One the provider no longer has is already
        removed, so a resume asking again succeeds and removes nothing.
        """

    # ── the account root's removals (U143) ───────────────────────────────────

    def remove_root_playlist(self, playlist_id: str, kind: str) -> None:
        """Remove one root playlist of a kind the gate named, and nothing else.

        ``kind`` is ``kinds.DEBRIS`` or ``kinds.EMPTY``. REFUSED BEFORE ANY
        REMOVAL for any other kind, for a playlist a ledger claims, and for one
        the provider serves as not of that kind: debris carries the source
        system's suffix, an empty one declares no track and no video. One the
        provider no longer has is already removed; one still served after is
        refused.
        """

    def remove_legacy_folder(self, folder_id: str) -> None:
        """Remove one empty legacy year folder at the root, and nothing else.

        REFUSED BEFORE ANY REMOVAL for a folder not at the root, not named as a
        legacy year folder, or holding any playlist or folder. One the root no
        longer lists is already removed; one still listed after is refused.
        """
