"""U113: a playlist the author made on the account lands as its own INBOX playlist.

Driven on the xml bridge over a pass whose jobs are queued the way ``crate
sync all`` queues them and run by the real worker, so the landing reads the
reports the product writes. D1 applies: no real person or track is named.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import account_playlists, batch_name, ingest, missing_cli
from cratekit.intake import cli as intake_cli
from cratekit.sync import playlists
from tests.test_intake_land import GATE, _drive, _land, _manifest, _music, _stage
from tests.test_intake_land import cfg as cfg  # noqa: PLC0414 - the fixture, re-exported
from tests.test_intake_land import export as export  # noqa: PLC0414 - the fixture
from tests.test_intake_land_account_playlists_native import (  # noqa: PLC0414 - made once
    silence as silence,
)
from tests.test_sync_all import _playlist, _playlist_jobs, _tracks, bind_playlists
from tests.test_sync_all import slim as slim  # noqa: PLC0414 - the fixture

DAY = date(2026, 10, 3)
RUN = "2026-10-03T101500Z-cd34"
PASS = missing_cli.synced_name(RUN)
BATCH = "2026-10-03 Tidal playlists"
INBOX_NODE = '<NODE Name="INBOX" Type="0" Count="0">'


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


def _track(title: str) -> dict:
    """One frozen track as a sweep freezes it, keyed by a provider id of its own."""
    return {"artist": "Probe", "title": title, "origin": match.TIDAL, "ref": f"tid-{title}"}


def swept(
    cfg: config.Config,
    listed: dict[str, tuple[str | None, tuple[str, ...]]],
    *,
    run_id: str = RUN,
    source_id: str = playlists.SOURCE_ID,
) -> list[jobs.Job]:
    """One job per playlist, ``id -> (account name, titles)``, queued as a sweep does and run.

    The library holds none of the titles, so every report says missing.
    """
    with jobs.open_store() as store:
        queued = [
            intake_cli.queue_playlist(
                store,
                cfg,
                handler_key="intake.playlist",
                reference=playlist_id,
                tracks={f"tid-{title}": _track(title) for title in titles},
                run_id=run_id,
                source_id=source_id,
                name=name,
            )
            for playlist_id, (name, titles) in listed.items()
        ]
    for job in queued:
        code, resumed = _drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), resumed
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    return queued


def _staged(cfg: config.Config, silence: Path, *titles: str) -> None:
    for title in titles:
        _stage(cfg, silence, f"{title}.flac")


def _applied(export: Path, *extra: str) -> dict:
    code, envelope = _drive(["-d", f"{GATE}=apply", *_land(export, *extra)])
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    return envelope


def _inbox(intake: Path) -> dict[str, list[str]]:
    """Every playlist under the intake file's INBOX and the track names it holds."""
    body = intake.read_text(encoding="utf-8")
    names = {}
    for line in body.splitlines():
        if "<TRACK TrackID=" in line and 'Name="' in line:
            tid = line.split('TrackID="', 1)[1].split('"', 1)[0]
            names[tid] = line.split(' Name="', 1)[1].split('"', 1)[0]
    inbox = body[body.index('<NODE Name="INBOX"') :]
    held: dict[str, list[str]] = {}
    current = None
    for line in inbox.splitlines():
        if 'Type="1"' in line:
            current = line.split('Name="', 1)[1].split('"', 1)[0]
            held[current] = []
        elif "<TRACK Key=" in line and current is not None:
            held[current].append(names[line.split('Key="', 1)[1].split('"', 1)[0]])
    return held


def _intake(envelope: dict) -> Path:
    return Path(envelope["pending_human_action"]["artifact"])


def _held(envelope: dict) -> dict[str, list[str]]:
    return _inbox(_intake(envelope))


def _written(envelope: dict) -> list[dict]:
    return [item for item in envelope["data"]["items"] if item["action"] == "playlist"]


def _left(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == account_playlists.LEFT_OUT]


