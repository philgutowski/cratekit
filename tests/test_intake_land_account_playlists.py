"""U113: a playlist the author made on the account lands as its own INBOX playlist.

Every landing here drives the real dispatcher on the xml bridge, with the
fixtures ``tests/test_intake_land.py`` keeps, over a pass whose jobs are queued
with the account's names the way ``crate sync all`` queues them and then RUN by
the real worker, so the reports the landing reads are the ones the product
writes. The native medium is pinned in
``tests/test_intake_land_account_playlists_native.py``.

D1 applies. Nothing here names a real person or a real track.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs, session
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import account_playlists, batch_name, ingest, missing_cli
from cratekit.intake import cli as intake_cli
from cratekit.sync import playlists
from tests.test_intake_land import GATE, _drive, _land, _manifest, _music, _stage
from tests.test_intake_land import cfg as cfg  # noqa: PLC0414 - the fixture, re-exported
from tests.test_intake_land import export as export  # noqa: PLC0414 - the fixture
from tests.test_intake_land import silence as silence  # noqa: PLC0414 - the fixture
from tests.test_sync_all import _playlist, _playlist_jobs, _tracks, bind_playlists
from tests.test_sync_all import slim as slim  # noqa: PLC0414 - the fixture

DAY = date(2026, 10, 3)
RUN = "2026-10-03T101500Z-cd34"
PASS = missing_cli.synced_name(RUN)
BATCH = "2026-10-03 Tidal playlists"


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
    """One job per playlist, ``id -> (account name, titles)``, queued and run.

    Queued through the one spelling ``crate sync all`` uses, then driven by the
    real worker against the library, which holds none of the titles, so every
    report says missing, which is what a download is made from.
    """
    queued: list[jobs.Job] = []
    with jobs.open_store() as store:
        for playlist_id, (name, titles) in listed.items():
            queued.append(
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
            )
    for job in queued:
        code, resumed = _drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), resumed
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    return queued


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


# ---------------------------------------------------------------------------
# The scenarios the brief names
# ---------------------------------------------------------------------------


def test_two_swept_playlists_land_as_two_inbox_playlists_under_their_exact_names(
    cfg, silence, export
):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Two")), "pl-b": ("Deep Cuts", ("Three",))})
    for name in ("One.flac", "Two.flac", "Three.flac"):
        _stage(cfg, silence, name)

    envelope = _applied(export, "--pass", PASS)

    # The files still land in the one batch folder U110 names.
    assert sorted(p.name for p in _music(cfg, BATCH).iterdir()) == [
        "One.flac",
        "Three.flac",
        "Two.flac",
    ]
    # Only the playlists split, and the batch playlist, holding nothing, is not written.
    assert _inbox(_intake(envelope)) == {"Sunset Warmup": ["One", "Two"], "Deep Cuts": ["Three"]}
    split = [item for item in envelope["data"]["items"] if item["action"] == "playlist"]
    assert split == [
        {"action": "playlist", "playlist": "Sunset Warmup", "account": "pl-a", "count": 2},
        {"action": "playlist", "playlist": "Deep Cuts", "account": "pl-b", "count": 1},
    ]


def test_a_track_both_playlists_brought_in_is_a_member_of_both(cfg, silence, export):
    swept(
        cfg,
        {"pl-a": ("Sunset Warmup", ("One", "Shared")), "pl-b": ("Deep Cuts", ("Shared",))},
    )
    for name in ("One.flac", "Shared.flac"):
        _stage(cfg, silence, name)

    envelope = _applied(export, "--pass", PASS)

    assert _inbox(_intake(envelope)) == {
        "Sunset Warmup": ["One", "Shared"],
        "Deep Cuts": ["Shared"],
    }


def test_a_second_landing_of_one_playlist_the_next_week_is_named_two(
    cfg, silence, export, monkeypatch
):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One.flac")
    first = _intake(_applied(export, "--pass", PASS))

    # A week on: the next pass of the same playlist, landed against an export
    # that holds the first landing's playlist under INBOX, as one taken after
    # its import does.
    later = date(2026, 10, 10)
    run = "2026-10-10T101500Z-ef56"
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Two",))}, run_id=run)
    _stage(cfg, silence, "Two.flac")
    monkeypatch.setattr(batch_name, "today", lambda: later)
    envelope = _applied(first, "--pass", missing_cli.synced_name(run))

    held = _inbox(_intake(envelope))
    assert held["Sunset Warmup"] == ["One"]
    assert held["Sunset Warmup 2"] == ["Two"]


def test_a_name_an_unimported_intake_file_holds_is_not_given_again(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One.flac")
    _applied(export, "--pass", PASS)

    # The first intake file is still waiting on its import, so the export the
    # second landing is handed holds neither of its playlists.
    run = "2026-10-03T201500Z-ab78"
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Two",))}, run_id=run)
    _stage(cfg, silence, "Two.flac")
    envelope = _applied(export, "--pass", missing_cli.synced_name(run))

    assert _inbox(_intake(envelope)) == {"Sunset Warmup 2": ["Two"]}


def test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there(
    cfg, silence, export
):
    body = export.read_text(encoding="utf-8").replace(
        '<NODE Name="INBOX" Type="0" Count="0">',
        '<NODE Name="Sunset Warmup" Type="1" KeyType="0" Entries="0">\r\n'
        "      </NODE>\r\n"
        '      <NODE Name="INBOX" Type="0" Count="0">',
    )
    export.write_text(body, encoding="utf-8")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One.flac")

    envelope = _applied(export, "--pass", PASS)

    assert _inbox(_intake(envelope)) == {"Sunset Warmup 2": ["One"]}


def test_a_label_landing_keeps_the_name_u110_gives_it(cfg, silence, export, tmp_path):
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])

    envelope = _applied(export, "--manifest", str(manifest))

    assert _music(cfg, "2026-10-03 Kompakt").is_dir()
    assert next(iter(_inbox(_intake(envelope)))) == "2026-10-03 Kompakt"
    assert not [i for i in envelope["data"]["items"] if i["action"] == "playlist"]


# ---------------------------------------------------------------------------
# What stays as it was, and what the batch playlist keeps
# ---------------------------------------------------------------------------


def test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    swept(cfg, {"favorites": (None, ("Hearted",))}, source_id=intake_cli.FAVORITES_SOURCE_ID)
    for name in ("One.flac", "Hearted.flac"):
        _stage(cfg, silence, name)

    envelope = _applied(export, "--pass", PASS)

    batch = "2026-10-03 Tidal playlists and Favorites"
    assert _inbox(_intake(envelope)) == {batch: ["Hearted"], "Sunset Warmup": ["One"]}
    steps = " ".join(envelope["pending_human_action"]["steps"])
    assert f"each of the {batch} and Sunset Warmup playlists" in steps


def test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before(cfg, silence, export):
    swept(cfg, {"pl-a": (None, ("One",))})
    _stage(cfg, silence, "One.flac")

    envelope = _applied(export, "--pass", PASS)

    assert _inbox(_intake(envelope)) == {BATCH: ["One"]}
    assert not [i for i in envelope["data"]["items"] if i["action"] == "playlist"]


def test_a_landing_with_no_pass_splits_nothing(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One.flac")

    envelope = _applied(export, "--name", "by hand")

    assert _inbox(_intake(envelope)) == {"by hand": ["One"]}


def test_an_owned_track_whose_row_the_export_does_not_hold_is_warned(cfg, silence, export):
    # The library holds the file and the export the batch is spliced into has
    # no entry for it, so there is no TrackID for the playlist to name: the
    # track is left, and the landing names it rather than dropping it (U128).
    owned = _music(cfg, "older batch")
    owned.mkdir(parents=True)
    _stage(cfg, silence, "Held.flac").rename(owned / "Held.flac")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Held"))})
    _stage(cfg, silence, "One.flac")

    envelope = _applied(export, "--pass", PASS)

    assert _inbox(_intake(envelope)) == {"Sunset Warmup": ["One"]}
    (warning,) = [w for w in envelope["warnings"] if w["code"] == account_playlists.LEFT_OUT]
    assert "Sunset Warmup 2. Probe - Held" in warning["message"]
    assert account_playlists.NO_ROW in warning["message"]


# ---------------------------------------------------------------------------
# U128: the INBOX playlist mirrors the whole account playlist
# ---------------------------------------------------------------------------


def _owned_export(cfg, silence, export: Path, titles: tuple[str, ...]) -> Path:
    """An export whose collection holds ``titles``, landed earlier into the library.

    Landed by the product itself under a name of its own and no pass, so each
    is a file under the music folder and an entry of the intake file, which is
    then the export the next landing is spliced into, as one taken after the
    import is.
    """
    for title in titles:
        _stage(cfg, silence, f"{title}.flac")
    return _intake(_applied(export, "--name", "older batch"))


def test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order(
    cfg, silence, export
):
    held = _owned_export(cfg, silence, export, ("Held1", "Held2", "Held3"))
    swept(
        cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1", "Held2", "New2", "Held3"))}
    )
    for name in ("New1.flac", "New2.flac"):
        _stage(cfg, silence, name)

    envelope = _applied(held, "--pass", PASS)

    inbox = _inbox(_intake(envelope))
    assert inbox["Sunset Warmup"] == ["Held1", "New1", "Held2", "New2", "Held3"]
    # The owned tracks are the export's own entries, not spliced a second time.
    body = _intake(envelope).read_text(encoding="utf-8")
    assert body.count('Name="Held1"') == 1
    split = [item for item in envelope["data"]["items"] if item["action"] == "playlist"]
    assert split == [
        {"action": "playlist", "playlist": "Sunset Warmup", "account": "pl-a", "count": 5}
    ]
    assert not [w for w in envelope["warnings"] if w["code"] == account_playlists.LEFT_OUT]


def test_the_gate_screen_counts_the_owned_tracks_beside_the_new(cfg, silence, export):
    held = _owned_export(cfg, silence, export, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    _stage(cfg, silence, "New1.flac")

    code, refused = _drive(_land(held, "--pass", PASS))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["account playlists"] == ["Sunset Warmup (2 file(s), 1 already in the library)"]


def test_an_owned_track_in_two_account_playlists_is_in_both(cfg, silence, export):
    held = _owned_export(cfg, silence, export, ("Held1",))
    swept(
        cfg,
        {
            "pl-a": ("Sunset Warmup", ("Held1", "New1")),
            "pl-b": ("Deep Cuts", ("New1", "Held1")),
        },
    )
    _stage(cfg, silence, "New1.flac")

    envelope = _applied(held, "--pass", PASS)

    inbox = _inbox(_intake(envelope))
    assert inbox["Sunset Warmup"] == ["Held1", "New1"]
    assert inbox["Deep Cuts"] == ["New1", "Held1"]


def test_a_track_neither_owned_nor_brought_is_named_in_the_warnings(cfg, silence, export):
    # The download for Gone never arrived, a lossy file refused or a row
    # nothing answered, so the library does not hold it and the landing did
    # not bring it.
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Gone"))})
    _stage(cfg, silence, "One.flac")

    envelope = _applied(export, "--pass", PASS)

    assert _inbox(_intake(envelope)) == {"Sunset Warmup": ["One"]}
    (warning,) = [w for w in envelope["warnings"] if w["code"] == account_playlists.LEFT_OUT]
    assert "Sunset Warmup 2. Probe - Gone" in warning["message"]
    assert account_playlists.NOT_BROUGHT in warning["message"]


def test_a_rerun_of_the_same_pass_is_a_no_op(cfg, silence, export):
    held = _owned_export(cfg, silence, export, ("Held1",))
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Held1", "New1"))})
    _stage(cfg, silence, "New1.flac")
    first = _intake(_applied(held, "--pass", PASS))
    before = first.read_bytes()

    code, again = _drive(["-d", f"{GATE}=apply", *_land(first, "--pass", PASS)])

    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op", again
    assert again["data"]["items"] == []
    assert first.read_bytes() == before


def test_a_row_that_only_resembles_a_file_does_not_claim_it(cfg, silence, export, monkeypatch):
    # The playlist asked for the extended mix and the file is the plain one:
    # filing it would be the landing answering a question only a person may.
    real = _track

    def versioned(title: str) -> dict:
        return {**real(title), "version": "Extended Mix"} if title == "One" else real(title)

    monkeypatch.setattr(sys.modules[__name__], "_track", versioned)
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Two"))})
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)

    envelope = _applied(export, "--pass", PASS)

    assert _inbox(_intake(envelope)) == {BATCH: ["One"], "Sunset Warmup": ["Two"]}


# ---------------------------------------------------------------------------
# The gate, the digest and the record
# ---------------------------------------------------------------------------


def test_the_gate_screen_names_each_playlist_before_anything_moves(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",)), "pl-b": ("Deep Cuts", ("Two",))})
    for name in ("One.flac", "Two.flac", "Three.flac"):
        _stage(cfg, silence, name)

    code, refused = _drive(_land(export, "--pass", PASS))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["account playlists"] == ["Sunset Warmup (1 file(s))", "Deep Cuts (1 file(s))"]
    assert shown["batch playlist holds"] == "1 file(s) no account playlist claimed"
    assert sorted(p.name for p in Path(cfg.paths.download_staging).glob("*.flac")) == [
        "One.flac",
        "Three.flac",
        "Two.flac",
    ]


def test_an_answer_given_for_one_split_is_stale_for_another(cfg, silence, export):
    """The digest covers which playlist each file goes to, not only which files move."""
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One.flac")
    argv = _land(export, "--pass", PASS)
    code, refused = _drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])

    # The same files, folder and batch, but the account playlist now lands
    # under another name, because INBOX came to hold its own.
    body = export.read_text(encoding="utf-8").replace(
        '<NODE Name="INBOX" Type="0" Count="0">',
        '<NODE Name="INBOX" Type="0" Count="1">\r\n'
        '        <NODE Name="Sunset Warmup" Type="1" KeyType="0" Entries="0">\r\n'
        "        </NODE>",
    )
    export.write_text(body, encoding="utf-8")
    code, envelope = _drive(["--run", run_id, *argv])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()


def test_the_intake_record_names_each_playlist_and_its_batch_folder(cfg, silence, export):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One.flac")

    envelope = _applied(export, "--pass", PASS)

    assert envelope["outcome"] == "pending"
    (record,) = session.records(cfg)
    # The account and the pass beside the name since U128, which a rerun of
    # the pass reads to find what it already mirrored.
    assert record.detail[ingest.INBOX_PLAYLISTS_KEY] == [
        {"name": "Sunset Warmup", "batch": BATCH, "account": "pl-a", "pass": PASS}
    ]


def test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing(
    cfg, silence, export, monkeypatch
):
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One.flac")
    argv = _land(export, "--pass", PASS)
    code, refused = _drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused

    # The export is rewritten after the screen to hold the name, under the
    # same path; the verb is then handed the names it chose before.
    chosen = account_playlists.named
    monkeypatch.setattr(
        account_playlists, "named", lambda claimed, held, batch: chosen(claimed, (), batch=batch)
    )
    body = export.read_text(encoding="utf-8").replace(
        '<NODE Name="INBOX" Type="0" Count="0">',
        '<NODE Name="INBOX" Type="0" Count="1">\r\n'
        '        <NODE Name="Sunset Warmup" Type="1" KeyType="0" Entries="0">\r\n'
        "        </NODE>",
    )
    export.write_text(body, encoding="utf-8")

    code, envelope = _drive(["-d", f"{GATE}=apply", *argv])

    assert code != int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["cause"]["reason"] == "decision-stale"
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()


# ---------------------------------------------------------------------------
# The sweep records the name, and the naming rule
# ---------------------------------------------------------------------------


def test_sync_all_records_the_name_the_account_listed_on_each_playlist_job(slim, monkeypatch):
    from tests.cli_drive import drive

    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Sunset Warmup", 1), _tracks("1")),
        (_playlist("pl-b", "Deep Cuts", 1), _tracks("2")),
    )
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed

    recorded = {
        str(job.payload[intake_cli.SOURCE]): job.payload.get(intake_cli.PLAYLIST_NAME)
        for job in _playlist_jobs()
    }
    assert recorded == {"pl-a": "Sunset Warmup", "pl-b": "Deep Cuts"}


def test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took():
    assert batch_name.inbox_names(
        ["Sunset Warmup", "Deep Cuts", "Sunset Warmup", "B"],
        ["Sunset Warmup", "Sunset Warmup 2"],
        batch="B",
    ) == ("Sunset Warmup 3", "Deep Cuts", "Sunset Warmup 4", "B 2")


def test_inbox_names_keeps_a_name_exactly_and_compares_it_exactly():
    assert batch_name.inbox_names(
        ["sunset warmup", "A/B: C?"], ["Sunset Warmup"], batch="x"
    ) == ("sunset warmup", "A/B: C?")
