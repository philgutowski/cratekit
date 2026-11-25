"""U4, U5 and U6: the label verbs queue real items, run them, and harvest."""

from __future__ import annotations

import io
from dataclasses import replace

import pytest
from tidalapi.exceptions import TooManyRequests

from cratekit import cli
from cratekit.cli import handlers, output, registry, render
from cratekit.core import config, jobs, review, tombstone
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.label import catalogue, sweep
from cratekit.label import cli as label_cli
from cratekit.label import registry as label_registry
from cratekit.label.catalogue import ReleaseUnresolvable
from tests.cli_drive import drive
from tests.label_fakes import (
    FakeCatalogue,
    FakePagedArtist,
    FakePagedPlaylist,
    FakeRelease,
    FakeTrack,
    UnlistablePlaylist,
    UnreadableCatalogue,
    VerificationOutage,
    catalogue_factory,
)
from tests.test_config import valid_data

SWEEP_KEY = "sync.labels"
IMPORT_KEY = "label.import"

#: Display names whose slugs differ from them, so an item keyed on a name fails (R19, D5).
LABELS = ("Hotflush Recordings", "Ostgut Ton", "Kompakt")
SLUGS = ("hotflush-recordings", "ostgut-ton", "kompakt")


@pytest.fixture
def installed(tmp_path, monkeypatch):
    """A machine the real dispatcher can load, with every module switched on."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    return resolved


#: The parser per module membership, shared by drives: building it is most of a drive's CPU.
_PARSERS: dict = {}


@pytest.fixture(autouse=True)
def one_parser(monkeypatch):
    """Every drive parses with the one parser its membership builds."""
    build = cli.build_parser
    def shared(*args, **kwargs):
        if args or kwargs:
            return build(*args, **kwargs)
        membership = cli._membership()
        if membership not in _PARSERS:
            _PARSERS[membership] = build()
        return _PARSERS[membership]
    monkeypatch.setattr(cli, "build_parser", shared)


def register(*names: str) -> None:
    """Put labels in the registry through the real verb, not through the store."""
    for name in names:
        code, envelope = drive(["label", "registry", "add", name])
        assert code == int(ExitCode.OK), envelope


def queued_items(job_id: str) -> list[str]:
    """The item identifiers one job carries, in ordinal order."""
    with jobs.open_store() as store:
        return [item.item_id for item in jobs.items(store, job_id)]


def queue_is_empty() -> bool:
    with jobs.open_store() as store:
        return not jobs.list_jobs(store)


#: Releases per label, their identifiers naming the label, so a label swept twice shows.
RELEASES = {"hotflush-recordings": ("hf-1", "hf-2"), "ostgut-ton": ("ot-1",), "kompakt": ("ko-1",)}


def artists_of(*label_ids: str) -> dict:
    """Each label's listing of its ``RELEASES``, keyed as the seam keys it."""
    return {
        label_id: FakePagedArtist([FakeRelease(release_id) for release_id in RELEASES[label_id]])
        for label_id in label_ids
    }


def readable(*label_ids: str, **kwargs) -> FakeCatalogue:
    """A catalogue that can list exactly these labels, keyed as the seam keys it."""
    return FakeCatalogue(artists=artists_of(*label_ids), **kwargs)


def bind(monkeypatch, fake: FakeCatalogue) -> FakeCatalogue:
    """Put ``fake`` in front of the provider seam for this test."""
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def refused_by(argv: list[str]) -> dict:
    """Drive ``argv``, which must refuse on a precondition. Its envelope."""
    code, refused = drive(argv)
    assert code == int(ExitCode.PRECONDITION), refused
    return refused


def imported(name: str) -> dict:
    """Queue an import of ``name`` through the real verb, which must succeed."""
    code, queued = drive(["label", "import", name])
    assert code == int(ExitCode.OK), queued
    return queued


def queued_job(verb: list[str]) -> str:
    """Queue through the real verb and return the job identifier."""
    code, envelope = drive(verb)
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"]


def sweep_job(monkeypatch, fake: FakeCatalogue, *names: str) -> str:
    """Register ``names``, bind ``fake``, and file a sweep. Its job id."""
    register(*names)
    bind(monkeypatch, fake)
    return queued_sweep()


def queued_sweep(run_id: str | None = None) -> str:
    """File a labels sweep the way a build before U109 did, and return its id."""
    cfg = config.load()
    held = label_registry.RegistryStore().load()
    items = tuple(entry.label_id for entry in held.labels.values())
    assert items, "register a label before filing a sweep, as the old verb refused"
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key=SWEEP_KEY,
            payload={"source_id": "labels", "run_id": run_id or output.new_run_id()},
            item_ids=items, cfg=cfg,
        )
    return job.job_id


def swept(job_id: str) -> dict:
    """Drive a queued sweep through ``sync labels --job``, which must succeed."""
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    return resumed


def unswept(job_id: str) -> dict:
    """Drive a queued sweep through ``sync labels --job``, which must not succeed."""
    code, failed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    return failed


def item_states(job_id: str) -> dict[str, str]:
    with jobs.open_store() as store:
        return {item.item_id: str(item.state) for item in jobs.items(store, job_id)}


def item_causes(job_id: str) -> dict[str, str | None]:
    """Each item's OWN cause, which is not the same thing as the job's."""
    with jobs.open_store() as store:
        return {
            item.item_id: (item.cause.reason if item.cause is not None else None)
            for item in jobs.items(store, job_id)
        }


def item_cause_message(job_id: str, item_id: str) -> str:
    """One item's cause SENTENCE, which is the half a slug cannot carry."""
    with jobs.open_store() as store:
        for item in jobs.items(store, job_id):
            if item.item_id == item_id:
                assert item.cause is not None, f"item {item_id} carries no cause"
                return item.cause.message
    raise AssertionError(f"job {job_id} has no item {item_id}")


def job_state(job_id: str) -> str:
    with jobs.open_store() as store:
        return str(jobs.get(store, job_id).state)


def job_is_open(job_id: str) -> bool:
    with jobs.open_store() as store:
        return jobs.get(store, job_id).is_open()


def offers(cfg: config.Config) -> dict[str, str]:
    """The label-release queue under ``cfg``, as release identity to label id."""
    with review.open_store(cfg) as store:
        page = review.list_items(store, queue=str(review.Queue.LABEL_RELEASE))
    return {
        str(item.payload.get("identity")): str(item.payload.get("label_id"))
        for item in page.items
    }


# ── 1. The sweep's queueing half is retired (U109) ───────────────────────────


def test_sync_labels_refuses_to_queue_and_names_the_guided_verb(installed):
    """Labels registered, so the old verb would have queued, and it queues nothing."""
    register(*LABELS)
    refused = refused_by(["sync", "labels"])
    assert refused["cause"]["reason"] == "verb-retired"
    assert "crate label sync" in refused["cause"]["message"]
    steps = refused["cause"]["remediation"]["steps"]
    assert any(step.endswith(": crate label sync") for step in steps), steps
    assert any("--job" in step for step in steps), steps
    assert queue_is_empty()


