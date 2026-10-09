"""U107: ``crate label sync`` asks, label by label, about what is new, and records each answer.

The guided label sync's asking half, cut from the author's brainstorm of
2026-10-02. Every scenario the brief names is driven here through the real
dispatcher with a fake provider, a fake general catalogue where the gate is in
play, and a scripted prompter where the question is put at a terminal.

NOTHING HERE DOWNLOADS. A taken release is an accepted review item and a line
in the sync record, and that is all this unit produces.

NOTHING HERE REACHES A NETWORK. The root fixtures fail any test that does.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from cratekit.cli import prompt, registry
from cratekit.core import config, review, tombstone
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.jobs import Parked
from cratekit.core.review import DecisionStore, Queue
from cratekit.label import catalogue, sweep, sync_cli
from cratekit.label import registry as labels
from cratekit.sync import run
from cratekit.tagging import published
from tests.cli_drive import drive, drive_human
from tests.label_fakes import FakeCatalogue, FakePagedArtist, FakeRelease, catalogue_factory
from tests.test_config import valid_data
from tests.test_label_workers import queued_sweep

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"

LABEL = "Tide Works"
SLUG = "tide-works"
QUEUE = str(Queue.LABEL_RELEASE)


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures and fakes
# ═══════════════════════════════════════════════════════════════════════════


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
    return resolved


class Track:
    """A provider row the provider reader reads, with a duration and no ISRC.

    No ISRC on purpose: the genre gate then asks the general catalogue
    nothing, which is the shape most of these scenarios want. The gate
    scenario gives its rows an ISRC and binds a lookup.
    """

    def __init__(
        self, track_id: str, artist: str, name: str, *, duration: int = 360, isrc: str = ""
    ) -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = isrc
        self.duration = duration


def rows_for(release_id: str, count: int, *, isrc: str = "") -> list[Track]:
    return [
        Track(f"t-{release_id}-{n}", "Label Act", f"Cut {n} of {release_id}", isrc=isrc)
        for n in range(1, count + 1)
    ]


class Provider(FakeCatalogue):
    """A fake catalogue that can be told to refuse one label as the gate would."""

    def __init__(self, *args, parked: set[str] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parked = set(parked or ())

    def artist_for(self, entry):
        label_id = str(getattr(entry, "label_id", entry))
        if label_id in self.parked:
            self.asked_for.append(label_id)
            raise Parked(
                Cause(
                    reason="provider-cooldown",
                    message="the streaming provider rate limited this account",
                    remediation=Remediation(remedy=Remedy.RETRY_LATER),
                    origin=("provider_gate",),
                )
            )
        return super().artist_for(entry)


def bind(
    monkeypatch,
    catalogue_by_label: dict[str, list[tuple[str, str, int]]],
    **kwargs,
) -> Provider:
    """Labels keyed by identifier, each a list of ``(release_id, year, tracks)``."""
    fake = Provider(
        artists={
            label_id: FakePagedArtist(
                [FakeRelease(rid, year=year) for rid, year, _count in releases]
            )
            for label_id, releases in catalogue_by_label.items()
        },
        releases={
            rid: (rows_for(rid, count), int(year))
            for releases in catalogue_by_label.values()
            for rid, year, count in releases
        },
        **kwargs,
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def register(name: str = LABEL, *argv: str) -> None:
    code, envelope = drive(["label", "registry", "add", name, *argv])
    assert code == int(ExitCode.OK), envelope


def three_new(monkeypatch) -> Provider:
    return bind(monkeypatch, {SLUG: [("r3", "2026", 4), ("r2", "2025", 2), ("r1", "2024", 1)]})


class Scripted:
    """A terminal that answers from a list and keeps what was written to it."""

    def __init__(self, answers: list[str]) -> None:
        self.answers = list(answers)
        self.said: list[str] = []

    def read_line(self) -> str:
        if not self.answers:
            raise EOFError("standard input is at end of file")
        return self.answers.pop(0) + "\n"

    def write(self, text: str) -> None:
        self.said.append(text)

    @property
    def shown(self) -> str:
        return "".join(self.said)


def script(monkeypatch, *answers: str) -> Scripted:
    scripted = Scripted(list(answers))
    monkeypatch.setattr(
        sync_cli,
        "PROMPTER",
        lambda: prompt.Prompter(read_line=scripted.read_line, write=scripted.write),
    )
    return scripted


def sync(*argv: str) -> tuple[int, dict]:
    return drive(["label", "sync", *argv])


def next_question() -> dict | None:
    code, envelope = sync("--next")
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["summary"]["question"]


def answer(label: str, word: str, *releases: str) -> dict:
    argv = ["--answer", word, "--label", label]
    for one in releases:
        argv.extend(["--release", one])
    code, envelope = sync(*argv)
    assert code == int(ExitCode.OK), envelope
    (answered,) = envelope["data"]["summary"]["answered"]
    return answered


def record(cfg: config.Config) -> dict:
    return sync_cli.load_record(cfg)


def items(cfg: config.Config) -> dict[str, review.Item]:
    with review.open_store(cfg) as store:
        page = review.list_items(
            store, queue=QUEUE, include_resolved=True, include_suppressed=True, limit=None
        )
    return {str(item.payload.get("identity") or item.item_id): item for item in page.items}


def open_items(cfg: config.Config) -> list[review.Item]:
    with review.open_store(cfg) as store:
        return list(review.list_items(store, queue=QUEUE, limit=None).items)


def offered(cfg: config.Config, release_id: str, *, label_id: str = SLUG, **payload) -> str:
    """One release in review as the old sweep left it. Returns the item id."""
    with review.open_store(cfg) as store:
        item = sweep.offer_release(
            store,
            run.Candidate(
                identity=release_id,
                recency="2023",
                payload={
                    "artist": "Label Act",
                    "title": f"Release {release_id}",
                    "label_id": label_id,
                    "label_name": LABEL,
                    "identity": release_id,
                    **payload,
                },
            ),
            run_id="old-sweep",
        )
    return item.item_id


def tombstones(cfg: config.Config) -> int:
    return len(list(DecisionStore(tombstone.STORE_KEY, cfg).suppressions()))


def checks(envelope: dict, prefix: str) -> list[dict]:
    return [one for one in envelope["data"]["checks"] if one["key"].startswith(f"label.sync.{prefix}")]


def walked() -> list[str]:
    """A walk that answered every label, which ends at U108's one gate.

    Returns the lines the walk said about each label, which the refusal
    carries in front of the summary, so a test reads what the walk did from
    exactly what a person deciding is shown.
    """
    code, envelope = sync()
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    detail = envelope["cause"]["detail"]
    assert detail["gate"] == "label.sync.confirm"
    return detail["shown"]["answered_this_run"]


def line_for(lines: list[str], name: str) -> str:
    (found,) = [one for one in lines if one.startswith(f"{name}: ")]
    return found


# ═══════════════════════════════════════════════════════════════════════════
# 1. The brief's scenarios, through the structured path
# ═══════════════════════════════════════════════════════════════════════════


def test_a_label_with_three_new_releases_is_asked_once(installed, monkeypatch):
    register()
    fake = three_new(monkeypatch)

    question = next_question()

    assert question is not None
    assert question["label_id"] == SLUG and question["label_name"] == LABEL
    assert [one["identity"] for one in question["releases"]] == ["r3", "r2", "r1"]
    assert question["new"] == 3
    assert question["tracks"] == 7
    assert question["size"] == 7 * 360 * sync_cli.BYTES_PER_SECOND
    assert question["answers"] == ["all", "pick", "not-now", "stop"]
    assert fake.asked_for == [SLUG]

    answered = answer(SLUG, "all")

    assert answered["taken"] == ["r3", "r2", "r1"]
    assert answered["tracks"] == 7
    held = record(installed)["labels"][SLUG]
    assert sorted(held["asked"]) == ["r1", "r2", "r3"]
    assert held["answer"] == "all" and "pending" not in held
    filed = items(installed)
    assert {rid: filed[rid].verdict for rid in ("r1", "r2", "r3")} == {
        rid: review.Verdict.ACCEPTED for rid in ("r1", "r2", "r3")
    }
    assert all(filed[rid].actor == sync_cli.ACTOR for rid in ("r1", "r2", "r3"))

    # A SECOND RUN ASKS NOTHING ABOUT THOSE THREE, and lists the label to know.
    assert next_question() is None
    assert fake.asked_for == [SLUG, SLUG]


@pytest.mark.parametrize("word", ["all", "pick", "not-now", "stop"])
def test_after_any_answer_a_second_run_asks_nothing_about_those_releases(
    installed, monkeypatch, word
):
    register()
    three_new(monkeypatch)
    next_question()

    answer(SLUG, word, *(["r2"] if word == "pick" else []))

    if word == "stop":
        code, envelope = sync("--next")
        assert code == int(ExitCode.PRECONDITION), envelope
        assert envelope["cause"]["reason"] == "label-registry-empty"
    else:
        assert next_question() is None
    assert sorted(record(installed)["labels"][SLUG]["asked"]) == ["r1", "r2", "r3"]


def test_not_now_moves_the_marker_and_a_release_published_after_is_asked_next_run(
    installed, monkeypatch
):
    register()
    three_new(monkeypatch)
    next_question()
    answered = answer(SLUG, "not-now")
    assert answered["taken"] == [] and answered["offered"] == 3
    assert items(installed) == {}

    bind(monkeypatch, {SLUG: [("r4", "2027", 3), ("r3", "2026", 4), ("r2", "2025", 2), ("r1", "2024", 1)]})

    question = next_question()

    assert question is not None
    assert [one["identity"] for one in question["releases"]] == ["r4"]
    answer(SLUG, "all")
    assert sorted(record(installed)["labels"][SLUG]["asked"]) == ["r1", "r2", "r3", "r4"]
    assert list(items(installed)) == ["r4"]


def sweep_labels() -> None:
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed


def test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep(installed, monkeypatch):
    """The asked marker holds for the old sweep too, or a no comes back as catch up.

    Until U109 takes labels out of ``sync all``, ``sync labels`` still sweeps.
    A sweep that did not read the marker filed every release answered not now
    into review, and the next ``label sync`` asked about them again as open
    items, so a no did not stay a no.
    """
    register()
    three_new(monkeypatch)
    next_question()
    answer(SLUG, "not-now")
    bind(monkeypatch, {SLUG: [("r4", "2027", 3), ("r3", "2026", 4), ("r2", "2025", 2), ("r1", "2024", 1)]})

    sweep_labels()

    assert sorted(items(installed)) == ["r4"]
    question = next_question()
    assert [one["identity"] for one in question["releases"]] == ["r4"]


def test_a_release_the_sweep_filed_while_its_question_waited_is_settled_by_the_answer(
    installed, monkeypatch
):
    """A question saved by ``--next`` holds its releases under pending, not asked.

    A sweep that ran before the answer filed them, and a not now that settled
    only the items the question knew of left them open for the next catch up.
    """
    register()
    three_new(monkeypatch)
    next_question()
    sweep_labels()
    assert sorted(items(installed)) == ["r1", "r2", "r3"]

    answer(SLUG, "not-now")

    assert open_items(installed) == []
    assert {item.verdict for item in items(installed).values()} == {review.Verdict.SUPERSEDED}
    assert tombstones(installed) == 0
    assert next_question() is None


def test_a_walk_whose_gate_took_back_every_open_item_is_not_a_no_op(installed, monkeypatch):
    register()
    bind(monkeypatch, {SLUG: []})
    offered(installed, "r-old-hymn", published_genres=["Christian"])

    code, envelope = sync("--next")

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    (label_line,) = checks(envelope, f"label.{SLUG}")
    assert "1 open item(s) taken back by the genre gate" in label_line["detail"]
    assert open_items(installed) == []


def test_the_labels_sweep_refuses_an_unreadable_record_before_any_login(installed, monkeypatch):
    register()
    three_new(monkeypatch)
    resolved: list[object] = []
    monkeypatch.setattr(catalogue, "resolve", lambda cfg: resolved.append(cfg))
    path = config.state_path("label_sync", installed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json")

    job_id = queued_sweep()
    code, refused = drive(["sync", "labels", "--job", job_id])

    assert "label-sync-unusable" in json.dumps(refused)
    assert resolved == []
    assert items(installed) == {}


def test_pick_records_exactly_the_chosen_releases_and_no_others(installed, monkeypatch):
    register()
    three_new(monkeypatch)
    next_question()

    answered = answer(SLUG, "pick", "r3", "r1")

    assert answered["taken"] == ["r3", "r1"]
    filed = items(installed)
    assert set(filed) == {"r3", "r1"}
    assert all(item.verdict is review.Verdict.ACCEPTED for item in filed.values())
    assert tombstones(installed) == 0
    held = record(installed)["labels"][SLUG]
    assert sorted(held["asked"]) == ["r1", "r2", "r3"]
    (logged,) = record(installed)["answers"]
    assert logged["answer"] == "pick"
    assert [one["identity"] for one in logged["releases"]] == ["r3", "r1"]
    assert logged["tracks"] == 5


def test_stop_following_removes_the_label_and_records_no_download(installed, monkeypatch):
    register()
    three_new(monkeypatch)
    next_question()

    answered = answer(SLUG, "stop")

    assert answered["removed"] is True and answered["taken"] == []
    assert labels.RegistryStore().load().labels == {}
    assert items(installed) == {}
    assert tombstones(installed) == 0
    (logged,) = record(installed)["answers"]
    assert logged["answer"] == "stop" and logged["releases"] == []


def test_a_label_with_nothing_new_is_not_asked_and_a_run_with_nothing_to_ask_says_so(
    installed, monkeypatch
):
    register()
    bind(monkeypatch, {SLUG: []})

    code, envelope = sync("--next")

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["question"] is None
    (label_line,) = checks(envelope, f"label.{SLUG}")
    assert label_line["status"] == "ok"
    assert "nothing new since it was last asked" in label_line["detail"]
    (said,) = checks(envelope, "question")
    assert "no label has anything new to ask about" in said["detail"]
    assert record(installed)["labels"] == {}

    code, text = drive_human(["label", "sync", "--next"])
    assert code == int(ExitCode.OK)
    assert "nothing new" in text


def test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest(
    installed, monkeypatch
):
    register()
    bind(monkeypatch, {SLUG: [(f"r{year}", str(year), 1) for year in range(2026, 1976, -1)]})

    question = next_question()

    assert question is not None
    assert [one["identity"] for one in question["releases"]] == [
        f"r{year}" for year in range(2026, 2016, -1)
    ]
    assert question["new"] == installed.labels.offer_per_sweep == 10
    assert question["beyond"] == 40
    assert "40 more past this run's window" in checks(drive(["label", "sync", "--next"])[1], "question")[0]["detail"]


def test_a_labels_own_offer_bounds_a_first_question(installed, monkeypatch):
    register(LABEL, "--offer", "3")
    bind(monkeypatch, {SLUG: [(f"r{year}", str(year), 1) for year in range(2026, 2016, -1)]})

    question = next_question()

    assert [one["identity"] for one in question["releases"]] == ["r2026", "r2025", "r2024"]


# ═══════════════════════════════════════════════════════════════════════════
# 2. The genre gate, before a label is asked
# ═══════════════════════════════════════════════════════════════════════════


def test_a_release_the_genre_gate_holds_never_appears_in_a_question(installed, monkeypatch):
    register()
    fake = bind(monkeypatch, {SLUG: [("r-dance", "2026", 1), ("r-hymn", "2025", 1)]})
    fake.releases["r-dance"] = ([Track("t1", "Label Act", "Floor", isrc="ZZTST2600001")], 2026)
    fake.releases["r-hymn"] = ([Track("t2", "Label Act", "Psalm", isrc="ZZTST2600002")], 2025)
    table = {"ZZTST2600001": ("Dance",), "ZZTST2600002": ("Christian",)}

    def lookup(value):
        return published.Published(published.SOURCE, "matched", genres=table[str(value)])

    monkeypatch.setattr(published, "for_lookup", lambda: lookup)

    question = next_question()

    assert [one["identity"] for one in question["releases"]] == ["r-dance"]
    code, held = drive(["label", "held"])
    assert code == int(ExitCode.OK), held
    assert [one["release_id"] for one in held["data"]["summary"]["releases"]] == ["r-hymn"]

    answer(SLUG, "all")

    # THE HOLD STANDS, and the held release is not in the asked set either:
    # it was never offered, so a kind change can still bring it to a question.
    assert record(installed)["labels"][SLUG]["asked"] == ["r-dance"]
    code, held = drive(["label", "held"])
    assert [one["release_id"] for one in held["data"]["summary"]["releases"]] == ["r-hymn"]


def test_an_open_item_the_gate_would_now_hold_is_taken_back_before_the_question(
    installed, monkeypatch
):
    register()
    bind(monkeypatch, {SLUG: []})
    offered(installed, "r-old-hymn", published_genres=["Christian"])
    offered(installed, "r-old-dance", published_genres=["Dance"])
    offered(installed, "r-old-unjudged")

    question = next_question()

    assert sorted(one["identity"] for one in question["releases"]) == [
        "r-old-dance",
        "r-old-unjudged",
    ]
    assert question["withheld"] == 1
    assert question["unjudged"] == 1
    code, held = drive(["label", "held"])
    assert [one["release_id"] for one in held["data"]["summary"]["releases"]] == ["r-old-hymn"]
    assert tombstones(installed) == 0


# ═══════════════════════════════════════════════════════════════════════════
# 3. The first run's catch up
# ═══════════════════════════════════════════════════════════════════════════


def test_open_review_items_are_offered_once_and_settled_by_the_answer(installed, monkeypatch):
    register()
    three_new(monkeypatch)
    kept = offered(installed, "r-old-1")
    dropped = offered(installed, "r-old-2")
    assert len(open_items(installed)) == 2

    question = next_question()

    assert sorted(one["identity"] for one in question["releases"]) == [
        "r-old-1", "r-old-2", "r1", "r2", "r3"
    ]
    waiting = {one["identity"]: one["item_id"] for one in question["releases"]}
    assert waiting["r-old-1"] == kept and waiting["r-old-2"] == dropped
    assert waiting["r3"] is None

    answered = answer(SLUG, "pick", "r-old-1", "r3")

    assert answered["taken"] == ["r3", "r-old-1"]
    filed = items(installed)
    assert filed["r-old-1"].verdict is review.Verdict.ACCEPTED
    assert filed["r-old-2"].verdict is review.Verdict.SUPERSEDED
    assert filed["r-old-2"].actor == sync_cli.ANSWERED_RULE
    assert filed["r3"].verdict is review.Verdict.ACCEPTED
    assert "r2" not in filed and "r1" not in filed
    assert open_items(installed) == []
    assert tombstones(installed) == 0
    assert not any(item.verdict is review.Verdict.REJECTED for item in filed.values())

    # AFTER THE FIRST RUN THE QUEUE HOLDS NO LABEL RELEASE FROM THIS PATH,
    # and the next run has nothing to ask.
    assert next_question() is None


def test_a_superseded_item_is_not_counted_as_waiting_by_label_approved(installed, monkeypatch):
    register()
    fake = bind(monkeypatch, {SLUG: []})
    fake.releases["r-old-1"] = (rows_for("r-old-1", 2), 2023)
    offered(installed, "r-old-1")
    offered(installed, "r-old-2")
    next_question()
    answer(SLUG, "pick", "r-old-1")

    code, envelope = drive(["label", "approved"])

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["accepted"], summary["rejected"], summary["open"]) == (1, 0, 0)
    (queue_line,) = [one for one in envelope["data"]["checks"] if one["key"] == "label.approved.queue"]
    assert "0 rejected and 0 not yet answered" in queue_line["detail"]


def test_an_item_filed_under_a_labels_old_identifier_is_offered_under_the_label(
    installed, monkeypatch
):
    register("Voll Schön")
    bind(monkeypatch, {"voll-schoen": []})
    held = labels.RegistryStore()
    moved = held.load()
    assert "voll-schoen" in moved.labels
    offered(installed, "r-moved", label_id="voll-schon")
    path = held.path
    document = json.loads(path.read_text())
    document["renamed"] = {"voll-schon": "voll-schoen"}
    path.write_text(json.dumps(document))

    question = next_question()

    assert question["label_id"] == "voll-schoen"
    assert [one["identity"] for one in question["releases"]] == ["r-moved"]


# ═══════════════════════════════════════════════════════════════════════════
# 4. The interactive path
# ═══════════════════════════════════════════════════════════════════════════


def five_labels(monkeypatch) -> Provider:
    names = ["Alpha Works", "Beta Works", "Gamma Works", "Delta Works", "Epsilon Works"]
    for name in names:
        register(name)
    return bind(
        monkeypatch,
        {
            labels.slug(name): [(f"{labels.slug(name)}-r{n}", str(2026 - n), 2) for n in range(2)]
            for name in names
        },
    )


def test_stopping_after_two_of_five_labels_resumes_at_the_third(installed, monkeypatch):
    fake = five_labels(monkeypatch)
    terminal = script(monkeypatch, "all", "not-now", "quit")

    code, envelope = sync()

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert [one["answer"] for one in summary["answered"]] == ["all", "not-now"]
    assert summary["stopped_at"] == "gamma-works"
    assert [one["state"] for one in summary["labels"]] == ["answered", "answered", "unanswered"]
    assert fake.asked_for == ["alpha-works", "beta-works", "gamma-works"]
    assert "Alpha Works: 2 new release(s), 4 track(s)" in terminal.shown
    assert "left unanswered" in checks(envelope, "label.gamma-works")[0]["detail"]
    held = record(installed)["labels"]
    assert held["alpha-works"]["answer"] == "all"
    assert held["beta-works"]["answer"] == "not-now"
    assert "answer" not in held["gamma-works"] and held["gamma-works"]["pending"]
    assert "delta-works" not in held and "epsilon-works" not in held
    assert sorted(items(installed)) == ["alpha-works-r0", "alpha-works-r1"]

    terminal = script(monkeypatch, "pick", "2", "stop", "all")
    lines = walked()

    answered = record(installed)["answers"][2:]
    assert [(one["label_id"], one["answer"]) for one in answered] == [
        ("gamma-works", "pick"),
        ("delta-works", "stop"),
        ("epsilon-works", "all"),
    ]
    assert "nothing new" in line_for(lines, "Alpha Works")
    assert "nothing new" in line_for(lines, "Beta Works")
    assert line_for(lines, "Gamma Works").startswith("Gamma Works: pick")
    held = record(installed)["labels"]
    assert held["alpha-works"]["answer"] == "all"
    assert held["beta-works"]["answer"] == "not-now"
    assert held["gamma-works"]["answer"] == "pick"
    assert answered[0]["taken"] == ["gamma-works-r1"]
    assert "delta-works" not in labels.RegistryStore().load().labels
    assert "every label is answered" in lines[-1]


def test_the_structured_path_asks_the_same_question_and_takes_the_same_answer(
    installed, monkeypatch
):
    """Two labels of one shape: one answered through ``--next`` and ``--answer``,
    the other at a terminal, and the two records agree line for line."""
    register("Alpha Works")
    register("Beta Works")
    bind(
        monkeypatch,
        {
            "alpha-works": [("a3", "2026", 4), ("a2", "2025", 2), ("a1", "2024", 1)],
            "beta-works": [("b3", "2026", 4), ("b2", "2025", 2), ("b1", "2024", 1)],
        },
    )
    shown = next_question()
    assert shown["label_id"] == "alpha-works"
    answer("alpha-works", "pick", "a2")
    terminal = script(monkeypatch, "pick", "2")

    lines = walked()

    assert "nothing new" in line_for(lines, "Alpha Works")
    assert line_for(lines, "Beta Works").startswith("Beta Works: pick")
    assert "Beta Works: 3 new release(s), 7 track(s), about 277 MB" in terminal.shown
    for number, one in enumerate(shown["releases"], start=1):
        twin = one["identity"].replace("a", "b")
        assert (
            f"{number:>3}. Label Act - Release {twin} ({one['year']}), "
            f"{one['tracks']} track(s)"
        ) in terminal.shown
    held = record(installed)["labels"]
    assert held["alpha-works"]["asked"] == ["a1", "a2", "a3"]
    assert held["beta-works"]["asked"] == ["b1", "b2", "b3"]
    assert held["alpha-works"]["answer"] == held["beta-works"]["answer"] == "pick"
    structured, interactive = record(installed)["answers"]
    assert structured["taken"] == ["a2"] and interactive["taken"] == ["b2"]
    assert structured["tracks"] == interactive["tracks"] == 2
    assert {rid: item.verdict for rid, item in items(installed).items()} == {
        "a2": review.Verdict.ACCEPTED,
        "b2": review.Verdict.ACCEPTED,
    }


def test_an_empty_line_never_moves_a_marker_and_a_prompt_nobody_answers_refuses(
    installed, monkeypatch
):
    register()
    three_new(monkeypatch)
    terminal = script(monkeypatch, "", "", "")

    code, envelope = sync()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unanswerable"
    assert envelope["cause"]["detail"] == {"label": SLUG, "answered": []}
    assert "--next" in " ".join(envelope["cause"]["remediation"]["steps"])
    held = record(installed)["labels"][SLUG]
    assert "asked" not in held and held["pending"]["new"] == 3
    assert items(installed) == {}
    assert terminal.shown.count("Answer (all, pick, not-now, stop, quit)") == 3


def test_a_word_outside_the_set_is_asked_again_and_the_answers_before_it_are_saved(
    installed, monkeypatch
):
    five_labels(monkeypatch)
    terminal = script(monkeypatch, "all", "download", "yes", "maybe")

    code, envelope = sync()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unanswerable"
    assert envelope["cause"]["detail"]["answered"] == ["alpha-works"]
    assert "'download' is not one of" in terminal.shown
    assert record(installed)["labels"]["alpha-works"]["answer"] == "all"
    assert "answer" not in record(installed)["labels"]["beta-works"]


def test_a_pick_outside_the_numbers_is_asked_again(installed, monkeypatch):
    register()
    three_new(monkeypatch)
    terminal = script(monkeypatch, "pick", "9", "1 3")

    walked()

    assert "9 is not a release number between 1 and 3" in terminal.shown
    assert record(installed)["answers"][0]["taken"] == ["r3", "r1"]


def test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again(installed, monkeypatch):
    """A superscript two is a digit to ``str.isdigit`` and not a number to ``int``."""
    register()
    three_new(monkeypatch)
    terminal = script(monkeypatch, "pick", "\u00b2", "2")

    walked()

    assert "\u00b2 is not a release number between 1 and 3" in terminal.shown
    assert record(installed)["answers"][0]["taken"] == ["r2"]


def test_the_prompt_goes_through_the_one_allowlisted_reader_and_the_verb_reads_no_stdin():
    tree = ast.parse((SRC_ROOT / "cratekit" / "label" / "sync_cli.py").read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"input", "raw_input"}
        if isinstance(node, ast.Attribute):
            assert node.attr != "stdin"
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [a.name for a in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
            )
            assert all(name.split(".")[0] != "getpass" for name in names)
    assert sync_cli.PROMPTER is prompt.Prompter


# ═══════════════════════════════════════════════════════════════════════════
# 5. The provider, and what a refusal leaves
# ═══════════════════════════════════════════════════════════════════════════


def test_a_provider_refusal_mid_run_parks_it_with_the_remaining_labels_unasked(
    installed, monkeypatch
):
    fake = five_labels(monkeypatch)
    fake.parked.add("gamma-works")
    script(monkeypatch, "all", "not-now", "all", "all", "all")

    code, envelope = sync()

    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "provider-cooldown"
    assert fake.asked_for == ["alpha-works", "beta-works", "gamma-works"]
    held = record(installed)["labels"]
    assert held["alpha-works"]["answer"] == "all"
    assert held["beta-works"]["answer"] == "not-now"
    assert set(held) == {"alpha-works", "beta-works"}
    assert sorted(items(installed)) == ["alpha-works-r0", "alpha-works-r1"]


def test_a_label_whose_catalogue_cannot_be_listed_fails_its_line_and_the_walk_goes_on(
    installed, monkeypatch
):
    five_labels(monkeypatch)
    fake = bind(monkeypatch, {"alpha-works": [("a-r0", "2026", 1)], "gamma-works": [("g-r0", "2026", 1)]})
    script(monkeypatch, "all", "all")

    lines = walked()

    assert line_for(lines, "Alpha Works").startswith("Alpha Works: all")
    assert line_for(lines, "Gamma Works").startswith("Gamma Works: all")
    for name in ("Beta Works", "Delta Works", "Epsilon Works"):
        assert "not asked; its catalogue could not be listed" in line_for(lines, name)
    assert set(record(installed)["labels"]) == {"alpha-works", "gamma-works"}
    assert fake.asked_for == ["alpha-works", "beta-works", "gamma-works", "delta-works", "epsilon-works"]


def test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new(
    installed, monkeypatch
):
    register()
    bind(monkeypatch, {SLUG: [("r3", "2026", 1), ("r2", "2025", 1)]}, confirmed=set())

    code, envelope = sync("--next")

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    (line,) = checks(envelope, f"label.{SLUG}")
    assert line["status"] == "fail"
    assert "could not confirm a single one" in line["detail"]
    assert record(installed)["labels"] == {}


def test_a_release_whose_tracks_cannot_be_read_is_counted_as_unread_not_as_empty(
    installed, monkeypatch
):
    register()
    fake = three_new(monkeypatch)
    del fake.releases["r2"]

    question = next_question()

    assert question["tracks"] == 5
    assert question["unknown"] == 1
    by_id = {one["identity"]: one for one in question["releases"]}
    assert by_id["r2"]["tracks"] is None and by_id["r2"]["size"] is None
    code, envelope = sync("--next")
    (line,) = checks(envelope, f"question.{SLUG}")
    assert "1 with tracks unread" in line["detail"]


def test_a_saved_question_is_printed_again_with_no_provider_call(installed, monkeypatch):
    register()
    fake = three_new(monkeypatch)
    first = next_question()

    again = next_question()

    assert again == first
    assert fake.asked_for == [SLUG]


# ═══════════════════════════════════════════════════════════════════════════
# 6. Refusals of the command line, each with nothing recorded
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "argv, said",
    [
        (["--answer", "all"], "needs the label"),
        (["--answer", "pick", "--label", SLUG], "needs the releases to take"),
        (["--label", SLUG], "go with --answer"),
        (["--release", "r1"], "go with --answer"),
        (["--next", "--answer", "all", "--label", SLUG], "one invocation does one"),
        (["--answer", "all", "--label", SLUG, "--release", "r1"], "goes with --answer pick"),
    ],
)
def test_a_half_shaped_invocation_is_refused_and_records_nothing(installed, monkeypatch, argv, said):
    register()
    three_new(monkeypatch)
    if "--release" in argv and "pick" not in argv:
        next_question()

    code, envelope = sync(*argv)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "review-selection-invalid"
    assert said in envelope["cause"]["message"]
    assert record(installed)["answers"] == []
    assert items(installed) == {}


def test_an_answer_with_no_question_waiting_is_refused(installed, monkeypatch):
    register()
    three_new(monkeypatch)

    code, envelope = sync("--answer", "all", "--label", SLUG)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "review-selection-invalid"
    assert "no question is waiting" in envelope["cause"]["message"]
    assert record(installed)["labels"] == {}


def test_stop_with_no_question_waiting_names_the_registry_remove(installed, monkeypatch):
    """A label with nothing new is never asked, so ``--next`` is no remedy for stop."""
    register()
    bind(monkeypatch, {SLUG: []})

    code, envelope = sync("--answer", "stop", "--label", SLUG)

    assert code == int(ExitCode.PRECONDITION), envelope
    steps = json.dumps(envelope["cause"])
    assert f"crate label registry remove {SLUG}" in steps
    assert "crate label sync --next" not in steps
    assert SLUG in labels.RegistryStore().load().labels


def test_a_later_answer_files_its_releases_under_the_run_that_asked(installed, monkeypatch):
    register()
    three_new(monkeypatch)
    code, asked = sync("--next")
    assert code == int(ExitCode.OK), asked

    answer(SLUG, "all")

    filed = items(installed)
    assert {filed[rid].payload[sweep.SWEEP_RUN] for rid in ("r1", "r2", "r3")} == {
        asked["run_id"]
    }


def test_a_walk_left_unanswered_after_its_question_was_saved_is_not_a_no_op(
    installed, monkeypatch
):
    register()
    three_new(monkeypatch)
    script(monkeypatch, "quit")

    code, envelope = sync()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert record(installed)["labels"][SLUG]["pending"]


def test_a_pick_naming_a_release_the_question_did_not_offer_is_refused(installed, monkeypatch):
    register()
    three_new(monkeypatch)
    next_question()

    code, envelope = sync("--answer", "pick", "--label", SLUG, "--release", "r3", "--release", "r9")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "review-selection-invalid"
    assert envelope["cause"]["detail"]["unknown"] == ["r9"]
    assert items(installed) == {}
    assert "pending" in record(installed)["labels"][SLUG]


def test_an_answer_for_a_label_nobody_follows_is_refused(installed, monkeypatch):
    register()
    three_new(monkeypatch)

    code, envelope = sync("--answer", "all", "--label", "Nobody Works")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-unknown"


def test_an_empty_registry_is_refused_before_any_provider_is_resolved(installed, monkeypatch):
    fake = bind(monkeypatch, {})

    code, envelope = sync("--next")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-registry-empty"
    assert fake.asked_for == []


def test_a_record_that_cannot_be_read_refuses_rather_than_asking_everything_again(
    installed, monkeypatch
):
    register()
    fake = three_new(monkeypatch)
    path = config.state_path("label_sync", installed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json")

    code, envelope = sync("--next")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unusable"
    assert fake.asked_for == []


def test_a_record_of_another_version_refuses_rather_than_being_read_as_this_builds(
    installed, monkeypatch
):
    """Measured at zero by R-857's table, row S02: no test wrote another version."""
    register()
    fake = three_new(monkeypatch)
    path = config.state_path("label_sync", installed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 2, "labels": {}, "answers": []}))

    code, envelope = sync("--next")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-sync-unusable"
    assert "version 2" in envelope["cause"]["message"]
    assert fake.asked_for == []


