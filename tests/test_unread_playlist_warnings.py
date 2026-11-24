"""R-2020: route resort's gate and the rebuild's report name every playlist not compared.

A playlist the after check could not tie to one destination (R-1991) is not a
difference, so a rebuild clears a restored tree's flag over it and
``left_behind`` never counts it; the resort's gate read ``left behind: N`` as
the whole count. Now the gate, the resort's drive and the rebuild's drive name
each one in ``converge``'s wording, driven through ``cli.run`` over
``tests/test_routing_workers.py``'s disposable database. D1 applies.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.cli import converge as converge_cli
from cratekit.cli import rebuild as rebuild_verb
from cratekit.core import config, convergence, jobs, rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild, routing_cli
from tests import test_routing_workers as routing
from tests._sync_builders import exited

# The routing suite's fixtures and seams, by name so pytest finds them here.
_platform_seams, _release_process_locks = routing._platform_seams, routing._release_process_locks
acknowledged, configured, leftover = routing.acknowledged, routing.configured, routing.leftover
library, native, stocked = routing.library, routing.native, routing.stocked

ARRIVED, RESORT, TREE_ID = routing.ARRIVED, routing.RESORT, routing.TREE_ID
RESORT_GATE = routing.RESORT_GATE

#: A folder under the tree's root whose name declares no genre and that no write recorded.
RENAMED = "Loud! Room"

REBUILD = ("rebuild", "--actor", "a-person")


def _unread(cfg: config.Config, root_id: str, *, beside: str = "2") -> str:
    """Track 1, which the tree files, in a playlist of a folder no write recorded.
    The playlist bears the name of the one a write filed track ``beside`` into, so
    the check cannot tell whose it is: the case R-1991 names as not compared."""
    (playlist_name,) = {
        node.playlist_display
        for node in routing._tree_nodes(cfg, root_id)
        if beside in node.content_ids
    }
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        folder = rb_writer.ensure_folder(handle, RENAMED, handle.get_playlist(ID=root_id))
        playlist = rb_writer.ensure_playlist(handle, playlist_name, folder)
        rb_writer.add_memberships(handle, playlist, ["1"])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    return f"{RENAMED}/{playlist_name}"


def _named(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == rebuild.UNIDENTIFIED_PLAYLISTS]


def _left(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == rebuild.LEFT_BEHIND]


def _offered() -> dict:
    """What the resort's gate shows on its first ask, which ends in a refusal."""
    refused = exited(routing._drive_once([*RESORT]), ExitCode.DECISION_REQUIRED)
    assert refused["cause"]["detail"]["gate"] == RESORT_GATE
    return refused["cause"]["detail"]["shown"]


def _resumed(argv) -> dict:
    """``argv`` queued and its job resumed, which must exit OK."""
    _job_id, code, done = routing._queue_and_resume(argv)
    assert code == int(ExitCode.OK), done
    return done


def _says_what_it_left(done: dict) -> None:
    (left,) = _left(done)
    assert ARRIVED in left["message"] and "1 membership" in left["message"], left


def _enqueued(handler_key: str, payload: dict, item_ids: tuple[str, ...]) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.enqueue(
            store, handler_key=handler_key, payload=payload, cfg=config.load(), item_ids=item_ids
        )


# 1. The resort's gate


def test_the_resort_gate_names_a_playlist_not_compared_beside_its_left_behind_count(
    acknowledged, native, leftover
):
    """THE RESIDUAL: the count is the check's, and the playlist it did not read is named."""
    unread = _unread(acknowledged, native)
    shown = _offered()
    assert shown["left behind"] == 1, shown
    (said,) = shown["playlists not compared"]
    assert unread in said, said
    assert said.endswith(rebuild.UNIDENTIFIED), said
    assert "1 playlist(s)" in said, said
    # Only asking: nothing was written.
    assert routing._membership(acknowledged, native) == {"1", "2"}


def test_the_resort_gate_over_nothing_unread_says_nothing_of_it(acknowledged, native, leftover):
    """The same tree, every playlist read: no such fact, so the fact means something."""
    shown = _offered()
    assert shown["left behind"] == 1, shown
    assert shown["playlists not compared"] == [], shown


def test_the_resumes_gate_shows_the_playlist_the_plan_could_not_read(
    acknowledged, native, leftover
):
    """Frozen with the facts, so a person answering later reads what the plan read."""
    unread = _unread(acknowledged, native)
    job_id = exited(routing._drive([*RESORT]))["data"]["job_id"]
    with jobs.open_store() as store:
        facts = jobs.get(store, job_id).payload[routing_cli.RESORT_FACTS_KEY]
    assert facts["unidentified"] == [unread], facts
    assert routing_cli._resort_facts([], facts)["playlists not compared"] == [
        rebuild.unidentified_message([unread])
    ]


