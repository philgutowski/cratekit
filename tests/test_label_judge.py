"""R-815: the label releases already in review are judged without a sweep."""

from __future__ import annotations

import os
import signal
from types import SimpleNamespace

import pytest

from cratekit.cli import handlers, registry
from cratekit.core import active_taxonomy, config, jobs, review, tombstone
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.core.review import DecisionStore, Queue
from cratekit.label import catalogue, judge_cli, sweep
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.sync import run
from cratekit.tagging import published
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedArtist, FakeRelease, catalogue_factory
from tests.test_label_approved import human
from tests.test_label_genre_gate import (
    LABEL,
    SLUG,
    Lookup,
    Track,
    active_copy_without_published_rules,
    bind_lookup,
    check,
    filed,
    held_ids,
    held_ok,
    held_verb,
    isrc,
    never_asked,
    provider_of,
    register,
    serve,
    sweep_once,
)
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_label_workers import item_states, queued_sweep
from tests.test_label_workers import one_parser as one_parser  # noqa: PLC0414 - fixture
from tests.test_tag_workers import warning_codes

QUEUE = str(Queue.LABEL_RELEASE)
FILED_BY = "sweep-1"
UNKNOWN = "the general catalogue does not know its tracks"
#: The fields a judged item is stamped with.
GATE, ANSWER, NOTE = genre_gate.GATE_FIELD, genre_gate.GATE_ANSWER_FIELD, genre_gate.GATE_NOTE_FIELD
GENRES, GATE_RUN = genre_gate.GENRES_FIELD, genre_gate.GATE_RUN_FIELD


def queue_release(
    cfg: config.Config, *release_ids: str, label_id: str = SLUG, label_name: str = LABEL,
    filed_by: str | None = FILED_BY, **stamp,
) -> str:
    """Each release pending in review, as a sweep before the gate filed it. The last item id."""
    with review.open_store(cfg) as store:
        for release_id in release_ids:
            payload = {
                "artist": "Label Act", "title": f"Release {release_id}", "label_id": label_id,
                "label_name": label_name, "identity": release_id, **stamp,
            }
            candidate = run.Candidate(identity=release_id, recency="2026", payload=payload)
            item_id = sweep.offer_release(store, candidate, run_id=filed_by).item_id
    return item_id


def recorded(gate: str, note: str, answer: str, *genres: str) -> dict:
    """The stamp a sweep leaves on an item, as ``queue_release`` keywords."""
    stamp = {"genre_gate": gate, "genre_gate_note": note, "genre_gate_answer": answer}
    return {**stamp, "published_genres": list(genres)} if genres else stamp


def pending(cfg, monkeypatch, releases: dict[str, str], lookup=None, *argv: str,
            **stamp) -> FakeCatalogue:
    """Register the label with ``argv``, queue each release with ``stamp``, bind both catalogues."""
    register(*argv)
    queue_release(cfg, *releases, **stamp)
    return provider_of(monkeypatch, releases, lookup)


def five_pending(cfg, monkeypatch, lookup) -> FakeCatalogue:
    """Releases r-1 to r-5 pending, each with its own ISRC."""
    return pending(cfg, monkeypatch, {f"r-{n}": isrc(n) for n in range(1, 6)}, lookup)


def judge(*argv: str) -> tuple[int, dict]:
    return drive(["label", "judge", *argv])


def resumed(job_id: str) -> dict:
    code, envelope = judge("--job", job_id)
    assert code == int(ExitCode.OK), envelope
    return envelope


def parked_on(job_id: str) -> dict:
    """Drive the job, which must park as blocked. Its envelope."""
    code, parked = judge("--job", job_id)
    assert code != int(ExitCode.OK)
    assert parked["outcome"] == "blocked"
    return parked


def queued_job(*argv: str) -> str:
    code, envelope = judge(*argv)
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"]


def judge_once(*argv: str) -> tuple[str, dict]:
    """Queue a judging job and drive it to its end. The job and the last envelope."""
    job_id = queued_job(*argv)
    return job_id, resumed(job_id)


def judging(envelope: dict) -> dict:
    return envelope["data"]["progress"]["judging"]


def counts(row: dict) -> dict:
    return {word: row[word] for word in ("judged", "held", "passed", "not-judged")}


def tally(judged: int, held: int, passed: int, not_judged: int) -> dict:
    return {"judged": judged, "held": held, "passed": passed, "not-judged": not_judged}


def label_row(envelope: dict, label_id: str = SLUG) -> dict:
    [row] = [one for one in judging(envelope)["labels"] if one["label_id"] == label_id]
    return row


def item_of(cfg: config.Config, release_id: str) -> review.Item:
    return filed(cfg)[release_id]


def reports(cfg: config.Config, job_id: str) -> dict[str, dict]:
    return {
        str(report["release_id"]): report
        for report in judge_cli.ARTIFACTS.committed(cfg, job_id)
    }


def withhold(store, item_id: str, *, run_id: str = "judge-1", reason: str = "another kind"):
    return review.withhold(
        store, item_id, group=SLUG, name=LABEL, reason=reason,
        detail={"genres": ["Christian"], "kind": "dance", "placed": [["Christian", "christian"]]},
        run_id=run_id,
    )


def held_by_hand(store, *, release_id: str = "r-1", payload: dict, reason: str, run_id: str,
                 **kwargs):
    """A hold written straight through the store, under this file's label."""
    return review.hold(
        store, queue=QUEUE, kind=sweep.KIND, identity={"release_id": release_id},
        payload=payload, group=SLUG, name=LABEL, reason=reason, detail={}, run_id=run_id, **kwargs,
    )


def deferred(store, item_id: str) -> None:
    """Give the item a verdict this build cannot read, as a newer build would."""
    with store.immediate() as conn:
        conn.execute("UPDATE review_items SET verdict = 'deferred' WHERE item_id = ?", (item_id,))


def test_an_open_item_leaves_the_queue_and_becomes_a_hold_carrying_what_it_carried(installed):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        before = review.get(store, item_id)
        hold = withhold(store, item_id)
        assert review.find(store, item_id) is None
        assert review.count_unresolved(store, queue=QUEUE) == 0
        [standing] = review.holds(store, queue=QUEUE)
    assert hold == standing
    assert (hold.item_id, hold.kind, hold.state) == (item_id, sweep.KIND, review.HOLD_HELD)
    assert hold.identity == {"release_id": "r-1"}
    # What the item carried, and the word that says it was taken back.
    assert hold.payload == {**before.payload, review.WITHHELD_FIELD: True}
    assert (hold.group, hold.name, hold.reason, hold.run_id) == (
        SLUG, LABEL, "another kind", "judge-1",
    )
    assert hold.detail["genres"] == ["Christian"]


def _resolved(verdict: review.Verdict):
    return lambda store, item_id: review.resolve(store, item_id, verdict, actor="suite")


def _superseded(store, item_id: str) -> review.Item:
    [retired] = review.supersede(store, [item_id], rule="suite-rule")
    return retired


