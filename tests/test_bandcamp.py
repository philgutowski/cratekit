"""U176: the Bandcamp client reads the account's purchases and fetches one release.

The account is :class:`tests.bandcamp_fakes.FakeAccount`, which answers the
three requests in the shapes sitting 46 measured. NO TEST REACHES BANDCAMP: the
shipped transport is never built here, and the suite's autouse guard refuses it
everywhere else.

D1 applies. No real person, seller or release is named.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from cratekit.acquire import bandcamp
from tests.bandcamp_fakes import COOKIE, FAN_ID, SIGNED, FakeAccount, archive, download_page, item

NOW = 1_800_000_000


def four(**extra) -> list[dict]:
    return [
        item("1", seller="northlabel", artist="Aurora Bloom", title="Sun Path",
             purchased="27 Oct 2026 10:00:00 GMT", tracks=[("", "Sun Path"), ("", "Tide")], **extra),
        item("2", seller="southlabel", artist="Nova Reef", title="Low Light",
             purchased="20 Oct 2026 10:00:00 GMT", tracks=[("", "Low Light")]),
        item("3", seller="northlabel", artist="Various", title="Compiled",
             purchased="12 Oct 2026 10:00:00 GMT",
             tracks=[("Aurora Bloom", "Glass"), ("Nova Reef", "Shore")]),
        item("4", seller="eastlabel", artist="Coral Arc", title="Drift",
             purchased="01 Oct 2026 10:00:00 GMT", tracks=[("", "Drift")]),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# Listing the collection
# ═══════════════════════════════════════════════════════════════════════════


def test_a_collection_of_three_pages_ends_on_the_empty_page():
    account = FakeAccount(four(), page_size=2)
    found = bandcamp.read_collection(account, COOKIE, now=NOW)
    assert found.fan_id == FAN_ID
    assert [one.item_id for one in found.purchases] == ["1", "2", "3", "4"]
    pages = [payload for url, payload in account.posted if url.endswith(bandcamp.ITEMS_PATH)]
    assert len(pages) == 3, "two full pages and the empty one that ends the listing"
    assert pages[0]["older_than_token"] == f"{NOW}::a::"
    assert pages[1]["older_than_token"] == "tok2"
    assert pages[2]["older_than_token"] == "tok4"
    assert all(page["fan_id"] == FAN_ID and page["count"] == bandcamp.PAGE_SIZE for page in pages)


def test_each_purchase_carries_its_seller_from_the_host_and_its_track_list():
    found = bandcamp.read_collection(FakeAccount(four()), COOKIE, now=NOW)
    first = found.purchases[0]
    assert first.seller == "northlabel"
    assert first.artist == "Aurora Bloom" and first.title == "Sun Path"
    assert [(t.number, t.title) for t in first.tracks] == [(1, "Sun Path"), (2, "Tide")]
    compiled = found.purchases[2]
    assert [(t.artist, t.title) for t in compiled.tracks] == [("Aurora Bloom", "Glass"), ("Nova Reef", "Shore")]
    assert first.downloadable


def test_a_seller_on_its_own_domain_keeps_the_whole_host():
    assert bandcamp.seller_of("https://music.example.org/album/x") == "music.example.org"
    assert bandcamp.seller_of("https://PulsLabel.bandcamp.com/album/x") == "pulslabel"


def test_the_purchases_are_newest_first_whatever_order_the_pages_held():
    shuffled = list(reversed(four()))
    found = bandcamp.read_collection(FakeAccount(shuffled), COOKIE, now=NOW)
    assert [one.item_id for one in found.purchases] == ["1", "2", "3", "4"]


def test_a_purchase_with_an_unreadable_date_follows_every_dated_one():
    items = four()
    items[0]["purchased"] = "sometime"
    found = bandcamp.read_collection(FakeAccount(items), COOKIE, now=NOW)
    assert [one.item_id for one in found.purchases] == ["2", "3", "4", "1"]


def test_a_preorder_and_a_purchase_with_no_link_are_not_downloadable():
    items = [
        item("5", seller="northlabel", artist="A", title="Soon", purchased="27 Oct 2026 10:00:00 GMT",
             preorder=True),
        item("6", seller="northlabel", artist="A", title="Shirt", purchased="26 Oct 2026 10:00:00 GMT",
             item_type="package", downloadable=False),
    ]
    found = bandcamp.read_collection(FakeAccount(items), COOKIE, now=NOW)
    assert [one.downloadable for one in found.purchases] == [False, False]
    assert found.purchases[0].preorder


def test_hidden_purchases_are_read_and_marked():
    hidden = [item("9", seller="westlabel", artist="B", title="Hid", purchased="15 Oct 2026 10:00:00 GMT")]
    found = bandcamp.read_collection(FakeAccount(four(), hidden=hidden), COOKIE, now=NOW)
    marked = {one.item_id: one.hidden for one in found.purchases}
    assert marked["9"] is True and marked["1"] is False
    assert [one.item_id for one in found.purchases] == ["1", "2", "9", "3", "4"]


def test_an_expired_session_is_rejected_never_an_empty_collection():
    with pytest.raises(bandcamp.SessionRejected):
        bandcamp.read_collection(FakeAccount(four(), expired=True), COOKIE, now=NOW)


def test_a_session_the_summary_names_but_the_pages_refuse_is_rejected():
    class Refusing(FakeAccount):
        def post_json(self, url, payload, *, cookie):
            return bandcamp.Response(403, "forbidden")

    with pytest.raises(bandcamp.SessionRejected):
        bandcamp.read_collection(Refusing(four()), COOKIE, now=NOW)


def test_a_page_with_items_and_no_way_on_refuses_rather_than_ending():
    class Stuck(FakeAccount):
        def _page(self, items, end, *, more):
            page = super()._page(items, end, more=more)
            page["last_token"] = None
            return page

    with pytest.raises(bandcamp.BandcampUnavailable, match="older than it"):
        bandcamp.read_collection(Stuck(four(), page_size=2), COOKIE, now=NOW)


def test_a_page_that_repeats_its_token_refuses_rather_than_looping():
    class Repeating(FakeAccount):
        def _page(self, items, end, *, more):
            page = super()._page(items, end, more=more)
            page["last_token"] = "tok2"
            return page

    with pytest.raises(bandcamp.BandcampUnavailable):
        bandcamp.read_collection(Repeating(four(), page_size=2), COOKIE, now=NOW)


def test_a_server_failure_is_unavailable_not_rejected():
    class Down(FakeAccount):
        def get(self, url, *, cookie):
            return bandcamp.Response(503, "down")

    with pytest.raises(bandcamp.BandcampUnavailable) as caught:
        bandcamp.read_collection(Down(four()), COOKIE, now=NOW)
    assert not isinstance(caught.value, bandcamp.SessionRejected)


# ═══════════════════════════════════════════════════════════════════════════
# The signed page never serializes
# ═══════════════════════════════════════════════════════════════════════════


def test_the_signed_page_stays_out_of_the_json_and_the_repr():
    found = bandcamp.read_collection(FakeAccount(four()), COOKIE, now=NOW)
    first = found.purchases[0]
    assert first.download_page == download_page("1")
    assert SIGNED not in json.dumps(first.to_json())
    assert SIGNED not in repr(first)
    assert SIGNED not in repr(found)


# ═══════════════════════════════════════════════════════════════════════════
# Fetching one release
# ═══════════════════════════════════════════════════════════════════════════


def test_the_offers_are_read_from_the_pages_data_blob():
    account = FakeAccount(four())
    offers = bandcamp.download_offers(account, COOKIE, download_page("1"))
    assert set(offers) == {"flac", "mp3-320"}
    assert "enc=flac" in offers["flac"]


def test_a_page_with_no_data_blob_is_unavailable():
    class Blank(FakeAccount):
        def get(self, url, *, cookie):
            return bandcamp.Response(200, "<html></html>")

    with pytest.raises(bandcamp.BandcampUnavailable):
        bandcamp.download_offers(Blank(), COOKIE, download_page("1"))


def test_the_download_page_refusing_the_session_is_rejected():
    with pytest.raises(bandcamp.SessionRejected):
        bandcamp.download_offers(FakeAccount(expired=True), COOKIE, download_page("1"))


def test_the_file_is_fetched_from_the_link_the_stat_answer_names(tmp_path):
    account = FakeAccount(archives={"1": archive({"a.flac": b"x"})})
    offers = bandcamp.download_offers(account, COOKIE, download_page("1"))
    landed = bandcamp.fetch(account, COOKIE, offers["flac"], tmp_path / "hold")
    assert landed.parent == tmp_path / "hold"
    assert account.downloaded == [f"https://p4.bcbits.com/download/album?enc=flac&fsig={SIGNED}READY&id=1"]
    stat = [url for _method, url in account.requests if "/statdownload/" in url]
    assert stat and stat[0].endswith("&.vrs=1")


def test_a_stat_answer_that_is_not_ready_is_unavailable(tmp_path):
    class Busy(FakeAccount):
        def get(self, url, *, cookie):
            if "/statdownload/" in url:
                return bandcamp.Response(200, json.dumps({"result": "err"}))
            return super().get(url, cookie=cookie)

    account = Busy(archives={"1": archive({"a.flac": b"x"})})
    offers = bandcamp.download_offers(account, COOKIE, download_page("1"))
    with pytest.raises(bandcamp.BandcampUnavailable, match="not finished"):
        bandcamp.fetch(account, COOKIE, offers["flac"], tmp_path / "hold")
    assert account.downloaded == []


def test_an_unreadable_stat_answer_keeps_the_link_it_was_given(tmp_path):
    class Odd(FakeAccount):
        def get(self, url, *, cookie):
            if "/statdownload/" in url:
                return bandcamp.Response(200, "nothing here")
            return super().get(url, cookie=cookie)

    account = Odd(archives={"1": archive({"a.flac": b"x"})})
    offers = bandcamp.download_offers(account, COOKIE, download_page("1"))
    bandcamp.fetch(account, COOKIE, offers["flac"], tmp_path / "hold")
    assert account.downloaded == [offers["flac"]]


def test_unpack_flattens_audio_and_leaves_the_rest(tmp_path):
    landed = tmp_path / "release.zip"
    landed.write_bytes(
        archive({
            "A - B - 01 One.flac": b"1",
            "inner/A - B - 02 Two.flac": b"2",
            "../escape.flac": b"3",
            "cover.jpg": b"art",
            ".hidden.flac": b"4",
        })
    )
    into = tmp_path / "out"
    found = bandcamp.unpack(landed, into)
    assert sorted(path.name for path in found) == ["A - B - 01 One.flac", "A - B - 02 Two.flac", "escape.flac"]
    assert all(path.parent == into for path in found)
    assert not landed.exists()
    assert not (tmp_path / "escape.flac").exists()


def test_unpack_refuses_a_name_the_archive_holds_twice(tmp_path):
    landed = tmp_path / "release.zip"
    with zipfile.ZipFile(landed, "w") as written:
        written.writestr("x/One.flac", b"1")
        written.writestr("y/One.flac", b"2")
    with pytest.raises(bandcamp.BandcampUnavailable, match="twice"):
        bandcamp.unpack(landed, tmp_path / "out")


def test_unpack_takes_a_single_track_as_the_file_itself(tmp_path):
    landed = tmp_path / "A - One.flac"
    landed.write_bytes(b"1")
    found = bandcamp.unpack(landed, tmp_path / "out")
    assert found == (tmp_path / "out" / "A - One.flac",)


def test_unpack_refuses_a_file_that_is_neither_archive_nor_audio(tmp_path):
    landed = tmp_path / "page.html"
    landed.write_text("<html>")
    with pytest.raises(bandcamp.BandcampUnavailable):
        bandcamp.unpack(landed, tmp_path / "out")


def test_the_content_disposition_name_is_reduced_to_a_base_name():
    name = bandcamp._disposition_name({"Content-Disposition": 'attachment; filename="../A - B.zip"'})
    assert name == "A - B.zip"
    assert bandcamp._disposition_name({}) == ""
    encoded = bandcamp._disposition_name({"content-disposition": "attachment; filename*=UTF-8''A%20B.zip"})
    assert encoded == "A B.zip"


def test_the_real_transport_replaces_an_exception_whose_text_names_the_link(monkeypatch):
    """A curl error names the address it failed on, and that address is signed."""

    class Exploding:
        def get(self, url, **_kwargs):
            raise RuntimeError(f"curl: (28) timed out fetching {url}")

        post = get

    transport = bandcamp.CurlTransport.__new__(bandcamp.CurlTransport)
    transport._session = Exploding()
    link = f"https://p4.bcbits.com/download/album?fsig={SIGNED}1"
    for call in (
        lambda: transport.get(link, cookie=COOKIE),
        lambda: transport.post_json(link, {}, cookie=COOKIE),
        lambda: transport.download(link, Path("/nonexistent"), cookie=COOKIE),
    ):
        with pytest.raises(bandcamp.BandcampUnavailable) as caught:
            call()
        assert SIGNED not in str(caught.value)
        assert caught.value.__cause__ is None and caught.value.__context__ is None


# ═══════════════════════════════════════════════════════════════════════════
# Review round one: each guard driven alone
# ═══════════════════════════════════════════════════════════════════════════


def test_a_repeated_token_is_refused_at_once_not_after_every_page_allowed():
    class Repeating(FakeAccount):
        def _page(self, items, end, *, more):
            page = super()._page(items, end, more=more)
            page["last_token"] = "tok2"
            return page

    account = Repeating(four(), page_size=2)
    with pytest.raises(bandcamp.BandcampUnavailable):
        bandcamp.read_collection(account, COOKIE, now=NOW)
    assert len(account.posted) == 2


def test_a_summary_naming_no_fan_is_rejected_even_when_the_pages_would_answer():
    class Anonymous(FakeAccount):
        def get(self, url, *, cookie):
            if url.endswith(bandcamp.SUMMARY_PATH):
                return bandcamp.Response(200, json.dumps({"fan_id": None}))
            return super().get(url, cookie=cookie)

    account = Anonymous(four())
    with pytest.raises(bandcamp.SessionRejected):
        bandcamp.read_collection(account, COOKIE, now=NOW)
    assert account.posted == []


@pytest.mark.parametrize(
    "page", [{}, {"items": None}, {"error": False}, {"items": "x"}], ids=["empty", "null", "no-items", "not-a-list"]
)
def test_a_page_holding_no_list_of_items_is_unavailable_never_the_end(page):
    class Shapeless(FakeAccount):
        def post_json(self, url, payload, *, cookie):
            return bandcamp.Response(200, json.dumps(page))

    with pytest.raises(bandcamp.BandcampUnavailable):
        bandcamp.read_collection(Shapeless(four()), COOKIE, now=NOW)


def test_a_page_answering_with_an_error_is_rejected():
    class Erroring(FakeAccount):
        def post_json(self, url, payload, *, cookie):
            return bandcamp.Response(200, json.dumps({"error": True, "error_message": "no"}))

    with pytest.raises(bandcamp.SessionRejected):
        bandcamp.read_collection(Erroring(four()), COOKIE, now=NOW)


def test_a_purchase_in_both_listings_is_read_once():
    items = four()
    found = bandcamp.read_collection(FakeAccount(items, hidden=[items[1]]), COOKIE, now=NOW)
    assert [one.item_id for one in found.purchases] == ["1", "2", "3", "4"]
    assert not found.purchases[1].hidden


@pytest.mark.parametrize(
    "link",
    [
        "http://p4.bcbits.com/download/album?enc=flac&id=1",
        "https://elsewhere.example/download/album?enc=flac&id=1",
        "https://bcbits.com.elsewhere.example/download/album?id=1",
    ],
    ids=["plain-http", "other-host", "lookalike-host"],
)
def test_the_session_is_never_sent_to_a_link_outside_bandcamp(tmp_path, link):
    class Elsewhere(FakeAccount):
        def get(self, url, *, cookie):
            answer = super().get(url, cookie=cookie)
            return bandcamp.Response(answer.status, answer.text.replace(
                html_escape("https://p4.bcbits.com/download/album"), html_escape(link.split("?")[0])
            ))

    account = Elsewhere(archives={"1": archive({"a.flac": b"x"})})
    offers = bandcamp.download_offers(account, COOKIE, download_page("1"))
    assert offers == {}
    with pytest.raises(bandcamp.BandcampUnavailable):
        bandcamp.fetch(account, COOKIE, link, tmp_path / "hold")
    assert account.downloaded == []
    assert not any(url.startswith(link.split("?")[0]) for _method, url in account.requests)


def html_escape(text: str) -> str:
    import html

    return html.escape(text, quote=True)


def test_a_stat_answer_naming_a_link_outside_bandcamp_is_not_followed(tmp_path):
    class Redirecting(FakeAccount):
        def get(self, url, *, cookie):
            if "/statdownload/" in url:
                answer = {"result": "ok", "download_url": "https://elsewhere.example/f.zip"}
                return bandcamp.Response(200, json.dumps(answer))
            return super().get(url, cookie=cookie)

    account = Redirecting(archives={"1": archive({"a.flac": b"x"})})
    offers = bandcamp.download_offers(account, COOKIE, download_page("1"))
    bandcamp.fetch(account, COOKIE, offers["flac"], tmp_path / "hold")
    assert account.downloaded == [offers["flac"]]


def test_the_stat_request_refusing_the_session_is_rejected(tmp_path):
    class Expiring(FakeAccount):
        def get(self, url, *, cookie):
            if "/statdownload/" in url:
                return bandcamp.Response(403, "forbidden")
            return super().get(url, cookie=cookie)

    account = Expiring(archives={"1": archive({"a.flac": b"x"})})
    offers = bandcamp.download_offers(account, COOKIE, download_page("1"))
    with pytest.raises(bandcamp.SessionRejected):
        bandcamp.fetch(account, COOKIE, offers["flac"], tmp_path / "hold")


@pytest.mark.parametrize(
    "header, name",
    [
        ('attachment; filename="Coral Arc - Don\'t Stop.flac"', "Coral Arc - Don't Stop.flac"),
        ('attachment; filename="A; B.flac"', "A; B.flac"),
        ('attachment; filename=".hidden.zip"', ""),
        ("attachment", ""),
    ],
    ids=["apostrophe", "semicolon", "leading-dot", "no-name"],
)
def test_the_content_disposition_name_arrives_whole(header, name):
    assert bandcamp._disposition_name({"Content-Disposition": header}) == name