def test_an_item_decided_between_the_question_and_the_answer_is_left_as_decided(
    installed, monkeypatch
):
    """Measured at zero by R-857's table, row S14: nothing decided an item mid question."""
    register()
    bind(monkeypatch, {SLUG: []})
    decided = offered(installed, "r-old-1")
    offered(installed, "r-old-2")
    next_question()
    with review.open_store(installed) as store:
        review.resolve(store, decided, review.Verdict.REJECTED, actor="a person")

    answered = answer(SLUG, "all")

    assert answered["taken"] == ["r-old-2"]
    assert answered["left"] == ["r-old-1"]
    filed = items(installed)
    assert filed["r-old-1"].verdict is review.Verdict.REJECTED
    assert filed["r-old-2"].verdict is review.Verdict.ACCEPTED


def test_a_provider_refusal_while_counting_a_catch_up_release_parks_the_run(
    installed, monkeypatch
):
    """Measured at zero by R-857's table, row S25: a refusal counted as tracks unread."""
    register()
    fake = bind(monkeypatch, {SLUG: []})
    offered(installed, "r-old-1")

    def refused(release_id):
        raise Parked(
            Cause(
                reason="provider-cooldown",
                message="the streaming provider rate limited this account",
                remediation=Remediation(remedy=Remedy.RETRY_LATER),
                origin=("provider_gate",),
            )
        )

    monkeypatch.setattr(fake, "release_tracks", refused)

    code, envelope = sync("--next")

    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "provider-cooldown"
    assert record(installed)["labels"] == {}


