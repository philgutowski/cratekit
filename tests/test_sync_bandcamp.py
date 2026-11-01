"""U179: ``crate sync bandcamp`` takes new Bandcamp purchases to their landing gate in one verb.

WHAT THIS FILE GUARDS. Sitting 46 took 96 tracks from one seller to filed in
about two hours and 25 messages, each step typed by hand. The properties here
make the one verb real: it plans before it fetches, so an expired session ends
before anything downloads; it fetches into one batch folder, continuing an
open fetch there rather than queueing a second; it runs the shared tail in its
order and never plans a landing over files the tail has not run on; it names
the batch from the files' label tags and passes ``--label-from-tags`` only
when one carries a label; it rehearses the landing with the very arguments the
landing then takes; and it ends at the landing's own gate naming what the
session does next, with a closing report of what was held as owned, refused,
staged, left without a genre and which sellers no label names.

WHAT IS REAL AND WHAT STANDS IN. The plan and the fetch run through the real
dispatcher over U176's fake account, as ``tests/test_bandcamp_cli.py`` runs
them: everything but the transport is real. The tail, the rehearsal and the
landing stand in through the chain's one seam, ``cratekit.cli.tail.dispatch``,
with ``sync land``'s own stand in, which queues and drives a real job for
each tail step. ``tests/test_sync_bandcamp_native.py`` lets the rehearsal and
the landing run for real on the native fixture database.

D1 applies. No real person, seller or release is named; ``pulsromania`` and
``otherlabel`` are the fake account's sellers.
"""

from __future__ import annotations

import shlex
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from cratekit.acquire import bandcamp_cli
from cratekit.cli import registry, sync_bandcamp
from cratekit.cli import tail as tail_chain
from cratekit.core import config, jobs, rb_writer, tags
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import batch_name
from tests.bandcamp_fakes import FakeAccount, item
from tests.cli_drive import drive
from tests.test_bandcamp_cli import (
    SESSION,
    bind,
    collection,
    owned,
)
from tests.test_bandcamp_cli import (
    account as account,  # noqa: PLC0414
)
from tests.test_bandcamp_cli import (
    cfg as cfg,  # noqa: PLC0414
)
from tests.test_bandcamp_cli import (
    library as library,  # noqa: PLC0414
)
from tests.test_bandcamp_cli import (
    signed_in as signed_in,  # noqa: PLC0414
)
from tests.test_bandcamp_cli import (
    silence as silence,  # noqa: PLC0414
)
from tests.test_bandcamp_labels import PULS_FILES
from tests.test_bandcamp_labels import puls as puls  # noqa: PLC0414
from tests.test_sync_land import Tail, _gate, _ok, _refused

ENTRY = registry.entry("sync.bandcamp")
BATCH = "Batch One"
TODAY = date(2026, 11, 1)
OTHER_FILE = "Coral Arc - Drift - 01 Drift.flac"


# ═══════════════════════════════════════════════════════════════════════════
# The stand ins
# ═══════════════════════════════════════════════════════════════════════════


class Landing:
    """The rehearsal and the landing, standing in: each records its arguments."""

    def __init__(self) -> None:
        self.rehearsed: list[list[str]] = []
        self.landed: list[list[str]] = []
        self.rehearsal: tuple[int, dict[str, Any]] = _ok(
            {"digest": "rehearsed-digest", "items": [], "totals": {"count": 1}}
        )
        self.live: tuple[int, dict[str, Any]] = _refused(_gate("land-run"), outcome="blocked")

    def __call__(self, argv: list[str]) -> tuple[int, dict[str, Any]]:
        if tail_chain.REHEARSE_FLAG in argv:
            self.rehearsed.append(list(argv))
            return self.rehearsal
        self.landed.append(list(argv))
        return self.live


