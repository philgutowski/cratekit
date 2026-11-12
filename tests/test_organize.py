"""U112: ``crate organize`` tidies both sides by the product's own rules.

Every drive goes through the real dispatcher against a disposable database
built the way the adoption and rotation suites build one, with the two provider
seams faked the way the label and set suites fake them: a catalogue that
answers from memory and a strict account that records every call and refuses
any method the protocol does not declare. Each scenario reads the database from
SQL and the account from the fake, never from the verb's own report alone.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import io
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.cli import registry
from cratekit.core import config, locations, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.organize import account as account_area
from cratekit.organize import cli as organize_cli
from cratekit.organize import filing, own, rekordbox
from tests import adopt_fixtures, cutover_fixtures, deadca7_fixtures, outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedArtist, catalogue_factory
from tests.test_adoption import _bucket_and_genre
from tests.test_config import valid_data
from tests.test_export_set import BUILD as SET_BUILD
from tests.test_export_set import NAME as SET_NAME
from tests.test_export_set import ROWS, SEARCHES
from tests.test_label_playlists import LABEL, LABEL_ID, LISTED, RELEASES
from tests.test_label_workers import register
from tests.test_outbound_workers import bind as bind_account
from tests.test_rb_writer_db import RECORDED_APP_VERSION

DECLARED = taxonomy.default_taxonomy()
DB_GATE = organize_cli.REKORDBOX_GATE
ACCOUNT_GATE = organize_cli.ACCOUNT_GATE
TODAY = date(2026, 10, 3)
VERB = ["organize", "--as-of", TODAY.isoformat()]

#: The batch named for its run, forty days old: the rotation moves it into Old,
#: where it is younger than the expiry and stays.
RUN_NAMED = "2026-06-25T101010Z-1_inboxed"
#: A batch named the way U110 names one, which no suggestion touches.
DATED = "2026-09-28 Tidal playlists"
#: The author's own, one on each side, each with an obvious home.
MINE_IN_REKORDBOX = f"{LABEL} favourites"
MINE_ON_ACCOUNT = "Warmup 2024"


def _tracks() -> tuple[adopt_fixtures.Track, ...]:
    _bucket, genre = _bucket_and_genre(DECLARED)
    return (
        adopt_fixtures.Track("r-one", "one.flac", genre),
        adopt_fixtures.Track("r-two", "two.flac", genre),
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as the rotation suite patches it."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False)
    )


@pytest.fixture
def machine(tmp_path, monkeypatch):
    """Every module on, two unfiled tracks in the database, nothing acknowledged."""
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(
        root,
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, _tracks())
    collection.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return resolved


@pytest.fixture
def seams(machine, monkeypatch):
    """The catalogue and the account, with one playlist of the author's on it."""
    fake = FakeCatalogue(
        artists={LABEL_ID: FakePagedArtist(list(LISTED))},
        releases=dict(RELEASES),
        confirmed={"r1", "r2", "r3", "r4", "r5", "r7"},
        searches=dict(SEARCHES),
        account=[AccountPlaylist("mine-1", MINE_ON_ACCOUNT, 4)],
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    held = outbound_fakes.StrictAccount()
    held.titles["mine-1"] = MINE_ON_ACCOUNT
    bind_account(monkeypatch, held)
    return machine, fake, held


def _query(cfg: config.Config, sql: str, *params) -> list[tuple]:
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def _node(cfg, name: str, *, under: str | None, age: int | None = None, tracks=()) -> str:
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        parent = handle.get_playlist(ID=under) if under is not None else None
        row = handle.create_playlist(name, parent=parent)
        if age is not None:
            row.created_at = datetime.combine(TODAY - timedelta(days=age), datetime.min.time())
        for content_id in tracks:
            handle.add_to_playlist(row, content_id)
        handle.session.commit()
        return str(row.ID)
    finally:
        rb_writer.close_db(handle)


def _cut_over(cfg: config.Config) -> str:
    """Both trees database native. Answers the intake root's identifier."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        handle.session.commit()
        tree_root = str(root.ID)
    finally:
        rb_writer.close_db(handle)
    tree_registry.record_cutover(
        cfg, DECLARED.tree.id, root_id=tree_root, on=TODAY,
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    inbox = cutover_fixtures.add_folder(cfg, DECLARED.intake.display)
    tree_registry.write(
        cfg,
        tree_registry.read(cfg).with_record(
            tree_registry.TreeRecord(
                tree_id=DECLARED.intake.id,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=TODAY,
                root_id=inbox,
                source=tree_registry.DerivationSource.TAXONOMY,
            )
        ),
    )
    return inbox


def _two_acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _proof(cfg: config.Config, name: str) -> Path:
    """An intake file named for ``name``, naming one file under the music folder."""
    music = Path(cfg.library.root) / "Music" / "one.flac"
    xml = Path(cfg.library.root) / f"{name}_inboxed.xml"
    xml.write_text(
        '<DJ_PLAYLISTS Version="1.0.0"><COLLECTION Entries="1">'
        f'<TRACK TrackID="1" Location="{locations.location_url(music)}"/>'
        "</COLLECTION></DJ_PLAYLISTS>\n",
        encoding="utf-8",
    )
    return xml


@pytest.fixture
def world(seams):
    """The brief's library: unfiled tracks, an old batch, a label with no folder,
    a downloaded set at the account root, and one thing of the author's each side."""
    cfg, fake, held = seams
    session.record_acknowledgment(cfg, terminal=lambda: True)
    inbox = _cut_over(cfg)
    ids = {
        "batch": _node(cfg, RUN_NAMED, under=inbox, age=40, tracks=("r-one",)),
        # A U110 batch, young and readably named: kept, and no rename suggested.
        "dated": _node(cfg, DATED, under=inbox, age=5, tracks=("r-two",)),
        "listen later": _node(cfg, "listen later", under=inbox, age=5),
        "mine": _node(cfg, MINE_IN_REKORDBOX, under=None),
    }
    (Path(cfg.library.root) / cfg.library.music_dir / DATED).mkdir(parents=True)
    register(LABEL)
    tracklist = Path(cfg.library.root).parent / "lists" / f"{SET_NAME}.txt"
    tracklist.parent.mkdir(parents=True, exist_ok=True)
    tracklist.write_text("".join(f"{a} - {t}\n" for a, t in ROWS), encoding="utf-8")
    code, built = _two_acts(["export", "set", str(tracklist)], SET_BUILD)
    assert code == int(ExitCode.OK), built
    _proof(cfg, SET_NAME)
    # THE ACCOUNT LISTS WHAT THE PRODUCT MADE TOO, at its root, so an
    # assertion that the set is not the author's has something to exclude.
    from cratekit.modules.outbound import ledger

    fake.account.append(
        AccountPlaylist(ledger.set_playlist(cfg, SET_NAME).remote_id, SET_NAME, len(ROWS))
    )
    return cfg, fake, held, inbox, ids


def _answered(db: str = "approve", acct: str = "apply", *extra: str) -> tuple[int, dict, dict]:
    """Both explicit gates answered by their two acts, then the run that writes.

    Answers the final code and envelope, and the refusal at the first gate.
    """
    argv = [*VERB, *extra]
    collection.reset_cache()
    code, first = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert first["cause"]["detail"]["gate"] == DB_GATE
    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, DB_GATE, db, "--actor", "a-person"])[0] == 0
    collection.reset_cache()
    code, second = drive(["--run", run_id, *argv])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert second["cause"]["detail"]["gate"] == ACCOUNT_GATE
    assert drive(["run", "decide", run_id, ACCOUNT_GATE, acct, "--actor", "a-person"])[0] == 0
    collection.reset_cache()
    code, done = drive(["--run", run_id, *argv])
    return code, done, first


def _steps(envelope: dict, area: str) -> dict[str, dict]:
    return {step["step"]: step for step in envelope["data"]["summary"]["areas"][area]["steps"]}


def _report() -> dict:
    collection.reset_cache()
    code, envelope = drive([*VERB, "--report"])
    assert code == int(ExitCode.OK), envelope
    return envelope


def _parent(cfg: config.Config, playlist_id: str) -> str:
    ((parent,),) = _query(cfg, "SELECT ParentID FROM djmdPlaylist WHERE ID = ?", playlist_id)
    return str(parent)


def _filed(cfg: config.Config) -> list[str]:
    """Every live membership outside the INBOX batches, as content identifiers."""
    rows = _query(
        cfg,
        "SELECT s.ContentID, p.Name FROM djmdSongPlaylist s JOIN djmdPlaylist p "
        "ON p.ID = s.PlaylistID WHERE COALESCE(s.rb_local_deleted, 0) = 0",
    )
    return sorted(str(content) for content, name in rows if name not in (RUN_NAMED, DATED))


# ---------------------------------------------------------------------------
# The declaration
# ---------------------------------------------------------------------------


def test_the_verb_declares_one_explicit_gate_per_area_and_every_surface_its_steps_write():
    entry = registry.entry("organize")
    by_name = {spec.name: spec for spec in entry.gates}
    for name in (DB_GATE, ACCOUNT_GATE):
        assert by_name[name].explicit is True
        assert by_name[name].digest_source == "plan"
    assert registry.CLOUD_SYNC_UNREADABLE_GATE in entry.gates
    assert entry.writes == frozenset({"db_tree", "db_metadata", "remote"})
    assert entry.destructive is True


def test_the_adoption_step_queues_under_the_handler_key_adopt_apply_owns():
    assert rekordbox.ADOPT_HANDLER == registry.entry("adopt.apply").handler_key


# ---------------------------------------------------------------------------
# The brief's scenarios
# ---------------------------------------------------------------------------


def test_one_step_of_each_kind_is_planned_in_its_own_area(world):
    envelope = _report()

    database = _steps(envelope, rekordbox.AREA)
    remote = _steps(envelope, account_area.AREA)
    assert database[rekordbox.ADOPT]["state"] == "planned"
    assert database[rekordbox.ADOPT]["counts"]["to file"] == 2
    assert database[rekordbox.ROTATE]["state"] == "planned"
    assert database[rekordbox.ROTATE]["counts"]["move"] == 1
    assert database[rekordbox.RECORD_LABELS]["state"] == "listed"
    assert remote[f"label:{LABEL_ID}"]["state"] == "planned"
    assert remote[f"archive:{SET_NAME}"]["state"] == "planned"
    # Nothing of one area's leaks into the other.
    assert not {key for key in database if key.startswith(("label:", "archive:", "mark:"))}
    assert not {rekordbox.ADOPT, rekordbox.ROTATE} & set(remote)


