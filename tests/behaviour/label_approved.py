"""Label approved's scenarios: the download list written from the accepted label releases (U308).

`crate label approved` reads every label release accepted in review, asks
the provider for each one's tracks, leaves out what the library owns, and
writes the list `acquire download` reads. A run with nothing accepted is a
no op that opens no catalogue. On the approved suite's own machine, its
strict fake catalogue and releases offered by the sweep's own producer.
"""

from __future__ import annotations

from cratekit.core import review
from cratekit.core.exit_codes import ExitCode
from tests.label_fakes import StrictCatalogue
from tests.test_label_approved import (
    Track,
    accepted,
    answered,
    bind,
    offered,
    owned,
    two_track_release,
)
from tests.test_label_approved import cfg as cfg  # noqa: PLC0414
from tests.test_label_approved import library as library  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_accepted_releases_listed_for_download(stage, cfg, library, monkeypatch):
    bind(monkeypatch, StrictCatalogue(releases={}))
    assert stage.crate("label", "approved").code == OK
    owned(library, "Aurora Bloom - Sun Path.flac")
    accepted(cfg, "r-1")
    accepted(cfg, "r-gone")
    answered(cfg, offered(cfg, "r-2"), review.Verdict.REJECTED)
    offered(cfg, "r-3")
    bind(
        monkeypatch,
        StrictCatalogue(
            releases={
                "r-1": two_track_release(),
                "r-2": ([Track("401", "Mira Vale", "Glass Hour")], 2023),
            }
        ),
    )
    listed = stage.crate("label", "approved")
    assert listed.code == OK, listed.stderr
    assert stage.json("label", "approved").code == OK
