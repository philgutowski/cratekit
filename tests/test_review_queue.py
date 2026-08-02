"""U11: the review queue, the decision stores, and the split between them.

R12 in one sentence: every state the product asks a person to adjudicate is a
persisted, addressable review item, never a file the user must hand edit. The
source system's answer is a spread of comma-separated files a person opens in a
spreadsheet, edits, and saves, and the failure modes of that shape are what this
suite asserts against:

* it re-prompts unconditionally every run, because a decision is not recorded
  anywhere a later run consults;
* it has no rejected state at all, so an item a person looked at and turned down
  is indistinguishable from one nobody has reached yet, and unresolved items roll
  forward forever;
* it is per set directory, so a decision made on one machine is invisible to the
  next, and a decision made this morning is invisible after the directory is
  cleaned up.

Every test here is written against those three, and the harder ones use a REAL
second process rather than a second handle in the same interpreter. A second
handle shares the interpreter's memory, so it can only prove that a value was
kept; a second process can only see what actually reached the disk.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output
from cratekit.core import config, review
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from tests import _pending
from tests._pending import requires
from tests._source_guards import (
    calls_review,
    constructs_a_csv_writer,
    constructs_review,
    methods_on_review_construction,
    offers_into,
    package_modules,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library, saved, so a second process resolves the same one.

    The environment variable is set as well as the file, and it has to be: the
    suite's isolation fixture already points the library root somewhere, and
    ``from_dict`` relocates a configured root onto whatever the environment says.
    Writing only the file would leave the value under test and the value in force
    as two different directories, which is the exact P2 shape.
    """
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def store(cfg):
    with review.open_store(cfg) as opened:
        yield opened


def _in_another_process(*argv: str) -> subprocess.CompletedProcess:
    """Run the real command line in a genuinely separate interpreter.

    The environment is inherited, which is what makes this honest: the suite's
    isolation fixtures redirect every state root through environment variables,
    so the child resolves the same temporary library and the same temporary
    installation state as the parent, and nothing real is reachable from either.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    return subprocess.run(
        [sys.executable, "-m", "cratekit.cli", *argv],
        env=env,
        capture_output=True,
        text=True,
    )


def _start_another_process(*argv: str) -> subprocess.Popen:
    """Start the real command line WITHOUT waiting, so two of them overlap.

    ``_in_another_process`` waits, which serializes what a race test needs to
    interleave. Everything else about the environment is the same.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    return subprocess.Popen(
        [sys.executable, "-m", "cratekit.cli", *argv],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _in_separate_processes(script: str, *, workers: int, arguments) -> None:
    """Run one short script in several REAL interpreters at once, and check each.

    A thread would share this interpreter's memory and its locks, so it can only
    ever prove that a value was kept. Only a separate process can show what
    actually reached the disk, which is the whole question a decision store has
    to answer.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    running = [
        subprocess.Popen(
            [sys.executable, "-c", script, *(str(value) for value in arguments(worker))],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for worker in range(workers)
    ]
    for process in running:
        out, err = process.communicate()
        assert process.returncode == 0, err or out


def _drive(*argv: str) -> tuple[int, dict, str]:
    """Run the real dispatcher in process and return the parsed envelope.

    Used for everything except the cross process scenarios, which need a real
    interpreter on each side and use ``_in_another_process`` instead.
    """
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue()), err.getvalue()


def _offer_one(store, *, key: str = "a", **overrides):
    """One item in the version-match queue, with a stable identity."""
    fields = {
        "queue": review.Queue.VERSION_MATCH,
        "kind": "version-difference",
        "identity": {"source": "list-1", "row": key},
        "payload": {"wanted": f"track {key}", "found": f"track {key} (edit)"},
        "options": (
            review.Option(option_id="opt-accept", summary="the edit is the same recording"),
            review.Option(option_id="opt-other", summary="a different recording entirely"),
        ),
        "handler_key": "match.run",
    }
    fields.update(overrides)
    return review.offer(store, **fields)


# ═══════════════════════════════════════════════════════════════════════════
# Part 1: identity, and the storage that survives the process
# ═══════════════════════════════════════════════════════════════════════════


def test_an_item_identifier_is_derived_from_stable_facts_rather_than_a_display_name():
    """D5. A record keyed by what a thing is CALLED is orphaned by a rename.

    The identifier is a function of the queue, the kind, and an identity mapping
    the producer supplies, so two producers that mean the same candidate agree
    without coordinating, and a display name changing moves nothing.
    """
    first = review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", {"row": "7"})
    again = review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", {"row": "7"})
    other = review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", {"row": "8"})
    assert first == again
    assert first != other
    # Key order is not identity: a producer that builds its mapping differently
    # must not manufacture a second item for the same candidate.
    assert review.item_id_for(
        review.Queue.VERSION_MATCH, "version-difference", {"a": "1", "b": "2"}
    ) == review.item_id_for(
        review.Queue.VERSION_MATCH, "version-difference", {"b": "2", "a": "1"}
    )


def test_an_identity_with_nothing_in_it_is_refused():
    """An empty identity hashes to one value, so every item would collide."""
    with pytest.raises(CratekitError) as excinfo:
        review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", {})
    assert excinfo.value.cause.reason == "review-selection-invalid"


# ── The identity is NORMALIZED before it is hashed ───────────────────────────
#
# This is the module's central claim and the whole reason three comma separated
# files fold into one queue: two producers that mean the same candidate agree
# without coordinating. The identity mapping and the kind are both free-form
# producer input, and a canonical JSON hash distinguishes 7 from "7", so the
# claim was false for the commonest disagreement there is. ``_same_value``
# already exists in this module because this codebase mixes text and numeric
# spellings of one fact, and the identity is where that mix costs the most.


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ({"track_id": 7}, {"track_id": "7"}),
        ({"track_id": 7.0}, {"track_id": "7"}),
        ({"flag": True}, {"flag": "true"}),
        ({"pair": [1, "2"]}, {"pair": ["1", 2]}),
        ({"nested": {"row": 3}}, {"nested": {"row": "3"}}),
    ],
)
def test_the_same_candidate_spelled_two_ways_is_one_identifier(left, right):
    """A type difference is not a different candidate.

    Observed before this: ``{"track_id": 7}`` and ``{"track_id": "7"}`` produced
    different identifiers, so the same candidate was asked about twice and the
    second question could not be recognized as the first.
    """
    assert review.item_id_for(
        review.Queue.VERSION_MATCH, "version-difference", left
    ) == review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", right)
    assert review.suppression_id_for("declines", "removed-file", left) == (
        review.suppression_id_for("declines", "removed-file", right)
    )


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ({"track_id": None}, {"track_id": "None"}),
        ({"track_id": None}, {"track_id": ""}),
        ({"flag": True}, {"flag": 1}),
        ({"track_id": "7"}, {"track_id": " 7"}),
    ],
)
def test_normalizing_the_identity_does_not_collapse_facts_that_differ(left, right):
    """The other direction, and it is the one that would be dangerous.

    ``_same_value`` refuses to match ``None`` against the text ``"None"``
    because "this field is absent" and "this field says None" are different
    facts. Collapsing them in an identity would merge two candidates onto one
    item and settle a decision nobody made about the second.
    """
    assert review.item_id_for(
        review.Queue.VERSION_MATCH, "version-difference", left
    ) != review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", right)


def test_the_same_candidate_under_two_spellings_of_one_kind_is_one_item(store):
    """A kind is an identifier and never a display name (D5, R19).

    Two producers describing one candidate wrote ``version-difference`` and
    ``version_difference``, which produced a third item for a candidate that was
    already in the queue twice.
    """
    identity = {"source": "list-1", "row": "a"}
    first = review.offer(
        store,
        queue=review.Queue.VERSION_MATCH,
        kind="version-difference",
        identity=identity,
        payload={"wanted": "one"},
    )
    again = review.offer(
        store,
        queue=review.Queue.VERSION_MATCH,
        kind="Version_Difference",
        identity=identity,
        payload={"wanted": "one"},
    )
    assert again.item_id == first.item_id
    assert again.kind == first.kind, (
        "the stored kind is the normalized one on both sides, or a predicate "
        "written against one spelling silently matches nothing"
    )
    assert review.count_unresolved(store) == 1


def test_an_item_records_the_identity_it_was_addressed_by(store):
    """Stored, so a duplicate or a collision is detectable AFTERWARDS.

    A content addressed identifier with no record of what it was derived from
    can be checked by nobody: two candidates that hash alike are indistinguishable
    from one candidate offered twice, which is the failure that looks most like
    the feature working.
    """
    item = _offer_one(store)
    assert review.identity_of(store, item.item_id) == {"source": "list-1", "row": "a"}


def test_two_different_candidates_that_hash_alike_are_refused_rather_than_merged(
    store, monkeypatch
):
    """A collision must never be settled silently by the first one there.

    The digest is forced here rather than searched for, because the point is what
    the queue does WHEN one happens, not how unlikely it is.
    """
    monkeypatch.setattr(review, "item_id_for", lambda *args, **kwargs: "rv_forced")
    review.offer(
        store,
        queue=review.Queue.VERSION_MATCH,
        kind="version-difference",
        identity={"source": "list-1", "row": "a"},
        payload={},
    )
    with pytest.raises(CratekitError) as excinfo:
        review.offer(
            store,
            queue=review.Queue.VERSION_MATCH,
            kind="version-difference",
            identity={"source": "list-1", "row": "b"},
            payload={},
        )
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_the_queue_lives_where_the_state_inventory_says_and_is_owner_only(cfg, store):
    """P1: the file mode and the DIRECTORY mode, because one without the other is nothing."""
    declared = config.state_path("review_queue", cfg)
    assert review.queue_path(cfg).parent == declared
    assert review.queue_path(cfg).exists()
    if hasattr(os, "chmod"):
        assert declared.stat().st_mode & 0o777 == config.PRIVATE_DIR_MODE
        assert review.queue_path(cfg).stat().st_mode & 0o777 == config.PRIVATE_FILE_MODE


def test_every_file_the_queue_creates_is_owner_only_derived_by_walking(cfg, store):
    """P3: the set is DERIVED by walking, never listed.

    The version of this that named the database alone would have missed the
    write-ahead log beside it, which is where the queue's contents actually live
    until a checkpoint, and it would have kept missing every file added later.
    """
    _offer_one(store)
    root = config.state_path("review_queue", cfg)
    if not hasattr(os, "chmod"):  # pragma: no cover - platforms without POSIX modes
        return
    for current, directories, files in os.walk(root):
        for name in directories:
            path = Path(current) / name
            assert path.stat().st_mode & 0o777 == config.PRIVATE_DIR_MODE, path
        for name in files:
            path = Path(current) / name
            assert path.stat().st_mode & 0o777 == config.PRIVATE_FILE_MODE, path


def test_an_offered_item_is_addressable_and_starts_unresolved(store):
    item = _offer_one(store)
    assert item.item_id
    assert item.verdict is None
    assert review.get(store, item.item_id) == item


def test_an_item_survives_the_handle_that_created_it(cfg, store):
    item = _offer_one(store)
    store.close()
    with review.open_store(cfg) as reopened:
        assert review.get(reopened, item.item_id).payload == item.payload


def test_an_unknown_identifier_refuses_by_name_rather_than_returning_nothing(store):
    """Returning None would make a typo indistinguishable from an empty queue."""
    with pytest.raises(CratekitError) as excinfo:
        review.get(store, "rv_not_a_real_item")
    assert excinfo.value.cause.reason == "review-item-unknown"
    assert excinfo.value.cause.detail["item_id"] == "rv_not_a_real_item"


def test_offering_the_same_candidate_twice_produces_one_item(store):
    first = _offer_one(store)
    second = _offer_one(store)
    assert first.item_id == second.item_id
    assert len(review.list_items(store).items) == 1


def test_a_queue_nothing_declares_is_refused_and_the_refusal_names_the_declared_ones(store):
    with pytest.raises(CratekitError) as excinfo:
        _offer_one(store, queue="not-a-declared-queue")
    cause = excinfo.value.cause
    assert cause.reason == "review-queue-undeclared"
    assert "not-a-declared-queue" in cause.message


# ═══════════════════════════════════════════════════════════════════════════
# Part 2: the split between an adjudication surface and a plain output
# ═══════════════════════════════════════════════════════════════════════════


def test_every_declared_surface_says_which_side_of_the_split_it_is_on():
    """Approach step 4: name the split. Outputs stay files.

    Asserted over the DECLARATION rather than over a list here, so a surface
    added later is covered the day it lands.
    """
    assert review.SURFACES
    for surface in review.SURFACES:
        assert surface.why, f"{surface.legacy_file} does not say why"
        if surface.adjudicated:
            assert surface.queue is not None, f"{surface.legacy_file} adjudicates nothing"
        else:
            assert surface.queue is None, (
                f"{surface.legacy_file} is a plain output and must not name a queue; "
                f"outputs stay files"
            )


def test_the_declared_queues_are_exactly_the_adjudicated_surfaces_queues():
    """Both directions, because each one rots differently.

    A queue with no surface behind it is a slug nobody can say why exists. A
    surface pointing at a queue the enum does not declare is a producer that will
    refuse at run time on a value the table already promised.
    """
    declared = {str(surface.queue) for surface in review.SURFACES if surface.adjudicated}
    assert declared == set(review.adjudicated_queues())
    assert declared == {str(member) for member in review.Queue}


def test_several_legacy_files_may_fold_into_one_queue_and_that_is_the_point():
    """Fourteen files becoming one surface is the unit's goal, not an accident.

    The same question asked in three files is how a person answers it in one and
    the other two keep asking, so the table is allowed to point several files at
    one queue and is NOT allowed to give one file two.
    """
    files = [surface.legacy_file for surface in review.SURFACES if surface.legacy_file]
    assert len(files) == len(set(files))
    folded = [s.legacy_file for s in review.SURFACES if s.adjudicated and s.legacy_file]
    queues = {str(s.queue) for s in review.SURFACES if s.adjudicated and s.legacy_file}
    assert len(folded) > len(queues), (
        "no legacy file folds into a shared queue, so this table is a rename "
        "rather than a consolidation"
    )


def test_a_plain_output_cannot_be_smuggled_into_the_queue(store):
    """The split has teeth only if the queue refuses the other side of it."""
    output = next(s for s in review.SURFACES if not s.adjudicated)
    with pytest.raises(CratekitError) as excinfo:
        _offer_one(store, queue=output.legacy_file)
    assert excinfo.value.cause.reason == "review-queue-undeclared"


# ═══════════════════════════════════════════════════════════════════════════
# Part 3: a different process, which is the requirement R12 actually states
# ═══════════════════════════════════════════════════════════════════════════


def test_an_item_resolved_in_one_process_is_seen_resolved_by_another(cfg, store):
    """The plan's first test scenario, run with a real interpreter on each side."""
    item = _offer_one(store)
    store.close()

    done = _in_another_process(
        "--output", "json", "review", "resolve", item.item_id, "--verdict", "accepted",
        "--option", "opt-accept",
    )
    assert done.returncode == 0, done.stderr
    envelope = json.loads(done.stdout)
    assert envelope["data"]["items"][0]["verdict"] == "accepted"

    with review.open_store(cfg) as reopened:
        settled = review.get(reopened, item.item_id)
    assert settled.verdict is review.Verdict.ACCEPTED
    assert settled.option == "opt-accept"
    assert settled.actor


# ═══════════════════════════════════════════════════════════════════════════
# Part 4: a verdict persists, so the same decision is never re-asked
# ═══════════════════════════════════════════════════════════════════════════


def test_re_offering_a_settled_item_does_not_reopen_it(store):
    """The property the source system cannot have, because it records nothing.

    A producer runs again, meets the same candidate, and offers it again. If that
    reopened the item, every run would re-ask every question a person has already
    answered, which is what happens today.
    """
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="tester")
    again = _offer_one(store)
    assert again.verdict is review.Verdict.ACCEPTED
    assert review.list_items(store).items == ()


