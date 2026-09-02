"""U4: neither label verb can queue a job with nothing to claim.

WHAT THIS FILE GUARDS THAT NO OTHER SUITE CAN. ``cratekit.core.jobs.drive``
transitions a job whose item count is zero straight to SUCCEEDED, because
nothing was attempted and nothing failed. Both label verbs called ``enqueue``
with no ``item_ids`` at all, so a person who queued a sweep and later resumed it
was told it succeeded over a registry nothing was read from.
``tests/modules/test_labels.py`` proves the sweep engine keeps its promises when
called directly and has always passed, because nothing in ``src`` queued an item
for it to claim. This file is about the enqueue: that the registry decides the
items, that an empty registry refuses instead of queueing, and that a person is
told the catalogue seam is unbound at the one moment the information is still
useful to them.

THE ITEMS ARE READ BACK FROM THE STORE rather than inferred from the envelope.
The envelope is exactly ``job_state/1``, four keys and no item list, so the only
thing that can see an item row is the queue itself. A refusal is likewise proven
by the ABSENCE of a job row rather than by the exception alone: a verb that
queued first and refused afterwards would raise the same cause and leave the
empty job sitting in the queue for a later resume to succeed at.

NOTHING HERE DRIVES A JOB. U4 is the enqueue half; the worker, the bindings and
the resume branch are U5's, and the two handler keys are still unbound while this
file is written.
"""

from __future__ import annotations

import pytest

from cratekit.core import config, jobs
from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue
from tests.cli_drive import drive
from tests.test_config import valid_data

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
