"""U27: the ``adopt apply`` command line, and the one session it opens.

WHY THIS FILE EXISTS SEPARATELY FROM THE CONFORMANCE SUITE. Eight of the nine
conformance properties drive this verb the moment its entry loses ``planned_in``,
and every one of them drives the QUEUEING path: build the plan, ask the approval
gate, enqueue, report. None of them reaches the session, because the plan the
conformance fixture can build is empty and a session opened to apply nothing is a
session this verb deliberately does not open. So the thing the unit exists for
would ship undriven if this file did not exist.

WHAT THE UNIT EXISTS FOR. The residual titled "Adoption's tag write takes no
destructive session and no library lock" says ``apply_plan`` rewrites a user's
file with nothing asserting that the volume identity still matches, that a backup
was acknowledged, or that no other run is writing, and with nothing stopping two
runs reaching one file twice. Its close condition is a command line that opens
ONE session around the whole loop. :func:`apply_outstanding` is that, and the
four tests at the top of this file are the proof: the lock is observed HELD from
inside the loop, and each of the three refusals is measured against the file's
own bytes rather than argued from the call order.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track.
"""

from __future__ import annotations

import io
import json
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.adopt import apply as adopt_apply
from cratekit.adopt import apply_cli
from cratekit.adopt import plan as adopt_plan
from cratekit.cli import registry
from cratekit.core import config, jobs, rb_writer, session, tags, taxonomy
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode
from tests.test_adoption import TREE_ID, _bucket_and_genre, _plan_of, _row
from tests.test_config import valid_data
from tests.test_tags import _synth

#: A volume identity that is not the configured one. Any string that differs
#: would do; it is named once so the two tests that need it cannot drift apart.
FOREIGN_VOLUME = "0000-0000"


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library, monkeypatch):
    resolved = config.from_dict(valid_data(library))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    return resolved


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


@pytest.fixture
def acknowledged(cfg):
    """A machine that has answered the backup question, which is two of three gates.

    Recorded through the real ``record_acknowledgment`` rather than by writing the
    file, so a change to what an acknowledgment must contain fails here instead of
    being satisfied by a fixture that knows last year's shape.
    """
    session.record_acknowledgment(cfg, terminal=lambda: True)
    return cfg


def _matching(cfg_value):
    """An identity provider that answers with the configured volume."""
    return lambda _path: cfg_value.library.volume_id


def _one_track_plan(cfg_value, declared_taxonomy) -> tuple[adopt_plan.AdoptionPlan, Path]:
    """A plan with exactly one applicable entry, over a real file on disk.

    The file is REAL because the property under test is what reaches a user's
    file, and a plan over a path nothing backs would let every assertion below
    pass on a run that wrote nowhere.
    """
    _bucket, genre = _bucket_and_genre(declared_taxonomy)
    music = Path(cfg_value.library.root) / "Music"
    path = _synth(music, ".flac")
    tags.write_genre(path, "Original Genre")
    plan = _plan_of(cfg_value, declared_taxonomy, [_row(cfg_value, path.name, genre, "c-1")])
    assert plan.applicable(), "the fixture built a plan with nothing to apply"
    return plan, path


def _bytes_of(path: Path) -> bytes:
    return path.read_bytes()


# ═══════════════════════════════════════════════════════════════════════════
# The session. This is the unit.
# ═══════════════════════════════════════════════════════════════════════════


def test_the_whole_loop_runs_with_the_library_lock_actually_held(
    acknowledged, declared, monkeypatch
):
    """The lock is observed FROM INSIDE the loop, not inferred from the call order.

    ``tag_value`` is called once per entry, in the middle of the pass, so reading
    the lock's recorded holder there answers the question the residual asks:
    while a user's file is being rewritten, is the whole-run lock held. Asserting
    that ``apply_outstanding`` calls ``assert_gates`` would have been a claim
    about this module's source; this is a measurement of the disk.
    """
    plan, path = _one_track_plan(acknowledged, declared)
    holders: list[object] = []

    def tag_value(_entry, _declared):
        holders.append(session.read_lock_holder(session.lock_path(acknowledged)))
        return "Adopted Genre"

    report, _memberships = apply_cli.apply_outstanding(
        acknowledged,
        plan,
        declared,
        actor="a-person",
        tag_value=tag_value,
        identity_provider=_matching(acknowledged),
        mount_enumerator=lambda: (),
    )

    assert len(holders) == 1, "the loop did not reach the one entry the plan holds"
    assert holders[0] is not None, (
        "the tag write happened with no holder recorded against the library lock, "
        "which is the residual's condition unchanged"
    )
    assert len(report.applied) == 1
    assert tags.read_genre_from_file(path) == "Adopted Genre"