def test_re_offering_an_open_item_refreshes_what_it_shows(store):
    """Still open, so the newest description of the candidate is the useful one."""
    item = _offer_one(store)
    refreshed = _offer_one(store, payload={"wanted": "track a", "found": "track a (2026 edit)"})
    assert refreshed.item_id == item.item_id
    assert refreshed.payload["found"] == "track a (2026 edit)"


def test_a_rejected_verdict_suppresses_the_item_until_it_is_explicitly_cleared(store):
    """The state the source system has no representation for at all."""
    item = _offer_one(store)
    rejected = review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="tester")
    assert rejected.suppressed

    # Suppressed means out of the way, not gone: deleting it would let the next
    # producer offer it again, which is the roll forward this replaces.
    assert review.list_items(store).items == ()
    assert [i.item_id for i in review.list_items(store, include_suppressed=True).items] == [
        item.item_id
    ]

    reopened = review.clear(store, item.item_id, actor="tester")
    assert reopened.verdict is None
    assert [i.item_id for i in review.list_items(store).items] == [item.item_id]


def test_a_second_verdict_on_a_settled_item_refuses_rather_than_overwriting(store):
    """Last writer wins is not the same property as a decision being recorded."""
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="first")
    with pytest.raises(CratekitError) as excinfo:
        review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="second")
    assert excinfo.value.cause.reason == "review-already-resolved"
    assert review.get(store, item.item_id).verdict is review.Verdict.REJECTED
    assert review.get(store, item.item_id).actor == "first"


def test_a_verdict_naming_a_candidate_the_item_never_offered_refuses(store):
    item = _offer_one(store)
    with pytest.raises(CratekitError) as excinfo:
        review.resolve(
            store, item.item_id, review.Verdict.ACCEPTED, option="opt-nowhere", actor="tester"
        )
    assert excinfo.value.cause.reason == "review-option-unknown"
    assert review.get(store, item.item_id).verdict is None


def test_clearing_an_item_that_was_never_resolved_changes_nothing(store):
    item = _offer_one(store)
    assert review.clear(store, item.item_id, actor="tester").verdict is None


# ── A verdict this build cannot read (P2: two layers, one answer) ────────────
#
# The queue is library scoped by KTD21, so two installations at different
# versions share one queue on the library volume. The Python reader degrades an
# unrecognized verdict to unresolved on purpose, and every SQL consumer used to
# ask the raw column whether it was NULL. The two disagreed, which is P2 exactly:
# the item was not listed, not counted, refused a resolution with a message that
# was factually false, and clear returned before touching the row. It was
# unreachable by every route this module offers.


def _a_verdict_from_a_newer_build(store, item_id: str, raw: str = "deferred") -> None:
    with store.immediate() as conn:
        conn.execute(
            "UPDATE review_items SET verdict = ? WHERE item_id = ?", (raw, item_id)
        )


def test_an_item_carrying_a_verdict_this_build_cannot_read_is_still_offered(store):
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)

    assert [held.item_id for held in review.list_items(store).items] == [item.item_id]
    assert review.count_unresolved(store) == 1
    assert review.get(store, item.item_id).verdict is None


def test_an_item_carrying_a_verdict_this_build_cannot_read_can_be_resolved(store):
    """Recoverable rather than frozen, and it is the reader's own direction.

    An unknown verdict must not become a decision, so the item is presented as a
    question again; answering it therefore has to be allowed to land.
    """
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)

    settled = review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="tester")
    assert settled.verdict is review.Verdict.REJECTED
    assert review.count_unresolved(store) == 0


def test_clearing_an_item_whose_verdict_this_build_cannot_read_clears_the_row(store):
    """``clear`` returned early on this item and never touched the column.

    It read the COERCED verdict, saw None, and concluded there was nothing to
    revoke, leaving the value that made the item unreachable exactly where it was.
    """
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)

    review.clear(store, item.item_id, actor="tester")
    row = store.conn.execute(
        "SELECT verdict FROM review_items WHERE item_id = ?", (item.item_id,)
    ).fetchone()
    assert row["verdict"] is None


def test_an_export_carries_a_verdict_this_build_cannot_read_rather_than_dropping_it(store):
    """The other end of the same disagreement, and it is a silent decision loss.

    An export that rendered the unreadable value as "no verdict" would hand the
    next installation a document saying nobody had decided, and that installation
    would insert the item as open. The decision would be gone with nobody told,
    which is the one thing this whole surface refuses to do.
    """
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)

    document = review.export_document(store)

    assert [entry["verdict"] for entry in document["items"]] == ["deferred"]


def test_an_import_does_not_overwrite_a_local_verdict_it_cannot_read(store):
    """The local decision is unreadable, not absent, so it is a conflict.

    Applying over it would discard a decision somebody made on a build that could
    represent it, with nobody told, which is the shape import exists to refuse.
    """
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)
    incoming = {
        "export": review.EXPORT_VERSION,
        "queue": "",
        "exported": "2026-01-01T00:00:00+00:00",
        "items": [{**item.to_json(), "verdict": str(review.Verdict.ACCEPTED)}],
    }

    result = review.import_document(store, incoming, actor="importer")

    assert result.conflicts == (item.item_id,)
    row = store.conn.execute(
        "SELECT verdict FROM review_items WHERE item_id = ?", (item.item_id,)
    ).fetchone()
    assert row["verdict"] == "deferred"