@pytest.fixture
def chain(monkeypatch) -> Tail:
    """The tail standing in, the landing answered by a :class:`Landing`."""
    stand_in = Tail()
    stand_in.landing = Landing()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    monkeypatch.setattr(batch_name, "today", lambda: TODAY)
    return stand_in


def _tag_with(genre: str):
    """A tag step that writes ``genre`` into each file, as the label's genre would."""

    def work(job: jobs.Job, item_: jobs.Item) -> None:
        assert tags.write_tags(Path(job.payload["folder"]) / item_.item_id, {"genre": genre})

    return work


def run(*args: str) -> tuple[int, dict]:
    return drive(["sync", "bandcamp", *args])


def _summary(envelope: dict) -> dict:
    cause = envelope.get("cause") or {}
    if "sync_bandcamp" in (cause.get("detail") or {}):
        return cause["detail"]["sync_bandcamp"]["summary"]
    return envelope["data"]["summary"]


def _checks(envelope: dict) -> dict[str, dict]:
    cause = envelope.get("cause") or {}
    data = (cause.get("detail") or {}).get("sync_bandcamp") or envelope["data"]
    return {c["key"]: c for c in data["checks"]}


def _fetch_jobs() -> list[jobs.Job]:
    key = registry.entry(sync_bandcamp.FETCH_VERB).handler_key
    with jobs.open_store() as store:
        return [job for job in jobs.list_jobs(store) if job.handler_key == key]


def _folder(cfg_: config.Config, batch: str = BATCH) -> Path:
    return (Path(cfg_.paths.download_staging).expanduser() / batch).absolute()


def _staged(cfg_: config.Config, batch: str = BATCH) -> list[str]:
    folder = _folder(cfg_, batch)
    return sorted(p.name for p in folder.iterdir() if p.is_file()) if folder.is_dir() else []


def _verbs(stand_in: Tail) -> list[tuple[str, ...]]:
    return [tuple(argv[:2]) if argv[:1] != ["-d"] else ("name", "apply") for argv in stand_in.calls]


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declaration
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_queues_nothing_of_its_own_and_declares_no_gate():
    assert not ENTRY.long_running
    assert ENTRY.argv_builder is None
    assert not ENTRY.gates
    assert ENTRY.writes == frozenset({"files"})


def test_the_steps_are_the_plan_the_fetch_the_shared_tail_the_rehearsal_and_the_landing():
    assert sync_bandcamp.STEPS == (
        "preflight", "plan", "fetch", "tag", "analyze", "restamp", "name", "rehearse", "land",
    )


# ═══════════════════════════════════════════════════════════════════════════
# 2. One label's purchases to the gate
# ═══════════════════════════════════════════════════════════════════════════


def test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label(
    signed_in, account, puls, chain, library
):
    chain.work[tail_chain.TAG] = _tag_with("Rominimal")

    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == "pending"
    folder = _folder(signed_in)
    # THE ORDER: the plan, the fetch, the tail, the rehearsal, then the landing.
    assert _verbs(chain) == [
        ("acquire", "bandcamp"),
        ("acquire", "bandcamp-fetch"),
        ("tag", "folder"), ("tag", "folder"),
        ("analyze", "run"), ("analyze", "run"),
        ("analyze", "restamp"), ("analyze", "restamp"),
        ("name", "apply"),
        ("intake", "land"),
        ("intake", "land"),
    ]
    name = "2026-11-01 Bandcamp PULS"
    (landed,) = chain.landing.landed
    assert landed == ["intake", "land", str(folder), "--name", name, "--label-from-tags"]
    # THE REHEARSAL IS THE LANDING'S OWN ARGUMENTS, so the gate names it.
    assert chain.landing.rehearsed == [[*landed, "--rehearse"]]
    summary = _summary(envelope)
    assert summary["landing_name"] == name
    assert summary["staged"] == sorted(PULS_FILES)
    assert summary["rehearsal"] == "rehearsed-digest"
    assert summary["gate_run"] == "land-run"
    assert summary["labels"] == {"pulsromania": "PULS"}
    assert summary["sellers_unregistered"] == []
    assert summary["no_genre"] == [] and summary["no_label"] == []
    # WHAT WAS HELD AS OWNED, with the library file each owned track is.
    (owned_release,) = summary["owned"]
    assert owned_release["release"] == "Nova Reef - Low Light (pulsromania)"
    assert owned_release["tracks"][0]["paths"] == [
        str(library / "Music" / "Owned" / "Nova Reef - Low Light.flac")
    ]
    (held,) = summary["held"]
    assert held["release"] == "Various Artists - Compiled (pulsromania)"
    assert [one["track"] for one in held["tracks"]] == ["Nova Reef - Shore"]
    assert sorted(summary["fetched"]) == [
        "Aurora Bloom - Sun Path (pulsromania)",
        "Various Artists - Compiled (pulsromania)",
    ]
    steps = envelope["pending_human_action"]["steps"]
    assert steps[0] == (
        "read the plan, then answer the gate as the session: crate run decide "
        "land-run intake.land.native apply --actor session"
    )
    assert any("Analyze Tracks" in step for step in steps)


