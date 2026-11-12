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

R-1634 closed the case U277 left: with every held release carrying a line,
the one re-verified was judged from it with no provider read, so a provider
answering album reads with no line left the label saying nothing new. When a
drop is not a mismatch, the held release is now read again from the provider
through the catalogue's ``reread_release``, and the ``reverified`` line says
whether an answer came from the provider or from the release's own line.

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

    #: The shipped forced read (R-1634) and the album read it makes, so a held
    #: release re-verified is read from ``_session`` whatever line it carries.
    reread_release = tidal_catalogue.TidalCatalogue.reread_release
    _album = tidal_catalogue.TidalCatalogue._album


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

    No held release lacks a line. On U277 the newest held, a RAWAXXX one, was
    judged from its line and answered mismatch; since R-1634 a held ``Rawax``
    one is read again from the provider, which answers it with no line, so the
    label still refuses, now naming the provider's answer.
    """
    held = [*rawaxxx(), *rawax()]
    session = Session(degraded=True)
    bind(monkeypatch, [*(lineless(f"m{n}") for n in range(3)), *held, *others(112)], session=session)
    asked(installed, *(one.id for one in held))

    code, envelope = next_rawax()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unlisted"
    reverified = check(envelope, f"reverified.{SLUG}")["detail"]
    assert "release a1, answered unconfirmed" in reverified
    assert "read again from the provider" in reverified


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


# ═══════════════════════════════════════════════════════════════════════════
# 4. R-1634: the release re-verified is read from the provider, never its line
# ═══════════════════════════════════════════════════════════════════════════


def every_line_shape(cfg: config.Config, monkeypatch, session: Session, *, also: list | None = None):
    """Three new releases with no line over four held ``Rawax`` ones, and no held one lineless."""
    held = [*(also or []), *rawax()]
    new = [lineless(f"m{n}") for n in range(3)]
    fake = bind(monkeypatch, [*new, *held, *others(112)], session=session)
    asked(cfg, *(one.id for one in held))
    return fake


def test_a_degraded_provider_refuses_though_every_held_line_names_the_label(
    installed, monkeypatch
):
    """The defect: on ``main`` the held ``a1`` was judged from its line and the label said nothing new."""
    session = Session({"a1": "2025 Rawax"}, degraded=True)
    every_line_shape(installed, monkeypatch, session)

    code, envelope = next_rawax()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unlisted"
    reverified = check(envelope, f"reverified.{SLUG}")["detail"]
    assert "release a1, answered unconfirmed (no label credit)" in reverified
    assert "read again from the provider" in reverified
    # THE PROVIDER WAS READ FOR THE HELD RELEASE, though its line names the label.
    assert session.reads == ["m0", "m1", "m2", "a1"]


def test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label(
    installed, monkeypatch
):
    session = Session({"a1": "2025 Rawax"}, degraded=True)
    every_line_shape(installed, monkeypatch, session)

    code, job_id = sweep_job()

    assert code != int(ExitCode.OK)
    cause = item_cause(job_id)
    assert cause.reason == "label-sweep-incomplete"
    assert cause.detail["reverified"]["identity"] == "a1"
    assert cause.detail["reverified"]["verdict"] == "unconfirmed"
    assert cause.detail["reverified"]["basis"] == sweep.READ_PROVIDER
    assert "read again from the provider" in cause.message
    assert "a1" in session.reads
    assert filed(installed) == []


def test_a_provider_crediting_another_label_still_answers_nothing_new(installed, monkeypatch):
    """Every drop a mismatch: the held line shows the needle right, and no held release is read."""
    session = Session({f"m{n}": "2026 Moon Harbour" for n in range(3)})
    every_line_shape(installed, monkeypatch, session)

    code, envelope = next_rawax()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    reverified = check(envelope, f"reverified.{SLUG}")["detail"]
    assert reverified.endswith("release a1, answered confirmed")
    # SAID: the answer came from the release's own line, not from the provider.
    assert "from its own copyright line, with no provider read" in reverified
    assert session.reads == ["m0", "m1", "m2"]


def test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new(
    installed, monkeypatch
):
    """The real nothing new kept: the provider reads the held release and credits the label.

    The new releases genuinely carry no credit, the provider answers the held
    one's read with its line, so the label has nothing new. The RAWAXXX holds
    newest are passed over for a held ``Rawax`` line, which a healthy read
    confirms, so R-1635's false refusal clears too.
    """
    session = Session({one.id: "2025 Rawax" for one in rawax()})
    every_line_shape(installed, monkeypatch, session, also=rawaxxx())

    code, envelope = next_rawax()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    reverified = check(envelope, f"reverified.{SLUG}")["detail"]
    assert "release a1, answered confirmed" in reverified
    assert "read again from the provider" in reverified
    assert session.reads == ["m0", "m1", "m2", "a1"]


def test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release(
    installed, monkeypatch
):
    session = Session({one.id: "2025 Rawax" for one in rawax()})
    every_line_shape(installed, monkeypatch, session, also=rawaxxx())

    code, job_id = sweep_job()

    assert code == int(ExitCode.OK)
    assert item_cause(job_id) is None
    assert filed(installed) == []
    assert "a1" in session.reads


def test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified(installed, entry):
    """A sweep handed only a verifier cannot read the provider for a held release with a line.

    So it is not asked, and the listing counts as one that confirmed nothing,
    rather than answering nothing new from the line.
    """
    releases = [lineless("m1"), *rawax(), *others(3)]
    fake = LineCatalogue(session=Session({"a1": "2025 Rawax"}))
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(releases),
        verify=fake.search_release,
        offered=frozenset({"a1", "a2", "a3", "a4"}),
    )

    assert found.canary is not None
    assert found.canary.identity == "a1"
    assert not found.canary.confirmed
    assert found.canary.basis == sweep.READ_NONE
    assert found.held_unconfirmed == 4
    assert "a1" not in fake.verified


def test_the_forced_read_is_asked_only_when_a_drop_is_not_a_mismatch(installed, entry):
    """Every drop a mismatch: the ordinary verifier is asked, and the forced read never."""
    releases = [*rawax(), *others(3)]
    fake = LineCatalogue(session=Session({"a1": "2025 Rawax"}))
    reread: list[str] = []

    def forced(claimed, one):
        reread.append(one.id)
        return fake.reread_release(claimed, one)

    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(releases),
        verify=fake.search_release,
        reread=forced,
        offered=frozenset({"a1", "a2", "a3", "a4"}),
    )

    assert (found.canary.identity, found.canary.verdict) == ("a1", "confirmed")
    assert found.canary.basis == sweep.READ_LINE
    assert reread == []
    assert fake._session.reads == []


def test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts(
    installed, entry
):
    """No held release lacks a line: a held ``Rawax`` is read, not the newer RAWAXXX."""
    releases = [lineless("m1"), *rawaxxx(), *rawax(), *others(3)]
    fake = LineCatalogue(session=Session({"a1": "2025 Rawax"}))
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(releases),
        verify=fake.search_release,
        reread=fake.reread_release,
        offered=frozenset({"x0", "x1", "x2", "a1", "a2", "a3", "a4"}),
    )

    assert (found.canary.identity, found.canary.verdict) == ("a1", "confirmed")
    assert found.canary.basis == sweep.READ_PROVIDER
    assert found.held_unconfirmed == 0
    assert fake._session.reads == ["m1", "a1"]


# ═══════════════════════════════════════════════════════════════════════════
# 5. The seam: ``TidalCatalogue.reread_release``
# ═══════════════════════════════════════════════════════════════════════════


class Gone(Exception):
    """Named as the provider's client names a release it does not have."""