def _unreadable(store, item_id: str) -> review.Item:
    """A newer build's decision on a shared queue is a decision. It lists as open here."""
    deferred(store, item_id)
    item = review.get(store, item_id)
    assert item.verdict is None
    assert item.stored_verdict == "deferred"
    return item


@pytest.mark.parametrize(
    "decide",
    [
        pytest.param(_resolved(review.Verdict.ACCEPTED), id="accepted"),
        pytest.param(_resolved(review.Verdict.REJECTED), id="rejected"),
        pytest.param(_superseded, id="superseded"),
        pytest.param(_unreadable, id="a-verdict-this-build-cannot-read"),
    ],
)
def test_a_decided_item_is_not_withheld_and_stays_exactly_as_it_was(installed, decide):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        decided = decide(store, item_id)
        assert withhold(store, item_id) is None
        assert review.get(store, item_id) == decided
        assert review.holds(store, queue=QUEUE) == ()


def test_a_release_a_person_returned_is_never_withheld_again(installed):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        held_by_hand(
            store, payload={}, reason="returned by hand while it was in review",
            run_id="", returned=True,
        )
        assert withhold(store, item_id) is None
        assert review.find(store, item_id) is not None
        assert review.find_hold(store, queue=QUEUE, item_id=item_id).state == review.HOLD_RETURNED


def test_withholding_an_identifier_nothing_answers_to_moves_nothing(installed):
    with review.open_store(installed) as store:
        assert withhold(store, "rv-nobody") is None
        assert review.holds(store, queue=QUEUE) == ()


def test_a_hold_in_force_beside_an_open_item_is_refreshed_and_keeps_its_first_run(installed):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        held_by_hand(store, payload={"title": "stale"}, reason="an older reason", run_id="sweep-0")
        hold = withhold(store, item_id, reason="another kind")
        assert review.find(store, item_id) is None
        assert [one.item_id for one in review.holds(store, queue=QUEUE)] == [item_id]
    assert (hold.run_id, hold.reason) == ("sweep-0", "another kind")
    assert hold.payload["title"] == "Release r-1"


def test_an_item_that_arrived_with_no_identity_is_still_found_as_a_hold(installed):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        with store.immediate() as conn:
            conn.execute("UPDATE review_items SET identity = NULL WHERE item_id = ?", (item_id,))
        hold = withhold(store, item_id)
        assert hold.identity == {}
        assert hold.payload["identity"] == "r-1"
        assert review.find_hold(store, queue=QUEUE, item_id=item_id) == hold


def test_an_ordinal_a_withheld_item_held_is_never_given_to_a_later_one(installed):
    """Paging keys on the ordinal, so a reused one hides a new item behind an old cursor."""
    queue_release(installed, "r-1")
    second = queue_release(installed, "r-2")
    with review.open_store(installed) as store:
        assert review.get(store, second).ordinal == 2
        withhold(store, second)
    third = queue_release(installed, "r-3")
    with review.open_store(installed) as store:
        assert review.get(store, third).ordinal == 3
        page = review.list_items(store, queue=QUEUE, after=2)
        assert [item.item_id for item in page.items] == [third]
        # The other writer that inserts an item allocates the same way.
        document = review.export_document(store, queue=QUEUE)
        document["items"] = [
            {**document["items"][0], "id": "rv-imported", "payload": {"identity": "r-9"}}
        ]
        review.import_document(store, document, actor="suite")
        assert review.get(store, "rv-imported").ordinal == 4


def test_the_floor_is_raised_and_never_lowered(installed):
    first = queue_release(installed, "r-1")
    second = queue_release(installed, "r-2")
    with review.open_store(installed) as store:
        withhold(store, second)
        withhold(store, first)
    assert review_ordinal(installed, queue_release(installed, "r-3")) == 3


def review_ordinal(cfg: config.Config, item_id: str) -> int:
    with review.open_store(cfg) as store:
        return review.get(store, item_id).ordinal


def test_an_open_item_is_redescribed_and_keeps_its_place(installed):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        before = review.get(store, item_id)
        after = review.redescribe(store, item_id, {**before.payload, "said": "more"})
        assert after == review.get(store, item_id)
    assert after.payload == {**before.payload, "said": "more"}
    assert (after.ordinal, after.handler_key, after.verdict) == (
        before.ordinal, before.handler_key, None,
    )


@pytest.mark.parametrize(
    "decide",
    [pytest.param(_resolved(review.Verdict.REJECTED), id="rejected"),
     pytest.param(_unreadable, id="an-unreadable-verdict")],
)
def test_redescribing_a_decided_item_changes_nothing(installed, decide):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        decided = decide(store, item_id)
        assert review.redescribe(store, item_id, {"said": "more"}) is None
        assert review.get(store, item_id) == decided


def test_redescribing_an_item_that_is_gone_files_nothing(installed):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        withhold(store, item_id)
        assert review.redescribe(store, item_id, {"said": "more"}) is None
        assert review.find(store, item_id) is None
        assert review.count_unresolved(store, queue=QUEUE) == 0


def test_a_refreshed_hold_keeps_the_run_its_release_was_filed_under(installed):
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        withhold(store, item_id)
        def refresh(payload: dict):
            return held_by_hand(
                store, payload=payload, reason="still another kind", run_id="sweep-2",
            )
        # Described as never filed, it keeps its filing run and its withheld word.
        assert refresh({"identity": "r-1", "title": "T"}).payload == {
            "identity": "r-1", "title": "T", sweep.SWEEP_RUN: FILED_BY, review.WITHHELD_FIELD: True,
        }
        # One that names a run of its own is believed.
        again = refresh({"identity": "r-1", sweep.SWEEP_RUN: "sweep-7"}).payload
        assert (again[sweep.SWEEP_RUN], again[review.WITHHELD_FIELD]) == ("sweep-7", True)


def test_a_refreshed_hold_that_never_named_a_run_gains_none(installed):
    with review.open_store(installed) as store:
        for title in ("first", "second"):
            hold = held_by_hand(
                store, payload={"identity": "r-1", "title": title}, reason="another kind",
                run_id="sweep-1",
            )
    assert hold.payload == {"identity": "r-1", "title": "second"}


def test_a_queued_release_of_another_kind_is_held_listed_and_returned(installed, monkeypatch):
    lookup = Lookup({isrc(1): ("Christian",), isrc(2): ("Dance",)})
    pending(installed, monkeypatch, {"r-christian": isrc(1), "r-dance": isrc(2)}, lookup)
    job_id, envelope = judge_once()
    assert counts(judging(envelope)) == tally(2, 1, 1, 0)
    assert counts(label_row(envelope)) == tally(2, 1, 1, 0)
    assert label_row(envelope)["label_name"] == LABEL
    # Gone from review, and held, not rejected.
    assert sorted(filed(installed)) == ["r-dance"]
    assert held_ids(installed) == ["r-christian"]
    assert DecisionStore(tombstone.STORE_KEY, installed).suppressions() == ()
    with review.open_store(installed) as store:
        [hold] = review.holds(store, queue=QUEUE)
    assert hold.run_id == job_id
    assert hold.detail["genres"] == ["Christian"]
    assert "which is christian and not dance" in hold.reason
    listing = held_ok()
    line = check(listing, "label.held.release.r-christian")["detail"]
    assert "release r-christian ('Release r-christian' by Label Act) on Tide Works is held" in line
    assert "which is christian and not dance" in line
    returned = held_ok("return", "r-christian")
    assert returned["data"]["summary"]["returned"] == ["r-christian"]
    back = item_of(installed, "r-christian")
    assert back.verdict is None
    assert back.payload[GATE] == genre_gate.RETURNED
    # Filed under the sweep that first filed it, not under the judging job.
    assert back.payload[sweep.SWEEP_RUN] == FILED_BY
    # The word that it was taken back was the hold's, and stayed with it.
    assert review.WITHHELD_FIELD not in back.payload
    assert held_ids(installed) == []


