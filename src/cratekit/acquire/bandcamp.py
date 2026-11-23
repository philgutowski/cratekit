"""Bandcamp: the account's purchases, read from the account's own endpoints (U176).

Lists what the account holds and fetches one release; what to fetch and where
it goes is :mod:`cratekit.acquire.bandcamp_cli`'s. Two endpoints are written here
rather than taking ``bandcampsync``, whose state file is a checkpoint and whose
log carries part of the session.

The session and every signed link are credentials, so neither reaches a message,
a ``repr``, a log line or anything serialized, and transport exceptions are
replaced rather than chained, since their text names the address. The network
seam is :class:`Transport`; :class:`CurlTransport` imports ``curl_cffi``, for a
browser's fingerprint past the bot check, only when built.
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

#: Purchases asked for a page.
PAGE_SIZE = 100

#: The most pages one listing reads, bounding a token that moves forever.
MAX_PAGES = 1000

#: FLAC is the lossless format asked for; MP3 at 320 the marked lossy fallback.
LOSSLESS_ENCODING = "flac"
LOSSY_ENCODING = "mp3-320"

#: Every lossless format a release may offer, in the order one is taken.
LOSSLESS_ENCODINGS = (LOSSLESS_ENCODING, "alac", "aiff-lossless", "wav")

#: Statuses that judge the SESSION, as against the request.
REJECTED_STATUSES = frozenset({401, 403})

#: The suffix of a seller account's own address.
_ACCOUNT_HOST = ".bandcamp.com"

#: The only hosts, over https, a request may go to, since every request carries the session.
TRUSTED_HOSTS = ("bandcamp.com", "bcbits.com")

#: Audio suffixes; anything else in a release stays in the holding folder.
AUDIO_SUFFIXES = frozenset({".flac", ".mp3", ".aiff", ".aif", ".wav", ".m4a", ".ogg"})

_BLOB = re.compile(r"""data-blob\s*=\s*(["'])(?P<blob>.*?)\1""", re.DOTALL)


class BandcampError(Exception):
    """Base for every failure here. Its message never carries a link or a cookie."""


class SessionRejected(BandcampError):
    """The session is expired, logged out or refused: the person signs in again."""


class BandcampUnavailable(BandcampError):
    """Bandcamp did not answer, or answered in a shape this client cannot read."""


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
    """One purchase; ``download_page`` is a credential, kept out of ``to_json``, repr and ==."""

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
            "item_id": self.item_id, "seller": self.seller, "artist": self.artist,
            "title": self.title, "item_type": self.item_type, "purchased": self.purchased,
            "item_url": self.item_url, "hidden": self.hidden, "preorder": self.preorder,
            "downloadable": self.downloadable, "tracks": [track.to_json() for track in self.tracks],
        }


@dataclass(frozen=True, slots=True)
class Collection:
    """Every purchase the account holds, hidden ones included, newest first."""

    fan_id: str
    purchases: tuple[Purchase, ...]


def _json(response: Response, what: str) -> Any:
    """The body of a JSON answer; a rejected session raises, never reads as an empty account."""
    if response.status in REJECTED_STATUSES:
        raise SessionRejected(f"Bandcamp refused the session when asked for {what}")
    if response.status != 200:
        raise BandcampUnavailable(f"Bandcamp answered {response.status} when asked for {what}")
    try:
        return json.loads(response.text)
    except ValueError:
        raise BandcampUnavailable(f"Bandcamp's answer for {what} is not JSON") from None


def seller_of(item_url: str) -> str:
    """The seller account of a purchase, its address's host less ``.bandcamp.com``."""
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
                artist=str(entry.get("artist") or "").strip(), title=title,
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
        item_id=str(item.get("item_id") or tralbum or sale), seller=seller_of(item_url),
        artist=str(item.get("band_name") or "").strip(),
        title=str(item.get("item_title") or "").strip(), item_type=str(item.get("item_type") or ""),
        purchased=str(item.get("purchased") or ""), item_url=item_url,
        tracks=_tracks(listed.get(tralbum) if isinstance(listed, Mapping) else None), hidden=hidden,
        preorder=bool(item.get("is_preorder")),
        download_page=str(links.get(sale) or "") if isinstance(links, Mapping) else "",
    )


