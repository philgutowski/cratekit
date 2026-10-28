"""A Bandcamp account in memory, answering the client's three requests (U176).

Every address the fake serves is shaped like the real one, and every signed
part of it carries ``SIGNED`` so a test can look for it anywhere it must not
be. The session is ``COOKIE``, whose identity value carries ``IDENTITYVALUE``
for the same reason. NOTHING HERE REACHES A NETWORK.

D1 applies. No real person, seller or release is named.
"""

from __future__ import annotations

import html
import io
import json
import zipfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from cratekit.acquire import bandcamp

#: The identity value a leak test looks for.
IDENTITY = "7%09IDENTITYVALUE0123456789abcdef%09%7B%22id%22%3A1%7D"
COOKIE = f"client_id=ABC; identity={IDENTITY}; js_logged_in=1"

#: The part of every signed link a leak test looks for.
SIGNED = "SIGNED"

FAN_ID = "4242"


def download_page(item_id: str) -> str:
    return f"https://bandcamp.com/download?from=collection&payment_id=9{item_id}&sig={SIGNED}{item_id}&sitem_id={item_id}"


def file_link(item_id: str, encoding: str) -> str:
    return f"https://p4.bcbits.com/download/album?enc={encoding}&fsig={SIGNED}{item_id}&id={item_id}&ts=1"


def item(
    item_id: str,
    *,
    seller: str,
    artist: str,
    title: str,
    purchased: str,
    tracks: Sequence[tuple[str, str]] = (),
    item_type: str = "album",
    preorder: bool = False,
    downloadable: bool = True,
    host: str | None = None,
) -> dict[str, Any]:
    """One collection item as the endpoint answers it, with its track list."""
    return {
        "item_id": int(item_id),
        "item_type": item_type,
        "band_name": artist,
        "item_title": title,
        "item_url": f"https://{host or seller + '.bandcamp.com'}/album/{title.lower().replace(' ', '-')}",
        "purchased": purchased,
        "tralbum_type": "a",
        "tralbum_id": int(item_id) + 1000,
        "sale_item_type": "p",
        "sale_item_id": int(item_id) + 2000,
        "is_preorder": preorder,
        "label": None,
        "_tracks": [
            {"track_number": number, "artist": track_artist, "title": track_title}
            for number, (track_artist, track_title) in enumerate(tracks, start=1)
        ],
        "_downloadable": downloadable,
    }


def archive(files: Mapping[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as written:
        for name, data in files.items():
            written.writestr(name, data)
    return buffer.getvalue()


class FakeAccount:
    """The account: a collection, hidden purchases, and one archive per release.

    ``page_size`` splits the collection into pages the way the endpoint does, so
    a collection of four purchases at two a page is three requests, the last
    one answering an empty page.
    """

    def __init__(
        self,
        items: Sequence[dict[str, Any]] = (),
        *,
        hidden: Sequence[dict[str, Any]] = (),
        page_size: int = 100,
        archives: Mapping[str, bytes] | None = None,
        encodings: Sequence[str] = ("flac", "mp3-320"),
        expired: bool = False,
        cookie: str = COOKIE,
    ) -> None:
        self.items = list(items)
        self.hidden = list(hidden)
        self.page_size = page_size
        self.archives = dict(archives or {})
        self.encodings = tuple(encodings)
        self.expired = expired
        self.cookie = cookie
        self.requests: list[tuple[str, str]] = []
        self.posted: list[tuple[str, dict[str, Any]]] = []
        self.downloaded: list[str] = []

    # -- the three calls --------------------------------------------------

    def _signed_in(self, cookie: str) -> bool:
        return not self.expired and cookie == self.cookie

    def get(self, url: str, *, cookie: str) -> bandcamp.Response:
        self.requests.append(("GET", url))
        parts = urlsplit(url)
        if parts.path == bandcamp.SUMMARY_PATH:
            if not self._signed_in(cookie):
                return bandcamp.Response(200, json.dumps({"error": True, "error_message": "not logged in"}))
            return bandcamp.Response(
                200, json.dumps({"fan_id": int(FAN_ID), "collection_summary": {"username": "fan"}})
            )
        if parts.path == "/download":
            if not self._signed_in(cookie):
                return bandcamp.Response(403, "forbidden")
            item_id = parse_qs(parts.query)["sitem_id"][0]
            blob = {
                "digital_items": [
                    {
                        "downloads": {
                            encoding: {"url": file_link(item_id, encoding), "size_mb": "1MB"}
                            for encoding in self.encodings
                        }
                    }
                ]
            }
            page = f'<div id="pagedata" data-blob="{html.escape(json.dumps(blob), quote=True)}"></div>'
            return bandcamp.Response(200, f"<html><body>{page}</body></html>")
        if parts.path.startswith("/statdownload/"):
            query = parse_qs(parts.query)
            ready = (
                f"https://p4.bcbits.com/download/album?enc={query['enc'][0]}"
                f"&fsig={SIGNED}READY&id={query['id'][0]}"
            )
            answer = json.dumps({"result": "ok", "download_url": ready})
            return bandcamp.Response(200, f"if ( window.Downloads ) {{ Downloads.statResult ( {answer} ) }};")
        return bandcamp.Response(404, "not found")

    def post_json(self, url: str, payload: Mapping[str, Any], *, cookie: str) -> bandcamp.Response:
        self.posted.append((url, dict(payload)))
        if not self._signed_in(cookie):
            return bandcamp.Response(401, "unauthorized")
        path = urlsplit(url).path
        pool = self.items if path == bandcamp.ITEMS_PATH else self.hidden
        token = str(payload.get("older_than_token") or "")
        start = int(token[len("tok"):]) if token.startswith("tok") else 0
        page = pool[start : start + self.page_size]
        end = start + len(page)
        return bandcamp.Response(200, json.dumps(self._page(page, end, more=bool(page))))

    def download(self, url: str, directory: Path, *, cookie: str) -> Path:
        self.downloaded.append(url)
        item_id = parse_qs(urlsplit(url).query)["id"][0]
        target = directory / f"release {item_id}.zip"
        target.write_bytes(self.archives[item_id])
        return target

    # -- shaping a page ----------------------------------------------------

    def _page(self, items: list[dict[str, Any]], end: int, *, more: bool) -> dict[str, Any]:
        served = [{k: v for k, v in one.items() if not k.startswith("_")} for one in items]
        return {
            "items": served,
            "more_available": more,
            "last_token": f"tok{end}" if items else None,
            "tracklists": {f"a{one['tralbum_id']}": one["_tracks"] for one in items},
            "redownload_urls": {
                f"p{one['sale_item_id']}": download_page(str(one["item_id"]))
                for one in items
                if one["_downloadable"]
            },
        }


__all__ = [
    "COOKIE",
    "FAN_ID",
    "FakeAccount",
    "IDENTITY",
    "SIGNED",
    "archive",
    "download_page",
    "file_link",
    "item",
]