def test_what_the_author_made_is_listed_with_a_home_and_never_a_write(world):
    cfg, _fake, held, inbox, ids = world
    envelope = _report()
    areas = envelope["data"]["summary"]["areas"]

    mine_db = {one["name"]: one for one in areas[rekordbox.AREA]["yours"]}
    # The trees the taxonomy declares are the product's, never the author's.
    assert not {DECLARED.tree.display, DECLARED.intake.display} & set(mine_db)
    assert DATED not in mine_db
    assert mine_db[MINE_IN_REKORDBOX]["suggested_home"] == f"{DECLARED.catalog.display} / {LABEL}"
    assert mine_db["listen later"]["suggested_home"] is None
    mine_account = {one["name"]: one for one in areas[account_area.AREA]["yours"]}
    # A WORKING CUSTOM PLAYLIST STAYS AT THE ROOT (U143), reversing U131's move
    # into Mine: unmarked and unclaimed, it is listed and never planned.
    assert set(mine_account) == {MINE_ON_ACCOUNT}
    assert mine_account[MINE_ON_ACCOUNT]["suggested_home"] == "the 2024 year folder"
    # The set the product made is listed by the account and is not the author's.
    assert SET_NAME not in mine_account
    (filed,) = [
        step for step in areas[account_area.AREA]["steps"] if step["step"] == account_area.FILE
    ]
    assert [row["id"] for row in filed["plan"] if row.get("kind_folder") == "Mine"] == []
    # The run named batch is a suggestion, never a step.
    assert [one["name"] for one in areas[rekordbox.AREA]["suggested"]] == [RUN_NAMED]

    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert ("mine-1", MINE_ON_ACCOUNT) not in held.renamed
    assert "mine-1" not in held.placed
    assert ("mine-1", "empty") not in held.root_removed and "mine-1" in held.titles
    assert _parent(cfg, ids["mine"]) in rb_writer.ROOT_PARENT_SENTINELS
    assert _parent(cfg, ids["listen later"]) == inbox
    for area in done["data"]["summary"]["areas"].values():
        for step in area["steps"]:
            if step["step"] == account_area.FILE:
                # THE FILING STEP NAMES EVERY PLAYLIST AT THE ROOT (U116), and an
                # unmarked one of the author's is left there (U143), with why.
                (row,) = [one for one in step["plan"] if one["name"] == MINE_ON_ACCOUNT]
                assert row["action"] == filing.LEFT and row["why"] == filing.WORKING_CUSTOM
                assert "kind_folder" not in row
                continue
            assert MINE_ON_ACCOUNT not in str(step["plan"])
            assert MINE_IN_REKORDBOX not in str(step["plan"])


def test_deadca7s_folder_is_named_once_as_foreign_and_a_full_apply_leaves_it_as_it_was(world):
    """U185. Another app's folder at the top, holding the very tracks organize files.

    The report names it once, as a fact, and never among the author's own with
    a home; both gates applied leave every row the push wrote, its cues and the
    pushed track's analysis columns byte for byte as they were, and a second
    report reads it the same way.
    """
    cfg, _fake, _held, _inbox, _ids = world
    pushed = deadca7_fixtures.push(cfg.library.db_path, ("r-one", "r-two"))
    before = deadca7_fixtures.written(cfg.library.db_path, pushed)

    envelope = _report()
    area = envelope["data"]["summary"]["areas"][rekordbox.AREA]
    assert deadca7_fixtures.FOLDER not in {one["name"] for one in area["yours"]}
    assert area["facts"][rekordbox.FOREIGN_FACT].startswith(f"{deadca7_fixtures.FOLDER} at")
    # NAMED ONCE, as the folder: the playlists in it are never listed.
    for name in deadca7_fixtures.PLAYLISTS.values():
        assert name not in str(envelope)

    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert deadca7_fixtures.written(cfg.library.db_path, pushed) == before
    # Organize filed the tracks the push holds, into its own tree, and that
    # took nothing from the push's playlists.
    filed_outside = _query(
        cfg,
        "SELECT s.ContentID FROM djmdSongPlaylist s JOIN djmdPlaylist p ON p.ID = s.PlaylistID "
        "WHERE COALESCE(s.rb_local_deleted, 0) = 0 AND p.ParentID != ? AND p.Name NOT IN (?, ?)",
        pushed.folder_id,
        RUN_NAMED,
        DATED,
    )
    assert {"r-one", "r-two"} <= {str(content) for (content,) in filed_outside}
    again = _report()["data"]["summary"]["areas"][rekordbox.AREA]
    assert deadca7_fixtures.FOLDER not in {one["name"] for one in again["yours"]}
    assert rekordbox.FOREIGN_FACT in again["facts"]


def test_approving_rekordbox_and_aborting_the_account_writes_only_rekordbox(world):
    cfg, _fake, held, inbox, ids = world
    assert _filed(cfg) == []

    code, done, _first = _answered("approve", "abort")

    assert code == int(ExitCode.OK), done
    assert _filed(cfg) == ["r-one", "r-two"]
    assert _parent(cfg, ids["batch"]) != inbox
    assert held.folders_created == []
    assert [one for one in held.renamed if one[0] != "mine-1"] == []
    assert held.moves == []


def test_aborting_rekordbox_and_applying_the_account_writes_only_the_account(world):
    cfg, _fake, held, inbox, ids = world

    code, done, _first = _answered("abort", "apply")

    assert code == int(ExitCode.OK), done
    assert _filed(cfg) == []
    assert _parent(cfg, ids["batch"]) == inbox
    assert LABEL in held.folders_created
    # U242: what the account area marked is held as taken, no prefix written.
    from cratekit.sync import mark_record

    assert mark_record.MarkRecord(cfg).taken_ids()
    assert not any(name.startswith("DOWNLOADED ") for _pid, name in held.renamed)


def test_report_writes_nothing_and_asks_nothing(world):
    cfg, _fake, held, inbox, ids = world
    before = _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID")
    members = _query(cfg, "SELECT * FROM djmdSongPlaylist ORDER BY ID")
    created = list(held.created)

    envelope = _report()

    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["answers"] == {}
    assert _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID") == before
    assert _query(cfg, "SELECT * FROM djmdSongPlaylist ORDER BY ID") == members
    assert held.created == created and held.folders_created == [] and held.moves == []


def test_one_steps_refusal_leaves_every_other_plan_on_screen(world):
    register("Ostgut Ton")  # followed, and the catalogue has no artist for it

    envelope = _report()

    remote = _steps(envelope, account_area.AREA)
    refused = [key for key, step in remote.items() if step["state"] == "refused"]
    assert refused == ["label:ostgut-ton"], remote
    assert remote[f"label:{LABEL_ID}"]["state"] == "planned"
    assert remote[f"archive:{SET_NAME}"]["state"] == "planned"
    assert _steps(envelope, rekordbox.AREA)[rekordbox.ADOPT]["state"] == "planned"
    codes = [warning["code"] for warning in envelope["warnings"]]
    assert "organize-step-refused" in codes


def test_a_second_run_after_a_full_apply_plans_nothing(world):
    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done

    # U147. THE MIRROR READS THE TREE BEFORE THE DATABASE AREA WRITES IT, plan
    # then ask then write, so a playlist the adoption made in a run is mirrored
    # by the next one, and the mirror is all the second run plans.
    lagging = [
        step["step"]
        for area in _report()["data"]["summary"]["areas"].values()
        for step in area["steps"]
        if step["state"] == "planned"
    ]
    assert lagging and all(key.startswith("mirror:") for key in lagging), lagging
    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done

    envelope = _report()

    for area in envelope["data"]["summary"]["areas"].values():
        planned = [step["step"] for step in area["steps"] if step["state"] == "planned"]
        assert planned == [], area
        assert all(step["state"] != "refused" for step in area["steps"]), area


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(seams):
    """The database area is refused before it is planned; the account area still asks."""
    cfg, _fake, held = seams
    register(LABEL)

    code, first = drive(VERB)

    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert first["cause"]["detail"]["gate"] == ACCOUNT_GATE
    code, done = _two_acts(VERB, ACCOUNT_GATE, "apply")
    assert code == int(ExitCode.OK), done
    refused = done["data"]["summary"]["areas"][rekordbox.AREA]["refused"]
    assert refused["reason"] == "backup-acknowledgment-missing"
    assert done["data"]["summary"]["areas"][rekordbox.AREA]["steps"] == []
    assert done["data"]["summary"]["answers"][rekordbox.AREA] is None
    assert LABEL in held.folders_created


def test_a_set_with_no_intake_file_named_for_it_waits_and_is_not_planned(world):
    cfg, _fake, _held, _inbox, _ids = world
    (Path(cfg.library.root) / f"{SET_NAME}_inboxed.xml").unlink()

    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]

    assert step["state"] == "listed"
    assert "crate export archive" in step["detail"]
    # U142: the reason names both proofs, so neither reads as the only one.
    assert "no intake file named for this set" in step["detail"]
    assert "no INSPIRATION playlist of its name" in step["detail"]


def test_an_area_with_nothing_to_do_still_asks(seams):
    cfg, _fake, _held = seams
    session.record_acknowledgment(cfg, terminal=lambda: True)

    code, first = drive(VERB)

    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert first["cause"]["detail"]["gate"] == DB_GATE
    shown = first["cause"]["detail"]["shown"]
    # No tree has cut over here, so the adoption and the rotation each refuse
    # on their own, and the area has nothing to write and says so.
    assert "nothing to do" in shown, shown
    states = {item["step"]: item["state"] for item in shown["items"]}
    assert states[rekordbox.ADOPT] == "refused" and states[rekordbox.ROTATE] == "refused"


# ---------------------------------------------------------------------------
# The homes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "home"),
    [
        ("Kompakt", "the Kompakt label folder"),
        ("kompakt  2021 picks", "the Kompakt label folder"),
        ("Kompakter", None),
        ("Warmup 2024", "the 2024 year folder"),
        ("1999 and 2024", None),
        ("Room 12345", None),
        ("anything", None),
    ],
)
def test_an_account_home_is_a_label_then_a_year_and_otherwise_none(name, home):
    assert own.account_home(name, ("Kompakt",)) == home


def test_the_longest_followed_label_wins():
    assert own.label_of("Kompakt Extra 2", ("Kompakt", "Kompakt Extra")) == "Kompakt Extra"


def test_a_rekordbox_home_needs_a_declared_label_tree():
    assert own.rekordbox_home("Kompakt faves", ("Kompakt",), None) is None
    assert own.rekordbox_home("Kompakt faves", ("Kompakt",), "Record Labels") == (
        "Record Labels / Kompakt"
    )


# ---------------------------------------------------------------------------
# What the review found
# ---------------------------------------------------------------------------