def test_the_analysis_watch_is_armed_on_the_library_root(acknowledged, declared):
    """R17's fifth surface, runtime half. The watch has to WATCH something.

    ``analysis_roots`` defaults to empty in ``assert_gates`` and a watch over no
    roots reports a clean session whatever happened to the library's grids, which
    is worse than an absent guard. So "the root is named" cannot be asserted by
    reading the call; it is asserted by putting a real analysis file under the
    library, moving it while the loop is running, and requiring the session to
    refuse.

    THE FILE MOVES FROM INSIDE ``tag_value``, which is the middle of the pass.
    Moving it before or after would be a test of ``analysis_files_unmoved`` rather
    than of whether this verb armed it over the right roots.
    """
    plan, _path = _one_track_plan(acknowledged, declared)
    grid = Path(acknowledged.library.root) / "Music" / "ANLZ0001.DAT"
    grid.write_bytes(b"not a real grid, and never written by this product")

    def tag_value(_entry, _declared):
        grid.rename(grid.with_name("ANLZ0002.DAT"))
        return "Adopted Genre"

    with pytest.raises(CratekitError):
        apply_cli.apply_outstanding(
            acknowledged,
            plan,
            declared,
            actor="a-person",
            tag_value=tag_value,
            identity_provider=_matching(acknowledged),
            mount_enumerator=lambda: (),
        )


def test_the_workflow_name_and_the_registry_verb_name_cannot_drift():
    """One verb name lives in two modules, and nothing compared them.

    ``WORKFLOW`` is what the session log records this run under, and
    ``registry.entry("adopt.apply").name`` is what every other surface calls the
    same verb. They are the same string today, which is exactly why a mutation
    that renames one measures nothing: no fixture reads the session log, so the
    drift would be silent and a person looking for their adoption run in the log
    would not find it. This is the "one symbol meaning two things in two modules"
    shape, and the only thing that can see it is a comparison.
    """
    assert apply_cli.WORKFLOW == registry.entry("adopt.apply").name


def test_the_lock_is_released_when_the_pass_finishes(acknowledged, declared):
    """A session that does not close is a library one crash away from unusable.

    Measured by taking the lock again afterwards rather than by reading the
    recorded holder, because clearing the record and releasing the kernel lock are
    two acts and only the second one is what a later run meets.
    """
    plan, _path = _one_track_plan(acknowledged, declared)
    apply_cli.apply_outstanding(
        acknowledged,
        plan,
        declared,
        actor="a-person",
        tag_value=lambda *_: "Adopted Genre",
        identity_provider=_matching(acknowledged),
        mount_enumerator=lambda: (),
    )
    with session.session_lock(acknowledged):
        pass


def test_an_unacknowledged_machine_rewrites_no_file(cfg, declared):
    """Refusal two of three, measured against the file's own bytes.

    The acknowledgment fixture is deliberately NOT used here: this is the state
    every library is in before a person answers the backup question, and it is the
    state adoption is most likely to meet, since adoption is what a person runs on
    a library they have never pointed this tool at.
    """
    plan, path = _one_track_plan(cfg, declared)
    before = _bytes_of(path)

    with pytest.raises(CratekitError) as excinfo:
        apply_cli.apply_outstanding(
            cfg,
            plan,
            declared,
            actor="a-person",
            tag_value=lambda *_: "Adopted Genre",
            identity_provider=_matching(cfg),
            mount_enumerator=lambda: (),
        )

    assert excinfo.value.cause.code == ExitCode.ACK_REQUIRED
    assert _bytes_of(path) == before, (
        "a refused apply rewrote the file anyway, which is a refusal that has "
        "already done the thing it refused"
    )
    assert adopt_apply.read(cfg).entry_ids() == frozenset()


