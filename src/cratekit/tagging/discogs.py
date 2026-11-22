"""Discogs, asked through its documented API with a person's own token (U244).

Its releases carry styles DJs and collectors tagged, so it covers the dance
records Beatport does not sell, and it is an API rather than a page behind a
bot check; it is asked first since U282.

A SEARCH, THEN THE RELEASES IT NAMES. The search carries no tracklist, so the
first few releases are read and one is accepted only when a track, or its own
title for a single, matches the file's title and artist through the shared
matcher. A wrong release is worse than a miss: its style would be written for
good. A file naming a mix takes only a release that writes that mix (U318).

The styles ride the outcome in Discogs' order, for the walk to choose among;
the coarse genres ride the note as context.

THE TOKEN IS A CREDENTIAL: read through ``core.secrets``, sent only in the
``Authorization`` header, and scrubbed from every note. No token is
``not-asked``, never a miss. A token the API rejects is the run's refusal,
since every later file would be refused alike. A refusal is remembered for the
process, so the asker is one per process, with one pacer for the run.

Layer: modules.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from urllib.parse import urlencode

from cratekit import __version__
from cratekit.core import secrets
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import titles
from cratekit.tagging.catalogues import (
    _GONE_STATUSES,
    DISCOGS,
    NOT_SENT,
    Answer,
    Fetch,
    Pacer,
    SourceOutcome,
    _artist_matches,
    _title_matches,
    unread_outcome,
)

#: The last bracketed group of a title, left out of the Discogs query.
_LAST_GROUP = re.compile(r"\s*\([^()]*\)\s*$")


def _last_group_stripped(value: str) -> str:
    return _LAST_GROUP.sub("", value).strip()


DISCOGS_API = "https://api.discogs.com"
DISCOGS_SEARCH = f"{DISCOGS_API}/database/search"
DISCOGS_RELEASE = f"{DISCOGS_API}/releases/"
#: Who a token belongs to, the one call setup spends to check one (U283).
DISCOGS_IDENTITY = f"{DISCOGS_API}/oauth/identity"

#: Search results asked for, and releases read: each read is a paced request,
#: so three is the cost a miss may spend.
DISCOGS_RESULTS_PER_PAGE = 10
DISCOGS_RELEASES_READ = 3

#: At or under this remaining count the next request waits first: slowing
#: down is cheaper than a 429 and the ladder behind it.
DISCOGS_REMAINING_FLOOR = 5
DISCOGS_SLOWDOWN_S = 10.0

DISCOGS_REMAINING_HEADER = "x-discogs-ratelimit-remaining"

#: The credential, by the name ``crate login`` records it under.
DISCOGS_CREDENTIAL = secrets.Credential.DISCOGS_TOKEN

#: How a person records the token, said wherever its absence is.
DISCOGS_LOGIN_STEPS = (
    "make a personal access token in your Discogs account's developer settings, "
    "put it in a file, and record it with crate login discogs-token --from-file PATH"
)

#: The ``not-asked`` notes for no token to send: never recorded, or recorded
#: and gone from the keychain. The tag summary counts both as "no token".
DISCOGS_NO_TOKEN = f"not asked: no Discogs token is recorded; {DISCOGS_LOGIN_STEPS}"
DISCOGS_TOKEN_LOST = (
    f"not asked: a Discogs token is recorded and the keychain no longer holds it; "
    f"{DISCOGS_LOGIN_STEPS}"
)
DISCOGS_UNASKED_NOTES: tuple[str, ...] = (DISCOGS_NO_TOKEN, DISCOGS_TOKEN_LOST)

#: The head of the ``not-asked`` note for a token Discogs refused, which the
#: tag summary counts and warns about even when Beatport settled every file.
DISCOGS_TOKEN_REFUSED = f"{NOT_SENT}Discogs refused the recorded token: "

#: A personal token is one printable word; anything else would be refused by a
#: client library in an error naming its value, so it is never sent.
_TOKEN_SHAPE = re.compile(r"[!-~]+")

_SCRUBBED = "[token]"

#: The product's one slug for a credential the run cannot use.
_CREDENTIAL_REASON = "credential-missing"

#: The same slug, public for a caller that tells a token refusal apart (U322).
CREDENTIAL_REASON = _CREDENTIAL_REASON


def discogs_headers(token: str) -> dict[str, str]:
    """What every Discogs request says: this tool and its version, never the
    person running it, and the token in its one place."""
    return {
        "User-Agent": f"Cratekit/{__version__}",
        "Accept": "application/json",
        "Authorization": f"Discogs token={token}",
    }


class TokenVerdict(Enum):
    """What Discogs said about a token setup was given (U283)."""

    #: Discogs named the account the token belongs to.
    ACCEPTED = "accepted"
    #: Discogs answered 401, or the token could not be sent at all.
    REJECTED = "rejected"
    #: A block, an outage, or an answer that was not the identity.
    UNCHECKED = "unchecked"


@dataclass(frozen=True, slots=True)
class TokenCheck:
    """One token check's verdict, and a note that never carries the token."""

    verdict: TokenVerdict
    note: str


