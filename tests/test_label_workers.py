"""U4 and U5: the two label verbs queue real items and then run them.

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

from dataclasses import replace

import pytest

from cratekit.cli import handlers, registry
from cratekit.core import config, jobs, review
from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue, sweep
from cratekit.label import cli as label_cli
from tests.cli_drive import drive
from tests.label_fakes import (
    FakeCatalogue,
    FakePagedArtist,
    FakeRelease,
    UnreadableCatalogue,
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
# 1. The sweep's items are the registry
# ═══════════════════════════════════════════════════════════════════════════


def test_a_sweep_queues_one_item_per_registered_label(installed):
    """One favourite label is one item (KTD1), and the id is the identifier."""
    del installed
    register(*LABELS)
    code, queued = drive(["sync", "labels"])
    assert code == int(ExitCode.OK), queued
    assert queued_items(queued["data"]["job_id"]) == list(SLUGS)


def test_a_sweep_carries_the_identifier_and_never_the_display_name(installed):
    """R19 in the one place it can be broken silently.

    A display name is what a person typed and a rename moves it, so an item keyed
    on one is an item the registry can no longer answer for. Asserted as a
    disjointness rather than by equality alone, so a build that carried both
    fails here too.
    """
    del installed
    register(*LABELS)
    code, queued = drive(["sync", "labels"])
    assert code == int(ExitCode.OK), queued
    carried = set(queued_items(queued["data"]["job_id"]))
    assert carried == set(SLUGS)
    assert carried.isdisjoint(set(LABELS))


def test_a_sweep_with_an_empty_registry_refuses_and_queues_nothing(installed):
    """The zero item rule, proven by the absence of a job row.

    A verb that enqueued and then refused would raise this same cause and leave
    the empty job in the queue, where a later resume would drive it to SUCCEEDED
    over work nothing did. Only the queue can see that difference.
    """
    del installed
    code, refused = drive(["sync", "labels"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert code != int(ExitCode.USAGE)
    assert refused["cause"]["reason"] == "label-registry-empty"
    assert queue_is_empty()


def test_the_empty_registry_refusal_names_the_command_that_fixes_it(installed):
    """A remedy a person can act on, rather than a diagnostic to go and run."""
    del installed
    code, refused = drive(["sync", "labels"])
    assert code == int(ExitCode.PRECONDITION), refused
    steps = refused["cause"]["remediation"]["steps"]
    assert any("crate label registry add" in step for step in steps), steps


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


@pytest.mark.parametrize(
    "verb",
    [["sync", "labels"], ["label", "import", "Kompakt"]],
    ids=["sync.labels", "label.import"],
)
def test_both_queueing_paths_warn_that_no_catalogue_adapter_is_bound(installed, verb):
    """Told at the moment it is still actionable, and still queued.

    A refusal here would refuse work a later build could run, which is the reason
    ``catalogue.bound`` gives for existing beside ``catalogue.resolve``. So the
    assertion is BOTH halves: the warning is present and the job is queued anyway.
    """
    del installed
    assert catalogue.bound() is False
    register(*LABELS)
    code, queued = drive(verb)
    assert code == int(ExitCode.OK), queued
    codes = {warning["code"] for warning in queued.get("warnings") or ()}
    assert "label-catalogue-unbound" in codes
    assert queued_items(queued["data"]["job_id"])


@pytest.mark.parametrize(
    "verb",
    [["sync", "labels"], ["label", "import", "Kompakt"]],
    ids=["sync.labels", "label.import"],
)
def test_the_unbound_warning_says_the_job_will_fail_at_the_provider_seam(
    installed, verb
):
    """A code alone is a slug; the sentence is what a person reads."""
    del installed
    register(*LABELS)
    code, queued = drive(verb)
    assert code == int(ExitCode.OK), queued
    said = [
        warning["message"]
        for warning in queued.get("warnings") or ()
        if warning["code"] == "label-catalogue-unbound"
    ]
    assert said and "provider seam" in said[0], queued.get("warnings")


def test_a_refused_sweep_carries_no_warning_because_nothing_was_queued(installed):
    """The warning belongs to a queued job, so a refusal must not carry one.

    A refusal telling a person their job will fail at the provider seam would be
    naming a job that does not exist.
    """
    del installed
    code, refused = drive(["sync", "labels"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert not (refused.get("warnings") or ())


def test_the_warning_rides_the_envelope_rather_than_the_job_state_payload(installed):
    """KTD7: the payload stays exactly the four ``job_state/1`` keys.

    ``cli.output`` closes that surface with ``additionalProperties: false`` and
    ``tests.cli_drive.drive`` validates every envelope it emits, so an undeclared
    key would already fail. This says the positive half as well: the warning is a
    sibling of ``data`` and not a field inside it.
    """
    del installed
    register(*LABELS)
    code, queued = drive(["sync", "labels"])
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
    job_id = queued_job(["sync", "labels"])
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
    job_id = queued_job(["sync", "labels"])
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
    job_id = queued_job(["sync", "labels"])
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
    job_id = queued_job(["sync", "labels"])
    code, failed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    assert item_causes(job_id) == {SLUGS[0]: "sync-source-lookups-failed"}
    assert job_state(job_id) == str(jobs.JobState.FAILED)
    assert failed["cause"]["reason"] == "no-evidence"


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
    job_id = queued_job(["sync", "labels"])
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
    job_id = queued_job(["sync", "labels"])
    code, removed = drive(["label", "registry", "remove", LABELS[0]])
    assert code == int(ExitCode.OK), removed

    code, failed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    causes = item_causes(job_id)
    assert causes[SLUGS[0]] == "label-unknown"
    assert causes[SLUGS[1]] is None
    assert item_states(job_id)[SLUGS[1]] == str(jobs.ItemState.DONE)


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
    branch has no re-raise at all, which is what this asserts was not copied.
    """
    del installed
    register(LABELS[0])
    bind(monkeypatch, UnreadableCatalogue())
    job_id = queued_job(["sync", "labels"])
    assert drive(["sync", "labels", "--job", job_id])[0] != int(ExitCode.OK)

    code, again = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), again
    assert again["cause"]["reason"] == "unavailable-transient"
    assert job_state(job_id) == str(jobs.JobState.FAILED)


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
    job_id = queued_job(["sync", "labels"])

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