def test_quitting_partway_through_a_set_and_returning_presents_only_what_is_left(cfg, store):
    """The plan's second scenario, with a genuine reopen between the two halves."""
    offered = [_offer_one(store, key=f"{index:02d}") for index in range(6)]
    for item in offered[:2]:
        review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="tester")
    review.resolve(store, offered[2].item_id, review.Verdict.REJECTED, actor="tester")
    store.close()

    with review.open_store(cfg) as reopened:
        left = review.list_items(reopened).items
        assert [item.item_id for item in left] == [item.item_id for item in offered[3:]]
        # The prior verdicts are still there, which is the other half of the
        # scenario: re-entry must not have cost the work already done.
        assert review.get(reopened, offered[0].item_id).verdict is review.Verdict.ACCEPTED
        assert review.get(reopened, offered[2].item_id).verdict is review.Verdict.REJECTED
        assert review.count_unresolved(reopened) == 3


# ═══════════════════════════════════════════════════════════════════════════
# Part 5: batch resolution by predicate
# ═══════════════════════════════════════════════════════════════════════════


def _mixed_queue(store) -> dict[str, list[str]]:
    """Three kinds across two queues, so a predicate has something to miss."""
    made: dict[str, list[str]] = {}
    for index in range(3):
        item = _offer_one(store, key=f"v{index}", kind="version-difference")
        made.setdefault("version-difference", []).append(item.item_id)
    for index in range(2):
        item = _offer_one(store, key=f"c{index}", kind="clean-cut")
        made.setdefault("clean-cut", []).append(item.item_id)
    for index in range(2):
        item = _offer_one(
            store,
            key=f"g{index}",
            queue=review.Queue.GENRE,
            kind="proposed-genre",
            payload={"confidence": "low"},
        )
        made.setdefault("proposed-genre", []).append(item.item_id)
    return made


def test_batch_resolution_by_predicate_resolves_the_subset_and_leaves_the_rest(store):
    made = _mixed_queue(store)
    settled = review.resolve_where(
        store,
        review.Predicate(kind="version-difference"),
        review.Verdict.REJECTED,
        actor="tester",
    )
    assert sorted(item.item_id for item in settled) == sorted(made["version-difference"])
    still_open = {item.item_id for item in review.list_items(store, limit=None).items}
    assert still_open == set(made["clean-cut"]) | set(made["proposed-genre"])


def test_a_predicate_may_select_on_a_payload_field(store):
    _mixed_queue(store)
    settled = review.resolve_where(
        store,
        review.Predicate(queue=review.Queue.GENRE, payload_equals={"confidence": "low"}),
        review.Verdict.REJECTED,
        actor="tester",
    )
    assert len(settled) == 2


def test_a_predicate_typed_at_a_command_line_matches_a_payload_number(store):
    """A filter that matches nothing is indistinguishable from an empty queue.

    Everything arriving from a command line is text, and a producer that wrote a
    count as a number would otherwise be unmatchable: the predicate would be
    correct, the payload would be correct, and the sweep would settle nothing
    while reporting success.
    """
    _offer_one(store, key="numeric", payload={"attempts": 3})
    settled = review.resolve_where(
        store,
        review.Predicate(payload_equals={"attempts": "3"}),
        review.Verdict.REJECTED,
        actor="tester",
    )
    assert len(settled) == 1


def test_an_absent_payload_field_is_not_matched_by_the_text_none(store):
    """The one coercion that must NOT happen, or a typo selects the absent rows.

    "This field is not there" and "this field says None" are different facts.
    Matching them would mean a mistyped field name quietly selects every item
    that does not carry it, which is every item.
    """
    _offer_one(store, key="plain", payload={"wanted": "something"})
    settled = review.resolve_where(
        store,
        review.Predicate(payload_equals={"missing_field": "None"}),
        review.Verdict.REJECTED,
        actor="tester",
    )
    assert settled == ()
    assert review.count_unresolved(store) == 1


def test_a_batch_predicate_that_selects_everything_is_refused(store):
    _mixed_queue(store)
    with pytest.raises(CratekitError) as excinfo:
        review.resolve_where(store, review.Predicate(), review.Verdict.ACCEPTED, actor="tester")
    assert excinfo.value.cause.reason == "review-selection-invalid"
    assert review.count_unresolved(store) == 7


def test_batch_resolution_skips_what_is_already_settled_rather_than_refusing(store):
    made = _mixed_queue(store)
    review.resolve(store, made["version-difference"][0], review.Verdict.ACCEPTED, actor="first")
    settled = review.resolve_where(
        store,
        review.Predicate(kind="version-difference"),
        review.Verdict.REJECTED,
        actor="second",
    )
    assert sorted(i.item_id for i in settled) == sorted(made["version-difference"][1:])
    assert review.get(store, made["version-difference"][0]).actor == "first"


def test_a_second_process_sweeping_the_same_predicate_does_not_abort_the_first(cfg, store):
    """The skip above held inside ONE process and failed the moment two existed.

    ``resolve_where`` collected the identifiers and then called ``resolve`` on
    each with no handling for the race ``resolve`` is designed to raise, so the
    loser of any single item aborted the whole sweep AFTER it had already written
    every verdict before it. Observed: a sweep that settled two hundred items
    reported zero of them and exited 30, and the caller had no way to learn what
    had landed.

    Two REAL processes, because a second handle in one interpreter shares the
    connection's own serialization and can only prove that a value was kept.
    """
    outstanding = {_offer_one(store, key=f"{index:03d}").item_id for index in range(200)}
    store.close()

    running = [
        _start_another_process(
            "--output",
            "json",
            "review",
            "resolve",
            "--where",
            f"queue={review.Queue.VERSION_MATCH}",
            "--verdict",
            "rejected",
            "--actor",
            f"sweep-{index}",
        )
        for index in range(2)
    ]
    finished = [(process, *process.communicate()) for process in running]

    reported: list[str] = []
    for process, out, err in finished:
        assert process.returncode == int(ExitCode.OK), err or out
        reported.extend(row["id"] for row in json.loads(out)["data"]["items"])

    assert sorted(reported) == sorted(outstanding), (
        "a sweep wrote verdicts it did not report, so nobody can tell what landed"
    )
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 0


# ═══════════════════════════════════════════════════════════════════════════
# Part 6: paging, asserted by counting what is built rather than by reading SQL
# ═══════════════════════════════════════════════════════════════════════════


def _four_hundred(store) -> list[str]:
    return [_offer_one(store, key=f"{index:04d}").item_id for index in range(400)]


def test_four_hundred_items_page_without_loading_all_of_them_at_once(store, monkeypatch):
    """The plan's fifth scenario, asserted against the objects actually built.

    Counting rows CONVERTED is the only check that can tell real paging from
    reading everything and slicing the result, which is what the obvious
    implementation does and what a test asserting only the page size would pass.
    """
    made = _four_hundred(store)
    built = 0
    original = review._item_from_row

    def counting(row):
        nonlocal built
        built += 1
        return original(row)

    monkeypatch.setattr(review, "_item_from_row", counting)

    page = review.list_items(store, limit=25)
    assert [item.item_id for item in page.items] == made[:25]
    assert page.next_cursor is not None
    assert built <= 25 + 1, (
        f"{built} items were built to show 25; the queue is being read whole and "
        f"then sliced, which is not paging"
    )


def test_walking_every_page_visits_each_item_exactly_once(store):
    made = _four_hundred(store)
    seen: list[str] = []
    cursor = None
    while True:
        page = review.list_items(store, limit=37, after=cursor)
        seen.extend(item.item_id for item in page.items)
        if page.next_cursor is None:
            break
        cursor = page.next_cursor
    assert seen == made


def test_a_cursor_is_a_position_so_an_insert_mid_walk_does_not_shift_a_later_page(store):
    """Why the cursor is an ordinal and not an offset.

    Under offset paging, an item inserted while somebody is working through the
    queue pushes every later item back by one, and the next page silently skips
    whatever crossed the boundary. That is the failure a person experiences as
    "it never asked me about that one".
    """
    made = [_offer_one(store, key=f"{index:03d}").item_id for index in range(10)]
    first = review.list_items(store, limit=4)
    _offer_one(store, key="inserted-later")
    second = review.list_items(store, limit=4, after=first.next_cursor)
    assert [item.item_id for item in second.items] == made[4:8]


def test_the_walk_used_by_batch_work_holds_one_page_at_a_time(store, monkeypatch):
    """``iter_items`` is the shape export and batch resolution both use.

    If it read the queue whole, the paging above would be decorative: the two
    operations most likely to meet a large queue would both bypass it.
    """
    _four_hundred(store)
    alive = 0
    peak = 0
    original = review.list_items

    def watching(*args, **kwargs):
        nonlocal alive, peak
        page = original(*args, **kwargs)
        alive = len(page.items)
        peak = max(peak, alive)
        return page

    monkeypatch.setattr(review, "list_items", watching)
    assert sum(1 for _ in review.iter_items(store, page=20)) == 400
    assert peak <= 20


@pytest.mark.parametrize("limit", [0, -1, -2])
def test_a_page_size_that_is_not_a_positive_number_is_refused(store, limit):
    """Three different failures behind one bad argument, and none of them said so.

    Zero and minus one crashed with an index error out of the cursor arithmetic.
    Minus two and below silently omitted items and reported success, because a
    negative limit is UNBOUNDED in SQLite: those paths read the entire queue and
    then sliced it, which is the shape every test in this part exists to forbid.
    """
    _offer_one(store)
    with pytest.raises(CratekitError) as excinfo:
        review.list_items(store, limit=limit)
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_a_page_size_that_is_not_a_positive_number_is_refused_at_the_command_line(cfg, store):
    _offer_one(store)
    store.close()
    code, envelope, _ = _drive("review", "list", "--limit", "0")
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "review-selection-invalid"


# ═══════════════════════════════════════════════════════════════════════════
# Part 7: export and import, for anyone who genuinely wants a file
# ═══════════════════════════════════════════════════════════════════════════