def test_the_adoption_job_carries_a_run_its_own_resume_can_answer(world):
    from cratekit.cli import gates
    from cratekit.core import jobs

    code, done, _first = _answered("approve", "abort")
    assert code == int(ExitCode.OK), done

    step = _steps(done, rekordbox.AREA)[rekordbox.ADOPT]
    with jobs.open_store() as store:
        (job,) = [one for one in jobs.list_jobs(store) if one.handler_key == rekordbox.ADOPT_HANDLER]
    handed = gates.load(job.payload[jobs.GATE_RUN_KEY])
    assert handed.verb == rekordbox.ADOPT_VERB == registry.entry("adopt.apply").name
    decision = handed.decisions[rekordbox.ADOPT_GATE]
    assert (decision.option, decision.actor, decision.digest) == ("approve", "a-person", step["digest"])
    from cratekit.adopt import apply_cli

    assert job.payload[apply_cli.ACTOR_KEY] == "a-person"
    assert rekordbox.ADOPT_GATE in {spec.name for spec in registry.entry("adopt.apply").gates}


def _held_gates(digest: str):
    from cratekit.cli import gates

    state = gates.RunState(run_id="run-1", verb="organize", created="2026-10-03T00:00:00Z")
    state.decisions[DB_GATE] = gates.Decision(
        option="approve", actor="a-person", recorded="2026-10-03T00:00:00Z", digest=digest
    )
    return gates.Gates(state=state)


def test_a_part_hand_off_refuses_a_digest_the_answer_was_not_given_over(tmp_path, monkeypatch):
    from cratekit.cli import output
    from cratekit.core.cause import CratekitError

    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(tmp_path))
    document = {"kind": "organize", "steps": [["adopt", "planned", "aaaa"]]}
    spec = next(one for one in registry.entry("organize").gates if one.name == DB_GATE)
    held = _held_gates(output.digest_of(document))
    with pytest.raises(CratekitError):
        held.hand_off(
            spec, verb=rekordbox.ADOPT_VERB, gate=rekordbox.ADOPT_GATE, part=(document, "bbbb")
        )
    other = {**document, "kind": "something else"}
    with pytest.raises(CratekitError):
        held.hand_off(
            spec, verb=rekordbox.ADOPT_VERB, gate=rekordbox.ADOPT_GATE, part=(other, "aaaa")
        )


def test_report_says_the_backup_acknowledgment_is_missing(seams):
    envelope = _report()

    facts = envelope["data"]["summary"]["areas"][rekordbox.AREA]["facts"]
    assert facts["backup acknowledgment"].startswith("missing")
    rows = {row["key"]: row for row in envelope["data"]["checks"]}
    assert "backup acknowledgment: missing" in rows[f"organize.{rekordbox.AREA}"]["detail"]


def test_a_set_whose_mark_was_put_back_waits_rather_than_reads_archived(world):
    from cratekit.modules.outbound import ledger
    from cratekit.sync import mark_record

    cfg, _fake, _held, _inbox, _ids = world
    (Path(cfg.library.root) / f"{SET_NAME}_inboxed.xml").unlink()
    recorded = ledger.set_playlist(cfg, SET_NAME)
    record = mark_record.MarkRecord(cfg)
    record.record_marked(SET_NAME, {recorded.remote_id: (SET_NAME, f"DOWNLOADED {SET_NAME}")})
    assert _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]["state"] == "nothing"

    record.record_unmarked(SET_NAME, recorded.remote_id)

    assert _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]["state"] == "listed"


def test_the_latest_retired_landing_wins_by_number_and_a_bracket_is_no_pattern(machine):
    root = Path(machine.library.root)
    name = "Boiler [Berlin] 2024"
    for tail in (".imported", ".imported-9", ".imported-10"):
        (root / f"{name}_inboxed.xml{tail}").write_text("x", encoding="utf-8")
    (root / "other_inboxed.xml.imported-2").write_text("x", encoding="utf-8")
    (root / "other_inboxed.xml").write_text("x", encoding="utf-8")

    found = account_area.intake_by_pass(machine)

    assert found[name].name == f"{name}_inboxed.xml.imported-10"
    assert found["other"].name == "other_inboxed.xml"


def test_an_unreadable_label_registry_refuses_the_label_step_alone(world):
    from cratekit.label import registry as labels

    labels.RegistryStore().path.write_text("{ not json", encoding="utf-8")

    envelope = _report()

    remote = _steps(envelope, account_area.AREA)
    assert remote[account_area.LABELS]["state"] == "refused"
    assert remote[account_area.LABELS]["reason"] == "label-intent-unusable"
    assert remote[f"archive:{SET_NAME}"]["state"] == "planned"
    assert _steps(envelope, rekordbox.AREA)[rekordbox.ROTATE]["state"] == "planned"


def test_a_step_that_fails_unexpectedly_lets_the_rest_run_and_is_raised_after(world, monkeypatch):
    from cratekit.intake import rotate_cli

    cfg, _fake, held, inbox, ids = world

    def broken(*args, **kwargs):
        raise RuntimeError("the disk went away")

    monkeypatch.setattr(rotate_cli, "written", broken)

    code, done, _first = _answered()

    assert code != int(ExitCode.OK)
    assert done["cause"]["reason"] == "internal-error"
    assert "These were written and stay written" in done["cause"]["message"]
    # The steps after the broken one were still applied.
    assert LABEL in held.folders_created
    assert _parent(cfg, ids["batch"]) == inbox


def test_a_plan_that_moves_after_the_answer_is_stale_rather_than_applied(world):
    cfg, _fake, held, inbox, ids = world
    collection.reset_cache()
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, DB_GATE, "approve", "--actor", "a-person"])[0] == 0
    # Another batch old enough to move, landed after the answer was given.
    _node(cfg, "2026-07-01T101010Z-2_inboxed", under=inbox, age=60)

    collection.reset_cache()
    code, again = drive(["--run", run_id, *VERB])

    assert code == int(ExitCode.DECISION_STALE), again
    assert again["cause"]["reason"] == "decision-stale"
    # U222: an area with nothing to say beside the digests leaves the refusal as the gate gave it.
    assert again["cause"]["message"] == (
        f"the decision on {DB_GATE!r} was made against a plan that has since changed"
    )
    assert "stale" not in again["cause"]["detail"]
    assert _filed(cfg) == [] and held.folders_created == []


def test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed(world):
    _cfg, _fake, held, _inbox, _ids = world
    folder = held.create_folder("My sets")
    held.placed["mine-1"] = folder

    mine = {one["name"] for one in _report()["data"]["summary"]["areas"][account_area.AREA]["yours"]}

    assert MINE_ON_ACCOUNT not in mine


def test_a_run_that_writes_nothing_ends_as_a_no_op(world):
    code, done, _first = _answered("abort", "abort")

    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert done["data"]["summary"]["answers"] == {
        rekordbox.AREA: "abort",
        account_area.AREA: "abort",
    }


def test_an_exported_playlist_the_product_made_is_not_listed_as_yours(world):
    from cratekit.modules.outbound import ledger

    cfg, fake, _held, _inbox, _ids = world
    ledger.reserve_playlist(cfg, "crate-export", lambda: "exported-1")
    fake.account.append(AccountPlaylist("exported-1", "Exported 2025", 3))

    mine = {one["name"] for one in _report()["data"]["summary"]["areas"][account_area.AREA]["yours"]}

    assert "Exported 2025" not in mine
    # The author's working custom playlist stays at the root and is listed (U143).
    assert mine == {MINE_ON_ACCOUNT}
    rows = _file_rows(_report()).values()
    assert sorted(row["id"] for row in rows if row.get("kind_folder") == "Mine") == []
    assert sorted(row["id"] for row in rows if row.get("kind_folder") == "Exports") == [
        "exported-1"
    ]


# ---------------------------------------------------------------------------
# U116: a marked custom playlist is filed into its year folder
# ---------------------------------------------------------------------------

#: A custom playlist a sync swept and marked, and its mark's year.
MARKED_ID = "custom-1"
MARKED_NAME = "DOWNLOADED Phil 10_8_26"
MARKED_YEAR = "2026"


def _marked(cfg, fake, held, playlist_id=MARKED_ID, name=MARKED_NAME, *, when="2026-10-08T21:00:00+00:00"):
    from cratekit.sync import mark_record

    fake.account.append(AccountPlaylist(playlist_id, name, 3))
    held.titles[playlist_id] = name
    mark_record.MarkRecord(cfg).record_marked(
        "Phil 10_8_26", {playlist_id: (name.removeprefix("DOWNLOADED "), name)}, now=when
    )


def _file_rows(envelope: dict) -> dict[str, dict]:
    step = _steps(envelope, account_area.AREA)[account_area.FILE]
    return {row["id"]: row for row in step["plan"]}


def test_a_marked_playlist_at_the_root_moves_into_its_year_folder(world):
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)

    step = _steps(_report(), account_area.AREA)[account_area.FILE]
    assert step["state"] == "planned"
    assert _file_rows({"data": {"summary": {"areas": {account_area.AREA: {"steps": [step]}}}}})[
        MARKED_ID
    ]["action"] == filing.MOVE

    code, done, _first = _answered()

    assert code == int(ExitCode.OK), done
    folder = held.placed[MARKED_ID]
    assert held.folder_names[folder] == MARKED_YEAR
    applied = _steps(done, account_area.AREA)[account_area.FILE]["applied"]
    # The marked playlist to its year, nothing else: the author's working
    # custom playlist stays at the root (U143).
    assert applied["moved"] == [[MARKED_ID, folder]]
    assert "mine-1" not in held.placed
    mine = {one["name"] for one in done["data"]["summary"]["areas"][account_area.AREA]["yours"]}
    assert MARKED_NAME not in mine


def test_a_missing_year_folder_is_created_once_and_reused(world):
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)
    _marked(cfg, fake, held, "custom-2", "DOWNLOADED Phil 10_9_26")

    code, done, _first = _answered()

    assert code == int(ExitCode.OK), done
    assert held.folders_created.count(MARKED_YEAR) == 1
    assert held.placed[MARKED_ID] == held.placed["custom-2"]
    # A second pass reads the folder the first made, and moves nothing again.
    step = _steps(_report(), account_area.AREA)[account_area.FILE]
    assert step["state"] == "nothing"
    assert MARKED_ID not in _file_rows(_report())


def test_an_existing_year_folder_on_the_account_is_adopted_not_made_again(world):
    cfg, fake, held, _inbox, _ids = world
    existing = held.create_folder(MARKED_YEAR)
    held.folders_created.clear()
    _marked(cfg, fake, held)

    code, done, _first = _answered()

    assert code == int(ExitCode.OK), done
    assert held.placed[MARKED_ID] == existing
    assert MARKED_YEAR not in held.folders_created


