"""R-1313. A 404 whose body is not JSON is still the provider saying it has nothing.

Found at the review of R-1305. The provider client decodes an error answer's
body inside its own handler of the HTTP error, so a 404 whose body is a page
never becomes the client's ``ObjectNotFound``: it surfaces as the decode error
with the 404 three context links down. Four readers of a not found read the
failure itself alone, so a track or a release the provider had nothing for was
retried, failed as the provider being unavailable, and asked again every run.

Every failure here is raised by the installed client's own request handler
(``tests.provider_answers``), not built by hand, so the chain is the client's.
The four readers: ``adapter.classify_unavailable``, the outbound account's
``_not_found`` (which asks it), ``isrc_cache.said_not_found`` and the
catalogue's ``_gone``.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from cratekit.acquire import adapter, isrc_cache
from cratekit.acquire.adapter import (
    AdapterSettings,
    NoFileLanded,
    Remedy,
    TrackOutcome,
    TrackRequest,
    acquire_one,
)
from cratekit.core import cause
from cratekit.core.cause import CratekitError
from cratekit.label import tidal_catalogue
from cratekit.modules.outbound import account as outbound_account
from cratekit.modules.outbound import tidal_account
from tests.provider_answers import HTML, NOT_FOUND_BODY, client_failure
from tests.test_isrc_cache import ONE, Client, Clock, single, stored
from tests.test_isrc_cache import account as isrc_account
from tests.test_isrc_cache import cache as isrc_cache_of
from tests.test_isrc_cache import catalogue as isrc_catalogue
from tests.test_label_tidal_catalogue import AlbumClient
from tests.test_provider_rejection_bodies import cyclic

#: A provider saying it has nothing, with a body the client can and cannot read.
NOT_FOUND = [
    pytest.param(404, HTML, id="404-html"),
    pytest.param(404, b"", id="404-empty"),
    pytest.param(404, NOT_FOUND_BODY, id="404-json"),
]

#: Answers that say nothing about the thing asked for, whatever their body.
UNAVAILABLE = [
    pytest.param(503, HTML, id="503-html"),
    pytest.param(502, HTML, id="502-html"),
    pytest.param(503, b"", id="503-empty"),
    pytest.param(500, NOT_FOUND_BODY, id="500-json"),
]


def classified(exc: BaseException) -> bool:
    return adapter.classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT


#: Each reader of a not found, as the question "is this failure a not found?"
READERS: dict[str, Callable[[BaseException], bool]] = {
    "classify_unavailable": classified,
    "account": tidal_account._not_found,
    "isrc_cache": isrc_cache.said_not_found,
    "catalogue": tidal_catalogue._gone,
}

READER_IDS = list(READERS)


def while_handling(first: Callable[[], Exception], later: Callable[[], Exception]) -> Exception:
    """``later``'s failure, raised while ``first``'s is being handled.

    A failure the client already raised is returned as it came, never raised
    again: raising an exception inside a handler sets its context to the
    handled one, which would cut the client's own chain off at the top and
    put ``first`` where the decode error's links were.
    """
    try:
        raise first()
    except Exception:  # noqa: BLE001 - the context is the point
        made = later()
        if made.__traceback__ is not None:
            return made
        try:
            raise made
        except Exception as exc:  # noqa: BLE001
            return exc
    raise AssertionError("unreachable")


def inside_a_refusal(later: Callable[[], Exception]) -> Exception:
    """``later``'s failure, raised while a product refusal raised from a 404 page is handled.

    The shape ``core.cause._chain`` refuses to read context over: a handler
    that caught a refusal and then met an unrelated failure. The refusal is
    raised FROM the 404, so the 404 is reachable under it and only the walk's
    refusal limit keeps it out.
    """
    gone = client_failure(404, HTML)
    refusal = outbound_account.provider_failure(gone, "look up the track 8")
    assert isinstance(refusal, CratekitError)
    try:
        raise refusal from gone
    except CratekitError:
        try:
            raise later()
        except Exception as exc:  # noqa: BLE001
            return exc
    raise AssertionError("unreachable")


# ═══════════════════════════════════════════════════════════════════════════
# 1. Each reader, on the failure the client raises
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("reader", READER_IDS)
@pytest.mark.parametrize(("status", "body"), NOT_FOUND)
def test_a_404_is_a_not_found_whatever_its_body(reader, status, body):
    assert READERS[reader](client_failure(status, body)) is True


@pytest.mark.parametrize("reader", READER_IDS)
@pytest.mark.parametrize(("status", "body"), UNAVAILABLE)
def test_a_server_error_is_never_a_not_found_whatever_its_body(reader, status, body):
    assert READERS[reader](client_failure(status, body)) is False


@pytest.mark.parametrize("reader", READER_IDS)
def test_a_server_error_met_while_handling_a_404_is_the_outage_it_says(reader):
    """The status nearest the failure is the provider's answer to it."""
    later = while_handling(lambda: client_failure(404, HTML), lambda: client_failure(503, HTML))

    assert READERS[reader](later) is False