def test_an_export_round_trips_into_an_empty_queue_with_its_verdicts(tmp_path, cfg, store):
    first = _offer_one(store, key="one")
    second = _offer_one(store, key="two")
    review.resolve(store, first.item_id, review.Verdict.REJECTED, actor="tester")
    document = review.export_document(store)
    assert {entry["id"] for entry in document["items"]} == {first.item_id, second.item_id}

    elsewhere = tmp_path / "other" / "queue.db"
    with review.open_store(cfg, path=elsewhere) as receiving:
        result = review.import_document(receiving, document, actor="importer")
        assert sorted(result.inserted) == sorted([first.item_id, second.item_id])
        assert review.get(receiving, first.item_id).verdict is review.Verdict.REJECTED
        assert review.get(receiving, second.item_id).verdict is None


def test_an_import_never_overwrites_a_local_verdict_and_reports_the_conflict(
    tmp_path, cfg, store
):
    """Two people resolving one item differently is a real situation.

    Picking a winner silently is how the losing decision disappears with nobody
    told, so the conflict is reported and the local record stands.
    """
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="local")
    incoming = {
        "export": review.EXPORT_VERSION,
        "queue": "",
        "exported": "2026-01-01T00:00:00+00:00",
        "items": [
            {
                **item.to_json(),
                "verdict": str(review.Verdict.REJECTED),
                "option": None,
                "actor": "remote",
            }
        ],
    }
    result = review.import_document(store, incoming, actor="importer")
    assert result.conflicts == (item.item_id,)
    assert review.get(store, item.item_id).verdict is review.Verdict.ACCEPTED
    assert review.get(store, item.item_id).actor == "local"


def test_an_export_written_by_another_version_refuses(store):
    with pytest.raises(CratekitError) as excinfo:
        review.import_document(store, {"export": 99, "items": []}, actor="importer")
    assert excinfo.value.cause.reason == "review-file-unusable"


def test_one_unapplicable_item_does_not_abort_the_import(tmp_path, cfg, store):
    """A partial import that stopped halfway would report nothing about the half.

    Two items the queue cannot take, for two different reasons, either side of a
    good one. Everything applicable applies, the other two are reported, and the
    caller can tell a person exactly which is which.
    """
    good = _offer_one(store, key="good").to_json()
    document = {
        "export": review.EXPORT_VERSION,
        "queue": "",
        "exported": "2026-01-01T00:00:00+00:00",
        "items": [
            # A verdict this build has no representation for. Dropping it
            # silently would discard a decision and look like a clean import.
            {**good, "id": "rv_unreadable", "verdict": "whatever-that-means"},
            {**good, "verdict": str(review.Verdict.ACCEPTED), "option": "opt-accept"},
            # A candidate the item never offered, which ``resolve`` refuses.
            {
                **good,
                "id": "rv_bad_option",
                "options": [],
                "verdict": str(review.Verdict.ACCEPTED),
                "option": "opt-nowhere",
            },
        ],
    }
    elsewhere = tmp_path / "receiving" / "queue.db"
    with review.open_store(cfg, path=elsewhere) as receiving:
        result = review.import_document(receiving, document, actor="importer")
        assert sorted(result.conflicts) == ["rv_bad_option", "rv_unreadable"]
        assert review.get(receiving, good["id"]).verdict is review.Verdict.ACCEPTED


@pytest.mark.parametrize(
    ("name", "broken"),
    [
        ("a payload that is not a mapping", {"payload": [1, 2, 3]}),
        ("an option with no identifier", {"options": [{"summary": "no identifier here"}]}),
        ("a queue nobody declared", {"queue": "invented"}),
        ("options that are not a list", {"options": 7}),
    ],
)
def test_a_malformed_item_is_reported_rather_than_raised_out_of_the_import(
    tmp_path, cfg, store, name, broken
):
    """An import is TOTAL, and its own docstring says so.

    Two of these escaped the refusal guard entirely, as a type error and a key
    error, and both aborted the loop AFTER earlier items had already been
    written. A caller cannot report what it applied when the call it made never
    returned, and re-running never succeeds because the good half is already in.
    """
    good = _offer_one(store, key="good").to_json()
    document = {
        "export": review.EXPORT_VERSION,
        "queue": "",
        "exported": "2026-01-01T00:00:00+00:00",
        "items": [
            {**good, "id": "rv_broken", **broken},
            {**good, "verdict": str(review.Verdict.ACCEPTED), "option": "opt-accept"},
        ],
    }
    elsewhere = tmp_path / "receiving" / "queue.db"
    with review.open_store(cfg, path=elsewhere) as receiving:
        result = review.import_document(receiving, document, actor="importer")
        assert result.conflicts == ("rv_broken",), name
        assert review.get(receiving, good["id"]).verdict is review.Verdict.ACCEPTED


def test_an_import_says_why_each_item_it_could_not_apply_was_not_applied(tmp_path, cfg, store):
    """A caller that reports every conflict as a disagreement is lying about most.

    "Already settled here and the export disagrees" is one of four reasons an
    item lands in this list, and the other three send a person somewhere else
    entirely.
    """
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="local")
    document = {
        "export": review.EXPORT_VERSION,
        "queue": "",
        "exported": "2026-01-01T00:00:00+00:00",
        "items": [
            {**item.to_json(), "verdict": str(review.Verdict.REJECTED), "actor": "remote"},
            {**item.to_json(), "id": "rv_unreadable", "verdict": "whatever-that-means"},
            {**item.to_json(), "id": "rv_broken", "payload": [1, 2, 3]},
        ],
    }

    result = review.import_document(store, document, actor="importer")

    assert set(result.conflicts) == {"rv_broken", "rv_unreadable", item.item_id}
    assert set(result.reasons) == set(result.conflicts), (
        "every conflict carries a reason, or the caller has to invent one"
    )
    assert len(set(result.reasons.values())) == 3, (
        f"three different failures collapsed into {set(result.reasons.values())}"
    )


def test_an_unresolved_cause_says_how_many_are_outstanding_and_what_to_do():
    """One sentence for "a person still has to decide", built in one place.

    Every producer that cannot proceed past open items reports it the same way,
    rather than each inventing its own wording, which is how the source system
    ended up with eleven prose variants of one instruction.
    """
    cause = review.unresolved_cause(4)
    assert cause.code is ExitCode.PENDING_HUMAN
    assert cause.detail["unresolved"] == 4
    assert cause.remediation.steps


# ═══════════════════════════════════════════════════════════════════════════
# Part 8: the decision stores, which share this shape and are revocable
# ═══════════════════════════════════════════════════════════════════════════


def test_the_decision_stores_are_the_two_the_state_inventory_declares(cfg):
    """DERIVED from the inventory, so a third store cannot appear undeclared.

    The name of this test quantifies over the inventory, and the constant it
    iterated was a literal pair spelled in the review module with a docstring
    saying it came from the inventory (P3). The inventory declares which entries
    are decision stores now, and this reads that declaration.
    """
    declared = tuple(sorted(entry.key for entry in config.STATE_FILES if entry.decision_store))
    assert review.DECISION_STORE_KEYS == declared, (
        "the module's list and the inventory's declaration disagree, so one of "
        "them is a copy that has drifted"
    )
    # R35's declines and R36's tombstones are the two the plan names. Asserted
    # against the DERIVED set rather than instead of it: a derivation that lost
    # both entries would otherwise pass this test by being vacuously equal.
    assert {"declines", "tombstones"} <= set(declared)
    for key in review.DECISION_STORE_KEYS:
        entry = config.state_file(key)
        assert entry.root is config.StateRoot.LIBRARY
        assert entry.snapshot is config.SnapshotRole.COUPLED, (
            f"{key} must roll back with the database, or a restore leaves a "
            f"suppression standing for a removal it undid"
        )
        assert review.DecisionStore(key, cfg).path == config.state_path(key, cfg)


def test_a_decline_suppresses_and_is_revocable(cfg):
    """R35's exact sentence: remembered, never offered again, until revoked."""
    declines = review.DecisionStore("declines", cfg)
    identity = {"device": 12, "inode": 3456}
    assert not declines.suppresses("removed-file", identity)

    recorded = declines.record(kind="removed-file", identity=identity, actor="tester")
    assert declines.suppresses("removed-file", identity)
    assert [d.suppression_id for d in declines.suppressions()] == [recorded.suppression_id]

    declines.revoke(recorded.suppression_id, actor="tester")
    assert not declines.suppresses("removed-file", identity)
    # Revoked, not forgotten: the record of the suppression having existed is
    # what makes the revocation reportable.
    assert declines.suppressions() == ()
    assert [d.suppression_id for d in declines.suppressions(include_revoked=True)] == [
        recorded.suppression_id
    ]


def test_recording_a_suppression_twice_changes_nothing(cfg):
    tombstones = review.DecisionStore("tombstones", cfg)
    identity = {"recording": "abc", "version": "original"}
    first = tombstones.record(kind="version", identity=identity, actor="tester")
    again = tombstones.record(kind="version", identity=identity, actor="somebody-else")
    assert again == first


def test_a_revoked_suppression_can_be_recorded_again(cfg):
    tombstones = review.DecisionStore("tombstones", cfg)
    identity = {"recording": "abc", "version": "original"}
    first = tombstones.record(kind="version", identity=identity, actor="tester")
    tombstones.revoke(first.suppression_id, actor="tester")
    assert tombstones.record(kind="version", identity=identity, actor="tester").suppressing


def test_the_two_stores_do_not_share_an_identifier_space(cfg):
    """A decline and a tombstone about the same thing are different decisions."""
    identity = {"recording": "abc"}
    assert review.suppression_id_for("declines", "version", identity) != (
        review.suppression_id_for("tombstones", "version", identity)
    )


def test_a_suppression_identifier_is_not_mistakable_for_a_review_item(cfg):
    assert review.suppression_id_for("declines", "k", {"a": 1}).startswith(
        review.SUPPRESSION_ID_PREFIX
    )
    assert review.item_id_for(review.Queue.DELETION, "k", {"a": 1}).startswith(review.ID_PREFIX)


def test_an_unreadable_decision_store_refuses_rather_than_reading_as_empty(cfg):
    """A tolerant read on a path that governs an action fails OPEN.

    Reading an unreadable suppression list as empty un-suppresses everything in
    it, silently, and the next acquisition re-acquires exactly what somebody
    removed on purpose. That is U8's lesson about the session gate, one store
    along.
    """
    declines = review.DecisionStore("declines", cfg)
    declines.record(kind="removed-file", identity={"inode": 1}, actor="tester")
    declines.path.write_text("{not json at all")
    with pytest.raises(CratekitError) as excinfo:
        declines.suppresses("removed-file", {"inode": 1})
    assert excinfo.value.cause.reason == "review-file-unusable"