def test_a_returned_release_is_not_judged_again_and_nobody_is_asked(installed, monkeypatch):
    provider = pending(installed, monkeypatch, {"r-christian": isrc(1)})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Christian",)}))
    judge_once()
    assert held_verb("return", "r-christian")[0] == int(ExitCode.OK)
    asked_before = list(provider.releases_asked_for)
    bind_lookup(monkeypatch, never_asked)
    job_id, envelope = judge_once()
    assert provider.releases_asked_for == asked_before
    assert sorted(filed(installed)) == ["r-christian"]
    assert held_ids(installed) == []
    assert judging(envelope)["returned"] == 1
    assert counts(judging(envelope)) == tally(0, 0, 0, 0)
    assert reports(installed, job_id)["r-christian"]["outcome"] == judge_cli.RETURNED


@pytest.mark.parametrize(
    ("table", "argv", "stamped", "tallied", "warned"),
    [
        pytest.param({isrc(1): ("Dance",)}, (),
                     {GATE: "passed", GENRES: ["Dance"]},
                     tally(1, 0, 1, 0), [], id="of-the-labels-kind-it-says-the-gate-passed-it"),
        pytest.param({}, (), {GATE: "not-judged", ANSWER: "miss",
                              NOTE: UNKNOWN}, tally(0, 0, 0, 1),
                     [(judge_cli.NOT_JUDGED_LEFT, "1 release(s) stay in review not judged")],
                     id="the-catalogue-does-not-know-it-and-it-is-marked-not-judged"),
        pytest.param(None, ("--kind", "any"),
                     {GATE: "passed",
                      NOTE: "its label is followed for any kind of music"},
                     tally(1, 0, 1, 0), [], id="a-label-marked-any-has-nothing-held-nobody-asked"),
    ],
)
def test_a_queued_release_that_stays_in_review_says_what_the_gate_made_of_it(
    installed, monkeypatch, table, argv, stamped, tallied, warned
):
    lookup = never_asked if table is None else Lookup(table)
    provider = pending(installed, monkeypatch, {"r-1": isrc(1)}, lookup, *argv)
    job_id, envelope = judge_once()
    stays = item_of(installed, "r-1")
    assert stays.verdict is None
    assert {key: stays.payload[key] for key in stamped} == stamped
    assert (stays.payload[GATE_RUN], stays.payload[sweep.SWEEP_RUN]) == (job_id, FILED_BY)
    assert held_ids(installed) == []
    assert counts(judging(envelope)) == tallied
    asked = 0 if table is None else 1
    assert (provider.releases_asked_for, judging(envelope)["asked"]) == (["r-1"] * asked, asked)
    assert warning_codes(envelope) == [code for code, _ in warned]
    for (_, said), warning in zip(warned, envelope["warnings"]):
        assert said in warning["message"]


@pytest.mark.parametrize("verdict", [review.Verdict.ACCEPTED, review.Verdict.REJECTED])
def test_an_item_decided_before_the_run_is_no_part_of_it(installed, monkeypatch, verdict):
    register()
    item_id = queue_release(installed, "r-christian")
    queue_release(installed, "r-open")
    with review.open_store(installed) as store:
        decided = review.resolve(store, item_id, verdict, actor="suite")
    provider = provider_of(monkeypatch, {"r-christian": isrc(1), "r-open": isrc(2)})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Christian",), isrc(2): ("Dance",)}))
    job_id, _ = judge_once()
    assert list(item_states(job_id)) == [item_of(installed, "r-open").item_id]
    assert provider.releases_asked_for == ["r-open"]
    with review.open_store(installed) as store:
        assert review.get(store, item_id) == decided
    assert held_ids(installed) == []


@pytest.mark.parametrize("verdict", [review.Verdict.ACCEPTED, review.Verdict.REJECTED])
def test_an_item_decided_after_the_job_was_queued_is_untouched(installed, monkeypatch, verdict):
    register()
    item_id = queue_release(installed, "r-christian")
    provider = provider_of(monkeypatch, {"r-christian": isrc(1)}, never_asked)
    job_id = queued_job()
    with review.open_store(installed) as store:
        decided = review.resolve(store, item_id, verdict, actor="suite")
    envelope = resumed(job_id)
    assert provider.releases_asked_for == []
    with review.open_store(installed) as store:
        assert review.get(store, item_id) == decided
    assert held_ids(installed) == []
    assert judging(envelope)["decided"] == 1
    assert counts(judging(envelope)) == tally(0, 0, 0, 0)


def test_a_release_decided_while_it_was_being_judged_is_not_held(installed, monkeypatch):
    """The verdict is checked inside the write, so the person's answer wins the race."""
    register()
    item_id = queue_release(installed, "r-christian")
    provider_of(monkeypatch, {"r-christian": isrc(1)})
    def decided_meanwhile(value):
        with review.open_store(installed) as store:
            review.resolve(store, item_id, review.Verdict.ACCEPTED, actor="suite")
        return published.Published(published.SOURCE, "matched", genres=("Christian",))
    bind_lookup(monkeypatch, decided_meanwhile)
    job_id, envelope = judge_once()
    assert item_of(installed, "r-christian").verdict is review.Verdict.ACCEPTED
    assert GATE not in item_of(installed, "r-christian").payload
    assert held_ids(installed) == []
    assert reports(installed, job_id)["r-christian"]["outcome"] == judge_cli.DECIDED
    assert judging(envelope)["held"] == 0


def test_an_artist_put_right_while_a_release_was_being_judged_is_kept_by_the_stamp(
    installed, monkeypatch
):
    """R-840. The stamp is made on the payload as it stands, not as it was read."""
    register()
    item_id = queue_release(installed, "r-dance")
    provider_of(monkeypatch, {"r-dance": isrc(1)})
    def repaired_meanwhile(value):
        with review.open_store(installed) as store:
            current = review.get(store, item_id)
            review.redescribe(store, item_id, {**current.payload, "artist": "Harbour Act"})
        return published.Published(published.SOURCE, "matched", genres=("Dance",))
    bind_lookup(monkeypatch, repaired_meanwhile)
    job_id, _envelope = judge_once()
    after = item_of(installed, "r-dance")
    assert reports(installed, job_id)["r-dance"]["outcome"] == judge_cli.PASSED
    assert after.payload[GATE] == "passed"
    assert after.payload["artist"] == "Harbour Act", "the stamp took the repair back"


