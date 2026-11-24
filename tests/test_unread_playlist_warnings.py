"""R-2020: route resort's gate and the rebuild's report name every playlist not compared.

A playlist the after check could not tie to one destination
(``ConvergenceReport.unidentified``, R-1991) is not a difference, so a
rebuild clears a restored tree's flag over it and ``left_behind`` never
counts it. Only ``crate converge`` named it, so the resort's gate read
``left behind: N`` as the whole count over a playlist nothing read. Now the
gate, the resort's drive and the rebuild's drive name each one, in the
wording ``converge`` uses. Driven through ``cli.run`` over the disposable
database ``tests/test_routing_workers.py`` builds; every expected name is
asked of the shipped taxonomy. D1 applies.
"""

from __future__ import annotations

import json
from pathlib import Path

from cratekit.cli import converge as converge_cli
from cratekit.cli import rebuild as rebuild_verb
from cratekit.core import config, convergence, jobs, rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild, routing_cli
from tests._sync_builders import exited
from tests.test_routing_workers import (
    ARRIVED,
    RESORT,
    RESORT_GATE,
    TREE_ID,
    _drive,
    _drive_once,
    _enqueue_resort,
    _fail_other_trees,
    _fails,
    _membership,
    _platform_seams,
    _queue_and_resume,
    _release_process_locks,
    _tree_nodes,
    acknowledged,
    configured,
    leftover,
    library,
    native,
    stocked,
)

__all__ = [
    "_platform_seams",
    "_release_process_locks",
    "acknowledged",
    "configured",
    "leftover",
    "library",
    "native",
    "stocked",
]

#: A folder under the tree's root whose name declares no genre and that no write recorded.
RENAMED = "Loud! Room"

REBUILD = ("rebuild", "--actor", "a-person")


def _unread(cfg: config.Config, root_id: str) -> str:
    """Track 1, which the tree files, in a playlist of a folder no write recorded.

    The playlist bears the name of the one the inbox route filed the leftover
    into, read back from the database, so the check cannot tell whose it is:
    the case R-1991 names as not compared.
    """
    (playlist_name,) = {
        node.playlist_display for node in _tree_nodes(cfg, root_id) if "2" in node.content_ids
    }
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        root = handle.get_playlist(ID=root_id)
        folder = rb_writer.ensure_folder(handle, RENAMED, root)
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
    code, refused = _drive_once([*RESORT])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == RESORT_GATE
    return refused["cause"]["detail"]["shown"]


# 1. The resort's gate


def test_the_resort_gate_names_a_playlist_not_compared_beside_its_left_behind_count(
    acknowledged, native, leftover
):
    """THE RESIDUAL: the count is the check's, and the playlist it did not read is named."""
    unread = _unread(acknowledged, native)
    shown = _offered()
    assert shown["left behind"] == 1, shown
    (said,) = shown["not compared"]
    assert unread in said, said
    assert said.endswith(rebuild.UNIDENTIFIED), said
    assert "1 playlist(s)" in said, said
    # Only asking: nothing was written.
    assert _membership(acknowledged, native) == {"1", "2"}


def test_the_resort_gate_over_nothing_unread_says_nothing_of_it(acknowledged, native, leftover):
    """The same tree, every playlist read: no such fact, so the fact means something."""
    shown = _offered()
    assert shown["left behind"] == 1, shown
    assert shown["not compared"] == [], shown


def test_the_resumes_gate_shows_the_playlist_the_plan_could_not_read(
    acknowledged, native, leftover
):
    """Frozen with the facts, so a person answering later reads what the plan read."""
    unread = _unread(acknowledged, native)
    job_id = exited(_drive([*RESORT]))["data"]["job_id"]
    with jobs.open_store() as store:
        facts = jobs.get(store, job_id).payload[routing_cli.RESORT_FACTS_KEY]
    assert facts["unidentified"] == [unread], facts
    assert routing_cli._resort_facts([], facts)["not compared"] == [
        rebuild.unidentified_message([unread])
    ]