#: Documents that are perfectly good JSON and are not this store. The refusal
#: used to cover only the case where ``json.loads`` itself raised, so every one
#: of these fell through to an empty read: the store reported that it suppressed
#: nothing, and the next write then replaced the file with what it had read.
STRUCTURALLY_WRONG_STORES = {
    "a top level list": "[]",
    "a top level scalar": "7",
    "a version this build does not know": json.dumps(
        {"version": 99, "store": "declines", "decisions": []}
    ),
    "no version at all": json.dumps({"store": "declines", "decisions": []}),
    "records under another version's key": json.dumps(
        {"version": 1, "store": "declines", "records": []}
    ),
    "decisions present and null": json.dumps(
        {"version": 1, "store": "declines", "decisions": None}
    ),
    "decisions that are not a list": json.dumps(
        {"version": 1, "store": "declines", "decisions": {"dc_one": {}}}
    ),
    "another store's document": json.dumps(
        {"version": 1, "store": "tombstones", "decisions": []}
    ),
    "a record whose identifier key was renamed": json.dumps(
        {"version": 1, "store": "declines", "decisions": [{"identifier": "dc_one"}]}
    ),
    "a record whose payload is not a mapping": json.dumps(
        {"version": 1, "store": "declines", "decisions": [{"id": "dc_one", "payload": 5}]}
    ),
    "a record that is not a mapping": json.dumps(
        {"version": 1, "store": "declines", "decisions": ["dc_one"]}
    ),
}


@pytest.mark.parametrize("shape", sorted(STRUCTURALLY_WRONG_STORES))
def test_a_store_this_build_cannot_positively_recognize_refuses(cfg, shape):
    """Refusal is the ONLY alternative to a correct read.

    Everything here parses as JSON and none of it is this store's document, so
    the reader that only caught a parse error returned an empty mapping for every
    one of them. Fail open plus a name that says the opposite.
    """
    declines = review.DecisionStore("declines", cfg)
    declines.path.parent.mkdir(parents=True, exist_ok=True)
    declines.path.write_text(STRUCTURALLY_WRONG_STORES[shape])
    with pytest.raises(CratekitError) as excinfo:
        declines.suppressions()
    assert excinfo.value.cause.reason == "review-file-unusable"


@pytest.mark.parametrize("shape", sorted(STRUCTURALLY_WRONG_STORES))
def test_a_store_this_build_cannot_read_is_never_overwritten_by_the_next_write(cfg, shape):
    """The half that turns a fail open into permanent data loss.

    The empty read was fed straight back into the writer, so ONE further record
    deleted every prior decline from the disk, in the store whose own docstring
    says treating it as empty would re-acquire exactly what somebody removed on
    purpose.
    """
    declines = review.DecisionStore("declines", cfg)
    declines.path.parent.mkdir(parents=True, exist_ok=True)
    declines.path.write_text(STRUCTURALLY_WRONG_STORES[shape])
    before = declines.path.read_text()

    with pytest.raises(CratekitError):
        declines.record(kind="removed-file", identity={"inode": 1}, actor="tester")
    assert declines.path.read_text() == before

    with pytest.raises(CratekitError):
        declines.revoke("dc_one", actor="tester")
    assert declines.path.read_text() == before


def test_a_record_whose_payload_is_not_a_mapping_refuses_rather_than_raising(cfg):
    """``suppresses`` is asked once per candidate by an acquisition pass.

    A type error out of it is not a refusal anything up the stack can render, and
    the pass that was consulting the store dies rather than reporting.
    """
    declines = review.DecisionStore("declines", cfg)
    declines.path.parent.mkdir(parents=True, exist_ok=True)
    declines.path.write_text(
        json.dumps(
            {
                "version": 1,
                "store": "declines",
                "decisions": [{"id": "dc_one", "payload": [1, 2, 3]}],
            }
        )
    )
    with pytest.raises(CratekitError) as excinfo:
        declines.suppresses("removed-file", {"inode": 1})
    assert excinfo.value.cause.reason == "review-file-unusable"


# ── Two processes, which is the case a document store has to survive ─────────

_RECORD_IN_A_CHILD = """
import sys

from cratekit.core import config, review

key, worker, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
store = review.DecisionStore(key, config.load())
for index in range(count):
    store.record(
        kind="version",
        identity={"worker": worker, "index": index},
        actor="worker-" + str(worker),
    )
"""

_REVOKE_IN_A_CHILD = """
import sys

from cratekit.core import config, review

key, worker, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
store = review.DecisionStore(key, config.load())
for index in range(count):
    store.revoke(
        review.suppression_id_for(key, "version", {"worker": worker, "index": index}),
        actor="worker-" + str(worker),
    )
"""

#: Eight writers, twenty five decisions each. The numbers are the reviewer's:
#: they produced 78 records on disk out of 200 expected, with every call
#: returning a record that reported success.
WORKERS = 8
PER_WORKER = 25


def test_every_decision_recorded_by_eight_processes_at_once_survives(cfg):
    """A lost record re-offers a declined file and re-acquires a tombstoned version.

    ``atomic_write_bytes`` makes the RENAME atomic; it does nothing for the read
    then write around it. Two processes both read the same document, both add
    their own record, and the second rename discards the first one's, while the
    call that lost returns a record saying it worked.

    The queue next door survives exactly this by taking the write lock up front,
    and the config module already ships a lock whose docstring names this hazard.
    """
    _in_separate_processes(
        _RECORD_IN_A_CHILD,
        workers=WORKERS,
        arguments=lambda worker: ("tombstones", worker, PER_WORKER),
    )
    held = review.DecisionStore("tombstones", cfg).suppressions()
    assert len(held) == WORKERS * PER_WORKER, (
        f"{len(held)} of {WORKERS * PER_WORKER} decisions reached the disk; the "
        f"rest were reported as recorded and are gone"
    )


def test_every_revocation_by_eight_processes_at_once_survives(cfg):
    """A lost revocation leaves a suppression standing forever.

    Which is worse than losing a record: nothing ever offers the thing again, so
    nobody finds out.
    """
    _in_separate_processes(
        _RECORD_IN_A_CHILD,
        workers=WORKERS,
        arguments=lambda worker: ("declines", worker, PER_WORKER),
    )
    _in_separate_processes(
        _REVOKE_IN_A_CHILD,
        workers=WORKERS,
        arguments=lambda worker: ("declines", worker, PER_WORKER),
    )
    declines = review.DecisionStore("declines", cfg)
    assert declines.suppressions() == ()
    assert len(declines.suppressions(include_revoked=True)) == WORKERS * PER_WORKER


def test_a_mode_the_filesystem_refuses_is_reported_rather_than_swallowed(cfg, monkeypatch):
    """Absence is normal for a sidecar. A refusal is not, and it was tolerated.

    Swallowing every operating system error meant a chmod the filesystem declined
    left a world readable queue of everything a person has decided about their
    library, with nothing raised and nothing logged, on exactly the platforms
    where the mode is the only protection there is.
    """
    real_chmod = os.chmod
    target = review.queue_path(cfg)

    def refusing(path, mode, *args, **kwargs):
        if str(path).startswith(str(target)):
            raise PermissionError(1, "operation not permitted")
        return real_chmod(path, mode, *args, **kwargs)

    monkeypatch.setattr(os, "chmod", refusing)
    with pytest.raises(CratekitError) as excinfo:
        review.open_store(cfg)
    assert excinfo.value.cause.reason == "review-file-unusable"


@pytest.fixture
def permissive_umask():
    """Run the body under umask 000, then put the process back.

    A test that does not manipulate the umask cannot see this class of defect at
    all: on a developer machine the umask is usually 022 and a plain create lands
    0644, which looks fine until somebody with a laxer umask runs the same code.
    """
    previous = os.umask(0o000)
    try:
        yield
    finally:
        os.umask(previous)


def test_every_path_this_unit_creates_is_private_under_any_umask(permissive_umask, cfg):
    """P1 over EVERYTHING this unit writes, derived by walking rather than listed.

    Three roots, because this unit now writes in three places: the queue and its
    sidecars, the decision store documents, and the sibling locks that serialize
    them. The lock is the one that needed saying: it is created by ``os.open``
    with an explicit mode, which the umask still masks, and 0600 carries no group
    or other bits for a mask to add, so masking can only leave it at or below the
    mode asked for.
    """
    if not hasattr(os, "chmod"):  # pragma: no cover - platforms without POSIX modes
        return
    with review.open_store(cfg) as store:
        _offer_one(store)
    declines = review.DecisionStore("declines", cfg)
    recorded = declines.record(kind="removed-file", identity={"inode": 1}, actor="tester")
    declines.revoke(recorded.suppression_id, actor="tester")

    roots = [
        config.state_path("review_queue", cfg),
        declines.path.parent,
        declines.lock_path.parent,
    ]
    checked = 0
    for root in roots:
        for path in [root, *root.rglob("*")]:
            mode = path.stat().st_mode & 0o777
            expected = config.PRIVATE_DIR_MODE if path.is_dir() else config.PRIVATE_FILE_MODE
            assert mode == expected, f"{path} landed {oct(mode)}"
            checked += 1
    assert checked >= 6, "the walk found less than this unit is known to write"


def test_a_decision_store_lands_owner_only_whatever_the_umask(cfg):
    declines = review.DecisionStore("declines", cfg)
    declines.record(kind="removed-file", identity={"inode": 1}, actor="tester")
    if hasattr(os, "chmod"):
        assert declines.path.stat().st_mode & 0o777 == config.PRIVATE_FILE_MODE
        assert declines.path.parent.stat().st_mode & 0o777 == config.PRIVATE_DIR_MODE


def test_a_store_the_inventory_does_not_declare_is_refused(cfg):
    with pytest.raises(CratekitError) as excinfo:
        review.DecisionStore("whatever", cfg)
    assert excinfo.value.cause.reason == "review-queue-undeclared"


# ═══════════════════════════════════════════════════════════════════════════
# Part 9: the unit's verification
# ═══════════════════════════════════════════════════════════════════════════