def _inbox_holds(export: Path, name: str) -> None:
    """Rewrite ``export`` so its INBOX holds a playlist of ``name``."""
    body = export.read_text(encoding="utf-8").replace(
        INBOX_NODE,
        '<NODE Name="INBOX" Type="0" Count="1">\r\n'
        f'        <NODE Name="{name}" Type="1" KeyType="0" Entries="0">\r\n'
        "        </NODE>",
    )
    export.write_text(body, encoding="utf-8")


def _renumber_held1(held: Path) -> None:
    """Held1's entry is renumbered, as a later export of the collection can do."""
    body = held.read_text(encoding="utf-8")
    tid = body.split('Name="Held1"', 1)[0].rsplit('TrackID="', 1)[1].split('"', 1)[0]
    held.write_text(body.replace(f'TrackID="{tid}"', 'TrackID="98765"'), encoding="utf-8")


def _decided(argv: list[str]) -> dict:
    """The first act refused at the gate, and a person's answer recorded."""
    code, refused = _drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    _drive(["run", "decide", refused["run_id"], GATE, "apply", "--actor", "a-person"])
    return refused


# ---------------------------------------------------------------------------
# The scenarios the brief names
# ---------------------------------------------------------------------------


def test_two_swept_playlists_land_as_two_inbox_playlists_under_their_exact_names(
    cfg, silence, export
):
    """A track both playlists brought in is a member of both."""
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Two")), "pl-b": ("Deep Cuts", ("Three", "Two"))})
    _staged(cfg, silence, "One", "Two", "Three")
    envelope = _applied(export, "--pass", PASS)
    # The files still land in the one batch folder U110 names.
    assert sorted(p.name for p in _music(cfg, BATCH).iterdir()) == [
        "One.flac",
        "Three.flac",
        "Two.flac",
    ]
    # Only the playlists split, and the batch playlist, holding nothing, is not written.
    assert _held(envelope) == {
        "Sunset Warmup 2026-10-03": ["One", "Two"],
        "Deep Cuts 2026-10-03": ["Three", "Two"],
    }
    assert _written(envelope) == [
        {"action": "playlist", "playlist": "Sunset Warmup 2026-10-03", "account": "pl-a", "count": 2},
        {"action": "playlist", "playlist": "Deep Cuts 2026-10-03", "account": "pl-b", "count": 2},
    ]


def test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date(
    cfg, silence, export, monkeypatch
):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _staged(cfg, silence, "One")
    first = _intake(_applied(export, "--pass", PASS))
    # A week on: the next pass of the same playlist, landed against an export
    # that holds the first landing's playlist under INBOX, as one taken after
    # its import does.
    run = "2026-10-10T101500Z-ef56"
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Two",))}, run_id=run)
    _staged(cfg, silence, "Two")
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 10))
    held = _held(_applied(first, "--pass", missing_cli.synced_name(run)))
    assert held["Sunset Warmup 2026-10-03"] == ["One"]
    # Its own landing's date tells the two passes apart, so no `` 2`` is needed.
    assert held["Sunset Warmup 2026-10-10"] == ["Two"]
    assert "Sunset Warmup 2026-10-03 2" not in held