def test_a_release_on_a_label_nobody_follows_any_more_is_judged_as_the_default_kind(
    installed, monkeypatch
):
    queue_release(installed, "r-christian", label_id="gone-label", label_name="Gone Label")
    provider_of(monkeypatch, {"r-christian": isrc(1)}, Lookup({isrc(1): ("Christian",)}))
    _, envelope = judge_once()
    assert held_ids(installed) == ["r-christian"]
    assert counts(label_row(envelope, "gone-label")) == tally(1, 1, 0, 0)


def test_words_the_item_recorded_pass_a_release_with_no_request_at_all(installed, monkeypatch):
    note = "the general catalogue calls it Dance, and its label is followed as dance"
    stamp = recorded("passed", note, "matched", "Dance")
    provider = pending(installed, monkeypatch, {"r-dance": isrc(2)}, never_asked, **stamp)
    _, envelope = judge_once()
    assert provider.releases_asked_for == []
    assert held_ids(installed) == []
    assert counts(judging(envelope)) == tally(1, 0, 1, 0)
    assert judging(envelope)["asked"] == 0
    # A verdict the item already carried is not written again: the stamp stays the sweep's.
    assert GATE_RUN not in item_of(installed, "r-dance").payload


def test_recorded_words_that_would_hold_are_asked_about_before_the_release_is_held(
    installed, monkeypatch
):
    """Judged against the kind the label has now, and held on what the catalogue says now."""
    stamp = recorded("passed", "filed when the label was a dance label", "matched", "Dance")
    lookup = Lookup({isrc(2): ("Dance",)})
    provider = pending(installed, monkeypatch, {"r-dance": isrc(2)}, lookup, "--kind", "christian",
                       **stamp)
    _, envelope = judge_once()
    assert provider.releases_asked_for == ["r-dance"]
    assert lookup.asked == [isrc(2)]
    assert held_ids(installed) == ["r-dance"]
    assert filed(installed) == {}
    assert judging(envelope)["asked"] == 1


def test_a_record_of_one_tracks_album_does_not_hold_a_release_its_next_track_passes(
    installed, monkeypatch
):
    """A sweep stops asking at the first passing track, so its record can be one album."""
    register()
    stamp = recorded("passed", "filed on its first track", "matched", "Christian")
    queue_release(installed, "r-two", **stamp)
    rows = [Track("t-1", "Artist", "One", isrc(1)), Track("t-2", "Artist", "Two", isrc(2))]
    lookup = Lookup({isrc(1): ("Christian",), isrc(2): ("Dance",)})
    serve(monkeypatch, FakeCatalogue(releases={"r-two": (rows, 2026)}), lookup)
    _, envelope = judge_once()
    assert lookup.asked == [isrc(1), isrc(2)]
    assert held_ids(installed) == []
    stays = item_of(installed, "r-two").payload
    assert (stays[GATE], stays[GENRES]) == ("passed", ["Christian", "Dance"])
    assert counts(judging(envelope)) == tally(1, 0, 1, 0)


@pytest.mark.parametrize("answer", ["matched", "miss", "no-isrc"])
def test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again(
    installed, monkeypatch, answer
):
    stamp = recorded("not-judged", "what the sweep was told", answer)
    provider = pending(installed, monkeypatch, {"r-known-nothing": isrc(4)}, never_asked, **stamp)
    job_id, envelope = judge_once()
    assert provider.releases_asked_for == []
    stays = item_of(installed, "r-known-nothing")
    assert stays.payload[NOTE] == "what the sweep was told"
    assert GATE_RUN not in stays.payload
    report = reports(installed, job_id)["r-known-nothing"]
    assert (report["outcome"], report["reason"], report["asked"]) == (
        "not-judged", "what the sweep was told", False,
    )
    assert counts(judging(envelope))["not-judged"] == 1


@pytest.mark.parametrize("answer", ["blocked", "unreachable", "parse-break", "not-asked"])
def test_a_release_nobody_was_told_anything_about_is_asked_about(installed, monkeypatch, answer):
    stamp = recorded("not-judged", "the general catalogue could not be read", answer)
    lookup = Lookup({isrc(1): ("Christian",)})
    provider = pending(installed, monkeypatch, {"r-christian": isrc(1)}, lookup, **stamp)
    _, envelope = judge_once()
    assert provider.releases_asked_for == ["r-christian"]
    assert lookup.asked == [isrc(1)]
    assert held_ids(installed) == ["r-christian"]
    assert judging(envelope)["asked"] == 1


def test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item(installed, monkeypatch):
    """The stamp is one statement. Old words beside a new verdict would be asked about for ever."""
    stamp = recorded("passed", "filed when the label was followed for christian music", "matched",
                     "Christian")
    provider = pending(installed, monkeypatch, {"r-1": isrc(1)}, Lookup({}), **stamp)
    judge_once()
    stays = item_of(installed, "r-1").payload
    assert (stays[GATE], stays[ANSWER]) == ("not-judged", "miss")
    assert GENRES not in stays
    assert stays["title"] == "Release r-1"
    assert held_ids(installed) == []
    # And so the next run reads the record and asks nobody.
    bind_lookup(monkeypatch, never_asked)
    judge_once()
    assert provider.releases_asked_for == ["r-1"]


def test_an_item_that_names_no_release_is_not_judged_and_nothing_is_read(installed, monkeypatch):
    register()
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        before = review.get(store, item_id)
        with store.immediate() as conn:
            conn.execute(
                "UPDATE review_items SET identity = NULL, payload = ? WHERE item_id = ?",
                ('{"label_id": "tide-works", "label_name": "Tide Works"}', item_id),
            )
    provider = provider_of(monkeypatch, {"r-1": isrc(1)}, never_asked)
    job_id, envelope = judge_once()
    assert provider.releases_asked_for == []
    [report] = reports(installed, job_id).values()
    assert report["outcome"] == "not-judged"
    assert report["reason"] == "its review item names no release, so its tracks could not be read"
    with review.open_store(installed) as store:
        after = review.get(store, item_id)
    # It stays, and it says why it could not be judged.
    assert (after.payload[GATE], after.payload[NOTE]) == ("not-judged", report["reason"])
    assert (after.payload["label_id"], after.verdict, after.ordinal) == (
        "tide-works", None, before.ordinal,
    )
    assert counts(judging(envelope))["not-judged"] == 1


