"""U4, U5 and U6: the label verbs queue real items, run them, and harvest.

Harvest is the third verb on the same seam and it queues nothing at all, which
is why it arrives in this file rather than in a queueing suite of its own: it
runs in process and its whole behaviour depends on the catalogue substitution
the two queued verbs already needed. Section 9 holds it.

WHAT THIS FILE GUARDS THAT NO OTHER SUITE CAN. ``cratekit.core.jobs.drive``
transitions a job whose item count is zero straight to SUCCEEDED, because
nothing was attempted and nothing failed. Both label verbs called ``enqueue``
with no ``item_ids`` at all, so a person who queued a sweep and later resumed it
was told it succeeded over a registry nothing was read from.
``tests/modules/test_labels.py`` proves the sweep engine keeps its promises when
called directly and has always passed, because nothing in ``src`` queued an item
for it to claim. This file is about the enqueue and the binding: that the
registry decides the items, that an empty registry refuses instead of queueing,
that a person is told the catalogue seam is unbound at the one moment the
information is still useful to them, and that a queued job now actually runs.

THE ITEMS ARE READ BACK FROM THE STORE rather than inferred from the envelope.
The envelope is exactly ``job_state/1``, four keys and no item list, so the only
thing that can see an item row is the queue itself. A refusal is likewise proven
by the ABSENCE of a job row rather than by the exception alone: a verb that
queued first and refused afterwards would raise the same cause and leave the
empty job sitting in the queue for a later resume to succeed at.

THE CATALOGUE IS ALWAYS A STAND IN, and it is the ONLY thing substituted. No
adapter ships in this build, so every drive below puts a fake in front of
``cratekit.label.catalogue.resolve`` on the module attribute, which is the
substitution that module's docstring contracts for. The real dispatcher, the
real queue, the real handler resolution, the real driver and the real sweep
engine are all in the path, because the property under test is the binding
rather than the fake.
"""

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

#: Three display names whose slugs are distinct and are not the names, so an
#: item carrying a display name fails here rather than passing by coincidence
#: (seam R19, and D5's rule that a persisted record is never keyed on a name).
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


def register(*names: str) -> None:
    """Put labels in the registry through the real verb, not through the store.

    The registry is what decides the items, so a fixture that wrote the file
    itself would be a second writer of the document under test and could put a
    shape in it that ``crate label registry add`` cannot produce.
    """
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


#: One catalogue's worth of releases per label, with identifiers that carry the
#: label they belong to. That is what makes the per item assertions below able to
#: fail: a worker that swept the same label twice would produce one label's
#: identifiers where two are expected, rather than the same count of anonymous
#: rows.
RELEASES = {
    "hotflush-recordings": ("hf-1", "hf-2"),
    "ostgut-ton": ("ot-1",),
    "kompakt": ("ko-1",),
}


def readable(*label_ids: str) -> FakeCatalogue:
    """A catalogue that can list exactly these labels, keyed as the seam keys it."""
    return FakeCatalogue(
        artists={
            label_id: FakePagedArtist(
                [FakeRelease(release_id) for release_id in RELEASES[label_id]]
            )
            for label_id in label_ids
        }
    )


def bind(monkeypatch, fake: FakeCatalogue) -> FakeCatalogue:
    """Put ``fake`` in front of the provider seam for this test.

    On the MODULE ATTRIBUTE rather than on an imported name, because that is what
    ``cratekit.label.catalogue``'s docstring contracts for and what the worker
    looks up at call time. A worker that bound ``resolve`` into its own scope at
    import time would not see this and would meet the real unbound seam.
    """
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def queued_job(verb: list[str]) -> str:
    """Queue through the real verb and return the job identifier."""
    code, envelope = drive(verb)
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"]


def queued_sweep(run_id: str | None = None) -> str:
    """File a labels sweep the way a build before U109 did, and return its id.

    NOTHING IN ``src`` QUEUES ONE ANY MORE. ``crate sync labels`` refuses to and
    ``crate sync all`` no longer composes the labels source, so the only sweep
    job that can exist is one a person queued before upgrading. This is that
    job: the payload and the items exactly as the retired ``queue_sweep`` wrote
    them, one item per registered label keyed by identifier (KTD1, R19), under
    the sweep's own handler key. Every test that drives a sweep through
    ``sync labels --job`` is therefore a test that such a job still resumes.
    """
    cfg = config.load()
    held = label_registry.RegistryStore().load()
    items = tuple(entry.label_id for entry in held.labels.values())
    assert items, "register a label before filing a sweep, as the old verb refused"
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=SWEEP_KEY,
            payload={"source_id": "labels", "run_id": run_id or output.new_run_id()},
            item_ids=items,
            cfg=cfg,
        )
    return job.job_id


def item_states(job_id: str) -> dict[str, str]:
    with jobs.open_store() as store:
        return {item.item_id: str(item.state) for item in jobs.items(store, job_id)}


def item_causes(job_id: str) -> dict[str, str | None]:
    """Each item's OWN cause, which is not the same thing as the job's.

    ``jobs.drive`` records the failing item's cause on the item row and then, when
    every attempted item failed, raises ``no-evidence`` with that cause nested as
    ``inner``. So the envelope a person sees names the evidence rule and the row
    names what actually went wrong, and a test asserting the worker's refusal has
    to read the row.
    """
    with jobs.open_store() as store:
        return {
            item.item_id: (item.cause.reason if item.cause is not None else None)
            for item in jobs.items(store, job_id)
        }


def item_cause_message(job_id: str, item_id: str) -> str:
    """One item's cause SENTENCE, which is the half a slug cannot carry.

    A refusal that names a population has to say the size of it, and the reason
    slug is the same string whether it says four or nothing at all. Read off the
    row for the same reason :func:`item_causes` is: the envelope a person sees
    names the evidence rule and only the row names what the worker refused.
    """
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
    """The label-release queue under ``cfg``, as release identity to label id.

    Keyed on the identity rather than counted, because a count cannot tell one
    label swept twice from two labels swept once, and that is exactly the defect
    the per item worker exists to avoid.
    """
    with review.open_store(cfg) as store:
        page = review.list_items(store, queue=str(review.Queue.LABEL_RELEASE))
    return {
        str(item.payload.get("identity")): str(item.payload.get("label_id"))
        for item in page.items
    }


# ═══════════════════════════════════════════════════════════════════════════
# 1. The sweep's queueing half is retired (U109)
# ═══════════════════════════════════════════════════════════════════════════


