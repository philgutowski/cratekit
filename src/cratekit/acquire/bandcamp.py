"""Bandcamp: the account's purchases, read from the account's own endpoints (U176).

Sitting 46 brought 45 releases from one seller into staging by hand, through a
third party tool, a cookie pasted into a file, a name match on file paths, an
ignore file kept by hand and a flatten with ``mv``. This module is the part of
that lane that talks to Bandcamp: it lists what the account holds and fetches
one release. Deciding what to fetch, and where the files go, is
:mod:`cratekit.acquire.bandcamp_cli`'s.

WHY A CLIENT OF TWO ENDPOINTS AND NOT ``bandcampsync``. The tool sitting 46 ran
does three things this product cannot have: its state file is a checkpoint, so
a purchase skipped once is never offered again; a missing ignore file makes it
copy a template that exists only in its container image and crash; and it logs
the first twenty characters of the session at INFO. Taking it in meant guarding
against all three to use two requests, so the two requests are written here.

WHAT THE ENDPOINTS ARE, as sitting 46 measured them. The collection summary
names the fan; the collection is ``collection_items``, a POST of the fan, an
``older_than_token`` and a count, a page at a time, newest first; the purchases
the fan hid come from ``hidden_items`` in the same shape. Each item carries its
seller's account in the host of its address, since the ``label`` field was
empty on every release of the seller measured. A release downloads from a
signed page whose data blob names one link per format.

THE SESSION AND EVERY SIGNED LINK ARE CREDENTIALS. The session is the browser's
cookie and its ``identity`` value is the login; a signed link fetches a release
without one. So neither is put in a message, a ``repr``, a log line or anything
that serializes: :class:`Purchase` holds its signed page apart from its
``to_json``, the transport's own exceptions are replaced rather than chained,
because their text carries the address they failed on, and nothing here logs.

THE TRANSPORT IS A SEAM. :class:`Transport` is three calls, and the one that
reaches the network, :class:`CurlTransport`, imports ``curl_cffi`` only when it
is built, so the suite never loads it and a test hands in a fake. Bandcamp sits
behind a bot check that refuses an ordinary client, so the real transport
presents a browser's TLS fingerprint, which is what ``curl_cffi`` is for.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import time
import zipfile
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from email.message import Message
from pathlib import Path, PurePosixPath
from typing import Any, Protocol
from urllib.parse import urlsplit, urlunsplit

#: The account's home. Every request but a download goes here.
BASE = "https://bandcamp.com"
SUMMARY_PATH = "/api/fan/2/collection_summary"
ITEMS_PATH = "/api/fancollection/1/collection_items"
HIDDEN_PATH = "/api/fancollection/1/hidden_items"

#: Purchases a page, the count sitting 46 measured the endpoint answering.
PAGE_SIZE = 100

#: The most pages one listing reads before it refuses. A page whose token does
#: not move is refused on its own; this bounds a token that moves forever.
MAX_PAGES = 1000

#: The formats asked for. FLAC is lossless and is what the strict policy calls
#: for; MP3 at 320 is the lossy fallback a permissive policy may take, marked.
LOSSLESS_ENCODING = "flac"
LOSSY_ENCODING = "mp3-320"

#: Every lossless format a release may offer, in the order one is taken. FLAC
#: first, since it carries its tags the way the rest of the library does.
LOSSLESS_ENCODINGS = (LOSSLESS_ENCODING, "alac", "aiff-lossless", "wav")

#: Statuses that judge the SESSION, as against the request.
REJECTED_STATUSES = frozenset({401, 403})

#: The suffix of a seller account's own address.
_ACCOUNT_HOST = ".bandcamp.com"

#: The hosts the session is ever sent to: Bandcamp itself and the file servers
#: its download pages name. A link anywhere else, or over plain http, is never
#: requested, because every request carries the session.
TRUSTED_HOSTS = ("bandcamp.com", "bcbits.com")

#: Suffixes a release may carry that are audio. Everything else in a release's
#: archive, the cover image above all, stays in the holding folder and goes
#: with it.
AUDIO_SUFFIXES = frozenset({".flac", ".mp3", ".aiff", ".aif", ".wav", ".m4a", ".ogg"})

_BLOB = re.compile(r"""data-blob\s*=\s*(["'])(?P<blob>.*?)\1""", re.DOTALL)


class BandcampError(Exception):
    """Base for every failure here. Its message never carries a link or a cookie."""


class SessionRejected(BandcampError):
    """The session is expired, logged out or refused: the person signs in again."""


class BandcampUnavailable(BandcampError):
    """Bandcamp did not answer, or answered in a shape this client cannot read."""


class FormatUnavailable(BandcampError):
    """The release offers no download in the format asked for."""

    def __init__(self, message: str, *, offered: Sequence[str]) -> None:
        super().__init__(message)
        self.offered = tuple(offered)


@dataclass(frozen=True, slots=True)
class Response:
    """What one request answered: the status, the body as text, the headers."""

    status: int
    text: str
    headers: Mapping[str, str] = field(default_factory=dict)


class Transport(Protocol):
    """The three requests this client makes. A test implements these."""

    def get(self, url: str, *, cookie: str) -> Response: ...

    def post_json(self, url: str, payload: Mapping[str, Any], *, cookie: str) -> Response: ...

    def download(self, url: str, directory: Path, *, cookie: str) -> Path:
        """Stream ``url`` into a new file inside ``directory`` and return it."""
        ...


@dataclass(frozen=True, slots=True)
class Track:
    """One track of a release as the collection lists it."""

    number: int | None
    artist: str
    title: str

    def to_json(self) -> dict[str, Any]:
        return {"number": self.number, "artist": self.artist, "title": self.title}


@dataclass(frozen=True, slots=True)
class Purchase:
    """One purchase in the account, everything about it that is not a credential.

    ``download_page`` IS A CREDENTIAL. It is the signed page a release is
    fetched from, so it stays out of :meth:`to_json`, out of the ``repr`` and
    out of equality, and is read only by the worker that fetches.
    """

    item_id: str
    seller: str
    artist: str
    title: str
    item_type: str
    purchased: str
    item_url: str
    tracks: tuple[Track, ...]
    hidden: bool = False
    preorder: bool = False
    download_page: str = field(default="", repr=False, compare=False)

    @property
    def downloadable(self) -> bool:
        """Whether the account can download it now: a link, and no preorder."""
        return bool(self.download_page) and not self.preorder

    def to_json(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "seller": self.seller,
            "artist": self.artist,
            "title": self.title,
            "item_type": self.item_type,
            "purchased": self.purchased,
            "item_url": self.item_url,
            "hidden": self.hidden,
            "preorder": self.preorder,
            "downloadable": self.downloadable,
            "tracks": [track.to_json() for track in self.tracks],
        }


@dataclass(frozen=True, slots=True)
class Collection:
    """Every purchase the account holds, hidden ones included, newest first."""

    fan_id: str
    purchases: tuple[Purchase, ...]


# ---------------------------------------------------------------------------
# Reading answers
# ---------------------------------------------------------------------------


def _json(response: Response, what: str) -> Any:
    """The body of a JSON answer, or the failure it is.

    A status that judges the session is :class:`SessionRejected`, never an
    empty collection: a logged out cookie must not read as an account that
    holds nothing.
    """
    if response.status in REJECTED_STATUSES:
        raise SessionRejected(f"Bandcamp refused the session when asked for {what}")
    if response.status != 200:
        raise BandcampUnavailable(f"Bandcamp answered {response.status} when asked for {what}")
    try:
        return json.loads(response.text)
    except ValueError:
        raise BandcampUnavailable(f"Bandcamp's answer for {what} is not JSON") from None


def seller_of(item_url: str) -> str:
    """The seller account a purchase belongs to: the host of its address.

    ``pulsromania.bandcamp.com`` is ``pulsromania``. A seller on a domain of its
    own keeps the whole host, which is the only name the address gives.
    """
    host = (urlsplit(item_url).hostname or "").lower()
    if host.endswith(_ACCOUNT_HOST):
        return host[: -len(_ACCOUNT_HOST)]
    return host


def trusted(link: str) -> bool:
    """Whether ``link`` may be requested with the session: https, to Bandcamp."""
    parts = urlsplit(link)
    host = (parts.hostname or "").lower()
    return parts.scheme == "https" and any(
        host == domain or host.endswith("." + domain) for domain in TRUSTED_HOSTS
    )


def _number(value: object) -> int | None:
    try:
        number = int(str(value))
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def _tracks(listed: object) -> tuple[Track, ...]:
    if not isinstance(listed, list):
        return ()
    found: list[Track] = []
    for entry in listed:
        if not isinstance(entry, Mapping):
            continue
        title = str(entry.get("title") or "").strip()
        if not title:
            continue
        found.append(
            Track(
                number=_number(entry.get("track_number")),
                artist=str(entry.get("artist") or "").strip(),
                title=title,
            )
        )
    return tuple(found)


def _purchase(item: Mapping[str, Any], page: Mapping[str, Any], *, hidden: bool) -> Purchase:
    links = page.get("redownload_urls") or {}
    listed = page.get("tracklists") or {}
    sale = f"{item.get('sale_item_type') or ''}{item.get('sale_item_id') or ''}"
    tralbum = f"{item.get('tralbum_type') or ''}{item.get('tralbum_id') or ''}"
    item_url = str(item.get("item_url") or "")
    return Purchase(
        item_id=str(item.get("item_id") or tralbum or sale),
        seller=seller_of(item_url),
        artist=str(item.get("band_name") or "").strip(),
        title=str(item.get("item_title") or "").strip(),
        item_type=str(item.get("item_type") or ""),
        purchased=str(item.get("purchased") or ""),
        item_url=item_url,
        tracks=_tracks(listed.get(tralbum) if isinstance(listed, Mapping) else None),
        hidden=hidden,
        preorder=bool(item.get("is_preorder")),
        download_page=str(links.get(sale) or "") if isinstance(links, Mapping) else "",
    )


def _pages(
    transport: Transport, cookie: str, fan_id: str, path: str, *, hidden: bool, start: str
) -> Iterator[Purchase]:
    """Every purchase one listing holds, a page at a time, until an empty page.

    NO CHECKPOINT. Every run reads the whole account from the newest purchase
    back, because the record of what was fetched is kept by purchase, and a
    listing that started where the last one stopped would hide every purchase
    older than that point, which is the trap ``bandcampsync``'s state file sets.
    """
    token = start
    seen = {token}
    what = "the hidden purchases" if hidden else "the collection"
    for _ in range(MAX_PAGES):
        page = _json(
            transport.post_json(
                BASE + path,
                {"fan_id": fan_id, "older_than_token": token, "count": PAGE_SIZE},
                cookie=cookie,
            ),
            what,
        )
        if not isinstance(page, Mapping):
            raise BandcampUnavailable(f"a page of {what} is not an object")
        if page.get("error"):
            raise SessionRejected(f"Bandcamp refused the session when asked for {what}")
        items = page.get("items")
        if not isinstance(items, list):
            # A page with no list at all is not the empty page that ends a
            # listing; read as one it would call every purchase absent.
            raise BandcampUnavailable(f"a page of {what} holds no list of items")
        if not items:
            return
        for item in items:
            if isinstance(item, Mapping):
                yield _purchase(item, page, hidden=hidden)
        if page.get("more_available") is False:
            return
        token = str(page.get("last_token") or "")
        if not token or token in seen:
            # A page with items and no way on: reading it as the end would call
            # every older purchase absent, so it is refused instead.
            raise BandcampUnavailable(
                f"a page of {what} names no next page, so the purchases older than "
                f"it could not be read"
            )
        seen.add(token)
    raise BandcampUnavailable(f"{what} ran past {MAX_PAGES} pages without ending")


def _when(purchase: Purchase) -> float | None:
    text = purchase.purchased.strip()
    for shape in ("%d %b %Y %H:%M:%S %Z", "%d %b %Y %H:%M:%S"):
        try:
            return datetime.strptime(text, shape).timestamp()
        except ValueError:
            continue
    return None


def newest_first(purchases: Sequence[Purchase]) -> tuple[Purchase, ...]:
    """Newest purchase first. A date that cannot be read keeps its listed place
    after every dated one, since the listing itself is newest first."""
    order = []
    for position, purchase in enumerate(purchases):
        stamp = _when(purchase)
        order.append(((0, -stamp) if stamp is not None else (1, 0.0), position, purchase))
    return tuple(purchase for *_key, purchase in sorted(order, key=lambda row: row[:2]))


def read_collection(
    transport: Transport, cookie: str, *, now: float | None = None
) -> Collection:
    """Every purchase the account holds, hidden ones marked, newest first.

    A cookie the summary does not answer with a fan is :class:`SessionRejected`:
    the summary is how a logged out cookie is told from an empty account.
    """
    summary = _json(transport.get(BASE + SUMMARY_PATH, cookie=cookie), "the collection summary")
    fan_id = str(summary.get("fan_id") or "") if isinstance(summary, Mapping) else ""
    if not fan_id:
        raise SessionRejected("Bandcamp did not recognise the session as a signed in fan")
    start = f"{int(time.time() if now is None else now)}::a::"
    shown = list(_pages(transport, cookie, fan_id, ITEMS_PATH, hidden=False, start=start))
    hidden = list(_pages(transport, cookie, fan_id, HIDDEN_PATH, hidden=True, start=start))
    known = {purchase.item_id for purchase in shown}
    merged = shown + [purchase for purchase in hidden if purchase.item_id not in known]
    return Collection(fan_id=fan_id, purchases=newest_first(merged))


# ---------------------------------------------------------------------------
# Fetching one release
# ---------------------------------------------------------------------------


def _blob(text: str) -> Mapping[str, Any]:
    for found in _BLOB.finditer(text):
        try:
            data = json.loads(html.unescape(found.group("blob")))
        except ValueError:
            continue
        if isinstance(data, Mapping) and "digital_items" in data:
            return data
    raise BandcampUnavailable("the release's download page holds no download data")


def download_offers(transport: Transport, cookie: str, page_url: str) -> dict[str, str]:
    """Format to signed link, for the release behind one signed download page.

    THE RETURN VALUE IS A CREDENTIAL. A caller reads one link out of it and
    hands that to :func:`fetch`, and keeps it out of every message.

    THE PAGE IS CHECKED BEFORE IT IS ASKED, the way every file link is, because
    this is the first request of a fetch that carries the session. A page that
    lists no formats, or only formats whose links lead outside Bandcamp, is
    :class:`BandcampUnavailable`: read as an empty offer it would tell the
    person to relax the lossless policy over a release that offers FLAC.
    """
    if not trusted(page_url):
        raise BandcampUnavailable("the release's download page does not lead to Bandcamp over https")
    response = transport.get(page_url, cookie=cookie)
    if response.status in REJECTED_STATUSES:
        raise SessionRejected("Bandcamp refused the session on the release's download page")
    if response.status != 200:
        raise BandcampUnavailable(
            f"Bandcamp answered {response.status} for the release's download page"
        )
    items = _blob(response.text).get("digital_items")
    if not isinstance(items, list) or not items or not isinstance(items[0], Mapping):
        raise BandcampUnavailable("the release's download page lists no item to download")
    downloads = items[0].get("downloads")
    if not isinstance(downloads, Mapping):
        raise BandcampUnavailable("the release's download page lists no formats")
    offers: dict[str, str] = {}
    untrusted = 0
    for encoding, offer in downloads.items():
        link = offer.get("url") if isinstance(offer, Mapping) else None
        if not isinstance(link, str):
            continue
        if trusted(link):
            offers[str(encoding)] = link
        else:
            untrusted += 1
    if untrusted and not offers:
        raise BandcampUnavailable(
            "the release's download links do not lead to Bandcamp over https, so "
            "none was asked"
        )
    return offers


#: The object inside the stat answer, which arrives as plain JSON or wrapped in
#: the page's own callback, ``if ( window.Downloads ) { Downloads.statResult ( {...} ) };``.
_STAT_CALL = re.compile(r"statResult\s*\(\s*(?P<answer>\{.*\})\s*\)", re.DOTALL)


def _stat_answer(text: str) -> Any:
    """The stat answer's object, or None when the text holds none."""
    found = _STAT_CALL.search(text)
    for candidate in (found.group("answer") if found else None, text.strip()):
        if not candidate:
            continue
        try:
            return json.loads(candidate)
        except ValueError:
            continue
    return None


def _prepared(transport: Transport, cookie: str, link: str) -> str:
    """The link to stream, after asking Bandcamp whether the file is ready.

    A release is built into its archive on request, and Bandcamp's own page asks
    the ``statdownload`` twin of the link before it fetches. An answer that says
    the file is not ready is a retry, never a download of whatever came back.
    An answer this client cannot read leaves the link as it was, which is the
    link a browser follows, and the archive is checked when it arrives.
    """
    parts = urlsplit(link)
    if "/download/" not in parts.path or not trusted(link):
        return link
    stat = urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path.replace("/download/", "/statdownload/", 1),
            f"{parts.query}&.vrs=1" if parts.query else ".vrs=1",
            "",
        )
    )
    response = transport.get(stat, cookie=cookie)
    if response.status in REJECTED_STATUSES:
        raise SessionRejected("Bandcamp refused the session while preparing the release")
    if response.status != 200:
        return link
    answer = _stat_answer(response.text)
    if not isinstance(answer, Mapping):
        return link
    if answer.get("result") != "ok":
        raise BandcampUnavailable("Bandcamp has not finished preparing the release")
    ready = answer.get("download_url") or answer.get("retry_url")
    return ready if isinstance(ready, str) and trusted(ready) else link


