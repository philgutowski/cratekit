"""Export's set scenarios: a set made, archived, backfilled and renamed (U309).

`crate export set` makes a private playlist of a tracklist's rows on the
account behind its explicit gate; `crate export archive` files it in its
year's Downloaded Sets folder and holds it as taken; each, given nothing,
backfills over what the library proves; and `crate export set --rename`
follows the INSPIRATION playlist's new name behind its own gate. On the set
suite's installed machine with the catalogue and the account the suite's
fakes, the account's record of every call written beside the ledger.

The refusals are the rename's when the ledger already holds a set playlist
under the new name, and the set's when no provider session is stored.
"""

from __future__ import annotations

from cratekit.acquire import match
from cratekit.core.exit_codes import ExitCode
from cratekit.export import set_cli
from cratekit.label import catalogue
from cratekit.modules.outbound import ledger
from tests.behaviour.outbound import account_calls, gated
from tests.label_fakes import FakeCatalogue, catalogue_factory
from tests.test_export_set import ARCHIVE, BUILD, NAME, ROWS, SEARCHES, _landed, _tracklist
from tests.test_export_set import account as account  # noqa: PLC0414
from tests.test_export_set_rename import NEW, RENAME, _recorded
from tests.test_export_set_rename import renamed as renamed  # noqa: PLC0414
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_u129_set_account_playlist import _succeeded_set_job

OK = int(ExitCode.OK)
#: Two sets an INSPIRATION folder holds, each a succeeded set job of that name.
SETS = (
    ("10_09_26 Public Service NYC Live at Vonking 5-26", "2026-10-09T12:00:00+00:00"),
    ("10_10_26 Public Service NYC Live at Signal 5-26", "2026-10-10T12:00:00+00:00"),
)


def test_a_set_made_on_the_account_with_its_unmatched_row_named(stage, account):
    cfg, _fake, held = account

    assert gated(stage, ("export", "set", str(_tracklist(cfg))), BUILD).code == OK

    assert held.created == [NAME]
    assert ledger.set_playlist(cfg, NAME) is not None
    account_calls(stage, held)


def test_a_set_archived_into_its_years_downloaded_sets_folder(stage, account):
    cfg, _fake, held = account
    assert gated(stage, ("export", "set", str(_tracklist(cfg))), BUILD).code == OK
    xml = _landed(cfg)

    assert gated(stage, ("export", "archive", NAME, "--xml", str(xml)), ARCHIVE).code == OK

    year = ledger.set_playlist(cfg, NAME).year
    assert held.folders_created == [f"Downloaded Sets {year}"]
    account_calls(stage, held)


def test_the_set_backfill_makes_a_playlist_for_each_inspiration_set(stage, account, monkeypatch):
    cfg, _fake, held = account
    for name, created in SETS:
        _succeeded_set_job(cfg, name, created=created)
    listed = [(name, f"id-{index}") for index, (name, _created) in enumerate(SETS)]
    monkeypatch.setattr(set_cli, "_inspiration_playlists", lambda _cfg: listed)
    wanted = tuple(match.Wanted(artist=a, title=t, origin=match.TEXT) for a, t in ROWS)
    monkeypatch.setattr(set_cli, "_wanted_from_job", lambda _cfg, _job: wanted)

    assert gated(stage, ("export", "set"), BUILD).code == OK

    assert held.created == [name for name, _created in SETS]
    account_calls(stage, held)


def test_the_archive_backfill_files_every_set_its_intake_file_proves(stage, account):
    cfg, _fake, held = account
    assert gated(stage, ("export", "set", str(_tracklist(cfg))), BUILD).code == OK
    proof = cfg.library.root / f"{NAME}_inboxed.xml"
    proof.write_bytes(b"<DJ_PLAYLISTS Version='1.0.0'></DJ_PLAYLISTS>\n")

    assert gated(stage, ("export", "archive"), ARCHIVE).code == OK

    (playlist,) = held.playlists
    assert held.folder_names[held.placed[playlist]].startswith("Downloaded Sets ")
    account_calls(stage, held)


def test_a_renamed_inspiration_playlist_renames_the_sets_account_playlist(stage, renamed):
    cfg, held, job_id, remote_id, _live = renamed

    assert gated(stage, ("export", "set", "--rename", job_id), RENAME).code == OK

    assert held.renamed == [(remote_id, NEW)]
    assert ledger.set_playlist(cfg, NEW).remote_id == remote_id
    account_calls(stage, held)


def test_a_rename_onto_a_name_the_ledger_already_holds_is_refused(stage, renamed):
    cfg, held, job_id, _remote_id, _live = renamed
    _recorded(cfg, held, NEW)

    refused = stage.crate("export", "set", "--rename", job_id)

    assert refused.code == int(ExitCode.PRECONDITION), refused.stderr
    assert set_cli.RENAME_UNRESOLVED in refused.stderr, refused.stderr
    assert held.renamed == []
    account_calls(stage, held)


def test_a_set_with_no_stored_account_session_is_refused(stage, installed, monkeypatch):
    fake = FakeCatalogue(searches=dict(SEARCHES))
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))

    # The plan reads the catalogue alone, so the gate is asked; the write is refused.
    refused = gated(stage, ("export", "set", str(_tracklist(installed))), BUILD)

    assert refused.code == int(ExitCode.PRECONDITION), refused.stderr
    assert "credential-missing" in refused.stderr, refused.stderr