def test_sync_labels_refuses_to_queue_and_names_the_guided_verb(installed):
    """Labels registered, so the old verb would have queued, and it queues nothing.

    Proven by the absence of a job row as well as by the cause, because a verb
    that queued first and refused afterwards would raise the same cause and
    leave a sweep in the queue for the next resume to run.
    """
    del installed
    register(*LABELS)
    code, refused = drive(["sync", "labels"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "verb-retired"
    assert "crate label sync" in refused["cause"]["message"]
    steps = refused["cause"]["remediation"]["steps"]
    assert any(step.endswith(": crate label sync") for step in steps), steps
    assert any("--job" in step for step in steps), steps
    assert queue_is_empty()


def test_the_retired_refusal_reads_nothing_so_a_fresh_install_gets_it_too():
    """No ``installed`` fixture: a machine that was never set up.

    The refusal is about the verb, not about this installation, so it must not
    be outranked by ``config-unusable`` or ``label-registry-empty``. Either
    would send a person to fix something that would not make the verb queue.
    """
    code, refused = drive(["sync", "labels"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "verb-retired"
    assert queue_is_empty()


def test_a_sweep_queued_before_u109_still_resumes_to_done(installed, monkeypatch):
    """The other half of retiring by reduction: an old job is never dropped."""
    del installed
    register(*LABELS[:2])
    bind(monkeypatch, readable(*SLUGS[:2]))
    job_id = queued_sweep()
    assert queued_items(job_id) == list(SLUGS[:2])
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job_id).values()) == {str(jobs.ItemState.DONE)}
    assert set(offers(config.load()).values()) == set(SLUGS[:2])


# ═══════════════════════════════════════════════════════════════════════════
# 2. The import's one item
# ═══════════════════════════════════════════════════════════════════════════


def test_an_import_queues_exactly_one_item_and_it_is_the_label_id(installed):
    """Driven by DISPLAY NAME and asserted on the identifier, which is the point.

    ``import_label`` resolves the entry before it queues, so the name a person
    typed never reaches the item even when the two look interchangeable here.
    """
    del installed
    register(*LABELS)
    code, queued = drive(["label", "import", "Ostgut Ton"])
    assert code == int(ExitCode.OK), queued
    assert queued_items(queued["data"]["job_id"]) == ["ostgut-ton"]


def test_an_import_of_an_unregistered_name_refuses_and_queues_nothing(installed):
    """R6: the import cannot queue an empty job because it refuses first.

    There is no zero item guard on this path and there should not be one. This is
    the test that says why: the refusal that makes one unnecessary is this one,
    so a build that lost it would fail here rather than growing a redundant guard
    to compensate.
    """
    del installed
    register(*LABELS)
    code, refused = drive(["label", "import", "no-such-label"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "label-unknown"
    assert queue_is_empty()


def test_an_import_against_an_empty_registry_refuses_the_unknown_name(installed):
    """The two refusals stay distinguishable when both conditions hold at once.

    An empty registry means every name is unresolvable, and the import's answer is
    still about the NAME rather than about the registry, because the command that
    fixes it is the one that adds that label.
    """
    del installed
    code, refused = drive(["label", "import", "Kompakt"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "label-unknown"
    assert queue_is_empty()


# ═══════════════════════════════════════════════════════════════════════════
# 3. The unbound catalogue is a warning, not a refusal
# ═══════════════════════════════════════════════════════════════════════════


def test_the_import_queues_without_a_warning_now_an_adapter_is_bound(installed):
    """U62 flipped the warning, and the job still queues.

    Before a catalogue adapter shipped, both paths warned that the job would fail
    at the provider seam. A warning that stays after the adapter lands tells a
    person their sweep will fail when it will not.
    """
    del installed
    assert catalogue.bound() is True
    register(*LABELS)
    code, queued = drive(["label", "import", "Kompakt"])
    assert code == int(ExitCode.OK), queued
    codes = {warning["code"] for warning in queued.get("warnings") or ()}
    assert "label-catalogue-unbound" not in codes
    assert queued_items(queued["data"]["job_id"])


def test_the_unbound_warning_says_the_job_will_fail_at_the_provider_seam(
    installed, monkeypatch
):
    """A code alone is a slug; the sentence is what a person reads.

    Driven on a build whose adapter does not import, which is the only build the
    warning still describes, and the job is queued anyway.
    """
    del installed
    monkeypatch.setattr(catalogue, "bound", lambda: False)
    register(*LABELS)
    code, queued = drive(["label", "import", "Kompakt"])
    assert code == int(ExitCode.OK), queued
    said = [
        warning["message"]
        for warning in queued.get("warnings") or ()
        if warning["code"] == "label-catalogue-unbound"
    ]
    assert said and "provider seam" in said[0], queued.get("warnings")
    assert queued_items(queued["data"]["job_id"])


def test_a_refused_sweep_carries_no_warning_because_nothing_was_queued(installed, monkeypatch):
    """The warning belongs to a queued job, so a refusal must not carry one.

    A refusal telling a person their job will fail at the provider seam would be
    naming a job that does not exist. Driven with the catalogue unbound, which
    is the one state that would put the warning on a queued job.
    """
    del installed
    monkeypatch.setattr(catalogue, "bound", lambda: False)
    register(*LABELS)
    code, refused = drive(["sync", "labels"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert not (refused.get("warnings") or ())


def test_the_warning_rides_the_envelope_rather_than_the_job_state_payload(installed, monkeypatch):
    """KTD7: the payload stays exactly the four ``job_state/1`` keys.

    ``cli.output`` closes that surface with ``additionalProperties: false`` and
    ``tests.cli_drive.drive`` validates every envelope it emits, so an undeclared
    key would already fail. This says the positive half as well: the warning is a
    sibling of ``data`` and not a field inside it.
    """
    del installed
    monkeypatch.setattr(catalogue, "bound", lambda: False)
    register(*LABELS)
    code, queued = drive(["label", "import", "Kompakt"])
    assert code == int(ExitCode.OK), queued
    assert set(queued["data"]) == {"job_id", "state", "cause", "progress"}
    assert queued.get("warnings")


# ═══════════════════════════════════════════════════════════════════════════
# 4. The bindings themselves
# ═══════════════════════════════════════════════════════════════════════════


def test_both_label_keys_report_a_bound_worker_rather_than_a_reason_they_have_none():
    """``crate job show``'s worker field, at the source it is derived from.

    Asked through ``handlers`` rather than through a verb, because the answer is
    given WITHOUT importing the feature module (KTD26) and driving a verb would
    import it and prove nothing about that property.
    """
    for key in (SWEEP_KEY, IMPORT_KEY):
        assert handlers.is_known(key), key
        assert handlers.unbound_reason(key) is None, key
        assert callable(handlers.resolve(key)), key


def test_neither_label_key_is_recorded_as_unbound_now_that_both_are_bound():
    """Deleting the exemption is the other half of adding the binding.

    A key in both tables would make ``unbound_reason`` answer with a sentence
    about a worker that exists, which is the reporting surface telling a person
    their job will not run while it does.
    """
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
    """The sweep and the import differ in how many items they queue, not in work.

    Asserted as identity rather than as two declarations that look alike, because
    two functions doing the same thing is how the item-not-payload rule gets fixed
    in one of them.
    """
    assert handlers.resolve(SWEEP_KEY) is handlers.resolve(IMPORT_KEY)
    assert handlers.resolve(SWEEP_KEY) is label_cli.handle


# ═══════════════════════════════════════════════════════════════════════════
# 5. A queued sweep runs
# ═══════════════════════════════════════════════════════════════════════════


def test_a_sweep_runs_every_one_of_its_labels_from_pending_to_done(
    installed, monkeypatch
):
    """The whole point of the unit, read back from the queue rather than the exit code."""
    del installed
    register(*LABELS[:2])
    bind(monkeypatch, readable(*SLUGS[:2]))
    job_id = queued_sweep()
    assert set(item_states(job_id).values()) == {str(jobs.ItemState.PENDING)}

    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert item_states(job_id) == {slug: str(jobs.ItemState.DONE) for slug in SLUGS[:2]}
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)


def test_each_item_sweeps_its_own_label_and_not_one_named_by_the_payload(
    installed, monkeypatch
):
    """The first defect U46's end to end drive surfaced, pinned on the label path.

    A handler that took its subject from the payload would make every item of a
    multi item job do the SAME work, so the assertion is on which releases were
    offered rather than on how many. Two labels with different catalogues produce
    two disjoint sets of identifiers, and a worker reading the payload cannot
    produce both of them however many items it runs.
    """
    register(*LABELS[:2])
    catalogue_fake = bind(monkeypatch, readable(*SLUGS[:2]))
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed

    assert offers(installed) == {
        "hf-1": "hotflush-recordings",
        "hf-2": "hotflush-recordings",
        "ot-1": "ostgut-ton",
    }
    assert catalogue_fake.asked_for == list(SLUGS[:2])


def test_an_import_runs_its_one_item_to_done_through_the_same_worker(
    installed, monkeypatch
):
    """The second key, driven through the real dispatcher rather than by calling handle."""
    del installed
    register(LABELS[2])
    bind(monkeypatch, readable(SLUGS[2]))
    job_id = queued_job(["label", "import", "Kompakt"])
    code, resumed = drive(["label", "import", "Kompakt", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert item_states(job_id) == {SLUGS[2]: str(jobs.ItemState.DONE)}
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)


def test_the_resume_envelope_is_exactly_job_state_and_nothing_beside_it(
    installed, monkeypatch
):
    """KTD7: no artifact, no per verb detail, four keys.

    ``tests.cli_drive.drive`` already validates every envelope against the
    declared schema, and U51 shipped an undeclared key on this exact surface, so
    the positive half is asserted here too.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, readable(SLUGS[0]))
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert set(resumed["data"]) == {"job_id", "state", "cause", "progress"}


# ═══════════════════════════════════════════════════════════════════════════
# 6. What a failing round does
# ═══════════════════════════════════════════════════════════════════════════


def test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job(
    installed, monkeypatch
):
    """R-135 through the binding: an unreadable listing is not a quiet label.

    THE CAUSE IS READ OFF THE ITEM ROW. When every attempted item fails
    ``jobs.drive`` records the item's cause on the row and then raises
    ``no-evidence`` with it nested as ``inner``, so the envelope names the
    evidence rule and only the row names the lookup failure. Both are asserted,
    because a build that reported the sweep as SUCCEEDED with an empty result is
    the state this closes.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, UnreadableCatalogue())
    job_id = queued_sweep()
    code, failed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), failed
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
    """R-380 through the dispatcher: the sitting's mixed job, one item each way.

    One label lists, one does not, because the provider has no artist named for
    it. The job used to report unavailable-transient and resume-job over that.
    """
    del installed
    register(*LABELS[:2])
    bind(monkeypatch, readable(SLUGS[0]))
    job_id = queued_sweep()
    code, failed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {
        SLUGS[0]: None,
        SLUGS[1]: "sync-source-lookups-failed",
    }
    assert job_state(job_id) == str(jobs.JobState.FAILED)
    cause = failed["cause"]
    assert cause["reason"] == "sync-source-lookups-failed"
    assert cause["retryable"] is False
    assert cause["remediation"]["remedy"] != "resume-job"
    assert "finished 1 items and failed 1" in cause["message"]
    assert cause["inner"] is not None
    assert cause["inner"]["reason"] == "sync-source-lookups-failed"


def test_an_increment_that_could_not_offer_every_release_fails_the_item(
    installed, monkeypatch
):
    """A partial round FAILS rather than completing, which is a decision.

    ``run.increment`` reports per candidate errors in a result it still returns,
    so a worker that only looked at ``processed`` would mark the item done having
    offered some of the label. The person's remedy is another attempt at the same
    job, which is why the refusal carries ``resume-job`` rather than the exit
    code's own default.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, readable(SLUGS[0]))

    def refusing_offer(store, candidate, **kwargs):
        del store, kwargs
        raise RuntimeError(f"the review queue rejected {candidate.identity}")

    monkeypatch.setattr(sweep, "offer_release", refusing_offer)
    job_id = queued_sweep()
    code, failed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {SLUGS[0]: "label-sweep-incomplete"}
    assert job_state(job_id) == str(jobs.JobState.FAILED)


def test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing(
    installed, monkeypatch
):
    """The registry can move between enqueue and drive, and the items cannot.

    The queue froze an identifier; the registry is a live document a person edits
    with another verb. A worker that resolved nothing and swept an empty registry
    would report the job done having read no label at all.
    """
    del installed
    register(*LABELS[:2])
    bind(monkeypatch, readable(*SLUGS[:2]))
    job_id = queued_sweep()
    code, removed = drive(["label", "registry", "remove", LABELS[0]])
    assert code == int(ExitCode.OK), removed

    code, failed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    causes = item_causes(job_id)
    assert causes[SLUGS[0]] == "label-unknown"
    assert causes[SLUGS[1]] is None
    assert item_states(job_id)[SLUGS[1]] == str(jobs.ItemState.DONE)


# ═══════════════════════════════════════════════════════════════════════════
# 6b. A catalogue that confirms nothing is not a label with nothing new
#
# THE THREE ARMS BELONG TOGETHER AND ARE WRITTEN TOGETHER. A catalogue whose
# verification endpoint is degraded, rate limited, or answering under a
# distributor's name confirms nothing, so every release it listed is dropped,
# the increment sees no processed items and no errors, and it reports
# ``shortfall="empty"``. That is the same envelope a label with genuinely
# nothing new produces, which is R-135's shape on the one path U52 made
# reachable.
#
# THE REFUSAL IS KEYED ON THE DROPPED POPULATION rather than on an empty
# candidate list, and the second and third tests are what hold that key in
# place. An all tombstoned label and a label whose crawl is exhausted both
# produce no candidates and both are genuine no ops, so a build that refused on
# "nothing was offered" would turn every quiet label into an error and would
# trade R-135 for its mirror image.
# ═══════════════════════════════════════════════════════════════════════════


def unconfirming(*label_ids: str) -> FakeCatalogue:
    """A catalogue that lists these labels and confirms none of what it lists.

    ``confirmed`` is the parameter ``label_fakes`` has documented since U52 as
    "how a suite drives the unconfirmed-and-dropped path", and an empty set is
    the whole of that path: every release is read off the provider and every one
    is answered ``unconfirmed``.
    """
    return FakeCatalogue(
        artists={
            label_id: FakePagedArtist(
                [FakeRelease(release_id) for release_id in RELEASES[label_id]]
            )
            for label_id in label_ids
        },
        confirmed=frozenset(),
    )


def test_a_sweep_that_confirmed_none_of_what_it_read_fails_rather_than_succeeding(
    installed, monkeypatch
):
    """The dishonest success this closes, driven end to end through the binding.

    Every assertion here failed the same way before the fix and it is worth
    naming which way: the job reported SUCCEEDED with one item done, no cause and
    no warning, over forty releases the product read and threw away. That is
    indistinguishable from a label with nothing new, which is the one reading
    ``sweep.py``'s own module docstring forbids.
    """
    register(LABELS[0])
    bind(monkeypatch, unconfirming(SLUGS[0]))
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {SLUGS[0]: "label-sweep-incomplete"}
    assert job_state(job_id) != str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_the_unconfirmed_refusal_says_how_many_were_read_and_that_the_provider_answered(
    installed, monkeypatch
):
    """Two different problems, two different remedies, so the sentence separates them.

    A sweep that could not REACH the provider and a sweep that reached it and
    confirmed nothing are repaired by different acts: the first waits for the
    network and the second is a verification endpoint answering wrongly, most
    often because a release is credited to a distributor rather than to the
    imprint. A message that only said the sweep was incomplete would send a
    person to check their connection.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, unconfirming(SLUGS[0]))
    job_id = queued_sweep()

    drive(["sync", "labels", "--job", job_id])

    said = item_cause_message(job_id, SLUGS[0])
    assert str(len(RELEASES[SLUGS[0]])) in said, said
    assert "confirm" in said, said


def test_a_label_whose_every_release_is_tombstoned_still_succeeds(
    installed, monkeypatch
):
    """A genuine no op, and the reason the refusal is keyed on the drops.

    A tombstoned release was CONFIRMED and then suppressed by a decision this
    person already made, so a sweep that offers none of them has done exactly
    what it was asked to. ``list_for_label`` reports those in ``suppressed`` and
    never in ``dropped``, and this is the test that fails if a build keys its
    refusal on the empty candidate list instead.
    """
    register(LABELS[0])
    for release_id in RELEASES[SLUGS[0]]:
        review.DecisionStore(tombstone.STORE_KEY, installed).record(
            kind=tombstone.KIND_VERSION,
            identity=tombstone.version_identity(
                artist="Label Act", title=f"Release {release_id}"
            ),
            actor="tests",
        )
    bind(monkeypatch, readable(SLUGS[0]))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_a_verification_call_that_raises_fails_the_item_in_the_lookup_vocabulary(
    installed, monkeypatch
):
    """The fourth provider read, which had no failure boundary at all.

    ``_artist_for`` wraps its seam call and ``_verifier`` returned
    ``self.catalogue.search_release`` bare, so an exception from verification
    flew past ``increment``'s ``except LookupFailure`` and failed the item
    through ``jobs.drive``'s generic handler. ``sync-source-lookups-failed`` is
    the single vocabulary this branch's own docstrings claim for "this source
    could not list", and a second spelling of one condition is how the two come
    to disagree about what a person should do next.
    """
    del installed
    register(LABELS[0])
    bind(
        monkeypatch,
        VerificationOutage(
            artists={
                SLUGS[0]: FakePagedArtist(
                    [FakeRelease(release_id) for release_id in RELEASES[SLUGS[0]]]
                )
            },
            answers=0,
        ),
    )
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {SLUGS[0]: "sync-source-lookups-failed"}
    assert job_state(job_id) == str(jobs.JobState.FAILED)


def test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds(
    installed, monkeypatch
):
    """The other no op: an exhausted crawl, which has to keep reporting empty.

    Nothing was read, so nothing was discarded, and there is no dishonesty to
    refuse. U7 records the remaining producer this leaves open, a first page that
    comes back empty from a method that exists, and it stays open here on purpose.
    """
    register(LABELS[0])
    bind(monkeypatch, FakeCatalogue(artists={SLUGS[0]: FakePagedArtist([])}))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_a_sweep_that_confirmed_some_of_what_it_read_succeeds_and_offers_those(
    installed, monkeypatch
):
    """The other arm of the refusal's conjunction, which nothing had pinned.

    The unconfirmed refusal is keyed on BOTH an empty increment AND a dropped
    population. A build that refused on the dropped population alone would fail
    every sweep in which one release was credited to a distributor, over a label
    it had just offered the rest of. A partial confirmation is the ordinary case
    for a real catalogue, so it has to succeed, and what it confirmed has to be
    sitting in the review queue when it does.
    """
    register(LABELS[0])
    bind(
        monkeypatch,
        FakeCatalogue(
            artists={
                SLUGS[0]: FakePagedArtist(
                    [FakeRelease(release_id) for release_id in RELEASES[SLUGS[0]]]
                )
            },
            confirmed={"hf-1"},
        ),
    )
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {"hf-1": SLUGS[0]}


class SessionExpiredAtVerification(FakeCatalogue):
    """A catalogue whose listings answer and whose verification refuses in kind.

    The refusal is one of THIS PRODUCT'S, ``credential-missing``, which is what an
    adapter raises when it discovers at call time that the stored provider
    session has expired. That names an act the person can take. The two
    verification boundaries, the sweep's and the harvest's, each let a
    ``CratekitError`` through unchanged and flatten only a foreign exception,
    and neither passthrough had a test: removing either layer left the suite
    green, because every fake that failed verification failed it with a
    ``RuntimeError``.
    """

    def search_release(self, claimed: str, release: object) -> dict:
        del claimed, release
        raise refuse(
            "credential-missing",
            "the stored provider session expired between the listing and the "
            "verification",
            origin=("tests",),
        )

    def check_label(self, name: str) -> dict:
        del name
        raise refuse(
            "credential-missing",
            "the stored provider session expired between the listing and the "
            "verification",
            origin=("tests",),
        )


def test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason(
    installed, monkeypatch
):
    """An expired session is not "this source could not list".

    Flattening it would send a person to wait for a network that is fine, when
    the act that repairs it is a login. The cause is read off the item row, as
    every failing round in this file reads it.
    """
    del installed
    register(LABELS[0])
    bind(
        monkeypatch,
        SessionExpiredAtVerification(
            artists={
                SLUGS[0]: FakePagedArtist(
                    [FakeRelease(release_id) for release_id in RELEASES[SLUGS[0]]]
                )
            }
        ),
    )
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {SLUGS[0]: "credential-missing"}


def test_a_revoked_tombstone_no_longer_keeps_a_release_out_of_the_queue(
    installed, monkeypatch
):
    """A lifted suppression lifts, which the one read of the store has to honour.

    ``DecisionStore.suppressions`` filters to the suppressing records by default
    and keeps the revoked ones in the document, so a snapshot that asked for
    every record would carry a decision the person already reversed and keep the
    release out of the queue for ever, silently. The sibling test above proves a
    live tombstone suppresses; this one proves a revoked one does not.
    """
    register(LABELS[0])
    store = review.DecisionStore(tombstone.STORE_KEY, installed)
    recorded = store.record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist="Label Act", title="Release hf-1"),
        actor="tests",
    )
    store.revoke(recorded.suppression_id, actor="tests")
    bind(monkeypatch, readable(SLUGS[0]))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}


def corrupt_tombstone_store(cfg: config.Config) -> None:
    """Leave a document in the tombstone store's place that it must refuse.

    A top level list is good JSON and is not this store, which is exactly the
    shape ``DecisionStore._read`` learned to refuse rather than read as empty.
    """
    path = review.DecisionStore(tombstone.STORE_KEY, cfg).path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[]\n")


def test_an_unreadable_tombstone_store_does_not_fail_a_label_with_nothing_to_ask(
    installed, monkeypatch
):
    """THE LAZY READ, which is the behaviour preserving half of the one-read change.

    The per release form only opened the store when a confirmed release asked
    whether it was suppressed, so a label whose crawl listed nothing never read
    it and never met its refusal. A snapshot taken when the reader is built
    would refuse that same label over a file the sweep had no question for. The
    pair below is the composite: the refusal still fires on exactly the runs
    that used to raise it.
    """
    register(LABELS[0])
    corrupt_tombstone_store(installed)
    bind(monkeypatch, FakeCatalogue(artists={SLUGS[0]: FakePagedArtist([])}))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)


def test_an_unreadable_tombstone_store_still_refuses_a_label_with_a_confirmed_release(
    installed, monkeypatch
):
    """The composite for the test above: deferring the read did not lose the refusal.

    A confirmed release has to ask whether it is suppressed, and an unreadable
    suppression list read as empty would re-offer exactly what somebody removed
    on purpose. So this run refuses, with the store's own reason and not a
    lookup failure, because nothing about the provider went wrong.
    """
    register(LABELS[0])
    corrupt_tombstone_store(installed)
    bind(monkeypatch, readable(SLUGS[0]))
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {SLUGS[0]: "review-file-unusable"}
    assert offers(installed) == {}


# ═══════════════════════════════════════════════════════════════════════════
# 7. The resume branch
# ═══════════════════════════════════════════════════════════════════════════


def test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open(installed):
    """A job frozen by a build before U52, met by the build that can drive it.

    REFUSED RATHER THAN REPAIRED, and the job is deliberately left open: filling
    items into a payload frozen by a build with a different idea of the job would
    run work under a configuration snapshot nobody checked. Driving it instead
    would report a clean success, because ``jobs.drive`` transitions a job whose
    item count is zero straight to SUCCEEDED.
    """
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=SWEEP_KEY,
            payload={"source_id": "labels"},
            cfg=installed,
            item_ids=(),
        )
    code, refused = drive(["sync", "labels", "--job", job.job_id])
    assert code == int(ExitCode.INTERNAL), refused
    assert refused["cause"]["reason"] == "internal-error"
    assert job.job_id in refused["cause"]["message"]
    assert job_is_open(job.job_id), (
        "the refusal drove the job anyway, so a later resume would report a "
        "success over work nothing did"
    )