def test_a_match_producing_all_three_states_round_trips_across_two_processes(cfg, store):
    """The unit's stated verification, end to end.

    R11 resolves each track to matched, needs review, or missing. Only the middle
    state is an adjudication surface: the other two are the match result, and the
    assertion that they never reach the queue is as load bearing as the assertion
    that the middle one does. A person then answers half the queue, everything
    restarts, and a second process answers the rest.
    """
    matched = [{"row": "1", "state": "matched"}]
    needs_review = [{"row": "2", "state": "needs_review"}, {"row": "3", "state": "needs_review"}]
    missing = [{"row": "4", "state": "missing"}]

    offered = [
        review.offer(
            store,
            queue=review.Queue.VERSION_MATCH,
            kind="version-difference",
            identity={"source": "list-9", "row": row["row"]},
            payload=dict(row),
            options=(review.Option(option_id="opt-same", summary="the same recording"),),
            handler_key="match.run",
        )
        for row in needs_review
    ]
    assert review.count_unresolved(store) == len(needs_review)

    # The two states that are OUTPUTS never become queue items. Asserted by
    # identity rather than by count, so an item smuggled in under another kind
    # would still be caught.
    for row in matched + missing:
        absent = review.item_id_for(
            review.Queue.VERSION_MATCH, "version-difference", {"source": "list-9", "row": row["row"]}
        )
        with pytest.raises(CratekitError):
            review.get(store, absent)

    # A person answers the first one, then everything stops.
    review.resolve(
        store, offered[0].item_id, review.Verdict.ACCEPTED, option="opt-same", actor="person"
    )
    store.close()

    # A restart, then a genuinely separate process answers the rest.
    done = _in_another_process(
        "--output", "json", "review", "resolve", offered[1].item_id, "--verdict", "rejected"
    )
    assert done.returncode == 0, done.stderr

    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 0
        assert review.get(reopened, offered[0].item_id).verdict is review.Verdict.ACCEPTED
        assert review.get(reopened, offered[1].item_id).verdict is review.Verdict.REJECTED
        assert review.get(reopened, offered[1].item_id).suppressed


# ═══════════════════════════════════════════════════════════════════════════
# Part 10: the verbs, and the structured output R32 requires of them
# ═══════════════════════════════════════════════════════════════════════════


def test_the_review_set_output_validates_against_its_committed_schema(cfg, store):
    """The plan's sixth scenario, checked against the SHIPPED contract.

    Two validations rather than one. ``envelope_problems`` is the product's own
    check, and the committed schema document is what a consumer outside this
    repository validates against; a payload satisfying one and not the other
    would mean the shipped contract and the running code disagree.
    """
    _offer_one(store)
    store.close()

    code, envelope, _ = _drive("review", "list")
    assert code == int(ExitCode.OK)
    assert output.envelope_problems(envelope) == [], envelope
    assert envelope["schema"] == "review_set/1"

    declared = json.loads((SCHEMA_DIR / "review_set.v1.json").read_text())
    payload = envelope["data"]
    assert sorted(payload) == declared["required"]
    assert declared["additionalProperties"] is False
    assert payload["unresolved"] == 1
    assert payload["items"][0]["kind"] == "version-difference"


def test_listing_shows_what_is_outstanding_and_not_what_is_settled(cfg, store):
    open_item = _offer_one(store, key="open")
    settled = _offer_one(store, key="settled")
    review.resolve(store, settled.item_id, review.Verdict.ACCEPTED, actor="tester")
    store.close()

    _, outstanding, _ = _drive("review", "list")
    assert [row["id"] for row in outstanding["data"]["items"]] == [open_item.item_id]
    assert outstanding["data"]["unresolved"] == 1

    _, everything, _ = _drive("review", "list", "--all")
    assert {row["id"] for row in everything["data"]["items"]} == {
        open_item.item_id,
        settled.item_id,
    }
    # The backlog is a query over the queue, never the length of the page. A
    # listing that showed two items and called two the backlog would tell a
    # person they have twice the work left.
    assert everything["data"]["unresolved"] == 1


def test_an_empty_queue_is_a_no_op_rather_than_a_failure(cfg, store):
    store.close()
    code, envelope, _ = _drive("review", "list")
    assert code == int(ExitCode.OK)
    assert envelope["outcome"] == "no_op"


def test_showing_one_item_carries_its_whole_record(cfg, store):
    item = _offer_one(store)
    store.close()
    code, envelope, _ = _drive("review", "show", item.item_id)
    assert code == int(ExitCode.OK)
    shown = envelope["data"]["items"][0]
    assert shown["payload"] == dict(item.payload)
    assert [option["option_id"] for option in shown["options"]] == ["opt-accept", "opt-other"]
    assert envelope["data"]["queue"] == str(review.Queue.VERSION_MATCH)


def test_an_unknown_identifier_refuses_with_a_code_from_the_vocabulary(cfg, store):
    store.close()
    code, envelope, _ = _drive("review", "show", "rv_nothing")
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "review-item-unknown"


def test_a_batch_resolution_from_the_command_line_settles_only_the_subset(cfg, store):
    made = _mixed_queue(store)
    store.close()

    code, envelope, _ = _drive(
        "review", "resolve", "--where", "kind=version-difference", "--verdict", "rejected"
    )
    assert code == int(ExitCode.OK)
    assert {row["id"] for row in envelope["data"]["items"]} == set(made["version-difference"])
    assert envelope["data"]["unresolved"] == 4


def test_a_predicate_on_a_payload_field_is_reachable_from_the_command_line(cfg, store):
    _mixed_queue(store)
    store.close()
    code, envelope, _ = _drive(
        "review", "resolve",
        "--where", "queue=genre",
        "--where", "payload.confidence=low",
        "--verdict", "rejected",
    )
    assert code == int(ExitCode.OK)
    assert len(envelope["data"]["items"]) == 2


def test_a_resolution_naming_both_an_item_and_a_predicate_refuses(cfg, store):
    item = _offer_one(store)
    store.close()
    code, envelope, _ = _drive(
        "review", "resolve", item.item_id, "--where", "kind=x", "--verdict", "accepted"
    )
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "review-selection-invalid"


def test_a_batch_resolution_naming_a_candidate_refuses_rather_than_dropping_it(cfg, store):
    """Each item offers its own candidates, so one identifier cannot span a subset.

    Accepting the argument and quietly ignoring it would leave a person believing
    a choice was recorded that never was.
    """
    _mixed_queue(store)
    store.close()
    code, envelope, _ = _drive(
        "review", "resolve",
        "--where", "kind=version-difference",
        "--verdict", "accepted",
        "--option", "opt-accept",
    )
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "review-selection-invalid"
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 7


def test_a_resolution_naming_neither_refuses_rather_than_answering_everything(cfg, store):
    _offer_one(store)
    store.close()
    code, envelope, _ = _drive("review", "resolve", "--verdict", "accepted")
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "review-selection-invalid"
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 1


def test_a_malformed_predicate_is_refused_rather_than_matching_nothing(cfg, store):
    """A filter that silently matches nothing looks exactly like an empty queue."""
    _offer_one(store)
    store.close()
    for bad in ("kind", "nonsense=1"):
        code, envelope, _ = _drive("review", "resolve", "--where", bad, "--verdict", "accepted")
        assert code == int(ExitCode.PRECONDITION), bad
        assert envelope["cause"]["reason"] == "review-selection-invalid"


def test_clearing_from_the_command_line_puts_a_rejected_item_back(cfg, store):
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="tester")
    store.close()

    code, envelope, _ = _drive("review", "clear", item.item_id, "--actor", "somebody")
    assert code == int(ExitCode.OK)
    assert envelope["data"]["items"][0]["verdict"] is None
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 1


def test_an_export_and_an_import_round_trip_through_the_command_line(
    tmp_path, cfg, store, monkeypatch
):
    first = _offer_one(store, key="one")
    second = _offer_one(store, key="two")
    review.resolve(store, first.item_id, review.Verdict.REJECTED, actor="tester")
    store.close()

    target = tmp_path / "exports" / "queue.json"
    code, envelope, _ = _drive("review", "export", str(target))
    assert code == int(ExitCode.OK)
    assert target.exists()
    assert {row["id"] for row in envelope["data"]["items"]} == {first.item_id, second.item_id}

    # A file is a transport, not an editing surface: versioned JSON rather than
    # the comma separated shape whose column breaks silently change a verdict.
    document = json.loads(target.read_text())
    assert document["export"] == review.EXPORT_VERSION

    # A SECOND library, reached the way a relocation is actually reached: the
    # root moves and the configuration follows it. Building a second Config by
    # hand would not work here and the reason is worth knowing, because it is the
    # property that keeps this suite off a real library: an environment override
    # relocates a configured root, so a hand built Config naming another
    # directory resolves straight back to this one.
    elsewhere = tmp_path / "second-library"
    (elsewhere / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(elsewhere))
    config.reset_cache()
    moved = config.load()
    assert moved.library.root == elsewhere

    code, imported, _ = _drive("review", "import", str(target))
    assert code == int(ExitCode.OK)
    assert {row["id"] for row in imported["data"]["items"]} == {first.item_id, second.item_id}
    with review.open_store(moved) as receiving:
        assert review.get(receiving, first.item_id).verdict is review.Verdict.REJECTED
        assert review.count_unresolved(receiving) == 1


def test_an_export_never_replaces_a_file_that_is_already_there(tmp_path, cfg, store):
    """Refusing is what keeps this verb out of the destructive class entirely."""
    _offer_one(store)
    store.close()
    target = tmp_path / "already-here.json"
    target.write_text("something somebody wanted")

    code, envelope, _ = _drive("review", "export", str(target))
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "review-file-unusable"
    assert target.read_text() == "something somebody wanted"


def test_an_import_reports_a_conflict_as_a_warning_and_keeps_the_local_verdict(
    tmp_path, cfg, store
):
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="local")
    store.close()

    target = tmp_path / "incoming.json"
    target.write_text(
        json.dumps(
            {
                "export": review.EXPORT_VERSION,
                "queue": "",
                "exported": "2026-01-01T00:00:00+00:00",
                "items": [
                    {
                        **item.to_json(),
                        "verdict": str(review.Verdict.REJECTED),
                        "option": None,
                        "actor": "remote",
                    }
                ],
            }
        )
    )

    code, envelope, _ = _drive("review", "import", str(target))
    assert code == int(ExitCode.OK)
    assert [warning["code"] for warning in envelope["warnings"]] == ["review-verdict-conflict"]
    with review.open_store(cfg) as reopened:
        assert review.get(reopened, item.item_id).actor == "local"