def test_the_retired_refusal_reads_nothing_so_a_fresh_install_gets_it_too():
    """No ``installed`` fixture: a machine that was never set up."""
    refused = refused_by(["sync", "labels"])
    assert refused["cause"]["reason"] == "verb-retired"
    assert queue_is_empty()


def test_a_sweep_queued_before_u109_still_resumes_to_done(installed, monkeypatch):
    """The other half of retiring by reduction: an old job is never dropped."""
    job_id = sweep_job(monkeypatch, readable(*SLUGS[:2]), *LABELS[:2])
    assert queued_items(job_id) == list(SLUGS[:2])
    swept(job_id)
    assert set(item_states(job_id).values()) == {str(jobs.ItemState.DONE)}
    assert set(offers(config.load()).values()) == set(SLUGS[:2])


# ── 2. The import's one item ─────────────────────────────────────────────────


def test_an_import_queues_exactly_one_item_and_it_is_the_label_id(installed):
    """Driven by DISPLAY NAME and asserted on the identifier, which is the point."""
    register(*LABELS)
    queued = imported("Ostgut Ton")
    assert queued_items(queued["data"]["job_id"]) == ["ostgut-ton"]


@pytest.mark.parametrize(
    "held, name",
    [
        # R6: the import cannot queue an empty job because it refuses first.
        pytest.param(LABELS, "no-such-label", id="unregistered-name"),
        # The two refusals stay distinguishable when both conditions hold at once.
        pytest.param((), "Kompakt", id="empty-registry"),
    ],
)
def test_an_import_of_an_unregistered_name_refuses_and_queues_nothing(installed, held, name):
    register(*held)
    refused = refused_by(["label", "import", name])
    assert refused["cause"]["reason"] == "label-unknown"
    assert queue_is_empty()


# ── 3. The unbound catalogue is a warning, not a refusal ─────────────────────


def test_the_import_queues_without_a_warning_now_an_adapter_is_bound(installed):
    assert catalogue.bound() is True
    register(*LABELS)
    queued = imported("Kompakt")
    codes = {warning["code"] for warning in queued.get("warnings") or ()}
    assert "label-catalogue-unbound" not in codes
    assert queued_items(queued["data"]["job_id"])


def test_the_unbound_warning_says_the_job_will_fail_at_the_provider_seam(installed, monkeypatch):
    """A code alone is a slug; the sentence is what a person reads."""
    monkeypatch.setattr(catalogue, "bound", lambda: False)
    register(*LABELS)
    queued = imported("Kompakt")
    said = [
        warning["message"]
        for warning in queued.get("warnings") or ()
        if warning["code"] == "label-catalogue-unbound"
    ]
    assert said and "provider seam" in said[0], queued.get("warnings")
    assert queued_items(queued["data"]["job_id"])


def test_a_refused_sweep_carries_no_warning_because_nothing_was_queued(installed, monkeypatch):
    """The warning belongs to a queued job, so a refusal must not carry one."""
    monkeypatch.setattr(catalogue, "bound", lambda: False)
    register(*LABELS)
    refused = refused_by(["sync", "labels"])
    assert not (refused.get("warnings") or ())


def test_the_warning_rides_the_envelope_rather_than_the_job_state_payload(installed, monkeypatch):
    """KTD7: the payload stays exactly the four ``job_state/1`` keys."""
    monkeypatch.setattr(catalogue, "bound", lambda: False)
    register(*LABELS)
    queued = imported("Kompakt")
    assert set(queued["data"]) == {"job_id", "state", "cause", "progress"}
    assert queued.get("warnings")


# ── 4. The bindings themselves ───────────────────────────────────────────────


def test_both_label_keys_report_a_bound_worker_rather_than_a_reason_they_have_none():
    """``crate job show``'s worker field, at the source it is derived from."""
    for key in (SWEEP_KEY, IMPORT_KEY):
        assert handlers.is_known(key), key
        assert handlers.unbound_reason(key) is None, key
        assert callable(handlers.resolve(key)), key


def test_neither_label_key_is_recorded_as_unbound_now_that_both_are_bound():
    """Deleting the exemption is the other half of adding the binding."""
    for key in (SWEEP_KEY, IMPORT_KEY):
        assert key not in handlers.HANDLERS_NOT_YET_BOUND, key
        assert key in handlers.HANDLERS, key


def test_the_two_bound_keys_are_the_ones_the_registry_declares():
    """Derived, so a renamed handler key fails here rather than at a queue."""
    declared = {
        entry.handler_key
        for entry in registry.ENTRIES
        if entry.landed and entry.long_running
    }
    assert {SWEEP_KEY, IMPORT_KEY} <= declared


def test_one_worker_serves_both_label_keys():
    """The sweep and the import differ in how many items they queue, not in work."""
    assert handlers.resolve(SWEEP_KEY) is handlers.resolve(IMPORT_KEY)
    assert handlers.resolve(SWEEP_KEY) is label_cli.handle


# ── 5. A queued sweep runs ───────────────────────────────────────────────────


def test_a_sweep_runs_every_one_of_its_labels_from_pending_to_done(installed, monkeypatch):
    job_id = sweep_job(monkeypatch, readable(*SLUGS[:2]), *LABELS[:2])
    assert set(item_states(job_id).values()) == {str(jobs.ItemState.PENDING)}
    resumed = swept(job_id)
    assert item_states(job_id) == {slug: str(jobs.ItemState.DONE) for slug in SLUGS[:2]}
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)


def test_each_item_sweeps_its_own_label_and_not_one_named_by_the_payload(installed, monkeypatch):
    register(*LABELS[:2])
    catalogue_fake = bind(monkeypatch, readable(*SLUGS[:2]))
    job_id = queued_sweep()
    swept(job_id)
    assert offers(installed) == {
        "hf-1": "hotflush-recordings", "hf-2": "hotflush-recordings", "ot-1": "ostgut-ton",
    }
    assert catalogue_fake.asked_for == list(SLUGS[:2])