def test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok(
    installed, monkeypatch
):
    """R-225, and the placement that decides it.

    The re-raise sits OUTSIDE the ``is_open`` branch. A job already FAILED on
    entry is not open, so the drive is skipped, and a re-raise written inside the
    branch would be skipped with it: the first ask answers "failed" and every ask
    after it exits 0 over the same unfinished work. ``master/cli.py``'s resume
    branch had no re-raise at all when this was written, which is what this
    asserts was not copied. Every shell calls ``jobs.raise_for_state`` now.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, UnreadableCatalogue())
    job_id = queued_sweep()
    assert drive(["sync", "labels", "--job", job_id])[0] != int(ExitCode.OK)

    code, again = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), again
    # The stored job cause, raised on a closed job. It used to be the wrapper's
    # unavailable-transient. The items failed as sync-source-lookups-failed, which
    # is not retryable, so that is now the job's reason too.
    assert again["cause"]["reason"] == "sync-source-lookups-failed"
    assert again["cause"]["retryable"] is False
    assert again["cause"]["remediation"]["remedy"] != "resume-job"
    assert job_state(job_id) == str(jobs.JobState.FAILED)


def test_a_resume_of_a_cancelled_sweep_does_not_exit_ok_over_the_items_it_never_ran(
    installed, monkeypatch
):
    """ANY closed job carrying a cause, not FAILED alone.

    A run stopped with a signal is CANCELLED, and ``jobs.cancel`` writes a cause
    on it. A resume predicate narrowed to FAILED would skip the drive, because a
    cancelled job is not open, and then skip the re-raise too, exiting 0 over a
    job with none of its items done. Measured on 2026-09-02 as exactly that, and
    it survived the mutation table because nothing here had ever cancelled a job.
    """
    del installed
    register(*LABELS)
    bind(monkeypatch, readable(*SLUGS))
    job_id = queued_sweep()
    with jobs.open_store() as store:
        jobs.cancel(store, job_id)

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), resumed
    assert resumed["cause"]["reason"] == "cancelled"
    assert job_state(job_id) == str(jobs.JobState.CANCELLED)
    assert set(item_states(job_id).values()) == {str(jobs.ItemState.PENDING)}


# ═══════════════════════════════════════════════════════════════════════════
# 8. The frozen configuration reaches the worker
# ═══════════════════════════════════════════════════════════════════════════


def test_the_worker_offers_into_the_library_its_job_was_queued_for(
    installed, tmp_path, monkeypatch
):
    """R17 and KTD9, on a path the worker genuinely resolves against ``cfg``.

    The review queue is LIBRARY scoped, so ``config.state_path`` puts it under the
    configured library and a worker holding a live configuration would offer into
    a different library from the one its job was queued for. The favourite label
    registry cannot prove this and is not asked to: it is installation scoped and
    ``RegistryStore`` takes no configuration at all (KTD6).

    THE DIVERGENCE HAS TO COME FROM THE FILE. ``config.from_dict`` applies
    environment overrides unconditionally and ``jobs.frozen_config`` rebuilds
    through it, so with ``CRATEKIT_LIBRARY_ROOT`` still set both readings relocate
    onto the variable and agree whatever the saved file says. The variable is
    therefore unset, and the database moves WITH the root because KTD21b refuses
    to save one without the other. Recorded in
    ``docs/solutions/workflow-issues/a-frozen-config-is-frozen-against-the-file-not-against-an-env-override.md``.
    """
    register(LABELS[0])
    bind(monkeypatch, readable(SLUGS[0]))
    job_id = queued_sweep()

    elsewhere = tmp_path / "another-library"
    (elsewhere / "Music").mkdir(parents=True)
    (elsewhere / "db").mkdir(parents=True)
    monkeypatch.delenv(config.ENV_LIBRARY_ROOT)
    config.save(
        replace(
            installed,
            library=replace(
                installed.library,
                root=elsewhere,
                db_path=elsewhere / "db" / "master.db",
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

    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}
    assert not review.queue_path(live).exists(), (
        "the worker opened the review store against the CURRENT configuration, "
        "so the offers landed in a library this job was never queued for"
    )


# ═══════════════════════════════════════════════════════════════════════════
# 9. Harvest, the verb that can now succeed
#
# THE DEFECT THESE REPLACE. ``harvest_playlist`` raised
# ``label-playlist-unreadable`` on every call and had never listed a playlist,
# so a person was told their playlist could not be read at a moment when
# nothing had been contacted. A refusal whose stated cause is false is worse
# than an honest one, because it sends somebody to check a playlist that is
# fine.
#
# HARVEST QUEUES NOTHING, so nothing below reads the job store. It runs in
# process, it writes into the review queue, and the queue is the only durable
# record it leaves; every assertion here therefore reads either the emitted
# envelope or the review store, and never an exit code alone.
# ═══════════════════════════════════════════════════════════════════════════

PLAYLIST = "https://example.invalid/playlist/harvest"

#: One imprint the fake catalogue confirms and one it does not. The unconfirmed
#: name is what makes ``unresolved`` able to fail: a build that reported the
#: offered count twice would agree with a fixture where everything is confirmed.
CONFIRMED = "Anjunadeep"
UNCONFIRMED = "Mystery Distro"


def playlist_of(*tracks: FakeTrack) -> FakeCatalogue:
    """A catalogue holding exactly one readable playlist, at ``PLAYLIST``."""
    return FakeCatalogue(
        playlists={PLAYLIST: FakePagedPlaylist(list(tracks))},
        known_labels={CONFIRMED},
    )


def harvested(cfg: config.Config) -> list[str]:
    """The label names sitting in the review queue under ``cfg``, in order.

    Read back from the store rather than taken from the envelope, for the reason
    section 1 gives about items: the envelope is what the verb SAID, and the
    queue is what a person will actually find waiting for them.
    """
    with review.open_store(cfg) as store:
        page = review.list_items(store, queue=str(review.Queue.LABEL_RELEASE))
    return [str(item.payload.get("name")) for item in page.items]


def run_harvest(reference: str = PLAYLIST) -> tuple[int, dict]:
    return drive(["label", "harvest", reference])


def run_harvest_human(reference: str = PLAYLIST) -> tuple[int, str]:
    """The default output a person gets.

    ``drive`` always requests json, which is why every harvest test in this file
    stayed green over a blank human answer. These rows go through the dispatcher
    the way a person does.
    """
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["label", "harvest", reference], stdout=out, stderr=err)
    return code, out.getvalue() or err.getvalue()


def test_harvest_of_a_readable_playlist_offers_one_item_per_verified_label(
    installed, monkeypatch
):
    """The success branch, which no build has ever reached before this unit.

    Both halves are asserted. The envelope names the queue a consumer should go
    and read, and the queue itself holds the offer, because a verb that reported
    a review set and wrote nothing would satisfy either assertion on its own.
    """
    bind(monkeypatch, playlist_of(FakeTrack("t1", copyright="2026 Anjunadeep")))

    code, envelope = run_harvest()

    assert code == int(ExitCode.OK), envelope
    assert envelope["schema"] == "review_set/1"
    assert envelope["data"]["queue"] == str(review.Queue.LABEL_RELEASE)
    assert [item["name"] for item in envelope["data"]["items"]] == [CONFIRMED]
    assert harvested(installed) == [CONFIRMED]


def test_harvest_payload_is_exactly_the_three_declared_review_set_keys(
    installed, monkeypatch
):
    """KTD7's rule on the other surface: no per verb detail beside the contract.

    ``cli.output`` closes ``review_set/1`` with ``additionalProperties: false``
    and ``tests.cli_drive.drive`` validates every envelope, so an undeclared key
    already fails. U51 shipped one anyway on ``job_state/1``, which is why the
    positive half is spelled out rather than left to the validator.
    """
    del installed
    bind(monkeypatch, playlist_of(FakeTrack("t1", copyright="2026 Anjunadeep")))

    code, envelope = run_harvest()

    assert code == int(ExitCode.OK), envelope
    assert set(envelope["data"]) == {"queue", "items", "unresolved"}


def test_a_name_the_catalogue_will_not_confirm_is_counted_and_never_offered(
    installed, monkeypatch
):
    """A copyright string is a heuristic, so an unconfirmed name is not a label."""
    bind(
        monkeypatch,
        playlist_of(
            FakeTrack("t1", copyright="2026 Anjunadeep"),
            FakeTrack("t2", copyright="2026 Mystery Distro"),
        ),
    )

    code, envelope = run_harvest()

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["unresolved"] == 1
    assert harvested(installed) == [CONFIRMED]
    assert UNCONFIRMED not in harvested(installed)


def test_a_track_with_no_copyright_string_is_counted_rather_than_dropped_silently(
    installed, monkeypatch
):
    """The track that yields no NAME at all, which is not the same as a drop.

    ``harvest.from_tracks`` records a drop per name the catalogue refused, and a
    track carrying neither a copyright nor a label credit produces no name for it
    to refuse. Counting only the drops would report a clean zero over a playlist
    whose tracks harvest could not read a thing from, which is the shape of every
    silent-empty defect this branch exists to close.
    """
    bind(
        monkeypatch,
        playlist_of(
            FakeTrack("t1", copyright="2026 Anjunadeep"),
            FakeTrack("t2"),
        ),
    )

    code, envelope = run_harvest()

    assert code == int(ExitCode.OK), envelope
    assert harvested(installed) == [CONFIRMED]
    assert envelope["data"]["unresolved"] == 1, (
        "the track carrying no copyright string was dropped silently, so a "
        "playlist harvest can report nothing wrong having read nothing at all"
    )


def test_an_empty_playlist_offers_nothing_and_reports_zero_rather_than_refusing(
    installed, monkeypatch
):
    """The adversarial half of the unreadable refusal, and the reason it is here.

    A literal reading of "an unreadable playlist must refuse" turns an EMPTY one
    into an error too, and the two are different facts about the world: one
    playlist could not be reached and the other genuinely has nothing in it. A
    build that collapsed them would pass every refusal test above and turn this
    one red, which is exactly what it is for.
    """
    bind(monkeypatch, playlist_of())

    code, envelope = run_harvest()

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["items"] == []
    assert envelope["data"]["unresolved"] == 0
    # NO_OP rather than OK, because "harvested nothing" and "harvested four
    # labels" are both successes and the difference belongs where it can be read.
    assert envelope["outcome"] == "no_op"
    assert harvested(installed) == []


def test_harvest_human_output_names_each_offered_label(installed, monkeypatch):
    """The sitting's missing case: default output names what harvest found.

    A substring match on the name is not enough. Dumping the json envelope as
    text would contain the name inside a quoted key and would not tell a person
    what was harvested. The name is its own indented line, which is the shape
    ``_offered`` put on the envelope for this reason.
    """
    del installed
    bind(monkeypatch, playlist_of(FakeTrack("t1", copyright="2026 Anjunadeep")))

    code, text = run_harvest_human()

    assert code == int(ExitCode.OK), text
    lines = text.splitlines()
    assert f"  {CONFIRMED}" in lines, text
    assert "  unresolved: 0" in lines, text
    assert f"  queue: {review.Queue.LABEL_RELEASE}" in lines, text


def test_harvest_human_output_names_the_unresolved_count_and_not_an_unconfirmed_imprint(
    installed, monkeypatch
):
    """An unconfirmed copyright string is a count, never a harvested label."""
    del installed
    bind(
        monkeypatch,
        playlist_of(
            FakeTrack("t1", copyright="2026 Anjunadeep"),
            FakeTrack("t2", copyright="2026 Mystery Distro"),
        ),
    )

    code, text = run_harvest_human()

    assert code == int(ExitCode.OK), text
    lines = text.splitlines()
    assert f"  {CONFIRMED}" in lines, text
    assert f"  {UNCONFIRMED}" not in lines, text
    assert "  unresolved: 1" in lines, text


def test_an_empty_harvest_still_names_that_nothing_was_offered(installed, monkeypatch):
    """A no_op that prints only the verb and a run id is the original defect.

    The empty playlist is a success, and the human form has to say the set was
    empty rather than looking like the renderer still has no case for it.
    """
    del installed
    bind(monkeypatch, playlist_of())

    code, text = run_harvest_human()

    assert code == int(ExitCode.OK), text
    lines = text.splitlines()
    assert lines[0] == "label.harvest: no_op", text
    assert f"  {CONFIRMED}" not in lines, text
    assert "  unresolved: 0" in lines, text
    assert f"  queue: {review.Queue.LABEL_RELEASE}" in lines, text


def test_a_review_set_item_without_a_name_is_rendered_from_its_own_fields():
    """Harvest is not the only review_set verb. Do not invent a name line."""
    envelope = output.build(
        verb="review.list",
        run_id="r",
        schema=output.current_schema("review_set"),
        started="2026-08-02T00:00:00+00:00",
        data={
            "queue": "deletion",
            "items": [{"id": "abc", "kind": "removed-track", "path": "/x.flac"}],
            "unresolved": 3,
        },
    )

    lines = render.render_review_set(envelope)
    assert "  id=abc, kind=removed-track, path=/x.flac" in lines
    assert "  unresolved: 3" in lines


def test_review_set_rendering_is_gated_on_the_schema_not_an_items_key():
    """Same gate render_checks uses: a later surface with items is not this shape."""
    plan = output.build(
        verb="profile.set",
        run_id="r",
        schema=output.current_schema("plan"),
        started="2026-08-02T00:00:00+00:00",
        data={
            "digest": "d",
            "items": [{"name": CONFIRMED}],
            "totals": {},
            "chunk": None,
        },
    )

    assert render.render_review_set(plan) == []
    assert CONFIRMED not in render.render(plan)


def test_a_playlist_the_catalogue_cannot_resolve_refuses_that_it_was_unreadable(
    installed, monkeypatch
):
    """R13: the slug is earned, because a BOUND provider was asked and failed.

    ``UnreadableCatalogue`` is credentialled and bound and cannot answer, which
    is the only condition this cause may be raised for. The refusal carries
    ``UPSTREAM_UNAVAILABLE``, so a person is sent to the provider rather than to
    their own installation.
    """
    catalogue_fake = bind(monkeypatch, UnreadableCatalogue())

    code, refused = run_harvest()

    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), refused
    assert refused["cause"]["reason"] == "label-playlist-unreadable"
    assert catalogue_fake.playlists_asked_for == [PLAYLIST]
    # The provider's OWN exception type, carried through. The refusal this unit
    # replaced raised the same slug and the same code having asked nothing at
    # all, so the detail is what tells the two builds apart.
    assert refused["cause"]["detail"]["kind"] == "RuntimeError"
    assert harvested(installed) == []


def test_a_playlist_that_resolves_and_cannot_be_listed_refuses_the_same_way(
    installed, monkeypatch
):
    """The second unreadable shape, which reaches the boundary as another type.

    ``listing.ListingNotPaginated`` is a plain ``RuntimeError`` defined in this
    codebase, and the provider's own exception re-raised by
    ``listing.fetch_with_retry`` is whatever the installed client version
    raises. A translation that only knew one of the two would let the other
    escape as an unclassified crash, so both are driven.
    """
    bind(
        monkeypatch,
        FakeCatalogue(playlists={PLAYLIST: UnlistablePlaylist()}),
    )

    code, refused = run_harvest()

    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), refused
    assert refused["cause"]["reason"] == "label-playlist-unreadable"
    assert refused["cause"]["detail"]["kind"] == "ListingNotPaginated"
    assert harvested(installed) == []


def test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist(
    installed, monkeypatch
):
    """A failure that is not the provider's must not be reported as the provider's.

    The review queue is a local file, and a queue written at another schema
    version refuses ``review-schema-mismatch``. Catching every exception at this
    boundary and calling it an unreadable playlist would blame a reachable
    provider for a file on this machine, and send a person to check a playlist
    that is fine, which is the exact defect this unit removes at the top.
    """
    del installed
    from cratekit.core.cause import refuse
    from cratekit.label import harvest as label_harvest

    bind(monkeypatch, playlist_of(FakeTrack("t1", copyright="2026 Anjunadeep")))

    def refusing_tracks(playlist, **kwargs):
        del playlist, kwargs
        raise refuse(
            "review-schema-mismatch",
            "the review queue was written by another build",
            origin=("tests",),
        )

    monkeypatch.setattr(label_harvest, "playlist_tracks", refusing_tracks)

    code, refused = run_harvest()

    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "review-schema-mismatch"


def test_a_provider_that_fails_mid_verification_refuses_rather_than_reporting_a_defect(
    installed, monkeypatch
):
    """The boundary covered only two of the three provider calls harvest makes.

    ``playlist_tracks_or_refuse`` wraps ``playlist_for`` and
    ``playlist_tracks``, and ``found.check_label`` was handed into
    ``from_tracks`` outside it. ``listing.fetch_with_retry`` re-raises the
    provider's own exception once its retry ladder is spent, so a provider outage
    during verification left the verb as ``internal-error`` with
    ``report-defect``: a person whose provider was down was told to file a bug
    against this program. The remedy is asserted as well as the cause, because
    the cause slug alone is what a reader checks and the remedy is what the
    person is actually told to do.
    """
    del installed
    bind(
        monkeypatch,
        VerificationOutage(
            playlists={
                PLAYLIST: FakePagedPlaylist(
                    [
                        FakeTrack("t1", copyright="2026 Anjunadeep"),
                        FakeTrack("t2", copyright="2026 Mystery Distro"),
                    ]
                )
            },
            known_labels={CONFIRMED},
            answers=1,
        ),
    )

    code, refused = run_harvest()

    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), refused
    assert refused["cause"]["reason"] == "label-playlist-unreadable"
    assert refused["cause"]["remediation"]["remedy"] != str(Remedy.REPORT_DEFECT)
    steps = refused["cause"]["remediation"]["steps"]
    assert any("retry" in step for step in steps), steps


def test_a_harvest_that_fails_mid_verification_names_what_it_already_offered(
    installed, monkeypatch
):
    """The partial state nothing named, and it is durable rather than rolled back.

    ``review.offer`` commits per call, so the label confirmed before the outage
    is already sitting in the queue when the refusal is raised. Both halves are
    asserted: the queue holds it, and the refusal SAYS the queue holds it. A
    person who retries this command needs to know, and a build that reported the
    failure without the population would leave them guessing at a review queue
    they cannot see from here.
    """
    bind(
        monkeypatch,
        VerificationOutage(
            playlists={
                PLAYLIST: FakePagedPlaylist(
                    [
                        FakeTrack("t1", copyright="2026 Anjunadeep"),
                        FakeTrack("t2", copyright="2026 Mystery Distro"),
                    ]
                )
            },
            known_labels={CONFIRMED},
            answers=1,
        ),
    )

    code, refused = run_harvest()

    assert code != int(ExitCode.OK), refused
    assert harvested(installed) == [CONFIRMED]
    assert refused["cause"]["detail"]["offered"] == [CONFIRMED]


def test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason(
    installed, monkeypatch
):
    """The harvest half of the passthrough the sweep test in section 6 pins.

    ``_label_verifier`` lets a ``CratekitError`` through and wraps only a foreign
    exception as ``label-playlist-unreadable``. An expired session discovered at
    verification is a login, not an unreadable playlist, and a person told the
    playlist could not be read would go and check a playlist that is fine.
    """
    del installed
    bind(
        monkeypatch,
        SessionExpiredAtVerification(
            playlists={
                PLAYLIST: FakePagedPlaylist([FakeTrack("t1", copyright="2026 Anjunadeep")])
            }
        ),
    )

    code, refused = run_harvest()

    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "credential-missing"


# ═══════════════════════════════════════════════════════════════════════════
# 10. The review round, 2026-09-07
#
# Each test here drives one finding the built in review raised after the merge
# with main. They sit together rather than in their sections because a reader
# of the record should be able to find what a round changed in one place.
# ═══════════════════════════════════════════════════════════════════════════


def test_the_keys_this_verb_will_drive_are_the_keys_bound_to_its_worker():
    """LABEL_KEYS is two spelled strings, so this is what keeps them true."""
    bound_here = {
        key for key, target in handlers.HANDLERS.items() if target == "cratekit.label.cli:handle"
    }
    assert label_cli.LABEL_KEYS == bound_here


def test_a_label_verb_will_not_drive_a_job_queued_for_another_verb(installed):
    """The resume drives whatever the row names, so the row has to be a label job.

    ``handlers.run_job`` resolves the worker from the job and not from the verb,
    which without this check made ``sync labels --job`` a gate free driver for
    any queued job: the outbound shell re-requires its gate and its payload
    digest on resume by design, and a job driven from here would have skipped
    both. The job is left exactly as it was, every item still pending.
    """
    with jobs.open_store() as store:
        foreign = jobs.enqueue(
            store,
            handler_key="export.playlist",
            payload={"playlist": "x"},
            cfg=installed,
            item_ids=("track-1",),
        )

    code, refused = drive(["sync", "labels", "--job", foreign.job_id])

    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "job-unknown"
    assert "export.playlist" in refused["cause"]["message"]
    assert item_states(foreign.job_id) == {"track-1": str(jobs.ItemState.PENDING)}


def test_an_import_on_an_unconfigured_machine_says_so_rather_than_naming_the_label():
    """The sibling of the sweep's fresh install test, which the round found missing.

    The registry is installation scoped and reads on a machine never set up, so
    the import refused ``label-unknown`` first and sent a person to add a label,
    and then refused ``config-unusable`` once they had. One blocker, two
    refusals, in the verb the sweep's own comment claimed to have brought into
    line.
    """
    code, refused = drive(["label", "import", LABELS[0]])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "config-unusable"
    assert queue_is_empty()


def test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out(installed):
    """The job stays open on purpose, so the way out has to be in the steps."""
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=SWEEP_KEY,
            payload={"source_id": "labels"},
            cfg=installed,
            item_ids=(),
        )
    _, refused = drive(["sync", "labels", "--job", job.job_id])
    steps = refused["cause"]["remediation"]["steps"]
    assert any(f"crate job cancel {job.job_id}" in step for step in steps), steps
    # A SWEEP CANNOT BE QUEUED AGAIN (U109), so the way back is the guided verb
    # and never the retired one, which would only refuse.
    assert steps[-1] == "then take label releases with: crate label sync", steps


def test_the_itemless_refusal_of_an_import_still_says_queue_it_again(installed):
    """The other branch of the same step: an import can still be queued."""
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=IMPORT_KEY,
            payload={"source_id": "labels", "name": "Kompakt", "label_id": "kompakt"},
            cfg=installed,
            item_ids=(),
        )
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
    return CountingCatalogue(
        artists={
            label_id: FakePagedArtist(
                [FakeRelease(release_id) for release_id in RELEASES[label_id]]
            )
            for label_id in label_ids
        },
        confirmed=confirmed,
    )


def bury(cfg: config.Config, release_id: str) -> None:
    review.DecisionStore(tombstone.STORE_KEY, cfg).record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(
            artist="Label Act", title=f"Release {release_id}"
        ),
        actor="tests",
    )


def test_a_mixed_listing_of_tombstoned_and_unconfirmed_releases_is_a_label_with_nothing_new(
    installed, monkeypatch
):
    """The false refusal the round found, driven.

    One release the person confirmed and then deleted on purpose, one the
    catalogue credits to a distributor. Nothing is offered, and a guard keyed on
    "anything was dropped" refused this as a catalogue nobody could verify a
    line of, with ``confirmed: 0`` and a remedy to set a match needle, over a
    label that is honestly up to date. Every resume re-listed the same
    catalogue and failed the same way.
    """
    register(LABELS[0])
    bury(installed, "hf-1")
    bind(monkeypatch, counting(SLUGS[0], confirmed=frozenset()))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_a_sweep_that_read_releases_and_confirmed_none_of_them_still_refuses(
    installed, monkeypatch
):
    """The composite for the test above: the refusal it keeps is the one that was true."""
    register(LABELS[0])
    bind(monkeypatch, counting(SLUGS[0], confirmed=frozenset()))
    job_id = queued_sweep()

    drive(["sync", "labels", "--job", job_id])

    assert item_causes(job_id) == {SLUGS[0]: "label-sweep-incomplete"}


def test_a_tombstoned_release_is_never_sent_to_the_provider_for_verification(
    installed, monkeypatch
):
    """The local questions first, the provider call last.

    A tombstone is a decision already made on this machine, so verifying the
    release first spent a provider round trip whose answer the tombstone then
    threw away. On a label with a long deleted back catalogue that was most of
    the sweep's network calls, each one a step nearer the rate limited endpoint
    the unconfirmed refusal exists for.
    """
    register(LABELS[0])
    bury(installed, "hf-1")
    fake = bind(monkeypatch, counting(SLUGS[0]))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert fake.verifications == 1, fake.verifications
    assert offers(installed) == {"hf-2": SLUGS[0]}


def test_one_item_opens_the_review_store_once_however_many_releases_it_offers(
    installed, monkeypatch
):
    """The increment hands the source no store, so the worker has to.

    Without this every offered release opened, migrated and checkpointed the
    review database on its own, measured at 0.386 ms per round trip, which on a
    label at the default cap of four hundred is a hundred and fifty milliseconds
    of connection churn and four hundred checkpoints per label. Counted through
    the module attribute the worker reaches the store by, during the drive
    alone.
    """
    register(LABELS[0])
    bind(monkeypatch, readable(SLUGS[0]))
    job_id = queued_sweep()
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
            "the stored provider session expired before the artist was resolved",
            origin=("tests",),
        )


def test_a_refusal_the_artist_lookup_raises_in_kind_keeps_its_own_reason(
    installed, monkeypatch
):
    """The third seam boundary, brought onto the rule the other two already kept.

    ``_artist_for`` flattened EVERY exception into a lookup failure, so an
    adapter refusing ``credential-missing`` for an expired session became
    "retry when the provider is reachable". The item row carries the adapter's
    own reason now, as it does when the same refusal surfaces one call later at
    verification.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, SessionExpiredAtListing())
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {SLUGS[0]: "credential-missing"}