def _pages(
    transport: Transport, cookie: str, fan_id: str, path: str, *, hidden: bool, start: str
) -> Iterator[Purchase]:
    """Every purchase one listing holds, a page at a time. No checkpoint: resuming
    where the last run stopped would hide every older purchase."""
    token = start
    seen = {token}
    what = "the hidden purchases" if hidden else "the collection"
    for _ in range(MAX_PAGES):
        page = _json(
            transport.post_json(
                BASE + path, {"fan_id": fan_id, "older_than_token": token, "count": PAGE_SIZE},
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
            # Read as the end, it would call every older purchase absent.
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
    """Newest first; an unreadable date keeps its listed place after every dated one."""
    order = []
    for position, purchase in enumerate(purchases):
        stamp = _when(purchase)
        order.append(((0, -stamp) if stamp is not None else (1, 0.0), position, purchase))
    return tuple(purchase for *_key, purchase in sorted(order, key=lambda row: row[:2]))


def read_collection(transport: Transport, cookie: str, *, now: float | None = None) -> Collection:
    """Every purchase, hidden ones marked, newest first. A summary naming no fan is
    :class:`SessionRejected`, telling a logged out cookie from an empty account."""
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
    """Format to signed link (a credential) for one signed download page.

    A page offering no trusted link raises rather than read as an empty offer, which
    would ask the person to relax the lossless policy over a release offering FLAC.
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


#: The stat answer's object, plain or wrapped in the page's ``statResult`` callback.
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
    """The link to stream, once its ``statdownload`` twin says the archive is built.
    Not ready is a retry; an unreadable answer leaves the link a browser follows."""
    parts = urlsplit(link)
    if "/download/" not in parts.path or not trusted(link):
        return link
    stat = urlunsplit(
        (
            parts.scheme, parts.netloc, parts.path.replace("/download/", "/statdownload/", 1),
            f"{parts.query}&.vrs=1" if parts.query else ".vrs=1", "",
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
    """Stream one release into ``holding``; an untrusted link is never requested."""
    if not trusted(link):
        raise BandcampUnavailable("the release's link does not lead to Bandcamp over https")
    holding.mkdir(parents=True, exist_ok=True)
    return transport.download(_prepared(transport, cookie, link), holding, cookie=cookie)


def unpack(landed: Path, into: Path) -> tuple[Path, ...]:
    """The audio files of one release, flat in ``into``. A member keeps only its base
    name, so none lands outside; a name twice in one archive is refused as a guess."""
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


#: The browser ``curl_cffi`` presents, past the bot check a plain client meets.
IMPERSONATE = "chrome"

#: Seconds to wait for an answer to begin.
TIMEOUT_S = 60

def _disposition_name(headers: Mapping[str, str]) -> str:
    """The base name a ``Content-Disposition`` gives, parsed by the standard library."""
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
    """The real transport; exceptions are replaced, not chained, as they name a signed link."""

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
    "AUDIO_SUFFIXES", "BASE", "BandcampError", "BandcampUnavailable", "Collection", "CurlTransport",
    "HIDDEN_PATH", "ITEMS_PATH", "LOSSLESS_ENCODING", "LOSSLESS_ENCODINGS",
    "LOSSY_ENCODING", "PAGE_SIZE", "Purchase", "Response", "SUMMARY_PATH", "SessionRejected",
    "Track", "TRUSTED_HOSTS", "Transport", "download_offers", "fetch", "newest_first",
    "read_collection", "seller_of", "trusted", "unpack",
]
