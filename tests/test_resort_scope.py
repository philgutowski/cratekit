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
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild
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


def _resort() -> tuple[int, dict]:
    """Queue the resort and drive the job it queued, as the job engine would."""
    code, queued = _drive(["route", "resort"])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]
    assert job_id, queued
    return _drive(["route", "resort", "--job", job_id])


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