# ═══════════════════════════════════════════════════════════════════════════
# 12. A release the library already holds is not offered. R-259.
#
# The worker passed an empty owned set, and both filters on the labels path are
# membership tests against the set they are handed, so every sweep offered what
# the library already held. A release is owned when the provider lists at least
# one track on it and the library index the match engine uses resolves every
# one of them as matched. Anything short of that is still offered, because an
# offer costs a person one decline and a release wrongly called owned is music
# they never see.
# ═══════════════════════════════════════════════════════════════════════════


class Row:
    """A provider track row in the shape ``match.read_tidal_tracks`` reads."""

    def __init__(self, track_id: str, artist: str, name: str) -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = ""


#: The tracks on each of the first label's two releases, as the provider lists
#: them when a release is read again by identifier.
TRACKS = {
    "hf-1": ([Row("11", "Aurora Bloom", "Sun Path"), Row("12", "Nova Reef", "Tide")], 2026),
    "hf-2": ([Row("21", "Mira Vale", "Glass Hour")], 2025),
}


def hold(cfg: config.Config, *names: str) -> None:
    """Put files in the library's music folder, named the way the library names them."""
    for name in names:
        (cfg.library.root / cfg.library.music_dir / name).write_bytes(b"")


def tracked(*, releases=None, confirmed=None, cls=FakeCatalogue) -> FakeCatalogue:
    """The first label's catalogue, able to read its releases' tracks."""
    return cls(
        artists={
            SLUGS[0]: FakePagedArtist(
                [FakeRelease(release_id) for release_id in RELEASES[SLUGS[0]]]
            )
        },
        releases=TRACKS if releases is None else releases,
        confirmed=confirmed,
    )