def test_a_volume_whose_identity_moved_rewrites_no_file(acknowledged, declared):
    """Refusal three of three. The library is somewhere else, so nothing is touched.

    This is the refusal that must happen before any path is resolved, and the file
    is the only witness that can tell "refused first" from "refused after".
    """
    plan, path = _one_track_plan(acknowledged, declared)
    before = _bytes_of(path)

    with pytest.raises(CratekitError) as excinfo:
        apply_cli.apply_outstanding(
            acknowledged,
            plan,
            declared,
            actor="a-person",
            tag_value=lambda *_: "Adopted Genre",
            identity_provider=lambda _path: FOREIGN_VOLUME,
            mount_enumerator=lambda: (),
        )

    assert excinfo.value.cause.code == ExitCode.LIBRARY_UNAVAILABLE
    assert _bytes_of(path) == before
    assert adopt_apply.read(acknowledged).entry_ids() == frozenset()


def test_a_second_run_holding_the_lock_rewrites_no_file(acknowledged, declared):
    """Refusal one of three, and the one the residual measured as absent.

    "Two apply runs over one plan both see the same entries outstanding. Nothing
    stops them reaching the FILE twice." The lock is taken on a separate handle so
    it looks exactly like another run holding it, which is the shape conformance 6
    uses for the same refusal.
    """
    plan, path = _one_track_plan(acknowledged, declared)
    before = _bytes_of(path)

    lock = session.lock_path(acknowledged)
    lock.parent.mkdir(parents=True, exist_ok=True)
    contender = open(lock, "a+")
    try:
        rb_writer._acquire_exclusive(contender)
        with pytest.raises(CratekitError) as excinfo:
            apply_cli.apply_outstanding(
                acknowledged,
                plan,
                declared,
                actor="a-person",
                tag_value=lambda *_: "Adopted Genre",
                identity_provider=_matching(acknowledged),
                mount_enumerator=lambda: (),
            )
    finally:
        contender.close()

    assert excinfo.value.cause.code == ExitCode.LIBRARY_BUSY
    assert _bytes_of(path) == before
    assert adopt_apply.read(acknowledged).entry_ids() == frozenset()


# ═══════════════════════════════════════════════════════════════════════════
# The memberships, and why they are collected rather than written
# ═══════════════════════════════════════════════════════════════════════════


def test_the_memberships_are_collected_and_match_what_the_loop_reached(
    acknowledged, declared
):
    """What comes back is the mapping the tree writer takes, for the entries PLACED.

    Compared against ``membership_plan`` over the applied entries rather than over
    the whole plan. The two are equal here and are not the same claim: a second
    derivation from the plan would put back an entry the loop failed, which is the
    difference between reporting what was done and reporting what was intended.
    """
    plan, _path = _one_track_plan(acknowledged, declared)
    report, memberships = apply_cli.apply_outstanding(
        acknowledged,
        plan,
        declared,
        actor="a-person",
        tag_value=lambda *_: "Adopted Genre",
        identity_provider=_matching(acknowledged),
        mount_enumerator=lambda: (),
    )

    landed = [entry for entry in plan.applicable() if entry.entry_id in set(report.applied)]
    assert dict(memberships) == adopt_apply.membership_plan(landed, declared)
    assert memberships, "the loop placed an entry and reported no membership for it"


def test_the_place_handed_down_writes_nothing_to_the_database(acknowledged, declared):
    """Sessions do not nest, and this is what stops the composition arising.

    ``cratekit.write.trees.write_tree_membership`` opens its own session and
    refuses a caller-supplied gates factory, so a ``place`` that called it from
    inside this session would meet ``SessionComposition`` on every apply. The
    guarantee is that the collector touches no database at all, and it is measured
    by driving a pass and asserting the library's database file is untouched,
    rather than by reading the collector's body.
    """
    plan, _path = _one_track_plan(acknowledged, declared)
    db = Path(acknowledged.library.db_path)
    before = db.stat().st_mtime_ns if db.exists() else None

    apply_cli.apply_outstanding(
        acknowledged,
        plan,
        declared,
        actor="a-person",
        tag_value=lambda *_: "Adopted Genre",
        identity_provider=_matching(acknowledged),
        mount_enumerator=lambda: (),
    )

    after = db.stat().st_mtime_ns if db.exists() else None
    assert after == before, "the collector reached the database it is written not to touch"


