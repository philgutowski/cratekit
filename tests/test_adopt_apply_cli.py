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
from cratekit.adopt import apply_cli, collection
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import config, jobs, preflight, rb_writer, session, tags, taxonomy
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode
from tests import adopt_fixtures
from tests.test_adoption import TREE_ID, _bucket_and_genre, _plan_of, _readable, _row
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION
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


@pytest.fixture(autouse=True)
def _reader_cache():
    """No test may inherit another test's library.

    The collection reader memoizes per process, keyed on the resolved database
    path, and every test here builds a library at the same configured path inside
    its own temporary directory. Without this, the second test in a session would
    census the first test's rows.
    """
    collection.reset_cache()
    yield
    collection.reset_cache()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What this machine cannot speak for on behalf of a temporary library.

    The cloud-sync marker is read by the canary on every open, including a read
    only one, and this machine's answer says nothing about a database built in a
    temporary directory. Patched at the seam the guard resolves; that the canary
    refuses a tripped marker is proved directly in ``tests/test_rb_writer_db.py``.
    """
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )


@pytest.fixture
def cfg(library, monkeypatch):
    resolved = config.from_dict(valid_data(library))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    return resolved


#: The library every census test here reads. One readable routable track, one row
#: whose file is not on disk, and one tombstone, so a census over it exercises
#: three of the derivation's outcomes rather than only the happy one.
def _tracks(declared_taxonomy) -> tuple[adopt_fixtures.Track, ...]:
    _bucket, genre = _bucket_and_genre(declared_taxonomy)
    return (
        adopt_fixtures.Track("r-ok", "present.flac", genre),
        adopt_fixtures.Track("r-missing", "absent.flac", genre, on_disk=False),
        adopt_fixtures.Track("r-gone", "removed.flac", genre, deleted=True),
    )


@pytest.fixture
def seeded(cfg, declared):
    """Configuration pointing at a disposable database holding those three rows."""
    adopt_fixtures.build(cfg, _tracks(declared))
    collection.reset_cache()
    return cfg


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
    # BESIDE THE MUSIC FOLDER, NOT INSIDE IT, and that placement is the assertion.
    # A grid under Music is still watched when the roots are narrowed to Music, so
    # a test that put it there would hold "the watch is armed" and would say
    # nothing about WHICH roots. Measured: narrowing the declared root to
    # cfg.library.root / "Music" killed zero tests until this file moved up one
    # level, and kills this one now.
    grid = Path(acknowledged.library.root) / "ANLZ0001.DAT"
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


def test_the_analysis_watch_reaches_a_share_outside_the_library_root(
    acknowledged, declared, tmp_path
):
    """R-14. The grids live beside the database, and the database may be elsewhere.

    An acknowledged database outside the library root takes its analysis share
    with it, so the library root holds no grid at all and a watch armed there
    alone fingerprints nothing. The grid here is rewritten from inside the pass
    and has to be seen, which the library root alone cannot do: measured by the
    assertion before the drive rather than argued.
    """
    share = tmp_path / "home" / "rekordbox" / "share"
    outside = replace(
        acknowledged,
        library=replace(
            acknowledged.library,
            db_path=share.parent / "master.db",
            db_outside_root_acknowledged_on="2026-09-11",
        ),
    )
    plan, _path = _one_track_plan(outside, declared)
    grid = share / "PIONEER" / "USBANLZ" / "8d2" / "one" / "ANLZ0000.DAT"
    grid.parent.mkdir(parents=True)
    grid.write_bytes(b"not a real grid, and never written by this product")
    assert grid not in session.analysis_files_under([outside.library.root]), (
        "the grid sits under the library root, so this cannot show the root alone misses it"
    )

    def tag_value(_entry, _declared):
        grid.write_bytes(b"a rewritten grid, longer than the one that was there")
        return "Adopted Genre"

    with pytest.raises(CratekitError) as excinfo:
        apply_cli.apply_outstanding(
            outside,
            plan,
            declared,
            actor="a-person",
            tag_value=tag_value,
            identity_provider=_matching(outside),
            mount_enumerator=lambda: (),
        )
    cause = excinfo.value.cause
    assert cause.reason == "anlz-modified", cause
    assert any(str(grid) in line for line in cause.detail["changed"]), cause.detail


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

    Compared against ``membership_locations`` over the applied entries rather than
    over the whole plan. The two are equal here and are not the same claim: a
    second derivation from the plan would put back an entry the loop failed, which
    is the difference between reporting what was done and reporting what was
    intended.

    THE VALUES ARE LOCATIONS AND NOT CONTENT IDENTIFIERS, which is U55's
    correction. ``write_tree_membership`` decodes every value of its ``plan`` as a
    recorded location and looks it up in an index keyed on resolved paths, so a
    content identifier resolves to nothing, every entry comes back UNRESOLVED, and
    the write reports a session that added no rows as a session that ran.
    ``membership_plan`` still groups identifiers and is another unit's function;
    that divergence is the residual, and this assertion is what keeps this side
    right.
    """
    plan, path = _one_track_plan(acknowledged, declared)
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
    assert dict(memberships) == apply_cli.membership_locations(landed, declared)
    assert memberships, "the loop placed an entry and reported no membership for it"
    placed = [value for values in memberships.values() for value in values]
    assert placed and all(str(path) == value for value in placed), (
        "the collector grouped something that is not a location, so handing it to "
        "write_tree_membership would match nothing and report a clean session"
    )
    assert not set(placed) & {entry.content_id for entry in plan.applicable()}, (
        "the collector is back to grouping content identifiers, which is the defect"
    )


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


