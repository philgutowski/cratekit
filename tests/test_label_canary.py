"""U277: a label whose only confirmed releases are held says nothing new.

Sitting 94 ran ``crate label sync --next --label rawax`` over a listing of 119
releases and was refused as a catalogue it could not confirm. Sitting 93 had
asked about all seven of Rawax's releases then, four credited ``Rawax`` and
three credited ``RAWAXXX``, another act the old substring needle matched, so
all seven are held. The sweep re-verifies one held release to tell a dead
verifier from a label with nothing new, and it took the newest, a
``RAWAXXX`` one, which U237's whole word needle rightly answers as a
mismatch; every held release then counted as unconfirmed and 112 dropped
plus 7 held was the 119 read.

The canary is now the held release whose own copyright line the needle
confirms, and it is still ASKED, so a verifier that answers nothing still
refuses. These tests verify as the real catalogue does, by the release's own
line, and drive both the guided ``--next`` and the sweep worker.

NOTHING HERE REACHES A NETWORK OR ACCEPTS A RELEASE.
"""

from __future__ import annotations

from typing import Any

import pytest

from cratekit.core import config, jobs, review
from cratekit.core.exit_codes import ExitCode
from cratekit.core.review import Queue
from cratekit.label import catalogue, sweep, sync_cli, tidal_catalogue
from cratekit.label import registry as labels
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedArtist, FakeRelease, catalogue_factory
from tests.test_config import valid_data
from tests.test_label_workers import queued_sweep

LABEL = "Rawax"
SLUG = "rawax"


