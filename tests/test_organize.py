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
from cratekit.organize import filing, own, rekordbox
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
    # THE AUTHOR'S OWN ON THE ACCOUNT IS FILED IN MINE (U131), on the gate, so
    # it is a move of the filing step and no longer a listing.
    assert MINE_ON_ACCOUNT not in mine_account
    # The set the product made is listed by the account and is not the author's.
    assert SET_NAME not in mine_account
    # The run named batch is a suggestion, never a step.
    assert [one["name"] for one in areas[rekordbox.AREA]["suggested"]] == [RUN_NAMED]

    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert ("mine-1", MINE_ON_ACCOUNT) not in held.renamed
    assert held.folder_names[held.placed["mine-1"]] == "Mine"
    assert _parent(cfg, ids["mine"]) in rb_writer.ROOT_PARENT_SENTINELS
    assert _parent(cfg, ids["listen later"]) == inbox
    for area in done["data"]["summary"]["areas"].values():
        for step in area["steps"]:
            if step["step"] == account_area.FILE:
                # THE FILING STEP NAMES EVERY PLAYLIST AT THE ROOT (U116), and an
                # unmarked one of the author's is moved into Mine (U131), with why.
                (row,) = [one for one in step["plan"] if one["name"] == MINE_ON_ACCOUNT]
                assert row["action"] == filing.MOVE and row["why"] == filing.UNMARKED
                assert row["kind_folder"] == "Mine"
                continue
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
    # The author's own is filed in Mine (U131), and so is a move, not a listing.
    assert MINE_ON_ACCOUNT not in mine
    assert _file_rows(_report())["exported-1"]["kind_folder"] == "Exports"


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
    assert [MARKED_ID, folder] in applied["moved"]
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


def test_an_unmarked_playlist_of_the_authors_is_filed_in_mine(world):
    _cfg, _fake, held, _inbox, _ids = world

    row = _file_rows(_report())["mine-1"]

    assert row["action"] == filing.MOVE and row["why"] == filing.UNMARKED
    assert row["kind_folder"] == "Mine" and row["folder"] == "create"
    code, done, _first = _answered()
    assert code == int(ExitCode.OK), done
    assert held.folder_names[held.placed["mine-1"]] == "Mine"


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


def test_a_mark_with_no_year_is_left_and_the_year_is_local():
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
    # Only the author's own playlist's Mine folder is made, never the year's.
    assert held.folders_created == ["Mine"]


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