def test_the_resume_names_the_job_and_carries_the_run_that_holds_the_approval():
    """The contract every long-running verb owes, in both shapes it has to answer.

    A job frozen by this build carries its run, so the resume continues the run
    holding the recorded approval. A job frozen by an older build carries none,
    and the resume must still be a valid command line rather than a crash: it
    refuses at the gate resumably, which is the state that job was already in.
    """

    class _Job:
        job_id = "job-7"
        payload = {jobs.GATE_RUN_KEY: "run-3"}

    class _Older:
        job_id = "job-7"
        payload = {}

    assert apply_cli.adopt_apply_argv(_Job()) == [
        "--run", "run-3", "adopt", "apply", "--job", "job-7",
    ]
    assert apply_cli.adopt_apply_argv(_Older()) == ["adopt", "apply", "--job", "job-7"]


# ═══════════════════════════════════════════════════════════════════════════
# The gap, stated as a test rather than only as a docstring
# ═══════════════════════════════════════════════════════════════════════════


def test_the_census_is_the_library_and_every_row_of_it_is_carried(seeded, declared):
    """The reader landed, so the census is the person's own collection.

    THIS REPLACES A GUARD THAT PINNED THE EMPTINESS, and replacing it rather than
    deleting it is the point. That guard was safe only because its subject was
    unimplemented, and the obvious restatement of such a guard measures nothing;
    ``docs/solutions/workflow-issues`` records the shape under the title about a
    guard expiring the day somebody implements its subject. What is asserted now
    is the derivation: every live row comes back classified, the tombstone is
    skipped, and the one row whose file is on disk with a routable genre is the
    only one the plan can act on.
    """
    scanned = apply_cli.census(seeded, declared)
    by_id = {track.content_id: track for track in scanned}

    assert set(by_id) == {"r-ok", "r-missing", *adopt_fixtures.BASELINE_CONTENT_IDS}, (
        "the census dropped a row, or invented one; a tombstone must be skipped "
        "and every other row must be carried"
    )
    assert by_id["r-ok"].readability is adopt_scan.Readability.READABLE
    assert by_id["r-ok"].disposition is adopt_scan.Disposition.ROUTE
    assert by_id["r-missing"].readability is adopt_scan.Readability.MISSING
    assert by_id["r-missing"].disposition is adopt_scan.Disposition.EXCLUDED

    plan = apply_cli.current_plan(seeded, declared)
    assert plan.content_ids() == set(by_id)
    assert [entry.content_id for entry in plan.applicable()] == ["r-ok"]
    assert plan.tree == declared.tree.id