# ═══════════════════════════════════════════════════════════════════════════
# 7. What the verb and its record declare
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_declares_what_it_is():
    entry = registry.entry("label.sync")
    assert entry.interactive
    assert entry.output_schema == "diagnostic/1"
    assert entry.adjudicates
    # U108's go writes the list and lands the downloads, behind its one gate.
    assert entry.destructive
    assert entry.writes == frozenset({"files"})
    assert [(gate.name, gate.explicit, gate.digest_source) for gate in entry.gates] == [
        ("label.sync.confirm", True, "plan")
    ]
    assert not entry.long_running
    assert entry.module_id == "labels"
    assert entry.doctor_checks == ("library.mounted", "credential.provider")


def test_the_record_is_library_state_coupled_with_the_review_queue(installed, monkeypatch):
    held = config.state_file("label_sync")
    assert held.root is config.StateRoot.LIBRARY
    assert held.snapshot is config.SnapshotRole.COUPLED
    assert held.rollback_effects == (config.RollbackEffect.NONE,)
    assert config.state_file("label_sync_lock").snapshot is config.SnapshotRole.NEVER_RESTORED
    register()
    three_new(monkeypatch)
    next_question()
    answer(SLUG, "all")
    path = config.state_path("label_sync", installed)
    assert path.is_file()
    assert config.library_coupled_dir(installed) in path.parents
    assert installed.library.root in path.parents


