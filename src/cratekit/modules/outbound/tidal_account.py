"""The streaming provider's account behind the outbound seam: its writes and their read backs.

**ONE CLASS OVER U62'S SESSION.** :class:`TidalAccount` asks every question of
the client ``acquire.provider_session.session_for`` logs in and holds for the
process. Its reads, the matching, hearts, playlists and folders, are
``tidal_reads.Reads``; this module holds the writes, the reading each is judged
by, and :func:`open_account`.

**THE REMOVALS, BECAUSE THE PROTOCOL DECLARES THEM (R-836).** The suite's scan
of the adapter's files admits one removal call on the client inside each of
four members and nowhere else. ``remove_tracks`` takes tracks off a playlist the
outbound ledger records as the product's or the pairs name, and refuses any
other before a provider call; ``remove_playlist`` (U123) is that rule for a
whole playlist. The account root's ``remove_root_playlist`` and
``remove_legacy_folder`` (U143) remove what the product did not create, each
narrowed to a kind the provider's own answer must confirm before anything is
sent. ``rename_playlist`` writes to something the product did not create too,
and removes nothing. The outbound gates and the confirm digest sit in front of
every write; this module adds no gate and removes none.

**A WRITE CHECKS BEFORE IT WRITES**, so a resumed item that already reached the
provider makes no second write.

**A PROVIDER FAILURE IS THE ITEM'S CAUSE, NOT A DEAD SESSION.** Every call is
translated by ``account.provider_failure``, which asks the not found question
FIRST (the ordering ``acquire.vendored.raise_if_session_dead`` argues) and
raises at item scope, so the job engine fails that item and claims the next.

**ONE RETRY ON A WRITE, NO MORE**, through ``listing.fetch_with_retry``: a
ladder of five would hold a sweep for a minute per item against a provider that
is refusing it. A create is not retried at all: one that reached the provider
and then timed out would be retried into a second playlist nothing records.

Layer: modules.
"""

from __future__ import annotations

import copy
import time
from collections.abc import Callable, Iterable
from functools import reduce
from typing import Any

# Imported at module top rather than deferred, because ``account.bound`` asks
# whether THIS module imports, and the answer has to include the client library.
import tidalapi  # noqa: F401

from cratekit.acquire import catalogue_api, isrc_cache, isrc_screen, listing, provider_session
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import account, kinds, ledger, pairs

# The reads' names the suite and other modules read off this module stay here.
from cratekit.modules.outbound.tidal_reads import (  # noqa: F401
    _ABSENT,
    NOT_FOUND_NAMES,
    TRACK_HOSTS,
    Reads,
    _agrees,
    _album_name,
    _artist_names,
    _identifier,
    _not_found,
    _row_of,
    _shown_artist,
    _streamable,
    track_reference,
)
from cratekit.sync.pair_stopped import front_moves

#: How many times a write or a single lookup is retried after its first attempt.
WRITE_RETRIES = 1

#: How many tracks one add to a playlist carries (R-835): the client's own add
#: asks the provider for a hundred per request.
ADD_CHUNK = 100

#: How many positions one removal request names (R-836): the client's own clear
#: takes fifty a request.
REMOVE_CHUNK = 50

#: U220. How many times a reading that does not agree with what is known of the
#: playlist is taken again, and (U231) how many times one move refused for a
#: stale version tag is sent again.
ORDER_REREADS = 3

#: U220. The pause before each reading taken again, the first before the first;
#: past the last, the last repeats. Since U231 also the pause before a move
#: answered 412 is sent again, counted afresh for each move. Sitting 86
#: measured the provider's reads lagging its moves for minutes, which is why no
#: read back is taken between moves.
ORDER_PAUSES = (1.0, 2.0, 4.0)

#: U220. The status of a write whose version tag is not the playlist's current
#: one, having changed nothing (Sitting 62).
PRECONDITION_FAILED = 412


def _pause(attempt: int) -> float:
    """The pause before the ``attempt``-th reading taken again, from one; the last repeats."""
    return ORDER_PAUSES[min(attempt, len(ORDER_PAUSES)) - 1]


def _stale_tag(exc: BaseException) -> bool:
    """Whether a failure, or one it was raised from or while handling, is the provider's 412 (U220).

    BOTH CHAINS ARE WALKED: the client decodes an error answer's body inside its
    own handler of the HTTP error, so a 412 whose body is not JSON surfaces as
    the decode error with the HTTP error as its context, not its cause.
    """
    seen: list[BaseException] = [exc]
    walked: set[int] = set()
    while seen:
        one = seen.pop()
        if id(one) in walked:
            continue
        walked.add(id(one))
        status = getattr(getattr(one, "response", None), "status_code", None)
        if status == PRECONDITION_FAILED:
            return True
        seen.extend(link for link in (one.__cause__, one.__context__) if link is not None)
    return False


def _to_the_front(before: list[str], remote_ids: Iterable[str]) -> list[str]:
    """The tracks to move to the front, in the order to move them (U220), by ``front_moves``'s rule."""
    return front_moves(before, remote_ids)


def _fronted(order: list[str], one: str) -> list[str]:
    """``order`` with the track ``one``, held once, moved to the front, as a move to the front leaves it (U231)."""
    return [one, *(other for other in order if other != one)]


def _in_agreed_order(reading: list[str], agreed: Iterable[str]) -> bool:
    """Whether every track of ``agreed`` the reading holds stands in ``agreed``'s order (R-1411).

    Read over the tracks both hold, each at its first place: a track only the
    reading holds (one this command added) may stand anywhere, and one only
    ``agreed`` names (one this command took off) is not asked. What the reading
    holds is the membership check's to judge.
    """
    named = {str(one) for one in agreed}
    held = set(reading)
    return [one for one in dict.fromkeys(reading) if one in named] == [
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
    ]