def test_an_item_that_names_another_items_release_is_not_read_and_stamps_only_itself(
    installed, monkeypatch
):
    """An imported item carries no identity, and its payload is all there is to go on."""
    register()
    item_id = queue_release(installed, "r-1")
    note = "the general catalogue calls it Dance, and its label is followed as dance"
    other = queue_release(installed, "r-2", **recorded("passed", note, "matched", "Dance"))
    with review.open_store(installed) as store:
        with store.immediate() as conn:
            conn.execute(
                "UPDATE review_items SET identity = NULL, payload = ? WHERE item_id = ?",
                ('{"identity": "r-2", "label_id": "tide-works"}', item_id),
            )
        untouched = review.get(store, other)
    provider = provider_of(monkeypatch, {"r-1": isrc(1), "r-2": isrc(2)}, never_asked)
    job_id, _ = judge_once()
    assert provider.releases_asked_for == []
    with review.open_store(installed) as store:
        assert review.get(store, other).payload == untouched.payload
        mislabelled = review.get(store, item_id).payload
    assert (mislabelled["identity"], mislabelled[GATE]) == ("r-2", "not-judged")
    wrong = [
        report
        for report in judge_cli.ARTIFACTS.committed(installed, job_id)
        if report["item"] == item_id
    ]
    assert [report["outcome"] for report in wrong] == ["not-judged"]
    assert "is not the one release r-2 is addressed by" in wrong[0]["reason"]


def test_nothing_pending_queues_nothing_and_says_so(installed):
    register()
    code, envelope = judge()
    assert code == int(ExitCode.OK), envelope
    assert (envelope["outcome"], envelope["data"]["job_id"]) == ("no_op", "")
    assert warning_codes(envelope) == [judge_cli.NOTHING_PENDING]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_named_label_scopes_the_job_to_its_releases(installed, monkeypatch):
    register()
    register(name="Other Works")
    queue_release(installed, "r-ours")
    queue_release(installed, "r-theirs", label_id="other-works", label_name="Other Works")
    provider = provider_of(monkeypatch, {"r-ours": isrc(1), "r-theirs": isrc(2)})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Christian",), isrc(2): ("Christian",)}))
    _, envelope = judge_once("--label", LABEL)
    assert provider.releases_asked_for == ["r-ours"]
    assert held_ids(installed) == ["r-ours"]
    assert sorted(filed(installed)) == ["r-theirs"]
    assert [row["label_id"] for row in judging(envelope)["labels"]] == [SLUG]


def test_a_label_nobody_follows_refuses_the_scope_and_queues_nothing(installed):
    register()
    queue_release(installed, "r-1")
    code, envelope = judge("--label", LABEL, "--label", "No Such Label")
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "label-unknown"
    assert envelope["cause"]["detail"]["unknown"] == ["No Such Label"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_scope_with_nothing_pending_says_which_zero_it_is(installed):
    register()
    register(name="Other Works")
    queue_release(installed, "r-theirs", label_id="other-works", label_name="Other Works")
    code, envelope = judge("--label", LABEL)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert "for the labels named" in envelope["warnings"][0]["message"]


def test_the_job_is_one_item_per_pending_release_and_carries_no_harvested_name(installed):
    register()
    first = queue_release(installed, "r-1")
    second = queue_release(installed, "r-2")
    with review.open_store(installed) as store:
        review.offer(
            store, queue=QUEUE, kind="harvested-label", identity={"label": "someone"},
            payload={"name": "Someone"}, handler_key="label.harvest",
        )
    job_id = queued_job()
    assert item_states(job_id) == {first: "pending", second: "pending"}


class Interrupting(Lookup):
    """A catalogue during whose answer about one ISRC the run is told to stop."""

    def __init__(self, table, *, on: str) -> None:
        super().__init__(table)
        self.on = on

    def __call__(self, value):
        if str(value) == self.on:
            os.kill(os.getpid(), signal.SIGINT)
        return super().__call__(value)


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (("Christian",), tally(3, 2, 1, 0)),
        (("Dance",), tally(3, 1, 2, 0)),
    ],
    ids=["stopped-on-a-held-release", "stopped-on-a-passed-release"],
)
def test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none(
    installed, monkeypatch, words, expected
):
    """The release in flight when the run stopped was written and not marked done."""
    lookup = Interrupting({isrc(1): ("Dance",), isrc(2): words, isrc(3): ("Christian",)},
                          on=isrc(2))
    provider = pending(installed, monkeypatch, {f"r-{n}": isrc(n) for n in (1, 2, 3)}, lookup)
    job_id = queued_job()
    code, stopped = judge("--job", job_id)
    assert code != int(ExitCode.OK)
    assert (stopped["outcome"], stopped["cause"]["detail"]["left"]) == ("cancelled", 2)
    assert counts(stopped["cause"]["detail"]["judging"]) == tally(1, 0, 1, 0)
    said = stopped["cause"]["remediation"]["steps"][-1]
    assert f"crate job resume {job_id}" in said
    assert "2 release(s) of this job are not judged yet" in said
    lookup.on = ""
    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    envelope = resumed(job_id)
    assert lookup.asked == [isrc(1), isrc(2), isrc(3)]
    assert provider.releases_asked_for == ["r-1", "r-2", "r-3"]
    assert counts(judging(envelope)) == expected
    assert sorted(reports(installed, job_id)) == ["r-1", "r-2", "r-3"]
    assert set(item_states(job_id).values()) == {"done"}
    assert len(held_ids(installed)) == expected["held"]


def test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left(
    installed, monkeypatch
):
    """One refusal is enough. The lookup would answer every later release from memory."""
    lookup = Lookup({isrc(n): "blocked" for n in range(1, 6)})
    provider = five_pending(installed, monkeypatch, lookup)
    job_id = queued_job()
    parked = parked_on(job_id)
    cause = parked["cause"]
    assert cause["reason"] == "catalogue-unreachable"
    assert "the general catalogue refused" in cause["message"]
    assert "the catalogue said blocked" in cause["detail"]["refused"]
    assert cause["detail"]["left"] == 4
    assert provider.releases_asked_for == ["r-1"]
    assert lookup.asked == [isrc(1)]
    assert sorted(item_states(job_id).values()) == ["done"] + ["pending"] * 4
    refused = item_of(installed, "r-1").payload
    assert (refused[GATE], refused[ANSWER]) == ("not-judged", "blocked")
    assert GATE not in item_of(installed, "r-2").payload
    lookup.table = {isrc(n): ("Dance",) for n in range(1, 6)}
    envelope = resumed(job_id)
    assert lookup.asked[1:] == [isrc(2), isrc(3), isrc(4), isrc(5)]
    assert counts(judging(envelope)) == tally(4, 0, 4, 1)