def test_an_import_runs_its_one_item_to_done_through_the_same_worker(installed, monkeypatch):
    """The second key, driven through the real dispatcher rather than by calling handle."""
    register(LABELS[2])
    bind(monkeypatch, readable(SLUGS[2]))
    job_id = queued_job(["label", "import", "Kompakt"])
    code, resumed = drive(["label", "import", "Kompakt", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert item_states(job_id) == {SLUGS[2]: str(jobs.ItemState.DONE)}
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)


def test_the_resume_envelope_is_exactly_job_state_and_nothing_beside_it(installed, monkeypatch):
    """KTD7: no artifact, no per verb detail, four keys."""
    job_id = sweep_job(monkeypatch, readable(SLUGS[0]), LABELS[0])
    resumed = swept(job_id)
    assert set(resumed["data"]) == {"job_id", "state", "cause", "progress"}


# ── 6. What a failing round does ─────────────────────────────────────────────


def test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job(installed, monkeypatch):
    """R-135 through the binding: an unreadable listing is not a quiet label."""
    job_id = sweep_job(monkeypatch, UnreadableCatalogue(), LABELS[0])
    failed = unswept(job_id)
    assert item_causes(job_id) == {SLUGS[0]: "sync-source-lookups-failed"}
    assert job_state(job_id) == str(jobs.JobState.FAILED)
    assert failed["cause"]["reason"] == "no-evidence"
    assert failed["cause"]["retryable"] is False
    assert failed["cause"]["remediation"]["remedy"] != "resume-job"
    inner = failed["cause"]["inner"]
    assert inner is not None
    assert inner["reason"] == "sync-source-lookups-failed"


def test_a_sweep_whose_failures_are_permanent_does_not_tell_the_person_to_resume(
    installed, monkeypatch
):
    job_id = sweep_job(monkeypatch, readable(SLUGS[0]), *LABELS[:2])
    failed = unswept(job_id)
    assert item_causes(job_id) == {SLUGS[0]: None, SLUGS[1]: "sync-source-lookups-failed"}
    assert job_state(job_id) == str(jobs.JobState.FAILED)
    cause = failed["cause"]
    assert cause["reason"] == "sync-source-lookups-failed"
    assert cause["retryable"] is False
    assert cause["remediation"]["remedy"] != "resume-job"
    assert "finished 1 items and failed 1" in cause["message"]
    assert cause["inner"] is not None
    assert cause["inner"]["reason"] == "sync-source-lookups-failed"


def test_an_increment_that_could_not_offer_every_release_fails_the_item(installed, monkeypatch):
    """A partial round FAILS rather than completing, which is a decision."""
    def refusing_offer(store, candidate, **kwargs):
        del store, kwargs
        raise RuntimeError(f"the review queue rejected {candidate.identity}")
    monkeypatch.setattr(sweep, "offer_release", refusing_offer)
    job_id = sweep_job(monkeypatch, readable(SLUGS[0]), LABELS[0])
    unswept(job_id)
    assert item_causes(job_id) == {SLUGS[0]: "label-sweep-incomplete"}
    assert job_state(job_id) == str(jobs.JobState.FAILED)


def test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing(
    installed, monkeypatch
):
    """The registry can move between enqueue and drive, and the items cannot."""
    job_id = sweep_job(monkeypatch, readable(*SLUGS[:2]), *LABELS[:2])
    code, removed = drive(["label", "registry", "remove", LABELS[0]])
    assert code == int(ExitCode.OK), removed
    unswept(job_id)
    causes = item_causes(job_id)
    assert causes[SLUGS[0]] == "label-unknown"
    assert causes[SLUGS[1]] is None
    assert item_states(job_id)[SLUGS[1]] == str(jobs.ItemState.DONE)


# ── 6b. Confirming nothing is not nothing new: keyed on the drops, a quiet label stays a no op ──


def unconfirming(*label_ids: str) -> FakeCatalogue:
    """A catalogue that lists these labels and confirms none of what it lists."""
    return readable(*label_ids, confirmed=frozenset())


def test_a_sweep_that_confirmed_none_of_what_it_read_fails_rather_than_succeeding(
    installed, monkeypatch
):
    job_id = sweep_job(monkeypatch, unconfirming(SLUGS[0]), LABELS[0])
    unswept(job_id)
    assert item_causes(job_id) == {SLUGS[0]: "label-sweep-incomplete"}
    assert job_state(job_id) != str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_the_unconfirmed_refusal_says_how_many_were_read_and_that_the_provider_answered(
    installed, monkeypatch
):
    """Two different problems, two different remedies, so the sentence separates them."""
    job_id = sweep_job(monkeypatch, unconfirming(SLUGS[0]), LABELS[0])
    drive(["sync", "labels", "--job", job_id])
    said = item_cause_message(job_id, SLUGS[0])
    assert str(len(RELEASES[SLUGS[0]])) in said, said
    assert "confirm" in said, said


def test_a_label_whose_every_release_is_tombstoned_still_succeeds(installed, monkeypatch):
    """A genuine no op, and the reason the refusal is keyed on the drops."""
    for release_id in RELEASES[SLUGS[0]]:
        bury(installed, release_id)
    job_id = sweep_job(monkeypatch, readable(SLUGS[0]), LABELS[0])
    assert swept(job_id)["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_a_verification_call_that_raises_fails_the_item_in_the_lookup_vocabulary(
    installed, monkeypatch
):
    fake = VerificationOutage(artists=artists_of(SLUGS[0]), answers=0)
    job_id = sweep_job(monkeypatch, fake, LABELS[0])
    unswept(job_id)
    assert item_causes(job_id) == {SLUGS[0]: "sync-source-lookups-failed"}
    assert job_state(job_id) == str(jobs.JobState.FAILED)


def test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds(installed, monkeypatch):
    """The other no op: an exhausted crawl, which has to keep reporting empty."""
    job_id = sweep_job(monkeypatch, listing_nothing(), LABELS[0])
    assert swept(job_id)["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_a_sweep_that_confirmed_some_of_what_it_read_succeeds_and_offers_those(
    installed, monkeypatch
):
    job_id = sweep_job(monkeypatch, readable(SLUGS[0], confirmed={"hf-1"}), LABELS[0])
    assert swept(job_id)["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {"hf-1": SLUGS[0]}


class SessionExpiredAtVerification(FakeCatalogue):
    """A catalogue whose listings answer and whose verification refuses in kind."""

    def search_release(self, claimed: str, release: object) -> dict:
        raise refuse(
            "credential-missing",
            "the stored provider session expired between the listing and the verification",
            origin=("tests",),
        )

    def check_label(self, name: str) -> dict:
        return self.search_release(name, None)


def test_a_revoked_tombstone_no_longer_keeps_a_release_out_of_the_queue(installed, monkeypatch):
    """A lifted suppression lifts, which the one read of the store has to honour."""
    store = review.DecisionStore(tombstone.STORE_KEY, installed)
    recorded = store.record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist="Label Act", title="Release hf-1"),
        actor="tests",
    )
    store.revoke(recorded.suppression_id, actor="tests")
    swept(sweep_job(monkeypatch, readable(SLUGS[0]), LABELS[0]))
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}


def listing_nothing() -> FakeCatalogue:
    """The first label's crawl, exhausted with nothing listed."""
    return FakeCatalogue(artists={SLUGS[0]: FakePagedArtist([])})


def corrupt_tombstone_store(cfg: config.Config) -> None:
    """Leave a document in the tombstone store's place that it must refuse."""
    path = review.DecisionStore(tombstone.STORE_KEY, cfg).path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[]\n")


def test_an_unreadable_tombstone_store_does_not_fail_a_label_with_nothing_to_ask(
    installed, monkeypatch
):
    """THE LAZY READ, which is the behaviour preserving half of the one-read change."""
    corrupt_tombstone_store(installed)
    job_id = sweep_job(monkeypatch, listing_nothing(), LABELS[0])
    assert swept(job_id)["data"]["state"] == str(jobs.JobState.SUCCEEDED)


