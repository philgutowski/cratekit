"""Acquire's fallback search scenarios: candidates offered, kept and accepted (U305).

Apart from ``acquire.py`` because the fallback suite names its own ``cfg`` and ``library``.
"""

from __future__ import annotations

from cratekit.core import binaries
from tests.test_acquire_fallback import (
    BOOT,
    GLASS,
    SC,
    TIDE_Q,
    YT,
    FakeSearcher,
    bind,
    boot_answers,
    items_of,
    tracklist,
    unfindable,
)
from tests.test_acquire_fallback import cfg as cfg  # noqa: PLC0414
from tests.test_acquire_fallback import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_acquire_fallback import library as library  # noqa: PLC0414
from tests.test_acquire_fallback import no_real_searcher as no_real_searcher  # noqa: PLC0414


def test_fallback_offers_and_accepts(stage, cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT, "Nova Reef - Tide", GLASS)
    bind(monkeypatch, FakeSearcher(boot_answers(), fail={(YT, TIDE_Q), (SC, TIDE_Q)}))
    assert "cause" in stage.json("acquire", "fallback", str(path)).envelope
    stage.crate("acquire", "fallback", str(path))
    offered = [item for item in items_of(cfg) if item.options]
    assert offered
    choice = offered[0].options[0].option_id
    stage.crate("review", "resolve", offered[0].item_id, "--verdict", "accepted", "--option", choice)
    stage.json("acquire", "fallback", str(path))
    stage.crate("acquire", "fallback", str(tmp_path / "absent.txt"))


def test_fallback_without_its_downloader_and_with_a_broken_override(
    stage, cfg, library, tmp_path, monkeypatch
):
    """The refusal both verbs share, whose one spelling U331 moved into ``core.binaries``."""
    path = tracklist(tmp_path, BOOT)
    unfindable(monkeypatch)
    missing = stage.json("acquire", "fallback", str(path)).envelope
    assert missing["cause"]["reason"] == "yt-dlp-missing"
    stage.crate("acquire", "fallback", str(path))
    monkeypatch.setenv(binaries.env_var("yt-dlp"), str(tmp_path / "not-a-program"))
    broken = stage.json("acquire", "fallback", str(path)).envelope
    assert broken["cause"]["remediation"]["remedy"] == "fix-binary-override"
