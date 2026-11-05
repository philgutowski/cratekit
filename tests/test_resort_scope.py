"""U219: a resort after a genre sub is added writes only under the genre tree.

Sitting 61 (A69) hand edited the Rominimal genre sub into a copy of the live
library's taxonomy and ran ``crate route resort`` on a disposable copy. It made
``BY GENRE + ENERGY / Minimal / Deep Tech / Rominimal`` as it should, and it
also made a folder ``INBOX / Minimal / Deep Tech`` holding every band and the
genre sub, which the live INBOX has never carried. The resort queued one item
per database native tree, the intake tree is native, and since R-746 the
cutover records it with the taxonomy as its derivation source, so its rebuild
derived the routing tree's placements and wrote them under the INBOX root. This
is R-789, which was filed unmeasured.

Every expected value here is spelled from the brief or read off the database
the fixture built, never from the code under test.
"""

from __future__ import annotations

import io
import json
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output
from cratekit.core import config, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild, routing_cli
from tests.cli_drive import approve_and_queue
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

GENRE_TREE = "BY GENRE + ENERGY"
INTAKE = "INBOX"
BATCH = "a landed batch"
BUCKET_FOLDER = "Minimal / Deep Tech"
GENRE_SUB = "Rominimal"

#: Two files under the music directory, each tagged with the genre sub's one
#: source, so both file into their band and into the genre sub.
FIRST = "Puls One.flac"
SECOND = "Puls Two.flac"


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def configured(library) -> config.Config:
    cfg = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    config.save(cfg)
    config.reset_cache()
    return cfg


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """The machine facts a temporary library cannot speak for, as the sibling suites patch them."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION
    )
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / "Music"


@pytest.fixture
def tagged(configured, monkeypatch) -> config.Config:
    """Both files read as Rominimal at one energy, through the readings seam.

    The derivation reads tags off disk; the readings are supplied here rather
    than written into audio, which is the seam ``declared_membership`` names for
    a caller supplying readings and not rules.
    """
    for name in (FIRST, SECOND):
        (_music(configured) / name).write_bytes(b"")

    def readings(music: Path):
        return [
            rebuild.Truth(location=str(music / name), genre=GENRE_SUB, energy=5)
            for name in (FIRST, SECOND)
        ]

    monkeypatch.setattr(rebuild, "library_truth", readings)
    return configured


@pytest.fixture
def both_native(tagged, monkeypatch) -> dict[str, str]:
    """A disposable database where BOTH declared trees have cut over.

    The genre tree's root is empty; the intake root holds one landed batch with
    both rows in it, as INBOX does after a sync landing. Both are recorded with
    the taxonomy as their source, which is what the cutover verb records for
    each since R-746.
    """
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: tagged.library.volume_id),
    )
    path = Path(tagged.library.db_path)
    _build_disposable_database(path)
    conn = sqlite3.connect(path)
    try:
        for content_id, name in (("1", FIRST), ("2", SECOND)):
            conn.execute(
                "UPDATE djmdContent SET FolderPath = ?, rb_local_deleted = 0 WHERE ID = ?",
                (str(_music(tagged) / name), content_id),
            )
        conn.commit()
    finally:
        conn.close()
    handle = rb_writer.open_db(path, unlock=False, cfg=tagged)
    try:
        genre_root = rb_writer.ensure_folder(handle, GENRE_TREE)
        intake_root = rb_writer.ensure_folder(handle, INTAKE)
        batch = rb_writer.ensure_playlist(handle, BATCH, intake_root)
        rb_writer.add_memberships(handle, batch, ["1", "2"])
        handle.session.commit()
        roots = {"genre": str(genre_root.ID), "intake": str(intake_root.ID)}
    finally:
        rb_writer.close_db(handle)
    declared = taxonomy.default_taxonomy()
    tree_registry.write(
        tagged,
        tree_registry.Registry(
            tuple(
                tree_registry.TreeRecord(
                    tree_id=tree_id,
                    mode=tree_registry.Mode.DATABASE,
                    cutover_on=date(2026, 8, 1),
                    root_id=root_id,
                    source=tree_registry.DerivationSource.TAXONOMY,
                )
                for tree_id, root_id in (
                    (declared.tree.id, roots["genre"]),
                    (declared.intake.id, roots["intake"]),
                )
            )
        ),
    )
    session.record_acknowledgment(tagged, terminal=lambda: True)
    return roots


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    assert out.getvalue().strip(), f"the verb printed nothing: {err.getvalue()}"
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    return code, document


def _below(cfg: config.Config, root_id: str) -> dict[str, set[str]]:
    """Every node under a root by its path from the root, and the rows each holds.

    Read straight from the file with sqlite rather than through the engine's
    own walk, which stops two levels down and would not see a node deeper than
    the shape it expects.
    """
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        found: dict[str, set[str]] = {}
        pending = [(root_id, "")]
        while pending:
            parent, prefix = pending.pop()
            for node_id, name in conn.execute(
                "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? "
                "AND COALESCE(rb_local_deleted, 0) = 0",
                (parent,),
            ).fetchall():
                path = f"{prefix}{name}"
                found[path] = {
                    str(row[0])
                    for row in conn.execute(
                        "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
                        "AND COALESCE(rb_local_deleted, 0) = 0",
                        (node_id,),
                    ).fetchall()
                }
                pending.append((str(node_id), f"{path} / "))
        return found
    finally:
        conn.close()


GATE = "route.resort.apply"


def _resort() -> tuple[int, dict]:
    """Approve the plan, queue the resort and drive its job, as the engine would."""
    run_id, job_id = approve_and_queue(["route", "resort"], GATE)
    return _drive(["--run", run_id, "route", "resort", "--job", job_id])


def _offered() -> dict:
    """The refusal the first ask ends in, which carries the plan it showed."""
    code, refused = _drive(["route", "resort"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    return refused


def _decide(run_id: str, option: str) -> None:
    code, envelope = _drive(["run", "decide", run_id, GATE, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), envelope


def test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root(both_native):
    """Sitting 61 in one test: INBOX gains nothing, the genre tree gains the sub."""
    cfg = config.load()
    before = _below(cfg, both_native["intake"])
    assert before == {BATCH: {"1", "2"}}, before

    code, done = _resort()
    assert code == int(ExitCode.OK), done

    assert _below(cfg, both_native["intake"]) == before, (
        "the resort wrote under INBOX, which is the folder sitting 61 found: "
        "the intake tree's rebuild derived the routing tree's placements"
    )
    genre = _below(cfg, both_native["genre"])
    assert genre[f"{BUCKET_FOLDER} / {GENRE_SUB}"] == {"1", "2"}, genre



# ═══════════════════════════════════════════════════════════════════════════
# The plan at its gate
# ═══════════════════════════════════════════════════════════════════════════


def test_the_gate_shows_every_add_and_only_the_routing_trees(both_native):
    """The brief's "the gate shows the adds": both bands and the genre sub, by file."""
    cfg = config.load()
    shown = _offered()["cause"]["detail"]["shown"]
    music = _music(cfg)
    expected = sorted(
        (BUCKET_FOLDER, playlist, str(music / name))
        for playlist in ("Med Energy", GENRE_SUB)
        for name in (FIRST, SECOND)
    )
    assert sorted((row["folder"], row["playlist"], row["path"]) for row in shown["items"]) == (
        expected
    ), shown
    assert {row["tree"] for row in shown["items"]} == {taxonomy.default_taxonomy().tree.id}
    assert shown["adds"] == 4 and shown["count"] == 4, shown
    assert any("INBOX" in line for line in shown["left alone"]), (
        "the intake tree was left alone without a word, so a person cannot tell "
        "that from a resort that forgot it"
    )
    assert _below(cfg, both_native["genre"]) == {}, "asking wrote something"


