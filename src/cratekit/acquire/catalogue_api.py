"""The streaming provider's official catalogue API, under Cratekit's own app (U205).

A client credentials client: the app's identifier and key, kept in the keychain
through ``core/secrets``, are exchanged for a short lived token at
:data:`TOKEN_URL` and sent with every read of :data:`API_ROOT`. No user is behind
it, so catalogue questions stay off the person's account and no write can reach
it. :class:`AppCatalogue` is built only by
``acquire.provider_session.catalogue_client``, where the pacing gate attaches.
:class:`Track` carries the account client's track attributes, so the choosing
logic reads one shape.

Errors are classified here, never by text downstream: 404 is
:class:`CatalogueNotFound`, 401 or 403 :class:`AppCredentialsRejected` with the
token dropped, 429 :class:`CatalogueRateLimited`, all else
:class:`CatalogueUnavailable`. **No message carries a URL, an ISRC, an identifier
or the digits of a not found**, because ``acquire.adapter.classify_unavailable``
reads "404" out of text and an outage read as an absence reports a track the
provider lacks. A batch answers presence only (U207). Nothing pages, and no label
or listing is read here.

Layer: acquire.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from cratekit.acquire import match
from cratekit.core import secrets
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

#: Where the app's identifier and key are exchanged for a token.
TOKEN_URL = "https://auth.tidal.com/v1/oauth2/token"

#: The official catalogue API's root. Every read is a path under it.
API_ROOT = "https://openapi.tidal.com/v2/"

#: The media type the API answers in, asked for by name.
JSON_API = "application/vnd.api+json"

#: The related resources a track read asks for, so names come in the same response.
INCLUDE = "artists,albums"

#: The most ISRCs one request may name, the API's ``maxItems``. A batch answers one
#: track per code, so it says which codes are held, never which releases (U207).
ISRC_BATCH = 20

#: Per request timeout, since a read that hangs holds the gate's lock.
TIMEOUT_S = 30.0

#: How long before expiry a token is replaced, so it is not refused on the way.
TOKEN_MARGIN_S = 60.0

#: Statuses that mean the provider judged the app's credential or token.
REJECTED_STATUSES = frozenset({401, 403})

#: The token service answers a bad identifier or key with an OAuth 400 as well.
TOKEN_REJECTED_STATUSES = frozenset({400, *REJECTED_STATUSES})

NOT_FOUND_STATUS = 404
RATE_LIMIT_STATUS = 429

#: The slug of the refusal a rejected app credential becomes once the ladder is spent.
REJECTED_REASON = "credential-missing"

#: The two stored values, the identifier first. Both or neither.
CREDENTIALS = (secrets.Credential.CATALOGUE_APP_ID, secrets.Credential.CATALOGUE_APP_KEY)

#: How a person records them, named by every refusal and by doctor.
LOGIN_STEPS = (
    f"register an app on the streaming provider's developer platform, put its "
    f"client identifier in one file and its key in another, each readable only "
    f"by you, then run crate login {CREDENTIALS[0]} --from-file PATH and crate "
    f"login {CREDENTIALS[1]} --from-file PATH"
)


class CatalogueError(Exception):
    """A catalogue API call that did not answer. ``status`` is the HTTP status,
    or None for a call that never got one."""

    def __init__(self, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class CatalogueNotFound(CatalogueError):
    """The API answered that it holds no such resource. The one absence."""


class AppCredentialsRejected(CatalogueError):
    """The token service or the API refused the app's credential or its token."""


class CatalogueRateLimited(CatalogueError):
    """The API answered rate limited. The gate has counted it already."""


class CatalogueUnavailable(CatalogueError):
    """Every other failure: a server error, an unknown shape, no connection."""


@dataclass(frozen=True, slots=True)
class Artist:
    """One billed artist, as the provider library's artist is read here."""

    id: str
    name: str


@dataclass(frozen=True, slots=True)
class Album:
    """The release a track sits on. ``name`` is what ``_album_name`` reads."""

    id: str
    name: str


@dataclass(frozen=True, slots=True)
class Track:
    """One catalogue track in the account client's track attributes. ``available``
    is None when the answer said nothing, which ``_streamable`` reads as streamable."""

    id: str
    name: str
    title: str
    version: str | None
    isrc: str | None
    artists: tuple[Artist, ...]
    artist: Artist | None
    album: Album | None
    available: bool | None