@dataclass(frozen=True, slots=True)
class NotAsked:
    """A source the walk passed over with a reason, recorded ``not-asked``."""

    source: str
    note: str


@dataclass(frozen=True, slots=True)
class _Release:
    """The parts of one Discogs release this reader uses."""

    release_id: int
    title: str
    artists: str
    tracks: tuple[tuple[str, str], ...]
    styles: tuple[str, ...]
    genres: tuple[str, ...]


def _words_of(value: object) -> tuple[str, ...] | None:
    """The non empty strings of a list, or None when the field is not a list."""
    if not isinstance(value, list):
        return None
    return tuple(word.strip() for word in value if isinstance(word, str) and word.strip())


#: Discogs' numeral for a second artist of the same name, "Moodymann (2)".
_DISAMBIGUATION = re.compile(r"\s*\(\d+\)$")

#: An article filed last, "Prodigy, The", which the comma split of
#: ``_artist_matches`` would read as a second artist called "the".
_ARTICLE_LAST = re.compile(r"^(?P<name>.+?),\s*(?P<article>the|a|an)$", re.IGNORECASE)


def _discogs_name(name: str) -> str:
    """One Discogs artist name as a file's tag spells it: the numeral and the
    variation mark dropped, an article filed last put back first."""
    bare = _DISAMBIGUATION.sub("", name.strip().rstrip("*").strip())
    moved = _ARTICLE_LAST.match(bare)
    return f"{moved['article']} {moved['name']}" if moved else bare


def _credited(value: object) -> str:
    """The names of a Discogs artist list, joined as ``_artist_matches`` reads them."""
    if not isinstance(value, list):
        return ""
    names = (entry.get("name") for entry in value if isinstance(entry, dict))
    return ", ".join(
        _discogs_name(name) for name in names if isinstance(name, str) and name.strip()
    )


def _tracks_of(rows: object) -> list[dict[str, Any]]:
    """Every track of a tracklist, the sub tracks under an index row included."""
    if not isinstance(rows, list):
        return []
    found: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("type_", "track") == "track":
            found.append(row)
        found.extend(_tracks_of(row.get("sub_tracks")))
    return found


def _discogs_release(payload: dict[str, Any], release_id: int) -> _Release | None:
    """The release, or None when the answer is not a release this reader knows.

    Every release carries a tracklist, so an answer without one is a shape
    never seen. Absent styles or genres are no words; present and not a list
    is not a release.
    """
    tracklist = payload.get("tracklist")
    styles = _words_of(payload.get("styles", []))
    genres = _words_of(payload.get("genres", []))
    if not isinstance(tracklist, list) or styles is None or genres is None:
        return None
    title = payload.get("title")
    tracks = tuple(
        (str(row.get("title") or "").strip(), _credited(row.get("artists")))
        for row in _tracks_of(tracklist)
    )
    return _Release(
        release_id=release_id,
        title=title.strip() if isinstance(title, str) else "",
        artists=_credited(payload.get("artists")),
        tracks=tracks,
        styles=styles,
        genres=genres,
    )