def test_a_fresh_plan_over_no_routed_tree_records_an_empty_list(acknowledged):
    """A plan that routed nothing still records the list, or it reads as an older build's."""
    shown = _offered()
    assert shown["trees"] == [] and shown["adds"] == 0, shown
    assert shown["playlists not compared"] == [], shown


def test_a_job_an_older_build_froze_says_its_plan_did_not_record_them(
    acknowledged, native, leftover
):
    """Round one's blocker: facts frozen with no list showed an empty one, a clean report."""
    _unread(acknowledged, native)
    # The facts the base froze over this library: no ``unidentified`` key at all.
    facts = {"left_alone": [], "left_behind": 1, "not_derived": ["vocal"], "trees": [TREE_ID]}
    payload = {
        routing_cli.RESORT_ADDS_KEY: routing._approved_adds(), routing_cli.RESORT_FACTS_KEY: facts
    }
    job = _enqueued("route.resort", payload, (TREE_ID,))
    resumed = routing._drive_once([*RESORT, "--job", job.job_id])
    refused = exited(resumed, ExitCode.DECISION_REQUIRED)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["playlists not compared"] == [routing_cli.UNRECORDED_UNREAD], shown
    # A plan that recorded the list and found nothing shows nothing.
    recorded = routing_cli._resort_facts([], {**facts, "unidentified": []})
    assert recorded["playlists not compared"] == []


def test_every_envelope_after_the_gate_names_it(acknowledged, native, leftover):
    """Queued, declined and nothing to add alike: an answer over a gate is not complete."""
    unread = _unread(acknowledged, native)
    (queued,) = _named(exited(routing._drive([*RESORT])))
    assert unread in queued["message"]
    run_id = routing._drive_once([*RESORT])[1]["run_id"]
    decide = ["run", "decide", run_id, RESORT_GATE, "abort", "--actor", "a-person"]
    exited(routing._drive_once(decide))
    declined = exited(routing._drive_once(["--run", run_id, *RESORT]))
    assert declined["data"]["state"] == "declined"
    (said,) = _named(declined)
    assert unread in said["message"]


# 2. The resort's drive


def test_the_resort_drive_names_the_playlist_beside_what_it_left(acknowledged, native, leftover):
    """The after check's own reading, carried through the item report."""
    unread = _unread(acknowledged, native)
    done = _resumed(RESORT)
    assert routing._membership(acknowledged, native) == {"1", "2"}
    _says_what_it_left(done)
    (named,) = _named(done)
    assert named["message"] == rebuild.unidentified_message([unread]), named


def test_a_resort_drive_over_nothing_unread_says_nothing_of_it(acknowledged, native, leftover):
    done = _resumed(RESORT)
    assert len(_left(done)) == 1
    assert _named(done) == []


def test_a_resort_that_failed_part_way_names_the_playlist_as_a_step(
    acknowledged, native, leftover, monkeypatch
):
    """The other exit: a refusal carries no warnings, so it is a step on the cause."""
    unread = _unread(acknowledged, native)
    job = routing._enqueue_resort(TREE_ID, "second_tree")
    routing._fail_other_trees(monkeypatch)
    refused = routing._fails(routing._drive([*RESORT, "--job", job.job_id]))
    steps = list(refused["cause"]["remediation"]["steps"])
    assert rebuild.unidentified_message([unread]) in steps, steps
    assert any(ARRIVED in step for step in steps), steps


# 3. The rebuild's drive


@pytest.fixture
def filed(acknowledged, native) -> str:
    """A tree a rebuild filed, then a playlist beside track 1's own that no write recorded."""
    _resumed(REBUILD)
    return _unread(acknowledged, native, beside="1")


def test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist(
    acknowledged, native, filed
):
    """THE BRIEF'S THIRD SCENARIO: not a difference, so the flag clears, and it is said."""
    convergence.mark_unconverged(acknowledged, [TREE_ID], reason="a restore")
    assert convergence.read(acknowledged).tree(TREE_ID).blocking
    done = _resumed(REBUILD)
    assert not convergence.read(acknowledged).tree(TREE_ID).blocking
    (named,) = _named(done)
    assert named["message"] == rebuild.unidentified_message([filed]), named
    assert _left(done) == []


def test_a_rebuild_names_what_it_left_beside_what_it_did_not_compare(
    acknowledged, native, leftover
):
    """R-635: the rebuild says what it left, as the resort does, and the flag stays."""
    unread = _unread(acknowledged, native)
    convergence.mark_unconverged(acknowledged, [TREE_ID], reason="a restore")
    done = _resumed(REBUILD)
    assert convergence.read(acknowledged).tree(TREE_ID).blocking
    _says_what_it_left(done)
    (named,) = _named(done)
    assert named["message"] == rebuild.unidentified_message([unread]), named


