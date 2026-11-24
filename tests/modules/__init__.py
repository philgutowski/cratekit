"""Tests for the feature modules under ``cratekit.modules``."""

from __future__ import annotations

from cratekit.core import config


def library_config(tmp_path, monkeypatch) -> config.Config:
    """A library under ``tmp_path``, its state and config folders redirected beside it. Unsaved."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (tmp_path / "install").mkdir()
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "install"))
    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(tmp_path / "cfgdir"))
    built = config.from_dict({
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(root), "volume_id": "F1E2-D3C4", "db_path": str(root / "db" / "master.db")
        },
        "paths": {"download_staging": str(tmp_path / "staging")},
        "profile": {"name": "full"},
    })
    config.reset_cache()
    return built