def fetch(transport: Transport, cookie: str, link: str, holding: Path) -> Path:
    """Stream one release into ``holding`` and return the file that arrived.

    A link that is not :func:`trusted` is refused before any request, since the
    request would carry the session to it.
    """
    if not trusted(link):
        raise BandcampUnavailable("the release's link does not lead to Bandcamp over https")
    holding.mkdir(parents=True, exist_ok=True)
    return transport.download(_prepared(transport, cookie, link), holding, cookie=cookie)


def unpack(landed: Path, into: Path) -> tuple[Path, ...]:
    """The audio files of one release, extracted flat into ``into``.

    A release arrives as one archive, a single track as the file itself. Each
    member of an archive is reduced to its base name, so a member naming a
    folder, or a path outside ``into``, lands inside ``into`` or nowhere. A name
    that arrives twice in one archive is refused, since keeping either copy
    would be a guess about which one the release meant.
    """
    into.mkdir(parents=True, exist_ok=True)
    if not zipfile.is_zipfile(landed):
        if landed.suffix.lower() not in AUDIO_SUFFIXES:
            raise BandcampUnavailable(
                f"the release arrived as {landed.name!r}, which is neither an archive "
                f"nor an audio file"
            )
        target = into / landed.name
        landed.replace(target)
        return (target,)
    extracted: list[Path] = []
    try:
        with zipfile.ZipFile(landed) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                name = PurePosixPath(member.filename.replace("\\", "/")).name
                if not name or name.startswith(".") or Path(name).suffix.lower() not in AUDIO_SUFFIXES:
                    continue
                target = into / name
                if target.exists():
                    raise BandcampUnavailable(
                        f"the release's archive holds {name!r} twice, so neither copy was kept"
                    )
                with archive.open(member) as source, target.open("xb") as written:
                    shutil.copyfileobj(source, written)
                extracted.append(target)
    except zipfile.BadZipFile:
        raise BandcampUnavailable("the release's archive could not be read") from None
    landed.unlink()
    return tuple(sorted(extracted))


