"""Intake's missing scenarios over a set: rows named by exact ISRC and the rest handed on (U307).

A set identified through the worker suite's recognition fakes is queued and
driven to the end; `crate intake missing --job` then asks the catalogue for
each recognised row's ISRC, lists the row one identifier names, and writes
the rest, two identifiers or none, to the unlisted list a person reads with
its reasons. A provider that cannot answer refuses before any file is
written. Only the catalogue is a fake beside the recognition seams.

A file of its own, because the ISRC suite calls its configuration ``cfg``
and its library ``library`` as other intake suites call theirs.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.intake.test_workers import recognised as recognised  # noqa: PLC0414
from tests.label_fakes import FakeCatalogue, FakeTrack, UnreadableCatalogue
from tests.test_intake_missing_isrc import ONE, TWO, bind, finished_set, three
from tests.test_intake_missing_isrc import cfg as cfg  # noqa: PLC0414
from tests.test_intake_missing_isrc import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_intake_missing_isrc import library as library  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_one_isrc_is_listed_and_the_rest_handed_on(stage, cfg, library, recognised, monkeypatch):
    job_id = finished_set(library, recognised, monkeypatch, *three())
    bind(
        monkeypatch,
        FakeCatalogue(
            isrcs={ONE: [FakeTrack("9001")], TWO: [FakeTrack("9002"), FakeTrack("9003")]}
        ),
    )

    assert stage.crate("intake", "missing", "--job", job_id).code == OK
    listed = stage.json("intake", "missing", "--job", job_id)
    assert listed.code == OK, listed.stdout
    summary = listed.envelope["data"]["summary"]
    assert (summary["written"], summary["unlisted"]) == (1, 2)


def test_a_provider_outage_refuses_and_writes_nothing(stage, cfg, library, recognised, monkeypatch):
    job_id = finished_set(library, recognised, monkeypatch, *three())
    bind(monkeypatch, UnreadableCatalogue())
    refused = stage.json("intake", "missing", "--job", job_id)
    assert refused.code != OK, refused.stdout
    assert refused.envelope["cause"]["reason"] == "unavailable-transient"