def test_the_tail_runs_on_the_absolute_batch_folder(signed_in, account, puls, chain):
    run("--seller", "PULS", "--batch", BATCH)

    folder = str(_folder(signed_in))
    queued = [argv for argv in chain.calls if argv[:1] in (["tag"], ["analyze"]) and "--job" not in argv]
    assert [argv[-1] for argv in queued] == [folder] * 3
    (named,) = chain.named
    assert named[-1] == folder


# ═══════════════════════════════════════════════════════════════════════════
# 3. What ends before a download, and what has nothing to do
# ═══════════════════════════════════════════════════════════════════════════


def test_an_expired_session_stops_at_the_plan_with_the_login_step_before_any_download(
    signed_in, tmp_path, silence, monkeypatch, chain
):
    account_ = bind(monkeypatch, collection(tmp_path, silence, expired=True))

    code, envelope = run("--batch", BATCH)

    assert code == int(ExitCode.UPSTREAM_AUTH), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "auth-failed"
    assert any(f"crate login {SESSION} --from-file" in step for step in cause["remediation"]["steps"])
    assert _verbs(chain) == [("acquire", "bandcamp")]
    assert _fetch_jobs() == []
    assert account_.downloaded == []
    assert _summary(envelope)["stopped_at"] == "plan"
    # NOTHING WAS FETCHED, so the refusal names no batch folder to continue.
    assert not any("kept in its batch folder" in step for step in cause["remediation"]["steps"])


def test_nothing_new_ends_with_no_fetch_no_tail_and_no_landing(
    signed_in, tmp_path, silence, library, monkeypatch, chain
):
    owned(library, "Nova Reef - Low Light.flac")
    bind(
        monkeypatch,
        FakeAccount(
            [
                item("2", seller="pulsromania", artist="Nova Reef", title="Low Light",
                     purchased="20 Oct 2026 10:00:00 GMT", tracks=[("", "Low Light")]),
            ]
        ),
    )

    code, envelope = run("--batch", BATCH)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _verbs(chain) == [("acquire", "bandcamp")]
    assert _fetch_jobs() == []
    assert chain.landing.landed == [] and chain.landing.rehearsed == []
    checks = _checks(envelope)
    assert "nothing new to fetch" in checks["sync.bandcamp.plan"]["detail"]
    assert "nothing is staged" in checks["sync.bandcamp.fetch"]["detail"]
    assert len(_summary(envelope)["owned"]) == 1


def test_a_second_run_after_a_landing_finds_nothing_new_and_lands_nothing(
    signed_in, account, puls, chain
):
    run("--seller", "PULS", "--batch", BATCH)
    # The landing moved the files out of staging, as an applied landing does.
    for path in _folder(signed_in).iterdir():
        path.unlink()
    chain.calls.clear()

    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _verbs(chain) == [("acquire", "bandcamp")]
    assert len(_fetch_jobs()) == 1
    assert len(chain.landing.landed) == 1