class _Carries(Enum):
    """Whether a Discogs release carries the searched recording (U318)."""

    YES = "yes"
    #: The recording is there and the file's named version is not.
    ANOTHER_VERSION = "another version"
    NO = "no"


def _release_carries(
    release: _Release, artist: str, title: str, named: frozenset[titles.Words]
) -> _Carries:
    """Whether a release carries the searched recording, in its own version.

    A track whose title and credit (its own, else the release's) match, or for
    a single the release's own title and artist, through the shared matcher,
    which refuses a title that strips to nothing (R-1534).

    A REMIX IS NOT ITS TITLE (U318): a file naming a version, ``named``,
    counts a track only when it writes that version, and the single only when
    its title does or a track is the mix alone, or a remix takes a release of
    four other mixes. A version naming no one, "Extended Mix", is matched as
    before.
    """
    found = False
    for track_title, track_artists in release.tracks:
        credited = track_artists or release.artists
        if credited and _title_matches(title, track_title, artist=artist):
            if _artist_matches(artist, credited):
                if not named or titles.writes_version(track_title, named, titled=True):
                    return _Carries.YES
                found = True
    if (
        release.artists
        and _title_matches(title, release.title, artist=artist)
        and _artist_matches(artist, release.artists)
    ):
        if (
            not named
            or titles.writes_version(release.title, named, titled=True)
            or any(titles.writes_version(track, named, titled=False) for track, _ in release.tracks)
        ):
            return _Carries.YES
        found = True
    return _Carries.ANOTHER_VERSION if found else _Carries.NO


def _another_version(numbers: Sequence[int], named: frozenset[titles.Words]) -> str:
    """The miss's note when releases were refused for the file's version."""
    version = " or ".join(sorted(" ".join(name) for name in named))
    return "; ".join(
        f"Discogs release {number} holds no track with this version ({version})" for number in numbers
    )


def _release_note(release: _Release) -> str:
    styles = ", ".join(release.styles) or "none"
    genres = ", ".join(release.genres) or "none"
    return f"release {release.release_id} lists styles {styles} and genres {genres}"


#: What a read answered when the release it asked for is gone.
_GONE = object()