def test_a_nested_session_is_refused_rather_than_deadlocking(acknowledged, declared):
    """The composition the collector avoids, driven once so the reason is not a claim.

    If a later unit hands ``apply_outstanding`` a ``place`` that opens its own
    session, this is what it meets. Proving it here means the module docstring's
    argument is a measured fact rather than a reading of ``session_lock``.
    """
    plan, _path = _one_track_plan(acknowledged, declared)

    def nesting(_entry, _folder, _sub):
        with session.session_lock(acknowledged):
            pass

    with pytest.raises(session.SessionComposition):
        with session.assert_gates(
            acknowledged,
            workflow=apply_cli.WORKFLOW,
            analysis_roots=(acknowledged.library.root,),
            identity_provider=_matching(acknowledged),
            mount_enumerator=lambda: (),
        ):
            nesting(plan.applicable()[0], "folder", "sub")


# ═══════════════════════════════════════════════════════════════════════════
# The approval, the gate, and the shell
# ═══════════════════════════════════════════════════════════════════════════


def test_the_approval_names_whoever_answered_the_gate(acknowledged, declared):
    """R34. The ledger records the actor, so the record says who asserted it.

    Read off the APPLIED LEDGER rather than off the report, because the ledger is
    what outlives the process and is what a person auditing an adoption reads.
    """
    plan, _path = _one_track_plan(acknowledged, declared)
    apply_cli.apply_outstanding(
        acknowledged,
        plan,
        declared,
        actor="the-approver",
        tag_value=lambda *_: "Adopted Genre",
        identity_provider=_matching(acknowledged),
        mount_enumerator=lambda: (),
    )
    ledger = adopt_apply.read(acknowledged)
    actors = {entry.actor for entry in ledger.applied}
    assert actors == {"the-approver"}


def test_the_approval_gate_is_found_by_digest_source_not_by_position():
    """Reordering the declared gates must not change which question is asked.

    The verb declares two, and the shared cloud-sync one is raised by the guarded
    writer rather than asked by this handler. Indexing position zero would bind
    the handler to the order they happen to be written in, and the failure would
    be silent: the verb would ask a question about cloud sync and treat the answer
    as an approval to rewrite files.
    """
    entry = registry.entry("adopt.apply")
    assert apply_cli._approval_gate(entry).name == "adopt.apply.approve"

    reversed_entry = replace(entry, gates=tuple(reversed(entry.gates)))
    assert apply_cli._approval_gate(reversed_entry).name == "adopt.apply.approve"


def test_a_verb_declaring_no_plan_digested_gate_refuses_rather_than_applying():
    """The other side of the lookup. An absent question is not a granted answer."""
    entry = replace(registry.entry("adopt.apply"), gates=())
    with pytest.raises(CratekitError) as excinfo:
        apply_cli._approval_gate(entry)
    assert excinfo.value.cause.reason == "internal-error"


def test_the_resume_names_the_job_rather_than_restating_the_request():
    """The contract every long-running verb owes, and the reason it is a function."""

    class _Job:
        job_id = "job-7"

    assert apply_cli.adopt_apply_argv(_Job()) == ["adopt", "apply", "--job", "job-7"]


# ═══════════════════════════════════════════════════════════════════════════
# The gap, stated as a test rather than only as a docstring
# ═══════════════════════════════════════════════════════════════════════════


def test_the_census_is_empty_because_no_unit_lands_a_collection_reader(cfg, declared):
    """The absent input, driven, so it is a measured fact and not a claim in prose.

    ``adopt.scan`` shipped in this same position and said so in the same words.
    This guard is what makes the day a collection reader lands VISIBLE: it fails,
    and whoever landed the reader is told that the plan this verb builds is no
    longer empty and that the session below it is now doing real work.
    """
    assert apply_cli.census(cfg) == ()
    plan = apply_cli.current_plan(cfg, declared)
    assert plan.entries == ()
    assert plan.applicable() == ()
    assert plan.tree == declared.tree.id