def test_an_unreadable_tombstone_store_still_refuses_a_label_with_a_confirmed_release(
    installed, monkeypatch
):
    """The composite for the test above: deferring the read did not lose the refusal."""
    corrupt_tombstone_store(installed)
    job_id = sweep_job(monkeypatch, readable(SLUGS[0]), LABELS[0])
    unswept(job_id)
    assert item_causes(job_id) == {SLUGS[0]: "review-file-unusable"}
    assert offers(installed) == {}


# ── 7. The resume branch ─────────────────────────────────────────────────────


def itemless(cfg: config.Config, key: str = SWEEP_KEY, **payload: str) -> jobs.Job:
    """A job frozen with no items, as a build before U52 left one."""
    with jobs.open_store() as store:
        return jobs.enqueue(
            store, handler_key=key, payload={"source_id": "labels", **payload}, cfg=cfg,
            item_ids=(),
        )


def test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open(installed):
    """A job frozen by a build before U52, met by the build that can drive it."""
    job = itemless(installed)
    code, refused = drive(["sync", "labels", "--job", job.job_id])
    assert code == int(ExitCode.INTERNAL), refused
    assert refused["cause"]["reason"] == "internal-error"
    assert job.job_id in refused["cause"]["message"]
    assert job_is_open(job.job_id), (
        "the refusal drove the job anyway, so a later resume would report a "
        "success over work nothing did"
    )


def test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok(installed, monkeypatch):
    job_id = sweep_job(monkeypatch, UnreadableCatalogue(), LABELS[0])
    assert drive(["sync", "labels", "--job", job_id])[0] != int(ExitCode.OK)
    again = unswept(job_id)
    assert again["cause"]["reason"] == "sync-source-lookups-failed"
    assert again["cause"]["retryable"] is False
    assert again["cause"]["remediation"]["remedy"] != "resume-job"
    assert job_state(job_id) == str(jobs.JobState.FAILED)


def test_a_resume_of_a_cancelled_sweep_does_not_exit_ok_over_the_items_it_never_ran(
    installed, monkeypatch
):
    """ANY closed job carrying a cause, not FAILED alone."""
    job_id = sweep_job(monkeypatch, readable(*SLUGS), *LABELS)
    with jobs.open_store() as store:
        jobs.cancel(store, job_id)
    resumed = unswept(job_id)
    assert resumed["cause"]["reason"] == "cancelled"
    assert job_state(job_id) == str(jobs.JobState.CANCELLED)
    assert set(item_states(job_id).values()) == {str(jobs.ItemState.PENDING)}


# ── 8. The frozen configuration reaches the worker ───────────────────────────


def test_the_worker_offers_into_the_library_its_job_was_queued_for(
    installed, tmp_path, monkeypatch
):
    """R17 and KTD9, on a path the worker genuinely resolves against ``cfg``."""
    job_id = sweep_job(monkeypatch, readable(SLUGS[0]), LABELS[0])
    elsewhere = tmp_path / "another-library"
    (elsewhere / "Music").mkdir(parents=True)
    (elsewhere / "db").mkdir(parents=True)
    monkeypatch.delenv(config.ENV_LIBRARY_ROOT)
    config.save(
        replace(
            installed,
            library=replace(
                installed.library, root=elsewhere, db_path=elsewhere / "db" / "master.db",
            ),
        )
    )
    config.reset_cache()
    live = config.load()
    assert live.library.root == elsewhere, (
        "the live configuration still names the queued library, so the two "
        "readings cannot differ and this test would pass either way"
    )
    assert not review.queue_path(live).exists(), (
        "the relocated library already holds a review queue, so an offer written "
        "there would be indistinguishable from one written to the frozen library"
    )
    swept(job_id)
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}
    assert not review.queue_path(live).exists(), (
        "the worker opened the review store against the CURRENT configuration, "
        "so the offers landed in a library this job was never queued for"
    )


# ── 9. Harvest queues nothing: every assertion reads the envelope or the review store ─────────

PLAYLIST = "https://example.invalid/playlist/harvest"

#: One imprint the fake confirms and one it does not, so ``unresolved`` can fail.
CONFIRMED = "Anjunadeep"
UNCONFIRMED = "Mystery Distro"


def anjuna() -> FakeTrack:
    return FakeTrack("t1", copyright="2026 Anjunadeep")


def mystery() -> FakeTrack:
    return FakeTrack("t2", copyright="2026 Mystery Distro")


def harvest_ok() -> dict:
    code, envelope = run_harvest()
    assert code == int(ExitCode.OK), envelope
    return envelope


def harvest_human_ok() -> str:
    code, text = run_harvest_human()
    assert code == int(ExitCode.OK), text
    return text


def playlist_of(*tracks: FakeTrack) -> FakeCatalogue:
    """A catalogue holding exactly one readable playlist, at ``PLAYLIST``."""
    return FakeCatalogue(
        playlists={PLAYLIST: FakePagedPlaylist(list(tracks))}, known_labels={CONFIRMED},
    )


def harvested(cfg: config.Config) -> list[str]:
    """The label names sitting in the review queue under ``cfg``, in order."""
    with review.open_store(cfg) as store:
        page = review.list_items(store, queue=str(review.Queue.LABEL_RELEASE))
    return [str(item.payload.get("name")) for item in page.items]


def run_harvest(reference: str = PLAYLIST) -> tuple[int, dict]:
    return drive(["label", "harvest", reference])


def run_harvest_human(reference: str = PLAYLIST) -> tuple[int, str]:
    """The default output a person gets."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["label", "harvest", reference], stdout=out, stderr=err)
    return code, out.getvalue() or err.getvalue()


def test_harvest_of_a_readable_playlist_offers_one_item_per_verified_label(installed, monkeypatch):
    bind(monkeypatch, playlist_of(anjuna()))
    envelope = harvest_ok()
    assert envelope["schema"] == "review_set/1"
    assert envelope["data"]["queue"] == str(review.Queue.LABEL_RELEASE)
    assert [item["name"] for item in envelope["data"]["items"]] == [CONFIRMED]
    assert harvested(installed) == [CONFIRMED]


def test_harvest_payload_is_exactly_the_three_declared_review_set_keys(installed, monkeypatch):
    """KTD7's rule on the other surface: no per verb detail beside the contract."""
    bind(monkeypatch, playlist_of(anjuna()))
    envelope = harvest_ok()
    assert set(envelope["data"]) == {"queue", "items", "unresolved"}


def test_a_name_the_catalogue_will_not_confirm_is_counted_and_never_offered(installed, monkeypatch):
    """A copyright string is a heuristic, so an unconfirmed name is not a label."""
    bind(monkeypatch, playlist_of(anjuna(), mystery()))
    envelope = harvest_ok()
    assert envelope["data"]["unresolved"] == 1
    assert harvested(installed) == [CONFIRMED]
    assert UNCONFIRMED not in harvested(installed)


def test_a_track_with_no_copyright_string_is_counted_rather_than_dropped_silently(
    installed, monkeypatch
):
    """The track that yields no NAME at all, which is not the same as a drop."""
    bind(monkeypatch, playlist_of(anjuna(), FakeTrack("t2")))
    envelope = harvest_ok()
    assert harvested(installed) == [CONFIRMED]
    assert envelope["data"]["unresolved"] == 1, (
        "the track carrying no copyright string was dropped silently, so a "
        "playlist harvest can report nothing wrong having read nothing at all"
    )