def test_rekordbox_running_refuses_before_the_plan(signed_in, account, monkeypatch, chain):
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)

    code, envelope = run("--batch", BATCH)

    assert code == int(ExitCode.REKORDBOX_OPEN), envelope
    assert "crate sync bandcamp" in envelope["cause"]["message"]
    assert chain.calls == []


# ═══════════════════════════════════════════════════════════════════════════
# 4. Sellers, labels and the batch's name
# ═══════════════════════════════════════════════════════════════════════════


def test_a_seller_no_label_names_lands_unlabelled_and_is_named(signed_in, account, puls, chain):
    code, envelope = run("--seller", "otherlabel", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    (landed,) = chain.landing.landed
    # NO LABEL TAG, NO LABEL FLAG, and the batch is not named for any label.
    assert landed == ["intake", "land", str(_folder(signed_in)), "--name", "2026-11-01 Bandcamp"]
    summary = _summary(envelope)
    assert summary["sellers_unregistered"] == ["otherlabel"]
    assert summary["no_label"] == [OTHER_FILE]
    assert [w for w in envelope["warnings"] if w["code"] == bandcamp_cli.SELLER_UNREGISTERED]


def test_a_batch_of_a_label_and_an_unregistered_seller_files_by_tag_under_a_plain_name(
    signed_in, account, puls, chain
):
    code, envelope = run("--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    (landed,) = chain.landing.landed
    assert landed[-3:] == ["--name", "2026-11-01 Bandcamp", "--label-from-tags"]
    assert sorted(_summary(envelope)["staged"]) == sorted([*PULS_FILES, OTHER_FILE])


def test_files_left_without_a_genre_are_named_in_the_report(signed_in, account, puls, chain):
    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert _summary(envelope)["no_genre"] == sorted(PULS_FILES)
    (warned,) = [w for w in envelope["warnings"] if w["code"] == sync_bandcamp.NO_GENRE]
    assert all(name in warned["message"] for name in PULS_FILES)
    assert _checks(envelope)["sync.bandcamp.tags"]["status"] == "warn"


def test_a_file_whose_tags_cannot_be_read_is_unread_not_ungenred_and_names_no_label(
    signed_in, account, puls, chain
):
    folder = _folder(signed_in)
    folder.mkdir(parents=True)
    (folder / "Broken.flac").write_bytes(b"not a flac container")
    chain.work[tail_chain.TAG] = _tag_with("Rominimal")
    # The tag stand in writes each file; the broken one it cannot, so it is
    # passed over the way the real step would record it.
    real_work = chain.work[tail_chain.TAG]
    chain.work[tail_chain.TAG] = lambda job, it: None if it.item_id == "Broken.flac" else real_work(job, it)

    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    summary = _summary(envelope)
    assert summary["tags_unread"] == ["Broken.flac"]
    assert "Broken.flac" not in summary["no_genre"]
    # A FILE NOBODY COULD READ IS NOT TAKEN AS THE LABEL'S, so the name is plain.
    assert summary["landing_name"] == "2026-11-01 Bandcamp"
    assert [w for w in envelope["warnings"] if w["code"] == sync_bandcamp.TAGS_UNREAD]


@pytest.mark.parametrize(
    ("labels", "words"),
    [
        (("PULS", "PULS"), "Bandcamp PULS"),
        (("PULS", "puls"), "Bandcamp PULS"),
        (("PULS", "Kompakt"), "Bandcamp"),
        (("PULS", None), "Bandcamp"),
        ((None,), "Bandcamp"),
        (("A/B",), "Bandcamp A-B"),
        (("  ",), "Bandcamp"),
    ],
)
def test_the_batch_name_is_the_one_label_every_file_names_or_plain(cfg, monkeypatch, labels, words):
    monkeypatch.setattr(batch_name, "today", lambda: TODAY)
    assert batch_name.bandcamp(cfg, labels) == f"2026-11-01 {words}"


def test_a_taken_batch_name_takes_the_next_number(cfg, monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: TODAY)
    (Path(cfg.library.root) / cfg.library.music_dir / "2026-11-01 Bandcamp PULS").mkdir(parents=True)
    assert batch_name.bandcamp(cfg, ("PULS",)) == "2026-11-01 Bandcamp PULS 2"


# ═══════════════════════════════════════════════════════════════════════════
# 5. The landing is never planned over files the tail did not run on
# ═══════════════════════════════════════════════════════════════════════════


def _analysis_fails(job: jobs.Job, item_: jobs.Item) -> None:
    raise CratekitError(
        Cause(
            reason="module-extras-missing",
            message="the analysis extra is not installed",
            remediation=Remediation(remedy=Remedy.INSTALL_MODULE_EXTRA),
            origin=("test",),
        )
    )


def test_a_failed_tail_step_plans_no_landing_and_names_the_continuation(
    signed_in, account, puls, chain
):
    chain.work[tail_chain.ANALYZE] = _analysis_fails

    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    assert code != int(ExitCode.OK), envelope
    assert chain.landing.landed == [] and chain.landing.rehearsed == []
    assert ("name", "apply") not in _verbs(chain)
    assert _summary(envelope)["stopped_at"] == "analyze"
    # THE FETCH IS KEPT, and the way on is the verb again over the same batch.
    assert _staged(signed_in) == sorted(PULS_FILES)
    steps = envelope["cause"]["remediation"]["steps"]
    assert any(
        "crate sync bandcamp --batch 'Batch One' --seller PULS" in step for step in steps
    ), steps


def test_the_same_batch_again_takes_the_staged_files_on_and_fetches_nothing_twice(
    signed_in, account, puls, chain
):
    chain.work[tail_chain.ANALYZE] = _analysis_fails
    run("--seller", "PULS", "--batch", BATCH)
    del chain.work[tail_chain.ANALYZE]
    chain.calls.clear()

    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert len(_fetch_jobs()) == 1, "the purchases the first run staged are not fetched again"
    assert ("acquire", "bandcamp-fetch") not in _verbs(chain)
    assert "already staged" in _checks(envelope)["sync.bandcamp.fetch"]["detail"]
    (landed,) = chain.landing.landed
    assert landed[-3:] == ["--name", "2026-11-01 Bandcamp PULS", "--label-from-tags"]


def test_a_failed_rehearsal_plans_no_live_landing(signed_in, account, puls, chain):
    stale = Cause(
        reason="decision-stale",
        message="the rehearsal's plan differs from the live plan",
        remediation=Remediation(remedy=Remedy.REPLAN_THEN_DECIDE),
        origin=("test",),
    )
    chain.landing.rehearsal = _refused(stale)

    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    # A GATE CODE FROM A STEP IS THE STEP'S OWN, never this verb's refusal,
    # since raised as the verb's own it would mark the run resumable over a
    # question it does not declare (``tail.required``). It ends for a person.
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    (rehearsed,) = chain.landing.rehearsed
    assert chain.landing.landed == []
    assert _summary(envelope)["stopped_at"] == "decision-stale"
    steps = envelope["pending_human_action"]["steps"]
    assert f"then run the step again: crate {shlex.join(rehearsed)}" in steps
    assert f"then plan the landing: crate {shlex.join(rehearsed[:-1])}" in steps


def test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing(
    signed_in, account, puls, chain
):
    missing = Cause(
        reason=tail_chain.ACK_STOP,
        message="no backup acknowledgment is recorded",
        remediation=Remediation(remedy=Remedy.ACKNOWLEDGE_BACKUP),
        origin=("test",),
    )
    chain.landing.rehearsal = _refused(missing, outcome="blocked")

    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["pending_human_action"]["kind"] == "backup_ack"
    assert chain.landing.landed == []
    (rehearsed,) = chain.landing.rehearsed
    steps = envelope["pending_human_action"]["steps"]
    assert f"then rehearse the landing again: crate {shlex.join(rehearsed)}" in steps
    assert f"then plan the landing: crate {shlex.join(rehearsed[:-1])}" in steps
    assert any("Analyze Tracks" in step for step in steps)


# ═══════════════════════════════════════════════════════════════════════════
# 6. The fetch: refused releases, a parked fetch, an open one elsewhere
# ═══════════════════════════════════════════════════════════════════════════


def test_a_release_refused_for_good_is_recorded_and_nothing_is_landed_over_none(
    signed_in, tmp_path, silence, monkeypatch, chain
):
    bind(monkeypatch, collection(tmp_path, silence, encodings=("mp3-320",)))

    code, envelope = run("--seller", "otherlabel", "--batch", BATCH)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    summary = _summary(envelope)
    (refused,) = summary["fetch_refused"]
    assert refused["reason"] == "lossy-refused"
    assert refused["release"] == "Coral Arc - Drift (otherlabel)"
    statuses = [c["status"] for c in envelope["data"]["checks"] if c["key"] == "sync.bandcamp.fetch"]
    assert statuses == ["fail", "info"], "the fetch that staged nothing reads fail, then the end"
    assert [w for w in envelope["warnings"] if w["code"] == sync_bandcamp.FETCH_REFUSED]
    assert chain.landing.landed == []
    assert not any(argv[:1] == ["tag"] for argv in chain.calls)


def test_a_fetch_parked_by_the_session_ends_blocked_and_the_next_run_drives_it_on(
    signed_in, account, puls, chain
):
    original = account.get
    state = {"expired": True}

    def expiring(url, *, cookie):
        if "/download" in url and state["expired"]:
            return type(original(url, cookie=cookie))(403, "forbidden")
        return original(url, cookie=cookie)

    account.get = expiring
    code, envelope = run("--seller", "otherlabel", "--batch", BATCH)
    assert code != int(ExitCode.OK), envelope
    assert envelope["outcome"] == "blocked"
    (job,) = _fetch_jobs()
    assert str(job.state) == "blocked"
    assert chain.landing.landed == []

    state["expired"] = False
    bandcamp_cli.forget()
    chain.calls.clear()
    code, envelope = run("--seller", "otherlabel", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert [one.job_id for one in _fetch_jobs()] == [job.job_id], "driven on, not queued twice"
    assert chain.calls[0] == ["acquire", "bandcamp-fetch", "--job", job.job_id]
    assert _staged(signed_in) == [OTHER_FILE]


def test_two_fetches_left_open_in_the_batch_are_both_driven_on_oldest_first(
    signed_in, account, puls, chain
):
    """Two hand run fetches into one batch, both parked: a run drives every one."""
    original = account.get
    state = {"expired": True}

    def expiring(url, *, cookie):
        if "/download" in url and state["expired"]:
            return type(original(url, cookie=cookie))(403, "forbidden")
        return original(url, cookie=cookie)

    account.get = expiring
    drive(["acquire", "bandcamp-fetch", "--seller", "otherlabel", "--batch", BATCH])
    bandcamp_cli.forget()
    drive(["acquire", "bandcamp-fetch", "--seller", "otherlabel", "--batch", BATCH])
    newest, oldest = _fetch_jobs()
    assert str(oldest.state) == str(newest.state) == "blocked"
    state["expired"] = False
    bandcamp_cli.forget()

    code, envelope = run("--seller", "otherlabel", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert chain.calls[:2] == [
        ["acquire", "bandcamp-fetch", "--job", oldest.job_id],
        ["acquire", "bandcamp-fetch", "--job", newest.job_id],
    ]
    assert not any(job.is_open() for job in _fetch_jobs()), "no fetch is left open behind the gate"
    summary = _summary(envelope)
    assert summary["fetch_jobs"] == [oldest.job_id, newest.job_id]
    assert _staged(signed_in) == [OTHER_FILE]
    # THE ONE RELEASE BOTH HELD IS COUNTED ONCE: the newer found it recorded.
    assert summary["fetched"] == ["Coral Arc - Drift (otherlabel)"]
    fetch_checks = [
        c["detail"] for c in envelope["data"]["checks"] if c["key"] == "sync.bandcamp.fetch"
    ]
    assert f"fetch job {newest.job_id} staged 0 release(s), 1 already staged by this run" in fetch_checks


def test_a_release_refused_by_two_fetches_is_named_once(
    signed_in, account, puls, chain, tmp_path, silence, monkeypatch
):
    """An open fetch driven on refuses a lossy only release, and the new fetch refuses it again."""
    with jobs.open_store() as store:
        jobs.enqueue(
            store,
            handler_key=registry.entry(sync_bandcamp.FETCH_VERB).handler_key,
            payload={
                bandcamp_cli.BATCH: BATCH,
                bandcamp_cli.RELEASES: {
                    "4": {"seller": "otherlabel", "label": None, "label_id": None,
                          "artist": "Coral Arc", "title": "Drift", "item_type": "album",
                          "tracks": [{"number": 1, "artist": "", "title": "Drift"}], "held": []},
                },
            },
            cfg=config.load(),
            item_ids=("4",),
        )
    bind(monkeypatch, collection(tmp_path, silence, encodings=("mp3-320",)))

    code, envelope = run("--seller", "otherlabel", "--batch", BATCH)

    assert code == int(ExitCode.OK), envelope
    summary = _summary(envelope)
    assert len(summary["fetch_jobs"]) == 2
    assert [row["item_id"] for row in summary["fetch_refused"]] == ["4"]
    (warned,) = [w for w in envelope["warnings"] if w["code"] == sync_bandcamp.FETCH_REFUSED]
    assert warned["message"].startswith("1 release(s) were refused")


def test_the_tags_are_read_from_the_files_the_name_step_renamed(
    signed_in, account, puls, chain, monkeypatch
):
    """``name apply`` renames every staged file; the label is read off the renamed ones."""

    def renaming(argv):
        if argv[:1] == ["-d"]:
            folder = Path(argv[-1])
            for path in sorted(folder.iterdir()):
                path.rename(folder / f"01A - 124 - {path.name}")
        return chain(argv)

    monkeypatch.setattr(tail_chain, "dispatch", renaming)

    code, envelope = run("--seller", "PULS", "--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    summary = _summary(envelope)
    assert summary["staged"] == sorted(f"01A - 124 - {name}" for name in PULS_FILES)
    assert summary["tags_unread"] == []
    (landed,) = chain.landing.landed
    assert landed[-3:] == ["--name", "2026-11-01 Bandcamp PULS", "--label-from-tags"]


def test_an_open_fetch_into_another_batch_is_named_and_nothing_is_fetched(
    signed_in, account, chain
):
    with jobs.open_store() as store:
        held = jobs.enqueue(
            store,
            handler_key=registry.entry(sync_bandcamp.FETCH_VERB).handler_key,
            payload={bandcamp_cli.BATCH: "Bandcamp 2026-10-31", bandcamp_cli.RELEASES: {}},
            cfg=config.load(),
            item_ids=("9",),
        )

    code, envelope = run("--batch", BATCH)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert chain.calls == []
    (step,) = envelope["pending_human_action"]["steps"]
    assert step == "continue that batch first: crate sync bandcamp --batch 'Bandcamp 2026-10-31'"
    assert _summary(envelope)["open_fetch"] == {
        "job_id": held.job_id,
        "batch": "Bandcamp 2026-10-31",
    }