@pytest.mark.parametrize("reader", READER_IDS)
def test_a_failure_met_while_handling_a_refusal_raised_from_a_404_is_not_a_not_found(reader):
    """A context link into a refusal the product raised is not followed."""
    later = inside_a_refusal(lambda: ValueError("the parse of an unrelated answer failed"))

    assert READERS[reader](later) is False


@pytest.mark.parametrize("reader", READER_IDS)
def test_a_rewrapped_404_page_is_a_not_found(reader):
    """A wrapper raised from the client's failure, as a caller's own code might."""
    try:
        raise RuntimeError("the read failed") from client_failure(404, HTML)
    except RuntimeError as exc:
        wrapped = exc

    assert READERS[reader](wrapped) is True


@pytest.mark.parametrize("reader", READER_IDS)
def test_a_cyclic_chain_ends_and_is_not_a_not_found(reader):
    assert READERS[reader](cyclic()) is False


def test_the_nearest_status_is_the_first_the_walk_reaches():
    assert cause.nearest_status(client_failure(404, HTML)) == 404
    assert cause.nearest_status(client_failure(503, b"")) == 503
    later = while_handling(lambda: client_failure(404, HTML), lambda: client_failure(503, HTML))
    assert cause.nearest_status(later) == 503
    assert cause.nearest_status(ValueError("no status anywhere")) is None


def a_wrapper_of_a_404_raised_while_handling_a_503() -> Exception:
    """A failure met while handling a wrapper raised FROM a 404 page while a 503 page was handled.

    The wrapper says it is the 404 and was merely raised while the 503 was
    being handled, so off the declared chain the walk reads a link's own
    declared cause before what it was handling (round one's review: the other
    order read the 503 first and every reader called the not found an outage).
    """
    outage = client_failure(503, HTML)
    gone = client_failure(404, HTML)
    try:
        raise outage
    except Exception:  # noqa: BLE001 - the context is the point
        try:
            raise RuntimeError("the read failed") from gone
        except RuntimeError:
            try:
                raise ValueError("a parse in the handler failed")
            except ValueError as exc:
                return exc
    raise AssertionError("unreachable")


def test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling():
    later = a_wrapper_of_a_404_raised_while_handling_a_503()

    assert cause.nearest_status(later) == 404
    assert {name: reader(later) for name, reader in READERS.items()} == dict.fromkeys(
        READERS, True
    )


def test_a_name_reached_only_as_context_is_not_a_not_found():
    """A status is the provider's word; a class reached only as context is a guess."""

    class ObjectNotFound(Exception):
        """Named as the provider client names its own not found."""

    later = while_handling(lambda: ObjectNotFound("gone"), lambda: ValueError("parse failed"))

    assert {name: reader(later) for name, reader in READERS.items()} == dict.fromkeys(
        READERS, False
    )


# ═══════════════════════════════════════════════════════════════════════════
# 2. Through each seam: answered once and remembered, or retried and never kept
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def clock() -> Clock:
    return Clock()


