"""U179: one new PULS release and one owned release land one batch filed under ``Record Labels / PULS``.

The brief's first test scenario, end to end. ``crate sync bandcamp`` plans
and fetches over U176's fake account through the real dispatcher, the tail
stands in at the chain's seam (analysis needs an extra and a real collection
this fixture does not hold), and the rehearsal and the landing run FOR REAL on
the disposable native database ``tests/test_intake_land_native.py`` builds.
The verb ends at the landing's gate; the session's two acts then answer and
apply it, and SQL reads the batch back filed under its label and year.

D1 applies. No real person, seller or release is named; ``pulsromania`` is
the fake account's seller.
"""

from __future__ import annotations

import shlex
from datetime import date
from pathlib import Path

import pytest

from cratekit.acquire import bandcamp_cli
from cratekit.cli import tail as tail_chain
from cratekit.core import config, jobs, secrets, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name
from cratekit.label import registry as labels
from tests.bandcamp_fakes import COOKIE, FakeAccount, archive, item
from tests.cli_drive import drive
from tests.test_intake_land_labels_native import _filed
from tests.test_intake_land_native import GATE, _query
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_intake_land_rehearse import _areas
from tests.test_sync_land import Tail

TODAY = date(2026, 11, 1)
BATCH = "Batch One"
NAME = "2026-11-01 Bandcamp PULS"


def _track(scratch: Path, silence: Path, name: str, artist: str, title: str) -> bytes:
    """A real FLAC tagged the way a release's file comes, its date tag set."""
    path = scratch / name
    path.write_bytes(silence.read_bytes())
    assert tags.write_tags(path, {"artist": artist, "title": title, "date": "2026-10-27"})
    return path.read_bytes()


@pytest.fixture
def account(native_library, silence, tmp_path, monkeypatch) -> FakeAccount:
    """One new PULS release of two tracks, and one the library already owns."""
    cfg, _root = native_library
    owned = Path(cfg.library.root) / cfg.library.music_dir / "Owned" / "Nova Reef - Low Light.flac"
    owned.parent.mkdir(parents=True)
    owned.write_bytes(b"")
    scratch = tmp_path / "served"
    scratch.mkdir()
    served = FakeAccount(
        [
            item("1", seller="pulsromania", artist="Aurora Bloom", title="Sun Path",
                 purchased="27 Oct 2026 10:00:00 GMT", tracks=[("", "Sun Path"), ("", "Tide")]),
            item("2", seller="pulsromania", artist="Nova Reef", title="Low Light",
                 purchased="20 Oct 2026 10:00:00 GMT", tracks=[("", "Low Light")]),
        ],
        archives={
            "1": archive({
                "Aurora Bloom - Sun Path - 01 Sun Path.flac":
                    _track(scratch, silence, "a1.flac", "Aurora Bloom", "Sun Path"),
                "Aurora Bloom - Sun Path - 02 Tide.flac":
                    _track(scratch, silence, "a2.flac", "Aurora Bloom", "Tide"),
            }),
        },
    )
    monkeypatch.setattr(bandcamp_cli, "transport", lambda: served)
    secrets.set(str(secrets.Credential.BANDCAMP_SESSION), COOKIE)
    labels.RegistryStore().add("PULS", bandcamp="pulsromania")
    return served


@pytest.fixture
def chain(monkeypatch) -> Tail:
    """The tail standing in, the tag step giving each file the label's genre; the landing real."""
    stand_in = Tail()
    stand_in.landing = stand_in.real

    def genre(job: jobs.Job, one: jobs.Item) -> None:
        assert tags.write_tags(Path(job.payload["folder"]) / one.item_id, {"genre": "Deep House"})

    stand_in.work[tail_chain.TAG] = genre
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    monkeypatch.setattr(batch_name, "today", lambda: TODAY)
    return stand_in


def test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label(
    native_library, account, chain
):
    cfg, _root = native_library

    code, envelope = drive(["sync", "bandcamp", "--seller", "PULS", "--batch", BATCH])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    summary = envelope["data"]["summary"]
    assert summary["landing_name"] == NAME
    assert [one["release"] for one in summary["owned"]] == ["Nova Reef - Low Light (pulsromania)"]
    assert summary["fetched"] == ["Aurora Bloom - Sun Path (pulsromania)"]
    # THE REHEARSAL RAN FOR REAL, on its own copy, and left no area behind.
    assert summary["rehearsal"]
    assert _areas(cfg) == []
    run_id = summary["gate_run"]
    folder = Path(summary["staging"])
    assert folder == (Path(cfg.paths.download_staging) / BATCH).absolute()

    # THE SESSION'S TWO ACTS, AS THE VERB NAMES THEM, pasted as a shell reads
    # them: the batch folder and the name both hold spaces.
    decide, apply = envelope["pending_human_action"]["steps"][:2]
    decide_argv = shlex.split(decide.split(": ", 1)[1])
    apply_argv = shlex.split(apply.split(": ", 1)[1])
    assert decide_argv == ["crate", "run", "decide", run_id, GATE, "apply", "--actor", "session"]
    assert apply_argv == [
        "crate", "--run", run_id, "intake", "land", str(folder), "--name", NAME, "--label-from-tags",
    ]
    decided, answered = drive(decide_argv[1:])
    assert decided == int(ExitCode.OK), answered
    code, applied = drive(apply_argv[1:])

    assert code == int(ExitCode.OK), applied
    assert _filed(cfg) == {"PULS": {"PULS 2026": ["Sun Path", "Tide"]}}
    (batch,) = _query(
        cfg, "SELECT ID FROM djmdPlaylist WHERE Name = ? AND rb_local_deleted = 0", NAME
    )
    assert batch
    assert not folder.is_dir() or not any(folder.iterdir()), "every staged file landed"
    # The owned release was never fetched.
    assert set(bandcamp_cli.fetched(config.load())) == {"1"}