def test_a_label_whose_catalogue_the_library_already_holds_offers_nothing(
    installed, monkeypatch
):
    """R-259's closing condition, driven through the real dispatcher and driver.

    Before the fix both releases were offered, because the worker handed the
    increment an empty owned set and nothing else on the path asked.
    """
    register(LABELS[0])
    hold(
        installed,
        "Aurora Bloom - Sun Path.flac",
        "Nova Reef - Tide.flac",
        "Mira Vale - Glass Hour.flac",
    )
    bind(monkeypatch, tracked())
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {}


def test_a_release_with_one_track_still_missing_is_offered_beside_one_that_is_held(
    installed, monkeypatch
):
    """Every track, not any track. The composite for the test above."""
    register(LABELS[0])
    hold(installed, "Aurora Bloom - Sun Path.flac", "Mira Vale - Glass Hour.flac")
    bind(monkeypatch, tracked())
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert offers(installed) == {"hf-1": SLUGS[0]}


def test_a_release_listing_no_tracks_and_a_release_that_is_gone_are_both_offered(
    installed, monkeypatch
):
    """Two absences that must not read as ownership.

    ``all`` over no tracks is ``True``, so a release the provider lists with
    nothing on it would be called owned by the shortest implementation. A
    release the provider cannot read again is not known to be held either.
    """
    register(LABELS[0])
    hold(installed, "Mira Vale - Glass Hour.flac")
    fake = bind(monkeypatch, tracked(releases={"hf-1": ([], 2026)}))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}
    assert sorted(fake.releases_asked_for) == ["hf-1", "hf-2"]


