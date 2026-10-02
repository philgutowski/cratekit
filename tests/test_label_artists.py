"""R-840: an open label release whose artist reads an address is given the name.

Before R-379 a sweep wrote the provider's artist object into the review item as
text, so the item reads a memory address where the artist belongs. The producer
was fixed and the items already filed were not, since a sweep never offers a
release again while it holds a place in its label's window. ``crate label
artists`` reads each such release again by its identifier and writes the name.

These tests drive the verb where a person meets it, through the real
dispatcher and the real review store, with a fake provider catalogue. Every
release is filed by the sweep's own ``offer_release`` and decided by the
queue's own ``resolve``. Every expected value is a literal from the fixtures.
D1 applies: no real label, artist or release is named.
"""

from __future__ import annotations

import io
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import registry
from cratekit.core import config, review
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.review import Queue
from cratekit.label import artists_cli, catalogue, sweep
from cratekit.label import gate as genre_gate
from cratekit.sync import run
from tests.cli_drive import drive
from tests.label_fakes import StrictCatalogue, UnreadableCatalogue, catalogue_factory
from tests.test_config import valid_data

#: What a payload written before R-379 carries where the artist belongs.
ADDRESS = "<provider.artist.Artist object at 0x10b77ec00>"
QUEUE = str(Queue.LABEL_RELEASE)


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library) -> config.Config:
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


def offered(cfg: config.Config, release_id: str, *, artist: str = ADDRESS, **stamp) -> str:
    """One release pending in review, as the sweep's own producer files it."""
    with review.open_store(cfg) as items:
        item = sweep.offer_release(
            items,
            run.Candidate(
                identity=release_id,
                recency="2024",
                payload={
                    "artist": artist,
                    "title": f"Release {release_id}",
                    "label_id": "tide-works",
                    "label_name": "Tide Works",
                    "identity": release_id,
                    **stamp,
                },
            ),
            run_id="sweep-1",
        )
    return item.item_id


def decided(cfg: config.Config, item_id: str, verdict: review.Verdict) -> None:
    with review.open_store(cfg) as items:
        review.resolve(items, item_id, verdict, actor="suite")


def stored(cfg: config.Config, item_id: str) -> review.Item:
    with review.open_store(cfg) as items:
        return review.get(items, item_id)


def bind(monkeypatch, fake) -> None:
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))


def artists() -> tuple[int, dict]:
    return drive(["label", "artists"])


def repaired_ok() -> dict:
    code, envelope = artists()
    assert code == int(ExitCode.OK), envelope
    return envelope


def counts(summary: dict) -> dict:
    return {word: summary[word] for word in artists_cli.OUTCOMES}


def zeroes(**given: int) -> dict:
    return {**dict.fromkeys(artists_cli.OUTCOMES, 0), **given}


def check(envelope: dict, key: str) -> dict:
    found = [one for one in envelope["data"]["checks"] if one["key"] == f"label.artists.{key}"]
    assert len(found) == 1, (key, envelope["data"]["checks"])
    return found[0]


# ═══════════════════════════════════════════════════════════════════════════
# 1. What an address is
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "value",
    [
        ADDRESS,
        "<tidalapi.artist.Artist object at 0x10b77ec00>",
        "<Artist object at 0xABCDEF>",
        f"  {ADDRESS}  ",
    ],
)
def test_an_object_address_is_recognised(value):
    assert artists_cli.is_address(value)


@pytest.mark.parametrize(
    "value",
    [
        "Label Act",
        "",
        None,
        17,
        "<3 object at 0x10>",
        "Object At 0x10",
        f"Label Act {ADDRESS}",
        f"{ADDRESS} (remix)",
        "<provider.artist.Artist object at 0xZZ>",
        "<provider.artist.Artist object at 10b77ec00>",
    ],
)
def test_a_name_is_never_read_as_an_address(value):
    assert not artists_cli.is_address(value)


# ═══════════════════════════════════════════════════════════════════════════
# 2. The brief's five scenarios
# ═══════════════════════════════════════════════════════════════════════════


