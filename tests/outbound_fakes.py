"""One stand-in for a streaming account, shared by every suite that needs one.

**WHY IT MOVED HERE IN U51.** ``tests/modules/test_outbound.py`` owned this class
while the engines had no caller in ``src``, so there was one consumer and no
reason to share it. Binding the two outbound handlers created three more, and
three private copies of a provider stand-in is three descriptions of one
protocol, drifting apart at whatever rate each suite happens to need. One copy
means a method the real ``RemoteAccount`` protocol grows is missing in one place
rather than absent in three.

**IT REFUSES ANYTHING OUTSIDE THE PROTOCOL, AND THAT IS A GUARD RATHER THAN
TIDINESS.** ``modules/outbound/service.RemoteAccount`` declares no un-heart and
no folder delete but an empty legacy year folder's, and the removals it does
declare are narrow: ``remove_tracks`` (R-836) and ``remove_playlist`` (U123),
each of a playlist the product made, and the account root's debris and empties
(U143), each of a kind a gate named.
:class:`StrictAccount` raises on any other attribute, so a worker that reached
for one fails the suite instead of failing silently against a fake permissive
enough to answer.

Not a test module: pytest does not collect it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from tests.modules.test_reports import _close, _collection, _document, _folder, _playlist

#: Every method the ``RemoteAccount`` protocol declares. Derived once here rather
#: than remembered at each assertion site.
PROTOCOL_METHODS = frozenset(
    {
        "match_track",
        "unmatched_reason",
        # U207. Reads only: which codes a plan will ask the provider files nothing under.
        "screen_isrcs",
        # U208. Whether the last match broke a tie between agreeing releases.
        "tie_broken",
        "add_heart",
        "has_heart",
        "create_playlist",
        "add_to_playlist",
        "playlist_tracks",
        "rename_playlist",
        # R-835. The folder members, none of which takes anything away.
        "add_tracks",
        "folders",
        "folder_playlists",
        # U216. The same read with when the account says each playlist was made.
        "folder_playlists_dated",
        "folder_folders",
        "create_folder",
        "move_to_folder",
        # R-836. A read that names a playlist's tracks, and the one removal.
        "track_names",
        "remove_tracks",
        # U201. The same read with each track's added time and the declared count.
        "playlist_listing",
        # U123. The one playlist removal, of a dated playlist heard.
        "remove_playlist",
        # U130. The order of a playlist the product made or the author paired.
        "order_tracks",
        # U143. The account root's removals, each of a kind the gate named.
        "remove_root_playlist",
        "remove_legacy_folder",
    }
)


class FakeAccount:
    """A streaming account that records every mutation and never talks to a network.

    ``fail_after`` makes the Nth write raise, which is how a partially completed
    outbound run is driven. ``fail_on`` is the finer instrument: it names the
    remote identifiers whose write must fail, so a multi-item job can be made to
    fail on exactly one item and the resume can be asked whether it redid that
    one and only that one.
    """

    def __init__(
        self,
        catalog: dict[str, str] | None = None,
        *,
        fail_after: int | None = None,
        fail_on: frozenset[str] | set[str] | None = None,
        hearts: set[str] | None = None,
        transient: bool = False,
        provider_error: bool = False,
    ) -> None:
        self.catalog = dict(catalog or {})
        self.hearts: set[str] = set(hearts or ())
        self.playlists: dict[str, list[str]] = {}
        self.created: list[str] = []
        self.added: list[tuple[str, str]] = []
        self.hearted: list[str] = []
        self.removed: list[str] = []
        #: Every retitle, in order, as ``(playlist_id, new_name)``. A list rather
        #: than a mapping so a second rename of one playlist is visible.
        self.renamed: list[tuple[str, str]] = []
        #: What each playlist is called now, for the retitle to change.
        self.titles: dict[str, str] = {}
        self.fail_after = fail_after
        self.fail_on = frozenset(fail_on or ())
        #: How a failed write fails. ``False`` raises ``RuntimeError``, which
        #: the item boundary records as ``internal-error`` and NOT retryable, the
        #: shape a defect takes. ``True`` raises the provider's own transient
        #: refusal, retryable, the shape a dropped connection takes. A test that
        #: re-arms the job afterwards needs the second, because ``jobs.retry``
        #: refuses a job whose recorded failures are permanent (R-390).
        self.transient = transient
        #: When set, a failed write raises a ``CratekitError`` the way the real
        #: account's ``provider_failure`` does, so a mid pass refusal can be
        #: asserted through the path that rebuilds the cause and merges totals.
        self.provider_error = provider_error
        self._writes = 0
        #: U220. Every order asked, as ``(playlist, expect)``.
        self.expected: list[tuple[str, tuple[str, ...] | None]] = []
        #: Every match asked, as the keyword arguments it was asked with, so a
        #: test can say what an engine handed the account to choose by.
        self.matches: list[dict[str, str]] = []
        #: The identities a match was asked for with ``agree`` (R-879).
        self.agreeing: list[str] = []
        #: The identities a match was asked for with ``any_agreeing`` (R-1032).
        self.any_agreeing: list[str] = []
        #: What this account says about a row it does not match, by identity.
        self.reasons: dict[str, str] = {}
        #: Every ``screen_isrcs`` call, its codes in the order given (U207).
        self.screened: list[tuple[str, ...]] = []
        #: The identities whose match this account says broke a tie (U208).
        self.ties: set[str] = set()
        #: When the account says each playlist was made, for ``folder_playlists_dated``
        #: (U216); a playlist absent here reads as made at no known time.
        self.made_at: dict[str, Any] = {}
        #: Each ``(playlist, track)``'s added time for ``playlist_listing`` (U201).
        self.added_at: dict[tuple[str, str], str] = {}
        #: Tracks a playlist holds that its listing leaves out, by playlist.
        self.hidden: dict[str, tuple[str, ...]] = {}
        #: Playlists whose listing declares no count.
        self.undeclared: set[str] = set()
        #: R-835. Folders, identifier to name, which folder each playlist
        #: sits in, and which folder (if any) each folder sits in. A
        #: playlist or folder with no parent sits at the root.
        self.folder_names: dict[str, str] = {}
        self.folder_parent: dict[str, str] = {}
        self.placed: dict[str, str] = {}
        self.folders_created: list[str] = []
        #: Every move, in order, as ``(playlist_id, folder_id)``.
        self.moves: list[tuple[str, str]] = []
        #: Every chunked add, in order, as ``(playlist_id, ids)``.
        self.chunks: list[tuple[str, tuple[str, ...]]] = []
        #: Tracks the provider will not add, as the client skips them.
        self.unaddable: set[str] = set()
        #: Every playlist created private, which is what the adapter does.
        self.private: set[str] = set()
        #: R-836. What each remote track is called, ``(artist, title)``, and
        #: every removal asked, in order, as ``(playlist_id, ids)``.
        self.names: dict[str, tuple[str, str]] = {}
        self.taken: list[tuple[str, tuple[str, ...]]] = []
        #: Every order asked for, as ``(playlist, remote_ids)`` (U130).
        self.ordered: list[tuple[str, tuple[str, ...]]] = []
        #: U123. Every playlist removed, in order, and what it held.
        self.deleted: list[tuple[str, tuple[str, ...]]] = []
        #: U143. Every root playlist removed, as ``(playlist_id, kind)``, and
        #: every legacy folder removed, in order.
        self.root_removed: list[tuple[str, str]] = []
        self.folders_removed: list[str] = []

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
        self.matches.append(
            {
                "identity": identity,
                "isrc": isrc,
                "title": title,
                "artist": artist,
                "album": album,
            }
        )
        if agree:
            self.agreeing.append(identity)
        if any_agreeing:
            self.any_agreeing.append(identity)
        return self.catalog.get(identity)

    def unmatched_reason(self, identity: str) -> str:
        return self.reasons.get(identity, "")

    def screen_isrcs(self, codes) -> int:
        """Recorded, and asks nothing: this account has no batch form (U207)."""
        self.screened.append(tuple(codes))
        return 0

    def tie_broken(self, identity: str) -> bool:
        return identity in self.ties and bool(self.catalog.get(identity))

    def add_heart(self, remote_id: str) -> None:
        self._bump(remote_id)
        self.hearts.add(remote_id)
        self.hearted.append(remote_id)

    def has_heart(self, remote_id: str) -> bool:
        return remote_id in self.hearts

    def create_playlist(self, name: str) -> str:
        self._bump(name)
        remote_id = f"pl-{len(self.created) + 1}"
        self.playlists[remote_id] = []
        self.titles[remote_id] = name
        self.created.append(name)
        self.private.add(remote_id)
        return remote_id

    def add_to_playlist(self, playlist_id: str, remote_id: str) -> None:
        self._bump(remote_id)
        self.playlists.setdefault(playlist_id, []).append(remote_id)
        self.added.append((playlist_id, remote_id))

    def playlist_tracks(self, playlist_id: str) -> tuple[str, ...]:
        return tuple(self.playlists.get(playlist_id, ()))

    def rename_playlist(self, playlist_id: str, name: str) -> None:
        """Retitle, keyed by identifier. Counts as a write, so ``fail_on`` bites.

        The subject handed to :meth:`_bump` is the PLAYLIST identifier and not
        the new title, because a caller asking to fail one rename knows which
        playlist it means and not what the run decided to call it.
        """
        self._bump(playlist_id)
        self.titles[playlist_id] = name
        self.renamed.append((playlist_id, name))

    def add_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Chunked add. One write per call, so ``fail_on`` names the playlist."""
        self._bump(playlist_id)
        members = self.playlists.setdefault(playlist_id, [])
        fresh = tuple(
            one for one in dict.fromkeys(remote_ids)
            if one not in members and one not in self.unaddable
        )
        members.extend(fresh)
        self.chunks.append((playlist_id, fresh))
        self.added.extend((playlist_id, one) for one in fresh)
        return tuple(one for one in remote_ids if one in members)

    def folders(self) -> dict[str, str]:
        return {
            folder_id: name
            for folder_id, name in self.folder_names.items()
            if folder_id not in self.folder_parent
        }

    def folder_playlists(self, folder_id: str) -> dict[str, str]:
        return {
            playlist_id: self.titles.get(playlist_id, "")
            for playlist_id, folder in self.placed.items()
            if folder == folder_id
        }

    def folder_playlists_dated(self, folder_id: str) -> dict[str, tuple[str, Any]]:
        """U216. Each playlist's title and when it was made, as ``made_at`` says, else None."""
        return {
            playlist_id: (title, self.made_at.get(playlist_id))
            for playlist_id, title in self.folder_playlists(folder_id).items()
        }

    def folder_folders(self, folder_id: str) -> dict[str, str]:
        return {
            nested: self.folder_names[nested]
            for nested, parent in self.folder_parent.items()
            if parent == folder_id
        }

    def create_folder(self, name: str) -> str:
        self._bump(name)
        folder_id = f"folder-{len(self.folders_created) + 1}"
        self.folder_names[folder_id] = name
        self.folders_created.append(name)
        return folder_id

    def nest_folder(self, name: str, parent_id: str) -> str:
        """A folder under another. Test helper, not a protocol write."""
        folder_id = f"nested-{len(self.folder_parent) + 1}"
        self.folder_names[folder_id] = name
        self.folder_parent[folder_id] = parent_id
        return folder_id

    def move_to_folder(self, playlist_id: str, folder_id: str) -> None:
        self._bump(playlist_id)
        self.placed[playlist_id] = folder_id
        self.moves.append((playlist_id, folder_id))

    def track_names(self, playlist_id: str) -> dict[str, tuple[str, str]]:
        return {
            one: self.names.get(one, (f"Artist of {one}", f"Title of {one}"))
            for one in self.playlists.get(playlist_id, ())
        }

    def playlist_listing(self, playlist_id: str):
        """``track_names`` with ``added_at``'s times and a declared count (U201).

        ``hidden`` names tracks the provider counts and does not list, by
        playlist, so a short read is drivable; ``undeclared`` names playlists
        that declare no count.
        """
        from cratekit.modules.outbound.service import PlaylistListing

        held = list(self.playlists.get(playlist_id, ()))
        names = self.track_names(playlist_id)
        hidden = self.hidden.get(playlist_id, ())
        for one in hidden:
            names.pop(one, None)
        listed = [one for one in held if one not in hidden]
        return PlaylistListing(
            names=names,
            added={
                one: self.added_at[(playlist_id, one)]
                for one in names
                if (playlist_id, one) in self.added_at
            },
            listed=len(listed),
            declared=None if playlist_id in self.undeclared else len(held),
        )

    def remove_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Take every occurrence off. One write per call, so ``fail_on`` names the playlist."""
        self._bump(playlist_id)
        asked = set(remote_ids)
        members = self.playlists.setdefault(playlist_id, [])
        members[:] = [one for one in members if one not in asked]
        self.taken.append((playlist_id, tuple(remote_ids)))
        return tuple(one for one in remote_ids if one not in members)

    def order_tracks(
        self,
        playlist_id: str,
        remote_ids: tuple[str, ...],
        *,
        expect: tuple[str, ...] | None = None,
    ) -> tuple[str, ...]:
        """Put the asked tracks it holds once in the asked order, the rest after (U220). One write.

        ``expect`` is recorded in :attr:`expected`, by playlist (U220).
        """
        self.expected.append((playlist_id, None if expect is None else tuple(expect)))
        self._bump(playlist_id)
        members = self.playlists.setdefault(playlist_id, [])
        once = {one for one in members if members.count(one) == 1}
        asked = [one for one in dict.fromkeys(remote_ids) if one in once]
        members[:] = asked + [one for one in members if one not in set(asked)]
        self.ordered.append((playlist_id, tuple(remote_ids)))
        return tuple(members)

    def remove_playlist(self, playlist_id: str) -> None:
        """Remove the playlist and its place. One write, so ``fail_on`` names it.

        A playlist this account does not hold is already removed, as the
        adapter answers it, and is recorded with nothing in it.
        """
        self._bump(playlist_id)
        held = tuple(self.playlists.pop(playlist_id, ()))
        self.titles.pop(playlist_id, None)
        self.placed.pop(playlist_id, None)
        self.deleted.append((playlist_id, held))

    def remove_root_playlist(self, playlist_id: str, kind: str) -> None:
        """Remove a root playlist of the named kind. One write, so ``fail_on`` names it."""
        from cratekit.modules.outbound import kinds

        assert kind in kinds.ROOT_REMOVALS, kind
        self._bump(playlist_id)
        self.playlists.pop(playlist_id, None)
        self.titles.pop(playlist_id, None)
        self.placed.pop(playlist_id, None)
        self.root_removed.append((playlist_id, kind))

    def remove_legacy_folder(self, folder_id: str) -> None:
        """Remove an empty root folder; one holding anything is refused, as the adapter does."""
        if folder_id not in self.folders():
            return
        if self.folder_playlists(folder_id) or self.folder_folders(folder_id):
            raise refuse(
                "outbound-remove-refused",
                f"the folder {folder_id} still holds something, so it was not removed",
                origin=("test", "outbound_fakes"),
                detail={"folder_id": folder_id, "problem": "not-empty"},
            )
        self._bump(folder_id)
        del self.folder_names[folder_id]
        self.folders_removed.append(folder_id)

    def _bump(self, subject: str = "") -> None:
        self._writes += 1
        if subject and subject in self.fail_on:
            self._fail(f"interrupted outbound write for {subject}")
        if self.fail_after is not None and self._writes > self.fail_after:
            self._fail("interrupted outbound write")

    def _fail(self, message: str) -> None:
        if self.transient or self.provider_error:
            raise refuse(
                "unavailable-transient",
                message,
                remedy=Remedy.RETRY_LATER,
                retryable=True,
                origin=("test", "outbound_fakes"),
            )
        raise RuntimeError(message)


class StrictAccount(FakeAccount):
    """A :class:`FakeAccount` that raises on any attribute outside the protocol.

    The add-only property cannot be asserted by watching for a remove that never
    happens: an absence proves nothing about the mechanism, only about this
    input. This raises instead, so the assertion is that no code path in the
    shell or the engine can even NAME a remove.

    ``rename_playlist`` is admitted and that is deliberate (R-358). It is
    inherited from :class:`FakeAccount` as a real method, so ``__getattr__``
    never fires for it, and the protocol declares it. Widening the guard is one
    line in :data:`PROTOCOL_METHODS`, and the line is what makes the widening
    visible in the diff rather than silent in a fake permissive enough to answer.
    """

    def __getattr__(self, name: str):
        raise AssertionError(
            f"the outbound path reached {name!r}, which the RemoteAccount "
            f"protocol does not declare. It declares only "
            f"{', '.join(sorted(PROTOCOL_METHODS))}"
        )


class FakeColors:
    """Pink colour store with no clear path. Add-only, like the protocol it stands in for."""

    def __init__(self) -> None:
        self.pink: set[str] = set()
        self.cleared: list[str] = []

    def color_pink(self, row_id: str) -> None:
        self.pink.add(row_id)

    def is_pink(self, row_id: str) -> bool:
        return row_id in self.pink


def account_factory(account: FakeAccount) -> Callable[[object], FakeAccount]:
    """A stand-in for ``modules.outbound.account.resolve`` that hands back ``account``.

    Takes the configuration and ignores it, matching the real signature, so a
    monkeypatch of the module attribute is a drop-in rather than a shape a caller
    has to be written around.
    """

    def resolve(cfg: object) -> FakeAccount:
        del cfg
        return account

    return resolve


#: The playlist an outbound fixture exports unless it says otherwise.
CRATE = "crate-export"

#: The favourites playlist name the shipped default names. Spelled here so a
#: fixture that stopped matching the default fails rather than silently drifting.
FAVORITES = "All Favorites"


def export_document(
    *,
    crate: Sequence[int] = (1, 2, 3),
    favorites: Sequence[int] = (1, 2),
    tracks: int = 3,
    extra_children: Sequence[str] = (),
    root_count: int | None = None,
    locations: Mapping[int, str] | None = None,
    crate_name: str | None = CRATE,
) -> bytes:
    """A collection export carrying a crate and a favourites playlist.

    ONE DOCUMENT FOR BOTH VERBS, because both read the same kind of file and a
    fixture per verb is two descriptions of one format. The track identifiers are
    integers here and strings everywhere downstream, which is the export format's
    own shape rather than a convenience: ``TrackID`` is an attribute and every
    reader in this product treats it as text.

    ``extra_children`` takes already-rendered nodes so a test can add the second
    playlist that makes a bare name ambiguous, or a folder that makes a name
    resolve to nothing.

    ``locations`` replaces a row's ``Location`` by index, so a test can point a
    row at a real audio file whose tag the outbound source reads (R-355). A row
    left out keeps a location naming no file, which reads as no ISRC.

    ``crate_name`` renames the top level crate, and none leaves it out, which
    with a nested one in ``extra_children`` is the crate dragged into a folder
    (R-229). Both are what rekordbox shows after a reorganisation: the same
    tracks under a path nothing was recorded against.
    """
    rows = [
        (
            index,
            f"08A - 124 - Track {index}",
            f"Artist {index}",
            (locations or {}).get(index, f"file://localhost/library/{index}.flac"),
        )
        for index in range(1, tracks + 1)
    ]
    crates = _playlist(crate_name, list(crate), 1) if crate_name is not None else []
    children = [
        *crates,
        *_playlist(FAVORITES, list(favorites), 1),
        *extra_children,
    ]
    fixed = 2 if crate_name is not None else 1
    counted = root_count if root_count is not None else fixed + len(extra_children)
    return _document(
        collection=_collection(rows), root_children=children, root_count=counted
    )


def write_export(directory: Path, **kwargs) -> Path:
    """Put one export document on disk under ``directory`` and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "collection.xml"
    path.write_bytes(export_document(**kwargs))
    return path


def nested_playlist(folder: str, name: str, track_ids: Sequence[int]) -> list[str]:
    """A playlist one folder deep, for the ambiguity and full-path cases."""
    return [_folder(folder, 1, 1), *_playlist(name, list(track_ids), 2), _close(1)]


def folder_only(name: str) -> list[str]:
    """A folder with nothing under it, which is the live library's ``Favorites`` shape."""
    return [_folder(name, 0, 1), _close(1)]


__all__ = [
    "CRATE",
    "FAVORITES",
    "PROTOCOL_METHODS",
    "FakeAccount",
    "FakeColors",
    "StrictAccount",
    "account_factory",
    "export_document",
    "folder_only",
    "nested_playlist",
    "write_export",
]