def test_a_release_the_library_holds_only_in_another_version_is_offered(
    installed, monkeypatch
):
    """A different cut is a question for the person, never ownership."""
    register(LABELS[0])
    hold(
        installed,
        "Aurora Bloom - Sun Path.flac",
        "Nova Reef - Tide.flac",
        "Mira Vale - Glass Hour (Extended Mix).flac",
    )
    bind(monkeypatch, tracked())
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert offers(installed) == {"hf-2": SLUGS[0]}


def test_an_unconfirmed_release_is_never_read_and_a_confirmed_one_is_read_once(
    installed, monkeypatch
):
    """Ownership is a provider read now, so it is asked after verification.

    A release the catalogue will not confirm is not the label's to offer, so
    reading its tracks spends a call on an answer nothing uses. And the owned
    check is asked twice on this path, once by the sweep and again by the
    increment's scope, so an answer that was not kept is two reads per release.
    """
    register(LABELS[0])
    fake = bind(monkeypatch, tracked(confirmed={"hf-1"}))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
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
            "credential-missing",
            "the stored provider session expired before the release was read",
            origin=("tests",),
        )


def test_a_track_read_the_provider_could_not_answer_offers_the_release(
    installed, monkeypatch
):
    """Not owned, offered, and the rest of the label is still swept.

    The listing and the verifier refuse the whole source when the provider
    cannot answer. This read comes after both have succeeded, so the sweep has
    new releases in hand, and refusing would withhold all of them over a
    question whose worst answer is one row a person declines. The library holds
    every track here, so an offer can only come from the failed read.
    """
    register(LABELS[0])
    hold(
        installed,
        "Aurora Bloom - Sun Path.flac",
        "Nova Reef - Tide.flac",
        "Mira Vale - Glass Hour.flac",
    )
    fake = bind(monkeypatch, tracked(cls=TracksOutage))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert offers(installed) == {"hf-1": SLUGS[0], "hf-2": SLUGS[0]}
    assert sorted(fake.releases_asked_for) == ["hf-1", "hf-2"]