def test_an_import_that_applies_one_verdict_and_cannot_apply_another_reports_both(
    tmp_path, cfg, store
):
    """The verb wrote verdicts and then reported failure, which is the worst pair.

    Observed: a document carrying one applicable verdict plus one item this build
    cannot read applied the good verdict, then exited 30 with review-item-unknown
    and a remediation telling the user to list the queue and take an identifier
    from it. Zero warnings, no account of what landed, and re-running never
    succeeded because the good half was already in. The cause was a report step
    that looked every touched identifier up locally, including the conflicts,
    which need not exist here at all.
    """
    item = _offer_one(store)
    store.close()
    target = tmp_path / "incoming.json"
    target.write_text(
        json.dumps(
            {
                "export": review.EXPORT_VERSION,
                "queue": "",
                "exported": "2026-01-01T00:00:00+00:00",
                "items": [
                    {**item.to_json(), "verdict": str(review.Verdict.ACCEPTED)},
                    {
                        **item.to_json(),
                        "id": "rv_from_a_newer_build",
                        "verdict": "whatever-that-means",
                    },
                ],
            }
        )
    )

    code, envelope, _ = _drive("review", "import", str(target))

    assert code == int(ExitCode.OK)
    assert [row["id"] for row in envelope["data"]["items"]] == [item.item_id], (
        "the verb reports what it applied, and an identifier it never took in is "
        "not something it applied"
    )
    assert [warning["code"] for warning in envelope["warnings"]] == [
        "review-verdict-conflict"
    ]
    assert "rv_from_a_newer_build" in envelope["warnings"][0]["message"]
    with review.open_store(cfg) as reopened:
        assert review.get(reopened, item.item_id).verdict is review.Verdict.ACCEPTED

    # Re-running is the move a person makes after a failure, and it used to be
    # the move that could never succeed.
    again, second, _ = _drive("review", "import", str(target))
    assert again == int(ExitCode.OK)


def test_an_import_lists_an_item_it_inserted_and_could_not_settle_exactly_once(
    tmp_path, cfg, store
):
    """Both facts are true, and one of them is not a second item.

    The row WAS inserted and the verdict WAS not applied, so the identifier is in
    both lists, and concatenating the lists showed a person two items where the
    queue holds one.
    """
    good = _offer_one(store, key="good").to_json()
    store.close()
    target = tmp_path / "incoming.json"
    target.write_text(
        json.dumps(
            {
                "export": review.EXPORT_VERSION,
                "queue": "",
                "exported": "2026-01-01T00:00:00+00:00",
                "items": [
                    {
                        **good,
                        "id": "rv_no_such_option",
                        "options": [],
                        "verdict": str(review.Verdict.ACCEPTED),
                        "option": "opt-nowhere",
                    }
                ],
            }
        )
    )

    code, envelope, _ = _drive("review", "import", str(target))

    assert code == int(ExitCode.OK)
    assert [row["id"] for row in envelope["data"]["items"]] == ["rv_no_such_option"]


def test_an_import_carrying_a_malformed_item_does_not_fail_as_an_internal_error(
    tmp_path, cfg, store
):
    """A payload that is a list of numbers used to leave as a type error.

    An internal error at the process boundary is a bare status with no cause and
    no remediation, which is the one shape the exit-code vocabulary exists to
    make impossible.
    """
    good = _offer_one(store, key="good").to_json()
    store.close()
    target = tmp_path / "incoming.json"
    target.write_text(
        json.dumps(
            {
                "export": review.EXPORT_VERSION,
                "queue": "",
                "exported": "2026-01-01T00:00:00+00:00",
                "items": [
                    {**good, "id": "rv_broken", "payload": [1, 2, 3]},
                    {**good, "verdict": str(review.Verdict.REJECTED)},
                ],
            }
        )
    )

    code, envelope, _ = _drive("review", "import", str(target))

    assert code == int(ExitCode.OK)
    assert [warning["code"] for warning in envelope["warnings"]] == [
        "review-verdict-conflict"
    ]
    with review.open_store(cfg) as reopened:
        assert review.get(reopened, good["id"]).verdict is review.Verdict.REJECTED


def test_every_reason_an_import_can_report_has_a_sentence_a_person_can_act_on():
    """DERIVED by introspecting the module, so a fifth reason cannot arrive mute.

    The verb reported all four as "already settled here and the export
    disagrees", which is true of one of them. The others send a person to a
    different place entirely: re-export from the build that wrote the file,
    repair the file, or run it again.
    """
    from cratekit.cli import review as verbs

    declared = {
        value
        for name, value in vars(review).items()
        if name.startswith("CONFLICT_") and isinstance(value, str)
    }
    assert declared, "the reasons are no longer discoverable by introspection"
    missing = declared - set(verbs.CONFLICT_SENTENCES)
    assert not missing, f"conflict reasons with no sentence for the user: {sorted(missing)}"
    assert set(verbs.CONFLICT_SENTENCES) == declared, (
        f"sentences for reasons the core cannot report: "
        f"{sorted(set(verbs.CONFLICT_SENTENCES) - declared)}"
    )


def test_an_import_of_something_that_is_not_an_export_refuses(tmp_path, cfg, store):
    store.close()
    target = tmp_path / "not-an-export.json"
    target.write_text("[]")
    code, envelope, _ = _drive("review", "import", str(target))
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "review-file-unusable"


def test_an_import_of_a_file_that_is_not_there_refuses_by_name(tmp_path, cfg, store):
    store.close()
    code, envelope, _ = _drive("review", "import", str(tmp_path / "absent.json"))
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "review-file-unusable"


# NOTE ON WHAT IS DELIBERATELY NOT HERE. There is no per module assertion that
# the review verbs never read standard input. R33 needs that property and
# ``tests/test_cli_contract.py`` already asserts it over EVERY module this
# repository authors, derived by walking the package. A narrower copy here would
# cover strictly less and would be the second opinion that eventually disagrees.


# ═══════════════════════════════════════════════════════════════════════════
# Part 11: what this unit settled that a LATER unit owes (P5)
# ═══════════════════════════════════════════════════════════════════════════
#
# Every guard below is gated on the unit that lands the package it walks, so each
# is a countdown rather than a wish in a docstring. Each walks the syntax tree for
# a call that resolves to THIS module through the import graph, rather than for an
# attribute of the right name.
#
# WHY THE BINDING MATTERS, stated because this section shipped without it. A guard
# that looks for a call to something spelled ``offer`` is satisfied by any object
# in the language with a method of that name. A reviewer wrote a module that hand
# edits a gate column in a comma separated file, never touches the queue, and
# passed all three assertions this section used to make: one unrelated
# ``_Ranking.offer`` call and one dead assignment of the queue constant were
# enough. The same walk failed in the other direction too, on correct code written
# as ``from cratekit.core.review import offer``, and P7 says a guard that fires on
# correct code is a guard somebody routes around. Both directions have fixtures
# below, and the fixtures run on every suite run rather than on the day the unit
# lands.


# ── The fixtures. One evasion, and correct code in both import shapes ────────

#: The reviewer's evasion, kept verbatim in shape: it adjudicates nothing, hand
#: edits the exact comma separated file R12 replaces, hides the writer behind an
#: aliased import, and satisfies a name matching countdown anyway.
EVASION_SOURCE = '''
"""A module that answers a name matching countdown and adjudicates nothing."""

import csv as spreadsheet

from cratekit.core import review

_PLANNED_QUEUE = review.Queue.VERSION_MATCH


class _Ranking:
    def offer(self, candidate):
        return candidate


def run(rows, handle):
    ranking = _Ranking()
    writer = spreadsheet.DictWriter(handle, ["wanted", "found", "gate"])
    for row in rows:
        writer.writerow({**row, "gate": ranking.offer(row)["found"]})
'''

#: Correct code, module import shape.
CORRECT_OFFER_MODULE_IMPORT = '''
from cratekit.core import review


def run(store, needing_review):
    for candidate in needing_review:
        review.offer(
            store,
            queue=review.Queue.VERSION_MATCH,
            kind="version-difference",
            identity=candidate.identity,
            payload=candidate.payload,
        )
'''

#: Correct code, symbol import shape, with the queue held in a module constant.
#: This is the shape the previous walk could not see at all.
CORRECT_OFFER_SYMBOL_IMPORT = '''
from cratekit.core.review import Queue, offer

QUEUE = Queue.VERSION_MATCH


def run(store, needing_review):
    for candidate in needing_review:
        offer(
            store,
            queue=QUEUE,
            kind="version-difference",
            identity=candidate.identity,
            payload=candidate.payload,
        )
'''

#: Correct code holding a decision store on a field, which is the ordinary shape.
CORRECT_DECISION_STORE = '''
from cratekit.core import review


class DeletionPass:
    def __init__(self, cfg):
        self.declines = review.DecisionStore("declines", cfg)

    def decline(self, identity):
        self.declines.record(kind="removed-file", identity=identity, actor="cli")

    def undo(self, suppression_id):
        self.declines.revoke(suppression_id, actor="cli")
'''

#: Correct code reaching the store through a small helper, one hop further out.
CORRECT_DECISION_STORE_VIA_HELPER = '''
from cratekit.core.review import DecisionStore


def _tombstones(cfg):
    return DecisionStore("tombstones", cfg)


def run(cfg, identity, suppression_id):
    store = _tombstones(cfg)
    store.record(kind="version", identity=identity, actor="cli")
    store.revoke(suppression_id, actor="cli")
'''

#: A deletion pass keeping its own ledger. It satisfies "remembered" and fails
#: "until the decline is revoked", which is exactly what the countdown forbids.
EVASIVE_DECISION_STORE = '''
class _Ledger:
    def record(self, row):
        ...

    def revoke(self, row):
        ...


def run(rows):
    ledger = _Ledger()
    for row in rows:
        ledger.record(row)
        ledger.revoke(row)
'''


def test_the_countdown_bites_the_evasion_that_satisfied_the_name_match():
    """P7's first half, run against the thing the guard exists to catch."""
    assert not calls_review(EVASION_SOURCE, "offer"), (
        "an unrelated method called 'offer' still answers for the review queue"
    )
    assert not offers_into(EVASION_SOURCE, "Queue.VERSION_MATCH"), (
        "an assignment of the queue constant that reaches no call still counts "
        "as offering into it"
    )
    assert constructs_a_csv_writer(EVASION_SOURCE), (
        "a comma separated writer behind an aliased import is invisible to the "
        "guard, which is one keyword away from switching it off"
    )
    assert not methods_on_review_construction(EVASIVE_DECISION_STORE, "DecisionStore"), (
        "a private ledger with methods named record and revoke answers for the "
        "decision stores, so R35's revocability is unenforced"
    )


@pytest.mark.parametrize(
    "source", [CORRECT_OFFER_MODULE_IMPORT, CORRECT_OFFER_SYMBOL_IMPORT]
)
def test_the_countdown_stays_quiet_on_correct_code_in_either_import_shape(source):
    """P7's second half, which is the half that was skipped.

    A guard that fires on correct code trains people to route around it, and the
    symbol import shape is not exotic: it is what a module offering into one
    queue writes.
    """
    assert calls_review(source, "offer")
    assert offers_into(source, "Queue.VERSION_MATCH")
    assert not constructs_a_csv_writer(source)