# ---------------------------------------------------------------------------
# The transport that reaches the network
# ---------------------------------------------------------------------------

#: The browser ``curl_cffi`` presents. Bandcamp answers a plain client with a
#: bot check, which this product never works around any other way.
IMPERSONATE = "chrome"

#: Seconds to wait for an answer to begin.
TIMEOUT_S = 60

def _disposition_name(headers: Mapping[str, str]) -> str:
    """The file name a download's ``Content-Disposition`` gives, as a base name.

    Read by the standard library's header parser, which knows the quoted and the
    encoded forms, so a name holding an apostrophe or a semicolon arrives whole.
    """
    for key, value in headers.items():
        if key.lower() != "content-disposition":
            continue
        parsed = Message()
        parsed["content-disposition"] = value or ""
        given = parsed.get_filename() or ""
        name = PurePosixPath(given.replace("\\", "/")).name
        if name and not name.startswith("."):
            return name
    return ""


class CurlTransport:
    """The real transport: ``curl_cffi`` with a browser's fingerprint.

    EVERY EXCEPTION IS REPLACED, NOT CHAINED. A ``curl_cffi`` error names the
    address it failed on, and an address here is a signed link, so its text
    must not reach a message, a cause or a traceback.
    """

    def __init__(self) -> None:
        from curl_cffi import requests as curl_requests  # noqa: PLC0415 - the network seam

        self._session = curl_requests.Session(impersonate=IMPERSONATE)

    def _headers(self, cookie: str) -> dict[str, str]:
        return {"Cookie": cookie}

    def get(self, url: str, *, cookie: str) -> Response:
        try:
            answer = self._session.get(url, headers=self._headers(cookie), timeout=TIMEOUT_S)
            return Response(answer.status_code, answer.text, dict(answer.headers))
        except Exception as exc:  # noqa: BLE001 - replaced so its text cannot leak a link
            failure = type(exc).__name__
        raise BandcampUnavailable(f"a request to Bandcamp failed ({failure})")

    def post_json(self, url: str, payload: Mapping[str, Any], *, cookie: str) -> Response:
        try:
            answer = self._session.post(
                url, json=dict(payload), headers=self._headers(cookie), timeout=TIMEOUT_S
            )
            return Response(answer.status_code, answer.text, dict(answer.headers))
        except Exception as exc:  # noqa: BLE001 - replaced so its text cannot leak a link
            failure = type(exc).__name__
        raise BandcampUnavailable(f"a request to Bandcamp failed ({failure})")

    def download(self, url: str, directory: Path, *, cookie: str) -> Path:
        failure = ""
        try:
            answer = self._session.get(
                url, headers=self._headers(cookie), timeout=TIMEOUT_S, stream=True
            )
            try:
                if answer.status_code in REJECTED_STATUSES:
                    raise SessionRejected("Bandcamp refused the session on the release's file")
                if answer.status_code != 200:
                    raise BandcampUnavailable(
                        f"Bandcamp answered {answer.status_code} for the release's file"
                    )
                target = directory / (_disposition_name(dict(answer.headers)) or "release.zip")
                with target.open("wb") as written:
                    for chunk in answer.iter_content():
                        written.write(chunk)
                return target
            finally:
                answer.close()
        except BandcampError:
            raise
        except Exception as exc:  # noqa: BLE001 - replaced so its text cannot leak a link
            failure = type(exc).__name__
        raise BandcampUnavailable(f"the release's download failed ({failure})")


__all__ = [
    "AUDIO_SUFFIXES",
    "BASE",
    "BandcampError",
    "BandcampUnavailable",
    "Collection",
    "CurlTransport",
    "FormatUnavailable",
    "HIDDEN_PATH",
    "ITEMS_PATH",
    "LOSSLESS_ENCODING",
    "LOSSLESS_ENCODINGS",
    "LOSSY_ENCODING",
    "PAGE_SIZE",
    "Purchase",
    "Response",
    "SUMMARY_PATH",
    "SessionRejected",
    "Track",
    "TRUSTED_HOSTS",
    "Transport",
    "download_offers",
    "fetch",
    "newest_first",
    "read_collection",
    "seller_of",
    "trusted",
    "unpack",
]