def test_an_empty_playlist_offers_nothing_and_reports_zero_rather_than_refusing(
    installed, monkeypatch
):
    """The adversarial half of the unreadable refusal, and the reason it is here."""
    bind(monkeypatch, playlist_of())
    envelope = harvest_ok()
    assert envelope["data"]["items"] == []
    assert envelope["data"]["unresolved"] == 0
    # NO_OP rather than OK: both are successes, and the difference must be readable.
    assert envelope["outcome"] == "no_op"
    assert harvested(installed) == []


QUEUE_LINE = f"  queue: {review.Queue.LABEL_RELEASE}"


@pytest.mark.parametrize("tracks, shown, hidden", [
    # The sitting's missing case: default output names what harvest found.
    pytest.param(
        [anjuna], [f"  {CONFIRMED}", "  unresolved: 0", QUEUE_LINE], [], id="names-each-label",
    ),
    # An unconfirmed copyright string is a count, never a harvested label.
    pytest.param(
        [anjuna, mystery], [f"  {CONFIRMED}", "  unresolved: 1"], [f"  {UNCONFIRMED}"],
        id="names-the-unresolved-count-and-not-an-unconfirmed-imprint",
    ),
    pytest.param(
        [], ["  unresolved: 0", QUEUE_LINE], [f"  {CONFIRMED}"], id="empty-names-nothing-offered",
    ),
])
def test_harvest_human_output_names_each_offered_label(
    installed, monkeypatch, tracks, shown, hidden
):
    bind(monkeypatch, playlist_of(*(track() for track in tracks)))
    text = harvest_human_ok()
    lines = text.splitlines()
    if not tracks:
        assert lines[0] == "label.harvest: no_op", text
    for line in shown:
        assert line in lines, text
    for line in hidden:
        assert line not in lines, text


def test_a_review_set_item_without_a_name_is_rendered_from_its_own_fields():
    """Harvest is not the only review_set verb. Do not invent a name line."""
    envelope = output.build(
        verb="review.list",
        run_id="r",
        schema=output.current_schema("review_set"),
        started="2026-08-02T00:00:00+00:00",
        data={
            "queue": "deletion",
            "items": [{"id": "abc", "kind": "removed-track", "path": "/x.flac"}], "unresolved": 3,
        },
    )
    lines = render.render_review_set(envelope)
    assert "  id=abc, kind=removed-track, path=/x.flac" in lines
    assert "  unresolved: 3" in lines


def test_review_set_rendering_is_gated_on_the_schema_not_an_items_key():
    """Same gate render_checks uses: a later surface with items is not this shape."""
    plan = output.build(
        verb="profile.set", run_id="r", schema=output.current_schema("plan"),
        started="2026-08-02T00:00:00+00:00",
        data={"digest": "d", "items": [{"name": CONFIRMED}], "totals": {}, "chunk": None},
    )
    assert render.render_review_set(plan) == []
    assert CONFIRMED not in render.render(plan)


@pytest.mark.parametrize("fake, kind", [
    # R13: the slug is earned, because a BOUND provider was asked and failed.
    pytest.param(UnreadableCatalogue, "RuntimeError", id="cannot-resolve"),
    # The second unreadable shape, which reaches the boundary as another type.
    pytest.param(
        lambda: FakeCatalogue(playlists={PLAYLIST: UnlistablePlaylist()}), "ListingNotPaginated",
        id="resolves-and-cannot-be-listed",
    ),
])
def test_a_playlist_the_catalogue_cannot_read_refuses_that_it_was_unreadable(
    installed, monkeypatch, fake, kind
):
    catalogue_fake = bind(monkeypatch, fake())
    code, refused = run_harvest()
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), refused
    assert refused["cause"]["reason"] == "label-playlist-unreadable"
    assert catalogue_fake.playlists_asked_for == [PLAYLIST]
    # The provider's OWN exception type, which tells it from a refusal that asked nothing.
    assert refused["cause"]["detail"]["kind"] == kind
    assert harvested(installed) == []


def test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist(
    installed, monkeypatch
):
    """A failure that is not the provider's must not be reported as the provider's."""
    from cratekit.core.cause import refuse
    from cratekit.label import harvest as label_harvest
    bind(monkeypatch, playlist_of(anjuna()))
    def refusing_tracks(playlist, **kwargs):
        del playlist, kwargs
        raise refuse(
            "review-schema-mismatch", "the review queue was written by another build",
            origin=("tests",),
        )
    monkeypatch.setattr(label_harvest, "playlist_tracks", refusing_tracks)
    code, refused = run_harvest()
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "review-schema-mismatch"


def test_a_provider_that_fails_mid_verification_refuses_rather_than_reporting_a_defect(
    installed, monkeypatch
):
    listing = {PLAYLIST: FakePagedPlaylist([anjuna(), mystery()])}
    bind(monkeypatch, VerificationOutage(playlists=listing, known_labels={CONFIRMED}, answers=1))
    code, refused = run_harvest()
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), refused
    assert refused["cause"]["reason"] == "label-playlist-unreadable"
    assert refused["cause"]["remediation"]["remedy"] != str(Remedy.REPORT_DEFECT)
    steps = refused["cause"]["remediation"]["steps"]
    assert any("retry" in step for step in steps), steps


def test_a_harvest_that_fails_mid_verification_names_what_it_already_offered(
    installed, monkeypatch
):
    """The partial state nothing named, and it is durable rather than rolled back."""
    listing = {PLAYLIST: FakePagedPlaylist([anjuna(), mystery()])}
    bind(monkeypatch, VerificationOutage(playlists=listing, known_labels={CONFIRMED}, answers=1))
    code, refused = run_harvest()
    assert code != int(ExitCode.OK), refused
    assert harvested(installed) == [CONFIRMED]
    assert refused["cause"]["detail"]["offered"] == [CONFIRMED]


def test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason(installed, monkeypatch):
    listing = {PLAYLIST: FakePagedPlaylist([anjuna()])}
    bind(monkeypatch, SessionExpiredAtVerification(playlists=listing))
    code, refused = run_harvest()
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "credential-missing"


def test_the_keys_this_verb_will_drive_are_the_keys_bound_to_its_worker():
    """LABEL_KEYS is two spelled strings, so this is what keeps them true."""
    bound_here = {
        key for key, target in handlers.HANDLERS.items() if target == "cratekit.label.cli:handle"
    }
    assert label_cli.LABEL_KEYS == bound_here


def test_a_label_verb_will_not_drive_a_job_queued_for_another_verb(installed):
    """The resume drives whatever the row names, so the row has to be a label job."""
    with jobs.open_store() as store:
        foreign = jobs.enqueue(
            store, handler_key="export.playlist", payload={"playlist": "x"}, cfg=installed,
            item_ids=("track-1",),
        )
    code, refused = drive(["sync", "labels", "--job", foreign.job_id])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "job-unknown"
    assert "export.playlist" in refused["cause"]["message"]
    assert item_states(foreign.job_id) == {"track-1": str(jobs.ItemState.PENDING)}


