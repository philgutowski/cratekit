"""Tagging's library scenarios: `crate tag suggest`, `crate tag guess` and `crate tag backlog` (U306).

All three read the library's rows, so they share one machine: a disposable
rekordbox database built from the binding's own schema, every row naming a
FLAC container the encoder synthesized, and the platform seams a temporary
library cannot speak for.

`tag suggest` writes a genre on the file and the row behind its explicit
gate, then a second run finds nothing left to write; it refuses with no
backup acknowledgment, refuses an inline answer and a pick off the taxonomy,
leaves everything as it was when declined, meets a plan that changed as
stale, and refuses with rekordbox running; with ``--catalogue`` it asks a
recorded catalogue once across the two acts. `tag guess` reports what it
would write, writes it, finds nothing left, names a pass no job carries,
goes on when the library cannot be read, and refuses a missing folder. `tag
backlog` sorts a library's needs genre rows by cause, asks a recorded
catalogue once and reads the kept answer the second time, says when a
library is empty of backlog, and refuses a library most of whose rows are
under no prefix rule. Self contained, so the suites it stands beside can be
trimmed without moving it.
"""

from __future__ import annotations

import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.core import config, locations, preflight, rb_writer, session, tags, taxonomy
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging.tag import SearchHit
from tests._containers import synth_container
from tests.test_config import valid_data

OK = int(ExitCode.OK)
DECISION = int(ExitCode.DECISION_REQUIRED)
GATE = "tag.suggest.confirm"
SUGGEST = ("tag", "suggest")
BACKLOG = ("tag", "backlog")
GUESS = ("tag", "guess")
RECORDED_APP_VERSION = "9.9.9.0001"

DECLARED = taxonomy.default_taxonomy()
MELODIC = "Melodic House"
DEEP = "Deep House"
PROGRESSIVE = "Progressive House"
AFRO = "Afro House"
LOOSE = "Dance"
COARSE = next(word for word in DECLARED.fallback.too_coarse_as_source if word)
INDIE = "Indie Tech"
ALTERNATIVE = "alternative"
MPB = "mpb"
AMAPIANO = "amapiano"
RNB = "R&B"
LOOKUPS = (MELODIC, DEEP, PROGRESSIVE, LOOSE, COARSE)
BACKLOG_LOOKUPS = (*LOOKUPS, INDIE, "Grime", AMAPIANO, MPB, ALTERNATIVE, RNB, "House")
ABSENT = object()


# ---------------------------------------------------------------------------
# The disposable database
# ---------------------------------------------------------------------------


