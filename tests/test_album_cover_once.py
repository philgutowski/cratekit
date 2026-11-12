"""U260. An album's one cover is fetched and encoded once in a folder sweep.

The speed survey of 2026-11-12 counted ten fetches of one address and ten
encodes of the same bytes for an album of ten files, each fetch paced at one to
one and a half seconds. The worker builds its picture seam once per file, so
the memory lives behind the per process binder, :func:`searchers.for_images`,
and beside the encoder, :func:`art.to_cdj_jpeg_remembered`, as the solutions
entry on queued workers says it must.

EVERY TEST HERE TAGS THROUGH THE BINDER, one ``for_images()`` per file as
``tagging.cli.handle`` asks for it, over the SHIPPED image fetch with only its
HTTP getter and its sleep replaced. A test that handed ``tag_one`` one closure
for the whole folder would prove the memory and say nothing about the verb.

WHAT MUST NOT MOVE is what each file carries. The control for that is today's
behaviour reproduced exactly: the same sweep with both memories dropped before
every file, which is one fetch and one encode per file, the shape the survey
measured. Every file's picture block and every result sentence must be the same
in both runs, byte for byte.
"""

from __future__ import annotations

import functools
import re
from pathlib import Path

import pytest

from cratekit.core import art
from cratekit.tagging import searchers, tag
from cratekit.tagging.tag import SearchHit
from tests.test_tagging_engine import SPECIFIC, _jpeg, blocks, place

ALBUM = "https://catalogue.invalid/album.jpg"
OTHER = "https://catalogue.invalid/other.jpg"
NOT_A_PICTURE = b"<html>not found</html>"


@functools.cache
def cover() -> bytes:
    """A source picture that is not 800 square, so every encode resizes."""
    return _jpeg(1000, 1000)


@functools.cache
def other_cover() -> bytes:
    return _jpeg(900, 700)


class _Response:
    def __init__(self, status_code: int, content: bytes = b"") -> None:
        self.status_code = status_code
        self.content = content
        self.text = ""
        self.headers = {}


class Host:
    """A fake image host: per address, its answers in order, the last repeated.

    An answer is the bytes of a 200, an int status, or an exception the
    transport raises. ``asked`` is every request that reached the host, which
    is the count the survey measured.
    """

    def __init__(self, answers: dict[str, list]) -> None:
        self.answers = {url: list(given) for url, given in answers.items()}
        self.asked: list[str] = []

    def __call__(self, url: str, headers: dict, timeout: float) -> _Response:
        self.asked.append(url)
        queue = self.answers[url]
        answer = queue.pop(0) if len(queue) > 1 else queue[0]
        if isinstance(answer, BaseException):
            raise answer
        if isinstance(answer, int):
            return _Response(answer)
        return _Response(200, answer)


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    from tests._containers import synth_container

    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def slept() -> list[float]:
    """Every pacer wait, and every backoff, the shipped fetch slept."""
    return []


def ship(monkeypatch, host: Host, slept: list[float]) -> None:
    """The shipped image fetch over ``host``, built where the binder builds it."""
    real = searchers.default_image_fetch
    monkeypatch.setattr(
        searchers, "default_image_fetch", lambda: real(get=host, sleep=slept.append)
    )


@pytest.fixture
def encodes(monkeypatch) -> list[bytes]:
    """Every call of the encoder, by the bytes it was handed."""
    made: list[bytes] = []
    real = art.to_cdj_jpeg

    def counting(data, *args, **kwargs):
        made.append(data)
        return real(data, *args, **kwargs)

    monkeypatch.setattr(art, "to_cdj_jpeg", counting)
    return made


def album(folder: Path, silence: Path, names, prefix: str = "") -> list[Path]:
    return [place(folder, silence, f"{prefix}{name}") for name in names]


def sweep(paths: list[Path], address_of, *, today: bool = False) -> list[tag.TagResult]:
    """Tag each file as the worker does, one binder call per file.

    ``today`` drops both memories before every file, which is what the code
    did before this unit: a fresh fetch and a fresh encode for each one.
    """
    results = []
    for path in paths:
        if today:
            searchers.reset_images()
            art.reset_cache()

        def searcher(artist: str, title: str, _path=path) -> SearchHit:
            return SearchHit(
                genre=SPECIFIC,
                source=searchers.BEATPORT,
                source_genre="deep house",
                art_url=address_of(_path),
            )

        results.append(tag.tag_one(path, searcher=searcher, fetch_image=searchers.for_images()))
    return results


