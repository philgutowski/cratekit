"""``library.processed_dir`` is a setup answer under the four source rule (U154).

A flag is recorded, a recorded answer survives a re-run, an absent answer in a
pipe takes the default rather than prompting, and the key composes with the
music folder wherever the processed tree is read. D1 applies.
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
    """With standard input trapped, a question the wizard cannot ask takes the derived default."""
    # Edit the raw text, since every writer puts the dataclass back whole, defaults included.
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
    field = config.LibraryConfig.__dataclass_fields__["processed_dir"]
    assert field.default == config.DEFAULT_PROCESSED_DIR


def test_the_processed_root_composes_from_the_two_keys(configured):
    code, _envelope, err = _setup("--processed-dir", "Filed")
    assert code == int(ExitCode.OK), err
    config.reset_cache()
    cfg = config.load()
    assert shelve.processed_root(cfg) == Path(cfg.library.root) / cfg.library.music_dir / "Filed"


def test_a_clean_machine_records_the_default_when_no_flag_names_one(tmp_path, monkeypatch):
    """A clean machine with no flag and standard input trapped writes the derived default."""
    from cratekit.cli import doctor
    from tests.test_doctor import VOLUME, probes

    root = tmp_path / "fresh"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    code, _out, err = drive([
        "--output", "json", "setup", "--library-root", str(root), "--db-path",
        str(root / "db" / "master.db"), "--volume-id", VOLUME, "--staging",
        str(tmp_path / "staging"), "--profile", "slim", "--taxonomy", "default",
    ])
    assert code in {int(ExitCode.OK), int(ExitCode.PRECONDITION)}, err
    config.reset_cache()
    assert config.load().library.processed_dir == config.DEFAULT_PROCESSED_DIR
    written = config.config_path().read_text(encoding="utf-8")
    assert f'processed_dir = "{config.DEFAULT_PROCESSED_DIR}"' in written