def test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left(
    installed, monkeypatch
):
    lookup = Lookup({isrc(n): "unreachable" for n in range(1, 6)})
    provider = five_pending(installed, monkeypatch, lookup)
    job_id = queued_job()
    parked = parked_on(job_id)
    cause = parked["cause"]
    assert cause["reason"] == "catalogue-unreachable"
    assert "could not be read for 3 releases in a row" in cause["message"]
    assert cause["detail"]["left"] == 2
    assert cause["remediation"]["steps"][-1] == (
        f"2 release(s) of this job are not judged yet; continue with: "
        f"crate label judge --job {job_id}"
    )
    assert counts(cause["detail"]["judging"]) == tally(0, 0, 0, 3)
    assert cause["detail"]["judging"]["unread"] == 3
    # Three asked, three answers, then nobody asked: the fourth was never read.
    assert provider.releases_asked_for == ["r-1", "r-2", "r-3"]
    assert lookup.asked == [isrc(1), isrc(2), isrc(3)]
    assert sorted(item_states(job_id).values()) == ["done"] * 3 + ["pending"] * 2
    assert held_ids(installed) == []
    for release_id in ("r-1", "r-2", "r-3"):
        stamped = item_of(installed, release_id).payload
        assert (stamped[GATE], stamped[ANSWER]) == ("not-judged", "unreachable")
    assert GATE not in item_of(installed, "r-4").payload
    # Resumed once the catalogue answers, the run picks up where it stopped.
    lookup.table = {isrc(n): ("Christian",) for n in range(1, 6)}
    envelope = resumed(job_id)
    assert lookup.asked[3:] == [isrc(4), isrc(5)]
    assert held_ids(installed) == ["r-4", "r-5"]
    assert counts(judging(envelope)) == tally(2, 2, 0, 3)
    assert warning_codes(envelope) == [judge_cli.CATALOGUE_UNREAD, judge_cli.NOT_JUDGED_LEFT]
    assert "could not be read for 3 release(s)" in envelope["warnings"][0]["message"]
    # And another run asks about the three that went unread.
    _, again = judge_once()
    assert lookup.asked[5:] == [isrc(1), isrc(2), isrc(3)]
    assert held_ids(installed) == ["r-4", "r-5", "r-1", "r-2", "r-3"]
    assert counts(judging(again)) == tally(3, 3, 0, 0)


def test_an_answer_between_two_unread_ones_keeps_the_run_going(installed, monkeypatch):
    lookup = Lookup({isrc(n): ("Dance",) if n == 3 else "unreachable" for n in range(1, 6)})
    five_pending(installed, monkeypatch, lookup)
    _, envelope = judge_once()
    assert len(lookup.asked) == 5
    assert counts(judging(envelope)) == tally(1, 0, 1, 4)
    assert judging(envelope)["unread"] == 4


def test_a_refusal_from_the_provider_parks_the_run_on_that_refusal(installed, monkeypatch):
    """An expired session is about this machine's account and not about one release."""
    register()
    queue_release(installed, "r-1", "r-2")
    class Expired(FakeCatalogue):
        refusing = True
        def release_tracks(self, release_id):
            if self.refusing and release_id == "r-2":
                raise refuse(
                    "credential-missing", "the provider session has expired",
                    steps=("log in again with: crate login",), origin=("suite",),
                )
            return super().release_tracks(release_id)
    fake = Expired(releases={
        f"r-{n}": ([Track(f"t-{n}", "Artist", "Song", isrc(n))], 2026) for n in (1, 2)
    })
    serve(monkeypatch, fake, Lookup({isrc(1): ("Dance",), isrc(2): ("Christian",)}))
    job_id = queued_job()
    parked = parked_on(job_id)
    assert parked["cause"]["reason"] == "credential-missing"
    assert parked["cause"]["remediation"]["steps"][0] == "log in again with: crate login"
    assert parked["cause"]["detail"]["left"] == 1
    assert sorted(item_states(job_id).values()) == ["done", "pending"]
    assert GATE not in item_of(installed, "r-2").payload
    fake.refusing = False
    envelope = resumed(job_id)
    assert held_ids(installed) == ["r-2"]
    assert counts(judging(envelope)) == tally(2, 1, 1, 0)


def test_three_provider_reads_failing_in_a_row_stop_the_run(installed, monkeypatch):
    register()
    ids = [f"r-{n}" for n in range(1, 6)]
    queue_release(installed, *ids)
    class Down(FakeCatalogue):
        down = True
        def release_tracks(self, release_id):
            self.releases_asked_for.append(release_id)
            if self.down:
                raise ConnectionError("the provider did not answer")
            self.releases_asked_for.pop()
            return super().release_tracks(release_id)
    fake = Down(releases={
        rid: ([Track(f"t-{rid}", "Artist", "Song", isrc(n))], 2026)
        for n, rid in enumerate(ids, start=1)
    })
    lookup = Lookup({isrc(n): ("Christian",) for n in range(1, 6)})
    serve(monkeypatch, fake, lookup)
    job_id = queued_job()
    parked = parked_on(job_id)
    assert parked["cause"]["reason"] == "unavailable-transient"
    assert "the provider failed 3 release reads in a row" in parked["cause"]["message"]
    assert parked["cause"]["detail"]["left"] == 2
    assert fake.releases_asked_for == ["r-1", "r-2", "r-3"]
    assert lookup.asked == []
    # Asked for, not read: a read that failed spent its calls all the same.
    assert parked["cause"]["detail"]["judging"]["asked"] == 3
    stamped = item_of(installed, "r-1").payload
    assert stamped[GATE] == "not-judged"
    said = stamped[NOTE]
    assert "its tracks could not be read from the provider (ConnectionError" in said
    assert stamped[ANSWER] == "not-asked"
    fake.down = False
    resumed(job_id)
    assert held_ids(installed) == ["r-4", "r-5"]