def test_three_failed_track_reads_in_a_row_stop_the_asking(installed, monkeypatch):
    """A provider that is down costs three retry ladders, not one per release."""
    register(LABELS[0])
    many = [FakeRelease(f"hf-{n}") for n in range(1, 6)]
    fake = bind(
        monkeypatch, TracksOutage(artists={SLUGS[0]: FakePagedArtist(many)})
    )
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert len(fake.releases_asked_for) == 3, fake.releases_asked_for
    assert sorted(offers(installed)) == [f"hf-{n}" for n in range(1, 6)]


def test_a_release_that_is_gone_breaks_the_run_of_failed_reads(installed, monkeypatch):
    """Gone is the provider answering, so it resets the count as a read does."""

    class Alternating(FakeCatalogue):
        def release_tracks(self, release_id: str):
            self.releases_asked_for.append(release_id)
            if release_id in {"hf-3", "hf-6"}:
                raise ReleaseUnresolvable(f"no catalogue release {release_id!r}")
            raise RuntimeError("the provider answered 503 after the retry ladder")

    register(LABELS[0])
    many = [FakeRelease(f"hf-{n}") for n in range(1, 8)]
    fake = bind(monkeypatch, Alternating(artists={SLUGS[0]: FakePagedArtist(many)}))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert len(fake.releases_asked_for) == 7, fake.releases_asked_for