def test_an_import_on_an_unconfigured_machine_says_so_rather_than_naming_the_label():
    refused = refused_by(["label", "import", LABELS[0]])
    assert refused["cause"]["reason"] == "config-unusable"
    assert queue_is_empty()


def test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out(installed):
    """The job stays open on purpose, so the way out has to be in the steps."""
    job = itemless(installed)
    _, refused = drive(["sync", "labels", "--job", job.job_id])
    steps = refused["cause"]["remediation"]["steps"]
    assert any(f"crate job cancel {job.job_id}" in step for step in steps), steps
    # A sweep cannot be queued again (U109), so the way back is the guided verb.
    assert steps[-1] == "then take label releases with: crate label sync", steps


def test_the_itemless_refusal_of_an_import_still_says_queue_it_again(installed):
    """The other branch of the same step: an import can still be queued."""
    job = itemless(installed, IMPORT_KEY, name="Kompakt", label_id="kompakt")
    _, refused = drive(["label", "import", "Kompakt", "--job", job.job_id])
    steps = refused["cause"]["remediation"]["steps"]
    assert steps[-1] == "then queue the import again, which records its items", steps


class CountingCatalogue(FakeCatalogue):
    """A catalogue that counts how many times it was asked to verify a release."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verifications = 0

    def search_release(self, claimed: str, release: object) -> dict:
        self.verifications += 1
        return super().search_release(claimed, release)


def counting(*label_ids: str, confirmed=None) -> CountingCatalogue:
    return CountingCatalogue(artists=artists_of(*label_ids), confirmed=confirmed)


def bury(cfg: config.Config, release_id: str) -> None:
    review.DecisionStore(tombstone.STORE_KEY, cfg).record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist="Label Act", title=f"Release {release_id}"),
        actor="tests",
    )


def test_a_mixed_listing_of_tombstoned_and_unconfirmed_releases_is_a_label_with_nothing_new(
    installed, monkeypatch
):
    bury(installed, "hf-1")
    job_id = sweep_job(monkeypatch, counting(SLUGS[0], confirmed=frozenset()), LABELS[0])
    assert swept(job_id)["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_a_sweep_that_read_releases_and_confirmed_none_of_them_still_refuses(
    installed, monkeypatch
):
    """The composite for the test above: the refusal it keeps is the one that was true."""
    job_id = sweep_job(monkeypatch, counting(SLUGS[0], confirmed=frozenset()), LABELS[0])
    drive(["sync", "labels", "--job", job_id])
    assert item_causes(job_id) == {SLUGS[0]: "label-sweep-incomplete"}


def test_a_tombstoned_release_is_never_sent_to_the_provider_for_verification(
    installed, monkeypatch
):
    """The local questions first, the provider call last."""
    bury(installed, "hf-1")
    fake = counting(SLUGS[0])
    swept(sweep_job(monkeypatch, fake, LABELS[0]))
    assert fake.verifications == 1, fake.verifications
    assert offers(installed) == {"hf-2": SLUGS[0]}


def test_one_item_opens_the_review_store_once_however_many_releases_it_offers(
    installed, monkeypatch
):
    """The increment hands the source no store, so the worker has to."""
    job_id = sweep_job(monkeypatch, readable(SLUGS[0]), LABELS[0])
    opened: list[object] = []
    real_open = review.open_store
    def counted_open(cfg):
        opened.append(cfg)
        return real_open(cfg)
    monkeypatch.setattr(review, "open_store", counted_open)
    code, resumed = drive(["sync", "labels", "--job", job_id])
    monkeypatch.setattr(review, "open_store", real_open)
    assert code == int(ExitCode.OK), resumed
    assert len(opened) == 1, len(opened)
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}


class SessionExpiredAtListing(FakeCatalogue):
    """A catalogue whose artist lookup refuses in this product's own vocabulary."""

    def artist_for(self, entry: object) -> object:
        del entry
        raise refuse(
            "credential-missing",
            "the stored provider session expired before the artist was resolved", origin=("tests",),
        )


# ── 12. A release the library already holds is not offered. R-259. ───────────


class Row:
    """A provider track row in the shape ``match.read_tidal_tracks`` reads."""

    def __init__(self, track_id: str, artist: str, name: str) -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = ""


#: The tracks of the first label's two releases, as a read by identifier lists them.
TRACKS = {
    "hf-1": ([Row("11", "Aurora Bloom", "Sun Path"), Row("12", "Nova Reef", "Tide")], 2026),
    "hf-2": ([Row("21", "Mira Vale", "Glass Hour")], 2025),
}


#: Every track of ``TRACKS`` as the library names its file.
EVERY_TRACK = (
    "Aurora Bloom - Sun Path.flac", "Nova Reef - Tide.flac", "Mira Vale - Glass Hour.flac",
)


def hold(cfg: config.Config, *names: str) -> None:
    """Put files in the library's music folder, named the way the library names them."""
    for name in names:
        (cfg.library.root / cfg.library.music_dir / name).write_bytes(b"")


def tracked(*, releases=None, confirmed=None, cls=FakeCatalogue) -> FakeCatalogue:
    """The first label's catalogue, able to read its releases' tracks."""
    releases = TRACKS if releases is None else releases
    return cls(artists=artists_of(SLUGS[0]), releases=releases, confirmed=confirmed)


def test_a_label_whose_catalogue_the_library_already_holds_offers_nothing(installed, monkeypatch):
    hold(installed, *EVERY_TRACK)
    job_id = sweep_job(monkeypatch, tracked(), LABELS[0])
    assert swept(job_id)["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_a_release_with_one_track_still_missing_is_offered_beside_one_that_is_held(
    installed, monkeypatch
):
    """Every track, not any track. The composite for the test above."""
    hold(installed, "Aurora Bloom - Sun Path.flac", "Mira Vale - Glass Hour.flac")
    swept(sweep_job(monkeypatch, tracked(), LABELS[0]))
    assert offers(installed) == {"hf-1": SLUGS[0]}


def test_a_release_listing_no_tracks_and_a_release_that_is_gone_are_both_offered(
    installed, monkeypatch
):
    """Two absences that must not read as ownership."""
    hold(installed, "Mira Vale - Glass Hour.flac")
    fake = tracked(releases={"hf-1": ([], 2026)})
    swept(sweep_job(monkeypatch, fake, LABELS[0]))
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}
    assert sorted(fake.releases_asked_for) == ["hf-1", "hf-2"]


def test_a_release_the_library_holds_only_in_another_version_is_offered(installed, monkeypatch):
    """A different cut is a question for the person, never ownership."""
    hold(installed, *EVERY_TRACK[:2], "Mira Vale - Glass Hour (Extended Mix).flac")
    swept(sweep_job(monkeypatch, tracked(), LABELS[0]))
    assert offers(installed) == {"hf-2": SLUGS[0]}


