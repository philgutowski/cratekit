"""One stand-in for a streaming account, shared by every suite that needs one.

**WHY IT MOVED HERE IN U51.** ``tests/modules/test_outbound.py`` owned this class
while the engines had no caller in ``src``, so there was one consumer and no
reason to share it. Binding the two outbound handlers created three more, and
three private copies of a provider stand-in is three descriptions of one
protocol, drifting apart at whatever rate each suite happens to need. One copy
means a method the real ``RemoteAccount`` protocol grows is missing in one place
rather than absent in three.

**IT REFUSES ANYTHING OUTSIDE THE PROTOCOL, AND THAT IS A GUARD RATHER THAN
TIDINESS.** ``modules/outbound/service.RemoteAccount`` declares no remove, no
un-heart, and no playlist delete, and the product's add-only promise (R36) rests
on that. :class:`StrictAccount` raises on any other attribute, so a worker that
reached for one fails the suite instead of failing silently against a fake
permissive enough to answer.

Not a test module: pytest does not collect it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Mapping, Sequence

from tests.modules.test_reports import _close, _collection, _document, _folder, _playlist

#: Every method the ``RemoteAccount`` protocol declares. Derived once here rather
#: than remembered at each assertion site.
PROTOCOL_METHODS = frozenset(
    {
        "match_track",
        "add_heart",
        "has_heart",
        "create_playlist",
        "add_to_playlist",
        "playlist_tracks",
        "rename_playlist",
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
        self._writes = 0

    def match_track(self, *, identity: str, isrc: str = "") -> str | None:
        del isrc
        return self.catalog.get(identity)

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

    def _bump(self, subject: str = "") -> None:
        self._writes += 1
        if subject and subject in self.fail_on:
            raise RuntimeError(f"interrupted outbound write for {subject}")
        if self.fail_after is not None and self._writes > self.fail_after:
            raise RuntimeError("interrupted outbound write")


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
    children = [
        *_playlist(CRATE, list(crate), 1),
        *_playlist(FAVORITES, list(favorites), 1),
        *extra_children,
    ]
    counted = root_count if root_count is not None else 2 + len(extra_children)
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
