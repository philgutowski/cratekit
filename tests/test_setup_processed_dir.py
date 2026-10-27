"""U154: ``library.processed_dir`` is a setup answer under the four source rule.

A flag is recorded, a recorded answer survives a re-run that does not name it,
an absent answer in a pipe falls to the default rather than prompting, and the
key composes with the music folder wherever the processed tree is read.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import json
from pathlib import Path

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import shelve
from tests.test_config_update import _trap_standard_input as _trap_standard_input  # noqa: PLC0414
from tests.test_config_update import configured as configured  # noqa: PLC0414
from tests.test_config_update import drive, on_disk
from tests.test_config_update import library as library  # noqa: PLC0414


def _setup(*extra: str) -> tuple[int, dict, str]:
    code, out, err = drive(["--output", "json", "setup", *extra])
    return code, json.loads(out) if out.strip() else {}, err


def test_the_flag_is_recorded_under_the_library_table(configured):
    code, _envelope, err = _setup("--processed-dir", "Filed")
    assert code == int(ExitCode.OK), err
    assert on_disk()["library"]["processed_dir"] == "Filed"


def test_a_recorded_answer_survives_a_rerun_that_does_not_name_it(configured):
    code, _envelope, err = _setup("--processed-dir", "Filed")
    assert code == int(ExitCode.OK), err
    code, _envelope, err = _setup()
    assert code == int(ExitCode.OK), err
    assert on_disk()["library"]["processed_dir"] == "Filed", "the re-run re-answered the question"


def test_an_absent_answer_falls_to_the_default_in_a_pipe(configured):
    """The wizard runs with standard input trapped, so a question it cannot ask
    takes the derived default, which is the tree the author kept by hand."""
    # THE RAW FILE, because every writer this product has puts the dataclass
    # back whole, defaults included, so the one way to a file without the key
    # is to take the line out of the text the way a hand edit would.
    path = config.config_path()
    kept = [
        line
        for line in path.read_text(encoding="utf-8").splitlines(keepends=True)
        if not line.startswith("processed_dir")
    ]
    path.write_text("".join(kept), encoding="utf-8")
    config.reset_cache()
    assert "processed_dir" not in config.config_path().read_text(encoding="utf-8")
    code, _envelope, err = _setup()
    assert code == int(ExitCode.OK), err
    assert on_disk()["library"]["processed_dir"] == config.DEFAULT_PROCESSED_DIR


def test_the_default_is_spelled_once(configured):
    assert config.LibraryConfig.__dataclass_fields__["processed_dir"].default == (
        config.DEFAULT_PROCESSED_DIR
    )


def test_the_processed_root_composes_from_the_two_keys(configured):
    code, _envelope, err = _setup("--processed-dir", "Filed")
    assert code == int(ExitCode.OK), err
    config.reset_cache()
    cfg = config.load()
    assert shelve.processed_root(cfg) == Path(cfg.library.root) / cfg.library.music_dir / "Filed"


def test_a_clean_machine_records_the_default_when_no_flag_names_one(tmp_path, monkeypatch):
    """The four source rule's last two sources, on the one run where no answer is
    recorded yet: no flag, nothing on disk, standard input trapped, so the
    derived default is what reaches the file."""
    from cratekit.cli import doctor
    from tests.test_doctor import VOLUME, probes

    root = tmp_path / "fresh"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    code, _out, err = drive(
        [
            "--output",
            "json",
            "setup",
            "--library-root",
            str(root),
            "--db-path",
            str(root / "db" / "master.db"),
            "--volume-id",
            VOLUME,
            "--staging",
            str(tmp_path / "staging"),
            "--profile",
            "slim",
            "--taxonomy",
            "default",
        ]
    )
    assert code in {int(ExitCode.OK), int(ExitCode.PRECONDITION)}, err
    config.reset_cache()
    assert config.load().library.processed_dir == config.DEFAULT_PROCESSED_DIR
    assert f'processed_dir = "{config.DEFAULT_PROCESSED_DIR}"' in config.config_path().read_text(
        encoding="utf-8"
    )