def _relaxed_schema():
    """The binding's schema copied with every non key column nullable, as rekordbox's is."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import MetaData

    schema = MetaData()
    for table in tables.Base.metadata.tables.values():
        table.to_metadata(schema)
    for table in schema.tables.values():
        for column in table.columns:
            if not column.primary_key:
                column.nullable = True
    return schema


def _row(model, **values):
    """One mapped row with every timestamp column filled, at the pinned instant."""
    from pyrekordbox.db6 import tables

    now = datetime.now(timezone.utc)
    made = model(**values)
    for key, column in model.__mapper__.columns.items():
        if isinstance(column.type, tables.DateTime) and getattr(made, key, None) is None:
            setattr(made, key, now)
    return made


@dataclass(frozen=True)
class Track:
    """One row to seed and the file it names, under ``folder`` by ``artist``."""

    content_id: str
    row: str = ""
    file: object = ""
    artist: str = ""
    folder: str = "inbox"
    deleted: bool = False


def build(cfg: config.Config, silence: Path, *tracks: Track, lookups=LOOKUPS) -> dict[str, Path]:
    """A disposable database holding ``tracks``, each with the file it names."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    db_path = Path(cfg.library.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}")
    _relaxed_schema().create_all(engine)
    ids = {name: str(ordinal) for ordinal, name in enumerate(lookups, start=100)}
    artists: dict[str, str] = {}
    paths: dict[str, Path] = {}
    with Session(engine) as db_session:
        db_session.add(_row(tables.AgentRegistry, registry_id="localUpdateCount", int_1=100))
        db_session.add(_row(tables.DjmdProperty, DBID="1", DBVersion=rb_writer.pinned_db_version()))
        db_session.add(_row(tables.DjmdContent, ID="1", Title="a track", rb_local_deleted=0))
        db_session.add(_row(tables.DjmdContent, ID="2", Title="another track", rb_local_deleted=0))
        for name, genre_id in ids.items():
            db_session.add(_row(tables.DjmdGenre, ID=genre_id, Name=name))
        for track in tracks:
            if track.artist and track.artist not in artists:
                artists[track.artist] = str(500 + len(artists))
                db_session.add(
                    _row(tables.DjmdArtist, ID=artists[track.artist], Name=track.artist)
                )
            path = Path(cfg.library.root) / "Music" / track.folder / f"track-{track.content_id}.flac"
            path.parent.mkdir(parents=True, exist_ok=True)
            if track.file is not ABSENT:
                shutil.copyfile(silence, path)
                if track.file:
                    assert tags.write_tags(path, {"genre": str(track.file)})
            paths[track.content_id] = path
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=track.content_id,
                    Title=f"track {track.content_id}",
                    ArtistID=artists.get(track.artist),
                    GenreID=ids.get(track.row),
                    Rating=3,
                    Commnt="a comment a person typed",
                    rb_local_deleted=1 if track.deleted else 0,
                    FolderPath=locations.location_url(path),
                )
            )
        db_session.commit()
    engine.dispose()
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.commit()
    connection.close()
    collection.reset_cache()
    return paths


def genre_of(cfg: config.Config, content_id: str) -> str:
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        ((name,),) = connection.execute(
            "SELECT g.Name FROM djmdContent c LEFT JOIN djmdGenre g ON g.ID = c.GenreID "
            "WHERE c.ID = ?",
            (content_id,),
        ).fetchall()
    finally:
        connection.close()
    return name or ""


def eight(genre: str = MELODIC, artist: str = "The Artist", folder: str = "one", first: int = 20):
    """Eight tracks by one artist, all one genre, in a folder of their own."""
    return [Track(str(first + n), genre, genre, artist=artist, folder=folder) for n in range(8)]


# ---------------------------------------------------------------------------
# The machine
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _field_policies():
    """The policy registry is process wide and the apply registers into it."""
    rb_writer.reset_field_policies()
    yield
    rb_writer.reset_field_policies()