def unreadable_taxonomy(cfg: config.Config) -> None:
    path = config.state_path("taxonomy_active", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("this is not a taxonomy = = =", encoding="utf-8")


def test_a_taxonomy_that_cannot_be_read_refuses_before_anything_is_queued(installed):
    register()
    queue_release(installed, "r-1")
    unreadable_taxonomy(installed)
    code, envelope = judge()
    assert code != int(ExitCode.OK)
    assert envelope["outcome"] != "ok"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_taxonomy_that_stops_being_readable_parks_the_run_and_fails_no_release(
    installed, monkeypatch
):
    """One cause, one stop. Failing each release in turn would mark a whole queue failed."""
    provider = pending(installed, monkeypatch, {"r-1": isrc(1), "r-2": isrc(2)}, never_asked)
    job_id = queued_job()
    unreadable_taxonomy(installed)
    parked = parked_on(job_id)
    assert parked["cause"]["detail"]["left"] == 2
    assert set(item_states(job_id).values()) == {"pending"}
    assert provider.releases_asked_for == []


def test_a_library_whose_taxonomy_has_no_published_rules_holds_nothing_and_asks_nothing(
    installed, monkeypatch
):
    provider = pending(installed, monkeypatch, {"r-christian": isrc(1)}, never_asked)
    active_copy_without_published_rules(installed)
    _, envelope = judge_once()
    assert provider.releases_asked_for == []
    assert held_ids(installed) == []
    note = item_of(installed, "r-christian").payload[NOTE]
    assert "declares no rule" in note
    assert counts(judging(envelope)) == tally(0, 0, 0, 1)


def test_the_verb_drives_no_job_but_its_own(installed, monkeypatch):
    register()
    fake = FakeCatalogue(artists={SLUG: FakePagedArtist([])})
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    other = queued_sweep()
    code, envelope = judge("--job", other)
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "job-unknown"
    assert "is not a judging job" in envelope["cause"]["message"]
    assert set(item_states(other).values()) == {"pending"}


def test_a_job_that_finished_reports_the_same_counts_when_asked_again(installed, monkeypatch):
    lookup = Lookup({isrc(1): ("Christian",)})
    pending(installed, monkeypatch, {"r-christian": isrc(1)}, lookup)
    job_id, first = judge_once()
    second = resumed(job_id)
    assert judging(second) == judging(first)
    assert lookup.asked == [isrc(1)]


def test_a_release_another_job_withheld_meanwhile_is_not_filed_again(installed, monkeypatch):
    """Two judging jobs can hold the same items. A stamp must not re-create one."""
    register()
    item_id = queue_release(installed, "r-1")
    provider_of(monkeypatch, {"r-1": isrc(1)})
    def withheld_meanwhile(value):
        with review.open_store(installed) as store:
            withhold(store, item_id, run_id="another-job")
        return published.Published(published.SOURCE, "unreachable", note="timed out")
    bind_lookup(monkeypatch, withheld_meanwhile)
    job_id, envelope = judge_once()
    assert filed(installed) == {}
    assert held_ids(installed) == ["r-1"]
    with review.open_store(installed) as store:
        [hold] = review.holds(store, queue=QUEUE)
    assert hold.run_id == "another-job"
    assert reports(installed, job_id)["r-1"]["outcome"] == "not-judged"


def test_a_release_another_job_held_while_this_one_was_asking_is_counted_held(
    installed, monkeypatch
):
    """Reported as what it is now. Not as gone, and not as decided by a person."""
    register()
    item_id = queue_release(installed, "r-1")
    provider_of(monkeypatch, {"r-1": isrc(1)})
    def withheld_meanwhile(value):
        with review.open_store(installed) as store:
            withhold(store, item_id, run_id="another-job", reason="the other job's reason")
        return published.Published(published.SOURCE, "matched", genres=("Christian",))
    bind_lookup(monkeypatch, withheld_meanwhile)
    job_id, envelope = judge_once()
    report = reports(installed, job_id)["r-1"]
    assert (report["outcome"], report["reason"], report["asked"]) == (
        "held", "the other job's reason", True,
    )
    assert counts(judging(envelope)) == tally(1, 1, 0, 0)
    assert judging(envelope)["gone"] == 0
    assert held_ids(installed) == ["r-1"]


def moved_registry(monkeypatch, old_id: str) -> None:
    """The registry as it reads after a label's identifier moved from ``old_id``."""
    real = labels.RegistryStore.load
    def load(self):
        held = real(self)
        return labels.Registry(labels=dict(held.labels), renamed={old_id: SLUG})
    monkeypatch.setattr(labels.RegistryStore, "load", load)


def test_a_release_filed_under_a_labels_old_identifier_is_in_a_run_scoped_to_the_label(
    installed, monkeypatch
):
    """The scope reads the registry the way the worker does, and the hold is the label's."""
    lookup = Lookup({isrc(1): ("Christian",)})
    pending(installed, monkeypatch, {"r-1": isrc(1)}, lookup, label_id="tide-works-old")
    moved_registry(monkeypatch, "tide-works-old")
    _, envelope = judge_once("--label", LABEL)
    assert [row["label_id"] for row in judging(envelope)["labels"]] == [SLUG]
    with review.open_store(installed) as store:
        # Under the identifier the label has now, which is where a sweep looks.
        [hold] = review.holds(store, queue=QUEUE, group=SLUG)
    assert hold.identity == {"release_id": "r-1"}


def test_a_release_held_under_an_earlier_holds_run_is_counted_held_when_it_is_redone(
    installed, monkeypatch
):
    """The hold keeps the run that FIRST held the release, which is not this job's."""
    register()
    item_id = queue_release(installed, "r-1")
    with review.open_store(installed) as store:
        held_by_hand(store, payload={"identity": "r-1"}, reason="an older reason", run_id="sweep-0")
    provider_of(monkeypatch, {"r-1": isrc(1)}, Lookup({isrc(1): ("Christian",)}))
    job_id, _ = judge_once()
    with review.open_store(installed) as store:
        assert review.find_hold(store, queue=QUEUE, item_id=item_id).run_id == "sweep-0"
    bind_lookup(monkeypatch, never_asked)
    redone = judge_cli._judge_one(SimpleNamespace(job_id=job_id), item_id, installed)
    assert (redone["outcome"], redone["release_id"], redone["label_id"]) == ("held", "r-1", SLUG)
    assert "which is christian and not dance" in redone["reason"]


def test_an_item_that_left_review_with_no_hold_is_reported_gone(installed):
    redone = judge_cli._judge_one(SimpleNamespace(job_id="job-1"), "rv-nobody", installed)
    assert redone["outcome"] == judge_cli.GONE


def test_the_taxonomy_and_the_registry_are_read_once_for_the_job(installed, monkeypatch):
    register()
    queue_release(installed, "r-1", "r-2", "r-3", published_genres=["Dance"])
    job_id = queued_job()
    loads: list[str] = []
    real_taxonomy = active_taxonomy.load
    real_registry = judge_cli.labels.RegistryStore.load
    def taxonomy(cfg):
        loads.append("taxonomy")
        return real_taxonomy(cfg)
    def followed(self):
        loads.append("registry")
        return real_registry(self)
    monkeypatch.setattr(active_taxonomy, "load", taxonomy)
    monkeypatch.setattr(judge_cli.labels.RegistryStore, "load", followed)
    envelope = resumed(job_id)
    assert counts(judging(envelope))["passed"] == 3
    assert sorted(loads) == ["registry", "taxonomy"]


def test_the_reader_forgets_each_release_and_keeps_its_count_of_failures(installed, monkeypatch):
    class Flaky(FakeCatalogue):
        def release_tracks(self, release_id):
            if release_id.startswith("bad"):
                raise ConnectionError("no answer")
            return super().release_tracks(release_id)
    flaky = Flaky(releases={"r-1": ([Track("t-1", "A", "S", isrc(1))], 2026)})
    reader = catalogue.ReleaseTracks(flaky)
    reader.release_tracks("r-1")
    for release_id in ("bad-1", "bad-2"):
        with pytest.raises(ConnectionError):
            reader.release_tracks(release_id)
        reader.forget()
    assert reader._read == {}
    assert not reader.given_up
    with pytest.raises(ConnectionError):
        reader.release_tracks("bad-3")
    reader.forget()
    assert reader.given_up
    pending(installed, monkeypatch, {"r-1": isrc(1)}, Lookup({isrc(1): ("Dance",)}))
    job_id, _ = judge_once()
    assert judge_cli._JOB_TOOLS[job_id].reader._read == {}


def test_the_next_sweep_keeps_the_hold_and_does_not_file_the_release_again(installed, monkeypatch):
    """The reason the item leaves the queue: a sweep drops a hold on a queued release."""
    register()
    queue_release(installed, "r-christian")
    fake = FakeCatalogue(
        artists={SLUG: FakePagedArtist([FakeRelease("r-christian", year="2026")])},
        releases={"r-christian": ([Track("t-1", "Label Act", "Release", isrc(1))], 2026)},
    )
    serve(monkeypatch, fake, Lookup({isrc(1): ("Christian",)}))
    job_id, _ = judge_once()
    assert held_ids(installed) == ["r-christian"]
    bind_lookup(monkeypatch, never_asked)
    sweep_once()
    assert held_ids(installed) == ["r-christian"]
    assert filed(installed) == {}
    with review.open_store(installed) as store:
        [hold] = review.holds(store, queue=QUEUE)
    assert hold.run_id == job_id
    # The sweep's rewrite kept the filing run, so a return files it as the old release.
    assert hold.payload[sweep.SWEEP_RUN] == FILED_BY
    assert held_verb("return", "r-christian")[0] == int(ExitCode.OK)
    assert item_of(installed, "r-christian").payload[sweep.SWEEP_RUN] == FILED_BY


def test_label_held_does_not_say_a_sweep_was_refused_over_what_a_judge_run_met(
    installed, monkeypatch
):
    pending(installed, monkeypatch, {"r-1": isrc(1)}, Lookup({isrc(1): "unreachable"}))
    with review.open_store(installed) as store:
        review.record_round(store, queue=QUEUE, run_id=FILED_BY, group=SLUG, name=LABEL, beyond=0)
    judge_once()
    assert item_of(installed, "r-1").payload[ANSWER] == "unreachable"
    listing = held_ok()
    [swept] = listing["data"]["summary"]["sweeps"]
    # Still not judged, but neither asked nor unread by the SWEEP, which asked nobody.
    assert (swept["filed"], swept["asked"], swept["unread"], swept["not_judged"]) == (1, 0, 0, 1)
    line = check(listing, f"label.held.sweep.{SLUG}")
    assert line["status"] == "info"
    assert "the genre gate could not judge 1 of them" in line["detail"]
    assert "because the general catalogue could not be read" not in line["detail"]


def test_a_release_a_sweep_held_is_still_returned_under_that_sweep(installed, monkeypatch):
    """The run a return files under is the payload's when it names one, else the hold's."""
    register()
    with review.open_store(installed) as store:
        review.hold(
            store, queue=QUEUE, kind=sweep.KIND, identity={"release_id": "r-swept"},
            payload={"identity": "r-swept", "label_id": SLUG, "label_name": LABEL, "title": "T"},
            group=SLUG, name=LABEL, reason="held by a sweep",
            detail={"genres": ["Christian"], "kind": "dance", "placed": []}, run_id="sweep-9",
        )
    held_ok("return", "r-swept")
    assert item_of(installed, "r-swept").payload[sweep.SWEEP_RUN] == "sweep-9"


def test_a_withheld_release_the_window_does_not_reach_is_not_dropped_when_its_kind_changes(
    installed, monkeypatch
):
    """It was in front of a person. Dropped past the window, it would be in neither place."""
    register("--offer", "1")
    queue_release(installed, "r-new", "r-old")
    listed = [FakeRelease("r-new", year="2026"), FakeRelease("r-old", year="2020")]
    fake = FakeCatalogue(artists={SLUG: FakePagedArtist(listed)}, releases={
        "r-new": ([Track("t-new", "Label Act", "New", isrc(1))], 2026),
        "r-old": ([Track("t-old", "Label Act", "Old", isrc(2))], 2020),
    })
    serve(monkeypatch, fake, Lookup({isrc(1): ("Dance",), isrc(2): ("Christian",)}))
    judge_once()
    assert held_ids(installed) == ["r-old"]
    assert drive(["label", "registry", "set", LABEL, "--kind", "any"])[0] == int(ExitCode.OK)
    bind_lookup(monkeypatch, never_asked)
    sweep_once()
    assert held_ids(installed) == ["r-old"]
    assert sorted(filed(installed)) == ["r-new"]
    listing = held_ok()
    assert "release r-old" in check(listing, "label.held.release.r-old")["detail"]
    assert held_verb("return", "r-old")[0] == int(ExitCode.OK)
    assert sorted(filed(installed)) == ["r-new", "r-old"]


def test_a_withheld_release_filed_before_runs_were_recorded_is_returned_under_no_run(
    installed, monkeypatch
):
    """Never under the judging job, which filed nothing."""
    lookup = Lookup({isrc(1): ("Christian",)})
    pending(installed, monkeypatch, {"r-legacy": isrc(1)}, lookup, filed_by=None)
    assert sweep.SWEEP_RUN not in item_of(installed, "r-legacy").payload
    judge_once()
    held_ok("return", "r-legacy")
    back = item_of(installed, "r-legacy").payload
    assert sweep.SWEEP_RUN not in back
    assert review.WITHHELD_FIELD not in back


def test_a_stale_hold_beside_a_release_the_gate_passes_is_dropped(installed, monkeypatch):
    """In review and still held. The queue is the truth, as the sweep reads it."""
    register()
    item_id = queue_release(installed, "r-dance")
    with review.open_store(installed) as store:
        held_by_hand(
            store, release_id="r-dance", payload={"identity": "r-dance"}, reason="an older reason",
            run_id="sweep-0",
        )
    provider_of(monkeypatch, {"r-dance": isrc(2)}, Lookup({isrc(2): ("Dance",)}))
    judge_once()
    assert held_ids(installed) == []
    assert item_of(installed, "r-dance").item_id == item_id
    assert item_of(installed, "r-dance").payload[GATE] == "passed"


def test_the_verb_is_declared_queued_adjudicating_and_not_destructive():
    entry = registry.entry("label.judge")
    assert entry.long_running and entry.adjudicates
    assert not entry.destructive and entry.writes == frozenset()
    assert entry.output_schema == "job_state/1"
    assert handlers.HANDLERS[entry.handler_key] == "cratekit.label.judge_cli:handle"
    assert handlers.resolve(entry.handler_key) is judge_cli.handle


def test_the_command_that_continues_a_job_names_the_job(installed):
    register()
    queue_release(installed, "r-1")
    job_id = queued_job()
    with jobs.open_store() as store:
        argv = judge_cli.label_judge_argv(jobs.get(store, job_id))
    assert argv == ["label", "judge", "--job", job_id]


def test_a_person_reads_the_counts_per_label_without_asking_for_json(installed, monkeypatch):
    lookup = Lookup({isrc(1): ("Christian",), isrc(2): ("Dance",)})
    releases = {"r-christian": isrc(1), "r-dance": isrc(2), "r-unknown": isrc(3)}
    pending(installed, monkeypatch, releases, lookup)
    job_id = queued_job()
    code, text = human(["label", "judge", "--job", job_id])
    assert code == int(ExitCode.OK), text
    assert "  releases: 2 judged, 1 held, 1 passed, 1 not judged" in text
    assert "    Tide Works: 2 judged, 1 held, 1 passed, 1 not judged" in text
    assert "  the held releases are listed by: crate label held" in text


def test_a_job_that_has_not_run_prints_no_counts(installed):
    register()
    queue_release(installed, "r-1")
    code, text = human(["label", "judge"])
    assert code == int(ExitCode.OK), text
    assert "releases:" not in text
    assert "drive it with: crate label judge --job" in text