def test_a_sweep_of_two_labels_walks_the_library_once(installed, monkeypatch):
    """One view per job. A view per item walked the whole music volume per label."""
    from cratekit.acquire import match_cli

    register(LABELS[0], LABELS[1])
    walks: list[object] = []
    real_view = match_cli.library_view

    def counted_view(cfg):
        walks.append(cfg)
        return real_view(cfg)

    monkeypatch.setattr(match_cli, "library_view", counted_view)
    bind(
        monkeypatch,
        FakeCatalogue(
            artists={
                slug: FakePagedArtist([FakeRelease(one) for one in RELEASES[slug]])
                for slug in SLUGS[:2]
            },
            releases={**TRACKS, "ot-1": ([Row("31", "Lumen Drift", "Salt Road")], 2024)},
        ),
    )
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert len(walks) == 1, len(walks)
    assert set(offers(installed)) == {"hf-1", "hf-2", "ot-1"}


def test_a_refusal_the_track_read_raises_in_kind_keeps_its_own_reason(
    installed, monkeypatch
):
    """The same pass through rule the other three seam boundaries keep."""
    del installed
    register(LABELS[0])
    bind(monkeypatch, tracked(cls=TracksSessionExpired))
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {SLUGS[0]: "credential-missing"}


def test_a_release_with_a_row_the_reader_cannot_read_is_offered(installed, monkeypatch):
    """A row naming no artist is a track nobody can look for, so it is not held.

    Every row the reader CAN read is in the library here, so the offer can come
    only from the unreadable one.
    """
    register(LABELS[0])
    hold(
        installed,
        "Aurora Bloom - Sun Path.flac",
        "Nova Reef - Tide.flac",
        "Mira Vale - Glass Hour.flac",
    )
    releases = {
        **TRACKS,
        "hf-2": ([Row("21", "Mira Vale", "Glass Hour"), Row("22", "", "Untitled")], 2025),
    }
    bind(monkeypatch, tracked(releases=releases))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert offers(installed) == {"hf-2": SLUGS[0]}


def test_a_track_read_that_succeeds_breaks_the_run_of_failed_reads(
    installed, monkeypatch
):
    """An answer resets the count, so failures that are not in a row never stop it."""

    class Intermittent(FakeCatalogue):
        def release_tracks(self, release_id: str):
            self.releases_asked_for.append(release_id)
            if release_id in {"hf-3", "hf-6"}:
                return (Row(release_id, "Lumen Drift", release_id),), 2026, None
            raise RuntimeError("the provider answered 503 after the retry ladder")

    register(LABELS[0])
    many = [FakeRelease(f"hf-{n}") for n in range(1, 8)]
    fake = bind(monkeypatch, Intermittent(artists={SLUGS[0]: FakePagedArtist(many)}))
    job_id = queued_sweep()

    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code == int(ExitCode.OK), resumed
    assert len(fake.releases_asked_for) == 7, fake.releases_asked_for


# ═══════════════════════════════════════════════════════════════════════════
# 13. A rate limit is retryable, and resuming retries exactly those labels. R-704.
# ═══════════════════════════════════════════════════════════════════════════


class Limit:
    """Whether the provider is answering rate limited, shared by every fake below."""

    def __init__(self) -> None:
        self.on = True
        self.answered = 0


class RateLimitedArtist(FakePagedArtist):
    """A label listing the provider refuses with its own ``TooManyRequests``.

    The class is the client's, not a stand in, because the sweep's question is
    asked of the provider's own type and a fake spelling of it would prove only
    that the fake was recognized.
    """

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
    """The crawl's real retry ladder, every rung climbed, none of it slept.

    ``listing.fetch_with_retry`` sleeps 31 real seconds before re-raising, and
    ``list_for_label`` exposes no seam for it. Only the sleep is replaced: the
    retry count, the pagination wrapper and the re-raise all run as shipped,
    so the provider's error reaches the sweep as the ladder re-raises it.

    NOT THE WHOLE LIVE PATH, and the difference is the provider gate. These
    fakes make no HTTP call, so the gate never sees an answer. Live, six 429s
    in a row on one ladder trip it and the item parks before the sweep sees
    the error; what reaches the sweep's boundary is a limit that did not trip
    it, the sitting's single album read among them, which the verification
    test below drives.
    """
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
    fake = FakeCatalogue(
        artists={
            SLUGS[0]: FakePagedArtist([FakeRelease(one) for one in RELEASES[SLUGS[0]]]),
            SLUGS[1]: RateLimitedArtist(
                [FakeRelease(one) for one in RELEASES[SLUGS[1]]], limit
            ),
        }
    )
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
    """R-704, the eleventh sitting's shape: one label settled, one rate limited.

    The sitting recorded every rate limited label ``permanent_failed`` and the
    job said resuming could not succeed. The listing climbed the whole ladder,
    so the error the sweep sees is the one the provider raised last.
    """
    del installed
    register(*LABELS[:2])
    waits = _ladder_without_waiting(monkeypatch)
    _, limit = _one_label_rate_limited(monkeypatch)
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    assert limit.answered == 6 and len(waits) == 5, (limit.answered, waits)
    assert item_states(job_id) == {
        SLUGS[0]: str(jobs.ItemState.DONE),
        SLUGS[1]: str(jobs.ItemState.FAILED),
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
    """R-704's Closes when: ``crate job resume`` re-arms exactly those items.

    The resume verb re-arms and spawns a child; the child is the argument list
    it was handed, driven here in process so the second pass is observable.
    The settled label is not listed again, which is the spend the sitting's
    only remedy, a whole new sweep, paid on the 27 labels that had succeeded.
    """
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
        SLUGS[0]: str(jobs.ItemState.DONE),
        SLUGS[1]: str(jobs.ItemState.PENDING),
    }
    assert len(spawned) == 1 and spawned[0][:4] == ["sync", "labels", "--job", job_id]

    limit.on = False
    code, finished = drive(spawned[0])

    assert code == int(ExitCode.OK), finished
    assert finished["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert item_states(job_id) == {slug: str(jobs.ItemState.DONE) for slug in SLUGS[:2]}
    assert fake.asked_for == [SLUGS[0], SLUGS[1], SLUGS[1]]
    assert offers(installed) == {
        "hf-1": SLUGS[0],
        "hf-2": SLUGS[0],
        "ot-1": SLUGS[1],
    }


def test_a_rate_limited_verification_is_retryable_too(installed, monkeypatch):
    """The sitting's error was an album read, and verification is one with no ladder.

    Every provider boundary in the sweep asks the same question, so a limit
    met by the verifier rather than the listing is the same retryable cause.
    """
    del installed
    register(LABELS[0])
    limit = Limit()
    bind(
        monkeypatch,
        RateLimitedVerification(
            artists={
                SLUGS[0]: FakePagedArtist([FakeRelease(one) for one in RELEASES[SLUGS[0]]])
            },
            limit=limit,
        ),
    )
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    assert limit.answered == 1
    cause = item_cause(job_id, SLUGS[0])
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is True
    assert failed["cause"]["retryable"] is True
    assert failed["cause"]["inner"]["retryable"] is True


def test_a_listing_failure_that_is_not_a_rate_limit_stays_permanent(
    installed, monkeypatch
):
    """The split is a rate limit against everything else, not a blanket retry.

    The same catalogue error the suite has always driven, an outage spelled as
    a plain ``RuntimeError``, keeps the permanent reading and its own sentence.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, UnreadableCatalogue())
    job_id = queued_sweep()

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
    """An artist whose listing attribute is a lazy read the provider refuses.

    ``crawl.can_list`` reads the attribute with ``getattr`` and a default,
    which swallows only ``AttributeError``, so the provider's own error
    reaches the sweep's probe boundary rather than the listing's.
    """

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
def test_a_rate_limit_at_every_other_sweep_boundary_is_retryable(
    installed, monkeypatch, fake
):
    """R-704. The sweep has four provider boundaries and each asks the question.

    The listing and the verifier are driven above; these are the other two,
    the resolve of the label's artist and the probe of its listing methods.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, fake())
    job_id = queued_sweep()

    code, failed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), failed
    cause = item_cause(job_id, SLUGS[0])
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is True
    assert "TooManyRequests: Artist unavailable" in cause.message


# ═══════════════════════════════════════════════════════════════════════════
# R-515: a harvest over a playlist the provider lists short
# ═══════════════════════════════════════════════════════════════════════════


def test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns(
    installed, monkeypatch
):
    bind(
        monkeypatch,
        FakeCatalogue(
            playlists={
                PLAYLIST: FakePagedPlaylist(
                    [FakeTrack("t1", copyright="2026 Anjunadeep")], declared=3
                )
            },
            known_labels={CONFIRMED},
        ),
    )
    code, envelope = run_harvest()

    assert code == int(ExitCode.OK), envelope
    assert harvested(installed) == [CONFIRMED]
    assert set(envelope["data"]) == {"queue", "items", "unresolved"}
    (warning,) = [
        w for w in envelope["warnings"] if w["code"] == "label-harvest-playlist-withheld"
    ]
    assert "3 declared, 1 listed, 2 withheld by the provider" in warning["message"]


def test_a_harvest_over_a_full_playlist_warns_nothing(installed, monkeypatch):
    del installed
    bind(
        monkeypatch,
        FakeCatalogue(
            playlists={
                PLAYLIST: FakePagedPlaylist(
                    [FakeTrack("t1", copyright="2026 Anjunadeep")], declared=1
                )
            },
            known_labels={CONFIRMED},
        ),
    )
    code, envelope = run_harvest()
    assert code == int(ExitCode.OK), envelope
    assert envelope.get("warnings", []) == []