def test_an_unmarked_playlist_of_the_authors_stays_at_the_root_as_a_working_custom(world):
    """U143 REVERSES U131's MOVE INTO MINE for an unmarked, unclaimed playlist:
    by Phillip's rule of 2026-10-13 it is the one playlist the root is for."""
    _cfg, _fake, held, _inbox, _ids = world

    row = _file_rows(_report())["mine-1"]

    assert row["action"] == filing.LEFT and row["why"] == filing.WORKING_CUSTOM
    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert "mine-1" not in held.placed and held.folders_created.count("Mine") == 0


def test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine(world):
    cfg, fake, held, _inbox, _ids = world
    fake.account.append(AccountPlaylist("own-2", "DOWNLOADED by hand", 2))
    held.titles["own-2"] = "DOWNLOADED by hand"

    row = _file_rows(_report())["own-2"]

    assert row["action"] == filing.MOVE and row["why"] == filing.PREFIXED_UNMARKED
    assert row["kind_folder"] == "Mine" and row["folder"] == "create"
    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert held.folder_names[held.placed["own-2"]] == "Mine"


def test_a_mark_put_back_is_no_mark_and_the_playlist_stays(world):
    from cratekit.sync import mark_record

    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)
    mark_record.MarkRecord(cfg).record_unmarked("Phil 10_8_26", MARKED_ID)

    # The name still carries the prefix; only the mark record was put back.
    assert _file_rows(_report())[MARKED_ID]["why"] == filing.PREFIXED_UNMARKED


def test_a_marked_playlist_already_in_a_folder_is_left_where_it_is(world):
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)
    elsewhere = held.create_folder("Old faves")
    held.placed[MARKED_ID] = elsewhere

    assert MARKED_ID not in _file_rows(_report())
    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert held.placed[MARKED_ID] == elsewhere


def test_a_label_playlist_is_the_label_steps_and_a_set_the_archives(world):
    from cratekit.modules.outbound import ledger

    cfg, fake, held, _inbox, _ids = world
    # Marked as well, so only the label rule can be what leaves it.
    _marked(cfg, fake, held, "label-1", f"{LABEL} 2026")

    rows = _file_rows(_report())

    assert rows["label-1"]["action"] == filing.LEFT
    assert rows["label-1"]["why"] == filing.LABEL_STEP
    set_id = ledger.set_playlist(cfg, SET_NAME).remote_id
    assert rows[set_id]["why"] == filing.SET_STEP


def test_the_plan_is_empty_and_still_asks_when_the_root_is_clean(seams):
    _cfg, fake, _held = seams
    fake.account.clear()

    code, first = drive(VERB)

    # No acknowledgment, so the database area is refused and the account asks first.
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert first["cause"]["detail"]["gate"] == ACCOUNT_GATE
    items = first["cause"]["detail"]["shown"]["items"]
    (item,) = [one for one in items if one["step"] == account_area.FILE]
    assert item["state"] == "nothing" and item["plan"] == []


def test_two_root_folders_named_as_the_year_leave_its_playlists_reported(world):
    cfg, fake, held, _inbox, _ids = world
    held.create_folder(MARKED_YEAR)
    held.create_folder(MARKED_YEAR)
    _marked(cfg, fake, held)

    row = _file_rows(_report())[MARKED_ID]

    assert row["action"] == filing.LEFT and "2 root folders" in row["why"]


def test_a_provider_refusal_mid_pass_stops_and_names_what_moved(world):
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held, "custom-a", "DOWNLOADED A pass")
    _marked(cfg, fake, held, "custom-b", "DOWNLOADED B pass")
    held.fail_on = frozenset({"custom-b"})

    code, done, _first = _answered()

    assert code != int(ExitCode.OK)
    assert "custom-a" in held.placed and "custom-b" not in held.placed
    assert "1 playlist(s) were moved" in done["cause"]["message"]
    assert f"custom-a into {held.placed['custom-a']}" in done["cause"]["message"]


def test_a_marks_year_is_local_and_an_unreadable_one_is_empty():
    assert filing.year_of_mark("2025-12-31T23:00:00+00:00") == "2025"
    # 20:00 Eastern on 31 Dec is 01:00 UTC on 1 Jan; local year must win.
    assert filing.year_of_mark("2026-01-01T01:00:00+00:00") == "2025"
    assert filing.year_of_mark("") == ""
    assert filing.year_of_mark("soon") == ""


def test_a_year_folder_already_on_the_account_is_adopted_with_no_set_to_make_it(seams):
    """No set archive runs here, so only the filing step can have found the folder."""
    cfg, fake, held = seams
    existing = held.create_folder(MARKED_YEAR)
    held.folders_created.clear()
    _marked(cfg, fake, held)

    code, done = _two_acts(VERB, ACCOUNT_GATE, "apply")

    assert code == int(ExitCode.OK), done
    assert held.placed[MARKED_ID] == existing
    # No folder is made: the year's is adopted, and the author's working custom
    # playlist stays at the root (U143) rather than making a Mine for it.
    assert held.folders_created == []


def test_a_playlist_marked_twice_is_filed_by_its_latest_mark(seams):
    from cratekit.sync import mark_record

    cfg, fake, held = seams
    _marked(cfg, fake, held, when="2025-12-30T10:00:00+00:00")
    mark_record.MarkRecord(cfg).record_marked(
        "a later pass", {MARKED_ID: ("Phil 10_8_26", MARKED_NAME)}, now="2026-01-02T10:00:00+00:00"
    )

    code, done = _two_acts(VERB, ACCOUNT_GATE, "apply")

    assert code == int(ExitCode.OK), done
    assert held.folder_names[held.placed[MARKED_ID]] == "2026"

def test_a_playlist_two_folders_down_is_left_where_it_is(world):
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)
    archive = held.create_folder("Archive")
    nested = held.nest_folder("2025", archive)
    held.placed[MARKED_ID] = nested

    assert MARKED_ID not in _file_rows(_report())
    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert held.placed[MARKED_ID] == nested
    assert all(playlist_id != MARKED_ID for playlist_id, _folder in held.moves)


def test_a_provider_cratekit_refusal_mid_pass_carries_the_moved_list(world):
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held, "custom-a", "DOWNLOADED A pass")
    _marked(cfg, fake, held, "custom-b", "DOWNLOADED B pass")
    held.fail_on = frozenset({"custom-b"})
    held.provider_error = True

    code, done, _first = _answered()

    assert code != int(ExitCode.OK)
    assert "custom-a" in held.placed and "custom-b" not in held.placed
    detail = done["cause"]["detail"]
    assert detail["moved"] == [["custom-a", held.placed["custom-a"]]]
    assert "1 playlist(s) were moved" in done["cause"]["message"]


def test_a_folder_made_before_a_failed_ledger_write_is_named(seams, monkeypatch):
    from cratekit.modules.outbound import ledger, sets

    cfg, fake, held = seams
    _marked(cfg, fake, held)
    planned = filing.FilePlan(
        rows=(filing.Placement(MARKED_ID, MARKED_NAME, filing.MOVE, year=MARKED_YEAR),),
        years={MARKED_YEAR: filing.YearFolder(year=MARKED_YEAR, action=sets.CREATE)},
    )

    def boom(cfg_arg, document):
        raise OSError("ledger write failed")

    monkeypatch.setattr(ledger, "_write", boom)

    with pytest.raises(RuntimeError) as raised:
        filing.apply(cfg, held, planned)

    assert MARKED_YEAR in held.folders_created
    assert "1 year folder(s) were created" in str(raised.value)
    assert MARKED_ID not in held.placed


def test_a_prefixed_but_unmarked_playlist_has_its_own_reason(world):
    _cfg, fake, held, _inbox, _ids = world
    fake.account.append(AccountPlaylist("hand-1", "DOWNLOADED Hand marked", 2))
    held.titles["hand-1"] = "DOWNLOADED Hand marked"

    row = _file_rows(_report())["hand-1"]

    # No mark says when, so no year: it is the author's own and goes to Mine.
    assert row["action"] == filing.MOVE and row["why"] == filing.PREFIXED_UNMARKED
    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert held.folder_names[held.placed["hand-1"]] == "Mine"


# ---------------------------------------------------------------------------
# U137: one kind of step runs alone, ``--only``
# ---------------------------------------------------------------------------

ONLY_FILE = [*VERB, "--only", account_area.FILE]


def _not_planned(*args, **kwargs):
    raise AssertionError("an area with no step named was planned")


def _filed_alone() -> tuple[int, dict]:
    """``--only file`` answered at its one gate, the account's, then the run that writes."""
    collection.reset_cache()
    return _two_acts(ONLY_FILE, ACCOUNT_GATE, "apply")


def test_only_file_plans_the_filing_alone_and_the_database_is_not_asked(world, monkeypatch):
    cfg, fake, held, inbox, ids = world
    monkeypatch.setattr(rekordbox, "plan_area", _not_planned)
    # A marked playlist, so the filing alone has a move to make (U143 left the
    # author's unmarked one at the root).
    _marked(cfg, fake, held)
    folders, renamed, added = list(held.folders_created), list(held.renamed), list(held.added)

    collection.reset_cache()
    code, envelope = drive([*ONLY_FILE, "--report"])
    assert code == int(ExitCode.OK), envelope
    areas = envelope["data"]["summary"]["areas"]
    assert list(areas) == [account_area.AREA]
    assert [step["step"] for step in areas[account_area.AREA]["steps"]] == [account_area.FILE]
    assert areas[account_area.AREA]["facts"]["only these steps"] == account_area.FILE

    # The acknowledgment is in force, and still the account is the first gate.
    code, done = _filed_alone()

    assert code == int(ExitCode.OK), done
    assert list(done["data"]["summary"]["answers"]) == [account_area.AREA]
    assert held.folder_names[held.placed[MARKED_ID]] == MARKED_YEAR
    # No label folder, no year playlist's tracks, no mark, no archive.
    assert held.folders_created == [*folders, MARKED_YEAR]
    assert held.renamed == renamed and held.added == added
    assert _filed(cfg) == [] and _parent(cfg, ids["batch"]) == inbox


def test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing(world, monkeypatch):
    """U147. The mirror runs alone under the account's one gate, and is kept by a rerun."""
    _cfg, _fake, held, _inbox, _ids = world
    # The full verb files the batch into the tree, whose new folders the mirror
    # read before they existed, so the mirror alone has them to plan.
    assert _answered()[0] == int(ExitCode.OK)
    monkeypatch.setattr(rekordbox, "plan_area", _not_planned)
    folders = list(held.folders_created)
    only = [*VERB, "--only", account_area.MIRROR]
    renamed = list(held.renamed)

    collection.reset_cache()
    code, envelope = drive([*only, "--report"])
    assert code == int(ExitCode.OK), envelope
    steps = envelope["data"]["summary"]["areas"][account_area.AREA]["steps"]
    assert steps and all(step["step"].startswith("mirror:") for step in steps), steps
    assert any(step["state"] == "planned" for step in steps), steps

    collection.reset_cache()
    code, done = _two_acts(only, ACCOUNT_GATE, "apply")

    assert code == int(ExitCode.OK), done
    applied = [
        step["applied"]
        for step in done["data"]["summary"]["areas"][account_area.AREA]["steps"]
        if "applied" in step
    ]
    assert applied and all("requests" in one and "seconds" in one for one in applied)
    assert len(held.folders_created) > len(folders) and held.renamed == renamed
    collection.reset_cache()
    code, again = drive([*only, "--report"])
    assert code == int(ExitCode.OK), again
    states = {step["state"] for step in again["data"]["summary"]["areas"][account_area.AREA]["steps"]}
    assert "planned" not in states and "refused" not in states, again