def test_a_rebuild_over_nothing_unread_or_left_says_nothing_of_either(acknowledged, native):
    done = _resumed(REBUILD)
    assert _named(done) == [] and _left(done) == []


def test_a_rebuild_that_failed_part_way_names_what_the_finished_tree_found_as_steps(
    acknowledged, native, leftover, monkeypatch
):
    """The rebuild's other exit, new with R-2020: a refusal carries the sentences as steps."""
    unread = _unread(acknowledged, native)
    job = _enqueued("rebuild", {"tree": None, "actor": "a-person"}, (TREE_ID, "second_tree"))
    routing._fail_other_trees(monkeypatch)
    refused = routing._fails(routing._drive([*REBUILD, "--job", job.job_id]))
    with jobs.open_store() as store:
        stored = jobs.get(store, job.job_id).cause
    steps = list(refused["cause"]["remediation"]["steps"])
    assert steps[: len(stored.remediation.steps)] == list(stored.remediation.steps)
    left, named = steps[len(stored.remediation.steps) :]
    assert ARRIVED in left and "1 membership" in left, left
    assert named == rebuild.unidentified_message([unread])
    assert refused["cause"]["reason"] == stored.reason


def test_the_rebuild_worker_reports_its_after_check(acknowledged, native, leftover):
    """The item report is the only way back from a worker to its resume (R-443)."""
    unread = _unread(acknowledged, native)
    job_id, code, done = routing._queue_and_resume(REBUILD)
    assert code == int(ExitCode.OK), done
    (report,) = rebuild_verb.REBUILD_ARTIFACTS.committed(acknowledged, job_id)
    assert report["tree_id"] == TREE_ID
    assert report["unidentified"] == [unread]
    assert [entry["content_id"] for entry in report["left_behind"]] == ["2"]
    listed_in = Path(_left(done)[0]["message"].rsplit("listed in ", 1)[1])
    assert listed_in == rebuild_verb.REBUILD_ARTIFACTS.final_dir(acknowledged, job_id)
    (written,) = sorted(listed_in.glob("*.json"))
    assert json.loads(written.read_text(encoding="utf-8")) == report


# 4. One wording


def test_converge_and_the_writes_share_one_wording(filed):
    """The sentence a person reads after a playlist not compared is the same everywhere."""
    (check,) = converge_cli.converge(_ConvergeCtx())["data"]["checks"]
    assert f"not-compared:{filed}" in check["detail"], check
    assert check["status"] == converge_cli.NOT_COMPARED, check
    assert check["detail"].endswith(rebuild.UNIDENTIFIED), check


class _ConvergeCtx:
    class args:  # noqa: N801 - the namespace argparse would hand the verb
        tree = None

    @staticmethod
    def envelope(*, data, **kwargs):
        return {"data": data, **kwargs}


def test_the_message_names_every_playlist_uncapped_and_sorted():
    """Every one, since a cut list would read as the whole set."""
    names = [f"F/{index:02d}" for index in range(30, 0, -1)]
    message = rebuild.unidentified_message(names)
    assert message is not None
    assert message.startswith("30 playlist(s)"), message
    assert "; ".join(sorted(names)) in message, message
    assert rebuild.unidentified_message([]) is None
    assert rebuild.unidentified_warnings([]) == ()
    (warning,) = rebuild.unidentified_warnings(["F/P"])
    assert warning == {
        "code": "playlist-not-compared", "message": rebuild.unidentified_message(["F/P"])
    }


def test_the_count_is_every_entry_named_a_name_two_trees_share_included():
    """Row M5: two trees' playlists of one folder and name are two, as the list shows them."""
    message = rebuild.unidentified_message(["F/P", "F/P"])
    assert message is not None
    assert message.startswith("2 playlist(s)"), message
    assert "F/P; F/P" in message, message


def test_every_item_report_of_a_job_is_read_back():
    """Row M9: a job over several trees names what each one's check found, not the first's."""
    reports = [
        {"tree_id": "one", "left_behind": [], "unidentified": ["A/One"]},
        {"tree_id": "two", "left_behind": [], "unidentified": ["B/Two"]},
    ]
    warnings, steps = rebuild.after_messages(reports, listed_in="the list")
    (warning,) = warnings
    assert warning == {
        "code": rebuild.UNIDENTIFIED_PLAYLISTS,
        "message": rebuild.unidentified_message(["A/One", "B/Two"]),
    }
    assert steps == (warning["message"],)
    # A report an older build wrote, with no such key, adds nothing and breaks nothing.
    assert rebuild.after_messages([{"tree_id": "old", "left_behind": []}], listed_in="x") == ((), ())