def test_a_name_an_unimported_intake_file_holds_is_not_given_again(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _staged(cfg, silence, "One")
    _applied(export, "--pass", PASS)
    # The first intake file is still waiting on its import, so the export the
    # second landing is handed holds neither of its playlists.
    run = "2026-10-03T201500Z-ab78"
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Two",))}, run_id=run)
    _staged(cfg, silence, "Two")
    envelope = _applied(export, "--pass", missing_cli.synced_name(run))
    assert _held(envelope) == {"Sunset Warmup 2026-10-03 2": ["Two"]}


def test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there(cfg, silence, export):
    body = export.read_text(encoding="utf-8").replace(
        INBOX_NODE,
        '<NODE Name="Sunset Warmup 2026-10-03" Type="1" KeyType="0" Entries="0">\r\n'
        f"      </NODE>\r\n      {INBOX_NODE}",
    )
    export.write_text(body, encoding="utf-8")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _staged(cfg, silence, "One")
    envelope = _applied(export, "--pass", PASS)
    assert _held(envelope) == {"Sunset Warmup 2026-10-03 2": ["One"]}


def test_a_label_landing_keeps_the_name_u110_gives_it(cfg, silence, export, tmp_path):
    _staged(cfg, silence, "One")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
    envelope = _applied(export, "--manifest", str(manifest))
    assert _music(cfg, "2026-10-03 Kompakt").is_dir()
    assert next(iter(_held(envelope))) == "2026-10-03 Kompakt"
    assert not _written(envelope)


# ---------------------------------------------------------------------------
# What stays as it was, and what the batch playlist keeps
# ---------------------------------------------------------------------------


def test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    swept(cfg, {"favorites": (None, ("Hearted",))}, source_id=intake_cli.FAVORITES_SOURCE_ID)
    _staged(cfg, silence, "One", "Hearted")
    envelope = _applied(export, "--pass", PASS)
    batch = "2026-10-03 Tidal playlists and Favorites"
    assert _held(envelope) == {batch: ["Hearted"], "Sunset Warmup 2026-10-03": ["One"]}
    steps = " ".join(envelope["pending_human_action"]["steps"])
    assert f"each of the {batch} and Sunset Warmup 2026-10-03 playlists" in steps


def test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before(cfg, silence, export):
    swept(cfg, {"pl-a": (None, ("One",))})
    _staged(cfg, silence, "One")
    envelope = _applied(export, "--pass", PASS)
    assert _held(envelope) == {BATCH: ["One"]}
    assert not _written(envelope)


def test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two(cfg, silence, export):
    """A batch named by hand can be the dated name; the account playlist never merges into it."""
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    swept(cfg, {"favorites": (None, ("Hearted",))}, source_id=intake_cli.FAVORITES_SOURCE_ID)
    _staged(cfg, silence, "One", "Hearted")
    envelope = _applied(export, "--pass", PASS, "--name", "Sunset Warmup 2026-10-03")
    assert _held(envelope) == {
        "Sunset Warmup 2026-10-03": ["Hearted"],
        "Sunset Warmup 2026-10-03 2": ["One"],
    }


def test_a_landing_with_no_pass_splits_nothing(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _staged(cfg, silence, "One")
    envelope = _applied(export, "--name", "by hand")
    assert _held(envelope) == {"by hand": ["One"]}


def test_an_owned_track_whose_row_the_export_does_not_hold_is_warned(cfg, silence, export):
    # The library holds the file and the export the batch is spliced into has
    # no entry for it, so there is no TrackID for the playlist to name: the
    # track is left, and the landing names it rather than dropping it (U128).
    owned = _music(cfg, "older batch")
    owned.mkdir(parents=True)
    _stage(cfg, silence, "Held.flac").rename(owned / "Held.flac")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Held"))})
    _staged(cfg, silence, "One")
    envelope = _applied(export, "--pass", PASS)
    assert _held(envelope) == {"Sunset Warmup 2026-10-03": ["One"]}
    (warning,) = _left(envelope)
    assert "Sunset Warmup 2026-10-03 2. Probe - Held" in warning["message"]
    assert account_playlists.NO_ROW in warning["message"]


# ---------------------------------------------------------------------------
# U128: the INBOX playlist mirrors the whole account playlist
# ---------------------------------------------------------------------------


def _owned_export(cfg, silence, export: Path, titles: tuple[str, ...]) -> Path:
    """The intake file of an earlier landing of ``titles``, as the export taken after its import."""
    _staged(cfg, silence, *titles)
    return _intake(_applied(export, "--name", "older batch"))


def test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order(
    cfg, silence, export
):
    """And an owned track in two account playlists is in both."""
    held = _owned_export(cfg, silence, export, ("Held1", "Held2", "Held3"))
    swept(
        cfg,
        {
            "pl-a": ("Sunset Warmup", ("Held1", "New1", "Held2", "New2", "Held3")),
            "pl-b": ("Deep Cuts", ("New1", "Held1")),
        },
    )
    _staged(cfg, silence, "New1", "New2")
    envelope = _applied(held, "--pass", PASS)
    inbox = _held(envelope)
    assert inbox["Sunset Warmup 2026-10-03"] == ["Held1", "New1", "Held2", "New2", "Held3"]
    assert inbox["Deep Cuts 2026-10-03"] == ["New1", "Held1"]
    # The owned tracks are the export's own entries, not spliced a second time.
    assert _intake(envelope).read_text(encoding="utf-8").count('Name="Held1"') == 1
    assert _written(envelope)[0] == {
        "action": "playlist",
        "playlist": "Sunset Warmup 2026-10-03",
        "account": "pl-a",
        "count": 5,
    }
    assert not _left(envelope)


def test_a_track_neither_owned_nor_brought_is_named_in_the_warnings(cfg, silence, export):
    # The download for Gone never arrived, a lossy file refused or a row
    # nothing answered, so the library does not hold it and the landing did
    # not bring it.
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Gone"))})
    _staged(cfg, silence, "One")
    envelope = _applied(export, "--pass", PASS)
    assert _held(envelope) == {"Sunset Warmup 2026-10-03": ["One"]}
    (warning,) = _left(envelope)
    assert "Sunset Warmup 2026-10-03 2. Probe - Gone" in warning["message"]
    assert account_playlists.NOT_BROUGHT in warning["message"]


def test_a_rerun_of_the_same_pass_is_a_no_op(cfg, silence, export):
    """The intake file's record names the account and the pass, which the rerun reads."""
    held = _owned_export(cfg, silence, export, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1", "Late"))})
    _staged(cfg, silence, "New1")
    first = _intake(_applied(held, "--pass", PASS))
    before = first.read_bytes()
    code, again = _drive(["-d", f"{GATE}=apply", *_land(first, "--pass", PASS)])
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op", again
    assert again["data"]["items"] == []
    assert first.read_bytes() == before
    assert account_playlists.mirrored(cfg, PASS) == frozenset({"pl-a"})
    assert account_playlists.mirrored(cfg, "another pass") == frozenset()
    # A second landing of the pass, with the late file staged, claims only it.
    late = _stage(cfg, silence, "Late.flac")
    (claim,) = account_playlists.split(cfg, PASS, [late])
    assert claim.files == (late,)
    assert claim.left == ()


def test_a_row_that_only_resembles_a_file_does_not_claim_it(cfg, silence, export, monkeypatch):
    # The playlist asked for the extended mix and the file is the plain one:
    # filing it would be the landing answering a question only a person may.
    real = _track

    def versioned(title: str) -> dict:
        return {**real(title), "version": "Extended Mix"} if title == "One" else real(title)
    monkeypatch.setattr(sys.modules[__name__], "_track", versioned)
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Two"))})
    _staged(cfg, silence, "One", "Two")
    envelope = _applied(export, "--pass", PASS)
    assert _held(envelope) == {BATCH: ["One"], "Sunset Warmup 2026-10-03": ["Two"]}


# ---------------------------------------------------------------------------
# The gate, the digest and the record
# ---------------------------------------------------------------------------


def test_the_gate_screen_names_each_playlist_before_anything_moves(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",)), "pl-b": ("Deep Cuts", ("Two",))})
    _staged(cfg, silence, "One", "Two", "Three")
    code, refused = _drive(_land(export, "--pass", PASS))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["account playlists"] == [
        "Sunset Warmup 2026-10-03 (1 file(s)), the account's Sunset Warmup",
        "Deep Cuts 2026-10-03 (1 file(s)), the account's Deep Cuts",
    ]
    assert shown["batch playlist holds"] == "1 file(s) no account playlist claimed"
    assert sorted(p.name for p in Path(cfg.paths.download_staging).glob("*.flac")) == [
        "One.flac",
        "Three.flac",
        "Two.flac",
    ]


def test_an_answer_given_for_one_split_is_stale_for_another(cfg, silence, export):
    """The digest covers which playlist each file goes to, not only which files move."""
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _staged(cfg, silence, "One")
    argv = _land(export, "--pass", PASS)
    run_id = _decided(argv)["run_id"]
    # The same files, folder and batch, but the account playlist now lands
    # under another name, because INBOX came to hold its own.
    _inbox_holds(export, "Sunset Warmup 2026-10-03")
    code, envelope = _drive(["--run", run_id, *argv])
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()


def test_the_intake_record_names_each_playlist_and_its_batch_folder(cfg, silence, export):
    """And a person who discarded the intake file discarded its playlists too."""
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _staged(cfg, silence, "One")
    envelope = _applied(export, "--pass", PASS)
    assert envelope["outcome"] == "pending"
    (record,) = session.records(cfg)
    # The account and the pass beside the name since U128, which a rerun of
    # the pass reads to find what it already mirrored.
    assert record.detail[ingest.INBOX_PLAYLISTS_KEY] == [
        {"name": "Sunset Warmup 2026-10-03", "batch": BATCH, "account": "pl-a", "pass": PASS}
    ]
    assert account_playlists.mirrored(cfg, PASS) == frozenset({"pl-a"})
    session.close_session(record, cfg, state=session.SessionState.ABANDONED)
    assert account_playlists.mirrored(cfg, PASS) == frozenset()


def test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing(
    cfg, silence, export, monkeypatch
):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _staged(cfg, silence, "One")
    argv = _land(export, "--pass", PASS)
    code, refused = _drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    # The export is rewritten after the screen to hold the name, under the
    # same path; the verb is then handed the names it chose before.
    chosen = account_playlists.named
    monkeypatch.setattr(
        account_playlists, "named", lambda claimed, held, batch: chosen(claimed, (), batch=batch)
    )
    _inbox_holds(export, "Sunset Warmup 2026-10-03")
    code, envelope = _drive(["-d", f"{GATE}=apply", *argv])
    assert code != int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["cause"]["reason"] == "decision-stale"
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()


# ---------------------------------------------------------------------------
# The sweep records the name, and the naming rule
# ---------------------------------------------------------------------------


def test_sync_all_records_the_name_the_account_listed_on_each_playlist_job(slim, monkeypatch):
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Sunset Warmup", 1), _tracks("1")),
        (_playlist("pl-b", "Deep Cuts", 1), _tracks("2")),
    )
    code, passed = _drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    recorded = {
        str(job.payload[intake_cli.SOURCE]): job.payload.get(intake_cli.PLAYLIST_NAME)
        for job in _playlist_jobs()
    }
    assert recorded == {"pl-a": "Sunset Warmup", "pl-b": "Deep Cuts"}


def test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took():
    assert batch_name.inbox_names(
        ["Sunset Warmup", "Deep Cuts", "Sunset Warmup", "B"],
        ["Sunset Warmup 2026-10-03", "Sunset Warmup 2026-10-03 2"],
        batch="B 2026-10-03",
    ) == (
        "Sunset Warmup 2026-10-03 3",
        "Deep Cuts 2026-10-03",
        "Sunset Warmup 2026-10-03 4",
        "B 2026-10-03 2",
    )
    # A name is kept exactly and compared exactly.
    assert batch_name.inbox_names(
        ["sunset warmup", "A/B: C?"], ["Sunset Warmup 2026-10-03"], batch="x"
    ) == ("sunset warmup 2026-10-03", "A/B: C? 2026-10-03")


def test_inbox_names_puts_the_landing_date_at_the_end_of_the_accounts_name(monkeypatch):
    """U175: INBOX stays flat and the date goes after the name, never before it."""
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 27))
    assert batch_name.inbox_names(["Lisa_10_27_26"], (), batch="b") == ("Lisa_10_27_26 2026-10-27",)
    monkeypatch.setattr(batch_name, "today", lambda: DAY)
    # An undated name INBOX holds, one landed before U175, takes nothing from a
    # dated one, and is never renamed.
    assert batch_name.inbox_names(["Sunset Warmup"], ["Sunset Warmup"], batch="b") == (
        "Sunset Warmup 2026-10-03",
    )


def test_an_export_rewritten_after_the_gate_moves_nothing(cfg, silence, export):
    """The owned tracks' TrackIDs are read again before the first move.

    The gate screen counts the owned tracks beside the new.
    """
    held = _owned_export(cfg, silence, export, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    _staged(cfg, silence, "New1")
    argv = _land(held, "--pass", PASS)
    refused = _decided(argv)
    assert refused["cause"]["detail"]["shown"]["account playlists"] == [
        "Sunset Warmup 2026-10-03 (2 file(s), 1 already in the library), the account's Sunset Warmup"
    ]
    _renumber_held1(held)
    code, envelope = _drive(["--run", refused["run_id"], *argv])
    # The gate's digest covers each owned track's TrackID, so the answer is stale.
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert (Path(cfg.paths.download_staging) / "New1.flac").is_file()


def test_the_engine_reads_the_owned_entries_again_before_the_first_move(cfg, silence, export):
    """Between the plan and the moves, the engine's own check, not only the gate's."""
    from cratekit.intake import landing
    held = _owned_export(cfg, silence, export, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    staged = _stage(cfg, silence, "New1.flac")
    planned = landing.plan(staged.parent, cfg, BATCH)
    claims = account_playlists.split(cfg, PASS, planned.items)
    named = account_playlists.named(claims, (), batch=BATCH)
    split, _emptied = landing.owned_in_export(cfg, named, held)
    (one,) = split
    assert [m.row for m in one.members if m.file is None] != [""]
    _renumber_held1(held)
    with pytest.raises(CratekitError) as refused:
        landing.apply(
            planned,
            cfg=cfg,
            export=held,
            destination=Path(cfg.library.root).parent / "engine_inboxed.xml",
            split=split,
            pass_name=PASS,
        )
    assert refused.value.cause.reason == "decision-stale"
    assert "no longer lists the owned tracks" in refused.value.cause.message
    assert staged.is_file()


def test_an_export_entry_on_another_machine_is_no_owned_row(cfg, silence, export):
    """A Location naming another host has no path here, and is not a refusal."""
    held = _owned_export(cfg, silence, export, ("Held1",))
    body = held.read_text(encoding="utf-8").replace(
        'Location="file://localhost/', 'Location="file://otherhost/'
    )
    held.write_text(body, encoding="utf-8")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    _staged(cfg, silence, "New1")
    envelope = _applied(held, "--pass", PASS)
    assert _held(envelope)["Sunset Warmup 2026-10-03"] == ["New1"]
    (warning,) = _left(envelope)
    assert "Probe - Held1" in warning["message"]


def _one_owned(name: str, paths: tuple[str, ...], *more) -> account_playlists.Claimed:
    member = account_playlists.Member(
        position=1, paths=paths, artist="Probe", title="Held1", state="owned"
    )
    return account_playlists.Claimed(
        name=name, account_name=name, playlist_id="pl-a", members=(member, *more)
    )


def test_a_file_two_active_rows_claim_is_no_owned_row(cfg):
    from cratekit.write import trees
    held = Path(cfg.library.root) / cfg.library.music_dir / "b" / "Held1.flac"
    rows = [
        trees.ContentRow(content_id=one, recorded=str(held), deleted=False) for one in ("7", "8")
    ]
    new = account_playlists.Member(position=2, file=Path("New1.flac"))
    (kept,), emptied = account_playlists.resolve_owned(
        cfg, [_one_owned("Sunset Warmup", (str(held),), new)], rows
    )
    assert kept.members == (new,)
    assert [one.why for one in kept.left] == [account_playlists.AMBIGUOUS_ROWS]
    assert emptied == ()


def test_a_claim_left_holding_nothing_still_answers_its_left_rows(cfg):
    held = Path(cfg.library.root) / cfg.library.music_dir / "b" / "Held1.flac"
    kept, emptied = account_playlists.resolve_owned(
        cfg, [_one_owned("Deep Cuts", (str(held),))], []
    )
    assert kept == ()
    assert [(name, one.title, one.why) for name, one in emptied] == [
        ("Deep Cuts", "Held1", account_playlists.NO_ROW)
    ]