def test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves(
    cfg, monkeypatch
):
    stamp = {
        genre_gate.GATE_FIELD: "pass",
        genre_gate.GENRES_FIELD: ["Dance"],
        genre_gate.GATE_ANSWER_FIELD: "matched",
    }
    item_id = offered(cfg, "r-1", **stamp)
    before = stored(cfg, item_id)
    bind(monkeypatch, StrictCatalogue(release_artists={"r-1": "Harbour Act"}))

    envelope = repaired_ok()

    after = stored(cfg, item_id)
    assert after.payload["artist"] == "Harbour Act"
    assert {k: v for k, v in after.payload.items() if k != "artist"} == {
        k: v for k, v in before.payload.items() if k != "artist"
    }
    assert set(after.payload) == set(before.payload)
    assert after.verdict is None
    assert (after.ordinal, after.created, after.handler_key, after.kind) == (
        before.ordinal,
        before.created,
        before.handler_key,
        before.kind,
    )
    assert envelope["outcome"] == "ok"
    assert counts(envelope["data"]["summary"]) == zeroes(repaired=1)
    assert envelope["data"]["summary"]["releases"] == [
        {
            "release_id": "r-1",
            "item_id": item_id,
            "label_id": "tide-works",
            "label_name": "Tide Works",
            "title": "Release r-1",
            "outcome": "repaired",
            "artist": "Harbour Act",
        }
    ]
    assert check(envelope, "release.r-1")["status"] == "ok"
    assert "Harbour Act" in check(envelope, "release.r-1")["detail"]


@pytest.mark.parametrize("verdict", [review.Verdict.ACCEPTED, review.Verdict.REJECTED])
def test_a_decided_item_reading_an_address_is_left_as_it_is(cfg, monkeypatch, verdict):
    item_id = offered(cfg, "r-1")
    decided(cfg, item_id, verdict)
    before = stored(cfg, item_id)
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert stored(cfg, item_id) == before
    assert before.payload["artist"] == ADDRESS
    assert fake.artists_asked_for == []
    assert envelope["outcome"] == "no_op"
    assert counts(envelope["data"]["summary"]) == zeroes()