def test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing(cfg, declared):
    """Stated as the LIMIT of what the census can say, rather than left implicit.

    ``scan_rows`` skips a deleted row, so a library whose every row is a removal
    produces the same census as a library with no rows at all. The two are
    genuinely different facts and only the COLLECTION can tell them apart, which
    is why ``adopt.scan`` derives its items from the collection and reports the
    two zeroes with different warnings.
    """
    adopt_fixtures.build(
        cfg, (adopt_fixtures.Track("r-gone", "gone.flac", "Techno", deleted=True),)
    )
    collection.reset_cache()
    tombstoned = apply_cli.census(cfg, declared)
    live_rows = [row for row in collection.read_collection(cfg) if not row.deleted]

    adopt_fixtures.build(cfg, ())
    collection.reset_cache()
    empty = apply_cli.census(cfg, declared)

    assert adopt_scan.categories(tombstoned) == adopt_scan.categories(empty)
    assert len(tombstoned) == len(empty) == len(adopt_fixtures.BASELINE_CONTENT_IDS)
    assert len(live_rows) == len(adopt_fixtures.BASELINE_CONTENT_IDS), (
        "the collection is what tells the two zeroes apart, and it must be able to"
    )


def test_two_builds_of_one_unchanged_library_give_one_digest(seeded, declared):
    """What makes a recorded approval survive the resume that re-derives the plan.

    A digest that moved between two identical runs would make every approval stale
    on the first resume, which is the property the frozen ``digest`` payload key
    and the worker's own comparison both rest on. Driven across a cleared reader
    cache so the second build genuinely re-reads.
    """
    first = apply_cli.current_plan(seeded, declared).digest()
    collection.reset_cache()
    second = apply_cli.current_plan(seeded, declared).digest()
    assert first == second
    assert first


def test_the_tree_comes_off_the_declared_taxonomy_rather_than_a_flag(seeded):
    """R19. A taxonomy declares exactly one routing tree, by stable identifier.

    Driven against a MODIFIED taxonomy rather than against the shipped one, so the
    assertion is that the value is resolved and not that it happens to equal the
    constant this repository ships.
    """
    declared = taxonomy.default_taxonomy()
    moved = replace(declared, tree=replace(declared.tree, id=TREE_ID))
    assert apply_cli.current_plan(seeded, moved).tree == TREE_ID