def _mirrored_folder(cfg: config.Config) -> str:
    """One genre folder the mirror copies, by its database identifier."""
    from cratekit.organize import account_mirror

    names = [folder.name for folder in account_mirror.read_library(cfg).folders]
    assert names, "the tree holds no folder for the mirror to copy"
    ((found,),) = _query(
        cfg, "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1", names[0]
    )
    return str(found)


def _mirror_between_acts(cfg, held, monkeypatch) -> tuple[int, dict, int]:
    """``--only mirror``'s two acts with a library write between them (R-1031).

    Answers the run's code and envelope and how many matches the apply asked.
    """
    monkeypatch.setattr(rekordbox, "plan_area", _not_planned)
    only = [*VERB, "--only", account_area.MIRROR]
    collection.reset_cache()
    code, refused = drive(only)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    # A PLAYLIST MADE IN A MIRRORED FOLDER after the gate was shown, which a
    # plan read afresh would have to create, so its digest would move.
    _node(cfg, "Made After The Gate", under=_mirrored_folder(cfg), tracks=("r-one",))
    code, decided = drive(["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    asked = len(held.matches)
    collection.reset_cache()
    code, done = drive(["--run", run_id, *only])
    return code, done, len(held.matches) - asked


def test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan(world, monkeypatch):
    """R-1031, AE3. The apply rebuilds the frozen plan: no stale decision, no match asked."""
    cfg, _fake, held, _inbox, _ids = world
    assert _answered()[0] == int(ExitCode.OK)

    code, done, asked = _mirror_between_acts(cfg, held, monkeypatch)

    assert code == int(ExitCode.OK), done
    area = done["data"]["summary"]["areas"][account_area.AREA]
    assert area["facts"]["mirror plan frozen"].startswith("rebuilt from the plan frozen on run ")
    assert "rebuild" in area["facts"]["mirror plan"], area["facts"]
    assert asked == 0
    # THE APPROVED PLAN, not the moved library: the playlist made after the
    # gate is not on the account until the next refresh plans it.
    assert not any("Made After The Gate" in title for title in held.titles.values())
    frozen = config.state_path("mirror_plans", cfg)
    before = sorted(path.name for path in frozen.glob("*.json"))
    assert f"{done['run_id']}.json" in before
    collection.reset_cache()
    code, again = drive([*VERB, "--only", account_area.MIRROR, "--report"])
    assert code == int(ExitCode.OK), again
    planned = [
        item
        for step in again["data"]["summary"]["areas"][account_area.AREA]["steps"]
        if step["state"] == "planned"
        for item in step["plan"]
    ]
    assert any(" Made After The Gate" in str(item.get("playlist", "")) for item in planned), planned
    # A REPORT FREEZES NOTHING.
    assert sorted(path.name for path in frozen.glob("*.json")) == before


def test_the_gate_freezes_every_step_of_the_full_account_area(world):
    """U222. The steps a stale answer names are the whole area's, the mirror planned last.

    A step kind planned after the mirror would be missing from the frozen plan
    and named on every stale answer as one the gate did not show.
    """
    from cratekit.organize import mirror_frozen

    cfg, _fake, _held, _inbox, _ids = world
    collection.reset_cache()
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    frozen, said = mirror_frozen.load(cfg, refused["run_id"])
    assert frozen is not None, said
    collection.reset_cache()
    code, report = drive([*VERB, "--report"])
    assert code == int(ExitCode.OK), report
    keys = [step["step"] for step in report["data"]["summary"]["areas"][account_area.AREA]["steps"]]
    assert len(keys) > len([one for one in keys if one.startswith("mirror:")]) > 0, keys
    assert sorted(frozen.steps) == sorted(keys)


def test_without_the_frozen_plan_the_same_two_acts_are_refused_stale(world, monkeypatch):
    """The contrast to the drive above: what the frozen plan holds, shown by its absence."""
    from cratekit.organize import mirror_frozen

    cfg, _fake, held, _inbox, _ids = world
    assert _answered()[0] == int(ExitCode.OK)
    monkeypatch.setattr(mirror_frozen, "load", lambda _cfg, run_id: (None, "none, by the test"))

    code, done, _asked = _mirror_between_acts(cfg, held, monkeypatch)

    assert code == int(ExitCode.DECISION_STALE), done
    assert done["cause"]["reason"] == "decision-stale"
    # U222: and it says the plan was made afresh, not rebuilt, and what it cost.
    assert "mirror plan frozen: none, by the test, so it was planned afresh" in done["cause"]["message"]
    assert "to read the library and the account and plan" in done["cause"]["message"]


def test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh(world, monkeypatch):
    """R-1031. Only an answered account gate rebuilds from the frozen plan.

    A run resumed before its account gate is answered asks the gate again, and
    it is shown the library as it is now, not the plan the first act froze.
    """
    cfg, _fake, held, _inbox, _ids = world
    assert _answered()[0] == int(ExitCode.OK)
    monkeypatch.setattr(rekordbox, "plan_area", _not_planned)
    only = [*VERB, "--only", account_area.MIRROR]
    collection.reset_cache()
    code, refused = drive(only)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    _node(cfg, "Made After The Gate", under=_mirrored_folder(cfg), tracks=("r-one",))

    collection.reset_cache()
    code, again = drive(["--run", refused["run_id"], *only])

    assert code == int(ExitCode.DECISION_REQUIRED), again
    shown = again["cause"]["detail"]["shown"]
    assert not shown["mirror plan frozen"].startswith("rebuilt"), shown["mirror plan frozen"]
    planned = [item for step in shown["items"] for item in step["plan"]]
    assert any(" Made After The Gate" in str(item.get("playlist", "")) for item in planned), planned


def test_only_file_moves_a_marked_playlist_as_the_full_verb_does_and_then_plans_nothing(world):
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)

    code, done = _filed_alone()

    assert code == int(ExitCode.OK), done
    folder = held.placed[MARKED_ID]
    assert held.folder_names[folder] == MARKED_YEAR
    applied = _steps(done, account_area.AREA)[account_area.FILE]["applied"]
    assert applied["moved"] == [[MARKED_ID, folder]]
    collection.reset_cache()
    code, again = drive([*ONLY_FILE, "--report"])
    assert code == int(ExitCode.OK), again
    assert _steps(again, account_area.AREA)[account_area.FILE]["state"] == "nothing"


def test_only_files_digest_is_not_the_full_areas_and_an_answer_over_one_is_stale_for_the_other(seams):
    """No acknowledgment here, so the full verb's first gate is the account's too."""
    _cfg, _fake, held = seams
    register(LABEL)
    collection.reset_cache()
    full = _report()["data"]["summary"]["areas"][account_area.AREA]["digest"]
    collection.reset_cache()
    code, narrowed = drive([*ONLY_FILE, "--report"])
    assert code == int(ExitCode.OK), narrowed
    assert narrowed["data"]["summary"]["areas"][account_area.AREA]["digest"] != full

    code, first = drive(VERB)
    assert first["cause"]["detail"]["gate"] == ACCOUNT_GATE, first
    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person"])[0] == 0

    code, again = drive(["--run", run_id, *ONLY_FILE])

    assert code == int(ExitCode.DECISION_STALE), again
    assert held.folders_created == [] and held.moves == []


def test_the_selection_alone_moves_the_digest_when_it_names_every_step(world):
    """``--only`` over every kind plans what the full verb plans, and is still its own answer."""
    full = _report()["data"]["summary"]["areas"]
    every = [arg for kind in organize_cli.KINDS for arg in ("--only", kind)]
    collection.reset_cache()
    code, named = drive([*VERB, "--report", *every])
    assert code == int(ExitCode.OK), named
    for name, area in named["data"]["summary"]["areas"].items():
        assert [step["step"] for step in area["steps"]] == [
            step["step"] for step in full[name]["steps"]
        ]
        assert area["digest"] != full[name]["digest"]


def test_an_unknown_kind_is_refused_by_name_before_anything_is_read(machine, monkeypatch, capsys):
    from cratekit import cli
    from cratekit.modules.outbound import shell

    monkeypatch.setattr(shell, "load_config", _not_planned)

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *VERB, "--only", "filing"], stdout=out, stderr=err)

    assert code == 2
    said = capsys.readouterr().err + err.getvalue()
    assert "'filing'" in said and account_area.FILE in said