def test_the_digest_is_the_same_over_one_unchanged_library(both_native):
    """The rehearsal rule compares two digests, so two asks over one library agree."""
    first = _offered()["cause"]["detail"]["shown"]["digest"]
    second = _offered()["cause"]["detail"]["shown"]["digest"]
    assert first == second


def test_an_abort_queues_nothing_and_writes_nothing(both_native):
    cfg = config.load()
    run_id = _offered()["run_id"]
    _decide(run_id, "abort")
    code, declined = _drive(["--run", run_id, "route", "resort"])
    assert code == int(ExitCode.OK), declined
    assert declined["data"]["job_id"] == ""
    assert declined["data"]["state"] == "declined"
    assert _below(cfg, both_native["genre"]) == {}


def test_a_resort_with_no_change_plans_nothing_and_queues_nothing(both_native):
    """The second resort over a library the first one filed asks over nothing."""
    code, done = _resort()
    assert code == int(ExitCode.OK), done
    shown = _offered()["cause"]["detail"]["shown"]
    assert shown["items"] == [] and shown["adds"] == 0, shown
    refused = _offered()
    run_id = refused["run_id"]
    _decide(run_id, "apply")
    code, again = _drive(["--run", run_id, "route", "resort"])
    assert code == int(ExitCode.OK), again
    assert again["data"]["job_id"] == "", "a resort with nothing to add queued a job"
    assert again["data"]["state"] == "nothing-to-add"