def test_the_census_classifies_against_the_taxonomy_its_caller_resolved(seeded):
    """``declared`` is a PARAMETER, and this is the assertion that makes it one.

    ``census`` resolved its own taxonomy until U55 while ``current_plan`` resolved
    ``sub`` from the one IT was handed, so one plan entry could be built from two
    taxonomies at once. The guard above could not see it: it drives a modified
    taxonomy and reads back only the TREE identifier, which
    ``build_adoption_plan`` takes as its own argument. Driven here by handing the
    census a taxonomy that declares the fixture's genre too coarse to be a source.
    If the census asked ``default_taxonomy`` for itself, the row would still route.
    """
    declared = taxonomy.default_taxonomy()
    routed = apply_cli.census(seeded, declared)
    assert any(track.disposition is adopt_scan.Disposition.ROUTE for track in routed)

    _bucket, genre = _bucket_and_genre(declared)
    narrowed = replace(
        declared,
        fallback=replace(
            declared.fallback,
            too_coarse_as_source=(*declared.fallback.too_coarse_as_source, genre),
        ),
    )
    collection.reset_cache()
    starved = apply_cli.census(seeded, narrowed)
    assert not any(track.disposition is adopt_scan.Disposition.ROUTE for track in starved), (
        "the census routed against a taxonomy its caller did not pass, so an "
        "entry can be built from two taxonomies at once"
    )


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
    resolved = config.from_dict(
        valid_data(
            library,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    config.save(resolved)
    config.reset_cache()
    # A LIBRARY WITH SOMETHING APPLICABLE IN IT, because the verb now refuses to
    # queue a job over a plan with nothing to place. A fixture with an empty
    # database would drive every test below down the no-op path.
    adopt_fixtures.build(resolved, _tracks(taxonomy.default_taxonomy()))
    collection.reset_cache()
    # THE MACHINE IS SET UP RATHER THAN HALF SET UP, because the resume branch now
    # drives real work and that work opens a destructive session. A fixture that
    # left the volume identity unanswered would make every resume test below fail
    # on the gate instead of on the thing it is asking about.
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(resolved, terminal=lambda: True)
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
    assert envelope["data"]["job_id"] == "", (
        "R-234: cli.output requires job_id to be a string, so a null here failed "
        "the declared job_state/1 schema this verb emits"
    )
    assert _queued(installed) == [], "a declined adoption was queued anyway"


def test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused(
    installed, monkeypatch
):
    """The digest is what the gate is offered, and it is what makes a stale answer visible.

    ``digest_source="plan"`` on this verb's gate is only worth anything if the
    handler actually OFFERS the digest, and nothing else in this file could see
    that: the queued payload digest is computed straight from the plan, so it
    matches whether or not the gate was ever told. Measured: dropping
    ``digest=plan.digest()`` from the require call killed zero tests across the
    whole suite before this one existed.

    THE PLAN IS MOVED BY GIVING THE CENSUS A ROW, which is the one honest way to
    move it here, and it is also the shape a real library changes by: somebody
    approves an adoption, the collection gains a track, and the plan they
    approved is no longer the plan that would be applied.
    """
    plan_before = apply_cli.current_plan(installed, taxonomy.default_taxonomy())

    _code, refused = _drive(["adopt", "apply"])
    run_id = refused["run_id"]
    decided, _ = _drive(
        ["run", "decide", run_id, "adopt.apply.approve", "approve", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK)

    music = Path(installed.library.root) / "Music"
    path = _synth(music, ".flac")
    _bucket, genre = _bucket_and_genre(taxonomy.default_taxonomy())
    scanned = tuple(
        adopt_scan.scan_rows(
            [_row(installed, path.name, genre, "c-moved")],
            taxonomy.default_taxonomy(),
            root=installed.library.root,
            probe=_readable,
        )
    )
    monkeypatch.setattr(apply_cli, "census", lambda _cfg, _declared: scanned)
    assert apply_cli.current_plan(installed, taxonomy.default_taxonomy()).digest() != (
        plan_before.digest()
    ), "the fixture did not actually move the plan, so the assertion below is empty"

    code, envelope = _drive(["--run", run_id, "adopt", "apply"])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert _queued(installed) == [], "a plan that moved after approval was queued anyway"


def test_the_resume_the_job_driver_spawns_can_actually_proceed(installed):
    """The argv this verb hands the driver has to be one the verb will accept.

    THE DEFECT THIS GUARDS, driven on 2026-08-23 before it was fixed. The approval
    gate is explicit, so R34 makes it answerable only by a separate recorded act
    against a run. The resume argv named the job and nothing else, so the child
    minted a fresh run, met the gate with nothing recorded against it, and exited
    DECISION_REQUIRED. Every respawn did the same, so the job could never be
    advanced by anything, and no test in this file or in the conformance suite
    could see it: conformance 3 drives the verb WITHOUT a job, and every other
    test here calls the engine directly.

    So this drives the real ``argv_for`` output through the real dispatcher, which
    is the only thing that can tell a resume that works from one that is refused
    for ever.
    """
    _code, refused = _drive(["adopt", "apply"])
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, "adopt.apply.approve", "approve", "--actor", "a-person"])
    approved, envelope = _drive(["--run", run_id, "adopt", "apply"])
    assert approved == int(ExitCode.OK), envelope

    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    argv = cli_jobs.argv_for(job)
    assert "--job" in argv and job.job_id in argv

    code, resumed = _drive(argv)
    assert code != int(ExitCode.DECISION_REQUIRED), (
        f"the resume the driver spawns refuses its own gate: {resumed.get('cause')}. "
        f"A job whose own resume cannot answer its gate is a job nothing can advance"
    )
    assert len(_queued(installed)) == 1, "the resume queued a second record"

    # WHAT IT REACHES, now that the resume drives instead of reporting. The
    # membership write refuses because this library's taxonomy tree has never
    # been cut over to the database, which is the state every real library is in
    # and which no shipped verb can change. That refusal arriving here is the
    # proof the resume got PAST the gate: a run that had not would carry
    # ``decision-required`` instead, and nothing about the tree would be reached.
    assert resumed["cause"]["reason"] == "no-evidence", resumed
    assert resumed["cause"]["inner"]["reason"] == "tree-unconverged", resumed
    with jobs.open_store() as store:
        assert jobs.get(store, job.job_id).state is jobs.JobState.FAILED
    assert adopt_apply.read(installed).entry_ids() == frozenset(), (
        "the applied ledger marked entries over an adoption that placed nothing"
    )


def test_a_resume_reconciles_a_claim_a_dead_driver_left_behind(installed):
    """Reconcile, not get. A row saying running while no driver holds the lock is a lie.

    Measured: swapping ``jobs.reconcile`` for ``jobs.get`` in the resume branch
    killed zero tests across the whole suite before this one existed, because
    nothing drove the resume branch at all.

    THE JOB IS PUT INTO RUNNING WITH NO LOCK HELD, which is exactly the state a
    killed driver leaves: the queue cannot see for itself that the process is
    gone, and a report that trusted the row would tell a person their adoption is
    in progress when nothing is running it.
    """
    _code, refused = _drive(["adopt", "apply"])
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, "adopt.apply.approve", "approve", "--actor", "a-person"])
    _approved, envelope = _drive(["--run", run_id, "adopt", "apply"])
    job_id = envelope["data"]["job_id"]

    with jobs.open_store() as store:
        jobs.transition(store, job_id, jobs.JobState.RUNNING)
        assert jobs.get(store, job_id).state is jobs.JobState.RUNNING

    code, resumed = _drive(["--run", run_id, "adopt", "apply", "--job", job_id])
    assert code != int(ExitCode.OK)
    assert resumed["cause"]["reason"] == "no-evidence", resumed

    # THE STALE ROW DID NOT SURVIVE. A resume that reported ``jobs.get`` would
    # have carried RUNNING out to the person; the job reaches a terminal state
    # instead, which is only possible because the row was re-derived first and
    # the item was then claimed and attempted.
    with jobs.open_store() as store:
        reconciled = jobs.get(store, job_id)
        assert reconciled.state is jobs.JobState.FAILED
        assert [item.state for item in jobs.items(store, job_id)] == [jobs.ItemState.FAILED]