@dataclass
class DiscogsAsker:
    """One process's way of asking Discogs, with what it has learned on the way.

    ``token`` is None when none is recorded, and every file is then
    ``not-asked`` with ``unasked``. ``remaining`` is the last count Discogs
    said was left; after ``refused`` nothing more is asked in this process,
    and after ``rejected`` the token is never sent again in it. The token is
    kept out of the ``repr``.
    """

    token: str | None = field(repr=False)
    fetch: Fetch
    pacer: Pacer
    unasked: str = DISCOGS_NO_TOKEN
    remaining: int | None = None
    refused: SourceOutcome | None = None
    rejected: str | None = None

    def ask(self, artist: str, title: str, *, track: str | None = None) -> SourceOutcome | NotAsked:
        """Discogs' answer about one track, or why it was not asked.

        Asked for ``track``, the question (U289), and matched against
        ``title``, the file's own text; with no ``track`` the title is both.
        """
        if self.token is None:
            return NotAsked(DISCOGS, self.unasked)
        if self.rejected is not None:
            raise _rejected(f"{self.rejected}, earlier in this run, so Discogs was not asked")
        if not _TOKEN_SHAPE.fullmatch(self.token):
            self.rejected = "the recorded Discogs token is not one printable word"
            raise _rejected(f"{self.rejected}, so it was not sent")
        if self.refused is not None:
            return SourceOutcome(
                DISCOGS,
                Answer.BLOCKED,
                note=(
                    f"{NOT_SENT}Discogs refused this client earlier in this run and "
                    f"is not asked again in it. Then, {self.refused.note}"
                ),
            )
        said = self._search(artist, title, title if track is None else track)
        if said.answer is Answer.BLOCKED:
            self.refused = said
        return said

    def identity(self) -> TokenCheck:
        """Whether Discogs accepts this asker's token, by one identity call (U283).

        Through :meth:`_read`, the client a sweep asks through. Three verdicts,
        since a rejected token is one to make again and nothing may store it,
        while an unchecked one Discogs said nothing about may be stored and
        said so. Only a JSON object naming the account by number is acceptance.
        """
        if self.token is None:
            return TokenCheck(TokenVerdict.REJECTED, "no token was given, so Discogs was not asked")
        if not _TOKEN_SHAPE.fullmatch(self.token):
            return TokenCheck(
                TokenVerdict.REJECTED,
                "the token is not one printable word, so it was not sent to Discogs",
            )
        try:
            read = self._read(DISCOGS_IDENTITY, release=False)
        except CratekitError:
            if self.rejected is None:
                raise
            return TokenCheck(TokenVerdict.REJECTED, "Discogs answered 401, it does not accept this token")
        if isinstance(read, SourceOutcome):
            # Built by ``_said``, which scrubs the token from every note.
            return TokenCheck(TokenVerdict.UNCHECKED, read.note)
        assert isinstance(read, dict)
        if type(read.get("id")) is not int:
            return TokenCheck(
                TokenVerdict.UNCHECKED,
                "Discogs answered and the answer did not name an account, so the "
                "token was neither accepted nor refused",
            )
        return TokenCheck(TokenVerdict.ACCEPTED, "Discogs accepted the token")

    def _scrub(self, text: str) -> str:
        return text.replace(self.token, _SCRUBBED) if self.token else text

    def _said(self, answer: Answer, note: str = "") -> SourceOutcome:
        return SourceOutcome(DISCOGS, answer, note=self._scrub(note))

    def _read(self, url: str, *, release: bool) -> dict[str, Any] | SourceOutcome | object:
        """One paced touch: the JSON object, the answer its absence is, or gone.

        The count Discogs sent last decides whether to wait first. A release
        that is gone is a dead result, passed over; a search answering one is
        an API that moved, and unreachable.
        """
        if self.remaining is not None and self.remaining <= DISCOGS_REMAINING_FLOOR:
            self.pacer.sleep(DISCOGS_SLOWDOWN_S)
            self.remaining = None
        self.pacer.wait()
        page = self.fetch(url)
        if page.text is not None:
            self.remaining = _remaining(page.headers)
        if page.status == 401:
            self.rejected = "Discogs answered 401 to the token this installation records"
            raise _rejected(self.rejected)
        if release and page.status in _GONE_STATUSES:
            return _GONE
        refused = unread_outcome(DISCOGS, page)
        if refused is not None:
            return self._said(refused.answer, refused.note)
        try:
            payload = json.loads(page.text or "")
        except ValueError:
            return self._said(
                Answer.UNREACHABLE,
                "the answer was not JSON, so it did not come from the Discogs API",
            )
        if not isinstance(payload, dict):
            return self._said(
                Answer.PARSE_BREAK, "the answer was JSON and not an object"
            )
        return payload

    def _search(self, artist: str, title: str, track: str) -> SourceOutcome:
        # The question is ``track`` with its last bracketed group, the mix,
        # left out, or asked whole when that leaves nothing: an empty track
        # field asks for every release by the artist.
        bare = _last_group_stripped(track.strip()) or track.strip()
        query = urlencode(
            {
                "type": "release",
                "artist": artist.strip(),
                "track": bare,
                "per_page": DISCOGS_RESULTS_PER_PAGE,
            }
        )
        found = self._read(f"{DISCOGS_SEARCH}?{query}", release=False)
        if isinstance(found, SourceOutcome):
            return found
        assert isinstance(found, dict)
        results = found.get("results")
        if not isinstance(results, list):
            return self._said(
                Answer.PARSE_BREAK, "the search answer carries no list of results"
            )
        numbers = [
            entry["id"]
            for entry in results
            if isinstance(entry, dict)
            and type(entry.get("id")) is int
            and entry.get("type", "release") == "release"
        ]
        if results and not numbers:
            # The only evidence that tells a reshaped answer from an empty one.
            return self._said(
                Answer.PARSE_BREAK,
                "the search answered results and none names a release by number",
            )
        held: SourceOutcome | None = None
        styleless: SourceOutcome | None = None
        named = titles.named_versions(titles.read_file(title, artist))
        refused_version: list[int] = []
        for number in numbers[:DISCOGS_RELEASES_READ]:
            read = self._read(f"{DISCOGS_RELEASE}{number}", release=True)
            if read is _GONE:
                continue
            if isinstance(read, SourceOutcome):
                # A block ends the walk over releases; anything else unread is
                # held, since a later release may answer.
                if read.answer is Answer.BLOCKED:
                    return read
                held = held or read
                continue
            assert isinstance(read, dict)
            release = _discogs_release(read, number)
            if release is None:
                held = held or self._said(
                    Answer.PARSE_BREAK,
                    f"release {number} answered without a tracklist this reader knows",
                )
                continue
            carries = _release_carries(release, artist, title, named)
            if carries is _Carries.ANOTHER_VERSION:
                refused_version.append(number)
            if carries is not _Carries.YES:
                continue
            matched = SourceOutcome(
                DISCOGS,
                Answer.MATCHED,
                source_genre=release.styles[0] if release.styles else "",
                note=_release_note(release),
                words=release.styles,
            )
            if not release.styles:
                # Kept, not returned: another pressing may carry the styles.
                styleless = styleless or matched
                continue
            return matched
        # An unread pressing outranks a styleless match, since it may have
        # carried a style; and it is never a miss.
        if held is not None:
            return held
        if styleless is not None:
            return styleless
        return held if held is not None else self._said(Answer.MISS, _another_version(refused_version, named))