def test_the_default_human_output_names_the_question_and_each_release(installed, monkeypatch):
    register()
    three_new(monkeypatch)

    code, text = drive_human(["label", "sync", "--next"])

    assert code == int(ExitCode.OK)
    assert "Tide Works: 3 new release(s), 7 track(s), about 277 MB" in text
    assert "Release r3 (2026), 4 track(s)" in text
    assert "crate label sync --answer all --label tide-works" in text


# ═══════════════════════════════════════════════════════════════════════════
# R-515: a release the provider lists short of its declared count
# ═══════════════════════════════════════════════════════════════════════════


def test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall(
    installed, monkeypatch
):
    register()
    fake = three_new(monkeypatch)
    rows, year = fake.releases["r3"]
    fake.releases["r3"] = (rows, year, 6)

    question = next_question()

    (short,) = [one for one in question["releases"] if one["identity"] == "r3"]
    assert short["tracks"] == 4
    assert short["shortfall"] == {"declared": 6, "listed": 4, "withheld": 2}
    assert all(one["shortfall"] is None for one in question["releases"] if one is not short)
    assert question["provider_withheld"] == 2
    code, envelope = sync("--next")
    assert code == int(ExitCode.OK), envelope
    (asked,) = checks(envelope, "question")
    assert "2 track(s) withheld by the provider on 1 release(s)" in asked["detail"]
    (line,) = checks(envelope, "release.r3")
    assert "4 track(s) (6 declared, 4 listed, 2 withheld by the provider)" in line["detail"]


def test_full_releases_say_nothing_of_a_shortfall(installed, monkeypatch):
    register()
    three_new(monkeypatch)
    question = next_question()
    assert question["provider_withheld"] == 0
    assert all(one["shortfall"] is None for one in question["releases"])