class GoneNotFound(Gone):
    pass


def test_the_shipped_reread_reads_the_provider_though_the_release_carries_a_line(installed):
    session = Session({"a1": "2025 Moon Harbour"})
    found = tidal_catalogue.TidalCatalogue(session)

    answer = found.reread_release(LABEL, release("a1", "2025", "Rawax"))

    assert session.reads == ["a1"]
    assert answer["resolved_label"] == "Moon Harbour"
    # The ordinary read judges the same release from its line, with no call.
    assert found.search_release(LABEL, release("a1", "2025", "Rawax"))["resolved_label"] == "Rawax"
    assert session.reads == ["a1"]


def test_the_shipped_reread_of_a_release_the_provider_no_longer_has_is_no_credit(installed):
    class Withdrawn(Session):
        def album(self, identity):
            self.reads.append(identity)
            raise GoneNotFound(identity)

    session = Withdrawn()
    answer = tidal_catalogue.TidalCatalogue(session).reread_release(LABEL, release("a1", "2025", "Rawax"))

    assert answer["verdict"] == catalogue.RELEASE_GONE
    assert answer["resolved_label"] == ""
    assert session.reads == ["a1"]


def test_the_shipped_reread_of_a_release_with_no_identifier_reads_nothing(installed):
    session = Session({"": "2025 Rawax"})
    answer = tidal_catalogue.TidalCatalogue(session).reread_release(LABEL, release("", "2025", "Rawax"))

    assert answer["verdict"] == "unconfirmed"
    assert session.reads == []


class ReadFails(LineCatalogue):
    """A provider whose forced read raises, as ``listing.fetch_with_retry`` does once its ladder is spent."""

    def reread_release(self, claimed: str, release: Any) -> dict:
        raise RuntimeError("the provider stopped answering album reads")


