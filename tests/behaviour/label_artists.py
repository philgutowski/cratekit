"""Label artists' scenarios: an open release reading an object address given its artist (U308).

Decided and already named items are left alone.
"""

from __future__ import annotations

from cratekit.core import review
from cratekit.core.exit_codes import ExitCode
from tests.label_fakes import StrictCatalogue
from tests.test_label_artists import bind, decided, offered
from tests.test_label_artists import cfg as cfg  # noqa: PLC0414
from tests.test_label_artists import library as library  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_an_address_given_its_artist(stage, cfg, monkeypatch):
    bind(monkeypatch, StrictCatalogue(release_artists={}))
    assert stage.crate("label", "artists").code == OK
    offered(cfg, "r-1")
    offered(cfg, "r-gone")
    offered(cfg, "r-named", artist="Named Act")
    decided(cfg, offered(cfg, "r-decided"), review.Verdict.ACCEPTED)
    bind(monkeypatch, StrictCatalogue(release_artists={"r-1": "Harbour Act", "r-decided": "Other"}))
    repaired = stage.crate("label", "artists")
    assert repaired.code == OK, repaired.stderr
    assert stage.json("label", "artists").code == OK