def carried(path: Path) -> list[tuple]:
    """Everything a FLAC picture block says, the image bytes included."""
    return [
        (block.type, block.mime, block.desc, block.width, block.height, block.depth, block.data)
        for block in blocks(path)
    ]


def said(result: tag.TagResult) -> tuple[str, str]:
    """The result and its sentence, with the one part no two runs share masked.

    Pillow names the in memory buffer it could not read by its object address,
    which differs on every call, before this unit and after it alike.
    """
    return result.art_fetch, re.sub(r" at 0x[0-9a-f]+", " at 0x", result.art_fetch_detail)


TEN = [f"track{index:02d}" for index in range(10)]


# ═══════════════════════════════════════════════════════════════════════════
# One request and one encode for an album
# ═══════════════════════════════════════════════════════════════════════════


def test_ten_files_naming_one_address_make_one_request_one_wait_and_one_encode(
    tmp_path, silence, monkeypatch, slept, encodes
):
    host = Host({ALBUM: [cover()]})
    ship(monkeypatch, host, slept)
    paths = album(tmp_path / "Music", silence, TEN)

    results = sweep(paths, lambda _path: ALBUM)

    assert host.asked == [ALBUM]
    assert len(slept) == 1, "the pacer waits before the one request that was made"
    assert encodes == [cover()]
    assert [result.art_fetch for result in results] == [tag.ART_EMBEDDED] * 10
    for path in paths:
        ((kind, mime, _desc, width, height, depth, _data),) = carried(path)
        assert (kind, mime, width, height, depth) == (art.FRONT_COVER, art.JPEG_MIME, 800, 800, 24)


def test_every_file_carries_byte_for_byte_what_it_carried_before(
    tmp_path, silence, monkeypatch, slept, encodes
):
    """The merge blocker, measured. Today's run is the control, and its own
    counts are asserted so the control is known to be today's shape."""
    host = Host({ALBUM: [cover()]})
    ship(monkeypatch, host, slept)
    before = album(tmp_path / "before", silence, TEN)
    after = album(tmp_path / "after", silence, TEN)

    then = sweep(before, lambda _path: ALBUM, today=True)
    assert host.asked == [ALBUM] * 10
    assert len(slept) == 10
    assert len(encodes) == 10
    host.asked.clear()
    slept.clear()
    encodes.clear()
    searchers.reset_images()
    art.reset_cache()

    now = sweep(after, lambda _path: ALBUM)

    assert host.asked == [ALBUM]
    assert len(encodes) == 1
    assert [said(result) for result in now] == [said(result) for result in then]
    assert [carried(path) for path in after] == [carried(path) for path in before]
    expected = art.to_cdj_jpeg(cover()).data
    assert {carried(path)[0][-1] for path in after} == {expected}


def test_two_albums_in_one_folder_make_two_requests_and_two_encodes(
    tmp_path, silence, monkeypatch, slept, encodes
):
    """Interleaved, the order a flat folder of two albums sorts into."""
    host = Host({ALBUM: [cover()], OTHER: [other_cover()]})
    ship(monkeypatch, host, slept)
    paths = album(tmp_path / "Music", silence, TEN)
    address = {path: (ALBUM if index % 2 == 0 else OTHER) for index, path in enumerate(paths)}

    results = sweep(paths, address.__getitem__)

    assert host.asked == [ALBUM, OTHER]
    assert len(slept) == 2
    assert encodes == [cover(), other_cover()]
    assert [result.art_fetch for result in results] == [tag.ART_EMBEDDED] * 10
    first, second = (art.to_cdj_jpeg(source).data for source in (cover(), other_cover()))
    for path in paths:
        assert carried(path)[0][-1] == (first if address[path] == ALBUM else second)


# ═══════════════════════════════════════════════════════════════════════════
# A failure is never remembered
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "failure",
    [503, OSError("connection reset"), b""],
    ids=["a refusal", "a transport failure", "an empty answer"],
)
def test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next(
    tmp_path, silence, monkeypatch, slept, encodes, failure
):
    host = Host({ALBUM: [failure, cover()]})
    ship(monkeypatch, host, slept)
    paths = album(tmp_path / "Music", silence, ["a", "b", "c"])

    results = sweep(paths, lambda _path: ALBUM)

    assert host.asked == [ALBUM, ALBUM], "asked again after the failure, then remembered"
    assert len(slept) == 2
    assert said(results[0]) == (
        tag.ART_UNAVAILABLE,
        f"the picture at {ALBUM} could not be fetched",
    )
    assert carried(paths[0]) == []
    assert [result.art_fetch for result in results[1:]] == [tag.ART_EMBEDDED] * 2
    assert encodes == [cover()]