def test_a_library_that_moved_after_the_gate_refuses_before_writing(both_native, monkeypatch):
    """The approved adds are what the worker may write, and nothing else."""
    cfg = config.load()
    run_id, job_id = approve_and_queue(["route", "resort"], GATE)

    def moved(music: Path):
        # The same two files, retagged to a genre the sub does not take.
        return [
            rebuild.Truth(location=str(music / name), genre="Minimal", energy=5)
            for name in (FIRST, SECOND)
        ]

    monkeypatch.setattr(rebuild, "library_truth", moved)
    code, refused = _drive(["--run", run_id, "route", "resort", "--job", job_id])
    assert code != int(ExitCode.OK), refused
    assert "resort-plan-stale" in json.dumps(refused), refused
    assert _below(cfg, both_native["genre"]) == {}, (
        "the worker wrote a plan nobody approved"
    )


def test_the_resume_argv_names_the_gate_run():
    job = type("J", (), {"job_id": "job-1", "payload": {"gate_run_id": "run-1"}})()
    assert routing_cli.resort_argv(job) == ["--run", "run-1", "route", "resort", "--job", "job-1"]
    older = type("J", (), {"job_id": "job-1", "payload": {}})()
    assert routing_cli.resort_argv(older) == ["route", "resort", "--job", "job-1"]


# ═══════════════════════════════════════════════════════════════════════════
# The class one file over: rebuild, converge and inbox
# ═══════════════════════════════════════════════════════════════════════════


def test_a_rebuild_naming_the_intake_tree_refuses_and_queues_nothing(both_native):
    code, refused = _drive(["rebuild", "--actor", "a-person", "--tree", "inbox"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "rebuild-tree-not-derivable"
    assert "INBOX" in refused["cause"]["message"]


def test_a_rebuild_of_every_tree_leaves_the_intake_tree_alone(both_native):
    cfg = config.load()
    code, queued = _drive(["rebuild", "--actor", "a-person"])
    assert code == int(ExitCode.OK), queued
    assert [w["code"] for w in queued["warnings"]] == ["tree-not-derived"], queued
    code, done = _drive(["rebuild", "--actor", "a-person", "--job", queued["data"]["job_id"]])
    assert code == int(ExitCode.OK), done
    assert _below(cfg, both_native["intake"]) == {BATCH: {"1", "2"}}
    assert _below(cfg, both_native["genre"])[f"{BUCKET_FOLDER} / {GENRE_SUB}"] == {"1", "2"}


def test_converge_reads_the_intake_tree_as_not_compared(both_native):
    """Not hundreds of missing rows: the derivation does not describe that tree."""
    code, report = _drive(["converge", "--tree", "inbox"])
    (check,) = report["data"]["checks"]
    assert check["status"] == "not-compared", report
    assert "INBOX" in check["detail"]


def test_route_inbox_files_into_the_routing_tree_only(both_native, monkeypatch):
    """Route inbox filed into every native tree, the same shape one verb over."""
    cfg = config.load()
    intake = Path(cfg.library.root) / taxonomy.default_taxonomy().intake.display
    intake.mkdir(parents=True, exist_ok=True)
    arrived = intake / "Puls Three.flac"
    arrived.write_bytes(b"")
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute("UPDATE djmdContent SET FolderPath = ? WHERE ID = '2'", (str(arrived),))
        conn.commit()
    finally:
        conn.close()
    monkeypatch.setattr(
        rebuild,
        "read_truth",
        lambda path: rebuild.Truth(location=str(path), genre=GENRE_SUB, energy=5),
    )
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert _below(cfg, both_native["intake"]) == {BATCH: {"1", "2"}}, (
        "route inbox wrote the routing tree's folders under INBOX"
    )
    assert _below(cfg, both_native["genre"])[f"{BUCKET_FOLDER} / {GENRE_SUB}"] == {"2"}


# ═══════════════════════════════════════════════════════════════════════════
# The guard, at the derivation
# ═══════════════════════════════════════════════════════════════════════════


def test_every_declared_place_but_the_routing_tree_is_not_derivable():
    declared = taxonomy.default_taxonomy()
    others = rebuild.other_declared_trees(declared)
    assert declared.tree.id not in others
    assert others[declared.intake.id] == declared.intake.display
    for node in (declared.intake_old, declared.inspiration, declared.catalog):
        if node is not None:
            assert others[node.id] == node.display
    assert rebuild.derivable(declared, declared.tree.id)
    assert not rebuild.derivable(declared, declared.intake.id)
    # A tree the declaration does not name is read as a routing tree.
    assert rebuild.derivable(declared, "shelf_stack")


def test_the_derivation_refuses_the_intake_tree_before_reading_a_file(configured, monkeypatch):
    declared = taxonomy.default_taxonomy()

    def unread(music):
        raise AssertionError("the derivation read the library before refusing")

    monkeypatch.setattr(rebuild, "library_truth", unread)
    with pytest.raises(CratekitError) as caught:
        rebuild.declared_membership(
            configured,
            declared,
            tree_id=declared.intake.id,
            source=tree_registry.DerivationSource.TAXONOMY,
            vocal_threshold=None,
        )
    assert caught.value.cause.reason == "rebuild-tree-not-derivable"