def test_an_unconfirmed_release_is_never_read_and_a_confirmed_one_is_read_once(
    installed, monkeypatch
):
    """Ownership is a provider read now, so it is asked after verification."""
    fake = tracked(confirmed={"hf-1"})
    swept(sweep_job(monkeypatch, fake, LABELS[0]))
    assert fake.releases_asked_for == ["hf-1"]
    assert offers(installed) == {"hf-1": SLUGS[0]}


class TracksOutage(FakeCatalogue):
    """A catalogue that lists and confirms, and cannot read a release's tracks."""

    def release_tracks(self, release_id: str):
        self.releases_asked_for.append(release_id)
        raise RuntimeError("the provider answered 503 after the retry ladder")


class TracksSessionExpired(FakeCatalogue):
    """A catalogue whose track read refuses in this product's own vocabulary."""

    def release_tracks(self, release_id: str):
        del release_id
        raise refuse(
            "credential-missing", "the stored provider session expired before the release was read",
            origin=("tests",),
        )


def test_a_track_read_the_provider_could_not_answer_offers_the_release(installed, monkeypatch):
    """Not owned, offered, and the rest of the label is still swept."""
    hold(installed, *EVERY_TRACK)
    fake = tracked(cls=TracksOutage)
    job_id = sweep_job(monkeypatch, fake, LABELS[0])
    assert swept(job_id)["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}
    assert sorted(fake.releases_asked_for) == ["hf-1", "hf-2"]


def test_three_failed_track_reads_in_a_row_stop_the_asking(installed, monkeypatch):
    """A provider that is down costs three retry ladders, not one per release."""
    fake = TracksOutage(artists={SLUGS[0]: FakePagedArtist(releases(5))})
    swept(sweep_job(monkeypatch, fake, LABELS[0]))
    assert len(fake.releases_asked_for) == 3, fake.releases_asked_for
    assert sorted(offers(installed)) == [f"hf-{n}" for n in range(1, 6)]


def releases(count: int) -> list[FakeRelease]:
    """The first label's releases ``hf-1`` to ``hf-<count>``."""
    return [FakeRelease(f"hf-{n}") for n in range(1, count + 1)]


def gone(release_id: str):
    raise ReleaseUnresolvable(f"no catalogue release {release_id!r}")


def read(release_id: str):
    return (Row(release_id, "Lumen Drift", release_id),), 2026, None


@pytest.mark.parametrize("answer", [
    # Gone is the provider answering, so it resets the count as a read does.
    pytest.param(gone, id="gone"),
    # An answer resets the count, so failures that are not in a row never stop it.
    pytest.param(read, id="read-succeeds"),
])
def test_an_answer_breaks_the_run_of_failed_reads(installed, monkeypatch, answer):
    class Answering(FakeCatalogue):
        def release_tracks(self, release_id: str):
            self.releases_asked_for.append(release_id)
            if release_id in {"hf-3", "hf-6"}:
                return answer(release_id)
            raise RuntimeError("the provider answered 503 after the retry ladder")
    fake = Answering(artists={SLUGS[0]: FakePagedArtist(releases(7))})
    swept(sweep_job(monkeypatch, fake, LABELS[0]))
    assert len(fake.releases_asked_for) == 7, fake.releases_asked_for


def test_a_sweep_of_two_labels_walks_the_library_once(installed, monkeypatch):
    """One view per job. A view per item walked the whole music volume per label."""
    from cratekit.acquire import match_cli
    walks: list[object] = []
    real_view = match_cli.library_view
    def counted_view(cfg):
        walks.append(cfg)
        return real_view(cfg)
    monkeypatch.setattr(match_cli, "library_view", counted_view)
    tracks = {**TRACKS, "ot-1": ([Row("31", "Lumen Drift", "Salt Road")], 2024)}
    swept(sweep_job(monkeypatch, readable(*SLUGS[:2], releases=tracks), *LABELS[:2]))
    assert len(walks) == 1, len(walks)
    assert set(offers(installed)) == {"hf-1", "hf-2", "ot-1"}


@pytest.mark.parametrize("fake", [
    # An expired session is not "this source could not list".
    pytest.param(
        lambda: SessionExpiredAtVerification(artists=artists_of(SLUGS[0])), id="sweep-verifier",
    ),
    pytest.param(SessionExpiredAtListing, id="artist-lookup"),
    pytest.param(lambda: tracked(cls=TracksSessionExpired), id="track-read"),
])
def test_a_refusal_raised_in_kind_keeps_its_own_reason(installed, monkeypatch, fake):
    job_id = sweep_job(monkeypatch, fake(), LABELS[0])
    unswept(job_id)
    assert item_causes(job_id) == {SLUGS[0]: "credential-missing"}


def test_a_release_with_a_row_the_reader_cannot_read_is_offered(installed, monkeypatch):
    """A row naming no artist is a track nobody can look for, so it is not held."""
    hold(installed, *EVERY_TRACK)
    unreadable = {
        **TRACKS, "hf-2": ([Row("21", "Mira Vale", "Glass Hour"), Row("22", "", "Untitled")], 2025),
    }
    swept(sweep_job(monkeypatch, tracked(releases=unreadable), LABELS[0]))
    assert offers(installed) == {"hf-2": SLUGS[0]}


# ── 13. A rate limit is retryable, and resuming retries exactly those labels. R-704. ───


class Limit:
    """Whether the provider is answering rate limited, shared by every fake below."""

    def __init__(self) -> None:
        self.on = True
        self.answered = 0


class RateLimitedArtist(FakePagedArtist):
    """A label listing the provider refuses with its own ``TooManyRequests``."""

    def __init__(self, releases: list[FakeRelease], limit: Limit) -> None:
        super().__init__(releases)
        self.limit = limit

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[FakeRelease]:
        if self.limit.on:
            self.limit.answered += 1
            raise TooManyRequests("Album unavailable")
        return super().get_albums(limit=limit, offset=offset)


class RateLimitedVerification(FakeCatalogue):
    """Every verification call answers rate limited while the limit is on."""

    def __init__(self, *args, limit: Limit, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.limit = limit

    def search_release(self, claimed: str, release) -> dict:
        if self.limit.on:
            self.limit.answered += 1
            raise TooManyRequests("Album unavailable")
        return super().search_release(claimed, release)


def _ladder_without_waiting(monkeypatch) -> list[float]:
    """The crawl's real retry ladder, every rung climbed, none of it slept."""
    from cratekit.label import crawl
    real = crawl.releases
    waits: list[float] = []
    def patient(artist, **kwargs):
        kwargs.setdefault("sleep", waits.append)
        return real(artist, **kwargs)
    monkeypatch.setattr(crawl, "releases", patient)
    return waits


def _one_label_rate_limited(monkeypatch) -> tuple[FakeCatalogue, Limit]:
    """Two labels: the first lists, the second's listing answers rate limited."""
    limit = Limit()
    limited = RateLimitedArtist([FakeRelease(one) for one in RELEASES[SLUGS[1]]], limit)
    fake = FakeCatalogue(artists={**artists_of(SLUGS[0]), SLUGS[1]: limited})
    return bind(monkeypatch, fake), limit


def item_cause(job_id: str, item_id: str):
    with jobs.open_store() as store:
        for item in jobs.items(store, job_id):
            if item.item_id == item_id:
                return item.cause
    raise AssertionError(f"job {job_id} has no item {item_id}")


def test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume(
    installed, monkeypatch
):
    register(*LABELS[:2])
    waits = _ladder_without_waiting(monkeypatch)
    _, limit = _one_label_rate_limited(monkeypatch)
    job_id = queued_sweep()
    failed = unswept(job_id)
    assert limit.answered == 6 and len(waits) == 5, (limit.answered, waits)
    assert item_states(job_id) == {
        SLUGS[0]: str(jobs.ItemState.DONE), SLUGS[1]: str(jobs.ItemState.FAILED),
    }
    cause = item_cause(job_id, SLUGS[1])
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is True
    assert cause.remediation.remedy is Remedy.RESUME_JOB
    assert cause.detail["rate_limited"] is True
    assert "rate limited" in cause.message
    assert "TooManyRequests: Album unavailable" in cause.message
    job = failed["cause"]
    assert job["reason"] == "unavailable-transient"
    assert job["retryable"] is True
    assert job["remediation"]["remedy"] == "resume-job"
    assert job["detail"]["retryable_failed"] == 1
    assert job["detail"]["permanent_failed"] == 0
    assert "every failure is permanent" not in job["message"]


def test_a_resumed_job_rearms_the_rate_limited_label_and_not_the_settled_one(
    installed, monkeypatch
):
    """R-704's Closes when: ``crate job resume`` re-arms exactly those items."""
    register(*LABELS[:2])
    _ladder_without_waiting(monkeypatch)
    fake, limit = _one_label_rate_limited(monkeypatch)
    job_id = queued_sweep()
    assert drive(["sync", "labels", "--job", job_id])[0] != int(ExitCode.OK)
    assert fake.asked_for == [SLUGS[0], SLUGS[1]]
    spawned: list[list[str]] = []
    def recorded(store, job, argv, **kwargs):
        del store, job, kwargs
        spawned.append(list(argv))
        return 4242
    monkeypatch.setattr(jobs, "spawn", recorded)
    code, resumed = drive(["job", "resume", job_id])
    assert code == int(ExitCode.OK), resumed
    assert item_states(job_id) == {
        SLUGS[0]: str(jobs.ItemState.DONE), SLUGS[1]: str(jobs.ItemState.PENDING),
    }
    assert len(spawned) == 1 and spawned[0][:4] == ["sync", "labels", "--job", job_id]
    limit.on = False
    code, finished = drive(spawned[0])
    assert code == int(ExitCode.OK), finished
    assert finished["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert item_states(job_id) == {slug: str(jobs.ItemState.DONE) for slug in SLUGS[:2]}
    assert fake.asked_for == [SLUGS[0], SLUGS[1], SLUGS[1]]
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0], "ot-1": SLUGS[1]}


def test_a_rate_limited_verification_is_retryable_too(installed, monkeypatch):
    """The sitting's error was an album read, and verification is one with no ladder."""
    limit = Limit()
    fake = RateLimitedVerification(artists=artists_of(SLUGS[0]), limit=limit)
    job_id = sweep_job(monkeypatch, fake, LABELS[0])
    failed = unswept(job_id)
    assert limit.answered == 1
    cause = item_cause(job_id, SLUGS[0])
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is True
    assert failed["cause"]["retryable"] is True
    assert failed["cause"]["inner"]["retryable"] is True


def test_a_listing_failure_that_is_not_a_rate_limit_stays_permanent(installed, monkeypatch):
    """The split is a rate limit against everything else, not a blanket retry."""
    job_id = sweep_job(monkeypatch, UnreadableCatalogue(), LABELS[0])
    drive(["sync", "labels", "--job", job_id])
    cause = item_cause(job_id, SLUGS[0])
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is False
    assert "rate_limited" not in cause.detail
    assert "rate limited" not in cause.message


class RateLimitedResolve(FakeCatalogue):
    """The artist resolve answers rate limited, before any listing is asked."""

    def artist_for(self, entry):
        self.asked_for.append(str(getattr(entry, "label_id", entry)))
        raise TooManyRequests("Artist unavailable")


class RateLimitedProbe:
    """An artist whose listing attribute is a lazy read the provider refuses."""

    @property
    def get_albums(self):
        raise TooManyRequests("Artist unavailable")


@pytest.mark.parametrize(
    "fake",
    [
        pytest.param(lambda: RateLimitedResolve(), id="artist-resolve"),
        pytest.param(
            lambda: FakeCatalogue(artists={SLUGS[0]: RateLimitedProbe()}), id="listing-probe"
        ),
    ],
)
def test_a_rate_limit_at_every_other_sweep_boundary_is_retryable(installed, monkeypatch, fake):
    """R-704. The sweep has four provider boundaries and each asks the question."""
    job_id = sweep_job(monkeypatch, fake(), LABELS[0])
    unswept(job_id)
    cause = item_cause(job_id, SLUGS[0])
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is True
    assert "TooManyRequests: Artist unavailable" in cause.message


# ── R-515: a harvest over a playlist the provider lists short ────────────────


def test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns(installed, monkeypatch):
    listing = {PLAYLIST: FakePagedPlaylist([anjuna()], declared=3)}
    bind(monkeypatch, FakeCatalogue(playlists=listing, known_labels={CONFIRMED}))
    envelope = harvest_ok()
    assert harvested(installed) == [CONFIRMED]
    assert set(envelope["data"]) == {"queue", "items", "unresolved"}
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "label-harvest-playlist-withheld"]
    assert "3 declared, 1 listed, 2 withheld by the provider" in warning["message"]