def test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did(
    tmp_path, silence, monkeypatch, slept, encodes
):
    """A decode failure is a failure: never remembered as an answer, asked for
    again on every file as today, and said in today's sentence on each."""
    host = Host({ALBUM: [NOT_A_PICTURE]})
    ship(monkeypatch, host, slept)
    before = album(tmp_path / "before", silence, ["a", "b", "c"])
    after = album(tmp_path / "after", silence, ["a", "b", "c"])

    then = sweep(before, lambda _path: ALBUM, today=True)
    host.asked.clear()
    encodes.clear()
    now = sweep(after, lambda _path: ALBUM)

    assert host.asked == [ALBUM] * 3
    assert encodes == [NOT_A_PICTURE] * 3
    assert [said(result) for result in now] == [said(result) for result in then]
    assert {result.art_fetch for result in now} == {tag.ART_UNAVAILABLE}
    assert "is not a usable picture" in now[0].art_fetch_detail
    assert all(carried(path) == [] for path in after)


def test_a_second_sweep_over_the_tagged_folder_fetches_nothing(
    tmp_path, silence, monkeypatch, slept, encodes
):
    host = Host({ALBUM: [cover()]})
    ship(monkeypatch, host, slept)
    paths = album(tmp_path / "Music", silence, ["a", "b", "c"])
    sweep(paths, lambda _path: ALBUM)
    host.asked.clear()
    encodes.clear()
    searchers.reset_images()
    art.reset_cache()

    again = sweep(paths, lambda _path: ALBUM)

    assert host.asked == []
    assert encodes == []
    assert [result.art_fetch for result in again] == [tag.ART_PRESENT] * 3


def test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode(
    tmp_path, silence, monkeypatch, slept, encodes
):
    """The fetch is remembered by its address and the encode by its bytes."""
    host = Host({ALBUM: [cover()], OTHER: [cover()]})
    ship(monkeypatch, host, slept)
    paths = album(tmp_path / "Music", silence, ["a", "b"])
    address = dict(zip(paths, (ALBUM, OTHER), strict=True))

    sweep(paths, address.__getitem__)

    assert host.asked == [ALBUM, OTHER]
    assert encodes == [cover()]
    assert carried(paths[0]) == carried(paths[1])


# ═══════════════════════════════════════════════════════════════════════════
# The two memories, each on its own terms
# ═══════════════════════════════════════════════════════════════════════════


def test_the_binder_hands_back_one_fetch_per_process_and_the_reset_drops_it(monkeypatch):
    def detonate(*args, **kwargs):
        raise AssertionError("the binder reached the network")

    monkeypatch.setattr(searchers, "_requests_get", detonate)
    first = searchers.for_images()
    assert searchers.for_images() is first
    searchers.reset_images()
    assert searchers.for_images() is not first


def test_a_fetch_that_raises_is_not_remembered():
    calls: list[str] = []

    def fetch(url: str) -> bytes | None:
        calls.append(url)
        if len(calls) == 1:
            raise OSError("reset")
        return cover()

    remembered = searchers.remembering(fetch)
    with pytest.raises(OSError):
        remembered(ALBUM)
    assert remembered(ALBUM) == cover()
    assert remembered(ALBUM) == cover()
    assert calls == [ALBUM, ALBUM]


def test_an_answer_the_admission_refuses_is_handed_on_and_not_remembered():
    calls: list[str] = []

    def fetch(url: str) -> bytes | None:
        calls.append(url)
        return NOT_A_PICTURE

    remembered = searchers.remembering(fetch, admit=art.decodes)
    assert remembered(ALBUM) == NOT_A_PICTURE
    assert remembered(ALBUM) == NOT_A_PICTURE
    assert calls == [ALBUM, ALBUM]


def test_an_empty_answer_handed_straight_in_is_not_remembered():
    """The shipped fetch turns an empty body into None; a seam that answers the
    empty bytes themselves must not have them kept as an answer either."""
    calls: list[str] = []

    def fetch(url: str) -> bytes | None:
        calls.append(url)
        return b"" if len(calls) == 1 else cover()

    remembered = searchers.remembering(fetch)
    assert remembered(ALBUM) == b""
    assert remembered(ALBUM) == cover()
    assert remembered(ALBUM) == cover()
    assert calls == [ALBUM, ALBUM]