# ═══════════════════════════════════════════════════════════════════════════
# R-693: the approval gate shows the plan it asks about
# ═══════════════════════════════════════════════════════════════════════════


def _expected_document(installed) -> dict:
    return adopt_plan.to_json(apply_cli.current_plan(installed, taxonomy.default_taxonomy()))


def _shown_matches(shown: dict, document: dict) -> None:
    assert shown["items"] == document["entries"]
    assert shown["items"], "a plan with nothing in it proves nothing about the screen"
    assert shown["digest"] == document["digest"]
    assert shown["count"] == len(document["entries"])
    assert shown["tree"] == document["tree"]
    assert shown["counts"] == document["counts"]
    assert shown["collisions"] == document["collisions"]


def test_the_approval_gate_shows_every_entry_the_digest_was_taken_over(installed):
    """The gate carried the question and not one entry (R-693). Its ``shown``
    now holds the plan document's entries, every one and not only the
    applicable ones, with the digest, the tree, the counts and the collisions
    the digest was taken over."""
    document = _expected_document(installed)
    code, refused = _drive(["adopt", "apply"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    _shown_matches(refused["cause"]["detail"]["shown"], document)
    assert _queued(installed) == []


def test_the_resume_gate_shows_the_rebuilt_plan_it_asks_about(installed):
    """A resume on a run holding no answer meets the same gate over the plan
    rebuilt from the census, and shows it the same way."""
    document = _expected_document(installed)
    _code, refused = _drive(["adopt", "apply"])
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, "adopt.apply.approve", "approve", "--actor", "a-person"])
    _approved, envelope = _drive(["--run", run_id, "adopt", "apply"])
    job_id = envelope["data"]["job_id"]

    code, refused = _drive(["adopt", "apply", "--job", job_id])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == "adopt.apply.approve"
    _shown_matches(refused["cause"]["detail"]["shown"], document)