@pytest.mark.parametrize(
    "source", [CORRECT_DECISION_STORE, CORRECT_DECISION_STORE_VIA_HELPER]
)
def test_the_decision_store_countdown_stays_quiet_on_correct_code(source):
    assert methods_on_review_construction(source, "DecisionStore") >= {"record", "revoke"}


# ── The countdowns themselves ────────────────────────────────────────────────

#: Every adjudication surface this unit declared with NO legacy file, and the
#: pending key of the unit that owes it a producer. A ported surface has a file in
#: the source tree that a porting unit must dispose of, and ``SURFACES`` already
#: records that disposition. A NEW surface has nothing in the source tree at all,
#: so a countdown is the only thing that makes it exist (P5).
NEW_SURFACE_OWED_BY: dict[str, str] = {
    review.Queue.DUPLICATES: "cratekit.modules.reports",
    review.Queue.DELETION: "cratekit.deletion.cli",
    review.Queue.ADOPTION: "cratekit.adopt",
    review.Queue.PATH_REPAIR: "cratekit.intake",
}


def test_every_new_adjudication_surface_is_owed_by_a_registered_unit():
    """DERIVED from the split, so a fifth new surface cannot arrive uncovered.

    A queue declared with no producer and no countdown is a surface that exists
    only in this module's own table. R26 named the duplicate audit and the
    adoption plan as review items, and both obligations lived in a ``why`` string
    until this test, which is the shape P5 forbids by name.
    """
    declared = {
        surface.queue
        for surface in review.SURFACES
        if surface.adjudicated and not surface.legacy_file
    }
    assert set(NEW_SURFACE_OWED_BY) == declared, (
        f"new adjudication surfaces with no registered producer: "
        f"{sorted(declared - set(NEW_SURFACE_OWED_BY))}; stale entries: "
        f"{sorted(set(NEW_SURFACE_OWED_BY) - declared)}"
    )
    for queue, key in NEW_SURFACE_OWED_BY.items():
        assert key in _pending.PENDING, (
            f"{queue} is owed by {key}, which is not in the pending register, so "
            f"nothing counts down to it"
        )


@requires("cratekit.acquire.match_cli")
def test_the_match_verb_sends_only_the_middle_state_to_the_queue():
    """U16's obligation, registered here because U11 settled the split.

    R11 resolves each track to matched, needs review, or missing. U11 declared
    the first and the last as OUTPUTS and the middle one as the version match
    queue, and that declaration is only worth having if the first unit able to
    contradict it is held to it.
    """
    source = (SRC_ROOT / "cratekit" / "acquire" / "match_cli.py").read_text()
    assert calls_review(source, "offer"), (
        "the match verb declares that it adjudicates and never calls this "
        "module's offer; a call to something else spelled the same way is not "
        "the review queue"
    )
    assert offers_into(source, "Queue.VERSION_MATCH"), (
        "the match verb offers into some queue other than the one U11 declared "
        "for R11's needs-review state; the queue must reach the offer call, "
        "directly or through a constant assigned from it"
    )
    assert not constructs_a_csv_writer(source), (
        "the match verb writes a comma separated file for a person to edit, which "
        "is the surface R12 replaces"
    )


def _package_methods_on(package: str, wanted: str) -> set[str]:
    """Every method called on something ANY module in a package built from ``wanted``.

    The union across modules rather than per module, for the reason
    :func:`_package_offers_into` is walked: the subject of the countdown is the
    UNIT, not one file in it, and a unit that puts its store access in one module
    and its queue access in another has done the ordinary thing.
    """
    reached: set[str] = set()
    root = SRC_ROOT.joinpath(*package.split("."))
    for _name, source in package_modules(root):
        reached |= methods_on_review_construction(source, wanted)
    return reached


def _package_constructs(package: str, wanted: str) -> bool:
    root = SRC_ROOT.joinpath(*package.split("."))
    return any(constructs_review(source, wanted) for _name, source in package_modules(root))


def test_the_deletion_pass_records_declines_and_tombstones_where_they_are_revocable():
    """U24's obligation, ARMED. R35 and R36 both require revocability by name.

    A deletion pass keeping its own file would satisfy "remembered" and fail
    "until the decline is revoked", and nothing about a green suite would show it.

    IT WALKS THE PACKAGE RATHER THAN ONE FILE, and the change is deliberate. The
    entry was registered against ``cratekit.deletion.cli`` because that was the
    only module name the plan had spelled at the time. What R35 and R36 require
    is a property of the UNIT: a countdown pointed at one file inside a package
    is satisfied by that file and blind to the rest, which is P3, and it is also
    how the obligation would have been read as met by a shell that merely called
    something. The shape here is the one U34's and U23's countdowns already use.
    """
    reached = _package_methods_on("cratekit.deletion", "DecisionStore")
    assert _package_constructs("cratekit.deletion", "DecisionStore"), (
        "the deletion pass does not reach the decision stores at all"
    )
    assert "record" in reached, (
        "the deletion pass never records a suppression through a store it built "
        "from this module, so a declined file is offered again on the next run "
        "(R35)"
    )
    assert "revoke" in reached, (
        "the deletion pass records suppressions and offers no way to revoke one; "
        "R36 says a tombstone is listable AND revocable"
    )
    assert _package_offers_into("cratekit.deletion", "Queue.DELETION"), (
        "R35 presents a removed row's file for review, and U11 declared the "
        "queue that presentation goes through"
    )
    root = SRC_ROOT / "cratekit" / "deletion"
    for name, source in package_modules(root):
        assert not constructs_a_csv_writer(source), (
            f"{name} writes a comma separated file for a person to edit"
        )


#: A package that does everything the countdown asks, SPLIT ACROSS TWO MODULES,
#: which is the shape the landed unit actually has and the shape a per-file guard
#: would have failed on. Assembled here rather than asserted against the real
#: package alone, because a guard proved only against the code it was written for
#: is a guard nobody has proved anything about (P7).
_CORRECT_SPLIT_PACKAGE = {
    "stores.py": """
from cratekit.core import review


def tombstones(cfg):
    return review.DecisionStore("tombstones", cfg)


def record(cfg, identity):
    store = tombstones(cfg)
    return store.record(kind="version", identity=identity, actor="cli")


def undo(cfg, suppression_id):
    store = tombstones(cfg)
    return store.revoke(suppression_id, actor="cli")
""",
    "run.py": """
from cratekit.core import review


def present(store, identity):
    return review.offer(
        store, queue=review.Queue.DELETION, kind="removed-file",
        identity=identity, payload={},
    )
""",
}

#: The same package with the store replaced by a private ledger and the queue
#: replaced by one that is not this one. Every method name still matches, which is
#: exactly what the name-matching version of this guard was satisfied by.
_EVASIVE_SPLIT_PACKAGE = {
    "stores.py": """
class _Ledger:
    def record(self, row):
        ...

    def revoke(self, row):
        ...


def keep(rows):
    ledger = _Ledger()
    for row in rows:
        ledger.record(row)
        ledger.revoke(row)
""",
    "run.py": """
from cratekit.core import review


def present(store, identity):
    return review.offer(
        store, queue=review.Queue.GENRE, kind="removed-file",
        identity=identity, payload={},
    )
""",
}


def _assemble(root: Path, files: dict[str, str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "__init__.py").write_text("")
    for name, source in files.items():
        (root / name).write_text(source)
    return root


def _package_answers(root: Path) -> tuple[bool, set[str], bool]:
    """The three questions the countdown asks, over an assembled package."""
    modules = package_modules(root)
    reached: set[str] = set()
    for _name, source in modules:
        reached |= methods_on_review_construction(source, "DecisionStore")
    return (
        any(constructs_review(source, "DecisionStore") for _name, source in modules),
        reached,
        any(offers_into(source, "Queue.DELETION") for _name, source in modules),
    )


def test_the_deletion_countdown_bites_a_package_that_evades_it(tmp_path):
    """P7's first half, on the guard's own shape rather than on one file's."""
    constructs, reached, offers = _package_answers(
        _assemble(tmp_path / "evasive", _EVASIVE_SPLIT_PACKAGE)
    )
    assert not constructs, (
        "a private ledger with methods named record and revoke answers for the "
        "decision stores, so R35's revocability is unenforced"
    )
    assert reached == set()
    assert not offers, (
        "offering into some other queue satisfies the deletion countdown, so the "
        "surface U11 declared for R35 is unenforced"
    )


def test_the_deletion_countdown_stays_quiet_on_a_correct_package(tmp_path):
    """P7's second half, which is the half that keeps getting skipped.

    The correct package here SPLITS the store access and the queue access across
    two modules. A guard that reads one file would fail this, and a guard that
    fails correct code is a guard somebody routes around.
    """
    constructs, reached, offers = _package_answers(
        _assemble(tmp_path / "correct", _CORRECT_SPLIT_PACKAGE)
    )
    assert constructs
    assert {"record", "revoke"} <= reached
    assert offers


def _package_offers_into(package: str, queue: str) -> bool:
    """Whether ANY module in a landed package offers into ``queue``.

    Walked rather than named, because a countdown pointed at one file inside a
    package is satisfied by that file and blind to the rest of the unit (P3).
    """
    root = SRC_ROOT.joinpath(*package.split("."))
    return any(offers_into(source, queue) for _name, source in package_modules(root))


@requires("cratekit.modules.reports")
def test_the_duplicate_audit_offers_its_pairs_into_the_duplicates_queue():
    """U34's obligation, and half of R26.

    The source system's duplicate audit prints and never records, so a pair
    somebody has already judged an intentional alternate is reported again on
    every run. The persistent ignore U34's brief asks for IS a verdict in this
    queue, and a private ignore file beside the report would satisfy the brief
    and re-create the defect.
    """
    assert _package_offers_into("cratekit.modules.reports", "Queue.DUPLICATES")


@requires("cratekit.adopt")
def test_the_adoption_plan_becomes_review_items_rather_than_a_file():
    """U23's obligation, and the other half of R26.

    R26 says adoption presents its whole plan for review and applies it
    incrementally and resumably. Resumable across sessions is precisely what a
    plan file cannot be, because the verdicts have to outlive the process that
    collected them.
    """
    assert _package_offers_into("cratekit.adopt", "Queue.ADOPTION")


@requires("cratekit.intake")
def test_the_path_repair_pass_offers_its_proposals_into_the_path_repair_queue():
    """U37's obligation.

    A wrong answer here re-points a library row at somebody else's file, so a
    proposal is never applied without a decision, and a decision is never taken
    from a file somebody edited.
    """
    assert _package_offers_into("cratekit.intake", "Queue.PATH_REPAIR")