@pytest.mark.parametrize("seam", ["account", "catalogue"])
def test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept(clock, monkeypatch, seam):
    client = Client({ONE: client_failure(404, HTML)})
    made = isrc_cache_of(clock)

    def ask():
        if seam == "account":
            return isrc_account(client, made).match_track(identity="1", isrc=ONE)
        return isrc_catalogue(client, made, monkeypatch).tracks_for_isrc(ONE)

    assert ask() in (None, ())
    assert client.asked == [ONE]
    assert ask() in (None, ())

    assert client.asked == [ONE]
    assert stored()["entries"][f"{ONE}|GB"]["tracks"] == []


@pytest.mark.parametrize("seam", ["account", "catalogue"])
def test_an_isrc_answered_by_a_503_page_is_retried_and_never_kept(clock, monkeypatch, seam):
    client = Client({ONE: single()})
    client.failures = [client_failure(503, HTML) for _ in range(6)]
    made = isrc_cache_of(clock)

    def ask():
        if seam == "account":
            return isrc_account(client, made).match_track(identity="1", isrc=ONE)
        return isrc_catalogue(client, made, monkeypatch).tracks_for_isrc(ONE)

    with pytest.raises((CratekitError, ValueError)):
        ask()
    asked = len(client.asked)
    assert asked > 1, "an outage was answered without a retry"
    client.failures = []

    assert ask()
    assert len(client.asked) == asked + 1


def test_a_release_answered_by_a_404_page_is_gone_at_once(monkeypatch):
    waited: list[float] = []
    monkeypatch.setattr(tidal_catalogue, "_pause", waited.append)
    client = AlbumClient(client_failure(404, HTML))

    with pytest.raises(tidal_catalogue.ReleaseUnresolvable):
        tidal_catalogue.TidalCatalogue(client).release_tracks("r-gone")

    assert client.album_reads == ["r-gone"]
    assert waited == []


def test_a_release_answered_by_a_503_page_climbs_the_ladder(monkeypatch):
    waited: list[float] = []
    monkeypatch.setattr(tidal_catalogue, "_pause", waited.append)
    client = AlbumClient(client_failure(503, HTML))

    with pytest.raises(ValueError) as excinfo:
        tidal_catalogue.TidalCatalogue(client).release_tracks("r-1")

    assert not isinstance(excinfo.value, tidal_catalogue.ReleaseUnresolvable)
    assert len(client.album_reads) == 6
    assert waited == [1.0, 2.0, 4.0, 8.0, 16.0]


class _Refusing:
    """A track source whose offer fails as ``failure`` says."""

    def __init__(self, failure: BaseException) -> None:
        self.failure = failure

    def offer(self, request: TrackRequest):
        raise self.failure


@pytest.fixture
def settings(tmp_path: Path) -> AdapterSettings:
    staging = tmp_path / "staging"
    staging.mkdir()
    return AdapterSettings(download_staging=staging)


def test_a_track_the_provider_answers_with_a_404_page_is_permanent_with_no_retry(settings):
    result = acquire_one(_Refusing(client_failure(404, HTML)), TrackRequest(key="1"), settings)

    assert result.outcome is TrackOutcome.UNAVAILABLE_PERMANENT
    assert result.remedy is None


def test_a_track_the_provider_answers_with_a_503_page_is_transient(settings):
    result = acquire_one(_Refusing(client_failure(503, HTML)), TrackRequest(key="1"), settings)

    assert result.outcome is TrackOutcome.UNAVAILABLE_TRANSIENT
    assert result.remedy is Remedy.RETRY_LATER


def test_no_file_landed_carrying_a_404_page_stays_transient():
    """The downloader's swallowed cause is for a person; the type decides (R-703)."""
    gone = client_failure(404, HTML)
    try:
        raise NoFileLanded("the downloader reported no file for 1", cause=gone) from gone
    except NoFileLanded as exc:
        landed = exc

    assert adapter.classify_unavailable(landed) is TrackOutcome.UNAVAILABLE_TRANSIENT
