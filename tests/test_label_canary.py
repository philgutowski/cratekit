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

When every release the sweep turned down is a mismatch, the verifier
answered each with another label's name, so the only question left is
whether the needle still names anything of the label's, and a held release
whose own line it names answers that. When the verifier gave no answer for
some release, the held release re-verified is one the provider is READ for,
one with no line first, since the real catalogue judges a release carrying a
line from that line alone (round one of U277's review). These tests verify
through the shipped catalogue's own read over a fake session, and drive both
the guided ``--next`` and the sweep worker.

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


class Session:
    """The provider's album read, which the real catalogue makes only for a release with no line.

    ``lines`` is what each album read credits when the provider answers.
    ``degraded`` is a provider that answers the read with no copyright line
    at all, which the verifier then reads as no label credit: the endpoint the
    refusal exists for. ``reads`` records every album read made.
    """

    def __init__(self, lines: dict[str, str] | None = None, *, degraded: bool = False) -> None:
        self.lines = dict(lines or {})
        self.degraded = degraded
        self.reads: list[str] = []

    def album(self, identity: str) -> FakeRelease:
        self.reads.append(identity)
        line = "" if self.degraded else self.lines.get(identity, "")
        return FakeRelease(identity, copyright=line)


class LineCatalogue(FakeCatalogue):
    """Verifies a release through the shipped catalogue's own read, over a fake session.

    So a release carrying a line is judged from that line with no provider
    call, and one with none is read again from ``_session``, exactly as a live
    sweep verifies. ``verified`` records each release asked.
    """

    def __init__(self, *args: Any, session: Session | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._session = session or Session()
        self.verified: list[str] = []

    def search_release(self, claimed: str, release: Any) -> dict:
        self.verified.append(str(release.id))
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

    canary = check(envelope, f"reverified.{SLUG}")
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
    canary = check(envelope, f"reverified.{SLUG}")
    assert "release x0, answered mismatch (credited as 'RAWAXXX')" in canary["detail"]
    assert len([one for one in fake.verified if one.startswith(("a", "x"))]) == 1
    assert sync_cli.load_record(installed)["labels"][SLUG] == {
        "asked": ["x0", "x1", "x2", "a1", "a2", "a3", "a4"]
    }


def lineless(identity: str, year: str = "2026") -> FakeRelease:
    return release(identity, year, "")


def unanswered_shape(cfg: config.Config, monkeypatch, session: Session) -> LineCatalogue:
    """Round one's shape: three new releases with no line, one held with none, four Rawax.

    The held ``n0`` was taken when the provider answered its read with
    ``2025 Rawax``. Whatever the provider now answers for the new ones, the
    four held Rawax lines say only that the needle is right, never that the
    provider is answering.
    """
    held = [lineless("n0"), *rawax()]
    new = [lineless(f"m{n}") for n in range(3)]
    fake = bind(monkeypatch, [*new, *held, *others(112)], session=session)
    asked(cfg, *(one.id for one in held))
    return fake


def test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label(
    installed, monkeypatch
):
    session = Session({"n0": "2025 Rawax"}, degraded=True)
    unanswered_shape(installed, monkeypatch, session)

    code, envelope = next_rawax()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unlisted"
    reverified = check(envelope, f"reverified.{SLUG}")
    assert "release n0, answered unconfirmed (no label credit)" in reverified["detail"]
    # THE PROVIDER WAS READ FOR THE RELEASE RE-VERIFIED, not only for the new ones.
    assert "n0" in session.reads


def test_a_provider_that_answers_turns_the_same_shape_into_nothing_new(installed, monkeypatch):
    """The new releases' reads credit another label, and the held one's credits Rawax."""
    lines = {"n0": "2025 Rawax", **{f"m{n}": "2026 Moon Harbour" for n in range(3)}}
    session = Session(lines)
    unanswered_shape(installed, monkeypatch, session)

    code, envelope = next_rawax()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    # Every drop named another label, so the verifier is answering and a held
    # Rawax line is what shows the needle right; the held n0 is never read.
    assert check(envelope, f"reverified.{SLUG}")["detail"].endswith(
        "release a1, answered confirmed"
    )
    assert session.reads == ["m0", "m1", "m2"]


def test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before(
    installed, monkeypatch
):
    """Sitting 94's shape with three new releases the provider answers with no line.

    No held release lacks a line, so nothing held can show the provider
    answering: the newest held is asked, as on main, and it is a RAWAXXX one.
    """
    held = [*rawaxxx(), *rawax()]
    session = Session(degraded=True)
    bind(monkeypatch, [*(lineless(f"m{n}") for n in range(3)), *held, *others(112)], session=session)
    asked(installed, *(one.id for one in held))

    code, envelope = next_rawax()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unlisted"
    assert "release x0, answered mismatch" in check(envelope, f"reverified.{SLUG}")["detail"]


def test_a_listing_with_no_release_held_asks_no_canary_and_says_none(installed, monkeypatch):
    bind(monkeypatch, others(5))

    code, envelope = next_rawax()

    assert envelope["cause"]["reason"] == "label-sync-unlisted", envelope
    assert code == int(ExitCode.PRECONDITION)
    assert [one for one in envelope["data"]["checks"] if "reverified" in one["key"]] == []


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
    assert cause.detail["reverified"]["identity"] == "x0"
    assert cause.detail["reverified"]["verdict"] == "mismatch"
    assert "Release x0" in cause.message
    assert "credited as 'RAWAXXX'" in cause.message
    assert filed(installed) == []


def test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label(
    installed, monkeypatch
):
    session = Session({"n0": "2025 Rawax"}, degraded=True)
    unanswered_shape(installed, monkeypatch, session)

    code, job_id = sweep_job()

    assert code != int(ExitCode.OK)
    cause = item_cause(job_id)
    assert cause.reason == "label-sweep-incomplete"
    assert cause.detail["reverified"]["identity"] == "n0"
    assert cause.detail["reverified"]["verdict"] == "unconfirmed"
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


def test_with_every_drop_a_mismatch_a_held_labels_line_is_asked_before_one_with_none(
    installed, entry
):
    """Every drop carried another label's name, so the verifier is answering.

    The held release with no line is newest, and its read credits nothing; the
    held Rawax line below it is the one that shows the needle still names the
    label's releases.
    """
    releases = [lineless("n1"), *rawax(), *others(3)]
    fake = LineCatalogue()
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(releases),
        verify=fake.search_release,
        offered=frozenset({"n1", "a1", "a2", "a3", "a4"}),
    )

    assert {one.reason for one in found.dropped} == {"mismatch"}
    assert (found.canary.identity, found.canary.verdict) == ("a1", "confirmed")
    assert found.held_unconfirmed == 0


def test_with_a_drop_the_verifier_gave_no_answer_for_a_held_release_with_no_line_is_asked(
    installed, entry
):
    """A held Rawax line is judged from the line alone and says nothing of the provider."""
    releases = [lineless("m1"), lineless("n1"), *rawax(), *others(3)]
    fake = LineCatalogue(session=Session(degraded=True))
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(releases),
        verify=fake.search_release,
        offered=frozenset({"n1", "a1", "a2", "a3", "a4"}),
    )

    assert "unconfirmed" in {one.reason for one in found.dropped}
    assert (found.canary.identity, found.canary.verdict) == ("n1", "unconfirmed")
    assert found.held_unconfirmed == 5
    assert fake._session.reads == ["m1", "n1"]


def test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label(
    installed, monkeypatch
):
    """The newest held line names the label and an older held release has none.

    The read the new release failed on is the provider's, so the held release
    the provider is read for is asked, not the newest, which its own line
    would confirm with no provider call (round two of U277's review, P8).
    """
    held = [*rawax(), lineless("n0", "2024")]
    session = Session({"n0": "2024 Rawax"}, degraded=True)
    bind(monkeypatch, [lineless("m0"), *held, *others(3)], session=session)
    asked(installed, *(one.id for one in held))

    code, envelope = next_rawax()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unlisted"
    assert "release n0, answered unconfirmed" in check(envelope, f"reverified.{SLUG}")["detail"]
    assert session.reads == ["m0", "n0"]
