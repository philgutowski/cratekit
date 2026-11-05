"""The streaming provider's official catalogue API, under Cratekit's own app (U205).

WHAT WENT WRONG. The first two way sync asked the provider thousands of
catalogue questions, about one a second for over half an hour, and every one of
them went out under the person's own account session, beside his playlists, his
hearts and his downloads. Which tracks carry an ISRC is not a fact about his
account, and nothing made it his account's business except that the one client
the product held was logged in as him.

WHAT THIS IS. A client of the provider's developer platform, authenticated by
the client credentials flow: an app's identifier and key, stored in the
keychain through ``core/secrets``, exchanged for a short lived token at
:data:`TOKEN_URL`, and that token sent with every read of :data:`API_ROOT`. No
user is behind it, so it can answer catalogue questions and nothing else, which
is the property this unit exists for: a write cannot reach it, because it has
no write.

BUILT IN ONE PLACE. :class:`AppCatalogue` is constructed only by
``acquire.provider_session.catalogue_client``, beside the account opener, and
the pacing gate attaches to its transport there exactly as it attaches to the
account client's. Its token request and every read are then one more call the
gate paces, counts (as the ``app`` identity), breaks on and caps, unchanged. A
test walks the package for a second construction site.

THE OBJECTS IT RETURNS ARE SHAPED LIKE THE ACCOUNT CLIENT'S. :class:`Track`
carries the attributes ``modules.outbound.tidal_account._among`` and
``acquire.match.read_row`` read off the provider library's own track (an
identifier, a title, a version, an ISRC, the billed artists, the release, and
whether it streams), so the choosing logic reads one shape whichever identity
answered, and is not touched by this unit. The names come out of the answer's
``included`` resources, asked for with ``include``, so a lookup is one request
however many releases carry the code.

ERRORS ARE CLASSIFIED HERE AND NEVER BY TEXT DOWNSTREAM. A 404 is
:class:`CatalogueNotFound`, whose class name the callers already read as the
one "nothing there" answer. A 401 or 403, from the token service or a read, is
:class:`AppCredentialsRejected`, and the token is dropped so the next attempt
asks for a fresh one, since an expired token is the ordinary reason. A 429 is
:class:`CatalogueRateLimited`. Everything else, a server error, an answer that
is not JSON, a shape this client does not know, a transport that could not
connect, is :class:`CatalogueUnavailable`. **No message carries a URL, an
ISRC, an identifier or the digits of a not found**, because
``acquire.adapter.classify_unavailable`` reads "404" and "not found" out of an
exception's text, an ISRC or a track identifier can hold the digits 404, and
the outbound seam asks that classifier whether a failure is an absence. An
outage read as an absence is a track reported as one the provider lacks.

WHAT IT DOES NOT DO. It does not page. An ISRC answer is read as the one page
the API returns, as the provider library's own ISRC lookup reads it; a code
filed under more releases than one page holds is a residual of this unit. It
reads no label, no artist listing and no album listing: those stay on the
account for the reason ``label.tidal_catalogue`` gives.

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

#: The related resources a track read asks to be answered with, so the names
#: ``_among`` reads come in the same response rather than in one more request
#: per release.
INCLUDE = "artists,albums"

#: The most ISRCs one request may name, the catalogue API's own ``maxItems``
#: on ``filter[isrc]`` (U207). Given several, the API answers ONE TRACK PER
#: CODE and pages nothing, so a batch says which codes are held and never
#: which releases: see :meth:`AppCatalogue.isrcs_held`.
ISRC_BATCH = 20

#: How long one request may take before the transport gives up. The provider
#: library sets none, and a read that hangs holds the gate's lock for as long.
TIMEOUT_S = 30.0

#: How long before its stated expiry a token is replaced, so a token is never
#: sent in the last seconds of its life and refused on the way.
TOKEN_MARGIN_S = 60.0

#: Statuses that mean the provider judged the app's credential or token.
REJECTED_STATUSES = frozenset({401, 403})

#: The token service answers a bad identifier or key with a 400 under the
#: OAuth error form, so it is a rejection there as well.
TOKEN_REJECTED_STATUSES = frozenset({400, *REJECTED_STATUSES})

NOT_FOUND_STATUS = 404
RATE_LIMIT_STATUS = 429

#: The refusal a rejected app credential becomes once the ladder is spent.
#: ``credential-missing``, the slug every credential refusal carries, with the
#: remedy to record the value again rather than to log the account in.
REJECTED_REASON = "credential-missing"

#: The two stored values, the identifier first. Both or neither: one without
#: the other cannot ask for a token.
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
    """One catalogue track, in the attributes the account client's track has.

    ``available`` is None when the answer said nothing about streaming, which
    ``_streamable`` reads as streamable, the same reading it gives the account
    client's track when the field is absent.
    """

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
    """A status for a message, never spelled with the digits of a not found.

    A 404 that is NOT the API's own answer about a resource (the token service
    has no such address, say) is an unavailability, and its message must not
    read as an absence to ``classify_unavailable``.
    """
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
    resource: Mapping[str, Any],
    name: str,
    included: Mapping[tuple[str, str], Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    """The included resources one relationship names, in its order.

    A relationship naming a resource the answer did not include is skipped, so
    a track whose artists did not come back reads with no artist, which
    ``match.read_row`` refuses as unreadable and ``_among`` then declines to
    choose over. Skipping is the safe reading: a name made up here would be a
    choice made on nothing.
    """
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
        id=str(resource.get("id") or "").strip(),
        name=title,
        title=title,
        version=_text(attributes.get("version")) or None,
        isrc=_text(attributes.get("isrc")) or None,
        artists=artists,
        artist=artists[0] if artists else None,
        album=albums[0] if albums else None,
        available=_available(attributes),
    )


class AppCatalogue:
    """The catalogue reads the app's credential can make. Reads only.

    ``request_session`` is the transport, under the name the provider library
    gives its own, so ``provider_gate.Gate.attach`` finds and wraps it the same
    way. ``country_code`` is the account's own, so an availability answer is
    the one the account would get. ``clock`` is injectable so a suite drives a
    token's expiry without waiting it out.
    """

    def __init__(
        self,
        client_id: str,
        client_key: str,
        country_code: str,
        *,
        transport: Any,
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
        """One request, a failure to connect named without the address.

        THE GATE'S OWN REFUSAL PASSES THROUGH: a trip, a held lock or the call
        ceiling is raised inside the gated transport as the job engine's park,
        and wrapped here it would read as an outage and be retried into the
        cooldown. Every other exception the transport raises is one this client
        could not get an answer to, and its text, which carries the URL and so
        the ISRC, is left on the cause rather than in the message.
        """
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
            "POST",
            TOKEN_URL,
            data={"grant_type": "client_credentials"},
            auth=(self._client_id, self._client_key),
            headers={"Accept": "application/json"},
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
                f"the provider's token service answered {_status(int(status or 0))}",
                status=status,
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
        # A lifetime that cannot be read is treated as one margin long, so the
        # token serves the calls of the next minute and is then asked for again
        # rather than kept until the API refuses it.
        self._token = token
        # A SHORT LIFETIME KEEPS HALF OF ITSELF rather than none: a token living
        # a minute or less, with the margin taken whole, would be asked for
        # again before every read and double the app's calls.
        self._expires_at = (
            now + max(seconds - TOKEN_MARGIN_S, seconds / 2) if seconds > 0 else now + TOKEN_MARGIN_S
        )
        return token

    # ── the reads ─────────────────────────────────────────────────────────

    def _get(
        self, path: str, params: Mapping[str, Any], what: str, *, absence: bool = True
    ) -> Mapping[str, Any]:
        """One read. ``absence`` says whether a 404 on this route is the API's
        answer about a resource (a track by its identifier) or about the
        address itself (a collection, which answers a filter matching nothing
        with an empty list), in which case it is an outage and never no track."""
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
            # An expired token is the ordinary reason, so the next attempt on
            # the retry ladder asks for a fresh one rather than resending this.
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

        The provider library's method of the same name, answered in one request
        with the names included. An ISRC the catalogue files nothing under is
        answered as an empty list; the library raises its not found for that,
        and both callers read the two alike. A 404 HERE IS NOT THAT ANSWER: the
        collection answers a code matching nothing with an empty list, so a
        404 says the address moved or the filter's name changed, and read as
        no track it would be remembered by ``sync pair`` as a miss for every
        row it asked about (U205's review, round one).
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

        ONE REQUEST, NEVER A LOOKUP (U207). Given several codes the API answers
        one track per code, a release it picked, so nothing here reads a track
        off the answer: only the codes it names. A code it does not name is
        filed under nothing. A held code's releases are still
        :meth:`get_tracks_by_isrc`'s to answer.

        AN ANSWER THAT CANNOT BE ATTRIBUTED WHOLE IS AN OUTAGE, never a list of
        absences, because the caller reads every code left out as not found:

        * a track whose ISRC is missing or not one answers a code nobody can
          name, which may be any of those asked;
        * a code nobody asked says the API matched on something other than
          the spelling sent, so the one asked may be that one;
        * a ``next`` link says the answer is paged, and a code may be on the
          page not read.

        Each raises :class:`CatalogueUnavailable`, which the screen reads as
        nothing learned. The codes must be distinct, well formed and spelled as
        their own fold, which the caller checks; anything else is a defect
        here, not an answer.
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

    RUN SCOPE, because every lookup after it would be refused the same way and
    each would spend a ladder on the way. THE REMEDY IS TO RECORD THE APP'S
    VALUES AGAIN, never to log the account in: the account session was not
    judged, and sending a person to re-authorise it fixes nothing.
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
        scope=Scope.RUN,
        origin=("acquire", "catalogue_api"),
        detail={"credential": str(CREDENTIALS[0]), "status": exc.status},
    )


def unreadable(exc: secrets.CredentialError) -> CratekitError:
    """App credentials the presence index records and the keychain could not be read for.

    REFUSED, NOT READ AS ABSENT. A keychain that answered "not there" is an
    absence, and the opener reads it as one; a keychain that could not answer
    at all is a broken machine, and reading it as no app would put every
    lookup back on the account over a question nobody answered.
    """
    return refuse(
        REJECTED_REASON,
        f"Cratekit's app credentials are recorded and could not be read from the "
        f"keychain ({exc}), so the catalogue lookups that would go under them were "
        f"not asked of the account instead",
        # THE KEYCHAIN'S OWN REMEDY (round two): a backend that cannot be
        # reached refuses a write as it refused this read, so recording the
        # values again is the act only for a failure that says so.
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
    "API_ROOT",
    "CREDENTIALS",
    "INCLUDE",
    "ISRC_BATCH",
    "LOGIN_STEPS",
    "TOKEN_URL",
    "Album",
    "AppCatalogue",
    "AppCredentialsRejected",
    "Artist",
    "CatalogueError",
    "CatalogueNotFound",
    "CatalogueRateLimited",
    "CatalogueUnavailable",
    "Track",
    "rejected",
    "track_of",
    "unreadable",
]