def test_report_with_only_file_makes_no_provider_write(world):
    _cfg, fake, held, _inbox, _ids = world
    _marked(_cfg, fake, held)
    before = (
        list(held.created), list(held.folders_created), list(held.moves),
        list(held.renamed), list(held.added), dict(held.placed),
    )

    collection.reset_cache()
    code, envelope = drive([*ONLY_FILE, "--report"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _steps(envelope, account_area.AREA)[account_area.FILE]["state"] == "planned"
    assert before == (
        held.created, held.folders_created, held.moves,
        held.renamed, held.added, held.placed,
    )


def test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label(world):
    from cratekit.label import registry as labels

    _cfg, _fake, held, _inbox, _ids = world
    labels.RegistryStore().path.write_text("{ not json", encoding="utf-8")

    collection.reset_cache()
    code, envelope = drive([*ONLY_FILE, "--report"])

    assert code == int(ExitCode.OK), envelope
    step = _steps(envelope, account_area.AREA)[account_area.FILE]
    assert step["state"] == "refused" and step["reason"] == "label-intent-unusable"
    code, first = drive(ONLY_FILE)
    assert first["cause"]["detail"]["gate"] == ACCOUNT_GATE, first
    assert "nothing to do" in first["cause"]["detail"]["shown"]
    assert held.moves == []


def test_only_a_database_kind_asks_the_database_alone(world, monkeypatch):
    cfg, _fake, held, _inbox, _ids = world
    monkeypatch.setattr(account_area, "plan_area", _not_planned)
    argv = [*VERB, "--only", rekordbox.ADOPT]

    collection.reset_cache()
    code, done = _two_acts(argv, DB_GATE, "approve")

    assert code == int(ExitCode.OK), done
    assert [step["step"] for step in _steps(done, rekordbox.AREA).values()] == [rekordbox.ADOPT]
    assert _filed(cfg) == ["r-one", "r-two"]
    assert list(done["data"]["summary"]["areas"]) == [rekordbox.AREA]
    assert held.folders_created == []


def test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists(world):
    """What the filing moves and what the rotation leaves alone are planned for it too."""
    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)
    fake.account.append(AccountPlaylist("kept-1", "Kept in place", 2))
    held.placed["kept-1"] = held.create_folder("My sets")
    full = _report()["data"]["summary"]["areas"]

    collection.reset_cache()
    code, envelope = drive([*VERB, "--report", "--only", "yours"])

    assert code == int(ExitCode.OK), envelope
    areas = envelope["data"]["summary"]["areas"]
    assert areas[rekordbox.AREA]["yours"] == full[rekordbox.AREA]["yours"]
    assert areas[rekordbox.AREA]["suggested"] == full[rekordbox.AREA]["suggested"]
    assert "listen later" in {one["name"] for one in areas[rekordbox.AREA]["yours"]}
    assert areas[account_area.AREA]["yours"] == full[account_area.AREA]["yours"]
    assert MARKED_NAME not in str(areas[account_area.AREA]["yours"])
    for name in (rekordbox.AREA, account_area.AREA):
        assert [step["step"] for step in areas[name]["steps"]] == ["yours"], areas[name]


def test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other(world):
    collection.reset_cache()
    code, envelope = drive(
        [*VERB, "--report", "--only", account_area.FILE, "--only", rekordbox.ROTATE]
    )

    assert code == int(ExitCode.OK), envelope
    areas = envelope["data"]["summary"]["areas"]
    assert [step["step"] for step in areas[rekordbox.AREA]["steps"]] == [rekordbox.ROTATE]
    assert [step["step"] for step in areas[account_area.AREA]["steps"]] == [account_area.FILE]
    assert areas[rekordbox.AREA]["facts"]["only these steps"] == rekordbox.ROTATE
    assert areas[account_area.AREA]["facts"]["only these steps"] == account_area.FILE


def test_a_registry_the_profile_does_not_use_does_not_refuse_the_filing(world, monkeypatch):
    from cratekit.label import registry as labels

    cfg, fake, held, _inbox, _ids = world
    _marked(cfg, fake, held)

    labels.RegistryStore().path.write_text("{ not json", encoding="utf-8")
    real = organize_cli.profiles.resolve

    def without_labels(profile, explicit=None):
        return real(profile, {**dict(explicit or {}), account_area.LABELS_MODULE: False})

    monkeypatch.setattr(organize_cli.profiles, "resolve", without_labels)

    collection.reset_cache()
    code, envelope = drive([*ONLY_FILE, "--report"])

    assert code == int(ExitCode.OK), envelope
    assert _steps(envelope, account_area.AREA)[account_area.FILE]["state"] == "planned"


def test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short(seams):
    """No tree has cut over here, so the rotation refuses, and says so under yours."""
    cfg, _fake, _held = seams
    session.record_acknowledgment(cfg, terminal=lambda: True)

    collection.reset_cache()
    code, envelope = drive([*VERB, "--report", "--only", "yours"])

    assert code == int(ExitCode.OK), envelope
    steps = _steps(envelope, rekordbox.AREA)
    assert list(steps) == [rekordbox.ROTATE, rekordbox.YOURS]
    assert steps[rekordbox.ROTATE]["state"] == "refused"


@pytest.mark.parametrize(
    ("kind", "called"),
    [
        (account_area.LABELS, ["_labels"]),
        (account_area.SETS, ["_sets"]),
        (account_area.MARKS, ["_mark_steps"]),
        (account_area.FILE, ["_file_step"]),
        (account_area.ROOT, ["_root_step"]),
        # The filing is planned for yours too, so what it moves is not listed;
        # the root step is not, since yours reads its empties off the filing.
        (account_area.YOURS, ["_file_step", "_yours"]),
    ],
)
def test_each_account_kind_runs_its_own_builder_and_no_other(seams, monkeypatch, kind, called):
    """No world here holds a landed sync pass, so the marks are pinned at their seam."""
    ran: list[str] = []

    def recorder(name):
        def built(*args, **kwargs):
            ran.append(name)
            return frozenset()

        return built

    for name in ("_labels", "_sets", "_mark_steps", "_file_step", "_root_step", "_yours"):
        monkeypatch.setattr(account_area, name, recorder(name))
    if kind not in rekordbox.STEPS:
        monkeypatch.setattr(rekordbox, "plan_area", _not_planned)

    collection.reset_cache()
    code, envelope = drive([*VERB, "--report", "--only", kind])

    assert code == int(ExitCode.OK), envelope
    assert ran == called


# ---------------------------------------------------------------------------
# U142: a set is archived into Downloaded Sets <year>, and INSPIRATION proves it
# ---------------------------------------------------------------------------


def _inspiration(cfg: config.Config, *names: str) -> str:
    """The declared INSPIRATION folder at the database root, a playlist in it per name."""
    folder = cutover_fixtures.add_folder(cfg, DECLARED.inspiration.display)
    for name in names:
        _node(cfg, name, under=folder)
    return folder


def _no_intake_file(cfg: config.Config) -> None:
    (Path(cfg.library.root) / f"{SET_NAME}_inboxed.xml").unlink()


def test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived(world):
    from cratekit.modules.outbound import ledger
    from cratekit.sync import mark_record

    cfg, _fake, held, _inbox, _ids = world
    _no_intake_file(cfg)
    _inspiration(cfg, SET_NAME)

    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]
    assert step["state"] == "planned", step
    assert f"proven by the INSPIRATION playlist {SET_NAME}" in step["detail"]

    code, done, _first = _answered("abort", "apply")

    assert code == int(ExitCode.OK), done
    recorded = ledger.set_playlist(cfg, SET_NAME)
    assert held.folder_names[held.placed[recorded.remote_id]] == f"Downloaded Sets {recorded.year}"
    assert held.titles[recorded.remote_id] == SET_NAME, "no title written (U242)"
    # THE SET'S OWN NAME IS THE PASS, so ``sync unmark --pass <set>`` finds it.
    taken = mark_record.MarkRecord(cfg).taken()[recorded.remote_id]
    assert (taken.by, taken.how) == (SET_NAME, mark_record.BY_SET)


def test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing(world):
    cfg, _fake, held, _inbox, _ids = world
    _no_intake_file(cfg)
    _node(cfg, SET_NAME, under=None)
    folder = _inspiration(cfg, SET_NAME.lower(), f"{SET_NAME} 2")
    removed = _node(cfg, SET_NAME, under=folder)
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute(
            f"UPDATE djmdPlaylist SET {rb_writer.SOFT_DELETE_COLUMN} = 1 WHERE ID = ?", (removed,)
        )
        conn.commit()
    finally:
        conn.close()

    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]

    assert step["state"] == "listed", step
    assert "no INSPIRATION playlist of its name" in step["detail"]
    assert held.moves == [] and held.renamed[-1:] != [(SET_NAME, f"DOWNLOADED {SET_NAME}")]


def test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing(world):
    """Moved and prefixed by hand, no mark recorded: the INSPIRATION proof finds it done."""
    from cratekit.modules.outbound import ledger

    cfg, _fake, held, _inbox, _ids = world
    _no_intake_file(cfg)
    _inspiration(cfg, SET_NAME)
    recorded = ledger.set_playlist(cfg, SET_NAME)
    # NOT CLEARED: the fake numbers a folder by how many it made, so a clear
    # lets the next one take this folder's identifier.
    folder = held.create_folder(f"Downloaded Sets {recorded.year}")
    held.placed[recorded.remote_id] = folder
    held.titles[recorded.remote_id] = f"DOWNLOADED {SET_NAME}"

    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]
    assert step["state"] == "nothing", step

    code, done, _first = _answered("abort", "apply")

    assert code == int(ExitCode.OK), done
    assert recorded.remote_id not in [pid for pid, _folder in held.moves]
    assert recorded.remote_id not in [pid for pid, _title in held.renamed]
    assert ledger.set_folder(cfg, f"Downloaded Sets {recorded.year}") == ""

    # A title a person set is left, and the step says so rather than "marked".
    held.titles[recorded.remote_id] = "My Own Title"
    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]
    assert step["state"] == "nothing", step
    assert "its title left as a person set it" in step["detail"]


def test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year(world):
    """The ledger records the plain year folder, and the set never goes there."""
    from cratekit.modules.outbound import ledger

    cfg, fake, held, _inbox, _ids = world
    recorded = ledger.set_playlist(cfg, SET_NAME)
    year = recorded.year
    by_hand = held.create_folder(f"Downloaded Sets {year}")
    plain = held.create_folder(year)
    made_by_hand = len(held.folders_created)
    assert ledger.reserve_set_folder(cfg, year, lambda: plain) == (plain, True)
    _marked(cfg, fake, held, when=f"{year}-06-15T12:00:00+00:00")

    code, done, _first = _answered("abort", "apply")

    assert code == int(ExitCode.OK), done
    assert held.placed[recorded.remote_id] == by_hand
    assert held.placed[MARKED_ID] == plain
    assert not {year, f"Downloaded Sets {year}"} & set(held.folders_created[made_by_hand:])
    assert held.folder_names[by_hand] == f"Downloaded Sets {year}"
    assert held.folder_names[plain] == year
    assert ledger.set_folder(cfg, f"Downloaded Sets {year}") == by_hand
    assert ledger.set_folder(cfg, year) == plain


def test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings(world):
    """Recorded under the plain year before U142, renamed by a person to the sets' name."""
    from cratekit.modules.outbound import ledger

    cfg, fake, held, _inbox, _ids = world
    recorded = ledger.set_playlist(cfg, SET_NAME)
    year = recorded.year
    renamed = held.create_folder(f"Downloaded Sets {year}")
    made_by_hand = len(held.folders_created)
    assert ledger.reserve_set_folder(cfg, year, lambda: renamed) == (renamed, True)
    _marked(cfg, fake, held, when=f"{year}-06-15T12:00:00+00:00")

    code, done, _first = _answered("abort", "apply")

    assert code == int(ExitCode.OK), done
    assert held.placed[recorded.remote_id] == renamed
    custom = held.placed[MARKED_ID]
    assert custom != renamed
    assert held.folder_names[custom] == year
    assert [name for name in held.folders_created[made_by_hand:] if year in name] == [year]
    assert ledger.set_folder(cfg, year) == custom
    assert ledger.set_folder(cfg, f"Downloaded Sets {year}") == renamed


