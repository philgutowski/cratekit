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

import ast
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
from tests._pending import requires

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
    """DERIVED from the inventory, so a third store cannot appear undeclared."""
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
# Both guards below are gated on the unit that lands the module they walk, so
# each is a countdown rather than a wish in a docstring. Both walk the syntax
# tree for real CALLS rather than searching the source text for a token: a token
# search is satisfied by a docstring explaining why the call matters, which is how
# this repository shipped a countdown that would have kept passing with every
# call deleted.


def _calls_named(source: str, names: set[str]) -> set[str]:
    """Which of ``names`` this source actually CALLS, as attribute calls."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in names:
                found.add(node.func.attr)
    return found


def _attributes_named(source: str, names: set[str]) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Attribute) and node.attr in names:
            found.add(node.attr)
    return found


def _writes_a_comma_separated_file(source: str) -> list[str]:
    """Comma separated WRITER construction, in either import shape.

    Narrowed to the ``csv`` module rather than to the attribute name, and to
    writing rather than reading, so it cannot fire on an unrelated ``.writer``
    or on legitimate intake of a file somebody else produced (P7). The same
    question is asked in ``tests/test_cli_contract.py`` by conformance 4.
    """
    tree = ast.parse(source)
    names = {"writer", "DictWriter"}
    imported = {
        alias.asname or alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "csv"
        for alias in node.names
        if alias.name in names
    }
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in names:
            if isinstance(func.value, ast.Name) and func.value.id == "csv":
                found.append(f"line {node.lineno}")
        elif isinstance(func, ast.Name) and func.id in imported:
            found.append(f"line {node.lineno}")
    return found


@requires("cratekit.acquire.match_cli")
def test_the_match_verb_sends_only_the_middle_state_to_the_queue():
    """U16's obligation, registered here because U11 settled the split.

    R11 resolves each track to matched, needs review, or missing. U11 declared
    the first and the last as OUTPUTS and the middle one as the version match
    queue, and that declaration is only worth having if the first unit able to
    contradict it is held to it.
    """
    source = (SRC_ROOT / "cratekit" / "acquire" / "match_cli.py").read_text()
    assert _calls_named(source, {"offer"}), (
        "the match verb declares that it adjudicates and never offers anything "
        "into the review queue"
    )
    assert _attributes_named(source, {"VERSION_MATCH"}), (
        "the match verb offers into some queue other than the one U11 declared "
        "for R11's needs-review state"
    )
    assert not _writes_a_comma_separated_file(source), (
        "the match verb writes a comma separated file for a person to edit, which "
        "is the surface R12 replaces"
    )


@requires("cratekit.deletion.cli")
def test_the_deletion_verb_records_declines_and_tombstones_where_they_are_revocable():
    """U24's obligation. R35 and R36 both require revocability by name.

    A deletion pass keeping its own file would satisfy "remembered" and fail
    "until the decline is revoked", and nothing about a green suite would show it.
    """
    source = (SRC_ROOT / "cratekit" / "deletion" / "cli.py").read_text()
    assert _attributes_named(source, {"DecisionStore"}) or _calls_named(
        source, {"DecisionStore"}
    ), "the deletion verb does not reach the decision stores at all"
    assert _calls_named(source, {"record"}), (
        "the deletion verb never records a suppression, so a declined file is "
        "offered again on the next run (R35)"
    )
    assert _calls_named(source, {"revoke"}) or _attributes_named(source, {"revoke"}), (
        "the deletion surface records suppressions and offers no way to revoke "
        "one; R36 says a tombstone is listable AND revocable"
    )
    assert not _writes_a_comma_separated_file(source), (
        "the deletion verb writes a comma separated file for a person to edit"
    )
