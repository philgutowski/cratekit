"""U37: path repair proposes, offers, and is idempotent."""

from __future__ import annotations

from pathlib import Path

from cratekit.core import config, review
from cratekit.core.review import Queue
from cratekit.intake import repair
from tests.test_config import valid_data


def _cfg(tmp_path: Path) -> config.Config:
    root = tmp_path / "library"
    root.mkdir()
    data = valid_data(root)
    data["paths"] = {"download_staging": str(tmp_path / "staging")}
    cfg = config.from_dict(data)
    config.save(cfg)
    config.reset_cache()
    return cfg


def test_propose_name_is_idempotent_on_a_name_that_already_fits(tmp_path):
    cfg = _cfg(tmp_path)
    path = Path(cfg.library.root) / "04A - 124 - Short Title.flac"
    path.write_bytes(b"fLaC")
    first, err = repair.propose_name(path, cfg=cfg)
    assert err == ""
    assert first == path.name
    again, err2 = repair.propose_name(path, cfg=cfg)
    assert err2 == ""
    assert again == first


def test_offer_repairs_writes_path_repair_queue_items(tmp_path):
    cfg = _cfg(tmp_path)
    path = Path(cfg.library.root) / "too-long-name.flac"
    path.write_bytes(b"fLaC")
    proposed = "short.flac"
    with review.open_store(cfg) as store:
        items = repair.offer_repairs(store, [(path, proposed, "")])
        assert items
        listed = review.list_items(store, queue=Queue.PATH_REPAIR)
        assert listed.items
        assert listed.items[0].queue == Queue.PATH_REPAIR
        again = repair.offer_repairs(store, [(path, proposed, "")])
        assert again[0].item_id == items[0].item_id
        assert review.count_unresolved(store) == 1