def test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved(world):
    from cratekit.modules.outbound import ledger

    cfg, _fake, held, _inbox, _ids = world
    _no_intake_file(cfg)
    _inspiration(cfg, SET_NAME)
    recorded = ledger.set_playlist(cfg, SET_NAME)
    folder = held.create_folder(f"Downloaded Sets {recorded.year}")
    held.placed[recorded.remote_id] = folder
    held.titles[recorded.remote_id] = SET_NAME

    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]

    assert step["state"] == "planned", step
    assert step["detail"].startswith("record it as taken where it is"), step
    assert "file it in" not in step["detail"]

    code, done, _first = _answered("abort", "apply")

    assert code == int(ExitCode.OK), done
    assert recorded.remote_id not in [pid for pid, _folder in held.moves]
    assert held.titles[recorded.remote_id] == SET_NAME
    from cratekit.sync import mark_record

    assert recorded.remote_id in mark_record.MarkRecord(cfg).taken_ids()


def test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it(world):
    from cratekit.modules.outbound import ledger

    cfg, fake, held, _inbox, _ids = world
    year = ledger.set_playlist(cfg, SET_NAME).year
    _marked(cfg, fake, held, when=f"{year}-06-15T12:00:00+00:00")

    code, done, _first = _answered("abort", "apply")

    assert code == int(ExitCode.OK), done
    made = [name for name in held.folders_created if year in name]
    assert sorted(made) == sorted([f"Downloaded Sets {year}", year])
    set_id = ledger.set_playlist(cfg, SET_NAME).remote_id
    assert held.folder_names[held.placed[set_id]] == f"Downloaded Sets {year}"
    assert held.folder_names[held.placed[MARKED_ID]] == year


def test_two_inspiration_folders_refuse_the_unproven_set_alone(world):
    """Unread is not none: a proof the database cannot answer is a refusal, never a wait."""
    cfg, _fake, _held, _inbox, _ids = world
    _no_intake_file(cfg)
    _inspiration(cfg, SET_NAME)
    _inspiration(cfg)

    envelope = _report()

    remote = _steps(envelope, account_area.AREA)
    assert remote[f"archive:{SET_NAME}"]["state"] == "refused", remote
    assert remote[f"label:{LABEL_ID}"]["state"] == "planned"
    assert "organize-step-refused" in [warning["code"] for warning in envelope["warnings"]]


def test_a_taxonomy_with_no_inspiration_folder_waits_and_says_why(world, monkeypatch):
    import dataclasses

    from cratekit.core import active_taxonomy

    cfg, _fake, _held, _inbox, _ids = world
    _no_intake_file(cfg)
    _inspiration(cfg, SET_NAME)
    real = active_taxonomy.load
    monkeypatch.setattr(
        active_taxonomy, "load", lambda *a, **k: dataclasses.replace(real(*a, **k), inspiration=None)
    )

    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]

    assert step["state"] == "listed", step
    assert "no INSPIRATION folder declared" in step["detail"]


def test_a_set_proven_by_its_intake_file_never_opens_the_database_for_inspiration(world, monkeypatch):
    from cratekit.export import set_cli

    def tripwire(*_args, **_kwargs):
        raise AssertionError("the INSPIRATION folder was read for a set its file proves")

    monkeypatch.setattr(set_cli, "_inspiration_playlists", tripwire)

    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]

    assert step["state"] == "planned"
    assert f"proven by {SET_NAME}_inboxed.xml" in step["detail"]


def test_the_inspiration_proof_is_read_while_rekordbox_runs(world, monkeypatch):
    """A read handle, as the rekordbox area's own listing: an open rekordbox refuses no proof."""
    cfg, _fake, _held, _inbox, _ids = world
    _no_intake_file(cfg)
    _inspiration(cfg, SET_NAME)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)

    step = _steps(_report(), account_area.AREA)[f"archive:{SET_NAME}"]

    assert step["state"] == "planned", step


# ---------------------------------------------------------------------------
# U143: the account root kept to working custom playlists
# ---------------------------------------------------------------------------

ONLY_ROOT = [*VERB, "--only", account_area.ROOT]
DEBRIS_NAME = f"{LABEL} LIBRARY"
LEGACY_NAME = "2026 Custom Playlists"


def _root_world(world) -> tuple:
    """The 2026-10-13 root in small: debris copies whose tracks the label folder
    holds, an empty playlist, a legacy year folder, a working custom playlist,
    and two folders of the author's that no step may name."""
    cfg, fake, held, _inbox, _ids = world

    def playlist(playlist_id, name, tracks, folder=""):
        held.titles[playlist_id] = name
        held.playlists[playlist_id] = list(tracks)
        if folder:
            held.placed[playlist_id] = folder
        fake.account.append(AccountPlaylist(playlist_id, name, len(tracks)))

    held.folder_names.update(
        {
            "hand-label": LABEL,
            "hand-legacy": LEGACY_NAME,
            "hand-spotify": "Phil's Spotify",
            "hand-trivia": "Genre Trivia!",
        }
    )
    playlist("year-1", f"DOWNLOADED {LABEL} 2026", ("t1", "t2", "t3"), "hand-label")
    playlist("debris-1", DEBRIS_NAME, ("t1", "t2"))
    playlist("debris-2", DEBRIS_NAME, ("t1", "t2"))
    playlist("empty-1", "Untitled Playlist", ())
    playlist("old-1", "Custom from before", ("t9",), "hand-legacy")
    playlist("spotify-1", "Empty and kept", (), "hand-spotify")
    playlist("custom-1", "tech_house_hits - Phil", ("t1", "t2", "t3", "t4", "t5"))
    return cfg, fake, held


def _listing_without_removed(fake, held) -> None:
    """The catalogue's next listing, which no longer names what the account removed."""
    fake.account[:] = [one for one in fake.account if one.playlist_id in held.titles]


def test_only_root_removes_debris_and_empties_on_the_gate_and_files_the_legacy_folder(world):
    _cfg, fake, held = _root_world(world)
    collection.reset_cache()

    code, first = drive(ONLY_ROOT)

    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert first["cause"]["detail"]["gate"] == ACCOUNT_GATE
    shown = first["cause"]["detail"]["shown"]
    deletes = shown["deletes"]
    assert sorted(line.split(" (")[0] for line in deletes) == [
        f"remove the playlist {DEBRIS_NAME!r}",
        f"remove the playlist {DEBRIS_NAME!r}",
        "remove the playlist 'Untitled Playlist'",
    ]
    assert "Phil's Spotify" not in str(shown) and "Genre Trivia!" not in str(shown)
    (item,) = [one for one in shown["items"] if one["step"] == account_area.ROOT]
    rows = {row["id"]: row for row in item["plan"]}
    assert rows["old-1"]["action"] == "move" and "custom-1" not in rows

    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person"])[0] == 0
    collection.reset_cache()
    code, done = drive(["--run", run_id, *ONLY_ROOT])

    assert code == int(ExitCode.OK), done
    assert held.root_removed == [("debris-1", "debris"), ("debris-2", "debris"), ("empty-1", "empty")]
    applied = _steps(done, account_area.AREA)[account_area.ROOT]["applied"]
    assert [name for _kind, _id, name in applied["removed"]] == [
        DEBRIS_NAME,
        DEBRIS_NAME,
        "Untitled Playlist",
    ]
    assert held.folder_names[held.placed["old-1"]] == "2026"
    assert applied["moved"] == [["old-1", held.placed["old-1"]]]
    # The legacy folder stays through the apply that emptied it, and the
    # label folder, the author's folders and the working custom are untouched.
    assert "hand-legacy" in held.folder_names and held.folders_removed == []
    assert held.placed["year-1"] == "hand-label" and held.playlists["year-1"] == ["t1", "t2", "t3"]
    assert held.placed["spotify-1"] == "hand-spotify" and "custom-1" not in held.placed

    _listing_without_removed(fake, held)
    collection.reset_cache()
    code, second = _two_acts(ONLY_ROOT, ACCOUNT_GATE, "apply")

    assert code == int(ExitCode.OK), second
    assert held.folders_removed == ["hand-legacy"]

    collection.reset_cache()
    code, again = drive([*ONLY_ROOT, "--report"])
    assert code == int(ExitCode.OK), again
    step = _steps(again, account_area.AREA)[account_area.ROOT]
    assert step["state"] == "nothing" and step["plan"] == []


def test_the_full_verb_lists_the_working_custom_and_never_the_root_steps_removals(world):
    _root_world(world)

    envelope = _report()

    area = envelope["data"]["summary"]["areas"][account_area.AREA]
    yours = {one["name"] for one in area["yours"]}
    assert "tech_house_hits - Phil" in yours
    assert not {"Untitled Playlist", DEBRIS_NAME} & yours
    assert _steps(envelope, account_area.AREA)[account_area.ROOT]["state"] == "planned"
    file_rows = _file_rows(envelope)
    assert file_rows["custom-1"]["why"] == filing.WORKING_CUSTOM
    assert file_rows["empty-1"]["why"] == filing.EMPTY
    assert file_rows["debris-1"]["why"] == filing.DEBRIS


def test_an_unread_label_registry_refuses_the_root_step_as_it_refuses_the_filing(world):
    from cratekit.label import registry as labels

    _root_world(world)
    labels.RegistryStore().path.write_text("{ not json", encoding="utf-8")

    step = _steps(_report(), account_area.AREA)[account_area.ROOT]

    assert step["state"] == "refused"


def test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved(world, monkeypatch):
    """U222. The refusal names the step and playlist that moved, and says the plan was rebuilt.

    Sitting 66's refusal named two digests and nothing else, so the sitting
    could not tell a rebuild from a fresh plan, nor which playlist moved.
    """
    _cfg, _fake, held, _inbox, _ids = world
    assert _answered()[0] == int(ExitCode.OK)
    monkeypatch.setattr(rekordbox, "plan_area", _not_planned)
    only = [*VERB, "--only", account_area.MIRROR]
    collection.reset_cache()
    code, refused = drive(only)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    # A person deletes a mirrored INBOX batch's playlist on the account.
    (gone,) = [pid for pid, title in held.titles.items() if title.endswith("Tidal playlists")]
    title = held.titles[gone]
    del held.playlists[gone], held.titles[gone], held.placed[gone]
    asked, created = len(held.matches), list(held.created)

    collection.reset_cache()
    code, done = drive(["--run", run_id, *only])

    assert code == int(ExitCode.DECISION_STALE), done
    cause = done["cause"]
    assert cause["reason"] == "decision-stale"
    assert cause["message"].startswith(
        f"the decision on {ACCOUNT_GATE!r} was made against a plan that has since changed; "
        f"account: moved since the gate showed it: mirror INBOX onto the account, in {title!r}; "
        f"mirror plan frozen: rebuilt from the plan frozen on run {run_id}; mirror plan: "
    ), cause["message"]
    assert cause["detail"]["stale"][0] == (
        f"moved since the gate showed it: mirror INBOX onto the account, in {title!r}"
    )
    assert cause["detail"]["gate"] == ACCOUNT_GATE
    # Said with no row asked again and nothing written.
    assert len(held.matches) == asked and held.created == created