@pytest.fixture
def installed(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    code, envelope = drive(["label", "registry", "add", LABEL])
    assert code == int(ExitCode.OK), envelope
    return resolved


class LineCatalogue(FakeCatalogue):
    """Verifies a release as the real catalogue does: by its own copyright line.

    ``dead`` is a verification endpoint that answers nothing for any release,
    the case the refusal exists for. ``verified`` records each release asked.
    """

    def __init__(self, *args: Any, dead: bool = False, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.dead = dead
        self.verified: list[str] = []

    def search_release(self, claimed: str, release: Any) -> dict:
        self.verified.append(str(release.id))
        if self.dead:
            return {
                "verdict": "unconfirmed",
                "resolved_label": "",
                "source": "fake-catalogue",
                "notes": "the verification endpoint answered nothing",
            }
        # The shipped catalogue's own read, so a fixture line is judged by
        # exactly the extractor and needle a live sweep uses. It reads the
        # provider again only for a release with no line, and every release
        # here carries one.
        return dict(tidal_catalogue.TidalCatalogue.search_release(self, claimed, release))


def release(identity: str, year: str, line: str, *, artist: str = "Arapu") -> FakeRelease:
    return FakeRelease(identity, year=year, artist=artist, copyright=line)


def others(count: int) -> list[FakeRelease]:
    """Releases of the roster's artists on other labels, each a line naming one."""
    names = ("Planet Radio", "20/20 Vision Recordings", "Moon Harbour", "Cocoon")
    return [
        release(f"o{n}", str(2024 - n // 20), f"2024 {names[n % len(names)]}", artist="Other Act")
        for n in range(count)
    ]


def rawaxxx() -> list[FakeRelease]:
    return [release(f"x{n}", "2026", "2026 RAWAXXX", artist="RAWAXXX") for n in range(3)]


def rawax(line: str = "Rawax") -> list[FakeRelease]:
    return [
        release("a1", "2025", line),
        release("a2", "2025", line),
        release("a3", "2025", line),
        release("a4", "2025", line, artist="Carl Finlow"),
    ]


def bind(monkeypatch, releases: list[FakeRelease], **kwargs: Any) -> LineCatalogue:
    fake = LineCatalogue(artists={SLUG: FakePagedArtist(releases)}, **kwargs)
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def asked(cfg: config.Config, *identities: str) -> None:
    """The sync record as a sitting that asked about ``identities`` left it."""
    document = sync_cli.load_record(cfg)
    document["labels"][SLUG] = {"asked": list(identities)}
    sync_cli.write_record(cfg, document)


def live_shape(cfg: config.Config, monkeypatch, *, line: str = "Rawax", **kwargs: Any):
    """Sitting 94's listing: 112 other lines, 3 RAWAXXX newest, 4 Rawax, all 7 asked."""
    held = [*rawaxxx(), *rawax(line)]
    fake = bind(monkeypatch, [*held, *others(112)], **kwargs)
    asked(cfg, *(one.id for one in held))
    return fake


def next_rawax() -> tuple[int, dict]:
    return drive(["label", "sync", "--next", "--label", LABEL])


def check(envelope: dict, key: str) -> dict:
    (found,) = [one for one in envelope["data"]["checks"] if one["key"] == f"label.sync.{key}"]
    return found


def sweep_job() -> tuple[int, str]:
    job_id = queued_sweep()
    code, _resumed = drive(["sync", "labels", "--job", job_id])
    return code, job_id


def item_cause(job_id: str):
    with jobs.open_store() as store:
        (item,) = jobs.items(store, job_id)
    return item.cause


def filed(cfg: config.Config) -> list[review.Item]:
    with review.open_store(cfg) as store:
        return list(review.list_items(store, queue=str(Queue.LABEL_RELEASE), limit=None))


# ═══════════════════════════════════════════════════════════════════════════
# 1. The guided sync, ``--next``
# ═══════════════════════════════════════════════════════════════════════════


def test_the_live_shape_answers_nothing_new_rather_than_refusing(installed, monkeypatch):
    live_shape(installed, monkeypatch)

    code, envelope = next_rawax()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["question"] is None
    line = check(envelope, f"label.{SLUG}")
    assert line["status"] == "ok"
    assert "nothing new since it was last asked" in line["detail"]


def test_the_record_names_the_release_re_verified_and_what_it_answered(
    installed, monkeypatch
):
    fake = live_shape(installed, monkeypatch)

    _code, envelope = next_rawax()

    canary = check(envelope, f"canary.{SLUG}")
    assert canary["status"] == "info"
    assert "a1" in canary["detail"] and "Release a1" in canary["detail"]
    assert "answered confirmed" in canary["detail"]
    # ONE held release was verified again, and it was a Rawax one: none of
    # the RAWAXXX releases, newest though they are, was asked.
    held_asked = [one for one in fake.verified if one.startswith(("a", "x"))]
    assert held_asked == ["a1"]


def test_four_held_releases_whose_line_is_the_label_answer_nothing_new(installed, monkeypatch):
    """The brief's literal fixture: 115 other lines and 4 held Rawax."""
    held = rawax()
    bind(monkeypatch, [*held, *others(115)])
    asked(installed, *(one.id for one in held))

    code, envelope = next_rawax()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"


def test_held_releases_whose_lines_name_another_act_still_refuse(installed, monkeypatch):
    fake = live_shape(installed, monkeypatch, line="2025 Moon Harbour")

    code, envelope = next_rawax()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unlisted"
    line = check(envelope, f"label.{SLUG}")
    assert line["status"] == "fail"
    assert "read 119 release(s)" in line["detail"]
    assert "could not confirm a single one" in line["detail"]
    canary = check(envelope, f"canary.{SLUG}")
    assert "release x0, answered mismatch (credited as 'RAWAXXX')" in canary["detail"]
    assert len([one for one in fake.verified if one.startswith(("a", "x"))]) == 1
    assert sync_cli.load_record(installed)["labels"][SLUG] == {
        "asked": ["x0", "x1", "x2", "a1", "a2", "a3", "a4"]
    }


def test_a_dead_verifier_still_refuses_though_a_held_line_names_the_label(
    installed, monkeypatch
):
    live_shape(installed, monkeypatch, dead=True)

    code, envelope = next_rawax()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unlisted"
    canary = check(envelope, f"canary.{SLUG}")
    assert "a1" in canary["detail"]
    assert "answered unconfirmed" in canary["detail"]
    assert "the verification endpoint answered nothing" in canary["detail"]


def test_a_listing_with_no_release_held_asks_no_canary_and_says_none(installed, monkeypatch):
    bind(monkeypatch, others(5))

    code, envelope = next_rawax()

    assert envelope["cause"]["reason"] == "label-sync-unlisted", envelope
    assert code == int(ExitCode.PRECONDITION)
    assert [one for one in envelope["data"]["checks"] if "canary" in one["key"]] == []


# ═══════════════════════════════════════════════════════════════════════════
# 2. The sweep worker, the go's twin of the refusal
# ═══════════════════════════════════════════════════════════════════════════


def test_the_worker_answers_the_live_shape_as_nothing_new(installed, monkeypatch):
    live_shape(installed, monkeypatch)

    code, job_id = sweep_job()

    assert code == int(ExitCode.OK)
    assert item_cause(job_id) is None
    assert filed(installed) == []


def test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary(
    installed, monkeypatch
):
    live_shape(installed, monkeypatch, line="2025 Moon Harbour")

    code, job_id = sweep_job()

    assert code != int(ExitCode.OK)
    cause = item_cause(job_id)
    assert cause.reason == "label-sweep-incomplete"
    assert cause.detail["read"] == 119
    # Every held line names another act, so the newest is asked, as before.
    assert cause.detail["canary"]["identity"] == "x0"
    assert cause.detail["canary"]["verdict"] == "mismatch"
    assert "Release x0" in cause.message
    assert "credited as 'RAWAXXX'" in cause.message
    assert filed(installed) == []


def test_the_worker_refuses_a_dead_verifier_over_held_lines_that_name_the_label(
    installed, monkeypatch
):
    live_shape(installed, monkeypatch, dead=True)

    code, job_id = sweep_job()

    assert code != int(ExitCode.OK)
    cause = item_cause(job_id)
    assert cause.reason == "label-sweep-incomplete"
    assert cause.detail["canary"]["verdict"] == "unconfirmed"
    assert filed(installed) == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. The engine: which held release is the canary
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def entry(installed):
    return labels.RegistryStore().load().by_id(SLUG)


def listing_of(cfg, entry, releases, held, *, verify=None) -> tuple[sweep.LabelListing, list[str]]:
    fake = LineCatalogue()
    found = sweep.list_for_label(
        cfg,
        entry,
        artist=FakePagedArtist(releases),
        verify=verify or fake.search_release,
        offered=frozenset(held),
    )
    return found, fake.verified


def test_the_canary_is_a_held_release_whose_line_the_needle_confirms(installed, entry):
    releases = [*rawaxxx(), *rawax(), *others(3)]
    held = {one.id for one in [*rawaxxx(), *rawax()]}
    found, verified = listing_of(installed, entry, releases, held)

    assert found.canary is not None
    assert (found.canary.identity, found.canary.verdict) == ("a1", "confirmed")
    assert found.held_unconfirmed == 0
    assert "x0" not in verified


def test_with_no_held_line_naming_the_label_a_held_release_with_no_line_comes_next(
    installed, entry
):
    lineless = release("n1", "2025", "")
    releases = [*rawaxxx(), lineless, *others(3)]

    def confirm_lineless(claimed, one):
        if one.id == "n1":
            return {"resolved_label": "Rawax", "source": "fixture"}
        return LineCatalogue().search_release(claimed, one)

    found, _ = listing_of(installed, entry, releases, {"x0", "n1"}, verify=confirm_lineless)

    assert found.canary.identity == "n1"
    assert found.held_unconfirmed == 0


def test_with_every_held_line_naming_another_act_the_newest_is_asked_and_all_count(
    installed, entry
):
    releases = [*rawaxxx(), *others(3)]
    found, verified = listing_of(installed, entry, releases, {"x1", "x2", "x0"})

    assert found.canary.identity == "x0"
    assert found.canary.verdict == "mismatch"
    assert found.held_unconfirmed == 3
    assert len(found.dropped) == 3
    assert verified.count("x0") == 1


def test_no_canary_is_asked_when_the_sweep_confirmed_something(installed, entry):
    releases = [*rawax(), *others(3)]
    found, verified = listing_of(installed, entry, releases, {"a1"})

    assert found.canary is None
    assert "a1" not in verified
    assert [one.identity for one in found.candidates] == ["a2", "a3", "a4"]