def test_a_harvest_over_a_full_playlist_warns_nothing(installed, monkeypatch):
    listing = {PLAYLIST: FakePagedPlaylist([anjuna()], declared=1)}
    bind(monkeypatch, FakeCatalogue(playlists=listing, known_labels={CONFIRMED}))
    envelope = harvest_ok()
    assert envelope.get("warnings", []) == []


# ── R-2071: the ownership container driven alone ─────────────────────────────


def unwalkable_library() -> sweep.LibraryView:
    """A library that cannot be walked, so a walk shows as a failure."""
    raise RuntimeError("the library could not be walked")


def test_a_release_listing_no_tracks_is_not_owned_and_walks_no_library(installed):
    """Nothing to resolve, so the library is never walked and the release is offered."""
    owned = sweep.OwnedReleases(
        installed, tracked(releases={"hf-1": ([], 2026)}), library=unwalkable_library
    )
    assert "hf-1" not in owned


def test_an_ownership_answer_is_kept_after_the_shared_reader_forgets_its_reads(installed):
    """The sweep and the increment both ask, and a release is read from the provider once."""
    fake = tracked(releases={"hf-1": ([], 2026)})
    reader = catalogue.ReleaseTracks(fake)
    owned = sweep.OwnedReleases(installed, reader, library=unwalkable_library)
    assert "hf-1" not in owned
    reader.forget()
    assert "hf-1" not in owned
    assert fake.releases_asked_for == ["hf-1"]