# ---------------------------------------------------------------------------
# R-1334: the answer recorded after a stale refusal is the plan it showed
# ---------------------------------------------------------------------------


def _playlists(items: list[dict]) -> list[str]:
    return [str(item.get("playlist", "")) for step in items for item in step["plan"]]


def test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan(
    world, monkeypatch
):
    """R-1334. The review of U222's drive: the playlist reaches the account only once shown.

    With no frozen plan, a playlist made under a mirrored folder between the
    acts moves the digest. The refusal used to name the two digests alone, and
    a second ``run decide`` bound the moved one, so the resume created a
    playlist no screen had shown.
    """
    from cratekit.cli import gates
    from cratekit.organize import mirror_frozen

    cfg, _fake, held, _inbox, _ids = world
    assert _answered()[0] == int(ExitCode.OK)
    monkeypatch.setattr(mirror_frozen, "load", lambda _cfg, run_id: (None, "none, by the test"))

    code, stale, _asked = _mirror_between_acts(cfg, held, monkeypatch)

    assert code == int(ExitCode.DECISION_STALE), stale
    detail = stale["cause"]["detail"]
    assert detail["gate"] == ACCOUNT_GATE
    assert detail["shown"]["digest"] == detail["actual"]
    assert any(" Made After The Gate" in name for name in _playlists(detail["shown"]["items"]))
    (spec,) = [g for g in registry.entry("organize").gates if g.name == ACCOUNT_GATE]
    assert detail["options"] == list(spec.options)
    assert not any("Made After The Gate" in title for title in held.titles.values())

    run_id = stale["run_id"]
    code, decided = drive(["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    assert gates.load(run_id).decisions[ACCOUNT_GATE].digest == detail["shown"]["digest"]
    collection.reset_cache()
    code, done = drive(["--run", run_id, *VERB, "--only", account_area.MIRROR])

    assert code == int(ExitCode.OK), done
    assert any("Made After The Gate" in title for title in held.titles.values())


def test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing(
    world, monkeypatch
):
    from cratekit.organize import mirror_frozen

    cfg, _fake, held, _inbox, _ids = world
    assert _answered()[0] == int(ExitCode.OK)
    monkeypatch.setattr(mirror_frozen, "load", lambda _cfg, run_id: (None, "none, by the test"))
    code, stale, _asked = _mirror_between_acts(cfg, held, monkeypatch)
    assert code == int(ExitCode.DECISION_STALE), stale
    run_id = stale["run_id"]
    assert drive(["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person"])[0] == 0
    _node(cfg, "Made After The Answer", under=_mirrored_folder(cfg), tracks=("r-one",))
    created = list(held.created)

    collection.reset_cache()
    code, again = drive(["--run", run_id, *VERB, "--only", account_area.MIRROR])

    assert code == int(ExitCode.DECISION_STALE), again
    detail = again["cause"]["detail"]
    assert detail["expected"] == stale["cause"]["detail"]["actual"]
    assert any(" Made After The Answer" in name for name in _playlists(detail["shown"]["items"]))
    assert held.created == created
    assert not any("Made After The" in title for title in held.titles.values())


def test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it(world):
    """R-1334 for the database gate: the batch landed between the acts is on the screen first."""
    from cratekit.cli import gates

    cfg, _fake, _held, inbox, _ids = world
    collection.reset_cache()
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, DB_GATE, "approve", "--actor", "a-person"])[0] == 0
    late = "2026-07-01T101010Z-2_inboxed"
    landed = _node(cfg, late, under=inbox, age=60)
    collection.reset_cache()
    code, stale = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_STALE), stale
    detail = stale["cause"]["detail"]
    assert detail["gate"] == DB_GATE
    assert detail["shown"]["digest"] == detail["actual"]
    assert late in _playlists(detail["shown"]["items"])
    assert _parent(cfg, landed) == inbox

    assert drive(["run", "decide", run_id, DB_GATE, "approve", "--actor", "a-person"])[0] == 0
    assert gates.load(run_id).decisions[DB_GATE].digest == detail["shown"]["digest"]
    collection.reset_cache()
    code, second = drive(["--run", run_id, *VERB])
    # The database answer now holds, and the run goes on to ask the account.
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert second["cause"]["detail"]["gate"] == ACCOUNT_GATE
    assert drive(["run", "decide", run_id, ACCOUNT_GATE, "abort", "--actor", "a-person"])[0] == 0
    collection.reset_cache()
    code, done = drive(["--run", run_id, *VERB])

    assert code == int(ExitCode.OK), done
    assert _parent(cfg, landed) != inbox


# ---------------------------------------------------------------------------
# R-1349: a gate is answered once its run has shown it
# ---------------------------------------------------------------------------


def _account_side(held) -> tuple[list, list, list]:
    return list(held.created), list(held.folders_created), list(held.moves)


def test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing(world):
    """R-1349. The drive that created three folders on the account with no account gate.

    The rekordbox gate open, the account answered ahead of its own gate. The
    answer used to be recorded with no digest, so the resume applied the
    account area unasked. Now the decide is refused, names the gate the run
    waits at and the command that reaches the account gate, and the resume
    after the rekordbox answer stops at the account gate with nothing written.
    """
    from cratekit.cli import gates

    _cfg, _fake, held, _inbox, _ids = world
    before = _account_side(held)
    collection.reset_cache()
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert first["cause"]["detail"]["gate"] == DB_GATE
    run_id = first["run_id"]
    record = gates.load(run_id).to_json()

    code, early = drive(["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person"])

    assert code == int(ExitCode.PRECONDITION), early
    cause = early["cause"]
    assert cause["reason"] == "gate-not-reached"
    assert cause["remediation"]["remedy"] is None
    assert cause["detail"]["gate"] == ACCOUNT_GATE
    assert cause["detail"]["open_gate"] == DB_GATE
    assert cause["detail"]["run_id"] == run_id
    steps = cause["remediation"]["steps"]
    assert f"crate run decide {run_id} {DB_GATE} <option>" in steps[0]
    assert f"crate --run {run_id} organize --as-of {TODAY.isoformat()}" in steps[1]
    # Nothing recorded: the run reads exactly as it did.
    assert gates.load(run_id).to_json() == record

    assert drive(["run", "decide", run_id, DB_GATE, "approve", "--actor", "a-person"])[0] == 0
    collection.reset_cache()
    code, second = drive(["--run", run_id, *VERB])

    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert second["cause"]["detail"]["gate"] == ACCOUNT_GATE
    assert _account_side(held) == before


def test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs(world):
    """``--continue`` does not carry an early answer past the gate it was refused at."""
    _cfg, _fake, held, _inbox, _ids = world
    before = _account_side(held)
    collection.reset_cache()
    code, first = drive(VERB)
    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, DB_GATE, "approve", "--actor", "a-person"])[0] == 0
    reached = _parent(_cfg, _ids["batch"])

    # The run waits at nothing now (the database answer is recorded, the
    # account gate not reached), so the refusal names the run to continue.
    code, early = drive(
        ["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person", "--continue"]
    )

    assert code == int(ExitCode.PRECONDITION), early
    assert early["cause"]["reason"] == "gate-not-reached"
    assert early["cause"]["detail"]["open_gate"] is None
    (step, *_rest) = early["cause"]["remediation"]["steps"]
    assert f"crate --run {run_id} organize --as-of {TODAY.isoformat()}" in step
    # The verb did not run: no rekordbox write, nothing on the account.
    assert _parent(_cfg, _ids["batch"]) == reached
    assert _account_side(held) == before


def test_an_account_answer_after_its_gate_is_shown_binds_the_digest_it_showed(world):
    from cratekit.cli import gates

    collection.reset_cache()
    code, first = drive(VERB)
    run_id = first["run_id"]
    assert drive(["run", "decide", run_id, DB_GATE, "approve", "--actor", "a-person"])[0] == 0
    collection.reset_cache()
    code, second = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    shown = second["cause"]["detail"]["shown"]["digest"]

    code, decided = drive(["run", "decide", run_id, ACCOUNT_GATE, "apply", "--actor", "a-person"])

    assert code == int(ExitCode.OK), decided
    assert gates.load(run_id).decisions[ACCOUNT_GATE].digest == shown


def test_a_gate_with_no_digest_source_still_takes_an_answer_before_it_is_reached(world):
    """The cloud sync gate binds no plan, so an answer ahead of it is what it always was."""
    from cratekit.cli import gates

    (cloud,) = [g for g in registry.entry("organize").gates if g.name == "write.cloudsync.unreadable"]
    assert cloud.digest_source is None
    collection.reset_cache()
    code, first = drive(VERB)
    run_id = first["run_id"]

    code, decided = drive(["run", "decide", run_id, cloud.name, "abort", "--actor", "a-person"])

    assert code == int(ExitCode.OK), decided
    state = gates.load(run_id)
    assert state.decisions[cloud.name].option == "abort"
    assert state.decisions[cloud.name].digest is None
    assert state.open_gate == DB_GATE


def test_an_answer_ahead_of_a_gate_the_continue_may_not_reach_promises_no_stop_there(world):
    """Round one's drive: the acknowledgment lapsed, so the rekordbox area refuses before it plans.

    The run stops at the account gate alone, and a decide on the rekordbox
    gate is refused. Its steps used to promise that the continued run stops at
    the rekordbox gate with its plan on the screen, and it never does: the
    area refuses again, and the decide those steps end on is refused again.
    """
    cfg, _fake, _held, _inbox, _ids = world
    session.ack_path(cfg).unlink()
    collection.reset_cache()
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert first["cause"]["detail"]["gate"] == ACCOUNT_GATE
    run_id = first["run_id"]

    code, early = drive(["run", "decide", run_id, DB_GATE, "approve", "--actor", "a-person"])

    assert code == int(ExitCode.PRECONDITION), early
    steps = early["cause"]["remediation"]["steps"]
    assert not any(f"stops at {DB_GATE}" in step for step in steps)
    assert any("its report says why if it does not" in step for step in steps)
    assert drive(["run", "decide", run_id, ACCOUNT_GATE, "abort", "--actor", "a-person"])[0] == 0
    collection.reset_cache()
    code, done = drive(["--run", run_id, *VERB])
    # The continue reaches no rekordbox gate, and says why.
    assert code == int(ExitCode.OK), done
    assert done["data"]["summary"]["areas"][rekordbox.AREA]["refused"]["reason"] == (
        "backup-acknowledgment-missing"
    )