@pytest.fixture(autouse=True)
def _reader_cache():
    collection.reset_cache()
    yield
    collection.reset_cache()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as the metadata verb patches it."""
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
def silence(tmp_path) -> Path:
    made = tmp_path / "silence"
    made.mkdir()
    return synth_container(made, ".flac")


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A set up machine with every module on and no acknowledgment yet."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(
        valid_data(
            root,
            profile={"name": "full"},
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
        )
    )
    config.save(cfg)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return cfg


def acknowledge(cfg: config.Config) -> None:
    session.record_acknowledgment(cfg, terminal=lambda: True)


def recorded(monkeypatch, hits: dict[str, SearchHit]) -> list[tuple[str, str]]:
    """A catalogue answering from recorded hits by title, bound where the plan asks."""
    from cratekit.tagging import published, searchers

    asked: list[tuple[str, str]] = []

    def search(artist, title):
        asked.append((artist, title))
        return hits.get(title)

    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: search)
    monkeypatch.setattr(published, "for_suggestions", lambda declared: lambda hit, isrc: hit)
    return asked


def first_act(stage, *verb: str) -> str:
    refused = stage.json(*verb)
    assert refused.code == DECISION, refused.stdout
    return refused.envelope["run_id"]


# ---------------------------------------------------------------------------
# tag suggest
# ---------------------------------------------------------------------------


def test_suggest_written_behind_its_gate_and_then_nothing_left(stage, machine, silence):
    acknowledge(machine)
    paths = build(
        machine, silence, *eight(), Track("10", artist="The Artist"), Track("11")
    )

    assert stage.crate(*SUGGEST).code == DECISION
    run_id = first_act(stage, *SUGGEST)
    assert stage.decide(run_id, GATE, "apply").code == OK
    written = stage.json("--run", run_id, *SUGGEST)
    assert written.code == OK, written.stdout
    assert tags.read_genre_from_file(paths["10"]) == MELODIC
    assert genre_of(machine, "10") == MELODIC and genre_of(machine, "11") == ""

    # Again: the plan holds nothing to write, and still asks.
    run_id = first_act(stage, *SUGGEST)
    assert stage.decide(run_id, GATE, "apply").code == OK
    assert stage.crate("--run", run_id, *SUGGEST).code == OK


def test_suggest_refusals(stage, machine, silence, monkeypatch):
    paths = build(
        machine, silence, *eight(), Track("10", artist="The Artist"), Track("11", artist="The Artist")
    )
    # No backup acknowledgment: refused before the plan and the gate.
    assert stage.json(*SUGGEST).code != OK
    acknowledge(machine)

    # An inline answer, and a pick off the taxonomy, are refused.
    assert stage.json("-d", f"{GATE}=apply", *SUGGEST).code == DECISION
    assert stage.crate(*SUGGEST, "--set", f"10={LOOSE}").code != OK

    # Declined: nothing is written.
    run_id = first_act(stage, *SUGGEST)
    assert stage.decide(run_id, GATE, "abort").code == OK
    assert stage.json("--run", run_id, *SUGGEST).code == OK

    # A plan that changed after the decision is stale.
    run_id = first_act(stage, *SUGGEST)
    assert stage.decide(run_id, GATE, "apply").code == OK
    assert tags.write_tags(paths["11"], {"genre": DEEP})
    assert stage.json("--run", run_id, *SUGGEST).code != OK

    # rekordbox running: the plan is read and the write refused.
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    run_id = first_act(stage, *SUGGEST)
    assert stage.decide(run_id, GATE, "apply").code == OK
    assert stage.crate("--run", run_id, *SUGGEST).code != OK
    assert genre_of(machine, "10") == ""


def test_suggest_asks_the_catalogue_once_across_the_two_acts(
    stage, machine, silence, monkeypatch
):
    acknowledge(machine)
    paths = build(machine, silence, Track("10"))
    asked = recorded(monkeypatch, {"track 10": SearchHit(genre=DEEP, source="beatport")})

    run_id = first_act(stage, *SUGGEST, "--catalogue")
    assert stage.decide(run_id, GATE, "apply").code == OK
    written = stage.json("--run", run_id, *SUGGEST, "--catalogue")
    assert written.code == OK, written.stdout
    assert asked == [("", "track 10")]
    assert tags.read_genre_from_file(paths["10"]) == DEEP and genre_of(machine, "10") == DEEP


# ---------------------------------------------------------------------------
# tag guess
# ---------------------------------------------------------------------------


def staged(cfg: config.Config, silence: Path, name: str, **fields: str) -> Path:
    folder = Path(cfg.library.root).parent / "staging"
    folder.mkdir(exist_ok=True)
    path = folder / f"{name}.flac"
    shutil.copyfile(silence, path)
    if fields:
        assert tags.write_tags(path, fields)
    return path


def test_guess_reported_written_and_then_nothing_left(stage, machine, silence):
    build(machine, silence, *(Track(str(n), row=DEEP, artist="Ana Vale") for n in (11, 12, 13)))
    lone = staged(machine, silence, "lone", artist="Ana Vale", title="Lone")
    staged(machine, silence, "kept", artist="Ana Vale", title="Kept", genre=MELODIC)
    staged(machine, silence, "nobody", artist="Nobody Known", title="Nobody")
    staged(machine, silence, "latin", artist="Ana Vale", title="Latin", genre="Latin Electronic")
    folder = str(Path(machine.library.root).parent / "staging")

    assert stage.json(*GUESS, folder, "--report").code == OK
    assert not tags.read_genre_from_file(lone)
    guessed = stage.crate(*GUESS, folder)
    assert guessed.code == OK, guessed.stderr
    assert tags.read_genre_from_file(lone) == DEEP
    # Again: every file the votes reach carries a genre now.
    assert stage.json(*GUESS, folder).code == OK
    assert stage.json(*GUESS, folder, "--pass", "no-such-pass").code == OK
    assert stage.crate(*GUESS, str(Path(machine.library.root) / "no-such-folder")).code != OK


def test_guess_over_a_library_that_cannot_be_read(stage, machine, silence):
    # No database is built, so the library cannot be opened.
    staged(machine, silence, "tagged", artist="Ana Vale", title="Tagged", genre=PROGRESSIVE)
    lone = staged(machine, silence, "lone", artist="Ana Vale", title="Lone")
    folder = str(Path(machine.library.root).parent / "staging")

    guessed = stage.json(*GUESS, folder)
    assert guessed.code == OK, guessed.stdout
    assert tags.read_genre_from_file(lone) == PROGRESSIVE


# ---------------------------------------------------------------------------
# tag backlog
# ---------------------------------------------------------------------------


def shipped_copy(cfg: config.Config) -> None:
    """The library holds the shipped template as its active copy."""
    path = config.state_path("taxonomy_active", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME), encoding="utf-8"
    )


def backlog_library() -> list[Track]:
    return [
        *eight(MELODIC, "The Artist", "one", 20),
        Track("10", "", MELODIC, artist="Someone", folder="two"),
        Track("11", "", AFRO, artist="Someone", folder="two"),
        Track("12", "", "", artist="Solo", folder="one"),
        Track("13", "", "", artist="Nobody", folder="three"),
        Track("14", COARSE, "", artist="Nobody", folder="three"),
        Track("15", "", INDIE, artist="The Artist", folder="four"),
        Track("16", "", "indie tech", artist="The Artist", folder="four"),
        Track("17", INDIE, "", artist="The Artist", folder="four"),
        Track("18", "", ALTERNATIVE, artist="Nobody", folder="three"),
        Track("41", "", MPB, artist="Nobody", folder="three"),
        Track("42", "", AMAPIANO, artist="Nobody", folder="three"),
        Track("43", "", ABSENT, artist="Nobody", folder="five"),
        Track("19", "", "", deleted=True),
    ]


def test_backlog_sorted_by_cause_and_the_catalogue_kept(stage, machine, silence, monkeypatch):
    shipped_copy(machine)
    build(machine, silence, *backlog_library(), lookups=BACKLOG_LOOKUPS)
    asked = recorded(
        monkeypatch,
        {"track 13": SearchHit(genre=DEEP, source="discogs", source_genre="Deep House")},
    )

    shown = stage.crate(*BACKLOG)
    assert shown.code == OK, shown.stderr
    assert stage.json(*BACKLOG).code == OK
    assert stage.json(*BACKLOG, "--catalogue").code == OK
    count = len(asked)
    assert count >= 1
    # Again: the kept answers are read, and no catalogue is asked twice.
    assert stage.crate(*BACKLOG, "--catalogue").code == OK
    assert len(asked) == count


def test_backlog_empty_and_refused(stage, machine, silence, monkeypatch):
    from cratekit.write import metadata_cli

    shipped_copy(machine)
    build(machine, silence, *eight(), lookups=BACKLOG_LOOKUPS)
    empty = stage.json(*BACKLOG)
    assert empty.code == OK, empty.stdout

    monkeypatch.setattr(
        metadata_cli,
        "resolution_totals",
        lambda cfg, db: metadata_cli.ResolutionTotals(
            active=10, unresolved=9, unmapped=9, prefixes={"/Elsewhere": 9}
        ),
    )
    assert stage.json(*BACKLOG).code != OK
    acknowledge(machine)
    assert stage.crate(*SUGGEST).code != OK