def test_an_empty_plan_still_has_a_digest_to_approve_against(cfg, declared):
    """The gate fires on an empty plan, so the digest has to exist and be stable.

    Two builds of the same empty plan give one digest, which is what makes a
    recorded approval survive the resume that re-derives the plan. A digest that
    moved between two identical runs would make every approval stale on the first
    resume.
    """
    first = apply_cli.current_plan(cfg, declared).digest()
    second = apply_cli.current_plan(cfg, declared).digest()
    assert first == second
    assert first


def test_the_tree_comes_off_the_declared_taxonomy_rather_than_a_flag(cfg):
    """R19. A taxonomy declares exactly one routing tree, by stable identifier.

    Driven against a MODIFIED taxonomy rather than against the shipped one, so the
    assertion is that the value is resolved and not that it happens to equal the
    constant this repository ships.
    """
    declared = taxonomy.default_taxonomy()
    moved = replace(declared, tree=replace(declared.tree, id=TREE_ID))
    assert apply_cli.current_plan(cfg, moved).tree == TREE_ID


# ═══════════════════════════════════════════════════════════════════════════
# The shell, driven through the real dispatcher
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def installed(library, monkeypatch):
    """A machine the real ``cli.run`` can load, rather than a monkeypatched load.

    The ``cfg`` fixture above patches ``config.load`` so the engine-level tests
    never touch disk. The dispatcher loads configuration for itself, in the parser
    construction every invocation runs first, so a driven test needs the file to
    genuinely exist. Both fixtures are kept: patching is right for the loop, and
    saving is the only thing that proves the verb reaches its own handler.
    """
    resolved = config.from_dict(valid_data(library))
    config.save(resolved)
    config.reset_cache()
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    return resolved


def _drive(argv: list[str]) -> tuple[int, dict]:
    """Run the real dispatcher and return the status with the parsed envelope."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def _queued(cfg_value) -> list:
    del cfg_value
    with jobs.open_store() as store:
        return [
            held
            for held in jobs.list_jobs(store)
            if held.handler_key == registry.entry("adopt.apply").handler_key
        ]


def test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest(installed):
    """R34's two acts, driven, and then what the frozen payload actually holds.

    THE PAYLOAD IS THE ASSERTION, not the exit code. A resume rebuilds the plan
    from scratch, so the digest the approval was recorded against has to travel
    with the job or nothing downstream can tell a resume of THIS approved plan
    from a resume of a plan that has since moved. Conformance 3 drives this verb
    to OK and asserts nothing about what was queued, which is why this is here.
    """
    verb = registry.entry("adopt.apply")
    expected = apply_cli.current_plan(installed, taxonomy.default_taxonomy())

    first_code, refused = _drive(["adopt", "apply"])
    assert first_code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == "adopt.apply.approve"
    run_id = refused["run_id"]

    decided, _ = _drive(
        ["run", "decide", run_id, "adopt.apply.approve", "approve", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK)

    code, envelope = _drive(["--run", run_id, "adopt", "apply"])
    assert code == int(ExitCode.OK), envelope

    held = _queued(installed)
    assert len(held) == 1, "an approved run queued something other than exactly one job"
    assert held[0].payload["tree"] == expected.tree
    assert held[0].payload["digest"] == expected.digest(), (
        "the queued job does not carry the digest its approval was recorded "
        "against, so a resume cannot tell this plan from one that has moved"
    )
    assert envelope["data"]["job_id"] == held[0].job_id
    assert envelope["verb"] == verb.name


def test_a_declined_run_queues_nothing_at_all(installed):
    """Abort is a real answer, and the measurement is the queue rather than the word.

    A verb that reported NO_OP and queued the pass anyway would read correctly in
    every envelope anyone looks at, and would apply a plan the person declined the
    next time a driver picked the queue up.
    """
    first_code, refused = _drive(["adopt", "apply"])
    assert first_code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]

    decided, _ = _drive(
        ["run", "decide", run_id, "adopt.apply.approve", "abort", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK)

    code, envelope = _drive(["--run", run_id, "adopt", "apply"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["job_id"] is None
    assert _queued(installed) == [], "a declined adoption was queued anyway"