def _status(status: int) -> str:
    """A status for a message, never the digits of a not found, so an outage's
    message is not read as an absence."""
    if status == NOT_FOUND_STATUS:
        return "a status saying the address does not exist"
    return f"status {status}"


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _included(body: Mapping[str, Any]) -> dict[tuple[str, str], Mapping[str, Any]]:
    """Every included resource, by its type and identifier."""
    held: dict[tuple[str, str], Mapping[str, Any]] = {}
    for resource in body.get("included") or ():
        if isinstance(resource, Mapping):
            kind = _text(resource.get("type"))
            identity = str(resource.get("id") or "").strip()
            if kind and identity:
                held[(kind, identity)] = resource
    return held


def _related(
    resource: Mapping[str, Any], name: str, included: Mapping[tuple[str, str], Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    """The included resources one relationship names, in order. One not included
    is skipped rather than invented, so the track reads as unreadable."""
    relationships = resource.get("relationships")
    if not isinstance(relationships, Mapping):
        return []
    related = relationships.get(name)
    data = related.get("data") if isinstance(related, Mapping) else None
    if isinstance(data, Mapping):
        data = [data]
    found: list[Mapping[str, Any]] = []
    for pointer in data or ():
        if not isinstance(pointer, Mapping):
            continue
        key = (_text(pointer.get("type")), str(pointer.get("id") or "").strip())
        target = included.get(key)
        if target is not None:
            found.append(target)
    return found


def _attributes(resource: Mapping[str, Any]) -> Mapping[str, Any]:
    attributes = resource.get("attributes")
    return attributes if isinstance(attributes, Mapping) else {}


def _available(attributes: Mapping[str, Any]) -> bool | None:
    """Whether the track streams, off ``availability``, else None for unsaid."""
    said = attributes.get("availability")
    if not isinstance(said, (list, tuple)):
        return None
    return any(str(mode).strip().upper() == "STREAM" for mode in said)


def track_of(
    resource: Mapping[str, Any], included: Mapping[tuple[str, str], Mapping[str, Any]]
) -> Track:
    """One track resource, with its artists and release read off ``included``."""
    attributes = _attributes(resource)
    title = _text(attributes.get("title"))
    artists = tuple(
        Artist(id=str(found.get("id") or "").strip(), name=_text(_attributes(found).get("name")))
        for found in _related(resource, "artists", included)
        if _text(_attributes(found).get("name"))
    )
    albums = [
        Album(id=str(found.get("id") or "").strip(), name=_text(_attributes(found).get("title")))
        for found in _related(resource, "albums", included)
    ]
    return Track(
        id=str(resource.get("id") or "").strip(), name=title, title=title,
        version=_text(attributes.get("version")) or None,
        isrc=_text(attributes.get("isrc")) or None, artists=artists,
        artist=artists[0] if artists else None, album=albums[0] if albums else None,
        available=_available(attributes),
    )


class AppCatalogue:
    """The catalogue reads the app's credential can make. Reads only.

    ``request_session`` is named as the provider library's is, so the gate attaches
    the same way. ``country_code`` is the account's, and ``clock`` is injectable.
    """

    def __init__(
        self, client_id: str, client_key: str, country_code: str, *, transport: Any,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.request_session = transport
        self.country_code = country_code
        self._client_id = client_id
        self._client_key = client_key
        self._clock = clock
        self._token: str | None = None
        self._expires_at = 0.0

    # ── the transport ─────────────────────────────────────────────────────

    def _send(self, method: str, url: str, **kwargs: Any) -> Any:
        """One request, a failure to connect named without the address. The gate's
        own refusal passes through, since wrapped it would be retried as an outage."""
        try:
            return self.request_session.request(method, url, timeout=TIMEOUT_S, **kwargs)
        except CratekitError:
            raise
        except Exception as exc:  # noqa: BLE001 - classified, never swallowed
            raise CatalogueUnavailable(
                f"the catalogue API could not be reached ({type(exc).__name__})"
            ) from exc

    @staticmethod
    def _json(response: Any, what: str) -> Mapping[str, Any]:
        try:
            body = response.json()
        except Exception as exc:  # noqa: BLE001 - every decoder fails differently
            raise CatalogueUnavailable(
                f"the {what} answered with a body that is not JSON ({type(exc).__name__})",
                status=getattr(response, "status_code", None),
            ) from exc
        if not isinstance(body, Mapping):
            raise CatalogueUnavailable(
                f"the {what} answered with JSON that is not an object",
                status=getattr(response, "status_code", None),
            )
        return body

    # ── the token ─────────────────────────────────────────────────────────

    def _access_token(self) -> str:
        """The app's token, fetched once and reused until shortly before it lapses."""
        now = self._clock()
        if self._token is not None and now < self._expires_at:
            return self._token
        response = self._send(
            "POST", TOKEN_URL, data={"grant_type": "client_credentials"},
            auth=(self._client_id, self._client_key), headers={"Accept": "application/json"},
        )
        status = getattr(response, "status_code", None)
        if status in TOKEN_REJECTED_STATUSES:
            raise AppCredentialsRejected(
                f"the provider's token service refused Cratekit's app credentials "
                f"({_status(status)})",
                status=status,
            )
        if status == RATE_LIMIT_STATUS:
            raise CatalogueRateLimited(
                "the provider's token service answered rate limited", status=status
            )
        if status != 200:
            raise CatalogueUnavailable(
                f"the provider's token service answered {_status(int(status or 0))}", status=status,
            )
        body = self._json(response, "token service")
        token = _text(body.get("access_token"))
        if not token:
            raise CatalogueUnavailable(
                "the provider's token service answered with no access token", status=status
            )
        lifetime = body.get("expires_in")
        seconds = (
            float(lifetime)
            if isinstance(lifetime, (int, float)) and not isinstance(lifetime, bool)
            else 0.0
        )
        # An unreadable lifetime counts as one margin, so the token is asked again soon.
        self._token = token
        # A short lifetime keeps half itself, or the token is fetched before every read.
        self._expires_at = (
            now + max(seconds - TOKEN_MARGIN_S, seconds / 2) if seconds > 0 else now + TOKEN_MARGIN_S
        )
        return token

    # ── the reads ─────────────────────────────────────────────────────────

    def _get(
        self, path: str, params: Mapping[str, Any], what: str, *, absence: bool = True
    ) -> Mapping[str, Any]:
        """One read. ``absence`` says whether a 404 here answers about a resource; on
        a collection it is about the address, so an outage and never no track."""
        token = self._access_token()
        response = self._send(
            "GET",
            API_ROOT + path,
            params={**params, "countryCode": self.country_code},
            headers={"Authorization": f"Bearer {token}", "Accept": JSON_API},
        )
        status = getattr(response, "status_code", None)
        if status == NOT_FOUND_STATUS and absence:
            raise CatalogueNotFound(
                f"the catalogue API holds no such resource for this {what}", status=status
            )
        if status in REJECTED_STATUSES:
            # An expired token is the ordinary reason, so the next attempt fetches anew.
            self._token = None
            raise AppCredentialsRejected(
                f"the catalogue API refused Cratekit's app token for this {what} "
                f"({_status(status)})",
                status=status,
            )
        if status == RATE_LIMIT_STATUS:
            raise CatalogueRateLimited(
                f"the catalogue API answered rate limited to this {what}", status=status
            )
        if status != 200:
            raise CatalogueUnavailable(
                f"the catalogue API answered {_status(int(status or 0))} to this {what}",
                status=status,
            )
        return self._json(response, f"catalogue API's answer to this {what}")

    def get_tracks_by_isrc(self, isrc: str) -> list[Track]:
        """Every track the catalogue files under one ISRC, an empty list for none.

        A 404 here is an outage, not that answer: the collection answers a code
        matching nothing with an empty list, and a miss is remembered by ``sync pair``.
        """
        what = "ISRC lookup"
        body = self._get(
            "tracks", {"filter[isrc]": str(isrc), "include": INCLUDE}, what, absence=False
        )
        data = body.get("data")
        if not isinstance(data, list):
            raise CatalogueUnavailable(
                f"the catalogue API's answer to this {what} carries no list of tracks"
            )
        included = _included(body)
        return [
            track_of(resource, included)
            for resource in data
            if isinstance(resource, Mapping) and _text(resource.get("type")) in ("", "tracks")
        ]

    def isrcs_held(self, codes: Sequence[str]) -> frozenset[str]:
        """Which of two to :data:`ISRC_BATCH` codes the catalogue files any track under.

        One request, reading only the codes named (U207). An answer that cannot be
        attributed whole, a track with no readable ISRC, a code not asked or a
        ``next`` link, raises :class:`CatalogueUnavailable`, since the caller reads
        every code left out as not found. The caller passes distinct folded codes.
        """
        asked = tuple(str(code) for code in codes)
        if not 2 <= len(asked) <= ISRC_BATCH:
            raise ValueError(f"a batch names two to {ISRC_BATCH} ISRCs")
        if len(set(asked)) != len(asked) or any(code != match.isrc_token(code) for code in asked):
            raise ValueError("a batch names distinct ISRCs, each in its own fold")
        what = "ISRC batch"
        body = self._get("tracks", {"filter[isrc]": list(asked)}, what, absence=False)
        data = body.get("data")
        if not isinstance(data, list):
            raise CatalogueUnavailable(
                f"the catalogue API's answer to this {what} carries no list of tracks"
            )
        links = body.get("links")
        if isinstance(links, Mapping) and _text(links.get("next")):
            raise CatalogueUnavailable(
                f"the catalogue API paged its answer to this {what}, so a code "
                f"left out may be on a page not read"
            )
        named: set[str] = set()
        for resource in data:
            if not isinstance(resource, Mapping):
                raise CatalogueUnavailable(
                    f"the catalogue API's answer to this {what} holds an entry that is not a resource"
                )
            if _text(resource.get("type")) not in ("", "tracks"):
                continue
            code = match.isrc_token(_attributes(resource).get("isrc"))
            if not code:
                raise CatalogueUnavailable(
                    f"the catalogue API's answer to this {what} holds a track with no "
                    f"readable ISRC, so which code it answers cannot be told"
                )
            named.add(code)
        if not named <= set(asked):
            raise CatalogueUnavailable(
                f"the catalogue API's answer to this {what} names a code that was not asked"
            )
        return frozenset(named)

    def track(self, track_id: str) -> Track:
        """One track by its identifier. A track the catalogue lacks is not found."""
        identity = str(track_id or "").strip()
        if not (identity.isascii() and identity.isdigit()):
            raise ValueError("a catalogue track identifier is a whole number")
        what = "track read"
        body = self._get(f"tracks/{identity}", {"include": INCLUDE}, what)
        data = body.get("data")
        if not isinstance(data, Mapping):
            raise CatalogueUnavailable(
                f"the catalogue API's answer to this {what} carries no track"
            )
        return track_of(data, _included(body))


def rejected(exc: AppCredentialsRejected, doing: str) -> CratekitError:
    """A rejected app credential, once the ladder is spent, as the run's refusal.

    Run scope, since every later lookup would be refused alike. The remedy is to
    record the app's values again, never to log in: the account was not judged.
    """
    return refuse(
        REJECTED_REASON,
        f"the streaming provider refused Cratekit's app credentials while trying "
        f"to {doing} ({exc}); the account session was not judged and is kept",
        remedy=Remedy.SET_CREDENTIAL,
        steps=(
            "check the app on the provider's developer platform",
            f"record its identifier and key again: {LOGIN_STEPS}",
        ),
        scope=Scope.RUN, origin=("acquire", "catalogue_api"),
        detail={"credential": str(CREDENTIALS[0]), "status": exc.status},
    )


def unreadable(exc: secrets.CredentialError) -> CratekitError:
    """App credentials recorded but unreadable from the keychain, refused rather than
    read as absent, so lookups do not fall back to the account on no answer."""
    return refuse(
        REJECTED_REASON,
        f"Cratekit's app credentials are recorded and could not be read from the "
        f"keychain ({exc}), so the catalogue lookups that would go under them were "
        f"not asked of the account instead",
        # The keychain's own remedy: recording again helps only a failure that says so.
        remedy=Remedy(str(exc.remedy)),
        steps=(
            (f"record them again: {LOGIN_STEPS}",)
            if exc.remedy is secrets.Remedy.SET_CREDENTIAL
            else ()
        ),
        scope=Scope.RUN,
        origin=("acquire", "catalogue_api"),
        detail={"credential": str(getattr(exc, "name", "") or CREDENTIALS[0])},
    )


__all__ = [
    "API_ROOT", "CREDENTIALS", "INCLUDE", "ISRC_BATCH", "LOGIN_STEPS", "TOKEN_URL", "Album",
    "AppCatalogue", "AppCredentialsRejected", "Artist", "CatalogueError", "CatalogueNotFound",
    "CatalogueRateLimited", "CatalogueUnavailable", "Track", "rejected", "track_of", "unreadable",
]