def test_every_envelope_after_the_gate_names_it(acknowledged, native, leftover):
    """Queued, declined and nothing to add alike: an answer over a gate is not complete."""
    unread = _unread(acknowledged, native)
    (queued,) = _named(exited(_drive([*RESORT])))
    assert unread in queued["message"]
    run_id = _drive_once([*RESORT])[1]["run_id"]
    exited(_drive_once(["run", "decide", run_id, RESORT_GATE, "abort", "--actor", "a-person"]))
    declined = exited(_drive_once(["--run", run_id, *RESORT]))
    assert declined["data"]["state"] == "declined"
    (said,) = _named(declined)
    assert unread in said["message"]


# 2. The resort's drive


def test_the_resort_drive_names_the_playlist_beside_what_it_left(acknowledged, native, leftover):
    """The after check's own reading, carried through the item report."""
    unread = _unread(acknowledged, native)
    _, code, done = _queue_and_resume(RESORT)
    assert code == int(ExitCode.OK), done
    assert _membership(acknowledged, native) == {"1", "2"}
    (left,) = _left(done)
    assert ARRIVED in left["message"] and "1 membership" in left["message"], left
    (named,) = _named(done)
    assert named["message"] == rebuild.unidentified_message([unread]), named


def test_a_resort_drive_over_nothing_unread_says_nothing_of_it(acknowledged, native, leftover):
    _, code, done = _queue_and_resume(RESORT)
    assert code == int(ExitCode.OK), done
    assert len(_left(done)) == 1
    assert _named(done) == []


def test_a_resort_that_failed_part_way_names_the_playlist_as_a_step(
    acknowledged, native, leftover, monkeypatch
):
    """The other exit: a refusal carries no warnings, so it is a step on the cause."""
    unread = _unread(acknowledged, native)
    job = _enqueue_resort(TREE_ID, "second_tree")
    _fail_other_trees(monkeypatch)
    refused = _fails(_drive([*RESORT, "--job", job.job_id]))
    steps = list(refused["cause"]["remediation"]["steps"])
    assert rebuild.unidentified_message([unread]) in steps, steps
    assert any(ARRIVED in step for step in steps), steps


# 3. The rebuild's drive


def test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist(
    acknowledged, native, leftover
):
    """THE BRIEF'S THIRD SCENARIO: not a difference, so the flag clears, and it is said."""
    unread = _unread(acknowledged, native)
    convergence.mark_unconverged(acknowledged, [TREE_ID], reason="a restore")
    _, code, done = _queue_and_resume(REBUILD)
    assert code == int(ExitCode.OK), done
    assert not convergence.read(acknowledged).tree(TREE_ID).blocking
    (named,) = _named(done)
    assert named["message"] == rebuild.unidentified_message([unread]), named
    # R-635: the rebuild says what it left, as the resort does.
    (left,) = _left(done)
    assert ARRIVED in left["message"], left


def test_a_rebuild_over_nothing_unread_or_left_says_nothing_of_either(acknowledged, native):
    _, code, done = _queue_and_resume(REBUILD)
    assert code == int(ExitCode.OK), done
    assert _named(done) == [] and _left(done) == []


def test_the_rebuild_worker_reports_its_after_check(acknowledged, native, leftover):
    """The item report is the only way back from a worker to its resume (R-443)."""
    unread = _unread(acknowledged, native)
    job_id, code, done = _queue_and_resume(REBUILD)
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


def test_converge_and_the_writes_share_one_wording(acknowledged, native, leftover, monkeypatch):
    """The sentence a person reads after a playlist not compared is the same everywhere."""
    unread = _unread(acknowledged, native)
    (check,) = converge_cli.converge(_ConvergeCtx())["data"]["checks"]
    assert f"not-compared:{unread}" in check["detail"], check
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
        "code": "playlist-not-compared",
        "message": rebuild.unidentified_message(["F/P"]),
    }