def test_two_pictures_of_one_length_are_encoded_apart(encodes):
    """The digest is what tells two pictures apart, never their length alone.
    A JPEG decodes with bytes after its end marker, so the shorter of two
    covers is padded to the longer one's length."""
    one, two = cover(), other_cover()
    longer = max(len(one), len(two))
    one, two = (picture + b"\0" * (longer - len(picture)) for picture in (one, two))
    assert len(one) == len(two) and one != two

    first = art.to_cdj_jpeg_remembered(one)
    second = art.to_cdj_jpeg_remembered(two)

    assert encodes == [one, two]
    assert first.data != second.data


def test_two_covers_sharing_a_long_header_are_encoded_apart(encodes):
    """The digest is over every byte, not a prefix. Two covers carrying one
    embedded colour profile agree for thousands of bytes before their pixels
    differ, and are padded to one length too, so only the whole digest tells
    them apart. Round one of the review found a 2 KB prefix digest killed by
    nothing."""
    import io

    from tests.test_tagging_engine import _gradient

    profile = bytes(range(256)) * 12

    def saved(turn: int) -> bytes:
        buffer = io.BytesIO()
        _gradient(300, 300).rotate(turn).save(buffer, "JPEG", quality=85, icc_profile=profile)
        return buffer.getvalue()

    one, two = saved(0), saved(90)
    longer = max(len(one), len(two))
    one, two = (picture + b"\0" * (longer - len(picture)) for picture in (one, two))
    shared = next(index for index, (a, b) in enumerate(zip(one, two, strict=True)) if a != b)
    assert shared > len(profile), "the fixture must share more than its profile"

    first = art.to_cdj_jpeg_remembered(one)
    second = art.to_cdj_jpeg_remembered(two)

    assert encodes == [one, two]
    assert first.data != second.data

def test_the_encode_memory_drops_the_least_recently_used(monkeypatch, encodes):
    monkeypatch.setattr(art, "COVER_MEMORY", 2)
    third = _jpeg(600, 500)
    for picture in (cover(), other_cover(), cover(), third, cover()):
        art.to_cdj_jpeg_remembered(picture)
    # cover was used again before third arrived, so other_cover is the one dropped.
    assert encodes == [cover(), other_cover(), third]


def test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest():
    calls: list[str] = []

    def fetch(url: str) -> bytes | None:
        calls.append(url)
        return url.encode()

    remembered = searchers.remembering(fetch, keep=2)
    for url in ("a", "b", "a", "c", "a", "b"):
        assert remembered(url) == url.encode()
    # a and b held; a touched again so c evicts b; a still held; b asked again.
    assert calls == ["a", "b", "c", "b"]


def test_the_shipped_fetch_memory_is_bounded():
    assert 1 < searchers.IMAGE_MEMORY <= 8


def test_the_same_bytes_at_another_size_or_cap_are_encoded_again(encodes):
    first = art.to_cdj_jpeg_remembered(cover())
    assert art.to_cdj_jpeg_remembered(cover()) is first
    smaller = art.to_cdj_jpeg_remembered(cover(), size=400)
    capped = art.to_cdj_jpeg_remembered(cover(), max_bytes=art.ART_MAX_BYTES - 1)
    assert len(encodes) == 3
    assert (smaller.width, smaller.height) == (400, 400)
    assert first.data == art.to_cdj_jpeg(cover()).data
    assert capped.data == art.to_cdj_jpeg(cover(), max_bytes=art.ART_MAX_BYTES - 1).data


def test_different_bytes_are_encoded_apart(encodes):
    one = art.to_cdj_jpeg_remembered(cover())
    two = art.to_cdj_jpeg_remembered(other_cover())
    assert one.data != two.data
    assert len(encodes) == 2
    assert art.to_cdj_jpeg_remembered(cover()) is one


def test_a_picture_that_cannot_be_encoded_is_not_remembered(encodes):
    for _ in range(2):
        with pytest.raises(art.ArtError):
            art.to_cdj_jpeg_remembered(NOT_A_PICTURE)
    assert encodes == [NOT_A_PICTURE] * 2


def test_the_encode_memory_keeps_a_few_pictures_and_forgets_the_oldest(monkeypatch, encodes):
    monkeypatch.setattr(art, "COVER_MEMORY", 1)
    art.to_cdj_jpeg_remembered(cover())
    art.to_cdj_jpeg_remembered(other_cover())
    art.to_cdj_jpeg_remembered(cover())
    assert encodes == [cover(), other_cover(), cover()]


def test_the_shipped_encode_memory_is_bounded():
    assert 1 < art.COVER_MEMORY <= 8


def test_the_encode_reset_forgets(encodes):
    art.to_cdj_jpeg_remembered(cover())
    art.reset_cache()
    art.to_cdj_jpeg_remembered(cover())
    assert len(encodes) == 2
