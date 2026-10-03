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
from cratekit.organize import own, rekordbox
from tests import adopt_fixtures, cutover_fixtures, outbound_fakes
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
        "listen later": _node(cfg, "listen later", under=inbox, age=5),
        "mine": _node(cfg, MINE_IN_REKORDBOX, under=None),
    }
    register(LABEL)
    tracklist = Path(cfg.library.root).parent / "lists" / f"{SET_NAME}.txt"
    tracklist.parent.mkdir(parents=True, exist_ok=True)
    tracklist.write_text("".join(f"{a} - {t}\n" for a, t in ROWS), encoding="utf-8")
    code, built = _two_acts(["export", "set", str(tracklist)], SET_BUILD)
    assert code == int(ExitCode.OK), built
    _proof(cfg, SET_NAME)
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
    """Every live membership outside INBOX, as content identifiers."""
    rows = _query(
        cfg,
        "SELECT s.ContentID, p.Name FROM djmdSongPlaylist s JOIN djmdPlaylist p "
        "ON p.ID = s.PlaylistID WHERE COALESCE(s.rb_local_deleted, 0) = 0",
    )
    return sorted(str(content) for content, name in rows if name != RUN_NAMED)


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
    assert mine_db[MINE_IN_REKORDBOX]["suggested_home"] == f"{DECLARED.catalog.display} / {LABEL}"
    assert mine_db["listen later"]["suggested_home"] is None
    mine_account = {one["name"]: one for one in areas[account_area.AREA]["yours"]}
    assert mine_account[MINE_ON_ACCOUNT]["suggested_home"] == "the 2024 year folder"
    # The set the product made is not the author's.
    assert SET_NAME not in mine_account
    # The run named batch is a suggestion, never a step.
    assert [one["name"] for one in areas[rekordbox.AREA]["suggested"]] == [RUN_NAMED]

    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert ("mine-1", MINE_ON_ACCOUNT) not in held.renamed
    assert "mine-1" not in held.placed
    assert _parent(cfg, ids["mine"]) in rb_writer.ROOT_PARENT_SENTINELS
    assert _parent(cfg, ids["listen later"]) == inbox
    for area in done["data"]["summary"]["areas"].values():
        for step in area["steps"]:
            assert MINE_ON_ACCOUNT not in str(step["plan"])
            assert MINE_IN_REKORDBOX not in str(step["plan"])


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
    assert any(name.startswith("DOWNLOADED ") for _pid, name in held.renamed)


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