def test_a_forced_read_that_raises_fails_the_item_in_the_lookup_vocabulary(
    installed, monkeypatch
):
    """The forced read is wrapped as the verifier is, so a provider failure is never an internal error."""
    held = rawax()
    fake = ReadFails(
        artists={SLUG: FakePagedArtist([lineless("m0"), *held, *others(3)])},
        session=Session(),
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    asked(installed, *(one.id for one in held))

    code, job_id = sweep_job()

    assert code != int(ExitCode.OK)
    assert item_cause(job_id).reason == "sync-source-lookups-failed"
    assert filed(installed) == []


# ═══════════════════════════════════════════════════════════════════════════
# 6. A held release the provider has withdrawn (round one of R-1634's review)
# ═══════════════════════════════════════════════════════════════════════════


class PartlyGone(Session):
    """A healthy provider that no longer has the releases named in ``gone``."""

    def __init__(self, lines: dict[str, str], gone: set[str]) -> None:
        super().__init__(lines)
        self.gone = set(gone)

    def album(self, identity: str) -> FakeRelease:
        if identity in self.gone:
            self.reads.append(identity)
            raise GoneNotFound(identity)
        return super().album(identity)


def withdrawn_shape(cfg, monkeypatch, *, gone: set[str]) -> PartlyGone:
    """The new releases genuinely uncredited, the held ones credited ``Rawax`` unless withdrawn."""
    session = PartlyGone({one.id: "2025 Rawax" for one in rawax()}, gone)
    every_line_shape(cfg, monkeypatch, session)
    return session


def test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new(
    installed, monkeypatch
):
    """A kept listing still lists ``a1`` after the provider withdrew it: ``a2`` is read in its place."""
    session = withdrawn_shape(installed, monkeypatch, gone={"a1"})

    code, envelope = next_rawax()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    reverified = check(envelope, f"reverified.{SLUG}")["detail"]
    assert "release a2, answered confirmed" in reverified
    assert "read again from the provider" in reverified
    # ONE more read, and only because the first answered gone.
    assert session.reads == ["m0", "m1", "m2", "a1", "a2"]


def test_the_worker_passes_over_a_withdrawn_held_release_too(installed, monkeypatch):
    session = withdrawn_shape(installed, monkeypatch, gone={"a1"})

    code, job_id = sweep_job()

    assert code == int(ExitCode.OK)
    assert item_cause(job_id) is None
    assert filed(installed) == []
    assert session.reads[-2:] == ["a1", "a2"]


def test_two_withdrawn_held_releases_refuse_and_no_third_is_read(installed, monkeypatch):
    session = withdrawn_shape(installed, monkeypatch, gone={"a1", "a2"})

    code, envelope = next_rawax()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unlisted"
    reverified = check(envelope, f"reverified.{SLUG}")["detail"]
    assert "release a2, answered gone" in reverified
    assert session.reads == ["m0", "m1", "m2", "a1", "a2"]


def test_a_lone_withdrawn_held_release_refuses(installed, entry):
    releases = [lineless("m1"), release("a1", "2025", "Rawax"), *others(3)]
    fake = LineCatalogue(session=PartlyGone({}, {"a1"}))
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(releases),
        verify=fake.search_release,
        reread=fake.reread_release,
        offered=frozenset({"a1"}),
    )

    assert (found.canary.identity, found.canary.verdict) == ("a1", catalogue.RELEASE_GONE)
    assert found.held_unconfirmed == 1


# ═══════════════════════════════════════════════════════════════════════════
# 7. What the answer rested on, and where the forced read comes from
# ═══════════════════════════════════════════════════════════════════════════


def test_every_drop_a_mismatch_over_a_held_release_with_no_line_says_the_provider_was_read(
    installed, entry
):
    """No held line names the label, so the lineless one is asked, and the catalogue reads it."""
    releases = [*rawaxxx(), lineless("n1"), *others(3)]
    fake = LineCatalogue(session=Session({"n1": "2025 Rawax"}))
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(releases),
        verify=fake.search_release,
        offered=frozenset({"x0", "n1"}),
    )

    assert {one.reason for one in found.dropped} == {"mismatch"}
    assert (found.canary.identity, found.canary.verdict) == ("n1", "confirmed")
    assert found.canary.basis == sweep.READ_PROVIDER


def test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read(installed, entry):
    """The verifier handed in is the one asked, so the catalogue's forced read is not taken."""
    held = rawax()
    fake = LineCatalogue(
        artists={SLUG: FakePagedArtist([lineless("m0"), *held, *others(3)])},
        session=Session({"a1": "2025 Rawax"}),
    )
    source = sweep.LabelSource(
        installed,
        registry=labels.Registry(labels={SLUG: entry}),
        catalogue=fake,
        verify=fake.search_release,
        offered=frozenset(one.id for one in held),
    )

    source.list_recent(10)

    ((_, listing),) = source.listings
    assert listing.canary.basis == sweep.READ_NONE
    assert listing.held_unconfirmed == 4
    assert fake._session.reads == ["m0"]