def test_an_item_whose_artist_is_a_name_is_not_asked_about(cfg, monkeypatch):
    item_id = offered(cfg, "r-1", artist="Label Act")
    before = stored(cfg, item_id)
    fake = StrictCatalogue(release_artists={"r-1": "Somebody Else"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert stored(cfg, item_id) == before
    assert fake.artists_asked_for == []
    assert envelope["outcome"] == "no_op"
    assert counts(envelope["data"]["summary"]) == zeroes(already_fine=1)
    assert envelope["data"]["summary"]["addresses"] == 0


def test_a_release_the_provider_does_not_serve_is_counted_and_never_blanked(cfg, monkeypatch):
    item_id = offered(cfg, "r-gone")
    before = stored(cfg, item_id)
    fake = StrictCatalogue(release_artists={})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert stored(cfg, item_id) == before
    assert before.payload["artist"] == ADDRESS
    assert fake.artists_asked_for == ["r-gone"]
    assert envelope["outcome"] == "no_op"
    assert counts(envelope["data"]["summary"]) == zeroes(not_served=1)
    line = check(envelope, "release.r-gone")
    assert line["status"] == "info"
    assert "no longer served" in line["detail"]


def test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others(
    cfg, monkeypatch
):
    first = offered(cfg, "r-1")
    named = offered(cfg, "r-2", artist="Label Act")
    settled = offered(cfg, "r-3")
    decided(cfg, settled, review.Verdict.ACCEPTED)
    second = offered(cfg, "r-4")
    fake = StrictCatalogue(
        release_artists={"r-1": "Harbour Act", "r-2": "X", "r-3": "Y", "r-4": "Quay Act"}
    )
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == ["r-1", "r-4"]
    assert fake.releases_asked_for == []
    summary = envelope["data"]["summary"]
    assert counts(summary) == zeroes(repaired=2, already_fine=1)
    assert (summary["addresses"], summary["asked"]) == (2, 2)
    assert stored(cfg, first).payload["artist"] == "Harbour Act"
    assert stored(cfg, second).payload["artist"] == "Quay Act"
    assert stored(cfg, named).payload["artist"] == "Label Act"
    assert stored(cfg, settled).payload["artist"] == ADDRESS


# ═══════════════════════════════════════════════════════════════════════════
# 3. The queue with nothing to repair, and the second run
# ═══════════════════════════════════════════════════════════════════════════


def never_opened(cfg: object):
    raise AssertionError("the catalogue was opened with no release to read")


def test_a_queue_with_no_address_opens_no_catalogue(cfg, monkeypatch):
    offered(cfg, "r-1", artist="Label Act")
    monkeypatch.setattr(catalogue, "resolve", never_opened)

    envelope = repaired_ok()

    assert envelope["outcome"] == "no_op"
    assert check(envelope, "addresses")["status"] == "ok"
    assert "no open label release reads an address" in check(envelope, "addresses")["detail"]


def test_an_empty_queue_is_a_no_op_that_opens_no_catalogue(cfg, monkeypatch):
    monkeypatch.setattr(catalogue, "resolve", never_opened)

    envelope = repaired_ok()

    assert envelope["outcome"] == "no_op"
    assert counts(envelope["data"]["summary"]) == zeroes()


def test_a_second_run_asks_about_nothing_the_first_repaired(cfg, monkeypatch):
    offered(cfg, "r-1")
    offered(cfg, "r-gone")
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act"})
    bind(monkeypatch, fake)
    repaired_ok()
    assert fake.artists_asked_for == ["r-1", "r-gone"]

    envelope = repaired_ok()

    assert fake.artists_asked_for == ["r-1", "r-gone", "r-gone"]
    assert counts(envelope["data"]["summary"]) == zeroes(already_fine=1, not_served=1)


# ═══════════════════════════════════════════════════════════════════════════
# 4. An address is never replaced by nothing
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("nothing", ["", "   "])
def test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read(
    cfg, monkeypatch, nothing
):
    item_id = offered(cfg, "r-1")
    before = stored(cfg, item_id)
    bind(monkeypatch, StrictCatalogue(release_artists={"r-1": nothing}))

    envelope = repaired_ok()

    assert stored(cfg, item_id) == before
    assert envelope["outcome"] == "no_op"
    assert counts(envelope["data"]["summary"]) == zeroes(unnamed=1)
    assert "names no artist" in check(envelope, "release.r-1")["detail"]


def unread_refusal() -> dict:
    """The refusal a run ends on when the provider failed a read. Its cause."""
    code, envelope = artists()
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "unavailable-transient"
    assert envelope["cause"]["remediation"]["remedy"] == Remedy.RETRY_LATER.value
    return envelope["cause"]


def test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses(
    cfg, monkeypatch
):
    item_id = offered(cfg, "r-1")
    before = stored(cfg, item_id)
    fake = UnreadableCatalogue()
    bind(monkeypatch, fake)

    cause = unread_refusal()

    assert stored(cfg, item_id) == before
    assert fake.artists_asked_for == ["r-1"]
    assert "could not answer about 1 of the 1 release(s)" in cause["message"]
    assert counts(cause["detail"]["artists"]) == zeroes(unread=1)
    assert cause["detail"]["artists"]["asked"] == 1
    assert cause["detail"]["left"] == 0
    [release] = cause["detail"]["artists"]["releases"]
    assert (release["release_id"], release["outcome"], release["artist"]) == (
        "r-1",
        "unread",
        None,
    )


class Parsing(StrictCatalogue):
    """A client that met a payload it could not parse, which is a ``LookupError``."""

    def release_artist(self, release_id: str) -> str:
        self.artists_asked_for.append(release_id)
        raise KeyError("artist")


def test_a_lookup_error_that_is_not_the_seams_own_is_unread_and_never_not_served(
    cfg, monkeypatch
):
    offered(cfg, "r-1")
    bind(monkeypatch, Parsing())

    cause = unread_refusal()

    assert counts(cause["detail"]["artists"]) == zeroes(unread=1)


# ═══════════════════════════════════════════════════════════════════════════
# 5. When the run stops
# ═══════════════════════════════════════════════════════════════════════════


def test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left(cfg, monkeypatch):
    for rid in ("r-1", "r-2", "r-3", "r-4", "r-5"):
        offered(cfg, rid)
    fake = UnreadableCatalogue()
    bind(monkeypatch, fake)

    cause = unread_refusal()

    assert "3 release reads in a row, so the run stopped reading" in cause["message"]
    assert fake.artists_asked_for == ["r-1", "r-2", "r-3"]
    assert cause["detail"]["left"] == 2
    assert counts(cause["detail"]["artists"]) == zeroes(unread=3)
    assert "run crate label artists again" in cause["remediation"]["steps"][-1]


def test_an_outage_over_the_last_releases_of_a_run_is_the_same_refusal(cfg, monkeypatch):
    """Three items and three failures: no fourth read is there to stop before."""
    for rid in ("r-1", "r-2", "r-3"):
        offered(cfg, rid)
    fake = UnreadableCatalogue()
    bind(monkeypatch, fake)

    cause = unread_refusal()

    assert "3 release reads in a row" in cause["message"]
    assert fake.artists_asked_for == ["r-1", "r-2", "r-3"]
    assert cause["detail"]["left"] == 0


class Flaky(StrictCatalogue):
    """Fails every read of a release named in ``failing`` and answers the rest."""

    def __init__(self, *args, failing: tuple[str, ...], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.failing = failing

    def release_artist(self, release_id: str) -> str:
        if release_id in self.failing:
            self.artists_asked_for.append(release_id)
            raise RuntimeError(f"the provider timed out on {release_id!r}")
        return super().release_artist(release_id)


def test_an_answer_between_failures_keeps_the_run_going(cfg, monkeypatch):
    for rid in ("r-1", "r-2", "r-3", "r-4", "r-5"):
        offered(cfg, rid)
    fake = Flaky(
        release_artists={"r-3": "Harbour Act"}, failing=("r-1", "r-2", "r-4", "r-5")
    )
    bind(monkeypatch, fake)

    cause = unread_refusal()

    assert fake.artists_asked_for == ["r-1", "r-2", "r-3", "r-4", "r-5"]
    assert "could not answer about 4 of the 5 release(s)" in cause["message"]
    assert counts(cause["detail"]["artists"]) == zeroes(repaired=1, unread=4)
    assert cause["detail"]["left"] == 0
    assert cause["remediation"]["steps"][-1].startswith("1 release(s) were given their artist")
    with review.open_store(cfg) as items:
        repaired = [
            item.payload["identity"]
            for item in review.list_items(items, queue=QUEUE, limit=None).items
            if item.payload["artist"] == "Harbour Act"
        ]
    assert repaired == ["r-3"], "a repair made before the refusal did not stay made"


def test_a_release_that_is_gone_does_not_count_towards_an_outage(cfg, monkeypatch):
    for rid in ("r-1", "r-2", "r-gone", "r-4", "r-5"):
        offered(cfg, rid)
    fake = Flaky(release_artists={}, failing=("r-1", "r-2", "r-4", "r-5"))
    bind(monkeypatch, fake)

    cause = unread_refusal()

    assert fake.artists_asked_for == ["r-1", "r-2", "r-gone", "r-4", "r-5"]
    assert counts(cause["detail"]["artists"]) == zeroes(not_served=1, unread=4)


class ExpiresAfter(StrictCatalogue):
    """Answers ``answers`` reads and then refuses as the seam itself refuses."""

    def __init__(self, *args, answers: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.answers = answers

    def release_artist(self, release_id: str) -> str:
        if len(self.artists_asked_for) >= self.answers:
            self.artists_asked_for.append(release_id)
            raise refuse(
                "credential-missing",
                "the stored provider session expired",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
                origin=("suite",),
            )
        return super().release_artist(release_id)


def test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired(cfg, monkeypatch):
    first = offered(cfg, "r-1")
    second = offered(cfg, "r-2")
    third = offered(cfg, "r-3")
    fake = ExpiresAfter(
        release_artists={"r-1": "Harbour Act", "r-2": "Quay Act", "r-3": "Pier Act"}, answers=1
    )
    bind(monkeypatch, fake)

    code, envelope = artists()

    assert code != int(ExitCode.OK)
    cause = envelope["cause"]
    assert cause["reason"] == "credential-missing", envelope
    assert cause["remediation"]["remedy"] == Remedy.REAUTHENTICATE_PROVIDER.value
    assert fake.artists_asked_for == ["r-1", "r-2"]
    assert counts(cause["detail"]["artists"]) == zeroes(repaired=1)
    assert cause["detail"]["artists"]["asked"] == 1, "a refused read was counted as asked"
    assert cause["detail"]["left"] == 2
    assert cause["remediation"]["steps"][-1].startswith("1 release(s) were given their artist")
    assert stored(cfg, first).payload["artist"] == "Harbour Act"
    assert stored(cfg, second).payload["artist"] == ADDRESS
    assert stored(cfg, third).payload["artist"] == ADDRESS


def test_a_catalogue_that_cannot_be_opened_refuses_and_repairs_nothing(cfg, monkeypatch):
    item_id = offered(cfg, "r-1")

    def missing(cfg: object):
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored",
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            origin=("suite",),
        )

    monkeypatch.setattr(catalogue, "resolve", missing)

    code, envelope = artists()

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "credential-missing"
    assert envelope["cause"]["detail"]["left"] == 1
    assert stored(cfg, item_id).payload["artist"] == ADDRESS


# ═══════════════════════════════════════════════════════════════════════════
# 6. What changes while a release is being read
# ═══════════════════════════════════════════════════════════════════════════


class Meanwhile(StrictCatalogue):
    """Runs ``during`` inside the read, as another process would act during it."""

    def __init__(self, *args, during, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.during = during

    def release_artist(self, release_id: str) -> str:
        self.during(release_id)
        return super().release_artist(release_id)


def test_a_release_decided_while_it_was_being_read_is_not_rewritten(cfg, monkeypatch):
    item_id = offered(cfg, "r-1")
    bind(
        monkeypatch,
        Meanwhile(
            release_artists={"r-1": "Harbour Act"},
            during=lambda rid: decided(cfg, item_id, review.Verdict.REJECTED),
        ),
    )

    envelope = repaired_ok()

    after = stored(cfg, item_id)
    assert after.verdict is review.Verdict.REJECTED
    assert after.payload["artist"] == ADDRESS
    assert counts(envelope["data"]["summary"]) == zeroes(decided=1)
    assert envelope["outcome"] == "no_op"


def test_a_release_that_left_review_while_it_was_being_read_is_not_filed_again(
    cfg, monkeypatch
):
    item_id = offered(cfg, "r-1")

    def withheld(release_id: str) -> None:
        with review.open_store(cfg) as items:
            review.withhold(
                items,
                item_id,
                group="tide-works",
                name="Tide Works",
                reason="another kind",
                detail={},
                run_id="judge-1",
            )

    bind(monkeypatch, Meanwhile(release_artists={"r-1": "Harbour Act"}, during=withheld))

    envelope = repaired_ok()

    with review.open_store(cfg) as items:
        assert review.find(items, item_id) is None
        assert review.count_unresolved(items, queue=QUEUE) == 0
    assert counts(envelope["data"]["summary"]) == zeroes(decided=1)


def test_what_a_judging_job_stamped_meanwhile_is_kept(cfg, monkeypatch):
    item_id = offered(cfg, "r-1")

    def stamped(release_id: str) -> None:
        with review.open_store(cfg) as items:
            current = review.get(items, item_id)
            review.redescribe(
                items, item_id, {**current.payload, genre_gate.GATE_FIELD: "pass"}
            )

    bind(monkeypatch, Meanwhile(release_artists={"r-1": "Harbour Act"}, during=stamped))

    repaired_ok()

    after = stored(cfg, item_id)
    assert after.payload["artist"] == "Harbour Act"
    assert after.payload[genre_gate.GATE_FIELD] == "pass"


def test_an_artist_put_right_meanwhile_is_not_overwritten(cfg, monkeypatch):
    item_id = offered(cfg, "r-1")

    def renamed(release_id: str) -> None:
        with review.open_store(cfg) as items:
            current = review.get(items, item_id)
            review.redescribe(items, item_id, {**current.payload, "artist": "Typed By Hand"})

    bind(monkeypatch, Meanwhile(release_artists={"r-1": "Harbour Act"}, during=renamed))

    envelope = repaired_ok()

    assert stored(cfg, item_id).payload["artist"] == "Typed By Hand"
    assert counts(envelope["data"]["summary"]) == zeroes(already_fine=1)
    assert envelope["outcome"] == "no_op"
    assert "stopped reading an address" in check(envelope, "release.r-1")["detail"]
    assert "0 open label release(s) do not read an address" in check(envelope, "fine")["detail"]


def test_a_stamp_landing_between_the_read_and_the_write_is_kept(cfg, monkeypatch):
    """The write is a compare and set: a payload that moved is read again."""
    item_id = offered(cfg, "r-1")
    real_find = review.find
    reads: list[str] = []

    def find_then_stamp(store, wanted):
        found = real_find(store, wanted)
        reads.append(wanted)
        if len(reads) == 1:
            # Another writer's stamp, landing after this read and before the write.
            review.redescribe(store, wanted, {**found.payload, genre_gate.GATE_FIELD: "pass"})
        return found

    monkeypatch.setattr(review, "find", find_then_stamp)
    bind(monkeypatch, StrictCatalogue(release_artists={"r-1": "Harbour Act"}))

    envelope = repaired_ok()

    after = stored(cfg, item_id)
    assert after.payload["artist"] == "Harbour Act"
    assert after.payload[genre_gate.GATE_FIELD] == "pass", "the write took the stamp back"
    assert reads == [item_id, item_id], "the item was not read again after the write was refused"
    assert counts(envelope["data"]["summary"]) == zeroes(repaired=1)


def test_an_item_that_moves_under_every_attempt_refuses_the_run_and_is_left(
    cfg, monkeypatch
):
    item_id = offered(cfg, "r-1")
    offered(cfg, "r-2")
    real_find = review.find
    reads: list[str] = []

    def find_then_stamp(store, wanted):
        found = real_find(store, wanted)
        reads.append(wanted)
        review.redescribe(store, wanted, {**found.payload, "stamped": len(reads)})
        return found

    monkeypatch.setattr(review, "find", find_then_stamp)
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act", "r-2": "Quay Act"})
    bind(monkeypatch, fake)

    code, envelope = artists()

    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "unavailable-transient"
    assert f"review item {item_id} changed under each of 3 attempts" in cause["message"]
    assert cause["detail"]["item_id"] == item_id
    assert cause["detail"]["left"] == 2
    assert reads == [item_id] * artists_cli.WRITE_ATTEMPTS == [item_id] * 3
    assert fake.artists_asked_for == ["r-1"]
    after = stored(cfg, item_id)
    assert after.payload["artist"] == ADDRESS
    assert after.payload["stamped"] == 3, "another writer's last word was taken back"


# ═══════════════════════════════════════════════════════════════════════════
# 6b. The store: a rewrite that expects the payload it read
# ═══════════════════════════════════════════════════════════════════════════


def test_a_rewrite_expecting_the_payload_the_item_carries_is_written(cfg):
    item_id = offered(cfg, "r-1")
    with review.open_store(cfg) as items:
        before = review.get(items, item_id)

        after = review.redescribe(
            items, item_id, {**before.payload, "artist": "Harbour Act"}, expecting=before.payload
        )

        assert after is not None and after.payload["artist"] == "Harbour Act"
        assert review.get(items, item_id).payload == {**before.payload, "artist": "Harbour Act"}


def test_a_rewrite_expecting_a_payload_the_item_no_longer_carries_writes_nothing(cfg):
    item_id = offered(cfg, "r-1")
    with review.open_store(cfg) as items:
        stale = review.get(items, item_id).payload
        moved = review.redescribe(items, item_id, {**stale, genre_gate.GATE_FIELD: "pass"})

        assert (
            review.redescribe(items, item_id, {**stale, "artist": "Harbour Act"}, expecting=stale)
            is None
        )

        assert review.get(items, item_id) == moved


@pytest.mark.parametrize("verdict", [review.Verdict.ACCEPTED, review.Verdict.REJECTED])
def test_a_rewrite_expecting_the_payload_of_a_decided_item_writes_nothing(cfg, verdict):
    item_id = offered(cfg, "r-1")
    decided(cfg, item_id, verdict)
    with review.open_store(cfg) as items:
        before = review.get(items, item_id)

        assert (
            review.redescribe(
                items, item_id, {**before.payload, "artist": "X"}, expecting=before.payload
            )
            is None
        )

        assert review.get(items, item_id) == before


def test_a_rewrite_expects_a_payload_that_is_not_json_as_the_empty_one_a_reader_sees(cfg):
    item_id = offered(cfg, "r-1")
    with review.open_store(cfg) as items:
        with items.immediate() as conn:
            conn.execute(
                "UPDATE review_items SET payload = 'not json' WHERE item_id = ?", (item_id,)
            )
        shown = review.get(items, item_id).payload
        assert shown == {}

        after = review.redescribe(items, item_id, {"artist": "Harbour Act"}, expecting=shown)

        assert after is not None and after.payload == {"artist": "Harbour Act"}


def test_a_rewrite_expecting_anything_of_an_item_that_is_gone_files_nothing(cfg):
    with review.open_store(cfg) as items:
        assert review.redescribe(items, "rv_nothing", {"artist": "X"}, expecting={}) is None
        assert review.count_unresolved(items) == 0


# ═══════════════════════════════════════════════════════════════════════════
# 7. Items the verb cannot read a release for
# ═══════════════════════════════════════════════════════════════════════════


def test_an_item_carrying_a_verdict_this_build_cannot_read_is_left_and_not_asked_about(
    cfg, monkeypatch
):
    item_id = offered(cfg, "r-1")
    with review.open_store(cfg) as items, items.immediate() as conn:
        conn.execute("UPDATE review_items SET verdict = 'deferred' WHERE item_id = ?", (item_id,))
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == []
    assert stored(cfg, item_id).payload["artist"] == ADDRESS
    assert counts(envelope["data"]["summary"]) == zeroes(decided=1)
    assert envelope["data"]["summary"]["addresses"] == 1
    assert "never rewritten" in check(envelope, "decided")["detail"]


def unidentified(cfg: config.Config, item_id: str, payload: dict) -> None:
    """Make an item one that arrived by import: no identity, and this payload."""
    import json

    with review.open_store(cfg) as items, items.immediate() as conn:
        conn.execute(
            "UPDATE review_items SET identity = NULL, payload = ? WHERE item_id = ?",
            (json.dumps(payload), item_id),
        )


def test_an_item_that_names_no_release_is_left_and_nothing_is_read(cfg, monkeypatch):
    item_id = offered(cfg, "r-1")
    unidentified(cfg, item_id, {"artist": ADDRESS, "title": "Release r-1"})
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == []
    assert stored(cfg, item_id).payload["artist"] == ADDRESS
    assert counts(envelope["data"]["summary"]) == zeroes(unaddressed=1)
    assert check(envelope, f"item.{item_id}")["status"] == "info"


def test_an_item_naming_another_items_release_is_not_given_that_releases_artist(
    cfg, monkeypatch
):
    item_id = offered(cfg, "r-1")
    unidentified(cfg, item_id, {"artist": ADDRESS, "title": "Release r-1", "identity": "r-2"})
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act", "r-2": "Somebody Else"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == []
    assert stored(cfg, item_id).payload["artist"] == ADDRESS
    assert counts(envelope["data"]["summary"]) == zeroes(unaddressed=1)


def test_an_item_filed_under_an_empty_identifier_is_not_asked_about(cfg, monkeypatch):
    """The sweep files ``""`` for a release with no id, and that item addresses it."""
    item_id = offered(cfg, "")
    assert item_id == genre_gate.release_item_id("")
    fake = StrictCatalogue(release_artists={"": "Nobody"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == []
    assert stored(cfg, item_id).payload["artist"] == ADDRESS
    assert counts(envelope["data"]["summary"]) == zeroes(unaddressed=1)
    assert check(envelope, f"item.{item_id}")["status"] == "info"


def test_two_items_naming_one_release_are_two_lines_under_two_keys(cfg, monkeypatch):
    stray = offered(cfg, "r-1")
    unidentified(cfg, stray, {"artist": ADDRESS, "title": "Stray", "identity": "r-2"})
    own = offered(cfg, "r-2")
    fake = StrictCatalogue(release_artists={"r-2": "Quay Act"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == ["r-2"]
    assert check(envelope, f"item.{stray}")["status"] == "info"
    assert check(envelope, "release.r-2")["status"] == "ok"
    keys = [one["key"] for one in envelope["data"]["checks"]]
    assert len(keys) == len(set(keys)), keys
    assert stored(cfg, own).payload["artist"] == "Quay Act"
    assert stored(cfg, stray).payload["artist"] == ADDRESS


def test_an_imported_item_is_read_by_the_identifier_its_payload_carries(cfg, monkeypatch):
    item_id = offered(cfg, "r-1")
    unidentified(cfg, item_id, {"artist": ADDRESS, "title": "Release r-1", "identity": "r-1"})
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act"})
    bind(monkeypatch, fake)

    repaired_ok()

    assert fake.artists_asked_for == ["r-1"]
    assert stored(cfg, item_id).payload["artist"] == "Harbour Act"


def test_an_item_with_no_artist_at_all_is_not_an_address_and_is_not_said_to_have_one(
    cfg, monkeypatch
):
    offered(cfg, "r-1", artist="")
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == []
    assert counts(envelope["data"]["summary"]) == zeroes(already_fine=1)
    said = check(envelope, "fine")["detail"]
    assert "1 open label release(s) do not read an address" in said
    assert "already read an artist" not in said


def test_a_release_held_out_of_review_is_not_an_open_item_and_is_not_read(cfg, monkeypatch):
    """The scope the verb states. A hold keeps the address until it is returned."""
    item_id = offered(cfg, "r-1")
    with review.open_store(cfg) as items:
        hold = review.withhold(
            items,
            item_id,
            group="tide-works",
            name="Tide Works",
            reason="another kind",
            detail={},
            run_id="judge-1",
        )
    assert hold is not None and hold.payload["artist"] == ADDRESS
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == []
    assert counts(envelope["data"]["summary"]) == zeroes()
    with review.open_store(cfg) as items:
        kept = review.find_hold(items, queue=QUEUE, item_id=item_id)
    assert kept is not None and kept.payload["artist"] == ADDRESS


def test_another_queues_item_reading_an_address_is_not_this_verbs(cfg, monkeypatch):
    with review.open_store(cfg) as items:
        other = review.offer(
            items,
            queue=QUEUE,
            kind="harvested-label",
            identity={"label": "tide-works"},
            payload={"artist": ADDRESS, "identity": "r-1"},
        )
    fake = StrictCatalogue(release_artists={"r-1": "Harbour Act"})
    bind(monkeypatch, fake)

    envelope = repaired_ok()

    assert fake.artists_asked_for == []
    assert stored(cfg, other.item_id).payload["artist"] == ADDRESS
    assert counts(envelope["data"]["summary"]) == zeroes()


# ═══════════════════════════════════════════════════════════════════════════
# 8. What the verb declares, and what a person reads
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_declares_what_it_is():
    entry = registry.entry("label.artists")
    assert entry.output_schema == "diagnostic/1"
    assert not entry.adjudicates
    assert not entry.long_running
    assert not entry.destructive
    assert entry.writes == frozenset()
    assert entry.doctor_checks == ("library.mounted", "credential.provider")
    assert entry.landed


def test_a_person_reads_each_release_without_asking_for_json(cfg, monkeypatch):
    offered(cfg, "r-1")
    offered(cfg, "r-gone")
    bind(monkeypatch, StrictCatalogue(release_artists={"r-1": "Harbour Act"}))

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["label", "artists"], stdout=out, stderr=err)
    text = out.getvalue() + err.getvalue()

    assert code == int(ExitCode.OK), text
    assert "2 open label release(s) read an address" in text
    assert "1 were given the artist's name and 1 were left as they are" in text
    assert "release r-1 ('Release r-1') on Tide Works now reads its artist, Harbour Act" in text
    assert "release r-gone ('Release r-gone') on Tide Works is no longer served" in text