def _remaining(headers: Mapping[str, str]) -> int | None:
    """The request count Discogs said is left, or None when it said none."""
    raw = headers.get(DISCOGS_REMAINING_HEADER, "").strip()
    # ASCII digits only: ``isdigit`` is true of a superscript two, which
    # ``int`` refuses.
    return int(raw) if raw.isascii() and raw.isdigit() else None


def _rejected(why: str) -> CratekitError:
    """A token Discogs cannot use, as the run's refusal, typed as a rejection.

    Built from ``secrets.CredentialRejected`` so the remedy is the store's for
    a credential set and refused. Run scope, since every later file would be
    refused alike. The token is never in the sentence.
    """
    typed = secrets.CredentialRejected(why, name=str(DISCOGS_CREDENTIAL))
    error = refuse(
        _CREDENTIAL_REASON,
        f"{why}. Discogs was not read and nothing was recorded as a miss",
        remedy=Remedy(str(typed.remedy)),
        steps=(DISCOGS_LOGIN_STEPS,),
        scope=Scope.RUN,
        retryable=False,
        origin=("tagging", "searchers"),
        detail={"credential": str(DISCOGS_CREDENTIAL), "source": DISCOGS},
    )
    error.__cause__ = typed
    return error


def _recorded_token() -> tuple[str | None, str]:
    """The token the keychain holds, or None and the note saying why not.

    The presence index first, so an installation that never recorded one never
    touches the keychain. A keychain that cannot be read is refused, never
    read as no token, or a recorded token would go unasked without a word.
    """
    name = str(DISCOGS_CREDENTIAL)
    if not secrets.exists(name):
        return None, DISCOGS_NO_TOKEN
    try:
        return secrets.get(name), ""
    except secrets.CredentialMissing:
        return None, DISCOGS_TOKEN_LOST
    except secrets.CredentialError as exc:
        raise refuse(
            _CREDENTIAL_REASON,
            f"the Discogs token is recorded and the keychain could not be read for it "
            f"({type(exc).__name__}), so Discogs was not asked and nothing was "
            f"recorded as a miss",
            remedy=Remedy(str(exc.remedy)),
            scope=Scope.RUN,
            origin=("tagging", "searchers"),
            detail={"credential": name},
        ) from exc