def _count(value: Any) -> bool:
    """Whether a declared count is a whole number and not a flag."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _waited(seconds: float) -> str:
    """Seconds paused, as a refusal names them: ``7`` rather than ``7.0``."""
    return f"{seconds:g}"


def _refused(message: str, step: str, scope: Scope, **detail: str) -> CratekitError:
    """A write or a removal refused with nothing (more) sent, ``outbound-remove-refused``."""
    return refuse(
        "outbound-remove-refused",
        message,
        steps=(step,),
        scope=scope,
        origin=("outbound", "account"),
        detail=detail,
    )


def _root_refusal(what: str, said: str, problem: str, **detail: str) -> CratekitError:
    """A root removal refused with nothing sent, in words and by problem."""
    return _refused(
        f"{said}, so {what} was not removed",
        f"remove {what} by hand in the provider's own player",
        Scope.SOURCE,
        **detail,
        problem=problem,
    )


def _window_lags(
    identifier: str, kept: str, *, readings: int | None = None, waited: float = 0.0
) -> CratekitError:
    """The refusal of a playlist whose window read still disagrees with its unpaged read (U226).

    ``kept`` says what was not done; ``readings`` and the seconds ``waited``,
    when given, are named so an attended sitting reads the lag.
    """
    detail = {"playlist_id": identifier, "problem": "window-lags", "lagged": "yes"}
    said = ""
    if readings is not None:
        detail |= {"readings": str(readings), "waited": _waited(waited)}
        said = f" after {readings} readings and {_waited(waited)} seconds"
    return _refused(
        f"the playlist {identifier} read one way through its pages and another "
        f"through the provider's unpaged read{said}, and the unpaged read is not "
        f"the whole playlist, so it may lag a recent change and which position "
        f"holds which track is not known; {kept}",
        "wait a few minutes for the provider to serve the playlist as it stands, then run it again",
        Scope.RUN,
        **detail,
    )


def _gone(playlist_id: str, doing: str) -> CratekitError:
    """A playlist the provider stopped having in the middle of a write."""
    return account.provider_failure(
        LookupError(f"the provider no longer has the playlist {playlist_id!r}"), doing
    )


def _created(created: Any, what: str, doing: str) -> str:
    """The identifier the provider gave what it just created, which must carry one."""
    identifier = _identifier(created) if created is not _ABSENT else ""
    if not identifier:
        raise account.provider_failure(
            LookupError(f"the provider assigned the new {what} no identifier"), doing
        )
    return identifier


class TidalAccount(Reads):
    """The ``RemoteAccount`` members over one logged in client: the reads of :class:`Reads` and the writes here."""

    def __init__(
        self,
        session: Any,
        *,
        sleep: Callable[[float], None] | None = None,
        cfg: Any = None,
        catalogue: Any = None,
        cache: isrc_cache.Cache | None = None,
    ) -> None:
        self._session = session
        #: Where catalogue lookups go: the app client when the opener built one (U205).
        self._lookups = catalogue if catalogue is not None else session
        #: The codes a batch answered as filed under nothing (U207).
        self._screen = isrc_screen.Screen()
        #: The configuration whose outbound ledger says which playlists the
        #: product made (R-836). None refuses every removal: a ledger that
        #: cannot be named cannot say yes.
        self._cfg = cfg
        # Looked up now rather than bound as a default, so a replaced
        # ``time.sleep`` is honoured.
        self._sleep = sleep or time.sleep
        #: What the provider already answered for an ISRC (U206).
        self._cache = cache if cache is not None else isrc_cache.Cache.from_config(cfg)
        self._hearts: set[str] | None = None
        self._members: dict[str, list[str]] = {}
        #: U255. The object each playlist's membership was read through, so the
        #: adds after it send no open of their own; see :meth:`_held`.
        self._opened: dict[str, Any] = {}
        self._reasons: dict[str, str] = {}
        #: U208. The identities whose last match took one of a tie.
        self._ties: set[str] = set()
        #: U226. Every reading a write or an order was judged by (:meth:`read_backs`).
        self._read_backs: list[dict[str, Any]] = []

    def _call(self, doing: str, fn: Callable[[], Any], *, retries: int = WRITE_RETRIES) -> Any:
        """One provider call, retried ``retries`` times, translated on failure.

        An explicit not found is returned as ``_ABSENT`` from inside the retried
        callable, so a lookup the provider has answered is never asked again.
        """

        def attempt(limit: int, offset: int) -> Any:
            del limit, offset
            try:
                return fn()
            except Exception as exc:
                if _not_found(exc):
                    return _ABSENT
                raise

        try:
            return listing.fetch_with_retry(
                attempt, limit=0, offset=0, max_retries=retries, sleep=self._sleep
            )
        except catalogue_api.AppCredentialsRejected as exc:
            # THE APP'S CREDENTIAL, NOT THE ACCOUNT'S: read as the account's it
            # would be a wait, and the held account the wrong thing to forget.
            raise catalogue_api.rejected(exc, doing) from exc
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            raise account.provider_failure(exc, doing) from exc

    def _read(self, doing: str, fn: Callable[[], list[Any]]) -> list[Any]:
        """One paged read through ``listing``, translated on failure."""
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            raise account.provider_failure(exc, doing) from exc

    # ── hearts ──────────────────────────────────────────────────────────────

    def add_heart(self, remote_id: str) -> None:
        identifier = str(remote_id)
        hearts = self._favorites()
        if identifier in hearts:
            return
        doing = f"heart the track {identifier}"
        accepted = self._call(doing, lambda: self._session.user.favorites.add_track(identifier))
        # The client answers a refused heart with ``False`` rather than a raise,
        # and recording it as hearted would put a heart in the ledger the
        # account does not hold.
        if accepted is False or accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the heart"), doing
            )
        hearts.add(identifier)

    # ── playlists ───────────────────────────────────────────────────────────

    def _playlist(self, playlist_id: str) -> Any:
        """The client's object for one playlist, opened now: two requests.

        THE HOLD IS DROPPED FIRST (U255). A member that writes through the
        object it opened moves the playlist's version tag on, so a held object
        would carry a tag the provider refuses; every open comes through here,
        so dropping it here covers every such member. Only :meth:`_membership`
        and :meth:`_held` hold what they open, after it.
        """
        self._opened.pop(playlist_id, None)
        doing = f"open the playlist {playlist_id}"
        found = self._call(doing, lambda: self._session.playlist(playlist_id))
        if found is _ABSENT or found is None:
            raise account.provider_failure(
                LookupError(f"the provider has no playlist {playlist_id!r}"), doing
            )
        return found

    def _held(self, playlist_id: str) -> Any:
        """The playlist's held object, opened through :meth:`_playlist` only if none is held.

        ONE OPEN FOR A RUN OF ADDS, NOT ONE PER ADD (U255). An open is two GETs
        (the client fetches a ``Playlist``, then the ``UserPlaylist`` its
        factory builds) and the client's add reads the playlist again after its
        POST for the next version tag: opening per add cost 4,003 requests for
        1,000 adds. Through the held object an add costs the POST and that read.

        THE TAG AND THE POSITION COME FROM ONE ANSWER. The client's add sends the
        object's tag and puts the track at the object's length, both set by its
        open or its own read after each write. So :meth:`_membership` reads the
        tracks through a copy, since the client's track read overwrites the tag
        and leaves the length, and nothing is held until the read it was opened
        for has succeeded. A held tag the provider has moved on from is refused
        412 with nothing changed (Sitting 62), and :meth:`add_to_playlist` meets
        that by opening afresh. Held for the life of the adapter, which
        ``account.forget`` drops.
        """
        held = self._opened.get(playlist_id)
        if held is None:
            held = self._playlist(playlist_id)
            self._opened[playlist_id] = held
        return held

    def _membership(self, playlist_id: str) -> list[str]:
        if playlist_id not in self._members:
            opened = self._playlist(playlist_id)
            # THROUGH A COPY, so the opened object keeps the tag and the length
            # its own open read together (U255, see :meth:`_held`).
            tracks = self._listed(playlist_id, copy.copy(opened))
            self._members[playlist_id] = [_identifier(track) for track in tracks]
            self._opened[playlist_id] = opened
        return self._members[playlist_id]

    def create_playlist(self, name: str) -> str:
        """Create one playlist on the account, private, and return its identifier.

        PRIVATE BECAUSE THE SOURCE SYSTEM MAKES EVERY PLAYLIST IT CREATES PRIVATE
        (R-834), set through the client's ``set_playlist_private`` on the object
        the create returned, since the create takes no visibility. A resumed
        item that finds its playlist recorded never reaches this member. The
        identifier is returned even when the private step is refused, see
        :meth:`_make_private`.
        """
        doing = f"create the playlist {name!r}"
        created = self._call(doing, lambda: self._session.user.create_playlist(name, ""), retries=0)
        identifier = _created(created, "playlist", doing)
        self._make_private(created, identifier)
        self._members[identifier] = []
        return identifier

    def _make_private(self, created: Any, identifier: str) -> None:
        """Set a playlist this account just created private. Retried like a write.

        A REFUSAL IS NOT RAISED, AND THAT IS THE WHOLE POINT OF ITS SHAPE. The
        playlist already exists, and raising would keep its identifier out of the
        ledger, so the next item of the export would create another, one public
        playlist per track (driven on 2026-09-02). So the one playlist is
        recorded and the refusal costs its visibility instead (R-849). That
        includes a park from the provider gate: its cooldown is written to the
        shared gate file, so the next gated call refuses at once anyway. It runs
        inside the ledger's lock, so a kill leaves an unrecorded playlist only
        within the create and this step. A client with no such call is passed
        over the same way; a guard in the suite pins the call on the library.
        """
        try:
            self._call(
                f"make the playlist {identifier} private",
                lambda: created.set_playlist_private(),
            )
        except CratekitError:
            return

    def add_to_playlist(self, playlist_id: str, remote_id: str) -> None:
        """Add one track, through the playlist's held object (U255).

        A FAILED ATTEMPT DROPS THE HOLD, AND THE RETRY OPENS AFRESH, inside the
        retried attempt and on its own retry, so a failed open is never sent an
        add; the first open, when nothing is held, is made before the attempts.
        A 412 for a stale tag changed nothing, and an add that landed before its
        answer was lost is skipped by the provider as a duplicate and read back.
        """
        identifier = str(remote_id)
        members = self._membership(playlist_id)
        if identifier in members:
            return
        self._held(playlist_id)
        doing = f"add the track {identifier} to the playlist {playlist_id}"

        def attempt() -> Any:
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
            try:
                return playlist.add([identifier])
            except Exception:
                self._opened.pop(playlist_id, None)
                raise

        added = self._call(doing, attempt)
        if added is _ABSENT:
            raise _gone(playlist_id, doing)
        # THE CLIENT SKIPS A TRACK IT CANNOT FIND AND RAISES NOTHING, answering
        # with what it added. An answer not naming this track is read again from
        # the playlist, on a fresh open (``_membership`` opens through
        # ``_playlist``, which drops the hold): the track may have landed
        # elsewhere, and recording one the playlist does not hold would make a
        # resume skip it.
        if identifier not in {str(item) for item in added or ()}:
            del self._members[playlist_id]
            if identifier not in self._membership(playlist_id):
                raise account.provider_failure(
                    LookupError(f"the provider added nothing for the track {identifier!r}"),
                    doing,
                )
            return
        members.append(identifier)

    def rename_playlist(self, playlist_id: str, name: str) -> None:
        """Retitle the playlist, leaving its membership and description alone.

        RETRIED LIKE A WRITE, NOT LIKE A CREATE: a retitle names the playlist it
        edits and asks for one fixed title, so the retry asks for what the first
        attempt asked for. A playlist the session does not own comes back with
        no editor and is refused, since a rename reported over a playlist still
        carrying its old title tells the source system a sweep finished that it
        will offer again. An empty title is refused here: the client reads a
        falsy title as "keep the current one" and answers True.
        """
        # Not stripped for the write: a caller that asked for a trailing space
        # asked for it.
        wanted = str(name)
        doing = f"rename the playlist {playlist_id} to {wanted!r}"
        if not wanted.strip():
            # NOT ``provider_failure``, whose remedy, resume to retry, cannot work.
            raise refuse(
                "internal-error",
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
                scope=Scope.SOURCE,
                origin=("outbound", "account"),
                detail={"playlist_id": str(playlist_id)},
            )
        playlist = self._playlist(playlist_id)
        retitle = getattr(playlist, "edit", None)
        if not callable(retitle):
            raise account.provider_failure(
                LookupError(
                    f"the provider's playlist {playlist_id!r} cannot be retitled by "
                    f"this account"
                ),
                doing,
            )
        # The client answers a refused edit with ``False`` rather than a raise.
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False or accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the new playlist title"), doing
            )

    def add_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Add every asked track the playlist lacks, :data:`ADD_CHUNK` per request.

        RETRIED LIKE A WRITE: the client asks the provider to skip a track the
        playlist holds, so a retried chunk that landed adds nothing twice. A
        failed attempt drops the object and the retry opens afresh (U270), since
        an add whose POST landed and whose read after it failed leaves the tag
        stale. THE ANSWER IS READ, NOT TRUSTED: one that leaves out an asked
        track has the playlist read again, and a track still absent is left out
        of the return rather than raised.
        """
        wanted = [str(one) for one in dict.fromkeys(remote_ids) if str(one)]
        members = self._membership(playlist_id)
        held = set(members)
        lacking = [one for one in wanted if one not in held]
        if lacking:
            opened: list[Any] = [self._playlist(playlist_id)]
            doing = f"add {len(lacking)} tracks to the playlist {playlist_id}"
            unconfirmed = False

            def attempt(chunk: list[str]) -> Any:
                playlist = opened[0]
                if playlist is None:
                    playlist = opened[0] = self._playlist(playlist_id)
                try:
                    return playlist.add(chunk)
                except Exception:
                    opened[0] = None
                    raise

            for start in range(0, len(lacking), ADD_CHUNK):
                chunk = lacking[start : start + ADD_CHUNK]
                added = self._call(doing, lambda chunk=chunk: attempt(chunk))
                if added is _ABSENT:
                    raise _gone(playlist_id, doing)
                named = {str(item) for item in added or ()}
                members.extend(one for one in chunk if one in named)
                unconfirmed = unconfirmed or any(one not in named for one in chunk)
            if unconfirmed:
                del self._members[playlist_id]
                members = self._membership(playlist_id)
            held = set(members)
        return tuple(one for one in wanted if one in held)

    # ── folders (R-835) ─────────────────────────────────────────────────────

    def create_folder(self, name: str) -> str:
        """Create one root folder and return its identifier. NEVER RETRIED.

        No visibility step: the source system sets none, and the provider keeps
        an account's folders to the account.
        """
        doing = f"create the folder {name!r}"
        created = self._call(doing, lambda: self._session.user.create_folder(name), retries=0)
        return _created(created, "folder", doing)

    def move_to_folder(self, playlist_id: str, folder_id: str) -> None:
        """Put the playlist in the folder. RETRIED LIKE A WRITE, asking for one fixed place.

        The client answers a refused move with ``False`` rather than a raise.
        """
        handle = self._folder(folder_id)
        doing = f"put the playlist {playlist_id} in the folder {folder_id}"
        moved = self._call(
            doing, lambda: handle.move_items_to_folder([str(playlist_id)], str(folder_id))
        )
        if moved is False or moved is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the move into the folder"), doing
            )

    # ── the judged readings (U220, U226) ────────────────────────────────────

    def _noting(self, playlist_id: str, after: str, **more: int) -> dict[str, Any]:
        """A record of one judged reading's readings and wait, kept from its start (U226).

        Appended now and filled as it goes, so a refusal raised anywhere inside
        the reading leaves it recorded as ``"refused"``.
        """
        note: dict[str, Any] = {
            "playlist_id": str(playlist_id),
            "after": after,
            "readings": 0,
            "waited": 0.0,
            "window_lagged": 0,
            "outcome": "refused",
            **more,
        }
        self._read_backs.append(note)
        return note

    def read_backs(self) -> tuple[dict[str, Any], ...]:
        """Every reading this adapter judged a write or an order by, in order (U226).

        Each is ``{"playlist_id", "after", "readings", "waited",
        "window_lagged", "outcome"}``. ``after`` is ``"order"`` for the reading
        an order is planned from, ``"removal positions"`` for a removal's,
        ``"removal"`` for a removal's read back, ``"moves"`` for an order's
        moves (U231), which adds ``moved``, the moves accepted, and ``stale``,
        the 412s sent again, and ``"settle"`` for the reading an order is
        decided by, whose outcome is ``"lags"`` when its window lagged.
        ``window_lagged`` counts readings whose window read disagreed with an
        unpaged read that was not the whole playlist; ``outcome`` is ``"done"``
        or ``"refused"``. Copies, so a caller cannot change what is recorded;
        ``crate sync pair`` carries them as the run's facts.
        """
        return tuple(dict(note) for note in self._read_backs)

    def _paused(self, note: dict[str, Any], seconds: float) -> None:
        """Pause before a reading taken again, and count the wait in its record."""
        self._sleep(seconds)
        note["waited"] += seconds

    def _reading(self, playlist_id: str, playlist: Any) -> tuple[list[str], Any, Any, str]:
        """One reading of an opened playlist: its tracks by position, declared tracks and videos, and how its two reads stood.

        TWO READS, THE WINDOW AND THEN THE UNPAGED ONE (U226). Sitting 84
        measured the window read serving a playlist's old order for minutes
        after a move while the unpaged read served the new one at once.
        :func:`listing.judge_window` reads them against the declared count: the
        unpaged tracks when it is the whole playlist (``WINDOW_UNPAGED``), else
        the window's, agreeing (``WINDOW_AGREES``) or marked ``WINDOW_LAGS``,
        which no caller takes as the playlist as it stands.

        THE UNPAGED READ IS TAKEN LAST, so the version tag the client keeps is
        its own: a window served from before a write carries that write's old
        tag. Past a capped first page it walks on (R-1360), and a walk that
        broke on a page with an older tag is not whole, so it lags. Nothing is
        judged here: each caller judges by its own rule.
        """
        paged = [listing.row_id(track) for track in self._listed(playlist_id, playlist)]
        unpaged = [
            listing.row_id(track)
            for track in self._read(
                f"read the playlist {playlist_id}", lambda: listing.playlist_tracks_unpaged(playlist)
            )
        ]
        declared = getattr(playlist, "num_tracks", None)
        window = listing.judge_window(paged, unpaged, declared)
        return (
            unpaged if window == listing.WINDOW_UNPAGED else paged,
            declared,
            getattr(playlist, "num_videos", None),
            window,
        )

    def _positions(self, playlist_id: str, playlist: Any) -> list[str]:
        """The playlist's tracks by position, refused when a position is unknowable.

        THE PROVIDER LEAVES OUT A TRACK THIS ACCOUNT CANNOT PLAY AND STILL COUNTS
        IT (``listing.playlist_tracks``), so a read short of the declared total
        has positions shifted from the provider's, and a removal by position
        would take the wrong track; a playlist declaring no total cannot be
        checked. The client removes by ITEM position, tracks and videos
        together, so any video, or no video count, refuses too. A window that
        disagrees with the unpaged read (U226) refuses first, ``window-lags``;
        each caller says whether that reading is read again.
        """
        members, declared, videos, window = self._reading(playlist_id, playlist)
        if window == listing.WINDOW_LAGS:
            raise _window_lags(str(playlist_id), "nothing was sent on that reading")
        if (
            not _count(declared)
            or declared != len(members)
            or not _count(videos)
            or videos != 0
        ):
            raise _refused(
                f"the playlist {playlist_id} declares {declared!r} track(s) and "
                f"{videos!r} video(s), and {len(members)} track(s) could be read, so "
                f"which position holds which track is not known and nothing was "
                f"taken off it",
                "take the tracks off by hand in the provider's own player, or "
                "remove the tracks this account cannot play first",
                Scope.SOURCE,
                playlist_id=str(playlist_id),
                problem="positions-unknown",
            )
        self._members[playlist_id] = members
        return members

    def _vouched(self, identifier: str, kept: str) -> None:
        """Refuse, before any provider call, a playlist nothing vouches for changing.

        TWO RECORDS VOUCH, AND ONLY TWO: the outbound ledger, for a playlist the
        product made (R-836), and the playlist pairs, for one of the author's own
        the author marked to stay the same list as a rekordbox playlist (U130).
        ``kept`` says what was not done.
        """
        if self._cfg is not None and (
            ledger.product_made(self._cfg, identifier) or pairs.paired(self._cfg, identifier)
        ):
            return
        raise _refused(
            f"the outbound ledger does not record the playlist {identifier} as "
            f"one this product created and no playlist pair names it, so "
            f"{kept} and the provider was not asked",
            "change the playlist by hand in the provider's own player",
            Scope.SOURCE,
            playlist_id=identifier,
            problem="not-product-made",
        )

    def _settled(
        self,
        identifier: str,
        known: tuple[str, ...] | None,
        *,
        exact: bool = False,
        after: str = "order",
        kept: str = "no track was moved",
        agreed: tuple[str, ...] | None = None,
    ) -> tuple[Any, list[str]]:
        """The playlist opened and read for an order or a removal, once the reading agrees with ``known`` (U220).

        ``known`` is what was last known of the playlist, None for nothing, and
        then the first reading is taken as it is. ``exact`` compares the
        distinct tracks in order, for a reading the caller took; otherwise the
        tracks held, since a provider may put an added track somewhere other
        than where this adapter appended it. ``agreed`` (R-1411) is an order the
        caller agreed on before this command wrote the playlist, which every
        track of it the reading holds must stand in (:func:`_in_agreed_order`).

        A READING THAT LAGS A WRITE IS WHAT THIS IS FOR: Sitting 62's order ran
        straight after six additions, and a reading not yet showing them puts
        every later position wrong. A reading that disagrees, or is short of its
        declared count while something is known, is taken again after each
        pause of :data:`ORDER_PAUSES`, and once :data:`ORDER_REREADS` are spent
        the last refusal is raised with nothing sent; with nothing known a short
        reading refuses at once, as there is no write for it to lag. A window
        that lags its unpaged read (U226) is read again whether or not anything
        is known, and once spent is refused ``window-lags``. ``after`` names the
        record and ``kept`` what a refusal says was not done.
        """

        def agrees(reading: list[str]) -> bool:
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
            if known is None:
                return True
            if exact:
                return list(dict.fromkeys(reading)) == list(dict.fromkeys(known))
            return sorted(reading) == sorted(known)

        note = self._noting(identifier, after)
        last: CratekitError | None = None
        for attempt in range(ORDER_REREADS + 1):
            if attempt:
                self._paused(note, _pause(attempt))
            playlist = self._playlist(identifier)
            note["readings"] += 1
            try:
                reading = self._positions(identifier, playlist)
            except CratekitError as exc:
                problem = (exc.cause.detail or {}).get("problem")
                if problem == "window-lags":
                    note["window_lagged"] += 1
                    last = _window_lags(
                        identifier, kept, readings=note["readings"], waited=note["waited"]
                    )
                    continue
                if known is None or problem != "positions-unknown":
                    raise
                last = exc
                continue
            if agrees(reading):
                note["outcome"] = "done"
                return playlist, reading
            last = _refused(
                f"the playlist {identifier} read {attempt + 1} time(s) does not hold "
                f"what was last known of it, so the reading may lag a write and "
                + kept,
                "check the playlist by hand in the provider's own player, then "
                "run the sync again",
                Scope.RUN,
                playlist_id=identifier,
                problem="read-differs",
            )
        assert last is not None
        raise last

    # ── the order (U220, U231) ──────────────────────────────────────────────

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
        """Put the playlist's tracks in this order, the moves sent with no read back between. NO MOVE IS SENT TWICE.

        The two records :meth:`_vouched` names are asked first, before the
        playlist is opened.

        EVERY MOVE IS TO THE FRONT (U220), the one move whose landing does not
        depend on how the provider counts its target (Sitting 62's provider
        lands a move to the length one short). The longest run at the tail of
        ``remote_ids`` already in order stays, and the tracks before it are
        moved to the front, the last first. A track not asked stays among the
        kept tail.

        PLANNED FROM ONE JUDGED READING, SENT BLIND (U231). The reading must
        agree with ``expect``, else with what this adapter's own writes left,
        and with ``agreed`` (:meth:`_settled`); then every move's position is
        worked out from it and sent with NO READ BACK BETWEEN, since Sitting 86
        measured reads lagging moves for minutes. Whether the order landed is
        read once, later, by the caller (:meth:`settled_order`).

        ``begun`` is called with the reading planned from and the order the
        moves leave, before the first move and not at all when nothing moves;
        whatever it raises sends nothing. It may answer a recorder (R-1394),
        called with ``(sent, landed)`` before each move is sent (and sent
        again), whatever it raises sending no further move. A 412 changed
        nothing (Sitting 62), so the recorder is then told with ``sent`` brought
        back down, before the pause; the adapter pauses, opens the playlist for
        its current tag and sends THE SAME MOVE again, at most
        :data:`ORDER_REREADS` times. Any other failure is raised and nothing is
        sent again, since a move that landed and timed out, sent again, would
        move whatever stands at that position now.

        A track the playlist does not hold, or holds twice, is not moved. The
        return is the order the moves leave, as sent and not read back.
        """
        identifier = str(playlist_id)
        self._vouched(identifier, "no track was moved")
        known = self._members.get(identifier)
        playlist, before = self._settled(
            identifier,
            tuple(expect) if expect is not None else (tuple(known) if known is not None else None),
            exact=expect is not None,
            agreed=tuple(str(one) for one in agreed) if agreed is not None else None,
        )
        moves = _to_the_front(before, remote_ids)
        if not moves:
            return tuple(before)
        end = reduce(_fronted, moves, list(before))
        told = begun(tuple(before), tuple(end)) if begun is not None else None
        doing = f"put the playlist {identifier} in order"
        note = self._noting(identifier, "moves", moved=0, stale=0)
        now = list(before)
        for number, one in enumerate(moves, start=1):
            at = now.index(one)
            stale = 0
            while True:
                if told is not None:
                    told(number, number - 1)
                try:
                    accepted = self._call(
                        doing,
                        lambda at=at, playlist=playlist: playlist.move_by_indices([at], 0),
                        retries=0,
                    )
                    break
                except CratekitError as exc:
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
                        # R-1394. A 412 CHANGED NOTHING: recorded before the
                        # pause, so a stop inside it reads as no move in flight.
                        told(number - 1, number - 1)
                    if stale >= ORDER_REREADS:
                        raise
                    # The same move, never planned afresh, sent once the
                    # playlist is opened for the tag it carries now.
                    stale += 1
                    note["stale"] += 1
                    self._paused(note, _pause(stale))
                    playlist = self._playlist(identifier)
            if accepted is False or accepted is _ABSENT:
                raise account.provider_failure(
                    RuntimeError("the provider did not accept the move"), doing
                )
            now = _fronted(now, one)
            note["moved"] += 1
        note["outcome"] = "done"
        self._members[identifier] = list(now)
        return tuple(now)

    def settled_order(self, playlist_id: str, *, wait: float = 0.0) -> tuple[str, ...] | None:
        """The playlist's order as the provider serves it, read once after ``wait`` seconds (U231).

        The one reading that decides an order :meth:`order_tracks` sent blind.
        The pause is counted in its record, so a caller with other playlists to
        write waits only what is left. One judged reading, never read again: a
        window that lags an unpaged read that is not whole answers None, and the
        caller leaves the order pending. Reads only, so no record is asked.
        """
        identifier = str(playlist_id)
        note = self._noting(identifier, "settle")
        if wait > 0:
            self._paused(note, wait)
        playlist = self._playlist(identifier)
        note["readings"] += 1
        members, _declared, _videos, window = self._reading(identifier, playlist)
        if window == listing.WINDOW_LAGS:
            note["window_lagged"] += 1
            note["outcome"] = "lags"
            return None
        note["outcome"] = "done"
        self._members[identifier] = list(members)
        return tuple(members)

    # ── the removals (R-836, U123) ──────────────────────────────────────────

    def remove_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Take tracks off one playlist the product made or the author paired. NEVER RETRIED.

        The two records :meth:`_vouched` names are asked first, before the
        playlist is opened.

        BY POSITION, BECAUSE THE CLIENT'S REMOVE BY IDENTIFIER READS ONE PAGE.
        The positions are read here through ``listing`` as an order's first
        reading is (:meth:`_settled`), so a window that lags is read again, and
        :meth:`_positions` refuses positions that cannot be trusted. Each
        request carries the version tag of the read it was planned from.

        NOT RETRIED: a removal by position that landed and then timed out, sent
        again, would take off whatever moved into those positions. READ BACK,
        NOT TRUSTED: see :meth:`_removal_read_back`, whose reading is the next
        request's.
        """
        identifier = str(playlist_id)
        wanted = [str(one) for one in dict.fromkeys(remote_ids) if str(one)]
        self._vouched(identifier, "no track was taken off it")
        asked = set(wanted)
        doing = f"take {len(wanted)} tracks off the playlist {identifier}"
        playlist, before = (
            self._settled(
                identifier, None, after="removal positions", kept="nothing was taken off it"
            )
            if wanted
            else (None, [])
        )
        while playlist is not None:
            at = sorted(i for i, one in enumerate(before) if one in asked)[:REMOVE_CHUNK]
            if not at:
                break
            accepted = self._call(
                doing, lambda at=at, playlist=playlist: playlist.remove_by_indices(at), retries=0
            )
            if accepted is False or accepted is _ABSENT:
                raise account.provider_failure(
                    RuntimeError("the provider did not accept the removal"), doing
                )
            gone = set(at)
            expected = [one for i, one in enumerate(before) if i not in gone]
            playlist, before = self._removal_read_back(identifier, before, expected)
        held = set(self._members.get(identifier, ()))
        return tuple(one for one in wanted if one not in held)

    def _removal_read_back(
        self, identifier: str, before: list[str], expected: list[str]
    ) -> tuple[Any, list[str]]:
        """The playlist opened and read after a removal, which must be ``expected`` (R-1308).

        EACH READING IS JUDGED ON ITS TWO HALVES, the tracks read and the
        declared count, each the playlist BEFORE the removal or AFTER it, with
        no video declared. Both after is done, and only that reading is
        remembered and carried as the next request's positions and tag. Either
        half still before, the other before or after, is a read that LAGS the
        removal (as U220 measured for a move): it is read again after each pause
        of :data:`ORDER_PAUSES`, at most :data:`ORDER_REREADS` times, then
        refused saying the removal may have landed. Anything else, a wrong track
        gone or a count that is neither, is refused at once. The removal is
        never sent again from here.
        """
        note = self._noting(identifier, "removal")
        lagged = False
        tracks: str | None = None
        counted: str | None = None
        for attempt in range(ORDER_REREADS + 1):
            if attempt:
                self._paused(note, _pause(attempt))
            playlist = self._playlist(identifier)
            note["readings"] += 1
            reading, declared, videos, window = self._reading(identifier, playlist)
            # U226. A window that disagrees with an unpaged read not whole says
            # nothing of which tracks are on it now: that half is a lag.
            if window == listing.WINDOW_LAGS:
                note["window_lagged"] += 1
                tracks = "window"
            else:
                tracks = (
                    "before" if reading == before else "after" if reading == expected else None
                )
            counted = (
                None
                if not _count(declared) or not _count(videos) or videos != 0
                else "before"
                if declared == len(before)
                else "after"
                if declared == len(expected)
                else None
            )
            if tracks == counted == "after":
                self._members[identifier] = reading
                note["outcome"] = "done"
                return playlist, reading
            lagged = tracks is not None and counted is not None
            if not lagged:
                break
        # WHAT THE PLAYLIST HOLDS IS NOT KNOWN NOW, so it is forgotten.
        self._members.pop(identifier, None)
        shown = {
            ("before", "before"): "still read as it was before a removal",
            ("before", "after"): (
                "read after a removal with its declared count changed and its "
                "tracks still as they were before"
            ),
            ("after", "before"): (
                "read after a removal with its tracks changed as asked and its "
                "declared count still as it was before"
            ),
            ("window", "before"): (
                "read after a removal with its pages otherwise than the provider's "
                "unpaged read and its declared count still as it was before"
            ),
            ("window", "after"): (
                "read after a removal with its pages otherwise than the provider's "
                "unpaged read and its declared count changed"
            ),
        }
        # NOT ``provider_failure``, whose remedy is to run it again: a playlist
        # that did not change as asked may have lost the wrong track.
        raise _refused(
            (
                f"the playlist {identifier} {shown[(tracks, counted)]} after "
                f"{note['readings']} readings and {_waited(note['waited'])} seconds, "
                f"so the removal may have landed with the read lagging it; nothing "
                f"more was sent"
            )
            if lagged
            else (
                f"the playlist {identifier} read back after a removal is not "
                f"what it held with the asked positions gone, so a track other "
                f"than the asked ones may have come off, and nothing more was sent"
            ),
            "check the playlist by hand in the provider's own player "
            "before running anything on it again",
            Scope.RUN,
            playlist_id=identifier,
            problem="read-back-differs",
            lagged="yes" if lagged else "no",
            readings=str(note["readings"]),
            waited=_waited(note["waited"]),
        )

    def _served(self, doing: str, identifier: str) -> Any:
        """The playlist the provider serves now, or None, forgotten here, when it has none."""
        found = self._call(doing, lambda: self._session.playlist(identifier))
        if found is _ABSENT or found is None:
            self._members.pop(identifier, None)
            return None
        return found

    def _sent_and_read_back(
        self, doing: str, send: Callable[[], Any], identifier: str, named: str
    ) -> None:
        """Send a playlist's delete, NEVER RETRIED, and read back that it is gone.

        A delete that timed out is read back rather than sent again, and one
        the provider still serves is refused, so a removal that did not happen
        is never reported as one that did.
        """
        if self._call(doing, send, retries=0) is False:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the removal"), doing
            )
        if self._served(doing, identifier) is not None:
            raise _refused(
                f"{named} is still served by the provider after it was asked to "
                f"remove it, so it was not removed",
                "check the playlist by hand in the provider's own player",
                Scope.RUN,
                playlist_id=identifier,
                problem="read-back-differs",
            )
        self._members.pop(identifier, None)

    def remove_playlist(self, playlist_id: str) -> None:
        """Remove one playlist the product made (U123). NEVER RETRIED, read back.

        THE LEDGER IS ASKED FIRST, before any provider call. A playlist the
        provider no longer has is already removed, so a resume that asks again
        after a removal landed removes nothing.
        """
        identifier = str(playlist_id)
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
            raise _refused(
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
                f"was not asked",
                "remove the playlist by hand in the provider's own player",
                Scope.SOURCE,
                playlist_id=identifier,
                problem="not-product-made",
            )
        doing = f"remove the playlist {identifier}"
        found = self._served(doing, identifier)
        if found is None:
            return
        # THE CLIENT HANDS BACK A PLAYLIST IT OWNS WITH A DELETE AND ANY OTHER
        # WITHOUT ONE; read as an attribute, so the suite's removal scan sees it.
        remove = found.delete if hasattr(found, "delete") else None
        if not callable(remove):
            raise _refused(
                f"the provider does not serve the playlist {identifier} as one this "
                f"account owns, so it was not removed",
                "remove the playlist by hand in the provider's own player",
                Scope.SOURCE,
                playlist_id=identifier,
                problem="not-owned",
            )
        self._sent_and_read_back(doing, remove, identifier, f"the playlist {identifier}")

    # ── the account root's removals (U143) ──────────────────────────────────

    def _claimed(self, identifier: str) -> bool:
        """Whether any ledger record names the playlist, made or adopted."""
        cfg = self._cfg
        return (
            ledger.product_made(cfg, identifier)
            or identifier in ledger.label_playlist_ids(cfg)
            or identifier in ledger.set_playlist_ids(cfg)
            or identifier in ledger.exported_playlist_ids(cfg)
        )

    def remove_root_playlist(self, playlist_id: str, kind: str) -> None:
        """Remove one root playlist of the named kind (U143). NEVER RETRIED, read back.

        THE KIND IS ASKED FIRST, then the ledger: a kind other than debris or
        empty, and a playlist any ledger record names, are refused with no
        provider call (the product's own are :meth:`remove_playlist`'s). THE
        PROVIDER'S OWN ANSWER MUST BE OF THE KIND: debris must carry the label
        batch's suffix, case exactly, and an empty one must declare no track and
        no video, both readable; else it is refused before the delete. Where it
        sits and whether debris's tracks are still filed the caller reads again
        before it asks (``organize.root.apply``).
        """
        from cratekit.sync.playlists import is_library_debris

        identifier = str(playlist_id)
        what = f"the playlist {identifier}"
        if kind not in kinds.ROOT_REMOVALS:
            raise _root_refusal(
                what,
                f"{kind!r} is not a kind of root playlist this account removes",
                "not-a-root-kind",
                playlist_id=identifier,
            )
        if self._cfg is None or self._claimed(identifier):
            raise _root_refusal(
                what,
                "a ledger record names it, or no ledger could be read, and the "
                "product's own playlists are not removed as root debris or empties",
                "ledger-claimed",
                playlist_id=identifier,
            )
        doing = f"remove the {kind} playlist {identifier}"
        found = self._served(doing, identifier)
        if found is None:
            return
        name = str(getattr(found, "name", "") or "")
        tracks = getattr(found, "num_tracks", None)
        videos = getattr(found, "num_videos", None)
        if kind == kinds.DEBRIS:
            served = is_library_debris(name)
        else:
            served = _count(tracks) and _count(videos) and tracks == 0 and videos == 0
        if not served:
            raise _root_refusal(
                what,
                f"the provider serves it as {name!r} with {tracks!r} track(s) and "
                f"{videos!r} video(s), which is not {kind}",
                "not-this-kind",
                playlist_id=identifier,
                kind=kind,
            )
        remove = found.delete if hasattr(found, "delete") else None
        if not callable(remove):
            raise _root_refusal(
                what,
                "the provider does not serve it as one this account owns",
                "not-owned",
                playlist_id=identifier,
            )
        self._sent_and_read_back(doing, remove, identifier, f"the {kind} playlist {identifier}")

    def remove_legacy_folder(self, folder_id: str) -> None:
        """Remove one empty legacy year folder at the root (U143). NEVER RETRIED, read back.

        READ FIRST: the root's folders must list it under a legacy year folder's
        name, holding no playlist and no folder; one the root no longer lists is
        already removed. Removed through the collection's own removal, which
        names the folder by identifier, rather than the client's folder object,
        whose lookup reads one page of fifty root folders (R-835).
        """
        identifier = str(folder_id)
        what = f"the folder {identifier}"
        root = self.folders()
        if identifier not in root:
            return
        name = root[identifier]
        if not kinds.legacy_year(name):
            raise _root_refusal(
                what,
                f"its name {name!r} is not a legacy year folder's",
                "not-a-legacy-folder",
                folder_id=identifier,
            )
        held = len(self.folder_playlists(identifier)) + len(self.folder_folders(identifier))
        if held:
            raise _root_refusal(
                what,
                f"{name!r} still holds {held} playlist(s) or folder(s)",
                "not-empty",
                folder_id=identifier,
            )
        doing = f"remove the folder {identifier}"
        # THE CLIENT IS REACHED INSIDE THE CALL, so a session with no user is
        # translated like any failure. A NOT FOUND ANSWER IS READ BACK: the
        # folder may have gone since the read.
        accepted = self._call(
            doing,
            lambda: self._session.user.favorites.remove_folders_playlists(
                [identifier], type="folder"
            ),
            retries=0,
        )
        if accepted is False:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the folder removal"), doing
            )
        if identifier in self.folders():
            raise _refused(
                f"the folder {identifier} is still listed at the root after it was "
                f"asked to remove it, so it was not removed",
                "check the folder by hand in the provider's own player",
                Scope.RUN,
                folder_id=identifier,
                problem="read-back-differs",
            )


def open_account(cfg: Any = None) -> TidalAccount:
    """A fresh account over the process's logged in client, from the stored session.

    The client is the one :func:`provider_session.session_for` holds for the
    process (U261), shared with the label catalogue, so a verb that opens both
    logs in once. ``cfg`` is the FROZEN configuration the pacing gate reads its
    interval and cooldown off (R-705); None means the gate's own defaults.
    """
    held = provider_session.session_for(cfg)
    return TidalAccount(held.client, cfg=cfg, catalogue=held.app)


__all__ = [
    "ADD_CHUNK", "NOT_FOUND_NAMES", "REMOVE_CHUNK", "TRACK_HOSTS", "WRITE_RETRIES",
    "TidalAccount", "open_account", "track_reference",
]
